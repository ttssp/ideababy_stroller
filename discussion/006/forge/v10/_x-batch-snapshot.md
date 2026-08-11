# X 批次权威快照 · forge 006 v10

> **本文件的地位**:X 的**首选阅读源 · 自足**。外部路径(XenoDev 仓)在 Codex 沙箱下大概率
> BLOCK,**读不到时以本文件为准**,不要因为读不到就产出「未检索到 ⇒ 无此问题」型负结论。
> 承 v9 `_x-batch-snapshot.md` 先例。
>
> **批次**:簇 A(治理条款的可执行性)4 条 + 簇 B(声明存在但机制不存在)4 条 = **8 条**。
> **显式排除**:簇 C(KG-B13 / KG-B14 · cdx-run 执行面)· 簇 D(XD-45 / KG-49 · SKILL 与 file_domain 结构冲突)。
> 排除项在 `discussion/006/FORGE-006-v10-PENDING.md` 里有完整条目,**本轮不裁**。
>
> **Y 只有「架构设计」一个视角,这是 operator 刻意收窄的** —— 见 forge-config.md §K 第 2 段。

---

## Part 0 · 本批的共同结构(先读这一节)

八条分两簇,但 operator 判断是**同一根的两个面**:

```
                    ┌─ 簇 A:规则写下了,但没有「执行边」
   同一根 ──────────┤     (规则存在 → 执行不存在)
                    └─ 簇 B:声明写下了,但没有「校验边」
                          (字段/防线/指标存在 → 实现不存在)
```

**两簇共有的形状**:某个东西在**文档层面存在**(一条规约 / 一个自证字段 / 一条健康度指标 /
一个 fixture 语料 / 一个升级判据),而**使它生效的那个东西不存在**(执行边 / 校验代码 /
上升工具 / 执行记录 / 升级 owner)。两侧的落差**不产生任何信号** —— 系统看起来是绿的。

**已被实证排除的解释**:「执行不力 / 该有人跟进 / 纪律要更严」。四次独立实证:
1. XD-44′ 连续四次,**没有一次**是靠 codex 判 `approve` 结束的,全部由 operator 叫停;
2. KG-B15 的升级判据在**第 2 次**就达成,达成后仍复发到**第 4 次**;
3. v9 违反了 v8 给它下的 intake 义务 —— 那次**决议、下发、留痕全做了**,仍然蒸发;
4. 2026-08-11(本轮 Phase 0)obligation gate 拦下 OB-006-v9-01,74 天没人做的回审
   **在 gate 上被迫做完** —— 说明缺的从来不是意愿,是**边**。

⇒ 请把「人没做」当作**已排除项**,直接审结构。

---

## Part 1 · 簇 A · 治理条款的可执行性(4 条)

### A-1 · XD-44′ · review gate 缺「收敛」这个终止边(连续 **4** 次)

现行 `codex-review` SKILL §4.2 只有**轮数上限**一个终止边,没有**收敛**这个终止边。
后果:撞顶后 `needs-attention` 与 `approve` **导向同一出口(ship)**,于是
**唯一的实际终止条件是 operator 疲劳**。

**四次计数(据实 · 均在 001-radar-pA)**:

| # | task | 终止轮 | 该轮 findings | 谁叫停 |
|---|---|---|---|---|
| 1 | T040 | round-6 | 3×`[P2]` | operator |
| 2 | FU-R1F1 | round-4 | 1×`[high]` | operator |
| 3 | T042 | round-5 | 1×`[high]`(KG-50)+1×`[medium]` | operator |
| 4 | **T041** | round-6 | 2×`[P2]` | operator(**两次**显式介入) |

**第 4 次(T041)带来前 3 次没有的两条硬证据**:

- **(a) finding 序列非单调 ⇒ 直接否证「多跑几轮就会收敛」**
  6 轮依次 **4 → 2 → 1 → 3 → 3 → 2**,`needs-attention` ×6,**一次 `approve` 都没有**。
  round-3 已降到 1 又**反弹**到 3。这是本家族第一次有**定量**证据说明轮次与收敛之间没有单调关系。
- **(b) 「提高轮数上限」这条修法已被预先证伪**
  T041 是四次里**唯一一次 operator 显式授权加轮**(round-6)的案例,加了轮**仍以
  `needs-attention` + 2 条新 finding 结束**。⇒ 只调 XD-44 的上限值不构成解法。

