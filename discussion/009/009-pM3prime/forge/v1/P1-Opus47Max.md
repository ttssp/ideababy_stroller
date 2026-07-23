# Forge v1 · 009-pM3prime · P1 · Claude Opus 4.8 · 独立审阅(no search)

**Timestamp**: 2026-07-23T09:20:00Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1 (GPT-5.6-Sol).
**Reviewer stance**: 审阅人 —— 评判已存在物(frozen PRD 冲突 + 金标 harness 现状),不是 daydream。先看坏处再看好处。

## 0. 我读到的标的清单 + 阅读策略

- 我读了:
  - `handback 20260723T082127Z`(全文)—— 冲突主诉:§2 × §4-E1/D-7 互斥,Layer-2 无验收主体,诚实 STOP。
  - `PRD.md` §2(L56-60)+ §4-E1(L97-142)—— frozen 冲突两造原文;金标两层验收定义 + "operator 可当标注者之一,不单独终审"(L135)。
  - `spec.md` C9(L191)/ D-7(L209)/ O7-O8(L261-262)/ O7-O8「待第二源·未验收」状态注(L115-117)。
  - `gold_layer2.py`(全文)—— **关键**:`mapping_agreement_rate()` 是**逐维度 `==` 机械比对**(sector/ticker/direction/horizon/timepoint 5 维逐条对齐);`:81` `if second_source_kind != 'human': raise`。
  - `gold_layer1.py`(对照)+ `gate.py`(`_both_layers_passed` fail-closed · L44)。
  - `risks.md` E1-R2(L43-57)+ **原始 G-R1**(`specs/009-pForge/risks.md:63`)。
  - `dogfood-backlog.md` KG-42(L789)。
- 我跳过的:无 BLOCK(本机可读 XenoDev-009)。
- **K(用户判准)摘要**:operator 核心质疑 —— 2026 顶尖强模型 + **异源**,在"NL 笔记/直播 → 可交易信号映射"这个**具体任务**上,够不够格当 D-7 第二源?D-7 现要"领域独立**真人**",根源是 009-pForge **G-R1 双模型 echo-chamber**;forge 必须直面这个先例是否在异源强模型下仍成立。红线:绝不接受第二 LLM 假过(V4)。
- **我的阅读策略**:按 Y=验证方法学/认识论优先 —— 先挖清 **D-7 到底在防什么**(回原始 G-R1)+ **Layer-2 第二源实际要做什么工作**(读 `mapping_agreement_rate` 实装);再按 Y=架构看接入点可演化性;按 Y=产品看三方向对"不懂投资 operator"的真实价值。

## 1. 现状摘要(按 Y 视角组织 · 只描述不评价)

### 视角 A · 验证方法学/认识论(核心)

**D-7 要防的原始失败,是"两个同姿态 AI 收敛共享盲点"。** 原始 G-R1(`009-pForge risks.md:63`)白纸黑字:"v1+v2 蓝图是**两个 AI 高度收敛的产物**...可能共享盲点(如低估干净历史数据获取成本)";其缓解是"**M1 真实测、M2 真跑**"——即用一种**正交手段**(碰真实世界)去验纸上推演。E1-R2(risks.md:43)把这条先例**类比迁移**到 Layer-2 金标:"若第二标注源也用 LLM,两 LLM 可能共享同套直觉 → Krippendorff α 虚高,金标假过。"D-7 / C9 由此硬性要求"Layer-2 用真人第二源"、`gold_layer2.py:81` 落死 `!= 'human' → raise`。

