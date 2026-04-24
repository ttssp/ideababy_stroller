#!/usr/bin/env bash
# pre_pip_install.sh · T015 · R5 pip 供应链防御
#
# 职责：拦截 Claude Code Bash tool 中的 pip/uv 安装命令，
#       仅放行符合 architecture §7 三条等价白名单的命令。
#
# stdin: Claude Code 传入 JSON:
#   {"tool": {"name": "Bash"}, "input": {"command": "pip install ..."}}
#
# exit 0 → allow（Claude Code 规范）
# exit 2 → deny（Claude Code 规范：非 0 = deny；exit 2 是约定值）
#
# 实现策略：
#   - shell 侧保持最小逻辑（仅 JSON 解析 + pip/uv 前缀过滤）
#   - 真实决策委托给 pars.safety.pip_policy（Python 可单测，纯函数）
#
# 白名单（architecture §7 · 唯一真相源）：
#   A. pip install -r requirements-locked.txt --require-hashes
#   B. uv pip install -r requirements-locked.txt --require-hashes
#   C. uv sync --frozen
#
# 关联任务：T015 · 依赖：T002（requirements-locked.txt）· T012（hook 框架）

set -euo pipefail

# ---------------------------------------------------------------------------
# 读取 stdin JSON（Claude Code hook 协议）
# ---------------------------------------------------------------------------
input="$(cat)"

# 提取 command 字段（支持两种 JSON 结构）
# 结构1：{"tool": {"name": "Bash"}, "input": {"command": "..."}}
# 结构2：{"input": {"command": "..."}}（T012 stub 兼容格式）
cmd=$(echo "$input" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    # 尝试两种路径
    cmd = (data.get('input') or {}).get('command', '')
    if not cmd:
        cmd = data.get('command', '')
    print(cmd)
except Exception:
    print('')
" 2>/dev/null || echo "")

# ---------------------------------------------------------------------------
# 快速过滤：非 pip/uv 开头的命令直接放行
# pre_tool_use.sh 在更高层处理其他 deny 清单（如 rm -rf / curl）
# ---------------------------------------------------------------------------
if ! echo "$cmd" | grep -qE '^[[:space:]]*(pip[0-9.]?|uv)[[:space:]]'; then
    echo "[pre_pip_install] SKIP (not pip/uv): ${cmd:0:80}" >&2
    exit 0
fi

# ---------------------------------------------------------------------------
# 调用 Python 策略判决
# 通过临时文件在子进程中安全传递决策结果（避免 $() 内 stderr 重定向问题）
# pars.safety.pip_policy.is_pip_install_allowed 是纯函数，可单独测试
# ---------------------------------------------------------------------------
_tmpfile=$(mktemp /tmp/pre_pip_install_result_XXXXXX)
trap 'rm -f "$_tmpfile"' EXIT

python3 -c "
import sys, os, pathlib

# 确保能 import pars（hook 在 worker cwd 下运行，需含项目根）
# 优先使用 PYTHONPATH（测试 fixture 注入），其次自动查找
extra_path = os.environ.get('PYTHONPATH', '')
if extra_path:
    for p in extra_path.split(':'):
        if p and p not in sys.path:
            sys.path.insert(0, p)

# 自动从 cwd 向上查找 pars 包（生产路径，worker 的 cwd = worktree）
cwd = pathlib.Path.cwd()
for candidate in [cwd, cwd.parent, cwd.parent.parent]:
    if (candidate / 'pars' / 'safety' / 'pip_policy.py').exists():
        if str(candidate) not in sys.path:
            sys.path.insert(0, str(candidate))
        break

try:
    from pars.safety.pip_policy import is_pip_install_allowed, evaluate_pip_command, format_denial_message
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    ok, reason = is_pip_install_allowed(cmd)
    if ok:
        print('ALLOW', file=sys.stderr)
        sys.exit(0)
    else:
        # 生成完整 deny 消息（含替代建议），写到 stderr 供 shell 打印
        result = evaluate_pip_command(cmd)
        msg = format_denial_message(result, cmd)
        print(msg, file=sys.stderr)
        sys.exit(2)
except ImportError as e:
    # pars.safety.pip_policy 不可 import → fail-closed
    print(f'[pre_pip_install] DENIED: import error: {e}', file=sys.stderr)
    sys.exit(2)
" "$cmd"

python_exit=$?

if [[ $python_exit -eq 0 ]]; then
    echo "[pre_pip_install] ALLOW: ${cmd:0:120}" >&2
    exit 0
else
    echo "[pre_pip_install] DENIED pip/uv command (see above for details)" >&2
    exit 2
fi
