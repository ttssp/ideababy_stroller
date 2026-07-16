# P1 · Opus 4.8 Max · 独立审阅(forge 001 v2)

**Phase**: 1(independent review · no search)
**Written**: 2026-07-16T11:20:00Z

## §0 · 我读到的标的清单 + 阅读策略 + K 摘要

**全部 14 项标的读毕,无 skipped**:proposal §001 摘要(经 v1 config)· v1 stage 文档 · hand-back 13(第一因)· PRD v1.3 · HANDBACK-LOG(13 条)· hand-back 11 · L3 moderator-notes(两次 injection)· dogfood-backlog(KG-B4/B7/B8/B9 + v1 处置回填)· T011.md · T021.md · dependency-graph.mmd · 真 briefing(run-877f1c1e)· gate.py(全 799 行)· domain/\_\_init\_\_.py(全 279 行)。

**阅读策略**:按 Y 三视角,先治理链(v1 verdict → PRD v1.3 → hand-back 13)建立裁决语境,再**独立核验** hand-back 的每条 file:line 证据——不转述,直接读源码。两条 provenance 备注:① KG-B9 原文只在 XenoDev **worktree** 副本(`.claude/worktrees/001-radar-pA/dogfood-backlog.md:646`),main checkout 尚未合回(hand-back「已记 dogfood-backlog」表述准确但需知位置);② specs/src 类标的已验证 worktree 与 main 逐字节一致。

**K 摘要**:裁三件事——A(①② 资格:trace 前移 a1 / 分阶段 a2 / 改使用期抽查对象 a3)· B(T010/T011 解锁前置定实,不许悬空)· C(KG-B9 与 B4 合并处置)。判准:贴真实工作流、防 V4 精神保留、**新前置必须附现有产物立即可验证的自证步骤**(连续第二次被现实打回后的硬要求)、最小化「先建再推翻」。不看 v1 面子与沉没成本。

**证据核验结论**:hand-back 13 的事实层**全部属实**——briefing 2150 字节零引用 token(我逐字读过:叙事+3 切片纯散文);`TimeSlice`/`DisplacementNarrative` 无 source 回链(domain L89-210);gate.py:219 注释原文在;`cli/reconstruct.py` 图空传;DAG 链 `T004-A1→T010/T011→T012→T020→T021→T022` 与 T011/T021 frontmatter 一致;`src/radar/{graph,evidence,journal}` 不存在。循环依赖成立。

## §1 · 现状摘要(按 Y 视角)

**架构设计**:核心病灶比 hand-back 表述的还深一层——v1 verdict 的 ① 原文是「**每条位移判断/边**带 source trace」,但在 T010/T011 解锁时点,「判断」(Judgment)是 T020 产物、「边」(GraphEdge)是 T011 产物,**两者在该边界上结构性不存在**。即 v1 把一个 **Phase 2 形状的验收**绑到了 **P0.1→Phase 1 的解锁点**上——不只是「底料被 gate 挡在下游」,而是检查项的谓词对象在该时点无定义。这给出两条对称解法:把底料前移(a1),或**把检查项后移到底料天然存在的位置**(①② 重绑为 Phase 2 出口验收——T021 验收测名字面就是 ①②:`should_link_each_judgment_to_source_within_3_hops` / `should_resolve_source_ref_to_real_retrieved_document`,T021.md:40)。后者是 hand-back a3 的架构化表述。另一关键发现:**gate.py 自己已点名 a1 是它想要的能力**——round-7 拒 doc 锚的注释写明「本 run 无 per-slice source 映射可信……未来 per-slice source 映射落地后可改回」(gate.py:213-214)。即 build 侧代码在 forge v1 之前就独立识别了同一缺口,a1(per-slice source 映射)不是 forge 外加的发明,是管线自证的最小缺件。其实现面小:`Paper.source_ref` 已有(retrieval 层),丢失点单一(reconstructor.py 只回写 structural_state);但 `TimeSlice` 是 T001 冻结 domain,加字段=契约变更,须 forge 授权(同 KG-B5 先例)且须审 RT-2 边界——「保留 P0.1 已有的 provenance」与「偷建 Phase 1 图」在我初判里是两回事,前者不违 RT-2 原意,待对方与 spec 原文校验。

