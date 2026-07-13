# X batch snapshot · forge 006 v8(权威快照 · Codex 首选阅读源)

> **Provenance**: 摘自 `/home/ys/codes/XenoDev/dogfood-backlog.md`(工作树 @ 2026-07-13,
> KG-B2/B3/B4 记于 2026-07-07/08,KG-B5/B6/B7 记于 2026-07-12/13,001-radar-pA build 周期实证)
> + operator worktree 隔离诉求(2026-07-13 口述原文)+ XenoDev CLAUDE.md 工作流摘录。
> 外部路径 Codex 沙箱可能 BLOCK —— 本快照自足,BLOCK 时以本文件为准。

## Part 1 · operator 新诉求(TEXT · 2026-07-13 原话)

「我发现后面有很多点子,都涉及 ids 和 xenodev 两仓切换。我发现尤其是 ids,经常很多 idea
混着进行,比如一会 001,一会 009。我觉得这个地方需要调整下,**每开一个 session,就在自己
独立的 worktree 下,working on 一个 idea,不相互干扰。xenodev 也一样。只有在刚开始
proposal 的时候用 main 分支**。」

**实证(IDS 侧,本周)**:当前 session 名义在 `forge/009-blueprint` 分支,实际连续三天做
001 治理(handback-review×3 / PRD v1.1→v1.2 / L3 injection×2 / forge 006 v8 kickoff),
20+ commits 混在一根 009 命名的分支上;001/006/009 三个 idea 的文档变更交错入同一分支历史。
**关联既有机制**:codex inbox/outbox v2 已按 queue-per-idea 隔离(README 明言多 idea 并行
不再冲突),但 git 分支/worktree 层与 session 层无对应隔离约定;XenoDev 侧 KG-B2(基线偏离)
同属「并行 fork 的分支拓扑无显式规约」一族。

## Part 2 · KG-B2..B7 六条框架缺口(dogfood-backlog 原文全文)

### KG-B2(001分支发现 · 与KG-B1同源 · medium) · parallel-builder 隐含「一切 merge 回 main」· blocked-handback 的 fork 代码留 feature 分支 → build 基线偏离(worktree off main / depends_on 查 main 都语义错)
- 日期: 2026-07-07(001-radar-pA T002 起跑 · §0.1 preflight + §1.2 worktree 创建阶段发现)
- 类型: 框架缺陷(SKILL 拓扑假设 · parallel-builder §0.1 depends_on gate + §1.2 worktree base 都硬编码 main 为基线)
- 严重度: medium(不硬阻断 —— operator 可决基线改 feature 分支绕过;但 SKILL 字面照跑会炸:worktree off main 里没有前置 task 的代码,import 立刻 fail;且 depends_on gate 查 main 会误报「未 merge」)
- 复现场景: 001-radar-pA 因 KG-B1(hand-back blocked)· operator 决「先 merge 代码 · hand-back 缓回流」→ T001 代码 merge 到 **feat/001-radar-pA-spec**(不进 main)。起 T002 时:① §0.1 depends_on gate `git log main | grep T001` **查不到**(T001 只在 feature 分支)→ 误报未 merge;② §1.2 `git worktree add ... -b task/... main`(off main)起的 worktree **没有 T001 的 radar/domain + radar/interfaces** → T002 import 接口即炸。根因:SKILL 隐含「每 task ship 即 merge 回 main · main 永远是最新集成基线」,但 **blocked-handback 的 fork 代码被迫留 feature 分支缓回流**(KG-B1 导致)→ 打破该假设 → build 基线偏离。撞面 = 任何因 hand-back blocked / 尚未回流而把代码留在 feature 分支上继续多-task build 的 fork(与 KG-B1 同源:都是「代码回流受阻 → 留 feature 分支 → 偏离 SKILL 拓扑假设」的下游症状)。
- 关联: parallel-builder §0.1(depends_on gate 硬编码 `git log main`)· §1.2(worktree `-b task/... main` 硬编码 base=main)· KG-B1(上游根因 · hand-back blocked 逼代码留 feature 分支)· 多-fork 并行拓扑(同 KG-B1 附带的多-fork 假设漏洞)
- operator 确认: <留空 · 待 operator review(框架级 · parallel-builder 是 XenoDev 自派生 SKILL · 但改拓扑假设影响 ship 收口纪律 · 攒批回 IDS forge 一并议)· 建议方向:① parallel-builder §0.1/§1.2 引入「build 基线」参数(默认 main · 可显式指定 feature 分支 · 覆盖 depends_on gate 查询目标 + worktree base 两处);② 或规约「blocked-handback fork 必须显式声明其集成基线分支」· gate/worktree 都读该声明;③ 与 KG-B1 联动:KG-B1 修好后代码回流 main · 基线偏离自然消解 —— 但在回流受阻窗口内 SKILL 需支持 feature-branch 基线。本次 operator 决基线改 feat/001-radar-pA-spec 继续 · 记此缺口不当场改 SKILL>

