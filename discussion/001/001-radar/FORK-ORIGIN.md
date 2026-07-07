# Fork origin

**This fork**: 001-radar
**Forked from**: 001 · L1
**Source stage doc**: [../L1/stage-L1-inspire.md](../L1/stage-L1-inspire.md)
**Selected candidate**: Direction 7 · "Topic Cartographer（做地图不做流）"
**Candidate description (extracted from source)**:

放弃"信息流"范式，做**持续更新的研究地图**。每个 topic 是一张图：节点是工作，边是
derives-from / contradicts / generalizes / supersedes。不是被每天/每周推送通知，而是在想查某个
topic 时打开地图，看这个领域最近六个月发生了什么**位移**——哪些方向被证伪、哪些被合并、哪些新节点
挤到中心。准备 invited talk 前一晚，打开 RL-from-preferences 的图，看到 frontier 从 DPO 往 online
方向漂了 40 度——这成为演讲的一张关键 slide。

**Spark**：流是**时间**的 organizing principle，地图是**结构**的 organizing principle。对研究来说
"位移"比"新增"更有信息量——哪些假设在退潮、哪些合并、哪些被证伪。把产品容器从 feed 换成 cartography
是一次元素级换向。

**从原提案的认知跃迁**：原提案里 "timeline / 同源 / 继承 / 对立" 全都存在，但它们在字面上仍被想象为
知识库的**索引维度**，不是产品的**主形态**。把结构从次要维度升级成主容器需要一次反转。

**Forked at**: 2026-07-06T13:04:20Z
**Forked by**: human moderator (via /fork command)
**Rationale** (human-provided):

operator 2026-07-06 澄清真实愿景 —— 要的不是当年 fork 的 **001-pA「PI Briefing Console」**（那是主动
砍窄的每日简报版，PRD 明确删掉了知识图谱），而是一个 **Paper Radar agent**：持续收集 SOTA 文章、
构建 paper/方法的**知识图谱 + 知识库**、帮 AI lab 负责人快速跟进 SOTA 进展 + 把握研究方向 **big picture**。
这个愿景几乎就是 001 最原始提案原文（"多层级 topic 知识库 + 时间线/同源/继承/对立检索 + 实时 SOTA"），
且精确匹配 Direction 7。**这条方向 L1 探过但从没 fork** —— 现在补上，走完整 pipeline（L2→L3→L4）。

> 更具体的 KG-radar 愿景（比 Direction 7 原文更细）已落 [L2/moderator-notes.md](./L2/moderator-notes.md)，
> L2 explore 从那份澄清愿景起步，不从 Direction 7 字面起步。

---

## What this fork is for

Now `001-radar` is its own independent sub-tree. The next layer (L2) will operate on the
candidate above (+ moderator note 里的澄清愿景) as if it were a fresh proposal. Run:

  /explore-start 001-radar

**核心待解问题（L2/L3 必答 · Direction 7 自己标注的）**：要辨析清楚比
**Connected Papers / Litmaps / ResearchRabbit** 的图视图多给了什么。现有工具已有 paper citation graph
视图；KG-radar 的差异化（SOTA 持续跟进 + **方法级** KG + big-picture **位移** + agent 自主品味）必须在
L2 explore / L3 scope-reality search 里说清，否则会撞进"功能 parity 无人区"。

## Sibling forks (for cross-reference)

- **001-radar**（this one）— Direction 7「Topic Cartographer」· 做地图不做流 · KG-radar 正确方向
- **001-pA**「PI Briefing Console」— Candidate A（当年 fork · 主动砍窄的每日简报版 · 删掉了知识图谱）·
  走到 Phase 0 kickoff-ready（25 任务 spec 包，T001 LLM spike 因成本 deferred）· **作 valid sibling 保留不动**。
  其 paper 收集 pipeline / LLM 摘要成本 gate 教训（T001: p95 46s · 月 $1838，7 月模型可能已解）/ 双 persona
  （PI + PhD）与 KG-radar 重叠，L2/L3 可引为参考。
