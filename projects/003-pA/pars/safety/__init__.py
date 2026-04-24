"""
pars.safety — 安全 deny 清单与 hook 管理。

职责：管理 worker_claude_dir/ 下的 settings.json deny 规则和 hooks 脚本；
提供 is_command_allowed() 供 proxy 层使用；fail-closed 只读挂载逻辑。
由 T012 实现。

T012 公共 API：
  - readonly_mount: ensure_readonly_claude_dir, detect_best_strategy, MountStrategy,
                    MountResult, ReadonlyHandle, ReadonlyFailsClosed, refuse_to_start
  - integrity:      compute_manifest, verify_manifest, compute_tree_sha256,
                    verify_tree_unchanged, MISSING, UNEXPECTED
"""

from pars.safety.integrity import (
    MISSING,
    UNEXPECTED,
    compute_manifest,
    compute_tree_sha256,
    verify_manifest,
    verify_tree_unchanged,
)
from pars.safety.readonly_mount import (
    MountResult,
    MountStrategy,
    ReadonlyFailsClosed,
    ReadonlyHandle,
    detect_best_strategy,
    ensure_readonly_claude_dir,
    mount_readonly,
    refuse_to_start,
    unmount,
)

__all__ = [  # noqa: RUF022
    # integrity
    "MISSING",
    "UNEXPECTED",
    "compute_manifest",
    "compute_tree_sha256",
    "verify_manifest",
    "verify_tree_unchanged",
    # readonly_mount
    "MountResult",
    "MountStrategy",
    "ReadonlyFailsClosed",
    "ReadonlyHandle",
    "detect_best_strategy",
    "ensure_readonly_claude_dir",
    "mount_readonly",
    "refuse_to_start",
    "unmount",
]
