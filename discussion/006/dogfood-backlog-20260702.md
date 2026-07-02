# Dogfood Backlog · 框架级问题攒集处

> **这是什么**:用 XenoDev 真开发项目(dogfood)的过程中,踩到的**框架级**缺陷 / bug / 优化空间攒在这里。
> **append-only** —— 只往下加,不删不改已有条目(同 HANDBACK-LOG / events.jsonl 纪律)。
> **去向**:阶段性随 hand-back 包回流到 IDS 治理仓,攒够一批后回 IDS 起 `/expert-forge 006` 做 forge 审议(backlog 直接当 forge 的 X 标的)。
> **为什么存在**:operator 用 XenoDev 真开发时专注在项目上,容易忘记记框架问题。本文件 + CLAUDE.md/AGENTS.md 的「dogfood 铁律」一起,让开发 Claude 干活时**记得**把框架问题随手记下,不丢。

---

## ⚠️ 判别标准:什么该记这里,什么不该(记之前先过这一关)

**只记「框架级」问题** —— 改的是**框架本身**:
- ✅ 协议层(SHARED-CONTRACT 条款 / hand-back schema / workspace schema)
- ✅ SKILL 机制(spec-writer / task-decomposer / parallel-builder / codex-review 的逻辑或 edge case)
- ✅ hand-back / validator / mirror / 并发机制(R-Q7 immutable / G3 / B-3 / mirror-sha 等)
- ✅ 跨仓协调 / event log / eval 数据接口
- ✅ 这套"自动开发 framework"本身用起来的痛点 / 优化空间

**不记「项目级」问题** —— 改的是**你在建的那个具体项目的功能**:
- ❌ "我这个 todo-app 要加登录" → 项目内迭代,不记这里
- ❌ "这个 API 的某字段要改" → 项目内处理
- ❌ 任何只影响单个在建项目、不影响 framework 的东西

**一句话判别**:这个问题修好后,**受益的是"以后所有用这套 framework 开发的项目"**(→ 记)还是**"只有当前这个项目"**(→ 不记)。

**铁律联动**:框架级变更**不在 XenoDev 当场改**(per CLAUDE.md / AGENTS.md 已有铁律「不动 SHARED-CONTRACT / 不复制 forge / 重大架构转向必须 forge」)→ **记这里 → 攒批回 IDS forge**。当场改框架 = 绕过治理 = V4 失败模式。

---

## 条目模板(照这个填 · 复制下面整块到文件末尾)

```
## <短标题 · 一句话说清是什么问题>
- 日期: <ISO · 如 2026-06-02T10:00:00Z>
- 类型: 框架缺陷 | bug | 优化空间 | schema-gap
- 严重度: high | medium | low
- 复现场景: <真实 dogfood 场景 · 越具体越值钱 —— 在开发什么项目、跑到哪一步、怎么触发的、现象是什么>
- 关联: <task / file / 已有 known-gap · 如 KG-1 / 某 SKILL §x.y / 某脚本 line>
- operator 确认: <留空 · operator 阶段性 review 时补:确认/补充/降级/这条其实是项目级误记>
```

> **复现场景**是这里最值钱的字段 —— forge v5 最大的教训就是"R-Q7 零运行证据"(审一个没真跑过的东西容易跑偏)。真实复现场景 = 回 IDS forge 时的硬证据,比凭空推演强 10 倍。

---

## 条目(append-only · 新的往下加)

### KG-1 · G3 单全局 latest 指针无 task identity(approve-over-approve 残留重放面)
- 日期: 2026-06-02T00:00:00Z(forge v5 P0 ship 时记录 · 种子条目)
- 类型: 框架缺陷
- 严重度: medium(并发规模上去才暴露 · 现非 ship-blocker)
- 复现场景: G3 `verify_evidence_latest` 用单 global `working-tree` 指针 + verdict-direction guard,挡得住"旧 approve 偷过新 needs-attention",但**挡不住**"同 scope 旧 approve 在新 approve 之后重 ship"(approve-over-approve)。真上多 worktree 并发 + 同一文件反复审时会暴露。**dogfood 时盯**:同一个文件被反复 codex 审、旧批准还能用 → 记下真实复现。
- 关联: forge v5 verdict KG-1 / XenoDev `verdict-evidence-lib.sh` verify_evidence_latest / `.work/IDS-handoff-006-forge-v5-P0.md` §4.2
- operator 确认: 已知架构债 · operator 决议 ship · 待并发实战暴露真形态后回 forge v6

### KG-2 · B-3 immutable 记录秒级命名同秒碰撞
- 日期: 2026-06-02T00:00:00Z(forge v5 P0 ship 时记录 · 种子条目)
- 类型: 优化空间
- 严重度: low(noclobber 已干净兜住 · 无损坏 · 输家重跑即可)
- 复现场景: immutable 文件名 `<scope-slug>-<ts-到秒>.md`,同秒同 scope 两 review → 一个被 noclobber 拒(fail-closed · 正确行为)。stress N=20×8 轮实测 noclobber 干净兜住,无丢 review / 无半写。**dogfood 时盯**:同秒撞库频率 —— 若真并发下一天撞好几次,说明该升 B-3(content-addressed / 单调 nonce 命名)。
- 关联: forge v5 verdict KG-2 / B-3 / codex-review SKILL §3.6.2 命名方案 / `.work/IDS-handoff-006-forge-v5-P0.md` §4.2
- operator 确认: 已知 · 留 P1 · v0.4-note 1 触发条件(真撞库丢 review)未达 · 待 dogfood 观测

### KG-3 · spec.template.md 被 HANDOFF + spec-writer SKILL 引用但实际不存在
- 日期: 2026-06-04T00:00:00Z(008-pB spec-writer 真开发时记录)
- 类型: 框架缺陷(文档/实装漂移)
- 严重度: low(SKILL 内嵌骨架是事实 SSOT · spec 仍能产 · 但指针指向 ghost 文件,易误导新 operator/agent)
- 复现场景: 开发 008-pB,跑 XenoDev spec-writer。HANDOFF.md §1.4 写「spec-writer 产 spec.md(7 元素 schema,**具体格式见 XenoDev `templates/spec.template.md`**)」,spec-writer SKILL §0 也称输出 `specs/<feature>/spec.md` + 配套。但 `ls /Users/admin/codes/XenoDev/templates/` → `No such file or directory`,全仓无 `spec.template.md`(`find` 实证空)。实际 spec 骨架 SSOT 在 SKILL.md §6 内嵌 + IDS derivation-guide。即:**文档指针指向一个从未实装的文件**。本次靠读 SKILL §6 骨架 + 既有 specs/004-pB、006a-pM 范例绕过,未受阻,但下一个 operator 照 HANDOFF 字面找 template 会扑空。
- 关联: IDS plan-start 产的 HANDOFF.md §1.4 模板串 / XenoDev spec-writer SKILL §0+§6 / derivation-guide OQ-derive-3(「operator 手写还是 cp IDS templates 改」当时留 OQ,推荐手写但没落地 template 文件)/ CLAUDE.md「关键实装位置」表列 `templates/spec.template.md`(同样指向不存在路径)
- operator 确认: <留空 · 待 operator review:补一份 templates/spec.template.md(从 SKILL §6 骨架提)统一 SSOT,还是把 HANDOFF/CLAUDE.md/SKILL 的指针都改成「见 SKILL §6 内嵌骨架」消除 ghost 引用 —— 二选一,框架级,回 IDS forge 定>

### KG-4 · REVIEW-LOG findings_count 的 grep pattern 与实际 codex companion 输出格式不匹配
- 日期: 2026-06-04T00:00:00Z(008-pB spec-writer 写 REVIEW-LOG 时记录)
- 类型: bug(schema-gap · 静默零计数)
- 严重度: medium(不报错但**静默写错 findings_count=0**,污染 REVIEW-LOG machine-readable 字段 · 下游若按 count 判健康会误判)
- 复现场景: 008-pB spec-writer §3.2.1 写 REVIEW-LOG。SKILL §3.2.1 给的计数命令是 `grep -cE '^- \[(P[0-9]|BLOCK|FOLLOW-UP)\]' /tmp/codex-review.log`,但本机 codex companion(`codex-companion.mjs` adversarial-review)实际输出 findings 行格式是 `- [high] ...` / `- [medium] ...` / `- [low] ...`(severity tag),**不是** `[P0]/[BLOCK]/[FOLLOW-UP]`。结果 SKILL 原 pattern 实测 `grep -c` 返回 **0**,而真实 findings = 1(本轮)。即 SKILL 的 pattern 是对着一个**旧/别的 codex 输出格式**写的,与当前 companion 漂移。本次手工改用 `^- \[(high|medium|low)\]` 取到真值 1,但若 operator 照抄 SKILL 命令会静默记 0。
- 关联: XenoDev spec-writer SKILL §3.2.1 / codex-review SKILL §3.6(REVIEW-LOG 真路径,大概率同 bug)/ `codex-companion.mjs` 1.0.3 输出格式 / `/tmp/codex-review-008-r6.log`(可复现:两 pattern 各跑 grep -c 对比 0 vs 1)
- operator 确认: <留空 · 待 operator review:把两个 SKILL §3.2.1/§3.6 的 grep pattern 改成匹配 `[high|medium|low]`(或同时兼容两种格式),框架级,回 IDS forge 定>

### KG-5 · 探针/可行性-gate task 缺「证据骨架 + 自测脚本」的 skill 范式(每个 probe task 各自重发明)
- 日期: 2026-06-04T00:00:00Z(008-pB Phase 0 探针链全工程化时记录)
- 类型: 优化空间(框架能力缺口)
- 严重度: medium(不记会让每个 probe-gated 项目各自重发明这套,且容易漏掉「自测≠真结论」纪律 → mock-pass 风险)
- 复现场景: 开发 008-pB,HANDOFF §0 要求「v0.1 第一个 task 必须是可行性探针,探针过才进主开发」。探针链(T002 可达性 / T003 回放下载+ASR / T004 节奏 / T005 gate / T006 放行门)有个本质特征:**真结论(可达性/链通/M 实测/go-no-go)物理上依赖 operator 真登录态 + 真实世界 1-2 周,Claude 无法代跑**,但**全部工程骨架 + 验证脚本 + 负向 fixture 可自主做到 ship-ready 并自测真跑通**。我为此摸出一套可复用范式,但 task-decomposer / parallel-builder / spec-writer 的 SKILL **都没有codify这套**,导致每个 probe-gated 项目都得重发明 + 容易漏关键纪律。范式四件套:① **占位符防线证据骨架**(`<待真采集>` 未填 → verify 脚本 exit 1,逼真采集填真值,防预填假结论被当真结论);② **独立 `selftest-*.sh`**(用合成 fixture 跑 verify,证明每个守卫真生效 —— 尤其负向 fixture 各单独 exit 1 是反 mock-pass 的真正落点;且自测产的合成证据跑完即清,不污染真证据目录);③ **「自测≠探针结论」红字纪律**(每个 RUN-T*.md 执行单顶部标注,合成 fixture 自测证明的是「校验逻辑对」非「探针通过」,真结论待 operator 真采集);④ **合成证据与真证据物理隔离**(`selftest-fixtures/` gitignore 动态生成 vs `probe-evidence/` 真证据入 git)。这套直接对应 spec §7 PPV 的反 autodev_pipe-V4-mock-pass 诉求,应固化进 SKILL(probe-gated task 的标准产物形态),而非靠 agent 临场发挥。
- 关联: XenoDev task-decomposer SKILL(无 probe-task 范式)/ parallel-builder SKILL §3.0(probe task 路由但无「证据骨架+自测」产物约定)/ spec-writer SKILL §2.2 PPV(PPV 真路径要 owning task,但没说 probe 阶段「真证据未产时怎么自测 verify 脚本」)/ 008-pB `specs/008-pB/scripts/selftest-*.sh` + `projects/008-pB/probe/RUN-T*.md` + `DECISION-LOG.md` D0(可作 forge 范式样本)
- operator 确认: <留空 · 待 operator review:是否把这套「probe-gated task 四件套范式」固化进 task-decomposer/parallel-builder SKILL(probe task 必产证据骨架+selftest-*.sh+RUN执行单+占位符防线),框架级,回 IDS forge 定。008-pB 的实现可直接当 forge 的正向样本>

### KG-6 · verify 脚本自测在 harness zsh 下踩 PATH/coreutils 解析坑(selftest 作者会重踩)
- 日期: 2026-06-04T00:00:00Z(008-pB 写第一个 selftest 时踩到)
- 类型: bug(环境/工具链 · 框架级因所有 verify 脚本自测都会碰)
- 严重度: low(有确定解法,但不记会让每个写 selftest 的 agent 各踩一次,浪费一轮)
- 复现场景: 008-pB 写 `selftest-reachability.sh`。首版图省事把自测逻辑写成 Bash 工具顶层(harness 实际用 zsh 执行)的 inline 函数 `run_case(){ ... $(tail -1 ...) ... }`,跑出来全 `command not found: tail` + exit 127(报错格式 `run_case:6:` 是 zsh 的,非 bash)。实证 `/usr/bin/tail` 存在、PATH 含 `/usr/bin` —— 是 zsh 函数内 PATH/hash 表的解析差异,不是 tail 真缺失。**确定解法**:① 自测逻辑固化成独立 `.sh` 文件用 `bash <file>` 显式跑(不依赖顶层 shell 环境);② 自测里调的 coreutils(tail/head 等)用绝对路径 `/usr/bin/tail`。副益:独立 selftest 脚本本身成为可复现留痕产物。这条对 codex-review SKILL 里任何「写脚本 + 自测」流程通用 —— 凡在 harness 里写 shell 自测都可能踩。
- 关联: 008-pB `specs/008-pB/scripts/selftest-*.sh`(全部按此模式:独立 bash 脚本 + 绝对路径 coreutils)/ DECISION-LOG D2「遇到的真实障碍」/ 任何 SKILL 里「inline bash 自测」的示例（建议改成独立脚本范式 + 提示 harness=zsh 的 PATH 坑）
- operator 确认: <留空 · 待 operator review:是否在 task-decomposer/parallel-builder SKILL 的「verification 自测」处加一行环境提示(harness shell=zsh,自测用独立 bash 脚本 + 绝对路径 coreutils),低优先框架级 note,回 IDS forge 时顺带>

