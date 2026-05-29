---
name: parallel-builder
description: |
  XenoDev L4 ship 流程标准 SKILL · 把 frozen spec 的 tasks/T*.md 拉进独立 worktree
  → TDD → codex adversarial-review(node companion.mjs 真路径)→ squash merge 回 main
  → 删 worktree → 产 hand-back。**单 task 端到端 ship**。

  **Load 触发条件**(任一满足必激活):
    1. operator 说 "起 T<NNN>" / "起 T<NNN>-A" / "ship T<NNN>" / "做 T<NNN>"(T010 / T020 / T040-A 等 numbered task)
    2. operator 说"起 FU-<...>"(FU-hotfix / FU-followup 类 task)
    3. operator 说 "起 codex review" / "跑 codex adversarial-review" / "review T<NNN>"
       · 触发 §3.1 真路径(用 node companion.mjs · 不是 codex exec hack)
    4. spec status=frozen + 至少 1 个 task 入度为 0 + operator 想起跑 build phase
    5. 任何 worktree 内 commit 后 squash merge 前的 cross-model review 阶段

  **强约束**(违 = ship 流程错误):
    - codex review 真路径 = `node "/Users/admin/.claude/plugins/cache/openai-codex/codex/1.0.3/scripts/codex-companion.mjs" {review|adversarial-review} --wait --scope working-tree [focus]`
    - 不准走 `codex exec --json ... <手写 prompt>` hack 路径(companion 自动 collect git context · 不需手写 review framing)
    - **review 命令分流**(per §3.0 决策表 · adv 不是默认):
      · `risk_level: high` / spine 重构(phase 2-3 核心)/ alembic migration / SQL / auth / 凭据 / 新增 API endpoint → `adversarial-review`
      · `risk_level: low|medium` 单层改动 / FU-hotfix / docs-only / 普通 domain+repo 加字段 → `review`
      · retroactive spec amendment commit(纯文档 frontmatter)→ 跳过 review
    - verdict enum 严格 `{approve, needs-attention}` · 任何其它值 fail closed
    - §3.2 解析必走 grep -E "^Verdict: " anchored full-line

  **不**调 IDS 的 parallel-kickoff command — 本 skill 是 XenoDev 自派生
  (per AGENTS.md §5 + framework/xenodev-spec-writer-derivation-guide.md §"3. parallel-builder")。
inspired_by: IDS .claude/commands/parallel-kickoff.md(概念引用,不 cp 代码;XenoDev 把 batch launcher 改造为 single-task end-to-end skill)+ Cursor 3 multi-root + worktrees(per stage doc verdict L549 SOTA 共同方向)
schema_version: 0.3
schema_version_history:
  - 0.1 → 0.2(2026-05-17 operator decision):加 ship task 触发条件 +
    强约束(codex review 真路径 · 不走 codex exec hack)· 防 T021+ ship 重蹈 T010-T020 hack 覆辙
  - 0.2 → 0.3(2026-05-17 operator decision):分流 `/codex:review`(常规)vs
    `/codex:adversarial-review`(高风险)· 防默认全走 adv 浪费 round + over-engineer
    finding · §3.0 加决策表 + §3.1 加两条 path
tools: Read, Write, Edit, Glob, Grep, Bash
model: opus
isolation: inline
disable-model-invocation: false
---

# parallel-builder · XenoDev L4 自派生

> **结论先**:读 frozen spec + tasks/T*.md → 独立 worktree → TDD(test red → impl green)→ codex adversarial-review(verdict ≠ BLOCK)→ merge 回 main → 删 worktree → 产 hand-back 包写回 IDS。**单 task 端到端**;batch 由 operator 串起多次调用(或在 §2.4 调度算法演化为 batch)。

## §0 输入硬约束 + Safety Floor preflight(失败立停,fail closed)

读 `specs/<feature>/spec.md` + `tasks/<TID>.md`,**任一不满足 hard-fail**(全部跑 → 全 exit 0 才进 §1):

### §0.1 spec/task/DAG 形态硬约束

| 检查 | 期望 | 失败行为 |
|---|---|---|
| spec.md `status` | `frozen` | echo "ERR: spec.md status=$val,需 frozen 才接 build" >&2; exit 1 |
| spec.md `reviewed-by` | 非 `pending`、非 `blocked-*` | echo "ERR: reviewed-by=$val,需 codex@<date> 等" >&2; exit 1 |
| 目标 task `<TID>.md` | 文件存在 + 9 字段 frontmatter 全 | echo "ERR: task 文件缺 / frontmatter 不齐" >&2; exit 1 |
| 目标 task `depends_on` | 全部已 merge 到 main(`git log --oneline main \| grep "feat.*<dep_id>"`)| echo "ERR: T<NNN> depends_on T<MMM> 未 merge,先跑那个" >&2; exit 1 |
| `dependency-graph.mmd` | 文件存在 + 含目标 task 节点 | echo "ERR: DAG 图缺;先跑 task-decomposer" >&2; exit 1 |
| working tree | 干净(`git status --porcelain` 空)| echo "ERR: working tree 有未 commit 改动,先 commit/stash" >&2; exit 1 |

