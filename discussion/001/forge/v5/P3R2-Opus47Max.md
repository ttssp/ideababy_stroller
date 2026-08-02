# Forge v5 · 001 · P3R2 · Opus47Max · 联合收敛 R2(finalize)

**Timestamp**: 2026-08-02T14:30:00Z
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: strong-converge

## 1. 我对每条分歧的最终立场 + 让步

**分歧 1 · ratchet 的证据等级**
- 对方论证:"ratchet 是成熟行业实践而非正式标准";称「共同构成明文先例」过强。
- **让步。** 对方对:W3C/NASA/IEEE 29148 是**标准条文**,ratchet 是**行业实践**,两者证据等级不同,我 P3R1 把它们并列成「共同构成明文先例」确实过强。
- **最终立场**:T040 窄起跑的正当性写成**两层**——「scoped verification(W3C/NASA/29148 明文)**为主**;ratchet/baseline(行业实践,非标准条文)**为实施形态**」。结论不变,证据分级如实标。

**分歧 2 · 第三值何时落** — 双方同意。语义名现在冻结,CLI/字段协议留 T041,**不追溯**把当前 briefing 判 PASS。无残余。

**分歧 3 · keep 还是 refactor** — 双方同意拆分:**O7 机制 keep;消毒转义 + 可读性 + 判断密度 refactor**。不再用含混的 narrow PASS/hold。无残余。

**分歧 4 · 双方的「解释掉」** — 双方同意,且**双向登记**:我方 post-hoc 定累积规则;对方未检索强制多样本有效性、结论在该面不设防。**双方规则均只对下一次评估生效。** 无残余。

**分歧 5 · 九特征能否直接成为 gate(对方新提 · 打我 P3R1 §4)**
- 对方论证:"采用 ISO 九特征不会自动解除自指";九特征是诊断分类,不是本仓可执行牙。
- **让步 —— 对方对,我 P3R1 §4 那个 ✅ 给早了。** 补完这条推理:要判「(c) 是否 Feasible」,得先知道 judge 能不能产 3 条,**而那正是只有真跑才知道的经验问题**;九特征**命名**了要证什么,没有**替你证**。
- **最终立场**:自指链的正确终点不是「标准自动解除」,而是**「终止于有资质者的评审 + 真跑证据」** —— 这与 oracle 文献「人是最后的 oracle 来源,合法」同构,是**合法终点而非自动解除**。⇒ 九特征本地化表必须带 **对象 / 证据 / 责任人 / fallback** 四列(采对方措辞),且 **Feasible 一栏不接受推演,须真跑或历史数据**。

## 2. 联合 verdict(单一)

**采「ISO/IEC/IEEE 29148 九特征作为判据冻结前置的分类框架 + 逐项本地化为可执行牙」为 v5 主裁,12 项按其归位,每项带 A + 判据 + 证不出则 B。**

本仓在册的「判据可达性族」(数学不可达 / 结构不可达 / 不可复现 / 唯一可读 / 缺起算点)是 29148 九特征的**重新发明**:Feasible / Verifiable / Unambiguous / Complete(集合级 no TBD-TBS-TBR)各有其位。采用它的收益不是「换个名字」,而是**把五个看似偶发的事故收敛成同一族的同一种违反**,并自带**个体级 vs 集合级**二分——这一刀直接诊断出 **§1-O2 (c) 是集合级属性却被写成单 run 自足的个体级门**,也就是本轮最核心的那处挂错侧。

**但九特征只是分类,不是牙**(采纳对方分歧 5)。自指链终止于**有资质者评审 + 真跑证据**,不是标准本身;故本地化表强制四列,且 Feasible 栏**不接受推演**——这正是本仓七次「推演≠真跑」的制度化收口。

**三条一次裁死**:① **(c) 改挂集合验收侧**(跨 run 累积池 + 单 run 不足记 `INSUFFICIENT_EVIDENCE` 不阻断),**产出侧不加 judge 下界**(违 §1-O4 且 Goodhart:measure 变 target);② **R4-F4 = compensating control**,四要件(合法技术约束 / 等效替代 / **批准人 ≠ 申请人** / **带 expiry**)——ISO 27001 5.3 与 NIST RMF 双路独立同构,`writer.py` 拒绝自批**被追认为无意中执行了职责分离**;③ **T040 立即以 warn + baseline 窄起跑**,不等全部收敛。**O7 补 longstop**(否则洞只是从「没有起点」挪到「起点可能永不到来」)。词汇撞车按 **DDD 限定词 + RFC 6365 点名否决**处理,**不动 C″ 分流契约**。

**无 unresolved。**

## 3. 残余分歧降级为 v0.2 note

