# Ops Runbook · 001-pA · PI Briefing Console

**版本**: 0.1
**创建**: 2026-04-23
**对应 spec**: `spec.md` v0.2.1 · `architecture.md` v0.2 · `SLA.md` v0.1 · `compliance.md` v0.2 · `risks.md` v0.2
**读者**: operator（日常维护）· lab member（operator 缺席时只读模式）· 未来交接人员
**配套脚本位置**: `deploy/systemd/` · `deploy/caddy/` · `deploy/postgres/` · `deploy/scripts/`（见 `reference/directory-layout.md` §1）

> 本文件是 v0.1 上线 + 日常运维的**可抄可跑**手册。每一行命令都以"照抄能跑"为目标。与 `spec.md` / `architecture.md` / `SLA.md` 冲突时**以后者为准**；本文件内的 invariant 以 `compliance.md §4` 为上位。

---

## §1 Overview & audience · 本文档谁读、何时读

### 1.1 读者与场景

| 读者 | 何时读这份文档 | 最关心哪几节 |
|---|---|---|
| **Operator（=项目负责人+solo dev）** | 首次部署 · 每月 15 分钟自审 · 任一告警邮件触发 · 计划缺席 ≥ 7 天前 · 接到 systemd OnFailure 通知 | §3 首次部署 · §6–§8 备份/恢复/监控 · §9 incident runbook · §10 缺席前 checklist |
| **Lab member（PI / ≤ 2 名 operator）** | operator 缺席 > 7 天时；日常**不应**读本文档 | §9.I4 "operator-absent" SOP（仅 read-only） |
| **未来交接人员** | operator 永久离开 / 项目 hand-over | 全部（按顺序通读一遍约 30 分钟） |

### 1.2 本文档的核心假设

1. 部署拓扑 = `architecture.md §9` 单 VPS（2 vCPU / 4 GB RAM · Ubuntu 24.04 · 自持 Postgres 16）
2. Operator 作风是 **boring > clever**；任何"新潮工具"（k8s / Docker / Vercel / Supabase）在本项目里不会出现
3. 整个 lab ≤ 15 seat · 实际 dogfood ≤ 3 seat（C10）；不追求商业级 uptime
4. 每月**必须**做 1 次备份 drill + 1 次自审（compliance.md §7）；drill 费时 < 30 分钟

### 1.3 本文档 **不** 覆盖的内容

| 不覆盖 | 权威文档 |
|---|---|
| Feature 需求 / 产品决策 | `PRD.md` / `spec.md` |
| 数据 schema / index | `reference/schema.sql` · `architecture.md §5` |
| API 契约 | `reference/api-contracts.md` |
| 工程代码目录结构 | `reference/directory-layout.md` |
| LLM 调用细节 | `reference/llm-adapter-skeleton.md` |
| 错误码定义 | `reference/error-codes-and-glossary.md` |
| 测试策略 | `reference/testing-strategy.md` |

---

## §2 Target deployment topology

### 2.1 Physical topology

单 VPS，全部组件 co-located（本项目刻意不拆多机；C13 solo operator 可持续性）。

建议配置：
- **Provider**：DigitalOcean Singapore（sgp1）/ Linode / Vultr 任一（月费 $10–15）
- **机型**：2 vCPU · 4 GB RAM · 40 GB SSD · Ubuntu 24.04 LTS
- **域名**：`lab-briefing.example.com`（operator 自有 · A 记录指向 VPS IP）
- **网络**：仅 22 / 80 / 443 开放；Postgres 绑 `127.0.0.1:5432`（不暴露公网 · `architecture.md §7 · pg_hba.conf` 限 localhost）

### 2.2 Logical topology（ASCII）

```
                              +--------------------+
                              | operator/lab member|
                              |  浏览器 (1024px+)  |
                              +---------+----------+
                                        |
                                        | HTTPS (443)
                                        v
+-----------------------------------------------------------------+
|                        Ubuntu 24.04 VPS                          |
|                                                                   |
|   +----------+    +---------------------------------+             |
|   | Caddy 2  |----| pi-briefing-web.service         |             |
|   | (80/443) |    |  Next.js 15 (Node 22 LTS)       |             |
|   |  autohttp|    |  listen 127.0.0.1:3000          |             |
|   +----------+    +-----------------+---------------+             |
|                                     |                             |
|                                     | pg-wire (Unix socket)       |
|                                     v                             |
|                          +---------------------+                  |
|                          | Postgres 16         |                  |
|                          |  listen localhost   |                  |
|                          |  /var/lib/postgresql|                  |
|                          +----------+----------+                  |
|                                     ^                             |
|                                     | pg-wire                     |
|                                     |                             |
|   +------------------------------+  |                             |
|   | pi-briefing-worker.timer     |  |                             |
|   |   OnCalendar=daily 06:00     |  |                             |
|   |     |                        |  |                             |
|   |     v                        |  |                             |
|   | pi-briefing-worker.service   |--+                             |
|   |   src/workers/daily.ts       |                                |
|   |     |   \                    |                                |
|   |     |    \--- HTTPS ---> [arXiv API]                          |
|   |     \------- HTTPS ---> [LLM provider (Anthropic/OpenAI)]     |
|   +------------------------------+                                |
|                                                                   |
|   +----------------+       +---------------+                      |
|   | pg-dump.timer  |-----> | /var/backups/ |                      |
|   |  daily 02:00   |       |  pi-briefing/ |                      |
|   +----------------+       |  dumps/*.gz   |                      |
|                            +-------+-------+                      |
|                                    |                              |
|                                    | restic (weekly Sunday 03:00) |
|                                    v                              |
|                            [Backblaze B2 / cloud object store]    |
|                                                                   |
+-------------------------------------------------------------------+
```

### 2.3 Stack 清单（全部 apt 装 · 零 Docker）

| 层 | 组件 | 版本 | 来源 | 备注 |
|---|---|---|---|---|
| OS | Ubuntu Server | 24.04 LTS | VPS image | 不用 22.04 · 24.04 的 systemd 256 是 `LoadCredential=` 的稳定版 |
| Runtime | Node.js | 22.x LTS | nodesource apt | 由 `deploy/systemd/pi-briefing-web.service` 的 `ExecStart` 调 |
| Package mgr | pnpm | 9.x | `corepack enable pnpm` | 不用 npm · 项目 `packageManager` 字段锁住 |
| Reverse proxy | Caddy | 2.x | Caddy 官方 apt | autohttps · Let's Encrypt 自动续签 |
| DB | Postgres | 16.x | Ubuntu apt `postgresql-16` | **native install, NOT docker** |
| Backup | restic | latest apt | Ubuntu apt `restic` | 加密增量 · Backblaze B2 |
| Cron | systemd timer | systemd 256 | 系统内置 | 不用 `cron` daemon · 全走 systemd |

### 2.4 Account 清单

| Account | 用途 | 创建方式 |
|---|---|---|
| `root` | 初装 apt · 不日常用 | VPS provider 给的 |
| `operator`（或 `yashu`） | SSH 登录 · 日常运维 | `adduser operator` + `usermod -aG sudo operator` |
| `pi-briefing` | 应用 runtime user | `adduser --disabled-password --gecos '' pi-briefing` |
| `postgres` | DB runtime user | 由 `postgresql-16` 安装自动创建 |
| `webapp_user`（DB role） | Web process 的 DB 连接身份 | `deploy/postgres/grants.sql` 里创建 |
| `worker_user`（DB role） | Worker process 的 DB 连接身份 | 同上 |

---

## §3 First-time deployment · 冷启 VPS → 上线（目标 ≤ 2h）

### 3.1 Pre-flight（在 laptop 上做）

```bash
# 1. 确认域名 DNS 已生效（A 记录指向未来 VPS IP 或预留的 floating IP）
dig +short lab-briefing.example.com

# 2. 准备 SSH key
ssh-keygen -t ed25519 -f ~/.ssh/pi-briefing-ed25519 -C "pi-briefing-deploy"

# 3. （可选）用 doctl 创建 droplet
doctl auth init
doctl compute droplet create pi-briefing-prod \
    --region sgp1 \
    --size s-2vcpu-4gb \
    --image ubuntu-24-04-x64 \
    --ssh-keys "$(doctl compute ssh-key list --format ID --no-header | head -1)" \
    --wait

VPS_IP=$(doctl compute droplet list pi-briefing-prod --format PublicIPv4 --no-header)
echo "VPS_IP=$VPS_IP"

# 4. DNS 更新（DigitalOcean 例）
doctl compute domain records create example.com \
    --record-type A --record-name lab-briefing --record-data "$VPS_IP" --record-ttl 300
```