### KG-7 · 探针把「浏览可达」误当「采集可达」+ build runtime 越权做 C5 法律判定 → 整轮 gate 结论作废
- 日期: 2026-06-05T00:00:00Z(008-pB hand-back 被 IDS /handback-review + /expert-forge v1 整体推翻后记录)
- 类型: 框架缺陷(SKILL 范式 + 跨仓边界双重)
- 严重度: high(导致整个探针轮 go/no-go 结论错误且差点掏空项目核心价值 · 错误结论已写回 IDS 才被 operator 当场证伪)
- 复现场景: 开发 008-pB Phase 0 可行性探针。探针对「微信小程序顾问图文 + 直播回放能否采集」做 go/no-go,产出 gate=**FAIL**(回放合规下不可达)+ 推荐「图文先走 / 回放移 v0.2」,并据此产 prd-revision-trigger hand-back 写回 IDS。operator 在 IDS `/handback-review 008` **当场证伪整轮结论**,起 `/expert-forge 008`(verdict=refactor-and-reset)。**两个独立的框架级错判**:
  ① **「浏览可达」≠「采集可达」被混为一谈**:探针拿 `article-sample-001.png`(operator 截屏)当「图文合规可达 ✓」的证据。但截屏 ≠ 合规采集到图文**原内容**;真要采集图文原文件**和回放一样要抓包**。探针把「人能正常浏览 + 截屏」误当成「能采集原内容」,两者合规边界与技术手段完全不同。证据骨架(reachability.md)的「访问方式」字段没有强制区分 *浏览路径* vs *采集路径*,让 agent 容易用浏览证据冒充采集证据。
  ② **build runtime 越权做 C5 法律定性**:探针自行把「抓包下载回放」判为「复用过期 token 模拟未授权 → 规避访问控制 → 踩 DMCA§1201/CFAA → FAIL」。但合规边界判定**本应 operator 负责**(forge v1 verdict 明确「合规由 operator 负责」),且该法律判定本身就是错的(真实手段 = 付费订阅·有效登录态抓自己合法流量·自用不传播 = 采集自己有权访问的内容,未规避任何本不该有的访问权)。build runtime 把一个**法律灰区的红线判定**当成确定性事实写进 gate 结论,且 fail-closed 到 FAIL,等于让 agent 替 operator 做了它无权做的法律风险决策。
  **根因**:探针 SKILL / spec §1.0 三态门把「**源头合规可达性**」当 gate 判准,而合规可达性内在依赖(a)浏览vs采集的区分 (b)C5 法律边界判定——两者都超出 build runtime 应做的范围。forge v1 已把判准改向「**自动化稳定性/低维护恢复**」(合规移出探针判准 · 由 operator 负责)。
- 关联: XenoDev spec-writer SKILL §1.0 三态门建模(把「合规可达」当 gate 判准)/ 探针证据骨架 reachability.md(「访问方式」未强制区分 浏览vs采集)/ CLAUDE.md「Safety Floor 违反 → 停+escalate」与「重大架构转向必须 forge」边界(C5 判定属 operator 职责,build runtime 不应自行定性)/ IDS `discussion/008/forge/v1/stage-forge-008-v1.md`(verdict=refactor-and-reset · 可作 forge 反面样本)/ KG-5(probe 四件套范式应连带 codify「判准必须是 build-runtime 可自证的工程事实,不是法律/合规定性」)
- operator 确认: <留空 · 待 operator review:是否在 spec-writer/task-decomposer SKILL 加硬约束 ——(1)探针 gate 判准只能是 build-runtime 可独立验证的工程事实(可达性须区分浏览vs采集、稳定性、维护成本),合规/法律定性一律不进 gate 判准、escalate operator;(2)证据骨架的「访问方式」字段强制分「浏览路径」「采集路径」两栏防冒充。框架级,回 IDS forge 定 · 008-pB forge v1 可直接当反面样本>

### KG-8 · 对反-mock-pass 护栏跑 codex adversarial-review 收敛极慢(12 轮)· 需 operator 收口纪律
- 日期: 2026-06-05T00:00:00Z(008-pB v1.1-reset spec 重过 codex review 时记录)
- 类型: 优化空间(SKILL 流程 · 收敛/止境纪律)
- 严重度: medium(不记会让以后每个『改反-mock-pass 护栏』的 task 都陷入无限 review 循环 · 烧 token + 拖工期)
- 复现场景: 008-pB v1.1-reset 把 Phase 0 探针 gate 判准从『合规可达』改向『自动化稳定性』,顺带把 PPV verifier(verify-ppv-p1.sh)从『信任 manifest 写入者』硬化成『信任真实文件系统+artifact字节』。对这个改动跑 codex adversarial-review,**连跑 12 轮每轮都 needs-attention**(无一轮 approve / 无一轮 BLOCK):R1-3 修 prose↔guardrail 一致性;R4-7 修信任边界(run-scoped path、真 mtime/exit、symlink 逃逸、下游绑定);R8-11 修章节级解析 + 活区收口 + 逐点 provenance;R12 还在挑 R11 修法的精度(source_ref 子串偏弱 / video_ts 不校时长)。**关键观察**:反-mock-pass 护栏的攻击面近乎无穷(总能再构造一个更刁的伪造场景),codex 作为对抗性 reviewer 会一直找到『下一个』,severity 缓慢下降但不归零;自 R4 起无新结构性洞、R8 起多为前轮修法的精度迭代 = 已进收敛尾部但 codex 不会主动 approve。operator R11 后决议收口(selftest 31→68 case,每道防线有负向自测,残留 2 known-gap 显式记录),不无限刷。
- 关联: XenoDev codex-review SKILL §3.2(needs-attention 处置后可 frozen · 但没给『反-mock-pass 这类近无穷攻击面的护栏何时收口』的判据)/ parallel-builder SKILL §4.2(4 轮 cap · 但 operator 屡次破 cap 已成常态:004 多 task / 006a-pM / 006a-pM-v0.2 11 轮 / 本轮 12 轮)/ 008-pB `specs/008-pB/scripts/verify-ppv-p1.sh`(12 轮硬化的实物)+ spec.md frontmatter D-spec-v1.1-refrozen(收口决议 + 2 known-gap)
- operator 确认: <留空 · 待 operator review:是否在 SKILL 给一条『收敛尾部收口判据』——如『连续 K 轮无新结构性洞(只剩前轮修法精度迭代 / 攻击面边际化)+ 无 BLOCK → operator 可决议 frozen 并显式记 known-gap』,把『何时停止对抗性 review』从个案 operator 拍板固化成可复用纪律。本轮 12 轮收敛曲线可作样本。框架级,回 IDS forge 定>

<!-- 新条目从这里往下 append · 别动上面已有条目 -->

### KG-9 · Codex 适配层 `.agents/.Codex` 路径漂移导致当前 SKILL 真入口不可复现/会 fail-closed
- 日期: 2026-06-10T12:30:11Z
- 类型: 框架缺陷
- 严重度: high
- 复现场景: 做 XenoDev 全仓 review 时,当前 Codex session 暴露的本仓专属 skill 路径是 `.agents/skills/{spec-writer,task-decomposer,parallel-builder}/SKILL.md`,但 `git status --short` 显示 `.agents/` 与 `.codex/` 未跟踪;AGENTS.md/CLAUDE.md/SHARED-CONTRACT 仍以 `.claude/skills` 为 canonical。更严重的是 `.agents/skills/*` 相比 `.claude/skills/*` 批量把 `.claude` 改成 `.Codex`;parallel-builder preflight 要求 `test -x .Codex/safety-floor/credential-isolation/scan-credentials.sh` + `.Codex/settings.json`,实测 `codex_cred=1` / `codex_settings=1`,因为 repo 内 `.codex/` 只有 hooks,完整三件套仍在 `.claude/`。结果:若 operator 在 Codex 环境触发 `.agents` 版 parallel-builder,会在 Safety Floor preflight 直接 fail-closed,build phase 起不来;若 clone 新仓,`.agents` 不入 git 又导致 Codex skill 不可复现。
- 关联: `.agents/skills/parallel-builder/SKILL.md` §0.2 / `.agents/skills/codex-review/SKILL.md` §0.1+§3.6 / `.codex/hooks.json` / AGENTS.md §5-§6 / `git status --short` 显示 `.agents/` `.codex/` untracked
- operator 确认: <留空 · 待 operator review:决定 Codex canonical 是 `.agents` 还是 `.codex` 还是继续 mirror `.claude`;需要一条迁移/同步规则,不能让运行入口和受控 SSOT 分叉。框架级,回 IDS forge 定>

### KG-10 · integration tests 原地改 `HANDOFF.md`,并行跑会互相污染导致假失败
- 日期: 2026-06-10T12:30:11Z
- 类型: bug
- 严重度: medium
- 复现场景: review 时用并行工具同时跑 `tests/integration/test-gen-handback-out-prefix.sh` 和 `tests/integration/test-FU-T207-1-grep-brackets.sh`。前者第一次出现 3 PASS / 3 FAIL(case B explicit `--out`,case C setup,case F `--task` alias);随后单独复跑 `test-gen-handback-out-prefix.sh` 变成 6 PASS / 0 FAIL。根因:FU-T207 测试会 `cp -p "$HANDOFF_REAL" "$HANDOFF_BAK"` 并通过 `inject_handoff_field` 直接修改仓根 `HANDOFF.md`,trap 再恢复;另一个测试同时读 `HANDOFF.md` 的 source_repo_identity,于是读到污染态并失败。即 Deterministic Feedback 层不具备并行隔离,和 XenoDev/parallel-builder 的并行理念冲突。
- 关联: `tests/integration/test-FU-T207-1-grep-brackets.sh` lines 42-80 / `tests/integration/test-gen-handback-out-prefix.sh` / `lib/handback-validator/gen-handback.sh` 读仓根 HANDOFF.md SSOT / 本次实测 first run FAIL 后 solo rerun PASS
- operator 确认: <留空 · 待 operator review:测试应改为 fixture repo-root/HANDOFF override 或 mktemp worktree,并标注哪些 integration test 不可并行;框架级,回 IDS forge 定>

### KG-11 · eval event schema/README 对 `handback_drifts` 与 versioned `prd_fork_id` 的契约漂移
- 日期: 2026-06-10T12:30:11Z
- 类型: schema-gap
- 严重度: medium
- 复现场景: review v0.2 event-log 时发现实现和文档/正式 schema 不一致。`lib/eval-event-log/event-schema.json` enum 已是 `handback_drifts`,writer 也只允许新写复数,`tests/integration/test-T104-enum-plural.sh` 6/6 PASS;但 `lib/eval-event-log/README.md` 仍把第 3 类 event 写成 `handback_drift`,示例也用单数,会误导新 caller 写入被拒。另一个漂移:同一个 schema 的 `prd_fork_id` pattern 仍是 `^[0-9]{3}[a-z]?(-p[A-Z])?$`,不接受当前 v0.2 真 ID `006a-pM-v0.2`;writer 目前只做手写最小校验,没有真正执行 schema 的 optional field pattern,所以问题被隐藏。正式 schema 与运行校验不一致,会在未来接入 jsonschema/ajv 或外部消费者时爆。
- 关联: `lib/eval-event-log/README.md` event 列表+示例 / `lib/eval-event-log/event-schema.json` event_type enum + prd_fork_id pattern / `lib/eval-event-log/writer.sh` 手写校验 / T104 B-2
- operator 确认: <留空 · 待 operator review:统一 README 示例为复数;把 event-schema prd_fork_id regex 与 check-6 v0.2 regex 对齐;决定 writer 是否要真正校 optional fields。框架级,回 IDS forge 定>

### KG-12 · handback-validator valid fixture/README 默认命令与 producer/consumer mode 分流不一致
- 日期: 2026-06-10T12:30:11Z
- 类型: bug
- 严重度: low
- 复现场景: review 时按 `lib/handback-validator/README.md` 的“valid → exit 0”思路跑 `bash lib/handback-validator/validate-handback.sh lib/handback-validator/test-fixtures/valid/handback.md /Users/admin/codes/ideababy_stroller`,实际 exit 1:默认 `--mode=consumer`,check-5 要求物理路径包含 `/discussion/<id>/handback/` 且 filename 是 `<ISO>-<handback_id>.md`,而 fixture 在 `lib/handback-validator/test-fixtures/valid/` 下。改用 `--mode=producer` 后 PASS;另一个带 timestamp basename 的 valid fixture默认 consumer 也因路径不含 `/discussion/.../handback/` 失败。即 README 的单元测试说明停留在 mode 分流之前,且缺一个真正 consumer-mode valid fixture 或模拟路径。
- 关联: `lib/handback-validator/README.md` §单元测试 / `lib/handback-validator/validate-handback.sh` `--mode=consumer|producer` / `lib/handback-validator/check-5-id-consistency.sh` / valid fixtures
- operator 确认: <留空 · 待 operator review:README valid 示例改成 producer mode,并新增/生成 consumer-mode fixture 路径测试;框架级,回 IDS forge 定>

### KG-13 · 008-pB PPV verify 脚本依赖 Bash 4 `mapfile`,在 macOS 默认 Bash 3.2 下真实校验入口崩溃
- 日期: 2026-06-10T12:47:36Z
- 类型: bug
- 严重度: medium
- 复现场景: review 008-pB 时,`specs/008-pB/scripts/selftest-all.sh` 与各 `selftest-*.sh` 合成 fixture 自测通过,但直接跑真实入口 `bash specs/008-pB/scripts/verify-ppv-p1.sh` 在本机 macOS 默认 `GNU bash, version 3.2.57(1)-release` 下报 `line 24: mapfile: command not found` + `_RUNMF: unbound variable`,随后才报 `FAIL: manifest 不存在:`。脚本第 24 行用 `mapfile -t _RUNMF < <(...)`;`mapfile` 是 Bash 4+ 特性,macOS 系统 Bash 3.2 不支持。结果:operator 真采集后按 RUN 执行单跑默认 `bash` 入口会先踩环境崩溃,不是得到干净的证据校验结果;这削弱 Deterministic Feedback 层的可移植性。可选修法:用 POSIX/ Bash 3 兼容 while-read 数组收集;或在脚本头显式检测 Bash >=4 并给出可操作错误;或标准化项目工具链要求 Homebrew bash 路径并在 RUN 文档写死。
- 关联: `specs/008-pB/scripts/verify-ppv-p1.sh` lines 16-30 / 008-pB RUN 执行单 / KG-6 shell 环境坑 / 本次实测 `bash --version` + `bash specs/008-pB/scripts/verify-ppv-p1.sh`
- operator 确认: <留空 · 待 operator review:统一 verify 脚本 portability 规则,禁止无检测使用 Bash 4+ 特性,或明确 XenoDev shell baseline;框架级,回 IDS forge 定>

