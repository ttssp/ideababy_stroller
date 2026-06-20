# PRD · 008-pB · "投资顾问内容自动采集 → 个人知识库(全形态)" (phased)

**Version**: 1.3  (forge v3 verdict 驱动修订 · human-approved)
**Created**: 2026-06-04T02:14:35Z
**Last revised**: 2026-06-20 (forge v3 · 受控自动翻页分层架构 + 采集会话凭据隔离)
**Source**: discussion/008/L3/stage-L3-scope-008.md · Candidate B「全形态 · 原始证据库」
**Approved by**: human moderator
**PRD-form**: phased
**Phases**: [v0.1, v0.2]
**Phase-current**: v0.1

> ⚠️ **本 PRD 对 stage doc 原始 Candidate B 有两处 operator 授权偏离**(见 FORK-ORIGIN.md):
> 1. **phase 排序按"价值优先"**:v0.1 = 图文 + 回放,v0.2 = 加预警(非原"v0.1 图文+预警/v0.2回放")。
> 2. **回放 v0.1 即做文字摘要**(非原始 B 的"存文件不转写")—— 依 operator 补充意图。

> 🔧 **v1.1 修订(2026-06-05 · forge v1 verdict 驱动 · 见 discussion/008/forge/v1/stage-forge-008-v1.md)**:
> 008-pB 的 Phase 0 探针曾判 FAIL(回放「合规下不可达」),被 operator 证伪 —— 探针把
> 「浏览/截屏」误当「采集」,且把「付费有效登录态抓自己流量」误判成「规避访问控制」。
> forge v1(converged · strong-converge)verdict = **refactor-and-reset**,本次修订落地四项:
> ① **C5 措辞改写**(「正常能看到」→「有权访问 + 有效登录态采集原内容」);
> ② **回放 scope 复位**(撤销「图文先走、回放移 v0.2」依据,回放留 v0.1);
> ③ **token 失效介入成本升为显式 v0.1 outcome**(operator 选定档位 = 失效时扫码一次);
> ④ **Phase-0 探针 gate 判准改向**(「合规可达性」→「自动化稳定性/低维护恢复」)。
> **合规边界由 operator 负责**(operator 已就「付费订阅 · 有效登录态抓自己合法流量 · 自用不传播」
> 的合规性拍板并承担责任);本修订只改产品措辞与判准,不替 operator 做法律判断。
> operator 同期拍板 3 个产品决策点:token 阈值=失效扫码一次 / 回放摘要须含稳定时间戳 / 三形态共享登录态。

> 🔧 **v1.2 修订(2026-06-16 · forge v2 verdict 驱动 · 见 discussion/008/forge/v2/stage-forge-008-v2.md)**:
> v0.1(图文+回放)已 ship(T101-T112,406 test 绿)后,operator 经 XenoDev 尝鲜提出把 **Obsidian
> 个人知识库前端**定为 US8 实现方向。forge v2(converged · strong-converge)verdict = **GO**,本次修订落地五项:
> ① **US8 实现载体锚定**(Obsidian vault:Calendar=统一时间线 / `reviewed`=已看未看 / 双链=长内容不进 backlog);
> ② **C5 增补渠道中性原则**(自用不传播 —— 原内容不得进入会被传播/同步的衍生渠道,覆盖 git + iCloud/Obsidian Sync;**不溯及 v0.1 已 ship 落点**);
> ③ **UX principle 复位**(原「不做 PKM 式双链/图谱」与 v0.2 双链方向矛盾,已复位);
> ④ **v0.2 Scope IN/OUT 增补**(库→vault 单向 exporter;原文进 vault / 双向同步 / 依赖可写脚本三条新 OUT);
> ⑤ **v0.2 验收 outcomes 增补**(O8/O9/O10)。
> **SQLite 仍是唯一 SSOT**(v0.1 三护栏 allowlist/C7/source_id 反作弊保留);①替换 SSOT、③双向同步永久出局。
> 合规定性仍由 operator 负责(沿用 v1 binding);forge v2 只审产品 + 数据流边界,未审工程可行性(回放管线之上加导出层的工作量是 L4 才能答的真风险)。

