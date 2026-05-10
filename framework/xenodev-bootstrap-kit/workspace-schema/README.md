# Workspace Schema 4 字段 validator

per `framework/SHARED-CONTRACT.md` §6.2 + workspace-schema.json。

## 4 字段(per §6.2 normative)

| 字段 | 类型 | 必填 | 含义 |
|---|---|---|---|
| `source_repo` | absolute path | ✅ | PRD 源仓(IDS 仓路径) |
| `build_repo` | absolute path | ✅ | build 目标仓(XenoDev 仓路径) |
| `working_repo` | absolute path | ✅ | 当前 operator 所在仓 |
| `handback_target` | absolute path | ✅ | hand-back 包写回路径 |

## 文件清单

- `README.md`(本文件)
- `workspace-schema.json` — formal JSON schema(SSOT)
- `extract.sh` — 从 hand-off/hand-back 包 frontmatter 提 workspace 块(awk)
- `validate.sh` — bash 校验 4 字段全填 + absolute path
- `test-fixtures/` — 4 测试 fixtures(1 valid + 3 invalid)

## 装机(XenoDev 端,operator bootstrap.sh 后)

bootstrap.sh 已自动 cp 到 `lib/workspace-schema/`。

## 实装策略(单人 dev 环境)

- **首选**:`workspace-schema.json` 是 formal JSON schema(SSOT,B2.2 起跑后若装 npm + ajv 可直接调)
- **退化**:`validate.sh` 用 grep + bash 校验,不依赖 ajv / npm install — 单人 dev 环境零依赖
- **未来 v0.2**:可加 `validate.py`(用 jsonschema lib)+ `validate.js`(用 ajv)双语言版本

## 单元测试

```bash
# 测试 1: valid handoff(应 exit 0)
bash framework/xenodev-bootstrap-kit/workspace-schema/validate.sh \
  framework/xenodev-bootstrap-kit/workspace-schema/test-fixtures/valid-handoff.md
# 期望: exit 0

# 测试 2: 缺字段(应 exit 1)
bash framework/xenodev-bootstrap-kit/workspace-schema/validate.sh \
  framework/xenodev-bootstrap-kit/workspace-schema/test-fixtures/invalid-missing-field.md
# 期望: exit 1 + stderr 报 working_repo missing

# 测试 3: 非 absolute path(应 exit 1)
bash framework/xenodev-bootstrap-kit/workspace-schema/validate.sh \
  framework/xenodev-bootstrap-kit/workspace-schema/test-fixtures/invalid-relative-path.md
# 期望: exit 1 + stderr 报 source_repo not absolute

# 测试 4: 缺 workspace 块(应 exit 1)
bash framework/xenodev-bootstrap-kit/workspace-schema/validate.sh \
  framework/xenodev-bootstrap-kit/workspace-schema/test-fixtures/invalid-no-workspace-block.md
# 期望: exit 1 + stderr 报 no workspace block found
```

## 与 §6.2.1 6 约束 validator 的关系

- `workspace-schema/validate.sh` 校验 **4 字段结构**(必填 + absolute path)
- `handback-validator/validate-handback.sh` 校验 **6 约束语义**(canonical-path containment / symlink reject / repo identity / id consistency / id charset + final-path / hard-fail)
- 两者**互补**:workspace validator 是结构层,handback validator 是语义层;hand-off / hand-back 包都需两者都过

## OQ

- **OQ-workspace-1**:JSON schema 在 single-developer 场景的 friction(operator 改 hand-off 包模板时是否每次都校验)— v0.2 实践决
- **OQ-workspace-2**:跨 idea fork 切换时 working_repo 字段是否会被遗忘改 — 待真跑后看