### 3.2 System prep（SSH 到 VPS 执行）

```bash
ssh root@$VPS_IP
# ---- 以下全部在 VPS 内执行 ----

# 1. System update
apt update && apt upgrade -y

# 2. Minimal packages
apt install -y \
    build-essential git curl ca-certificates gnupg lsb-release \
    ufw fail2ban unattended-upgrades \
    postgresql-16 postgresql-client-16 \
    restic \
    mailutils    # sendmail CLI · 给告警邮件用

# 3. Node 22 LTS
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs
corepack enable pnpm

# 4. Caddy 2
apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' \
  | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' \
  | tee /etc/apt/sources.list.d/caddy-stable.list
apt update && apt install -y caddy

# 5. Firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# 6. fail2ban（SSH 防暴破）
systemctl enable --now fail2ban

# 7. Unattended security upgrades
dpkg-reconfigure -plow unattended-upgrades   # 接受默认

# 8. 创建 operator + pi-briefing 用户
adduser operator
usermod -aG sudo operator
mkdir -p /home/operator/.ssh
cp /root/.ssh/authorized_keys /home/operator/.ssh/
chown -R operator:operator /home/operator/.ssh
chmod 700 /home/operator/.ssh
chmod 600 /home/operator/.ssh/authorized_keys

adduser --disabled-password --gecos '' pi-briefing

# 9. sshd 禁 root login + 强制 key
sed -i 's/^#*PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config
sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl restart ssh

# 10. 日志目录
mkdir -p /var/log/pi-briefing
chown pi-briefing:pi-briefing /var/log/pi-briefing

# 11. Backup 目录
mkdir -p /var/backups/pi-briefing/dumps
chown postgres:postgres /var/backups/pi-briefing
chmod 750 /var/backups/pi-briefing

# 12. Credentials 目录（存 API key · SEC-3）
mkdir -p /etc/pi-briefing/credentials
chown root:pi-briefing /etc/pi-briefing
chmod 750 /etc/pi-briefing
chmod 750 /etc/pi-briefing/credentials
```

### 3.3 Postgres 初始化

```bash
# 1. 确认 Postgres 16 已起
systemctl status postgresql@16-main

# 2. 建 DB 与 role（用 postgres 身份跑）
sudo -u postgres psql <<'SQL'
create role webapp_user login password 'CHANGE_ME_WEBAPP_PW';
create role worker_user login password 'CHANGE_ME_WORKER_PW';
create database pi_briefing owner webapp_user;
\c pi_briefing
grant usage on schema public to worker_user;
SQL

# 3. pg_hba.conf · 仅允许 localhost SCRAM-SHA-256
PG_HBA=/etc/postgresql/16/main/pg_hba.conf
cp "$PG_HBA" "$PG_HBA.bak"
cat > "$PG_HBA" <<'CONF'
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             postgres                                peer
host    pi_briefing     webapp_user     127.0.0.1/32            scram-sha-256
host    pi_briefing     worker_user     127.0.0.1/32            scram-sha-256
host    pi_briefing     webapp_user     ::1/128                 scram-sha-256
host    pi_briefing     worker_user     ::1/128                 scram-sha-256
CONF
systemctl reload postgresql@16-main

# 4. postgresql.conf · 仅监听 localhost
POSTGRES_CONF=/etc/postgresql/16/main/postgresql.conf
sed -i "s/^#*listen_addresses.*/listen_addresses = 'localhost'/" "$POSTGRES_CONF"
systemctl restart postgresql@16-main
```

### 3.4 Clone & install application

```bash
# 切到 pi-briefing 用户
sudo -u pi-briefing -i
# ---- 以下 pi-briefing 身份 ----
cd /home/pi-briefing

git clone git@github.com:<your-org>/pi-briefing.git app
cd app

# 装依赖（frozen lockfile 模式）
pnpm install --frozen-lockfile

# 准备环境文件
cp .env.example /etc/pi-briefing/env
# operator 用编辑器把 /etc/pi-briefing/env 里的占位值换成真实值；
# 但 ANTHROPIC_API_KEY / OPENAI_API_KEY / SESSION_SECRET 不放这里 (见 §3.6)

# 把 schema 应用到 pi_briefing
exit   # 退回 operator
sudo -u postgres psql pi_briefing \
  < /home/pi-briefing/app/specs/001-pA/reference/schema.sql

# apply grants.sql（T030 生成）
sudo -u postgres psql pi_briefing \
  < /home/pi-briefing/app/deploy/postgres/grants.sql

# 回到 pi-briefing 身份 build
sudo -u pi-briefing bash -c "cd /home/pi-briefing/app && pnpm build"
```

### 3.5 Seed 首个 lab + admin seat

```bash
# 由 scripts/db-seed.ts 建 labs 行 + 生成第一条 admin invite
sudo -u pi-briefing bash <<'SH'
cd /home/pi-briefing/app
export $(grep -v '^#' /etc/pi-briefing/env | xargs)
pnpm db:seed
SH
# stdout 会打出第一条 invite URL · G4 H4（2026-04-24 R_final）· fragment 形式：
#   https://lab-briefing.example.com/login#invite=abcdef...
# operator 在本地浏览器打开（此时 Caddy 还没跑；下一步启动完再打开）
# 客户端 JS 读取 fragment → POST /api/invite/consume · token 在 body · 不进 Caddy 日志
```

### 3.6 敏感 secret 注入（systemd LoadCredential · SEC-3）

LLM API key / SESSION_SECRET **不**放 `/etc/pi-briefing/env`；放到 credentials 目录，由 systemd 以 ephemeral mount 注入：

```bash
# SESSION_SECRET · 64 hex
openssl rand -hex 32 > /etc/pi-briefing/credentials/session-secret
chown root:pi-briefing /etc/pi-briefing/credentials/session-secret
chmod 640 /etc/pi-briefing/credentials/session-secret

# Anthropic API key（从 Anthropic console 拿到后粘进来）
cat > /etc/pi-briefing/credentials/anthropic-api-key <<'KEY'
sk-ant-api03-REPLACE_ME
KEY
chmod 640 /etc/pi-briefing/credentials/anthropic-api-key
chown root:pi-briefing /etc/pi-briefing/credentials/anthropic-api-key

# OpenAI API key（同上）
cat > /etc/pi-briefing/credentials/openai-api-key <<'KEY'
sk-proj-REPLACE_ME
KEY
chmod 640 /etc/pi-briefing/credentials/openai-api-key
chown root:pi-briefing /etc/pi-briefing/credentials/openai-api-key

# Restic 密码
openssl rand -hex 32 > /etc/pi-briefing/credentials/restic-password
chmod 640 /etc/pi-briefing/credentials/restic-password
chown root:pi-briefing /etc/pi-briefing/credentials/restic-password
```

### 3.7 安装 systemd unit + Caddyfile + backup scripts

```bash
# 假设已把 deploy/ 的 unit/Caddyfile/scripts 推到 repo 里
cd /home/pi-briefing/app

sudo cp deploy/systemd/*.service    /etc/systemd/system/
sudo cp deploy/systemd/*.timer      /etc/systemd/system/
sudo cp deploy/caddy/Caddyfile      /etc/caddy/Caddyfile
sudo cp deploy/scripts/pg-dump.sh   /usr/local/sbin/pi-briefing-pg-dump
sudo cp deploy/scripts/restic-backup.sh /usr/local/sbin/pi-briefing-restic-backup
sudo chmod 755 /usr/local/sbin/pi-briefing-{pg-dump,restic-backup}

sudo systemctl daemon-reload
sudo systemctl enable --now pi-briefing-web.service
sudo systemctl enable --now pi-briefing-worker.timer
sudo systemctl enable --now pi-briefing-pg-dump.timer
sudo systemctl enable --now pi-briefing-restic.timer
sudo systemctl reload caddy
```

### 3.8 Smoke test