> 🔧 **v1.3 修订(2026-06-20 · forge v3 verdict 驱动 · 见 discussion/008/forge/v3/stage-forge-008-v3.md)**:
> v0.2 实战采集「2026 全历史库」暴露**列表接口止于 2025-07-21**(2026 内容仅逐篇 detail 可达),operator
> 要求引入**自动翻页**补齐历史。真正拦路虎是**凭据隔离**(登录态绝不进 agent context · non-overridable),
> 非合规。forge v3(converged · strong-converge)verdict = **GO(分层架构)**,本次修订落地四项:
> ① **受控自动翻页 = v0.2+ Scope IN**(分层采集架构:agent 出可审计 plan → operator 授权 → 隔离
>    broker/runner 持登录态执行 → agent 只读落盘;agent **不持 key、不发请求**);
> ② **两种授权粒度并存**:交互式 bounded-batch 确认(默认)+ **预授权式全自动**(operator 选开 ·
>    固定 schedule/budget/kill-switch · agent 不得动态扩大 · 配失败显式可见对齐 C7);
> ③ **3 条新 Scope OUT 红线**(agent 持 key/发请求 · broker 作通用 HTTP 代理盲转发 · agent 动态扩大授权);
> ④ **C5 追加一句 IN/OUT 边界**(自动翻页属 IN 侧采集手段,不松动 OUT 侧渠道中性)+ **新增 O11**(凭据隔离可验收)。
> **合规定性仍由 operator 负责**(沿用 v1/v2 binding);forge v3 只审架构 + 凭据边界,**未审 broker 工程实装
> 复杂度 + 列表截断根因**(分页未尽 vs API 物理截断,须 L4 实装前实测 —— 见 Scope IN 自动翻页段 Open notes)。
> ⚠ **协议层联动**:本修订的凭据隔离原则同步要求 XenoDev `SHARED-CONTRACT.md §2` 新增「采集会话凭据隔离」
> 子条款(协议级 · 措辞草案见 stage-forge-008-v3.md §"协议修订草案")—— 该改动跨仓在 XenoDev,不在本 PRD 内。

## Problem / Context

operator 付费订阅了一个微信投资顾问(在微信小程序里发布)。顾问每天产出**图文资讯**(以文字为主、
图片少,图片多为数据补充或偶尔搞笑),不定时发**盘中关键预警**,每周几次发**直播回放**(1-2 小时视频,
内含重要消息、周度复盘、下周重要事件展望与策略预备)。

痛点:operator 工作日没时间实时盯小程序,直播回放更是没时间看完 1-2 小时;人工收集易漏、散、难复用。
008 = 一个**自动采集这些内容、沉淀成 operator 个人知识库**的程序,作为 **004 投资决策智能体的上游
数据采集模块**。008 只负责"把顾问发的东西完整、及时、省心地收进来并可消费",**不产生投资决策**(那是 004)。

最终形态(v0.2 达成):图文 + 预警 + 回放三形态全收,一件不漏。本 PRD 分阶段抵达该形态。

## Users

operator 本人,自用,不商业化。具体画像:中年、有家庭财务责任、ML 方向 CS PhD(但本工具不需他懂技术
运维)。付费订阅一个微信投顾,信任其内容、想长期留存。工作日难实时盯盘,愿异步消费。同时持美/港/A 股,
集中看 30-50 只股票。已踩过手动监听维护成本高、易失效的坑,核心诉求是"更自动、最小化操作"。

## Core user stories

