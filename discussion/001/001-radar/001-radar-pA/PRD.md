# PRD · 001-radar-pA · "方向评估官（历史位移内嵌）"

**Version**: 1.7  (human-approved revision)
**Created**: 2026-07-07T02:58:21Z
**Revised**: 2026-07-11 · v1.0→v1.1:P0.2 盲测门首判 FAIL(handback `001-radar-pA-20260711T135303Z`)决议 + moderator injection(`../L3/moderator-notes.md` @2026-07-10T08:19:13Z)——O4 两层化 + 要件③重 operationalize + 语义切窗/分层阅读原则
**Revised (v1.2)**: 2026-07-13 · operator 价值重定义(injection @2026-07-13T10:43:29Z):gate 硬门槛收敛为要件①②,要件③降级为使用期校准信号;Candidate B 诉求记 v0.2 展望
**Revised (v1.3)**: 2026-07-16 · forge 001 v1 verdict(`discussion/001/forge/v1/stage-forge-001-v1.md` · hand-back `001-radar-pA-20260715T093226Z` 决议链):P0.2 人肉盲测二值签字 gate 从 T010/T011 前置退役(采纳 KG-B8),改机器可判最小验收三项;识伪降为零解锁语义的可选校准;FAIL→STOP 双道保留
**Revised (v1.4)**: 2026-07-16 · forge 001 v2 verdict(`discussion/001/forge/v2/stage-forge-001-v2.md` · hand-back `001-radar-pA-20260716T085807Z` 决议链):v1.3「机器可判三项」中 ①② 因循环依赖(KG-B9,XenoDev 真跑证实)退役出 T010/T011 解锁前置,重绑 T021/T022 ship 验收 + O2/O7 使用期抽查;新解锁前置 = a1 per-slice source 映射单一谓词,生效条件写死「真 briefing rerun 自证 PASS」
**Revised (v1.5)**: 2026-07-17 · forge 001 v3 verdict(`discussion/001/forge/v3/stage-forge-001-v3.md` · hand-back `001-radar-pA-20260717T052416Z` 决议链):D′ 真 rerun 证实 a1 机制内存层生效但真跑走不到判定(a1 验证产物被锁在被否 gate 形态后面 = 隐依赖环 · 第四次「推演≠真跑」)——g1(人肉盲测二值签字)永久退役出解锁链;新 gate 形态 = 按 run 类型分流 + 两层 + 信号;评估 run 证据生成时落盘始终可见,T010/T011 解锁全机器自证;校准 run 只密封 answer-key、零解锁语义
**Revised (v1.6)**: 2026-07-18 · forge 001 v4 verdict(`discussion/001/forge/v4/stage-forge-001-v4.md` · hand-back `001-radar-pA-20260717T092547Z` 决议链):D″ 生效自证真跑正确 fail-closed STOP——v1.5 钦点标的「07-17 真产物」实为 pre-split 校准产物,评估/校准分流禁止评估自证消费它(第五次「推演≠真跑」= 生效条款标的错配)——采 γ · 正式 amendment(非 waiver):生效自证标的改「首个评估 run 产物」(同 stem · 同一验收事件),首个自证 PASS = 条款生效事件;07-17 降校准活动历史样本(exclusion 非豁免);β cut;key 轮换写入 runbook 序列不进机器谓词
**Effective (O4 生效条件 · 2026-07-18)**: forge v4 §c 条款生效事件达成(hand-back `001-radar-pA-20260718T231642Z` 决议 · HANDBACK-LOG 第 22 条):首个默认评估 run 产物 `diffusion-models-20260718T231343Z` 同一验收事件内 B′+D′ 自证 PASS → 条款状态 `landed-not-yet-effective` → **`landed-and-effective`** · T010/T011 机器解锁前置(unlock-preflight)PASS。条款文本零改动,版本号维持 v1.6
**Revised (v1.7)**: 2026-08-03 · forge 001 v5 verdict(`discussion/001/forge/v5/stage-forge-001-v5.md` · hand-back `001-radar-pA-20260802T162313Z` 决议链 · HANDBACK-LOG 第 40 条):**零骨架改动**——Scope OUT 不改、O4 生效条款不改(v1.6 已生效,本轮零触碰),只补三点:O1 补 O7 时间锚(longstop 起算算法 · 触发而无 journal 行判 FAIL 非「不可判」)/ 产物呈现面(消毒转义)列为 O1 完成率的实质风险(与差异化风险并列)/ 「≥3 条非豁免判断」定位澄清为集合验收采样口径而非单次产出 KPI
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
- **人肉签字参与任何解锁判定**(v1.5 注:g1 永久退役出解锁链——operator 07-15 拒签三条批评 · SLSA 硬门人不在判定回路 · forge v3 verdict)· **评估 run 的 post-gate 证据重生成**(v1.5 注:OSCAL「证据应是管线副产物非 ex-post 重建」;评估 run 改生成时落盘,校准 run 密封面不受影响)

