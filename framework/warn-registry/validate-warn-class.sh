#!/usr/bin/env bash
# validate-warn-class.sh — warn registry schema 校验 + due_event 到期查询
# per ideababy_stroller discussion/006/forge/v10/stage-forge-006-v10.md(verdict)
#      + framework/warn-registry/README.md(schema 与三态裁决)
#
# Usage:
#   validate-warn-class.sh                      # 全表 schema 校验(hard gate)
#   validate-warn-class.sh --due-at <gate>      # 列出在 <gate> 到期、需三态裁决的 temporary warn
#
# 🔴 **本 gate 是 hard 的,不是第四个 warn。** exit 1 即拒 —— 这是本机制与它废掉的
# 三条「复发 ≥N 次」判据之间的全部区别(v10 verdict)。
#
# exit 0 = PASS / 无到期项
# exit 1 = schema 违规,或 --due-at 命中到期未裁决项
# exit 2 = usage / registry 不可读(fail-closed:registry 读不到不得静默放行)

set -euo pipefail

REGISTRY="${WARN_REGISTRY:-framework/warn-registry/registry.jsonl}"
MODE="validate"
DUE_GATE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --due-at) MODE="due"; DUE_GATE="${2:-}"; shift 2 ;;
        --registry) REGISTRY="${2:-}"; shift 2 ;;
        -h|--help)
            echo "Usage: validate-warn-class.sh [--due-at <gate>] [--registry <path>]" >&2
            exit 2 ;;
        *) echo "ERR: unknown arg: $1" >&2; exit 2 ;;
    esac
done

if [[ "$MODE" == "due" && -z "$DUE_GATE" ]]; then
    echo "ERR: --due-at 需要 gate 名" >&2; exit 2
fi

if [[ ! -f "$REGISTRY" ]]; then
    echo "🔴 FAIL-CLOSED: warn registry 不可读: $REGISTRY" >&2
    echo "   registry 读不到**不得静默放行**(同 obligations ledger 的取舍)。" >&2
    echo "   恢复路径: git checkout $REGISTRY" >&2
    exit 2
fi

python3 - "$REGISTRY" "$MODE" "$DUE_GATE" <<'PYEOF'
import json, os, sys

registry, mode, due_gate = sys.argv[1], sys.argv[2], sys.argv[3]
VALID_CLASSES = {"soft advisory", "temporary"}
BASE = ("★", "id title site warn_class declared_at declared_by_gate source".split())

rows, errors = [], []
with open(registry, encoding="utf-8") as fh:
    for lineno, raw in enumerate(fh, 1):
        if not raw.strip():
            continue
        try:
            rows.append((lineno, json.loads(raw)))
        except json.JSONDecodeError as exc:
            errors.append(f"L{lineno}: JSON 解析失败 — {exc}")

seen = {}
for lineno, r in rows:
    rid = r.get("id", f"<no-id@L{lineno}>")

    for field in BASE[1]:
        if not r.get(field):
            errors.append(f"{rid}: 缺必填字段 `{field}`")

    if rid in seen:
        errors.append(f"{rid}: id 重复(另见 L{seen[rid]})—— id 必须稳定且唯一")
    seen[rid] = lineno

    wc = r.get("warn_class")
    if wc not in VALID_CLASSES:
        errors.append(f"{rid}: warn_class=`{wc}` 非法,只能是 {sorted(VALID_CLASSES)}")

    # site 存在性(路径类声明会 stale —— 这正是 KG-B17/B18/B19 同族的病)
    site = (r.get("site") or "").split(":")[0]
    if site and not os.path.exists(site):
        errors.append(f"{rid}: site 不存在于磁盘: `{site}` —— 路径类声明已 stale")

    if wc == "soft advisory":
        if r.get("no_upgrade_plan") is not True:
            errors.append(f"{rid}: soft advisory 必须显式 `no_upgrade_plan: true`"
                          " —— 承 PEP 387『永久 defer 合法,但必须承认无移除计划』")
        if not r.get("rationale"):
            errors.append(f"{rid}: soft advisory 的 `rationale` 不得留白")
        for forbidden in ("due_event", "owner", "consumer_gate"):
            if r.get(forbidden):
                errors.append(f"{rid}: soft advisory 不应带 `{forbidden}`"
                              "(带了说明它其实是 temporary,分型错)")

    elif wc == "temporary":
        for field in ("owner", "due_event", "consumer_gate"):
            if not r.get(field):
                errors.append(f"{rid}: temporary 必须带 `{field}`")
        if "consumer_wired" not in r:
            errors.append(f"{rid}: temporary 必须带 `consumer_wired`")
        elif r.get("consumer_wired") is False and not r.get("exposure"):
            errors.append(f"{rid}: consumer_wired=false 时 `exposure` 必填 —— 敞口要可见,不能沉默")
        # 🔴 v10 核心:due_event 不得是次数
        due = str(r.get("due_event") or "")
        if any(tok in due for tok in ("≥", ">=", "次", "count", "times")):
            errors.append(f"{rid}: `due_event` 像一个**次数**而不是 gate 事件: `{due}`"
                          " —— v10 已作废「复发 ≥N 次」型判据(无计数者/无消费点/无执行者)")

if mode == "due":
    if errors:
        print("🔴 registry schema 有违规,--due-at 拒绝在脏数据上作答:", file=sys.stderr)
        for e in errors:
            print(f"   · {e}", file=sys.stderr)
        sys.exit(1)
    hits = [r for _, r in rows
            if r.get("warn_class") == "temporary" and r.get("due_event") == due_gate]
    for r in hits:
        blocked = f"  ⛔ blocked_on={r['blocked_on']}" if r.get("blocked_on") else ""
        print(f"DUE {r['id']} | owner={r['owner']}{blocked}")
        print(f"    {r['title']}")
    print(f"COUNT {len(hits)}")
    if hits:
        print("", file=sys.stderr)
        print(f"🔴 上列 {len(hits)} 条 temporary warn 在 `{due_gate}` 到期,必须**三态裁决**:", file=sys.stderr)
        print("   convert(升 hard-fail)/ revert(移除机制)/ defer(具名签署 + 写明理由 + 给出新 due_event)", file=sys.stderr)
        print("   —— 或改判 soft advisory(须补 no_upgrade_plan + rationale)。", file=sys.stderr)
        print("   ⚠ **被遗忘的 defer 不是 defer,是缺席。**", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)

# mode == validate
if errors:
    print(f"🔴 FAIL · warn registry schema 违规 {len(errors)} 处 —— 这是 hard gate,不是 warn:", file=sys.stderr)
    for e in errors:
        print(f"   · {e}", file=sys.stderr)
    sys.exit(1)

soft = sum(1 for _, r in rows if r.get("warn_class") == "soft advisory")
temp = sum(1 for _, r in rows if r.get("warn_class") == "temporary")
print(f"✓ warn registry PASS · {len(rows)} 条(soft advisory {soft} · temporary {temp})", file=sys.stderr)
sys.exit(0)
PYEOF