### §0.2 Safety Floor preflight(per AGENTS.md §1 non-overridable;**fail closed**)

本 skill grants Bash/Write/Edit,grant 前必须实地校验三件套就位 — **缺任一 → 拒 launch,不允许"反正 hook 应该装了"假设**:

| 检查 | 命令 | 失败行为 |
|---|---|---|
| **凭据隔离**(件 1) | `test -x .claude/safety-floor/credential-isolation/scan-credentials.sh` + 对 task `file_domain` 真跑 scan,任一返 deny → block | echo "ERR: credential-isolation 缺 / task file_domain 触秘" >&2; exit 1 |
| **dangerous 命令拦截**(件 2) | `test -x .claude/hooks/block-dangerous.sh` + `grep -q '"command".*block-dangerous.sh' .claude/settings.json`(注册位生效) | echo "ERR: block-dangerous.sh 缺 / 未注册到 settings.json PreToolUse" >&2; exit 1 |
| **备份破坏检测**(件 3) | `test -x .claude/safety-floor/backup-detection/snapshot.sh` + `test -x .claude/safety-floor/backup-detection/diff-snapshot.sh` | echo "ERR: backup-detection 缺" >&2; exit 1 |

任一缺 → **fail closed**,不进 §1 worktree 创建。这条违反 AGENTS.md §1 是 non-negotiable,不接受 sandbox / dev mode override。

### §0.3 framework/ 写保护 preflight

- 拒任何 `file_domain` 含 `framework/SHARED-CONTRACT.md`(per AGENTS.md §6 + Prior Decision D4 + framework/MIRROR-PROVENANCE.md "只读")
- `framework/` 下其他文件(MIRROR-PROVENANCE.md)只允许 `task.id` 是显式声明 mirror-maintenance task 时才允许写

```bash
# preflight check
if grep -q 'framework/SHARED-CONTRACT.md' <(yq '.file_domain[]' "$TASK_FILE"); then
  echo "ERR: task file_domain 含 framework/SHARED-CONTRACT.md;违反 D4 + MIRROR-PROVENANCE 只读约束;若需改 → 起 IDS forge" >&2; exit 1
fi
```

## §1 worktree 创建

per Cursor 3 multi-root 范式(D9):每 task 一个独立 worktree + 独立分支。

### §1.1 路径 + 分支命名

```
worktree path:  projects/<feature>/<TID>
branch name:    task/<feature>-<TID>-<short-slug>
```

- `<short-slug>`:从 task `title` 字段抽 1-3 个英文 / 拼音 kebab-case(operator 可手指定)
- 路径 `projects/<feature>/<TID>` 是约定俗成,per CLAUDE.md "Per-project: `projects/<feature>/CLAUDE.md`" 隐含目录结构

### §1.2 创建命令

```bash
cd /Users/admin/codes/XenoDev
mkdir -p projects/<feature>
git worktree add projects/<feature>/<TID> -b task/<feature>-<TID>-<slug> main
```

### §1.3 file_domain 重叠检测(单 task 模式跳;batch 模式必跑)

batch 模式(2+ task 并起)时,产 conflict matrix(per IDS parallel-kickoff §2):

```
        TID-A  TID-B
TID-A   —      ?
TID-B   ?      —
```

任一 ❌(file_domain 重叠)→ **拒 launch**;让 operator 改 spec / DAG 加 dep 串行化。

单 task 模式:跳此步(无对手)。

## §2 TDD 强制 + 机器可验证(per AGENTS.md §6 C10)

worktree 内 cd 后,**严格 TDD 顺序**;**机器可验证**靠两层:(a) commit message convention + (b) `tests/red-green-log/<TID>.log` 真录证据。

**关键工程细节**:
- per round-2 F1:`bash <test> | tee` 的 `$?` 是 tee 的 exit;必须取 pipeline 第一个的 exit
- per round-3 F2(实证):**zsh `${PIPESTATUS[0]}` = EMPTY**(zsh 用 lowercase 1-indexed `${pipestatus[1]}`);bash `${PIPESTATUS[0]}` = 1
- **解法**:本 skill 所有 TDD/verify 命令**强制 bash**(用 `bash -c` 包裹或 `#!/usr/bin/env bash` shebang),不依赖用户登录 shell

### §2.1 写 negative test 先(red)

