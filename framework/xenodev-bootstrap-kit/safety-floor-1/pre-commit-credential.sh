#!/usr/bin/env bash
# pre-commit-credential.sh — git pre-commit hook 调用 scan-credentials.sh on staged files
# per ideababy_stroller framework/SHARED-CONTRACT.md §1 第 1 件
#
# 装机:
#   ln -s ../../.claude/safety-floor/credential-isolation/pre-commit-credential.sh .git/hooks/pre-commit
# 或在 lefthook.yml 注册:
#   pre-commit:
#     commands:
#       credential-scan:
#         run: bash .claude/safety-floor/credential-isolation/pre-commit-credential.sh

set -euo pipefail

# 注:本 hook 内嵌 staged-blob 扫描逻辑,不依赖 sibling scan-credentials.sh
# (旧版本有 SCAN_SCRIPT path resolution,但通过 git symlink 调起时 BASH_SOURCE
#  指向 .git/hooks/pre-commit → 找不到 sibling scan-credentials.sh。
#  既然 hook 自身已含完整扫描逻辑,删 SCAN_SCRIPT 死引用。)

# 取 staged files(每 commit 跑)— NUL-delimited 防文件名含空格 / 换行
# codex review (B2.2 Block A.5 finding #2 fix):
# - 旧实现读 working tree 的 $file → 攻击者可 stage prod:// 后清 working tree 绕过
# - 新实现读 staged blob (`git show :$file`)→ 真审 index 内容,与 commit 落地一致

# 检测:staged file 名匹配 production env / secrets/production / staged blob 含 prod://
FOUND=0
MATCHED=()

# B2.2 Block A.6 fix(与 scan-credentials.sh 同步):
# SSOT 文档 + Safety Floor 件 1 自身组件含 prod:// 字面串作模式定义,非真凭据
declare -a SKIP_BASENAMES=(
    "scan-credentials.sh"
    "pre-commit-credential.sh"
    "context-loader-filter.md"
    "README.md"
    "README.md.template"
    "AGENTS.md"
    "CLAUDE.md"
    "SHARED-CONTRACT.md"
)

# 用 process substitution + git -z 的 NUL-delimited 流;read -d '' 期望每条以 NUL 终止
# git diff --cached -z 用 NUL 分隔(每条后跟 NUL),read -d '' 正确
while IFS= read -r -d '' file; do
    [[ -z "$file" ]] && continue
    base="$(basename "$file")"
    # filename pattern(纯文件名判定 — 用 staged path,不读 working tree)
    case "$base" in
        .env.production|.env.production.*|.env.prod|.env.prod.*|.env.local)
            FOUND=1
            MATCHED+=("$file (staged: production env file)")
            ;;
    esac
    # path pattern(staged path)
    case "$file" in
        secrets/production/*|secrets/prod/*)
            FOUND=1
            MATCHED+=("$file (staged: secrets/production/ path)")
            ;;
    esac
    # skip SSOT 文档 + 件 1 自身的 prod:// 内容检查(只跳第 3 项,前两项 filename / path 仍生效)
    skip_content=0
    for sk in "${SKIP_BASENAMES[@]}"; do
        if [[ "$base" == "$sk" ]]; then
            skip_content=1
            break
        fi
    done
    # test-fixtures/ 下的 .fake 也跳
    if [[ "$file" == *.fake ]] || [[ "$file" == *test-fixtures* ]]; then
        skip_content=1
    fi
    [[ $skip_content -eq 1 ]] && continue
    # 文件内含 prod://(读 staged blob;不读 working tree — 防 add 后 clean 绕过)
    # git show ":$file" 输出 staged blob 内容;grep -I 跳过 binary;|| true 防 grep 不匹配 + set -e 杀
    if { git show ":$file" 2>/dev/null | grep -I -q 'prod://'; } 2>/dev/null; then
        FOUND=1
        MATCHED+=("$file (staged blob: contains prod:// connection string)")
    fi
done < <(git diff --cached --name-only --diff-filter=ACMR -z 2>/dev/null)

if [[ ${#MATCHED[@]} -eq 0 && $FOUND -eq 0 ]]; then
    # 无 staged files 或全干净 — 跳过(成功路径)
    :
fi

if [[ "$FOUND" == 1 ]]; then
    echo "ERROR: production credentials detected in staged files (Safety Floor 件 1)" >&2
    echo "" >&2
    for entry in "${MATCHED[@]}"; do
        echo "  - $entry" >&2
    done
    echo "" >&2
    echo "Commit BLOCKED. Action:" >&2
    echo "  1. git restore --staged <file>  # unstage 后处理" >&2
    echo "  2. 加到 .gitignore + 不 commit" >&2
    echo "  3. 若是 test fixture,重命名加 .fake 后缀" >&2
    exit 1
fi

# 通过
exit 0
