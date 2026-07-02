# Forge v6 · P1 · Opus 4.8 Max(独立审阅)

**Phase**: 1（独立现状审阅 · 无 web search · 无 SOTA 对标 · 无修法详案）
**Reviewer**: Opus 4.8 Max
**X read**: 5 槽全部一手读取(backlog 快照 KG-26..30 段 / plan-start.md HANDOFF 模板 / SHARED-CONTRACT §6.2 / XenoDev 三 SKILL 热点行 / KG-29 fix diff + 009 两包 PASS 实证 / gen-handback + validator papercut)

---

## §0 · 我读到的标的 + 阅读策略 + K 摘要

**读取清单(全部一手 · 无 fallback)**:
- 槽1 backlog 快照:KG-26/27/28/29/30 五条全文(696 行文件聚焦这 5 段)
- 槽2 KG-26 现场:`plan-start.md` HANDOFF 模板(`build_repo: /Users/admin/codes/XenoDev` + §1 `cd /Users/admin/...`)+ `SHARED-CONTRACT.md` §6.2(4 字段示例表 + YAML 全 mac)
- 槽3 KG-27/28/30 现场:三 SKILL 热点行(spec-writer L94-96 · codex-review 8+ 处 mac+1.0.3 · parallel-builder L17/L58/L135-151)
- 槽4 KG-29 追认:commit `7164381` diff + 009 两包 6 约束全 PASS 实测
- 槽5 evidence:gen-handback 产包 mac 路径 + validator 相对路径 papercut

**阅读策略(按 Y)**:
- 视角=跨机器可移植性 → 逐处定位"某台机器的绝对形态被当默认值写死"的字面量(路径/版本/目录),判断每处是"字面硬编码"还是"逻辑本身对只是 base 写死"。
- 视角=工程纪律 → 追每处硬编码的 **SSOT 层级**(条款/实装/mirror 哪一层),判断修一处会不会漏同族;查 KG-29 已修部分是否留了半同步态。

**K 摘要**:5 条同根 = 框架把某台 mac 的环境形态硬编码成默认(路径/版本/env/目录)。要**系统性修法**(环境假设住哪层 + 一次清扫 + 防再漂移)非逐处补丁。KG-29 已 operator 直接决策修(追认审安全,不推翻)。守 binding:框架变更只走 forge / SSOT 三层同步不留半同步态 / 不推翻 009 已 ship / 双机非发行(不过度工程) / 轻收尾可执行优先。

---

## §1 · 现状摘要（按 Y 视角）

### Y1 · 跨机器可移植性

**核心事实:硬编码不是"多处巧合",是一个可辨认的分层结构。** 我把 5 条按"硬编码了什么"归类,浮现三类:

**(A) 硬编码绝对路径**（KG-26 + KG-27 base 目录 + X#5 gen-handback）。字面量 `/Users/admin/codes/XenoDev`（build_repo / cd 指令 / workspace 4 字段示例 / gen-handback 产包的 to_source_repo）与 `/Users/admin/.claude/plugins/...`（codex base 目录）。这些是"某台 mac 的绝对布局被当默认值"。关键观察:**其中有的字段本该是运行期值,却被塞进了模板/示例字面** —— 如 `plan-start.md` 的 `build_repo`,我上次产 009 HANDOFF 时是用 `realpath` 手填对的,说明"生成时可推断"这条路是通的,只是模板没走。

**(B) 硬编码版本号**（KG-27 codex-review 的 `1.0.3`）。这是最"会持续腐烂"的一类 —— 与路径不同,路径换机器才错,版本号**同机器 codex 一升级就错**(本机已是 1.0.4)。而且同一个 codex-review SKILL 内部**自相矛盾**:spec-writer 用的是 `codex/*/scripts/...` glob + `sort -V | tail -1`（版本无关,**正确范式**),但 codex-review 里 8+ 处写死 `1.0.3`。即**正确修法在同一仓已存在**(spec-writer 的 glob),只是没推广到 codex-review / parallel-builder。

