# Forge Stage · 006 · v3 · "Bootstrap kit v0.2 反向同步 + 协议 4 项修订 + lib bug 清班"

**Generated**: 2026-05-27T13:35:00Z
**Source**: forge run v3 with X = 13 标的 / 9 槽位, Y = 架构设计 + 工程纪律 + Y5 重做代价/沉没成本/知识保留, Z = 不对标 · 纯内部审阅
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both), P2 (both), P3R1 (both), P3R2 (both)
**Searches run**: 0(Z mode = 不对标 · 跳 Phase 2 web search)
**Moderator injections honored**: none(`moderator-notes.md` 不存在)
**Convergence outcome**: converged(3/3 分歧 closed · 1 v0.2-note B-3 IDS dir flock · 0 unresolved)

---

## How to read this

forge 是横切层(不是 L1-L4 pipeline 的一部分)。本文档是双专家审阅(Opus 4.7
+ GPT-5.5 xhigh)在 v3 fresh intake 后,对 v0.1 ship 已落地的 **11 项 backlog
三类** 的强收敛产出。**v3 mission 与 v2 verdict 大架构无关** — 不重审 IDS=治理
/ XenoDev=唯一 L4 / 双向 hand-off,只动落地后的协议 + lib + mirror 细节。

读完后你应该:

- 知道 11 项 backlog 一一对一的最终 verdict(N×9 / R×6 / cut-to-note×1,见 §"Decision matrix")
- 知道支持每条结论的具体证据(§"Evidence map" 可逐条溯源到 HANDBACK-LOG ENTRY 7-17 / v2 stage / 4 SKILL 真路径)
- 拿到按 W 全 6 形态准备好的可执行草案:verdict / 决策矩阵 / 3 wave refactor / dev plan / v0.2 PRD draft / 跨 backlog free essay
- 能基于 §"Decision menu" 直接进入下一步(进 L4 fork PRD / 跑 forge v4 / 局部接受 / park / abandon)

## Verdict

**v0.2 = 11 项 backlog 三类 batch ship · 3 wave 顺序 · 每 wave 1 IDS commit + MANIFEST-v0.2.md append**。

- **wave 1 (P0 hard-block)**:mirror cp `handback-validator/{templates,gen-handback,score-handback}`(producer 入口硬依赖)+ 修 C-1 scan-credentials exit code & 14 false positive + 修 C-3 FU-producer-1 case F regression + 协议 B-2 event-schema enum 全复数统一。
- **wave 2 (P1 + 协议改)**:mirror cp skills/ 4 SKILL + hooks/wrappers + tests/integration 8 sh(**文件级 only**)+ 协议 B-1 Cross-device publish 段 + B-4-IDS verdict-evidence 协议语义 + 修 C-2 `--out` 默认前缀。
- **wave 3 (bootstrap 真路径联调)**:`bootstrap.sh` 升级读新子树 + 临时 test fixture idea bootstrap + `verify-all-outcomes.sh` SHIP-READY exit 0。

**v0.2 ship 关闭判据**:wave 3 verify-all SHIP-READY + MANIFEST 三波完整 + B-3 IDS dir flock 在 SHARED-CONTRACT changelog 记 v0.2-note(K11 合规旁注 · 非压扁分歧)+ B-4-XenoDev runtime implementation 在 XenoDev 单独 task ship 并 hand-back 返 IDS。

此 verdict 直接回应 K8(v3 mission 11 项三类)+ K9(v2 verdict 不重审,IDS/XenoDev 双仓边界保持)+ K10(每 wave 锁子树边界 + manifest + SHA + bootstrap verify)+ K11(strong-converge · 10/11 项硬收敛 + 1 项 v0.2-note 旁注)。

## Evidence map

| 结论 | 来源 | 引用 ≤15 words | 反对证据 |
|---|---|---|---|
| wave 1 = templates/gen/score mirror P0 硬阻 | P1-Opus §2 Cluster A-7/A-8 + P1-GPT §2 row 6 | "gen 不能跑 = 硬阻"/"producer 入口硬依赖" | - |
| C-1 scan-credentials = P0 | P1-Opus §1 Y2 + P1-GPT §1 视角 B | "Safety Floor 件 1 真聚合"/"误报会拖慢全链" | - |
| C-3 case F stale = P0 真 regression | P1-Opus §1 Y2 + P1-GPT §1 视角 B | "main 14/15 fail 真 regression" | ⚠ R2 期望收敛根因(删 case vs escape 修)— 见 §"What this menu underweights" |
| B-2 enum 全复数 = P0 | P2-Opus §3.2 Cluster B + P2-GPT §3.2 row 8 | "5 文件 grep 一致 · 5 分钟修" | - |
| B-1 Cross-device publish 协议段 = P1 | P2-GPT §3.1 反驳 + P2-Opus §3.2 接受 | "EXDEV fallback 已实装,协议未写" | Opus P1 初评 P2(已让步) |
| B-3 IDS dir flock = v0.2-note | P2-Opus §3.2 + P2-GPT §3.2 row 9 | "并发未实证 · fail-closed cleanup 足够" | Codex P1 初评 P1(已让步) |
| B-4 拆 IDS 协议改 + XenoDev 实装 | P3R1-Opus §3 D2 + P3R1-GPT §3 D2 接受 | "v3 stage doc 可给约束,不能越界实现" | - |
| 分波 + manifest + SHA dual-verify | P3R1-Opus §2 + P3R1-GPT §2 + P2-GPT §3.1 | "分波执行 + 每波 manifest + SHA dual-verify" | - |
| MANIFEST 入 `bootstrap-kit/MANIFEST-v0.2.md` | P3R1-GPT §3 D3 + P3R2-Opus §1 D3 接受 | "同目录即 SSOT 边界内 · 消费者拿到完整 provenance" | - |
| tests wave 2 cp / wave 3 联调 | P3R1-Opus §3 D1 折中 + P3R1-GPT §3 D1 接受 | "cp 边界和真路径验证边界拆开" | - |
| bootstrap.sh 升级归 IDS bootstrap-kit | P3R1-GPT §3 D3 + P3R2-Opus §1 D3 | "IDS 是 SSOT owner · XenoDev 只消费" | - |
| Cluster A skills+hooks+tests 全 N(new) | P1-Opus §2 Cluster A row 1-6 + P1-GPT §2 row 1-5 | "mirror 缺 skills,真路径合同在 XenoDev" | - |
| K11 残余 1 项 v0.2-note 合规 | P3R1-Opus §4 K11 自检 + P3R1-GPT §4 K11 | "残余分歧 v0.2-note 旁注 显式允许" | - |
| v2 verdict 不重审 | 双方 P1 §0 K9 binding + P3R2-Opus §2 verdict | "v3 不动这个大架构,只动落地后细节" | - |

