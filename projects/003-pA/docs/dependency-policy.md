# 依赖管理策略

**版本**: 1.0  
**生效**: T002  
**对应风险**: R5 pip 供应链投毒（High）  
**对应约束**: C17 依赖白名单  

---

## §1 三重锁定原则

本项目使用三重锁定保障供应链安全：

| 文件 | 作用 | 格式 |
|------|------|------|
| `pyproject.toml` | 版本声明（runtime 全部 `==x.y.z` exact pin） | PEP 621 |
| `uv.lock` | 完整依赖图 + 精确版本，可重现解析 | uv 专有格式 |
| `requirements-locked.txt` | 每依赖含 SHA-256 hash，供 `--require-hashes` 校验 | pip 兼容格式 |

**三者必须同步提交 git**，不得分离。

---

## §2 依赖升级流程（操作员权限）

只有 **操作员** 可以升级依赖，流程如下：

```bash
# 1. 升级单个包（修改 pyproject.toml 声明）
uv add <pkg>==<new_ver>          # runtime 依赖
uv add --dev <pkg>==<new_ver>    # dev 依赖

# 2. 重新锁定并导出
bash scripts/lock-deps.sh

# 3. Review diff（重要：检查新增传递依赖）
git diff uv.lock requirements-locked.txt

# 4. 安全扫描
uv run pip-audit -r requirements-locked.txt

# 5. 确认无 critical/high 后提交
git add pyproject.toml uv.lock requirements-locked.txt
git commit -m "chore: bump <pkg> to <new_ver>"
```

---

## §3 Worker 禁止事项（C17 硬约束）

**Worker 内部（训练容器 / CI）只允许以下安装方式**：

```bash
# 允许：使用锁文件 + hash 校验
pip install -r requirements-locked.txt --require-hashes
# 或：
uv pip install -r requirements-locked.txt --require-hashes
# 或：
uv sync --frozen
```

**严格禁止**：

- `pip install <pkg>` — 未 pin 版本，跳过 hash 校验
- `pip install -r requirements.txt`（未加 `--require-hashes`）
- 修改 `pyproject.toml` / `uv.lock` / `requirements-locked.txt`
- `uv add` / `pip install --upgrade` / `pip install --pre`

> 违规行为将由 T015 pre-commit hook 拦截（git hook 检查 pyproject.toml 变更是否经过操作员审批）。

---

## §4 macOS 本地开发说明

**背景**（ops-decision 2026-04-24）：运行环境分两类：
- **本机开发（macOS arm64）** — 不装 bitsandbytes / CUDA-only 依赖，只跑 lm-eval 评估和 CLI 工具开发
- **训练执行（Linux x86_64 / CUDA 可用）** — 装全套依赖

`pyproject.toml` 中 `unsloth`、`bitsandbytes` 等训练依赖已加 `sys_platform == 'linux'` PEP 508 marker，macOS 下 uv 自动跳过这些包。

**推荐安装命令（macOS 开发机）**：

```bash
# 方式 A（推荐）：直接 sync，platform marker 自动跳过 linux-only 包
uv sync --frozen

# 方式 B（显式跳过，更保险，避免潜在依赖解析问题）：
uv sync --no-install-package bitsandbytes --no-install-package unsloth

# 方式 C（仅 dev 工具，不装任何训练相关包）：
uv sync --only-dev
```

**注意**：
- `uv sync --frozen` 在 macOS 现在可以成功（v0.1 起，因 PEP 508 marker 生效）
- 若遇到 `triton` 相关安装失败，使用方式 B 或方式 C
- macOS 上无法运行 Unsloth 训练（triton CUDA kernel 限制，非 bug）
- `requirements-locked.txt` 为 linux-targeted，不用于 macOS 安装

---

## §5 每月安全审计

每月 1 日操作员运行：

```bash
uv run pip-audit -r requirements-locked.txt
```

- 若出现 **critical/high** CVE → 立即启动升级流程（§2），合并前须清零
- 若出现 **medium** CVE → 本月内处理
- 若出现 **low** CVE → 记录到 `specs/003-pA/risks.md`，下次升级周期处理

---

## §6 版本选择依据（T002 锁定时的决策记录）

| 包 | Spec §8 参考版本 | 实际锁定版本 | 原因 |
|----|----------------|------------|------|
| transformers | 4.44.x | 4.51.3 | Unsloth 2026.3.18 要求 >=4.51.3 |
| peft | 0.11.x | 0.19.1 | Unsloth 要求 >=0.18.0,!=0.11.0；spec 版本不满足 |
| trl | 0.9.x | 0.18.2 | Unsloth 要求 >=0.18.2；spec 版本不满足 |
| datasets | 2.20.x | 3.6.0 | trl 0.18.2 要求 datasets>=3.0.0 |
| bitsandbytes | 0.44.x | 0.49.2 | 0.44.x 不存在于 PyPI；Unsloth 要求 >=0.45.5,!=0.46.0,!=0.48.0；0.49.2 同时有 linux+macOS wheel |

> Spec §8 版本表为"阶段参考"，注明"实际以 uv lock 为准"，T002 按实际 Unsloth 依赖约束调整。
