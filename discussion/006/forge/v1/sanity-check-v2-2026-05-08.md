---
doc_type: sanity-check-v2-with-adp-versions
generated: 2026-05-08
upstream: sanity-check-2026-05-08.md(v1) + autodev_pipe v3.2/v3.3/v4 spec + ADR 0008/0009 + next_draft §3 三方共同盲区
purpose: 把 autodev_pipe v3.2/v3.3/v4 真实状态纳入,重审 forge 006 v1 verdict + 5 件事产物的过时程度
verdict: 核心 verdict 仍对(分仓 / L/P/C / 8KB AGENTS / Safety Floor / SHARED-CONTRACT);但 stage v1 §3 模块 4 / §5 dev plan 需大幅修订(autodev_pipe 已经做了大部分 v4 范围)
---

# Sanity Check v2 · 2026-05-08(纳入 autodev_pipe v3.2/v3.3/v4)

## 总评

**5 件事核心 verdict 仍对**(独立于 autodev_pipe 哪个版本的事实)。**但 stage v1 §3 模块 4 / §4 PRD draft / §5 dev plan 大幅过时**(autodev_pipe 已经做了 v3.2/v3.3 + v4 frozen 代码层)。

需要做的:**不回滚 commit**;在 next-steps.md / sanity-check-2026-05-08.md 旁加一份本文件作 v2 增补;视情决定是否起 forge v2 重审 stage §3-§5。

---

## 关键发现:autodev_pipe 真实演进 vs 我们 forge 跑用的版本

forge 006 v1 跑的 X 标的:**autodev_pipe v3.1 设计稿 + STARTER_KIT.md**。

实际状态(2026-05-08 核查):

| 版本 | 日期 | 状态 | 主旨 | 我们 forge 是否纳入? |
|---|---|---|---|---|
| v3.1 | 2025-Q4? | 设计稿(gap-audit 11 项 ×) | 11 阶段流水线设计 | ✅ 是 X 主标的 |
| v3.1-gap-audit | (W0.1 输出) | 11 × / 5 △ / 13 √ 真实落地盘点 | 揭示 v3.1 是设计稿不是 running system | ❌ 没读过 |
| v3.2 | 2026-04-29 | frozen | port stroller 五件套(sdd-workflow / task-decomposer / quality-gate-runner / parallel-builder / check-disjoint) | ❌ 没读过 |
| v3.3 | 2026-04-29 frozen / 2026-05-06 真审 | frozen | 三方共同盲区(spec-validator / 跨 LLM review / Constraint Index / 7 元素 / reviewed-by hook) | ❌ 没读过 |
| v4 | 2026-05-06 frozen(代码层)/ 12 周 dogfood 进行中 | frozen 代码层 | retrospective(L1+L2)+ lesson 反哺 + append_lesson script | ❌ 没读过 |
| ADR 0008 → 0009 | 2026-05-06 | active | B 真外部 → C Hybrid 路径修正 | ❌ 没读过 |
| next_draft §3 三方盲区 | 2026-05 | reference | spec 7 元素 / Constraint Index / lesson 反哺 / worker-monitor 4 个核心改进 | ❌ 没读过 |

**结论**:forge X 标的截止 v3.1,**漏看了 6 个月内 v3.2 → v3.3 → v4 的 3 次重大演进**。这是 stage v1 部分 verdict 严重偏老的根本原因。

---

## 5 件事产物 vs autodev_pipe v3.2-v4 真实状态对照

逐件审计(L=Lesson 仍对 / P=Pattern 部分对 / D=Drift 已过时 / X=与现状冲突):

### 事 1 · NON-GOALS.md(7 条)

