---
feature: 008-pB
prd_source: PRD.md
handoff_source: /Users/admin/codes/ideababy_stroller/discussion/008/008-pB/L4/HANDOFF.md
prd_form: phased
phases: [phase0-probe, v0.1, v0.2]
phase_current: phase0-probe
gate_phase: phase0-probe        # 硬门:v0.1 全部 task 入度依赖此 phase PASS 或 CONDITIONAL-accepted(§1.0 三态 + C10);task-decomposer/scheduler 必须把 phase0-probe 排在所有 v0.1 task 之前,不得当普通 v0.1 task
gate_blocks: v0.1               # phase0-probe FAIL 或未获批准的 CONDITIONAL → v0.1 不启动 → §5 退路;仅 PASS / CONDITIONAL-accepted(operator 显式批准)放行
schema_version: 0.1
status: frozen
reviewed-by: codex@2026-06-05 (v1.1-reset · with-known-gaps)
frozen_at: 2026-06-05
frozen_by: claude(spec-writer skill · v1.1-reset 重过 codex adversarial-review 12 轮 · 无任何 BLOCK · operator 决议 R11 修后收口 · 残留 2 known-gap 见 D-spec-v1.1-refrozen · 超 §3.2 4 轮上限有 006a-pM/006a-pM-v0.2 precedent)
prev_frozen_at: 2026-06-04
unfrozen_at: 2026-06-05
unfrozen_reason: "PRD v1.1(forge v1 refactor-and-reset)驱动实质性修订 —— gate 判准从『合规可达性』改向『自动化稳定性』· 旧 frozen 结论已不对齐 PRD · 需重过 codex adversarial-review 才能重新 frozen(per spec-writer SKILL §3.2:实质变更非纯 frontmatter amendment)"
ppv_count: 3
discussion_id: "008"
prd_fork_id: 008-pB
created: 2026-06-04
operator_decision_log:
  - decision: D-spec-frozen
    date: 2026-06-04
    topic: needs-attention(非 BLOCK)6 轮收敛后升 frozen
    verdict: 接受 frozen · 12 findings 全实修闭环(非 defer)
    rationale: "codex 6 轮无任何 BLOCK;R1 4 个 substantive finding(Phase 0 机器可读 gate 建模 / PPV 回放链 mock-hole / 维护阈值三态门 / 004 allowlist)全修;R2-R6 仅暴露同一类『PASS-only 措辞 / 三态门完整性』在 frontmatter/C10/§1.0/§5/§6/§2.1/architecture/non-goals/SLA 各文件残留实例,已穷尽 sweep 修齐为 PASS/CONDITIONAL-accepted/FAIL 状态机整包一致;自 R3 起 0 high、无新 substantive 洞 = 收敛非打转;SKILL §3.2『BLOCK 才阻 frozen · needs-attention 处置后可 frozen』+ 006a-pM(D1 破 4 轮上限 · 真证据)/006a-pM-v0.2(11 轮)precedent"
    impact: spec frozen · task-decomposer 可接 · 无遗留 binding gap(区别于 006a-pM-v0.2 留 R-Q 的情形)
    status: superseded-by-D-spec-v1.1-reset
  - decision: D-spec-v1.1-reset
    date: 2026-06-05
    topic: "gate 判准改向 —— 从『合规可达性』到『自动化稳定性/低维护恢复』"
    verdict: "解 frozen 重派 · 待重过 codex review 后重新 frozen"
    rationale: "008-pB Phase 0 探针曾判 gate=FAIL(回放『合规下不可达』),被 operator 在 IDS /handback-review 008 当场证伪 → /expert-forge 008 verdict=refactor-and-reset(converged)→ PRD v1.0→v1.1(IDS commit 1e7018c)。两条根因:① 探针把『浏览/截屏可达』误当『采集可达』(采集图文原内容和回放一样需抓包);② build runtime 越权做 C5 法律定性且判错(真实手段=付费有效登录态抓自己合法流量=采集有权访问内容,未踩 C5)。本次修订把 spec 的 gate 判准、P0-O1/O2 语义、三态判据、§5 退路、§7 PPV、证据骨架全部从『合规可达』改向『自动化稳定性』,删合规可达语义(合规由 operator 负责,不进 gate 判准),回放复位 v0.1。框架级教训(判准只能是 build-runtime 可自证工程事实)记 dogfood-backlog KG-7,不在本 spec 当场改框架。"
    impact: "spec status frozen→review · 旧探针观测结论(reachability=回放不可达 / P0-GATE=FAIL / gate-acceptance=blocked)全部作废、保留作审计留痕、需 operator 按新判准重采 · 重过 codex review 后重新 frozen"
    status: resolved-by-D-spec-v1.1-refrozen
  - decision: D-spec-v1.1-refrozen
    date: 2026-06-05
    topic: "v1.1-reset 重过 codex adversarial-review 12 轮后 · operator 决议收口 frozen(needs-attention 非 BLOCK)"
    verdict: "接受 frozen · 12 轮无任何 BLOCK · operator 在 R11 修后决议停止迭代"
    rationale: "v1.1-reset 的实质改动(gate 判准 + PPV 反 mock-pass 护栏)重过 12 轮 codex adversarial-review,无任何 BLOCK。R1-3 修判准 prose↔guardrail 一致性(『改 prose 没改 guardrail』2 个 high);R4-7 把 PPV verifier 的信任从 manifest 写入者整体移到『真实文件系统 + artifact 字节 + symlink-free realpath 锚定 run 目录 + 全 5 件 artifact』(run-scoped manifest/path、真 mtime/exit、下游绑定、symlink 逃逸);R8-11 收口 reachability 章节级解析(防 KG-7 浏览≠采集误判从粗 grep 漏回)、replay_entry 活区收口(防 stale/poison block)、timestamp_map 逐点 provenance + canonicalization 强校。selftest 从 31 → 68 case,每道防线有负向自测。自 R4 起无新结构性洞,R8 起 severity 持续降(R11=1high+1medium),R9-12 多为前轮修法精度迭代 = 收敛尾部非打转。operator 决议:R11 两 finding 修后收口,不无限刷 codex。SKILL §3.2『BLOCK 才阻 frozen · needs-attention 处置后可 frozen』+ 006a-pM(R5 operator 破 4 轮上限)/006a-pM-v0.2(11 轮)precedent。"
    impact: "spec frozen(v1.1)· task-decomposer/parallel-builder 可接 · 残留 2 known-gap(非 BLOCK · R12 提)显式记录:① timestamp_map source_ref 是子串匹配(可被转录里恰好出现的无关串满足 · 未做更强 provenance 如 span offset);② video_ts 不校回放总时长(语法合法但超时长的偏移不拦)。两者均属『语义完整性深化』非反 mock-pass 结构洞,留待真采集阶段或后续 forge 决定是否加强。"
    status: resolved
  # --- v1.1-reset 重过 codex review 史(12 轮 · 见各轮 /tmp/codex-roundN.txt · operator R11 后收口)---
  v1_1_reset_review_history:
    - round: 1
      verdict: needs-attention
      summary: "verify-ppv-p1 只到 transcript / verify-gate-decision 不管语义 / non-goals 漏扫(改 prose 没改 guardrail · 2 high)"
    - round: 2
      verdict: needs-attention
      summary: "gate-decision 合规检查误查全文(误杀留痕)/ ppv attest 字段可留占位"
    - round: 3
      verdict: needs-attention
      summary: "gate-decision 其余检查仍查全文(--- layout 绕过)/ ppv 下游产物只验存在不验绑定 / RUN-T003 未同步 5 步链"
    - round: 4
      verdict: needs-attention
      summary: "lineage 只在 manifest 元数据 / mtime 信 manifest 自报 / step() 硬编码 exit:0(信任错放 manifest 写入者 · 3 high)"
    - round: 5
      verdict: needs-attention
      summary: "singleton manifest 路径 / 不要求早环 step / run_id 子串匹配可树外冒充"
    - round: 6
      verdict: needs-attention
      summary: "symlink run 目录逃逸 / 不要求 replay_video+extracted_audio artifact"
    - round: 7
      verdict: needs-attention
      summary: "symlink 祖先层(probe-evidence)逃逸 / timestamp_map 可空映射"
    - round: 8
      verdict: needs-attention
      summary: "reachability 两栏 file-level grep(回放段只截图也过 · KG-7 误判漏回)/ video_ts 只验形状"
    - round: 9
      verdict: needs-attention
      summary: "两 verifier replay_entry 全文件抓取(旧/失效 T002 假绑定)/ video_ts 误把 mm<60 一刀切(假阴性回归)"
    - round: 10
      verdict: needs-attention
      summary: "poison 检查误杀模板规则附录(回归)/ 活区内容去重漏 byte-identical poison"
    - round: 11
      verdict: needs-attention
      summary: "timestamp_map 点未绑 summary/transcript(伪造映射)/ replay_entry_canonicalization 未校"
    - round: 12
      verdict: needs-attention
      summary: "[known-gap · 未修] source_ref 子串匹配偏弱 / video_ts 不校回放总时长 —— operator R11 后决议收口"
