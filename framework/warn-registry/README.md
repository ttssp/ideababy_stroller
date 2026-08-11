# Warn registry

> **状态**:v0.1 · 落地于 forge 006 **v10** 的 **[B] 止血核心**(2026-08-11)
> **权威裁决**:`discussion/006/forge/v10/stage-forge-006-v10.md`
> **结清的义务**:`OB-006-v10-01`(M1 · warn registry 载体 + `warn_class` schema 定形)

## 为什么存在

forge 006 v10 审「治理条款的可执行性 + 声明存在但机制不存在」两簇八条时,发现一条自指的事实:
**本仓面对「该不该硬拦」时的默认动作是「先 warn,附一条『复发 ≥N 次再说』」,而这个默认动作
本身没有任何后续边** —— 谁计数、在哪个 gate 上被读到、达成后谁执行,三个问题一个都没有答案。

实证:`CLAUDE.md` 的 worktree 规约判据**在第 2 次就达成,达成后仍复发到第 4 次**。

SOTA 给出的形状(RFC 1589 · 双侧独立取得):最成熟的 warn→error 治理**不用自动到期**,
它用的是 **① 固定节奏的复审 gate ② 每条 warn 一个具名 tracking 条目 ③ 到期必须作出三态裁决**。
PEP 387 再补一层:**并非所有 warn 都要升级** —— 永久 `defer` 完全合法,
**但必须显式标为 soft 并承认无移除计划**。

⇒ 真正的缺陷不是「warn 没有到期」,是 **「warn 从未被分型」**。

```
关键区分不是「自动 vs 手动」,
而是「被裁决出来的 defer」 vs 「被遗忘的 defer」。
```

## 与 `framework/obligations/` 的分层(**不要混成一层**)

| | `obligations/ledger.jsonl` | `warn-registry/registry.jsonl`(本目录) |
|---|---|---|
| 承载什么 | **裁决结果**(某件事该做、由谁、到哪个 gate 清偿) | **规则语义**(某条 warn 是哪一类、它的边在哪) |
| 形态 | **append-only 事件流**(同 id 取最后一行) | **当前态**(一条 warn 一行,就地编辑) |
| 审计 | 靠 append-only 本身 | 靠 git 历史 |
| 生命周期 | `pending → satisfied \| skipped`,终态后不再变 | 与 warn 同寿;`warn_class` 可经三态裁决改变 |

🔴 **v10 verdict 明写两层不得混**:`skipped` **只能关闭「升级义务」,不能表达 advisory 本身的
持续语义** —— 一个永久 soft advisory 不是「一次被签掉的义务」,它是一条持续有效的规则属性。
(把两者混成一层的冲动,forge 记录在案是 Opus 两次偏袒 v9 的同一根;见 v10 §underweights-2。)

## Schema(一行一条 JSON · **当前态 · 就地编辑**)

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | ★ | `WARN-<slug>`,**稳定不复用** |
| `title` | ★ | 一句话 |
| `site` | ★ | warn 的实际所在(`<path>:<line>` 或 `<path>`);validator 校验其存在 |
| `warn_class` | ★ | **`soft advisory`** 或 **`temporary`** |
| `declared_at` / `declared_by_gate` | ★ | 分型是在哪个 gate 上作出的 |
| `source` | ★ | 裁决出处 |
| **`soft advisory` 专属** | | |
| `no_upgrade_plan` | ⚠ | 必须 `true` —— **显式承认无升级计划**(承 PEP 387) |
| `rationale` | ⚠ | 为什么它永久是 advisory;**不得留白** |
| **`temporary` 专属** | | |
| `owner` | ⚠ | 具名主体 |
| `due_event` | ⚠ | **gate 事件**,不是次数、不是日期 |
| `consumer_gate` | ⚠ | 谁在 `due_event` 上消费它 |
| `consumer_wired` | ⚠ | 该消费点是否已接线 |
| `exposure` | ⚠ | `consumer_wired: false` 时必填 |
| `blocked_on` | | 可选:本条的裁决被哪条 obligation 前置阻塞 |