```bash
# 1. Healthz
curl -fsS https://lab-briefing.example.com/api/healthz | jq
# 期望：{"status":"ok","uptimeSec":...,"version":"...","now":"..."}

# 2. 登录（在本地浏览器）
# 打开 §3.5 记下的 invite URL；期望：302 → /today；cookie 被 Set-Cookie

# 3. 造 1 条 topic
# /topics → 新建 topic "RLHF alignment" + keyword 3 个 + arxiv cs.CL

# 4. 手动触发一次 worker（不等 06:00）
sudo systemctl start pi-briefing-worker.service
journalctl -u pi-briefing-worker.service -n 100 --no-pager
# 期望：started → fetched N papers → summary pass OK → briefing inserted → finished

# 5. /today
# 浏览器打开 /today；期望：至少一 topic 有 state_summary + 至多 3 篇 paper
```

### 3.9 可选 · 监控 cron 安装（§8.2）

```bash
sudo crontab -u operator -e
# 追加：
*/10 * * * * curl -fsS --max-time 10 https://lab-briefing.example.com/api/healthz > /dev/null || echo "[pi-briefing ALERT] /api/healthz down at $(date -u +%FT%TZ)" | sendmail -t <<< "To: operator@example.com
Subject: [pi-briefing ALERT] healthz down

"
```

### 3.10 首次部署 checklist

- [ ] `dig +short lab-briefing.example.com` 返回 VPS IP
- [ ] `ssh operator@$VPS_IP` 成功（root 禁 login）
- [ ] `ufw status` 显示 22/80/443 allow，其余 deny
- [ ] `sudo -u postgres psql pi_briefing -c '\dt'` 列出 15 张表（含 `paper_summaries`, `export_log`）
- [ ] `systemctl status pi-briefing-web.service` = active (running)
- [ ] `systemctl status pi-briefing-worker.timer` = active (waiting)
- [ ] `systemctl status pi-briefing-pg-dump.timer` = active (waiting)
- [ ] `curl https://lab-briefing.example.com/api/healthz` 200
- [ ] 浏览器登录 invite URL 成功
- [ ] 手动触发 worker 后 `SELECT count(*) FROM briefings` ≥ 1
- [ ] `cat /var/backups/pi-briefing/dumps/*.dump.gz` 存在（触发一次 pg-dump）
- [ ] Caddy 自动拿到 TLS 证书（`curl -I https://...` 200 + no cert warning）

---

## §4 systemd units 完整文件

### 4.1 `/etc/systemd/system/pi-briefing-web.service`

```ini
[Unit]
Description=pi-briefing web server (Next.js 15)
After=network.target postgresql@16-main.service
Wants=postgresql@16-main.service
OnFailure=pi-briefing-alert@%n.service

[Service]
Type=simple
User=pi-briefing
Group=pi-briefing
WorkingDirectory=/home/pi-briefing/app
EnvironmentFile=/etc/pi-briefing/env
ExecStart=/usr/bin/pnpm start
Restart=on-failure
RestartSec=5
TimeoutStopSec=30

# --- Resource caps（OPS-4 OOM 防护）---
MemoryMax=2G
MemoryHigh=1.5G
TasksMax=200

# --- Sensitive secrets（SEC-3 · LoadCredential 把文件 ephemeral-mount 到 $CREDENTIALS_DIRECTORY）---
LoadCredential=session-secret:/etc/pi-briefing/credentials/session-secret
LoadCredential=anthropic-api-key:/etc/pi-briefing/credentials/anthropic-api-key
LoadCredential=openai-api-key:/etc/pi-briefing/credentials/openai-api-key
# Web process 只需要 SESSION_SECRET；LLM key 不暴露给 Web（Web 不直调 LLM · ADR-2）
# 但为了保持两 unit 的 env 形态一致,仍 LoadCredential 再在 entry script 里 pick session

# --- Security hardening ---
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
ProtectKernelLogs=true
ProtectHostname=true
ProtectClock=true
RestrictNamespaces=true
RestrictSUIDSGID=true
LockPersonality=true
RestrictRealtime=true
RemoveIPC=true
ReadWritePaths=/home/pi-briefing/app/.next /home/pi-briefing/app/node_modules/.cache /var/log/pi-briefing
SystemCallArchitectures=native
SystemCallFilter=@system-service

[Install]
WantedBy=multi-user.target
```

### 4.2 `/etc/systemd/system/pi-briefing-worker.service`

```ini
[Unit]
Description=pi-briefing daily worker (arXiv fetch + LLM pass)
After=network.target postgresql@16-main.service
Wants=postgresql@16-main.service
OnFailure=pi-briefing-alert@%n.service

[Service]
Type=oneshot
User=pi-briefing
Group=pi-briefing
WorkingDirectory=/home/pi-briefing/app
EnvironmentFile=/etc/pi-briefing/env
# TimeoutStartSec=1800 · 一次 daily pass 最长 30min（90 paper × 20s p95 LLM call · 带裕量）
TimeoutStartSec=1800
ExecStart=/usr/bin/pnpm worker:daily

# Resource cap · worker 吃内存
MemoryMax=3G

LoadCredential=anthropic-api-key:/etc/pi-briefing/credentials/anthropic-api-key
LoadCredential=openai-api-key:/etc/pi-briefing/credentials/openai-api-key

NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ProtectKernelTunables=true
ProtectKernelModules=true
RestrictNamespaces=true
LockPersonality=true
ReadWritePaths=/var/log/pi-briefing
SystemCallArchitectures=native
SystemCallFilter=@system-service

# 仅启 timer · 不安装 WantedBy
```

### 4.3 `/etc/systemd/system/pi-briefing-worker.timer`

```ini
[Unit]
Description=Run pi-briefing-worker daily at 06:00 Asia/Shanghai

[Timer]
# OnCalendar 使用 systemd 语法 · Asia/Shanghai 由 timedatectl 保证
OnCalendar=*-*-* 06:00:00 Asia/Shanghai
# Persistent=true · 如错过（机器关机 / 电源闪退）启动后立即补跑
Persistent=true
# AccuracySec=1min · 允许 ±1 分钟漂移 · 节电
AccuracySec=1min
Unit=pi-briefing-worker.service

[Install]
WantedBy=timers.target
```

### 4.4 `/etc/systemd/system/pi-briefing-pg-dump.service`

```ini
[Unit]
Description=pi-briefing Postgres daily dump
After=postgresql@16-main.service
OnFailure=pi-briefing-alert@%n.service

[Service]
Type=oneshot
User=postgres
Group=postgres
ExecStart=/usr/local/sbin/pi-briefing-pg-dump
TimeoutStartSec=600

NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/var/backups/pi-briefing
```

### 4.5 `/etc/systemd/system/pi-briefing-pg-dump.timer`

```ini
[Unit]
Description=Daily pg_dump at 02:00 Asia/Shanghai

[Timer]
OnCalendar=*-*-* 02:00:00 Asia/Shanghai
Persistent=true
Unit=pi-briefing-pg-dump.service

[Install]
WantedBy=timers.target
```

### 4.6 `/etc/systemd/system/pi-briefing-restic.service` + `.timer`

```ini
# restic.service
[Unit]
Description=pi-briefing offsite backup (restic → B2)
After=pi-briefing-pg-dump.service
OnFailure=pi-briefing-alert@%n.service

[Service]
Type=oneshot
User=root
ExecStart=/usr/local/sbin/pi-briefing-restic-backup
LoadCredential=restic-password:/etc/pi-briefing/credentials/restic-password
TimeoutStartSec=1800
```

```ini
# restic.timer
[Unit]
Description=Weekly restic backup · Sundays 03:00

[Timer]
OnCalendar=Sun *-*-* 03:00:00 Asia/Shanghai
Persistent=true
Unit=pi-briefing-restic.service

[Install]
WantedBy=timers.target
```

### 4.7 `/etc/systemd/system/pi-briefing-alert@.service`（OnFailure 收件者）

```ini
[Unit]
Description=Send email on %i failure
# 这是 instance template · %i 会填入失败的 unit 名（e.g. pi-briefing-web.service）

[Service]
Type=oneshot
User=operator
ExecStart=/usr/local/sbin/pi-briefing-alert "%i"
```

`/usr/local/sbin/pi-briefing-alert`：

