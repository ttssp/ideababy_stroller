# Idea 001-radar · L3R2 · GPT-5.5 xhigh

**Timestamp**: 2026-07-07T02:23:16Z
**Opponent's L3R1 read**: yes
**Searches run**: 15 queries, scope-reality category only; evidence current to 2026-07

## 1. From opponent's candidates — what sharpened my thinking

- Claude 的 Candidate C 比我的 C 更顺：它把“冷启动”定义成“雷达第一帧”，于是冷启动与位移不再互相抢主位。这应成为保留候选。
- Claude 对 Candidate B 的质疑更硬：8-15 topic 持续雷达不仅贴预算上沿，还会在首月没有位移价值时刻。我的 B 写得偏乐观，R2 应明确降级为高风险 cut。
- Claude 的“pull 内置顶提示，不做 push”裁法解决了 alert 红线：v0.1 不做每日 feed，但允许打开时把显著变化置顶。
- 我方 R1 的“公开脉络 diff”仍应保留，但应降为证据形态，不单独成为主产品。否则它会拖慢冷启动，并让用户先看复杂变化而不是先拿判断。

## 2. Scope-reality searches

| Candidate pressure | Comparable product / source | What similar products include | What they cut / do not foreground | URL |
|---|---|---|---|---|
| 图谱与监控已是常规能力 | Litmaps | 搜索大论文库、按引用/参考关系找相关工作、可视化、分享、监控新文章邮件 | 不以前沿“结构成型度判断”作为主 payload；图和监控是中心 | https://www.litmaps.com/features |
| 探索型 paper map 已成熟 | ResearchRabbit | 个性化推荐、topic/collection 组织、paper/author/concept 互动地图、趋势探索 | 不把“该不该投一个方向”绑定到 lab lead 决策仪式 | https://www.researchrabbit.ai/features |
| 报告/问答面竞争很挤 | Elicit | 搜索、研究报告、系统综述筛选/抽取、library、alerts、句级引用透明度 | 它做 research brief，但不是方法/claim 位移雷达；若 001-radar 变通用报告，会正面撞车 | https://elicit.com/ |
| 深度研究 agent 已覆盖 novelty/gap | Undermind | 描述问题、深入搜文献、迭代报告、引用核验、更新提醒、novelty/gap/scoping 用例 | 不以私有 topic 地图的时间位移为主；但“评估复杂方向”已被它纳入话术 | https://www.undermind.ai/ |
| AI 文献工具的信任底线变高 | 2026 evaluation paper | 早期探索有价值，但精准抽取、可复现性、透明度仍是痛点，用户仍需核验 | 不能只给强判断；每个判断必须带可核验证据，否则信任烧得很快 | https://arxiv.org/abs/2605.10125 |
| citation-backed synthesis 不是空白 | OpenScholar | 从大量开放论文中找相关段落并合成带引用回答；评测强调 citation accuracy | “带引用的文献综述”不是差异点；差异必须落在方向位移和决策语境 | https://arxiv.org/abs/2411.14199 |
| contribution/prerequisite graph 学术侧逼近 | Scientific Contribution Graph | contribution 节点、prerequisite 边、大规模 roadmapping 资源 | 方法/贡献级图语义不能单独当护城河；v0.1 要卖判断仪式，不卖图谱本身 | https://arxiv.org/abs/2605.15011 |

净读法：相邻产品的 v0.1/成熟主面通常先做“发现、保存、图、报告、提醒、引用透明”。用户不会想念 team admin、billing、lab 共享、复杂协作、全量覆盖；但会马上要求证据可追溯。001-radar 的可活空间不是再做 paper discovery，而是把这些能力收束到“新方向是否成型、是否下注”的窄仪式。

## 3. Refined candidates

### Candidate A · “冷启动评估官”

