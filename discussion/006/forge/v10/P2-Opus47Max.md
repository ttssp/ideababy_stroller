# P2 · Opus 4.7 Max · forge 006 v10 · 参照系评估

## §0 · 本轮 Z 执行状态(必须先读)

🔴 **`WebSearch` 三次同错 400**(`output_config.effort 'xhigh' is not supported when thinking is disabled`)
—— **与 forge 001 v6、forge 006 v9 完全相同的后端故障,第三次复发**。

⇒ 本轮 Opus 侧 Z **退化为对已知权威源的定向 `WebFetch`(不是检索)**。据此:
- **本 P2 不产出任何「未检索到 ⇒ 无先例」型负结论**;
- Z 的第 1 方向(policy-as-code 强制边的下一层)与第 3 方向(技术债/例外的到期 ratchet ·
  SonarQube "Clean as You Code")**本轮未取到**(前者 v9 已有反证故未重投,后者两次 fetch
  均落到 404 / 无相关段落)⇒ **已在 P2 inbox 指派 Codex 单侧覆盖**;
- 第 5 方向(review 终止按被审对象**关键性分级**)同样未取到,一并指派。

**已读**:对方 `P1-GPT55xHigh.md`(全文)· 自己 P1 · `forge-config.md` · `moderator-notes.md`(不存在)。

---

## §1 · SOTA 对标

| # | 锚点 | 出处 | 对本批的作用 |
|---|---|---|---|
| ⭐1 | **rustc 的 future-incompatible lint 升级程序**:每 **6 周 release cycle 开始时**,编译器团队**复审全部未决的 future-compat warnings** 并提名进 FCP;**每个 breaking change 必须有 dedicated tracking issue**;FCP 持续一个 cycle,末期裁定;**三种合法结局:convert to error / revert / defer**;理想情况下变更先落 stable 分支再定案 | RFC 1589(rustc bug fix procedure)· 经 `doc.rust-lang.org/rustc/lints` 指引取得 | 🔴 **本轮唯一一次真正的证伪,推翻的是我自己 P1 的核心直觉** —— 见 §3(1) |
| 2 | **git 的多 checkout 路径语义**:linked worktree **共享** `.gitignore` / `.gitattributes`;文档**明令**「**不要假设某个路径属于 `$GIT_DIR` 还是 `$GIT_COMMON_DIR`**,需要直接访问时**用 `git rev-parse --git-path`**」 | `git-scm.com/docs/git-worktree` | KG-B19 的**直接锚点**:按 checkout 根归一路径**不是我们的发明,是 git 自己的文档指引** |
| 3 | (未取到)ratchet / new-code baseline 的到期语义 | — | 已指派 Codex 单侧覆盖,**不作负结论** |

**限缩(本轮野心的边界,verdict 不得越过)**:
RFC 1589 描述的是**单一团队、固定发布节奏、且有 crater 级生态影响面**的场景。本仓是
**单 operator、无自然发布节奏、批次间隔以周计** —— v9 `underweight-8①` 与 obligation README
局限 3 已指出「`due_gate` 在本仓没有自然时钟」。**Rust 的 6 周 cycle 正是那个本仓没有的时钟。**
故下文 §3(2) 的推论必须带这个限缩,不能直接移植。

---

## §2 · 用户外部材料消化

K 中未提供外部链接或文件,无材料需消化。本节为空属正常。

---

## §3 · 修正后的视角

**(1) 🔴 我 P1 §1(2) 的核心直觉被 RFC 1589 推翻,且推翻的方式比我原来的想法更有用。**

我 P1 主张:`warn` 是「没有出口的状态」,架构上应当**自带到期**(到期自动升级或自动失效)。
**错了。** 最成熟的 warn→error 治理体系(rustc)**根本不用自动到期**,而且它明确把
**`defer` 列为三种合法结局之一**。

真正的机制是三件东西的组合:**① 固定节奏的复审 gate(每 6 周)· ② 每条 warn 一个具名
tracking issue · ③ 到期必须作出三态裁决,而 `defer` 是被裁出来的、不是被忘记的。**

⇒ **关键区分不是「自动 vs 手动」,而是「被裁决出来的 defer」vs「被遗忘的 defer」。**
本仓四条「≥2 次」判据的病,不在于它们是手动的,而在于**没有任何时刻会强迫任何人对它们作出裁决**。

**(2) 这反过来大幅提高了我对 v9 机制的评价,并精确定位了它缺什么。**

把 RFC 1589 的三件套映射到本仓:**obligation ledger ≈ tracking issue**(每条一个、具名、可查、
append-only);**forge Phase 0 gate ≈ 固定复审 gate**;而 **v9 的 `skipped`(具名签署 + 不得留白的理由)
恰好就是「被裁出来的 defer」** —— 我 P1 写这条时并没有意识到 v9 已经把它做对了。

⇒ v9 的状态机**比我 P1 设想的更接近 SOTA 形态**。它缺的是**第一件**:**固定节奏**。
本仓的 forge Phase 0 只在 operator 起 forge 时发生,**而起不起 forge 由 operator 决定** ——
这正是 README 局限 3「`due_gate` 没有自然时钟」的同一个洞。**⚠ 但按 §1 的限缩,
「引入固定节奏」在单 operator 仓里是否可行,本轮无证据,不得当作已解决。**

**(3) 我接受 Codex P1 的反对,并大幅收回 P1 §1(3) 的归并倾向。**

Codex 判「至少 review 终止、真运行证明、权威值职责与路径身份属于旧框架未定义的新结构」——
**这是对的,而且 RFC 1589 从侧面印证了它**:Rust 有 tracking issue 机制,但「这条 lint 该不该
升 error」的**判据本身**来自另一套东西(FCP、生态影响评估、团队判断),**不是 tracking issue 提供的**。

⇒ **义务层与语义层是两层,不能互相替代。** obligation ledger 能保证「这件事不会被忘记」,
但定义不了「review 怎样算终止」「怎样证明真跑过」「谁拥有路径真值」。
我 P1 §3(1) 自陈过对自己上一轮机制有偏袒动机 —— **该偏袒确实发生了**,Codex 独立判对了。
簇 A 的 XD-44′ / XD-47 应保持 `new`,不得降级为「v9 的接线实例」。

**(4) 两处评级修正 + 一条事实订正。**

- **KG-B17** 我原判 `refactor`,Codex 判 `new`,我**改判 `new`** —— Codex 的理由更强:
  fixture 不是"路径写错了",而是 **validator 的发布环节从未消费过「fixture 通过」这个产物**;
  补一个环境无关的 fixture 只是必要条件,真缺的是发布 gate 上的消费点。
- **KG-B18** 双方 P1 **独立**判 `cut`(我未读它、它未读我)—— 但 Codex §3-2 给了更好的细化:
  `source_repo` 可能承载「**producer 当时所见的目标**」这一审计价值,
  ⇒ 应**改名为观察值并与 consumer 权威值分域**,而不是直接删。**我接受这个细化**,
  它比我的"删字段"更保守且不丢信息。
- 🔴 **事实订正**:我在权威快照 Part 3.2 写「11 条中 10 条 `consumer_wired: false`」,**错**。
  真值 **9/11**(`OB-006-v9-01`/`-02` 两条均为 `true`,同挂 `forge:006:phase0`,今日一并终态)。
  **由 Codex P1 §Notes 抓出**,快照已订正并留可见的订正块(不静默改数 ——
  本仓有「假事实照单流过四轮 forge」的先例)。实质结论不变(build 侧三个 gate 仍全未接线)。
