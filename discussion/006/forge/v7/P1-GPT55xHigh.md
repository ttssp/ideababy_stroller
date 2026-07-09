# Forge v7 · 006 · P1 · GPT55xHigh · 独立审阅(no search)

**Timestamp**: 2026-07-07T12:21:03Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了:`forge-config.md`(X/Y/Z/W/K + strong-converge);`moderator-notes.md` 不存在;`FORGE-006-v7-PENDING.md` 整文件;`_x-backlog-snapshot.md` 整文件;`/home/ys/codes/XenoDev/dogfood-backlog.md` 相关段核对(当前分支含 KG-12/22/23、未编号长任务、KG-B1,不含 KG-32~38,与快照分支说明一致);v6 stage 只读 verdict / decision matrix / underweight;`forge-protocol/SKILL.md` 完整读;`AGENTS.md` 完整读。
- 我跳过的:未读 `discussion/006/forge/v7/P1-Opus47Max.md`;未做 web search。
- **K(用户判准)摘要**:K 的第一主攻是“review gate 不能单点依赖 codex,fallback 要制度化不靠临场犹豫,且挂起态要能超时检测触发 fallback”。第二主攻是 KG-B1:`001-radar-pA` 这类带 idea-slug 中段 fork-id 被 XenoDev validator 拒绝,正在阻断 hand-back 反向通道。
- **我的阅读策略**:按 Y=工程纪律先看 review gate、fallback、verdict 落盘、测试/验证闭环;按 Y=架构设计再看单点依赖、跨仓协议、SSOT/mirror 漂移和多 fork 并行假设。

## 1. 现状摘要(按 Y 视角组织)

### 视角 A · 工程纪律

v7 的纪律问题不是“没有 gate”,而是“强 gate 自身不够确定”。簇 1 五条 KG 分别击穿 codex review 门:KG-23 让 committed diff 变空审,KG-32 是额度/插件不可用死锁,KG-35 是 verdict 不稳定落主 stdout,KG-37 是沙箱下 branch-mode 读不到必要命令,KG-38 是 job/session stream 静默挂起。未编号长任务条目同样指向存活检测缺口:手搓 `ps|grep` 误判后会重复启动并互写产物。

材料也显示 codex 仍有价值:T001 的 codex R1 抓到真实 high 缺陷;T016/T017 的 fallback 也没有绕过 review,而是用 red-team/code-reviewer 保住 review 门。其他 KG 是 deterministic feedback 细缝:KG-12 的 validator mode/路径说明不一致,KG-22 的 phased spec status gate 只读 top-level,KG-33 的 worktree remove 与 stash park 有近失丢失,KG-34 的 migration 单测路径与生产路径不等价。

### 视角 B · 架构设计

架构上有两个单点。第一个是 codex-review 被放在 ship review gate 的中心,但它同时承担 diff 收集、沙箱命令、LLM 会话、verdict 输出和状态机职责;任一子系统失败都会把 gate 变成卡死或假绿。第二个是 hand-back 协议的 id 铸造与校验分离:IDS 能铸 `001-radar-pA`,XenoDev check-6 不接;gen-handback 又强读仓根 HANDOFF,多 fork 并行时会静默拿 stale id。

v6 背景说明 KG-26~31 已归入“环境事实不进模板常量”,KG-29 只修 `-p` 后缀,没有覆盖 KG-B1 的中段 slug。因此 v7 与 v6 不重叠:review gate 是运行时可靠性架构问题,KG-B1 是跨仓 fork-id 契约漂移的新形态。

## 2. First-take 评分(按 Y 视角)

| Y 维度 | 倾向 | 理由(引用 §1 现状) |
|---|---|---|
| 工程纪律 | refactor | 保留强 review gate 和 fail-closed 方向,但 scope、fallback、超时、verdict 提取、fixture/consumer 路径、migration 真路径都需要从临场经验升为确定规则。 |
| 架构设计 | refactor | 不 cut codex,因为它有真实发现价值;但不能让 codex 或根 HANDOFF 成为单点,必须把 fallback 分流、状态机、fork-id SSOT 和多 fork 选择边界显式化。 |

## 3. 我现在最不确定的 3 件事

1. fallback 强度应按 task risk、失败模态,还是两者交叉决定?
2. KG-B1 最终应扩 regex 接受 IDS 现有铸造,还是收紧 IDS fork-id 铸造约定?
3. KG-22 是轻量成文约束足够,还是必须让 schema/gate 按 phase 读取状态?
