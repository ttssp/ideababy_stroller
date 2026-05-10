# Eval append-only event log kit

per `framework/SHARED-CONTRACT.md` §"模块 B" + stage-forge-006-v2.md L255 / L329 / IN-5。

## 这是什么

XenoDev 的 Eval 数据接口。**v0.1 只产 raw event log,不实装 scoring 算法**(per stage doc L259 OUT-2 + L341 v0.2 note 2)。

3 类 event(stage doc verbatim):
1. `review_failures` — cross-model review 失败 / Codex review BLOCK / 同行 review 拒绝
2. `operator_interventions` — operator 手工介入 build 流程(拒绝 task 自动化结论 / 改 spec / 重派 task)
3. `handback_drift` — hand-back 包 tags=drift 计数

## v0.1 范围(per stage doc OUT)

✅ **In v0.1**:
- event JSON schema(SSOT)
- append-only writer(校验 schema 后 append JSONL 行)
- query reader(按 event_type / discussion_id / ts 范围 filter)

❌ **Out v0.1(v0.2 note 2)**:
- scoring 算法(operator 干预率 X% / 成功 N idea 阈值)
- verdict / risk tier(v0.2 note 3)
- 自动报警(v0.2)

## 文件清单

- `README.md`(本文件)
- `event-schema.json` — formal JSON schema(SSOT)
- `writer.sh` — append-only writer(校验 + append `.eval/events.jsonl`)
- `reader.sh` — query reader(filter by type / discussion / since)
- `test-fixtures/` — 4 测试 fixtures(3 valid + 1 invalid)

## 装机(XenoDev 端,operator bootstrap.sh 后)

bootstrap.sh 已自动 cp 到 `lib/eval-event-log/`。

XenoDev parallel-builder / operator 在以下时机调 writer.sh:
- review 失败:`bash lib/eval-event-log/writer.sh '{"ts":"...","event_type":"review_failures","details":"...","task_id":"..."}'`
- operator 介入:operator 手工拒绝 task / 改 spec 时 append
- hand-back drift:hand-back 包写入后,若 tags=drift,计数 append

## 单元测试

```bash
EVAL_LOG_DIR="$(mktemp -d)"
export EVAL_LOG_DIR

# 测试 1: valid event 1(review_failures)→ exit 0
bash framework/xenodev-bootstrap-kit/eval-event-log/writer.sh \
  '{"ts":"20260510T120000Z","event_type":"review_failures","details":"codex BLOCK on T013"}'
test "$(wc -l < "$EVAL_LOG_DIR/events.jsonl")" -eq 1 && echo PASS

# 测试 2: valid event 2(operator_interventions)→ exit 0
bash framework/xenodev-bootstrap-kit/eval-event-log/writer.sh \
  '{"ts":"20260510T130000Z","event_type":"operator_interventions","details":"rejected auto-conclusion","task_id":"T014"}'
test "$(wc -l < "$EVAL_LOG_DIR/events.jsonl")" -eq 2 && echo PASS

# 测试 3: valid event 3(handback_drift)→ exit 0
bash framework/xenodev-bootstrap-kit/eval-event-log/writer.sh \
  '{"ts":"20260510T140000Z","event_type":"handback_drift","details":"PRD-spec mismatch","discussion_id":"008"}'
test "$(wc -l < "$EVAL_LOG_DIR/events.jsonl")" -eq 3 && echo PASS

# 测试 4: invalid event(missing event_type)→ exit 1
bash framework/xenodev-bootstrap-kit/eval-event-log/writer.sh \
  '{"ts":"20260510T150000Z","details":"no type"}' 2>&1
# 应 exit 1 + stderr 报 missing event_type

# 测试 5: reader filter
bash framework/xenodev-bootstrap-kit/eval-event-log/reader.sh --type review_failures
# 应输出 1 行(测试 1 的 event)
bash framework/xenodev-bootstrap-kit/eval-event-log/reader.sh --discussion 008 --count
# 应输出 1(测试 3 的 event)
bash framework/xenodev-bootstrap-kit/eval-event-log/reader.sh --since 20260510T130000Z --count
# 应输出 2(测试 2 + 3)

rm -rf "$EVAL_LOG_DIR"
```

## v0.2 升级 trigger

per stage doc v0.2 note 2:**累计 ≥ 3 真 idea 或 ≥ 30 task 后定 scoring 算法 + N + 干预率 X 阈值**。

到时升级方向:
- writer.sh 加 `--validate` 选项跑 jsonschema(若装 npm)
- reader.sh 加 `--summary` 输出 aggregate(N 真 idea 完成率 / X% intervention rate)
- 加 `scorer.sh`(独立 script)算 verdict / risk tier(v0.2 note 3)

## OQ

- **OQ-eval-1**:3 类 event 是否完备(漏 event 类型?eg "spec validation failed" 算 review_failures 还是新类?)— B2.2 跑首 PRD 后回看
- **OQ-eval-2**:`.eval/events.jsonl` 是否进 git history(v0.1 .gitignore 排除,但 retrospective 时是否需要 git history)— v0.2 决
- **OQ-eval-3**:event log retention(永久保留 vs 按月归档)— v0.2 决