## Success — observable outcomes

- **O1** 3 个月内完成 ≥5 次真实新方向评估,其中 ≥1 次实际改变了 operator 的投入决策
  - **时间锚(v1.7 新增,per forge 001 v5 verdict @2026-08-02 · 对应 XenoDev spec 侧 O7)**:「3 个月」此前无起算点,长期处于「测量窗未开始 ⇒ 永远不可判」的空转态。现定死起算算法——
    **start = min(首条真实评估 journal 行的 date, spec v0.7 生效日 + 30 日)**;本次代入 ⇒ **start = 2026-08-02,截止 = 2026-11-02**。
    **longstop 到期而 journal 无行 → O1 判 FAIL(0/5),不判「不可判」**——「没跑」是一个结果,不是一个待定态。
- **O2** 任一 briefing 的任一判断都能在 3 次点击内到达原文证据
  - **「≥3 条非豁免判断」的定位澄清(v1.7 新增,per forge 001 v5 verdict @2026-08-02)**:该数量是**集合验收的采样口径**(operator 抽样核验时手上要有足够条目),**不是单次产出的 KPI**。
    **显式 non-goal**:不得为凑满数量而让 judge 多产判断——那直接违 O4「不做真理机」与 Scope OUT-8;证据不够时的正确行为是如实判「样本不足」,不是把产出量做上去(Goodhart)。
    (本条只作定位澄清,不改 Scope OUT 列表,不改 O4 生效条款。)
