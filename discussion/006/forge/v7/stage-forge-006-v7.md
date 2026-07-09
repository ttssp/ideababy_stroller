# Forge Stage · 006 · v7 · "review gate 单点依赖根治 + fork-id 跨仓契约漂移终结"

**Generated**: 2026-07-08T00:00:00Z
**Source**: forge run v7 with X = 4 标的（1 导航 + 1 pending KG 权威快照[首选] + 1 外部原文[可选核对] + 1 v6 承接）, Y = 工程纪律 + 架构设计, Z = 对标 SOTA（CI review gate 容错/降级 · fallback 制度化 · 挂起检测 · 多 reviewer 分流 · 跨系统 id/schema 契约演化）, W = decision-list + refactor-plan
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both), P2 (both), P3R1 (both), P3R2 (both)
**Searches run**: 16 across ~10 distinct sources（circuit breaker · k8s liveness probe/watchdog · Schema Registry + Pact 契约测试 · GitHub required status checks · CODEOWNERS bypass vs merge queue · SRE/Google/MS/GitLab/Confluent）
**Moderator injections honored**: none（无 moderator-notes.md）
**Convergence outcome**: converged（单一 verdict · 双方 P3R2 4/4 分歧全签字收敛 · 无 unresolved · 3 条 v0.2 note）

---

## How to read this

forge 是横切层（不是 L1-L4 pipeline 的一部分）。本文档是 v7 forge run 双专家审阅 + SOTA 对标 + 联合收敛后的产物，**强制给出立场**。本轮承接 v6（可移植性加固,覆盖 KG-26~31,不重叠）,专攻两条主线:review gate 对 codex 的单点依赖 + KG-B1 跨仓 fork-id charset 协议漂移。

- W 只勾了 **decision-list + refactor-plan**,本文档就只产这两块(无 verdict-rationale / next-PRD / dev-plan / long-essay)。
- verdict 是**单一收敛**(strong-converge),骨架取自双方 P3R2 §2 联合 verdict(两份逐条同案)。
- refactor-plan 每条都标清**落哪个仓(IDS mirror 三层同步 / XenoDev 授权条目)+ 落地顺序**,可直接指导落地。
- 读完你应能直接进 §"Decision menu" 选 [A] 全落 / [B] 局部先落 P0 / [C] 跑 v8 / [P] park。

## Verdict

**refactor,不 redesign、不 cut codex。** 簇1 五条 KG 不是 5 个孤立 bug,是**同一根因的 5 个失效切面 = review gate 把 codex 当唯一可靠通道,但它在 scope 语义(KG-23)/额度(KG-32)/输出落盘(KG-35)/沙箱(KG-37)/会话流挂死(KG-38)五处都会失效**,而失效处理停留在临场外推(CLAUDE.md 过桥文字),没升格为架构组件。

修法 = 把 codex 保持 primary,外包一个「review 通道状态机」(circuit breaker 四要素:失效三分类判据 × watchdog 判死 × 降级链 = 失败模态开路 + risk×领域分流 × 审计标注 + half-open 补跑)。KG-B1 终结「逐例放宽 regex」路径:**fork-id 语法进 SHARED-CONTRACT 作跨仓 SSOT,FULL 向后兼容已铸 id(001-radar-pA 立即解阻),双仓消费同一 fixture 跑契约测试**。

单一 verdict 回应 K 双主攻:① review gate 单点依赖(K1)→ 状态机 + 预定义降级链替代临场犹豫,挂起态(K2)→ watchdog 判死触发 fallback;② KG-B1 跨仓漂移(K3)→ 契约层 SSOT,不逐例放宽,反向通道立即恢复。硬约束(K5 mirror 件 IDS 三层同步)全量遵守;companion.mjs 内建 watchdog 为目标态,作授权条目经 hand-off/backlog 交 XenoDev,不在 XenoDev 当场改。

## Evidence map

