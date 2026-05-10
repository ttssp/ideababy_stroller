#!/usr/bin/env bash
# check-3-repo-identity.sh — §6.2.1 约束 3:repo identity check(三模式)
# per ideababy_stroller framework/SHARED-CONTRACT.md §6.2.1 约束 3 + §3.1
#
# Usage: check-3-repo-identity.sh <source_repo> <expected_remote_url> <repo_marker> <git_common_dir_hash>
#
# 三模式比对(任一 PASS 即满足约束 3):
# - remote 模式:有 git remote → git config remote.origin.url == expected_remote_url
# - no-remote 模式:无 git remote 或 expected 空 → head -c 30 CLAUDE.md 含 repo_marker
# - hash-only 模式:operator 显式开启(git_common_dir_hash 非空)→ sha256 比对
#
# exit 0 if any mode PASS
# exit 1 if all modes FAIL

set -euo pipefail

SOURCE_REPO="${1:-}"
EXPECTED_REMOTE="${2:-}"
REPO_MARKER="${3:-}"
GIT_HASH="${4:-}"

if [[ -z "$SOURCE_REPO" ]]; then
    echo "Usage: check-3-repo-identity.sh <source_repo> <expected_remote_url> <repo_marker> <git_common_dir_hash>" >&2
    exit 2
fi

if [[ ! -d "$SOURCE_REPO" ]]; then
    echo "FAIL · §6.2.1 约束 3: source_repo not a directory: $SOURCE_REPO" >&2
    exit 1
fi

REASONS=()