## Intake recap

### X · 审阅标的(13 个文件 / 9 大槽位)

- 槽位 1:`discussion/006/forge/v2/stage-forge-006-v2.md`(stage-doc / baseline · 不重审)
- 槽位 2:`discussion/006/handback/HANDBACK-LOG.md`(17 ENTRY · batch 2 = v3 主线锚)
- 槽位 3:`framework/SHARED-CONTRACT.md` v2.2(协议层 · 4 项修订源)
- 槽位 4:`framework/xenodev-bootstrap-kit/` 整子树(IDS mirror 现状)
- 槽位 5-7:XenoDev SSOT skills(parallel-builder / spec-writer / codex-review)
- 槽位 8:XenoDev SSOT `hooks/wrappers/dangerous-event-emit.sh`
- 槽位 9:XenoDev SSOT `tests/integration/` 8 sh
- 槽位 10-12:XenoDev SSOT handback-validator(templates / gen / score)
- 槽位 13:`/Users/admin/codes/XenoDev/lib/eval-event-log/event-schema.json`(operator override · B-2 原文)

### Y · 审阅视角

- 架构设计
- 工程纪律
- Y5 重做代价 / 沉没成本 / 知识保留(operator 自定义 · K10 边界纪律核心 axis)

### Z · 参照系

- mode: 不对标 · 纯内部审阅
- 用户外部材料: 无

### W · 产出形态(6 · 全)

- verdict-only
- decision-list
- refactor-plan
- next-dev-plan
- next-PRD
- free-essay

### K · 用户判准(verbatim)

```
// from "想法":
给定一个PRD,claude code可以几乎没有人工干预的情况下自主完成开发任务。
我需要一个**可靠的、自动化程度最高**解决方案。

// from "我为什么想做这个":
我是非软件开发背景。我可以将需求描述清楚,我也可以尝试构建较可靠的PRD。
但是我缺少软件开发的经验,对各个规模(大中小型)的开发的方案、流程、规范等内容都没有把握。

// from "我已经想过的角度":
1. idea_gamma2(数字基建 + phase + pipeline skill + retrospective + subagent + skills)
2. vibe-workflow(engineer team 协作 + 自动化开发)
3. autodev_pipe(vibe coding + agentic coding + agent-skills + superpowers)
4. 当前 repo(idea→PRD→自动开发)

// from "我诉求":
基于 Claude Code 实现**可靠**自动化开发的 framework/pipeline 的共识方案

// === v3 specific additions(operator append 2026-05-27)===

K8(v3 mission · binding):v3 mission = "Bootstrap kit v0.2 反向同步、带上协议
修订 + lib bug 清班"。v0.1(006a-pM)已 ship 封箱;v3 不重审 idea / 不重审 v2
verdict 主线,只在 v2 verdict 落地后的真路径 backlog 三类上收敛:
  (a) mirror rebuild 4 子树
  (b) 协议级修订 4 项
  (c) XenoDev 本仓 lib bug 3 项

K9(v2 verdict 继承 · 不重审):v2 已收敛"IDS=idea→PRD + 治理 / XenoDev=唯一
L4 runtime / 双向 hand-off"= v3 不动这个大架构。

K10(operator 偏好):Cluster A 选项 1 已实证 — 单 ENTRY 7/9/13 三连 cp + 不越
mirror 边界;v3 应延续"边界先定、批量 SSOT、不越界"纪律。

K11(v3 收敛模式偏好):strong-converge — 11 项 backlog 一一对一收敛产 verdict,
不允许"双方都对"式压扁,残余分歧用 v0.2-note 旁注。
```

### 收敛模式

strong-converge(K11 binding · 与 v2 同档 · converged outcome)

---

## §W1 · Verdict rationale(展开 ≤500 字)

v3 的收敛基本盘极稳:双方 P1 / P2 / P3R1 共 6 个独立审阅,**0 推翻**,3 个分歧
全部在 R2 closed,K8/K9/K10/K11 自检全 ✅。能这么快收敛的根因是 v2 verdict
继承(K9 binding)+ K8 提前锁定 11 项 backlog 三类作为本 forge 的全部 surface
area — 这意味着双方没有重开架构辩论的空间,只在"哪一波 cp、协议改怎么写、
manifest 放哪里"上做工程纪律级的精修。

