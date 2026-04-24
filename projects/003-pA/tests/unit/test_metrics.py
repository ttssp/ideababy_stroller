"""
tests.unit.test_metrics — pars.ledger.metrics 单元测试。

覆盖点：
1.  append_metric 写一条,read_metrics 读出一条,字段对齐
2.  append_metric 写 100 条,count_metrics 返回 100
3.  read_metrics 按 phase="training" 过滤,只返回 training
4.  read_metrics 按 kind="epoch" 过滤
5.  read_metrics 文件不存在 → 空 iterator(不 raise)
6.  append_metric run_id 目录不存在 → 自动创建父目录
7.  损坏行不中断后续行读取,log warning
8.  append_metric data 含 set → TypeError(不可序列化)
9.  last_metric 空文件返回 None
10. last_metric 按 phase 过滤返回最后匹配的一条
11. 并发 append 测试:10 线程同时 append,最终 count 正确且每行可解析
12. datetime round-trip:append 带 ts= → read 出的 MetricRecord.ts 等于原 datetime
13. data 超大(>8KB) → log warning 但仍写入
"""

from __future__ import annotations

import json
import threading
from datetime import UTC, datetime, timezone
from pathlib import Path
from typing import Any

import pytest

from pars.ledger.metrics import (
    MetricRecord,
    append_metric,
    count_metrics,
    get_metrics_path,
    last_metric,
    read_metrics,
)


# ---------------------------------------------------------------------------
# 辅助 fixture
# ---------------------------------------------------------------------------


@pytest.fixture()
def run_id(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> str:
    """提供一个隔离的 run_id,RECALLKIT_RUN_DIR 指向 tmp_path。"""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))
    return "01HZTEST00000000000000TEST"


@pytest.fixture()
def run_dir_with_file(run_id: str) -> Path:
    """预先创建 metrics.jsonl 所在 run 目录并返回 Path。"""
    p = get_metrics_path(run_id)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


# ---------------------------------------------------------------------------
# Test 1: 写一条,读一条,字段对齐
# ---------------------------------------------------------------------------


def test_should_read_single_record_when_one_appended(
    run_id: str,
    run_dir_with_file: Path,
) -> None:
    """append 一条 metric,read_metrics 能读出且字段匹配。"""
    append_metric(run_id, "training", "epoch", {"loss": 0.5, "epoch": 1})
    records = list(read_metrics(run_id))
    assert len(records) == 1
    rec = records[0]
    assert rec.phase == "training"
    assert rec.kind == "epoch"
    assert rec.data == {"loss": 0.5, "epoch": 1}
    assert isinstance(rec.ts, datetime)
    assert rec.ts.tzinfo is not None  # UTC-aware


# ---------------------------------------------------------------------------
# Test 2: 写 100 条,count_metrics 返回 100
# ---------------------------------------------------------------------------


def test_should_count_100_when_100_appended(
    run_id: str,
    run_dir_with_file: Path,
) -> None:
    """写 100 条后 count_metrics 正确返回 100。"""
    for i in range(100):
        append_metric(run_id, "training", "step", {"step": i, "loss": 0.1 * i})
    assert count_metrics(run_id) == 100


# ---------------------------------------------------------------------------
# Test 3: 按 phase 过滤
# ---------------------------------------------------------------------------


def test_should_filter_by_phase_when_mixed_phases(
    run_id: str,
    run_dir_with_file: Path,
) -> None:
    """read_metrics(phase='training') 只返回 training 记录。"""
    append_metric(run_id, "baseline", "eval", {"score": 0.3})
    append_metric(run_id, "training", "epoch", {"loss": 0.5})
    append_metric(run_id, "training", "epoch", {"loss": 0.4})
    append_metric(run_id, "evaluating", "eval", {"score": 0.6})

    training_records = list(read_metrics(run_id, phase="training"))
    assert len(training_records) == 2
    assert all(r.phase == "training" for r in training_records)


# ---------------------------------------------------------------------------
# Test 4: 按 kind 过滤
# ---------------------------------------------------------------------------


