#!/usr/bin/env bash
# T102 · scan-credentials.sh 测试套
# per spec O4 + R-Sec1 + backlog C-1:
# V1 positive: fake-secret fixture · 期望 exit=1
# V2 negative: clean fixture · 期望 exit=0
# V3 exclude flag: --exclude-paths glob · 期望白名单文件不算 violation
# V4 ignore file: .scan-credentials-ignore 真路径白名单 · 期望 ignore 列出的文件不算
# V5 regression: 当前 XenoDev 仓在白名单后 · 期望 exit=0(false positive 治理)
# V6 v0.1 11 hand-back 包(若 IDS 仓存在) · 期望全 exit=0

set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCAN="$REPO/.claude/safety-floor/credential-isolation/scan-credentials.sh"
SCAN_SHIM="$REPO/lib/handback-validator/scan-credentials.sh"  # spec verification 真路径

[ -x "$SCAN" ] || { echo "ERR: $SCAN 不存在或无 +x" >&2; exit 2; }
[ -x "$SCAN_SHIM" ] || { echo "ERR: $SCAN_SHIM compat shim 不存在或无 +x" >&2; exit 2; }

TMPDIR=$(mktemp -d -t t102-scan.XXXXXX)
trap "rm -rf $TMPDIR" EXIT

PASS_CNT=0
FAIL_CNT=0
report() {
  local rc="$1" msg="$2" detail="${3:-}"
  if [ "$rc" -eq 0 ]; then
    echo "  PASS: $msg"
    PASS_CNT=$((PASS_CNT + 1))
  else
    echo "  FAIL: $msg"
    [ -n "$detail" ] && echo "    detail: $detail"
    FAIL_CNT=$((FAIL_CNT + 1))
  fi
}

# === V0 真路径 · spec verification 命令 lib shim forward 真路径 ===
echo "=== V0: lib/handback-validator/scan-credentials.sh shim forward ==="
mkdir -p "$TMPDIR/v0"
echo "API_KEY=fake" > "$TMPDIR/v0/.env.production"
bash "$SCAN_SHIM" "$TMPDIR/v0" >/dev/null 2>&1
RC=$?
[ "$RC" -eq 1 ] && report 0 "V0 shim forward · 真路径 detect production env · exit=1" || report 1 "V0 shim" "rc=$RC (期望 1)"

# === V1 positive · 含 .env.production → exit 1 ===
echo "=== V1: positive · .env.production → exit 1 ==="
mkdir -p "$TMPDIR/v1"
echo "API_KEY=fake" > "$TMPDIR/v1/.env.production"
bash "$SCAN" "$TMPDIR/v1" >/dev/null 2>&1
RC=$?
[ "$RC" -eq 1 ] && report 0 "V1 positive · exit=1" || report 1 "V1 positive" "rc=$RC (期望 1)"

# === V2 negative · clean fixture → exit 0 ===
echo "=== V2: negative · clean fixture → exit 0 ==="
mkdir -p "$TMPDIR/v2"
echo "just text" > "$TMPDIR/v2/README.md"
bash "$SCAN" "$TMPDIR/v2" >/dev/null 2>&1
RC=$?
[ "$RC" -eq 0 ] && report 0 "V2 negative · exit=0" || report 1 "V2 negative" "rc=$RC (期望 0)"

# === V3 --exclude-paths flag · 排除指定 glob → exit 0 ===
echo "=== V3: --exclude-paths flag ==="
mkdir -p "$TMPDIR/v3/docs"
echo "prod://example-in-doc" > "$TMPDIR/v3/docs/protocol.md"
# 无 flag:exit 1 (检出 docs/protocol.md)
bash "$SCAN" "$TMPDIR/v3" >/dev/null 2>&1
RC1=$?
[ "$RC1" -eq 1 ] && report 0 "V3a 无 flag · 真检出 doc · exit=1" || report 1 "V3a no flag" "rc=$RC1 (期望 1)"
# 有 flag:exit 0
bash "$SCAN" --exclude-paths 'docs/*' "$TMPDIR/v3" >/dev/null 2>&1
RC2=$?
[ "$RC2" -eq 0 ] && report 0 "V3b --exclude-paths 'docs/*' · exit=0" || report 1 "V3b flag" "rc=$RC2 (期望 0)"

# === V4 .scan-credentials-ignore 白名单 → exit 0 ===
echo "=== V4: .scan-credentials-ignore 白名单 ==="
mkdir -p "$TMPDIR/v4/notes"
echo "prod://example" > "$TMPDIR/v4/notes/example.md"
cat > "$TMPDIR/v4/.scan-credentials-ignore" <<EOF
# T102 white-list false positive · doc reference
notes/example.md
EOF
bash "$SCAN" "$TMPDIR/v4" >/dev/null 2>&1
RC=$?
[ "$RC" -eq 0 ] && report 0 "V4 .scan-credentials-ignore · exit=0" || report 1 "V4 ignore file" "rc=$RC (期望 0)"

# === V5 regression · 当前 XenoDev 仓 + .scan-credentials-ignore → exit 0 ===
echo "=== V5: regression · XenoDev 当前仓 + ignore → exit 0 ==="
# 在仓根 scan(已有 .scan-credentials-ignore 列 14 false positive)
bash "$SCAN" "$REPO" >/dev/null 2>&1
RC=$?
[ "$RC" -eq 0 ] && report 0 "V5 regression · XenoDev 仓 exit=0(false positive 治理)" || report 1 "V5 regression" "rc=$RC (期望 0)"

