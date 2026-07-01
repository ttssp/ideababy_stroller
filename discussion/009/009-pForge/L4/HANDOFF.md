---
# §6.2 workspace schema 4 字段(全必填)
# ⚠ 本机为 linux,XenoDev 实际在 /home/ys/codes/XenoDev(SHARED-CONTRACT §6.2 示例用的
#   /Users/admin/... 是 mac 路径,schema 定义为 "absolute path" — 此处填本机真实路径)
workspace:
  source_repo: /home/ys/codes/ideababy_stroller
  build_repo: /home/ys/codes/XenoDev
  working_repo: /home/ys/codes/ideababy_stroller
  handback_target: /home/ys/codes/ideababy_stroller/discussion/009/handback/

# §6.5 第 13 项 source_repo_identity 字段(由 IDS 产源时填入,XenoDev 写 hand-back 前必须验)
source_repo_identity:
  expected_remote_url: git@github.com:ttssp/ideababy_stroller.git
  repo_marker: "# Idea Incubator — Project C"
  git_common_dir_hash: 11c3749cc9465c4d

# Hand-off metadata
prd_fork_id: 009-pForge
discussion_id: 009
prd_form: phased
phases: [M1, M2]
modules: null
module_forms: null
critical_path_module: null
skip_rationale: null

handed_off_at: 2026-07-01T09:07:53Z
prd_source: /home/ys/codes/ideababy_stroller/discussion/009/009-pForge/PRD.md
shared_contract_version_honored: 2.0
---

# Hand-off · 009-pForge → XenoDev (per SHARED-CONTRACT §6 v2.0)

**Handed off at**: 2026-07-01T09:07:53Z
**PRD source**: /home/ys/codes/ideababy_stroller/discussion/009/009-pForge/PRD.md
**Build repo**: /home/ys/codes/XenoDev  ⚠ (本机 linux 真实路径;非模板 mac 占位 /Users/admin/...)
**Workspace**: 见 frontmatter `workspace:` 块(§6.2 4 字段全填)
**Source repo identity**: 见 frontmatter `source_repo_identity:` 块(XenoDev 写 hand-back 前必须按 §6.2.1 约束 3 校验)
**SHARED-CONTRACT version honored**: 2.0

## §0 · 这个 hand-off 是什么(给接手 operator 的 30 秒摘要)

009 = 投资决策闭环集合体 idea,经 forge v1(该不该建/怎么建)+ v2(目标态蓝图/分期路线)双轮收敛。
本 hand-off 交付 **Strangler Fig 前两期**:

- **M1 · PIT 价格历史层**(唯一关键新器官):日线 + 复权 + 退市感知 + as-of 契约。给回测提供
  唯一、干净、as-of 正确的历史股价 ground truth。
- **M2 · alpha 头**(闭环第一个可验证价值锚):产分析师 hit-rate / 超额 / DSR/PBO 报告,回答
  "某分析师到底有没有 alpha";alpha 得分作为独立 lane 平权进 004 conflict_reports。

**核心纪律(严守,勿越界)**:这是**围绕已 ship 的 004/008 松耦合生长的回测地基**,**不是**一个新建
的独立统一壳。M3 calibration 头 / 统一壳 / 图谱 / 蒸馏 **全部 defer,不在本 hand-off 范围**(见 PRD §5
Scope OUT)。build runtime 若把它们做进来 = 越界 = BLOCK。详见 PRD §0 定位 + §5。

## §1 · 给 XenoDev operator 的指令

operator 切到 build_repo 后:

1. `cd /home/ys/codes/XenoDev`  ⚠ (本机 linux 真实路径)
2. 读本 HANDOFF.md(全文)+ 引用的 PRD.md(`/home/ys/codes/ideababy_stroller/discussion/009/009-pForge/PRD.md`)
3. 在 XenoDev session 触发 XenoDev 自带的 spec-writer(per XenoDev AGENTS.md;**不**调 IDS 的 spec-writer subagent — XenoDev 派生自己的)
4. spec-writer 产 XenoDev 内部 spec.md(7 元素 schema,具体格式见 XenoDev `templates/spec.template.md`)
5. XenoDev task-decomposer 产 tasks/T*.md
6. parallel-builder 跑 task,quality gate 在 XenoDev 内部决议
7. 每个 task ship 后 XenoDev 产 hand-back 包(per §6.3 schema)写回 IDS `/home/ys/codes/ideababy_stroller/discussion/009/handback/`

## §2 · PRD-form 透传(XenoDev spec-writer 分派依据)

