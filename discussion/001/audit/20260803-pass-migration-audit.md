---
doc_type: pass-migration-audit
discussion_id: "001"
prd_fork_id: 001-radar-pA
audit_id: 001-radar-pA-pass-migration-20260803
created: 2026-08-03T12:55:00Z
performed_by: Claude Opus 5(IDS session · /expert-forge 001 v6 → Decision menu [A] ★1)
mandated_by: discussion/001/forge/v6/stage-forge-001-v6.md · Decision list #5 · [A] 执行顺序 ★1
result: ZERO_AFFECTED
operator_signoff: PENDING
operator_signoff_at: null
---

# 零受影响 PASS 核查记录 · 001-radar-pA

> **为什么存在这份文件**:forge 001 v6 verdict 第 5 行裁定 ——
> **「零受影响是核查结果,不是默认值」**。若不先清点就把追溯规则写进 spec,
> 「迁移表为零」就是**靠沉默推断**,而那正是本轮明令禁止的那件事。
> 本文件是 v0.8 amendment 的**必带附件**:缺此件,amendment 不予验收。

## §1 核查范围(什么算「受影响的已放行结论」)

forge v6 裁定池键将改为 `decision_epoch + rubric + comparability_class`,
且 `direction` 退出去重计数。**受影响 = 任何依据旧池语义(`epoch + rubric` 分区 ·
`claim + direction` 去重)作出并被下游消费的 O2 或 §7-P2 `PASS` 结论。**

**明确不在范围内**:T010/T011 的 a1 解锁自证(`predicate_passed`)—— 它是
**a1 单一谓词**(映射可解析 + 审计通道就位 + 命名一致),与 O2 证据链抽样是两条独立判据链。
理由见 §3-C。

## §2 核查方法(可复现 · 命令逐条列出)

核查时间 2026-08-03,对象为 **两个 checkout**(权威副本 = worktree):

```bash
W=/home/ys/codes/XenoDev/.claude/worktrees/001-radar-pA/projects/001-radar-pA
M=/home/ys/codes/XenoDev/projects/001-radar-pA

# 1 · 枚举全部产物目录
ls -la $W/out/{briefing,journal,credibility,reconstruct}/
ls -la $M/out/{briefing,journal,credibility,reconstruct}/

# 2 · 全产物扫 PASS 声称
rg -n 'PASS|"o2"|"p2"|O2|P2|INSUFFICIENT|非豁免' $W/out/
rg -n 'PASS|不得据以判|非豁免' $M/out/

# 3 · journal 行数
wc -l < $W/out/journal/evaluations.jsonl     # → 1

# 4 · 池化是否实装(结构性检验 · 见 §3-D)
rg -c 'pool|epoch|rubric|comparability' $W/src/

# 5 · 全 worktree 找其它 jsonl 记录面
find /home/ys/codes/XenoDev/.claude/worktrees/001-radar-pA -name '*.jsonl'
```

## §3 核查结果

### A · worktree(权威副本)

| 位置 | 内容 | 是否含 O2/P2 PASS |
|---|---|---|
| `out/briefing/` | `coding-llms-20260802T022608Z.md` **1 份** | ❌ **产物自我否认** |
| `out/journal/evaluations.jsonl` | **1 行**(coding LLMs · 观望 · `decision_delta: true`) | ❌ 内嵌同一份否认 |
| `out/journal/a1-selfcheck.jsonl` | 1 行 · `predicate_passed: true` | ⚠ **不在范围**(见 C) |
| `out/credibility/` | answer-key + runbinding + `diffusion-models-20260718T231343Z.audit.json` | ❌ 无 |
| `out/reconstruct/` | 2 份 `diffusion-models` 产物 | ❌ 无(`O2 可解析真原文` 是 source-ref 标签,非 verdict) |

⭐ **关键证据 —— 唯一那份真 evaluate 产物是「自我否认 PASS」的**,逐字三处:
- `:22` 「**非豁免判断**:1 条(抽样下界:3)」
- `:25` 「⚠ **非豁免判断 1 条 < 抽样下界 3** —— 按 spec §1-O2 (c),本份 briefing
  **不得据以判 O2 / §7-P2 PASS**。」
- `:43-46` 「⚠ **P2 判据边界**:`evaluate ... && ls out/briefing/*.md` 命令成功 **≠**
  spec §7-P2 PASS…**不宣称 P2 整体已绿**。」

⇒ 该产物**不仅没有声称 PASS,而且主动写明了它不能被当作 PASS 用**。

### B · main checkout(非权威,一并核以求完备)

