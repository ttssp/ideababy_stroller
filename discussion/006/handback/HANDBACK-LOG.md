---
doc_type: handback-decision-log
first_created: 2026-05-11T14:30:00Z
last_updated: 2026-05-27T09:08:34Z
total_decisions: 17
note: append-only;每条决议追加一段 ## entry;不删除 / 不修改既有 entry
---

# HANDBACK-LOG · discussion 006

per `framework/SHARED-CONTRACT.md` §6.4,本文件是 operator 在 IDS 端对 XenoDev hand-back 包的决议日志。append-only。

## 2026-05-11T14:30:00Z · 006a-pM-20260510T123126Z

**Reviewed at**: 2026-05-11T14:30:00Z
**Tags**: self-test
**Severity**: low
**Validator (consumer-mode)**: FAIL · §6.2.1 约束 3(repo identity)— `expected_remote_url` 留空但 IDS 真有 origin remote(`git@github.com:ttssp/ideababy_stroller.git`)
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [x] 修 XenoDev spec(本仓内,信息式)— FU-producer-1 跟进:XenoDev producer 多入口(PPV self-test vs parallel-builder ship)需统一 remote 字段填写逻辑
- [x] 无操作(收悉,作为 practice-stats 入库)

**Operator note**: 早期 PPV self-test 草稿包;round 5 codex F1 fix(包 2 起)后 producer 已修但本包未追溯。落 practice-stats:**首跑 producer drift 是真问题,需 XenoDev 端统一 remote 字段填写 contract**。

**Follow-up commits**: pending(XenoDev side FU-producer-1 task)

## 2026-05-11T14:30:00Z · 006a-pM-20260510T123452Z

**Reviewed at**: 2026-05-11T14:30:00Z
**Tags**: self-test
**Severity**: low
**Validator (consumer-mode)**:
- 绝对路径 → ✓ 6 约束全 PASS
- 相对路径 → ✗ §6.2.1 约束 5(path discussion_id 提取失败)— **IDS validator check-5 regex bug**,handback 包本身合规
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] **修 IDS validator** — `framework/xenodev-bootstrap-kit/handback-validator/check-5-id-consistency.sh` line 31 sed regex `.*/discussion/([^/]+)/handback/.*` 要求 `/discussion/` 前有 `/`;相对路径 `discussion/006/handback/...` 不匹配。修 regex 同时接受相对 + 绝对路径

**Operator note**: B2.2 Block F 第一个真 validator false-positive — 评分维度 #4(6 约束 real data 无 false positive / false negative)扣分。修 regex 即可,不影响 §6.2.1 normative semantic。

**Follow-up commits**: pending(IDS 1 commit)

## 2026-05-11T14:30:00Z · 006a-pM-20260511T000000Z

**Reviewed at**: 2026-05-11T14:30:00Z
**Tags**: drift
**Severity**: high
**Validator (consumer-mode)**: FAIL · §6.2.1 约束 3(同包 1)— `expected_remote_url` 留空
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [x] 修 XenoDev spec(本仓内,信息式)— ship-side producer 同 FU-producer-1 范围
- [x] 无操作(收悉)— FU-001 drift 标(hook fork from autodev_pipe)operator ack

**Operator note**: FU-001 修 block-dangerous.sh JSON escape + here-doc bug 是真技术修复 + drift 标 ack(autodev_pipe upstream 若升 24 patterns operator 手动 merge)。**Safety Floor 件 2 设计实证(§7 收获)落 practice-stats:Claude Code auto mode classifier 在工具层拦 agent 编辑 hook,即使 settings.json 加 permissions.allow 也拦 — non-overridable 真 non-overridable**。

**Follow-up commits**:
- XenoDev main `5af78f6` fix(safety-floor): FU-001 hook JSON escape + here-doc removal(已 ship)
- pending FU-producer-1(remote 字段统一)

## 2026-05-11T14:30:00Z · 006a-pM-20260511T001000Z

**Reviewed at**: 2026-05-11T14:30:00Z
**Tags**: feature, spec-gap
**Severity**: medium
**Validator (consumer-mode)**: FAIL · §6.2.1 约束 3(同包 1)— `expected_remote_url` 留空
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [x] 修 XenoDev spec(本仓内,信息式)— spec-gap 已开 FU-002(已 ship)+ FU-003(待 ship);producer remote 同 FU-producer-1
- [x] 无操作(收悉)— T001 dangerous-24 fixture ship 落 practice-stats

