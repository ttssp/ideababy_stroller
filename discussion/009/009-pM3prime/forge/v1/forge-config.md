---
forge_version: v1
created: 2026-07-23T09:05:00Z
convergence_mode: strong-converge
x_hash: df74b5e59ff6526c031d6f4dcf352696
prefill_source: manual
fork_id: 009-pM3prime
triggering_handback: 009-pM3prime-20260723T082127Z
---

# Forge Config · 009-pM3prime · v1

## X · 审阅标的

（operator 与 orchestrator 协商拟定 · 核实全部可达 · 2026-07-23）

本次 forge 由 handback `009-pM3prime-20260723T082127Z`(FU-KG42 · prd-revision-trigger)触发。
证伪链 E1 密度普查已收口(US go · HANDBACK-LOG 第 25 条),但最后一块「两层金标 Layer-2 验收」
撞 frozen PRD 内部约束冲突(§2 单人不懂投资 × §4-E1/D-7 领域独立真人第二源)→ Layer-2 无合格
验收主体。operator 提出核心质疑:**2026 顶尖强模型 + 异源,能否当合法第二源(替代 D-7 的"真人")?**

### 解析后的标的清单

- `discussion/009/handback/20260723T082127Z-009-pM3prime-20260723T082127Z.md`(类型:本仓库文件 · handback 冲突主诉 · 全文)
- `discussion/009/009-pM3prime/PRD.md`(类型:本仓库文件 · **重点读 §2 Users [L56-58] + §4-E1 金标两层验收 [L97-142]**,即 frozen 冲突的两造)
- `/home/ys/codes/XenoDev-009/specs/009-pM3prime/spec.md`(类型:外部 repo · **重点 D-7 [L209] / C9 [L191] / O7-O8 [L261-262] / O7-O8 状态注 [L115-117]**,硬约束落点 + G-R1 先例引用)
- `/home/ys/codes/XenoDev-009/projects/004-pB/src/decision_ledger/extraction/gold_layer2.py`(类型:外部 repo · **重点 :81 second_source_kind != 'human' → raise**,把 D-7 焊死的代码)
- `/home/ys/codes/XenoDev-009/projects/004-pB/src/decision_ledger/extraction/gold_layer1.py`(类型:外部 repo · Layer-1 span 金标 harness · 对照 Layer-2)
- `/home/ys/codes/XenoDev-009/specs/009-pM3prime/risks.md`(类型:外部 repo · **重点 E1-R2 [L43-57]**,双模型 echo-chamber 下游后果 + 009-pForge G-R1 同类先例 + 缓解措施)
- `/home/ys/codes/XenoDev-009/dogfood-backlog.md`(类型:外部 repo · **重点 KG-42 [L789]**,证伪链金标框架缺「第二源可得性」立项前置校验)

**沙箱注记**:X 含 XenoDev-009 外部 repo 路径。Codex 默认沙箱在 ideababy_stroller 内,读 `/home/ys/codes/XenoDev-009/*`
可能 BLOCK。ideababy_stroller 已 trust_level=trusted;若 Codex 端 BLOCK,按 SKILL §"Codex sandbox edge cases"
处理(剔标的重跑 / 调沙箱 scope / 关键内容直贴)。orchestrator Phase 推进前 grep outbox 首 30 行有无 `Verdict: BLOCK`。

## Y · 审阅视角

✅ **验证方法学/认识论**(自定义 · 核心)—— 金标验收的认识论基础:什么才算「独立第二源」;异源模型
   错误相关性多高算「独立」;009-pForge G-R1 双模型 echo-chamber 实证在「异源强模型」下是否仍成立;
   D-7「领域独立真人」要求的根本目的(捕捉提取器捕不到的隐性错误)在异源模型下能否达成。
✅ **架构设计** —— 两层金标 harness / gate(fail-closed)/ 第二源接入点的可演化性;若放宽 D-7 到异源模型
   或定降级验收口径,架构改动面多大;harness 现结构能否零代码/低代码接入新验收姿态。
✅ **产品价值** —— 三方向 (a)/(b)/(c) 哪个让「单人自用不懂投资 operator」这个真实用户真正拿到可信信号;
   降级验收会不会让 E1 交付物失去 ROI 意义(密度实测达标但信号质量没验 = 半成品)。

（operator 显式未选「工程纪律」—— 聚焦认识论+架构+产品,不发散到 harness 实装/测试/CI 细节。）

