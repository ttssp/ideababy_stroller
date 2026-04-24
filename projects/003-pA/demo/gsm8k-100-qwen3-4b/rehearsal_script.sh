#!/usr/bin/env bash
# =============================================================================
# rehearsal_script.sh — RecallKit v0.1 · 7-Day Operator Rehearsal
#
# 实跑演练，非 CI fixture。
#
# 用途：
#   - 验证 O1（操作员能在 7 天内完成 baseline + 2 LoRA 变体 + compare）
#   - 验证 rehearsal_script.sh bash -n 语法通过（T027 Verification）
#   - 供操作员按天执行，不要求一次性跑完
#
# 使用方式：
#   # Day 1: 跑 baseline + LoRA r=16
#   bash demo/gsm8k-100-qwen3-4b/rehearsal_script.sh day1
#
#   # Day 2: 跑 LoRA r=32
#   bash demo/gsm8k-100-qwen3-4b/rehearsal_script.sh day2
#
#   # Day 5: 三方对比
#   bash demo/gsm8k-100-qwen3-4b/rehearsal_script.sh compare
#
#   # 全流程一次性跑（适合 H200 等快速 GPU，不适合 4090）
#   bash demo/gsm8k-100-qwen3-4b/rehearsal_script.sh all
#
# 前置条件：
#   1. uv sync --frozen 已跑通
#   2. ANTHROPIC_API_KEY 已设置（export ANTHROPIC_API_KEY=sk-ant-...）
#   3. GPU 驱动 + CUDA 12.1+ 就绪
#   4. MacFUSE + bindfs 只读 mount 已配置（C21）
#
# 注意事项：
#   - 本脚本仅生成 pars sft start / retry / compare 命令，不直接调用训练逻辑
#   - 每条命令执行前打印进度信息
#   - 若某天失败，可单独重跑对应天的命令（pars sft start 有幂等检查）
#
# 关联文件：
#   - scenario.md：剧本说明（研究问题 / day-by-day 计划 / 故障排查）
#   - expected_metrics.md：期望指标与判断标准
#   - run_config.yaml：完整 RunConfig 参数文档化记录
#
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# 常量定义
# ---------------------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Run 名称（对应 scenario.md Day 1-5 命名）
RUN_DAY1="day1-r16"
RUN_DAY2="day2-r32"
RUN_DAY4="day4-r16-lowlr"

# 模型和数据集（对应 run_config.yaml）
BASE_MODEL="Qwen/Qwen2.5-3B-Instruct"
DATASET="openai/gsm8k"
DATASET_SPLIT="main[:100]"
EVAL_TASKS="gsm8k"

# 预算上限
USD_CAP="10.0"
WALL_CLOCK_CAP="8.0"
GPU_HOURS_CAP="8.0"

# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

log_step() {
    local msg="$1"
    echo ""
    echo "========================================================"
    echo "[REHEARSAL] ${msg}"
    echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "========================================================"
}

check_prereqs() {
    log_step "检查前置条件"

    # 确认 pars CLI 可用
    if ! command -v pars >/dev/null 2>&1; then
        echo "[ERROR] pars CLI 未找到。请先运行: uv sync --frozen && uv tool install ."
        exit 1
    fi

    # 确认 ANTHROPIC_API_KEY 已设置
    if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
        echo "[ERROR] ANTHROPIC_API_KEY 未设置。请先: export ANTHROPIC_API_KEY=sk-ant-..."
        exit 1
    fi

    echo "[OK] 前置条件检查通过"
    pars --version
}

# ---------------------------------------------------------------------------
# Day 1: Baseline + LoRA r=16
# ---------------------------------------------------------------------------