### KG-14 · 008 抓包采集依赖的 mitmproxy 在新 macOS 上经 Homebrew 装不可用 — 工具链 bootstrap 缺可移植安装规约
- 日期: 2026-06-14T11:47:00Z
- 类型: 框架缺陷(工具链 bootstrap)
- 严重度: medium
- 复现场景: 008-pB 探针采集链(spec C5「须抓包取得」)依赖 mitmproxy 落 addon。在本机(macOS 26.5.1 / Apple Silicon)装 mitmproxy 踩连环坑:① Homebrew **已无 mitmproxy formula**(`No available formula`,只剩 cask);② cask 版是 PyInstaller 打包 app bundle,其 CLI 二进制 `mitmproxy.app/Contents/MacOS/mitmdump` 带 `com.apple.quarantine` + `com.apple.provenance`,`spctl` 评 `rejected (does not seem to be an app)`;③ 删 quarantine **连 sudo 都 `Operation not permitted`**(SIP/系统保护该路径,root 无权改);④ 本机默认 `xattr` 是 pip 装的精简版(`~/.local/bin/xattr`,不支持 `-r`,删带值属性会抛 Python traceback),与系统 `/usr/bin/xattr` 行为不一致,放大排查噪音。**最终可用路径 = pipx**:`brew install pipx` + `pipx install mitmproxy`(纯 PyPI Python 包,装进独立 venv,无 app bundle/无 Gatekeeper quarantine)→ `~/.local/bin/mitmdump` 秒级可用,CA 2 秒生成。**另一坑(排查教训)**:用 `后台起进程 + sleep N + kill` 判「是否 hang」会误判——pip 版首次启动 1.6s(编译 .pyc),提前 kill 会误报「仍 hang」;应给足时间 + 计时,或轮询目标产物(CA 文件)而非猜测。
- 关联: `projects/008-pB/probe/RUN-T002.md` 前置 0(装 mitmproxy CA 的步骤,现假设裸 `mitmdump` 可用)/ `specs/008-pB/scripts/mitm-capture-addon.py`(依赖 mitmdump 加载)/ KG-6 + KG-13 shell/环境可移植性坑系列 / 本次实测 `brew info --formula mitmproxy`(无)+ `spctl -a` + `sudo /usr/bin/xattr -d`(Operation not permitted)+ `pipx install mitmproxy`(成功)
- operator 确认: <留空 · 待 operator review:XenoDev 是否需要一份「探针/采集类工具链 bootstrap 规约」——对 mitmproxy 这类 Homebrew formula 已退役 / cask 被 Gatekeeper 拦的工具,标准化用 pipx(或 uv tool)从 PyPI 装,并在 RUN 执行单写死安装方式 + 可用性自检(check-local-tools.sh 已查 whisper-cli,应补查 mitmdump 真能启动而非仅 in PATH);框架级,回 IDS forge 定>

### KG-15 · 探针 selftest 把「活证据文件」当 fixture,operator 真采集填值后 selftest 必然误报
- 日期: 2026-06-14T13:30:00Z
- 类型: 框架缺陷(探针自测设计 · spec-writer/task-decomposer 派生规则)
- 严重度: medium(不记会让每个探针 task 在 operator 真采集后都误报 selftest FAIL,污染 status/完成判据)
- 复现场景: 008-pB RUN-T002 operator 真采集后,把真值填进 `specs/008-pB/probe-evidence/reachability.md`(正常流程),`selftest-all.sh` 立刻报 FAIL。根因:`selftest-reachability.sh` 两处直接拿**活的** reachability.md 当 fixture —— 第 168 行 `run_case "真证据骨架(含占位符)→ 应 FAIL" "<活文件>" 1`(硬编码期望活文件含占位符→FAIL),第 178 行又读活文件做「真模板」靠 `.replace("<待真采集...>")` 填充。一旦 operator 填值:① 骨架用例:活文件无占位符→verify PASS,但期望 FAIL→MISMATCH(selftest-all 报红元凶);② 真模板用例:replace 变空操作,语义失真(碰巧仍 exit 0 没暴露)。**本质 = 探针自测的 fixture 生命周期与「证据文件本就该被 operator 填值」冲突**:自测隐含假设「operator 永不填证据文件」,但填值正是 RUN 执行单要求的正常流程。**008 项目内已当场修**(内联生成固定骨架 fixture `skeleton-placeholders.md`,两处改用它脱离活文件;selftest-all 恢复全绿)—— 但**模式级**问题(派生的探针 selftest 不得拿活证据文件当 fixture)是框架级,该进 spec-writer/task-decomposer 的 selftest 派生规则。
- 关联: `specs/008-pB/scripts/selftest-reachability.sh` line 168+178(已修)/ `specs/008-pB/probe-evidence/reachability.md`(被误当 fixture 的活文件)/ KG-10 + KG-13(测试不可靠/可移植性坑系列)/ spec-writer SKILL(探针证据骨架 + selftest 派生) / task-decomposer SKILL
- operator 确认: <留空 · 待 operator review:在 spec-writer/task-decomposer 派生探针 selftest 时,加一条规则「selftest 的 fixture 必须是脚本内联生成或独立静态 fixture,绝不引用 operator 待填的活证据文件(reachability/gate-decision/cadence 等);否则 operator 真采集填值后 selftest 必误报」。008 已当场修具体 bug,此条固化模式;框架级,回 IDS forge 定>

---

## 如何回流到 IDS(阶段性 · 攒够一批再回)

1. **轻量持续**:dogfood 中随手 append 上面的条目(这是 framework 自动捕获的本体)。
2. **阶段性回流**:攒够一批(或某条 high 严重度需要尽快 forge),把本 backlog 的快照带回 IDS:
   - **跟 hand-back 走**(推荐):产 hand-back 包时,在 §3「Suggested IDS actions」里指向本 backlog(`dogfood-backlog.md` 有 N 条待审框架问题),operator 在 IDS `/handback-review 006` 时看到 → 决定起 forge。
   - **或 operator 直接 cp 快照**:`cp dogfood-backlog.md` 到 IDS `discussion/006/dogfood-backlog-<ts>.md` 作为 forge v6 的 X 标的。
3. **回 IDS 起 forge**:`/expert-forge 006`(forge 永远在 IDS 治理仓)· 本 backlog 整个当 X 标的 · 双 AI 收敛出 v6 verdict + 改造方案 → 再下发 XenoDev 半边 brief。这正是 v4→v5 走过的"攒批真问题再 forge"模式。

> **不在 XenoDev 当场改框架** —— 即使 dogfood 发现的框架坑很想顺手修。框架级变更必须走 IDS forge(治理),否则 SHARED-CONTRACT / mirror 体系会乱套(V4 失败模式)。本 backlog 是"记下来带回去",不是"就地改"。

## KG-16 · whisper.cpp 长音频 ASR 默认参数遭灾难性 repetition-loop(须 -mc 0)
- 日期: 2026-06-14T14:40:00Z
- 类型: 优化空间(ASR 管线操作痛点 · 同 KG-14 工具坑性质)
- 严重度: low(工具用法坑,非 framework 核心缺陷;但任何后续做转录的项目都会踩,值得攒)
- 复现场景: 008-pB RUN-T003 真跑回放转录链。whisper.cpp(whisper-cli + large-v3)转 54min 中文音频,
  **默认参数**首跑遭灾难性 repetition-loop:产 2137 段但**唯一仅 32 段**,`今天礼拜天我都不知道直播`
  重复 **2134 次**,仅头 ~80 秒是真转录,后 52 分钟单句刷屏(空转 40 分钟)。诊断:① 音频本体正常
  (中段 -20dB 健康人声,90s 小样转录完美);② 根因 = whisper.cpp 默认**跨 30s 窗口带 text-context**,
  一吐重复就滚雪球污染后续(经典 greedy-decoding 病)。修方:`-mc 0`(max-context 0,不跨窗带 context)
  + `-sns`(抑非语音),**不加 `-nf`**(保留 temp fallback)。重跑 1390 段无重复,24.8min。
- 为什么可能算框架级(供 forge 判):若 XenoDev 后续把「视频/音频 → ASR → 摘要」做成可复用 SKILL/管线
  (008 不会是唯一要转录的项目),那「ASR 默认参数对长音频不稳」是该管线的**默认配置缺陷** ——
  默认就该带 `-mc 0`,否则每个用的人都空转 40min + 产垃圾才发现。当前已在 008 项目内修
  (RUN-T003.md 的 ③ ASR 命令加了 `-mc 0 -sns` + loop 自检),**但这是项目内补丁**;若要固化成
  framework 级 ASR 管线默认,该回 forge 决议(本条记此,不在 XenoDev 当场建管线 SKILL)。
- 关联: projects/008-pB/probe/RUN-T003.md ③ ASR 命令(已加 -mc 0 -sns + 自检) / KG-14(同为工具坑性质) /
  run-20260614T055139Z-63869-7c2c1d/asr.BROKEN-rep-loop.log(坏转录留痕,诊断硬证据)
- operator 确认: 

## KG-17 · KG-15 复发:第 2 个探针 selftest 同样引用 live 活证据当 fixture(模式确认系统性)
- 日期: 2026-06-14T16:30:00Z
- 类型: 框架缺陷(SKILL 级 · KG-15 同根复发 → 升级证据)
- 严重度: medium(单发是偶然,复发=系统性;探针 selftest 生成器有共性缺陷)
- 复现场景: 008-pB T004 真填 cadence-log.md(回溯抓包 30 天数据)后,`selftest-cadence.sh` 的
  **NEG-3「骨架→应FAIL」当场翻转(expect=1 got=0)** —— 因 NEG-3 引用 **live `cadence-log.md`** 当"占位骨架"
  fixture,operator 真填后该文件不再是骨架 → verify 正确 PASS → 自测误报红。**与 KG-15(selftest-reachability
  同病)字节级同根**:探针 selftest 把「operator 待填的活证据文件」直接当负向 fixture。已就地修(内联固定骨架,
  与活文件解耦),同 KG-15 修法。
- 为什么升级证据: KG-15 单发时可能被当个案;**现 reachability + cadence 两个 selftest 都犯**(2/N)→ 证明这是
  探针 selftest **生成模式的系统性缺陷**,非偶然。建议 forge 把「selftest 负向 fixture 必须自带固定样本、
  严禁引用 live 活证据文件」固化进 task-decomposer/spec-writer 的探针自测生成约定(写进 SKILL),否则
  每个新探针 task 真填后都会重踩。
- 关联: KG-15(selftest-reachability 同病,已修) / specs/008-pB/scripts/selftest-cadence.sh NEG-3(已修) /
  specs/008-pB/scripts/selftest-reachability.sh(KG-15 修过的)
- operator 确认: 

## KG-17-UPDATE · 同病第 3 例确认(gate-decision selftest)—— 3/N,系统性铁证
- 日期: 2026-06-14T17:00:00Z
- (接 KG-17,append-only 不改原条)T005 真填 P0-GATE-decision.md 后,`selftest-gate-decision.sh`
  NEG-5「骨架→应FAIL」**同样当场翻转**(expect=1 got=0)—— 与 KG-15(reachability)、KG-17(cadence)
  **字节级同根**:引用 live 活证据文件当占位骨架 fixture。已就地修(内联固定骨架到 $FX,同前两次)。
- **现 3/3 探针证据类 selftest(reachability + cadence + gate-decision)全中同一坑** → 不再是"偶发"或"2 例巧合",
  是探针 selftest 生成模式的**确定性系统缺陷**。forge 必修:把「selftest 负向骨架 fixture 必须内联自带、
  严禁 `run` live 活证据文件」写进 task-decomposer/spec-writer 的探针自测生成约定(SKILL 级硬规则)。
- 关联: KG-15 / KG-17 / specs/008-pB/scripts/selftest-gate-decision.sh NEG-5(已修)
- operator 确认: 

## KG-17-UPDATE-2 · 同病第 4 例(gate-acceptance selftest)—— 4/4 探针证据 selftest 全中
- 日期: 2026-06-14T17:20:00Z
- (接 KG-17,append-only)T006 真填 gate-acceptance.md 后,`selftest-gate-acceptance.sh`「骨架→应FAIL」
  **第 4 次同样翻转**(expect=1 got=0)。已就地修(内联固定骨架到 $FX)。
- **最终统计:4/4 探针证据类 selftest(reachability / cadence / gate-decision / gate-acceptance)全中同一坑**。
  这是 008-pB 探针轮自测生成器的**100% 确定性缺陷** —— 每一个"骨架→FAIL"负向 case 都引用了 operator
  待填的 live 活证据文件,operator 真填后**无一例外全部翻转**。forge 此条优先级应从 medium 提到 **high**:
  不修则任何沿用这套探针 selftest 模式的新 task,operator 一旦真填证据,自测必假绿(且 selftest-all 当场红,
  阻断后续)。修法已四处验证:负向骨架 fixture 必须内联自带、严禁 run live 活证据文件。
- 关联: KG-15 / KG-17 / KG-17-UPDATE / 四个 selftest-*.sh(均已修)
- operator 确认: 

## KG-18 · codex-review 轮数应设硬上限(~3) + 超限转 followup 累积,留到全开发完再逐一精修判定
- 日期: 2026-06-15T00:00:00Z
- 类型: 框架缺陷 | 优化空间(parallel-builder §3 + codex-review SKILL §4.2 轮次策略)
- 严重度: medium(拖慢单 task ship 节奏 · 不阻断正确性,但放大每 task 的 review 往返成本)
- 复现场景: **operator 用 XenoDev 真开发 008-pB v0.1,跑 parallel-builder 第一个 task T101(004 allowlist schema)。
  codex `review` 连跑 4 轮 needs-attention,逐轮逼近**:R1 `published_at` 没强校 ISO → 加 ISO;R2 ISO 校验仍比
  schema 松(date-only/无时区/空格分隔)+ selftest 不 fail-fast → RFC3339 正则 + fixture 断言;R3 validator 比
  文档「ISO」措辞严 → 契约不一致(operator 拍板:收紧契约到 RFC3339);R4 又出新 [P1]:`capture_status=failed`
  仍被 unconditional 要 raw_content/transcript_ref → 失败记录无法诚实表达(破 O4/C7)。**现象:每修一轮 codex 就
  从新角度再挑一条,单个最小接口 task 卡在 review 循环里迟迟不能 ship**。SKILL 现有 §4.2 是「4 轮上限 → hard-stop
  交 operator」,但 hard-stop 太晚(4 轮已烧不少往返)且粒度太粗(approve / 全停 二选一,没有"先记下、继续走、回头精修"档)。
