# Forge 006 · v10 待跑批次(攒批处 · append-only)

> **这是什么**:forge 006 v9(2026-08-04 起跑 · X = 证据完整性家族 KG-B11 / XD-41 / XD-43 / XD-44
> + IDS HANDBACK-LOG 第 40/42 条实测证据)**冻结之后**新撞到的框架级问题攒在这里,作为下一轮
> `/expert-forge 006` 的 X 标的预填。承 `FORGE-006-v7-PENDING.md` 先例。
>
> **为什么不补进 v9**:v9 的 `x_hash`(`7ad1bb97a7760addddb7cd371eca3b71`)已冻结且 **Opus P1 已写完**,
> P1-GPT 尚未跑。此刻改 X 会重演 forge 001 v6 的「**P1 独立性污染 / 非双向对称**」事故
> (见 `discussion/001/forge/v6/stage-forge-001-v6.md` §underweight-1)—— 收益不抵代价。
>
> **创建**:2026-08-09(001 forge v6 误重放事件顺带暴露 · 见 `discussion/001/handback/HANDBACK-LOG.md` 第 43 条)

## 条目

### KG-B13 · `cdx-run` 静默重放已完成轮次并**覆盖**产物(HEAD 完成后不前进、不标记)

- **现场**:`.codex-inbox/queues/<q>/HEAD` 是单行文本 = 待执行任务文件名。`cdx-run <q>`
  (`~/.bashrc`)读 HEAD 即跑,**执行完不改 HEAD、不写任何完成标记**。
  完成态只由 `cdx-queues` 用「outbox 是否存在同名文件」**推断**(存在 ⇒ 显示 `✅ done`)。
- **失效模态**:对同一队列再敲一次 `cdx-run <q>`,会**静默重跑一个已完成、甚至已被下游消费封存的轮次**,
  产物**直接覆盖** outbox 与 discussion 下的正式文件 —— **无警告、无确认、无备份**。
  若当时工作区不干净或已 commit,覆盖可能被误当成正常改动带进 commit。
- **真实发生**:2026-08-09T21:24 · `cdx-run 001` 重放了 08-03 的 forge v6 P3R2
  (v6 早已 finalize + 落地),覆盖 `discussion/001/forge/v6/P3R2-GPT55xHigh.md` 与同名 outbox 文件。
  靠 git 恢复。详见 HANDBACK-LOG 第 43 条。
- **候选 verdict 方向(不预设答案)**:完成后 HEAD 前进/置空 · 或 `cdx-run` 见 outbox 已存在同名文件
  时改为 fail-closed(需 `--force` 或显式确认)· 或产物写入前对已存在文件做 `-resample` 旁路命名
  而非原地覆盖。
- **同题**:与 v9 的「机制已装但从未被强制调用」(XD-43 preflight)同族 —— 这里是
  **状态机缺一个前进边**,导致「完成」这个状态**从不被写下**,只能靠副作用推断。

### KG-B14 · `reuse-session` 形态被 `cdx-run` **静默降级**为冷 session(执行面零强制零留痕)

- **现场**:`.codex-inbox/README.md` §"两种 kickoff 形态" 定义 —— `oneshot`(每次新会话,`cdx-run` 执行)
  与 `reuse-session`(人在**已开**的 Codex 终端粘贴短 prompt,沿用上一轮上下文)。
  任务文件 frontmatter 用 `**Kickoff form**:` 声明形态,`reuse-session` 任务还带 `## Session hint`
  写「**已读(勿重读)**:……」。
- **失效模态**:`cdx-run` 的实现是 `codex "read <task> and execute…"` = **必然新起 session**
  (`codex resume` 是独立子命令,未被使用)。⇒ 用 `cdx-run` 执行一个 `reuse-session` 任务时,
  「**已读勿重读**」从「复用上下文」**语义反转**成「**根本不读**」,模型在**远少于协议假设的证据**上作答,
  **而产物里看不出这件事**(没有任何字段记录本轮实际拿到了哪些上下文)。
  没有任何机制阻止或警告这种形态错配。
- **影响面**:所有默认 `reuse-session` 的命令 —— `inspire-next` / `explore-next` / `scope-next` /
  `plan-adversarial-next`,以及 forge 的 P2 / P3R1 / P3R2 轮。**下游读产物的人无法判断**
  某一轮到底是在完整上下文还是冷启动下产出的。
- **真实发生**:同 KG-B13 的那次重放(P3R2 任务书写 `reuse-session`,却经 `cdx-run` 冷跑)。
  该次产物与正式版的 verdict 一致但 `evidence_grade` 打分不同,详见 HANDBACK-LOG 第 43 条 (3)。
- **候选 verdict 方向(不预设答案)**:`cdx-run` 读 frontmatter,遇 `reuse-session` 拒跑或
  显式改走 `codex resume --last` · 或要求产物 frontmatter 自报「本轮实际读了什么」使形态可审计 ·
  或取消 reuse-session 形态、全部 oneshot 并把省 token 的目标交给自足任务书。
- **同题**:与 v9 的「**缺席即豁免**」(SHARED-CONTRACT §6 B-4-IDS:协议写「任一字段缺 = REJECT」,
  实装却「父键不存在 ⇒ 整步跳过不 warn」)是**同一形状** —— 声明与执行两层之间**没有校验**。

### KG-B15 · Session-per-idea worktree 规约:warn 已复发 **2** 次,hook block 升级判据达成

- **现场**:`CLAUDE.md`「Session-per-idea worktree 规约(forge 006 v8 · 簇② · 2026-07-13)」定
  **warn 型 preflight 起步**,并明写 hook block(commit-time 硬拦)留 v0.2、
  **升级判据 = warn 上线后 mismatch 混线仍复发 ≥2 次**。
- **计数(据实)**:
  1. **第 1 次** · 2026-08-04 · `/handback-review 001` 跑在 `main` 分支 —— HANDBACK-LOG 第 42 条 (4) 留痕。
  2. **第 2 次** · 2026-08-09 · forge v6 重采样处置跑在 `main` 分支,且单次改动**同时触及 001 与 006
     两个 idea**(典型混线形态)—— HANDBACK-LOG 第 43 条 (5) 留痕。
- ⇒ **判据已达成**,v0.2(commit-time hook block)具备起动条件。**未自行升级** ——
  规约属框架层,按铁律只走 forge。
- **待判**:硬拦的粒度(分支名 mismatch 就拦 / 还是只拦「一次 commit 跨多个 idea 目录」)、
  以及**治理产物合回 main 的 checkpoint 场景怎么豁免**(合回本身就是 main 上的合法写)。

## 与 v9 的关系(起 v10 时必读)

三条与 v9 正在审的**证据完整性家族**同题,**建议并案而不是另起家族**:

| v10 pending | v9 在审 | 共同结构 |
|---|---|---|
| KG-B14(形态声明 vs 执行无校验) | B-4-IDS「缺席即豁免」 | 声明层与执行层之间没有校验点 |
| KG-B13(完成状态从不被写下) | XD-43(preflight 已实装但从未被调用) | 机制存在但**没有强制边**,靠副作用推断状态 |
| KG-B15(warn 型规约的升级判据) | v8 簇② 的 warn 起步设计本身 | warn→block 的升级由谁、在哪触发,至今无 owner |

⚠ **起 v10 前先读 v9 的 verdict** —— 若 v9 已给出「声明/执行两层校验」的一般条款,
这三条可能变成**该条款的实例**而非独立议题,X 应据此重写。