| # | As a | I want | So that | Phase target |
|---|------|--------|---------|--------------|
| US1 | operator | 顾问发的**图文资讯**被自动收下、零漏 | 我不用手动翻小程序 | v0.1 |
| US2 | operator | 顾问的**直播回放**被自动转成几分钟可读的**文字 + 关键点摘要** | 我不用看完 1-2 小时视频也能掌握重要消息/复盘/下周策略 | v0.1 |
| US3 | operator | 每个回放关键点能**溯源回原始转录 + 视频稳定时间戳** | 我能确认这是顾问说的、不是程序编的,且能跳回视频原位复核 | v0.1 |
| US4 | operator | 任一形态采集**失败/不确定时我立刻看到**(按天可见缺口) | 我对"没漏"有把握,而非静默漏掉 | v0.1 |
| US5 | operator | 按**日期/形态/标的**回看顾问内容 | 复盘时能快速找到 | v0.1 |
| US6 | operator | 把收下的内容(轻量格式)**喂给 004** | 004 能引用顾问观点做决策 | v0.1 |
| US7 | operator | 顾问的**盘中预警**被自动收下并**及时通知** | 有时效的预警漏了就没价值 | v0.2 |
| US8 | operator | 三形态在**统一时间线**回看,标记回放已看/未看 | 长内容不消失进 backlog | v0.2 |

## Scope IN

### Scope IN — v0.1
- 单一指定顾问的**图文资讯**自动采集(文字为主;**图片只原样留存,不费力解析**)。
- 单一顾问的**直播回放**自动采集 + **转文字 + 关键点摘要**(可几分钟消费;关键点可溯源原始内容)。
- 轻结构化沉淀(时间 + 标的/主题标签 + 原文/原始转录)。
- **采集失败 / 不确定状态显式可见**(按天可见缺口),不静默丢失。
- 按日期/形态/标的检索。
- 给 004 的**轻量输出包**(粗约定:发布时间、形态、原始内容/转录、关键点、涉及标的、采集状态)。
- **进入 v0.1 主开发前的第 0 阶段探针**(见 §关键前置 gate)。

### Scope IN — v0.2
- 加**盘中预警**自动采集 + **及时通知** → 达成全形态(图文+回放+预警)。
- 统一时间线(三形态合并视图)+ 回放已看/未看状态管理。
- 较完整的 004 输出契约(在 v0.1 粗约定基础上补全)。
- (候选,待 v0.1 反馈后定)更深的结构化检索 / 全文搜索。

#### v0.2 增补(forge v2 verdict · 见 stage-forge-008-v2.md)

> 🔧 **US8 实现载体**:Obsidian vault。
> - 统一时间线 = Calendar/Bases 插件按 `published_at` 排布
> - 回放已看/未看 = frontmatter `reviewed` 布尔字段
> - 长内容不消失进 backlog = 标的双链 `[[标的]]` 反链聚合
> SQLite 仍是唯一 SSOT;Obsidian 是人读衍生前端,不替换库。

- **Obsidian vault as US8 carrier**:`SQLite 库 → vault` 单向 exporter(vault 只读衍生,不回写库)。
  - frontmatter 白名单字段 = `source_id` / `published_at` / `form` / `capture_status` / `raw_ref` / `source_url_canonical` / `tickers` / `reviewed`
  - body 仅摘要级 `key_points` / `source_ref` + 标的双链 `[[标的]]`
  - vault 目录强制 git-ignored,经 `_assert_c5_safe_out_dir` 守卫(复用 v0.1 C5 机制)
  - **bounded scope**:不挤掉 US7;与 US7 盘中预警、完整 004 契约并列属 v0.2(build 先后由 L4 排,forge 不定)

#### v0.2+ 增补(forge v3 verdict · 受控自动翻页 · 见 stage-forge-008-v3.md)

> 🔧 **受控自动翻页(补齐历史库 · 分层采集架构)**:采集面从「半自动被动监听」扩到「受控自动翻页」,
> 补齐 addon 被动监听够不到的历史列表页(实战:列表接口止于 2025-07-21,2026 内容仅逐篇 detail 可达)。

