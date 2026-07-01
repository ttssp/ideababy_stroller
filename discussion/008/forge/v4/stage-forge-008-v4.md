# Forge Stage · 008 · v4 · "用途锚定 + 可靠性前置的 gated refactor"

**Generated**: 2026-06-30T11:00:00Z
**Source**: forge run v4 with X = 4 标的(IDS 本仓 2 + XenoDev 外部 2), Y = 产品价值/用途成立性 + 提取可靠性/可行性 + 数据建模/字典设计 + 工程纪律, Z = 对标 SOTA(架构/提取层 · 零法律/ToS/DMCA 检索), W = next-PRD draft + decision-list + next-dev-plan
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both), P2 (both), P3R1 (both), P3R2 (both) — 共 8 份 round file
**Searches run**: 11 across 提取/反讽/copy-trading/structured-output 多源(Opus P2 四次;GPT P2 七批 21 query)— **零法律/ToS/DMCA 检索**(Z binding 禁止)
**Moderator injections honored**: none(本 v 无 moderator-notes.md)
**Convergence outcome**: converged(双方 P3R2 §2 各为单一 GO · gated refactor 且逐项同向;双方均显式标 "无 unresolved";R2 后三条分歧全部按对方更优措辞收敛)

---

## How to read this

forge 是横切层(不是 L1-L4 pipeline 的一部分)。本文档是双专家(Opus 4.8 Max + GPT-5.5x High)
独立审阅 + 提取/反讽/copy-trading SOTA 对标 + 两轮联合收敛后的产出,**强制给出立场**(不是候选菜单 defer 给你拍板)。

读完后你应该:
- 知道双专家对「结构化数据下游用途该不该现在定 / 机器可信跟单可不可行 / 字典三层怎么取舍」的最终 verdict(单一 GO · gated refactor)
- 能用 §"Evidence map" 把每条结论逐条溯源到具体 round file 段落
- 拿到三件套产物:§"Decision matrix"(字典+PRD 的 保留/调整/删除/新增 全景)、§"Next-version PRD draft"(可回流改 008-pB PRD v1.3→v1.4 的 008↔004 契约 + 信号 spike 工作项)、§"Next-version dev plan"(M1-M4 落地路线,含信号 spike 规格)
- 能基于 §"Decision menu" 直接进入下一步(fork PRD branch 进 L4 / 跑 v5 / 局部接受 / park / abandon)

> ⚠ **本 forge 审的是产品用途 + 提取可靠性,不审【自动翻页/采集对此顾问平台的合规性】**(operator 已拍板并担责,binding,沿用 v1/v2/v3)。全程未论证合规。**GO ≠ 合规**。
> ⚠ **架构未重开**(v3 已 converge 在凭据隔离之下的分层 broker);本 verdict 未要求改架构。
> ⚠ **语料永远单作者 trader韭团队**(operator 2026-06-30 确认):字典可放心对该团队文体过拟合,作者特异性是 feature 不是 bug。
> ⚠ **本 verdict 不审 spike 的工程实装复杂度 / 真实准确率落点**(那是 XenoDev/L4 才能产的硬证据,见 §"What this menu underweights")。forge 只把 spike 列为 PRD 工作项 + 定证据形状,不替 operator 拍跟单 go/no-go。

## Verdict

**GO · 用途锚定 + 可靠性前置的 gated refactor。** v4 推进三件事,不多做(双方 P3R2 §2 单一收敛,无 unresolved):

**①** 现在把 008↔004 消费契约写进 PRD,分两层:**无悔下游**(operator 自己回看检索 + 给 004 的「可溯源证据 + 置信度」契约)立即成立;**机器可信跟单信号** = 候选目标,**gated 在信号可靠性 spike 验证门之后**,PRD 用「候选/验证门」措辞并显式标注「build runtime 不得据此自行实现信号产品」(防 V4 写进 PRD 本体)。

**②** 信号可靠性 spike 列为 PRD 工作项、且是跟单候选的**硬前置**:XenoDev 跑小样本(~100-200 条),**分层报**(stance/conviction/action × 反讽/非反讽子集 × high-confidence 子集,false-positive signal 为一等风险)。spike pass 条件 = 产生 **decision-grade 证据**,**不由 forge 拍固定百分比**;置信度门槛由 operator 看分层数字后定。

