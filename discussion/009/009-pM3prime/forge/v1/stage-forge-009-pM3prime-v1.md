# Forge Stage · 009-pM3prime · v1 · "异源强模型能否当 D-7 金标 Layer-2 第二源"

**Generated**: 2026-07-23T10:05:00Z
**Source**: forge run v1 with X = 7 标的(2 本仓库文件 + 5 XenoDev-009 外部 repo 文件), Y = 验证方法学/认识论(核心) · 架构设计 · 产品价值, Z = 对标 SOTA, W = verdict-only + decision-list + next-PRD
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both), P2 (both), P3R1 (both), P3R2 (both)
**Reviewers**: Claude Opus 4.8(Reviewer A)· GPT-5.6-Sol xhigh(Reviewer B)
**Searches run**: 16 across ~9 distinct sources(Opus 4 · GPT-5.6-Sol 12)
**Moderator injections honored**: none(本 run 无 moderator-notes 注入)
**Convergence outcome**: converged(单一 verdict,无 unresolved;残余分歧降 3 条 v0.2 note)

---

## How to read this

forge 是横切层(不是 L1-L4 pipeline 的一部分)。本文档是两个异源强模型(Claude Opus 4.8 ×
GPT-5.6-Sol xhigh)独立审阅 + 各自跑 SOTA 对标 + 联合收敛后的产出,**强制给出单一立场**(不是候选
菜单 defer 给你拍板)。

本轮触发源:handback `009-pM3prime-20260723T082127Z`(FU-KG42)。证伪链 E1 密度普查已收口
(US go · HANDBACK-LOG#25),但最后一块「两层金标 Layer-2 验收」撞 frozen PRD 内部冲突(§2 单人
不懂投资 × §4-E1/D-7 领域独立真人第二源)→ Layer-2 无合格验收主体 → 诚实 STOP。operator 的核心
质疑:2026 顶尖强模型 + 异源,能否当合法第二源替代 D-7 的「真人」?

读完后你应该:
- 知道双方对「异源强模型当 Layer-2 第二源」的最终 verdict(§Verdict)
- 能逐条溯源支持每个子结论的具体证据(§Evidence map — SOTA 证据链是 load-bearing 的外部实证)
- 拿到按 W 形态准备好的可执行草案:decision matrix(三方向采纳判决)+ D-7 改写草案
- 能基于 §Decision menu 直接进入下一步(手工改 PRD / `/scope-inject 009` / 回 XenoDev 实装 / 跑 v2 / park)

## Verdict

**保留 gate 骨架 + 双层链 + D-7 的 Layer-2 fail-closed 实质;把「第二源」从来源类型硬编码
refactor 为三项分离契约(错误独立性 / 领域能力 / 最终仲裁权);不 redesign。**

`human` 是**独立性的当前可执行代理,不是投资知识的同义词**。**跨 vendor 强模型不能自动解除
correlated failure,不得按品牌放行当 Layer-2 独立终审** —— 两组零论文重叠的正交 SOTA 一致证明
(Nine Judges 跨 vendor φ=0.6 · Correlated Errors 350+ 模型 60% 同错 · 人 n_eff 是 LLM 2 倍)。
独立性可经「外部证据锚定 + 任务内盲测逐维双错率 + abstain」证成,不必等同碳基。**frozen PRD §2 ×
D-7 非产品级真互斥** —— 收窄为「当前资源下 Layer-2 全量验收暂不可满足」。可执行路 **(b)+(c)**:
Layer-1 短期可交付 + Layer-2 明示 known-limitation;**operator 配可审计证据协议后可自任独立第二源
(靠独立性而非领域深度),无须前置外求真人**。窄义 (a) = 外证据锚定模型辅助仅进 Layer-1;未校准前
fail-closed。**红线:第二 LLM 直接当 Layer-2 终审 = V4,`gold_layer2.py:81` 保留。**