```bash
bash -c '
set -e
mkdir -p tests/red-green-log
bash <test-cmd> 2>&1 | tee -a tests/red-green-log/<TID>.log
RC=${PIPESTATUS[0]}    # bash only;调用方用 bash -c 包
echo "[red][negative][$(date -u +%Y-%m-%dT%H:%M:%SZ)] rc=$RC" >> tests/red-green-log/<TID>.log
[[ $RC -ne 0 ]] || { echo "ERR: negative test 在 impl 前已 green,TDD 顺序错" >&2; exit 1; }
'
git add tests/ && git commit -m "test: <TID> negative case for <feature> (red)"
```

### §2.2 写 positive test(red)

```bash
bash -c '
set -e
bash <test-cmd> 2>&1 | tee -a tests/red-green-log/<TID>.log
RC=${PIPESTATUS[0]}
echo "[red][positive][$(date -u +%Y-%m-%dT%H:%M:%SZ)] rc=$RC" >> tests/red-green-log/<TID>.log
[[ $RC -ne 0 ]] || { echo "ERR: positive test 在 impl 前已 green" >&2; exit 1; }
'
git add tests/ && git commit -m "test: <TID> positive case for <feature> (red)"
```

### §2.3 写 implementation(green)

按 task `## Implementation plan` 步骤实装;每步 commit:

```bash
git add <impl-files>
git commit -m "feat(<scope>): <TID> impl <slice>"
# commit message 前缀必须 'feat:' / 'fix:' / 'chore:' / 'refactor:',§4.4 verifier 校验
```

### §2.4 green 验证(转 green)

```bash
bash -c '
set -e
bash <test-cmd> 2>&1 | tee -a tests/red-green-log/<TID>.log
RC=${PIPESTATUS[0]}
echo "[green][$(date -u +%Y-%m-%dT%H:%M:%SZ)] rc=$RC" >> tests/red-green-log/<TID>.log
[[ $RC -eq 0 ]] || { echo "ERR: green 阶段 test 仍 fail" >&2; exit 1; }
'
# 跑 task ## Verification 全 checklist 真跑命令(全 0 才进 §3)
```

### §2.5 边界守则

- 不修 task `## Out of scope` 列出的文件
- 不引新依赖未更新 tech-stack.md(若有)
- 不"顺手清理"邻接代码(per ~/.claude/CLAUDE.md)
- `git diff main...HEAD --name-only` 出的所有路径必须在 task `file_domain` glob 内或 `tests/red-green-log/` 内 — §4.4 verifier 校验

## §3 cross-model review(强 hook,per AGENTS.md C11 + spec-writer SKILL §3)

verification 全过后,**必须**跑 codex review。

### §3.0 用哪个 codex review · 跑命令(单一真相 = codex-review SKILL)

**决策表 + 真路径 + verdict 解析 + log 留档全部委托给 `codex-review` SKILL**(本仓 `.claude/skills/codex-review/SKILL.md`)· 本节只列调用契约:

| 维度 | 引用 codex-review SKILL 章节 |
|---|---|
| 决策表(`review` vs `adversarial-review`)| §2(§2.1 adv 触发 / §2.2 review 触发 / §2.3 跳过) |
| 真路径(node companion.mjs)+ 两条命令 | §3(§3.1 path A · §3.2 path B · §3.3 参数说明) |
| ship 流程内调用契约 | §3.4 |
| verdict 解析 + fail closed | §4(§4.1 严格命令 + §4.2 4 轮上限) |
| review log 留档 | §5.1 ship 流程(worktree)|
| Anti-patterns + escalation | §6 + §7 |

#### §3.0.1 ship 流程调用 contract

ship 流程内本节(parallel-builder §3)对 codex-review SKILL 的输入:
- task frontmatter 真值(`risk_level` / `phase` / `file_domain` · 走 codex-review §2 决策表)
- worktree path(`scope = working-tree`)
- focus 串 task 信息(TID / worktree 路径 / 重点 challenge)

codex-review SKILL 返:
- verdict ∈ {approve, needs-attention}
- 若 approve → 进本 SKILL §4 merge
- 若 needs-attention → 回本 SKILL §2 改 impl · 重跑

**ship 流程内强约束**:codex-review §2 触发 path A(adversarial) → 本 SKILL §4.1 atomic order 必跑 path A;不接受 ship 流程内默认全走 review 路。

### §3.2 verdict 解析 + log 留档(委托 codex-review SKILL)

| 项 | 委托位置 |
|---|---|
| verdict enum + 严格解析命令 | codex-review SKILL §4.1 |
| 4 轮上限 + needs-attention 回流处理 | codex-review SKILL §4.2 |
| ship 流程内 log 路径 = `review-log/<TID>-round<N>.md`(worktree 内 · 不进 main)| codex-review SKILL §5.1 |

ship 流程 verdict 处理结果(`approve`/`needs-attention`/fail closed)按 codex-review §4 返;本 SKILL §4.1 atomic order 按 verdict 决策 merge or 回流。

