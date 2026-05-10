# Context Loader Filter Rules — Safety Floor 件 1 第 3 层防御

> **声明式规则**(非可执行脚本) — 用于 Claude Code agent context loader / .claude/settings.json permissions / IDE plugin。
> per ideababy_stroller framework/SHARED-CONTRACT.md §1 第 1 件
>
> **注意**:本文件是**约束声明**(给 agent context loader 实装方读),**不是可调脚本**。具体实装由 .claude/settings.json + Claude Code agent context loader 完成。

## 三层防御架构

| 层 | 实装位置 | 实装文件 |
|---|---|---|
| 第 1 层:文件系统扫描 | `scan-credentials.sh`(本目录) | scan-credentials.sh |
| 第 2 层:git pre-commit | `pre-commit-credential.sh`(本目录) | pre-commit-credential.sh |
| 第 3 层:agent context loader | `.claude/settings.json` permissions.deny | 本文件 documentation |

## 第 3 层规则(给 .claude/settings.json 实装方)

### permissions.deny 必填项

XenoDev `.claude/settings.json` 必须含以下 deny 规则:

```json
{
  "permissions": {
    "deny": [
      "Read(.env.production)",
      "Read(.env.production.*)",
      "Read(.env.prod)",
      "Read(.env.prod.*)",
      "Read(.env.local)",
      "Read(secrets/production/**)",
      "Read(secrets/prod/**)",
      "Bash(cat .env.production*)",
      "Bash(cat .env.prod*)",
      "Bash(cat secrets/production/*)",
      "Bash(grep .* .env.production*)",
      "Bash(grep .* secrets/production/*)"
    ]
  }
}
```

### 为什么 3 层都需要

- **第 1 层**(文件系统扫描):defensive — operator 不小心 cp/mv production env 文件到 repo,本层兜底
- **第 2 层**(git pre-commit):防 commit 进 history(unrecoverable;`git filter-repo` 是噩梦)
- **第 3 层**(agent context loader):防 LLM agent 读到 production secret 后写到日志 / 决策过程 / hand-back 包

任何一层失效 = 凭据泄露;3 层 defense in depth 是行业最佳实践(NIST 800-53 / OWASP Cheat Sheet)。

## 失败案例(为何此 3 层必装)

- **Cursor + Claude 9 秒删库**(tomshardware 2025) — agent 读到 prod credentials 后跑了 destructive query
- **Yale 学生 GPT-4 误投递 prod API key**(2025) — context loader 未拦截
- **多次 chat-leak 真实事件**:agent 在 chat completion 中暴露 production env 字串

## XenoDev 装机 checklist

operator 在 XenoDev 起跑后:
1. `bash .claude/safety-floor/credential-isolation/scan-credentials.sh .` 应 exit 0
2. `git status --untracked-files=all` 应不含 `.env.production*` / `secrets/production/*`(除 `.fake` 后缀)
3. `.claude/settings.json` 含本文件 permissions.deny 规则
4. 若用 lefthook,`lefthook.yml` pre-commit 注册 pre-commit-credential.sh

## 与 SHARED-CONTRACT 的关系

- **SSOT 在 IDS** `framework/SHARED-CONTRACT.md` §1 第 1 件 + §2 件 1
- 本文件是 XenoDev 端的实装规则 + 实装清单
- IDS 不直接跑本规则(IDS M2 cutover 后不 build,无 production secret 风险);但 XenoDev 跑 build,必装 3 层

## OQ(本 kit 不解决的)

- **OQ-credential-1**:operator OS-level vs application-level secret store 选择(eg macOS Keychain / 1Password CLI / age encrypted)— v0.2 决,由 operator dev workflow 偏好
- **OQ-credential-2**:CI 环境的 secret 注入方式(GitHub Actions secrets / Vault)— XenoDev v0.1 不跑 CI,不在范围
