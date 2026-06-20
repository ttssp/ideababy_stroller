<!-- FROZEN SNAPSHOT · forge 008 v3 _external
     source_repo: /Users/admin/codes/XenoDev (git HEAD: 6f1a0df)
     source_file: framework/SHARED-CONTRACT.md §1+§2 (lines 29-282)
     snapshot_sha256(slice): 3fded6ca63a8afe22c4ca5cf0e9506b854ac4fce94471cc27d5380a416f4baaa
     snapshot_at: 2026-06-19T15:49:50Z
     reason: cross-repo target #3 · 被本议题挑战的硬约束(凭据隔离原则之源)
     ⚠ ORCHESTRATOR NOTE(给双专家的事实校正,非 binding 注入):
        K/backlog 把本议题的非可覆盖硬约束称作「§1+§2 凭据隔离 + 半自动采集原则」。
        实读:§1 = PRD schema(字段约定);§2 = Safety Floor 三件套(件1 production
        credential 物理隔离 / 件2 不可逆命令 hard block / 件3 备份破坏检测)。
        §2件1 是「凭据隔离」最接近的成文条款,但其 scope 是 .env.production / secrets/
        production/ / prod:// 这类【部署密钥不进 agent context】——并非字面写「顾问平台
        登录态 cookie 在采集翻页时不进 agent context」。亦即:K 里那条「登录态绝不进
        agent context」是 §2件1 在【采集域】的解读/外推,§1+§2 原文未字面覆盖采集会话凭据,
        更无「半自动采集原则」成文条款。**这道 written-constraint vs 实际诉求的落差本身
        是 v3 该解的题之一**(§2 措辞是否需扩展到采集会话凭据 · 见 K 第 3 点)。
-->

## §1 · PRD schema(plain markdown)

> **2026-05-08 v2 sanity check 修订**:本节明确 **PRD vs Spec 区分**,并修正 v1 的 cli 假设。
> **2026-05-08 v1.1 修订**:删除"`make sdd-init` / `make decompose`"误标(audit 实证 ADP Makefile 无此 target);改为 ADP 真实入口 `.claude/skills/sdd-workflow/` + `.claude/skills/task-decomposer/` 两个 skill。

### §1 字段约定(v1.1 新增)

本节描述的是 **IDS PRD schema**(8 字段:frontmatter + 7 markdown 节)。
ADP spec.md 是 **不同 schema**(7 元素 + frontmatter,schema_version: 0.2)。
两者**不是同一文件**;PRD → spec 转换由 operator 人工完成(ADP sdd-workflow skill 不接受 PRD 文件作为输入,只接受 short feature description),见 §3 Hand-off 协议。

### PRD vs Spec(SDLC 不同阶段,不同产物)

ideababy_stroller(IDS)产出的是 **PRD**;autodev_pipe(ADP)消费的是 **它自己的 spec**(v3.2/v3.3/v4 schema 0.2 的 7 元素 spec.template.md)。**两者不是同一文件**:

| 阶段 | 产物 | 仓库 | Schema | 入口 |
|---|---|---|---|---|
| L3 Scope(IDS) | PRD-v\<n\>.md(本节定义,8 字段) | ideababy_stroller | 本节 §1 | `/scope-start` 命令 |
| L4 Plan(IDS) | spec.md / architecture.md / tasks/T\*.md / HANDOFF.md | ideababy_stroller | (IDS L4 规范) | `/plan-start` 命令 |
| Build(ADP) | autodev_pipe 自己的 spec.md(7 元素) | autodev_pipe | ADP `templates/spec.template.md`(schema_version 0.2) | `.claude/skills/sdd-workflow/SKILL.md` skill(operator 在 ADP Claude Code session 触发) |
| Build(ADP) | autodev_pipe `tasks/T*.md`(9 字段 frontmatter) | autodev_pipe | (ADP task-decomposer 规范) | `.claude/skills/task-decomposer/SKILL.md` skill |

