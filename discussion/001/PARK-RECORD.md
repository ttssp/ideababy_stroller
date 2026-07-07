# Park record · 001

**Parked at**: 2026-04-23T09:32:00Z
**Status before parking**: L1 Inspire 完成（menu-ready，13 条 directions，5 条 both-endorsed，尚未 fork）
**Reason for parking**: menu 已就位但暂时不作 fork 决策，隔一段时间再看
**Revival condition**: 暂无明确条件，凭后续直觉/时机决定
**Revival check date**: 2026-05-23（30 天后系统提醒回看）

## What we have so far
- L1 inspire menu: [stage-L1-inspire.md](./L1/stage-L1-inspire.md)（13 directions，Synthesizer Top 3 = `001a` Dissent Cartographer · `001c` Question→Dissent Belief Router · `001b` Lab-Scale Shared Intelligence）
- L1R1 rounds: [Opus](./L1/L1R1-Opus47Max.md) · [GPT-5.4](./L1/L1R1-GPT54xHigh.md)
- L1R2 rounds (cross + value validation): [Opus](./L1/L1R2-Opus47Max.md) · [GPT-5.4](./L1/L1R2-GPT54xHigh.md)（GPT 跑了 21 次搜索）
- L2 explore report: n/a
- L3 scope decision: n/a
- Code: n/a

## Lessons captured during the live phase

即便不 fork 也值得记下来的几个观察（来自 synthesizer 的交叉分析）：

1. **双方独立收敛到的三条强候选方向**：Dissent Cartographer（反共识雷达）、Lab-Scale Shared Intelligence（lab 级共享认知）、Question→Dissent Belief Router（以 lab 活问题为中心的 belief 路由）。两轮 R2 都把这三条放进 Top 3 —— 收敛信号强。
2. **整份菜单暗含一次重大 reframe**：原提案的真实锚点可能不是 "跟不上信息"（throughput 问题），而是 **judgement 形成**。菜单里所有 high-spark 方向都在往 judgement / taste / conviction / immune-system 这个轴上滑。如果以后回来，这个 reframe 值得作为 L2 的默认背景。
3. **"个人 vs lab" 是产品骨架级别的决策**。不是 feature 差异，是产品物种差异。Lab infra 方向（001b, 001c 的 lab 版, 001e 的 lab 版）是 2026 全市场的结构性空白——所有 11 个主流 literature AI 工具都是 individual-user 定位。
4. **最大 structured 空白是 Dissent Cartographer**：所有现有 radar 的 incentive 都在放大 mainstream 信号，没有人在 structurally 捕捉 anti-mainstream 信号。PubPeer / Retraction Watch 是人工新闻站不是系统工具。注意 cultural failure mode（gotcha / negativity spiral）必须提前对冲。
5. **菜单里未被充分探索的维度**（以后 re-inspire 可以 steer 的方向）：
   - 时间尺度的极端版本（10 年考古 / 实时 live）
   - 与 reading group / journal club / 周会的社会仪式绑定
   - Non-AI domain transplant（Legal / wet-lab biology / policy / education）
   - 对抗 AI 生成灌水论文的视角（2026 显性 risk，整份菜单只有 Dissent 方向擦过）
6. **Key Mind Tracking 的 1.0 饱和，2.0 空白**：Semantic Scholar / alphaXiv / Benty Fields 都有 author alerts 但停在 new-paper notification；focus shift detection（"Ilya 的焦点从 X 漂到 Y"）是 10 年没被做出来的空白 —— 要么难做，要么 PMF 不硬。

## Revival checklist

回来时先做这几件事：
1. `/status 001` 加载所有 artifact
2. 重读 `L1/stage-L1-inspire.md` 的 "Themes I notice" 和 "What's notably missing" 两节
3. 判断：市场是否出现新的 prior art 让某条 direction 不再空白？是否有新的 failure case 让某条 direction 需要重估？
4. 决定：直接 `/fork 001 from-L1 direction-<n> as <id>` 还是先 `/inspire-inject 001 "<steering>"` 再重跑一轮

---

To resume: run `/status 001` —— 所有 artifact 保留，什么都没丢。

---

## 二次 park（2026-07-06）

**上次 park 后发生了什么**：2026-04-23 首次 park 后曾 revive，proposals 状态改为 `exploring (L2 进行中)`，但 **L2 实际从未真正推进** —— `stage-L2-explore-001.md` 之后约 2 个月无实质动作，"exploring" 名不副实。

**再次 park 原因**：名义在 L2 但长期停滞；operator 当前主攻投资闭环 009 + 框架 006，001 的 Research Radar 方向不在近期主推面。与其挂个假 exploring，不如诚实 park。

**Revival condition**（沿用首次 + 补充）：market 出现新 prior art 让某条 direction 不再空白，或 operator 认知带宽腾出、想重拾 "judgement 形成" 这个 reframe 轴时。首次 park 的 revival checklist（上方）仍适用。

**这次没丢任何东西**：L1 menu（13 directions）+ L2R1/R2 rounds + stage-L2-explore-001.md 全在。revive 时从 L2 继续或 `/inspire-inject` 重 steer 均可。

---

## REVIVE（2026-07-06 · 转向 Topic Cartographer / KG-radar 方向）

**为什么 revive**：operator 澄清了真实愿景 —— 要的不是当年 fork 的 **001-pA「PI Briefing Console」**（那是主动砍窄的每日简报版，PRD 明确删掉了知识图谱），而是一个 **Paper Radar agent**：持续收集 SOTA 文章、构建 paper/方法的**知识图谱 + 知识库**、帮 AI lab 负责人快速跟进 SOTA + 把握研究方向 **big picture**。

**关键发现**：这个愿景几乎就是 001 最原始提案原文（"多层级 topic 知识库 + 时间线/同源/继承/对立检索 + 实时 SOTA"），且**精确匹配 L1 菜单 Direction 7「Topic Cartographer（做地图不做流）」** —— 节点=工作，边=derives-from/contradicts/generalizes/supersedes，看领域半年"位移"。**这条方向 L1 探过但从没 fork。**

**重启方式**：fork Direction 7 为新 sibling（走 pipeline L2→L3→L4），**不是** build 那份错方向的窄 spec。001-pA（PI Briefing）作为一个 valid sibling 保留不动，其 paper 收集 pipeline / T001 LLM 成本教训 / 双 persona 可作参考。核心待解问题：与 Connected Papers / Litmaps / ResearchRabbit 的图视图差异化（L2/L3 必答）。方案见 `~/.claude/plans/robust-wondering-naur.md`。

