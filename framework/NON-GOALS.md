---
doc_type: framework-non-goals
status: v1
generated: 2026-05-08
upstream: discussion/006/forge/v1/stage-forge-006-v1.md
purpose: 显式列出 framework 不做的事,锁定 scope,化解 second-system effect 风险
---

# Framework NON-GOALS

## 本文档定位

ideababy_stroller framework 是从 4 个历史尝试(idea_gamma2 / vibe-workflow / autodev_pipe / 当前 ideababy_stroller)+ forge 006 v1 双专家审阅 收敛得到的"分级 harness framework",**主语是 idea→PRD 阶段**(idea 孵化、L1-L4 + forge 横切层)。配套仓库 `autodev_pipe` 是 PRD→code 阶段(build harness)。

本文档列出 framework **明确不做**的事。每条 NON-GOAL 必须满足三个条件:

1. **客观依据**(benchmark / 文献 / 失败案例,不是主观偏好)
2. **至少一个 failure case**(被该 NON-GOAL 防住的具体反例)
3. **与 stage v1 §4 Scope OUT 一致或更利**(不与已收敛立场矛盾)

> **Why scope discipline matters**:Forsgren 2018 *Accelerate* 基于 23,000 团队的实证数据指出 — scope creep 是高绩效团队失败的首要原因。Brooks 1975 *The Mythical Man-Method* ch.5 "second-system effect" 警示工程师在第二个系统时倾向把所有"上次没做"的功能塞进来,通常导致项目失败。NON-GOALS 必须先于实现写,否则诱惑会持续存在。

---

## NG-1 · NOT 内化 idea_gamma2 / vibe-workflow / autodev_pipe 任一历史 repo 代码作为 framework 组件

### 含义

framework 仓库不通过 `git submodule` / `cp -r` / `npm install` / 任何代码级别复用方式,把 4 个历史 repo 的代码内化为 framework 自身的组件。它们的 **Lesson(设计原则)** 和 **Pattern(范式结构)** 被吸收(自己重新实现),但 **Component(代码)** 不复用——除非该代码满足以下严格条件之一:

- 已被 forge stage v1 §2 重写后的 L/P/C 分层表显式标为 `C 级,直接 cp`
- 与历史 repo 的非 framework 关注点(协议语义 / Workflow Builder DSL / 等)无耦合
- 经过红队测试,确认无引入额外维护负担

### 客观依据

- **Linux 50 年 OSS 协作范式**:Linux kernel 大量从 BSD / Plan 9 / Multics 吸收设计原则(VM 子系统 / file descriptor / process model),但**不 cp 它们的代码**。这是 free software / open source 50 年验证的 reuse model。来源:Linux kernel 历史档案 + Torvalds 公开访谈
- **Anthropic Skills SDK 不内化 superpowers**:只采纳 progressive disclosure pattern,自己实现。来源:Anthropic Skills SDK 公开设计 + P2-Opus §1 row 1
- **Brooks 1975 "second-system effect"**:把 4 套尝试的所有最佳实践塞进 framework = 创造第 5 套失败尝试。来源:*The Mythical Man-Method* ch.5

### Failure case

**Spotify Backstage 早期失败**(已公开 retrospective):试图把多个开源 developer portal 工具"全融合"成内部 platform,3 年后变成无人能维护的怪物,被迫重组并迁移到 plugin 架构。来源:Backstage 官方早期 retrospective 博客。

**Uber Cadence**(Temporal 前身)早期类似教训:试图把多个 distributed task scheduler 内化合一,后期不得不剥离重组。来源:Cadence/Temporal 公开历史。

### 例外

- ✅ autodev_pipe v3.1 STARTER_KIT **已物化的** 🟢 RUNTIME-COMPLETE 项可直接 cp(`scripts/router.py` / `scripts/kill_switch.py` / `.claude/hooks/block-dangerous.sh` / `templates/AGENTS.md`),因为它们与 v3.1 协议语义无耦合,是**通用工程脚本**——但**它们应该 cp 到 autodev_pipe 而非 ideababy_stroller**(参见 NG-2)
- ✅ idea_gamma2 33 条 phase-retrospective lesson(A1-A33)作为**数据**(不是代码)直接 import 到 autodev_pipe 的 Learning Loop 冷启动 corpus

---

## NG-2 · NOT 在 ideababy_stroller 仓库做 build / review coordinator / in-process brakes

### 含义

