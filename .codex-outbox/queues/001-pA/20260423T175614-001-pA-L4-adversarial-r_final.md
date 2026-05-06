# Adversarial Review · 001-pA · R_final

**Reviewer**: GPT-5.4 xhigh
**Completed**: 2026-04-24T01:30:24Z
**Runtime**: ~55 min
**Prior rounds**: R1 BLOCK (3 blockers); R_final verifies fixes + reviews expanded reference layer

## Executive summary (≤ 5 sentences)
结论是 **不能** 直接把这包规范交给 1 名架构师 + 6–8 名初级工程师开工。`reference/` 层确实把很多“怎么做”写到了可执行级别，但同时又引入了 3 条新的合同断裂：`paper_summaries` 的中文句界 CHECK 仍然不成立、LLM adapter/persist/env 契约仍有旧新两套并存、export envelope 在 architecture/task/API 三层不是同一份合同。R1 的三个 blocker 里，B1/B2 在“文档上看起来修了”，但至少前两条并没有闭合到端到端可实现。修完这 3 条后，我会把整体判断上调到至少 `CLEAN-WITH-NOTES`。

## Cross-check results (X1–X10)

| Check | Pass | Key findings |
|---|---|---|
| X1 Schema integrity | ❌ | `schema.sql §14` 的 `summary_sentence_cap` 仍用 `(?<=[.!?。！？])\\s+`；与 `testing-strategy.md §3.2` 的纯中文无空格句测例不相容。 |
| X2 API ↔ schema | ⚠️ | 大部分资源能映到 `schema.sql`，但 `api-contracts.md §3.11` / `E17` 的 export 契约和 `architecture.md §8` / `T023.md` 不是同一份 envelope。 |
| X3 LLM ↔ spec ↔ cost | ❌ | `tech-stack.md §2.4` / `llm-adapter-skeleton.md §2, §7` 已统一，但 `T004.md`、`T007.md`、`T013.md` 仍残留旧 casing、旧 provider 枚举、旧 DB 字段和旧价目。 |
| X4 Tasks ↔ reference | ❌ | `T010.md`、`T021.md`、`T023.md`、`T030.md` 与 `directory-layout.md §1` / `spec.md §5` 多处漂移；初级工程师会先卡在“到底该按哪份写”。 |
| X5 Testing catalog | ⚠️ | `testing-strategy.md` 覆盖面很强，但 D15 中文句界测试在现有 schema 下不可同时通过；export 测试也未覆盖 API 契约里的额外 top-level keys。 |
| X6 Ops runbook | ⚠️ | `ops-runbook.md §5, §9, §10` 很扎实，但 H6 的 Caddy 缓解删的是 query，不是 path token；`T030.md` 的权限验证命令也不可直接跑。 |
| X7 Junior readiness | ❌ | `T015` 基本可做，但 `T010` 与 `T021` 仍有合同级冲突；未达到“拿包就写、不必 pager 架构师”的标准。 |
| X8 Spec versioning | ⚠️ | `spec.md` 版本号与 changelog 已到 0.2.2，但 `spec.md §5` 仍保留旧 task 编号与旧 LLM interface。 |
| X9 New blockers | ❌ | reference 层新增/暴露了 3 个 blocker：D15 regex、LLM contract drift、export envelope drift。 |
| X10 Bus-factor | ⚠️ | `ops-runbook.md §9.I4` 与 `§10` 已明显补强 BUS-1，但缺席文件仍是运行时临时生成，不是现成模板。 |

## Blockers (must fix before Phase 0)

- **B1 · `paper_summaries.summary_sentence_cap` 仍无法机械覆盖纯中文/无空格句界，R1 的 B1/B2 没有闭合到底。** `reference/schema.sql §14` 明写“句末标点后可选空白”，但实际 CHECK 仍是 `(?<=[.!?。！？])\s+`，见 [schema.sql](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/schema.sql:521)。这与 `reference/testing-strategy.md §3.2` 要求接受“3 句纯中文 `。`”并拒绝“5 句纯中文 `。`”直接冲突，见 [testing-strategy.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/testing-strategy.md:273)。按当前定义，`中文。第二句。第三句。` 会被当成 1 段，5 句纯中文也可能误放行，所以红线 2 的 DB 层兜底并未真正成立。修法应是先统一真正支持无空格中英句界的 split 规则，再反向同步 `T003.md` / `T004.md` / `T013.md` 的说明与测试。