## Z · 参照系

mode: 对标 SOTA

双方在 P2 各自检索领域 SOTA,聚焦「LLM 当验证/判断源的独立性与错误相关性」:
- LLM-as-judge 的独立性 / self-preference bias / 与被判对象同源时的相关误差
- 多模型集成判断(ensemble judging)错误相关性实证 —— 异源到什么程度才降低相关性
- echo-chamber / 模型同构盲区的实证研究
- 人机混合验收(human-in-the-loop acceptance)何时人不可替代
- 跨谱系模型(不同 vendor/架构)在同一 NL→结构化任务上的错误独立性证据

**外部材料叠加**:无额外 operator 外部链接(K 已含全部关切)。

## W · 产出形态

✅ **verdict-only**(扩展 rationale 200-500 字)—— 单一 verdict:异源强模型能否当 D-7 合法第二源
✅ **decision-list**(4 列矩阵)—— handback 三方向 (a)放宽D-7 / (b)降级验收 / (c)找真人源 逐条给
   保留/调整/删除/新增判决 + 引 evidence
✅ **next-PRD**(D-7 改写草案)—— 若 verdict 倾向改 D-7 措辞,给出 D-7 / §4-E1 可落地改写草案段

（按上面顺序拼接,共享前置 §Verdict + §Evidence map。）

## K · 用户判准

2026 顶尖强模型(如 GPT-5.6-Sol xhigh / Claude Opus)已在很多任务上强过普通人。operator 的核心质疑:
**这样的模型 + 异源(谱系不同于提取器),在「把自然语言笔记/直播片段映射成可交易信号」这个具体任务上,
独立性够不够格当 D-7 金标第二源?**

关键约束与背景:
- D-7 现在硬要「领域独立**真人**第二源」(`gold_layer2.py:81` 焊死:非 human → raise),其**根源是 009-pForge
  G-R1 双模型 echo-chamber 实证**(两个 LLM 在同一任务上犯高度相关的同类错,第二个 LLM 会给提取器的错盖章通过 = 没验)。
  → forge 必须**直面 G-R1 这个先例**:它证的是「同源/同构双 LLM 不独立」,还是「任何双 LLM 都不独立」?异源强模型是否逃出这个结论?
- **若模型够独立** → 要定「异源够独立」的可操作判据:错误相关性怎么量化、可接受阈值是多少、怎么证一对具体模型达标。
- **若模型不够独立** → 在「单人自用、不懂投资、供不出领域真人第二源」这个 frozen 现实下(PRD §2),降级验收怎么设计
  (如:只做 Layer-1 span 一致性验收 + Layer-2 标 known-limitation;或外部众包;或定义「无合格第二源时的降级口径」)。
- **红线(绝不接受)**:用第二个同源/弱异源 LLM 假装过 Layer-2 = echo-chamber 假过 = CLAUDE.md 点名的 V4 失败模式。
  「金标诚实待第二源」是合法 STOP;凑假金标不是。verdict 必须显式守住这条红线。
- 元层自证:本 forge 本身就是「两个异源强模型交叉审」——若连 forge 内 Claude×GPT-5.6-Sol 都收敛不出可信结论、
  暴露同构盲区,那本身就是「异源模型第二源不够独立」的一个实证信号;若两方能互揪对方漏,也是证据。reviewer 可留意这层。

## 收敛强度

✅ strong-converge

---

## Summary for reviewers

**审阅标的总数**: 7(2 本仓库文件 + 5 XenoDev-009 外部 repo 文件)
**视角维度**: 验证方法学/认识论(核心) · 架构设计 · 产品价值
**参照系**: 对标 SOTA —— LLM-as-judge 独立性 / 多模型集成错误相关性 / echo-chamber 实证 / 人机混合验收
**预期产出**: verdict + rationale · decision-list(三方向采纳矩阵)· next-PRD(D-7 改写草案)
**用户最在乎**: 2026 异源强模型能否当 D-7 金标第二源(替代"真人"),取代/放宽/降级三条路怎么选;必须直面 009-pForge
  G-R1 双模型 echo-chamber 先例、守住"不许第二 LLM 假过"(V4)红线;若放宽需给"异源够独立"的可操作判据,
  若不放宽需给单人 operator 供不出真人源现实下的降级验收设计。
**收敛模式**: strong-converge(P3R2 finalize 单一 verdict,残余分歧降 v0.2 note)
