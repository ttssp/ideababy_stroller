# Idea 007/007a-agent-emit · L2R1 · Opus 4.7 Max · Explore (no search)

**Timestamp**: 2026-05-08T07:35:00Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read GPT-5.5's L2R1.
**Origin**: Forked from idea 007 L1 menu Direction 1 "Agent 自录摩擦"。L1 mode = narrow,本 fork 把 friction-tap 的主语从 operator 反转为 Claude session。

---

## 1. The idea, unpacked

**这个 idea 真正的样子是什么**

它不是一个 CLI。它也不是一个 hook。它是一个**约定**:Claude session 在某种约定的"摩擦时刻",自己往一个特定文件追加一行。`friction <msg>` 这个 50 行 Python CLI 仍然存在,但它在新形态下从"主路径"退到"operator-fallback"——operator 看到 agent 漏报、或者觉得 agent 不会识别但自己想留个种子的瞬间,才用一下。日常 95% 的 friction entry 是 agent 自动产生的。

**用户是谁(具体)**

主用户是**正在跑 dogfood 的单个 operator**,他在 Claude Code 终端里调度 agent 跑 task,目标是把 autodev_pipe 的 V4 阶段(2026-05-06 frozen 起 12 周)走完并产出 checkpoint-01/02/03 三份 retrospective 报告。这个人不是软件工程师身份(per CLAUDE.md 的 user 画像),但他是这个工具链的最高频使用者。次用户是 4 周后回看 retrospective 报告的同一个 operator —— **真正读 friction-log 的人是 3-4 天后乃至 4 周后的自己,不是别人**。

**没有这个工具时,他的一天**

operator 跑了 6 小时 dogfood task。其中 2 小时被工具坑了:retrospective skill 跑出 placeholder 而不是真分析、`append_lesson.py` 静默失败、parallel-builder 在某个 task 上无限重试同一个错。每次坑的当下他想"我应该记一笔",然后 (1) 想找 friction-log 文件路径,(2) 算 ISO timestamp 格式,(3) 切到正确 cwd,(4) echo + redirect。4 步加在一起是 90 秒,但更关键是这 90 秒打断了"我正在调试这个具体 task"的心流。结果:他记了第 1 次,跳过第 2/3/4 次,第 5 次怒气太大记了一条 angry 的"!!! 又来了 !!!" 但缺 context。一周后他打开 friction-log 看到 4 条混乱条目,3 条已经想不起来当时具体是什么。

**有这个工具时,他的一天**

operator 跑同样 6 小时 dogfood。这一次,每次某个 hook 或 tool 失败、或某个 skill 输出明显是 placeholder 时,Claude session 自己识别这是 friction signal,通过一个 hook(可能是 PostToolUse 或专门的 friction-emit channel)写一行。operator 看不见这个动作,他依然在解决他眼前的具体 task。一周后他打开 friction-log,看到 27 条带完整 context 的 entry —— "task T013 跑到第 4 步时,parallel-builder 在 worktree X 收到 spec_validator 拒绝但错误信息只有 'failed at line 23',没有指明哪条 constraint 违反,operator 必须手动跑 spec_validator --verbose 才看到 C-OQ-3 缺值"。这段是 agent 写的,不是他写的。他读到时第一反应是"对啊!那次我也卡了",第二反应是"哦,这条以前从来没记下来过"。

**第一次"啊哈"30 秒**

operator 把 hook 装上,跑当天第一个 task。task 跑到一半 spec_validator 失败。他正在排查时,顺手 `cat docs/dogfood/v4-friction-log.md` 看一眼 —— 看到刚才 30 秒前 agent 已经写了一行:`2026-05-15T08:23:11Z [agent-emit] · spec_validator failed during T007 build, exit code 2 stderr "expected 7 elements found 6", task description: ...`。**他没动手,记录已经在那里了**。"啊哈"瞬间不是工具好用,是"哦原来工具该是这样运作的 —— 我根本不该是写记录的人"。

**6 个月后的 mastery**

operator 不再去 cat friction-log 文件。retrospective skill 在 phase 收官时自动从 friction-log 提取主题并产出聚合报告,operator 直接看报告。friction-log 自身退到 audit trail 的位置:存在,但从来不被人手工读。**它的真价值在那个时候是历史 archive,而不是日常工具** —— 历经 12 周后回头看,你能 trace 出哪一类 friction 是哪个 phase 才出现、哪个 phase 真的修掉了、哪个 phase 假装修掉但又复发。

**一百万人用是什么样**

把这个比喻打开:任何一个用 agent 协作的开发团队,都积累一份这种"agent 视角的工具链 friction archive"。这就不再是"一个 operator 的 dogfood 工具"了 —— 它变成 **agent ecosystem 的共享免疫记忆库**。一个新的 skill 上线后,可以被检索"这个 skill 的同类前作发布初期遇过哪些 friction"。这个 vision 可能太宽,先不展开 —— v0.1 不需要它就有意义。

---

## 2. What's genuinely novel

