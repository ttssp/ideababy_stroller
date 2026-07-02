---
doc_type: handback-decision-log
first_created: 2026-07-02T02:32:43Z
last_updated: 2026-07-02T02:32:43Z
total_decisions: 2
note: append-only;每条决议追加一段 ## entry;不删除 / 不修改既有 entry
---

# HANDBACK-LOG · discussion 009

per `framework/SHARED-CONTRACT.md` §6.4,本文件是 operator 在 IDS 端对 XenoDev hand-back 包的决议日志。append-only。

## 2026-07-02T02:32:43Z · 009-pForge-20260701T161131Z

**Reviewed at**: 2026-07-02T02:32:43Z
**Related task**: T001(M1.1 PIT 价格层地基)
**Tags**: feature
**Severity**: low
**6 约束自检**: ✅ all 6 PASS(consumer mode · 绝对路径)
**verdict-evidence 预检**: n/a(无 ids_verdict_evidence 块)

**内容摘要**: 004 alembic 迁移 0014 建 price_daily + ticker_status 两张 bitemporal 表
(as_of/CHECK/PK 含 source + 6 触发器强制 append-only);18 单测绿 + 真 DB 验证;
codex adversarial-review R3 approve(0 findings)。§2/§3 为占位("待补 · operator 未传
--section2/3")。

**Operator decisions**:
- [x] 无操作(收悉,作为 practice-stats 入库)—— T001 是 M1 地基 ship 汇报,无 spec/PRD 触发,纯信息式。

**Operator note**: T001 干净 ship(codex 0 finding + 真 DB)。§2/§3 空是 gen-handback 未传
section flag 所致,非内容缺失。无需 IDS action。

**Follow-up commits**: pending(本 LOG 提交)

---

## 2026-07-02T02:32:43Z · 009-pForge-20260702T005910Z

**Reviewed at**: 2026-07-02T02:32:43Z
**Related task**: T002(M1 PIT 层接口契约 · interface-before-impl)
**Tags**: feature, prd-revision-trigger
**Severity**: medium
**6 约束自检**: ✅ all 6 PASS(consumer mode · 绝对路径)
**verdict-evidence 预检**: n/a(无 ids_verdict_evidence 块)

**内容摘要**: T002 交付 `decision_ledger.price` 包(PricePoint/TickerStatus/StatusKind +
PITPriceProvider Protocol · 双时间轴 · 全 keyword-only · market+query_as_of 必填);
codex adv-review R3 approve(0 findings · 3 轮);15 单测绿;守 OUT-10(不改 004
PriceDataProvider 签名)。附 2 条 prd-revision-trigger(codex R1-F2/F3 暴露)。

**Operator decisions**(2 条 spec 修订触发逐条决议):

### 触发 #1(codex T002-R1-F2 · [high])· PIT 取价返回类型 → **采纳:改结构化返回**
- **决议**: 接受 codex 建议。`get_adjusted_close` 返回类型从标量 `float | None` 改为**结构化**
  (含 adjusted_close + 命中行 provenance:hit_trade_date / hit_as_of / source / close_raw /
  factor_used)。可保留 float convenience 建于结构化接口之上。
- **理由**: 标量丢失 as-of 可复现所需的命中行溯源;`None` 无法区分 无价/退市/因子缺失。
  与 spec O6「M2 alpha as-of 可复现」直接冲突(已核 spec O6/D-M2-4/P2 属实)。
- **落地**(pending):
  1. **IDS PRD** `discussion/009/009-pForge/PRD.md` §7 契约措辞(L67 `(ticker, as-of date) → 复权收盘价`)
     补结构化返回类型说明 —— IDS 是 source of truth。
  2. **XenoDev spec** `specs/009-pForge/spec.md` D-M1-2 / O1 / P1 签名契约同步改(跨仓 · XenoDev 侧改)。
  3. 影响 T003 查询引擎 + T012 M2 realized-return:按结构化返回实装。**宜在 T003 起跑前定**(已定)。

### 触发 #2(codex T002-R1-F3 · [medium])· PricePoint close-only vs 004 PriceBar OHLCV → **搁置(park · 标 open)**
- **决议**: 暂不当场定。标 open-question,等后续 forge 或 operator 想清楚再定。
- **理由**: 二选一(A 扩 schema 存 OHLCV+volume / B 收窄 C7 为 close-only)都有真实代价,
  operator 选先不锁。alpha 头(M2)只需 close,不阻 M1→M2 主线。
- **⚠ 已知风险(记录在案)**: T003 实装 `CurrentStatePriceProvider` 时**必然撞到**这条
  (它必须 satisfy 004 `PriceDataProvider.get_history -> PriceBar(OHLCV+volume)`)。
  搁置 = T003 起跑即卡。**T003 起跑前须先回来定 #2**(或 T003 先只做 M2 直取路径、
  delay 004 adapter)。此风险随 T003 排期显性化。

**Operator note**: #1 采纳结构化返回(as-of 可复现是硬需求);#2 搁置——alpha 只需 close,
先不为 OHLCV 卡住,但明确记 T003 会撞、起跑前须定。另 XenoDev 记了 KG-30(red-green log
mirror 子树 gitignore 挡)+ KG-29 已解追认 → 连同 KG-26/27/28 攒批回 `/expert-forge 006`。

**Follow-up commits**: pending(PRD §7 结构化返回 edit + 本 LOG 提交)
