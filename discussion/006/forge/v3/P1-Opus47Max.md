---
phase: P1
side: Opus47Max
forge_id: 006
forge_version: v3
generated: 2026-05-27T12:30:00Z
word_count_approx: 1380
---

# P1 · Opus side · 独立审阅(v3 · v0.2 protocol bump)

## §0 · 标的清单 + 阅读策略 + K 摘要

**K 摘要**(指南针,本 P1 全程对齐):
- K8 binding · v3 mission = "Bootstrap kit v0.2 反向同步 + 协议修订 + lib bug 清班";三类 backlog:(a) mirror rebuild 4 子树,(b) 协议 4 项,(c) lib 3 bug。
- K9 · v2 verdict(IDS=治理 / XenoDev=唯一 L4 / 双向 hand-off)不重审。
- K10 · operator 偏好 = "边界先定、批量 SSOT、不越界"(Cluster A 选项 1 实证)。
- K11 binding · strong-converge · 11 项 backlog 一一对一收敛。

**X 标的实读情况**(13 个文件 / 9 大槽位 · 全部 reachable ✅):
- v2 stage doc(`discussion/006/forge/v2/stage-forge-006-v2.md` · 476 行)— verdict baseline + W3 refactor plan + W4 v0.1 PRD + W5 B1+B2 dev plan 已吸收,**不重审**(K9)。
- HANDBACK-LOG.md(17 ENTRY · batch 2 含 v3 backlog 三类全集)— v3 主线锚。已 verbatim 读完 ENTRY 7-17 + 汇总 batch 2 §5/§6。
- SHARED-CONTRACT.md v2.2 · 已读 §6.1-§6.6 + Changelog 完整(§6.3 hand-back schema = 4 协议级修订的语义位置)。
- framework/xenodev-bootstrap-kit/ 整子树清单 + 5 个本 session 已 cp 文件(writer / validate / check-3/5 / _yaml-helpers)。
- XenoDev SSOT 4 SKILL frontmatter + 核心段(parallel-builder § "强约束" / spec-writer § "0 核心契约" / codex-review § "Load 触发条件" / spec-writer 已含 spec 7 元素 + PPV 第 7)。
- XenoDev hooks/wrappers/dangerous-event-emit.sh(105 行 · 全读 · 含 mktemp fallback + EVAL_LOG_DIR + stderr 摘要 + writer.sh JSON 接口)。
- XenoDev tests/integration · 抽 verify-all-outcomes.sh head 80 + round-trip-006a-pM.sh head 40(O1/O2/O3/O4 + 4 distinct exit code 0/1/2/3 + --ids-verdict-confirmed flag)。
- XenoDev lib/handback-validator/{templates,gen-handback,score-handback} head + event-schema.json 全读。

**阅读策略 priority**(按 Y 视角):
- Y "架构设计"+"工程纪律" 优先看 SHARED-CONTRACT §6 + HANDBACK-LOG batch 2 §5 + XenoDev SKILL frontmatter。
- Y5 "重做代价/沉没成本/知识保留" 锚:K10 边界纪律 + Cluster A 选项 1 实证(本 session 5 文件 cp PASS · 不越 mirror 边界)。

**BLOCK / 跳过 标的**:0 项。

---

## §1 · 现状摘要(按 Y 视角)

### Y1 · 架构设计

**v2 verdict 落地后的实际架构**(2026-05-27 现状):

- IDS 端:协议层 SHARED-CONTRACT v2.2 ACTIVE-but-not-battle-tested,§6 v2.0 + §6.3 v2.2 已落:6 约束 validator + workspace 4 字段 + hand-back schema 3 节 normative + 4 节 RECOMMENDED + §6.4.1 同步/异步段责任分担。framework/xenodev-bootstrap-kit/ mirror 当前**仅含 v0.1 ship 5 子树**(eval-event-log + handback-validator 部分 + safety-floor-1/2/3 + workspace-schema)。
- XenoDev 端:v0.1(006a-pM)2026-05-27 真路径 ship 4 步 1-2 ✓ / 3-4 pending operator 跨仓。lib/handback-validator 已发展出**完整的 producer-side 工具链**(_yaml-helpers + 6 check + validate + gen-handback + score-handback + templates)+ tests/integration 8 个 sh + 4 个 .claude/skills(parallel-builder / spec-writer / codex-review / task-decomposer)+ .claude/hooks/wrappers 加 dangerous-event-emit。
- 架构落差实证(此即 v3 的"问题陈述"):**XenoDev 比 IDS mirror 多 4 个子树**(skills + hooks + tests/integration + handback-validator templates/gen/score)。本 session ENTRY 7+9+13 SSOT cp 5 文件(writer / validate / check-3/5 / _yaml-helpers)只补到 handback-validator/ 子树内,**其余 4 子树仍 stale**。Cluster A 选项 1 锁定 mirror "现有子树"边界,主动接受这 4 子树 backlog。

