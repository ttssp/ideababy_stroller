---
forge_version: v10
created: 2026-08-11T04:57:56Z
convergence_mode: strong-converge
x_hash: dde3abd42f0fac55f7085e1c89d882d1
prefill_source: manual(caller v10 批次 = FORGE-006-v10-PENDING.md 攒批 簇A+簇B 8 条 · 非 proposals.md prefill)
obligation_gate: OB-006-v9-01 satisfied @ 2026-08-11T04:42:18Z(gate 首次真阻断 · 详见 _x-batch-snapshot.md Part 3.3)
---

# Forge Config · 006 · v10

## X · 审阅标的

discussion/006/forge/v10/_x-batch-snapshot.md
discussion/006/FORGE-006-v10-PENDING.md
framework/obligations/README.md
framework/obligations/ledger.jsonl
framework/xenodev-bootstrap-kit/handback-validator/
framework/SHARED-CONTRACT.md
framework/hook-allowlist-governance.md
CLAUDE.md
discussion/006/forge/v9/stage-forge-006-v9.md
discussion/001/handback/HANDBACK-LOG.md
/home/ys/codes/XenoDev/.scan-credentials-ignore

### 解析后的标的清单

- `discussion/006/forge/v10/_x-batch-snapshot.md`(本仓库文件 · ✅ · **权威快照 · 首选阅读源 ·
  自足**。Part 0 两簇一根的共同结构 + 已排除的解释;Part 1 簇 A 四条带实证计数;
  Part 2 簇 B 四条带实测数据;Part 3 现行机制带行号现场(**3.1 是本轮最重要的自指事实**);
  Part 4 七个待判问题;Part 5 本快照自身的诚实边界。**外部路径 BLOCK 时以本文件为准。**)
- `discussion/006/FORGE-006-v10-PENDING.md`(本仓库文件 · ✅ · 攒批原文 · **11 条全在此**,
  其中簇 C(KG-B13/B14)与簇 D(XD-45/KG-49)**本轮显式排除**,列出仅供判断 verdict
  的一般条款是否自然覆盖它们 —— **不要为覆盖而扩张 X**)
- `framework/obligations/README.md`(本仓库文件 · ✅ · **v9 verdict 的落地物** ·
  重点 `:60-80` schema(`consumer_wired` / `exposure` 两字段)+ `:81-91` **接线状态表**
  (4 个消费 gate 只有 `forge:<id>:phase0` 已接线)+ `:97` 作者自陈的 v0.1 局限)
- `framework/obligations/ledger.jsonl`(本仓库文件 · ✅ · **11 条义务的实况** ·
  append-only,同 id 取最后一行。注意 **10/11 条 `consumer_wired: false`**;
  `OB-006-v9-01` 今天刚从 pending → satisfied,其 `evidence` 字段是本轮 KG-B19 的一手记录)
- `framework/xenodev-bootstrap-kit/handback-validator/`(本仓库目录 · ✅ · **warn 型止血件现场** ·
  重点三个文件:`check-7-topology-selfattest.sh`(:13 恒 exit 0 · :16 升级判据)·
  `check-8-declared-source-repo.sh`(:23 同 · :26 同)· `validate-handback.sh`
  (**:76 `SOURCE_REPO_FM` 死变量的现场** + 末尾 check-7/check-8 的 `|| true` 接线))
- `framework/SHARED-CONTRACT.md`(本仓库文件 · ✅ · **协议 SSOT** · **严禁整读(1300+ 行)** ——
  只读 **§6.3.1**(`:800-820`,尤其 `:814`「校验强度 · warn 型起步(不阻断)」)
  + Changelog v2.5 条目(`:1298`,含 warn 型理由与升级判据的完整表述))
- `framework/hook-allowlist-governance.md`(本仓库文件 · ✅ · **三不变量原文** ·
  `:30` 不变量 1(按模式类收敛)· `:47` 不变量 2(每条白名单是待回审承诺)·
  `:55` 不变量 3(定期回审 + **健康度指标「只减不增」**)· `:76-83` §4 落地状态
  (**三个模式类识别至今 ⏳ 未实装** —— KG-B19 结构问题 1 的直接出处))