- `out/briefing/` **空** —— main checkout **一份 evaluate briefing 都没有**
- `out/journal/` **只有** `a1-selfcheck.jsonl`,**无** `evaluations.jsonl`
- `out/credibility/` `out/reconstruct/` 为 07-13/07-18 的校准与 reconstruct 产物
- 全目录扫 PASS,**唯一命中仍是 a1-selfcheck**(见 C)

### C · `a1-selfcheck.jsonl` 的 `predicate_passed: true` 为何不在范围内

该行 `reason` 字段逐字为:
> 「**PASS:a1 单一谓词三件满足(映射可解析 + 审计通道就位 + 命名一致)—— 结构谓词就绪**」

⇒ 它是 **T010/T011 的解锁谓词**(forge v2/v3/v4 裁定的 a1 链),判据是
**结构谓词**(structure / resolvable / coverage / naming 四件,该行 `checks` 字段可见),
**与 O2 的「证据链 3 击 + 非豁免判断抽样」完全不同的判据链**。
把它算作「受影响 PASS」是**判据链混淆**。
(此结论与 GPT P2 §2 独立一致 —— 见 §5。)

### D · ⭐ 结构性论证:即使有 PASS,也不可能来自旧池

前三节是**枚举法**(查了没有)。本节给**结构法**(不可能有),两者独立:

`rg -c 'pool|epoch|rubric|comparability' $W/src/` 全 `src/` 树**仅 2 处命中**,
且均在 `lifecycle/ephemeral.py` 的**注释**里,内容是 **`corpus pool` / `corpus_pool.py`**
—— 指**检索语料复用**(C9 生命周期议题),**与 O2 判断池毫无关系**。

⇒ **O2 判断池(跨 run 累积 · epoch/rubric 分区 · claim+direction 去重)在
`src/` 中从未实装**,无任何持久化落点。
⇒ **任何 O2/P2 PASS 都不可能是"借旧池"得来的** —— 池根本不存在。
⇒ 这与 HANDBACK-LOG 决议 40 (4) 记录的 spec-task 同步缺口一致:
**机器侧跑的仍是 v0.6 单 run 语义,v0.7 池化只在规范层生效。**

## §4 结论

> **迁移表 = 零项。零真实 O2/P2 `PASS` 结论存在,亦无任何下游消费面。**

**双重证据**:枚举法(§3-A/B 两个 checkout 全产物扫描)+ 结构法(§3-D 池从未实装)。
两者独立成立,任一单独也足以支撑结论。

⇒ **forge v6 verdict 第 5 行成立**:现在落追溯规则的迁移成本为零,**这是本轮立规则最便宜的时点**。

## §5 独立性声明(本记录的证据强度)

本核查是**第二次独立核查**:
- **第一次**:GPT-5.5 xHigh 于 forge v6 **P2 §2** 自行仓内实查(`discussion/001/forge/v6/P2-GPT55xHigh.md`),
  结论「未发现真实 O2/P2 PASS 被旧池消费」。
- **第二次(本记录)**:Claude Opus 5 于 2026-08-03 独立重跑,**未采信上述结论**,
  命令与范围自行确定。

**本次相对第一次的增量**:① 明确覆盖 **main checkout**(第一次表述为「worktree 与主副本」但未列细目);
② 给出 **§3-D 结构性论证**(池从未实装 ⇒ 不可能有池 PASS),这是**枚举法之外的独立路径**,
第一次未给;③ 逐字引出产物**自我否认 PASS** 的三处原文。

⚠ **诚实边界**:两次核查**都由 AI agent 执行**,均未经第三方人工复核。
按 forge v6 verdict #6 的 chair 条款,**本记录的效力以 operator 签收为准**。

## §6 会推翻本结论的情形(证伪条件 · 预先写死)

任一成立即本记录作废并**触发 forge v7**(v6 §underweights-9 判据 1):
1. 在**本记录未枚举的位置**发现 evaluate 产物或 journal 行(如 operator 本地未提交的 `out/`、
   已删除但可从 git 历史恢复的产物、其它机器上的副本);
2. 发现**任何**声称 O2 或 §7-P2 `PASS` 的记录(无论其判据是否为池化);
3. `src/` 中被发现存在**本记录未识别的**判断池持久化实装。

## §7 Operator 签收

> forge v6 verdict #5 fallback 明定:**「谁」= 执行核查的 agent(记名)+ operator 签收**;
> **「何时」= v0.8 amendment 提交前**。本记录为 amendment 必带附件,**缺签收不予验收**。

- [ ] **operator 签收**:我已阅读本记录,确认其范围与方法,采纳「迁移表 = 零项」结论
- 签收时间:______
- 备注:______
