# Open Questions — 004-pB · 决策账本

**Version**: 0.2
**Created**: 2026-04-25T15:35:00+08:00
**Updated**: 2026-04-25T19:30:00+08:00 (R2 surgical revision)
**Companion**: PRD §11 · spec.md §8

> 本文档记录 spec 阶段**未独立解决**, 需 human / operator 决定的问题。
> **每条 question 都给了 spec 当前默认假设** (避免 implementation 卡死),
> 但仍标 OPEN 等 human 确认或推翻。

## Revision History

| Version | 修订摘要 |
|---------|---------|
| 0.1 | 初稿 (Q1-Q10) |
| 0.2 (R2) | Q4 推后到 v1.0+ (M5: D18 删除); Q5 RESOLVED (H5: D9 锁死); 新增 Q11 (cache miss 例外审) |

---

## Q1. "稳定赚钱"的精确 benchmark 与时间尺度

**来源**: PRD §11.1 + L2R3-GPT §7.Q1

**问题**: PRD §6.O9 给了"跑赢标普 2-5%/年", 但**多少年算"稳定"**?

| 候选答案 | 含义 | 对 spec 影响 |
|---------|------|-------------|
| **6 个月** | 样本太小, 噪声主导 | 不推荐 |
| **12 个月 (一年滚动)** | 主流个人投资者评估周期; 仍噪声大 | review generator 输出年化对标; spec 默认假设 |
| **3 年** | 行业标准最低观察期 | v0.1 仅积累数据不出年化; 减少假精度 |
| **N/A (永远只看 proxy)** | 接受 alpha 不可在合理时间证伪; 仅看 calibration proxies (O3/O4) | 删除 O9 verification, 仅保留 north star 文字 |

**spec 默认假设 (暂用)**: **12 个月 (一年滚动窗口)**

**建议**: human 可以延后回答, 但回答 **影响 monthly review generator 设计**:
- 若 12 个月: review 含年化对标 + 12 个月窗口图
- 若 3 年: review 仅累积数据, 无对标
- 若 N/A: 完全删除对标章节

**Block 状态**: 不阻塞 v0.1 ship, 但阻塞 monthly review v1 实现 (Phase 2)

---

## Q2. 动机二选一

**来源**: PRD §11.2 + L2R3-GPT §7.Q6

**问题**: human 真想 "**成为会投资的人**" (需要持续摩擦 → B 更 fit) 还是 "**摆脱不知道该怎么办**的焦虑" (需要清晰出口 → A 更 fit)?

**对 spec 的影响**:
- **若前者**: 现在 spec 设计正确 (B fork)
- **若后者**: B 的 upkeep (录入 < 30s × 8 周) 撑不住, 应该已 fork 到 A; 本 spec 失效

**spec 默认假设**: **前者**, 通过 fork 选 B 隐含确认

**Block 状态**: 不阻塞 (已隐含确认), 但若 8 周自我观察显示 OP-3 风险 (停用), 需重审此问题

---

## Q3. 情绪承受预案 (两周冷静期机制)

**来源**: PRD §11.3 + L2R3-GPT §7.Q5

**问题**: 连续两次建议都亏钱, 是否需要明确 "两周冷静期" 机制 (系统暂停 push / 强制 review 才能继续)?

**对 spec 的影响**:
- **若需**:
  - schema 加 `cooling_off_period` 状态机
  - ReviewGenerator 增加"冷静期触发"逻辑
  - Telegram push 在冷静期内仅 review reminder, 不 event
  - +5-8h 实现成本
- **若不需**: 不实现, 进入 v0.2 待 8 周自我观察后决定

**spec 默认假设 (暂用)**: **不实现 v0.1, 进 v0.2**

**理由**: human 8 周内若未触发 (期望情况), 实现成本浪费; 若触发, v0.2 紧急加是合理路径

**Block 状态**: 不阻塞 v0.1

---

## Q4. **(R2 推后到 v1.0+)** 配偶可见度

**来源**: PRD §11.4 + L2R3-GPT Q10

**R2 修订背景 (M5)**: Codex R1 review 指出 v0.1 在 `ReviewGenerator` 接口预留
`audience: enum {self, partner}` 参数 (D18) 是**弱 scope leak** — PRD §11.4 把
配偶可见度明确放到 v1.0+, v0.1 接口层预留也算超出 v0.1 scope IN.

**R2 决断**: **D18 删除**, v0.1 不预留接口. partner audience 整体推后到 v1.0+ open
question, 由 human 与配偶外部对话后决定优先级再实现 (届时可能需要配偶可见度信息
过滤 + 隐私边界 + UX 二次设计, 不能在 v0.1 仅靠接口预留就能"轻量"完成).

**spec 影响**: `MonthlyReviewService.generate(month_id)` 签名移除 `audience`
参数. 仅 `self`. T015 修订已反映.

**Block 状态**: 推后到 v1.0+, 不阻塞 v0.1.