**一条 scope 侧候选真因(⚠ 标为假说 · 未经 producer 确认)**:T041 被审对象是 operator
自用的批跑脚手架(`tests/e2e/batch_runner.py` + `src/radar/bench/`),15 条 finding 多为
path traversal / 命令注入形状;而同批次 `FU-R5F4` 审的是 `gate.py` 真门禁逻辑,
**1 轮 0 finding 结束**。⇒ **review gate 对被审模块的「关键性分级」无感,评审强度全线均一**;
这可能同时解释非收敛 —— 低风险面上对抗式评审永远能再找出一条 `[P2]`。

### A-2 · XD-52 · 4 轮上限**怎么执行**:轮次真相住在对话记忆里

`codex-review` SKILL §4.2 的 4 轮上限**靠 agent 在对话上下文里自己数轮次**,
没有机器可查的计数器。T041 round-4 是上限最后一轮、本该 hard-stop,执行时判断有误又跑了
round-5(该会话此前经历过一次 context compaction,**压缩摘要对轮次是叙述性文字而非结构化字段**)。
**无任何产物因此被错误放行**;偏差是 producer **自曝**的。

**三条的分工(务必区分,勿混为一谈)**:
- **XD-44** = 上限**值**该多少(v9 已裁:按风险/复杂度分档)
- **XD-44′** = 该不该**只有「上限」这一个终止边**
- **XD-52** = 上限**怎么执行**(真相在对话记忆里,不在文件系统里)

### A-3 · XD-47 · 假审与真审在解析层**逐字节同形**

T042 round-1:codex 只读执行器 `bwrap` 起不来,**一个字节 diff 都没看过**,却产出
`Verdict: needs-attention` + `findings: 0`,与「真审了、审出 0 条」按 SKILL §4.1 契约
**无法区分**,并吃掉 4 轮预算里的一轮。

⇒ **review gate 的输出不携带「gate 是否真的运行过」这一位信息,且降级方向是 fail-open**
(没审 ⇒ 0 finding ⇒ 看起来更干净)。

与 **XD-41**(v9 已审)同根:XD-41 是**语义**上没真审(子代理与被审代码同源同上下文),
XD-47 是**物理**上没真审。XD-44′ 给出了 XD-41「`needs-attention` 事实等价于放行」成立的
**机制**:撞顶后两种 verdict 导向同一出口。

### A-4 · KG-B15 · warn 型规约的升级:判据达成后仍复发(**4** 次)

`CLAUDE.md:112-114` 定「Session-per-idea worktree 规约」为 **warn 型 preflight 起步**,
并明写升级判据 = **warn 上线后 mismatch 混线仍复发 ≥2 次**。

| # | 日期 | 现场 |
|---|---|---|
| 1 | 2026-08-04 | `/handback-review 001` 跑在 `main` |
| 2 | 2026-08-09 | forge v6 重采样跑在 `main`,单次改动同时触及 001 与 006 |
| 3 | 2026-08-10 | `/handback-review 001` 跑在 `main`,改动触及 001+006+framework |
| 4 | **2026-08-11** | 同上形态(HANDBACK-LOG 第 45 条) |

**判据在第 2 次就达成,达成后仍复发两次。** ⇒ **「记录升级判据」本身不构成任何行为约束**。

**⚠ 第 4 次的性质与前 3 次不同,这是本条最关键的新信息**:第 4 次 operator 是在
**被明确告知 mismatch 后显式裁决「就在 main 上写」**。⇒ 不是纪律失效,而是
**规约本身有歧义**:规约把「handback-review 决议后」列为合回 main 的 checkpoint,
隐含「决议在 idea 分支做、之后合回」,但 checkpoint 产物本身就是 main 的合法内容。
⇒ **升级 hook block 之前必须先消掉这个歧义**,否则硬拦会把合法的 checkpoint 写入一并拦掉。

---

## Part 2 · 簇 B · 声明存在但机制不存在(4 条)

### B-1 · KG-B16 · forge v8 三字段只在 XenoDev 单侧实装、IDS SSOT 三处全空

v8 簇② 决议明写「hand-back / outbox 包 frontmatter 加 `current_idea`/`worktree`/`baseline`
三字段(跨仓通道自带拓扑自证)」,但**只在 XenoDev 单侧实装,IDS SSOT 三处全空**
(SHARED-CONTRACT schema / template / validator)—— 与 `ssot_owner: ideababy_stroller`
声明**反向**。