**③** 字典第 1 层无悔(asker bug / entity_type 板块黑洞 / tech_side 三值 / 黑话词典)立即落地,**不等 spike**;第 2/3 层 gated 在「用途确定 + spike 通过」。边界硬约束:**008 只产可溯源结构化 + 置信度(C5/C9 内),信号决策归 004,不越界**。KG-24/KG-25 作框架可靠性附带必修入 W,实装留 XenoDev。

> **显式回应 K**:K#1(用途该不该现在定、定成什么)→ 现在定 008↔004 契约,无悔下游 now + 跟单 gated 候选(verdict ①);K#2(要不要先做信号可靠性 spike)→ spike 列 PRD 工作项 + 跟单硬前置,SOTA 证据(反讽轴 SOTA 仅 67-84%)支持「几乎必做」(verdict ②);K#3(字典三层怎么据用途取舍)→ 第 1 层 now、第 2/3 层 gated 在用途+spike(verdict ③);K binding「别让 build runtime 静默定产品方向(防 V4)」→ 核心:spike 由 forge 先列 PRD 工作项才让 XenoDev 跑,跟单 go/no-go 由 operator 据数字定;K「信号错标=真金亏损,比无信号更危险」→ 直接驱动 verdict ② 的「分层报 + false-positive 一等风险 + 置信度门槛」设计。

## Evidence map

| 结论 | 来源 | 引用(≤15 words) | 是否有反对证据 |
|---|---|---|---|
| 根因不是「008 没下游」,是「008↔004 消费契约从未写」 | P1-Opus §1A / P2-GPT §2(收窄) / P3R1-Opus §1 | "下游用途未定义的精确位置=008 与 004 之间的接缝" | - |
| 现 PRD 已把下游价值显式划给 004(US6 / 轻量粗约定包) | P1-Opus §1A / PRD US6+O5+line 93 | "008…作为 004 投资决策智能体的上游数据采集模块" | - |
| 机器可信跟单本质是 004 职责回流到 008 采集层 | P1-Opus §1A / P2-Opus §3 / P2-GPT §3 | "机器可信信号本质是 004 的职责回流到 008" | - |
| 跟单依赖的 stance/conviction/action 恰是被红队踢出无悔层的字段 | P1-Opus §1B / P1-GPT §1B / X#2 摘录 | "跟单依赖的恰恰是被踢出的那三个字段" | - |
| 「中等易错」从无实测分母,代价不对称使模糊档位不足以拍 go/no-go | P1-Opus §1B / §3#1 | "中等易错是个没有分母的形容词" | - |
| 干净金融 sentiment SOTA 88-97% 是上界,非本语料可指望 | P2-Opus §1 row1 / P2-GPT §1 row1 | "90% 是 clean-text 上界,不是本语料能指望的" | - |
| 反讽/code-mixed 专门任务 SOTA 仅 67-84% 且零/少样本 LLM 输给微调小模型 | P2-Opus §1 row2 / P2-GPT §1 row2 | "本语料 stance 会向 67-76% irony 带塌陷" | - |
| copy-trading 信号本身经验失败率高(独立于提取质量)→ 提取准是必要非充分 | P2-Opus §1 row3 / P2-GPT §1 row3 | "信号→盈利这步本身经验上高失败率…提取准只是必要非充分" | - |
| spike 必须分层报(反讽/非反讽 × high-confidence × FP-signal 一等风险),非单一总准确率 | P2-Opus §3 新浮现 / P3R1 双方 §3 分歧2 / P3R2 双方 §1 | "spike 必须分层报…false-positive signal 作为一等风险" | - |
| spike pass = 产生 decision-grade 证据,不由 forge 拍固定百分比 | P3R1-GPT §3 分歧2 / P3R2-Opus §1(撤回倾向值) / P3R2-GPT §1 | "把 spike pass/fail 先定为产生可决策证据,而不是现在拍百分比" | ⚠ Opus P3R1 草案曾隐含「forge 先给倾向值」,R2 撤回(见 underweight) |
| 字典第 1 层无悔可先落、第 2/3 层 gated;红队踢出 stance/conviction 被反讽数字事后证明正确 | P1 双方 §2(keep) / P2-Opus §3 / X#2 摘录 | "红队把 stance/conviction 踢出无悔层…被反讽数字事后证明正确" | - |
| 008 只产可溯源结构化(C9 内),系统替 operator 判方向跟单越界成 004 | P1-Opus §1A/§3#3 / PRD Scope OUT line 152 + C9 | "stance/conviction 作可溯源结构化存=C9 内;作机器跟单信号=越界" | - |
| KG-24 = manifest 状态语义无单一契约(纯工程 bug),倾向抽状态契约非一行修 | P1-Opus §1D/§2 / P1-GPT §1D / X#4 摘录 | "两处对 manifest 状态语义理解不一致" | - |
| KG-25 = LLM 坏 JSON 缺鲁棒层;重试解偶发解不了确定性坏,须清洗+降级+上报 | P1 双方 §1D / P2-Opus §1 row5 / P2-GPT §1 row4 | "重试解偶发、解不了确定性坏(KG-25 正是确定性坏)" | ⚠ KG-25 修 JSON 形状≠修 stance 语义(见 underweight) |

