---
doc_type: handback-decision-log
first_created: 2026-05-12T03:31:30Z
last_updated: 2026-05-12T11:25:30Z
total_decisions: 6
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
