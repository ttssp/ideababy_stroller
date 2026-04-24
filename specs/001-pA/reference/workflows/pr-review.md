# PR Review · 001-pA · PI Briefing Console

**版本**: 0.1
**创建**: 2026-04-23
**读者**: PR 作者 + reviewer
**原则**: 有 1 位 reviewer approve,CI 全绿,file_domain 无越界,即可 squash merge;spine task 需架构师 approve

---

## §1 PR 描述模板(**作者必填**)

在 GitHub 开 PR 时,贴入以下 template。`.github/pull_request_template.md`(T002 交付)里会预填这个模板。

```markdown
## Summary
<1–2 bullet points · 本 PR 做了什么>
- <bullet 1>
- <bullet 2>

## Task
Closes T<NNN>

## Verification
- [ ] `pnpm typecheck` 绿
- [ ] `pnpm test` 绿(<N> 个新测试)
- [ ] `pnpm lint` 绿
- [ ] `pnpm build` 绿
- [ ] E2E: `pnpm test:e2e tests/e2e/<spec-file>.spec.ts` 绿(UI / API 改动时必填)
- [ ] 手动 smoke: <描述你点了什么 / 跑了什么命令、期望 / 实际输出>

## Spec impact
- [ ] 未修改 `specs/**`
- [ ] 如修改了 spec 文件,附 spec-writer 批准 comment 链接:<URL>

## Red line 2 compliance(仅 T003 / T013 / T015 需勾)
- [ ] DB CHECK(`skip_requires_why` / `summary_sentence_cap`)已经过 constraint test 覆盖
- [ ] API validation 已覆盖(zod refine + error code)
- [ ] UI disabled gate 已覆盖(Playwright `disabled` 断言)

## Risks
<任何顾虑 / trade-off · 对应 risks.md 某条 ID,如 TECH-3 / SEC-1>

## Screenshots / demos
<UI 改动必附;非 UI 跳过>
```

---

## §2 Review bar(**reviewer 必过**)

作为 reviewer,读到这份 PR 要确认的**硬标准**(任一项红灯 = request changes):

### 2.1 合同符合性
- [ ] PR 改动的文件**完全**在 task file `file_domain` 列表内
- [ ] Task 的 `Outputs` 每一条都在 PR 里出现
- [ ] Task 的 `Verification` 每一条都有测试或手验报告
- [ ] `Closes T<NNN>` 在 PR 描述或 commit message 里

### 2.2 代码质量
- [ ] 函数 / 变量名语义清晰,非缩写(`trimmedWhy` 而非 `tw`)
- [ ] **代码注释用中文、先结论后细节、结构化**(CLAUDE.md 硬性)
- [ ] `noUncheckedIndexedAccess` 下数组 `arr[i]` 必经 `if (!x) throw` 守卫
- [ ] 无 `any`(Biome 已禁;偶有必要时用 `unknown` + 类型守卫)
- [ ] 无 `console.log`(生产代码应通过 `src/lib/log.ts`;仅 dev 允许)

### 2.3 测试
- [ ] 新增测试符合 `should ... when ...` 命名(CLAUDE.md)
- [ ] 覆盖快乐路径 + 每个错误分支
- [ ] 涉及 DB 的任务有 `tests/db/` 测试(连真实 Postgres)
- [ ] 涉及 UI 的任务有对应 Playwright e2e

### 2.4 spec / reference 一致性
- [ ] 未修改 `specs/001-pA/**`(或,若修改,spec-writer 已书面批准)
- [ ] 引入新 dep → `tech-stack.md §2` / `directory-layout.md §2` 已随 PR 更新
- [ ] 引入新 error code → `reference/error-codes-and-glossary.md §1` 已更新(这两件事必须 spec-writer 批)
- [ ] 新 env 变量 → `.env.example` + `src/lib/env.ts` zod schema 同步(directory-layout §3)

### 2.5 安全
- [ ] 无硬编码密钥(即使 placeholder)
- [ ] 外部 API 调用(arXiv / LLM)不在 web request path(ADR-2)
- [ ] 任何 `admin-only` 路由有 `requireAdmin` 调用 + 控制器层二次 `seat.role === 'admin'` 断言(SEC-1)

### 2.6 Red line 机械兜底(仅涉及时)
- [ ] `action='skip'` 路径:DB CHECK / API / UI 三层都有对应实现与测试(D16)
- [ ] `paper_summaries.summary_text`:adapter 截断 + DB CHECK 双兜底(D15)

---

## §3 Merge 规则

- **≥ 1 approval 必需**(GitHub branch protection 强制)
- **Spine task 需架构师 approval**:T003(DB schema) / T004(LLM adapter interface) / T015(红线 2 三层)/ T023(export 合规)
- **Squash merge only**(分支保护已配);merge 时 PR 标题作为最终 commit subject
- Merge 后 **立即** delete branch
- **CI 全绿**才能 merge(GitHub 强制);`pnpm audit --prod --audit-level=high` 失败 = 阻断

---

## §4 常见 review feedback(作者自检)

| Reviewer 可能 comment | 自检 |
|---|---|
| "这里应该用 error code X 而不是 Y" | 查 `error-codes-and-glossary.md §1` 的触发条件对不对 |
| "这个字段应该是 camelCase" | 跨层看:DB snake_case / TS camelCase / 映射在 `src/lib/summary/persist.ts` |
| "测试没覆盖 why=' ' 空格情况" | `btrim().length >= 5` 要在测试里显式验纯空格 |
| "为什么改了 `specs/`?" | 没得说,撤回改动;改 spec 走 `/spec-patch` 流程 |
| "file_domain 里没有这个路径" | 回去读 task file `Domain` 字段;动了不该动的 = 回滚 |
| "这里 async 函数没 await" | TS strict 下 floating promise 是 warn;要么 await 要么 `void` 显式忽略 |
| "commit 消息不符合 Conventional Commits" | 按 `git-branching.md §2` 重写,然后 `git commit --amend` + `git push --force-with-lease` |

---

## §5 做 reviewer 的正向反馈义务

发现好的实现要**显式说**:

- "nice — 这里用 discriminated union 让 TS 帮你兜底"
- "这个 test name 很清楚"
- "把 rate-limit 放到 adapter 外面是对的,正合 TECH-3 fallback 思路"

为什么重要:本项目是 solo operator + AI agent 协作,review 是**知识传播**的主要机制,不只是 gatekeeping。

---

## §6 Review 时长约定

| PR 规模 | Reviewer 承诺响应时长 |
|---|---|
| ≤ 200 行 diff | 当天(8h 内) |
| 200–500 行 | 1 个工作日 |
| 500–1000 行 | 2 个工作日 + 建议拆分 |
| > 1000 行 | **不接受**;作者必须拆成多个 PR |

**作者义务**:PR 规模控制在 ≤ 500 行;超了主动拆。

---

## §7 PR 卡住怎么办

| 场景 | 处理 |
|---|---|
| PR 开了 > 3 天无人 review | 作者在 PR 里 @operator + Slack/微信 ping 一次;operator 协调 |
| Reviewer request changes 超过 5 轮 | 停下,作者 + reviewer + 架构师开 15min 同步会对齐 |
| CI 因外部服务抖动红(如 arXiv API 挂) | 重跑 1 次;仍红则作者去查根因,不要关闭/重开 PR 刷 CI |
| 依赖的上游 PR 未 merge 导致 conflict | 本 PR 标记 blocked;待上游 merge 后 rebase |

---

## §8 变更日志

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-23 | 0.1 | 初版 · PR template + review bar + merge 规则 |
