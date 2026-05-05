# 决策账本 — 运维 Runbook

> 版本: T021 · 更新: 2026-04-27
> 适用: single-operator (human) 日常运维

---

## 1. 启动

```bash
cd projects/004-pB
cp .env.example .env   # 首次: 填写 ANTHROPIC_API_KEY / TELEGRAM_BOT_TOKEN
uv sync                # 安装依赖 (首次或 pyproject.toml 更新后)
uv run alembic upgrade head  # 运行数据库迁移 (首次或新 migration 后)
./scripts/start.sh     # 启动服务 (绑定 127.0.0.1:8000)
```

浏览器访问: `http://localhost:8000`

首次启动 → 自动跳转 `/onboarding` 引导页 (约 15 分钟完成配置)

---

## 2. 备份

```bash
# SQLite 数据库备份 (建议每周手动执行)
cp ~/decision_ledger/data.sqlite ~/decision_ledger/backups/data_$(date +%Y%m%d).sqlite

# 完整数据目录备份
tar -czf ~/decision_ledger/backups/full_$(date +%Y%m%d).tar.gz ~/decision_ledger/
```

数据目录结构:
- `~/decision_ledger/data.sqlite` — 主数据库
- `~/decision_ledger/inbox/` — PDF 监听目录
- `~/decision_ledger/llm_cache/` — LLM 响应缓存 (可删重建)
- `~/decision_ledger/backups/` — 备份文件

---

## 3. 法律边界 (compliance §4.2)

1. 本系统**不是** robo-advisor / 投顾持牌产品
2. 本系统**不**自动下单，不持有任何 broker / 资金凭证
3. 本系统数据**仅本地**，不上传，不对外
4. 咨询师订阅内容仅供本人决策参考，不 redistribute
5. 若有任何**对外**使用需求（分享 / 商业化），**必须 fork 新 spec**，重审合规

---

## 4. 故障处理

### 4.1 服务无法启动

```bash
# 检查端口占用
lsof -i :8000

# 检查 .env 文件
cat .env | grep -v "^#" | grep -v "^$"

# 查看日志
uv run python -m decision_ledger.main 2>&1 | head -50
```

### 4.2 数据库迁移失败

```bash
# 查看当前迁移版本
uv run alembic current

# 重置到指定版本 (危险: 会丢数据)
uv run alembic downgrade base && uv run alembic upgrade head
```

### 4.3 LLM API 超时

系统内置 5s LLM 超时保护 (T008 DecisionRecorder)。超时返回 503。

解决方案:
1. 检查 `ANTHROPIC_API_KEY` 是否有效
2. 检查网络连接
3. 查看 `~/decision_ledger/llm_cache/` 是否有缓存命中

### 4.4 Telegram 推送失败

```bash
# 检查 bot token 格式 (应含 ':')
echo $TELEGRAM_BOT_TOKEN | grep -c ':'

# 测试 bot 连通性
curl "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe"
```

---

## 5. 性能压测参考

- **O5 手动压测**: `docs/runbook/o5_press_test.md`
  - 目标: 单次决策录入 wall-clock < 30s (含 LLM draft 阶段)
  - 执行: `uv run python scripts/manual_press_test.py`

- **O6 Onboarding 计时**: `tests/e2e/test_onboarding.py`
  - 目标: 7 步引导 < 900s (O6 pass 门槛)
  - 执行: `uv run pytest tests/e2e/test_onboarding.py -m slow`

---

## 6. B-lite 降级模式

B-lite 降级模式限制非核心功能，降低 LLM 调用频率。

操作方式参考 `docs/runbook/b_lite.md` (T022 CLI):

```bash
# 查看 B-lite 状态 (T022 交付后可用)
uv run python scripts/toggle_b_lite.py status

# 开启降级
uv run python scripts/toggle_b_lite.py enable

# 关闭降级
uv run python scripts/toggle_b_lite.py disable
```

---

## 7. 规格参考

- 完整规格: `specs/004-pB/spec.md`
- 架构图: `specs/004-pB/architecture.md`
- 合规文档: `specs/004-pB/compliance.md`