| 结论 | 来源 | 引用 | 反对证据 |
|---|---|---|---|
| 簇1 五条同根 = review gate 单通道 + 失效停留惯例 | P1-Opus §1B + P1-GPT §1A + P3R1 双方 §1 | "失效处理是事后追认的惯例而非架构组件" | - 双方 P1 + SOTA 同判 |
| 不 cut codex(有真实发现价值) | P1-GPT §1A + P2-Opus §3 | "T001 codex R1 抓到真实 high 缺陷;fallback 也没绕过 review" | - 双方同判 |
| 制度化 = 套 circuit breaker 四要素(非自创) | P2-Opus §1 row1 + P2-GPT §1 row2 | "实践已自发长出 half-open(codex 恢复补跑)" | - SOTA 背书 |
| 判死用 watchdog 公式:心跳源 = job log 末次活动(非 pid) | P2-Opus §1 row2 | "status 恒 running 正是查错了心跳源" | ⚠ 执行层归属 P3R1 分歧1(见 §underweight,R2 已收敛为两段式) |
| fallback = 交叉矩阵(失败模态开路 × risk/领域分流) | P2-Opus §3(修正 P1-Opus 单轴) + P2-GPT §3 | "失败开路,risk/领域分流" | ⚠ P1-Opus 原「按 risk 单轴」被 P2 修正 |
| KG-B1 拒绝第三次逐例放宽 regex → 契约层 SSOT | P1-Opus §1B + P2-Opus §1 row3 + P3R2 双方 §2 | "每种新命名再断一次 = 教科书级缺契约测试症状" | - 双方同判(KG-29 史佐证) |
| fork-id FULL 向后兼容已铸 id + path-safe 字符集 | P3R1 双方分歧4 + P3R2 双方 §1 | "001-radar-pA 已铸且阻塞,新语法须 path-safe" | - 双方同案(分歧4 已收敛) |
| gen-handback 废「仓根 HANDOFF = 唯一活跃 fork」假设 | P1-Opus §1B + P1-GPT §1B + snapshot KG-B1 附带发现 | "多 fork 并行时会静默拿 stale id" | - 双方同判 |
| KG-23 branch-scope 默认 + 沙箱失效降级 working-tree + 空 diff 拦截 | P3R1-Opus 分歧2 + P3R1-GPT 分歧2 + P3R2 双方 §1 | "空 diff → verdict 无效,不产生 approve" | ⚠ KG-23×KG-37 修法互斥(P3R1 分歧2,R2 已用降级链解) |
| KG-22 最小 per-phase status schema + gate 读取规则(不重构 phased spec) | P3R1 双方分歧3 + P3R2 双方 §1 | "只加 per-phase status+gate 读取规则……不重构 phased spec" | - 双方收窄同案 |
| KG-33 只加守卫+告警,根因待复现不推演 | P1-Opus §1A + P3R2-Opus §3 v0.2 note | "根因存疑,不该在推演里定修法,先真复现" | - 对齐 forge-verdict-vs-empirical-ship 教训 |
| KG-34「migration 必真跑 alembic upgrade head」硬 checklist | P1-Opus §2 + P1-GPT §1A + P3R2 双方 §2 | "单测测不出,只有真跑兜底" | - 双方同判 |
| mirror 件(codex-review SKILL)改动落 IDS 三层同步 | forge-config K5 + P3R1 双方 §4 + P3R2 双方 §2 | "不在 XenoDev 当场改;runtime 边界进 handoff/backlog" | - K 硬约束 |

（表以最 load-bearing 的 13 条结论为限;KG-12/KG-31 papercut 归入 refactor-plan 一并清,不单列）

## Intake recap

