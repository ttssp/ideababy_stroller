---
doc_type: contract-audit
fork_id: 009-pM3prime
created: 2026-08-13
trigger: forge v3 §underweights 第 2 条 · operator 选 Decision menu [B]
closes: OB-009-pM3prime-v3-12
verdict: C4 是孤例(未发现第二例);另发现一条独立的交叉引用缺口
---

# Hard 契约「恒真替身」普查 · 009-pM3prime

**问题**:forge v3 发现 spec C4「同文同版必同输出」的验收测试把 proposer 换成了
`literal_ticker_proposer`(构造上确定)⇒ 一条 Hard 100% 要求的验收物是**恒真的**。
**本次普查问的是:这是孤例,还是验收体系性失效?**

## 判据(先声明,防事后挪)

对每条 Hard 契约问同一个问题:

> **该属性的责任方是谁?测试是否把责任方换成了「必然满足该属性」的替身?**

⚠ **关键区分**(不做这个区分会大量误报):
**用测试替身喂输入是正当的**,只有当**被测属性本身是替身的属性**时,替换才使命题恒真。
- C4:被测属性 =「**proposer 的输出**是否稳定」,而 proposer 被换成确定性替身 ⇒ **恒真 · 有病**
- C2:被测属性 =「**`extract()`** 是否守 PIT」,proposer 只是喂候选的 fixture ⇒ **正当 · 无病**

## 结果:**C4 是孤例**