### KG-B3(001-T002发现 · medium) · red-green-log TDD 证据日志被根 .gitignore `*.log` 吞掉 · 豁免规则 `!tests/**/red-green-log/*.log` 假设 tests/ 在仓根 · 但 XenoDev 项目在 projects/<feature>/tests/ 下 → 豁免失效 → §4.4 verifier 的 TDD 机器证据无法随 commit 留存
- 日期: 2026-07-07(001-radar-pA T002 · §2.1 negative test red 后 git add T002.log 阶段发现)
- 类型: 框架缺陷(bootstrap .gitignore 与 parallel-builder §4.4 red-green-log 证据要求不自洽 · 路径锚定假设错)
- 严重度: medium(不硬阻断 build —— worktree 内文件系统仍有 log · §4.4 能查到;但 TDD 证据**无法入 git** → merge squash 后可能丢 → 「red 先于 green」的机器可审计证据链断在 git 层。**已实证 T001 也中招**:T001.log 从没进 git(git ls-files 空)· 说明 T001 ship 时 §4.4 的「red-green log 存在」只靠 worktree 文件系统过关 · 未真入仓)
- 复现场景: T002 写完 negative test 跑出 red(rc=2)· 落 tests/red-green-log/T002.log · git add 报「路径根据 .gitignore 被忽略」。check-ignore -v 显示命中根 .gitignore:64 的 `*.log`。根 .gitignore:66 **有**豁免 `!tests/**/red-green-log/*.log`,但**不生效** —— 因 gitignore 的 `tests/**` 锚定在 .gitignore 所在目录(仓根)的 tests/,而 XenoDev 项目真实路径是 `projects/001-radar-pA/tests/red-green-log/T002.log`(tests/ 前有 projects/<feature>/ 前缀)→ 豁免 pattern 不匹配 → `*.log` 兜底吞掉。根因:.gitignore red-green-log 豁免规则假设「tests/ 直接在仓根」· 但 XenoDev 的项目结构是 `projects/<feature>/tests/` · 二者路径假设冲突。
- 关联: 仓根 .gitignore L64(`*.log`)+ L66(豁免 `!tests/**/red-green-log/*.log`)· parallel-builder §4.4(要求 tests/red-green-log/<TID>.log 作 TDD 机器证据)· §2.1/§2.4(red/green 落该 log)· 撞面 = 所有 projects/<feature>/ 下的 task(即所有 XenoDev 真项目 build · 通用)
- 项目内即时修(不算框架改动 · 只调本仓 .gitignore 豁免 pattern): 把豁免从 `!tests/**/red-green-log/*.log` 改为 `!**/red-green-log/*.log`(匹配任意深度前缀 · 含 projects/<feature>/tests/)· 本次 T002 已如此修让证据能入仓。
- operator 确认: <留空 · 待 operator review · 框架侧根治建议:bootstrap-kit 的 .gitignore 模板把 red-green-log 豁免改为 `!**/red-green-log/*.log`(路径无关)· 或 parallel-builder bootstrap 时对每个 projects/<feature>/ 显式写豁免。**本次项目内已修 .gitignore(非框架改动)· 框架侧模板缺口记此攒批回 IDS forge**>

