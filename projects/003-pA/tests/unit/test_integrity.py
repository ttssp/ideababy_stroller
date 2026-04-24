"""tests.unit.test_integrity — pars.safety.integrity 单元测试。

T012 · C21 · R6:
SHA-256 manifest 校验是第二道验证（post-run integrity check）。
即使 fail-closed 只读 mount 意外失效，本检测层仍能发现篡改。

测试覆盖点（spec T012 要求 ≥6 个）：
1. compute_manifest 覆盖所有常规文件（非目录/非符号链接）
2. compute_manifest 排除目录本身（只返回文件路径）
3. 空目录返回空 dict
4. verify_manifest 完全一致 → 空 list
5. 单文件篡改 → verify 返回 1 条记录（含 path/expected/actual）
6. 文件删除 → verify 返回记录（actual 用 MISSING sentinel）
7. 新增文件 → verify 返回记录（expected 用 UNEXPECTED sentinel）
8. compute_tree_sha256 + verify_tree_unchanged 聚合校验正/负路径
9. 符号链接处理：链接本身被记录，链接目标被排除
10. .DS_Store / .gitkeep 被忽略
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from pars.safety.integrity import (
    MISSING,
    UNEXPECTED,
    compute_manifest,
    compute_tree_sha256,
    verify_manifest,
    verify_tree_unchanged,
)


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------


def _write(path: Path, content: str = "hello") -> None:
    """在 path 写入内容（自动 mkdir）。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Test 1: compute_manifest 覆盖所有常规文件
# ---------------------------------------------------------------------------


def test_compute_manifest_should_include_all_regular_files_when_directory_has_files(
    tmp_path: Path,
) -> None:
    """should include all regular files when directory has multiple files."""
    _write(tmp_path / "a.txt", "aaa")
    _write(tmp_path / "b.txt", "bbb")
    _write(tmp_path / "sub" / "c.txt", "ccc")

    manifest = compute_manifest(tmp_path)

    assert len(manifest) == 3
    assert Path("a.txt") in manifest
    assert Path("b.txt") in manifest
    assert Path("sub/c.txt") in manifest

    # SHA-256 格式正确（64 hex chars）
    for digest in manifest.values():
        assert len(digest) == 64
        assert all(c in "0123456789abcdef" for c in digest)


# ---------------------------------------------------------------------------
# Test 2: compute_manifest 排除目录本身
# ---------------------------------------------------------------------------


def test_compute_manifest_should_exclude_directories_when_scanning(
    tmp_path: Path,
) -> None:
    """should not include directory paths, only file paths."""
    _write(tmp_path / "file.txt", "data")
    (tmp_path / "empty_dir").mkdir()

    manifest = compute_manifest(tmp_path)

    # 只有 file.txt，empty_dir 不在里面
    assert len(manifest) == 1
    assert Path("file.txt") in manifest

    # 确认所有键都指向文件，不含纯目录
    for rel_path in manifest:
        full = tmp_path / rel_path
        # 最终路径是文件或符号链接
        assert full.exists() or full.is_symlink()


# ---------------------------------------------------------------------------
# Test 3: 空目录返回空 dict
# ---------------------------------------------------------------------------


def test_compute_manifest_should_return_empty_dict_when_directory_is_empty(
    tmp_path: Path,
) -> None:
    """should return empty dict when directory has no files."""
    manifest = compute_manifest(tmp_path)
    assert manifest == {}


# ---------------------------------------------------------------------------
# Test 4: verify_manifest 完全一致 → 空 list
# ---------------------------------------------------------------------------


def test_verify_manifest_should_return_empty_list_when_no_changes(
    tmp_path: Path,
) -> None:
    """should return empty list when manifest matches current state."""
    _write(tmp_path / "settings.json", '{"version": "0.1"}')
    _write(tmp_path / "hooks" / "pre_tool_use.sh", "#!/bin/bash\nexit 0")

    expected = compute_manifest(tmp_path)
    violations = verify_manifest(tmp_path, expected)

    assert violations == []


# ---------------------------------------------------------------------------
# Test 5: 单文件篡改 → verify 返回 1 条记录
# ---------------------------------------------------------------------------


