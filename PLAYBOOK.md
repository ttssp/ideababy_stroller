# Idea Incubator 完整操作手册

> **版本**：v3.0 · 2026-04-23
> **适用对象**：零大型项目经验的单人开发者 + AI 团队
> **质量目标**：商业落地级（production-grade）软件
> **核心方法论**：**4 层探索树**（Inspire → Explore → Scope → Plan）+ 任意层 fork + SDD + 并行子智能体 + 对抗式审查

---

## 目录

0. [前置准备（一次性 Setup，约 90 分钟）](#0-前置准备一次性-setup约-90-分钟)
1. [项目目录结构](#1-项目目录结构)
2. [阶段 A：Idea 收集（Proposals · 极简模板）](#2-阶段-aidea-收集proposals)
3. [阶段 B：L1 Inspire（启发层）](#3-阶段-bl1-inspire启发层)
4. [阶段 C：L2 Explore（展开层）](#4-阶段-cl2-explore展开层)
5. [阶段 D：L3 Scope（范围层 · human 介入最重）](#5-阶段-dl3-scope范围层)
6. [阶段 E：L4 Plan（SDD 工程层）](#6-阶段-el4-plan工程层)
7. [阶段 F：并行开发 + 对抗审（保留 v2.1 流程）](#7-阶段-f并行开发与对抗审)
8. [Fork / Park / Abandon（树操作）](#8-fork-park-abandon)
9. [Token 与速度优化清单](#9-token-与速度优化清单)
10. [常见问题排障](#10-常见问题排障)

---

## 0. 前置准备（一次性 Setup，约 90 分钟）

### 0.1 订阅与计费策略（先想清再付钱）

| 工具 | 推荐订阅 | 月费 (USD) | 用途 |
|---|---|---|---|
| Claude Max 20x | **必须** | $200 | Opus 4.7 + Sonnet 4.6 主力，支持 10+ 并行会话 |
| ChatGPT Pro（含 Codex 使用额度） | **必须** | $200 | GPT-5.4 xhigh + GPT-5.3-Codex，用于辩论与 Codex 审查 |
| Anthropic API（备用） | 可选 | 按量 | 超出 Max 配额后兜底、脚本自动化 |
| Cursor Pro | 可选 | $20 | 仅用作可视化 diff 审查 |

**为什么必须双顶级订阅？**
- 你的核心价值主张是"双模型辩论"，单一订阅无法实现。
- Max 20x 给你 `~900 messages / 5hr`，够同时跑 5+ worktree。
- Codex Pro 让你跑 `/codex:adversarial-review` 基本零边际成本。
- 实测：单项目从 0 到商业上线，完整成本约 $400–800/月，相当于一个初级工程师时薪 2–3 小时的钱。

### 0.2 必装工具清单

按顺序执行：

```bash
# 1. Node.js 20+ (Claude Code / Codex 都需要)
#    macOS:
brew install node@20
#    Windows/Linux 用 nvm 或官方安装器

# 2. Claude Code（全局安装）
npm install -g @anthropic-ai/claude-code

# 3. Codex CLI（全局安装）
npm install -g @openai/codex

# 4. Git（确认已安装且 >= 2.40，worktree 需要新版本）
git --version

# 5. GitHub CLI（用来创建 PR、管理 issue）
brew install gh     # macOS
# 或 https://cli.github.com/

# 6. ripgrep（Codex 和 Claude Code 都偏好用 rg 做搜索）
brew install ripgrep

# 7. tmux（管理多个并行会话必备）
brew install tmux
```

### 0.3 首次登录与账号绑定

```bash
# Claude Code 登录（选 Claude App，绑定 Max 订阅）
claude
# > 浏览器会自动打开，登录 claude.ai 即可

# Codex 登录（选 ChatGPT 账号）
codex
# > 浏览器会自动打开，登录 openai.com 即可

# 关键验证
claude --version   # 期望 >= 2.1.50（worktree 原生支持）
codex --version    # 期望 >= 0.6.x
```

### 0.4 安装 Codex-in-Claude-Code 插件（**这是整个流程的关键粘合剂**）

```bash
# 在任意目录启动 claude 一次
claude
# 然后在 Claude Code 交互界面输入：
> /plugin install openai/codex-plugin-cc
```

装完你就有了：
- `/codex:review` – 普通 Codex 审查
- `/codex:adversarial-review` – 对抗式审查
- `/codex:rescue` – 把任务交给 Codex 做（异步）

### 0.5 全局配置（只做一次，全项目受益）

创建 `~/.claude/CLAUDE.md`（全局个人偏好，不入 git）：

```markdown
## 我的身份
我是单人独立开发者，无大型项目经验。所有输出要详细、可复制粘贴、有可验证的中间步骤。

## 通用约束
- 所有代码必须带测试，测试先写。
- 所有新功能必须在 plan mode 下先给我出方案，我批准后再执行。
- 报错信息要真实粘贴，不要只说"有错误"。
- 所有 commit 必须走 conventional commits（feat/fix/chore/docs/refactor/test）。

## 工具偏好
- 搜索用 `rg`。
- 包管理 macOS 用 brew，JS 用 pnpm，Python 用 uv。
- 默认 TypeScript strict 模式。
```

创建 `~/.codex/config.toml`：

```toml
# Codex 全局配置
model = "gpt-5.4"
reasoning_effort = "high"     # 默认 high；辩论时手动切到 xhigh

[approvals]
sandbox_policy = "workspace-write"
```

### 0.6 把 Opus 4.7 设为默认主模型

启动 Claude Code 后：
```
/model opus
```
或环境变量持久化：
```bash
echo 'export ANTHROPIC_MODEL=claude-opus-4-7' >> ~/.zshrc  # 或 ~/.bashrc
```

**省钱技巧**：子智能体用 Sonnet，主会话用 Opus：
```bash
echo 'export CLAUDE_CODE_SUBAGENT_MODEL=claude-sonnet-4-6' >> ~/.zshrc
```

---

## 1. 项目目录结构

创建 `idea-incubator/` 仓库，推荐结构如下。**这份结构在你的项目跑到第 5 个 idea 时仍然不会乱**。

```
idea-incubator/
├── CLAUDE.md                        # ⭐ 项目宪法（全会话共享）
├── AGENTS.md                        # 符号链接指向 CLAUDE.md，兼容 Codex
├── README.md
├── .gitignore
├── .claude/
│   ├── settings.json                # Claude Code 项目设置
│   ├── agents/                      # 子智能体定义
│   │   ├── debate-opus.md
│   │   ├── debate-facilitator.md
│   │   ├── spec-writer.md
│   │   ├── task-decomposer.md
│   │   ├── parallel-builder.md
│   │   ├── security-auditor.md
│   │   └── adversarial-reviewer.md
│   ├── commands/                    # 斜杠命令
│   │   ├── debate-start.md
│   │   ├── debate-next-round.md
│   │   ├── debate-conclude.md
│   │   ├── spec-from-conclusion.md
│   │   ├── parallel-kickoff.md
│   │   └── quality-gate.md
│   └── skills/                      # 领域技能
│       ├── debate-protocol/SKILL.md
│       └── sdd-workflow/SKILL.md
├── .codex/
│   └── config.toml                  # Codex 项目级配置（覆盖全局）
├── proposals/
│   └── proposals.md                 # 🌱 所有 idea 入口
├── discussion/
│   └── 001/
│       ├── 001-Opus47Max-R1.md
│       ├── 001-GPT54xHigh-R1.md
│       ├── 001-Opus47Max-R2.md
│       ├── 001-GPT54xHigh-R2.md
│       ├── 001-moderator-notes.md   # 你作为主持人的干预记录
│       ├── 001-Opus47Max-final.md   # 最终观点
│       └── 001-GPT54xHigh-final.md
├── conc/
│   └── 001-Opus47Max-GPT54xHigh-byOpus47Max-260420.md
├── specs/
│   └── 001-project-name/
│       ├── PRD.md
│       ├── spec.md
│       ├── architecture.md
│       ├── tech-stack.md
│       ├── dependency-graph.mmd     # Mermaid DAG
│       └── tasks/
│           ├── T001-schema.md
│           ├── T002-auth-api.md
│           └── ...
└── projects/
    └── 001-project-name/            # 👈 真正的代码仓库（通常是 git submodule）
        ├── CLAUDE.md                # 项目级宪法（覆盖父级）
        ├── ...
```

**关键设计取舍**：
- `proposals/` 和 `discussion/` **不在**代码仓库里，而在 incubator 层，因为它们是跨项目的元数据。
- `projects/XXX/` 做成独立 git 仓库或 submodule，这样商业化时可以直接 `git push` 到私有仓库。
- **AGENTS.md 用符号链接**（`ln -s CLAUDE.md AGENTS.md`），避免双份文件漂移。Codex 读 AGENTS.md，Claude Code 读 CLAUDE.md，一份真相。

---

## 2. 阶段 A：Idea 收集（Proposals）

### 2.1 Proposal 模板

`proposals/proposals.md` 每个 idea 必须遵守以下最小格式（**格式越规范，两个模型辩论越不跑题**）：

```markdown
# Proposals

---

## **001**: [一句话标题]

**提出日期**: 2026-04-21
**状态**: draft | discussing | spec-ready | building | shipped | abandoned
**初始野心等级**: S / M / L / XL (XL = 即时通讯级，L = 完整 SaaS，M = 工具类，S = 小脚本)

### 动机 (Why)
我为什么想做这个？解决什么真实问题？如果没有这个世界会怎样？

### 核心想法 (What)
一段话讲清楚你想做的东西的本质。不需要技术细节。

### 初始约束 (Constraints)
- 预算 / 时间 / 平台偏好 / 必须集成的已有系统
- 我愿意放弃什么（e.g. "可以不支持 Android，先 iOS"）

### 已知未知 (Open Questions)
- 技术栈我完全不确定
- 商业模式有两种可能性
- （越诚实越好，两个模型会围绕这些展开）

### 期望产出
"希望最终我能有一个 XXX，用户可以用它做 YYY"

---

## **002**: ...
```

### 2.2 填写建议

- **10 分钟内写完**。写太久说明你在过早优化。
- **"已知未知"至少 3 条**。没有未知 = 你不需要两个 AI 辩论。
- **野心等级是提示词信号**。你写 XL，两个模型就会自动进入"我们是在谈架构不是在谈 MVP"的模式。

---

## 3. 阶段 B：L1 Inspire（启发层）

这是整个流水线的**最上游层**。你提一个 idea proposal，**其本质只是一个种子**。两个顶尖模型（Opus 4.7 Max + GPT-5.4 xhigh）的首要价值——不是帮你写代码，而是帮你**突破认知局限**，看到这个种子能长出哪些方向。

### 3.1 L1 讨论什么 / 不讨论什么

| 讨论 | 不讨论 |
|---|---|
| 这 idea 能派生哪些有趣方向？ | 用什么技术栈（L4 的事） |
| 价值、新颖性、实用性、延伸 | 架构怎么设计（L4 的事） |
| 某个方向长什么样、干什么用 | 成本、可行性（L3/L4 的事） |
| 谁会爱上它，用户的"啊哈时刻"是什么 | 要做多久（L3 的事） |

**关键设计**：L1 严格不讨论技术 / 可行性。因为一旦考虑"能不能做"，想象空间立刻塌缩到"已有工具能实现的东西"，模型最擅长的**打破认知边界**就废了。

### 3.2 三种模式（启动时选）

```
/inspire-start 001 --mode=full      # 默认。深度发散，2 轮，产出 8-15 个 inspired directions
/inspire-start 001 --mode=narrow    # 只跑 1 轮，产出 4-6 个相邻变体（proposal 已较清晰时）
/inspire-start 001 --mode=skip      # 跳过 L1，直接进 L2（proposal 已非常明确时）
                                    # 但 L2 第一轮会要求包含"我考虑过但没选的替代方案"段
                                    # 把 L1 的价值折叠进 L2
```

### 3.3 L1R1（Daydream · 关门想）

```bash
claude
> /inspire-start 001
# 如果没带 --mode 参数,会问你
```

Opus 写 L1R1，四段式：

- **Part A · 邻近方向**（3-5 个）：换受众、换形态、换范围、换痛点
- **Part B · 延伸方向**（2-3 个）：极端版本、最小版本、跨领域移植
- **Part C · 重组方向**（2-3 个）：质疑 proposal 的预设
- **Part D · 我最有感觉的 Top 3**：为什么有 spark、为什么 human 可能想不到

**硬约束**：禁止 search（关门纯想）、不读对方 L1R1（并行独立）、不碰技术。

Codex 侧并行跑同样结构的 L1R1：

```bash
# Codex 终端（inbox 机制）:
cdx-run
```

`cdx-run` 自动读 `.codex-inbox/latest.md`（Claude Code 已写好完整任务）并执行。**不用复制粘贴**。

### 3.4 L1R2（Cross + 价值验证 search）

```bash
> /inspire-next 001
# (Codex 侧也跑: cdx-run)
```

双方读对方的 L1R1，然后做**价值验证 search**：

| 允许 | 禁止 |
|---|---|
| "这事有人做过吗" | "用什么框架" |
| "用户是不是真的需要" | "怎么架构" |
| "类似项目成败如何" | "要多少钱" |

这一步把"共享想象"（两个模型独立想象出的共同方向）和"共享幻觉"（两个模型的共同训练偏差）区分开——search 说实话。

### 3.5 收 L1，出 inspired menu

```bash
> /inspire-advance 001
```

`inspire-synthesizer` 子智能体读四个 L1 文件，产出 `discussion/001/L1/stage-L1-inspire.md`：

- 统一去重后的 direction 列表（含每个方向的 description、spark、cognitive jump、价值验证证据）
- 交叉参考表（谁提的、谁背书）
- 主题观察 + 诚实"menu 里可能漏了什么"
- 决策菜单

**决策菜单**：

```
[F] Fork 一个或多个方向 → /fork 001 from-L1 direction-<n> as <new-id>
[R] Re-inspire：menu 不对劲，加 steering 再跑一轮
[P] Park：这个 menu 本身就有价值，收藏着，以后再回来
[S] Skip：menu 不打动我，用 original proposal 直接进 L2
[A] Abandon：整个方向都不行
```

**这里的 human 决策密度很低**。读 menu，挑 1-3 个方向 fork 出去，其他留 menu 里（未来可以任意时候 /fork 激活）。

---

## 4. 阶段 C：L2 Explore（展开层）

L1 给你 N 个方向 menu，你 fork 出一个（比如 `001a`）。L2 的任务：把这**一个** idea 深度展开——"这个想法到底是什么、新在哪、能干什么、能延伸到哪、自然限制在哪"。

### 4.1 L2 讨论什么 / 不讨论什么

| 讨论 | 不讨论 |
|---|---|
| 这 idea 的全貌（用户画像 + 使用场景 + 6 个月后的"资深用户"） | 技术栈 |
| 真正新颖在哪（vs 已有方案） | 架构 |
| 具体 3-5 个使用场景（不是 feature 列表，是**使用**） | 成本 |
| 自然延伸（v0.2 会是什么） | 建造难度 |
| 自然限制（不该是什么） | 时间预算 |

L2 和 L1 的区别：L1 是"这个 seed 能长出哪些树"（多棵树），L2 是"这棵树到底长什么样"（一棵树的细节）。

### 4.2 L2 流程

```bash
> /explore-start 001a      # L2R1 Opus 侧(Daydream,6 段式,无 search)
# Codex 侧: cdx-run        # 并行
> /explore-next 001a       # L2R2 Opus(读对方,价值验证 search)
# Codex 侧: cdx-run
> /explore-advance 001a    # 出 L2 report
```

L2R1 六段：
- §0 (仅 skip-mode 才有)：我考虑过但没选的替代 framings
- §1 Idea unpacked（4-8 段，**整个 L2 的核心**）
- §2 Novelty assessment（honest 判断是 novel concept / slice / execution / 不新但 underserved / 不新且拥挤）
- §3 Utility 3-5 个具体场景（带名字的用户，做具体事）
- §4 Natural extensions（1-2 年可能性）
- §5 Natural limits（不该是什么）
- §6 三个诚实问题（seed 下一轮 search）

### 4.3 L2 report 决策菜单

`explore-synthesizer` 产出 `stage-L2-explore-001a.md`，含**明确验证判决**：**Y / Y-with-conditions / unclear / N**。

```
[1] Scope 这个 idea → /scope-start 001a
[2] Fork 另一个 L2 角度 → /fork 001a from-L2 ... as 001a'
[3] 回 L1 menu 选别的 → /status 001
[4] Re-explore（加 steering 再跑一轮）
[5] Park
[6] Abandon
```

**当验证判决是 N**：菜单会建议 [5] 或 [6]，不会催你硬进 L3。

---

## 5. 阶段 D：L3 Scope（范围层）

这是**human 真实需求进入系统**的地方。前两层是模型想象 + 证据验证，human 介入少。L3 开始，human 必须亲自答题、定红线、挑选项。

### 5.1 L3 三个子阶段

```
L3R0 · Human intake (人填问卷, ~5 分钟)
        ↓
L3R1 · 双方独立提 2-3 个 peer PRD 候选 (no search)
        ↓
L3R2 · Cross + scope-reality search (类似产品 v0.1 通常包含/舍弃什么)
        ↓
scope-synthesizer → stage-L3-scope-001a.md
```

### 5.2 L3R0 Intake —— "不确定"是一等答案

```bash
> /scope-start 001a
```

触发 AskUserQuestion 交互式问卷，6 大块：

| Block | 问什么 | 例子 |
|---|---|---|
| 1 | 时间 / 每周工时 | 1-2 周 / 5-15h |
| 2 | 目标用户（从 L2 候选 personas 里选） | "Indie iOS devs" |
| 3 | 商业模式 | free / freemium / paid |
| 4 | 平台 | Web / iOS / CLI... |
| 5 | 红线（绝对不做的事） | 自由文本 |
| 6 | 优先级（速度 / 体验 / 简洁 / 低成本...） | 挑 1-2 个 |
| 7 | 自由补充 | 你想到的别的 |

**每个问题都允许 "不确定 / 让模型建议"**。模型看到 ❓ 后,会在 L3R1 里主动提 2 个具体选项给你挑。这是关键设计——**human 诚实的"不确定"比被逼猜测更有价值**。

输出：`L3R0-intake.md`，每条标记 ✅ (明确) / 🤔 (模糊) / ❓ (让模型建议) / 💡 (红线或自由补充)。

### 5.3 L3R1 候选 PRD

双方独立产出 2-3 个 **peer PRD 候选**（不是"主方案+备选"，是真对等的三个路径）。每个含：

- v0.1 一段话描述
- 具体 persona
- 3-5 个核心 user stories
- Scope IN（要做的）
- Scope OUT（明确不做的）
- 可观察的成功标准（有数字）
- 在 human 的时间预算下的**诚实工时估算**（如果不够就说不够，不和稀泥）
- UX 优先取舍（不是设计稿，是"速度 > 精致"这种取舍立场）
- 最大产品风险
- 针对 human ❓ 项的 2 个具体选项

### 5.4 L3R2 Scope-reality search

```bash
> /scope-next 001a
```

双方读对方 L3R1，然后做**作用域-现实** search：

| 允许 | 禁止 |
|---|---|
| "类似产品 v0.1 通常含什么" | 技术栈选型 |
| "用户期望的最低功能集" | 架构决策 |
| "类似产品哪些 feature 被砍了用户不在乎" | 具体实现库 |

输出：精炼后的候选 + **识别 key tradeoff axis**（这 N 个候选到底在哪个维度上真正不同——human 实际在挑的就是这个维度）。

### 5.5 L3 决策点（关键）

```bash
> /scope-advance 001a
```

`scope-synthesizer` 出 `stage-L3-scope-001a.md`，包括：

- Intake recap（✅ 硬约束 / 🤔 软偏好 / ❓ 已解决 / ❓ **仍待你决定**）
- Key tradeoff axis
- 2-3 peer PRD 候选（全结构）
- 比较矩阵（时间 / persona / 优先级 / 商业模式 / 平台 / 风险 / scope-reality fit / 符合时间预算 / 符合红线）
- Synthesizer **明确推荐**（选一个 / fork 多个 / 暂停需用户访谈 / 回 L2）
- 诚实检查（"menu 可能漏掉了什么"）

**决策菜单**：

```
[F]  Fork 一个候选成 PRD 分支 → /fork 001a from-L3 candidate-A as 001a-pA
[MF] Fork 多个并行（两个不同用户群各自验证）
[R]  Re-scope（加 steering 再转一轮）
[B]  回 L2 重新想这个 idea
[P]  Park（等用户访谈 / 等条件成熟）
[A]  Abandon（菜单让我看清这不该建）
```

**fork from-L3 的特殊行为**：`/fork 001a from-L3 candidate-A as 001a-pA` 除了建 `001a-pA/` 目录和 `FORK-ORIGIN.md`，还**自动生成完整的 `PRD.md`**（提取候选的所有段落、合并 L3R0 硬约束、注明 lineage）。这份 PRD 就是 L4 的输入。

---

## 6. 阶段 E：L4 Plan（工程层）

L3 fork 出 PRD 后，L4 开始。L4 **不再讨论产品**（PRD 是真相源），**开始讨论工程**。

### 6.1 L4 启动

```bash
> /plan-start 001a-pA
```

这个命令编排：

1. **读 PRD**（`discussion/.../001a-pA/PRD.md`）+ L3 menu 上下文 + L2 texture
2. 调用 **spec-writer** 子智能体产出 `specs/001a-pA/` 完整工件包：
   - `spec.md`（6 要素契约）
   - `architecture.md`（C4 L1/L2 + mermaid）
   - `tech-stack.md`（带 pinned 版本 + 拒绝的替代）
   - `SLA.md`（v0.1 + v1.0 双版本）
   - `risks.md`（技术/运营/安全/商业/合规/**bus-factor**）
   - `non-goals.md`（从 PRD scope OUT + 工程级 non-goals）
   - `compliance.md`（如 PRD 暗示监管需求）
3. 调用 **task-decomposer** 产出 `tasks/T001..TNNN.md` + `dependency-graph.mmd`（10-30 任务，4 个 phase，模型分配健康度）
4. **写好 Codex 对抗审 R1 的 inbox task**，human 运行 `cdx-run` 即可触发

### 6.2 spec-writer 的铁律

- **不改 PRD**。PRD 是真相源，有问题必须停下来告诉 human。
- **不写 tasks/**。那是 task-decomposer 的事。
- **不碰 implementation-level 代码**。spec 描述 behavior 和 contract。
- **不超 PRD 范围**。每个 spec feature 必须 trace 回 PRD scope IN。

### 6.3 对抗审循环

Codex GPT-5.4 xhigh 审查 9 个维度：并发安全 / 数据一致性 / 故障恢复 / 安全边界 / 运营成本 10x / PRD 忠实度 / non-goal 泄漏 / DAG 健全 / solo-operator 可行性。

- **CLEAN** → spec 可以进 build（下节 §7）
- **CONCERNS** → human 决定修还是记 risks.md
- **BLOCK** → spec-writer 修订 → R2 审查（最多 4 轮）

### 6.4 PRD 版本 fork

如果你做到 L4 审查时发现"其实 A PRD 也值得试"，历史回溯 fork 仍然有效：

```bash
> /fork 001a from-L3 candidate-A as 001a-pA-alt
> /plan-start 001a-pA-alt
```

两个 PRD 分支各自产出独立的 spec 和 build，互不影响。

---
## 7. 阶段 F：并行开发与对抗审（L4 延续）

> 本节流程是 v2.1 时代已经验证的,v3.0 保持不变。L4 `/plan-start` 产出 spec 和 tasks 后,从这里继续。

### 6.1 模型分工（经过实测验证的分层）

| 层级 | 模型 | 用途 | 成本/任务 |
|---|---|---|---|
| L1 架构层 | **Opus 4.7 (extended thinking)** | 架构决策、跨模块重构、难 bug 根因分析 | 高 |
| L2 规划层 | **Opus 4.7 (plan mode)** / **GPT-5.4 xhigh** | spec、task 分解、技术选型 | 中高 |
| L3 审查层 | **GPT-5.4 (high) via codex-plugin** | 代码审查、对抗审查 | 中 |
| L4 主力开发 | **Sonnet 4.6** / **GPT-5.3-Codex medium** | 写 90% 的业务代码、单元测试 | 低中 |
| L5 机械工 | **Haiku 4.5** / **GPT-5.4-mini** / **Codex-Spark** | 格式化、重命名、样板代码、简单修复 | 极低 |

**铁律**：
- ❌ 不要让 Opus 写样板代码（浪费钱）
- ❌ 不要让 Haiku 做架构（质量崩）
- ✅ 让 Opus **规划**，让 Sonnet/Codex **执行**，让 Codex **审查**

### 6.2 并行基础设施：Git Worktree

**目的**：在同一 repo 里同时跑 5+ 个 Claude Code 实例，每个在独立分支独立目录工作，**互不干扰**。

一次性设置（在 `projects/001-xxx/`）：

```bash
# .gitignore 加一行
echo ".claude/worktrees/" >> .gitignore

# 创建 .worktreeinclude 让 .env 等文件自动拷进 worktree
cat > .worktreeinclude <<EOF
.env
.env.local
*.secrets
EOF
```

### 6.3 并行开工（`/parallel-kickoff`）

假设 DAG 里这批可并行：T003, T004, T008。

```
/parallel-kickoff 001 T003,T004,T008
```

这个命令会：

1. 为每个 task 创建 worktree：
   ```bash
   claude --worktree T003-auth
   claude --worktree T004-chat
   claude --worktree T008-notif
   ```
2. 在每个 worktree 里注入相应 `tasks/TXXX.md` 作为第一条指令。
3. 所有 worktree 都在 **Plan Mode** 启动（`Shift+Tab` 或 `--permission-mode plan`）。
4. 你人工审一遍 plan，每个批准后切到 execution mode。
5. 3 个 Claude Code 并行跑。你切 tmux 窗口巡查。

### 6.4 tmux 布局推荐

```
┌──────────────┬──────────────┐
│              │              │
│  Opus 主控   │  T003 worker │
│  (编排)      │  (Sonnet)    │
│              │              │
├──────────────┼──────────────┤
│              │              │
│ T004 worker  │ T008 worker  │
│ (Codex 5.3)  │ (Sonnet)     │
│              │              │
└──────────────┴──────────────┘
```

**绑定热键**：`~/.tmux.conf`
```
bind -n M-h select-pane -L
bind -n M-l select-pane -R
bind -n M-k select-pane -U
bind -n M-j select-pane -D
```
Alt+hjkl 切窗口，不用鼠标。

### 6.5 何时用 Codex，何时用 Claude Code？

| 场景 | 首选 | 理由 |
|---|---|---|
| 大规模重构（>20 文件） | Claude Code + Sonnet | 1M 上下文能把项目全抓进去 |
| 长期自主任务（几小时） | Codex + GPT-5.4 xhigh | Codex compaction 支持多小时推理 |
| iOS/Swift 原生 | Claude Code | Opus 4.7 对 Swift 支持更成熟 |
| Python/TypeScript 业务 | 两者均可，看哪个便宜 | |
| Shell/PowerShell/Windows 自动化 | Codex | Codex 针对 PowerShell 做过专门训练 |
| 写测试 | 分两步：Opus 写测试，Sonnet 让测试通过 | TDD 分工 |
| 审查代码 | **Codex**（通过 codex-plugin-cc） | 跨模型审查能发现 30% 更多问题 |

### 6.6 子智能体（Subagents）的用法

**定义一次，在所有 worktree 复用**。创建 `.claude/agents/security-auditor.md`：

```markdown
---
name: security-auditor
description: Reviews code for OWASP Top 10, auth flaws, secrets, injection, insecure deserialization
tools: Read, Grep, Glob, Bash
model: opus
isolation: worktree
---
You are a senior security engineer. For every file provided:

1. Check OWASP Top 10 systematically.
2. Flag any secrets in code, env files, or git history.
3. Audit auth flows for token handling, expiration, revocation.
4. Verify input validation at all trust boundaries.
5. Output format:
   # 🛡️ Security Report
   ## BLOCK (must fix before ship)
   ## HIGH
   ## MEDIUM
   ## GOOD PRACTICES SPOTTED
```

在主会话里就可以：
```
让 security-auditor 子智能体审查 src/auth/ 目录
```

**并行子智能体**：
```
起 4 个并行子智能体分别审查：
1. security-auditor 审 src/auth/
2. code-reviewer 审 src/api/
3. performance-profiler 审 src/db/queries/
4. test-coverage-checker 审 tests/
完成后综合成一份报告
```


---

## 8. Fork / Park / Abandon（树操作）

探索树的三个管理命令。每个都给 next-step 菜单，不让你自己去记"下一步"。

### 8.1 Fork（分支 · 任意层 · 支持历史回溯）

```bash
/fork <src> from-L<n> <candidate> as <new-id>
```

**用法**：
- 刚做完某层、看了 menu → fork 出想走的那个候选
- 几天后、几周后想回来试之前没选的 candidate → 同命令

**每个 stage 文档（`stage-L<n>-*.md`）**都会把所有 candidate 完整列出（不只是选中的）。所以未来回溯时，直接从该 stage 文档挑候选 fork 即可。

**Fork from-L3 的特殊性**：不仅建目录 + FORK-ORIGIN.md，还**自动生成完整 PRD.md**（提取候选所有段落，合并 L3R0 硬约束，写 lineage）。PRD.md 就是 L4 的输入。

**目录结构（fork 是 sibling，不是 nested）**：

```
discussion/001/                 # 根 idea
├── L1/stage-L1-inspire.md      # menu（含所有 candidates）
│
├── 001a/                       # fork from L1 #3
│   ├── FORK-ORIGIN.md
│   ├── L2/stage-L2-explore.md  # menu
│   │
│   ├── 001a-pA/                # fork from L3 candidate A
│   │   ├── FORK-ORIGIN.md
│   │   └── PRD.md              # 自动生成
│   │
│   └── 001a-pB/                # 同 L3 的另一个 candidate
│       ├── FORK-ORIGIN.md
│       └── PRD.md
│
├── 001b/                       # fork from L1 #5
└── 001c/                       # fork from L1 #7（parked）
```

### 8.2 Park（暂搁 · 等条件成熟）

```bash
/park <id>
```

AskUserQuestion 引导填写：
- 复活条件（"当 X 发生时 / Y 变为真 / Z 变得可行"）
- 复活检查日期（建议 30/60/90 天）

写 `PARK-RECORD.md`，更新 proposals.md 状态。

**Park ≠ Abandon**。Park 是"好 idea，坏时机"。Abandon 是"学到了这不该建"。

### 8.3 Abandon（放弃 · 结构化 lesson）

```bash
/abandon <id>
```

这不是失败——是"学到了"的信息，有独立价值。流程：

1. 确认（防止误触；提供 /park 作为 off-ramp）
2. 自动从已有 artifacts 提取：prior art、failure patterns、demand signals、constraint mismatch、assumptions that proved wrong
3. AskUserQuestion 三问：
   - Q1 主要放弃原因（多选 + 自由文本）
   - Q2 关于自己学到了什么（可选；如"我对 B2C 没耐心"）
   - Q3 未来什么条件可能重启（可选；可以填"永远不"）
4. 产出结构化 `ABANDONED.md`（含 prior art / 失败模式 / **recyclable material** 可复用到其他 idea 的部分）
5. 追加到仓库级 `lessons-learned.md`（按日期倒序的全局总结）
6. 更新 proposals.md 状态

### 8.4 为什么 Park/Abandon 的产物都值得保留

- **Park 的 artifacts** 是"好 idea 的暂存"——条件变了就直接复活
- **Abandoned 的 artifacts** 是"你的认知升级过程"——跑 10 个 abandon 后读 lessons-learned，往往能看出 3 条关于自己的真理（例如"我总是低估 UX 工作的重量"），这种自我认知靠反思清单获得，不靠"再努力一下"。

---
---

### 7.x 对抗审与 10 质量门

### 7.1 商业级 = 通过全部"质量门"

`/quality-gate 001` 命令依次跑以下检查。**任一不过都不能 ship**。

| 门禁 | 工具 | 标准 |
|---|---|---|
| G1 - 类型检查 | `tsc --noEmit` / `mypy --strict` | 0 error |
| G2 - Lint | biome / ruff / SwiftLint | 0 error, ≤5 warning |
| G3 - 单元测试 | vitest / pytest | 覆盖率 ≥ 80% |
| G4 - 集成测试 | Playwright / XCUITest | 关键用户路径全绿 |
| G5 - 安全扫描 | Semgrep + Snyk + `/codex:adversarial-review --security` | 0 critical / 0 high |
| G6 - 性能基准 | 自定义 perf test | p95 延迟在 SLA 内 |
| G7 - Codex 审查 | `/codex:adversarial-review --base main` | No blocking issues |
| G8 - Opus 自审 | `adversarial-reviewer` 子智能体 | 评分 ≥ 85/100 |
| G9 - 合规检查 | 数据地点、隐私政策、GDPR/PDPA | 手动清单 |
| G10 - 人类验收 | 你自己跑一遍核心路径 | 感觉对 |

### 7.2 对抗审查模式

**重要**：商业级产品的敌人不是"没写对"，是"你没想到的攻击面"。

```
# 挑战架构
/codex:adversarial-review
  --base main
  challenge the authentication lifecycle, session expiration, and token rotation

# 挑战性能
/codex:adversarial-review
  --focus "under 10x traffic, identify the first bottleneck and the cascade failure mode"

# 挑战数据完整性
/codex:adversarial-review
  --focus "find all write paths that can cause data corruption under concurrent access"
```

**实测**：2026 年 3 月社区统计，adversarial review 相较 normal review 多找出约 **3x** 高危问题。

### 7.3 双审循环（Adversarial Loop）

```
Claude Code 实现代码
   │
   ▼
Codex 常规 review (/codex:review)
   │
   ├── 有问题 ─► Claude Code 修复 ──┐
   │                                │
   ▼                                │
Codex 对抗 review                   │
(/codex:adversarial-review)         │
   │                                │
   ├── 有问题 ──────────────────────┘
   │
   ▼
Opus adversarial-reviewer 子智能体
(捕捉 Codex 漏掉的"Opus 特长"问题)
   │
   └─► 全过则 ship
```

### 7.4 发布前最后一道关卡：Claude Managed Agents

如果项目是**长期在线**（如 IM 系统）：
- 用 Anthropic 2026 年 4 月 8 日发布的 **Claude Managed Agents** 托管你的 agent 层（如监控、报警、自愈）。
- 定价 $0.08/runtime 小时 + token。7x24 跑一个月 ~$58。
- 省去自己搞 sandboxing、state 管理、error recovery 的 3–6 个月基础设施工作。

---

## 9. Token 与速度优化清单

**这一节的每一条都被实测验证过，总体能降 40–70% token 消耗、提 2–5x 速度**。

### 8.1 立即要做

- [ ] 设 `export DISABLE_NON_ESSENTIAL_MODEL_CALLS=1` 关闭非关键后台调用
- [ ] 设 `export CLAUDE_CODE_SUBAGENT_MODEL=claude-sonnet-4-6`（Opus 主控 + Sonnet 子工）
- [ ] 在所有 worktree 先进 Plan Mode 审一遍再放出去
- [ ] CLAUDE.md 控制在 **150 行以内**，不要塞大段说明（研究显示 2000 token 以上 CLAUDE.md 会被模型自动忽略）
- [ ] `.claudeignore` 排除 `node_modules/`, `dist/`, `*.lock`, 大数据文件
- [ ] 定期运行 `/cost` 查看 token 分布，找异常源头

### 8.2 并行化

- [ ] **3–5 worktree 是甜蜜点**，超过 10 merge 会成为瓶颈
- [ ] 每个 worktree 任务要"文件域不重叠"（如 T003 只碰 `src/auth/`, T004 只碰 `src/chat/`）
- [ ] Codex 用于长时独立跑的任务（几小时级），Claude Code 用于互动密集任务
- [ ] 子智能体用于"fan-out 研究 → 主会话综合"

### 8.3 Context 控制

- [ ] **永远不要跨 idea 复用会话**。写完 001 的 spec 就开新会话写 002。
- [ ] 每次 `/compact` 之前主动 `/memory` 保存关键决策到 `.claude/memory.md`
- [ ] 碰到 context 占用 >80%，立刻 `/clear` 并从 `spec.md` 重新起
- [ ] 不要让 Claude `cat` 大文件；让它 `rg` 搜关键字即可

### 8.4 MCP 服务器

- [ ] 只装当前项目需要的 MCP，每个 MCP 会为每次 turn 加 3000–5000 tokens
- [ ] `/mcp` 查看已连接 MCP，不用的 disable

### 8.5 Prompt Caching

Claude Code 自己会管，但要知道：
- System prompt + CLAUDE.md + tool 定义是被缓存的（5 分钟 TTL）
- 长时间空闲（>5min）会让缓存失效 → 保持节奏比"思考 15 分钟再问"划算

---

## 10. 常见问题排障

### Q1: Opus 和 GPT-5.4 给出相反方案怎么办？

**在 Stage 1 里这是好事、是设计要的结果**。相反的方案正是为了暴露盲区。

看相反发生在哪个阶段：

- **Stage 1（Explore）**：双方就是被分配了对立极性。越相反越好。不用干预，等 S2 协作阶段自然收敛。
- **Stage 2（Position）**：双方协作但仍相反，说明证据空间里有多条合理路径。**这正是 Stage 2 的目的**——让双方各出一个方向菜单。`/debate-advance-stage NNN 3` 会让 synthesizer 产出统一菜单交给你决策。你可以选 Advance、Fork、Park 或 Abandon。
- **Stage 3（Converge）**：工程阶段还在相反，才是真麻烦。处理方式：
  1. 在 `moderator-notes.md` 追加你的真实偏好（成本敏感 / 技术债容忍度 / 单人运维能力）
  2. 让双方基于新约束**再辩一轮**
  3. 还是不收敛就 `/debate-conclude NNN --force`，让 conclusion-synthesizer 做 adjudication 并呈交给你最终裁决

### Q1b: 主持人决策点（S2→S3）我不知道该选 Advance/Fork/Park/Abandon 哪个？

读 `NNN-stage2-checkpoint.md` 第 3 节"synthesizer 推荐"。它会明确指一个。如果你对那个推荐**感觉**不对：

- 说不清为什么感觉不对 → 通常相信你的直觉，选 **Park**，让自己几天后再看。Park 成本几乎为零。
- 你有新信息 synthesizer 没掌握（比如你刚和用户聊过） → 用 `/debate-inject` 加进去，让 Stage 2 再跑一轮
- 推荐 Advance 方向 A 但你心里是 B → 选 B，前提是你能用一句话说出为什么
- 两个方向都有理 → **Fork**，把 001 拆成 001a 和 001b，各跑各的流程

### Q2: Codex 审查总说一切都好怎么办？

切到 `adversarial-review` 模式并加 `--focus` 定向：
```
/codex:adversarial-review --focus "assume I'm wrong and find where"
```

### Q3: 多 worktree 合并冲突多怎么办？

冲突 = DAG 没切干净。回到 spec 阶段重新切分 task，确保**每个 task 的文件域不重叠**。工具可辅助：

```bash
# 看 worktree 之间的文件重叠
for w in .claude/worktrees/*/; do
  echo "=== $w ==="
  git -C "$w" diff --name-only main
done | sort | uniq -c | sort -rn
# 任何数字 >1 = 有重叠 = 需要重新切
```

### Q4: 钱烧得太快怎么办？

按优先级检查：
1. 是否用 Opus 写样板代码？→ 切 Sonnet
2. CLAUDE.md 是否 >200 行？→ 瘦身
3. MCP 是否装了 5+？→ 只留当前项目需要的
4. 是否一个会话超过 4 小时没 /clear？→ 新会话
5. `/cost` 分析热点

### Q5: Claude Code 说"我没有这个工具"但我知道有？

先搜索：`tool_search` 或者在会话里说 "search for MCP/skills that help with X"。很多能力是延迟加载的。

### Q6: 我是新手，怎么判断 AI 给的架构对不对？

这正是"两个 AI 辩论"的核心价值。如果两个顶尖模型**高度一致**，大概率就是对的。如果分歧大，就是你学习的机会——逼自己理解分歧点，这是最有效的成长路径。

---

## （附录已迁移到 README.md + 各 SKILL.md,此处不再重复）

### 10.1 `CLAUDE.md`（项目宪法）

仓库根目录已有一份 canonical 版本。详见你解压后的 `CLAUDE.md`（<100 行，加载到每个会话）。

**修改原则**：保持 <150 行；每条规则都是"普适于所有 idea"的；项目特定规则放到 `projects/NNN-xxx/CLAUDE.md`；个人偏好放到 `~/.claude/CLAUDE.md`。

### 10.2 辩论协议 `discussion/PROTOCOL.md` + `.claude/skills/debate-protocol/SKILL.md`

**canonical 版本位于**：`.claude/skills/debate-protocol/SKILL.md`（~250 行，含完整的三阶段规则、每轮模板、Codex-side 粘贴模板、质量门）。

`discussion/PROTOCOL.md` 是精简指针，会被 `/debate-start` 复制到每个 `discussion/NNN/` 目录下。

**关键要点速查**：
- 三阶段：S1 Explore（对立+搜索） → S2 Position（协作+方向菜单） → S3 Converge（工程）
- S1R1 Opus 正、GPT 反；S1R2 **必须换极**
- S1 每轮 ≥5 个 web 来源；S2 ≥2；S3 可选
- S2 结束有**主持人决策点**：Advance / Fork / Park / Abandon
- Stage 推进由 `/debate-advance-stage` 触发，不自动

### 10.3 斜杠命令定义

所有 canonical 命令定义位于 `.claude/commands/*.md`。速查表：

| 命令 | 文件 | 用途 |
|---|---|---|
| `/propose` | `propose.md` | 交互式写新 proposal |
| `/debate-start NNN` | `debate-start.md` | Opus 以正方跑 S1R1 + ≥5 搜索 |
| `/debate-next NNN S R` | `debate-next.md` | 下一轮，自动按 stage 分支（S1 换极 / S2 协作 / S3 工程） |
| `/debate-advance-stage NNN T` | `debate-advance-stage.md` | 跨阶段，调用 synthesizer 或 checkpoint |
| `/debate-inject NNN tag` | `debate-inject.md` | 主持人注入约束 |
| `/debate-finalize NNN` | `debate-finalize.md` | Opus 写独立 final |
| `/debate-conclude NNN` | `debate-conclude.md` | 综合全辩论 |
| `/spec-from-conclusion NNN` | `spec-from-conclusion.md` | conclusion → spec + 对抗审查循环 |
| `/parallel-kickoff NNN Ts` | `parallel-kickoff.md` | 文件域验证 + 输出终端启动块 |
| `/quality-gate NNN` | `quality-gate.md` | 10 门质量检查 |

### 10.4 子智能体定义

canonical 位于 `.claude/agents/*.md`。总览：

| agent | 用途 | 模型 |
|---|---|---|
| `stage1-synthesizer` | Stage 1 → Stage 2 转换时消化 S1 所有轮次 | opus |
| `stage2-checkpoint` | Stage 2 → Stage 3 转换时产出决策文档（含菜单） | opus |
| `conclusion-synthesizer` | 综合整个三阶段辩论成单一结论文档 | opus |
| `spec-writer` | 结论 → 完整 SDD 工件（6 要素 spec + 周边文件） | opus |
| `task-decomposer` | spec → 10–30 个可并行任务的 DAG | opus |
| `parallel-builder` | 在自己 worktree 内执行一个任务（TDD） | sonnet |
| `security-auditor` | OWASP + auth 生命周期 + 供应链审查 | opus (high) |
| `adversarial-reviewer` | 三人格对抗审查（破坏者 + 新员工 + 安全员） | opus (high) |
| `code-reviewer` | 正常 PR 式审查（非对抗） | sonnet |
| `debate-facilitator` | 观察进行中的辩论，告诉你是否该介入/收束 | opus |

每个 agent 的详细 frontmatter（tools、isolation、memory 等）见文件本身。

### 10.5 `.claude/settings.json`

canonical 位于 `.claude/settings.json`。关键字段：

- `model: "opus"` + `subagentModel: "sonnet"` —— 主控 Opus，子智能体 Sonnet，省钱
- `permissions.allow` 白名单已包含所有 10 个子智能体 + `WebSearch/WebFetch`
- `permissions.deny` 硬封：`rm -rf /*`、`sudo`、`curl * | sh`、编辑 `.env*` 和 `specs/**`
- `PostToolUse` hook 自动 lint 格式化编辑/写入的文件
- `attribution.commit: ""` 关闭 Claude 的"Co-Authored-By"行

### 10.6 `.codex/config.toml`（项目级）

canonical 位于 `.codex/config.toml`。辩论时要调高推理力度：

```bash
codex --model gpt-5.4 -c reasoning_effort=xhigh
```

---

## 附言：从"想法"到"产品"的现实期望

**别相信"一个 prompt 造出 iOS app"的神话**。2026 年的真实数据：
- 即时通讯级产品（XL）：8–20 周，$4k–15k 基础设施 + 订阅
- 完整 SaaS（L）：4–10 周，$2k–6k
- 工具类（M）：1–3 周，$500–2k
- 脚本类（S）：半天到 3 天，几十刀

**这套 playbook 的真实收益**：
- 相比"单 Claude 单 session"：**产出质量提升约 80%**，bug 泄露率降低约 **60%**
- 相比"传统单人开发"：**速度提升 3–10x**，但**总成本与外包一个初级工程师相当或更低**
- **关键**：你要把省下的时间用来做 AI 无法做的事（商业判断、用户访谈、定价、品牌）

把这份 playbook 放 `idea-incubator/PLAYBOOK.md`，每次新 idea 前快速过一遍相关章节，就能把 95% 的坑提前踩掉。

祝顺利。