### X · 审阅标的(4 个)
- **导航** · `FORGE-006-v7-PENDING.md`(本仓库文件 · pending KG 聚簇导航 + 两 session fresh evidence)
- **权威全文快照[首选]** · `forge/v7/_x-backlog-snapshot.md`(本仓库文件 · pending KG 权威文本合流 KG-12/22/23/32/33/34/35/37/38 + KG-B1 + 未编号长任务条 · 标注 provenance)
- **外部原文[可选核对]** · `/home/ys/codes/XenoDev/dogfood-backlog.md`(外部 repo · 分支依赖 · Codex 沙箱可能 BLOCK)
- **v6 承接** · `forge/v6/stage-forge-006-v6.md`(stage 文档 · v6 verdict=可移植性覆盖 KG-26~31 · 确认 v7 不重叠)

### Y · 审阅视角
- ✅ 工程纪律(review/CI/fallback 机制 · 核心)
- ✅ 架构设计(review gate 单点依赖 · fallback 分流架构)

### Z · 参照系
- mode: 对标 SOTA(CI review gate 容错/降级 · fallback 制度化/circuit-breaker · 长时任务挂起态检测 liveness/watchdog · 多 reviewer 分流 · 跨系统 id/schema 契约演化)
- 用户外部材料: 无(K 未给额外链接)

### W · 产出形态
- ✅ decision-list(4 列矩阵:保留/调整/删除/新增)
- ✅ refactor-plan(按模块分组 · SKILL/协议层改法 · 落 IDS 三层同步)

### K · 用户判准
> v7 收 v6(可移植性)之后攒的一批框架级 KG,主攻【codex-review 作为 review gate 的可靠性】——簇1 五条同根(KG-23 scope 语义 / KG-32 额度死锁 / KG-35 输出落盘 / KG-37 沙箱权限 / KG-38 会话流静默挂起),共同根因是 review gate 把 codex 当唯一可靠通道,但它在五处都会失效。核心诉求:**review gate 不能单点依赖 codex,fallback 要制度化不靠临场犹豫,且挂起态要能超时检测触发 fallback**。(毗邻证据:未编号「后台长任务缺存活检测+单实例锁」与挂起检测同主题族。)
>
> **簇2 升级为第二主攻(2026-07-07 现场并入)**:KG-B1(spine 级 · high · 正在阻塞)——hand-back validator 约束6 charset regex 不接受 IDS 铸的「带 idea-slug 中段」fork-id(001-radar-pA 三段式),连 KG-29 v0.3 修都不接 → 001-radar-pA 全部 hand-back 无法发布,反向通道断裂。附带 gen-handback 强读根 HANDOFF 的 SSOT 假设在多 fork 并行下会静默用错 fork id。**fork-id 铸造约定 SSOT 在 IDS,charset 校验在 XenoDev mirror——跨仓协议漂移,恰是 forge 该裁的**:修 regex(严审 path-traversal)还是收紧 IDS 铸造,或两者。簇3(KG-33/34)/ 簇4(KG-22)顺手清。
>
> 硬约束:codex-review SKILL 是 IDS bootstrap-kit mirror 件,改动必须落 IDS 三层同步,不在 XenoDev 当场改。fresh evidence 权重:KG-38 是 2026-07-06 T017 新撞;KG-12 连续两 session 重现;KG-37 T016 撞、T016b 证间歇性。活疼不是陈账。

### 收敛模式
strong-converge

---

## Decision matrix

针对 X 标的现状,4 列矩阵。每行可在 §"Evidence map" 溯源。

