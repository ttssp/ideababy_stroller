---
description: Review hand-back packages from XenoDev (per SHARED-CONTRACT §6 v2.0). Reads discussion/<id>/handback/*.md, validates against §6.2.1 6 constraints (M2 contract-only; validator code lands in B2.1), prompts operator to decide on each package's §3 actions, appends decision to HANDBACK-LOG.md.
argument-hint: "<discussion-id>  e.g. 008"
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(date:*), Bash(realpath:*), Bash(test:*), Glob, Grep
model: opus
---

# Handback Review · L4 reverse channel consumer (v2.0)

Discussion id: **$ARGUMENTS** (e.g. `008`).

> **v2.0 (M2 cutover, 2026-05-10)**:per `framework/SHARED-CONTRACT.md` §6 v2.0,本命令是 hand-back 通道在 IDS 端的 consumer 入口。XenoDev 跑完 task ship / spec violation / drift detection 后产 hand-back 包(§6.3 schema)写回 IDS `discussion/<id>/handback/`,operator 在 IDS 跑本命令决议。
>
> **本 v2.0 是命令骨架(M2 contract-only)**:6 约束的真实校验代码在 B2.1 阶段(XenoDev bootstrap)实装为可调 validator;本命令在 M2 阶段引 §6.2.1 全文为 normative source,operator 手工按 contract 校验。

## Step 1 · locate handback dir

```bash
HANDBACK_DIR="discussion/<discussion-id>/handback/"
test -d "$HANDBACK_DIR" || {
  echo "no hand-back packages found at $HANDBACK_DIR — nothing to review"
  exit 0
}
```

若目录不存在 → exit 0(operator 未跑过 XenoDev 或 XenoDev 未产任何 hand-back 包,正常状态)。

## Step 2 · 6 约束自检契约(§6.2.1 normative source)

per `framework/SHARED-CONTRACT.md` §6.2.1,任何 hand-back 包 **producer**(XenoDev)写入前与 **consumer**(本命令)读取前都必须按 6 条约束自检。任一失败即 `hard-fail`(producer 不写 / consumer 不读)。

**约束 1 · canonical-path containment**:
- `realpath(handback_target)` 必须严格落在 `realpath(source_repo) + "/discussion/" + <id> + "/handback/"` 之下
- 防 `handback_target = "/tmp/whatever"` / `"<source_repo>/../other-repo/..."` / `"<source_repo>/discussion/006/handback/../../specs/..."` 三种 path traversal

**约束 2 · symlink reject**:
- `<source_repo>/discussion/...` 路径段任一是 symlink → reject(不要 follow)
- `source_repo` 自身可以是 symlink(operator dev workflow 决定),只校验 source_repo 之下路径段

**约束 3 · repo identity check(三模式)**:
- **remote 模式**(有 git remote):比对 `git config remote.origin.url` == hand-off 包 `source_repo_identity.expected_remote_url`
- **no-remote 模式**(无 git remote):比对 `head -c 30 CLAUDE.md` 含 hand-off 包 `source_repo_identity.repo_marker`(必含 "Idea Incubator")
- **hash-only 模式**(operator 显式开启):比对 `sha256(.git/HEAD + .git/config)` == hand-off 包 `source_repo_identity.git_common_dir_hash`
- 任一模式 PASS 即满足约束 3
- (M2 阶段 contract-only;B2.1 实装 validator 代码)

**约束 4 · hard-fail 行为**:
- 任一约束失败,producer 不写文件 / 不创目录 / 只 stderr;consumer 不读取内容 / 只 stderr 报哪条约束失败 + handback_id / exit 非 0
- 第一性原因:hand-back 通道是跨仓写入,silent error 在跨仓场景下永远诊断不到

**约束 5 · id consistency check**:
- 三处 id 严格一致:
  1. 物理路径中 `discussion/<X>/handback/` 的 `<X>` 段
  2. 文件名 `<ISO ts>-<handback_id>.md` 中 `handback_id` 解出的 `<discussion_id>` 前缀
  3. frontmatter `discussion_id` / `prd_fork_id` / `handback_id` derived 公式
- 三处任一不匹配 = `Drop`(防 corruption-of-corpus)

**约束 6 · id 字符集 + filename basename + final-path containment**:
- id 字符集 regex(producer + consumer 都校验):
  - `discussion_id` ~= `^[0-9]{3}$`
  - `prd_fork_id`   ~= `^[0-9]{3}[a-z]?(-p[A-Z])?$`
  - `<ISO ts>`      ~= `^[0-9]{8}T[0-9]{6}Z$`(UTC,无毫秒)
  - `handback_id`   ~= `<prd_fork_id> + "-" + <ISO ts>` 严格拼接
  - 三个 id token 任一含 `/` `\` `..` 控制字符 (`\x00-\x1f\x7f`) 或绝对路径前缀 = `Drop`
- filename basename 校验:`os.path.basename(filename) == filename`(不含 separator)
- final-path containment 二次校验:`realpath(target_dir + "/" + filename)` 必须严格落在 §6.4 路径之下
- OWASP path traversal 标准防御(input shape validation + defense in depth)

**M2 contract-only 注**:本节列约束 1-6 全文是 normative contract;实际可调 validator 代码在 B2.1 阶段(XenoDev bootstrap)实装。M2 阶段 operator 按 contract 手工核对。

## Step 3 · 读取 hand-back 包列表

```bash
ls "$HANDBACK_DIR"*.md 2>/dev/null | grep -v 'HANDBACK-LOG.md' | sort
```

按文件名 ts 排序(文件名格式 `<ISO ts>-<handback_id>.md`,ts 在前自然按时间序)。

若空 → exit 0("no new hand-back packages, only HANDBACK-LOG.md exists")。

## Step 4 · 逐条决议

对每个 hand-back 包(顺序处理):

1. **Read frontmatter**:提取 `discussion_id` / `prd_fork_id` / `handback_id` / `tags` / `severity` / `created` / `related_task` / `related_spec_section` / `workspace`
2. **6 约束自检**(M2 阶段 operator 手工按 §6.2.1 contract 核对;B2.1 后 validator 自动跑):
   - 路径在 `discussion/<id>/handback/` 之下?
   - 路径段无 symlink?
   - frontmatter `workspace.source_repo` 与本仓 identity 一致?
   - 三处 id 一致(路径 / filename / frontmatter)?
   - id 字符集 / filename basename 都通过?
   - 任一失败 → 报 stderr,跳过本包,继续下一个
3. **Read body**:§1 build-side 上下文 / §2 触发理由(按 tags 列条) / §3 给 IDS 的建议
4. **Display to operator**:
   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📦 Handback: <handback_id>
   📅 Created: <created>
   🏷️  Tags: <tags>      Severity: <severity>
   🔗 Related task: <related_task>
   🔗 Related spec: <related_spec_section>

   §1 (Build-side context):
   <body §1 content, max 500 字>

   §2 (Triggers):
   <body §2 content, per tags>

   §3 (Suggested IDS actions):
   - [ ] 修 PRD §"<section>"
   - [ ] 修 SHARED-CONTRACT §"<section>"
   - [ ] 修 XenoDev spec(本仓内,信息式)
   - [ ] 无操作(收悉,作为 practice-stats 入库)

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Operator decides which to apply (multiSelect possible) + free-text comment
   ```
5. **operator 决议**:用 AskUserQuestion 收集勾选 + 自由备注

## Step 5 · 写入 HANDBACK-LOG.md(append-only 决议日志)

```bash
LOG="$HANDBACK_DIR/HANDBACK-LOG.md"
test -f "$LOG" || cat > "$LOG" <<'EOF'
---
doc_type: handback-decision-log
first_created: <ISO ts>
last_updated: <ISO ts>
total_decisions: 0
note: append-only;每条决议追加一段 ## entry;不删除 / 不修改既有 entry
---

# HANDBACK-LOG · discussion <discussion-id>

per `framework/SHARED-CONTRACT.md` §6.4,本文件是 operator 在 IDS 端对 XenoDev hand-back 包的决议日志。append-only。

EOF
```

每条决议 append 一段:

```markdown
## <ISO ts> · <handback_id>

**Reviewed at**: <`date -u +%Y-%m-%dT%H:%M:%SZ`>
**Tags**: <from frontmatter>
**Severity**: <from frontmatter>
**Operator decisions**:
- [<x|>] 修 PRD §"<section>"
- [<x|>] 修 SHARED-CONTRACT §"<section>"
- [<x|>] 修 XenoDev spec(本仓内,信息式)
- [<x|>] 无操作(收悉)

**Operator note**: <free text from AskUserQuestion>

**Follow-up commits**: <if operator already acted, list commit hashes;else "pending">
```

frontmatter `last_updated` + `total_decisions` 同步更新(用 Edit 而非 Write,保 append-only 语义)。

## Step 6 · 输出 next-step menu

per CLAUDE.md "every command outputs next-step menu":

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Handback review complete for discussion <id>.

Reviewed: <N> hand-back packages
Decisions logged: discussion/<id>/handback/HANDBACK-LOG.md
Pending operator actions:
  - <M> PRD revisions      → /scope-inject <id> 或手工改 PRD 后 /plan-start <prd-fork-id>
  - <K> SHARED-CONTRACT 修订 → 手工改 framework/SHARED-CONTRACT.md(M2 cutover 后协议层 ACTIVE)
  - <J> XenoDev spec 修订   → 跨仓:cd /Users/admin/codes/XenoDev && 改 spec
  - <L> 信息式无操作         → 已入库 practice-stats

📋 Next step menu:

[1] (默认 if M ≥ 1) 修 PRD → /scope-inject <id>
[2] (默认 if accumulated drift) 起新 forge → /expert-forge <id>
[3] 切到 XenoDev 改 spec → cd /Users/admin/codes/XenoDev
[4] 暂停 → 决议已 log,稍后再做

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4 or describe.
```

## After handback review

- **PRD revisions(M ≥ 1)** → `/scope-inject <id>` 或手工改 PRD,然后 `/plan-start <prd-fork-id>` 产新 hand-off 包
- **SHARED-CONTRACT 修订(K ≥ 1)** → 手工改 framework/SHARED-CONTRACT.md;若是 schema 级 change → bump contract_version + Changelog entry
- **XenoDev spec 修订(J ≥ 1)** → 跨仓 cd 改;XenoDev 自己 review loop 跑
- **累积 N ≥ 5 + 系统性 drift** → `/expert-forge <discussion-id>` 起新一轮 forge 重审 §6 协议或 PRD 整体

## Notes

- 本命令是 **hand-back consumer 入口**,不是 producer。Producer = XenoDev build runtime(per §6.3)。
- M2 阶段 6 约束是 **contract-only**(operator 手工核对);B2.1 阶段(XenoDev bootstrap)实装可调 validator(`lib/handback-validator.*`)。
- HANDBACK-LOG.md 是 **append-only**(per §6.4);Edit 时只追加新 entry + 更新 frontmatter `last_updated` / `total_decisions`,不删除既有 entry。
- 跨仓 audit trail:hand-back 包文件名 + frontmatter `handback_id` + path `<id>` 三处一致(约束 5);decision log 保留全 handback_id 便于追溯回 XenoDev 那边的 task。
- 与 forge / L1-L4 关系:hand-back **不**触发新 forge(单包决议级);hand-back **可**触发 PRD 修订(/scope-inject 或新 PRD 版本);累积 N + 系统性 → operator 决定起 forge v3。