(上表 14 行,挑了最 load-bearing 的;其余次级结论散见各 round §1/§2/§3。)

## Intake recap

### X · 审阅标的(4 个)
- `discussion/008/handback/20260630T084333Z-008-pB-20260630T084333Z.md`(本仓库文件 · hand-back 包 · 75 行)— 核心 X:下游用途缺口 + 信号提取可靠性瓶颈 + KG-24/25 原始上报。
- `/home/ys/codes/XenoDev/docs/STRUCTURE-DICTIONARY-draft.md`(**外部 repo 文件** · 241 行)— 结构化字典三层划分 + 红队收敛后的无悔层 + 单作者约束。Opus 端已读全文;GPT 端 P1 §0 标"X#2 真实可读、未用 fallback"。
- `discussion/008/008-pB/PRD.md`(本仓库文件 · phased PRD · 315 行 · 现 v1.3)— 现 PRD 怎么定 gate / 用途,判断「用途从未定义」缺口的严重度。
- `/home/ys/codes/XenoDev/dogfood-backlog.md`(**外部 repo 文件** · KG-24 @591-618 / KG-25 @620-645)— 两条框架级数据缺陷的真实复现 + 候选解法。

### Y · 审阅视角
- ✅ 产品价值/用途成立性(核心)
- ✅ 提取可靠性/可行性(核心)
- ✅ 数据建模/字典设计
- ✅ 工程纪律(KG-24/KG-25 + 增量链路 + 结构化容错)

### Z · 参照系
- mode: **对标 SOTA**(架构/提取层)
- 用户外部材料: 无额外 URL;X 的 4 个标的即全部一手材料
- forbidden(binding,沿用 v1-v3): 法律 / ToS / DMCA / 合规检索一律不跑

### W · 产出形态
- ✅ next-PRD draft(补 008↔004 消费目标 + 把信号可靠性 spike 列为 PRD 工作项)
- ✅ decision-list 矩阵(字典三层字段 + PRD 条款的 保留/调整/删除/新增)
- ✅ next-dev-plan(信号 spike 执行计划:样本量 / 人工核验法 / 准确率门槛逻辑 / 反讽误判率)
- (本 v **未含** verdict-only / refactor-plan / free-essay → 下方对应章节不出现)

### K · 用户判准(完整摘抄)
008 跑到现在暴露根因问题:**结构化数据的下游用途/消费目标从未定义**。008-pB 的 PRD/spec 通篇定义「采集稳定性」,没有任何一条定义「结构化数据被某个下游消费并产生价值」。后果:字典第 2 层(方向/确定性/情绪/仓位/财报预期差…)和第 3 层(层级树/关系/跨文档/细粒度)全部悬空。继续堆字段=「纸上谈兵」。operator 已倾向下游做「自己回看检索 + 提炼投资信号/跟单」,且要**机器可信信号**(半自动跟单/报警,不是给人读个大概)。但要双专家盯死:**真瓶颈不是 schema 设计,是提取可靠性**。trader韭团队满嘴反讽(「这票真是好啊」可能是看空)+ 黑话(达子/卤馒头/谷子…),LLM 判 stance_direction/conviction/action_type 在这种语料中等易错,而这恰是跟单核心字段。**信号错标 = 真金白银亏损,比没有信号更危险。** 关键空白:LLM 在本语料提取这些信号的准确率从无实测数字。

