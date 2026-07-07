# Idea 001-radar · L2R2 · GPT-5.5 xhigh · Cross + Value Validation

**Timestamp**: 2026-07-06T13:27:40Z
**Opponent's L2R1 read**: yes
**Searches run**: 8, value-validation only

## 1. From opponent's L2R1, what sharpened my thinking

1. Opus 把用户痛点说成“PI 脑中的 big picture 在悄悄过期”，比我 R1 的“信息过载”更准。真正的 job 不是读得更快，而是避免自己用过期地图做方向判断。
2. “第一屏不是图本身，是位移”这个表述 sharpen 了产品重心。图谱只是底图；用户买的是两个时间切片之间的解释性 diff。
3. “判断的外骨骼”比“第二记忆”更有力：它暗示 KG-radar 不只是保存知识，而是让 lab lead 在组会、砍方向、开题时把判断外化成可争论物。
4. Opus 对 trust 的提醒很关键：contradicts / supersedes 这类边不是事实，而是判断。地图必须暴露不确定性，否则一个显眼错边会烧掉信任。

## 2. Where I'd push back on opponent's L2R1

1. “它不该是每日简报”说得略绝对。001-pA 式 feed 不是主形态，但 map-region alert 很自然：当某个关键节点周边发生位移时提醒 PI，不等于退回每日新闻流。
2. “方法级节点”不能再当强 novelty。2026 年已有 contribution-level / claim-level 研究近邻；真正差异应是“持续位移 + lab 决策语境 + taste calibration”。
3. “一百万人用它会形成公共物件”可能过宽。更可信的初始价值是 lab-local private map：不同 lab 对“重要”的判断不同，公共地图反而可能稀释品味。

## 3. Search-based reality check

| Claim | Source side | What I searched | What I found | Verdict |
|---|---|---|---|---|
| Connected Papers / Litmaps / ResearchRabbit 类工具没有覆盖 KG-radar 的核心差异 | Both | Prior art: Litmaps, ResearchRabbit, Elicit, Undermind, Scientific Contribution Graph | Litmaps 已有 citation/reference-based search、visualize、monitor new articles（https://www.litmaps.com/features）。ResearchRabbit 明确说 visual maps 可看 papers/authors/concepts interconnect 和 ideas evolve over time（https://www.researchrabbit.ai/features）。Elicit 有 reports、alerts、Research Agent、sentence-level citations（https://elicit.com/）。Undermind 主打 novelty、gaps、emerging trends、cross-disciplinary insights（https://undermind.ai/）。同时 2026 Scientific Contribution Graph 已做 contribution nodes + prerequisite edges（https://arxiv.org/abs/2605.15011）。 | 部分成立。消费级工具多仍围绕 paper discovery/review/search；但“方法/贡献级图谱”已有研究近邻，不能当独占 novelty。 |
| 研究者/PI 被论文洪水淹没，需求强 | Both | Demand signals: paper volume, AI-generated survey flood, research synthesis tools | Guardian 2025 报道 indexed papers 2015-2024 从 1.71M 到 2.53M，并称 researchers/peer review overwhelmed（https://www.theguardian.com/science/2025/jul/13/quality-of-scientific-papers-questioned-as-academics-overwhelmed-by-the-millions-published）。NeurIPS 2025 position paper 直接把 AI-generated surveys 称为对 research community 的 DDoS，并主张 dynamic live surveys（https://arxiv.org/abs/2510.09686）。Elicit 自称 5M+ researchers，说明该类痛点已有大市场信号。 | 强成立。需求不是假想，但市场已拥挤。 |
| claim / contradiction 关系仍是空白 | Both, especially moderator notes | Prior art: scite, scientific claim/contribution graphs | scite 早已围绕 supporting / disputing(or contrasting) / mentioning citations 建立 smart citation 视角；相关论文使用 scite citation index 分析 supporting/disputing/mentioning（https://arxiv.org/abs/2104.08087）。Scientific Contribution Graph 也指出 paper-level citations 与 sentence triples 之间有 representation gap，并提出 contribution-level roadmapping。 | 不成立。edge label 本身不是 novelty；KG-radar 要胜在把这些关系组织成可用的位移判断。 |
| 研究趋势 dashboard 容易变成没人看第二次的装饰 | Both | Failure cases: dashboard usability/evaluation literature | Dashboard 研究指出用户常遇到理解和验证信息的困难，且用户 literacy 与 dashboard 所需 literacy 不匹配，需求还会移动（https://arxiv.org/abs/2209.06363）。另有 mixed-initiative visualization 失败评估案例，问题包括 interface design 和对用户预期错误（https://arxiv.org/abs/2009.06019）。 | 警告成立。KG-radar 必须服务明确决策 ritual，而不是只做漂亮地图。 |
| AI literature synthesis agent 会直接压到 KG-radar | GPT R1 implied, Opus less emphasized | Prior art: OpenScholar, Elicit, Undermind | OpenScholar 面向 scientific query synthesis，覆盖 45M open-access papers，并强调 citation-backed responses（https://arxiv.org/abs/2411.14199）。Elicit/Undermind 已经把 search、report、alerts、gap finding 做到产品层。 | 高竞争压力。KG-radar 应避免做“问答/报告生成器”，专注 temporal structure + lab-local judgment。 |

## 4. Refined picture

验证后，我会把 KG-radar 收窄成：**面向 AI lab lead 的 topic displacement system**。它不是通用文献搜索、不是 systematic review、不是 citation graph 竞品，也不是每日简报；它维护 8-15 个 lab-critical topic 的活地图，并把“过去一段时间哪些方法/claims/问题簇的地位改变了”变成组会、季度复盘、开题讨论能直接使用的判断材料。

这条路仍值得继续，但 verdict 是 **Y-with-conditions**。条件一：不要把“方法级 KG”当护城河，2026 已有近邻；差异必须落在持续时间维度的位移叙事。条件二：目标用户必须是有方向判断责任的 lab lead / research lead，而不是泛 researcher。条件三：每张图都要导向一个 decision ritual：该读什么、该停什么、该补什么、哪个假设变弱、哪个 frontier 变强。没有 ritual，它会被 Litmaps/ResearchRabbit 的图、Elicit/Undermind 的报告、scite 的 citation semantics 分别拆掉。

## 5. Open questions that L2 cannot answer

1. v0.1 应该选哪个 first topic：RLHF / agents / eval / multimodal / model efficiency？这需要 operator 的真实 lab 关注和痛感排序。
2. “位移”第一屏到底是 map diff、文字 briefing、变化列表，还是组会问题清单？这需要用户试用，不是 L2 想象能定。
3. lab lead 是否愿意每周打开 pull-style map，还是必须由 high-signal alert 拉回？这会影响 L3 scope。
4. 可信度呈现的最低要求是什么：边级置信、来源证据、反例、人工确认状态，还是只需保守表达？

## 6. Three things I'd want a real user interview to ask

1. 过去三个月里，你在哪一次方向判断中明显感觉“我脑中的领域地图可能过期了”？当时你怎么补救？
2. 如果给你一张 topic 位移图，你会在什么会议或决策里真的打开它：组会、one-on-one、grant、talk、招聘、砍方向？
3. 对你来说，一条“DPO 往 online 漂移”这类判断要配多少证据，你才敢在组会里引用它？
