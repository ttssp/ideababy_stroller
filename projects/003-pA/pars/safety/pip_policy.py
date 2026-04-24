"""
pars.safety.pip_policy — pip 调用白名单校验 (T015 · R5 · C17)

结论：纯函数，供 shell hook 与 Python 测试共用。
    仅允许三条等价白名单命令，其他全部 DENY。

目的：R5 防御 PyPI 供应链投毒。

三条等价白名单（architecture §7 · 唯一真相源）：
  A. pip install -r requirements-locked.txt --require-hashes
     → tokens: ["pip", "install", "-r", "requirements-locked.txt", "--require-hashes"]

  B. uv pip install -r requirements-locked.txt --require-hashes
     → tokens: ["uv", "pip", "install", "-r", "requirements-locked.txt", "--require-hashes"]

  C. uv sync --frozen
     → tokens: ["uv", "sync", "--frozen"]

实现策略（T015.md §Implementation plan）：
  - shlex.split → normalize（去除多余空格） → 与 allowlist 做 tuple 精确比较
  - 禁止任何额外参数（如 -v / --quiet），避免参数注入绕过
  - allowlist 用 tuple 比较，避免 regex 被绕过
  - 考虑 python -m pip / easy_install / pipx 变体 — 全部 deny
"""

from __future__ import annotations

import shlex
from dataclasses import dataclass
from enum import Enum


class PipCommandDecision(Enum):
    """pip 命令策略判决结果枚举。"""

    ALLOW = "allow"
    DENY_UNLOCKED = "deny_unlocked"  # 未指定 locked 文件 / 错误文件名
    DENY_NO_HASHES = "deny_no_hashes"  # pip 命令但无 --require-hashes
    DENY_UV_SYNC_UNFROZEN = "deny_uv_sync_unfrozen"  # uv sync 无 --frozen
    DENY_UV_ADD = "deny_uv_add"  # uv add 会修改 lock
    DENY_UNKNOWN = "deny_unknown"  # 不认识的命令形状 / 变体 / 空字符串


@dataclass(frozen=True)
class PipPolicyResult:
    """pip 策略判决结果，含决策 + 人类可读原因 + 替代建议。"""

    decision: PipCommandDecision
    reason: str
    # 如果 deny，给个替代建议
    allowed_alternative: str | None = None


# ---------------------------------------------------------------------------
# 白名单定义（architecture §7 唯一真相源）
# tuple 比较：精确匹配，禁止任何额外参数
# ---------------------------------------------------------------------------

_ALLOWLIST: tuple[tuple[str, ...], ...] = (
    # 白名单 A: pip install -r requirements-locked.txt --require-hashes
    ("pip", "install", "-r", "requirements-locked.txt", "--require-hashes"),
    # 白名单 B: uv pip install -r requirements-locked.txt --require-hashes
    ("uv", "pip", "install", "-r", "requirements-locked.txt", "--require-hashes"),
    # 白名单 C: uv sync --frozen
    ("uv", "sync", "--frozen"),
)

# 替代建议（deny 时展示给 worker 的指引）
_RECOMMENDED_USAGE = (
    "允许的命令形式：\n"
    "  pip install -r requirements-locked.txt --require-hashes\n"
    "  uv pip install -r requirements-locked.txt --require-hashes\n"
    "  uv sync --frozen\n"
    "请确认 requirements-locked.txt 已在仓库根目录。"
)


