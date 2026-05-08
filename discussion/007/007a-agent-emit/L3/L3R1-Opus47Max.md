# Idea 007a-agent-emit · L3R1 · Opus 4.7 Max · Scope (no search)

**Timestamp**: 2026-05-08T09:55:00Z
**Inputs read**: L2 stage doc, L3R0-intake
**Searches used**: NONE in this round
**Visibility**: did NOT read GPT-5.5's L3R1

---

## 0. How I read the intake

operator 在严苛 timeline(1-2 周 ship × 5-10 hr/week × 与 dogfood 并行)下要 ship 一个 v0.1,且明确把 trust calibration 排在 speed-to-ship 之上。这意味着**两条候选必须都把"质量优先"内化进 scope,不能用"先 ship 再加 trust"作借口**。同时 4 条红线全 hard、6 条 condition 中 4 条已锁(IDS first / PostToolUseFailure-only / default private / default single-operator),L3R1 真正的 scope 自由度只剩 OQ-2(friction 判定规则)、OQ-4(log 路径硬编码 vs 可配)、OQ-10(误报处理),以及 condition 1 审阅入口的具体形态(operator 已同意简化为 markdown tag,不做 state machine)。

- **Hard constraints I'm respecting**: C1 1-2 周 / C2 single-operator / C3 free OSS / C4 hook + CLI / C5 4 红线 / C6 4 condition / C7 PostToolUseFailure only / C8 IDS first / C9 minimal scope
- **Unknowns I'll propose options for**: OQ-2(judgment rule)、OQ-4(log path)、OQ-10(false positive 处理)
- **Red lines I'll honor**: 4 条 hard red line + condition 4 default private

operator catch-all 还说"friction-tap 不能拼动太多时间",所以**两条候选都要在 10-20 小时总预算内可信完成**。任何超出这个的候选我必须诚实标"不推荐 in current timeline"。

---

## 1. Candidate A · "Hook-only · Static-Rule · IDS-Local"

### v0.1 in one paragraph

一个 Claude Code `PostToolUseFailure` hook 脚本(~100 行 Python),fire 时按**静态规则**判断这是不是 friction(根据 hook payload 的 tool 名 / exit code / stderr 长度)。是 friction 则按固定格式 append 一行进 IDS 仓库的 `docs/dogfood/v4-friction-log.md`(路径**硬编码**,IDS 仓库必须有此目录)。每条 entry 含 timestamp / tool / exit code / first-200-chars-of-stderr / **uncertainty 自评**(low / medium / high · 基于规则判断置信)。Operator 通过 markdown tag 在 entry 后手工标 `[acked]` / `[disputed]` / `[needs-context]`(无 state machine,operator 直接编辑文件)。一个超薄 `friction <msg>` Python CLI 兜底 operator-fallback。第 14 天 hook 自动跑一次 trust monitoring 输出(过去 14 天 entry 数 / 三种 tag 比例 / hook 是否仍开),写入 `docs/dogfood/v4-trust-w2.md`。

### User persona

**Yashu**(operator 自己):正在做 V4 dogfood 的 single user。背景非软件开发,但是这个工具链最高频用户。每周 5-10 小时,**同时还在跑 ADP V4 dogfood + 其他 forge 事务**。需要 friction-tap 不打扰他的主线工作,只在他真被坑的当下、不需任何动作的情况下,把摩擦点留给 4 周后回看的同一个自己。

### Core user stories

- 作为 operator,我可以**完全不动手**(0 操作)就让 agent 把"刚才 tool 失败"这件事记到 friction-log,所以我不会因为"切上下文太麻烦"漏记真正卡过的事
- 作为 operator,我可以在 friction-log 任何 entry 后手工敲 `[acked]` / `[disputed]` / `[needs-context]`,所以我能保留对 entry 准确性的最终叙事权
- 作为 operator,我可以在 friction-log 任何位置敲 `friction <msg>` 命令补一条 subjective 体感(eg "心里这流程不对劲"),所以 agent 看不到的层面也能进 archive
- 作为 operator,我可以在第 14 天读一份自动产出的 trust monitoring 摘要,所以我知道这个 hook 真的在帮我还是只在制造噪声
- 作为 operator,我可以一行命令(`friction --off`)关掉 hook 或调阈值,所以误报失控时我有快速止血

