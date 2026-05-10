---
discussion_id: 008
prd_fork_id: 008a-pA
handback_id: 008a-pA-20260520T103015Z
from_build_repo: /Users/admin/codes/XenoDev
to_source_repo: /Users/admin/codes/ideababy_stroller
workspace:
  source_repo: /Users/admin/codes/ideababy_stroller
  build_repo: /Users/admin/codes/XenoDev
  working_repo: /Users/admin/codes/XenoDev
  handback_target: /Users/admin/codes/ideababy_stroller/discussion/008/handback/
source_repo_identity:
  expected_remote_url: ""
  repo_marker: "# Idea Incubator"
  git_common_dir_hash: ""
tags:
  - drift
severity: low
created: 2026-05-20T10:30:15Z
related_task: T013
---

# Hand-back · 008a-pA · drift fixture(valid · 6 约束全过)

valid fixture for handback-validator unit test。

## §1 · Build-side 上下文(发生了什么)

T013 跑完后发现 spec §3 C2 与实际 lib 行为冲突(测试用 fake)。

## §2 · 触发理由

drift: spec §3 C2 假设 lib 返回 None,实际返回 [];evidence: tests/test_c2.py:42

## §3 · 给 IDS 的建议

- [ ] 修 PRD §"Real constraints" C2(改为 list 或 None)
