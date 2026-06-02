#!/usr/bin/env bash
# test-concurrency-preflight.sh · idea 006 forge v5 M0-1 · concurrency-preflight.sh 自测
#
# 结论先:验并发前 preflight gate 的正/负路径 + 可扩展性 + 不污染 SSOT。
#   gate 自己若 drift(eg 误删 check / 判定逻辑反)无人知 · 故 preflight 本身要可测。
#
# 4 个用例:
#   1. 正路径:真 preflight(mirror 一致)→ exit 0 + stdout 含 PREFLIGHT PASS
#   2. FAIL 聚合:临时 preflight 副本 CHECKS 指向必 FAIL stub → exit 1 + 含 PREFLIGHT FAIL
#   3. 可扩展性自检:真 preflight 的 CHECKS array 当前恰好 1 项(verdict-evidence)· 防误删
#   4. 不污染 SSOT:测试前后真 mirror 两件 lib+wrapper SHA 字节不变
#
# ⚠️ 负路径(用例 2)**不真改 mirror 文件**(破坏 SSOT)· 而是注入必 FAIL stub 验聚合逻辑。
#   "真改 mirror 会被抓到" 由已有 test-verdict-evidence-mirror-sha.sh 负责 · 本测试不重复。

set -uo pipefail

IDS_ROOT="/Users/admin/codes/ideababy_stroller"
KIT="$IDS_ROOT/framework/xenodev-bootstrap-kit"
PREFLIGHT="$KIT/concurrency-preflight.sh"
LIB_MIRROR="$KIT/handback-validator/verdict-evidence-lib.sh"
WRAPPER_MIRROR="$KIT/handback-validator/validate-verdict-evidence.sh"

FAIL=0
TMPDIR_TEST=""

# cleanup trap · 删临时副本 · 不留垃圾
cleanup() {
  [ -n "$TMPDIR_TEST" ] && [ -d "$TMPDIR_TEST" ] && rm -rf "$TMPDIR_TEST"
}
trap cleanup EXIT

# === 记录测试前真 mirror SHA(用例 4 复原断言) ===
LIB_SHA_BEFORE=$(shasum -a 256 "$LIB_MIRROR" | awk '{print $1}')
WRAPPER_SHA_BEFORE=$(shasum -a 256 "$WRAPPER_MIRROR" | awk '{print $1}')

# ──────────────────────────────────────────────────────────────
# 用例 1 · 正路径(真 preflight · mirror 一致 → exit 0 + PREFLIGHT PASS)
# ──────────────────────────────────────────────────────────────
echo "----- 用例 1 · 正路径 preflight exit 0 -----"
OUT1=$(bash "$PREFLIGHT" 2>&1)
RC1=$?
if [ "$RC1" -eq 0 ] && echo "$OUT1" | grep -q "PREFLIGHT PASS"; then
  echo "PASS · preflight exit 0 + PREFLIGHT PASS"
else
  echo "FAIL · 期望 exit 0 + PREFLIGHT PASS · 实得 RC=$RC1"
  echo "$OUT1" | tail -8
  FAIL=1
fi
echo ""

# ──────────────────────────────────────────────────────────────
# 用例 2 · FAIL 聚合(临时 preflight 副本 · CHECKS 指向必 FAIL stub → exit 1)
# ──────────────────────────────────────────────────────────────
# 造临时副本:复制真 preflight,把 CHECKS 那行替换为指向一个必 exit 1 的 stub。
# 完全不碰真 preflight / 真 mirror。
echo "----- 用例 2 · FAIL 聚合 exit 1 -----"
TMPDIR_TEST=$(mktemp -d)
FAIL_STUB="$TMPDIR_TEST/always-fail.sh"
cat > "$FAIL_STUB" <<'STUB'
#!/usr/bin/env bash
echo "FAIL[stub] 模拟 mirror drift" >&2
exit 1
STUB
chmod +x "$FAIL_STUB"

PREFLIGHT_COPY="$TMPDIR_TEST/preflight-copy.sh"
# 复制真 preflight · 把 CHECKS array 唯一行替换为指向 fail stub
#（sed 替换 CHECKS 内那条 "verdict-evidence-mirror|..." 行为 "drift-sim|$FAIL_STUB"）
sed "s#\"verdict-evidence-mirror|.*\"#\"drift-sim|$FAIL_STUB\"#" "$PREFLIGHT" > "$PREFLIGHT_COPY"

OUT2=$(bash "$PREFLIGHT_COPY" 2>&1)
RC2=$?
if [ "$RC2" -eq 1 ] && echo "$OUT2" | grep -q "PREFLIGHT FAIL"; then
  echo "PASS · 模拟 drift → preflight exit 1 + PREFLIGHT FAIL"
else
  echo "FAIL · 期望 exit 1 + PREFLIGHT FAIL · 实得 RC=$RC2"
  echo "$OUT2" | tail -8
  FAIL=1
fi
echo ""

# ──────────────────────────────────────────────────────────────
# 用例 3 · 可扩展性自检(真 preflight CHECKS 当前恰好 1 项 · 防误删/误增越 scope)
# ──────────────────────────────────────────────────────────────
# 数真 preflight CHECKS array 里 "标签|路径" 行数(只数 CHECKS=( ... ) 块内含 | 的引号行)。
echo "----- 用例 3 · 可扩展性自检 CHECKS=1 项 -----"
CHECK_LINES=$(awk '/^CHECKS=\(/{f=1; next} /^\)/{f=0} f && /\|/{c++} END{print c+0}' "$PREFLIGHT")
if [ "$CHECK_LINES" -eq 1 ]; then
  echo "PASS · CHECKS 当前恰好 1 项(verdict-evidence · scope 对齐 v5 M0-1)"
else
  echo "FAIL · CHECKS 应为 1 项 · 实得 $CHECK_LINES(误删或越 scope 加 check?)"
  FAIL=1
fi
echo ""

# ──────────────────────────────────────────────────────────────
# 用例 4 · 不污染 SSOT(测试前后真 mirror 两件 SHA 字节不变)
# ──────────────────────────────────────────────────────────────
echo "----- 用例 4 · 不污染 SSOT mirror SHA 复原 -----"
LIB_SHA_AFTER=$(shasum -a 256 "$LIB_MIRROR" | awk '{print $1}')
WRAPPER_SHA_AFTER=$(shasum -a 256 "$WRAPPER_MIRROR" | awk '{print $1}')
if [ "$LIB_SHA_BEFORE" = "$LIB_SHA_AFTER" ] && [ "$WRAPPER_SHA_BEFORE" = "$WRAPPER_SHA_AFTER" ]; then
  echo "PASS · 真 mirror 两件 SHA 字节不变(测试未污染 SSOT)"
else
  echo "FAIL · mirror SHA 被改动!lib: $LIB_SHA_BEFORE → $LIB_SHA_AFTER · wrapper: $WRAPPER_SHA_BEFORE → $WRAPPER_SHA_AFTER"
  FAIL=1
fi
echo ""

# ──────────────────────────────────────────────────────────────
# 汇总
# ──────────────────────────────────────────────────────────────
if [ "$FAIL" -eq 0 ]; then
  echo "ALL PASS · concurrency-preflight 4 用例全绿(正路径 + FAIL 聚合 + 可扩展自检 + 不污染 SSOT)"
  exit 0
else
  echo "FAILED · 见上"
  exit 1
fi
