# Stuck 检测器 8 场景测试矩阵 Fixture 说明

> 唯一真相源：`specs/003-pA/architecture.md §8.7`

## Fixture 格式（每行一个 probe sample）

```jsonl
{"ts": 0.0, "gpu": 82.5, "cpu": 12.3, "disk_delta_mbs": 0.1, "net_delta_mbs": 0.5}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `ts` | float | 相对采样时刻（秒），从 0.0 起，步长 5s |
| `gpu` | float \| null | GPU 利用率 0-100%；null 表示无 GPU |
| `cpu` | float | 子进程 CPU% 累加（psutil.children） |
| `disk_delta_mbs` | float | 磁盘 IO 增量 MB/s |
| `net_delta_mbs` | float | 网络 IO 增量 MB/s |

字段命名与 `StuckStateMachine.transition(sample)` 直接对齐，测试里可零转换喂入 SM。

## 8 场景矩阵

| # | 文件 | 描述 | 期望最终状态 | SIGINT |
|---|---|---|---|---|
| 1 | `scene1_lora_60min.jsonl` | LoRA epoch 60min，GPU=30-50% 全程 | `training` | 0 |
| 2 | `scene2_pip_slow_download.jsonl` | pip 慢下载，net=200KB-2MB/s 交替 | `idle` 或 `downloading` | 0 |
| 3 | `scene3_deadlock.jsonl` | 子进程死锁，冷启动期后全 0 超 15min | `truly_stuck` | 1 |
| 4 | `scene4_cold_start_deadlock.jsonl` | 冷启动期（0-300s）内全 0 | `idle` + warnings 非空 | 0 |
| 5 | `scene5_boundary_29s.jsonl` | GPU=25% 持续 29s（5 样本）→ 跌 0 | `idle`（未触发 training） | 0 |
| 6 | `scene6_boundary_30s.jsonl` | GPU=25% 持续 30s（6 样本）→ 跌 0 | `training`（已触发） | 0 |
| 7 | `scene7_training_idle_59s.jsonl` | training 态 GPU<5%+CPU<10%+disk<1MB 持续 59s | `training`（未触发 idle） | 0 |
| 8 | `scene8_disk_suppression.jsonl` | GPU=0 但 disk=5MB/s 全程（写 checkpoint） | `training`（AND 不满足） | 0 |

## 采样参数（architecture §8.1 契约）

- 采样周期：5s/sample
- 滚动窗口：12 样本 = 60s
- idle → training：GPU > 20% 持续 30s（6 样本）
- training → idle：GPU<5% AND CPU<10% AND disk<1MB/s 持续 60s（12 样本）
- idle → truly_stuck：停留 idle > 900s 且 elapsed ≥ 300s

## 场景 3 时间序列设计

```
t=0-295s（59 样本）：冷启动期，全 0 信号 → SM 停留 idle，记录 warning，豁免 truly_stuck
t=300s（第 60 样本）：elapsed=300 >= COLD_START_SECS，冷启动期结束
t=300-1199s（样本 60-299）：全 0 信号，idle 态持续累积（idle_duration → 900s）
t=1200s（第 240 样本）：idle_duration = 900s，触发 idle → truly_stuck
```

场景 3 总 sample 数：至少 (1200/5)+1 = 241 个样本，覆盖 t=0..1200s。

## 场景 4 时间序列设计

```
t=0-295s（59 样本）：全 0 信号，在冷启动豁免期内
期望：state=idle + warnings = ["cold_start_silence_suspected_stuck"]，SIGINT=0
```

## Fixture 生成说明

所有 fixture 由 `tests/fixtures/generate_stuck_fixtures.py` 脚本生成（一次性，可重复运行）。
直接提交 `.jsonl` 文件，CI 读取即可，无需运行时生成。
