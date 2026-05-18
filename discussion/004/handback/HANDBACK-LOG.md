---
doc_type: handback-decision-log
first_created: 2026-05-12T03:31:30Z
last_updated: 2026-05-18T07:30:00Z
total_decisions: 14
total_drops: 1
note: append-only;每条决议追加一段 ## entry;不删除 / 不修改既有 entry
---

# HANDBACK-LOG · discussion 004

per `framework/SHARED-CONTRACT.md` §6.4,本文件是 operator 在 IDS 端对 XenoDev hand-back 包的决议日志。append-only。

## 2026-05-12T03:31:30Z · 004-pB-20260512T025510Z

**Reviewed at**: 2026-05-12T03:31:30Z
**Tags**: feature
**Severity**: low
**Validator (consumer-mode)**: ✓ all 6 constraints PASS — FU-producer-1 ship 后第一次跨非 006 idea 真验:`expected_remote_url` / `repo_marker` / `git_common_dir_hash` 三 identity 字段全实
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉,作为 practice-stats 入库)

**Operator note**: plan v0.2-global T3 件 3.1 起跑 — 第一个非 006 真 idea (004-pB) T001 Phase 0 setup ship。FU-producer-1 ship 后真验:跨非 006 idea / phased prd_form / consumer mode 全 PASS。**v0.2 真触发器第一阶段通过**(待 ≥1 vertical-slice task ship 才完成件 3.1 全部 criteria)。FU-hotfix-F1 是 XenoDev 内 gating(T010/T020/T024),IDS 不预决。

**Follow-up commits**: pending(本 IDS commit 后填)

## 2026-05-12T05:41:52Z · 004-pB-20260512T040013Z

**Reviewed at**: 2026-05-12T05:41:52Z
**Tags**: spec-gap-fix
**Severity**: low
**Validator (consumer-mode)**: ✓ all 6 constraints PASS — FU-producer-1 ship 后第二次跨非 006 idea 真验,producer identity 三字段全实
**Related task**: FU-hotfix-F1a (XenoDev squash commit `e555241`)
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [x] 修 XenoDev spec(本仓内,信息式)— A3 跟进:task-decomposer SKILL 加 audit checkpoint(phased build 拆 task 前必须 check"build runtime 当前 src 状态 vs file_domain 假设")
- [x] 无操作(收悉)— A1 (F1a ship approve) + A4 (不开新 PRD · 不撤 spec frozen · 产品 outcome 0 改动)

**Operator note**: F1a ship 接受 · D-baseline-1 (路线 A · 11k LOC 整体 cp 进 XenoDev) 路线确认。包 §3 A2 (RETRO 记录) 延到 plan v0.2 件 3.1 整体 RETRO 一并写;A3 (task-decomposer SKILL audit baseline cp 前置) 入 v0.2 framework feedback queue (同 F1-F5 类型 · 但是 F6 新条目)。包 §7 风险 #1 (.gitignore L53 通配过宽) + #2 (T010 migration 编号 0042 → 0008) + #3 (multi-feature HANDOFF 切换问题 · 超出 FU-producer-2 cross-device 范围) 是 XenoDev 内 follow-up,IDS 不预决。

**framework 维度观察**:
- 包 §3 由模板空白进化为 4 行有内容表格 → hand-back 包质量提升信号(v0.2 RETRO 正面 evidence)
- 包 §4 自带 PRD-revision-trigger 自检段 → XenoDev producer 主动承担部分 IDS 决议负担,F6 候选(入 SHARED-CONTRACT §6.3 schema 推荐字段)
- 包 §7 风险 #3 提 FU-producer-2 范围扩大(multi-feature HANDOFF 切换 ≠ 只 cross-device fallback)→ T4 件 4.0b 触发时需 scope 调整

**Follow-up commits**: pending(本 IDS commit 后填)

## 2026-05-12T07:00:06Z · 004-pB-20260512T063934Z

**Reviewed at**: 2026-05-12T07:00:06Z
**Tags**: feature
**Severity**: low
**Validator (consumer-mode)**: ✓ all 6 constraints PASS — FU-producer-1 ship 后第三次跨非 006 idea 真验,producer identity 三字段全实
**Related task**: FU-hotfix-F1b (XenoDev squash commit `1055aae`)
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [x] 修 XenoDev spec(本仓内,信息式)— A3 (v0.1 product bug 2 个 hotfix:/notes NoteRepository.list_all 未实装 + /reviews/weekly 模板缺 maintenance) · A4 (v0.2 production app factory API 拆 init/background) · A5 (启动 BANNER 文案 cleanup)
- [x] 无操作(收悉)— A1 (F1b ship approve · codex 3 round adversarial approve · F1+F2+F3 silent green finding 真闭环) + A2 (件 3.1 阶段 2b 闭环 doc · 体现在本 LOG entry + commit msg)

**Operator note**: F1b ship 接受 · production app 真接通 47 routes(spec ≥17 · 超 175%)· codex 3 round adversarial review · F1+F2+F3 silent green finding 真闭环 · approve。**plan v0.2-global 件 3.1 阶段 2b routes wire ✅ 闭环 · 阶段 2c T010/T020/T024 三 lane 入度变 0 unblock**。包 §3 5 条建议:A1 接受 · A2 体现在本 LOG entry + commit msg · A3 (v0.1 product bug 2 个 hotfix) 是 XenoDev 内 task scope(IDS 不预决) · A4 (v0.2 production app factory API 拆 init/background) 延 v0.2 件 4.0c 候选(known-issues §10 已 doc) · A5 (BANNER 文案) XenoDev doc 跟进。§7 风险 #5 (multi-feature HANDOFF 切换) 与 F1a 包 §7 #3 一致 · FU-producer-2 scope 已扩(plan v1.5 已记)。

**framework 维度观察**:
- F1b 是**plan v0.2 件 3.1 真正的解锁里程碑** — F1b ship 后 vertical-slice 三 lane (T010/T020/T024) 入度变 0,件 3.1 阶段 2c 可起;件 3.1 全部 criteria 只差 ≥1 真 vertical-slice ship(三 lane 任选 1)
- codex 3 round adversarial review 深度高 — F1+F2+F3 三 finding 全是 silent green 类(test 看似 pass 实际 prod 会爆),非表面问题。这是 opus high-risk vertical-slice task 真正的质量保证示范
- 包 §3 + §4 schema 升级(F6 候选)在 F1b 包持续 — 5 条 A1-A5 actionable 表格 + PRD-revision-trigger 自检段 一致呈现 → 不是 F1a 一次性,而是 producer 端 schema 稳定提升 → 件 2.5 F6 落地时直接照 F1a/F1b 实例作 schema reference
- v0.2 件 4.0c 新候选(若 A4 落):v0.2 production app factory 拆 init/background API · 同 4.0a (FU-003) / 4.0b (FU-producer-2) 一组 v0.3 / v0.2 trigger 队列

**Follow-up commits**: pending(本 IDS commit 后填)

## 2026-05-12T09:33:54Z · 004-pB-20260512T092800Z

**Reviewed at**: 2026-05-12T09:33:54Z
**Tags**: feature
**Severity**: low
**Validator (consumer-mode)**: ✓ all 6 constraints PASS — FU-producer-1 ship 后第四次跨非 006 idea 真验,producer identity 三字段全实
**Related task**: T010 (XenoDev squash commit `db09f00`)
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [x] 修 XenoDev spec(本仓内,信息式)— A2 (specs/004-pB/tasks/T010.md L12/L48/L64 修 3 行:0042→0008 / SQLAlchemy→Pydantic / int→TEXT note_id) + A5 (FU-wire-2 task 跟进 · 替换 wire.py _StubAssembler · v0.2 production app factory 范围)
- [x] 无操作(收悉)— A1 (T010 ship approve · 12 finding 累积闭环 + 159/159 PASS + coverage 91% + ruff clean) + A3 (件 3.1 阶段 2c 完成 doc · 体现在本 LOG entry + commit msg) + A4 (c) (接受当前 review · 不阻塞等 codex usage 恢复 · F1b precedent 一致)

**Operator note**: T010 ship 接受 · Concept domain + 0008 migration + 159/159 测试 + 91% coverage · cross-model adversarial 5+1 round · 12 finding 累积闭环 (11 直 fix + 1 spec-gap-fix A2 memo XenoDev)。**🎉 plan v0.2-global 件 3.1 阶段 2c '≥1 真 vertical-slice ship' criteria ✅ 达成 · 件 3.1 全部 criteria 满足 · 阶段 3 v0.2 RETRO 可起**。A4 决议:选 **(c) 接受当前** — codex CLI usage limit 撞顶非项目质量问题 · 12 finding 累积闭环 + 0 high pending + evidence chain 完整 · F1b precedent 一致 · 不阻塞 4 天等 codex 恢复。A2 路径:memo XenoDev 下次 session 改 specs/004-pB/tasks/T010.md L12/L48/L64 三行 · IDS 不预决跨仓改动。§7 风险 #4 (multi-feature HANDOFF) 与 F1a/F1b 一致 · FU-producer-2 scope 已扩 · 件 4.0b · 新增 §7 风险 #7 gen-handback.sh grep brackets stderr · FU-producer-3 候选(scope 极小,延 T2 或 v0.3)。

**framework 维度观察**:
- T010 是**plan v0.2 件 3.1 完成 criteria 达成里程碑** — setup (T001) + baseline cp (F1a) + routes wire (F1b) + ≥1 vertical-slice (T010) + hand-back round-trip × 4 + 6/6 validator 全 PASS · 件 3.1 100% done · 阶段 3 v0.2 RETRO 可起
- cross-model adversarial review 深度持续高:T001 0 round · F1a 1 round · F1b 3 round · T010 **5+1 round 12 finding 累积闭环** · 真质量随 task 复杂度提升而 review 深度提升 → 这是 adversarial-review 范式真有效的证据(v0.2 RETRO 正面 evidence · F1b precedent + T010 cap-breaking 双案例)
- A2 spec-gap-fix 模式真触发:T010 ship 实装新 contract · spec 文件还显示旧 contract · IDS operator 决议跨仓改 spec 3 行 → 这是 spec L85 self-ack 约定的 "实装时需 +1 确认" 真落地 · 该模式应入 v0.2 RETRO 作为典型 spec known-issue closure pattern
- 包 §3 schema 演化稳定:T001 0 行 → F1a 4 行 → F1b 5 行 → T010 **5 行**(A1-A5)· §4 PRD-revision-trigger 自检段持续呈现 → 件 2.5 F6 落地时直接照 F1a/F1b/T010 三包实例作 schema reference
- v0.2 件 4.0d 新候选(若 §7 风险 #7 落):FU-producer-3 gen-handback.sh grep brackets bug 修复 · scope 极小(< 1h)· 同 4.0a/4.0b/4.0c 一组 v0.2-v0.3 trigger 队列
- 件 4.0a (FU-003) / 4.0b (FU-producer-2) / 4.0c (production app factory API) / 4.0d (FU-producer-3 grep brackets) 已成 v0.2-v0.3 follow-up 真实集合,plan v1.7 可考虑整合命名

**Follow-up commits**: pending(本 IDS commit 后填)

## 2026-05-12T11:25:00Z · 004-pB-20260512T105103Z

**Reviewed at**: 2026-05-12T11:25:00Z
**Tags**: feature
**Severity**: medium
**Validator (consumer-mode)**: ✓ all 6 constraints PASS — A 通道真并行 ship 第一包(W1 bug1 闭环)· FU-producer-1 ship 后第五次跨非 006 idea 真验
**Related task**: FU-notes-fix (XenoDev squash commit `7eb8626`)
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉,作为 practice-stats 入库)

