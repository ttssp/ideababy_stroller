# Forge 008 · v3 · P3R1 · Opus 4.8 Max(联合收敛 R1)

**读取**:P2-GPT55xHigh.md(对方,新读)+ 双方 P1+P2(refresh)。无 moderator-notes。**NO new search this round.**

## §1 · 整合摘要

双盲两轮后,两位审阅人在**结构层完全收敛**,且 GPT P2 补了一个 load-bearing 的安全约束。整合如下:

- **架构形态(双方一致)**:3 候选**不是三选一,是一条管线的分层组合** ——
  **③控制流(agent 出 declarative plan → operator 确认)＋ ②白名单 credential broker/runner 执行基座(持 key、按白名单抓取、落盘)＋ ①侦察兵/fallback(诊断列表缺口、指方向)**。
- **凭据隔离的真机制(双方一致)**:agent 不持 key 只是第一层;**第二层 = broker 必须是 capability-scoped 连接器**
  (固定源 + 端点白名单 + 参数 schema + 请求预算),**不是通用 HTTP 代理**。GPT P2 的关键反驳:「broker/sidecar
  并不天然安全 —— 盲转发 agent 给的任意 URL = 只是把 key 从 agent 挪到一个可被 agent 滥用的代理」。SOTA
  (Secretless connector / Vault Agent / MCP capability control)印证这一层。
- **协议层(双方一致)**:SHARED-CONTRACT **§2 需补「采集会话凭据隔离」子条款**(现字面只到 deployment
  secret);**§1 PRD schema 不动**。
- **C5(双方一致)**:OUT 侧渠道中性 **keep**,本轮**不重写 C5**;新增的是 **IN 侧采集架构约束**。
- **silent-checkpoint(GPT P2 新增,我接受)**:分页须落盘 cursor/页边界/重试来源供 agent 只读审计,否则
  silent drift —— 直接对齐 v0.1 **C7「不静默丢」**。这是把抽象凭据边界接回 v0.1 既有护栏的关键一笔。

## §2 · 我的初步 verdict(单段,不 hedge)

**GO（分层架构）**:自动翻页能力**可在凭据隔离硬约束之下落地**,形态 = **agent 只产可审计的 declarative
plan（源/端点/参数/页上限/预算）→ operator 一键授权 → 隔离的 capability-scoped credential broker/runner
持 operator 登录态、按端点白名单抓取、把内容＋分页 checkpoint 落盘 → agent 只读落盘结果**。持 key 主体 =
broker/runner，与 agent context **物理隔离**（独占 userDataDir/storageState，agent 无文件读权限 + 日志脱敏）；
信任边界划在「agent 产意图、broker 持凭据并执行、二者不互穿」。**①侦察兵保留为诊断/fallback 层**（列表 API
够得到时降 operator 手动成本）。**协议层须补 §2 采集会话凭据隔离子条款（broker 端点白名单 + agent 不经手运行
时采集凭据），§1 不动，C5 OUT 侧 keep**。残余分歧无；唯一外部未知（列表截断根因）以**条件分支**兜（见 §3）。

## §3 · 关键分歧清单

**§3 无 reviewer 分歧 —— 双方 P1→P2 已在结构、凭据机制、协议层、C5 处理全部对齐**（GPT P2 §3 末句与我 §2
verdict 逐项同向）。R2 重点不在消分歧,在**把 verdict 落成 4 件 W 产物草案**。

唯一须 R2 处理的不是分歧而是**一个外部事实未知**（双方 P1 §3 共同标注,非对立立场）：

- **列表截断 2025-07-21 根因未定**：分页 cursor 未续（翻页能解）vs 列表 API 服务端物理不返回 2026（翻页无效,
  只能 detail 入口批量发现）。**双方一致认为这是外部数据问题,非架构选择问题**。R2 verdict 须对两种根因都给
  路径：**主路径 = 分层翻页架构**（假设分页可续）；**条件分支 = 若实测 API 物理截断,broker 的抓取目标从
  「列表翻页」切到「detail 入口批量发现」,分层架构与凭据边界不变,仅 broker connector 的端点白名单换一组**。
  → 建议 operator 在 L4 实装前用一次实测确认（看响应有无 `has_more`/`next_cursor`、offset 越界返回空 vs 报错）。

## §4 · 与 K 的对齐性自检

- ✅ **K 核心问题「凭据隔离之下自动翻页是否/如何落地」** → verdict 正面回答：可落地,形态 = 分层 broker 架构。
- ✅ **K binding「合规 operator 担责,不审」** → 全程未审是否违法/ToS/规避访问控制；Z 未跑法律检索。
- ✅ **K binding「凭据隔离 non-overridable,不论证放宽」** → verdict 在硬约束**之下**设计（agent 不持 key、
  不发请求）,未论证放宽；反而把隐式约束**显式化**为协议子条款,强化而非松动。
- ✅ **K binding「v0.1/v0.2 不重审」** → 未触碰已 ship 实现；silent-checkpoint 是**新增 IN 侧约束**,接 C7 但不改 C7。
- ✅ **K#1 持 key 主体怎么设/信任边界** → broker/runner 持 key,独占会话,边界 = agent 产意图 vs broker 执行,不互穿。
- ✅ **K#2 3 候选向选哪/混** → 分层组合（③控制流＋②broker 基座＋①侦察兵）,非三选一。
- ✅ **K#3 是否触及 §1/§2 协议层修订＋改动边界** → §2 补采集会话凭据隔离子条款（broker 白名单＋agent 不经手
  运行时采集凭据）；§1 不动。改动边界精确,留 W=协议修订草案落字。
- ⚠ **残留**（非 K 偏离,是外部未知）：列表截断根因须实测；一键确认粒度（GPT §3#3）影响 O5b 单一恢复路径,
  R2 须给判准（避免太粗=隐藏全自动 / 太细=回到手动）。
