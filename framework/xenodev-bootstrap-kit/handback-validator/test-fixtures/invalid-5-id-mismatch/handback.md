---
discussion_id: 008
prd_fork_id: 999z-pZ
handback_id: 999z-pZ-20260520T103015Z
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
---

# Invalid fixture · §6.2.1 约束 5 失败(三处 id 不一致)

frontmatter discussion_id = 008,但 prd_fork_id = 999z-pZ(前缀 999 ≠ 008)。
prd_fork_id 前缀 != discussion_id → 约束 5 FAIL。

应 exit 1 + stderr 报 "FAIL · §6.2.1 约束 5 (id consistency check)"
