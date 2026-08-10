# Authorization Brief · forge 006 v9 · operator 选 **[B] 止血核心**

**Decided**: 2026-08-10
**Verdict 全文**: `discussion/006/forge/v9/stage-forge-006-v9.md`
**机制载体**: `framework/obligations/README.md` + `framework/obligations/ledger.jsonl`

---

## operator 的选择

菜单四选一里选 **[B] 只落 forge 治理链一段** —— 只做 **M2 的两个 forge 入口** + **note 3
白名单清偿的登记**,**build 侧全部延后**。

**理由**(承 stage doc §Decision menu [B]):两个入口都在 IDS 内、成本最低;而且本轮自己欠了一条债
(v9 违反了 v8 定给它的「下次 forge intake 把 hook 白名单全表过一遍」义务),正好当控制面的
**首个真跑样本** —— 机制若无效,下一次 `/expert-forge 006` 就会立刻暴露。

---

## IDS 侧已落地(本批次)

| # | 落点 | 内容 |
|---|---|---|
| 1 | `framework/obligations/ledger.jsonl` | **新建** · append-only · 首批 11 条 |
| 2 | `framework/obligations/README.md` | **新建** · schema / 状态机 / 签署权 / 接线状态表 / **5 条已知局限** |
| 3 | `.claude/commands/expert-forge.md` **Step 0.6** | **消费点接线** · `forge:<id>:phase0` · **fail-closed** |
| 4 | `.claude/commands/expert-forge.md` **Step 6.5** | **产生点接线** · `forge:<id>:v<N>:phase4` · 候选须 operator 逐条确认 |
| 5 | `.claude/commands/expert-forge.md` Step 0.3 | 状态检测表首行加 Step 0.6 前置 |
| 6 | `.claude/skills/forge-protocol/SKILL.md` | Phase 0 / Phase 4 两段同步条款(**声明层与执行层必须一致** —— 只改一边就是本轮在审的那个毛病) |

**为什么不动 `SHARED-CONTRACT.md`**:已核实 `.claude/commands/expert-forge.md` 与
`.claude/skills/forge-protocol/SKILL.md` **都不在 `framework/xenodev-bootstrap-kit/` 里**
⇒ **非 mirror 件**,不需要三层同步、不需要 bump `contract_version`。
这是 [B] 相对 [A] 便宜得多的根本原因。

---

## XenoDev 侧授权条目(**本轮延后 · 已登记为可见敞口**)

⚠ 按铁律「框架级变更只走 forge,XenoDev 不当场改」,以下条目**已产生但消费点未接线**。
operator 明确选择「**敞口可见,而不是沉默**」⇒ 全部登记进 ledger 并带 `exposure` 字段。

| ledger id | 授权条目 | `due_gate`(未接线) |
|---|---|---|
| `OB-006-v9-03` | XD-41 · fallback 补审债从 merge 时即创建 `pending` | `xenodev:handoff-intake` |
| `OB-006-v9-04` | KG-B11 + XD-43 · build 侧 canonical entry gate 接线 | `xenodev:handoff-intake` |
| `OB-006-v9-05` | 接手 `SHARED-CONTRACT:993` post-P0 (b)(c)(d) | `xenodev:ship-gate → ids:handback-review` |
| `OB-006-v9-06` | v0.2 note 1 · v0.7/v0.8 漏调入口复盘 | `xenodev:task-review`(M2 首个接线 task) |
| `OB-006-v9-07` | v0.2 note 2 · 每个 gate 登记覆盖面 + `due_gate` | `xenodev:task-review`(各 gate pre-merge) |
| `OB-006-v9-08` | v0.2 note 4 · `skipped` 签署格式定形 | `xenodev:task-review`(M1 首个实现 task) |
| `OB-006-v9-09` | XD-44 · 四轮上限改风险/复杂度分档 ⚠ **mirror 件** | `xenodev:handoff-intake` |
| `OB-006-v9-10` | `needs-attention` 不再等价放行(泛化到全仓 gate) | `xenodev:handoff-intake` |
| `OB-006-v9-11` | XD-44 粒度触发线(归 task-decomposer) | `xenodev:handoff-intake` |

⚠ **`OB-006-v9-09` 触及 mirror 件**(`codex-review/SKILL.md`)⇒ 落地时顺序固定:
**IDS SSOT 改 → `cp` 回 bootstrap-kit mirror → 更新 MANIFEST SHA**。

---

## 受 gate 约束的两条(`consumer_wired: true`)

| ledger id | 条目 | 状态 |
|---|---|---|
| `OB-006-v9-01` | **hook 白名单全表回审** —— v8 定给 v9、v9 未履行的那条 | `pending` · **下次 `/expert-forge 006` intake 会被 Step 0.6 硬拦** |
| `OB-006-v9-02` | **M2 forge 两入口接线本身** | 本批次完成后追加 `satisfied` 行(带 `content_identity`)· **控制面的首个真跑样本** |

---

## 明确不做(non-goals)

- ❌ **不动 `framework/SHARED-CONTRACT.md`**(非 mirror、非 spine 必要 · 见上)
- ❌ **不动 XenoDev**(铁律 · build 侧接线属 [A])
- ❌ **不裁批次外 5 条**:KG-B8 / KG-B9 / KG-B10 / KG-B12 / XD-42(intake 时 operator 显式排除)
- ❌ 🔴 **IDS 现存另外 7 条 ⏳ 授权条目不登记进 ledger**
  (`SHARED-CONTRACT :634 / :1170 / :1173 / :1175 / :1239 / :1242` + `hook-allowlist-governance :79`)。
  **不是遗漏** —— v9 §underweight-5 明令不得借 moderator note 扩裁批次外条目,
  只登记 note 3 点名的白名单那一条。
  ⚠ **后果据实写明**:那 7 条在 [A] 落地前**继续暴露在同一失败模式下**;
  其中 `:1239` 正是 XD-43 的授权条目(已 ⏳ 28 天)—— 它由 `OB-006-v9-04` 在 build 侧接线后覆盖。

---

## 升级 / 复盘触发点

- 🔴 **`OB-006-v9-01` 在下一次 `/expert-forge 006` intake 又蒸发** ⇒ 证明治理链覆盖是纸面的,
  **直接触发 forge v10**(stage doc §Forge versioning 第 1 条,本轮最强判据)。
- 其余 v10 判据见 stage doc:note 1 复盘推翻「未调用」/ 清单外入口仍在放行 /
  `due_gate` 给不出可判定到期语义 / XD-41 形态复发。
