---
phase: P1
side: GPT55xHigh
forge_id: 006
forge_version: v4
generated: 2026-05-31T00:00:00+08:00
searches_used: none
---

# Forge v4 · 006 · P1 · GPT55xHigh · 独立审阅(no search)

## §0 · 读到的标的清单 + 阅读策略 + K 摘要

我读了 inbox 指定 13 个 X 标的,外加 `discussion/006/forge/v4/PROTOCOL.md` P1 template 与 `discussion/006/forge/v4/P1-Opus47Max.md`。跨仓 `/Users/admin/codes/XenoDev/` 标的全部可读,无 `skipped due to access`。阅读顺序是先读 13 X,最后按 inbox 要求对照 Opus P1,所以本轮不是没看对方,而是先独立取证再做差异声明。

K 摘要:本轮受 K8/K9/K10/K11 约束。K8 把 v4 限定为 "post-v0.2-shipped 协议层稳态化 + 治理债清理"(`discussion/006/forge/v4/forge-config.md:154`);K9 明确 v3 11 项 backlog 三波 ship 已完整闭环,不重审大架构(`discussion/006/forge/v4/forge-config.md:163`);K10 要延续"边界先定、批量 SSOT、不越界"(`discussion/006/forge/v4/forge-config.md:166`);K11 要 strong-converge,5 项 backlog 一一给 verdict,残余只作 v0.3-note(`discussion/006/forge/v4/forge-config.md:168`)。本 P1 不联网、不做 SOTA、不写 next-PRD。

## §1 · 现状摘要

### Y1 · 架构设计

v3 baseline 已收敛:0 unresolved,仅 B-3 IDS dir flock 降 v0.2-note(`discussion/006/forge/v3/stage-forge-006-v3.md:9`,`discussion/006/forge/v3/P3R2-GPT55xHigh.md:50`)。v0.2 之后,O1-O6 真路径已补齐:spec.md 定义 O1-O6(`/Users/admin/codes/XenoDev/specs/006a-pM-v0.2/spec.md:109-114`),HANDBACK-LOG ENTRY 29 记 O6 round-trip 达成并留下 R-Q6/R-Q7 followup(`discussion/006/handback/HANDBACK-LOG.md:609-619`)。MANIFEST 也证明三波 mirror 采用 7 字段 audit schema(`framework/xenodev-bootstrap-kit/MANIFEST-v0.2.md:12-16`,`framework/xenodev-bootstrap-kit/MANIFEST-v0.2.md:54-70`)。

真正的新架构债是 `cross_repo_split`:HANDOFF frontmatter 已有 `cross_repo_split: true`、`target_repo_enum: [IDS, XenoDev]`(`discussion/006a-pM-v0.2/L4/HANDOFF.md:29-31`),§7.2-§7.5 已规定 task `target_repo`、spec-writer、task-decomposer、parallel-builder 路由(`discussion/006a-pM-v0.2/L4/HANDOFF.md:124-157`),spec.md 也把 D09 记为显式协议(`/Users/admin/codes/XenoDev/specs/006a-pM-v0.2/spec.md:177`)。但 SHARED-CONTRACT §6 还未把它升为通用 normative,目前仍像一次性 HANDOFF 扩展。

### Y2 · 工程纪律

R-Q6 是对称性缺口。SHARED-CONTRACT 已规定 B-4-IDS 的 `ids_verdict_evidence` 7 字段全必填,任一字段缺或 SHA mismatch 需 consumer REJECT(`framework/SHARED-CONTRACT.md:905-945`),并写明 v0.2-shipped 后 2-field fallback 应删、7-field 强制(`framework/SHARED-CONTRACT.md:949-954`)。XenoDev `verify-ppv-p2.sh` 已做父键绑定、字段完整性、rehash、target_file/ts/codex_model 比对和 freshness(`/Users/admin/codes/XenoDev/scripts/verify-ppv-p2.sh:18-23`,`/Users/admin/codes/XenoDev/scripts/verify-ppv-p2.sh:231-303`)。但 IDS consumer `/handback-review` 仍只调用 6 约束 validator(`.claude/commands/handback-review.md:28-94`),`validate-handback.sh` 自身也只列 check-1/2/3/5/6,consumer mode 目标是 6 约束(`/Users/admin/codes/XenoDev/lib/handback-validator/validate-handback.sh:2-18`,`/Users/admin/codes/XenoDev/lib/handback-validator/validate-handback.sh:113-155`)。