## §4 merge 回 main(原子化:hand-back 先于 merge)

per round-1 codex finding F4:hand-back 失败必须能阻 ship,**所以 hand-back draft + producer validate 必须在 merge 前完成**(详见 §6)。本节仅讲 merge 机制。

### §4.1 atomic order(强约束)

```
1. §3 codex review PASS
2. §4.4 TDD/scope verifier PASS(commit 序 + diff 边界)
3. §6.1 + §6.2 hand-back draft + producer 6 约束 PASS(merge 前)
4. §4.5 merge --squash 到 main + commit
5. §6.4 cp hand-back 到 IDS dir + consumer 6 约束 PASS(merge 后立即)
6. §6.5 写 .eval/events.jsonl 一行(verdict=PASS)
7. §5 删 worktree + branch(全部成功才删,失败留 worktree 给 operator 调试)
```

任一失败 → 不 merge / 不 cp / 不删;留 worktree;stderr 真错,operator 修。

### §4.2 scope 映射(白名单,非自由推断)

| file_domain prefix | scope 字串 | 备注 |
|---|---|---|
| `.claude/hooks/` | `safety-floor` | hook 自身改动 |
| `.claude/safety-floor/` | `safety-floor` | 三件套配套 |
| `.claude/skills/` | `skill` | skill 派生 |
| `lib/handback-validator/` | `handback` | validator + template 实装 |
| `lib/eval-event-log/` | `eval` | event log 实装 |
| `lib/workspace-schema/` | `workspace` | workspace 4 字段 |
| `tests/integration/` | `test` | integration test |
| `tests/red-green-log/` | `test` | TDD 证据日志(随 task commit)|
| `specs/` | `docs` | spec 文档 |
| `framework/MIRROR-PROVENANCE.md` | `framework` | **只允许此一文件**;改 SHARED-CONTRACT.md 已 §0.3 拒 |
| 其他 | hard-fail,operator 决 | 不自由推断 |

### §4.3 merge 命令

```bash
cd /Users/admin/codes/XenoDev      # 回 main worktree
git merge --squash task/<feature>-<TID>-<slug>
git commit -m "$(cat <<EOF
feat(<scope>): <TID> <title>

<task body 关键点 + verification 摘要 + review verdict 证据>

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

### §4.4 pre-merge TDD/scope verifier(commit topology + 每 commit 内容校验)

per round-2 F3 + round-3 F3:timestamp 可改写,**必须**用 `git rev-list --reverse main..HEAD` 拓扑序;且 round-3 F3 实证只查前缀可被 spoof — `test:` commit 内可塞 production 改动。**必须**逐 commit 内容验:test: commit 只允许 test path,production 改动只能在 feat: commit。

merge 前必须跑 verifier,exit 0 才 merge:

| 检查 | 期望 | 失败行为 |
|---|---|---|
| **commit 拓扑序** | `git rev-list --reverse main..HEAD` 抽序;**第 1 个 commit 必须 `^test:`**;**所有 `^feat:` / `^fix:` commit 索引 > 至少 1 个 `^test:` commit 索引** | exit 1 |
| **每 commit 内容**(per round-3 F3)| 对每 commit:`git show --name-only --format= <SHA>` 抽改动文件:<br>- `^test:` commit 改动仅在 `tests/**`(包括 `tests/red-green-log/` `tests/integration/` 等)<br>- `^feat:` / `^fix:` commit 改动允许在 task `file_domain` 内,但**不允许**新加 test fixture(那已在 test commit)<br>- `^chore:` / `^docs:` commit 不动 production code | echo "ERR: <SHA> commit prefix '$P' 但改动 file 越类型: <list>" >&2; exit 1 |
| red-green log | `tests/red-green-log/<TID>.log` 含 ≥1 `[red] rc!=0` + 末尾 `[green] rc=0` | exit 1 |
| diff 边界(全 branch)| `git diff --name-only main...HEAD` 所有路径在 task `file_domain` glob ∪ `tests/red-green-log/` ∪ task scope 显式列的 dir | exit 1 |
| framework/SHARED-CONTRACT.md | 0 改动(`git diff --name-only main...HEAD \| grep -F framework/SHARED-CONTRACT.md` 空)| exit 1 |
| commit message 前缀 | 每 commit 前缀 ∈ {test:, feat:, fix:, chore:, refactor:, docs:} | exit 1 |

timestamp 仅作 audit metadata 写 hand-back,**不**作 gate 输入。

### §4.5 push 策略

**不主动 push**(per CLAUDE.md);留给 operator。

## §5 删 worktree + 分支(条件:§6 全 PASS)

仅当 §6 全部 PASS(producer + cp + consumer + event log 全 0)才删:

```bash
git worktree remove projects/<feature>/<TID>
git branch -D task/<feature>-<TID>-<slug>
```

worktree 残留检查:`git worktree list` 应只剩 main 一行。

§6 任一失败 → **保留 worktree + branch**(证据不丢,operator 调试用);main 上的 squash commit 视失败原因决定是否 revert(operator 拍板)。

## §6 hand-back 包(原子化:draft 先于 merge,cp 后于 merge)

per AGENTS.md §6 + CLAUDE.md 工作流 + Prior Decision D10。**两段式**(per round-1 codex finding F4):

### §6.1 draft + producer 验(merge 前;私有 mktemp -d + 700 + 进程内 sha256)

per round-2 F4 + round-3 F4:`/tmp/handback-lock-*` 共享路径不安全;改 **私有 dir + 700 perm + 进程内变量持锁**(不落 lock file):

```bash
bash -c '
set -e

# 私有 dir,owner 700,无别人可读写
PRIV_DIR=$(mktemp -d -t "xenodev-handback.XXXXXXXX")
chmod 700 "$PRIV_DIR"
# DRAFT 用临时 basename(gen-handback 会决定真 basename,SKILL §6.3 从 frontmatter 反推)
DRAFT="$PRIV_DIR/draft.md"

bash lib/handback-validator/gen-handback.sh \
  --feature <F> --task-id <TID> \
  --tag <tag> --severity <sev> --rationale "<text>" \
  --out "$DRAFT"

bash lib/handback-validator/validate-handback.sh "$DRAFT" /Users/admin/codes/ideababy_stroller --mode=producer || {
  echo "ERR: producer fail,拒 merge" >&2
  rm -rf "$PRIV_DIR"
  exit 1
}

# producer 通过 → 从 draft frontmatter 反推 IDS basename
# (gen-handback 内部 BASE=${TS}-${HANDBACK_ID}.md;HANDBACK_ID=${PRD_FORK_ID}-${TS})
# **关键**:不要在 SKILL 里手算 BASE,容易与 gen 实装漂移(round 3 F1 实证)
HANDBACK_ID=$(awk "/^---\$/{if(++c==1) next; if(c==2) exit} c==1" "$DRAFT" \
  | grep -E "^handback_id:" | head -1 \
  | sed -E "s/^handback_id:[[:space:]]*//" | sed "s/^\"//;s/\"\$//")
