---
doc_type: framework-shared-contract
contract_version: 1.0.0
status: v1
generated: 2026-05-08
upstream: discussion/006/forge/v1/stage-forge-006-v1.md
ssot_owner: ideababy_stroller
ssot_consumer: autodev_pipe
purpose: 定义 ideababy_stroller (idea→PRD) 与 autodev_pipe (PRD→code) 跨仓接口
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

### PRD vs Spec(SDLC 不同阶段,不同产物)

ideababy_stroller(IDS)产出的是 **PRD**;autodev_pipe(ADP)消费的是 **它自己的 spec**(v3.2/v3.3/v4 schema 0.2 的 7 元素 spec.template.md)。**两者不是同一文件**:

| 阶段 | 产物 | 仓库 | Schema | 入口命令 |
|---|---|---|---|---|
| L3 Scope(IDS) | PRD-v\<n\>.md(本节定义,8 字段) | ideababy_stroller | 本节 §1 | `/scope-start` |
| L4 Plan(IDS) | spec.md / architecture.md / tasks/T\*.md | ideababy_stroller | (IDS L4 规范) | `/plan-start` |
| Build(ADP) | autodev_pipe 自己的 spec.md(7 元素) | autodev_pipe | ADP `templates/spec.template.md`(schema_version 0.2) | `make sdd-init <feature>` 或 `make decompose <spec>`(ADP v3.2 V1+V2) |

**关键澄清(v2 修订前 v1 的错误假设)**:
- ❌ v1 假设有 `autodev_pipe-cli build` 命令直接消费 PRD — **该命令不存在**
- ✅ 实际:ADP 入口是 `make sdd-init` / `make decompose`(stroller-port 的 sdd-workflow / task-decomposer skill 实现)
- ✅ 跨仓 hand-off **不是 IDS PRD 直送 ADP cli**,而是:**IDS PRD → operator 切到 ADP 仓库 → 在 ADP 那边用 sdd-workflow skill 把 PRD 转成 ADP spec → 跑 make decompose 产 task**
- ✅ ADP 的 spec 7 元素与本节 PRD 8 字段是**不同 schema**(PRD 在前,Spec 在后,SDLC 经典分阶段)

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
| frontmatter (PRD-form / Status / Sources / Forked-from) | required | operator 切到 ADP 时,用此 frontmatter 判断 PRD 适用形态(simple / phased / composite / v1-direct)→ 选 ADP `make sdd-init` 还是 `make decompose` 等不同入口 |
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
- **autodev_pipe v3.2 PD1**(spec/task 工具链 = stroller schema) — ADP 实际入口是 `make sdd-init` / `make decompose`,**v2 修订采纳此事实**

### v2 修订记录(2026-05-08 sanity check)

| 修订点 | v1 描述 | v2 修订 |
|---|---|---|
| ADP 入口命令 | 假设 `autodev_pipe-cli build` 存在 | 实际是 `make sdd-init` / `make decompose`(ADP v3.2 V1+V2) |
| PRD 与 Spec 关系 | 隐含为同一物 | 显式区分:PRD 在 IDS,spec 在 ADP,SDLC 不同阶段 |
| Schema 单一性 | 隐含 PRD 直接喂给 build cli | 修正:PRD 是 ADP sdd-workflow skill 的输入,不是 ADP build worker 的输入 |

---

## §2 · Safety Floor 三件套定义

> **2026-05-08 v2 sanity check 修订**:**SSOT 归属修正** — autodev_pipe 早于本 framework 文档存在,且已实装多层防御(`block-dangerous.sh` + `parallel-builder` 5 hard rule + `request-approval.sh` + `spec-validator`)。本节**不再要求 ADP "binding from IDS"**;改为:**IDS 这边声明上游一致性约束(写 PRD 时必须考虑这三件套),ADP 这边持续维护实装 SSOT**。

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

**规则**:任何场景下,**同一凭据 / 同一 API 不可同时拥有"删除主存储 + 删除备份存储"权限**。检测方式:

- 在 agent context loading 时,扫描凭据 scope(IAM policy / db role)
- 如果检测到一个凭据可同时操作 production storage + backup storage → hard block
- 如果检测到 agent 准备调用 backup deletion API(`aws backup delete-recovery-point` / `gcloud sql backups delete` 等) → hard block + escalate

**Failure case 防御**:Cursor + Claude 9 秒删库案例**核心创伤**——AI 通过同一 API 9 秒内删除主库 + 备份。如果有"凭据物理隔离主备"约束,事故不会发生。

**实现层**(在 autodev_pipe):
- IAM policy linter(static analysis 阶段)
- runtime API call interceptor(hook on backup-related API)

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

> **2026-05-08 v2 sanity check 全节重写**:删除 `autodev_pipe-cli build` 假设(该命令不存在);改为基于 ADP v3.2/v3.3/v4 真实入口(`make sdd-init` / `make decompose`)的 hand-off 流程。

### 设计原则

跨仓 hand-off 不是"IDS 直接调用 ADP cli";是**operator 切到 ADP 仓库,把 IDS 的 PRD 作为输入,在 ADP 自己的 sdd-workflow skill 上跑**。

PRD 是上游产物;ADP 自己产 spec(7 元素 + Production Path Verification)是 build 阶段产物。**两阶段独立,不共享 schema**。

### Hand-off 数据流(v2 修订)

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
       │ operator 读 HANDOFF.md 中给的 PRD 路径 + 推荐 ADP 命令
       │ 切到 autodev_pipe 仓库
       ▼
                                          cd <autodev_pipe path>
                                          # operator 把 PRD 内容 cp 进 ADP 的 sdd-workflow 输入位置
                                          # 或: 让 ADP sdd-workflow skill 直接读 IDS PRD 路径
                                          make sdd-init <feature>      # ADP v3.2 V1 入口
                                            ↓ 产出 ADP 自己的 spec.md (7 元素 schema)
                                          make decompose <spec>        # ADP v3.2 V2 入口
                                            ↓ 产出 ADP tasks/T*.md
                                          .claude/agents/parallel-builder      # ADP v3.2 V3 跑 task
                                            ↓ + 5 hard rule + Safety Floor
                                          # 测试 + review (ADP v3.3 reviewed-by hook)
                                          # ship
```

### HANDOFF.md schema(v2 修订)

`/plan-start` 在 spec 目录下生成 `HANDOFF.md`,**为 operator 切仓后做事提供指引**(不是机器读的 cli 配置):

```markdown
# Hand-off · <NNN>-<fork>-<prd> → autodev_pipe

**Handed off at**: <ISO timestamp>
**IDS spec path**: <absolute path>/specs/<NNN>-<fork>-<prd>/
**PRD source**: <absolute path>/discussion/<NNN>/<fork>/<prd>/PRD.md
**ADP repo path** (operator 自填): <autodev_pipe absolute path>

## Operator manual steps(切仓后)

1. cd <autodev_pipe path>
2. 阅读 IDS PRD: cat <PRD source>
3. 在 ADP 这边起新 feature:
   make sdd-init <feature-name>     # 产出 ADP 自己的 spec.md (7 元素)
4. 把 IDS PRD 内容**人工转写**进 ADP spec.md 的 §1 Outcomes / §2 Scope / §3 Constraints
   (PRD 8 字段 → ADP spec 7 元素:Outcomes / Scope / Constraints / Prior Decisions / Tasks / Verification / Production Path Verification)
5. ADP spec frontmatter 加 reviewed-by 走 v3.3 codex review 路径(若需要)
6. 任务分解: make decompose specs/<feature>/spec.md
7. parallel-builder 跑 tasks
8. ship 流程按 ADP 自己规则

## Schema 转换(IDS PRD 8 字段 → ADP spec 7 元素)

