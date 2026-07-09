# Forge v7 · 006 · P3R2 · Claude · 联合收敛 R2(finalize)

**Timestamp**: 2026-07-07T16:30:58Z
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: strong-converge(从 forge-config 读)
**Model note**: 本轮由 Claude(Fable 5)执笔,文件名沿用管线约定。

## 1. 我对每条分歧的最终立场 + 让步

- **分歧 1(挂起判死执行层 + companion 管辖权)**:
  - 对方论证:"目标态是 SKILL/config 声明阈值,companion 内建执行;当前可 SKILL 轮询过渡" → **接受**,与我 P2 的 k8s 声明/执行分离完全同构。
  - 我的最终立场:两段式落地——**现在**:判死阈值 + 轮询规则写进 codex-review SKILL 决策表(IDS 三层同步件,forge 直接决议);**目标态**:companion.mjs 内建 watchdog。companion.mjs 按现有证据属 XenoDev 侧 runtime(非 bootstrap-kit mirror 件),forge 不当场改,verdict 里写成「授权条目」经 hand-off/dogfood-backlog 传达给 XenoDev 实施。
  - 让步给对方的部分:采纳其「若属 XenoDev runtime,只在 handoff/backlog 标边界」的管辖处理。
- **分歧 2(KG-23 × KG-37 修法互斥)**:
  - 对方论证:"branch-scope 仍默认正确;沙箱失败才由 breaker 降级到 working-tree + 空 diff 拦截" → **接受**,这正是我 P3R1 的降级链方案,对方补上了「scope 选择进 decision table」。
  - 我的最终立场:scope 语义先修文档-实现一致(KG-23 契约违约);ship 流程 branch-scope 默认;KG-37 类沙箱失效由状态机降级 working-tree;**空 diff / vacuous approve 拦截判定进 SKILL 决策表**(空 diff → verdict 无效,不产生 approve),ship hook 只消费该判定结果。
  - 让步:无(双方同案)。
- **分歧 3(KG-22 修法深度)**:
  - 对方论证:"应加最小 phase/status 字段与读取规则……不扩成 phased spec 重构" → **接受收窄**。
  - 我的最终立场:最小 schema 扩展——per-phase status 字段 + 下游 gate 读取规则,不动 frozen-before-build 铁律,不做 phased spec 全量重构。
  - 让步给对方的部分:接受「最小化」边界,放弃我原表述中可能被读大的「共用契约对齐框架」扩展空间(框架同构性只作论证,不作实施范围)。
- **分歧 4(fork-id 兼容范围)**:
  - 对方论证:"FULL backward-compatible;新语法须 path-safe……写语法、禁用字符、旧/新/异常 fixture" → **接受**,与我立场一致。
  - 我的最终立场:FULL 向后兼容(001-radar-pA 及全部已铸 id 合法化);语法收编进 SHARED-CONTRACT;fixture 语料三类齐备(旧 id / 新三段式 / path-traversal 异常样本);check-6 regex 降级为「契约的一个实现」,随契约测试走。
  - 让步:无(双方同案)。

## 2. 联合 verdict(单一)

**refactor,不 redesign、不 cut codex。**簇1 五条 KG 收敛为一个「review 通道状态机」refactor:codex 保持 primary reviewer,外包 circuit breaker 四要素——失效三分类判据(起不来 / 起得来跑不动 / 跑得动挂死)触发开路,task risk × 领域决定 fallback reviewer 分流,watchdog 判死(心跳源 = job log 末次活动,阈值 = threshold × period,防假阳性),fallback verdict 带审计标注不冒充 codex,codex 恢复后补跑作 half-open 权威确认。判死阈值声明与轮询规则现在落 SKILL(IDS 三层同步);companion.mjs 内建 watchdog 为目标态,作为授权条目经 hand-off/backlog 交 XenoDev 实施。KG-B1 终结「逐例放宽 regex」路径:fork-id 语法进 SHARED-CONTRACT 作跨仓 SSOT,FULL 向后兼容已铸 id、显式 path-safe 字符集,双仓消费同一 fixture 语料跑契约测试;gen-handback 废除「仓根 HANDOFF = 唯一活跃 fork」假设,fork-id 显式化。簇3/4:KG-22 最小 per-phase status schema + gate 读取规则;KG-34 「migration 必真跑 alembic upgrade head」硬 checklist;KG-33 只加守卫 + 告警,根因待复现不推演;KG-12/KG-31 papercut 一并清。无 unresolved。

## 3. 残余分歧降级为 v0.2 note

- **v0.2 note 1(KG-33 根因)**:worktree remove 丢 stash 指针仅做守卫 + 告警;何时回头看——XenoDev 侧任一次可控复现成功后,再裁根因修法(对齐 forge-verdict-vs-empirical-ship 教训)。
- **v0.2 note 2(half-open 校准)**:「codex 恢复后补跑作权威确认」的触发时机(每次 fallback 后必补跑 vs 仅 high-risk task 补跑)未细化;跑 3-5 次真实 fallback 后按数据校准。
- **v0.2 note 3(通用长任务框架)**:未编号条目的「后台长任务 liveness + 单实例锁」本轮只落约定(心跳查产物/日志不查进程表);若后续再出第二例多进程互写事故,升级为框架级通用组件设计。

## 4. W 形态产出的初步草稿建议

- **W 含 decision-list** → 我建议的 4 列矩阵 row(前 5 条):
  - 保留:「无 review 不 merge」强 hook fail-closed 姿态;codex primary reviewer 地位;REVIEW-LOG「subagent-fallback 不冒充」诚实标注惯例;KG-34 §2.4 真跑兜底实践。
  - 调整:codex-review SKILL 加状态机决策表(失效三分类 × 判死阈值 × 降级链 × 审计标注);scope 语义修文档-实现一致 + branch-scope 默认 + 沙箱失效降级 working-tree + 空 diff 拦截;KG-35 verdict 提取三级 fallback 链(主 log → status --all summary → job logFile);KG-22 最小 per-phase status schema;KG-12/KG-31 papercut。
  - 删除:「逐例放宽 check-6 regex」修法路径;gen-handback「仓根 HANDOFF = 唯一活跃 fork」SSOT 假设。
  - 新增:SHARED-CONTRACT「fork-id 语法」章(SSOT + FULL 向后兼容 + path-safe 字符集)+ 双仓契约 fixture 测试;watchdog/liveness 约定(SKILL 层判死,声明/执行分离);「后台长任务 liveness + 单实例锁」纪律约定;companion.mjs watchdog 内建之 XenoDev 授权条目。
- **W 含 refactor-plan** → 关键模块(3 个):
  1. **codex-review SKILL(IDS 三层同步)**:review 通道状态机——失效三分类判据、判死阈值(心跳源 = job log 末次活动)、降级链(失败模态开路 × risk 分流)、verdict 提取三级链、空 diff 拦截、审计标注 + half-open 补跑。
  2. **SHARED-CONTRACT(跨仓契约层)**:新增 fork-id 语法 SSOT 章(语法、禁用字符、FULL 兼容声明)+ 双仓契约测试(同一 fixture 语料:IDS 铸造侧全过 + XenoDev 接受侧全过);KG-22 per-phase status 最小 schema + gate 读取规则同章或邻章落地。
  3. **XenoDev 侧授权条目(经 hand-off/backlog,不当场改)**:companion.mjs 内建 watchdog + status/result 语义修一致(status 恒 running 与 No job found 矛盾);gen-handback fork-id 显式参数化;KG-33 守卫 + 告警;KG-34 migration 硬 checklist 落 XenoDev 执行面。
