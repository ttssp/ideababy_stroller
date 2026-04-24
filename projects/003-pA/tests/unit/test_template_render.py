"""
tests.unit.test_template_render — Jinja2 模板渲染单元测试（T016）

结论：
  - 每个模板至少 2 个测试：missing var 报错 + 合法渲染 + 路径来自 env
  - SHA256 确定性：相同 config → 同 hash
  - 所有路径来自 os.environ（RECALLKIT_RUN_DIR / RECALLKIT_CKPT_DIR / HF_HOME）
  - 无硬编码 /home/ 或 /Users/ 路径（docstring 除外）

对应 task：specs/003-pA/tasks/T016.md
依赖：pars.workflow.render（T016 实现）
"""

from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path

import pytest
from jinja2 import UndefinedError


# ---------------------------------------------------------------------------
# 从 render 模块导入（若模块未实现测试会在此 fail，是期望的失败原因）
# ---------------------------------------------------------------------------

from pars.workflow.render import render_template, write_rendered_script


# ---------------------------------------------------------------------------
# 测试用 config fixture
# ---------------------------------------------------------------------------

BASELINE_CTX = {
    "base_model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "dataset_id": "tatsu-lab/alpaca",
    "dataset_split": "train",
    "n_samples": 100,
    "eval_tasks": "hellaswag",
}

LORA_CTX = {
    "base_model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "dataset_id": "tatsu-lab/alpaca",
    "lora_rank": 8,
    "lora_alpha": 16,
    "lr": 2e-4,
    "epochs": 1,
    "batch_size": 4,
    "max_seq_len": 512,
}

EVAL_CTX = {
    "base_model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "lora_ckpt_dir": "/tmp/ckpt",
    "eval_tasks": "hellaswag",
    "n_shot": 0,
    "limit": 10,
}

PROMPT_CTX = {
    "run_id": "01JTEST00000000000000000000",
    "base_model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "dataset_id": "tatsu-lab/alpaca",
    "question": "Does LoRA SFT improve GSM8K accuracy?",
}


# ---------------------------------------------------------------------------
# baseline_script 模板测试
# ---------------------------------------------------------------------------


class TestBaselineTemplate:
    """baseline_script.py.j2 模板测试。"""

    def test_missing_required_var_raises_undefined_error(self):
        """missing var → UndefinedError（StrictUndefined 生效）。"""
        # 故意漏掉 dataset_id
        ctx = {k: v for k, v in BASELINE_CTX.items() if k != "dataset_id"}
        with pytest.raises(UndefinedError):
            render_template("baseline_script.py.j2", ctx)

    def test_valid_render_contains_base_model(self):
        """合法 ctx → 渲染结果包含 base_model 值。"""
        result = render_template("baseline_script.py.j2", BASELINE_CTX)
        assert "TinyLlama/TinyLlama-1.1B-Chat-v1.0" in result

    def test_valid_render_contains_dataset_id(self):
        """合法 ctx → 渲染结果包含 dataset_id 值。"""
        result = render_template("baseline_script.py.j2", BASELINE_CTX)
        assert "tatsu-lab/alpaca" in result

    def test_valid_render_contains_eval_tasks(self):
        """合法 ctx → 渲染结果包含 eval_tasks 值。"""
        result = render_template("baseline_script.py.j2", BASELINE_CTX)
        assert "hellaswag" in result

    def test_paths_use_env_vars(self):
        """渲染结果的路径必须来自 os.environ，不含硬编码绝对路径。"""
        result = render_template("baseline_script.py.j2", BASELINE_CTX)
        assert 'os.environ["RECALLKIT_RUN_DIR"]' in result or "RECALLKIT_RUN_DIR" in result

    def test_no_hardcoded_absolute_paths(self):
        """渲染后脚本不含 /home/ 或 /Users/ 硬编码（docstring/注释除外）。"""
        result = render_template("baseline_script.py.j2", BASELINE_CTX)
        # 过滤掉注释行和 docstring 行（# 或 ''' 或 """）
        code_lines = [
            line for line in result.splitlines()
            if not line.strip().startswith("#") and '"""' not in line and "'''" not in line
        ]
        code_text = "\n".join(code_lines)
        assert "/home/" not in code_text
        assert "/Users/" not in code_text

    def test_metrics_jsonl_written_with_phase_baseline(self):
        """渲染结果应包含 phase=baseline 的 metrics.jsonl 写入逻辑。"""
        result = render_template("baseline_script.py.j2", BASELINE_CTX)
        assert "baseline" in result
        assert "metrics.jsonl" in result

    def test_render_is_deterministic_same_sha256(self):
        """相同 ctx → 两次渲染 SHA256 相同（确定性输出，可审计）。"""
        r1 = render_template("baseline_script.py.j2", BASELINE_CTX)
        r2 = render_template("baseline_script.py.j2", BASELINE_CTX)
        h1 = hashlib.sha256(r1.encode()).hexdigest()
        h2 = hashlib.sha256(r2.encode()).hexdigest()
        assert h1 == h2

    def test_rendered_python_is_syntactically_valid(self):
        """渲染后的脚本能通过 ast.parse（Python 语法合法）。"""
        import ast

        result = render_template("baseline_script.py.j2", BASELINE_CTX)
        # 应不抛出 SyntaxError
        ast.parse(result)

    def test_env_var_count_ge_2(self):
        """渲染后 RECALLKIT_ env var 引用数量 >= 2（路径可移植性）。"""
        result = render_template("baseline_script.py.j2", BASELINE_CTX)
        count = len(re.findall(r'RECALLKIT_', result))
        assert count >= 2, f"期望 >=2 个 RECALLKIT_ 引用，实际 {count}"


