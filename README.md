# Idea Incubator (`ideababy_stroller`)

> 把一句话点子，按 4 层探索树喂给两个顶尖 AI 模型 + Codex 审查，最后产出**商业级**软件的单人开发流水线。
>
> 项目宪法见 [`CLAUDE.md`](./CLAUDE.md)；完整操作手册见 [`PLAYBOOK.md`](./PLAYBOOK.md)。本 README 解释**为什么**、**怎么设计**、**怎么跑**。

---

## 📌 What's new (2026-05-07)

今天落地三项改进，把孵化器从"4 层主线"扩展到"4 层 + 横切层 + PRD 形态多元化"：

| 改进 | 解决的问题 | 主要入口 |
|---|---|---|
| **横切层 `/expert-forge`** | 主线 L1-L4 不覆盖"已有 repo / 多份 stage 文档 / 外部材料"的双专家审阅 + SOTA 对标 + **强制收敛**到单一 verdict 的工作模式 | `/expert-forge <id>` · `/forge-inject <id>`（详见 §2.6） |
| **4 种 PRD 形态** | L3→L4 fork 不再只能"单 candidate v0.1"，把 `phased / composite / v1-direct` 提升为一等公民，避免 operator 现场发明 | `/fork-phased` · `/fork-composite` · `/fork-v1` · `/fork-module-out`（详见 §2.2 的 4 种形态表） |
| **GPT-5.4 → GPT-5.5 xhigh** | 统一升级所有 L1-L4 命令模板 / skill / agent 描述里的 Codex debater 模型名；新启动 idea 默认走新模型，已落盘文件保持原名 | 影响 30+ 文件的 docstring，无需 operator 操作 |

下面 §2.2、§2.6、§5 已嵌入这些改动；想直接看每条怎么用，跳到 §5 命令速查表。

---

## 0. 这个 repo 到底是什么

它**不是一个普通软件项目**，而是一个**"想法 → 软件"的孵化器仓库**。一个仓库同时承载多个 idea 在不同阶段的全部产物：

- 一句话 proposal（阶段 0）
- 双模型脑暴 / 论证 / 范围拆解的逐轮文档（阶段 1–3）
- 工程级 spec + 任务 DAG（阶段 4 的设计）
- 真正的代码与测试（阶段 4 的产出，多个 idea 并行存在）

operator 是**单个人类**(我自己)；执行体是一支 AI 团队：Claude Opus 4.7 / Sonnet 4.6 / Haiku 4.5、GPT-5.5 xhigh / GPT-5.3-Codex，再加上 Anthropic 的子智能体（subagent）系统与 Git Worktree 做并行隔离。

> ⚠️ **关于根目录**：当前 `package.json` / `pnpm dev` / `next.config.mjs` / `src/app/` 等 **属于 idea 001-pA(`pi-briefing`)** 的工程交付物。本 worktree(`worktree-idea001`) 同时承载孵化器(根仓 `ideababy_stroller`)和 001-pA 工程包，上半部分根文件是 001-pA 的，下半部分目录(`discussion/` `specs/` `proposals/` `.codex-inbox/` …)是孵化器自身的。其它 idea(003-pA、004-pB…)各自的工程代码在 [`projects/<fork-id>/`](./projects) 中，互不污染。

---

## 1. 设计初衷 / Why

我是**非软件开发背景**的单人开发者，但希望产出**商业落地级**软件。直接让 Claude Code "vibe coding" 出 SaaS 在 2026 年仍然不可靠。常见失败模式：

| 失败模式 | 根因 |
|---|---|
| AI 给了一个看起来不错的方案，但其实漏掉了你没想到的角度 | **认知盲区** —— 单一模型 + 单一 operator 无法跳出训练偏差 |
| 写到一半发现 PRD 还没想清，停下重写 | **层级混乱** —— 把"想做什么"、"为谁做"、"怎么做"搅在一起讨论 |
| 改 A 模块炸 B 模块；并行 5 个 worktree merge 时打架 | **缺少 spec 和文件域纪律** |
| 上线后才发现安全 / 并发 / 故障恢复一堆问题 | **没有跨模型对抗审查**，单模型审自己代码会跳过自己的盲点 |
| 多 idea 并行时上下文互相污染、token 烧穿 | **没有按 idea 隔离的工作目录与消息总线** |

本 repo 的核心设计目的，就是为单人 + AI 团队提供一套结构化方法论，让上述每一个失败模式都有**对应机制**去防：

| 防什么 | 怎么防 |
|---|---|
| 认知盲区 | **L1 Inspire 双模型并行 daydream + 价值验证 search** |
| 层级混乱 | **4 层流水线 + 铁律：L1/L2 不谈技术、L3 才上 human 真实约束、L4 才工程** |
| 模块互打 | **L4 spec-writer 出 spec → task-decomposer 切 DAG → file_domain 强约束 + worktree 并行 + 合并前 task-review** |
| 漏盲点 | **跨模型对抗审：Claude 实现 → Codex GPT-5.5 xhigh 9 维 adversarial review →（可选）Opus adversarial-reviewer** |
| 上下文污染 | **多队列 Codex inbox/outbox 总线 + 任意层 fork(sibling 不嵌套) + Park/Abandon 树操作** |

---

## 2. 设计方案 / What

### 2.1 4 层探索树（每层都能 fork）