**关键澄清(v1.1 修订前 v1 的错误假设)**:
- ❌ v1 假设有 `autodev_pipe-cli build` 命令直接消费 PRD — **该命令不存在**
- ❌ v1 假设 `make sdd-init <feature>` / `make decompose <spec>` 是 ADP 真实 Makefile target — **2026-05-08 v1.1 audit 实证:这两个 target 在 ADP Makefile 里 0 命中**(它们只是 v3.2 spec.md L31 outcome 描述里的 example 字串,从未实装为 make target)
- ✅ 实际:ADP 真实入口是 **skill 调用,非 Makefile target** — `.claude/skills/sdd-workflow/SKILL.md`(spec init)+ `.claude/skills/task-decomposer/SKILL.md`(task 分解);两个 skill 都是 stroller-port 来的,在 ADP Claude Code session 里 operator 主动触发
- ✅ 跨仓 hand-off **不是 IDS PRD 直送 ADP cli**,而是:**IDS PRD → operator 切到 ADP 仓库 → operator 人工把 PRD §"User persona"+§"Core user stories" 提炼为短 feature description 喂 sdd-workflow skill → sdd-workflow 产出 ADP spec.md 7 元素骨架 → operator 按 §3 Schema 转换表把 PRD 内容填入对应节 → 触发 task-decomposer skill 产 task → parallel-builder 跑 task**
- ✅ ADP 的 spec 7 元素与本节 PRD 8 字段是**不同 schema**(PRD 在前,Spec 在后,SDLC 经典分阶段)
- ✅ **ADP sdd-workflow skill 不接受 PRD 文件作为输入,只接受 short feature description** — 因此 PRD → spec 之间**必须有 operator 人工转写步骤**(不是 cp,不是 import,不是脚本一键转换)

### 设计原则

- PRD 是 plain markdown 文件,**不是任何 DSL / YAML / JSON / 自定义格式**
- 这样保证跨 IDE / 跨 agent / 人类可直接编辑
- 字段顺序固定,但允许扩展子节(以下 8 字段必须存在)
- **PRD 是 ADP spec 的输入,但 ADP spec 自有 schema(7 元素 + Production Path Verification),IDS 不规定 ADP spec 内部结构**

### Schema(8 个 required 字段)

```markdown
# PRD · <name>

**PRD-form**: simple | phased | composite | v1-direct
**Status**: draft | reviewed | approved | superseded
**Sources**: <upstream stage doc path(s) — comma-separated if multiple>(L3 candidate / forge stage / direct bootstrap)
**Forked-from**: <parent PRD or "root">

## User persona

<one paragraph: 用户是谁,他们的能力 / 角色 / 真实约束>

## Core user stories

- 作为 <persona>, 我 <do X>, 因为 <reason Y>
- ...

## Scope IN

<bullet list: 必须做的事>

## Scope OUT(显式 non-goals)

- **NOT** <explicit exclusion>(evidence: <source>)
- ...

## Success looks like

<量化 / 可证伪的成功标准 — 必须 falsifiable,不允许 "用户满意 / 系统稳定" 这类不可证伪表述>

## Real constraints

- **时间**: ...
- **预算**: ...
- **平台**: ...
- **合规**: ...

## UX principles(optional but recommended)

- ...

## Open questions(forge / scope 阶段未解决的)

- **OQ1**: ...
- ...
```

### Example

参见 `discussion/006/forge/v1/stage-forge-006-v1.md` §4(Next-version PRD draft)是符合本 schema 的完整 example。

### Required vs Optional

| 字段 | required? | 说明 |
|---|---|---|
| frontmatter (PRD-form / Status / Sources / Forked-from) | required | operator 切到 ADP 时,用此 frontmatter 判断 PRD 适用形态(simple / phased / composite / v1-direct)→ 决定是否需要拆多个 ADP feature(eg composite PRD 的多 module → 多次触发 ADP `.claude/skills/sdd-workflow/`) |
| User persona | required | 没有 persona 的 PRD 不可执行 |
| Core user stories | required | 至少 3 条 |
| Scope IN | required | |
| Scope OUT | required | 必须显式列出 |
| Success looks like | required | 必须 falsifiable |
| Real constraints | required | |
| UX principles | optional | 中型项目以上推荐 |
| Open questions | optional | 但建议有(诚实优于完美) |