**3 wave 不是任意切割,而是按依赖图自然分层**:wave 1 是 producer 入口硬阻
(gen-handback 不能跑 = bootstrap 不能 ship)+ 真路径 P0 bug(scan exit code、
case F regression)+ 5 分钟可修的 enum corruption 风险。wave 2 是 SSOT 教学
+ 协议补段(producer 已实装但协议 lag)+ 不阻塞的 UX bug。wave 3 才是真路径
联调 — bootstrap.sh 升级 + 用临时 fixture idea 跑 verify-all。**关键纪律 = wave 2
cp 通过不等于 ship-ready**(Codex P3R1 §3 D1 提议、Opus R2 接受的硬规则)。

**双仓边界(K9)在 B-4 上得到最严的捍卫**:B-4 verdict-evidence flag 被拆成
B-4-IDS(协议改 · v3 IDS commit)+ B-4-XenoDev(runtime 实装 · XenoDev 单独
task · hand-back 返 IDS)。这条拆分等于把"v3 forge stage doc 给 XenoDev task
约束,但不能越界替它实现"作为 hard rule 写进 verdict。

**B-3 IDS dir flock 降 v0.2-note 是 K10 / K11 双重达标的范例** — 不假装解决
(K11 §"残余分歧 v0.2-note 旁注"显式允许),不向 v0.3 范畴扩张(K10 边界先定),
触发条件显式列出(任一 XenoDev session 报 race 或 operator 实证 corruption)。

---

## §W2 · Decision matrix(11 项 backlog 一一对一)

| 类别 | 项 | 来源 | 理由 | 优先级 |
|---|---|---|---|---|
| **保留** | IDS=治理 / XenoDev=唯一 L4 / 双向 hand-off 大架构 | v2 verdict | K9 binding · v3 不重审 | P0 |
| **保留** | SHARED-CONTRACT §6 6 约束 + workspace 4 字段 + hand-back schema | SHARED-CONTRACT v2.2 | 已 ACTIVE · 修订不动核心 | P0 |
| **保留** | hand-back v2.2 producer 真路径 7 节 body schema | HANDBACK-LOG batch 2 §5 | 11 包 PASS · 0 false positive | P0 |
| **保留** | adversarial codex review precedent(ship-blocker) | HANDBACK-LOG ENTRY 13 A5 | T007/T012 4-round 真路径 | P0 |
| **新增** | A-7 `handback-validator/templates/handback.template.md` mirror | wave 1 · P1-Opus §2 A-7 | gen 必依赖 · 硬阻 | P0 |
| **新增** | A-8 `handback-validator/gen-handback.sh` mirror | wave 1 · P1-Opus §2 A-8 | 495 行 producer 入口 | P0 |
| **新增** | A-9 `handback-validator/score-handback.sh` mirror | wave 1 · P1-Opus §2 A-9 | 229 行 operator 真路径 | P0 |
| **调整** | B-2 `event-schema.json` enum 全复数统一 | wave 1 · ENTRY 15/16 A2 | 5 文件 grep 一致 · 5 分钟修 | P0 |
| **调整** | C-1 `scan-credentials.sh` exit code + 14 false positive | wave 1 · ENTRY 8 A1 | Safety Floor 件 1 真聚合 | P0 |
| **调整** | C-3 FU-producer-1 case F regression(score escape 真路径) | wave 1 · ENTRY 16 A4 | main 14/15 fail 真 regression | P0 |
| **新增** | A-1 `skills/parallel-builder/SKILL.md` mirror(553 行) | wave 2 · P1-Opus §2 A-1 | ship 流程 SSOT 不可 stale | P1 |
| **新增** | A-2 `skills/spec-writer/SKILL.md` mirror(257 行) | wave 2 · P1-Opus §2 A-2 | PPV 第 7 元素 + portability | P1 |
| **新增** | A-3 `skills/codex-review/SKILL.md` mirror(422 行) | wave 2 · P1-Opus §2 A-3 | adv vs review 分流 + ship-blocker | P1 |
| **新增** | A-4 `skills/task-decomposer/SKILL.md` mirror | wave 2 · P1-Opus §2 A-4 | 一起 cp 减边界跨越 | P2 |
| **新增** | A-5 `hooks/wrappers/dangerous-event-emit.sh` mirror(105 行) | wave 2 · P1-Opus §2 A-5 | Safety Floor T001 + eval-event wire | P1 |
| **新增** | A-6 `tests/integration/` 整子树 8 sh(文件级 only) | wave 2 · P3R1-Opus §3 D1 | T012 SHIP GATE 主体 | P1 |
| **调整** | B-1 SHARED-CONTRACT §6 Cross-device publish 段(EXDEV) | wave 2 · P2-GPT §3.1 反驳 | 代码会做、契约没说 drift 源 | P1 |
| **调整** | B-4-IDS `--ids-verdict-evidence` flag 协议语义 + REVIEW-LOG schema | wave 2 · P3R1-Opus §3 D2 | F10 cross-repo trust real gap | P1 |
| **调整** | C-2 `gen-handback.sh --out` 默认前缀 | wave 2 · ENTRY 8 A4 | low UX bug · 不阻塞 ship | P1 |
| **新增** | `bootstrap.sh` 升级读新子树 + 临时 fixture idea bootstrap | wave 3 · P3R2-Opus §2 | v0.2 ship 关闭判据主体 | P1 |
| **新增** | `framework/xenodev-bootstrap-kit/MANIFEST-v0.2.md`(3 wave append) | wave 1-3 · P3R1-GPT §3 D3 | SSOT 边界内 provenance | P0 |
| **新增** | `framework/xenodev-bootstrap-kit/README.md` 4 子树说明同步 | wave 3 · P3R2-Opus §1 D3 | 消费者文档同步 | P1 |
| **删除/降级** | B-3 IDS dir flock/fcntl 不入 v3 主线 | v0.2-note · P3R2-Opus §3 | 并发未实证 · fail-closed cleanup 足够 | P2 → note |
| **新增**(XenoDev 端) | B-4-XenoDev runtime implementation(flag + REVIEW-LOG + verify-all 消费 + hand-back) | XenoDev side · P3R2-Opus §1 D2 | K9 双仓边界 binding | P1(XenoDev) |

