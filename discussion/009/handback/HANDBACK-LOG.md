---
doc_type: handback-decision-log
first_created: 2026-07-02T02:32:43Z
last_updated: 2026-08-11T15:42:50Z
total_decisions: 32
note: append-only;每条决议追加一段 ## entry;不删除 / 不修改既有 entry(既有 entry 的 Follow-up commits 字段随决议落地更新,非新增决议)。2026-07-05 F6 条撤销 2026-07-03 batch-T010 的 F6 采纳决议(前提证伪),撤销以新增 entry 记录,不改原 entry
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
✅ **已收尾**(见下 2026-07-05 T012 收尾条 · handback `20260703T170209Z`):XenoDev FU-task shipped 双轴契约 +
T012 realized_return 双轴调用 · merge `feat/009-spec` · **T012 BLOCKED 解除**。

## 2026-07-05 · 009-pForge-20260703T170209Z(T012 收尾 · BLOCKED 解除 · verdict 实装订正)

**Reviewed at**: 2026-07-05T00:00:00Z
**Tags**: spec-gap-fix,feature
**Severity**: medium
**6 约束自检**: ✅ all 6 PASS(consumer 模式 · validator 自动)
**Related task**: T012(M2 realized-return · 双 as_of 轴收尾)

**内容摘要**: XenoDev 按 forge v3 verdict 实装候选 (a) 双 as_of 轴 —— `get_adjusted_close` 加 `factor_as_of`,
factor 锁 close 命中行同 trade_date+同 source。**R6 复现闭合**:entry 后同 trade_date 的 close_raw 修订
(04-30→90)不再拉进 entry basis → **+9.5% 非 +20%**。4 文件改(interface/provider/models/realized_return ·
全 009 fork 内)· 6 双轴验收测 + 2 R7 回归测 · **595 全套绿无回归** · provider cov 98%/realized 94% · ruff clean ·
merge `feat/009-spec` → **T012 BLOCKED 解除**。reviewed-by=codex@2026-07-04(R7→R8 approve · 权威非 fallback)。

**⚠ verdict 实装订正(codex R7 抓 1 high)**: forge v3 stage §细节1 原描述的**两阶段两次独立 SELECT**,
在 SQLite autocommit 下**跨两个快照** → 并发 ingest 可拼「旧 close_raw + 新 factor」= silent-wrong(退化路径
也破原子性)。**shipped 收紧为单语句 CTE**(`_SELECT_DUAL_AXIS_SQL` · SQLite 单语句 = 单一致快照原子读)+
2 回归测(并发等价 + 结构 mutation-killer · 实证 kill 掉 two-SELECT)。**契约语义(factor 锁同源同天 + 双
as_of provenance)完全不变**,只是把「两次 SQL / 单 SQL self-join 等价」的实现选择收紧为「必须单语句原子读」。

**Operator decisions**:
- [x] 修 PRD §"7 M1 契约" —— §细节① 加注 shipped 单 CTE(非 two-SELECT)+ T012 收尾状态改「已 shipped · BLOCKED 解除」
- [x] 修 forge stage `stage-forge-009-v3.md` §细节1 —— 加「实装订正」note(two-SELECT → 单 CTE · 原子性)
- [ ] 修 SHARED-CONTRACT(无 · 非协议层)
- [ ] 无操作

**Operator note**: T012 收尾干净 · BLOCKED 解除。codex R7 的原子性发现是 forge-lite(无 P3 对抗)+ strong-converge
回声室的实证盲区 —— 恰好命中 stage doc §"What this menu underweights" 已预警的「两阶段之间未对抗验证」。
契约语义未变,实装比 verdict 更严。**forge verdict 与 shipped 实现的差异已双向回写(PRD + stage doc)保留审计。**

**Follow-up commits**: pending(本 LOG + PRD §7 + stage doc 订正 · 同一 IDS commit)

## 2026-07-05 · 009-pForge-20260704T234247Z(F6 前提证伪 · 关闭 not-a-bug · 撤销 batch-6 F6 采纳)

**Reviewed at**: 2026-07-05T00:00:00Z
**Tags**: prd-revision-trigger
**Severity**: medium
**6 约束自检**: ✅ all 6 PASS(consumer 模式 · validator 自动)
**Related task**: F6(004 upsert INSERT OR REPLACE vs 0015 复合 FK)

**内容摘要**: F6 **前提实证证伪 · 建议关闭 not-a-bug · 不 ship**。XenoDev 起 F6 后按 plan-mode 核真 schema +
写 TDD 复现测,**前提站不住**:
- **CASE B(同键 re-upsert · 即 T010-F6 说的复现路径 · 常见)**:有 alpha 子行时旧 `INSERT OR REPLACE` 同 PK →
  **成功不炸 FK**。SQLite 对同 PK 的 REPLACE **不 orphan 子行**(子行 FK 目标 PK 值不变),非天真 DELETE+INSERT
  跨 FK。4 个 F6 复现测跑**未改的旧 `advisor_repo.py`** → **全绿 = bug 不复现**。
- **CASE A(advisor_id 跨 fetch 变 · 撞 (week_id,source_id) UNIQUE · 罕见)**:旧代码真炸,但**无简单 ON CONFLICT
  能修**(本质是 re-parent 子行 = 数据迁移,归 `rebind_source_id_for_advisor_week`,不归 `upsert_weekly`)。
- **决定性旁证**:`domain/advisor.py:27` v0.1 只有一个 advisor + `source_id=advisor_id` → **CASE A 在 v0.1 根本
  不发生** → F6 连 edge 都不存在。

**⚠ 撤销先前决议**: 本条**撤销 2026-07-03 batch T010 条(`20260703T034538Z`)的 F6 决议**「采纳 · 改 004
`upsert_weekly` INSERT OR REPLACE → ON CONFLICT DO UPDATE」。原决议基于 codex 理论推演(REPLACE=DELETE+INSERT),
**未算 SQLite 同 PK 实际行为** → 证伪。**不 ship ON CONFLICT no-op**(常见路径无 bug 可修 · 对真 edge 无效 ·
装上 = 给「FK 风险已处理」假信心)。

**Operator decisions**:
- [ ] 修 PRD(无 · 见 note:CASE A 作 v0.2 known-edge · 本轮不写 PRD)
- [ ] 修 SHARED-CONTRACT(无)
- [x] 修 XenoDev spec(信息式)—— F6 关闭为 not-a-bug · CASE A(多 advisor re-parent)转 v0.2 known-edge 追踪
      (归 rebind 路径 · 非 upsert_weekly · v0.1 不触发)
- [x] 收悉入库(practice-stats:FU-task 先验证前提再动手 · 杀掉幻影 bug · 省一次无效 ship)

**Operator note**: F6 是幻影 bug —— 好的 dogfood 结果:FU-task 没盲目实装,先做实前提就证伪了。诚实记录:
IDS 侧原 handback-review F6 采纳决议 + 我写的 FU 指令都基于错误前提。**T016 不受阻**(v0.1 常见路径 upsert 本就不炸)。
交付:worktree `aeff2a8` 保留 · 只提交 4 证伪测(对未改代码全绿 = 证据)· `advisor_repo.py` 一字未改 · 未 merge。

**Follow-up commits**: pending(本 LOG · 同一 IDS commit)· CASE A v0.2 known-edge 追踪待 XenoDev spec 侧记(信息式)

## 2026-07-06 · 009-pForge-20260705T025527Z(T013 · M2 alpha 统计聚合 · clean · 双 Z drift 回写 PRD)

**Reviewed at**: 2026-07-06T00:00:00Z
**Tags**: feature,drift
**Severity**: medium
**6 约束自检**: ✅ all 6 PASS(consumer 模式 · validator 自动)
**Related task**: T013(M2 alpha 头统计聚合层 · 三件套)

**内容摘要**: T013 = 把 T012 per-signal RealizedResult 逐 horizon 聚合成分析师三件套(Hit Ratio + 平均超额 +
Z 显著性)。新增 `alpha/metrics.py`(compute_triplet)· 全 009 fork 内 · 不违 OUT-10。**615 全绿无回归** ·
metrics.py cov 100%(68 stmts)· ruff clean · 6 类 mutation 全 kill · codex **6 轮单调收敛**(每轮真
silent-wrong-number:generator 双遍历耗尽→n=0 静默错数 / 畸形 COMPUTED 行污染 / hit 未绑 excess 符号 /
重复样本放大 n→z 夸大 / 去重覆盖不全)→ R6 approve 0 material findings。

**drift 决策(operator 2026-07-05 授权 · 已在 hand-back §2 记全)**: task body 字面 z_score 单值 → 扩为
**z_hit(二项 Z vs 0.5)+ z_excess(单样本 Z · ddof=1)**。理由:O6「Hit Ratio + 平均超额 + Z 显著性」两量
各配 Z 才完整覆盖「命中率显著」与「超额显著」两独立命题 · 诚实扩展非越界。逐 horizon 只出现行(报告层补齐是 T016)。

**Operator decisions**:
- [x] 修 PRD §"7 M2 alpha 头" —— 三件套 Z 显著性明确为双 Z(z_hit + z_excess)· 固化为 PRD 级契约(非仅 build 授权)
- [ ] 修 SHARED-CONTRACT(无 · 非协议层)
- [x] 收悉入库(practice-stats:codex 6 轮单调收敛 · 每轮实质 silent-wrong-number)

**Operator note**: clean 交付 · T014 已解锁。双 Z drift 回写 PRD 固化。

**Follow-up commits**: pending(本 LOG + PRD §7 双 Z · 同一 IDS commit)

## 2026-07-06 · 009-pForge-20260705T102002Z(T014 · M2 防过拟合 · clean · 价值锚 · walk-forward 参数回写 PRD)

**Reviewed at**: 2026-07-06T00:00:00Z
**Tags**: feature,drift
**Severity**: medium
**6 约束自检**: ✅ all 6 PASS(consumer 模式 · validator 自动)
**Related task**: T014(M2 alpha 头防过拟合层 · 投资闭环第一个价值锚 · risks M2-R1)

**内容摘要**: T014 = 完整 Bailey & López de Prado 防过拟合层。新增 `alpha/deflate.py`(deflate)· 全 009 fork
内 · 不违 OUT-10。DSR 概率口径[0,1](skew/kurt 样本矩 + SR0 期望最大 Sharpe · N=trials·Euler-γ·Acklam Z⁻¹)+
PBO 走 CSCV + walk-forward/OOS(真建滚动窗口)· 正态 CDF/PPF 纯 `math.erf` 无 scipy(对齐 metrics/realized_return
惯例)。**656 全绿无回归** · cov 97%(229 stmts)· ruff clean · mutation 全 kill · codex **9 轮单调收敛**(PBO
门禁/CSCV 丢行/trials 崩/重复样本 DSR 放大/generator 物化/非 COMPUTED 反向校验/CSCV 零方差 fold/walk-forward
未实装泄漏)→ R9 approve 0 findings。教训:sibling 聚合层应主动 port T013 已修防线(多为 T013-parity)。

**drift 决策(operator 2026-07-05 · 3 项 · 已在 hand-back §2 记全)**: ① results=list[RealizedResult](取 .excess
回报序列 · TripletMetrics 不携序列不能喂 DSR);② 完整 Bailey-LdP(非简化 · skew/kurt+SR0+CSCV);③ walk-forward
**本层真建窗口**(非 pre-split 契约 · 非 defer · task 明写 T014 建):train 18月/test 3月/step 3月 + embargo 5TD ·
DSR 只在 OOS 算。**判不出 = 达标非失败**(O9/C12:trials<20 / n<2 / std=0 / 无 OOS 窗 → insufficient_sample)。

**Operator decisions**:
- [x] 修 PRD §"7 M2 alpha 头 · 防过拟合统计纪律" —— walk-forward 窗口参数(train18/test3/step3+embargo5TD)+ DSR 只在 OOS + insufficient_sample 语义 · 固化 PRD 级契约
- [ ] 修 SHARED-CONTRACT(无)
- [x] 收悉入库(practice-stats:codex 9 轮单调收敛 · T013-parity 教训)

**Operator note**: 价值锚地基已铺 · T015 已解锁。**M2-R1 提示**:v0.1 单分析师历史可能不足建多 walk-forward 窗 →
deflate 诚实标 insufficient_sample(O9/C12 达标非失败)· 若真判不出触发 OQ-2 重估(prd-revision-trigger)· 不静默给数。

**Follow-up commits**: pending(本 LOG + PRD §7 walk-forward 参数 · 同一 IDS commit)

## 2026-07-06 · 009-pForge-20260706T040059Z(T015 · alpha 上台 · 能力层稳但揭 O8 下游架构缺口 · 起 forge · 不 merge)

**Reviewed at**: 2026-07-06T00:00:00Z
**Tags**: prd-revision-trigger,drift
**Severity**: high
**6 约束自检**: ✅ all 6 PASS(consumer 模式 · validator 自动)
**Related task**: T015(M2 alpha 头「上台」层 · AlphaLane StrategyModule · D-M2-1/O8)

**内容摘要**: T015 = 把 T013 三件套包成新 StrategyModule lane,经 004 registry get_all() 平权进 conflict_reports
(O8)。新增 `strategy/alpha_lane.py`(AlphaLane + AlphaResultProvider Protocol + Mock)· 全 009 fork 内 · 不违
OUT-10。**能力层已稳**(28 测/100% cov · 684 全绿无回归 · ruff clean · mutation 全 kill)· **但 codex 3 轮
adversarial 逐层钻出 T015 spec 没预见的下游集成架构缺口** → operator 决切回 IDS 起 forge · **未 merge**(下游
澄清前 O8 不算真达成)· worktree + 8-commit 审计链保留。**reviewed-by 未标 approve**(R1-R3 全 needs-attention)。

**已在 XenoDev 修完(不越界 · alpha_lane.py 内部)**:
- R1-F1 [high] direction 系统性反向 —— 上游 `realized_return.py:231` excess 已按信号方向 signed,mean_excess
  符号不含当前多空方向 → 改产 NO_VIEW 质量旁证(非方向票)。
- R1-F3 TripletMetrics 矛盾值静默信任 → 加 `_metrics_inconsistency` 自洽校验 fail-closed。
- R2-F1 [high] 不能借 Direction.NEUTRAL(004 NEUTRAL = 中性持仓观点 · 会把显著+/−/真中性塌缩成同一高置信
  NEUTRAL)→ 改 `direction=NO_VIEW · confidence=0.0 · is_directional=False · signal_kind="alpha_quality_evidence"` ·
  强度移到 `inputs_used["evidence_strength"]`。
- R2-F2 + R3-F3 provider 异常分层 —— 可恢复(OSError/TimeoutError/ValueError)降级 NO_VIEW · 编程错
  (AttributeError/TypeError)fail-loud 重抛 + error_type 结构化可观测。

**⚠ 切回 IDS 的 2 个架构缺口(prd-revision-trigger 核心 · 均已核 004 真代码铁证)**:
- **R3-F1 [high · silent-wrong]**: AlphaLane 有效结果全是 `no_view:confidence=0.0`(非方向证据必然),强度只在
  `evidence_strength`。但 `conflict_report_assembler.py:159-164` 的 signals_hash 只 hash `{direction}:{confidence_bucket}`
  → 强/弱/error/no-provider alpha 全 hash 成 `analyst_alpha=no_view:low` → **缓存键相同 → 复用旧
  divergence_root_cause**(用户看到新 evidence_strength 但报告根因是旧的 = silent-wrong)。修需改 assembler
  缓存键语义(纳入 reason/signal_kind/is_directional/evidence_strength/z_excess,或结构化输入前禁缓存)· **assembler = spine · 在 T015 file_domain 外**。
- **R3-F2 [medium]**: O8 要 analyst_alpha 平权进 report.signals,assemble 层确实达成(4 路),但用户可见路径
  **两处硬编码 3 路**:`telegram/conflict_narrative.py:54` `signals[:3]` + `ui/router_conflicts.py:169`
  `first_three = signals[:3]` → 第四路在 Telegram+UI **完全丢失**。O8 测只断 assemble 覆盖不到渲染层。修需改
  双渲染为 N 路 / 显式区分方向票 vs 非方向 evidence · **UI 层 · 在 T015 file_domain 外 · 且「非方向 evidence
  怎么展示」是产品决策**。

**为什么切回 IDS**:R3-F1/F2 不是 alpha_lane.py 内部 bug,是 D-M2-1 的 O8 定义与 004 实际下游架构之间的缺口。
继续 XenoDev 硬修会把 T015 从「单文件 lane」膨胀成「改 assembler 缓存 + 双渲染 + 定义非方向 evidence 展示语义」
的跨 spine 改动 —— 越 file_domain + 可能牵动其他 task + 「非方向 evidence 怎么承载/展示」是需要 forge 的产品/架构
决策(V4 失败模式:静默扩范围绕治理)。

**Operator decisions**:
- [x] 起 forge 决 O8 下游集成(见下 Operator note · 非 scope-inject · 这是产品+架构决策 · 双模型对抗审)
- [x] 修 PRD §"7 M2 alpha 头 · lane 条" —— 加 O8 下游集成待 forge 澄清指针 + alpha=NO_VIEW 非方向 evidence 定性 + alpha_lane 未 merge 状态
- [ ] 修 SHARED-CONTRACT(无)
- [x] 修 XenoDev spec(信息式 · forge 结论后)—— 待 forge 定 O8 下游语义后回 XenoDev 起下游集成 task(拆新或并入 T016)
- [x] 收悉入库(practice-stats:codex 3 轮 adversarial 从「单文件 lane bug」逐层钻到「spec↔下游架构缺口」· 正确切回不硬修)

**Operator note**: 起 **forge**(scope preview 已定 X)决三件事 —— (a)ConflictReport 是否扩「非方向 evidence」
一等公民 vs 复用 direction 5 值 (b)缓存键语义是否纳入 evidence 强度(否则 R3-F1 silent-wrong)(c)Telegram/UI
渲染从「固定 3 路方向票」改「N 路 + 方向票/非方向 evidence 分区」。**alpha_lane worktree 保留不 merge**,待 forge
结论定 signal 形态(NO_VIEW+evidence vs 扩 direction)后再 merge —— 避免 ship「O8 假达成(assemble 进了但用户
看不到 + 缓存 silent-wrong)」。这承 R1→R2 教训:alpha 本质是「分析师历史 edge 质量旁证」而非「第四路方向票」。