review_history:
  - round: 1
    reviewer: codex
    verdict: needs-attention
    findings: 4
    summary: "Phase 0 未进 frontmatter / P0-GATE 未把高维护判 no-go / PPV 回放链可 mock-pass / 004 grep 黑名单"
  - round: 2
    reviewer: codex
    verdict: needs-attention
    findings: 3
    summary: "§2.1 仍'v0.1 第一个 task' / P2-P3 仍仅 test-s+schema / SLA-risks O5 仍 grep"
  - round: 3
    reviewer: codex
    verdict: needs-attention
    findings: 2
    summary: "P3 manifest 缺 source_id / architecture 门仍二态"
  - round: 4
    reviewer: codex
    verdict: needs-attention
    findings: 1
    summary: "C10/frontmatter 仍 PASS-only 与 CONDITIONAL-accepted 冲突"
  - round: 5
    reviewer: codex
    verdict: needs-attention
    findings: 1
    summary: "§2.1 标题仍'探针 PASS 后' PASS-only"
  - round: 6
    reviewer: codex
    verdict: needs-attention
    findings: 1
    summary: "SLA:17 P0-GATE row 缺 CONDITIONAL(本轮已修)"
  # --- 以上 R1-R6 = v1.0 frozen 的 review 史(保留作审计留痕)。PRD v1.1 reset 后重 review 史见上方 v1_1_reset_review_history(12 轮)---
  - round: "v1.1-reset"
    reviewer: codex
    verdict: needs-attention-resolved
    summary: "PRD v1.1(forge v1)gate 判准『合规可达』→『自动化稳定性』全改向 + PPV 反 mock-pass 护栏 12 轮硬化(selftest 31→68)· 无 BLOCK · operator R11 后收口 frozen · 残留 2 known-gap 见 D-spec-v1.1-refrozen"
