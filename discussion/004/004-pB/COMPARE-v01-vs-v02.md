# PRD v01 vs v2.0 · 协议根因修复对比

**目的**: 同一 fork (004-pB), 同一 source candidate (B 决策账本), 用旧 vs 新 scope-protocol 各跑一次, 看新协议产生的实际结构差异。

**生成时间**: 2026-04-29
**协议变更 commits**: 76ee06c (skill) + 4071a23 (fork.md) + c1b5686 (spec-writer) on `chore/scope-protocol-split-roadmap`

---

## TL;DR — 三个最重要的差异

1. **§5 Scope OUT 从 18 项 → 6 项**, v0.5+/v1.0+/v1.5+ 阶段规划全部从 §5 移走
2. **新增 §6 Phased roadmap (12 项, 全部 committed)**, 含 phase 标签 / 难度 / 重要度 / **L2 §4 风险编号映射** / v0.1 已留位
3. **下游 architecture / spec 解读完全反转** — v01 让 L4 把 v0.2+ 当"非目标"(不留扩展点), v2.0 让 L4 把 v0.2+ 当"committed 工作"(必须留扩展点)

---

## 1. 顶层结构对比

| 节 | v01 | v2.0 |
|---|---|---|
| §1 Problem / Context | ✅ 同 | ✅ 同 |
| §2 Users | ✅ 同 | ✅ 同 |
| §3 Core user stories | ✅ 同 (5 条) | ✅ 同 (5 条) |
| §4 Scope IN | ✅ 同 | ✅ 同 |
| **§5 Scope OUT** | "明确非目标" — 含 v0.5+ / v1.0+ / v1.5+ / 永远不做 (4 子节, 18 项) | **"永远不做 — red-line / 永久排除"** — 仅红线 (6 项) |
| **§6** | Success | **Phased roadmap (committed, 按阶段交付)** ⬅️ 新增 |
| §7 (旧) → §8 (新) | Real-world constraints | (顺移) |
| §8 (旧) → 删除 | "Red lines" 单列一节 | (合并入 §5) |
| §10 Maintenance hint | ❌ 缺失 | ✅ 加入 (告知如何持续演进 PRD) |

**关键变化**: 旧 §5 是混合篮 (18 项), 旧 §8 是纯红线 (重复内容). 新版把"红线"和"分阶段交付"明确分开为**两个独立节**。

---

## 2. §5 Scope OUT 的核心差异 — 哪些项被移走?

### v01 §5 内容 (18 项, 4 子节)

```
v0.5+ (下一版再说) — 5 项
├── ❌ 事件日历 / FOMC 预警 (可 v0.2+ 加, 或 fork C)
├── ❌ 私有模型真实训练 (v0.1 只有占位接口)
├── ❌ 多市场 cross-signal (v1.0+)
├── ❌ 音频 / 视频解析 (v0.2+, 接口占位)
└── ❌ 自动抓取 (v0.2+, v0.1 可接受 human 粘贴或半自动 Proxyman fetch)

v1.0+ — 2 项
├── ❌ 配偶可见度模块
└── ❌ 回测环境

v1.5+ — 1 项
└── ❌ 半自动执行 (永远红线上限)  [注: 这条标签内部矛盾 — 既是 v1.5 又是红线]

永远不做 (红线级别) — 4 项
├── ❌ 自动下单
├── ❌ 期权 / 加密 / 高杠杆 / 日内
├── ❌ 商业化 / 付费层 / 多用户
└── ❌ 广谱 research terminal 功能
```

**问题**: 4 个子节都用 ❌ 红叉, **同一视觉权重**。reader (含 L4 spec-writer agent) 没有元信号区分 "永远不做" vs "v0.2 之后做". 容易把 v0.2+ 的功能也当成"永久非目标", 导致 v0.1 architecture 不留扩展点 → v0.2 启动时全栈重写.

### v2.0 §5 内容 (6 项, 单一节)

```
Scope OUT (永远不做 — red-line / 永久排除) — 6 项
├── ❌ 自动下单 (红线 #1)
├── ❌ 期权 / 加密 / 高杠杆 / 日内 (红线 #2)
├── ❌ 隐藏式默认推荐 (红线 #9 — 三列冲突报告永远不能合并)
├── ❌ "不动 / 等待"被建模为失败 (红线 #10)
├── ❌ 决策档案静默"建议你高频" (红线 #5 / Barber-Odean 铁律)
└── ❌ 跳过白话解释的"快速模式" (红线 #3)
```

