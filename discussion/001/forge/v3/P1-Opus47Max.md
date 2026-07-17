# Forge v3 · 001 · P1 · Opus47Max · 独立审阅(no search)

**Timestamp**: 2026-07-17T05:52:00Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了(17/17,无跳过):IDS 侧 8 件全文(v2/v1 stage doc · hand-back 17/16/11 · HANDBACK-LOG(17 条决议史,重点 11-17)· PRD v1.4 · L3 moderator-notes 两次 injection);XenoDev worktree 侧 9 件——`audit_channel.py`/`unlock_preflight.py`/`rerun_selfcheck.py` 全文,`gate.py` 选读(模块 docstring + `evaluate_gate` 签名与 run 绑定段 + `write_rerun_pass_artifact` 结构,798 行按议题选读),`dependency-graph.mmd` 全文,dogfood-backlog KG-B9/B10/B11 段,followup-log FU-D-rerun 段,07-17 真跑盲测面产物(22 行)与被否签字模板(57 行)。**未读**同目录密封 answer-key(config ⚠⚠ 红线)。
- **K 摘要**:一次裁清两件事——A · gate 存废/形态四方向(g1 盲测二值已被否 / g2 留痕可审计验收 / g3 非阻断 smoke / g4 移 O2/O7 后验);B · a1 产物可见性时机(现 post-gate 才产 vs 留痕底料该始终可见)。硬约束:第四次「推演≠真跑」后,新形态必须附 07-17 真跑现有产物立即可验证的自证步骤 + 回答「真跑如何走到判定」;T010/T011 条款落定不悬空;防 V4 STOP 精神保留;a1 对错不再审;KG-B10 只裁前提方向;倾向改接 A'/B'/D' 而非重写。
- **阅读策略**:按 Y=架构设计,以「解锁判定的依赖链」为主线追代码(audit 产出时机 → B' 谓词输入 → D' 生效判定);按 Y=工程纪律,核对 fail-closed 纪律与 codex 硬化投资的前提;按 Y=产品价值/用户体验,拿 hand-back 11 operator 三条批评原话逐一对照现状产物形态。

## 1. 现状摘要(按 Y 视角组织)

### 视角 A · 架构设计

解锁链现状(a09d45b 后):`T003-A3(a1)→ T004-A2(B' 结构谓词)→ T004-A4(D' 生效自证)→ T010/T011`,`depends_on` 已重绑,机器道 wiring 结构闭合(hand-back 16)。B' 谓词(`check_unlock_predicate`)输入 = **audit.json + 盲测 briefing + corpus_refs** 三件,本身不直接依赖 gate。但 audit.json 的唯一生成入口 `generate_audit_channel_postgate` **强制要求 gate PASS artifact + run-binding 指纹校验**(audit_channel.py:198-257),而 gate PASS 只能由 `evaluate_gate` 对 operator 盲测签字对答案后产出(gate.py docstring:「三者全满足才 PASS」)。于是形成一条**隐依赖环**:a1 生效自证(D')→ 需 B' 谓词 → 需 audit.json → 需 gate PASS → 需 operator 盲测二值签字 = **被 operator 07-15 当面否掉的那个形态**。v2 verdict 说「a1 走 amendment 通道不被 gate 挡」对生成机制成立,但 **a1 的验证产物被 gate 挡**——真跑走不到判定(hand-back 17)不是实现 bug,是这条隐环的必然。RERUN-PASS artifact 在 hand-back 16 里「未退役 · 降为被 preflight 内部消费的 spine 底座」,实际效果 = 被否形态从「前门」搬到了「地基」,依然是唯一 driver。三条 a1 可见路径(盲测面故意不渲染 / render_markdown 不落盘 / audit.json post-gate)全部由「保识伪难度」这一个设计动机锁死(audit_channel.py round-3/4/5 注释链自证:去 period 字段、落受保护目录、post-gate 生成,全为防签字前泄负控)。

### 视角 B · 工程纪律

fail-closed 纪律全线优秀:`read_audit_channel` 严格结构校验(空壳/sparse 类型陷阱都拒),B' 的 ①b briefing 覆盖 fail-closed,D' 的 `independent_check_agree is not True 即不解锁`,fixture 恒不生效。KG-B10 两面(A' PASS artifact 可伪造 / D' selfcheck 信 caller 布尔)在源码 docstring 诚实降级为「非安全边界」并在册,未越权当场修——防 V4 纪律到位。但**投资前提风险重演**:audit_channel 的 run-binding/per-slice 指纹/防泄负控体系是 codex 10 轮硬化产物,其全部动机 = 「盲测识伪不可在签字前泄露」;而识伪在 v1 已裁 retire-as-gate keep-as-calibration。若 v3 裁 g2/g4,「签字前」这个时点概念本身消失,10 轮硬化的前提又塌一半——与 T004-A1 十四轮被 KG-B8 推翻同型(KG-B7 教训第三次逼近)。

