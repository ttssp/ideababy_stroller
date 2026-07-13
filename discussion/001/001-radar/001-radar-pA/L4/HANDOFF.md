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
prd_version: "1.2"

handed_off_at: 2026-07-13T10:43:29Z
prd_source: /home/ys/codes/ideababy_stroller/discussion/001/001-radar/001-radar-pA/PRD.md
shared_contract_version_honored: 2.0
supersedes_handoff: 2026-07-11T14:19:30Z
---

# Hand-off · 001-radar-pA → XenoDev (per SHARED-CONTRACT §6 v2.0)

**Handed off at**: 2026-07-13T10:43:29Z(supersedes 2026-07-11T14:19:30Z 版,PRD v1.1→v1.2)
**PRD source**: /home/ys/codes/ideababy_stroller/discussion/001/001-radar/001-radar-pA/PRD.md(**v1.2**,commit 见 git log)
**Build repo**: /home/ys/codes/XenoDev(经 $XENODEV_REPO → sibling 优先级链解析;不硬编码)
**Workspace**: 见 frontmatter `workspace:` 块(§6.2 4 字段全填)
**Source repo identity**: 见 frontmatter `source_repo_identity:` 块(XenoDev 写 hand-back 前必须按 §6.2.1 约束 3 校验)
**SHARED-CONTRACT version honored**: 2.0

## §0 · v1.1→v1.2 delta(续建 hand-off · 先读本节)

这**不是**新项目 bootstrap——`projects/001-radar-pA/` 已存在(T001-T005 + T002-A1/T003-A1/T003-A2/T004-A1 全 shipped,254 tests green)。本 hand-off 由 operator 价值重定义(IDS injection @2026-07-13T10:43:29Z)触发,承载 PRD v1.2。spec-writer 做**增量 spec 修订**,不从零重写。

PRD v1.2 变化(全文见 PRD §Success O4 / §Scope OUT v1.2 注 / §Open questions #3 / §Moderator injection response v1.2 response):

1. **gate 硬门槛收敛为要件①②**:P0.2 判 PASS/FAIL 只看「真切片全判可信」+「负控被识伪」。`evaluate_gate` 的 `require_evidence_chain` 语义需改为 **record-not-block**(记录有无 new_evidence_chain,不作为 FAIL 依据)。
2. **要件③降级为使用期校准信号**:new_evidence_chain schema 保留;记录值进 O5 journal/taste 闭环(与 T010/T011 briefing/journal 设计衔接——"operator 知不知道"是使用中逐步学习的个人属性)。
3. **首跑证据处置(build 侧决定)**:P0.2 首跑(2026-07-11 signoff)①✅ ②✅——v1.2 语义下构成 PASS 证据。XenoDev 按自己的 anti-replay/run-binding 设计决定:(a) 复用首跑 signoff 按 v1.2 语义重判,或 (b) 快速新跑一轮(需 operator ~15 分钟盲判)。**RERUN-PASS artifact 机制不变,仍是 T010/T011 唯一前置**——只是判分标准变了,不是绕 gate。
4. **Candidate B 展望仅记档**:operator「跟踪动态/及时同步」诉求已记 PRD v0.2 展望;v0.1 scope 不变,T010/T011 仍按单次评估工具建。

**build 侧待办的直接推论**(spec/task 排布由 XenoDev 自定):evaluate_gate 语义调整(小任务)→ 首跑证据重判 or 快速重跑 → RERUN-PASS artifact → T010/T011 解锁。

## §1 · 给 XenoDev operator 的指令

operator 切到 build_repo 后:

1. `cd "$BUILD_REPO"`(= frontmatter `workspace.build_repo`,本机 `/home/ys/codes/XenoDev`)
2. 读本 HANDOFF.md(全文,**先 §0**)+ 引用的 PRD.md(v1.2)
3. 在 XenoDev session 触发 XenoDev 自带的 spec-writer(per XenoDev AGENTS.md;**不**调 IDS 的 spec-writer subagent — XenoDev 派生自己的)
4. spec-writer 对既有 spec.md 做**增量修订**(7 元素 schema;v1.2:gate 硬门槛收敛①② + 要件③ record-not-block + Candidate B 展望注记)
5. XenoDev task-decomposer 增补/调整 tasks/T*.md(evaluate_gate 语义调整、首跑证据处置、要件③记录值接 journal/taste 闭环)
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

(从 IDS PRD v1.2 §"Open questions" 分流;XenoDev build 自然遇到时再解决,不污染 spec frozen)

1. **P0.2 收口路径(v1.2 语义,最高优先)**:evaluate_gate 改 record-not-block 后,首跑证据(2026-07-11 signoff,①✅②✅)如何产 RERUN-PASS artifact——复用重判 or 快速新跑,由 build 侧按 anti-replay/run-binding 设计定;不得绕过 artifact 机制。多轮盲测转为可选的使用期校准活动(operator 有空时做,不阻塞)。
2. **延迟预算单档起步**(30 分钟初判 · O3):abstract 输入会增大 LLM 负载,若逼近 30 分钟预算再议分档;v0.1 仍单档。
3. **briefing 结论词表**:借 Tech Radar 四环(投入/试点/观察/暂缓)起步,v0.1 中后期拿真产出物非正式验证,不阻塞 spec。

## §5 · Rollback plan

如果 XenoDev build 失败:
- (a) 回到 IDS 修 PRD,重跑 `/plan-start`
- (b) 改 XenoDev spec(不改 IDS PRD),用 XenoDev 自己的修订机制
- (c) 起 forge 重新审整个 idea(重大架构转向必须回 IDS forge,防 V4 失败模式)
- (d) XenoDev 产 hand-back 包(tags: `prd-revision-trigger`)写回 IDS,operator 在 IDS 跑 `/handback-review 001` 决议
