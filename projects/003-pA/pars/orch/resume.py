"""
pars.orch.resume — resume 逻辑层（T019 · O3 · C13 · C22）。

结论：提供 can_resume / find_latest_checkpoint / prepare_resume / execute_resume
      四个公开函数，供 CLI (pars/cli/resume.py) 调用。
      resume 前必须校验机器指纹（C22），阻断跨机器 resume。

### 检查链（can_resume）

1. state.json 存在且 phase 不是终态（completed / failed）
2. checkpoint 目录非空（有可用存档）
3. stuck_lock 不存在（T017 §8.5；存在 → 提示 pars unlock）
4. 机器指纹比对（C22）：
   - 指纹文件缺失 → warning + 放行（向后兼容旧 run）
   - hard_mismatches 非空 → 拒绝（跨机器）
   - warn_mismatches 非空 → 仅 warning，放行

### 终态定义

completed / failed 均为不可 resume 的终态，见 architecture.md §4 RunPhase。
"""

from __future__ import annotations

from pathlib import Path

from pars.ledger.state import RunPhase, read_state
from pars.logging import get_logger
from pars.orch.machine_fingerprint import (
    collect_fingerprint,
    diff_fingerprint,
    read_fingerprint,
)
from pars.paths import ckpt_dir
from pars.stuck.stuck_lock import has_stuck_lock

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# 终态集合（这两个 phase 不可 resume）
# ---------------------------------------------------------------------------

_TERMINAL_PHASES: frozenset[RunPhase] = frozenset({RunPhase.COMPLETED, RunPhase.FAILED})


# ---------------------------------------------------------------------------
# 公开 API
# ---------------------------------------------------------------------------

def find_latest_checkpoint(run_id: str) -> Path | None:
    """查找 run 的 checkpoint 目录，若为空或不存在则返回 None。

    checkpoint 写在 checkpoints/<run_id>/ （worktree 外），见 architecture §4.2。

    返回：
        Path  : checkpoint 目录（非空，可用）
        None  : 目录不存在或为空（无可用存档）
    """
    ckpt = ckpt_dir(run_id)
    if not ckpt.exists():
        logger.debug(
            "find_latest_checkpoint: 目录不存在",
            extra={"run_id": run_id, "path": str(ckpt)},
        )
        return None

    # 检查目录是否非空（至少有一个文件或子目录）
    # iterdir() 返回的是 generator，next() + StopIteration 判空
    try:
        next(ckpt.iterdir())
    except StopIteration:
        logger.debug(
            "find_latest_checkpoint: 目录为空",
            extra={"run_id": run_id, "path": str(ckpt)},
        )
        return None

    logger.debug(
        "find_latest_checkpoint: checkpoint 可用",
        extra={"run_id": run_id, "path": str(ckpt)},
    )
    return ckpt


