"""
WatchedFolderWatcher — T006
结论: asyncio 任务，用 watchdog 监听 inbox 目录新增 PDF，触发 enqueue 回调
细节:
  - 默认用 watchdog.observers.Observer（macOS FSEvents / Linux inotify 原生）
  - force_poll=True 时用 watchdog.observers.polling.PollingObserver（TECH-6 fallback）
  - 仅对 .pdf 后缀文件调用 enqueue_callback
  - stop() 幂等：多次调用不报错
  - 若 inbox_dir 不存在，自动创建
  - asyncio event loop 通过 asyncio.get_event_loop() 持有，回调用 loop.call_soon_threadsafe
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver
from watchdog.observers.polling import PollingObserver

logger = logging.getLogger(__name__)


class _PDFEventHandler(FileSystemEventHandler):
    """
    watchdog 事件处理器 — 仅对新建 .pdf 文件触发回调。
    结论: 在 watchdog 线程中被调用，需用 loop.call_soon_threadsafe 回到 asyncio。
    """

    def __init__(
        self,
        enqueue_callback: Callable[[Path], Awaitable[None]],
        loop: asyncio.AbstractEventLoop,
    ) -> None:
        super().__init__()
        self._enqueue_callback = enqueue_callback
        self._loop = loop

    def on_created(self, event: FileSystemEvent) -> None:
        """结论: 仅处理非目录的 .pdf 文件创建事件。"""
        if event.is_directory:
            return
        src_path = Path(str(event.src_path))
        if src_path.suffix.lower() != ".pdf":
            return
        logger.info("检测到新 PDF: %s", src_path)
        # 从 watchdog 线程安全地调度 asyncio 协程
        self._loop.call_soon_threadsafe(
            asyncio.ensure_future,
            self._enqueue_callback(src_path),
        )


class WatchedFolderWatcher:
    """
    asyncio 任务：监听 inbox 目录新增 PDF，触发 enqueue 回调。

    结论:
      - start() 启动 watchdog Observer，阻塞直到 stop() 被调用
      - stop() 幂等，可多次调用

    使用方式:
        watcher = WatchedFolderWatcher(inbox_dir=Path("..."), enqueue_callback=my_fn)
        task = asyncio.create_task(watcher.start())
        ...
        watcher.stop()
        await task
    """

    def __init__(
        self,
        inbox_dir: Path,
        enqueue_callback: Callable[[Path], Awaitable[None]],
        *,
        force_poll: bool = False,
        poll_interval: float = 5.0,
    ) -> None:
        """
        参数:
            inbox_dir: 监听的收件箱目录路径（不存在时自动创建）
            enqueue_callback: 新 PDF 出现时调用的 async 回调
            force_poll: True 时强制使用 PollingObserver（TECH-6 fallback）
            poll_interval: 轮询间隔（秒），仅 force_poll=True 时有效，默认 5.0
        """
        self._inbox_dir = inbox_dir
        self._enqueue_callback = enqueue_callback
        self._force_poll = force_poll
        self._poll_interval = poll_interval
        self._observer: BaseObserver | None = None
        self._stop_event = asyncio.Event()

    async def start(self) -> None:
        """
        启动 watchdog Observer，监听 inbox_dir 直到 stop() 被调用。
        结论: asyncio.sleep(0.1) 轮询 _stop_event，让 Observer 在后台线程运行。
        """
        # 自动创建 inbox 目录
        self._inbox_dir.mkdir(parents=True, exist_ok=True)
        logger.info("WatchedFolderWatcher 启动: %s", self._inbox_dir)

        loop = asyncio.get_event_loop()
        handler = _PDFEventHandler(
            enqueue_callback=self._enqueue_callback,
            loop=loop,
        )

        # TECH-6: force_poll=True → PollingObserver（跨平台 fallback）
        observer: BaseObserver
        if self._force_poll:
            observer = PollingObserver(timeout=self._poll_interval)
        else:
            observer = Observer()

        self._observer = observer
        observer.schedule(handler, str(self._inbox_dir), recursive=False)
        observer.start()

        try:
            # 非阻塞轮询，等待 stop() 信号
            while not self._stop_event.is_set():
                await asyncio.sleep(0.1)
        finally:
            observer.stop()
            observer.join(timeout=5.0)
            logger.info("WatchedFolderWatcher 已停止")

    def stop(self) -> None:
        """
        停止 watcher（幂等，可多次调用）。
        结论: 设置 asyncio.Event，start() 协程的 while 循环检测后退出。
        """
        self._stop_event.set()
