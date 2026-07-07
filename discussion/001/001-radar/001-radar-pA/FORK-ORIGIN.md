# Fork origin

**This fork**: 001-radar-pA
**Forked from**: 001-radar · L3
**Source stage doc**: [../L3/stage-L3-scope-001-radar.md](../L3/stage-L3-scope-001-radar.md)
**Selected candidate**: Candidate A · "方向评估官（历史位移内嵌）"
**Candidate description (extracted from source)**:

一个**按需出动**的研究方向评估 agent。给它一个方向（一句描述或 2-3 篇种子 paper），它冷启动
重建该方向的公开研究脉络（含 2-3 个历史时间切片），交付一份**强观点评估 briefing**：结构成没成型
（分散爆发 vs 稳定问题簇+方法簇互连）、核心 claim、"如何从热词变成结构（或为什么没有）"的历史
位移证据、结论落在投入/试点/观察/暂缓（词表借 Tech Radar 四环），每条判断 3 击内到原文。评估留档
进 journal 供后验复核 + taste 反馈标记。**不常驻、不推送、不做组合盘**——评估哪个方向,哪个方向的
地图才存在,用完即完整。~9-11 周 @20h,盒内有余量,双方 R2 均列为最稳验证 cut。

**Forked at**: 2026-07-07T02:58:21Z
**Forked by**: human moderator (via /fork command · L3 菜单选项 [1] 推荐候选)
**Rationale**:

intake 亲选的冷启动仪式 + 窄切成功先例（Connected Papers/Undermind 单动作起家）+ 预算余量
都指向 A。**B（评估→留驻漏斗）不是被拒的 sibling,是同一产品晚一个 phase 的样子**——A 的评估
journal 使用数据（operator 会不会回访旧评估）直接验证 B 的核心假设,到时从同一份 L3 菜单
fork B 不用重跑 L3。

---

## What this fork is for

Now `001-radar-pA` is its own PRD branch. PRD.md（本目录）是 L4 的 source of truth。Run:

  /plan-start 001-radar-pA

（L4 产 HANDOFF.md → XenoDev build runtime 消费,per SHARED-CONTRACT §6）

## Sibling forks (for cross-reference)

- **001-radar-pA**（this one）— L3 Candidate A「方向评估官（历史位移内嵌）」
- （未 fork,留在菜单里）L3 Candidate B「评估→留驻漏斗（组合盘）」— 数据驱动的自然 v0.2:
  若 A 的 journal 数据显示 operator 反复回访旧评估,fork B 即为顺承 phase,无需重跑 L3
- （不同世系的叔辈）001-pA「PI Briefing Console」— 001 直接 L3 的产物,窄简报形态,
  Phase 0 kickoff-ready 后停;其 paper 收集 pipeline / T001 LLM 成本教训可作 L4 参考
