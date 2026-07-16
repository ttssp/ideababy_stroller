# Forge v1 · 001 · P2 · Opus(Claude Code main)· 参照系评估(with search)

**Timestamp**: 2026-07-16T02:15:22Z
**Searches run**: 4,SOTA-benchmark(限验证/gate 设计先例层,per forge-config Z)
**Visibility**: 我已读对方 P1(P1-GPT55xHigh.md)。

## 1. SOTA 对标

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| P0.2 人肉盲测二值 gate | Human-in-the-loop eval 工业实践(Braintrust / Maxim / Label Studio / Comet) | 人类审查走 **spot-check 随机抽样 + uncertainty sampling**(低置信路由给人)+ diversity sampling;专家抽查让系统持续可问责 | 停机、operator 全量盲读 3 切片、二值签字解锁下游 | 工业界**没有**「人肉盲测二值签字作阻断发布闸门」的先例形态;人的角色是抽查者/校准者,不是一次性考官 | getmaxim.ai · labelstud.io · braintrust.dev · comet.com |
| operator 判据可靠性(批评①) | 噪声评审统计处理(arXiv "Noisy but Valid" 2601.20913 · "How to Correctly Report LLM-as-a-Judge" 2511.21140) | 把评审者当**噪声传感器**:小校准集估其 TPR/FPR,误差校正后做推断,控制 type I error;主观任务人类 kappa 仅 0.3-0.6 | 单轮 3 切片 1 负控,直接二值 PASS/FAIL | 文献明确警告单轮二值裁决不可靠;标准解法 = 校准集 + **多轮累积 + 误差校正**,与 operator「我不是可靠打分器」自评精确同构 | arxiv.org/abs/2601.20913 · arxiv.org/abs/2511.21140 |
| 「前置 gate vs 边用边校准」(批评③) | 2026 成熟 LLM 团队三分工(SentryML / TrueFoundry / qaskills) | offline eval 管发布 + **CI 自动化 gate**(机器可跑、秒级)+ 生产持续监控/定期再校准,三者互补;"every production trace carries quality verdicts" | 唯一阻断点 = 人肉盲测 RERUN-PASS artifact | SOTA **保留阻断 gate 但它是自动化的**;人肉判断被移到在线抽样与校准循环。即:砍人肉二值 ≠ 砍一切阻断检查 | sentryml.com · truefoundry.com · qaskills.sh |
| 留痕验收(批评②) | AI audit-trail 规范(NIST AI RMF 引述 · Snowflake / VisoTrust / isimplifyme) | 审计单元 = **全量、防篡改、可长期回溯**的 trace(版本+决策日志+人工监督记录+数据 provenance 四件套);抽样只够监控、不够为单个决策辩护 | O2 已要求 3 击回溯,但只是产品功能,不是验收机制 | 留痕必须**机器全量**、人肉才可抽查——「全量 trace 由机器保证 + 人抽查」的分工是标准形态,恰是 operator 批评②的原话结构 | snowflake.com · visotrust.com · isimplifyme.com |

## 2. 用户外部材料消化

n/a — K 内无外部链接/文件(forge-config §Z「外部材料叠加:无」)。

## 3. 修正后的视角

- P1 判断(工程纪律)「强制点应移到 in-band 留痕完整性,那才是能被真正 enforce 的纪律形态」→ **站住且被加强**:audit-trail 规范正是把「全量防篡改 trace」当审计单元,四件套里「human oversight records」对应 operator 抽查留档——机器管全量、人管抽查的分工有直接先例(§1 行 4)。
- P1 判断(产品价值)「盲测仪式偏 cut,识伪留作可选校准」→ **站住**:四路检索均未发现「人肉盲测二值签字作阻断闸门」的工业先例;人的角色一律是 spot-check/校准(§1 行 1)。对方 P1 的更锐利表述「产品价值 cut」在 SOTA 映衬下成立。
- P1 不确定 #3「抽查功效是否只是更便宜的剧场」→ **部分解决,且答案比两个选项都好**:SOTA 不是「抽查功效更高」,而是「把人当噪声传感器,用校准集+多轮累积+误差校正做推断」(§1 行 2)。新形态的诚实框架应是**累积校准证据流**,不是任何单轮裁决——这同时确认了旧 gate 功效低(operator 批评①有文献背书)和「新形态若只是换个单轮仪式则同样是剧场」。
- P1 判断(架构设计)「砍带外签字、解锁改为机器可验的留痕验收」→ **站住但需补一刀**:SOTA 三分工里 CI 自动化 gate 仍是阻断的(§1 行 3)。故 T010/T011 新解锁不应是「无 gate 直接放行」,而是「**机器可自动判的 smoke gate**(trace 完整性/引用可达性等)阻断 + operator 抽查非阻断」。这修正了我 P1 §3.1 里选项 (c)(纯非阻断告警)的倾向——纯告警会丢掉防 V4 的 STOP 精神,K 明言那不可丢。