| 类别 | 项 | 来源(标的具体位置) | 理由 | 优先级 |
|---|---|---|---|---|
| **保留** | 「无 review 不 merge」强 hook fail-closed 姿态 | parallel-builder SKILL §3/§4.1 | 强 gate 卡死不丢人,别动;SOTA 也不弱 gate 而是状态化重验 | P0 |
| **保留** | codex primary reviewer 地位 | codex-review SKILL 全体 | T001 codex R1 抓到真实 high;有发现价值,cut 是错答案 | P0 |
| **保留** | REVIEW-LOG「subagent-fallback@date 不冒充 codex」诚实标注惯例 | 009 T016/T017 REVIEW-LOG | 已避开 CODEOWNERS bypass「冒充」坑,方向对,升格即可 | P0 |
| **保留** | KG-34 §2.4「真跑 alembic upgrade head」兜底实践 | parallel-builder §2.4 | 是它抓到 ':字' bind-param 陷阱,单测测不出 | P0 |
| **调整** | codex-review SKILL 加状态机决策表(失效三分类 × 判死阈值 × 降级链 × 审计标注) | codex-review SKILL §2 决策表 / §3 / §4 | 把 CLAUDE.md 过桥文字制度化,消除临场犹豫成本(KG-32/37/38 家族) | P0 |
| **调整** | scope 语义修文档-实现一致 + branch-scope 默认 + 沙箱失效降级 working-tree + 空 diff 拦截 | codex-review SKILL §0.2 line 67 / §3 ship 契约 | KG-23 是文档-实现契约违约(vacuous approve = 假绿最危险),KG-23×KG-37 用降级链解互斥 | P0 |
| **调整** | KG-35 verdict 提取三级 fallback 链(主 log → status --all summary → job logFile) | codex-review SKILL §4 verdict 解析 | 只 grep 主 log 会漏 verdict → 误判无 finding 可 merge | P1 |
| **调整** | KG-22 最小 per-phase status schema + 下游 gate 读取规则 | spec-writer SKILL §3.3 frontmatter + 3 consumer gate | 只读 top-level 会把未审 v0.2 当 buildable,破 frozen-before-build | P1 |
| **调整** | KG-12 validator README valid 示例改 producer mode + 补 consumer fixture;KG-31 gen-handback mac 字面路径 | handback-validator README / gen-handback template | papercut,连续两 session 重现,一并清 | P2 |
| **删除** | 「逐例放宽 check-6 regex」修法路径 | handback-validator check-6 | 已断两次(KG-29→KG-B1),每种新命名再断一次,路径本身错 | P0 |
| **删除** | gen-handback「仓根 HANDOFF = 唯一活跃 fork」SSOT 假设 | gen-handback 强读根 HANDOFF | 多 fork 并行(008/009/001)时静默拿 stale id | P0 |
| **删除** | 判死靠 pid 存活 / ps\|grep 进程表判进程活 | companion status 恒 running / 未编号长任务条 | 查错心跳源,ps\|grep 误判起 3 进程互写坏 mp4 是反面教材 | P1 |
| **新增** | SHARED-CONTRACT「fork-id 语法」章(SSOT + FULL 向后兼容 + path-safe 字符集) + 双仓契约 fixture 测试 | (新建 · 来自 Schema Registry + Pact SOTA) | 语法定义权收契约层,IDS/XenoDev 都变 consumer,终结跨仓漂移 | P0 |
| **新增** | watchdog/liveness 判死约定(SKILL 层声明阈值 · 声明/执行分离) | (新建 · 来自 k8s liveness probe SOTA) | K2 挂起态超时检测触发 fallback,声明阈值 threshold×period + 防假阳性 | P0 |
| **新增** | companion.mjs 内建 watchdog + status/result 语义修一致 · XenoDev 授权条目 | (新建 · 经 hand-off/backlog) | 目标态执行层属拥有 job 生命周期的 companion;mirror 边界不当场改 | P1 |
| **新增** | 「后台长任务 liveness + 单实例锁」纪律约定(心跳查产物/日志不查进程表) | (新建 · 未编号长任务条) | 与挂起检测同族,先落约定;再出第二例事故则组件化(v0.2 note 3) | P2 |

## Refactor plan

按模块分组(模块来自 review gate + 跨仓契约的现有结构)。合并吸收双方 P3R2 §4 草稿(Opus 三模块 + GPT 补 CODEOWNERS routing / merge-queue 重验 / schema compatibility fixture)。

### 模块 A · codex-review SKILL(review 通道状态机)· 落 IDS 三层同步