- **分层采集架构(三层分离 · 凭据隔离地基)**:
  - **① 控制流层(agent)**:agent 只产**可审计 declarative plan** —— 六要素:`源 / 时间窗或目标范围 /
    端点集合 / 参数 schema / 最大请求预算 / 停止条件 / 落盘位置`。agent **不持 key、不发请求**。
  - **② 执行基座层(隔离 broker/runner)**:operator 授权后,**独占 operator 登录态**(独占
    `userDataDir`/`storageState` · agent 无文件读权 · 日志默认脱敏),**按端点/参数白名单**抓取列表或 detail,
    把内容 + 分页 checkpoint(`cursor`/页边界/重试来源)落盘。**broker 必须 capability-scoped,绝非通用 HTTP
    代理 —— 不盲转发 agent 给的任意 URL**(只认预授权那组白名单端点)。
  - **③ 侦察兵/fallback 层(agent)**:agent 分析已落盘数据诊断列表缺口、把「盲滑」变「定向滑」。列表 API
    够得到时降 operator 手动成本。
  - **半自动被动监听对已可达内容仍保留为默认路径**(不废 v0.1 采集)。
- **两种授权粒度(operator 选)**:
  - **(默认)交互式 bounded capture batch**:每个 batch 一次 operator 确认,确认内容 = 上述六要素。适合
    一次性补历史 / 偶发采集。一次 batch = 一次 operator 介入(可量化,不破 O5b「介入趋近零」)。
  - **(可选)预授权式全自动**:operator **预授权一次固定** `schedule`(何时跑)+ `budget`(请求/速率上限)+
    `kill-switch`(随时停),之后 broker **在该固定边界内全自动跑,无需逐批确认**。**硬约束**:① 边界由 operator
    写死,**agent 不得动态扩大** schedule/budget/端点白名单;② 全自动无人盯时,**失败必须显式可见**(预警/缺口
    当天可见,对齐 C7「不静默丢」)+ checkpoint 可审计,不静默重试触发风控;③ 仅在该顾问平台已实证可稳定翻页
    后才建议开启(见下 Open notes 列表根因)。
  - 边界原则:**采集范围由谁定 = operator(预授权一次或每批一次);范围内的执行 = 全自动。** 预授权 = operator
    决策前移一次,**非取消** operator 授权主体 —— 若改成「agent 自主决定+扩大采集范围」即破 verdict 核心,须回 forge。

> **Open notes(forge v3 未解 · L4 实装前须处理)**:
> - **列表截断 2025-07-21 根因未实测**:是分页 cursor 未续(翻页能解)还是列表 API 物理不返回 2026(只能
>   detail 入口批量发现)?L4 实装前做一次实测(看响应有无 `has_more`/`next_cursor`、offset 越界返回空 vs 报错)
>   定主路径 vs 条件分支。**若出现第三种情况(登录态轮换/风控验证码)条件分支可能不够 → 回 forge v4。**
> - **broker 认证会话隔离实装手段**(Playwright persistent context 等)= L4 选型,forge 只给候选未定。
> - **请求预算/速率数值** = L4 + operator 调参;本 PRD 只定「plan 须含最大请求预算 + 停止条件」结构要求。

## Scope OUT

### 永久 OUT(任何 phase 都不做)
- ❌ 产生投资建议 / 买卖信号 / 仓位建议 / 收益判断(红线 —— 是 004 的职责)。
- ❌ 二次分发 / 公开 / 转售顾问内容(红线 —— 仅个人留存)。
- ❌ 规避**他人**访问控制 / 复用过期失效 token 模拟未授权请求 / 破解付费墙采集**自己无权访问的内容**(红线 —— 见 §Real-world constraints C5)。
  - ✅ **对比明确**:operator 作为付费订阅用户,用有效登录态抓取自己合法请求返回的图文/回放原文件,属「采集自己有权访问的内容」,**在 C5 内**(forge v1 verdict · 合规由 operator 负责)。
- ❌ 多顾问 / 多平台通用采集器(008 是 004 的单源模块,不是通用工具)。
- ❌ 自动判断顾问观点对错。

#### v0.2 OUT 增补(forge v2 verdict)
- ❌ **原内容(图文全文 / 完整转录 / 视频音频 / 含签名 URL)进入 vault 或任何可能传播的衍生输出目录**(红线 —— vault 只放指针+摘要;原文永久留本地 raw_ref 区;见 C5 渠道中性原则)。
- ❌ **双向同步 / vault 回写库 / Obsidian 替换 SQLite SSOT**(SSOT 不可漂 —— ②单向 exporter 是唯一可接受路线)。
- ❌ **依赖 Dataview JS 等可写文件/联网脚本作为验收必需路径**(查询层只读 —— 验收只认 frontmatter 可被 Bases/普通只读查询消费)。

