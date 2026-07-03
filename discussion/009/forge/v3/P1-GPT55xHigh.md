# Forge v3 · 009 · P1 · GPT55xHigh · 独立审阅(no search)

**Timestamp**: 2026-07-03T09:51:21Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了:
  - `discussion/009/forge/v3/forge-config.md` → 读 X/Y/Z/W/K、forge-lite scope、三候选 a/b/c。
  - `discussion/009/handback/20260703T085623Z-009-pForge-20260703T085623Z.md` → 读 T012 R6 复现与两项 IDS 决议。
  - `/home/ys/codes/XenoDev/projects/004-pB/src/decision_ledger/price/interface.py` → 读现 `PITPriceProvider.get_adjusted_close(... query_as_of, adjust)` 契约。
  - `/home/ys/codes/XenoDev/projects/004-pB/src/decision_ledger/price/provider.py` → 读 `_SELECT_PRICE_SQL` 与 `AdjustedPricePoint` 构造路径。
  - `discussion/009/009-pForge/PRD.md` §7 + `discussion/009/handback/HANDBACK-LOG.md` T012 条 → 读 M1 契约与 operator 决议溯源。
  - `discussion/009/forge/v3/PROTOCOL.md` §P1 template。
- 我跳过的:无。XenoDev 标的可读；我未读取 `discussion/009/forge/v3/P1-Opus47Max.md` 正文。
- **K(用户判准)摘要**: operator 已定 A「执行时可见」:entry raw close 按 entry as_of 取,不含 entry 后修订；factor 按 exit as_of 取；`adjusted = entry_raw(@entry) × factor(@exit)`。本轮只定双轴接口形状,不重议语义。
- **我的阅读策略**: 沿 R6 的污染路径追 SQL 和返回结构:当前 `query_as_of` 同时选 close_raw 版本和 factor 版本。评分只看四点:是否解 R6、是否保 T004/T005/T007 旧调用、是否守 OUT-10 不碰 004 `PriceDataProvider`、双 as_of provenance 是否能复现。

## 1. 现状摘要(按 Y 视角组织)

### 视角 A · 契约正确性 / PIT 语义

现接口把 `target_date` 与 `query_as_of` 称为双时间轴。实现 SQL 是 `trade_date<=target AND as_of<=query_as_of ORDER BY trade_date DESC, as_of DESC, source ASC LIMIT 1`,一次命中一整行,再用同一行的 `close_raw × adj_factor_*` 生成 `adjusted_close`。返回结构带 `hit_trade_date / hit_as_of / source / close_raw / factor_used`,但 `hit_as_of` 目前只能表示整行 as_of。

T012 的 realized-return 语义现在需要三层信息:entry 的价格发生日、entry 执行时可见的 raw close 版本、exit 估值时可见的 factor 版本。PRD §7 已把这写成「价格版本轴 ≠ 复权因子轴」,T012 在 provider 新契约前保持 BLOCKED。

### 视角 B · 器官边界 / OUT-10

`PITPriceProvider` 是 009 M1 PIT 层的自有契约,文档明确与 004 `PriceDataProvider` 并存,并且 `CurrentStatePriceProvider` 只是 T008 桥接。OUT-10 的硬边界是不改 004 已 ship 表/签名；在 009 自有 `interface.py/provider.py` 内扩契约,只要旧调用退化为旧语义,边界仍可控。

## 2. 三候选 first-take 评分

| 候选 | 解 R6 | 冲击面/兼容 | OUT-10 边界 | provenance | first-take |
|---|---:|---:|---:|---:|---|
| (a) `get_adjusted_close(..., query_as_of, factor_as_of=None)` | 5/5 | 4/5 | 4/5 | 4/5 | **倾向选**。`query_as_of` 明确管 close_raw 版本轴,`factor_as_of` 管因子轴；默认 `None -> query_as_of` 可保 T004/T005/T007。实现可在 009 provider 内做两次 PIT 选择,不碰 004。需要把 `AdjustedPricePoint` provenance 扩成至少 `price_as_of/hit_as_of` + `factor_as_of`。 |
| (b) `get_raw_close(as_of)` + `get_factor(as_of)` | 5/5 | 2/5 | 3/5 | 5/5 | 语义最原子,但把同一 hit_trade_date、source、因子缺失、adjust 校验等 invariant 分散给调用层。对 forge-lite/T012 收尾偏重,也更容易让未来调用方各算各的。 |
| (c) 现签名两次调用后调用层重组 | 3/5 | 5/5 | 5/5 | 2/5 | 窄场景可行:第一次取 `close_raw@entry`,第二次取 `factor_used@exit`,再相乘。但它依赖结构化返回字段被当作原子 API 使用,且要调用层自行检查两次 `hit_trade_date/source` 一致；若后来 as_of 下命中不同 source 或补录出不同 hit row,污染会从 provider 内部不变量变成 T012 私有约定。 |

我的结论:选 (a)。它不是最少代码,但在「最干净接口形状」上最好:双轴显式、旧调用可退化、实现边界仍在 009 PIT provider,并把最终 adjusted 点的双 as_of provenance 写回契约。可进 synthesizer 定契约；我没有看到需要补 P2 SOTA 的设计分歧。

## 3. 我现在最不确定的 3 件事

1. factor 查询是否必须锁定 raw close 命中行的同一 `source`。我倾向必须锁,否则跨源 raw/factor 混算会产生新 silent wrong。
2. `AdjustedPricePoint.hit_as_of` 是保留为 close 行 as_of 并新增 `factor_as_of`,还是破坏性改名为 `price_as_of`。兼容性上前者更稳。
3. 当 `factor_as_of < query_as_of` 或 factor 行缺失但 raw close 存在时,返回 `None` 还是结构化 data-quality outcome。现 provider 只有 `None`,T012 可能需要更细分,但这也可能超出本次最小契约。
