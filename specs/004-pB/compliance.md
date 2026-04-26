# Compliance — 004-pB · 决策账本

**Version**: 0.1
**Created**: 2026-04-25T15:30:00+08:00
**Companion**: `risks.md` LEG-1 / LEG-2 / LEG-3 · PRD §10 Risk #4

> **核心结论**: 本系统是**单用户私用投资决策辅助工具**, **不构成持牌投顾产品**,
> v0.1 **无强制合规义务**。本文档存在的目的是**显式划清自用边界**, 防止未来误踩
> 监管线。

---

## 1. 适用判断 (是否触发监管)

逐项检查常见监管框架, 给出本项目当前的触发状态:

| 框架 | 适用范围 | 本项目触发? | 理由 |
|------|---------|-----------|------|
| **美国 SEC Investment Advisers Act of 1940** | 收费提供投资建议 | ❌ 不触发 | 不收费, 不对外提供建议, 单用户自用 |
| **美国 FINRA 持牌经纪 / 投顾** | 经纪交易 / 投顾业务 | ❌ 不触发 | 不接 broker API, 不下单 (R1), 不收费 |
| **中国《证券投资顾问业务暂行规定》(2010)** | 接受委托提供证券投资分析、预测或者建议 | ❌ 不触发 | 不接受任何外部委托, 单用户自用; 用户即开发者 |
| **香港 SFC 持牌资产管理 / 投顾** | 香港居民投顾 / 资管业务 | ❌ 不触发 | 不对外提供服务 |
| **GDPR (欧盟个人数据保护)** | 处理欧盟居民个人数据 | ❌ 不触发 | 单用户私用, 无第三方个人数据; 用户即数据主体 |
| **PIPL (中国个人信息保护法 2021)** | 处理个人信息 | ❌ 不触发 (灰色: 用户自身信息) | 仅处理 human 自己的投资信息, 无他人个人信息; 数据本地存储不出境 |
| **CCPA / CPRA (美国加州)** | 处理加州居民个人信息商用 | ❌ 不触发 | 非商业, 单用户 |
| **PCI DSS** | 持卡人数据 | ❌ 不触发 | 不存任何账户 / 卡号 / 资金凭证 |
| **HIPAA** | 健康数据 | ❌ 不触发 | 无健康数据 |
| **COPPA** | 儿童 (< 13 岁) 数据 | ❌ 不触发 | 单用户成年 |
| **MiFID II** | 欧盟金融市场工具 | ❌ 不触发 | 不在欧盟运营 |
| **Anthropic Usage Policy** | LLM API 使用条款 | ✅ **适用** | 见 §3 |
| **Telegram Bot API ToS** | bot 使用条款 | ✅ **适用** | 见 §3 |
| **咨询师订阅服务条款** | 个人订阅合理使用 | ✅ **适用** | 见 §2 |

**净结论**: 无政府强制合规要求 (LEG-1 / LEG-3 风险 = Low)。仅有 3 项**第三方服务条款**适用, 均为软约束。

---

## 2. 咨询师内容合理使用 (LEG-2)

### 2.1 现状

human 已付费订阅哥大背景华语投顾的微信小程序服务, 含视频/音频/PDF/图文。

### 2.2 v0.1 处理边界

| 项 | v0.1 行为 | 合规理由 |
|----|---------|---------|
| **缓存咨询师 PDF** | ✅ 本地 `~/decision_ledger/inbox/` + SQLite | 个人订阅合理使用 (用户为合法订阅者, 个人使用) |
| **LLM 解析咨询师内容** | ✅ Anthropic API | 解析输出仅供 human 自用决策, 不 republish |
| **解析结果存入 advisor_reports 表** | ✅ 本地 SQLite | 同上 |
| **Telegram 推送咨询师摘要** | ✅ 仅推送给 human 自己 chat_id (单白名单) | 不分发给第三方 |
| **commit 到 git repo** | ❌ 永远不 (D20) | 防止公开传播 |
| **export 到云盘** | ❌ 永远不 | 同上 |
| **Web UI 多用户访问** | ❌ 永远不 (D5 single user) | 防止外人通过 LAN 访问 |
| **训练数据 / fine-tune** | ❌ 永远不 (v0.1 + v0.5 都不) | 训练数据需独立许可 |

### 2.3 边界提醒 (runbook 写明)

- 不要 paste 咨询师内容到任何**对外**论坛 / 群组 / 社交平台
- 不要 commit `inbox/` 或 `db.sqlite` 到 git (gitignored, pre-commit hook 拦截)
- 不要让他人从同一台机器**直接**访问 Web UI (localhost binding 只对本机有效)
- 备份位置不放云同步路径 (SEC-6)

### 2.4 若投顾服务条款变化

若 human 收到投顾的合规通知 (例如禁止任何形式 caching), 必须立即:
1. 删除 `~/decision_ledger/inbox/`
2. 删除 SQLite 中 `advisor_reports` 表的原文字段
3. 仅保留结构化结果 (方向/标的/置信度) 而非原文
4. 工作流改回 human 阅读后只导入结论 (不导入原文)

