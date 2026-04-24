"""
tests.unit.test_worker_env — Worker subprocess env builder 严苛测试。

覆盖 R4 API key exfil 攻击面 + C15 硬约束。

TDD 顺序：先写测试（红），实现后全绿。
"""

from __future__ import annotations

import pytest

from pars.orch.worker_env import (
    WorkerEnvConfig,
    assert_no_keys,
    build_worker_env,
    strip_key_env,
)


# ---------------------------------------------------------------------------
# 工具函数：构造受控 host_env
# ---------------------------------------------------------------------------


def _clean_host() -> dict[str, str]:
    """最小干净 host env：仅含白名单安全字段。"""
    return {
        "PATH": "/usr/bin:/bin",
        "HOME": "/home/testuser",
        "USER": "testuser",
        "LANG": "en_US.UTF-8",
    }


def _dirty_host() -> dict[str, str]:
    """含多种 key/secret 的污染 host env，用于验证剥离能力。"""
    base = _clean_host()
    base.update(
        {
            "ANTHROPIC_API_KEY": "sk-ant-test-secret",
            "ANTHROPIC_ADMIN_KEY": "sk-ant-admin-secret",
            "OPENAI_API_KEY": "sk-openai-secret",
            "HF_TOKEN": "hf_test_token",
            "MY_CUSTOM_TOKEN": "custom_token_value",
            "AWS_ACCESS_KEY_ID": "AKIASECRET",
            "AWS_SECRET_ACCESS_KEY": "aws_secret",
            "GCP_SERVICE_ACCOUNT_KEY": "gcp_key",
            "AZURE_CLIENT_SECRET": "azure_secret",
            "DB_PASSWORD": "db_pass",
            "GITHUB_TOKEN": "ghp_token",
        }
    )
    return base


# ---------------------------------------------------------------------------
# 基础：ANTHROPIC_API_KEY 剥除
# ---------------------------------------------------------------------------


def test_anthropic_api_key_stripped_from_host():
    """测试 1：host env 有 ANTHROPIC_API_KEY → worker env 不含。"""
    host = _clean_host()
    host["ANTHROPIC_API_KEY"] = "sk-ant-test-secret"

    cfg = WorkerEnvConfig(run_id="01HXYZ", proxy_port=8123)
    env = build_worker_env(cfg, host_env=host)

    assert "ANTHROPIC_API_KEY" not in env, "ANTHROPIC_API_KEY 不能出现在 worker env 中"


def test_anthropic_admin_key_stripped():
    """测试 2：host env 有 ANTHROPIC_ADMIN_KEY → worker env 不含（具名黑名单）。"""
    host = _clean_host()
    host["ANTHROPIC_ADMIN_KEY"] = "sk-ant-admin-key"

    cfg = WorkerEnvConfig(run_id="01HXYZ", proxy_port=8123)
    env = build_worker_env(cfg, host_env=host)

    assert "ANTHROPIC_ADMIN_KEY" not in env, "ANTHROPIC_ADMIN_KEY 不能出现在 worker env 中"


# ---------------------------------------------------------------------------
# HF_TOKEN 行为：默认不传入，显式注入才可
# ---------------------------------------------------------------------------


def test_hf_token_not_in_worker_by_default():
    """测试 3：host env 有 HF_TOKEN → 默认 worker env 不含（必须显式 hf_token= 注入）。"""
    host = _clean_host()
    host["HF_TOKEN"] = "hf_from_host"  # noqa: S105

    cfg = WorkerEnvConfig(run_id="01HXYZ", proxy_port=8123)
    env = build_worker_env(cfg, host_env=host)

    assert "HF_TOKEN" not in env, (
        "HF_TOKEN 必须由 WorkerEnvConfig.hf_token 显式注入，"
        "不能自动从 host env 继承"
    )


def test_hf_token_explicitly_injected():
    """测试 4：WorkerEnvConfig(hf_token=...) 才能把 HF_TOKEN 注入 worker env。"""
    host = _clean_host()
    cfg = WorkerEnvConfig(run_id="01HXYZ", proxy_port=8123, hf_token="hf_explicit_token")  # noqa: S106
    env = build_worker_env(cfg, host_env=host)

    assert env.get("HF_TOKEN") == "hf_explicit_token", (
        "显式注入的 HF_TOKEN 必须出现在 worker env 中"
    )


