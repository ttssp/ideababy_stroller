#!/usr/bin/env bash
# T105 SHA dual-verify · 验 event-schema.json 从 XenoDev SSOT cp 到 IDS bootstrap-kit
# 模式同 T100b / T101 · cp 前跑 = red(SHA 不等)· cp 后跑 = green(SHA 严格相等 + grep gate)
set -uo pipefail

XENODEV_ROOT="/Users/admin/codes/XenoDev"
IDS_ROOT="/Users/admin/codes/ideababy_stroller"
SRC="$XENODEV_ROOT/lib/eval-event-log/event-schema.json"
TGT="$IDS_ROOT/framework/xenodev-bootstrap-kit/eval-event-log/event-schema.json"

FAIL=0

# === SHA dual-verify ===
if [ ! -f "$SRC" ]; then
  echo "FAIL[src-missing] $SRC 不存在"
  FAIL=1
fi
if [ ! -f "$TGT" ]; then
  echo "FAIL[tgt-missing] $TGT 不存在"
  FAIL=1
fi

if [ "$FAIL" -eq 0 ]; then
  SRC_SHA=$(shasum -a 256 "$SRC" | awk '{print $1}')
  TGT_SHA=$(shasum -a 256 "$TGT" | awk '{print $1}')
  if [ "$SRC_SHA" != "$TGT_SHA" ]; then
    echo "FAIL[sha-diff] src=$SRC_SHA · tgt=$TGT_SHA"
    FAIL=1
  else
    echo "PASS sha · $SRC_SHA"
  fi

  # === grep gate · T104 真路径迁移要求(grep -c 返 0 命中也 exit 1 · 单独 wrap)===
  PLURAL_HITS=$(grep -c 'handback_drifts' "$TGT" 2>/dev/null); PLURAL_HITS="${PLURAL_HITS:-0}"
  if [ "$PLURAL_HITS" -lt 1 ]; then
    echo "FAIL[no-plural] $TGT 不含 handback_drifts ($PLURAL_HITS 命中)"
    FAIL=1
  else
    echo "PASS plural · handback_drifts $PLURAL_HITS 命中"
  fi

  SINGULAR_HITS=$(grep -c 'handback_drift[^s]' "$TGT" 2>/dev/null); SINGULAR_HITS="${SINGULAR_HITS:-0}"
  if [ "$SINGULAR_HITS" -ne 0 ]; then
    echo "FAIL[stale-singular] $TGT 仍含 OLD 单数 handback_drift ($SINGULAR_HITS 命中)"
    FAIL=1
  else
    echo "PASS gate · OLD 单数 'handback_drift[^s]' 0 命中(T104 迁移真路径)"
  fi
fi

# === symlink 拒(同 T101 防写树外)===
if [ -L "$TGT" ]; then
  echo "FAIL[symlink] $TGT 是 symlink"
  FAIL=1
fi

if [ "$FAIL" -eq 0 ]; then
  echo "ALL PASS · event-schema.json mirror SHA 等 + T104 迁移真路径完整"
  exit 0
else
  echo "FAILED"
  exit 1
fi