### KG-B4(001-T004发现 · medium-high) · gate 类 task 的 PASS 判定无机器强制 · parallel-builder 靠「读 depends_on markdown 约定」拦下游 · 无代码验证 gate PASS artifact 存在 → gate STOP 可被绕过(尤其防 V4 的 prd-revision-trigger gate)
- 日期: 2026-07-08(001-radar-pA T004 · PPV P1 盲测 gate build · code-reviewer/red-team 双跑发现 · red-team F6 + code-reviewer 佐证)
- 类型: 框架缺陷(parallel-builder gate 强制机制 · gate 类 task 的「PASS 前下游不起」只是 SKILL 读 markdown depends_on 的约定 · 非机器可验证不变量)
- 严重度: medium-high(不硬阻断当前 build · 但**削弱 gate 的立法本意**:T004 是防 V4 失败模式的 prd-revision-trigger gate · 「FAIL → STOP 不降级」的保证若只靠 parallel-builder 读 depends_on 的程序纪律 · 一个赶时间/困惑的 agent 或 operator 可以不跑 evaluate_gate 就起 T010/T011 · 代码层无任何拦阻。撞面 = 所有 gate 类 task(尤其 PPV gate / prd-revision-trigger gate · 这类恰是最需要硬强制的))
- 复现场景: T004 P0.2 位移可信性盲测 gate build。`evaluate_gate` + `write_prd_revision_trigger` 是纯库函数(radar.credibility 导出)· 但**没有任何生产代码路径调它们**(grep 全 src/ · CLI 只产盲测叙事+签字模板 · 不调 gate 判定)。gate 的 PASS/FAIL 判定 + 「STOP 不起下游」全靠:① task-decomposer 在 DAG 里写 T010/T011 depends_on=[T004];② parallel-builder §0.1 读这个 depends_on markdown 判「T004 已 merge?」。但「T004 已 merge」≠「T004 gate PASS」—— gate 代码 merge 了不等于 operator 盲测签了字 PASS。**没有机器检查**验证「verification/P0.2-*.md 签字文件存在且 evaluate_gate 判 PASS」才放行 T010/T011。红队原话:STOP 是 markdown 约定不是 enforced code block;code-reviewer 佐证:nothing in shipped code calls evaluate_gate on a signoff artifact or gates subsequent action on its return。
- 关联: parallel-builder §0.1(depends_on gate 只查「dep task 已 merge」· 不查「gate task 的 PASS artifact」)· T004 的 evaluate_gate/write_prd_revision_trigger(库函数无 wiring)· HANDOFF §4-OQ1(防 V4:gate FAIL 即 STOP)· 撞面 = 所有 gate 类 task
- 可能的框架侧解法(留 forge 议): ① parallel-builder §0.1 对「标了 gate 语义的 task」(task frontmatter 加 `gate: true` 或 blocks 里有下游)· 除查 merge 外**额外查 gate PASS artifact**(如约定 verification/<gate>-PASS.md 存在 + evaluate_gate 判 PASS);② gate task 的 ship 收口强制跑其 evaluate_gate 并落一个机器可读 PASS/FAIL record · 下游 preflight 读它;③ task-decomposer 对 gate task 产额外的「PASS 前置检查脚本」· parallel-builder 起下游前必跑。**本仓不当场改 parallel-builder(SKILL · 攒批回 IDS forge)· 项目内 T004 已把 gate 判定逻辑做成可调库函数(evaluate_gate)· 缺的是框架层把它接进下游 preflight 的强制点**。
- operator 确认: <留空 · 待 operator review · 框架级 · 与防 V4 强相关(gate 是防 V4 的核心机制 · 其强制性不该只靠程序纪律)· 攒批回 IDS forge · 建议与 KG-B2(parallel-builder gate/基线机制)同簇审>