最在乎(按顺序):
1. **用途该不该现在定、定成什么**:候选 = 自己回看检索(轻量)/ 提炼投资信号·跟单(机器可信,倾向)/ 对外产品(观点聚合·情绪指数·板块轮动图谱)。
2. **要不要先做信号提取可靠性 spike**:小样本(~100-200 条)让 LLM 提 stance/conviction/action、人工核准确率,拿真数字再决定 ① 跟单是否可行 ② 是否需置信度门槛 ③ 反讽/黑话误判率上界。要 forge **先把它列为 PRD 工作项** —— 绝不让 build runtime 静默替决产品方向(V4 失败模式)。
3. **字典三层怎么据用途取舍**:第 1 层无悔可不等 forge 先落地;第 2 层据用途点名挑;第 3 层全量重提只在确需图谱级查询时做(可逆的是重提,不可逆的是已烧的 LLM 成本)。

binding context:语料永远单作者 trader韭团队(过拟合 OK,黑话词典封闭可穷举值得一次建全)/ 合规不审 / 架构不重开 / KG-24(增量守护漏 skipped · high)+ KG-25(DeepSeek 坏 JSON 无容错 · medium)纳入批审给候选解立场。

### 收敛模式
**strong-converge** —— 双方 P3R2 §2 各为单一 GO · gated refactor verdict,逐项同向,均显式标"无 unresolved"。本文档收敛到单一 verdict。

---

## Decision matrix(字典三层 + PRD 条款 · W 含 decision-list)

> 范围:本矩阵合并两方 P3R2 §4 的 decision-list 草稿。每行可在 §"Evidence map" 或 §"Intake recap" 溯源。
> **优先级语义**:P0 = 立即(不等 spike)· P1 = 写进 PRD 待 build · P2 = gated 在 spike/用途之后。

| 类别 | 项 | 来源(X 标的具体位置) | 理由 | 优先级 |
|---|---|---|---|---|
| **保留** | 字典第 1 层无悔字段:asker / 双时间戳 / entity_type / tech_side 三值 / 黑话词典 | X#2 第 1 层 · 红队收敛后 | 修 bug + 真无悔 + LLM 可靠提 + 单团队高频;与下游用途无关 | P0 |
| **保留** | C5/C6/C9 可溯源红线 + 008 不直接给建议红线 | PRD C5/C6/C9 + Scope OUT line 152 | 是「只产可溯源结构化」边界的地基,不松动 | P0 |
| **保留** | SQLite SSOT + 三护栏(allowlist/C7/source_id)+ v3 凭据隔离 broker 架构 + 现采集稳定性 gate | PRD v1.2/v1.3 修订 | 架构本轮不重开;采集稳定性 gate 仍是 build-runtime 自证事实 | P0 |
| **调整** | 008↔004 出口:「轻量粗约定包」(PRD line 93)→ 「可溯源证据 + 置信度契约」 | P1-Opus §1A / PRD US6+line 93 | 把没写的 004 消费侧写实;字段含原文回链/实体/主题/可选置信度/降级标记 | P1 |
| **调整** | 字典第 2/3 层:从「悬空」→ 「gated 在用途确定 + spike 通过」 | X#2 第 2/3 层 / K#3 | 第 2 层据用途点名挑;第 3 层全量重提只在确需图谱查询时做(可逆的是重提) | P2 |
| **调整** | Phase gate 增「信号 spike 通过 + operator 定门槛」为跟单候选硬前置 | P3R2 双方 §2 ② | 防 build runtime 静默把字段堆成产品方向 | P1 |
| **删除/降级** | 「机器可信跟单 = 当前产品目标」这一(operator 倾向里隐含的)定位 → 降为候选 | K 倾向 / P3R1 双方分歧1 | copy-trading 失败率 + 反讽轴低准确率使「当前目标」站不住;降候选 gated | P1 |
| **删除/冻结** | 无悔层里「conviction/stance/author_tone 当前就提」的预设;第 2 层全量重提 / 第 3 层全量图谱化 | X#2 第 2/3 层 · 红队踢出理由 | 反讽数字事后证明踢出正确;未过 spike 门不写成自动跟单能力 | P2 |
| **新增** | 信号可靠性 spike(PRD 工作项 · ~100-200 条样本) | K#2 / P2 双方「几乎必做」 | 拿真实分层准确率才能判跟单 go/no-go;这是 v4 最该产的硬动作 | P1(列入)/ P2(执行) |
| **新增** | 008↔004 消费契约节 + 防 V4 的「build-runtime 不得自行定信号产品」PRD 条款 | P3R2-Opus §1 让步 / K binding | 把防 V4 写进 PRD 本体,不只留 forge 决议 | P1 |
| **新增** | KG-24 抽 manifest 单一状态契约(MEDIA_READY_STATUSES) | X#4 KG-24 候选解② / P1-Opus §1D | 根因是两处硬编码状态语义不一致,非漏一个枚举值 | P1(候选)/ XenoDev 实装 |
| **新增** | KG-25 结构化输出鲁棒层:清洗+鲁棒提取+降级标 degraded+失败可见(或 constrained decoding 待 L4 验) | X#4 KG-25 候选解 / P2 双方 §1 | 重试解不了确定性坏;须组合;只修 JSON 形状不修语义 | P1(候选)/ XenoDev 实装 |