- **O3** 30 分钟内出初判(评估延迟是产品属性,不是实现细节)
- **O4** 信任分两层校准(v1.5 修订,per forge 001 v3 verdict @2026-07-17;v1.4「真 briefing rerun 自证 PASS」的二值/人肉读法废止——D′ 真 rerun 证实 a1 机制内存层生效,但 a1 验证产物被锁在被否 gate 形态后面(隐依赖环:D′ 自证→B′ 谓词→audit.json→gate PASS→人肉盲测签字),真跑走不到判定 = 第四次「推演≠真跑」):
  - **初始层 · T010/T011 解锁前置 = 评估 run 全机器自证(人不在判定回路)**:
    ① a1 per-slice source 映射**生成时落盘、始终可见**(证据是管线副产物;废止评估用途的 post-gate ex-post 重生成 = SOTA 点名反模式);
    ② B′ 结构谓词(映射可解析 + briefing 覆盖 + 命名一致 · 硬阻断 · fail-closed)对真产物成立;
    ③ D′ 真 rerun 自证(独立核验一致)入 A1SelfCheckRecord journal,机器核验通过。
    preflight 消费对象从 RERUN-PASS 文本**一步换为 evidence bundle**(audit.json + briefing + D′ journal 记录),无双轨过渡;**人肉签字与二值 PASS 彻底移出解锁链**(g1 永久退役)。
    **生效条件(v1.6 修订 · amendment 非 waiver,per forge 001 v4 verdict @2026-07-18;v1.5「对 07-17 真产物立即可跑自证」废止——该标的是 pre-split 校准产物,分流禁止评估自证消费它,真跑正确 STOP = 第五次「推演≠真跑」)**:
    ① **每个评估 run 产物落地后,在同一验收事件内**以同 stem evidence bundle(audit.json + briefing + D′ journal 记录)跑 B′+D′ 自证;自证前该产物不得作解锁凭据(不得先投入产品使用、自证无限期挂起);
    ② **首个自证 PASS 的评估 run = 条款生效事件**,T010/T011 随之机器解锁;
    ③ 自证 **FAIL** → 机器道 STOP + hand-back 回流(documented deviation),修复后下一评估 run 重试(Argo abort→fix→new rollout 同构);
    ④ **未跑/未过** → 维持 blocked = `landed-not-yet-effective` 态(诚实且无 deadline,判据 B′+D′ 预定义;不跑评估 run 就不解锁,阻塞是自我施压的)。
    **条款内 runbook 兑现序列(预注册,防悬空)**:DEEPSEEK key 轮换 → operator 授权 → 首个默认评估 run(烧 key;自证序列本身不烧 key)→ 同一验收事件内跑同 stem 自证。**key 轮换是操作/授权前置,不进入 B′/D′ 机器 PASS 谓词**。合成 fixture 仅作回归,不得替代生效自证(v1.4 条款延续)。
    **✅ 生效记录(2026-07-18 · 本条款已生效 · hand-back `001-radar-pA-20260718T231642Z`)**:runbook 序列全兑现——key 轮换就位 → operator 三前置门逐一显式授权 → 首个默认评估 run `diffusion-models-20260718T231343Z`(真 OpenAlex + 真 DeepSeek · 封闭历史窗 2021-01-01→2023-12-31 · 非 --calibration · 与 07-17 校准样本干净隔离)→ **同一验收事件内**同 stem B′+D′ 自证 PASS(B′ 四件全真:structure/resolvable/coverage/naming;D′:`unlock_allowed=True` · `is_fixture=False` · 独立真检索双路径一致 · audit_digest 入 append-only journal)→ ② 生效事件达成 · T010/T011 机器解锁前置(unlock-preflight)exit 0(人不在判定回路 · g1 已退役)。**注意**:生效自证绑定该 evidence bundle stem;后续换方向/换窗的评估 run 各自按 ① 履行同事件自证义务(per-run 义务延续,非全局一次性豁免)。
    **07-17 产物处置(v1.6)**:diffusion-models-20260717T051551Z 降为**校准活动历史样本**——exclusion 非豁免:不销毁、不豁免、不作 PASS 证据;answer-key/run-binding 维持密封;决议 log / 脚本注记如实记录其 pre-split 身份(与 v1「retire-as-gate keep-as-calibration」一致化 · 污染治理 exclusion 背书)。
    **解锁语义(v1.4 延续)**:一次性 stage-0 治理动作,不承担 certification;自托管点条款不变(Phase 2 出口 ①② 生效后机器验收面升级)。
  - **run 类型分流(v1.5 新增 · 显式命名)**:评估 run(默认)= 透明留痕即解锁凭据,新增 human-readable 审计渲染面(operator 可读的留痕入口);校准 run(operator `--calibration` 自发起可选)= 保留盲测密封 + 负控 + answer-key,**只密封 answer-key 不密封证据通道**,产出零解锁语义只入 journal。密封是校准活动属性,不是管线默认属性(sealed-exam 先例)。
  - **原 ①② 迁移**(v1.4 延续不变):trace/provenance schema 完整性 + 证据 3 击可达性重绑 T021/T022 ship 验收 + O2/O7 使用期抽查对象。
  - **FAIL→STOP 双道**(延续 · 机器道 wiring 对象更新):机器道 = B′ 结构谓词任一 FAIL → 自动阻断下游(wiring 对象 = evidence bundle,全为真实文件级 artifact);治理道 = prd-revision-trigger hand-back 通道(流程级 STOP)。叙事级非阻断信号**折入 O2/O7 journal 带 escalation,不设独立 smoke 层**(「a warning nobody reads is not a gate」)。
  - **识伪盲测 = 校准 run 专属**(v1.3 retire-as-gate keep-as-calibration 延续,v1.5 落地为分流):校准产出零解锁语义;要件③ schema 保留于校准活动内;RERUN-PASS 生成机制随校准活动保留或废止按 build 实况定,**不再被 preflight 消费**(hand-back 16「spine 底座」定位被 forge v3 显式覆盖)。
  - **长期层 · 信任主锚**(v1.2 延续并强化):O2(任一判断 3 击回溯原文,**升级为验收机制**)+ O5(journal 后验复核 + taste 标记)+ operator 使用期抽查(非盲判,经 human-readable 审计面)承担;非 gate 一次发证。
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

