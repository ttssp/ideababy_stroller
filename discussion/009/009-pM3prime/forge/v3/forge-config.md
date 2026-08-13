---
forge_version: v3
created: 2026-08-13T04:56:45Z
convergence_mode: strong-converge
x_hash: d3b0a5bb7ff31f946365f393d5e13868
prefill_source: manual
fork_id: 009-pM3prime
trigger: 2026-08-12 五条实跑证据(提取器测量效度)· operator 起 forge
---

# Forge Config · 009-pM3prime · v3

**主题**:E1 普查的**测量仪器本身**能不能用 —— 前两轮审的是金标标注,这轮审的是产出信号的那台机器。

## X · 审阅标的

### 解析后的标的清单

**本仓(✅ 可达)**

1. `discussion/009/009-pM3prime/PREREG-census-scaleup.md`(类型:本仓库文件 · 650 行)
   - ★ **核心证据文档**。推荐读取范围:**全文**,重点 §1(效力实算)/ §2(41 是抽样产物)/ §6(实测成本 + 两个执行绕法)/ **§10 执行记录(五条发现的原始数据全在这里)**
2. `discussion/009/009-pM3prime/PRD.md`(类型:本仓库文件 · 506 行 · v0.9)
   - 推荐读取范围:§2 / §4-E1(含 block (p) 41 条盲标路 CLOSED)/ §6 停止条件与 E2 两 lane / §7 trial ledger 与「移动球门」判据 (f)
3. `discussion/009/009-pM3prime/forge/v2/stage-forge-009-pM3prime-v2.md`(类型:本仓库文件 · 396 行)
   - **前轮裁决,对本轮有约束力**。推荐读取范围:§Verdict / §Decision matrix / §v0.2 notes / §What this menu underweights
4. `discussion/009/handback/HANDBACK-LOG.md`(类型:本仓库文件 · 1419 行)
   - 推荐读取范围:**选读第 28 / 29 / 33 条**(不必通读)

**XenoDev-009 build repo(⚠ 外部 repo,Codex 沙箱可能 BLOCK —— 若 BLOCK 请在 §0 显式声明并改用下方 TEXT 块,不要假装读过)**

5. `/home/ys/codes/XenoDev-009/projects/004-pB/src/decision_ledger/extraction/census.py`(921 行 · 提取器本体)
   - 重点:模块级常量、`_default_deepseek_client_factory`、LLM 调用与失败处置路径、`usage` 的使用方式
6. `/home/ys/codes/XenoDev-009/projects/004-pB/src/decision_ledger/extraction/sampling.py`(90 行 · 分层抽样)
7. `/home/ys/codes/XenoDev-009/projects/004-pB/src/decision_ledger/extraction/gold_layer2.py`(Layer-2 门 · `criteria_met` 与 `_CORRECTNESS_GATE_AUTHORIZED_V0_1`)
8. `/home/ys/codes/XenoDev-009/specs/009-pM3prime/spec.md`(580 行 · 契约面)
9. `/home/ys/codes/XenoDev-009/specs/009-pM3prime/SLA.md`(150 行 · 门槛表)

### TEXT: 关键代码常量原文(沙箱 BLOCK 时的替代来源)

> 以下为 2026-08-13 从 XenoDev-009 工作副本 `rg` 出的**逐字原文**,非转述。

`src/decision_ledger/extraction/census.py`:

```python
_HORIZONS = (5, 20, 60)
_LLM_TEMPERATURE = 0.0
_EXTRACTION_TEMPLATE_VERSION = "extraction_v2"
_DEEPSEEK_BASE_URL = "https://api.deepseek.com"
_DEEPSEEK_MODEL = "deepseek-v4-flash"  # operator 指定(CLI --model 可覆盖)· DeepSeek 侧真模型 ID
_LLM_TIMEOUT_SEC = 60.0
_N_MAX = 12                 # 每 record 最多抽的信号条数(prompt 声明 + 代码截断兜底 · 长语料防输出爆预算)
_QUOTE_CHAR_LIMIT = 80      # 每条 quote 的字符上限(引文制:抄能定位信号的最短原文片段 · 别整段抄)
_TOKEN_FACTOR = 2           # 字符→token 保守系数(中文 1 字 ≈ 1-2 token · 取 2 保守)
_JSON_OVERHEAD = 512        # JSON 结构骨架 + 字段名 + 逗号引号的固定开销(token)
_QUOTE_HARD_MAX = _QUOTE_CHAR_LIMIT * 2  # 160 · 硬上限(fuzzy 层另有独立护栏 · 见 anchoring)
```

