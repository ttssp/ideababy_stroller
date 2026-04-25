# Fork origin

**This fork**: `004-pB`
**Forked from**: `004` · L3
**Source stage doc**: `discussion/004/L3/stage-L3-scope-004.md`
**Selected candidate**: Candidate B · "决策账本" (承诺壳, impulse → discipline calibration)

## Candidate description (paraphrased from source)

Web-first + log-heavy 决策账本台。周报和 event 卡都仍然存在, 但它们是入口不是主角。v0.1 的核心是把每次 `动 / 不动 / 等待` 都沉淀成一条"决策档案": 咨询师观点、占位模型信号、agent 综合建议、冲突报告、human 最终决定 + 1 行理由、环境快照、事后回看字段。Web UI 是主场 (本地 localhost, 不追 polish), Telegram 只做提醒和入口。关键 UX 门槛: 单次决策录入 < 30 秒, 否则退化为日志弃用工具。

**痛点假设**: "我知道很多, 但压力下不稳定, 临场乱动。" 不是"我信息不够", 是"我约束不够"。

**独特 slice**: 事前 pre-commit 决策 + 事后复盘双侧。GPT L3R2 scope-reality search 显示: Fiscal.ai / Koyfin / Aiera / Bridgewise / 雪球付费 五项产品全做**信息壳**, 无人做**承诺壳**。B 是 uniquely 空白的 market slice。

**预计时间**: 5-6 周 / 100-160 小时 · 置信度 M
**最大风险**: upkeep 负担 (录入 >30 秒即死)

**Forked at**: 2026-04-25T02:16:00Z
**Forked by**: human moderator (经由 fork command, skill 已知 bug 手动执行)

## Rationale

Synthesizer 基于三条收敛证据强推 B:

1. **GPT L3R2 scope-reality search** — 信息壳市场饱和 (5 项产品全做), 承诺壳 uniquely 空白
2. **L2 v2 核心洞见** "calibration engine first, action engine second" 直接指向 B
3. **Barber-Odean 铁律** (散户越频交越差) 说明"减少乱动" = 最大价值源, B 直接命中

Human 接受了 synthesizer 推荐, fork 前按照 handoff 计划直接进 L4 plan。

`/plan-start` 前**强建议**先做自我访谈压测: 连续 5 次尝试决策档案录入, 单次 < 30 秒 — 若嫌重, 降级到 "B-lite" 或改 fork A。

---

## What this fork is for

`004-pB` 是独立的子树, 下一层 (L4 Plan) 将把本 fork 的 PRD.md 作为 spec-writer 的输入, 产出完整 SDD 包 (spec.md / architecture.md / tech-stack.md / SLA.md / risks.md / non-goals.md / compliance.md), 接着 task-decomposer 拆 DAG, Codex 做 adversarial review loop。

**进入下一层的命令**:
```
/plan-start 004-pB
```

## Sibling forks (for cross-reference)

本 fork 是 004 · L3 的**第一个 fork**. 其它 L3 候选仍在 menu 中可被未来 fork:

- **004-pA (未 fork)** — Candidate A · 研究收件箱 (信息壳, noise→signal). 若未来想并行做信息壳角度, 可 `/fork 004 from-L3 candidate-A as 004-pA`.
- **004-pC (未 fork)** — Candidate C · 事件卡台 (事件 calibration). 同上可 fork.

## Related handoff

完整的 L4 onboarding handoff (给新 session 或新 contributor): `discussion/004/HANDOFF-L4.md` — 包含 PRD 提炼、全套红线、🧭 策略模块占位原则、spec-writer 重点、task-decomposer 优先级建议。

**新 session 进入 L4 必读顺序**:
1. `discussion/004/HANDOFF-L4.md` (压缩上下文)
2. `discussion/004/004-pB/PRD.md` (本 fork 的权威 PRD)
3. `discussion/004/004-pB/FORK-ORIGIN.md` (此文件)
4. `discussion/004/L3/L3R0-intake.md` (hard constraints 全集)
5. `discussion/004/L2/moderator-notes.md` (L2 framing 校正)
