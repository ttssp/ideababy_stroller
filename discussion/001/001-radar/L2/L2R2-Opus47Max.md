# Idea 001/001-radar · L2R2 · Claude · Cross + Value Validation

**Timestamp**: 2026-07-06T13:30:00Z
**Opponent's L2R1 read**: yes
**Searches run**: 8, value-validation only
**Model note**: 本轮由 Claude(Fable 5)执笔,文件名沿用管线约定。

## 1. From opponent's L2R1, what sharpened my thinking

1. **"所有新增都长得像噪声"这个病灶定义**比我的"big picture 悄悄过期"更准:敌人不是数量,是**新增的同质化**——爆款补丁 paper 和"把两个方法族接起来"的 paper 在 feed 里长得一样。radar 的任务是把第二种从第一种里拎出来。这直接定义了品味层的工作对象。
2. **claim/问题意识作为第三类节点**+"谁推翻了谁的瓶颈叙事"这类边。我停在 paper+方法双层,GPT 把 claim 层补上了——而"contradicts"这种边真正挂的对象恰恰是 claim,不是 paper。图的语义骨架应该是三层。
3. **"组会前挑 3 篇精读"场景**把"不替代精读"这条 limit 翻成了正面产品语义:地图不是阅读的替代品,是**精读的选择器**(读什么、带什么问题读、读完放回哪)。这比我"判断的外骨骼"更可落地。
4. GPT §6-Q3(位移的最可信表达是图、briefing、前后快照、还是问题清单)是**本 fork 最好的产品形态问题**——我默认了"地图"是主容器,这个默认值得被审。

## 2. Where I'd push back

1. **"覆盖足够窄位移才有意义"这道栅栏缺一扇门**。原提案明确要求"给一个新工作,若无对应 topic 则新建并主动搜索补齐"——lab 负责人的真实工作里,"评估一个**还没进我 8~15 个 topic**的新方向"(GPT 自己的场景三!)恰是高价值时刻。冷启动一张新 topic 地图必须是一等公民动作,不是例外。
2. **30 秒 aha 里那句"frontier 漂移"叙事是一句 briefing,不是一张地图**。如果最有价值的 payload 是那句话,图可能只是生成那句话的中间产物——那产品重心就该在叙事而非可视化。GPT 同时押了"地图为主"和"一句话最尖锐"两注,没有指出两者之间存在张力。
3. **"第二记忆"的六个月图景跳过了信任的建立过程**。用户凭什么从"看看"走到"依赖"?中间必经的是若干次"地图说的和我后来验证的一致"。这个信任积累机制在两份 R1 里都缺席,L3 必须补。

## 3. Search-based reality check