```
Proposal （一句话点子）
   │
   ▼
L1 · Inspire   —— 让两个顶尖模型脑暴 N 个**启发方向**
   │           只谈价值/新颖性/实用性,**不谈技术**
   │           output: stage-L1-inspire.md (菜单)
   │           fork: human 选 1+ 方向 → 001a, 001b, ...
   ▼
L2 · Explore   —— 把选中的**那一个**方向深度展开成长文
   │           用户画像 / aha moment / 自然延伸 / 自然限制
   │           仍**不谈技术**
   │           output: stage-L2-explore-<fork>.md
   │           fork: 想试这个方向的不同切法
   ▼
L3 · Scope     —— **human 真实约束**首次进入(预算/工时/红线/平台)
   │           双方独立产 2-3 个 peer PRD 候选
   │           output: stage-L3-scope-<fork>.md → fork 出 PRD.md
   │           fork: 不同 PRD 解读
   ▼
L4 · Plan      —— 工程层。spec / architecture / 任务 DAG / 并行 build / 10 质量门
              output: 真实代码 + ship
```

**为什么是 4 层而不是 1 层**：每一层都有自己**该谈和不该谈**的事。把 L1 的发散和 L4 的工程混在一起，模型会立刻塌缩到"已有工具能实现的东西"，**最有价值的认知突破在 L1/L2 必须保护**。L3 才是 human 真实约束(钱/时间/红线)进入的位置，过早引入会扼杀想象力，过晚引入会让 spec 不接地气。

**每层产物独立有价值**：即使一个 idea 最终被 park 或 abandon，它的 L1 inspire menu 和 L2 essay 仍然是你认知地图的一部分。**Park 是常态，Abandon 附带 lesson 文档**(沉淀到 `lessons-learned.md`)。

#### 一个具象化例子：从"我想做个记账 App"到代码

| | 输入 | 这层产出什么(✅ 该谈) | 这层不能产出什么(❌ 留给后面) |
|---|---|---|---|
| **Proposal** | "我想做个记账 App，比现有的好用" | 一句话点子 + 写在 `proposals.md` 的状态标记 | — |
| **L1 Inspire** | 上面这句话 | 8–15 个**启发方向菜单**：①给跨境工作者多币种自动归一 ②给夫妻共账、月底自动复盘吵架点 ③不输数字，拍小票 OCR + 情绪标签 ④给小店老板的"现金流体感"看板 ⑤跨平台订阅自动识别 ⑥给青少年的零花钱教练… 每个方向附 spark / cognitive jump / "谁会爱上它" | ❌ "用 React Native 还是 Flutter" ❌ "OCR 用谁家 API" ❌ "做这个要多久" ❌ "App Store 抽成 30% 划算吗" |
| **(human fork)** | 选中方向 ②"夫妻共账+月底复盘" | `/fork 001 from-L1 direction-2 as 001a` | — |
| **L2 Explore** | 方向 ② 这一个 | 一篇长文：典型用户是"30+ 双职工夫妻、各自有信用卡和支付宝"；aha moment 是"月底自动生成 3 张图：花最多的类目 / 最容易吵架的类目 / 谁这个月主动多付了"；6 个月后的资深用户用它做"年度财务复盘"；自然延伸到"家庭年度预算共识"；自然限制是"不该变成第二个 Mint" | ❌ 仍然不谈技术。也不谈"v0.1 做哪几个功能"——那是 L3 |
| **L3 Scope** | L2 长文 + human 答 6 块问卷(预算/工时/红线/平台/优先级/商业模式) | 2-3 个对等 PRD 候选。例如：<br>**A**：iOS only · 8 周 · 只做"自动同步两人账单 + 月底报告"，红线"绝不做投资建议"<br>**B**：Web only · 4 周 · 只做"导入 Excel + 自动归类 + 共享链接"，更轻<br>**C**：iOS+Web · 14 周 · A+B+预算协商投票<br>每个含 user stories / scope IN / scope OUT / 成功标准 / 时间是否够诚实回答 | ❌ "A 用 SwiftUI 还是 UIKit" ❌ 具体接口 schema |
| **(human fork)** | 选 PRD-A | `/fork 001a from-L3 candidate-A as 001a-pA` → 自动生成 `PRD.md` | — |
| **L4 Plan** | `PRD-A` | `specs/001a-pA/` 完整工件包：spec.md(6 要素契约) / architecture.md(C4) / tech-stack.md(pinned 版本 + 拒绝的替代) / SLA.md / risks.md / non-goals.md / `tasks/T001..T020.md` + `dependency-graph.mmd`(并行友好的 DAG) | ❌ 仍然不改 PRD 的产品决策；spec-writer 发现 PRD 有问题必须 escalate |
| **L4 Build** | spec 包 | 真实代码 in `projects/001a-pA/`，每个 task 一个 worktree，TDD，合并前 task-review，最后过 10 质量门 → ship | ❌ build worker 不能改 specs/ |

**关键观察**：
- **L1 决定"我们到底在做什么品类的 App"**——选 ② 还是 ④，是认知层面的分歧，越早越便宜。
- **L2 决定"这个品类长什么具体样子"**——同样是 ②，可能是"自动报告型"也可能是"实时博弈型"，长文写出来才知道。
- **L3 决定"v0.1 砍到哪"**——A/B/C 三个 PRD 都合理，是 human 的钱/时间/性格在选。
- **L4 决定"代码怎么写不会炸"**——前 3 层任意一层没做扎实，L4 越往后翻车成本越高。

如果你跳过 L1/L2 直接 vibe coding，最常见的悲剧不是代码烂，是**做了 6 周才发现自己其实想做的是方向 ④ 而不是 ②**。

#### L2 vs L3：最容易混淆的两层

很多人会把 L2 当 L3 用，说"L2 不就是确定产品主题吗"。**不是**。主题在 L1 选方向时就定了，L2 是把这个主题**摸透**，L3 才是按 human 资源**砍出 v0.1**。