R-Q7 是 evidence binding 的可变路径缺口。当前 REVIEW-LOG 是 singleton,frontmatter 只显示本次 `verdict/findings_count/ts`(`/Users/admin/codes/XenoDev/.claude/skills/codex-review/REVIEW-LOG.md:5-9`),而同文件正文承认 R1/R4 已围绕 7 字段与不可达 path 做过修复(`/Users/admin/codes/XenoDev/.claude/skills/codex-review/REVIEW-LOG.md:16-23`)。若新 review 覆盖 singleton,旧 hand-back 的 `review_log_sha256` 与 `review_log_path` 就可能失效。

### Y6 · 治理债 + forward evolution

contract_version 是硬治理债:SHARED-CONTRACT frontmatter 仍是 `contract_version: 2.2` / `status: v2.2`(`framework/SHARED-CONTRACT.md:3-4`),但 2026-05-29 changelog 已写入 B-1、B-2、B-4-IDS、B-3-note 等 v0.2 条目(`framework/SHARED-CONTRACT.md:1075-1079`)。D-precedent 也已成模式:spec.md `operator_decision_log` 记录 D2-D6,尤其 D6 明确把多轮 needs-attention 接受 ship 并转 R-Q6/R-Q7 followup(`/Users/admin/codes/XenoDev/specs/006a-pM-v0.2/spec.md:18-31`);HANDBACK-LOG batch 3 汇总也把 D4/D6 retroactive approve 和 R-Q6/R-Q7 backlog 列出(`discussion/006/handback/HANDBACK-LOG.md:640-652`)。

## §2 · First-take 评分

**Verdict: CONCERNS**。不是 BLOCK:v0.2 已真路径 ship,O6 已闭环。也不是 CLEAN:consumer-side 7 字段、singleton REVIEW-LOG、contract_version 漂移都已在协议层形成可见债。

| backlog | 决策 | P | target_repo | 理由 / 下一步 |
|---|---:|---:|---|---|
| R-Q6 consumer-side 7 字段 verify | **new** | P0 | IDS + XenoDev mirror | 接受 Opus:必须做。把 `verify-ppv-p2.sh` 的 7 字段 rehash/freshness 逻辑抽成 reusable validator,IDS `/handback-review` 调用;XenoDev SSOT 与 IDS bootstrap-kit mirror 同步。 |
| R-Q7 immutable per-review REVIEW-LOG path | **refactor** | P0 | XenoDev | 接受 Opus:做成 `real-review/<task>-round<N>-REVIEW-LOG.md`;singleton 可保留 latest pointer,但 hand-back 绑定必须指 immutable path。 |
| contract_version bump | **refactor** | P0 | IDS | 接受 Opus 的 `2.3` 倾向,不升 3.0。理由:旧 hand-back 可用 6 约束兼容读取,新 7 字段只 forward 强制。同步 bump `status` 与 changelog。 |
| B-3 IDS dir flock | **keep-as-note** | P2 note | IDS | 接受 Opus:12 包 0 撞库,触发条件未实证;保留 v0.3-note 和升级路径,不进 v4 主线。 |
| D-precedent codify | **new** | P1 | IDS | 接受但收窄:不重审 7 次历史正确性,只 codify "accept-with-followup" 的准入条件、必须绑定 owner/期限/验证门。 |
| 新增:cross_repo_split §7 升 SSOT | **refactor** | P1 | IDS | 接受 Opus新增项。HANDOFF §7 已被 spec/task/build 三层消费,应升 SHARED-CONTRACT §6 normative,避免 idea 007 重抄扩展。 |

Next-dev plan:一波 P0 可先改 contract_version + R-Q6 + R-Q7,估 0.5-1 天;二波 P1 改 D-precedent + cross_repo_split SSOT,估 0.5 天。按 `cross_repo_split target_repo`:R-Q7 在 XenoDev,其余以 IDS 为主,涉及 mirror 时双仓同步。

## §3 · 我现在最不确定的 3 件事

1. R-Q6 是否应抽成 `validate-verdict-evidence.sh`,还是并入 `validate-handback.sh`。我倾向独立脚本,避免 6 约束路径安全逻辑与 REVIEW-LOG 语义校验耦合。
2. R-Q7 的 immutable path 是否要反向更新 SHARED-CONTRACT B-4-IDS 7 字段示例中的 `review_log_path`。我倾向要,否则协议示例继续鼓励 singleton。
3. D-precedent codify 放 SHARED-CONTRACT §6 还是新 §7 治理段。我倾向新 §7,因为它不是 hand-back schema,而是 operator 决议纪律。
