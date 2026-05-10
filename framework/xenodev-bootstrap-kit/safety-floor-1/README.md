# Safety Floor 件 1 · 凭据隔离 kit

per `framework/SHARED-CONTRACT.md` §1 第 1 件 + §2 件 1。

## 目的

防止 production credentials(`.env.production*` / `secrets/production/*` / `prod://` 字串)进入:
1. agent context(LLM 读到后写到 chat / 日志 / hand-back 包)
2. git history(commit 进 history 后 unrecoverable;`git filter-repo` 噩梦)
3. 文件系统(operator 误 cp/mv production env 到 repo)

## 三层防御架构

| 层 | 文件 | 作用 |
|---|---|---|
| 第 1 层:文件系统扫描 | `scan-credentials.sh` | bash script,可手动跑 / CI 跑 |
| 第 2 层:git pre-commit | `pre-commit-credential.sh` | git hook,commit 前拦截 staged files |
| 第 3 层:agent context loader | `context-loader-filter.md` | 声明式规则,给 .claude/settings.json 实装方读 |

## 文件清单

- `README.md`(本文件)
- `scan-credentials.sh` — 第 1 层,扫文件系统
- `pre-commit-credential.sh` — 第 2 层,git pre-commit hook
- `context-loader-filter.md` — 第 3 层,声明式规则文档
- `test-fixtures/` — 测试 fixtures(全部 `.fake` 后缀,不会被本 script 检测)

## 装机(XenoDev 端,operator 跑 bootstrap.sh 后)

bootstrap.sh 已自动 cp 到 `.claude/safety-floor/credential-isolation/`。还需 operator:

1. **第 1 层** — 不需要装机,需要时手动跑:
   ```bash
   bash .claude/safety-floor/credential-isolation/scan-credentials.sh .
   ```

2. **第 2 层** — 装 git pre-commit hook:
   ```bash
   # 选项 A: symlink 到 .git/hooks/pre-commit
   ln -sf "$(pwd)/.claude/safety-floor/credential-isolation/pre-commit-credential.sh" .git/hooks/pre-commit
   chmod +x .git/hooks/pre-commit

   # 选项 B(推荐):用 lefthook
   # lefthook.yml:
   #   pre-commit:
   #     commands:
   #       credential-scan:
   #         run: bash .claude/safety-floor/credential-isolation/pre-commit-credential.sh
   ```

3. **第 3 层** — 改 `.claude/settings.json` 加 permissions.deny(见 `context-loader-filter.md`)

## 单元测试

```bash
# 应 exit 1(检测出 .env.production.fake → 但因有 .fake 后缀实际跳过 → 因有 secrets/production/api-key.fake 跳过)
# 实际:test-fixtures/ 下全部 .fake,scan 应 exit 0
bash framework/xenodev-bootstrap-kit/safety-floor-1/scan-credentials.sh \
  framework/xenodev-bootstrap-kit/safety-floor-1/test-fixtures/

# 模拟真泄露(cp .fake 去 .fake 后缀):
TMPDIR="$(mktemp -d)"
cp framework/xenodev-bootstrap-kit/safety-floor-1/test-fixtures/.env.production.fake "$TMPDIR/.env.production"
bash framework/xenodev-bootstrap-kit/safety-floor-1/scan-credentials.sh "$TMPDIR"
# 应 exit 1 + stderr 报 .env.production
rm -rf "$TMPDIR"

# 空目录 — 应 exit 0
bash framework/xenodev-bootstrap-kit/safety-floor-1/scan-credentials.sh /tmp
```

## 失败模式参考

- **Cursor + Claude 9 秒删库**(tomshardware 2025):agent 读到 prod credentials → 跑 destructive query
- **Yale GPT-4 prod API key 泄露**(2025):context loader 未拦
- **chat-leak 真实事件**(多次):agent 在 chat completion 中暴露 production env 字串

## OQ

- **OQ-credential-1**:operator OS-level vs application-level secret store(macOS Keychain / 1Password / age)— v0.2 由 operator dev workflow 决
- **OQ-credential-2**:CI secret 注入方式 — XenoDev v0.1 不跑 CI,不在范围