TS_FROM_ID=$(echo "$HANDBACK_ID" | sed -E "s/^.*-([0-9]+T[0-9]+Z)\$/\\1/")
BASE="${TS_FROM_ID}-${HANDBACK_ID}.md"

# producer 通过 → 锁 sha 在进程内变量(不落 lock file,per round-3 F4)
DRAFT_SHA=$(shasum -a 256 "$DRAFT" | awk "{print \$1}")
export DRAFT_SHA PRIV_DIR DRAFT BASE HANDBACK_ID    # 后续 §6.3 在同进程内消费
'
```

**两段命令必须同 bash 进程**(用 `bash -c '...'` 一气包,或 wrap 成单 `.sh` 脚本);否则 export 丢失,要 fall back 到落 file 但要 chmod 600 + chown $USER 验。

**注(FU-producer-1 ship 后)**:`gen-handback.sh` 已实装(2026-05-11),强制三字段 source_repo_identity 读 HANDOFF.md 真值,**拒任何 `--remote-url` 等 CLI override**(防绕 SSOT)。caller 不允许传三字段;`--feature` / `--task-id` / `--tag` / `--severity` / `--rationale` / `--out` 是 task 信息 API,gen 内部从 HANDOFF.md SSOT 拉真值填 frontmatter。

### §6.2 producer 失败 = 拒 merge(per D10 hard-fail)

draft 或 producer 任一失败 → **绝不 merge**(此时 main 还没动);stderr 真粘;不缓冲 / 不重试 / 不静默。

### §6.3 merge 后 cp + consumer 验(进程内 sha 复核 + 排他 ln 创建 + EXDEV fallback)

per round-3 F5:`mv -n` 与 target check 之间有 race;改 **`ln`(hardlink)排他创建** — `ln src dst` 在 dst 存在时直接 fail,无 race。

**per FU-producer-2(2026-05-24)**:实装 cross-device fallback(原文字声明 line 414 现真为代码):`ln` 因 EXDEV(cross-device)失败 → cp 到同目录 tmp + sha 复验 + 同目录 ln tmp→TGT(同目录 ln 不会 EXDEV) → 清 tmp。两步都失败 hard-fail。EEXIST(撞库)仍 hard-fail 不重试(per FU-producer-1 round 2 F3 决议)。

```bash
# 同 §6.1 的 bash -c 进程内继续(DRAFT_SHA / PRIV_DIR / DRAFT / BASE 已 export)
bash -c '
set -e
[[ -n "${DRAFT_SHA:-}" && -f "${DRAFT:-}" ]] || { echo "ERR: §6.1 export 丢失;不能继续" >&2; exit 1; }

