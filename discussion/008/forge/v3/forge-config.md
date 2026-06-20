---
forge_version: v3
created: 2026-06-19T23:42:37Z
convergence_mode: strong-converge
x_hash: ec36f97e8ff858302f86e581d7112535
prefill_source: manual
---

# Forge Config · 008 · v3

## X · 审阅标的

本轮 forge 由 operator 触发,议题源 = XenoDev `dogfood-backlog.md` 末尾条目
**「operator 治理诉求:放宽采集面到『自动翻页』(去掉『不主动发请求』半自动约束)」**
(commit `6f1a0df`,已 push origin/main)。

**议题一句话**:实战采集「2026 起全历史库」暴露 —— moduleContentList 列表接口只吐到
**2025-07-21(contentId 164966)**;2026 的内容(176375/176384,6-17)仅在 operator
「点开单篇 detail」时被动抓到,**不在任何已抓列表页**。operator「在 App 里手动滑列表找
2026 入口很慢」,明确要求「改红线,自动翻页没问题」。**核心拦路虎不是 C5,而是凭据隔离**:
自动翻页须带 operator 登录态发请求,而登录态绝不进 agent context —— agent 物理上无法以
operator 身份发请求。本轮 forge 在该硬约束**之下**论证「怎么做」,而非论证是否放宽它。

> ⚠ **跨仓快照说明**:议题主源(XenoDev `dogfood-backlog.md` 条目)+ 被挑战的硬约束源
> (XenoDev `framework/SHARED-CONTRACT.md` §1+§2)物理上在 XenoDev 仓
> (`/Users/admin/codes/XenoDev/...`),Codex 沙箱大概率不可达。故 operator 决议把二者
> **快照进 `discussion/008/forge/v3/_external/`**(同 v2 做法),两位审阅人读同一份本仓内容,
> 避免沙箱 BLOCK。快照保真(`sed` 切片 + 原文),snapshot header 标 source/sha256/git-HEAD
> 保 audit trail。

### 解析后的标的清单

**IDS 本仓(✅ 可达):**
- `discussion/008/008-pB/PRD.md` —— **现行 PRD v1.2**(C5:133 渠道中性原则 / 采集架构描述 /
  v0.1 半自动被动监听落点)。⚠ **版本校正**:operator intake 写「v1.1」,但 forge v2 verdict
  已落地把 PRD bump 到 **v1.2**(2026-06-16,Obsidian US8 + C5 渠道中性)。双专家读的 C5 基线
  是 **v1.2 的 C5 渠道中性条款**(line 172 增补),非 v1.1。类型:本仓库文件。
- `discussion/008/forge/v2/stage-forge-008-v2.md` —— forge v2 verdict(C5 **渠道中性原则**在此
  定基线:「自用不传播 —— 原内容不得进入会被传播/同步的衍生渠道」)。本轮自动翻页是采集侧的
  **新议题**,v2 渠道中性管的是采集**之后**的衍生渠道(vault),二者边界不同 —— 双专家须分清
  「采集面放宽(进)」vs「衍生渠道传播(出)」是两件事。类型:stage 文档。

**XenoDev 快照(✅ 可达 · 已拷进 `_external/`):**
- `_external/XENODEV-dogfood-backlog-autopage-entry.md` —— **议题主源**。含:实战边界硬证据
  (列表止于 2025-07-21 / 2026 仅 detail 可达)+ 「为何是框架级 + 为何拒绝当场改」3 条
  (C5 是 spec 项目约束改它须回 IDS / **真拦路虎是凭据隔离 non-overridable IAM 级** / dogfood
  铁律不当场改安全边界 = 防 V4 失败模式)+ **3 候选决议向**(① 维持半自动 + agent 侦察兵 /
  ② 受控自动翻页 daemon 持 key / ③ 混合:agent 出翻页计划 + operator 一键确认 + 持 key 进程执行)。
- `_external/XENODEV-SHARED-CONTRACT-s1-s2.md` —— SHARED-CONTRACT §1+§2(被本议题挑战的硬约束源)。
  ⚠ **嵌入事实校正注(snapshot header,给双专家)**:§1 = PRD schema(字段约定);§2 = Safety
  Floor 三件套(件1 production credential 物理隔离 / 件2 不可逆命令 hard block / 件3 备份破坏检测)。
  **§2件1 是「凭据隔离」最接近的成文条款,但其 scope 是 `.env.production` / `secrets/production/`
  / `prod://` 这类【部署密钥不进 agent context】—— 并非字面写「顾问平台采集会话登录态 cookie 不进
  agent context」**。即:K 里「登录态绝不进 agent context」是 §2件1 在**采集域**的解读/外推,
  §1+§2 原文未字面覆盖采集会话凭据,更无「半自动采集原则」成文条款。**这道 written-constraint
  vs 实际诉求的落差本身是 v3 该解的题之一**(见 K 第 3 点:§2 措辞是否需扩展)。