---

## ⬇ forge v7 处置结果回填(2026-07-08 · IDS 治理仓 forge 006 v7 verdict)

> **这不是新缺陷条目**,是 forge v7 对上面已记 KG(簇1 五条 + KG-B1)的**处置回填**,append 在此供 XenoDev session 对照落地。
> **权威文档**:IDS `discussion/006/forge/v7/stage-forge-006-v7.md`(verdict + decision matrix + refactor plan)
> **授权 brief 全文**:IDS `discussion/006/forge/v7/AUTHORIZATION-BRIEF-v7.md`(本回填的完整版 · A1-A4 + C1-C5 + 落地顺序)
> **operator 落地决策**:选项 [B] 局部先落 P0 · D0=严格守铁律(契约先行) · D1=只落止血核心 · D2=IDS+XenoDev 两处都留档

### verdict 一句话
refactor,不 redesign、不 cut codex。簇1 五条 KG = review gate 单点依赖的同根 5 失效切面;codex 保 primary + 外包「review 通道状态机」(circuit breaker 四要素)。KG-B1 拒第三次逐例放宽 regex,fork-id 语法进 SHARED-CONTRACT 作跨仓 SSOT + FULL 兼容 001-radar-pA + 双仓 fixture 契约测试。

### IDS 侧本轮已落(2026-07-08)
- ✅ **SHARED-CONTRACT §7 · fork-id 语法 SSOT**(新章):v7 grammar `^[0-9]{3}[a-z]?(-[a-z0-9]+)*(-p[A-Z][a-zA-Z0-9]*)?(-v[0-9]+\.[0-9]+)?$` · 相对 v0.3 唯一变化 = 新增中段 `(-[a-z0-9]+)*` · 全量 23 真实已铸 id 语料全绿 + traversal 异常全拒 · 已知语义弱化(-p 大小写)由铸造侧兑保
- ✅ **SHARED-CONTRACT §6.2.1 约束 6** 引用改造:正则字面量不再内嵌 · 统一引用 §7 SSOT(终结「铸造侧与校验侧各自演化正则」= KG-B1 根因)

### XenoDev 侧待改源(授权条目 · 本轮不当场改 · 见 AUTHORIZATION-BRIEF-v7.md 全文)
- **A1**(P0 · 解阻)`handback-validator/check-6-id-charset-and-final-path.sh` §1.2 regex → §7.2 SSOT 值。改完 cp -p 回 IDS mirror + 更新 MANIFEST SHA + 跑 mirror-sha 测试。**A1 完成 = 001-radar-pA 解阻**(本轮 IDS 守铁律未当场改 mirror · 解阻等这一跳)。
- **A2**(P0)codex-review SKILL 状态机止血核心 4 处:失效三分类(KG-32/37/38)/ scope+空 diff 拦截(KG-23)/ 降级链交叉矩阵 / fallback 审计标注。watchdog 阈值 + 完整 breaker + half-open 标 v0.2 靠真跑校准,本轮不做(D1)。
- **A3**(P0)KG-35 verdict 提取三级 fallback 链(主 log → status --all summary → job logFile)· operator 提级与 KG-23 空 diff 同批(同属假绿病族)。
- **A4**(P0)双仓契约 fixture 语料三类(旧 id 全过 / 新三段式 / traversal 异常必拒)· IDS 铸造侧 + XenoDev 接受侧同语料各跑。
- **C1-C5**(P1/P2)companion watchdog+status/result 语义 / gen-handback fork-id 参数化 / KG-33 守卫告警(根因待复现)/ KG-34 migration 硬 checklist / 长任务 flock 单实例锁。