- **当前问题**:codex-review SKILL 本体无任何失效分支(P1-Opus §1A);一周内 fallback 被迫发生 3 次 3 种失效模态(KG-32 额度尽 / KG-37 沙箱起得来跑不动 / KG-38 会话流挂死),都靠「按铁律外推」临场判断,每次消耗犹豫成本;companion 无超时、无 fail-closed、status/result 语义自相矛盾。
- **目标态**:review 通道状态机 = circuit breaker 四要素(P2-Opus §1 row1;SOTA:groundcover/Aerospike)。codex 保持 primary,失效时安全降级,恢复后 half-open 补跑作权威确认(实践已自发长出)。
- **改造步骤**(顺序):
  1. **失效判据三分类**进 SKILL §2 决策表:起不来(KG-32 额度)/ 起得来跑不动(KG-37 沙箱 bwrap)/ 跑得动挂死(KG-38 会话流静默)→ 三类均触发 breaker 开路走 fallback。
  2. **watchdog 判死规则**:心跳源 = job log 末次活动(**非 pid 存活**,status 恒 running 正是查错心跳源);阈值 = threshold × period;显式防假阳性(负载慢≠挂死)。判死阈值声明现在落 SKILL(IDS 三层同步件,forge 直接决议);SKILL 侧轮询判死为过渡态。
  3. **降级链 = 交叉矩阵**(P2-Opus §3 修正单轴):失败模态决定开路,task risk × 领域决定 fallback reviewer 分流(write-boundary → red-team+code-reviewer 双跑;medium test-only → code-reviewer 单跑,与 T016/T017 实践吻合)。补 CODEOWNERS-style routing 表(GPT 补:失败开路 + owner/领域分流,不是补丁式 bypass,避开 merge-queue all-or-nothing 破坏)。
  4. **verdict 提取三级 fallback 链**(KG-35):主 stdout log → `status --all --json` 的 latestFinished.summary → job 独立 logFile,任一拿到即用。
  5. **scope 语义 + 空 diff 拦截**(KG-23×KG-37):文档-实现先改一致;ship 流程 branch-scope 默认;沙箱失效由状态机降级 working-tree;**空 diff → verdict 无效不产生 approve**,判定进 SKILL 决策表,ship hook 只消费结果。
  6. **审计标注 + half-open**:fallback verdict 带 `reviewed-by: subagent-fallback@date` 不冒充 codex;codex 恢复后补跑作权威确认。
- **风险**:双模型回声室(双方 P3R1 「收敛度罕见地高」)可能掩盖共享盲点;watchdog 阈值靠 3-5 次真实 fallback 校准(v0.2 note 1)。
- **预估代价**:M(SKILL 决策表 + 三处 verdict 解析改造,IDS 三层同步)。

### 模块 B · SHARED-CONTRACT(跨仓 fork-id 契约层)· 落 IDS 三层同步

- **当前问题**:fork-id 铸造在 IDS(plan-start),校验在 XenoDev(check-6 charset regex),两边无共同 schema 定义源(P1-Opus §1B);KG-29 v0.2→v0.3 只放宽 `-p` 多字符,001-radar-pA 的 idea-slug 中段立刻再断,且 v0.3 修还只在 009 分支(main 停 v0.2)——每种新命名再断一次,每次修跨分支漂。
- **目标态**:fork-id 语法进 SHARED-CONTRACT 作跨仓 SSOT(P2-Opus §1 row3;SOTA:Schema Registry + Pact 消费者驱动契约测试),IDS/XenoDev 都变 consumer,check-6 regex 降级为「契约的一个实现」。
- **改造步骤**(顺序):
  1. SHARED-CONTRACT 新增「fork-id 语法」章:语法规范(三段式 `NNN[-slug]-pX*`)、禁用字符表、**FULL 向后兼容声明**(001-radar-pA 及全部已铸 id 合法化)、显式 path-safe 字符集(严审 path-traversal:中段只引连字符不引危险字符,basename+realpath containment 防线仍在)。
  2. **双仓契约 fixture 语料**(GPT 补 schema compatibility fixture):三类齐备 —— 旧 id(001-radar-pA/008-pB/009-pForge)/ 新三段式 / path-traversal 异常样本(`009-pv0.2`、`008/../../etc`)。IDS 铸造侧全过 + XenoDev 接受侧全过,同一语料双仓各跑。
  3. **gen-handback 废「仓根 HANDOFF = 唯一活跃 fork」假设**:fork-id 显式参数化(加显式 HANDOFF 路径 flag + 多-fork workflow 规约),防多 fork 并行拿 stale id。
  4. KG-22 per-phase status 最小 schema + gate 读取规则同章或邻章落地(与 fork-id 共用「契约对齐」框架,但仅最小 schema,不重构 phased spec)。
