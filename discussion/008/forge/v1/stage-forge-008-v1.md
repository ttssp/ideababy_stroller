# Forge Stage · 008 · v1 · "C5 措辞证伪后的 refactor-and-reset"

**Generated**: 2026-06-04T13:05:00Z
**Source**: forge run v1 with X = 4 标的, Y = 仅产品价值, Z = 不对标, W = verdict-only + decision-list + next-PRD
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both), P2 (both), P3R1 (both), P3R2 (both)
**Searches run**: 0 across 0 distinct sources(Z=不对标 · 法律检索由 operator 负责)
**Moderator injections honored**: none
**Convergence outcome**: converged(双方 P3R2 §2 verdict 字面级一致 · 0 unresolved)

---

## How to read this

forge 是横切层(不是 L1-L4 pipeline 的一部分)。本文档是双专家(Opus47Max +
GPT55xHigh)对 008-pB 现状的独立审阅 + 联合收敛后的产出,**强制给出立场**
(不是候选菜单 defer 给你拍板)。本轮由 `/handback-review 008` 触发:008-pB
Phase 0 探针判定 FAIL(回放「合规下不可达」)被 operator 证伪。

读完后你应该:
- 知道双专家对「C5 措辞 + 受 C5 污染的 scope/gate」的最终 verdict
- 能在 §"Evidence map" 逐条溯源每条结论到具体 round 段落
- 拿到 §"Decision matrix"(4 列保留/调整/删除/新增)+ §"Next-version PRD draft"
  (C5 重定草案 + 3 个待 operator 拍板的产品决策点),可直接进 `/scope-inject`
- 能基于 §"Decision menu" 进入下一步(改 PRD → 解锁探针 → 进 L4 / 跑 v2 / park)

## Verdict

**008-pB 产品方向站得住,不 redesign、不降 scope。本轮唯一动作 = refactor-and-reset**
—— 把被旧 C5 措辞污染的三处判准复位:

1. **修 C5 措辞**:「正常能看到」→「有权访问的内容 + 有效登录态采集原内容
   (含须抓包取得的图文/回放原文件),自用不传播,不规避**他人**访问控制」。消除
   「视觉可见/截屏」的字面化误读。(回应 K「『正常能看到』= operator 有权访问的内容」)
2. **回放 scope 复位**:cut handback「图文先走、回放移 v0.2」的依据(源于已作废的
   探针 FAIL),回放留 v0.1。(回应 K「回放是最高价值、不可移 v0.2」)
3. **token 失效介入成本升为显式可验收 outcome**,给可选阈值档位让 operator 选。
   (回应 K「最在乎自动化程度 · token 失效要重登录是真痛点」)
4. **Phase-0 探针 gate 判准改向**:从「合规可达性」(伪命题,已作废)→「自动化
   稳定性/低维护恢复」。gate 不删,换尺子。(回应 K「探针 FAIL 作废」)

合规边界由 operator 负责,本 verdict 全程未碰法律定性,只改产品措辞与判准。

## Evidence map

| 结论 | 来源 | 引用(≤15 words) | 是否有反对证据 |
|---|---|---|---|
| C5 措辞是根因(隐喻被字面化) | P1-Opus §1(1) + P1-GPT §1 + P2-Opus §3 | "把『自动化我自己的眼睛』收成了字面『只采视觉可见』" | 无 — 双方无沟通定位同一根因,置信度最高 |
| C5 应重写为「有权访问 + 有效登录态采原内容」 | P3R2-Opus §2.1 + P3R2-GPT §2 | "operator 有权访问的内容;有效登录态采集原内容,自用不传播" | 无 |
| 回放留 v0.1(cut handback 降级依据) | P1-Opus §2 + P1-GPT §2 + P3R2 双方 §2.2 | "cut handback 的『回放移 v0.2』依据" | 无(双方一致;handback 建议被显式作废) |
| token 失效介入成本升为显式 outcome | P1-Opus §1(3)/§2 + P1-GPT §2 | "尚未把『token 失效后的介入次数』变成验收指标" | 无 |
| outcome 应给可选阈值档位 | P1-GPT §3.1 + P2-Opus §3 + P3R2-Opus §4 | "每天一次、每周一次、失效扫码一次,还是趋近无感" | 无 |
| Phase-0 gate 判准从「合规可达性」改「自动化稳定性」 | P2-GPT §3 + P3R1 双方 §1 | "从『合规可达性』复位为『自动化稳定性』" | 无 |
| 回放摘要用「最低验收边界 + 可分层升级」 | P3R1 分歧 1 → P3R2 双方 §1 合并 | "最低验收边界…哪些达标,哪些升级" | ⚠ 曾为唯一分歧(叫法之争),R2 已合并(见下) |
| 回放管线工程量仍是真风险(非合规风险) | P1-Opus §3.3 + P2-Opus §3 末 | "下载/ASR/摘要工程量真风险" | ⚠ 见 §"What this menu underweights" |
| 三形态登录态是否共享 = v0.2 待观测项 | P1-GPT §3.2 + P2-Opus §3 + P3R2 双方 §3 | "三形态登录态/失效模式不共享…多条恢复路径" | 无(降级为 v0.2 note,不阻塞主 verdict) |

