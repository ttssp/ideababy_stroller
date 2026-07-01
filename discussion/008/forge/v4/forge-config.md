---
forge_version: v4
created: 2026-06-30T09:03:24Z
convergence_mode: strong-converge
x_hash: b5c8cfe432db47fb3f4e48e4d1bbcecd
prefill_source: manual
---

# Forge Config · 008 · v4

> **触发**:`/handback-review 008`(2026-06-30)决议 20260630 hand-back 包 → 起 forge。
> **与 v1/v2/v3 的边界**:v1 定 C5 采集边界、v2 定 Obsidian 人读前端、v3 定凭据隔离之下的受控自动翻页 broker 架构。**那三轮全部 done 且只解工程/架构/合规**。v4 审的是 **v3 之后冒出来的产品方向问题**:结构化数据的下游用途从未定义,以及「机器可信信号/跟单」这一倾向的可行性瓶颈(提取可靠性)。**v4 不重审架构 / 不重审合规**(合规仍是 operator 已拍板的 binding 前提,沿用 v1-v3)。

## X · 审阅标的

(operator 经 AskUserQuestion 勾选 4 项,manual intake)

```
1. discussion/008/handback/20260630T084333Z-008-pB-20260630T084333Z.md
2. /home/ys/codes/XenoDev/docs/STRUCTURE-DICTIONARY-draft.md
3. discussion/008/008-pB/PRD.md
4. /home/ys/codes/XenoDev/dogfood-backlog.md (KG-24 / KG-25 两条)
```

### 解析后的标的清单

- `discussion/008/handback/20260630T084333Z-008-pB-20260630T084333Z.md`(类型:本仓库文件 · hand-back 包 · 75 行)— **核心 X**。下游用途缺口 + 信号提取可靠性瓶颈 + KG-24/25 的原始上报。§3 给出 forge 的 X 标的清单。
- `/home/ys/codes/XenoDev/docs/STRUCTURE-DICTIONARY-draft.md`(类型:**外部 repo 文件** · 241 行)— 结构化字典三层划分 + 红队收敛后的无悔层 + 单作者约束。字段取舍的 evidence base。⚠ **Codex 沙箱 BLOCK risk**:此文件在 XenoDev 仓(`/home/ys/codes/XenoDev/`)非 IDS 仓内。Opus 端已读全文;Codex 若沙箱不可达 → 在 P1 §0 显式标 "skipped due to access",**不要假装读了**。关键内容已在本 config 末尾 §"X-fallback TEXT" 摘录,Codex 可据摘录评价。
- `discussion/008/008-pB/PRD.md`(类型:本仓库文件 · phased PRD · 315 行)— 现 PRD。让专家看现 PRD 怎么定 gate / 用途,才能准确判断「用途从未定义」这一缺口的严重度 + 怎么补。
- `/home/ys/codes/XenoDev/dogfood-backlog.md`(类型:**外部 repo 文件** · 646 行,只需 KG-24 @591-618 / KG-25 @620-645)— 两条框架级数据缺陷的真实复现 + 候选解法。⚠ **Codex 沙箱 BLOCK risk** 同上;两条全文已在 §"X-fallback TEXT" 摘录。

## Y · 审阅视角

(operator 勾选 4 项)

✅ **产品价值/用途成立性** —— 结构化数据到底服务不服务一个真下游?「机器可信信号/跟单」作为产品目标是否立得住?(**核心**)
✅ **提取可靠性/可行性** —— LLM 在反讽+黑话语料提 stance_direction / conviction / action_type 的准确率够不够支撑跟单?需不需要先做可靠性 spike?(**核心**)
✅ **数据建模/字典设计** —— 三层字典划分合不合理?无悔层边界(红队收敛后)准不准?字段该不该据用途取舍?
✅ **工程纪律** —— KG-24/KG-25 这类框架缺陷;增量链路可靠性;结构化提取容错机制。

## Z · 参照系

mode: **对标 SOTA**

- 双方 Phase 2 各自检索领域 SOTA,聚焦**架构/提取层**,为「信号可行性」提供外部证据:
  - 金融文本 LLM 信号提取准确率研究(stance / sentiment / event extraction on financial text)
  - 反讽 / 讽刺 / 谐音黑话 NLP 检测难度(sarcasm detection、code-mixed / slang NER 的已知准确率上界)
  - 跟单 / copy-trading / signal-from-text 系统的失败案例与演化路径
  - LLM 结构化输出鲁棒性(坏 JSON 容错)的工业范式(对 KG-25)