(显式回应 K:①「异源强模型够不够格」→ 不够格直接替代;②「若不够给降级验收」→ (b)+(c) + operator
自任源;③ 红线「不许第二 LLM 假过」→ 守住,`:81` 不动。)

## Evidence map

每条 verdict 子结论 → 来源段落(可逐条溯源到 P1/P2/P3R1/P3R2):

| 结论 | 来源 | 引用(≤15 words) | 是否有反对证据 |
|---|---|---|---|
| 跨 vendor 强模型错误相关性≈同族,不构成独立性 | P2-Opus §1 row1 · P2-GPT §1 row3 | "Claude×Gemini φ=0.603 · GPT×Claude φ=0.588";"两模型都错时 60% 同错" | - (两组零重叠 SOTA 同向) |
| 人的错误独立性实测是 LLM 2 倍,human 非过度保守 | P2-Opus §1 row2 | "human n_eff 4.0–5.8 vs LLMs' 2.2–2.5" | - |
| 越强推理越相关(CoT 放大共享错误) | P2-Opus §1 row3 | "Chain-of-thought actually increases correlation" | - (直接打「用最强模型更独立」直觉) |
| 独立性来自外部证据锚定,非模型品牌 | P2-GPT §1 row5(FActScore/SAFE) | "正交性来自外部证据,不只来自模型品牌" | - |
| 冷门别名(老黄/达子/ASR 错词)异源模型仍共享流行度先验 | P2-GPT §1 row6(AmbER) | "同名冷门实体误取概率约为热门实体两倍" | - |
| gate 骨架 + 双层链 fail-closed 应 keep(结构正确) | P1-Opus §2(架构 keep)· P1-GPT §1(架构) | "harness/gate/SLA 占位结构本身正确且已 fail-closed" | ⚠ P1-GPT §2 初判架构 refactor(P2/P3R1 收敛到 gate keep) |
| 第二源契约须实质 refactor(逐维双错率+abstain+留痕),不只改 guard | P2-GPT §2.4 · P3R1-Opus §3侧重2 让步 | "只改 guard 又过窄…须记录证据来源、模型家族与 abstain" | ⚠ P1-Opus §2 初判架构纯 keep(P3R1 向对方让步) |
| §2 × D-7 非产品级真互斥,收窄为验收级暂不可满足 | P3R1-GPT §3侧重3 · P3R2-Opus §2 | "互斥只存在于当前资源下要求 Layer-2 全量通过" | - |
| operator 配证据协议可自任独立第二源(靠独立性非领域深度) | P3R2-Opus §1侧重2 · P3R2-GPT §1侧重2 | "operator 可以自任第二源,无须前置外求真人" | ⚠ P1-Opus/P3R1-Opus 初倾向「必须外求真人」(P3R2 被说服让步) |
| 窄义 (a):外证据锚定模型辅助仅进 Layer-1,不替代 Layer-2 终审 | P3R2-Opus §1侧重1 · P3R2-GPT §1侧重1 | "异源模型仅在 Layer-1 做原子化、检索与证据整理" | - |
| 红线:第二 LLM 直接当 Layer-2 终审 = V4,`gold_layer2.py:81` 保留 | P1-Opus §0(K 红线)· P3R2-Opus §2 | "gold_layer2.py:81 保留";CLAUDE.md V4 失败模式 | - |
| 元层自证:双方 P1 双双 refactor 是回声室,被各自零重叠 SOTA 推翻 | P2-Opus §3 元层 · P3R1-GPT §1 | "P2 我主动搜到反证并推翻自己的 P1" | 见 §What this menu underweights(本轮的皇冠证据) |

## Intake recap

