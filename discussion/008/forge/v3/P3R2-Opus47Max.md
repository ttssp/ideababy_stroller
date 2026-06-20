# Forge 008 · v3 · P3R2 · Opus 4.8 Max(finalize · strong-converge)

**读取**:P3R1-GPT55xHigh.md(对方,新读)+ 自己 P3R1 + forge-config(convergence_mode=strong-converge)。无 moderator-notes。

## §1 · 我对每条分歧的最终立场 + 让步

**无 reviewer 分歧需消解** —— 双方 P3R1 §3 均显式判「无」,且 GPT P3R1 §2 verdict 与我 P3R1 §2 逐字同向
(同一架构形态、同一协议层处理、同一 C5 处理)。本节记录我对两个**非分歧待定点**的最终立场(均采纳 GPT 措辞):

- **列表截断根因 → 采纳条件分支(双方一致)**。最终 verdict **不卡实测**:默认路径 = broker 按
  `cursor`/`next`/`checkpoint` 翻页;若 L4 实测 API 物理截断(响应无 `has_more`/`next_cursor`、offset 越界
  返回空),broker 的能力白名单切到「detail 入口批量发现」,**架构与凭据边界零改动,仅换一组端点白名单**。
  我**让步**:P2 时我倾向「建议 operator 先实测」,GPT 主张「不卡实测、写成条件分支」更对 —— 采纳 GPT,
  实测降为 L4 实装前的一次性确认动作,不阻断 verdict。
- **一键确认粒度 → 全采纳 GPT 的 bounded-capture-batch 判准**。**每个 bounded capture batch 一次确认(非每页)**,
  确认内容须含【源 + 时间窗/目标范围 + 端点集合 + 最大请求预算 + 停止条件 + 落盘位置】六要素。**定时任务**
  须另有 operator 预授权的固定 schedule/budget/kill-switch,**agent 不得临时扩大**。这条同时解了 O5b:一次
  batch 确认 = 一次 operator 介入,可量化,不破「介入次数趋近零」目标。

## §2 · 联合 verdict(单一)

**GO（分层架构）· 自动翻页能力在凭据隔离硬约束之下可落地,形态为三层分离:**

**① 控制流层**:agent 只产**可审计的 declarative plan**(源 / 时间窗 / 端点集合 / 参数 schema / 最大请求预算 /
停止条件 / 落盘位置),**不持 key、不发请求**。**② 执行基座层**:operator 一键授权后,**隔离的 capability-scoped
credential broker/runner** 独占 operator 登录态(独占 userDataDir/storageState · agent 无文件读权 · 日志脱敏),
**按端点/参数白名单**抓取 —— **绝非通用 HTTP 代理**(broker 不盲转发 agent 给的任意 URL),并把内容＋分页
checkpoint(cursor/页边界/重试来源)落盘。**③ 侦察兵/fallback 层**:agent 分析已落盘数据诊断列表缺口、指方向,
列表 API 够得到时降 operator 手动成本。**持 key 主体 = broker/runner,与 agent context 物理隔离;信任边界 =
「agent 产意图 vs broker 持凭据并执行」二者不互穿,broker 端点白名单是防 agent 滥用持 key 进程的核心闸。**
**协议层:SHARED-CONTRACT §2 新增「采集会话凭据隔离」子条款(agent 不经手运行时采集凭据 + broker capability
白名单 + checkpoint 落盘可审计);§1 PRD schema 不动;C5 OUT 侧渠道中性 keep,仅补一句 IN/OUT 边界说明。**
确认粒度 = 每 bounded capture batch 一次(六要素)。**无 unresolved。**

## §3 · 残余分歧降级为 note

无 reviewer 分歧可降级。以下是**非分歧的残余 attention 点**(降级为 L4/note,不阻断 verdict):

- **note-1(外部未知)**:列表截断根因须 L4 实装前一次实测确认。条件分支已兜,实测只是选定主路径 vs detail 分支。
- **note-2(L4 工程)**:broker/runner 用 Playwright persistent context 还是别的认证会话隔离手段,是 L4 实装选型,
  本 forge 未定(SOTA 给了 persistent context 作候选,非强制)。
- **note-3(速率/源治理)**:请求预算/速率上限的具体数值属 L4 + operator 调参;本轮只定「plan 须含最大请求预算 +
  停止条件」这一**结构要求**,不定数值。
- **note-4(协议层级定位)**:§2 子条款写进 SHARED-CONTRACT(对所有 XenoDev 采集类项目生效)= 我建议的层级;
  若 operator 只想要项目级(仅 008-pB),退为 PRD/spec 约束 —— 这是 operator 决策点,W=协议修订草案会标两个选项。

## §4 · W 形态产出的初步草稿建议(逐项对应 forge-config.W)

**W1 · verdict-only**(≤500 字):用 §2 联合 verdict 浓缩。一句话版:**「agent 只产可审计计划 → operator 一键
授权 → 隔离的白名单 broker/runner 持登录态按端点白名单抓取并 checkpoint 落盘 → agent 只读结果;§2 补采集会话
凭据隔离子条款,§1/C5 不动」**。

**W2 · decision-list**(4 列矩阵 keep/refactor/cut/new):
- **keep**:半自动被动监听架构(默认路径保留)· v2 C5 OUT 侧渠道中性 · §1 PRD schema · v0.1 三护栏(C7 等)
- **refactor**:「②daemon 自动翻页」重述为「capability-scoped 白名单 broker/runner」· C5 补一句 IN/OUT 边界说明
- **cut**:②作为「无确认全自动常驻翻页产品形态」出局(只作受控执行基座)· broker 作通用 HTTP 代理的任何形态出局
- **new**:③控制流(agent declarative plan + operator 确认)· broker 端点/参数白名单闸 · 分页 checkpoint 落盘(接 C7)·
  ①agent 侦察兵诊断层 · §2「采集会话凭据隔离」子条款 · bounded-capture-batch 六要素确认判准

**W3 · 协议修订草案**(对应 K#3):产 SHARED-CONTRACT §2 **新增子条款的具体措辞草案**,须覆盖:
(a) agent 不经手运行时采集会话凭据(登录态只在隔离 broker/runner,agent 无文件读权);(b) broker 必须
capability-scoped(固定源 + 端点白名单 + 参数 schema + 请求预算 + 停止条件),不得作通用代理盲转发;
(c) 分页/抓取须 checkpoint 落盘可审计(对齐 C7 不静默丢);(d) 确认粒度 = bounded capture batch 六要素;
(e) 定时任务须 operator 预授权固定 schedule/budget/kill-switch。**标层级二选**:协议级(SHARED-CONTRACT,推荐)vs
项目级(008-pB)。§1 显式写「不改 + 理由」。

**W4 · next-PRD**(对应采集架构变更):产 008-pB PRD **采集架构 + C5 章节的下一版草案** —— 采集面从「半自动
被动」扩到「受控自动翻页(分层 broker 架构)」是否须 PRD 显式记?建议:PRD §采集架构加一段「v0.2+ 受控自动
翻页(分层架构,持 key 主体隔离)」+ C5 补一句 IN/OUT 边界(IN 侧采集手段扩展不松动 OUT 侧渠道中性)。
若 operator 判「这属实装细节、PRD 不必记」→ next-PRD 退化为「PRD 无需改 + 仅 backlog/spec 记」,理由附上。
