"""
alembic env.py — T002
结论: 配置 alembic 运行环境，URL 来自 config.py 或 DECISION_LEDGER_DB_URL env var
细节:
  - PRAGMA journal_mode=WAL + PRAGMA foreign_keys=ON 在每次连接时设置
  - 仅使用 raw SQL DDL（op.execute），不引入 SQLAlchemy ORM（tech-stack §1 决策）
  - DECISION_LEDGER_DB_URL env var 允许测试时传入临时 SQLite 路径
  - migration 前 pre-migration backup hook（TECH-8 需求）
"""

from __future__ import annotations

import logging
import os
import shutil
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine

# alembic Config 对象（alembic.ini 内容）
config = context.config

# 配置 Python 日志（alembic.ini [loggers] 配置）
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

logger = logging.getLogger("alembic.env")


def _get_db_url() -> str:
    """
    结论: 优先从 DECISION_LEDGER_DB_URL env var 读取（测试用），否则从 config.py 构建。
    细节:
      - 测试时通过 DECISION_LEDGER_DB_URL 传入临时 SQLite 路径，隔离测试数据
      - 生产时读 Settings.decision_ledger_home / db.sqlite
    """
    # 测试 hook: 环境变量直接覆盖
    env_url = os.environ.get("DECISION_LEDGER_DB_URL")
    if env_url:
        return env_url

    # 生产路径: 从 config.py 推导（避免循环 import）
    home = Path(os.environ.get("DECISION_LEDGER_HOME", "~/decision_ledger")).expanduser()
    return f"sqlite:///{home}/db.sqlite"


def _configure_sqlite_pragmas(engine: Engine) -> None:
    """
    结论: 每次连接设置 SQLite PRAGMA，防止并发写冲突 + 外键完整性。
    细节:
      - WAL mode: 解决 asyncio 多 task 同时读写（HTTP read + worker write）
      - foreign_keys=ON: 架构 §9 invariant — FK 约束在 SQLite 默认关闭
    """
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection: object, connection_record: object) -> None:
        cursor = dbapi_connection.cursor()  # type: ignore[attr-defined]
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def _pre_migration_backup(url: str) -> None:
    """
    结论: migration 前自动备份 db.sqlite（TECH-8 需求）。
    细节:
      - 仅在 file-based SQLite 且文件已存在时执行
      - 备份到 backups/ 目录，按 alembic revision 版本号命名
      - 测试时 db 不存在，直接跳过
    """
    if not url.startswith("sqlite:///"):
        return  # 非文件 SQLite（:memory: 等）跳过

    db_file = Path(url.removeprefix("sqlite:///"))
    if not db_file.exists():
        return  # 首次创建，无需备份

    backups_dir = db_file.parent / "backups"
    backups_dir.mkdir(parents=True, exist_ok=True)

    # 获取当前 revision 作为备份文件名后缀
    try:
        rev_head = config.get_main_option("version_locations")
        suffix = rev_head or "pre_migration"
    except Exception:
        suffix = "pre_migration"

    backup_path = backups_dir / f"db.{suffix}.bak.sqlite"
    shutil.copy2(str(db_file), str(backup_path))
    logger.info("pre-migration backup: %s → %s", db_file, backup_path)


def run_migrations_offline() -> None:
    """
    结论: offline 模式（生成 SQL 脚本，不实际连接 DB）。
    细节: 仅用于 `alembic upgrade --sql` 预览，不走 pragma hook。
    """
    url = _get_db_url()
    context.configure(
        url=url,
        target_metadata=None,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    结论: online 模式（直接连接 DB 执行 migration）。
    细节:
      - 先备份（TECH-8）
      - 创建 engine + 注册 pragma listener
      - 执行 migration
    """
    url = _get_db_url()
    _pre_migration_backup(url)

    # create_engine: 同步引擎（alembic 本身同步执行 migration）
    # aiosqlite 仅在业务运行时使用，migration 用同步 sqlite3 驱动
    connectable = create_engine(
        url,
        echo=False,
    )
    _configure_sqlite_pragmas(connectable)

    with connectable.connect() as connection:
        # PRAGMA 由 event listener 在 connect() 时设置 (见 _configure_sqlite_pragmas)
        # 不在 connection.execute 里重复执行 — 会破坏 alembic 的 transaction 状态
        # 导致 alembic_version 表写入失败 (downgrade 找不到 revision)

        context.configure(
            connection=connection,
            target_metadata=None,
            # 结论: 不使用 render_as_batch，migration 全部用 op.execute() raw DDL
            # 细节: render_as_batch 仅用于 ORM op.add_column/alter_column 场景；
            #        raw SQL DDL 下 render_as_batch=True 会干扰 DROP TABLE 事务执行
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