| 契约 | 责任方 | 测试是否换掉了责任方 | 判定 |
|---|---|---|---|
| **C4** 提取确定性 | LLM proposer | 🔴 **是** —— 换成 `literal_ticker_proposer`;另一半 `test_should_call_deepseek_with_temperature_zero_and_json_mode` 只断言**参数被传给 API** | 🔴 **恒真** |
| C2 文本 PIT | `extract()` 的时间比较 | 否。且有**真 mutation-killer**;更强的是 `census.py` 的 `_V2_FORBIDDEN_FIELDS` 禁止 LLM 携带 `content_published_at`(产线路径**不能**像测试替身那样绕过守门) | ✅ 干净 |
| C3 引文锚定 | `anchoring.py` + `extract()` | 否。**且覆盖了 v2 产线路径** —— `test_citation_slice_equals_llm_quote_for_exact_tier` / `..._normalizes_to_llm_quote_for_normalized_tier` 直接用 `ProposedSpan(quote=...)` 走 quote→anchor;`test_anchoring.py` 另有 31 个测试 | ✅ 干净 |
| C5 金标 gate | `gate.assert_gold_passed` + `gold_layer2` | 否,**而且是本仓的正面样板**:正例必须 `monkeypatch` 常量 `_CORRECTNESS_GATE_AUTHORIZED_V0_1`,测试 docstring 自陈「这本身就说明 v0.1 生产链路开不了这道门」;另有 `test_gate_blocks_when_db_self_signed_but_code_authorization_false`(库侧自签**不能**绕过代码常量) | ✅ 干净(样板) |
| C1 trial-ledger 完整性 | SQL 记账 | 否(真 sqlite conn · 缺行 block / 齐全 pass / marker 行排除 三例齐) | ✅ 干净(**但 grain 问题另计** —— 见 v3 v0.2 note 2:测试只能测 grain 表达得出的东西) |
| C6 预注册不可回改 | SQL 约束 | 否(`test_threshold_immutable_after_census` + `test_threshold_change_only_via_new_caliber_version`,真 conn) | ✅ 干净 |
| C9 第二源红线 | `evaluate_layer2` guard | 否(`second_source_kind="llm"` 拒 / `"human"` 过,真 DB) | ✅ 干净 |
| C12 窗口纪律(防抄考卷) | `is_in_oos_window` 纯函数 | 否。边界 / 字面冻结 / **真实 UTC 日跨时区**(修过一个 MED#3 真 bug)三类齐;**且 `census.py:592` 真消费它** | ✅ 干净 |
| C10 008/raw 只读 | SQLite 引擎 | 不适用 —— **结构强制**:`sqlite3.connect(f"file:{path}?mode=ro", uri=True)`,任何写在引擎层抛错。**比测试更强** | ✅ 干净 |
| C7 / C8 / C11 / C13 | migration / rejection taxonomy / 栈链 / 凭据隔离 | 否(各有真测试:`migration_0017_adds_only_no_004_mutation` · 11 个 caliber 测 · 真 `alembic upgrade head` · `not_log_key_value` + `not_leak_key_in_sanitized_exc`) | ✅ 干净 |

⇒ **verdict (b) 的范围不需要重划。** forge v3 的 decision matrix 按原样执行。

## 但普查带出一条独立的新缺口

**13 条 Hard 契约中,`C7 / C8 / C10 / C11 / C12 / C13` 六条在 spec 的 Outcome 表里零引用。**

```
O 表(含可执行验收命令的行)引用到的 C: C1 C2 C3 C4 C5 C6
spec 声明的全部 Hard C:              C1..C13(13 条)
⇒ 6 条 Hard 契约没有从 O 表指向它们的验收锚
```

⚠ **这不是效度缺口** —— 上表已逐条核实,这 6 条**都有真测试或结构强制**。
**这是交叉引用缺口**,后果是:

> **无法机械回答「每条 Hard 契约是否都有具名验收锚」** —— 必须逐条人工追溯。
> **而 C4 之所以能藏住,正是因为没人做过这次人工追溯。**

⇒ 本条作为**新议题**记入 forge v3 的 v0.2 note 邻域,归 `OB-009-pM3prime-v3-13`(新登记)。

## 🔴 落地时又挖出一条,比上面两条都重:**逃生舱被那个绿测试自己拆了**

改契约文本时做残留普查,在 **shipped 的 task 卡 `specs/009-pM3prime/tasks/T011.md`** 里读到:

> §Known gotchas:
> **「C4 是未证假说(G-R2):真 LLM 温度 0 同输出是否真成立 —— build 真跑才知 · 不成立 → 记 dogfood(触发 forge v6)。」**
>
> §实现步骤 2:
> 「`test_same_text_same_version_same_output`:同输入跑两次 extractor → 断言相等
> (温度 0 · **若真 LLM 不确定 → 记 dogfood G-R2**)。」

**⇒ 不是没人想到。有人想到了,给它起了名字(G-R2),写明「build 真跑才知」,还预置了逃生舱。**

而 **`dogfood-backlog.md` 里查无 `G-R2`**(整个 `G-R*` 系列一条都没有):

```
$ rg -n 'G-R2' dogfood-backlog.md   →  无命中
$ rg -no 'G-R[0-9]+' dogfood-backlog.md | sort -u  →  空
```

**逃生舱的触发条件是「测试不成立」,而测试用 `literal_ticker_proposer` 恒真 ⇒ 触发条件永远不发生。**

⇒ **那条绿测试干了两件事:①它没有检验该假说;②它同时压住了为「该假说不成立」而预置的告警机制。**
task 卡说「同输入跑两次 extractor」—— 字面被满足了(literal proposer 也是 extractor),
**精神丢了,而且是无声地丢的**。

**这条的性质与前两条不同**:前两条是 009 本地问题,**这条是框架级失败模式** ——
「预置逃生舱 + 逃生舱的触发条件由一个可被替身满足的测试决定」。
⇒ 归 **forge 006 攒批**(承 CLAUDE.md「框架级变更只走 forge」),登记为 `OB-009-pM3prime-v3-14`。

⚠ **未改 `T011.md`** —— 它是**已 ship 的 task 卡,是历史记录**,回改会篡改「当时做了什么」。
只引用,不修改。

## 本次普查的边界(诚实交代)

- **只查了「责任方被换成恒真替身」这一种病**。没查:测试是否覆盖了契约的**全部**语义、断言强度是否足够、是否存在死代码路径。
- **没跑测试**,只读代码与测试源码。若某测试实际是 skip / xfail,本普查看不出来。
  ⇒ 这一条可零成本补:`uv run pytest tests/contract tests/unit -q --collect-only` 后查 skip 标记。
- 成本:一次会话内的 `rg` + 人读,**零 API 调用、零测试执行**。