---

## §W3 · Refactor plan(按模块 + 3 wave)

### 模块 A · mirror rebuild(3 wave · IDS bootstrap-kit 子树扩张)

**当前问题**:XenoDev 真路径已长出 4 个子树(skills + hooks + tests/integration
+ handback-validator/{templates,gen,score}),IDS `framework/xenodev-bootstrap-kit/`
mirror 仅含 v0.1 ship 的 5 子树(eval-event-log + handback-validator 部分 +
safety-floor-1/2/3 + workspace-schema)。本 session ENTRY 7+9+13 已 cp 5 文件
到 handback-validator/ 子树内,**其余 4 子树仍 stale**。

**目标态**:bootstrap-kit 与 XenoDev SSOT 字节级一致(SHA dual-verify)+ 每波
manifest provenance + README 同步描述 4 新子树。

**改造步骤**(严格顺序):

1. **wave 1 cp(P0 硬阻 · IDS commit 1)**:
   1. `cp -p` 3 文件:`handback-validator/templates/handback.template.md` /
      `gen-handback.sh` / `score-handback.sh` 从 XenoDev 到
      `framework/xenodev-bootstrap-kit/handback-validator/`
   2. SHA dual-verify(source / target sha256 一致)
   3. append `MANIFEST-v0.2.md §wave-1`(7 字段)
   4. wave 1 同 commit:修 C-1 + C-3 + B-2(详见 模块 B/C)
2. **wave 2 cp(P1 文件级 mirror · IDS commit 2)**:
   1. mkdir IDS mirror 新子树:`skills/{parallel-builder,spec-writer,codex-review,task-decomposer}/` +
      `hooks/wrappers/` + `tests/integration/`
   2. `cp -rp` 4 SKILL + 1 wrapper + 8 sh
   3. SHA dual-verify 每文件
   4. append `MANIFEST-v0.2.md §wave-2`
   5. wave 2 同 commit:协议 B-1 + B-4-IDS + lib bug C-2(模块 B/C)
3. **wave 3 联调(P1 真路径 · IDS commit 3)**:
   1. 升级 `framework/xenodev-bootstrap-kit/bootstrap.sh` 读新路径
   2. 用 IDS bootstrap 出生临时 test fixture(eg `discussion/006-bootstrap-test-fixture/`)
   3. 跑 `tests/integration/verify-all-outcomes.sh`,期望 exit 0 SHIP-READY
   4. 同步 `bootstrap-kit/README.md`(4 子树说明 + MANIFEST-v0.2.md 引用)
   5. append `MANIFEST-v0.2.md §wave-3`

**风险**:bootstrap.sh 升级是真路径代码改动(不只是 cp)· 风险随 cp 文件数
quadratic 上升(P1-Opus §3 不确定 1)· 缓解 = 分波 + manifest + SHA + wave 2
不声称 ship-ready(R2 硬规则)。

**预估代价**:M(wave 1 ~0.5 天 · wave 2 ~1 天 · wave 3 ~1.5 天 · 总 ~3 天)

### 模块 B · SHARED-CONTRACT §6 + event-schema 修订(协议 4 项)

**当前问题**:协议 v2.2 已 ACTIVE,但 batch 2 暴露的新事实未全部写入(EXDEV
cross-device publish / event enum 单复数 / IDS dir 排他写 / verdict-evidence
machine-readable)。

**目标态**:协议显式覆盖 producer 已实装的真路径;enum corruption 风险归 0;
B-4 协议语义 ready 等 XenoDev 端实装 follow-up。

**改造步骤**:

1. **B-2 enum 全复数统一**(wave 1):`event-schema.json` 改 `handback_drift` →
   `handback_drifts`;grep 5 文件一致(writer.sh / reader.sh / dangerous-event-emit.sh /
   score-handback.sh / event-schema.json);跨 migration cost = `.eval/events.jsonl`
   OLD 4 行考虑 reader 兼容
2. **B-1 Cross-device publish 段**(wave 2):SHARED-CONTRACT §6 加段 ·
   描述 EXDEV fallback(hardlink → cp + sha + ln)· producer 已实装(parallel-builder §6.3)
3. **B-4-IDS verdict-evidence 协议语义**(wave 2):SHARED-CONTRACT §6 加
   `--ids-verdict-evidence` consumer 期望 + REVIEW-LOG.md machine-readable schema
4. **B-3 IDS dir flock**(v0.2-note · NOT 入主线):SHARED-CONTRACT changelog v0.2
   entry 显式记 v0.2-note(触发条件 + 升 P1 路径)

**风险**:B-2 enum migration 可能漏改 reader;缓解 = grep 全仓 + dual-verify
events.jsonl OLD 行兼容。

**预估代价**:S(B-2 5 分钟 · B-1 半小时段落 · B-4-IDS 半小时段落 · B-3-note 5 分钟)

### 模块 C · XenoDev 本仓 lib bug 3 项

**注**:模块 C 改动在 XenoDev 仓真路径(不是 IDS mirror)· 但**hand-back 返 IDS**
形成 audit trail。

**当前问题**(HANDBACK-LOG batch 2 §5):

- C-1 scan-credentials exit code spec/impl gap(echo "ERROR" 但 exit 0)
- C-2 gen-handback `--out` 默认前缀冲突(004-pB T010 + 006a-pM T010 真撞)
- C-3 FU-producer-1 case F regression(T007 ship 后 template 真路径无 `{{RATIONALE}}` · main 14/15 fail)