- **forbidden**(binding,沿用 v1-v3):法律 / ToS / DMCA / 合规检索一律不跑。合规是 operator 已拍板前提,**GO ≠ 合规**。
- **外部材料叠加**:无额外 URL;X 的 4 个标的即全部一手材料。

## W · 产出形态

(operator 勾选 3 项)

✅ **next-PRD draft** —— 下一版 PRD 草案:补「下游用途/消费目标」定义 + 把「信号提取可靠性 spike」列为 PRD 工作项。可回流改 008-pB PRD。
✅ **decision-list 矩阵** —— 结构化字典三层字段的 保留/调整/删除/新增 4 列矩阵(据用途取舍 stance/conviction/action/sentiment 等)。
✅ **next-dev-plan** —— 若决议做信号 spike,给 spike 的执行计划(样本量 / 人工核验法 / 准确率门槛 / 反讽误判率上界)。

## K · 用户判准

我要 forge 这个标的,是因为 008 跑到现在暴露了一个根因问题:**结构化数据的下游用途/消费目标从未定义**。008-pB 的 PRD/spec 通篇定义的是「采集稳定性」(gate 判准 = build-runtime 可自证的工程事实,合规与用途由 operator 负责、不进 gate),**没有任何一条定义「结构化数据被某个下游消费并产生价值」**。后果:结构化字典的第 2 层(方向/确定性/情绪/仓位/财报预期差…)和第 3 层(层级树/关系/跨文档/细粒度)全部悬空——无法判断该不该提、该提哪些。继续在 build runtime 堆字段,就是我担心的「纸上谈兵」(为没确定的用途过度设计)。

我已经倾向下游做「自己回看检索 + 提炼投资信号 / 跟单」,而且要的是**机器可信信号**(能半自动跟单 / 报警,不是给人读个大概)。但我要双专家替我盯死一件事:**这个倾向的真瓶颈不是 schema 设计,是提取可靠性**。trader韭团队满嘴反讽(「这票真是好啊」可能是看空)+ 黑话(达子 / 卤馒头 / 谷子…),LLM 判 stance_direction(看多空)/ conviction(确定性)/ action_type(加减仓)在这种语料**中等易错**——而这恰恰是跟单依赖的核心字段。**信号错标 = 真金白银亏损,比没有信号更危险。** 关键空白:LLM 在本语料提取这些信号的准确率**从来没有实测数字**,红队只是定性推测。在拿到真实准确率之前,「机器可信信号 / 跟单」的可行性**无法判定**。

所以我最在乎的几件事,按顺序:
1. **用途该不该现在定、定成什么**:候选 = 自己回看检索(轻量)/ **提炼投资信号·跟单(机器可信,我倾向)**/ 对外产品(观点聚合·情绪指数·板块轮动图谱)。用途定了,字典第 2/3 层才有取舍依据。
2. **要不要先做「信号提取可靠性 spike」**:跟单真瓶颈是提取可靠性。我想要双专家判断:该不该先用小样本(~100-200 条)让 LLM 提 stance/conviction/action、我或对照原文人工核准确率,拿真数字再决定 ① 跟单是否可行 ② 是否需要置信度门槛(只保留 high-confidence 信号)③ 反讽/黑话误判率上界。这是 XenoDev 能直接产的硬证据,但我要 forge **先把它列为 PRD 工作项**——绝不让 build runtime 静默替我决定产品方向(这正是 V4 的失败模式)。
3. **字典三层怎么据用途取舍**:第 1 层无悔(asker bug / entity_type 板块黑洞 / tech_side 三值 / 黑话词典)可以不等 forge 先落地;第 2 层据用途点名挑;第 3 层全量重提成嵌套树图只在用途确需图谱级查询时才做(我接受红队那句:可逆的是重提,不可逆的是已烧的 LLM 成本)。

贯穿全程双方要记住的 context:
- **语料永远只出自 trader韭团队一家**,不扩展其他作者。所以字典可以**放心针对该团队文体过拟合**(右/左侧方言、四桶仓位、黑话谐音、BDSR/SP 期权打法、「鬼故事」风险叙事),作者特异性是 feature 不是 bug。黑话词典是封闭可穷举的,值得一次性建全。
- **合规不在本轮范围**(operator 已拍板并担责,沿用 v1-v3)。不要论证自动翻页 / 采集是否违法。
- **架构不在本轮范围**(v3 已 converge 在分层 broker)。除非用途/可行性结论**反过来**要求改架构,否则不重开架构议题。
- KG-24(增量守护漏 skipped → 漏 ASR · high)/ KG-25(DeepSeek 坏 JSON 无容错 · medium)是随包回流的框架级缺陷,纳入本轮批审,给候选解法的取舍立场。

---