(表格 9 行 · 均可溯源 · 无 verbatim quote >15 words)

## Intake recap

### X · 审阅标的(4 个)
- `discussion/008/008-pB/PRD.md`(本仓库文件 · C5 在 line 116)
- `discussion/008/L3/L3R2-Opus47Max.md`(stage 文档 · C5 措辞 source)
- `discussion/008/handback/20260604T095517Z-008-pB-20260604T095517Z.md`(XenoDev 探针 hand-back · 被证伪 FAIL)
- `proposals/proposals.md` §008(operator 原始痛点:token 过期要重登录)

### Y · 审阅视角
- ✅ 产品价值 —— 唯一视角(合规/法律定性 = binding 已决前提,非审议对象)

### Z · 参照系
- mode: 不对标(Phase 2 不跑法律检索 · 0 search)
- 用户外部材料: 无(proposals §008 已在 X 标的内)

### W · 产出形态
- ✅ verdict-only → §"Verdict rationale"
- ✅ decision-list → §"Decision matrix"
- ✅ next-PRD → §"Next-version PRD draft"

### K · 用户判准
核心问题:在「C5 不再卡死抓包」这个 operator 已拍板的新前提下,008 的产品形态/
scope/自动化挑战该怎么定?binding 前提:合规由 operator 负责;「正常能看到」=
operator 有权访问的内容(非视觉可见/截屏);探针 FAIL 作废,回放与图文均可达。
operator 最在乎:① 自动化程度(token 失效少操作);② 回放是最高价值、不可移 v0.2;
③ 三形态不漏;④ C4/C6/C8/C9 既有约束不变。不要:论证法律 / 劝阻改 C5 / 重审
candidate B 或 phase 排序。

### 收敛模式
- strong-converge(双方 P3R2 §2 verdict 字面级一致 → 单一 verdict)

---

## Verdict rationale(W: verdict-only)

本轮的判断置信度异常高,原因在 evidence 结构本身:**两位审阅人在并行独立阶段
(P1 互不可见)无沟通却定位到完全相同的根因**。Opus P1 §1(1) 追到 L3R2-Opus §2
「自动化我自己的眼睛」隐喻,指出它在 L4 探针被字面化为「视觉可见 = 截屏 OK,抓包 =
越界」;GPT P1 §1 独立追到同一条链「把有效登录态抓包误判成绕过访问控制」。
double-blind 命中同一根因,使「C5 措辞是根因」成为本 stage 最 load-bearing 且最难
被推翻的结论。

为什么是 refactor 而非 redesign:产品骨架(candidate B 全形态 / v0.1 含回放 /
价值优先排序)是 operator 已拍板、K 显式禁止重审的背景。问题域被精确地限制在「一个
措辞歧义污染了三处下游判准」—— C5(合规措辞)、Phase-0 gate(判准)、outcomes
(缺口)。修措辞 + 复位判准即可,不动骨架。

为什么 token outcome 是「补回缺口」而非「发明需求」:它本就是 proposals §008 写在
最前的真痛点(token 过期每次要重登录),却在现行 PRD 只以 UX principle「省心 >
功能丰富」「介入趋近零」(PRD line 127)一句带过,没量化、没进 outcomes 表。新 C5
解锁「抓包可达」后,而抓包正是 token 失效的发生地,「token 失效后怎么少操作」从
合规问题彻底变回纯自动化产品挑战 —— 这正是双专家该聚焦的。