**Layer-2 第二源的实际工作 = 独立重做一次映射,然后系统机械比一致率。** `mapping_agreement_rate()` 不含任何"金融理解"逻辑 —— 它把 machine 映射与第二源映射逐条对齐,每条算 5 维度(sector/ticker/direction/horizon/timepoint)命中率,全条平均。即第二源要产出的是**同一段文本的独立 {sector,ticker,direction,horizon,timepoint} 五元组标注**。E1 真普查已实证(HANDBACK-LOG#25):这些映射的难点是**隐性指称消解**——"老黄/达子"→NVDA、"谷子"→GOOGL、"美光"→MU、ASR 转错"新一生"→300502。~23/29 真隐性信号被口径捕捉。

**冲突事实(frozen · 立项即在)**:PRD §2(L58)"单人自用 operator,懂算法不懂投资";§4-E1/D-7 要"领域独立真人第二源"。operator 自评无合格金融判断、标注质量不如 LLM → Layer-2 无合格验收主体 → verdict 停"待第二源·未验收"。forge v5(立项)/v6(引文回锚)全程未算出这对互斥(KG-42 记)。

### 视角 B · 架构设计

金标验收链已结构就位、缺的只是"第二源输入":harness 实装经审(`gold_layer1/2.py`)· gate `_both_layers_passed` fail-closed(无金标行→False→挡下游)· SLA 门槛槽位留空标 blocked-on-第二源 · O9 挡未过信号流向任何回测消费方。`gold_layer2.py:81` 的 human 硬约束是**唯一**把"第二源类型"焊死的点;`evaluate_layer2()` 的其余入参(machine/human_annotations/threshold/arbitration_note)对"第二源是谁"不可知 —— 即**放宽/改判第二源合法类型的改动面极小**(一处 guard + schema 的 `human_second_source` 列语义)。第二源到位后 OQ-1 预注册门槛 → 跑 harness → gate 自动转真,零/低代码。

### 视角 C · 产品价值

E1 对"不懂投资 operator"的产品承诺(PRD §3)= 投回测**之前**拿两个真数字:① 密度(已达标 US)② 提取器过不过金标。**金标是"信号质量硬门",与密度 advisory 正交**(handback §3-3)。若 Layer-2 永远验不了,E1 交付物只剩"密度达标"半个数字 —— 提取器可靠性未证 = ROI 结论悬空(§0 防 V4:"不过金标,任何回测都是自欺")。三方向 (a)放宽D-7 /(b)降级验收 /(c)找真人源,对这个真实用户的价值差异,是本轮产品视角要判的。

## 2. First-take 评分(按 Y 视角)

| Y 维度 | 倾向 | 理由(引用 §1 现状) |
|---|---|---|
| 验证方法学/认识论 | **refactor** | D-7 现措辞"真人"把手段(human)当成了目的。原始 G-R1 的真实教训是"**错误正交性**"(纸上蓝图 vs 真跑),不是"碳基 vs 硅基"。D-7 应重述为"第二源错误须与提取器**正交/独立**",再论证什么样的第二源满足;"必须 human"是这条原则在"当年无够强异源模型"下的保守实例化,值得在 2026 异源强模型下重审。**但**——是否真能找到与提取器错误正交的异源模型,是经验问题(P2 SOTA + P3 论证),refactor≠直接放行第二 LLM。 |
| 架构设计 | **keep** | harness/gate/SLA 占位结构本身正确且已 fail-closed,不需改。改动只应发生在"第二源合法类型判据"(`:81` guard + schema 语义),不动验收链骨架。keep 现结构 + 未来在 guard 处做最小放宽。 |
| 产品价值 | **refactor** | 现状(Layer-2 永久 blocked)让 E1 ROI 悬空,对真实用户不可接受。必须给一条"能真跑出 Layer-2 数字"的路——无论 (a)/(b)/(c)。但"降级到只做 Layer-1 + Layer-2 标 known-limitation"(b 的保守版)也是合法产品形态(诚实半验 > 假全验),需权衡 ROI。 |

## 3. 我现在最不确定的 3 件事(留 P2 搜索 / P3 协商)

1. **异源强模型的错误与提取器错误,在"隐性指称→ticker 映射"这个具体任务上,相关性到底多高?** 这是 verdict 的经验支点。我希望 P2 搜:LLM-as-judge 与被判对象同源时的相关误差、跨 vendor/架构模型集成的错误独立性实证、self-preference bias。若证据显示"跨谱系模型在事实性映射任务上错误显著不相关"→ 支持 refactor D-7 到"异源模型可当源";若"再异源也共享训练语料盲点(如冷门 ticker 别名)"→ 支持保 human 或降级。
2. **Layer-2 的映射任务,错误来源是"金融判断"还是"事实性指称消解"?** 若主要是后者(查得到的客观事实:"老黄"=黄仁勋=NVDA CEO),则"懂不懂投资"其实不是门槛,"独立且信息充分"才是 —— 这会松动 §2×D-7 的"互斥"前提本身(operator 配领域小抄后或可胜任,或异源模型胜任)。我希望对方 P3 给我这个视角的洞见:互斥是真的吗,还是被"领域深度"这个措辞夸大了?
3. **元层自证怎么读?** 本 forge 本身 = Claude × GPT-5.6-Sol 两异源模型交叉审"异源模型能否当第二源"。若我俩在 P3 高度收敛且都没揪出对方硬伤 —— 这是"异源够独立"的正面信号,还是"再异源也 echo-chamber"的反面自证?我不确定该把我俩的收敛当证据还是当警讯,希望 P3 显式讨论这层(避免我们自己踩进要审的那个坑)。