---

## 3. 第三方 API 服务条款

### 3.1 Anthropic API

**适用**: [Anthropic Usage Policy](https://www.anthropic.com/legal/usage-policy)

**v0.1 合规清单**:
- ✅ 不用于生成误导性医疗 / 法律 / 金融**对外**建议 (仅自用)
- ✅ 不试图绕过 safety filter
- ✅ 不存储 / 转发 Anthropic 输出供他人使用
- ✅ API key 安全存储 (`.env`, 不 commit) — SEC-3 mitigation

**注意点**: Anthropic Usage Policy §financial advice 未禁止"个人金融工具自用", 但禁止"对公众提供 unlicensed financial advice"。本系统在 D5 单用户 + D17 不商业化的前提下不触发。

### 3.2 Telegram Bot API

**适用**: [Telegram Bot API Terms](https://telegram.org/tos/bot)

**v0.1 合规清单**:
- ✅ Bot 仅 push 给单白名单 chat_id (human 自己)
- ✅ 不滥用 sendMessage rate limit (节制 push 已是 R4 + O8)
- ✅ Bot token 安全存储 (`.env`)
- ✅ 不用 bot 做未授权数据收集 / spam

### 3.3 LLM 输出免责

LLM 输出 (StrategySignal / ConflictReport / Rebuttal) 在系统内**始终标注**来源:
- StrategySignal.source_id (e.g. `"agent_synthesis"`) 显式标 LLM
- 任何 Web UI / Telegram 渲染 LLM 输出的地方, 文案附 "LLM 生成, 仅供参考, 由 human 最终决策" (可在通用 footer 显示)

---

## 4. 自用免责声明 (内置在 Web UI / runbook)

### 4.1 在 Web UI 首页 footer 显示 (永远在线)

```
本系统是 [human name] 的个人投资决策辅助工具, 不是持牌投顾产品。
所有决策由 human 自己最终做出, 工具仅提供参考视角与冲突报告。
LLM 输出可能包含错误或偏见, human 不应不加审慎地接受任何建议。
不接受任何外部投资委托, 不为他人提供建议。
```

### 4.2 在 runbook.md 显式记录

```markdown
## 法律边界

1. 本系统**不是**robo-advisor / 投顾持牌产品
2. 本系统**不**自动下单, 不持有任何 broker / 资金凭证
3. 本系统数据**仅本地**, 不上传, 不对外
4. 咨询师订阅内容仅供本人决策参考, 不 redistribute
5. 若有任何**对外**使用需求 (分享 / 商业化), **必须 fork 新 spec**, 重审合规
```

### 4.3 R1 / R2 红线工程化体现

- 系统 schema 不存在任何 broker / order / account / payment 字段
- LLM prompt 不允许输出 "请你立即下单" 字样 (单元测试 sanity check)
- Devil's advocate 输出风格强制带"反方意见仅供考虑"

---

## 5. 数据保留与删除

### 5.1 v0.1 不需要 GDPR/PIPL 级别的 retention policy

理由: 单用户即数据主体, 数据控制权完全在 human 手上。

### 5.2 但提供基础数据管理操作 (runbook 写明)

```bash
# 完全删除所有数据 (核选项)
rm -rf ~/decision_ledger/

# 仅删除咨询师内容 (保留决策档案)
sqlite3 ~/decision_ledger/db.sqlite "DELETE FROM advisor_reports;"
rm -rf ~/decision_ledger/inbox/
rm -rf ~/decision_ledger/llm_cache/

# 导出决策档案 (CSV)
sqlite3 ~/decision_ledger/db.sqlite ".headers on" ".mode csv" "SELECT * FROM decisions;" > decisions.csv

# 删除单条决策
sqlite3 ~/decision_ledger/db.sqlite "DELETE FROM decisions WHERE trade_id = '...';"
```

---

## 6. 未来商业化 / 多用户 / 公开使用 → 触发重审

### 6.1 触发重审的事件

如果 human 改主意, 任何**一项**发生:
- 让他人 (包括配偶) 通过任意方式访问系统输出
- 收费 / 接受捐赠 / 卖订阅
- 把系统部署到云 / 公网
- 让多个 user 并行使用

→ **必须**重新走完 compliance 评估, 极可能需要持牌或注册。

### 6.2 重审 deliverable

- 重新评估第 §1 表所有框架的触发状态
- 新合规相关风险纳入 risks.md (LEG-X / SEC-X 子树)
- 商业化路径要走 fork 新 spec (D17 / COM-1)
- 红线 R1 / R2 仍然硬不变

---

## 7. 自查 (spec-writer 交付前)

- [x] 列出可能适用的监管框架
- [x] 每条给出"是否触发 + 理由"
- [x] 咨询师内容合理使用边界明确
- [x] 第三方 API 条款 (Anthropic + Telegram) 已检查
- [x] 自用免责声明的 UI / runbook 落点明确
- [x] 商业化触发重审的条件明确
- [x] 与 risks.md LEG-X / SEC-X 一致
