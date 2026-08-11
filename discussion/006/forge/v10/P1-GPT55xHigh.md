# Forge v10 · 006 · P1 · GPT55xHigh · 独立审阅(no search)

**Timestamp**: 2026-08-11T05:06:29Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read `P1-Opus47Max.md`.
**Reviewer stance**: 审阅人——评判已存在物，不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了：`forge-config.md` 全文；`_x-batch-snapshot.md` 与 `FORGE-006-v10-PENDING.md` 全文；obligation `README.md` 全文及 ledger 全 13 行；validator 的 check-7/check-8/主入口全文；`SHARED-CONTRACT.md:800-820,1298`；hook 治理全文；`CLAUDE.md:100-130`；v9 verdict 至 v10 触发判据；HANDBACK-LOG 第 44/45 条；XenoDev `.scan-credentials-ignore` 全文；forge protocol 与 `AGENTS.md` 全文。
- 我跳过的：`moderator-notes.md` 不存在；无不可达标的。外部白名单可读，确认当前 21 条及 24→21 留痕。按要求未读对方 P1，未扩张到簇 C/D。
- **K（用户判准）摘要**：用户要的是“**这根的结构性回答，不是八个个案的处置清单**”，并明确“**任何建议再加一个 warn 型 check……必须同时给出升级边由谁、在哪个 gate、凭什么触发**”；“人没做”已被排除，偏好通用机制但不接受虚构抽象。
- **阅读策略**：只用“架构设计”视角，沿“声明/规则 → 权威状态 → 强制消费点”核对每条链；优先寻找能推翻“多数只是 v9 未接线”的反例，不切换到纪律或安全视角。

## 1. 现状摘要（架构设计视角）

八条共享“文档节点存在、执行边缺席”的外形，但落在三种不同层次：XD-44′/XD-52/XD-47 缺 review 状态机的终态、持久计数与 `not-run` 信息；KG-B15 缺对合法 main checkpoint 与违规混线的语义分割；KG-B16—B19 缺跨仓 SSOT 完整性、可运行 fixture、声明权威划分及 worktree-aware 路径模型。

v9 ledger 已提供 `pending → satisfied|skipped` 与 `due_gate`，forge Phase 0 的一次 fail-closed 消费清掉了 74 天欠债；但最新态仍有 9/11 项 `consumer_wired:false`。check-7、check-8 与 worktree preflight 都以 warn 起步并写“复发 ≥2 次”，没有机器计数、升级 owner 或会消费该条件的 gate；validator 末端 `|| true` 还把未来脚本改成 hard-fail 与主入口真正阻断拆成两次改动。

## 2. First-take 评分（架构设计）

我**反对**“多数只是 v9 verdict 的未接线实例”。v9 控制面能防义务蒸发，适合承载 B16/B17 的同步与执行欠债，也可承载其他修复的交付；但它不能定义 review 如何终止、怎样证明真跑、谁拥有路径真值。把这些塞成接线计划会把“义务存在”误当成“机制语义完整”。

| 条目 | 倾向 | 理由与 warn 自查 |
|---|---|---|
| XD-44′ | **new** | 需要区别 `approved`、`exhausted-with-open-findings` 与 chair override 的可消费终态；不是加 warn，ship gate 直接消费终态并拒绝同形放行。 |
| XD-52 | **refactor** | 轮次真相应持久化并由每轮入口机械读取；不是 warn，review-entry gate 在分档上限处确定性阻断。 |
| XD-47 | **new** | 输出须携带可验证的 `ran/not-run` 与被读对象身份；不是 warn，缺运行证据由 review gate 判失败，不计有效轮次。 |
| KG-B15 | **refactor** | 先把合法 checkpoint 与跨 idea 混线分型，再由 commit gate 执行；现有“≥2 次”已失效，不再续一条 warn，规则定形后对违规类型硬拦。 |
| KG-B16 | **refactor** | v9 可承载 SSOT→mirror→MANIFEST 的交付义务，但“单侧即落地”还需完整性收据；新包由 handoff intake 阻断缺件，老包仅走具名 policy，不靠 warn。 |
| KG-B17 | **new** | validator 发布必须消费环境无关 fixture 的通过产物；不是记录“应跑”，producer/consumer 发布 gate 缺该产物即失败。 |
| KG-B18 | **cut** | `source_repo` 若是 consumer 已有权威值，不应继续让 producer 冗余自报；新包由 consumer 派生，历史字段只读兼容，不新增 warn 升级链。 |
| KG-B19 | **refactor** | 精确路径模型须先按 checkout 根归一，再实现模式类 ratchet；credential gate 拥有基线并阻断“新增未归类豁免”，不是等待人工累计 warn。 |

这些判断不需切换到工程纪律或安全视角：关键都在状态所有权、身份绑定与 gate 拓扑；Safety Floor 的强度不在本轮重裁。

## 3. 我现在最不确定的 3 件事

1. `exhausted-with-open-findings` 最终应永久禁止 ship，还是允许 operator-chair 按 finding 逐条签署；需要 P2 查可执行终止模型，而非寻找统一轮数。
2. `source_repo` 是否还承载“producer 当时所见目标”的审计价值；若有，应该改名为观察值并与 consumer 权威值分域，而非直接删除。
3. worktree 归一后，credential scan 对嵌套 checkout、未跟踪文件与 gitignored Safety Floor 命中的边界是否仍完备；这决定 KG-B19 是单一身份层修正还是两层扫描模型。