| NG | 立场 | vs autodev_pipe v3.2-v4 | 判定 |
|---|---|---|---|
| NG-1 不内化历史 repo 代码 | 客观工程范式 | autodev_pipe v3.2 PD1 实际**已做相反的事** — port stroller 五件套(C 级 cp,通过测试验证)。但 NG-1 立场是从 IDS 视角,不内化 ADP 代码,这与 ADP 内化 stroller 不冲突 | **L · 仍对**(立场对应 IDS 内,不矛盾 ADP 自己怎么做) |
| NG-2 IDS 不做 build/review/brakes | autodev_pipe v3.2/v3.3 已实现 5 hard rule + parallel-builder + check-disjoint;v3.3 实现 reviewed-by hook + spec-validator | **L · 强烈仍对** — 现实证明 ADP 已做完这些;IDS 抢工作就是重复发明 |
| NG-3 不再发明 SKILL/AGENT 体系 | LF AAIF + Anthropic Skills SDK | autodev_pipe v3.2 PD1 已遵守(走 stroller schema,非自创) | **L · 仍对** |
| NG-4 不承诺 full-auto 跨 Safety Floor | Cursor 删库 + Codex CLI 范式 | autodev_pipe AGENTS.md L48 "危险命令唯一防线 = block-dangerous.sh";v3.2 parallel-builder 5 hard rule 已实装 | **L · 强烈仍对** — ADP 已落地,IDS 这条是上游一致性约束 |
| NG-5 不复制 Cloudflare 全量 7 reviewer | MVP 80/20 + SWE-PRBench | autodev_pipe v3.3 reviewed-by hook 是单 reviewer + plugin 路径,符合 NG-5 立场 | **L · 仍对** |
| NG-6 不把 SWE-bench Pro 当 CI gate | regression-vs-absolute | autodev_pipe v3.2 V_global 用 G1-G10 + audit-consistency 而非 benchmark 阻塞 | **L · 仍对** |
| NG-7 两仓不版本绑定 | Newman + Pact + semver | **关键发现**:autodev_pipe v3.2/v3.3/v4 内**没有任何机制锁定 IDS 版本**;它的 self-parasitic 是"用 v3.x 自身的能力"而非"对接 IDS";这与 NG-7 完全一致 | **L · 仍对** |

**事 1 总评**:**7/7 NG 全部仍对**,且**实际状态比 NG-1/NG-2 论证的"应该"更强**(autodev_pipe 已经在做相应工作,IDS 抢工作的诱惑被 ADP 的真实存在自然消除)。

### 事 2 · SHARED-CONTRACT.md(5 节)

| 节 | 立场 | vs autodev_pipe v3.2-v4 | 判定 |
|---|---|---|---|
| §1 PRD schema | 8 字段 plain markdown | autodev_pipe v3.2/v3.3/v4 用 spec.template.md(7 元素 schema,**不同于** PRD 8 字段) | **D · drift** — autodev_pipe spec **不是** PRD,它是 spec 自身;PRD 在 IDS 这边产出,然后**变成** autodev_pipe spec 的输入。两边 schema 不同是合理的(PRD vs Spec 是 SDLC 不同阶段),但 SHARED-CONTRACT §1 没说清这层映射 |
| §2 Safety Floor 三件套 | production credential / 不可逆命令 / 备份破坏 | autodev_pipe AGENTS.md L48 "block-dangerous.sh" 是单一防线;v3.2 parallel-builder 5 hard rule 是另一层;**实装比 §2 描述的更分散** | **P · 部分对** — 三件套精神对,但具体实装不在单一 binding 文件;需要 SHARED-CONTRACT 说清 ADP 已用 hook + agent rule + spec validator 多层实现 |
| §3 Hand-off 协议(HANDOFF.md) | `/plan-start` 产出 HANDOFF.md | autodev_pipe **没有** ingestion 端的 cli。它的入口是 `make sdd-init <feature>`(v3.2 V1)或 `make decompose <spec>`(V2),消费的是 **autodev_pipe 自己的 spec.md**,不是 IDS 的 PRD | **X · 与现状冲突** — `autodev_pipe-cli build` 命令**不存在**;实际入口是 stroller-port 的 `make sdd-init` / `make decompose`。HANDOFF.md 必须重写为 "PRD 转 ADP spec" 的协议而非 "PRD 直送 cli build" |
| §4 版本演化机制 | semver + 三阶段 deprecation | autodev_pipe 实际用 schema_version: 0.1 → 0.2(v3.2 → v3.3 升级时 spec.template.md 加第 7 元素);PD10"v3.2 已 ship spec 不强制回填" 是 backward-compat 范式 | **L · 强烈仍对** — autodev_pipe 实际正在用类似机制,本节立场被 ADP 的真实实践印证 |
| §5 interface-contract 五元组 | producer/consumer/schema/version/error-handling | autodev_pipe 的 sdd-workflow / task-decomposer / quality-gate-runner 之间**已隐式遵守类似五元组**(spec_ref + phase + depends_on + blocks + parallelizable_with) | **L+P · 仍对**(范式)+ ADP 已实践 |