**实证代价**:2026-08-10 `/handback-review 001` 4 包中,恰好那 2 个跑在 per-task 专用
worktree 的包,`worktree` 值均错填为 idea 主 worktree —— **自证字段在它唯一有价值的场景失真**,
且因 IDS 侧无校验而无任何机制发现。**已止血**(v2.5 + `check-7`),留 forge 追认 + mirror 同步。

### B-2 · KG-B17 · handback-validator 的 test-fixture 语料在 Ubuntu 上**整体不可跑**

`test-fixtures/` 下 **valid 与 invalid 全部 6 个 fixture** 在本机跑 `validate-handback.sh`
均 `exit 1`,且 **valid fixture 挂在 check-1** —— 因为 fixture 的 `handback_target` 是硬编码
macOS 路径。

**推论(要点)**:valid fixture 恒 FAIL ⇒ 该 fixture 语料**自 mac→Ubuntu 迁移后就没有被
真正执行过** —— 否则第一次跑就会炸。**validator 是 hand-back 通道唯一的自动化防线,
而它自己的测试语料是死的。**

### B-3 · KG-B18 · `workspace.source_repo` 声明**从未被任何 check 校验** —— 全语料 **47/100** 包失真

hand-back `001-radar-pA-20260811T024101Z`(T041)声明
`workspace.source_repo = /Users/admin/codes/ideababy_stroller`(mac 旧路径,Ubuntu 上不存在),
而 `workspace.handback_target = /home/ys/.../discussion/001/handback/`。这两个字段按
**§6.2.1 约束 1 自身的公式**(`handback_target` ⊂ `source_repo` + `/discussion/<id>/handback/`)
**互相矛盾**,却 **7 个 check 全 PASS**。

**实证根因(grep 确认 · 非推演)**:`validate-handback.sh:76` 抽出的 `SOURCE_REPO_FM`
**全文件再未被使用** —— 死变量。check-1 把约束 1 的公式作用在**运行时 CLI 传入的**
`source_repo`(consumer 的 `realpath .`)上,那个值**恒自洽**;包里**声明的**那个从未进过任何判据。

**全语料实测**(落 `check-8` 后逐包跑 · 非抽样):

| 语料 | PASS | **WARN(声明失真)** | 无字段 |
|---|---|---|---|
| `discussion/001` | 22 | **19** | 0 |
| `discussion/006` | 29 | **0** | 0 |
| `discussion/009` | 2 | **28** | 0 |
| **合计** | 53 | **47 / 100** | 0 |

**且是回归**:8-09/8-10 连续 4 包都填对 `/home/ys`,本包退回 mac 路径 ⇒ producer 取值**不稳定**。
**根因候选**:XenoDev live `CLAUDE.md` 三处仍把 IDS 仓路径写成 mac 路径
(`:38` workflow 步骤 2 · `:55` 跨仓引用 · `:90` validator dry-run 示例),
IDS 侧 mirror 同样 4 处 ⇒ **每个 XenoDev session 读到的宪法都在告诉它 IDS 在 mac 路径上**。
**已止血**(`check-8` · warn 型),留 forge 追认。

### B-4 · KG-B19 · hook 白名单「只减不增」**没有工具可执行** + 与 worktree 规约结构冲突

**本条是本轮 Phase 0 的 obligation gate 阻断后被迫执行的白名单全表回审当场产出的。**

`framework/hook-allowlist-governance.md` 三条不变量(`:30` / `:47` / `:55`):
1. **不变量 1** · 按模式类收敛,不按撞一次加一条(三个模式类:heredoc-commit-message /
   mktemp 私有 dir / 变量拼路径)
2. **不变量 2** · 每条白名单是一条待回审承诺(无理由的裸豁免 = 回审时默认候选删除)
3. **不变量 3** · 定期回审入纪律;**健康度指标:精确路径条数只减不增**

**回审实测**(XenoDev `.scan-credentials-ignore` · 24 条逐条真跑):
- 21 条有效;**3 条失效已删**(`review-log/T102-round3/4/5.md` —— **从未进过 git、
  磁盘上也不存在**;同 commit `0837e92` 里 round1/2 是真 tracked 的)⇒ 这 3 条是
  **对不存在文件的豁免承诺**,承诺没有指称对象。条数 24 → 21(XenoDev commit `5442afd`)。
- **该文件自 2026-05-29 创建后 74 天零修改** ⇒ 「回审」这个动作**一次都没发生过**;
  健康度指标此前**只有一个数据点**。

