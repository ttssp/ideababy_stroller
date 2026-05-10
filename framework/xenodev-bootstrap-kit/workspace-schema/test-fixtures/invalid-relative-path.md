---
workspace:
  source_repo: ./ideababy_stroller
  build_repo: /Users/admin/codes/XenoDev
  working_repo: /Users/admin/codes/ideababy_stroller
  handback_target: /Users/admin/codes/ideababy_stroller/discussion/008/handback/
---

# Invalid fixture — source_repo is relative path

source_repo 不以 / 开头(`./ideababy_stroller`)。
应 exit 1 + stderr 报 source_repo not absolute。
