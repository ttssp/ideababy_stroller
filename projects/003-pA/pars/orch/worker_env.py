"""
pars.orch.worker_env — Worker subprocess env builder。

安全契约(C15 / R4):
  - 默认 deny-all：新 env 从空 dict 开始，不继承 host env
  - 显式允许（白名单）：WHITELIST_FROM_HOST 中列出的 key 从 host_env 复制（若存在）
  - 显式注入：ANTHROPIC_BASE_URL（指向 localhost proxy）/ RECALLKIT_RUN_ID /
            HF_TOKEN（仅 config.hf_token 不为 None 时注入）
  - 黑名单最终扫描：任何 key 命中 BLACKLIST_PATTERNS → raise ValueError（绝不沉默）

Known key patterns（黑名单正则，按从严到宽顺序）：
  - ANTHROPIC_API_KEY（具名，最严格）
  - *_API_KEY, *_TOKEN, *_SECRET, *_PASSWORD, *_CREDENTIALS（通配后缀）
  - AWS_*, GCP_*, AZURE_*（云 credentials 前缀）
  - ANTHROPIC_*（通用 ANTHROPIC 前缀，ANTHROPIC_BASE_URL 例外）

设计决策（case sensitivity）：
  - 黑名单正则均对大写进行匹配（POSIX env var 约定大写）
  - 小写 key（如 anthropic_api_key）不是同一个 env var，不匹配黑名单
  - 生产路径永远只使用大写 env var；小写 key 如出现应视为编程错误而非安全逃逸
  - 此设计在 docstring 中明示，测试 test_lowercase_key_not_treated_as_secret 验证

fail-safe 原则：
  - 若出 bug，宁可 worker env 太干净跑不起来，也不可 leak key
  - build_worker_env 最后一步必做黑名单扫描，即使 extra_injected 含 key 也会被捕获
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

from pars.logging import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# 白名单：允许从 host env 复制的 key（明确的安全 key）
# ---------------------------------------------------------------------------

WHITELIST_FROM_HOST: frozenset[str] = frozenset(
    {
        "PATH",
        "HOME",
        "USER",
        "LANG",
        "LC_ALL",
        "LC_CTYPE",
        "TMPDIR",
        "TMP",
        "TEMP",
        "SHELL",
        "TERM",
        "PYTHONPATH",         # 让 worker 能找到 pars 包
        "CUDA_VISIBLE_DEVICES",  # GPU 任务必需
        "HF_HOME",            # HF 缓存目录（路径，非 token）
    }
)


# ---------------------------------------------------------------------------
# 黑名单正则：匹配到任何一个就 raise ValueError
# ---------------------------------------------------------------------------

# 例外：ANTHROPIC_BASE_URL 允许；其余 ANTHROPIC_* 禁止
# 实现：先检查非例外的 ANTHROPIC_* 通配，再单独豁免 ANTHROPIC_BASE_URL
_BLACKLIST_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"^ANTHROPIC_API_KEY$"),        # 具名，最高优先
    re.compile(r"^ANTHROPIC_ADMIN_KEY$"),       # 具名
    re.compile(r".*_API_KEY$"),                 # *_API_KEY 通配
    re.compile(r".*_TOKEN$"),                   # *_TOKEN 通配（HF_TOKEN 通过白名单显式控制）
    re.compile(r".*_SECRET$"),                  # *_SECRET 通配
    re.compile(r".*_PASSWORD$"),                # *_PASSWORD 通配
    re.compile(r".*_CREDENTIALS$"),             # *_CREDENTIALS 通配
    re.compile(r"^AWS_"),                       # AWS 云 credentials 前缀
    re.compile(r"^GCP_"),                       # GCP 云 credentials 前缀
    re.compile(r"^AZURE_"),                     # Azure 云 credentials 前缀
    # ANTHROPIC_* 通配（ANTHROPIC_BASE_URL 通过例外豁免处理）
    re.compile(r"^ANTHROPIC_"),
]

# 黑名单例外：即使命中上面正则，这些 key 也允许存在
# - ANTHROPIC_BASE_URL：命中 ^ANTHROPIC_ 正则，但它是安全的（指向 localhost proxy，无 secret）
# - HF_TOKEN：命中 .*_TOKEN$ 正则，但架构允许（scope 小，仅 gated 模型下载；
#             通过 WorkerEnvConfig.hf_token 显式控制，不自动从 host 继承）
#             参考：architecture.md §5 / spec §2.1 §Safety / T011.md Known gotchas
_BLACKLIST_EXCEPTIONS: frozenset[str] = frozenset({"ANTHROPIC_BASE_URL", "HF_TOKEN"})


# ---------------------------------------------------------------------------
# 配置数据类
# ---------------------------------------------------------------------------


@dataclass
class WorkerEnvConfig:
    """Worker subprocess env 构造参数。

    字段：
        run_id           : 当前 run ULID，注入为 RECALLKIT_RUN_ID
        proxy_port       : localhost proxy 端口，构造 ANTHROPIC_BASE_URL
        hf_token         : 仅 gated 模型下载时临时注入；默认 None（公开 demo 无需）
                           用完后 orchestrator 应从状态移除（不由本模块负责清理）
        extra_allowed_keys : 额外的白名单 key，从 host_env 复制（需要确保它们不含 secret）
        extra_injected   : 额外注入的 key-value pairs（如 RECALLKIT_CKPT_DIR）
                           注意：仍会经过黑名单最终扫描，含 secret key 会 raise
    """

    run_id: str
    proxy_port: int
    hf_token: str | None = None
    extra_allowed_keys: frozenset[str] = field(default_factory=frozenset)
    extra_injected: dict[str, str] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# 核心函数
# ---------------------------------------------------------------------------


def _is_blacklisted(key: str) -> bool:
    """检查 key 是否命中黑名单正则且不在例外白名单中。

    返回 True 表示该 key 是安全威胁，应被禁止。
    """
    if key in _BLACKLIST_EXCEPTIONS:
        return False
    return any(pattern.search(key) for pattern in _BLACKLIST_PATTERNS)


def build_worker_env(
    config: WorkerEnvConfig,
    *,
    host_env: dict[str, str] | None = None,
) -> dict[str, str]:
    """构造 worker subprocess env。

    步骤（deny-all 方案）：
      1. 从空 dict 开始（不继承 host env）
      2. WHITELIST_FROM_HOST ∪ config.extra_allowed_keys 中的 key，
         若在 host_env 中存在则复制
      3. 注入 ANTHROPIC_BASE_URL=http://127.0.0.1:<proxy_port>
      4. 注入 RECALLKIT_RUN_ID=<run_id>
      5. 若 config.hf_token 不为 None，注入 HF_TOKEN
      6. 合并 config.extra_injected（后写覆盖，如 RECALLKIT_CKPT_DIR）
      7. 最终黑名单扫描：对结果 dict 每个 key 过黑名单正则
         → 若命中 raise ValueError（包含具体 key 名）

    参数：
        config   : WorkerEnvConfig 实例
        host_env : 替代 os.environ 的 env dict（用于测试隔离）；
                   None 时使用 os.environ（不 copy，只读访问）

    返回：
        干净的 worker env dict（str → str）

    Raises:
        ValueError: 发现黑名单 key（绝不沉默吞掉，fail-safe 原则）
    """
    if host_env is None:
        host_env = dict(os.environ)

    # 步骤 1：从空 dict 开始
    env: dict[str, str] = {}

    # 步骤 2：白名单 key 从 host_env 复制
    allowed_keys = WHITELIST_FROM_HOST | config.extra_allowed_keys
    for key in allowed_keys:
        if key in host_env:
            env[key] = host_env[key]

    # 步骤 3：注入 ANTHROPIC_BASE_URL（指向 localhost proxy）
    env["ANTHROPIC_BASE_URL"] = f"http://127.0.0.1:{config.proxy_port}"

    # 步骤 4：注入 RECALLKIT_RUN_ID
    env["RECALLKIT_RUN_ID"] = config.run_id

    # 步骤 5：可选注入 HF_TOKEN（仅 gated 模型下载时）
    if config.hf_token is not None:
        env["HF_TOKEN"] = config.hf_token

    # 步骤 6：合并 extra_injected（后写覆盖）
    env.update(config.extra_injected)

    # 步骤 7：最终黑名单扫描（fail-safe：即使 extra_injected 含 secret 也被捕获）
    _enforce_blacklist(env)

    logger.debug(
        "worker env built",
        extra={
            "run_id": config.run_id,
            "proxy_port": config.proxy_port,
            "env_keys": sorted(env.keys()),
        },
    )
    return env


def _enforce_blacklist(env: dict[str, str]) -> None:
    """对 env dict 的每个 key 进行黑名单扫描。

    Raises:
        ValueError: 发现黑名单 key（含具体 key 名，用于安全审计 log）
    """
    for key in env:
        if _is_blacklisted(key):
            raise ValueError(
                f"[C15/R4 SECURITY] Worker env 包含禁止的 key: '{key}'。"
                f"请勿将 API key / token / secret 注入 worker subprocess env。"
            )


def strip_key_env(env: dict[str, str]) -> dict[str, str]:
    """从任意 env dict 剥除黑名单 key，返回新 dict（原 dict 不变）。

    用途：测试辅助 + 预防性清理（如从 os.environ 粗取后再做安全清理）。
    注意：不调用 _enforce_blacklist（即不会 raise），仅静默移除。

    返回：
        不含黑名单 key 的新 dict
    """
    return {k: v for k, v in env.items() if not _is_blacklisted(k)}


def assert_no_keys(env: dict[str, str]) -> None:
    """断言 env 不含黑名单 key。生产路径在 worker 启动前必调（防御性检查）。

    与 _enforce_blacklist 的区别：
    - _enforce_blacklist：内部函数，在 build_worker_env 内使用
    - assert_no_keys：公开 API，供 orchestrator / 测试外部调用

    Raises:
        ValueError: 发现黑名单 key（含具体 key 名，方便定位问题）
    """
    for key in env:
        if _is_blacklisted(key):
            raise ValueError(
                f"[C15/R4 SECURITY] env 断言失败：发现禁止的 key '{key}'。"
                f"Worker env 不应含 API key / token / secret / cloud credentials。"
            )
