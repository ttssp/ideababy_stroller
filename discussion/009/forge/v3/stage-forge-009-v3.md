# Forge Stage · 009 · v3 · "provider 双 as_of 轴契约 · 解 T012 R6"

**Generated**: 2026-07-03T10:12:00Z
**Source**: forge run v3 (forge-lite · P1-only convergence) with X = 4 标的, Y = [契约正确性/PIT语义, 器官边界/OUT-10], Z = 不对标, W = [refactor-plan]
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both) · **forge-lite — 无 P2/P3**(方向已由 operator 拍板选 A · 契约形状已明确 · P1 双方零分歧强收敛)
**Searches run**: 0 (forge-lite · 不对标 · 纯内部契约审)
**Moderator injections honored**: none
**Convergence outcome**: converged(P1 双方独立收敛到候选 (a),零分歧)

---

## How to read this

forge 是横切层(不是 L1-L4 pipeline 的一部分)。本文档是 **forge-lite** 变体的产出:
只跑 P1 双方独立审(无 P2 SOTA / 无 P3 收敛轮),因为方向已由 operator 拍板(选 A「执行时可见」),
契约形状已很明确(单 `query_as_of` → 双 as_of 轴),不是"该不该建"而是"接口怎么钉"。

读完后你应该:
- 拿到 `get_adjusted_close` 的精确新签名(带 `factor_as_of=None` 向后兼容默认)
- 拿到 P1 双方独立命中的三个收尾细节的**契约级裁决**(不留悬)
- 拿到向后兼容保证 + 落哪个仓 + T012 收尾的具体调用形状 + 可测验收
- 能基于 §"Decision menu" 直接进入下一步(在 XenoDev 起 FU-task 收尾 T012)

## Verdict

选 **候选 (a)**:`get_adjusted_close(..., query_as_of, factor_as_of=None, ...)` —— `query_as_of`
管 close_raw 版本轴、新增可选 `factor_as_of` 管复权因子轴,默认 `None → 退化 = query_as_of`
即旧行为。**这是"解 R6 + 最小冲击 + 守 OUT-10 + 向后兼容"四项都最优的**(直接回应 K binding
②最小冲击 + ③不破已 ship M1)。

P1 双方独立判死 (c)(用现签名两次调用重组):Opus 判**技术不可行**(现契约只返已算好的 adjusted,
不暴露 raw/factor 独立取用,从 provenance 反解是脆 hack);Codex 判**污染从 provider 内不变量退化成
T012 私有约定**(两次调用需调用层自查 hit_trade_date/source 一致,后续补录不同源会 silent wrong)。
双方判 (b)(拆两个原子读)次选:语义最正交但破坏"单入口拿齐 provenance" + 冲击面最大 + 全体调用方要改。

改的是 009 自有 `PITPriceProvider`(T002 定 · 本 fork 可改)→ **不违 OUT-10**(OUT-10 禁的是改 004
`PriceDataProvider.get_history`)。`CurrentStatePriceProvider`(T008 桥接 004)用 as_of=今天 退化查询,
不涉双轴回测语义 → 不受影响。

## Evidence map