```bash
#!/usr/bin/env bash
# Invoked by systemd OnFailure=pi-briefing-alert@%n.service · $1 = unit name
set -euo pipefail
UNIT="${1:-unknown}"
TS=$(date -u +%FT%TZ)
TAIL=$(journalctl -u "$UNIT" -n 20 --no-pager 2>&1 || echo "(journalctl failed)")

sendmail operator@example.com <<MAIL
To: operator@example.com
Subject: [pi-briefing ALERT] $UNIT failed @ $TS
Content-Type: text/plain; charset=utf-8

Timestamp: $TS
Component: $UNIT
Message:   systemd reports failure.
Recommended action: SSH + systemctl status $UNIT + journalctl -u $UNIT -n 200

Log tail (last 20 lines):
$TAIL
MAIL
```

---

## §5 Caddyfile

`/etc/caddy/Caddyfile`：

```
{
    # 全局选项
    email operator@example.com
    # Let's Encrypt 使用 operator 邮箱做证书注册
}

lab-briefing.example.com {
    encode gzip zstd

    # --- 日志 ---
    # Access log 仅记 method/status/size/latency · 不记 query string
    # (G4 H4 · 2026-04-24 R_final 重述：invite token 现在走 POST body + URL fragment · 天然不进 Caddy log · 原 query-delete 的写法保留为一般性敏感参数清理 · 不是 invite token 的主要缓解)
    log {
        output file /var/log/caddy/pi-briefing-access.log {
            roll_size 10MiB
            roll_keep 8
            roll_keep_for 720h
        }
        format filter {
            wrap json
            fields {
                uri query delete
                request>headers>Cookie delete
            }
        }
    }

    # --- 反向代理 ---
    reverse_proxy 127.0.0.1:3000 {
        health_uri /api/healthz
        health_interval 30s
        health_timeout 5s
        health_status 200

        # 传递必要 header
        header_up X-Forwarded-Proto {scheme}
        header_up X-Forwarded-For {remote_host}

        # 防止应用假死
        transport http {
            dial_timeout 5s
            response_header_timeout 30s
        }
    }

    # --- 安全 header（见 architecture.md §7 安全边界 + compliance.md）---
    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains"
        X-Frame-Options "DENY"
        X-Content-Type-Options "nosniff"
        Referrer-Policy "same-origin"
        Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; frame-ancestors 'none'; form-action 'self'"
        Permissions-Policy "interest-cohort=(), geolocation=(), microphone=(), camera=()"
        # 仅业务内部工具 · 无第三方 script / pixel
    }

    # --- Rate limit（v0.1 软上限 · 用 Caddy defer_body 不阻塞 · 保守值）---
    # 说明：api-contracts.md §1.5 明确 v0.1 不做服务端 rate limit；此处 Caddy 层仅 sanity cap
    # 若触发 response 429 · 下一步 v0.2 再用 caddy-rate-limit 插件做精细化
}

# 健康检查端点单独放（无 auth · api-contracts.md E18）
# 不需要单独 site block · reverse_proxy 已覆盖；但明确把它列出来提醒 ops
```

**Invariant**（G4 H4 · 2026-04-24 R_final 重写）：invite token 现在走 POST body（`/api/invite/consume`）+ URL fragment（`/login#invite=<token>`）· Caddy **默认不记 POST body** · fragment **永不**进 server 日志 · 所以 token 根本不可能出现在 access log 里。原 `uri query delete` 配置保留作为一般性敏感参数清理（防止未来任何新 endpoint 把敏感值放 query），但**不是** invite token 泄漏的缓解措施。如需调试查 POST body，必须在应用层（不是 Caddy 层）开 request log，且明确不 log `/api/invite/consume` 路径。

---

## §6 Backup strategy（满足 SLA §1.3 · RPO ≤ 24h · RTO ≤ 2h）

### 6.1 三层备份总览

| 层 | 频率 | 存放位置 | 保留期 | 覆盖什么 |
|---|---|---|---|---|
| **L1 本地 dump** | 每日 02:00 | `/var/backups/pi-briefing/dumps/` | 14 日 · 每周日留至 8 周 | Postgres 全库 |
| **L2 云盘副本** | 每周日 03:00 | Backblaze B2（restic 加密） | 4 周 + 12 月 | L1 的整个 dump 目录 |
| **L3 代码 + 配置** | 每次 commit + 每次 `/etc/pi-briefing/env` 改 | GitHub private repo（代码）· `/etc/pi-briefing/env` 手抄到 operator 云笔记 | 永久 | Application code · config |

### 6.2 `deploy/scripts/pg-dump.sh`（装到 `/usr/local/sbin/pi-briefing-pg-dump`）

```bash
#!/usr/bin/env bash
# -----------------------------------------------------------------
# pi-briefing daily Postgres dump
# Runs as postgres user · 由 pi-briefing-pg-dump.timer 触发 · 02:00 local
# -----------------------------------------------------------------
set -euo pipefail

BACKUP_DIR=/var/backups/pi-briefing/dumps
TODAY=$(date +%Y-%m-%d)
DOW=$(date +%a)   # Mon Tue ... Sun
OUT="${BACKUP_DIR}/${TODAY}-${DOW}.dump.gz"
ALERT_EMAIL=operator@example.com

mkdir -p "$BACKUP_DIR"

# 1. Dump + gzip
if ! pg_dump --no-owner --format=custom pi_briefing | gzip -9 > "$OUT"; then
    echo "[pi-briefing ALERT] pg_dump failed at $TODAY" \
      | sendmail "$ALERT_EMAIL"
    exit 1
fi

# 2. Sanity: size > 1 KB
SIZE=$(stat -c%s "$OUT")
if [ "$SIZE" -lt 1024 ]; then
    echo "[pi-briefing ALERT] pg_dump size suspiciously small: $SIZE bytes at $TODAY" \
      | sendmail "$ALERT_EMAIL"
    exit 1
fi

# 3. Rotate
#    - 保留最近 14 日
#    - 但每个 Sunday 留 8 周（56 日内非 Sun 的 > 14 日才删）
find "$BACKUP_DIR" -name '*.dump.gz' -mtime +14 ! -name '*-Sun.dump.gz' -delete
find "$BACKUP_DIR" -name '*-Sun.dump.gz' -mtime +56 -delete

# 4. 记录成功日志
echo "[$(date -u +%FT%TZ)] pg_dump ok · size=$SIZE · file=$OUT" \
  >> /var/log/pi-briefing/pg-dump.log
```

### 6.3 `deploy/scripts/restic-backup.sh`（装到 `/usr/local/sbin/pi-briefing-restic-backup`）

```bash
#!/usr/bin/env bash
# -----------------------------------------------------------------
# pi-briefing offsite weekly backup to Backblaze B2 via restic
# Runs as root · 由 pi-briefing-restic.timer 触发 · Sun 03:00 local
# -----------------------------------------------------------------
set -euo pipefail

# 从 systemd LoadCredential 读 restic password（只在本进程生命周期可读）
export RESTIC_PASSWORD_FILE="${CREDENTIALS_DIRECTORY}/restic-password"
export RESTIC_REPOSITORY="b2:pi-briefing-backups:/"

# B2 auth（放在 /etc/pi-briefing/env 最底部 · 仅 systemd 读）
# shellcheck disable=SC1091
source /etc/pi-briefing/env  # 提供 B2_ACCOUNT_ID / B2_ACCOUNT_KEY

ALERT_EMAIL=operator@example.com

# 1. Init 仓库（幂等 · 若已存在则 no-op）
restic cat config > /dev/null 2>&1 || restic init

# 2. Backup 本地 dumps 目录
if ! restic backup /var/backups/pi-briefing/dumps \
    --tag weekly --tag "$(date +%Y-W%V)" \
    --host pi-briefing-prod; then
    echo "[pi-briefing ALERT] restic backup failed at $(date -u +%FT%TZ)" \
      | sendmail "$ALERT_EMAIL"
    exit 1
fi

# 3. Retention
restic forget \
    --keep-weekly 4 \
    --keep-monthly 12 \
    --prune

# 4. 完整性 check（每月首个 Sunday 跑）
if [ "$(date +%d)" -le 07 ]; then
    restic check || {
        echo "[pi-briefing ALERT] restic check failed · repo integrity issue" \
          | sendmail "$ALERT_EMAIL"
        exit 1
    }
fi

echo "[$(date -u +%FT%TZ)] restic backup ok" \
  >> /var/log/pi-briefing/restic.log
```

### 6.4 Backup 失败响应