---

## Next-version PRD draft(可回流改 008-pB PRD v1.3 → v1.4 · W 含 next-PRD)

> ⚠ **本草案不是新建独立 PRD,而是对现 `discussion/008/008-pB/PRD.md`(v1.3)的回流修订条目**。内容全部来自 forge v4 已验证事实,**不 daydream**。最终措辞 + 是否回流由 operator 拍板;若选 [A] fork 出独立 PRD branch,则把以下条目整合为新 PRD 本体。

```
# PRD 回流修订条目 · 008-pB · v1.3 → v1.4(草案)

**Status**: Draft from forge v4, awaiting human approval
**Sources**: discussion/008/forge/v4/stage-forge-008-v4.md + 关键 evidence(见 §"Evidence map")
**Driving verdict**: GO · 用途锚定 + 可靠性前置的 gated refactor(strong-converge · 无 unresolved)

## 一、新增节 · 008↔004 消费契约(替代现「轻量粗约定包」line 93)
008 输出**可溯源结构化证据包**,字段集:
- 原文回链(source_ref · 对齐 C6/C9 可回到顾问原话)
- 发布时间 / 形态 / 涉及 entities(带 entity_type)/ 主题
- 关键点(可溯源原始转录 + 视频稳定时间戳,对齐 US3/C6)
- 可选置信度(_confidence)+ 降级标记(degraded)
- 采集状态(对齐 C7 · 失败/不确定显式可见)
004 据此证据包**自行决定是否形成投资信号**。008 不产信号。

## 二、新增 US/Scope 表述 · 信号候选目标 gated
- US(候选 · gated):stance_direction / conviction / action_type 仅作为**信号可靠性 spike 的验证字段**,
  **未过 spike 门前不得写成自动跟单能力**;过门后是否升级为 004 跟单输入由 operator 据分层数字另行决议。
- ⚠ **防 V4 条款(写进 PRD 本体)**:build runtime 不得据此自行实现信号产品 / 不得把第 2 层字段堆成产品方向;
  产品方向(跟单 go/no-go + 置信度门槛)由 operator 据 spike 证据定。

## 三、Scope OUT / C9 澄清(强化现 line 152 红线)
- 008 不产买卖信号 / 仓位建议 / 收益判断(红线沿用)。
- stance/conviction/action 作「顾问原话的可溯源结构化」存(谁说 / 原话在哪 / 置信度)= C9 内;
  **作「系统替 operator 判方向跟单」= 越界成 004,永久 OUT**。
- 任何信号化消费必须在 004 或后续 PRD 承接,不在 008。

## 四、新增工作项 · 信号可靠性 spike(PRD 工作项)
- spike = 跟单候选的**硬前置**;pass 条件 = 产生 decision-grade 证据(规格见 §"Next-version dev plan" M2)。
- spike **不**由 forge 拍固定准确率阈值;置信度门槛由 operator 看分层数字后定。

## 五、字典三层取舍(写进 PRD 或 FORK-ORIGIN 备注)
- 第 1 层无悔:立即落地(M1),不等 spike。
- 第 2 层:据用途点名挑,gated 在用途确定 + spike 通过。
- 第 3 层:全量重提成嵌套树图只在确需图谱级查询时做。

## Scope OUT(本次新增 non-goals · 每条引用 evidence)
- ❌ 把「机器可信跟单」写成当前产品目标(evidence: copy-trading 失败率 + 反讽轴 67-84% · §"Evidence map" row7/8)。
- ❌ 未过 spike 门就提第 2 层信号字段并据此跟单(evidence: 「中等易错」无分母 · row5)。
- ❌ build runtime 自行决定产品方向(evidence: K binding 防 V4)。

## Open questions(forge v4 也没解决的 · 见 §"What this menu underweights")
- spike 真实准确率落点(只能 XenoDev 跑出来)。
- 反讽子集若准确率确实低 → 是否对反讽密集内容只存原文不提信号字段(v0.2 note 1)。
- KG-25 根治选型:constrained decoding(DeepSeek 是否支持)vs 清洗+鲁棒提取+降级(v0.2 note 3)。
```

