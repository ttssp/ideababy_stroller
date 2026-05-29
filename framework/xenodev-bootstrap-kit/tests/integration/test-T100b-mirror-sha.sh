#!/usr/bin/env bash
# test-T100b-mirror-sha.sh — T100b · check-6 字节级 mirror SHA dual-verify
#
# 测试 IDS bootstrap-kit 镜像的 check-6 与 XenoDev SSOT 字节级一致。
# 红:cp 前 / 漂移 → SHA 不等 → exit 1
# 绿:cp 后 → SHA 严格相等 → exit 0

set -u

XENODEV_SRC="/Users/admin/codes/XenoDev/lib/handback-validator/check-6-id-charset-and-final-path.sh"
IDS_TGT="/Users/admin/codes/ideababy_stroller/framework/xenodev-bootstrap-kit/handback-validator/check-6-id-charset-and-final-path.sh"

[ -f "$XENODEV_SRC" ] || { echo "FAIL · XenoDev source 不存在: $XENODEV_SRC" >&2; exit 2; }
[ -f "$IDS_TGT" ]    || { echo "FAIL · IDS target 不存在: $IDS_TGT" >&2; exit 2; }

SRC_SHA=$(shasum -a 256 "$XENODEV_SRC" | awk '{print $1}')
TGT_SHA=$(shasum -a 256 "$IDS_TGT"    | awk '{print $1}')

echo "XenoDev source SHA: $SRC_SHA"
echo "IDS target SHA:     $TGT_SHA"

if [ "$SRC_SHA" = "$TGT_SHA" ]; then
  echo "PASS · SHA dual-verify 字节级镜像一致"
  exit 0
else
  echo "FAIL · SHA 不等 · mirror 漂移 (T100 在 XenoDev 改完未 cp 到 IDS)" >&2
  exit 1
fi
