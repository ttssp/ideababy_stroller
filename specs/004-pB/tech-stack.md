# Tech Stack — 004-pB · 决策账本

**Version**: 0.1
**Created**: 2026-04-25T15:10:00+08:00
**Companion**: `spec.md` D11/D12 / `architecture.md` §3.5 / §4.3

> 全部版本号 **pinned** (无 `^` `~`)。私用 localhost, 选稳定不选最新。

---

## 1. Primary stack

| 层 | 选型 | 版本 (pinned) | 理由 |
|----|------|---------------|------|
| **主语言** | Python | 3.12.7 | LLM SDK 生态成熟 (anthropic / openai 都首选 Python); pandas 做档案聚合; type hint 进入主流; ML PhD 家底语言, ramp 0 |
| **包管理 / 虚拟环境** | uv | 0.5.11 | CLAUDE.md 指定; 比 pip/poetry 快 10x; lockfile 稳定; 单二进制 |
| **Web 框架** | FastAPI | 0.115.5 | 异步原生, type-hint-first, 单文件起步, OpenAPI 自动生成; 比 Flask 更适配 asyncio LLM 调用 |
| **ASGI 服务器** | uvicorn (standard) | 0.32.1 | FastAPI 标配; localhost 单 worker 足够 |
| **HTML 模板** | Jinja2 | 3.1.4 | server-rendered; PRD §UX 5 秒看完原则不需 SPA |
| **前端交互** | HTMX | 2.0.4 | 无打包, 无 build step, 直接 server push partial HTML; ML PhD 友好 (无需学 React); 第一屏快 |
| **CSS** | Pico CSS | 2.0.6 | classless, 极简, 5KB; 不引入 Tailwind 编译链 |
| **数据库** | SQLite | 3.46.x (system) | 单文件无运维; WAL mode 支持 task 并发; 单用户性能远超需求 |
| **DB 驱动** | sqlite3 (stdlib) + aiosqlite | aiosqlite 0.20.0 | 异步访问; 不引入 SQLAlchemy ORM (轻量优先) |
| **Migration** | alembic | 1.14.0 | schema drift 防御; 即使单用户也防自己改坏; 单独脚本运行 |
| **PDF 解析** | pdfplumber | 0.11.4 | 中文 PDF 文本提取稳定; 比 PyPDF2 强 |
| **LLM SDK** | anthropic | 0.42.0 | Claude API 官方; structured output 支持 |
| **Telegram bot** | python-telegram-bot | 21.9 | 官方推荐 PTB v21, async-native; long-polling 模式简单 |
| **Watched folder** | watchdog | 6.0.0 | 跨平台文件监听; macOS/Linux 都能跑 |
| **任务调度** | apscheduler | 3.11.0 | weekly review cron + alert daily; in-process; 不引入 celery |
| **数据校验** | pydantic | 2.10.4 | FastAPI 标配; dataclass 替代品 |
| **Async utility** | anyio | 4.6.2 | FastAPI 已依赖; task group 模式 |
| **测试框架** | pytest | 8.3.4 | 标配 |
| **Async 测试** | pytest-asyncio | 0.24.0 | async test 支持 |
| **E2E 测试** | playwright | 1.49.0 | O5 timing test (Python binding); 比 selenium 快 |
| **HTTP mock** | respx | 0.21.1 | mock httpx (FastAPI test client) |
| **Fixture / factory** | factory-boy | 3.3.1 | 决策档案 / advisor_report fixture |
| **Linter / Formatter** | ruff | 0.8.4 | CLAUDE.md 指定; 同时 lint + format; 替代 black/flake8/isort |
| **类型检查** | mypy | 1.13.0 | strict mode; 拦截大部分 contract 违反 |
| **CI** | GitHub Actions | (latest) | 私 repo 也用; PR 跑 ruff + mypy + pytest |

---

## 2. 排除的替代品 (Excluded alternatives)