| 结论 | 来源 | 引用 | 是否有反对证据 |
|---|---|---|---|
| 病灶 = close_raw 与 factor 被同一 `as_of<=:query_as_of` 一起选 | P1-Opus §1(Y1)/ provider.py L48-55 `_SELECT_PRICE_SQL` | "一条 SQL 取整行(close_raw 和 factor 绑同一 as_of)" | - |
| 选 (a) 加可选第三参数 `factor_as_of` | P1-Opus §2(✅ 倾向)/ P1-GPT §2(倾向选 · 5/5 解 R6) | "四项都最优的" / "在最干净接口形状上最好" | - |
| (c) 技术不可行 / 退化成私有约定 | P1-Opus §2(❌)/ P1-GPT §2(3/5 provenance 2/5) | "现契约不暴露 raw/factor 独立取用" / "从 provider 内不变量变成 T012 私有约定" | - |
| (b) 次选(破坏单入口 provenance) | P1-Opus §2(⚠)/ P1-GPT §2(2/5 冲击) | "破坏单入口拿齐 provenance + 冲击最大" | - |
| 改 009 PITPriceProvider 不违 OUT-10 | P1-Opus §1(Y2)/ P1-GPT §1(视角B)/ handback §2 决议项2 | "OUT-10 禁的是改 004 PriceDataProvider" | - |
| 细节1:factor 子查询锁同一 hit_trade_date + 同一 source | P1-Opus §3.1 / P1-GPT §3.1 | "entry 命中的 trade_date 与 factor 命中的必须同一天" / "factor 查询必须锁同一 source" | - |
| 细节2:非破坏扩 provenance(保 hit_as_of + 加 factor_as_of) | P1-GPT §3.2 | "前者(保留+新增)更稳" | - |
| 细节3:factor 缺失细分降级 v0.2 | P1-GPT §3.3(Opus 未覆盖) | "也可能超出本次最小契约" | ⚠ 仅 Codex 单侧提出(见 §"What this menu underweights") |
| T012 用 entry_raw@entry × factor@exit 算 realized | handback §2 决议项1 / PRD §7 | "adjusted = entry_raw(@entry as_of) × factor(@exit as_of)" | - |

## Intake recap

### X · 审阅标的(4 个)
1. T012 hand-back `20260703T085623Z-009-pForge`(R6 复现 + 2 决议项 · **核心 X** · handback 类)
2. `XenoDev/.../price/interface.py`(现 `PITPriceProvider` 契约 · 单一 query_as_of · **要改的接口** · 代码)
3. `XenoDev/.../price/provider.py`(T003 实装 · 病灶 SQL `_SELECT_PRICE_SQL` · 代码)
4. `discussion/009/009-pForge/PRD.md` §7 + `HANDBACK-LOG.md` T012 条(决议溯源 · PRD 类)

### Y · 审阅视角
- **契约正确性 / PIT 语义** — 双 as_of 轴怎么表达才干净 + 向后兼容
- **器官边界 / OUT-10** — 改动最小化冲击 · 扩 009 自有契约 vs 碰 004 已 ship 签名

### Z · 参照系
- mode: 不对标(forge-lite · 契约方向已定 · v1 已刷过 PIT 数据模型 SOTA)
- 用户外部材料: 无

### W · 产出形态
- **refactor-plan** ✅(verdict-only / decision-list / next-PRD / free-essay 未勾)

### K · 用户判准
> operator 已决议 T012 两项:决议项 1 = 选 A「执行时可见」(PIT 严格 · entry raw close 按 entry as_of 取、
> 复权 factor 按 exit as_of 取 · adjusted = entry_raw(@entry) × factor(@exit));决议项 2 = 需分离价格版本轴
> 与复权因子轴,具体契约形状留 forge 定。
>
> 要定死:① 分离双轴的最干净接口形状(三选一 a/b/c);② 向后兼容(T004/T005/T007 单 query_as_of 不能破);
> ③ OUT-10 边界(改 009 自有 vs 碰 004 已 ship)。
>
> **binding**:① 死守选 A 不重议语义;② 最小冲击优先;③ 不破 v1/v2 verdict + 不破已 ship M1(T001-T007);
> ④ 契约要能直接指导 T012 收尾 + 可能的 FU-task;⑤ 轻收尾(forge-lite · 可执行优先)。

### 收敛模式
strong-converge → 单一 verdict(单一契约方案)+ 残余降级 v0.2 note

---

## §Refactor plan(W = refactor-plan · forge-lite · P1-only convergence)

单一契约方案(strong-converge · 不列并行 path)。改造分三处:接口签名(interface.py)、
返回模型(models.py)、查询实装(provider.py)。全在 009 自有 PIT 契约内。

### §新契约签名

interface.py `PITPriceProvider.get_adjusted_close` 与 provider.py 实装同步改为:

```python
def get_adjusted_close(
    self,
    ticker: str,
    *,
    market: Market,
    target_date: str,
    query_as_of: str,
    factor_as_of: str | None = None,   # ← 新增 · 复权因子版本轴 · 默认 None 退化为 query_as_of
    adjust: Literal["fwd", "back"] = "fwd",
) -> AdjustedPricePoint | None:
    ...
```

**双轴语义(契约级定死)**:
- `query_as_of`:**close_raw 版本轴** —— 选哪一版原始收盘价(entry 场景 = entry as_of · "执行时可见")。
- `factor_as_of`:**复权因子版本轴** —— 选哪一版复权因子(entry 场景 = exit as_of · 统一 valuation)。
  - `factor_as_of=None`(默认)→ **退化为 `query_as_of`** → 单轴取整行 = **旧行为字节级不变**(向后兼容)。
  - `factor_as_of` 须与 `query_as_of` 同格式(canonical UTC · 走同一 `_require_canonical_utc` 校验)。
- 三个 canonical 校验位置:`target_date`(日期)、`query_as_of`(UTC)、`factor_as_of`(UTC · 仅当非 None)。

### §三个收尾细节定死(契约级裁决 · P1 双方命中的不确定点)

#### 细节 1 · factor 命中行必须锁定 close_raw 命中行的同一 (hit_trade_date, source)

**裁决:factor 子查询必须同时锁定 (a) 同一 hit_trade_date **和** (b) 同一 source。** 两者都锁,不是二选一。

- **理由**:P1-Opus §3.1「entry 命中的 trade_date 与 factor 命中的 trade_date 必须同一天(否则 factor 对错票)」
  + P1-GPT §3.1「factor 查询必须锁 raw close 命中行的同一 source,否则跨源 raw/factor 混算产生新 silent wrong」。
  复权因子是**针对某一 (ticker, market, trade_date, source) 的估值属性** —— 用 A 源的 close_raw × B 源的 factor,
  或用 04-27 的 close_raw × 04-28 的 factor,都是逻辑错票。

- **SQL 层如何钉死(两阶段选择)**:
  1. **第一次 PIT 选择(定命中行身份)**:用现有 `_SELECT_PRICE_SQL`,按 `query_as_of` 选出
     `(hit_trade_date, source)` + `close_raw` —— 这是 close_raw 版本轴的命中行,身份 = (hit_trade_date, source)。
  2. **第二次 PIT 选择(选 factor 版本)**:在**已锁定的 (ticker, market, hit_trade_date, source)** 上,
     加 `as_of <= :factor_as_of` 再取最新可见 factor:

     ```sql
     SELECT adj_factor_fwd, adj_factor_back, as_of
     FROM price_daily
     WHERE ticker = ? AND market = ? AND trade_date = :hit_trade_date
       AND source = :hit_source
       AND as_of <= :factor_as_of
       AND as_of GLOB '<canonical>'
     ORDER BY as_of DESC
     LIMIT 1
     ```

  - **约束表达**:`trade_date = :hit_trade_date`(精确等 · 不是 `<=`)+ `source = :hit_source`(精确等)
    锁死身份;`as_of <= :factor_as_of` 是唯一放开的轴(选 factor 版本)。沿用现有 `as_of GLOB <canonical>`
    脏小数秒守卫(R4)+ `ORDER BY as_of DESC LIMIT 1` tie-break 纪律 —— **不破 provider.py 现有加固**。
  - `factor_as_of=None` 退化时:第二次查询用 `query_as_of` 作 `factor_as_of` → 命中行与第一次同一行 →
    factor 与 close_raw 同源同版本 = 旧单轴行为。

