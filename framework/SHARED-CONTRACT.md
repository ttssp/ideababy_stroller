---
doc_type: framework-shared-contract
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

### 设计原则

- PRD 是 plain markdown 文件,**不是任何 DSL / YAML / JSON / 自定义格式**
- 这样保证跨 IDE / 跨 agent / 人类可直接编辑
- 字段顺序固定,但允许扩展子节(以下 8 字段必须存在)

### Schema(8 个 required 字段)

```markdown
# PRD · <name>

**PRD-form**: simple | phased | composite | v1-direct
**Status**: draft | reviewed | approved | superseded
**Source**: <upstream stage doc path>(L3 candidate / forge stage / direct)
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
| frontmatter (PRD-form / Status / Source / Forked-from) | required | autodev_pipe 用于路由判断 |
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

---

## §2 · Safety Floor 三件套定义

### 设计原则

Safety Floor 是 framework **不可妥协的硬约束**(NG-4):无论 autodev_pipe 在哪个 sandbox mode,这三件套**必须 hard block**。**ideababy_stroller 是 SSOT 拥有方**——任何 Safety Floor 定义变更必须先改这里,autodev_pipe 跟随。

> **Why ideababy_stroller 拥有 SSOT**:idea→PRD 阶段比 build 阶段更早接触 idea 全貌,能更早识别 production-related 风险点;且 ideababy_stroller release cadence 慢(per-idea 数天),适合做不变量层。

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

### autodev_pipe 实现 contract

autodev_pipe 仓库的 AGENTS.md 必须包含一节(完整文本见 `framework/AUTODEV-PIPE-SYNC-PROPOSAL.md`):

```markdown
## Safety Floor (binding from ideababy_stroller framework/SHARED-CONTRACT.md §2)

The following three rules are non-overridable. No prompt / config / sandbox
mode can disable them. See SSOT at: <ideababy_stroller path>.

1. Production credential isolation: ...
2. Irreversible command hard block: ...
3. Backup destruction detection: ...
```

---

## §3 · Hand-off 协议

### 设计原则

ideababy_stroller `/plan-start` 命令在产出 spec / tasks 后,**输出明确的"下一步在 autodev_pipe 跑哪个命令"指引**。用户不需要记忆跨仓 workflow,机器告诉机器。

### Hand-off 数据流

```
ideababy_stroller                       autodev_pipe
─────────────                       ──────────────
proposal.md
  ↓ /inspire-start
L1 stage doc
  ↓ /explore-start
L2 stage doc
  ↓ /scope-start
L3 stage doc → PRD
  ↓ /plan-start
specs/<NNN>-<fork>-<prd>/
  ├── spec.md
  ├── architecture.md
  ├── tasks/T001.md ... T0NN.md
  └── HANDOFF.md  ← 这是 hand-off 协议产物

                                   ← 用户切到 autodev_pipe 仓库
                                   autodev_pipe-cli build \
                                     --spec-path <path> \
                                     --safety-floor binding
                                       ↓
                                   parallel-builder workers
                                       ↓
                                   review coordinator MVP
                                       ↓
                                   ship
```

### HANDOFF.md schema

`/plan-start` 在 spec 目录下生成 `HANDOFF.md`:

```markdown
# Hand-off · <NNN>-<fork>-<prd> → autodev_pipe

**Handed off at**: <ISO timestamp>
**spec_id**: <NNN>-<fork>-<prd>
**spec_path**: <absolute path in ideababy_stroller>
**PRD source**: discussion/<NNN>/<fork>/<prd>/PRD.md
**Tasks**: <count> tasks in tasks/

## Recommended autodev_pipe command

```bash
cd <autodev_pipe path>
autodev_pipe-cli build \
  --spec-path <ideababy_stroller spec absolute path> \
  --safety-floor binding \
  --reviewer-mode <mixed | claude-full | codex>
```

## Required autodev_pipe state

- autodev_pipe AGENTS.md must reference ideababy_stroller framework/SHARED-CONTRACT.md §2 (Safety Floor)
- autodev_pipe contract version >= <semver from this hand-off>

## Open questions for build phase

(任何 spec 没解决,留给 build phase 的 OQ)

## Rollback plan

(如果 build 失败,回到 ideababy_stroller 哪一层 / 哪个命令)
```

### 客观依据

- **机器告诉机器**:工业范式 — CI 系统通常打印明确的"下一步命令",不让人记忆。来源:GitHub Actions / GitLab CI 等
- **跨仓 workflow 必须显式协议**:Newman *Building Microservices* ch.7,Consumer-Driven Contracts 不仅声明 schema,也声明 invocation
- **rollback plan 是 SOTA 实践**:Forsgren 2018 *Accelerate* 4 个核心实践之一是 "automated change failure recovery"
- **stage-forge-006-v1.md §"Decision menu"** 已示范类似 hand-off 结构(进 L4 / 跑 v2 / park / abandon 各带具体命令)

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
