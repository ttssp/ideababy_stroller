# XenoDev-009 启动 prompt · forge v4 落地 B/C 两组

> **用法**:在 XenoDev-009 session 的**第一条消息**里贴下面「启动 prompt」整段(或让 agent 读本文件全文)。
> 本文件是 **IDS 侧产物**(forge v4 的落地指令),XenoDev 侧只读不改。

---

## 启动 prompt(从这里开始复制)

你在 `XenoDev-009` build runtime,分支 `feat/009-spec`。本次任务 = 落地 **IDS forge 009-pM3prime v4 verdict** 的
**B 组(记账/可观测性)+ C 组(C4 三处同步)的 XenoDev 侧部分**。

### 授权来源(**不重开已决问题,逐条照做 —— 这是本次的合同**)

1. `/home/ys/codes/ideababy_stroller/discussion/009/009-pM3prime/forge/v4/stage-forge-009-pM3prime-v4.md`
   —— **先通读**。重点 §Verdict / §Decision matrix / §Refactor plan / §What this menu underweights
2. `/home/ys/codes/ideababy_stroller/framework/obligations/ledger.jsonl`
   —— 读 `OB-009-pM3prime-v4-02` / `-03` / `-06` / `-07` / `-08` 五行(**兑现判据写在各自 note 里,逐条照做**)
3. `/home/ys/codes/ideababy_stroller/discussion/009/009-pM3prime/PRD.md` **v1.1**
   —— §7 红线 3 的「`convert` 判据形态定形」块 + §6 科学重判条件 1 的「未满足注记」

⚠ **IDS 已裁决的事不要重新论证**;若你认为某条裁决有问题,**记 hand-back 交回 IDS,不要当场改**。

### 交付物(四项 · 顺序不硬,但 ① 是最大的一项)

**① `OB-009-pM3prime-v4-03` —— `extraction_attempt_log` 的四前提(A + 判据 + 证不出则 B)**

目标不是「实现写穿透」,是**证明或证否四个前提**。四前提合取:

1. **预注册观察/停止边界** —— 观察窗口与停止规则在**看数之前**固定;
2. **逐 attempt exposure 可计** —— 每次 LLM 调用的暴露量可从库里算出(risk-set 可构造);
3. **已观察失败的结果 + 精确时间/区间留存,且删失可识别** —— 即能区分「失败了并记下了何时失败」
   与「进程死了所以不知道」,后者必须**显式标为删失**而不是缺行;
4. **失败批次内容身份可比** —— 失败批次也能绑定语料内容哈希,使跨批次比较的是同一份输入。

- **四者都能证 ⇒ 保持现有批量落库形态**,把四前提各自的证据落成可 `SELECT` 的字段/测试;
- **任一证不出 ⇒ fallback**:改写穿透(每次 API 响应立即落库)**或等价耐久回执**。
- ⚠ **fallback 是契约预置的分支,不是失败**。选了哪条、为什么,写进 task 卡与 hand-back。

**病灶面**:`projects/004-pB/src/decision_ledger/extraction/census.py` 的 `_persist_attempt_log`
(约 :714-740)与 `CensusReport.attempt_log_persist_failed`(约 :168-177)。

⚠ **两条必须带进设计的既有事实**(IDS 已实读复核):
- `_persist_attempt_log` docstring 自陈本表存在的理由就是**跨批次比对**
  (「RETRY-CONTRACT §2 主判据是……跨批次比对」「**不做这条,前面全是空话**」)——
  **这是本条判据的本地唯一来源**,SOTA 不提供(IDS P2 检索为否定性结果);
- `attempt_log_persist_failed` 是 round-7 为**同一风险类**加的告警,但它**在 SIGKILL 场景结构上无法开火**
  (它是 run 正常返回时才打的标)⇒ **为「不自知」而设的告警,恰在该场景静默**。第 3 前提要正面解决这一点。

**② `OB-009-pM3prime-v4-08` —— `SLA.md:136` 判据列补「跨次一致性读数**存在性**」判据**

`specs/009-pM3prime/SLA.md` 提取稳定性行:**目标**列要求「每批普查产**可复核的跨次一致性读数** +
语料内容哈希四元组 + 身份字段」,而**判据**列的两条 SQL 只验 ① `trial_ledger` 四元组恒非空
② `extraction_attempt_log` 每次 LLM 调用一行 —— **没有任何一条验证「跨次一致性读数」存在**。

⇒ 补一条可 `SELECT` 的存在性判据。**四个「必须」里最核心的「必须测」目前零判据**,
这与它要替换掉的 C4 假绿是同一形状(目标列陈述要求,判据列验证更弱的东西)。

**③ `OB-009-pM3prime-v4-06` + `-07` —— C4 三处同步的 XenoDev 侧两处**

把下面两条**逐字同步**进 `specs/009-pM3prime/spec.md` 的 C4 与 `SLA.md` 的 E1「提取确定性」行
(IDS `PRD.md` §7 红线 3 已于 2026-08-14 落地,是三处中的第一处):

