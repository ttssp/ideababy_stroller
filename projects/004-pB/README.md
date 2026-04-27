# 决策账本 (Decision Ledger)

ML PhD 自用投资决策档案系统 — calibration engine first。

> 单用户私用工具，不构成投顾产品。详见 [法律边界](docs/runbook.md#3-法律边界-compliance-42)。

---

## 安装

**前置要求**: Python 3.12、[uv](https://github.com/astral-sh/uv)

```bash
git clone <repo-url>
cd projects/004-pB

# 安装依赖
uv sync

# 配置环境变量
cp .env.example .env
# 编辑 .env，填写:
#   ANTHROPIC_API_KEY=sk-ant-...
#   TELEGRAM_BOT_TOKEN=123456:ABC...   (可选, 推送通知用)
#   TELEGRAM_CHAT_ID=987654321         (可选)

# 运行数据库迁移
uv run alembic upgrade head
```

---

## 启动

```bash
./scripts/start.sh
```

浏览器访问: `http://localhost:8000`

首次启动将自动跳转 `/onboarding` 引导页（约 15 分钟完成 7 步配置）。

---

## 日常使用

```bash
./scripts/start.sh         # 启动
# 浏览器访问 http://localhost:8000

# 决策录入 -> http://localhost:8000/decisions/new
# 设置关注股 -> http://localhost:8000/settings/watchlist
# 设置持仓 -> http://localhost:8000/settings/holdings
```

---

## 测试

```bash
# 单元测试 + 集成测试 (快速, <30s)
uv run pytest tests/ -m "not slow and not e2e" -v

# E2E 测试 (需要 Playwright chromium)
uv run playwright install chromium
uv run pytest tests/e2e/ -m "slow" -v --tb=short

# Lint + 类型检查
uv run ruff check src/
uv run mypy --strict src/decision_ledger/
```

---

## 文档

- [运维 Runbook](docs/runbook.md) — 启动 / 备份 / 故障处理 / 法律边界
- [O5 手动压测](docs/runbook/o5_press_test.md) — 性能验证
- 完整规格: `specs/004-pB/spec.md` (项目根 `../../specs/004-pB/`)

---

## 数据目录

```
~/decision_ledger/
  data.sqlite      # 主数据库
  inbox/           # PDF 监听目录 (拖入咨询师报告)
  llm_cache/       # LLM 响应缓存
  backups/         # 手动备份
  logs/            # 日志文件
```