---

# Spec — 008-pB · 投资顾问内容自动采集 → 个人知识库(全形态 · phased)

**Version**: 0.1  **Updated**: 2026-06-05  **Source**: PRD.md(008-pB **v1.1** · forge v1 refactor-and-reset)+ HANDOFF.md(SHARED-CONTRACT §6 v2.0)

> 🔧 **v1.1 reset(2026-06-05)**:本 spec 的 Phase 0 探针判准已从「合规可达性」**改向**「**自动化稳定性 / 低维护恢复**」
> (PRD v1.1 · forge v1 verdict 驱动)。旧判准下的探针 FAIL 结论(回放「合规下不可达」)**已被 operator 证伪作废** ——
> 它把「浏览/截屏可达」误当「采集可达」,且越权把「付费有效登录态抓自己合法流量」误判成「破解访问控制」。
> **合规边界由 operator 负责,不再是探针判准**(C5 已在 PRD v1.1 重定)。详见 frontmatter D-spec-v1.1-reset + DECISION-LOG D9。

> **结论先**:008-pB 是 phased PRD `[v0.1, v0.2]`,**第 0 阶段(可行性探针)是硬门** —— 探针证明
> 「微信小程序图文 + 直播回放用 operator **有效登录态能持续稳定采集**,且登录态失效能低维护恢复(≤ O5b:失效扫码一次),
> 缺口显式可见」且产 P0-GATE =PASS(或 CONDITIONAL 经 operator 显式批准)后,才进 v0.1 主开发。探针 FAIL /
> 未获批准的 CONDITIONAL → 产 `prd-revision-trigger` hand-back 写回 IDS,operator 回 forge / L3 重评工程可行性,**不硬做**。
>
> ⚠️ **两处 operator 授权偏离已锁进 §4 Prior Decisions(D1/D2),agents 不可 re-litigate**:
> ① phase 排序价值优先(回放在 v0.1,非 v0.2);② 回放 v0.1 即做文字摘要(非「存文件不转写」)。

---

## §1 Outcomes

> 分段:`Phase 0(探针)` / `v0.1` / `v0.2`。Phase 0 的产出是 **go/no-go 决策 + 证据**(非可 ship 产品行为);
> v0.1/v0.2 派生 PRD §Success 的 observable outcomes,带量化目标。

### §1.0 Phase 0(可行性探针)Outcomes —— 产出 = go/no-go 决策 + 证据

> 🔧 **v1.1 判准改向**:P0-O1/O2 的判准从「合规可达性(不破解 / 合规下载)」改为「**采集自动化稳定性**」——
> 测的是「operator **有效登录态**能否**持续稳定采集**(非仅浏览/截屏)+ 登录态失效能否低维护恢复」。
> **合规不在探针判准内**(C5 已重定,合规由 operator 负责)。区分「浏览路径」与「采集路径」是本轮硬要求(防旧轮「截屏冒充采集」)。

| # | Outcome(可观察)| 量化 / 判据 |
|---|---|---|
| P0-O1 | **采集自动化稳定性已证**:图文 + 回放在某落点(本机 / 云 / 手机微信)用 operator **有效登录态**能被程序化**持续稳定采集**(拿到**原内容**,非仅浏览/截屏);**证据须分「浏览路径」与「采集路径」两栏**,采集路径才是判准依据 | 产「稳定可采 / 不稳定 / 高维护」三态结论 + 证据(成功**采到**≥1 条真图文原内容 + ≥1 个真回放原文件入口);落点候选≥1 个被证可稳定采集 |
| P0-O2 | **回放采集 + 转录链已证**:用有效登录态拿到一个真实 1-2h 回放原文件 → 抽音频 → ASR 出文本 → 关键点摘要 → **稳定时间戳**溯源,**全链能稳定跑通** | 产「链通 / 断在哪一环」结论;若链通,产出该回放的真实转录文件(≥1 份)+ 每环耗时/维护动作量化 + 关键点→视频稳定时间戳映射可用 |
| P0-O3 | **发布节奏 + 登录态失效频率已观测**:连续观察 1-2 周顾问真实发布(图文/预警/回放各占比、漏哪个最痛、回放频率)+ **token 实际失效频率**(验证 O5b 阈值现实性)| 产观察记录(逐天)+ 三形态计数 + 失效次数/恢复动作量化(对照 O5b) |
| P0-GATE | **go/no-go 决策**(三态,判「能否稳定自动化」非「能否可达」)| 见下「P0-GATE 三态判据」—— 含「可采但高维护(失效恢复 > O5b)」必须判 CONDITIONAL/FAIL,不得仅因「能采到一次」就 PASS |

#### P0-GATE 三态判据(防「采过一次但持续不稳/高维护仍推进主开发」— 判准 = 自动化稳定性,非合规可达性)

