# 007 = 测试夹具(非真产品 idea)

> **定性**:007「agent-emit / friction-tap」是为**测 006 dogfood 循环**造的合成实验,**不是要 ship 的产品**。
> operator 2026-07-06 确认此定性,补记于此(此前 007 未在 proposals 登记 —— 因为它本就不是产品 idea)。

## 是什么

`007a-agent-emit` 把「摩擦记录」的主语从 operator 反转成 **agent 自录**:Claude session 跑 task 被工具链
卡住的当下(tool 失败 / hook block / retrospective 出 placeholder),session 自己写一行 entry 进 friction-log,
不需要 operator 主动动作。详见 [007a-agent-emit/FORK-ORIGIN.md](./007a-agent-emit/FORK-ORIGIN.md)。

## 为什么是 fake / 不 park 不 abandon

- 它的目的是**验证 006 auto-agentic-coding 框架的 self-monitoring 假设**,产物价值是**框架证据**,非独立产品。
- 它跑通了 L1→L4(见 `007a-agent-emit/007a-pA/`),但那是"证明 dogfood 记录机制可行"的演练,不是产品交付。
- **不 park**(它不是"好 idea 坏时机")**也不 abandon**(它不是"学到不该建")—— 它是**工具/夹具**,任务已达成。

## 归属

- 归 **006 框架族**:006 若重审 dogfood 机制,007 的实测数据(agent 自录 27 条 friction)是硬证据。
- 与投资闭环(004/008/009)无关。