> **⚠ 实装订正(post-ship · 2026-07-04 · handback `009-pForge-20260703T170209Z` T012 收尾)**:
> 上述「两阶段两次独立 SELECT」在实装时被 codex R7 判为 **1 high** —— 两次独立 SELECT 在 SQLite
> autocommit 下**跨两个快照**,并发 ingest 可拼「旧 close_raw + 新 factor」= silent-wrong,**退化路径
> 也破原子性**。**shipped 契约改为单语句 CTE**(`_SELECT_DUAL_AXIS_SQL` · SQLite 单语句 = 单一致快照
> 原子读)+ 2 回归测(并发等价 + 结构 mutation-killer · mutation 实证 kill 掉 two-SELECT 版本)→ R8
> approve 0 findings。**契约语义(factor 锁同 hit_trade_date+source · 双 as_of provenance)完全不变,
> 只是把「两次 SQL / 单 SQL self-join 等价」的实现选择收紧为「必须单语句原子读」**。本 stage §细节1 当时把
> two-SELECT 列为主实现 + self-join 列为可选优化,低估了原子性 —— 是 forge-lite(无 P3 对抗)+ strong-converge
> 回声室的一个实证盲区(见本文 §"What this menu underweights" 已预警的"两阶段之间未对抗验证"一条)。

#### 细节 2 · AdjustedPricePoint provenance 双 as_of(非破坏性扩)

**裁决:采纳 Codex 的非破坏性扩法 —— 保留 `hit_as_of`(语义收窄为 close_raw 行 as_of)+ 新增
`factor_as_of`,不改名为 `price_as_of`。** binding② 最小冲击 + 向后兼容 → 倾向非破坏。

- **理由**:P1-GPT §3.2「兼容性上前者(保留 hit_as_of + 新增 factor_as_of)更稳」;
  P1-Opus §3.2「provenance 该记两个 as_of 才诚实,否则 O6 as-of 可复现在双轴下更模糊」。
  破坏性改名 `hit_as_of → price_as_of` 会破所有读 provenance 的现有调用方(无收益)。

- **AdjustedPricePoint 新字段**(models.py · frozen 不变):

  ```python
  adjusted_close: float          # = close_raw × factor_used(不变)
  hit_trade_date: str            # close_raw 命中行 trade_date(= factor 命中行 trade_date · 细节1 已锁同一天)
  hit_as_of: str                 # close_raw 命中行 as_of(语义收窄:仅 close 版本轴 · 单轴退化时 == factor_as_of)
  factor_as_of: str              # ← 新增 · factor 命中行 as_of(双轴 provenance · 满足 O6 可复现)
  source: str                    # 命中行数据源(close 与 factor 同源 · 细节1 已锁)
  close_raw: float               # close_raw 命中行原始价(不变)
  factor_used: float | None      # 实际用的复权因子(T003 直取恒非 None · 不变)
  ```

  - 单轴退化(`factor_as_of=None`)时:`factor_as_of` 字段填入 `hit_as_of` 的值 → 旧调用方读到的
    provenance 语义与从前一致(hit_as_of == factor_as_of · 双 as_of 同值)。
  - 新增字段无默认(必填)→ 但因所有构造点都在 provider.py 内部,不破外部构造(外部不构造本对象)。

#### 细节 3 · factor 缺失 / 跨 as_of 的返回语义 → **降级 v0.2 note**

**裁决:纳入本次最小契约的部分 = 沿用现有 `None` 语义(factor 行缺 → 返 None);
细分"无数据 skip" vs "有数据但因子缺 data-quality gap"的结构化 outcome → 降级 v0.2 note(见 §残余降级)。**

- **理由**:K binding⑤ = 轻收尾 / 可执行优先;P1-GPT §3.3 自己也说「这也可能超出本次最小契约」;
  P1-Opus 未覆盖此点(仅 Codex 单侧提出)→ 非双方共识,不强纳最小契约。
- **本次最小契约的 factor-缺失行为**:第二次 factor 子查询 `fetchone()` 为 None(该 source/trade_date
  在 factor_as_of 口径下无可见 factor 行),或命中行请求方向 adj_factor 为 NULL → **返 None**(与现语义一致 ·
  不返 close_raw 伪装已复权)。T012 侧现有 `GAP_*` / typed skip 全集(11 枚举)已能吸收 None,不阻收尾。