> ⚠️ 维护尺子 = **O5b**(PRD v1.1 operator 已拍板,不再由 spec 自定义 `M_ok`):
> 「登录态失效后 operator 介入成本 ≤ **失效时扫码一次**」+ 持续采集期间无因失效导致的静默漏采。
> **不得**探针出结果后再移动成功标准;合规性**不**进判准(C5 已重定,合规由 operator 负责)。

| 判定 | 条件 | 处理 |
|---|---|---|
| **PASS** | P0-O1 = 稳定可采 ∧ P0-O2 = 链通(含稳定时间戳)∧ 登录态失效恢复成本 **≤ O5b**(失效扫码一次)∧ 缺口显式可见 | 进 v0.1 主开发 |
| **CONDITIONAL** | 可采 ∧ 链通,但失效恢复成本 **> O5b**(高维护 / 需频繁人工介入)| **不自动进主开发**:产 hand-back 标 `prd-revision-trigger` → operator 在 IDS 决议(收紧 v0.1 success 阈值 / 重排 scope / 接受降级)→ 显式批准才进 v0.1 |
| **FAIL** | P0-O1 = **无法稳定自动化采集**(持续掉链 / 仅一次性可采)**或** P0-O2 = 链建不起来(下载/ASR/摘要/时间戳任一环稳定跑不通)| 触发 §5 退路(产 `prd-revision-trigger` hand-back),**不进** v0.1;operator 回 forge / L3 重评工程可行性 |

### §1.1 v0.1 Outcomes(派生 PRD O1-O5)

| # | Outcome | How measured(量化)|
|---|---|---|
| O1 | 连续 **2 周**,顾问图文资讯**零漏**(漏/不确定都显式可见,可按天重建「那天发了什么」)| 人工核对 2 周采集记录 vs 实际发布;每个缺口都有显式标记 |
| O2 | 回放被转成**几分钟可消费**的文字 + 关键点;operator **不看完整 1-2h 视频**即可掌握一场直播要点 | operator 主观确认 + 抽查关键点 vs 视频实际内容 |
| O3 | 每个回放关键点能**溯源**回原始转录 + **视频稳定时间戳**(可跳回视频原位复核;C6:LLM 不得发挥成 008 观点)| 抽查关键点的溯源链接可用、**稳定时间戳定位准确**、内容与原始转录对应 |
| O4 | 采集失败/不确定**当天(24h 内)可见**,operator 对「没漏」有信心(C7)| 制造一次采集失败,确认 24h 内缺口可见 |
| O5 | 004 能稳定拿到边界清楚的顾问内容轻量包,且**不误认 008 在给建议** | 004 侧读入测试;输出包**无任何「建议」字段** |
| O5b | ⭐ **登录态失效后 operator 介入成本 ≤「失效时扫码一次」**:token 失效→当天可见提醒→operator 扫码重登 1 次→其余采集全自动,不静默漏。三形态共享同一登录态 → **单一恢复路径**(PRD v1.1)| 观察窗(2 周)内每次 token 失效仅需 1 次扫码;手动介入次数 = token 失效次数;无因失效导致的静默漏采 |

### §1.2 v0.2 Outcomes(派生 PRD O6-O7;阈值待 v0.1 learnings)

| # | Outcome | How measured |
|---|---|---|
| O6 | 连续 2 周,**三形态(图文+回放+预警)全部零漏** | 人工核对 2 周三形态采集 vs 实际发布 |
| O7 | 盘中预警到达有**及时通知**(及时性阈值 `<待 v0.1 后量化>`)| 制造一次预警,确认通知在约定延迟内到达 |

---

## §2 Scope Boundaries

### §2.1 In scope(分 Phase 0 / v0.1 / v0.2)

**Phase 0(探针 · 独立 gate phase,非 v0.1 task)**:
- 采集自动化稳定性探针(图文 + 回放,在候选落点上验证 operator 有效登录态**持续稳定采集原内容** —— **区分浏览路径 vs 采集路径**,采集路径才算数)。
- 回放采集 + ASR 转录链探针(拿真回放原文件走通「下载→抽音频→ASR→摘要→稳定时间戳溯源」,验证全链稳定)。
- 观察顾问 1-2 周真实发布节奏 + **token 失效频率**(验证 O5b 阈值现实性)。
- (合规边界**不**在探针 scope —— 由 operator 负责,C5 已在 PRD v1.1 重定。)

**v0.1**(探针 PASS 或 CONDITIONAL-accepted 后):
- 单一指定顾问的**图文资讯**自动采集(文字为主;**图片只原样留存,不费力解析** — D4)。
- 单一顾问的**直播回放**自动采集 + **转文字 + 关键点摘要**(几分钟可消费;关键点可溯源原始内容 — D2/D3)。
- 轻结构化沉淀(时间 + 标的/主题标签 + 原文/原始转录)。
- **采集失败/不确定状态显式可见**(按天可见缺口),不静默丢失(C7)。
- 按日期/形态/标的检索。
- 给 004 的**轻量输出包**(粗约定:发布时间、形态、原始内容/转录、关键点、涉及标的、采集状态)。