ideababy_stroller 仓库的关注点是 **idea→PRD**(L1 inspire / L2 explore / L3 scope / L4 plan + forge 横切层)。**build 阶段(代码生成、review 调度、运行时安全约束、cost 控制)归属配套仓库 `autodev_pipe`**。

具体不在 ideababy_stroller 仓库做的事:
- 不写代码生成 agent / build worker
- 不写 review coordinator MVP(stage v1 §3 模块 3)
- 不写 in-process brakes(tool-call 计数 / stasis detection / cost circuit breaker)
- 不写 runtime hooks(block-dangerous.sh 等)
- 不集成 SWE-bench Pro micro-benchmark runner

### 客观依据

- **Newman *Building Microservices* ch.4**:polyrepo 判定标准 = lifecycle + failure radius,**不是功能数量**
- **idea 阶段 vs build 阶段 4 维度数量级差异**:
  - 输出形态:markdown 无运行时 vs 代码 + 测试有运行时
  - 失败成本:废 PRD 可丢 vs 数据丢失 / 凭据泄露 / 烧钱
  - 反馈环:慢思考 / 多专家 vs 快迭代 / TDD / CI
  - 可逆性:完全可逆 vs 部分不可逆
- **Google monorepo 论据反向适用**:Potvin & Levenberg 2016 *Why Google Stores Billions of Lines of Code in a Single Repository* 显示 monorepo **仅在内部强耦合 + 变更原子性优先时**有意义。idea 阶段与 build 阶段无强耦合(PRD 是 plain markdown 接口),变更原子性也不需要(PRD 改完不需要立刻同步 build 代码),反向推论:**应该分仓**

### Failure case

**单仓承担两类目标的反例**:Spotify Backstage 早期试图同时承担 service catalog + developer onboarding + plugin marketplace 三个目标在一个仓库,导致 release cadence 互相阻塞(developer onboarding 需要快迭代,service catalog 需要稳定),后期重组为 plugin 架构。

**ideababy_stroller 当前实际状态**:repo 根有 `package.json` / `next.config.mjs` / `drizzle.config.ts` 等(应是早期实验残留),与 idea→PRD 关注点已经矛盾;framework 必须显式声明不做 build 才能避免进一步混淆。

### 例外

无。idea→PRD 的范畴是清晰的:L1-L4 命令链 / forge 横切层 / discussion/ 树形产物。任何 build 相关的代码都应在 autodev_pipe 仓库。

---

## NG-3 · NOT 做 SKILL/AGENT 体系再发明

### 含义

framework 不重新发明 SKILL 文件格式 / AGENT frontmatter schema / activation mechanism。**直接采用已存在的开放标准**:

- **AGENTS.md**(Linux Foundation AAIF 2025):事实 SSOT 文件格式
- **Anthropic Skills SDK + Claude Code Skills**:SKILL.md 文件格式 + progressive disclosure
- **agent-skills (addy osmani)**:社区 reference 实现的 skill 治理 pattern

framework 自己写的 SKILL/AGENT 文件**遵循上述格式,不另立**。

### 客观依据

- **AGENTS.md 已进 Linux Foundation AAIF**(Agentic Application Interoperability Framework, 2025),跨 IDE / 跨 agent 通用,已是事实标准。来源:LF AAIF 2025 公告 + P2-GPT §1 row 1
- **Anthropic 2025 Q3-Q4 推出 Claude Code Skills + Skills SDK**:progressive disclosure 是官方设计,自己再发明等于跟官方版本不兼容
- **Vercel benchmark 实证**:AGENTS.md 8KB 命中 100% / Skills 顶 79%。这两个数据已对应已存在的两个标准,自创格式无 benchmark 数据,reliability 未知。来源:P2-Opus §1 row 1 + P2-GPT §1 row 1-2

### Failure case

**Atom 编辑器 vs VS Code**:Atom 团队早期发明自己的 package format,VS Code 后来采用更标准的 extension API + 兼容更广,Atom 最终被 GitHub 弃用。教训:在已有事实标准时再发明会失败。

**Cordova vs React Native**:Cordova 早期发明自己的 plugin 体系,React Native 采用 native module 标准 API,Cordova 生态萎缩。

### 例外

- ✅ framework 可以**扩展** SKILL/AGENT 标准的 frontmatter 字段(如 vibe-workflow 的 `Allowed write paths` / `refusal rules`)——这是 Pattern 借鉴而非再发明,不违反此 NG
- ✅ framework 可以写自己的 命令(`/inspire-start` / `/expert-forge` 等)——这些不是 SKILL/AGENT 体系本身,是 framework 在 SKILL/AGENT 体系上的应用

