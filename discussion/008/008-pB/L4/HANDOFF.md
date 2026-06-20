---
# §6.2 workspace schema 4 字段
workspace:
  source_repo: /Users/admin/codes/ideababy_stroller
  build_repo: /Users/admin/codes/XenoDev
  working_repo: /Users/admin/codes/ideababy_stroller
  handback_target: /Users/admin/codes/ideababy_stroller/discussion/008/handback/

# §6.5 第 13 项 source_repo_identity 字段(由 IDS forward 产源时填入,XenoDev 验)
source_repo_identity:
  expected_remote_url: git@github.com:ttssp/ideababy_stroller.git
  repo_marker: "# Idea Incubator — Project C"
  git_common_dir_hash: 28d25bf82af4c0e2

# Hand-off metadata
prd_fork_id: 008-pB
discussion_id: 008
prd_form: phased
phases: [v0.1, v0.2, v0.3]
phase_current: v0.3
modules: null
module_forms: null
critical_path_module: null
skip_rationale: null

handed_off_at: 2026-06-20T03:40:00Z
prd_source: /Users/admin/codes/ideababy_stroller/discussion/008/008-pB/PRD.md
prd_version_honored: "1.3"
shared_contract_version_honored: 2.0

# Hand-off 序列(本 fork 第 3 次 hand-off · v0.2 ship→v0.3 受控自动翻页)
handoff_seq: 3
supersedes_handoff_at: 2026-06-16T12:30:46Z
---

# Hand-off · 008-pB → XenoDev (per SHARED-CONTRACT §6 v2.0)

**Handed off at**: 2026-06-20T03:40:00Z(第 3 次 · v0.3 受控自动翻页)
**PRD source**: /Users/admin/codes/ideababy_stroller/discussion/008/008-pB/PRD.md(**v1.3** · forge v3 verdict 驱动)
**Build repo**: /Users/admin/codes/XenoDev
**Workspace**: 见 frontmatter `workspace:` 块(§6.2 4 字段全填)
**Source repo identity**: 见 frontmatter `source_repo_identity:` 块(XenoDev 写 hand-back 前必须按 §6.2.1 约束 3 校验)
**SHARED-CONTRACT version honored**: 2.0

## §0 · ⚠️ 本次 hand-off 的特殊性(v0.2 ship→v0.3 新增能力 · XenoDev spec-writer 必读)

> **这是 008-pB 的第 3 次 hand-off**,触发 = **v0.1+v0.2 已 ship + PRD 改 v1.3(forge v3 verdict)→ v0.3 受控自动翻页新增能力**。
> **不是**初次 hand-off,**不是** v0.1/v0.2 重 build。`phase_current: v0.3`。

**1. v0.1 + v0.2 已 ship,绝不重 build / 绝不改已 frozen 段**:
- v0.1(图文+回放采集 / 存储 / 检索 / 缺口可见 / P2/P3 反作弊 / 004 输出)= T101-T112 全 12 task ship,406 test 绿。
- v0.2(Obsidian vault 单向 exporter + US7 盘中预警 + 完整 004 契约)= 9 task ship(DAG 终点 T222),732 test 绿(见 IDS hand-back `discussion/008/handback/20260617T011156Z-008-pB-20260617T011156Z.md` + XenoDev `specs/008-pB/spec.md` v0.2 段 · `status: frozen`)。
- XenoDev 侧已有 v0.1+v0.2 完整 frozen spec(`specs/008-pB/spec.md`)。本次 spec-writer 应**在既有 spec 之上补 v0.3 段**(扩展,非重写;v0.1/v0.2 段保持 frozen 不动),task-decomposer 只拆**新增的 v0.3 task**。
- ⚠ **frozen 铁律**:v0.1/v0.2 段 immutable from build workers。加 v0.3 须新增 phase 段,**不得**改旧段。⚠ **撞 dogfood KG-22**(spec frontmatter 单一 top-level `status` 对「v0.1/v0.2 frozen + v0.3 review 中」部分 frozen 状态表达不好)—— XenoDev 给 v0.3 标状态时按 KG-22 既有 workaround 处理(top-level 暂降 review,v0.3 过 review 后连同复位 frozen)。

**2. 本次 hand-off 的 build 目标 = 【仅】PRD v1.3 的 v0.3 受控自动翻页**(来自 forge v3 verdict · 见 PRD §"Scope IN — v0.2+" 受控自动翻页块[PRD:116-147] + PRD v1.3 修订块[PRD:43-52]):

- ⭐ **受控自动翻页(补齐历史库 · 分层采集架构)**:采集面从「半自动被动监听」扩到「受控自动翻页」,补齐 addon 被动监听够不到的历史列表页。**实战边界硬证据**:moduleContentList 列表接口止于 **2025-07-21**(contentId 164966),2026 内容(176375/176384)仅逐篇 detail 可达、不在任何列表页。
- ⚠ **这是 v0.1/v0.2 之上的新增 IN 侧采集能力**,不替换、不重做半自动被动监听(后者对已可达内容仍是默认路径)。