### 与 KG-B2 / KG-B4 的关系(v7 未审 · 下批 forge 料)
- **KG-B2**(parallel-builder「一切 merge 回 main」假设被 blocked-handback 打破):**是 KG-B1 的下游症状**。A1 解阻 001-radar-pA 后,代码回流 main,基线偏离自然消解——但**回流受阻窗口内 parallel-builder 需支持 feature-branch 基线**这条 SKILL 拓扑缺口,v7 未审(不在 X 快照),留下批 forge。
- **KG-B4**(gate 类 task PASS 判定无机器强制 · 防 V4 gate 可绕过):v7 未审 · 与防 V4 强相关 · 建议下批与 KG-B2 同簇审(都是 parallel-builder gate/基线机制)。

---

## KG-B5 · LlmClient Protocol 无 system/user role 分离 → prompt-injection 防御只能靠 prompt 内文本边界(whack-a-mole)(2026-07-12 · 001-radar-pA T003-A2)

- **判别**:框架级(LlmClient interface 契约层 · 撞面 = 所有用这套 framework 调 LLM 且喂不可信外部数据的 task/项目)。
- **真实复现(forge 硬证据)**:
  - 开发 001-radar-pA T003-A2(abstract 输入:LLM 结构状态提炼输入从 titles 扩到 title+abstract)· abstract 来自公开检索源(不可信)。
  - codex adversarial-review **连跑 6 轮 needs-attention**(operator 两次授权破 4 轮上限),每轮找到一个更冗余的 prompt-injection 绕过向量:R2 二阶注入(structural_state 裸拼指令流)→ R3 变体闭合标签(`</PAPERS>`/`< /slice_states>`)→ R4 ASCII-only 转义自败(`‹›` 是替换字形本身)→ R6 Unicode 角括号 lookalike(U+3008 `〈〉`/U+27E8 `⟨⟩`/U+300A `《》` NFKC 不折)。
  - **根因 codex 在 R2 已点破**:「边界只靠单字符串 prompt 让模型理解,并没有真实 parser 强制隔离」。用 `<papers>...</papers>` 数据块 + "证据非指令" 声明做隔离,本质是 prompt 内文本边界 —— 任何能被模型视觉识别为闭合标签的字形都是绕过面,denylist 是无穷 whack-a-mole。项目内最终改 allowlist(只留安全字符白名单)结构性封类,但那是**没有 role 分离前提下**的次优兜底。
- **关联**:T001 `LlmClient` Protocol(`complete(prompt: str) -> str` · 单字符串入口 · 无 system/user/data 分离)· 撞面 = 未来任何喂不可信数据(检索语料/用户输入/外部 API 返回)进 LLM 的 task。
- **可能的框架侧解法(留 forge 议)**:① `LlmClient` Protocol 加 messages-style(system=指令 · user=数据)· provider 层(DeepSeek/Anthropic 都支持 role)做真隔离 · 不可信数据永不进 system;② 提供框架级 `sanitize_untrusted_field()` 工具(allowlist 序列化 · 本次项目内手搓逻辑上提到 lib/);③ spec-writer/task-decomposer 对「喂不可信数据进 LLM」的 task 默认要求 role 分离 + 注入回归测试(进 PPV 反模式)。
- **不当场改**:改 T001 `LlmClient` = 动冻结 interface = 契约变更(防 V4 · 攒批回 IDS forge)。项目内 T003-A2 已用 allowlist+decode 序列化兜底(v0.1 自用风险可控)。
- **⬆ 更新(2026-07-13 · T003-A2 ship 决策)**:codex adversarial-review 最终跑到 **9 轮 5 个注入面 finding**(单字符 lookalike → 变体标签 → ASCII 转义自败 → Unicode 角括号类 → letter-class isalnum → 多字符 HTML/percent 编码)· **string-sanitize 防注入证实不收敛**(每轮一个新编码面 · base64/双编码/零宽拼接理论上还有)。operator 决策:**修当前已知编码面后 ship T003-A2**(allowlist+decode 是 v0.1 defense-in-depth bound 非 proof)· **残留"未知编码面"= 本 KG-B5 硬 followup**(真根治 = LlmClient role 分离 · data 永不进指令通道)。代码内已留 `# NOTE (KG-B5):` 注释指向本条。**这是 forge 高优先条目**(注入防御无 role 分离时无终点是硬证据)。
- **operator 确认**: <留空 · 待 operator review · 框架级 · AI-security(prompt injection)· **9 轮 review 成本 = 真实硬证据**:无 role 分离时 string-sanitize 防注入是无底洞 · T003-A2 已 ship-with-followup · 攒批回 IDS forge 高优先>