- **`convert` 判据 = 过程证据 + 结果证据 + 具名批准 + 版本化回退,四者合取,不给数字。**
  (过程证据 = 真实观察期且期内审阅过真实误杀;结果证据 = per-market 噪声量级 < 该市场密度阈值裕度;
  具名批准 = 具名主体签署,不得由自动化流程或 agent 认定;版本化回退 = 见下。)
- **版本化回退语义 = 历史不可变;授权被后续 `caliber_version` supersede。**
  回退 = 再升一个新 `caliber_version`,**只撤销旧版未来消费权**,旧阈值/旧证据/当时裁决永久保留可查。
  🔴 **不得**写成「旧结论作废」——那暗示追改历史,违反 C6。
- `WARN-c4-extraction-stability-report-only` 的 `due_event` 已由 `forge:009-pM3prime:phase0`
  **改指 `forge:006:phase0`**(2026-08-14 三态裁决 = defer)。若 XenoDev 侧文档引用了旧值,一并更正。

**④ `OB-009-pM3prime-v4-02` 的未完成部分 —— 查证 M1=pass 裁决是否需同步进 XenoDev 侧文档**

IDS 已在 `PRD.md` v1.1 载明该裁决;**XenoDev 侧 `spec.md` / `SLA.md` 是否需同步,IDS 本轮未查证**。
请查证并给结论(需要同步 ⇒ 同步;不需要 ⇒ 说明理由)。裁决内容与两项必载风险输入:

> 接受 M1 为**固定批可比性**证据(NIST:统计控制「can only guarantee comparability among measurements」)·
> 不作效度代理 · 不外推 · **不解锁扩样与 E2**。
> 两项必载风险输入:(i) 一致率上升**无法区分**噪声去除与**歧义抹除**
> (「filtering non-consensus samples results in over-optimistic results」逐字对应 M2 留存口径);
> (ii) 6 个跑的 `census_verdict` **全部** `below_threshold_advisory`。

### 冻结项(**不许动**)

- 扩样与 **E2 继续 blocked**;`M1 = pass` **不解锁**
- **41 条盲标路 v0.1 CLOSED**,不重开
- **C6 冻结门槛数字**不动(本轮只议其形态中的可回退性)· `caliber_hash` / `threshold_hash` / `density_threshold` 不动
- 红线 4(第二源资格)不动 · `gold_layer2.py` 的 `second_source_kind != 'human'` 硬挡不动
- **不改 IDS 仓任何文件**(有意见走 hand-back)

### 验收

- `cd projects/004-pB && uv run pytest` —— 全量回归绿,**0 回归**(当前基线 **1287 passed / 7 skipped / 1 xfailed**,
  IDS 于 2026-08-14 实跑复证过该基线)
- `uv run ruff check <改动文件>` —— clean
- 四项交付物各自的兑现判据(见 ledger 各行 note)逐条可 `SELECT` 或可 `pytest` 验证
- codex adversarial-review(`risk_level: high`);**真路径**,非 fallback

### hand-back 要求(**两条容易漏的,本次必须做到**)

1. 🔴 **frontmatter 必须含拓扑自证三字段** `current_idea` / `worktree` / `baseline` ——
   最近**两个** hand-back 包都全缺,导致 validator 的 check-7 静默 skip 并输出一句**假陈述**
   (对 08-13 的包说「2026-08-10 前的老包属正常」)。这是 **KG-B21**,producer `gen-handback.sh` 未修,
   **请手工补齐**。
2. 🔴 **`ids_verdict_evidence` 父键必须产出**,且 `review_log_path` / `review_log_sha256` 与
   `.claude/skills/codex-review/REVIEW-LOG.md` singleton 及 immutable `real-review/` 记录**三处一致**。
   这是 **KG-B20**,T015 那次已经做对了,**本次保持**,不要退回。
3. §3 建议里请分别标注:哪几条是**要 IDS 决议**的,哪几条是**信息式收悉**的。

### 已知陷阱

- 真实验若涉及 LLM:`env -u ALL_PROXY -u all_proxy`(runbook 记录的 SOCKS 代理坑)
- validator 必须传**绝对路径**(相对路径会误判 corruption)
- 本次**不需要**跑真实验;四项交付物都是代码/契约/文档层

## 启动 prompt(到这里结束)

---

## Operator 执行命令

```bash
cd /home/ys/codes/XenoDev-009 && claude
```

首条消息:

```
读 /home/ys/codes/ideababy_stroller/discussion/009/009-pM3prime/forge/v4/XENODEV-startup-v4-BC.md
的「启动 prompt」整段,按它执行。
```

⚠ **worktree 规约**:`XenoDev-009` 已是 009 专用 checkout(分支 `feat/009-spec`),
**不需要**再 `claude -w`;直提交到 `feat/009-spec` 是本 fork 既有惯例(非 worktree+squash 流程)。