### Scope IN

- `PostToolUseFailure` hook(~50 行,JSON 解析 + 静态规则 + append)
- 静态规则 = 白名单(eg `Bash` tool 失败、`Edit` tool 失败、自定义 hook block)+ 黑名单(eg operator 主动 `--off` 标记、特定 task description 含 `[debugging-friction-detection]` 关键字)
- friction-log 固定路径 `docs/dogfood/v4-friction-log.md`(脚本启动时若无该目录则创建)
- entry 格式:`<ISO> [agent-emit] [confidence:H|M|L] · <tool> exit <code> · "<stderr-200chars>" · task: <desc>`
- markdown tag:operator 直接在 entry 后追加 `[acked]` / `[disputed]` / `[needs-context]` 一行,grep 即可统计
- `friction <msg>` CLI(~30 行,用于 fallback subjective 体感)
- `friction --off` / `--on` / `--threshold low|medium|high`(~20 行,止血开关)
- 第 14 天自动 trust report:`docs/dogfood/v4-trust-w2.md`(~50 行 cron 或 launchd 触发的简单 grep 统计)

### Scope OUT(explicit non-goals)

- **state machine**(operator 选择 simplified — markdown tag 即可)
- skill placeholder 检测、其他 lifecycle hook(C7 PostToolUseFailure only 锁)
- LLM 自己判断是不是 friction(留给 OQ-2 选项)
- 跨仓 ship(C8 IDS first,ADP 那边 4 周等待期不动)
- entry 的 frontend / 可视化(C5 红线 4 不与 enterprise observability 竞争)
- 团队共享 / 多读者格式(C2 single-operator)
- 自动开 issue / PR / fix(C5 红线 2 不接追责文化)

### Success looks like

- **O1**:第 14 天 friction-log 累计 ≥ 8 条 agent-emit entry(证明 hook 在工作)
- **O2**:第 14 天 trust report 显示 `[acked]` 比例 ≥ 50% 且 `[disputed]` ≤ 20%(operator 没频繁觉得 entry 不准)
- **O3**:第 14 天 hook 仍 enabled(operator 没在第 14 天前关掉)— 这是 GPT R2 search 引的 quantified-self 弃用研究的反向 metric
- **O4**:operator 跟自己说"我能审阅一份 archive,而不是从零回忆"(主观但可记录)

### Honest time estimate

- hook + 静态规则 + append:**3-4 小时**
- markdown tag 约定 + 文档:**1 小时**
- `friction <msg>` CLI:**1-2 小时**
- 开关 + 阈值:**1-2 小时**
- 第 14 天 trust report 脚本:**2-3 小时**
- 测试 + commit + 文档:**3-4 小时**
- **总计 ≈ 11-16 小时**,operator 5-10 hr/week × 1.5 周 = 7.5-15 小时 → **可信落在 1-2 周** ✅
- Confidence: **H**

### UX principles(tradeoff stances)

- **trust > speed**:entry tone 必须含 confidence 自评(L/M/H),不假装权威
- **simplicity > cleverness**:markdown tag 优于 state machine — operator 用记事本就能编辑
- **fast off-switch > sophisticated tuning**:`friction --off` 一行止血,胜过精细阈值参数
- **agent 是 witness 不是 judge**:entry 不写"this is critical","建议你做"等措辞;只写"我观察到 X · 我推测 Y · 置信 L/M/H"

### Biggest risk

最大的风险是**静态规则的误报率超出 operator 容忍**。Bash tool 失败 ≠ 一定是 friction(operator 故意 `set -e` 测试某条命令时,hook 会把它误判为 friction)。如果第 1 周累计 5 条 `[disputed]`,operator 心理上会开始怀疑,第 2 周即使 disputed 比例没继续涨,他可能为防麻烦 `--off` 关掉 hook。**第 14 天 trust report 必须 honest 反映这个数字**,而非粉饰。