---

## Next-version dev plan(M1-M4 · W 含 next-dev-plan)

> 合并两方 P3R2 §4 milestone 建议(Opus M1-M3 / GPT M1-M4)。**不到 spec 级**(spec 是 XenoDev/L4 的工作)。
> M1 与 M2/M4 可并行;**M2 是跟单候选的硬前置门**;跟单升级在 M2 出数字 + operator 决议之后,不在本计划内。

### Phase M1 · 字典第 1 层无悔落地(不等 spike · 预估 S-M)
- 目标:把「任何用途都需要 + 真无悔 + LLM 可靠提 + 单团队高频」的字段落地。
- 关键 milestone:
  - M1.1: entity_type(补 73-85% 无 ticker 的板块/指数/宏观黑洞;不补则板块层永久丢)
  - M1.2: tech_side 三值(右/左/na · 该团队最高频方言 · 明文可抓 LLM 极可靠)
  - M1.3: 黑话词典(独立文件 · 单团队封闭可穷举 · 一次建终身用)
  - M1.4: asker / 双时间戳 bug 修(records.author 存的是答主、提问人埋正文 · 保留 source_ref 回链)
- 依赖:无(与 spike 解耦)。
- 风险 / 排序:资源紧时先 entity_type(不补则永久丢的黑洞)后 asker(红队降为「搭便车字段」· v0.2 note 2)。

### Phase M2 · 信号可靠性 spike(跟单候选硬前置 · 预估 M)
- 目标:产 decision-grade 证据,让 operator 据真数字定跟单 go/no-go + 置信度门槛。
- 关键 milestone:
  - M2.1: 抽 ~100-200 条样本,**覆盖反讽/非反讽 + 黑话 + 免责声明 + 问答/图文**多类型。
  - M2.2: 人工金标(operator 或对照原文)stance / conviction / action 三字段。
  - M2.3: LLM 提取同三字段,**剥离免责声明后**比对。
  - M2.4: 产**分层报告** —— stance/conviction/action × 反讽 vs 非反讽子集 × high-confidence 子集,给出
    **precision / recall + 错标率上界 + false-positive signal 统计(一等风险)**。
- pass 条件 = 产生上述 decision-grade 证据(**不是 forge 拍的固定百分比**)。
- 依赖:M1 黑话词典(降低反讽/黑话误判)有助但非强阻塞。
- 风险:spike 必须分层,**不能退化成泛泛总准确率抽查**(SOTA 教训:反讽是误差主源 · §"Evidence map" row9)。

### Phase M3 · 无悔层之上的 008↔004 证据契约(PRD patch 后 · 预估 S)
- 目标:把 PRD 新增的「可溯源证据 + 置信度契约」落到 004 出口(替代轻量粗约定包)。
- 关键 milestone:
  - M3.1: 证据包字段集实现(原文回链 / entities / 主题 / 可选置信度 / degraded / 采集状态)。
  - M3.2: 验证 004 侧能稳定读入且不误认 008 在给建议(对齐 O5)。
- 依赖:M1(entity_type 等字段)+ PRD v1.4 契约定义。

### Phase M4 · 工程纪律 · KG-24/KG-25 框架修(并行可做 · 实装在 XenoDev · 预估 S-M)
- 目标:防结构化链路静默漏数 / 坏 JSON 假失败(支撑 spike 与重提可信)。
- 关键 milestone:
  - M4.1: KG-24 抽单一 manifest ready 状态契约(MEDIA_READY_STATUSES),两处入口共用。
  - M4.2: KG-25 结构化输出鲁棒层:清洗控制字符 + 鲁棒 span 提取 + 降级标 degraded + 失败计数可见告警
    (或 constrained decoding · DeepSeek 是否支持待 L4 验 · v0.2 note 3)。
  - M4.3: 保证 spike / 重提失败不静默(对齐 C7 一等公民)。
