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

# === 模式 1: remote 模式(若 expected_remote_url 非空)===
if [[ -n "$EXPECTED_REMOTE" ]]; then
    if [[ -d "$SOURCE_REPO/.git" ]]; then
        ACTUAL_REMOTE="$(cd "$SOURCE_REPO" && git config remote.origin.url 2>/dev/null || echo "")"
        # normalize:strip protocol prefix + trailing .git
        normalize() {
            local url="$1"
            # 移除 git@host: 或 https://host/ prefix
            url="${url#git@*:}"
            url="${url#http://*/}"
            url="${url#https://*/}"
            url="${url#ssh://*/}"
            # 移除 trailing .git
            url="${url%.git}"
            echo "$url"
        }
        N_ACTUAL="$(normalize "$ACTUAL_REMOTE")"
        N_EXPECTED="$(normalize "$EXPECTED_REMOTE")"
        if [[ -n "$N_ACTUAL" && "$N_ACTUAL" == "$N_EXPECTED" ]]; then
            exit 0  # remote 模式 PASS
        else
            REASONS+=("remote 模式 FAIL: actual=$ACTUAL_REMOTE (norm: $N_ACTUAL) vs expected=$EXPECTED_REMOTE (norm: $N_EXPECTED)")
        fi
    else
        REASONS+=("remote 模式 N/A: source_repo/.git not found")
    fi
fi

# === 模式 2: no-remote 模式(若 repo_marker 非空)===
if [[ -n "$REPO_MARKER" ]]; then
    CLAUDE_FILE="$SOURCE_REPO/CLAUDE.md"
    if [[ -f "$CLAUDE_FILE" ]]; then
        ACTUAL_MARKER="$(head -c 30 "$CLAUDE_FILE")"
        if echo "$ACTUAL_MARKER" | grep -qF "$REPO_MARKER"; then
            exit 0  # no-remote 模式 PASS
        else
            REASONS+=("no-remote 模式 FAIL: CLAUDE.md L1 head -c 30 = '$ACTUAL_MARKER' does not contain '$REPO_MARKER'")
        fi
    else
        REASONS+=("no-remote 模式 N/A: CLAUDE.md not found at $CLAUDE_FILE")
    fi
fi

# === 模式 3: hash-only 模式(若 git_common_dir_hash 非空)===
if [[ -n "$GIT_HASH" ]]; then
    GIT_HEAD="$SOURCE_REPO/.git/HEAD"
    GIT_CONFIG="$SOURCE_REPO/.git/config"
    if [[ -f "$GIT_HEAD" && -f "$GIT_CONFIG" ]]; then
        ACTUAL_HASH="$(cat "$GIT_HEAD" "$GIT_CONFIG" | shasum -a 256 | head -c 16)"
        if [[ "$ACTUAL_HASH" == "$GIT_HASH" ]]; then
            exit 0  # hash-only 模式 PASS
        else
            REASONS+=("hash-only 模式 FAIL: actual=$ACTUAL_HASH vs expected=$GIT_HASH")
        fi
    else
        REASONS+=("hash-only 模式 N/A: .git/HEAD or .git/config not found")
    fi
fi

# === 所有模式都没 PASS ===
echo "FAIL · §6.2.1 约束 3 (repo identity check, all 3 modes failed or N/A):" >&2
for r in "${REASONS[@]}"; do
    echo "  - $r" >&2
done
echo "  source_repo: $SOURCE_REPO" >&2
echo "  问题:source_repo 与 hand-off 包预期身份不符(IDS 副本 / test clone / 误移动)" >&2

# 若 3 个 expected 字段全空 → 无 ground truth,也算 FAIL(per §3.1 normative)
if [[ -z "$EXPECTED_REMOTE" && -z "$REPO_MARKER" && -z "$GIT_HASH" ]]; then
    echo "  ⚠ all 3 expected fields empty — no ground truth to compare against" >&2
fi

exit 1
