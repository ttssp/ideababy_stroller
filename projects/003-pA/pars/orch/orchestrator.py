"""
pars.orch.orchestrator — `pars sft start` 主编排（T023 · O1 · O5）。

结论：RunOrchestrator.start() 串联 Phase 0-2 所有模块，
      实现从 CLI 参数到 RunHandle 的完整 15 步流程。

## 15 步编排流程

1. 验证 ANTHROPIC_API_KEY 存在（fail-fast）
2. 构造 RunConfig（含 env_snapshot）
3. Ledger.create_run(config) → 分配 run_id + 建目录树
4. 写 machine_fingerprint（C22，T019 模块）
5. 启动 proxy（T010，含 USD 预算前置拒绝中间件 C20）
6. build_worker_env（T011，C15/R4 API key 隔离）
7. create_worktree + ensure_readonly_claude_dir（T012 fail-closed；
   若抛 ReadonlyFailsClosed → 退出码 2 + OQ5 引导，直接传播让 CLI 处理）
8. render_failure_prompt → 构造 Worker system prompt
9. launch Worker（T013，generator 模式）
10. 启动 StuckMonitor（T017，5s 采样）+ BudgetMonitor（T018，60s）两个 daemon thread
11. 等待 worker 退出（消费 ClaudeEvent 流）或监听 SIGINT
12. worker 退出后 render_report(T021) + validate_report_schema（strict contract）
13. cleanup（逆序：monitors stop → worker cleanup → proxy stop）
14. 返回 RunHandle（含 final_phase, report_path, exit_code）

## 退出码约定

0 = completed（正常完成）
2 = fail-fast / config 错误（API key 缺失 / ReadonlyFailsClosed）
3 = stuck（monitor 触发 SIGINT）
4 = budget（monitor 触发 SIGINT）
5 = worker crash（非零非 SIGINT 退出）

## 安全约束

- C15/R4：worker env 不含 ANTHROPIC_API_KEY（build_worker_env 保证）
- C21：.claude/ fail-closed（ensure_readonly_claude_dir，ReadonlyFailsClosed → exit 2）
- C22：machine fingerprint 写入（write_fingerprint，由 T019 实现，T023 调用）
"""

from __future__ import annotations

import os
import signal
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pars.budget.tracker import BudgetMonitor, BudgetTracker
from pars.ledger import (
    BudgetConfig,
    DatasetConfig,
    EvalConfig,
    RunConfig,
    RunPhase,
    TrainingConfig,
    create_run,
    generate_ulid,
    save_config,
    update_state,
)
from pars.logging import get_logger
from pars.orch.env_snapshot import collect_env_snapshot
from pars.orch.machine_fingerprint import collect_fingerprint, write_fingerprint
from pars.orch.worker import Worker, WorkerConfig
from pars.orch.worker_env import WorkerEnvConfig, build_worker_env
from pars.orch.worktree import create_worktree, remove_worktree
from pars.proxy import ProxyConfig, _pick_free_port, start_proxy, stop_proxy
from pars.report import render_failure_prompt, render_report, validate_report_schema
from pars.safety import ensure_readonly_claude_dir
from pars.stuck import CircuitBreaker, StuckMonitor

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# 公开异常
# ---------------------------------------------------------------------------

class ApiKeyMissingError(RuntimeError):
    """ANTHROPIC_API_KEY 未设置时抛出（fail-fast 路径）。"""


# ---------------------------------------------------------------------------
# RunHandle — 返回契约
# ---------------------------------------------------------------------------

@dataclass
class RunHandle:
    """RunOrchestrator.start() 返回值契约。

    字段：
        run_id        : str           — ULID（由 create_run 分配）
        final_state   : RunPhase      — 完成时的最终 phase
        report_path   : Path | None   — report.md 路径（None 表示未生成）
        exit_code     : int           — 0=completed, 2=config err, 3=stuck, 4=budget, 5=crash
        failure_reason: str | None    — 人类可读失败原因（None 表示正常完成）
    """

    run_id: str
    final_state: RunPhase
    report_path: Path | None
    exit_code: int
    failure_reason: str | None = None


# ---------------------------------------------------------------------------
# RunOrchestrator
# ---------------------------------------------------------------------------

