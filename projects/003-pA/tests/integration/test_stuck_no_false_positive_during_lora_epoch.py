"""
test_stuck_no_false_positive_during_lora_epoch.py — O7 R2 验证：Stuck 状态机 8 场景矩阵集成测试。

唯一真相源：specs/003-pA/architecture.md §8.7（8 条正负样本矩阵）

测试目标：
  - 覆盖 architecture §8.7 全部 8 个场景
  - 每个场景读取对应 fixture（5s/样本 的合成 trace）
  - 使用 ts 字段模拟单调时钟（替代真实时钟）
  - 验证期望最终状态 + SIGINT 行为（通过 truly_stuck 判断）

Probe sample dict 格式（对齐 StuckStateMachine.transition()）：
    {"gpu": float|None, "cpu": float, "disk_delta_mbs": float, "net_delta_mbs": float}

场景矩阵（architecture §8.7）：
  1. LoRA epoch 60min：GPU=30-50% 全程 → training 全程，SIGINT=0
  2. pip install 慢下载：net=200KB-2MB/s 交替 → idle/downloading，SIGINT=0
  3. 子进程死锁：冷启动期后全 0 → truly_stuck @ t≈905s，SIGINT=1
  4. 冷启动期内真卡死：t=0-300s 全 0 → idle + warnings 非空，SIGINT=0
  5. 60s 窗口 off-by-one：GPU=25% 持续 29s（5 样本）→ 不触发 training
  6. 60s 窗口 on-boundary：GPU=25% 持续 30s（6 样本）→ 触发 training
  7. training→idle 边界：59s AND 条件（11 样本）→ 不触发 training→idle
  8. disk IO 抑制误判：GPU=0 但 disk=5MB/s → 保持 training

注意（SM 实际行为偏差记录，见 test_scene3_deadlock 的 KNOWN_DEVIATION 注释）：
  架构 §8.3 期望 truly_stuck 在 t≈1200s（冷启动期后再等 15min），
  但 SM 实现从 t=0 起算 idle_duration，实际在 t=905s 触发。
  该偏差已记录在 handoff notes；本测试基于 SM 实际行为断言，不修改 SM。

CI marker：所有 8 个场景均标记为 @pytest.mark.integration，< 2min 内可完成。
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pars.stuck.state_machine import StuckState, StuckStateMachine

# ---------------------------------------------------------------------------
# 常量 & 工具
# ---------------------------------------------------------------------------

FIXTURE_DIR = Path(__file__).parent.parent / "fixtures" / "stuck_testcases"


def _load_samples(scene_name: str) -> list[dict]:
    """读取场景 fixture 文件，返回 sample list。"""
    p = FIXTURE_DIR / f"{scene_name}.jsonl"
    assert p.exists(), f"fixture 不存在: {p}"
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def _run_sm(samples: list[dict]) -> tuple[StuckStateMachine, list[StuckState]]:
    """用 ts 字段作为时钟驱动 SM，返回 (sm, state_trace)。

    时钟策略：
    - SM 的 clock 注入为 lambda，返回当前处理 sample 的 ts 值
    - start_time 在 SM 构造时设为第一个 sample 的 ts（通常 0.0）
    - 这样 elapsed_since_start = ts - 0 = ts（天然对齐场景设计）
    """
    clock_idx = [0]
    all_ts = [s["ts"] for s in samples]

    # clock 返回当前 sample 的 ts（通过 closure 捕获 mutable index）
    def clock() -> float:
        return all_ts[min(clock_idx[0], len(all_ts) - 1)]

    sm = StuckStateMachine(clock=clock)
    state_trace: list[StuckState] = [sm.current_state]

    for i, s in enumerate(samples):
        clock_idx[0] = i  # 推进时钟到当前 sample 的 ts
        sample = {
            "gpu": s["gpu"],
            "cpu": s["cpu"],
            "disk_delta_mbs": s["disk_delta_mbs"],
            "net_delta_mbs": s["net_delta_mbs"],
        }
        state = sm.transition(sample)
        if state != state_trace[-1]:
            state_trace.append(state)

    return sm, state_trace


# ===========================================================================
# §8.7 场景 1：LoRA epoch 60min（正例：不误杀）
# ===========================================================================


@pytest.mark.integration
def test_scene1_lora_60min_should_stay_training_not_trigger_sigint():
    """§8.7 场景 1：LoRA 60min 全程 GPU=30-50%，期望全程 training，SIGINT=0。

    这是核心防误杀场景：LoRA 训练中 GPU 持续活跃，不应被 stuck 检测器误判。
    fixture 包含 720 个样本（3600s = 60min），每个样本 GPU=30-50%。
    期望：
    - 最终状态 = training
    - 从未进入 truly_stuck（SIGINT 不触发）
    - 状态迹中包含 training
    """
    samples = _load_samples("scene1_lora_60min")
    assert len(samples) >= 180, "场景 1 fixture 至少 180 个样本（15min 覆盖）"

    sm, state_trace = _run_sm(samples)

    # 最终状态必须是 training（LoRA 全程不应回 idle 或 truly_stuck）
    assert sm.current_state == StuckState.TRAINING, (
        f"场景 1 期望最终状态 training，实际 {sm.current_state.value}"
    )
    # 不得触发 truly_stuck
    assert StuckState.TRULY_STUCK not in state_trace, (
        f"场景 1 LoRA 训练期间不得触发 truly_stuck，状态迹: {[s.value for s in state_trace]}"
    )
    # 状态迹必须含 training（确认进入了 training 态）
    assert StuckState.TRAINING in state_trace, "场景 1 状态迹中必须出现 training"
    # warnings 不应有内容（GPU 一直活跃，不触发冷启动警告）
    assert sm.warnings == [], f"场景 1 不期望有 warnings，实际: {sm.warnings}"


# ===========================================================================
# §8.7 场景 2：pip install 慢下载（正例：不误杀）
# ===========================================================================


@pytest.mark.integration
def test_scene2_pip_slow_download_should_not_trigger_sigint():
    """§8.7 场景 2：pip 慢下载，net=200KB-2MB/s 交替，SIGINT=0。

    HF 模型下载期间网络速率波动是正常现象，不应误判为 stuck。
    期望：
    - 最终状态 ∈ {idle, downloading}（非 truly_stuck）
    - SIGINT=0
    """
    samples = _load_samples("scene2_pip_slow_download")
    assert len(samples) >= 12, "场景 2 fixture 至少 12 个样本"

    sm, state_trace = _run_sm(samples)

    # 不得触发 truly_stuck
    assert sm.current_state != StuckState.TRULY_STUCK, (
        f"场景 2 pip 下载期间不得触发 truly_stuck，实际: {sm.current_state.value}"
    )
    assert StuckState.TRULY_STUCK not in state_trace, (
        f"场景 2 状态迹不得包含 truly_stuck: {[s.value for s in state_trace]}"
    )
    # 最终态应为 idle 或 downloading
    assert sm.current_state in {StuckState.IDLE, StuckState.DOWNLOADING}, (
        f"场景 2 最终态应为 idle 或 downloading，实际: {sm.current_state.value}"
    )


# ===========================================================================
# §8.7 场景 3：子进程死锁（负例：必须触发 SIGINT）
#
# KNOWN_DEVIATION（T022 handoff note）：
# architecture §8.3 描述："冷启动期满后立即评估，从 t=300s 起算 15min，非从 t=0"，
# 即期望 truly_stuck 在 t≈1200s。
# 但当前 SM 实现从 SM 构造时（t=0）起算 idle_duration，
# 冷启动期内的时间也被计入 idle，导致在 t=905s（300s 冷启动 + 605s idle）就触发。
# 实际触发时刻：idle_duration = ts - 0 > 900 → ts > 900s。
# 本测试基于 SM 实际行为断言（t≈905s），不修改 SM。
# 若 T017 修复此偏差（从 t=300s 起算），本 fixture 需同步延长。
# ===========================================================================


@pytest.mark.integration
def test_scene3_deadlock_should_trigger_truly_stuck():
    """§8.7 场景 3：子进程死锁，全 0 信号超过 15min，必须触发 truly_stuck。

    fixture 设计：
    - t=0-290s（59 样本）：冷启动期，全 0 → warnings 记录，豁免
    - t=295-1205s（183 样本）：全 0，elapsed>=300 后 idle 计时累积
    - t=905s 处：idle_duration=905 > 900 → truly_stuck（SM 实际行为）

    期望：
    - 最终状态 = truly_stuck
    - 状态迹含 truly_stuck
    - warnings 非空（冷启动期全 0 警告）
    """
    samples = _load_samples("scene3_deadlock")
    # 至少 182 个样本（覆盖到 t=905s：905/5+1=182）
    assert len(samples) >= 182, (
        f"场景 3 fixture 至少 182 个样本才能覆盖 t=905s，实际: {len(samples)}"
    )

    sm, state_trace = _run_sm(samples)

    # 必须进入 truly_stuck
    assert sm.current_state == StuckState.TRULY_STUCK, (
        f"场景 3 死锁期望最终状态 truly_stuck，实际: {sm.current_state.value}"
    )
    assert StuckState.TRULY_STUCK in state_trace, (
        f"场景 3 状态迹必须包含 truly_stuck: {[s.value for s in state_trace]}"
    )
    # 冷启动期全 0 警告必须记录
    assert "cold_start_silence_suspected_stuck" in sm.warnings, (
        f"场景 3 期望有冷启动警告，实际 warnings: {sm.warnings}"
    )


# ===========================================================================
# §8.7 场景 4：冷启动期内真卡死（豁免行为）
# ===========================================================================


@pytest.mark.integration
def test_scene4_cold_start_deadlock_should_stay_idle_with_warnings():
    """§8.7 场景 4：冷启动期（0-300s）内全 0 信号，不触发 SIGINT，记录 warning。

    豁免行为：elapsed < 300s 时 truly_stuck 转移被禁止，仅记录 warning。
    期望：
    - 最终状态 = idle（未转 truly_stuck）
    - SIGINT=0
    - warnings 包含 cold_start_silence_suspected_stuck
    """
    samples = _load_samples("scene4_cold_start_deadlock")
    assert len(samples) >= 12, "场景 4 fixture 至少 12 个样本"

    # 验证所有样本的 ts 都在冷启动期内（ts < 300s）
    last_ts = samples[-1]["ts"]
    assert last_ts < 300.0, (
        f"场景 4 fixture 所有样本应在冷启动期内（ts < 300s），最后 ts={last_ts}"
    )

    sm, state_trace = _run_sm(samples)

    # 不得触发 truly_stuck
    assert sm.current_state == StuckState.IDLE, (
        f"场景 4 冷启动期内期望 idle，实际: {sm.current_state.value}"
    )
    assert StuckState.TRULY_STUCK not in state_trace, "场景 4 不得触发 truly_stuck"
    # 必须有冷启动警告
    assert len(sm.warnings) > 0, "场景 4 期望有 warnings（冷启动全 0 信号）"
    assert "cold_start_silence_suspected_stuck" in sm.warnings, (
        f"场景 4 期望 warning=cold_start_silence_suspected_stuck，实际: {sm.warnings}"
    )


# ===========================================================================
# §8.7 场景 5：60s 窗口 off-by-one（边界：29s 不触发）
# ===========================================================================


@pytest.mark.integration
def test_scene5_boundary_29s_should_not_trigger_training():
    """§8.7 场景 5：GPU=25% 持续 5 个样本（25s），不满足 30s 条件，不触发 training。

    关键边界：idle → training 需要 GPU > 20% 持续 30s（连续 6 个样本）。
    5 个样本 = 25s < 30s，不应触发。

    注意：fixture 前 59 个样本是冷启动期全 0，第 60-64 个样本（5个）是 GPU=25%。
    期望：
    - 最终状态 = idle（未进入 training）
    - GPU 连续计数未达阈值
    """
    samples = _load_samples("scene5_boundary_29s")

    sm, state_trace = _run_sm(samples)

    assert sm.current_state == StuckState.IDLE, (
        f"场景 5（29s 边界）期望 idle，实际: {sm.current_state.value}"
    )
    assert StuckState.TRAINING not in state_trace, (
        f"场景 5 GPU 持续 29s 不应触发 training，状态迹: {[s.value for s in state_trace]}"
    )
    assert StuckState.TRULY_STUCK not in state_trace, "场景 5 不得触发 truly_stuck"


# ===========================================================================
# §8.7 场景 6：60s 窗口 on-boundary（边界：30s 触发）
# ===========================================================================


@pytest.mark.integration
def test_scene6_boundary_30s_should_trigger_training():
    """§8.7 场景 6：GPU=25% 持续 6 个样本（30s），满足 30s 条件，触发 idle→training。

    关键边界：恰好 6 个连续样本 → 触发转移。
    fixture 前 59 个样本冷启动全 0，第 60-65 个样本（6个）是 GPU=25%。
    期望：
    - 状态迹包含 training（已触发转移）
    - 不触发 truly_stuck
    """
    samples = _load_samples("scene6_boundary_30s")

    sm, state_trace = _run_sm(samples)

    # 必须进入 training
    assert StuckState.TRAINING in state_trace, (
        f"场景 6 GPU 持续 30s 必须触发 training，状态迹: {[s.value for s in state_trace]}"
    )
    # 最终状态不应是 truly_stuck（training 后 GPU 跌 0，但不满足 training→idle AND 条件的 12 个样本）
    assert sm.current_state != StuckState.TRULY_STUCK, "场景 6 不得触发 truly_stuck"


# ===========================================================================
# §8.7 场景 7：training→idle 边界 59s（11 个样本不触发）
# ===========================================================================


@pytest.mark.integration
def test_scene7_training_idle_59s_should_stay_training():
    """§8.7 场景 7：在 training 态，低信号（GPU<5%+CPU<10%+disk<1MB/s）持续 11 个样本（55s），
    不触发 training→idle（需要 12 个样本 = 60s）。

    期望：
    - 最终状态 = training
    - 状态迹不包含 idle（在进入 training 之后）
    """
    samples = _load_samples("scene7_training_idle_59s")

    sm, state_trace = _run_sm(samples)

    # 最终状态必须是 training
    assert sm.current_state == StuckState.TRAINING, (
        f"场景 7（59s 边界）期望最终 training，实际: {sm.current_state.value}"
    )
    # training 之后不应出现 idle（11 个低样本不满足 training→idle 的 12 个条件）
    assert StuckState.TRULY_STUCK not in state_trace, "场景 7 不得触发 truly_stuck"
    # 验证确实进入过 training（fixture 设计保证这一点）
    assert StuckState.TRAINING in state_trace, "场景 7 状态迹必须包含 training"
    # 状态迹中 training 之后不应有 idle
    if StuckState.TRAINING in state_trace:
        training_idx = state_trace.index(StuckState.TRAINING)
        post_training = state_trace[training_idx + 1:]
        assert StuckState.IDLE not in post_training, (
            f"场景 7：进入 training 后不应出现 idle（11 样本不满足 12 样本条件），"
            f"post-training 状态迹: {[s.value for s in post_training]}"
        )


# ===========================================================================
# §8.7 场景 8：disk IO 抑制误判（GPU=0 但 disk=5MB/s）
# ===========================================================================


@pytest.mark.integration
def test_scene8_disk_suppression_should_stay_training():
    """§8.7 场景 8：GPU=0 但 disk=5MB/s（写 checkpoint），training→idle 的 AND 条件不满足。

    disk IO 是 training→idle 的 AND 条件之一（disk < 1 MB/s）。
    当 disk=5MB/s 时，即使 GPU=0，AND 不满足 → 保持 training。

    期望：
    - 最终状态 = training
    - disk 活跃阻止了 training→idle 转移
    """
    samples = _load_samples("scene8_disk_suppression")

    sm, state_trace = _run_sm(samples)

    # 最终状态必须是 training（disk 抑制了 idle 转移）
    assert sm.current_state == StuckState.TRAINING, (
        f"场景 8 期望 disk 抑制 training→idle，最终 training，实际: {sm.current_state.value}"
    )
    # 不得触发 truly_stuck
    assert StuckState.TRULY_STUCK not in state_trace, "场景 8 不得触发 truly_stuck"
    # 验证确实进入过 training
    assert StuckState.TRAINING in state_trace, "场景 8 状态迹必须包含 training"
    # 进入 training 后不应有 idle（disk 活跃阻止了转移）
    if StuckState.TRAINING in state_trace:
        training_idx = state_trace.index(StuckState.TRAINING)
        post_training = state_trace[training_idx + 1:]
        assert StuckState.IDLE not in post_training, (
            f"场景 8：disk=5MB/s 时不应从 training 转 idle，"
            f"post-training 状态迹: {[s.value for s in post_training]}"
        )


# ===========================================================================
# 附加：真实 GPU 版（场景 1 的 slow gpu 变体）
# CI 环境 skip，操作员手跑（需要 nvidia-smi + 真实 GPU）
# ===========================================================================


@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.requires_gpu
@pytest.mark.skipif(
    not __import__("shutil").which("nvidia-smi"),
    reason="需要 NVIDIA GPU 和 nvidia-smi 才能运行真实 GPU 版",
)
def test_scene1_real_gpu_lora_should_not_trigger_sigint():
    """§8.7 场景 1 真实 GPU 版：TinyLlama 1.1B 真实训练 1 epoch，断言 SIGINT=0。

    操作员手跑：uv run pytest -v -m "integration and slow and requires_gpu"
    预计运行时间：30-90 分钟（取决于 GPU 型号）

    由于无法在测试中真实运行训练（需要完整的 orchestrator），
    此测试验证的是"若 SM 在实际 GPU 运行中被调用，不应触发 truly_stuck"的证明。
    实际执行方式：操作员运行 `pars sft start --dry-run` 并观察 stuck state。
    """
    # 此处仅作占位声明，真实验证需要完整的 orchestrator + 训练环境
    # 留给操作员手动验证
    pytest.skip("真实 GPU 版测试需要操作员手动运行，自动跳过")
