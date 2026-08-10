# Forge v9 · 006 · P1 · GPT55xHigh · 独立审阅(no search)

**Timestamp**: 2026-08-09T14:38:34Z  
**Searches used**: NONE in this round.  
**Visibility**: I did NOT read other reviewer's P1.  
**Reviewer stance**: 审阅人——评判已存在物，不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- **已读**：`forge-config.md` 与完整 `_x-batch-snapshot.md`；XenoDev worktree backlog 的 KG-B11、XD-41、XD-43、XD-44 四段；`HANDBACK-LOG.md` 第 40/41/42 条；`SHARED-CONTRACT.md` §6 B-4-IDS；`handback-review.md` Step 2、Step 4.2/4.3；forge v8 的 Verdict、Intake、underweights 与 v9 触发提示；根 `CLAUDE.md` 的 Iron rules、跨仓与 Prohibited。`moderator-notes.md` 不存在，属正常。**skipped：无**。
- **独立真核 Part 1.3**：worktree 的 `real-review/` 最晚确为 v0.6；`REVIEW-LOG.md` 仍是 `2026-07-26T00:10:51Z / approve / 0`；`git ls-files` 显示 immutable 目录受追踪、草稿 `review-log/` 无记录。故 v0.7/v0.8 的“两者皆无”成立，不能由 singleton-only 解释；但这只证明写入步骤未发生，尚未定位究竟哪个调用入口失效。
- **K（用户判准）**：目标是“可靠的、自动化程度最高”，本轮更具体要求“要 enforcement，不要又一条建议”“先判故障态再定修法”，并要求判出“该带而未带”而非粗暴“未带就拒”；四条批次 KG-B11 / XD-41 / XD-43 / XD-44、五条 operator 关切与四条硬约束均作为判尺。阅读上以工程纪律为主，沿“义务何时产生—门是否执行—证据是否绑定—consumer 如何拒绝”追链，再看架构与安全。

## 1. 现状摘要（按 Y 视角）

### 工程纪律（主）

现行系统并非没有机制：R-Q7 有双写 lib 与 anti-pattern，task-preflight 有 fail-closed runner，B-4-IDS 有七字段契约，codex-review 有四轮 hard-stop。但实际入口可以不调用 runner、不写任何 review record、不携带父块；consumer 又以父块是否存在决定是否校验。第 40 条路由 forge 后，第 42 条原样复发，形成两包、16 轮、零 immutable、stale singleton 的实测链。替代评审六批均可在 `needs-attention` 下合入，恢复 codex 后累积区间发现 21 条、其中 11 high。

### 架构设计

协议把“证据存在后的字段合法性”建模得较细，却没有先建模“哪类工作流在何时产生一项不可逃逸的评审义务”。因此缺父键同时充当“不适用”和“逃避校验”两种状态。通用层可以是由权威工作流状态预先生成、绑定 task/spec 与内容身份的 obligation；证据只能关闭 obligation，不能反过来决定 obligation 是否存在。但各入口仍须逐点接线到该共同语义：通用机制无法自动发现任意未调用步骤。

### 安全

主要风险不是空证据，而是 v0.6 `approve/0` 被当成当前结论的错误正信号。SHA 只能证明“某文件未变”，不能证明“本次评审跑过且审的是当前内容”；singleton 的“合法可绑”又留下 stale/replay 面。B-4-IDS 的 shallow consumer 是跨仓可达性限制，不等于可以用证据自身的缺席判定不适用。

## 2. First-take 评分

| 批次 | 倾向 | 工程纪律 · 架构 · 安全理由 |
|---|---|---|
| **KG-B11 · medium→阻断链一部分** | **refactor** | 保留历史 singleton-only 缺陷，但拆开“旧路径写法不对”与“v0.7/v0.8 整步未执行”。只让 spec-writer source lib 会制造假完成感；本次主因应按未调用态处理。 |
| **XD-41 · high** | **new** | fallback 目前是事实放行而非等强 gate；需要机器可见的补审债与恢复后的累积区间清偿条件。`needs-attention` 不能继续等价于通过。 |
| **XD-43 · high** | **refactor** | runner 与 fail-closed 解析器可保留，必须把调用接到权威起跑/交付闸点，并以当前 task/spec 内容身份判断成功记录是否适用；否则仍是“装了门但可绕行”。 |
| **XD-44 · medium** | **refactor** | 四轮不应是无差别质量上限，但“finding 语义重复”在非结构化文本下也不能单独机器执法。先保留有界 hard-stop，增加风险/协议类分档与结构化 finding 类别。5 与 11 是两个独立收敛实例；可合计为 16 轮成本与 stale 跨度，不应伪装成一次连续 review。 |
| **§993 post-P0 backlog** | **new（本轮接手）** | 2026-05-31 已登记且 v5-v8 未接；它正是本批的 consumer 侧根。应显式区分 producer-full / consumer-shallow，并裁掉 shipped evidence 绑定 singleton 的正当性；改 spine 时须 bump contract_version + Changelog。 |

“该带而未带”的通用判据不是看块在不在，而是看**预先存在的 obligation**：由包类型、生命周期事件及上游 task/risk 状态在评审前决定是否必需；老包/非 build-ship 包没有 obligation，合法通过；有 obligation 而无内容绑定的完成证据才拒绝。此抽象可合并三类缺席语义，但每条 workflow 的创建点与消费闸仍必须接线，不能靠一条文案替代。

## 3. 我现在最不确定的 3 件事

1. **漏调位置**：真核排除了“仅 singleton-only”对两次事件的解释，却未排出是 spec-writer、codex-review 收尾、hand-back producer 还是编排入口漏调；P2/P3 前不应把“未调用”进一步冒充为已定位根因。
2. **obligation 的权威来源与兼容边界**：若包类型仍由 producer 自报，攻击者可连类型一起省略；若 consumer 从 HANDOFF/task 状态推导，又要处理旧包与 spec-only amendment。需要验证最小、不可自我豁免的来源。
3. **回声室自检——本结论尚未落成 consensus，也不能因无人反对而通过。** 我没有读取对方 P1；因此“无反对”在此不存在。本文已实质处理三个反命题：strict missing→reject 会误拒合法包，KG-B11 单因说与现场矛盾，纯语义重复判据难机器落地；不是 merely noted。但 exact caller 与 obligation 来源仍未被 addressed，故 verdict 只能是 **CONCERNS**。在对方与 chair 给出 reasoned explanation 前，任何把本 P1 当共同结论的动作本身都会落进“缺席即豁免”。