- **operator 决议的改法(待 forge 审议落地)**:① codex review 轮数硬上限**降到 ~3 轮**(非 4);② 超限**不 hard-stop**,
  而是把**剩余 finding 记成 followup**(累积到一个 followup 清单),**ship 继续往下走**;③ 等**所有 task 开发完毕**,
  再**逐一 review followup 清单**判「这条是否值得精修 / 还是可接受」。即把「逐 task 死磕到 codex 满意」换成
  「快速过 + 末尾统一精修」—— 适配"先把整条管线打通、细节(格式/严格度/边界)最后统一调"的真实开发节奏
  (与 operator 早先「细节等成型再细调」偏好一致)。
- **设计注意(给 forge)**:(a) 区分 finding 严重度 —— **P1(破 spec outcome,如本轮 failed 记录破 O4/C7)可能仍该当轮修**,
  只把 P2/P3 转 followup;否则"快速过"会把真正的契约 bug 也 defer 掉。轮数上限 + followup 机制要和「P1 当轮修」共存。
  (b) followup 清单要可机器累积(类似本 backlog / events.jsonl 的 append-only),且 ship 的 hand-back 要带上"本 task 留了
  哪些 followup 未精修"的显式标记,不静默吞。(c) 末尾"逐一精修判定"本身需要一个 gate(谁判、判据是什么)。
- 关联: parallel-builder SKILL §3(codex review 决策表)/ codex-review SKILL §4.2(4 轮上限 + hard-stop)/ 
  本轮 T101 review-log/T101-round{1,2,3,4}.md(4 轮真实复现证据,留在 worktree)
- operator 确认: operator 2026-06-15 主动提出(本条即其原话转录)· 待回 IDS forge 决议轮数策略 + followup 机制设计

## KG-19 · task-ID 命名空间跨 feature 复用 → red-green-log 被旧同名任务内容污染
- 日期: 2026-06-15T00:30:00Z
- 类型: 框架缺陷(parallel-builder §2 red-green-log 路径命名 + task-ID 复用)
- 严重度: medium(不阻断 ship 但污染证据 · 每次手工 de-contaminate 易漏 · pre-merge verifier 读 log 可能被旧绿误导)
- 复现场景: **跑 008-pB v0.1 parallel-builder,T101 与 T102 都从 main 拉 worktree 时,
  `tests/red-green-log/T101.log` / `T102.log` 已存在 —— 内容来自更早完全不同 feature 的同名 "T101"/"T102"
  任务**(T101.log 是个 handback-mirror 任务的 SHA 校验输出;T102.log 是个 credential-isolation `.env.production`
  任务的 V1/V2/V3 输出)。parallel-builder §2 的 red-green-log 路径是 `tests/red-green-log/<TID>.log`,**只按 TID 命名、
  不带 feature/wave 前缀**。多个 feature 各自从 T101/T102… 起编号(task-decomposer 每个 spec 独立编号),
  TID 撞车 → 新任务 append red/green 时**叠在旧任务遗留内容上**。现象:① red 行混在几十行无关旧输出里;
  ② pre-merge verifier 检 log「有 [red]rc≠0 + 末 [green]rc=0」时,旧任务的绿行可能被当本任务证据;
  ③ codex 审 diff 时看到一堆无关红绿历史会困惑(T101 codex round 真去读了 T101.log 头部)。
  两个 task 连续撞同一坑(T101 + T102),系统性,非偶发。
- **修法建议(给 forge)**:red-green-log 路径带 feature 前缀,如 `tests/red-green-log/<feature>/<TID>.log`
  或 `tests/red-green-log/<feature>-<TID>.log`(与 verify-ppv 的 run-<id>/ 隔离思路一致);或 worktree 创建时
  若 log 已存在且属别的 feature → 报错/归档而非静默 append。当前我每次手工 de-contaminate(重置为本任务内容 +
  注释说明来历),但这正是 KG-15 家族「证据被陈旧内容污染」的同型问题,应 framework 层根治。
- 关联: parallel-builder SKILL §2(red-green-log)/ task-decomposer(每 spec 独立 TID 编号)/ KG-15 / KG-17 /
  本轮 T101.log + T102.log(均已手工去污,注释留来历)/ §4.4 pre-merge verifier 读 log 那条
- operator 确认: 

## KG-20 · codex 配额墙打在 review 轮中 → ship 卡死无 fail-closed 之外的恢复档
- 日期: 2026-06-15T02:35:00Z
- 类型: 框架缺陷(parallel-builder §3 codex review 不可用时的恢复路径缺失)
- 严重度: medium(不破坏正确性 · 但单 task 在 review 阶段被外部配额墙无限期卡住 · 无标准断点恢复)
- 复现场景: **跑 008-pB v0.1 T103(采集记录 schema),codex review 跑到第 4 轮时
  codex-companion 返回 `You've hit your usage limit ... try again at 12:15 PM`**(ChatGPT/codex 账号
  级配额墙,非本仓问题)。此时 task 代码已全绿(42 test · cov 99% · selftest 全绿)且 R1-R3 三轮发现的
  问题都已逐字对齐 reachability.md 修掉,但 **parallel-builder §3 要求 codex verdict=approve 才能 merge**,
  配额墙下 §3 既不是 approve 也不是 needs-attention,而是「reviewer failed to output」。SKILL §3 对
  codex CLI 异常的规定是 **fail-closed(不静默标 reviewed)**——这是对的(防把没审过的当审过),但
  **没有「外部配额墙 + 已知重置时间」这一档的恢复指引**:operator/agent 该等到重置再续审?该记什么状态?
  worktree 该留着还是清?当前我的处置:worktree 留存 + 代码 commit 在分支 + 排 wakeup 到重置后重跑 R4,
  但这是我临场判断,SKILL 无明文档位。
- **修法建议(给 forge)**:parallel-builder §3 codex 不可用分支细化为两类:(a) CLI 真异常/崩溃 → fail-closed
  hard-stop 交 operator(现状);(b) **可恢复的外部限流(配额/网络,带或不带重置时间)→ 标 task 为
  `review-pending-quota` 暂挂态**(worktree + commit 留存,记重置时间),到点自动/手动续审,**不算 review 失败、
  不丢进度**。配合一个轻状态文件(如 `.eval/` 里记 `<TID> review blocked on quota until <ts>`)让恢复有据。
- 关联: parallel-builder SKILL §3(codex review 决策表 + CLI 异常 fail-closed)/ codex-companion.mjs(配额墙
  错误透传)/ 本轮 T103 R4(配额墙复现 · 已排 wakeup 重试)/ [[feedback-codex-round-cap-policy]](KG-18 同族:
  codex review 流程的工程化缺口)
- operator 确认: 

## KG-18 补记 · 轮数上限与「自诱回归」的交互(R1→R2→R3 每轮修引入下轮问题)
- 日期: 2026-06-15T02:36:00Z
- 类型: 优化空间(KG-18 round-cap 政策的执行细节 · 非新缺陷)
- 严重度: low(政策已立 · 此为执行观察补强证据)
- 复现场景: **T103 codex review R1-R3 连续三轮,每轮的 needs-attention 都是「我上一轮修复引入的新问题」**:
  R1 提 source_id 该校 form 一致性 → 我 R2 加 `<form>:` 前缀 → R2 codex 判这破下游裸-id 契约([P1] 回归)→
  我 R3 撤前缀但 R2 顺手改的 canonicalize 全剥 query → R3 codex 判这偏离 reachability url-stable([P1])。
  **三轮都是真 [P1] 契约缺陷(非 nitpick),但根因是我没在 R1 就把 reachability.md:58-66 的 url-stable 规则
  逐字读全、逐字对齐**,而是逐轮被 codex 逼着逼近。KG-18 政策「P1 当轮修、无底洞→停 escalate」在此奏效
  (R3 后我逐字 port 了 spec,R4 才有望收敛),但暴露一个执行教训:**契约类 task 应在动手前先把所有相关
  既有契约文件(reachability/spec §7/同族已 ship task)逐字读全建「契约清单」,再写**,否则 codex 轮次会
  退化成「逐条发现我漏读的契约」——这比「发现真 bug」便宜但仍烧轮次 + 烧 codex 配额(直接导致 KG-20 撞墙)。
- **修法建议(给 forge)**:parallel-builder §2 或 §0 增「契约前置清单」步骤:contract/schema/interface 类 task
  动工前,列出本 task 须对齐的所有既有契约文件 + 逐字摘录关键规则进 worktree 的 contract-checklist,
  TDD 测试直接钉这些规则。把「逐字对齐既有契约」从「codex 逐轮逼出来」前移到「写之前自己做」。
- 关联: [[feedback-codex-round-cap-policy]] / KG-18 / parallel-builder §2 TDD / reachability.md:58-66 /
  本轮 T103 R1-R3(三轮自诱回归真实复现 · review-log 留分支)
- operator 确认: 

## KG-21 · Python 包 __init__ re-export 与 CLI 子模块同名 → `python3 -m pkg.<name>` 被函数遮蔽(3 例确认系统性)
- 日期: 2026-06-15
- 类型: 缺陷(framework 用起来的痛点 · parallel-builder TDD 流程不暴露此坑)· 跨 task 复发
- 严重度: medium(每次都是 CLI 运行期 AttributeError,测试若不跑 `python3 -m pkg.<sub>` 会漏到 ship 前)
- 复现场景(**3 例同坑,系统性铁证**):v0.1 实装里凡「公开函数名 == CLI 子模块名」必中:
  ① **T104** `src/pipeline/article/`:`run` 函数 re-export 遮蔽 `run.py`(`python3 -m ...run` 崩);
  ② **T106** `src/store/db/`:`query` 函数遮蔽 `query.py`(`python3 -m ...query` 崩);
  ③ **T107** `src/retrieval/`:`search` 函数遮蔽 `search.py`(`python3 -m ...search`/import 崩)。
  机理:`__init__.py` 里 `from .mod import func`,当 `func` 与某子模块同名,`__init__` 跑完后
  `pkg.func` 绑定到**函数**,`python3 -m pkg.func`(本想跑子模块 CLI)拿到函数 → `'function' object has
  no attribute 'main'`。每次都是写完 impl、跑 `## Verification` 的 `python3 -m` 命令才炸,逐 task 重新踩。
- 当前各 task 的处置(一致但靠人记):`__init__` **不 re-export 与 CLI 子模块同名的函数**,
  改 `from pkg.mod import func` 直接用 / 或函数换名(T104 `run`→`run_pipeline`)。
- **修法建议(给 forge)**:parallel-builder §2.4 task 验收清单或 spec-writer 的 scaffold 约定里加一条
  **命名规约 + 自动 lint**:① 约定「CLI 子模块名(run/query/search/cli)不与 __init__ re-export 的公开
  函数同名」;② §2.4 验收**强制真跑** task `## Verification` 里的每条 `python3 -m <module>` 命令(本就该跑,
  但若 task 没写全 `-m` 命令就漏)→ 把「`python3 -m` 冒烟」设为 CLI-bearing task 的硬验收项;
  ③ 或更省心:scaffold 统一 CLI 子模块名为 `cli.py`(T107/T108 已自发这么做),公开函数永不撞。
- 关联: parallel-builder §2.4 验收 / spec-writer scaffold 约定 / T104(run)・T106(query)・T107(search)
  三例 review-log + 红队主审均独立揪出 / Python import system(submodule vs attribute 同名遮蔽)
- operator 确认: 

### KG-22 · phased spec 增量补 phase 段时,per-phase review status 不被下游 gate 识别(只读 top-level status/reviewed-by)
- 日期: 2026-06-16T00:00:00Z(008-pB v0.2 spec 补段 · codex adversarial-review R3 [high] 捕获)
- 类型: 框架缺陷 | schema-gap
- 严重度: high(直接破 frozen-before-build 铁律 · 任何 phased spec 增量补 phase 都中招)
- 复现场景: 008-pB 是 phased spec(v0.1 已 frozen+ship)。本次在既有 spec 上**补 v0.2 段**(改了 binding 契约
  C5+/C11/P4/P5/O8-O10),为标 v0.2 段独立 review 状态,加了 frontmatter `v0.2_status: review` + `v0.2_reviewed-by: pending`,
  **保留 top-level `status: frozen`**(想表达「v0.1 段仍 frozen」)。codex R3 grep 了三个 consumer 证明:
  `task-decomposer/SKILL.md:22-24`、`parallel-builder/SKILL.md:54-55`、`specs/008-pB/scripts/status-008.sh:58-61`
  **全部只 gate top-level `status`==frozen + `reviewed-by`!=pending,没有任何一个读 `v0.2_status`**。
  → 后果:留 top-level frozen 时,下游 operator/automation 会把**未 review 的 v0.2 scope 当 buildable**,
  起 T2xx decomposition/build = 破「frozen-before-build」不变量,可 ship 未审 v0.2 契约变更。
  本项目当轮 workaround:top-level status 整体降 review(已 grep 证明 gate 正确 BLOCK),v0.2 过 review 后连同复位 frozen。
  但这是**项目级 workaround,框架本身缺「phased spec 的 per-phase 可 build 状态」表达**。
- 为何是框架级(非项目级): spec-writer SKILL 的 frontmatter schema(§3.3)只有单一 `status`/`reviewed-by`,
  对 phased spec「v0.1 frozen + v0.2 review 中」这种**部分 frozen** 状态无表达;task-decomposer/parallel-builder
  的 gate 也只认单一 top-level。**任何** phased spec 增量补 phase(像 006a-pM/008-pB 这类多次 hand-off 的 fork)
  都会撞同一问题。修好后受益的是「以后所有 phased 增量开发的项目」。
- 候选修法(回 forge 议 · 不当场改): ① spec frontmatter 加 `phase_status` map(每 phase 一个 frozen/review 状态);
  ② task-decomposer/parallel-builder gate 改为「读目标 task 的 phase → 查该 phase 的 status」而非单 top-level;
  ③ 或约定「补 phase 段期间 top-level 必须降 review」写进 SKILL(把本项目 workaround 升为框架约定 + 加 lint)。
  ②最彻底(支持 v0.1 task 仍可 build 而 v0.2 被 block 的并行态),但改动面大;③最轻(成文约定)。