| 替代品 | 排除理由 |
|--------|---------|
| **TypeScript / Node.js / Next.js** | LLM SDK 在 Python 生态更厚; pandas 档案聚合是天然优势; ML PhD 语言路径; 二选一无需双栈 |
| **Streamlit** | 适合 dashboard 但**录入 UX 不可控** (输入响应延迟); 不能保证 < 30s 录入硬门槛; 部署反而比 FastAPI+HTMX 重 |
| **Flask** | 同步框架, 异步 LLM 调用要 patch; FastAPI 原生异步更顺 |
| **Django** | 全栈框架, 自带 admin/ORM 但**重**, 单用户 localhost 不需要; 6 周交付时间不奢侈 |
| **PostgreSQL / MySQL** | 单用户无并发压力, SQLite 已足; 增加 daemon 运维违反 C13 (≤ 3h/周维护) |
| **DuckDB** | OLAP-first 列存, 我们是 OLTP read/write; SQLite 更稳熟 |
| **MongoDB / NoSQL** | 决策档案 + advisor_report + notes 三个域有 FK + JOIN 需求; SQL 顺手 |
| **SQLAlchemy ORM** | 轻量优先; raw SQL + dataclass + Repository pattern 已经足; ORM 增加学习面 |
| **Celery / RQ + Redis** | 多进程 worker 队列; 单用户单进程 asyncio 足够; Redis 是额外 daemon → 维护负担 |
| **React / Vue / Svelte** | SPA 引入 build step + 状态管理; HTMX 在 server-rendered 场景更轻; "5 秒看完"原则不需 SPA |
| **Tailwind CSS** | 编译链 + class 噪音; Pico CSS classless 更适合极简 server HTML |
| **OpenAI / Gemini API** | Anthropic Sonnet 在中文金融 PDF 解析 + structured output 经验更稳; 单一供应商减少 SDK 杂项; Anthropic 已有合作经验 |
| **本地 LLM (Ollama / llama.cpp)** | 中文质量差 + 设备 RAM 要求 + 量化 / GPU driver 维护负担, 违反 C13 |
| **Selenium** | E2E 用 Playwright 更快, async 友好 |
| **Black + isort + flake8 三件套** | ruff 单一工具替代, 速度 + 配置都简洁 |
| **Poetry / pip-tools** | uv 已替代; CLAUDE.md 指定 |
| **Docker / Docker Compose** | localhost 单进程 Python, 无需容器化; 增加冷启动/挂载 path 调试 |
| **nginx / Caddy reverse proxy** | localhost 不需要 reverse proxy |
| **OAuth / JWT / session 库** | D5 单用户无 auth; localhost binding 127.0.0.1 即足 |
| **TimescaleDB / InfluxDB** | 时序数据库; 我们的 timestamp 字段稀疏, SQLite index 已足 |

---

## 3. 依赖策略

### 3.1 版本钉死
- 所有生产依赖 (`[project.dependencies]`) **不带 `^` 或 `~`**, 钉到 patch
- 例: `fastapi==0.115.5`, 不写 `fastapi>=0.115`
- 升级走单独 PR, 跑全 test suite

### 3.2 漏洞审计
- 每次 `uv add <pkg>` 后跑 `uv run pip-audit` (or `safety check`)
- 0 critical / high 漏洞才 commit
- v0.1 ship 前再扫一次

### 3.3 依赖数量预算
- 生产依赖 ≤ **20** 个 (pyproject.toml `[project.dependencies]`)
- dev 依赖 ≤ **15** 个 (pytest / mypy / playwright / etc.)
- 超预算 → 评估是否真需要, 不行就自己写

### 3.4 lockfile
- `uv.lock` 必 commit
- 跨机器 / CI 走 `uv sync --frozen`

### 3.5 Python 版本
- 钉到 3.12.7 (pyproject.toml `requires-python = "==3.12.7"`)
- 不允许 3.13 (新, ecosystem 兼容性未稳)
- 不允许 < 3.12 (PEP 695 type alias / StrEnum / asyncio.TaskGroup 都已用)

