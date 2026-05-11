---
doc_type: b2-2-retrospective
generated: 2026-05-11
b2_2_completion_date: 2026-05-11
operator: Yashu Liu
based_on:
  - /Users/admin/codes/XenoDev/specs/006a-pM/B2-2-RETROSPECTIVE-DRAFT.md(XenoDev session 草稿,206 行)
  - /Users/admin/codes/XenoDev/specs/006a-pM/friction-report.md(self-test 5 friction)
  - discussion/006/handback/HANDBACK-LOG.md(IDS /handback-review 决议 5 包)
  - 4 轮 codex adversarial-review(round 2/3/4/5)累积安全加固
status: draft-for-operator-review
---

# B2.2 retrospective · 首个真 PRD ship + hand-back 闭环验证

> **plan rosy-naur v11 Block G 产物**。基于 XenoDev session 草稿 + IDS /handback-review 实跑数据合并。
> **operator 责任**:看完后改/补 §3 决策 + §4 自由 retro,然后落 commit 触发 §6 Status: ACTIVE 或 forge v3。

---

## §0 · B2.2 全 Block 完成度回顾

| Block | 状态 | 实证 | IDS commit |
|---|---|---|---|
| A · dry-run + 修 friction | ✅ | 6 friction 全修(b2.1-dry-run 跑通)| `dc757f4..463d55b` |
| A.5 · codex round 2 三 finding 修 + 1 park | ✅ | `b34686e..10774b4` + park decision | `cfcd6d3` |
| A.6 · codex round 3 三 finding 修 | ✅ | force-push bypass + identity fail-closed + pre-commit hook | `055509f..be5bafd` |
| A.7 · codex round 4 四 finding 修 | ✅ | 凭据 skip 精确 + force-push 全变体 + marker 强度 + 件 3 文字降级 | `495461a..d80ea1f` |
| A(round 5 决策)| ✅ 0 修 | 3 finding all OQ-v0.2 · solo dev local · CODEX-REVIEW-ROUND5.md | `423dcbd` |
| B · operator 手补 PRD | ✅ | 006a-pM PRD-v0(operator 接受初稿 + 平铺命名)| `4341072` |
| C · HANDOFF + bootstrap | ✅ | plan-start v3.0 产 L4/HANDOFF.md(§6.5 13 项 + 6 约束)| `17fa525` + XenoDev `bc7559f` |
| D · XenoDev L4 skill 派生 | ✅ 超额 | spec-writer 12KB + task-decomposer 9KB + parallel-builder 25KB | XenoDev `0e85476` + `351e51f` |
| D · D3 IDS-side patch 应用 | ✅ | derivation-guide 加 N=1 实证 + 边界声明 | `3c534d0` |
| D · F3 bootstrap-kit mirror | ✅ | bootstrap.sh Step 6.5 + sha256 校验 + MIRROR-PROVENANCE | `e29eb0f` |
| E · parallel-builder ship | ✅ 超额(3 ship) | FU-001 + T001 + FU-002 全入 XenoDev main | XenoDev `5af78f6` + `45e54fd` + `d8c903a` |
| F · hand-back 闭环 | ✅ | 5 包真写回 + /handback-review 真跑 + HANDBACK-LOG 决议 + 1 IDS validator fix | `73d0655` + `a57972a` |
| G · 评分 + Status 决策 | **本文件** | — | — |

**IDS 端 B2.2 commit 数**:**~30 commit**(plan v11 估 3-8;实际超额由 codex round 2-5 加固 + Block D-F 跨仓 follow-up 拉高)

**XenoDev 端 commit 数**:**12 commit**(bootstrap → 3 skill → spec frozen → 全 12+3 task spec → 3 task ship → FU-001/002 + 1 doc log)

**5 个 hand-back 包**(round-trip 实证):
- `20260510T123126Z-006a-pM-*.md`(self-test low,round 1 草稿)
- `20260510T123452Z-006a-pM-*.md`(self-test low,round 5 producer fix 后 — 6 约束全 PASS)
- `20260511T000000Z-006a-pM-*.md`(FU-001 drift high,hook JSON escape + here-doc fix)
- `20260511T001000Z-006a-pM-*.md`(T001 spec-gap medium,dangerous-24 fixture ship)
- `20260511T020000Z-006a-pM-*.md`(FU-002 drift/spec-gap-fix high,hook patterns 24→18 加固 + known-limit)