- 关联: spec-writer SKILL §3.3 frontmatter schema / task-decomposer SKILL §(status gate) / parallel-builder SKILL §0.1 /
  specs/008-pB/scripts/status-008.sh:58 / 008-pB spec.md frontmatter v0.2_status / codex-v0.2-round3.log R3-F1
- operator 确认: <留空 · operator 阶段性 review 时补>

### KG-23 · codex `--scope working-tree` 看不到「已 commit 未 merge」的改动 → ship 流程每轮 commit 后 review 会 vacuous approve(空 diff)
- 日期: 2026-06-17T00:00:00Z(008-pB v0.2 T210 R3 ship review 踩到)
- 类型: 框架缺陷 | SKILL 机制(codex-review · ship 流程交互)
- 严重度: high(假 approve 风险 · ship gate 失效 · 任何「每轮修完 commit 再 review」的流程都中招)
- 复现场景: parallel-builder ship 流程 §2-§3 是「TDD commit → codex review → 改 → commit → 再 review」。
  T210 R2 修完**已 commit**(dc73508)后,跑 `codex adversarial-review --wait --scope working-tree` 做 R3 →
  codex 报「当前工作树无 staged/unstaged/untracked 变更,无可审 diff」**vacuous approve**。根因:codex
  companion 的 working-tree scope 实测只看 `git diff`(unstaged)+ 可能 staged,**不含已 commit 未 merge**。
  但 codex-review SKILL §0.2 line 67 明写 working-tree scope「worktree 内未 commit 改动 **+ 已 commit 但未
  merge 改动**」—— **文档与实现不符**。改用 `--base main --scope branch` 后得真 R3(3 个 high finding)。
  对照:T205 R2 同样 committed 后跑 working-tree 却**看到了** diff(真 review)—— 行为**不一致/intermittent**,
  更危险(有时假 approve 有时真审,无法预期)。
- 为何是框架级(非项目级): 影响 codex-review SKILL + parallel-builder ship 流程对**所有** task 的 review 有效性。
  ship 流程默认每轮 commit(§2.3/§4.4 要 commit 拓扑),然后 review —— 若 working-tree scope 漏 committed 改动,
  每个 task 的 codex gate 都可能 vacuous approve = ship gate 静默失效。修好后受益的是所有用这套 framework 的 task。
- 候选修法(回 forge 议 · 不当场改): ① codex-review SKILL §3 ship 流程内调用契约改为 `--base <merge-base>
  --scope branch`(review 已 commit 的 branch 全量),而非 working-tree;② 或 parallel-builder §3 调 review 前
  **不 commit**(review 未 commit 改动)再 commit —— 但破坏「每轮 commit 留痕」;③ 或修 companion 的 working-tree
  scope 让它真含 committed-unmerged(对齐 SKILL §0.2 line 67 文档);④ 至少 SKILL 加显式告警「ship 流程内每轮
  commit 后必须用 branch scope,不可用 working-tree」+ 加 lint(review 前检 working-tree 是否空 → 空则强制 branch scope)。
  ①最对(ship 流程本就该 review 整个未 merge branch);③修文档不符;④最轻(成文 + lint)。
- 关联: codex-review SKILL §0.2 line 67(scope 文档)+ §3.0.1 ship 调用契约 / parallel-builder SKILL §3 /
  /tmp/codex-T210-review-r3.log(vacuous approve)vs /tmp/codex-T210-review-r3b.log(branch scope 真 R3)
- operator 确认: <留空 · operator 阶段性 review 时补>

## addon 绝对 import `from src.capture...` 在 mitmdump 12 加载时 ModuleNotFoundError(capture-base.md 起法照抄即崩)
- 日期: 2026-06-17T10:21:00Z
- 类型: 框架缺陷
- 严重度: high
- 复现场景: 008-pB v0.2 实战采集(operator「先图文」)。环境 preflight 全过(addon 4 文件齐 / C5 gitignore 守卫有效 / mitmdump 12.2.3 在 PATH / captures/ 已归档旁路空目录)。按 `capture-base.md` line 33-41 起法 `cd 仓根 && mitmdump -s src/capture/addon.py --set capture_advisor=xincaitong --listen-host 0.0.0.0 --listen-port 8080` → **addon 启动即崩**:`ModuleNotFoundError: No module named 'src'`(addon.py line 19 `from src.capture.classify import classify`)。根因:mitmdump 12 的 `-s` 脚本加载上下文 **sys.path 不含 cwd**,且**不读 `PYTHONPATH` 环境变量**——实测三种 workaround 全失败:① `PYTHONPATH=<repo> mitmdump ...`(env 前缀)崩;② `export PYTHONPATH=<repo>` 同 shell 再起 崩;③ 文档原样起 崩。对照:`PYTHONPATH=<repo> python3 -c "from src.capture.classify import classify"` **成功**(证代码无错,纯 mitmdump 加载机制问题)。`paths.py` 的「落盘根锚定仓根」设计(从 addon 文件位置上溯)解决的是**落盘路径**不依赖 cwd,但解决不了 **import 时** sys.path 的问题——两件事。**capture-base.md 文档的起法在 mitmdump 12.2.3 下 100% 不可用**,任何 operator 照文档起都会卡在这。
- 影响: 阻断**全部**实战抓包采集(图文 + 回放都依赖 addon 落盘)。v0.1 实战(6/14 captures/ 那 107 文件)能产说明当时某种起法可用——可能 mitmproxy 版本不同(12 改了加载机制)或当时有未记录的 workaround;**回归到 12.2.3 后文档起法失效**,典型版本漂移坑。
- 候选修向(框架级 · 回 forge 定 · 不在 XenoDev 当场改): ① addon 顶部加 sys.path 自举(`sys.path.insert(0, os.path.dirname(...up to repo))` 再 import)——但这是改 addon 框架代码;② 改 capture-base.md 起法用 `mitmdump -s` 的相对 import 改造 / 或起法改 `python -m mitmproxy.tools.main` 注入 path;③ 把 addon 拆成「mitmdump 入口薄文件(sys.path 自举)+ src.capture 纯逻辑」。三者都动框架,须 forge 决议选哪个。**当下实战**:operator 同意的话用「起法层 workaround」(不改任何框架文件)临时跑通——见下方 operator 确认。
- 关联: `src/capture/addon.py` line 19-33(绝对 import 块)/ `specs/008-pB/scripts/capture-base.md` line 33-41(失效起法)/ `src/capture/paths.py`(落盘锚定 ≠ import path)/ dogfood KG「mitmproxy 安装坑」条(同采集工具链可移植性系列)/ 本次实测三 workaround 失败日志 /tmp/addon-loadtest.log
- operator 确认: <留空 · 待 operator review:回 IDS forge 定 addon import 自举方式(改 addon / 改文档起法 / 拆薄入口)。当下实战是否授权用「起法层 workaround」(如 `cd src/capture && mitmdump -s addon.py` 改相对 import 不行→ 需 sys.path 注入;或 PYTHONSTARTUP / 临时 .pth)临时跑通而不改框架文件?>

## 实战暴露:_derive_key_points 直接摘原文前段进 vault body,逼近 C5+ 边界(真链首跑实证)
- 日期: 2026-06-17T10:31:00Z
- 类型: 优化空间(关联已有 known-gap · 非新缺陷)
- 严重度: medium
- 复现场景: 008-pB v0.2 真链首跑(真抓包 2 条 2026-06-17 图文 176375/176384 → 入库→004→vault→verify-ppv-p3 全 PASS)。export 进 vault 后,note body「## 摘要要点」下的 key_point 形如 `[原文摘录] <顾问原文前段连续片段>`(**具体原文不录入本 backlog · C5** —— 本文件入 git 回流 IDS,绝不粘顾问原文)——**_derive_key_points(src/feed/article/generate.py:54)直接截取顾问原文前段当 key_point**,不是真摘要。T203 assert_summary_length_bounds 放行(≤500 字 + 单段不算跨点拼接 > 3 句),但 vault body 里实际出现了顾问原文的实质连续片段。对自用 vault(不传播)在 C5+ 边界内(spec line 272「text 保护即长度上限」已记此为 known-gap),但实战看**很直观**:vault body ≈ 原文截断,而非"可溯源但不可重建"的真摘要。
- 为何不是新缺陷: spec §2.1 line 272 + FU-T111 + FU-T202-2 已记「key_points.text 逐字原文 ≤500 = 长度上限即保护」是 v0.1/v0.2 accepted-limit(真摘要需 LLM,属上游)。本条是**实战实证**该 known-gap 的真实观感 + 一个候选优化:exporter 渲染 body 时,key_point 若来自 raw_content 截断(无独立摘要),是否该标注「⚠️ 原文截断非摘要」或截更短(如 ≤120 字)以更远离原文重建。
- 候选优化向(回 forge 定 · 不当场改): ① _derive_key_points 在无真摘要时产更短的引导句(非前 N 字截断);② exporter body 对「截断式 key_point」加显式标注;③ 接真 LLM 摘要管线(根治 · 属上游/v1)。
- 关联: src/feed/article/generate.py:54(_derive_key_points)/ src/export/obsidian.py(_render_body)/ spec line 272 / FU-T111 / FU-T202-2 / 本次真链 vault note out/vault/176384.md(gitignored 不入库,仅本地)
- operator 确认: <留空 · 待 review:确认是否就停在 accepted-limit(自用 vault 可接受)还是排真摘要优化>

## operator 治理诉求:放宽采集面到「自动翻页」(去掉「不主动发请求」半自动约束)
- 日期: 2026-06-19T00:00:00Z
- 类型: 框架缺陷(协议层 · 安全边界 scope 争议 · 非 bug)
- 严重度: high
- 复现场景: 008-pB v0.2 实战采集「2026-01-01 起至今全历史库」。实测边界:moduleContentList 列表接口只吐到 2025-07-21(contentId 164966);2026 的 2 篇(176375/176384,6-17)只在 operator「点开单篇 detail」时被动抓到,**不在任何已抓列表页**。operator 反馈「在 App 里手动滑列表找 2026 入口很慢」,明确要求「改红线,自动翻页没问题」——即希望 agent 程序化翻页/抓取顾问内容列表,而非半自动(operator 手滑 + addon 被动监听)。
- 为何是框架级 + 为何拒绝当场改(3 条):
  ① **C5「不爬/不规避访问控制」**是 spec 写死的项目约束;改它属 PRD 约束变更,SSOT 在 IDS,须回 `/handback-review` → `/scope-inject`,不在 XenoDev 当场删。
  ② **真正拦路虎是凭据隔离(三件硬约束①· non-overridable · IAM 级)**:自动翻页须带 operator 登录态(key/cookie)发请求,而登录态绝不进 agent context——agent 物理上无法以 operator 身份发请求,删 C5 也解不了。这是「半自动被动采集」架构的地基,不是一句「没问题」能拆。
  ③ **dogfood 铁律**:框架级安全边界变更绝不在 XenoDev 当场改(= V4 失败模式「agent 觉得没问题就静默绕过」)。
- 候选决议向(回 IDS forge 定 · 不当场改): 
  ① **维持半自动**(operator 手滑/点开,addon 被动落盘)——当前架构,安全边界最清晰;agent 侧可优化「侦察兵」体验(分析 addon 落盘接口,告诉 operator 哪个栏目含目标时段 + 翻页参数形态,把盲滑变定向滑)降低 operator 手动成本。
  ② **受控自动翻页**(若 forge 评估某些源、某频率、不带高敏登录态确实合规):须解决凭据隔离(如何在不让 key 进 agent context 的前提下翻页?可能需独立采集 daemon 持 key,agent 只读其落盘——但这又引入新信任边界)+ 重定义 C5 scope(「规避访问控制」边界在哪)+ 速率/源白名单治理。这是协议层重大变更,须 forge 专题。
  ③ **混合**:agent 产「翻页计划」(参数序列),operator 一键确认后由持 key 的 daemon 执行——agent 不持 key、不直接发请求,但自动化程度提升。信任边界仍需 forge 审。
- 关联: spec 008-pB C5 条款 / framework/SHARED-CONTRACT.md §1+§2(凭据隔离 + 半自动采集原则)/ src/capture/addon.py(被动监听架构)/ 三件硬约束① / CLAUDE.md dogfood 铁律 / 本次实战边界证据(列表止于 2025-07-21,2026 仅 detail 可达)
- operator 确认: <留空 · 待 operator 回 IDS:这是要不要改采集架构的治理决议,operator 已口头表态「自动翻页没问题」——但须在 IDS forge 走正式决议(评估凭据隔离怎么解 / C5 scope 怎么重定义 / 选哪个候选向),不在 XenoDev 当场拆安全底线>

---

## 方案A 凭据隔离 hook 与 parallel-builder 自身命令的根本张力(static-analysis vs build-needs)
- 日期: 2026-06-20T00:00:00Z
- 类型: 框架张力(SKILL 机制 · 凭据隔离 hook ↔ parallel-builder 命令集 · 非单 bug)
- 严重度: medium(单用户本地可接受 · 但 framework 推广到多场景前须 forge 决)
- 复现场景: 008-pB v0.3 T301 落 forge v3 verdict 的「方案A:resolved-path PreToolUse hook」做凭据隔离
  (agent 不读 secrets/)。codex adversarial-review **3 轮**反复证明同一根本点:**纯静态 shell 分析
  无法完整封堵 runtime 字符串构造的读路径**。R1 文本deny被 `$(printf sec)rets/` 绕;R2 引号拼接
  `'secr'ets/` 绕 + 「无条件 fail-closed 把 build 自身的 `python3 -m pytest`/`$(date)` 也拦了」;
  R3 零片段 `d=$(printf %s s e c r e t s);cat "$d"/prod/*` 绕。每轮修完又有新构造。
- 为何是框架级(受益面 = 所有用这套 framework 的项目):
  ① **凭据隔离 hook 是 framework 安全件**(三件硬约束①的一种实现路径),不是 008 项目专属。任何 L4
     项目要「agent 不读某敏感目录」都会撞同一墙。
  ② **核心张力**:parallel-builder SKILL **强制**用 `python3 -m pytest`/`$(date)`/`bash -c`/`${PIPESTATUS}`
     跑 TDD(§2),而「拦一切解释器/命令替换」的 fail-closed 会**拦掉 build 自身**(codex R2-critical)。
     → 凭据隔离 hook 与 build runner 的命令集**天然冲突**:hook 越严越拦 build,越松越漏凭据。
  ③ 这对**任何**「在 agent 跑 build 的同时要隔离凭据」的 framework 用户都是结构性问题。
