---
forge_version: v1
created: 2026-07-15T13:22:01Z
convergence_mode: strong-converge
x_hash: 7fb3c580d1ed08629fd2e6333183f1d7
prefill_source: proposals.md§001
---

# Forge Config · 001 · v1

> **本次 forge 的真实标的**(prefill 语境错位提示,human 已确认):不是 root proposal §001
> 那句宽泛的 research-radar seed,而是**已 ship 的 001-radar-pA build 里 P0.2 盲测 gate
> 的形态治理**——触发源 = hand-back `001-radar-pA-20260715T093226Z`(operator 真跑拒签
> gate 形态),同簇审 KG-B8(gate 形态该不该存在)+ KG-B4(gate 无机器强制)+ KG-B7
> (反作弊单次执行)。HANDBACK-LOG 末条 operator 决议明确勾「起 forge 同簇审」。

## X · 审阅标的

来源:prefill bundle:forge-target(5 件)+ operator 追加 3 件(injection 77a5176 /
首跑 FAIL 对照 / 跨仓 KG 原文)。

### 解析后的标的清单

1. `TEXT:` proposal §001「Research Radar」原文(proposals.md:99-134)(类型:粘贴文本 · 背景 seed,idea 原始愿景,非本次审阅重心)
2. `discussion/001/001-radar/L3/stage-L3-scope-001-radar.md`(类型:stage 文档 · scope 语境:Candidate A/B 菜单 + 信任建立机制三件套的出处)
3. `discussion/001/001-radar/001-radar-pA/PRD.md`(类型:本仓库文件 · **PRD v1.2 · gate 形态直接标的**,含 O4 两层信任 + v1.1/v1.2 演进 + 两次 injection response)
4. `discussion/001/handback/20260715T093226Z-001-radar-pA-20260715T093226Z.md`(类型:本仓库文件 · **触发本次 forge 的 hand-back · 第一因**,operator 三条批评原话 + §3 建议 A/B/C)
5. `discussion/001/handback/HANDBACK-LOG.md`(类型:本仓库文件 · 11 条决议史 SSOT,gate 演进 + KG-B4/B5/B7/B8 脉络)
6. `discussion/001/001-radar/L3/moderator-notes.md`(类型:本仓库文件 · injection 77a5176 @2026-07-10 主锚移 O2+O7 + injection @2026-07-13 价值重定义 → v1.2)
7. `discussion/001/handback/20260711T135303Z-001-radar-pA-20260711T135303Z.md`(类型:本仓库文件 · P0.2 首跑 FAIL hand-back,**能力层 FAIL** vs 本次**结构层拒签**的关键对照)
8. `/home/ys/codes/XenoDev/dogfood-backlog.md`(类型:外部 repo 文件 · ⚠ Codex 沙箱可能 BLOCK · KG-B4 @:525 / KG-B7 @:588 / KG-B8 @:602 三条同簇原文;inbox 任务内附关键摘录兜底,BLOCK 时用摘录不判 BLOCK)

## Y · 审阅视角

✅ 工程纪律 — gate/验收机制、TDD/review 流、防 V4 铁律的形态
✅ 架构设计 — PPV 结构、T010/T011 解锁依赖、O2/O7 信任链的可演化性
✅ 产品价值 — 验证范式是否贴 operator 真实工作流(边用边审计 vs 停下来考试)

## Z · 参照系

mode: 对标 SOTA

**检索方向约束**(非指定列表,双方 P2 各自检索,但限定在验证/gate 设计先例层):
- human-in-the-loop evaluation 设计(盲测 vs 抽查审计 vs 后验校准的取舍先例)
- audit-trail / provenance-based 验收(每条判断带 trace、抽查验收的工程先例)
- LLM-as-judge / eval 校准(人类判据不可靠时的统计功效处理)
- 后验闭环(production eval / online calibration,边用边校准的机制先例)