# ---------------------------------------------------------------------------
# lora_script 模板测试
# ---------------------------------------------------------------------------


class TestLoraTemplate:
    """lora_script.py.j2 模板测试。"""

    def test_missing_lora_rank_raises_undefined_error(self):
        """missing lora_rank → UndefinedError。"""
        ctx = {k: v for k, v in LORA_CTX.items() if k != "lora_rank"}
        with pytest.raises(UndefinedError):
            render_template("lora_script.py.j2", ctx)

    def test_missing_base_model_raises_undefined_error(self):
        """missing base_model → UndefinedError。"""
        ctx = {k: v for k, v in LORA_CTX.items() if k != "base_model"}
        with pytest.raises(UndefinedError):
            render_template("lora_script.py.j2", ctx)

    def test_valid_render_contains_unsloth_import(self):
        """合法 ctx → 渲染结果包含 Unsloth import。"""
        result = render_template("lora_script.py.j2", LORA_CTX)
        assert "from unsloth import FastLanguageModel" in result

    def test_valid_render_contains_sft_trainer(self):
        """合法 ctx → 渲染结果包含 SFTTrainer。"""
        result = render_template("lora_script.py.j2", LORA_CTX)
        assert "SFTTrainer" in result

    def test_valid_render_contains_lora_rank(self):
        """合法 ctx → 渲染结果包含 lora_rank 值（8）。"""
        result = render_template("lora_script.py.j2", LORA_CTX)
        assert "8" in result  # lora_rank=8

    def test_checkpoint_written_to_env_ckpt_dir(self):
        """渲染结果的 checkpoint 路径来自 RECALLKIT_CKPT_DIR。"""
        result = render_template("lora_script.py.j2", LORA_CTX)
        assert "RECALLKIT_CKPT_DIR" in result

    def test_resume_checkpoint_logic_present(self):
        """渲染结果包含 resume-friendly 逻辑（检查 last/ 目录）。"""
        result = render_template("lora_script.py.j2", LORA_CTX)
        assert "last" in result  # 检测 last/ 目录
        assert "resume_from_checkpoint" in result

    def test_metrics_jsonl_event_train_epoch(self):
        """渲染结果包含 train_epoch event 写入逻辑。"""
        result = render_template("lora_script.py.j2", LORA_CTX)
        assert "train_epoch" in result
        assert "metrics.jsonl" in result

    def test_no_api_key_literal(self):
        """渲染结果不含任何 API key 字面量（安全规则）。"""
        result = render_template("lora_script.py.j2", LORA_CTX)
        assert "sk-ant-" not in result
        assert "ANTHROPIC_API_KEY" not in result  # 训练脚本不应感知 API key

    def test_rendered_python_is_syntactically_valid(self):
        """渲染后的脚本能通过 ast.parse。"""
        import ast

        result = render_template("lora_script.py.j2", LORA_CTX)
        ast.parse(result)

    def test_render_is_deterministic_same_sha256(self):
        """相同 ctx → SHA256 确定性。"""
        r1 = render_template("lora_script.py.j2", LORA_CTX)
        r2 = render_template("lora_script.py.j2", LORA_CTX)
        h1 = hashlib.sha256(r1.encode()).hexdigest()
        h2 = hashlib.sha256(r2.encode()).hexdigest()
        assert h1 == h2

    def test_env_var_count_ge_2(self):
        """渲染后 RECALLKIT_ env var 引用数量 >= 2。"""
        result = render_template("lora_script.py.j2", LORA_CTX)
        count = len(re.findall(r'RECALLKIT_', result))
        assert count >= 2, f"期望 >=2 个 RECALLKIT_ 引用，实际 {count}"

    def test_no_hardcoded_absolute_paths(self):
        """渲染后代码行中不含 /home/ 或 /Users/。"""
        result = render_template("lora_script.py.j2", LORA_CTX)
        code_lines = [
            line for line in result.splitlines()
            if not line.strip().startswith("#") and '"""' not in line and "'''" not in line
        ]
        code_text = "\n".join(code_lines)
        assert "/home/" not in code_text
        assert "/Users/" not in code_text