**v0.2**(v0.1 ship + operator 显式启动后):
- 加**盘中预警**自动采集 + **及时通知** → 达成全形态(图文+回放+预警)。
- 统一时间线(三形态合并视图)+ 回放已看/未看状态管理。
- 较完整的 004 输出契约(在 v0.1 粗约定基础上补全)。
- (候选,待 v0.1 反馈后定)更深的结构化检索 / 全文搜索。`<具体范围待 v0.1 反馈后补>`

### §2.2 Explicitly OUT of scope(带 evidence)

**永久 OUT(任何 phase 都不做)**:
| OUT | Evidence |
|---|---|
| ❌ 产生投资建议 / 买卖信号 / 仓位建议 / 收益判断 | PRD §Scope OUT 永久(红线 — 是 004 职责);008 = 004 上游采集模块 |
| ❌ 二次分发 / 公开 / 转售顾问内容 | PRD §Scope OUT 永久(红线 — 仅个人留存,C4)|
| ❌ 规避**他人**访问控制 / 复用**过期失效** token 模拟未授权请求 / 破解付费墙采集**自己无权访问的内容** | PRD §Scope OUT 永久 + **C5 红线**(DMCA§1201 / CFAA)。✅ **对比**:付费订阅用户用**有效登录态**抓自己合法请求返回的图文/回放原文件 = 采集**有权访问**内容,**在 C5 内**(PRD v1.1 · 合规由 operator 负责)|
| ❌ 多顾问 / 多平台通用采集器 | PRD §Scope OUT 永久(C8 单源;008 不是通用工具)|
| ❌ 自动判断顾问观点对错 | PRD §Scope OUT 永久 |

**当前 phase(v0.1)OUT(本 phase 不做,v0.2 会做)**:
| OUT | Evidence |
|---|---|
| ❌ 盘中预警采集 + 及时通知(US7)| PRD §当前 phase OUT;phase 排序价值优先,预警隔离到 v0.2(D1)|
| ❌ 三形态统一时间线 + 回放已看/未看管理(US8)| PRD §当前 phase OUT |
| ❌ 完整 004 输出契约(v0.1 仅粗约定)| PRD §当前 phase OUT |

---

## §3 Constraints

> 直接搬 PRD C1-C9,补 1 条 spec 级(C10)。`Rigidity`:Hard 不可妥协 / Soft 可权衡。

| # | Constraint | Source | Rigidity | Phase scope |
|---|---|---|---|---|
| C1 | v0.1 时间窗 2-3 月内,每周 15-30 小时 | PRD §Real-world constraints C1(L3R0 Block 1)| Soft | v0.1 |
| C2 | v0.2 时间窗待 v0.1 反馈后定 | PRD C2(operator)| Soft | v0.2 |
| C3 | 采集落点(本机 vs 云 vs 手机微信)**未定**,是头号未决,需第 0 阶段探针定 | PRD C3(L3R0 Block 3 + 双模型 R2)| Hard(待定)| both |
| C4 | 永久自用,不商业化 | PRD C4(L3R0 Block 3)| Hard | both |
| C5 | ⭐ **只采 operator 有权访问的内容;可用有效登录态采集原内容**(含须抓包取得的图文/回放原文件),**自用不传播,不规避他人访问控制 / 不复用过期失效 token**。**合规边界由 operator 负责**(spec/探针不替 operator 做法律判断;DMCA§1201 付费自用不天然豁免,operator 已知悉并承担)| PRD C5 v1.1(L3R2 Opus §2/§4 + forge v1 verdict)| Hard | both |
| C6 | **回放关键点必须溯源原始转录**,LLM 不得发挥成 008 自己的观点 | PRD C6(operator 补充 + 红线)| Hard | both |
| C7 | uncertain capture states 一等公民:失败/不确定显式可见,不静默丢失 | PRD C7(L3R2 GPT §5)| Hard | both |
| C8 | 单源:只一个指定顾问 | PRD C8(L3R1 双方)| Hard | both |
| C9 | 不为结构化牺牲原始留存:任何标签/要点可回到顾问原话 | PRD C9(L3R2 双方)| Hard | both |
| C10 | **v0.1 主开发所有 task 入度依赖 Phase 0 探针 PASS 或 CONDITIONAL-accepted**(§1.0 三态判据);探针 FAIL 或未获批准的 CONDITIONAL → 不投主开发 | HANDOFF §0 + PRD §关键前置 gate | Hard | v0.1 |

---

## §4 Prior Decisions(已决,agents 不可 re-litigate)

> 必引 source 节号。**尤其 D1/D2 是 operator 对 stage doc 原始 Candidate B 的授权偏离 —— 以本 PRD 为准,
> 不得回退 stage doc**;D5 探针硬门不可绕。

