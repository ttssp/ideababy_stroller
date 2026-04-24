"""`.claude/` fail-closed 只读分离。

C21 / R6 · T012:
worker 容器内 `.claude/` 配置必须对 worker 进程只读，
防止 worker 修改自己的 hooks / settings 绕过 deny 清单（Sakana v1 事故）。

实现优先级（OQ5 CONFIRMED · 操作员 2026-04-24）：
  1. MacFUSE + bindfs（推荐，最强 fail-closed）
  2. chflags uchg（macOS）/ chattr +i（Linux）— fallback，需 sudo 装机一次
  3. chmod -w（仅 RECALLKIT_ALLOW_UNSAFE_CHMOD=1 测试环境）
  4. refuse-to-start（fail-closed 兜底）

禁用：纯 chmod 作为生产路径（可被 os.chmod 绕回）

公共 API：
  ensure_readonly_claude_dir(worktree, template) -> ReadonlyHandle
  ReadonlyHandle.release()                        # 清理，供 orchestrator teardown 用

  detect_best_strategy()    -> MountStrategy
  mount_readonly(src, tgt)  -> MountResult
  unmount(result)           -> None
  refuse_to_start(reason)   -> NoReturn
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from pars.logging import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# 类型定义
# ---------------------------------------------------------------------------


class MountStrategy(Enum):
    """可用的只读策略（按强度排序）。"""

    BINDFS = "bindfs"            # MacFUSE / Linux FUSE — 最强 fail-closed
    IMMUTABLE_FLAG = "immutable" # chflags uchg / chattr +i — 需 sudo
    UNSAFE_CHMOD = "chmod"       # 仅 RECALLKIT_ALLOW_UNSAFE_CHMOD=1 测试环境
    REFUSE = "refuse"            # fail-closed 兜底


class ReadonlyFailsClosed(RuntimeError):  # noqa: N818
    """当所有可接受的只读策略都不可用时抛出（fail-closed 兜底）。

    orchestrator 捕获此异常后调用 refuse_to_start() → exit 2。
    命名使用 FailsClosed 而非 Error 以明确语义（规格 T012 / C21 要求保持此命名）。
    """


@dataclass
class MountResult:
    """mount_readonly 的返回值，供 unmount 使用。"""

    strategy: MountStrategy
    source: Path
    target: Path
    cleanup_cmd: list[str] | None = field(default=None)  # unmount / chflags nouchg 命令
    chmod_files: list[Path] = field(default_factory=list)  # UNSAFE_CHMOD 模式用


@dataclass
class ReadonlyHandle:
    """ensure_readonly_claude_dir 的返回值。

    封装 MountResult，提供 release() 清理接口。
    """

    _result: MountResult

    def release(self) -> None:
        """清理 mount / 恢复 mutable flag，由 orchestrator teardown 调用。"""
        unmount(self._result)


# ---------------------------------------------------------------------------
# 核心函数：策略探测
# ---------------------------------------------------------------------------


def detect_best_strategy() -> MountStrategy:
    """检测本机可用的最佳只读策略。

    探测顺序（不真正挂载）：
      1. which bindfs → 可用 → BINDFS
      2. 测试 env 标志 RECALLKIT_ALLOW_UNSAFE_CHMOD=1 → UNSAFE_CHMOD（仅测试）
      3. 平台支持 chflags（macOS）或 chattr（Linux）→ IMMUTABLE_FLAG
      4. 其他 → REFUSE

    Returns:
        检测到的最佳 MountStrategy
    """
    # 1. 检查 bindfs 是否可用
    if shutil.which("bindfs") is not None:
        logger.info("readonly_mount: bindfs 可用，使用 BINDFS 策略")
        return MountStrategy.BINDFS

    # 2. 测试环境降级（RECALLKIT_ALLOW_UNSAFE_CHMOD=1）
    if os.environ.get("RECALLKIT_ALLOW_UNSAFE_CHMOD") == "1":
        logger.warning(
            "readonly_mount: RECALLKIT_ALLOW_UNSAFE_CHMOD=1 已设置，"
            "使用 UNSAFE_CHMOD 模式（非生产路径！仅用于 CI / 开发测试）"
        )
        return MountStrategy.UNSAFE_CHMOD

    # 3. 检查平台级 immutable flag 支持
    sys_platform = platform.system()
    if sys_platform == "Darwin":
        # macOS：检查 chflags 可用性
        if shutil.which("chflags") is not None:
            logger.info("readonly_mount: macOS chflags 可用，使用 IMMUTABLE_FLAG 策略")
            return MountStrategy.IMMUTABLE_FLAG
    elif sys_platform == "Linux":
        # Linux：检查 chattr 可用性
        if shutil.which("chattr") is not None:
            logger.info("readonly_mount: Linux chattr 可用，使用 IMMUTABLE_FLAG 策略")
            return MountStrategy.IMMUTABLE_FLAG

    # 4. 全部失败 → refuse
    logger.error("readonly_mount: 无可用的 fail-closed 只读策略")
    return MountStrategy.REFUSE


# ---------------------------------------------------------------------------
# 核心函数：挂载只读
# ---------------------------------------------------------------------------


def mount_readonly(
    source: Path,
    target: Path,
    *,
    strategy: MountStrategy | None = None,
) -> MountResult:
    """对 source 挂载只读副本到 target。

    Args:
        source:   源目录（worker_claude_dir 模板路径）
        target:   目标挂载点（worker worktree 内的 .claude/ 路径）
        strategy: 若 None 则自动探测（调用 detect_best_strategy）

    Returns:
        MountResult（供 unmount 使用）

    Raises:
        ReadonlyFailsClosed: 当策略为 REFUSE 或操作实际失败且无 fallback 时
    """
    if strategy is None:
        strategy = detect_best_strategy()

    source = Path(source).resolve()
    target = Path(target)

    if strategy == MountStrategy.REFUSE:
        refuse_to_start(
            "所有 fail-closed 只读策略均不可用"
            "（bindfs 未安装、chflags/chattr 不可用、非测试环境）"
        )

    # 确保挂载点目录存在
    target.mkdir(parents=True, exist_ok=True)

    if strategy == MountStrategy.BINDFS:
        return _mount_bindfs(source, target)
    elif strategy == MountStrategy.IMMUTABLE_FLAG:
        return _mount_immutable(source, target)
    elif strategy == MountStrategy.UNSAFE_CHMOD:
        return _mount_unsafe_chmod(source, target)
    else:
        refuse_to_start(f"未知策略: {strategy}")


def _mount_bindfs(source: Path, target: Path) -> MountResult:
    """使用 bindfs 进行只读挂载（MacFUSE / Linux FUSE）。

    macOS: bindfs -o ro,nonempty <source> <target>
    Linux: 先 mount --bind 再 mount -o remount,ro（需 root 或 FUSE）

    Raises:
        ReadonlyFailsClosed: bindfs 命令执行失败
    """
    sys_platform = platform.system()

    if sys_platform == "Darwin":
        cmd = [
            "bindfs",
            "-o", "ro,nonempty",
            "--no-allow-other",
            str(source),
            str(target),
        ]
        cleanup_cmd = ["umount", str(target)]
    elif shutil.which("bindfs") is not None:
        # Linux：bindfs 通用命令
        cmd = [
            "bindfs",
            "-o", "ro",
            str(source),
            str(target),
        ]
        cleanup_cmd = ["fusermount", "-u", str(target)]
    else:
        # fallback: Linux mount --bind（需 root）
        try:
            subprocess.run(  # noqa: S603
                ["mount", "--bind", str(source), str(target)],
                check=True, capture_output=True, text=True,
            )
            subprocess.run(  # noqa: S603
                ["mount", "-o", "remount,ro", str(target)],
                check=True, capture_output=True, text=True,
            )
        except subprocess.CalledProcessError as exc:
            raise ReadonlyFailsClosed(
                f"Linux mount --bind 失败（需要 root）: {exc.stderr}"
            ) from exc
        return MountResult(
            strategy=MountStrategy.BINDFS,
            source=source,
            target=target,
            cleanup_cmd=["umount", str(target)],
        )

    try:
        subprocess.run(  # noqa: S603
            cmd, check=True, capture_output=True, text=True,
        )
        logger.info(
            "readonly_mount: bindfs 挂载成功",
            extra={"source": str(source), "target": str(target)},
        )
    except subprocess.CalledProcessError as exc:
        raise ReadonlyFailsClosed(
            f"bindfs 挂载失败: {exc.stderr or exc.stdout}"
        ) from exc
    except FileNotFoundError as exc:
        raise ReadonlyFailsClosed(
            f"bindfs 命令未找到: {exc}"
        ) from exc

    return MountResult(
        strategy=MountStrategy.BINDFS,
        source=source,
        target=target,
        cleanup_cmd=cleanup_cmd,
    )


def _mount_immutable(source: Path, target: Path) -> MountResult:  # noqa: PLR0912
    """使用 immutable flag 保护文件（chflags uchg / chattr +i）。

    流程：
    1. 将 source 内容复制到 target（cp -R 或 shutil.copytree）
    2. 对 target 下所有文件设置 immutable flag（需 sudo / 已 root）

    Raises:
        ReadonlyFailsClosed: 命令执行失败
    """
    sys_platform = platform.system()

    # 复制文件到目标（先清空目标目录内容）
    if target.exists():
        for item in target.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    else:
        target.mkdir(parents=True, exist_ok=True)

    shutil.copytree(str(source), str(target), dirs_exist_ok=True)

    # 收集所有复制过去的文件
    immutable_files: list[Path] = []
    for entry in target.rglob("*"):
        if entry.is_file():
            immutable_files.append(entry)

    if sys_platform == "Darwin":
        # macOS：chflags uchg
        for f in immutable_files:
            try:
                subprocess.run(  # noqa: S603,S607
                    ["chflags", "uchg", str(f)],
                    check=True, capture_output=True, text=True,
                )
            except subprocess.CalledProcessError as exc:
                raise ReadonlyFailsClosed(
                    f"chflags uchg 失败（可能需要 sudo）: {exc.stderr}"
                ) from exc
        cleanup_cmd = ["chflags", "nouchg"]
    else:
        # Linux：chattr +i
        for f in immutable_files:
            try:
                subprocess.run(  # noqa: S603,S607
                    ["chattr", "+i", str(f)],
                    check=True, capture_output=True, text=True,
                )
            except subprocess.CalledProcessError as exc:
                raise ReadonlyFailsClosed(
                    f"chattr +i 失败（可能需要 root）: {exc.stderr}"
                ) from exc
        cleanup_cmd = ["chattr", "-i"]

    logger.info(
        "readonly_mount: immutable flag 设置成功",
        extra={"target": str(target), "files": len(immutable_files)},
    )

    return MountResult(
        strategy=MountStrategy.IMMUTABLE_FLAG,
        source=source,
        target=target,
        cleanup_cmd=cleanup_cmd,
        chmod_files=immutable_files,
    )


def _mount_unsafe_chmod(source: Path, target: Path) -> MountResult:
    """UNSAFE：仅 RECALLKIT_ALLOW_UNSAFE_CHMOD=1 测试模式使用。

    纯 chmod -R a-w 不是生产路径（Python os.chmod 可绕过）。
    仅供 CI / 测试环境使用。

    打印显著警告后继续。
    """
    _print_unsafe_banner()

    # 复制文件到目标
    if target.exists():
        for item in target.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    else:
        target.mkdir(parents=True, exist_ok=True)

    shutil.copytree(str(source), str(target), dirs_exist_ok=True)

    # 收集文件并设置 a-w
    chmod_files: list[Path] = []
    for entry in target.rglob("*"):
        if entry.is_file():
            chmod_files.append(entry)
            entry.chmod(entry.stat().st_mode & ~0o222)  # 去掉所有写权限位

    logger.warning(
        "readonly_mount: UNSAFE chmod 模式已应用（非生产路径）",
        extra={"target": str(target), "files": len(chmod_files)},
    )

    return MountResult(
        strategy=MountStrategy.UNSAFE_CHMOD,
        source=source,
        target=target,
        cleanup_cmd=None,
        chmod_files=chmod_files,
    )


def _print_unsafe_banner() -> None:
    """打印 UNSAFE 模式警告 banner。"""
    banner = (
        "\n"
        "╔══════════════════════════════════════════════════════════════╗\n"
        "║  WARNING: RECALLKIT_ALLOW_UNSAFE_CHMOD=1 已设置              ║\n"
        "║  当前使用 chmod 模式 — 这不是生产路径！                        ║\n"
        "║  Python os.chmod() 可以绕过此保护。                            ║\n"
        "║  仅限 CI / 开发测试环境使用。                                  ║\n"
        "║  生产环境请安装 bindfs（brew install bindfs + MacFUSE）        ║\n"
        "╚══════════════════════════════════════════════════════════════╝\n"
    )
    print(banner, file=sys.stderr, flush=True)


# ---------------------------------------------------------------------------
# 核心函数：卸载 / 恢复
# ---------------------------------------------------------------------------


def unmount(result: MountResult) -> None:
    """清理：umount / 恢复 mutable flag。

    对应 mount_readonly 的逆操作，由 orchestrator teardown 调用。

    Args:
        result: mount_readonly 返回的 MountResult
    """
    strategy = result.strategy
    target = result.target

    if strategy == MountStrategy.BINDFS:
        _unmount_bindfs(target, result.cleanup_cmd)

    elif strategy == MountStrategy.IMMUTABLE_FLAG:
        _unmount_immutable(result)

    elif strategy == MountStrategy.UNSAFE_CHMOD:
        _unmount_unsafe_chmod(result)

    else:
        logger.warning(f"readonly_mount: 未知策略 {strategy}，跳过 unmount")


def _unmount_bindfs(target: Path, cleanup_cmd: list[str] | None) -> None:
    """卸载 bindfs 挂载点。"""
    if cleanup_cmd is None:
        sys_platform = platform.system()
        if sys_platform == "Darwin":
            cleanup_cmd = ["umount", str(target)]
        else:
            cleanup_cmd = ["fusermount", "-u", str(target)]

    try:
        subprocess.run(  # noqa: S603
            cleanup_cmd, check=True, capture_output=True, text=True,
        )
        logger.info("readonly_mount: bindfs 卸载成功", extra={"target": str(target)})
    except subprocess.CalledProcessError as exc:
        logger.error(
            "readonly_mount: bindfs 卸载失败（忽略，继续 teardown）",
            extra={"error": exc.stderr, "target": str(target)},
        )


def _unmount_immutable(result: MountResult) -> None:
    """恢复 immutable flag → 清除文件。"""
    target = result.target
    sys_platform = platform.system()

    for f in result.chmod_files:
        if not f.exists():
            continue
        try:
            if sys_platform == "Darwin":
                subprocess.run(  # noqa: S603,S607
                    ["chflags", "nouchg", str(f)],
                    check=True, capture_output=True, text=True,
                )
            else:
                subprocess.run(  # noqa: S603,S607
                    ["chattr", "-i", str(f)],
                    check=True, capture_output=True, text=True,
                )
        except subprocess.CalledProcessError as exc:
            logger.warning(
                "readonly_mount: 恢复 mutable flag 失败",
                extra={"file": str(f), "error": exc.stderr},
            )

    # 清除复制的目录
    if target.exists():
        shutil.rmtree(target, ignore_errors=True)

    logger.info("readonly_mount: immutable flag 恢复 + 目录清除完成")


def _unmount_unsafe_chmod(result: MountResult) -> None:
    """恢复 chmod 写权限 → 清除文件。"""
    for f in result.chmod_files:
        if f.exists():
            try:
                f.chmod(f.stat().st_mode | 0o644)
            except OSError:
                pass

    if result.target.exists():
        shutil.rmtree(result.target, ignore_errors=True)

    logger.info("readonly_mount: UNSAFE chmod 模式清除完成")


# ---------------------------------------------------------------------------
# fail-closed 兜底
# ---------------------------------------------------------------------------


def refuse_to_start(reason: str) -> None:
    """打印明确错误 + OQ5 引导，然后 sys.exit(1)。

    orchestrator 若用 ReadonlyFailsClosed 捕获了异常，
    可以自己决定退出码（推荐 exit 2 表示配置错误）。
    本函数用于无 orchestrator 的直接调用场景。

    Args:
        reason: 错误原因说明
    """
    msg = f"""