**第二条并列风险 · 产物呈现面(v1.7 新增,per forge 001 v5 verdict @2026-08-02)**:**消毒转义把叙事
读坏,是 O1 完成率的实质风险**,与上述差异化风险并列而非从属。理由:O1 要 operator 每周真读一份、
连做 5 次;PRD O1 又是"信任第一块砖"——读起来费劲的产物,operator 不会连读 5 次,O1 直接空转。
实样(forge v5 §5.6)显示叙事被转义成 `\*\*结构连接\*\*` 形态。
⚠ **修法不是"反转义"**,而是**从规范存档生成一份上下文安全的展示投影**:恶意样本在目标上下文必须
保持 inert,且可回指规范证据。**证不出安全 → 展示版不 ship**,保留规范版并改善非执行式阅读辅助;
"不作证据用途"的标签**不能**替代注入防御。

## Open questions for L4 / Operator

1. **延迟预算是否分快慢两档**(30 分钟初判 vs 学生开题当场讨论要更快档)——建议 v0.1 单档,自用数据说话。非骨架决定,不阻塞。
2. **briefing 结论词表最终形态**(借 Tech Radar 四环起步,分几级/用什么词需拿真产出给 3-5 同行看反应)——v0.1 中后期非正式验证,不阻塞。
3. ⚠ **共享地基假设(v1.6 更新:生效条款标的重裁)**:v1.5「自证对 07-17 真产物立即可跑」的**标的表述废止**(D″ 生效自证真跑正确 fail-closed STOP——07-17 产物是 pre-split 校准产物,v3 自己的评估/校准分流禁止评估自证消费它 = 第五次「推演≠真跑」= 生效条款标的错配;v1.5 落地前置警告「D″ 立即自证是最后防线」再次预言命中,但命中的是四条监测项之外的第五种)。新表述:生效自证标的 = **首个评估 run 产物**(同 stem evidence bundle · 同一验收事件内 B′+D′ 自证);首个自证 PASS = 条款生效;07-17 降校准活动历史样本。**v4 amendment lineage**:γ 经 forge v4 prospective amendment 批准(documented deviation → hand-back 19 → forge v4 → 本修订),任何再偏离须再走 deviation→amendment 循环。⚠ 新落地前置警告(forge v4 §underweights):自证脚本参数化「S 级」+「同一验收事件靠 runbook 纪律未机器强制」仍是**推演**(与 v1/v2/v3 的 S 级估计同型)——**首个评估 run 的真跑自证是本 amendment 的最后防线**;再次 STOP / 参数化远超 S / 事件锚僵尸化 / 验收事件纪律被打破 / key 轮换持续 pending 阻塞生效,任一即触发 forge v5。**✅ 兑现注记(2026-07-18 · hand-back `001-radar-pA-20260718T231642Z`)**:最后防线兑现——首个评估 run 真跑自证 PASS,第六次「推演≠真跑」**落生效侧**(非被推翻),上游 forge/推演 verdict 四连被真跑推翻的链在本条款收口;v5 触发条件①(再 STOP)与④(先用后证/隔日补证)均未触发。残留监测继续在案:「同一验收事件」仍 runbook 纪律未机器强制(本次靠 operator 纪律 + task 铁律双守成立);KG-B10 provider-proof spine 维持冻结在册(本次真跑走的正是纪律默认路径,未触及该面);v5 触发条件五条继续监测。

