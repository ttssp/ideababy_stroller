# On-boarding Day 1 · 001-pA · PI Briefing Console

**版本**: 0.1
**创建**: 2026-04-23
**读者**: 新加入 001-pA 项目的初级工程师(第一天)
**目标**: 结束前开出你的第一个 PR(可 WIP)

> Day-1 不是"学完整个项目"。是"把环境跑起来 + 读够 spec 能接 task + 开第一个 PR 让反馈 loop 启动"。照抄时间块,别跳步。

---

## §1 一天的节奏

| 时段 | 时长 | 活动 | 交付物 |
|---|---|---|---|
| 09:00–11:00 | 2h | Reading pass 1(产品 + 架构) | 读完 `README.md` + `spec.md` + `architecture.md §1-3` |
| 11:00–12:00 | 1h | Reading pass 2(自己的 task 上下文) | 读完被分配的 `tasks/T<NNN>.md` + 相关 `reference/*.md` 段 |
| 12:00–13:00 | 1h | 午餐 🍚 | — |
| 13:00–15:00 | 2h | 环境搭建 | `pnpm test` 本地绿(`workflows/local-dev-setup.md`) |
| 15:00–17:00 | 2h | 写第一个 failing test + 1 个 TODO 实现 | 第一次 commit |
| 17:00–18:00 | 1h | 开 PR(可 WIP) + 自检 | PR URL 交给 operator |

**到 18:00 如果 PR 没开,不必加班**;晚了 = 某步出了本文档没写明的坑,明天 15min 反思会收录。

---

## §2 Morning · reading pass 1(2h)

### 2.1 `README.md`(10 min)
- 读 §1–§3;理解项目是啥、你属于哪个 role(大概率"初级工程师")

### 2.2 `spec.md`(30 min)
- §1 Outcomes(O1–O5):知道产品**判生存**的 5 条指标
- §2 Scope IN/OUT:知道 v0.1 做什么,不做什么
- §3 Constraints:注意 C5–C7 三条红线,v0.1 是硬宪法
- §4 Prior Decisions D1–D16:**跳读**,留个印象;看到 D15 / D16 停下仔细读(这两条是红线 2 的代码兑现,你的第一个 PR 大概率涉及)
- §4.1 state-shift formal 定义:知道这是 provisional
- §5 Phase 划分:判断你的 task 属于 Phase 0/1/2/3
- §6 Verification:对应的验收命令

### 2.3 `architecture.md §1-3`(30 min)
- §1 C4 L1 (system context):外部是谁,系统边界在哪
- §2 C4 L2 (container):Web / Worker / DB 三块怎么放
- §3 ADR-1 到 ADR-7:一共 7 条架构决策,每条有 rationale;这是遇到"为什么这么做"最好的快查

### 2.4 自测(30 min;写个人笔记 · 不交)
回答以下 5 道题,答不出的回去读:
1. v0.1 的 5 个 Outcome 分别是什么?(不用背数字,能讲"日活 / resurface / 双 seat / 漏看案例 / aha")
2. 为什么主存储是自持 Postgres 而不是 Supabase?
3. Red line 2(不替代第一手阅读)的三层机械兜底是哪三层?
4. `/today` 页面有没有 `/api/today` endpoint?为什么?
5. Worker 几点跑?在什么进程里?

---

## §3 Morning · reading pass 2(1h)

### 3.1 打开你的 task file
```bash
less specs/001-pA/tasks/T<NNN>.md
```

### 3.2 根据 task 类别补读

| task 类别(例) | 必读 reference |
|---|---|
| API route(T009 / T015 / T023 / T027) | `reference/api-contracts.md` 对应 endpoint 块 + §1 global conventions |
| DB schema(T003) | `reference/schema.sql` 对应表 · `spec.md` D15/D16 |
| LLM adapter(T004 / T013) | `reference/llm-adapter-skeleton.md` §1–§5 |
| Worker pass(T011 / T012 / T014 / T021) | `architecture.md` ADR-1 / ADR-2 · `reference/ops-runbook.md` cron 块 |
| UI(T014 client / T015 UI / T019) | `reference/api-contracts.md` §3 shapes · CLAUDE.md 注释规则 |
| 测试 harness(T008) | `reference/testing-strategy.md` 全文 |
| 部署 / 运维(T030 / T031 / T033) | `reference/ops-runbook.md` 全文 |

### 3.3 打开 skeleton
```bash
cat specs/001-pA/reference/skeletons/README.md
# 定位你的 skeleton
ls specs/001-pA/reference/skeletons/
```

