# Moderator notes · forge 006 v9

> 由 `/forge-inject 006` 追加。后续每个 phase 的双方产出**必须**读本文件。

## Injection @ 2026-08-10T09:58:07Z

**Type**: **Hard constraint**
**Binding on**: **Both**
**Phase context**: 注入时 forge 处于 **Phase 3R1 · 等 Codex** 阶段。
⇒ **Codex 在 P3R1 即须回应**(其 inbox 已同步更新);
**Opus 的 P3R1 已写完,故 Opus 在 P3R2 回应** —— 该不对称**如实记录在此**,
不得读作某一方回避;它对 Codex 有利(Codex 拿到更多输入)。
**Affects K**: **no**(本 note 是**新证据**不是新判准;K 不改,`forge-config.md` 不动,x_hash 不变)

---

### 注入内容 · 本家族的失败链已有 **3 次实证**,而且第 2、3 次发生在**治理层自己身上**

双方 P1/P2 都把「缺席即豁免」定位在 **build 侧的评审证据**(R-Q7 记录 / preflight 门 /
替代路径放行 / 轮次上限)。**IDS 侧一次独立清点显示:同一失败模式在「forge 决议 → 授权条目 →
落地」这条治理链上,已经独立发生 3 次。** 三条证据如下,均为仓内实查、可逐条复核:

**实例 1 · `framework/SHARED-CONTRACT.md:993` post-P0 backlog(已在 P1-Opus §1 记录)**
登记于 2026-05-31,明写「**需 forge 决议**」;forge v5 / v6 / v7 / v8 **一场都没接**,至今 **约 65 天**。

**实例 2 · 🔴 `framework/SHARED-CONTRACT.md:1239`(§8.5 落地状态 · forge v8 · 2026-07-13)——
它就是 XD-43 本身**

> ⏳ **XenoDev preflight 登记表 + `evaluate_gate` 接下游**:执行侧实装 · **本轮不当场改**,作
> 授权条目经 hand-off/dogfood-backlog 下发 XenoDev 实装(per forge v8 verdict K5 硬约束)

⇒ **v9 正在审的 XD-43「preflight runner 已实装但无任何入口调用」,不是「没人想到要接线」** ——
**forge v8 已经裁定要接、已经下发了授权条目,28 天后仍是 ⏳。**
这比双方 P1 手上的事实**更坏**:它**走完了完整的 forge 决议流程**才蒸发的。

**实例 3 · `framework/hook-allowlist-governance.md:82`**

> ⏳ **回审入 forge intake 固定项**:下次 `/expert-forge 006` 起时把白名单全表过一遍。

⇒ **v9 就是那个「下次」。v9 起了,白名单全表没过**(v9 的 X 七件标的里没有它)。
**本轮 forge 自己正在违反上一轮 forge 给自己定的 intake 义务。**

**背景数据**:IDS 侧现存 `⏳` 授权条目共 **8 条**(`SHARED-CONTRACT` 6 条 `:634 / :1170 / :1173 /
:1175 / :1239 / :1242` + `hook-allowlist-governance` 2 条 `:79 / :82`),分别源自 forge v7 / v8。
**本 note 不要求本轮裁这 8 条**(其中数条属批次外),只要求把「**这条链本身没有机器落点**」
作为已证事实纳入 verdict 的推理。

---

### Required response(双方 · 三问,逐条作答,不得合并含混)

在你的 phase 产出开头加一节 **`## Moderator injection response`**,回答:

1. **覆盖面**:你主张的机制(如 obligation ledger / 期望清单 / 三态申报)
   **是否覆盖治理层自己的决议与授权条目**?
   —— 若**覆盖**,请说明 forge verdict / 授权条目**在谁的 gate 上**产生 obligation、由谁消费。
   —— 若**不覆盖**,请正面说明:为什么这条链的 **3 次实证失败不构成反例**?
   (⚠ 若答案是「治理层靠人盯」,请直接写出来并接受它与 K 第 1 条「要 enforcement」的张力。)
2. **归层**:承 P2-GPT 已确立的判断(**design gap 与 execution gap 并存**),
   请判这 3 个实例属**哪一层**。⚠ **不得**笼统读成「执行不力 / 人没跟进」——
   实例 2 恰恰证明**流程全走对了仍然蒸发**。
3. **实例 3 的自指处置**:v9 本轮**违反了 v8 给它定的 intake 义务**。
   请判:这是否要求 verdict 里包含**一条约束 forge 自身**的条款?
   (支持 / 反对均可,但**不得沉默** —— 沉默在本批的语境里等于 merely noted。)

### ⚠ 传递要求(机械细节,别漏)

**Phase 4 synthesizer 读的是 `forge-config.md` + 8 个 round 文件,它不读本文件。**
⇒ 双方对本 note 的结论**必须写进 P3R2 的正文**(§2 联合 verdict / §3 v0.2 note / §4 W 草案),
**只在 `## Moderator injection response` 里提一句,会在 synthesizer 处整条丢失** ——
那将成为本家族的第 4 个实例,且是本轮自己制造的。

### 冲突解决

本 note 为 **Hard constraint**:与 P1/P2/P3R1 中既有判断冲突时,**须调整既有判断以 honor 本 note**,
并**显式指出冲突点**,不得静默改写。