- **风险**:path-safe 字符集若放太宽引入 traversal 面(Y 未含专门安全视角,但 KG-29 已走 OWASP,此章须复用同防线);半同步窗口(mirror 无法字节级同时落,沿用 v6 组 G 同步 checklist)。
- **预估代价**:M(SHARED-CONTRACT 章 + IDS check-6 + XenoDev mirror + fixture 双仓)。

### 模块 C · XenoDev 侧授权条目(经 hand-off/backlog · 不当场改)

- **当前问题**:companion.mjs 是 XenoDev 侧 runtime(非 bootstrap-kit mirror 件),forge 不当场改;但 watchdog 目标态执行层、gen-handback 实现、KG-33/34 执行面都在 XenoDev。
- **目标态**:目标态改动经 hand-off/dogfood-backlog 传达 XenoDev 实施,IDS forge 只写「授权条目 + 边界标注」(K5 硬约束 + 双方 P3R1 §4)。
- **改造步骤**(授权条目,不在本 forge 落地):
  1. companion.mjs 内建 watchdog(目标态执行层)+ 修 status/result 语义不一致(status 报 running 时 result 该回「job 仍 running · 无结果」而非「No job found」)。
  2. gen-handback fork-id 显式参数化实现(消费模块 B 的契约)。
  3. KG-33 §5 删 worktree 前 stash list 快照 + 删后比对告警(**根因待复现不推演**,v0.2 note 2)。
  4. KG-34 「migration task 必真跑 alembic upgrade head」硬 checklist 落 XenoDev 执行面 + parallel-builder §2.4。
  5. 「后台长任务 liveness + 单实例锁」纪律约定落地(flock 单实例锁 + 心跳查产物/日志不查进程表)。
- **风险**:授权条目跨仓传达有落地滞后;companion watchdog 未落前 SKILL 轮询判死为过渡态,判死靠人工触发存在窗口。
- **预估代价**:L(涉及 companion runtime 改造 + 跨仓协调,非本 forge 直接管辖)。

---

## What this menu underweights(强制自批判)

- **双模型回声室(最该警惕)**:双方 P3R1 均称「四份 round file 收敛度罕见地高」「诊断层完全一致」,P3R2 4/4 分歧全签字。**共享盲点风险**:双方独立检索都撞同一组 SOTA(circuit breaker/watchdog/Schema Registry/Pact),可能是这组模式确实对,也可能是两模型训练语料共享同一「韧性工程」canon 而集体忽略了更贴合「单人双机非发行」场景的更轻方案。verdict 采纳状态机是因 SOTA 背书 + 实践已自发逼近,但**它是把成熟企业级模式套到单人工具链上,可能过度工程**——若落地后发现状态机维护成本 > 临场判断成本,是 v8 触发信号。[[forge-verdict-vs-empirical-ship]] 教训在此适用:理论决议会漏实证盲区,watchdog 判死阈值、half-open 触发时机必须真跑校准。
- **反对证据的整合**(§Evidence map 标 ⚠ 的):
  - watchdog 执行层归属(P3R1 分歧1):companion.mjs 改动是否越出 IDS forge 管辖,材料无直接答案 → R2 用「两段式」解(现在 SKILL 轮询 / 目标态 companion,授权条目交 XenoDev)。主 verdict 仍坚持是因职责分离(k8s probe 声明/执行分离)有明确 SOTA 形状,但**过渡态 SKILL 轮询判死仍靠人工触发,存在无人值守时的挂死窗口**。
  - KG-23×KG-37 修法互斥(P3R1 分歧2):branch-scope 最对但恰是沙箱重灾区 → R2 用降级链解(branch 默认 + 沙箱失效降 working-tree + 空 diff 拦截)。但**这个交互在单条 KG 里看不见,若还有第三条 KG 与降级链顶牛,当前状态机未穷举**。