#### v0.2+ OUT 增补(forge v3 verdict · 受控自动翻页红线)
- ❌ **agent 直接持登录态 / 发请求 / 读 broker 的会话凭据文件**(红线 —— 登录态只在隔离 broker/runner;
  违反「登录态绝不进 agent context」non-overridable 硬约束)。
- ❌ **broker 作通用 HTTP 代理 / 盲转发 agent 给的任意 URL**(红线 —— broker 必须 capability-scoped,只认
  预授权端点白名单;否则等于把 key 控制权交回可被 agent 滥用的代理)。
- ❌ **agent 动态扩大授权(schedule/budget/端点白名单)/ 无请求预算或无停止条件的开放式翻页**(红线 ——
  预授权式全自动的边界由 operator 写死,agent 不得自主扩大;否则破 verdict 核心,须回 forge v4 重审)。

### 当前 phase(v0.1)OUT(本 phase 不做但 v0.2 会做)
- v0.1 不做、v0.2 会做:**盘中预警采集 + 及时通知**(US7)。
- v0.1 不做、v0.2 会做:三形态统一时间线 + 回放已看/未看管理(US8)。
- v0.1 不做、v0.2 会做:完整 004 输出契约(v0.1 仅粗约定)。

## Phase transition learning

v0.1 上线后必须验证的假设(决定 v0.2 的具体内容):

1. **假设**:回放"下载→ASR→LLM 摘要"这条链能在 operator 可接受的省心度下稳定运行,且摘要质量够用
   (关键点准确、可溯源)。— 若摘要质量不达标或维护成本过高,v0.2 要先修回放管线,而非急着加预警。
2. **假设**:v0.1 的采集落点(本机/云/手机微信,见 §关键前置)在真实运行 2 周后被证明"既可达又低维护"。
   — 若落点暴露出"扫码重登频率高到超过 O5b 阈值",v0.2 的首要任务变成解决省心问题,而非加形态。
   (注:token 失效介入成本已由 v1.1 升为显式 O5b outcome,不再只是 phase-transition 假设。)
3. **已知(v1.1 operator 拍板)**:图文/回放共享同一登录态(同一微信小程序同账号),故 token 失效恢复是
   **单一路径**(一次扫码恢复全部)。**待 v0.1 观测**:盘中预警(v0.2 形态)是否也共享此登录态/渠道
   — 若不共享,v0.2 加预警可能引入第 2 条恢复路径,需重评 O5b 阈值是否仍成立。
4. **假设**:operator 最常消费的是回放摘要还是图文(US1 vs US2 哪个更高频)。— 决定 v0.2 资源往哪倾斜。

phase 转换由 operator 显式决定(ship v0.1 → 跑 quality-gate → 收集反馈 → 决定启动 v0.2 build)。

## Success — observable outcomes

### v0.1 outcomes
| # | Outcome | How measured |
|---|---------|--------------|
| O1 | 连续 2 周,顾问**图文资讯零漏**(漏/不确定都显式可见,可按天重建"那天发了什么") | 人工核对 2 周采集记录 vs 实际发布;缺口都有标记 |
| O2 | 回放被转成几分钟可消费的文字+关键点;operator **不看完整视频**即可掌握一场直播要点 | operator 主观确认 + 抽查关键点 vs 视频实际内容 |
| O3 | 每个回放关键点能**溯源**回原始转录 + **视频稳定时间戳**(可跳回视频原位) | 抽查关键点的溯源链接可用、时间戳定位准确、内容对应 |
| O4 | 采集失败/不确定**当天可见**,operator 对"没漏"有信心 | 制造一次采集失败,确认 24h 内可见缺口 |
| O5 | 004 能稳定拿到边界清楚的顾问内容轻量包,且**不误认 008 在给建议** | 004 侧读入测试;输出包无任何"建议"字段 |
| O5b | ⭐ **登录态失效后 operator 介入成本 ≤「失效时扫码一次」**:token 失效→系统当天可见提醒→operator 扫码重登 1 次→其余采集全自动,不静默漏。三形态共享同一登录态,故为**单一恢复路径**(非多路) | 观察窗(2 周)内,每次 token 失效仅需 1 次扫码;统计手动介入次数 = token 失效次数;无因失效导致的静默漏采 |

