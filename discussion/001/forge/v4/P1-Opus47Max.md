# Forge v4 · 001 · P1 · Opus47Max · 独立审阅(no search)

**Timestamp**: 2026-07-17T17:25:00Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了(9/9,全部可达,无跳过):
  1. `stage-forge-001-v3.md` → 全文(Verdict + Evidence map + §underweights + v4 触发条件 + 生效条款原文)
  2. hand-back 19(`20260717T092547Z-...md`)→ 全文(§1 四模块 DONE / §4 codex 9 轮 + v4 触发核心 / §6 α·β·γ)
  3. `PRD.md` v1.5 → O4 全文 + Open questions #3 + 修订历史头
  4. `HANDBACK-LOG.md` → 19 条决议 lineage(重点 11/16/17/18/19 条)
  5. `selfcheck_sequence.py` → 全文(三道 fail-closed 守卫 + KG-B10 诚实边界 docstring)
  6. `cli/reconstruct.py` → 全文(`_emit_eval_run` / `_emit_calibration_run` 分流)
  7. `selfcheck-07-17.sh` → 全文(生效自证入口 + 头部「已知张力」注记)
  8. `diffusion-models-20260717T051551Z.md` → 全文(⚠ 同 stem answer-key/runbinding 只指认未读,红线遵守)
  9. `test_selfcheck_sequence_forge_v3.py` → 全文(5 主测 + 9 旁路回归测)
- **K(用户判准)摘要**:本次只裁一件事——生效条款标的重裁(α 对评估 run 新产物 / β 07-17 特批豁免 /
  γ 条款改写「首个评估 run 产物落地即自证」)。铁律:新条款必须附真跑可执行的兑现步骤,「首个评估 run」
  不许悬空;T010/T011 解锁链闭合;**护栏不拆**;不新建机制;烧 key 与轮换时序显式裁进条款。不再审:
  四模块机制对错、a1 对错、KG-B10 spine、g1 复活。
- **我的阅读策略**:按 Y=架构设计 先核「07-17 产物是否结构性不可为评估自证标的」(读产物本体 + 守卫代码);
  按 Y=工程纪律 核三选项各自与既有护栏/条款的冲突面(读 selfcheck_sequence.py 守卫 + 脚本 + 测试);
  按 Y=产品价值 核三选项与 07-15 拒签三条批评哲学的对齐(读 HANDBACK-LOG lineage + PRD O4 长期层)。

## 1. 现状摘要(按 Y 视角组织)

### 视角 A · 架构设计

生效条款现行文本(PRD v1.5 O4 + v3 verdict 同文)是**双重钦点**:「生效条件(写死):谓词须对
**07-17 真跑产物立即可跑自证**」。而 07-17 产物本体我已通读:标题即「位移重建(盲测)」,顶部有
盲测说明 + 「混入了阴性对照切片」提示,三个 slice 段**全部没有 per-slice 来源块**(评估面
`render_markdown` 独有的 `**来源(source refs...)**:` 块,盲测面从不产)。同 stem
`_answer-key-*.json` + `*.runbinding.json` 在 sibling `out/credibility/` 存在(指认未读)。也就是说
07-17 产物有**三层校准身份证据**:①同 stem 校准标记(触发 `_reject_if_calibration_stem`)②正文盲测
denylist 标记 ③缺评估形状 allowlist 特征(无来源块)。守卫链是三道独立防线,STOP 不是单一守卫的偶然
命中,是**产物身份的结构事实**。v3 条款把「立即可跑」绑在一个 pre-split 产物上,而 v3 自己的 C″ 分流
禁止评估自证消费校准产物——条款与分流在同一 verdict 内部自相矛盾,真跑只是把矛盾显影。

### 视角 B · 工程纪律

