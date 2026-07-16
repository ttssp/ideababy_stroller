# PRD · 001-radar-pA · "方向评估官（历史位移内嵌）"

**Version**: 1.4  (human-approved revision)
**Created**: 2026-07-07T02:58:21Z
**Revised**: 2026-07-11 · v1.0→v1.1:P0.2 盲测门首判 FAIL(handback `001-radar-pA-20260711T135303Z`)决议 + moderator injection(`../L3/moderator-notes.md` @2026-07-10T08:19:13Z)——O4 两层化 + 要件③重 operationalize + 语义切窗/分层阅读原则
**Revised (v1.2)**: 2026-07-13 · operator 价值重定义(injection @2026-07-13T10:43:29Z):gate 硬门槛收敛为要件①②,要件③降级为使用期校准信号;Candidate B 诉求记 v0.2 展望
**Revised (v1.3)**: 2026-07-16 · forge 001 v1 verdict(`discussion/001/forge/v1/stage-forge-001-v1.md` · hand-back `001-radar-pA-20260715T093226Z` 决议链):P0.2 人肉盲测二值签字 gate 从 T010/T011 前置退役(采纳 KG-B8),改机器可判最小验收三项;识伪降为零解锁语义的可选校准;FAIL→STOP 双道保留
**Revised (v1.4)**: 2026-07-16 · forge 001 v2 verdict(`discussion/001/forge/v2/stage-forge-001-v2.md` · hand-back `001-radar-pA-20260716T085807Z` 决议链):v1.3「机器可判三项」中 ①② 因循环依赖(KG-B9,XenoDev 真跑证实)退役出 T010/T011 解锁前置,重绑 T021/T022 ship 验收 + O2/O7 使用期抽查;新解锁前置 = a1 per-slice source 映射单一谓词,生效条件写死「真 briefing rerun 自证 PASS」
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

- **常驻 8-15 topic 持续跟进 / 留驻 / re-scan / 组合盘**——那是 Candidate B(数据驱动的 v0.2);A 里 topic 地图是评估副产物,不做后台持续 ingest(**v1.2 注**:operator 2026-07-13 明示「跟踪动态/及时同步有价值内容」为其核心诉求——Candidate B 复活信号已确认,v0.1 用起来后优先评估 v0.2 转向)
- **watch / re-scan**——v0.2 扩展位(Undermind 先例:watch 后加且没伤采用)
- 跨 topic 视图、方法迁移检测、区域 alert、任何 push / 每日 feed
- 问答 / 报告生成器(不撞 Elicit/Undermind/OpenScholar 的 synthesis 面)
- 全覆盖(不把 arxiv 全量塞进图)· **全量全文抓取**(分层阅读红线:abstract 全量、全文只深读锚点)· lab 共享 / 团队协作 · 账号 / 计费
- **人肉盲测二值签字作解锁闸门**(v1.3 注:operator 真跑拒签 + SOTA 无此先例形态 + KG-B8 采纳)· **四样本 certification 语义**(统计功效只够 smoke)· **review queue / journal 回溯作阻断前置**(全归使用期治理,否则重造更宽 gate)· **KG-B7 反作弊面的进一步投资**(现状冻结,不删已 ship 代码)
- **trace schema 完整性 / 证据 3 击可达性作 T010/T011 解锁前置**(v1.4 注:循环依赖 KG-B9——trace 底料由 gate 下游的 T011/T021 产,真 briefing 零 trace token;两项本身不删,迁 Phase 2 出口验收 + 使用期抽查)

## Success — observable outcomes