### v0.2 outcomes (subject to v0.1 learnings)
| # | Outcome | How measured |
|---|---------|--------------|
| O6 | 连续 2 周,**三形态(图文+回放+预警)全部零漏** | 人工核对 2 周三形态采集 vs 实际发布 |
| O7 | 盘中预警到达有**及时通知**(及时性阈值待 v0.1 后量化) | 制造一次预警,确认通知在约定延迟内到达 |
| O8 | (forge v2) exporter 导出后 **vault 无正文字段、git check-ignore 命中 vault 路径** | 抽查 frontmatter 仅白名单字段;`git check-ignore` 命中 vault |
| O9 | (forge v2) **库记录 `source_id` 集合 == vault note 集合**(幂等 + drift 可检,无 silent loss) | 重跑 exporter 对比集合;制造一次漏导确认可检出(对齐 C7) |
| O10 | (forge v2) 可按**日期/形态/标的/已看状态**查询,且**查询不依赖可写文件/联网脚本** | Bases/普通只读查询验证四维;确认无 Dataview JS 依赖 |
| O11 | (forge v3) 自动翻页全程 **agent 无 key / 无直接请求**:broker 独占会话目录 agent 无读权 · 抓取仅命中端点白名单 · checkpoint 可审计无 silent drift · 预授权全自动失败当天可见 | 抽查 agent 进程无凭据访问;broker 日志仅命中白名单端点;制造一次漏页确认可检出(对齐 C7);全自动模式制造一次失败确认 24h 内可见 |

## Real-world constraints

| # | Constraint | Source | Rigidity | Phase scope |
|---|------------|--------|----------|-------------|
| C1 | v0.1 时间窗在 2-3 月内,每周 15-30 小时 | L3R0 Block 1 | Soft | v0.1 |
| C2 | v0.2 时间窗待 v0.1 反馈后定 | operator | Soft | v0.2 |
| C3 | 平台/采集落点(本机 vs 云 vs 手机微信)**未定**,是头号未决,需第 0 阶段探针定 | L3R0 Block 3 + 双模型 R2 | Hard(待定) | both |
| C4 | 永久自用,不商业化 | L3R0 Block 3 | Hard | both |
| C5 | ⭐ **只采 operator 有权访问的内容;可用有效登录态采集原内容**(含须抓包取得的图文/回放原文件)。**自用不传播 —— 原内容不得进入任何会被传播/同步的衍生渠道**(含 git、iCloud/Obsidian Sync 及任何同步通道),**不规避他人访问控制**。合规边界由 operator 负责。详见下方渠道中性原则。 | L3R2 Opus §2/§4 + forge v1 + **v2** verdict | Hard | both |
| C6 | **回放关键点必须溯源原始转录**,LLM 不得发挥成 008 自己的观点 | operator 补充 + 红线 | Hard | both |
| C7 | uncertain capture states 一等公民:失败/不确定显式可见,不静默丢失 | L3R2 GPT §5 | Hard | both |
| C8 | 单源:只一个指定顾问 | L3R1 双方 | Hard | both |
| C9 | 不为结构化牺牲原始留存:任何标签/要点可回到顾问原话 | L3R2 双方 | Hard | both |

> 🔧 **C5 渠道中性原则(forge v2 增补 · 见 stage-forge-008-v2.md)**:本约束**不溯及 v0.1 已 ship 采集落点**
> (其合规性 operator 已负责,不重审);新增约束**只针对 vault 这类衍生导出层**。原内容(图文全文 / 完整转录 /
> 视频音频 / 含签名 URL)永久留在本地 `raw_ref` 原文区,**绝不进 vault**。
> 第一性原因:vault 常挂 iCloud/Obsidian Sync,**git-ignored 只挡 git、挡不住云同步**(SOTA 坐实 iCloud 不读
> `.gitignore`)—— 故 C5 从「绝不入 git」扩为渠道中性的「不进任何会传播/同步的渠道」。