**事 2 总评**:**§1 / §2 / §3 需修订**(当前描述假设 autodev_pipe 是 v3.1 设计稿,实际是 v3.2-v4 已 frozen 系统);§4 / §5 立场仍对。

### 事 3 · AGENTS.md 升级(7 节,7252 字节)

| 节 | 立场 | vs autodev_pipe AGENTS.md(94 行) | 判定 |
|---|---|---|---|
| §1 Safety Floor | hard block 三件套 | ADP AGENTS.md L48 单条"block-dangerous.sh 唯一防线" — 范围比 §1 小但思想一致 | **L · 仍对** |
| §2 可靠三层 | Safety Floor / Deterministic Feedback / Learning Loop | ADP 实际:hook(Safety) + G1-G10 + spec-validator(Deterministic) + retrospective + append_lesson(Learning) — **三层 ADP 都已实装**,本节描述对 | **L · 仍对**,且 ADP 已落地 |
| §3 轻入口 vs 重升级触发器 | 小/中/大三档 | ADP 范围全是中/大型(它就是 build harness),没有"轻入口"子集。本节立场对 IDS 的判断仍对(IDS 内的轻/重) | **L · 仍对**(IDS 范围内) |
| §4 跨仓引用契约 | 独立 release 无版本绑定 | ADP 当前**无 IDS 引用**(它 self-parasitic),所以"无绑定"是默认状态。本节立场对 | **L · 仍对** |
| §5 Pipeline & forge 入口 | L1-L4 + forge 横切 | IDS 自己的命令链,与 ADP 无关 | **L · 仍对** |
| §6 Iron rules + defaults | 11 条 + 工具 + 目录 | IDS 自己的规则 | **L · 仍对** |
| §7 References & scope | 5 文件链接 | IDS 自己的引用 | **L · 仍对** |

**事 3 总评**:**7/7 节全部仍对**,且 ADP 已经实装了 §2 描述的"可靠三层"。AGENTS.md 8KB 限制 + 6 节 framework SSOT 立场被 ADP 的实际 AGENTS.md(94 行,L1-L93)印证可行。

### 事 4 · AUTODEV-PIPE-SYNC-PROPOSAL.md(3 节)

| 节 | 立场 | vs autodev_pipe 真实状态 | 判定 |
|---|---|---|---|
| 节 1 README "Repo role" | "consume PRD, honor Safety Floor" | autodev_pipe 实际 README 1201 行,主体是 v3.1 starter kit 文档;**没有 ingest PRD 的部分**(因为它消费 spec 不是 PRD);"honor Safety Floor"立场对 | **D · 部分 drift** — README 实际不会变成"PRD consumer";应改为"承认 IDS 是上游 PRD 来源,但 ADP 的 sdd-workflow 把 PRD 转成自己的 spec" |
| 节 2 ADP AGENTS.md 创建 binding | "must reference IDS framework/SHARED-CONTRACT.md §2 Safety Floor" | ADP AGENTS.md L48 已有"危险命令唯一防线",但**没引用 IDS**;ADP 是先于 IDS framework 文档存在的 | **D · drift** — 不能要求 ADP "binding from IDS",因为 ADP 早于 IDS framework 文档;实际 SSOT 在 ADP 自己,IDS framework SHARED-CONTRACT §2 应改为"参考 ADP 实践" |
| 节 3 SHARED-CONTRACT.md mirror | byte-level cp + sync 检查脚本 | ADP 没有 SHARED-CONTRACT.md 的需求(它独立运作);强行加 mirror = 给 ADP 加无意义维护负担 | **X · 与现状冲突** — 不应要求 ADP 加 mirror;SHARED-CONTRACT 应在 IDS 这边作为"推荐实践参考",而非"binding contract" |