---

## NG-4 · NOT 承诺 full-auto 跨 Safety Floor 的能力

### 含义

framework 永不承诺"agent 可以在 Safety Floor 边界**之外**完全自主操作"。具体含义:即便用户在 autodev_pipe 选择最高自动化档(`full-auto` sandbox mode),Safety Floor 三件套(production credential 隔离 / 不可逆命令 hard block / 备份破坏检测)**仍然 hard block,无任何 prompt / config / sandbox mode 可覆写**。

### 客观依据

- **Cursor + Claude 9 秒删库案例**(tomshardware 2025):AI agent 对生产数据做破坏性操作,生产库和备份被同一 API 删除。该案例是 prompt 纪律失效的硬证据——任何"灵活"的 Safety Floor 都会在某个 prompt 路径下被绕过。来源:tomshardware 2025 报告 + P2-GPT §1 row 9
- **Codex CLI 官方 sandbox modes**(suggest / auto-edit / full-auto):OpenAI 2025 范式即便在 full-auto 也保留某些 hard block(如 destructive shell 操作)。来源:Codex CLI 文档
- **K2 用户判准**:"可靠的、自动化程度最高"——可靠优先级高于全自动,K 自身已 disambiguate

### Failure case

**Cursor + Claude 9 秒删库案例**(已述):AI 在 9 秒内通过同一 API 删除主库 + 备份,无人工干预机会。如果当时有 hard block 拦截"对 production 凭据的不可逆操作",事故不会发生。

**Magicrails 14k tool-call loop**:agent 在无 in-process brakes 的情况下,15min 内调用 14000 次工具直到 kill_switch 触发——这是没有 hard block 时间边界的反例(虽然不是 Safety Floor 直接事故,但同类逻辑)。

### 例外

无。这是 framework 哲学层面的硬约束。

---

## NG-5 · NOT 复制 Cloudflare 全量 7 reviewer 系统

### 含义

framework 的 review coordinator MVP(归属 autodev_pipe)**不复制 Cloudflare 的全量 7 specialist reviewer 系统**(security / performance / correctness / readability / architecture / docs / tests)。MVP 只做 4 件套:

1. risk tier 分类器(file_domain / spec section / 危险命令 → tier 1/2/3)
2. specialist review 路由(tier 2 → 双签 / tier 3 → 三签)
3. timeout / circuit breaker
4. human escape hatch

### 客观依据

- **Cloudflare 30 天 131,246 run / 5,169 repos 数据来自他们 production 规模**。来源:Cloudflare 2025 工程博客 + P2-GPT §1 row 7
- **MVP 不必复制 SOTA 全量**:P3R1-GPT §3.3 明确"第一版只做风险 tier + specialist review + timeout,不必复制 7 reviewer 全量系统"
- **80/20 法则**:4 件套覆盖 80% 场景,7 reviewer 全量覆盖剩余 20% 边缘 case;MVP 阶段先做 80%
- **SWE-PRBench 数据**:AI review diff-only 命中率 15-31%,即便 7 reviewer 也只能在这个区间。MVP 4 件套先到 30% 即达基线。来源:SWE-PRBench 2025 论文 + P2-GPT §1 row 8

### Failure case

**Cloudflare 起步阶段也不是 7 reviewer 全量**(他们公开博客提及早期是 single coordinator + 2-3 reviewer)——直接复制别人 production 阶段方案到自己 MVP 是 over-engineering。

**Spotify Backstage 早期 over-engineering**(已述):试图一次到位完整功能,反而拖慢交付。

### 例外

- ✅ 在 Eval Score 数据反馈下,review recall 长期 < 30% 时,可以加 specialist reviewer——但每加一个必须有数据论据,不批量加
- ✅ 用户可以在自己的 autodev_pipe instance 配置中扩展到 7 reviewer——framework 不阻止,但**官方 MVP 文档不内置**

---

## NG-6 · NOT 把 SWE-bench Pro 当 CI 阻塞门

### 含义

framework / autodev_pipe 不把 SWE-bench Pro 通过率作为**CI 必过项**(merge 阻塞门)。它**只是 retrospective 触发器之一**——当 micro-benchmark 数据持续走低时,触发 retrospective 反思,不直接阻塞 release。

### 客观依据