> 🔧 **C5 IN/OUT 边界(forge v3 增补 · 见 stage-forge-008-v3.md)**:C5 渠道中性约束管的是采集**后**的
> **OUT 侧**传播/同步(原文/转录/视频/签名 URL 仍永久 OUT)。**自动翻页属 IN 侧采集手段**(怎么把列表页抓
> 进来),仅限 operator 有权访问内容,且**采集会话凭据不得进入 agent context**(见 Scope IN 受控自动翻页段)。
> **IN 侧采集面扩展不松动 OUT 侧任何约束** —— 二者正交。

## UX principles (tradeoff stances)

- **不漏 > 一切**:覆盖所有形态(终态),每种哪怕先做最浅留存;但 v0.1 已含回放摘要(价值优先排序)。
- **显式缺口 > 假完整**:已收/待确认/未能确认必须分开(C7)。这是"不漏"的真正实现 —— 漏了要知道。
- **原文/原始转录可追溯 > 加工**:回放摘要、图文标签都必须能回到原始证据(C6/C9);避免提取出错丢信息或越界成"建议"。
- **省心 > 功能丰富**:operator 介入次数趋近零是核心目标。v0.1 检索/展示够用即可;**v0.2 起以 Obsidian vault 提供双链/图谱(US8 载体),但作人读衍生层,不增加采集侧维护负担,SQLite 仍是唯一 SSOT**。(🔧 forge v2:原「不做 PKM 式双链/图谱」与 v0.2 Obsidian 双链方向矛盾,已复位)
- **及时 > 实时**(v0.2 预警):及时通知即可,非毫秒级。
- UX 立场随 phase:v0.1 重"把最痛的(图文+回放)采稳采全 + 缺口可见";v0.2 重"补齐预警 + 统一视图"。

## Biggest product risk

**v0.1 直接包含整个项目最难的回放管线**(operator 知情选择"价值优先")。
回放是 1-2 小时大文件 + 微信小程序/手机端 + "下载→ASR→摘要→**稳定时间戳映射**"多环节,任一环节不稳都拖累 v0.1。
双模型 L3R2 一致判全形态路径 "ambitious and brittle"。

> 🔧 **v1.1 风险修订(forge v1)**:原表述含「未验证的采集落点 + 回放合规不可达」两条风险。
> 其中**「回放在合规下不可达」是伪风险,已被 forge v1 证伪删除** —— 回放与图文均靠 operator 有效
> 登录态抓包可达(C5 已重定,合规由 operator 负责)。**残留的是纯工程量风险**:① 1-2h 大文件下载;
> ② ASR 转录质量;③ LLM 摘要关键点准确;④ **关键点→视频稳定时间戳的稳定映射**(operator 决策点 2
> 拍板「必须含稳定时间戳」,此项**抬高了 v0.1 回放管线复杂度** —— 比 forge 双专家建议的「覆盖关键点+可溯源即可」更重,是 v0.1 工程量的敏感项)。
> ⚠ **forge 未审工程可行性**(Y=仅产品价值):回放管线能否在 C1 时间窗(2-3 月)内如期建成,
> 是 L4 才能回答的真风险,本 PRD 无法兜底。

**缓解**:① phase 排序虽价值优先,但仍把预警隔离到 v0.2;② **第 0 阶段探针是硬门**(见下,v1.1 已改判
为「自动化稳定性」而非「合规可达性」),探针不过不投入 v0.1 主开发,避免在不稳的源头上空耗 2-3 个月;
③ 回放**价值风险**已由 operator 确认消除,**合规风险**已由 forge v1 证伪消除,只剩**工程量可行性风险**(待 L4 探针验)。

**phase 间流失风险**:operator 是唯一用户,无传统流失风险;但若 v0.1 回放管线维护太累(或 token 失效频率
高到超 O5b 阈值),operator 可能弃用 —— 故 C7"省心"、O5b 阈值与探针是关键。