| # | Decision | Source |
|---|---|---|
| D1 | **phase 排序「价值优先」**:v0.1 = 图文 + **回放**,v0.2 = 加预警(**非**原始 B 的「v0.1 图文+预警 / v0.2 才回放」)| FORK-ORIGIN §「关键:phase 排序按价值优先」+ PRD 顶部偏离 1 |
| D2 | **回放 v0.1 即做文字摘要**(下载→ASR→LLM 关键点),**非**原始 B 的「存文件不转写」| FORK-ORIGIN §operator 补充 1 + PRD 偏离 2 |
| D3 | **回放关键点必须溯源原始转录**(新增红线):LLM 不得发挥成 008 自己的观点 | FORK-ORIGIN §operator 补充 1(新增回放红线)+ PRD C6 |
| D4 | **图片 v0.1 只原样留存,不费力解析**(图片是文字的补充/偶尔搞笑)| FORK-ORIGIN §operator 补充 2 + PRD §Scope IN v0.1 |
| D5 | **第 0 阶段探针是硬门**:探针不过不投 v0.1 主开发;探针证明回放/图文**无法在 O5b 省心阈值内稳定自动化** → 回 forge / L3 重评工程可行性,不硬做。(v1.1:判准为「自动化稳定性」非「合规可达性」;合规由 operator 负责)| HANDOFF §0 + PRD §关键前置 gate v1.1 |
| D6 | 选 Candidate B(全形态)且 phased 降风险(operator 充分知情接受「ambitious and brittle」代价)| FORK-ORIGIN §「为什么选 B 且为什么 phased」|

---

## §5 Task Breakdown(仅 phase 名 + 跨 phase 依赖;细节留 task-decomposer)

> 本节只给 phase 拓扑与依赖,**不写 task 实现**(那是 task-decomposer 的事)。

### Phase 拓扑

- **Phase 0 — 可行性探针**(**独立 gate phase,非 v0.1 内的 task**;frontmatter `gate_phase: phase0-probe`,入度 = 0):验证采集自动化稳定性(图文+回放 · 区分浏览/采集)+ 回放采集转录链(含稳定时间戳)+ 1-2 周节奏+失效频率观察 → 产 P0-GATE 三态决策(PASS/CONDITIONAL/FAIL,§1.0)。**所有 v0.1 task 入度依赖本 phase PASS 或 CONDITIONAL-accepted**(C10);task-decomposer 不得把它拆进 v0.1 phase 或与 v0.1 task 并行启动。
- **v0.1 主开发**(入度依赖 **Phase 0 PASS / CONDITIONAL-accepted** — C10):图文采集 + 回放管线(下载→ASR→LLM 摘要→溯源)+ 缺口显式可见 + 检索 + 004 轻量输出包。
- **v0.2**(入度依赖 **v0.1 ship + operator 显式启动**):加预警采集+通知 + 统一时间线 + 回放已看/未看 + 完整 004 契约。`<v0.2 内部 task 拆分待 v0.1 learnings 后补>`

### ⚠️ 探针 FAIL / CONDITIONAL 退路(显式,spec 一等公民 — per HANDOFF §5 Rollback + dogfood「重大转向必须先 forge,不静默停」)

> 触发条件 = P0-GATE 三态判据(§1.0)的 **FAIL**(无法稳定自动化采集 / 回放链建不起来)**或 CONDITIONAL**(可采但失效恢复成本 > O5b)。
> 两者都不静默推进 v0.1,都产 `prd-revision-trigger` hand-back —— 区别仅在 operator 决议空间(FAIL 回 forge 重评工程可行性;CONDITIONAL 可能收紧阈值/降级后再进)。

```
Phase 0 探针:P0-GATE = FAIL(无法稳定自动化采集 或 回放链建不起来)或 CONDITIONAL(可采但失效恢复 > O5b)
   │
   ├─→ 不进 v0.1 主开发(不在不稳的源头上空耗 2-3 个月 — PRD §缓解②)
   │
   ├─→ parallel-builder 产 hand-back 包(tags: `prd-revision-trigger`)
   │     写回 IDS discussion/008/handback/(走 §6.2.1 6 约束自检)
   │
   └─→ operator 在 IDS 跑 `/handback-review 008` 决议:
         回 forge / L3 重评回放管线工程可行性(在 C1 时间窗内能否如期建成),
         或 `/scope-inject` 改 PRD。**不静默停、不硬做。**
         (v1.1:退路因「工程不可行/高维护」触发,非因「合规不可达」—— 合规已由 operator 负责)
```

---

## §6 Verification Criteria(每 Outcome 一行:可跑命令 / 量化 / 签字)

### §6.0 Phase 0 验证

| Outcome | Verification |
|---|---|
| P0-O1 | ☐ 探针报告产出「稳定可采/不稳定/高维护」三态结论 + 证据文件存在(`ls specs/008-pB/probe-evidence/reachability.md`);证据**分「浏览路径」「采集路径」两栏**;成功**采到**≥1 真图文原内容 + ≥1 真回放原文件入口 |
| P0-O2 | ☐ `bash specs/008-pB/scripts/verify-ppv-p1.sh` PASS(manifest 哈希一致 + source_id 全链一致 + exec log exit 0)+ 「链通/断点」结论 + 关键点→视频稳定时间戳映射可用(人审签字)|
| P0-O3 | ☐ 1-2 周观察记录存在(逐天)+ 三形态计数 + **token 失效频率/恢复动作量化(对照 O5b)** |
| P0-GATE | ☐ 三态决策记录(PASS/CONDITIONAL/FAIL · 人审 checkbox);判据 = §1.0「P0-GATE 三态判据」;CONDITIONAL/FAIL 时 §5 退路已触发(hand-back 产出);**失效恢复成本对照 O5b(失效扫码一次)**,超出不得 PASS |

### §6.1 v0.1 验证(派生 PRD「How measured」)

