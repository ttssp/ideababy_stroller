# L3R0 · Human Intake · 001

**Captured**: 2026-04-23T10:55:00Z
**Method**: AskUserQuestion interactive（8 个 block）
**Human**: idea owner（原 proposal 作者 / lab 运营者）

---

## Block 1 — Time reality

### Target delivery
- ❓ **Human 选：让模型先定 scope，再匹配时间**
- Implication：L3R1 模型须以**价值密度**为主导产 2-3 个 scope 候选，每个候选**给出各自诚实的所需时间**，让 human 通过 scope 选时间（而不是通过时间压 scope）

### Weekly hours
- ✅ **15-30 小时 / 周（serious commitment）**
- 取中位 ~20 小时 / 周用于时间估算；如果候选方案需要 40+ 小时等价，必须显式标注"超出你当前投入"而不是偷偷压缩 scope

---

## Block 2 — Audience reach (narrowing)

### First user slice
- 🤔 **Human 选：Block 1 (PI / Dr. Chen 类型) 优先 + Block 2 (senior PhD/postdoc / Maya 类型) 次选**
- 原话："1 & 2, 1 in priority"
- Implication（这是一个双 persona + PI-first 的组合，不是二选一）：
  - L3R1 必须**同时服务**两类用户，但**优先级不同** —— 产品形状和功能重心应该**先让 PI 能用（买单、做决策）、然后确保 senior PhD/postdoc 作为高频 operator 不会被牺牲**
  - 这与 L2 report §1 的 buyer/operator split 完美对齐：PI 是经济 buyer + 决策者，operator 是高频使用者；双层必须都被 serve，但 entry point 和重心以 PI 为先
  - **Carol 类型（onboarding 场景）优先级降级为 v0.2+**，不是 v0.1 必备
  - 候选之间可以在"how much operator polish before shipping for PI"上拉开差异

---

## Block 3 — Business model

- ✅ **先免费，未来可能有付费层**
- Implication：
  - v0.1 **预留 auth 但不做 billing**；auth 可以做到最轻（lab 邀请码 / 团队 admin invite），不是消费级 OAuth
  - scope 不为商业化付代价，但数据模型和权限设计要留"以后能分 free/paid tier"的缝
  - L3R1 的候选不必在"如何收钱"上做决策，但**必须避免做出让将来付费层不可能的早期决策**（比如把所有价值都做成公开免费无账户的形态）

---

## Block 4 — Platform

- ✅ **没强烈偏好 / 选适合 idea 的**（user notes: 由模型选）
- L3R1 建议默认 **Web-first**：digest-first homepage + topology as explainer layer + rich rendering 都在 Web 上最自然；desktop / CLI 可作为 Candidate 差异化维度或 extension
- 模型可以在某个候选里用"Web + 开放 API"组合来兼顾差异化

---

## Block 5 — Red lines

- ❓ **Human 选：让模型提 3 条 likely red lines**
- L3R1 §5 必须基于 L2 §5 "natural limits" 提出 3 条候选 red lines，human 在 L3 menu 阶段确认 / 否决

**模型将基于 L2 limits 提议的候选 red lines（预览，以 L3R1 §5 为准）**：
1. **不强吃 long-tail topic**（8-15 topic 是护城河；超出会退化）
2. **不替代第一手阅读**（委托 triage ≠ 替代 reading；后者会让品味退化）
3. **v0.1 不做公开打分 / 社区 review 市场**（Paperstars 式公开评分会把 lab 信任变成表演）

---

## Block 6 — Priorities

- ✅ **Human 选：Speed to ship + Differentiation + Polish/UX quality（三个全选）**
- ⚠️ **重要 flag：priorities 三角冲突** —— Speed 与 Polish 冲突；Speed 与 Differentiation（需要多 feature 堆出独特价值）冲突；Polish 与 Technical-simplicity 冲突
- Implication：L3R1 必须**诚实承认无法同时全满足三项**，并用**候选方案的差异**来呈现取舍 —— 不同候选 lean 不同组合：
  - 候选 A 可以 lean "Speed + Differentiation"（快 + 独特，但 UX 粗糙）
  - 候选 B 可以 lean "Differentiation + Polish"（独特 + 打磨，但时间长）
  - 候选 C 可以 lean "Speed + Polish"（快 + 好看，但内核与现有产品相似度高）
- **不允许的候选**：任何声称"三个都满足"的候选 —— 这是 L3R1 必须识别并拒绝的"空头支票"

---

## Block 7 — Freeform

- ✅ **无**
- 无额外 context，L3R1 基于 L2 report + 上面 7 个 block 推进

---

## Summary for debaters

### 硬约束（✅）—— MUST honor in every candidate

1. **双 persona，PI 优先**：v0.1 必须同时服务 PI（buyer）+ senior PhD/postdoc（operator），但产品重心以 PI 为先；Carol 类型（onboarding）降级为 v0.2
2. **15-30h / 周投入**：时间估算基于 ~20h/周；超出必须显式 flag
3. **v0.1 先免费，预留 auth 但不做 billing**：不做让付费层不可能的早期决策
4. **L2 §6 的 6 条 conditions 全部继承**（data portability 承诺 / digest-first homepage / hybrid taste learning / 可剪枝低价值留痕 / buyer+operator 双层 / delegation 假设要 validate）

### 软偏好（✅ 但可商量）

1. **Web-first**（没强硬约束，模型可在候选中用 Web / Web+API / Web+desktop-companion 等组合）
2. **时间由 scope 驱动**（不是相反）

### ❓ 未知项（模型须在 §4 主动给 options）

1. **Target delivery 时长**：L3R1 须为每个候选给出诚实的 wk/mo 估算
2. **Red lines**：模型提 3 条候选，human 在 L3 menu 里选/改

### ⚠️ 三角冲突 flag

- Priorities 选了 Speed + Differentiation + Polish 三个 —— 必须通过**候选之间的取舍**来呈现，不允许"三个都满足"的候选

### 红线（候选须遵守，模型提议待 human 确认）

- 见 Block 5（3 条候选 red lines 在 L3R1 §5 给出）
- L2 §5 的 8 条 "natural limits" 作为边界参考，不全是 v0.1 red line，但候选必须在限制内
