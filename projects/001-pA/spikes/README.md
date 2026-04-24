# T001 LLM provider spike workspace

本目录是 T001 (Phase 0 blocking gate) 的工作区。权威 task 契约见
`specs/001-pA/tasks/T001.md`,prompt 来源是 `specs/001-pA/reference/llm-adapter-skeleton.md` §3 / §3.5 / §6。

## 内容

- `eval-harness.ts` — 主评测脚本 (CLI · TS strict)
- `runs/` — 每次运行的原始 JSON record (`<provider>-<ISO-ts>.json`)
- `T001-llm-provider-report.md` — 最终报告 (operator 跑完 eval 后填数字 + 签字)

## v0.1 评测范围

仅 **GLM5.1**(火山引擎 ARK · Anthropic-compatible 端点)。环境变量:

```
ANTHROPIC_BASE_URL=https://ark.cn-beijing.volces.com/api/coding
ANTHROPIC_AUTH_TOKEN=<volces ark token>
ANTHROPIC_MODEL=glm-5.1
```

## 4 条命令

```bash
# 1) dry-run 验证 prompt (不调 API · 无需 token)
ANTHROPIC_BASE_URL=x ANTHROPIC_AUTH_TOKEN=x ANTHROPIC_MODEL=x \
  pnpm tsx projects/001-pA/spikes/eval-harness.ts --provider glm --dry-run --fixture human-labeled --limit 2

# 2) human-labeled 真跑 (operator 必须先用真实 arxiv abstract 替换 fixture 里的 PLACEHOLDER)
pnpm tsx projects/001-pA/spikes/eval-harness.ts --provider glm --fixture human-labeled

# 3) adversarial 稳健性 (需 sibling agent 先生成 tests/fixtures/adversarial-abstracts.json)
pnpm tsx projects/001-pA/spikes/eval-harness.ts --provider glm --fixture adversarial

# 4) 查看上一次结果
ls -la projects/001-pA/spikes/runs/

# 5) (可选) 单独 typecheck 本 harness (不污染根 tsconfig)
pnpm tsc --noEmit -p projects/001-pA/spikes/tsconfig.json
```

## Fixture 位置

- `tests/fixtures/human-labeled-20.json` — 20 条 human-labeled (10 shift / 6 incremental / 4 unrelated)
- `tests/fixtures/adversarial-abstracts.json` — 15 条 / 5 大类 prompt-injection 样本 (见 `reference/testing-strategy.md §11.3`)

## Gate 阈值 (tech-stack.md §2.5)

`judge_accuracy ≥ 14/20 (70%)` + `monthly_cost_extrapolation_usd ≤ 50` + `p95_latency_ms ≤ 5000`。

任一不达标 → fallback heuristic + LLM 仅 summarize,触发 spec.md OP-Q1。