| Outcome | Verification |
|---|---|
| O1 | 人工核对 **2 周**采集记录 vs 实际发布;每个缺口都有显式标记(量化:0 个未标记缺口)|
| O2 | operator 主观确认「不看完整视频即掌握要点」+ 抽查关键点 vs 视频实际内容 |
| O3 | 抽查每个关键点的溯源链接可用、内容与原始转录对应(量化:抽查样本 100% 可溯源)|
| O4 | 制造一次采集失败 → 确认 **24h 内**缺口可见 |
| O5 | 004 侧读入测试通过;输出包过 **allowlist schema 校验**(§7:只允许声明的采集字段,拒任何未声明顶层/嵌套 key — 非 grep 黑名单),证明无任何建议字段 |

### §6.2 v0.2 验证

| Outcome | Verification |
|---|---|
| O6 | 人工核对 2 周三形态采集 vs 实际发布(零漏)`<阈值/方法待 v0.1 后补>` |
| O7 | 制造一次预警 → 确认通知在约定延迟内到达 `<及时性阈值待 v0.1 后量化>` |

---

## §7 Production Path Verification(PPV)

> XenoDev 必加(防 mock-pass-prod-fail;灵感 autodev_pipe V4 stroller idea004 12 routes 404)。
> **任一必经环节被 mock 即不算 PPV**。
> ⚠️ 008 特殊性:P1/P2 的真证据**由 Phase 0 探针 + v0.1 实装跑出**(探针就是「真路径首跑」)—— spec 阶段给真路径
> 描述 + 可跑命令骨架,**不在 spec 阶段伪造样本**;命令在 Phase 0 / v0.1 ship 时产真证据落 `probe-evidence/` 与 `out/`。
>
> **证据完整性铁律(防「文件存在 ≠ 真路径跑过」)**:PPV 证据不能只验「文件存在/非空」。每条 P_i 必须产一份
> `evidence-manifest.json`,记录:① 源标识(顾问源 + 落点)② 真实时间戳 ③ 全链各产物哈希(原视频 / 抽出音频 /
> 原始转录 / 摘要 / 004 输出包,逐一 sha256)④ 执行日志(各环节命令 + 退出码)。验证命令校 manifest 字段齐
> **且**各哈希与实际落盘文件一致 —— 哈希对不上 = 证据是预置样本 = 不算 PPV。

| P# | 起点(真路径)| 必经环节(逐个列,任一 mock 即不算)| 终点(真持久化)| 验证命令 |
|----|---|---|---|---|
| **P1**(回放真路径 · 强制全链贯穿,**不可被图文路径替代**)| operator **有效登录态**访问指定顾问微信小程序源(本机/云/手机微信落点之一)| 源接入(有效登录态采集原文件,**采集路径非浏览路径** · 合规由 operator 负责)→ 拿 **1 个真回放入口** → 下载真回放原文件 → 抽音频 → ASR 转文本 → 落原始转录 →(v0.1 加)LLM 关键点摘要 → 溯源原始转录 + **视频稳定时间戳**。**同一条真实回放必须贯穿全链**(下载/抽音频/ASR/摘要/溯源同一 source_id),不得各环节用不同来源拼接 | `probe-evidence/run-<run_id>/{transcript,summary,timestamp-map,...}-<source_id>.*`(v1.1:run-scoped 路径,防陈年文件复用)+ `probe-evidence/evidence-manifest.json`(含 source_id/ts/各产物 sha256/真实 exit log)| Phase 0/v0.1 探针脚本(operator paste 跑)→ `bash specs/008-pB/scripts/verify-ppv-p1.sh`:校 manifest 存在 ∧ source_id 全链一致 ∧ 各 sha256 与落盘实际匹配 ∧ artifact 在 `run-<run_id>/` 下 ∧ **真实文件系统 mtime**(非 manifest 自报)同窗 ∧ exec log 各环节**真实** exit 0 ∧ **summary/timestamp_map 必经且 lineage 从 artifact 字节解析绑本链 transcript/回放**(任一不符 → exit 1)|
| **P2**(回放摘要 → 004 真路径 · **强制走回放支线**,起点**只能**是 P1 产出的真回放摘要)| **P1 产出的**真回放关键点摘要(带溯源)| 轻结构化(时间+标的+原始转录引用)→ 写 004 轻量输出包(schema 见下 allowlist)| `out/004-feed/replay-<source_id>.json` + `out/004-feed/manifest-replay-<source_id>.json`(输入摘要 sha256 + 输出 JSON sha256 + source_id + gen 命令 + exit code)真文件落盘 | `bash specs/008-pB/scripts/verify-ppv-p2.sh`:`test -s` ∧ **allowlist schema 校验** ∧ manifest 输入 sha256 == P1 摘要实际哈希 ∧ manifest 输出 sha256 == 落盘 JSON 实际哈希 ∧ source_id == P1 manifest source_id ∧ gen exit 0(任一不符 → exit 1;**不接受仅 test -s/schema/source_id**)|
| **P3**(图文 → 004 真路径 · 较轻,**不可替代 P2**)| 一条已采集的真图文(v0.1 产物,带采集记录 source_id)| 轻结构化(时间+标的+原文)→ 写 004 轻量输出包 | `out/004-feed/article-<source_id>.json` + `out/004-feed/manifest-article-<source_id>.json`(**source_id** + 输入图文 sha256 + 输出 JSON sha256 + gen 命令 + exit code)真文件落盘 | `bash specs/008-pB/scripts/verify-ppv-p3.sh`:`test -s` ∧ allowlist schema 校验 ∧ manifest 输入 sha256 == 源图文实际哈希 ∧ manifest 输出 sha256 == 落盘 JSON 实际哈希 ∧ **manifest source_id == 源图文采集记录 source_id == 输出 JSON source_id**(证明输出来自同一真实采集源,非预置/错源)∧ gen exit 0(任一不符 → exit 1)|