- **B2 · LLM 核心合同仍是一包互斥说明，T004/T007/T013 无法被不同 junior 独立实现后无缝拼接。** 权威定义已经很清楚：`tech-stack.md §2.4` 与 `reference/llm-adapter-skeleton.md §2, §7` 都要求 `SummaryRecord` 用 camelCase、`judgeRelation` 是 per-pair、adapter 不写 DB、caller 写 `llm_calls` + `paper_summaries`，provider 名是 `anthropic|openai`，见 [tech-stack.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/tech-stack.md:94) 和 [llm-adapter-skeleton.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/llm-adapter-skeleton.md:96)。但 `T004.md` 仍写着 snake_case `SummaryRecord`、batch 风格 `judgeRelation`、以及“adapter 内部写 `llm_calls`”与“adapter 不写两张表”并存，见 [T004.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/tasks/T004.md:41)。`T013.md` 更进一步同时使用了不存在的 `llm_calls.kind`、不存在的 `llm_calls.created_at`、旧的 GPT 输出单价 `$10/M`、以及“adapter 已写 llm_calls”与“persist 再写一次 llm_calls”两套流程，见 [T013.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/tasks/T013.md:42) 与 [schema.sql](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/schema.sql:469)。`T007.md` 又把 env 枚举写成 `claude|gpt`，但 `.env.example` 与 skeleton 用的是 `anthropic|openai`，见 [T007.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/tasks/T007.md:47) 与 [directory-layout.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/directory-layout.md:305)。这不是“文案有点旧”，而是会让不同 worker 产出根本拼不起来。

- **B3 · Export envelope 目前没有单一真源，T023/T032 无法被稳定实现或验收。** `architecture.md §8` 与 `T023.md` 把 export 定义成 snake_case、9 张表、portable-only payload，明确排除 `fetch_runs` / `paper_citations` / `sessions` / `llm_calls` / `export_log`，见 [architecture.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/architecture.md:278) 与 [T023.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/tasks/T023.md:35)。但 `reference/api-contracts.md §3.11` / `E17` 又把它写成 camelCase，并新增 `paperTopicScores`、`paperCitations`、`fetchRuns`、`exportedBySeatId` 等字段，且同一 endpoint 描述里还出现 `schema_version` 与 `schemaVersion` 混用，见 [api-contracts.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/api-contracts.md:569) 与 [api-contracts.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/api-contracts.md:806)。`reference/testing-strategy.md §2.5/§4.4` 只断言了一个混合子集，未帮你选边，见 [testing-strategy.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/testing-strategy.md:143)。`T023.md` 还让 route 调 `buildFullExport(env.LAB_ID)`，但 `.env.example` 并无 `LAB_ID`，见 [T023.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/tasks/T023.md:40) 与 [directory-layout.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/directory-layout.md:292)。在 Phase 2 开工前，必须先把 export payload 的字段集合、casing、lab 来源统一成一份合同。

## High-severity concerns

- `T021.md §Outputs/Verification` 仍用 `6w|3mo|6mo`，但 `schema.sql §10` 与 `api-contracts.md §3.8` 只接受 `timed_6wk|timed_3mo|timed_6mo`；同一个 resurface event 现在有两套枚举，见 [T021.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/tasks/T021.md:37)、[schema.sql](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/schema.sql:373)、[api-contracts.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/api-contracts.md:749)。
- `T010.md`、`api-contracts.md E6`、`directory-layout.md §1` 三者对 Topic CRUD 不是同一任务：task 编号是 T010，但 API 文档写 T009；task 验证要求 400 `TopicCapExceeded`，API 契约要求 422 `TOO_MANY_TOPICS`；文件路径又是 `topics/new` / `[id]/page` vs `[id]/edit/page` + `crud.ts`，见 [T010.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/tasks/T010.md:8)、[api-contracts.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/api-contracts.md:272)、[directory-layout.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/directory-layout.md:58)。
- `T030.md` 的部署工件与验证流程仍未收口：systemd unit 明明是 `T007.md` 的产出，但 `T030.md` Goal 又把它算作本 task；备份脚本路径写成 `deploy/backup/*`，而 `directory-layout.md` / `ops-runbook.md` 用的是 `deploy/scripts/*`；权限验证还把 DB role 当成 OS user 去 `sudo -u webapp_user`，见 [T030.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/tasks/T030.md:39)、[T007.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/tasks/T007.md:38)、[directory-layout.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/directory-layout.md:20)、[ops-runbook.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/ops-runbook.md:247)。
- H6 的现有缓解写法是错位的：invite token 明确在 path param，不在 query；但 `ops-runbook.md §5` 的 Caddy 只删 query，仍会把 `/api/invite/<token>/consume` 整条 path 落到 access log，见 [api-contracts.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/api-contracts.md:157)、[DECISIONS-LOG.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/DECISIONS-LOG.md:301)、[ops-runbook.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/ops-runbook.md:656)、[risks.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/risks.md:43)。
- `spec.md §5` 的 phase 摘要仍保留旧 task 编号与旧接口描述，例如 `T005`=schema、`T007`=LLM adapter、`T029`=export，以及旧式 `summarize(paper): string`，这会反向污染 README 给 junior 的阅读路径，见 [spec.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/spec.md:149) 与 [spec.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/spec.md:189)。