**Operator note**: T001 round-5 codex F1 实证 — adversarial-review 在 spec scope 内挖出 spec scope 外真问题(dash-dash 变体 bypass)。**D-4(SKILL §3.2 4 轮上限破例 forward-fix)有效**:trend 一致下降 medium → forward-fix;非 scope high → spawn FU-task。这是 §3.2 contract 自身价值的关键实证(落 §7 设计实证 practice-stats)。

**Follow-up commits**:
- XenoDev main `45e54fd` feat(safety-floor): T001 ship dangerous-24 fixture + runner(已 ship)
- pending FU-producer-1

## 2026-05-11T14:30:00Z · 006a-pM-20260511T020000Z

**Reviewed at**: 2026-05-11T14:30:00Z
**Tags**: drift, spec-gap-fix
**Severity**: high
**Validator (consumer-mode)**: FAIL · §6.2.1 约束 3(同包 1)— `expected_remote_url` 留空
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [x] 修 XenoDev spec(本仓内,信息式)— FU-003 hybrid(shlex token + regex fallback)重设计已 spec'd 待 ship;producer remote 同 FU-producer-1
- [x] 无操作(收悉)— **regex 字符串匹配防 shell 注入是猫鼠游戏** 设计认知落 practice-stats

**Operator note**: FU-002 ship + known-limit 段是关键交付(reviewer / IDS 端不会误以为是 0 漏)。三 round codex trend critical+high 不下降 → 确认 regex 路径根本限制 → spawn FU-003 重设计是正确判别。**accept-with-followup 政策成熟**(落 practice-stats)。

**Follow-up commits**:
- XenoDev main `d8c903a` fix(safety-floor): FU-002 hook patterns 加固 + spec-gap 部分修复 + FU-003 跟进(已 ship)
- pending FU-003(5h opus risk_level high)+ FU-producer-1

---

## 2026-05-11T15:00:00Z · 006a-pM-20260511T111609Z

**Reviewed at**: 2026-05-11T15:00:00Z
**Tags**: spec-gap-fix
**Severity**: medium
**Validator (consumer-mode)**: ✓ all 6 constraints PASS — **producer drift 真修复**:`expected_remote_url` 填 `git@github.com:ttssp/ideababy_stroller.git` + repo_marker `# Idea Incubator — Project C` + hash `647b0db7b4d47318` 三字段全实
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [x] 修 XenoDev spec(本仓内,信息式)— FU-producer-2(SKILL §6.3 cross-device fallback)跟进 XenoDev 内 spec'd 待决
- [x] 无操作(收悉)— FU-producer-1 ship 闭环本 batch hand-back producer drift

**Operator note**: per plan v0.2-global v1.2 T1 件 1.1 闭环。FU-producer-1 ship 实证(XenoDev commit `59143df`):
- gen-handback.sh + _yaml-helpers.sh 抽离(producer 多入口 codepath 合一)
- 37/37 test PASS · 4 轮 codex D-4 accept-followup
- 新包 6 约束 validator consumer mode 全 PASS(check-5 regex fix 经 a57972a 修后真数据再验)

producer drift 闭环;后续 XenoDev session 跑任何新 idea 的 hand-back producer 都不会再撞此 friction。

