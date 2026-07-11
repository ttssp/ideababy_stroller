---
# §6.2 workspace schema 4 字段
workspace:
  source_repo: /home/ys/codes/ideababy_stroller
  build_repo: /home/ys/codes/XenoDev
  working_repo: /home/ys/codes/ideababy_stroller
  handback_target: /home/ys/codes/ideababy_stroller/discussion/001/handback/

# §6.5 第 13 项 source_repo_identity 字段(由 IDS forward 产源时填入,XenoDev 验)
source_repo_identity:
  expected_remote_url: "git@github.com:ttssp/ideababy_stroller.git"
  repo_marker: "# Idea Incubator — Project C"
  git_common_dir_hash: "11c3749cc9465c4d"

# Hand-off metadata
prd_fork_id: 001-radar-pA
discussion_id: "001"
prd_form: simple
prd_version: "1.1"

handed_off_at: 2026-07-11T14:19:30Z
prd_source: /home/ys/codes/ideababy_stroller/discussion/001/001-radar/001-radar-pA/PRD.md
shared_contract_version_honored: 2.0
supersedes_handoff: 2026-07-07T03:18:24Z
---

# Hand-off · 001-radar-pA → XenoDev (per SHARED-CONTRACT §6 v2.0)

**Handed off at**: 2026-07-11T14:19:30Z(supersedes 2026-07-07T03:18:24Z 版,PRD v1.0→v1.1)
**PRD source**: /home/ys/codes/ideababy_stroller/discussion/001/001-radar/001-radar-pA/PRD.md(**v1.1**,commit 6024159)
**Build repo**: /home/ys/codes/XenoDev(经 $XENODEV_REPO → sibling 优先级链解析;不硬编码)
**Workspace**: 见 frontmatter `workspace:` 块(§6.2 4 字段全填)
**Source repo identity**: 见 frontmatter `source_repo_identity:` 块(XenoDev 写 hand-back 前必须按 §6.2.1 约束 3 校验)
**SHARED-CONTRACT version honored**: 2.0

## §0 · v1.0→v1.1 delta(续建 hand-off · 先读本节)

这**不是**新项目 bootstrap——`projects/001-radar-pA/` 已存在(T001-T005 shipped & merged,95+ tests green)。本 hand-off 由 P0.2 盲测 gate 首判 **FAIL**(hand-back `001-radar-pA-20260711T135303Z`,prd-revision-trigger)触发,承载 PRD v1.1 修订。spec-writer 做**增量 spec 修订**,不从零重写。