## Pleasant surprises / things done well

- `README.md §2.2` 的“初级工程师 1 小时 kickoff 路线”非常强，尤其把 `directory-layout`、task file、API/DB/LLM/testing reference 的阅读顺序直接排好了，见 [README.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/README.md:29)。
- `reference/testing-strategy.md` 对 spec §6 的映射粒度很高，unit / db / e2e / fixture 都给到了具体文件名和断言句式，这点远超一般 spec 包。
- `reference/ops-runbook.md §9.I4` 与 `§10` 的 BUS-1 处理很扎实；“operator 缺席也不停 briefing”的 operational contract 已经成型。

## Junior-engineer stress test (X7 detail)

### T010

- **What a junior could do from the spec alone**：topic 输入校验、CRUD service、admin-only route、基础表单/表格 UI 都已经有足够业务上下文。
- **What would require architect consultation**：先要问清楚它到底是 `T009` 还是 `T010`；topic cap 该返回 400 `TopicCapExceeded` 还是 422 `TOO_MANY_TOPICS`；页面与模块到底落在 `topics/new + [id]/page + service.ts` 还是 `topics/[id]/edit + crud.ts`，见 [T010.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/tasks/T010.md:43)、[api-contracts.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/api-contracts.md:287)、[directory-layout.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/directory-layout.md:60)。
- **Estimated time to first-commit under ideal conditions**：45–90 分钟；若不先消歧，第一提交前就会停下来问人。

### T015

- **What a junior could do from the spec alone**：它是 3 个样本任务里最接近“可直接实现”的一个；skeleton copy 点、loader 语义、`recordAction` 三层守门、placeholder 文案、manual verification 都写得相当具体，见 [T015.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/tasks/T015.md:48)。
- **What would require architect consultation**：测试文件应该落在 `tests/lib/actions/**` / `tests/app/today/**`，还是 `reference/testing-strategy.md` 规定的 `tests/unit/actions.test.ts` / `tests/e2e/skip-requires-why.spec.ts`；另外 `directory-layout.md` 并未把 `src/lib/today/loader.ts`、`src/lib/actions/service.ts` 写进“完整目录树”，见 [T015.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/tasks/T015.md:56) 与 [testing-strategy.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/testing-strategy.md:50)。
- **Estimated time to first-commit under ideal conditions**：30–60 分钟。

### T021

- **What a junior could do from the spec alone**：citation JOIN、timed 调度、`context_text` 模板、以及把 hook 放在 briefing 之后，这些业务意图都足够明确。
- **What would require architect consultation**：最核心的 `trigger_type` 枚举现在有两套；`directory-layout.md` 也没列出 `src/lib/resurface/context.ts` / `types.ts`，但 task 需要它们；`UNIQUE` / 幂等策略靠应用层还是 schema 也没一锤定音，见 [T021.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/tasks/T021.md:37)、[schema.sql](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/schema.sql:385)、[directory-layout.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/directory-layout.md:112)。
- **Estimated time to first-commit under ideal conditions**：30 分钟能搭脚手架，但有意义的实现会在枚举/文件归属处卡住。

## Remaining R1 H1–H10 status

由于用户指定的 `.codex-outbox/20260423T142034-001-pA-L4-adversarial-r1.md` 现已不是 001-pA 内容，本段以 `specs/001-pA/STATUS.md §Deferred` 为索引，再结合 reference 层逐项核验，见 [STATUS.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/STATUS.md:140)。

