# Forge v3(forge-lite)· P1 · Opus 4.8 Max(独立审阅)

**Phase**: 1（独立审接口新形状 · forge-lite · 无 web search · 无 SOTA）
**Reviewer**: Opus 4.8 Max
**X read**: 4 槽全一手（T012 hand-back R6+2 决议 / interface.py PITPriceProvider 契约 / provider.py 取价 SQL 核心 / PRD §7 + HANDBACK-LOG T012 条）

---

## §0 · 读到的标的 + K 摘要

**一手读取**:
- T012 hand-back:R6 复现（entry=100@04-27 → 04-30 修 90 → exit=110，单轴取整行误算 log(110/90)=+20% 而非执行价 log(110/100)=+9.5%）+ 2 决议项。
- `interface.py`:`get_adjusted_close(ticker, *, market, target_date, query_as_of, adjust="fwd") → AdjustedPricePoint|None`——**单一 `query_as_of`**。
- `provider.py` L49-54:病灶实现 = `SELECT trade_date, close_raw, adj_factor_fwd, adj_factor_back, source, as_of ... WHERE trade_date<=:target AND as_of<=:query_as_of ORDER BY trade_date DESC, as_of DESC, source ASC LIMIT 1`——**一条 SQL 取整行**（close_raw 和 factor 绑在同一 `as_of<=:query_as_of` 上）。
- PRD §7 已落 entry 价 PIT 语义决议（entry raw@entry as_of × factor@exit as_of）。

**K 摘要**:operator 已定选 A（执行时可见 · PIT 严格），要 forge 定**分离双轴的最干净接口形状**（三候选 a/b/c）+ 向后兼容 + OUT-10 边界。binding:守选 A / 最小冲击优先 / 不破已 ship M1 / 契约要能直接指导 T012 收尾 / 轻收尾。

---

## §1 · 现状摘要（按 Y 视角）

### Y1 · 契约正确性 / PIT 语义

**病灶精确定位（比 hand-back 描述更细）**:`get_adjusted_close` 的语义缺陷不在"用了 query_as_of"，而在**close_raw 与 factor 被同一条 SQL 的同一个 `as_of<=:query_as_of` 一起选中**。R6 的场景里,当 T012 为统一拆股复权基准把 entry 也用 exit_date 的 as_of 查时,拿到的不只是 exit 时点的 factor,**还有 exit 时点可见的 close_raw 修订版**。

**关键洞察:两轴本质不同**。
- **价格版本轴（close_raw 该按哪个 as_of 取）**:entry 价的经济语义 = "投资者 entry 当时能据以行动的价" → 该按 **entry as_of** 取（不含 entry 后修订）。
- **因子估值轴（adj_factor 该按哪个 as_of 取）**:复权因子的作用是把 entry 和 exit 拉到同一可比基准（消除期间拆股/分红）→ 该按 **exit as_of**（或统一 valuation 时点）取,让 entry/exit 用同一套 factor。

R5 之所以引入 R6,是因为它**对**（factor 该统一到 exit）但**误伤了 close_raw**（把 close_raw 也拖到了 exit as_of）。所以修法本质 = **让这两轴能独立指定 as_of**。

### Y2 · 器官边界 / OUT-10

- `PITPriceProvider`（`interface.py`）是 **009 自有契约**（T002 定 · 本 fork 可改）—— 改它**不违 OUT-10**。OUT-10 禁的是改 004 的 `PriceDataProvider.get_history` 签名。
- `CurrentStatePriceProvider`（T008 · 桥接 004）用 as_of=今天 的退化查询,**不涉及双轴回测语义** → 不受影响。
- **所以改 `get_adjusted_close` 加轴,是在 009 自有契约内动,边界干净**。真正要权衡的是"改签名"vs"调用层重组"的冲击面（见 §2）。

---

## §2 · First-take:三候选评分（K 点名要定的 a/b/c）