- **v0.2 note 1 · 累积池的可比性**:跨 run 累积抽样假设不同方向的判断可比。**何时回头看**:累积池首次达 3 条且抽样时,若发现三条来自三个不相干方向导致 operator 无法有意义地抽查 → 回落 item 2 的 fallback B。
- **v0.2 note 2 · expiry 机制的实现代价**:compensating control 的 expiry 若实装超 S 级,先落静态表 + 人工 review 周期。**何时回头看**:第二条 compensating control 条目出现时(一条可人工盯,两条起就该机器盯)。
- **v0.2 note 3 · forge-protocol 字数约束的唯一可读性缺陷**(元层 · **归 006 不归本轮**):「800-1500 字」中文歧义致双方各按一种读法执行(对方 `sed` 机械压缩 / 我超标 43%)。**这是本轮要裁的 Unambiguous 缺陷发生在裁它的这场 forge 里**,自指实例。建议 006 改「≤N CJK 字符 / ≤M words」明写,并加「宁可超标具名声明,禁有损压缩」。
- **v0.2 note 4 · 强制多样本输出的有效性面未检索**(对方 §4 自陈):双方结论在此面**不设防**。**何时回头看**:若累积池方案实施后 O2 仍长期不可达,该面需补检索再议。

## 4. W 形态产出的初步草稿建议

**W 含 verdict-only → 关键句**:
> 「判据冻结前必须先证什么」有现成国际标准答案(ISO 29148 九特征),本仓不必自造术语;但**标准只命名要证什么,不替你证** —— 自指链终止于有资质者评审 + **真跑证据**,Feasible 栏不接受推演。

**W 含 decision-list → 12 项施工单(每项 A + 判据 + 证不出则 B)**:

| # | 项 | A(裁决) | 判据 | 证不出则 B(fallback) | 落点 |
|---|---|---|---|---|---|
| 1 | 通用前置 | spec 新增 §0.1「判据冻结前置」:拟冻结为 gate 的判据须填九特征本地化表(**对象/证据/责任人/fallback** 四列) | 表填满 ∧ **Feasible 栏有真跑或历史数据**(不收推演) | Feasible 冻结前证不出(须先跑才知)→ 该判据以 **warn 模式**上线 + 记 baseline,满 N 次真跑后再议升 block | spec §0.1(新) |
| 2 | §1-O2 (c) | 改挂**集合验收侧**:O2 抽样池 = **跨 run 累积**非豁免判断;单 run <3 **不阻断**,记 `INSUFFICIENT_EVIDENCE` 且判断入池;池 ≥3 且抽样全 ≤3 击 → O2 PASS | 累积规则**预先**写死(池定义/去重/时效窗)∧ 明标 **post-hoc 制定 · 不追溯** | 跨 run 合并被证不可比 → 回落「单 run ≥3」**但**放宽为「judge 已产出全部可锚判断而数量 <3 时记 INSUFFICIENT_EVIDENCE,不判 FAIL」 | spec §1-O2 (c) · §6 O2 行 · §7-P2 |
| 3 | 唯一可读性 | 更名锚定为 29148 **Unambiguous**;spec 加术语章,九特征作规范性引用 | 每条验收行「产物」列与「验证命令」列**不得**推出两种互斥实装 | 某行天然需两种实装 → 不是 Unambiguous 违反,是**两个 bounded context**,转 item 11 处理 | spec 术语章 · §6 表头注 |
| 4 | O7 起算点 | 「起算日 = 首条真实评估 journal 行 `date`,**或 spec v0.7 生效后满 30 日,以先到者为准**」⇒ 本次 2026-08-02 / 截止 2026-11-02 | 机器可读(journal 首行 date vs 生效日+30) | longstop 触发而仍无 journal 行 → O7 判 **FAIL(0/5)而非不可判** —— 时钟已起 | spec §1-O7 · §6 O7 行 |
| 5 | 用途分类 | 每条判据标 `usage: one-shot-gate \| recurring \| cumulative`(preflight=one-shot · O2=cumulative · C9=recurring) | 三类穷尽互斥 ∧ 每条恰好一个标签 | 某判据跨两类(如 O2 既 ship gate 又长期锚)→ **拆成两条**分别标,不允许一条兼任 | spec §1 各 O 行 |
| 6 | judge 下界 | **产出侧不加下界**。现状「非稀疏叙事零判断 fail-loud」= 下界 1,保留;产物侧只如实计数并声明 | judge 产出数由证据决定;`renderer.py:244-253` 计数警示已在位 | 累积池 **≥5 run** 仍达不到 3 条 → 判为**上游 provenance/检索**问题,起独立 task 查 `anchor_map` 密度;**仍不**在 judge 加下界 | judge.py **零改动** + spec 注明理由 |
| 7 | OQ-A1-1 | **spec 语义层现在落**:非-PASS 细分 `INSUFFICIENT_EVIDENCE`(样本不足)vs `FAIL`(断链/违约);**CLI 退出码 + 产物状态字段协议留 T041** | OQ-A1-1 从 Open Questions **移除**(满足 Complete: no TBD/TBS/TBR) | 落语义层被证连带改 CLI 契约进而触 KG-B10 → 只落**文档语义**,产物侧沿用现有计数警示文本 | spec §1-O2 (c) · 删 OQ-A1-1 |
| 8 | T040 | **立即起跑**,形态 = **warn + baseline + 只卡新增**;6 个测文件中 5 个正常建 block 测,`test_o2_exemption_contract.py` 的 (c) 条按 item 2 新语义建 + mutation 证 teeth | `pytest tests/contract/ -q` 全绿 + red-green-log 每条 mutation 证据 | item 2 累积语义建测时被证不可测(如池无持久化落点)→ 该条降 **warn-only 断言 + 记 baseline**,**不阻断**其余 5 文件 ship | T040.md · tests/contract/ |
| 9 | 靠另一道门兜底 | 采纳为 spec 级规则:任何「本门可放行因另一门会挡」的论证**须附另一门确实挡得住的可执行证据**(测/mutation),否则视为**无兜底** | 历史实例为准:C9 绕过 #1 判「可接受」的理由是②+⑤双红,而 #5 打掉了 ⑤ ⇒ 该判断已在无人知晓下失效 | 某处兜底论证给不出可执行证据 → 按**无兜底**处理,**收紧本门** | spec §6 meta-note · T032/T040 |
| 10 | R4-F4 | 给门① 建**与门②不同构**的 `COMPENSATING_CONTROLS` 表:① 合法技术约束陈述 ② 等效替代缓解 ③ **批准人 = operator(≠ 写码 agent)** ④ **expiry**。R4-F4 为首条,替代缓解 = 写后 verify + 失败删半成品 | 缺任一字段 → 门① 仍红;**expiry 过期 → 门① 转红** | expiry 实装超 S → 先落 ①②③(静态表 + operator 批注),expiry 用 review 周期人工兜(→ v0.2 note 2) | `ephemeral.py` 新表 · `writer.py` 补 dir fsync |
| 11 | 词汇撞车 | 裁 **(i)**;落地改 **DDD 限定词 + RFC 6365 手法**:限定为「**解锁评估 run**(reconstruct)」/「**产品评估 run**(evaluate)」,术语章**点名否决**跨语境用法,并**命名 evaluate 自己那条 provenance 链**(RunProvenance + journal `lines[2]`) | spec 全文「评估 run」**裸用为 0** | 限定词波及面 >S(grep 命中过多)→ 先只在术语章 + §7-P2 + selfcheck 三处限定,其余加一次性脚注 | spec 术语章 + 全文 grep · **不动 C″ 分流契约** |
| 12 | §5.6 可读性 | 起**独立 task**(本轮不修):渲染时反转义 / 分离展示层。定位 = **产品面风险**(O7 要 operator 每周真读 5 次 × PRD O1「信任第一块砖」),非渲染整洁 | operator 读一份产物**不需在脑内反转义** | 反转义被证削弱注入防御 → 改**双产物**:消毒版存档 + 展示版渲染,展示版明标「**不作证据用途**」 | 新 task · PRD 风险段 |

