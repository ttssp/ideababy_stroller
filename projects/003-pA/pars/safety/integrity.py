"""worker_claude_dir integrity 校验（第二道验证，post-run）。

C21 / R6 · T012:
启动时记录 settings.json / CLAUDE.md / hooks/*.sh 的 SHA-256 manifest；
worker 退出后再次校验；发现变更 → 记 CRITICAL + R6 事件。

设计说明：
- 第一道防御：fail-closed 只读 mount（bindfs / chflags）
- 第二道防御（本模块）：post-run SHA-256 manifest 对比
  即使只读 mount 意外失效，仍能事后检测到篡改
- 忽略 .DS_Store / .gitkeep / 符号链接目标（只记录链接本身）
"""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

# sentinel 值：用于 verify_manifest 返回结果中标识文件状态
MISSING = "__MISSING__"       # 文件在磁盘上不存在（被删除）
UNEXPECTED = "__UNEXPECTED__" # 文件不在 expected manifest 中（新增）


def compute_manifest(root: Path) -> dict[Path, str]:
    """递归计算目录下所有常规文件的 SHA-256 digest。

    返回：{相对路径: sha256_hex_string}

    规则：
    - 只计算常规文件（regular file），排除目录本身、符号链接目标
    - 符号链接：只记录链接本身（readlink 路径作为内容哈希），不跟进目标
    - 忽略 .DS_Store / .gitkeep（macOS 和 git 占位文件）
    - 路径为相对于 root 的 Path 对象（POSIX 格式）

    Args:
        root: 要扫描的目录（必须存在）

    Returns:
        dict，键为相对 Path，值为 sha256 hex digest
    """
    root = Path(root)
    result: dict[Path, str] = {}

    if not root.exists() or not root.is_dir():
        return result

    # 遍历所有文件（包含符号链接路径本身）
    for entry in sorted(root.rglob("*")):
        # 只处理文件（常规文件 + 符号链接），跳过目录
        if entry.is_dir() and not entry.is_symlink():
            continue

        # 忽略 macOS 和 git 占位文件
        if entry.name in (".DS_Store", ".gitkeep"):
            continue

        rel_path = entry.relative_to(root)

        if entry.is_symlink():
            # 符号链接：哈希链接目标路径字符串（不跟进目标）
            link_target = str(entry.readlink())
            digest = sha256(link_target.encode()).hexdigest()
        else:
            # 常规文件：哈希文件内容
            digest = sha256(entry.read_bytes()).hexdigest()

        result[rel_path] = digest

    return result


def verify_manifest(
    root: Path,
    expected: dict[Path, str],
) -> list[tuple[Path, str, str]]:
    """对比磁盘状态与 expected manifest，返回不一致列表。

    检测三类情况：
    1. 文件内容变更（hash 不同）
    2. 文件被删除（actual 用 MISSING sentinel）
    3. 新增文件（expected 用 UNEXPECTED sentinel，表示"意外出现"）

    Args:
        root:     要扫描的目录
        expected: compute_manifest() 返回的快照

    Returns:
        不一致列表，每项为 (相对路径, expected_hash, actual_hash)
        空 list = integrity OK
    """
    actual = compute_manifest(root)
    violations: list[tuple[Path, str, str]] = []

    # 检查 expected 中的每个文件：是否被删除或被修改
    for rel_path, exp_hash in expected.items():
        act_hash = actual.get(rel_path)
        if act_hash is None:
            # 文件被删除
            violations.append((rel_path, exp_hash, MISSING))
        elif act_hash != exp_hash:
            # 文件内容被修改
            violations.append((rel_path, exp_hash, act_hash))

    # 检查 actual 中多出的文件（新增文件）
    for rel_path in actual:
        if rel_path not in expected:
            # 新增文件（expected 不认识）
            violations.append((rel_path, UNEXPECTED, actual[rel_path]))

    return violations


def compute_tree_sha256(root: Path) -> str:
    """计算整个目录树的稳定聚合 SHA-256。

    算法：
    1. 递归获取所有文件的 (相对路径, content_hash)
    2. 按相对路径排序（确保稳定性）
    3. 将列表序列化为 JSON 字符串（确保跨平台稳定）
    4. 对 JSON 字符串再算一次 SHA-256 → 返回

    适用于 integrity.py 第一版（compute_manifest 的聚合版）。
    T012 spec 中 verify_manifest 使用 per-file 校验；
    本函数供 verify_tree_unchanged 使用。

    Args:
        root: 目录路径

    Returns:
        整棵树的 SHA-256 hex digest
    """
    import json

    manifest = compute_manifest(root)
    # 排序确保稳定性（dict 遍历顺序 Python 3.7+ 有序，但 rglob 顺序可能受 OS 影响）
    sorted_entries = sorted(
        [(str(rel), digest) for rel, digest in manifest.items()]
    )
    canonical = json.dumps(sorted_entries, ensure_ascii=False, separators=(",", ":"))
    return sha256(canonical.encode()).hexdigest()


def verify_tree_unchanged(root: Path, expected_sha: str) -> bool:
    """验证目录树 SHA-256 未变（与 compute_tree_sha256 配对使用）。

    Args:
        root:         要验证的目录
        expected_sha: 之前 compute_tree_sha256 返回的值

    Returns:
        True = 未变；False = 已变（篡改 / 增删文件）
    """
    actual_sha = compute_tree_sha256(root)
    return actual_sha == expected_sha