# ---------------------------------------------------------------------------
# 10 种不同命名的 key 全被剥除
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "key_name,key_value",
    [
        ("ANTHROPIC_API_KEY", "sk-ant-secret"),
        ("OPENAI_API_KEY", "sk-openai-secret"),
        ("HF_TOKEN", "hf_token_val"),
        ("MY_CUSTOM_TOKEN", "custom_token"),
        ("AWS_ACCESS_KEY_ID", "AKIASECRET"),
        ("AWS_SECRET_ACCESS_KEY", "aws_secret"),
        ("GCP_SERVICE_ACCOUNT_CREDENTIALS", "gcp_creds_json"),
        ("AZURE_CLIENT_SECRET", "azure_secret"),
        ("DB_PASSWORD", "db_pass"),
        ("GITHUB_TOKEN", "ghp_token"),
    ],
)
def test_all_secret_keys_stripped(key_name: str, key_value: str):
    """测试 5：10 种不同命名的 key 全部不出现在 worker env 中。"""
    host = _clean_host()
    host[key_name] = key_value

    cfg = WorkerEnvConfig(run_id="01HXYZ", proxy_port=8123)
    env = build_worker_env(cfg, host_env=host)

    assert key_name not in env, f"{key_name} 不能出现在 worker env 中（黑名单规则）"


# ---------------------------------------------------------------------------
# ANTHROPIC_BASE_URL 必须注入
# ---------------------------------------------------------------------------


def test_anthropic_base_url_injected():
    """测试 6：build_worker_env 返回 ANTHROPIC_BASE_URL=http://127.0.0.1:<port>。"""
    cfg = WorkerEnvConfig(run_id="01HXYZ", proxy_port=8123)
    env = build_worker_env(cfg, host_env=_clean_host())

    assert env.get("ANTHROPIC_BASE_URL") == "http://127.0.0.1:8123", (
        f"ANTHROPIC_BASE_URL 应为 http://127.0.0.1:8123，实际得到 {env.get('ANTHROPIC_BASE_URL')}"
    )


def test_anthropic_base_url_uses_correct_port():
    """测试 7：不同 proxy_port 值都能正确反映在 ANTHROPIC_BASE_URL 中。"""
    cfg = WorkerEnvConfig(run_id="01HXYZ", proxy_port=9999)
    env = build_worker_env(cfg, host_env=_clean_host())

    assert env["ANTHROPIC_BASE_URL"] == "http://127.0.0.1:9999"


# ---------------------------------------------------------------------------
# RECALLKIT_RUN_ID 必须注入
# ---------------------------------------------------------------------------


def test_recallkit_run_id_injected():
    """测试 8：build_worker_env 返回包含 RECALLKIT_RUN_ID=<run_id>。"""
    cfg = WorkerEnvConfig(run_id="01HABCDEF", proxy_port=8123)
    env = build_worker_env(cfg, host_env=_clean_host())

    assert env.get("RECALLKIT_RUN_ID") == "01HABCDEF", (
        f"RECALLKIT_RUN_ID 应为 '01HABCDEF'，实际得到 {env.get('RECALLKIT_RUN_ID')}"
    )


# ---------------------------------------------------------------------------
# extra_allowed_keys 与 extra_injected 功能
# ---------------------------------------------------------------------------


def test_extra_allowed_keys_copies_custom_key():
    """测试 9：extra_allowed_keys 能让白名单以外的自定义 key 从 host 复制。"""
    host = _clean_host()
    host["MY_CUSTOM_PATH"] = "/custom/path"

    cfg = WorkerEnvConfig(
        run_id="01HXYZ",
        proxy_port=8123,
        extra_allowed_keys=frozenset({"MY_CUSTOM_PATH"}),
    )
    env = build_worker_env(cfg, host_env=host)

    assert env.get("MY_CUSTOM_PATH") == "/custom/path", (
        "extra_allowed_keys 中声明的 key 应从 host env 复制"
    )


def test_extra_injected_adds_key_value():
    """测试 10：extra_injected 能将任意键值注入 worker env（非黑名单 key）。"""
    cfg = WorkerEnvConfig(
        run_id="01HXYZ",
        proxy_port=8123,
        extra_injected={"FOO": "bar", "RECALLKIT_CKPT_DIR": "/tmp/ckpt"},
    )
    env = build_worker_env(cfg, host_env=_clean_host())

    assert env.get("FOO") == "bar"
    assert env.get("RECALLKIT_CKPT_DIR") == "/tmp/ckpt"


# ---------------------------------------------------------------------------
# 黑名单绕过：extra_injected 含 key pattern → 必须 raise
# ---------------------------------------------------------------------------


def test_extra_injected_with_blacklisted_key_raises():
    """测试 11：extra_injected={"SNEAKY_TOKEN": "..."} → 必须 raise ValueError（黑名单在 extra 之后扫描，不可被绕过）。"""
    cfg = WorkerEnvConfig(
        run_id="01HXYZ",
        proxy_port=8123,
        extra_injected={"SNEAKY_TOKEN": "leaked_value"},
    )
    with pytest.raises(ValueError, match="SNEAKY_TOKEN"):
        build_worker_env(cfg, host_env=_clean_host())