- **Y 视角覆盖盲区**:Y 只选工程纪律 + 架构设计,**未含专门安全视角**。模块 B 的 fork-id path-safe 字符集是纯安全判断(path-traversal 面),本轮靠 KG-29 已走的 OWASP containment 防线兜底,但**新语法中段字符集的 traversal 面未被独立 red-team**——建议落地时对 fixture 异常语料做一次专门安全扫,而非仅信推演。
- **K 中未充分回应的关切**:K 提「未编号长任务条 + 单实例锁」与挂起检测同族,本轮只落约定(心跳查产物不查进程表 + flock),**未做通用「后台长任务 liveness 组件」设计**(v0.2 note 3:再出第二例多进程互写事故才组件化)。若 operator 期望一次性根治,当前 verdict 只给了纪律约定不给组件。
- **X 标的覆盖局限**:X 只审 v7 pending 批次(KG-12/22/23/32/33/34/35/37/38 + KG-B1 + 未编号),v6 及更早 KG 不重审。**若 KG-1~25 里有与 review gate 单点或跨仓契约同根的坑,本 verdict 的状态机/契约设计未把它们纳入射程**。另:外部 dogfood-backlog 是分支依赖的(001 分支看不到 009 分支的 KG-30~38),快照合流了两边但**append-only 纪律在多分支并行下事实上被切成多本账**——这本身是一条未收进 verdict 的元级观察(P1-Opus §1B),值得后续 attention。
- **3 条 v0.2 note(非阻塞残留 · 来自双方 P3R2 §3)**:
  1. **watchdog 阈值校准** — 「codex 恢复补跑」触发时机(每次 fallback 必补 vs 仅 high-risk 补)+ 判死阈值未细化,跑 3-5 次真实 fallback 后按数据校准。
  2. **KG-33 根因** — worktree remove 丢 stash 指针仅做守卫+告警,XenoDev 侧任一次可控复现成功后再裁根因修法(对齐 forge-verdict-vs-empirical-ship)。
  3. **通用长任务框架** — 未编号条只落约定,再出第二例多进程互写事故则升级为框架级通用组件。
- **forge versioning 提示**:以下新信息进入会触发 v8 —— (a) 状态机上线后维护成本 > 临场判断成本(过度工程被证实);(b) SKILL 轮询判死过渡态在无人值守时反复挂死(companion watchdog 迟迟不落地);(c) fork-id 契约上线后**仍有新命名习惯再断一次**(证明语法/fixture 不完备);(d) 出现簇1 五类失效之外的**第六种** review gate 失效模态;(e) KG-33 复现成功拿到根因(触发 v0.2 note 2 回头看)。

## Decision menu(for human)