| IDS PRD 字段 | ADP spec 7 元素映射 |
|---|---|
| User persona + Core user stories | §1 Outcomes(每个 story → outcome ID) |
| Scope IN | §2 Scope IN |
| Scope OUT | §2 Scope OUT |
| Real constraints | §3 Constraints(数字,不是形容词) |
| Success looks like | §6 Verification(每条对应 PASS 命令) |
| (新增,IDS PRD 没有) | §7 Production Path Verification(operator 必须补) |
| Open questions | §3 Constraints 中"Open"小节 / §"Risks" |
| frontmatter (PRD-form / Status / Sources / Forked-from) | ADP spec frontmatter (spec_id / status / schema_version / reviewed-by) |

## ADP-side prerequisites

- ADP 仓库为 v3.2+ (含 sdd-workflow / task-decomposer skill)
- ADP `make doctor` exit 0(`pyproject.toml` deps 装齐)
- ADP `pre-commit install` 已跑(spec-validator + check-spec-review + check-constraint-references hooks)

## Open questions for build phase

(IDS PRD 没解决,留给 ADP build 阶段的 OQ)

## Rollback plan

如果 ADP build 失败:
- (a) 回到 IDS 修 PRD,重跑 /plan-start
- (b) 改 ADP spec(不改 IDS PRD),用 ADP 自己的 W-* 修订机制
- (c) 起 forge v2 重新审整个 idea
```

### Implementation status (2026-05-08 v2 修订)

✅ **HANDOFF.md schema 已重写为 operator-readable 格式**(不再依赖不存在的 `autodev_pipe-cli build`)。

⚠ **`/plan-start` 命令仍未实装产出 HANDOFF.md** — follow-up:
- 当前 `.claude/commands/plan-start.md` 不产出 HANDOFF.md
- 改造工作量:~2h(在 spec/tasks 写完后加一步)
- 触发条件:operator 真实跑 1 个 idea 走完 IDS L1→L4 + 切到 ADP 实测 schema 转换流程后,再改造 `/plan-start.md`(避免预先猜错)
- 在改造完成前,operator 跑完 `/plan-start` 后**手工创建** HANDOFF.md(按上述 schema 填字段)

### 客观依据

- **autodev_pipe v3.2 V1+V2** — `make sdd-init` / `make decompose` 是 ADP 实际入口,**v2 修订采纳此事实**
- **autodev_pipe v3.3 7 元素 spec schema**(含 Production Path Verification) — ADP spec 与 IDS PRD 是不同 schema 的事实根据
- **stroller idea004 12 路由 404 失败案例** — Production Path Verification 第 7 元素的设计动机
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

- **Producer**: ideababy_stroller `/plan-start` 命令
- **Consumer**: autodev_pipe `autodev_pipe-cli build` 命令
- **Schema**: 本文件 §1
- **Version**: follows shared-contract v1
- **Error-handling**: 缺 required 字段时,autodev_pipe 必须报错并提示具体字段名,不允许"尽力解析"

#### Interface 2 · Safety Floor binding

- **Producer**: ideababy_stroller `framework/SHARED-CONTRACT.md` §2
- **Consumer**: autodev_pipe AGENTS.md(必须引用并标注 binding)
- **Schema**: §2 三件套清单 + 实现 contract
- **Version**: follows shared-contract v1
- **Error-handling**: autodev_pipe 启动时若未检测到 Safety Floor binding 声明 → 拒绝运行 + 错误信息引导用户阅读本文件

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

## 验证

```bash
# 必须存在,有 5 节
test -f framework/SHARED-CONTRACT.md
grep -c '^## §' framework/SHARED-CONTRACT.md  # 应返回 5

# §1 PRD schema 必须含 example reference
grep -c 'discussion/006/forge/v1/stage-forge-006-v1.md.*§4' framework/SHARED-CONTRACT.md

# §2 Safety Floor 三件套必须列全
grep -c '^#### 件 [123]' framework/SHARED-CONTRACT.md  # 应返回 3

# §3 hand-off 必须给具体命令模板
grep -c 'autodev_pipe-cli build' framework/SHARED-CONTRACT.md

# §4 三阶段必须列出
grep -c '^#### 阶段 [123]' framework/SHARED-CONTRACT.md  # 应返回 3
```

---

## Changelog

- 2026-05-08 v1: 初稿,5 节(PRD schema / Safety Floor / Hand-off / 版本演化 / 五元组)
