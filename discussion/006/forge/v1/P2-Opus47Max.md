# Forge v1 · 006 · P2 · Opus47Max · 参照系评估(with search)

**Timestamp**: 2026-05-07T15:25:00Z
**Searches run**: 4(SOTA-benchmark mode);全部对标 SOTA,无指定列表外项
**Visibility**: 我已读对方 P1(GPT55xHigh)。

---

## 1. SOTA 对标(表格)

| 标的 X' | 参照项(SOTA) | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| autodev_pipe v3.1 §错 2 "AGENTS.md 是根上下文" | Vercel AGENTS.md vs Skills 实证 | 8KB AGENTS.md = 100% Next.js 16 API eval 命中;Skills 顶 79%;**56% 情况 Skills 根本未被 activate**("activation problem") | autodev_pipe v3.1 已显式接住此结论 + 在 §0.2 错 2 + §1.3 路线 A 把 AGENTS.md 立为根 | 与 SOTA 一致 — autodev_pipe v3.1 是**已对齐 SOTA** 的设计;idea_gamma2 / vibe-workflow 都还是 CLAUDE.md 中心,**未对齐** | [vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals) |
| idea_gamma2 phase + retrospective + cross-model review | Cloudflare 7 子审查者 + coordinator | 7 专业子审(security/perf/quality/docs/release/compliance/AGENTS.md 合规)+ coordinator 去重判 severity;30 天 131,246 run / 48,095 MR / 5,169 repos;coordinator model 失败 hot-swap config 重试 | idea_gamma2 = Codex `/codex:adversarial-review` 单线对抗审 + Opus 自审;vibe-workflow = code-reviewer + tech-lead 双 agent 但**串行**而非分层 coordinator | gap 大 — 三套 X 都**没有 coordinator + 多专业子审分层**;autodev_pipe v3.1 §错 6 已识别此 gap 并改为"协调者+子审"但**未物化到 STARTER_KIT** | [blog.cloudflare.com/ai-code-review](https://blog.cloudflare.com/ai-code-review/) |
| autodev_pipe v3.1 §0.2 错 4 "上下文腐化阈值 300-400K token / 40% 利用率愚蠢区" | Anthropic context engineering "attention budget" | "context as a finite resource with attention budget — scarce, directional, deserving of engineering discipline";建议 high-signal-density 压缩 | autodev_pipe v3.1 已对齐(§0.4 第 2 条引此阈值);idea_gamma2 / vibe-workflow 都未显式做上下文预算 | 与 SOTA 一致 — autodev_pipe v3.1 数据真实;但**没有 starter kit 物化"自动检测 token 占用 + 触发压缩"机制**,只有静态阈值 | [anthropic.com/engineering/effective-context](https://www.anthropic.com/engineering/effective-context) |
| autodev_pipe v3.1 §0.2 错 5 "Opus 4.7 tokenizer 1.0-1.35x 膨胀" | Simon Willison 实测 + Anthropic 官方迁移指南 | 实测 1.46x token 膨胀(Opus 4.7 self-count);1.0-1.35x 范围;表面同价实际成本高 5-40% | autodev_pipe v3.1 已对齐(§0.2 错 5)— 路由表按等效成本;Phase 4 idea_gamma2 retrospective A27 也已识别 codex cap 接近耗尽 | 与 SOTA 一致;但**两套都未自动化** — 需人工查路由表;Cloudflare 的 hot-swap 是真正自动化路径 | [Simon Willison 2026-04-20](https://simonwillison.net/2026/apr/20/claude-token-counts/) |
| 三套对"unattended autonomous agentic coding"的态度 | 真实失败案例 | earezki $437 overnight(2026-04-29);Magicrails 14k `list_files` 工具调用 loop;163-article $0 revenue;"$8k-15k per session w/ 49 sub-agents";"$47k per 3 days w/ 23 sub-agents";**核心缺口:in-process brakes 监控状态停滞 + token 消耗,而非 post-hoc dashboard** | autodev_pipe v3.1 已识别此问题(§0.4 第 4 条 "失败案例的成本上限");`scripts/kill_switch.py` + `.github/workflows/budget.yml` 每 15 分钟跑;但**仍是 post-hoc**,不是 in-process | gap 大 — 三套都**没有 in-process brakes**(检测 tool-call loop / state stasis);kill_switch 在 15min 粒度,失控 14k tool calls 早已烧完 | [earezki.com $437 overnight](https://earezki.com/ai-news/2026-04-29-i-let-my-ai-agent-run-overnight-it-cost-437/) · [Anthropic measuring-agent-autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) |
| L1-L4 idea→PRD pipeline | Anthropic 2026 Agentic Coding Trends Report | "harness > model upgrade" — agent harness 已是 product 本身;harness 工程化(prompts / tools / context / verification)= 5 个核心工作流 | 当前 ideababy_stroller 的 L1-L4 + forge 横切 = idea-incubator harness;autodev_pipe v3.1 §0.4 第 1 条认证"Idea→PRD 阶段是 v2 完全没说的缺口" | 与 SOTA 方向一致 — L1-L4 填了"未 PRD 化的早期 idea"段缺口,**这是 ideababy_stroller 的真实差异化**;但**对外文档薄**(根 README.md 简短) | [resources.anthropic.com/2026 Agentic Coding Trends](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf) · [mindstudio.ai/agent-harnesses-beat-model-upgrades](https://www.mindstudio.ai/blog/agent-harnesses-beat-model-upgrades-5-benchmarks) |
| SWE-bench Verified 用作 reliability 度量 | OpenAI Preparedness Framework + SWE-Bench Pro | Claude Mythos 93.9% / GPT-5.3 Codex 85% / Opus 4.5 80.9% on Verified;**SWE-Bench Pro = long-horizon 真实任务,顶级 23%**(vs Verified 70%+);差距巨大说明"短任务高分 ≠ 长任务可用" | 三套 X 都**未引入** SWE-bench / Pro 作为 framework 自检指标;只有 idea_gamma2 用 acceptance test + 真跑 CI 作为内部 reliability;ideababy_stroller forge 也没有 | gap 巨大 — Y4 "可靠性度量"在三套都缺失;K 中"可靠"诉求**未配可量化指标** | [arxiv.org/abs/2509.16941 SWE-Bench Pro](https://arxiv.org/abs/2509.16941) · [openai.com/index/swe-bench-verified](https://openai.com/index/introducing-swe-bench-verified/) |

paraphrase findings;verbatim quote ≤15 words("AGENTS.md outperforms skills"、"Skills max at 79%"、"context as a finite resource with attention budget"均原文短引)。

---

## 2. 用户外部材料消化

K 中提到的外部材料:`technology_roadmap.md`、`pipeline SKILL.md`、`phase-retrospective skill`、`solo_ai_pipeline_v3.1.md`、4 个 repo 全部 `.claude/`。**已在 P1 §0.2 全部读过** — 本节不重复。

K 没有列额外外部链接(无 URL / pdf 下载链接),所以无新材料消化任务。

但 K 隐含一个外部锚点:**addy osmani agent-skills**(autodev_pipe v3.1 §1.2 主推 + idea_gamma2 CLAUDE.md "addy osmani 模式"暗合)— SOTA 检索结果证实 addy osmani agent-skills 是真实存在的体系,但**Vercel 的实测说 Skills 顶 79%**(Vercel 用的是 Anthropic Skills,addy osmani 是同一体系延展)。**这条消化结果是关键修正**:autodev_pipe v3.1 路线 A 推 agent-skills 作为骨架 + 5 个手动 cp 是**对齐 Vercel 数据**的(因为 v3.1 已把 AGENTS.md 立为根上下文,Skills 只是辅助)。

---

## 3. 修正后的视角(P1 哪些站住、哪些被推翻)

### 3.1 站住的判断

- **P1 Y1 "autodev_pipe v3.1 最贴 §006 诉求"** → **站住**。SOTA 检索确认 v3.1 §错 1-6 的所有自批都对齐外部数据(Vercel AGENTS.md / 上下文阈值 / Opus 4.7 tokenizer / Cloudflare 协调者 + 子审 / 失败案例成本上限)。v3.1 设计稿在 framework 层级**已是 SOTA 对齐设计**。
- **P1 Y2 "三套抽象不重合,但 agent + skill + slash + rules + AGENTS.md/CLAUDE.md 是基本盘"** → **站住**。Cloudflare、Vercel、Anthropic Trends Report 都印证此基本盘。
- **P1 Y3 "idea_gamma2 retrospective + 候选教训沉淀机制是 SOTA 候选"** → **部分站住**。Cloudflare coordinator hot-swap 也是"机制学到 → 写入配置"的同源思路;但 idea_gamma2 是文档层(SKILL.md retrospective),Cloudflare 是配置层(opencode.json hot-swap),后者**更接近 in-process 而前者更接近 post-hoc**。

### 3.2 被推翻或显著修正的判断

- **P1 Y4 "refactor + 留 P2 SOTA 验证"(暂判)** → **修正为 new + refactor 双层**。SOTA 检索结果显示三套 X **全部缺少**:(a) 可量化 reliability 度量(SWE-bench Pro long-horizon 23% vs Verified 70%+ 差距巨大,说明短任务通过 ≠ 框架可靠);(b) in-process brakes(state stasis / tool-call loop 检测,而非 15min 粒度 kill_switch);(c) coordinator-driven hot-swap(model 失败自动切)。这三件**都是 new infrastructure**,不能通过 refactor 现有获得。GPT P1 §2 Y4 标 `new` 比 Opus P1 标 `refactor` 更准确。**Opus 让步**。
- **P1 §3-1 "autodev_pipe 三条路线 SOTA 对标度不确定"** → **得到验证 — 路线 A 对齐 SOTA**。Vercel "AGENTS.md > Skills 8KB 100%"数据 + Skills "activation problem 56%" 数据,**支持** autodev_pipe v3.1 路线 A(agent-skills 骨架 + 5 个手动 cp)的设计选择。但 framework 共识方案应明确指出:**Skills 不是被否定**,只是当前形态下 activation 不可靠;搭配 AGENTS.md 作为 passive context 才能发挥。
- **P1 §3-3 "L1-L4 严肃 vs 易用 权衡"** → **新证据偏向保留 + 加强**。Anthropic 2026 Trends Report "harness > model upgrade" + autodev_pipe v3.1 §0.4 第 1 条"Idea→PRD 阶段是 v2 完全没说的缺口" → L1-L4 是 ideababy_stroller 的真实差异化,且填了行业普遍空缺。**不应压缩**,但**应在 framework README 里把 L1-L4 价值显式化**(目前根 README.md 简短)。

### 3.3 P2 引出的新 unknowns(留给 P3)

- **in-process brakes 应放在 framework 哪一层?** SKILL?agent?hook?这关系到三套 X 哪个能 host 此 mechanism。idea_gamma2 是 Codex `/codex:review --wait` cap-aware,但仍是粗粒度;Cloudflare 是 coordinator hot-swap config。framework 共识需要选 1。
- **SWE-bench Pro 类长任务度量是否应嵌入 framework 自检?** 还是只在 retrospective 层做 self-eval?framework 内置 benchmark hook 是否过重?

(P2 字数:正文 ~1080 字,扣表格、引用块、heading)