## KG-B6 · credential-isolation hook(件1 C12)对 heredoc / 变量拼路径 / `$(...)` 命令替换误报 fail-closed(2026-07-12 · 001-radar-pA ship 流程多次撞)

- **判别**:框架级(Safety Floor 件1 hook · 撞面 = 所有用 heredoc 写多行 commit message / 变量拼路径 / mktemp 命令替换的 ship 流程 · 即几乎所有 parallel-builder ship)。
- **真实复现**:
  - 001-radar-pA ship 流程(T002-A1 / T003-A1 hand-back · T003-A2 fix commit · **本 backlog 条目的 heredoc append 本身**)多次撞 hook `read-util + 动态路径前缀(命令替换/变量拼路径)· 静态不可判真实路径 → fail-closed(凭据隔离 C12)`。
  - 触发模式三类:① `$IDS_ROOT`/`$PRIV_DIR` **变量拼路径**传给 ls/cat;② `$(mktemp -d)` **命令替换**赋值路径变量;③ `git commit -m "$(cat <<'EOF' ... EOF)"` **heredoc + cat 替换**写多行 commit(subagent 也独立撞到)。
  - 现象:合法操作被 fail-closed 拦(非真读凭据)· 每次改用字面路径 / `git commit -F <file>` / Edit 工具绕。
- **关联**:`.claude/safety-floor/credential-isolation/`(件1 · C12 零片段合成防御)· 撞面 = parallel-builder §6.1 范式(mktemp 私有 dir + 变量路径是 SKILL **明写**的范式,与件1 hook 直接冲突)+ 任何多行 commit(Conventional Commits 常用 heredoc)。
- **可能的框架侧解法(留 forge 议)**:① hook 对 `git commit -m "$(cat <<heredoc)"` 这个已知安全的 commit-message 惯用法加白;② parallel-builder §6.1(mktemp 私有 dir)与件1 hook 冲突需协调(SKILL 改固定 scratchpad 路径 · 或 hook 放行 mktemp);③ 文档化「撞 C12 的标准绕法」进 parallel-builder known-gotchas。
- **不当场改**:件1 是三件硬约束之一(non-overridable)· 记 backlog。项目内已用字面路径 + `git commit -F` + Edit 工具绕(不阻塞)。
- **operator 确认**: <留空 · 待 operator review · 框架级 · 件1 hook 与 parallel-builder §6 范式冲突 · 高频撞(每个 ship 都可能)· 攒批回 IDS forge>

## KG-B7 · P0.2 盲测 gate 对「动机 operator 试错/重放取盲测答案」的威胁模型需框架层单次执行强制(2026-07-13 · 001-radar-pA T004-A1)

- **判别**:框架级(gate 机器强制的**执行语义**层 · 非 gate 判定逻辑 · 撞面 = 所有「人在环 + 机器对答案」的 gate · 尤其防作弊/反橡皮图章 gate · 同 KG-B4 族)。
- **真实复现(forge 硬证据 · codex adversarial-review 连出 3 轮同族 bypass)**:
  - 开发 001-radar-pA T004-A1(P0.2 要件③ gate operationalize)· codex adversarial-review **round 12-14 连出 3 个同族真结构假 PASS**,都是「operator 可取/重放盲测答案」:
    - **R12 replay**:签字无 run 绑定 → 旧 run 的 PASS 签字重放到新失败 run 铸 RERUN-PASS。修:run_id 绑定。
    - **R13 run_id 泄露**:R12 的 run_id digest 了低熵(31-bit seed)answer-key → operator 爆破 seed 反推负控位置。修:run_id 改 256-bit 独立 nonce(不 digest answer-key)。
    - **R14 FAIL-reason 泄露**:gate FAIL reason 直接写出负控 slice_id → operator 先错签字取答案 → 改签字重跑 PASS(试错 oracle)。修:FAIL reason 泛化(不出具体 control id)。
  - **根因(设计层)**:gate 是**确定性机器对答案** + answer-key **可复用**(seed 确定性)+ operator **可无限重跑**(无单次执行强制)。逐个补泄露面(run_id/reason/文件名)是必要但不充分——只要 operator 能**重跑**且 answer-key **不变**,试错攻击面无法在 gate 代码内彻底关闭。