- 依赖:无;但 M4.2 应在 M2 spike 跑大批量前就位,避免坏 JSON 污染 spike 样本。
- 边界:forge 只列 decision + 候选解,**实装细节 + 选型留 XenoDev**(框架级变更走 dogfood-backlog → 攒批回 forge,XenoDev 不当场扩做产品方向)。

---

## What this menu underweights(强制自批判)

诚实表述本 stage 文档可能 underweight 的点。这是质量栏,不能跳过。

- **回声室风险(strong-converge 副作用)**:双方 P1 四维**全同向**(用途=refactor / 可靠性=new-spike / 字典=keep / 工程=refactor),P3 几乎无方向级对立,仅程度/落地收敛。**双方都同意但可能错的判断**:把跟单降为「候选 gated」可能**低估了 operator「机器可信」诉求的强度** —— 若 operator 实际要求跟单是 PRD 主目标(只是 gated),措辞应是「主目标 · gated」而非「候选」,这点 P3R1-Opus 分歧1 提过但 R2 收敛成「候选」时未再强调。请 operator 在 [C] 局部接受时校准这一颗粒度。
- **spike 真实准确率落点未知(最大 open)**:整个 verdict 的 ② 建立在「跟单 go/no-go 须等 spike 数字」之上,但 forge **没有也不能**产出那个数字。SOTA 给的是区间上下界(反讽轴 67-84%),**不是本语料的真分母**。真实数据(XenoDev 跑出的分层报告)可能推翻「跟单可行」或「跟单不可行」任一侧 —— 这正是 forge 刻意不替 operator 拍的部分。
- **反对/警示证据未充分整合**:§"Evidence map" 两条标 ⚠ —— (a) KG-25「修 JSON 形状 ≠ 修 stance 语义正确」:别让 M4.2 修好后产生「JSON 不坏了所以信号可信了」的错觉,二者正交;(b) Opus P3R1 草案曾隐含 forge 先给门槛倾向值,R2 已撤回为「数值全留 operator」,本文档采纳撤回后立场,但提醒 operator:spike 后定门槛**没有 forge 背书的锚点**,须自行据代价不对称拍。
- **Y 视角覆盖盲区**:Y 未单列「成本/ROI」视角。spike 本身要烧人工金标时间(~100-200 条三字段标注)+ LLM 成本;若 operator 资源极紧,「先做 M1 无悔层、spike 押后」是合法路径(verdict 已允许 M1 不等 spike),但本文档未量化 spike 的具体代价。
- **K 中未充分回应的关切**:K#1 候选里的**第三类「对外产品(观点聚合/情绪指数/板块轮动图谱)」**双方几乎未展开 —— 因 operator 自陈倾向跟单、且对外产品涉及多作者/传播会撞 C5 渠道中性,被默认搁置。若 operator 未来想转对外产品方向,需另起 forge(本 verdict 不覆盖)。
- **X 标的覆盖局限**:004 智能体本身的 PRD/现状**未在 X 标的内**(本轮只读 008 侧 4 个标的)。「008↔004 契约」的 004 侧需求是基于 008 PRD 反推 + 双专家推断,**未经 004 实际 PRD 校验**。若 004 有独立 PRD,契约字段集应回 004 侧对齐。
- **forge versioning 提示(什么会触发 v5)**:① spike 跑出数字后若 operator 要据此把跟单升级为正式产品方向(改产品定位)→ 起 v5;② 若 spike 显示需「分内容类型差异化提取」(反讽密集只存原文)成为架构级改动 → 起 v5;③ 若 004 侧 PRD 与本契约冲突 → 起 v5;④ PRD v3 Open notes 里「列表截断出现第三种情况(登录态轮换/风控验证码)」仍是悬而未决的 v4 触发点(与本轮用途/可靠性正交,但仍在 008 上空)。

## Decision menu(for human)