| 候选 | 形状 | 评 | 理由 |
|---|---|---|---|
| **(a) 加第三参数** | `get_adjusted_close(..., query_as_of, factor_as_of=None, ...)`：`query_as_of` 管 close_raw 版本轴,`factor_as_of` 管因子轴（默认 None → 退化 = query_as_of,向后兼容） | **✅ 倾向此** | 单一读入口不变（T012 一次调用拿齐 adjusted + provenance）· 向后兼容干净（默认 factor_as_of=query_as_of = 旧行为,T004/T005/T007 不破）· SQL 只需把 factor 的 as_of 拆出单独子查询。**最小签名增量 + 最小冲击** |
| **(b) 拆两个原子读** | `get_raw_close(ticker,*,target_date,as_of)` + `get_factor(ticker,*,target_date,as_of)`,调用层自算 adjusted | ⚠ 次选 | 语义最正交,但**破坏"单入口拿齐 provenance"** · T012 要自己拼 AdjustedPricePoint · 且新增两个公开方法 = 更大接口面 · 现有调用方全要改。冲击大于 (a) |
| **(c) 调用层重组,provider 签名不动** | T012 调 `get_adjusted_close` 两次:一次 entry as_of 拿 close_raw、一次 exit as_of 拿 factor,自算 | ❌ 技术不可行 | provider 返回的是**已算好的 adjusted_close**,不单独暴露"只要 close_raw 不要 factor"或"只要 factor"。用现签名两次调用各自拿到的都是各自 as_of 的 adjusted，**无法重组出 entry_raw × exit_factor**（除非从 AdjustedPricePoint 的 provenance 里反解 close_raw + factor_used 再自乘 —— 那是 hack,且依赖 provenance 字段语义,脆） |

**倾向 (a)**:一个可选第三参数 `factor_as_of`，默认退化即向后兼容，SQL 改动局部（factor 拆独立 as_of 子查询），T012 一次调用解 R6。**这是"解 R6 + 最小冲击 + 守 OUT-10 + 向后兼容"四项都最优的。**

**(c) 的诱惑要警惕**:hand-back 和 K 都把"调用层重组不改签名"列为最守 OUT-10 的选项，但我判它**技术不可行**——现契约不暴露 raw/factor 的独立取用，AdjustedPricePoint.provenance 虽有 close_raw+factor_used，但从两次不同 as_of 调用的结果里反解重组是脆 hack，不是干净契约。**改 009 自有契约（a）本就不违 OUT-10，不必为"不改签名"扭曲。**

---

## §3 · 我最不确定的 3 件事（留 Codex 独立审）

1. **(a) 的 SQL 实现:factor 拆独立 as_of 子查询后,tie-break 与 canonical 校验会不会破**？provider.py 现有 `ORDER BY trade_date DESC, as_of DESC, source ASC LIMIT 1` + canonical UTC 校验（R1-F3）是精心加固的。factor 单独按 factor_as_of 查时,要保证同样的 canonical + tie-break 纪律,且 **entry 命中的 trade_date 与 factor 命中的 trade_date 必须是同一天**（否则 factor 对错票）—— 这个约束怎么在 SQL/契约里钉死,我不确定。

2. **AdjustedPricePoint 的 provenance 语义要不要扩**？现在它有单一 hit_as_of。双轴后,一个 AdjustedPricePoint 里 close_raw 来自 entry as_of、factor 来自 factor_as_of —— provenance 该记**两个 as_of**（close_version_as_of + factor_as_of）才诚实,否则"as-of 可复现"（O6）在双轴下反而更模糊。这是不是要连带改 AdjustedPricePoint 结构,我不确定。

3. **(a) vs (b) 的长期演化**:若将来还要分离更多轴（如分红 vs 拆股 factor 各自 as_of）,(a) 的"加参数"会不会膨胀成参数地狱、(b) 的正交原子读反而更可扩？forge-lite 只解当下 R6,但契约选型有长期影响 —— 这个 tradeoff 我给不出定论,倾向"当下 (a) 够且最小,膨胀了再说",但留 Codex 判。

---

**P1 自评**:X 全一手（含 provider.py 病灶 SQL L49-54 精确定位）。核心判断——**(a) 加可选 `factor_as_of` 第三参数是四项最优**（解 R6 + 最小冲击 + 守 OUT-10 + 向后兼容）；(c) 调用层重组技术不可行（现契约不暴露 raw/factor 独立取用）；改 009 自有 PITPriceProvider 不违 OUT-10,不必为"不改签名"扭曲。§3 三个不确定点（factor 子查询的 tie-break/同日约束 / provenance 要不要记双 as_of / 长期演化）留 Codex 独立审。forge-lite:若 Codex 也收敛到 (a) → 直接进 synthesizer 定契约；若分歧 → 升级补 P2。字数约 1400。
