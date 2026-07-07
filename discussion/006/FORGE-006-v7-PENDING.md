# Forge 006 · v7 待跑批次(intake 预填)

> **这是什么**:自 forge v6(2026-07-02 · 跨机器可移植性 verdict,覆盖 KG-26~31)以来,XenoDev dogfood 又攒了
> 一批**框架级** KG,全部标「待 operator review · 攒批回 IDS forge」。本文件是下次 `/expert-forge 006` 的 X 标的
> 预填 + 聚簇分析,让 Phase 0 intake 不用现场从头梳。**权威全文仍是 XenoDev `dogfood-backlog.md`**(forge 直接读它);
> 本文件只做"哪些没进过 forge + 怎么聚簇"的导航。
>
> **创建**:2026-07-06(handback-review T016 顺带盘点时发现 backlog 攒够一批)

## forge 覆盖线(判断 pending)

- **forge v6 已覆盖**:KG-1/2/4/6/13/14/26/27/28/29/30/31(跨机器可移植性 + 早期批)
- **forge v4 已覆盖**:KG-36(forge-lite 漏消费面)
- **⇒ pending(未进任何 forge)**:KG-12 · KG-22 · KG-23 · KG-32 · KG-33 · KG-34 · KG-35 · KG-37 · **KG-38**(2026-07-06 T017 新撞)· **KG-B1**(2026-07-07 001-T001 新撞 · fork-id charset · 见簇 5)

## 聚簇(建议 forge v7 的 X 标的分组)

### 簇 1 · codex-review 作为 review gate 的可靠性(最大簇 · **5 条同根** · 建议主攻)
codex-review companion 在多个维度上脆弱,fallback 机制不制度化:
- **KG-23** · codex `--scope working-tree` 看不到「已 commit 未 merge」的改动 → 每轮 commit 后 review vacuous approve(空 diff)
- **KG-32** · codex-review SKILL 无 fallback:codex 额度用尽/插件挂 → §3 review 强 hook 死锁(干等或违规无 review merge)
- **KG-35** · companion `--wait` 的 verdict/findings 不稳定落 stdout log,需 `status --all` 兜底
- **KG-37** · companion branch-mode 在 sandbox 下跑不了只读 git/rg(bwrap loopback 失败)→ review 环境性失效
- **KG-38**(2026-07-06 T017 新撞)· codex review **后台 job session-stream 掉流/静默挂起**:job 撞 `Reconnecting 2/5、3/5`,
  读完源文件后**静默 7+ 分钟无 verdict**(status 仍 running · pid alive · reasoning stream 死)—— 是 **session-DROP 非额度耗尽**,
  与 KG-32(额度耗尽死锁)是**不同失效模态**(挂起态更隐蔽:不报错、不退出、干等)。T017 靠取消 + fallback 到 code-reviewer subagent 救回。
- **共同根因**:review gate 把 codex 当唯一可靠通道,但它在 scope 语义 / 额度 / 输出落盘 / 沙箱权限 / **会话流稳定性** 五处都会失效。
  verdict 方向:fallback 分流制度化(codex 不可用→red-team/code-reviewer subagent · 标 subagent-fallback 不冒充 codex)
  + review scope/序审查(working-tree vs branch)+ 输出提取加 fallback 链 + **挂起态超时检测**(KG-38:不能只等 exit code,
  reasoning-stream 静默 N 分钟须判为 DROP 触发 fallback,否则无限干等)。**⚠ codex-review SKILL 是 IDS bootstrap-kit
  mirror 件 → 改动落 IDS 三层同步,不在 XenoDev 当场改。**

### 簇 2 · handback tooling papercuts(2 条 · low severity · 顺手清)
- **KG-12** · handback-validator valid fixture/README 默认命令与 producer/consumer mode 分流不一致(consumer 模式要求
  物理路径含 `/discussion/<id>/handback/` + 绝对路径,README 单测说明停在 mode 分流之前)