# normalize 函数(remote 模式比对前用):统一为 host[:port]/path 形式,host 必须保留比对
# codex review B2.2 Block A.5 finding #3 fix(host 比对)
normalize_remote() {
    local url="$1"
    # 1. 剥 scp-like 形式 user@host:path → host/path
    if [[ "$url" =~ ^[^/]+@[^:/]+:[^/].*$ ]]; then
        local user_host="${url%%:*}"
        local host="${user_host#*@}"
        local path="${url#*:}"
        url="${host}/${path}"
    fi
    # 2. 剥 URL 形式 scheme://[user@]host[:port]/path → host[:port]/path
    if [[ "$url" =~ ^[a-zA-Z][a-zA-Z0-9+.-]*:// ]]; then
        url="${url#*://}"
        url="${url#*@}"
    fi
    # 3. 删 trailing .git + 末尾 /
    url="${url%.git}"
    url="${url%/}"
    # 4. 转小写
    url="$(printf '%s' "$url" | tr '[:upper:]' '[:lower:]')"
    printf '%s' "$url"
}

# === 优先级链(codex round 3 finding #2 fix · fail-closed)===
#
# 旧版:三模式 OR 关系,任一 PASS 即满足。漏洞:expected_remote_url 非空但 actual remote 不同时,
# 仍能 fall through 到 no-remote 模式 + repo_marker(只要 marker 也匹配)→ 攻击者只要保留前 30 字
# CLAUDE.md header 就能冒充。
#
# 新版:优先级 + fail-closed
# - 若 EXPECTED_REMOTE 非空 → **必须** remote 模式 PASS(无 fall through)
# - 若 EXPECTED_REMOTE 空 + REPO_MARKER 非空 → no-remote 模式;且要求 source_repo 真无 origin remote
# - 若上述都空 + GIT_HASH 非空 → hash-only 模式
# - 三字段全空 → FAIL(无 ground truth)

# === 模式 1: remote 模式(EXPECTED_REMOTE 非空时锁定本模式,fail-closed)===
if [[ -n "$EXPECTED_REMOTE" ]]; then
    if [[ ! -d "$SOURCE_REPO/.git" ]]; then
        echo "FAIL · §6.2.1 约束 3 (remote 模式锁定 · source_repo/.git not found): $SOURCE_REPO" >&2
        exit 1
    fi
    ACTUAL_REMOTE="$(cd "$SOURCE_REPO" && git config remote.origin.url 2>/dev/null || echo "")"
    if [[ -z "$ACTUAL_REMOTE" ]]; then
        echo "FAIL · §6.2.1 约束 3 (remote 模式锁定 · source_repo 无 origin remote 但 expected_remote_url 非空)" >&2
        echo "  expected: $EXPECTED_REMOTE" >&2
        echo "  hint:若本仓真无 remote,producer 应在 hand-off 包写空 expected_remote_url + 走 no-remote 模式" >&2
        exit 1
    fi
    N_ACTUAL="$(normalize_remote "$ACTUAL_REMOTE")"
    N_EXPECTED="$(normalize_remote "$EXPECTED_REMOTE")"
    if [[ "$N_ACTUAL" == "$N_EXPECTED" ]]; then
        exit 0  # remote 模式 PASS
    fi
    echo "FAIL · §6.2.1 约束 3 (remote 模式锁定 mismatch · 不允许 fall through)" >&2
    echo "  actual:   $ACTUAL_REMOTE (norm: $N_ACTUAL)" >&2
    echo "  expected: $EXPECTED_REMOTE (norm: $N_EXPECTED)" >&2
    echo "  问题:source_repo 的 origin remote 与 hand-off 包预期不符(IDS 副本 / fork / 误移动)" >&2
    exit 1
fi

# === 模式 2: no-remote 模式(EXPECTED_REMOTE 空 + REPO_MARKER 非空)===
# 要求:source_repo 也真无 origin remote,防 "有 remote 但 producer 故意填空 expected" 的 downgrade
if [[ -n "$REPO_MARKER" ]]; then
    # B2.2 Block A.6 fix:downgrade defense
    if [[ -d "$SOURCE_REPO/.git" ]]; then
        ACTUAL_REMOTE="$(cd "$SOURCE_REPO" && git config remote.origin.url 2>/dev/null || echo "")"
        if [[ -n "$ACTUAL_REMOTE" ]]; then
            echo "FAIL · §6.2.1 约束 3 (no-remote 模式 downgrade · source_repo 有 origin remote 但 expected 留空)" >&2
            echo "  actual remote: $ACTUAL_REMOTE" >&2
            echo "  hint:producer 应填 expected_remote_url 并走 remote 模式" >&2
            exit 1
        fi
    fi
    # B2.2 Block A.7 codex round 4 finding #4 fix:marker 强度校验
    # §3.1 normative 写 "marker 必含 'Idea Incubator'" — 之前实装漏强制
    # 攻击场景:repo_marker = "I"(1 字符),CLAUDE.md 含字母 I → PASS,绕过身份校验
    if [[ ${#REPO_MARKER} -lt 10 ]]; then
        echo "FAIL · §6.2.1 约束 3 (no-remote 模式 · marker 太短 < 10 字符,可能被简单字符冒充)" >&2
        echo "  repo_marker: '$REPO_MARKER' (长度 ${#REPO_MARKER})" >&2
        echo "  hint:per §3.1,marker 必含 'Idea Incubator' 完整字串(本仓固定 prefix)" >&2
        exit 1
    fi
    if [[ "$REPO_MARKER" != *"Idea Incubator"* ]]; then
        echo "FAIL · §6.2.1 约束 3 (no-remote 模式 · marker 不含必需 'Idea Incubator' 字串)" >&2
        echo "  repo_marker: '$REPO_MARKER'" >&2
        echo "  hint:per §3.1 normative,marker 必含 'Idea Incubator'(IDS CLAUDE.md L1 永久标识)" >&2
        exit 1
    fi
    CLAUDE_FILE="$SOURCE_REPO/CLAUDE.md"
    if [[ ! -f "$CLAUDE_FILE" ]]; then
        echo "FAIL · §6.2.1 约束 3 (no-remote 模式 · CLAUDE.md not found): $CLAUDE_FILE" >&2
        exit 1
    fi
    ACTUAL_MARKER="$(head -c 30 "$CLAUDE_FILE")"
    if echo "$ACTUAL_MARKER" | grep -qF "$REPO_MARKER"; then
        exit 0  # no-remote 模式 PASS
    fi
    echo "FAIL · §6.2.1 约束 3 (no-remote 模式 marker mismatch)" >&2
    echo "  actual:   '$ACTUAL_MARKER'" >&2
    echo "  expected to contain: '$REPO_MARKER'" >&2
    exit 1
fi

# === 模式 3: hash-only 模式(EXPECTED_REMOTE + REPO_MARKER 都空 + GIT_HASH 非空)===
if [[ -n "$GIT_HASH" ]]; then
    GIT_HEAD="$SOURCE_REPO/.git/HEAD"
    GIT_CONFIG="$SOURCE_REPO/.git/config"
    if [[ ! -f "$GIT_HEAD" || ! -f "$GIT_CONFIG" ]]; then
        echo "FAIL · §6.2.1 约束 3 (hash-only 模式 · .git/HEAD or .git/config not found)" >&2
        exit 1
    fi
    ACTUAL_HASH="$(cat "$GIT_HEAD" "$GIT_CONFIG" | shasum -a 256 | head -c 16)"
    if [[ "$ACTUAL_HASH" == "$GIT_HASH" ]]; then
        exit 0  # hash-only 模式 PASS
    fi
    echo "FAIL · §6.2.1 约束 3 (hash-only 模式 hash mismatch)" >&2
    echo "  actual:   $ACTUAL_HASH" >&2
    echo "  expected: $GIT_HASH" >&2
    exit 1
fi

# === 三字段全空 → 无 ground truth,FAIL(per §3.1 normative)===
echo "FAIL · §6.2.1 约束 3 · 三字段(expected_remote_url / repo_marker / git_common_dir_hash)全空,无 ground truth 可比对" >&2
echo "  source_repo: $SOURCE_REPO" >&2
echo "  hint:hand-off 包 frontmatter source_repo_identity 块至少需 1 字段非空" >&2
exit 1