(v1.5 历史表述存档:T010/T011 解锁 = B′ 结构谓词 + D′ 自证 + A1SelfCheckRecord journal 机器核验;自证对 07-17 产物立即可跑;v4 触发条件四条 = 改接超 S / 泄露面未收窄 / 抽查范式失效 / KG-B10 方向不受控。v1.4 历史表述存档:新解锁前置 = a1 单一谓词同批解锁,生效条件「真 briefing rerun 自证 PASS」;机器道 wiring 对象 = a1 映射 + 审计通道结构 + 治理 STOP 记录。)

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

### v1.5 response(forge 001 v3 verdict @2026-07-17 · `../../forge/v3/stage-forge-001-v3.md`)

(回应 hand-back `001-radar-pA-20260717T052416Z` D′ 真 rerun 结构盲区 · 双专家 strong-converge 无 unresolved · operator 已批准落地(Decision menu [A])。注:v1.4 response 第 3 点的生效条款即本次触发器——XenoDev 执行 D′ 真 rerun,证实真跑走不到判定,机制第四次正常工作。)

1. **g1 永久退役出解锁链 → 采纳**:隐依赖环成立(a1 自证→B′→audit.json→gate PASS→被否盲测签字;三条 a1 可见路径全由「保识伪难度」锁死);RERUN-PASS 一步退出 preflight 消费链,无双轨过渡(hand-back 16「spine 底座」定位被显式覆盖)。已落 O4 初始层 + Scope OUT。
2. **按 run 类型分流 + 两层 + 信号 → 采纳**:评估 run 证据生成时落盘始终可见(SLSA attestation / OSCAL「管线副产物」/ PyPI attestations 三重背书);校准 run 只密封 answer-key 不密封证据通道(sealed-exam / HF public-private leaderboard / SLSA VSA 先例);g3 折入 O2/O7 journal 信号 + escalation 不设独立层(advisory-gate 划线判据)。已落 O4。
3. **生效条款 PASS 语义改写 → 机器谓词**:PASS = B′+D′ 对真产物成立 + journal 机器核验,人不在判定回路;自证步骤对 07-17 真跑产物立即可跑(第四次「推演≠真跑」后铁律)。已落 O4 + Open questions #3。
4. **XenoDev 落地路径(v3)**:refactor plan 四模块——A″(CLI 评估 run 生成时落 audit.json + human-readable 审计渲染面,S)/ B″(preflight 消费对象换 evidence bundle · 去 gate-PASS 检查(评估 run),S)/ C″(`--calibration` 分流 flag + 密封面维持,S)/ D″(对 07-17 真产物跑通自证序列 + A1SelfCheckRecord 字段级小改,S);**显式冻结** audit_channel 防伪 spine 面(KG-B10 收窄至校准面,细节留后续);B′/D′ 谓词逻辑原样复用。

### v1.6 response(forge 001 v4 verdict @2026-07-18 · `../../forge/v4/stage-forge-001-v4.md`)

(回应 hand-back `001-radar-pA-20260717T092547Z` D″ 生效自证 STOP · 双专家 strong-converge 无 unresolved · operator 已批准落地(Decision menu [A])。注:v1.5 response 第 3 点「自证对 07-17 产物立即可跑」即本次触发器——XenoDev 执行 D″ 真跑,三道守卫正确拦下校准产物流入评估解锁面,机制第五次正常工作;命中的是 v3 四条监测项之外的第五种「生效条款标的错配」。)