**(C) 硬编码环境/目录形态假设**（KG-28 env 就位 + KG-30 log 落仓根）。KG-28:parallel-builder 假设 `uv`/`.venv`/可达 pypi/新鲜 lock 都就位(SKILL 本身 0 处 `uv run` —— 假设藏在 task 的 Verification 块 + "env 天然在"的隐性前提)。KG-30:red-green log `tee` 到相对路径 `tests/red-green-log/`,假设它落仓根(不被 ignore),但 build mirror 子项目(004-pB)时落子树、被子树 .gitignore 挡。这两条是"目录/环境的形态假设",比路径字面更隐蔽。

**一句话现状**:三类(路径 / 版本 / 环境形态)本质是同一个反模式——**把"我这台机器现在长这样"固化进了框架**。单机永不暴露,跨机器全暴露。

### Y2 · 工程纪律

**SSOT 三层视角下,问题更清楚也更麻烦。** 框架有三层 SSOT:① 条款 `SHARED-CONTRACT.md`；② 实装 `framework/xenodev-bootstrap-kit/`；③ XenoDev `lib/`（②的 mirror）。5 条缺陷散落在不同层:
- KG-26 在 ①(条款示例)+ IDS 命令(`plan-start.md`)
- KG-27/28/30 在 XenoDev SKILL（`.claude/skills/` —— 注意这**不在**三层 SSOT 里,是 XenoDev 自派生的 skill,不走 mirror）
- KG-29 在 ①条款 + ②实装 + ③mirror **全三层**

**KG-29 暴露的纪律问题最尖锐**:它现在是**半同步态**。我上一步修了 IDS 的 ①②(commit 7164381),但 ③ XenoDev mirror 靠 operator 手动 apply patch 才补上。这正是 K binding② 要防的——**修法若不能"两仓一次落地",就会反复产生半同步窗口**。而 shared-lib-drift(v5 已列)说明这个手动 mirror 机制本身就是脆的。

**另一个纪律观察**:KG-27/28/30 所在的 XenoDev `.claude/skills/` **不走 mirror 机制**(是 XenoDev 自派生)。所以这三条的修法**只在 XenoDev 落地**,不涉及 IDS 三层同步 —— 但 forge 在 IDS 决议,决议后要下发 XenoDev 半边 brief。这是 v4→v5 的既有模式,v6 沿用。

---

## §2 · First-take 评分（keep / refactor / cut / new）

| 项 | 评 | 理由 |
|---|---|---|
| **KG-27 的 `codex/*/scripts + sort -V` glob 范式**（spec-writer 已用) | **keep + 推广** | 版本无关的正确范式,同仓已存在。修法核心 = 把它推广到 codex-review/parallel-builder 的所有 `1.0.3` 写死处,**不是发明新东西** |
| KG-26/27 的 mac 绝对路径字面量 | **refactor（系统性）** | 环境假设住错了层。核心决策:住哪层(生成时 `realpath`/`git config` 推断 vs 环境变量 vs 运行时探测)。这是 v6 最大设计决策 |
| KG-27 的 `1.0.3` 版本钉死 | **refactor（P0 优先）** | 会持续腐烂(同机升版即错),比路径更急。修法确定(glob+sort -V),几乎机械 |
| KG-28 env preflight 缺失 | **new（加 preflight）** | 框架缺一个能力(新机 build 前的 env 就位检查/文档)。但要防过度工程(K binding④双机非发行) |
| KG-30 log 落点 | **refactor（二选一）** | (a) log 强制落仓根绝对/仓根相对路径,或 (b) §4.4 verifier 对子项目 ignore 情况降级。改动小 |
| KG-29 charset 放宽 | **keep（追认）** | 已修已跑通,不推翻。**唯一要审 = 放宽有无安全隐患**（见 §3） |
| X#5 gen-handback mac + validator papercut | **refactor（并入 KG-26 射程）** | 同族,别漏。gen-handback 的 to_source_repo 该同 KG-26 一起改;validator 相对路径 papercut 是独立小修 |
| **防再漂移机制**（现无) | **new（关键）** | 5 条能同时存在,根因之一是**没有任何守卫拦"新硬编码"进来**。若不加(lint / grep-gate / CI check),修完过阵子又漂。这是 v6 该产的最有价值的"新增" |