- **O1** 3 个月内完成 ≥5 次真实新方向评估,其中 ≥1 次实际改变了 operator 的投入决策
- **O2** 任一 briefing 的任一判断都能在 3 次点击内到达原文证据
- **O3** 30 分钟内出初判(评估延迟是产品属性,不是实现细节)
- **O4** 信任分两层校准(v1.4 修订,per forge 001 v2 verdict @2026-07-16;v1.3「机器可判三项」因循环依赖 KG-B9 废止——①② 的底料由 gate 下游的 T011/T021 产,真 briefing 无字可判):
  - **初始层 · T010/T011 解锁前置 = a1 单一谓词(同批解锁)**:a1(per-slice source 映射最小前移——管线生成叙事时保留 slice→source refs;走 P0.1 amendment 通道,不建图不做 judge,不违 RT-2)落地后,机器秒级判三件:
    ① briefing 带 per-slice source 映射且逐项可解析到检索语料;
    ② 轻量审计通道结构就位(a1 后非空壳,内有 slice 源映射可查;最小**文件级**,v0.1 不得膨胀为重基础设施);
    ③ 产物命名一致。
    **生效条件(写死)**:谓词须在**现有真 briefing rerun 上自证 PASS** 方可生效;合成 fixture 仅作回归测试,不得替代生效自证(「前置 gate 形态」连续两次被现实打回后的硬要求)。
    **解锁语义(显式)**:一次性 stage-0 治理动作 + 最小机器谓词,不承担 certification;**自托管点条款**:Phase 2 出口(T021/T022)完整 trace 验收生效后,机器验收面从 a1 谓词升级为完整 trace 验收。
  - **原 ①② 迁移(退役出解锁前置,资格改写非删除)**:trace/provenance schema 完整性 + 证据 3 击可达性重绑两处——T021/T022 ship 验收(其验收测名字面即此两项,底料彼时天然存在)+ O2/O7 使用期抽查对象(生产 trace 抽样审计,贴「边用边抽查」工作流)。
  - **FAIL→STOP 双道**:机器道 = a1 谓词任一 FAIL → pipeline 内自动阻断下游(须**代码级 wiring**;wiring 对象 = a1 映射 + 审计通道结构 + 治理 STOP 记录,全为真实存在的文件级 artifact = KG-B4 改写落点更新);治理道 = operator 使用期抽查发现叙事级造假/系统性失真 → 既有 prd-revision-trigger hand-back 通道(流程级 STOP)。
  - **识伪盲测 = 可选的使用期校准活动**(retire-as-gate, keep-as-calibration):operator 自发起、无签字模板、无 PASS/FAIL 裁决;产出**只写 journal 作校准证据,零解锁语义**(封死借尸还魂回前置)。要件③(新证据链)schema 保留于校准活动内(v1.2 语义延续)。四样本级别的活动只承担 smoke 诊断,**不承担 certification 语义**(若未来要认证,按目标功效反推样本量)。
  - **长期层 · 信任主锚**(v1.2 延续并强化):O2(任一判断 3 击回溯原文,**升级为验收机制**)+ O5(journal 后验复核 + taste 标记)+ operator 使用期抽查(非盲判)承担;非 gate 一次发证。
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
3. ⚠ **共享地基假设(v1.4 更新:循环依赖续裁)**:「机器可判三项作 T010/T011 解锁前置」的 v1.3 表述**废止**(XenoDev 真跑证实 ①② 无底料可判,循环依赖 = KG-B9;v1.3 的落地前置警告预言命中,verdict 自定义 STOP 出口被正当触发)。新解锁前置 = O4 初始层 **a1 单一谓词**(T010/T011 同批解锁);原 ①② 迁 T021/T022 ship 验收 + O2/O7 使用期抽查。历史盲测证据用途不变(校准活动历史样本入 journal);多轮盲测 = 可选校准,不挡解锁。FAIL→STOP 铁律以双道形态保留;机器道 wiring 对象更新为 a1 映射 + 审计通道结构 + 治理 STOP 记录(KG-B4 改写落点)。⚠ 新落地前置警告(forge v2 §underweights):「a1 谓词秒级可判」与「①② 在 Phase 2 出口可判」仍是推演——故生效条件已写死为真 briefing rerun 自证 PASS(不达标按双道回流,触发 forge v3);a1 动冻结 TimeSlice,实装前须逐面 grep 枚举消费面(forge-lite 教训:序列化面最易 silent 丢)。

---

## Moderator injection response

(回应 `../L3/moderator-notes.md` · Injection @2026-07-10T08:19:13Z · hard constraint;本节即 injection 要求的强制回应,operator 已批准)

1. **gate 语义右调 → 采纳**:P0.2 盲测 gate 定位「初始 smoke test」,只挡"地基明显烂还继续烧预算"(防 V4);PASS 解锁 Phase 1+ 语义保留,但不宣称位移重建可信性终审证成。已落 O4 初始层。
2. **长期质量主锚移 O2 + O5 → 采纳**:「结论可回溯」由 O2(3 击到原文)落地;「使用中反馈偏差」由 O5(journal 后验复核 + taste 标记)落地——信任是使用中校准出来的,非 gate 发证。已落 O4 长期层。(注:XenoDev spec 侧对应编号为 O2/O7,映射由 spec-writer 维护,PRD 不追 spec 编号。)
3. **历史窗回溯验证 → 采纳且已实装**:封闭历史窗(`--from-date/--to-date`,XenoDev T002-A1,102 tests green 待 ship)成为盲测标准形态——拿 operator 已知答案的深耕期窗口考管线,信号强于近期窗。P0.2 首跑即用此形态。
4. **KG-B4 机器强制语义 → 确认**:强制的是「FAIL 不降级续建」(STOP 铁律);非「一次 PASS 永久免检」。gate 类 task 的机器强制设计按此语义执行(XenoDev 侧 dogfood-backlog 在册,攒批走 forge 006)。