- **关联**:`credibility/gate.py`(FAIL reason)· `injector.py`(AnswerKey seed 确定性 · run_id)· `cli/reconstruct.py`(重跑入口)· **KG-B4**(gate PASS artifact 无机器强制 · 同属 gate 执行语义框架缺口)· RT-1 反橡皮图章(本 gate 核心防线)。
- **可能的框架侧解法(留 forge 议)**:① **单次执行强制**——同一方向/answer-key 的盲测 gate 每 answer-key 只允许判一次(harness/parallel-builder 层记录已判 run · 拒重跑同 answer-key);② **签字不可变 + 时序绑定**——签字必须在 answer-key 生成后、gate 判定前的单调时间窗内产生 · 判定后 answer-key 作废;③ **answer-key 一次性**——每次重跑强制新 seed + 新 answer-key(operator 无法复用上次的答案 · 但 operator 仍可对新 run 试错 → 需配合 ①);④ 把「盲测反作弊威胁模型」整体形式化进 SHARED-CONTRACT gate 契约(单次执行/不可变签字/answer-key 一次性 三要素)。
- **不当场改**:gate **执行语义**强制(单次执行/不可重跑)属**框架层**(parallel-builder/harness · 同 KG-B4)· 不在 XenoDev 项目内建(防 V4)。项目内 T004-A1 已逐个封当前已知泄露面(run 绑定 + nonce + reason 泛化 · v0.1 自用风险可控:operator 是自己 · 无对抗动机)· 代码留 `# NOTE (KG-B7)` 注释。
- **operator 确认**: <留空 · 待 operator review · 框架级 · **AI-security/gate 反作弊** · codex 3 轮同族 bypass = 硬证据:gate 代码逐个补泄露面不充分 · 真根治 = 框架层单次执行强制 · 与 KG-B4 同簇(都是 gate 执行语义框架缺口)· 高优先攒批回 IDS forge>

## Part 3 · XenoDev CLAUDE.md 工作流相关摘录(供 worktree 隔离议题参照)

## 工作流(per stage doc §"模块 B")

```
1. operator cd XenoDev
2. cat /Users/admin/codes/ideababy_stroller/discussion/<id>/<prd>/L4/HANDOFF.md
3. cp PRD 进 XenoDev/PRD.md
4. spec-writer 产 specs/<feature>/spec.md(7 元素 + PPV)
5. task-decomposer 产 tasks/T*.md
6. parallel-builder 跑 task → ship
7. 每个 task ship 后产 hand-back 包(§6.3 schema)
8. 跑 lib/handback-validator/validate-handback.sh(6 约束自检)
9. 写到 IDS discussion/<id>/handback/<ts>-<id>.md
10. operator 在 IDS 跑 /handback-review <id> 决议
```

## 跨仓引用

> **路径可移植(迁移收口)**:下方绝对路径是**旧机(macOS)示例**。framework 脚本(gen-handback / verify-ppv-* /
> 测试)已 env 化 —— 读 `${IDS_ROOT:-<默认>}` / `${XENODEV_ROOT:-<默认>}`。**新机(如 Ubuntu /home/ys/codes)
> 只需 `export XENODEV_ROOT=... IDS_ROOT=...`**(写 shell profile),不改源码。迁移清单见 `docs/MIGRATION.md`。

