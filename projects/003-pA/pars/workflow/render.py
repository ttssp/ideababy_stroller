"""
pars.workflow.render — Jinja2 模板渲染层（T016）

结论：
  提供两个核心函数，将 templates/ 下的 Jinja2 模板渲染为确定性 Python 脚本。
  所有路径通过 env var 注入（D18 路径可移植），绝不硬编码。

设计要点：
  - StrictUndefined：缺少任何模板变量即 raise UndefinedError，防止静默渲染出缺字段的脚本
  - 确定性渲染：相同 ctx → 相同 SHA256（无时间戳、随机数注入）
  - 模板位置：<repo_root>/projects/003-pA/templates/（相对于本模块位置解析）
  - 输出位置：runs/<run_id>/artifacts/<name>.py（T027 demo 可审计 + 复现）

对应 task：specs/003-pA/tasks/T016.md D15/D18
"""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

# ---------------------------------------------------------------------------
# 模板目录解析（相对于本文件向上找 templates/）
# ---------------------------------------------------------------------------

# pars/workflow/render.py → pars/workflow/ → pars/ → projects/003-pA/ → templates/
_THIS_FILE = Path(__file__).resolve()
_TEMPLATES_DIR = _THIS_FILE.parent.parent.parent / "templates"


def _get_jinja_env() -> Environment:
    """构造 Jinja2 Environment（StrictUndefined，FileSystemLoader 指向 templates/）。

    StrictUndefined 语义：
    - 模板变量未在 ctx 中提供 → UndefinedError（而非渲染空字符串）
    - 保证 missing var 立即暴露，不产生静默错误的脚本

    每次调用创建新 Environment（保证线程安全、可测试，性能损耗可忽略）。
    """
    return Environment(
        loader=FileSystemLoader(str(_TEMPLATES_DIR)),
        undefined=StrictUndefined,
        keep_trailing_newline=True,  # 保留模板末尾换行，符合 Python 文件惯例
        autoescape=False,  # 脚本模板，不转义 HTML
    )


# ---------------------------------------------------------------------------
# 公开 API
# ---------------------------------------------------------------------------


def render_template(template_name: str, ctx: dict) -> str:
    """渲染指定模板，返回渲染后的字符串。

    确定性保证：
    - 相同 template_name + ctx → 完全相同的输出字符串 → 相同 SHA256
    - 模板本身不注入时间戳、随机数等非确定性内容

    Args:
        template_name: 模板文件名（相对于 templates/ 目录），如 "baseline_script.py.j2"
                       支持子目录：如 "prompts/worker_system_prompt.md.j2"
        ctx:           模板变量 dict；StrictUndefined 下，缺少任何模板用到的变量
                       都会 raise UndefinedError

    Returns:
        渲染后的字符串内容

    Raises:
        UndefinedError: ctx 缺少模板中引用的变量
        TemplateNotFound: template_name 在 templates/ 下不存在
    """
    env = _get_jinja_env()
    template = env.get_template(template_name)
    return template.render(**ctx)


def write_rendered_script(run_id: str, template_name: str, ctx: dict) -> Path:
    """渲染模板并写入 runs/<run_id>/artifacts/<name>.py，返回写入路径。

    路径解析：
    - 依赖 pars.paths.run_dir(run_id) → $RECALLKIT_RUN_DIR/<run_id>
    - 写入 <run_dir>/artifacts/<stem>.py（去掉 .j2 后缀，保留原文件名 stem）
    - 自动创建 artifacts/ 目录（如不存在）

    用途：
    - worker 审计：artifacts/ 下保存实际运行的脚本（可审计）
    - T027 demo 复现：可直接用相同 config 重新渲染验证脚本一致性

    Args:
        run_id:        run 唯一标识（ULID 格式）
        template_name: 模板文件名（相对于 templates/），如 "baseline_script.py.j2"
        ctx:           模板变量 dict

    Returns:
        Path: 写入的脚本文件绝对路径

    Raises:
        UndefinedError: ctx 缺少模板变量
        OSError: 磁盘错误
    """
    from pars.paths import run_dir

    # 渲染内容
    content = render_template(template_name, ctx)

    # 目标路径：去掉 .j2 后缀，写入 artifacts/
    # 支持 "prompts/worker_system_prompt.md.j2" → artifacts/worker_system_prompt.md
    template_stem = Path(template_name).name  # 取文件名部分
    if template_stem.endswith(".j2"):
        output_name = template_stem[:-3]  # 去掉 .j2
    else:
        output_name = template_stem

    artifacts_dir = run_dir(run_id) / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    output_path = artifacts_dir / output_name
    output_path.write_text(content, encoding="utf-8")

    return output_path
