# Forge v4 · 008 · P3R2 · Opus47Max · 联合收敛 R2(finalize)

**Timestamp**: 2026-06-30T10:40:00Z
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: strong-converge(从 forge-config 读)

## 1. 我对每条分歧的最终立场 + 让步

- **分歧 1 · 用途定义颗粒度**:
  - 对方在 P3R1 给的论证:"机器跟单 = spike hypothesis,不能写成当前产品目标"+「最终 verdict 用『候选目标/验证门』表述跟单,避免 build runtime 误读成要直接实现信号产品」→ **接受**。
  - 我的最终立场:现在定 008↔004 消费契约的**两层**——「自己回看检索 + 给 004 的可溯源证据契约」= 无悔下游(now);「机器可信跟单」= **候选目标 · gated 在 spike 验证门后**,PRD 用「候选/验证门」措辞写死,不写成当前产品目标。
  - 让步给对方的部分:采纳对方更强的措辞约束——不仅「gated」,且 PRD 文字必须显式标「build runtime 不得据此自行实现信号产品」(把防 V4 写进 PRD 本体,不只留在 forge 决议)。

- **分歧 2 · spike 通过门槛怎么写**:
  - 对方在 P3R1 给的论证:"把 spike pass/fail 先定为『产生可决策证据』,而不是现在拍一个固定百分比;门槛数值给 operator 在 W 中选择" → **接受,并认定比我的原案更好**。
  - 我的最终立场:spike 的 pass 条件 = **产生 decision-grade 证据**(分层报:stance/conviction/action × 反讽/非反讽子集 × high-confidence 子集,且 false-positive signal 列一等风险),**不由 forge 拍固定百分比**;具体置信度门槛由 operator 看到分层数字后定。
  - 让步给对方的部分:撤回我 P3R1「门槛由 operator 据代价不对称定」里隐含的「forge 先给倾向值」,改为 forge 只定**证据形状**、数值全留 operator。

- **分歧 3 · KG-24/KG-25 在最终产物里的权重**:
  - 对方在 P3R1 给的论证:"KG 作为工程纪律附带必修项,而非 v4 的主判题" → **接受**(我 P3R1 立场本就一致)。
  - 我的最终立场:KG-24(抽 manifest 状态单一契约)/ KG-25(constrained-output 或 清洗+鲁棒提取+降级+可见告警)进 decision-list + next-dev-plan,**作为框架可靠性附带必修**,不喧宾夺主于产品 verdict;实装留 XenoDev,forge 只列 decision + 候选解。
  - 让步给对方的部分:无(双方一致)。

## 2. 联合 verdict(单一)

**GO · 用途锚定 + 可靠性前置的 gated refactor。** v4 推进三件事,不多做:

**①** 现在把 008↔004 消费契约写进 PRD,分两层:**无悔下游**(operator 自己回看检索 + 给 004 的「可溯源证据 + 置信度」契约)立即成立;**机器可信跟单信号** = 候选目标,**gated 在信号可靠性 spike 验证门之后**,PRD 用「候选/验证门」措辞并显式标注「build runtime 不得据此自行实现信号产品」(防 V4 写进 PRD 本体)。

**②** 信号可靠性 spike 列为 PRD 工作项、且是跟单候选的**硬前置**:XenoDev 跑小样本,**分层报**(stance/conviction/action × 反讽/非反讽子集 × high-confidence 子集,false-positive signal 为一等风险)。spike 的 pass 条件 = 产生 decision-grade 证据,**不由 forge 拍固定百分比**;置信度门槛由 operator 看分层数字后定。

**③** 字典第 1 层无悔(asker bug / entity_type 板块黑洞 / tech_side 三值 / 黑话词典)立即落地,**不等 spike**;第 2/3 层 gated 在「用途确定 + spike 通过」。边界硬约束:008 只产**可溯源结构化 + 置信度**(C5/C9 内),信号决策归 004,不越界。KG-24/KG-25 作框架可靠性附带必修入 W,实装留 XenoDev。

**无 unresolved。** 双方 P1→P3R1 四维同向,R2 后三条分歧全部按对方更优措辞收敛。

## 3. 残余分歧降级为 v0.2 note

- v0.2 note 1:**spike 之后**——若 spike 显示反讽子集 stance 准确率确实低,需回头决议「是否对反讽密集内容只存原文+不提信号字段」(分内容类型差异化提取)。何时回看:spike 出数字后。
- v0.2 note 2:**entity_type vs asker 优先级**——红队把 asker 降为「搭便车字段」,真硬的是 entity_type;第 1 层落地时若资源紧,先 entity_type 后 asker。何时回看:第 1 层 build 排期时。
- v0.2 note 3:**KG-25 根治路径选型**——constrained decoding(DeepSeek 是否支持待 L4 验)vs 清洗+鲁棒提取+降级;两条都列,L4 实测后定。何时回看:XenoDev 修 KG-25 时。

## 4. W 形态产出的初步草稿建议

- **W 含 next-PRD draft → 关键产品决策点(3 条)**:
  1. 008↔004 消费契约成节:定义 004 消费的「可溯源证据 + 置信度」字段集(替代现「轻量粗约定」);
  2. 新增 US/Scope 表述:「机器可信跟单信号」= 候选目标 gated 在 spike 门,显式标 build-runtime 不得自行实现;
  3. Scope OUT / C9 澄清:008 产可溯源结构化+置信度 ≠ 产信号;stance/conviction/action 作「顾问原话的可溯源结构化」存(谁说/原话/置信度),不作系统判方向。

- **W 含 decision-list → 4 列矩阵(列前 5 条)**:
  - **保留**:SQLite SSOT + 三护栏 / C5/C9 可溯源红线 / 字典第 1 层无悔字段 / v3 凭据隔离 broker 架构 / 现采集稳定性 gate。
  - **调整**:008↔004 出口从「轻量粗约定」→「可溯源证据 + 置信度契约」;字典第 2/3 层从「悬空」→「gated 在用途+spike」;Phase gate 增「信号 spike 通过」为跟单候选前置。
  - **删除**:「机器可信跟单 = 当前产品目标」这一(未明说但 operator 倾向里隐含的)定位 → 降为候选;无悔层里被红队踢出的 conviction/stance/author_tone「当前就提」的预设。
  - **新增**:信号可靠性 spike(PRD 工作项)/ 008↔004 消费契约节 / 防 V4 的「build-runtime 不得自行定信号产品」PRD 条款 / KG-24 状态契约 / KG-25 输出鲁棒层。

- **W 含 next-dev-plan → 关键 milestone(3 条)**:
  1. **M1 · 字典第 1 层无悔落地**(不等 spike):entity_type + tech_side 三值 + 黑话词典 + asker/双时间戳 bug 修;
  2. **M2 · 信号可靠性 spike**:小样本(~100-200 条)分层测 stance/conviction/action,产 decision-grade 证据报告(分反讽/非反讽 + high-confidence 子集 + FP-signal 风险),operator 据此定跟单 go/no-go + 置信度门槛;
  3. **M3 · KG 框架修**(并行可做):KG-24 manifest 状态单一契约 + KG-25 输出鲁棒层(清洗/降级/可见告警,或 constrained decoding 待验)。