def test_should_filter_by_kind_when_mixed_kinds(
    run_id: str,
    run_dir_with_file: Path,
) -> None:
    """read_metrics(kind='epoch') 只返回 epoch 记录。"""
    append_metric(run_id, "training", "step", {"step": 1})
    append_metric(run_id, "training", "epoch", {"epoch": 1, "loss": 0.5})
    append_metric(run_id, "training", "step", {"step": 2})
    append_metric(run_id, "training", "epoch", {"epoch": 2, "loss": 0.4})

    epoch_records = list(read_metrics(run_id, kind="epoch"))
    assert len(epoch_records) == 2
    assert all(r.kind == "epoch" for r in epoch_records)


# ---------------------------------------------------------------------------
# Test 5: 文件不存在 → 空 iterator,不 raise
# ---------------------------------------------------------------------------


def test_should_return_empty_iterator_when_file_not_exist(
    run_id: str,
) -> None:
    """metrics.jsonl 不存在时 read_metrics 返回空 iterator,不抛异常。"""
    records = list(read_metrics(run_id))
    assert records == []


# ---------------------------------------------------------------------------
# Test 6: run_id 目录不存在 → 自动创建
# ---------------------------------------------------------------------------


def test_should_auto_create_parent_dir_when_run_dir_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """append_metric 时若 run 目录不存在,自动创建父目录。"""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))
    new_run_id = "01HZNEW00000000000000NEW0"
    # 目录不存在,append 不应 raise
    append_metric(new_run_id, "baseline", "custom", {"note": "auto-create"})
    records = list(read_metrics(new_run_id))
    assert len(records) == 1
    assert records[0].phase == "baseline"


# ---------------------------------------------------------------------------
# Test 7: 损坏行跳过,不中断读取
# ---------------------------------------------------------------------------


def test_should_skip_corrupted_line_and_continue_reading(
    run_id: str,
    run_dir_with_file: Path,
) -> None:
    """手动写入损坏行后,read_metrics 跳过该行继续读后续记录。"""
    # 先写合法记录
    append_metric(run_id, "training", "epoch", {"epoch": 1})
    # 手动注入损坏行
    metrics_path = get_metrics_path(run_id)
    with open(metrics_path, "a", encoding="utf-8") as f:  # noqa: PTH123
        f.write("garbage not json\n")
    # 写第二条合法记录
    append_metric(run_id, "training", "epoch", {"epoch": 2})

    records = list(read_metrics(run_id))
    # 损坏行被跳过,合法行正常读出
    assert len(records) == 2
    assert records[0].data == {"epoch": 1}
    assert records[1].data == {"epoch": 2}


# ---------------------------------------------------------------------------
# Test 8: data 含不可序列化对象 → TypeError
# ---------------------------------------------------------------------------


def test_should_raise_type_error_when_data_contains_set(
    run_id: str,
    run_dir_with_file: Path,
) -> None:
    """data 含 set(不可 JSON 序列化)时抛 TypeError。

    注意:json.dumps(default=str) 会把 set 转为字符串表示,
    但根据 docstring 约定:data 含真正不可序列化对象(set)时应 raise TypeError。
    本实现不使用 default=str 对 set 降级,调用方必须传可序列化 data。
    """
    with pytest.raises(TypeError):
        append_metric(run_id, "training", "custom", {"bad": {1, 2, 3}})  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Test 9: last_metric 空文件返回 None
# ---------------------------------------------------------------------------


def test_should_return_none_when_metrics_file_empty(
    run_id: str,
    run_dir_with_file: Path,
) -> None:
    """metrics.jsonl 存在但为空时,last_metric 返回 None。"""
    # 文件已创建(run_dir_with_file fixture 创建了目录),但未写内容
    result = last_metric(run_id)
    assert result is None


# ---------------------------------------------------------------------------
# Test 10: last_metric 按 phase 过滤返回最后匹配
# ---------------------------------------------------------------------------


def test_should_return_last_matched_when_last_metric_filtered(
    run_id: str,
    run_dir_with_file: Path,
) -> None:
    """last_metric(phase='training') 返回最后一条 training 记录。"""
    append_metric(run_id, "training", "epoch", {"epoch": 1})
    append_metric(run_id, "training", "epoch", {"epoch": 2})
    append_metric(run_id, "evaluating", "eval", {"score": 0.7})

    result = last_metric(run_id, phase="training")
    assert result is not None
    assert result.phase == "training"
    assert result.data == {"epoch": 2}


# ---------------------------------------------------------------------------
# Test 11: 并发 append 测试
# ---------------------------------------------------------------------------


