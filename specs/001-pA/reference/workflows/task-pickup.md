# Task Pickup · 001-pA · PI Briefing Console

**版本**: 0.1
**创建**: 2026-04-23
**读者**: 刚拿到任务 `T<NNN>` 的初级工程师
**用法**: 第一次被分派任务时从头读一次;之后每次只需对照 §2 的 checklist

> "我被分配了 task T015 / T023 / T032 —— 接下来该做什么?" 本文档给出**单一权威流程**。不要跳步;每一步都是 adversarial review 抓漏的常见点。

---

## §1 核心纪律(5 条)

1. **Specs 不可改**。你在 `src/` / `tests/` 里写代码;`specs/001-pA/**` 里的所有文件只读(包括 skeletons)。spec 有疑问 → 见 §4 "遇到 spec 模糊"。
2. **TDD**。测试先写、必定 fail、然后实现、然后 green(CLAUDE.md 硬性)。不存在"先写实现再补测试"的 loop。
3. **File domain 严格**。task file 里的 `file_domain` 列出你允许修改的路径清单。写任何其他路径 = PR 必拒。
4. **Dependencies 验证**。`depends_on` 列出的上游 task 必须全部 merge 进 main。如果还没,你停下;不要开始本 task。
5. **TODO 指向哪就抄哪**。skeleton 的 TODO 注释已经指定了"去哪找规范"(`reference/xyz.md §N`);按那里的条款实现。不要猜。

---

## §2 10-step pickup checklist

**你的终点判断**:PR 已开,第一轮 `pnpm typecheck && pnpm test && pnpm lint && pnpm build` 都绿。

### Step 1 · 读 task file(≤ 10 min)

```bash
less specs/001-pA/tasks/T<NNN>.md
```

重点读:
- `Goal`(一句话说清要做什么)
- `spec_ref`(指向 `spec.md` / `architecture.md` / `reference/*.md` 的具体行号)
- `depends_on`(上游 task)
- `file_domain`(你允许编辑的路径)
- `Outputs`(本 task 必须交付的文件 / 函数 / 测试)
- `Verification`(本 task 的 gate;你的 PR 必须过这些)
- `Implementation plan`(给你的实现步骤 guide · 不是铁律但通常就是正解)

### Step 2 · 验 depends_on 都已 merge

```bash
# 对每个上游 task,确认 main 里有 "Closes T<NNN-up>" 的 commit
git log main --oneline --grep="Closes T<NNN-up>"
```

没找到 → 该任务还没合。**停下**。私信 operator 或看 `specs/001-pA/dependency-graph.mmd` 确认次序。

### Step 3 · 读 spec_ref 指向的原文(10–20 min)

打开 task 引用的每个 `spec.md §X` / `architecture.md ADR-N` / `reference/*.md` 条款,**逐字读完**。不能跳读;条款里通常有"必须 / 禁止 / 默认"的限定词,漏看会在 review 被打回。

### Step 4 · 找到要 copy 的 skeleton

对照 `reference/skeletons/README.md §3` 表格,找你的 task 对应的 skeleton:

```bash
# 举例:T015 对应 recordAction + skip-why-input
ls specs/001-pA/reference/skeletons/
```

如果你的 task 在表里没对应 skeleton(少数纯配置 / 脚本 / 测试的 task 没有 skeleton)→ 直接在 `src/` 下按 `directory-layout.md §1` 指定的路径新建。

### Step 5 · 创建分支

按 `workflows/git-branching.md` 约定:

```bash
git checkout main
git pull
git checkout -b feat/T<NNN>-<kebab-short-desc>
```

**例**:
- `feat/T015-skip-why-input`
- `feat/T023-export-full-route`
- `fix/T018-breadcrumb-dedupe`

### Step 6 · Copy skeleton + 首先写失败的测试

**非常重要的 TDD 顺序**:

1. Copy skeleton(见 §3):
   ```bash
   cp specs/001-pA/reference/skeletons/recordAction.ts \
      src/lib/actions/recordAction.ts
   # 如有 UI 组件:
   cp specs/001-pA/reference/skeletons/skip-why-input.tsx \
      src/components/skip-why-input.tsx
   ```

2. **先**在 `tests/unit/actions.test.ts` 写一个**必然 fail** 的测试:
   ```typescript
   it('should reject skip action when why is shorter than 5 chars', async () => {
     const result = await recordAction({ paperId: 1, action: 'skip', why: 'no.' });
     expect(result.ok).toBe(false);
     if (result.ok === false) expect(result.code).toBe('SKIP_WHY_REQUIRED');
   });
   ```

3. 跑 `pnpm test tests/unit/actions.test.ts` → 确认**红**(fail)。

### Step 7 · 填 TODO 直到测试绿

按 skeleton 里 TODO 的顺序逐个实现;对每个 TODO 确认:

- 它的 `T<NNN>` 归属就是**你**的 task(若不是,说明 skeleton 有 bug 或你搞错了 file_domain;停下确认)
- 它指向的 `reference/xyz.md §N` 条款你已经读过

实现完一个 TODO 跑一次 `pnpm test:watch`,保持测试从红转绿的节奏。

### Step 8 · 补边界 / 红线测试

**每个 task 至少覆盖**:
- 快乐路径(happy path)- 至少 1 测试
- 每个 `Verification` 条目 - 1 测试/条
- 每个错误 code - 1 测试/code
- 红线 2 相关任务(T003 / T015 / T013)**必加 DB CHECK 测试**到 `tests/db/constraints.test.ts`

