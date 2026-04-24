# Fork origin

**This fork**: 001-pA
**Forked from**: 001 · L3
**Source stage doc**: ../L3/stage-L3-scope-001.md
**Selected candidate**: Candidate A · "PI Briefing Console"
**Candidate description (extracted from source)**:

一个**只做每日 topic-state briefing + 低价值留痕**的极简 Web 工具。面向 8–15 个 topic，每天生成一份 briefing，按 "state shift"（不是论文堆叠）组织；每篇新工作都有 4-action 归档 —— read now / read later / skip / breadcrumb；breadcrumb 带 6 周 / 3 个月 / 6 个月的 resurface 逻辑。

v0.1 的 bet 是 "digest-first briefing + 可剪枝 breadcrumb" 这一对 novelty axis 值不值得花时间；为此主动砍掉完整 taste agent 闭环、topology graph、lab shared view 深度协作，只剩一个 loop：每天打开 → 读 briefing → 对每篇做 4-action → 系统记住 → 在未来合适的时间 resurface。

**双 persona + PI 优先**（硬约束）：
- 主 persona = Dr. Chen 类型 PI（经济 buyer + 决策者，每天 8:00 10 分钟扫完 8–15 topic、定今日深入方向）
- 次 persona = Maya 类型 senior PhD/postdoc（独立 login、独立 seat，全员 read+write，admin 管理 topic 池；日常替 lab 做 triage 并对 skip/breadcrumb 写轻量 "why I disagree"）

**三角取舍**：Speed + Differentiation 并存，主动放弃 Polish。UI 粗糙可接受（表格 + 纯文本 briefing），但 "digest-by-state-shift" 和 "breadcrumb resurface" 两条 core bet 必须做对。

**时间**：~5 周 @ 20h/周（Opus+GPT R2 合并中值，已包含 operator 独立 login 修正），confidence Medium-High。主要 unknown 是 LLM 解读质量 —— 若失败 briefing 会退化成 summary list，day-30 必须陪 PI 实际用 ≥ 10 次校准。

**Kill-window**：60 天（不是 30 天）—— Readwise spaced repetition 的 aha 窗口 ~30 天累积，breadcrumb resurface 的 aha 更晚，需要 45–60 天真实陪跑。

**A 的战略定位**：三候选中 risk-management 最占优的起点；若 60 天验证成功，可直接扩展为 B（Lab Dossier Beta），已完成 scope 可复用 40–60%，不是从 0 并行重建。

**Forked at**: 2026-04-23T13:27:47Z
**Forked by**: human moderator (via /fork command)
**Rationale** (optional, human can fill in):

[ ___________________________________________________ ]

---

## What this fork is for

现在 `001-pA` 是独立 sub-tree。下一层 L4（Plan）将把上面 candidate 视作一份已确定的 PRD，产出 spec + architecture + tasks。PRD.md 与本文件在同一目录，是 L4 的 source of truth。

下一步：

```
/plan-start 001-pA
```

## Sibling forks (for cross-reference)

来自同一 L3 stage 文档的三候选：

- **001-pA**（本 fork）· Candidate A · PI Briefing Console · 5 周 @ 20h/周 · Speed + Differentiation · 🟢 Typical
- 001-pB（未 fork）· Candidate B · Lab Dossier Beta · 12–14 周 beta · Differentiation + Polish · 🟡 Ambitious
- 001-pC（未 fork）· Candidate C · Polished Personal Lab Radar · 6–7 周 · Speed + Polish · 🟢 Typical (v0.1) / ⚠️ Undershooting (v1.0+)

**Synthesizer recommendation**: fork A 作为主 fork，B 留作 "A 验证成功后的升级路径" 而非从 0 并行；C 不推荐起点。上游 lineage：

```
proposals/proposals.md · entry 001 (Research Radar)
  → discussion/001/L1/stage-L1-inspire.md (13 directions)
    → discussion/001/L2/stage-L2-explore-001.md (deep unpack)
      → discussion/001/L3/stage-L3-scope-001.md (3 candidates)
        → discussion/001/001-pA/ (本 fork · candidate A)
```
