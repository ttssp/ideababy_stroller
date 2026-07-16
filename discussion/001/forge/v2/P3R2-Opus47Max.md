# P3R2 · Opus 4.8 Max · finalize(forge 001 v2 · strong-converge)

**Phase**: 3R2
**Written**: 2026-07-16T12:30:00Z
**Convergence mode**: strong-converge

## §1 · 对每条分歧的最终立场 + 让步

1. **自证对象(我 P3R1 分歧1 = 对方分歧1)**:收敛。真 briefing rerun = **MUST**(解锁条款写死);fixture 仅作回归测试,不得替代生效自证。对方 P3R1 已把 "真 briefing rerun 是 MUST" 立为立场,与我一致——无让步需要,只需 R2 落字。
2. **stage-0 语义写进 PRD(我分歧2,对方并入其分歧1)**:收敛。解锁条款明示:这是一次性 bootstrap 治理动作 + 最小机器谓词,不承担 certification;并写明**自托管点**(对方要求的补充,我采纳)——Phase 2 出口 ①② 生效后,机器验收面从 a1 谓词升级为完整 trace 验收。
3. **T010/T011 同批解锁(我分歧3 = 对方分歧2)**:收敛。同批、单一 unlock predicate(a1 产物 + ③),避免半解锁状态机;对方 "谓词只依赖 a1 amendment 产物" 的理由与我 "谓词与两 task 内容无关" 互补,合并入 rationale。

**无 unresolved。**

## §2 · 联合 verdict(单一)

**forge v1「机器可判三项」的 ①② 从 T010/T011 解锁前置中退役——KG-B9 采纳,循环依赖成立**(底料由 gate 下游的 T011/T021 产,checker 底料 ⊂ gate 所 gate 的范围;且 ① 的谓词对象「判断/边」在解锁时点结构性不存在)。①② **重绑两处**:T021/T022 的 ship 验收(其验收测字面即 ①②,底料彼时天然存在)+ O2/O7 使用期抽查对象(生产 trace 抽样审计范式)。**新 T010/T011 解锁前置(单一谓词 · 同批解锁)**= a1(per-slice source 映射最小前移:仅 slice→source refs 保留,走 P0.1 amendment 通道,不建图不做 judge,不违 RT-2)落地后,机器秒级判三件:briefing 带 slice→source 映射且逐项可解析到检索语料 / ③ 轻量审计通道结构就位 / 产物命名一致。**生效条件写死:对真 briefing rerun 自证 PASS**(fixture 仅回归);解锁语义显式命名为一次性 stage-0 治理动作 + 自托管点条款。**KG-B4 改写落点更新**:机器道 STOP 的 wiring 对象 = a1 映射 + ③ 结构 + 治理 STOP 记录(全部为真实存在的文件级 artifact)。KG-B7 冻结、识伪零解锁语义、FAIL→STOP 双道——v1 已裁,维持不变。

## §3 · 残余分歧降级 v0.2 note

1. ①② 在 Phase 2 出口的「秒级可判」仍是推演——T021/T022 落地时须对第一份真判断 briefing 复用同款自证协议(真产物 rerun);不达标按双道回流。
2. a1 动冻结 `TimeSlice` 的消费面枚举(slicer/reconstructor/writer/gate/injector/序列化)留 XenoDev spec 层;forge-lite 教训(KG-36):序列化面最易 silent 丢,amendment review 必须逐面 grep。
3. 使用期抽查的频率/条件设计(固定比例 vs tail-sampling 式条件抽样)攒 journal 数据后定。
4. 若 T021 长期不落地,机器验收面长期停在 a1 谓词——治理道兜底,v0.2 检视是否需中间验收点。

## §4 · W 形态产出的初步草稿建议

- **verdict-only**:§2 全文即草稿。
- **decision-list**(建议行):保留 = 双道 STOP / B7 冻结 / 识伪零解锁 / ③(配 a1 后非空壳);调整 = ①② 重绑 Phase 2 出口 + 使用期(资格改写非删除)/ KG-B4 wiring 对象改绑 a1 产物+③+治理记录 / O4 初始层谓词重写;删除 = ①② 作解锁前置的资格 / a2「先启空壳 ③」原样 / 「三项」并列表述(①② 与 ③ 不再同层);新增 = a1 最小前移(窄授权 + RT-2 边界条款)/ 真 rerun 自证生效条款 / stage-0 + 自托管点语义入 PRD / unlock-preflight checker(B4 落点)。
- **next-PRD**(v1.3→v1.4 方向):O4 初始层重写(解锁前置 = a1 谓词三件 + stage-0 语义 + 自证条款 + 自托管点);Open questions #3 再更新(「机器可判三项」表述废止,①② 迁移说明);识伪/长期层/Scope OUT 不动。
- **refactor-plan**(XenoDev 四模块,替换 v1 refactor plan 的 A/C):A' = a1 amendment(slicer/reconstructor/writer 保留 paper→slice 映射 + TimeSlice 契约变更授权,S-M);B' = unlock-preflight checker + 机器道 STOP wiring(a1 映射可解析 + ③ 结构 + 命名一致,S);C' = ③ 审计通道最小文件结构(S);D' = 自证协议(真 briefing rerun 一次 + 结果入 journal,S)。v1 模块 B(gate.py 降级校准工具)、D(journal schema)不变继续有效。①② full checker **不建**——迁到 T021/T022 验收原位。