def evaluate_pip_command(cmd: str) -> PipPolicyResult:  # noqa: PLR0911
    """解析 shell cmd，返回策略判决。

    结论：
    - 空字符串 → DENY_UNKNOWN
    - 三条白名单（精确匹配）→ ALLOW
    - pip/pip3/uv pip/uv sync 相关命令 → 细分 DENY 类型
    - python -m pip / easy_install / pipx 等变体 → DENY_UNKNOWN
    - 其他 pip/uv 非 install 命令（pip --version / pip list）→ ALLOW（非安装操作）

    参数：
        cmd: 完整命令字符串（shlex 切分，支持多空格 normalize）

    示例：
        evaluate_pip_command("pip install -r requirements-locked.txt --require-hashes")
            → PipPolicyResult(decision=ALLOW, ...)
        evaluate_pip_command("pip install requests")
            → PipPolicyResult(decision=DENY_UNLOCKED, ...)
        evaluate_pip_command("uv sync")
            → PipPolicyResult(decision=DENY_UV_SYNC_UNFROZEN, ...)
    """
    # 空字符串直接拒绝
    if not cmd or not cmd.strip():
        return PipPolicyResult(
            decision=PipCommandDecision.DENY_UNKNOWN,
            reason="空命令",
            allowed_alternative=_RECOMMENDED_USAGE,
        )

    # shlex.split 规范化（处理多空格、引号等）
    try:
        tokens = tuple(shlex.split(cmd))
    except ValueError as exc:
        # shlex 解析失败（如未闭合引号）→ DENY_UNKNOWN
        return PipPolicyResult(
            decision=PipCommandDecision.DENY_UNKNOWN,
            reason=f"无法解析命令（shlex 错误）：{exc}",
            allowed_alternative=_RECOMMENDED_USAGE,
        )

    if not tokens:
        return PipPolicyResult(
            decision=PipCommandDecision.DENY_UNKNOWN,
            reason="空命令",
            allowed_alternative=_RECOMMENDED_USAGE,
        )

    # ------------------------------------------------------------------
    # 精确白名单匹配（tuple 比较，不允许额外参数）
    # ------------------------------------------------------------------
    if tokens in _ALLOWLIST:
        return PipPolicyResult(
            decision=PipCommandDecision.ALLOW,
            reason="命令在白名单中",
        )

    # ------------------------------------------------------------------
    # 从第一个 token 判断命令类型
    # ------------------------------------------------------------------
    first = tokens[0]

    # python -m pip ... → DENY_UNKNOWN（变体绕过）
    if first == "python" or first.startswith("python"):
        return PipPolicyResult(
            decision=PipCommandDecision.DENY_UNKNOWN,
            reason=(
                f"不允许通过 '{first} -m pip' 安装依赖。"
                "请使用白名单命令形式。"
            ),
            allowed_alternative=_RECOMMENDED_USAGE,
        )

    # easy_install / pipx → DENY_UNKNOWN
    if first in ("easy_install", "pipx"):
        return PipPolicyResult(
            decision=PipCommandDecision.DENY_UNKNOWN,
            reason=f"不允许使用 '{first}'，请使用白名单命令形式。",
            allowed_alternative=_RECOMMENDED_USAGE,
        )

    # ------------------------------------------------------------------
    # pip / pip3 系列
    # ------------------------------------------------------------------
    if first in ("pip", "pip3"):
        return _evaluate_pip_tokens(tokens)

    # ------------------------------------------------------------------
    # uv 系列
    # ------------------------------------------------------------------
    if first == "uv":
        return _evaluate_uv_tokens(tokens)

    # 其他未知命令 → DENY_UNKNOWN
    return PipPolicyResult(
        decision=PipCommandDecision.DENY_UNKNOWN,
        reason=f"未知命令前缀：'{first}'",
        allowed_alternative=_RECOMMENDED_USAGE,
    )


def _evaluate_pip_tokens(tokens: tuple[str, ...]) -> PipPolicyResult:  # noqa: PLR0911
    """处理 pip / pip3 开头的命令。

    结论：只有严格匹配白名单 A 才 ALLOW，其他细分 DENY 类型。
    注意：调用前已确认精确白名单匹配失败（不是 ALLOW 路径）。
    """
    # tokens[0] = pip/pip3，至少需要 tokens[1]
    if len(tokens) < 2:  # noqa: PLR2004
        return PipPolicyResult(
            decision=PipCommandDecision.DENY_UNKNOWN,
            reason="pip 命令过短，无法识别操作",
            allowed_alternative=_RECOMMENDED_USAGE,
        )

    subcmd = tokens[1]

    # pip --version / pip list / pip show / pip freeze 等非 install 操作 → ALLOW
    if subcmd not in ("install",):
        return PipPolicyResult(
            decision=PipCommandDecision.ALLOW,
            reason=f"pip {subcmd} 是非安装操作，不受白名单限制",
        )

    # pip install 系列：以下均为 deny（精确白名单已在上面匹配过）
    # 判断具体 deny 类型以给出友好提示
    token_set = set(tokens)

    # 检查是否有 -r requirements-locked.txt
    has_dash_r = "-r" in token_set
    has_locked_file = "requirements-locked.txt" in token_set
    has_require_hashes = "--require-hashes" in token_set

    if has_dash_r and has_locked_file and not has_require_hashes:
        # 有正确文件但缺 --require-hashes
        return PipPolicyResult(
            decision=PipCommandDecision.DENY_NO_HASHES,
            reason=(
                "pip install 必须包含 --require-hashes 以防止供应链投毒（R5）。\n"
                "缺失：--require-hashes"
            ),
            allowed_alternative=_RECOMMENDED_USAGE,
        )

    if has_dash_r and has_locked_file and has_require_hashes:
        # 有正确文件和 --require-hashes，但有额外参数（精确匹配失败）
        return PipPolicyResult(
            decision=PipCommandDecision.DENY_NO_HASHES,
            reason=(
                "pip install 不允许任何额外参数（防止参数注入绕过）。\n"
                "检测到白名单命令之外的额外参数。"
            ),
            allowed_alternative=_RECOMMENDED_USAGE,
        )

    # 没有 locked file 或没有 -r → DENY_UNLOCKED
    return PipPolicyResult(
        decision=PipCommandDecision.DENY_UNLOCKED,
        reason=(
            "pip install 必须使用 -r requirements-locked.txt（R5 pip 锁定）。\n"
            "不允许直接安装包名、git URL、index-url 等形式。"
        ),
        allowed_alternative=_RECOMMENDED_USAGE,
    )