---

## §4 Afternoon 1 · 环境搭建(2h)

严格按 `workflows/local-dev-setup.md` 跑完 15 步。**时间盒 90 分钟,卡住 15 分钟以上求助**(不要死磕)。

到这一步结束你应该:
- `pnpm test` 本地绿
- `pnpm dev` 起来后 `http://localhost:3000/api/healthz` 返回 `{"status":"ok", ...}`
- Postgres 里 15 张表都在

---

## §5 Afternoon 2 · 第一行代码 + 第一个 commit(2h)

### 5.1 创建分支
```bash
git checkout -b feat/T<NNN>-<kebab-short>
```

### 5.2 Copy skeleton(如适用)
参考 `reference/skeletons/README.md §3` 找目标路径。

### 5.3 先写一个**必然 fail** 的测试
选 task `Verification` 的第一条,写成一个 `should ... when ...` 测试。

### 5.4 跑 `pnpm test:watch` 确认红

### 5.5 实现最小代码让测试绿
- 只做一个 TODO;不要一口气写完
- 遇到 "这个字段叫什么 / 该抛哪个 error code" 查 `reference/api-contracts.md` 和 `error-codes-and-glossary.md`,**不要猜**

### 5.6 第一个 commit
```bash
git add -p      # 逐 hunk 审视
pnpm typecheck  # 确认绿
pnpm lint       # 确认绿
git status --untracked-files=all   # CLAUDE.md 规范
git commit -m "feat(T<NNN>): <第一个 minimal 功能>"
```

Conventional Commits 格式参考 `workflows/git-branching.md §2`。

---

## §6 End of day · 开 PR(1h)

### 6.1 push 分支
**先和 operator 确认**(CLAUDE.md),再 push。

### 6.2 开 PR
- 标题 = 你的 commit subject
- 描述按 `workflows/pr-review.md §1` template 填写
- Draft PR 也可以(WIP 状态),但 template 必须填
- 贴 PR URL 给 operator

### 6.3 自检 review bar
用 `workflows/pr-review.md §2` review bar 自审一遍;确保有 CI 绿的前景。

---

## §7 Recommended starter tasks for day-1

如果架构师允许你自选第一个 task,优先挑以下(小、低风险、能快速过完整 loop):

| Task | 为啥适合 day-1 |
|---|---|
| **T008 · test harness** | 纯设施 task,无业务逻辑,但让你把 vitest + Playwright 跑通 |
| **T031 · runbook template** | 纯 docs task;帮你熟悉 reference 体系 |
| **T009 · Topic CRUD**(简单 endpoint) | 小型 API + DB 组合,覆盖从 zod 到 Drizzle 的完整切片 |
| **T030 healthz 部分** | 只是 healthz route,一个文件,纯粹 |

**不适合 day-1**:
- T001(LLM spike)· 需要 provider 判断经验
- T003(DB schema)· 牵一发动全身,spine task
- T012 / T013 / T021(worker)· 跨多模块
- T023(export)· SEC-1 合规要求高

---

## §8 判断"你今天算成功了吗"

结束前 15 min 自问:

- [ ] 我知道 v0.1 的 5 个 Outcome + 3 条红线?
- [ ] 我的本地 `pnpm test` 绿?
- [ ] 我今天至少 commit 1 次?
- [ ] 我开了一个 PR(即便 WIP)?
- [ ] 我知道明天早上该从哪儿继续?

**≥ 4 项 yes = 成功**;否则约 operator 明早 15min 对齐。

---

## §9 常见 day-1 心理包袱 + 回应

| 想法 | 回应 |
|---|---|
| "我 spec 看不懂,该不该先全看懂再写代码?" | 不。先能跑起来,在实践中不断回来看 spec |
| "我看到 skeleton 有 TODO,这不就等于没实现吗?" | 对;skeleton 的唯一目的是让后续 task**不被 blocking**。你的 task 就是填它 |
| "我改一下 skeleton 让它更合理可以吗?" | 不可以。skeleton 是 spec-writer 维护;要改走 `/spec-patch` |
| "我卡了 2 小时还没跑起来,是不是我的问题?" | 不是。15 min 卡住就求助,这是给后来人节省时间的投资 |
| "我的 PR 第一版会不会太 naive?" | 会。但是开出来 = 反馈 loop 启动;不开 = 无人知道你卡在哪 |

---

## §10 变更日志

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-23 | 0.1 | 初版 · 8h day-1 节奏 + starter tasks |