**改造步骤**:

1. **C-1**(wave 1 · XenoDev real path):改 `scan-credentials.sh` exit code 1 if found · 加 `.scan-credentials-ignore` 白名单 + `--exclude-paths` flag · 14 false positive 治理
2. **C-3**(wave 1 · XenoDev real path):**operator 决定根因**(P1-Opus §3 不确定 2):
   - 选项 a(推荐):修 `score-handback.sh` yaml double-quoted rationale escape 真路径 → 让 case F 跑通
   - 选项 b(降级):删 case F → 接受"ship 后 template 无 `{{RATIONALE}}` 字面"= case F 永久 stale
   - **本 stage 不强行收敛**(operator 临门一脚决定)· 但 verdict 强制 P0 必须**有人修**
3. **C-2**(wave 2 · XenoDev real path):`gen-handback.sh --out` 默认前缀
   `<prd_fork_id>-<task-id>-handback.md` · 防同名冲突

**风险**:C-3 选 b 会让"case F 不再有意义"成为 spec 真路径模糊;选 a 是更
严格但 corner case 需测真路径找回。

**预估代价**:S(C-1 5 分钟 + C-2 5 分钟 + C-3 选 a ~1 小时 / 选 b 5 分钟)

### 模块 D · bootstrap 真路径联调(wave 3)

见 模块 A wave 3 改造步骤 — 不重复。

**关键 ship 关闭判据**(R2 硬规则):wave 3 跑通 verify-all SHIP-READY exit 0 +
MANIFEST 三波完整 + B-3 v0.2-note 在 changelog + B-4-XenoDev 实装 hand-back 已回 IDS。

---

## §W4 · Next-version PRD draft(v0.2 PRD · 可直接进 plan-start)

```
# PRD · 006 · v0.2 · "bootstrap-kit v0.2 反向同步 + 协议修订 + lib bug 清班"

**Status**: Draft from forge v3, awaiting human approval
**Sources**: discussion/006/forge/v3/stage-forge-006-v3.md + HANDBACK-LOG batch 2
**PRD-form**: simple

## User persona

- 非软件开发背景的 1-人 operator(K verbatim)
- 用 Claude Code 实现可靠自动化开发(K verbatim)
- 已经跑通 v0.1 ship(006a-pM)真路径 4 步 1-2;3-4 跨仓 pending

## Core user stories

- 作为 operator,我希望 IDS bootstrap-kit 字节级镜像 XenoDev SSOT,这样新 idea
  bootstrap 不会缺 skills/hooks/tests/templates
- 作为 operator,我希望 SHARED-CONTRACT §6 显式覆盖 producer 已实装真路径
  (EXDEV / verdict-evidence),避免"代码会做、契约没说"drift
- 作为 operator,我希望 lib bug 3 项(scan exit / `--out` 前缀 / case F regression)
  不阻塞下一个 idea 的真路径 ship

## Scope IN

- IN-1 完整 mirror(7 子树 + 4 SKILL + MANIFEST-v0.2.md)— wave 1+2
- IN-2 协议升 B-1(EXDEV)+ B-2(enum 全复)+ B-4-IDS(verdict-evidence 语义)
- IN-3 lib bug 0 残余(C-1 + C-2 + C-3 · XenoDev real path · hand-back 回 IDS)
- IN-4 bootstrap.sh 升级 + 真路径联调(临时 fixture idea + verify-all SHIP-READY)
- IN-5 MANIFEST-v0.2.md(3 wave append · 7 字段)+ README.md 同步描述新子树

## Scope OUT(显式 non-goals)

- OUT-1 不动 IDS=治理 / XenoDev=唯一 L4 双仓边界(Evidence map "v2 verdict 不重审" 行 · K9 binding)
- OUT-2 不实装 B-3 IDS dir flock/fcntl(Evidence map "B-3 v0.2-note" 行 · 并发未实证 · 触发后升 P1)
- OUT-3 不在 IDS v3 直接实现 B-4-XenoDev runtime(Evidence map "B-4 拆 IDS+XenoDev" 行 · K9 binding)
- OUT-4 不重审 v2 verdict / 不重开 idea 判断(Evidence map "v2 verdict 不重审" 行 · K9)
- OUT-5 不引入 IDS bootstrap-kit 包装层(P1-GPT §3 不确定 1 R2 收敛 = 字节级 cp + manifest)

## Success looks like

- wave 3 跑通临时 fixture idea bootstrap → verify-all-outcomes.sh exit 0 SHIP-READY
- MANIFEST-v0.2.md 三波完整 + 每文件 source/target SHA 一致 · operator 可手工 grep 验证
- SHARED-CONTRACT v2.3(或 v2.x)Changelog 显式记 B-1 + B-2 + B-4-IDS + B-3-note
- XenoDev side B-4-XenoDev runtime implementation hand-back 已返 IDS · HANDBACK-LOG 新 ENTRY
- 下一个新 idea(eg 007)bootstrap 后真路径跑通 ship 流程 0 中断

## Real constraints

- 时间:~1.5 周(IDS ~3 天 + XenoDev B-4-XenoDev ~3 天 + buffer)
- 平台:macOS Darwin 25.4.0(已知)+ Codex 5.3/5.4 + Claude Opus 4.7
- 跨仓:IDS(本仓)+ XenoDev(`/Users/admin/codes/XenoDev/`)· hand-back 通道
  v2.2 既有
- 合规:K10 边界纪律(每 wave 1 commit · 不混波)+ K11 strong-converge

## UX principles

- 边界先定、批量 SSOT、不越界(K10 verbatim)
- wave 2 cp 通过 ≠ ship-ready(R2 硬规则)
- 残余分歧用 v0.2-note 旁注(K11 §"残余分歧 v0.2-note 旁注")

## Open questions(forge 也没解决的)

- C-3 case F 根因修复(选 a escape vs 选 b 删 case F)· operator 临门决定 · 不影响 P0 必修
- bootstrap.sh 升级是否需要新增 verify-bootstrap.sh smoke test?(W3 模块 A wave 3 未列 · 可在 plan-start 决定)
- B-4-XenoDev runtime task 在 XenoDev 仓走 plan-start 还是直接 task ship?(W5 dev plan 已列,但调度由 XenoDev runtime 决定)
```