# sha256 复核(producer 验后到 cp 前 draft 不能变)
NEW_SHA=$(shasum -a 256 "$DRAFT" | awk "{print \$1}")
[[ "$NEW_SHA" == "$DRAFT_SHA" ]] || {
  echo "ERR: draft sha256 漂移(producer locked=$DRAFT_SHA, now=$NEW_SHA);拒 cp" >&2
  rm -rf "$PRIV_DIR"
  exit 1
}

# 目标路径:per validator §6.2.1 约束 6
TGT="/Users/admin/codes/ideababy_stroller/discussion/<id>/handback/${BASE}"
mkdir -p "$(dirname "$TGT")"

# **排他 hardlink 创建** + **EXDEV fallback**(FU-producer-2 实装)
# 路径 1:同卷 ln(原子,首选)
# 路径 2:cross-device → cp 到 TGT 同目录 tmp + sha 复验 + ln tmp→TGT(同目录无 EXDEV)
# 撞库(EEXIST):hard-fail 不重试(per FU-producer-1 round 2 F3 决议 · 让 caller 重 gen TS)
if ln "$DRAFT" "$TGT" 2>/dev/null; then
    PUBLISH_MODE="ln"
else
    # ln 失败 — 区分 EEXIST(撞库)vs EXDEV(cross-device)
    if [[ -e "$TGT" ]]; then
        echo "ERR: target $TGT 已存在(撞库),hard-fail;若并发 ship 重 gen TS" >&2
        rm -rf "$PRIV_DIR"
        exit 1
    fi
    # 同目录 tmp + cp + sha 复验 + ln tmp→TGT(rename-like 原子语义)
    # tmp 名:basename.tmp.$$.<ts>(防 $$ collision)
    TGT_TMP="${TGT}.tmp.$$.$(date +%s)$RANDOM"
    cp "$DRAFT" "$TGT_TMP" || {
        echo "ERR: cp draft → $TGT_TMP fail(cross-device fallback)" >&2
        rm -f "$TGT_TMP"
        rm -rf "$PRIV_DIR"
        exit 1
    }
    # 复 sha 验证(防 cp 期间 disk corruption · per round-3 F5 范式)
    TMP_SHA=$(shasum -a 256 "$TGT_TMP" | awk "{print \$1}")
    [[ "$TMP_SHA" == "$DRAFT_SHA" ]] || {
        echo "ERR: cp 后 tmp sha 漂移(disk corruption?)expected=$DRAFT_SHA, got=$TMP_SHA" >&2
        rm -f "$TGT_TMP"
        rm -rf "$PRIV_DIR"
        exit 1
    }
    # ln tmp → TGT(同目录 ln 不会 EXDEV;失败说明撞库或 perm)
    if ! ln "$TGT_TMP" "$TGT" 2>/dev/null; then
        echo "ERR: ln $TGT_TMP $TGT 失败(撞库或 perm 异常)" >&2
        rm -f "$TGT_TMP"
        rm -rf "$PRIV_DIR"
        exit 1
    fi
    rm -f "$TGT_TMP"
    PUBLISH_MODE="cp+ln"
fi

# 发布后 sha 复验(per round-3 F5:确认 disk 上的就是 producer 验过的)
TGT_SHA=$(shasum -a 256 "$TGT" | awk "{print \$1}")
[[ "$TGT_SHA" == "$DRAFT_SHA" ]] || {
  echo "ERR: 发布后 target sha 与 producer locked 不一致(mode=$PUBLISH_MODE · disk corruption?)" >&2
  rm -f "$TGT"
  rm -rf "$PRIV_DIR"
  exit 1
}

# consumer 6 约束验
bash lib/handback-validator/validate-handback.sh "$TGT" /Users/admin/codes/ideababy_stroller --mode=consumer || {
  rm -f "$TGT"
  echo "ERR: consumer fail (mode=$PUBLISH_MODE);已清 $TGT;merge 已入 main,operator 决 revert/forward fix" >&2
  rm -rf "$PRIV_DIR"
  exit 1
}