**Operator note**: W1 FU-notes-fix ship 接受 · v0.1 product bug 1 hotfix(NoteRepository 5 method 补齐 + 10 unit + 170/170 PASS + codex round 1 approve 0 finding) · §4 自检不触 PRD-revision-trigger(实装 5 method 是 v0.1 NoteRepository 设计 intent 内 · 跟 T010 A2 spec-gap-fix 同性质)· A1 spec doc 同步(architecture.md §2.1 加 5 method 签名)延 XenoDev session 自决(IDS 不预决跨仓 spec 改动)· A2-A4 backlog 入 polish queue(non-blocking codex finding · v0.2 之外性质) · A5 release note tracking。**🎉 plan v0.2-global B + A 真并行模式真有效**:operator 切 XenoDev 自跑 W1+W2 两 worktree 并起 · IDS 端我同步 ship B 件 2.4(parallel-builder guide) · 三 ship 真并行无冲突 · A 通道写回 IDS 后端被 B ship 期间 git status 探到 · 即时处理。

**framework 维度观察**:
- 第一个由 **B + A 真并行模式触发的 hand-back 包** — W1 (10:51:03Z) 写回时间在 B 件 3 ship 中段(11:00 前后) · IDS git status 探到 untracked file · /handback-review 与 B ship 单 commit boundary 严格分离(B 件 2.4 commit `23c4db7` 只 stage parallel-builder guide · A 包仍 untracked · 等本 LOG commit 单独 ship)
- 包 §3 表格 schema v2.2 RECOMMENDED 字段真落地:producer 出 5 列 A1-A5 actionable + §4 自检段 + §7 风险 5 条 · 跟 v2.2 SHARED-CONTRACT §6.3 RECOMMENDED schema 1:1 对齐 · F6 落地后第一包真实运用 reference
- TDD 严格:10 test 先 fail (AttributeError 5 method 不存在) → 实装 → 10/10 PASS · 这是 spec-gap-fix 模式真做法(先红 → 实装 → 绿) · 跟 T010 cross-model 5+1 round 模式互补(后者深度 review · 前者 TDD 真闭环)
- KNOWN_500_PATHS by frozenset → frozenset[str] 类型 append-only pattern · 留类型方便未来追 bug · 这是 ship 时关注 future fault tracking 的好做法

**Follow-up commits**: pending(本 IDS commit 后填)

## 2026-05-12T11:25:30Z · 004-pB-20260512T110141Z

**Reviewed at**: 2026-05-12T11:25:30Z
**Tags**: feature
**Severity**: medium
**Validator (consumer-mode)**: ✓ all 6 constraints PASS — A 通道真并行 ship 第二包(W2 bug2 闭环)· FU-producer-1 ship 后第六次跨非 006 idea 真验
**Related task**: FU-weekly-fix (XenoDev squash commit `09f6cc1`)
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉,作为 practice-stats 入库)

**Operator note**: W2 FU-weekly-fix ship 接受 · v0.1 product bug 2 hotfix(weekly.html L107-111 `{% with maintenance = review.maintenance %}` 桥接 partial 上下文 + 3 integration test + 174/174 PASS + codex round 1 approve 0 finding) · §4 自检不触 PRD-revision-trigger(纯 Jinja2 模板上下文绑定 · 不动 v0.2 spec scope · 无 spec doc amendment) · A1 无 spec 改 · A2 partial 命名风格统一延 backlog refactor(future v0.3+) · A3 test 覆盖扩 backlog · A4 KNOWN_500_PATHS 全清 + 类型保留 append-only pattern · A5 release note tracking。**🎉 plan v0.2-global 件 3.1 阶段 2c 波 1 真闭环**:W1 (commit 7eb8626) + W2 (commit 09f6cc1) = 两 v0.1 product bug 全清 · KNOWN_500_PATHS frozenset(2) → frozenset() 空 · F1b smoke 32/32 PASS · 用户实际可用 /notes + /reviews/weekly。

**framework 维度观察**:
- **B + A 真并行模式连发两包**:W1 (10:51:03Z) + W2 (11:01:41Z) · 间隔 ~10min · 真两 worktree 并起 ship + 顺序 hand-back 写回 · B 通道 ship 件 2.4 期间(commit `23c4db7` ≈ 11:00) · 三 ship 真并行(B 1 + A 2)· 跨仓边界 0 冲突 · plan v12 "B + A 真并行" 模式真实证
- Jinja2 fix path 探索真做法:operator 初选 `{% include "x" with context maintenance=... %}` → TemplateSyntaxError(Jinja2 不接受 keyword args)→ 改 `{% with %}{% include %}{% endwith %}` 桥接 · 这是 producer 真 evidence 链 · 包 §2 决议链段记录(spec doc 不需 amendment 但实战 evidence 锚)
- KNOWN_500_PATHS 类型 append-only 设计:`frozenset[str] = frozenset()` 全空 · 留类型方便未来追 bug · 这是 production smoke test infrastructure 的真做法 · spec 不预决 · operator 实战决定
- v0.1 partial 命名风格 v0.3+ refactor 候选(A2 backlog):`_weekly_maintenance_partial.html` 用 `review.maintenance.*` 显式嵌套 + 删 `{% with %}` 桥接 · 性质同 v0.2 件 4.0c production app factory · v0.2-v0.3 follow-up 集合可加 4.0e

**Follow-up commits**: pending(本 IDS commit 后填)

## 2026-05-12T12:35:00Z · 004-pB-20260512T121248Z

**Reviewed at**: 2026-05-12T12:35:00Z
**Tags**: feature
**Severity**: low
**Validator (consumer-mode)**: ✓ all 6 constraints PASS — FU-producer-1 ship 后第七次跨非 006 idea 真验
**Related task**: T011 Concept self_check + explain_audit + 0009 migration (XenoDev squash commit `e0c2c48`)
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉,作为 practice-stats 入库)

**Operator note**: T011 ship 接受 · v0.2 Phase 2a feature 实装 spec §1.1 O1/O2/O3 ship gate 基础设施(SelfCheckService + ExplainAuditService + MockLLMClient + run-concept-self-check.sh wrapper) · TDD red→green 11/11 PASS + full suite 185/185 PASS(W2 174 + T011 11 = 185)· codex round 1 verdict=approve 0 high/medium ship-blocking · §4 自检不触 PRD-revision-trigger(完全 in v0.2 spec scope · 0 外部依赖 · 不动 v0.1 already shipped code) · A1 spec doc sync(architecture.md §2.1 加 path B' 决议)是跨仓 XenoDev spec 改 · 同 T010 A2 spec-gap-fix 模式 · IDS 端不预决 · 延 XenoDev session 自决 · A2-A3-A5 backlog 入 FU-T011-followup polish queue · A4 T015 scheduler activate tracking。**🎉 plan v0.2-global 件 3.1 阶段 2c 波 2 闭环**:T010(d4d04e7)+ 波 1(7eb8626 + 09f6cc1)+ 波 2 T011(e0c2c48)= v0.2 Phase 2a feature + v0.1 bug 修 + spec amendment 全 ship · T012 入度变 0 · 波 3 可起(T012 / T013 / T020 / T024 自选 · operator 自决)。

**framework 维度观察**:
- **A2 spec-gap-fix 模式真触发 第二次**(T010 第一次 · T011 第二次):0009 migration 加 `concept_explain_log` audit 表 = path B' 修正 spec L70 "expand_count > 1" 真意(spec 字面 vs producer 实装合理化)· 这是 v2.2 schema RECOMMENDED §3 表格 A1 actionable + §4 自检自我承认 spec-gap-fix 的连续 evidence · v0.2-retro §3.3 "A2 spec-gap-fix 模式真触发" 在 T011 ship 后第二次实证 · framework 维度稳定
- **plan-v0.3-global G1 仍 pending**:T011 是 sonnet 6-8h feature · 不算 G1 真触发(G1 = T020 / T024 opus 10-16h 重件 · ship + RETRO ≥7.0)· 本包入 LOG 后 plan v0.3-global 不动 · 等下一 ship
- **包 §3 表格 schema v2.2 RECOMMENDED 字段稳定**:T011 §3 5 行 A1-A5 + §4 自检 + §7 7 条 known gotchas · 跟 W1/W2 同样高度严格遵循 v2.2 schema · v2.2 落地后 producer 端 5 包(F1a/F1b/T010/W1/W2/T011)全 conformant · schema 演化已稳态
- **TDD + cross-model 模式持续**:11 test 先 fail (ModuleNotFoundError + AttributeError) → 7 file 实装 → 11/11 PASS · codex round 1 approve 0 ship-blocking · 与 T010 (5+1 round 12 finding) / F1b (3 round 3 finding) / W1+W2 (1 round 0 finding) 形成 review 深度按 task 复杂度匹配的真稳态(简单 feature 1 round / 复杂 schema 5+1 round)
- **dormant scheduler 设计**:`register_scheduler_job` import 副作用 + main.py 不 import = dormant 状态 · 跟 v0.1 monthly_scheduler 同 pattern · T015 显式 import 触 register · 这是 v0.1 既定的"模块化 lazy activate"设计 · 真有效

**Follow-up commits**: pending(本 IDS commit 后填)

## 2026-05-12T13:15:00Z · 004-pB-20260512T130000Z

**Reviewed at**: 2026-05-12T13:15:00Z
**Tags**: feature
**Severity**: low
**Validator (consumer-mode)**: ✓ all 6 constraints PASS — FU-producer-1 ship 后第八次跨非 006 idea 真验
**Related task**: T012 prompt lookup short-circuit + 30 天 audit caller (XenoDev squash commit `36eb012`)
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉,作为 practice-stats 入库)