---

## §W5 · Next-version dev plan(按 phase / milestone)

### Phase 1 · IDS side wave 1(预估 ~0.5 天)

- 目标:P0 hard-block 全 ship · gen-handback 真路径 unblock
- 关键 milestone:
  - M1.1: cp 3 文件(templates + gen + score)+ SHA dual-verify PASS
  - M1.2: C-1 scan-credentials exit code 修(XenoDev real path commit)+ hand-back 回 IDS
  - M1.3: C-3 case F regression 修(operator 决定 a/b)+ hand-back 回 IDS
  - M1.4: B-2 enum 全复数(5 文件 grep 一致)
  - M1.5: MANIFEST-v0.2.md §wave-1 append + IDS commit 1
- 依赖:operator 在 M1.3 决定 a/b
- 风险:case F 选 a 时 score escape 真路径找回 corner case(P1-Opus §3 不确定 2)

### Phase 2 · IDS side wave 2(预估 ~1 天)

- 目标:文件级 SSOT mirror 完整 + 协议补段
- 关键 milestone:
  - M2.1: cp 4 SKILL + 1 wrapper + 8 sh + SHA dual-verify 每文件
  - M2.2: B-1 SHARED-CONTRACT §6 Cross-device publish 段补写
  - M2.3: B-4-IDS verdict-evidence 协议语义 + REVIEW-LOG.md schema 加入 §6
  - M2.4: C-2 gen-handback `--out` 默认前缀(XenoDev real path · hand-back 返)
  - M2.5: MANIFEST-v0.2.md §wave-2 append + IDS commit 2
- 依赖:wave 1 已 ship · 已 SHA dual-verify 跑通 1 次
- 风险:**wave 2 cp 通过不等于 ship-ready**(R2 硬规则)· 不可在此宣称 v0.2 done

### Phase 3 · IDS side wave 3(预估 ~1.5 天)

- 目标:bootstrap 真路径联调 PASS · v0.2 ship 关闭判据全达成
- 关键 milestone:
  - M3.1: `bootstrap.sh` 升级读新子树(skills/ + hooks/wrappers/ + tests/integration/ + handback-validator/{templates,gen,score})
  - M3.2: IDS bootstrap 临时 fixture idea(eg `discussion/006-bootstrap-test-fixture/`)
  - M3.3: 跑 `tests/integration/verify-all-outcomes.sh` exit 0 SHIP-READY
  - M3.4: `bootstrap-kit/README.md` 同步描述 4 子树 + MANIFEST 引用
  - M3.5: MANIFEST-v0.2.md §wave-3 append + IDS commit 3
  - M3.6: SHARED-CONTRACT changelog v0.2 entry(含 B-3 v0.2-note)
- 依赖:wave 1+2 都 ship
- 风险:bootstrap.sh 升级真路径代码改动 · fixture idea 清理(P1-Opus §3 不确定 1)

### Phase X(并行) · XenoDev side B-4-XenoDev runtime(预估 ~3 天 · XenoDev 仓)

- 目标:`--ids-verdict-evidence` flag 真路径实装 + REVIEW-LOG.md 写出 + verify-all 消费证据 · 完成 round-trip
- 关键 milestone:
  - MX.1: XenoDev parallel-builder 接 `--ids-verdict-evidence` flag(读 IDS REVIEW-LOG.md)
  - MX.2: codex-review / spec-writer 写 machine-readable REVIEW-LOG.md schema
  - MX.3: `tests/integration/verify-all-outcomes.sh` 加 evidence 消费 case
  - MX.4: XenoDev task ship + hand-back 返 IDS(HANDBACK-LOG 新 ENTRY)
- 依赖:IDS wave 2 ship(SHARED-CONTRACT §6 已含 B-4-IDS 协议语义)
- 风险:XenoDev schema 与 IDS 协议 lag · 缓解 = 协议先 ship · 实装后 hand-back 验证

---

## §W6 · Long-form synthesis(跨 backlog 系统性 insight)

**论点 1 · K10 从"5 文件 cp"升级为"分波 SSOT mirror"**

本 session 2026-05-27 ENTRY 7+9+13 三连 cp 5 文件 + SHA dual-verify 是 K10
"边界先定、批量 SSOT、不越界"的第一次实证。但实证范围仅止于 handback-validator/
子树内的 5 个文件(_yaml-helpers + writer + validate + check-3 + check-5)。
v3 verdict 把这条纪律升级到完整的"4 子树 + manifest + provenance + 真路径联调"
形态:wave 1 锁 templates/gen/score(producer 入口)· wave 2 锁 skills+hooks+tests
文件级 cp · wave 3 才声称真路径 bootstrap-kit 可生成可验证的新 XenoDev idea。
**这个升级的本质是把"小范围 cp"的工程纪律,扩展为"完整 SSOT mirror"的产品级
工程纪律 — 每波必须有 manifest 7 字段 + bootstrap-kit/MANIFEST-v0.2.md 同位置
provenance + SHA dual-verify 双向**。如果某天 operator 决定再扩 mirror 边界
(eg 把 XenoDev `.claude/agents/` mirror 进 IDS),这条 SOP 是直接可复用的。