---

## §1 · playbook deviation 清单(operator 严肃记录,不掩盖)

per XenoDev RETRO 草稿 §1 全文(`/Users/admin/codes/XenoDev/specs/006a-pM/B2-2-RETROSPECTIVE-DRAFT.md` L29-118),保留原文 6 项 deviation。简要复述 + 我端评估:

### 1.1 deviation: Step 4 字面跑 `/task-review` 未执行 — 用 codex adversarial-review 替代

- playbook L155 字面要求 `/task-review verdict ≠ BLOCK`,但 `/task-review` slash command 在 IDS 仓,XenoDev 仓无 `.claude/commands/` 目录
- 实际跑:`parallel-builder` SKILL §3.1 强制的 `node $CODEX_MJS adversarial-review`(FU-001 6 轮 / T001 5 轮 / FU-002 2 轮)
- **实质同效**(cross-model + verdict-gate + 失败回 fix);命名差异
- **RETRO 决议(operator 拍)**:**选 A · 声明 codex adversarial-review 是 `/task-review` 的 cross-model 等价物**。playbook v2 应在 Step 1.5 补"派生 task-review command 到 XenoDev/.claude/commands/"或显式写等价物注

### 1.2 deviation: parallel-builder SKILL §6.4 `.eval/events.jsonl` 三个 ship 全没写

- SKILL §6.4 + §9 checklist 第 12 项要求每 task ship 写一行 event
- 3 个 ship 全跳了 — events.jsonl 是纯 side-effect(不阻 ship gate)
- producer/consumer validate 是 fail-closed → 都 PASS;side-effect step → 全漏 → **agent 默认轻视 audit step**
- **严重度**:中-高 — 影响 spec O3 outcome(append-only event log)实证
- **RETRO 决议**:PHASE 1 起跑前 backfill 这 3 条;PHASE 1-3 所有 task ship 必跑 §6.4

### 1.3 deviation: SKILL §4.3 merge 命令偏离 — 用 `git checkout` 替代 `git merge --squash`

- 技术等价,git history 不显示分支合并轨迹
- **严重度**:低
- **RETRO 决议**:PHASE 1 起跑前确认用字面 `git merge --squash`

### 1.4 deviation: SKILL §4.4 pre-merge verifier 未机器化

- §4.4 6 项 check(commit 拓扑 / red-green log / diff 边界 / framework 写保护 / commit prefix / 内容)是手工 grep + 肉眼判
- **严重度**:中 — 人工易漏,影响 PHASE 1-3 可扩展性
- **RETRO 决议**:PHASE 1 起跑前实装 `XenoDev/lib/parallel-builder/verifier.sh`

### 1.5 deviation: SKILL §0.2 Safety Floor preflight 未独立显式跑

- §0.2 要求每 task ship 前 `test -x` + 实地 scan 三件套;本 batch 直接进 §1
- 三件套实际就位(FU-001/FU-002 改 hook 时实测过)
- **严重度**:低-中
- **RETRO 决议**:PHASE 1 起跑前在 SKILL §0.2 实装 `preflight-safety-floor.sh`

### 1.6 deviation(spec 授权,不算违规): FU-001 + FU-002 跳 worktree

- SKILL §1 + §7 "Anti-pattern 1" 字面禁直接 main impl
- FU-001/FU-002 spec 显式授权直接 main(单文件 hook fix + operator 临时 settings.json 加 Edit 权限)
- **严重度**:0(spec + plan 双文档化)
- **RETRO 决议**:SKILL §1 + §7 加"单文件 hook fix + spec 显式授权"exception 白名单

### 1.7 deviation(IDS 端 · 新增): handback-validator check-5 regex false-positive