**事 4 总评**:**3/3 节都需要重新设计**。**根本错误是方向**:本来想"IDS 拥有 SSOT,ADP 跟随",但实际上 **ADP 的工程实践早于 IDS framework 文档,且 ADP 自洽运作不需要 IDS binding**。正确方向应该是:**IDS framework 文档参考 ADP 实践 + ADP 不需要做任何同步**。

### 事 5 · stage v1 §2 Decision matrix L/P/C 重写(28 项)

| 项 | 重写后立场 | vs autodev_pipe v3.2-v4 | 判定 |
|---|---|---|---|
| #4 v3.1 STARTER_KIT 🟢 项 | C 级 / 留 ADP 不 cp 到 IDS | **过时** — autodev_pipe **v3.2 已 port stroller 五件套**,STARTER_KIT.md 仍存但已被部分覆盖;cp 到 IDS 仍不必要,但理由不再是"v3.1 已物化",而是"v3.2 已升级" | **D · drift**(立场不变,理由过时) |
| #5 idea_gamma2 phase-retrospective 五维 + §2.6 | P / ADP 借鉴自己实现 | **autodev_pipe v4 已 frozen 代码层**:retrospective skill + L1/L2 触发 + append_lesson — **它已经做完"借鉴自己实现"** | **D · drift**(立场对,但已是历史 — ADP v4 已实现) |
| #15 Safety Floor 三件套 | L+P / IDS SSOT + ADP 实现 | autodev_pipe **没有** SSOT 在 IDS 的 binding;它自己的 block-dangerous.sh + parallel-builder 5 hard rule + spec-validator 已是多层实现 | **D · drift**(SSOT 归属错;实际 ADP 自洽) |
| #16 in-process brakes | P / ADP 工业失败教训驱动 | next_draft §3.3 改进 4 "worker-monitor 半推论未实证",**v4 spec 显式推 V4.2**(C8 不修;ADR 0009 D3 推 V4.2);现状没实装 | **L · 仍对**(实装位置正确,但时间维度过时) |
| #18 Eval Score 层(SWE-bench Pro micro-eval) | P / ADP | **autodev_pipe 没有 SWE-bench Pro 计划**;它用 G1-G10 + audit-consistency + reviewed-by 三层质量门;Eval Score micro-benchmark 是 forge 自己加的 SOTA 论据,ADP 没纳入 | **D · 弱 drift**(立场没问题,但 ADP 未来未必采纳) |
| #19 项目规模升级触发器 | L / IDS AGENTS.md | autodev_pipe 范围全在中/大型,本身没"小型"概念。本立场对 IDS 仍对 | **L · 仍对** |
| #20-#28 + L20-L23 / P24-P27 / C28 补充项 | 各种 L/P/C | 补充项主要来自 idea_gamma2 / vibe-workflow,与 ADP 无关 | **L · 仍对** |

**事 5 总评**:**核心立场仍对(L/P/C 分层方法论 + 28 项分类),但具体项的"理由"和"时间维度"过时**。需在 §2 表格旁加一段说明:"本表 cutoff 2026-05-07;autodev_pipe v3.2/v3.3/v4 frozen 状态使 #4/#5/#15/#16/#18 的具体描述需重写,但 L/P/C 分类不变"。