1. **采 γ · 生效标的改写 → 采纳(amendment 非 waiver)**:生效自证标的从「07-17 真产物」改「首个评估 run 产物」(同 stem · 同一验收事件内 B′+D′ 自证);首个自证 PASS = 条款生效事件;FAIL → STOP+回流+下次重试;未跑/未过 = landed-not-yet-effective(诚实无 deadline 有判据,canary blocked-until-verified 正统背书)。已落 O4 生效条件段 + Open questions #3。
2. **07-17 降校准活动历史样本 → 采纳**:exclusion 非豁免(污染治理零 grandfather 豁免先例 + 临床 protocol「waivers not permitted」跨域合围);不销毁、不豁免、不作 PASS 证据;answer-key 维持密封。已落 O4。
3. **β cut · α 非独立选项 → 采纳**:β 是跨域明文反模式(放行须穿三道守卫 = 拆护栏);α 收编为 γ 的立即执行 note(operator 授权 + key 轮换完成后可即刻跑)。已落 O4 runbook 序列。
4. **XenoDev 落地路径(v4)**:a. **即刻收编** forge v3 worktree 实装 commit(状态命名「机制 landed」,与「条款生效」显式两态);b. `selfcheck-07-17.sh` S 级参数化(direction/ts/briefing · 只复用现有 D″ 入口/守卫 · 禁新判据/旁路/spine;超 S 回落手工模板);c. key 轮换 → 授权 → 首个默认评估 run → 同事件自证。护栏三道守卫 + 14 测 + KG-B10 冻结全 keep 零削弱。

### v1.7 response(forge 001 v5 verdict @2026-08-02 · `../../forge/v5/stage-forge-001-v5.md`)

(回应 hand-back `001-radar-pA-20260802T162313Z`「v0.6→v0.7 amendment 落地」· HANDBACK-LOG 第 40 条决议 · operator 已批准落地。**与 v1.3~v1.6 四次不同:本次不是被真跑推翻后的修补**——v5 是"判据冻结前置"的主动审查,采 ISO/IEC/IEEE 29148 九特征作分类框架,12 项施工单中 9 项已落 XenoDev `spec.md` v0.7,PRD 侧只需承接三点。)

1. **O1 补 O7 时间锚 → 采纳**:起算算法 `start = min(首条真实评估 journal 行 date, spec v0.7 生效日 + 30 日)` ⇒ 本次 2026-08-02 → 2026-11-02;longstop 到而无 journal 行**判 FAIL 不判「不可判」**。已落 Success O1 时间锚条。**这是把"永远测不完所以永远不算失败"这条退路堵死**。
2. **呈现面列为 O1 实质风险 → 采纳**:与差异化风险**并列**(非从属)——O1 要求连读 5 次,读不动即 O1 空转。修法是**上下文安全的展示投影**而非反转义,证不出安全则展示版不 ship。已落 Biggest product risk 第二条。对应 forge v5 item 12(独立 task,XenoDev 侧本轮未起)。
3. **判断数量定位澄清 → 采纳**:「≥3 条非豁免判断」是集合验收采样口径,非单次产出 KPI;显式 non-goal = 不得为凑数让 judge 多产判断(违 O4/OUT-8 · Goodhart)。已落 Success O2 注。**Scope OUT 列表零改动**(forge v5 明文「PRD 零骨架改动」)。

**本次未处置 · 已显式路由(HANDBACK-LOG 第 40 条)**:

- **累积池分区键**(池仅按 decision epoch + rubric 分区、不按评估方向分区 ⇒ 理论上可借跨不相干方向的历史判断凑满 ≥3 判 PASS,且拆池不追溯)——codex adversarial-review round 3/4/5 三轮持续判 high。核实为 **forge v5 决策表第 2 行原文逐字决定**,非 spec-writer 起草缺陷;改分区键属"重大架构转向"⇒ 按本仓 CLAUDE.md 决策矩阵**路由 forge v6 裁**,不在单包决议级处置。注:此项是 **v6 的新增触发器**,与 v5 声明的既有 v6 判据(warn 候选过 review_by 后无证据仍被续期)并列。
- **R5-F2/F4 第 6 轮 codex 复核**——两条修法已落成 spec 规范文本,但其保证被明文挂起(**不得援引为 O2/P2 PASS 依据**)。经判定该挂起是 **fail-closed**(不复核 ⇒ 不得判 PASS)而非 fail-open,且 spec-task 同步缺口使新池化路径的 PASS 本就不可达 ⇒ **不单独跑,挂为 v0.7→v0.8 amendment 的强制随行项**(防遗忘条款见 HANDBACK-LOG 第 40 条)。

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