- **KG-31** · gen-handback template L6/L8 `to_source_repo`/`source_repo` 是 mac 字面量(非 `{{占位符}}`),env 化那波
  漏改 → 产出的包 frontmatter 静默带错 mac 路径且 validator 不查这两字段

### 簇 3 · build mechanics(2 条)
- **KG-33** · parallel-builder §5 `git worktree remove --force` 静默丢 main worktree 的 stash 列表指针(根因存疑 · 需深查)
- **KG-34** · 迁移单测 `executescript` 与生产 `op.execute(text)` 行为不一致:DDL 内 `':字'` bind-param 陷阱单测测不出

### 簇 4 · spec/review status(1 条 · 可并簇 1 或单列)
- **KG-22** · phased spec 增量补 phase 段时,per-phase review status 不被下游 gate 识别(只读 top-level status)

### 簇 5 · fork-id charset 跨仓协议漂移(1 条 · **high · spine cross-repo · 重开 KG-29 族**)
- **KG-B1**(2026-07-07 · 001-radar-pA T001 build 新撞)· hand-back validator 约束6 charset regex **拒 IDS `/plan-start` 铸的「带 idea-slug 中段」fork-id**(如 `001-radar-pA` 的 `radar` 中段)→ **该 fork 全部 hand-back 无法回流**(硬阻断 · 撞面 = 所有带中段 slug 的 fork · 通用)。
  - **与 KG-29 同族但不同触发**:KG-29(forge v6 已覆盖)只放宽 `-p` 后缀多字符(接 `009-pForge`);KG-B1 是**中段 idea-slug**,连 v6 的 v0.3 regex 也不接。→ **重开 fork-id charset 协议**审。
  - **附带**:gen-handback 强读根 `HANDOFF.md` → 多 fork 并行时静默用 stale id(001 差点产成 008-pB)。
  - **✅ 修复方案已备(带安全论证 + 测试向量 + 落地路径)**:`discussion/006/KG-B1-forge-proposal-20260707.md`(XenoDev `specs/001-radar-pA/KG-B1-forge-proposal.md` 的字节级副本 · sha256 一致)。核心:约束6 regex v0.3→v0.4 加 `(-[a-z0-9]+)*` 中段 · **安全零损**(字符集仅 `{0-9a-zA-Z.-}` · `..` 结构不可能 · regex 是三层防御第一层 · realpath containment 兜真 traversal · 同 KG-29 v0.3 安全论证同构)· 8 接受 + 9 拒绝 + 既有 fixture 零回归。
  - verdict 方向:采纳 v0.4 regex(或 forge 决更强命名约束)+ gen-handback `--handoff` flag。**⚠ check-6/gen-handback 是 bootstrap-kit mirror → 改动落 IDS 三层同步,不在 XenoDev 当场改。**

> **注**:KG-24/25 是 008 build 内容层问题(ASR 增量守护 / DeepSeek 坏-JSON 容错),偏 project-specific 非框架级,
> 是否纳入 forge v7 由 operator 定。

## 本 session(T016 handback-review · 2026-07-06)的 fresh evidence

三条 pending KG 在**同一个 T016 周期**内重现,证明是活疼不是陈账 —— forge v7 可引为「反复发生」的硬证据:
- **KG-37 重现**:T016 build 时 codex adversarial-review 撞 sandbox bwrap loopback 失败 → 走 red-team fallback(3 轮
  收敛 approve · red-team 抓到 codex 漏的 F1 幂等 ship-blocker)。
- **KG-31 重现**:T016 hand-back 包(`20260706T102608Z-...`)frontmatter `to_source_repo`/`source_repo` 仍是
  `/Users/admin/codes/ideababy_stroller`(mac),`handback_target` 却对(linux)—— 同包一半字段对一半错,与 KG-31 描述完全吻合。
- **KG-12 重现**:`/handback-review 009` Step 4 validator 传**相对路径**误报「约束 5 id 不一致」,传绝对路径才 PASS。
  这是从 **live 命令侧**(非 README fixture)复现 KG-12,说明命令文档 Step 4 示例也该标"传绝对路径"。