---

## stage v1 §3 模块 1-5 vs autodev_pipe 真实状态

stage v1 §3 列了 5 个 framework 模块。逐一对照:

| 模块 | stage v1 §3 立场 | autodev_pipe 真实状态 | 判定 |
|---|---|---|---|
| 模块 1 · Context/Instruction(AGENTS.md SSOT + Skills 过程化) | "改造步骤 1-3" | autodev_pipe AGENTS.md 已是 SSOT(94 行 L18-93,实际 5KB 不到);Skills 过程化在 v3.2/v3.3/v4 已落地 | **D · 已过时** — autodev_pipe 已做完此模块;IDS 这边事 3 升级 AGENTS.md 是 IDS 内部,与 ADP 模块 1 无关 |
| 模块 2 · Safety/Permission(Safety Floor 三件套 + sandbox modes) | "改造步骤 1-4 / S 估时" | autodev_pipe **block-dangerous.sh** + **parallel-builder 5 hard rule** + **request-approval.sh** 已实装;sandbox modes 没有显式三档,但有 5 hard rule 等价 | **D · 已 80% 完成** — 不是"S 估时改造",而是"已落地,审计是否充分"。剩下 20%(production credential 物理隔离 + 备份破坏检测)是真 gap |
| 模块 3 · Quality/Review(coordinator MVP 4 件套) | "L MVP / XL 完整" | autodev_pipe v3.3 reviewed-by hook + plugin 路径 = 单 specialist + 单 coordinator + timeout(plugin 级);**risk tier 没显式**;**human escape hatch** = pre-commit reject + manual review;实际比 4 件套**少 1**(risk tier) | **D · 已 75% 完成** — risk tier 是真 gap;其他 3 件已落地 |
| 模块 4 · Learning Loop(retrospective + Eval Score) | "改造步骤 1-3 / M 估时" | **autodev_pipe v4 已 frozen 代码层**:retrospective L1+L2 + append_lesson + ~/.claude/lessons + 4 个 category(core/project-type/anti-pattern/tool);**自寄生跑过 v3.3 W2.7 retrospective**;**Eval Score 没有 SWE-bench Pro 计划** | **D · 90% 完成** — autodev_pipe v4 已做完 retrospective + lesson 反哺;Eval Score(micro-benchmark)是真 gap |
| 模块 5 · Idea Incubation(L1-L4 + forge,high-risk path 默认) | "改造步骤 1-3 / S 估时" | IDS 自己范畴,与 ADP 无关 | **L · 仍对** |

**stage v1 §3 总评**:**模块 1-4 在 autodev_pipe 那边已经 60-90% 完成**;stage v1 §3 当成"待启动改造"是错的,实际是"审计已落地状态 + 补真正的 gap"。

**真正的 gap**(已对照 autodev_pipe v3.2-v4 真实状态):

1. **Safety Floor 三件套**:autodev_pipe **缺** production credential 物理隔离机制 + 备份破坏检测(只有 block-dangerous 单层)— 这是 stage v1 §3 模块 2 的剩余 20%
2. **Risk tier 分类器**:autodev_pipe **没有** file_domain/spec section/危险命令 → tier 1/2/3 的显式分类器(reviewed-by hook 是单一 tier)— stage v1 §3 模块 3 的剩余 25%
3. **Eval Score micro-benchmark**:autodev_pipe **没有** SWE-bench Pro 任务集 + recall/precision 量化机制 — stage v1 §3 模块 4 的剩余 10%

**这 3 个真 gap 是 framework 落地的真实工作量**,不是 stage v1 描述的"5 个模块从零启动"。

---

## stage v1 §4 PRD draft + §5 dev plan 过时程度

### §4 PRD draft

stage v1 §4 PRD 写"使用 v3.1 STARTER_KIT 🟢 项物化"。但 autodev_pipe v3.2/v3.3/v4 已经升级。PRD 应改为:

| stage v1 §4 原描述 | 应改为 |
|---|---|
| "v3.1 STARTER_KIT 🟢 RUNTIME-COMPLETE 物化项 framework 化采纳" | "**审计** autodev_pipe v3.2/v3.3/v4 已实装项,**补 3 个 gap**(prod cred 隔离 / risk tier / Eval Score),不重复造轮子" |
| "Phase 1 直接 cp v3.1 STARTER_KIT 🟢 项" | "Phase 1 ADP 已 frozen v4 代码层 + 12 周 dogfood 进行中,仅补真 gap" |
| "节奏 A 2 周 MVP" | "节奏依赖 ADP v4 dogfood 12 周窗口外推" |

### §5 dev plan

stage v1 §5 5 个 phase 的工作量假设全部需要 IDS 这边做。**实际**:

- **Phase 1 Skeleton + Safety Floor**(预估 1 周) → 80% 已在 ADP 完成
- **Phase 2 Review Coordinator MVP**(4-5 天) → 75% 已在 ADP 完成
- **Phase 3 Learning Loop**(3-4 天) → 90% 已在 ADP 完成(v4 frozen 代码层)
- **Phase 4 L1-L4 重升级路径打磨**(2-3 天) → IDS 自己范畴,仍需做
- **Phase 5 v1.0 polish + Eval pass**(1 周) → 整体节奏依赖 ADP 12 周 dogfood

**真正需要做的 dev plan**:

1. **gap 1 实装**:autodev_pipe 加 production credential 物理隔离 + 备份破坏检测 — 估时 1-2 周
2. **gap 2 实装**:autodev_pipe 加 risk tier 分类器 — 估时 4-5 天
3. **gap 3 实装**:autodev_pipe 加 SWE-bench Pro micro-benchmark — 估时 1 周(任务集选取 + recall/precision 量化)
4. **IDS 自身 Phase 4**:L1-L4 重升级路径文档 + 升级触发器规则 — 估时 2-3 天
5. **整合 dogfood**:跨仓 hand-off 实现(不是 SHARED-CONTRACT §3 假设的 cli,而是 IDS PRD → ADP spec 的转换流程) — 估时 1 周

**总计**:**~4-5 周**,小于 stage v1 节奏 A 2 周(因为 stage v1 假设 IDS 从零做),也小于节奏 B 6 周(因为大部分已在 ADP 完成)。

---

## 5 个真发现(ADP 已做完 stage v1 §3 模块 1-4 大部分时,**新出现**的事实)

next_draft §3 三方共同盲区揭示了 forge 没纳入的真 SOTA:

### 发现 1 · spec 7 元素的"Production Path Verification"

stroller / gamma2 / autodev_pipe v3.1 三方都缺。autodev_pipe v3.3 已加(第 7 元素 + spec.template.md §7)。

**对 forge stage v1 的影响**:stage v1 SHARED-CONTRACT §1 PRD schema 8 字段没包含"Production Path Verification"。**应补**为第 9 字段。

### 发现 2 · Constraint Index 跨多 agent 引用范式

gamma2 W18 4 文件 cp 漂移是失败案例。autodev_pipe v3.3 `docs/constraints/<id>.md` + check_constraint_references.py 是解药。

**对 forge stage v1 的影响**:stage v1 SHARED-CONTRACT 没提"约束跨多 agent 引用"问题。**应补** "Constraints management" 节(参考 ADP v3.3 实践)。

### 发现 3 · cross-LLM review 已在 ADP 实装(v3.3 reviewed-by hook + plugin 路径)

autodev_pipe v3.3 已落地"reviewed-by frontmatter + pre-commit reject"机制;v3.3 spec 自身首次跑 codex review(2026-05-06)抓 3 个 finding 全闭。