**🔴 `due_event` 不得是次数。**「复发 ≥N 次」不是升级机制 —— 无计数者、无消费点、无执行者。
v10 已把本仓现存三条这样的判据**全部作废**。

## 三态裁决(承 RFC 1589)

`temporary` 的 warn 到 `due_event` 时,**必须**作出三选一,**且 defer 必须被签出来**:

```
convert  → 升为 hard-fail(改 warn_class 为 n/a,warn 退出 registry)
revert   → 撤销该 warn(机制本身移除)
defer    → 合法!但必须:① 具名签署 ② 写明理由 ③ 给出新的 due_event
           —— 或改判为 soft advisory(此时必须补 no_upgrade_plan + rationale)
```

**被遗忘的 defer 不是 defer,是缺席。** 这是本 registry 存在的全部理由。

## 接线状态(v0.1 · [B] 止血核心)

| gate | 角色 | 状态 |
|---|---|---|
| `forge:<id>:phase4` | **admission** —— 拒绝缺 `warn_class` 的治理行 | ✅ **已接线**(`.claude/commands/expert-forge.md` Step 6.5) |
| `forge:<id>:phase0` | **consumption** —— `due_event` 到期的 warn 必须三态裁决 | ✅ **已接线**(同文件 Step 0.6 · **fail-closed**) |
| `xenodev:task-review` | admission(build 侧) | ❌ **未接线** —— 属 [A],本轮延后 |
| `xenodev:ship-gate` | admission(build 侧) | ❌ **未接线** —— 属 [A],本轮延后 |
| `xenodev:handoff-intake` | admission(跨仓) | ❌ **未接线** —— 属 [A],本轮延后 |

⇒ **本轮 [B] 只接了 IDS 侧两个 gate。** v10 verdict 正文的限定**仍然生效且必须被复述**:
**「此契约只有 M1 schema 与 M2 三处 hard-reject 均落地后才是机制;
此前不得宣称 build/mirror 已受保护。」**
`OB-006-v10-02` 保持 `pending`,会在下一次 `/expert-forge 006` 的 Phase 0 **持续阻断**,
直到 build 侧接线完成或 operator-chair 具名签 skip。**这是设计,不是遗留。**

## 已知局限(不得靠沉默推断)

1. 🔴 **枚举完备性是已知敞口**(承 v9 v0.2 note 2)。本 registry 只覆盖**被登记的** warn;
   **清单外的 warn 产生零约束**。validator **不声称**能自动发现未登记的 warn ——
   它只能校验已登记行的 schema 与 `site` 存在性。
   ⇒ 新增 warn 的拦截靠 **admission gate**(创建时拒绝未分型),不靠事后扫描。
2. 🔴 **admission gate 只覆盖 forge 治理行**。经由 build/mirror 路径新增的 warn
   在 `xenodev:*` 三个 gate 接线前**仍可不分型进入系统**(= `OB-006-v10-02` 的 exposure)。
3. **`due_event` 沿用 obligation 的事件语义,本仓没有自然时钟**(承 v9 README 局限 3)。
   若某 `due_event` 长期不发生,该 warn 会**无限期停在当前分型** —— 可见,但不阻断。
   ⚠ 本轮把三条现存 warn 的 `due_event` 全部指向 `forge:006:phase0`,**正是为了绕开这一点**:
   那是本仓唯一有实证会真的发生、且已接线的复审 gate。
4. **registry 不可读时 admission/consumption 两个 gate 均 fail-closed**(同 ledger 的取舍)。
   恢复路径 = `git checkout framework/warn-registry/registry.jsonl`。

## 怎么读

```bash
# 全部条目
python3 -c "import json;[print(json.loads(l)['id'], json.loads(l)['warn_class'], json.loads(l)['title']) for l in open('framework/warn-registry/registry.jsonl') if l.strip()]"

# schema 校验(hard gate · exit 1 即拒)
bash framework/warn-registry/validate-warn-class.sh

# 某次 forge intake 会被要求三态裁决的 warn
bash framework/warn-registry/validate-warn-class.sh --due-at forge:006:phase0
```