---

## 2. Candidate B · "Hook + LLM-Judge · Configurable Path · IDS-Local"

### v0.1 in one paragraph

跟 Candidate A 同样的载体(`PostToolUseFailure` hook + Python CLI fallback),但**判定规则**升级为 **LLM-driven**:hook fire 时启动一个超低成本 LLM 调用(用最小模型 + 短 prompt)让 LLM 给"这是不是 friction"打 confidence 分(0-100),≥60 才 emit entry。同时 **log 路径可配**(`~/.config/friction-tap/config.json` 或环境变量),所以将来 ADP 那边接入零工程量。entry 格式同 A 但 confidence 从规则置信换成 LLM 评分(更精细 0-100)。

### User persona

同 A(operator 自己)。

### Core user stories

(基本同 A,差异在第 1 条)

- 作为 operator,我可以**完全不动手**(0 操作)就让 agent 把"刚才 tool 失败"这件事**经 LLM 智能筛选**后记到 friction-log,所以漏报率比静态规则低
- (其余同 A)

### Scope IN

(同 A,但替换两项)

- 替换"静态规则"为"LLM-judge 调用"(~80 行 — 含 prompt 模板 + LLM API 抽象 + cache 层 + 失败 fallback 到静态规则)
- 替换"硬编码 friction-log 路径"为"可配路径(`~/.config/friction-tap/config.json` + 环境变量 `FRICTION_LOG_PATH`)"(~30 行)

### Scope OUT

(同 A,加一条)
- **不接外部 LLM API**(C5 红线 3 default private + condition 4 单 operator)— 用 Claude Code session 自身的 LLM,不调外部

### Success looks like

(同 A,改 O2)
- **O2 (revised)**:第 14 天 trust report 显示 `[disputed]` ≤ 10%(LLM-judge 应比静态规则更准 — 如果没显著下降,LLM 这层就是浪费工程量)

### Honest time estimate

- hook + LLM judge prompt 设计 + cache + fallback:**6-8 小时**(prompt 调优是不可压缩的工程成本)
- 可配路径 + 环境变量:**1-2 小时**
- 同 A 的 markdown tag / CLI / 开关 / trust report:**8-11 小时**
- 总计 ≈ **15-21 小时**,operator 5-10 hr/week × 1.5 周 = 7.5-15 小时 → **可能超 1 周,逼近 2 周上限** 🟡
- Confidence: **M**(LLM judge prompt 调优有不可预见的迭代成本)
- **不推荐 in current timeline,除非 operator 明确接受 push 到 2.5 周**

### UX principles

(同 A)

### Biggest risk

LLM judge prompt 设计的隐藏成本。Anthropic 自己的 prompt engineering 经验说"看起来 5 行的 prompt 通常实际要 50 行以上 + 多次 iteration"。如果 prompt 第一版 disputed 率 25%,operator 必须迭代;每次迭代要等 24 小时(每天产生足够 entry 才有信号),3 次迭代就是 1 周。在 1-2 周 timeline 下,LLM-judge 增加的工程量可能挤掉 trust monitoring 工作。

---

## 3. (no Candidate C)

operator catch-all 明确说 "scope 必须最 minimal,宁愿加 OQ 也不要加虚假本化的 hard requirement"。在 1-2 周 × 5-10 hr/week 现实预算下,Candidate A 已经是最 honest 的 scope,Candidate B 是"ambitious 但可能延期"的对照,**第三条候选会让 menu 失去信号** —— 我选择诚实给 2 条。

如果一定要列 C,可能的形态是 "**Hook + LLM-Judge + Configurable Path + Cross-Repo Ready (能直接接 ADP)**" — 但那条违反 C8 IDS first(ADP 4 周等待期),且时间预算 ≈ 25-30 小时显著超出 catch-all,**主动放弃**。

