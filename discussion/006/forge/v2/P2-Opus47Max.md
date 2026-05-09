# Forge v2 · 006 · P2 · Opus 4.7 Max · 参照系评估(with search)

**Timestamp**: 2026-05-09T12:48:00Z
**Searches used**: 4(Anthropic Skills SDK / Cursor Composer multi-repo / GitHub Spec Kit v2 / agentic coding failure cases 2026)
**Visibility**: 已读对方 P1-GPT55xHigh.md(P3 收敛起点)
**Reviewer stance**: 审阅人 — 用 SOTA 校准 P1 first-take。

## §1. SOTA 对标

| 范畴 | SOTA 方向(2026 现状) | 与 ADP-next/IDS 对照 | 我的判定 |
|---|---|---|---|
| **Spec-driven development** | GitHub **Spec Kit** v2 已成主流(90k stars,30+ AI agent 兼容,Specify→Plan→Tasks 4 phase),Anthropic 4 月公布 Planner/Generator/Evaluator agent 三角架构(structured artifact 而非 shared context)([github/spec-kit](https://github.com/github/spec-kit) / [Anthropic Engineering 2026-04](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)) | ADP V4 sdd-workflow 7 元素 + reviewed-by 4 轮 = 与 Spec Kit "Specify→Plan→Tasks" 同构;但 IDS PRD 8 字段(SHARED-CONTRACT §1)与 Spec Kit `spec.md` schema 不一致 | **建议 ADP-next/XenoDev 直接采用 Spec Kit v2 schema**(社区已收敛,自创 7 元素是 NIH);IDS PRD 阶段保留 8 字段(idea→PRD 阶段 Spec Kit 也没标准),hand-off 时 operator 转写为 Spec Kit `spec.md` |
| **Multi-repo agent build** | Cursor 3 (2026-04) 推出**多根工作区**(multi-root workspace)+ 异步 subagent + isolated worktrees,**单 agent session 跨 frontend/backend/shared lib** 不重 retarget([Cursor changelog 04-24-26](https://cursor.com/changelog/04-24-26) / [AlternativeTo 2026-04](https://alternativeto.net/news/2026/4/cursor-3-launches-unified-multi-repo-workspace-for-building-software-with-ai-agents/)) | IDS↔ADP/XenoDev 是 2 仓 hand-off 模式(operator 切仓 + skill 触发),与 Cursor 多根工作区**正交**(它在 IDE 层串多仓,IDS-XenoDev 在文档协议层串 idea→build);但 hand-back 通道思路与 Cursor "subagent + worktree → 主线汇总" 同构 | **现有 SHARED-CONTRACT v2.0 双向 hand-off 设计成立**;不必改为 Cursor 式 IDE 多根(不同抽象层);可借鉴 Cursor 异步 subagent 的"主进程汇总" pattern 来设计 hand-back 包格式 |
| **Agent Skills 范式** | Anthropic Agent Skills(SKILL.md = YAML+Markdown,progressive disclosure)+ Spec Kit + addy osmani 三家共同共识;Skills 通过 code execution tool 接入 Messages API,**custom skills 与 prebuilt skills integration 形态相同**([Anthropic Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)) | ADP `.claude/skills/sdd-workflow/` + `task-decomposer/` 已是 SKILL.md 形态(port from IDS);IDS 这边也有同名 skills | XenoDev 起来时 **skills 物理 source-of-truth 应在 XenoDev**(L4 工具),IDS 这边的同名 skills 标 DEPRECATED 或迁出(解决 P1 §3 Q3 不确定性);两份并行 = 双 source 反模式 |
| **Failure case** | 2026 实证:**60% 无 AI-ready data 的项目会在 2026 被放弃**;agent PR 失败 4 类 = reviewer abandonment / PR-level / code-level / agentic-level([arxiv 2601.15195](https://arxiv.org/html/2601.15195) / [Forte Group 2026](https://www.fortegrp.com/insights/why-your-ai-pilots-are-stalling-and-how-agentic-data-engineering-fixes-that)) | V4 = "abandonment" 模式典型案例(operator 半年前停掉 + 半成品 + 现在决议不再维护);K7 显式 reframe 为"物证非吸收对象"是 sunk cost 健康止损 | 验证 GPT P1 §2 "Y5 = cut" 判断:**cut V4 作为继承对象** 是符合 2026 SOTA 实证的健康决策;Opus P1 §2 "L+P 全保 + C 部分 cp" 与 GPT 立场可融合(L+P 不是 V4 代码,是抽象 Lesson/Pattern;不冲突) |

## §2. 用户外部材料消化

**moderator-notes §四"V1 verdict 仅参考"** 与 SOTA 对照:Anthropic 4 月明示 Planner/Generator/Evaluator 三角是 production-validated pattern,**忌讳 shared context** — 这刚好对应 K7 + DRIFT-1:不能让 V1 verdict 当 shared context 污染 v2(V1 假设 IDS 自带 L4 build,这是错前提)。**强 binding 是对的,SOTA 支持。**

**moderator-notes §三 SHARED-CONTRACT v2.0 双向 hand-off** 与 SOTA 对照:Cursor 3 异步 subagent 模式是"主进程派发任务 + subagent 回汇报",同形态;hand-back 包**应像 Cursor subagent return** 一样结构化(drift / PRD 不够细 / 实践统计 三类标签),而非 free-text。

**moderator-notes §五 不重走 L1-L3** 与 SOTA 对照:Spec Kit "Specify→Plan→Tasks" 是 4 phase,不强制重走前 phase;Anthropic 三角也是 artifact 间 hand-off,不要求重 plan。**operator Q13 决议合理,SOTA 支持。**

**operator §六 strong-converge + 旁注补充** 与 SOTA 对照:Anthropic Evaluator agent 角色 = 独立质量评估,与"主线收敛 + v0.2 旁注"同构(主线 = Generator + Planner 的合力 verdict,旁注 = Evaluator 残余意见)。**模式映射 OK。**

## §3. 修正后的视角(P1 哪些站住、哪些被推翻)

**站住的 P1 判断**(SOTA 验证):
- §1 Y1 架构:"L1-L4 + forge 横切 = framework 默认骨架"是错前提 → SOTA(Spec Kit / Anthropic 三角)都是 4 phase 模式,没有 L1-L4 一条龙假设
- §2 Y2 工程:V4 6 模块的 sdd-workflow + task-decomposer + block-dangerous 是工业级实装 → 与 Spec Kit 4 phase 形成同构(可继承 L+P)
- §2 Y5 重做代价:"L+P 全保;C 部分 cp" → 与 GPT P1 "cut V4 作为继承对象,keep Lesson borrow Pattern" **可融合**(我的"L+P"对应他的"keep Lesson borrow Pattern";我说"C 部分 cp" 是指 block-dangerous.sh 这种纯工业共识脚本,他说"archive Component" 是指 V4 业务代码 — 实际无冲突,只是颗粒度不同)
- §3 不确定 1(应然分工边界)+ §3 不确定 3(skills 物理 source-of-truth)→ SOTA 给了答案:**XenoDev 直接用 Spec Kit v2 schema + skills 物理在 XenoDev**(NIH 反模式 SOTA 早共识)

**被 SOTA 推翻或细化的 P1 判断**:
- P1 §1 Y2 "spec_validator + reviewed-by 4 轮闭环 production-grade" → SOTA 视角下,**4 轮 codex review 是过度收敛风险**(Anthropic 推荐 Evaluator 一次独立评估即可);XenoDev 起来时 reviewed-by 应降到 1-2 轮 + 显式 Evaluator role,不应原样 cp V4 4 轮模式
- P1 §2 Y2 "保留 retrospective skill" → SOTA 视角下,V4 retrospective L1+L2 + lessons/ user scope 是**未经实证的实验性设计**(V4 dogfood 12 周 0 次跑过);**XenoDev 不应直接继承,应在 XenoDev 真 dogfood 后回炉重做**
- P1 §2 architecture "new XenoDev 仓" 的具体形态 → SOTA(Cursor multi-root)给替代方案:**多根工作区在 IDE 层串多仓**;但 ADP-next 选 IDE-层 vs 文档协议层是 operator 偏好(operator §六已选文档协议层 = 新仓 + SHARED-CONTRACT v2.0,**保持原决定 OK**,因为 operator 不用 Cursor)
- P1 §3 不确定 2(B1 IDS 优化 vs B2 XenoDev L4 耦合度) → SOTA 视角下,Spec Kit 4 phase 是**强顺序**(Specify → Plan → Tasks 不能并行),所以 **B1 SHARED-CONTRACT v2.0 必须先 → B2 XenoDev hand-off 才能跑**;**回答 OK 收敛**

**P3R1 应聚焦的真分歧**:
1. V4 reviewed-by 4 轮模式的处置(Opus P1 倾向 keep,SOTA 推翻 → 应改为 1-2 轮 + Evaluator role)
2. retrospective skill 的处置(Opus P1 倾向 keep+refactor,SOTA 推翻 → cut 在 XenoDev 重做)
3. ADP-next/XenoDev 是否直接 fork Spec Kit v2 vs 自创 schema 7 元素(SOTA 强烈建议 fork,operator 待决)