⚠ prefill 提醒已确认:proposal 里的 autoresearch / 9-opus 是**终局愿景层**对标,
不是 gate 形态层对标,P2 不要跑偏到那里。

**外部材料叠加**:无(K 内无额外链接)。

## W · 产出形态

✅ verdict-only — gate 形态去留的核心裁决 + rationale
✅ decision-list — keep/调整/删除/新增 4 列矩阵(KG-B4/B7/B8 三层各需明确裁决)
✅ next-PRD — PRD v1.3 草案方向(O4/PPV 章节重写 + T010/T011 新解锁条件)
✅ refactor-plan — 盲测二值 → 新验收形态的按模块落地路径(XenoDev 改 spec 时直接消费)

## K · 用户判准

**原始愿景(背景 seed,proposal §001 原文)**:做一个 research radar,自动发现/跟进最新
AI 研究(arxiv/顶会/lab blog/repo),下载解析解读分析,构建多层级 topic 知识库,及时跟进+
梳理脉络+归纳进展,为 brainstorm/research 提供可靠前瞻判断。终局 = 结合 autoresearch/9-opus
优势构建 lab research agent;本 idea 是第一步(先做深理解)。

**本次 forge 真实标的(非上面宽泛 seed)**:已 ship 的 001-radar-pA build 里 **P0.2 盲测
gate 的形态治理**。operator 真跑拒签「人肉盲测二值签字」形态,三条批评:①operator 非可靠
打分器(单轮 3 切片 1 负控,功效低)②应留痕可审计,不应盲测签字(每条位移判断留 source
trace + 抽查 + log 回溯)③应边用边迭代,不应前置一次性闸门(只得 local 解且费时费力)。
同簇三层一并审:**KG-B8**(gate 形态该不该存在)+ **KG-B4**(gate PASS 无机器强制)+
**KG-B7**(反作弊单次执行)。

**预置输入 1 · 必须裁的张力**:PRD v1.2(a5b6044)已收敛 gate 到要件①②、③record-not-block,
但**保留 RERUN-PASS 为 T010/T011 唯一前置**;hand-back §3.A 更进一步——彻底去二值硬前置,
改「可审计留痕验收 + O7 journal 后验闭环」。forge 要裁的正是这条线画在哪:保留弱化版 gate,
还是彻底改验收范式。

**预置输入 2 · 过度投资教训作证据**:T004-A1 花 codex 14 轮把 gate 硬化到防作弊(KG-B7),
随即被 KG-B8 推翻前提——「先修下游再被上游推翻」的实证。支持先裁 B8 的次序论:若去掉二值
硬 gate,B4/B7 攻击面大概率自然消解,别再往被拒形态上加固。

**我在乎**:验证范式要贴 operator 真实工作流(边用边审计,不是停下来考试);裁决要给出
T010/T011 的新解锁条件(不能悬空);防 V4 铁律(FAIL→STOP→回流)的精神要保留,哪怕形态变。
**我不在乎**:gate 现有代码的沉没成本;保住 T004-A1 那 14 轮投入的面子。

## 收敛强度

✅ strong-converge

---

## Summary for reviewers

**审阅标的总数**: 8(1 粘贴文本 + 6 本仓库文件/stage 文档 + 1 外部 repo 文件)
**视角维度**: 工程纪律 · 架构设计 · 产品价值
**参照系**: 对标 SOTA(验证/gate 设计先例:human-in-loop eval / audit-trail 验收 / LLM-judge 校准 / 后验闭环)
**预期产出**: verdict-only + decision-list + next-PRD + refactor-plan
**用户最在乎**: P0.2 盲测 gate 形态被 operator 真跑拒签后,裁「保留弱化 gate vs 彻底改
可审计留痕验收」这条线画在哪;KG-B4/B7/B8 同簇三层一并裁,给出 T010/T011 新解锁条件;
防 V4 精神保留但形态可变;不看沉没成本。
**收敛模式**: strong-converge
