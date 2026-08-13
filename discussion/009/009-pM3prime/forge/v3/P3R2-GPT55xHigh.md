# Forge v3 · 009-pM3prime · P3R2 · GPT-5.5 xHigh · 联合收敛 R2(finalize)

**Timestamp**: 2026-08-13T06:22:58Z
**Visibility**: 已读对方 P3R2。
**Convergence mode**: strong-converge。
**Searches used**: NONE。

## 1. 最终立场、让步与实验契约验收

- **分歧 4**：A 方承认“真信号留存”是范畴错误并改为候选留存，我全盘接受；效度铰链留作 v0.2。
- **分歧 1**：接受一次探针，但契约为 **accept-with-fixes**，修复前不得启动。
- **分歧 2**：收敛为 `pass_semantic: none`；report-only 是强制申报义务，不是门禁。
- **分歧 3**：收敛为执行态 `STOP`、认识态 `UNKNOWN` 双记；旧“真稀疏”作废。

逐条验收：① N=6 是两个 3-run 聚合的最小构造，但同一 102 条已被观察，只适合 fixed-batch 校准；不得外推到扩样语料，M1 pass 也不解锁扩样/E2。同批 `J_1` 作成对基线不天然循环，事后调规则才构成过拟合。另有硬冲突：6 次有效跑加最多 2 次补跑不是 N=6，且可达 4 h 40 min。须改为有效跑≤6、尝试≤8，3.5 h/$10 总帽优先；未凑齐即 indeterminate。② “将来由新脚本计算”不满足唯一命令；XenoDev task 必须先交付一个端到端入口及验收测试，再准运行。③ 比较型判据成功避开看过 0.44 后拍绝对阈值，但现写法不成立：应对同一 record resample 计算配对差值 `Δ=J_agg-J_1` 的 bootstrap CI，以 CI 全部大于/不大于/跨 0 判三态。N=6 只有一个 3-v-3 比较，不能 bootstrap run variance；record bootstrap 只支持本批推断。它不必然 indeterminate，但修正前无法声称有区分力。④ `(1-0.0017)^102≈84%`，再六次方约 35%，算术正确；独立同分布与 p 点估计未证实，只能作排程依据，重试义务仍由 SLA 与已见瞬态失败支持。⑤ 补齐结果矩阵：M1 fail/indeterminate 均起 forge v4；M1 pass 时无论 M2 高低都只证明本批信度改善，M2 全量申报，低于 50% 加注候选损失；任何组合都不证明效度、不解锁 E2。

## 2. 联合 verdict（单一）

E1 v0.1 路线保留，但单次输出立即失去事实地位，扩样与 E2 继续 blocked。先落实既有 SLA 的有界语义重试；C4 改为 `pass_semantic: none` 的强制测量、申报、落库与模型/语料身份绑定。CN/HK 保留执行态 STOP，认识态改 UNKNOWN，旧“真稀疏”作废。聚合探针仅在上述修复及端到端唯一命令验收后运行一次；固定有效跑≤6、尝试≤8、102 条、单跑≤35 分钟、总计≤3.5 小时且≤$10，总帽优先。任一硬帽先触发，或补跑后仍不足六个有效结果，整体记 indeterminate，禁止追跑且不得解释为成功。它以 record-level 配对 bootstrap 的 `Δ=J_agg-J_1` 判三态，只测本批跨次信度与候选留存；所有 M2 均申报。M1 fail/indeterminate 触发 forge v4；M1 pass 亦不代表效度成立、不能外推或解锁扩样。

## 3. 残余事项降级为 v0.2 note

1. validity 无真值锚，公开未解；不得把 M1 pass 改写为效度验证。
2. 校准周期、升版责任及 trial-ledger 新 grain 待单独设计，避免顺手改变 DSR/PBO 分母。
3. `_N_MAX=12` 顶满因果未测，可顺带观测但不得成为本探针判据。
4. A 方“三次被证据推翻”可作为 forge 机制过程注记纳入：它说明交叉裁决捕获了范畴替换；不得写进技术结论，也不能由单例泛化。

## 4. W 形态初步草稿

- **verdict-only**：采用 §2 原文，首句保留“单次输出立即失去事实地位”。
- **decision-list**：保留 E1 路线、KG-40、扩样/E2 blocked、41 条 CLOSED；调整 C4/SLA E1、确定性测试、PRD CN/HK 与 ledger 双态；删除“100% 同输出”门禁及“真稀疏”；新增语义重试、身份落库、端到端探针 task。每行写 obligation path，维持项填 `N/A`。
- **refactor-plan**：① `census.py` 重试和身份落库；② 同步 spec/SLA/PRD、测试语义与 ledger 双态；③ XenoDev 实现唯一入口、配对 Δ bootstrap、硬上限与结果矩阵，验收后运行一次。③ 依赖①，完成前不得扩样；ledger grain 与 `_N_MAX` 留 v0.2。

**P3R2 verdict：CONCERNS · converged。**