**四列矩阵归类**:
- **保留**:judge 现状(item 6)· C″ 分流契约(item 11)· 门② `DECLARED_READ_SITES`(item 10)· O7 机制与节奏(item 3 拆分后)
- **调整**:(c) 挂点(2)· O7 措辞加 longstop(4)· T040 形态(8)· 自证域措辞(11)· 唯一可读性更名(3)
- **删除**:OQ-A1-1 作为 Open Question(7)· 「在 judge 加下界」这一候选方案(6)· 「给门①开豁免」三条坏路(10)
- **新增**:spec §0.1 判据冻结前置 + 九特征本地化表(1)· `usage:` 用途标签(5)· 兜底论证举证规则(9)· `COMPENSATING_CONTROLS` 表(10)· 术语章(3/11)· 可读性 task(12)

**W 含 next-PRD → 关键产品决策点**:
1. **PRD 零骨架改动**;仅在 Biggest product risk 段补一条:**产物呈现面(消毒转义)是 O7 完成率的实质风险**,与差异化风险并列。
2. O7 起算/截止日入 PRD Success O1 注记(2026-08-02 / 2026-11-02 + longstop 规则)。
3. **不改** Scope OUT、不改 O4 生效条款(v1.6 已生效,本轮零触碰)。

**给 synthesizer 的一条提醒**:本轮 verdict 的**可证伪点**是 item 1 的 Feasible 栏——若 spec §0.1 落地后第一次实际使用时发现「Feasible 在冻结前几乎总是证不出」,那说明九特征本地化表**退化成了 warn 模式的橡皮图章**,应触发 v6。