| 连续失败次数 | 响应 |
|---|---|
| 1 次 | systemd OnFailure 发告警邮件 · operator 等下次运行观察 |
| 2 次 | operator 必须 SSH 手工调查 · `journalctl -u pi-briefing-pg-dump.service` |
| 3 次 | **DOGFOOD 状态升级**：停 worker · 暂缓新 feature · 优先修复备份 |

---

## §7 Restore drill · 每季度演练 2 次（本地 dump 1 次 + restic 1 次）

> 目的：验证 RTO ≤ 2h（SLA §1.3）。drill 在 **test VM** 跑，绝不在 prod。

### 7.1 Drill via local `pg_dump` archive（每季度 1 次）

```bash
# 1. 在 test VM（另一台 VPS / localVM）准备
apt install -y postgresql-16 postgresql-client-16

# 2. 复制最新 dump
scp pi-briefing-prod:/var/backups/pi-briefing/dumps/$(date +%Y-%m-%d)-*.dump.gz \
    /tmp/test-restore.dump.gz

# 3. 创建目标 DB
sudo -u postgres createdb pi_briefing_restore

# 4. Restore（计时！）
time sudo -u postgres bash -c '
  gunzip -c /tmp/test-restore.dump.gz \
    | pg_restore --no-owner --dbname=pi_briefing_restore --clean --if-exists
'
# 期望输出：real < 2h（通常实际 < 2min · 数据规模小）

# 5. Smoke queries（validate schema + rows）
sudo -u postgres psql pi_briefing_restore <<'SQL'
\d
SELECT count(*) FROM topics;
SELECT count(*) FROM briefings;
SELECT max(for_date) FROM briefings;
SELECT count(*) FROM actions;
SELECT count(*) FROM paper_summaries;
SELECT count(*) FROM seats WHERE role = 'admin';
SELECT count(*) FROM export_log;
SQL
# 预期：count 与 prod 最新 /api/admin/lab-stats 一致 · max(for_date) 距今 ≤ 24h（RPO）

# 6. 验证 CHECK 约束仍在
sudo -u postgres psql pi_briefing_restore <<'SQL'
-- 预期：以下两条都报 CHECK violation
INSERT INTO actions (seat_id, paper_id, action, why)
  VALUES (1, 1, 'skip', NULL);
INSERT INTO paper_summaries (paper_id, topic_id, summary_text, llm_call_id,
                              model_name, prompt_version)
  VALUES (1, 1, 's1. s2. s3. s4. s5.', 1, 'test', 'v0');
SQL

# 7. 记录 drill 结果
cat >> /home/operator/docs/runbook/restore-drill-$(date +%Y-%m-%d).md <<NOTE
# Restore drill · $(date +%Y-%m-%d)
- Dump age: $(stat -c %Y /tmp/test-restore.dump.gz) seconds old
- Restore time (real): <填 time 命令输出>
- Row counts (topics/briefings/actions/paper_summaries): ...
- RTO met (<2h): YES/NO
- Issues: <填>
- Operator sign-off: <operator name>
NOTE

# 8. 清理 test VM（绝不保留含 lab 数据的 test DB · compliance.md §5.3）
sudo -u postgres dropdb pi_briefing_restore
sudo rm -f /tmp/test-restore.dump.gz
```

### 7.2 Drill via restic archive（每季度 1 次）

```bash
# 在 test VM 上
apt install -y restic postgresql-16

# 1. 拿到 restic password（operator 手工）
export RESTIC_PASSWORD='...'
export RESTIC_REPOSITORY='b2:pi-briefing-backups:/'
export B2_ACCOUNT_ID='...'
export B2_ACCOUNT_KEY='...'

# 2. List snapshots
restic snapshots

# 3. 取最新 weekly
SNAP=$(restic snapshots --tag weekly --json | jq -r 'max_by(.time).short_id')
restic restore "$SNAP" --target /tmp/restore-dumps

# 4. Pick 最新 dump
LATEST_DUMP=$(ls -t /tmp/restore-dumps/var/backups/pi-briefing/dumps/*.dump.gz | head -1)

# 5. 跑 §7.1 的 step 3–8
```

### 7.3 Drill 失败的应对

| 现象 | 可能原因 | 动作 |
|---|---|---|
| `pg_restore` 出 role does not exist | `--no-owner` 未加 | 修 script · 重跑 |
| Row counts 严重偏低 | Dump 被某日部分失败污染 | 取更早的 dump 试；若仍失败 → RPO 破坏 → 升级 incident I-DB-DATA-LOSS |
| CHECK violation 测试未拒绝 | Schema drift | 停！对比 `reference/schema.sql` vs `\d+ <table>` · 按 drift 方向修复 |
| Restore 耗时 > 2h | 数据体量超预期 | 记下实际时长；若持续 > 2h · 升 SLA（v1.0 目标已 ≤ 4h） |

---

## §8 Monitoring & alerting（solo operator 最小集）

v0.1 **不装** Prometheus / Grafana / DataDog（C13 · 每多一个服务 = 一个 oncall 点）。

### 8.1 告警来源矩阵

| 监控项 | 机制 | 频率 | 触发动作 |
|---|---|---|---|
| systemd unit OnFailure | `pi-briefing-alert@.service` | 事件触发 | 邮件 |
| /api/healthz 连续 down | cron + curl | 10 min | 连续 2 次失败 → 邮件 |
| Worker daily succeeded | systemd unit 状态 + `fetch_runs` 表 | 06:30 local 检查 | 当天无 `run_date=today AND status='ok'` → 邮件 |
| Disk > 85% | cron + df | 1 h | 立即邮件 |
| Backup freshness | cron + find | 10:00 local daily | 0 新文件 → 邮件 |
| LLM 月度成本 | `llm_calls` SUM · 在 adapter 内做 | 每次 LLM call | > $40 → warn 日志 · 邮件 |
| TLS 证书临期 | Caddy 自动续 + systemd timer 自查 | 每日 | 7 天内过期 → 邮件 |

### 8.2 Cron entries（operator crontab）

```cron
# m h dom mon dow command

# Healthz ping · 连续 2 次失败才告警（reduce 噪声）
*/10 * * * * /usr/local/sbin/pi-briefing-healthz-watch

# 早 06:30 校验 worker
30 6 * * * /usr/local/sbin/pi-briefing-check-worker

# Daily 磁盘检查 · 每小时
0 * * * * /usr/local/sbin/pi-briefing-disk-watch

# Daily 10:00 检查备份新鲜度
0 10 * * * /usr/local/sbin/pi-briefing-backup-watch

# TLS 证书自查（Caddy 自动 · 此处仅作冗余）
0 8 * * * /usr/local/sbin/pi-briefing-cert-watch
```

### 8.3 告警脚本 · `pi-briefing-healthz-watch`

```bash
#!/usr/bin/env bash
set -euo pipefail
STATE=/var/lib/pi-briefing/healthz-misses
mkdir -p "$(dirname "$STATE")"
touch "$STATE"
MISSES=$(cat "$STATE")

if ! curl -fsS --max-time 8 https://lab-briefing.example.com/api/healthz > /dev/null; then
    MISSES=$((MISSES + 1))
    echo "$MISSES" > "$STATE"
    if [ "$MISSES" -ge 2 ]; then
        sendmail operator@example.com <<MAIL
To: operator@example.com
Subject: [pi-briefing ALERT] healthz down x${MISSES}

Timestamp: $(date -u +%FT%TZ)
Component: web + caddy
Message: 连续 $MISSES 次 /api/healthz 请求失败
Recommended action: SSH + systemctl status pi-briefing-web.service caddy
MAIL
    fi
else
    echo "0" > "$STATE"
fi
```

### 8.4 Worker-watch · `pi-briefing-check-worker`

```bash
#!/usr/bin/env bash
set -euo pipefail

TODAY=$(date +%Y-%m-%d)
COUNT=$(sudo -u postgres psql pi_briefing -tAc "
  SELECT count(*)
  FROM fetch_runs
  WHERE run_date = '${TODAY}' AND source='arxiv' AND status='ok'
")

if [ "$COUNT" -lt 1 ]; then
    TAIL=$(journalctl -u pi-briefing-worker.service -n 50 --no-pager || true)
    sendmail operator@example.com <<MAIL
To: operator@example.com
Subject: [pi-briefing ALERT] worker 未成功 @ ${TODAY} 06:30

Timestamp: $(date -u +%FT%TZ)
Component: pi-briefing-worker.service
Message: fetch_runs 无当日 ok 记录
Recommended action: sudo systemctl start pi-briefing-worker.service · 然后 journalctl 读 tail
Log tail:
${TAIL}
MAIL
fi
```