- **H1**：未被 reference 层实质解决；仍是“self-report 替代外部证据”的 accepted tradeoff，见 [STATUS.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/STATUS.md:141)。
- **H2**：未实质解决；`api-contracts.md §3.6` 仍明确 `labActions` 在 v0.1 可返回空数组，见 [STATUS.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/STATUS.md:142) 与 [api-contracts.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/api-contracts.md:717)。
- **H3**：未解决；仍是 Week 1 dogfood 暴露再补的 deferred 项，见 [STATUS.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/STATUS.md:143)。
- **H4**：未解决；仍主要停留在 `risks.md TECH-5` 的登记层，见 [STATUS.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/STATUS.md:144)。
- **H5**：**部分 addressed**；`directory-layout.md §9` 已放入 `export-route-scan` 的 CI 草稿，但仍注释掉，尚未前置守门，见 [STATUS.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/STATUS.md:145) 与 [directory-layout.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/directory-layout.md:664)。
- **H6**：**保留且已文档化**；`DECISIONS-LOG drift 5`、`risks.md SEC-10`、`api-contracts.md E2 Notes` 都完整记录了 accepted risk，但 runbook 的“删 query string 日志”并不能保护 path token，实际防线弱于文档口径，见 [STATUS.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/STATUS.md:146)、[DECISIONS-LOG.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/DECISIONS-LOG.md:301)、[risks.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/risks.md:43)。
- **H7**：**大体 addressed**；`reference/llm-adapter-skeleton.md §6/§10` 确实补了 XML wrap、system prompt、防御清单和 adversarial fixture，但我会把它保留在“高强度复核后仍建议继续观察”的状态，见 [STATUS.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/STATUS.md:147) 与 [llm-adapter-skeleton.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/llm-adapter-skeleton.md:682)。
- **H8**：**reference 层 incidentally addressed，但未端到端闭合**；`llm-adapter-skeleton.md §7` 已把 `summarize` 与 `judge` 都放到 `recordLLMCall()` 前置预算检查里，但 `T004.md` / `T013.md` 仍与该归属冲突，所以实现层还会重新破口，见 [STATUS.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/STATUS.md:148) 与 [llm-adapter-skeleton.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/llm-adapter-skeleton.md:817)。
- **H9**：**部分 addressed**；`T001.md` 与 `llm-adapter-skeleton.md §8` 都给了扩到 40 条样本的升级建议，但默认 contract 仍是 20 条，最终是否加样本仍留给 operator kickoff 时拍板，见 [STATUS.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/STATUS.md:149)。
- **H10**：**addressed**；`ops-runbook.md §9.I4` + `§10` 已把 operator 缺席、lab member 权限边界、回归检查都写成可执行 SOP，见 [STATUS.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/STATUS.md:150) 与 [ops-runbook.md](/Users/admin/codes/ideababy_stroller/specs/001-pA/reference/ops-runbook.md:1201)。

## Final verdict
- **BLOCK** — 当前至少有 3 条 blocker，而且都打在主干任务合同上，不是“边角文案”问题。只要 `T004/T007/T013` 与 `T023` 仍允许不同 junior 从不同文档读出不同真相，就还没达到“架构师放手、junior 直接开工”的 bar。

## Operator's personal action list
1. 先统一 **LLM 单一真源**：provider 枚举、`SummaryRecord` casing、`judgeRelation` 形状、`llm_calls` 归属、`purpose/called_at` 字段名、GPT `$15/M` 价目，一次性同步 `spec.md §5`、`T004.md`、`T007.md`、`T013.md`、`tech-stack.md §2.4`、`reference/llm-adapter-skeleton.md §2/§7`。
2. 再统一 **export 单一真源**：明确 top-level keys、snake_case 还是 camelCase、`lab` 来源是 session 还是 env、是否含 `paperTopicScores/paperCitations/fetchRuns`，然后同步 `architecture.md §8`、`T023.md`、`api-contracts.md §3.11/E17`、`testing-strategy.md §2.5/§4.4`、`spec.md §5`。
3. 最后修 **D15 中文句界**：改 `summary_sentence_cap` 的 regex/实现策略，加入“纯中文无空格”“中英混合无空格”“无尾标点”真实 DB 测例，并做一次短 R_final follow-up 只复核 X1/X3/X5。