forge 比 handback 走得更远的一点:handback 只说「探针判错了」,forge 进一步说
「探针该换一把尺子量」—— 从「回放在合规下能否采到」(已证伪伪命题)改为「有效
登录态采集能否低维护恢复」(真产品风险)。这把 008 的命门从假问题挪回真问题。

## Decision matrix(W: decision-list · 4 列)

| 类别 | 项 | 来源(标的具体位置) | 理由 | 优先级 |
|---|---|---|---|---|
| **保留** | candidate B 全形态方向 | PRD FORK-ORIGIN / §产品形态 | operator 已拍板 · K 禁止重审 | P0 |
| **保留** | v0.1 含图文+回放(价值优先排序) | PRD §v0.1 outcomes | 回放含重要消息+周度复盘+下周策略,决策价值最高 | P0 |
| **保留** | 回放摘要「转文字+关键点+可溯源」意图 | PRD §UX / C6 | 不只存文件,压成几分钟可溯源 | P0 |
| **保留** | C4/C6/C7/C8/C9 既有约束 | PRD line 115-120 | 未受 C5 污染 · K 显式不动 | P0 |
| **调整** | C5 措辞(line 116) | PRD line 116 ← L3R2-Opus §2 | 「正常能看到」→「有权访问+有效登录态采原内容」,消除截屏字面化 | P0 |
| **调整** | Phase-0 探针 gate 判准 | PRD line 142-148 | 「合规可达性」→「自动化稳定性/低维护恢复」 | P0 |
| **调整** | §Biggest product risk 表述(line 131-138) | PRD line 138 | 去「合规不可达」伪风险,保留「下载/ASR/摘要工程量」真风险 | P1 |
| **删除** | handback「图文先走、回放移 v0.2」作为 PRD 修订依据 | handback §3 | 源于已作废探针 FAIL · 违背价值优先排序 | P0 |
| **删除** | 探针原 FAIL 结论(回放合规下不可达) | handback §1/§2 | 被 operator 证伪 · 图文回放均靠有效登录态抓包 | P0 |
| **删除** | C5 中「绝不破解/绕过访问控制」对「自己有权访问内容抓包」的误覆盖 | PRD line 116 | 仅保留对「他人/规避」的约束,不再误盖自己合法流量 | P0 |
| **新增** | v0.1 outcome:登录态失效后 operator 介入成本 + 可选阈值档位 | (新 — proposals §008 第一痛点) | 从 UX 一句话升为可验收 outcome | P0 |
| **新增** | 回放摘要「最低验收边界」+ 可分层升级项 | (新 — P3R2 双方合并) | 守住回放价值 + 让工程风险有显式 v0.1 合格门 | P0 |
| **新增** | next-PRD「待 v0.1 观测确认项」:三形态登录态是否共享 | (新 — v0.2 note 1) | v0.1 实采观测后,v0.2 加预警前确认 | P1 |

每行均可在 §"Evidence map" / 上方 PRD 行号溯源。

## Next-version PRD draft(W: next-PRD)

> **可直接喂 `/scope-inject 008-pB`**(C5 改写 + scope 复位 + outcome 新增),
> 或开新 PRD 版本。以下 3 个 ❓ 决策点需 operator 拍板。