**论点 2 · hand-back v2.2 已成熟到需要完整 producer/tooling mirror**

hand-back schema v2.2 在 batch 2(2026-05-27 ENTRY 7-17)的 11 包真路径 ship 中
表现出**0 false positive / 0 false negative / 全 6 约束 PASS**。这意味着 hand-back
通道已经从"协议草案"演化到"producer 真路径工具链"阶段 — gen-handback.sh
495 行 + score-handback.sh 229 行 + 6 check 脚本 + _yaml-helpers + template
SSOT 都是真路径必需件。**IDS bootstrap-kit 只 mirror 一半工具链(handback-validator
部分)是不可持续的** — operator 在 IDS 仓 bootstrap 一个新 idea 时,如果只
拿到 validate + check 但没有 gen + score + template,等于让新 idea 的 producer
从零写 hand-back YAML,这与 K verbatim "可靠的、自动化程度最高的解决方案"违背。
v3 wave 1 cp templates/gen/score 是补这个 gap 的 P0 硬阻。

**论点 3 · v3 的关键纪律 = 协议与 runtime 实装分仓**

B-4 verdict-evidence flag 在 R2 被拆成 B-4-IDS(协议改 · v3 IDS commit)+
B-4-XenoDev(runtime 实装 · XenoDev 单独 task · hand-back 返 IDS),是 v2 verdict
双仓边界(IDS=治理 + XenoDev=唯一 L4 runtime)在 v3 真路径上的首次"按协议
形态分仓"实证。**含义**:IDS 仓的 forge stage doc 不该 surface 包含 XenoDev
runtime 实装的 task,因为这等于 IDS 越界跨仓 commit XenoDev 代码 — 违反 K9
"v2 verdict 不重审"。**正确形态**:IDS 仓的 forge / PRD 只给协议语义 + 消费者
期望 + task 约束,XenoDev 仓自主决定真路径(plan-start / 直接 task ship),
完成后通过 hand-back 通道返 IDS 完成 round-trip。这条纪律未来会扩展到所有
"协议改影响 XenoDev runtime"的 forge,B-1 EXDEV 段(协议描述 producer 已实装
真路径)是相同模式的 v3 第二个实例 — 但因为 producer 已实装,只需协议补段,
不需要 B-4 那样的"协议改 + runtime 实装"拆分。

**v3 整体的故事线**:v0.1 在 2026-05-27 早 ship 封箱 → 同日批量 ENTRY 7-17
决议把 11 项 backlog 系统化 → forge v3 在同日午 fresh intake,把 11 项一一
对一收敛到 verdict + 3 wave dev plan + v0.2 PRD draft。整个跨度不到 12 小时,
但 verdict 强度极高(0 推翻 / 3 分歧 closed / 1 v0.2-note · strong-converge)。
**这个速度可能本身就是 v2 verdict + K10 边界纪律成熟度的一个 KPI** — 当大架构
稳定后,落地后的真路径修订能在一天内从 backlog 决议演化到可执行 v0.2 PRD,
说明本仓的 forge / hand-back / 协议 / lib 工具链已经成熟到"工程纪律级 batch
ship"阶段。**未来 3-6 月可能的演化**:v0.2 ship 后,B-3 IDS dir flock 若实证
触发 → forge v4 处理 + 升 P1;否则下一个 forge 可能转向新 idea 的 L4 plan
真路径或 IDS 协议 v3 主要演化(如 spec-writer 多 PRD-form 支持的协议化、
parallel-builder 并发拓扑的协议化)。

---

## What this menu underweights(强制自批判)

诚实表述本 stage 文档可能 underweight 的点。

- **反对证据未充分整合**:
  - C-3 case F regression 修法 a/b(score escape 真路径 vs 删 case F):P1-Opus
    §3 不确定 2 提议 operator 决定,R2 verdict 强制 P0 必修但**未硬性收敛根因**。
    这是双方都让步给 operator 的 1 个 micro-decision,不影响 wave 1 ship。
  - B-1 EXDEV 协议段 priority:Opus P1 初评 P2,Codex P2 §3.1 反驳后让步 P1。
    主 verdict 接受 P1,但 P1 vs P0 的边界对 wave 安排不影响。

- **Y 视角覆盖盲区**:
  - Y 视角未含**安全/审计**:11 项 backlog 中 C-1 scan-credentials 14 false
    positive 治理涉及 Safety Floor 件 1,有 secret leak 风险。verdict 修了
    exit code + 白名单,但**未让任何视角对"白名单机制本身是否引入新攻击面"
    做独立审视**。建议在 wave 1 ship 后,operator 单独 mental review 白名单
    设计是否合理。
  - Y 视角未含**性能/扩展性**:tests/integration 8 sh + verify-all
    跨 fixture 跑的真路径性能未在任何视角触及。若未来新 idea bootstrap 多
    了,wave 3 真路径联调时长可能超预估 1.5 天。

- **K 中未充分回应的关切**:
  - K verbatim "可靠的、自动化程度最高的解决方案":v3 verdict 显式回应了
    "可靠"(SHA dual-verify + manifest + wave 2 不声 ship-ready),但**自动化
    程度最高**这条仅由 wave 3 真路径联调间接覆盖。bootstrap.sh 升级后是否
    能做到"operator 0 干预生新 idea"未硬性写进 ship 关闭判据 — 这可以是
    v0.3 forge 的关切点。