run_day1() {
    log_step "Day 1: 启动 baseline + LoRA r=16 run (name=${RUN_DAY1})"

    echo "[INFO] 研究假设: LoRA r=16 更新 QKV projection 能否在 gsm8k-100 上提升 >= 5% accuracy"
    echo "[INFO] 预计耗时: 25-45min (H200) / 60-90min (4090)"
    echo "[INFO] 执行命令:"

    echo "  pars sft start \\"
    echo "    --question \"LoRA r=16 更新 QKV projection 能否在 gsm8k-100 上提升 >= 5% accuracy?\" \\"
    echo "    --base ${BASE_MODEL} \\"
    echo "    --dataset ${DATASET} \\"
    echo "    --dataset-split \"${DATASET_SPLIT}\" \\"
    echo "    --lora-rank 16 \\"
    echo "    --lora-alpha 32 \\"
    echo "    --lr 2e-4 \\"
    echo "    --epochs 3 \\"
    echo "    --batch-size 2 \\"
    echo "    --max-seq-len 2048 \\"
    echo "    --eval-tasks ${EVAL_TASKS} \\"
    echo "    --usd-cap ${USD_CAP} \\"
    echo "    --wall-clock-hours-cap ${WALL_CLOCK_CAP} \\"
    echo "    --gpu-hours-cap ${GPU_HOURS_CAP} \\"
    echo "    --name ${RUN_DAY1}"

    pars sft start \
        --question "LoRA r=16 更新 QKV projection 能否在 gsm8k-100 上提升 >= 5% accuracy?" \
        --base "${BASE_MODEL}" \
        --dataset "${DATASET}" \
        --dataset-split "${DATASET_SPLIT}" \
        --lora-rank 16 \
        --lora-alpha 32 \
        --lr 2e-4 \
        --epochs 3 \
        --batch-size 2 \
        --max-seq-len 2048 \
        --eval-tasks "${EVAL_TASKS}" \
        --usd-cap "${USD_CAP}" \
        --wall-clock-hours-cap "${WALL_CLOCK_CAP}" \
        --gpu-hours-cap "${GPU_HOURS_CAP}" \
        --name "${RUN_DAY1}"

    log_step "Day 1 完成"
    echo "[NEXT] 请查看 runs/${RUN_DAY1}/report.md 确认 baseline 和 LoRA acc"
    echo "[NEXT] 若结果符合预期，继续 Day 2: bash $0 day2"
}

# ---------------------------------------------------------------------------
# Day 2: LoRA r=32（基于 day1 结果的 retry）
# ---------------------------------------------------------------------------

run_day2() {
    log_step "Day 2: retry r=32（继承 ${RUN_DAY1} 配置，只调 rank + alpha）"

    echo "[INFO] 研究假设: r=32 相比 r=16 能在 gsm8k-100 上进一步提升 accuracy"
    echo "[INFO] 父 run: ${RUN_DAY1}"
    echo "[INFO] 预计耗时: 30-50min (H200) / 70-100min (4090)"

    echo "[INFO] 执行命令:"
    echo "  pars sft retry \\"
    echo "    --from ${RUN_DAY1} \\"
    echo "    --hypothesis \"r=32 相比 r=16 能在 gsm8k-100 上进一步提升 accuracy\" \\"
    echo "    --lora-rank 32 \\"
    echo "    --lora-alpha 64 \\"
    echo "    --name ${RUN_DAY2}"

    pars sft retry \
        --from "${RUN_DAY1}" \
        --hypothesis "r=32 相比 r=16 能在 gsm8k-100 上进一步提升 accuracy，因为更高的 rank 给 QKV projection 更多可学习参数" \
        --lora-rank 32 \
        --lora-alpha 64 \
        --name "${RUN_DAY2}"

    log_step "Day 2 完成"
    echo "[NEXT] 请查看 runs/${RUN_DAY2}/report.md"
    echo "[NEXT] 若想探索低 lr 变体，继续: bash $0 day4"
    echo "[NEXT] 若直接对比，继续: bash $0 compare"
}

# ---------------------------------------------------------------------------
# Day 4: LoRA r=16 + lr=5e-5（低学习率变体）
# ---------------------------------------------------------------------------

