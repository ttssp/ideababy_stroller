# Idea 001-radar · L3R2 · Claude

**Timestamp**: 2026-07-07T01:05:00Z
**Opponent's L3R1 read**: yes
**Searches run**: 4, scope-reality category only
**Model note**: 本轮由 Claude(Fable 5)执笔,文件名沿用管线约定。

## 1. From opponent's candidates — what sharpened my thinking

1. **GPT Candidate C 的裁法比我的更好**:我在 R1 断言"刚冷启动的新方向没有旧地图可 diff",这被证明想窄了——**方向自己的公开研究脉络就是旧地图**。冷启动时重建该方向的历史前后快照("它如何从热词变成结构/为什么没有"),位移就内嵌在单次评估里,不必等用户留驻回访。这直接消解了 intake 张力①,而且比我的 C(位移=留驻后回访)兑现更早。
2. **"30 分钟完成一次初判"作为 success 指标**——把评估延迟当产品属性钉住,我的 R1 只含糊说了"一次咖啡的时间尺度"。
3. **GPT B 的"状态卡组合盘 + 明示覆盖质量"**:允许不同 topic 深浅不一但把覆盖质量标出来,这是"8-15 期望 vs 预算"张力的诚实呈现方式,比我"覆盖靠用长出来"的单一答案多了一个显示层。
4. **taste 反馈故事**(标记 agent 判断是否符合我的 taste,让下一轮更贴)——L2 说品味校准是护城河交集的一角,GPT 把它落成了具体 user story,我的 R1 漏了。

## 2. Scope-reality searches

| Candidate 相关 | Comparable | 它 v0.1 装了什么 / 砍了什么 | 对我们的启示 | URL |
|---|---|---|---|---|
| 冷启动评估官(A 系) | Undermind | launch 即单一动作:agent 式深检索(3-5 分钟,迭代式跟引用),表格/溯源/watch 后加 | 单动作深检索产品被市场接受;"keeps tabs + notify"证明 watch 是成熟的 v0.2 扩展位,不必进 v0.1 | [undermind.ai](https://www.undermind.ai/) · [YC 页](https://www.ycombinator.com/companies/undermind) |
| briefing 延迟预算 | Gemini/OpenAI Deep Research | 5-30 分钟出一份带溯源报告是 2025-26 已被驯化的用户预期,有实时进度流缓解等待 | "评估要等几分钟"不是采用障碍;30 分钟初判的指标现实 | [Gemini Deep Research](https://gemini.google/overview/deep-research/) · [支持文档](https://support.google.com/gemini/answer/15719111?hl=en&co=GENIE.Platform%3DDesktop) |
| 窄切 v0.1 先例 | Connected Papers | 2020 以 side project 发布,launch 只有单种子图一个动作,researcher 圈立刻起量;premium/multi-origin 都是后加 | 这个品类里"一个动作做深"的 v0.1 有直接成功先例 | [post-launch update](https://medium.com/connectedpapers/connected-papers-post-launch-community-update-64d952423d56) · [premium 公告](https://medium.com/connectedpapers/announcing-premium-accounts-multi-origin-graphs-and-more-92e8dbd66848) |
| verdict 词表 + 复盘节奏 | ThoughtWorks Tech Radar | 四环 adopt/trial/assess/hold + "没真用过不能算 assess 完"的 litmus;按期重发,**环间移动就是位移叙事** | 方向评估的结论词表有 20 年验证的先例可借;"按期重评 → 环间移动"正是我们 journal+复盘的形态 | [Tech Radar FAQ](https://www.thoughtworks.com/en-us/radar/faq) · [build your own](https://www.thoughtworks.com/insights/blog/build-your-own-technology-radar) |

## 3. Refined candidates

双方 R1 各三个候选,交叉后收敛为两个;**纯 Radar-first(我 B / GPT B 的重版)被双方独立判死**——超预算 + 首月无价值时刻 + 仪式错位,不再作为候选,只在菜单里留"为什么不选"。

### Refined A′ · "方向评估官(历史位移内嵌版)"
我 R1-A 为骨架 + GPT-C 的公开脉络 diff + Tech Radar 词表。**v0.1 = 单一动作做深**:输入方向 → agent 冷启动重建该方向的公开脉络(含 2-3 个历史时间切片)→ 交付强观点 briefing:结构成型度判断(词表借 radar 环:投入/试点/观察/暂缓)+ "它如何从热词变成结构(或为什么没有)"的**历史位移证据** + 每条判断 3 击内到原文。评估留档进 journal(后验复核)。**不做留驻、不做 re-scan、不做组合盘**——watch 是 v0.2 扩展位(Undermind 先例)。
- 故事新增(vs R1):作为 lab lead,我能看到该方向过去 12-18 个月的结构位移(公开脉络重建),判断它是在成型还是退潮。
- Success:3 个月 ≥5 次真实评估、≥1 次改变投入决策、30 分钟内出初判、journal ≥1 条后验证实。
- 时间:**~9-11 周 @20h(180-220h),盒内有余量**。信心 M+。
- 最大风险:与 Deep Research 类通用工具的差异化要靠"结构成型度框架 + 方法级图证据 + taste 校准",若 briefing 读起来像 Gemini DR 的报告,产品就没了。

### Refined B′ · "评估→组合盘漏斗"
我 R1-C 为骨架 + GPT-B 的状态卡组合盘。A′ 的全部 + 评估完可"留驻":留驻 topic 形成**状态卡组合盘**(结论/关键变化/覆盖质量标注,深浅允许不一),周级轻量 re-scan,回访时给"自基线以来位移"。覆盖从 0 长到 3 个月末 5-10 卡,8-15 是轨迹终点。
- 时间:**~11-13 周 @22-28h(250-330h),贴上沿**。信心 M-。退化路线:第 8 周超支则 re-scan 降手动,回到 A′+留档。
- 最大风险:v0.1 里塞两层机制(评估 + 组合盘),首月交付压力大;组合盘若使用频次低于预期,留驻机制成为死重。

## 4. The single biggest tradeoff human must decide

**位移的来源:公开脉络重建(A′,单次评估内当场兑现)vs 自建基线积累(B′,留驻回访后兑现)。** 等价的问法:v0.1 是一把**每次用完即完整的工具**(评估官),还是一个**越用越厚的系统**(雷达的第一级)?A′ 价值第一天兑现、零维护负担、盒内余量大,但 3 个月末你手里只有一叠评估档案,没有"活的雷达";B′ 朝原始梦想(8-15 张活地图)迈出真实一步,但 v0.1 就背上留驻机制的成本和"组合盘会不会没人回访"的风险。intake 的仪式选择(冷启动评估)和 Connected Papers/Undermind 的窄切先例都指向 A′;operator 对"8-15 覆盖"的期望指向 B′。这是 operator 要拍的板。

## 5. What I'm less sure about now than in R1

1. **"冷启动无 diff 可看"被推翻**——GPT-C 的公开脉络重建让位移在单次评估内可得,我 R1 的三角框架(冷启动×覆盖×位移互斥)其实少画了一条边。
2. **留驻/re-scan 属不属于 v0.1 我不再确定**——Undermind 把 watch 做成后加功能且没伤采用,Tech Radar 用"按期重评"而非持续监控实现位移;也许 B′ 的整个留驻层都该是 v0.2。
3. **延迟预算**:我 R1 写"咖啡时间尺度",市场证据说 5-30 分钟被接受;但"学生开题当场讨论"场景可能需要快慢两档——v0.1 要不要分档,我判断不了,留给 operator/自用数据。
