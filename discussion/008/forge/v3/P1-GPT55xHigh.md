# Forge v3 · 008 · P1 · GPT55xHigh · 独立审阅(no search)

**Timestamp**: 2026-06-20T00:00:14Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了:
  - `forge-config.md`:X/Y/Z/W/K 与 strong-converge 前提。
  - `_external/XENODEV-dogfood-backlog-autopage-entry.md`:整文件读,本轮主源。
  - `_external/XENODEV-SHARED-CONTRACT-s1-s2.md`:整文件读,重点看 §1/§2 与 snapshot 校正注。
  - `discussion/008/008-pB/PRD.md`:聚焦 v1.2 C5、O5b、采集落点、风险与前置 gate。
  - `discussion/008/forge/v2/stage-forge-008-v2.md`:聚焦 Verdict 与 C5 渠道中性修订。
  - `.claude/skills/forge-protocol/SKILL.md`:读取 P1 template。
- 我跳过的:
  - `moderator-notes.md`:不存在。
  - `P1-Opus47Max.md`:按 parallel independence 硬约束未读。
- **K(用户判准)摘要**:核心是「在不违反凭据隔离(登录态绝不进 agent context)的前提下,自动翻页能力是否/如何落地」。binding 前提:合规由 operator 担责;v0.1/v0.2 已 ship 不重审;agent 不得直接持 key 发请求。
- **阅读策略**:按 Y 拆两层:先判自动翻页的 IN 侧主体与数据流,再判凭据是否可能进入 agent context。v2 C5 只作为 OUT 侧既定边界,不拿来替代本轮采集侧判断。

## 1. 现状摘要(按 Y 视角组织)

### 架构设计 / 数据流边界

实战事实:moduleContentList 只到 2025-07-21(contentId 164966),2026 内容 176375/176384 只有 operator 点开 detail 后被动抓到。现架构是 operator 手动浏览,addon/mitmdump 被动监听落盘;agent 读落盘,不以 operator 身份请求。

X 的三向是:①半自动+侦察兵;②独立 daemon 持登录态自动翻页,agent 只读落盘;③agent 出翻页计划,operator 确认后由持 key 进程执行。三者核心差别是持 key 主体与 agent 角色,不是能否技术上发请求。可把它们理解为同一能力的不同控制面:侦察兵发现缺口,计划层给最小请求集合,持 key 层实际抓取,落盘层供后续只读消费。v2 C5 是 OUT 侧:原内容不进 vault/git/云同步等衍生渠道;本轮是 IN 侧:如何把列表/detail 抓入本地原文区。二者正交。

### 安全 / 凭据边界

SHARED-CONTRACT §2 件1 字面覆盖 production credential 文件和 cloud/KMS 运行时凭据,不字面覆盖「顾问平台采集会话 cookie」。K 把登录态不进 agent context 作为采集域硬约束,这比原文更具体,形成 written-constraint 与实际诉求的落差。现有凭据扫描偏文件模式,不足以证明运行时 cookie 没被 agent 读取;若上自动翻页,保证必须来自进程边界、权限、脱敏日志和 agent 只读落盘接口,并要求可追溯。

## 2. First-take 评分(按候选与协议边界)

| 审阅项 | 倾向 | 理由 |
|---|---|---|
| ① 半自动 + agent 侦察兵 | refactor | 保留为 fallback/诊断层,但仍要 operator 手动翻页,不足以满足 K 的自动翻页诉求。 |
| ② 独立 daemon 持 key 自动翻页 | refactor | 合理的持 key 主体,但直接全自动会把确认、限速、scope、审计后移成隐患。应作为执行基座,不是单独 verdict。 |
| ③ agent 出计划 → operator 确认 → 持 key 进程执行 | new | 我的一阶主向。agent 不持 key、不发请求,只产参数序列/时间窗/预期页数;持 key runner 执行后,agent 只读落盘与脱敏日志。 |
| SHARED-CONTRACT §2 措辞 | refactor | 需显式纳入「采集会话凭据」,否则 written constraint 仍停在 deployment secret。§1 PRD schema 不需动。 |
| C5 / PRD 配套 | refactor | C5 渠道中性 keep;另窄幅补 IN/OUT 分界或采集架构约束。不要把凭据边界塞进 OUT 侧 vault 条款。 |

## 3. 我现在最不确定的 3 件事

1. 持 key runner/daemon 的「agent 不可读 cookie」能否在目标机器上可验证,而不只是流程承诺。
2. `moduleContentList` 分页语义是否稳定:cursor/offset、detail 补抓、重复/缺页与速率风险还未确认。
3. 一键确认的粒度:太粗近似隐藏全自动,太细又回到手动维护,会影响 O5b 是否成立。