---

## 4. Options for ❓ items

### OQ-2 · friction signal 判定规则

- **Option 1 · 静态规则**(Candidate A 的选择):基于 hook payload(tool 名 / exit code / stderr 长度) + operator 维护的小型白/黑名单。**优点**:5 行规则覆盖 80% 真实 friction signal;成本可控(无 LLM 调用)。**缺点**:operator 故意触发的失败会被误报(场景 5);白名单维护需 operator 偶尔手工调
- **Option 2 · LLM-driven**(Candidate B 的选择):每次 hook fire 启动一次小 LLM 调用判断。**优点**:理论 disputed 率更低。**缺点**:prompt 工程不可压缩成本(隐藏 6-8 小时);失败 fallback 仍要走 Option 1,所以 Option 1 是 LLM 路径的子集 — 不能跳过
- **推荐 · Option 1**:与 priority #4 speed-to-ship 一致;LLM 优化是 v0.2 题目

### OQ-4 · log 路径硬编码 vs 可配

- **Option 1 · 硬编码** `docs/dogfood/v4-friction-log.md`(Candidate A):**优点**:1 小时实现 ✅;新建目录是 IDS first 的边际成本可接受。**缺点**:ADP 跨仓 ship 时要重写
- **Option 2 · 可配**(Candidate B):`~/.config/friction-tap/config.json` + 环境变量。**优点**:跨仓零成本接入。**缺点**:多 1-2 小时;但 forge 006 路径 2 4 周后 ADP 接入时是 free 的优势
- **推荐 · Option 1 + 留 v0.2 升级路径**:v0.1 硬编码,v0.2 加可配。如果 4 周后 ADP 接入时再加,工程量是 1-2 小时,**未来增量成本可控**

### OQ-10 · 误报 5 条如何处理

- **Option 1 · 手工删 entry**:operator 自己开文件删行;5 条以下可接受。但 5 条以上 = 心理负担
- **Option 2 · 调阈值**:operator 跑 `friction --threshold high`,后续只有高置信 entry。**v0.1 推荐**(Candidate A 内置)
- **Option 3 · 直接关 hook**:`friction --off`。最严的反应,触发 trust monitoring 的红色信号
- **推荐 · Option 2 first, Option 3 if 持续**:阈值是中间件;关 hook 是最终线。trust report 必须区分这两种"摆脱"

---

## 5. Red lines I'd propose

operator 已经名了 4 条 hard red line(intake Q5),无需 Opus 再提。我支持现有的 4 条,且将 condition 4 default private 解释为内含的第 5 条。

唯一可补充的是:**"v0.1 不接受 entry 数量优化为 metric"** —— 即不要因为想让 trust report O1 看好看而调阈值放水。但这条 operator 在 catch-all 已经表达了类似意思("不要加虚假本化的 hard requirement"),所以也不需我再正式列。

---

## 6. Questions that need real user interviews

L3R1 只有 1 个 user(operator 自己),所以"用户访谈"实际是 30-60 min self-interview。L2 stage doc §7 末尾已经把 GPT R2 §6 的 3 个问题放进。这里我补充 2 个 candidate-specific 的:

1. **如果 v0.1 是 Candidate A(静态规则),你愿意接受第 1 周 disputed 率高达 30% 的可能吗?** 这个数字会决定你在第 1 周能不能 hold 住不去优化(因为优化也是工程成本)
2. **如果第 14 天 trust report 显示 hook disabled,你希望这件事的反应链是什么?**(比如是"自动起 v0.2 plan"?还是"abandon")。这条直接影响 v0.1 是否要内置 escalation 流程

(这两条建议在 L3 advance 前的 30-60 min self-interview 中回答,可以写进 L3R0-intake.md 或新建 L3-self-interview.md)

---

**总字数 ≈ 1480 words**(在 800-1500 上限,Candidate A 拿了大头反映"推荐路径",Candidate B 给对照不刻意求平衡)
