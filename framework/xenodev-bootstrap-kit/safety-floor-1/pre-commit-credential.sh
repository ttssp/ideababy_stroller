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

# B2.2 Block A.7 codex round 4 finding #1 fix:
# 旧 SKIP_BASENAMES(基名)误 skip docs/README.md;旧 SKIP_PATH_SUFFIXES suffix 通配
# 仍误 skip vendor/lib/AGENTS.md。新 SKIP_PATHS:**精确仓根相对路径**(== 比对)。
# git diff --cached --name-only 输出本就是 repo-root-relative,直接精确匹配即可。
declare -a SKIP_PATHS=(
    "framework/xenodev-bootstrap-kit/safety-floor-1/scan-credentials.sh"
    "framework/xenodev-bootstrap-kit/safety-floor-1/pre-commit-credential.sh"
    "framework/xenodev-bootstrap-kit/safety-floor-1/context-loader-filter.md"
    "framework/xenodev-bootstrap-kit/safety-floor-1/README.md"
    "framework/xenodev-bootstrap-kit/AGENTS.md"
    "framework/xenodev-bootstrap-kit/CLAUDE.md"
    "framework/xenodev-bootstrap-kit/README.md.template"
    "framework/SHARED-CONTRACT.md"
    "framework/AUTODEV-PIPE-SYNC-PROPOSAL.md"
    "AGENTS.md"
    "CLAUDE.md"
    ".claude/safety-floor/credential-isolation/scan-credentials.sh"
    ".claude/safety-floor/credential-isolation/pre-commit-credential.sh"
    ".claude/safety-floor/credential-isolation/context-loader-filter.md"
    ".claude/safety-floor/credential-isolation/README.md"
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
    # skip 白名单(精确仓根相对路径;前两项 filename / path 仍生效,只跳第 3 项内容扫描)
    skip_content=0
    for p in "${SKIP_PATHS[@]}"; do
        if [[ "$file" == "$p" ]]; then
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
