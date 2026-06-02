#!/usr/bin/env bash
# concurrency-preflight.sh · idea 006 forge v5 · M0-1 · 多 worktree 并发批次启动前 gate
#
# 结论先:operator 起每批多 worktree 并发构建**之前**必跑本脚本;exit 0 = 可起并发,
#   exit 1 = 检出 mirror drift / 其它并发前隐患 · 修复后重跑。当前只挂一项检查
#   (verdict-evidence 共享 lib mirror SHA 一致性),但**设计为可扩展骨架** —— 见下
#   "可扩展" 注释,未来加并发前检查只需往 CHECKS array 追加一行。
#
# 为什么需要它(per forge v5 verdict · shared-lib-drift backlog):
#   R-Q6 共享 lib SSOT 在 XenoDev · IDS bootstrap-kit 持 mirror。多 worktree 各自携带
#   不同时间点的 mirror 拷贝 → drift 风险。守护测试 test-verdict-evidence-mirror-sha.sh
#   早已存在但**孤立无人调用**(从没被挂成 gate)。本脚本把它升为"并发前强制 preflight",
#   让 worktree 携旧 mirror 在并发启动前被拦,不再静默漂移。
#
# K8 滤网(per forge v5):轻量正确即可 —— SHA dual-verify 已足够,不上签名供应链/分布式锁。
#
# Usage:
#   bash framework/xenodev-bootstrap-kit/concurrency-preflight.sh
#   # exit 0 = PREFLIGHT PASS · 可起并发批次
#   # exit 1 = PREFLIGHT FAIL · mirror drift / 隐患 · 见上方逐项输出 · 修复后重跑
#
# 退码:
#   0 = 全 PASS · 可起并发
#   1 = 任一 check FAIL · 不可起并发批次

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ──────────────────────────────────────────────────────────────
# CHECKS · 并发前检查清单(可扩展骨架)
# ──────────────────────────────────────────────────────────────
# 每条 = "标签|脚本绝对路径"。脚本必须 exit 0=PASS / 非0=FAIL,自带断言 + stderr drift 报告
# (本 preflight 只靠子脚本 exit code 判定,不解析其内部输出)。
#
# ⚠️ 可扩展:未来加并发前检查(eg 其它 mirror SHA / workspace schema / 并发锁状态 /
#   新抽出的 lib mirror —— 如 forge v5 M0-2 若抽出新 source-able lib,IDS mirror 它后
#   把对应 mirror-sha 测试加进这里),只需往下面 CHECKS array 追加一行,无需改判定逻辑。
#
# 当前(v5 M0-1)只挂一项:verdict-evidence 共享 lib mirror SHA 一致性。
# 范式注:用 indexed array(macOS 默认 bash 3.2 无 associative array · 同 verify-all-outcomes.sh)。
CHECKS=(
  "verdict-evidence-mirror|$SCRIPT_DIR/tests/integration/test-verdict-evidence-mirror-sha.sh"
)

# ──────────────────────────────────────────────────────────────
# 跑全部 check · 聚合 PASS/FAIL
# ──────────────────────────────────────────────────────────────
TS_ISO=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "================================================================="
echo "并发前 preflight gate · idea 006 forge v5 M0-1 · $TS_ISO"
echo "================================================================="
echo ""

FAIL=0
PASS_COUNT=0
FAIL_COUNT=0

for entry in "${CHECKS[@]}"; do
  LABEL="${entry%%|*}"
  CHECK_SCRIPT="${entry##*|}"

  echo "----- check · $LABEL -----"
  if [ ! -f "$CHECK_SCRIPT" ]; then
    echo "[FAIL] check 脚本不存在: $CHECK_SCRIPT" >&2
    FAIL=1
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo ""
    continue
  fi

  # 跑子 check(捕获输出 · 只靠 exit code 判定)
  CHECK_OUT=$(bash "$CHECK_SCRIPT" 2>&1)
  CHECK_RC=$?
  if [ "$CHECK_RC" -eq 0 ]; then
    echo "[PASS] $LABEL · mirror 一致"
    PASS_COUNT=$((PASS_COUNT + 1))
  else
    echo "[FAIL] $LABEL · RC=$CHECK_RC · drift / 隐患如下:" >&2
    # 把子 check 的 drift 报告透传给 operator(便于定位)
    echo "$CHECK_OUT" | tail -15 >&2
    FAIL=1
    FAIL_COUNT=$((FAIL_COUNT + 1))
  fi
  echo ""
done

# ──────────────────────────────────────────────────────────────
# 汇总 + 退码
# ──────────────────────────────────────────────────────────────
echo "================================================================="
if [ "$FAIL" -eq 0 ]; then
  echo "PREFLIGHT PASS · ${PASS_COUNT} check 全绿 · mirror 一致 · 可起并发批次"
  echo "================================================================="
  exit 0
else
  echo "PREFLIGHT FAIL · ${FAIL_COUNT} check FAIL / ${PASS_COUNT} PASS · 不可起并发批次"
  echo "  修复 drift(重新 mirror / cp SSOT)后重跑本 preflight · exit 0 才起并发"
  echo "================================================================="
  exit 1
fi