**改进**: 每条都有 **"Why invariant"** 说明 (项目身份冲突 / 红线 / 法律). 不再有 "v1.5+ 半自动执行" 这种内部矛盾的标签 (v1.5+ 暗示"将来做", 但红线又说"永远不做").

### 两版 §5 的项目去向追踪

| v01 §5 中的项 | v2.0 中去向 |
|---|---|
| 事件日历 / FOMC 预警 | ✅ §6 Phase v0.5 (committed, 难度 M / 重要度 H, 风险 R-v0.5-3) |
| 私有模型真实训练 | ✅ §6 Phase v0.2.3 详细 (committed, 难度 H / 重要度 H, 风险 R-v0.2-3) |
| 多市场 cross-signal | ✅ §6 Phase v0.5 (committed, 难度 H / 重要度 M, 风险 R-v0.5-2) |
| 音频 / 视频解析 | ✅ §6 Phase v0.2.2 详细 (与"自动化咨询师监控"耦合, 风险 R-v0.2-2) |
| 自动抓取 | ✅ §6 Phase v0.2.2 详细 (同上) |
| 配偶可见度模块 | ✅ §6 Phase v1.0 (committed, 难度 L / 重要度 M, 风险 R-v1.0-2) |
| 回测环境 | ✅ §6 Phase v1.0 (合并入 "私有模型 v2+", 风险 R-v1.0-1) |
| 半自动执行 | ✅ §6 Phase v1.5+ (committed, 难度 H / 重要度 L, 风险 R-v1.5-1) — 明确"红线 #1 永远不破"指的是不破"自动下单", 而非不做"一键填表助手" |
| 自动下单 | ✅ §5 (留, 红线) |
| 期权 / 加密 / 高杠杆 / 日内 | ✅ §5 (留, 红线) |
| 商业化 / 付费层 / 多用户 | ✅ 隐含在 C3 (intake constraint), §5 不再重复 |
| 广谱 research terminal | ❌ 删除 (是"反对其他 candidate"的 Scope IN, 不属于 B 自己的红线; 旧 PRD 写在这里是误归类) |