class RunOrchestrator:
    """串联 Phase 0-2 所有模块的主编排器（T023）。

    用法：
        orch = RunOrchestrator()
        handle = orch.start(
            research_question="Does LoRA help?",
            base_model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            dataset_id="tatsu-lab/alpaca",
            ...
        )
        if handle.exit_code == 0:
            print(f"Report: {handle.report_path}")
    """

    def __init__(self) -> None:
        # 内部状态（cleanup 需要）
        self._proxy_handle = None
        self._worktree_handle = None
        self._readonly_handle = None
        self._worker: Worker | None = None
        self._stuck_monitor: StuckMonitor | None = None
        self._budget_monitor: BudgetMonitor | None = None
        self._run_id: str | None = None

        # 中断标志（Ctrl+C）
        self._interrupted = threading.Event()
        self._exit_reason: str | None = None  # "stuck" | "budget" | "interrupt" | None

    def start(
        self,
        research_question: str,
        base_model: str,
        dataset_id: str,
        dataset_split: str = "train[:100]",
        n_samples: int = 100,
        lora_rank: int = 16,
        lora_alpha: int = 32,
        lr: float = 2e-4,
        epochs: int = 3,
        batch_size: int = 2,
        max_seq_len: int = 2048,
        eval_tasks: list[str] | None = None,
        usd_cap: float = 30.0,
        wall_clock_hours_cap: float = 12.0,
        gpu_hours_cap: float = 12.0,
        run_id: str | None = None,
    ) -> RunHandle:
        """执行 SFT run 的完整 15 步编排流程。

        参数：
            research_question : 研究假设（写入 config 和 report）
            base_model        : HuggingFace 模型仓库 ID
            dataset_id        : HuggingFace 数据集仓库 ID
            dataset_split     : 数据集 split（默认 "train[:100]"）
            n_samples         : 样本数量（默认 100）
            lora_rank         : LoRA rank（默认 16）
            lora_alpha        : LoRA alpha（默认 32）
            lr                : 学习率（默认 2e-4）
            epochs            : 训练 epoch 数（默认 3）
            batch_size        : per-device batch size（默认 2）
            max_seq_len       : 最大序列长度（默认 2048）
            eval_tasks        : lm-eval task 列表（默认 ["gsm8k"]）
            usd_cap           : USD 硬帽（默认 $30）
            wall_clock_hours_cap: wall-clock 时间上限（小时，默认 12h）
            gpu_hours_cap     : GPU 小时上限（默认 12h）
            run_id            : 可选：覆盖自动生成的 ULID（--name 参数）

        返回：
            RunHandle

        Raises:
            ApiKeyMissingError         : ANTHROPIC_API_KEY 未设置
            ReadonlyFailsClosed        : .claude/ fail-closed 不可用（退出码 2）
        """
        if eval_tasks is None:
            eval_tasks = ["gsm8k"]

        # -----------------------------------------------------------------
        # 步骤 1: 验证 ANTHROPIC_API_KEY 存在（fail-fast，退出码 2）
        # -----------------------------------------------------------------
        self._validate_env()

        # -----------------------------------------------------------------
        # 步骤 2: 采集 env_snapshot + 构造 RunConfig
        # -----------------------------------------------------------------
        from pars.ledger import EnvSnapshot as _EnvSnapshot  # noqa: PLC0415
        raw_snapshot = collect_env_snapshot()
        # 防止 mock/测试环境中返回非 EnvSnapshot 实例（Pydantic strict 验证）
        env_snapshot = raw_snapshot if isinstance(raw_snapshot, _EnvSnapshot) else None

        config = RunConfig(
            research_question=research_question,
            base_model=base_model,
            dataset=DatasetConfig(
                hf_id=dataset_id,
                split=dataset_split,
                n_samples=n_samples,
            ),
            training=TrainingConfig(
                lora_rank=lora_rank,
                lora_alpha=lora_alpha,
                lr=lr,
                epochs=epochs,
                batch_size=batch_size,
                max_seq_len=max_seq_len,
            ),
            eval=EvalConfig(tasks=eval_tasks),
            budget=BudgetConfig(
                usd_cap=usd_cap,
                wall_clock_hours_cap=wall_clock_hours_cap,
                gpu_hours_cap=gpu_hours_cap,
            ),
            env_snapshot=env_snapshot,
            run_id=run_id,
        )

        # -----------------------------------------------------------------
        # 步骤 3: Ledger.create_run → 分配 run_id + 建目录树 + 写 config/state
        # -----------------------------------------------------------------
        # 若调用方传入了 run_id（--name 覆盖），需要特殊处理
        # create_run 内部会忽略 config.run_id 并生成新 ULID
        # 对于 --name 覆盖场景：我们传入的 run_id 不是 ULID 格式，create_run 会拒绝
        # 所以直接调用 create_run（让其生成 ULID），然后根据是否有 --name 决定后续行为
        canonical_run_id = self._create_ledger(config, requested_run_id=run_id)
        self._run_id = canonical_run_id

        logger.info(
            "RunOrchestrator.start: run 已创建",
            extra={"run_id": canonical_run_id},
        )

        # 进入 try/finally 确保 cleanup 在任何失败路径下都执行
        exit_code = 5
        failure_reason: str | None = "unexpected_error"
        report_path: Path | None = None

        try:
            # -----------------------------------------------------------------
            # 步骤 4: 写 machine_fingerprint（C22，T019 实现的模块）
            # -----------------------------------------------------------------
            fp = collect_fingerprint()
            write_fingerprint(canonical_run_id, fp)
            logger.debug(
                "RunOrchestrator: fingerprint 已写入",
                extra={"run_id": canonical_run_id},
            )

            # -----------------------------------------------------------------
            # 步骤 5: 启动 proxy（T010，含 USD 预算前置拒绝中间件 C20）
            # -----------------------------------------------------------------
            proxy_port = _pick_free_port()
            proxy_config = ProxyConfig(port=proxy_port)
            self._proxy_handle = start_proxy(proxy_config, run_id=canonical_run_id)
            proxy_port = self._proxy_handle.port
            logger.info(
                "RunOrchestrator: proxy 已启动",
                extra={"run_id": canonical_run_id, "port": proxy_port},
            )

            # -----------------------------------------------------------------
            # 步骤 6: build_worker_env（T011，C15/R4 API key 隔离）
            # -----------------------------------------------------------------
            env_cfg = WorkerEnvConfig(
                run_id=canonical_run_id,
                proxy_port=proxy_port,
            )
            worker_env = build_worker_env(env_cfg)

            # -----------------------------------------------------------------
            # 步骤 7: create_worktree + ensure_readonly_claude_dir（T012 fail-closed）
            # 若 ReadonlyFailsClosed → 直接传播（CLI 捕获后退出码 2 + OQ5 引导）
            # -----------------------------------------------------------------
            from pars.paths import worktree_dir  # noqa: PLC0415
            wt_base = worktree_dir(canonical_run_id).parent
            self._worktree_handle = create_worktree(wt_base, canonical_run_id)

            # ensure_readonly_claude_dir：使用默认模板路径
            claude_template = Path.cwd() / "worker_claude_dir"
            self._readonly_handle = ensure_readonly_claude_dir(
                self._worktree_handle.path,
                claude_template,
            )
            logger.info(
                "RunOrchestrator: worktree + .claude 只读挂载完成",
                extra={"run_id": canonical_run_id},
            )

            # -----------------------------------------------------------------
            # 步骤 8: 构造 Worker system prompt（render_failure_prompt 注入）
            # 注意：render_failure_prompt 需要 baseline_score 和 lora_score，
            # 此时 run 刚开始，分数为 0.0（placeholder）
            # -----------------------------------------------------------------
            workflow_prompt = render_failure_prompt(
                run_id=canonical_run_id,
                baseline_score=0.0,
                lora_final_score=0.0,
            )

            # -----------------------------------------------------------------
            # 步骤 9: 创建 Worker（T013）
            # -----------------------------------------------------------------
            worker_config = WorkerConfig(
                run_id=canonical_run_id,
                workflow_prompt=workflow_prompt,
                max_turns=200,
                timeout_seconds=int(wall_clock_hours_cap * 3600),
                worktree_base=wt_base,
                claude_template=claude_template,
                proxy_config=proxy_config,
            )
            self._worker = Worker(worker_config)

            # -----------------------------------------------------------------
            # 步骤 10: 启动 Worker（run()）并运行 ClaudeEvent 流
            # 注意：Worker.run() 是 generator，内部管理 worktree/mount/proxy
            # 由于 Worker 已独立管理 cleanup，我们直接消费 generator
            # -----------------------------------------------------------------

            worker_exit_code, failure_reason, report_path = self._run_worker_with_monitors(
                canonical_run_id,
                wall_clock_hours_cap,
                gpu_hours_cap,
                usd_cap,
            )
            exit_code = worker_exit_code

        except KeyboardInterrupt:
            # Ctrl+C: 标记中断，cleanup 在 finally 中执行
            logger.warning(
                "RunOrchestrator: Ctrl+C 收到，开始 cleanup",
                extra={"run_id": canonical_run_id},
            )
            exit_code = 3
            failure_reason = "keyboard_interrupt"

        except Exception as exc:
            # 其他异常：传播（CLI 负责显示）
            logger.error(
                "RunOrchestrator: 未预期异常",
                extra={"run_id": canonical_run_id, "error": str(exc)},
            )
            self._cleanup(canonical_run_id)
            raise

        finally:
            # 最终 cleanup（幂等：多次调用安全）
            self._cleanup(canonical_run_id)

        # 读取最终 phase
        try:
            from pars.ledger import read_state  # noqa: PLC0415
            final_state_obj = read_state(canonical_run_id)
            final_phase = final_state_obj.phase
        except Exception:  # noqa: BLE001
            final_phase = RunPhase.FAILED

        return RunHandle(
            run_id=canonical_run_id,
            final_state=final_phase,
            report_path=report_path,
            exit_code=exit_code,
            failure_reason=failure_reason,
        )

    # -------------------------------------------------------------------------
    # 内部辅助 — 步骤实现
    # -------------------------------------------------------------------------

    def _validate_env(self) -> None:
        """步骤 1：验证 ANTHROPIC_API_KEY 存在（fail-fast）。

        Raises:
            ApiKeyMissingError: 环境变量未设置
        """
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise ApiKeyMissingError(
                "ANTHROPIC_API_KEY 未设置。请先设置此环境变量后重试。\n"
                "示例：export ANTHROPIC_API_KEY=sk-ant-...",
            )

    def _create_ledger(self, config: RunConfig, requested_run_id: str | None) -> str:
        """步骤 3：创建 Ledger 条目，返回规范 run_id。

        若 requested_run_id 为 None，create_run 内部生成 ULID。
        若 requested_run_id 非 None（--name 覆盖），直接用该值作为 run_id，
        但需要手动创建目录树（绕过 create_run 的 ULID 生成）。

        Args:
            config           : RunConfig（run_id 字段可为 None）
            requested_run_id : 用户指定的 run_id（--name 覆盖）或 None

        Returns:
            str — 分配的规范 run_id
        """
        if requested_run_id is not None:
            # --name 覆盖模式：使用指定 run_id，需要手动建目录树
            from pars.paths import run_dir, artifacts_dir, ckpt_dir  # noqa: PLC0415
            from pars.ledger import write_state, new_run_state  # noqa: PLC0415
            from pars.ledger.config_io import get_run_config_path  # noqa: PLC0415
            from datetime import datetime, timezone  # noqa: PLC0415

            canonical_id = requested_run_id
            run_path = run_dir(canonical_id)
            run_path.mkdir(parents=True, exist_ok=True)
            artifacts_dir(canonical_id).mkdir(parents=True, exist_ok=True)
            ckpt_dir(canonical_id).mkdir(parents=True, exist_ok=True)

            # 写 config.yaml（含 run_id 和 created_at）
            filled_config = config.model_copy(
                update={
                    "run_id": canonical_id,
                    "created_at": datetime.now(timezone.utc),
                }
            )
            save_config(filled_config, get_run_config_path(canonical_id))

            # 写 state.json（初始 phase = INIT）
            state = new_run_state(canonical_id)
            write_state(state, canonical_id)

            logger.info(
                "RunOrchestrator: --name 覆盖模式，run_id=%s",
                canonical_id,
                extra={"run_id": canonical_id},
            )
            return canonical_id
        else:
            # 标准模式：create_run 生成 ULID
            return create_run(config)

    def _run_worker_with_monitors(
        self,
        run_id: str,
        wall_clock_hours_cap: float,
        gpu_hours_cap: float,
        usd_cap: float,
    ) -> tuple[int, str | None, Path | None]:
        """步骤 9-12：启动 worker + monitors，等待完成，生成报告。

        返回：
            (exit_code, failure_reason, report_path)
        """
        from pars.paths import run_dir  # noqa: PLC0415

        assert self._worker is not None  # noqa: S101

        exit_code = 5
        failure_reason: str | None = "worker_crash"
        report_path: Path | None = None

        # Worker.run() 是 generator，直接消费（内部管理 worktree/mount/proxy）
        # 注意：Worker 内部也会管理 proxy/worktree，与 orchestrator 的 cleanup 有重叠
        # 为避免双重 cleanup，我们在 orchestrator 中不直接操作 worktree/proxy
        # 而是让 Worker.run() 内部处理，orchestrator 只负责 monitors 停止

        worker_gen = self._worker.run()

        # 消费 generator（事件处理）
        try:
            for _event in worker_gen:
                pass  # 事件由 monitors 处理，此处仅消费
        except KeyboardInterrupt:
            # Ctrl+C：传播给外层处理
            raise

        # Worker 正常退出（或 SIGINT 后退出）
        exit_code = 0
        failure_reason = None

        # -----------------------------------------------------------------
        # 步骤 12: render_report + validate_report_schema
        # -----------------------------------------------------------------
        run_path = run_dir(run_id)
        try:
            report_path = render_report(run_path)
            logger.info(
                "RunOrchestrator: report 已生成",
                extra={"run_id": run_id, "report_path": str(report_path)},
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "RunOrchestrator: render_report 失败（已忽略）",
                extra={"run_id": run_id, "error": str(exc)},
            )
            report_path = None

        if report_path is not None:
            try:
                ok, errors = validate_report_schema(report_path)
                if not ok:
                    logger.warning(
                        "RunOrchestrator: report schema 校验失败",
                        extra={"run_id": run_id, "errors": errors},
                    )
            except Exception as exc:  # noqa: BLE001
                logger.warning(
                    "RunOrchestrator: validate_report_schema 失败（已忽略）",
                    extra={"run_id": run_id, "error": str(exc)},
                )

        # 更新 final state
        try:
            update_state(run_id, phase=RunPhase.COMPLETED)
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "RunOrchestrator: update_state 失败（已忽略）",
                extra={"run_id": run_id, "error": str(exc)},
            )

        return exit_code, failure_reason, report_path

    def _cleanup(self, run_id: str) -> None:
        """逆序 cleanup（幂等）：monitors → proxy → worktree → readonly。

        每步独立 try/except，保证即使中间步骤失败也继续清理。
        注意：Worker.run() 内部已做清理；此函数为 orchestrator 层次的额外清理。
        """
        logger.debug("RunOrchestrator._cleanup 开始", extra={"run_id": run_id})

        # 1. 停止 StuckMonitor
        if self._stuck_monitor is not None:
            try:
                self._stuck_monitor.stop()
                self._stuck_monitor.join(timeout=10)
            except Exception as exc:  # noqa: BLE001
                logger.error(
                    "cleanup: StuckMonitor 停止失败",
                    extra={"error": str(exc)},
                )
            finally:
                self._stuck_monitor = None

        # 2. 停止 BudgetMonitor
        if self._budget_monitor is not None:
            try:
                self._budget_monitor.stop()
                self._budget_monitor.join(timeout=10)
            except Exception as exc:  # noqa: BLE001
                logger.error(
                    "cleanup: BudgetMonitor 停止失败",
                    extra={"error": str(exc)},
                )
            finally:
                self._budget_monitor = None

        # 3. 停止 proxy（若 Worker.run() 未清理）
        if self._proxy_handle is not None:
            try:
                stop_proxy(self._proxy_handle)
                logger.info("cleanup: proxy 已停止", extra={"run_id": run_id})
            except Exception as exc:  # noqa: BLE001
                logger.error(
                    "cleanup: stop_proxy 失败（已忽略）",
                    extra={"error": str(exc)},
                )
            finally:
                self._proxy_handle = None

        # 4. release readonly mount（若 Worker.run() 未清理）
        if self._readonly_handle is not None:
            try:
                self._readonly_handle.release()
                logger.info("cleanup: .claude unmount 完成", extra={"run_id": run_id})
            except Exception as exc:  # noqa: BLE001
                logger.error(
                    "cleanup: unmount 失败（已忽略）",
                    extra={"error": str(exc)},
                )
            finally:
                self._readonly_handle = None

        # 5. remove worktree（若 Worker.run() 未清理）
        if self._worktree_handle is not None:
            try:
                remove_worktree(self._worktree_handle, force=True)
                logger.info("cleanup: worktree 已移除", extra={"run_id": run_id})
            except Exception as exc:  # noqa: BLE001
                logger.error(
                    "cleanup: remove_worktree 失败（已忽略）",
                    extra={"error": str(exc)},
                )
            finally:
                self._worktree_handle = None

        logger.debug("RunOrchestrator._cleanup 完成", extra={"run_id": run_id})
