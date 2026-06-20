<!-- FROZEN SNAPSHOT · forge 008 v3 _external
     source_repo: /Users/admin/codes/XenoDev (git HEAD: 6f1a0df)
     source_file: dogfood-backlog.md (lines 422-EOF · the 自动翻页 entry, commit 6f1a0df)
     snapshot_sha256(slice): 4b48c546b987a44d6678f2dece0e82648151a164cf31db3199d1be6587ef00b0
     snapshot_at: 2026-06-19T15:49:50Z
     reason: cross-repo target #1 · snapshot 进 IDS 避 Codex 沙箱 BLOCK(同 v2 _external 做法)
     NOTE: 这是 v3 议题主源 · 含实战边界硬证据(列表止于 2025-07-21 / 2026 仅 detail 可达)+ 3 候选架构向
-->

## operator 治理诉求:放宽采集面到「自动翻页」(去掉「不主动发请求」半自动约束)
- 日期: 2026-06-19T00:00:00Z
- 类型: 框架缺陷(协议层 · 安全边界 scope 争议 · 非 bug)
- 严重度: high
- 复现场景: 008-pB v0.2 实战采集「2026-01-01 起至今全历史库」。实测边界:moduleContentList 列表接口只吐到 2025-07-21(contentId 164966);2026 的 2 篇(176375/176384,6-17)只在 operator「点开单篇 detail」时被动抓到,**不在任何已抓列表页**。operator 反馈「在 App 里手动滑列表找 2026 入口很慢」,明确要求「改红线,自动翻页没问题」——即希望 agent 程序化翻页/抓取顾问内容列表,而非半自动(operator 手滑 + addon 被动监听)。
- 为何是框架级 + 为何拒绝当场改(3 条):
  ① **C5「不爬/不规避访问控制」**是 spec 写死的项目约束;改它属 PRD 约束变更,SSOT 在 IDS,须回 `/handback-review` → `/scope-inject`,不在 XenoDev 当场删。
  ② **真正拦路虎是凭据隔离(三件硬约束①· non-overridable · IAM 级)**:自动翻页须带 operator 登录态(key/cookie)发请求,而登录态绝不进 agent context——agent 物理上无法以 operator 身份发请求,删 C5 也解不了。这是「半自动被动采集」架构的地基,不是一句「没问题」能拆。
  ③ **dogfood 铁律**:框架级安全边界变更绝不在 XenoDev 当场改(= V4 失败模式「agent 觉得没问题就静默绕过」)。
- 候选决议向(回 IDS forge 定 · 不当场改): 
  ① **维持半自动**(operator 手滑/点开,addon 被动落盘)——当前架构,安全边界最清晰;agent 侧可优化「侦察兵」体验(分析 addon 落盘接口,告诉 operator 哪个栏目含目标时段 + 翻页参数形态,把盲滑变定向滑)降低 operator 手动成本。
  ② **受控自动翻页**(若 forge 评估某些源、某频率、不带高敏登录态确实合规):须解决凭据隔离(如何在不让 key 进 agent context 的前提下翻页?可能需独立采集 daemon 持 key,agent 只读其落盘——但这又引入新信任边界)+ 重定义 C5 scope(「规避访问控制」边界在哪)+ 速率/源白名单治理。这是协议层重大变更,须 forge 专题。
  ③ **混合**:agent 产「翻页计划」(参数序列),operator 一键确认后由持 key 的 daemon 执行——agent 不持 key、不直接发请求,但自动化程度提升。信任边界仍需 forge 审。
- 关联: spec 008-pB C5 条款 / framework/SHARED-CONTRACT.md §1+§2(凭据隔离 + 半自动采集原则)/ src/capture/addon.py(被动监听架构)/ 三件硬约束① / CLAUDE.md dogfood 铁律 / 本次实战边界证据(列表止于 2025-07-21,2026 仅 detail 可达)
- operator 确认: <留空 · 待 operator 回 IDS:这是要不要改采集架构的治理决议,operator 已口头表态「自动翻页没问题」——但须在 IDS forge 走正式决议(评估凭据隔离怎么解 / C5 scope 怎么重定义 / 选哪个候选向),不在 XenoDev 当场拆安全底线>
