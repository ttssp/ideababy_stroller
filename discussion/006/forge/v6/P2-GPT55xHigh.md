# Forge v6 · 006 · P2 · GPT55xHigh · 参照系评估(with search)

**Timestamp**: 2026-07-02T08:56:35Z
**Searches run**: 4 query attempts + 8 official-source opens, SOTA-benchmark
**Visibility**: 我已读对方 P1。

## 1. SOTA 对标

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| KG-26/27 | 12-Factor config | 会随部署/机器变的值放环境,不放代码常量 | mac 绝对路径写进模板/SKILL | 路径事实应由 env/生成时/运行时注入,不是字面默认 | https://12factor.net/config |
| KG-26/30 | Git repo-root 解析 | `git rev-parse --show-toplevel` 给当前 worktree 顶层绝对路径 | 依赖当前 cwd 与相对 `tests/` | 仓根/子项目边界应运行时解析 | https://git-scm.com/docs/git-rev-parse |
| KG-27 | SemVer + version sort | 版本有语义;GNU `sort -V` 做自然版本排序 | 多处钉 `1.0.3`;spec-writer 用 glob+sort | 推广“不钉死目录版本”,但注意 `sort -V` 是 GNU coreutils,mac 便携性要核 | https://semver.org/ ; https://www.gnu.org/software/coreutils/manual/html_node/Version-sort-overview.html |
| KG-28 | uv indexes | uv 支持 `[[tool.uv.index]]`,`--default-index`,`UV_DEFAULT_INDEX`;凭据不进 lock | 手工临时 `UV_INDEX_URL` 绕过 pypi 不通 | mirror/index 应成为显式 env 或项目配置,不靠人肉记忆 | https://docs.astral.sh/uv/concepts/indexes/ |
| KG-28 | uv sync/lock + PEP 592 | lock/sync 分开;PEP 592 允许 yanked 文件继续服务精确 pin/lock,但新解析应避开 | backlog 倾向“去 --locked” | 修正:不要无脑去锁;先 preflight,需更新时显式 `uv lock`/受控 sync,保留可复现性 | https://docs.astral.sh/uv/concepts/projects/sync/ ; https://peps.python.org/pep-0592/ |
| KG-29 | OWASP path traversal | known-good 输入、避免用户提供完整路径、normalize/containment | `-p` 仅放宽字母;仍有 basename+realpath containment | P1 keep 站住;无 SOTA 反例推翻 | https://owasp.org/www-community/attacks/Path_Traversal |
| KG-26/27/28 | XDG Base Directory | 用 env 定义搜索/写入基目录;相对 env path 视为 invalid | 插件/cache 路径写死 `/Users/admin` | `$HOME`/`$CODEX_HOME`/XDG 类入口优于机器绝对路径 | https://specifications.freedesktop.org/basedir-spec/latest/ |
| 防再漂移 | pre-commit | hook 在 commit 前自动跑;可本地/CI 跑全量 | 现在无硬编码回归 gate | 单人双机用轻量 grep/pre-commit gate 足够,不必上重 CI | https://pre-commit.com/ |

## 2. 用户外部材料消化

K 无额外 URL。双方 P1 的实际差异很小:5 条 KG 评分一致(KG-26/27/30 refactor,KG-28 new,KG-29 keep)。Opus P1 更强调“KG-27 的 glob 范式已在 spec-writer 内存在,应推广”;我同意,但 SOTA 补了一个 caveat:`sort -V` 是 GNU coreutils 能力,若 mac 默认不可用,需要便携替代或明确依赖。双方都把核心不确定点落在“环境事实住哪层”和“防再漂移守卫”。

## 3. 修正后的视角

- P1 “KG-26/27 应 refactor” → **站住并深化**:12-Factor/XDG 都支持“变的环境事实外置”;Git 支持运行时取 repo root。所以推荐方向不是单一层,而是:跨机器路径用 env/生成时推断,仓内路径用运行时 repo-root。
- P1 “KG-27 glob+sort 可推广” → **部分深化**:不钉 `1.0.3` 站住;但 `sort -V` 便携性需验证,否则会制造新 mac/linux 分歧。
- P1 “KG-28 new preflight” → **站住且修正**:SOTA 不支持简单“去 --locked”。yanked dep 应触发受控 lock 更新/显式 sync 策略;mirror/index 应显式配置或 env 化。
- P1 “KG-29 keep” → **站住**:OWASP 支持 known-good 字符集 + containment;当前放宽只加字母,负例仍被多层拒。
- P1 “KG-30 refactor” → **站住**:Git repo-root 锚定说明 log 落点应绑定 XenoDev 仓根,而不是 task cwd。