### [A] 接受 verdict 进 L4(需 fork 出 PRD branch)
```
⚠ XenoDev build runtime 消费的是 HANDOFF 包(per SHARED-CONTRACT §6),不直接吃 forge stage 文档。
⚠ 现有仓库 PRD 都是平铺布局 —— discussion/<root>/<prd-fork-id>/PRD.md(无嵌套)。
流程(暂时手工,等待 /fork-from-forge 命令落地):

1. 选一个 prd-fork-id:
   - <id>=008 的现役 PRD 是 fork 008-pB → 新派生名如 008-pB-pForge / 008-forgeV4
   - prd-fork-id 直接放在 discussion/008/ 下(平铺,不嵌套)

2. 创建 discussion/008/<prd-fork-id>/PRD.md
   - 把本 stage 中的 §"Next-version PRD draft" 抽出为 PRD 本体
   - 补 frontmatter:
     **PRD-form**: phased(沿用 008-pB)
     **Source**: forge stage-forge-008-v4.md

3. 创建 discussion/008/<prd-fork-id>/FORK-ORIGIN.md
   说明 forked-from = forge v4 stage,parent = 008-pB(非 L3 candidate)

4. /plan-start <prd-fork-id> → 产 HANDOFF.md → 新开 XenoDev session 真开发
```
> ⚠ **更轻量的替代(推荐先考虑)**:本 verdict 的 PRD 草案是**对 008-pB v1.3 的回流修订**(沿用 v1/v2/v3 的修订链模式),
> **不一定要 fork 新 branch**。可走 `/scope-inject 008-pB`(若该命令支持)把 §"Next-version PRD draft" 五条整合进
> 008-pB PRD v1.4,保持单一现役 PRD。fork 新 branch 仅在 operator 想保留 008-pB v1.3 不动、并行试验时才必要。

### [B] 跑 forge v5(说明需要补什么)
```
/expert-forge 008
# 在 Phase 0 intake 时调整 X / Y / Z / W / K
# 旧 v4 整目录保留作历史参考
```
适用:spike 已出数字要据此升级跟单定位 / 需把 004 侧 PRD 纳入 X 重审契约 / 出现列表截断第三种情况 / 想转对外产品方向(见 §"What this menu underweights" forge versioning 提示)。

### [C] 局部接受
列出哪几条采纳、哪几条挂起:
- ✅ 建议立即采纳:**verdict ③ 第 1 层无悔(M1)**(不等 spike,与下游用途无关,纯收益)+ **verdict ① 的「008 只产可溯源结构化、信号决策归 004」边界**(已是现 PRD 红线的强化)。
- ⏸ 建议挂起待确认:**跟单的颗粒度措辞**(「候选」vs「主目标·gated」—— 见 §underweight 回声室风险,operator 校准后再定 PRD 文字)。
- ❌ 可拒绝/缓做:**KG-24/KG-25 实装时机**(framework 级,可攒批走 XenoDev dogfood-backlog,非本轮硬性)。

### [P] Park
```
/park 008
```
保留所有 forge v4 产物,标记暂停。复活时不重做这一层(spike 决议挂起、字典第 1 层挂起)。

### [Z] Abandon
```
/abandon 008
```
forge verdict 显示该 idea 不该继续做。归档 lesson 文档。
> ⚠ **本 verdict 是 GO 不是 abandon** —— 此项仅为菜单完整性保留;选它意味着 operator 决定整个 008(含已 ship 的 v0.1)不再推进,与 v4 verdict 相悖,慎选。

---

## Forge log
(由 /expert-forge 命令更新;记录每次 forge run 的 v 序列 + 关键 verdict 一句话)

- v4: 2026-06-30 — verdict: "GO · 用途锚定 + 可靠性前置的 gated refactor:现在定 008↔004 契约(无悔下游 now + 跟单 gated 候选)/ 信号可靠性 spike 列 PRD 硬前置 / 字典第 1 层 now·第 2/3 层 gated;008 只产可溯源结构化+置信度,信号决策归 004。"
- v3: 2026-06-20 — verdict: "GO(分层架构):凭据隔离硬约束之下受控自动翻页落地为三层 broker + SHARED-CONTRACT §2 新增采集会话凭据隔离子条款。"
- v2: 2026-06-16 — verdict: "GO:Obsidian 个人知识库前端(US8)· 单向 exporter · SQLite 仍唯一 SSOT · C5 渠道中性。"
- v1: 2026-06-05 — verdict: "refactor-and-reset:Phase-0 探针误判证伪,C5 措辞改写 + 回放复位 + gate 判准改向自动化稳定性。"