## 关键前置 gate(进 v0.1 主开发前 / 第 0 阶段)

双模型 L3R2 收敛:008 真正的未知挡在 L4,有两件"动手前必答"的前置,**本 fork 因 v0.1 含回放而加重**:

> 🔧 **v1.1 gate 判准改向(forge v1)**:原探针判准 = 「源头**合规可达性**(回放能否在不破解前提下下载)」。
> 该判准已被 forge v1 证伪作废 —— 它把「浏览可达」误当「采集可达」,把「有效登录态抓包」误判成「破解」。
> 新判准 = 「**自动化稳定性 / 低维护恢复**」:回放/图文用有效登录态**能否持续稳定采集**,**登录态失效能否
> 低操作恢复(≤ O5b 阈值)**,缺口是否显式可见。**gate 不删,换尺子量。**

1. ⭐ **采集落点 + 自动化稳定性探针**(对应 C3,v1.1 改判):微信小程序里顾问的图文**和直播回放**用
   operator 有效登录态怎么采?本机/云/手机哪个落点能同时证明"**持续可采 + 低维护(登录态失效 ≤ O5b
   扫码一次即恢复)+ 缺口显式可见**"?**尤其回放 1-2h 大文件的下载 + ASR + 稳定时间戳映射能否稳定跑通。**
   这是 v0.1 第 0 件事;不答清,工期全浮。(注:合规性**不**再是探针判准 —— 合规由 operator 负责,C5 已重定。)
2. **观察顾问 1-2 周真实发布节奏**:图文/预警/回放各占多少、漏哪个最痛、回放频率多高、**token 实际失效频率**
   (验证 O5b 阈值现实性)。验证 phase 排序假设。

> 这两件作为 v0.1 的"第 0 阶段(探针)",探针通过再投入主开发。探针若显示**回放管线无法在 O5b 省心阈值内
> 稳定自动化**(注意:不再是「无法合规采集」—— 那条已作废),需回 forge / L3 重评,而非硬做。
> XenoDev 重跑探针时**必须按新判准**(自动化稳定性,非合规可达性)。

## Open questions for L4 / Operator

- **关键项(阻塞 v0.1 build)**:
  - ⭐ 采集落点(本机/云/手机微信)—— 探针(按新「自动化稳定性」判准)后由 operator 拍板。
  - 回放"下载→ASR→LLM 摘要→**稳定时间戳映射**"链的**工程可行性**(在 C1 时间窗内能否如期建成)。
    (合规性已不是 open question —— C5 已重定,合规由 operator 负责。)
- **v1.1 已拍板(原 open question 已解决)**:
  - ✅ operator 维护动作量化 = **O5b:失效时扫码一次**(不再是 ❓)。
  - ✅ 回放摘要最低验收线 = **必须含稳定时间戳**(operator 决策点 2)。
  - ✅ 图文/回放共享登录态 = **是**(单一恢复路径)。
- **v0.2 待定项(允许暂时 ❓)**:
  - 盘中预警是否与图文/回放共享登录态/渠道(决定 v0.2 加预警成本 + 是否引入第 2 条恢复路径,影响 O5b)。
  - v0.2 时间窗 + 是否需要更深检索。

---

## PRD Source

本 PRD 由 `/fork-phased` 命令从 L3 fork 生成。phases 由 operator 在 fork 时交互式声明([v0.1, v0.2])。

- L3 menu: discussion/008/L3/stage-L3-scope-008.md · Candidate B
- L2 unpack: discussion/008/L2/stage-L2-explore-008.md(L2-skip 桥接 doc,见 L2-SKIP-NOTE.md)
- FORK-ORIGIN.md in this directory(含 operator 两条关键补充 + 两处授权偏离说明)

本 PRD 是 L4 的**真相源**。L4 spec-writer 必须按声明的 phases([v0.1, v0.2])产各 phase 分段,
且**不得改动本 PRD 的产品决策** —— 有问题 escalate 给 operator。