错误：无法建立 fail-closed 的 .claude/ 只读分离（C21）

原因：{reason}

解决方案：
  方案 A（推荐）：brew install --cask macfuse && brew install bindfs
                  安装后重启以加载 MacFUSE kext，再重新运行。
  方案 B（一次性）：sudo chflags -R uchg worker_claude_dir/
                   （装机时运行一次；worker 每次重建 .claude/ 时重新执行）
  方案 C（测试/CI）：export RECALLKIT_ALLOW_UNSAFE_CHMOD=1
                   （非生产路径！chmod 可被 Python os.chmod 绕过）

v0.1 不接受纯 chmod 作为生产路径；请见 OQ5（architecture §6）。
退出码 2 = 配置错误，非程序 crash。
"""
    print(msg, file=sys.stderr, flush=True)
    logger.critical(
        "readonly_mount: refuse to start",
        extra={"reason": reason},
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# 高层接口：ensure_readonly_claude_dir
# ---------------------------------------------------------------------------


def ensure_readonly_claude_dir(
    worktree: Path,
    template: Path,
    *,
    strategy: MountStrategy | None = None,
) -> ReadonlyHandle:
    """确保 worker worktree 内的 .claude/ 是只读的。

    流程：
    1. 探测最佳策略（若未指定）
    2. 将 template（worker_claude_dir/）内容以只读方式挂载到
       worktree/.claude/
    3. 返回 ReadonlyHandle，orchestrator teardown 时调用 handle.release()

    Args:
        worktree: worker 的 git worktree 根目录（如 .worktrees/<run-id>/）
        template: worker_claude_dir/ 模板路径
        strategy: 强制使用特定策略（None = 自动探测）

    Returns:
        ReadonlyHandle

    Raises:
        ReadonlyFailsClosed: 无可用策略时（orchestrator 应捕获 + exit 2）
    """
    claude_dir = worktree / ".claude"
    result = mount_readonly(
        source=template,
        target=claude_dir,
        strategy=strategy,
    )
    return ReadonlyHandle(_result=result)