def test_verify_manifest_should_return_one_violation_when_single_file_tampered(
    tmp_path: Path,
) -> None:
    """should return 1 violation record with correct path/expected/actual when file modified."""
    settings = tmp_path / "settings.json"
    _write(settings, '{"version": "0.1"}')

    expected = compute_manifest(tmp_path)

    # 篡改文件内容
    _write(settings, '{"version": "0.2", "TAMPERED": true}')

    violations = verify_manifest(tmp_path, expected)

    assert len(violations) == 1
    rel_path, exp_hash, act_hash = violations[0]

    assert rel_path == Path("settings.json")
    assert len(exp_hash) == 64        # 有效 sha256
    assert len(act_hash) == 64        # 有效 sha256（新内容）
    assert exp_hash != act_hash       # 不同


# ---------------------------------------------------------------------------
# Test 6: 文件删除 → verify 返回记录（actual = MISSING）
# ---------------------------------------------------------------------------


def test_verify_manifest_should_return_missing_sentinel_when_file_deleted(
    tmp_path: Path,
) -> None:
    """should return MISSING sentinel as actual_hash when file is deleted."""
    hook = tmp_path / "hooks" / "pre_tool_use.sh"
    _write(hook, "#!/bin/bash")

    expected = compute_manifest(tmp_path)

    # 删除文件
    hook.unlink()

    violations = verify_manifest(tmp_path, expected)

    assert len(violations) == 1
    rel_path, exp_hash, act_hash = violations[0]

    assert rel_path == Path("hooks/pre_tool_use.sh")
    assert act_hash == MISSING
    assert len(exp_hash) == 64


# ---------------------------------------------------------------------------
# Test 7: 新增文件 → verify 返回记录（expected = UNEXPECTED）
# ---------------------------------------------------------------------------


def test_verify_manifest_should_return_unexpected_sentinel_when_new_file_added(
    tmp_path: Path,
) -> None:
    """should return UNEXPECTED sentinel as expected_hash when new file appears."""
    _write(tmp_path / "settings.json", '{"v": "0.1"}')

    expected = compute_manifest(tmp_path)

    # 新增文件（模拟 worker 尝试注入文件）
    _write(tmp_path / "evil_hook.sh", "#!/bin/bash\nexit 0")

    violations = verify_manifest(tmp_path, expected)

    assert len(violations) == 1
    rel_path, exp_hash, act_hash = violations[0]

    assert rel_path == Path("evil_hook.sh")
    assert exp_hash == UNEXPECTED
    assert len(act_hash) == 64


# ---------------------------------------------------------------------------
# Test 8: compute_tree_sha256 + verify_tree_unchanged 聚合校验
# ---------------------------------------------------------------------------


def test_compute_tree_sha256_should_be_stable_when_unchanged(tmp_path: Path) -> None:
    """should return identical sha when called twice on unchanged directory."""
    _write(tmp_path / "a.txt", "hello")
    _write(tmp_path / "b.sh", "#!/bin/bash")

    sha1 = compute_tree_sha256(tmp_path)
    sha2 = compute_tree_sha256(tmp_path)

    assert sha1 == sha2
    assert len(sha1) == 64


def test_verify_tree_unchanged_should_return_true_when_no_modification(tmp_path: Path) -> None:
    """should return True when directory is unchanged."""
    _write(tmp_path / "settings.json", '{"v": "0.1"}')
    snapshot = compute_tree_sha256(tmp_path)

    assert verify_tree_unchanged(tmp_path, snapshot) is True


def test_verify_tree_unchanged_should_return_false_when_file_modified(tmp_path: Path) -> None:
    """should return False (detect tampering) when file content changes."""
    target = tmp_path / "settings.json"
    _write(target, '{"v": "0.1"}')
    snapshot = compute_tree_sha256(tmp_path)

    # 篡改
    _write(target, '{"v": "TAMPERED"}')

    assert verify_tree_unchanged(tmp_path, snapshot) is False


# ---------------------------------------------------------------------------
# Test 9: 符号链接处理
# ---------------------------------------------------------------------------