`prd_form: phased`,`phases: [M1, M2]`(详见 frontmatter)

- simple    → 标准 7 文件输出
- **phased  → SLA / risks 按 PRD `**Phases**` 数组分段** ← 本 hand-off 走这个
- composite → 顶层 spec.md 退化为 INDEX,额外为每 module 输出 spec-<m>.md
- v1-direct → SLA.md 顶部加 §'Skip rationale'

**phased 分派要点**:XenoDev spec-writer 产 SLA.md / risks.md 时,按 `[M1, M2]` **分两段**写 ——
M1 段(数据层:as-of 正确性 / 复权 / 退市覆盖风险)+ M2 段(alpha 头:trial-count / DSR 显著性 /
样本量风险),并写清 **M2 依赖 M1 数据层**、**M1 单独完成即有唯一行情地基**(每期独立可用)。

## §3 · §6.2.1 6 约束自检契约(XenoDev producer 写 hand-back 前必走)

per `framework/SHARED-CONTRACT.md` §6.2.1,XenoDev 产 hand-back 包写入
`/home/ys/codes/ideababy_stroller/discussion/009/handback/` 前,必须按 6 约束自检:

1. canonical-path containment(realpath prefix 校验)
2. symlink reject(路径任一段是 symlink 即拒)
3. repo identity check(三模式:remote / no-remote / hash-only,任一 PASS 即满足)
   - 本 hand-off 提供 remote(`git@github.com:ttssp/ideababy_stroller.git`)+ marker + hash 三者,
     XenoDev 任选一模式校验即可 PASS。
4. id consistency check(三处 id 严格一致:`prd_fork_id` / 路径 / hand-back filename)
5. id 字符集 + filename basename + final-path containment(OWASP path traversal 防御)
6. hard-fail(任一约束失败,producer 不写 / consumer 不读)

任一失败 = `Drop`(不写文件,不创目录,只 stderr)。

## §4 · Open questions for build phase

(从 PRD §11 "Open questions / 现实缺口" 分流的 build 相关项;XenoDev build 自然遇到时再解决,
不污染 XenoDev spec frozen。)

- **M1**:免费源退市覆盖是最大风险 —— 每个价格源的退市覆盖**实测验证**,别信文档(PRD §11 缺口①)。
  第一个源建议 A 股 BaoStock 或美股 Tiingo(看分析师主覆盖哪个市场);港股若非重点先暂缓。
- **M2**:分析师历史样本量可能不足以让 DSR 显著 → alpha 可能"判不出"。**这是闭环第一个价值锚,
  优先验证样本量够不够**(PRD §11 缺口②)。若判不出 → 触发 IDS 端重估(见 §5 rollback c/d)。
- **M2**:"beat 80-90% 同行"缺 baseline 样本池 → v0.1 可能只能给 vs 大盘绝对超额,给不出同行分位
  (PRD §11 缺口③,非本 hand-off 硬门槛)。

## §5 · Rollback plan

如果 XenoDev build 失败或撞到 §4 缺口:
- (a) 回到 IDS 修 PRD,重跑 `/plan-start 009-pForge`
- (b) 改 XenoDev spec(不改 IDS PRD),用 XenoDev 自己的修订机制
- (c) 起 forge v3 重新审整个 idea(尤其若 M2 证明分析师样本量根本判不出 alpha → 闭环前提塌)
- (d) XenoDev 产 hand-back 包(tags: `prd-revision-trigger`)写回 IDS,operator 在 IDS 跑
  `/handback-review 009` 决议

## §6 · ⚠ 已知框架级坑(交接注意 · 不阻塞本 hand-off)

`/plan-start` 命令模板 + `SHARED-CONTRACT §6.2` 示例**硬编码了 mac 路径 `/Users/admin/codes/XenoDev`**,
但本机是 **linux**,IDS 在 `/home/ys/codes/ideababy_stroller`、XenoDev 在 `/home/ys/codes/XenoDev`
(forge v1/v2 stage doc 读的也是 `/home/ys/` 路径)。

- **本 HANDOFF 已全部填对真实 linux 路径**,可直接使用。
- 但**这是框架级陈旧**(模板跨机器没更新)。按 IDS CLAUDE.md「dogfood 铁律」,框架级变更**只走
  forge**,不当场改 —— 建议 operator 记 dogfood-backlog,攒批回 IDS 起 `/expert-forge` 修
  `plan-start.md` + `SHARED-CONTRACT.md` 的路径(改成从 `git config` / 环境推断,不硬编码)。
