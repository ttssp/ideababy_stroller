# Forge v8 · 006 · P2 · GPT55xHigh · 参照系评估(with search)

**Timestamp**: 2026-07-13T19:51:44+08:00
**Searches run**: 6, SOTA-benchmark
**Visibility**: 我已读对方 P1。

## 1. SOTA 对标

| 标的 X' | 参照项 | SOTA 形状 | 对本批的含义 | URL/Source |
|---|---|---|---|---|
| B2 + worktree 隔离 | CAID / git worktree / Claude CLI | SOTA 是 isolated workspace + branch/merge;Git worktree 原生支持多 working tree;本机 `claude --help` 有 `-w, --worktree [name]`;STORM 提醒隔离后仍需状态管理 | worktree 应默认命令化,但先用轻 preflight,不急着上重 hook | https://arxiv.org/abs/2603.21489 · https://arxiv.org/abs/2605.20563 · https://git-scm.com/docs/git-worktree |
| B5 role 分离 | OpenAI Model Spec + OWASP LLM01 | 现代接口用 role/authority message;OWASP 要隔离外部内容、最小权限、代码侧校验 | `complete(prompt)` 落后,应判 new(契约变更),迁移路径另保留 | https://model-spec.openai.com/2025-09-12.html · https://genai.owasp.org/llmrisk/llm01-prompt-injection/ |
| B4 + B7 gate | GitHub approval + AP2 nonce | GitHub environment gate 绑定 reviewer/pending/secrets;AP2 研究强调 context binding、time-bound nonce、consume-once | B4 静态 PASS 与 B7 防重放应合并成 gate 执行语义 | https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments · https://arxiv.org/abs/2602.06345 |
| B3 + B6 | detect-secrets / Gitleaks | 主流 secret scanning 用 baseline、audit、集中 ignore/fingerprint 降误报 | Safety Floor 不降级;误报治理集中化、可回审,避免 worker 临场绕法 | https://github.com/Yelp/detect-secrets · https://github.com/gitleaks/gitleaks |
| B2 非 main 基线 | GitHub PR base | PR base branch 可显式选择;部署环境也可限制 branch/tag | main-only 不是通用前提;baseline 必须进入 handoff/preflight | https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/changing-the-base-branch-of-a-pull-request |

## 2. 用户外部材料消化

K 本轮没有额外外部材料;只要求按 SOTA 搜索校正 P1,已在 §1 处理。

## 3. 修正后的视角

- 我 P1 把 B5 判为 **refactor**;搜索后改为 **new(契约变更)**。OpenAI/OWASP 参照共同指向 role/authority、不可信内容隔离、代码侧边界,这不是在原 `prompt: str` 上补丁能完成的事。这里我接受 Opus P1 的判级,但保留“必须给 T001 兼容迁移”的约束。
- 我 P1 对 worktree 强制层级不确定;现在上调为 **默认命令化 + 轻 preflight**。Claude CLI 与 CAID 都支持 worktree 作为默认隔离,但 STORM 说明还要显式状态/冲突管理。
- 我 P1 对 B4+B7 是否同一强度犹豫;现在更接近 Opus:二者应合为 gate 执行语义。nonce 一次性消费、run/context 绑定、stale 作废是通用授权不变量。
- B3/B6 与 B2 的 refactor 判断站住但更收窄:hook 误报用 baseline/ignore/audit 集中治理;build baseline 用机器可读声明,不能默认为 main。