# ---------------------------------------------------------------------------
# eval_script 模板测试
# ---------------------------------------------------------------------------


class TestEvalTemplate:
    """eval_script.py.j2 模板测试。"""

    def test_missing_eval_tasks_raises_undefined_error(self):
        """missing eval_tasks → UndefinedError。"""
        ctx = {k: v for k, v in EVAL_CTX.items() if k != "eval_tasks"}
        with pytest.raises(UndefinedError):
            render_template("eval_script.py.j2", ctx)

    def test_missing_base_model_raises_undefined_error(self):
        """missing base_model → UndefinedError。"""
        ctx = {k: v for k, v in EVAL_CTX.items() if k != "base_model"}
        with pytest.raises(UndefinedError):
            render_template("eval_script.py.j2", ctx)

    def test_valid_render_contains_lm_eval_import(self):
        """合法 ctx → 渲染结果包含 lm_eval import。"""
        result = render_template("eval_script.py.j2", EVAL_CTX)
        assert "lm_eval" in result

    def test_valid_render_contains_simple_evaluate(self):
        """合法 ctx → 渲染结果包含 simple_evaluate 调用。"""
        result = render_template("eval_script.py.j2", EVAL_CTX)
        assert "simple_evaluate" in result

    def test_valid_render_contains_eval_tasks(self):
        """合法 ctx → 渲染结果包含 eval_tasks 值。"""
        result = render_template("eval_script.py.j2", EVAL_CTX)
        assert "hellaswag" in result

    def test_metrics_jsonl_event_eval_scores(self):
        """渲染结果包含 eval_scores event 写入逻辑。"""
        result = render_template("eval_script.py.j2", EVAL_CTX)
        assert "eval_scores" in result
        assert "metrics.jsonl" in result

    def test_scores_json_artifact_written(self):
        """渲染结果包含 scores.json 写入逻辑。"""
        result = render_template("eval_script.py.j2", EVAL_CTX)
        assert "scores.json" in result

    def test_rendered_python_is_syntactically_valid(self):
        """渲染后的脚本能通过 ast.parse。"""
        import ast

        result = render_template("eval_script.py.j2", EVAL_CTX)
        ast.parse(result)

    def test_render_is_deterministic_same_sha256(self):
        """相同 ctx → SHA256 确定性。"""
        r1 = render_template("eval_script.py.j2", EVAL_CTX)
        r2 = render_template("eval_script.py.j2", EVAL_CTX)
        h1 = hashlib.sha256(r1.encode()).hexdigest()
        h2 = hashlib.sha256(r2.encode()).hexdigest()
        assert h1 == h2

    def test_env_var_count_ge_2(self):
        """渲染后 RECALLKIT_ env var 引用数量 >= 2。"""
        result = render_template("eval_script.py.j2", EVAL_CTX)
        count = len(re.findall(r'RECALLKIT_', result))
        assert count >= 2, f"期望 >=2 个 RECALLKIT_ 引用，实际 {count}"

    def test_no_hardcoded_absolute_paths(self):
        """渲染后代码行中不含 /home/ 或 /Users/。"""
        result = render_template("eval_script.py.j2", EVAL_CTX)
        code_lines = [
            line for line in result.splitlines()
            if not line.strip().startswith("#") and '"""' not in line and "'''" not in line
        ]
        code_text = "\n".join(code_lines)
        assert "/home/" not in code_text
        assert "/Users/" not in code_text


