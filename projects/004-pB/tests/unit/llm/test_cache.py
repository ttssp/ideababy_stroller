"""
LLM 文件缓存测试 — T005 TDD 先写 (红)
结论: 验证 cache get/put/invalidate 语义 + 原子写 + 缓存键含 prompt_template_version
细节:
  - D11: cache_key = sha256(advisor_week_id + ticker + prompt_template_version + model)
  - 原子写: 写 tmp 文件再 rename，防止读到半写文件
  - invalidate(template_version): 删除该版本所有条目
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from decision_ledger.llm.cache import LLMCache

# ── fixture ────────────────────────────────────────────────────────────────────

@pytest.fixture
def cache(tmp_path: Path) -> LLMCache:
    """返回指向 tmp_path 的 LLMCache 实例。"""
    return LLMCache(cache_dir=tmp_path)


# ── test: cache miss → None ────────────────────────────────────────────────────

def test_cache_miss_returns_none_when_key_absent(cache: LLMCache) -> None:
    """结论: 缓存未命中时 get 返回 None。"""
    result = cache.get(
        advisor_week_id="2026-W17",
        ticker="TSM",
        prompt_template_version="conflict_v1",
        model="claude-sonnet-4-6",
    )
    assert result is None


# ── test: put → get 命中 ───────────────────────────────────────────────────────

def test_cache_put_then_get_returns_same_data(cache: LLMCache) -> None:
    """结论: put 后 get 返回相同数据 (序列化/反序列化正确)。"""
    payload = {"direction": "long", "confidence": 0.8}
    cache.put(
        advisor_week_id="2026-W17",
        ticker="TSM",
        prompt_template_version="conflict_v1",
        model="claude-sonnet-4-6",
        data=payload,
    )
    result = cache.get(
        advisor_week_id="2026-W17",
        ticker="TSM",
        prompt_template_version="conflict_v1",
        model="claude-sonnet-4-6",
    )
    assert result == payload


# ── test: 缓存键隔离 — 不同 ticker 不互串 ──────────────────────────────────────

def test_cache_different_tickers_are_isolated(cache: LLMCache) -> None:
    """结论: ticker 不同时 cache key 不同，互不影响。"""
    cache.put(
        advisor_week_id="2026-W17",
        ticker="TSM",
        prompt_template_version="conflict_v1",
        model="claude-sonnet-4-6",
        data={"ticker": "TSM"},
    )
    result = cache.get(
        advisor_week_id="2026-W17",
        ticker="NVDA",
        prompt_template_version="conflict_v1",
        model="claude-sonnet-4-6",
    )
    assert result is None


# ── test: 缓存键必须含 prompt_template_version ─────────────────────────────────

def test_cache_different_template_versions_are_isolated(cache: LLMCache) -> None:
    """结论: prompt_template_version 不同时 cache key 不同，防止 prompt 改但 cache 不更新 (D11)。"""
    cache.put(
        advisor_week_id="2026-W17",
        ticker="TSM",
        prompt_template_version="conflict_v1",
        model="claude-sonnet-4-6",
        data={"version": "v1"},
    )
    # v2 应该 miss
    result = cache.get(
        advisor_week_id="2026-W17",
        ticker="TSM",
        prompt_template_version="conflict_v2",
        model="claude-sonnet-4-6",
    )
    assert result is None


# ── test: 不同 model 隔离 ───────────────────────────────────────────────────────

def test_cache_different_models_are_isolated(cache: LLMCache) -> None:
    """结论: model 不同时 cache key 不同 (Sonnet/Haiku 分开缓存)。"""
    cache.put(
        advisor_week_id="2026-W17",
        ticker="TSM",
        prompt_template_version="conflict_v1",
        model="claude-sonnet-4-6",
        data={"model": "sonnet"},
    )
    result = cache.get(
        advisor_week_id="2026-W17",
        ticker="TSM",
        prompt_template_version="conflict_v1",
        model="claude-haiku-4-5",
    )
    assert result is None


# ── test: invalidate 删除指定 template_version 的条目 ─────────────────────────

def test_cache_invalidate_removes_matching_version(cache: LLMCache) -> None:
    """结论: invalidate('conflict_v1') 删除该版本的所有 cache 文件。"""
    cache.put(
        advisor_week_id="2026-W17",
        ticker="TSM",
        prompt_template_version="conflict_v1",
        model="claude-sonnet-4-6",
        data={"data": "v1"},
    )
    cache.put(
        advisor_week_id="2026-W17",
        ticker="NVDA",
        prompt_template_version="conflict_v1",
        model="claude-sonnet-4-6",
        data={"data": "v1-nvda"},
    )
    cache.put(
        advisor_week_id="2026-W17",
        ticker="TSM",
        prompt_template_version="conflict_v2",
        model="claude-sonnet-4-6",
        data={"data": "v2"},
    )
    cache.invalidate(template_version="conflict_v1")
    # v1 已删除
    assert cache.get("2026-W17", "TSM", "conflict_v1", "claude-sonnet-4-6") is None
    assert cache.get("2026-W17", "NVDA", "conflict_v1", "claude-sonnet-4-6") is None
    # v2 未受影响
    result_v2 = cache.get("2026-W17", "TSM", "conflict_v2", "claude-sonnet-4-6")
    assert result_v2 == {"data": "v2"}


# ── test: 原子写 — 缓存文件实际写到磁盘 ───────────────────────────────────────

def test_cache_put_writes_json_file_to_disk(cache: LLMCache, tmp_path: Path) -> None:
    """结论: put 后 cache_dir 中存在对应 JSON 文件。"""
    cache.put(
        advisor_week_id="2026-W17",
        ticker="TSM",
        prompt_template_version="conflict_v1",
        model="claude-sonnet-4-6",
        data={"key": "value"},
    )
    json_files = list(tmp_path.glob("*.json"))
    assert len(json_files) == 1
    content = json.loads(json_files[0].read_text())
    assert content["key"] == "value"


# ── test: 缓存键格式是 sha256 hex (64字符) ────────────────────────────────────

def test_cache_key_is_sha256_hex(cache: LLMCache, tmp_path: Path) -> None:
    """结论: 缓存文件名 (去掉 .json 后缀) 是 64 字符 sha256 hex。"""
    cache.put(
        advisor_week_id="2026-W17",
        ticker="TSM",
        prompt_template_version="conflict_v1",
        model="claude-sonnet-4-6",
        data={},
    )
    json_files = list(tmp_path.glob("*.json"))
    assert len(json_files) == 1
    stem = json_files[0].stem
    assert len(stem) == 64
    assert all(c in "0123456789abcdef" for c in stem)