---

## Q5. **(R2 RESOLVED)** Proxyman 半自动 pipeline 的具体接入方式

**来源**: spec-writer 在 D9 选半自动路径后衍生

**R2 修订背景 (H5)**: Codex R1 指出 D9 锁了 "中等复杂度路径", 但接入方式仍
OPEN — 风险是 upkeep + build time 一起拉爆.

**R2 决断**: D9 锁死如下, **不再 OPEN**:
- watched folder = `~/decision_ledger/inbox/`
- 触发 = `scripts/proxyman_fetch.sh` shell wrapper, **human 手动调用** (Mac 可用 Alfred / Raycast 绑快捷键)
- 一次 fetch 单 PDF (主路径); 系统对 batch 也容错 (多文件依次处理)
- **fallback**: Web UI 提供 "贴 PDF / 文本" 按钮 (`/advisor/paste`) — backup, 不是主路径; 实现成本 ≤ 1h, 任何路径失败时 human 仍能 ingest

**spec 影响**: D9 已更新, T006 实现按此路径; spec.md §4 D9 删除 "暂用默认假设" 字样.

**Block 状态**: RESOLVED, 不再 OPEN.

---

## Q6. (新) 占位 PlaceholderModelStrategy 的具体规则

**来源**: spec-writer 在 §3.1 描述了 v0.1 三占位实现, 但 PlaceholderModelStrategy 的"极简规则"未具体化

**问题**: PlaceholderModelStrategy 对 ticker 给意见时, 用什么规则?

**候选**:
- (a) 持仓 < 板块平均 → 看多 (mean reversion 占位)
- (b) 持仓 > 板块平均 → 看空
- (c) 上周价格 / 本周价格 比较 (动量占位)
- (d) 完全随机 (反事实 baseline, ML PhD 友好)
- (e) 永远 confidence=0.0 / direction="no_view" (最 conservative, 让 advisor / agent_synthesis 主导)

**spec 默认假设 (暂用)**: **(e) 永远 no_view** (最低风险, 不假装"私有模型有意见", 真模型 v0.5+ 替换)

**留给 implementation 决定**, 可在 Phase 1 之后微调

**Block 状态**: 不阻塞

---

## Q7. (新) 学习检查 (季度) 的内容是 LLM 生成还是 human 手编?

**来源**: PRD §S4 / O4 / spec.md §6.O4 / §1 R7 红线

**问题**: 季度学习检查表 (≥ 7 条金融概念) 由谁产出?
- (a) LLM 从过去 90 天笔记 wiki 自动抽取概念列表 + 自动出题
- (b) human 自己手编一份 master checklist, 系统每季度展示填空

**spec 默认假设 (暂用)**: **(a) LLM 从笔记 wiki 抽取**, human 评分; LLM 输出题目 + 标准答案, human 写答案 + 自评是否 "懂"

**Block 状态**: 不阻塞 spec, 阻塞 Phase 3 学习检查实现

---

## Q8. (新) 错位矩阵的具体可视化与计算逻辑

**来源**: spec D16 选 HTML table; 但具体维度未指定

**问题**: 错位矩阵的轴是?
- 行 = 关注股 (ticker)? 列 = 咨询师方向?
- 还是按板块 (sector) 聚合?
- 加权方式 (持仓权重 × 咨询师 confidence)?

**spec 默认假设 (暂用)**:
```
行: 30-50 关注股 (ticker)
列: [咨询师方向, 占位模型方向, agent 综合方向, 当前持仓 %]
着色: 错位 (咨询师强推 vs 持仓 < 板块平均) = 黄色; 反向错位 = 红色
排序: 默认按错位强度降序
```

**留给 implementation Phase 1 微调**

**Block 状态**: 不阻塞 spec, 阻塞 Phase 1 矩阵任务

---

## Q9. (新) Onboarding 的 "≤ 15 分钟"具体步骤?

**来源**: PRD §6.O6 / SLA §1.4 / spec.md C12

**问题**: 首次 onboarding 包含哪些步骤?

**spec 默认假设 (暂用)** (15 分钟分解):
1. 启动系统 (`./scripts/start.sh`) — 1 分钟
2. 录入 30-50 关注股 (粘贴 CSV / 表单) — 5 分钟
3. 录入持仓快照 (粘贴 JSON / 表单) — 3 分钟
4. 把第一份咨询师 PDF 拖进 `~/decision_ledger/inbox/` — 1 分钟 (等待解析 ~30s)
5. 完成首次决策档案录入 (任意 ticker, action=hold/wait, reason="首次测试") — 30 秒
6. Telegram bot 注册 + chat_id 绑定 — 3 分钟
7. 看完笔记 wiki 空状态 / 学习检查空状态 → 完成 — 1.5 分钟

总计 **~15 分钟**, 留 buffer

**留给 implementation Phase 3 onboarding 任务微调**

