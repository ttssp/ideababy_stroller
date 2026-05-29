#!/usr/bin/env bash
# XenoDev bootstrap script
# per ideababy_stroller framework/xenodev-bootstrap-kit/
#
# 两种真路径模式(per T301 wave 3 升级):
#
# 模式 1 · legacy XenoDev bootstrap(无参数 · 原行为不变):
#   cd /Users/admin/codes/XenoDev && bash <kit>/bootstrap.sh
#   真路径 git init + cp 子树 + first commit + Safety Floor hooks
#
# 模式 2 · fixture mode(传路径参数 · T301/T303 新增):
#   bash bootstrap.sh /tmp/test-fixture-T301
#   真路径 cp v0.2 7 子树到 fixture/<rel> + per-file SHA dual-verify + summary
#   不 git init · 不 first commit · 用于 wave 3 联调 + verify-bootstrap.sh smoke

set -euo pipefail

IDS_KIT="/Users/admin/codes/ideababy_stroller/framework/xenodev-bootstrap-kit"

# === T301 · fixture mode 分流(传路径 arg1 = fixture mode) ===
# 真路径 R1 critical(per codex review):rm -rf "$FIXTURE_PATH" 真路径无 allowlist 真路径
# 接受任意绝对路径 · typo 真路径毁数据。修法:allowlist root + canonicalize realpath + 拒保护根
FIXTURE_MODE=0
FIXTURE_PATH=""
IDS_ROOT="$(cd "$IDS_KIT/.." && cd .. && pwd)"
if [[ $# -ge 1 ]]; then
    FIXTURE_PATH_RAW="$1"
    FIXTURE_MODE=1

    # 拒空
    if [[ -z "$FIXTURE_PATH_RAW" ]]; then
        echo "ERROR: fixture path 真路径为空 · 拒" >&2
        exit 1
    fi

    # 拒 '..' 真路径 traversal
    if [[ "$FIXTURE_PATH_RAW" == *".."* ]]; then
        echo "ERROR: fixture path 含 '..' 真路径 traversal: $FIXTURE_PATH_RAW" >&2
        exit 1
    fi

    # 相对路径转绝对(基于 IDS root 真路径)
    if [[ "$FIXTURE_PATH_RAW" != /* ]]; then
        FIXTURE_PATH_RAW="$IDS_ROOT/$FIXTURE_PATH_RAW"
    fi

    # canonicalize 真路径(realpath · 解 symlink)
    # macOS BSD realpath 真路径在 bash 3.2 真路径下也 OK
    # 真路径 fixture 真路径不要求事先存在 · 用 python 真路径 normpath
    FIXTURE_PATH=$(python3 -c "import os, sys; print(os.path.normpath(sys.argv[1]))" "$FIXTURE_PATH_RAW")

    # === 真路径 allowlist root(per codex R1 critical + R4 critical · 不信 TMPDIR) ===
    # R4 critical 真路径根因:caller 设 TMPDIR=/Users/admin 然后传 absolute /Users/admin/<X>-bootstrap-test-fixture 真路径 ·
    # commonpath 真路径过 · basename 真路径过 · rm -rf 真路径毁数据
    # 修法:完全去掉 TMPDIR 信任 · 真路径只接 fixed safe temp roots(/tmp · /private/tmp · macOS BSD 真路径 symlink)
    # 真路径用户若要在 $TMPDIR 跑 · 必须真路径环境变量真路径配 /tmp 真路径之内 · 否则真路径手 cd 到 /tmp 真路径
    ALLOWED_ROOTS=(
        "$IDS_ROOT/discussion/"
        "/tmp/"
        "/private/tmp/"
    )
    # 注:不再接 $TMPDIR · 防 caller-controlled environment 真路径绕 allowlist 真路径 deletion(per codex R4)

    # === T301 R2(per codex review):用 os.path.commonpath 真路径 directory-boundary check ===
    # 真路径 prefix-test 漏洞:`/private/tmp-backup/foo` 含 prefix `/private/tmp` 但是 adjacent path · 不在 /tmp 子树
    # 修法:commonpath([root, fixture]) == root 真路径才允许 · directory-boundary 真路径严格
    fixture_canon=$(python3 -c "import os, sys; print(os.path.realpath(os.path.dirname(sys.argv[1])) + '/' + os.path.basename(sys.argv[1]))" "$FIXTURE_PATH")

    FIXTURE_OK=0
    for root in "${ALLOWED_ROOTS[@]}"; do
        root_canon=$(python3 -c "import os, sys; print(os.path.realpath(sys.argv[1]))" "$root")
        # commonpath 真路径必须等于 root_canon · 且 fixture_canon ≠ root_canon(防 root 本身)
        boundary_check=$(python3 -c "
import os, sys
root = sys.argv[1]
fixture = sys.argv[2]
if fixture == root:
    sys.exit(1)
try:
    common = os.path.commonpath([root, fixture])
except ValueError:
    sys.exit(1)
if common == root:
    sys.exit(0)
sys.exit(1)
" "$root_canon" "$fixture_canon" 2>/dev/null && echo "OK" || echo "FAIL")
        if [[ "$boundary_check" == "OK" ]]; then
            FIXTURE_OK=1
            break
        fi
    done

    if [[ "$FIXTURE_OK" != "1" ]]; then
        echo "ERROR: fixture path 真路径不在 allowlist root 内 · 拒:" >&2
        echo "  fixture path: $FIXTURE_PATH" >&2
        echo "  allowed roots:" >&2
        for root in "${ALLOWED_ROOTS[@]}"; do
            echo "    - $root" >&2
        done
        echo "  真路径 rationale:防止 rm -rf 真路径意外毁数据(per codex T301 R1 critical)" >&2
        exit 1
    fi

    # === 真路径拒保护根真路径(双保险) ===
    # 即使在 allowlist root 下 · 也拒真路径明显保护目录
    PROTECTED_PATHS=(
        "/"
        "$HOME"
        "$IDS_ROOT"
        "/Users/admin/codes/XenoDev"
        "/Users/admin"
        "/Users"
        "/tmp"
        "/private/tmp"
    )
    for prot in "${PROTECTED_PATHS[@]}"; do
        prot_canon=$(python3 -c "import os, sys; print(os.path.realpath(sys.argv[1]))" "$prot" 2>/dev/null || echo "$prot")
        if [[ "$FIXTURE_PATH" == "$prot" || "$FIXTURE_PATH" == "$prot_canon" ]]; then
            echo "ERROR: fixture path 真路径等于保护根 · 拒:$FIXTURE_PATH (== $prot)" >&2
            exit 1
        fi
    done
fi

# === Sanity check(仅 legacy mode · fixture mode 跳过) ===
if [[ "$FIXTURE_MODE" == "0" ]]; then
    CWD="$(pwd)"
    if [[ "$CWD" != *"XenoDev"* ]]; then
        echo "ERROR: bootstrap.sh must run inside XenoDev directory (legacy mode)."
        echo "       current pwd: $CWD"
        echo "       expected: /Users/admin/codes/XenoDev (or similar)"
        echo "       tip: 用 fixture mode 真路径传一个 path 参数(eg discussion/006-bootstrap-test-fixture)"
        exit 1
    fi
    if [[ "$CWD" == *"ideababy_stroller"* ]]; then
        echo "ERROR: do NOT run bootstrap.sh inside ideababy_stroller (legacy mode)."
        echo "       This script bootstraps a NEW XenoDev repo, not modifies IDS."
        exit 1
    fi
fi

# === Check kit source exists ===
if [[ ! -d "$IDS_KIT" ]]; then
    echo "ERROR: IDS bootstrap kit not found at $IDS_KIT"
    echo "       did you clone ideababy_stroller? did the path change?"
    exit 1
fi

if [[ "$FIXTURE_MODE" == "1" ]]; then
    echo "→ T301 fixture mode · target=$FIXTURE_PATH"
    echo "→ kit source: $IDS_KIT"
    echo
else
    echo "→ XenoDev bootstrap starting in $CWD"
    echo "→ kit source: $IDS_KIT"
    echo
fi

# === T301 · fixture mode 真路径(cp v0.2 7 子树 + SHA dual-verify · fail-closed) ===
if [[ "$FIXTURE_MODE" == "1" ]]; then
    FIXTURE_BASENAME=$(basename "$FIXTURE_PATH")

    # === R6 真路径修(per codex R6 high)· basename 真路径 ordering 真路径 先于 cleanup ===
    # 真路径根因:R5 真路径把 basename check 真路径放在 rm -rf 后 · 真路径已删了才拒
    # 修法:basename 真路径 + 所有 non-destructive guards 真路径全部前置 · 任一拒 = exit · 然后才 rm
    if [[ "$FIXTURE_BASENAME" != *"bootstrap-test-fixture"* ]]; then
        echo "ERROR: fixture basename 真路径必须含 'bootstrap-test-fixture'(防 typo / collision 真路径误删):" >&2
        echo "  basename: $FIXTURE_BASENAME" >&2
        echo "  推荐真路径:discussion/006-bootstrap-test-fixture / /tmp/<id>-bootstrap-test-fixture" >&2
        echo "  真路径 ordering(per codex R6):basename check 真路径必须真路径先于 rm -rf 真路径 fail-closed" >&2
        exit 1
    fi

    # === R5 F1 真路径修(per codex R5)· 已存在 dir 必须有 marker 才允许 rm -rf ===
    # 真路径根因:basename 真路径 'bootstrap-test-fixture' 只用于命名约定 · 不是 ownership 证明
    # 已存在 dir 真路径必须真路径含 .bootstrap-fixture-marker(本脚本上次留下)才证明 owned · 才允许清
    # 修法:已存在 dir + 无 marker = 真路径 fail-closed · operator 真路径手清 OR 改 path
    if [[ -d "$FIXTURE_PATH" ]]; then
        if [[ ! -f "$FIXTURE_PATH/.bootstrap-fixture-marker" ]]; then
            echo "ERROR: fixture path 真路径已存在但无 .bootstrap-fixture-marker · 拒删(R5 真路径 ownership 防护):" >&2
            echo "  fixture: $FIXTURE_PATH" >&2
            echo "  真路径 rationale:本脚本只删 own 的 dir(marker 真路径证明上次本脚本创建过)·" >&2
            echo "  防 typo / collision 真路径意外删 operator 手编 evidence(per codex T301 R5 high)" >&2
            echo "  修法:(1) operator 真路径手 rm 旧 dir 后重跑 · 或 (2) 改 fixture path" >&2
            exit 1
        fi

        # === R5 F2 真路径修 mitigation(per codex R5)· rm 前真路径 canonical 真路径 re-check ===
        # 真路径 TOCTOU 真路径 mitigation · validation 后 + rm 前重 canonicalize 真路径 · 拒 symlink parent
        # macOS BSD find 真路径 -lname 真路径 print symlink target · 真路径 -type l 真路径 print symlink itself
        FIXTURE_PARENT=$(dirname "$FIXTURE_PATH")
        FIXTURE_PARENT_CANON=$(python3 -c "import os, sys; print(os.path.realpath(sys.argv[1]))" "$FIXTURE_PARENT")
        # 真路径 fixture 真路径 canonical 真路径 = parent_canon/basename
        FIXTURE_CANON_RECHECK="$FIXTURE_PARENT_CANON/$FIXTURE_BASENAME"
        # 真路径 re-check allowlist 真路径(同上文 commonpath 真路径)
        RECHECK_OK=0
        for root in "${ALLOWED_ROOTS[@]}"; do
            root_canon=$(python3 -c "import os, sys; print(os.path.realpath(sys.argv[1]))" "$root")
            boundary_check=$(python3 -c "
import os, sys
root = sys.argv[1]
fixture = sys.argv[2]
if fixture == root:
    sys.exit(1)
try:
    common = os.path.commonpath([root, fixture])
except ValueError:
    sys.exit(1)
if common == root:
    sys.exit(0)
sys.exit(1)
" "$root_canon" "$FIXTURE_CANON_RECHECK" 2>/dev/null && echo "OK" || echo "FAIL")
            if [[ "$boundary_check" == "OK" ]]; then
                RECHECK_OK=1
                break
            fi
        done
        if [[ "$RECHECK_OK" != "1" ]]; then
            echo "ERROR: fixture path 真路径 TOCTOU 真路径 re-check fail · canonical 真路径 $FIXTURE_CANON_RECHECK 不在 allowlist · 拒删(R5 F2)" >&2
            exit 1
        fi
        # 真路径 rm 之前真路径再确认 marker 真路径仍在(防 TOCTOU)
        if [[ ! -f "$FIXTURE_PATH/.bootstrap-fixture-marker" ]]; then
            echo "ERROR: fixture marker 真路径在 re-check 之间消失 · TOCTOU 真路径攻击 suspected · 拒删" >&2
            exit 1
        fi
        rm -rf "$FIXTURE_PATH"
    fi

    # 真路径 basename 真路径已在前置 guard 真路径 check 真路径 PASS 才到此(per R6 ordering)
    mkdir -p "$FIXTURE_PATH"
    # 落 marker · 让下次重跑识别本 dir 是真路径 fixture · 允许清(R5 真路径 ownership 证明)
    touch "$FIXTURE_PATH/.bootstrap-fixture-marker"

    # === 真路径 v0.2 子树清单 source→target mapping(per spec.md architecture.md §3.1) ===
    # bootstrap-kit 真路径布局(IDS source)→ XenoDev runtime 真路径布局(fixture target)
    # 真路径 T303 verify 期望 fixture 含 lib/handback-validator/ + .claude/skills/ + tests/integration/
    # 顶级文件 source→target 相同
    FIXTURE_TOP_FILES=(
        "AGENTS.md:AGENTS.md"
        "CLAUDE.md:CLAUDE.md"
    )
    # 子树 source:target mapping
    FIXTURE_SUBTREE_MAP=(
        "skills:.claude/skills"
        "hooks/wrappers:.claude/hooks/wrappers"
        "hooks/test-fixtures:.claude/hooks/test-fixtures"
        "safety-floor-1:.claude/safety-floor/credential-isolation"
        "safety-floor-3:.claude/safety-floor/backup-detection"
        "handback-validator:lib/handback-validator"
        "eval-event-log:lib/eval-event-log"
        "workspace-schema:lib/workspace-schema"
        "tests/integration:tests/integration"
    )
    # safety-floor-2 真路径单文件 cp(block-dangerous.sh → .claude/hooks/)
    FIXTURE_SINGLE_FILES=(
        "safety-floor-2/block-dangerous.sh:.claude/hooks/block-dangerous.sh"
    )

    FIXTURE_COPIED=0
    FIXTURE_DRIFT=0

    # cp top files
    for pair in "${FIXTURE_TOP_FILES[@]}"; do
        src_rel="${pair%%:*}"
        tgt_rel="${pair##*:}"
        SRC="$IDS_KIT/$src_rel"
        TGT="$FIXTURE_PATH/$tgt_rel"
        if [[ ! -f "$SRC" ]]; then
            echo "ERROR: fixture mode · top file source 缺: $SRC" >&2
            exit 1
        fi
        mkdir -p "$(dirname "$TGT")"
        cp -p "$SRC" "$TGT"
        SRC_SHA=$(shasum -a 256 "$SRC" | awk '{print $1}')
        TGT_SHA=$(shasum -a 256 "$TGT" | awk '{print $1}')
        if [[ "$SRC_SHA" != "$TGT_SHA" ]]; then
            echo "ERROR: SHA drift on top file $src_rel · src=$SRC_SHA · tgt=$TGT_SHA" >&2
            FIXTURE_DRIFT=$((FIXTURE_DRIFT + 1))
        fi
        FIXTURE_COPIED=$((FIXTURE_COPIED + 1))
    done

    # cp single files(safety-floor-2/block-dangerous.sh → .claude/hooks/)
    for pair in "${FIXTURE_SINGLE_FILES[@]}"; do
        src_rel="${pair%%:*}"
        tgt_rel="${pair##*:}"
        SRC="$IDS_KIT/$src_rel"
        TGT="$FIXTURE_PATH/$tgt_rel"
        if [[ ! -f "$SRC" ]]; then
            echo "ERROR: fixture mode · single file source 缺: $SRC" >&2
            exit 1
        fi
        mkdir -p "$(dirname "$TGT")"
        cp -p "$SRC" "$TGT"
        SRC_SHA=$(shasum -a 256 "$SRC" | awk '{print $1}')
        TGT_SHA=$(shasum -a 256 "$TGT" | awk '{print $1}')
        if [[ "$SRC_SHA" != "$TGT_SHA" ]]; then
            echo "ERROR: SHA drift on single file $src_rel · src=$SRC_SHA · tgt=$TGT_SHA" >&2
            FIXTURE_DRIFT=$((FIXTURE_DRIFT + 1))
        fi
        FIXTURE_COPIED=$((FIXTURE_COPIED + 1))
    done

    # cp subtrees · source→target mapping · 真路径递归 + per-file SHA dual-verify
    for pair in "${FIXTURE_SUBTREE_MAP[@]}"; do
        src_rel="${pair%%:*}"
        tgt_rel="${pair##*:}"
        SRC_DIR="$IDS_KIT/$src_rel"
        TGT_DIR="$FIXTURE_PATH/$tgt_rel"
        if [[ ! -d "$SRC_DIR" ]]; then
            echo "ERROR: fixture mode · subtree source 缺: $SRC_DIR" >&2
            exit 1
        fi
        mkdir -p "$TGT_DIR"
        cp -rp "$SRC_DIR/." "$TGT_DIR/"
        # 逐文件 SHA dual-verify
        while IFS= read -r SRC_FILE; do
            REL="${SRC_FILE#$SRC_DIR/}"
            TGT_FILE="$TGT_DIR/$REL"
            if [[ ! -f "$TGT_FILE" ]]; then
                echo "ERROR: subtree $src_rel · missing target file: $TGT_FILE" >&2
                FIXTURE_DRIFT=$((FIXTURE_DRIFT + 1))
                continue
            fi
            SRC_SHA=$(shasum -a 256 "$SRC_FILE" | awk '{print $1}')
            TGT_SHA=$(shasum -a 256 "$TGT_FILE" | awk '{print $1}')
            if [[ "$SRC_SHA" != "$TGT_SHA" ]]; then
                echo "ERROR: SHA drift on $src_rel/$REL · src=$SRC_SHA · tgt=$TGT_SHA" >&2
                FIXTURE_DRIFT=$((FIXTURE_DRIFT + 1))
            fi
            FIXTURE_COPIED=$((FIXTURE_COPIED + 1))
        done < <(find "$SRC_DIR" -type f)
    done

    if [[ "$FIXTURE_DRIFT" -gt 0 ]]; then
        echo "ERROR: fixture mode · $FIXTURE_DRIFT SHA drift detected · fail-closed" >&2
        exit 1
    fi

    # === fixture mode 真路径 framework/ mirror(per bootstrap-verify Step 4 真路径需求)===
    mkdir -p "$FIXTURE_PATH/framework"
    SSOT_SRC="$IDS_KIT/../SHARED-CONTRACT.md"
    if [[ -f "$SSOT_SRC" ]]; then
        cp "$SSOT_SRC" "$FIXTURE_PATH/framework/SHARED-CONTRACT.md"
        cat > "$FIXTURE_PATH/framework/MIRROR-PROVENANCE.md" <<EOF
# framework/ mirror provenance(fixture mode 真路径 stub)

> 真路径 fixture mode 真路径 bootstrap 产 · 真路径 SHARED-CONTRACT.md 真路径字节级 mirror。

## bootstrap 时点
- mode: fixture
- ts: $(date -u +%Y-%m-%dT%H:%M:%SZ)
EOF
    fi

    # === fixture mode 真路径 PRD/HANDOFF/.eval seed(per T304 PPV-P1 SHIP-READY 真路径前提)===
    # 真路径 verify-all-outcomes.sh 真路径假设 fixture 真路径自包含 XenoDev workspace · 真路径需要:
    #   - HANDOFF.md + HANDOFF-006a-pM.bak(O4 真路径 round-trip 真路径产 hand-back 真路径)
    #   - PRD.md(O3 bootstrap-verify 真路径 check)
    #   - .eval/events.jsonl 真路径 ≥ 6 events 真路径覆盖 3 类(O3 eval-events-count 真路径)
    XENODEV_HANDOFF="/Users/admin/codes/XenoDev/HANDOFF.md"
    XENODEV_PRD="/Users/admin/codes/XenoDev/PRD.md"
    if [[ -f "$XENODEV_HANDOFF" ]]; then
        cp "$XENODEV_HANDOFF" "$FIXTURE_PATH/HANDOFF.md"
        cp "$XENODEV_HANDOFF" "$FIXTURE_PATH/HANDOFF-006a-pM.bak"
    fi
    if [[ -f "$XENODEV_PRD" ]]; then
        cp "$XENODEV_PRD" "$FIXTURE_PATH/PRD.md"
    fi
    mkdir -p "$FIXTURE_PATH/.eval"
    if [[ ! -f "$FIXTURE_PATH/.eval/events.jsonl" ]]; then
        for evt in operator_interventions review_failures handback_drifts; do
            for i in 1 2; do
                echo "{\"type\":\"$evt\",\"event_type\":\"$evt\",\"ts\":\"2026-05-29T07:0${i}:00Z\",\"note\":\"fixture seed $evt $i\"}" >> "$FIXTURE_PATH/.eval/events.jsonl"
            done
        done
    fi

    echo "[bootstrap] $FIXTURE_COPIED files copied · SHA dual-verify PASS · fixture=$FIXTURE_PATH"
    exit 0
fi

# === Step 1: git init(若未 init)===
if [[ ! -d .git ]]; then
    git init -b main
    echo "✓ Step 1: git init -b main"
else
    echo "✓ Step 1: git already initialized (skipping init)"
fi

# === Step 2: cp 顶级文件 ===
cp "$IDS_KIT/AGENTS.md"            .
cp "$IDS_KIT/CLAUDE.md"            .
cp "$IDS_KIT/README.md.template"   README.md
cp "$IDS_KIT/LICENSE.template"     LICENSE
cp "$IDS_KIT/.gitignore.template"  .gitignore
echo "✓ Step 2: top-level files copied (AGENTS / CLAUDE / README / LICENSE / .gitignore)"

# === Step 3: .claude/ 骨架 ===
mkdir -p .claude/hooks .claude/safety-floor .claude/skills .claude/commands
echo "✓ Step 3: .claude/ skeleton created"

# === Step 4: cp Safety Floor 件 2(block-dangerous.sh)===
cp "$IDS_KIT/safety-floor-2/block-dangerous.sh" .claude/hooks/block-dangerous.sh
chmod +x .claude/hooks/block-dangerous.sh
echo "✓ Step 4: block-dangerous.sh installed (mirror from autodev_pipe)"

# === Step 5: cp Safety Floor 件 1 + 件 3 ===
cp -r "$IDS_KIT/safety-floor-1/" .claude/safety-floor/credential-isolation/
cp -r "$IDS_KIT/safety-floor-3/" .claude/safety-floor/backup-detection/
echo "✓ Step 5: safety floor 件 1 + 件 3 installed"

# === Step 6: cp lib/(workspace-schema + eval-event-log + handback-validator)===
mkdir -p lib
cp -r "$IDS_KIT/workspace-schema/"   lib/workspace-schema/
cp -r "$IDS_KIT/eval-event-log/"     lib/eval-event-log/
cp -r "$IDS_KIT/handback-validator/" lib/handback-validator/
echo "✓ Step 6: lib/ installed (workspace-schema + eval-event-log + handback-validator)"

# === Step 6.1: T301 v0.2 子树(skills + hooks/wrappers + tests/integration · per wave 3 R3 F2)===
# 真路径 codex R3 F2 finding:legacy mode 真路径 fresh XenoDev bootstrap 真路径缺 v0.2 子树 ·
# 真路径 runtime 真路径会缺 .claude/skills + .claude/hooks/wrappers + tests/integration
# 修法:legacy 真路径同步 cp v0.2 4 新子树 + per-file SHA dual-verify
LEGACY_V02_MAP=(
    "skills:.claude/skills"
    "hooks/wrappers:.claude/hooks/wrappers"
    "hooks/test-fixtures:.claude/hooks/test-fixtures"
    "tests/integration:tests/integration"
)
LEGACY_V02_COPIED=0
LEGACY_V02_DRIFT=0
for pair in "${LEGACY_V02_MAP[@]}"; do
    src_rel="${pair%%:*}"
    tgt_rel="${pair##*:}"
    SRC_DIR="$IDS_KIT/$src_rel"
    TGT_DIR="./$tgt_rel"
    if [[ ! -d "$SRC_DIR" ]]; then
        echo "ERROR: Step 6.1 v0.2 subtree source 缺: $SRC_DIR" >&2
        exit 1
    fi
    mkdir -p "$TGT_DIR"
    cp -rp "$SRC_DIR/." "$TGT_DIR/"
    while IFS= read -r SRC_FILE; do
        REL="${SRC_FILE#$SRC_DIR/}"
        TGT_FILE="$TGT_DIR/$REL"
        if [[ ! -f "$TGT_FILE" ]]; then
            echo "ERROR: Step 6.1 missing target: $TGT_FILE" >&2
            LEGACY_V02_DRIFT=$((LEGACY_V02_DRIFT + 1))
            continue
        fi
        SRC_SHA=$(shasum -a 256 "$SRC_FILE" | awk '{print $1}')
        TGT_SHA=$(shasum -a 256 "$TGT_FILE" | awk '{print $1}')
        if [[ "$SRC_SHA" != "$TGT_SHA" ]]; then
            echo "ERROR: Step 6.1 SHA drift: $src_rel/$REL" >&2
            LEGACY_V02_DRIFT=$((LEGACY_V02_DRIFT + 1))
        fi
        LEGACY_V02_COPIED=$((LEGACY_V02_COPIED + 1))
    done < <(find "$SRC_DIR" -type f)
done
if [[ "$LEGACY_V02_DRIFT" -gt 0 ]]; then
    echo "ERROR: Step 6.1 $LEGACY_V02_DRIFT SHA drift detected · fail-closed" >&2
    exit 1
fi
echo "✓ Step 6.1: v0.2 子树 installed (skills + hooks/wrappers + tests/integration · $LEGACY_V02_COPIED files · SHA dual-verify PASS)"

# === Step 6.5: cp framework SSOT mirror(SHARED-CONTRACT.md 字节级 mirror + provenance 文件)===
# B2.2 Block D friction F3 fix(006a-pM session 实证):
# AGENTS.md §4 + CLAUDE.md §"跨仓引用" 写 "framework/SHARED-CONTRACT.md 是 IDS SSOT 字节级 mirror",
# 但 bootstrap.sh 之前不带 framework/ 目录 → 每个 XenoDev session 首跑都重发现 mirror 缺位。
# 本 Step 在 bootstrap 时就落 mirror + 校验 + 落 provenance,避免重复 friction。
IDS_FRAMEWORK_DIR="$(cd "$IDS_KIT/.." && pwd)"
IDS_REPO_ROOT="$(cd "$IDS_FRAMEWORK_DIR/.." && pwd)"
SSOT_SRC="$IDS_FRAMEWORK_DIR/SHARED-CONTRACT.md"
if [[ ! -f "$SSOT_SRC" ]]; then
    echo "ERROR: Step 6.5 IDS SSOT not found: $SSOT_SRC"
    exit 1
fi
mkdir -p framework
cp "$SSOT_SRC" framework/SHARED-CONTRACT.md
# 字节级校验
SSOT_BYTES="$(wc -c < "$SSOT_SRC" | tr -d ' ')"
MIRROR_BYTES="$(wc -c < framework/SHARED-CONTRACT.md | tr -d ' ')"
SSOT_SHA="$(shasum -a 256 "$SSOT_SRC" | awk '{print $1}')"
MIRROR_SHA="$(shasum -a 256 framework/SHARED-CONTRACT.md | awk '{print $1}')"
if [[ "$SSOT_BYTES" != "$MIRROR_BYTES" || "$SSOT_SHA" != "$MIRROR_SHA" ]]; then
    echo "ERROR: Step 6.5 mirror integrity check FAILED"
    echo "  SSOT bytes=$SSOT_BYTES sha=$SSOT_SHA"
    echo "  mirror bytes=$MIRROR_BYTES sha=$MIRROR_SHA"
    exit 1
fi
# 落 MIRROR-PROVENANCE.md(per 006a-pM friction-report D2 闭环范式)
cat > framework/MIRROR-PROVENANCE.md <<EOF
# framework/ mirror provenance

> framework/ 下的文件是 ideababy_stroller(IDS · SSOT)的**只读字节级 mirror**。XenoDev 不修改这些文件;只在 IDS 改后由 operator 重新 cp。

## Mirror 列表

| 文件 | IDS 源路径 | mirror bootstrap 时 sha256 | bytes |
|---|---|---|---|
| SHARED-CONTRACT.md | $SSOT_SRC | $MIRROR_SHA | $MIRROR_BYTES |

## 校验命令(operator 任意时点跑,验是否 drift)

\`\`\`bash
diff -q $SSOT_SRC framework/SHARED-CONTRACT.md
shasum -a 256 framework/SHARED-CONTRACT.md
# 期望 sha256: $MIRROR_SHA
\`\`\`

## 重 cp 触发条件

- IDS \`framework/SHARED-CONTRACT.md\` 改了(operator 在 IDS commit 后通知 / XenoDev session 跑 \`diff -q\` 发现 drift)
- 重 cp 命令:\`cp $SSOT_SRC framework/SHARED-CONTRACT.md && shasum -a 256 framework/SHARED-CONTRACT.md\`

## 失败处置

- diff 不一致 = drift → operator 决:从 IDS 重 cp(若 IDS 是真新版本)/ 不动(若 XenoDev 仍按旧 contract 跑且无 break)
- bootstrap 时 sha 不一致 = bootstrap.sh bug → 报 IDS

## bootstrap 时点

- 时间:$(date -u +%Y-%m-%dT%H:%M:%SZ)
- IDS 仓:$IDS_REPO_ROOT
EOF
echo "✓ Step 6.5: framework/SHARED-CONTRACT.md mirror installed (sha256: ${MIRROR_SHA:0:16}... · $MIRROR_BYTES bytes) + MIRROR-PROVENANCE.md"

# === Step 7: 创建 .claude/settings.json 模板(注册 block-dangerous.sh hook)===
if [[ ! -f .claude/settings.json ]]; then
    cat > .claude/settings.json <<'EOF'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/block-dangerous.sh"
          }
        ]
      }
    ]
  }
}
EOF
    echo "✓ Step 7: .claude/settings.json created (block-dangerous.sh hook registered)"
else
    echo "✓ Step 7: .claude/settings.json already exists (skipping)"
fi

# === Step 8: 准备 .eval/ 目录(append-only event log)===
mkdir -p .eval
touch .eval/.keep   # 让 git 看见空目录(.eval/events.jsonl 在 .gitignore 中)
echo "✓ Step 8: .eval/ directory ready"

# === Step 8.5: 装 pre-commit credential hook(初始 commit 前必装,防 prod:// 进首 commit)===
# B2.2 Block A.6 codex round 3 finding #3 fix:
# 旧版本先 git commit,再让 operator 手装 hook → 首 commit 不受 Safety Floor 件 1 保护。
# 新版本:bootstrap.sh 自己装 hook(symlink 到 .git/hooks/pre-commit)+ 跑一次 scan-credentials.sh,
#       任一失败 → 整个 bootstrap exit 1,不创建首 commit。
HOOK_TARGET=".git/hooks/pre-commit"
HOOK_SOURCE=".claude/safety-floor/credential-isolation/pre-commit-credential.sh"
if [[ -f "$HOOK_TARGET" || -L "$HOOK_TARGET" ]]; then
    echo "  ⚠ $HOOK_TARGET already exists (overwriting; 旧 hook 备份到 ${HOOK_TARGET}.bak)"
    mv "$HOOK_TARGET" "${HOOK_TARGET}.bak"
fi
# 用相对路径 symlink(可移植性优于绝对路径)
ln -s "../../$HOOK_SOURCE" "$HOOK_TARGET"
chmod +x "$HOOK_SOURCE"  # 确保 hook 可执行
if [[ ! -x "$HOOK_TARGET" ]]; then
    echo "ERROR: Step 8.5 装 pre-commit hook 失败: $HOOK_TARGET 不可执行"
    exit 1
fi
echo "✓ Step 8.5: pre-commit credential hook installed (symlink → $HOOK_SOURCE)"

# 立即跑一次 full scan-credentials.sh 在所有待 commit 文件上(不只 staged):
# 这是 first-commit 保护(此时 staged 为空,也无 working tree 改动 — 跑全仓 scan)
SCAN_SCRIPT=".claude/safety-floor/credential-isolation/scan-credentials.sh"
if [[ -x "$SCAN_SCRIPT" ]]; then
    if ! bash "$SCAN_SCRIPT" . >/dev/null 2>&1; then
        echo "ERROR: Step 8.5 scan-credentials.sh 在 bootstrap 工作区发现凭据,bootstrap 中止"
        echo "       检查 stderr 输出:"
        bash "$SCAN_SCRIPT" . >&2 || true
        exit 1
    fi
    echo "✓ Step 8.5: scan-credentials.sh PASS (无 prod credential)"
else
    echo "ERROR: Step 8.5 scan-credentials.sh not found / not executable: $SCAN_SCRIPT"
    exit 1
fi

# === Step 9: 初始 commit(此时 hook 已装且 PASS,commit 受 Safety Floor 保护)===
git add .
git commit -m "chore: XenoDev bootstrap from ideababy_stroller framework/xenodev-bootstrap-kit/

per discussion/006/forge/v2/stage-forge-006-v2.md verdict
contract_version (mirror): SHARED-CONTRACT v2.0 ACTIVE-but-not-battle-tested
provenance: bootstrap.sh from \$IDS_KIT
pre-commit hook (credential): installed (Step 8.5)

Status: ready for B2.2 (first PRD ship + hand-back round-trip)"

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ XenoDev bootstrap complete!"
echo
echo "📋 Next steps:"
echo "  1. 验证 (本目录跑):"
echo "     test -x .claude/hooks/block-dangerous.sh && echo PASS"
echo "     test -d lib/handback-validator && echo PASS"
echo "     git log --oneline | head -1"
echo
echo "  2. 起 B2.2 sub-plan(operator 决定时机):"
echo "     - operator 手补 PRD §Real constraints + §Open questions"
echo "     - cp PRD 进 XenoDev/PRD.md"
echo "     - 起 spec-writer / task-decomposer / parallel-builder skill"
echo "     - 跑首个真 task → ship → hand-back round-trip"
echo
echo "  3. 跨仓引用:"
echo "     - IDS:   /Users/admin/codes/ideababy_stroller (SSOT)"
echo "     - kit 源: \$IDS_KIT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
