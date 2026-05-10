#!/usr/bin/env bash
# extract.sh — 从 hand-off 包 / hand-back 包 frontmatter 提取 workspace 块
# per ideababy_stroller framework/SHARED-CONTRACT.md §6.2
#
# Usage: extract.sh <handoff-or-handback-file.md>
#   stdout: workspace 块的 YAML 内容(只 workspace: 段)
#   exit 0 if extracted; exit 1 if no workspace block found

set -euo pipefail

FILE="${1:-}"

if [[ -z "$FILE" ]]; then
    echo "Usage: extract.sh <file.md>" >&2
    exit 2
fi

if [[ ! -f "$FILE" ]]; then
    echo "ERROR: file not found: $FILE" >&2
    exit 2
fi

# 用 awk 提取 frontmatter 中的 workspace 块
# - 找第一个 ^---$
# - 在第二个 ^---$ 前结束
# - 中间找 ^workspace:$ 起,后续连续缩进行(以空格开头)
awk '
BEGIN { in_fm = 0; in_ws = 0; ws_lines = 0 }
/^---$/ {
    if (in_fm == 0) { in_fm = 1; next }
    else { exit }
}
in_fm == 1 {
    if (/^workspace:[[:space:]]*$/) {
        in_ws = 1
        print
        ws_lines++
        next
    }
    if (in_ws == 1) {
        if (/^[a-zA-Z]/) { in_ws = 0 }  # 下一个顶级 key,workspace 段结束
        else { print; ws_lines++; next }
    }
}
END {
    if (ws_lines == 0) {
        print "ERROR: no workspace: block found in frontmatter" > "/dev/stderr"
        exit 1
    }
}
' "$FILE"
