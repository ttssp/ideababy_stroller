# RecallKit

RecallKit 是一个 CLI 驱动的单人后训练决策循环工具，让你在本机（单 GPU）上严格顺序地跑 baseline → LoRA SFT → eval → markdown 决策报告，并强制输出含训练曲线、分数对比和失败归因的可复现记录。

> ⚠️ **本项目处于 alpha 开发阶段（v0.1.0.dev0）**，API 随时可能变化，不建议在生产环境使用。

---

## 最低硬件与软件需求

| 项目 | 最低要求 | 推荐配置 |
|------|----------|----------|
| OS | macOS 14+ / Ubuntu 22.04+ | Ubuntu 22.04 LTS |
| GPU | NVIDIA 16GB+（TinyLlama 1.1B demo） | NVIDIA RTX 4090 24GB（Qwen3-4B QLoRA） |
| CUDA | 12.1+ | 12.4 |
| RAM | 32GB | 64GB |
| 磁盘 | 100GB 空余 | 500GB SSD |
| Python | 3.12.x | 3.12.x |
| uv | ≥ 0.5.0 | 最新 |
| Claude Code CLI | 2026-04-latest | 最新 |

<!-- TODO(T027): 在此处补充完整的 Quick Start、Demo 复现步骤、HF_TOKEN 说明等内容 -->