**Follow-up commits**:
- XenoDev main `59143df` feat(handback): FU-producer-1 实装(已 ship)
- pending FU-producer-2 (XenoDev 内 spec'd):SKILL §6.3 cross-device fallback — 等 operator 决是否优先 T3 件 3.1 (004-pB) 之前 ship,本 IDS RETRO 不预决

## 汇总 IDS-side 行动(post-review)

1. **修 IDS validator check-5 regex**(从相对路径校验失败)— 1 commit IDS 端
2. **XenoDev side**(operator 跨仓):
   - FU-producer-1:统一 producer remote 字段填写 contract(PPV self-test + parallel-builder ship 两入口)
   - FU-003(已 spec'd):hook 重设计 hybrid shlex token + regex
3. **未触发**:PRD 修订 / SHARED-CONTRACT 修订(本次 review 未暴露协议层 drift)
4. **practice-stats 落点**(B2.2 Block G 评分输入):
   - 评分 #4 扣分:validator check-5 regex 相对路径 false-positive(1 包)+ producer remote 字段 4 包真 fail
   - 评分 #1 加分:hand-back 包 §1-§7 结构 operator 可读可消费(5 包均含 commit hash + ship 历程 + known limit + 设计认知)
   - 评分 #5 加分:整套 hand-off → ship → hand-back 闭环跑通(5 包真到 IDS;validator 真校;real data 真 fail 真暴露 producer bug)

---

## 2026-05-27T09:08:34Z · 006a-pM-20260524T114651Z · ENTRY 7

**Reviewed at**: 2026-05-27T09:08:34Z
**Tags**: drift
**Severity**: medium
**Related task**: FU-T003-stderr-fix
**Validator (consumer-mode)**: ✓ all 6 constraints PASS(绝对路径调用 · upgraded mirror validator)
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] **SSOT 反向同步**:`framework/xenodev-bootstrap-kit/eval-event-log/writer.sh` 已 cp + SHA dual-verify PASS(本 commit)

**Operator note**: FU-T003-stderr-fix `set +e/set -e` 包裹 capture 区,真消除 `$(...)` + `python3 sys.exit(1)` + `set -e` 时序 silent bug。SSOT 真闭环本 session。A2-A5 backlog(README negative test 范式 / `_validate_event.py` 抽离 / 同 pattern audit / amendment-log)留 v0.2 forge。

**Follow-up commits**: 本 IDS commit(SSOT 反向同步)

## 2026-05-27T09:08:34Z · 006a-pM-20260524T123001Z · ENTRY 8

**Reviewed at**: 2026-05-27T09:08:34Z
**Tags**: feature
**Severity**: low
**Related task**: T010
**Validator (consumer-mode)**: ✓ all 6 constraints PASS
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉)

**Operator note**: T010 ship 落入。§3 A1(scan-credentials exit code)+ A2(14 false positive 治理)+ A3(bootstrap-verify v0.2 真扫)+ A4(gen-handback --out 前缀)全入 v0.2 forge backlog · 本 session 不动 XenoDev 真路径。A5 上游 FU-T003 drift 状态本 ENTRY 7 已答(已 SSOT 同步)。

**Follow-up commits**: pending(v0.2 forge backlog)

## 2026-05-27T09:08:34Z · 006a-pM-20260524T125052Z · ENTRY 9

**Reviewed at**: 2026-05-27T09:08:34Z
**Tags**: drift
**Severity**: low
**Related task**: T004
**Validator (consumer-mode)**: ✓ all 6 constraints PASS
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] **SSOT 反向同步**:`framework/xenodev-bootstrap-kit/handback-validator/validate-handback.sh` + `_yaml-helpers.sh`(新增)已 cp + SHA dual-verify PASS(本 commit)。template 化重构(templates/handback.template.md + gen-handback.sh)backlog · 跨 mirror 子树边界,留 v0.2 一次性 rebuild

**Operator note**: T004 spec V7 `--ship` flag 未实装是设计权衡(gen 只 produce 不 ship,符合 parallel-builder SKILL §6),`spec retroactive amendment 标 OUT-of-scope`(A2)已落 XenoDev 端。A3 同 pattern audit + A4 上游 drift 状态本 batch ENTRY 7 已闭。

**Follow-up commits**: 本 IDS commit(SSOT 反向同步 _yaml-helpers + validate-handback)

## 2026-05-27T09:08:34Z · 006a-pM-20260524T135054Z · ENTRY 10

**Reviewed at**: 2026-05-27T09:08:34Z
**Tags**: spec-gap-fix
**Severity**: low
**Related task**: T005
**Validator (consumer-mode)**: ✓ all 6 constraints PASS
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉)

**Operator note**: spec-writer SKILL `sort -V → gsort → python3` portability + verdict 严判 fix 落 XenoDev `.claude/skills/spec-writer/`。**IDS mirror 当前不含 `.claude/skills/` 子树**(原 bootstrap kit 范围只盖 lib/);A2 mirror SSOT 反向同步 留 v0.2 一次性 rebuild(决议 Cluster A 选项 1 锁定 mirror 现有子树范围)。A3 codex-review SKILL §6 anti-pattern #10 + A5 runner UX `--verbose` backlog。

**Follow-up commits**: pending(v0.2 forge backlog · skills mirror rebuild)

## 2026-05-27T09:08:34Z · 006a-pM-20260524T143059Z · ENTRY 11