真新的一点是**主语反转本身**:把"用户用工具记录使用工具的体验"反转成"工具自己记录被使用时的体验"。这不是一个新机制(observability 工业化已有几十年),也不是新概念(self-monitoring agent 在 academic 圈讨论很久),但它在**单 operator + LLM agent 协作 dogfood 这个 narrow context 里被工业化**这件事是新的。已有的 LLM observability 工具(Langfuse、Helicone、Phoenix 等)主要服务"我作为产品开发者监控我的 LLM app 服务用户" —— 用户和监控者分离;这个 fork 的场景里**用户、被监控者、读监控数据的人都是同一个人**,而且他读的目的不是诊断,是"4 周后回看 dogfood 信号"。

如果非要找真正"不组合现有"的核心:agent 自己识别"这是不是 friction"这一步是新的 —— 它不只是被动记日志,需要 agent 有 friction 的概念,有"是否值得记"的判断。这是 self-reflective primitive,不只是 observability。

---

## 3. Utility — concrete usage

**场景 1**: operator W2 周三下午,跑 task T012 时 parallel-builder 在 BLOCKED 状态卡 7 分钟。他第一反应是切换到另一个 task,把 T012 暂时搁置。一周后他打开 v4-friction-log.md 看到 agent 已经记了 "T012 BLOCKED · stale lock file in worktree-T012/.git/index.lock · session 7m22s no progress"。他对这条 friction 立刻有了反应:"对,锁文件我没清",此刻他能立刻去修 hook 自动检测过期 lockfile,而不是 4 周后再被一遍同样的坑撞。

**场景 2**: operator 在做 retrospective skill 自身的开发(meta:用 V4 retrospective skill 复盘 V4 retrospective skill)。他跑 L2 phase retrospective,skill 输出明显是 placeholder("phase X 的实际改动如下:[需要补]")。agent 此时识别 "skill 输出 placeholder = friction" 并 emit。一周后看 friction-log,这条触发了 "把 placeholder 检测做成 retrospective skill 自身的内置 verification" 的 V4.1 改进。

**场景 3**: operator 跑 dogfood 第 8 周,接近 D5 12 周硬条件。打开 friction-log 一看 agent 累计记了 90 条,grep `block-dangerous` 发现有 12 条都是"Claude 想跑某个命令被 hook 拦截但拦截信息缺乏 context (operator 不知道为什么被拦)"。operator 立刻看到 gap-1 production credential 隔离的真实威胁不是"凭据泄漏" —— 而是"operator 不知道 hook 到底在防什么"。他朋友问他 "你 dogfood 拿到了什么",他说 "比起 retrospective 报告,真正给我洞察的是 friction-log 自己" —— 不是 agent 写得多好,而是**他 4 周后能看到自己 4 周前看不到的图案**。

---

## 4. Natural extensions

- **friction-log → friction-graph**:phase 结束时聚类,出一份 cluster 报告(哪些工具 / 阶段是 friction 重灾)
- **agent-emit → multi-agent emit**:不只 Claude session,parallel-builder agent / spec-validator / pre-commit hook 都自报
- **friction tier**:agent 给每条 entry 打 tier(blocking / annoying / cosmetic),retrospective 时按 tier 加权
- **跨 dogfood 实例的元 friction-log**:多个 dogfood 周期(V4 / V5 / V6)的 friction-log 聚合,看哪些 friction 一直没修复
- **friction → fix issue 自动化**:一条 friction 触发自动开 issue / 草稿 PR / 给 retrospective skill 加 verification

---

## 5. Natural limits

- **如果 operator 不在 dogfood 模式**(只是日常用 agent 改改东西),agent 自动 emit 没有读者 —— 退化为日志膨胀。**需要明确开关**。
- **agent 的 "是 friction" 判断是 fuzzy 的**:它会漏(以为是正常错误)、会误报(明明是 user 故意制造的失败)。100% recall 不是目标。
- **多 agent 同时 emit 会撞写**:如果 parallel-builder 跑多 worktree,需要锁或 append-only 协议
- **隐私**:agent emit 可能附带 task 内容片段;若 task 涉敏感数据,需要 redact 规则
- **不能替代 operator 主观感受**:agent 看到的是 tool 失败,看不到 "我心里觉得这流程不对" —— 后者需要 operator-fallback CLI 兜底
- **过度 self-monitoring 反而成 noise**:agent 太 chatty 也会让 friction-log 失真

---

## 6. Three honest questions about this idea

1. **Claude Code 的 hook 系统当前能否捕获 "tool 调用失败" 这种 signal,并且允许 hook 写文件?** 如果不能,这个 idea 的载体可能要退到 wrapper script 而不是 hook —— 那就改变了 ergonomic 假设。

2. **"agent 自己判断是不是 friction" 的 prompt 设计有没有先例?** 是否已经有人在 LLM 工程里做"让 agent 给自己的失败打 tier"这件事,他们怎么解决误报和漏报?

3. **operator 自己能不能接受"我不再是记录者"?** 这个 idea 的 social/psychological 假设是 operator 愿意把"我有意识地选择记什么"这个动作让渡给 agent。如果他不愿意,fallback CLI 才是主路径,这条 fork 的 spark 就垮了 —— 这条假设值得用 GPT 那边 R2 search 调研用户访谈类素材。

---

**总字数 ≈ 1280 words**(在 700-1300 上限附近,§1 和 §3 拿了大头)
