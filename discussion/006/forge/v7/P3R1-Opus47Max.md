# Forge v7 · 006 · P3R1 · Claude · 联合收敛 R1(标分歧)

**Timestamp**: 2026-07-07T16:23:28Z
**Visibility**: 我已读对方 P1 + P2。
**Searches in this round**: NONE(避免 R1 又开搜索发散)。
**Model note**: 本轮由 Claude(Fable 5)执笔,文件名沿用管线约定。

## 1. 整合摘要

四份 round file 收敛度罕见地高。诊断层完全一致:簇1 五条 KG 的共同根因是 review gate 单通道架构 + 失效处理停留在惯例(对方 P1:"强 gate 自身不够确定";我 P1:"失效处理是事后追认的惯例而非架构组件")。SOTA 证据也互相印证——双方独立检索(我 5 次 / 对方 11 次)撞出同一组参照:circuit breaker、watchdog/liveness、CODEOWNERS/approval 分流、Schema Registry 兼容契约。对方 P2 headline「还不是可观测状态机加兼容契约」与我 P2 的「缺 SOTA 全部四要素」是同一句话的两种说法。

关键的相互修正也已发生:对方 P2 把我 P1 的「fallback 按 risk 分级」修正为**交叉矩阵**(失败模态决定开路,task risk/领域决定 reviewer 分流)——我接受,这比单轴更准,且与 T016/T017 实践吻合。反向,我 P2 把对方 P1 不确定点 2(扩 regex vs 收紧铸造)推进为第三条路:**语法定义权收到契约层**(SHARED-CONTRACT 收编 fork-id 语法 + 双仓同一 fixture 语料的契约测试),对方 P2 「按 schema 演化管」正好落在同一形状上。本轮活体证据(Codex 写 P1 时第三次撞 bwrap)进一步坐实「间歇性环境失效」不是陈账。

## 2. 我的初步 verdict(草案)

我倾向 **refactor(两个 Y 维度都是),不 redesign、不 cut codex**。核心裁定四条:(1)簇1 收敛为一个「review 通道状态机」refactor——circuit breaker 四要素(失效三分类判据 / 显式状态 / 预定义降级链 = 失败模态开路 × risk 分流 / 可观测),judged-dead 阈值用 watchdog 公式(心跳源 = job log 末次活动,非 pid 存活);(2)KG-B1 拒绝第三次逐例放宽 regex,fork-id 语法进 SHARED-CONTRACT 作 SSOT + 双仓契约测试,语法须向后兼容已铸的 001-radar-pA 并严审 path-traversal;(3)簇3/4 按各自性质清:KG-22 做 per-phase status 的 schema 契约修,KG-34 写「migration 必真跑」硬 checklist,KG-33 只加守卫+告警、根因先复现不推演;(4)所有 mirror 件改动落 IDS 三层同步。关键不确定点是挂起判死的执行层归属(分歧1),R2 解决不了就在 refactor-plan 里显式标 transitional。

## 3. 关键分歧清单

- **分歧 1:挂起判死的执行层归属 + 管辖权**
  - 我的立场:按 k8s probe 的声明/执行分离——阈值声明在 SKILL/config,执行属于拥有 job 生命周期的 companion;companion 改不动时 SKILL 侧轮询判死是过渡态。但 companion.mjs 是 XenoDev 侧 runtime,它是否属于 bootstrap-kit mirror 件、本 forge 能否直接决议改它,材料里没有答案。
  - 对方立场(P2):"codex 可保留为 primary,但要包 breaker/watchdog/fallback"——只给了要素,未给层次归属。
  - 我希望 R2 怎么收敛:对方明确表态执行层放哪(companion 内建 / SKILL 轮询 / 两段式过渡),以及 companion 改动在 refactor-plan 里的管辖标注(IDS 三层同步件 vs XenoDev 侧独立件 + backlog 授权)。

- **分歧 2:KG-23 × KG-37 修法互斥性**
  - 我的立场:KG-23 最正确的修法(ship 流程一律 branch-scope)恰好把 review 推进 KG-37 的沙箱重灾区。我主张:scope 语义先当「文档-实现契约违约」修一致,ship 流程 branch-scope 为默认,沙箱失效时按状态机降级为 working-tree + 空 diff lint 拦截 vacuous approve。
  - 对方立场:对方 P1/P2 均未触及这个交互(P1 只列 "KG-23 让 committed diff 变空审")。
  - 我希望 R2 怎么收敛:对方把簇1 当一个系统给出它对这对冲突的解法;若同意我的降级链方案,请补充空 diff 拦截的判定位置(SKILL 层还是 hook 层)。

- **分歧 3:KG-22 修法深度**
  - 我的立场:轻量成文不够——KG-22 与「required check 期望名 X、matrix 报名 Y」同构,是 status 命名契约不匹配,该做最小 schema 扩展让 gate 按 phase 读取,和 KG-B1 共用「契约对齐」框架。
  - 对方立场(P1 不确定点 3):"轻量成文约束足够,还是必须让 schema/gate 按 phase 读取状态?"——悬而未决。
  - 我希望 R2 怎么收敛:对方在两选项间表态;若选 schema,给最小字段形状(per-phase status 数组即可,不动 frozen-before-build 铁律)。

- **分歧 4(确认项):fork-id 语法的向后兼容范围**
  - 我的立场:新语法必须全量接受已铸 id(001-radar-pA 正在阻塞,改名历史成本不可接受),即「FULL backward-compat + path-safe 字符集」。
  - 对方立场(P2):"KG-B1 应按 schema 演化管"——compatibility policy 方向一致,但未显式确认对已铸 id 全兼容。
  - 我希望 R2 怎么收敛:确认 FULL 兼容 + 在 refactor-plan 给出具体语法形状(如三段式 `NNN[-slug]-pX*`)和 fixture 语料清单。

## 4. 与 K 的对齐性自检

- K1「review gate 不能单点依赖 codex,fallback 制度化不靠临场犹豫」→ ✅ verdict(1):breaker 态机 + 预定义降级链,交叉矩阵替代临场判断。
- K2「挂起态要能超时检测触发 fallback」→ ✅ watchdog 判死进 verdict;⚠ 执行层归属未定(分歧1,R2 必须收敛或显式标 transitional)。
- K3「KG-B1 裁 regex 扩展 vs IDS 铸造收紧」→ ✅ 裁了第三条路(契约层 SSOT + 双仓契约测试),终结「每种新命名再断一次」;分歧4 只剩兼容范围确认。
- K4「簇3/4 顺手清」→ ✅ KG-22(分歧3 定深度)/ KG-34 硬 checklist / KG-33 先复现不推演(对齐 forge-verdict-vs-empirical-ship 教训)/ KG-12、KG-31 papercut 一并清。
- K5 硬约束「mirror 件改动落 IDS 三层同步,不在 XenoDev 当场改」→ ✅ verdict(4)全量遵守;⚠ companion.mjs 的 mirror 归属待 R2 标注(并入分歧1)。
