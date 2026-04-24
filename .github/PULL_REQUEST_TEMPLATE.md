## 变更内容

<!-- 一段描述：解决了什么问题，为什么要做这个改动 -->

## Task 引用（如适用）

- [ ] specs/003-pA/tasks/T<!-- NNN -->.md

## Non-goal 检查（v0.1 红线）

以下三条来自 `specs/003-pA/non-goals.md §7`：

- [ ] 不引入多用户 / 账号 / 权限系统（N1-1 至 N1-5：v0.1 单 worker 顺序执行）
- [ ] 不引入 Docker / 容器隔离（非 v0.1 范围；本机单卡直接运行）
- [ ] 不引入 HPO / 大规模调度（N3-x 系列：v0.1 不做超参搜索或多 run 并发）

## Quality

- [ ] `uv run ruff check .` 通过（lint 零 error）
- [ ] `uv run ruff format --check .` 通过（格式一致）
- [ ] `uv run pytest -m "not slow and not gpu"` 通过（fast test 全绿）
- [ ] 覆盖率 ≥ 70%（CI 会自动检查；本地可用 `--cov=pars --cov-fail-under=70` 验证）
- [ ] 更新了 `CHANGELOG.md`（面向用户的改动需要记录）

## 测试说明

<!-- 如何手动验证这个 PR 的改动：步骤、预期输出、边界情况 -->