def test_compute_manifest_should_record_symlink_itself_not_target(
    tmp_path: Path,
) -> None:
    """should record symlink path (not follow target) when symlink present."""
    # 创建真实文件和符号链接
    real_file = tmp_path / "real.txt"
    _write(real_file, "real content")
    link_file = tmp_path / "link.txt"
    link_file.symlink_to(real_file)

    manifest = compute_manifest(tmp_path)

    # 两个条目都有（real.txt 和 link.txt）
    assert Path("real.txt") in manifest
    assert Path("link.txt") in manifest

    # 符号链接和真实文件的 hash 不同
    # （link hash = hash(target_path_str) 而非 hash(content)）
    assert manifest[Path("real.txt")] != manifest[Path("link.txt")]


# ---------------------------------------------------------------------------
# Test 10: .DS_Store / .gitkeep 被忽略
# ---------------------------------------------------------------------------


def test_compute_manifest_should_ignore_ds_store_and_gitkeep(tmp_path: Path) -> None:
    """should ignore .DS_Store and .gitkeep files."""
    _write(tmp_path / ".DS_Store", "macOS junk")
    _write(tmp_path / ".gitkeep", "")
    _write(tmp_path / "settings.json", '{"v": "0.1"}')

    manifest = compute_manifest(tmp_path)

    assert Path(".DS_Store") not in manifest
    assert Path(".gitkeep") not in manifest
    assert Path("settings.json") in manifest
    assert len(manifest) == 1


# ---------------------------------------------------------------------------
# Test 11: 多文件同时被篡改 → 多条 violations
# ---------------------------------------------------------------------------


def test_verify_manifest_should_return_multiple_violations_when_multiple_files_changed(
    tmp_path: Path,
) -> None:
    """should return all violations when multiple files are modified."""
    _write(tmp_path / "a.txt", "aaa")
    _write(tmp_path / "b.txt", "bbb")
    _write(tmp_path / "c.txt", "ccc")

    expected = compute_manifest(tmp_path)

    # 同时篡改两个文件
    _write(tmp_path / "a.txt", "TAMPERED_A")
    _write(tmp_path / "b.txt", "TAMPERED_B")

    violations = verify_manifest(tmp_path, expected)

    # 两条篡改记录
    tampered_paths = {v[0] for v in violations}
    assert Path("a.txt") in tampered_paths
    assert Path("b.txt") in tampered_paths
    assert len(violations) == 2

    for _, exp_hash, act_hash in violations:
        assert act_hash != MISSING
        assert exp_hash != UNEXPECTED


# ---------------------------------------------------------------------------
# Test 12: 不存在的根目录返回空 dict
# ---------------------------------------------------------------------------


def test_compute_manifest_should_return_empty_when_root_does_not_exist(
    tmp_path: Path,
) -> None:
    """should return empty dict when root path does not exist."""
    nonexistent = tmp_path / "no_such_dir"
    manifest = compute_manifest(nonexistent)
    assert manifest == {}


# ---------------------------------------------------------------------------
# Test 13: 文件内容相同但路径不同 → 两条独立记录
# ---------------------------------------------------------------------------


def test_compute_manifest_should_track_paths_independently_when_content_identical(
    tmp_path: Path,
) -> None:
    """should give each file its own entry even when content is identical."""
    _write(tmp_path / "file1.sh", "#!/bin/bash\nexit 0")
    _write(tmp_path / "file2.sh", "#!/bin/bash\nexit 0")

    manifest = compute_manifest(tmp_path)

    assert len(manifest) == 2
    # 内容相同，hash 也相同
    assert manifest[Path("file1.sh")] == manifest[Path("file2.sh")]


# ---------------------------------------------------------------------------
# Test 14: compute_manifest 使用 os.environ 不影响结果（防副作用）
# ---------------------------------------------------------------------------


def test_compute_manifest_should_not_depend_on_environment_variables(
    tmp_path: Path,
) -> None:
    """should produce same result regardless of environment variables."""
    _write(tmp_path / "settings.json", "content")

    sha_before = compute_tree_sha256(tmp_path)

    os.environ["TEST_DUMMY_VAR"] = "some_value"
    sha_after = compute_tree_sha256(tmp_path)

    os.environ.pop("TEST_DUMMY_VAR", None)

    assert sha_before == sha_after
