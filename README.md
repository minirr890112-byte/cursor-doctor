# 🩺 Cursor Doctor — Cursor IDE 诊断·定价·修复全能工具

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.2.0-blue?style=flat-square)](https://github.com/minirr890112-byte/cursor-doctor)

> **Cursor IDE 故障诊断、定价选型与修复工具** — 一键诊断 Cursor 报错、崩溃、配置问题，智能推荐套餐，并提供自动修复方案。
> 基于 **V2EX 156条 + CSDN 85篇** 中文开发者社区真实痛点信号。

---

## 🆕 v1.2.0 更新 (2026-06-06)

- 🎯 **定价选型矩阵** — `cursor-doctor pricing` 决策树 + 套餐对比 + 迁移指南
- 📋 **迁移指南** — `cursor-doctor migrate` 500次限制已取消 → 无限使用
- 🔍 **错误签名翻倍** — 14 → 28 条签名，10 个分类（新增定价/性能/更新/账号）
- 📊 **数据驱动** — 基于 V2EX 101条定价讨论 + CSDN 55篇 Cursor文章

---

## 📦 Installation / 安装

```bash
# 方法 1: 直接从 GitHub 安装 (推荐)
pip install git+https://github.com/minirr890112-byte/cursor-doctor.git

# 方法 2: 克隆本地安装
git clone https://github.com/minirr890112-byte/cursor-doctor.git
cd cursor-doctor
pip install -e .
```

**依赖**: Python 3.10+, pip 21.0+

---

## 🚀 Quick Start / 快速开始

```bash
cursor-doctor diagnose       # 诊断 Cursor 环境
cursor-doctor fix            # 自动修复
cursor-doctor pricing        # 🆕 定价选型矩阵
cursor-doctor migrate        # 🆕 500次限→无限迁移指南
cursor-doctor signatures     # 浏览错误签名库
cursor-doctor match --text "MCP Client Closed"  # 匹配错误文本
```

---

## ✨ Features / 功能

| Command | Description |
|---------|-------------|
| `cursor-doctor diagnose` | 全面诊断 Cursor 健康状态（版本、系统环境、错误日志、健康评分） |
| `cursor-doctor fix [category]` | 自动修复常见问题（可选类别: mcp_connection, crash, network_proxy, config_env） |
| `cursor-doctor pricing` | 🆕 Cursor 定价选型矩阵 — 决策树 + 4套餐对比 + FAQ |
| `cursor-doctor migrate` | 🆕 500次限制→无限使用迁移指南 |
| `cursor-doctor signatures` | 浏览 28 种错误签名（10 个分类） |
| `cursor-doctor match --text "..."` | 将错误文本匹配到已知签名 |

---

## 📊 Error Signature Database / 错误签名数据库

基于中文开发者社区 **77+ 条 Cursor 报错信号**分析提取，v1.2.0 覆盖 **10 大类 28 种错误签名**。

| Category / 分类 | Count | Severity | Description |
|-----------------|-------|----------|-------------|
| 🔌 MCP/Agent 连接 | 4 | CRITICAL–MEDIUM | MCP Client Closed, Shell Parse Failure, Token Expired, 多实例冲突 |
| 💥 崩溃/闪退 | 3 | CRITICAL–HIGH | 启动白屏, 扩展崩溃, OOM |
| 🤖 AI/Agent 功能异常 | 3 | HIGH–MEDIUM | AI超时, 补全降级, Agent死循环 |
| 🌐 网络/代理 | 2 | CRITICAL–HIGH | 代理冲突, GFW/网络不通 |
| ⚙️ 配置/环境 | 3 | HIGH–MEDIUM | 配置损坏, Python未找到, Node.js异常 |
| 📁 文件/同步 | 2 | MEDIUM–LOW | 同步冲突, 文件监视上限 |
| 💰 订阅/套餐 | 3 | HIGH–MEDIUM | 🆕 套餐困惑, 500次限迁移, 代充风险 |
| 🐌 性能卡顿 | 3 | HIGH–MEDIUM | 🆕 Cursor卡顿, AI排队, 索引卡住 |
| 🔄 更新/升级 | 3 | CRITICAL–MEDIUM | 🆕 更新失败, 更新后崩溃, macOS兼容 |
| 👤 账号/登录 | 2 | HIGH–MEDIUM | 🆕 登录循环, 订阅未生效 |

---

## 🎯 Pricing Demo / 定价选型演示

```
$ cursor-doctor pricing

╭─────────────────────────────────── 决策树 ───────────────────────────────────╮
│  🎯 Cursor 定价决策树                                                        │
│                                                                              │
│  Q1: 每月AI编程 超过 10 小时？                                               │
│    ├─ 否 → Free 或 Pro                                                       │
│    └─ 是 → Q2                                                                │
│  Q2: 需要 团队协作/管理 + 能 报销？                                          │
│    ├─ 否 → Pro ($20/月) ✅ ⬅️ 90% 开发者的最佳选择                            │
│    └─ 是 → Q3                                                                │

                    📊 Cursor 套餐对比 (2026年6月最新)
┏━━━━━━━━━━━━━━━━━━━━━━━━┯━━━━━━━━┯━━━━━━━━━┯━━━━━━━━━━━━━━┯━━━━━━━━━━━━━┓
┃ 特性                   │  Free  │ Pro $20 │ Business $60 │ Ultra $200  ┃
┠────────────────────────┼────────┼─────────┼──────────────┼─────────────┨
┃ AI 补全次数            │2000/月 │ 无限 ⭐ │     无限     │    无限     ┃
┃ Agent 工具调用         │   ❌   │ 无限 ⭐ │     无限     │    无限     ┃
┃ 适合谁                 │  尝鲜  │ 👤 个人 │  👥 小团队   │   🏢 企业   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━┷━━━━━━━━┷━━━━━━━━━┷━━━━━━━━━━━━━━┷━━━━━━━━━━━━━┛
```

---

## 🏗️ Project Structure / 项目结构

```
cursor-doctor/
├── cursor_doctor/
│   ├── __init__.py          # Package init, version
│   ├── cli.py               # CLI entry (click + rich)
│   ├── diagnose.py          # Core diagnostic engine
│   ├── pricing.py           # 🆕 Pricing matrix & migration guide
│   ├── signatures/
│   │   └── database.py      # 28 error signatures, matching logic
│   └── fixes/
│       └── apply.py         # Auto-fix implementations
├── pyproject.toml
└── README.md
```

---

## 🔗 Also Available on ClawHub

> 🚀 **cursor-doctor** will soon be available as a skill on **[ClawHub](https://clawhub.ai)** — the AI skills marketplace.

---

## 📄 License / 许可证

MIT © [minirr890112-byte](https://github.com/minirr890112-byte)

---

## 🙏 Acknowledgments / 致谢

错误签名提取自中文 Cursor 开发者社区的 **77+ 条真实报错信号**。定价数据基于 **V2EX 101条 + CSDN 55篇** 社区讨论。