### 客观依据

- **plain markdown 是 LF AAIF 跨 agent 标准**(2025) — AGENTS.md 也是 plain markdown
- **idea_gamma2 interface-contract 五元组借鉴**(producer/consumer/schema/version/error-handling) — 本节 schema 是 producer 端定义
- **Anthropic 2026 Trends "上游需求工程化"** 是 5 个核心 agentic coding 工作流之一 — PRD 必须是工程化产物,不是自由格式
- **stage-forge-006-v1.md §4** 已示范完整 PRD 结构
- **autodev_pipe v3.2 PD1**(spec/task 工具链 = stroller schema) — ADP 实际入口是 `.claude/skills/sdd-workflow/` + `.claude/skills/task-decomposer/` 两个 skill(2026-05-08 v1.1 audit 实证;Makefile 无 sdd-init / decompose target),**v1.1 修订采纳此事实**

### v2 → v1.1 修订记录(2026-05-08 两轮 sanity check)

| 修订点 | v1 描述 | v2 修订 | v1.1 进一步修订(本次) |
|---|---|---|---|
| ADP 入口命令 | 假设 `autodev_pipe-cli build` 存在 | 改为 `make sdd-init` / `make decompose`(误以为是 ADP v3.2 V1+V2 真 target) | **再修正**:audit 实证 Makefile 0 命中;真入口 = `.claude/skills/sdd-workflow/` + `.claude/skills/task-decomposer/` 两个 skill |
| PRD 与 Spec 关系 | 隐含为同一物 | 显式区分:PRD 在 IDS,spec 在 ADP,SDLC 不同阶段 | 不变 |
| Schema 单一性 | 隐含 PRD 直接喂给 build cli | 修正:PRD 是 ADP sdd-workflow skill 的输入 | **进一步**:sdd-workflow 不接受 PRD 文件,只接受 short feature description;PRD → feature description 是**operator 人工转写**步骤 |

---

## §2 · Safety Floor 三件套定义

> **2026-05-08 v2 sanity check 修订**:**SSOT 归属修正** — autodev_pipe 早于本 framework 文档存在,且已实装多层防御(`block-dangerous.sh` + `parallel-builder` 5 hard rule + `request-approval.sh` + `spec-validator`)。本节**不再要求 ADP "binding from IDS"**;改为:**IDS 这边声明上游一致性约束(写 PRD 时必须考虑这三件套),ADP 这边持续维护实装 SSOT**。
> **2026-05-08 v1.1 audit 修订**:跨仓 grep 实证 ADP `block-dangerous.sh` 23 条 dangerous pattern 现状,精确化件 1/件 2/件 3 的"已落地"vs"真 gap"分布。

### §2 ADP 实装现状(2026-05-08 audit 实证)

跨仓 grep 实证 `autodev_pipe/.claude/hooks/block-dangerous.sh` 内容(23 条 dangerous pattern):

- **件 1 production credential 物理隔离** — `grep "env\.production|env\.prod"` 命中 0;**真 gap,1-2 周(在 ADP 那边补)**
- **件 2 不可逆命令 hard block** — `block-dangerous.sh` 已覆盖:`rm -rf /` / `~` / `..` / `$HOME` / `*` / `git push --force.*main/master` / `git reset --hard.*origin` / `git clean -*f*d` / `DROP DATABASE` / `DROP TABLE` / `TRUNCATE TABLE` / `aws s3 rm.*--recursive.*production` / `aws s3 rb.*--force` / `kubectl delete namespace` / `terraform destroy` / fork bomb / `dd ... /dev/` / `mkfs.*` / `curl|bash` / `chmod -R 777 /`;**已落地**
- **件 3 备份破坏检测** — `grep "backup|备份"` 命中 0;**真 gap,与件 1 合并 1-2 周**

**3 个真 gap 全部归 ADP 范围**(IDS 阶段无运行时,无法实装 hard block);具体推迟到 ADP V4 dogfood checkpoint-01 出后(2026-06-03 ±)再启动。详见 `framework/ADP-AUDIT-2026-05-08.md`。