| | **L2 Explore** | **L3 Scope** |
|---|---|---|
| 核心问题 | 这个 idea 到底是什么？最丰满的样子长什么样？自然边界在哪？ | 给定我真实的预算/工时/红线/平台/商业模式，**v0.1 砍成什么样**？ |
| 姿态 | 发散 + 深入并存(无约束) | 收敛(强约束) |
| 谈什么 | aha moment / 具体场景里带名字的用户 / 自然延伸 / 自然限制 / 6 个月后的资深用户 / 一百万人用会怎样 | 时间够不够诚实回答 / scope IN / scope OUT / 成功标准(带数字) / UX 优先取舍立场 / 最大产品风险 |
| **不**谈什么 | 你能不能做、做得起做不起、做多久 | 技术栈、架构、具体接口 schema |
| 产出 | **一篇长文**(关于"这个东西本身") + 验证判决 Y/Y-with-conditions/unclear/N | **2-3 个对等 PRD 候选** + 比较矩阵 + 推荐 + 关键 tradeoff axis |
| human 介入 | 低(模型展开,你读) | **高**(L3R0 问卷答 6 块、最后挑砍法) |

**为什么 L3 输出 2-3 个候选而不是 1 个最佳方案**：因为给定同一份 L2 长文 + 同一组 human 约束，**有多种砍法都合理**——A 砍得激进(8 周做核心)、B 砍得保守(4 周做更轻的版本)、C 全做但时间紧(14 周)。human 在这几条之间挑，本质上是在挑**"我愿意接受哪种取舍"**，而不是"哪个方案对"。

#### 一个登山比喻把 4 层串起来

| 层 | 比喻 |
|---|---|
| **L1** | 站在山脚指着山说"这片山有 13 条路可以爬" |
| **L2** | 选定一条路，把这条路从山脚到山顶**完整走一遍勘察**——不背包、不带装备、只看地形 |
| **L3** | 回到家，**根据自己有多少假期、多少钱、能不能扛重**，决定这次只走前 1/3、还是从中段索道上、哪些装备不带 |
| **L4** | 真的去爬 |

记忆口诀：**L2 是"这个 idea 的最大版本长什么样"，L3 是"按我的钱包/日程，v0.1 砍成什么样最合适"**。

### 2.2 Fork 是 sibling，不是 nested

```
discussion/001/                   ← 根 idea
├── L1/stage-L1-inspire.md        ← menu(列出所有 candidate)
│
├── 001a/                         ← fork from L1 #3
│   ├── FORK-ORIGIN.md            ← 血统记录
│   ├── L2/stage-L2-explore.md
│   │
│   ├── 001a-pA/                  ← fork from L3 candidate A
│   │   ├── FORK-ORIGIN.md
│   │   └── PRD.md                ← /fork from-L3 自动生成
│   │
│   └── 001a-pB/                  ← 同 L3 的另一个 candidate
│       └── PRD.md
│
├── 001b/                         ← fork from L1 #5（并行 sibling）
└── 001c/                         ← 几周后回溯 fork from L1 #7
```

**关键性质**：
- 每个 stage 文档都**完整列出所有候选**（不只是被选中的）。所以未来任何时候都可以回溯 fork。
- fork 是 sibling，不嵌套，避免 `001a/001a-pA/001a-pA-x1` 这种深层路径地狱。
- `/fork from-L3` 除了建目录，还**自动从候选段落 + L3R0 硬约束生成完整 PRD.md**，这就是 L4 的输入。

#### 任意时刻、任意层都能 fork

很多人会以为 fork 只能在"刚做完那层、看了菜单"的当下做。**不是**。fork 命令对 5 分钟前完成的层和 5 周前完成的层一视同仁，因为**stage 文档本身就是真相源**——它完整列出了所有候选(不只是被选中的)。

| 场景 | 例子 |
|---|---|
| 刚做完那层、立刻 fork | `/inspire-advance 001` 后 → `/fork 001 from-L1 direction-3 as 001a` |
| **几周后历史回溯 fork** | 当时只 fork 了 #3，三周后想试 #7 → 同一个命令 `/fork 001 from-L1 direction-7 as 001g` |
| 同层多个候选并行 fork | `/fork 001a from-L3 candidate-A as 001a-pA` 和 `/fork 001a from-L3 candidate-B as 001a-pB` 同时存在,各自独立跑 L4 |
| Fork 的 fork(嵌套子树) | `/fork 001a from-L2 alternative-cut as 001a-v2` |

**3 个前提**：

1. **该层必须有 stage 文档**——fork 是从 stage 文档里挑候选，所以 `*-advance` 必须先跑过。还没闭层就 fork 会报错。
2. **Proposal 不 fork、L4 不 fork**——fork 只发生在 L1/L2/L3 三层。L4 是工程层，要换方向就回 L3 再 fork 一个 PRD 候选(因为换技术栈不该重写产品决策，换产品决策不该靠改代码)。
3. **fork 深度软上限 3 层**——超过的话路径和认知负担都会爆炸，违反 `CLAUDE.md` 铁律。

**为什么这个设计很重要**：它把"**现在做决定**"和"**把没选的路保留为未来选项**"解耦了：
- 你看完 L1 menu 选了 #3，**不等于放弃了 #5、#7、#11**——它们就静静躺在 stage 文档里
- 三个月后做完 #3 发现 #7 其实更值得，**直接从原 stage 文档 fork**，不用重新跑 L1
- 同理 L3：发现 PRD-A 选错了，回 L3 stage 文档 fork PRD-B，**L1/L2 不必重做**
- 这意味着**早期决策的"机会成本"被压到接近零**——选错的代价是几小时的 L4 沉没成本，而不是从零开始重想

#### 4 种 PRD 形态(L3→L4 的 fork 命令决定走哪条路)

L3 fork 出 PRD 时,有 4 种形态可选 — 不同形态决定了 L4 spec-writer 怎么消化、task-decomposer 怎么切 DAG。这是把"v1 直接规划"和"多 candidate 合集"作为一等公民支持的机制。