测试命名 per CLAUDE.md:`should <expected> when <condition>`。

### Step 9 · 跑完整 CI 等价套装

```bash
pnpm typecheck
pnpm lint
pnpm test
pnpm build
# E2E 任务才跑:
pnpm test:e2e tests/e2e/<你改的那条 spec>.spec.ts
```

**任何一条红**不得提 PR。

### Step 10 · 提 PR

按 `workflows/pr-review.md §1` 的 PR template 填写描述。commit message 按 `workflows/git-branching.md §2`:

```
feat(T015): add skip-why-input component

- Inline-expand UI with disabled-until-≥5-chars gate (D16 Layer 3)
- Wires recordAction via useTransition
- Playwright e2e verifies O-verify-c6-ui hook

Closes T015
```

push 前:**跟 operator 确认一次**(CLAUDE.md 硬性规定)。

---

## §3 Copy skeleton 的细则

1. 只 `cp`,**不**用 `mv`(保留 specs 下的原件)
2. 目标路径必须与 skeleton banner 里写的路径一致;不要"改到别的地方去"
3. 拷过去后第一件事是**把 banner 里的 "Skeleton for" 字样去掉**(这是你从现在起维护的真正代码,不是 skeleton 了)
4. 如果两个 task 依次修改同一个 `src/` 文件,后一个 task 不再 `cp` skeleton,而是在前一个 task merge 后的文件基础上继续改

---

## §4 遇到 spec 模糊怎么办

**最差做法**:在 `src/` 里按你的猜测实现,PR 里不声明 ambiguity —— 一定被 review 打回或 adversarial 抓到。

**正确做法**:

1. 打开 `specs/001-pA/OPEN-QUESTIONS-FOR-OPERATOR.md`
2. 新增一个 Q 条目:
   ```markdown
   ### Q<NN> · T<NNN> · <一句话问题>
   **Context**: spec.md §X 写了 "...",但未覆盖 <边界情况>。
   **我倾向**: <option A / B>
   **需要 operator / spec-writer 裁决**
   **Impact**: 此 Q 未决前本 task PR 保持 draft
   ```
3. PR 标记为 Draft,在 PR 描述里 @ operator
4. 等回复,按裁决改;若裁决触发 spec 改动,由 spec-writer 改 spec.md,不是你改

---

## §5 file_domain 小抄(常见 task 示例)

| Task | file_domain(你能改的路径) | 禁区(碰了会 PR 拒) |
|---|---|---|
| T003 · DB schema | `src/db/schema.ts` · `src/db/migrations/0000_initial.sql`(drizzle-kit 生成) · `tests/db/**` | `reference/schema.sql`(spec-writer 区) |
| T004 · LLM adapter | `src/lib/llm/**` · `tests/unit/llm-*.test.ts` · `src/db/schema.ts`(仅 llm_calls 列若有补丁) | `reference/llm-adapter-skeleton.md`(spec-writer 区) |
| T015 · Action API | `src/app/api/actions/route.ts` · `src/lib/actions/recordAction.ts` · `src/components/skip-why-input.tsx` · `tests/e2e/skip-requires-why.spec.ts` | `reference/api-contracts.md` · `src/db/schema.ts` |
| T023 · Export | `src/app/api/export/full/route.ts` · `src/lib/export/**` · `tests/e2e/admin-export.spec.ts` | `reference/api-contracts.md §3.11`(envelope 契约) |
| T030 · Deploy | `deploy/**` · `scripts/pg-dump.sh` · `src/app/api/healthz/route.ts` | `src/app/**`(除 healthz) · `src/lib/**` |

精确 file_domain 看具体 task file `Domain` 字段。

---

## §6 Task 完成标准(判定 "done")

PR 能 merge 的条件(同时满足):
- [ ] `pnpm typecheck` 绿
- [ ] `pnpm test` 绿(且**新增 ≥ 1 个测试**;pure doc/scripts 任务豁免)
- [ ] `pnpm lint` 绿
- [ ] `pnpm build` 绿
- [ ] 如涉及 UI / API 改动:相关 `pnpm test:e2e` 绿
- [ ] Task `Verification` 段每条都有对应测试或手动验证报告
- [ ] PR 描述填 `Closes T<NNN>` 和 review-bar checklist
- [ ] 至少 1 个 reviewer 批准(spine task:T003 / T004 / T015 需架构师批准)
- [ ] 无 spec 文件被改(或,若改了,附 spec-writer 书面批准)

---

## §7 常见"卡住"场景

| 场景 | 解法 |
|---|---|
| 上游 task 没 merge 但你等不起 | 创建 stub branch `chore/T<NNN-up>-stub` 只导出空函数以 unblock;上游真 merge 后你 rebase |
| skeleton 和 spec 不一致 | skeleton 有 bug,打开 OPEN-QUESTIONS,让 spec-writer 决定修 skeleton 还是 spec |
| 测试写不出来(比如 worker 里的 cron) | 把被测逻辑拆到可注入时钟的函数里(`Clock` interface),测试注 fake clock |
| 外部 API(arXiv / LLM)不稳 | 单测全 mock(`vi.mock('@anthropic-ai/sdk')`);集成测试用 vcr-style 录制 fixture |
| 本地 DB 状态乱了 | `dropdb pi_briefing && createdb pi_briefing && psql -d pi_briefing -f specs/001-pA/reference/schema.sql && pnpm db:seed` |

---

## §8 变更日志

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-23 | 0.1 | 初版 · 10-step checklist + file_domain 小抄 |