**3. ⭐ 受控自动翻页的硬约束(forge v3 verdict · spec-writer 不得放松 · 这是 verdict 核心)**:

- **三层分离架构(凭据隔离地基)**:
  - **① 控制流层(agent)**:agent 只产**可审计 declarative plan**(六要素:源 / 时间窗或目标范围 / 端点集合 / 参数 schema / 最大请求预算 / 停止条件 / 落盘位置)。**agent 不持 key、不发请求**。
  - **② 执行基座层(隔离 broker/runner)**:operator 授权后独占 operator 登录态(独占 `userDataDir`/`storageState` · agent 无文件读权 · 日志默认脱敏),**按端点/参数白名单**抓取,内容 + 分页 checkpoint(cursor/页边界/重试来源)落盘。**broker 必须 capability-scoped,绝非通用 HTTP 代理 —— 不盲转发 agent 给的任意 URL**(只认预授权白名单端点)。
  - **③ 侦察兵/fallback 层(agent)**:agent 分析已落盘数据诊断列表缺口、把盲滑变定向滑。
- **凭据隔离硬约束(non-overridable · IAM 级)**:登录态(cookie/token/storageState/userDataDir)**绝不进 agent context**。任何方案不得让 agent 直接持 key 发请求。⚠ 此约束同步要求 XenoDev `SHARED-CONTRACT.md §2` 新增「采集会话凭据隔离」子条款(协议级 · 措辞草案见 `discussion/008/forge/v3/stage-forge-008-v3.md` §"协议修订草案")。**本协议层改动跨仓在 XenoDev,是本 hand-off 的前置依赖**(见 §0.4)。
- **两种授权粒度**:(默认)交互式 bounded capture batch 每批一次确认(六要素);(可选)预授权式全自动 —— operator 预授权**固定** schedule/budget/kill-switch,broker 边界内全自动跑,**agent 不得动态扩大**,且全自动失败须显式可见(对齐 C7)。
- **3 条新 Scope OUT 红线**(PRD §"Scope OUT v0.2+" [PRD:164-170]):① agent 持 key/发请求/读 broker 会话凭据文件;② broker 作通用 HTTP 代理盲转发;③ agent 动态扩大授权 / 无预算无停止条件的开放式翻页。任一触碰 = 破 verdict 核心,回 forge v4。
- **C5 IN/OUT 边界(v1.3 增补)**:自动翻页属 **IN 侧采集手段**,不松动 OUT 侧渠道中性(原文/转录/视频/签名 URL 仍永久 OUT)。二者正交。
- **验收**:PRD O11(凭据隔离可验收:agent 进程无凭据访问 / broker 日志仅命中白名单端点 / checkpoint 可审计无 silent drift / 全自动失败 24h 内可见)。

**4. 残余决策点 / 前置依赖(forge v3 未定 · XenoDev build 遇到时处理)**:
- ⭐ **前置:协议层 §2 子条款须先落**:[A]① 改 XenoDev SHARED-CONTRACT §2(新增「采集会话凭据隔离」子条款 · 协议级)是本 build 的协议依据。建议 **build 起步前先落 §2**(措辞草案现成),否则 broker 隔离约束无协议层 SSOT。
- ⭐ **前置:列表截断根因须实测**:列表止于 2025-07-21 的根因 —— 分页 cursor 未续(翻页能解)vs 列表 API 物理不返回 2026(只能 detail 入口批量发现)?**L4 实装前做一次实测**(看响应有无 `has_more`/`next_cursor`、offset 越界返回空 vs 报错)定主路径 vs 条件分支。⚠ 若实测出**第三种情况**(登录态轮换 / 风控验证码 / 反爬挑战),现有二分条件分支可能不够 → 回 IDS 起 forge v4,不要硬做。
- **broker 认证会话隔离实装手段**(Playwright persistent context / storageState 等)= L4 选型,forge 只给候选未定。
- **请求预算/速率数值** = L4 + operator 调参;PRD 只定「plan 须含最大请求预算 + 停止条件」结构要求。

## §1 · 给 XenoDev operator 的指令

operator 切到 build_repo 后:

1. `cd /Users/admin/codes/XenoDev`
2. 读本 HANDOFF.md(全文,**尤其 §0 第 3 次 hand-off 说明 + §0.4 两个前置依赖**)+ 引用的 PRD.md(**v1.3**)
3. **先落前置**(强烈建议,见 §0.4):① 把 stage 文档 §"协议修订草案"的「采集会话凭据隔离」子条款加进 `framework/SHARED-CONTRACT.md §2 件1` 之后(协议级);② 做一次列表截断根因实测,定主路径(翻页)vs 条件分支(detail 批量发现)。
4. 在 XenoDev session 触发 XenoDev 自带的 spec-writer(per XenoDev AGENTS.md;**不**调 IDS 的 spec-writer subagent)
5. spec-writer **在既有 `specs/008-pB/spec.md` v0.1+v0.2 frozen 段之上补 v0.3 段**(7 元素 schema · 扩展非重写 · v0.1/v0.2 保持 frozen · 按 KG-22 workaround 处理部分 frozen 状态)
6. task-decomposer 拆**新增 v0.3 task**(不重拆已 ship task);受控自动翻页须含:agent declarative-plan 产出器 task + 隔离 broker/runner task(独占会话目录 · 端点白名单 · checkpoint 落盘)+ O11 凭据隔离验收 task
7. parallel-builder 跑 task,quality gate 在 XenoDev 内部决议
8. 每个 task ship 后 XenoDev 产 hand-back 包(per §6.3 schema)写回 IDS `discussion/008/handback/`

## §2 · PRD-form 透传(XenoDev spec-writer 分派依据)

`prd_form: phased` · `phases: [v0.1, v0.2, v0.3]` · `phase_current: v0.3`(详见 frontmatter)

- 本 PRD 是 **phased** → SLA / risks 按 PRD `**Phases**` 数组分段(v0.1+v0.2 段已 ship + **v0.3 段本次 build**)。
- **v0.1/v0.2 段已 ship 且 frozen,不重 build / 不改旧段**;本次聚焦 **v0.3 段**(受控自动翻页分层架构)。
- 参考其他形态(本 PRD 不适用):simple → 标准 7 文件;composite → spec.md 退化 INDEX + 每 module spec;v1-direct → SLA 顶部加 Skip rationale。

## §3 · §6.2.1 6 约束自检契约(XenoDev producer 写 hand-back 前必走)

per `framework/SHARED-CONTRACT.md` §6.2.1,XenoDev 产 hand-back 包写入 `discussion/008/handback/` 前,必须按 6 约束自检:

1. canonical-path containment(realpath prefix 校验)
2. symlink reject(路径任一段是 symlink 即拒)
3. repo identity check(三模式:remote / no-remote / hash-only,任一 PASS 即满足;本 hand-off 已提供 remote + marker + hash 三者)
4. id consistency check(三处 id 严格一致:discussion_id=008)
5. id 字符集 + filename basename + final-path containment(OWASP path traversal 防御)
6. hard-fail(任一约束失败,producer 不写 / consumer 不读)

任一失败 = `Drop`(不写文件,不创目录,只 stderr)。

## §4 · Open questions for build phase

(IDS PRD 中**关于 build 路径选择**的 OQ 在此承载;XenoDev build 自然遇到时再解决,不污染 XenoDev spec frozen)

**v0.3 阶段新增 OQ(forge v3 残余,见 §0.4):**
- ⭐ **列表截断 2025-07-21 根因** —— 分页未尽 vs API 物理截断,L4 实装前实测定主路径 vs 条件分支。若第三种情况(登录态轮换/风控验证码)→ 回 forge v4。
- ⭐ **broker/runner 认证会话隔离实装手段** —— Playwright persistent context 等,L4 选型,forge 只给候选。
- **请求预算/速率数值** —— L4 + operator 调参;PRD 只定结构要求(plan 含最大请求预算 + 停止条件)。
- **预授权式全自动的 schedule/budget 具体配置** —— operator 开启时定;配 kill-switch + 失败显式可见。

**v0.1/v0.2 阶段历史 OQ(已 ship,留档)**:采集落点已定;回放管线可行性已验;Obsidian exporter C5 边界 / source_ref 长度 = v0.2 build 已处理(见 v0.2 hand-back)。

## §5 · Rollback plan

如果 XenoDev build 失败:
- (a) 回到 IDS 修 PRD,重跑 `/plan-start 008-pB`(产新 hand-off 包,handoff_seq+1)
- (b) 改 XenoDev spec(不改 IDS PRD),用 XenoDev 自己的修订机制
- (c) 起 forge 重新审(`/expert-forge 008` → v4)
- (d) XenoDev 产 hand-back 包(tags: `prd-revision-trigger` / `drift` / `practice-stats`)写回 IDS,operator 在 IDS 跑 `/handback-review 008` 决议
- **特别地(v0.3 受控自动翻页高风险点)**:
  - 若 **列表截断根因实测出第三种情况**(登录态轮换 / 风控验证码 / 反爬挑战)→ 二分条件分支不够,走 (c) 回 forge v4 重评 broker connector,**不要硬做**。
  - 若 build 证明 **分层 broker 在 operator 单人本地场景过重**(over-engineering 信号 —— 单人自用是否真需工业级 broker)→ 走 (d) 产 hand-back,operator 可能回 forge v4 重评是否退到「仅侦察兵 + 维持半自动」。
  - 若 **凭据隔离硬约束在实装中守不住**(agent 间接经手 cookie / broker 退化成通用代理)→ 立即停,走 (c)/(d),**绝不**为跑通而破凭据隔离(= V4 失败模式)。