- **IDS 仓路径**:`/Users/admin/codes/ideababy_stroller`(只读;SSOT · 新机 `$IDS_ROOT`)
- **autodev_pipe(V4)**:`/Users/admin/codes/autodev_pipe`(已 archive,只 mirror block-dangerous.sh)
- **SHARED-CONTRACT**:本仓 `framework/SHARED-CONTRACT.md` 是 IDS SSOT 的字节级 mirror,只读

## 偏好(per `~/.claude/CLAUDE.md` 全局)

- 提交信息:Conventional Commits(feat/fix/chore/docs/test/refactor)
- 不主动 `git push`,push 前需 operator 确认
- 代码注释中文 / 先结论后细节
- TDD for production code
- 报错信息真实粘贴(不只说"有错误")

## dogfood 铁律(框架问题捕获 · 必守)

> **结论先**:开发任何项目时,一旦发现**框架级**缺陷 / bug / 优化空间,**立即** append 到仓根
> `dogfood-backlog.md`(按其顶部模板),不要等、不要只在脑子里记。operator 用 XenoDev 真开发时
> 专注在项目上,容易忘记框架问题 —— 这条铁律就是防漏。

- **判别**:改的是「框架本身」(协议 / SKILL / hand-back / mirror / 并发机制 / 这套 framework 用起来的痛点)
  → **记 `dogfood-backlog.md`**;改的是「在建项目的功能」→ 项目内迭代,**不记**。
  一句话:修好后受益的是「以后所有用这套 framework 的项目」→ 记;只「当前这个项目」→ 不记。
- **不当场改框架**:框架级变更**绝不在 XenoDev 当场改**(下方铁律 + 「不动 SHARED-CONTRACT / 不复制 forge」)
  → 记 backlog → 攒批回 IDS forge。当场改 = 绕过治理 = V4 失败模式。
- **复现场景最值钱**:记条目时把「在开发什么、跑到哪步、怎么触发、现象」写具体。真实复现 = 回 IDS
  forge 的硬证据(forge v5 教训:审没真跑过的东西容易跑偏)。

## 当出问题时(决策矩阵 · 何时切回 IDS vs XenoDev 内处理)

| 信号 | 处理 | 怎么做 |
|---|---|---|
| **框架级缺陷 / bug / 优化空间**(协议 / SKILL / hand-back / mirror / 并发) | **记 backlog · 攒批回 IDS forge** | append `dogfood-backlog.md` → 阶段性随 hand-back 回流 → 回 IDS `/expert-forge 006` |
| **在建项目的功能改动** | **XenoDev 内迭代** | 正常开发,不回 IDS,不记 backlog |
| **PRD 约束不可达 / spec 与 PRD 矛盾** | **切回 IDS 修 PRD** | 产 hand-back → operator 在 IDS 跑 `/handback-review 006` → `/scope-inject` 改 PRD |
| **重大架构转向** | **必须先 forge,不静默停**(防 V4 失败模式) | 在 IDS 仓 `/expert-forge 006`(forge 永远在 IDS 治理仓) |
| **Safety Floor 违反**(凭据 / 不可逆命令 / 备份破坏) | **停 + escalate IDS** | hard-fail · 不静默绕过 · 见三件硬约束 |
| **hand-back 6 约束 / validator 不通** | **先自查再 escalate** | 跑 `bash lib/handback-validator/validate-handback.sh <file> /Users/admin/codes/ideababy_stroller` dry-run |

**排查顺序**(具体问题):
1. 先看 `.eval/events.jsonl`(operator interventions / review_failures)
2. 跑 hand-back validator dry-run(见上表末行)
3. 框架级问题 → 记 `dogfood-backlog.md`(别当场改)→ 攒批回 IDS forge
4. 重大架构转向 → 必须先 forge,不静默停(防 V4 失败模式)

> **跨仓边界 SSOT**:更详尽的两仓分工 / hand-back schema / workspace 校验见 IDS
> `framework/SHARED-CONTRACT.md` §6(本仓有只读 mirror)。本段是"何时切回"的快速决策入口。

