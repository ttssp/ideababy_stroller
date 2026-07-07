# L3R0 Intake · 001-radar

**Captured**: 2026-07-06
**Target**: 001-radar（Topic Cartographer / KG-radar · Paper Radar agent）
**Captured by**: operator via /scope-start AskUserQuestion intake
**Note**: operator 本人即目标用户（AI lab 负责人 / research lead），故 L2 §7 的三个关键待决问题（决策仪式 / payload 形态 / topic 数）直接在 intake 里由 operator 回答，不留给 L3R1 模型猜。

---

## Block 1 · 时间 + 工时

- ✅ **v0.1 时间盒**：2-3 个月（完整产品）
- ✅ **周工时**：15-30 小时（认真投入）
- 💡 **推导预算**：约 130-360 小时（10-12 周 × 15-30h）。scope 须落在这个区间内；L3R1 若判定某候选超预算，必须诚实标出，不许偷偷砍窄。

## Block 2 · 用户 + 决策仪式

- ✅ **目标用户**：AI lab 负责人 / research lead（operator 本人）—— 对多个 topic 负有"这方向还值不值得下注"判断责任的 senior。**不是**泛 researcher，**不是**领域新人（L2 已把新人划为另一物种）。
- ✅ **v0.1 锚定的决策仪式**：**开新方向评估（冷启动）** —— L2 场景四。评估一个**还没进 topic 列表**的新方向是否值得投入：现场冷启动一张新地图，看这方向结构上成没成型（相关 work 是分散爆发还是已形成稳定问题簇 + 方法簇）。
  - 💡 **为什么这个选择重要**：operator 没选频次最高的"组会精读"，而选了痛感最高、且**直接命中原提案内核**（"给一个新工作，若无对应 topic 则新建并主动搜索补齐"）的冷启动评估。这把 L2 §7-Q6（冷启动是否列一等公民动作）直接答成了 **YES —— 冷启动就是 v0.1 的核心动作**，不是边缘 case。
  - 💡 **对 scope 的直接影响**：这意味着 v0.1 的重心不在"维护 8-15 张长期地图看位移"，而在"**对任意给定新方向，快速冷启动一张地图 + 给出结构成型度判断**"。位移（时间 diff）在冷启动语境里可能退居其次——因为一个刚冷启动的新方向本来就没有"旧地图"可 diff。⚠️ 这是 L3R1 必须正面处理的张力：**冷启动评估 vs 位移 diff 的主次关系**（见下 §unknowns）。

## Block 3 · 商业模式

- ❓ **未问 / 未定**（intake 批次未覆盖 · operator 未主动提）→ L3R1 提选项。默认推断：个人自用工具起步（operator 即用户），商业化非 v0.1 关切。L3R1 可提"自用 → 可能开源 → 可能小 SaaS"三档，但不应让它绑架 scope。

## Block 4 · 平台

- ❓ **未定** → L3R1 提选项。L2 未锁平台。合理候选：CLI/terminal（agent pipeline 最自然）、Web（图/briefing 展示面）、API-only（作为 research-agent 底座）。⚠️ L3 是产品层，平台的技术取舍留 L4，但 L3R1 可就"operator 打开它的地方"提产品级形态选项。

## Block 5 · 红线（scope OUT）

- ✅ **operator 明确红线**：**不追全覆盖**（不把 arxiv 全量塞进图 · 选择性中心度才是价值 · L2 natural limit）。
- 💡 **模型补提**（L3R1 从 L2 natural limits 提，operator fork 时审）：候选红线包括
  - 不做问答/报告生成器（避开 Elicit/Undermind/OpenScholar 占据的 synthesis 面）
  - 不做每日简报/feed（不退回 001-pA 那种 push 流 · ⚠ 但 map-region alert 是否算例外须 L3R1 裁）
  - 不做"真理机"（contradicts/supersedes 是判断非事实 · 不确定性必须外显）
  - 不面向领域新人（位移/成型度判断的前提是用户已有领域判断力）

## Block 6 · 优先级 tradeoff

- ❓ **未单独问** → L3R1 从已知约束推断。可推断的隐含优先级：
  - **差异化 > 广度**（红线"不追全覆盖" + L2 护城河脆弱性 → 差异化是生死线）
  - **可验证性**（operator 自用 · 冷启动评估的判断准不准是核心 · 信任机制 L2 §7-Q3）
  - L3R1 若发现 tradeoff 冲突（如"briefing 品质" vs "冷启动速度"），须显式列出让 operator 裁。

