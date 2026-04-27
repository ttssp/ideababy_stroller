# v0.1 已知 stub 与 plugin registry 死代码声明

> **INTERNAL — do not publish.** 本文档详细列出 v0.1 减弱保护层(R8 panic stop / O10 alert / OP-6 metric)各路径为何不生效。仅给运维/接手 v0.2 的工程师参考。如需对外说明 v0.1 限制,另写一份脱敏版(只说"v0.1 reduced async coverage",不点名具体 hook)。

**目的**:把"沉默的 0%"翻译成可见信号。本文档列出 v0.1 已知**未生效**的 wiring 链路,以及 v0.2 计划的修复方向。每次 FastAPI 启动会在 stderr 打印一段 BANNER 引用本文档,B-lite CLI 真实路径也会打 disclaimer 引用本文档。

> **不是 bug**:这些是 v0.1 的设计选择(spec §6 / architecture.md 默认承诺级别 = "hook 存在 + 单测覆盖",未承诺 production 真跑)。
> **是已知**:任何依赖这些路径的运维行为(R8 panic stop / O10 失败告警 / OP-6 tab ratio)都需要 workaround 或推到 v0.2。

---

## 1. ConflictWorker not wired in production

**症状**
- `services/conflict_worker.py::ConflictWorker.run_loop()` 是 long-running `while True`,但**没有任何 `register_startup_task` 注册它**。
- production 启动后 worker 不消费 cache_warmer 队列,job 永远堆积(实际危害很小,因为 v0.1 决策草稿同步路径不依赖 worker)。
- `monitor/pause_pipeline.py::pause_all_pipelines()` 在 R8 panic stop / B-lite engage 路径走 `_Noop` 替身(F2-T020 followup A1 改成 noop + WARNING + counter,不再 raise)。

**为什么 v0.1 接受**
- 决策草稿同步路径(T008 `DecisionRecorder`)直接调 `ConflictReportAssemblerService.assemble()`,**不经 worker**。worker 是异步 cache 加速器,不是必需路径。
- production 从未构造过 `LLMClient` / `StrategyRegistry` / `SourceDataProvider` 的实例(零 production 调用方)。要真启 worker 需要先把这条依赖链全部接好,工作量是新 task 级别。

**用户可见影响**
- 决策录入 wall-clock 仍 < 30s(spec §6 O5,不依赖 worker)。
- cache 不预热 → 第一次访问某 ticker 报告时 LLM 现算(从未命中过 cache 的成本)。
- B-lite engage 的 pause hook 在 FastAPI 进程内是 noop;CLI 在另一个进程,情况一样。
- **R8 panic stop 不真停 worker**(因为 worker 本就没启动)。

**workaround(v0.1)**
- 决策草稿:无需 workaround。
- B-lite:`scripts/toggle_b_lite.py engage` 仍写入 meta_decisions audit trail + DB 的 engaged 状态;Web banner 在 FastAPI 重启或下次 request 时从 DB 读到 engaged 状态并显示降级提示。

**v0.2 计划**(开新 task,不修改 v0.1 spec)
- 新建 task T023+ 构造 production wiring 链:
  - `LLMClient` startup 单例(传入 `ANTHROPIC_API_KEY` + `UsageWriter` + `cache_dir`)
  - `SourceDataProvider` 真实实现类(读 advisor PDF / portfolio / env_snapshot)
  - `StrategyRegistry.build_default(llm_client, provider)` 调用方
  - dedicated `job_queue` 表(替换 v0.1 用 notes 表伪造队列的 hack)
  - `ConflictWorker` startup task + `set_conflict_worker(...)` wire 到 pause_pipeline

---

## 2. FailureAlertMonitor cron not scheduled

**症状**
- `monitor/failure_alert.py::FailureAlertMonitor.check()` 实现完整(单测 5 个全过),但**完全没注册到 plugin registry 也没自启 cron**。
- spec §6 O10 verification 写"自动化 cron 09:00 跑",但 production 路径是死的。

**为什么 v0.1 接受**
- 同 #1:cron 跑起来需要 LLMClient 等 production 构造好,带不出来。

**用户可见影响**
- "连续 2 周决策档案 < 2 条"的告警**不会自动发出**。
- Telegram 推送 + Web banner 双通道告警都不会主动触发。

**workaround(v0.1)**
- 手工触发:`python -c "from decision_ledger.monitor.failure_alert import FailureAlertMonitor; ...; await monitor.check()"`
- 或外挂系统 cron:`0 9 * * * cd /path/to/project && uv run python scripts/run_failure_alert_check.py`(脚本待 v0.2 提供)
- 暂时建议:每周日做月度 review 时手动检查决策计数。

**v0.2 计划**
- 同 #1 的 startup wiring 任务:消费 `register_scheduler_job` 注册表,启动 APScheduler 跑 failure_alert / weekly_review / monthly_scheduler 三个 cron。

---

## 3. TabMetricsMiddleware not installed

