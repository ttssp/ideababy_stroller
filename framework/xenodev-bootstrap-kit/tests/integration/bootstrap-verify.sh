#!/usr/bin/env bash
# bootstrap-verify.sh — T010 · O3 setup precondition
#
# per specs/006a-pM/spec.md §6 O3 行末"追加 bootstrap verify"段
# 把 spec 内联的一长串 bash -c '...' 命令沉淀为单文件 test,
# operator 可单跑或被 T012 聚合(全 4 Outcomes SHIP GATE)
#
# 跑法:
#   bash tests/integration/bootstrap-verify.sh
# 退 0 + stdout 含 BOOTSTRAP-OK → 全过
# 退 1 + stderr 报哪项 missing  → 某 bootstrap 件缺失
#
# 校验范围(per T010 spec §"Outputs"):
#   1. spec §6 O3 原命令逐字(根 doc + lib/ 三套 + .claude/hooks 件 2 + 老 skill 二件)
#   2. T002 parallel-builder skill 实装 check
#   3. T003 eval-event-log writer 实装 check(SSOT 真名 writer.sh · 跟 T003 A1 amendment 对齐)
#   4. framework mirror 完整性 check(D2 落 SHARED-CONTRACT.md + MIRROR-PROVENANCE.md)
#   5. T001 dangerous-24 fixture 完整性 check
#
# 本 test 仅校文件存在性,**不**校文件内容(各 task 自己 verification 管内容)
# 本 test 仅校文件存在性,**不**接 eval-event-log writer(防自污染 events)

set -e

# === 切到 repo root,无视调用者 cwd ===
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

# === 1. spec §6 O3 原命令逐字(根 doc + lib/ 三套 + 件 2 + 老 skill 二件)===
ls AGENTS.md CLAUDE.md PRD.md HANDOFF.md >/dev/null
test -d lib/handback-validator
test -d lib/workspace-schema
test -d lib/eval-event-log
test -x .claude/hooks/block-dangerous.sh
test -f .claude/skills/spec-writer/SKILL.md
test -f .claude/skills/task-decomposer/SKILL.md

# === 2. T002 parallel-builder skill 实装 check ===
test -f .claude/skills/parallel-builder/SKILL.md

# === 3. T003 eval-event-log writer 实装 check ===
# 注:spec §40 写的是 write-event.sh 但 SSOT 真名是 writer.sh(per T003 A1 amendment)
test -x lib/eval-event-log/writer.sh

# === 4. framework mirror 完整性 check(D2 落)===
test -f framework/SHARED-CONTRACT.md
test -f framework/MIRROR-PROVENANCE.md

# === 5. T001 dangerous-24 fixture 完整性 check ===
test -f .claude/hooks/test-fixtures/dangerous-24.txt
test -x .claude/hooks/test-fixtures/run-dangerous-24.sh

# === 6. Safety Floor 件 1 凭据隔离实装 check ===
# per CLAUDE.md §"三件硬约束" + codex round 1 P2 finding(本 bootstrap gate
# 不能只校件 2 漏件 1/件 3 否则 SHIP GATE 会漏报)
test -d .claude/safety-floor/credential-isolation
test -x .claude/safety-floor/credential-isolation/pre-commit-credential.sh
test -x .claude/safety-floor/credential-isolation/scan-credentials.sh

# === 7. Safety Floor 件 3 备份破坏检测实装 check ===
test -d .claude/safety-floor/backup-detection
test -x .claude/safety-floor/backup-detection/diff-snapshot.sh
test -x .claude/safety-floor/backup-detection/snapshot.sh

echo BOOTSTRAP-OK
