---
doc_type: forge-config
forge_id: 009
forge_version: v3
created: 2026-07-03T09:38:25Z
prefill_source: manual(handback-review 009 · T012 决议项2 = provider 契约跨仓改 · 铁律须 forge)
convergence_mode: strong-converge
scope: forge-lite(仅 P1 双方独立审 → 直接收敛定契约 · 方向已由 operator 定 A · 不跑 P2 SOTA/P3)
x_count: 4
x_hash: 76ceb877c9e54198386edfff5b1b2483
y_count: 2
w_count: 1
z_mode: 不对标(纯内部契约审 · 方向已定 · forge-lite 跳 P2 SOTA)
k_provenance: verbatim handback T012 决议项1+2 + operator 选 A
v3_mission: 定 provider 分离双 as_of 轴的新契约(entry 价执行时可见 · PIT 严格)· 解 T012 BLOCK
inheritance: v1/v2 verdict 不重审;本轮只审 T012 R6 揭的 provider 单轴→双轴契约改
---

# Forge config · idea 009 · v3(forge-lite · provider 双轴契约)

## 背景:为什么起 v3(且为什么 forge-lite)

handback-review 009 决议 T012(M2 realized-return)的 codex R6:**entry 执行价被 entry 后的数据修订污染**。
根因 = `get_adjusted_close` 用**单一 `query_as_of`** 同时管两件事:选哪条 price_daily 行(价格版本轴)+
选哪个复权因子(因子估值轴)。operator 已决议**选 A「执行时可见」(PIT 严格)** → 需**分离这两轴**:
entry raw close 按 entry as_of 取、factor 按 exit as_of 取。

**为什么走 forge**:改 `get_adjusted_close` 签名 = 改 T003 已 ship 的 provider 契约 = **违 spec OUT-10
= 跨仓契约改**。CLAUDE.md 铁律「跨仓协议改 / 重大架构转向 → 必须回 IDS forge」。不在 XenoDev 当场改(防 V4)。

**为什么 forge-lite(仅 P1)**:方向已由 operator 拍板(选 A),契约形状已很明确(单 query_as_of → 双 as_of 轴)。
不需要 P2 SOTA 检索(不是"该不该建"而是"接口怎么钉")+ 不需要 4 轮收敛。**只跑 P1 双方独立审接口新形状
→ 直接收敛定契约**。~2 次 cdx-run。若 P1 双方发现未预见的设计分歧(如"该进 provider vs 调用层重组")→ 升级补跑 P2。

## X · 审阅标的(4)
1. `discussion/009/handback/20260703T085623Z-009-pForge-20260703T085623Z.md`(T012 hand-back · R6 复现 +
   2 决议项全文 · **核心 X**)
2. `/home/ys/codes/XenoDev/projects/004-pB/src/decision_ledger/price/interface.py`(现 PITPriceProvider 契约 ·
   `get_adjusted_close(ticker,*,market,target_date,query_as_of,adjust)` 单一 query_as_of · **要改的接口**)
3. `/home/ys/codes/XenoDev/projects/004-pB/src/decision_ledger/price/provider.py`(T003 实装 ·
   `WHERE trade_date<=:target AND as_of<=:query_as_of ORDER BY ... LIMIT 1` 单轴取整行 · 病灶实现)
4. `discussion/009/009-pForge/PRD.md` §7 M1 契约(已落 entry 价 PIT 语义决议 · 结构化返回)+
   `HANDBACK-LOG.md` T012 条(决议溯源)

## Y · 审阅视角(2)
- **契约正确性 / PIT 语义** — 双 as_of 轴怎么表达才干净:签名加第三参数?两个显式 as_of?调用层重组 vs
  provider 内建?向后兼容(现有单 query_as_of 调用方 T004/T005/T007 不破)?
- **器官边界 / OUT-10** — 改动如何最小化对 004 PriceDataProvider 的冲击;是扩 PITPriceProvider(009 自有契约 ·
  可改)还是碰 004 已 ship 签名(禁);T012 调用层能否用现有 provider 两次调用重组(entry raw@entry as_of ×
  factor@exit as_of)而**不改 provider 签名**(若可行则更轻,守 OUT-10 更干净)。

## Z · 参照系
- mode: 不对标(forge-lite · 契约方向已定 · 不重刷 PIT 数据模型 SOTA — v1 已做)

## W · 产出形态(1)
- **refactor-plan** ✅ → provider 双轴契约的最小改造方案:新接口签名(或调用层重组方案)+ 向后兼容策略 +
  T012 收尾指示 + 落哪个仓(009 契约改归 XenoDev spec + provider,IDS 侧 PRD/spec 契约同步)+ 可测验收。
  (verdict-only / decision-list / next-PRD / free-essay 未勾)

## K · 用户判准

> handback-review 009 已决议 T012 的两项:
> **决议项 1**:entry 价语义 = **A「执行时可见」(PIT 严格)** —— entry raw close 按 entry as_of 取
> (不含 entry 后修订)、复权 factor 按 exit as_of 取,adjusted = entry_raw(@entry) × factor(@exit)。
> **决议项 2**:需分离价格版本轴与复权因子轴 —— 但**具体契约形状留 forge 定**。
>
> **要你们定死的**:
> 1. 分离双轴的**最干净接口形状** —— 三选一(或更好):(a) `get_adjusted_close` 加第三参数
>    `factor_as_of`(price 版本轴用 query_as_of,factor 用 factor_as_of);(b) 拆成两个原子读
>    (`get_raw_close(as_of)` + `get_factor(as_of)`)调用层自算;(c) T012 调用层用现有 provider 两次调用重组,
>    **provider 签名不动**(若技术可行则最守 OUT-10)。评估哪个既解 R6 又最小冲击。
> 2. **向后兼容**:T004/T005/T007 现有单 query_as_of 调用不能破(默认 factor_as_of=query_as_of 退化为旧行为?)。
> 3. **OUT-10 边界**:改的是 009 自有的 PITPriceProvider(可改)还是碰 004 已 ship 的 PriceDataProvider(禁)?
>    CurrentStatePriceProvider(T008 · 桥接 004)受不受影响?
>
> **binding**:① 死守 operator 已定的选 A(执行时可见),不重议语义;② 最小冲击优先(能调用层重组不改签名
>    最好);③ 不破 v1/v2 verdict + 不破已 ship 的 M1 数据层(T001-T007);④ T012 靠此契约解 BLOCK,契约要能
>    直接指导 T012 收尾 + 可能的 provider FU-task;⑤ 轻收尾(forge-lite · 可执行优先)。

## 收敛模式
strong-converge → 单一 verdict(单一契约方案)+ 残余降级 v0.2 note
