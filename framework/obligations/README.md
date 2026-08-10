# Obligation ledger

> **状态**:v0.1 · 落地于 forge 006 v9 的 **[B] 止血核心**(2026-08-10)
> **权威裁决**:`discussion/006/forge/v9/stage-forge-006-v9.md`
> **授权 brief**:`discussion/006/forge/v9/AUTHORIZATION-BRIEF-v9.md`

## 为什么存在

forge 006 v9 审「证据完整性家族」四条缺口时,原始诊断是「机制都写对了,只是**执行面**没人调」。
**这个诊断被 P2 的 SOTA 推翻了** —— in-toto 的 owner **先签必经步骤**、GitHub 的 requirement
**由 ruleset 预置**、SLSA 的 subject digest **先绑内容再验后生证据**:成熟体系全都
**在证据之外先定义义务**。

⇒ 本仓真正缺的不是「门」,是**义务**。缺口的精确形状是:

```
实装判据  = 「这个东西在不在」        (grep -q '^ids_verdict_evidence:')
豁免理由  = 「这类对象本来就不该有」  (老 hand-back / 非 build-ship 包无此块属正常)
```

**两者被当成同一件事,但它们不等价** —— 于是「缺席」同时是「不适用」和「违规」的证据,
而系统**总是选前者**解释。本 ledger 就是那个**独立于被检查对象的预期声明层**。

### 三次实证(为什么这不是纸上谈兵)

1. `framework/SHARED-CONTRACT.md:993` 的 post-P0 backlog 明写「**需 forge 决议**」,
   登记于 2026-05-31,**forge v5/v6/v7/v8 一场没接**,挂了约 65 天。
2. 🔴 `framework/SHARED-CONTRACT.md:1239`(§8.5 · forge **v8** · 2026-07-13)已把
   「XenoDev preflight 登记表 + `evaluate_gate` 接下游」**作授权条目下发**,**28 天仍 ⏳** ——
   而这就是 v9 在审的 **XD-43 本身**。**决议、下发、留痕全做了,仍然蒸发,因为下游没有任何
   gate 要求它清偿。**
3. `framework/hook-allowlist-governance.md:82` 明写「下次 `/expert-forge 006` 起时把白名单
   全表过一遍」——**v9 就是那个「下次」,v9 没过**。

⇒ **本 ledger 的第一条条目(`OB-006-v9-01`),就是第 3 条实证欠下的那笔债。**

## 状态机

```
        ┌─────────┐
gate 预建 │ pending │ ──── 绑当前内容身份 ────▶ satisfied
        └────┬────┘
             │  权威签署(policy 或 operator-chair)
             └────────────────────────────────▶ skipped

     到 due_gate 仍 pending  ⇒  gate 派生 fail-closed 拒绝
```

🔴 **没有 `absent` 状态,这是设计的核心。**
如果「缺席」是一个**要被写下**的状态,**它自己就会缺席** —— 等于把「缺席即豁免」原样搬进新机制。
所以 `pending` 由 **gate 在事件发生时预建**,拒绝是**到期后派生的判定**,
**没有任何人需要写任何东西就能触发它**。

**签署权分层**(堵「producer 自报」的攻击面):
- **producer 只能「提出」skip**,不得自批
- **确定性豁免** → `signature: "policy:<id>"`
- **例外** → `signature: "operator-chair"` + 具名理由(不得留白)

## Schema(一行一条 JSON · append-only)

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | ★ | `OB-<idea>-<forge_v>-<NN>`,**稳定不复用** |
| `title` | ★ | 一句话 |
| `created_at` | ★ | ISO8601 |
| `created_by_gate` | ★ | 产生 gate,如 `forge:006:v9:phase4` |
| `source` | ★ | 证据指针(裁决出处) |
| `due_gate` | ★ | 消费 gate,如 `forge:006:phase0` / `xenodev:handoff-intake` |
| `consumer_wired` | ★ | `true` / `false` —— **该消费点是否已接线** |
| `exposure` | ⚠ | `consumer_wired: false` 时**必填**:这条在接线前不会被谁消费 |
| `state` | ★ | `pending` / `satisfied` / `skipped` |
| `closed_at` / `closed_by` | | 终态时填 |
| `signature` | ⚠ | `skipped` 时**必填**:`policy:<id>` 或 `operator-chair` |
| `reason` | ⚠ | `skipped` 时**必填**:具名理由,不得留白 |
| `content_identity` | ⚠ | `satisfied` 时**必填**:`{commit, path, sha256}` |
| `evidence` | ⚠ | `satisfied` 时**必填**:证据指针 |

