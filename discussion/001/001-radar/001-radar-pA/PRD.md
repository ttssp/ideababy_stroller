# PRD · 001-radar-pA · "方向评估官（历史位移内嵌）"

**Version**: 1.0  (human-approved via fork)
**Created**: 2026-07-07T02:58:21Z
**Source**: discussion/001/001-radar/L3/stage-L3-scope-001-radar.md · Candidate A
**Approved by**: human moderator
**PRD-form**: simple

## Problem / Context

AI lab 负责人对多个 topic 负有"这方向还值不值得下注"的判断责任,但**每个领域的 big picture 在
悄悄过期**——上次真正吃透某领域可能是八个月前,之后靠 X 碎片、走廊对话、学生转述拼凑。真正的
敌人不是论文数量而是**新增的同质化**:一篇"已有路线的漂亮补丁"和一篇"把两个方法族接起来"的
工作在 feed 里长得一样,而用户要的恰是第二种判断(L2 病灶定义)。

最痛的时刻是**评估一个还没进自己 topic 列表的新方向**(intake 亲选的决策仪式):要不要投一个
学生/一小队?现状是"回去想想一周",既没有结构化证据,也没有历史脉络。本产品把这个时刻变成
"30 分钟拿到可核验的结构成型度判断,当场有据讨论"。

v0.1 是一把**每次用完即完整的工具**(评估官),不是持续运转的雷达系统——位移证据靠**公开脉络
重建**(该方向自己的公开研究时间线就是"旧地图")在单次评估内当场兑现,不依赖用户自建基线。
这是 L3 双方 R2 收敛的裁法,消解了"冷启动 vs 位移"的张力。

## Users

**operator 本人**——AI lab 负责人,每月 1-3 次面临新方向投入决策。特征:自己写代码时间趋近零、
对 8-15 个 topic 负有方向判断责任、已有领域判断力(能读懂结构性 briefing)。
**显式排除**:泛 researcher、领域新人(位移/成型度判断的前提是脑中已有判断坐标系)、团队协作场景。

## Core user stories

1. 作为 lab lead,我能给出一个方向名/种子 paper,在一次咖啡的时间尺度内拿到冷启动评估 briefing,让"回去想想一周"变成"当场有据讨论"。
2. 作为 lab lead,我能看到该方向过去 12-18 个月的结构位移(公开脉络重建的 2-3 个历史切片),判断它在成型还是退潮——而不只看当前热度。
3. 作为 lab lead,我能点开 briefing 里任何一个判断,看到支撑它的节点/边/原文出处,自己核验 agent 有没有胡说。
4. 作为 lab lead,我能把评估结论(投/观望/不投 + 日期 + 理由)留档进 journal,三个月后回看当时判断对不对。
5. 作为 lab lead,我能标记 agent 的判断是否符合我的 taste,让下一轮评估更贴近我的标准。

## Scope IN (v0.1)

- 冷启动 pipeline:方向输入 → 检索收集 → 方法/claim 级图构建(单方向、量级小)+ 2-3 历史时间切片重建
- 结构成型度 briefing(判断 + 历史位移证据链,可展开)· 结论词表借 Tech Radar 环(投入/试点/观察/暂缓)
- 证据链强制(每条判断 3 击内到原文)+ 低置信标注
- 评估 journal(后验复核)+ taste 反馈标记
- 3-5 次真实评估跑通(operator 自用验证)

## Scope OUT (explicit non-goals)

- **常驻 8-15 topic 持续跟进 / 留驻 / re-scan / 组合盘**——那是 Candidate B(数据驱动的 v0.2);A 里 topic 地图是评估副产物,不做后台持续 ingest
- **watch / re-scan**——v0.2 扩展位(Undermind 先例:watch 后加且没伤采用)
- 跨 topic 视图、方法迁移检测、区域 alert、任何 push / 每日 feed
- 问答 / 报告生成器(不撞 Elicit/Undermind/OpenScholar 的 synthesis 面)
- 全覆盖(不把 arxiv 全量塞进图)· lab 共享 / 团队协作 · 账号 / 计费