### 8.5 Disk-watch · `pi-briefing-disk-watch`

```bash
#!/usr/bin/env bash
set -euo pipefail
PCT=$(df /var/lib/postgresql | awk 'NR==2 { print $5 }' | tr -d '%')
if [ "$PCT" -gt 85 ]; then
    sendmail operator@example.com <<MAIL
To: operator@example.com
Subject: [pi-briefing ALERT] Postgres disk @ ${PCT}%

Timestamp: $(date -u +%FT%TZ)
Component: filesystem (/var/lib/postgresql)
Message: 磁盘使用率 ${PCT}% · 阈值 85%
Recommended action: 查 §9 I3 流程 · 清理 llm_calls 历史 or 扩盘
MAIL
fi
```

### 8.6 Backup-watch · `pi-briefing-backup-watch`

```bash
#!/usr/bin/env bash
set -euo pipefail
FRESH=$(find /var/backups/pi-briefing/dumps -name '*.dump.gz' -mtime -1 | wc -l)
if [ "$FRESH" -lt 1 ]; then
    sendmail operator@example.com <<MAIL
To: operator@example.com
Subject: [pi-briefing ALERT] 昨日 pg_dump 缺失

Timestamp: $(date -u +%FT%TZ)
Component: pi-briefing-pg-dump.service
Message: /var/backups/pi-briefing/dumps 中未发现 24h 内的 .dump.gz
Recommended action: sudo systemctl start pi-briefing-pg-dump.service 手工补 + 调查为何未自动跑
MAIL
fi
```

### 8.7 告警邮件统一模板

所有 `sendmail` 的 Subject 必须带前缀 `[pi-briefing ALERT]`，便于 operator 邮件 filter 抓到。Body 结构固定：

```
Timestamp: <ISO UTC>
Component: <systemd unit | cron job | application>
Message:   <one-line 人话总结>
Recommended action: <one-line 下一步>
Log tail (如有):
<最多 20 行 journalctl 或应用日志>
```

### 8.8 可观测性"绝不装"名单

| 不装 | 理由 |
|---|---|
| Prometheus / node-exporter | 每多一进程 = oncall 风险（OPS-1） |
| Grafana | 无 prometheus 无用 |
| Sentry | 应用错误通过 journalctl 查即可 |
| DataDog | 成本高于整个 VPS |
| Loki / ELK / Graylog | 日志量 ≤ 100 MB/月 · grep 够用 |

---

## §9 On-call SOP · 事故响应剧本

**原则**：每类事故给**3 步 check · 1 条 manual fix · 1 条 escalate**。Operator 熟练后整个剧本应 < 15 min 完成。

### I1 · Briefing 未生成（PI 08:00 看到 stale banner）

**Trigger**：`/today` 顶部 stale banner 可见 · 或 operator 主动检查。

**Check（3 步）**：
```bash
# 1. Worker 状态
sudo systemctl status pi-briefing-worker.service
# 期望 · Active: inactive (dead) since <上次完成> — normal
# 若 failed / activating · 记下时间戳

# 2. 当日 fetch_runs
sudo -u postgres psql pi_briefing -c "
  SELECT run_date, source, status, items_fetched, error_text
  FROM fetch_runs
  WHERE run_date = CURRENT_DATE
  ORDER BY started_at
"

# 3. Journal 近 200 行
sudo journalctl -u pi-briefing-worker.service -n 200 --no-pager
```

**Manual fix**：
```bash
sudo systemctl start pi-briefing-worker.service
# 等它跑完（最多 30 min · 看 journalctl -f）
```

**Escalate**：
- 若 `error_text` 显示 arXiv 5xx/429 · 等 1 h 再试；/today 的 stale banner 是预期行为（risks.md TECH-2）
- 若 `LLM_BUDGET_EXCEEDED` · 进入 §9.I7
- 若连续 2 天 worker 均失败 · 升级为"sustained outage" · 邀 Codex review 日志

---

### I2 · `/today` 500

**Trigger**：用户汇报 · 或 healthz cron 告警。

**Check**：
```bash
# 1. Web 状态
sudo systemctl status pi-briefing-web.service

# 2. Journal
sudo journalctl -u pi-briefing-web.service -n 200 --no-pager

# 3. DB 通达
sudo -u postgres psql pi_briefing -c 'SELECT 1'
```

**Manual fix**：
```bash
# 最常见 · Node 进程 OOM
sudo systemctl restart pi-briefing-web.service
# 等 10s · 再 curl /api/healthz
```

**Escalate**：
- 若 `FATAL: too many clients` · 连接池泄漏 · 升 `DATABASE_POOL_WEBAPP` 无用 · 优先重启 pg-briefing-web + 排 `src/lib/db/client.ts` 是否未关连接
- 若 DB ping 失败 · 进入 §9.I3

---

### I3 · Postgres 磁盘 > 90% 或 DB 连接不通

**Check**：
```bash
df /var/lib/postgresql          # 总占用
du -sh /var/lib/postgresql/16/main/base/*   # 哪个数据库吃盘
du -sh /var/lib/postgresql/16/main/pg_wal/ # WAL 积压
```

**Manual fix**（优先级顺序）：
```bash
# A. 清 llm_calls 历史（compliance.md: 仅保留 90 天审计就够 · 不影响产品 · 不放进 export）
sudo -u postgres psql pi_briefing <<'SQL'
BEGIN;
DELETE FROM llm_calls WHERE called_at < now() - interval '90 days';
SELECT count(*) FROM llm_calls;
COMMIT;
VACUUM FULL llm_calls;
SQL

# B. 清 sessions 过期行（可安全删 · 已过期的 session 不会被查）
sudo -u postgres psql pi_briefing -c "
  DELETE FROM sessions WHERE expires_at < now() - interval '60 days';
  VACUUM FULL sessions;
"

# C. 清 fetch_runs 老记录（保留 90 天就够 audit）
sudo -u postgres psql pi_briefing -c "
  DELETE FROM fetch_runs WHERE started_at < now() - interval '180 days';
  VACUUM FULL fetch_runs;
"

# D. paper_summaries / papers · 产品数据 · 绝对不删
# 若真的 paper / summaries 撑爆盘 · 扩盘（DigitalOcean: resize-droplet）· 不清数据
```

**Escalate**：
- 若扩盘后仍 > 90% · LAB 用户数据超预期 · 升 v0.2 re-architecture
- 若 pg_wal 过大 · WAL archive 未跑 · 检查 `archive_command`（v0.1 默认未启用 · 无需处理）

---

### I4 · Operator 缺席 > 7 天（BUS-1 触发）

**Trigger**：operator 无法 SSH / 回邮件；lab member 按 §10 缺席前 checklist 寻找本节。

**Lab member 允许的操作（ONLY）**：
- 以自己已有的 seat 登录 · 查看 `/today` · 做 4-action
- 查看 `/breadcrumbs` · `/papers/:id/history`
- **不允许**：admin 路由（topic CRUD、`/admin/invite`、export、`/admin/allow-continue`）
- **不允许**：SSH 到 VPS

**Worker 行为**：systemd timer 自动每日 06:00 跑 · operator 不在也**不会停**（C13 明确：任何设计都不得依赖持续人工 oncall）。

**14 天无音讯后的行动**：
- 指定备用联系人（operator 在 §10 checklist 里提前指定）尝试联系 operator 本人
- 如确认 operator 永久失联 → 备用联系人有 git repo 的 read 权限 → 可继续在本地保留数据 → 在 VPS provider 那边把账单模式改成"只付服务器费" → 静默保留 6 个月 → 再决定 decommission

**14 天后允许的应急操作**：
- 只有在出现**数据丢失风险**（磁盘 > 95%）时 · 备用联系人可 SSH 跑 §7 restore drill 的 backup 步骤
- 任何修改代码 / 停服务 / 删数据都**不允许**

---

### I5 · DOGFOOD-1 sentinel 触发（day-30 < 3 active seat）

**Trigger**：`/today` 顶部显示红色 sentinel banner · 或 operator 主动 `GET /api/admin/lab-stats` 见 `sentinelState='escalate'`。