### Y2 · 工程纪律

- **hand-back v2.2 producer 真路径成熟度高**:11 包 batch 2 全 6 约束 PASS · 0 false positive / false negative · §1/§3/§4 三节固定 body + tags array + section1/2/3 flag 已普及到 producer · gen-handback.sh 有 `--section1/2/3 + --rationale + --out` CLI;§3 表格 + §4 PRD-revision-trigger 自检 + §5 后续 task + §6 file changes + §7 known gotchas 7 节常态化。
- **adversarial codex review precedent 落地**:T007 4 rounds 全 P-finding 真路径 + T012 4 round + 3 distinct exit code(0/1/2/3)+ `--ids-verdict-confirmed` flag · operator break-cap-by-fix 而非 accept-as-backlog(ENTRY 13 A5 codify · ship-blocker precedent)。
- **工程纪律 4 个真问题**(从 HANDBACK-LOG batch 2 §5 抽):
  1. **case F regression**(ENTRY 16 A4):T007 ship 后 template 真路径不含 `{{RATIONALE}}` · FU-producer-1 main 14/15 fail · medium 真 regression · 未修。
  2. **scan-credentials.sh spec/impl gap**(ENTRY 8 A1):spec 注释 "exit 1 if credentials found" 但实测 echo "ERROR" 后 exit 0 · 影响 T012 SHIP GATE 真聚合 Safety Floor 件 1 能力 · medium 真 lib bug · 未修。
  3. **gen-handback.sh `--out` 默认前缀冲突**(ENTRY 8 A4):同名冲突 004-pB T010 + 006a-pM T010 真撞 · low 真路径 UX bug · 未修。
  4. **event-schema enum 单复数不齐**(ENTRY 15/16 A2):`operator_interventions/review_failures`(复)vs `handback_drift`(单)· low 但是真路径 corruption 风险(stats 写错 enum)· 未修。

### Y5 · 重做代价 / 沉没成本 / 知识保留

- **K10 已实证成熟**:Cluster A 选项 1(锁定 mirror 现有子树范围)= 本 session ENTRY 7+9+13 三连 cp · 5 文件 SHA dual-verify PASS · 11 包 validator PASS · 0 跨边界。这是 v3 的"边界先定、批量 SSOT、不越界"原型。
- **未来重做代价主要来自 mirror 边界扩张**:若 v3 一次性 rebuild 4 子树(skills + hooks + tests + templates/gen/score)= 跨仓 cp ~30+ 文件 + bootstrap.sh 升级读新路径 + IDS mirror 子树 README 同步。Y5 axis 实证 = 本 session 决议时 operator 主动选项 1 拒绝全量 rebuild(过载风险已被规避)。
- **知识保留主要来自 HANDBACK-LOG**:17 ENTRY 决议日志 + 批量决议 ENTRY 7-17 集中决议 · 跨仓 audit trail 真路径成立(本 session commit / push 真完成 · 跨 6 个月一致性可追溯)。

---

## §2 · First-take 评分(按 Y 维度)

**评分维度**:K / R / C / N(keep / refactor / cut / new)+ priority(P0/P1/P2)。11 项 backlog 一一对一(对应 K11 strong-converge)。

### Cluster A · mirror rebuild 4 子树(全 R + new mirror file)

| # | backlog 项 | verdict | priority | 理由 |
|---|---|---|---|---|
| A-1 | `skills/parallel-builder/SKILL.md` mirror | **N**(new) | P1 | 553 行 SKILL · 含 ship 流程 §3 真路径 + verdict enum fail-closed · 是 SSOT 不可放任 stale |
| A-2 | `skills/spec-writer/SKILL.md` mirror | **N** | P1 | 257 行 · 含 PPV 第 7 元素 + 4 分支 prd_form 处理 · sort -V portability fix |
| A-3 | `skills/codex-review/SKILL.md` mirror | **N** | P1 | 422 行 · adv vs review 分流决策表 + verdict enum + log 留档 · ship-blocker precedent |
| A-4 | `skills/task-decomposer/SKILL.md` mirror | **N** | P2 | v0.1 已 ship 但 hand-back 未触动 · 一起 cp 减边界 |
| A-5 | `hooks/wrappers/dangerous-event-emit.sh` mirror | **N** | P1 | 105 行 · Safety Floor T001 + eval-event-log wire · 含 mktemp fallback + writer fd 2 |
| A-6 | `tests/integration/` 整子树(8 sh) | **N** | P1 | T012 SHIP GATE 主体 · O1-O4 全验 + 4 distinct exit code + --ids-verdict-confirmed |
| A-7 | `handback-validator/templates/handback.template.md` | **N** | P0 | 42 行 · gen-handback 必依赖 · 不 cp = gen 不能跑 |
| A-8 | `handback-validator/gen-handback.sh` | **N** | P0 | 495 行 · producer 入口 · v0.2 bootstrap 真路径必需 |
| A-9 | `handback-validator/score-handback.sh` | **N** | P1 | 229 行 · operator 真路径打 score + emit operator_interventions event |