**Block 状态**: 不阻塞 spec

---

## Q10. (新) v0.1 是否需要 git pre-commit hook 拦截敏感文件?

**来源**: SEC-2 / SEC-3 mitigation

**问题**: 是否在项目里配置 pre-commit hook 拦截 `.env`, `db.sqlite`, `inbox/*` 误 commit?

**spec 默认假设 (暂用)**: **是**, 用 `pre-commit` 库 + 自定义 hook

**Block 状态**: 不阻塞 spec, 列入 Phase 0 任务

---

## Q11. **(R2 新增)** Cache miss 时 draft 阶段 LLM 等待上限的可降级策略

**来源**: R2 修订引入 D21 (draft 阶段同步 LLM cache 命中常态 < 1s, miss 上限 10s);
若实际 ship 后 cache miss 率高, 是否需要降级.

**问题**: D21 给的 cache miss 上限 10s 是工程估算 (Sonnet 4.6 cold-start 约 5-8s,
三路并发 + rebuttal 约 8-10s p95). 若实际 ship 后 cache miss 率高 (新 ticker /
旧 advisor_week / Anthropic API p95 飙升), **是否需要降级**:
- (a) 缩短 prompt (减质换速)
- (b) 仅生成 ConflictReport, Rebuttal 推后 commit 后再补 (回到 v0.1 v0.1 的部分异步设计)
- (c) cache miss 时给 human 选项 "等 / 跳过冲突报告先 commit"

**spec 默认假设 (暂用)**: **不降级**, 接受 cache miss 时 5-10s 等待 (估测 < 5%
场景); 监控 `llm_usage` 表的 latency p95 + cache miss 率, 8 周后评估.

**ConflictCacheWarmer (T010 新增, R2)** 服务于让 cache 命中成为常态: AdvisorParser
完成后 enqueue 30-50 关注股 × (3 lane analyze + 1 assemble) 预生成. 周一次, 月成本
$2-4, 在预算内.

**Block 状态**: 不阻塞 v0.1, 监控数据驱动 v0.2 决策.

---

## 总结表 (R2 修订)

| # | 问题 | 默认假设 | 阻塞 | 何时确认 |
|---|------|---------|------|---------|
| Q1 | "稳定赚钱"时间尺度 | 12 个月 | Phase 2 (review) | spec freeze 前 |
| Q2 | 动机二选一 | "成为会投资" (隐含) | 不阻塞 | 8 周后 retro |
| Q3 | 冷静期机制 | 不实现 v0.1 | 不阻塞 | 8 周后 retro |
| Q4 | **配偶可见度 (R2 推后)** | **D18 删除, v0.1 不预留接口** | 不阻塞 | v1.0+ 评估 |
| Q5 | **Proxyman 接入 (R2 RESOLVED)** | **watched folder ~/decision_ledger/inbox/ + shell wrapper + Web 贴 PDF backup** | RESOLVED | — |
| Q6 | 占位模型规则 | no_view | 不阻塞 | Phase 1 implementation |
| Q7 | 学习检查内容 | LLM 抽取 (cut list 候选: 降级 human 手编) | Phase 3 | task-decomposer |
| Q8 | 错位矩阵维度 | 行 ticker / 列 三方向 | Phase 1 | task-decomposer |
| Q9 | Onboarding 步骤 | 15 分钟 7 步; **R2: step 7 解耦 T019** | 不阻塞 | Phase 3 |
| Q10 | pre-commit hook | 是 | 不阻塞 | Phase 0 |
| **Q11** | **Cache miss 降级 (R2 新增)** | **不降级, 接受 5-10s 等待 + 监控驱动 v0.2** | 不阻塞 | 8 周后 retro |

---

## Operator 决策路径建议 (R2 修订)

**spec freeze 前必答**: Q1 (影响 Phase 2 review 设计)

**Phase 1 启动前可答**: ~~Q5~~ (R2 RESOLVED) / Q6 / Q8 (影响 Phase 1 任务粒度)

**Phase 3 启动前可答**: Q7 / Q9

**8 周后 retro 评估**: Q2 / Q3 / **Q11** (影响 v0.2 是否继续 / 是否加冷静期 / 是否 cache 降级)

**v1.0+ 评估窗口**: Q4 (配偶视角是否 v1.0+ 实施, R2 推后)

---

## 自查 (spec-writer 提交前) — R2

- [x] 每个 question 标注 source + 默认假设 + 阻塞状态
- [x] PRD §11 的 4 条全部转入 (Q1-Q4)
- [x] spec 阶段新发现的问题 (Q5-Q11, R2 加 Q11) 都是工程级, 不是产品决策
- [x] 任何"new in spec" 的 prior decision 不放在这里 (放 spec.md §4)
- [x] **R2 修订**: Q4 推后到 v1.0+ (M5); Q5 RESOLVED (H5); 新增 Q11 (cache miss 降级评审, R2 D21 配套)