**Reviewed at**: 2026-05-27T09:08:34Z
**Tags**: drift, spec-gap-fix
**Severity**: medium
**Related task**: FU-producer-2
**Validator (consumer-mode)**: ✓ all 6 constraints PASS
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉)

**Operator note**: parallel-builder SKILL §6.3 cross-device fallback(63 行 ln→cp+sha+ln on EXDEV)真活儿。**IDS mirror 不含 `skills/parallel-builder/` 子树**;反向同步 backlog 同 ENTRY 10。A2 SHARED-CONTRACT §6 加 Cross-device publish 段 = 协议级修订 / Cluster B 选项 1 = 全部不改累积到下次 forge。A3 gen-handback `--tag drift,spec-gap-fix` CSV 拆数组 bug(XenoDev T007 round 1 F4 已 ship 真修)backlog 待 mirror rebuild 时连带同步。A5 SLA 真路径数据收集 backlog。

**Follow-up commits**: pending(v0.2 forge backlog · skills mirror + protocol bump)

## 2026-05-27T09:08:34Z · 006a-pM-20260524T151532Z · ENTRY 12

**Reviewed at**: 2026-05-27T09:08:34Z
**Tags**: feature, drift
**Severity**: low
**Related task**: T006
**Validator (consumer-mode)**: ✓ all 6 constraints PASS
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉)

**Operator note**: hooks/wrappers Safety Floor + eval-event-log wire 真修(round 1-4 mktemp fallback + 全 stderr 回放 + writer fd 2 + default EVAL_LOG_DIR)。**IDS mirror 不含 hooks/wrappers/ 子树**(原 bootstrap kit 范围未盖 hooks);反向同步 backlog · 同 ENTRY 10/11。A3 audit lib/ 同 pattern + A4 gen-handback 多 tag bug + A5 hand-back body 三节固定 block backlog。

**Follow-up commits**: pending(v0.2 forge backlog · hooks mirror)

## 2026-05-27T09:08:34Z · 006a-pM-20260524T155837Z · ENTRY 13

**Reviewed at**: 2026-05-27T09:08:34Z
**Tags**: feature, drift, spec-gap-fix
**Severity**: low
**Related task**: T007
**Validator (consumer-mode)**: ✓ all 6 constraints PASS
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] **SSOT 反向同步部分**:`validate-handback.sh`(本 commit ENTRY 9 cp)含 T007 加固(path traversal `@file` 防 + NFKC denylist + python3 allowlist)。template §1/§2/§3 三节固定 body + tags array + gen `--section1/2/3` flag 落在 `templates/` 子树 + gen-handback.sh · **IDS mirror 不含 templates/ + gen-handback.sh**;backlog 同 ENTRY 9

**Operator note**: T007 是 6 hand-back batch 累 drift 加固集大成。validate-handback.sh 已 SSOT 闭。A2 codex-review SKILL §6 anti-pattern(adversarial 4 rounds 实证)+ A4 FU-producer-2 CSV bug 闭(本 ship 真修)+ A5 codex round 4 CR finding 是 ship-blocker precedent 添加 backlog。

**Follow-up commits**: 本 IDS commit(部分 SSOT · validate-handback.sh 已升)

## 2026-05-27T09:08:34Z · 006a-pM-20260525T005630Z · ENTRY 14

**Reviewed at**: 2026-05-27T09:08:34Z
**Tags**: feature, drift, spec-gap-fix
**Severity**: low
**Related task**: T008
**Validator (consumer-mode)**: ✓ all 6 constraints PASS
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉)

**Operator note**: tests/integration round-trip + fail-closed cleanup + atomic ln publish + SHA 双校验 + trap 恢复 mv 真路径设计。**IDS mirror 不含 tests/integration/ 子树**(原 bootstrap kit 范围未盖 integration tests);反向同步 backlog 同 ENTRY 10。A2 O1 完整 round-trip 后段 = `/handback-review` verdict half = **本 session 真实跑的就是它** · 标 partial complete 入 backlog。A4 IDS dir flock/fcntl + A5 `--handback-target-override` flag backlog · 协议级 Cluster B 累积。

**Follow-up commits**: pending(v0.2 forge backlog · tests/integration mirror + protocol bump)

## 2026-05-27T09:08:34Z · 006a-pM-20260525T012426Z · ENTRY 15