### 设计原则

Safety Floor 是 framework **不可妥协的硬约束**(NG-4):无论在 IDS 写 PRD 还是 ADP build 时,这三件套**必须 hard block**。

**SSOT 归属(v2 修订)**:
- **实装 SSOT 在 autodev_pipe**(因为 hard block 发生在运行时,只有 ADP 有运行时):`autodev_pipe/.claude/hooks/block-dangerous.sh` + `autodev_pipe/.claude/agents/parallel-builder.md` 5 hard rule + `autodev_pipe/scripts/spec_validator.py`
- **上游约束 SSOT 在 ideababy_stroller**(PRD 阶段必须考虑):本节定义 PRD 在写 Scope IN / Real constraints 时必须满足三件套**约束声明**(eg "本 PRD 不要求 production credential 直连");IDS 的 `framework/SHARED-CONTRACT.md` §2 是这一层的 SSOT
- **两层不同**:实装 SSOT 决定运行时阻断;上游约束 SSOT 决定 PRD 不允许提出违反三件套的需求

> **Why 双 SSOT 而非单一**:idea→PRD 阶段无运行时,只能"声明约束",没法 hard block;build 阶段有运行时,才能真正 hard block。把它们捏成一个 SSOT 会要么"PRD 阶段管不到运行时"要么"build 阶段不知道 PRD 上游约束"。本 framework 范式是**双层独立 SSOT,语义对齐**。

### 三件套清单

#### 件 1 · Production credential 物理隔离

**规则**:任何匹配以下 pattern 的文件**不得进入 agent context**:

- `.env.production` / `.env.prod` / `.env.live`
- `*-prod.env` / `*-production.env`
- `secrets/production/*` / `credentials/prod/*`
- 文件内容含 `prod://` / `production-` 前缀的 connection string
- 通过 GitHub Actions secrets 或 cloud KMS 注入的运行时凭据

**实现层**(在 autodev_pipe):
- file-system level deny list(在 agent tool 调用前 path filter)
- git pre-commit hook 检测 production 凭据 commit
- agent context loading 阶段二次检查(白名单 + 黑名单)

**Failure case 防御**:Cursor + Claude 9 秒删库案例(tomshardware 2025)— 生产凭据进入 agent context 是事故根源。

#### 件 2 · 不可逆命令 hard block

**规则**:agent 在任何 sandbox mode 下,执行以下命令**必须返回 hard block,不允许 prompt / config 覆写**:

```
# 文件系统不可逆
rm -rf /
rm -rf ~
rm -rf <root-level paths>

# 数据库不可逆
DROP TABLE <not-test-prefix>
DROP DATABASE
TRUNCATE <not-test-prefix>
DELETE FROM <not-test-prefix> WITHOUT WHERE

# Git 不可逆
git push --force <protected-branch>
git push --force-with-lease <protected-branch>(取决于配置)
git reset --hard origin/<protected>(在 protected branch 上)
git filter-branch / git filter-repo on shared history

# Cloud 不可逆
aws s3 rm --recursive <prod-bucket>
aws rds delete-db-instance / aws rds delete-db-cluster
gcloud sql instances delete <prod-instance>
DELETE / production-tier resources

# 证书 / Key 不可逆
revoke production cert / rotate prod key without backup
```

**Protected branch 默认列表**:`main` / `master` / `production` / `release-*` / `v*-stable`

**Test prefix 白名单**:`test_*` / `*_test` / `tmp_*` / `staging_*` / `dev_*`

**Escape hatch**:用户必须使用 `human escape hatch`(打字声明 + 二次确认)才能执行被 block 的命令——agent 自己不能调用任何 escape API。

#### 件 3 · 备份破坏检测

**规则**:任何场景下,**同一凭据 / 同一 API 不可同时拥有"删除主存储 + 删除备份存储"权限**。

