# Forge v5 · 006 · P1 · GPT55xHigh · 独立审阅(no search)

**Timestamp**: 2026-05-31T23:01:08Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了:`forge-config.md`;`moderator-notes.md` 不存在;v4 stage 全文;v3 stage 的 B-3/v0.2-note 触发段;XenoDev handoff 全文;`SHARED-CONTRACT.md` 的 B-1/B-4-IDS/changelog v2.3 段;XenoDev `verdict-evidence-lib.sh`、`validate-verdict-evidence.sh`、`verify-ppv-p2.sh`;XenoDev `codex-review` 的 §3.6.2/§3.6.4;XenoDev `parallel-builder` 的 §3.1 与 §6 publish 段;IDS mirror SHA test;MANIFEST §wave-4;`handback-review.md` Step 4;项目记忆 `project_forge_v5_trigger.md`;v5 `PROTOCOL.md` P1 template。
- 我跳过的:无 X 标的因沙箱不可达而 skip。按 hard constraint,我没有读 `discussion/006/forge/v5/P1-Opus47Max.md`,也没有 web search。
- XenoDev reachability:6 个外部仓标的均可读。关键实证点:`/Users/admin/codes/XenoDev/.claude/skills/codex-review/real-review/` 目录不存在,因此当前没有任何 immutable review 记录文件可核查。
- **K 摘要**:用户核心判准是"可靠的、自动化程度最高",且 operator 非软件背景,所以并发安全要可靠优先,宁可保守用真锁/真绑定,但不能为单 operator 少量机器过度上分布式协调。v5 mission 明确是"多 worktree 并发上线前 · 并发安全加固 + evidence binding 时序闭合",只收敛 6 项并发 backlog。
- **阅读策略**:我按 Y1 先追 producer/consumer 证据链和 TOCTOU;按 Y2 看 SHARED-CONTRACT normative 与实现职责边界;按 Y3 看跨仓 mirror、SHA 守护和多 worktree 写同目录路径。

## 1. 现状摘要(按 Y 视角组织)

### Y1 · 并发安全

producer 侧已经比 v4 初态强很多。`verify-ppv-p2.sh` Step 0 会从 hand-back 绑定的 `review_log_path` 反绑 effective REVIEW_LOG,后续 verdict、rehash、一致性和 freshness 都锚同一 log。共享 lib 里 `resolve_review_log_path` 做 canonicalize + allowlist,只放行 singleton `REVIEW-LOG.md` 或 `real-review/` 下文件;producer full 还跑 sha256 rehash、target/ts/model 一致性和 600s freshness。

consumer 侧仍是 shallow。`validate-verdict-evidence.sh` 反复标注自己只是 syntax-only precheck,只验 7 字段齐、verdict enum、findings_count 整数,不验 path 可达、sha binding 或 REVIEW-LOG 一致性。`handback-review.md` Step 4 也是仅当 hand-back 含 `ids_verdict_evidence:` 时调用这个 shallow wrapper。因此 G1 的真实现状不是"consumer 有验证",而是"consumer 有语法闸 + producer 自证"。

B-3 publish 当前靠 `ln $DRAFT $TGT` 原子上架,EXDEV 时 cp 到同目录 tmp 后再 `ln tmp TGT`,并做 SHA 复验;EEXIST 撞库 hard-fail。这个路径防 corruption,但没有 dir-level flock,也不会自动避开同秒多 worker 同 basename 碰撞。

### Y2 · 架构设计

SHARED-CONTRACT v2.3 已把 B-4-IDS known-gap 写明:line 940-941 的可达/rehash 是 producer-side 校验,IDS consumer 不字面实装,因为 `review_log_path` 是 XenoDev repo-relative。协议层已经承认 consumer 深度小于 producer,但同段仍保留"consumer REJECT"风格的原始 normative 语言,靠 known-gap 注记解释。这是可运行的过渡态,不是闭环设计。

R-Q7 采用"策略 A 两者并存":singleton latest-pointer 可覆盖,immutable `real-review/<scope>-<ts>.md` 不可覆盖,hand-back 可绑任一。设计给了兼容性,也留下两个并发洞:绑 singleton 的包下次 review 后不可复证;绑旧 immutable approve 的包可在 600s 窗内绕过后续 needs-attention。`real-review/` 目录目前不存在,说明 immutable 范式还没有实际沉淀记录。

### Y3 · 工程纪律 + 跨仓一致性

共享 lib 的纪律较好:XenoDev 是 SSOT,IDS mirror 有 MANIFEST §wave-4 两行 SHA provenance,并有 `test-verdict-evidence-mirror-sha.sh` 双向 SHA + allowlist helper gate。wrapper 拒 `--mode=producer`,降低把 shallow 当 full validator 的误用概率。

跨仓一致性仍依赖人工/测试触发,不是自动同步。多 worktree 下如果每个 worktree 携带不同时间点的 bootstrap mirror,当前守护能发现 drift,但不会阻止 operator 在未跑 gate 时继续消费旧件。

## 2. First-take 评分(6 项 backlog 一一对应)

| backlog | 倾向 | 优先级直觉 | 理由 |
|---|---|---|---|
| G1 consumer-binding | refactor | P0 | consumer 现在只做 syntax-only;并发下伪造/stale path/sha 可过 IDS 预检。至少要把"consumer 可验什么"从 known-gap 改成正面模型,并给 IDS 一个可独立验证或明确不可验证的判据。 |
| G2 singleton-audit | refactor | P0 | 策略 A 允许绑 singleton,但多 worker 下 latest-pointer 覆盖是常态;ship hand-back 继续允许 singleton 会让审计不可复证。first-take:ship 流程应强制 immutable,保留 singleton 只作人读 latest。 |
| G3 replay-window | refactor | P0 | producer freshness 的 600s 只证明"不太旧",不证明"仍是当前有效 review"。10:00 approve、10:05 needs-attention、10:06 绑旧 approve 的场景仍成立;并发上线前应堵。 |
| B-3 dir-flock | refactor | P1 | 当前 atomic link + SHA 复验能保完整性,所以不是 corruption P0;但同秒并发 basename 撞库会 hard-fail,会伤害"自动化程度最高"。先压测真实碰撞率,再决定 flock/唯一后缀。 |
| R-Q7 immutable-stress | new | P0 | `real-review/` 目录不存在,现在不是"压测已运行系统",而是"验一个尚未产记录的范式"。并发前至少要有真实 immutable 写入、noclobber 碰撞、bound-log verify 的压力证据。 |
| shared-lib-drift | keep | P1 | SHA dual-verify + MANIFEST wave-4 + allowlist helper gate 是轻量正确方案,适合单 operator 少数机器。first-take 是保留,但把 mirror-sha gate 作为并发启动前 preflight;暂不上自动 sync hook。 |

## 3. 我现在最不确定的 3 件事

1. IDS 是否需要、也是否现实地能做到 full consumer binding。若不把 review artifact 随 hand-back 携带回 IDS,IDS 本地永远缺 XenoDev review log;P2/P3 要判断"producer 自证 + audit trail"是否足够。
2. B-3 的真实碰撞概率。协议上 hard-fail 很干净,但多 worktree 是否会在同一秒产同 `handback_id` 需要实测;没有数据前,我不愿把 flock 判成 P0 ship-blocker。
3. G3 应该用 latest-only、单调 review id、nonce,还是 task-bound review scope。强制 latest 最简单,但可能误杀合法的异步 hand-back;需要下一轮把时序边界说清。