**对 forge stage v1 的影响**:stage v1 §"P3R2-Opus47Max" / "P3R2-GPT55xHigh" 双专家审就是这个机制的实例,但没显式描述为 framework 机制。**应**在 IDS framework 文档里把 forge 横切层与 ADP reviewed-by hook 明确为同一范式的两个尺度。

### 发现 4 · ADP v4 retrospective 已自寄生过 v3.3 W2.7

autodev_pipe v4 spec phase 4 T008 用 v4 retrospective skill 处理 v3.3 W2.7 报告。这是 stage v1 §3 模块 4 描述"未来要做"的事 — **ADP 已经做完**。

**对 forge stage v1 的影响**:stage v1 §3 模块 4 描述需大幅重写为"ADP 已做完 L1+L2;IDS 应用 lesson 在 idea→PRD 阶段"。

### 发现 5 · ADR 0008 → 0009 路径修正:V4 dogfood 从"B 真外部 ≥ 2"降为"C Hybrid 1 真自用 + 1 ADP 自身"

这意味着 ADP 自己**已经在做**"决策账本 v0.1" + "ADP 自身 retrospective 周期"这两个 dogfood,**不依赖 IDS PRD 输入**。

**对 forge stage v1 的影响**:**SHARED-CONTRACT §3 hand-off 协议预设"IDS PRD → ADP build"是错的**;**ADP 当前 dogfood 路径就是它自己产 spec 跑,IDS 不在数据流中**。如果 IDS 想成为 ADP 的 PRD 上游,需要 ADP **主动**修改入口接受 PRD,但 v4 spec 没这个条款;这意味着**两仓集成需要双方都加工作**,不只 IDS 加 SHARED-CONTRACT。

---

## 推荐路径修订

### 原 plan 的 A/B/C 推荐(基于 v1 sanity check)

- A · 启动 stage §5 Phase 1 build(autodev_pipe)
- B · 起 forge v2
- C · framework v0.1 = 文档而已

### v2 sanity check 修订后的推荐

走 **C(原推荐)的弱化版** + **加 follow-up 起 forge v2 的明确触发条件**:

#### 推荐:走 C(framework v0.1 = 文档而已)

**理由(更强了)**:
- ADP 已经做完 stage v1 §3 模块 1-4 的 60-90%,**IDS 这边再做更多 framework 文档边际收益更低**
- 真 gap(prod cred / risk tier / Eval Score)**应该在 ADP 那边做**,不在 IDS
- 5 件事产物核心立场仍对,**不需要回滚**
- 但"事 4 SYNC-PROPOSAL"应该重新设计 — 方向是"IDS framework 文档参考 ADP 实践",**不是**"ADP 做 binding"
- "事 2 SHARED-CONTRACT §1/§2/§3"需要重写以匹配 ADP 真实接口

#### 新增 follow-up:**起 forge v2 的明确触发条件**

**何时起 v2**:

1. 用真实 idea 走完 1 个 IDS L1→L4 → PRD 流程,然后**实际去 ADP 那边消费 PRD**;此时暴露的接口缺陷(SHARED-CONTRACT §3 假设的 cli 不存在)是 v2 forge 的 X 输入
2. 或:autodev_pipe v4 12 周 dogfood 完成 + ship checkpoint 03 后,新事实可作为 forge v2 X 输入
3. 或:出现新 SOTA(如 Anthropic Claude Skills SDK 升级到 v2)需重审 NG-3

**何时不起 v2**:

- 仅"想再问一遍"
- 没有新 X 输入
- 现有 framework 文档 7-8 成够用

#### 紧急 follow-up:5 件事产物的局部修订(不起 v2)

不起 forge v2 的前提下,**直接编辑** 5 件事产物的局部:

- **事 2 SHARED-CONTRACT.md §1**:加"PRD vs Spec 区分" + ADP 实际入口("`make sdd-init` 而非 `autodev_pipe-cli build`")
- **事 2 §2 Safety Floor**:改为"参考 ADP block-dangerous.sh + 5 hard rule 实践,IDS 这边只声明上游一致性约束"
- **事 2 §3 Hand-off 协议**:重写为"PRD → ADP spec 转换流程",ADP 仍读自己 spec.md,不读 PRD
- **事 4 SYNC-PROPOSAL**:重新设计为"IDS framework 文档参考 ADP 实践的方向参考",而非 binding contract
- **事 5 stage v1 §2**:加 v2 增补段说明"#4/#5/#15/#16/#18 描述时间维度过时,但 L/P/C 分类不变"
- **next-steps.md**:加"v2 sanity check 后的修订记录"

### 不推荐的路径

- **A · 立即启动 build**(在 ADP)— ADP 已 frozen v4 代码层 + 12 周 dogfood 进行中,**插入新 build 工作会污染 ADP 自身 dogfood signal**
- **B · 立即起 forge v2** — 当前没有新 X 输入(v3.2/v3.3/v4 + ADR 0008/0009 + next_draft §3)足够支撑 v2,但**真正缺的是 IDS PRD→ADP spec 接口实测**;先做实测再起 v2 更有效

---

## 总结(三句话)

1. **forge 006 v1 5 件事产物核心立场全部仍对**(分仓 / L/P/C / 8KB AGENTS / Safety Floor / SHARED-CONTRACT 范式),不需要回滚
2. **stage v1 §3 模块 1-4 + §4 PRD + §5 dev plan 大幅过时**(autodev_pipe v3.2/v3.3/v4 已做 60-90%);需局部修订 5 件事产物文档而非起 forge v2
3. **真 gap 是 3 个**(autodev_pipe 这边的 prod cred 隔离 / risk tier 分类器 / Eval Score micro-benchmark),不在 IDS 这边

---

## 决策菜单(给 operator)

### [选项 1] 接受本 v2 sanity check + 局部修订 5 件事产物
- 编辑 SHARED-CONTRACT §1/§2/§3 / SYNC-PROPOSAL 全文 / stage v1 §2 增补段 / next-steps.md
- 不起 forge v2,不动 commit history
- 工作量:~2-3 小时
- 风险:低

### [选项 2] 接受本 v2 sanity check + 不修订(留 v2 文件作 audit)
- 5 件事产物保持不变(它们核心立场对,只是部分细节过时)
- 本文件作为已知 gap 的 audit trail
- 工作量:0
- 风险:留过时细节在 framework 文档,未来 onboarding 可能踩坑

### [选项 3] 起 forge v2(把 v3.2/v3.3/v4 + ADR + next_draft 加 X)
- 跑双专家 + Codex 4 phase
- 产出 stage-forge-006-v2.md
- 工作量:~30min(我跑) + ~30min Codex 跑
- 风险:核心 verdict 大概率不变,可能"白烧 token";但能产生权威 audit + v2 stage doc

### [选项 4] 推迟决定
- 先用 framework v0.1 实际跑 1 个新 idea 走 L1→L4 → PRD,然后**实际尝试** ADP 消费这个 PRD
- 暴露的真接口问题 → 后续再起 v2 或修订
- 工作量:不可预估(取决于走 1 个完整 idea 的时间)
- 风险:延迟,但暴露的问题最真实

---

## 我的推荐

**选项 1**:接受 v2 sanity check + 局部修订 5 件事产物。理由:

- 修订工作量小(~2-3h)
- 不留过时细节在 framework 文档(避免未来踩坑)
- 不起 forge v2(避免白烧 token)
- 不依赖未来真实跑(避免延迟)
- 选项 4 可在选项 1 完成后并行(实际跑 idea 暴露的进一步问题,可加 v3 修订)

下一步:你确认走选项 1,我开始局部修订 5 件事产物,产出 commit "fix(framework): v2 sanity check 后修订 SHARED-CONTRACT / SYNC-PROPOSAL / stage v1 §2 局部"。

如果你倾向其他选项,告诉我。
