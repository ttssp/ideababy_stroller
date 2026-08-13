# Forge v3 · 009-pM3prime · P1 · GPT55xHigh · 独立审阅(no search)

**Timestamp**: 2026-08-13T05:16:05Z  
**Searches used**: NONE in this round.  
**Visibility**: I did NOT read other reviewer's P1.  
**Reviewer stance**: 审阅人——评判已存在的测量仪器，不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了：① `PREREG-census-scaleup.md` 全文；② `PRD.md` 的 §4-E1（含块 (p)）、§6、§7、§8；③ forge v2 stage 的 Verdict、Decision matrix、v0.2 notes、underweights；④ `HANDBACK-LOG.md` 第 28/29/33 条；⑤ `census.py` 的常量、LLM 调用、三类失败、`usage`、invalid/rollback 路径；⑥ `sampling.py` 全文；⑦ `gold_layer2.py` 的授权常量及 `criteria_met/passed` 分离；⑧ XenoDev spec 的提取器、稳定性、trial-ledger 契约；⑨ `SLA.md` 全文。外部 repo 5–9 均可直接读取，**未走 TEXT 兜底**。
- 我跳过的 X 标的：无。`moderator-notes.md` 不存在。按硬约束未打开 `P1-Opus47Max.md`。控制材料另读 forge config、forge P1 template 与 `AGENTS.md`。
- 越界只读取证：`tests/contract/test_e1_citation_consistency.py` 与 `tests/integration/test_census_cli.py`，用于核对 C4 和 invalid rollback 的实际测试边界；前者的“同文同版同输出”只跑 `literal_ticker_proposer`，后者确认 invalid 时三张表（含 E1 trial 行）全回滚。
- **K（用户判准）摘要**：用户要“可执行裁决”，核心是“严格性 vs 可跑性”；接受有误差但须有定期校准，不接受不可复现语料被当事实。并要求“推演 ≠ 真跑”、每条后续建议可由一条命令验证；不得重开已 CLOSED 的 41 条盲标路，也不得把 CN/HK 的题偷换成市场价值判断。
- **阅读策略**：先把“抽样是否固定、测量是否固定、失败是否留痕、下游消费什么”四条链分开，再按科学效度、架构设计、工程纪律归位；本轮只形成 first-take，不作 SOTA 对标或详细改造方案。

## 1. 现状摘要（按 Y 视角组织）

### 科学效度（测量工具）

抽样端按 `sha256(seed_key:source_id)` 排序，同参两跑处理相同记录；输出端同日两跑 accepted 为 73/71，但 `(source_id,ticker,direction)` 的 Jaccard 为 0.44，7 月集合在同日两跑都出现的比例为 50%。总量差 3%，分市场却为 CN 0→2、HK 0→4；US 三次均高于 30。格式实验中 `_N_MAX=12` 几乎持续顶满，388 字、无方向推荐的财报摘要也产满候选。

现有密度、market go/STOP 与拟议 E2 都消费一次 accepted 集合作为点读数。PRD §7 同时要求“同文本同版本必须同输出”，但真 LLM 实跑与该要求不一致；当前契约测试只证明 literal proposer 的确定性。

### 架构设计

单 record 的 API、parse 或 truncation 失败先降级为 0 span 并累计三类 stats；`run_census` 发现任一增量后早停，将整轮判 `census_invalid` 并回滚信号、拒绝与 E1 trial 行。该结构阻止失败被解释为真稀疏；在 n=1364 时，K 给出的实测外推全过概率约 1.5%，跑 #1 在 593/1364 处失败并零落库。

下游 gate 对 Layer-2 已把 `criteria_met` 与 `passed` 分开，v0.1 correctness 授权恒假；但提取器到密度判据仍以单轮集合为接口。失败不落脏数据，也不留下可供下游消费的部分结果；同日集合不确定性尚未在密度或 market verdict 的数据形态中出现。

### 工程纪律

`extractor_variant` 记录 proposer 类型与 prompt 模板，模型名为可静默变化的别名；API 返回的 `system_fingerprint/service_tier` 未读取，`usage` 仅用于单次截断判断而不累计。trial ledger 记录 source-id 清单，但没有语料内容身份；invalid 又回滚 E1 trial 行，因此失败尝试不进入该账。

SLA/C4 把温度 0、版本化、同文同版同输出写成 Hard，现有真跑已提供反例。仓内已有阈值预注册、typed failure、原子回滚与真实运行日志；尚未见把模型指纹、语料哈希、重复读数信度和周期校准结果共同绑定成一次测量身份的持久化记录。

## 2. First-take 评分（按 Y 视角）

| Y 维度 | 倾向 | 理由（引用 §1 现状） |
|---|---|---|
| 科学效度（测量工具） | **refactor** | §1 显示抽样固定但输出集合非良定义；保留 US 方向性证据，停止把单次集合及 CN/HK 单次 0 当稳定事实。测量对象需从一次点读数改判。 |
| 架构设计 | **refactor** | §1 的 fail-closed 目标应 keep，但“任一 record 失败→整轮无产物”在规模下把严格性变成不可运行；不确定性需在提取器—判据边界被显式承载。 |
| 工程纪律 | **new** | §1 所列指纹、语料身份、失败 trial 与真 LLM 一致性证据均缺；现有 C4 测试没有覆盖被宣称的真测量路径，需新增可审计校准面。 |

## 3. 我现在最不确定的 3 件事

1. 集合型信息抽取应以哪种信度指标和最少重复次数形成可判门槛，才能同时覆盖总量稳定与元素稳定，而非只优化 Jaccard 数字。
2. 在不让单条失败伪装成稀疏的前提下，什么 fail-closed 单元（record、batch、run 或带覆盖率的 ledger）既保持 KG-40，又能在 1364 条规模实际完成。
3. `_N_MAX` 顶满在多大程度上造成组合漂移；若抑制过度提取后同日不稳定仍高，路线应改为“分布式测量”还是判定散文→信号抽取本身不适合作为 E2 输入。