> ⚠ **采集会话凭据隔离的"实装"在哪**(供双专家定位,非 binding):XenoDev `.claude/safety-floor/
> credential-isolation/scan-credentials.sh` 是 Safety Floor 件1 的落地脚本,parallel-builder
> SKILL §0.2 对 task `file_domain` 真跑 scan(fail-closed)。但它扫的是 `.env.production` 类
> **文件模式**,**不是**运行时「采集进程持 operator cookie 发请求」这件事 —— 二者是不同层。
> 当前「半自动被动监听(`src/capture/addon.py` 旁路 mitmdump,operator 手动浏览触发落盘)」
> 架构使 agent **物理上**不经手登录态;自动翻页若引入持 key 主体,这条物理隔离就需要新的边界设计。

## Y · 审阅视角

✅ **架构设计 / 数据流边界**(本轮主轴)—— 3 候选架构向(① 半自动 + 侦察兵 / ② 独立采集 daemon
   持 key / ③ agent 出计划 + operator 确认 + 持 key 进程执行)选哪个 / 怎么混?**持 operator 登录态
   发请求的主体怎么设、信任边界划在哪**?若引入 daemon,daemon↔agent 的落盘接口(agent 只读不写、
   只读 daemon 落盘、不经手 key)怎么定?自动化程度 vs 信任边界清晰度的取舍。
✅ **安全 / 凭据边界**(本轮主轴)—— 凭据隔离硬约束「登录态绝不进 agent context」在自动翻页下
   **怎么保**?agent 不持 key、不直接发请求的**可验证保证**是什么(而非口头承诺)?持 key 主体的
   最小权限边界(只读列表/detail,不碰写操作)。速率/源白名单治理是否属本轮(还是 L4)。

> ⚠ **operator 显式姿态(binding · 见 K)**:**自动翻页对此顾问平台的【合规性】由 operator 拍板
> 并担责 —— 不是本轮 forge 的审议对象**(沿用 v1/v2 binding,见 v2 stage line 39/62)。双专家
> **不得**论证「自动翻页是否违法 / 是否踩平台 ToS / 是否规避访问控制 / DMCA§1201」。把「合规由
> operator 负责」当**已决前提**输入。本轮**只审【架构与凭据边界】**:即「在凭据隔离硬约束之下,
> 自动翻页这个能力的主体/信任边界/数据流怎么设计」。

## Z · 参照系

mode: 对标 SOTA(架构 / 凭据边界层)

> Phase 2 检索**受控采集 / 凭据隔离架构**的 prior-art 与失败案例,**不跑法律检索**(合规由
> operator 负责)。建议 ≥3 检索方向:
> - **独立采集 daemon / sidecar 持凭据,主进程只读落盘**的工业做法(credential broker /
>   token sidecar / 凭据代理模式;如 Vault Agent sidecar、cloud metadata proxy 等隔离范式)
> - **浏览器自动化 + 已认证会话**怎么做凭据隔离(Playwright/Puppeteer persistent context、
>   authenticated session 复用、cookie jar 隔离;以及「agent 编排但不经手 cookie」的模式)
> - **自动翻页 / 分页抓取**的工程坑与失败案例(速率触发风控、列表接口截断的常见绕法、
>   增量抓取的 cursor/offset 边界)
> 双专家可在架构层引用这些 prior-art 判断 3 候选向的成熟度与信任边界清晰度,但**不强制对标
> 具体竞品**,**不得跑法律判例检索**。

## W · 产出形态

✅ **verdict-only** —— 浓缩 verdict + 简短 rationale(≤500 字):3 候选架构向选哪个(或怎么混)+
   持 key 主体/信任边界的一句话定性 + 是否触及 §1/§2 协议层措辞修订的 go/no-go,一段话给立场不 hedge。