## X-fallback TEXT(供 Codex 沙箱不可达 XenoDev 仓时使用)

> 以下是 X#2(STRUCTURE-DICTIONARY-draft.md)和 X#4(dogfood-backlog KG-24/25)的关键摘录。**Opus 端已读两文件全文**;此摘录仅为 Codex 在沙箱不可达 `/home/ys/codes/XenoDev/` 时提供评价依据。Codex 若能直接读原文件 → 以原文件为准,本摘录可忽略。

### X#2 摘录 · 结构化字典三层(红队收敛后)

**判据钉死**(红队批判后):无悔 = ① 修 bug(任何用途都需要)② 真无悔(不赌具体下游)③ LLM 可靠提取 ④ 单团队真高频。「信息价值高」≠「无悔」。

**第 1 层 · 无悔层 ✅(现在做)**:
- `asker`(问答提问人拆分,修 bug:records 只有 author 存的是答主,提问人埋正文)
- `asked_at`/`answered_at`(问答双时间戳,修 bug)
- `entity_type`(tickers→带类型 entities:73-85% key_point 无 ticker,因只抓个股不抓板块/指数/宏观=60%主语;不做=板块层永久丢)
- `tech_side`(右/左/na 三值,该团队最高频方言 + 明文可抓 LLM 极可靠;砍掉 left_with_value/turning 细分)
- 黑话词典(独立资产,单团队封闭可穷举,一次建终身用)

**第 2 层 · 赌用途层 ⚠️(冻结,等下游定再挑)**:stance_direction(⚠反讽中等易错,须带 _confidence)/ conviction(⚠语气判断不可靠,自报"准确率追踪命门")/ author_tone(humorous_sarcastic 最高频也最易错)/ asker_emotion / answer_evasion / priced_in / positions / action_type / directiveness / time_horizon / risk_attribution / theme_tags / catalyst / 财报层(vs_consensus 等)/ content_type 8 值细分。

**第 3 层 · 结构/关系层 🏗️(架构对·走轻量壳·全量重构待命)**:sections(原文层级树)/ relations(要点间对比因果)/ cross_refs(跨文档引用)/ 细粒度标注。红队驳「可逆所以不亏」:可逆的是重提(原料在),不可逆的是已烧的 LLM 成本+时间。

**执行 = 方案 B**(轻量可逆):只做第 1 层(文档级补 asker+时间戳 · 要点级只加 entity_type · 黑话词典独立文件 · tech_side 三值),第 2/3 层冻结。每条只多 1-2 字段。

**仍悬而未决**:下游用途未定义 → 赌用途层必须等下游目标定才值得做,operator「纸上谈兵」质疑依然成立。**定无悔层 ≠ 解决了用途问题,只是把无悔的先做了。**

**作者约束**(operator 2026-06-30 确认):所有内容永远只出自 trader韭团队一家,不扩展。作者特异性是 feature 不是 bug,可放心过拟合该团队文体。

### X#4 摘录 · KG-24 / KG-25

**KG-24(框架级 · high)**:增量守护 `_pending_replays_fn`(daemons.py:60-76)只认 manifest `status=="downloaded"`,**漏 `skipped`**;而正牌 ASR 入口 `run_asr_from_manifest`(batch.py:212-213)认 `status in ("downloaded","skipped")`。多 token 窗口断点续下载时,已下产物被标 `skipped` → 守护视而不见 → 永久漏 ASR(本次 43 个里 31 个被漏,守护只补 12)。**两处对 manifest 状态语义理解不一致**。受益面 = 所有「批量下载(含断点续)→ 守护增量消费」链路。候选解:① 守护改认 downloaded+skipped(一行修)② 抽单一状态契约 `MEDIA_READY_STATUSES`(根因:两处各自硬编码)③ manifest 显式标 `media_present: bool`。

**KG-25(框架级 · medium)**:DeepSeek 结构化提取无坏-JSON 容错。`make_deepseek_text_summarize`(tools.py:47-50)直接 `json.loads(content)`,无清洗/无重试/无降级。LLM 对特定正文**确定性**返回非法 JSON(未转义控制字符/裸换行,连试 3 次同位置失败)→ 一次失败即 raise → 守护 try/except 静默吞(错误计数+1 但不告警)→ 该条每轮被重选每轮失败,summary 永久缺,operator 无从知晓。受益面 = 所有「调 LLM → json.loads 产物」链路。候选解:① 控制字符清洗再 loads ② 重试 N 次(对确定性坏无效,须配①)③ 鲁棒 JSON 提取(json5/dirtyjson)④ 降级:坏 JSON 退回整段当单 key_point + 标 degraded ⑤ 失败计数上报可见。
