# PRD · 001-radar-pA · "方向评估官（历史位移内嵌）"

**Version**: 1.1  (human-approved revision)
**Created**: 2026-07-07T02:58:21Z
**Revised**: 2026-07-11 · v1.0→v1.1:P0.2 盲测门首判 FAIL(handback `001-radar-pA-20260711T135303Z`)决议 + moderator injection(`../L3/moderator-notes.md` @2026-07-10T08:19:13Z)——O4 两层化 + 要件③重 operationalize + 语义切窗/分层阅读原则
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

- 冷启动 pipeline:方向输入 → 检索收集(**分层阅读**:全量元数据+abstract;全文仅对位移锚点论文或 O2 证据链核验时选择性深读)→ 方法/claim 级图构建(单方向、量级小)+ 2-3 历史时间切片重建(**语义切窗**:切片边界贴领域结构事件,不按论文数量均分——数量均分稀释信息密度,P0.2 首跑 FAIL 实证)
- 结构成型度 briefing(判断 + 历史位移证据链,可展开)· 结论词表借 Tech Radar 环(投入/试点/观察/暂缓)
- 证据链强制(每条判断 3 击内到原文)+ 低置信标注
- 评估 journal(后验复核)+ taste 反馈标记
- 3-5 次真实评估跑通(operator 自用验证)

## Scope OUT (explicit non-goals)

- **常驻 8-15 topic 持续跟进 / 留驻 / re-scan / 组合盘**——那是 Candidate B(数据驱动的 v0.2);A 里 topic 地图是评估副产物,不做后台持续 ingest
- **watch / re-scan**——v0.2 扩展位(Undermind 先例:watch 后加且没伤采用)
- 跨 topic 视图、方法迁移检测、区域 alert、任何 push / 每日 feed
- 问答 / 报告生成器(不撞 Elicit/Undermind/OpenScholar 的 synthesis 面)
- 全覆盖(不把 arxiv 全量塞进图)· **全量全文抓取**(分层阅读红线:abstract 全量、全文只深读锚点)· lab 共享 / 团队协作 · 账号 / 计费

## Success — observable outcomes

- **O1** 3 个月内完成 ≥5 次真实新方向评估,其中 ≥1 次实际改变了 operator 的投入决策
- **O2** 任一 briefing 的任一判断都能在 3 次点击内到达原文证据
- **O3** 30 分钟内出初判(评估延迟是产品属性,不是实现细节)
- **O4** 信任分两层校准(v1.1 重写,per P0.2 首跑 FAIL 决议 + moderator injection):
  - **初始层 · P0.2 盲测 gate = smoke test**:对 operator 已深耕方向(含封闭历史窗回溯形态)盲测,三要件:①真切片全判"可信" ②注入的阴性对照被正确识伪 ③点名 ≥1 条**新证据链**(定义见下)。PASS = 地基无明显烂、解锁 Phase 1+,**不是**可信性终审;FAIL → prd-revision-trigger STOP 铁律(不降级续建,防 V4)。
  - **长期层 · 信任主锚**:靠使用中持续校准兑现——O2(任一判断 3 击回溯原文)+ O5(journal 后验复核 + taste 标记)承担;非 gate 一次发证。
  - **「新证据链」operationalize(要件③)**:以下任一,且可顺 O2 三击核验:(i) operator 读前不知道的新事实 claim;(ii) operator 已知事实间**未见过的结构连接**(如"方法族 A 的技术 X 被领域 B 借入解决问题 C"的具体链条)。纯词频常识综述两者都产不出——要件③可达但仍有牙。
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
3. ⚠ **共享地基假设(v1.1 更新:已部分兑现,问题演进)**:P0.2 盲测 gate 已建成并首次真跑(2026-07-11 · diffusion models · 封闭历史窗 2021→2023):识伪 ✅(阴性对照被精准命中,反橡皮图章机制有牙)、真切片可信 ✅、新洞察 ❌ → FAIL 触发本次 v1.1 修订。问题演进为 **P0.2 重跑协议**:pipeline 落地语义切窗 + abstract 输入后重跑;可换方向/换历史窗多轮盲测提升统计功效(单轮 3 切片 1 负控,瞎猜命中率 1/3);重跑 PASS 才解锁 Phase 1+(T010/T011)。FAIL→STOP 铁律不变。

---

## Moderator injection response

(回应 `../L3/moderator-notes.md` · Injection @2026-07-10T08:19:13Z · hard constraint;本节即 injection 要求的强制回应,operator 已批准)

1. **gate 语义右调 → 采纳**:P0.2 盲测 gate 定位「初始 smoke test」,只挡"地基明显烂还继续烧预算"(防 V4);PASS 解锁 Phase 1+ 语义保留,但不宣称位移重建可信性终审证成。已落 O4 初始层。
2. **长期质量主锚移 O2 + O5 → 采纳**:「结论可回溯」由 O2(3 击到原文)落地;「使用中反馈偏差」由 O5(journal 后验复核 + taste 标记)落地——信任是使用中校准出来的,非 gate 发证。已落 O4 长期层。(注:XenoDev spec 侧对应编号为 O2/O7,映射由 spec-writer 维护,PRD 不追 spec 编号。)
3. **历史窗回溯验证 → 采纳且已实装**:封闭历史窗(`--from-date/--to-date`,XenoDev T002-A1,102 tests green 待 ship)成为盲测标准形态——拿 operator 已知答案的深耕期窗口考管线,信号强于近期窗。P0.2 首跑即用此形态。
4. **KG-B4 机器强制语义 → 确认**:强制的是「FAIL 不降级续建」(STOP 铁律);非「一次 PASS 永久免检」。gate 类 task 的机器强制设计按此语义执行(XenoDev 侧 dogfood-backlog 在册,攒批走 forge 006)。

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