**🔴 结构问题 1 · 「只减不增」没有工具可执行**:三个模式类识别**至今 ⏳ 未实装**
(`hook-allowlist-governance.md:76-83` §4 落地状态)。⇒ **唯一能让条数下降的机制根本不存在**,
"只减不增"只能靠删失效条目达成,而失效条目有限。

**🔴 结构问题 2 · 与 forge v8 worktree-per-idea 规约结构冲突(新)**:
白名单是 **repo-root 相对精确路径**,而 v8 规约要求每 idea 一个独立 worktree,
仓内 worktree 落在 `.claude/worktrees/<idea>/` —— 同一份文件在 worktree 里前缀不同,
**全部不被覆盖**。
- **实测**:XenoDev 现有**一个**仓内 worktree,`scan-credentials.sh` 总命中 **22** =
  **2 条 by-design**(`secrets/prod/` 已 gitignored、从未进过 git、件 1 路径硬拦按设计触发
  且明文不受白名单放行)+ **20 条 worktree 副本假阳性**。
- **不能按精确路径修**:每多一个 worktree 多 ~20 条,条数随 worktree 数**线性膨胀**,
  必然同时违反不变量 1 与不变量 3。⇒ **两条框架规约互不兼容**,
  而这一点在 74 天无人回审期间从未被发现 —— **冲突本身就是"没有回审"的产物**。

---

## Part 3 · 现行机制的带行号现场原文

### 3.1 · 🔴 本轮最重要的自指事实:簇 B 的止血手段**自己全是 warn 型**

| 机制 | 位置 | 声明 |
|---|---|---|
| `check-7`(拓扑自证) | `check-7-topology-selfattest.sh:13` | 「**本 check 永远 exit 0** —— warn 型起步」 |
| 同上 · 升级判据 | 同文件 `:16` | 「warn 上线后 worktree mismatch 仍复发 **≥2 次**」 |
| `check-8`(声明侧 source_repo) | `check-8-declared-source-repo.sh:23` | 「**本 check 永远 exit 0** —— warn 型起步,与 check-7 同构」 |
| 同上 · 升级判据 | 同文件 `:26` | 「warn 上线后声明不自洽仍复发 **≥2 次**」 |
| worktree 规约 | `CLAUDE.md:112-114` | 「**warn 型 preflight**……hook block 留 v0.2,升级判据 = 仍复发 **≥2 次**」 |
| SHARED-CONTRACT | `framework/SHARED-CONTRACT.md:814` | 「**校验强度 · warn 型起步(不阻断)**」 |

⇒ **簇 A 的病(规则没有执行边)正在簇 B 的解药上原样复现。**
三个 warn 机制、三条形状相同的「≥2 次」升级判据,而 **KG-B15 的判据已经达成两次、
仍然没有人升级** —— 已有直接反例证明这种判据不产生行为。

### 3.2 · obligation ledger(v9 verdict 的产物)· 接线状态

`framework/obligations/README.md:81-91`:

| gate | 角色 | 状态 |
|---|---|---|
| `forge:<id>:phase0`(intake) | 消费 | ✅ **已接线 · fail-closed** |
| `xenodev:handoff-intake` | 消费 | ❌ **未接线** |
| `xenodev:task-review` | 消费 | ❌ **未接线** |
| `xenodev:ship-gate` | 消费 | ❌ **未接线** |

⇒ ledger 里 `consumer_wired: false` 的条目**登记了但不会被消费**(README `:91` 自陈)。

> 🔴 **订正(2026-08-11T05:12Z · 由 Codex P1 §Notes 抓出)**:本节原写「11 条中 **10 条**
> `consumer_wired: false`,唯一接线的那条今天刚被消费」—— **错**。真值经 `ledger.jsonl` 逐行复核:
> **13 原始行 / 11 唯一 id;`consumer_wired: true` 有 2 条**(`OB-006-v9-01` 与 `OB-006-v9-02`,
> **都**挂 `forge:006:phase0` 且**都**已 satisfied)⇒ **`false` 是 9/11,不是 10/11**。
> **实质结论不变**(build 侧 `xenodev:*` 三个 gate 仍全部未接线),但**数字是错的,且它写在权威快照里、
> 双方 P1 都读过**。留此订正而非静默改数:本仓已有「cwd 错致的假事实照单流过四轮 forge」的先例
> (forge 001 v6 §underweight-10),同类错误必须可见。
> **x_hash 不变**(X 的路径清单未改,只订正快照内的一个事实)。

现存 11 条义务中 **9 条 `consumer_wired: false`**;已接线的 2 条同属 `forge:006:phase0`,
今天在本轮 Phase 0 一并取得终态。