### Cluster B · 协议级修订 4 项

| # | backlog 项 | verdict | priority | 理由 |
|---|---|---|---|---|
| B-1 | `SHARED-CONTRACT §6` 加 Cross-device publish 真路径段 | **N** | P2 | 真 EXDEV 场景未实测;FU-producer-2 已 spec'd 跨 device fallback 真路径,加段是 protocol explicit |
| B-2 | `event-schema.json` enum 单复数统一(`handback_drifts` 复) | **R** | P0 | 真路径 corruption 风险(stats 写错 enum)+ 跨 reader/writer 一致性低 · 5 分钟修 |
| B-3 | IDS dir flock/fcntl 锁规则 | **N** | P2 | 真路径 race window 未实测(2 个 XenoDev session 同写)· 当前 fail-closed cleanup 足够 |
| B-4 | `--ids-verdict-evidence` flag | **N** | P1 | F10 cross-repo trust 真路径 short-coming · T012 A3 ship-blocker 候选 · 真路径机器可读 verdict 比 `--ids-verdict-confirmed` 单 bit 强 |

### Cluster C · XenoDev 本仓 lib bug 3 项(R/cut)

| # | backlog 项 | verdict | priority | 理由 |
|---|---|---|---|---|
| C-1 | `scan-credentials.sh` spec/impl gap(exit code) | **R** | P0 | medium · 影响 T012 真聚合 Safety Floor 件 1 · 真 lib bug · 5 分钟修 |
| C-2 | `gen-handback.sh --out` 默认前缀冲突 | **R** | P1 | low · UX bug · 真路径 prd_fork_id-task-id-handback.md 默认 |
| C-3 | FU-producer-1 case F stale(T007 ship 后无 `{{RATIONALE}}`) | **R** | P0 | medium 真 regression(main 14/15 fail)· 必须修 score-handback escape 真路径 OR 删 case F |

---

## §3 · 我现在最不确定的 3 件事

1. **mirror rebuild 4 子树是否真该全部进 v0.2 一锅 ship**(Y5 重做代价 axis)?
   - 论据 pro:K10 已实证 5 文件批量 cp 可行 · 单 commit 跨仓 cp 30+ 文件 + bootstrap.sh 升级 estimated 半天工作量。
   - 论据 con:bootstrap.sh 升级读新路径(skills/ + hooks/ + tests/)= 真实改动 bootstrap.sh 代码 + 测试新 bootstrap 跑通 · 不只是 cp · 风险随 cp 文件数 quadratic 上升。
   - **R2 期望收敛方向**:是否分波? wave 1 = templates + gen + score(P0 · gen 不能跑的硬阻)/ wave 2 = skills 4 SKILL(P1 · ship 流程 SSOT)/ wave 3 = hooks + tests(P1 · v0.2 bootstrap 真路径必需)。

2. **case F regression(C-3)修复策略**:删 case F vs 修 score-handback escape(yaml double-quoted rationale 真路径)?
   - 删 case F = template ship 后无 `{{RATIONALE}}` 字面 = case F 永久 stale = "case F 不再有意义" 的接受;
   - 修 score-handback escape = 真路径找回 yaml double-quoted rationale 真路径 corner case = test 通过但 spec 真路径模糊。
   - **R2 期望收敛**:operator 在 K10 边界纪律下倾向哪种?

3. **B-2 event-schema enum 单复数统一方向**:全复(`handback_drifts`)还是全单(`operator_intervention`)?
   - SOTA 方向:event sourcing 真路径(eg Kafka / EventStore)倾向复数(stream 是事件流);但 schema enum 真路径标 type 单数也常见(eg `UserCreated` event_type)。
   - 真路径影响范围:writer.sh + reader.sh + dangerous-event-emit.sh + score-handback.sh + event-schema.json 共 5 文件 grep 一致。
   - **R2 期望收敛**:GPT-5.5 倾向 + 跨 reader 兼容性(.eval/events.jsonl 已写过 OLD 4 行 schema · 须考虑 migration cost)。

---

**Soft hand-off to Codex P1**:本 P1 已锚 v3 mission(K8)+ K10/K11 binding + 11 项 backlog 一一对一 first-take 评分(N×11 / R×4 / cut×0)+ 3 件 R2 期望收敛事项。**NO web search 本 phase**(per protocol)。等 Codex P1 oneshot 独立 read 同 13 X · 出 first-take 后,Phase 2 双方对比再深入。