### v1.2 response(Injection @2026-07-13T10:43:29Z · operator 价值重定义)

1. **gate 硬门槛收敛①② → 采纳**:P0.2 判 PASS/FAIL 只看真切片可信 + 识伪命中;已落 O4 初始层。
2. **要件③降级使用期校准 → 采纳**:new_evidence_chain schema 保留、gate 记录但不挡 PASS;进 O5 journal/taste 闭环学习 operator 个人边界。已落 O4。
3. **Candidate B 展望 → 记档不转向**:「跟踪动态/及时同步」诉求记入 Scope OUT v1.2 注(v0.2 优先评估项);v0.1 维持单次评估工具。
4. **首跑证据处置 → 移交 XenoDev**:v1.2 语义下首跑①②实证构成 PASS 证据;复用 or 快速重判由 build 侧按 anti-replay 设计定。

### v1.3 response(forge 001 v1 verdict @2026-07-16 · `../../forge/v1/stage-forge-001-v1.md`)

(回应 hand-back `001-radar-pA-20260715T093226Z` 三条批评 · 双专家 strong-converge · operator 已批准落地)

1. **P0.2 盲测二值签字退役 → 采纳 KG-B8**:解锁前置改 O4 机器可判三项;operator 从「一次性考官」移位「使用期抽查者 + journal 校准」(批评①②③的直接落地;SOTA 无「人肉盲测二值作阻断闸门」先例)。已落 O4 初始层。
2. **FAIL→STOP 双道保留 → 防 V4 精神不丢**:机器道(可复现失败自动阻断,须代码级 wiring = KG-B4 改写落点)+ 治理道(prd-revision-trigger 通道;本次 forge 自身即该通道运转实证)。已落 O4。
3. **识伪 keep-as-calibration → 采纳**:零解锁语义、产出只入 journal;KG-B7 反作弊面现状冻结不再投资(吸取 T004-A1 十四轮硬化被 B8 推翻前提的过度投资教训)。已落 O4 + Scope OUT。
4. **XenoDev 落地路径**:spec §5/§6 + dependency-graph 前置重定义 + gate.py/injector.py 降级校准工具 + trace-validator 新增 + journal/抽查记录最小 schema,参 stage 文档 §Refactor plan 四模块(A:M · B:S · C:M · D:S);**落地前先用一次真 briefing 验证三项 checker 秒级可判性**(forge §underweights 回声室预警)。

### v1.4 response(forge 001 v2 verdict @2026-07-16 · `../../forge/v2/stage-forge-001-v2.md`)

(回应 hand-back `001-radar-pA-20260716T085807Z` 循环依赖 STOP · 双专家 strong-converge 无 unresolved · operator 已批准落地。注:v1.3 response 第 4 点的「先真跑验证」警告即本次 STOP 的触发器——XenoDev 执行该硬前置,证实 ①② 无底料可判,机制正常工作。)

1. **①② 退役出解锁前置 → 采纳 KG-B9**:循环依赖成立(checker 底料 ⊂ gate 所 gate 的范围;① 的谓词对象「判断/边」在解锁时点结构性不存在——Phase 2 形状的验收绑错到 P0.1 边界);①② 重绑 T021/T022 ship 验收(验收测名字面即此两项)+ O2/O7 使用期抽查。已落 O4 + Scope OUT。
2. **新解锁前置 = a1 单一谓词 → 采纳**:per-slice source 映射最小前移(SOTA「生成时织入 lineage」正解,SLSA/W3C PROV 背书;gate.py:219 注释自证管线缺件,非 forge 外加发明);走 P0.1 amendment 通道不被 gate 挡(T002-A1/T003-A1/A2 三次先例);T010/T011 同批解锁。已落 O4 初始层。
3. **真 rerun 自证生效条款 → 结构强制**:v1「建议真跑」升级为「生效条件写死」(吸取 v1 信推演被真跑推翻的教训);解锁语义显式 stage-0 + 自托管点条款,防新前置第三次被误读为 certification。已落 O4 + Open questions #3。
4. **XenoDev 落地路径(v2)**:refactor plan 四模块——A'(a1 amendment,S-M,实装前逐面 grep 枚举 TimeSlice 消费面)/ B'(unlock-preflight checker + KG-B4 wiring,S)/ C'(审计通道最小文件结构,S)/ D'(真 briefing rerun 自证协议,S);v1 模块 B(gate.py 降级校准工具)、D(journal schema)继续有效,A/C 被 A'/C' 替换。

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