```
# PRD 修订 · 008-pB · 由 forge v1 verdict 驱动

**Status**: Draft from forge v1, awaiting human approval
**Sources**: stage-forge-008-v1.md + forge v1 evidence map

## C5 改写(核心修订)
旧:只采 operator 正常登录、正常能看到的内容,绝不破解/绕过访问控制
新:只采 operator **有权访问**的内容,可用**有效登录态采集原内容**(含须抓包
    取得的图文/回放原文件),自用不传播,不规避**他人**访问控制。
理由:消除「正常能看到」被字面化为「视觉可见/截屏」的误读。合规由 operator
    负责,本修订只改产品措辞、不替 operator 做法律判断。

## Scope IN(复位)
- v0.1 含图文 + 回放(撤销 handback「图文先走」退路)
- 回放摘要:转文字 + 关键点 + 可溯源原始转录

## Scope OUT(显式 non-goals)
- 预警仍隔离 v0.2(evidence: PRD phase 排序 · 未受 C5 污染,不动)
- 自动续 token 极致无感形态 → 不在本轮拍板(evidence: v0.2 note 2 · 触及
  operator 合规负责灰区)

## Success looks like(新增/复位 outcomes)
- 【新增】登录态失效后 operator 介入成本 ≤ <operator 选定阈值>(可观测计数)
- 【复位】回放摘要可替代完整观看,关键点覆盖重要消息/周度复盘/下周策略且可溯源
- 【复位】图文+回放 2 周零漏,失败/不确定当天可见(C7)

## Phase-0 探针 gate 改判(换尺子)
旧判准:回放在合规下能否采到(伪命题,作废)
新判准:有效登录态采集能否**低维护恢复** —— 连续真实运行验证图文+回放可持续采,
        登录态失效能否低操作恢复,失败/不确定当天可见

## Open questions(forge 也没解决 · 需 operator 拍板)
❓ 决策点 1 · token 失效介入阈值档位:operator 选哪一档作 v0.1 success 线?
   候选:每天一次 / 每周一次 / 失效时扫码一次 / 趋近无感
   (008 能否「省心」的命门 · double-blind 两位审阅人都点为头号未决)
❓ 决策点 2 · 回放摘要最低验收线:「覆盖关键点 + 可溯源」是否够?还是必须含
   稳定时间戳 / 原始文件长期留存?(影响 v0.1 工程量)
❓ 决策点 3 · 三形态登录态共享性:列为 v0.1 实采观测项,v0.2 加预警前确认。
   (若不共享,「token 失效少操作」会裂成最多 3 条恢复路径)
```

---

## What this menu underweights(强制自批判)

- **反对证据未充分整合(⚠ 行)**:§"Evidence map" 中标 ⚠ 的两条,实质都不是
  立场对立。「回放摘要叫法之争」(执行节奏建议 vs 验收边界)在 P3R1 是唯一分歧,
  P3R2 双方已让步合并为「最低验收边界 + 可分层升级」—— 主 verdict 不受影响,但
  它隐含一个未量化的点:「最低验收边界」具体到哪(时间戳是否必须)仍是 next-PRD
  决策点 2 的 ❓,本 stage 未替你定。
- **回放工程量真风险被 verdict 绕过**:本轮把「合规不可达」证伪后,PRD
  §Biggest product risk 的另一半(1-2h 大文件下载 + ASR + LLM 摘要 + 可溯源的
  工程量)**依然真实存在**,且 Y=仅产品价值,双专家未做工程可行性评估。verdict
  让回放留 v0.1 是价值决定;它在 L4 是否如期可建,本 forge 没有也无权回答。
- **Y 视角覆盖盲区**:Y 仅含产品价值,合规被 binding 排除。这是 operator 显式
  姿态,但意味着本 stage 对「抓包采集的合规边界」零审议 —— 若 operator 的合规
  判断本身有误,本 stage 的全部 verdict 会连带失效(C5 改写正是建立在合规已决
  前提上)。这不是 forge 能兜底的。
- **K 中已充分回应**:K 的 4 个 operator 关切(自动化 / 回放不降级 / 三形态不漏 /
  既有约束不变)verdict 均显式覆盖,无遗漏项。
- **convergence_mode 副作用(回声室)**:strong-converge + double-blind 同根因
  命中,使「C5 措辞是根因」置信极高 —— 但两模型都只读了相同的 4 个 X 标的,
  都接受同一个 binding 合规前提。**双方都同意但可能错的判断**:假定「修措辞 +
  换 gate 尺子」就能解锁 008 —— 真正的命门(token 失效低维护恢复)能否在 L4
  工程上达成,两模型都没有也无法验证,只是把它升为 outcome。
- **X 标的覆盖局限**:未读 XenoDev 侧探针实现 / Proxyman 实采日志。verdict 基于
  PRD + handback 的文字论证,而非实际抓包行为数据。真实采集行为可能与文字假设不符。
- **forge versioning 提示**:以下任一新信息进入会触发 v2 并可能改变 verdict ——
  (a) operator 合规判断被外部(平台 ToS 变更 / 法律意见)推翻;(b) v0.1 实采
  观测到三形态登录态**不共享**,使「低操作恢复」不可行;(c) L4 证明回放管线工程量
  超出 v0.1 时间窗(C1: 2-3 月)。