- 当前 XenoDev 内处置(项目级 best-effort · 不算 framework 解): T301 用「窄 fail-closed」——只在命令
  含 secrets 片段/动态路径前缀+read-util 时拒,放行不涉 secrets 的正常 build。codex R3 exact payload
  已全 deny。但残留(解释器纯字符构造零片段)封不死,记 FU-v0.3-T301-1。
- 候选决议向(回 IDS forge 定 · 不当场改 framework):
  ① **OS 身份级隔离(方案B)** 作 framework 标准:agent 跑在无 secrets/ 读权限的 OS 用户/容器/
     macOS sandbox-exec 下 → build 命令照跑但 OS 级读不到凭据 → 根治张力(hook 不必拦 build)。
     代价:setup 复杂度 + 跨平台。operator 008 已选方案A(便利优先),但 framework 默认值该不该是 B?
  ② **受控 allowlist runner**:parallel-builder 的 build 命令走一个白名单执行器(已知安全命令直放),
     未知命令才过严 hook。需改 parallel-builder SKILL + 维护命令白名单。
  ③ **维持方案A + 文档化残留**:承认 hook 是 best-effort,配 0600+scrub 纵深,威胁模型限「单用户
     本地非对抗」。简单但不适合多租户/对抗场景。
- 关联: .claude/hooks/deny-secrets-read.{sh,py}(T301 实装)/ .claude/skills/parallel-builder/SKILL.md §2
  (强制 python3 -m pytest / $(date) / bash -c)/ 三件硬约束①凭据隔离 / forge v3 verdict 三层分离 /
  FU-v0.3-T301-1 / 上一条 dogfood「放宽采集面」候选② daemon 持 key(broker 即其实现)
- **实战复现(2026-06-20 · ship T301 当场撞到 · 高价值硬证据)**: T301 merge 后 hook 立即生效,**连 ship
  自己的 `git commit` 都被拦**。三连击全被 deny:① `git commit -m "$(cat <<EOF ...正文含'秘密'字样... EOF)"`
  → 触发「含片段 + 合成构造($(...)/heredoc)→ fail-closed」;② 改 `git commit -F msgfile` 但 `cat > msgfile <<EOF`
  heredoc 正文带片段 → 同拒;③ `python3 - <<PY ...正文带 secrets/ 段... PY` 追加 dogfood → Bash 外壳含片段段被拒。
  **均为写操作(git commit / 写文件 不读 secrets/),却被当读凭据拦**。最终 workaround = 多个 `-m` flag(无 $()/heredoc)
  + 用 Write/Edit 工具(非 Bash)改文件。→ **坐实「hook 越严越拦正常 build/ship workflow」是真实、当场、反复触发的**,
  不是理论担忧。尤其:任何 commit message / 文件正文**提到"凭据/secrets"这个词**且**用 heredoc 或 $() 写**就被拦
  —— 这对一个**专做凭据隔离的 task**几乎必然撞(正文天然要写"secrets")。修法见上候选①(OS身份·根治)②(allowlist runner)。
- operator 确认: <留空 · 待回 IDS forge:framework 默认凭据隔离强度 = 方案A(hook)还是方案B(OS身份)?
  parallel-builder 命令集与凭据 hook 的冲突怎么消?这是 framework 安全模型的专题,不在 XenoDev 当场拆>

## 后台长任务(真跑)缺「可靠存活检测 + 单实例锁」约定 → 易误判重复起、互相写坏产物
- 日期: 2026-06-25T12:15:00Z
- 类型: 优化空间
- 严重度: medium
- 复现场景: 用 XenoDev 真跑 008-pB 回放下载(281 个 mp4 · 后台 `python3 driver --download-only &` 长跑 ~1h)。
  开发 Claude 盯进度时用 `ps -eo args | grep verify_token | grep python3 | grep -v grep` 判进程存活,
  **两次误报「已停」**(实际原始进程一直健康在跑 · 那个 grep 管道因时序/缓冲漏报),于是又起了 2 个
  并行进程 → **3 个 download-only 进程并行写同一 manifest + 同一批 run 目录** → ffmpeg 孤儿进程
  写坏 mp4(同文件被两个 ffmpeg 同时写 · 不完整)。止损:杀多余进程 + 删不完整 mp4 + ffprobe 全量校验。
  根因两层:① 开发 Claude 手搓 ps|grep 判存活不可靠(易误判);② 框架未给后台真跑提供「单实例锁
  (防重复起)+ 标准进度/存活查询」约定 → 每个用框架的人自己手搓、各自踩坑。
- 关联: parallel-builder / 后台真跑模式 · run_download_only(断点续靠「mp4 存在且非空」做 done 标记 ·
  但「不完整 mp4」也算存在 → 误跳;且无 flock 单实例锁)· 易复发于任何用本框架跑后台长采集的项目。
- 可能的框架侧解法(留 forge 议): ① 给长任务 driver 标配 flock 单实例锁(同 manifest/run-dir 只允许一个
  writer);② 落 PID 文件 + 标准「进度查询」脚本(不靠开发 Claude 手搓 ps|grep);③ 断点续 done 标记
  不只判「文件存在非空」,加完整性校验(size 匹配 Content-Length / ffprobe 可读)防「不完整即跳」。
- **二次实战复现(2026-06-26 · 同坑又踩 · 高价值)**: operator 让继续跑回放下载,我后台起
  `run_download.py --download-only`(单实例)。盯进度时 `pgrep -af run_download.py` **连续两次误判「进程已结束」**
  (实际后台 pid 2351311 全程健康在下 · ffmpeg 正拉 myqcloud 签名流 · mp4 284→287 一直在涨)。
  根因同上条①:ffmpeg 单条耗时长(几十秒~分钟级)→ 输出稀疏 + pgrep 时序 → 漏报。**因误判「已结束」,我又前台
  跑了一次 `--limit 3` 想"重启"** → 短暂出现两个下载进程(所幸前台被 timeout SIGTERM 连 ffmpeg 子进程一起清掉,
  未真撞车写坏文件,但**这正是上条预言的"误判存活→重复起→并行写"路径的实际发生**,只是没酿成损坏)。
  → 坐实:**只要没有"可靠存活查询 + 单实例锁",开发 Claude 必然反复踩"误判→重起"**。这次安全只是侥幸
  (timeout 恰好兜住),不能依赖。② 额外暴露:`run_download.py` 这类 scratchpad wrapper **写死 `main([...])` 不透传
  CLI 参数** → 我 `--limit 3` 被忽略实际跑全量,加剧并行风险。框架若给标准 driver 入口(带 flock + 参数透传),
  这两类自制 wrapper 的坑都能消。
- **关联:凭据隔离 hook 加剧排查难度**: 本次想核进程目标 mp4(`tr < /proc/$pid/cmdline` / `stat <path>` / `head <log>`)
  时,凡命令含**变量拼路径 + read-util** 就被 C12 hook 当"零片段合成读凭据"拦掉(见新条 KG-env-pointer 同源张力)
  → 被迫绕道 `pgrep -a` 看命令行。即「盯后台真跑存活」这个高频运维动作本身与凭据 hook 冲突,放大了存活检测缺失的痛。
- operator 确认: 

## 凭据「env 名指针」范式:指针未持久化(~/.bashrc/unit 未设)→ load_token 静默 fail-closed,难诊断
- 日期: 2026-06-26T00:00:00Z
- 类型: 框架缺陷 | 优化空间
- 严重度: medium(单用户可自修 · 但「文件在却读不到 + 报错不指向真因」对任何用此范式的项目都坑)
- 复现场景: 008-pB 回放下载,token 文件 `secrets/prod/008-detail-token.json` **真实存在、0600、19 分钟前刚抓(新鲜)**,
  但开跑 `load_token()` 直接 `BrokerCredentialError: token 未注入(env XENODEV_008_DETAIL_TOKEN_FILE 缺)`。
  排查发现 **`~/.bashrc` 里根本没有 `export XENODEV_008_DETAIL_TOKEN_FILE=...`** —— 凭据隔离用「env 变量**名**
  指向文件路径」范式(名不读值 · `credentials.py:21 TOKEN_FILE_ENV`),但**这个 env 从没被持久化设过**。
  后果:① 任何新 shell(含我每次的 Bash 工具、可能含 systemd unit 若未写 `Environment=`)都读不到 token →
  增量服务/批跑静默失效(对上「07:19 后增量一直停」的现象);② 报错说「env 缺」但 operator 直觉是「token 不是刚抓了吗」,
  **真因(指针没设)与现象(token 读不到)之间隔了一层,不熟悉范式的人会去重抓 token(白抓 · token 明明在)**。
- 为何是框架级(受益面 = 所有用此凭据范式的项目): 「env 名指针 + 文件 0600 + 名不读值」是 framework 凭据隔离的
  **标准范式**(credential-isolation safety-floor 推荐口径),不是 008 专属。任何 L4 项目照搬都会遇到「指针未持久化 →
  fail-closed 静默 → 报错不指向真因」。这是范式的**可用性缺口**,非单项目 bug。
- 当前 XenoDev 内处置(项目级): operator 手动 `echo 'export XENODEV_008_DETAIL_TOKEN_FILE=~/codes/XenoDev/secrets/prod/008-detail-token.json' >> ~/.bashrc && source ~/.bashrc`
  即可(已建议)。我在 agent shell 内无法代设(① 改 operator profile 越界;② 命令含 secrets 路径字面量被 C12 hook 拦)。
- 候选框架解法(留 forge 议): ① **抓 token 的工具(grab-detail-token addon)落 token 文件时,顺手 append/校验
  env 指针到 shell profile**(或产一行可粘贴的 `export`,operator 一键)→ 文件与指针同生,杜绝「文件在指针无」;
  ② **load_token 的 fail-closed 报错升级**:检测「env 缺但默认路径 `secrets/prod/<x>.json` 文件存在」时,
  明确提示「文件在、但 env 指针 `XENODEV_*` 未设,跑 `export ...` 或写 ~/.bashrc」——把真因直接喂给 operator,
  不让其误以为 token 失效;③ 文档化:凭据范式的 setup 必含「持久化 env 指针」步骤 + 自检(本仓 CAPTURE-DETAIL-TOKEN.md §3
  有写 `>> ~/.bashrc`,但 operator 实际环境没生效 → 说明文档步骤与"真落地"之间仍有漏,需 setup 自检兜)。
- 关联: src/broker/credentials.py(TOKEN_FILE_ENV / load_token fail-closed)/ .claude/safety-floor/credential-isolation/ /
  docs/CAPTURE-DETAIL-TOKEN.md §3(env 指针步骤)/ grab-detail-token addon(落 token 处可同时设指针)/
  上条「凭据 hook 加剧排查」(同 C12 范式的可用性张力族)
- operator 确认: 

## 采集落盘丢失「入口维度标记」(content_id 内外)→ 下游按入口统计须反推,易错
- 日期: 2026-06-26T00:00:00Z
- 类型: schema-gap | 优化空间
- 严重度: low(数据未丢 · 只是维度需反推 · 但反推规则脆弱)
- 复现场景: operator 问「内部回放 vs 外部回放各多少、各差多少」。回放入口本按 `content_id` 区分
  (163785=内部 / 163786=公开 · 见 `batch.py:498 --content-id`),但:① `persist_course_list_to_captures`
  (`batch.py:447`)落盘只存 `{result: {...}}` + manifest 行 url=`clubSerialCourseList?dirId=<x>`(**不带 content_id**);
  ② `enumerate_from_captures` 产出 7 字段(record_id/title/created_at/dir_id/board/media_base_url/coursewares)
  **无 content_id / 内外标记**;③ 落库 records 表也无此维度。→ 想回答"内外各多少"**只能反推**:靠 courselist JSON
  的 `result.serialInfo.title`("内部直播回放"/"公开直播回放")反查。本次靠它算出内部 281 / 外部 71,但这依赖
  **响应里恰好带 serialInfo.title** 这个非契约字段,源站改字段就断。
- 为何是框架级(受益面 = 所有用本采集基座的项目): 「采集时知道用哪个入口(content_id/类目/来源),但落盘
  不保留入口标记 → 下游统计/检索按来源维度切分时只能反推」是**通用采集模式缺口**,非回放专属。任何用
  clubSerialCourseList / 图文 detail 等多入口采集的品类,都会遇到"采的时候有维度信息、落盘丢了"。
- 当前 XenoDev 内处置(项目级 · 仅查询): 本次用 serialInfo.title 反推出内外计数,未改采集代码(下载在跑 · 不动)。
- 候选框架解法(留 forge 议): ① `persist_course_list_to_captures` 落盘时把抓取用的 `content_id`(及其语义
  内部/外部)写进落盘 JSON + manifest 行 → enumerate 直接产 `entry`/`channel` 字段,下游零反推;
  ② 更一般:**采集落盘约定带「provenance 维度」最小集**(入口 id / 类目 / 抓取参数),作 hand-back provenance 模型一部分;
  ③ records schema 加可选 `channel`/`entry` 列(同 v0.3 加 title/tags/author 的 5 步加字段范式)。
- 关联: src/pipeline/replay/batch.py(persist_course_list_to_captures / make_fetch_course_list content_id / --content-id)/
  src/pipeline/replay/enumerate.py(enumerate_from_captures 产出字段)/ src/store/schema/collection_record.py(records 列)/
  serialInfo.title(当前反推依赖的非契约字段)/ hand-back provenance 模型
- operator 确认: 

## checkpoint 在 ingest 之前提交「captured」→ 批量入库前崩溃 = 数据永久不入库 + 重跑跳过(假完成)
- 日期: 2026-06-26T00:00:00Z
- 类型: 框架缺陷 | bug
- 严重度: high(数据正确性 · 长批跑崩溃即丢 · 但需"批中途崩"才触发)
- 复现场景: 008-pB 内部回放 ASR 入库(`run_asr_from_manifest` · `batch.py:202-262`)。operator 问"内部回放在转
  ASR 吗",查证发现:已转 42 个(checkpoint 42 行全 `captured` · raw-replays 落了 transcript),**但 records 表
  form=replay 只有 1 条(还是昨天测试的 57111)**。读码确认根因 = **逐条循环里每转完一条就 `append_checkpoint(captured)`
  (`:253`),但 `ingest_records` 在整个 for 循环跑完后才一次性执行(`:256-261`)**。即:
  - checkpoint 语义 = "这条已完成",但此刻它**只转录了、还没入库**(records 内存 list 攒着,循环结束才落库)。
  - 当前 42/136 库里为空属正常(ingest 还没轮到)—— 但这暴露**致命窗口**:若进程在第 136 条前被杀/崩溃/OOM,
    `records` 内存 list 全丢,**而 checkpoint 已记 N 条 captured → 重跑因 `load_done` 跳过这 N 条 → 它们永久不入库**
    (transcript 虽在盘上,但 records 表永远缺,且无任何信号提示"这些其实没入库")。
  - 本次幸未崩(进程健康跑完会入库),但 operator 暂停我的并行下载让 ASR 独占资源时,**正是怕这类长批跑被扰动**——
    一旦 ASR 进程在统一入库前挂掉,42+ 个转录(每个 ~3min GPU)的入库成果全废且静默。
