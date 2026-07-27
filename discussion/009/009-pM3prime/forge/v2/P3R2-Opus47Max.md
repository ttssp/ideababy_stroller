# P3R2 · Reviewer A(Claude Opus 4.8)· 009-pM3prime forge v2 · finalize

**Phase**: 3R2(finalize · convergence_mode = **strong-converge**)
**Written**: 2026-07-27

---

## §1 我对每条分歧的最终立场 + 让步

### 分歧 1 ·「数字 vs 形态」—— 收敛,采纳对方加固

我提分界,B 侧接受并加了一条我没想到的防线:「**形态改也不能 retroactively 解锁旧 gate**」,
并把机制落到 009 已有的 `caliber_version` 上。**我完全采纳 B 侧的措辞作为最终判据**:

> **看数后下调既有阈值数字 = 移动球门(禁);
> 用新 `caliber_version` 预注册完整曲线/区间并废止旧 pass 语义 = 方法学修正(可)。**

这条比我的原版强在两点:(a) 落到 009 既有的口径版本化机制上,**可执行不是口号**;
(b)「废止旧 pass 语义」堵死了「换形态顺便把旧数据重判为过」的后门。

### 分歧 2 · E2 处置 —— **让步**,采纳 B 侧的 (iii) 拆分

我 R1 给的是二选一(不解锁 / 弱条件下解锁),B 侧给的 **(iii) E2 拆分**更准。**我让步。**
理由:我的二分把「E2」当成一个原子对象,而它其实包含两件性质不同的事 ——
「产开发证据」与「跑历史窗回测」。前者可由 groundedness 支撑,后者不可。
拆开之后不需要在「解锁/不解锁」之间做假选择。

### 分歧 3 · Dorner & Hardt —— **让步**,接受判 v0.2+,并补一条前置条件

我 R1 主张它可进 v0.1 作第三候选,B 侧判 v0.2+,给了三条理由(改 estimand / 需更多样本 /
需二分类化 + 噪声与真值正相关假设)。**我让步,并补充一条 B 侧只点到未展开的关键**:

该路径成立**依赖「标注者噪声与真值正相关」(即标注者优于随机)**。
而本案的前提恰恰是 **operator 在 sector/direction/horizon 三维无领域判断力** ——
**这个假设在这三维上未经检验,且有可能为假**。
所以它不只是「v0.2+ 排期问题」,而是**带前置验证义务的候选**:
进 v0.2 前必须先证明 operator 在目标维度上优于随机,否则整条路径的地基不成立。
这一条请写进 v0.2 note。

### 新增分歧 · groundedness 是降级还是自我安慰 —— 收敛为**条件性采纳**

B 侧:「有意义的降级,但**若被写成授权原 E2/backtest 就会变成自欺,我会转向纯 STOP**」。
**我同意,并接受这个条件是 binding 的**:groundedness 的采纳**以边界被写硬为前提**。
边界写不硬 → 回退纯 STOP。这不是修辞,是 verdict 的生效条件。

## §2 联合 verdict(单一 · 无 unresolved)

**全量五维 Layer-2 作为「映射正确性 gold gate」在 v0.1 判定不成立,且不因换主体或调门槛而成立**
—— sector / direction / horizon 三维不存在可及的 validity 锚,而唯一在场的主体(operator)
产出的「gold 考据版 vs human 盲标版」按 Krippendorff 信度分类**只测 stability,不测 validity**。
forge v1「operator 可自任独立第二源」的推论**据此撤销**:错误独立性解决「不共享盲点」,
**不产生真值**;KG-42 的死结不是被 v1 解开的,是被挪位的。

**但不判纯 STOP。** 应把 Layer-2 的验收对象从 **correctness** 重定为 **groundedness**
(被引原文是否真支撑该五元组)—— 它只需阅读理解不需领域判断,009 的引文回锚基础设施
(`raw_ref` / `span_start` / `span_end`)已就位,且能真抓到东西(实测高达 57% 引文为事后合理化)。