### 3.3 · ⭐ 本轮 Phase 0 的正面实证(以及它的边界)

2026-08-11,本轮 v10 的 Phase 0 obligation gate **fail-closed 阻断 intake**,命中
`OB-006-v9-01`(hook 白名单全表回审)—— 正是 v9 自己在 `.forge-state.json` 的
`v10_triggers` 里标为「**最强判据**」的那条(原文:「note 3 白名单存量在下一次 Phase 0 intake
又蒸发」)。

**结果**:74 天没做的回审在 gate 上被迫做完,当场删 3 条失效条目、产出 **KG-B19 两条结构发现**。
**这是 obligation 机制第一次真的拦下东西,并且拦对了。**

**⚠ 边界(不得越过)**:
1. **只有 1 个数据点**,不得据此推论机制已充分;
2. 它拦下的是 **forge 自己这条链**,build 侧四个消费 gate 至今**全部未接线**;
3. 拦下它的判据是「同一 gate 名 + pending」这种**最简单的形态**,尚未经历
   `due_gate` 语义歧义 / 跨 gate / 到期判定等真实考验。

---

## Part 4 · 待判问题(供双方在 P1 组织自己的判断,非答案清单)

1. **「声明存在但机制不存在」有没有通用机制解?** 还是必须逐点接线?
   若只能逐点,**完备性敞口**是什么(谁枚举、枚举清单本身会不会缺席)?
2. **warn 型起步是不是正确的抽象?** 已有三个 warn 机制 + 三条同形「≥2 次」判据 +
   一个判据达成两次仍未升级的直接反例。是该修判据的形式,还是该放弃 warn/block 二态?
3. **升级判据的 owner 问题**:「≥2 次」由谁计数、在哪个 gate 上被读到、
   达成后由谁执行升级?(注意:这正是 obligation ledger 的 `due_gate` 想解决的形状 ——
   本轮的 warn 升级判据能不能直接表达为 obligation?)
4. **review gate 的终止边**:除「轮数上限」外,「收敛」这个终止边怎么定义才**可判定**?
   A-1(b) 已证伪「提高上限」;A-1 的「关键性分级」假说成立吗?
5. **自证字段的职责划分**:`source_repo` 这类 **consumer 侧有权威值**的字段,
   该不该允许 producer 声明?(声明一个对方有权威值的字段,本身就是在制造可失真面。)
6. **路径类声明在多 worktree / 多主机下如何保持有效?**(KG-B17 fixture 硬编码 +
   KG-B18 指令文档陈旧 + KG-B19 白名单 worktree 冲突 = 三条同族,能否一次性处置?)
7. **追溯性执法的边界**:`check-8` 若升 hard-fail,47/100 存量包会被整体判 corruption。
   存量语料与新语料该不该用不同强度?这个问题在 check-7(40+ 老包)已出现过一次。

---

## Part 5 · 本快照自身的诚实边界

1. **A-1 的「关键性分级」是 IDS consumer 侧推论,未经 producer 确认** —— 标为假说,
   不得当事实用。
2. **B-3 的 47/100 数字来自 `check-8` 这个我方今天刚写的 warn 检查** —— 检查逻辑是纯词法
   比较(不碰文件系统),已在回归包与正确包两侧对照验证,但它没有独立的第二实现交叉验证。
3. **XenoDev 侧数据(B-4 的 24→21、22 条命中分解、`scan EXIT=1`)全部在本机真跑取得**,
   且 `scan EXIT=1` 已用 `git stash` 对照确认是**删除前就存在**的既有状态,非本次改动引入。
   但 Codex 沙箱读不到 XenoDev 仓时**无法独立复核**这些数字。
4. **本快照由 Opus 侧撰写,而 Opus 也是 P1/P2/P3 的一方** —— 快照的取材与详略本身带撰写者
   偏好。Part 1/2 的每条都给了可独立核查的行号或 commit,请优先核查原始出处而非本快照转述。
5. **簇 C / 簇 D 被显式排除**,但它们与本批共享部分结构(KG-B14「形态声明 vs 执行无校验」
   与簇 B 同形)。若 verdict 的一般条款自然覆盖了它们,**请明说**,但不要为了覆盖而扩张 X。
6. **本轮 Y 只有「架构设计」**。若你认为某条的关键判断**必须**动用工程纪律或安全视角才能作出,
   请明确标出并说明为什么 —— 不要默默切换视角。