**Reviewed at**: 2026-05-27T09:08:34Z
**Tags**: feature, drift, spec-gap-fix
**Severity**: low
**Related task**: T011
**Validator (consumer-mode)**: ✓ all 6 constraints PASS
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉)

**Operator note**: eval-events-count.sh + test-T011-negative.sh portable 路径解析(EVAL_LOG_DIR + REPO_ROOT + git common dir fallback)真路径。同 ENTRY 14,IDS mirror 不含 tests/integration/;backlog。**A2 event-schema enum 不一致(operator_interventions/review_failures 复 / handback_drift 单)= 协议级 corruption 风险 · Cluster B 选项 1 决议全部不改累积到下次 forge**(Cluster B 选项 1)。A4 OLD schema migration + A5 producer drift event 自动 emit backlog。

**Follow-up commits**: pending(v0.2 forge backlog + 协议层 batch)

## 2026-05-27T09:08:34Z · 006a-pM-20260525T015435Z · ENTRY 16

**Reviewed at**: 2026-05-27T09:08:34Z
**Tags**: feature, drift, spec-gap-fix
**Severity**: low
**Related task**: T009
**Validator (consumer-mode)**: ✓ all 6 constraints PASS
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉)

**Operator note**: score-handback.sh + template 3 字段(operator_score / _at / _rationale: null)+ yaml double-quoted rationale escape + EVAL_LOG_DIR fallback 真路径。IDS mirror 不含 score-handback.sh(在 handback-validator/ 子树但本 session 决议 Cluster A 选项 1 锁定"现有 mirror 文件" · score-handback.sh 是新增 · backlog)。A2 event-schema enum = ENTRY 15 同。**A4 FU-producer-1 case F stale**(T007 ship 后 template 真路径不含 `{{RATIONALE}}` · main 14/15 fail) = 真 regression · 待 IDS forge 决议 score-handback escape 真路径或删 case F · backlog · medium 但本 session 不在 scope。A5 score 工具自动 emit baseline event backlog。

**Follow-up commits**: pending(v0.2 forge backlog · score-handback mirror + FU-producer-1 case F 修)

## 2026-05-27T09:08:34Z · 006a-pM-20260525T030446Z · ENTRY 17

**Reviewed at**: 2026-05-27T09:08:34Z
**Tags**: feature, drift, spec-gap-fix
**Severity**: low
**Related task**: T012
**Validator (consumer-mode)**: ✓ all 6 constraints PASS
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [x] **修 XenoDev spec(信息式 · ship gate confirm)**:T012 §3 A1 真路径 ship 4 步 — 步骤 1 cp 真路径完成(11 包到 IDS,本 batch ENTRY 7-17 决议)· **步骤 2 `/handback-review 006` ≥7 approve 达成**(11/11 包 validator PASS · operator 决议落 LOG · 11 ENTRY 全 [x] 收悉/同步)· 步骤 3 operator 跨仓 `--ids-verdict-confirmed` verify-all 待执行 · 步骤 4 git push 待 operator 单独确认
- [ ] 无操作(收悉)

**Operator note**: **T012 = v0.1 PRD 006a-pM Phase 3 SHIP GATE**。本 session 是 ship 4 步真路径的步骤 2 闭环。A2 SSOT 反向同步 tests/integration verify-all + exit code 合约 + --ids-verdict-confirmed = backlog 同 ENTRY 14。A3 `--ids-verdict-evidence` flag 消除 F10 cross-repo trust short-coming = 协议级 · Cluster B 累积下次 forge。A4 累计 10 个 hand-back 状态 = 本 batch ENTRY 7-16 全闭环。A5 FU-producer-1 case F stale = ENTRY 16 已答。

**Follow-up commits**: 本 IDS commit(批量决议 + SSOT 5 文件 反向同步);XenoDev side 步骤 3 + 4 待 operator 跨仓执行

---

## 汇总 IDS-side 行动 batch 2(post-review · 2026-05-27)