✅ **decision-list** —— 4 列矩阵(保留 / 调整 / 删除 / 新增):把本轮所有可决项理清 —— 当前半自动
   被动监听架构(保留?)、agent 侦察兵能力(新增?)、持 key daemon(新增/拒绝?)、agent 出
   翻页计划 + 一键确认(新增?)、SHARED-CONTRACT §2 措辞扩展到采集会话凭据(调整?)、C5 scope
   是否需配套动(调整?)、速率/源白名单治理(新增/L4?),每项落到 keep/refactor/cut/new 一格。
✅ **协议修订草案**(W 含 — 对应 K 第 3 点)—— 若 verdict 触及 SHARED-CONTRACT §1/§2 协议层,
   产**具体措辞修订草案**:§2 是否新增「采集会话凭据隔离」子条款(明确 agent 不经手运行时采集凭据 ·
   持 key 主体须独立于 agent context · 最小权限)?改动边界精确到「加哪段/改哪句」,而非泛泛说「要改」。
   若 verdict = 不触及协议层(现有 §2件1 外推已足),则显式写「§1/§2 无需改 · 理由」。
✅ **next-PRD** —— 若 verdict 改动采集架构 / C5 scope(采集面从「半自动被动」放宽到「受控自动翻页」
   是否需 PRD 显式记?),产 **PRD 采集架构 + C5 章节的下一版草案**,可直接回流改
   `discussion/008/008-pB/PRD.md`。若 verdict = 架构不变(维持半自动 + 仅加侦察兵),则 next-PRD
   退化为「PRD 无需改 · 理由 + 仅 backlog 记侦察兵能力」。

> **W 四件套**(2026-06-19 operator 调整:原选全 6 形态 → 砍掉 refactor-plan(偏 L4 工程,
> XenoDev 在 verdict 后决 addon/daemon 模块切分)+ free-essay(治理决议要结构化 verdict 而非散文))。
> 四者职责互补:verdict-only 给浓缩立场、decision-list 给可决项全景、协议修订草案给 §1/§2 措辞
> 落地、next-PRD 给 PRD 回流草案。本轮是**治理决议型 forge**,产物须可直接落到协议层 + PRD。

## K · 用户判准

**核心问题**:实战采集「2026 起全历史库」暴露 —— 列表接口止于 2025-07-21,2026 内容仅逐篇点
detail 可达,operator 手动找历史入口成本高。operator 要求引入「自动翻页」补齐历史。**在不违反
凭据隔离(三件硬约束①:登录态绝不进 agent context · non-overridable)的前提下,这个能力是否/
如何落地?**

**binding 前提(双专家不得审议):**
- **自动翻页对此顾问平台的【合规性】由 operator 拍板并担责**(沿用 v2 line 39/62 binding)。
  不审是否违法/踩 ToS/规避访问控制。本轮只审【架构与凭据边界】。
- **凭据隔离是 non-overridable 硬约束:登录态绝不进 agent context**。任何方案不得让 agent 直接
  持 key 发请求。这是地基,**不在本轮论证是否放宽 —— 而是论证「在它之下怎么做」**。
- **v0.1/v0.2 已 ship 是事实**,本轮不重审已交付实现。

**operator 最在乎的(架构/数据流层,这才是双专家该审的):**
1. **持 key 主体怎么设、信任边界划哪** —— 自动翻页须有「持 operator 登录态发请求的主体」。凭据
   隔离禁 key 进 agent,但**未禁** operator 授权的独立采集进程持 key —— 这个主体怎么设?信任边界
   划在哪?(agent 编排 vs 经手凭据的物理分界)
2. **3 候选架构向选哪个/怎么混**:
   - ① **维持半自动 + agent 当侦察兵**(只分析 addon 落盘指方向,operator 仍手动翻 —— 把盲滑变
     定向滑,降 operator 手动成本,安全边界最清晰)
   - ② **独立采集 daemon 持 key 自动翻页,agent 只读其落盘**(引入新信任边界:daemon↔agent)
   - ③ **agent 出翻页计划(参数序列)→ operator 一键确认 → 持 key 进程执行**(agent 不持 key、
     不直接发请求,但自动化程度提升)
3. **是否触及 SHARED-CONTRACT §1+§2 协议层措辞修订** —— 若是,改动边界是什么?

## 收敛模式

strong-converge —— 必须 finalize 单一 verdict(3 候选架构向选定一个主向 / 持 key 主体与信任边界
定性 / §1·§2 协议层是否改 + 改动边界 / C5 scope 是否配套动)。残余分歧降级为 note。沿用 v1/v2
收敛强度。