**该采纳是条件性的,条件必须同时落地**:**E2 拆分** —— 原 E2 历史窗回测**不解锁**;
新增 groundedness-only 诊断 lane 只证明「提取器没有无中生有」。
verdict 必须明写:**groundedness 过 ≠ 映射正确 ≠ 有 alpha ≠ 授权回测**。
边界写不硬则回退纯 STOP。**门槛形态同步修正**:固定 coverage 阈 → risk-coverage 曲线 + AURC,
经新 `caliber_version` 预注册并废止旧 pass 语义(**改数字 = 移动球门,改形态 = 方法学修正**)。
**红线不动**:`gold_layer2.py:203` 第二 LLM/跨 vendor 未校准终审仍 raise。

## §3 残余分歧 → v0.2 note

1. **Dorner & Hardt 变体比较路径**(v0.2+ · **带前置验证义务**):
   需先证明 operator 在目标维度上**噪声与真值正相关(优于随机)**,否则地基不成立。
   009 的 `trial_ledger` extractor_variant 基础设施使其值得保留。
2. **Partial identification / Fréchet 界在 n≈41 的实际宽度未知**:
   双方都认为方向存在但**未验证小样本下界宽到什么程度**。若界宽到无区分力,则该路径对 v0.1 无用。
   **可零成本先算**(与 KG-43 的可达性探针同性质)。
3. **Layer-1 的主体问题全程未被处置**:`spec.md` 显示 Layer-1 门槛仍空、同样 blocked-on 真盲标。
   本轮聚焦 Layer-2,Layer-1 是否被 groundedness 吸收、还是另有主体问题,**未解**。
4. **「operator 慢考据 gold 是否可产」未被文献救活**(我 P1 §3.1 的原始疑问):
   信度文献最多支持 stability/reproducibility,不自动给 validity。该问题在方法学上**无解**,
   只能靠外锚(watchlist / `published_at`)绕过,而外锚只覆盖两维。

## §4 W 形态产出草稿建议

**verdict-only**:§2 全文可直接用,建议加一句前置摘要 ——
「v1 的解被撤销;Layer-2 从 correctness 降级为 groundedness;E2 拆分,回测不解锁。」

**decision-list**(4 列矩阵)建议至少覆盖:
- **保留**:`:203` 红线 · gate fail-closed 骨架 · 双层链 · E1 US 密度结论 · 引文回锚基础设施
- **调整**:Layer-2 验收对象 correctness→groundedness · 门槛形态 固定 coverage→risk-coverage 曲线 ·
  E2 由单 gate 拆为两 lane · SLA Layer-2 门槛表整体经新 `caliber_version` 重注册
- **删除**:v1「operator 可自任 Layer-2 第二源」推论 · 「KG-42 死结解」判定(第 27 条)·
  全量五维 correctness gate 作为 v0.1 交付项 · 07-25 gold 协议**作为验收依据**的地位
  (作为 stability 记录可留,但不得当 validity 用)
- **新增**:groundedness 验收面 + 其硬边界声明 · KG-43 三道门 · v0.2 note 四条

**next-PRD** 需改的落点(只列位置与方向,细节留 synthesizer):
- **PRD §4-E1 D-7 改写块**:撤销「operator 可自任第二源」;改写为 groundedness 验收 + 明示不验 correctness
- **PRD E2 解锁条件 ②**:由「两层金标过」拆为两条 —— 诊断 lane 条件(groundedness)/ 回测 lane 条件(**在 v0.1 不可满足,明写**)
- **PRD §2 × D-7 关系**:v1 判「非产品级真互斥」应**部分撤销** —— 在 correctness 维度上它**就是**真互斥

**KG-43 建议写成三道冻结前置门**(合并双方):
① **存在性证明**(构造理想输入证明 `passed=1` 可达)
② **真值证明**(验收锚从哪来 / 谁能独立证伪 / 成本是否在本 tier 可承受)
③ **形态检验**(门槛形态是否符合该问题的标准处理方式 —— 形态错比数字错更难救,
数字受 C6 约束可经版本化修正,形态错则整套预注册作废)

---

**字数**:约 1,180 字
**Hard constraints 自检**:✅ strong-converge 已 finalize 单一 verdict · ✅ 无 unresolved ·
✅ 3 条分歧全收敛(2 条我让步)· ✅ 残余降 4 条 v0.2 note · ✅ §4 逐项对应 forge-config.W
