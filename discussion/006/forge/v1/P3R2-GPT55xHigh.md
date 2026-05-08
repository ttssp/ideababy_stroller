# Forge v1 · 006 · P3R2 · GPT55xHigh · 联合收敛 R2(finalize)

**Timestamp**: 2026-05-07T16:01:09Z
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: preserve-disagreement

## 1. 已收敛点

R2 后我判断四条分歧都已可收敛，不需要保留两个互斥 verdict path。

- **分歧 1 · 默认形态轻/重** → 已收敛到“分级 harness：轻入口、重升级”。我接受 Opus 的提醒：“L1-L4 是真实差异化”，但它不必成为所有小任务的默认负担；Opus 也接受轻骨架可作为 Path-B。
- **分歧 2 · 可靠性内涵** → 已收敛到 Safety Floor + Eval Score 两层。Safety Floor 优先，生产凭据、不可逆命令、数据删除、备份破坏必须 hard block；Eval Score 用任务通过率、review recall/precision、retrospective 数据持续改进。
- **分歧 3 · review 调度物化形态** → 已收敛到 MVP review 4 件套：风险 tier、specialist review、timeout/circuit breaker、human escape hatch。不复制 Cloudflare 7 reviewer 全量系统，但保留 coordinator 思路。
- **分歧 4 · autodev_pipe v3.1 核心 vs 材料库** → 我认为也已可语义收敛：v3.1 是 **L4 工程自动化核心资产**，不是整个 framework 的本体。全框架本体 = L1-L4 + forge + L4 harness；v3.1 负责提供 L4 的 AGENTS/skills/hooks/approval/cost/review 原料。这样同时保留 Opus 的“已对齐 SOTA”判断和我对“已设计 ≠ 已物化可靠”的区分。

## 2. 仍并存的分歧

§2 无 — 双方实质已收敛，转 §3 W 形态草稿建议。

这里的“无”不是说没有取舍，而是说取舍已经变成产品配置问题，不再是 verdict 分歧。human 后续仍要决定默认打开多少流程强度：小项目可以只启用轻入口；中大型、涉及生产数据、跨模块重构或 v1.0 发布的项目必须升级到完整 L1-L4 + forge + L4 harness。这个选择应在 stage 文档里写成明确开关，而不是写成两套互相竞争的哲学。

## 3. 给 synthesizer 的指令 / W 形态草稿建议

stage 文档不必展开双 path；建议写成“单一主体 verdict + 一个可选强度开关”。主体 verdict：构建基于 Claude Code 的**分级 harness framework**，面向非软件背景但能写 PRD 的 human；轻入口解决低风险小项目，重升级承接 idea→PRD→spec→tasks→parallel build 的中大型项目。

synthesizer 应避免把“可靠”写成泛泛的工程质量。请把可靠拆成三层：第一层 Safety Floor，任何自动化都不得越过；第二层 Deterministic Feedback，用测试、lint、hook、review gate 提供硬反馈；第三层 Learning Loop，用 retrospective 和 eval 把失败案例回写到 AGENTS、skills、rules 和质量门。这样 K 中“自动化程度最高”不会和“可靠”互相抵消。

- **W1 verdict-only**：现有尝试的正确方向是“分级 harness”，核心 gap 是把 SOTA 原语物化为权限、质量门、review 调度、遥测与 eval。
- **W2 decision-list**：保留 AGENTS.md 根上下文、L1-L4、forge、retrospective、cross-model review；调整 skills 从“事实承载”到“过程插件”；删除无治理工具堆叠和 full-auto 强承诺；新增 Safety Floor、Eval Score、review coordinator MVP、in-process brakes、项目规模升级触发器。
- **W3 refactor-plan**：模块 1：Context/Instruction 层，AGENTS.md + 本地 docs index + skill 激活测试。模块 2：Safety/Permission 层，凭据隔离 + 不可逆审批 + sandbox modes。模块 3：Quality/Review 层，risk tier + specialist review + timeout + telemetry。
- **W4 next-PRD**：决策 1：默认轻入口还是强制 L1-L4，应定为轻入口可升级。决策 2：full-auto 不得越过 Safety Floor。决策 3：可靠性验收至少包含最小 benchmark 与 review 命中率。
- **W5 next-dev-plan**：M1 把 v3.1 starter kit 改造成 L4 harness；M2 接入 review coordinator MVP；M3 建最小 eval/retrospective loop。
- **W6 free-essay**：关键论点：可靠不是“少问人”，而是高风险时必须问人；AGENTS.md 是事实 SSOT，skills 是可测试流程；L1-L4 是该框架相对通用 coding agent 工具的上游差异化。

如果 stage 文档需要保留 Opus 的 Path A / Path B，可降级为“实施节奏选项”：A 是两周内先物化 v3.1 为 L4 harness；B 是四到六周先重组完整 framework。两者共享同一 verdict，不再作为互斥路线呈现。