forge 是双模型综合,不是用户访谈或真实采集数据 —— 真实数据(尤其 token 失效频率、
回放管线实际工程量)可能仍推翻本 verdict。

## Decision menu(for human)

### [A] 接受 verdict → 改 PRD C5 + scope 复位(推荐路径)
```
本 verdict 的产出会回流改 008-pB 的 PRD(不是 fork 出新 PRD branch —— 这是
对现行 PRD 的修订,不是另起炉灶)。推荐走 /scope-inject:

1. /scope-inject 008-pB
   注入本 stage §"Next-version PRD draft":
   - 改写 C5(line 116):「正常能看到」→「有权访问 + 有效登录态采原内容」
   - 删除 C5 对「自己有权访问内容抓包」的误覆盖,保留对「他人/规避」的约束
   - Scope 复位:撤销 handback「图文先走、回放移 v0.2」依据,回放留 v0.1
   - 新增 outcome:登录态失效介入成本 + 阈值档位(operator 在注入时选决策点 1)
   - 改 Phase-0 gate 判准:「合规可达性」→「自动化稳定性/低维护恢复」
   - 改 §Biggest product risk:去「合规不可达」伪风险

2. 在注入时拍板 §"Next-version PRD draft" 的 3 个 ❓ 决策点
   (token 阈值档位 / 回放摘要最低验收线 / 三形态登录态共享性列为 v0.1 观测项)

3. PRD 修订后 → 解锁探针 gate(回放放行)→ 可让 XenoDev 按正确 C5 重跑探针
   (新探针判「自动化稳定性」而非「合规可达性」)→ 进 L4 /plan-start
```
⚠ 本路径是「修现行 PRD」,不需要 fork 出新 prd-fork-id。若 operator 希望保留
旧 PRD 作历史对照,可在 /scope-inject 前对 PRD.md 做 v 版本快照。

### [B] 跑 forge v2(说明需要补什么)
```
/expert-forge 008
# 在 Phase 0 intake 时调整 X / Y / Z / W / K
# 旧 v1 整目录保留作历史参考
```
适用:回放管线工程量风险想正式审(需把 Y 扩到「工程可行性」并解禁 Z 检索),
或 v0.1 实采后三形态登录态共享性有新数据需重判 token 自动化方案。

### [C] 局部接受
- ✅ 采纳:C5 措辞修订 + 回放 scope 复位 + Phase-0 gate 改判(这 3 项 double-blind
  共识,置信最高,建议至少采纳)
- ⏸ 挂起:token 失效阈值档位(等 operator 想清楚要哪一档「省心」标准再定)
- ⏸ 挂起:回放摘要最低验收线含不含稳定时间戳(等 L4 评估工程量后定)
- ❌ 拒绝:(无双专家建议被建议拒绝项)

### [P] Park
```
/park 008
```
保留所有 forge 产物,标记暂停。复活时不重做本轮。适用:operator 暂时无 v0.1
开发时间窗(C1: 每周 15-30 小时未就绪)。

### [Z] Abandon
```
/abandon 008
```
forge verdict 并**不**指向 abandon —— 方向站得住,只需 refactor。仅当 operator
对合规前提本身改变主意(不再愿承担合规责任)时此选项才相关。归档 lesson 文档。

---

## Forge log
(由 /expert-forge 命令更新;记录每次 forge run 的 v 序列 + 关键 verdict 一句话)

- v1: 2026-06-04 — verdict: "refactor-and-reset:修 C5 措辞(『有权访问』非『视觉可见』)、复位回放至 v0.1、token 失效介入成本升为显式 outcome、Phase-0 gate 改判『自动化稳定性』。合规由 operator 负责。"
- v2: 2026-06-16 — verdict: "GO:Obsidian 作 US8 人读前端入 v0.2 + 库→vault 单向 exporter;SQLite 唯一 SSOT 不漂(v0.1 三护栏保留);①替换/③双向永久出局;C5 增补渠道中性原则(自用不传播,不溯及 v0.1 已 ship 落点);vault 只放指针+摘要,原文永久 OUT;验收只读 frontmatter 不依赖可写脚本。" (converged · strong-converge · stage: forge/v2/stage-forge-008-v2.md)