- **convergence_mode 副作用**:
  - strong-converge 让 v3 极快收敛(P3R2 双方都 CLEAN),但**双方在 P1 都
    没有外部参照(Z=不对标)** → 可能让两模型回声室强化某些工程纪律细节
    (eg manifest 7 字段精确清单)而忽略外部 SOTA 的更优形态(如 OCI
    container manifest spec / git submodule)。建议:若 wave 2 ship 后
    operator 觉得 manifest 形态笨,可在 v4 加 Z = SOTA mode 重审。

- **X 标的覆盖局限**:
  - 13 个标的覆盖 IDS + XenoDev 真路径核心,但**未读 XenoDev 仓的
    .claude/commands/ 和 .claude/agents/**;若 v0.2 ship 后发现 IDS bootstrap 出生
    的新 idea 缺这些(在 K10 边界内但未列入 4 子树),会触发 v0.3 mirror
    边界再扩张。

- **forge versioning 提示**:以下新信息进入会触发 v4:
  1. B-3 IDS dir flock 实证 race / corruption(任一 XenoDev session 报错 or
     operator 实证)→ 升 P1 + forge v4 决定具体 lock 机制
  2. wave 2 cp 后,SHA mismatch 出现(SSOT drift)→ forge v4 决定如何防止
     drift(自动同步 hook?CI 校验?)
  3. K verbatim 提到的"自动化程度最高"在 wave 3 ship 后未达成 → forge v4
     可以是 "automation gap 审计" 视角的 fresh intake

如果真的没有可批判的点 — 但**本扫描后真发现上述 6 类盲区**;请注意 forge 是
双模型综合,不是用户访谈或真实数据,**wave 3 真路径联调跑通**才是 v0.2 真
ship 凭证,不是本 stage 文档拍板。

---

## Decision menu(for human)

### [A] 接受 verdict 进 L4(需 fork 出 PRD branch)

```
⚠ /plan-start 要求 <prd-fork-id> + 完整 PRD 目录,不能直接吃 forge stage 文档。
⚠ 现有仓库 PRD 都是平铺布局 — discussion/<root>/<prd-fork-id>/PRD.md
   (无嵌套,如 discussion/001/001-pA/PRD.md)
⚠ 注:idea 006 的 v0.1 已在 discussion/006/006a-pM/ 平铺 ship · v0.2 fork-id
   建议沿用 006a-pM-v0.2 或 006a-pM2 等命名,不要嵌套 discussion/006/006a-pM/006a-pM-v0.2/。

流程(暂时手工,等待 /fork-from-forge 命令落地):

1. 选一个 prd-fork-id:
   - 推荐 006a-pM-v0.2(显式表示是 006a-pM 的 v0.2 演进)
   - 或 006a-pForge-v3(显式表示来自 forge v3 stage doc)

2. 创建 discussion/006/<prd-fork-id>/PRD.md
   - 把本 stage 中的 §W4 "Next-version PRD draft" 抽出
   - 补 frontmatter:
     **PRD-form**: simple
     **Source**: discussion/006/forge/v3/stage-forge-006-v3.md

3. 创建 discussion/006/<prd-fork-id>/FORK-ORIGIN.md
   说明 forked-from = forge stage v3,parent = 006a-pM(v0.1 ship 封箱)

4. /plan-start <prd-fork-id>
```

§W5 dev plan 已给 phase 1+2+3 + XenoDev side phase X,plan-start 可直接消费。

### [B] 跑 forge v4(说明需要补什么)

```
/expert-forge 006
# 在 Phase 0 intake 时调整 X / Y / Z / W / K
# 旧 v3 整目录保留作历史参考
```

适用:
- B-3 IDS dir flock 实证 race(本 verdict 留作 v0.2-note · 升 P1 后)
- 需要 SOTA 对标 manifest / OCI / git submodule 等(本 v3 Z=不对标)
- 自动化程度 audit(K verbatim "自动化程度最高"未硬性覆盖)
- 新增 X 标的(eg .claude/commands/ + .claude/agents/ mirror 范围扩张)

### [C] 局部接受

列出哪几条采纳、哪几条挂起:

- ✅ 采纳示例:wave 1 P0 hard-block(templates/gen/score + C-1 + C-3 + B-2)
  立即 ship,因 producer 入口硬阻
- ⏸ 挂起示例:wave 2/3(skills/hooks/tests mirror + 协议 B-1/B-4-IDS +
  bootstrap.sh 升级)等 wave 1 实证后再决定 wave 2 边界
- ❌ 拒绝示例:某条 mirror 项(eg A-4 task-decomposer mirror)若 operator
  认为暂不需要 SSOT 同步

### [P] Park

```
/park 006
```

保留所有 forge 产物 + v0.1 ship 状态 · 标记为暂停 · 复活时不重做 forge v3。

### [Z] Abandon

```
/abandon 006
```

forge verdict 显示该 idea 不该继续做。归档 lesson 文档。
**注**:idea 006 的 v0.1 已 ship 真路径成功,此选项基本不应选用,除非 operator
判定整个 IDS+XenoDev framework 走错方向。

---

## Forge log

- **v3**: 2026-05-27 — verdict: "v0.2 = 11 项 backlog 三类 batch ship · 3 wave 顺序 · 每 wave 1 IDS commit + MANIFEST · B-3 IDS dir flock 留 v0.2-note · B-4 协议改 + XenoDev 实装拆分"
- **v2**: (历史 baseline · 见 `discussion/006/forge/v2/stage-forge-006-v2.md`) — verdict: "IDS=治理 + XenoDev=唯一 L4 runtime + 双向 hand-off"(K9 binding · v3 不重审)
- **v1**: (更早历史 · 见 `discussion/006/forge/v1/`)
