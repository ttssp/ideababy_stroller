---
forge_id: 006
forge_version: v3
phase: P2
side: GPT55xHigh
generated: 2026-05-27T12:52:25Z
searches_used: 0
z_mode: 不对标 · 纯内部审阅
---
**Verdict**: CONCERNS

# Forge v3 · 006 · P2 · GPT55xHigh · 参照系评估(no search)

**Timestamp**: 2026-05-27T12:52:25Z
**Searches run**: 0, mode=不对标 · 纯内部审阅
**Visibility**: 我已读对方 P1。

## 1. SOTA 对标

N/A。Z mode 明确为“不对标 · 纯内部审阅”；本 phase 不跑 web search、不做 SOTA benchmark。v3 目标是 v0.1 ship 后 backlog 收敛，外部参照价值低于内部真路径证据。

## 2. 用户外部材料消化

N/A。K 中无新增外部链接或外部文件；`moderator-notes.md` 不存在。本轮只继承 K8-K11：K8 锁 v3 mission，K9 不重审 v2 主线，K10 要边界纪律，K11 要 11 项 backlog 一一收敛。

## 3. 修正后的视角

### 3.1 读完对方 P1 后的 cross-check

**对齐处**:双方 P1 都把 v2 verdict 视为继承前提，而不是重开架构争论；都把问题压到三类 backlog：mirror rebuild、协议修订、XenoDev lib bug。Opus 的 K 摘要里写“11 项 backlog 一一对一收敛”，与我 P1 的 K11 处理完全一致。双方也都把 `HANDBACK-LOG` batch 2 当主证据，而不是凭空设计 v0.2。

**微差异**:Opus 更强调分波，尤其提出 wave 1=templates/gen/score、wave 2=skills、wave 3=hooks+tests。我 P1 更强调“manifest + provenance + SHA 验证”。这不是冲突，可以合并为：**分波执行 + 每波 manifest + provenance + SHA dual-verify + bootstrap verify**。这样既保留 K10 的边界纪律，也避免一次性 rebuild 变成不可审计大复制。

**我保留的反驳棱角**:Opus 把 B-1 Cross-device publish 段列 P2、B-3 IDS dir flock/fcntl 列 P2。我接受 B-3 可降 v0.2-note，因为双 XenoDev session 同写尚未实证；但我不接受 B-1 降太低。EXDEV fallback 已在 parallel-builder §6.3 形成真路径，如果 mirror 要带 tests/integration 和 producer publish 逻辑，协议不写 cross-device 语义会让 bootstrap-kit 成为“代码会做、契约没说”的 drift 源。我将 B-1 调为 P1，不是 P0。

**0 个推翻假设**:对方 P1 没推翻我 P1 的判断。主要更新是执行形态从“一次性 rebuild”修正为“分波 rebuild”；这是风险控制，不是方向改变。

### 3.2 我现在站住的判断(11 项 backlog)

| # | backlog | P2 判断 | priority | 调整 |
|---|---|---|---|---|
| 1 | `skills/parallel-builder` mirror | N | P1 | 从我 P1 P0 降为 P1；先 gen/score unblock |
| 2 | `skills/spec-writer` mirror | N | P1 | 维持；PPV/portability 是知识保留 |
| 3 | `skills/codex-review` mirror | N | P1 | 维持；review enum/分流需 SSOT |
| 4 | `hooks/wrappers/` mirror | N | P1 | 维持；Safety Floor event wire |
| 5 | `tests/integration/` mirror | N | P1 | 从 P0 降为 P1；随 wave 3 验证 |
| 6 | `templates/gen-handback/score-handback` mirror | N | P0 | 维持；producer 入口硬依赖 |
| 7 | Cross-device publish 协议段 | R | P1 | 从 P0 降为 P1；不接受 P2 |
| 8 | event-schema enum 单复数统一 | R | P0 | 维持；统计语义 corruption 风险 |
| 9 | IDS dir flock/fcntl | N | P2-note | 接受 Opus 降级；尚无并发实证 |
| 10 | `--ids-verdict-evidence` flag | N | P1 | 维持；替代单 bit trust |
| 11 | lib bug 三件:scan exit/FP, `--out`, case F | R | C-1/C-3 P0, C-2 P1 | 维持；case F 和 scan 是真 regression |

我的合并方向：Wave 1 修 P0：template/gen/score mirror + C-1/C-3 + B-2；Wave 2 修 P1：skills/hooks + B-1/B-4 + C-2；Wave 3 修 P1/P2：tests mirror + B-3 note 或实装。每波必须有 manifest、source path、target path、SHA、验证命令。

### 3.3 对 K 的对齐性自检

- K8 v3 mission → ✅ 本 P2 只处理 mirror/protocol/lib 三类 backlog，未重审 idea。
- K9 v2 verdict 不重审 → ✅ IDS/XenoDev 双仓边界保持不动；只处理落地 drift。
- K10 边界先定、批量 SSOT、不越界 → ✅ 分波 + manifest + SHA 比一次性 cp 更贴合；每波先声明边界再同步。
- K11 strong-converge 11 项一一收敛 → ✅ §3.2 已逐项给 verdict/priority；残余仅 B-3 是否 v0.2-note，留 P3R1/R2 收口。
