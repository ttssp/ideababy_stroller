---
# §6.2 workspace schema 4 字段
workspace:
  source_repo: /Users/admin/codes/ideababy_stroller
  build_repo: /Users/admin/codes/XenoDev
  working_repo: /Users/admin/codes/ideababy_stroller
  handback_target: /Users/admin/codes/ideababy_stroller/discussion/008/handback/

# §6.5 第 13 项 source_repo_identity 字段(由 IDS forward 产源时填入,XenoDev 验)
source_repo_identity:
  expected_remote_url: git@github.com:ttssp/ideababy_stroller.git
  repo_marker: "# Idea Incubator — Project C"
  git_common_dir_hash: 28d25bf82af4c0e2

# Hand-off metadata
prd_fork_id: 008-pB
discussion_id: 008
prd_form: phased
phases: [v0.1, v0.2]
modules: null
module_forms: null
critical_path_module: null
skip_rationale: null

handed_off_at: 2026-06-04T02:18:03Z
prd_source: /Users/admin/codes/ideababy_stroller/discussion/008/008-pB/PRD.md
shared_contract_version_honored: 2.0
---

# Hand-off · 008-pB → XenoDev (per SHARED-CONTRACT §6 v2.0)

**Handed off at**: 2026-06-04T02:18:03Z
**PRD source**: /Users/admin/codes/ideababy_stroller/discussion/008/008-pB/PRD.md
**Build repo**: /Users/admin/codes/XenoDev
**Workspace**: 见 frontmatter `workspace:` 块(§6.2 4 字段全填)
**Source repo identity**: 见 frontmatter `source_repo_identity:` 块(XenoDev 写 hand-back 前必须按 §6.2.1 约束 3 校验)
**SHARED-CONTRACT version honored**: 2.0

## §0 · ⚠️ 本 PRD 的特殊性(XenoDev spec-writer 必读)

008-pB 是一个 **phased PRD([v0.1, v0.2])**,且有两个非常规特征,spec-writer 必须重视:

1. **v0.1 含一个硬前置 gate(第 0 阶段探针)—— 不是普通 task,是"做不做得成"的门**:
   008 整个可行性押在"微信小程序里的图文 + 直播回放,能否在**不破解访问控制**(PRD C5 红线)的前提下
   可靠自动采集 + 下载视频"。**这个假设从未被验证。** spec-writer 应把 v0.1 的**第一个 task** 设计为
   独立的**可行性探针**(源头可达性 + 回放能否合规下载/转录 + 观察 1-2 周发布节奏),探针**通过才进
   主开发**。探针失败 → 产 hand-back(tag: `prd-revision-trigger`)写回 IDS,operator 可能退到 candidate A/C,
   **不要硬做**。详见 PRD §"关键前置 gate"。

2. **operator 对原始 Candidate B 有两处授权偏离**(见 PRD 顶部 + FORK-ORIGIN.md):
   - phase 排序"价值优先":v0.1 = 图文 + **回放**,v0.2 = 加预警(**回放在 v0.1,不在 v0.2**)。
   - 回放 v0.1 即做"下载视频 → 转文字 → LLM 关键点摘要"(**非**原始 B 的"存文件不转写")。
   spec-writer 以本 PRD 为准,**不要**回退到 stage doc 原始 B 的描述。

## §1 · 给 XenoDev operator 的指令

operator 切到 build_repo 后:

1. `cd /Users/admin/codes/XenoDev`
2. 读本 HANDOFF.md(全文)+ 引用的 PRD.md
3. 在 XenoDev session 触发 XenoDev 自带的 spec-writer(per XenoDev AGENTS.md;**不**调 IDS 的 spec-writer subagent — XenoDev 派生自己的)
4. spec-writer 产 XenoDev 内部 spec.md(7 元素 schema,具体格式见 XenoDev `templates/spec.template.md`),**按 phases [v0.1, v0.2] 分段**
5. XenoDev task-decomposer 产 tasks/T*.md(**v0.1 第一个 task = 可行性探针**,见 §0)
6. parallel-builder 跑 task,quality gate 在 XenoDev 内部决议
7. 每个 task ship 后 XenoDev 产 hand-back 包(per §6.3 schema)写回 IDS `/Users/admin/codes/ideababy_stroller/discussion/008/handback/`

## §2 · PRD-form 透传(XenoDev spec-writer 分派依据)

`prd_form: phased` · `phases: [v0.1, v0.2]`(详见 frontmatter)

- 本 PRD 是 **phased** → SLA / risks 按 PRD `**Phases**` 数组分段(v0.1 段 + v0.2 段)。
- v0.1 段须含探针 gate(§0)。v0.2 段(加预警 + 统一时间线 + 完整 004 契约)允许部分 `<待 v0.1 反馈后补>`。
- 参考其他形态(本 PRD 不适用):simple → 标准 7 文件;composite → spec.md 退化 INDEX + 每 module spec;v1-direct → SLA 顶部加 Skip rationale。

## §3 · §6.2.1 6 约束自检契约(XenoDev producer 写 hand-back 前必走)

per `framework/SHARED-CONTRACT.md` §6.2.1,XenoDev 产 hand-back 包写入 `/Users/admin/codes/ideababy_stroller/discussion/008/handback/` 前,必须按 6 约束自检:

1. canonical-path containment(realpath prefix 校验)
2. symlink reject(路径任一段是 symlink 即拒)
3. repo identity check(三模式:remote / no-remote / hash-only,任一 PASS 即满足;本 hand-off 已提供 remote + marker + hash 三者)
4. id consistency check(三处 id 严格一致:discussion_id=008)
5. id 字符集 + filename basename + final-path containment(OWASP path traversal 防御)
6. hard-fail(任一约束失败,producer 不写 / consumer 不读)

任一失败 = `Drop`(不写文件,不创目录,只 stderr)。

## §4 · Open questions for build phase

(IDS PRD 中**关于 build 路径选择**的 OQ 在此承载;XenoDev build 自然遇到时再解决,不污染 XenoDev spec frozen)

从 PRD §"Open questions for L4 / Operator" 分流的阻塞项:

- ⭐ **采集落点(本机 vs 云 vs 手机微信)** —— 探针(§0)后由 operator 拍板。三者须同时满足"源头可达 +
  低维护 + 合规(只采登录可见内容)"。GPT R2 提醒"云不是显然的可靠答案"。
- **回放管线可行性**:不破解前提下能否拿到 1-2 小时视频 → ASR → LLM 摘要。探针重点。
- **operator 可接受的延迟 / 维护动作量化**(每天确认一次?每周?完全无感?)→ 影响 v0.1 success 阈值。
- v0.2 待定:盘中预警与图文/回放是否同源(决定 v0.2 加预警成本)。

## §5 · Rollback plan

如果 XenoDev build 失败:
- (a) 回到 IDS 修 PRD,重跑 `/plan-start 008-pB`
- (b) 改 XenoDev spec(不改 IDS PRD),用 XenoDev 自己的修订机制
- (c) 起 forge 重新审整个 idea(`/expert-forge 008`)
- (d) XenoDev 产 hand-back 包(tags: `prd-revision-trigger`)写回 IDS,operator 在 IDS 跑 `/handback-review 008` 决议
- **特别地(本 PRD 高风险点)**:若 §0 探针证明"回放无法合规采集",走 (a)/(d) —— operator 可能把 008-pB
  退回 L3 重选 candidate A/C(只做图文/图文+预警,放弃回放),而非在 XenoDev 硬做撞红线。