**选项（operator 必须选一条）**：

| 选项 | 动作 | 预期效果 |
|---|---|---|
| (a) 补人 | admin 进 `/admin/invite` 发 token + 传链接给第 3 名 lab 成员 | 次日 active_seats_30d ≥ 3 · sentinel 变 ok |
| (b) 签延期 | admin 进 `/admin/allow-continue` 设 14 天延期 | `labs.allow_continue_until` 写今后 14 天 · banner 变 warn 不再阻塞 |
| (c) 停工 | 暂缓所有 Phase 2/3 feature · 回 L2 重新 scope | 项目进 park 模式 |

**不允许**：绕过 banner 继续加 feature（sentinel 是项目健康度代码兑现 · 绕过 = 违反 PRD kill-window 承诺）。

---

### I6 · LLM provider 全局故障

**Trigger**：worker 日志出现连续 5 次 `LLMProviderError(retryable=true)` · 或 `fetch_runs.error_text` 含 `BOTH_PROVIDERS_DOWN`。

**Check**：
```bash
sudo -u postgres psql pi_briefing -c "
  SELECT provider, count(*), max(called_at)
  FROM llm_calls
  WHERE called_at > now() - interval '24 hours'
  GROUP BY provider
"
```

**自动行为**：
- Adapter 层 `callWithFallback()` 自动切 `LLM_FALLBACK_PROVIDER`（`llm-adapter-skeleton.md §5`）
- 若 fallback 也失败 · T013 `persistSummary` 走 `fallback-heuristic-v1` 写 `paper_summaries`（内容 = abstract 头 2 句 + "[⚠️ fallback: LLM unavailable]"）
- Briefing 仍生成 · 但 state_summary 退化为 heuristic-only 描述

**Manual fix**：
```bash
# 若判定是账号问题（401 · billing）
vim /etc/pi-briefing/credentials/anthropic-api-key   # 更新 key
# 或切 primary
vim /etc/pi-briefing/env
# LLM_PROVIDER=openai
# LLM_FALLBACK_PROVIDER=anthropic
sudo systemctl restart pi-briefing-web.service   # Web 读 env
# 下一次 06:00 cron 自动用新 provider
```

**Escalate**：
- 若两家 provider 连续 > 24h 全挂 · 接受当天 briefing 退化 · 浏览器显示 `[⚠️ fallback]` 图标 · 是诚实降级 · 不是 bug

---

### I7 · LLM budget exceeded（C11 $50/月超线）

**Trigger**：worker 日志 `LLM_BUDGET_EXCEEDED` · 或 `/api/admin/lab-stats` 见 `costThisMonthCents > 5000`。

**自动行为**：`recordLLMCall()` 在写 DB 前抛 `LLMBudgetExceededError` · 当日剩余 paper skip LLM · `paper_summaries` 不写新行（旧行保留）· briefing 用 fallback 模板。

**operator 选项**：
| 选项 | 动作 |
|---|---|
| (a) 等下月 | 不做事 · 次月 1 日 cost 重置 · 恢复 LLM |
| (b) 加额度 | 编辑 `src/lib/llm/audit.ts` 的 `MONTHLY_BUDGET_CENTS` · commit + deploy · **需要 operator 明确 sign-off 因为违反 C11** |
| (c) 换 provider | 按 §I6 的切换流程 · 切到更便宜那家 |

---

### I8 · 发现未授权访问（SEC 事件）

**Trigger**：`/var/log/caddy/pi-briefing-access.log` 出现异常 IP 高频请求 · 或 `export_log` 出现非预期的 seat_id。

**Check**：
```bash
# 1. 最近 24h export
sudo -u postgres psql pi_briefing -c "
  SELECT created_at, seat_id, export_type, byte_size
  FROM export_log
  WHERE created_at > now() - interval '24 hours'
  ORDER BY created_at DESC
"

# 2. 异常 session
sudo -u postgres psql pi_briefing -c "
  SELECT seat_id, ip, user_agent, count(*) cnt
  FROM sessions
  WHERE issued_at > now() - interval '7 days'
  GROUP BY seat_id, ip, user_agent
  ORDER BY cnt DESC
  LIMIT 20
"

# 3. Caddy access
tail -200 /var/log/caddy/pi-briefing-access.log | jq -r '[.ts, .request.remote_ip, .request.method, .request.uri, .status] | @tsv'
```

**Containment（立即动作）**：
```bash
# 立刻 revoke 所有 session（强制所有人重登）
sudo -u postgres psql pi_briefing -c "
  UPDATE sessions SET revoked_at = now() WHERE revoked_at IS NULL
"

# 旋转 SESSION_SECRET
openssl rand -hex 32 > /etc/pi-briefing/credentials/session-secret
sudo systemctl restart pi-briefing-web.service

# 旋转 DB 角色密码
sudo -u postgres psql -c "ALTER ROLE webapp_user WITH PASSWORD 'NEW_PW'"
# 同步改 /etc/pi-briefing/env 里的 DATABASE_URL · 再重启 web + worker
```

**Escalate**：
- 若确认泄露 · 按 `compliance.md §3 数据使用声明` 通知全部 lab 成员 · 24h 内告知事件概要

---

## §10 Operator planned absence · >7 天离开前 checklist

必须在离开**至少 3 天前**完成，以便有时间处理漏项：

- [ ] Git tag 当前 HEAD · `git tag vX.Y.Z && git push origin vX.Y.Z`
- [ ] 确认过去 30 天内做过至少 1 次 restore drill（`ls /home/operator/docs/runbook/restore-drill-*.md`）
- [ ] 确认 `.env` + credentials 在未来 14 天内不会过期（LLM API key / TLS cert / SMTP cred）
- [ ] Compliance 自审（`compliance.md §7` 的 6 项 checklist）
- [ ] `/var/log/pi-briefing/*.log` 空间检查 · 如 > 1 GB 手工 rotate
- [ ] 在 `docs/runbook/operator-absent-until-YYYY-MM-DD.md` 写明：
  - 离开日期 / 预计回归日期
  - 备用联系人姓名 + 两种联系方式（email + 电话）
  - 允许 lab member 做什么 / 不允许做什么（复制 §9.I4）
  - 14 天后升级程序
- [ ] `journalctl --vacuum-time=30d` 清老日志 · 避免溢出
- [ ] **告知** lab 成员离开 · 贴本文档 §9.I4 链接
- [ ] **可选**（若 absence > 14 天）：设置 `DISABLE_ADMIN_DURING_ABSENCE=true` 环境变量 · 重启 web · 所有 admin 路由返 503
  - 实施方法：在 `src/lib/auth/middleware.ts` 的 `requireAdmin` 里读该 env · 若为 true 一律 503
  - v0.1 未硬编码此 feature flag；若真要用需在 Phase 2 临时加一个 middleware · 预留 2h 工期
- [ ] 在 README 顶部 append 一行 `⚠️ Operator absent until YYYY-MM-DD · 只接受只读操作`

回归后第 1 天必做：
- [ ] 读过去的全部告警邮件
- [ ] `SELECT * FROM fetch_runs WHERE started_at > '<离开日期>' AND status != 'ok'`
- [ ] `SELECT * FROM export_log WHERE created_at > '<离开日期>'` · 审 export 合理性
- [ ] `SELECT * FROM sessions WHERE issued_at > '<离开日期>'` · 审新 session
- [ ] 跑 1 次 §7 restore drill · 确认备份仍可恢复
- [ ] 写本次 absence 的 self-report（对齐 O3 · operator seat 连续性）

---

## §11 Disaster recovery scenarios

| 场景 | 操作 | RTO 期望 |
|---|---|---|
| **D1 VPS 被删 / 被盗** | 新 provider 跑 §3 所有步骤 · 从 B2 restic 拉最新 snapshot · pg_restore | ≤ 4h（含域名 DNS 生效） |
| **D2 DB 文件损坏 · dump 仍可读** | 在 prod 上 `dropdb + createdb + pg_restore`（§7.1 步骤 3–4）· 重启 web + worker | ≤ 2h（RTO 合规） |
| **D3 所有备份丢（B2 账号 + VPS 同时挂）** | Git repo 还在 → 重建空 schema · 告诉 lab 成员从 0 开始 · `compliance.md §5.3` 整体删除流程的 reverse | 不可恢复用户数据；服务 4h 内重起 |
| **D4 Domain 被劫持** | DNS provider 恢复 · Caddy 自动重新申请 TLS · 无需碰代码 | ≤ 1h |
| **D5 LLM provider 永久关账号** | 按 §I6 切到 fallback + 在 env 里永久去掉该 provider | ≤ 30 min |
| **D6 Operator 唯一 laptop 被盗** | Git repo 在 GitHub（无 `.env`）· credentials 另存 operator 云笔记 · 新 laptop clone repo + 下载 credentials → 继续 | ≤ 1 工作日（取决于 laptop 供应） |