run_day4() {
    log_step "Day 4: retry 低 lr 变体（继承 ${RUN_DAY1} 配置，只调 lr）"

    echo "[INFO] 研究假设: lr=5e-5 能减少训练震荡，稳定提升 gsm8k-100 accuracy"
    echo "[INFO] 父 run: ${RUN_DAY1}"
    echo "[INFO] 预计耗时: 25-35min (H200) / 60-90min (4090)"

    echo "[INFO] 执行命令:"
    echo "  pars sft retry \\"
    echo "    --from ${RUN_DAY1} \\"
    echo "    --hypothesis \"lr=5e-5 能减少震荡，稳定提升 accuracy\" \\"
    echo "    --lr 5e-5 \\"
    echo "    --name ${RUN_DAY4}"

    pars sft retry \
        --from "${RUN_DAY1}" \
        --hypothesis "lr=5e-5（原 lr=2e-4 的 1/4）能减少震荡，稳定提升 gsm8k-100 accuracy" \
        --lr 5e-5 \
        --name "${RUN_DAY4}"

    log_step "Day 4 完成"
    echo "[NEXT] 继续三方对比: bash $0 compare"
}

# ---------------------------------------------------------------------------
# Day 5-6: Compare 所有变体
# ---------------------------------------------------------------------------

run_compare() {
    log_step "Day 5-6: 对比所有变体，产出决策"

    echo "[INFO] 对比 ${RUN_DAY1} vs ${RUN_DAY2}"
    pars sft compare "${RUN_DAY1}" "${RUN_DAY2}"

    echo ""
    echo "[INFO] 对比 ${RUN_DAY1} vs ${RUN_DAY4}"
    pars sft compare "${RUN_DAY1}" "${RUN_DAY4}"

    echo ""
    echo "[INFO] 对比 ${RUN_DAY2} vs ${RUN_DAY4}"
    pars sft compare "${RUN_DAY2}" "${RUN_DAY4}"

    log_step "Compare 完成"
    echo "[NEXT] 查看各对比表，按 expected_metrics.md §4 的决策框架做结论"
    echo "[NEXT] 在 runs/<最优-run>/report.md 的结论节填写决策"
    echo "[NEXT] 完成后在 specs/003-pA/STATUS.md O1 行签字"
}

# ---------------------------------------------------------------------------
# 全流程（适合 H200 等快速 GPU）
# ---------------------------------------------------------------------------

run_all() {
    log_step "全流程演练（Day 1 + 2 + 4 + compare，建议仅在 H200 等快速 GPU 上使用）"
    echo "[WARN] 全流程估计 2-4h，确认 GPU 显存 >= 24GB 再继续"
    echo ""

    run_day1
    echo "[PAUSE] Day 1 完成，等待 10 秒后继续 Day 2..."
    sleep 10

    run_day2
    echo "[PAUSE] Day 2 完成，等待 10 秒后继续 Day 4..."
    sleep 10

    run_day4
    echo "[PAUSE] Day 4 完成，等待 5 秒后进行 compare..."
    sleep 5

    run_compare

    log_step "全流程演练完成"
    echo "[SUCCESS] 请查看以下文件确认结果："
    echo "  runs/${RUN_DAY1}/report.md"
    echo "  runs/${RUN_DAY2}/report.md"
    echo "  runs/${RUN_DAY4}/report.md"
}

# ---------------------------------------------------------------------------
# 入口点：按参数分发
# ---------------------------------------------------------------------------

COMMAND="${1:-help}"

case "${COMMAND}" in
    day1)
        check_prereqs
        run_day1
        ;;
    day2)
        check_prereqs
        run_day2
        ;;
    day4)
        check_prereqs
        run_day4
        ;;
    compare)
        check_prereqs
        run_compare
        ;;
    all)
        check_prereqs
        run_all
        ;;
    help|--help|-h)
        echo "用法: $0 [day1|day2|day4|compare|all]"
        echo ""
        echo "  day1     Day 1: baseline + LoRA r=16"
        echo "  day2     Day 2: LoRA r=32 (retry from day1)"
        echo "  day4     Day 4: LoRA r=16 + lr=5e-5 (retry from day1)"
        echo "  compare  Day 5-6: 三方对比 + 决策"
        echo "  all      全流程（Day 1+2+4+compare，适合 H200）"
        echo ""
        echo "详见 demo/gsm8k-100-qwen3-4b/scenario.md"
        ;;
    *)
        echo "[ERROR] 未知命令: ${COMMAND}"
        echo "运行 $0 help 查看用法"
        exit 1
        ;;
esac
