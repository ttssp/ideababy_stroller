"""
manual_press_test.py — T009
结论: O5 release-time 手动压测(R3 守 PRD §S1 原口径,度量全程 wall-clock)
细节:
  - human 连续 5 次手工录入,程序记录每次全程 wall-clock + 阶段分解
  - 起点 = GET /decisions/new 200 OK
  - 终点 = POST /decisions/{draft_id}/commit 200 OK
  - 全程 < 30s 才写 release_log.jsonl(任何一次 ≥ 30s 标 fail)
  - architecture.md §10 schema(R3 修订:含 total_durations 字段)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

_LOG_PATH = Path("release_log.jsonl")
_FULL_FLOW_THRESHOLD_MS = 30_000  # PRD §S1 / §6 O5 硬门槛


def _git_sha() -> str:
    """获取当前 commit sha(短)。失败返回 'unknown'。"""
    try:
        cmd = ["git", "rev-parse", "--short", "HEAD"]
        result = subprocess.run(  # noqa: S603
            cmd,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        return result.stdout.strip() or "unknown"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return "unknown"


def _press(idx: int, total: int) -> tuple[float, float, float]:
    """单次压测:返回 (total_ms, draft_ms, commit_ms) 全程毫秒。

    结论: 三计时(start / draft 结束 / commit 结束),主度量 = total = t2 - t0。
    细节: 起点严格 = GET /decisions/new 200 OK(R3 守 PRD 原口径)。
    """
    print(f"\n=== 第 {idx}/{total} 次压测 ===")
    input("打开浏览器到 http://127.0.0.1:8000/decisions/new,准备好后按 Enter 开始计时:")
    t0 = time.perf_counter()  # R3 起点

    input("draft 提交后等到 preview 出现,立刻按 Enter 标记 draft 阶段结束:")
    t1 = time.perf_counter()

    input("commit 提交完成跳到 success 页后按 Enter 结束全程计时:")
    t2 = time.perf_counter()  # R3 终点

    total_ms = (t2 - t0) * 1000
    draft_ms = (t1 - t0) * 1000
    commit_ms = (t2 - t1) * 1000
    print(
        f"  全程 {total_ms:.0f}ms (draft {draft_ms:.0f}ms + commit {commit_ms:.0f}ms)"
    )
    if total_ms >= _FULL_FLOW_THRESHOLD_MS:
        print(f"  ⚠️ 超过 {_FULL_FLOW_THRESHOLD_MS}ms 硬门槛")
    return total_ms, draft_ms, commit_ms


def main() -> int:
    parser = argparse.ArgumentParser(description="O5 手动压测脚本(R3 守 PRD 原口径)")
    parser.add_argument("--presses", type=int, default=5, help="压测次数")
    parser.add_argument("--log-path", type=Path, default=_LOG_PATH, help="结果写入路径")
    args = parser.parse_args()

    print("=" * 60)
    print("O5 手动压测(R3 守 PRD §S1 原口径)")
    print(f"  阈值: 单次全程 wall-clock < {_FULL_FLOW_THRESHOLD_MS}ms")
    print(f"  循环: {args.presses} 次")
    print(f"  结果: {args.log_path}")
    print("=" * 60)

    total_durations: list[float] = []
    draft_latencies: list[float] = []
    commit_latencies: list[float] = []
    for i in range(1, args.presses + 1):
        total_ms, draft_ms, commit_ms = _press(i, args.presses)
        total_durations.append(total_ms)
        draft_latencies.append(draft_ms)
        commit_latencies.append(commit_ms)

    passed = all(d < _FULL_FLOW_THRESHOLD_MS for d in total_durations)
    avg_ms = sum(total_durations) / len(total_durations)

    record = {
        "timestamp": datetime.now(tz=UTC).isoformat(),
        "git_sha": _git_sha(),
        "presses": args.presses,
        "total_durations_ms": total_durations,
        "draft_latencies_ms": draft_latencies,
        "commit_latencies_ms": commit_latencies,
        "avg_total_ms": avg_ms,
        "threshold_ms": _FULL_FLOW_THRESHOLD_MS,
        "pass": passed,
    }
    with args.log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print("\n" + "=" * 60)
    print(f"结果: {'✅ PASS' if passed else '❌ FAIL'}")
    print(f"  平均全程 {avg_ms:.0f}ms, 最大 {max(total_durations):.0f}ms")
    print(f"  写入 {args.log_path}")
    if not passed:
        print("  PRD R1 硬门槛未达 — release block(OP-1 触发降级 B-lite 候选)")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
