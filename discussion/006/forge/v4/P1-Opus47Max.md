---
phase: P1
side: Opus47Max
forge_id: 006
forge_version: v4
generated: 2026-05-29T16:50:00Z
prefill_used: false
word_count_approx: 1380
---

# P1 · Opus side · 独立审阅(v4)

## §0 · X 清单 + 阅读策略 + K 摘要

**X 标的(13 引用 · 12 unique files · 全 reachable ✅)**:

1. `discussion/006/forge/v3/stage-forge-006-v3.md`(v3 verdict baseline · 整文件 611 行)
2. `discussion/006/forge/v3/P3R2-Opus47Max.md`(v3 strong-converge 实证)
3. `discussion/006/forge/v3/P3R2-GPT55xHigh.md`(v3 双侧收敛)
4. `framework/SHARED-CONTRACT.md`(v2.2 现行 · 治理债源头 · Changelog L1073+ 重点读)
5. `discussion/006/handback/HANDBACK-LOG.md`(657 行 · 重点 tail batch 3 ENTRY 18-29 + 汇总 ~280 行)
6. XenoDev `specs/006a-pM-v0.2/spec.md`(operator_decision_log + 28 task DAG + cross_repo_split frontmatter)
7. XenoDev `specs/006a-pM-v0.2/risks.md`(R-D2 + R-Q5/Q6/Q7 + R-Q4 已 resolved)
8-9. XenoDev `scripts/verify-ppv-p1.sh` + `verify-ppv-p2.sh`(producer-side 真路径 PPV 实证 · R-Q6 升 consumer-side 时参考)
10. XenoDev `.claude/skills/codex-review/REVIEW-LOG.md`(singleton frontmatter · R-Q7 改造对象)
11. XenoDev `lib/handback-validator/validate-handback.sh`(6 约束 consumer mode · R-Q6 改造对象)
12. `discussion/006a-pM-v0.2/L4/HANDOFF.md`(§7 cross_repo_split 协议 · v4 是否升 SHARED-CONTRACT §6 normative)
13. `framework/xenodev-bootstrap-kit/MANIFEST-v0.2.md`(3 wave × 7 字段 audit · K10 边界纪律实证)

**阅读策略**(按 Y 视角):
- Y1 架构设计 → spec.md §1-§3 outcome/scope/constraints · HANDOFF §7 + risks.md §4 cross-repo + MANIFEST 7 字段
- Y2 工程纪律 → SHARED-CONTRACT Changelog 段 + REVIEW-LOG frontmatter + validate-handback.sh + HANDBACK-LOG batch 3
- Y6 治理债 + protocol forward-evolution(v4 新)→ SHARED-CONTRACT frontmatter `contract_version: 2.2` vs Changelog v0.2 4 entries 漂移 · spec.md `operator_decision_log` D2-D6 七次 accept-with-followup 集合

**K 摘要**:operator 非软件背景 · 求"可靠 · 自动化最高"· K8(v4 mission)post-v0.2-shipped 协议层稳态化 + 治理债清理 · K9 v3 verdict 不重审(11 项 backlog 三类 3 wave 已真路径实证)· K10 边界先定 · 批量 SSOT · 不越界 · K11 strong-converge + 残余降 v0.3-note 旁注。

**未读 / 跳过说明**:无。13 X 标的全部 read access · 0 BLOCK risk(v3 也跑通过同样的跨仓 path)。

---

## §1 · 现状摘要(按 Y 视角组织)

### Y1 · 架构设计

post-v0.2-shipped 的协议层已具备 3 个真路径成熟点 + 2 个不稳态:

**成熟点**(K10 边界纪律真路径实证):
- **MANIFEST 7 字段 schema** 在 wave-1/2/3 全部 append 完整 · 每行 SHA dual-verify · 这是 K10 "批量 SSOT · 不越界" 的首次大规模(31 行 mirror)实证 · 19 IDS + 9 XenoDev split 干净
- **B-4-IDS 协议**(SHARED-CONTRACT §6 + REVIEW-LOG 8 字段 + hand-back `ids_verdict_evidence` 7 字段 immutable binding)已 TX04 真路径首次 round-trip PASS · O6 关闭判据达成
- **cross_repo_split §7 协议**(HANDOFF v0.2 加 · 6 子节 · IDS=19 XenoDev=9 task 分派) 在 spec.md §5.6 + frontmatter `cross_repo_split: true` 双方一致消费 · spec-writer + parallel-builder + task-decomposer 三层都正确按 §7.3-§7.5 路由