# ---------------------------------------------------------------------------
# prompt 模板测试
# ---------------------------------------------------------------------------


class TestWorkerSystemPromptTemplate:
    """worker_system_prompt.md.j2 模板测试。"""

    def test_missing_run_id_raises_undefined_error(self):
        """missing run_id → UndefinedError。"""
        ctx = {k: v for k, v in PROMPT_CTX.items() if k != "run_id"}
        with pytest.raises(UndefinedError):
            render_template("prompts/worker_system_prompt.md.j2", ctx)

    def test_missing_question_raises_undefined_error(self):
        """missing question → UndefinedError。"""
        ctx = {k: v for k, v in PROMPT_CTX.items() if k != "question"}
        with pytest.raises(UndefinedError):
            render_template("prompts/worker_system_prompt.md.j2", ctx)

    def test_valid_render_contains_run_id(self):
        """合法 ctx → 渲染结果包含 run_id 值。"""
        result = render_template("prompts/worker_system_prompt.md.j2", PROMPT_CTX)
        assert "01JTEST00000000000000000000" in result

    def test_valid_render_contains_failure_attribution(self):
        """合法 ctx → 渲染结果包含失败归因说明（workflow 关键步骤）。"""
        result = render_template("prompts/worker_system_prompt.md.j2", PROMPT_CTX)
        assert "failure_attribution" in result or "失败归因" in result

    def test_valid_render_contains_pip_install_prohibition(self):
        """合法 ctx → 渲染结果包含禁止随意 pip install 的说明。"""
        result = render_template("prompts/worker_system_prompt.md.j2", PROMPT_CTX)
        assert "pip install" in result

    def test_valid_render_contains_config_yaml_workflow(self):
        """合法 ctx → 渲染结果包含 config.yaml → render → run → write 流程。"""
        result = render_template("prompts/worker_system_prompt.md.j2", PROMPT_CTX)
        assert "config" in result.lower()

    def test_render_is_deterministic_same_sha256(self):
        """相同 ctx → SHA256 确定性。"""
        r1 = render_template("prompts/worker_system_prompt.md.j2", PROMPT_CTX)
        r2 = render_template("prompts/worker_system_prompt.md.j2", PROMPT_CTX)
        h1 = hashlib.sha256(r1.encode()).hexdigest()
        h2 = hashlib.sha256(r2.encode()).hexdigest()
        assert h1 == h2


# ---------------------------------------------------------------------------
# write_rendered_script 测试（文件系统写入）
# ---------------------------------------------------------------------------


class TestWriteRenderedScript:
    """write_rendered_script() 函数测试。"""

    def test_writes_file_to_correct_path(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """write_rendered_script 应写入 runs/<id>/artifacts/<name>.py。"""
        run_id = "01JTEST00000000000000000000"
        runs_root = tmp_path / "runs"
        runs_root.mkdir()
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))

        output_path = write_rendered_script(run_id, "baseline_script.py.j2", BASELINE_CTX)

        assert output_path.exists()
        assert output_path.suffix == ".py"
        assert output_path.name == "baseline_script.py"
        # 应在 runs/<id>/artifacts/ 下
        assert "artifacts" in str(output_path)
        assert run_id in str(output_path)

    def test_written_file_content_matches_render(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """写入文件内容与 render_template 输出完全一致。"""
        run_id = "01JTEST00000000000000000001"
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))

        output_path = write_rendered_script(run_id, "baseline_script.py.j2", BASELINE_CTX)
        content = output_path.read_text(encoding="utf-8")
        expected = render_template("baseline_script.py.j2", BASELINE_CTX)

        assert content == expected

    def test_returns_path_object(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """write_rendered_script 返回 Path 对象。"""
        run_id = "01JTEST00000000000000000002"
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))

        result = write_rendered_script(run_id, "baseline_script.py.j2", BASELINE_CTX)

        assert isinstance(result, Path)