# === V6 v0.1 hand-back 包(IDS 仓 · 若存在 · 真路径 scan 不挂 ship)===
# per codex R1 P2:真路径捕 exit code · 任一 hand-back scan exit != 0 → FAIL
echo "=== V6: v0.1 hand-back 包(IDS · 若存在 · 真捕 exit)==="
IDS_HB="/Users/admin/codes/ideababy_stroller/discussion/006/handback"
if [ -d "$IDS_HB" ]; then
  V6_DIR="$TMPDIR/v6"
  mkdir -p "$V6_DIR"
  HB_CNT=0
  V6_FAIL=0
  V6_FAIL_FILES=()
  for hb in "$IDS_HB"/2026*.md; do
    [ -f "$hb" ] || continue
    HB_CNT=$((HB_CNT + 1))
    # 隔离每个 hand-back 到独立 dir 真路径 scan
    # per codex R6 真路径:用 spec verification 真路径 file-arg 模式(.md 真路径 doc 真路径放)
    bash "$SCAN" "$hb" >/dev/null 2>&1
    RC=$?
    if [ "$RC" -ne 0 ]; then
      V6_FAIL=$((V6_FAIL + 1))
      V6_FAIL_FILES+=("$(basename "$hb")")
    fi
  done
  if [ "$HB_CNT" -eq 0 ]; then
    echo "  SKIP: IDS hand-back dir 为空"
  elif [ "$V6_FAIL" -eq 0 ]; then
    report 0 "V6 v0.1 hand-back 包($HB_CNT 包) · 全 exit=0(scan 不挂 ship)"
  else
    report 1 "V6 v0.1 hand-back $V6_FAIL/$HB_CNT 包真 scan fail" "files=${V6_FAIL_FILES[*]}"
  fi
else
  echo "  SKIP: IDS hand-back dir 不存在"
fi

# === V7 真路径安全 · 白名单不应绕过 .env.production 真凭据(per codex R1 P1)===
echo "=== V7: 白名单不放行 .env.production hard block ==="
mkdir -p "$TMPDIR/v7"
echo "DB_PASSWORD=real_secret" > "$TMPDIR/v7/.env.production"
# 试图用 --exclude-paths + .scan-credentials-ignore 绕过
cat > "$TMPDIR/v7/.scan-credentials-ignore" <<EOF
.env.production
EOF
bash "$SCAN" --exclude-paths '.env.production' "$TMPDIR/v7" >/dev/null 2>&1
RC=$?
[ "$RC" -eq 1 ] && report 0 "V7 真路径安全 · 白名单不放行 .env.production · exit=1" || report 1 "V7 真路径安全" "rc=$RC (期望 1 · 白名单不应绕过 hard block)"

# === V8 真路径安全 · 白名单不应绕过 secrets/production/ 真凭据 ===
echo "=== V8: 白名单不放行 secrets/production/ hard block ==="
mkdir -p "$TMPDIR/v8/secrets/production"
echo "KEY=real" > "$TMPDIR/v8/secrets/production/api.key"
cat > "$TMPDIR/v8/.scan-credentials-ignore" <<EOF
secrets/production/api.key
secrets/
EOF
bash "$SCAN" --exclude-paths 'secrets/production/api.key' "$TMPDIR/v8" >/dev/null 2>&1
RC=$?
[ "$RC" -eq 1 ] && report 0 "V8 真路径安全 · 白名单不放行 secrets/production/ · exit=1" || report 1 "V8 真路径安全" "rc=$RC (期望 1)"

# === V9 真路径(per codex R2 P2.1):顶层 ignore 不放行 nested basename 同名 ===
echo "=== V9: basename match 不放行 nested per-project context ==="
mkdir -p "$TMPDIR/v9/projects/subA"
echo "doc reference prod://example" > "$TMPDIR/v9/AGENTS.md"
echo "doc reference prod://example" > "$TMPDIR/v9/projects/subA/AGENTS.md"
cat > "$TMPDIR/v9/.scan-credentials-ignore" <<EOF
AGENTS.md
EOF
bash "$SCAN" "$TMPDIR/v9" >/dev/null 2>&1
RC=$?
# 真路径:顶层 AGENTS.md 放行 · projects/subA/AGENTS.md hit · exit=1
[ "$RC" -eq 1 ] && report 0 "V9 nested AGENTS.md 仍 hit · 顶层 ignore 不误放行" || report 1 "V9 nested" "rc=$RC (期望 1)"

# === V10 真路径(per codex R5 P2):trailing slash 真路径规范化 ===
echo "=== V10: trailing slash SCAN_DIR 真路径规范化 ==="
mkdir -p "$TMPDIR/v10/notes"
echo "doc reference prod://example" > "$TMPDIR/v10/notes/doc.md"
cat > "$TMPDIR/v10/.scan-credentials-ignore" <<EOF
notes/doc.md
EOF
# 真路径调用 1:无 trailing slash
bash "$SCAN" "$TMPDIR/v10" >/dev/null 2>&1
RC1=$?
# 真路径调用 2:有 trailing slash
bash "$SCAN" "$TMPDIR/v10/" >/dev/null 2>&1
RC2=$?
# 真路径调用 3:多个 trailing slash
bash "$SCAN" "$TMPDIR/v10///" >/dev/null 2>&1
RC3=$?
if [ "$RC1" -eq 0 ] && [ "$RC2" -eq 0 ] && [ "$RC3" -eq 0 ]; then
  report 0 "V10 trailing slash 真路径规范化 · 三 case 全 exit=0"
else
  report 1 "V10 trailing slash" "no-slash=$RC1 one-slash=$RC2 multi-slash=$RC3 (期望全 0)"
fi

echo ""
echo "=== Summary ==="
echo "PASS: $PASS_CNT"
echo "FAIL: $FAIL_CNT"
[ "$FAIL_CNT" -eq 0 ]
