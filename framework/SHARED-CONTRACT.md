---
doc_type: framework-shared-contract
contract_version: 2.2
status: v2.2
generated: 2026-05-08
last_updated: 2026-05-12
upstream: discussion/006/forge/v1/stage-forge-006-v1.md (v1) + discussion/006/forge/v2/stage-forge-006-v2.md (v2)
ssot_owner: ideababy_stroller
ssot_consumer: XenoDev (v2.0+, replaces autodev_pipe per M2 cutover)
purpose: 定义 ideababy_stroller (idea→PRD + 治理) 与 XenoDev (PRD→code build runtime) 跨仓接口
---

# SHARED-CONTRACT · ideababy_stroller ↔ autodev_pipe

## 本文档定位

ideababy_stroller(idea→PRD)与 autodev_pipe(PRD→code)是**两个独立 release 的仓库**(理由见 `NON-GOALS.md` NG-2 / NG-7)。两仓通过本文档定义的接口契约协调,**不通过版本号绑定**。

本文档是 **SSOT(Single Source of Truth)**:

- **ideababy_stroller 拥有 SSOT**(本文件)——所有变更必须先在这里发生
- **autodev_pipe 持有 mirror**(其仓库内 SHARED-CONTRACT.md 是字节级 cp)——变更跟随 SSOT
- 跨仓 mirror 范式参考:Linux kernel `include/uapi/` headers(kernel 是 SSOT,libc 持 mirror)

> **Why explicit contract**:Newman *Building Microservices* ch.7 Consumer-Driven Contracts:跨服务边界的不变量必须 binary 双向声明,否则集成时永远断。Pact framework 同样原则。Spotify Backstage 早期 / Uber Cadence 早期失败案例都源于"先写代码后定契约"。

---

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

## §3 · Hand-off 协议

> **2026-05-08 v2 sanity check 全节重写**:删除 `autodev_pipe-cli build` 假设(该命令不存在)。
> **2026-05-08 v1.1 修订**:进一步修正 — `make sdd-init` / `make decompose` 也不是真 Makefile target(audit 实证);ADP 真实入口是 `.claude/skills/sdd-workflow/` + `.claude/skills/task-decomposer/` 两个 skill,operator 在 ADP Claude Code session 触发。

### 设计原则

跨仓 hand-off 不是"IDS 直接调用 ADP cli";是**operator 切到 ADP 仓库,把 IDS 的 PRD 作为人工转写的源头,在 ADP 自己的 sdd-workflow skill 上跑**。

PRD 是上游产物;ADP 自己产 spec(7 元素 + Production Path Verification)是 build 阶段产物。**两阶段独立,不共享 schema**。

### Hand-off 数据流(v1.1 修订)

```
ideababy_stroller                              autodev_pipe (独立运作)
─────────────                              ──────────────
proposal.md
  ↓ /inspire-start
L1 stage doc
  ↓ /explore-start
L2 stage doc
  ↓ /scope-start
L3 stage doc → PRD-v<n>.md
  ↓ /plan-start
specs/<NNN>-<fork>-<prd>/
  ├── spec.md           (IDS 内部 spec, 给 IDS L4 用)
  ├── architecture.md
  ├── tasks/T001.md ... T0NN.md
  └── HANDOFF.md        (operator 读这份,人工切仓)
       │
       │ operator 读 HANDOFF.md 中给的 PRD 路径 + ADP-side 操作清单
       │ 切到 autodev_pipe 仓库
       ▼
                                          cd <autodev_pipe path>
                                          # operator 在 ADP Claude Code session 里触发 .claude/skills/sdd-workflow/SKILL.md
                                          # 输入 = operator 人工把 IDS PRD §"User persona" + §"Core user stories" 提炼为
                                          #         1-2 段 short feature description
                                          # (sdd-workflow 不接受 PRD 文件作为输入,只接受 short description)
                                          .claude/skills/sdd-workflow/  ← 真实入口(skill,非 Makefile target)
                                            ↓ 产出 specs/<feature>/spec.md (7 元素 schema, schema_version: 0.2,
                                            ↓                                reviewed-by: pending)
                                          # operator 按 §3 Schema 转换表把 PRD 内容填入 ADP spec 7 元素
                                          # operator 必须补 §7 Production Path Verification(IDS 不产出,见 step 4.5)
                                          # 触发 reviewed-by 走 v3.3 codex review:status: draft → review → frozen
                                          .claude/skills/task-decomposer/  ← 真实入口(skill)
                                            ↓ 产出 tasks/T*.md (9 字段 frontmatter)
                                          .claude/agents/parallel-builder      # v3.2 V3 跑 task
                                            ↓ + 5 hard rule + Safety Floor
                                          # 测试 + review (ADP v3.3 reviewed-by hook)
                                          # ship
```

### HANDOFF.md schema(v1.1 修订)

`/plan-start` 在 spec 目录下生成 `HANDOFF.md`,**为 operator 切仓后做事提供指引**(不是机器读的 cli 配置):

```markdown
# Hand-off · <NNN>-<fork>-<prd> → autodev_pipe

**Handed off at**: <ISO timestamp>
**IDS spec path**: <absolute path>/specs/<NNN>-<fork>-<prd>/
**PRD source**: <absolute path>/discussion/<NNN>/<fork>/<prd>/PRD.md
**ADP repo path** (operator 自填): <autodev_pipe absolute path,默认 /Users/admin/codes/autodev_pipe>
**SHARED-CONTRACT version honored**: 1.1.0

> **v2.0 cutover 后(M2,2026-05-10)**:本 §3 schema 是 v1.1 历史 active 描述(IDS → ADP 流程)。v2.0 后 forward hand-off 由 plan-start v3.0 产 `discussion/<id>/<prd>/L4/HANDOFF.md`(目标仓改为 XenoDev),frontmatter 必加 §6.2 `workspace:` 块 + 下方 §3.1 `source_repo_identity:` 块。详见 §6 + Changelog v2.0。

### §3.1 · source_repo_identity 字段(v2.0 新增,forward hand-off frontmatter)

> **v2.0 新增**(M2 cutover,Block E)。响应 codex Round 4 (HEAD~6) Finding 2 — v1.1 `to_source_repo: <absolute path>` 不构成可校验的仓 identity,producer 实装无 ground truth → 退化成"`.git` 存在 = PASS"的弱 check,IDS 副本 / test clone 全通过。v2.0 加本字段提供可校验的 normative ground truth。

由 IDS forward hand-off producer(`/plan-start` v3.0)产源时填入,XenoDev hand-back producer 写包前按 §6.2.1 约束 3 三模式比对。

**字段结构**(YAML,嵌入 hand-off 包 frontmatter):

```yaml
source_repo_identity:
  expected_remote_url: <git remote.origin.url 输出;无 remote 时留空字符串>
  repo_marker: <head -c 30 CLAUDE.md 输出;MUST contain "Idea Incubator">
  git_common_dir_hash: <可选;sha256 of .git/HEAD + .git/config 前 16 字符>
```

**三个字段的产生命令**(IDS forward 端):

```bash
EXPECTED_REMOTE="$(git config remote.origin.url 2>/dev/null || echo '')"
REPO_MARKER="$(head -c 30 CLAUDE.md)"
GIT_HASH="$(cat .git/HEAD .git/config 2>/dev/null | shasum -a 256 | head -c 16)"
```

**约束 3 三模式比对规则**(per §6.2.1 约束 3,v2.0 normative spec):

- **remote 模式**(producer 端有 git remote):
  - 比对 `git config remote.origin.url` ∈ source_repo == `expected_remote_url`(精确字符串等)
  - PASS = 字面相等(包括 `git@` vs `https://` 等同 host 也算 PASS — 加 normalize:strip protocol prefix + trailing `.git`)
  - 失败 = 当前仓不是 hand-off 包预期的仓(IDS 副本 / test clone / 误移动)
- **no-remote 模式**(producer 端无 git remote,或 hand-off 包 expected_remote_url 为空):
  - 比对 `head -c 30 CLAUDE.md` ∈ source_repo 含 `repo_marker` 子串
  - `repo_marker` 必含 "Idea Incubator"(IDS CLAUDE.md L1 永久标识)
  - PASS = 子串匹配
  - 第一性原因:`single-developer / local-only` 场景无 remote 是常态;repo_marker 提供 fallback ground truth