**不稳态**(架构层债):
- **contract_version 漂移**:SHARED-CONTRACT.md 头部 `contract_version: 2.2` / `status: v2.2`(L3-4),但 v0.2 wave 2 commit `6ea00e4` 已合 169 行协议改(B-1 + B-4-IDS + B-3-note)· Changelog v0.2 4 entry 已写但版本号没 bump · semver 纪律破洞 · 任何下游 consumer 跑 `grep contract_version` 拿不到正确版本
- **cross_repo_split §7 的"扩展协议"地位**:HANDOFF §7.6 fallback 段写"若 XenoDev spec-writer 不认得本扩展,退化 default IDS"· 但 v0.2 实际 spec-writer 完整消费了 · 说明协议事实上已被实施 · 但 SHARED-CONTRACT §6 没有 normative 段说明 cross_repo_split · 实际是 HANDOFF.md per-instance 扩展 · 未来 idea 007 走同样路径要重抄一份

### Y2 · 工程纪律

v0.2 真路径暴露的纪律点:

- **R-Q6 consumer-side 升 7 字段 verify** 是真路径 gap:`verify-ppv-p2.sh`(XenoDev 端 producer)已实装完整 7 字段 verify + R-Q5 freshness · 但 IDS 端 consumer 链路 `validate-handback.sh` 仍是 6 约束(check-1 到 check-6) · `handback-review.md` Step 4 也只调 6 约束 · 含 `ids_verdict_evidence` 7 字段的 hand-back 进 IDS 后 · IDS 端无法 verify 这 7 字段的 SHA / freshness / immutability · 验证链单向不对称
- **R-Q7 REVIEW-LOG immutable per-review path**:当前 XenoDev `.claude/skills/codex-review/REVIEW-LOG.md` 是 singleton path · 每次 review 跑完用 `cat >` 覆盖之前内容 · 如果同时存在 async hand-back(还没被 IDS consumer 验)+ 新一轮 codex review 覆盖了 REVIEW-LOG → 老 hand-back 里的 `review_log_sha256` 字段对不上当前文件 SHA · hand-back 7 字段 immutable binding 失效 · 路径形态应升 `real-review/<task>-round<N>-REVIEW-LOG.md`(immutable per-review)
- **D-precedent 7 次 accept-with-followup**:D2(OQ-4 解法 A · operator)/ D3-T203(spec vs 真路径 cp 数 · 接受漂移)/ D3-T208(mirror SHA stale · 接受 update row)/ D4-T205(4 finding 不在 file_domain 内 · transitional bind wave 3/X)/ D6-T301(adversarial-review R7 needs-attention 接受 ship · follow-up wave 3.5)/ D6-T304(越界 fix 4 项)/ D6-T306(SHA 同步 hotfix)· 全部走"accept + 转 transitional/wave/v0.x followup" 模式 · 这是工程现场判断 · 但没 normative 流程 · 全部记 spec.md `operator_decision_log` 局部 · IDS 端没法 audit 历史 precedent · 下次 idea 007 spec-writer 不知道现场 accept 是否合规

### Y6 · 治理债 + protocol forward-evolution

3 项治理债的本质都是 "实装 ship 了 · 协议层 normative 没跟":

1. **contract_version**:Changelog 写了 / frontmatter 没改 → 治理债 P0 · 5 分钟改但必须改 · 拖延会让下次 v0.3 bump 时连续债
2. **cross_repo_split §7**:HANDOFF per-instance 扩展协议事实上已成熟 · 但 SHARED-CONTRACT §6 没 normative · 下一 idea 重抄 → 重复扩展 · 协议碎片化
3. **D-precedent 7 次**:accept-with-followup 模式真路径实证有效(v0.2 ship 关闭) · 但没 normative · 下次同样模式可能被新 spec-writer 拒(不知道 precedent) · 治理债

**B-3 IDS dir flock** 的判定:v0.2 12 包 hand-back round-trip 0 撞库 · 触发条件 "并发实证"未触发 · 这是 v3 v0.2-note 设计成功(等真路径触发再升)· v4 应**继续留 v0.3-note**(不进主线 / 不 cut · 触发条件不变)· 这是经验性证据下的稳态决策

---

## §2 · First-take 评分(5 项 backlog · keep/refactor/cut/new + 理由)