def test_extra_injected_with_api_key_raises():
    """测试 12：extra_injected 注入 ANTHROPIC_API_KEY → 必须 raise ValueError。"""
    cfg = WorkerEnvConfig(
        run_id="01HXYZ",
        proxy_port=8123,
        extra_injected={"ANTHROPIC_API_KEY": "sk-ant-bypassed"},
    )
    with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
        build_worker_env(cfg, host_env=_clean_host())


# ---------------------------------------------------------------------------
# ANTHROPIC_BASE_URL 例外：其他 ANTHROPIC_* 被黑
# ---------------------------------------------------------------------------


def test_anthropic_base_url_is_whitelisted_exception():
    """测试 13：ANTHROPIC_BASE_URL 是例外，必须出现在 worker env 中（其他 ANTHROPIC_* 全黑）。"""
    cfg = WorkerEnvConfig(run_id="01HXYZ", proxy_port=8123)
    env = build_worker_env(cfg, host_env=_clean_host())

    # ANTHROPIC_BASE_URL 必须存在
    assert "ANTHROPIC_BASE_URL" in env
    # ANTHROPIC_API_KEY / ANTHROPIC_ADMIN_KEY 等不存在
    for key in list(env.keys()):
        if key.startswith("ANTHROPIC_") and key != "ANTHROPIC_BASE_URL":
            pytest.fail(f"发现意外的 ANTHROPIC_* key: {key}")


def test_extra_injected_anthropic_base_url_ok():
    """测试 14：extra_injected 覆盖 ANTHROPIC_BASE_URL（允许，该 key 在例外白名单）。"""
    cfg = WorkerEnvConfig(
        run_id="01HXYZ",
        proxy_port=8123,
        extra_injected={"ANTHROPIC_BASE_URL": "http://127.0.0.1:9000"},
    )
    # ANTHROPIC_BASE_URL 不是黑名单 key，不应 raise
    env = build_worker_env(cfg, host_env=_clean_host())
    # 结果取 extra_injected 的值（后写覆盖）
    assert env["ANTHROPIC_BASE_URL"] == "http://127.0.0.1:9000"


# ---------------------------------------------------------------------------
# 空 host_env 不 crash
# ---------------------------------------------------------------------------


def test_empty_host_env_does_not_crash():
    """测试 15：空 host_env={} 不 crash，ANTHROPIC_BASE_URL 和 RECALLKIT_RUN_ID 仍然存在。"""
    cfg = WorkerEnvConfig(run_id="01HEMPTY", proxy_port=8000)
    env = build_worker_env(cfg, host_env={})

    assert "ANTHROPIC_BASE_URL" in env
    assert env["RECALLKIT_RUN_ID"] == "01HEMPTY"
    assert "ANTHROPIC_API_KEY" not in env


# ---------------------------------------------------------------------------
# assert_no_keys 功能验证
# ---------------------------------------------------------------------------


def test_assert_no_keys_raises_on_api_key():
    """测试 16：assert_no_keys 对含 ANTHROPIC_API_KEY 的 env raise ValueError 并含 key 名。"""
    dirty_env = {"ANTHROPIC_API_KEY": "sk-ant-secret", "PATH": "/bin"}
    with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
        assert_no_keys(dirty_env)


def test_assert_no_keys_raises_on_token():
    """测试 17：assert_no_keys 对含 MY_TOKEN 的 env raise ValueError 并含 key 名。"""
    dirty_env = {"MY_TOKEN": "secret", "HOME": "/home/user"}
    with pytest.raises(ValueError, match="MY_TOKEN"):
        assert_no_keys(dirty_env)


def test_assert_no_keys_passes_on_clean_env():
    """测试 18：assert_no_keys 对干净 env 不抛（包含 ANTHROPIC_BASE_URL 例外）。"""
    clean_env = {
        "PATH": "/usr/bin:/bin",
        "HOME": "/home/user",
        "ANTHROPIC_BASE_URL": "http://127.0.0.1:8123",
        "RECALLKIT_RUN_ID": "01HXYZ",
    }
    # 不应 raise
    assert_no_keys(clean_env)


# ---------------------------------------------------------------------------
# strip_key_env 功能验证
# ---------------------------------------------------------------------------


