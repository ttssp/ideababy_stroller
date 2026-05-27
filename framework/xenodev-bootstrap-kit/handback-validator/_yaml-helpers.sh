#!/usr/bin/env bash
# _yaml-helpers.sh — 共享 YAML frontmatter 解析 helpers
# 给 validate-handback.sh 和 gen-handback.sh 共用。
#
# 设计决议(2026-05-11 RETRO 后,第一性原理):
#   - 既存 5 个 validator 脚本统一用 awk/grep/sed,无 yq → consistency
#   - yq v3 / v4 syntax breaking change → macOS 用户体验不一致
#   - 0 外部依赖,test 在 CI 不需 brew install yq
#
# 此 helper **被 source**,不直接执行;不应有 set -euo pipefail
# (会污染调用方 shell 选项)。函数本身用 local var + return code 控错。
#
# 接口:
#   extract_yaml_field <file> <field> [indent]
#     返字段 raw value(strip 引号),未找到 → 返空 string,return 0
#   require_yaml_field <file> <field> [indent]
#     extract + 校验非空/非 null/非空 quote;有值 print + return 0;
#     无值 stderr 报错 + return 1

# 解析 frontmatter(第一个 --- 到第二个 --- 之间)取指定字段 value
# Args:
#   $1 = file path(必填)
#   $2 = field name(必填)
#   $3 = indent prefix(可选,默认空)— 顶级 = "", workspace/source_repo_identity 子段 = "  "(2 空格)
# Returns: stdout = field value(strip 引号);未找到则空 string
# Exit: 总 0(调用方靠 -z 判空)
extract_yaml_field() {
    local file="$1"
    local field="$2"
    local indent="${3:-}"
    # 取 frontmatter(第一个 ---)到第二个 --- 之间);grep -E 不匹配时不杀脚本
    # F4 修(round 1):去尾随空白 + strip inline comment(# 起始,空白前 OR 行首)→ 然后 strip 引号
    awk '/^---$/{if(++c==1) next; if(c==2) exit} c==1' "$file" \
        | { grep -E "^${indent}${field}:[[:space:]]" || true; } \
        | head -1 \
        | sed -E "s/^${indent}${field}:[[:space:]]*//" \
        | sed -E 's/[[:space:]]+#[[:space:]].*$//' \
        | sed -E 's/[[:space:]]+$//' \
        | sed 's/^"\(.*\)"$/\1/' \
        | sed "s/^'\(.*\)'$/\1/" \
        | sed -E 's/[[:space:]]+$//'
}

# extract + 严格校验非空;fail-closed contract
# Args 同 extract_yaml_field
# Returns: stdout = field value(若有值);return 1 + stderr 报错(若无值)
require_yaml_field() {
    local file="$1"
    local field="$2"
    local indent="${3:-}"
    local val
    val=$(extract_yaml_field "$file" "$field" "$indent")
    if [[ -z "$val" || "$val" == "null" || "$val" == '""' || "$val" == "''" ]]; then
        echo "ERR: $file frontmatter '${indent}${field}' 缺/空/null;补真值再跑" >&2
        return 1
    fi
    printf '%s' "$val"
    return 0
}