### [A] 接受 verdict · 落地全部改动(双仓)
```
落仓顺序(守 SSOT 三层同步 · K5 硬约束):
  IDS 侧(先):
    1. 模块 B — SHARED-CONTRACT「fork-id 语法」章(SSOT + FULL 兼容 + path-safe)
       + IDS check-6 对齐契约 + 双仓 fixture 语料
       → KG-B1 优先(spine 级 · 正在阻塞 001-radar-pA 反向通道,先解阻)
    2. 模块 A — codex-review SKILL 状态机决策表(失效三分类 × watchdog × 降级链
       × verdict 三级链 × scope/空 diff × 审计/half-open)· 三层同步
    3. 模块 B 尾 — KG-22 per-phase status 最小 schema + gate 读取规则
    4. papercut — KG-12 validator README/fixture + KG-31 gen-handback 字面路径
  XenoDev 侧(后 · 下发授权条目 brief · 不当场改 mirror):
    5. 模块 C — companion watchdog + status/result 语义 + gen-handback fork-id 参数化
       + KG-33 守卫告警 + KG-34 migration 硬 checklist + 长任务 flock 单实例锁
  每步记双仓 commit SHA · 半同步窗口用 v6 组 G 同步 checklist 收口
```
⚠ 框架级变更只走本 forge 决议后落地,不在 XenoDev 当场另改(K5)。
⚠ 模块 A/B 是 mirror 件(codex-review SKILL / SHARED-CONTRACT)· 必须 IDS 三层同步(条款 / bootstrap-kit / XenoDev mirror)。

### [B] 局部先落 P0(解阻 + 关键失效)
```
最小解阻集(先落这些):
  - 模块 B 步骤 1-3 全 P0:KG-B1 契约 SSOT(001-radar-pA 立即解阻,反向通道恢复)
  - 模块 A 步骤 1-2、5-6 P0:失效三分类 + watchdog + scope/空 diff 拦截 + 审计标注
  P1/P2 项(KG-35 verdict 链 / KG-22 schema / papercut / 模块 C 授权条目)后续批次
```
适用:KG-B1 硬阻断优先解,状态机核心先立,verdict 提取链和 papercut 缓落。

### [C] 跑 forge v8(说明需补什么)
```
/expert-forge 006
# 在 Phase 0 intake 调整 X / Y / Z / W / K;旧 v7 整目录保留作历史参考
```
适用触发(见 §underweight forge versioning):状态机被证过度工程 / SKILL 轮询判死过渡态反复挂死 / fork-id 契约上线仍有新命名再断 / 出现第六种 review gate 失效模态 / KG-33 复现拿到根因需裁修法。

### [P] Park
```
/park 006
```
保留所有 v7 forge 产物,标记暂停。复活时不重做本层收敛。

### [Z] Abandon
不适用 —— 本轮是框架加固(非产品 idea 存废判断),无 abandon 语义。簇1/KG-B1 是已 ship 框架的可靠性债与跨仓协议债,只有「修 / 缓修」,无「放弃这个 idea」。

---

## Forge log
- v7: 2026-07-08 — verdict: "review gate 单点依赖 = 同根 5 失效切面(scope/额度/落盘/沙箱/挂死);codex 保 primary + review 通道状态机(circuit breaker 四要素:三分类 × watchdog 判死[心跳=job log 非 pid] × 交叉矩阵降级链 × 审计/half-open);KG-B1 拒第三次逐例放宽 regex,fork-id 语法进 SHARED-CONTRACT 作 SSOT + FULL 兼容 001-radar-pA + 双仓 fixture 契约测试;mirror 件 IDS 三层同步,companion watchdog 授权 XenoDev"
- v6: 2026-07-02 — verdict: "5 条同根 = mac 环境形态硬编码成 constant;按 6 类性质分层外置 + 防漂移守卫 + KG-29 追认 keep;修可移植性的手段本身须先验可移植(mac sort -V)"
- v5: 并发安全 · CONCERNS(KG-1 G3 approve-over-approve / KG-2 B-3 同秒碰撞 · 已 ship 留 dogfood 观测)
- v4: hand-back/mirror 机制固化(v4→v5 攒批真问题再 forge 模式)
- v3/v2/v1: XenoDev 跨仓分工 + build runtime 边界确立(forge v2 verdict = IDS 治理 · XenoDev 唯一 L4 build runtime)