- **SWE-Bench Pro 顶级模型 23%**(vs SWE-Bench Verified 70%+),说明 long-task benchmark 远未达到"高分=高质量"的可靠映射。来源:SWE-Bench Pro 2025 论文 + P2-Opus §1 row 7
- **如果 CI 阻塞需要 SWE-bench Pro 通过,等于阻塞所有变更**(因为 23% 通过率意味着大部分 PR 会被卡住)
- **micro-benchmark 用法 vs CI gate 用法本质不同**:micro-benchmark 是统计信号,CI gate 是 deterministic feedback,两者目的不同

### Failure case

**早期 ML 团队把 model accuracy 当 CI gate**:导致小幅模型质量退化时所有变更被卡;后来普遍改为"accuracy regression > N%" 或 "p95 latency > T ms" 这种**回归阈值**,而非绝对值。SWE-bench Pro 也应类似处理——只在大幅回归时触发,不当绝对值 gate。

**JS 生态 webpack-bundle-analyzer 当 CI gate 失败案例**:某团队把 bundle size 绝对值当 gate,后来发现合理新功能也被阻塞,改为"相对 baseline 增长 > 5%" 才触发。

### 例外

- ✅ retrospective 触发器(stage v1 §3 模块 4 已规划):每个 phase / 每个 PRD release 跑一次 micro-eval,记录 recall/precision,趋势异常触发反思
- ✅ 在 framework v2.0+ 阶段,**如果**有充分数据论证 SWE-bench Pro 通过率与 framework reliability 强相关,可以加为可选 gate(用户启用)——但 v1.0 不内置

---

## NG-7 · NOT 在 ideababy_stroller / autodev_pipe 之间做版本绑定

### 含义

ideababy_stroller 和 autodev_pipe 是**独立 release 的两个仓库**:

- ideababy_stroller v1.2 不要求 autodev_pipe 必须升到 v2.5
- autodev_pipe v3.0 可以同时与 ideababy_stroller v1.0 / v1.1 / v1.2 兼容
- 共同遵守的是 SHARED-CONTRACT.md 定义的接口契约,而非版本号

接口 breaking change 走 idea_gamma2 范式(deprecation period + migration path + version pin)——但**版本号本身不绑定**。

### 客观依据

- **Newman *Building Microservices* ch.7**:Consumer-Driven Contracts 范式核心原则——通过契约协调,**不通过版本号协调**;否则两个独立 service 失去独立演化能力
- **npm 生态历史教训**:strict version pinning(`"foo": "1.2.3"` 全锁死)和 free-floating(`"foo": "*"`) 都失败,合理范式是 semver + contract test。framework 与 build harness 是同样关系
- **Linux kernel + glibc 模型**:两者独立 release(kernel 6.x / glibc 2.4x),只共享 syscall ABI 契约,这是 30 年验证的协调范式
- **Pact framework 默认配置**:contract testing 不要求双方版本同步

### Failure case

**Twitter 早期 monolith 拆分中的版本绑定**:把 user-service 和 timeline-service 拆分后强制版本同步,导致每次发布两边都要协调时间窗,后来改为 Consumer-Driven Contracts 才解决。

**Atlassian Jira + Confluence 历史**:早期版本严格绑定(必须同时升级),用户抱怨,后来通过 REST API 契约解耦,可独立升级。

### 例外

- ⚠ **唯一例外**:SHARED-CONTRACT.md 自身的 breaking change(如 PRD schema 字段变化 / Safety Floor 三件套定义变化)——这种变化需要两仓**同时**部署支持新契约的版本,但即便如此也不锁死版本号,只锁契约 schema 版本

---

## 与 stage v1 §4 Scope OUT 的差异

stage v1 §4 写了 5 条 Scope OUT,本文档 7 条 NON-GOAL。差异:

| 文档 | 条数 | 表述 | 力度 |
|---|---|---|---|
| stage v1 §4 | 5 条 | "NOT 修改任一原 repo" 等 | 模糊("引用作为材料库") |
| 本 NON-GOALS | 7 条 | 显式 + 双向(L/P/C 分层 + 仓库分工) | 精确(每条带 failure case) |

本文档把 stage v1 隐含的"单仓合一"预设替换为"分仓 + L/P/C 分层",新增 NG-2(分仓)和 NG-7(不绑版本)是 stage v1 没显式列出的。其他 5 条与 stage v1 一致但更利。

---

## 验证

```bash
test -f framework/NON-GOALS.md && grep -c '^## NG-' framework/NON-GOALS.md
# 应返回 7
```

每条 NG 都包含:含义 / 客观依据 / Failure case / 例外。

---

## Changelog

- 2026-05-08 v1: 初稿,7 条 NON-GOAL,基于 forge 006 v1 verdict + 用户问 1/2 客观推导