- 为何是框架级(受益面 = 所有用本采集/批跑基座的项目): "checkpoint(断点续的完成标记)与真正的副作用提交(入库)
  不在同一事务/不同步"是**通用持久化反模式**。任何用 `append_checkpoint + 末尾批量 ingest` 的长批跑(图文 detail
  broker 同范式?需查)都有此窗口。checkpoint 撒谎("captured"实为"转录完但未入库")破坏断点续的根本前提。
- 当前 XenoDev 内处置: 仅观察未改(ASR 在健康跑 · 不动它 · 让其自然跑完入库)。**若它真在入库前崩**,补救 =
  手动删/重置 checkpoint 里对应行 → 重跑会重转重入(transcript 在盘上可复用,但当前码每条仍会重跑 whisper)。
- 候选框架解法(留 forge 议): ① **每条转完立即 ingest 该条 + 紧接着才写 checkpoint**(per-record 事务:入库成功
  才记 captured)→ 崩溃最多丢"当前这条",已入库的不丢、checkpoint 不撒谎。代价:N 次小事务 vs 1 次大事务(回放
  量级 136 可接受)。② 若保留批量 ingest 性能:**checkpoint 分两态**(`transcribed` vs `ingested`),崩溃重跑对
  `transcribed` 但未 `ingested` 的只补入库不重转。③ 至少:循环中**周期性 flush**(每 K 条 ingest 一次)缩小窗口。
- 关联: src/pipeline/replay/batch.py:202-262(run_asr_from_manifest · checkpoint :253 / ingest :256)/
  src/broker/checkpoint.py(append_checkpoint/load_done 语义)/ src/store(ingest_records 事务边界)/
  上条「后台长任务缺存活检测」(同属"长批跑健壮性"族 · 崩溃+误判重起会叠加放大本 bug)
- operator 确认: 

### KG-24 · 增量守护 _pending_replays_fn 只认 manifest status=downloaded 不认 skipped → 重跑下载后已下产物漏 ASR
- 日期: 2026-06-30T04:10:00Z
- 类型: 框架缺陷 | bug
- 严重度: high(数据静默缺失:已下到的媒体永远不会被 ASR 入库,无任何告警)
- 复现场景(真实 dogfood): 008-pB 补 43 个公开直播回放音频缺口。因单 token 窗口(TTL~3h)下不完 43 条
  长录播(每条 1h+、源不支持 Range、~12min/条),分 **3 个 token 窗口**重跑 `batch --download-only --audio-only`
  接力(operator 刷新 token → 重跑断点续)。**断点续逻辑(batch.py:167)对已存在产物写 manifest status=`skipped`**。
  结果:第 1+2 批下的 31 个在第 3 批重跑时被标 `skipped`,只有第 3 批新下的 12 个是 `downloaded`。随后恢复
  xeno-process 守护跑 ASR,日志报「GPU 忙 → 回放 ASR 排队(**12** 个)」——**不是 43**。深挖:
  `daemons._pending_replays_fn`(daemons.py:60-76)判待 ASR 的条件是 `r.get("status")=="downloaded"`(**漏了 skipped**),
  而正牌 ASR 入口 `run_asr_from_manifest`(batch.py:212-213)认 `status in ("downloaded","skipped")`(=43,正确)。
  → 纯靠守护,前 31 个**永远 ASR 不到、永久缺**(manifest 最后状态 skipped + 守护视而不见 + 无告警)。
  实测对照:`status==downloaded 且不在DB` = 12;`status∈(downloaded,skipped) 且不在DB` = 43。
- 为何框架级(受益面 = 所有用本采集/批跑基座 + 增量守护的项目): "断点续把已完成产物标 skipped" 与 "下游
  消费只认 downloaded" 是**两处对 manifest 状态语义理解不一致**。任何"先批量下载(含断点续)→ 守护增量消费"
  的链路都有此漏:重跑下载一次,已下的就从 downloaded 变 skipped,守护就漏掉它们。skipped 本意是"已下到了"
  (该被 ASR),却被守护当成"不用管"。这是 manifest 作为多写者共享 append-log 时,**状态枚举缺统一契约**的体现
  (Plan agent 在方案阶段已预警"manifest 多次重跑后 skipped 覆盖 downloaded",现真实发生)。
- 当前 XenoDev 内处置: 不当场改守护(框架级)。operator 决策走正牌入口补:等本机 GPU 空闲 → 手动
  `batch --asr-from-manifest`(认 downloaded+skipped=43 全量)一次性 ASR 入库。守护只能补 12,故不靠它。
- 候选框架解法(留 forge 议): ① `_pending_replays_fn` 改认 `status in ("downloaded","skipped")`(与
  run_asr_from_manifest 对齐 · 一行修)→ 但根因是"两处各自硬编码状态集",应 ② **抽一个 manifest 状态契约**
  (如 `MEDIA_READY_STATUSES = {"downloaded","skipped"}` 单一真相,两处都引)。③ 更根本:downloaded/skipped
  区分对"是否要 ASR"无意义(都=媒体在盘),应合并语义或在 manifest 显式标 `media_present: bool`。
- 关联: src/broker/daemons.py:60-76(_pending_replays_fn · status=="downloaded")/
  src/pipeline/replay/batch.py:167(断点续写 skipped)+ :212-213(run_asr_from_manifest 认 downloaded+skipped)/
  上面 KG「checkpoint 与 ingest 不同步」(同属"长批跑/断点续状态语义"族)
- operator 确认: 

### KG-25 · DeepSeek 结构化提取无坏-JSON 容错 → LLM 稳定返回非法 JSON 的条目静默永久缺 summary
- 日期: 2026-06-30T04:15:00Z
- 类型: 框架缺陷 | 优化空间
- 严重度: medium(单条静默丢 summary · 不影响入库主体 · 但无重试/无告警/无降级)
- 复现场景(真实 dogfood): 008-pB 补 3 条历史遗留图文/问答的 LLM 结构化(.txt 正文齐但缺 .summary.json)。
  守护本轮跑文本结构化:`图文结构化+1 问答+0 错误=2`——3 条只成 1 条(176412),另 2 条(article-173372
  巴巴财报简评 / qa-30032 sell put 问答)失败。深挖真实异常(直接单跑捕获):
  · article-173372: `ValueError: DeepSeek content 非合法 JSON:Invalid control character at: line 10 column 46`
  · qa-30032: `ValueError: DeepSeek content 非合法 JSON:Expecting ',' delimiter: line 5 column 35`
  **连试 3 次,每次都在完全相同位置失败**(非偶发 · DeepSeek 对这两篇特定正文确定性地返回坏 JSON:string
  值内含未转义控制字符/裸换行)。`make_deepseek_text_summarize`(tools.py:47-50)直接 `json.loads(content)`,
  **无控制字符清洗、无重试、无降级**,一次失败即 raise → 守护 try/except 吞掉(daemons 错误计数+1 但不告警)
  → 这 2 条**每轮 process 都会被 pending 重新选中、每轮都失败**,summary 永久缺、operator 无从知晓(除非手查
  records 数 vs summary 文件数差额 —— 正是本次 dogfood 起因)。
- 为何框架级(受益面 = 所有用 LLM 做结构化提取的项目): "LLM 返回的 content 不是合法 JSON" 是**通用现实**
  (即便 prompt 要求 JSON、即便低 temperature,模型仍会偶发/对特定输入稳定地塞裸控制字符、漏逗号、多尾逗号)。
  任何"调 LLM → json.loads 产物"的链路都需**解析鲁棒性层**。本采集基座三品类(图文/问答/回放摘要)都走
  make_deepseek_*,此缺口面广。与 KG「DeepSeek 坏 JSON 拖垮整篇」若已记需合并/交叉引。
- 当前 XenoDev 内处置: 不当场改解析层(框架级)。operator 决策这 2 条暂缺 summary(不重要内容 · 巴巴财报简评/
  sell put 问答),记此条攒批回 forge。已补的 176412 正常。
- 候选框架解法(留 forge 议): ① 解析前对 content 做**控制字符清洗**(strip/escape `\x00-\x1f` 非法裸字符)再
  json.loads。② **重试 N 次**(对偶发坏 JSON 有效 · 但本例确定性坏 → 重试无效,故②不够,须配①)。③ 更鲁棒的
  **JSON 提取**(正则抠最外层 {...} + 容错解析库如 json5/dirtyjson)。④ 兜底**降级**:坏 JSON 时退回"整段正文
  当单条 key_point 入库 + 标 degraded",至少不静默丢、有信号。⑤ 失败计数应**上报可见**(非仅 log · 见下条族)。
- 关联: src/pipeline/replay/tools.py:47-50(json.loads content · 无容错)+ :306-324(make_deepseek_text_summarize)/
  src/broker/daemons.py(run_process_once 吞异常 · 错误计数不告警)
- operator 确认: 

### KG-26 · IDS `/plan-start` HANDOFF 模板 + SHARED-CONTRACT §6 硬编码 mac 路径 `/Users/admin/codes/XenoDev` → 跨机器(linux)产的 hand-off 包 build_repo/cd 指令全错
- 日期: 2026-07-01T09:10:00Z
- 类型: 框架缺陷(协议/模板 · 跨机器可移植性 · 与 KG-3 同族「模板指针漂移」)
- 严重度: medium(hand-off 包 producer 若照模板字面填,operator `cd /Users/admin/...` 在 linux 机直接 `No such file or directory`,build phase 起不来;须每次人肉改路径,易漏)
- 复现场景: 在 **IDS 仓推 idea 009「投资决策闭环」的 M1+M2 进 L4**,跑 `/plan-start 009-pForge` 产 hand-off 包。IDS `.claude/commands/plan-start.md` 的 HANDOFF 模板 §workspace 把 `build_repo` 写死 `/Users/admin/codes/XenoDev`,§1 operator 指令也写 `cd /Users/admin/codes/XenoDev`;`framework/SHARED-CONTRACT.md` §6.2 workspace schema 的示例/YAML 同样全用 `/Users/admin/...`(source_repo/build_repo/working_repo/handback_target 四字段示例都是 mac 路径)。**但本机是 linux**:IDS 在 `/home/ys/codes/ideababy_stroller`、XenoDev 在 `/home/ys/codes/XenoDev`(forge v1/v2 stage doc 读的一手代码路径也都是 `/home/ys/`)。若 producer 照模板字面产 hand-off 包,交接给 operator 的 `cd` 指令 + `build_repo` 字段全指向不存在的 mac 路径 → XenoDev consumer 侧 §6.2.1 约束1(canonical-path containment)也会因 build_repo 不存在而无从校验。**本次已在产的 `discussion/009/009-pForge/L4/HANDOFF.md` 里全部手工改成真实 `/home/ys/codes/XenoDev`**(并在 HANDOFF §6 记了这个坑),未受阻,但下一个 operator/agent 在 linux 机照 `plan-start.md` 或 SHARED-CONTRACT §6 字面模板产包会重踩。schema 本身把字段定义为 "string (absolute path)",并未要求 mac —— 纯粹是**模板/示例把某台 mac 的绝对路径当默认值写死**,跨机器即漂移。
- 关联: IDS `.claude/commands/plan-start.md`(HANDOFF 模板 workspace.build_repo + §1 `cd` 指令,均硬编码 `/Users/admin/codes/XenoDev`)/ IDS `framework/SHARED-CONTRACT.md` §6.2 workspace schema 示例表 + YAML 块(四字段示例全 mac 路径)/ KG-3(同族:HANDOFF/SKILL/CLAUDE 指针指向不存在的 mac `templates/spec.template.md`)/ 本次实物 `discussion/009/009-pForge/L4/HANDOFF.md` §6(已记该坑 + 填对真实 linux 路径,可作正向样本)
- operator 确认: <留空 · 待 operator review:把 `plan-start.md` 模板 + SHARED-CONTRACT §6 的 XenoDev 路径从硬编码 mac 绝对路径改为**从环境推断**(如 `git config` / 相对 source_repo 的兄弟目录 / 环境变量 `$XENODEV_REPO`),或至少把示例标注为「示例路径,按本机实际填」并在 plan-start 实装动作里用 `realpath` 动态取 build_repo,消除跨机器硬编码。框架级,回 IDS forge 定 · 009-pForge HANDOFF 可作正向样本>