**append-only 纪律**:状态变更**追加新行**(同 `id`,后写覆盖前读),**不改已有行**。
读取时以该 `id` 的**最后一行**为准。

## 接线状态(v0.1 · [B] 止血核心)

| gate | 角色 | 状态 |
|---|---|---|
| `forge:<id>:phase4`(定稿) | **产生** | ✅ 已接线 —— `.claude/commands/expert-forge.md` Step 6.5 |
| `forge:<id>:phase0`(intake) | **消费** | ✅ 已接线 —— 同文件 Step 0.6 · **fail-closed** |
| `xenodev:handoff-intake` | 消费 | ❌ **未接线** —— 属 [A],本轮延后 |
| `xenodev:task-review` | 消费 | ❌ **未接线** —— 属 [A],本轮延后 |
| `xenodev:ship-gate` | 消费 | ❌ **未接线** —— 属 [A],本轮延后 |

⇒ 目前 ledger 里 `consumer_wired: false` 的条目**登记了但不会被消费**。
**这是有意为之**:operator 明确选择「**敞口可见,而不是沉默**」。
它们的 `exposure` 字段写明了这一点。

## 已知局限(不得靠沉默推断,逐条写明)

1. 🔴 **`content_identity` 是 v0.1 形态**。`{commit, path, sha256}` 只能证明
   **「清偿动作发生在这份内容上」**,**不能证明评审充分** ——
   v9 证据 7②:SLSA 能证明「谁对哪份内容作何声明」,但不能证明 review 足够,
   且 producer 与证据**同信任域**。最终形态归 [A] / v0.2 note 4。
2. 🔴 **枚举完备性是已知敞口**。清单外的入口**产生零 obligation**,原病在控制面之外原样存活。
   OPA 已反证「采 policy-as-code 即解决」—— **enforcement 接线必须逐入口做,成本省不掉**。
   ⇒ **本机制不声称自动发现未枚举的入口。**(v9 v0.2 note 2)
3. 🔴 **`due_gate` 的到期语义在本仓没有自然时钟**。单 operator、跨仓、批次间隔以周计,
   「什么时候算到期」目前靠 `due_gate` 事件**是否发生**判定,不靠时间。
   若某个 `due_gate` 长期不发生,该义务**会无限期停在 `pending`** —— 可见,但不阻断任何东西。
   (v9 §underweight-8①)
4. **本机制自身的可用性即阻断面**:gate 预建 `pending` 后,若 ledger 不可读,
   `forge:<id>:phase0` 会 fail-closed 阻断 intake。这是**有意的**(fail-closed 优于假绿),
   但代价是 ledger 损坏 = forge 停摆。恢复路径 = git 还原(本文件是 append-only 纯文本)。
5. ⚠ **IDS 现存另外 7 条 ⏳ 授权条目未登记**(`SHARED-CONTRACT :634/:1170/:1173/:1175/:1239/:1242`
   + `hook-allowlist-governance :79`)。**不是遗漏** —— v9 §underweight-5 明令不得借 moderator note
   扩裁批次外条目,只登记 note 3 点名的白名单那一条。
   ⇒ **那 7 条在 [A] 落地前继续暴露在同一失败模式下。**

## 怎么读

```bash
# 全部条目
python3 -c "import json;[print(json.loads(l)['id'], json.loads(l)['state'], json.loads(l)['title']) for l in open('framework/obligations/ledger.jsonl')]"

# 某个 forge intake 会被拦下的条目
python3 - <<'EOF'
import json, collections
rows = [json.loads(l) for l in open('framework/obligations/ledger.jsonl')]
latest = {}
for r in rows: latest[r['id']] = r          # append-only:同 id 取最后一行
gate = 'forge:006:phase0'
for r in latest.values():
    if r['state'] == 'pending' and r.get('consumer_wired') and r['due_gate'] == gate:
        print('BLOCKING:', r['id'], r['title'])
EOF
```