# 全过 → 输出 publish mode + 清私有 dir
echo "Publish mode: $PUBLISH_MODE"
rm -rf "$PRIV_DIR"
'
```

**Cross-device fallback 真实装**(FU-producer-2 2026-05-24):`ln` 失败若因 EXDEV(/tmp 与 IDS dir 不同卷)→ cp 到 TGT 同目录 tmp + sha 复验 + ln tmp→TGT(rename-like 语义)→ 清 tmp。PUBLISH_MODE 区分 ln vs cp+ln,operator 调试 / SLA 追踪用。macOS 同 user `/tmp` 与 `/Users/...` 通常同卷,正常路径 PUBLISH_MODE=ln;不同卷(RAM disk / NFS / tmpfs)走 cp+ln。

**真路径警示(per FU-T021-followup-4 · IDS entry 13 DROP precedent)**:producer 端**不**在 hand-back 包 §7 "operator 下一步" 字面写 cp 命令(避手敲 filename 漏 ISO ts prefix · 触发 IDS validator §6.2.1 约束 5 hard-fail · 真实证 T021 hand-back-id `004-pB-20260518T060000Z` entry 13 DROP · IDS commit `44d0d5a` · XenoDev producer-fix commit `8eceddc`)· 真 cp 路径走本节 bash -c pipeline 真路径反推 BASE(L347 字面 `BASE="${TS_FROM_ID}-${HANDBACK_ID}.md"`)· 见 §7 #10 anti-pattern。

### §6.4 写 .eval/events.jsonl 一行

T003 实装后 `lib/eval-event-log/writer.sh` 可调;之前用 echo + jq:

```bash
bash lib/eval-event-log/writer.sh \
  --type review_failure --feature <F> --task-id <TID> \
  --reviewer codex --round <N> --verdict PASS \
  --findings_summary "task <TID> shipped + handback consumer PASS"
```

### §6.5 consumer 验失败 / event 写入失败的处置

main 上已 squash commit,IDS dir 可能有半文件:

1. `rm -f $TGT`(清 IDS 半文件)
2. **不**自动 revert main commit(留 operator 决:revert vs forward fix)
3. echo "WARN: hand-back consumer 失败,main 已 squash commit;operator 决 revert/forward fix" >&2
4. 不删 worktree(留证据)
5. `.eval/events.jsonl` 写一条 `verdict: handback_consumer_fail`

## §7 Anti-patterns(直接拒)

1. **跳 worktree**(直接在 main impl)→ 拒;失去隔离 + 风险 + cleanup 困难
2. **跳 TDD**(impl 先于 test)→ commit 序检测;违反 → review 阶段会被 codex 抓
3. **跳 review**(merge 前不跑 codex)→ 拒,违反 C11
4. **跳 hand-back**(merge 完即结束)→ 拒,违反 §6 + AGENTS.md §6 "hand-back 必产"
5. **file_domain 私自扩展**(改了 task 没列出的文件)→ codex review 会抓;follow-up 必须新开 task
6. **squash 后保留长 branch**(不删)→ 仓库累垃圾;§5 必跑
7. **review BLOCK 后强 merge**(--no-verify 等)→ 违反 C11 + 安全;hard-stop
8. **batch 模式不查 file_domain matrix**(直接并行)→ 拒,违反 §1.3
9. **worktree 跑完不删**(`git worktree list` 留多行)→ §5 必清
10. **hand-back 包 §7 字面写 cp 命令**(避 producer 手敲 filename 漏 ISO ts prefix)→ 拒;真 cp 流程走 §6.3 bash -c pipeline 从 frontmatter `handback_id` 反推 `BASE="${TS_FROM_ID}-${HANDBACK_ID}.md"`(L347 字面)· 不靠 hand-back §7 paste-runnable 命令(producer 手敲 filename 容易漏 ISO ts prefix · 触发 IDS validator §6.2.1 约束 5 hard-fail · 真实证 T021 hand-back-id `004-pB-20260518T060000Z` entry 13 DROP · IDS commit `44d0d5a` · XenoDev producer-fix commit `8eceddc` · FU-T021-followup-4 root cause)

## §8 Failure mode + escalation

| 症状 | 处置 |
|---|---|
| `git worktree add` 失败(分支已存在 / 路径占用)| 删旧 branch / 路径,重跑;不 force |
| TDD red 后 impl 一直 green 不了 | 先看是否 spec 有问题(回 spec-writer);别死磕 hack |
| codex 4 轮 BLOCK | hard-stop;operator 决(同 spec-writer §3.2)|
| codex CLI 不可用(node 报错)| stderr 真粘报错;**不**静默 mark reviewed;operator 修 codex 安装 |
| merge 出冲突(并行 task file_domain 漏检)| 退 task 到 worktree 修 / 重画 DAG;不强 merge |
| hand-back validator 6 约束失败 | hard-stop(per D10);看具体 check 哪条挂(check-1 ~ check-6)|
| 跑完发现 verification 实际跑不通(spec/task 有缝) | 加 follow-up task,operator 决先 ship 还是回退 |

## §8.1 review_history(本 SKILL 自身经历的 codex review)

| Round | Verdict | Findings | Actions |
|---|---|---|---|
| 1 | needs-attention | 2 high(Safety Floor 没接 / TDD 不可机器执行)+ 3 medium(verdict 解析弱 / hand-back 顺序错 / framework scope 弱)| §0.2/§0.3 加 preflight + §2 加 PIPESTATUS + log + §3.2 严格 enum + §4.1 atomic order + §4.2 scope 白名单 |
| 2 | needs-attention | 1 critical(`tee \| $?` 错)+ 3 high(verdict substring / timestamp 可改 / handback /tmp 路径)| §2 改 `${PIPESTATUS[0]}` + §3.2 anchored line + §4.4 拓扑序 + §6.1 mktemp + sha lock |
| 3 | needs-attention | 3 high(verdict enum 错 = `approve` / zsh PIPESTATUS empty / 拓扑只查 prefix)+ 2 medium(/tmp lock 共享 / mv -n race)| §3.2 enum 改 approve/needs-attention + §2 全 `bash -c` 包 + §4.4 加每 commit 内容验 + §6.1 私有 dir 700 + 进程内变量持锁 + §6.3 ln 排他创建 + sha 复验 |

**status**: 4 轮上限触顶(per spec-writer SKILL §3.2 同款契约);round 3 critical(verdict enum 错)若不修 skill 直接不工作,故修复 + 实证(zsh/bash PIPESTATUS 实跑见 commit message 或 git log evidence)+ 标 `blocked-after-4-rounds`,operator 决策升 frozen。

## §9 完成 checklist(每 task ship 前 operator 自审)

- [ ] §0.1 spec/task/DAG 形态硬约束全 PASS
- [ ] §0.2 Safety Floor 三件套 preflight PASS(凭据 + dangerous + 备份检测)
- [ ] §0.3 framework/SHARED-CONTRACT.md 写保护 PASS(0 改动)
- [ ] worktree 在 `projects/<feature>/<TID>`,branch `task/<feature>-<TID>-<slug>`
- [ ] §2 TDD 严格顺序(test red 在 impl 前)+ `tests/red-green-log/<TID>.log` 含 [red] [green] 行
- [ ] task `## Verification` 全 checklist PASS(实跑命令,不口头)
- [ ] §3.0 按决策表选 path(A=adversarial / B=review / 跳过 = retroactive 纯文档)
- [ ] §3.1 跑 codex `node companion.mjs {review|adversarial-review}` · verdict=approve · review log 留 worktree(`review-log/<TID>-round<N>.md`)
- [ ] §4.4 pre-merge verifier PASS(commit 序 + scope 边界 + framework 写保护)
- [ ] §6.1 hand-back draft + producer 6 约束 PASS(**merge 前**)
- [ ] §4.5 merge --squash 到 main,commit message Conventional + Co-Authored-By
- [ ] §6.3 cp 到 IDS dir + consumer 6 约束 PASS(**merge 后**)
- [ ] §6.4 `.eval/events.jsonl` 加一条(verdict=PASS)
- [ ] §5 worktree 删 + branch -D 删(条件:§6 全 PASS)
- [ ] `git worktree list` 只剩 main 一行
- [ ] **不 push**(等 operator)