---

## §12 Release / deployment workflow

### 12.1 正常 release（无 schema 变更）

```bash
# 1. 本地 tag + push
git tag -a vX.Y.Z -m "release: ..."
git push origin vX.Y.Z

# 2. SSH
ssh operator@$VPS_IP
sudo -u pi-briefing -i
cd ~/app

# 3. 拉 tag
git fetch --tags
git checkout vX.Y.Z
pnpm install --frozen-lockfile
pnpm build

# 4. 重启（web · worker 在下次 cron 自动使用新代码）
exit   # 回 operator
sudo systemctl restart pi-briefing-web.service

# 5. 验证
curl -fsS https://lab-briefing.example.com/api/healthz | jq '.version'
# 期望 · version 等于 git rev-parse --short vX.Y.Z
```

### 12.2 Release with schema change

```bash
# 1. 本地生成 migration（Drizzle）
pnpm db:generate

# 2. Review generated SQL
cat src/db/migrations/000X_*.sql
# ---- 重要 ----
# 任何 DROP COLUMN · ALTER TYPE · 非兼容 schema 变动必须：
#   (a) 在 PR 描述里标注 destructive
#   (b) 先在 staging drill 一遍
#   (c) Prod apply 前手工 backup 再跑

# 3. commit + tag + push
git add src/db/migrations/
git commit -m "feat(db): ..."
git tag -a vX.Y.Z -m "..."
git push --follow-tags

# 4. Prod apply
ssh operator@$VPS_IP
# 先 backup
sudo systemctl start pi-briefing-pg-dump.service
# 等它完成（journalctl -f）
# 然后 pull + apply
sudo -u pi-briefing bash <<'SH'
cd ~/app && git fetch --tags && git checkout vX.Y.Z
pnpm install --frozen-lockfile
# Drizzle migrate（小心 · 读 SQL 看清变动再执行）
pnpm db:migrate
pnpm build
SH

sudo systemctl restart pi-briefing-web.service
# worker 下一轮 cron 跑新 schema
```

### 12.3 Rollback

```bash
# 1. 找上一 stable tag
git log --oneline --tags -20 | grep 'tag:'

# 2. 按 12.1 步骤 checkout 那个 tag + 重启
# 但 schema 变动无法回滚 · 必须从 dump restore：
#   a) 停 web + worker
sudo systemctl stop pi-briefing-web.service pi-briefing-worker.timer

#   b) drop + restore
sudo -u postgres dropdb pi_briefing
sudo -u postgres createdb pi_briefing
sudo -u postgres pg_restore -d pi_briefing /var/backups/pi-briefing/dumps/<last-known-good>.dump.gz

#   c) 回老 tag code
sudo -u pi-briefing bash -c 'cd ~/app && git checkout vX.Y-1.Z && pnpm build'
sudo systemctl start pi-briefing-web.service pi-briefing-worker.timer
```

---

## §13 Secrets rotation schedule

| Secret | 周期 | 方法 | 下次执行日 |
|---|---|---|---|
| `SESSION_SECRET` | 6 月 | `openssl rand -hex 32 > /etc/pi-briefing/credentials/session-secret` + restart web · 所有 session 立即失效 | 填 |
| `ANTHROPIC_API_KEY` | 12 月 或 泄露 | Anthropic console → revoke 老 key → 新 key 写 `credentials/anthropic-api-key` → restart web + worker | 填 |
| `OPENAI_API_KEY` | 12 月 | 同上 | 填 |
| `webapp_user` / `worker_user` 密码 | 12 月 | `ALTER ROLE <user> WITH PASSWORD '...'` · 同步改 `/etc/pi-briefing/env` · restart | 填 |
| `RESTIC_PASSWORD` | **永不直接轮换** · 轮换 = 新 repo | 若要轮换：`restic key add` 先加新密钥 · `restic key list` 确认存在 · `restic key remove <old>` · **绝不**先删老密钥 | N/A |
| `B2_ACCOUNT_KEY` | 12 月 或 泄露 | Backblaze console → 新 applicationKey → 写 env → test restic ls | 填 |
| VPS SSH key | 24 月 | 本地生成新 key → 上传到 VPS authorized_keys → 测试 login → 从 DigitalOcean console 删老 key | 填 |

Operator 每 6 个月月初 review 本表 · 把"下次执行日"列刷新。

---

## §14 Invariants · 运维层不得违反的硬规则

（继承自 `compliance.md §4` · `architecture.md §7` · `SLA.md §4`；此处汇总供 runbook 读者一眼看到）

| # | Invariant | 守在哪 | 违反会被谁抓到 |
|---|---|---|---|
| INV-1 | Postgres 仅监听 127.0.0.1 | `postgresql.conf` + `pg_hba.conf` | nmap 扫描 · 或 compliance 自审 |
| INV-2 | LLM 调用不得走 Web 请求路径 | `src/lib/llm/*` 只被 `src/workers/*` import | CI 静态扫描 · code review |
| INV-3 | Export 仅 admin 可达 | 双重 middleware · DB audit | SEC-1 · export_log 自审 |
| INV-4 | Access log 无 query string | Caddyfile `uri query delete` | H6 修补 · 月度日志抽查 |
| INV-5 | `.env*` 不入 git | `.gitignore` + `gitleaks` 预提交 | pre-commit 钩子 |
| INV-6 | 生产 credentials 走 systemd `LoadCredential=` | systemd unit + chmod 640 | SEC-3 |
| INV-7 | Backup drill ≥ 1 次 / 季度 | §7 drill 日志 | 月度自审 |
| INV-8 | Cron worker 可在 operator 缺席时独立跑 ≥ 14 天 | systemd timer `Persistent=true` + on-boot catchup | BUS-1 |
| INV-9 | 任一 incident 响应时间 ≤ 对应 SLA | §9 脚本 | operator self-report |

违反任一条 = P1 incident · 必须 rollback + 根因分析。

---

## §15 Quick reference · 最常敲的 10 条命令

```bash
# 1. 整体健康
curl -fsS https://lab-briefing.example.com/api/healthz | jq

# 2. Web 日志
sudo journalctl -u pi-briefing-web.service -n 200 --no-pager

# 3. Worker 日志
sudo journalctl -u pi-briefing-worker.service -n 200 --no-pager

# 4. 手动跑 worker
sudo systemctl start pi-briefing-worker.service

# 5. 手动 pg_dump
sudo systemctl start pi-briefing-pg-dump.service

# 6. Lab stats
sudo -u postgres psql pi_briefing -c "
  SELECT
    (SELECT count(*) FROM seats WHERE last_login_at > now() - interval '30 days') AS active_30d,
    (SELECT count(*) FROM briefings WHERE for_date = current_date) AS briefings_today,
    (SELECT sum(cost_cents) FROM llm_calls WHERE called_at >= date_trunc('month', now())) AS cost_cents_this_month
"

# 7. 最近错误
sudo -u postgres psql pi_briefing -c "
  SELECT run_date, source, error_text FROM fetch_runs WHERE status != 'ok' ORDER BY started_at DESC LIMIT 10
"

# 8. 最新备份
ls -lh /var/backups/pi-briefing/dumps/ | tail -5

# 9. Caddy reload
sudo systemctl reload caddy

# 10. 打印本 runbook 目录
grep '^## ' /home/pi-briefing/app/specs/001-pA/reference/ops-runbook.md
```

---

## 变更日志

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-23 | 0.1 | 初版 · 15 节 · 对齐 spec.md v0.2.1 / architecture.md v0.2 / SLA.md v0.1 / risks.md v0.2 · 拷贝可跑的 systemd unit · Caddyfile · pg-dump / restic 脚本 · incident runbook 覆盖 8 类事件 |