### §向后兼容策略

`factor_as_of=None` 默认退化 = 现有单 `query_as_of` 调用方全不破的具体保证:

- **T004/T005**(源适配器)+ **T007** + **CurrentStatePriceProvider**(T008 桥接 004):它们调
  `get_adjusted_close` 时**不传 `factor_as_of`** → 走默认 None → 第二次 factor 查询用 `query_as_of` 作
  factor_as_of → 命中与第一次同一整行 → **SQL 结果与旧单轴 `_SELECT_PRICE_SQL` 取整行字节级等价**。
- **AdjustedPricePoint** 对旧调用方:新增 `factor_as_of` 字段填 `hit_as_of` 值 → 旧读 provenance 代码
  (读 hit_trade_date/hit_as_of/source/close_raw/factor_used)全部照常工作,新字段只是多一个可读项。
- **OUT-10 保证**:全部改动在 009 自有 `interface.py` / `provider.py` / `models.py`;
  **不碰 004 `PriceDataProvider` 表/签名**;`CurrentStatePriceProvider` 用 as_of=今天 退化查询(单轴口径),
  行为不变。

### §落哪个仓 + T012 收尾指示

- **契约改归 XenoDev**(spec OUT-10 授权 = 本 fork handback-review 已决议本轮 forge 定契约后授权改
  009 自有 provider):改 XenoDev `projects/004-pB/src/decision_ledger/price/` 下 `interface.py`(签名)+
  `provider.py`(两阶段 PIT 选择 + 锁 hit_trade_date/source)+ `models.py`(AdjustedPricePoint 加 factor_as_of)。
  起一个 **provider FU-task**(如 T003-rev-2 或新 task)做上述三文件改 + 补测。
- **IDS 侧 PRD §7 契约同步**:PRD §7 已落 entry 价 PIT 语义决议(entry_raw@entry × factor@exit)+
  已标"触发 provider 契约变更(走 forge · 未落地)"。本 stage 定稿后,IDS 侧把 §7 的
  "未落地" 更新为指向本 stage 的新契约签名(`factor_as_of` 参数 + AdjustedPricePoint.factor_as_of 字段)。
- **T012 用新契约算 realized-return 的具体调用形状**:
  - **entry 价**(执行时可见):
    ```python
    entry = provider.get_adjusted_close(
        ticker, market=mkt, target_date=entry_trade_date,
        query_as_of=entry_as_of,      # close_raw 版本轴 = entry 执行时可见
        factor_as_of=exit_as_of,      # factor 版本轴 = exit 统一 valuation
        adjust="fwd",
    )
    # entry.adjusted_close = close_raw(@entry as_of) × factor(@exit as_of)
    ```
  - **exit 价**:`query_as_of = exit_as_of` + `factor_as_of = exit_as_of`(两轴同点 · 或不传 factor_as_of 走退化)。
  - realized:`log(exit.adjusted_close) - log(entry.adjusted_close)`(沿用 T012 R4 已修的 log 差值口径)。

### §可测验收

契约改后的验收测试(FU-task TDD · 至少覆盖以下):

1. **R6 复现 → 修复**(核心):
   - fixture:`AAPL` · trade_date=04-27 · close_raw=100 @as_of=04-27 · **同 trade_date 04-27 close_raw=90 @as_of=04-30**(纯数据修订) · factor@两 as_of 均=1.0(无拆股) · exit trade_date=05-04 close=110。
   - `get_adjusted_close(target_date=04-27, query_as_of=04-27, factor_as_of=05-04)` →
     `entry.close_raw == 100`(entry as_of 版本 · **非 90**)· `entry.adjusted_close == 100`。
   - T012 realized = `log(110/100) = +9.5%`(**非**单轴误算 `log(110/90) = +20%`)。
