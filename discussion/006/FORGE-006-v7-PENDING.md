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
- **⇒ pending(未进任何 forge)**:KG-12 · KG-22 · KG-23 · KG-32 · KG-33 · KG-34 · KG-35 · KG-37 · **KG-38**(2026-07-06 T017 新撞)

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

## 下次怎么起

```
/expert-forge 006          # Phase 0 intake 时:
  X = XenoDev dogfood-backlog.md 的 pending 批次(KG-12/22/23/32/33/34/35/37/38)· 本文件是导航
  Y = 工程纪律 + 可靠性(review gate 脆弱性为主)
  Z = 对标 SOTA(CI review gate / fallback 模式)
  W = decision-list + refactor-plan(SKILL/协议层改法 · 落 IDS 三层同步)
  K = "review gate 不能单点依赖 codex;fallback 要制度化不靠临场犹豫"
```
簇 1 证据最硬、最 load-bearing(4 条同根 + 本 session 重现),建议作主攻;簇 2/3/4 顺带清。