`src/decision_ledger/extraction/sampling.py`:

```python
OOS_WINDOW_START = "2025-12-01"   # 含
OOS_WINDOW_END = "2026-02-01"     # 不含(半开区间 [start, end))
_FORMS = ("article", "qa", "replay")
_MARKETS = ("US", "CN", "HK")
_HORIZONS = (5, 20, 60)
_N_PER_STRATUM = 40
```

**两条已核实的代码事实(2026-08-12 读码确认)**:

- `usage` / `completion_tokens` 只被用于**截断检查**,token 总量**从不累计**。
- API 返回的 `system_fingerprint` **代码从不读取**。
- `select_source_ids` 按 `sha256(seed_key + source_id)` 排序,`seed_key = f"{caliber_version}:{form}"` —— **抽样是确定性的**(这一点很重要:同参两跑抽到的 record 集合相同,差异全部来自 LLM 输出)。

## Y · 审阅视角

✅ **科学效度(测量工具)** —— 构念效度 / 可复现性 / 信度。第 3 条「同日 Jaccard 0.44」的正题;7 个内置视角都盖不住它,故 operator 自定义加入。
✅ **架构设计** —— fail-closed 契约、提取器与下游的耦合、不确定性该在哪一层被吸收。
✅ **工程纪律** —— 模型指纹缺失、语料身份不可验证、校准机制该长什么样。

> ⚠ operator **未选**「产品价值」。第 5 条(CN/HK STOP 需重审)仍在题内,请在**科学效度**视角下处理它 —— 即「单次读数能不能支撑一个 STOP 裁决」,而不是「CN/HK 市场值不值得做」。

## Z · 参照系

mode: **对标 SOTA**

建议检索方向(不限于此,双方各自决定):
- LLM 输出的**非确定性**:temperature=0 为何仍不可复现(batching / MoE routing / 浮点非结合性 / 后端异构)
- **LLM-as-annotator 的信度**:与人工标注一致性、多次采样的稳定性度量、self-consistency
- **信息抽取(IE)评测**:抽取集合的稳定性怎么量、集合型输出的 agreement 度量选择
- **失败案例**:把不稳定 LLM 抽取直接当作事实语料喂下游的已知翻车
- 把不确定性**纳入度量**而非消除的做法(多次采样投票 / 置信度加权 / 抽取分布而非点估计)

**外部材料叠加**:无(K 中未给外部链接)。

## W · 产出形态

✅ **verdict-only** —— ≤500 字裁决 + 理由,回答「还能不能往下走」
✅ **decision-list** —— 4 列矩阵(保留 / 调整 / 删除 / 新增),五条议题逐条落到动作
✅ **refactor-plan** —— 按模块分组的改造方案,直接可转成 XenoDev 侧 task

> operator **未选** next-PRD。若裁决要求改 PRD,在 decision-list 中指明改点即可,不产 PRD 草案。

## K · 用户判准

**为什么起这轮**

前两轮 forge(009-pM3prime v1/v2)审的是**金标标注**(Layer-2 是否成立);这一轮审的是更底层的东西 —— **产出信号的那台仪器本身**。2026-08-12 五条真跑证据显示:E1 普查提取器的输出**不可复现**,而下游一切(密度判据、分市场 go/STOP、E2 回测)都建立在它的**一次读数**上。

**五条议题(全部由实跑数据触发,非推演)**