def can_resume(run_id: str) -> tuple[bool, str]:
    """检查指定 run 是否可以 resume。

    检查顺序（失败即返回，不继续后续检查）：
    1. state.json 存在且 phase 不是终态
    2. checkpoint 目录非空
    3. stuck_lock 不存在
    4. 机器指纹比对（C22 hard_reject 规则）

    参数：
        run_id : 要检查的 run 标识符

    返回：
        (True, "")    : 可以 resume（reason 为空串或空白）
        (False, msg)  : 不可以 resume，msg 解释原因
    """
    # --- 检查 1：state.json 存在 + 非终态 ---
    try:
        state = read_state(run_id)
    except FileNotFoundError:
        return False, f"run {run_id!r} 不存在（state.json 未找到）"
    except Exception as exc:
        return False, f"读取 state.json 失败: {exc}"

    if state.phase in _TERMINAL_PHASES:
        phase_str = state.phase.value
        return False, (
            f"run {run_id!r} 已处于终态 {phase_str!r}，无法 resume。"
            f"（completed run 不可 resume；如需重跑请用 pars sft retry）"
        )

    # --- 检查 2：checkpoint 目录非空 ---
    ckpt_path = find_latest_checkpoint(run_id)
    if ckpt_path is None:
        return False, (
            f"run {run_id!r} 无可用 checkpoint（checkpoints/{run_id}/ 不存在或为空）。"
            f"请确认训练至少完成了一个 epoch。"
        )

    # --- 检查 3：stuck_lock 不存在（T017 §8.5）---
    if has_stuck_lock(run_id=run_id):
        return False, (
            f"run {run_id!r} 存在 stuck_lock，需人工确认后解锁。"
            f"请先运行: pars unlock --run-id {run_id!r}\n"
            f"（needs_human_review, run: pars unlock {run_id} first）"
        )

    # --- 检查 4：机器指纹比对（C22）---
    saved_fp = read_fingerprint(run_id)

    if saved_fp is None:
        # 指纹文件缺失 → 向后兼容：warning + 放行
        logger.warning(
            "can_resume: machine_fingerprint.json 缺失（旧 run），跳过指纹校验，假设同机",
            extra={"run_id": run_id},
        )
        return True, ""

    current_fp = collect_fingerprint()
    hard_mismatches, warn_mismatches = diff_fingerprint(saved_fp, current_fp)

    if warn_mismatches:
        logger.warning(
            "can_resume: 指纹 warning 字段不一致（允许继续）",
            extra={
                "run_id": run_id,
                "warn_mismatches": warn_mismatches,
                "saved_python": saved_fp.get("python_version"),
                "current_python": current_fp.get("python_version"),
                "saved_os_release": saved_fp.get("os_release"),
                "current_os_release": current_fp.get("os_release"),
            },
        )

    if hard_mismatches:
        # 构造具体说明：列出哪些字段 mismatch + 实际值
        details = []
        for field in hard_mismatches:
            saved_val = saved_fp.get(field, "<derived>")
            current_val = current_fp.get(field, "<derived>")
            details.append(f"{field}: saved={saved_val!r}, current={current_val!r}")
        detail_str = "; ".join(details)

        msg = (
            f"cross-machine resume not supported "
            f"(hard mismatch on: {hard_mismatches}). "
            f"Details: {detail_str}. "
            f"See docs/h200-rsync-playbook.md for cross-machine migration path."
        )
        logger.error(
            "can_resume: 指纹 hard mismatch，拒绝 resume",
            extra={"run_id": run_id, "hard_mismatches": hard_mismatches},
        )
        return False, msg

    return True, ""


def prepare_resume(run_id: str) -> dict:
    """读取 run 的 state + config，返回 resume 计划摘要（供 CLI 打印确认）。

    注意：此函数假设 can_resume() 已通过检查。
    不执行任何副作用，只构造信息字典。

    返回：
        dict with keys:
        - run_id           : str
        - current_phase    : str
        - checkpoint_path  : str | None
        - last_epoch       : int | None
        - usd_spent        : float
        - wall_clock_s     : float
    """
    state = read_state(run_id)
    ckpt = find_latest_checkpoint(run_id)

    return {
        "run_id": run_id,
        "current_phase": state.phase.value,
        "checkpoint_path": str(ckpt) if ckpt else state.checkpoint_path,
        "last_epoch_completed": state.last_epoch_completed,
        "usd_spent": state.usd_spent,
        "wall_clock_elapsed_s": state.wall_clock_elapsed_s,
        "gpu_hours_used": state.gpu_hours_used,
    }


def execute_resume(run_id: str) -> None:
    """执行 resume：重建 worktree，注入 env，启动 worker（续跑）。

    此函数是 pars sft resume 的核心执行路径。
    依赖 T023（主编排）提供的 worktree + worker 启动逻辑。

    实现说明（T023 联动，当前版本仅打印 TODO）：
    - 重建 worktree（T013 API: rebuild_worktree）
    - 注入 RECALLKIT_RESUME=1 + RECALLKIT_CKPT_DIR=checkpoints/<run_id>
    - 启动 worker（T013 launch_worker）
    - 更新 state.phase = lora_train（若已是 eval 则跳过）

    TODO: T023 实现完整 execute_resume 逻辑。当前版本验证前置条件后报告 not-impl。
    """
    plan = prepare_resume(run_id)
    logger.info(
        "execute_resume: resume 计划已就绪",
        extra={
            "run_id": run_id,
            "phase": plan["current_phase"],
            "checkpoint_path": plan["checkpoint_path"],
        },
    )
    # T023 将在此处调用 rebuild_worktree + launch_worker
    # 当前 T019 deliverable 仅实现 can_resume / prepare_resume / find_latest_checkpoint
    # execute_resume 的 worktree + worker 部分由 T023 填充
    raise NotImplementedError(
        f"execute_resume: T023 will implement worktree rebuild + worker launch for run {run_id!r}. "
        f"plan={plan}"
    )