2. **factor 锁 hit_trade_date/source**(细节1):
   - fixture:04-27 有 A源 + B源 两行不同 factor;factor_as_of 下 B源有更新 factor。
   - 断言:factor 取的是 close_raw 命中行**同源同 trade_date**的 factor,不跨源 / 不跨天。
3. **向后兼容回归**(退化不变):
   - 不传 `factor_as_of`(=None)的调用 → 结果与改前旧 `_SELECT_PRICE_SQL` 取整行**字节级一致**
     (close_raw / factor_used / adjusted_close / provenance 全等);T004/T005/T007 现有测试全绿无回归。
   - 断言退化时 `AdjustedPricePoint.factor_as_of == hit_as_of`。
4. **provenance 双 as_of**(细节2):双轴调用返回的 `hit_as_of`(=entry as_of)≠ `factor_as_of`(=exit as_of),
   两者都取自真命中行,满足 O6 可复现。
5. **factor 缺失返 None**(细节3 最小契约):factor_as_of 口径下 factor 行缺 → 返 None(与现语义一致)。
6. **全 004 套回归**:587 passed 无回归(沿用 T012 hand-back 的回归基线)。

### §残余降级 v0.2 note

未纳入本次最小契约、降级到未来处理的:

- **细节 3 的结构化 data-quality outcome**(仅 Codex 单侧提出 · Opus 未覆盖):当 `factor_as_of < query_as_of`
  或 factor 行缺但 raw close 存在时,当前返 `None`(与现语义一致)。**若未来 T012/T013 回测需区分
  "无数据 skip" vs "有数据但因子缺 data-quality gap"** → 那时在 provider 加 typed error / sentinel(现不预设 ·
  接现有 interface.py L64-68 已记的 "T012 disambiguation 备注")。触发条件:realized-return 出分母时发现
  因子缺口被当无数据静默 skip 导致样本偏差。
- **多轴演化**(仅 Opus §3.3 单侧提出):若将来还要分离更多轴(如分红 factor vs 拆股 factor 各自 as_of),
  (a) 的"加参数"可能膨胀。当下判"(a) 够且最小,膨胀了再说" → 若真出现第三轴需求,回 IDS 起 v4 重评
  (a) 加参数 vs (b) 正交原子读的长期 tradeoff。

---

## What this menu underweights(强制自批判)

- **反对证据未充分整合**:本轮 §"Evidence map" 中唯一标 ⚠ 的是细节3(仅 Codex 单侧提出,Opus 未覆盖)。
  主裁决把它降级 v0.2 而非纳入最小契约 —— 风险 = 若 factor 缺口在真实数据里比预期常见,T012 会把
  "因子缺" 静默当 "无数据 skip",污染 alpha 样本。缓解 = §残余降级已记明触发条件 + interface.py 已有
  disambiguation 备注,不是遗漏而是显式 defer。
- **Y 视角覆盖盲区**:Y 只含"契约正确性 / 器官边界",**未含性能**。两阶段 PIT 选择(两次 SQL 而非一次)
  对 T012 每信号双侧取价 = 查询次数翻倍。forge-lite 未评估回测规模下的性能冲击 —— 若 M2 回测标的量大,
  值得后续 attention(可用单条带 self-join 的 SQL 合并两阶段,但那是实现优化,不改契约)。
- **K 中未充分回应的关切**:K binding④ 要求"契约能直接指导可能的 provider FU-task" —— 本 stage 给了
  三文件改点 + 验收,但**未给 FU-task 的 task-id / DAG 依赖**(那是 XenoDev spec-writer 的活,不在 forge 范围)。
- **convergence_mode 副作用**:strong-converge + forge-lite(只 P1 无 P3 对抗)= **双模型可能回声室强化同一盲区**。
  双方都聚焦 R6 的 close_raw 污染,都默认"两阶段选择 + 锁同源同天"是对的 —— 但**没有第三方对抗验证
  "两阶段之间的 as_of 单调性"**(若 factor_as_of < query_as_of,即 factor 版本早于 close 版本,是否合法?
  R6 场景是 factor_as_of > query_as_of,反向未验)。真实回测数据可能揭示反向场景。