**评分总结**:没有一条要 cut。主体是 refactor(系统性,非逐处),一条 keep+推广(glob 范式),两条 new(env preflight + 防漂移守卫)。KG-29 是 keep(追认)。

---

## §3 · 我现在最不确定的 3 件事（留给 Codex / P2 / P3）

**① KG-29 追认——charset 放宽 `-p[A-Z]` → `-p[A-Z][a-zA-Z]*` 有没有安全隐患?**
我的 first-take:**没有实质隐患**。理由:放宽只在 `-p` 段追加 `[a-zA-Z]*`,不引入 `/ \ . ..` 或控制字符;path-traversal 的四道防线(charset forbidden-chars + basename 校验 + realpath containment + hard-fail)一字未动;实测 `008/../../etc` 仍被四道全拦。但我**不确定**的是:(a) 多字符 `-p` 后缀会不会与 `-v` 段解析产生歧义边界(如 `009-pv0.2` 这种畸形 id 会被哪段吃掉)?(b) charset 变宽后,filename basename 拼接有没有新的边界 case?需要 Codex 独立构造对抗样例复核,不能只信我说"防线没动"。

**② 系统性修法——环境假设到底住哪一层?这是 v6 的核心设计岔口,我给不出唯一答案。**
候选:(a) **生成时推断**（`plan-start` 用 `realpath`/`git config` 动态填,模板不含字面量）;(b) **环境变量**（`$XENODEV_REPO` / `$CODEX_HOME`,一处定义处处引）;(c) **运行时探测**（脚本自己找兄弟目录/glob 版本);(d) **混合**（路径用生成时推断,版本用运行时 glob,env 用 preflight)。我倾向 (d) 混合——因为三类硬编码性质不同(路径是产物字段/版本是调用时值/env 是前置条件),硬套一种机制会别扭。但**哪类用哪个、$XENODEV_REPO 这种环境变量在双机怎么持久化**(KG-env-pointer 那条 backlog 已证 env 指针持久化本身是坑),我不确定,这正是 K 点名要 forge 定的。

**③ 防再漂移机制——加什么守卫、加在哪、成本多大?**
5 条同时存在证明"没有守卫拦硬编码进来"。候选:(a) grep-gate（CI/pre-commit 扫 `/Users/admin` / 写死版本号 → 拒);(b) lint 规则;(c) 只靠文档约定。我倾向 (a) grep-gate 最实(便宜、直接、可测)。但**不确定**:(i) 双机非发行场景下,加 CI 是不是过度工程(K binding④)?还是一个仓根 `check-no-hardcoded-paths.sh` 手动/pre-commit 跑就够?(ii) 守卫该放 IDS 还是 XenoDev 还是两边?(iii) 它自己会不会成为下一个"假设某机器形态"的东西?这条我最没把握,需要 P2 SOTA(12-factor / CI 跨平台)给锚 + Codex 判成本。

---

**P1 自评**:X 全一手读取无 fallback。核心判断——**5 条是一个系统性可移植性缺陷的 5 个切面,修法要系统性(住哪层 + 一次清扫 + 防漂移)非逐处补丁**;KG-27 的正确范式(glob+sort -V)同仓已存在只需推广;KG-29 追认倾向"安全、不推翻"但需 Codex 对抗复核;最大开放问题 = 环境假设住哪层(§3②)+ 防漂移守卫(§3③)。字数约 1400。