## 第二 session(M2 收尾 handback-review · 2026-07-06 · T016b/T017/M-fork-complete 三包)的 fresh evidence

M2 收尾三包 review 中又撞两条,其中一条是**新 KG**:
- **KG-38 首撞(新)**:T017 build 时 codex review 后台 job session-stream 掉流(`Reconnecting 2/5、3/5`)后**静默 7+ 分钟无 verdict**
  (running/pid-alive 但 reasoning-stream 死),取消后 fallback 到 code-reviewer subagent 救回。**与 KG-32(额度死锁)不同模态**:
  挂起态不报错不退出,更隐蔽。已入本文件簇1 + XenoDev dogfood-backlog(build 侧记 L 见 M-fork-complete §1)。
- **KG-12 又重现(第二次连续)**:本轮 3 包 validator 仍是相对路径全 FAIL 约束5、绝对路径全 PASS —— **两个连续 handback-review
  session 都撞同一坑**,证据强度升级(不是一次性偶发)。命令文档 Step 4 应硬性标"传 `$(realpath ...)`"。
- **KG-31 又重现**:3 包 frontmatter `to_source_repo`/`source_repo` 仍 mac 字面 `/Users/admin/...`,`handback_target` 却对(linux)—— 同 KG-31。

## 第三 session(001-radar-pA build · 2026-07-07 · spec+tasks+T001)的 fresh evidence

001-radar-pA 是新 idea fork(方向评估官 · 与 004/009 无关),走全流程 spec-writer → task-decomposer → parallel-builder T001。撞:
- **KG-B1 首撞(新 · high · spine)**:T001 代码 ship + 全 review approve 后,§4.1 hand-back producer 阶段撞死 —— validator 约束6 拒
  IDS 铸的 `001-radar-pA`(带 idea-slug 中段)。**这个 fork 的任何 hand-back 都发不出**,operator 决先 merge 代码缓回流。**修复方案已备**
  (簇 5 · `KG-B1-forge-proposal-20260707.md`)。同时暴露 gen-handback 强读根 HANDOFF 的多-fork stale-id 坑。
- **KG-37 重现(第二次跨 session)**:T001 codex adversarial-review R2 撞 bwrap loopback → 走 code-reviewer fallback(抓出 codex R1 修的残留
  model_copy 绕过 blocking)。**KG-37 现已跨 3 个 session 重现**(T016 / 本次),证据强度再升。
- **KG-38 对照(未撞但相关)**:本 session 早先 009-T017 + 001-spec review 撞 KG-38 挂起;但 T001 的 codex R1 **干净跑通**(抓 2 真 high)——
  说明 KG-37/KG-38 两 env 失效**都间歇**(同一 session 内 codex 有时干净跑、有时 bwrap、有时挂起),不是硬失效。fallback 制度化更显必要。
- **正面数据点(codex 价值)**:T001 codex R1 干净跑时抓的 2 条 high(高置信零证据判断绕 OUT-8 / 接口丢 graph)都是真地基缺陷 ——
  证 codex adversarial 对 spine/接口 task 有真价值,fallback 是过桥不是替代(能跑就跑 codex)。

## 下次怎么起

```
/expert-forge 006          # Phase 0 intake 时:
  X = XenoDev dogfood-backlog.md 的 pending 批次(KG-12/22/23/32/33/34/35/37/38 + KG-B1)· 本文件是导航
  Y = 工程纪律 + 可靠性(review gate 脆弱性为主 · fork-id 协议为次)
  Z = 对标 SOTA(CI review gate / fallback 模式 · path-safety id 白名单)
  W = decision-list + refactor-plan(SKILL/协议层改法 · 落 IDS 三层同步)
  K = "review gate 不能单点依赖 codex;fallback 要制度化不靠临场犹豫" + "fork-id 协议两仓要对齐(铸造 vs 校验)"
```
簇 1 证据最硬、最 load-bearing(5 条同根 + 跨 3 session 重现),建议作主攻;**簇 5(KG-B1)虽 1 条但 high + spine + 方案已备**,建议一并收(阻断实际 build);簇 2/3/4 顺带清。