**Operator note**: T012 ship 接受 · v0.2 Phase 2a O3 ship gate 真闭环(spec L243 wiki short-circuit 双路径 Web+Telegram) · 12 test PASS + full suite 197/197 PASS + routes 47→48 · codex **2 round adversarial-review**(round 1 verdict=block 2 finding [race condition + slash term] · round 2 fix `5cfc32a` verdict=approve 0 ship-blocking) · §4 自检不触 PRD-revision-trigger(完全 in v0.2 spec scope) · A1 spec doc sync(T012.md 4 处 file path/signature + architecture.md §2.1)是跨仓 XenoDev spec 改 · **同 T010/T011 A2 spec-gap-fix 模式 · 第三次连发触发** · IDS 端不预决 · 延 XenoDev session 自决 · A2-A4 backlog 入 FU-T012-followup polish queue · A5 T040 + opus 重件 tracking。**🎉 plan v0.2-global 件 3.1 阶段 2c 波 3 闭环**:T010(d4d04e7)+ 波 1 W1/W2(7eb8626/09f6cc1)+ 波 2 T011(e0c2c48)+ 波 3 T012(36eb012)= v0.2 Phase 2a (O1/O2/O3 ship gate) 全 ship · T040 入度全就绪 · 波 4 可起(T040 integration test 聚合 / T013/T020/T024 opus G1 重件 · operator 自决)。

**framework 维度观察**:
- **A2 spec-gap-fix 模式真触发 第三次连发**(T010 第一次 · T011 第二次 · T012 第三次):
  - T010:0042→0008 migration 编号 + SQLAlchemy→Pydantic + int→TEXT
  - T011:0009 migration concept_explain_log 表 path B'(修正 spec L70 真意)
  - T012:T012.md L9-12 web/handlers/concept_handler.py→ui/router_concept.py + L11 tg/→telegram/ + L37 signature + L52 mock LLM 说明
  - **连发 3 次**:不再是"年时 corner" · 已是真稳态模式 · v0.3 framework v0.3 升 candidate · 考虑加 SHARED-CONTRACT §6.3 §3 表格新类型字段 "spec-gap-fix" (RECOMMENDED 而非新 normative) · 让 producer 端 spec amendment 提案有 schema 位置(plan v0.3-global §3 T2 candidate "SHARED-CONTRACT v2.3+ 升级"真有 evidence 触发了)
- **codex adversarial-review 2 round 真触发深度**:T012 round 1 verdict=block 2 high/medium finding(race + slash)→ round 2 真 fix → approve。这跟 v0.2-retro §4 评分维度 1 "adversarial-review 深度按 task 复杂度自适应" 一致 · T012 跟 F1b (3 round) 是同等级中等复杂 · 跟 T010 (5+1 round 12 finding) 是低 · 跟 T011 (1 round 0 finding) 是高(因 T011 audit infra 简单设计 · T012 short-circuit + race 复杂设计) · review 深度自适应有效
- **race condition fix 真发现 · framework v2.2 SKILL §9 GATE/AUDIT 真生效**:codex round 1 真挑战 "writer_lock 是否真原子" · 真发现 race condition F1 high · round 2 fix `try_claim_expand` 单 connection 序列化 · 这是 v12 件 2.4 (parallel-builder guide §3 events.jsonl GATE) 实战 evidence · GATE/AUDIT 区分让 agent 不漏 audit 但 review 深度催生真 bug 发现 · 不只是 schema doc
- **包 §3 表格 schema v2.2 RECOMMENDED 字段稳态扩** :T012 §3 5 行 A1-A5 + §4 自检 + §7 7 条 known gotchas · 跟 T011 同 conformance · v2.2 落地后 producer 端 7 包(F1a/F1b/T010/W1/W2/T011/T012)全 conformant · schema 演化 7 包真稳态
- **plan-v0.3-global G1 仍 pending**:T012 是 sonnet 4-6h feature · 不算 G1 真触发(G1 = T020/T024 opus 10-16h 重件) · 本包入 LOG 后 plan v0.3-global 不动 · v0.2 Phase 2a 全闭环但等 opus 重件 ship 才正式启动 v0.3 · operator 自决何时跑 T020/T024
- **race condition 测试 真做法**:codex round 1 真挑战 "Web+Telegram 双路径并发" · round 2 加 test 11 (并发 race N=2) · test 真模拟 race 是 reduction-step pattern · 比单元测试更 strict · 这种"并发 race test"模式可作 v0.3 framework 升 candidate(在 parallel-builder derivation guide §2 audit checklist 加 "并发 race test for stateful operations")

**Follow-up commits**: pending(本 IDS commit 后填)

## 2026-05-17T14:05:00Z · 004-pB-20260517T140000Z

**Reviewed at**: 2026-05-17T14:05:00Z
**Tags**: feature, spec-gap-fix
**Severity**: low
**Validator (consumer-mode)**: ✓ all 6 constraints PASS — FU-producer-1 ship 后第九次跨非 006 idea 真验(v2.2 schema · ≤7 节真稳态 · 5 天后 plan v0.3-global G1 仍 pending 验证)
**Related task**: T013 DevilAdvocateService production wire + prompt md 补全 (XenoDev squash commit `064d659` + spec amend `098f749`)
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉,作为 practice-stats 入库)

**Operator note**: T013 ship 接受 · v0.2 Phase 2 DevilAdvocate 真上线(替 _StubDevil + prompt md 补全 + MockLLMClient.call 扩 8 templates) · 9 unit/e2e + 1 xfail · full suite 208 passed + 1 xfailed · production_app_smoke 33/33 PASS · codex **2 round adversarial-review**(round 1 verdict=block 2 finding [F1 high decision_recorder.create_draft 不传 DecisionDraft → prompt fallback / F2 medium DevilAdvocateService + DecisionRecorder 双 INSERT rebuttals orphan] · round 2 fix `cf4c346` verdict=approve 0 ship-blocking · F1 真闭环 spy LLM 锁 prompt 内容 · F2 锁 xfail backlog FU-T013-followup) · §4 自检不触 PRD-revision-trigger(完全 in v0.2 spec scope · 凭据隔离 / cost cap 全 PASS · spec frozen 边界引发 retroactive doc-fix 用 spec amendment commit `098f749` audit trail · 跟 T010/T011/T012 同 pattern) · A1 tracking `_StubDevil` 闭环 · A2 spec amend already applied · A3 FU-T013-followup 修 F2 双写(选项 A 或 B)medium · A4 wheel package_data prompt md hardening low · A5 T040 入度全就绪 · A6 wire.py docstring polish low · 全延 XenoDev session 自决。**🎉 plan v0.2-global 件 3.1 阶段 2c 波 4 闭环**:T010(d4d04e7)+ 波 1 W1/W2(7eb8626/09f6cc1)+ 波 2 T011(e0c2c48)+ 波 3 T012(36eb012)+ 波 4 T013(064d659 + 098f749)= v0.2 Phase 2 全 4 task(O1/O2/O3 ship gate + DevilAdvocate 真上线)全 ship · T040 入度 T010 + T011 + T012 + T013 全 ready · 波 5 可起(T040 integration test 聚合 / T020 / T024 opus G1 重件 · operator 自决)。

**framework 维度观察**:
- **A2 spec-gap-fix 模式真触发 第四次连发**(T010 第一次 · T011 第二次 · T012 第三次 · T013 第四次):
  - T010:0042→0008 migration 编号 + SQLAlchemy→Pydantic + int→TEXT
  - T011:0009 migration concept_explain_log 表 path B'(修正 spec L70 真意)
  - T012:T012.md L9-12 file path + signature + L52 mock LLM 说明 + architecture.md §2.1
  - T013:`tasks/T013.md` 新加 + dependency-graph.mmd +3 LOC + spec.md §6 +4 LOC (Phase 2-amend 段)· 单独 commit `098f749` 留 audit trail
  - **连发 4 次**:不是"年时 corner" · 不是"前 3 次 outlier" · 是真稳态 producer 端 default workflow · v0.3 framework v0.3 升 candidate 真有连发 4 次 evidence 触发了 · 考虑加 SHARED-CONTRACT §6.3 §3 表格新类型字段 "spec-gap-fix" (RECOMMENDED) · 或在 §3 表格 type 列新加 "spec-gap-fix · ship 后 amend" 作为公认 producer pattern · plan v0.3-global §3 T2 candidate "SHARED-CONTRACT v2.3+ 升级" evidence 强化
- **包 §3 表格 schema v2.2 RECOMMENDED 字段连发 4 包稳态**:T013 §3 6 行 A1-A6 + §4 7 项 PRD-revision-trigger 自检 + §5 6 条后续 task + §6 file changes + §7 7 条 known gotchas · v2.2 schema 全 7 节占满(3 normative §1/§2/§3 + 4 RECOMMENDED §4/§5/§6/§7) · 跟 T011/T012 同 conformance · v2.2 落地后 producer 端 **8 包**(F1a/F1b/T010/W1/W2/T011/T012/T013)全 conformant · schema 演化连发 8 包真稳态(超 v0.2-retro 5 包 baseline · 比 W12-A 多 3 包)
- **codex 2 round adversarial-review 真发现 production bug 第二次**:T013 round 1 F1 high 真发现 `decision_recorder.py:260` 不传 DecisionDraft → prompt 渲染成 "—" · production 真路径 prompt 失效 · e2e test 漏 spec 真路径(只验"非 stub 文本") · round 2 加 spy LLM 锁 prompt 内容 · 跟 T012 race condition fix 同等级 · 这是 v12 件 2.4 (parallel-builder guide §3 events.jsonl GATE + §2 AUDIT/GATE 区分) 实战 evidence 第二次 · adversarial-review 不只是 schema doc 校验 · 真出 production bug · plan v0.3-global §3 T2 candidate "codex review derivation guide" 真有 ROI 触发
- **xfail backlog 模式真触发**:T013 round 2 加 test 5 xfail (strict=False · F2 双写) 真锁 backlog · FU-T013-followup 修复后翻 strict=True · 这是 v0.3 framework 升 candidate "production-correct backlog 模式"(stable feature ship + 已知 design bug 用 xfail 真锁 · 不破 ship gate · 修复时 strict=True 真验) · 跟 v0.2-retro §3.4 "polish backlog 真有效" 一致 · 在 T013 第一次正式用 xfail strict=False 锁 design bug · 不是 polish · 是 production-design backlog
- **plan-v0.3-global G1 仍 pending(5 天后再验)**:T013 是 medium 复杂 sonnet 任务(8h codex 2 round)· 不算 G1 真触发(G1 = T020/T024 opus 10-16h 重件)· v0.2 Phase 2 全 ship 但 v0.3 真启动等 opus 重件 · 本包入 LOG 后 plan v0.3-global 不动 · operator 自决何时跑 T020/T024 真 G1(plan v0.3-global v1.0 draft 5 天后仍 stable · 无需 patch · 5 天后稳态验证通过)
- **件 3.1 阶段 2c 波 4 闭环 + v0.2 Phase 2 全 ship**:T010+W1+W2+T011+T012+T013 = 6 ship(IDS 9 个 hand-back 包累计)· O1/O2/O3 ship gate + DevilAdvocate 真上线 = v0.2 Phase 2 全闭环 · T040 入度全就绪 = v0.2 Phase 2a→Phase 2b 边界完成 · v0.3 起跑还差 G1 (opus 重件 ship + RETRO ≥7.0)
- **A2 spec-gap-fix 是否要 escalate 到 framework v0.3 真触发**:连发 4 次后 evidence 已充足 · 应在 plan v0.3-global §3 T2 candidate 1 "SHARED-CONTRACT v2.3+ 升 spec-gap-fix RECOMMENDED 字段" 加触发说明 · 但不立即改 SHARED-CONTRACT(等 G1 触发 + v13 sub-plan 一并落) · 本 LOG 入库即触发

