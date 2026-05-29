#!/usr/bin/env bash
# T101 SHA dual-verify · 验 3 producer 文件从 XenoDev SSOT cp 到 IDS bootstrap-kit
# 模式同 T100b · cp 前跑 = red(SHA 不等或 target 缺)· cp 后跑 = green(三文件 SHA 全等)
#
# 真路径 mirror 对照表:
#   templates/handback.template.md
#   gen-handback.sh
#   score-handback.sh
set -uo pipefail

XENODEV_ROOT="/Users/admin/codes/XenoDev"
IDS_ROOT="/Users/admin/codes/ideababy_stroller"
SRC_BASE="$XENODEV_ROOT/lib/handback-validator"
TGT_BASE="$IDS_ROOT/framework/xenodev-bootstrap-kit/handback-validator"

FILES=(
  "templates/handback.template.md"
  "gen-handback.sh"
  "score-handback.sh"
)

FAIL=0
for f in "${FILES[@]}"; do
  SRC="$SRC_BASE/$f"
  TGT="$TGT_BASE/$f"

  if [ ! -f "$SRC" ]; then
    echo "FAIL[src-missing] $f · src=$SRC 不存在"
    FAIL=1
    continue
  fi
  if [ ! -f "$TGT" ]; then
    echo "FAIL[tgt-missing] $f · tgt=$TGT 不存在"
    FAIL=1
    continue
  fi

  SRC_SHA=$(shasum -a 256 "$SRC" | awk '{print $1}')
  TGT_SHA=$(shasum -a 256 "$TGT" | awk '{print $1}')

  if [ "$SRC_SHA" != "$TGT_SHA" ]; then
    echo "FAIL[sha-diff] $f · src=$SRC_SHA · tgt=$TGT_SHA"
    FAIL=1
  else
    echo "PASS $f · sha=$SRC_SHA"
  fi
done

# perms 校验(2 个 .sh 必须保 +x · template 是 .md 无 +x 要求)
for f in gen-handback.sh score-handback.sh; do
  TGT="$TGT_BASE/$f"
  if [ -f "$TGT" ] && [ ! -x "$TGT" ]; then
    echo "FAIL[perm] $f · target 缺 +x"
    FAIL=1
  fi
done

# symlink 拒
if find "$TGT_BASE" -maxdepth 2 -type l 2>/dev/null | grep -q .; then
  echo "FAIL[symlink] $TGT_BASE 子树含 symlink"
  FAIL=1
fi

if [ "$FAIL" -eq 0 ]; then
  echo "ALL PASS · 3 mirror files SHA 严格相等 + perms ok"
  exit 0
else
  echo "FAILED"
  exit 1
fi
