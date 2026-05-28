# PRD · 006a-pM-v0.2 · "bootstrap-kit v0.2 反向同步 + 协议修订 + lib bug 清班"

**PRD-form**: simple
**Status**: approved (forked from forge v3 stage doc · operator 拍板进 L4)
**Sources**: discussion/006/forge/v3/stage-forge-006-v3.md §W4 "Next-version PRD draft" + HANDBACK-LOG batch 2(ENTRY 7-17)
**Forked-from**: discussion/006/forge/v3/stage-forge-006-v3.md(forge v3 verdict · 2026-05-27 converged · 0 unresolved)
**Parent PRD**: discussion/006a-pM/PRD.md(v0.1 · ship 封箱)

---

## User persona

- 非软件开发背景的 1-人 operator(K verbatim)
- 用 Claude Code 实现可靠自动化开发(K verbatim)
- 已经跑通 v0.1 ship(006a-pM)真路径 4 步 1-2;3-4 跨仓 pending

## Core user stories

- 作为 operator,我希望 IDS bootstrap-kit 字节级镜像 XenoDev SSOT,这样新 idea
  bootstrap 不会缺 skills/hooks/tests/templates
- 作为 operator,我希望 SHARED-CONTRACT §6 显式覆盖 producer 已实装真路径
  (EXDEV / verdict-evidence),避免"代码会做、契约没说"drift
- 作为 operator,我希望 lib bug 3 项(scan exit / `--out` 前缀 / case F regression)
  不阻塞下一个 idea 的真路径 ship

## Scope IN

- **IN-1** 完整 mirror(7 子树 + 4 SKILL + MANIFEST-v0.2.md)— wave 1+2
- **IN-2** 协议升 B-1(EXDEV)+ B-2(enum 全复)+ B-4-IDS(verdict-evidence 语义)
- **IN-3** lib bug 0 残余(C-1 + C-2 + C-3 · XenoDev real path · hand-back 回 IDS)
- **IN-4** bootstrap.sh 升级 + 真路径联调(临时 fixture idea + verify-all SHIP-READY)
- **IN-5** MANIFEST-v0.2.md(3 wave append · 7 字段)+ README.md 同步描述新子树

## Scope OUT(显式 non-goals)

- **OUT-1** 不动 IDS=治理 / XenoDev=唯一 L4 双仓边界(Evidence map "v2 verdict 不重审" 行 · K9 binding)
- **OUT-2** 不实装 B-3 IDS dir flock/fcntl(Evidence map "B-3 v0.2-note" 行 · 并发未实证 · 触发后升 P1)
- **OUT-3** 不在 IDS v3 直接实现 B-4-XenoDev runtime(Evidence map "B-4 拆 IDS+XenoDev" 行 · K9 binding)
- **OUT-4** 不重审 v2 verdict / 不重开 idea 判断(Evidence map "v2 verdict 不重审" 行 · K9)
- **OUT-5** 不引入 IDS bootstrap-kit 包装层(P1-GPT §3 不确定 1 R2 收敛 = 字节级 cp + manifest)

## Success looks like

- wave 3 跑通临时 fixture idea bootstrap → verify-all-outcomes.sh exit 0 SHIP-READY
- MANIFEST-v0.2.md 三波完整 + 每文件 source/target SHA 一致 · operator 可手工 grep 验证
- SHARED-CONTRACT v2.3(或 v2.x)Changelog 显式记 B-1 + B-2 + B-4-IDS + B-3-note
- XenoDev side B-4-XenoDev runtime implementation hand-back 已返 IDS · HANDBACK-LOG 新 ENTRY
- 下一个新 idea(eg 007)bootstrap 后真路径跑通 ship 流程 0 中断

## Real constraints

- **时间**:~1.5 周(IDS ~3 天 + XenoDev B-4-XenoDev ~3 天 + buffer)
- **平台**:macOS Darwin 25.5.0(已知)+ Codex 5.3/5.4 + Claude Opus 4.7
- **跨仓**:IDS(本仓)+ XenoDev(`/Users/admin/codes/XenoDev/`)· hand-back 通道
  v2.2 既有
- **合规**:K10 边界纪律(每 wave 1 commit · 不混波)+ K11 strong-converge

## UX principles

- 边界先定、批量 SSOT、不越界(K10 verbatim)
- wave 2 cp 通过 ≠ ship-ready(R2 硬规则)
- 残余分歧用 v0.2-note 旁注(K11 §"残余分歧 v0.2-note 旁注")

## Open questions(forge 也没解决的 · plan-start 阶段决定)

- **OQ-1**:C-3 case F 根因修复(选 a escape vs 选 b 删 case F)· operator 临门决定 · 不影响 P0 必修
- **OQ-2**:bootstrap.sh 升级是否需要新增 verify-bootstrap.sh smoke test?(W3 模块 A wave 3 未列 · 可在 plan-start 决定)
- **OQ-3**:B-4-XenoDev runtime task 在 XenoDev 仓走 plan-start 还是直接 task ship?(W5 dev plan 已列,但调度由 XenoDev runtime 决定)