> **B2.2 Block A.7 codex round 4 finding #3 状态降级**(2026-05-10):本节 normative 描述
> 是**协议层目标**;v0.1 实装是**子集**(本地 snapshot+diff,见
> `framework/xenodev-bootstrap-kit/safety-floor-3/`)。完整 IAM lint + cloud API interceptor
> 是 v0.2 trigger(operator 单人 + 本地 v0.1 阶段无 cloud,完整实装无收益;XenoDev 真用云时
> 必须升级)。AGENTS.md §1 第 3 条已同步此降级语言。

检测方式:

- 在 agent context loading 时,扫描凭据 scope(IAM policy / db role)
- 如果检测到一个凭据可同时操作 production storage + backup storage → hard block
- 如果检测到 agent 准备调用 backup deletion API(`aws backup delete-recovery-point` / `gcloud sql backups delete` 等) → hard block + escalate

**Failure case 防御**:Cursor + Claude 9 秒删库案例**核心创伤**——AI 通过同一 API 9 秒内删除主库 + 备份。如果有"凭据物理隔离主备"约束,事故不会发生。

**实现层**:
- v0.1 实装(单人本地 dev):filesystem snapshot+diff(`*.backup` / `*.bak` / `*.snapshot` + `.git/config` push policy + `.claude/settings.json` permissions.deny diff)— `framework/xenodev-bootstrap-kit/safety-floor-3/`
- v0.2 trigger(用云时):IAM policy linter(static analysis)+ runtime API call interceptor(hook on backup-related API)— per `safety-floor-3/README.md` OQ-backup-1
- 历史(autodev_pipe 范式):IAM policy linter + runtime API interceptor — 该 V4 范式未完整落地,XenoDev v0.2 重新设计

### 客观依据

- **Cursor + Claude 9 秒删库**(tomshardware 2025)— 三件套全部直接对应该案例的三个失败点
- **Codex CLI 三档 sandbox**(suggest / auto-edit / full-auto)— 工业范式,Safety Floor 在 full-auto 下仍 honor
- **AWS / GCP / Azure 共识**:production 凭据应通过 IAM least-privilege 设计,本文件把这条业界共识 hardcode 进 framework
- **OWASP Top 10 (2021/2024) A01 Broken Access Control**:Safety Floor 三件套是 access control 在 agentic coding 上下文的实例化

### autodev_pipe 实装现状(v2 修订:不再要求 binding,而是审计已落地)

autodev_pipe 已实装的 Safety Floor 多层防御(2026-05-08 核查):

| 件 | ADP 实装位置 | 实装状态 |
|---|---|---|
| 件 1 · Production credential 物理隔离 | (无显式实装) | **gap** — `block-dangerous.sh` 没扫 .env.production 模式;需补 |
| 件 2 · 不可逆命令 hard block | `autodev_pipe/.claude/hooks/block-dangerous.sh` | ✅ 已实装(`rm -rf` 类) |
| 件 2 (扩展) · 5 hard rule(file_domain 越界 / spec 漂移) | `autodev_pipe/.claude/agents/parallel-builder.md` | ✅ 已实装(v3.2 V3) |
| 件 3 · 备份破坏检测 | (无显式实装) | **gap** — 没有同凭据双 API 隔离机制;需补 |

**v2 修订采纳的事实**:autodev_pipe 实装比 v1 描述的更分散(hook + agent rule + spec validator 三层),件 1+件 3 是**真 gap**(sanity-check-v2 §3 模块 2 标的 80% 完成度的剩余 20%)。

**v1 假设的 binding 要求(已删除)**:不再要求 ADP AGENTS.md 加 "binding from ideababy_stroller" 段;ADP 自己维护实装 SSOT。
- 修订理由:ADP 早于本 framework 文档存在,要求它 binding 是 retroactive 倒置因果;且 ADP self-parasitic(它用自己的 spec 而非 IDS PRD 跑 dogfood),没有实质消费 IDS 的 SHARED-CONTRACT 内容
- 替代机制:**审计** — IDS 这边定期跑 sanity check 对照 ADP 实装,记录 gap(本节"实装现状"表 + sanity-check-v2)而非要求 binding

---