| 形态 | 命令 | 适用场景 | PRD 长什么样 | L4 产物差异 |
|---|---|---|---|---|
| **simple**(默认) | `/fork` | 单 candidate v0.1 — 没把握、要先打靶 | 单 candidate scope IN/OUT | 现有标准 7 文件 |
| **phased** | `/fork-phased` | 单 candidate,已对 v1 形态有清晰想象但选先 ship v0.1 验证假设 | `**Phases**: [v0.1, v0.2, v1.0]` 任意 ≥2;每 phase 有独立 Scope IN | SLA / risks 按 phases 分段;DAG 按 phase 分层 |
| **composite** | `/fork-composite` | 多 candidate **互补**(同一产品的不同器官,不是替代) | `**Modules**: [m1, m2, m3]`;每 module 一节 user stories / scope | 顶层 spec.md 是 INDEX + 每 module 独立 spec-`<m>`.md;DAG 按 module 用 subgraph 框 |
| **v1-direct** | `/fork-v1` | 已对方向有把握 — 内部工具 / 同质市场已验证赛道 / v0.1 没独立可发布价值(SDK/平台) | `**Skip-rationale**: \|<≥100 字 prose,必含 C1/C2/C3 之一>`;Scope 直接 v1 | SLA.md 顶部 §"Skip rationale";risks.md 必含 R-skip-v0.1(fallback path 必填) |

**怎么选?** scope-synthesizer 在 `stage-L3-scope-*.md` 末尾会强制产 §"Candidate relationships",分析 N candidate 之间是替代/互补/顺承,并**显式推荐**用哪个 fork 命令。这一节是机器人能给的"PRD-form 决策依据"。

**关键判别**:
- candidate 间是"替代" → 用多次 `/fork`(simple)做并行 sibling 子树,**不要**用 composite。sibling 允许 abandon 任一个,composite 一旦下注就要全做。
- composite 中途要砍 module → `/fork-module-out <prd> <module>`(剩 1 module 自动建议降级为 simple)。
- v1-direct 反悔 → next-step menu 里总有 `/fork-phased` 退路。

例:idea 001 research radar 的"采集 / 解析 / 知识库 / 主动补齐 / 时间线"5 块本来就是同一产品的不同器官 — composite 合理;而 idea 005 三个 candidate 是替代关系 → 应该 parallel forking 或 simple 选一。

### 2.3 Codex inbox/outbox 总线（v2 多队列）

human **从不在两个终端之间复制粘贴长 prompt**。Claude Code 把自包含任务写到 `.codex-inbox/queues/<id>/<TS>-...md` 并更新该队列的 `HEAD` 文件，Codex 终端只敲一个命令：

```bash
cdx-run 003-pA      # 读 HEAD 指向的任务,执行,写确认到 .codex-outbox/queues/003-pA/
cdx-queues          # 一行看完所有队列状态(✅ done / ⏸ pending)
cdx-peek 003-pA     # 偷看下一步要干嘛
```

**多队列**：每个 idea / fork-id 一个独立队列(`<id>` = `001` / `003-pA` / `004-pB`)。多个 idea 并行不冲突，多 worktree 合并时也只是文本冲突而不是 symlink 冲突。

**两种 kickoff 形态**：
- **oneshot**：每次新 Codex 会话(`*-start` 类命令默认；上下文重读，prompt cache 全部 miss，贵)
- **reuse-session**：在已开终端粘贴短 prompt(`*-next` 类默认；Codex 沿用上一轮上下文，~50–70% token 节省)

详见 [`.codex-inbox/README.md`](./.codex-inbox/README.md)。

### 2.4 模型分工（实测验证的"用对的模型干对的事"）

| 层级 | 模型 | 干什么 | 单位成本 |
|---|---|---|---|
| 架构层 | **Opus 4.7 (extended thinking)** | 跨模块决策 / 难 bug 根因 | 高 |
| 规划层 | **Opus 4.7 plan-mode** / **GPT-5.5 xhigh** | spec / 任务分解 / 选型 | 中高 |
| 审查层 | **GPT-5.5 (high) via codex-plugin** | 跨模型对抗审 | 中 |
| 主力开发 | **Sonnet 4.6** / **GPT-5.3-Codex medium** | 90% 业务代码 + 单测 | 低中 |
| 机械工 | **Haiku 4.5** / **Codex-Spark** | 格式化 / 重命名 / 样板 | 极低 |

**铁律**：不要让 Opus 写样板代码（浪费），不要让 Haiku 做架构（崩盘）。**Opus 规划，Sonnet/Codex 执行，Codex 审查**。

### 2.5 子智能体（Subagents）

`.claude/agents/` 下按角色定义：

| 智能体 | 用途 | 推荐模型 |
|---|---|---|
| `inspire-synthesizer` | L1 闭层，产 inspired menu | opus |
| `explore-synthesizer` | L2 闭层，产 explore 长文 + 验证判决 Y/Y-with-conditions/unclear/N | opus |
| `scope-synthesizer` | L3 闭层，产 PRD candidate 菜单 + 推荐 + key tradeoff axis | opus |
| `spec-writer` | PRD → 完整 SDD 工件包(spec/architecture/tech-stack/SLA/risks/non-goals/compliance) | opus |
| `task-decomposer` | spec → 10–30 个并行友好 task DAG | opus |
| `parallel-builder` | 单 task 在自己 worktree 内执行(TDD) | **sonnet 强制** |
| `adversarial-reviewer` | 三人格对抗审(破坏者+新员工+安全员) | opus high |
| `security-auditor` | OWASP Top 10 + auth 生命周期 + 供应链 | opus high |
| `code-reviewer` | 普通 PR 式审查 | sonnet |
| `debate-facilitator` | 观察辩论给 operator 决策建议 | opus |
| `stage1-synthesizer` / `stage2-checkpoint` / `conclusion-synthesizer` | (legacy v2.1 三阶段辩论) | opus |

> **个人偏好已固化**：`003-pA` build 阶段 parallel-builder 一律用 sonnet，忽略 task 的 recommended_model。

