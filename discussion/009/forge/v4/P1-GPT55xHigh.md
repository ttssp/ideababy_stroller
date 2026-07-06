# Forge v4 · 009-pForge · P1 · GPT55xHigh

**Timestamp**: 2026-07-06T05:15:45Z
**Search used**: NONE
**Opponent P1 read**: NO

## §0 我读到的标的清单 + 阅读策略 + K 摘要

读到 6 个标的:hand-back、assembler、Telegram narrative、UI router、T015 `alpha_lane.py`、`realized_return.py`。为复核 UI/缓存/承载语义,额外读了 UI 两个模板、`strategy_signal.py`、`conflict_report.py`、`llm/client.py`、`llm/cache.py`。未读 `P1-Opus47Max.md` 正文。

阅读策略:不接收 hand-back 结论,逐项回真代码复核。K 摘要:必须定死 (a) 非方向 evidence 是 ConflictReport 一等公民还是复用 direction 五值;(b) R3-F1 缓存 silent-wrong 必须真解;(c) Telegram/UI 是否改成 N 路且方向票/evidence 分区。binding:守 alpha_lane 的 `NO_VIEW/confidence=0/is_directional=False`,守 OUT-10,契约要能指导 XenoDev FU-task,产品展示不能让 operator 误读为第四张方向票。

## §1 现状摘要

**架构正确性 / 器官边界**:alpha 不能产方向站住。`realized_return.py:231` 已按历史信号方向 signed,正 excess 只说明“跟随历史方向有 edge”,不说明当前多空。T015 因而在 `alpha_lane.py:247-266` 产 `NO_VIEW/confidence=0.0`,把 `signal_kind/is_directional/evidence_strength` 放 `inputs_used`。问题是 004 `ConflictReport` 只有 `signals` 槽(`conflict_report.py:28-33`),`Direction` 仍是方向/无观点枚举(`strategy_signal.py:19-27`),没有非方向 evidence 的一等位置。

R3-F1 独立复核:站住。assembler 的 hash 只取 `source_id=direction:confidence_bucket`(`conflict_report_assembler.py:159-175`)。LLM cache key 由四元组+sorted extras 生成,不含 prompt 正文(`llm/cache.py:137-156`;`llm/client.py:171-179,237-246`)。所以强/弱/error alpha 都可落成 `analyst_alpha=no_view:low`,同 key 复用旧根因,是 silent-wrong。

**产品语义 / 用户可见性**:R3-F2 部分站住。Telegram 真丢第四路:`conflict_narrative.py:54-63` 固定 `signals[:3]`。UI 不真丢:`router_conflicts.py:169-176` 把 `remaining` 拼回,模板循环 `ordered_signals`(`_three_columns.html:10-24`)。但 UI 仍误导:它显示 direction/confidence/rationale,不显示 `evidence_strength`;用户会看到 `no_view 0%`,很难理解这是历史 alpha 质量旁证。

## §2 三子决策 first-take 评分

**(a) 8/10:轻扩一等公民。** 不建议复用 direction 五值;把语义藏在 `inputs_used` 会要求所有消费者二次判别 `signal_kind/is_directional`,是新脆点。保留三路方向票主结构,给非方向 evidence 显式旁路/类型。

**(b) 10/10:必须纳入 evidence 语义指纹。** 只要 evidence 参与 prompt/root-cause,cache key 就应含 `signal_kind/is_directional/evidence_strength/z_excess/reason/error_type`;短期无法规范化则对该路径禁 cache。

**(c) 7/10:Telegram 必改;UI 改语义。** Telegram 从固定三行改为方向票+evidence 区。UI 已透传第四路,但也要分区展示,用“历史 edge 旁证/强度/样本数/显著性”语言,避免 operator 把它计入方向多数票。

组合最优路径:轻扩 ConflictReport evidence lane → evidence digest 进缓存键 → Telegram/UI 分区渲染。它比全面重写 004 小,也比 NO_VIEW 复用稳,且能直接落成 XenoDev 下游集成 FU-task。

## §3 我现在最不确定的 3 件事

1. 轻扩应是 `evidence_lanes` 旁路,还是把 `signals` 升级为 discriminated union。
2. 非方向 evidence 是否参与 `has_divergence/divergence_root_cause`,还是只作报告附注。
3. 展示只给 `evidence_strength` 是否足够,还是必须同时给 z、样本数、horizon、显著性以免误读。