PRD v1.1 四个变化(全文见 PRD §Success O4 / §Scope IN / §Open questions #3 / §Moderator injection response):

1. **O4 两层化**:P0.2 盲测 gate = 初始 smoke test(FAIL→STOP 铁律保留;PASS 解锁 Phase 1+ 但非可信性终审);长期信任主锚 = O2(3 击回溯)+ O5(journal 后验)。KG-B4 机器强制按此语义设计。
2. **要件③重 operationalize**:「新洞察」→「新证据链」= (i) operator 读前不知道的新事实 claim,或 (ii) 已知事实间未见过的结构连接;须可顺 O2 三击核验。gate 对答案逻辑(evaluate_gate)需同步此定义。
3. **语义切窗**(优先级上调,对应既有 T012 方向):切片边界贴领域结构事件,不按论文数量均分——首跑 FAIL 的直接诊断之一(slice-2/3 挤 2023 半年粒度)。
4. **分层阅读**:检索层全量元数据+abstract(LLM 提炼输入从 titles 扩到 abstract,OpenAlex `abstract_inverted_index` 重建);全文抓取只对位移锚点论文/O2 证据链核验时选择性深读(Scope OUT 红线:不做全量全文)。

**build 侧待办的直接推论**(spec/task 排布由 XenoDev 自定,此处仅陈述 PRD 级事实):
- T002-A1(封闭历史窗 `--from/--to-date`,102 tests green)ship 留后已解除——v1.1 确认历史窗回溯为盲测标准形态,可走 review→ship。
- P0.2 重跑协议:pipeline 落地 2/3/4 后重跑盲测(可换方向/换历史窗多轮,提升统计功效);重跑 PASS 才解锁 T010/T011。STOP 期间不建 Phase 1+ 管线。

## §1 · 给 XenoDev operator 的指令

operator 切到 build_repo 后:

1. `cd "$BUILD_REPO"`(= frontmatter `workspace.build_repo`,本机 `/home/ys/codes/XenoDev`)
2. 读本 HANDOFF.md(全文,**先 §0**)+ 引用的 PRD.md(v1.1)
3. 在 XenoDev session 触发 XenoDev 自带的 spec-writer(per XenoDev AGENTS.md;**不**调 IDS 的 spec-writer subagent — XenoDev 派生自己的)
4. spec-writer 对既有 spec.md 做**增量修订**(7 元素 schema;O4 两层化 + 要件③新定义 + 切窗/阅读原则)
5. XenoDev task-decomposer 增补/调整 tasks/T*.md(T012 语义切窗上调、abstract 输入、evaluate_gate 要件③同步、P0.2 重跑)
6. parallel-builder 跑 task,quality gate 在 XenoDev 内部决议
7. 每个 task ship 后 XenoDev 产 hand-back 包(per §6.3 schema)写回 IDS `<source_repo>/discussion/001/handback/`

⚠ **项目形态提示(非指令 · 供 spec-writer 参考)**:`projects/001-radar-pA/` 为既有独立 Python 项目(与 004/009 无代码关系),CLI 出 markdown briefing;重心是 **agent pipeline(检索/切片/briefing 生成)**,不是 UI。

## §2 · PRD-form 透传(XenoDev spec-writer 分派依据)

`prd_form: simple` → 标准 7 文件输出(本轮为增量修订,非全量重产)。

## §3 · §6.2.1 6 约束自检契约(XenoDev producer 写 hand-back 前必走)

per `framework/SHARED-CONTRACT.md` §6.2.1,XenoDev 产 hand-back 包写入 `<source_repo>/discussion/001/handback/` 前,必须按 6 约束自检:

1. canonical-path containment(realpath prefix 校验)
2. symlink reject(路径任一段是 symlink 即拒)
3. repo identity check(三模式:remote / no-remote / hash-only,任一 PASS 即满足)
4. id consistency check(三处 id 严格一致)
5. id 字符集 + filename basename + final-path containment(OWASP path traversal 防御;fork-id 语法 SSOT = SHARED-CONTRACT §7,v7 正则已接中段)
6. hard-fail(任一约束失败,producer 不写 / consumer 不读)

任一失败 = `Drop`(不写文件,不创目录,只 stderr)。

⚠ **已知坑预警(dogfood 在册,写包时留意)**:KG-31(gen-handback 模板 `to_source_repo`/`source_repo` 是 mac 字面量,产包 frontmatter 会静默带错路径——workspace 块以本 HANDOFF 为准)· KG-12(validator 校验传**绝对路径**,相对路径会误报约束 5)· gen-handback 记得传 `--section2/--section3`(T001-T005 五包 §2/§3 全「待补」,consumer 端只能靠 §1 决议)。

## §4 · Open questions for build phase

(从 IDS PRD v1.1 §"Open questions" 分流;XenoDev build 自然遇到时再解决,不污染 spec frozen)

1. **P0.2 重跑协议(由 v1.0 的「地基假设验证」演进而来,仍最高优先)**:pipeline 落地语义切窗 + abstract 输入 + 要件③新定义后重跑盲测;可换方向/换历史窗多轮提升统计功效(单轮 3 切片 1 负控瞎猜命中率 1/3)。重跑 PASS 才解锁 Phase 1+(T010/T011);FAIL → 再次 prd-revision-trigger STOP(不降级续建)。多轮的轮数/方向数由 operator 跑时定,不预设。
2. **延迟预算单档起步**(30 分钟初判 · O3):abstract 输入会增大 LLM 负载,若逼近 30 分钟预算再议分档;v0.1 仍单档。
3. **briefing 结论词表**:借 Tech Radar 四环(投入/试点/观察/暂缓)起步,v0.1 中后期拿真产出物非正式验证,不阻塞 spec。

## §5 · Rollback plan

如果 XenoDev build 失败:
- (a) 回到 IDS 修 PRD,重跑 `/plan-start`
- (b) 改 XenoDev spec(不改 IDS PRD),用 XenoDev 自己的修订机制
- (c) 起 forge 重新审整个 idea(重大架构转向必须回 IDS forge,防 V4 失败模式)
- (d) XenoDev 产 hand-back 包(tags: `prd-revision-trigger`)写回 IDS,operator 在 IDS 跑 `/handback-review 001` 决议