### 2.6 横切层：`/expert-forge`（双专家审阅 + SOTA 对标 + 强制收敛）

L1-L4 主线是"从零生发"的工作流。但**已经存在的东西**也需要被审：repo 跑了几版要拍板 redesign 还是 incremental optimize、一份成熟 idea 文档要直接产出可执行 PRD、多个外部参考 repo 要被综合评估。这类工作 L1/L2 太发散、L3 给候选菜单 defer 给 human、`/code-review` 又只看代码——**没有合适的层**。

`/expert-forge` 是一个**横切动作**(cross-cutting)，可以在 pipeline 任何位置触发。两个顶级模型扮演**审阅人**而非设计师：读现状 → SOTA 对标 → **强制收敛**到单一 verdict + W 形态可执行草案。

#### Forge 与 L2/L3 的关键区别

| 维度 | L2/L3 | forge |
|---|---|---|
| **输入** | 文档（proposal / stage doc） | repo 代码 + 多份 stage 文档 + 外部材料 + 用户关切 |
| **双方姿态** | 设计师（daydreamer，从零想象） | 审阅人（reviewer，评判已存在物） |
| **决策权** | defer 给 human（给候选菜单） | **强制收敛**（默认 strong-converge） |
| **产出** | 候选 PRD 菜单 | 单一 verdict + W 形态草案 |
| **搜索类型** | 价值验证 / scope-reality | SOTA 对标 / 实现路径调研 |
| **是否进 pipeline** | 是（L1→L2→L3→L4） | 否（横切层，**不嵌入**主线） |

#### 4+1 变量 + 收敛强度（Phase 0 intake 收集）

| 变量 | 含义 | 例 |
|---|---|---|
| **X · 审阅标的** | 仓库子目录 / 外部 repo 路径 / URL / 直接粘贴文本 / 历史 stage 文档 | `discussion/005/L3/` + `/Users/admin/codes/idea_gamma2/` |
| **Y · 审阅视角** | multi-select：产品价值 / 架构设计 / 工程纪律 / 安全 / 教学价值 / 商业可行 / UX / free-text | 架构设计 + 工程纪律 + UX |
| **Z · 参照系** | single-select：对标 SOTA / 对标指定列表 / 不对标纯内部 | 对标 SOTA |
| **W · 产出形态** | multi-select：verdict-only / decision-list / refactor-plan / **next-PRD** / next-dev-plan / free-essay | next-PRD + refactor-plan |
| **K · 用户判准** | free-text，贯穿所有 phase 的"你最在乎什么" | "最少代码重写量、必须用上已验证的两个 novelty、v0.1 必须 polish 拿得出手" |
| **收敛强度** | strong-converge（默认，单 verdict）/ preserve-disagreement（允许 ≤2 个并存 path） | strong-converge |

#### 5 个 Phase（状态机模式：反复跑同一命令推进）

```
Phase 0 · intake          ── operator 答 4+1 变量 + 收敛强度
   ▼
Phase 1 · 独立审阅          ── 双方各自按 Y 视角审 X 标的（无 search）
   ▼
Phase 2 · SOTA 对标         ── 双方按 Z 检索 SOTA / 消化用户外部材料
   ▼
Phase 3 · 联合收敛 R1       ── 双方互读 P2，提出收敛草稿
   ▼
Phase 3 · 联合收敛 R2       ── 双方根据对方 R1 修订，对齐到单一 verdict
   ▼
Phase 4 · synthesizer       ── forge-synthesizer 子智能体出 stage doc
                              输出: <DISCUSSION_PATH>/forge/v<N>/stage-forge-<id>-v<N>.md
```

每跑一次 `/expert-forge <id>`，状态机自动推进到下一个未完成的 Phase；中间夹 `cdx-run <id>` 让 Codex 完成它的 P1/P2/P3R1/P3R2 任务。

#### 用法（2 个命令）

```bash
# 启动或推进（同一命令反复跑，每次推进一个 Phase）
[A] /expert-forge 005           # 第 1 次：Phase 0 intake → Phase 1 Opus 写完 → 等 Codex
[B] cdx-run 005                 # Codex 写 P1
[A] /expert-forge 005           # 第 2 次：检测 P1 齐全 → Phase 2 Opus → 等 Codex
[B] cdx-run 005                 # Codex 写 P2
[A] /expert-forge 005           # 第 3 次：→ Phase 3R1 Opus → 等 Codex
... 直到 Phase 4 synthesizer 出 stage doc

# 在任意 Phase 转换前注入约束（同 scope-inject 风格）
[A] /forge-inject 005           # 追加 moderator note 到 forge/v<N>/moderator-notes.md
                                # 下一轮 Opus/Codex 必须读取并响应
```

**版本管理**：
- `<DISCUSSION_PATH>/forge/v1/`、`v2/`、…—— 每次完整跑完是一个版本
- `phase=done` → 询问 [查看 / 起 v<N+1> / cancel]
- `phase=aborted` → 自动起 v<N+1>，Phase 0 重做 intake

**适用场景例**：
- idea 005（auto agentic coding）已经有几版 spec/exploration，想让两位专家拍板"哪些保留、哪些 redesign、下一版 PRD 应该长什么样" → `/expert-forge 005`，Z=对标 SOTA，W=`refactor-plan + next-PRD`
- 一个 fork 的 v0.1 已经发布，想让专家审阅"现状 vs SOTA"，给出 refactor 路径 → `/expert-forge <fork-id>`，X 包含 repo 代码 + 用户使用反馈

详细协议见 [`.claude/skills/forge-protocol/SKILL.md`](./.claude/skills/forge-protocol/SKILL.md)（808 行，覆盖每个 Phase 的契约 / 护栏 / 失败模式）。

### 2.7 10 质量门（v0.1 → 商业化前的硬关卡）

`/quality-gate <fork-id>` 依次跑（任一不过不能 ship）：