### X · 审阅标的(7 个)
- `discussion/009/handback/…20260723T082127Z…md`(本仓库文件 · handback 冲突主诉 · 全文)
- `discussion/009/009-pM3prime/PRD.md`(本仓库文件 · §2 Users + §4-E1 金标两层验收 = frozen 冲突两造)
- `XenoDev-009/specs/009-pM3prime/spec.md`(外部 repo · D-7 / C9 / O7-O8 硬约束落点)
- `XenoDev-009/…/extraction/gold_layer2.py`(外部 repo · `:81` `second_source_kind != 'human' → raise`)
- `XenoDev-009/…/extraction/gold_layer1.py`(外部 repo · Layer-1 span 金标 harness 对照)
- `XenoDev-009/specs/009-pM3prime/risks.md`(外部 repo · E1-R2 + 原始 G-R1 echo-chamber 先例)
- `XenoDev-009/dogfood-backlog.md`(外部 repo · KG-42「第二源可得性」立项前置校验缺失)

### Y · 审阅视角
- 验证方法学/认识论(自定义 · 核心)
- 架构设计
- 产品价值
- (operator 显式未选「工程纪律」— 聚焦认识论+架构+产品,不发散到 harness 实装/测试/CI 细节)

### Z · 参照系
- mode: 对标 SOTA(LLM-as-judge 独立性 / 多模型集成错误相关性 / echo-chamber 实证 / 人机混合验收)
- 用户外部材料: 无(K 已含全部关切)

### W · 产出形态
- verdict-only(扩展 rationale → §Verdict rationale)
- decision-list(三方向 4 列矩阵 → §Decision matrix)
- next-PRD(D-7 改写草案 → §Next-version PRD draft)

### K · 用户判准
2026 顶尖强模型(GPT-5.6-Sol xhigh / Claude Opus)已在很多任务上强过普通人。operator 核心质疑:
这样的模型 + 异源(谱系不同于提取器),在「把自然语言笔记/直播片段映射成可交易信号」这个具体任务上,
独立性够不够格当 D-7 金标第二源?关键约束:D-7 现硬要「领域独立**真人**」(`gold_layer2.py:81` 焊死),
根源是 009-pForge **G-R1 双模型 echo-chamber** 实证 → forge 必须直面这个先例在异源强模型下是否仍成立。
**红线(绝不接受)**:第二个同源/弱异源 LLM 假装过 Layer-2 = V4 失败模式;「金标诚实待第二源」是合法
STOP,凑假金标不是。verdict 必须显式守住这条红线。元层自证:本 forge 本身就是两个异源强模型交叉审,
若连 forge 内 Claude×GPT-5.6-Sol 都收敛不出可信结论/暴露同构盲区,那本身就是「异源第二源不够独立」的实证。

### 收敛模式
strong-converge(P3R2 finalize 单一 verdict,残余分歧降 v0.2 note)

---

## Verdict rationale(W: verdict-only)

问题的关键不在「2026 模型强不强」,而在**能力(capability)与错误独立性(error independence)是两回事**
—— 双方在 P1 就各自点破(Opus §2「D-7 把手段 human 当目的」;GPT §2「真人只是独立性的代理」),P2 的
SOTA 把这个区分坐实成硬数据。

