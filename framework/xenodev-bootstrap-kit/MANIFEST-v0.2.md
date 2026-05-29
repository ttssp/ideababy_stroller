---
title: MANIFEST · bootstrap-kit v0.2 mirror provenance
schema_version: 0.1
prd_fork_id: 006a-pM-v0.2
created: 2026-05-28
maintained_by: XenoDev → IDS bootstrap-kit mirror sync
schema_ref: XenoDev/specs/006a-pM-v0.2/architecture.md#§3.1
---

# MANIFEST · 006a-pM-v0.2 · bootstrap-kit v0.2 mirror provenance

> **结论先**:本 MANIFEST 是 v0.2 增量 inventory(非 full bootstrap-kit inventory · per spec.md §3.1 + codex round 7 F1)。每 wave append 一节 · 真路径每文件一行 · 7 字段严格 schema。任一字段缺 / SHA 不实测 = MANIFEST PASS gate fail。

## §wave-1

| source_path | target_path | source_sha256 | target_sha256 | copy_method | verification_command | operator_decision_source |
|---|---|---|---|---|---|---|
| /Users/admin/codes/XenoDev/lib/handback-validator/check-6-id-charset-and-final-path.sh | framework/xenodev-bootstrap-kit/handback-validator/check-6-id-charset-and-final-path.sh | 833c4ca0de89095ef475f0e4546bcf70dc8fea48d08e5e51f2d09da273a4c2dc | 833c4ca0de89095ef475f0e4546bcf70dc8fea48d08e5e51f2d09da273a4c2dc | cp -p | shasum -a 256 /Users/admin/codes/XenoDev/lib/handback-validator/check-6-id-charset-and-final-path.sh /Users/admin/codes/ideababy_stroller/framework/xenodev-bootstrap-kit/handback-validator/check-6-id-charset-and-final-path.sh | T100b / forge v3 §W2 A-1 |
| /Users/admin/codes/XenoDev/lib/handback-validator/templates/handback.template.md | framework/xenodev-bootstrap-kit/handback-validator/templates/handback.template.md | d2a510c51744ef7f097b57956730acb6852cc4fbdad56fe76586cc6f774be379 | d2a510c51744ef7f097b57956730acb6852cc4fbdad56fe76586cc6f774be379 | cp -p | shasum -a 256 /Users/admin/codes/XenoDev/lib/handback-validator/templates/handback.template.md /Users/admin/codes/ideababy_stroller/framework/xenodev-bootstrap-kit/handback-validator/templates/handback.template.md | T101 / forge v3 §W2 A-7 |
| /Users/admin/codes/XenoDev/lib/handback-validator/gen-handback.sh | framework/xenodev-bootstrap-kit/handback-validator/gen-handback.sh | 24947d0bb8b16ba186b0f1efb7a0fe3e00b7a7ef94c28cac8c29dea5804cd941 | 24947d0bb8b16ba186b0f1efb7a0fe3e00b7a7ef94c28cac8c29dea5804cd941 | cp -p | shasum -a 256 /Users/admin/codes/XenoDev/lib/handback-validator/gen-handback.sh /Users/admin/codes/ideababy_stroller/framework/xenodev-bootstrap-kit/handback-validator/gen-handback.sh | T101 / forge v3 §W2 A-8 + T103 真路径 dquote 修后重 cp |
| /Users/admin/codes/XenoDev/lib/handback-validator/score-handback.sh | framework/xenodev-bootstrap-kit/handback-validator/score-handback.sh | 4310fb600ca856db6a888750275a3ce21bdc18257e7e1f38350839c1ab9e241e | 4310fb600ca856db6a888750275a3ce21bdc18257e7e1f38350839c1ab9e241e | cp -p | shasum -a 256 /Users/admin/codes/XenoDev/lib/handback-validator/score-handback.sh /Users/admin/codes/ideababy_stroller/framework/xenodev-bootstrap-kit/handback-validator/score-handback.sh | T101 / forge v3 §W2 A-9 |
| /Users/admin/codes/XenoDev/lib/eval-event-log/event-schema.json | framework/xenodev-bootstrap-kit/eval-event-log/event-schema.json | 99c314116f3b298a34bf2f3eec8820c8ab40d1d851cf21d16411b4b25a73eaac | 99c314116f3b298a34bf2f3eec8820c8ab40d1d851cf21d16411b4b25a73eaac | cp -p | shasum -a 256 /Users/admin/codes/XenoDev/lib/eval-event-log/event-schema.json /Users/admin/codes/ideababy_stroller/framework/xenodev-bootstrap-kit/eval-event-log/event-schema.json | T105 / forge v3 §W2 B-2 |

<!-- wave-2 / wave-3 待 T209 / T306 append -->
