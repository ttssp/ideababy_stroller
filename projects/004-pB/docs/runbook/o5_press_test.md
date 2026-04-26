# O5 手动压测 Runbook

**结论**: ship 前 + 每次 release 必跑 `scripts/manual_press_test.py`,验证 PRD §S1 / §6 O5 硬门槛(单次决策录入 wall-clock < 30 秒,**全程含 draft 阶段 LLM**)。

## 度量口径(R3 守 PRD §S1 原口径)

- **起点**: GET `/decisions/new` 200 OK
- **终点**: POST `/decisions/{draft_id}/commit` 200 OK
- **判定**: 全程 wall-clock < 30s,**包含 draft 阶段 LLM 等待**(不豁免)
- **辅助记录**: draft 阶段 / commit 阶段分解 latency 仅供诊断,不参与 pass/fail

## 流程

### 1. 启动 server
```bash
cd projects/004-pB
uv run uvicorn decision_ledger.ui.app:_make_standalone_app --factory --host 127.0.0.1 --port 8000
```

### 2. 准备数据
- 关注股已录入(`/settings/watchlist`,30-50 个 ticker)
- 持仓快照已录入(`/settings/holdings`)
- advisor_report 已 ingest(放 PDF 到 `~/decision_ledger/inbox/` 或用 `/advisor/paste`)

### 3. 跑压测
```bash
cd projects/004-pB
python scripts/manual_press_test.py --presses 5
```

脚本会引导你 5 次依次:
1. 打开 `/decisions/new` 后按 Enter 开始计时
2. draft 提交完到 preview 后按 Enter 标记 draft 阶段结束
3. commit 提交跳 success 页后按 Enter 结束全程计时

### 4. 看结果
脚本写入 `release_log.jsonl`(append 模式),含:
- `git_sha`: 当前 commit
- `total_durations_ms`: 5 次全程 wall-clock(主度量)
- `draft_latencies_ms` / `commit_latencies_ms`: 阶段分解(诊断用)
- `pass`: `all(d < 30000 for d in total_durations)`

## 失败处理

任何一次全程 ≥ 30s 即 release block(PRD R1 硬门槛,OP-1 触发):

### 立即处置
1. **不 ship**(不打 release tag,不发 production)
2. 看 `draft_latencies_ms`:
   - 如果 draft > 5s → cache miss / LLM 慢 → 检查 ConflictCacheWarmer 是否在 advisor_parser 后正常 enqueue + 跑完
   - 如果 draft 突破 5s 上限 → 应该早就 503 了(R3 B-R2-2),如果没 503 是 bug
3. 看 `commit_latencies_ms`:
   - commit 应该 < 1s(无 LLM,§9.1 不变量)
   - 超过 → SQLite WAL 写入慢 / 表锁 / FK 约束查询慢

### 升级到 B-lite(R3 M2 + B-R2-4)
如反复 fail 且原因短期无法修复:
```bash
python scripts/toggle_b_lite.py engage
```
参考 `docs/runbooks/b_lite.md`。

> R3 修订:**v0.1 没有 UI toggle**(T022 R3 已删),仅 CLI + runbook 路径。
> Web UI banner 显示 alert 时也只引导 human 跑这个 CLI。

## 自动化版本(CI)

`tests/e2e/test_decision_input_timing.py` 在 CI 跑 Playwright headless 版,
阈值 < 25s(headless 比真浏览器快但 CI runner 慢,留余量)。手动压测仍以
< 30s 为 release 标准。

## R3 修订重点

- **PRD §S1 / §6 O5 原口径不变**:全程 wall-clock < 30s 含 draft LLM
- **删除 R2 "preview 200 OK 才计时" 字样**:任何 PR 想缩窄计时范围必拒
- **三 draft 场景**:cache 命中(≤ 1s)/ cache miss(≤ 5s)/ 超时(≥ 6s → 503)
- **503 路径**(R3 B-R2-2):draft 同步并发超 5s,abandon draft + 503,
  不放行 commit,不写 placeholder ConflictReport