- **X 标的覆盖局限**:未读 T012 的实装 `alpha/realized_return.py` 全文(只读 hand-back 描述)。R5/R6 的
  valuation_as_of 统一逻辑在该文件里,新契约调用形状(§落哪个仓)是基于 hand-back 推断,收尾时须对齐实装。
- **forge versioning 提示**:触发 v4 的新信息 = (1) 出现第三个需分离的 as_of 轴(分红 vs 拆股) → 重评
  (a) vs (b);(2) 真实数据揭示 factor 缺口频繁 → 细节3 从 v0.2 note 升级为必须纳入;(3) 两阶段查询
  性能不可接受 → 评估单 SQL self-join 合并(实现层,通常不需 forge)。

## Decision menu(for human)

### [A] 接受 verdict 进 L4
```
本 verdict 的 L4 落地 = 在 XenoDev 起 provider FU-task(非新 PRD fork · 契约已定形)。
⚠ W 未含 next-PRD → 无 PRD draft 可抽;本 verdict 直接指导 XenoDev 侧 FU-task。
流程:
1. IDS 侧:更新 discussion/009/009-pForge/PRD.md §7 —— 把"触发 provider 契约变更(未落地)"
   替换为指向本 stage 的新契约(factor_as_of 参数 + AdjustedPricePoint.factor_as_of 字段)。
2. 更新 discussion/009/handback/HANDBACK-LOG.md T012 条:标 forge v3 定契约 · 授权 XenoDev 收尾。
3. 新开 XenoDev session,起 provider FU-task(TDD):
   - 改 interface.py get_adjusted_close 签名(加 factor_as_of=None)
   - 改 provider.py:两阶段 PIT 选择 + 锁 hit_trade_date/source(§细节1 SQL)
   - 改 models.py AdjustedPricePoint(加 factor_as_of · §细节2)
   - 按 §可测验收 补 6 项测试(R6 复现→修 + 向后兼容回归)
4. T012 收尾:realized_return.py 改用双轴调用形状(§落哪个仓)· 从 BLOCKED → merge。
```

### [B] 跑 forge v4(说明需要补什么)
```
/expert-forge 009
# 触发条件见 §"forge versioning 提示":第三个 as_of 轴 / factor 缺口频繁 / 两阶段性能。
# 若只是想补性能视角(Y 未含),可在 Phase 0 加 Y=性能 + X 加回测规模数据。
```
适用:出现多轴演化需求、或真实数据推翻细节3 的降级判断。**当前不建议**(契约已强收敛且够 T012 收尾)。

### [C] 局部接受
- ✅ 采纳:候选 (a) 签名 + 细节1(锁同源同天)+ 细节2(非破坏扩 provenance)+ 向后兼容策略
- ⏸ 挂起:细节3 结构化 outcome(已降级 v0.2 · 等真实数据揭示 factor 缺口频率再定)
- ❌ 拒绝:候选 (b)/(c)(P1 双方已判死)

### [P] Park
```
/park 009
```
保留全部 forge v3 产物,标暂停。T012 保持 BLOCKED。**不建议**(T012 阻 M2 主链,park = 闭环停摆)。

### [Z] Abandon
```
/abandon 009
```
**强烈不建议**。本 verdict 是收窄的契约修,非"该不该做 009"的存亡判断;v1/v2 已定 009 该建。

---

## Forge log

- v3: 2026-07-03 (forge-lite · P1-only) — verdict: "选 (a) 加 factor_as_of=None 分离双 as_of 轴 · 两阶段 PIT 选择锁同源同天 · 非破坏扩 provenance · 解 T012 R6"
- v2: 2026-07-01 — verdict: "目标态七环节契约化闭环 · PIT 价格层为唯一新器官 · Strangler Fig 分期 M1-M4"
- v1: 2026-07-01 — verdict: "009 = 集成契约 + 共享回测地基,非统一壳"
