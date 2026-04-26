"""
WatchedFolderWatcher 集成测试 — T006
结论: 写 PDF 到 tmpdir inbox → watcher 捕获文件事件 → 触发 enqueue 回调
细节:
  - 测试 watchdog Observer 和 5s poll fallback 两条路径
  - TECH-6 跨平台: macOS/Linux 均用 watchdog.observers.Observer
  - 不依赖真实 DB, enqueue callback 用 mock 验证
"""

from __future__ import annotations

import asyncio
import shutil
from pathlib import Path

import pytest

from decision_ledger.pipeline.watcher import WatchedFolderWatcher


@pytest.fixture
def inbox_dir(tmp_path: Path) -> Path:
    """临时 inbox 目录。"""
    inbox = tmp_path / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    return inbox


@pytest.fixture
def sample_pdf_path() -> Path:
    """指向 tests/fixtures 的 sample PDF。"""
    here = Path(__file__).parent.parent.parent  # tests/
    return here / "fixtures" / "sample_advisor_2026w17.pdf"


class TestWatchedFolderWatcher:
    """WatchedFolderWatcher 单元/集成测试。"""

    async def test_should_enqueue_when_pdf_dropped_to_inbox(
        self, inbox_dir: Path, sample_pdf_path: Path
    ) -> None:
        """写一个 PDF 到 tmpdir inbox, watcher 触发 enqueue 单测。"""
        enqueued: list[Path] = []

        async def mock_enqueue(path: Path) -> None:
            enqueued.append(path)

        watcher = WatchedFolderWatcher(inbox_dir=inbox_dir, enqueue_callback=mock_enqueue)

        # 启动 watcher（短暂运行后停止）
        watcher_task = asyncio.create_task(watcher.start())

        # 给 watcher 启动时间
        await asyncio.sleep(0.2)

        # 复制 PDF 到 inbox
        dest = inbox_dir / "sample_advisor_2026w17.pdf"
        shutil.copy2(sample_pdf_path, dest)

        # 等待 watcher 捕获（最多 3s）
        deadline = asyncio.get_event_loop().time() + 3.0
        while not enqueued and asyncio.get_event_loop().time() < deadline:
            await asyncio.sleep(0.1)

        watcher.stop()
        await asyncio.wait_for(watcher_task, timeout=2.0)

        assert len(enqueued) >= 1
        assert enqueued[0] == dest

    async def test_should_ignore_non_pdf_files(
        self, inbox_dir: Path
    ) -> None:
        """非 PDF 文件不触发 enqueue。"""
        enqueued: list[Path] = []

        async def mock_enqueue(path: Path) -> None:
            enqueued.append(path)

        watcher = WatchedFolderWatcher(inbox_dir=inbox_dir, enqueue_callback=mock_enqueue)
        watcher_task = asyncio.create_task(watcher.start())

        await asyncio.sleep(0.2)

        # 写入 txt 文件
        txt_file = inbox_dir / "not_a_pdf.txt"
        txt_file.write_text("hello")

        await asyncio.sleep(1.0)  # 等待潜在的误触发

        watcher.stop()
        await asyncio.wait_for(watcher_task, timeout=2.0)

        assert len(enqueued) == 0

    async def test_should_create_inbox_dir_if_missing(self, tmp_path: Path) -> None:
        """inbox 不存在时，WatchedFolderWatcher 应自动创建。"""
        inbox = tmp_path / "new_inbox_dir"
        assert not inbox.exists()

        enqueued: list[Path] = []

        async def mock_enqueue(path: Path) -> None:
            enqueued.append(path)

        watcher = WatchedFolderWatcher(inbox_dir=inbox, enqueue_callback=mock_enqueue)
        watcher_task = asyncio.create_task(watcher.start())
        await asyncio.sleep(0.2)
        watcher.stop()
        await asyncio.wait_for(watcher_task, timeout=2.0)

        assert inbox.exists()

    async def test_should_handle_stop_idempotent(self, inbox_dir: Path) -> None:
        """多次调用 stop() 不报错。"""
        enqueued: list[Path] = []

        async def mock_enqueue(path: Path) -> None:
            enqueued.append(path)

        watcher = WatchedFolderWatcher(inbox_dir=inbox_dir, enqueue_callback=mock_enqueue)
        watcher_task = asyncio.create_task(watcher.start())
        await asyncio.sleep(0.2)

        watcher.stop()
        watcher.stop()  # 第二次 stop 不应报错
        await asyncio.wait_for(watcher_task, timeout=2.0)

    async def test_should_use_poll_observer_as_fallback(
        self, inbox_dir: Path, sample_pdf_path: Path
    ) -> None:
        """强制 poll observer 模式（TECH-6 fallback）也能检测到文件。"""
        enqueued: list[Path] = []

        async def mock_enqueue(path: Path) -> None:
            enqueued.append(path)

        # 强制 poll 模式
        watcher = WatchedFolderWatcher(
            inbox_dir=inbox_dir,
            enqueue_callback=mock_enqueue,
            force_poll=True,
            poll_interval=0.5,
        )

        watcher_task = asyncio.create_task(watcher.start())
        await asyncio.sleep(0.6)

        dest = inbox_dir / "poll_test.pdf"
        shutil.copy2(sample_pdf_path, dest)

        deadline = asyncio.get_event_loop().time() + 5.0
        while not enqueued and asyncio.get_event_loop().time() < deadline:
            await asyncio.sleep(0.2)

        watcher.stop()
        await asyncio.wait_for(watcher_task, timeout=3.0)

        assert len(enqueued) >= 1