## Success — observable outcomes

- **O1** 3 个月内完成 ≥5 次真实新方向评估,其中 ≥1 次实际改变了 operator 的投入决策
- **O2** 任一 briefing 的任一判断都能在 3 次点击内到达原文证据
- **O3** 30 分钟内出初判(评估延迟是产品属性,不是实现细节)
- **O4** 对 operator 已深耕方向做盲测评估,briefing 判断与其一致或给出其认可的新信息(信任校准)
- **O5** journal ≥1 条"当时 briefing 判断 → 后验证实"记录(信任第一块砖)

## Real-world constraints

| # | Constraint | Source |
|---|------------|--------|
| C1 | 时间盒 2-3 月 · 周工时 15-30h · 预算约 130-360h(本 cut 估 ~9-11 周 @20h,盒内有余量) | L3R0 intake Block 1 |
| C2 | 平台:v0.1 CLI/terminal 出 markdown briefing → v0.2 本地 Web 视图(证据展开更完整);技术选型留 L4 | L3R0 intake Block 4 + L3 菜单 ❓ 决定 |
| C3 | 商业模式:自用起步(无账号/无计费,scope 最小);商业化不绑架 v0.1 scope | L3R0 intake Block 3 + L3 菜单 ❓ 决定 |
| C4 | 红线:不追全覆盖(硬)· 不做问答/报告生成器 · 不做 push/每日 feed · 不做真理机(无证据判断标低置信)· 不面向新人 · 不做 lab 共享 | L3R0 intake Block 5 + L3 双方收敛 |

## UX principles (tradeoff stances)

- 判断先行,证据随取;宁可 briefing 观点强 + 标不确定度,不做四平八稳综述
- 单次评估体验 > 长期库完整性;不为未来的常驻功能预留 UI 复杂度
- 宁可少做几次深评估,也不给很多浅结论

## Biggest product risk

与 Deep Research 类通用工具(Gemini/OpenAI DR)的差异化,全押在**结构成型度框架 + 方法级图证据 +
taste 校准**三样的交集上。如果 briefing 读起来像 Gemini Deep Research 生成的一份带溯源报告,产品
就没了独占空间。这是产品级/差异化风险,不是技术风险——缓解靠"结构成型度"这个独有判断文体 +
位移叙事 + 品味校准,而不是靠把检索做得更全。

## Open questions for L4 / Operator

1. **延迟预算是否分快慢两档**(30 分钟初判 vs 学生开题当场讨论要更快档)——建议 v0.1 单档,自用数据说话。非骨架决定,不阻塞。
2. **briefing 结论词表最终形态**(借 Tech Radar 四环起步,分几级/用什么词需拿真产出给 3-5 同行看反应)——v0.1 中后期非正式验证,不阻塞。
3. ⚠ **共享地基假设(L3 honesty check · L4 应最先验证)**:"公开脉络重建"能否产出**可信的**历史位移证据,在 L3 层未经验证——这是 A 差异化的潜在返工点。L4 spec 应把"对 1-2 个 operator 已深耕的方向重建历史切片并人工核验"列为最早的验证性任务(相当于本项目的 PPV 锚点),不要把它排在管线深处。

---

## PRD Source
This PRD was auto-generated from L3 fork. Contents are derived from the
approved L3 candidate. For full context (why this cut vs siblings, scope-
reality verdict, comparison matrix), see:

- L3 menu: discussion/001/001-radar/L3/stage-L3-scope-001-radar.md
- L2 unpack: discussion/001/001-radar/L2/stage-L2-explore-001-radar.md
- FORK-ORIGIN.md in this directory

This PRD is the **source of truth** for L4 (spec-writer). Changes to PRD
require explicit human approval — never auto-revised by L4 agents.