**Follow-up commits**: ✅ forge v4 已定稿(`stage-forge-009-v4.md` · forge-lite · 2026-07-06 · P1 双方零分歧强收敛):
(a) 轻扩一等公民 evidence_lanes 旁路 +(b) 缓存纳 evidence 指纹(R3-F1 硬解)+(c) Telegram 真改/UI 加分区 ·
OUT-10 判为「授权下游集成」· 拆新 FU-task「009-pForge O8 下游集成」不并入 T016。
**⚠ forge 纠正本 hand-back 的 R3-F2 UI 断言**:`router_conflicts.py:169-176` `return ordered_first_three + remaining`
**透传第四路不丢**(双方 P1 + synthesizer 真读代码独立确认)· hand-back 说「双渲染都硬截断」不准 —— 只有 Telegram
真丢,UI 真实缺口是「无分区 + 显示 no_view 0% 误导」。✅ **已落地**(见下 2026-07-06 O8-downstream 条 ·
handback `20260706T073428Z`):XenoDev O8 下游集成 FU-task shipped(merge `c2e8347`)· alpha_lane 一并 ship ·
**O8 真达成** · T016 解锁。

## 2026-07-06 · 009-pForge-20260706T073428Z(O8-downstream · O8 真达成 · shipped · 起手 grep 抓 3 盲区)

**Reviewed at**: 2026-07-06T00:00:00Z
**Tags**: feature,spec-gap-fix
**Severity**: medium
**6 约束自检**: ✅ all 6 PASS(consumer 模式 · validator 自动)
**Related task**: O8-downstream(forge v4 授权的下游集成 · 兑现 T015 的 O8「alpha 平权上台」)

**内容摘要**: O8 下游集成 = 让 alpha「非方向质量旁证」正确上台 004 conflict_report。**status: shipped**
(merge `c2e8347` 到 feat/009-spec)· codex **R1-R4 单调收敛** → operator 收口 approve · **全 004 套 725 passed
无回归** · mutation 全 kill · §4.4 verifier 全过 · alpha_lane(T015)一并 ship。**O8 真达成 · T016 解锁。**
三模块全按 forge v4 verdict 落地:(a) StrategySignal 加一等 is_directional/signal_kind/evidence_strength +
ConflictReport evidence_lanes 旁路(不升级 discriminated union)+ assembler 装配分流(守方向票≥3 不变量);
(b) `_compute_signals_hash` 纳入 rationale_digest + evidence 显著性分桶 + has_divergence 确定性推导 +
`_reconcile_root_cause` 文案-布尔一致 + 方向票 canonical 排序贯穿;(c) Telegram evidence 区 + 共享
`_evidence_section.html` partial + `data-not-directional` + 「不计入多空」标注 + decisions.css auto-fit。
序列化:0016 migration(evidence_lanes_json · forward-only)+ conflict_repo 两端。

**🎯 §underweights guardrail 兑现(forge v4 硬要求起手 grep · 抓出 forge-lite 推演漏的 3 个消费面)**:
1. `ui/router_decisions.py:155` draft_preview **第 4 渲染面**(forge 未提)→ 已加 evidence 分区。
2. `repository/conflict_repo.py:32/81` **序列化两端(硬伤)**(forge 未提)→ evidence_lanes 落库即丢 = 新
   silent-wrong → 已加 0016 migration + 序列化两端 + `_dict_to_signal` 默认兜底。
3. `ui/static/decisions.css:13` `1fr 1fr 1fr` **三列硬编码**(forge 未提)→ 改 auto-fit 自适应。
两个 §underweights 未验点确认:`all_no_view` 短路只看方向票**不吞 evidence** · evidence 进 cache 键必同进 prompt。
**codex R1-R4 另抓 4 个推演漏的 silent-wrong**:has_divergence 可被 evidence 改 / prompt-hash 不同源 / 方向票
rationale 未进 hash / 无分歧类只 exact match。全是「推演看着对但真跑/真审才暴露」的对称遗漏。