- **hash-only 模式**(operator 显式开启;两个 repo 是 fork 关系无法靠 remote 区分):
  - 比对 `sha256(.git/HEAD + .git/config)` ∈ source_repo 前 16 字符 == `git_common_dir_hash`
  - PASS = hash 等
  - 适用场景:operator 在同 host 跑 IDS prod + IDS test clone,两者 remote 相同但 .git/HEAD(branch)+ .git/config(local user.name/email)总有差异

**fail-closed 优先级链**(B2.2 Block A.6 codex round 3 finding #2 修订;旧版"任一 PASS"已废弃):
- 若 `expected_remote_url` 非空 → **锁定** remote 模式;mismatch 直接 FAIL,**不允许** fall through 到 no-remote / hash-only(防同 marker 冒充)
- 若 `expected_remote_url` 空 + `repo_marker` 非空 → no-remote 模式;**额外要求** source_repo 也真无 origin remote(防 downgrade attack:有 remote 但故意填空 expected)
- 若 `expected_remote_url` + `repo_marker` 都空 + `git_common_dir_hash` 非空 → hash-only 模式
- 三字段全空 → FAIL(无 ground truth)

**为什么 fail-closed 而非 OR**(第一性论证):
- 旧 OR 模型下,攻击者只要保留 IDS CLAUDE.md 前 30 字 header 就能在任意 fork 通过 no-remote 模式(remote 不同也无所谓)→ 与 no-remote fallback 的设计意图("真无 remote 时才用 marker")相违
- fail-closed 保证 producer 一旦 declared 用 remote 模式(填 expected_remote_url),consumer 必须强制走 remote 比对;marker / hash 仅作 producer declared 的 fallback,不作"任一通过即可"的逃生口

**hard-fail 行为**(per §6.2.1 约束 4):优先级链锁定的模式 FAIL → producer 不写 hand-back 包 / consumer 不读 hand-back 包,只 stderr 报具体模式失败原因 + handback_id + exit 非 0。

**实装位置**(本协议 + 命令实装):
- 协议层(本节):normative spec(M2 Block E 落地)
- IDS 端 producer(forward hand-off):`/plan-start` v3.0 frontmatter 已填(M2 Block A2 落地,见 .claude/commands/plan-start.md)
- XenoDev 端 producer(hand-back):B2.1 阶段实装(XenoDev bootstrap)
- IDS 端 consumer(hand-back review):`/handback-review` v2.0 contract-only 引(M2 Block D 落地);可调 validator B2.1 阶段实装

**与 v1.1.0 §3 关系**:v1.1.0 §3 HANDOFF.md schema 不含 `source_repo_identity` 字段;v2.0 加本字段是 forward direction adapter,IDS forward hand-off frontmatter 必填,XenoDev hand-back producer 必读必校验。v1.1.0 历史 hand-off 包(specs/{007a-pA, 001-pA, 003-pA, 004-pB}/HANDOFF.md)是 ADP 范式,M3 已标 DEPRECATED,不需追溯加本字段。

## Operator manual steps(切仓后)

1. cd <ADP repo path>
2. 阅读 IDS PRD 与 IDS spec:
   - cat <PRD source>
   - cat <IDS spec path>/spec.md
3. 在 ADP 起新 feature(真实入口 = skill,不是 Makefile target):
   - 在 ADP Claude Code session 里,触发 `.claude/skills/sdd-workflow/SKILL.md`
   - **operator 必须人工转写**:把 IDS PRD §"User persona" + §"Core user stories" 提炼为 1-2 段 short feature description 作为 sdd-workflow input
4. sdd-workflow 产出 specs/<feature>/spec.md(7 元素骨架,schema_version: 0.2,reviewed-by: pending)后,operator 按下表强制项填入:
   - 详见 §3"Schema 转换"表(下方)
   - **§4 Prior Decisions / §5 Task Breakdown** 两节 ADP 必填但 IDS PRD 不含,operator 必须从 IDS L4 spec.md 对应字段补
   - **§7 Production Path Verification** 是 ADP v3.3 起的强制元素,**IDS 不产出**(IDS 阶段无真路径);见 step 4.5
   - **OQ 字段双路分流**(v1.1 决议 1):IDS PRD §"Open questions" 中**关于 constraint 数字**的(eg "QPS 上限 TBD")→ 进 ADP spec §3 Constraints 末尾 "Open" 小节(C-OQ-1, C-OQ-2);**关于 build 路径选择**的(eg "用 lib X 还是 Y")→ 不进 ADP spec,留在本 HANDOFF.md §"Open questions for build phase"
4.5. **operator 在 ADP 写 §7 Production Path Verification**(v1.1 决议 2):
   - **IDS 不产出 §7**(IDS 阶段无真路径,强写是占位文字反而误导)
   - 参考样本:`<ADP repo>/specs/v3.3/spec.md` §7 真路径 P1-P4 example
   - 模板:`<ADP repo>/templates/spec.template.md` §7 骨架
   - 最小要求:列至少 1 条 P_i 描述"真路径起点 → 终点 + 必经环节 + 可执行验证命令"
   - 失败模式:不写或只写 mock-pass-prod-fail 的样本 → ADP `scripts/spec_validator.py` reject + status 无法转 frozen
   - 第一性原因:所有 mock-pass-prod-fail 都因为 mock 满足 spec 真路径不满足(灵感来源 stroller idea004 12 routes 404 失败案例)
5. 在 ADP 跑 reviewed-by:
   - frontmatter `reviewed-by: pending` → 触发 ADP `/codex:adversarial-review` 或 plugin 路径
   - review 通过 → frontmatter 改 `reviewed-by: codex`(或 gpt-5.5 / gemini)
   - status: draft → review → frozen
6. 任务分解(ADP 这边的 task-decomposer skill,不复用 IDS task DAG):
   - 在 ADP Claude Code session 里触发 `.claude/skills/task-decomposer/SKILL.md`
   - 产出 specs/<feature>/tasks/T*.md(9 字段 frontmatter)
7. parallel-builder 跑 task(走 ADP 5 hard rule + Safety Floor)
8. ship 走 ADP 自己规则(不回 IDS)

## Schema 转换(IDS PRD 8 字段 → ADP spec 7 元素 + frontmatter,v1.1 修订)

| IDS PRD 字段 | ADP spec 节 | 强制? |
|---|---|---|
| frontmatter (PRD-form / Status / Sources / Forked-from) | spec.md frontmatter (`spec_id` / `status: draft` / `schema_version: 0.2` / `reviewed-by: pending`) | 强制 |
| User persona + Core user stories | §1 Outcomes(每个 story → O1/O2/... ID) | 强制 |
| Scope IN | §2.1 Scope IN | 强制 |
| Scope OUT | §2.2 Scope OUT | 强制 |
| Real constraints | §3 Constraints(C1, C2, ... 数字化) | 强制 |
| (IDS PRD 没有,operator 须补) | §4 Prior Decisions(PD1, PD2, ... 引用源) | 强制 |
| (高层 phase 由 IDS spec.md 承担,IDS PRD 不含) | §5 Task Breakdown(高层 phase + 依赖) | 强制 |
| Success looks like | §6 Verification Criteria(每条 V_n 可执行 shell) | 强制 |
| (IDS 不产出,operator 在 ADP 阶段补) | §7 Production Path Verification | **强制(v3.3 起)** |
| Open questions(关于 constraint 数字的) | §3 Constraints 末尾 "Open" 小节(C-OQ-1, C-OQ-2, ...) | 可选(spec_validator 帮逼解决) |
| Open questions(关于 build 路径选择的) | **不进 ADP spec**,留在 HANDOFF.md §"Open questions for build phase" | 可选 |

## ADP-side prerequisites(operator 切仓前自查)

- ADP 仓库为 v3.2+ (含 `.claude/skills/sdd-workflow/` + `.claude/skills/task-decomposer/` skill)
- ADP `make doctor` exit 0(`pyproject.toml` deps 装齐)
- ADP `pre-commit install` 已跑(spec-validator + check-spec-review + check-constraint-references hooks 装齐)
- **operator 已读 ADP `templates/spec.template.md` §7 + `specs/v3.3/spec.md` §7 真实样本**(为 step 4.5 写 §7 PPV 做准备)
- ADP V4 dogfood 状态:**首次切仓前确认 V4 checkpoint-01 已出**(2026-06-03 ±);切仓时机过早会污染 dogfood signal(ADR 0008 D2)

## Open questions for build phase

(IDS PRD 中**关于 build 路径选择**的 OQ 在此承载;ADP build 自然遇到时再解决,不污染 ADP spec frozen)

## Rollback plan

如果 ADP build 失败:
- (a) 回到 IDS 修 PRD,重跑 /plan-start
- (b) 改 ADP spec(不改 IDS PRD),用 ADP 自己的 W-* 修订机制
- (c) 起 forge v2 重新审整个 idea
```

### Implementation status (2026-05-08 v1.1 修订)

✅ **HANDOFF.md schema 已重写为 operator-readable 格式**(不再依赖不存在的 `autodev_pipe-cli build`,也不再误标 `make sdd-init` / `make decompose`)。

✅ **`/plan-start` 命令产出 HANDOFF.md 已实装**(v1.1) — 见 `.claude/commands/plan-start.md` Step 5.5。

### 客观依据

- **autodev_pipe v3.2 PD1**(spec/task 工具链 = stroller schema) — ADP 实际入口是 `.claude/skills/sdd-workflow/` + `.claude/skills/task-decomposer/`(2026-05-08 v1.1 audit 实证;Makefile 无 sdd-init / decompose target),**v1.1 修订采纳此事实**
- **autodev_pipe v3.3 7 元素 spec schema**(含 Production Path Verification) — ADP spec 与 IDS PRD 是不同 schema 的事实根据
- **stroller idea004 12 路由 404 失败案例** — Production Path Verification 第 7 元素的设计动机
- **OQ 双路分流第一性原理** — IDS PRD OQ 是"未决但仍推进"(idea 阶段允许);ADP spec 是"全部已决才 frozen"(build 阶段不允许);两者本质矛盾不能合一
- **§7 PPV 归属第一性原理** — IDS 阶段无真路径,无法产出真 §7;若 IDS 强行写,内容是占位文字反而误导(违反 verdict "诚实优于夸大"哲学)
- **机器告诉机器**:GitHub Actions / GitLab CI / Backstage 范式
- **rollback plan**:Forsgren 2018 *Accelerate*

---

## §4 · 版本演化机制

### 设计原则

SHARED-CONTRACT 的演化遵循 idea_gamma2 breaking-change 三阶段流程(此处是 Pattern 借鉴,非 Component 复用)。

### 三阶段流程

#### 阶段 1 · Deprecation 通告(announce 期 ≥ 4 周)

发起方:ideababy_stroller(SSOT 拥有方)
动作:
- 在 `framework/SHARED-CONTRACT.md` 加 deprecation 标记 + ISO 日期
- 在 `framework/CHANGELOG.md` 写新版本草案
- 通知 autodev_pipe 仓库通过 PR 或 issue
- **旧 schema 必须仍然工作**——autodev_pipe 此期间不需要立刻动

#### 阶段 2 · Migration 期(coexist 期 ≥ 4 周)

ideababy_stroller 与 autodev_pipe 同时支持新旧 schema:
- ideababy_stroller `/plan-start` 输出可选新 schema 字段(向后兼容)
- autodev_pipe 解析时同时支持两种(带 fallback)
- 此期间 autodev_pipe 升级到支持新 schema 的版本

#### 阶段 3 · Cutover(切换 ≥ 1 周通知)

- ideababy_stroller 移除旧 schema 支持
- autodev_pipe 必须已升级
- `framework/CHANGELOG.md` 记录 breaking change 完成日期

### Schema 版本号

SHARED-CONTRACT 的 frontmatter 含 `contract_version: <semver>`(本文件 v1):

- Major bump(2.0):breaking change(走三阶段流程)
- Minor bump(1.1):新增 optional 字段(向后兼容)
- Patch bump(1.0.1):文档澄清 / typo

### autodev_pipe 的协调义务

- autodev_pipe 仓库 AGENTS.md 必须显式声明支持的 contract_version 区间
- autodev_pipe 解析 PRD 时,必须读取 PRD frontmatter 的 `contract_version`(若有)
- 不支持的 contract_version → autodev_pipe 应明确报错,而非"尽力解析"

### 客观依据

- **idea_gamma2 breaking-change 三阶段已 30 天稳定运行** — Pattern 借鉴
- **semver 是事实标准** — npm / pip / cargo 等生态共识
- **Linux kernel 与 glibc 协调范式**:30 年 ABI 演化,deprecation period 通常 ≥ 1 年
- **Pact framework 默认配置**:contract testing 不要求双方版本同步,但要求双方明确声明支持区间

---

## §5 · interface-contract 五元组

### 设计原则

跨仓边界的每个不变量必须以五元组形式声明,确保 producer / consumer / schema / version / error-handling 都明确。借鉴 idea_gamma2 CONSTITUTION 的 interface-contract 五元组(已 30 天稳定运行,Pattern 级借鉴)。

### 五元组模板

每个跨仓不变量声明如下:

```markdown
### Interface · <name>

- **Producer**: <仓库 / 命令 / 文件>(谁产生这个不变量)
- **Consumer**: <仓库 / 命令 / 文件>(谁消费这个不变量)
- **Schema**: <格式定义 / 字段清单>
- **Version**: <contract_version 或 "follows shared-contract">
- **Error-handling**: <consumer 在 schema 不匹配时的行为>
```

### 当前所有 interface 清单(应用五元组)

#### Interface 1 · PRD document

- **Producer**: ideababy_stroller `/plan-start` 命令(产出 PRD + HANDOFF.md)
- **Consumer**: autodev_pipe operator(读 HANDOFF.md 后,在 ADP Claude Code session 触发 `.claude/skills/sdd-workflow/SKILL.md` skill,人工把 PRD 转写为 short feature description 喂 skill)
- **Schema**: 本文件 §1(PRD 8 字段)+ §3(HANDOFF.md schema + 转换表)
- **Version**: follows shared-contract v1.1
- **Error-handling**: PRD 缺 required 字段时,operator 在 ADP 转写阶段会缺源数据,应回到 IDS 修 PRD 重跑 `/plan-start`,而非"尽力转写"

#### Interface 2 · Safety Floor 双层 SSOT(v1.1 修订)

- **Producer**: ideababy_stroller `framework/SHARED-CONTRACT.md` §2(上游约束 SSOT — PRD 阶段必须考虑)
- **Producer (peer)**: autodev_pipe `.claude/hooks/block-dangerous.sh` + `.claude/agents/parallel-builder.md` 5 hard rule + `scripts/spec_validator.py`(实装 SSOT — 运行时阻断)
- **Consumer**: 两个 SSOT 互为参考,**不要求 ADP "binding from IDS"**(v2 修订撤回);IDS 这边定期跑 sanity check 对照 ADP 实装记录 gap
- **Schema**: §2 三件套清单 + 实装现状审计表
- **Version**: follows shared-contract v1.1
- **Error-handling**: ADP 运行时若发现违反三件套的命令 → hard block(由 ADP 实装层处理);IDS 这边发现 PRD 提出违反三件套的需求 → operator 回头改 PRD

#### Interface 3 · Hand-off document

- **Producer**: ideababy_stroller `/plan-start` 命令(产出 HANDOFF.md)
- **Consumer**: 用户(读 HANDOFF.md,在 autodev_pipe 跑命令)
- **Schema**: §3 HANDOFF.md schema
- **Version**: follows shared-contract v1
- **Error-handling**: 用户/autodev_pipe 在 HANDOFF.md 缺关键字段时,应回到 ideababy_stroller 重新跑 `/plan-start`

#### Interface 4 · Schema versioning

- **Producer**: ideababy_stroller `framework/SHARED-CONTRACT.md` frontmatter `contract_version`
- **Consumer**: autodev_pipe AGENTS.md `supported_contract_versions` 字段
- **Schema**: semver 区间表达
- **Version**: meta-level(描述自己)
- **Error-handling**: contract_version 不在 supported 区间 → autodev_pipe 拒绝运行 + 提示用户升级

### 客观依据

- **idea_gamma2 五元组已运行 30 天** — Pattern 级借鉴(非 Component cp)
- **OpenAPI / Swagger 范式同样要求 producer/consumer 明确**(虽然格式更结构化,精神一致)
- **Pact framework "states + interactions + matchers"** 模型与五元组同构

---

## §6 · v2.0 ACTIVE(workspace schema + hand-back 通道)

**Status**: ACTIVE
**Cutover landed**: M2 commit · 2026-05-10
**Promoted to ACTIVE**: B2.2 commit(本 commit)· 2026-05-11 · operator subjective score 7.6/10 (38/50)
  - per `discussion/006/b2-2/B2-2-RETROSPECTIVE.md` · plan rosy-naur v11 Block G
  - hand-back round-trip 实证:1 real PRD ship (006a-pM) · 3 task ship (FU-001 + T001 + FU-002) · 5 hand-back packs · 4 codex round adversarial 加固(round 2-5)+ 1 IDS validator real-data fix(check-5 regex commit a57972a)
  - 5 维度评分:可读 8 / 错误信息 8 / 跨仓 friction 7 / false positive 7 / 闭环 8
**依据**: forge 006 v2 verdict — `discussion/006/forge/v2/stage-forge-006-v2.md` §"Evidence map" row 11(hand-back 包结构化)+ row 12(workspace schema 4 字段)+ §"Refactor plan(W3)" 模块 A step 1 + 模块 C 全节;codex Round 4 (HEAD~6) Finding 2 → §3.1 source_repo_identity 字段 + §6.2.1 约束 3 三模式 normative 比对(M2 Block E)

> **v2.0 ACTIVE-but-not-battle-tested 含义**(M2 cutover 决策):
> - **协议层 ACTIVE**:本节(§6)所有 normative spec 已生效,IDS 工作流(plan-start v3.0 / handback-review)按本节实装
> - **跨仓闭环未实战**:hand-back 通道在 IDS 端 contract-only(M2),producer 端 validator 待 B2.1(XenoDev bootstrap)实装,首个真 hand-back round-trip 待 B2.2
> - **跳过 R5 决策**:用 B2.2 实跑代替纸面 review 收敛(per plan-rosy-naur v8/v9);若 B2.2 暴露 §6 结构性问题 → 起 forge v3,Status 不改 ACTIVE
> - **当前 consumer**:`/plan-start` v3.0 + `/handback-review` v2.0 + `framework/AUTODEV-PIPE-SYNC-PROPOSAL.md`(historical,pre-M2 不动);v1.1.0 历史 hand-off 包(specs/{007a-pA, 001-pA, 003-pA, 004-pB}/HANDOFF.md)是 ADP 范式,M3 已标 DEPRECATED

### §6.1 · v2.0 motivation

forge 006 v2 verdict 中心命题(GPT P2 §1 row 5 headline):**"目标方向没错,但 gap 是 harness 产品化,不是再补一份流程文档"**。SOTA 共同方向(Anthropic Agent SDK + Skills / Cursor 3 multi-root + worktrees / Spec Kit 0.8.7 spec-first / MSR 2026 失败实证)全部指向**运行时 harness + 4-phase + 跨仓 workspace + 可观测 + 可学习**。

v2.0 协议升级回应 2 件 SOTA gap:
1. **跨仓 workspace 一等建模**(Cursor multi-root 范式)— v1.1.0 hand-off 是单向 IDS → ADP 切仓人工转写,无 workspace 概念;Cursor 3.2 changelog 把 async subagents / worktrees / multi-root workspace 合在一个 agent window,跨 repo change 是 SOTA 一等能力。ADP-AUDIT §9 DRIFT-4 emergent `working_repo` 字段是该 schema 缺失的实证信号。
2. **反向 hand-back 学习闭环**(MSR 2026 agentic PR failure corpus 共识)— v1.1.0 单向 hand-off 后 IDS 收不到 build 反馈,无法学习 PRD 哪些约束在 build 时不可达;33k agent PR 失败研究表明,无 hand-back 通道 = 重复犯同类 PRD-spec mismatch。

### §6.2 · workspace schema 4 字段

跨仓 build 上下文显式建模。**4 字段全必填**(避免 v1.1.0 隐式假设单仓的同类问题)。

| 字段 | 类型 | 必填 | 含义 | 用例 |
|---|---|---|---|---|
| `source_repo` | string (absolute path) | ✅ | PRD 源仓(IDS 仓路径) | `/Users/admin/codes/ideababy_stroller` |
| `build_repo` | string (absolute path) | ✅ | build 目标仓(XenoDev 仓路径) | `/Users/admin/codes/XenoDev` |
| `working_repo` | string (absolute path) | ✅ | 当前 operator 所在仓(支持单 session 跨多仓 workspace) | 通常 = `source_repo` 或 `build_repo`;hand-off 中途切仓时显式记录 |
| `handback_target` | string (absolute path) | ✅ | hand-back 包写回路径 | `<source_repo>/discussion/<id>/handback/` |

YAML 表达(出现在 hand-off 包 / hand-back 包 frontmatter 中):

```yaml
workspace:
  source_repo: /Users/admin/codes/ideababy_stroller
  build_repo: /Users/admin/codes/XenoDev
  working_repo: /Users/admin/codes/XenoDev
  handback_target: /Users/admin/codes/ideababy_stroller/discussion/008/handback/
```

#### §6.2.1 · handback_target 路径约束(consumer 必须校验)

> **本子节是 normative constraints,非 convention**。任何 hand-back 包 producer(build runtime,如 XenoDev)与 consumer(`/handback-review` 命令)实装时,**必须**对 `handback_target` 执行下列校验,任一失败即 **hard-fail**(拒绝写入 / 拒绝读取 / 不进行任何 retry)。

**约束 1 · canonical-path containment**:
- `realpath(handback_target)` 必须严格落在 `realpath(source_repo) + "/discussion/" + <id> + "/handback/"` 之下(包含正好等于该目录)。
- "严格落在之下"含义:resolve symlink 后做 prefix 比较,字符串前缀匹配 + 边界字符为 `/` 或字符串末尾。
- 失败模式:`handback_target = "/tmp/whatever"` / `handback_target = "<source_repo>/../other-repo/..."` / `handback_target = "<source_repo>/discussion/006/handback/../../specs/..."` 三种典型 path traversal 全部 reject。

**约束 2 · symlink reject**:
- `handback_target` 路径上的任意一段(从 `source_repo` 起到目标目录止)若是 symlink,**reject**(不要 follow,不要 resolve 后通过校验)。
- 第一性原因:symlink 是 confused-deputy 攻击的经典载体;single-developer / local-only 场景看似无威胁,但 operator 自己手动建过的 dev symlink(eg `~/codes/ideababy_stroller -> ~/Dropbox/...`)会让 fs.write 静默落到 Dropbox,Dropbox 的 sync conflict resolver 可能覆盖 append-only 评审产物。
- 例外:**operator 在 IDS 仓根本身**(`source_repo`)可以是 symlink(operator 的 dev workflow 决定);校验从 `source_repo`(canonicalized 后)往下走,只校验 `<source_repo>/discussion/...` 这部分路径段不含 symlink。

**约束 3 · repo identity check(v2.0 normative · fail-closed 优先级链)**:
- 写入前 producer 必须按 hand-off 包 frontmatter `source_repo_identity:` 字段(§3.1)按 fail-closed 优先级链比对:
  - `expected_remote_url` 非空 → **锁定 remote 模式**;mismatch FAIL,不允许 fall through
  - `expected_remote_url` 空 + `repo_marker` 非空 → no-remote 模式;额外要求 source_repo 也无 origin remote(防 downgrade)
  - 仅 `git_common_dir_hash` 非空 → hash-only 模式
  - 三字段全空 → FAIL(无 ground truth)
- 完整规则、产生命令、字段语义、攻击场景论证见 §3.1。
- 失败 = `source_repo` 指向了一个看起来像 IDS 仓但其实是别人的 fork / 误移动的副本 / IDS 副本 / test clone,**reject**(per 约束 4 hard-fail)。
- v1.1.0 弱实装(`.git` 存在 = PASS)在 v2.0 已废弃;v2.0 早期"任一模式 PASS"已在 B2.2 Block A.6 改 fail-closed 优先级链(codex round 3 finding #2)。

**约束 5 · id consistency check**:
- hand-back 包必须满足 **三处 id 严格一致**:
  1. 物理路径中 `discussion/<X>/handback/` 的 `<X>` 段
  2. 文件名 `<ISO ts>-<handback_id>.md` 中 `handback_id` 解出的 `<prd_fork_id>` 前缀的 `discussion_id` 部分(`prd_fork_id` 形如 `008a-pA`,前缀 `008` = `discussion_id`)
  3. frontmatter `discussion_id` 字段 + `prd_fork_id` 字段 + `handback_id` derived 公式 (`<prd_fork_id>-<ts>`)
- 三处任一不匹配 = `Drop`(producer 不写 / consumer 不读)。
- 第一性原因:hand-back 是 IDS ↔ XenoDev 双向学习闭环的反馈源;若路径在容器内但 idea id 错位,`/handback-review <id>` 会把无关 build 证据当作 PRD `<id>` 反馈处理,驱动 PRD 做不该做的修订(corruption-of-corpus 失效模式)。Pact framework 风格 explicit contract(本文档开头已引 Newman 原则)要求 invariant 在协议层双向声明,producer 与 consumer 都按此实装。
- 失败模式典型场景:operator 在多 idea fork 间切换,XenoDev 跑 PRD 008a-pA 时 handback_target 误填 `discussion/006/handback/`;或自动化 script 把 `<id>` 参数化时变量串错。

**约束 6 · id 字符集 + final-path containment**:
- **id 字符集 regex**(producer 写入前 + consumer 读取前都必须校验):
  - `discussion_id` 必须匹配 `^[0-9]{3}$`(eg `008`)
  - `prd_fork_id` 必须匹配 `^[0-9]{3}[a-z]?(-p[A-Z])?$`(eg `008` / `008a` / `008a-pA`)
  - `<ISO ts>` 必须匹配 `^[0-9]{8}T[0-9]{6}Z$`(eg `20260520T103015Z`,UTC,无毫秒)
  - `handback_id` 必须严格等于 `<prd_fork_id> + "-" + <ISO ts>` 的拼接结果
  - 三个 id token 任意一处含 `/` `\` `..` 控制字符 (`\x00-\x1f\x7f`) 或绝对路径前缀 = `Drop`
- **filename basename 校验**(拼接后写入前):
  - 拼出的 `filename = "<ts>-<handback_id>.md"` 必须满足 `os.path.basename(filename) == filename`(自身不含任何 separator)
  - 失败 = `Drop`,不写入
- **final-path containment 二次校验**(写入前最后一道):
  - `realpath(target_dir + "/" + filename)` 必须严格落在 `realpath(source_repo) + "/discussion/" + discussion_id + "/handback/"` 之下(同约束 1 的 prefix 语义)
  - 失败 = `Drop`,不写入
- 第一性原因:约束 1 只校验 `handback_target` 这个**目录**字串,filename 是后置 derived 拼接;若 `prd_fork_id` 含 `/` 或 `..`,filename 会把目录 prefix 拆破 → 写入逃逸 `source_repo`(eg `prd_fork_id = "008a-pA/../../../etc/evil"` → 三处 id 一致 check 5 PASS,但 filename 拼出来逃逸目录)。OWASP path traversal 标准防御要求 input shape validation(字符集 regex)+ defense in depth(写入前最后一道 realpath containment),producer 与 consumer 都必须按此实装。
- 失败模式典型场景:shell `${var}` 未 quote 含空格 / unicode 反斜杠;XenoDev 自动化 script 把 git branch name / file path 当 `prd_fork_id` 来源;consumer 实装时自由解读 "id 应该长这样" 导致与 producer 行为分叉。

**约束 4 · hard-fail 行为**:
- 任一约束失败,producer **不写**任何文件,**不创建**任何目录,**不做** stderr 之外的副作用。
- consumer(`/handback-review`)读到不符合约束 1-3 + 5-6 的 hand-back 包,**不读取**其内容,只在 stderr 报具体哪条约束失败 + 该 hand-back 包的 `handback_id`,然后 exit 非 0。
- 第一性原因:hand-back 通道是跨仓写入,silent error 在跨仓场景下永远诊断不到;hard-fail 比 silent corruption 便宜两个数量级。

**约束实装位置**(M2 cutover 时):
- producer 校验:M2 新建 XenoDev 仓时,在产 hand-back 包的 skill / 命令实装(B2 范围)。
- consumer 校验:M2 新建 `.claude/commands/handback-review.md` 命令(§6.5 breaking change 清单条目)实装。
- 协议层(本节)只定义约束语义,具体校验代码由 M2 实装时落地。

**与 v1.1.0 §3 关系**:v1.1.0 §3 `HANDOFF.md` 隐式假设"operator 知道当前在哪个仓",从未显式记录;v2.0 显式 4 字段后,`HANDOFF.md` frontmatter 增加 `workspace:` 块,任意 agent 读 hand-off 包都能确认上下文(不靠 operator 记忆)。

### §6.3 · hand-back 包 schema

build 仓(XenoDev)在每个 task ship / spec violation / drift detection 时产 hand-back 包,写回 `source_repo`(IDS)的 `handback_target/`。

**frontmatter**(YAML):

```yaml
---
discussion_id: <id>                      # eg "008";必须与路径 discussion/<X>/ 中 <X> 严格一致(§6.2.1 约束 5)
prd_fork_id: <prd-fork-id>               # eg "008a-pA";discussion_id 之下的 fork 标识
handback_id: <prd_fork_id>-<ISO ts>      # eg "008a-pA-20260520T103015Z";derived = prd_fork_id + "-" + ts
from_build_repo: <absolute path>
to_source_repo: <absolute path>
workspace:                               # §6.2 4 字段嵌入
  source_repo: ...
  build_repo: ...
  working_repo: ...
  handback_target: ...
source_repo_identity:                    # §3.1 三字段嵌入(producer 必填,validator 按 §6.2.1 约束 3 三模式比对)
  expected_remote_url: <forward HANDOFF.md 透传>      # eg "git@github.com:ttssp/ideababy_stroller.git";remote 模式
  repo_marker: <forward HANDOFF.md 透传>              # eg "# Idea Incubator";no-remote 模式
  git_common_dir_hash: <forward HANDOFF.md 透传>      # eg "647b0db7b4d47318";hash-only 模式(可选)
tags:                                    # 三标签 enum,至少 1
  - drift                                # build 时发现 spec/PRD 与实际不符
  - prd-revision-trigger                 # PRD 某条约束需 IDS 修订才能继续
  - practice-stats                       # 跑完 N task 的成功率/干预率统计
severity: low | medium | high            # high = 阻断 build / medium = 可继续但需 IDS 关注 / low = 信息式
created: <ISO>
related_task: <task id, optional>        # eg "T013"
related_spec_section: <spec section anchor, optional>
---
```

> **producer 写入 frontmatter 前**,必须按 §6.2.1 六条约束(canonical-path containment / symlink reject / repo identity check / id consistency / id 字符集 + final-path containment / hard-fail)校验路径与 id;校验失败 hard-fail,不产 hand-back 包。
>
> **`source_repo_identity` 来源**:由 forward HANDOFF.md(IDS `/plan-start` v3.0 产)透传 — XenoDev producer 不自行计算,直接 cp HANDOFF.md frontmatter 同名块写入。这样 reverse trip 自带身份证明,与 forward 包解耦(forward 包写后可被改),同时与 §6.2 workspace 块"每个跨仓包自带"原则对齐。

**body 章节**(Markdown,**3 节 normative + 4 节 RECOMMENDED** · 共 ≤ 7 节):

```markdown
## §1 · Build-side 上下文(发生了什么)   [normative]

哪个 task / 哪个文件 / 哪段 spec / 哪条 PRD outcome 触发了本 hand-back。
最少 50 字,最多 500 字。引具体 file:line 或 task ID。

## §2 · 触发理由(三标签对应描述)        [normative]

按 frontmatter `tags` 列出的标签逐条说明:
- 若有 `drift`:具体 drift 描述(预期 vs 实际)+ 证据(测试输出 / log)
- 若有 `prd-revision-trigger`:PRD 哪条 outcome / scope / constraint 不可达 + 建议修订方向
- 若有 `practice-stats`:统计区间 + 数字(eg "T001-T013 共 13 task,intervention 5 次,平均 22min/task,2 task hit Safety Floor")

## §3 · 给 IDS 的建议                    [normative + RECOMMENDED 扩展]

[normative · operator 决议输入] operator 收到本 hand-back 后可选的动作(选 1-N):
- [ ] 修 PRD §"<section>"(具体改动建议)
- [ ] 修 SHARED-CONTRACT §"<section>"(若是协议级 drift)
- [ ] 修 XenoDev spec(本仓内,不需 IDS 介入,本 hand-back 仅信息式)
- [ ] 无操作(收悉,作为 practice-stats 入库)

[RECOMMENDED · v2.2 加 · producer-side Suggested actions]
producer 可在 normative checkbox **之前** / **之上**额外列 markdown 表格(5 列),
给 operator 决议提供 actionable list 与 rationale:

| # | Action | 类型 | 优先级 | 备注 |
|---|---|---|---|---|
| A1 | <具体 action 描述> | review / doc / hotfix-task / skill-patch / arch / doc-cleanup / no-op | high / medium / low | <evidence + 估时 + commit hash> |

reference 实例:F1a / F1b / T010 三包(IDS commit `8d24851` / `162bcf6` / `d4d04e7`)
皆 producer 自发出 5 列表格 · 与 normative checkbox 并存不冲突。

## §4 · PRD-revision-trigger 检查         [RECOMMENDED · v2.2 加]

producer 主动逐项 check 本次 ship 是否触发 PRD revision · 列出结论 + 理由:
- O1-O9 outcomes 改动?(是 / 否)
- phase target 改动?(是 / 否)
- D-spec-1..D-spec-N 改动?(是 / 否)
- 红线 §R-1..R-N 触动?(是 / 否)

reference 实例:F1a / F1b / T010 三包 §4 段实证。producer 主动自检可减
轻 IDS operator 决议负担(v0.2-retro.md §3.4 producer 主动自检模式)。

## §5 · 后续 task 建议                    [RECOMMENDED · v2.2 加]

若本 task ship 后 unblock 其他 task / 触发新 task / 标 hotfix:
列举 task id + 估时 + recommended_model + 入度变化(DAG 影响)。

reference 实例:F1b 包 §5 列出 T010/T020/T024 三 lane unblock + T013 推荐 + v0.1 product bug 2 个 hotfix。

## §6 · File changes(本 task)            [RECOMMENDED · v2.2 加]

列 squash commit hash + 新增 / 修改文件清单(行数 stats)+ verification
PASS 项目数。

reference 实例:F1a / F1b / T010 三包 §6 段(squash commit `e555241` /
`1055aae` / `db09f00`)。

## §7 · 已知风险 / known gotchas         [RECOMMENDED · v2.2 加]

ship 后已知但本 scope 不修的风险(下次 ship 或 follow-up task 时重看):
- 风险描述 + 显形条件 + 建议修复路径 + scope 范围(本 task / 下 task / v0.2 / v0.3)

reference 实例:F1a 3 条 / F1b 5 条 / T010 7 条 · 累积演化 evidence。
```

**版本与回溯**:
- v2.0:body 章节 normative 3 节(§1 / §2 / §3)· 见 v2.0 ACTIVE entry(2026-05-11)
- v2.2(2026-05-12):§3 加 producer-side 表格 RECOMMENDED 扩展 · 新增 §4 / §5 / §6 / §7 四节 RECOMMENDED 占位 · 老 3 节 normative 不变 · v2.0 producer 0 backfill 要求(只 forward apply)。Evidence:F1a / F1b / T010 三包 producer 自发实践。

### §6.4 · hand-back 接收路径约定

**IDS 端目录**:`<source_repo>/discussion/<id>/handback/`

**文件命名**:`<ISO ts>-<handback_id>.md`(eg `20260520T103015Z-008a-pA-20260520T103015Z.md` — ts 重复以便 ls 排序与 frontmatter 匹配)

**id 一致性**:文件名中 `handback_id` 解出的 `<discussion_id>` 前缀必须与物理路径 `discussion/<X>/` 的 `<X>` 严格相等,且与 frontmatter `discussion_id` 字段相等;否则 `/handback-review` hard-fail(§6.2.1 约束 5)。

**字符集与 final-path**:`discussion_id` / `prd_fork_id` / `<ISO ts>` / `handback_id` 必须匹配 §6.2.1 约束 6 定义的安全 regex(reject `/` `\` `..` 控制字符 绝对路径);拼出的 `<filename>` 必须自身不含 separator;`realpath(目录 + "/" + 文件)` 写入前必须再做一次 prefix 校验(防 `prd_fork_id` 含 `/..` 时 filename 把目录 prefix 拆破而逃逸 source_repo)。

**operator 操作**:在 IDS 仓运行 `/handback-review <id>`(M2 同期产命令)读 `discussion/<id>/handback/` 目录,逐条决议 §3 建议清单,写入 `discussion/<id>/handback/HANDBACK-LOG.md`(append-only 决议日志)。

#### §6.4.1 · Step 5 闭环责任分担(v2.2 加 · 防 XenoDev session 误判)

hand-back round-trip 是**异步两段闭环**,两段责任主体不同:

| 阶段 | 责任主体 | 完成判据 | 不闭环影响 |
|---|---|---|---|
| **同步段:producer 写回** | XenoDev session | producer validator(`--mode=producer`)PASS + 文件落到 `<source_repo>/discussion/<id>/handback/<file>.md` | XenoDev session 不能关 |
| **异步段:consumer 决议** | IDS session(operator 任意时机) | `/handback-review <id>` 跑完 + HANDBACK-LOG.md append entry + IDS commit | 决议延后不阻 XenoDev session 关闭 |

**关键**:XenoDev session 闭环责任**仅到文件写回** · 不等 IDS 决议。IDS `/handback-review` 是 operator 异步责任 · 可分钟级、天级、甚至跨 session(B + A 真并行模式下常见)。

**Evidence**:B2.2 RETRO §4.2 deviation — XenoDev session 误以为"等 IDS /handback-review 才算 Step 5 完成",实际同步段 ≠ 异步段。v2.2 codify 此分担,producer / consumer 各按自己段判定闭环。

**与 forge / L1-L4 关系**:
- hand-back **不**触发新 forge run(不是重大架构转向);
- hand-back **可**触发 PRD 修订(走 `/scope-inject` 或新 PRD 版本);
- hand-back 累积 N 条且呈现系统性 drift → operator 决定起 forge v3。

### §6.5 · v1.1.0 → v2.0 breaking change 清单(供 M2/M3 cutover 勾选)

cutover 时按此清单逐条勾选,确保所有 v1.1.0 consumer 同步迁移:

- [x] M2 改 `.claude/commands/plan-start.md` L140 1 处 frontmatter `SHARED-CONTRACT version honored: 1.1.0` → `2.0`(实证后修正:v8 plan 写"L140 / L194 / L225 三处"是错的,L194/L225 是文字引用 + 验证 grep,L127/L333 也是引用,真"version honored"字段只 L140 一处;A2 重写时所有 5 处都需同步改)— **M2 Block A2 落地**(commit bb188d9):plan-start 重写 v2.2 → v3.0,frontmatter `shared_contract_version_honored: 2.0`
- [x] M2 改 `.claude/commands/plan-start.md` Step 5.5 HANDOFF.md 模板 frontmatter 增加 `workspace:` 块(§6.2 4 字段)— **M2 Block A2 落地**(commit bb188d9):新 Step 3 frontmatter 含 `workspace:` 4 字段 + `source_repo_identity:` 3 字段
- [x] M2 改 `.claude/commands/plan-start.md` Step 5 不再产 `specs/<prd-fork-id>/` 完整 SDD 包(spec/architecture/tasks/SLA/etc),改为只产 hand-off 包(`discussion/<id>/<prd>/L4/HANDOFF.md` + 引用 §6.3 schema)。**实证修正**:plan-start.md 引 `specs/` 20+ 处(Step 3 mkdir / Step 4 spec-writer / Step 5 task-decomposer / Step 5.5 HANDOFF / Step 6 Codex review 全依赖),Block A 实际是 plan-start.md 几乎重写 ~200 行,非 5 行 fix — **M2 Block A2 落地**(commit bb188d9):plan-start 391 行 → 238 行(净 -153),specs/<prd-fork-id> 引用 0,只产 discussion/<id>/<prd>/L4/HANDOFF.md
- [x] M2 改 `CLAUDE.md` L25 `L4 · Plan      — spec, architecture, tasks, parallel build, quality gates` → `L4 · Hand-off    — produce hand-off package; downstream build runtime (XenoDev) does spec/tasks/build/quality` — **M2 Block B 落地**(commit 2744354)
- [x] M2 改 `CLAUDE.md` §"Directory ownership" 移除 `specs/NNN-<fork-id>-<prd>/` 行(IDS 不再产)— **M2 Block B 落地**(commit 2744354):微调 vs plan v9 — 保留 specs/NNN- 行但加 DEPRECATED 标注指向 commit d3194a0,audit trail 更完整
- [x] M2 改 `AGENTS.md` §4/§5 旧命令(若有引用 plan-start 产 specs/ 的描述)— **M2 Block C 落地**(commit 6722c8f):autodev_pipe 字串 8 处 → 0 处;XenoDev 出现 13 处;§4 Hand-off 段加 hand-back 行;§5 流图加 hand-back 行;`No code without a spec` → `No code without a hand-off package`;Specs immutable 段加 M3 archived 注
- [x] M2 新建 `.claude/commands/handback-review.md` 命令(§6.4 operator 操作入口)— **M2 Block D 落地**(commit b78ea5e):201 行命令骨架,6 个 Step,frontmatter argument-hint <discussion-id>,§6.2.1 6 约束全引为 normative source(M2 contract-only;B2.1 实装 validator 代码),Step 5 HANDBACK-LOG.md append-only 决议日志
- [x] M3 给 `specs/007a-pA/` 顶部加 `NOTICE.md` 或在 `spec.md` 顶部加段(标 DEPRECATED;保留 spec.md / tasks/ / HANDOFF.md 全部内容作 forge v2 evidence row 13 引用对象;新 PRD 不再走 IDS specs/)— **M3 已落地**(commit d3194a0,2026-05-10):spec.md 顶部加段(non-NOTICE.md 路线,1 处而非 2 处)
- [x] M3 给同级 `specs/{001-pA, 003-pA, 004-pB}/` 同样加 NOTICE(已 ship 的历史 fork,不再维护新 task)— **M3 已落地**(同 commit d3194a0):4 个 fork(007a-pA / 001-pA / 003-pA / 004-pB)spec.md 顶部各 +8 行 DEPRECATED 段
- [x] M2 cutover commit 同步 bump frontmatter `contract_version: 1.1.0` → `2.0` — **M2 Block F+G 落地**(本 commit):cutover sealing
- [x] M2 cutover commit 同步追加 §"Changelog" v2.0 entry(列本节所有 breaking change)— **M2 Block F+G 落地**(本 commit):cutover sealing
- [x] M2 cutover commit 同步在本节(§6)顶部把 `Status: DRAFT-pending-cutover` 改为 `Status: ACTIVE`,删除 v1.1 inactive warning 段 — **M2 Block F+G 落地**(本 commit):**改为中间态 `ACTIVE-but-not-battle-tested`** 而非直接 ACTIVE,留 B2.2 实跑 hand-back 闭环成功 + operator 主观评分 ≥ 7/10 后单独 1 commit 改 ACTIVE。理由:跳过 R5 = 用 B2.2 实跑代替纸面审查(per plan-rosy-naur v8/v9 决策),中间态防 Status = ACTIVE 后 B2.2 暴露 §6 结构性问题需改 ACTIVE 字段才能 fix 的心理摩擦
- [x] M2 改 §3 forward hand-off schema 加 `source_repo_identity` 字段(`expected_remote_url` + `repo_marker` + 可选 `git_common_dir_hash`),由 IDS forward 产源时填入;§6.2.1 约束 3 同步改为用该字段做 normative 比对(替代当前依赖 producer 自查 `remote.origin.url` 但无 expected 值的弱实装);定义 remote / no-remote / hash-only 三种比对规则。**第一性原因**:回应 codex Round 4 (HEAD~6) Finding 2 — 当前 `to_source_repo: <absolute path>` 不构成可校验的仓 identity,producer 实装无 ground truth → 退化成 `.git` 存在 = PASS 的弱 check,IDS 副本 / test clone 全通过 — **M2 Block E 落地**(commit pending),§3.1 新增,§6.2.1 约束 3 改 normative

### §6.6 · 与 §3 现有 hand-off 协议的关系

§3(v1.1.0)规定 IDS → ADP **单向** hand-off(operator 切仓人工转写)。§6 v2.0 **不删** §3,而是:

- **§3 forward hand-off 继续存在**:producer/consumer 改为 IDS → XenoDev(仓名变,流程不变 — operator 仍切仓,XenoDev 仍跑 sdd-workflow / task-decomposer);M2 cutover 时 §3 内容只需把 "autodev_pipe" 字面替换为 "XenoDev",HANDOFF.md frontmatter 增加 §6.2 workspace 块
- **§6 reverse hand-back 新增**:producer/consumer 为 XenoDev → IDS,通过 §6.3 schema + §6.4 路径约定流转

forward(§3)+ reverse(§6)形成双向闭环 — 这是 forge 006 v2 verdict 的核心 binding(P3R2 双方完全合一,见 stage doc §"Evidence map" row 11)。

---

## 验证

```bash
# §1-§5 active top-level 节必须齐全(用 awk 在 §6.x 子节出现前数,
# 否则 §6.3 hand-back body 模板里的 ## §1/§2/§3 会被误命中)
test -f framework/SHARED-CONTRACT.md
awk '/^### §6\./{exit} /^## §[1-5]/{c++} END{print c}' framework/SHARED-CONTRACT.md  # 应返回 5

# §1 PRD schema 必须含 example reference
grep -c 'discussion/006/forge/v1/stage-forge-006-v1.md.*§4' framework/SHARED-CONTRACT.md

# §2 Safety Floor 三件套必须列全
grep -c '^#### 件 [123]' framework/SHARED-CONTRACT.md  # 应返回 3

# §3 hand-off 必须引用 ADP 真实 skill 入口(非已删除的 cli/make target 假设)
grep -cE 'sdd-workflow|task-decomposer' framework/SHARED-CONTRACT.md  # 应 ≥4

# §4 三阶段必须列出
grep -c '^#### 阶段 [123]' framework/SHARED-CONTRACT.md  # 应返回 3
```

---

## Changelog

- **2026-05-12 v2.2 (件 2.5 + 件 2.2 合 · F6 + F2)**:§6.3 hand-back schema 加 §3 producer-side Suggested actions 表格 RECOMMENDED + §4-§7 四节 RECOMMENDED 占位(PRD-revision-trigger 检查 / 后续 task 建议 / File changes / 已知风险);§6.4.1 加 Step 5 闭环责任分担段(XenoDev 同步段 + IDS 异步段)。**非 BREAKING**(老 3 节 normative 不变;v2.0 producer 0 backfill 要求 · 只 forward apply)。Evidence:F1a / F1b / T010 三包(IDS commit `8d24851` / `162bcf6` / `d4d04e7`)producer 自发实践 + B2.2 RETRO §4.2 闭环责任 deviation。上游:plan-rosy-naur v12 B 件 2 / plan v0.2-global 件 2.5 + 件 2.2 / v0.2-retro.md §3.4。
- **2026-05-11 v2.0 ACTIVE (B2.2 Block G cutover sealing)**:§6 Status `ACTIVE-but-not-battle-tested` → `ACTIVE`;frontmatter `v2_status_note` 删除。依据:B2.2 hand-back round-trip 实跑评分 7.6/10(≥ 7/10 阈值,plan rosy-naur v11 决策门槛)— 1 real PRD (006a-pM) · 3 task ship · 5 hand-back packs round-trip · 1 IDS validator fix(check-5 regex 接受相对路径 commit a57972a)· 0 false negative · 1 false positive(已 fix)。详见 `discussion/006/b2-2/B2-2-RETROSPECTIVE.md`(38/50 评分 + 7 项 deviation + F1-F5 v0.2 trigger 入队)。非 BREAKING(纯 status 升级,协议层 0 字节修改)。
- **2026-05-10 v2.0 patch (B2.2 Block A.7 codex round 4 finding #3)**:§2 件 3 备份破坏检测加 v0.1/v0.2 状态标注 — declared 协议(IAM lint + runtime API interceptor)与 v0.1 实装(本地 snapshot+diff)不一致;本 patch 不删 normative 目标,加显式 v0.1 子集说明 + v0.2 trigger 说明。AGENTS.md §1 第 3 条 + xenodev-bootstrap-kit/CLAUDE.md 同步降级语言。非 BREAKING(v0.1 范围内无变化,只把已发生的实装状态写入文档)。
- **2026-05-10 v2.0 patch (B2.2 Block A.7 codex round 4 finding #4)**:check-3-repo-identity.sh no-remote 模式加 marker 强度校验 — 长度 ≥ 10 + 必含 "Idea Incubator"。修复 §3.1 normative ("marker 必含 Idea Incubator")与实装的不一致 — 旧版 `repo_marker: "I"`(1 字符)+ CLAUDE.md 含 I 即 PASS。新加 5 测试 case(3 攻击 + 2 合法),test 总数 13 → 18。
- **2026-05-10 v2.0 patch (B2.2 Block A.6 codex round 3 finding #2)**:§3.1 + §6.2.1 约束 3 由 "任一模式 PASS" 改 fail-closed 优先级链 — `expected_remote_url` 非空 → 锁定 remote 模式;空 + marker 非空 → 要求 source_repo 也无 origin remote(防 downgrade);防同 marker 冒充攻击。check-3-repo-identity.sh 同步重写 + 加 4 攻击场景测试(remote-mismatch+marker-match / downgrade / 都无 remote 合法 / 三字段全空)。**语义 BREAKING**:之前合法的"remote 不匹配但 marker 匹配 → PASS"现在 FAIL;但 plan-start v3.0 producer 一直 fill 三字段 + valid fixture 走 marker 模式(remote 留空)→ 实战 producer 实装无 break。
- **2026-05-10 v2.0 patch (B2.2 Block A.5 codex finding #4)**:§6.3 hand-back schema 加 `source_repo_identity:` 块(三字段),与 §6.2 workspace 块对齐;增加 producer 来源说明(forward HANDOFF.md 透传)。修复 contract 与 validator + valid fixture 的隐式漂移 — 之前 producer 按 §6.3 schema 写漏 identity 块 → check-3 必拒;按 fixture 写则成"undocumented schema drift"。本 patch 不改 §6.2.1 约束 3 行为,只把已发生的实装写进 schema。非 BREAKING(producer 实装本就携带,fixture 已含)。
- **2026-05-10 v2.0 (BREAKING · M2 cutover)**:contract_version 1.1.0 → 2.0,§6 cutover from DRAFT-pending-cutover → ACTIVE-but-not-battle-tested。
  Breaking changes(7 个 commit:850dd8f / bb188d9 / 2744354 / 6722c8f / b78ea5e / c73febb / 本 commit):
  - **plan-start v2.2 → v3.0**(commit bb188d9):IDS 不再产 specs/(spec-writer / task-decomposer / Codex review 全删除);只产 `discussion/<id>/<prd>/L4/HANDOFF.md`;frontmatter 加 `workspace:` 块(§6.2 4 字段)+ `source_repo_identity:` 块(§3.1 3 字段);391 行 → 238 行(净 -153)
  - **CLAUDE.md L4 重定义**(commit 2744354):L4 · Plan → L4 · Hand-off(spec/tasks/build/quality 移交 XenoDev);Directory ownership 加 HANDOFF.md entry;specs/NNN- 标 DEPRECATED 指向 commit d3194a0
  - **AGENTS.md autodev_pipe → XenoDev**(commit 6722c8f):8 处替换 + §4 加 hand-back 行 + §5 流图加 hand-back 行;`No code without a spec` → `No code without a hand-off package`;Specs immutable 加 M3 archived 注;字串 8 处 → 0 处,XenoDev 出现 13 处
  - **新建 .claude/commands/handback-review.md**(commit b78ea5e):201 行命令骨架,6 个 Step,§6.2.1 6 约束全引为 normative source(M2 contract-only;B2.1 实装 validator);Step 5 HANDBACK-LOG.md append-only 决议日志
  - **§3 加 §3.1 source_repo_identity 字段**(commit c73febb):replaces v1.1 weak `.git`-存在 = PASS check(响应 codex Round 4 Finding 2);3 字段 + 三模式比对规则(remote / no-remote / hash-only);§6.2.1 约束 3 改 normative 比对
  - **§6.5 13 项 cutover 清单全勾**(本 commit):M3 commit d3194a0 / M2 6 commit 全 attestation
  - **§6 Status 中间态**(本 commit):用 `ACTIVE-but-not-battle-tested` 而非直接 ACTIVE;留 B2.2 first hand-back round-trip 实跑评分 ≥ 7/10 后单独 1 commit 改 ACTIVE(替代纸面 R5 review,见 plan-rosy-naur v8/v9 决策)
  - **frontmatter bump**(本 commit):contract_version 1.1.0 → 2.0;status v1.1 → v2.0;ssot_consumer autodev_pipe → XenoDev;upstream 加 forge v2;加 last_updated / v2_status_note
  Migration impact:
  - **不影响 v1.1.0 active 段 §1-§5**:v1.1.0 段保留作 historical reference / audit trail evidence;autodev_pipe 字串 ~30 处不批量替换(破坏审计 evidence);新工作流走 §6 v2.0 + §3.1
  - **specs/ 4 个 fork**(M3 commit d3194a0 已 archived):spec.md 顶部 DEPRECATED 段;不再加 task / review;保留作 forge v2 evidence row 13
  - **未 push 任何 commit**:per ~/.claude/CLAUDE.md "push 前需我确认";operator 决定何时 push
- 2026-05-08 v1: 初稿,5 节(PRD schema / Safety Floor / Hand-off / 版本演化 / 五元组)
- 2026-05-08 v2 sanity check: 修订 §1/§2/§3(删除 `autodev_pipe-cli build` 假设 / SSOT 归属修正 / SYNC-PROPOSAL 整体方向逆转)
- 2026-05-08 v1.1: contract_version 1.0.0 → 1.1.0(minor,向后兼容)。基于 `framework/ADP-AUDIT-2026-05-08.md` 跨仓 grep 实证,进一步修正:
  - §3 数据流图 + HANDOFF.md schema:`make sdd-init` / `make decompose` 也不是真 Makefile target(audit 实证 0 命中);改为 ADP 真实 skill 入口 `.claude/skills/sdd-workflow/` + `.claude/skills/task-decomposer/`
  - §3 HANDOFF.md schema 加两决议:决议 1 OQ 字段双路分流(constraint OQ 进 §3 / build OQ 留 HANDOFF) + 决议 2 §7 PPV 归属 ADP(IDS 不越界产出)
  - §5 Interface 1 删 `autodev_pipe-cli build` 字串 + Interface 2 改双层 SSOT 描述
  - §1 加字段约定段 + §2 加 ADP 实装现状段(audit 实证件 1/件 3 真 gap,件 2 已落地)