**Layer-2 第二源实际要做的工作,不是「懂投资」。** `mapping_agreement_rate()` 不含任何金融理解逻辑
(P1-Opus §1),它把 machine 映射与第二源映射逐条对齐,每条算 5 维(sector/ticker/direction/horizon/
timepoint)命中率。即第二源产出的是「同一段文本的独立五元组标注」。E1 真普查已实证(HANDBACK-LOG#25):
难点是**隐性指称消解**(「老黄/达子」→NVDA),~23/29 真隐性信号被口径捕捉。这解释了为什么「operator 不懂
投资」不是全维阻断 —— 事实维度(ticker/交易所)可外证据核验,不需领域深度。

**但「不需领域深度」≠「可换成第二个 LLM」。** 这是本轮 verdict 最锐利的一刀。D-7 要防的原始失败是
「两个同姿态 AI 收敛共享盲点」(009-pForge G-R1)。operator 直觉「2026 异源强模型也许逃出这个结论」很合理
—— 双方 P1 也都独立倒向这个直觉。**然后两组零论文重叠的 SOTA 各自把这个直觉打回来了**:跨 vendor 不解除
correlated failure(φ=0.6 · 60% 同错),CoT 更相关,长尾别名共享流行度先验(AmbER),人的独立性是 LLM
2 倍。**能贡献独立性的唯一 SOTA 路径是「锚定外部证据」(FActScore/SAFE),不是模型品牌。**

因此 D-7 的 `human` 保留,但**理据重述**:它守的是错误独立性,不是碳基身份。这让两件事同时成立:
(1) `gold_layer2.py:81` 不动(红线守住,第二 LLM 不得当 Layer-2 终审);(2) frozen §2×D-7 的死结被
解开 —— operator 本人只要**独立于提取器**(不看提取器输出、独立盲标、按证据协议判「映射对不对」、可
abstain),就是合格第二源。handback 的「无验收主体」不成立;冲突收窄为「当前资源下 Layer-2 全量验收
暂不可满足」,给降级口径(Layer-1 交付 + Layer-2 known-limitation)+ 校准后解锁,而非产品级真互斥。

---

## Decision matrix(W: decision-list)

针对 handback 三方向 (a)放宽D-7 / (b)降级验收 / (c)找真人源,逐条判决(双方 P3R2 §4 高度一致,已综合):

| 类别 | 项 | 来源(标的位置) | 理由(evidence) | 优先级 |
|---|---|---|---|---|
| **保留** | gate 骨架 + 双层链 fail-closed | `gate.py:44 _both_layers_passed` | 结构正确、已 fail-closed,挡未过信号流向回测 | P0 |
| **保留** | `gold_layer2.py:81` human 默认硬约束 | `gold_layer2.py:81` | 独立性红线;第二 LLM 直接终审 = V4(见 §Evidence map) | P0 |
| **保留** | C9 operator 不单独终审 | `spec.md` C9 | 仲裁权与独立源分离,冲突留仲裁链 | P0 |
| **保留** | 密度普查资产(US go) | HANDBACK-LOG#25 | E1 已交付的半条价值链,不动 | P0 |
| **保留** | Layer-1 接受第二标注者算 α/span F1 | `gold_layer1.py` | Layer-1 harness 正确,是短期可交付面 | P0 |
| **调整** | D-7 措辞:领域独立真人 → 错误独立性代理 | `spec.md` D-7 · PRD §4-E1 | human 是当前唯一实测满足者,理据是独立性非领域深度 | P0 |
| **调整** | 第二源契约:加逐维双错率 + abstain + 仲裁留痕 + 证据来源/模型家族记录 | `gold_layer2.py` evaluate_layer2 | 现只测输出 agreement,未测真正要防的错误重叠(P2-GPT §2.4) | P0 |
| **调整** | handback「互斥」表述:产品级 → 验收级暂不可满足 | handback 主诉 · KG-42 | §2×D-7 非真互斥,仅当前资源约束(P3R1-GPT §3侧重3) | P1 |
| **调整** | Layer-2 报告口径:按维报告,不以总分掩盖 | `mapping_agreement_rate()` | 事实维度 vs 解释维度独立性不同,总分会掩盖长尾 | P1 |
| **删除** | 「必须外求领域内金融专家真人」这个不可操作门槛 | PRD §2 × D-7 冲突 | 降为可选加强;门槛是独立性+证据协议非领域深度(P3R2 双方一致) | P0 |
| **删除** | 「operator 不懂投资 = 无验收主体」死结判定 | handback STOP 结论 | operator 配证据协议即合格独立源,死结解开(P3R2-Opus §1侧重2) | P0 |
| **删除** | 未校准的全量 Layer-2 承诺 | PRD §4-E1 SLA 槽位 | 短期不可满足;改为 Layer-1 交付 + Layer-2 known-limitation | P1 |
| **新增** | operator 自任独立第二源的证据协议 + 隔离流程 | (无 — 新建议) | 独立盲标(不看提取器输出)+ 外证据引用 + abstain,消死结(K 关切) | P0 |
| **新增** | 外证据锚定的模型辅助路径(仅 Layer-1) | (无 — 来自 FActScore/SAFE 对标) | 事实维度降人力;窄义 (a),不进 Layer-2(P2-GPT §1 row5) | P1 |
| **新增** | 尾部/长尾别名专项盲测校准集 | (无 — 来自 AmbER 对标) | 冷门 ticker 别名误取率 2 倍,需尾部专项金标(P2-GPT §1 row6) | P0 |
| **新增** | 逐维双错率报告 + abstain 机制 + 覆盖率 | (无 — 来自 Nine Judges/Correlated Errors) | 用可操作判据取代按 vendor 授信;门槛预注册(K「若够独立需可操作判据」) | P0 |

**三方向裁定一句话**:(a) 仅窄义采纳(模型辅助限 Layer-1);(b) 采纳为 v0.1 主路(降级验收);
(c) 采纳但重定义(资格从「懂美股真人」改为「过证据协议者」,operator 即合格,外求真人降为可选加强)。

---

## Next-version PRD draft(W: next-PRD)· D-7 / §4-E1 改写草案

**Status**: Draft from forge v1, awaiting human approval
**Sources**: 本 stage 文档 §Verdict + §Evidence map;P3R2-Opus §4 + P3R2-GPT §4(已综合)
**粒度约定**: 写到「D-7 新措辞 + 验收铰链四条 + §2×D-7 关系澄清 + 红线保留」,**不下沉到代码/模块/阈值实装**
(实装是 XenoDev L4 的工作)。

### D-7 新措辞(替换 spec.md:209 / PRD §4-E1 对应句)

> **D-7(改写)**:Layer-2 gold 的第二源不得以模型家族或 provider 异源作为独立性代理。合格第二源须
> **独立于提取器盲标**(不先看提取器输出)、**以可追溯外部证据作答**、并**通过任务内校准**(含长尾/歧义
> 样本)。独立性靠外部证据锚定 + 任务内盲测逐维双错率证成,**不靠来源品牌/领域深度**。`human`(含
> operator 本人,若独立于提取器且遵循证据协议)是当前可执行的独立性默认;跨 vendor 模型未经任务内校准
> 不得替代 Layer-2 终审。**无法判断须 abstain;冲突未仲裁不得通过。**

### 验收铰链四条(挂在 §4-E1 金标 Layer-2 定义下)

1. **外证据锚定**:每个判断绑定外部证据与来源;事实维度(ticker/交易所)由权威知识源核验。
2. **盲测校准前置**:资格启用前完成含长尾/歧义样本的盲测校准集(直击 AmbER 冷门别名 2 倍误取)。
3. **逐维双错率报告**:按 5 维(sector/ticker/direction/horizon/timepoint)报告双错率 + abstain +
   覆盖率;可接受门槛**预注册**(OQ-1 精神:先写下再测)。
4. **人审歧义 + 仲裁留痕**:歧义/方向/时点维度必须人(operator 或加强复核者)审;冲突保留仲裁链;
   未闭环 fail-closed。

### §2 × D-7 关系澄清(消 handback 死结)

- **非产品级真互斥**:operator「不懂投资」不阻断独立第二源 —— 要的是独立性,非领域深度。
- 冲突仅「当前资源下 Layer-2 全量验收暂不可满足」→ 给降级口径:**Layer-1 span 一致性可交付 + Layer-2
  标 known-limitation**;operator 过证据协议校准后解锁全量。
- **外部真人不是 v0.1 前置门槛**:当 operator 尾部校准不过线 / abstain 导致覆盖不足 / 同类歧义持续
  复发时,再评估升级引入领域标注者。

### 红线保留(不动)

第二 LLM 直接当 Layer-2 终审 = V4 失败模式;`gold_layer2.py:81` human 默认不动。新增「外证据锚定
辅助」仅作用 Layer-1。以后若任务内数据证明某种证据锚定模型达到预注册的逐维独立性门槛,可重审其
Layer-2 资格,但**不得按 provider 品牌直接放行**。

### Open questions(forge 也没解决的 — 见下方 v0.2 note)

- 逐维双错率的可接受阈值具体数字未定。
- 「外证据锚定」用哪个权威知识源核验 ticker 未定。
- operator 自任第二源时技术上如何保证「独立于提取器」(标注 UI/流程隔离)未定。

---

## What this menu underweights(强制自批判)

诚实表述本 stage 文档可能 underweight 的点。这是质量栏,不能跳过。

- **[皇冠自证]本轮 forge 本身就是「不能靠双模型互审自证」的一个正面演示**:双方 P1 都**独立倾向
  refactor D-7**(重演 forge v5 §underweights 自认的「双模型强收敛回声室」模式)。**但 P2 双方各自跑
  零重叠 SOTA 都推翻了自己的 P1** = 引正交外部实证破双模型收敛,正是 009-pForge G-R1 的原始教训
  (「M1 真实测 vs 纸上蓝图」)的正确执行。**收敛不靠互认,靠外部实证。这轮 forge 恰恰是 D-7 想守护的
  道理本身。** 反过来说:如果本轮双方只靠 P1 互读就收敛,本文档的 verdict 就该被打折扣;它可信是因为
  P2 的外部实证,不是因为两个模型都同意。

- **逐维双错率的可接受阈值具体数字未定(v0.2 note 1)**:SOTA 给了方法(报告逐维双错率)未给本任务的
  阈值。verdict 说「预注册门槛」是对的方向,但「多少算过」这个 load-bearing 数字要等第二源校准集跑出后
  才能定 —— 在此之前 fail-closed 是唯一诚实姿态。

- **外证据锚定用哪个知识源核验 ticker 未定(v0.2 note 2)**:record_tickers 判定 / 外部 ticker DB /
  交易所清单三选一未定,且受红线约束(不得引入 look-ahead)。选错知识源会让「事实维度可核验」这个前提
  打折。

- **operator 自任第二源的技术隔离未定(v0.2 note 3)**:verdict 允许 operator 自任独立源的**前提**是
  「独立于提取器」(不先看提取器输出)。这需要一个标注 UI/流程隔离约束。若隔离做不干净(operator 无意间
  瞄到提取器答案),整个「operator 即合格独立源」的结论就塌了 —— 这是 (b)+(c) 主路最脆弱的技术假设。

- **Y 视角未含工程纪律**:operator 显式未选,故 harness 实装/测试/CI 细节未审。逐维双错率、abstain、
  证据留痕这些**契约**已给,但它们的**实装正确性**(会不会像 009 历史上 two-SELECT 原子性那样纸上正确
  实测踩坑)不在本 verdict 覆盖,需 XenoDev build-time 真跑兜底。

- **SOTA 外推边界**:引用的 SOTA(Nine Judges/Correlated Errors/AmbER/FActScore/SAFE/PoLL)证的是
  「一般 LLM-as-judge / NL 事实性判定」的错误相关性,**不是**直接在「直播片段→A股/美股五元组」这个精确
  任务上的实测。双方判断外推成立(事实性映射 + 长尾别名场景高度吻合),但严格说这是**强论证不是本任务
  直接实测** —— 真正的本任务双错率仍要 v0.1 校准集跑出来。

- **forge versioning 提示**:以下新信息进入会触发 v2 跑并可能改本 verdict —— ① 第二源校准集真跑出
  逐维双错率数据(可能证明某证据锚定模型达标,松动窄义 (a));② operator 自任源的隔离流程被实证做不到
  独立(可能逼回外求真人);③ 出现「直播→五元组」任务上的直接错误相关性实测(替代当前的 SOTA 外推)。

## Decision menu(for human)

### [A] 接受 verdict → 改 PRD → 回 XenoDev 实装
```
本 forge 不改产品决策的落点;落点在 frozen PRD D-7 / §4-E1。两条改法二选一:

选项 A1(手工改 PRD):
  1. 打开 /home/ys/codes/ideababy_stroller/discussion/009/009-pM3prime/PRD.md
  2. 把本 stage §"Next-version PRD draft" 的 D-7 新措辞 + 验收铰链四条 + §2×D-7 澄清
     抄进 §4-E1;标注 Source: forge stage-forge-009-pM3prime-v1.md
  3. 记一条 HANDBACK-LOG(FU-KG42 决议入库,呼应 KG-42「第二源可得性」立项前置校验)

选项 A2(命令化):
  /scope-inject 009        # 若该命令支持把 forge D-7 改写草案注入 frozen PRD

无论 A1/A2,改完 PRD 后:
  → 新开 XenoDev session:cd "$XENODEV_ROOT" && claude -w 009-pM3prime
  → 按新契约实装第二源资格层:证据协议 + 逐维双错率 + abstain + operator 自任独立源的隔离流程
  → 起跑前先解 3 条 v0.2 note(阈值 / 核验知识源 / 隔离流程)
```
⚠ 本 verdict 是 PRD 层改动(改 frozen PRD 内部约束),不是直接进 `/plan-start`。PRD 改定后走既有
   L4 链路。§"Next-version PRD draft" 已就绪可直接抄。

### [B] 跑 forge v2(若 operator 觉 verdict 不够锐)
```
/expert-forge 009
# 在 Phase 0 intake 时调整 X / Y / Z / W / K
# 旧 v1 整目录保留作历史参考
```
适用:verdict 不够锐利、需要把「直播→五元组」任务的直接错误相关性实测拉进 X、或 K 关切变化。

### [C] 局部接受
- ✅ 采纳:gate keep + `:81` 红线保留 + 降级验收口径(Layer-1 交付 + Layer-2 known-limitation)
- ⏸ 挂起:D-7 措辞暂不改(等第二源校准集真跑出逐维双错率再定改写细节)
- ❌ 拒绝:(按 operator 判断填,如「operator 自任源」这条若觉隔离流程风险太高可先拒)

适用:想先解 E2 阻塞(降级验收让 Layer-1 可交付),但对「operator 自任独立源」这条要更多技术验证再拍。

### [P] Park
```
/park 009-pM3prime
```
保留所有 forge 产物,标记暂停。E2 反正要三条件齐(密度 + 金标 Layer-1 + Layer-2),金标 Layer-2 这条
可挂,先推进其它条件。复活时不重做本轮 forge。

### [Z] Abandon
```
/abandon 009-pM3prime
```
放弃证伪链金标 Layer-2 —— **不推荐**。E1 真普查(US go)的 ROI 建立在「提取器可靠性可被验证」之上;
放弃 Layer-2 = 密度达标但信号质量永不验 = 半成品,毁 E1 ROI(handback §0 防 V4:「不过金标,任何回测
都是自欺」)。归档 lesson 文档。

---

## Forge log
(由 /expert-forge 命令更新;记录每次 forge run 的 v 序列 + 关键 verdict 一句话)

- v1: 2026-07-23 — verdict: "D-7 保留 human 为独立性默认代理但重述理据(要独立性非领域深度);第二源
  refactor 为错误独立性/领域能力/仲裁权三分离;跨 vendor 强模型不得当 Layer-2 独立终审(两组零重叠
  SOTA 无背书);frozen §2×D-7 收窄为验收级暂不可满足;可执行路 (b)+(c) + operator 配证据协议自任独立
  源 + 未校准前 fail-closed;红线 `gold_layer2.py:81` 保留。"