| # | backlog | 类别 | 理由 | P |
|---|---|---|---|---|
| **A** | **R-Q6** validate-handback.sh + handback-review.md 升 7 字段 verify | **new**(consumer-side feature)| O6 round-trip 真路径已通(TX04 producer 端)· consumer 端缺验证 · 验证链单向不对称是真 gap · IDS 端能 verify producer 端写的 7 字段 binding 才完整 | **P0** |
| **B** | **R-Q7** REVIEW-LOG immutable per-review path | **refactor**(REVIEW-LOG schema + writer 改 path 范式)| 7 字段 immutable binding 的 `review_log_sha256` 字段当前依赖 singleton 文件不被覆盖 · 是真路径假设漏洞 · 改 immutable path 后 binding 真路径成立 | **P0** |
| **C** | **contract_version bump**(SHARED-CONTRACT frontmatter)| **refactor**(semver 治理债)| 5 分钟改 · 已有 v0.2 4 行 Changelog 等版本号 · `contract_version: 2.2 → 2.3` + `status: v2.2 → v2.3` + frontmatter `last_updated` bump | **P0** |
| **D** | **B-3 IDS dir flock**(v3 v0.2-note)| **keep**(继续留 v0.3-note · 触发条件不变)| 12 包 round-trip 0 撞库 · 触发条件未实证 · 升主线无需求 · cut 会失去未来 P1 升级路径 · v3 决议成熟 v4 沿用 | **P2 → note** |
| **E** | **D-precedent codify**(7 次 accept-with-followup)| **new**(SHARED-CONTRACT 加 §7 D-precedent normative 流程)| 7 次实证 · 模式真路径成立 · 不 codify 下次 idea spec-writer 不知道 · codify 后下次 needs-attention ship 决议有 normative 参考 | **P1** |

**额外加 1 项** —— 我审计 13 X 标的时发现的 v3 verdict 范围外但 v0.2 ship 暴露的事实:

| **F** | **cross_repo_split §7 升 SHARED-CONTRACT §6 normative** | **refactor**(从 HANDOFF per-instance 扩展升 SSOT normative)| v0.2 真路径完整消费 + 三层(spec-writer / task-decomposer / parallel-builder)都按 §7.3-§7.5 路由 · 协议事实上已成熟 · 不升 SSOT 下次 idea 重抄会碎片化 | **P1** |

合计 6 项 backlog(5 + 1) · 我倾向 v4 verdict 把这 6 项打包 1-2 wave ship · 不是 v3 那种 3 wave 大动作 · 因为单仓改动占 4 项(A/C/D/E/F 全 IDS 仓 · 只 B R-Q7 是 XenoDev 仓改)· cross_repo_split 已稳态(spec.md §5.6 计数表)。

---

## §3 · 我现在最不确定的 3 件事(R2 期望收敛)

### 不确定 1 · contract_version 应该 bump 到 `2.3` 还是 `3.0`

v0.2 改的 169 行加了 B-1 + B-4-IDS + B-3-note 三项 normative + cross_repo_split §7 扩展协议事实落地:

- 若按 "non-BREAKING"(v0.2 producer 0 backfill 要求 · 只 forward apply · 与 v2.2 同档纪律)→ `2.3` · 小版本 bump
- 若按 "B-4-IDS 7 字段 immutable binding 是新 normative consumer expectation"(老 hand-back 没这字段会被新 validator 拒)→ 严格 BREAKING · `3.0`

我**倾向 `2.3`**:B-4-IDS 段在 consumer-side 默认 fallback(老 hand-back 无 `ids_verdict_evidence` 字段则跳过 7 字段 check,只跑 6 约束)· 不会 break 旧 hand-back · 但需要 R-Q6 task 实装 fallback 逻辑。如果 Codex 认为 `3.0` 更严谨我接受。

### 不确定 2 · R-Q7 immutable per-review path 是真需求还是过度工程

R-Q7 的攻击场景需要:async hand-back 已写但未被 IDS validator 验 + 同时 XenoDev session 跑新一轮 codex review 覆盖 REVIEW-LOG · 时序条件较严:

- 真路径风险:v0.2 单 operator workflow 几乎不会发生(operator 一时间一件事)
- 但未来多 worktree 并发 ship 时会真路径触发(plan-rosy-naur 多 worker 模式)
- 改造成本:`real-review/<task>-round<N>-REVIEW-LOG.md` 改 writer 路径 + immutable 写 + 不 cleanup 老文件 → 真路径不复杂

**我倾向做**(P0 不过分)· 但如果 Codex 认为应等真路径并发实证后再做(类比 B-3)我可让步成 P1 或 v0.3-note。

### 不确定 3 · v4 应不应该重新审 v0.2 spec.md operator_decision_log 7 次 D-precedent 是否全部正确

我 §2.E 给 **new**(codify) · 但 codify 前需要先 audit 7 次决议是否全部合规。如果 R2 发现某次 D-precedent 不对(eg D4-T205 4 finding transitional bind 是否 hindsight 看也对),那 codify 就要先纠错。

**我倾向 v4 P3R2 verdict 不重审具体 7 次决议**(K9 binding · v0.2 ship 关闭判据已达成 = 7 次决议在路径层有效) · 只 codify normative 流程(下次同样模式怎么走) · 但 Codex 若认为应该 audit 7 次我可接受。

---

**Soft hand-off to Codex P1**:本 P1 倾向 6 项 backlog 打包 1-2 wave ship · contract_version 2.3 · R-Q7 做 · D-precedent codify(不审历史 7 次)· B-3 继续 note · cross_repo_split §7 升 SSOT。3 不确定欢迎反驳。