## Block 7 · payload 形态（L2 §7-Q2 · 最大待决项，operator 已答）

- ✅ **v0.1 payload = briefing 为主 + diff/图作证据展开**。首屏给 agent 的**判断**（这方向结构上成没成型、该不该投 + 理由），想核验时点开看底层的快照 diff / 图。
  - 💡 **这答对了 L2 点出的张力**：L2 指出"位移叙事本质是一句 briefing 不是一张图"，R1 的"以图为主"默认被 operator 显式推翻。产品重心落在**叙事/判断**，图/diff 降为**证据支撑层**（可展开、可核验，但不是首屏主体）。
  - 💡 **对 novelty 落点的影响**：这让 KG-radar 更远离 Litmaps/ResearchRabbit（图为主）、更靠近"有品味的 agent 给判断"——正好落在 L2 §6 条件二说的护城河交集上（agent 品味校准 × 决策语境），避开了"又一张漂亮 paper map"的死法。

## Block 8 · topic 数 + 单人/共享（L2 §7-Q4/Q5 · operator 已答）

- ✅ **8-15 topic + 单人版**。直接做到 operator lab 的完整覆盖面，但只做单人（私人判断外骨骼），不做 lab 共享。
  - ⚠️ **L3R1 须核对的张力**：Block 1 预算 130-360h vs "8-15 topic 完整覆盖 + 冷启动能力 + briefing 生成 + diff/图证据层"——这个 scope 在 2-3 月内可能偏满。L3R1 应诚实评估，必要时给"先 3 topic 验证 → 再扩到 8-15"的分期候选，而不是硬塞。（注意与 operator 明确选的"8-15"存在潜在冲突，L3R1 要把这个 tradeoff 摆到台面上，不许静默砍窄。）

---

## Summary for debaters（L3R1 必读）

### ✅ Hard constraints（不可违背）
1. 时间盒 2-3 月 · 周工时 15-30h · 预算约 130-360h
2. 目标用户 = AI lab 负责人/research lead（operator 本人）· 非泛 researcher · 非新人
3. **决策仪式 = 开新方向评估（冷启动）** —— v0.1 核心动作，冷启动一张新 topic 地图 + 判断结构成型度
4. **payload = briefing 为主（判断+证据）+ diff/图作可展开的证据层**，非"以图为主"
5. 规模 = 8-15 topic + 单人版
6. 红线 = 不追全覆盖

### 🤔 Soft preferences（可调，标出理由即可）
- 隐含优先级：差异化 > 广度；可验证性高
- topic 数 8-15 是 operator 期望值，但与预算有张力 → 允许分期候选，但须显式列 tradeoff

### ❓ Unknowns（L3R1 必须提具体选项，不许留空）
1. 商业模式（默认自用起步）
2. 平台形态（CLI / Web / API-only —— 产品级形态选项，技术留 L4）
3. 优先级 tradeoff 的显式排序（从约束推断 + 让 operator 裁冲突）
4. **冷启动评估 vs 位移 diff 的主次**（v0.1 锚冷启动，但原 idea 核心卖点是位移——两者在"新方向本无旧地图可 diff"处冲突，L3R1 必须裁）
5. map-region alert 是否算"不做 feed"红线的例外（L2 §7-Q7）
6. 信任建立机制（L2 §7-Q3 · briefing 给判断 → 判断错了怎么让用户不弃用 · v0.1 要不要内建"可核验/可回溯"设计）

### 🚩 Red lines（operator 定 + 模型补提待审）
- ✅ 硬红线：不追全覆盖
- 💡 待审：不做问答/报告生成器 · 不做每日简报/feed（map-region alert 待裁）· 不做真理机 · 不面向新人

### 关键 tradeoff 轴（L3R1 候选应沿此展开）
**"冷启动评估深度" vs "topic 覆盖广度" vs "位移 diff 完整度"** —— 在 130-360h 预算里，这三者不可能同时拉满。候选 A/B/C 应是这个三角里的不同取舍点（如：A=窄 topic 深冷启动+强 briefing / B=广覆盖但位移简化 / C=先位移 diff 后冷启动）。