- `CLAUDE.md`(本仓库文件 · ✅ · 只读 **`:100-130`**「Session-per-idea worktree 规约」——
  `:112-114` warn 型起步 + 「升级判据 = 仍复发 ≥2 次」+ main 分支生命周期段
  (**KG-B15 第 4 次实证暴露的歧义就在这段**:checkpoint 产物本身是 main 的合法内容))
- `discussion/006/forge/v9/stage-forge-006-v9.md`(本仓库文件 · ✅ · **上一轮 verdict** ·
  本轮多条是它的直接后续。重点:obligation control plane 的四要素
  (pending 由 canonical gate 预建 / satisfied 绑当前内容身份 / skipped 权威签署 / 到期 fail-closed)
  + 4 条 v0.2 note + decision matrix 的第 5 列 `evidence_grade` 与第 6 列 obligation path 格式)
- `discussion/001/handback/HANDBACK-LOG.md`(本仓库文件 · ✅ · **200k+,严禁整读** ——
  只读两段:**第 44 条**(`:1370` 起 · XD-47 / XD-44′ 前三次 / KG-B16 的一手现场)·
  **第 45 条**(`:1502` 起 · XD-44′ **第 4 次的非单调证据** / XD-52 / **KG-B18 的完整实证链**
  / KG-B15 第 4 次的性质差异))
- `/home/ys/codes/XenoDev/.scan-credentials-ignore`(**外部 repo 文件 · ⚠ Codex 沙箱可能 BLOCK** ·
  KG-B19 的现场。读不到时以 `_x-batch-snapshot.md` **Part 2 B-4** 为准,那里有完整转述 +
  commit `5442afd` + 逐条核对结果。**不要因读不到而产出「无此问题」型结论。**)

## Y · 审阅视角

✅ **架构设计**(**本轮唯一视角 · operator 刻意收窄**)

- 「声明存在但机制不存在」是否有**通用机制解**,还是必须逐点接线;逐点接线的完备性敞口是什么
- **warn / block 二态是不是正确的抽象** —— 已有三个 warn 机制 + 三条同形「≥2 次」判据 +
  一个判据达成两次仍未升级的直接反例
- 声明方与权威方的**职责划分**(`source_repo` 这类 consumer 侧有权威值的字段,
  该不该允许 producer 声明)
- **门与被门对象的绑定语义**(review gate 的输出该不该携带「gate 是否真跑过」这一位)
- 两条框架规约互不兼容时(worktree 规约 × 精确路径白名单)的**架构级消解**

❌ **不选工程纪律 / 安全**——见 §K 第 2 段。这是刻意的,不是遗漏。

## Z · 参照系

mode: **对标 SOTA**

**检索方向**(P2):
- **policy-as-code 的强制边**(OPA/Conftest · Kyverno · admission controller)——
  ⚠ v9 已取得反证:*OPA 只是 decision point,enforcement 接线必须应用自己做*。
  本轮要问的是**下一层**:成熟体系怎么保证「策略被接线」这件事本身不缺席
- **warning → error 的升级治理**(编译器 `-Werror` 演进 · linter 的 warn/error 分级 ·
  deprecation policy 的 sunset 机制)—— 「先 warn 后 block」的业界形态,
  **尤其:升级由什么触发、由谁执行、有没有自动到期**
- **技术债 / 例外的到期机制**(SonarQube issue 的 grace period · `# noqa` 与
  ratchet/baseline 模式 · Google 的 "no new warnings" ratchet)——
  对应「只减不增」健康度指标该怎么**被工具执行**而非被写在文档里
- **path/identity 声明在多 checkout 场景下的归一**(git worktree 与工具链的已知冲突 ·
  `.gitattributes`/`.gitignore` 的路径语义 · monorepo 工具的 root 解析)——
  对应 KG-B19 结构问题 2 与 KG-B17/B18 同族
- **review 终止条件的实证**(⚠ v9 已取到:70% 约 1-2 轮但精确轮次预测很差;
  **未取到任何支持统一停轮阈值的研究**)—— 本轮只补**「按被审对象关键性分级」**
  这个方向有无支撑(对应 A-1 的假说)