| Claim | Source side | What I searched | What I found | Verdict |
|---|---|---|---|---|
| 现有图工具没做"方法级节点+位移 payload" | 双方 §2 | Connected Papers/Litmaps/ResearchRabbit 2026 功能对比 | 三者都是 paper 级、种子式静态图。[Litmaps 有时间轴+momentum 指标](https://effortlessacademic.com/litmaps-vs-researchrabbit-vs-connected-papers-the-best-literature-review-tool-in-2025/);[RR 已被 Litmaps 收购(2025-11)转 freemium](https://effortlessacademic.com/litmaps-vs-researchrabbit-vs-connected-papers-the-best-literature-review-tool-in-2025/),定位持续监控但单位仍是 paper | **大体成立**;Litmaps 时间轴+momentum 是"半步位移",差异化须踩在方法级+diff 叙事上 |
| "方法/技术"是研究者思考单位,方法级结构有人要 | Opus §2 | Papers with Code 关停后果;ORKG 采用情况 | [PwC 2025-07 被 Meta 关停](https://hyper.ai/en/news/42900),其众包方法分类+leaderboard 消失,[社区在呼吁替代品](https://www.researchgate.net/post/Can_someone_replace_papers_with_code);[ORKG 做结构化方法级对比但人工策展不可扩展](https://orkg.org/) | **支持,且新增时机变量**:方法级基础设施的空洞 12 个月内刚被腾出 |
| contradicts/supersedes 边没人规模化做过 | Opus §2(隐含) | scite.ai claim 级引用意图 | [scite 已对 15 亿条 citation statement 做 supporting/contrasting 分类](https://www.biorxiv.org/content/10.1101/2021.03.15.435418.full.pdf) | **部分推翻**:claim 级边已有规模化先例;我们的差异只能落在位移呈现+方法粒度+决策语境,不能落在"有这种边" |
| lab 负责人被淹没,需求真实且在恶化 | 双方 §1 | 2025-26 论文洪水证据 | [LLM 使采纳者产出 bioRxiv +50%/arXiv +1/3,Berkeley/Cornell 指"区分有价值工作"成为系统性危机](https://newsroom.haas.berkeley.edu/how-ai-is-transforming-research-more-papers-less-quality-and-a-strained-review-system/) | **强支持**:比 4 月立项时更痛,且"筛出结构性工作"恰是本产品的刀刃 |
| 气氛 dashboard 会退化成没人看第二次的装饰 | Opus §6-Q3 / L1R2 警告 | BI dashboard 弃用研究 | [72% 用户弃 dashboard 回电子表格;失败主因=与决策隔离建设+认知过载](https://medium.com/@bhumikaavula90/stop-building-dashboards-nobody-uses-why-most-analytics-deliverables-fail-and-how-to-design-for-b5d751a36ad3) | **风险确认,且给出分界线**:活下来的图都绑定一个**反复发生的决策仪式** |
| 这个生态位当前没被占 | 双方 §2 | Zeta Alpha 现状;近期学术动向 | [Zeta Alpha 已转向企业 RAG/搜索(客户 Festo/BASF/Deloitte)](https://www.zeta-alpha.com/);但 2026 年 5-6 月连出 [Eliot(交互式文献趋势探索)](https://arxiv.org/pdf/2605.27610)、[MIRAI(高影响力研究预测)](https://arxiv.org/pdf/2606.05443) 等学术工作 | **窗口开着但在变窄**:产品侧无人占位,学界正在逼近同一片区域 |

## 4. Refined picture

搜索后的收敛:KG-radar 的护城河**不在图、不在边、也不在 alert**——这三样分别被 Litmaps、scite、ResearchRabbit 各占了一角。它的独占组合是:**(a) 方法级+claim 级的图语义(PwC 之死刚把这层基础设施腾空)× (b) 位移作为主 payload(所有现存工具都只给静态切片或逐条通知)× (c) 有品味、可校准的 agent 持续策展(ORKG 证明了人工策展到不了这里)**。且 dashboard 失败研究给出了明确的生存法则:位移视图必须**绑定一个反复发生的决策仪式**(组会选精读/季度方向复盘/talk 备稿),而不是做一张"随时可看"的全景图——"随时可看"在行为上等于"从不看"。所以 refined 版的 v0.1 想象应当收窄为:**为一个具体决策仪式服务的位移 radar**,图是底层资产,仪式出口才是产品。相比 R1,我对"该不该存在"更有信心(需求证据+时机证据都变强了),对"以图为主容器"更没信心(形态问题升级为 L3 首要待决)。

## 5. Open questions that L2 cannot answer

1. **锚定哪个决策仪式起步**:组会精读选择 / 季度方向复盘 / talk 备稿,三者用户频次和痛感不同——需要 operator(本人即目标用户)拍板。
2. **位移 payload 的形态**:可视地图 / 强观点 briefing / 前后快照 diff / 可带进组会的问题清单——L3 的 scope 决策,可能决定整个产品的骨架。
3. **信任预算**:边错到什么程度用户弃用?第一个月里需要几次"地图说对了"才能建立依赖?这只有真用户(或 operator 自用)能回答。
4. **首发 topic 数**:8~15 是终态还是起点?v0.1 也许 3 个 topic 就够验证位移价值。
5. **单人版还是 lab 共享版起步**(L4 之前必须定,影响所有 scope)。

## 6. Three things I'd want a real user interview to ask

1. 回忆你最近一次**砍掉或新开一个研究方向**:当时你实际看了什么证据?如果当时有一张"该方向 90 天位移图",它会改变过程还是只是装饰?
2. 你现在感觉哪个 topic 上自己的理解**最过期**?为了补上它,你上次花了多少时间、用了什么工具、停在哪一步?
3. (给他看一张 mock 位移图)你愿意把这张图**原样放进你下周组会的 slide** 吗?不愿意的话,缺什么才敢放?
