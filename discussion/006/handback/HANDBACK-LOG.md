---
doc_type: handback-decision-log
first_created: 2026-05-11T14:30:00Z
last_updated: 2026-05-11T14:30:00Z
total_decisions: 5
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
