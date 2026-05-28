---
forge_id: 006
forge_version: v3
phase: P1
model: GPT55xHigh
generated: 2026-05-27T12:25:39Z
searches_used: none
---
**Verdict**: CONCERNS

# Forge v3 · 006 · P1 · GPT55xHigh · 独立审阅(no search)

**Timestamp**: 2026-05-27T12:25:39Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read the other reviewer's P1 content. I only saw the filename while listing the v3 directory.
**Reviewer stance**: 审阅人 -- 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

我读了 `forge-config.md`、`PROTOCOL.md`、v2 stage doc、`HANDBACK-LOG.md` batch 2、`SHARED-CONTRACT.md` §6/Changelog、`framework/xenodev-bootstrap-kit/` 非 fixture 头部与入口脚本、XenoDev 三个 skill、hook wrapper、integration tests、handback template/gen/score、event-schema，以及 `scan-credentials.sh`。`moderator-notes.md` 不存在；对方 P1 内容未读；本 phase 未联网、未做 SOTA 对比。

**K 摘要**:K8 把 v3 锁定为“Bootstrap kit v0.2 反向同步、协议修订、lib bug 清班”；K9 明确不重审 v2 主线，即 IDS=治理/PRD，XenoDev=唯一 L4 runtime；K10 偏好“边界先定、批量 SSOT、不越界”；K11 要求 11 项 backlog 一一收敛。我的阅读策略因此不是重评 idea，而是按三类 backlog 查证：哪些已经是 XenoDev 真路径、哪些只是 IDS mirror 缺失、哪些属于协议必须升格。

## 1. 现状摘要(按 Y 视角组织)

### 视角 A · 架构设计

v2 大架构仍成立：IDS 只做 idea→PRD+治理，XenoDev 承担 PRD→code runtime，hand-back 回 IDS 形成学习闭环。v0.1 已 ship 后，真实新增问题集中在“XenoDev 真路径已经长出新边界，而 IDS bootstrap mirror 仍停在较小子树”。当前 mirror 有 Safety Floor、workspace、eval-event-log、validator 核心，但不含 skills、hook wrapper、integration tests、template/gen/score。

SHARED-CONTRACT §6 已 ACTIVE，workspace 4 字段、source_repo_identity、6 约束和 hand-back schema 都清楚；但 batch 2 暴露的新事实尚未全部写入协议：EXDEV cross-device publish、event enum 单复数、IDS dir 排他写、`--ids-verdict-evidence`。

### 视角 B · 工程纪律

XenoDev 真路径纪律比 v0.1 bootstrap 初稿更强：parallel-builder 已把 hand-back draft/validate 放到 merge 前，publish 有 hardlink+EXDEV fallback；codex-review 把 review/adversarial-review 分流并 fail-closed；verify-all 有 0/1/2/3 distinct exit code 和 `--ids-verdict-confirmed`。这说明 backlog 多数不是“设计空缺”，而是 SSOT 同步滞后。

同时，lib bug 说明自动化仍会被小接口漂移拖住。`gen-handback.sh` 已适配 section1/2/3、tags array、template SSOT，但 `--out` 默认前缀和 FU-producer-1 case F stale 仍是实际测试/调用摩擦；`scan-credentials.sh` 有 0/1/2 退码意图，但 backlog 指向 exit code 与 14 false positive 治理，说明 Safety Floor 件 1 的可用性还不够稳。

### 视角 C · Y5 重做代价 / 沉没成本 / 知识保留

最省成本路径不是重做 XenoDev，也不是继续手工 cp 单文件，而是按 K10 先扩 mirror 边界，再批量同步。ENTRY 7/9/13 的 5 文件 cp 已证明“小范围锁边界+SHA 验证”可行；v3 要处理的是边界升级后的第一次完整 rebuild。沉没成本应保留为 provenance 和真路径教训，避免把 XenoDev 运行时细节散落成 IDS 里的半复制品。

## 2. First-take 评分(11 项 backlog 一一对一)

| # | backlog | 倾向 | priority | 理由 |
|---|---|---|---|---|
| 1 | mirror rebuild: `skills/{parallel-builder,spec-writer,codex-review}` | N | P0 | mirror 缺 skills,真路径合同在 XenoDev |
| 2 | mirror rebuild: `hooks/wrappers/` | N | P1 | wrapper 接 writer,属 Safety Floor 可观测 |
| 3 | mirror rebuild: `tests/integration/` | N | P0 | T012 gate 未镜像,无法复验 ship-ready |
| 4 | mirror rebuild: `handback-validator/{templates,gen,score}` | N | P0 | template/gen/score 已成 §6.3 实际 schema |
| 5 | 协议:Cross-device publish 段 | R | P0 | EXDEV fallback 已实装,协议未写 |
| 6 | 协议:event-schema enum 单复数统一 | R | P0 | 复/单混用会污染统计查询 |
| 7 | 协议:IDS dir flock/fcntl | N | P1 | 跨 session 写 LOG 需排他 |
| 8 | 协议:`--ids-verdict-evidence` flag | N | P1 | F10 信任缺口需 evidence 化 |
| 9 | lib bug:scan-credentials exit code + 14 false positive | R | P0 | Safety Floor 误报会拖慢全链 |
| 10 | lib bug:gen-handback `--out` 默认前缀 | R | P1 | caller 易写到不可控路径 |
| 11 | lib bug:FU-producer-1 case F stale | R | P0 | main 14/15 fail 是真 regression |

## 3. 我现在最不确定的 3 件事

1. mirror rebuild 应该字节级 cp XenoDev 子树，还是引入 IDS bootstrap-kit 包装层。R2 我希望收敛为“manifest + provenance + SHA 验证”的边界规则。
2. event enum 统一应选复数全量还是语义单数全量。R2 需要兼顾已有 `.eval/events.jsonl` 与未来 reader/filter 语义。
3. case F stale 的根因是 test 过期、score-handback escape 真路径不足，还是 gen/template backward-compat 设计没收口。R2 应先要求复现证据，再决定修 case 或删 case。