def _evaluate_uv_tokens(tokens: tuple[str, ...]) -> PipPolicyResult:  # noqa: PLR0911
    """处理 uv 开头的命令。

    结论：只有白名单 B/C 才 ALLOW（精确匹配已在上面完成），其他细分 DENY。
    """
    if len(tokens) < 2:  # noqa: PLR2004
        return PipPolicyResult(
            decision=PipCommandDecision.DENY_UNKNOWN,
            reason="uv 命令过短，无法识别操作",
            allowed_alternative=_RECOMMENDED_USAGE,
        )

    subcmd = tokens[1]

    # uv add → DENY_UV_ADD（修改 lock 文件，污染 worker）
    if subcmd == "add":
        return PipPolicyResult(
            decision=PipCommandDecision.DENY_UV_ADD,
            reason=(
                "uv add 会修改 uv.lock，污染 worker 环境（R5）。\n"
                "worker 不允许变更依赖锁定文件。"
            ),
            allowed_alternative=_RECOMMENDED_USAGE,
        )

    # uv sync 系列（已知精确白名单匹配失败 → 缺 --frozen）
    if subcmd == "sync":
        return PipPolicyResult(
            decision=PipCommandDecision.DENY_UV_SYNC_UNFROZEN,
            reason=(
                "uv sync 必须加 --frozen 以强制按 lockfile 精确安装（R5）。\n"
                "缺失：--frozen"
            ),
            allowed_alternative=_RECOMMENDED_USAGE,
        )

    # uv pip 系列
    if subcmd == "pip":
        if len(tokens) >= 3 and tokens[2] == "install":  # noqa: PLR2004
            # uv pip install 但不匹配白名单 B
            return _evaluate_uv_pip_install_tokens(tokens)
        # uv pip list / uv pip show 等非 install → ALLOW
        return PipPolicyResult(
            decision=PipCommandDecision.ALLOW,
            reason="uv pip 非安装操作，不受白名单限制",
        )

    # uv lock / uv venv / uv python 等 → ALLOW（非安装操作）
    non_install_subcmds = ("lock", "venv", "python", "run", "tool", "self", "version", "help")
    if subcmd in non_install_subcmds:
        return PipPolicyResult(
            decision=PipCommandDecision.ALLOW,
            reason=f"uv {subcmd} 是非安装操作，不受白名单限制",
        )

    # 未知 uv 子命令 → DENY_UNKNOWN
    return PipPolicyResult(
        decision=PipCommandDecision.DENY_UNKNOWN,
        reason=f"未知 uv 子命令：'{subcmd}'",
        allowed_alternative=_RECOMMENDED_USAGE,
    )


def _evaluate_uv_pip_install_tokens(tokens: tuple[str, ...]) -> PipPolicyResult:
    """处理 uv pip install 系列（精确白名单匹配已失败）。

    结论：细分 DENY_UNLOCKED 或 DENY_NO_HASHES。
    """
    token_set = set(tokens)
    has_dash_r = "-r" in token_set
    has_locked_file = "requirements-locked.txt" in token_set
    has_require_hashes = "--require-hashes" in token_set

    if has_dash_r and has_locked_file and not has_require_hashes:
        return PipPolicyResult(
            decision=PipCommandDecision.DENY_NO_HASHES,
            reason=(
                "uv pip install 必须包含 --require-hashes（R5）。\n"
                "缺失：--require-hashes"
            ),
            allowed_alternative=_RECOMMENDED_USAGE,
        )

    if has_dash_r and has_locked_file and has_require_hashes:
        # 有正确文件和 --require-hashes 但有额外参数
        return PipPolicyResult(
            decision=PipCommandDecision.DENY_NO_HASHES,
            reason=(
                "uv pip install 不允许额外参数（防止参数注入绕过）。"
            ),
            allowed_alternative=_RECOMMENDED_USAGE,
        )

    return PipPolicyResult(
        decision=PipCommandDecision.DENY_UNLOCKED,
        reason=(
            "uv pip install 必须使用 -r requirements-locked.txt --require-hashes。\n"
            "不允许直接安装包名或其他形式。"
        ),
        allowed_alternative=_RECOMMENDED_USAGE,
    )


def format_denial_message(result: PipPolicyResult, cmd: str) -> str:
    """生成人类可读 deny 消息，给 worker 指引 requirements-locked.txt 路径。

    结论：格式化 deny 结果为可读错误消息，含命令回显 + 拒绝原因 + 替代建议。
    """
    lines = [
        f"[pip-policy] DENIED: {result.decision.value}",
        f"  命令: {cmd!r}",
        f"  原因: {result.reason}",
    ]
    if result.allowed_alternative:
        lines.append(f"  建议:\n{result.allowed_alternative}")
    return "\n".join(lines)


def is_pip_install_allowed(cmd: str) -> tuple[bool, str]:
    """兼容接口：供 hook 和测试使用（T015.md §Outputs 定义）。

    结论：将 evaluate_pip_command 包装为 (allowed: bool, reason: str) 元组。

    参数：
        cmd: 完整命令字符串

    返回：
        (True, "allowed") 如果命令在白名单中
        (False, reason)   如果命令被拒绝，reason 含拒绝原因
    """
    result = evaluate_pip_command(cmd)
    if result.decision == PipCommandDecision.ALLOW:
        return True, "allowed"
    return False, result.reason