---

## 4. .python-version + uv 工作流

```bash
# 项目根
echo "3.12.7" > .python-version
uv venv  # 创建 .venv
uv sync  # 装依赖, 生成 uv.lock
uv run pytest  # 跑测试
uv run ruff check .  # lint
uv run mypy src/  # 类型检查
```

---

## 5. 项目目录结构 (建议, 非强制)

```
decision_ledger/
├── pyproject.toml       # uv 配置 + 依赖
├── uv.lock              # 依赖锁
├── .python-version      # 3.12.7
├── .env.example         # 模板, 真 .env gitignored
├── .gitignore           # 屏蔽 db.sqlite / inbox/ / llm_cache/ / .env
├── alembic.ini
├── alembic/
│   └── versions/
├── src/
│   └── decision_ledger/
│       ├── __init__.py
│       ├── main.py            # entry: FastAPI + Telegram + watcher 启动
│       ├── config.py          # 加载 .env (anthropic key, tg token)
│       ├── domain/            # Decision / EnvSnapshot / etc.
│       ├── strategy/          # StrategyModule + 三占位实现
│       ├── pipeline/          # AdvisorParser + WatchedFolderWatcher
│       ├── ui/                # FastAPI routes + Jinja2 templates
│       ├── telegram/          # bot handlers
│       ├── repository/        # SQLite repository
│       ├── llm/               # LLMClient + cache
│       └── monitor/           # AlertMonitor (O10) + cron jobs
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── scripts/
│   ├── start.sh
│   ├── proxyman_fetch.sh      # 占位; human 自定义
│   └── manual_press_test.py   # O5 双条件之一
└── docs/
    ├── runbook.md             # human 自用使用手册
    └── prompts/               # LLM prompt 模板版本化
```

---

## 6. 兼容性 / 平台

- **OS 支持**: macOS (主, human 设备) + Linux (备); Windows 不刻意支持 (watched folder 路径差异大)
- **Python**: 3.12.7
- **SQLite**: 用系统自带 (macOS 自带 ≥ 3.46), 实际 schema 兼容 ≥ 3.40
- **浏览器**: Chrome / Safari (HTMX 支持任何 modern browser, 无要求)
- **Telegram**: 全球 API; localhost long-polling 不需要公网 IP

---

## 7. 性能 (与 SLA.md 对应)

- **Web UI 第一屏 < 5s** (PRD §UX 4): 无 SPA, server-rendered, 网络成本 0 (localhost), 实测 ~50ms
- **决策录入提交 < 500ms**: SQLite local INSERT ~1ms, FastAPI overhead ~10ms, ample headroom
- **LLM 调用异步 5-30s 可接受**: conflict_resolve 平均 ~10s (Sonnet), 不阻塞 UI
- **PDF 解析 ~3-15s**: pdfplumber + LLM 一次结构化, 后台 worker

---

## 8. 关键风险 (与 risks.md 对应, tech 视角)

| 风险 | tech 选择对它的影响 |
|------|-------------------|
| TECH-1 (SQLite 并发) | WAL mode + aiosqlite 已缓解; 单用户写并发极低 |
| TECH-2 (LLM 成本) | 文件 cache + token 监控 + 单一供应商 (Anthropic Sonnet) |
| TECH-3 (PDF 多样) | pdfplumber 失败入 `parse_failures`, human 可手动结构化 |
| TECH-4 (StrategyModule 过/欠设计) | IDL 已锁; 不允许后续合并模块 (R9 红线) |
| OP-2 (开发超时) | 选最熟语言 (Python) + 最熟工具 (FastAPI / pytest); 不引入实验性技术 |

---

## 9. 待 task-decomposer 决定的 tech 细节

- pyproject.toml 完整 dep list (本文档给方向, 具体 commit 由 T001 拆解)
- alembic migration 文件结构 (T002 域)
- LLM prompt 模板版本号管理 (folder vs DB)
- HTMX template 复用结构 (Jinja2 macros)