1. **提取器身份不含模型指纹** —— `_DEEPSEEK_MODEL = "deepseek-v4-flash"` 是别名不是版本;API 返回的 `system_fingerprint` 代码从不读,token usage 也从不累计。⇒ 无法判定两批语料是否由同一模型产出。
2. **fail-closed 契约在规模下不可跑** —— 任一条 LLM 失败即整轮作废、零落库(这是 KG-40 的正当反应)。实测单条失败率 ⇒ n=1364 跑通概率 **≈1.5%**;两次实跑都失败(第一次 2:33:20 后 593/1364 崩)。**严格到不可跑,等于没有把关。**
3. **同日内容不稳定(最严重)** —— 同一天、同参数、同输入跑两次:总量 73 vs 71(差 3%),但按 `(source_id, ticker, direction)` 比对 **Jaccard 仅 0.44**;7 月那批 32 个元组在今天两跑中**都**出现的只有 50%。⇒「这批语料的信号集」**不是一个良定义的对象**。钉死模型指纹**解决不了这条**。
4. **提案上限顶满 / 疑似过度提取** —— `_N_MAX = 12` 几乎每次顶满,连 388 字符、零推荐语的财报摘要也提满 12 条。可能是第 3 条的成因之一。
5. **分市场读数的噪声大于总量噪声** —— 同日两跑总量只差 3%,而 **HK 0→4、CN 0→2**。⇒ PRD 里「CN/HK 真稀疏 → STOP」这条**产品级裁决是在单次读数上做的**,需重审。US go 方向不受影响(40/73/65 三次均 > 阈值 30)。

**我最在乎什么**

- 我要一份**可执行的裁决**,不是又一轮诊断。这条闭环还能不能往下走、往下走的第一步是什么。
- **核心 tradeoff:严格性 vs 可跑性**。放松 fail-closed 会踩 KG-40(静默失败伪装成真稀疏);不放松则规模上跑不出任何东西。**请正面处理这对矛盾,不要各说一半。**
- 我**接受**结果受一部分提取器误差影响,**前提是有定期校准机制**。我**不接受**不可复现的语料被当作事实往下游传。
- 「**推演 ≠ 真跑**」是本仓被反复打脸的失败模式(已 7 次)。本轮所有输入都是真跑出来的;请用同样标准要求你们的**输出** —— 每条建议都要能被**一条命令**验证。
- 承 v2 **反自欺条款**:「证据在场却被解释掉」是独立失败模式。若你要解释掉上面任何一条,须显式写明该解释的**可证伪点**。
- 承 v2 **门槛「数字 vs 形态」判据**:改门槛是改形态还是挪数字,要分清。

**我不关心 / 明确不要**

- 成本(DeepSeek 便宜,已实测)、代码风格、模型选型的商业面。
- **不要重开 41 条盲标路** —— v0.1 已 CLOSED(HANDBACK-LOG 决议 33),三前提全塌。那是关掉的门,不是本轮的题。
- 不要给我「再多做几个实验然后再说」当作唯一结论;若必须,请给出**有界**的实验清单 + 每条的判据。

**一个我自己也不确定的问题(请正面回答)**

如果第 3 条(同日不稳定)在架构上无解,那 009 这条「用 LLM 从散文里提取可回测信号」的路线本身,是不是应该改判?还是说存在一种把不稳定性**纳入**度量(而非消除)的做法?

## 收敛强度

✅ **strong-converge**

---

## Summary for reviewers

**审阅标的总数**: 9(本仓 4 ✅ · 外部 repo 5 ⚠ · 另附 TEXT 常量块作 BLOCK 兜底)
**视角维度**: 科学效度(测量工具) · 架构设计 · 工程纪律
**参照系**: 对标 SOTA —— LLM 非确定性 / LLM-as-annotator 信度 / IE 抽取稳定性 / 把不确定性纳入度量的做法
**预期产出**: verdict-only + decision-list + refactor-plan
**用户最在乎**: 要**可执行裁决**而非又一轮诊断。核心矛盾是**严格性 vs 可跑性** —— fail-closed 防住了 KG-40 的静默失败,却让 n=1364 的跑通概率只剩 1.5%。用户接受提取器带一部分误差,**前提是有定期校准机制**,但不接受不可复现的语料被当事实往下游传。所有建议须能被一条命令验证(「推演≠真跑」是本仓 7 次翻车的模式);要解释掉任何一条证据,须写出该解释的可证伪点。明确不要重开 41 条盲标路(已 CLOSED)。
**收敛模式**: strong-converge