## §10 单 task vs batch 模式

| 模式 | 适用 | §1.3 file_domain matrix | 调度 |
|---|---|---|---|
| 单 task(本 SKILL §1-§9 默认)| 入度 0 task / operator 串行调 | 跳 | 顺序 |
| batch 模式(2-5 task 并起,后续演化)| 多入度 0 task 同时 / max worker = 3-5 | **必跑**(任一 ❌ 拒)| 拓扑排序按 depends_on |

batch 模式留 v0.2 演化(per spec §2.2 OUT 不是,但 v0.1 单 task 已够)。

## §11 与上下游的关系

- **上游**:`task-decomposer` skill 产 frozen spec + tasks/T*.md + dependency-graph.mmd(SKILL §0 硬约束验)
- **下游**:hand-back 包 → IDS `discussion/<id>/handback/`(per SHARED-CONTRACT §6.3)
- **跨仓**:本 skill cp hand-back 到 IDS dir;**不**触发 IDS `/handback-review`(那是 operator 在 IDS session 跑)
- **同仓**:本 skill 不调 spec-writer / task-decomposer skill(单向消费);若发现 spec 有问题 → 加 follow-up task / 产 `prd-revision-trigger` hand-back

---

**Provenance**:
- 概念骨架(worktree-per-task / file_domain matrix / dependency check / launch summary)派生自 `ideababy_stroller/.claude/commands/parallel-kickoff.md`(IDS L3 范式,XenoDev 改造为 single-task end-to-end skill)
- TDD 强制 + cross-model review hook + 4 轮上限派生自 spec-writer SKILL §3 + AGENTS.md §6 C10/C11
- hand-back 失败 hard-fail 派生自 AGENTS.md §4 + CLAUDE.md "工作流" + Prior Decision D10
- isolation: worktree 范式参考 Cursor 3 multi-root(per stage doc verdict)
- 不 cp IDS commands/ 代码,只引概念(per stage doc §"模块 B" step 7 schema 重新派生原则)
