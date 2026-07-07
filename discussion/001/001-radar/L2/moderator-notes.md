# L2 Moderator Notes · 001-radar（起步前必读）

> 这份 note 在 L2R1 开跑前落地，目的是让 L2 explore 从 **operator 澄清后的真实愿景** 起步，
> 而不是从 Direction 7 的 L1 一句话字面起步。L2 两位 explorer（Claude 终端 A + Codex 终端 B）
> 请把本 note 当作 L2 的默认背景。

## operator 口述的真实愿景（2026-07-06 · 逐字要点）

> "严格说，并不是简报工具。更像是一个 **Paper radar agent**，这个 agent 会**持续收集最新的 SOTA 文章**，
> 会**构建 paper、方法的知识图谱、知识库**。最终可以帮助 **AI lab 负责人快速跟进 SOTA 进展，快速把握
> 研究方向的 big picture**。"

拆成 L2 要摸透的几块：

1. **持续 SOTA 收集**（不是一次性检索）—— agent 主动、持续地把最新工作纳入视野。
2. **方法级知识图谱 + 知识库**（不只 paper-level）—— 图的节点不止是"论文"，还有"方法/技术"；
   边是 derives-from / contradicts / generalizes / supersedes（承 Direction 7）。
3. **big-picture 位移感**（radar 的 payload）—— 给 lab 负责人的是"领域这半年往哪漂"，
   不是"今天有 N 篇新论文"。位移 > 新增。
4. **用户 = AI lab 负责人**（PI / 研究方向决策者），核心 job = **快速把握研究方向 + 跟进 SOTA**。
   （对照 001-pA 的双 persona PI+PhD，这里 PI/lab-lead 是主 persona。）

## L2 必须回答的核心辨析（否则 L2 不算完成）

**与 Connected Papers / Litmaps / ResearchRabbit 的差异化**。Direction 7 自己标注：这些工具已有
paper citation graph 视图，fork 前必须辨析清楚"比现有 citation graph 多给了什么"。KG-radar 的候选
差异点（L2 要逐条验证是不是真差异、是不是真有价值）：

- **方法级 KG**（不止 citation graph）—— 抽方法/技术为一等节点，而非只连引用。
- **持续 SOTA 跟进**（radar 属性）—— 现有工具多是"给一篇种子 paper 长出邻域图"，静态；KG-radar 要
  持续把新工作纳进来并**告诉你什么变了**。
- **big-picture 位移呈现** —— "frontier 从 DPO 往 online 漂了 40 度"这种可上台演讲的 slide 级结论，
  现有图视图不直接给。
- **agent 自主品味** —— agent 判断哪些位移重要、值得 lab-lead 一看，而非纯拓扑展示。

⚠️ L2R2 的 value-validation search 用**当前（2026-07 月）**的竞品/模型行情，别用 4 月旧假设。

## L2 要 unpack 的开放问题（供 explorer 展开，不预设答案）

- 图**捕捉什么**：paper 节点？方法节点？claim 节点？三者混合怎么组织？
- 边**怎么来**：引用关系（结构化、便宜）？还是 LLM 关系抽取（贵、脆、可能放大幻觉）？
  —— 注意 001-pA 的 T001 教训：LLM 摘要 p95 46s / 月 $1838 曾把成本打爆（7 月模型可能已缓解，L2 别当死约束但要标风险）。
- **"big-picture 位移"具体怎么呈现**：diff 两个时间快照？中心性变化？聚类漂移？
- 典型 **aha 场景**：invited-talk 前一晚打开图看 frontier 漂移（Direction 7 给的例子）——还有哪些？
- 与 001-pA（PI Briefing 每日简报）是**互补**还是**替代**？（KG-radar 做地图，001-pA 做流；operator 现在要地图。）

## 边界（L1/L2 铁律提醒）

- L2 **不谈技术/可行性/成本**做决策（成本教训只作"风险标注"背景，不在 L2 下技术结论）。
- 004/006/008/009（活跃）、003（单独议）、其他 parked 兄弟 —— 不在本 fork 讨论范围。
- 复用 001-pA 作**参考**（paper 收集 pipeline / 双 persona / 成本 gate 教训），但 **001-radar 是新方向**，
  不继承 001-pA 那份"删掉知识图谱"的窄 scope。