**v0.1**：输入方向名或少量种子 work，产出一份强观点 briefing：结构是否成型、核心问题簇/方法簇是什么、可投/观察/暂缓、理由和不确定性。图/diff 只作为证据展开，评估结果保存为候选 topic 基线。  
**Persona**：每月数次判断新方向是否值得投入学生/小队的 AI lab lead。  
**Stories**：可在一次评估会前拿到初判；可展开每条判断的证据；可保存当时结论供后验复核；可对已熟方向盲测校准。  
**IN**：4-6 次真实冷启动评估；结构成型度 briefing；证据链；决策 journal；低置信标注。  
**OUT**：8-15 常驻 topic、自动 alert、团队共享、开放问答、每日 feed。  
**Success**：至少 5 次评估中 1 次改变投入判断；operator 认为 3 份 briefing 抓住结构而非罗列论文。  
**Time**：8-10 周，160-240h，信心 M。  
**UX**：判断先行，证据随取；宁可少而深。  
**Risk**：若成型度框架不够尖，它会退化成一次性调研报告。

### Candidate B · “评估→留驻漏斗”

**v0.1**：冷启动评估是入口；评估后用户选择留驻或归档。留驻 topic 保存第一帧，后续打开时看到“自基线以来”的位移 briefing，并能回看当初判断是否被后续事实支持。  
**Persona**：既要评估新方向，也希望少数已认可方向不再从脑内过期的 research lead。  
**Stories**：评估新方向；一键留驻；回访留驻 topic 看变化；用 journal 校准 agent 的品味。  
**IN**：A 的冷启动核心；留驻/归档；5-8 个留驻 topic；手动或低频回访位移；pull 内置顶显著变化。  
**OUT**：一次性导入 15 topic、push 通知、跨 topic 迁移、团队协作。  
**Success**：3 个月末 ≥5 次评估、≥4 个留驻 topic 有第二帧、≥1 次回访位移给出 operator 未注意到的变化。  
**Time**：10-12 周，220-310h，信心 M-。  
**UX**：冷启动是价值时刻，位移是回访奖赏。  
**Risk**：机制比 A 重；若留驻 topic 不够，radar 感会弱。

### Candidate C · “8-15 组合盘点”

**v0.1**：直接维护 operator 的 8-15 topic 组合，每个 topic 是轻量状态卡：当前判断、关键变化、下一步动作、证据链接。冷启动用于把新方向纳入组合，但深度让位于覆盖。  
**Persona**：最痛的是“我同时管太多方向”的 lab lead。  
**Stories**：一次复盘扫过 8-15 topic；挑出需行动的 2-3 个；新增方向后决定纳入/观察/不纳入；标记判断是否符合 taste。  
**IN**：8-15 状态卡；组合层优先级；轻量冷启动；人工确认/反驳。  
**OUT**：深 claim 图、强成型度审判、完整 diff、alert、共享。  
**Success**：一次固定复盘能产出明确行动清单；70% 状态卡被认为足够支持下一步判断。  
**Time**：12-14 周，300-400h，信心 L；超出 2-3 月盒子的风险高。  
**UX**：广度优先，深浅透明。  
**Risk**：最容易变成浅 dashboard，且首月价值兑现慢。

## 4. The single biggest tradeoff human must decide

真正的轴不是“图 vs briefing”，而是：**v0.1 要先证明一个高信任方向判断，还是先兑现 8-15 topic 的组合覆盖承诺**。A 选择少数方向、强判断、快价值；C 选择覆盖面、组合复盘、慢价值；B 试图把二者接起来，用“评估后留驻”把 8-15 变成使用轨迹而非首发交付。若 human 的第一优先级是验证差异化和信任，选 A 或 B；若第一优先级是马上替代现有脑内 portfolio，才选 C，但要接受预算和浅化风险。我的 R2 倾向：B 是最稳的 product thesis，A 是最稳的验证 cut，C 是最像愿景但最不适合 v0.1 的 cut。

## 5. What I'm less sure about now than I was in R1

- 我更不确定 8-15 topic 应作为 v0.1 硬交付。市场现实显示提醒和 library 常见，但可信判断才是稀缺；topic 数可能是虚荣完整性。
- 我更担心“briefing”撞上 Elicit/Undermind。必须把 briefing 限定成“结构成型度/是否下注”，不能泛化成 research report。
- 我不再坚持完全不碰 alert：v0.1 不做 push，但 pull 内显著位移置顶可能是合理例外。
- 我对“公开脉络 diff 优先”的信心下降；它是好证据，但不应压过冷启动判断的首月价值时刻。
