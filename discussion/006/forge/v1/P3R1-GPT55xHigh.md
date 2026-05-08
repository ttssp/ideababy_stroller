# Forge v1 · 006 · P3R1 · GPT55xHigh · 联合收敛 R1(标分歧)

**Timestamp**: 2026-05-07T15:47:06Z
**Visibility**: 我已读对方 P1 + P2。
**Searches in this round**: NONE(避免 R1 又开搜索发散)。

## 1. 整合摘要

双方 P1/P2 已基本收敛到一个事实：现有四套尝试不是“缺 workflow”，而是 workflow 原语过多、治理层不足。共同证据是 Vercel 的 AGENTS.md 激活优势、Cloudflare 的 coordinator + 多 reviewer、SWE-PRBench 的 AI review 低召回，以及 PocketOS 类破坏性失败。也就是说，可靠自动化开发的核心不再是写更多 prompt，而是把上下文、权限、质量门、证据、遥测和人类审批变成可执行系统。

Opus P2 更强调 autodev_pipe v3.1 已经“已对齐 SOTA”，并认为 L1-L4 是 ideababy_stroller 的真实差异化。我接受这两点，但会加一个约束：SOTA 对齐的 design doc 不等于 framework 已可靠，starter kit 的 post-hoc budget、hooks、skills 还缺 in-process brakes、量化 eval 和 review 调度器。

## 2. 我的初步 verdict(草案)

我倾向的 verdict 是：做一个**分级 harness framework**，不是单纯整理文档，也不是重写所有流程。轻入口用 AGENTS.md + 权限模式 + 基础质量门；重路径保留 L1-L4 + forge + specs/tasks，用于 idea→PRD→中大型项目。关键不确定点是最小可靠性 eval 怎么定义，如果 R2 解决不了我会改为双轨 verdict：轻量 starter kit 与重型 L1-L4 framework 并存。

## 3. 关键分歧清单

- **分歧 1**：默认形态是轻框架还是重框架
  - 我的立场：默认应“轻入口、重升级”，让非软件背景用户先跑起来，再按风险升级到 L1-L4。
  - 对方立场(引用):“L1-L4 是 ideababy_stroller 的真实差异化”
  - 我希望 R2 怎么收敛：把 L1-L4 定为 high-risk / idea-incubation 默认，而不是所有小任务默认。

- **分歧 2**：可靠性的第一含义是统计指标还是破坏性边界
  - 我的立场：先定破坏性边界，生产凭据、不可逆命令、数据删除必须 hard block；统计 eval 是第二层。
  - 对方立场(引用):“全部缺少” reliability 度量
  - 我希望 R2 怎么收敛：可靠性拆成 Safety Floor + Eval Score 两层，不互相替代。

- **分歧 3**：review 调度器要不要 Cloudflare 化
  - 我的立场：需要 coordinator 思路，但第一版只做风险 tier + specialist review + timeout，不必复制 7 reviewer 全量系统。
  - 对方立场(引用):“gap 大”
  - 我希望 R2 怎么收敛：明确 MVP 物化形态，避免把 Cloudflare 规模误当起步门槛。

- **分歧 4**：autodev_pipe v3.1 是方案核心还是材料库
  - 我的立场：它是核心材料库，不是最终框架；最终框架必须吸收当前 repo 的 L1-L4 与 idea_gamma2 的 retrospective。
  - 对方立场(引用):“autodev_pipe v3.1 是已对齐 SOTA”
  - 我希望 R2 怎么收敛：承认 v3.1 方向正确，但把“已设计”与“已物化可靠”分开。

## 4. 与 K 的对齐性自检

- K1 “给定 PRD，Claude Code 几乎无人工干预完成开发” → ⚠ 我的 verdict 对齐方向，但要求按风险分级，不承诺所有任务 full-auto。
- K2 “可靠的、自动化程度最高” → ✅ 分级 harness 同时追求自动化和 hard safety，不把二者混为一谈。
- K3 “非软件背景，但能写较可靠 PRD” → ✅ 轻入口 + 上游 L1-L4 能降低工程经验门槛。
- K4 “缺少大中小型开发方案、流程、规范把握” → ⚠ 需要 R2 明确小/中/大型项目的升级触发条件。
- K5 “吸收四个项目尝试” → ✅ verdict 明确吸收 autodev_pipe、idea_gamma2、vibe-workflow、ideababy_stroller。
- K6 “达成基于 Claude Code 的 framework/pipeline 共识方案” → ✅ R1 已能形成框架骨架；preserve-disagreement 只保留默认轻/重的产品化分歧。