**外部材料叠加**:无

## W · 产出形态

✅ **verdict-only**(单一 verdict + 短 rationale)
✅ **decision-list**(8 条逐条:保留现状 / 调整 / 新增机制 / defer,四列矩阵;
  每条须标簇号 + **第 5 列 `evidence_grade`** + **第 6 列 obligation path(产生 gate → 消费 gate)**。
  🔴 **第 6 列必填** —— 它是 Phase 4 登记 obligation 的**唯一结构化抽取源**)
✅ **refactor-plan**(按簇分组;**mirror 件必须标 SSOT 侧改 → cp 回 mirror → MANIFEST SHA 更新
  的同步顺序** —— 簇 B 的 KG-B16/B17/B18 全部涉及 mirror,而 KG-B16 本身就是"只在单侧实装"的案例)

❌ **不产 next-dev-plan** —— **obligation ledger 的 `due_gate` 已严格覆盖其核心功能
(谁、在哪个 gate 前、必须做完什么),而且它有消费点、dev-plan 没有**。同一件事有两个载体、
其中一个没有消费点,等于给蒸发留后门(本仓已实证蒸发 3 次)。

## K · 用户判准

**为什么 forge 这一批**:八条分两簇,但我判断是同一根的两个面 —— 簇 A 是「写下的规则没有执行边」,
簇 B 是「声明存在但校验不存在」。我要的是这根的结构性回答,不是八个个案的处置清单。

**Y 只给架构设计是刻意的**。不接受、也不要产出「执行不力 / 该有人跟进 / 纪律要更严」型结论。
该解释已被本仓四次实证排除:XD-44′ 连续四次没有一次靠 codex 判 `approve` 结束,全部由 operator 叫停;
KG-B15 的升级判据在第 2 次就达成,达成后仍复发到第 4 次;v9 违反了 v8 给它下的 intake 义务
—— 那次决议、下发、留痕全做了,仍然蒸发。请把「人没做」当作**已排除项**,直接审结构。

**🔴 本轮最重要的一条自指约束**:簇 B 的止血手段自己全是 warn 型 —— `check-7`、`check-8`
都挂着「升级判据留 forge 定」,KG-B15 的 hook block 同样。**簇 A 的病正在簇 B 的解药上复现**。
因此:任何建议「再加一个 warn 型 check / 再记一条判据」的方案,**必须同时给出这条 warn 的
升级边由谁、在哪个 gate、凭什么触发**;给不出的不算解法。

**tradeoff 我的偏好**:通用机制解优先于逐点接线,但**不接受为了通用性而虚构抽象** ——
若证据只支持逐点接线,请直说,并给出逐点接线的完备性敞口。fail-closed 优先于 fail-open,
但追溯性执法(对存量语料硬拦)要单独论证。

**产出约束**:不要 next-dev-plan。排期由 obligation ledger 的 `due_gate` 承担 ——
同一件事有两个载体、其中一个没有消费点,等于给蒸发留后门。`decision-list` 第 6 列
obligation path **必填**,那是 Phase 4 登记 obligation 的唯一抽取源。

**一条今天刚拿到的正面实证,以及它的边界**:v9 建的 obligation gate 今天第一次真的拦下东西 ——
拦住的正是 v9 自己标为「最强 v10 触发判据」的 OB-006-v9-01,逼出了 74 天没做的白名单回审,
当场产出两条新发现。这是机制**有效**的证据。**但只有 1 个数据点**,不得据此推论机制已充分;
尤其注意它拦下的是 forge 自己这条链,build 侧四个消费 gate 至今全部 `consumer_wired: false`。

**回声室**:v8 已标注回声室风险高于 v7。v9 唯一一次真证伪来自 P2 单侧 SOTA,推翻的是
Opus 自己的地基。本轮同样要求 Codex 侧**优先证伪而非补强**。

**不要求本轮裁**:IDS 现存 ⏳ 授权条目(同 v9 的边界)。

## 收敛模式

**strong-converge** —— 必须 finalize 单一 verdict;残余分歧降级为 v0.2 note。
`unresolved` 仍可显式标出,不得为收敛而缝合。
