# B-lite 降级路径 Runbook

## 概述

B-lite 是一条紧急降级路径（T022），用于在系统运行异常时暂停资源密集型流程，同时保留核心交易档案写入与每周 review 功能。

## 何时触发

- O10 告警：连续 2 周 committed 决策数 < 2
- ConflictWorker 持续报错 / LLM 超时严重
- MonthlyScheduler 占用过多资源
- 任何需要紧急降负载的场景

**B-lite engage 后保留：**
- decisions 表写入（T008 DecisionRecorder 正常）
- 每周 review（T014 WeeklyReviewService 正常）

**B-lite engage 后暂停：**
- ConflictWorker（T010 冲突报告 cache warmer 停止消费）
- MonthlyScheduler（T015 月度 review 停止）

## CLI 操作

```bash
# 1. 触发降级（必须填写原因）
python scripts/toggle_b_lite.py engage --reason="连续 2 周决策 < 2，触发 O10 告警"

# 2. 查看当前状态
python scripts/toggle_b_lite.py status

# 3. 解除降级（14 天 cooling-off 后才可执行）
python scripts/toggle_b_lite.py disengage
```

## 14 天 cooling-off 约束

engage 后 **必须等待 14 天** 才能 disengage。提前调用 disengage 会收到错误：

```
[B-lite] ERROR: cooling-off 期内不可 disengage，剩余 N 天
```

这是硬约束，不可跳过。目的是防止频繁切换破坏系统稳定性。

## 数据保留

- 所有操作写入 `meta_decisions` 表（SQLite）
- 记录字段：meta_id / decision_type / reason / created_at / cooling_off_until
- 表由 BLiteService 自动创建（不依赖 alembic）
- 数据永久保留，作为审计档案

## 恢复流程

1. 等待 14 天 cooling-off 到期
2. 确认系统恢复正常（决策频率、LLM 响应时间）
3. 执行 `python scripts/toggle_b_lite.py disengage`
4. 确认 ConflictWorker 和 MonthlyScheduler 已恢复（查日志）

## 环境变量

| 变量 | 说明 |
|------|------|
| `DECISION_LEDGER_DB_URL` | SQLite DB 路径（`sqlite:///path/to/db`） |
| `DECISION_LEDGER_B_LITE_SKIP_PAUSE` | 测试逃逸（`1` = 跳过真实 pause hook，仅限 CI）|