三选项与既有资产的冲突面逐一核过:**β 的冲突面最宽**——要放行 07-17 产物,须同时穿过三道守卫
(stem 标记物理存在、正文 denylist 命中、allowlist 特征缺失),任何「豁免」实现要么加旁路 flag
要么删守卫,都字面违反 K 第 3 条「护栏不拆」;且 codex round-3/4 正是在拦「校准 briefing 挪到干净
root」这类豁免同型操作。**α 无守卫冲突**但引入两个新依赖:烧 DEEPSEEK key(泄露前科、轮换 pending
自决议 16 起三连 pending)+ 需要一次「专门为自证而跑」的评估 run。**γ 无守卫冲突、无立即烧 key**,
但条款兑现从「立即」变为「事件触发」——K 第 1 条点名的悬空风险落在这里。不过我注意到一个结构事实:
T010/T011 解锁本身就 gated 在自证 PASS 上(preflight 消费 evidence bundle),所以 γ 的「首个评估
run」不是无约束的未来事件——**不跑评估 run 就永远不解锁**,阻塞是诚实且自我施压的。悬空风险的真实
形态是「解锁被无限期推迟」而非「条款被绕过」,这与 v3 那种「条款字面不可执行」有本质区别。

### 视角 C · 产品价值

07-15 拒签三条批评的第三条是「要边用边迭代,不要前置一次性闸门」。对照三选项:α 本质是**为治理
条款专门安排一次仪式性验证 run**——「停下来考试」的形态换了考生(机器考,不是人考),但「专门停下来」
的姿态没变;γ 把自证折进**第一次真实使用**——operator 下一次真的想评估某个方向时,产物落地即自证,
验证是使用的副产物。这与 O4 长期层「信任是使用中校准出来的」同构。另外从 lineage 看(HANDBACK-LOG
11→19),001 主线五次「推演≠真跑」全部发生在「治理设计对真跑现实的假设」上,而 γ 是三选项中唯一
**不再对真跑做新假设**的:它不假设 07-17 产物可用(β 的假设,已被证伪),也不假设一次仪式 run 的
时序可行(α 对 key 轮换的依赖),只声明「下一个自然发生的评估 run 即标的」。

## 2. First-take 评分(按 Y 视角)

| Y 维度 | 倾向 | 理由(引用 §1 现状) |
|---|---|---|
| 架构设计 | **cut(β)+ refactor(条款→γ 方向)** | 07-17 产物三层校准身份证据(§1-A),β 结构性不可行非仅不可取;条款标的从「特定历史产物」改写为「首个评估 run 产物」是最小修正 |
| 工程纪律 | **keep(全部守卫)+ refactor(条款补兑现步骤)** | 三道守卫是本轮最大资产(§1-B);γ 条款必须附 runbook 级兑现步骤(命令/窗口/key 时序/授权点),否则重蹈悬空 |
| 产品价值 | **γ keep-tendency,α 降为补充路径** | γ = 验证折进真实使用(§1-C);α 若被采,应重定义为「operator 恰好现在就想跑一次真评估」的即时执行版 γ,而非独立仪式 |

## 3. 我现在最不确定的 3 件事

1. **γ 的悬空缓解是否有先例背书**:「解锁条件绑首个真实 run、blocked 状态诚实持续」在 SOTA 里是
   正统(progressive delivery 的 activation criteria?)还是治理逃避?希望 P2 搜 canary/release
   qualification 绑首次生产 run 的实证,以及「blocked until first use」形态的失败案例(会不会
   演化成永远 blocked 的僵尸条款)。
2. **pre-split 遗留产物的处置先例**:ML eval 治理里 train/test contamination 发现后,被污染样本
   的标准处置是「降级出评估集」(γ 的降级同构)还是存在正当的「grandfather 豁免」条件(β 的
   残余生机)?若 SOTA 明确豁免是反模式,β 可干净关死。
3. **α 与 γ 的真实距离**:若 operator 本来近期就要跑一次真评估(radar 是自用产品,评估是其存在
   目的),α 和 γ 在时间轴上可能塌缩为同一件事,分歧只剩条款措辞(「立即专门跑」vs「首个自然
   run」)。希望对方 P3 给判断:条款措辞该锚「事件」还是锚「期限」,以及 key 轮换该写成条款前置
   还是并行 pending。