- IDS /handback-review 跑包 2(123452Z)相对路径时 check-5 FAIL(规则 5 path discussion_id 提取);绝对路径 PASS
- **根因**:`framework/xenodev-bootstrap-kit/handback-validator/check-5-id-consistency.sh` line 31 sed regex 要求 `/discussion/` 前必有 `/`
- **严重度**:中(评分 #4 false-positive 直接扣分)
- **RETRO 决议**:✅ 已 fix(commit `a57972a`);regex 改为 `^(.*/)?discussion/([^/]+)/handback/.*` 同时接受相对+绝对路径;无 regression

---

## §2 · 5 维度评分(operator 主观给,1-10)

> evidence 段保留草稿 + 我 /handback-review 实跑补充。**operator 在最后落分前请改 §X/10 的具体数字**。

| # | 维度 | 评分 | evidence |
|---|---|---|---|
| 1 | hand-back 包格式 operator 可读可消费 | **8**/10 | 5 包均含 §1 结论 + §2 commit hash + §3 影响范围 + §4 ship 历程 + §5 known follow-up + §6 IDS action + §7 设计实证;包 5(FU-002)的"known limit + 设计认知再印证"段是关键交付,reviewer / IDS 端不会误判 0 漏。**扣分项**:packs 1 / 3 / 4 / 5 producer drift(remote 空)需 cross-repo follow-up |
| 2 | 6 约束 validator 错误信息清楚 | **8**/10 | 跑 5 包真出 fail 信息:`actual remote: ...` + `hint:producer 应填...`;check-5 false-positive 信息也直接定位"cannot extract from path ...";FU-001 round 1-6 validator 跑出 hook JSON escape 真问题 — 信息有指向性。**扣分项**:错误信息无 fix suggestion 行(operator 仍需读 §6.2.1 原文判断改哪边) |
| 3 | workspace + source_repo_identity 在跨仓 friction | **7**/10 | playbook L267-268 跨仓边界守住(XenoDev session 未直写 IDS);5 包 ln 入 IDS dir 全成功 + handback_target containment 6 约束 PASS。**扣分项**:producer 多入口 drift — round 5 修了 PPV self-test producer 但 ship-side parallel-builder producer 未继承 → 4 包 remote 空 → cross-repo FU-producer-1 跟进 |
| 4 | §6.2.1 6 约束在真数据无 false positive / false negative | **7**/10 | 5 包真数据:1 false positive(check-5 相对路径 → 已 fix · commit `a57972a`)+ 0 false negative · 4 真 fail(producer drift 是真问题)。**扣分项**:check-5 false-positive 暴露 fixture/relative-path 测试覆盖不足(test-fixtures/valid 路径不含 discussion/<X>/handback/ 段,fix 前后均 FAIL — fixture 设计 v0.2 重构 OQ) |
| 5 | hand-off → ship → hand-back 闭环符合 operator 预期 | **8**/10 | XenoDev 端:bootstrap 9 step + skill 派生 + spec frozen + 12+3 task + 3 ship + 5 包真到 IDS(全过)。IDS 端:plan-start v3.0 产 HANDOFF + /handback-review 真跑 5 包 + HANDBACK-LOG append-only + validator real-data fix 真触发。**扣分项**:1.2-1.5 共 4 项 SKILL §4 / §6 audit step deviation(events.jsonl / merge / verifier / preflight)— 闭环跑通但**字面合规度有 gap**;PHASE 1 backfill 后期补 |

**总分**:**38**/50 · **平均 7.6**/10

---

## §3 · 决策

per plan rosy-naur v11 Block G L226-227:

- 平均 **≥ 7/10** → **起 cutover sealing commit**(framework/SHARED-CONTRACT.md §6 Status: ACTIVE-but-not-battle-tested → ACTIVE)
- 平均 < 7/10 → 起 forge v3 plan,本 plan 标 PARTIAL

**本次评分 7.6/10 → 走 ACTIVE 路径**

cutover sealing commit 内容(待 operator 确认后我落):
- `framework/SHARED-CONTRACT.md` §6 顶部 `Status: ACTIVE-but-not-battle-tested` → `Status: ACTIVE`
- §6 顶部 `Promotion to ACTIVE pending` 段 → `Promoted to ACTIVE: B2.2 commit <hash> · 2026-05-11 · operator score 7.6/10 (38/50)`
- frontmatter `v2_status_note` 删除
- Changelog 加 `2026-05-11 v2.0 ACTIVE: B2.2 score 7.6/10 verified hand-back round-trip on 1 real PRD ship (006a-pM · 3 ship + 5 hand-back packs · 4 codex round adversarial 加固)`

**OQ + 后续 v0.2 trigger 入队**(本 plan cutover 不阻;v0.2 时由后续 forge / sub-plan 处置):
- FU-producer-1(XenoDev):producer 多入口 remote 字段统一 contract
- FU-003(XenoDev,已 spec'd · 5h opus risk_level high):hook 重设计 hybrid shlex token + regex fallback(8 真 bypass 全 deny)
- IDS test-fixtures 重构(check-5 valid fixture 路径不含 discussion/<X>/handback/)
- playbook v2:Step 1.5 补 task-review command 派生注 + Step 4 SKILL §6.4 events.jsonl 标 hard-gate
- SHARED-CONTRACT §6 加"Step 5 闭环责任分担"段(XenoDev 写到 cp + validator PASS 即闭环,IDS 决议是异步独立 step)

---

## §4 · 自由 retrospective(operator 补)

### 4.1 顺当之处

- **三 SKILL 派生(46KB)非 stub** — XenoDev session 在 Block D 自派生 spec-writer 12KB + task-decomposer 9KB + parallel-builder 25KB,真用真跑;Block D 设计目标(adapter 模式,非 IDS port)达成
- **Safety Floor 件 2 经 FU-001 + FU-002 双轮加固有量化承诺支撑** — 从 7/24 输出 invalid JSON → 43 真 bypass 实证拦下;codex adversarial-review 6+5+2 轮 trend 真暴露 bug,**未放水**
- **codex adversarial-review 6 轮模型对项目质量真有效** — round 1-5 100% finding actionable(N=1 实证已落 derivation-guide);round 5 操作 threat model 澄清(`CODEX-REVIEW-ROUND5.md`)
- **跨仓边界守住** — XenoDev session 0 次直写 IDS framework/;5 包 hand-back 用 ln + cp 跨仓写入,playbook L267-268 设计有效
- **append-only HANDBACK-LOG 范式落地** — 5 包决议有 audit trail,符合 §6.4 schema

### 4.2 不顺之处

- **playbook 与 SKILL 镜像差** — playbook 在 IDS,SKILL 在 XenoDev,中间桥是 CLAUDE.md 浓缩条款。XenoDev session **全程没看 playbook**(L162-184 实证),靠 CLAUDE.md + SKILL 跑通 — 跑通 ≠ 字面合规(产生 §1.1-1.5 共 5 项 deviation)
- **non-blocking audit step 易被 agent 忽略** — events.jsonl / merge 字面命令 / verifier 机器化 / preflight 显式跑 4 项全漏。producer/consumer validate(fail-closed)0 漏;side-effect step 全漏。**hard-block 反馈 vs 纯 side-effect 反馈** 在 agent 行为上有质的差
- **producer 多入口 drift 未自检** — XenoDev round 5 修了 PPV self-test producer 但 ship-side parallel-builder producer 是不同 codepath,未继承修复;直到 IDS /handback-review 5 包扫一遍才暴露。**single producer source 是 contract** 在 XenoDev 内未落 SKILL 强约束
- **Step 5 IDS 端依赖 operator 切 session,异步** — XenoDev 单跑不能闭环;闭环要求 operator 手工切仓 + 跑 /handback-review。**本次跨度 2026-05-10 → 2026-05-11(~24h)** 才闭环
- **plan v11 估 commit 数(IDS 3-8)与实际(~30)严重低估** — codex round 2-5 加固 + 跨仓 follow-up 双拉高;v0.2 plan 估算需修正

### 4.3 给 IDS 框架的反馈(F1-F5)

per XenoDev RETRO 草稿 §4.3 F1-F4 全收 + 新增 F5:

- **F1**(playbook v2 in scope · v0.2):Step 1.5 显式加"派生 task-review command 到 XenoDev"或写"XenoDev 用 codex adversarial-review 等价 IDS /task-review"
- **F2**(SHARED-CONTRACT §6 in scope · v0.2):加"Step 5 闭环责任分担"段 — 明确 XenoDev session 写到 cp + validator PASS 即闭环,IDS session 决议是异步独立 step
- **F3**(本次 B2.2 cutover 已支撑):`lib/handback-validator/` 6 约束在 5 真数据上 1 false positive(已 fix)+ 0 false negative → 足以支撑 SHARED-CONTRACT v2 Status: ACTIVE
- **F4**(parallel-builder SKILL §9 in scope · v0.2):checklist 区分 [GATE] / [AUDIT] 前缀,AUDIT 项注明"若漏,PHASE 末 operator 自审必 backfill",或把 events.jsonl 写入失败设为 hard-fail
- **F5**(新增 · IDS test-fixtures in scope · v0.2):handback-validator/test-fixtures/valid/ 路径不含 discussion/<X>/handback/ 段,fix 前后均 FAIL — 重构 fixture 路径模拟真 dir 结构

---

## §5 · cutover sealing commit 前置 + 执行清单

**前置**(operator 在改 §3 决策前确认):
- [ ] §2 5 维度评分各项数字是否同意(目前我建议 8/8/7/7/8 = 38)
- [ ] §3 决策 ACTIVE 是否同意(目前 7.6/10 > 7 → 默认 ACTIVE)
- [ ] §4 自由 retro 是否补充
- [ ] §4.3 F1-F5 是否同意(全部 v0.2 trigger,不阻本 cutover)

**cutover commit 执行**(operator 确认后我落):
1. Edit `framework/SHARED-CONTRACT.md` §6 顶部 Status 行
2. Edit §6 顶部 Promotion 段
3. Edit frontmatter 删 `v2_status_note`
4. Edit Changelog 加 v2.0 ACTIVE entry
5. 1 个 commit:`feat(framework)!: SHARED-CONTRACT v2.0 Status: ACTIVE — B2.2 hand-back round-trip verified (score 7.6/10, B2.2 Block G)`
6. `/status 006` 跑一次 verify

**若 operator 改评分到 < 7/10**:
- 改 §3 决策段,起 `/expert-forge 006` plan
- 本 plan 标 PARTIAL,B2.2 sub-plan 暂停
- 不动 SHARED-CONTRACT

---

## §6 · 与 plan rosy-naur v11 的对账

| plan v11 完成标志 | 本 RETRO 实证 |
|---|---|
| `discussion/006/b2-2/PRD-v0/PRD.md` 存在 | ✅ commit `4341072` |
| `discussion/006/b2-2/PRD-v0/L4/HANDOFF.md` 存在 | ✅ commit `17fa525` |
| `ls discussion/006/handback/*.md \| grep -v HANDBACK-LOG.md \| wc -l` ≥ 1 | ✅ 5 包(超额 4) |
| `discussion/006/handback/HANDBACK-LOG.md` 存在 | ✅ commit `a57972a`(5 包决议) |
| `discussion/006/b2-2/B2-2-RETROSPECTIVE.md` 存在 | ✅ 本文件 |
| 若 ≥ 7/10:`grep -q 'Status..*ACTIVE$' framework/SHARED-CONTRACT.md` | ⏳ pending cutover commit |
| 若 ≥ 7/10:`grep -q 'v2.0 ACTIVE' framework/SHARED-CONTRACT.md` Changelog | ⏳ pending cutover commit |
| git log 应看到 3-8 个 B2.2 commit(plan 估) | ⚠ ~30 commit(超额由 codex round 2-5 加固 + 跨仓 follow-up 拉高)|

---

## §7 · 与总路线图 v8 的对账

| 总路线图 v8 件 | 状态 |
|---|---|
| M3 · 4 fork specs/ DEPRECATED | ✅ commit `d3194a0` |
| M2 · SHARED-CONTRACT v1.1.0 → v2.0 cutover | ✅ 7 commit `850dd8f` → `bda80f1` |
| B2.1 · XenoDev bootstrap-kit + spec-kit-evaluation | ✅ 7 commit `dc757f4` → `56145ef` |
| **B2.2 · 首个真 PRD ship + hand-back 闭环** | **✅ 本 RETRO 完成,cutover pending operator 确认** |

**B2.2 完成 = 总路线图 v8 完成。**

cutover 后:
- SHARED-CONTRACT v2.0 真正 production-ready
- v0.2 触发器:≥3 真 idea / ≥30 task / Spec Kit fork 边界 / etc(本 RETRO §4.3 F1-F5 全部入 v0.2 队列)
