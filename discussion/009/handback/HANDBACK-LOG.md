---
doc_type: handback-decision-log
first_created: 2026-07-02T02:32:43Z
last_updated: 2026-07-04T00:00:00Z
total_decisions: 10
note: append-only;每条决议追加一段 ## entry;不删除 / 不修改既有 entry(既有 entry 的 Follow-up commits 字段随决议落地更新,非新增决议)
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

---

## 2026-07-03T09:19:52Z · 批量 · T003/T004/T005/T006/T007/T011(6 包 · feature/info)

**Reviewed at**: 2026-07-03T09:19:52Z
**Tags**: feature(全部)
**Severity**: medium(全部)
**6 约束自检**: ✅ all 6 PASS(consumer · 绝对路径)

**内容摘要**(M1 数据层 + M2 join 全套 clean ship · 各 §3 均"无需 IDS 决议动作"):
- T003(20260702T125820Z):M1 PIT 查询引擎 SqlitePITPriceProvider 双时间轴 ship
- T004(20260702T154536Z):M1 Tiingo(美股)价格源 ship
- T005(20260702T154812Z):M1 BaoStock(A股)源 + 港股 adapter 留位 ship
- T006(20260703T002635Z):M1 ingest CLI(P1 PPV 真路径 owner)ship
- T007(20260703T024038Z):M1 contract tests(spec §8 四条契约)ship
- T011(20260703T051452Z):M2 join 合约 resolve_signals ship + 2 carry-forward(留 open 事务→T016 须 commit/rollback;见 T012 §3)

**Operator decisions**:
- [x] 无操作(收悉 · practice-stats 入库)—— M1 数据层 5 task + M2 join 全 clean ship,无 spec/PRD 触发。
- carry-forward 记录:T011 的 open 事务契约 + 交易日历 known-gap(只跳周末不建节假日)留 T016/后续。

**Operator note**: M1(PIT 数据层 + 双源 + CLI + contract tests)整条 ship 完毕,M2 join 就位。
纯信息式,无需 IDS action。⚠ 注:这批包 frontmatter to_source_repo/source_repo 仍是 mac 路径
(KG-26 · gen-handback 产于 XenoDev mirror 我的修复之前)—— 待 XenoDev 侧 KG-27 session 同步 gen-handback 后消除。

**Follow-up commits**: pending(本 LOG)

---

## 2026-07-03T09:19:52Z · 009-pForge-20260703T034538Z(T010 · M2 alpha 建表 · F6 决议)

**Reviewed at**: 2026-07-03T09:19:52Z
**Related task**: T010(M2 analyst_alpha 两表 migration 0015)
**Tags**: feature
**Severity**: high(因 F6 待触发真回归须 T012 前决)
**6 约束自检**: ✅ all 6 PASS

**内容摘要**: alembic 0015 建 analyst_alpha_eval + analyst_alpha_rejections 两评估表(D-M2-2 ·
只新增不 alter 004 · OUT-10)。codex R1-R5 抓 7 finding,范围内 5 个(direction/horizon CHECK ·
FK→advisor_reports · rejections 幂等 · provenance FK→price_daily+完整性 · 结果列域约束)全修;
越界 2 个(F5→T012 责任 / F6→004 upsert)分流。26 迁移单测 + 540 全 004 套绿 + 真 alembic upgrade→0015。

**Operator decisions**:

### F6 [high · 加 FK 的次生真回归] → **采纳:改 004 upsert 为 ON CONFLICT DO UPDATE**
- **问题**: T010 给 alpha 两表加的复合 FK `(advisor_id,source_id,week_id)→advisor_reports`(无 ON DELETE
  = 默认 RESTRICT)会撞 004 `repository/advisor_repo.py:38` 的 `INSERT OR REPLACE`(upsert_weekly)。
  一旦有 alpha 子行,REPLACE 覆盖同周报告 = 先 DELETE 父行 → child FK RESTRICT → `FOREIGN KEY constraint failed`。
  现无触发(子行 T012+ 才写),但 **T012 起写子行后 upsert_weekly 会炸**(埋了地雷)。
- **决议**: 选 (a) 改 004 `upsert_weekly` 的 `INSERT OR REPLACE` → `ON CONFLICT DO UPDATE`(不删父行 · 最干净)。
  拒 (b) ON DELETE CASCADE(会静默删已算 alpha 样本 = 数据事故)。
- **落地**: 新开 **FU-task 改 004 repo 层**(改 004 已 ship 代码 · 归属明确为本 fork 授权的 M2 依赖修复)。
  **必须在 T012 起写子行前解决**。
- **F5**: 判定为 T012 责任(as-of look-ahead 防护 spec D-M2-4 明定 T012 运行时责任),不在 T010 · 见下 T012 条。

**Operator note**: T010 建表 clean。F6 采纳 ON CONFLICT(codex+仓库+我一致推荐),起 FU-task 改 004
upsert,T012 起写前落。