**Follow-up commits**: pending(本 IDS commit 后填)

## 2026-05-17T22:05:00Z · 004-pB-20260517T220000Z

**Reviewed at**: 2026-05-17T22:05:00Z
**Tags**: feature, spec-gap-fix, partial-scope
**Severity**: low
**Validator (consumer-mode)**: ✓ all 6 constraints PASS — FU-producer-1 ship 后第十次跨非 006 idea 真验(v2.2 schema · ≤7 节 + 新 tag `partial-scope` 第一次出现 · tag 演化)
**Related task**: T040-A partial Phase 3 ship gate(red-line + 30s SLA + O1/O2/O3 aggregate · XenoDev squash commit `f583654` + spec amend `2824d35`)
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉,作为 practice-stats 入库)

**Operator note**: T040-A ship 接受 · v0.2 Phase 3 partial ship gate 真上线(O1/O2/O3 aggregate + R-1 红线 enforcement + SLA §1.1 30s wall-clock) · 15 collected: 8 passed + 7 skipped(skipped 是 O4-O9 等 T020-T030 入度未 ship 自动 skipif · 设计如此) · full suite 216 passed + 7 skipped + 1 xfailed(0 回归) · production_app_smoke 33/33 · codex **2 round adversarial-review**(round 1 verdict=needs-attention 3 medium finding [F1 空 DB false-green / F2 SRC_ROOT 窄 / F3 Action enum 不 exact] · round 2 fix `0a1015b` verdict=approve 0 ship-blocking) · §4 自检不触 PRD-revision-trigger(完全 in v0.2 spec scope · 凭据隔离 / cost cap / SLA / smoke baseline 全 PASS · spec frozen 边界引发 retroactive doc-fix 用 spec amend commit `2824d35` audit trail · 跟 T010/T012/T013 同 pattern) · A1 tracking T040-A partial ship 闭环 · A2 spec amend already applied(T040 拆 T040-A/T040-B) · A3-A4 spec doc-lag(`human_action` 字段名口误 + `pre_filled_action_draft` v1.5+ 字段)留 tracking · A5 backlog per-row recall_score assertion polish · A6 T040-B 入度 7 opus 重件 tracking · A7 backlog 手动 5/5 SLA 压测 operator 自跑 · 全延 XenoDev session / operator 自决。**🎉 plan v0.2-global 件 3.1 阶段 2c 波 5 闭环**:T010(d4d04e7)+ 波 1 W1/W2(7eb8626/09f6cc1)+ 波 2 T011(e0c2c48)+ 波 3 T012(36eb012)+ 波 4 T013(064d659 + 098f749)+ 波 5 T040-A(f583654 + 2824d35)= v0.2 Phase 2 全 4 task(O1/O2/O3 ship gate + DevilAdvocate 真上线)+ Phase 3 partial ship gate 全 ship · T040-B + 7 opus 重件(T020/T021/T022/T023/T024/T025/T030 ≈ 60-80h)入度等 next wave · 由 operator 决议。

**framework 维度观察**:
- **A2 spec-gap-fix 模式真触发 第五次连发**(T010 第一次 · T011 第二次 · T012 第三次 · T013 第四次 · T040 第五次):
  - T010:0042→0008 migration 编号 + SQLAlchemy→Pydantic + int→TEXT
  - T011:0009 migration concept_explain_log 表 path B'(修正 spec L70 真意)
  - T012:T012.md L9-12 file path + signature + L52 mock LLM 说明 + architecture.md §2.1
  - T013:`tasks/T013.md` 新加 + dependency-graph.mmd +3 LOC + spec.md §6 +4 LOC
  - T040:T040 拆 T040-A partial / T040-B 完整 · `tasks/T040.md` amend frontmatter (partial_scope + deferred_to_T040_B) + dependency-graph.mmd 重接 edges + spec.md Phase 3-amend 段 · 单独 commit `2824d35`
  - **连发 5 次**:不是"年时 corner" · 不是"前 4 次 outlier" · 是 producer 端 default workflow 5 次连发 真稳态 · v0.3 framework v0.3 升 candidate **强触发**(plan v0.3-global §3 T2 candidate "SHARED-CONTRACT v2.3+ 升级"5 连发 evidence 触发了 · 真该启动 v0.3 framework 升 · 把 §3 表格 type 列加 "spec-gap-fix · ship 后 amend" RECOMMENDED 字段) · 5 次连发也是 v0.2-retro §3.3 "A2 spec-gap-fix 模式真触发" 的 conclusive evidence
- **新 tag `partial-scope` 第一次出现**(v2.2 schema 演化):T040 是 ship gate 聚合 task · spec depends_on 6 个 task · 真 ship 仅 3/6 · 拆 T040-A partial + T040-B 完整 · 新 tag `partial-scope` 跟 `feature` + `spec-gap-fix` 并列。**v2.2 schema 没显式列 partial-scope 但允许 RECOMMENDED tag** · T040 是第一次 producer 端真用 partial-scope tag · v0.3 framework v0.3 升 candidate 把 `partial-scope` 入 §3 tags 规范集(v2.2 RECOMMENDED · v0.3 normative)· 让 partial ship 有 schema 位置
- **包 §3 表格 schema v2.2 RECOMMENDED 字段连发 5 包稳态**:T040-A §3 7 行 A1-A7(超 T013 6 行 · T012 5 行 · v2.2 schema RECOMMENDED 字段 5+ 行均 conformant) + §4 8 项 PRD-revision-trigger 自检(新加 SLA §1.1 30s 行 · 跟 T040-A 真 scope 紧 couple) + §5 11 条后续 task(新加 T040-B + 7 opus 重件 + 2 polish + 1 inherit FU-T013-followup) + §6 file changes(新建 5 文件 0 修改 · pure additive ship) + §7 9 条 known gotchas · v2.2 schema 全 7 节占满 + RECOMMENDED 字段连 5 包稳态扩(超 8 包 baseline · 9 包真稳态) · producer 端 9 包(F1a/F1b/T010/W1/W2/T011/T012/T013/T040)全 conformant
- **codex 2 round adversarial-review 真发现 production-quality bug 第三次**:T040-A round 1 真发现:
  - F1 空 DB false-green:test_all_outcomes_aggregate.py O1/O2 部分不验 spec L66 ≥7 Concept · round 2 fix tmp_path SQLite + alembic upgrade + seed 7 Concept · O1/O2 真路径验
  - F2 SRC_ROOT 窄:R-1 红线扫 src/decision_ledger 太窄 · 未来 sibling package 绕过 · round 2 fix SRC_ROOT = src/ 全树 · 跟 spec 命令字节级对齐
  - F3 Action enum 不 exact:assert 1 forbidden substring 漏 rebalance/short/limit_buy 类破不变量 · round 2 fix exact set match
  - **3 finding 全是 silent green 类**(test 看似 pass 实际 prod 会爆) · 跟 F1b 同等级 · 跟 T013 F1 prompt fallback 同性质 · adversarial-review 第三次真出 production-quality bug · plan v0.3-global §3 T2 candidate "codex review derivation guide" ROI **连续 3 次实证**(T012 race / T013 prompt fallback / T040-A silent green)
- **plan-v0.3-global G1 仍 pending(10 天后再验)**:T040-A 是 medium 复杂 sonnet 任务(8h codex 2 round)· 不算 G1 真触发(G1 = T020/T024 opus 10-16h 重件 + RETRO ≥7.0)。**5 月 12 日 T012 sonnet · 5 月 17 日 14:00 T013 sonnet · 5 月 17 日 22:00 T040-A sonnet · 6 天 3 ship 全 sonnet** · operator 在 small/medium feature 上连续 ship 没碰 opus 重件 · v0.3 真启动等 T020/T024/T030 opus 重件 ship · plan v0.3-global v1.0 draft 10 天后仍 stable · 无需 patch · 真稳态验证通过
- **件 3.1 阶段 2c 波 5 闭环 + v0.2 Phase 2 + Phase 3 partial ship**:T010+W1+W2+T011+T012+T013+T040-A = 7 ship(IDS 10 个 hand-back 包累计) · v0.2 Phase 2 全 4 task ship + Phase 3 partial(O1/O2/O3 + R-1 + SLA) = v0.2 v0.2 ship gate 基础设施完整 ship · T040-B 等 T020-T030 全 ship 才能完整 O1-O9 · 还差 7 opus 重件(60-80h)
- **新 tag partial-scope = v0.3 framework v0.3 升真触发 candidate**(plan v0.3-global §3 T2 candidate "SHARED-CONTRACT v2.3+ 升级" 第二个 evidence · 跟 spec-gap-fix 5 连发并列) · 不立即改 SHARED-CONTRACT(等 G1 触发 + v13 sub-plan 一并落) · 本 LOG 入库即触发

**Follow-up commits**: pending(本 IDS commit 后填)

## 2026-05-17T23:05:00Z · 004-pB-20260517T230000Z

**Reviewed at**: 2026-05-17T23:05:00Z
**Tags**: feature, spec-gap-fix, spine-task
**Severity**: low
**Validator (consumer-mode)**: ✓ all 6 constraints PASS — FU-producer-1 ship 后第 11 次跨非 006 idea 真验(v2.2 schema · 新 tag `spine-task` 第一次出现 · tag 演化第二个新 tag)
**Related task**: T020 Phase 2b parser.py 三层重构(SourceAdapter/FormatHandler/Fetcher + orchestrator · XenoDev squash commit `8cb49e2` + spec amend `a37c388`)
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉,作为 practice-stats 入库)