def test_should_preserve_all_records_when_concurrent_appends(
    run_id: str,
    run_dir_with_file: Path,
) -> None:
    """10 个线程各写 10 条,最终 100 条且每行可解析(验证 append atomicity)。

    标记 slow:并发 threading 场景,可能稍慢。
    """
    n_threads = 10
    n_per_thread = 10
    errors: list[Exception] = []

    def worker(thread_idx: int) -> None:
        try:
            for i in range(n_per_thread):
                append_metric(
                    run_id,
                    "training",
                    "step",
                    {"thread": thread_idx, "step": i},
                )
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors, f"并发写入发生异常: {errors}"

    # 验证总条数
    total = count_metrics(run_id)
    assert total == n_threads * n_per_thread, f"期望 {n_threads * n_per_thread},实际 {total}"

    # 验证每行可解析(无行撕裂)
    metrics_path = get_metrics_path(run_id)
    with open(metrics_path, encoding="utf-8") as f:  # noqa: PTH123
        for line_no, raw_line in enumerate(f, 1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
                assert "ts" in obj
                assert "phase" in obj
                assert "kind" in obj
                assert "data" in obj
            except json.JSONDecodeError as e:
                pytest.fail(f"第 {line_no} 行 JSON 解析失败: {e}\n内容: {stripped!r}")


# ---------------------------------------------------------------------------
# Test 12: datetime round-trip
# ---------------------------------------------------------------------------


def test_should_preserve_datetime_when_ts_roundtrip(
    run_id: str,
    run_dir_with_file: Path,
) -> None:
    """append 带自定义 ts= 后,read 出的 MetricRecord.ts 等于原 datetime(UTC 对齐)。"""
    original_ts = datetime(2026, 4, 24, 10, 30, 45, 123456, tzinfo=UTC)
    append_metric(run_id, "reporting", "custom", {"note": "ts test"}, ts=original_ts)

    records = list(read_metrics(run_id))
    assert len(records) == 1
    rec = records[0]
    # ts 应等于写入时的 UTC datetime
    assert rec.ts == original_ts
    assert rec.ts.tzinfo == UTC


# ---------------------------------------------------------------------------
# Test 13: data 超大(>8KB) → log warning 但仍写入
# ---------------------------------------------------------------------------


def test_should_warn_and_still_write_when_data_too_large(
    run_id: str,
    run_dir_with_file: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """data 超过 PIPE_BUF(约 4-8KB)时记录 warning 但仍写入。"""
    import logging

    # 构造超过 8KB 的 data
    large_data: dict[str, Any] = {"payload": "x" * 8192}

    with caplog.at_level(logging.WARNING, logger="pars.ledger.metrics"):
        append_metric(run_id, "training", "custom", large_data)

    # warning 应出现
    assert any("PIPE_BUF" in msg or "large" in msg.lower() or "超" in msg for msg in caplog.messages), (
        f"期望有超大 data 的 warning,实际 log: {caplog.messages}"
    )

    # 数据仍写入
    records = list(read_metrics(run_id))
    assert len(records) == 1
    assert records[0].data["payload"] == "x" * 8192


# ---------------------------------------------------------------------------
# Test 14(bonus): get_metrics_path 返回正确路径
# ---------------------------------------------------------------------------


def test_should_return_correct_path_when_get_metrics_path(
    run_id: str,
    tmp_path: Path,
) -> None:
    """get_metrics_path 返回 run_dir / 'metrics.jsonl'。"""
    p = get_metrics_path(run_id)
    assert p.name == "metrics.jsonl"
    assert run_id in str(p)


# ---------------------------------------------------------------------------
# Test 15(bonus): count_metrics 按 phase 过滤
# ---------------------------------------------------------------------------


def test_should_count_filtered_when_count_metrics_with_phase(
    run_id: str,
    run_dir_with_file: Path,
) -> None:
    """count_metrics(phase='training') 只计 training 条数。"""
    append_metric(run_id, "training", "epoch", {"epoch": 1})
    append_metric(run_id, "training", "epoch", {"epoch": 2})
    append_metric(run_id, "evaluating", "eval", {"score": 0.8})

    assert count_metrics(run_id, phase="training") == 2
    assert count_metrics(run_id) == 3