| 门 | 工具 | 标准 |
|---|---|---|
| G1 类型 | `tsc --noEmit` / `mypy --strict` | 0 error |
| G2 Lint | biome / ruff / SwiftLint | 0 error · ≤5 warn |
| G3 单测 | vitest / pytest | 覆盖率 ≥ 80% |
| G4 集成 | Playwright / XCUITest | 关键路径全绿 |
| G5 安全扫描 | Semgrep + Snyk + Codex adversarial security | 0 critical/high |
| G6 性能基准 | 自定义 perf test | p95 在 SLA 内 |
| G7 跨模型审 | `/codex:adversarial-review --base main` | no blocking |
| G8 Opus 自审 | `adversarial-reviewer` 子智能体 | ≥ 85/100 |
| G9 合规 | 数据/隐私/GDPR/PDPA | 手动清单 |
| G10 人类验收 | operator 亲跑核心路径 | "感觉对" |

详细参考 `.claude/skills/quality-gate-runner/SKILL.md`。

---

## 3. 执行逻辑 / How（按 idea 全生命周期走一遍）

### 3.0 一次性 setup（约 90 分钟）

详见 [`PLAYBOOK.md` §0](./PLAYBOOK.md#0-前置准备一次性-setup约-90-分钟)。最关键的几步：

```bash
brew install node@22 ripgrep tmux gh
npm install -g @anthropic-ai/claude-code @openai/codex
claude     # 浏览器登录 Claude Max
codex      # 浏览器登录 ChatGPT Pro

# 在本 repo 内
bash install.sh                       # 建 AGENTS.md → CLAUDE.md 软链接 + 检查工具
bash scripts/codex-inbox-init.sh      # 初始化 Codex 总线目录

# 把 Codex alias 粘到 ~/.zshrc(见 .codex-inbox/README.md §"Codex 端推荐 alias")
source ~/.zshrc
```

订阅前提：**Claude Max 20x ($200/月) + ChatGPT Pro ($200/月)**。这是"双顶级模型辩论"得以成立的硬前提。完整成本估算见 PLAYBOOK §0.1。

### 3.1 提一个新 idea

```bash
claude
> /propose
```

或直接编辑 [`proposals/proposals.md`](./proposals/proposals.md)，按 `## **NNN**: <一句话标题>` 起头，**最少只填一句话想法**。状态字段：`draft → inspiring → menu-ready → exploring → scoping → planning → building → shipped | parked | abandoned | forked`。

### 3.2 走完一个 idea 的标准路径

下面用 `001` 这个虚构 idea 演示。Claude Code 终端 **A** + Codex 终端 **B** 各开一个，全程不需要复制粘贴长 prompt。

```bash
# ── L1 Inspire ──────────────────────────────────────
[A] /inspire-start 001                       # Opus 写 L1R1(daydream,无 search)
[B] cdx-run 001                              # GPT-5.5 xhigh 并行写 L1R1
[A] /inspire-next 001                        # 双方读对方,做价值验证 search
[B] cdx-run 001
[A] /inspire-advance 001                     # inspire-synthesizer 出 menu
                                             # human 选方向:
[A] /fork 001 from-L1 direction-3 as 001a

# ── L2 Explore (对 fork 001a) ───────────────────────
[A] /explore-start 001a                      # L2R1
[B] cdx-run 001a
[A] /explore-next 001a                       # L2R2
[B] cdx-run 001a
[A] /explore-advance 001a                    # 出 explore essay + 验证判决

# ── L3 Scope ────────────────────────────────────────
[A] /scope-start 001a                        # 先 L3R0 交互式 intake(允许"不确定")
                                             #   再 L3R1 双方独立 2-3 个候选 PRD
[B] cdx-run 001a
[A] /scope-next 001a                         # L3R2 cross + scope-reality search
[B] cdx-run 001a
[A] /scope-advance 001a                      # scope-synthesizer 出候选 PRD 菜单
                                             # human 挑一个 fork:
[A] /fork 001a from-L3 candidate-A as 001a-pA
                                             # 自动产出 PRD.md

# ── L4 Plan ─────────────────────────────────────────
[A] /plan-start 001a-pA                      # 触发 spec-writer + task-decomposer
                                             # 同时把 Codex adversarial R1 写进 inbox
[B] cdx-run 001a-pA                          # adversarial R1
[A] /plan-adversarial-next 001a-pA           # R2/R3/R4(默认 reuse-session)
                                             # 直至 verdict CLEAN
                                             # 然后并行开工:
[A] /parallel-kickoff 001a-pA T003,T004,T008
                                             # 每个 task worktree 合并前必跑:
[A] /task-review 001a-pA T003 --reviewer=claude-full
[A] /quality-gate 001a-pA                    # 10 门质量检查
```

### 3.3 任意时刻的"我现在该干嘛"

```bash
> /status                  # 全局面板:所有 idea 在哪一层、谁在等谁
> /status 001              # 单 idea 全树
> /status 001a             # 某 fork
> /status --activity 7     # 最近 7 天活动流
> /fork 001 from-L1 direction-7 as 001b   # 几周后想试当时没选的方向 → 历史回溯 fork
> /park 001a               # 好 idea 坏时机,等条件成熟
> /abandon 001a            # 学到了"这不该建",写 lesson
```

每个命令都以**编号决策菜单**结束（`[1] [2] [3]…`），human 回复数字或自然语言。永远不会出现"我做完了，然后呢？"的悬空。

### 3.4 出岔子时

详见 [`PLAYBOOK.md` §10](./PLAYBOOK.md#10-常见问题排障)。关键 3 招：

1. **`/status NNN`** 看真相（不要凭记忆）
2. **`/clear` 后从 stage 文档重启**，避免上下文污染
3. **某层在跑题（典型：L2 在谈技术）→ 重读对应 SKILL，用 `*-inject` 注入 moderator note**

---

## 4. 仓库目录速览

```
ideababy_stroller/
├── README.md                       # 你在这里
├── CLAUDE.md                       # 项目宪法（每个 Claude Code 会话自动加载）
├── AGENTS.md                       # CLAUDE.md 的软链接(给 Codex 读)
├── PLAYBOOK.md                     # 详细操作手册(~1000 行)
├── lessons-learned.md              # 所有 abandon 沉淀的全局教训(倒序)
├── install.sh                      # 一次性 bootstrap
│
├── proposals/proposals.md          # 所有 idea 入口(operator 写)
│
├── discussion/                     # 探索树(L1-L3 全部产物)
│   ├── PROTOCOL.md                 # 辩论协议指针(legacy v2.1)
│   ├── 001/...001a/                # 一个 idea 的整棵树(见 §2.2)
│   ├── 002/, 003/, 004/, 005/      # 其它 idea
│   └── ...
│
├── specs/                          # L4 spec 包(spec-writer + task-decomposer 写)
│   ├── 001-pA/  003-pA/  004-pB/   # 每个 PRD-fork 一个独立 spec 包
│   │   ├── spec.md  architecture.md  tech-stack.md
│   │   ├── SLA.md   risks.md   non-goals.md   compliance.md
│   │   ├── dependency-graph.mmd    # Mermaid DAG
│   │   └── tasks/T001..TNNN.md     # 并行友好的 task 卡
│
├── projects/                       # 真实代码(parallel-builder 写)
│   ├── 001-pA/                     # ⚠️ 当前根目录就是 001-pA 的工程包
│   ├── 003-pA/   004-pB/           # 其它 idea 的工程,各自隔离
│
├── .claude/
│   ├── settings.local.json         # 权限白名单 + 子智能体注册
│   ├── commands/                   # 30+ 斜杠命令(见 §5)
│   ├── agents/                     # 12 个子智能体定义
│   ├── skills/                     # 8 个领域 skill(协议/SDD/质量门/...)
│   ├── rules/                      # 路径作用域规则(specs 保护 / build 规则)
│   └── worktrees/                  # 并行 build 隔离目录(.gitignore 中)
│
├── .codex/config.toml              # Codex 项目级配置
├── .codex-inbox/                   # Claude → Codex 任务总线(多队列)
│   ├── queues/<id>/HEAD            # 每队列指针
│   ├── queues/<id>/<TS>-*.md       # 任务文件
│   └── archive/                    # v1 历史
├── .codex-outbox/                  # Codex → Claude 完成确认(对称结构)
│
├── ref_docs/                       # 跨项目参考资料
└── scripts/                        # 工具脚本
    ├── codex-inbox-init.sh         # 初始化总线目录
    └── check-disjoint.sh           # 检查 worktree 文件域是否真不重叠

# ── 以下属于 idea 001-pA(`pi-briefing`) 的工程交付,不是孵化器骨架 ──
├── package.json  pnpm-lock.yaml    # Next.js 15 + React 19 + Drizzle
├── biome.json   tsconfig.json
├── next.config.mjs   drizzle.config.ts   playwright.config.ts   vitest.config.ts
├── src/                            # 多 idea 代码混居(005, 003-pA, 004-pB...)
└── tests/
```

---

## 5. 命令速查（v3.0）

### 流水线主线（按层）

| 命令 | 时机 |
|---|---|
| `/propose` | 提一个一句话 idea 种子 |
| `/inspire-start <NNN> [--mode=full\|narrow\|skip]` | L1R1 daydream(无 search) |
| `/inspire-next <NNN>` | L1R2 cross + 价值验证 search |
| `/inspire-advance <NNN>` | 闭 L1，产 inspired menu |
| `/inspire-inject <NNN>` | 注入 moderator 约束(下一轮生效) |
| `/explore-start <fork-id>` | L2R1 deep unpack(无 search) |
| `/explore-next <fork-id>` | L2R2 cross + 价值验证 search |
| `/explore-advance <fork-id>` | 闭 L2，产 explore essay + 判决 |
| `/explore-inject <fork-id>` / `/explore-redebate <fork-id>` | 注入 / 整体 redebate |
| `/scope-start <fork-id>` | L3R0 intake + L3R1 候选 PRD |
| `/scope-next <fork-id>` | L3R2 scope-reality search |
| `/scope-advance <fork-id>` | 闭 L3，产 PRD 菜单 |
| `/scope-inject <fork-id>` | 注入约束 |
| `/plan-start <prd-fork>` | L4 启动：spec + task DAG + Codex adversarial R1 入箱 |
| `/plan-adversarial-next <prd-fork>` | R2-R4 迭代审 |
| `/parallel-kickoff <prd-fork> <task-ids>` | 并行 launch worktree |
| `/task-review <prd-fork> T<NNN>` | 单 task 合并前的强制 review gate |
| `/quality-gate <prd-fork>` | 10 门质量检查 |

### 树管理

| 命令 | 时机 |
|---|---|
| `/fork <src> from-L<n> <candidate> as <new-id>` | 任意层、任意时间，含历史回溯。from-L3 自动生成 simple PRD.md |
| `/fork-phased <src> from-L3 <candidate> as <new-id>` | 单 candidate 但 PRD 内声明 ≥2 个命名 phase(v0.1+v0.2 / v0.1+v1.0 等) |
| `/fork-composite <src> from-L3 <A,B,C> as <new-id>` | 多 candidate 合并成 1 PRD,各 candidate 变 module。**仅互补** — 替代关系请用 parallel /fork |
| `/fork-v1 <src> from-L3 <candidate> as <new-id>` | 直奔 v1,跳过 v0.1。需填 skip-rationale ≥100 字 + 含 C1/C2/C3 之一 |
| `/fork-module-out <prd-id> <module-id>` | composite 退路 — 砍 1 个 module(剩 1 个自动建议降级为 simple) |
| `/status [<id>] [--activity N] [--include-parked]` | 看全局或某 idea 的真相 |
| `/park <id>` | 暂搁(填复活条件) |
| `/abandon <id>` | 放弃(写结构化 lesson) |

### 横切层（不属于 L1-L4 主线）

| 命令 | 时机 |
|---|---|
| `/expert-forge <id>` | 双专家审阅已有产物（repo / stage 文档 / 外部材料）+ SOTA 对标 + 强制收敛。**状态机模式**——同一命令反复跑，每次推进 1 个 Phase（intake → P1 → P2 → P3R1 → P3R2 → synthesizer）。详见 §2.6 |
| `/forge-inject <id>` | 在任意 Phase 转换前注入 moderator 约束（同 `/scope-inject` 风格），下一轮 Opus + Codex 必须读取并响应 |

### Legacy v2.1（保留作 escape hatch，已标 DEPRECATED）

`/debate-start` `/debate-next` `/debate-advance-stage` `/debate-conclude` `/debate-finalize` `/debate-inject` `/spec-from-conclusion` —— 用于"我不想走 4 层，直接辩→结论→spec"的旧流程。

---

## 6. 铁律（违反会破坏整套系统的根基）

来自 [`CLAUDE.md`](./CLAUDE.md)，每个 Claude Code 会话自动加载：

1. **层级纪律**：L1/L2 不谈技术/可行性/成本；L3 才上 human 真实约束；L4 才工程。混层立刻塌缩。
2. **PRD 是 L3 之后的真相源**：spec-writer 读 PRD 但不改 PRD；有问题必须 escalate 给 operator。
3. **没有 spec 不写代码**(L4)：`specs/.../tasks/T<NNN>.md` 不存在的任务不能执行。
4. **TDD**(L4 production code)：测试先写、先 fail、再 implement、再 green。
5. **合并前必跑 task-review**(L4 build)：每个 parallel-builder worktree 必须 `/task-review` 拿到 verdict ≠ BLOCK 才能 merge。
6. **跨模型审查**（L4 v1.0 路径）：必须过 G7。
7. **specs/ 对 build worker 只读**：build worker 发现 spec 错就停下报告，operator 改、再分发。
8. **每个命令必须出 next-step 菜单**：human 永远不用记下一步。
9. **"不确定"是 L3R0 一等答案**：模型必须给选项，不能逼 human 表态。
10. **所有面向人类输出用中文**。

禁止：L1/L2 输出技术内容；自动生成 `AGENTS.md` / `CLAUDE.md`(LLM 生成的项目宪法质量崩)；从 build worker 改 specs；commit `.env*`；fork 深度 > 3 层。

---

## 7. 当前正在跑的 idea（截至 2026-05-07）

| ID | 标题 | 阶段 | 备注 |
|---|---|---|---|
| **001** Research Radar | 自动跟进 AI research 的 radar | L2 进行中 | 根目录工程包 `pi-briefing` 是其 fork `001-pA`(已 Phase 0 spec) |
| **002** 每天赚 100 美元 | (vague seed) | L1 done · 3 forks 待入 L2 | `002b/002f/002g` |
| **003** PARS | 并行自动化研究智能体系统 | L3 scoping | `003-pA` 已有完整 spec 包 + 在 `projects/003-pA/` 落地中 |
| **004** 个人投资顾问+助手 | 投资分析智能体 | `004-pB` L4 |
| **005** auto agentic coding | 让 Claude Code 自主完成开发的 framework | **L3 scoping**(本周) |

> 🪞 **特别说明**：idea 005 本质上是在**对本仓库自己做元层级反思**——"什么是最可靠的 agentic coding pipeline"，结论将反过来更新本 repo 的 SKILL/agents/commands。

---

## 8. 进一步阅读

| 想了解 | 看哪里 |
|---|---|
| 每一步详细操作 | [`PLAYBOOK.md`](./PLAYBOOK.md) |
| 项目宪法（铁律全文） | [`CLAUDE.md`](./CLAUDE.md) |
| Codex 总线机制细节 | [`.codex-inbox/README.md`](./.codex-inbox/README.md) |
| 各层协议（L1-L4 怎么写每一轮） | [`.claude/skills/{inspire,explore,scope}-protocol/SKILL.md`](.claude/skills/) |
| 横切层 forge 协议（4+1 变量 / 5 phase / 状态机） | [`.claude/skills/forge-protocol/SKILL.md`](.claude/skills/forge-protocol/SKILL.md) |
| SDD 工件契约(6 要素 spec) + 4 种 PRD 形态模板 | [`.claude/skills/sdd-workflow/SKILL.md`](.claude/skills/sdd-workflow/SKILL.md) · [`templates/PRD-{simple,phased,composite,v1-direct}.md`](.claude/skills/sdd-workflow/templates/) |
| 任务分解启发式 | [`.claude/skills/task-decomposer-skill/SKILL.md`](.claude/skills/task-decomposer-skill/SKILL.md) |
| 质量门跑哪些 | [`.claude/skills/quality-gate-runner/SKILL.md`](.claude/skills/quality-gate-runner/SKILL.md) |
| 当前 001-pA 工程契约 | [`specs/001-pA/README.md`](./specs/001-pA/README.md) |

---

## 9. 关于本 README 的角色

CLAUDE.md = 宪法（每会话加载，<150 行硬约束）。
PLAYBOOK.md = 操作手册（详尽，1000+ 行，按需查）。
**README.md = 门面 + 索引**：解释**为什么、怎么设计、怎么跑**，让任何第一次进 repo 的人在 10 分钟内理解全貌，并知道下一步该读哪份文档。

如果你只读一份文档，读 PLAYBOOK；如果你只有 10 分钟，读这份；如果你正在写代码、需要一条铁律提醒，看 CLAUDE.md。