**新增 §5 (v01 缺失的红线)**:
- 隐藏式默认推荐 (红线 #9) — v01 没列, 但是 B 的核心反向定义
- "不动 / 等待"被建模为失败 (红线 #10) — 同上, B 的核心反向定义
- 决策档案静默"建议你高频" — 同上
- 跳过白话解释的"快速模式" — 同上

---

## 3. §6 Phased roadmap — 全新章节, v01 无对应

### v2.0 §6 内容 (12 项)

#### v0.2 (NEXT, 详细描述, 3 项)

每项都含: **做什么 / 完成标准 / v0.1 已留位**

1. **个人金融笔记 wiki 升级** — 难度 L / 重要度 M / 风险 R-v0.2-1
   - v0.1 已留位: `concept_first_seen_at` 字段
2. **自动化咨询师监控** — 难度 H / 重要度 H / 风险 R-v0.2-2
   - v0.1 已留位: `AdvisorContentInput` 接口已抽象 source / format / fetcher 三层 + format enum 含 audio/video
3. **简单的私有模型 v1 (XGBoost + 技术指标)** — 难度 H / 重要度 H / 风险 R-v0.2-3
   - v0.1 已留位: 冲突报告 UI 已有"私有模型"列 + `PrivateSignal` 接口

#### v0.5 (3-9 个月, 一行概要, 3 项)

每项含: 难度 / 重要度 / **L2 §4 风险编号** / v0.2 ship 后细化

#### v1.0 (9-18 个月, 一行概要, 3 项)

#### v1.5+ (长期, 一行概要, 2 项)

### v01 缺失的关键元素

| 元素 | v01 | v2.0 |
|---|---|---|
| Phase 标签 (v0.2/v0.5/v1.0/v1.5+) | ❌ 部分有 (子节标题), 但项级缺失 | ✅ 每项都有 |
| 难度标签 (L/M/H) | ❌ | ✅ 每项都有 |
| 重要度标签 (L/M/H) | ❌ | ✅ 每项都有 |
| L2 §4 风险编号映射 | ❌ | ✅ 每项都有 |
| v0.2 详细描述 (做什么/完成标准/v0.1 已留位) | ❌ | ✅ 3 项 v0.2 都有 |
| Maintenance hint (PRD 如何持续演进) | ❌ | ✅ §6 顶部 |

---

## 4. 下游影响 (L4 spec-writer 解读差异)

### v01 让 spec-writer 怎么做?

v01 §5 列了 "v0.5+ 私有模型真实训练", 标 ❌. spec-writer 协议旧版本会把这条写到 `non-goals.md`, 提示 "v0.1 不做". 但因为没有 phase 标签和 v0.1 已留位指引, spec-writer 自然倾向于:

- ❌ 不在 architecture.md 写"私有模型预留接口" — 因为 §5 标 ❌, 像永久不做
- ❌ 不在 spec.md 写"需要 PrivateSignal IDL" — 因为没人提示要留口
- 结果: v0.2 启动时发现 v0.1 没接口, 需要全栈重写

### v2.0 让 spec-writer 怎么做?

v2.0 把同一项移到 §6.v0.2.3, 标注 "v0.1 已留位: 冲突报告 UI 已有'私有模型'列 + `PrivateSignal` 接口"。spec-writer 新协议 (c1b5686) 强制:

- ✅ architecture.md 必含 "Phased roadmap extension points" 节, traceability 表 phase / item / v0.1 extension point
- ✅ spec.md §2.3 加 "Phased roadmap extension points" 表, 列每个 phase item 在 v0.1 留的 extension point
- ✅ non-goals.md 严禁把 §6 项写进去 (协议明确警告)
- 结果: v0.2 启动时发现 v0.1 已有 `PrivateSignal` 接口, 替换占位实现即可, 不用重写

### 两个截然相反的架构哲学

| 节 | 性质 | v0.1 architecture 应该 |
|---|---|---|
| §5 Scope OUT | 永久不变量 | **不留扩展点** (留了会引诱人去做) |
| §6 Phased roadmap | committed 承诺序列 | **必须留扩展点** (v0.2+ 启动时不重写) |

v01 把两类项混在 §5, 让 L4 reader 没法区分应该留还是不留扩展点 → 走样默认值是"不留" → v0.2 启动时受罪.

---

## 5. v01 内部矛盾 (新协议消除)

### 矛盾 1: "半自动执行" 既是 v1.5+ 又是红线
- v01 §5 子节 "v1.5+" 写 "❌ 半自动执行 (永远红线上限)"
- 问题: v1.5+ 暗示"将来做", "红线"又说"永远不做"
- v2.0 修复: §6 Phase v1.5+ 写 "半自动化执行 (一键确认 + human 必拍板) — 红线 #1 永远不破". 明确"自动下单"是红线, "一键填表" 不是红线但是 v1.5+ 才做.

### 矛盾 2: "广谱 research terminal" 出现在 B 的 Scope OUT
- v01 §5 子节 "永远不做" 写 "❌ 广谱 research terminal 功能 (是 Candidate A 的 feature, 不在 B 的主场)"
- 问题: 这是 candidate 之间的差异, 不是 B 自己的"永远不做". B 没拒绝 research terminal, 只是没选这个赛道.
- v2.0 修复: 直接删除. 不在 PRD 里写"反对其他 candidate"的项.

### 矛盾 3: 配偶可见度 v01 标 v1.0+ ❌, v2.0 §6 同样列 v1.0
- v01 标 ❌ → 让 L4 当永不做
- v2.0 标 committed → 让 L4 在 v0.1 architecture 留 "share-token" 接口的扩展点 (decision_archive 表加 visibility 字段, v0.1 default=private, v1.0 加 partner-readable 选项)
- 同一现实需求, 协议解读完全反转

---

## 6. 哪些没变?

值得明确说**不**变的部分, 防止误解为"全部翻新":

- §1 Problem / Context — 完全相同 (问题没变)
- §2 Users — 完全相同 (人没变)
- §3 Core user stories — 5 条全部相同 (核心 loop 没变)
- §4 Scope IN — 完全相同 (v0.1 要做的没变)
- §7 Success outcomes — O1-O8 大致相同 (略有合并, 实质不变)
- §8 Real-world constraints — 完全相同 (来自 intake)
- §9 UX principles — 完全相同 (tradeoff stances 没变)
- §10 Biggest risk — 完全相同 (Upkeep 负担)

**核心结论**: 协议根因修复**不改变 PRD 内容**, 只**重组 PRD 结构**, 让下游 L4 能正确区分 "永远不做" vs "committed 序列, 按阶段交付".

---

## 7. 这次重跑过程中 synthesizer 的实际发现

(摘自 scope-synthesizer agent 重跑 L3 时的报告)

- 旧 v01 stage doc "Scope OUT" 在三个 candidate 共有 **~21 项**被错归类的 phased item, 新版重新归位 phased roadmap
- 单 candidate B 8 项: 笔记 wiki 升级 / 自动化咨询师监控 / 私有模型 v1 / pre-post-mortem 深化 / 多市场 / 事件日历 / 模型 tutor / paper trading
- 1 项不能 cleanly classify: 多模态 (视频/音频) — 归为 phased v0.2 与"自动化咨询师监控"耦合, 但 architecture 必须在 v0.1 留 `AdvisorContentInput` IDL audio/video format enum
- 新菜单每个 phased item 都引用回 L2 §4 的 1-3 个风险编号 (R-v0.2-1 等), 让下游能直接看到"为什么这一项必须做 + 它防的是什么"

---

## 8. v0.1 已 ship — 这次对比的实际意义

**v0.1 已经按 v01 PRD 实现并 ship 于 2026-04-27** (`projects/004-pB/docs/v0.1-ship-summary.md`), 所以这份对比不会触发 architecture 重写。但它对未来仍有价值:

1. **v0.2 启动时**: spec-writer 用新协议读 v2.0 PRD §6.v0.2.1/2/3, 能直接看到"v0.1 已留位 (实测)"指引, 知道哪些扩展点已存在 / 哪些需要在 v0.2 spec 里补上
2. **下个 fork**: 任何新 fork (例: 004-pA / 004-pC / 005-pX) 都会用新协议, 不会再走 v01 老路
3. **协议 acceptance test**: 这次重跑本身就是对新协议的 acceptance — 在面对**旧素材** (round files 是旧协议生成的) 的情况下, 新协议 + scope-synthesizer 仍能正确拆分
4. **历史对照**: 任何看 PRD_v01.md 的人都能通过本文档理解"这是旧协议产物, 新协议下 §5/§6 拆分后实质内容 mapping 见此"

## 9. PRD v2.0 二轮硬化 (2026-04-29)

v2.0 第一稿生成后, 自审发现 5 处质量短板, 修了 3 处高优先项 (commits 同批次):

| # | 问题 | 修复 |
|---|---|---|
| ✅ | v0.1 ship 状态 PRD 完全不见 (通篇未来时态) | 加 §0 "Current state" banner, §7/§10 Outcome 标 ✅/⏳ 状态 |
| ✅ | §6 "v0.1 已留位"是推测不是事实 (grep 实测发现 4/6 项是撒谎) | 改为"v0.1 已留位 (实测)", 每条标 ✅ 已有 / ⚠️ 未留 / 🔧 v0.2 工作量 |
| ✅ | §11 "30 秒录入 acceptance test" 已 close 但仍 open | 拆 Open / Closed 两节, 30s 移入 Closed (附 spec.md / SLA.md 引用) |
| ⏸ | §6 phase 内排序没有可见信号 | 暂不动, 等 v0.2 ship 后维护 |
| ⏸ | §4 "全部 Candidate A 的 IN" 引用模糊 | 暂不动, 优先级低 |

**实测 #2 的关键发现** (修 PRD §6 时一并核出):

| PRD §6 v01 暗示 v0.1 已留位 | 实际 v0.1 代码 | 真相 |
|---|---|---|
| `concept_first_seen_at` 字段 | 不存在 (只有简单 Note) | 撒谎 — v0.2 需扩 schema |
| `AdvisorContentInput` 三层抽象 + audio/video enum | 只有单一 `AdvisorParser`, 无 enum | 撒谎 — v0.2 需大重构 |
| `PrivateSignal` 接口 | 存在 (`StrategyModule` + `StrategySignal`) | **真** — 唯一真做对的扩展点 |
| 配偶可见度"升级成本低" | 无 visibility/partner/share 字段 | 撒谎 — v1.0 需扩 schema |
| 30s SLA verification | spec.md C11 + SLA.md §1.4 + E2E test | **真** — 已 ship |

**协议层启示**: 即使 fork 模板(已修)说"§6 必须列 v0.1 已留位",**没有任何东西强制核对真假**。L4 启动 v0.2 前必须先 grep 实测扩展点,否则 PRD 把"v0.2 工作量"低估几倍。这条经验应该回写到 spec-writer.md (architecture.md "Phased roadmap extension points" 节加 "实测核对" 强 instruction) — 后续 protocol 演进 backlog.
