#!/usr/bin/env bash
# verdict-evidence mirror SHA dual-verify · 验 verdict-evidence-lib.sh + validate-verdict-evidence.sh
# 从 XenoDev SSOT cp 到 IDS bootstrap-kit · 模式同 T100b/T101/T105。
# 结论先:本测试守住 idea 006 forge v4 P0 原子波的 mirror 完整性 ——
#   两件(lib + wrapper)IDS mirror 必须与 XenoDev SSOT 字节级一致(SHA 严格相等)。
#   cp 前跑 = red(SHA 不等)· cp 后跑 = green。
# 加固(per XenoDev handoff §5 硬告警):lib 必须含 resolve_review_log_path allowlist
#   安全 helper(codex F2 trust-boundary 加固)· 防 mirror 时退回缺 allowlist 的旧版。
set -uo pipefail

XENODEV_ROOT="/Users/admin/codes/XenoDev"
IDS_ROOT="/Users/admin/codes/ideababy_stroller"

# 两件 mirror · source(XenoDev SSOT)→ target(IDS bootstrap-kit)
declare -a FILES=(
  "lib/handback-validator/verdict-evidence-lib.sh|framework/xenodev-bootstrap-kit/handback-validator/verdict-evidence-lib.sh"
  "lib/handback-validator/validate-verdict-evidence.sh|framework/xenodev-bootstrap-kit/handback-validator/validate-verdict-evidence.sh"
)

FAIL=0

for entry in "${FILES[@]}"; do
  SRC_REL="${entry%%|*}"
  TGT_REL="${entry##*|}"
  SRC="$XENODEV_ROOT/$SRC_REL"
  TGT="$IDS_ROOT/$TGT_REL"
  BASE=$(basename "$SRC")

  # === 存在性 ===
  if [ ! -f "$SRC" ]; then echo "FAIL[src-missing] $SRC"; FAIL=1; continue; fi
  if [ ! -f "$TGT" ]; then echo "FAIL[tgt-missing] $TGT"; FAIL=1; continue; fi

  # === symlink 拒(防写树外)===
  if [ -L "$TGT" ]; then echo "FAIL[symlink] $TGT 是 symlink"; FAIL=1; continue; fi

  # === SHA dual-verify(字节级一致)===
  SRC_SHA=$(shasum -a 256 "$SRC" | awk '{print $1}')
  TGT_SHA=$(shasum -a 256 "$TGT" | awk '{print $1}')
  if [ "$SRC_SHA" != "$TGT_SHA" ]; then
    echo "FAIL[sha-diff] $BASE · src=$SRC_SHA · tgt=$TGT_SHA"
    FAIL=1
  else
    echo "PASS sha · $BASE · $SRC_SHA"
  fi
done

# === 安全 helper gate · per handoff §5 + codex F2 ===
# lib mirror 必须含 resolve_review_log_path(allowlist/canonicalize trust-boundary 加固)·
# 防退回缺 allowlist 的旧版 lib(旧版 `$xenodev/$path` 裸拼接 → ../ 逃逸)。
LIB_TGT="$IDS_ROOT/framework/xenodev-bootstrap-kit/handback-validator/verdict-evidence-lib.sh"
if [ -f "$LIB_TGT" ]; then
  HELPER_HITS=$(grep -c 'resolve_review_log_path()' "$LIB_TGT" 2>/dev/null); HELPER_HITS="${HELPER_HITS:-0}"
  if [ "$HELPER_HITS" -lt 1 ]; then
    echo "FAIL[no-allowlist-helper] lib mirror 缺 resolve_review_log_path · 疑似旧版(缺 codex F2 trust-boundary 加固)"
    FAIL=1
  else
    echo "PASS gate · resolve_review_log_path allowlist 安全 helper 在位($HELPER_HITS 命中)"
  fi
fi

if [ "$FAIL" -eq 0 ]; then
  echo "ALL PASS · verdict-evidence 两件 mirror SHA 字节一致 + allowlist 安全 helper 完整"
  exit 0
else
  echo "FAILED"
  exit 1
fi
