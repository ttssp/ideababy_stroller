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
  git_common_dir_hash: "5244f0d135f23915"

# Hand-off metadata
prd_fork_id: 001-radar-pA
discussion_id: "001"
prd_form: simple

handed_off_at: 2026-07-07T03:18:24Z
prd_source: /home/ys/codes/ideababy_stroller/discussion/001/001-radar/001-radar-pA/PRD.md
shared_contract_version_honored: 2.0
---

# Hand-off · 001-radar-pA → XenoDev (per SHARED-CONTRACT §6 v2.0)

**Handed off at**: 2026-07-07T03:18:24Z
**PRD source**: /home/ys/codes/ideababy_stroller/discussion/001/001-radar/001-radar-pA/PRD.md
**Build repo**: /home/ys/codes/XenoDev(经 $XENODEV_REPO → sibling 优先级链解析;不硬编码)
**Workspace**: 见 frontmatter `workspace:` 块(§6.2 4 字段全填)
**Source repo identity**: 见 frontmatter `source_repo_identity:` 块(XenoDev 写 hand-back 前必须按 §6.2.1 约束 3 校验)
**SHARED-CONTRACT version honored**: 2.0

## §1 · 给 XenoDev operator 的指令

operator 切到 build_repo 后:

1. `cd "$BUILD_REPO"`(= frontmatter `workspace.build_repo`,本机 `/home/ys/codes/XenoDev`)
2. 读本 HANDOFF.md(全文)+ 引用的 PRD.md
3. 在 XenoDev session 触发 XenoDev 自带的 spec-writer(per XenoDev AGENTS.md;**不**调 IDS 的 spec-writer subagent — XenoDev 派生自己的)
4. spec-writer 产 XenoDev 内部 spec.md(7 元素 schema,格式见 XenoDev `templates/spec.template.md`)
5. XenoDev task-decomposer 产 tasks/T*.md
6. parallel-builder 跑 task,quality gate 在 XenoDev 内部决议
7. 每个 task ship 后 XenoDev 产 hand-back 包(per §6.3 schema)写回 IDS `<source_repo>/discussion/001/handback/`

⚠ **项目形态提示(非指令 · 供 spec-writer 参考)**:001-radar-pA 是 XenoDev 的**新独立项目**
(建议 `projects/001-radar-pA/`),与 004/009 的 Python 决策台无代码关系。PRD C2 定 v0.1 =
CLI/terminal 出 markdown briefing——技术栈由 XenoDev spec-writer 定,但注意本项目重心是
**agent pipeline(检索/图构建/briefing 生成)**,不是 UI。

## §2 · PRD-form 透传(XenoDev spec-writer 分派依据)

`prd_form: simple` → 标准 7 文件输出。

## §3 · §6.2.1 6 约束自检契约(XenoDev producer 写 hand-back 前必走)

per `framework/SHARED-CONTRACT.md` §6.2.1,XenoDev 产 hand-back 包写入 `<source_repo>/discussion/001/handback/` 前,必须按 6 约束自检:

1. canonical-path containment(realpath prefix 校验)
2. symlink reject(路径任一段是 symlink 即拒)
3. repo identity check(三模式:remote / no-remote / hash-only,任一 PASS 即满足)
4. id consistency check(三处 id 严格一致)
5. id 字符集 + filename basename + final-path containment(OWASP path traversal 防御)
6. hard-fail(任一约束失败,producer 不写 / consumer 不读)

任一失败 = `Drop`(不写文件,不创目录,只 stderr)。

⚠ **已知坑预警(dogfood 在册,写包时留意)**:KG-31(gen-handback 模板 `to_source_repo`/`source_repo`
是 mac 字面量,产包 frontmatter 会静默带错路径——workspace 块以本 HANDOFF 为准)· KG-12(validator
校验传**绝对路径**,相对路径会误报约束 5)。

## §4 · Open questions for build phase

(从 IDS PRD §"Open questions for L4 / Operator" 分流;XenoDev build 自然遇到时再解决,不污染 spec frozen)

1. **⚠ 最高优先 · 共享地基假设验证(本项目的 PPV 锚点)**:"公开脉络重建"能否产出**可信的**
   历史位移证据,L3 未验证,是本产品差异化的潜在返工点。**spec/task 排布必须把它排为最早的
   验证性任务**:对 1-2 个 operator 已深耕的方向重建 2-3 个历史时间切片 → operator 人工核验
   位移叙事是否可信。这个任务失败 = 触发 hand-back(tags: prd-revision-trigger),不要继续深挖管线。
2. **延迟预算单档起步**(30 分钟初判 · O3):要不要分快慢两档由 operator 自用数据决定,v0.1 不建两档。
3. **briefing 结论词表**:借 Tech Radar 四环(投入/试点/观察/暂缓)起步,最终词表 v0.1 中后期
   拿真产出物非正式验证,不阻塞 spec。

## §5 · Rollback plan

如果 XenoDev build 失败:
- (a) 回到 IDS 修 PRD,重跑 `/plan-start`
- (b) 改 XenoDev spec(不改 IDS PRD),用 XenoDev 自己的修订机制
- (c) 起 forge 重新审整个 idea(重大架构转向必须回 IDS forge,防 V4 失败模式)
- (d) XenoDev 产 hand-back 包(tags: `prd-revision-trigger`)写回 IDS,operator 在 IDS 跑 `/handback-review 001` 决议