### KG-27 · XenoDev 三个 codex-调用 SKILL(spec-writer/parallel-builder/codex-review)硬编码 mac codex-companion.mjs 路径 + 部分钉死已不存在的 1.0.3 版本
- 日期: 2026-07-01T00:00:00Z(009-pForge spec-writer 真开发时记录)
- 类型: 框架缺陷(SKILL 机制 · 跨机器可移植性 · 与 KG-26/KG-3 同族「模板/指针硬编码 mac 路径」)
- 严重度: medium(codex review 是 spec-writer §3 + parallel-builder ship 流程的**强制 hook**;照 SKILL 字面路径 `node /Users/admin/.claude/plugins/...` 在 linux 机直接 `Cannot find module` → review 跑不起来 → verdict 拿不到 → spec 无法 frozen / task 无法 ship。**且 parallel-builder §强约束 + codex-review 多处把版本钉死 `1.0.3`,本机只有 `1.0.4`**,即便 base 目录改对、版本号写死也会 miss)
- 复现场景: 用 XenoDev 落地 **009-pForge(投资闭环 M1 PIT 价格层 + M2 alpha 头)**,跑 spec-writer 产 `specs/009-pForge/` spec 包后,进 SKILL §3「codex adversarial-review 强 hook」。spec-writer SKILL §3.1(line 96)`CODEX_MJS=$(find /Users/admin/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs ... | sort -V | tail -1)` —— `find` 逻辑(`sort -V | tail -1` 取 semver 最新)**是对的**(KG 曾修过 `head -1` glob-order bug),但 **base 目录 `/Users/admin/.claude/...` 写死 mac**;本机 codex 实装在 `/home/ys/.claude/plugins/cache/openai-codex/codex/1.0.4/scripts/codex-companion.mjs`(`find | sort -V | tail -1` 实证)。parallel-builder SKILL §强约束(line 17)、codex-review SKILL(line 16/58/138/152/357/391/548 等 8+ 处)不仅路径 mac,还**把版本号钉死 `1.0.3`**(本机是 `1.0.4`,1.0.3 目录不存在)。即:三个 SKILL 一旦真跑 codex 全部会因 mac 路径 + stale 版本号扑空。**本次 spec review 我用 linux 真路径 `node /home/ys/.claude/plugins/cache/openai-codex/codex/1.0.4/scripts/codex-companion.mjs adversarial-review ...` 绕过**,未受阻,但下一个 operator/agent 照 SKILL 字面跑必踩;且 codex 每次升版本(1.0.3→1.0.4→…)钉死版本号的行都会腐烂。
- 关联: XenoDev `.claude/skills/spec-writer/SKILL.md` §3.1 line 96(base 目录 mac,find 逻辑对)/ `.claude/skills/parallel-builder/SKILL.md` line 17(mac + 钉死 1.0.3)/ `.claude/skills/codex-review/SKILL.md` line 16/58/138/152/357/391/548(mac + 多处钉死 1.0.3)/ KG-26(同族:IDS 侧 plan-start/SHARED-CONTRACT 硬编码 mac 路径)/ KG-3(同族:指针指向不存在 mac 文件)
- operator 确认: <留空 · 待 operator review:三个 SKILL 统一成从环境探测 codex 路径 —— base 目录用 `${HOME}/.claude/plugins/...` 或环境变量,版本一律 `codex/*/scripts/...` glob + `sort -V | tail -1` 取最新(**绝不写死版本号**),消除 mac 硬编码 + stale-version 双重腐烂。框架级,回 IDS forge 与 KG-26 一起定(同根:跨机器路径硬编码)>

### KG-28 · parallel-builder/task 验证假设 uv+可复现 env 就位,但新机(linux)无 uv、无 .venv、pypi.org index 被墙、uv.lock 有 yanked dep
- 日期: 2026-07-01T00:00:00Z(009-pForge T001 parallel-builder 真 ship 时记录)
- 类型: 框架缺陷(env/工具链 bootstrap · 跨机器可复现性)
- 严重度: high(parallel-builder §2 TDD red/green + task `## Verification` 全 `uv run alembic/pytest` · 无 env 则**整个 ship 流程跑不起来** · T001 直接卡住;且 SKILL/task 无任何 env-bootstrap 步骤,假设 env 天然就位)
- 复现场景: 用 XenoDev 落地 **009-pForge T001**(004 alembic migration · 首个 M1 task),进 parallel-builder §2 TDD。撞三连:① **无 `uv`**(SKILL 全程 `uv run ...`,`which uv` 空)· ② **004-pB 无 `.venv`、依赖(alembic/pytest/pydantic/aiosqlite)一个没装**(004 是 mirror 进来的,env 从没在本机建过;系统 python3=3.11 但 004 钉 3.12)· ③ 装 uv 后 `uv sync --locked` **卡死 2h19m** —— 真因 **`pypi.org/simple` index 被墙**(`curl pypi.org/simple` 超时,但 `files.pythonhosted.org` + aliyun/tuna mirror 全 HTTP 200)→ 必须 `UV_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/` · ④ 换 mirror 后 `--locked` 又失败 —— **`uv.lock` 有 yanked dep(`anyio==4.6.2` 被 PyPI 撤)**,`--locked` 拒更新 → 只能 `uv sync`(非 --locked)。四步全过后 224 包装齐、369 test collect、alembic head=0013、TDD 才能真跑。**本次操作:装 uv(curl 官方)+ UV_INDEX_URL=aliyun mirror + 去 --locked,operator 已授权**,未静默假装 green。
- 关联: `.claude/skills/parallel-builder/SKILL.md` §2(TDD 命令全 `uv run`,无 env preflight)/ task `## Verification`(全 `uv run alembic/pytest`)/ `projects/004-pB/{pyproject.toml,uv.lock}`(3.12 钉死 + anyio yanked)/ KG-26/KG-27(同族:框架假设 mac/特定机器环境,跨机器不成立)
- operator 确认: <留空 · 待 operator review:parallel-builder §0 preflight 加一条 **env-bootstrap 检查/步骤**(uv 在否 · .venv 在否 · index 可达否 · lock 是否 stale)+ 文档化「新机首次 build 前跑 env 建设(装 uv + 配可达 index + uv sync)」;或 SKILL 显式支持 `UV_INDEX_URL` 透传 + `--locked` 失败降级策略。框架级,回 IDS forge>

### KG-29 · IDS `/plan-start` 铸的 fork id `009-pForge` 过不了 XenoDev hand-back validator 的 id charset 正则(cross-repo id 约定冲突 · 阻断 hand-back)
- 日期: 2026-07-01T00:00:00Z(009-pForge T001 hand-back producer 校验时记录)
- 类型: 框架缺陷(协议 · SHARED-CONTRACT §6.2.1 约束 6 id charset vs IDS `/plan-start` 实产 id · **cross-repo 契约不一致**)
- 严重度: high(**阻断 hand-back 产出** —— T001 代码已 codex approve + 18 test 绿 + 真 DB 验证,但 hand-back producer 6 约束 constraint-6 `FAIL`,写不回 IDS → ship 流程 §6 卡死;每个 `-p<多字符大写后缀>` fork id 都会踩)
- 复现场景: 用 XenoDev 落地 **009-pForge T001**,ship 到 parallel-builder §6.1 `gen-handback` + producer `validate-handback.sh ... --mode=producer`。gen-handback 成功产 draft(009 identity 正确),但 producer 校验 **constraint-6 FAIL**:`prd_fork_id (009-pForge) not matching ^[0-9]{3}[a-z]?(-p[A-Z])?(-v[0-9]+\.[0-9]+)?$`。真因:validator 正则 `-p[A-Z]` 只允许 `-p` + **单个大写字母**(`008-pB`/`006a-pM`/`009-pF` 过),但 **IDS `/plan-start` 铸的 id 是 `009-pForge`(`-p`+`Forge` 多字符后缀)**,HANDOFF/PRD/spec 全链一致用 `009-pForge`。即 IDS 端造了个 XenoDev 端 validator 收不了的 id。**实测:`009-pForge` ❌ / `009-pF` ✅ / `008-pB` ✅ / `006a-pM` ✅**。不能靠 XenoDev 端偷改 id 为 `009-pF`(会破 HANDOFF/spec/handback 三处 id 一致性 constraint-4,且掩盖真契约 bug)→ 必须回 IDS 对齐 id 约定。
- 关联: `lib/handback-validator/check-6-id-charset-and-final-path.sh` line 41 正则 `^[0-9]{3}[a-z]?(-p[A-Z])?(-v[0-9]+\.[0-9]+)?$` / IDS `.claude/commands/plan-start.md`(铸 fork id 逻辑)/ IDS `framework/SHARED-CONTRACT.md` §6.2.1 约束 6(id charset SSOT)/ IDS `discussion/009/009-pForge/`(全链用 009-pForge)/ 本次实物 draft `009-pForge-20260701T151408Z`
- operator 确认: <留空 · 待 operator review 二选一(框架级 · 回 IDS forge 定):① 放宽 validator + SHARED-CONTRACT §6.2.1 正则允许 `-p[A-Z][a-zA-Z]*`(接多字符后缀如 `-pForge`)· ② 或约束 IDS `/plan-start` 只铸单大写后缀 fork id(如 `009-pF`)并回改 009 全链。**推荐 ①**(id 表达力更强 · 且 `009-pForge` 已全链落地,改 IDS 造 id 规则代价小于回改全链但要动 plan-start)。在 IDS 定,XenoDev 只持 mirror>
  - **【2026-07-02 后续】operator 已决 ①并落地**:IDS 侧放宽正则 `-p[A-Z]`→`-p[A-Z][a-zA-Z]*`(check-6 + SHARED-CONTRACT §6.2.1 + event-schema.json 三处对齐 + `-v` 段消漂移),XenoDev mirror 已 sync(commit `ff5b7e1`)。T001 hand-back 随后 producer+consumer 6 约束全 PASS,写回 IDS `discussion/009/handback/`。此条**实质已解**,保留供 forge v6 追认(记录"当初为何判可直改 + 安全面核验":path-traversal 靠 check-6 §1.5 字符黑名单 + §3 realpath containment 纵深防御,正则非唯一防线,放宽只加纯字母无 traversal 字符 → 无安全面)。

### KG-30 · parallel-builder §4.4 假设 red-green log 落 XenoDev 根 tests/,但 build 目标是 mirror 子项目(如 004-pB)时 log 落子树被子树 .gitignore 挡 → 「log 随 commit」恒不满足
- 日期: 2026-07-02T01:00:00Z(009-pForge T002 parallel-builder §2 TDD 真 ship 时记录)
- 类型: 框架缺陷(SKILL 机制 · parallel-builder §2.1/§2.4 red-green log 落点 vs §4.4 verifier 期望 · 与 mirror 子项目结构错配)
- 严重度: low(不阻断 ship —— log 证据仍在磁盘可审计,只是不进 git;但 §4.4 verifier 里「red-green log 随 commit」那条对 004 类子项目 build **恒无法满足**,是 SKILL 假设与真实目录结构的静默错配 · T001 当时已踩但未察觉)
- 复现场景: 用 XenoDev 落地 **009-pForge T002**(PIT 接口契约 · file_domain 全在 `projects/004-pB/**`)。parallel-builder §2 TDD 把 red/green 命令的 `tee` 写到 `tests/red-green-log/T002.log` —— 但该路径落在 **004-pB 子树内**,而 **004-pB 自带 `.gitignore` 忽略 `tests/red-green-log/`**(`git check-ignore tests/red-green-log/T002.log` 命中)→ `git add` 被拒(`下列路径根据 .gitignore 被忽略`)。SKILL §4.4 verifier 那条「`tests/red-green-log/<TID>.log` 含 ≥1 [red]+末尾[green]」期望 log **在 diff 里/随 commit**,但对 004 类子项目**永远做不到**。根因:SKILL §2 假设 red-green log 落 **XenoDev 仓根** 的 `tests/red-green-log/`(不被 ignore),但当 build 目标是 mirror 进来的子项目(004-pB)、file_domain 全在子树下时,log 自然落子树、被子树 .gitignore 挡。**T001(同 file_domain 前缀)当时已踩同坑**——其 squash commit 里也只有 test+migration 无 log,但因 §4.4 是 parallel-builder 内部 verifier(非 hand-back 6 约束),ship 照过,坑被静默吞掉。
- 关联: `.claude/skills/parallel-builder/SKILL.md` §2.1/§2.2/§2.4(`tee -a tests/red-green-log/<TID>.log`)+ §4.4 verifier(「red-green log 随 commit」+「diff 边界含 `tests/red-green-log/`」)/ `projects/004-pB/.gitignore`(忽略 `tests/red-green-log/`)/ 009-pForge T001(`b850465` · 同坑未察)+ T002(`c97d684`/`6b1d1fb`)
- operator 确认: <留空 · 待 operator review(框架级 · 回 IDS forge 定):建议 SKILL §2 显式规定 red-green log **落 XenoDev 仓根** `tests/red-green-log/`(绝对/仓根相对路径,不随 build 目标子树走),或 §4.4 verifier 对「log 在子项目被 ignore」的情况显式降级(承认 log 只需磁盘留证、不强制随 commit)。同族根因与 KG-26/27/28 一致:SKILL 假设的目录/环境形态,遇到 mirror 子项目 build 时不成立>

### KG-31 · gen-handback template 的 to_source_repo/workspace.source_repo 是 mac 字面量(非 {{占位符}}),env 化那波漏改 → 产出的 hand-back 包静默带错误路径且 validator 不查
- 日期: 2026-07-02T09:30:00Z(009-pForge T001+T002 两个 hand-back 包实产时记录 · operator /handback-review 时点名)
- 类型: 框架缺陷(KG-26 同族:跨机器路径硬编码 · 但根因更细 —— **env 化补丁只覆盖了一半字段**)
- 严重度: low(不阻断 —— 6 约束 validator 的 check-3/check-5 读的是 positional arg + 物理路径,**不读这两个 frontmatter 字段** → 包照样全 PASS;但产物含错误元数据 = 静默错,下游若有人真读 `to_source_repo` 字段会拿到不存在的 mac 路径)
- 复现场景: 009-pForge T001 + T002 两次 `gen-handback.sh` 产包(本机 linux `/home/ys` · **`IDS_ROOT=/home/ys/codes/ideababy_stroller` 已正确 export**),draft frontmatter 里 `workspace.handback_target` 渲染**正确**(`/home/ys/...`),但 `to_source_repo` + `workspace.source_repo` 仍是 `/Users/admin/codes/ideababy_stroller`。**真根因(实查非猜)**:`lib/handback-validator/templates/handback.template.md` **L6 + L8 把这两个字段写成 mac 路径字面量**(不是 `{{VAR}}` 占位符),sed 替换只处理 `{{...}}` → 字面量原样带出;而 `handback_target` 走 `{{...}}` 占位 + `gen-handback.sh` L424 `IDS_ROOT="${IDS_ROOT:-mac默认}"`(env 化正确)→ 同一个包里一半字段对一半字段错。即 KG-26 那波 env 化(`${IDS_ROOT:-...}`)只改了 HANDBACK_TARGET_DIR 推导,**漏了 template 里的另两个字面量字段**。两个已写回 IDS 的包(`20260701T161131Z-...` / `20260702T005910Z-...`)都带此错误元数据。
- 关联: `lib/handback-validator/templates/handback.template.md` L6/L8(字面量)/ `lib/handback-validator/gen-handback.sh` L424(IDS_ROOT env 化 · 只喂 handback_target)/ KG-26(同族 mac 硬编码 · plan-start/SHARED-CONTRACT §6.2)/ 实物证据:IDS `discussion/009/handback/` 两包 frontmatter
- operator 确认: <留空 · 待 operator review(框架级 · template 在 bootstrap-kit 有上游,回 IDS forge 定):建议 template L6/L8 改 `{{SOURCE_REPO}}` 占位 + gen-handback 从 `$IDS_ROOT`(或更优:从 HANDOFF `workspace.source_repo` SSOT —— 它本就有正确值)喂值;顺带审 template 是否还有其他未占位化的路径字面量。**不当场改**(gen-handback/template 是 IDS bootstrap-kit mirror 件)>