**Operator note**: T020 ship 接受 · v0.2 Phase 2b spine task 真上线(parser.py 三层 Protocol 重构 · SourceAdapter / FormatHandler / Fetcher + PipelineOrchestrator) · TDD red→green 16/16 PASS + full suite 232 passed + 7 skipped + 1 xfailed(原 216 + T020 16 · 0 回归) · production_app_smoke 33/33 · routes 48 不变 · alembic 0010 真 upgrade 0007→0008→0009→0010 OK · codex **2 round adversarial-review**(round 1 verdict=needs-attention 2 finding [F1 high orchestrator bytes→tmp 后 cache key 漂移 + audit 指向已删 tmp · 真 R-v022-2 漏洞 / F2 medium file:// URL percent-encoded 不解码] · round 2 fix `230449d` verdict=approve 0 ship-blocking · F1 file source 直 parse(Path(original_path)) 跳 tmp + HTTP source `_derive_stem` 派生 deterministic / F2 urllib.parse + unquote 真解码) · §4 PRD-revision-trigger 自检 10 项全 PASS(新加 R-v022-2 双路径等价行 + SLA §1.1 30s 行 + 凭据隔离硬约束 #1 行)· A1 tracking T020 spine ship 闭环 · A2 spec amend already applied(migration 0043→0010 + table 名 advisor_parser_output→advisor_reports + R-v022-2 regression test)· A3 spec doc-lag advisor_parser_output→advisor_reports 留 tracking · A4 FU-T020-followup parse_bytes API medium · A5/A6 polish backlog(中文 URI + _derive_stem sanitize) · A7 alembic 0010 downgrade spec compliance · A8 入度释放 T021/T022/T023/T030 ready · A9 inherit FU-T013-followup · 全延 XenoDev session / operator 自决。**🎉 plan v0.2-global 件 3.1 阶段 2c 波 6 闭环**:T010(d4d04e7)+ 波 1 W1/W2(7eb8626/09f6cc1)+ 波 2 T011(e0c2c48)+ 波 3 T012(36eb012)+ 波 4 T013(064d659 + 098f749)+ 波 5 T040-A(f583654 + 2824d35)+ 波 6 T020(8cb49e2 + a37c388)= v0.2 Phase 2 全 4 task + Phase 2b spine + Phase 3 partial ship gate 全 ship · T021/T022/T023/T030 入度 ready · T040-B 等 T021-T030 · T024 旁路 T020 不阻塞 · 由 operator 决议 next wave。

**framework 维度观察**:
- **A2 spec-gap-fix 模式真触发 第六次连发**(T010 第一次 · T011 第二次 · T012 第三次 · T013 第四次 · T040 第五次 · T020 第六次):
  - T010:0042→0008 migration 编号 + SQLAlchemy→Pydantic + int→TEXT
  - T011:0009 migration concept_explain_log 表 path B'(修正 spec L70 真意)
  - T012:T012.md L9-12 file path + signature + L52 mock LLM 说明 + architecture.md §2.1
  - T013:`tasks/T013.md` 新加 + dependency-graph.mmd +3 LOC + spec.md §6 +4 LOC
  - T040:T040 拆 T040-A partial / T040-B 完整 · spec amend 拆 partial_scope + deferred_to_T040_B
  - T020:T020.md amend migration_id 0043→0010 + table name advisor_parser_output→advisor_reports + file_domain 加 R-v022-2 regression test · 单独 commit `a37c388`
  - **连发 6 次**:超 5 连发"强稳态" baseline 进入 **6 连发 = producer 端 default workflow 真事实** · v0.3 framework v0.3 升 candidate **强强触发**(plan v0.3-global §3 T2 candidate "SHARED-CONTRACT v2.3+ 升级"6 连发 evidence · 已不是 candidate · 是真触发即落)
- **新 tag `spine-task` 第一次出现**(v2.2 schema 演化第二个新 tag):T020 是 spec L23 `suggested_executor_model=opus` + risk_level=high + D-spec-2 option a 大重构 = spine task · 跟 `feature` + `spec-gap-fix` 并列 3 tag。**v2.2 schema 没显式列 spine-task 但允许 RECOMMENDED tag** · T020 是第一次 producer 端真用 spine-task tag · v0.3 framework v0.3 升 candidate 把 `spine-task` 跟 `partial-scope` 一起入 §3 tags 规范集(v2.2 RECOMMENDED · v0.3 normative)· 让 spine task / partial ship 都有 schema 位置
- **包 §3 表格 schema v2.2 RECOMMENDED 字段连发 6 包稳态**:T020 §3 9 行 A1-A9(超 T040-A 7 行 · T013 6 行 · T012 5 行 · v2.2 schema RECOMMENDED 字段 9 行真扩) + §4 10 项 PRD-revision-trigger 自检(新加 R-v022-2 双路径等价行 + SLA §1.1 行 + 凭据隔离硬约束 #1 行 · 比 T040-A 8 项 又扩 2) + §5 12 条后续 task(新加 T021/T022/T023/T030 入度 ready · T040-B 等 deps · 5 polish backlog · 1 inherit FU-T013-followup) + §6 file changes(新建 19 文件 3 修改 · 大重构) + §7 9 条 known gotchas · v2.2 schema 全 7 节占满 + RECOMMENDED 字段连 6 包稳态扩(超 9 包 baseline · 10 包真稳态) · producer 端 10 包(F1a/F1b/T010/W1/W2/T011/T012/T013/T040/T020)全 conformant
- **codex 2 round adversarial-review 真发现 production-quality bug 第四次**:T020 round 1 真发现:
  - F1 high orchestrator cache key 漂移:bytes→tmp 后 random name → pdf_path.stem 漂移 + audit 指 deleted tmp · **真破 R-v022-2 双路径等价**(spec L51 v0.1 PDF e2e regression 必 PASS) · round 2 fix file source 跳 tmp + HTTP source `_derive_stem(source)` 派生 · cache key deterministic 不漂移
  - F2 medium file:// URL percent-encoded 不解码:`a b.pdf` → `a%20b.pdf` → FileNotFoundError · round 2 fix urllib.parse + unquote 真解码 · netloc 验空/localhost
  - **2 finding 全是 production-quality bug**(F1 是真 R-v022-2 漏洞 + F2 是 input shape 真破)· 跟 F1b 同等级 · 跟 T013 F1 prompt fallback 同性质 · adversarial-review 第四次真出 production-quality bug · plan v0.3-global §3 T2 candidate "codex review derivation guide" ROI **连续 4 次实证**(T012 race / T013 prompt fallback / T040-A silent green / T020 R-v022-2 漏洞)
- **plan-v0.3-global G1 真触发 candidate**(重要):
  - T020 spec L23 `suggested_executor_model=opus` + risk_level=high + spine-task tag · **plan v0.3-global §1 G1 例子明确列 T020 作 G1 候选**
  - 但 G1 定义文字 = "**A 通道 ≥1 大 vertical-slice 重件(T020 / T024 任一)ship + RETRO ≥7.0**" · 实际是 spec 估时 10-14h opus 任务 ship · RETRO 评分待 operator 自评(本包 hand-back 不算 RETRO · RETRO 是 idea / sub-plan 级 retrospective 文档)
  - **G1 触发关键问题**:RETRO ≥7.0 是 plan v0.2-global v12 RETRO 模式(idea sub-plan 全集 RETRO · 不是 single task RETRO)· 单 T020 ship 是否触发 G1 需 operator 决议:
    - 路径 (a):**T020 ship 单算 G1** · 即 plan v0.3-global v1.1 启动 → plan-rosy-naur v13 起 sub-plan 落地 v0.3 第一波
    - 路径 (b):**等 T024 也 ship 后 + plan-rosy-naur v13 sub-plan 集合 RETRO ≥7.0** 才算 G1
    - 路径 (c):**当前 sub-plan vehicle 继续 reset · 等 operator 真启动 plan v0.3 时决议** · 现状不动 plan v0.3-global
  - 我倾向路径 (c) - 本 hand-back review 不动 plan · LOG 入库即触发 framework 维度观察 · operator 起 plan-rosy-naur v13 时正式决议 G1 状态(v13 sub-plan 启动条件 = G1 触发)
- **件 3.1 阶段 2c 波 6 闭环 + v0.2 Phase 2/2b/3 partial 全 ship**:T010+W1+W2+T011+T012+T013+T040-A+T020 = 8 ship(IDS 11 个 hand-back 包累计) · v0.2 Phase 2 全 4 task + Phase 2b spine + Phase 3 partial = v0.2 主体 ship gate + 重构基础全 ship · 剩 T021/T022/T023/T030(入度 ready · sonnet 6-12h)+ T024(独立 opus 重件 · 旁路 T020) + T040-B(等 T021-T030) · v0.2 收官只差 5-6 task
- **新 tag spine-task 第二个 framework v0.3 升 evidence**(跟 partial-scope 一起):plan v0.3-global §3 T2 candidate "SHARED-CONTRACT v2.3+ 升级" 已 3 个 evidence:
  - (1) spec-gap-fix 6 连发
  - (2) partial-scope tag 第一次出现(T040-A)
  - (3) spine-task tag 第一次出现(T020)
  - **3 evidence 全到位 · v0.3 framework 升真该启动**(operator 起 plan-rosy-naur v13 时决议)
- **R-v022-2 双路径等价锁 = framework 维度看不见的 production-quality 真功夫**:T020 F1 不 review 直接 ship · main 留 cache key 不稳定 + audit 错路径 · production 真 hazard。codex round 1 verdict=needs-attention 是 adversarial-review 真 ROI 实证 · 跟 T013 F1 prompt fallback 同等级 · 是 plan v0.3-global §3 T2 candidate "codex review derivation guide" 的连续 4 次硬证据
- **6 连发 spec-gap-fix + 2 新 tag = v0.3 framework 升真触发**:不立即改 SHARED-CONTRACT(等 G1 触发 + plan-rosy-naur v13 sub-plan 一并落) · 本 LOG 入库即触发 evidence 集合到 plan v0.3-global §3 candidate

**Follow-up commits**: pending(本 IDS commit 后填)

## 2026-05-18T01:35:00Z · 004-pB-20260518T013000Z

**Reviewed at**: 2026-05-18T01:35:00Z
**Tags**: feature, codex-multi-round, backlog-accepted
**Severity**: medium
**Validator (consumer-mode)**: ✓ all 6 constraints PASS — FU-producer-1 ship 后第 12 次跨非 006 idea 真验(v2.2 schema · 2 新 tag 第一次出现 · codex-multi-round + backlog-accepted · tag 演化第 3+4 个新 tag · severity 第一次升 medium)
**Related task**: T022 Phase 2b transcription module(Whisper API + KeypointExtractor + WhisperUsageAudit + LocalWhisperTranscriber ABC + AudioFormatHandler 实装 · XenoDev squash commit `f5e513e`)
**Operator decisions**:
- [x] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [x] 修 XenoDev spec(本仓内,信息式)— A1 路径:跨仓 cd XenoDev 改 specs/004-pB/spec.md + risks.md 3 处(R-v022-1 mitigation + R-v022-3 新加 + IN-v022-4 verification)· IDS 端不动 specs/004-pB/(CLAUDE.md Prohibited M3 archive)
- [x] 无操作(收悉,作为 practice-stats 入库)— FU-T022-followup-1 (high · partial-failure recovery) 留 backlog · FU-T022-followup-3 (medium · codex-review SKILL §3.2 path B 错) 留 framework maintenance backlog · FU-T022-followup-2 + FU-T022-followup-4 是 T030 scope

**Operator note**: T022 ship 接受 · v0.2 Phase 2b transcription module 真上线(WhisperTranscriber + KeypointExtractor + WhisperUsageAudit CLI + LocalWhisperTranscriber ABC · D-spec-5 D-spec-5a 全实装) · TDD red→green 24/24 PASS + full suite 256 passed + 7 skipped + 1 xfailed(baseline 232 + T022 24 · 0 回归) · pipeline/transcription/ TOTAL coverage 85%(spec verification "≥85%" 字面满足) · CLI `python -m decision_ledger.pipeline.transcription.usage_audit --month-to-date --report` 真出 JSON 含 cost_usd · audio_handler magic bytes detect ID3/RIFF/OggS/M4A/raw MP3 sync + parse_async 真接 transcriber+extractor。**codex 6 round adversarial-review** 超 SKILL §4.2 cap 4 round(operator A 决议超 cap 2 轮):Round 1-5 全部闭环(F1 verbose_json+duration / F2 OpenAI SDK 异常 / F3 cache key transcript_sha256_16 / F4 5xx InternalServerError / F5 408/409 + 4xx 永久 / F6 retry 边界 _record_usage / F7 usage 失败不阻 transcript)· **Round 6 高 finding F1 extractor 失败丢 transcript · partial-failure recovery 真架构题** · operator A 决议接受 backlog(FU-T022-followup-1)· 真根因跨 T022/T030 边界需 transcript_cache 模块。**T022 是第一个真要求 IDS 端 spec maintenance 的 hand-back · IDS 决议 A1 路径**:hand-back §6 的 spec.md / risks.md = XenoDev 端 specs/004-pB/(SHARED-CONTRACT §6 v2.0 由 XenoDev 持) · IDS specs/004-pB/ 已 M3 archived(CLAUDE.md Prohibited · commit d3194a0)· 跨仓 spec maintenance 由 operator 切 XenoDev session 做 · 跟 prior 11 ship pattern 一致(T010 A2 / T012 4 处 / T013 / T040-A / T020 全 XenoDev 端单独 commit)· IDS 端只 LOG entry 记决议 + tracking。**FU 队列**:FU-T022-followup-1(high · partial-failure recovery 跨 T022/T030 边界)留 IDS forge 决议 candidate(v0.3 transcript_cache 架构 task);FU-T022-followup-3(medium · codex-review SKILL §3.2 path B `review` 不支持 focus text · 实跑须 `adversarial-review`)留 framework maintenance backlog(IDS 端 .claude/skills/codex/codex-review/SKILL.md 改 · scope 极小 · 跟 T2 件 2.4 SKILL 维护同性质)· operator 决议晚一批一起做。**🎉 plan v0.2-global 件 3.1 阶段 2c 波 7 闭环**:T010(d4d04e7)+ 波 1 W1/W2(7eb8626/09f6cc1)+ 波 2 T011(e0c2c48)+ 波 3 T012(36eb012)+ 波 4 T013(064d659 + 098f749)+ 波 5 T040-A(f583654 + 2824d35)+ 波 6 T020(8cb49e2 + a37c388)+ 波 7 T022(f5e513e)= v0.2 Phase 2 全 4 task + Phase 2b spine T020 + Phase 2b transcription T022 + Phase 3 partial T040-A 全 ship · T030 入度 ready · T021/T023 入度 ready · v0.2 收官还差 3-4 task。

**framework 维度观察(本包真有质的不同 · 信息量重)**:
- **第一次 severity=medium 包**(前 11 包全 low):T022 升 medium 真因 = 1 high finding(FU-1 partial-failure recovery)operator A 路径接受 backlog · 不是 ship-blocking · 但跨任务边界架构题留 backlog 是 medium-severity 信号 · plan v0.3-global framework 升 candidate 真触发"severity 维度有效"实证
- **2 个新 tag 第一次出现 · 累计新 tag 4 个**:
  - 累计:partial-scope(T040-A) + spine-task(T020) + **codex-multi-round(T022 第一次)** + **backlog-accepted(T022 第一次)**
  - `codex-multi-round`:6 round 超 SKILL §4.2 cap 4 round · operator A 路径超 cap 2 轮接受 · 真信号 = adversarial-review 长尾(round 4-6 同类 partial-failure recovery pattern · 每修一处 codex 找下一处 · 真根因架构题)· cap 设计合理 · 超 cap 走 operator A/B/C 真有价值
  - `backlog-accepted`:operator A 路径接受 high finding 留 backlog(不阻 ship · 但跨边界架构题)· 跟 spec-gap-fix 类似的 v0.3 framework 升 candidate · §3 tags 规范集真该升 normative
  - **4 evidence 全到位 · plan v0.3-global §3 T2 candidate "SHARED-CONTRACT v2.3+ 升级" 真该启动**(operator 起 plan-rosy-naur v13 时一并落 normative tags 列:spec-gap-fix + partial-scope + spine-task + codex-multi-round + backlog-accepted)
- **A2 spec-gap-fix 模式 T022 真"无 spec gap"**(第七次 spec amendment 模式真断 · evidence 限定):
  - 前 6 task(T010/T011/T012/T013/T040/T020)全 spec-gap-fix · 6 连发 = producer 端 default workflow 真稳态
  - T022 §3 A-row tracking 真"无 spec gap" · file_domain 字面满足 · 是 producer 端**第一次** spec 跟实装零差 · 这是 v0.2 spec 质量提升信号 · 不是 spec-gap-fix 模式失效 · 而是 v0.2 spec 越走 producer 端越熟(T022 spec 写 v0.5 接口预留 + cost cap 决策 · 实装直对应)
  - 但仍 medium 严重度 · 因 §4 backlog 真有 high finding · spec 质量好 ≠ implementation 无 hidden bug · adversarial-review 仍真出 production-quality bug · plan v0.3 framework 升 candidate "codex review derivation guide" 第 5 次实证
- **codex adversarial-review ROI 连续 5 次实证 + 长尾 pattern 第一次显形**:
  - 累计:T012 race / T013 prompt fallback / T040-A silent green / T020 R-v022-2 漏洞 / **T022 6 round partial-failure recovery 架构题**(第 5 次 · 第 1 次长尾)
  - T022 是 review 长尾真信号 · round 1-3 单点 implementation bug · round 4-6 同类 pattern 长尾 · 真根因架构题 · cap 设计真合理(简单 ship 1-2 round · 复杂 ship 4-6 round 走 operator A/B/C 决议)
  - plan v0.3 framework 升 candidate "codex review derivation guide" 5 次连发 evidence + 长尾 pattern 实证 · ROI 已硬触发
- **第一次 IDS 端真有 actionable spec maintenance**(前 11 包全 IDS 不预决):
  - 前 11 包 §6 全说"不修 PRD" · operator 都 [4] 收悉
  - **T022 §6 真要求**改 spec.md / risks.md 3 处(R-v022-1 mitigation + R-v022-3 新加 + IN-v022-4 verification)
  - operator A1 决议 = 跨仓 cd XenoDev 改 specs/004-pB/(SHARED-CONTRACT §6 v2.0 由 XenoDev 持 · IDS specs/ M3 archived 不动)
  - 这是**第一次 hand-back §6 真触发跨仓 spec maintenance work** · IDS 端 LOG entry 只 tracking · 实际改在 XenoDev session
  - **framework 维度 evidence**:hand-back §6 不再是"producer 自我自检"占位 · 真触发 cross-repo 维护 · 跟 SHARED-CONTRACT §6.4.1 Step 5 闭环责任(IDS 异步段)真符合
- **plan-rosy-naur v13 sub-plan 启动条件 candidate 累积**:
  - G1 (T020 spine ship) 已 candidate · plan v0.3 决议 path (c) 暂不动
  - 现 加 T022 hand-back **第一次真有 IDS actionable** + **4 新 tag 累积** + **codex adversarial-review 5 次 + 长尾 pattern** = v0.3 framework 升真该启动 evidence 已重(超 v0.2 启动门槛)
  - 但仍按 plan v0.3 path (c) 路径:operator 起 plan-rosy-naur v13 时正式决议(本 hand-back review 不动 plan)· evidence 集合到 plan v0.3-global §3 candidate 强化
- **件 3.1 阶段 2c 波 7 闭环 + v0.2 主体 ship 接近收官**:T010+W1+W2+T011+T012+T013+T040-A+T020+T022 = 9 ship(IDS 12 个 hand-back 包累计) · v0.2 Phase 2 全 4 + Phase 2b spine T020 + Phase 2b transcription T022 + Phase 3 partial T040-A = v0.2 主体重件全 ship · 剩 T021(scheduled fetcher · sonnet 8-12h)+ T023(Telegram alert · sonnet 6-8h)+ T030(PPV + 多模态 e2e · sonnet 8-12h)+ T024(XGBoost · opus 12-16h G1 候选) + T025(冲突报告 UI · sonnet 6-8h)+ T040-B(等 deps · sonnet 5-8h) · v0.2 完整收官 ≈ 4-6 task + ≈ 40-50h(T024 算 opus G1)
- **第一次 hand-back §6 真触发 cross-repo spec maintenance follow-up commit · XenoDev 端 commit `0736d4a`**:
  - prior 11 包 Follow-up commits 全 pending(操作上只 LOG entry + 不动 spec/risks)
  - T022 是第一次 hand-back §6 触发跨仓真改 spec/risks + 真出 XenoDev commit 反向引用 IDS entry
  - audit trail 真闭环 path:IDS handback-id 004-pB-20260518T013000Z → IDS commit 651a25c LOG entry 12 → XenoDev commit 0736d4a(specs/004-pB/spec.md §IN-v022-4 verification 加实际值 + risks.md §R-v022-1 mitigation + §R-v022-3 新加)→ IDS 本 maintenance commit append Follow-up reference
  - **跨仓 audit 闭环模型实证**:SHARED-CONTRACT §6.4.1 Step 5 闭环责任(IDS 异步段)真符合 · "producer 写 → consumer 决议 → consumer 异步 follow-up 反引 producer commit" 三步完整跑通
- **FU-T022-followup-3 status: applied · XenoDev 端 commit `47d6c2a`(framework maintenance · codex-review SKILL §3.2 path B 修)**:
  - 触发:T022 §4 backlog · FU-T022-followup-3(medium · codex-review SKILL path B 真路径错)operator 决议起 framework maintenance(不算 task / 不算 ship)
  - **operator 关键反对意见纠偏**:不接受"用 adversarial-review 替代 review + focus text"(两工具目标本质不同:review = 平衡评估 + 协作型 senior · adversarial-review = 对抗找 bug + 怀疑型攻击者)· 用 adv 替 review = 拿榔头干起子 · 杀伤过大 + 浪费 round + 走偏目标 · T022 6 round 部分根因就是误升级触发的滚雪球
  - **真路径(由 XenoDev 端 verify + plan mode 出方案 operator 批准)**:具体改法见 XenoDev commit 47d6c2a · 优化 review 用法本身(verify 真支持的参数 / prompt 引导 / decision tree 选工具)· 不是粗暴 fallback adv
  - **位置 verify 纠错**:本 maintenance 第一次发现 codex-review SKILL 在 XenoDev 仓内 `.claude/skills/codex-review/SKILL.md`(IDS 仓无)· 之前 IDS session 误判为 user 全局 `~/.claude/` · 真路径 verify 后由 XenoDev 端做(项目级 SKILL · 跟 spec/risks 同性质 · 跨仓 by ownership)
  - audit trail 真闭环 path:IDS handback-id 004-pB-20260518T013000Z §4 FU-T022-followup-3 → IDS commit 651a25c LOG entry 12 → XenoDev commit 47d6c2a(.claude/skills/codex-review/SKILL.md §3.2 path B 改)→ IDS 本 maintenance commit append FU-3 status applied + cross-ref
  - **跟 0736d4a spec maintenance 同 audit pattern · 但性质不同**:0736d4a = hand-back §6 触发 cross-repo spec doc maintenance(产品维度);47d6c2a = hand-back §4 触发 cross-repo SKILL framework maintenance(framework 维度)· **两类 cross-repo follow-up 模式同 audit pattern 真稳态**
  - **plan v0.3-global §3 T2 candidate "v2.3+ FU 类型分类规范"evidence**:hand-back §4 backlog ID 应有 type 字段(spec-maintenance / skill-maintenance / arch-decision / polish)· 让未来 cross-repo follow-up 工作类型可统计

**Follow-up commits**:
- XenoDev commit `0736d4a`(spec maintenance · specs/004-pB/spec.md + risks.md · 3 处 · §6 cross-repo)
- XenoDev commit `47d6c2a`(skill maintenance · .claude/skills/codex-review/SKILL.md §3.2 path B 修 · §4 FU-T022-followup-3 cross-repo · operator 反对 adv 替代 review 路径)
- 跟 prior 11 包 pending 状态质变:T022 是第一个真出 2 个 cross-repo follow-up commit 的 hand-back · audit trail 模型双场景实证

## 2026-05-18T06:30:00Z · 004-pB-20260518T060000Z · DROP (validator hard-fail)

**Reviewed at**: 2026-05-18T06:30:00Z
**Status**: **DROP · 6 约束 hard-fail · 不入库 · 不读取内容**
**Validator (consumer-mode)**: ✗ FAIL · §6.2.1 约束 5 (id consistency check)
  - 真因:filename `004-pB-20260518T060000Z.md` 缺 ISO ts prefix · 期望 `<ISO ts>-<handback_id>.md` = `20260518T060000Z-004-pB-20260518T060000Z.md`
  - validator stderr: "cannot extract handback_id from 004-pB-20260518T060000Z.md (expected format: <ISO ts>-<handback_id>.md)"
  - 问题:hand-back 包 id 不一致 → corruption-of-corpus 失效模式

**Operator decision**: A 路径 · producer-fix · 通知 XenoDev re-emit handback(同 handback_id · 正确 filename · producer mv / rm 旧 malformed 文件 · IDS 不动)

**Why hard-fail 不绕过**:
- per SHARED-CONTRACT §6.2.1 约束 4 hard-fail 行为:consumer 不读取内容 · 不入库决议 · 只 stderr 报哪条约束失败 + handback_id · exit 非 0
- per CLAUDE.md "Iron rules" + memory feedback_push_confirmation 同性质 ground rule:silent fix(IDS mv 修 filename)= 偷改 audit trail = 跟 unauthorized push 同等级违 protocol
- 第一性原因:hand-back 通道跨仓写入 · filename 是 producer 写的物理证据 · IDS 改 = 破坏 audit 证据链 · 未来 dispute 无法追溯
- 真路径:producer 重写 handback(producer-fix loop)· 跟 prior 12 包 pattern 一致(producer 始终负责 filename + frontmatter id 一致)

**framework 维度观察(第一次 hard-fail 真触发)**:
- **6 约束 hard-fail 第一次真触发**(prior 12 包全 PASS):本 Drop 是 SHARED-CONTRACT §6.2.1 实战第一次真出 hard-fail · framework v2.2 hard-fail 设计**真有效** · 不是纸面规则 · 真阻断 corruption-of-corpus
- **producer 端 filename 生成 bug 真信号**:prior 12 包 filename 全 conformant · 第 13 包真出 bug · 可能 producer 端 gen-handback.sh / SKILL §6.4 路径有 regression(T010 hand-back §7 #7 早提过 gen-handback.sh grep brackets 类 bug · 跟 FU-producer-3 队列同集合 · 真 evidence)
- **plan v0.3-global §3 T2 candidate 真新加 evidence**:hand-back §4 backlog 应有 "producer-fix" type(跟 spec-maintenance / skill-maintenance / arch-decision / polish 并列)· 让未来 producer-fix loop 工作类型可统计
- **LOG schema 演化触发**:本 entry 是第一次 Drop entry · 跟 ship entry 结构不同:
  - 无 Operator decisions checkbox(包内容未读 · 不能做产品/spec 决议)
  - 无 framework 维度观察对包内容的解读(filename / frontmatter 已读 · 但 §2-§7 body 没读)
  - 只记 hard-fail 事实 + producer-fix 路径决议 + 反向引 producer re-emit commit(pending)
  - frontmatter 加 total_drops 字段(0→1)· 跟 total_decisions 并列统计
  - plan v0.3-global §3 T2 candidate "v2.3+ Drop entry schema" 新加 evidence
- **跟 T022 cap-escalation 重叠信号**:T022 已 6 round 超 SKILL §4.2 cap 4 · 本包 frontmatter 含 tag `cap-escalation` + severity high + codex 14 round(超 T022 又一倍)· 可能 codex review 长尾 pattern 在 T021 又一次显形 + 升级到 14 round 真深 · 真包内容入库后(producer-fix 后)再做 framework 维度评估
- **不算 ship 不算 task · 是 audit-trail event**:本 Drop 不影响 plan v0.2-global 件 3.1 阶段 2c 波数(T021 未真入库 · 波 8 候选 · 等 producer-fix 后真入)· 不进 ship gate · 不算 task · 是 audit-trail 事件

**Follow-up commits**:
- pending(待 XenoDev producer re-emit + IDS 重跑 /handback-review 004 真入库)
- 期望路径:XenoDev producer 端 mv 旧 malformed 文件 → 写正确 filename(20260518T060000Z-004-pB-20260518T060000Z.md · 同 handback_id · frontmatter 不动)→ commit `docs(handback): 004-pB T021 re-emit handback · filename 修正 ISO ts prefix(IDS validator hard-fail §6.2.1 约束 5 修响应)`→ IDS pull 后重跑 /handback-review 004 走 entry 14 真入库


## 2026-05-18T07:00:00Z · 004-pB-20260518T060000Z · ENTRY 14(producer-fix 后真入库)

**Reviewed at**: 2026-05-18T07:00:00Z
**Tags**: feature, codex-multi-round, cap-escalation, backlog-accepted, retroactive-spec-amend, schema-migration
**Severity**: **high(第一次真 high · 12 prior 中 11 low + 1 medium · T021 严重度真跳)**
**Validator (consumer-mode)**: ✓ all 6 constraints PASS · producer-fix 后真 PASS(entry 13 DROP precursor → producer-fix commit `8eceddc` mv filename → 本 entry 14 真入库 · audit trail 三步全闭环 第一次完整实证)
**Related task**: T021 Phase 2b 自动化咨询师监控收尾(ScheduledFetcher 真实装 + FailureLog + OracleAudit + fetcher_audit CLI + alembic 0011 复合 PK + 5 source placeholder · XenoDev squash commit `b17f2fa` + spec amend `6c52bab`)
**Operator decisions**:
- [ ] 修 PRD §"<section>"
- [ ] 修 SHARED-CONTRACT §"<section>"
- [x] 修 XenoDev spec(本仓内,信息式)— **§7 #1 立即起** · 跨仓 cd XenoDev 改 specs/004-pB/spec.md §6.1.1 O4 真意义补("per-source 唯一 week 覆盖 ≥ weeks"补字面 + 引 codex round 13/14 真发现)· 跟 T022 0736d4a precedent 同 pattern · 0.3h
- [x] 修 framework / SKILL — **producer SOP cp 路径错 root cause fix** · 跨仓 cd XenoDev 改 `.work/handback/` gen-handback.sh / SKILL §6.4 cp 命令模板(本 hand-back §194 行 producer 自报 cp 路径 `cp ... 004-pB-20260518T060000Z.md` 漏 ISO ts prefix 正是 hard-fail 真根因 · FU-producer-3 root cause)· 0.5-1h · 防未来再触发 hard-fail
- [x] 无操作(收悉)— §7 #2 alembic 0001 PK bug 跨 task verify 延 T025/T030 起时顺手 · §7 #4 lifespan wire 延 T030 wire 时同 T022 FU-2 一起处理 · FU-T021-followup-1 R-v022-4 mitigation 延 T040-B P1.B 真生产 soak 前决议 · FU-T021-followup-3 dry-run schema verify 低优先级 backlog

**Operator note**: T021 ship 接受 · v0.2 Phase 2b 自动化咨询师监控真上线(ScheduledFetcher 真实装 APScheduler integration + _fetch_one 真路径调 orchestrator 整链路 + FailureLog 顺序判定 missed_window_24h + OracleAudit 24h grace + late ingestion detect + fetcher_audit CLI 4 exit code + 5 source placeholder + sources_oracle.jsonl 5 expected content + alembic 0011 复合 PK 真生产 schema bug 修)。**TDD red→green 33+ test PASS · full suite 293 passed + 7 skipped + 1 xfailed**(baseline 264 + T021 ~30 - test_pipeline_fetcher.py test 2 替换 = 293 · 0 回归)· production_app_smoke 33/33 · routes 不变 · ruff clean · alembic 0010 + 0011 真路径 init OK · 复合 PK + UNIQUE INDEX 真保留 v0.1 row。**codex 14 round adversarial-review** 超 SKILL §4.2 cap 4 round 共 10 轮(operator decisions A x4 接受 cap escalation):23+ ship-blocking finding 真路径逐轮闭环(每轮真路径修真 P1/P2 bug · 真路径不属打转 · 跟 T022 6 round 长尾 pattern 升级版)· round 6 真发现 v0.1 alembic 0001 advisor_id PK 真生产 bug(INSERT OR REPLACE 覆盖历史周 · O4 4 周 audit 真路径必崩)· alembic 0011 真路径补 · round 7 P1 lifespan wire backlog accepted(同 T022 FU-2)· round 12 https-only 修 + dry-run schema verify 不修(mode 边界保持)· round 14 ship。§7 #1 立即起跨仓 spec maintenance(per-source 唯一 week 覆盖 ≥ weeks 字面补)+ producer SOP cp 路径错 root cause fix(防未来再触发 hard-fail) · §7 #2/#3/#4 延后续 task 顺手 / next wave 决议时处理。**🎉 plan v0.2-global 件 3.1 阶段 2c 波 8 闭环**:T010(d4d04e7) + 波 1 W1/W2(7eb8626/09f6cc1) + 波 2 T011(e0c2c48) + 波 3 T012(36eb012) + 波 4 T013(064d659 + 098f749) + 波 5 T040-A(f583654 + 2824d35) + 波 6 T020(8cb49e2 + a37c388) + 波 7 T022(f5e513e + cross-repo 0736d4a + 47d6c2a) + 波 8 T021(b17f2fa + 6c52bab + 待 cross-repo §7 #1 + producer SOP fix)= v0.2 Phase 2 全 4 + Phase 2b spine T020 + Phase 2b transcription T022 + Phase 2b fetcher T021 + Phase 3 partial T040-A 全 ship · 剩 T023 / T030 / T024 / T025 / T040-B 共 4-5 task ≈ 38-50h · v0.2 收官真近。

**framework 维度观察(本包真信号最重 · 4 个第一次)**:
- **第一次 severity=high 包**(prior 12 ship 中 11 low + 1 medium T022 · 严重度真跳):T021 升 high 真因 = codex 14 round / 23+ ship-blocking finding 闭环 + alembic 0011 真生产 schema bug 修 + 多处 retroactive amend + 1 backlog accepted ship · 这是 severity 维度第一次跳 high · plan v0.3 framework 升 candidate "severity 维度有效"实证连第 2 次(T022 medium · T021 high · severity 维度真分层)
- **第一次三步 audit trail 完整实证**(DROP → producer-fix → 真入库):
  - entry 13 DROP(2026-05-18T06:30:00Z · validator §6.2.1 约束 5 fail · IDS commit 44d0d5a)
  - producer-fix(XenoDev session 跑 mv + commit `8eceddc` · 同 handback_id · 正确 filename)
  - entry 14 真入库(本 entry · IDS validator PASS · 反引 entry 13 + producer-fix commit)
  - **SHARED-CONTRACT §6.2.1 hard-fail 设计真完整闭环**:不只是阻断 corruption · 还提供 producer-fix loop 真路径 · framework v2.2 实战首战 evidence
- **新 tag 累计 6 个 + 3 新 tag 本包出现**(v2.2 schema 演化 6 evidence):
  - 累计:partial-scope(T040-A) + spine-task(T020) + codex-multi-round(T022) + backlog-accepted(T022) + **cap-escalation(T021 第一次)** + **retroactive-spec-amend(T021 第一次)** + **schema-migration(T021 第一次)**
  - cap-escalation:T021 14 round 超 cap 10 轮 · operator decisions A x4 接受 · 真信号 = cap 不是死 limit · 是 operator 决议升级 trigger
  - retroactive-spec-amend:本包用 tag 显式标 retroactive 模式 · 跟 spec-gap-fix 同性质但更显式 · v0.3 framework normative 候选
  - schema-migration:alembic 0011 真生产 schema 改 · 是 schema 维度新 tag · 跟 spec-gap-fix 互补(spec gap fix doc · schema migration fix data 层)
  - **plan v0.3-global §3 T2 candidate "v2.3+ tags 规范集 normative" evidence 全到位**(6 个新 tag · 累 multi-axis schema)
- **codex adversarial-review ROI 第 6 次实证 + cap escalation pattern 第 1 次实证**:
  - 累计:T012 race / T013 prompt fallback / T040-A silent green / T020 R-v022-2 漏洞 / T022 6 round 长尾 / **T021 14 round + cap escalation + 23+ finding + schema migration 真生产 bug 发现**(第 6 次 · 第 1 次 cap escalation · 第 1 次真生产 schema bug 发现)
  - T021 round 6 真发现 v0.1 alembic 0001 advisor_id PK bug 是 codex review **真生产 schema bug 第一次发现**(prior 5 次都是 implementation bug · 这次是 v0.1 baseline 真生产 data 层 bug)· adversarial-review **ROI 已不只是 implementation 防 silent green** · 真扩到 v0.1 baseline schema 层
  - SKILL §4.2 cap 设计真路径实证:cap 不是死 limit · 是"超 cap 走 operator A/B/C 真有价值"的设计 trigger · T022 6 round + T021 14 round 双实证 · plan v0.3 framework 升 candidate "codex review derivation guide" cap escalation pattern 必入
- **producer 端 SOP / SKILL 缺陷真根因暴露**(framework 维护真触发):
  - hand-back §194 行 producer 自报 cp 路径 = `cp ... 004-pB-20260518T060000Z.md`(漏 ISO ts prefix · 跟 hard-fail filename 同一形 · 真根因)
  - **producer SOP 模板本身写错** · 不是手抖 · 是 SKILL §6.4 / gen-handback.sh 模板 bug · FU-producer-3 root cause 真发现
  - operator 决议 framework cross-repo fix · 防未来再触发 hard-fail · 跟 47d6c2a SKILL maintenance 同性质 · 第 3 次 framework maintenance commit candidate
- **跟 prior 12 包对比 evidence 跳级**:
  - 12 包累 framework 维度 evidence 集合:6 连发 spec-gap-fix · partial-scope · spine-task · codex-multi-round · backlog-accepted · cross-repo spec maintenance · cross-repo SKILL maintenance · adversarial-review ROI 5 次
  - **T021 一包加** 4 个第一次(severity high · 三步 audit trail · cap escalation · producer SOP 真根因)+ 3 新 tag · evidence 跳级到 plan v0.3 framework 升 candidate 真触发线以上(plan v0.3 candidate evidence 集合从 6 涨到 10+ 条)
- **G1 真触发 evidence 强化**:
  - T020 spine task(spec opus + 复杂度匹配)= G1 candidate
  - T024 XGBoost opus 12-16h = G1 候选 backlog
  - **T021 sonnet/codex 标准件 14 round 23+ finding alembic schema migration = 真复杂度比 G1 候选还重**(spec L16 suggested_executor_model: codex · 但真执行复杂度匹配 opus 重件)
  - plan v0.3 framework 升 G1 触发标准 candidate 真该考虑:"spec model 标 sonnet/codex 但 codex 14+ round + 真生产 schema bug 发现 = G1 实际触发"(spec 标 vs 实际复杂度差异)
  - 仍按 plan v0.3 path (c):operator 起 plan-rosy-naur v13 时正式决议(本 review 不动 plan)· evidence 集合到 plan v0.3-global §3 candidate
- **件 3.1 阶段 2c 波 8 闭环 + v0.2 收官真近**:T010+W1+W2+T011+T012+T013+T040-A+T020+T022+T021 = 10 ship(IDS 14 个 hand-back 包累计 + 1 Drop) · v0.2 Phase 2 全 4 + Phase 2b 三件(spine T020 + transcription T022 + fetcher T021)+ Phase 3 partial T040-A = v0.2 主体重件 + 自动化基础设施全 ship · 剩 T023 Telegram alert(sonnet 6-8h)+ T030 PPV multimodal e2e(sonnet 8-12h · 兼 T022 FU-2 + T021 FU-2 lifespan wire)+ T024 XGBoost(opus 12-16h · G1 候选)+ T025 冲突报告 UI(sonnet 6-8h)+ T040-B 完整 aggregate(sonnet 5-8h · 等 T030 done)· 共 4-5 task ≈ 38-50h · v0.2 收官真近

**Follow-up commits**:
- IDS DROP entry 13 precursor: commit `44d0d5a`(本 entry 14 反引 · 三步 audit trail 第一步)
- XenoDev producer-fix commit `8eceddc`(filename mv · 第二步 · 真在 IDS main · operator XenoDev session cd 进 IDS 改的特殊 case · pattern 跟 cross-repo 略不同)
- IDS 本 maintenance commit `318f200`(entry 14 入库 · audit trail 第三步 · 真闭环)
- XenoDev cross-repo maintenance commit `473dd6d`(docs(spec) · 004-pB T021 hand-back §7 #1 spec §6.1.1 O4 真意义补 · per-source 唯一 week 覆盖 ≥ weeks · 跟 0736d4a precedent 同 pattern · IDS spec maintenance 跨仓闭环第 2 次)
- XenoDev cross-repo maintenance commit `374f02b`(docs(skill) · parallel-builder SKILL §6.3 + §7 #10 加 anti-pattern · 防 hand-back §7 字面 cp 命令漏 ISO ts prefix · 真路径比 47d6c2a 更 generic 防御 · 跟 47d6c2a precedent 同性质但真路径 plan mode 决议加 anti-pattern 教 agent 不踩坑 · 不是模板替换 · IDS framework maintenance 跨仓闭环第 2 次)
- **三步 audit trail + 双 cross-repo maintenance 真完整闭环**:本 entry 14 累共 5 commit + 2 类 maintenance · 跟 T022 entry 12 (1 ship + 1 IDS + 2 cross-repo = 4 commit) 同 pattern 但本 entry 14 多 1 DROP precursor + 1 producer-fix · 是 hand-back §6.2.1 hard-fail loop 第一次完整 evidence
- **framework 维度真信号(本次 cross-ref 后强化)**:
  - XenoDev 端 framework maintenance 真路径 verify + plan mode 决议**改 anti-pattern 教 agent 不踩坑**(374f02b)· 不是粗暴改 cp 模板 · 是 parallel-builder SKILL §6.3 + §7 #10 加 anti-pattern 段 · 真路径思考深度 · 跟 operator 反对 "adv 替代 review" 同 framework 真路径 deepening(47d6c2a 同性质)
  - cross-repo maintenance 第 4 commit 累计(0736d4a + 47d6c2a + 473dd6d + 374f02b)· 累 2 类型 · 2 跨仓 task evidence(T022 + T021)· hand-back cross-repo maintenance 真稳态模型 · SHARED-CONTRACT §6.4.1 Step 5 闭环责任(IDS 异步段)真稳态实证
  - plan v0.3-global §3 T2 candidate "v2.3+ FU 类型分类规范" + "cross-repo maintenance pattern" 双 evidence 强化 · plan v0.3 framework 升真该启动 evidence 完整集

