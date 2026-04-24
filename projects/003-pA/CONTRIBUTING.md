# Contributing to RecallKit

## Bus-factor 声明

RecallKit 是**单人维护的研究工具**（见 `specs/003-pA/risks.md` R9 / BUS-1）。

- Issue / PR 回应以 **best-effort** 方式进行，无固定响应 SLA
- 不保证 v0.1 之后的 API 兼容性（pre-1.0 semver 语义）
- 若主维护者长期不可用，项目处于"存档但可 fork"状态

如果你依赖本项目用于生产环境，建议 fork 并自行维护。

---

## PR 合并检查清单

提交 PR 前，请确认以下 4 项全部通过：

- [ ] **Ruff lint + format pass**
  ```bash
  cd projects/003-pA
  uv run ruff check .
  uv run ruff format --check .
  ```

- [ ] **Fast test pass + coverage ≥ 70%**
  ```bash
  uv run pytest -m "not slow and not gpu" --cov=pars --cov-fail-under=70
  ```

- [ ] **更新 `CHANGELOG.md`**（面向用户的改动必须记录在 `## [Unreleased]` 段）

- [ ] **不违反 `specs/003-pA/non-goals.md` 中的任一条**。以下是前 3 条红线供快速核对：
  1. **N1-1** — 不引入多 worker 并行 / 协作机制（v0.1 单 worker 顺序执行）
  2. **N2-1** — 不引入 prompt 优化 / agent scaffold 工作流（定位是 LoRA SFT 决策循环）
  3. **N3-1** — 不引入 RLHF / RLAIF（硬件 + 复杂度超 v0.1 范围）

---

## 依赖升级流程

1. 阅读 `specs/003-pA/tech-stack.md`（§5 版本锁定策略 + §6 依赖升级原则）
2. 在 pyproject.toml 中更新版本 pin，**不使用 `^` 或 `~` 通配**（生产依赖 exact pin）
3. 重新生成 lock 文件：`uv lock` 后更新 `requirements-locked.txt`
4. 运行 `uv run pip-audit -r requirements-locked.txt --strict` 确认无 CVE
5. Commit message 中说明升级理由和来源（upstream changelog / CVE ID）

---

## Commit 规范（Conventional Commits）

格式：`<type>(<scope>): <description>`

| type | 用途 |
|------|------|
| `feat` | 新功能 |
| `fix` | bug 修复 |
| `refactor` | 重构（不改变行为） |
| `docs` | 文档更新 |
| `test` | 测试增删改 |
| `chore` | 构建工具 / 依赖 / CI 配置 |

**scope**：通常是 Task ID（如 `T028`）或模块名（如 `orchestrator`）。

示例：
```
feat(T015): add stuck_lock detection with 60s SIGINT safety net

closes specs/003-pA/tasks/T015.md
```

Conventional Commits 在 CI 中由 `wagoid/commitlint-github-action` 自动校验。

---

## 相关规范文件

- `specs/003-pA/spec.md` — 整体设计规范
- `specs/003-pA/non-goals.md` — 明确不做的事（PR 必须对照）
- `specs/003-pA/SLA.md` — 质量 gate 与错误预算
- `specs/003-pA/compliance.md` — 许可证与 artifact 合规要求
- `docs/demo-artifact-checklist.md` — demo 分发前检查清单