**Operator decisions**:
- [x] 修 PRD §"7 M2 alpha 头 · lane 条" —— O8 指针改「✅ 已 shipped · O8 真达成」+ 3 盲区追平 + has_divergence 正式化
- [ ] 修 SHARED-CONTRACT(无)
- [x] **修 XenoDev spec(信息式)+ 记 dogfood-backlog(§3 #1 框架级)** —— forge-lite 推演漏 3 消费面 →
      「凡给共享域对象加旁路字段的下游集成,forge 推演阶段强制枚举该对象所有消费面(渲染/序列化/导出/搜索)」·
      **攒批走 /expert-forge 006 改 forge 协议**(铁律:框架级变更只走 forge · 不当场改)· 另存 feedback memory 防再犯
- [x] 收悉入库(practice-stats:O8 真达成 · codex R1-R4 + 起手 grep 印证「推演漏实证盲区」MEMORY 教训)

**Operator note**: **O8 真达成 = M2 alpha 头闭环第一个价值锚正式上台** · 里程碑。§underweights guardrail 精确
兑现(起手 grep + codex 对抗审把 forge/我推演漏的盲区全抓出)· 再次印证 [[forge-verdict-vs-empirical-ship]]。
**#2 has_divergence 判据确认**:「≥2 不同实质方向(排 no_view · LONG/SHORT/NEUTRAL/WAIT 中 ≥2 种)= 分歧」符合
「分歧」直觉定义 · 向后兼容(现有测无一断 has_divergence 具体值)· 采纳为定 · 若 T016 真数据揭示更细口径需求再回 forge。
**#1 框架级发现走 dogfood-backlog 攒批回 006 forge**(非本 handback 当场改协议)。

**Follow-up commits**: pending(本 LOG + PRD §7 O8 已达成 · 同一 IDS commit)· dogfood-backlog 记录 + feedback memory 随后 ·
#1 forge 协议改进待攒批 /expert-forge 006

## 2026-07-06T11:16:50Z · 009-pForge-20260706T102608Z(T016 · M2 evaluate CLI shipped · registry-wiring spec-gap)

**Reviewed at**: 2026-07-06T11:16:50Z
**Tags**: feature, spec-gap
**Severity**: medium
**Validator**: ✅ 6 约束 PASS(绝对路径)· verdict-evidence 无该块跳过

**Build-side 摘要(§1)**:
T016 shipped M2 evaluate CLI(P2 PPV real-path owner)。`python -m decision_ledger.alpha.evaluate` 编排 resolve(T011)→ compute_realized(T012 真 PIT price 无 mock)→ triplet(T013)→ deflate(T014),upsert 真实行进 `analyst_alpha_eval`;`DbAlphaResultProvider` 读 0015 回 TripletMetrics 给 AlphaLane。P2 PPV 终点 = data.sqlite SELECT 得到真实行(端到端 on-disk 验证)。10 集成测试(真 PIT 无 mock)+ 004 全套 735 passed 无回归 · ruff clean · §4.4 verifier clean。
- **red-team 抓 F1 ship-blocker(codex 漏)**:re-run 同 advisor 触发 IntegrityError 崩溃 + 丢新行;已修 `INSERT ON CONFLICT DO UPDATE`(0015 recomputable-table 语义 · provenance 协同刷新)。codex 因 sandbox 环境失败没真跑而漏 → 再次印证"没真跑的 review 漏实证 bug"。

**Operator decisions**:
- [x] **开单独任务 T016b** —— registry-wiring gap 决议:M2 alpha 数据已到 `analyst_alpha_eval`(交付),但**未到 production `conflict_report`**,因 `build_default` 没注册 alpha lane。gap 掉在 T015(defer)和 T016(file_domain 排除 registry.py)之间。decision = 开 **T016b** 专做 `build_default alpha_provider DI wiring`,file_domain 只碰 `registry.py`(scope 最小 · 可单独 review/verify)。capability 已证可达(DbAlphaResultProvider→AlphaLane→evidence 集成测试过)。
- [x] **KG-37 记 dogfood-backlog** —— 确认**已入册** XenoDev `dogfood-backlog.md` L738(codex-review companion branch-mode 在 sandbox bwrap loopback 失败 → §3 review 强 hook 环境性失效)。不重复记;攒批回 IDS `/expert-forge 006`。
- [ ] 修 PRD:否(registry wiring 是 task 边界问题非 PRD 产品决策 · T016b 在 XenoDev tasks/ 建卡)
- [ ] 修 SHARED-CONTRACT:否
- [ ] 无操作:否

**Operator note**: registry gap 开 T016b 单独做(不折 T017-pre,保 file_domain 隔离可验证)。KG-37 已在 backlog,确认入册攒批 forge 006。T016 alpha 数据层达成 = M2 P2 PPV real-path 终点,只差 production DI 接线(T016b)。

**Follow-up commits**: 本 LOG entry(IDS commit,pending)· T016b task 卡待在 XenoDev `specs/009-pForge/tasks/` 建(operator 切仓)· KG-37 已 XenoDev backlog L738 待攒批 forge 006

---

## 2026-07-06T17:07:06Z · 009-pForge-20260706T122339Z(T016b · alpha lane 生产接线 · shipped)

**Reviewed at**: 2026-07-06T17:07:06Z
**Tags**: feature
**Severity**: low
**Validator**: ✅ 6 约束 PASS(绝对路径 · KG-12 相对路径误报复现,见本轮 review 注)· 无 ids_verdict_evidence 块跳过

**Build-side 摘要(§1)**:
T016b alpha lane production wiring shipped。`build_default` 加 `alpha_provider` DI 参数(镜像既有 `xgboost_price_provider` 的 **DI-only** 先例):传 `AlphaResultProvider`(如 T016 的 `DbAlphaResultProvider`,读 0015 `analyst_alpha_eval` 回 `TripletMetrics`)才把 `AlphaLane`(source_id=analyst_alpha)注册为 `get_all()` 里的平权 lane(D-M2-1 · 非方向 evidence · registry 层无跨源合并/无 aggregate/winner)。**默认 None 不注册**(防 provider-less 的 `AlphaLane` 返回 NO_VIEW 占位污染 `conflict_report` + 掩盖缺接线)。AlphaLane 分支内 lazy-import(镜像 xgboost · 已确认无真实循环依赖)。这补上了掉在 T015(defer)与 T016(registry.py 在冻结 file_domain 外)之间的 registry-wiring gap —— 正是上轮 handback-review 009 决议开的 T016b。
- **review**:codex adversarial-review 这轮**真跑了**(T016/KG-37 的 bwrap loopback sandbox 失败被证明是间歇性非硬阻),2 轮收敛 approve。R1(medium)抓到真实测试充分性缺口(原测只 assert `isinstance(AlphaLane)`,忘 forward provider 也会 pass 却退化 NO_VIEW)→ 强化断言注入 provider 身份 + `analyze()` 不返回 `fail_closed_no_alpha_provider`,mutation 验证过。R2 approve · 0 material findings。C8/C10/D-M2-1/R9 全 held。
- **out of scope(记录非缺陷)**:wire.py 生产接线未动(004-pB registry→assembler→conflict_report 链现是 `_StubAssembler`,运行 app 无人调 build_default);`DbAlphaResultProvider` sync-conn vs app async-pool 张力留给真集成时(同 xgboost price_provider defer)。5 单测(mutation-proven)+ 004 全套 740 passed 无回归 · ruff clean · §4.4 verifier clean。T017 解锁。

**Operator decisions**:
- [ ] 修 PRD:否(生产接线是 task/集成边界问题,非 PRD 产品决策)
- [ ] 修 SHARED-CONTRACT:否
- [ ] 修 XenoDev spec:否
- [x] **无操作(收悉 · practice-stats 入库)** —— T016b 干净交付 M2 alpha 生产接线能力(DI-only 与 xgboost 同姿态),无治理债。

**Operator note**: 三包全收悉入库。T016b 达成 registry-wiring capability(capability 已证可达 · mutation 测过),生产真接线随 wire.py 一并 defer(StubAssembler 现实),与 xgboost 同 defer 姿态,合理。

**Follow-up commits**: 本 LOG entry(IDS commit,pending)

---

## 2026-07-06T17:07:06Z · 009-pForge-20260706T131309Z(T017 · M2 契约测试 · M2 验收 gate · shipped)

**Reviewed at**: 2026-07-06T17:07:06Z
**Tags**: feature
**Severity**: low
**Validator**: ✅ 6 约束 PASS(绝对路径)· 无 ids_verdict_evidence 块跳过

**Build-side 摘要(§1)**:
T017 M2 契约测试 shipped = **M2 验收 gate**。把 spec §8 的 M2 三契约变成可跑 pytest(违反任一=BLOCK):(1) `test_m2_source_id_unique` = C8(AlphaLane `__init__` 不注入 registry/other lane · 签名审计禁词 registry/lane/assembler)+ R9(source_id=analyst_alpha 唯一 · 重复 register raises);(2) `test_m2_no_aggregate_in_004` = C10/R10 红线(ConflictReport+StrategySignal schema 无 winner/recommended/aggregate/priority/composite 字段 · schema 字段审计 + AST ClassDef→AnnAssign 审计防注释误读为字段);(3) `test_m2_no_cross_source` = AC-2/C10 端到端(真 `ConflictReportAssembler.assemble` + mock LLM:alpha 走 evidence_lanes 单 analyst_alpha 平权 lane · 三路方向票独立不合并 · runtime `hasattr(winner/aggregate)`=False)。**契约测试 TDD 姿态**:断言既存不变量(天生绿无自然红相)→ 用 **mutation 验证**证牙(4 个 mutation 各破一个不变量→目标测试 red rc=1 · revert 后全绿)。004 全套 743 passed 无回归 · ruff clean。
- **⚠ review 值得注意(= 新 KG-38)**:先跑 codex(medium test-only→review tier),codex 后台 job 撞 `Reconnecting 2/5、3/5` session-stream 掉流,读完 5 个不变量源文件后**静默 7+ 分钟无 verdict**(status 仍 running · pid alive · reasoning stream 死)—— **session-DROP 非额度耗尽**。取消,按 CLAUDE.md fallback 换 code-reviewer subagent(medium single-layer test-only→single-pass)。fallback reviewer 独立重跑 assemble 复现路由,逐条核对 5 个 ground-truth 源 + spec §8 C8/C10,确认 scope(4 文件全 addition · 零生产代码),approve · 0 blocking + 3 非阻塞完整性 nuance(测试自身已披露为 defense-in-depth,delegate 给 004 R3 架构兜底)。REVIEW-LOG 标 `reviewed-by: subagent-fallback@2026-07-06`(**不冒充 codex**),注 codex 恢复后可选重跑(非 spine · blocks 空 · 优先级低)。
- **C8 诚实解读(记录非 scope drift)**:spec §8 C8 字面说只接 `(LLMClient, SourceDataProvider)`,但 T016b(handback-review 009 决议)加的 `alpha_provider` 是 data-result provider 非 registry/lane · 测试按"无 registry/lane 类型注入"的真实意图编码 C8 而非死抠 arity==2 · docstring 透明记录分歧。

**Operator decisions**:
- [ ] 修 PRD:否(契约测试忠实 encode spec §8 既有不变量 · C8 分歧已随 T016b 决议接受)
- [ ] 修 SHARED-CONTRACT:否
- [ ] 修 XenoDev spec:否
- [x] **无操作(收悉 · practice-stats 入库)** —— M2 验收 gate 到位。同时**记 KG-38**(见下)。

**Operator note**: 三包全收悉。T017 是 M2 层验收 gate,mutation 证牙姿态正确(契约测试无自然红相靠 mutation 证)。KG-38(codex 后台 job session-stream 掉流/静默挂起)是新框架级问题,补进 forge v7 待跑批次簇1。fallback 到 subagent 且不冒充 codex = CLAUDE.md fallback 条款正确落地(印证 KG-32 缓解有效)。

**Follow-up commits**: 本 LOG entry(IDS commit,pending)· KG-38 补 FORGE-006-v7-PENDING.md 簇1(本轮同 commit)

---

## 2026-07-06T17:07:06Z · 009-pForge-20260706T133231Z(M-fork-complete · 009-pForge fork 交付完成 · M3 go/no-go 交回 IDS)

**Reviewed at**: 2026-07-06T17:07:06Z
**Tags**: feature
**Severity**: low
**Validator**: ✅ 6 约束 PASS(绝对路径)· 无 ids_verdict_evidence 块跳过(治理/收尾摘要 · 无生产 diff · 无 review gate)

**Build-side 摘要(§1)**:
**009-pForge FORK-COMPLETE 收尾** —— 授权 scope 全交付,把 M3 go/no-go 决策交回 IDS 治理。fork scope = PRD phased [M1,M2],只交付围绕已 ship 的 004(决策壳)+008(采集)的 Strangler-Fig 前两期:**M1** = PIT bitemporal 价格历史层(唯一关键新器官)· **M2** = alpha 头(第一个可验证价值锚:分析师到底行不行)。**M3(calibration 头/统一壳/时序异质图谱/蒸馏 lane/两条回流线)显式 OUT OF SCOPE**(spec line 23 + OUT-1/2/5/6/7 · 越界=BLOCK),defer 在 fork 外等 operator 决策,而该决策本身 gate 在"M2 样本量够不够 DSR 显著"。**按 CLAUDE.md 决策矩阵,起 M3 = scope 扩张/重大架构转向,SSOT 是 IDS(idea L1/PRD L3/forge),必须在 IDS forge 不在 XenoDev 起(正是宪法防的 V4 失败模式)** → 不 build M3,交回控制权。
- **SHIPPED**(全 merge 到 feat/009-spec):M1 = T001-T008(8 任务:bitemporal 表+alembic 0014 / PIT 域模型 / PITPriceProvider / Tiingo 美股 / BaoStock A股+HK 占位 / M1 ingest CLI=P1 PPV / M1 契约测试 / CurrentState 004 adapter+xgboost 真源接入)· M2 = T010-T017(analyst_alpha_eval+0015 / frozen join / realized-return C16 双 as_of / TipRanks 三件套 / walk-forward+DSR/PBO / AlphaLane 上台 / M2 evaluate CLI=P2 PPV / T016b 生产接线 / T017 契约测试)。每任务走全 parallel-builder 流(TDD/跨模型 review/逐任务 hand-back)· **18 条不可变记录**。终态:working tree clean · 004-pB 全套 **743 passed** / 4 skipped / 1 xfailed 无回归。
- **PPV 双终点真路径(路径中无 mock)**:P1(M1)真 ingest CLI→真 alembic→真 source→`price_daily/ticker_status` SELECT-able(close_raw/adj_factor/trade_date/as_of)· P2(M2)真 evaluate CLI→frozen join→per-signal 双侧显式 as_of 的 PIT-native `get_adjusted_close`(无 mock 价 · 无 as_of=today adapter)→C16→DSR/PBO→`analyst_alpha_eval` SELECT-able + `conflict_report` 有 alpha source_id 且无 winner/aggregate。两条 anti-PPV 线全 held。

**Operator decisions**:
- [ ] 修 PRD:否(收尾摘要 · 授权 scope 全交付无偏离)
- [ ] 修 SHARED-CONTRACT:否
- [ ] 修 XenoDev spec:否
- [x] **无操作(收悉 fork-complete 收尾 · practice-stats 入库)**
- [x] **M3 go/no-go = 显式待决项(交回 operator · 本轮不起 forge)** —— 见下 Operator note。

**Operator note**: **接受 009-pForge fork-complete 收尾**。M1+M2 授权 scope 全交付(20 任务 · 743 passed · PPV 双终点真路径无 mock),这是投资闭环第一个可验证价值锚落地。**M3 go/no-go 暂不决**:按 M-fork-complete 自陈,M3 gate 在"M2 样本量够不够 DSR 显著"——须先看 M2 实际 alpha 数字(真跑 evaluate CLI 出 analyst_alpha_eval 行 + DSR/PBO)才知道分析师 alpha 判不判得出;O9 不足样本诚实路径已在。**没看到数字前起 M3 forge = 信息不足下做重大架构决策**(正是 forge 反复防的 V4 失败模式)。DEFERRED/KNOWN-GAPS 三条(HK 付费源/wire.py 生产真集成 StubAssembler/M3 gate)均为授权 scope 内非缺陷,记录在案。dogfood 揭 KG-30~38(9 条)已 XenoDev backlog + FORGE-006-v7-PENDING 攒着,KG-38 本轮补入。

**Follow-up commits**: 本 LOG entry(IDS commit,pending)· M3 go/no-go 待 operator 看 M2 alpha 数字后另行决策(未起 forge)

---

## 2026-07-07T03:43:00Z · 009-pForge-20260707T032617Z(P2-prod-precondition-gap · spec-gap · M3 gate 数字拿不到的根因)

**Reviewed at**: 2026-07-07T03:43:00Z
**Tags**: spec-gap
**Severity**: medium
**Validator**: ✅ 6 约束 PASS(绝对路径)· 无 ids_verdict_evidence 块跳过

**Build-side 摘要(§1)**:
build-then-probe 结果(**没碰生产凭据、没写任何数据、建库前就停**):**M3 go/no-go 的 gate 数字当前拿不到**,两个 gap。
- **GAP 1(阻塞)· 缺 008→004 信号 backfill 链**:evaluate 读 004 的 `advisor_reports/strategy_signals/watchlist`(alpha/join.py 核实),**不读** 008 采集库。008 采集 pipeline 产的是**内容库**(collection.db:图文/回放/问答语料)非 004 信号行;当前部署**无**把 008 内容转成 004 信号行的实现路径。→ 004 源表空 → evaluate 结构上能跑但返 `resolved_signals=0/accepted_rows=0`(不崩,没数字)。
- **GAP 2(为什么顺手补越界)· strategy_signals 无 advisor 定位键**:该表无 advisor_id 列(T011 red-team #B 已记),v0.1 单 advisor 假设下不误触,真多 advisor backfill 会双重归因。彻底修=给已 ship 的 004 加定位键 → 撞 **spec OUT-10**(不改已 ship 的 004 StrategyModule/信号产出 schema)= BLOCK。
- **基础设施**:生产 data.sqlite 不存在(~/decision_ledger/ 无);alembic+evaluate 过 config.load_settings() 因缺 ANTHROPIC_API_KEY 硬失败(凭据隔离边界)。
- **为何是 spec-gap 非 XenoDev 内部修**:缺的 backfill 链是**跨 fork 集成面,归属从未指派**(009 spec scope 是 M1 价格层 + M2 alpha 头消费**已存在的** 004 信号,假设上游已填但当前部署未填,填充路径不在任何 fork)。闭合它要么建新 ingestion 组件(fork/PRD 不存在)要么改已 ship 的 004(OUT-10 BLOCK)——都是 IDS 治理决策。记录而非行动也避开 V4 失败模式(不猜数据、不越 BLOCK 线凑数字)。**再次印证 build-then-probe 是照妖镜**:理论上"跑 evaluate 拿数字"看似一步,实证 probe 才发现整条输入链缺失([[forge-verdict-vs-empirical-ship]])。

**Operator decisions**:
- [ ] 修 PRD:否(本轮不改 PRD · smoke path 不需要)
- [ ] 修 SHARED-CONTRACT:否
- [ ] 修 XenoDev spec:否(单 advisor 假设已在 domain/advisor.py:28 · 只需显式确认非新增)
- [x] **决议 1 · backfill 归属 = 先走 smoke path 拿真数字**(§3-(3))—— 手工塞**一个真 advisor 的少量真历史信号**(真 ticker/方向/日期)进 004 三表(advisor_reports+strategy_signals+watchlist)→ ingest 对应真价格(P1)→ 跑 evaluate → 得真 hit_rate/dsr/trial_count(或 O9 诚实 insufficient_sample)。**不建通用 backfill、不撞 OUT-10**,最快解锁 M3 决策且端到端验证 P2 全链。需 operator 提供真值 + 生产凭据(凭据不进 agent 上下文 · XenoDev 只给命令骨架 + 前置检查清单)。008→004 通用 bridge 的正式归属**暂不定**,待 smoke path 出的数字先告诉我们"分析师 alpha 判不判得出",再决定值不值得建通用桥。
- [x] **决议 2 · advisor 定位键 = 保持 v0.1 单 advisor 显式假设,defer 键**(§3-(2))—— evaluate 对**恰好一个** advisor 正常工作。把"单 advisor"钉成显式 v0.1 约束,多 advisor 定位键 defer 到真需要多 advisor 时。**不授权 OUT-10 修订**(不改已 ship 的 004)。与 v0.1 scope 一致。

**Operator note**: 组合决议 = smoke path + 单 advisor defer 键,两条都不建通用 backfill、不撞 OUT-10,最省事解锁 M3 gate。**M3 go/no-go 仍挂起**,现在多一个明确前置:operator 出一个真 advisor 的少量真历史信号 + 生产凭据 → XenoDev 跑 smoke path 出真 alpha 数字 → 看 DSR 显不显著 → 才谈 M3。这个 gap 是投资闭环的真卡点(M2 交付了"能算 alpha 的机器"但机器没输入,008 采集内容≠004 信号),记入 [[forge-009-closed-loop-inflight]] 与 [[closed-loop-investing-product-vision]] 的下游缺口。008→004 通用 bridge 归属留作未来 idea 候选(smoke path 出数字后再评估 ROI)。

**Follow-up commits**: 本 LOG entry(IDS commit,pending)· smoke path 执行在 XenoDev(需 operator 出真值+凭据,command skeleton 由 XenoDev 给)· M3 go/no-go 待 smoke path 真数字后另议

## 2026-07-17T03:09:16Z · 009-pM3prime-20260716T162427Z(T013 · E0+E1 全站 ship · E1 替身 STOP 需真 LLM 复核 · 4 决议)

**Reviewed at**: 2026-07-17T03:09:16Z
**Tags**: prd-revision-trigger
**Severity**: medium
**Validator**: ✅ 6 约束 PASS(绝对路径)· 无 ids_verdict_evidence 块跳过 R-Q6 预检

**Build-side 摘要(§1/§2)**:
E0(口径预注册)+ E1(密度普查/两层金标)全站实装完成(T001-T012 · 869 passed/7 skip/1 xfail · ruff clean),两条 PPV 真库端到端验过。**首要结论**:E1 密度普查产诚实 STOP(accepted 0 / rejected 29 全 no_direction · per-market {US:0,CN:0,HK:0} 全 < 候选阈值 30),**但 0-accepted 来自确定性 `literal_ticker_proposer` 替身**(英文 ASR 转写里中文情绪词/隐性荐股无法字面命中),**是"下界/占位"非真密度,不可据以否定 M3'**。真密度需真 LLM 提取器(`--proposer llm`),llm proposer 端到端接线本 fork 留 NotImplementedError 待授权。另:密度口径 spec 张力(per-horizon fan 3 桶 = 假独立证据,已修 per-market)· record_tickers=weak_association(literal_rate≈0.325 · 走 verify 路径)· 两层金标 harness 就绪未真跑(Layer-2 硬要真人第二源 D-7 · gate fail-closed 默认关)· gate extractor_variant known-gap(E2 设计输入)。codex 双挂死(KG-38 第 8 击)走 subagent fallback(red-team+code-reviewer 双跑 · 8 findings 全修)。

**Operator decisions**:
- [x] 修 PRD §"附录 B(密度口径/阈值)":per-market 口径确认 + 阈值语义改 advisory(决议 1/2)
- [ ] 修 SHARED-CONTRACT:否
- [x] 修 XenoDev spec(信息式):授权补接 llm proposer(决议 3)· variant-gap 记 E2 设计输入(决议 4)
- [ ] 无操作:否

- **决议 1 · 密度口径 = per-market horizon-independent(确认)**:采纳 hand-back 建议,确认 XenoDev 修正实装(review HIGH#1)。horizon 是 E2 回测窗选择、非提取时属性,一条信号 fan 进 3 个 horizon 桶 = 假独立证据。PRD 附录 B 口径随之回写。
- **决议 2 · 预注册阈值 = 签 30/stratum 为 advisory 参考阈值**(threshold_hash_candidate=97c58440426f8770):系统照常输出「过/不过参考线」的诚实判定并留事前预期记录(防事后挪标准),**但非自动毙刀** —— E2 go/no-go 由 operator 看完整密度报告后人工拍板。⚠ 本决议**修改了 hand-back 原建议的硬闸门语义**(operator 权衡:30 反推自 M2 walk-forward、无实证基础,不提前拍死;advisory 保住预注册纪律的诚实留底,又保留事后分析空间)。XenoDev 实装时 verdict 照出,但 gate 语义标 advisory。
- **决议 3 · 授权真密度补跑**:授权 XenoDev 补接 `build_llm_proposer` → decision_ledger.llm 客户端(温度 0 · 输出 schema=ProposedSpan[]),operator 随后配 LLM 凭据(`--token-env`)跑真密度普查(读中文原文语义抽)。E1 真数字是 M3' ROI 闸门。
- **决议 4 · E2/E3 = 维持不授权 + 纸面设计先行**:forge v5 三条 BLOCK 红线维持(E2 历史回测/E3 forward 线做进 XenoDev = 越界);但启动 **E2 设计输入清单 + 接口草案(纯文档 · 零代码)**,gate extractor_variant gap(gold 表加 variant 列 + gate WHERE 加此维)为清单第一条。E1 放行后开发照单起跑。
- **收悉**:金标真跑待 operator 配真人第二标注源(D-7 · 非 LLM)后排期;codex 恢复后对 census 密度口径/PIT 时区/Krippendorff α/0017 migration 优先补跑权威确认(KG-38 fallback 补偿)。

**Operator note**: E2/E3 现状确认 = **零代码**(hand-off 只授权 E0+E1),非"待测试"。operator 原倾向提前搭 E2 架子,经权衡后维持红线:证伪链的意义就是上游毙掉时下游零沉没成本(且沉没成本会让人舍不得毙,V4 失败模式);E2 图纸未定稿(口径刚改/variant 列缺/金标未跑),提前施工大概率返工。折中 = 纸面设计输入先行。阈值 advisory 化同理:不确定的数不拍死,但事前预期必须留底。E2/E3 解锁三条件 = 真密度显著 + 两层金标过 + operator 授权,当前均未满足。

**Follow-up commits**: 本 LOG entry(IDS commit,pending)· PRD 附录 B 回写(per-market + advisory 语义,pending)· llm proposer 接线 + 真普查在 XenoDev(待 operator 凭据)· E2 设计输入清单(纯文档,XenoDev 或 IDS 侧起草)

## 2026-07-17T09:25:00Z · 009-pM3prime-20260717T081757Z(KG40-density-blocked · E1 真密度被 proposer 契约缺陷系统性阻断 · 起 forge 009 专场)

**Reviewed at**: 2026-07-17T09:25:00Z
**Tags**: prd-revision-trigger
**Severity**: high
**Validator**: ✅ 6 约束 PASS(consumer 模式 · 绝对路径)· 无 ids_verdict_evidence 块跳过 R-Q6 预检
**Related task**: KG40-density-blocked(E1 真密度收口 · 接续第 22 条决议 3 授权)

**Build-side 摘要(§1/§2)**:
第 22 条决议 3 授权的真密度普查真跑结果:DeepSeek(deepseek-v4-flash · 温度 0 · JSON mode ·
sample 200)跑 61 分钟处理 58 条 → **56 条 finish_reason=length 截断 + 2 条返空 + 0 成功 span
(≈100% 失败)**,按 census 守门(`llm_parse_failures>0 → 0-accepted 不可信`)+ runbook 铁律
主动 TERM 停跑(key 停烧)。**根因(KG-40)**:`_build_extraction_prompt` 要求 LLM 产原文
**字符偏移**(span_start/end 整数),推理型模型在长语料 + JSON mode 下烧爆 4096 token 输出
预算 → JSON 未闭合即截断。smoke 7 条(2/7 截断)没暴露规模,真跑 200 才现形。**结论:E1
真密度读数不成立**(非 below/meets threshold,是工具契约缺陷)→ E2/E3 第一解锁条件仍未满足。
两条候选修法(①改产逐字文本片段 + 下游 `str.find` 回锚 · 需处置子串多处出现歧义 vs ②分块喂 ·
破坏全局偏移语义)均动 extractor 引文锚定 C3 契约(PRD §7-3)= spine 级,XenoDev 未当场改。
附:codex adversarial-review 本 project 累计第 5 次挂死 0 verdict(KG-38 复现 #3/#4/#5),全靠
subagent fallback 双跑(red-team + code-reviewer)审出并逼修 9 个真 bug(含 cache 串号 CRITICAL)。

**Operator decisions**:
- [x] **决议 1 · 起 forge 009 专场(forge-lite)定 extraction proposer 契约** —— 裁定候选①
      (文本片段 + `str.find` 回锚 + 歧义 typed rejection)vs 候选②(分块)vs 第三方案,含
      §7-3 引文锚定契约的歧义处置。**与 006 框架批次解耦**(E1 收口是 M3' ROI 闸门,不等 006
      排期;先例 = provider 契约走 forge v3)。契约定稿 + XenoDev 改线后才授权重跑真普查。
- [x] **决议 2 · 修 PRD §"4-E1" + version 头(v0.3)** —— E1 加 blocked-by-KG-40 状态注记
      (读数不成立 ≠ STOP · 守门拦下截断假 0 · 修法走 forge)。本轮已回写,与第 22 条 pending
      的附录 B 回写同一 commit 收口。
- [x] **决议 3 · `llm_parse_failures` 守门固化 = 采纳,进 forge 议题** —— 与候选裁定同场定稿进
      proposer 契约:任何 proposer 实现必须报 parse/api failure 计数,>0 则 0-accepted 判不可信,
      不许静默当真 0 密度(防「工具失败被误读成密度结论」通用护栏)。
- [ ] 修 SHARED-CONTRACT:否
- [x] **修 XenoDev spec(信息式 · forge 结论后)** —— proposer 契约 verdict 落地后回 XenoDev 起
      FU-task 改接线 + 重跑真普查。
- [x] **收悉入库(4 项)**:① E2/E3 维持不授权(三条件第一条未满足 · forge v5 三条 BLOCK 红线
      不动);② KG-40(high)+ KG-38 复现 #3/#4/#5(建议⑥升级 fallback 默认首选)已入 XenoDev
      dogfood-backlog,攒批回 /expert-forge 006;③ 已交付资产收悉(DeepSeek 接线/双口径密度/
      签字 threshold_hash 落库/E1 runbook + E2-design-inputs · 907 passed · 未 commit 领先 origin
      20 · 契约修好后重跑不需重做);④ codex 恢复后对 DeepSeek 接线/cache 语义/签字 hash/双口径
      密度优先补审作权威确认。

**Operator note**: 这次真跑不算失败——它精确定位了 spine 契约缺陷,且 census 守门(上轮 red-team
fallback 逼加的)把「截断假 0」和「真没信号」区分开,没让全 0 图被误当 STOP 依据。再次实证
smoke 绿 ≠ 真跑可行([[forge-verdict-vs-empirical-ship]] 第 N 击)。proposer 契约是 009 spine
非 006 框架件,专场 forge 与 006 攒批解耦,避免 M3' ROI 闸门被框架批次排期拖住。E1 真密度链
当前状态:契约裁定(forge)→ XenoDev 改线 → 重跑真普查 → 才有 E2 go/no-go 的输入。

**Follow-up commits**: pending(本 LOG + PRD v0.3 同一 IDS commit)· forge 009 专场待起
(/expert-forge 009 · 议题 = proposer 契约候选裁定 + 歧义处置 + 护栏固化)· XenoDev 改线 +
重跑待 forge verdict

## 2026-07-18T13:54:41Z · 009-pM3prime-20260718T133419Z(KG40-anchoring-dp · 引文回锚制落地 + DP 重写 R18 approve · 授权重跑真普查)

**Reviewed at**: 2026-07-18T13:54:41Z
**Tags**: spec-gap-fix
**Severity**: high
**Validator**: ✅ 6 约束 PASS(consumer 模式 · 绝对路径)· 无 ids_verdict_evidence 块跳过 R-Q6 预检
**Related task**: KG40-anchoring-dp(接续第 23 条决议 1 → forge v6 verdict [A] 的落地收口)

**Build-side 摘要(§1/§2)**:
forge v6「引文回锚制」四条款契约改造完成(XenoDev commit **76036af** · 13 files · +2515/-231 ·
feat/009-spec 未 push):新模块 `anchoring.py` 确定性分层回锚(exact→normalized→fuzzy→
not_found/ambiguous),核心 = **occurrence 消解 DP 重写**——单一归一坐标候选表 · 位置序分配 ·
三口径(distinct/capacity/分配)共源 → R13-R16 的 raw-vs-normalized 口径不对称**构造性移除**。
`census.py`:prompt_v2(LLM 只产逐字引文)· census_invalid 硬门(失败计数>0 → rollback + 非零
exit · 不声称落库)· 三类失败计数 fail-closed · 模型无关预算 · variant 身份(llm_extraction_v2)。
验证:**993 passed · 7 skipped · lint clean · codex 18 轮真跑 adversarial-review R18 approve ·
0 material**。硬边界全守(caliber v1 / gold_layer / 0017 / 004 未碰 · provenance 走 detail 不落库)。
决议链:R16 四轮同轴熔断 → operator 裁 [2] DP = **v6 契约「贪心证不出四语义 → 用 DP」分支执行**
(非新决策);R17 暴露两 latent(F1 NFKC 多字符展开假 strong → 回映边界校验;F2 distinct==demand
不保证非重叠可行 → 区间调度 capacity)——旧贪心码同漏 · 非 DP 引入;R18 确认自洽。熔断机制实证
有效(四轮同轴 → 裁决终结 → 两轮收敛)。附 KG-41:codex 本 worktree 跨天恢复,推翻 KG-38
「必挂 · fallback 首选」判断 → fallback 判据需加时效性(框架级)。

**Operator decisions**:
- [x] **决议 1 · 授权重跑 E1 真普查**(第 23 条「契约定稿 + 改线后才授权重跑」条件已满足)——
      XenoDev-009 新 session 按 E1 runbook(tier 读数版)跑 sample-size 真普查;**重跑前确认
      DEEPSEEK key 就位**(key 值不 log/不入 context 铁律不变);读数产出(exact+normalized
      硬下界 + fuzzy 分层另报 + weak_anchor 率)经 hand-back 交回,才谈 E2 go/no-go。
- [x] **修 PRD §"4-E1" + Version 头(v0.4)** —— blocked-by-KG-40 状态注记追加「已解除」段
      (保留 v0.3 原注记作审计);E2/E3 解锁第一条件在真密度读数产出前仍未满足。
- [ ] 修 SHARED-CONTRACT:否
- [ ] 修 XenoDev spec:否(FU 已收口,spec 无遗留)
- [x] **决议 2 · KG-41 归入 006 攒批**(hand-back 建议进 forge 009 被改判:fallback 判据在
      XenoDev CLAUDE.md = 框架件非 009 产品域,与 KG-38 复现批合并,下次 /expert-forge 006 议
      「fallback 判据加时效性」)。
- [x] **收悉入库(4 项)**:① R8 弱锚计入 verdict defer = operator 冻结口径(隐性信号前提 ·
      非缺陷 · 真跑读数时结合 weak_anchor 率人工终裁);② R10 并发 stats 竞态 defer = 假设场景
      (单进程串行无此路径 · docstring 已约束 · 并发化时重审);③ 76036af 未 push(push 需
      operator 在 XenoDev 侧确认);④ 熔断机制实证有效(「预写 fallback 分支 + 同轴熔断」模式
      成立,见 forge-verdict-vs-empirical-ship 案例 3)。

**Operator note**: R16 熔断没有变成治理事故,是因为 v6 契约把「贪心可能证不出」预写成了带判据的
fallback 分支——裁决只是执行分支,R13-R16 的对抗测试直接变成 DP 验收套件。R17 两个 latent 缺陷
(旧贪心同样漏)说明 DP 的清晰结构反而暴露了贪心结构藏住的洞。E1 链当前状态:契约已修 → 重跑
已授权 → 真密度读数 → E2 go/no-go。KG-40 从发现到解除:2026-07-17 真跑现形 → forge v6 一天收敛 →
2026-07-18 落地 + 18 轮 review 收口。

**Follow-up commits**: pending(本 LOG + PRD v0.4 同一 IDS commit)· 重跑授权下发 = operator 持
本条决议开 XenoDev-009 session(启动 prompt 见本次 review 输出)· KG-41 已在 XenoDev
dogfood-backlog 攒批,IDS 侧无需另建文件

## 2026-07-19T00:57:37Z · 009-pM3prime-20260718T143324Z(E1 真普查完成 · KG-40 根治实证 · 弱锚抽查后终裁 US 分市场 go)

**Reviewed at**: 2026-07-19T00:57:37Z
**Tags**: prd-revision-trigger
**Severity**: high
**Validator**: ✅ 6 约束 PASS(consumer 模式 · 绝对路径)· 无 ids_verdict_evidence 块跳过 R-Q6 预检
**Related task**: E1-real-census-rerun(接续第 24 条决议 1 的授权重跑 · E1 链收口)

**Build-side 摘要(§1/§2)**:
E1 真密度普查重跑完成(引文回锚制新契约 · commit 76036af · 真 DeepSeek v4-flash · 温度 0 ·
prompt_v2)。**KG-40 根治实证**:07-17 旧契约 58/58 全截断 → 本次 102 records · **0 truncation ·
三类失败全 0**,census_invalid 硬门未触发,读数有效。**strong 密度 = {US: 40, CN: 1, HK: 0}**
vs advisory 阈值 30/stratum;verdict=below_threshold_advisory(CN/HK 触发)但 US 单市场超阈
(+10)——per-market 分化非全域稀疏。拒绝构成:sector_only 175(语料特性主因)·
unanchorable_citation 13(not_found 4 + ambiguous 9 = DP 消解正确不猜)· no_direction 4;
fuzzy 率 1/42 极低。threshold_hash 库内核对 == 第 22 条期望值。weak_anchor_accepted 自报
34/41(83%),高率触发 R8 defer 的「operator 抽查引文质量」条款。

**IDS 侧弱锚抽查(本次 review 现场做 · 全量 29 条语义弱锚逐条切原文核验)**:
- **83% 口径修正**:build 侧 34/41 用区分大小写字面判据,其中 5 条是分析师小写 ticker
  (mu/amd/mrvl/hood/rddt)实为无争议真锚 → **真语义弱锚 = 29/41(71%)**。
- **~23/29 为教科书级真隐性信号**(M3' 前提场景实证):「老黄/达子」→NVDA ·「美光」→MU ·
  「谷子」→GOOGL ·「coke」→KO ·「新一生」(ASR 转错"新易盛")→300502 · 跨句指代
  (him=Walmart)→WMT 等,无幻觉铁证。
- **可疑过度联想簇 = 6 条(全在 US)**:① src=60232 ETF 权重枚举簇 ×5(KO/PG/PM/PEP/MO —
  IYK 成分权重表被拆成 5 条个股 long conf 0.7);② id=5「美存储大涨」→MU(sector→name 推断)。
- **鲁棒性结论**:最保守折扣(6 条全毙)后 US 40→34 **仍 > 30**;US 超阈对抽查折扣稳健。

**Operator decisions**:
- [x] **决议 1 · E2 终裁:US 分市场 go · CN/HK STOP**(advisory 人工终裁 · 抽查后裁定)——
      「真密度显著」前提对 US market 成立(最保守折扣 34>30);CN=1/HK=0 真稀疏(单团队语料
      美股为主 · 结构性限制),CN/HK 分市场 STOP,补语料后可另启普查再议。
- [x] **修 PRD(E2 闸门 per-market 化)**——M3' PRD「真密度显著」前提 / E2 解锁条件改写为
      分市场语义(US/CN/HK 各自判),记录本次真普查读数 + 抽查折扣依据;E2 对 US 解锁。
- [ ] 修 SHARED-CONTRACT:否
- [x] **修 XenoDev spec(信息式 · 口径反馈)**——跨仓信息式记录两条:① E2 分市场执行口径
      (US go / CN·HK STOP);② sector_only 口径延伸建议:「ETF 成分权重枚举 → 个股信号」与
      「板块词 → 单一 ticker」两类过度联想样本已定位(src=60232 簇 ×5 + id=5),建议下轮口径
      迭代时并入 rejection 判据(非本轮缺陷 · 不 rollback 读数)。实际改动在 XenoDev 侧 session 做。
- [x] **收悉入库(3 项)**:① 契约层健康 —— 引文回锚制 + census_invalid 硬门 + DP 消解真跑
      全绿,KG-40 已根治,无契约缺陷需回 forge;② R8 弱锚口径 defer 按约定完成人工终裁闭环
      (本条即终裁);③ R10 并发 defer 延续(单进程串行无此路径)。

**Operator note**: 弱锚抽查是本条决议的关键输入:handback 自报 83% 弱锚率吓人,切原文逐条核后
实际语义弱锚 71%,其中八成是 M3' 立项时赌的那类真隐性信号(中文俚语/别名/ASR 噪声指代)——
这正是「隐性信号可被口径捕捉」假设的第一次正面实证。可疑的只有一簇可定位的 ETF 权重枚举
(枚举成分 ≠ 逐股荐买)+ 一条 sector→name,毙掉也不改 US 超阈结论,故 US go 裁得放心。
E1 链就此收口:KG-40 发现(07-17)→ forge v6 契约(当天)→ DP 落地 R18 approve(07-18)→
真普查读数 + 终裁(07-19)。E2 的下一步输入 = per-market 化后的 PRD。

**Follow-up commits**: pending(本 LOG + PRD per-market 修订同一 IDS commit)· XenoDev 侧
信息式 spec 记录待 operator 开 XenoDev-009 session 时带入

## 2026-07-23T10:10:00Z · 009-pM3prime-20260723T082127Z(FU-KG42 · 金标 Layer-2 第二源冲突 · 起 forge 009-pM3prime v1 收敛)

**Reviewed at**: 2026-07-23T10:10:00Z
**Tags**: prd-revision-trigger
**Severity**: medium
**Operator decisions**:
- [x] **修 PRD §"4-E1/D-7"(手工改 · 已落地)**——operator 裁 Decision menu [A],D-7 改写草案
      (新措辞 + 验收铰链四条 + §2×D-7 澄清 + 红线保留 + 3 v0.2 待解)已抄进 PRD §4-E1 + §7-4;
      **PRD v0.5 → v0.6**。
- [ ] 修 SHARED-CONTRACT
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] **起 forge 009(专场)—— 已完成 v1,verdict 已产出**(operator 裁「起 forge 009」·
      本条为 forge 触发决议,PRD 改写落点在 forge stage §Next-version PRD draft,operator 读
      stage 文档后经 Decision menu [A] 手工改 PRD 已落地)

**Operator note**: handback 主诉 = frozen PRD §2(单人不懂投资)× §4-E1/D-7(领域独立真人第二源)
互斥 → 两层金标 Layer-2 无合格验收主体 → E1 诚实 STOP。validator 6/6 PASS(初判 check-5 FAIL 系
相对路径 gotcha · 传 realpath 后 PASS · 又一次复证 [[forge-006-v7]]「validator 必须传绝对路径」)。
声明已核实(gold_layer2.py:81 human 硬约束真实 · commit 6f11186 零代码留痕属实 · KG-42 在
dogfood-backlog:789)。operator 核心质疑「2026 异源强模型能否当合法第二源」→ 起 `/expert-forge
009-pM3prime` v1(Reviewer A=Claude Opus 4.8 · B=**GPT-5.6-Sol xhigh** 异源第二源本身呼应议题;
为此改 codex config→gpt-5.6-sol + 软链→0.144.5,均真跑验证 · 见 [[codex-version-model-config]])。

**Forge v1 verdict(converged · strong-converge · 无 unresolved)**:保留 gate 骨架 + 双层链 +
D-7 Layer-2 fail-closed 实质;第二源从来源类型硬编码 refactor 为三项分离契约(错误独立性/领域能力/
最终仲裁权);**跨 vendor 强模型不得当 Layer-2 独立终审 —— 两组零论文重叠正交 SOTA 一致证明**
(Nine Judges 跨 vendor φ=0.6 · Correlated Errors 350+ 模型 60% 同错 · 人 n_eff 是 LLM 2 倍 ·
AmbER 长尾别名共享流行度先验 · FActScore/SAFE 独立性来自外证据锚定非品牌)。**frozen §2×D-7 非
产品级真互斥 → 收窄为「当前资源下 Layer-2 全量验收暂不可满足」;operator 配可审计证据协议后可
自任独立第二源(靠独立性而非领域深度)· 无须前置外求真人**(消 handback「无验收主体」死结)。
可执行路 (b)降级验收 + (c)重定义真人源;窄义 (a) 外证据锚定模型辅助仅进 Layer-1;未校准前
fail-closed。红线:第二 LLM 直接当 Layer-2 终审 = V4 · `gold_layer2.py:81` 保留。三方向裁决 +
D-7 改写草案(新措辞 + 验收铰链四条)见 `discussion/009/009-pM3prime/forge/v1/stage-forge-009-pM3prime-v1.md`。
**皇冠自证**:双方 P1 都独立倒向 refactor(重演 forge v5 双模型回声室),但 P2 各自跑零重叠 SOTA
都推翻自己 P1 = 引正交外证据破收敛(G-R1 原教训正确执行)—— 本轮 forge 恰是「不能靠双模型互审自证、
须引外部实证」的正面演示,也正是 D-7 想守护的道理。3 条 v0.2 note 待解(逐维双错率阈值 / 核验知识源 /
operator 独立于提取器的隔离流程)。KG-42 框架缺口(第二源可得性立项前置校验)归 006 攒批。

**Follow-up commits**: pending(本 LOG 第 26 条 + forge v1 全产物 + **PRD v0.6 D-7 改写落地** +
codex 环境层修复同批 · 未 push)· **PRD 改写已落地(Decision menu [A] 完成 · §4-E1 D-7 改写块 + §7-4)**·
下一步 = 回 XenoDev-009 `claude -w 009-pM3prime` 按新契约实装第二源资格层(起跑前解 3 v0.2 note:
逐维双错率阈值 / 核验知识源 / operator 独立于提取器的隔离流程)

## 2026-07-23T15:04:24Z · 009-pM3prime-20260723T134606Z(FU-D7-layer2 · forge v1 D-7 改写 build 侧落地 · KG-42 死结解 · subagent-fallback 4 轮 approve)

**Reviewed at**: 2026-07-23T15:04:24Z
**Related task**: FU-D7-layer2
**Tags**: feature
**Severity**: medium
**6 约束自检**: ✅ all 6 PASS(consumer mode · 绝对 realpath)。⚠ 首次跑 FAIL 于约束 5(id consistency)——
根因是 `$HANDBACK_DIR` 尾斜杠致路径出现 `discussion/009/handback//` 双斜杠,validator 提取 `<X>` 段的 regex 断链;
传 `realpath` 归一后 all-6 PASS。**又一次复证 [[001-radar-gate-fail-prd-v11]] / [[forge-006-v7]]「validator 必须传绝对路径」gotcha**(非真 corruption)。
**verdict-evidence 预检**: n/a(无 `ids_verdict_evidence:` 父键 · 本包非机器 verdict-evidence 包)

**Operator decisions**:
- [ ] 修 PRD §"—"(不勾选:D-7 改写已在 PRD v0.6 §4-E1 · 本包非 re-litigate 产品语义 · 见 LOG 第 26 条)
- [ ] 修 SHARED-CONTRACT §"—"(不勾选:本包无协议层变更诉求)
- [x] **接收 build-ship · 收悉入库**(确认 D-7 改写 build 侧落地 · subagent-fallback 4 轮对抗 approve · 0 ship-blocking 红线 breach · 1054 passed · 作 practice-stats 入库)
- [x] **记 KG-42 框架治理 defer 归 IDS forge**(§3-3:① 证伪链金标框架加「第二源可得性」立项前置校验 ② PRD 模板加「金标验收主体来源」字段 · build 侧未当场改 framework=dogfood 铁律 · 攒批留待 forge 议)

**Operator note**:
本 hand-back 是 forge 009-pM3prime **v1 verdict 的 XenoDev build 侧落地回报**(build-ship + 残留 defer),非再抛问题——
闭合 LOG 第 26 条留的「回 XenoDev-009 按新契约实装第二源资格层」。**KG-42 死结解**:第二源从「领域独立真人」refactor 为
「错误独立性代理」(三分离契约 · 外证据锚 + 逐维双错率证成)→ operator 可自任独立第二源(靠独立盲标非领域深度)。
交付 7 改 + 5 新(alembic 0018 扩 `gold_layer2_result` 12 列 + 新子表 `gold_layer2_dimension` · `gold_layer2.py` 三纯函数 +
`evaluate_layer2` 演进 · 新 `blind_annotate.py` 两阶段盲标 CLI · SLA/spec/dogfood 回填)· **1054 passed**(was 993 · +61)·
**红线 4 轮复验逐字节不变**(`gold_layer2.py:203` 第二 LLM/跨 vendor 未校准终审仍 raise · gate.py fail-closed 不动 ·
caliber_hash=`46fbd4b7b46d397b` 不变)。**第 26 条留的 3 个 v0.2 note 本 build 全解**:逐维双错率阈值→方法学推算 + C6 预注册
(reconcile/CLI 偏离冻结门槛→raise · 从 advisory 升为结构 fail-closed · R4 根因修)· 核验知识源→复用 004 `watchlist`(PIT-neutral)·
隔离流程→`blind_annotate.py` 两阶段盲标 + 时序可证伪。

**cross-model review 处置(关键决议)**:codex 真路径**挂死**(job stalled 18min+ 无 verdict · 同 KG-38/KG-B12 codex-hang)→
build 侧按 CLAUDE.md fallback 段走 red-team + code-reviewer 双跑(4 轮单调收敛 4→3→3→1 approve · REVIEW-LOG 标 `subagent-fallback@2026-07-23` 未冒充 codex)。
build 侧建议「codex 恢复后优先补跑权威确认」。**operator 裁定:接受 subagent-fallback 为终态,不要求 codex 补跑**——
理由:4 轮 red-team+code-reviewer 对抗收敛 + 红线逐字节 4 轮复验 + 11 findings 全 latent library-layer footgun(生产路始终 fail-closed · 无一 false-PASS 逃逸到 ship)已足;
本裁定是对 build 侧「过桥非替代」建议的 operator 侧显式收口(**偏离 build 侧建议已如实记录**)。

**残留 defer(非本决议 close · 已收悉)**:① operator 真盲标产真数字(harness 全就位 · 待真跑 · 同 O8「待第二源真跑」性质)·
② watchlist 补权威数据(B1 · **本环境 watchlist 空 → ticker 外证据锚 coverage=0 → fail-closed 硬锚** · E2 前置 · 本 fork 外 · 零代码解锁 ·
红线:严禁本 fork 现填交易所清单可能引 look-ahead)· ③ blind 隔离技术不可证性(B5 · honor-system + 时序可证伪已是最强可得 · 更强隔离=PRD 治理级由 operator 决)。
**E2 解锁三条件 US market 仍未齐**:① 真密度 [US ✅ 决议 25] · ② 两层金标 [🔶 harness 扩契约就位 · 门槛预注册 · 待 operator 真盲标 + watchlist 补数] ·
③ operator 授权 [❌] → 第 2 条未真跑完 → **E2 不授权**(E2 历史窗回测 / E3 forward 线做进 XenoDev = 越界 BLOCK)。

**Follow-up commits**: pending(本 LOG 第 27 条决议入库 · 未 push)· build-ship 产物在 XenoDev-009 `feat/009-spec` 工作树(7 改 + 5 新 · 1054 passed · 未 commit/未 push · push 前需 operator 确认)·
下一活 = operator 真盲标跑 + watchlist 补数(B1)解 E2 解锁条件 ② · codex 补跑本决议已裁定不做(接受 fallback 终态)

## 2026-07-27T07:46:28Z · 009-pM3prime-20260727T065748Z(FU-KG43 · Layer-2 冻结门槛数学不可达 · D-1/D-2/D-3 全采纳 · **operator 领域判断力不足 → D-7「可自任」前提被推翻 · KG-42 重开 · 起 forge v2**)

**Reviewed at**: 2026-07-27T07:46:28Z
**Related task**: FU-KG43
**Tags**: drift, prd-revision-trigger
**Severity**: high
**6 约束自检**: ✅ all 6 PASS(consumer mode · 绝对 realpath · 一次通过)
**verdict-evidence 预检**: n/a(无 `ids_verdict_evidence:` 父键 · 本包零代码改动 · 非 build-ship 包 · 正常)

**IDS 侧独立复核(非转述 build 结论 · 本次 review 实跑)**:
- `gold_layer2.py:mapping_agreement_rate` 用 `m.get(dim) == h.get(dim)` → machine `null` vs human 有值 = 不命中 ✅ 属实
- `evaluate_layer2` 合取**确实**仍保留 `rate >= threshold` 作首项,与新 D-7 五项并列 ✅ 属实(refactor 未清干净)
- `coverage_denominator` = 「非弃权且 gold 有值的计数」→ human 弃权直接压覆盖率 ✅ 属实
- `blind_annotate.py:50-54` `SLA_COVERAGE_THRESHOLDS` sector/horizon = **0.75** ✅ 逐字属实
- SLA.md:28 逐字写「第二源资格从**「输出一致率」refactor 为**逐维双错率 + abstain 覆盖率 + 外证据锚 + 盲标隔离」✅ 属实 → 方向 (a) 理据成立
- **探针实跑 exit=1**,三组理想上界全 `passed=False`;A1 组五维双错率全 0.0 + 覆盖率全达标 + ticker 锚 1.0(D-7 三分离契约满分)仍被粗一致率 0.600 一票否决
- **算术独立验算**:上界 = (3×41 + 10 + 10)/205 = **143/205 = 0.69756 < 0.70**,矛盾差额恰好 1 个弃权名额。**与 operator 标注质量无关** ✅ 成立

**Operator decisions**:
- [ ] 修 PRD §"—"(本次不勾选:D-1/D-2/D-3 均为门槛自洽性修复 · 不触及产品决策 · 走直改 XenoDev spec/SLA。⚠ 但下方「主体缺失」条**将**触发 PRD 层重审,由 forge v2 裁)
- [ ] 修 SHARED-CONTRACT §"—"(不勾选:本包无协议层变更诉求;KG-43 框架缺口走 forge 而非直改协议)
- [x] **修 XenoDev spec/SLA · D-1 采纳方向 (a)**:新契约路(gold 存在)合取**去掉 `rate >= threshold` 项**,legacy 路(gold 缺)保留旧判据兼容 4 个既有旧测。**不改任何 SLA 冻结门槛 → 不碰 C6**。明确**否决 (c) 下调 threshold**(看到过不了才改数字 = 移动球门 = C6 自欺 = V4 失败模式;且擦边过 0.6976 说明该指标已无区分力)
- [x] **修 XenoDev · D-2 采纳**:给 `blind_annotate.py` CLI 补 `--dimension-arbitration-json` 入口(库层 `reconcile()` 已有该参数 · C9 仲裁留痕设计存在 · 能力在入口缺)。解「独立第二源的价值恰在于可能不同,而通过条件是零分歧」的方法论自反
- [x] **修 XenoDev spec §O8 / SLA §Layer-2 · D-3 定义补全**三项:① gold provenance 协议(gold=operator 考据版 / human=operator 盲标版 / machine=`extracted_signals`)② machine 在 sector/horizon **结构性弃权** → 该两维 `double_error_rate` 实测的是 operator 盲标 vs 自身考据的自洽性,**不构成对 machine 映射正确性的验收**(防数字被误读为「机器板块判得准」)③ B5 诚实边界(gold 与 human 同为 operator → 共享盲点;ticker 维靠 watchlist 外锚 + abstain 担独立性;**v0.1 降级验收,非技术保证**)
- [x] **记 KG-43 框架治理 defer 归 IDS forge**:framework 支持「门槛预注册 · C6 不可回改」(强治理,对),但**无任何一道门要求冻结前验证门槛可达**。建议 spec-writer / task-decomposer SKILL 加 feasibility probe 前置(理想上界合成数据跑存在性证明 · 零成本无 LLM)。受益面 = 所有预注册门槛场景(证伪链 / 金标验收 / SLA gate)
- [x] **E2 授权判据复核入库(信息式)**:条件 ② 从 LOG 第 27 条的「harness 就位 · 待真跑」**降级**为「门槛组合不自洽 + 无合格验收主体」→ **E2 仍不授权**
- [ ] 「修完重跑探针证明可达再起盲标」—— **未勾选**(如实记录。IDS 侧建议仍保留,见 Follow-up;但因下方主体缺失,「再起盲标」本身已悬置)

**Operator note**:

**一、D-1/D-2/D-3 决议(门槛层)**——全采纳 build 侧建议,走**直改 XenoDev spec/SLA**,不起 PRD 修订。三项均为「让冻结下来的门槛组合自洽」的修复,不移动球门:方向 (a) 删的是 SLA 自己已声明被 refactor 淘汰的旧指标,五个冻结门槛数值一字不动。

**二、【重磅 · 本次决议的真正重心】operator 补充推翻 D-7 前提 —— KG-42 重开**

operator 在决议中补充:**「operator 不具备标注能力,后续开发要考虑到这点」**,澄清后确认性质为 **「领域判断力不足(全维)」**——对金融新闻的 sector / direction / horizon / timepoint / ticker **五维都没把握**,非「有能力但无时间」,亦非「事实维行解释维不行」。

**这比 D-1 更上游,且方向相反地更坏**:
- D-1 是「门槛在数学上没人能过」;本条是「**即使门槛修好,也没有合格主体产出输入**」。修完 D-1/D-2 让门自洽了,Layer-2 依旧跑不起来。
- forge v1 对 KG-42「无验收主体」死结的解法,原文是「第二源 = 错误独立性代理 · **operator 可自任**(靠独立盲标非领域深度)」,LOG 第 27 条据此判 **「KG-42 死结解」**。该前提现被 operator 本人推翻 → **KG-42 并未真解,只是被 D-7 挪了位置**。
- 连带失效:`[OP-2] 盲标` / `[OP-3] 考据` 两个 judgment gate 无合格主体;**2026-07-25 拍板的 gold 真值协议**(gold=operator 考据版 / human=operator 盲标版)一并失去主体 —— 而该协议本就是 D-7 未闭合的定义缺口(spec/SLA/PRD 三处均未记),现在连主体都没了。
- ⚠ **诚实标注**:D-7 改写的核心论证是「独立性靠**错误独立性**而非领域深度」,这在方法论上仍可能成立(一个领域外行的错误确实与提取器的错误不相关);但**「不具备领域判断力的人产出的标注,其 gold 侧(考据版)本身可信度存疑」**——错误独立性解决的是「不共享盲点」,不解决「gold 本身是否为真值」。这个区分是 forge v2 必须处理的核心。

**处置**:按 CLAUDE.md 铁律「**重大架构转向 → 必须 `/expert-forge`(防 V4 失败模式)**」,**起 forge 009-pM3prime v2 专场**重审 KG-42 验收主体问题。D-1/D-2/D-3 的 spec/SLA 修订**不等 forge**,独立先行(门槛自洽是净收益,且与主体是谁正交)。

**三、build 侧处置认可**:本 fork **零代码改动**,未改任何冻结门槛、未传 `--*-threshold-json`、未代做三个 operator judgment gate、**未向 operator 展示任何机器答案**(`machine.json` 只验长度与非 null 计数;worksheet 只含 `id/source_id/raw_ref/span_start/span_end`)→ **41 条盲标机会完好未损**。四条红线逐条复核未破。**在 operator 投入劳动前用零成本合成探针抓到死锁**,未烧 token、未消耗不可逆的盲标机会 —— 这是「推演 ≠ 真跑」第五次实证中**代价最低的一次**,build 侧判断正确。

**四、方法论沉淀(与 [[forge-verdict-vs-empirical-ship]] 一致)**:本次 drift **不是** build 实装偏离 spec —— `gold_layer2.py` / `blind_annotate.py` 严格实现了 spec 与 SLA 写下的规则,4 轮 subagent-fallback 对抗审也 approve。drift 在于 **spec/SLA 写下的规则组合本身内部不自洽**,而这个不自洽经 forge v1 推演 + operator 批 plan 签字 + build 四轮对抗审,**全程无人验算**。KG-43 正是对这一类失败的框架级回应。

**Follow-up commits**: pending(本 LOG 第 28 条决议 + hand-back 包入库 · 未 push)
- **下一活 ①(不等 forge · 可立即起)**= `cd "$XENODEV_ROOT"`(009 线为 `/home/ys/codes/XenoDev-009`)→ `claude -w 009-pM3prime` 落地 D-1(a) + D-2 + D-3。**IDS 侧建议的验收判据**:改完重跑 `scripts/layer2-feasibility-probe.py` 至 **exit 0**(证明存在一组合法输入使 `passed=1`)—— 即把 KG-43 提的那道门先用在它自己的修复上。该项 operator 未勾选,记为建议非决议。
- **下一活 ②(治理主线)**= 起 `/expert-forge 009`(v2 专场)重审 KG-42:**在 operator 领域判断力不足(全维)的真实约束下,金标 Layer-2 的验收主体是谁 / 是否改非人工验收路(如事后市场真值回标)/ 是否降级为单一事实维 / 或 Layer-2 长期 blocked 并据此重定 E2 解锁条件**。一并带 KG-43(冻结门槛前置可达性验证门)。
- **残留 defer(非本决议 close)**:① watchlist 补权威数据(B1 · 未变 · 红线:严禁本 fork 现填交易所清单可能引 look-ahead;另注 build 侧提醒 —— 若照 gold ticker 反推 curate,外证据锚会退化为同义反复,该清单须来自 operator 外部权威认知)② blind 隔离技术不可证性(B5 · 未变)③ **operator 真盲标产真数字 —— 本条状态变更:从「待真跑」改为「待 forge v2 定主体后重估」**。

## 2026-07-27T10:05:38Z · 009-pM3prime-20260727T065748Z(forge 009-pM3prime **v2** verdict 落地 · operator 选 **[C] 局部接受** · **v1 推论撤销 · KG-42 死结未真解** · PRD v0.6→v0.7)

**Reviewed at**: 2026-07-27T10:05:38Z
**Related task**: FU-KG43(承第 28 条 · 本条是该决议触发的 forge v2 verdict 落地,非新 hand-back)
**Tags**: prd-revision-trigger
**Severity**: high
**6 约束自检**: n/a(本条非 hand-back 包决议 · 是 forge verdict 落地入库 · 沿第 26 条先例)
**verdict-evidence 预检**: n/a

**forge run 摘要**:`discussion/009/009-pM3prime/forge/v2/`(8 round file 齐 · Reviewer A=Claude Opus 4.8 ·
B=GPT-5.6-Sol xhigh · strong-converge · **converged 无 unresolved** · A 侧让步 2 条 · 残余降 4 条 v0.2 note ·
~26 次检索 / ~17 独立源 · **与 v1 零论文重叠**)。stage doc: `stage-forge-009-pM3prime-v2.md`(15,652 字符)。
Phase 4 synthesizer 经 operator 选择**在主进程产出**(未调 forge-synthesizer 子代理)。

**Operator decisions**:
- [x] **修 PRD**(v0.6→**v0.7**)· §4-E1 新增 **🔴 D-7 v2 修订块**(8 条 a-h)+ §7 新增 **🔴 E2/E3 解锁条件修订表**
- [ ] 修 SHARED-CONTRACT §"—"(不勾选:KG-43 是框架级但走 forge 攒批,不直改协议层)
- [x] **记 KG-43 三道门归 IDS forge 006 攒批**(dogfood 铁律:框架级变更只走 forge,不当场改)
- [x] **[C] 局部接受**(见下 Operator note 的三段式处置)

**Operator note**:

**决议 = forge v2 Decision menu [C] 局部接受**,三段式:

**✅ 采纳(否定性结论全落)**
- **(a) 撤销 forge v1「operator 可自任 Layer-2 第二源」推论**。断裂点是**范畴替换**:v1 由
  「`mapping_agreement_rate()` 不含金融逻辑」推出「标注不需领域深度」—— 该函数是**比较器**(只做 `==`),
  标注劳动在于五元组**怎么产生**;且 v1 用以支撑的「事实维可外证据核验」**只覆盖 ticker/timepoint 两维**,
  sector/direction/horizon 三维无任何外锚。**错误独立性解决「不共享盲点」,不产生真值。**
- **KG-42「无验收主体」死结并未真解,只是被 D-7 挪了位置** → **第 27 条「KG-42 死结解」判定作废**
  (本条以新增 entry 记录撤销,不改原 entry · 沿 2026-07-05 F6 撤销先例)。
- **(b) 撤销 07-25 gold 协议的 validity 地位**:`gold`=考据版 / `human`=盲标版 = **同一人两次标注**,
  按 **Krippendorff 信度三分类(stability / reproducibility / accuracy)只测 stability,不测 validity**。
  该数字**在测量理论上不是对 machine 映射正确性的验收**;作 stability 记录可留,不得当 validity 用。
  (v1 契约缺角:D-7 草案详写 human 资格却**从未定义 gold provenance**,而双错率恰相对 gold 定义 → 判据悬空。
  正因未定义,operator 才于 07-25 临时补协议,而**该补丁直接生产了本轮困境**。)
- **(c) 全量五维 Layer-2 作为 correctness gate 在 v0.1 不成立,且不因换主体/调门槛而成立**;
  v1「§2 × Layer-2 非产品级真互斥」的判断**在 correctness 维度撤销** —— 它就是真互斥。
- **(d) E2 解锁条件 ② 拆两条**:②-a 诊断 lane(待定)/ **②-b 回测 lane 明确 blocked(非「待跑」)**;
  含**反自欺条款**(②-a 过不得记作 ② 满足)。
- **(f) 门槛形态修正判据(跨场景通用)**:**看数后下调既有阈值数字 = 移动球门(禁);换形态 +
  新 `caliber_version` 预注册 + 废止旧 pass 语义 = 方法学修正(可);形态改亦不得 retroactively 解锁旧 gate。**
- **KG-43 三道冻结前置门**归 forge 006 攒批:① **存在性证明**(构造理想输入证 `passed=1` 可达)
  ② **真值证明**(验收锚从哪来 / 谁能独立证伪 / 成本是否本 tier 可承受)③ **形态检验**(门槛形态是否合乎
  该问题的标准处理方式 —— 形态错比数字错更难救:数字受 C6 约束尚可版本化修正,形态错则整套预注册语义作废)。

**⏸ 挂起(本次不采纳为既定验收面)**
- **(e) groundedness 降级面** —— forge verdict 主张把 Layer-2 验收对象由 correctness 降为 groundedness
  (**被引原文是否真支撑该五元组** · 只需阅读理解 · 009 引文回锚基础设施已就位 · 归因文献实测高达
  **57% 引文为事后合理化**故非稻草人验收)。**operator 选 [C] 挂起**,理由取自 forge 自身
  §underweights 的自曝:**groundedness 的统计效力两边都没算** —— correctness 侧「41 条 × 门槛 0.05 →
  约 2 条错即翻盘」的问题换成 groundedness 后**原样存在**。
  **解锁前置 = 零成本效力探针须先证明其在 n≈41 上具区分力**;出数字后另行决议。
  若日后采纳,**硬边界必须同时写死**:groundedness 过 ≠ 映射正确 ≠ 有 alpha ≠ 授权回测
  (此条为 Reviewer B 行使复核权时的 binding 条件:边界写不硬则整条 verdict 回退纯 STOP)。

**❌ 本次不做**
- 不改 SLA 门槛数字(**C6 不变**);形态重注册待 (e) 决议后与 groundedness 一并做。
- 不动红线 `gold_layer2.py:203`、gate fail-closed 骨架、E1 US 密度终裁(第 25 条)。

**方法论沉淀(两条,均可复用)**:
1. **「该事实并非新信息」** —— `risks.md` E1-R2 下游注(2026-07-23)已载「operator 无合格金融判断」,
   且该文件**就在 v1 的 X 清单里**。v1 读过并将其重新解释掉。故本轮性质是**裁决 v1 的推论**而非处理新事实
   ——「证据在场却被解释掉」是一种独立于「证据缺失」的失败模式,值得进 forge 006 议。
2. **回声室判据的正面执行** —— 双方 P1 同姿态收敛(已标警报),真正对抗只发生在 P2:
   双方文献**零重叠**(A 走 Krippendorff + Correctness-is-not-Faithfulness;B 走 Snow + FEVER/CFEVER +
   Dorner & Hardt),**各自推翻了自己 P1 的一部分**,再落到同一出路。**本 verdict 的可信度基本全押在 P2 这一环**
   —— 若 P2 检索面有共同盲区,双方会一起错。此为 stage doc §underweights 明载的自曝。

**Follow-up commits**: pending(本 LOG 第 29 条 + PRD v0.7 + forge v2 全产物[8 round file + config + state +
stage doc] + codex 总线 inbox/outbox p1-p3r2 + HEAD · 纯 009 不夹带 001 · 未 push)
- **下一活 ①(解 (e) 挂起 · 优先)** = XenoDev session 跑 **groundedness 效力探针**(零成本 · 判 n≈41 是否具区分力)
  → 出数字后回 IDS 决议是否采纳 groundedness lane。
- **下一活 ②(与本轮正交 · 可并行)** = XenoDev 落地第 28 条已决的 **D-1(a) + D-2 + D-3** 门槛自洽性修复
  (启动 prompt 已备:`scratchpad/XENODEV-startup-FU-KG43-fix.md`;含 IDS review 侧新发现的 O8 验收终点不一致)。
- **残留 defer**:① watchlist 补权威数据(B1 · 未变)② blind 隔离技术不可证性(B5 · 未变)
  ③ **operator 真盲标产真数字 —— 本条状态再降级**:correctness 盲标在 v0.1 已判不成立,
  41 条盲标机会**保持未使用**(全程未泄露机器答案),是否改作 groundedness 用途待 (e) 决议
  ④ **Layer-1 主体问题全程未处置**(门槛仍空 · 不得默认已解)。

## 2026-07-28T02:44:53Z · 009-pM3prime-20260727T130103Z(FU-KG43-fix · 方案 B 追认 · **(e) 重算推翻 indeterminate 框架** · **两维外锚 lane = forge v2 漏评分支** · 不可逆资源排序原则入库)

**Reviewed at**: 2026-07-28T02:44:53Z
**Related task**: FU-KG43-fix
**Tags**: drift, prd-revision-trigger
**Severity**: high
**6 约束自检**: ✅ all 6 PASS(consumer mode · 绝对 realpath · 一次通过)
**verdict-evidence 预检**: n/a(无 `ids_verdict_evidence:` 父键 —— 本包非 build-ship 包形态)

### IDS 侧独立复核(本次 review 实跑 · 非转述 build 结论)

**属实项(逐条实跑复证)**:
- `_CORRECTNESS_GATE_AUTHORIZED_V0_1 = False`(`gold_layer2.py:43`)· `passed = criteria_met and 常量`(`:473`)· 确非入参 ✅
- `gate.py:89` **代码常量优先**,False 即 `return False` 不查库 → DB 三列自签被挡 ✅
- migration 0019 已应用于 `out/e1-census-20260718.sqlite`:两新列在 · `gold_layer2_result`/`_dimension` **均 0 行** · `extracted_signals` 41 条 → 「无旧 pass 语义被 retroactively 解锁」✅
- **41 条信号 / 14 distinct source** 实测属实 ✅(正是翻转探针主结论的那个事实)
- 两支探针实跑 **exit 0**,复现 `indeterminate` ✅
- Wilson 天花板独立闭式验算 `1/(1+1.645²/41) = 0.93809` ✅ → τ=0.95 区间形态在 n=41 **数学不可达**属实,**与 KG-43 同型**
- `0.95⁴¹ = 0.1221` 独立验算 ✅ → 形态 B·τ=0.90 假毙率 87.8% 属实
- 红线 `second_source_kind != 'human' → raise` 存在且未动 ✅(实质属实)
- `blind/machine.json` mtime `2026-07-26 07:55`(早于本次 session)→ 与「41 条盲标机会未损」一致 ✅

**三处不符(build 侧未列 · 本次 IDS 新发现)**:
1. 🔴 **KG-45 在报告 KG-45 的这份 hand-back 里当场复发**:红线实际在 `gold_layer2.py:350`,hand-back §4 写 `:300`;且**代码内注释**仍写「红线(`:203` 不动)」。同一条红线现留下 `:81`/`:203`/`:300` **三个都已失效的行号** → **KG-45 severity 由 medium 上调 high**
2. ⚠️ **ticker 锚 fail-open 只在入口修好**:`blind_annotate.reconcile` 默认 None→0.90 且偏离即 raise ✅,但**库层 `gold_layer2.evaluate_layer2` 默认仍是 `0.0`**(`:302`)—— 绕过 reconcile 直调库仍拿「锚关闭」默认。hand-back 措辞准确(只声称修了 reconcile/CLI),但该残留面未进 §5 defer
3. ⚠️ **基线自相矛盾**:hand-back §1/§4 写 `1130 passed`,同 commit message 写 `1131`。**IDS 实跑 = `1131 passed, 7 skipped, 6 deselected, 1 xfailed`(130.72s)** → commit 对,hand-back 文本错

### 🔴 IDS 侧重算:(e) 的 `indeterminate` 框架不成立(推翻 build 主结论的框架,非其数字)

**发现 1 · `n_eff=14` 不是保守下界,真下界是 8.9**
41 条在 14 个 source 上**极不均匀**:簇大小 `[8,7,4,4,4,3,3,2,1,1,1,1,1,1]`。
build 取 `n_eff = 簇数 = 14` 是**等簇**假设。不等簇须用 Kish 有效簇大小
`m_A = Σm²/Σm = 4.6098`(非算术均值 2.9286)→ `DEFF(ρ=1) = 4.61` → **`n_eff = 8.89`**。
→ **build 声称的「保守端」本身是乐观的。**

**发现 2 · 二元「有/无区分力」判据在格点上抖动,不是稳定性质**
用 build 自己的 `gate_power.discriminates` + 同一套预注册参数(好 0.95 / 中 0.85 / 差 0.70)扫 ρ∈[0,1]:

| n_eff | 对应 ρ | 好 vs 中(**验收门**) | 好 vs 差(**粗筛**) |
|---|---|---|---|
| 41 | 0.00 | J=0.7347 · **True** | J=0.9776 · True |
| 35 | 0.05 | J=0.6954 · **False** | J=0.9659 · True |
| 30 | 0.10 | J=0.6608 · **True** | J=0.9542 · True |
| 27 | 0.14 | J=0.6421 · **False** | J=0.9361 · True |
| 21 | 0.28 | J=0.5619 · False | J=0.8955 · True |
| 14 | 0.55 | J=0.4903 · False | J=0.8091 · True |
| **8.9** | **1.00** | J≈0.39 · False | J≈0.69 · **False(临界)** |

True/False 在 41→35→30→27 之间**来回翻** = 整数临界计数相对两个概率门(0.80/0.20)的**格点落位**,非样本量的真实性质。
→ hand-back 报的「n=41 有 / n_eff=14 无 → 取决于同源相关性」**有相当部分是格点假象**。

**发现 3 · 换连续量看,结论不是 indeterminate,而是两个用途各有明确答案**
- **验收门用途**:ρ≳0.14 即失效,且 ρ<0.14 区间内仍在闪。同源文本(同一场直播/同一篇文章,引文风格与截断模式一致)ICC 通常 0.2–0.5 → **要求 ρ≲0.14 不现实** → 实质是**否**,非「不确定」
- **粗筛用途**:J 从 0.98 到 0.69,`discriminates=True` **一直撑到 ρ=1**(n_eff=8.9 才临界)→ 实质是**稳**,全 ρ 区间成立

**两个答案恰好落在 PRD v0.7 已有的 lane 切分上**:②-b 需 correctness 验收门 → groundedness 给不了(与 frozen (c)/(d) 一致);②-a 需粗筛/诊断 → groundedness 给得了,且 ρ=1 最坏情形仍成立。

**发现 4 · build 建议的「先补聚类相关性实测」多余且不可行**
- **多余**:粗筛在 ρ=1 都成立,验收门在 ρ=0.14 就死 —— **两个结论都不依赖 ρ 的精确值**
- **不可行**:groundedness 误差 ICC 需 **groundedness 标注结果**才能算,而那正是尚未产生的东西。build 写「本仓有 41 条的 source 归属,可直接算」—— 可直接算的是**簇结构**,**不是误差相关性**,两者被混为一谈

> ⚠️ **诚实边界**:以上建立在 build 预注册质量档(0.95/0.85/0.70)与 `discriminates` 判据(P(pass|好)≥0.80 ∧ P(pass|差)≤0.20)之上,档位设错则结论移动。Kish DEFF 是标准近似非精确。ρ 本身仍未知 —— 论证是「不需要知道」,不是「知道了」。**本重算是推演不是真跑。**

### 🔴 IDS 侧发现:第 28 条交 forge v2 的两个备选出路,一个已答、一个**漏评**

第 28 条下一活 ② 明确让 forge v2 审:验收主体是谁 / **是否改非人工验收路(事后市场真值回标)** / **是否降级为单一事实维** / 或长期 blocked。

- **① 事后市场真值回标 —— forge v2 答了,且否定。** Evidence map 载:「事后市场回标验 alpha 与市场反应,不验原文→五元组映射 · P2-GPT(StockNet 等)· "outcome 不能证明映射 gold 正确" · 无反对证据」。理由成立(市场结果混淆「抽取保真」与「信号有无 alpha」)→ **本条路正式关闭**
- **② 降级为单一/少数事实维 —— forge v2 未作为选项评估。** 它只以对 v1 的批评形式出现:§134「v1『事实维可外证据核验』**只覆盖 ticker(watchlist 外锚)与 timepoint(`published_at`)两维**」· §295 v0.2 note 4「该问题在方法学上无解,**只能靠外锚绕开,而外锚只覆盖两维**」。**forge v2 写下了「唯一出路是外锚」,却没去评估那个出路**,verdict 直接转向 groundedness;Decision menu 无两维 lane。
  - **关键读法**:PRD v0.7 (c) 冻结原文限定「**全量五维** Layer-2 作为 correctness gate 在 v0.1 不成立」→ **两维 gate 未被 frozen PRD 排除**
  - **该路绕开了杀死 D-7 的约束**:ticker 对权威 watchlist、timepoint 对 `published_at` **都是查表不是判断** → 不需 operator 领域判断力、不消耗 41 条盲标机会、可全自动
  - **弱点须同时记明**:两维不验 **direction**(交易信号最核心维)→ **大概率仍不足以解锁 ②-b**;卡 B1 权威 watchlist;现行 ticker 锚只核 **gold 的** ticker 不核 **machine 的**,当 correctness gate 用须掉转锚方向

**Operator decisions**:
- [ ] 修 PRD §"—"(不勾选:本轮无产品决策变更;(e) 拆用途采纳落在 PRD v0.7 已有的 ②-a/②-b 切分内,不需改 PRD)
- [ ] 修 SHARED-CONTRACT §"—"(不勾选:本包无协议层变更诉求)
- [x] **追认方案 B**(判据层 `criteria_met` / gate 层 `passed` 分离 + 授权单一真相 = 代码常量恒 False)· **并显式记账两项代价**(见 Operator note 一)
- [x] **§3-1b 解锁制品设计归 forge 006 攒批**(治理层语义 · build 不自决 · spec §O8 注块 ⑥ 已写死「翻常量不是合格解锁设计」)
- [x] **(e) 决议 · 拆成两半**:① **分析结论现在定死**——groundedness 作 ②-a **粗筛/诊断用途采纳**(ρ=1 仍稳)· 作 correctness **验收门用途否决**(需 ρ≲0.14 且格点抖动)· **不补 ρ 实测**(不必要且标注前不可行)② **资源动用(拆封 41 条)拆出,挂三道前置**(见 Operator note 三)
- [x] **两维外锚 lane · 授权零成本可行性探针**(合成数据 · 不消耗盲标机会 · 出数再决采纳;须一并回答 `published_at` 外锚独立性问题)
- [x] **B1 权威 watchlist 由长期 defer 提为当前任务**(查资料非判断 · 在 operator 能力范围内 · 两维 lane 卡它;红线不变:严禁照 gold ticker 反推 curate)
- [x] **F3 采纳 ②-a 降级**(契约升级前不产出被下游消费的 `criteria_met` · 旧 ②-a 结果行不得追认)+ **F3 拆做**:③ 先做,①② 视阶段 0-1 结果再定
- [x] **追认第 28/29 条冲突读法**(gold 协议照写入 spec §O8 作操作性定义,同写死只测 stability 不得当 validity 用 —— 唯一不自相矛盾读法)
- [x] **Layer-1 主体问题正式立案**(不再默认 defer · 只需回答一个问题:**它要不要用这 41 条盲标机会**)
- [x] **KG 分流入库**(不全塞 forge 006 议程 · 见 Operator note 五)
- [x] **记 IDS 复核发现**(三处属实项 + 三处不符 + 本次重算四项发现)
- [x] **E2 授权判据状态更新(信息式)**:**E2 仍不授权**

**Operator note**:

**一、方案 B 追认 —— 附两项代价记账**

追认。理据成立:它把 frozen PRD v0.7 (c)/(d) 从**文档条款**变成**代码不变量** —— 此前 ②-b blocked 实际依赖「Layer-1 恰好为空」这一**暂态**(是运气不是保证),现在无论标得多好、无论谁写库,gate 都不开。方向严格加严无放松面;C6 五个冻结值 IDS 实测未动;gold 表 0 行无追溯解锁面(合 forge v2 (f))。且它是 forge v2 (c) 文献论证的**代码层独立实证**,两条零重叠路径收敛 —— 本轮可信度最高的一条结论。否决会更糟(让 `passed=1` 可达 = 直接违 frozen PRD)。

**但两项代价显式记账,不默认吞下**:
1. 🔴 **这是 build 侧在 review 压力下当场做的决议**,而铁律写「重大架构转向 → 必须 `/expert-forge`」。追认 = 事后授权一次绕过 forge,**立了「build 自判某改动属于『实现已冻结条款』→ 可当场做」的先例**。本次判断对,但该自判边界模糊,**下次可能被用在更松的地方**。归 forge 006 一并议(与 §3-1b 同批)。
2. 第 28 条 IDS 原话「证明 `passed=1` 可达」被重述为「证明 `criteria_met=1` 可达」—— **验收判据被 build 单方面换了对象**。新对象是对的,但换这件事本身留痕。

**二、本轮决策的主导原则 —— 不可逆资源排序(可复用)**

把全部待办按**能否反悔**分类:可反悔的(改代码 / 跑探针 / 修防伪造 / 补 watchlist / 写文档)vs **不可逆的(41 条封存盲标考卷 —— 全局唯一一项)**。

> **原则:所有廉价、可反悔的信息先拿到手;不可逆的一步放到最后,等它成为唯一剩下的问题时再动。**

这是**期权思维**:41 条是一个期权,不该在决定其价值的廉价信息到齐前行权。而本轮恰有一个**可能彻底改变其价值**的廉价信息 —— **两维外锚探针**:若两维 lane 可行,即拿到一个不需判断力、不需拆考卷的验收锚,groundedness 从「唯一的路」降为「锦上添花」,**而 41 条仍未拆封**。

→ **故两维探针必须跑在拆封之前。**

**三、(e) 为何拆成两半**

「41 条够不够用」是**事实判断**(不会变,现在定死);「现在要不要花掉它们」是**资源决定**(会变,等信息到齐)。原决议把两者搅在一起。

**拆封 groundedness 标注的三道前置**(全部满足方可动手):
1. 两维外锚探针出数 ✓
2. Layer-1 立案并确认**不需要**这 41 条 ✓
3. F3 防伪造修好 ✓

**该前置零额外成本** —— F3 本来就必须先做(且顺序是硬约束:F3 必须严格先于 ②-a 实跑,否则标完再改格式,身份绑定得重做),那段时间窗天然存在。

**⚠️ 拆封的真实代价须记明**:groundedness 标注**必须看到 machine 答案** → 看过之后这 41 条**永远**不能再做独立盲标。而 Layer-1 门槛仍空、从未被任何一轮正面处置 —— **在未确认 Layer-1 需求的情况下拆封 = 在未知需求上做不可逆消耗**。这是本轮最需警惕的一点,也是 Layer-1 立案的直接动因。

**四、执行排序**

- **🟢 阶段 0(现在 · 零成本零消耗 · 可并行)**:追认方案 B + 记账 · **跑两维外锚探针** · **B1 提为当前任务** · 追认 28/29 读法 · 记 IDS 复核发现
- **🟡 阶段 1(必须在拆封前)**:Layer-1 立案 —— 只答「要不要这 41 条」
- **🟠 阶段 2(可反悔 · 必须先于标注)**:F3 ③ 先做(验收程序从 DB 规范化加载 machine,不再信任外部 JSON —— 纯收益:减一个不该有的信任面 + 板块/周期两维恒 null 由 DB 天然保证);F3 ①② 改格式**视阶段 0-1 结果再定**(①② 会导致 `blind/machine.json` 须**重新生成**→ 需重跑提取器,该连锁成本 hand-back 未标价,只在确定要拆封时才值得付)
- **🔴 阶段 3(三道前置齐全后)**:groundedness 标注(拆封 41 条)

**五、KG 分流(防 forge 006 攒批消化不良)**

006 攒批已含 KG-5/B11/B12/38/41/43,再无差别加塞会变成大杂烩。按**需不需要 forge 级讨论**分流:

| 归 forge 006 议程(**需讨论**) | 直接进检查清单(**照做即可 · 不占议程**) |
|---|---|
| KG-43 三道冻结前置门(存在性/真值/形态) | **KG-45** · 别用行号锚定代码红线,改用文件+稳定标识符/测试名(severity **上调 high** · 本次当场复发,三个失效行号) |
| **KG-44** · 区间/置信下界形态在小样本上的天花板陷阱(**前瞻性最高** —— 能拦住 forge v2 自己的改点 4 重蹈 KG-43) | **新** · 不等簇场景**别拿簇数当有效样本量**,须用 Kish `m_A = Σm²/Σm`(本次 build 因此把保守端 8.9 误报为 14) |
| **新 · 元层** · **forge 写下了自己的出路却没去评估它**(v2 §295 自陈「只能靠外锚绕开」→ 未评两维 lane;与第 29 条「证据在场却被解释掉」同族,属独立于「证据缺失」的失败模式) | **新** · 二元「有/无区分力」判据在格点上会抖(True/False 在 n=41/35/30/27 间来回翻),**不可直接当结论**,须看连续量(Youden J) |

**六、诚实预期(防「以为解开了、其实只是挪了位置」)**

**会得到**:可信的诊断能力(分辨好机器 vs 烂机器)· 可能一个局部的、不需判断力的验收锚(两维)· 一份权威 watchlist(对后续都有用)· 代码层焊死不会被误开的门。

**不会得到**:❌ **E2 回测仍解不开。桌上现在没有任何一条路能解开它** —— 两维 lane 即便成立也验不了 **direction**(最要紧的维)。

**本方案的诚实定位 = 把地基做扎实、把不可逆的牌留在手上,不是解锁 E2。若目标是「尽快开始回测」,按现有约束没有诚实的快路。**

**七、E2 授权判据状态(信息式)**

- ① 真密度显著:**US ✅**(决议 25)· CN/HK ❌ STOP
- **②-a 诊断 lane**:**分析结论已定**(groundedness 粗筛可用)· **实跑挂三道前置**(见 Operator note 三)· ⚠ 反自欺条款不变:②-a 过**不得**记作条件 ② 满足
- **②-b 回测 lane**:🔴 **blocked**(不变)· 现为**代码不变量**,不再依赖「Layer-1 恰好为空」暂态
- ③ operator 授权:❌
- **④ Layer-1**:🆕 **正式立案**(门槛仍空 · 不得默认已解)

→ **E2 仍不授权。** E2 历史窗回测 / E3 forward 线做进 XenoDev = 越界 = BLOCK(不变)。

**Follow-up commits**: `c35cf2f`(2026-08-11 · 本 LOG 第 30+31 条 + PRD v0.7→v0.8 + 2 hand-back 包同一 commit · 纯 009 不夹带 001 · **未 push**)。⚠ 本条「两维外锚 lane」分支已被第 31 条撤销(前提 §134 事实错误),该 commit 同时承载撤销记录
- **阶段 0 下一活**(可并行)= `cd /home/ys/codes/XenoDev-009` → `claude -w 009-pM3prime`:① 跑**两维外锚可行性探针**(含 `published_at` 外锚独立性核查)② **B1 权威 watchlist** 补数据(红线:严禁照 gold ticker 反推 curate)
- **阶段 1** = **Layer-1 立案**:答「Layer-1 要不要这 41 条盲标机会」——**该问题未答前不得拆封**
- **阶段 2** = F3 ③(machine 从 DB 规范化加载);①② 待阶段 0-1 结果
- **阶段 3** = groundedness 标注(三道前置齐全后方可动手)
- **归 forge 006 攒批**:KG-43 三道门 · KG-44 · **新增元层条**(forge 漏评自身写下的出路)· **§3-1b 解锁制品设计** · **build 当场决议自判边界**(本条第一项代价)
- **进检查清单(不占 forge 议程)**:KG-45(上调 high)· Kish 有效簇大小 · 二元区分力判据格点抖动
- **残留 defer**:① blind 隔离技术不可证性(B5 · 未变)② `blind/machine.json` 旧格式须按新契约重新生成(不代为回填 ID)③ **`evaluate_layer2` 库层 `ticker_anchor_coverage_threshold` 默认仍 0.0 的残留 fail-open 面**(本次 IDS 新发现 · build 未列)

## 2026-07-28T16:04:41Z · 009-pM3prime-20260728T035015Z(阶段 0+1+2 · **两维 lane STOP 并撤销第 30 条该分支** · **Layer-1 结论收窄:41 条不是 recall 框、而是唯一已物化 precision 框** · **F3 ③ 评审 CONCERNS:自称「纯收益」实含一条新 fail-open** · KG-45 在 IDS 语料 39 处失效)

**Reviewed at**: 2026-07-28T16:04:41Z
**Related task**: stage-0-1-2
**Tags**: drift, prd-revision-trigger
**Severity**: high
**6 约束自检**: ✅ all 6 PASS(consumer mode · 绝对 realpath · 一次通过)
**verdict-evidence 预检**: n/a(无 `ids_verdict_evidence:` 父键 —— 非 build-ship 包形态)

### IDS 侧独立复核(本次 review 实跑 · 非转述 build 结论)

**属实项(逐条实跑复证 · 无一不符)**:
- **forge v2 §134 事实错误属实**:v2 第 134 行原文「只覆盖 ticker(watchlist 外锚)与 timepoint(`published_at`)两维」;而 frozen `SLA.md` Layer-2 逐维门槛表 timepoint 行「外证据锚」列写的是 **「无(published_at 客观)」** ✅
- **Q4 管线恒等**:IDS 侧**自行跨库 join 真 `collection.db`(9,081 条)** → `extracted_signals.published_at` vs `records.published_at` **逐字节相同 41 · 不同 0 · 无匹配 0** ✅。代码链亦证:`_V2_FORBIDDEN_FIELDS` 含 `content_published_at`(即便带 null 也算 schema drift),`extractor.py` 引文制强制 `content_pub = published_at` 显式忽略 LLM 值
- **C 组张冠李戴**:IDS **独立跑探针**(exit 0)→ C 组 `criteria_2d_met = True`,两维覆盖率均 `1.0000` ✅ —— 逐条换成 watchlist 内别人的 ticker(相对 gold 100% 错)判据仍全过
- **KG-44 天花板**:IDS **闭式独立验算**全部吻合 —— n=41→`0.93810`;Kish `m_A = Σm²/Σm = 189/41 = 4.6098` → `n_eff = 8.894` → `0.76676`;ticker 簇 `m_A = 171/41` → `n_eff = 9.830` → `0.78418`。临界计数手算 Wilson 下界逐个复现:τ=0.85→k≥39 · τ=0.90→**41/41 零容错** · τ=0.95→**永不通过** ✅
- **真盘簇结构精确一致**:source `[8,7,4,4,4,3,3,2,1×6]` · ticker `[10,5,3,3,2,2,2,2,1×12]` · 41 信号/14 source/20 ticker · `gold_layer2_result`/`_dimension` 均 0 行 ✅
- **Layer-1 worksheet 泄露证实**:`.gitignore:91` 注释「不含任何答案(只有 id/source_id/raw_ref/**span**)」括号自曝;worksheet.txt **确被 git 追踪**,43 行 = 2 表头 + 41,列含 `span_start`/`span_end`;`machine.json` 则正确被 ignore ✅
- **recall 恒真数学内核成立**:`span_prf` 中 `recall = |gold∩pred|/|gold|`,`gold ⊆ pred ⇒ 恒 1.0` ✅
- **Layer-1 无生产调用方**:`evaluate_layer1`/`krippendorff_alpha`/`span_prf`/`pred_spans` 全仓仅测试触及;census 库 `gold_layer1_result` **0 行**(从未真跑)✅
- **红线 7 条全绿**:`gate.py` **不在 diffstat**(零改动)· `_CORRECTNESS_GATE_AUTHORIZED_V0_1 = False` 未动 · human 硬约束 raise 原样 · C6 五个冻结值一字未动 · 探针四组 `gate_passed` 全 False ✅
- **库层 fail-open 收口**(第 30 条残留 defer ③):默认 `0.0 → None`,缺参即 raise ✅
- **基线**:IDS 实跑 **`1184 passed, 7 skipped, 6 deselected, 1 xfailed`**(131.70s)· 评审侧再独立复现两次(122.75s / 124s)= **三次一致** ✅。⚠ 第 30 条那种「hand-back 文本 vs commit 数字打架」**本次未复发**
- **测试数 9/6/12/20 全对**(20 经 parametrize 展开)· migration 0020 **0 处 ALTER** 只 CREATE · `resolve_ticker_market` 确与 004 UI 的 `replace_watchlist` **同一张 `watchlist` 表**(双重用途冲突属实)· 004 `parse_watchlist_csv` `_HARD_LIMIT = 100` 属实 ✅
- **框架级未当场改** ✅:KG-46/47/48 记入 `dogfood-backlog.md` 攒批回 IDS

**IDS 侧新发现(build 未列)**:
1. 🔴 **KG-45 在 IDS 治理语料里比 build 报的严重一个量级**。build 只数了 `:81`/`:203`/`:300` 三个失效行号、且只修了 XenoDev 那一处代码注释。IDS 全仓扫 `discussion/`:**39 处**用 `gold_layer2.py:81` 或 `:203` 指这条红线,散在 **17 个治理文件**,其中 **PRD.md 占 5 处**(3×`:81` / 2×`:203`)。**真实位置是 `gold_layer2.py:358`,这 39 处无一有效。** ⇒ 行号漂移的**重灾区在 IDS 不在 build**,而 PRD 是 L3 后的 source of truth,是未来读者真正会跟的指针
2. 🟢 **Layer-1 泄露面比 build 描述的窄一档**(唯一的好消息):`.gitignore` 那条豁免的立论前提是「operator 在 git diff / **远端页面**就会看到答案」;实查 worksheet.txt 入库 commit `2579736` **未 push 到任何 remote**(`git branch -r --contains` 为空)⇒ span 从未上过 GitHub,暴露面**只限本地**。不改变裁定(recall 恒真那条理由与泄露无关),但缩小善后范围
3. ⚠ **IDS 曾提「28 源零 key 框」并被评审推翻(记此以留痕)**:数字全属实(120 抽样 → 102 真过提取器 → 14 有信号 / 28 只产 typed rejection / **60 完全静默**),但**推论错**:那 28 源里 116/126 是 `sector_only` = **句子被找到了只是口径判不合格**,把 pred 定义成「仅 accepted」会把正确的口径拒绝记成漏检 = 41 条框的**镜像退化**;`pred=∅` 的框上 `recall ≡ 0.0` 恒真 ⇒ **完美提取器必然 STOP**。**把「恒 1.0」换成「恒 0.0」不叫让 recall 可测**

### Operator 决议(4 问 · 全选推荐项)

- [x] **① 两维外锚 lane → STOP · 并撤销第 30 条该分支**。据:forge v2 §134 把 `published_at` 当外锚是事实错误(frozen SLA 写「无」)⇒ 第 30 条据 §134 立的两维分支**前提不成立** → 作废,与第 29 条撤销 v1 推论同处理法
- [x] **② Layer-1 不要那 41 条 · 但先查零 key 路**。不接受 build「必须烧 key」的成本结论,前置 = 先把 `pred_spans` 定义写下来
- [x] **③ 补 subagent fallback 评审后再落地**(codex 配额墙至 2026-08-02,不等)
- [x] **④ 框架级先入库 · 攒批不起 forge**。据:009 主线(Layer-1 契约 + 抽样框)未定,现在起 forge 会重演「在事实未齐时开会」
- [ ] 修 SHARED-CONTRACT(本次不动)

### 🔴 cross-model fallback 评审结果(3 路并行 · 决议 ③ 的执行)

**评审 A · 库层 anchor 门槛必填 → PASS**(build 声称成立)
AST(非 rg)枚举全仓 **32 个 `evaluate_layer2` 调用点**逐个分类 → **零遗漏调用方**;含 `**kwargs` 间接路(17 个 `_evaluate` 调用)与动态派发均查过。guard 不可绕:`gold is not None` 后到 `:458` 之间**零 `return`**;raise 早于 DB 写入(`:504`)**无半写**。**跑了 mutation 验齿**:默认值注回 `0.0` → 回归测 `DID NOT RAISE` 变红,门有齿。
⚠ **揪出 hand-back 一处措辞误导**:§4-2(a)「显式传 `0.0`(关锚)仍然合法」**只在库层成立** —— 经 `reconcile`(生产入口)传 `0.0` 是**被拒的**(`blind_annotate.py:422-431`)。两句不点明分层即打架。
两条 LOW:anchor guard 与两个同族 guard 隔 76 行未并置(未来插 early-return 会静默恢复本次关掉的 fail-open,且现有回归测抓不到);探针 `two-dim-anchor-probe.py:136` 自带一份 criteria 副本,不继承未来加严。

**评审 B · recall 恒真论证 → SOUND-BUT-CONDITIONAL(build 结论过宽)**
- 数学内核成立,唯一反例 = 空 gold(`gold=[] ⇒ recall=0.0`),方向 fail-closed 良性
- **隐藏前提**:`gold ⊆ pred` 只在「**逐条核验那 41 个 machine span**」读法下成立。改读那 14 个源记录独立标 span 则不成立 —— 但**换个方式坏掉**:exact-match 下差 1 字符即 0 分,recall 波动来自**边界抖动**而非漏检,同样测不到 O7
- 🔴 **precision 没有对偶问题,build 整个漏了**。实测 `gold ⊊ pred` 时 precision = 0.25/0.5/0.75/1.0 **完全可证伪**。且对称:**恰恰是杀死 recall 的那个读法让 precision 完美成立** —— gold = 判为真的那些 machine span,逐字节同源 ⇒ exact-match 天然满足 ⇒ `precision = |真|/41` **就是接受集的假阳性率**
- ⇒ **结论须收窄**:41 条**不可用作 recall 框 / 不得走 `evaluate_layer1`**;但它是**目前唯一已物化的 span precision 框**。build 写成「Layer-1 不需要那 41 条」过宽
- 🔴 **真正的危害在「走 `evaluate_layer1`」**:`gold_layer1.py:133-137` 把 P 与 R 和**同一个** `prf_threshold` 做 AND、`gate.py:109` 只读 `passed` ⇒ recall≡1.0 那半边假数会写进审计表并让 gate 以为两项都过。**Layer-2 有代码硬闸(授权常量恒 False),Layer-1 没有对应硬闸 —— 它是两道门里软的那道**
- **build 成本论断被实证推翻**(与 IDS 那条错推论殊途同归):存在**零 LLM 成本的正确 recall 框** —— 在**已普查的 102 条记录**上抽样标 gold,pred = **已物化的 41 个 accepted span**;14 源外每条记录贡献 0 个 pred span,在 accepted-span 定义下这是**正确**不是缺失 ⇒ `recall ∈ (0,1)` 真可证伪。build 提的「另抽 9081 里没碰过的 + 重跑提取器」是不必要开销
- ⚠ **两条路撞同一堵墙 = exact-match**。`span_prf` 不提供 overlap/IoU 也不提供句子级单元 ⇒ **换抽样框治不了,根因是判据形态**。与 KG-43「数字 vs 形态」同族;build 提的「正确抽样框」会继承同一抖动污染
- 回归测 `test_should_always_return_perfect_recall_...` 名含 "always" 却只跑 4 个前缀实例,且 `range(1, len(pred)+1)` **恰好排除 k=0** = 全称命题唯一反例
- `blind/machine.json` **不含 span 偏移**(只有五维 keys)⇒ 那 41 条**作为已封装制品是 Layer-2 映射资源,不是 Layer-1 span 资源**;build 理由 (b) 方向对但没锚到这个制品级事实
- 三条 build §4-4 未列的遗留:① `evaluate_layer1` 缺 frame-type 守卫 ② 空 gold → recall=0.0 → **完美提取器必 STOP** ③ 41 条中 **34/41(83%) 弱锚**,即便当 precision 框 pred 自身引文质量亦待抽查

**评审 C · F3 ③ 位置约定 → 🔴 CONCERNS(72/100 · 需修订后再合)**
**推翻 build「纯收益」的自我定性。** 净收益仍为正(封死「陈旧/篡改 payload 被静默采信」+「sector/horizon 靠调用方自觉」两个真实面;且顺带让现行缺 `source_id` 的 `machine.json` 重新可用 = **解阻**,build 自己没说透),但**不是 strictly a tightening**:
- **R1(HIGH)· 同 source 内错配今天已无任何检测器**,比 build 自述的「仍不能证明」更差。四道关逐条失效:`_assert_source_id_alignment` 同 source 字符串相同 → 换位全过;双错率因 gold≡human(同一 operator)恒 0;覆盖率/ticker 外锚置换不变;`_has_unresolved_conflict` 只看 `direction`/`timepoint` 两维,而 **`timepoint ≡ published_at`、同 source 全相同 ⇒ 结构性失明**,只剩 direction 一维且一条维度级仲裁留痕即清空。**合成实证**:同 source 换位 + 一条仲裁 → `criteria_met=True`(agreement 0.3333)。**暴露面 35/41 个位置(85%)落在多信号桶内**,单桶最大 8 条。今天**不是坏的**(已实证 worksheet 行首整数序列 == `ORDER BY id` 序列),属 latent
- **R2(HIGH)· F3 ③ 亲手引入的新 fail-open**:被评分的 machine 答案从**冻结文件**变成 **reconcile 时刻的可变 DB 表**,而证明隔离时序的 `machine_extracted_at` 仍是**调用方自报字符串**,与实际加载的行**零绑定**(`extracted_signals.created_at` 存在却从未被 SELECT)。**实证**:把全部 `created_at` 改成机器早于盲标,自报串照旧 → `criteria_met=True`,时序关毫无察觉
- **R3(MEDIUM)· `assert_machine_payload_matches_db` 对 payload 形状不 fail-closed**:键名大小写不同 / payload 写成 dict 而非 list / 41 个空对象 —— **三种都 ACCEPTED 且零字段被核对**。无数值后果(最终恒用 DB 值),但**语义有害**:一份键名写错的陈旧文件拿到绿灯,operator 会读成「已被核验」= D-1(a)「留一个必填却无效的 flag」同型缩微版
- **R4(MEDIUM)· 三方绑定实为两方 + 一个恒真式**,且两处 docstring 现在为假(「三方身份绑定」/「三份 JSON 的 ID 全部来自调用方」);`test_should_reject_when_machine_order_shuffled` 仍绿但守的已不是它自称的那道关
- **R5(MEDIUM)· `signal_id` 算了但从不落库** ⇒ 真跑 41 条后无字段能回答「位置 k 上被评分的是 DB 哪一行」,**错配一旦发生连事后取证材料都不存在**,而这是一次性资源
- R6-R8(LOW):产 `--source-ids` 无脚本无 runbook 且「顺手那条 SQL」因走覆盖索引给出**非 id 序**(R1 的投递向量);只按 `caliber_version` 过滤不含 `extractor_variant`;库层非 Mapping 元素抛 `AttributeError` 而非 `BlindIsolationError`
- **排除项(确认做对)**:`ORDER BY id` 在场且必要(实证裸扫描会走索引给非 id 序)· 0 行 → raise 不静默造空 · 多重集(非集合)对账对 14/41 形态是对的选择 · payload 多给 `sector` 被挡 · 相关契约测 45 passed

**评审过程副作用(已处置)**:评审 C 探测时 SQLite 在 `projects/004-pB/data/` 下新建 0 字节 `e1-census-20260718.sqlite`(真 DB 在 `out/`),**IDS 侧已 `rm`**;真 DB 完好(450560 字节 · mtime 未变)。仓内无代码引用 `data/e1-census-*`,无功能影响。

### 决议后果与待办

**A · 两维 lane(已裁 STOP)**
- 第 30 条「两维外锚 lane = forge v2 漏评分支」一条**作废**(前提 §134 事实错误)。⚠ 第 30 条其余内容不动(append-only:本条以新增 entry 记录撤销,不改原 entry)
- **明确不暗示 E2 可解锁**:桌上仍无任何一条路能解开 E2(两维即便成立也验不了 direction)
- Q3 锚方向:**不落地**。若日后要保留该能力,推荐 `gold ∧ machine` 形态(纯加严);现状 `gold → machine` **非纯加严**(gold miss 而 machine 命中时覆盖率反升),且撞 frozen spec §O8 D-3 注块 ⑥ 与 SLA,**非 build 可自决**

**B · Layer-1(裁定收窄 · 与 build 建议不同)**
- **41 条不得用作 recall 框、不得走 `evaluate_layer1`**(recall 恒真 + P/R 与单一门槛 AND 会污染审计表)
- **但保留其 precision 框地位** —— build「Layer-1 不需要那 41 条」过宽,不整体采纳
- **零 key 路已找到**:102 条已普查记录 + 已物化 41 accepted span ⇒ `recall ∈ (0,1)` 可证伪、零 LLM 成本。**build 的「必须烧 key」成本论断不成立**
- 🔴 **但换框治不了根因**:`span_prf` 的 **exact-match 形态**才是根因,须先决定放宽匹配(overlap/IoU)或改句子级单元 —— 这是 **KG-43「数字 vs 形态」的 Layer-1 同族实例**
- **Layer-1 α 契约缺角仍未解**:unit/label 空间从未定义 + `pred_spans` 定义未写 + 无生产调用方 + **无代码硬闸**。**冻结 Layer-1 门槛前必须先定义**,否则重蹈 KG-43「冻结了一个没定义清楚的门」

**C · F3 ③(CONCERNS · 修订后再视为验收)**
- **R1 止血**(强制 `source_ids` 序列 == `ORDER BY id` 序列)+ **R5**(`signal_id` 落库)= **拆封 41 条的前置**。理由:R5 意味着错配发生后连取证材料都没有,而这是一次性资源
- **R2** 建议同批修(1-2h · 不碰 payload 格式);⚠ 须先确认 `extracted_signals.created_at` 语义是否可用作提取时点锚(它是**普查时刻**不是提取时刻)—— 若不可用,正解改为**在契约里明写「时序关是自报的」**而非加代码
- R3/R4 文档与形状校验一并修;R6-R8 可后置

**D · 知悉项(3 条 build 提 + 1 条 IDS 补)**
- forge v2 §134 事实错误(已据以撤销 A)· `watchlist` 双重用途冲突(**operator 在 004 UI 增删关注股会静默改变金标验收结果**;彻底解需分表 → 会破坏「补数后零代码解锁」,**交后续定**)· `.gitignore` 「什么算答案」须按层重新界定(**Layer-2 的答案 ≠ Layer-1 的答案**)
- **IDS 补**:泄露仅限本地(未 push),善后范围小于预期

**E · 归 forge 006 攒批(本次不起 forge)**
- **新增 KG-46**(「外证据锚」缺独立性验证门 —— 一个由同一条管线回填的字段被当外部证据用了三轮)· **KG-47**(「答案」定义按当前关注的那层写死 → 盲标隔离对另一层静默失效)· **KG-48**(验收指标的抽样框可让指标恒真 = KG-43 门族第四道)
- **KG-45 再升级实证**:IDS 语料 **39 处失效行号 / 17 文件 / PRD 占 5 处**。⇒ 该条已从「注释卫生」升为**治理语料 SSOT 指针失效**,建议 forge 时把「行号锚禁令」写进 SHARED-CONTRACT 而不只是检查清单
- 既有攒批不变:KG-43 三道门 · KG-44 · KG-41 · 元层条(forge 漏评自身写下的出路)· §3-1b 解锁制品设计 · build 当场决议自判边界

**F · PRD 修订触发(tags: prd-revision-trigger)**
- PRD v0.7 需改三处:① §208/§250 转述 forge v2「外锚覆盖 ticker 与 timepoint 两维」= **已证伪**,须加订正块 ② 5 处 `gold_layer2.py:81`/`:203` 失效行号 → 改**无行号锚**(文件+函数名+常量名+回归测名)③ Layer-1 段须记入「41 条 = precision 框非 recall 框」与「α/pred_spans 契约缺角未解」

**Follow-up commits**: `c35cf2f`(2026-08-11 · 本条决议 + 第 30 条 + **PRD v0.7→v0.8 三处修订全部落地**(订正块 / 5 处行号锚清零 / Layer-1 段)+ 2 hand-back 包 · 评审结论已内含于本 entry · **未 push**)。
⚠ 订正:本条原写「3 hand-back 包」实为 **2 包** —— 第三个 `20260727T065748Z` 早在 `f4802f9`(第 28 条)已入库,非遗漏。
**尚未入库(去向已定)**:KG-46/47/48 → forge 006 攒批(`dogfood-backlog.md`)· F3 ③ 的 R1+R5 → XenoDev 侧(拆封 41 条前置)· KG-45 在 PRD 外仍余 **33 处失效行号 / 12 文件**,但均为 append-only 治理记录(hand-back 包 / forge round 文件)**不回改**,处置面是把「行号锚禁令」写进 SHARED-CONTRACT。

---

## 2026-08-11T15:42:50Z · 009-pM3prime-20260811T140531Z(F3 ③ CONCERNS 收口 R1-R5 · **五条逐条 mutation 实跑复证有齿** · 🔴 **R5 landed 但生产路径未生效:真盘 DB 停在 alembic 0019,取证表不存在,实跑 OperationalError** · KG-49 mirror 方向经更正后照铁律归 forge 006 · 新增 KG-50)

**Reviewed at**: 2026-08-11T15:42:50Z
**Related task**: FU-F3-3-concerns-fix
**Tags**: build-complete
**Severity**: medium
**6 约束自检**: ✅ all 6 PASS(consumer mode · 绝对 realpath)· check-8 PASS · ⚠ **check-7 WARN**(不阻断):`worktree` 字段填成散文句 `none(直接在 feat/009-spec 分支 commit · 未起 worktree · 同本 fork 既有 FU 惯例)`,与 `workspace.working_repo = /home/ys/codes/XenoDev-009` 不一致 —— 该字段用途是拓扑自证,填散文句让机器校验只能 WARN
**verdict-evidence 预检**: n/a(无 `ids_verdict_evidence:` 父键 —— 非 build-ship 包形态)

### IDS 侧独立复核(本次 review 实跑 · 非转述 build 结论)

**属实项(逐条实跑复证 · 无一不符)**:

- **测试基线属实**:IDS 侧独立复跑 **`1198 passed, 7 skipped, 6 deselected, 1 xfailed`**(140.90s)—— 与 hand-back 声称**逐字一致**。⚠ 第 30 条那种「hand-back 文本 vs commit 数字打架」本次未复发
- **R1 mutation 验齿(实跑)**:抽掉 `reconcile()` 里的 `_assert_source_ids_match_canonical_order` 调用 → `test_should_reject_when_reconcile_source_ids_diverge_from_canonical_order` 报 **`DID NOT RAISE`** 变红 ✅。调用点位置属实:在既有多重集 / 身份 / 清单锚检查**之后**、`evaluate_layer2` 消费 machine **之前**
- **R5 mutation 验齿(实跑)**:抽掉 `gold_layer2_item` INSERT 循环 → `test_should_persist_signal_id_per_item_when_reconcile_runs` 报 **`assert 0 == 3`**、`test_should_persist_items_even_when_criteria_not_met` 同红 ✅。migration 0021 逐条核对属实:只 `CREATE` 无 `ALTER`、跨表无 FK、`item_index >= 0` CHECK 在、`source_id`/`signal_id` nullable、downgrade raise(forward-only)
- **R5「无论 criteria_met/passed 真假都写」属实**:落库循环在 `criteria_met`/`passed` 计算与逐维写入**之后**、`return` **之前**,中间零 early-return
- **R3 mutation 验齿(实跑)**:neuter `Sequence` 形状守卫 → `test_should_raise_when_machine_payload_is_a_dict_not_a_list` 变红 ✅(另两条负例由第二道 `Mapping` + 至少一个可核对字段的守卫挡,分工清楚,非同一守卫)
- **R2 语义回答属实(实证)**:`census.py::run_census` 的 `now` 确在进入逐条循环**之前**只取一次(`SELECT strftime(...,'now')`),该批全部信号共享同一时间戳、条目间零区分度;全仓生产 SELECT 扫描确认**无一处读 `extracted_signals.created_at`**(grep 命中的三处分别是 `decision_drafts` / `strategy_signals` / `conflict_reports` 的同名列,不是本列)⇒ **不可用作提取时点独立锚成立**,「不加绑定代码、只在契约里明写时序关是自报的」是正确处置
- **R4 属实**:`_assert_source_id_alignment` 的「三方身份绑定」与 `_assert_matches_registered_sample_manifest` 的「三份 JSON」两处失真措辞均已订正;`test_should_reject_when_machine_order_shuffled` 的 docstring 已如实改写(承认它实际被多重集校验挡下而非乱序检测),并新增 `test_should_reject_machine_payload_when_source_id_order_swapped` 真守 F3 ③ 后那条关
- **红线 7 条全绿(实查)**:`extraction/gate.py` **零改动**(不在 `e0a08c5..HEAD` diffstat)· `_CORRECTNESS_GATE_AUTHORIZED_V0_1 = False` 未动 · `second_source_kind != _HUMAN_SOURCE_KIND → raise` 仍是 `evaluate_layer2` 首个 guard · C6 冻结常量未动 · `blind/` 与 `out/` **零改动** · **本次 diff 新增行零 `.py:行号` 锚**(KG-45 遵守属实)· KG-49 记 `dogfood-backlog.md` 未当场改 lib
- **41 条盲标机会确未拆封(真盘 DB 实查)**:`extracted_signals` **41 行**,`gold_layer2_result` / `gold_layer2_dimension` / `gold_layer1_result` **全 0 行**
- **确未 push**:`git branch -r --contains 849c30d` 为空;三条 commit(`849c30d` / `16c53ea` / `4820539`)均在 `feat/009-spec`
- **诚实边界属实**:「R1 挡不住同一 `source_id` 字符串重复时的内部换位、彻底闭合需 F3 ①」与第 31 条评审 C 原判一致,未夸大成「已闭合」

### 🔴 IDS 侧新发现(build 未列)

**发现 1 · R5 landed 但在生产路径上未生效 —— 实跑证,不是推演**

真盘 `projects/004-pB/out/e1-census-20260718.sqlite` 的 `alembic_version = **0019**`:不只缺 0021 的 `gold_layer2_item`,连 0020 的 `watchlist_snapshot` 也缺。`reconcile()` / `evaluate_layer2` **不自动跑迁移**,`docs/` 与 `scripts/` 全仓零处提 0021 或迁移步骤。

IDS 在真盘 DB 的**副本**上把所有 fail-closed 关逐个满足后跑完整生产路径(anchor 门槛必填 / 盲标隔离 / ticker 外锚三关依次挡下,均按设计 raise,证明这些关本身有齿),最终:

```
RAISED: OperationalError | no such table: gold_layer2_item
  崩溃前(未 commit)  gold_layer2_result=1 · gold_layer2_dimension=5
  关闭后(回滚检验)  0 · 0          ← 异常路径不 commit → 回滚 → 无半写、无 DB 损坏
```

四点:

1. **R5 的取证表在真正要取证的那个库里不存在**。R5 的立论是「错配发生后连事后取证材料都没有」—— as-shipped 在生产路径上**仍然没有**。这是 001-radar forge v4 已命名的 **landed ≠ 生效** 两态在 009 侧的同型实例
2. build §4「过程中的一次自查纠错」第 1 条**正是这个失败向量**(三个测试 fixture 缺迁移链 → `no such table`),但**只修了测试 fixture,没回头查真盘 DB**。同一根因,测试面修了、生产面没查
3. 真盘 DB mtime = 2026-07-27 ⇒ 0019 缺口**上一条(第 31 条)ship 时就存在**、一直没被发现;`watchlist_snapshot` 还是 E2「补数后零代码解锁」的前置表,也不在
4. **严重度校准(不夸大)**:41 条标注数据在 blind 包文件里、不在 DB,补迁移后重跑 `reconcile` **不损失标注劳动**;代价是一次中断,不是一次性资源报废。fail-closed 行为本身是对的

**发现 2 · KG-49 的 mirror 方向 —— IDS 复核先判错、已自我更正(留痕)**

IDS 初判「缺陷 lib 的 SSOT 在 IDS」⇒ **判错**。`framework/xenodev-bootstrap-kit/tests/integration/test-verdict-evidence-mirror-sha.sh:14` 原文:「source(**XenoDev SSOT**)→ target(**IDS bootstrap-kit**)」。即该 lib 的 SSOT 在 XenoDev,IDS 那份是 mirror(与 SHARED-CONTRACT 的方向相反)。三份 copy 字节一致(`43f13a60…`)。

后果:**改 IDS 那份 = 改 mirror,下次同步就被覆盖回去 = landed 但不生效**,恰是发现 1 的同一失败模式;而直接改 XenoDev SSOT 又踩铁律「框架级变更只走 forge,XenoDev 不当场改」。⇒ **build 把 KG-49 记 backlog 攒批 forge 006 是符合协议的**,IDS 初判「不宜继续躺 006 攒批」的理由不成立,**撤回**。

**发现 3(新条目 · KG-50)· mirror 完整性守卫当前完全失效**

`test-verdict-evidence-mirror-sha.sh` 硬编码 `/Users/admin/codes/XenoDev` 与 `/Users/admin/codes/ideababy_stroller`(mac→Ubuntu 迁移遗留)。IDS 实跑:

```
FAIL[src-missing] /Users/admin/codes/XenoDev/lib/handback-validator/verdict-evidence-lib.sh   (×3 件)
FAILED   EXIT=1
```

⇒ 三件 mirror(`verdict-evidence-lib` / `validate-verdict-evidence` / `review-log-writer-lib`)的字节一致性**现在没有任何守卫在跑**,任何一边漂移都不会被发现。而 KG-49 的整个处置面正好依赖 mirror 方向可信 —— 守卫失效时「哪边是 SSOT」只能靠读注释,不能靠测试。

**发现 4(轻)· hand-back 措辞不精确一处**

§4 与 KG-49 均写 fix commit `16c53ea`「diff 证 0 行删除」,实际 `git show 16c53ea` = **`987 insertions(+), 3 deletions(-)`**。IDS 做子集检验:`e0a08c5` 版 954 行**逐行 0 行缺失** ⇒ **历史实质零丢失,结论属实**;那 3 行删的是 `849c30d` 自己刚引入的 singleton pointer 行。属措辞不精确(应写「vs `HEAD~2` 老历史 0 行丢失」),**非事实错误**。记此因「hand-back 文本 vs commit 数字打架」是第 30 条踩过的坑。

### Operator 决议(6 问 · 全选推荐项)

- [x] **① 发现 1 → 起 FU**:把 0020+0021 迁移到真盘 DB + 在 `reconcile()` 入口加 `alembic_version` 前置校验(缺迁移即 fail-closed 明确报「拆封前置未齐」而非裸 `OperationalError`)+ `docs/` 写拆封 runbook。据:R5 的整个立论是取证材料必须在场,现在它不在场;且 build 已在 fixture 面修过同一根因却没查生产面,**靠 checklist 不靠代码就是重演**
- [x] **② 本包验收 → 接受 R1-R5 收口,CONCERNS 视为已闭;但拆封 41 条仍 blocked**。前置未齐:发现 1 未解 + F3 ① 残留缺口(同 source 内换位仍不可侦测)仍在。与第 31 条「R1+R5 是必要不充分」原判一致
- [x] **③ R6-R8 三条 LOW + 措辞订正 → 并入 ① 的 FU 一起做**。据:R6(`--source-ids` 无脚本无 runbook · 「顺手那条 SQL」走覆盖索引给非 id 序)本就是 R1 挡的那类漂移的投递向量,与「写拆封 runbook」是同一件事
- [x] **④ KG-49 → 止血到此为止 + 照铁律归 forge 006**。lib 本体不改:改 IDS mirror 不生效、改 XenoDev SSOT 踩铁律,两条路都不该在 handback-review 里当场做
- [x] **⑤ KG-50(mirror 守卫失效)→ 记新条目归 forge 006 攒批**,与 KG-49 同场处置(同一块框架面)
- [ ] 修 PRD(本次不动 —— 本包未产生 PRD 级冲突)
- [ ] 修 SHARED-CONTRACT(本次不动)

### 已执行(本次 review 当场做的唯一动作)

- **001-radar 线止血备份**:`/home/ys/codes/XenoDev/.claude/skills/codex-review/REVIEW-LOG.md` → `REVIEW-LOG.md.pre-KG49-backup-20260811`(**296 行 / 12 个 frontmatter 分隔符 ≈ 6 条累积历史**)。据:001 线正活跃(T040),下次按 SKILL §3.6.2 调用 `write_review_log_immutable` 就会把这 6 条砍成 1 条。此动作纯增量、不改任何框架件、与 SSOT 方向无关

### 决议后果与待办

**A · XenoDev 侧 FU(授权范围,合并 ①+③)**
- 真盘 DB 跑 `alembic upgrade` 到 **0021**(补 0020 `watchlist_snapshot` + 0021 `gold_layer2_item`)
- `reconcile()` 入口加 `alembic_version` 前置校验 —— **fail-closed 且报「拆封前置未齐:DB schema 为 <x>,需 ≥0021」**,不是裸 `OperationalError`
- `docs/` 写 41 条拆封 runbook:含迁移前置、`--source-ids` 产生方式(**必须 `ORDER BY id`,不得用会走覆盖索引的裸扫描** = R6)
- R7(库层只按 `caliber_version` 过滤、不含 `extractor_variant`)· R8(非 `Mapping` 元素抛 `AttributeError` 而非 `BlindIsolationError`)顺手带
- hand-back 措辞规范:「0 行删除」类断言须写清对比基准(vs `HEAD~2` / vs 哪个 commit),避免与 `git show` 的 stat 打架

**B · 仍 blocked / 未变(逐条延续,本次未触碰)**
- **拆封 41 条 = blocked**(前置未齐 · 见 ②)
- **F3 ①②**(身份键换 `extracted_signals.id` + 改三份 payload 格式)—— 未做,是 R1 无法闭合「同 source 内换位」的根因;连锁成本(`blind/machine.json` 重生成 + 重跑提取器)只在确定拆封时才值得付
- **两维外锚 lane**(第 31 条已 STOP)· **Layer-1 主体问题**(41 条 = precision 框非 recall 框 · α/`pred_spans` 契约缺角未解 · `span_prf` exact-match 形态是根因)· **金标 Layer-2 correctness gate blocked** —— 三条状态全不变
- **E2 仍不授权**

**C · 归 forge 006 攒批(本次不起 forge)**
- **KG-49**(`review-log-writer-lib.sh` 的「singleton 可覆盖」设计假设 vs 本仓 REVIEW-LOG 的追加式历史日志实际用法 —— 已真实发生一次 954→17 行数据丢失,靠 `git diff` 自查 + 未推送才挽回)
- **新增 KG-50**(`test-verdict-evidence-mirror-sha.sh` 因 `/Users/admin` 硬编码在 Ubuntu 上 100% `FAIL[src-missing]` ⇒ 三件 mirror 字节一致性**现无守卫**;而 KG-49 的处置面恰恰依赖 mirror 方向可信)
- 既有攒批不变:KG-43 三道门 · KG-44 · KG-45(行号锚禁令写进 SHARED-CONTRACT)· KG-46/47/48 · KG-41 · 元层条 · §3-1b 解锁制品设计
- ⚠ **forge 时的元层观察(本条自产)**:发现 1 与 IDS 自己在发现 2 的判错**同型** —— 都是「在一个面上验证过了,就默认另一个面也成立」(build:fixture 面修了默认生产面也修了;IDS:读到 IDS 有这份文件就默认 IDS 是 SSOT)。KG-45 / KG-49 / KG-50 也都长这样。**建议 forge 006 把这条当独立门族看,而不是三条互不相干的卫生问题**

**D · warn 型 preflight(不阻断 · 留痕)**
- 本次 review session 在 `main` 分支而非 `009-pM3prime` worktree —— worktree-per-idea 规约 warn。按 CLAUDE.md v10 注,`handback-review` 决议本就是规约列出的合回 main 的合法 checkpoint,且该 warn 的裁决被 `OB-006-v10-06`(规约消歧义)前置阻塞
- hand-back 侧 check-7 WARN(`worktree` 字段填散文句)—— 建议 XenoDev 下次填可机器比对的值(分支名或 `none`),散文句让拓扑自证降级成人工阅读

**Follow-up commits**: pending