**004 输出包边界校验 = allowlist schema(非 grep denylist)**:
> 004↔008 是信任边界,「无建议字段」不能靠关键词黑名单(挡不住 `recommendation`/`signal`/`action`/嵌套决策提示)。
> 改为 **allowlist**:只允许显式声明的采集字段,**拒绝任何未声明字段 + 未声明嵌套结构**。
- 允许字段(v0.1 粗约定):`published_at` / `form`(article|replay)/ `raw_content` / `transcript_ref` / `key_points[]`(每项含 `text` + `source_ref` 溯源)/ `tickers[]` / `capture_status`(captured|uncertain|failed)/ `source_id`。
- 校验脚本断言:输出包**顶层 + 嵌套**所有 key ∈ 允许集合;出现任何集合外 key(如 `recommendation`/`signal`/`action`/`buy`/`sell`/`仓位`/`target_price`/`收益`/...)→ exit 1。
- ⚠️ allowlist 实现(`scripts/004-schema.json` + 校验器)是 v0.1 task 产物;spec 阶段定契约,不伪造样本。

**反 PPV(直接拒)**:
- ❌ 「回放下载用 mock URL / 预录样本」→ P1「下载真回放→抽音频→ASR」必经环节被 mock,不算 PPV。
- ❌ 「用图文路径(P3)完成唯一下游落盘,跳过回放链(P1→P2)」→ P2 强制 source_id 来自 P1 回放 manifest,图文链顶替直接 fail。
- ❌ 「只验文件存在/非空」→ 必须校 evidence-manifest 哈希与实际落盘一致(防预置样本)。
- ❌ 「004 边界用 grep 黑名单」→ 必须 allowlist schema 校验(拒未声明字段)。
- ❌ 「004 输出包只在 stdout / log 显示」→ 终点必须真文件落盘。
- ❌ 「unit test 通过即算 PPV」→ unit test mock 一切,不验真路径。

---

## Glossary

- **落点(采集落点)**:008 实际运行 + 采集的宿主环境(本机 / 云服务器 / 手机微信),C3 头号未决,Phase 0 探针定(判准 = 自动化稳定性)。
- **浏览路径 vs 采集路径**(v1.1 关键区分):**浏览路径** = operator 人眼正常浏览/截屏能看到(≠ 程序能采到原内容);**采集路径** = 程序用有效登录态拿到**原文件/原内容**(图文原文 / 回放视频文件)。探针判准只认采集路径——「浏览可达」不等于「采集可达」(旧轮误判根因)。
- **图文资讯**:顾问每天发的以文字为主、图片少的资讯(US1)。
- **直播回放**:顾问每周几次发的 1-2h 视频(重要消息 + 周度复盘 + 下周策略展望),v0.1 做下载→ASR→摘要(D2)。
- **盘中预警**:顾问不定时发的有时效的关键预警(US7,v0.2)。
- **004 输出包**:008 给下游 004 投资决策智能体的轻量结构化数据包(无任何投资建议字段)。
- **溯源(关键点溯源)**:回放摘要的每个关键点能回到原始转录文本/视频位置(C6/C9)。
- **uncertain capture state**:采集「待确认/未能确认」状态,与「已收」分开显式可见(C7),是「不漏」的真正实现。

## Open Questions for Operator

> 这些是 build 路径选择的 OQ(承载自 HANDOFF §4),**自然遇到时再解决,不污染 spec frozen**。

- ⭐ **采集落点(本机 vs 云 vs 手机微信)**:Phase 0 探针后由 operator 拍板。三者须同时满足「**持续稳定可采(采集路径)** + 低维护(失效恢复 ≤ O5b)」。GPT R2 提醒「云不是显然的可靠答案」。(合规已不是判准 —— C5 重定,operator 负责。)
- **回放管线工程可行性**:有效登录态下能否拿到 1-2h 视频原文件 → ASR → LLM 摘要 → **稳定时间戳**,且**稳定跑通/低维护**。Phase 0 探针重点;FAIL → §5 退路。(v1.1:合规可达已不是 open question。)
- ✅ **维护尺子已由 PRD v1.1 拍板 = O5b(失效扫码一次)**,spec 不再自定义 `M_ok`。探针对照 O5b 判 PASS/CONDITIONAL,**不得探针出结果后再移动**。
- **v0.2 待定**:盘中预警与图文/回放是否**同源同渠道**(决定 v0.2 加预警成本;若不同源,v0.2 工作量接近重做一套采集,需重排 v0.2 scope)。
- **v0.1 高频消费形态**(回放摘要 vs 图文,US1 vs US2)→ 决定 v0.2 资源倾斜。