def test_strip_key_env_removes_multiple_keys():
    """测试 19：strip_key_env 从多重 key env 全部剥除黑名单 key，返回新 dict。

    注意：HF_TOKEN 在黑名单例外中（架构允许通过 WorkerEnvConfig.hf_token 显式注入），
    因此 strip_key_env 不会剥除它。
    HF_TOKEN 的安全控制通过 build_worker_env 的 deny-all 设计实现：
    host env 的 HF_TOKEN 不会被自动复制（必须显式传入 WorkerEnvConfig.hf_token）。
    """
    env = _dirty_host()
    stripped = strip_key_env(env)

    # 这些都命中黑名单正则且不在例外列表，全应被剥除
    for blacklisted in [
        "ANTHROPIC_API_KEY",
        "ANTHROPIC_ADMIN_KEY",
        "OPENAI_API_KEY",
        "MY_CUSTOM_TOKEN",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "GCP_SERVICE_ACCOUNT_KEY",
        "AZURE_CLIENT_SECRET",
        "DB_PASSWORD",
        "GITHUB_TOKEN",
    ]:
        assert blacklisted not in stripped, f"{blacklisted} 应被 strip_key_env 剥除"

    # 普通 env 应保留
    assert "PATH" in stripped
    assert "HOME" in stripped

    # HF_TOKEN 是例外（不在黑名单），strip 不剥除
    # 但 build_worker_env 通过 deny-all 保证 host HF_TOKEN 不会自动进入 worker env
    # （需通过 WorkerEnvConfig.hf_token 显式注入）
    assert "HF_TOKEN" in stripped  # strip_key_env 不会剥除例外 key


def test_strip_key_env_returns_new_dict():
    """测试 20：strip_key_env 返回新 dict，不修改原 dict。"""
    env = {"ANTHROPIC_API_KEY": "sk-ant-test", "PATH": "/bin"}
    original_keys = set(env.keys())
    stripped = strip_key_env(env)

    # 原始 dict 未被修改
    assert set(env.keys()) == original_keys
    # 返回的是新 dict
    assert stripped is not env


# ---------------------------------------------------------------------------
# CUDA_VISIBLE_DEVICES 在白名单（GPU 任务必需）
# ---------------------------------------------------------------------------


def test_cuda_visible_devices_in_whitelist():
    """测试 21：CUDA_VISIBLE_DEVICES 在白名单，能从 host env 复制到 worker env。"""
    host = _clean_host()
    host["CUDA_VISIBLE_DEVICES"] = "0,1"

    cfg = WorkerEnvConfig(run_id="01HXYZ", proxy_port=8123)
    env = build_worker_env(cfg, host_env=host)

    assert env.get("CUDA_VISIBLE_DEVICES") == "0,1", (
        "CUDA_VISIBLE_DEVICES 必须在白名单中，GPU 任务需要该字段"
    )


# ---------------------------------------------------------------------------
# 大写敏感性说明：env var 均大写（POSIX 约定），黑名单按大写精确匹配
# ---------------------------------------------------------------------------


def test_lowercase_key_not_treated_as_secret():
    """测试 22：小写的 anthropic_api_key 不被黑名单匹配（POSIX env var 约定大写）。

    设计决策：env var 在 POSIX 中大小写敏感，生产代码里所有 key 均大写。
    小写 key 不在黑名单模式（黑名单正则用大写），因此不被剥除。
    这是正确行为：POSIX env 不存在小写的 ANTHROPIC_API_KEY 场景。
    """
    host = _clean_host()
    host["anthropic_api_key"] = "lowercase_should_not_match"

    cfg = WorkerEnvConfig(
        run_id="01HXYZ",
        proxy_port=8123,
        extra_allowed_keys=frozenset({"anthropic_api_key"}),  # 显式放行才能进入
    )
    env = build_worker_env(cfg, host_env=host)

    # 小写 key 不匹配黑名单正则（正则均针对大写），不应被拦截（也不会自动加入白名单）
    # 但注意：若 extra_allowed_keys 允许则会被复制进来
    # 测试的关键点是：大写的 ANTHROPIC_API_KEY 才应被黑名单捕获，小写不是同一个 env var
    # 如果小写进来了（通过 extra_allowed_keys）且不被黑名单拦截：这是正确行为
    # 生产路径永远不应该用小写 env var
    assert "anthropic_api_key" in env  # 通过 extra_allowed_keys 进来
    # 大写的绝对不存在（从未注入）
    assert "ANTHROPIC_API_KEY" not in env


# ---------------------------------------------------------------------------
# 完整的 dirty host env 场景端到端验证
# ---------------------------------------------------------------------------


def test_full_dirty_host_produces_clean_worker_env():
    """测试 23：完整 dirty host env → worker env 全无黑名单 key + 含必要注入字段。"""
    host = _dirty_host()
    host["CUDA_VISIBLE_DEVICES"] = "0"
    host["PYTHONPATH"] = "/project/src"

    cfg = WorkerEnvConfig(run_id="01HFULL", proxy_port=7777)
    env = build_worker_env(cfg, host_env=host)

    # 黑名单全无
    assert_no_keys(env)

    # 必要字段存在
    assert env["ANTHROPIC_BASE_URL"] == "http://127.0.0.1:7777"
    assert env["RECALLKIT_RUN_ID"] == "01HFULL"
    assert env["CUDA_VISIBLE_DEVICES"] == "0"
    assert env["PYTHONPATH"] == "/project/src"

    # 白名单基本字段存在
    assert "PATH" in env
    assert "HOME" in env