### 视角 C · 产品价值

operator 三条批评对照现状:批评②「要留痕可审计」——留痕底料**已经存在**(audit.json 每 slice→source_refs,正是 O2 三击的结构锚),但被藏在 out/credibility/ 受保护目录、「判定前勿看」、post-gate 才产:**operator 在正常使用流中永远看不到它**。批评③「边用边迭代」——现状唯一判定入口仍是「跑完 → 停 → 人肉盲判签字」。即:v1/v2 两轮裁决后,产品的**留痕价值被拓扑锁在被否的考试形态后面**,a1 白前移了一半。另注意:盲测/负控/answer-key 只在「校准活动」有语义(v1 已裁零解锁);正常评估 run 本无负控注入需求——但现 CLI 真跑(07-17)默认仍走盲测面 + answer-key + 签字模板三件套,把校准形态当成了唯一形态。

### 视角 D · 用户体验

operator 操作面现状 = 签字模板 YAML 手填(slice:// 锚强约束、重跑拒 doc/node 锚)——考试式 UX,已被拒。审计侧没有任何 human-readable 入口:audit.json 是给 B' preflight 读的机器 JSON;render_markdown(渲染 refs 的人读审计面)真跑不落盘;「审计产物怎么看、多久看一次」在 PRD 只有 v0.2 open question。错误恢复通道(发现问题 → hand-back → 决议)已实证运转 17 条,是现状 UX 里唯一贴 operator 工作流的部分。

## 2. First-take 评分(按 Y 视角)

| Y 维度 | 倾向 | 理由(引用 §1 现状) |
|---|---|---|
| 架构设计 | **refactor** | 隐依赖环(a1 自证→audit→gate PASS→被否签字)必须拆:gate 从「唯一判定 driver」改为「校准活动组件」,audit.json 产出时机与 run 类型解耦(评估 run 生成时落盘、校准 run 维持密封)。B'/D' 谓词逻辑本身可原样改接——卡点只在输入产物的时机,不在谓词。 |
| 工程纪律 | **keep + 冻结** | fail-closed 纪律、双道 STOP、真跑自证结构强制全 keep;audit_channel 防伪造 spine 面(KG-B10 两面)**冻结不再投资**,等形态定(否则第三次重演 B7 过度投资)。 |
| 产品价值 | **refactor** | 留痕底料在而不可见 = 批评② 未兑现;g2 方向(留痕即验收)与 a1 产物「评估 run 始终可见」高度亲和;识伪密封需求收窄到校准 run。 |
| 用户体验 | **new** | operator 审计操作面结构性缺失:需要新建最小 human-readable 留痕面(render_markdown 落盘或等价物)+ 抽查入口;签字考试 UX 随 g1 废弃。 |

## 3. 我现在最不确定的 3 件事

1. **「按 run 类型分流」是否真能干净解开可见性张力**——我的初步方向是:评估 run(无负控)source 映射生成时即落盘可见;校准 run(injector 注负控)维持密封。但负控泄露面是否真的只存在于校准 run?盲测面与审计面同 ts 命名(B' ③ 命名一致检查)在分流后是否留下可 diff 的旁路?希望对方在 P3 对这个方案做对抗审查。
2. **无二值 PASS 后,D' 生效条款的判定语义怎么改写**——「真 rerun 自证 PASS」的 PASS 现在指 B' 结构谓词 + 独立核验一致,这部分**不依赖人肉签字**,似乎可整体保留、只换 audit.json 的供给时机;但若 g3(非阻断)成立,「解锁」概念本身要不要留?留 P2 搜 advisory-vs-hard gate 实证、P3 收敛。
3. **防 V4 的最小阻断集边界**——结构谓词 fail-closed(机器道)保留是我方确信项;不确定的是「叙事级可信性」还剩多少阻断语义(g2 的留痕验收是否阻断、还是全移 O2/O7 后验 + 治理道兜底)。这直接决定 KG-B10 前提方向:若评估 run 的 audit 不再 post-gate,KG-B10 收窄为「校准 run 的 answer-key 密封完整性」一件事,协议面大幅缩小。