**Follow-up commits**: pending(FU-task 待起 · 本 LOG)

---

## 2026-07-03T09:19:52Z · 009-pForge-20260703T085623Z(T012 · M2 realized-return · BLOCKED · 2 决议)

**Reviewed at**: 2026-07-03T09:19:52Z
**Related task**: T012(M2 realized-return 引擎 · **BLOCKED · 不 merge · 待决议后收尾**)
**Tags**: prd-revision-trigger
**Severity**: high(review 未闭合 + 阻 M2 主链)
**6 约束自检**: ✅ all 6 PASS

**内容摘要**: T012 realized-return 引擎 compute_realized(signal,horizon)→RealizedResult。codex 6 轮权威
对抗审,R1-R5 修 5 个 correctness bug(陈旧价/精确命中/非有限价/log差值/拆股同基准 · 27 单测绿 ·
cov 94% · 587 全绿无回归 · 13 commit 留任务分支)。**R6 揭 spec-semantic 空白 → prd-revision-trigger**。

**Operator decisions**(2 个互相牵连的语义决策):

### 决议项 1(核心)· entry 价可见口径 → **采纳:选 A「执行时可见」(PIT 严格)**
- **问题**(codex R6 复现): R5 统一复权轴为 valuation_as_of=exit_date 后,provider 选整条 price_daily
  最新可见行(close_raw+adj_factor 一起)→ entry 价被 entry 后的 close_raw 修订污染。复现:entry=100@04-27,
  04-30 修为 90(非拆股数据改),exit=110 → 当前算 log(110/90)=+20% 而非执行价 log(110/100)=+9.5%。
  C16/D-M2-4 只定"双侧显式 as_of"(防价格 look-ahead),未明 raw close 修订可见性。
- **决议**: 选 **A「执行时可见」**——entry 价 = 信号执行当时可见的 close,不含 entry 后修订。语义最纯
  ("投资者当时能据以行动的价")。拒 B(接受 ex-post correction = 用了执行后信息 · 轻微 look-ahead)。

### 决议项 2(依赖项 1)· provider API 分离两轴 → **采纳:改 provider(走 IDS forge/FU)**
- **问题**: 选 A 的干净实现需**分离价格版本轴(entry as_of)与复权因子轴(exit as_of)**——entry raw close
  按 entry as_of 取、factor 按 exit as_of 取,自算 adjusted = entry_raw × exit_factor。
- **决议**: 改 M1 provider 加分离的 close-version-as_of / factor-valuation-as_of(或调用层重组)。
- **⚠ 归属**: provider 是 T003 已 ship 件(price/provider.py + interface.py),改其 API **违 spec OUT-10
  (不改已 ship 004/provider 签名)= 跨仓契约改**。按 CLAUDE.md 铁律「跨仓协议改 / 重大架构转向 → 必须回
  IDS forge」→ **不走 scope-inject,须起 forge(或至少 forge-lite 定 provider 新契约)**,不在 XenoDev 当场改。
- **✅ 已由 forge v3 定契约**(`discussion/009/forge/v3/stage-forge-009-v3.md` · forge-lite · 2026-07-03 ·
  P1 双方零分歧强收敛候选 (a)):选 `get_adjusted_close(..., factor_as_of=None)` 加可选第三参数分离双 as_of
  轴(判死 (c) 调用层重组 = 技术不可行/退化成 T012 私有约定;判 (b) 拆原子读 = 次选破坏单入口 provenance)。
  三细节定死:factor 锁同 hit_trade_date+source · AdjustedPricePoint 非破坏扩 factor_as_of · factor 缺失沿用
  None(结构化 outcome 降级 v0.2)。**XenoDev 授权改 009 自有 provider**(不碰 004 · 不违 OUT-10)。

**T012 收尾指示**(回流后 operator 在 XenoDev 做):选 A → 待 provider 契约经 forge 定后,起 FU-task
改 provider + 改 realized_return 重组两轴 + 补测 + REVIEW-LOG 收口 → merge 任务分支
`task/009-pForge-T012-realized`(13 commit 保全)。**在此之前 T012 保持 BLOCKED 不 merge。**

**关联**: T010 F6(ON CONFLICT upsert · T012 起写子行前落)+ T011 open 事务契约(T016 commit/rollback)。

**Operator note**: 选 A(PIT 严格 · alpha 数字要真防 look-ahead)+ 改 provider 走 forge(跨仓契约 · 违 OUT-10)。
T012 待 provider 新契约定后收尾。这触发一个 provider 契约 forge(比 scope-inject 重)。

**Follow-up commits**: ✅ provider forge v3 已定稿(`stage-forge-009-v3.md` · 2026-07-03)+ PRD §7 已同步指向新契约;
⏳ 剩:XenoDev provider FU-task(改 interface.py/provider.py/models.py + 6 测)+ T012 realized_return.py 双轴调用 → merge 解 BLOCKED