1. **SSOT 反向同步真闭环**(本 commit · 5 文件)
   - `framework/xenodev-bootstrap-kit/eval-event-log/writer.sh`(FU-T003-stderr-fix)
   - `framework/xenodev-bootstrap-kit/handback-validator/validate-handback.sh`(T004 + T007)
   - `framework/xenodev-bootstrap-kit/handback-validator/_yaml-helpers.sh`(T004 抽出 · 新增)
   - `framework/xenodev-bootstrap-kit/handback-validator/check-3-repo-identity.sh`(B2.2 host fail-closed)
   - `framework/xenodev-bootstrap-kit/handback-validator/check-5-id-consistency.sh`(B2.2 Block F 相对路径接受)
   - SHA dual-verify 5/5 PASS;11 包 validator 全 PASS

2. **未触发 PRD 修订**(全 11 包 §4 PRD-revision-trigger 自检 NO)

3. **未触发 SHARED-CONTRACT 修订**(Cluster B 选项 1 决议:4 项协议级建议 — Cross-device publish / enum 单复数统一 / IDS dir flock / `--ids-verdict-evidence` flag — 全部累积到下次 forge v3 重审 §6 一并处理)

4. **XenoDev spec 修订**(T012 §3 A1 ship gate 步骤 2 确认):
   - 步骤 1 ✓(11 包 cp 到 IDS)
   - 步骤 2 ✓(本 session `/handback-review 006` ≥7 approve)
   - 步骤 3 pending(operator 跨仓 `cd XenoDev && bash tests/integration/verify-all-outcomes.sh --ids-verdict-confirmed`)
   - 步骤 4 pending(operator 单独 push 确认 · 跨仓)

5. **backlog 总览**(v0.2 forge 触发条件累积):
   - **mirror rebuild**(skills/parallel-builder · spec-writer · codex-review;hooks/wrappers;tests/integration;handback-validator/templates + gen-handback + score-handback)
   - **本仓 XenoDev lib bug**(scan-credentials exit code;gen-handback `--out` 默认前缀;14 false positive 治理;case F stale)
   - **协议级**(Cross-device publish 真路径段;event-schema enum 统一;IDS dir flock;`--ids-verdict-evidence` flag)
   - **practice-stats 落点**:plan v0.3 G1 多轴 evidence 完整集累积 · plan v0.2-global 件 3.1 阶段 2c 收官

6. **practice-stats 落点**(B2.2 Block G 评分输入 batch 2):
   - 评分 #1 加分:11 包 hand-back §1/§3/§4 三节固定 body + tags array + section1/2/3 flag(T007 实装后 producer 已经按新 schema 出)
   - 评分 #4 加分:11/11 包 validator PASS · 0 false positive · 0 false negative(check-5 regex bug batch 1 后 producer + IDS mirror 真闭)
   - 评分 #5 加分:**T012 ship gate 真路径 ship 4 步**第一次跨仓真路径执行(步骤 1+2 ✓)· hand-back 通道 v2.0 ship gate 真路径设计实证
   - 评分 #2 加分:Cluster A 选项 1(锁定 mirror 现有子树范围)= producer 真路径累积 6 个 drift hand-back 一次性 SSOT 闭(单 ENTRY 7/9/13 三连 cp · 不越 mirror 边界)— Cluster A 决议成熟度真路径成立


## 2026-05-29 · TX04 PPV-P2 round-trip · O6 关闭 · v0.2-shipped 候选

- **hand-back**: `20260529T095412Z-006a-pM-v0.2-20260529T095412Z.md`
- **从**: `/Users/admin/codes/XenoDev` · phase X TX04 PPV-P2 owning
- **tags**: feature, drift, spec-gap
- **severity**: medium
- **ids_verdict_evidence**(7 字段 immutable binding · per SHARED-CONTRACT §6 B-4-IDS):
  - verdict: needs-attention
  - findings_count: 8
  - review_log_path: `.claude/skills/codex-review/REVIEW-LOG.md`
  - review_log_sha256: `a324dec49291febae7b4a226f793420f71df78ef8e5b93c6a55d56d90fad6f61`
  - target_file: working-tree
  - ts: 2026-05-29T09:00:00Z
  - codex_model: gpt-5-4
- **决议**:approve · D6 precedent 接受 ship + R-Q6/R-Q7 followup
- **O6 round-trip 真路径**:✅ 透传链 REVIEW-LOG → hand-back.ids_verdict_evidence 真路径 7 字段 inject → IDS dir 真路径 publish → HANDBACK-LOG ENTRY 真路径
- **v0.2-shipped**:O1+O2+O3+O4+O5+O6 全 PASS · SLA.md §1.3 状态 2 真路径达成 · v0.2-shipped reached
