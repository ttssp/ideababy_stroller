---
doc_type: handback-decision-log
first_created: 2026-07-02T02:32:43Z
last_updated: 2026-07-06T00:00:00Z
total_decisions: 15
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

**Follow-up commits**: pending(本 LOG + PRD §7 O8 指针 · 同一 IDS commit)· forge setup 随后 · alpha_lane 不 merge