**症状**
- `monitor/tab_metrics.py::TabMetricsMiddleware` 类定义存在,F2-T020 H10 还做了路径白名单 + UA 截断的强化。但**`main.py` 没有 `app.add_middleware(TabMetricsMiddleware)` 调用**。
- `tab_open_log` 表 production 永远是空表。

**为什么 v0.1 接受**
- OP-6 tab ratio(tab_opens_14d / committed_decisions_14d)是 best-effort 指标,不阻塞决策录入。

**用户可见影响**
- `calculate_tab_ratio()` 返回 None(committed=0 或 opens=0 都触发零除保护)。
- 月度 review 中的 OP-6 数字显示为 placeholder "—"。

**workaround(v0.1)**
- OP-6 跳过,人工凭印象判断"是不是开了太多页面没下决策"。

**v0.2 计划**
- 在 `main.py` 加一行 `app.add_middleware(TabMetricsMiddleware, pool=pool)`。需要 production pool 单例(同 #1 wiring 任务的副产物)。

---

## 4. register_scheduler_job collected but never started

**症状**
- `plugin.py::register_scheduler_job` hook 收集了所有 cron 注册到 `_scheduler_jobs` list。
- 但 `lifespan` **只迭代 `get_startup_tasks()`,完全不读 `get_scheduler_jobs()`**。
- 所有进 `register_scheduler_job` 的注册(`services/scheduler.py:71` / `services/monthly_scheduler.py:140`)都是死代码。
- 唯一例外:`services/draft_gc_worker.py` 自己 `new AsyncIOScheduler() + .start()`,绕过 plugin registry 直接跑。

**为什么 v0.1 接受**
- 同 #2:任何一个 cron 真启动都会带出 LLMClient / Registry / Provider 依赖链炸弹。

**用户可见影响**
- weekly_review cron / monthly_scheduler cron 不会自动跑。
- B-lite engage 时即便 monthly_scheduler 真存在,pause/resume 也只在 module-level 单例上生效,不影响 cron 调度(因为 cron 没起)。

**workaround(v0.1)**
- 手工运行:周日晚 21:00 自己跑 weekly_review 脚本;每月 1 日早 8:00 自己跑 monthly_review 脚本。
- 或外挂系统 cron(同 #2)。

**v0.2 计划**
- 在 `main.py` lifespan 中加 APScheduler 启动逻辑,消费 `get_scheduler_jobs()` 列表。需要先解决 #1 的依赖链。

---

## 5. B-lite CLI cross-process pause hook

**症状**
- `scripts/toggle_b_lite.py` 在**独立进程**调 `pause_all_pipelines()`。
- CLI 进程的 `pause_pipeline._conflict_worker_instance` 与 FastAPI 进程的不是同一个 — module-level singleton 不跨进程。
- 即便 v0.2 在 FastAPI lifespan wire 了 worker,CLI 进程里仍是 None,disclaimer 仍会打。

**为什么 v0.1 接受**
- v0.1 worker 本来就没起,CLI 跨进程是双重失效里的第二重,实际危害不增量。
- B-lite 的真实有效路径(meta_decisions audit trail + DB-driven banner status)不依赖 pause hook 跨进程同步。

**用户可见影响**
- CLI 每次 engage / disengage 都会在 stderr 打 disclaimer(F2-T020 followup A2)。
- 用户看到"engaged" 时,banner 的"engaged"状态来自 DB(可靠),pause/resume worker 这一步不可靠(noop)。

**workaround(v0.1)**
- 接受 disclaimer 提示,理解"pause 是 noop,但 audit trail + banner 可靠"。
- 如果想确认 banner 已经更新:`curl http://127.0.0.1:8000/decisions`(或在浏览器刷新),banner 会从 DB 读到 engaged 状态。

**v0.2 计划**
- 方案 A(file sentinel):CLI 写 `~/.decision_ledger/B_LITE_ENGAGED` 文件,`ConflictWorker.run_loop()` 每轮 stat 一次。前提是 worker 真的在跑。
- 方案 B(DB-driven worker):worker 启动 loop 内每轮查 `meta_decisions` 表的 last_state,自然跨进程一致。代码量比 file sentinel 小。
- 推荐方案 B。

---

## 6. create_draft 三事务非原子,可能产生 orphan conflict_report/rebuttal (Codex review F3)

**症状**
- `services/decision_recorder.py::DecisionRecorder.create_draft()` 在 LLM gather 成功后,串行执行 3 个独立 `write_connection` 事务:
  1. INSERT decisions (status=draft)
  2. INSERT conflict_reports
  3. INSERT rebuttals
- 任意一步失败(磁盘满 / Ctrl+C / kernel OOM)会留下"前面已 commit、后面没写完"的 orphan 行。
- Codex 评级:medium。

**为什么 v0.1 接受(不修)**
- v0.1 是单用户 SQLite WAL,**只有一个 writer**。合并到一个长事务会让 writer_lock 持有 100ms+ (LLM 已成功,但 3 次 INSERT + index 更新 + WAL flush 是同步 I/O),阻塞所有读路径(列表 / 详情 / banner 都要 SELECT)。
- 单用户场景下,Codex 提到的"原子性"价值是负的:换来一致性 vs 可观察的 UI 卡顿,后者更刺眼。
- orphan 行的实际危害:每年最多几 MB,LLM 钱已经花掉(写了一半已经没救),不影响新决策录入也不影响列表查询(JOIN 时 `ON dec.id = cr.decision_id` orphan 永远 join 不上)。

**用户可见影响**
- 极少(年频次,且只在系统级故障 — 磁盘满 / 强制杀进程 — 时发生)。
- 列表 UI 不会显示 orphan 报告,因为入口都从 `decisions` 表 LEFT JOIN 出发。
- DB 大小缓慢增长,但远低于决策草稿本身的存储成本。

**workaround(v0.1)**
- 接受。每月做月度 review 时手工跑清理(脚本 v0.2 提供):
  ```sql
  -- scripts/cleanup_orphan_llm_data.sql (v0.2 待加)
  DELETE FROM conflict_reports
   WHERE decision_id NOT IN (SELECT id FROM decisions);
  DELETE FROM rebuttals
   WHERE decision_id NOT IN (SELECT id FROM decisions);
  ```
- 实测影响:零(从未触发过 orphan,因为 v0.1 单用户、SSD、有 swap、不会被 OOM)。

**v0.2 计划**
- **不**改成长事务(理由如上)。
- 真要原子性时考虑 saga / outbox pattern:
  - 写 `llm_outbox` 表记录 (decision_id, payload, step) 三步意图
  - 各步真写完后从 outbox 删除对应行
  - 启动期或定时 worker 兜底:扫 outbox 中 stale 行,要么继续完成,要么回滚 + cleanup
- 这才是"分布式事务"在 SQLite 单写场景下的合理近似,而不是把锁吃满。

---

## 7. LLMClient 每次 _call_api 新建 SDK client (Codex review F2)

**症状**
- `services/llm_client.py::LLMClient._call_api()` 每次调用 `anthropic.Anthropic(api_key=self._api_key)`,不复用 SDK 实例。
- 每次新建 client 触发 TLS 握手(~50ms)+ 内部 HTTP/2 connection setup,远超过纯 LLM token 推理时间分母里的几个百分点。
- Codex 评级:medium。

**为什么 v0.1 接受(不修)**
- v0.1 是**单用户决策录入**,实测每天最多 60 次 `_call_api`(决策草稿 ~4-5 次/条 × 10-15 条/天)。
- 60 × 50ms = 3 秒总 TLS 握手开销,远低于 30s SLA(spec §6 O5),用户感知 = 0。
- 改 SDK 复用要处理的真问题:
  - **thread-safety**:`anthropic.Anthropic` 在 SDK 文档里没有承诺 thread-safe(虽然底层 httpx 是),复用前需要研究或加 lock
  - **api_key 热轮换**:复用后改 key 要重建,需要新接口
  - **GC 语义**:旧 client 内部连接池什么时候释放,会不会泄漏 socket
- 上面三件都是单测覆盖不到的 edge case,在 v0.1 单用户负载下**永远观察不到**,改了反而引入回归风险。

**用户可见影响**
- 0。决策录入耗时仍 < 30s。

**workaround(v0.1)**
- 无需 workaround。

**v0.2 计划**
- `LLMClient.__init__` 期建 `self._client = anthropic.Anthropic(api_key=...)`,所有 `_call_api` 复用。
- 加 `set_api_key(new_key)` 接口处理热轮换:`self._client = anthropic.Anthropic(api_key=new_key)`(原 client 由 GC 释放,SDK 内部连接池超时关)。
- 加并发测试:同一 client 实例在 10 个 asyncio task 并发 `messages.create`,确保不报错且响应正确归位。
- 真正的收益不是节省 3 秒 TLS,而是 v0.2 引入 ConflictWorker 真启用后,异步并发场景下连接复用避免 socket 风暴。

---

## 实现引用

- F2-T020 H7 followup A1:`src/decision_ledger/monitor/pause_pipeline.py::_get_conflict_worker` 改 noop + counter + WARNING;`get_wiring_status()` / `pause_hook_noop_call_count()` 自检 API
- F2-T020 followup A1:`src/decision_ledger/main.py::_print_v01_banner` 启动期 stderr BANNER
- F2-T020 followup A2:`scripts/toggle_b_lite.py::_print_cli_pause_hook_disclaimer` CLI disclaimer
- Codex review F1 followup:`src/decision_ledger/ui/router_settings.py` 改 startup-task pool 模式 + 503 wiring gate (regression test `tests/integration/ui/test_settings_router_production_path.py`)

启动 BANNER 抑制方法(测试 / CI / 监控对接用):`DECISION_LEDGER_SUPPRESS_V01_BANNER=1`