**工程纪律**:双道 STOP 在本次事件里的表现值得记录:治理道**第三次正确运转**(首跑 FAIL→形态拒签→本次可判性 STOP),且这次是 **verdict 自带的自证前置**挡下了过度投资——K 要求的「新前置附自证步骤」在 v1 已有雏形(§underweights 建议真跑),v2 应把它**从建议升级为结构强制**:任何解锁谓词必须同时交付「对既有真产物跑一次」的可执行验证。KG-B4 的改写(wire 机器道 STOP 到三项)在 ①② 无底料时确实悬空一半——但注意 ③+「slice 源映射存在性」这类检查的 wiring 对象是**文件级 artifact**,秒级可判且底料在 a1 后存在,B4 的 wiring 路线本身不必推翻,只需换绑定对象。

**产品价值**:operator 的一贯立场(hand-back 11 三条批评 + injection 双锚 O2+O7)是「边用边抽查」。①② 若重绑为 Phase 2 出口验收 + 使用期抽查对象,恰好落在 operator 真实工作流上:briefing 产出时机器验 trace 完整(那时有 Judgment/证据链),operator 用时抽查。「解锁前置」位置上留下的应是**该边界真能判的最小集**,而非把全部信任检查堆在最早闸口——这与 v1 已裁的「识伪零解锁语义」同构。

## §2 · First-take 评分

- **v1 verdict「三项作 T010/T011 解锁前置」整体** → **refactor**:方向(机器判、退役人肉签字)保留;①② 绑定位置错(Phase 2 谓词绑 Phase 0 边界),须重绑。
- **①②(trace 完整性/3 击可达)** → **refactor(a3 为主 + a1 为底料)**:重绑为 T021/T022 的 ship 验收(它们字面就是 T021 验收测)+ O2/O7 使用期抽查对象;**不作** T010/T011 解锁前置。
- **a1(per-slice source 映射最小前移)** → **new(采,窄授权)**:仅「slice→source refs 保留」,不建图不做 judge;gate.py 注释自证其为管线缺件;须 forge 授权动冻结 domain + 确认不违 RT-2。
- **③(轻量审计通道)** → **keep(作解锁前置之一)**:配 a1 后非空壳——通道里有 slice 源映射可查。
- **T010/T011 新解锁前置(B 议题)** → **new**:= 「a1 落地(briefing 带 per-slice source 映射,机器可验存在性+可解析性)+ ③ 结构就位 + 治理道畅通」;每项附对真产物的自证步骤(K 硬要求)。
- **KG-B4 改写** → **refactor**:wiring 路线保留,绑定对象从「三项」改为上行新前置的文件级 artifact(C 议题:先 B9 定底料位置,B4 跟着绑)。
- **KG-B7 冻结 / 识伪零解锁语义 / 双道 STOP** → **keep**(v1 已裁,本次无新证据推翻)。
- **「先只启 ③ 空壳」的 a2 原样** → **cut**:hand-back 自己已证 ③ 无 trace 是空壳;a2 只作为 a1 的排序表述有意义。

## §3 · 我现在最不确定的 3 件事

1. **RT-2 原文边界**:「P0.1 不偷建 Phase 1」的 spec 原文(spec.md §5/RT-2)不在本次 X 中——a1 的「provenance 保留 ≠ 偷建图」论证依赖其确切措辞,若 RT-2 写死「P0.1 产物不得含图侧锚」则 a1 需更窄化。
2. **a1 的真实代价**:动冻结 `TimeSlice`(频改面:slicer/reconstructor/writer/gate/injector 全消费它)的连锁面我未逐一枚举——forge-lite 教训(枚举消费面,序列化面最易 silent 丢)提示这里可能不止 S 级。
3. **解锁时机**:operator 是否接受「T010/T011 等 a1 落地后解锁」(再多一个 build 周期)vs「立即解锁 + 使用期兜底」——这是 B 议题里唯一非技术判断,P3 须显式摆给 operator。
