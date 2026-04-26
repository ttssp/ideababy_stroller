"""
LLM 文件缓存 — T005
结论: 按 sha256 键缓存 API 响应，命中跳过 API 节省成本 (D11)
细节:
  - 缓存键 = sha256(advisor_week_id + ticker + prompt_template_version + model)
  - prompt_template_version 必须含，防止 prompt 改但 cache 不更新 (D11 spec)
  - 原子写: 写 tmp 文件 + os.replace (rename)，防止读到半写文件
  - invalidate(template_version): 元数据存在文件头，scan-and-delete 匹配的文件
  - 默认路径: ~/decision_ledger/llm_cache/
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# 默认缓存目录
_DEFAULT_CACHE_DIR = Path.home() / "decision_ledger" / "llm_cache"

# 元数据 key，存在 JSON 文件顶层
_META_KEY = "_llm_cache_meta"


class LLMCache:
    """
    LLM 响应文件缓存。
    线程安全: os.replace 是原子操作，多进程也安全（单进程项目，但防御性编程）。
    """

    def __init__(self, cache_dir: Path | None = None) -> None:
        self._dir = cache_dir or _DEFAULT_CACHE_DIR
        self._dir.mkdir(parents=True, exist_ok=True)

    # ── 公开接口 ──────────────────────────────────────────────────────────────

    def get(
        self,
        advisor_week_id: str,
        ticker: str,
        prompt_template_version: str,
        model: str,
    ) -> dict[str, Any] | None:
        """
        尝试命中缓存。
        返回: dict (命中) | None (未命中)
        """
        key = self._make_key(advisor_week_id, ticker, prompt_template_version, model)
        path = self._path(key)
        if not path.exists():
            return None
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            # 过滤掉元数据，返回业务数据
            return {k: v for k, v in raw.items() if k != _META_KEY}
        except (json.JSONDecodeError, OSError):
            logger.warning("缓存文件损坏，忽略: %s", path.name)
            return None

    def put(
        self,
        advisor_week_id: str,
        ticker: str,
        prompt_template_version: str,
        model: str,
        data: dict[str, Any],
    ) -> None:
        """
        原子写入缓存条目。
        元数据嵌入文件，供 invalidate 使用。
        """
        key = self._make_key(advisor_week_id, ticker, prompt_template_version, model)
        path = self._path(key)
        tmp_path = path.with_suffix(".tmp")

        # 注入元数据（版本信息，用于 invalidate）
        payload: dict[str, Any] = {
            **data,
            _META_KEY: {
                "prompt_template_version": prompt_template_version,
                "model": model,
                "advisor_week_id": advisor_week_id,
                "ticker": ticker,
            },
        }

        try:
            tmp_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            # 原子 rename（POSIX 保证）
            os.replace(tmp_path, path)
        except OSError as e:
            logger.error("缓存写入失败: %s", e)
            # 清理 tmp
            tmp_path.unlink(missing_ok=True)
            raise

    def invalidate(self, template_version: str) -> int:
        """
        删除指定 template_version 的所有缓存条目。
        返回删除的文件数。
        用于 prompt 升版时批量失效旧缓存。
        """
        deleted = 0
        for path in self._dir.glob("*.json"):
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
                meta = raw.get(_META_KEY, {})
                if meta.get("prompt_template_version") == template_version:
                    path.unlink(missing_ok=True)
                    deleted += 1
                    logger.debug("缓存失效删除: %s (version=%s)", path.name, template_version)
            except (json.JSONDecodeError, OSError):
                # 损坏文件跳过
                continue
        if deleted:
            logger.info("缓存失效: 删除 %d 个条目 (template_version=%s)", deleted, template_version)
        return deleted

    # ── 内部工具 ──────────────────────────────────────────────────────────────

    @staticmethod
    def _make_key(
        advisor_week_id: str,
        ticker: str,
        prompt_template_version: str,
        model: str,
    ) -> str:
        """
        生成缓存键 = sha256(advisor_week_id + ticker + prompt_template_version + model)
        D11 spec: prompt_template_version 必须含，否则 prompt 改 cache 不更新会污染。
        """
        raw = f"{advisor_week_id}|{ticker}|{prompt_template_version}|{model}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _path(self, key: str) -> Path:
        return self._dir / f"{key}.json"
