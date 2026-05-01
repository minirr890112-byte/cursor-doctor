# Cursor Doctor - Cursor IDE 故障诊断工具

Cursor IDE（基于 VS Code 的 AI 编辑器）常见报错、崩溃、配置问题的一键诊断与修复工具。

## 快速开始

```bash
pip install cursor-doctor

# 诊断 Cursor 环境
cursor-doctor diagnose

# 自动修复
cursor-doctor fix

# 匹配错误文本
cursor-doctor match --text "MCP Client Closed"
```

## 功能

- `cursor-doctor diagnose` — 全面诊断 Cursor 健康状态
- `cursor-doctor fix` — 自动修复常见问题
- `cursor-doctor signatures` — 浏览已知错误签名数据库
- `cursor-doctor match --text "<错误信息>"` — 匹配已知错误模式

## 数据来源

基于中文开发者社区 77+ 条 Cursor 报错/崩溃信号分析提取。

## 错误分类

| 分类 | 数量 | 说明 |
|------|------|------|
| MCP/Agent 连接 | 3 | MCP Client Closed, Shell Parse Failure, 授权过期 |
| 崩溃/闪退 | 3 | 启动白屏, 插件崩溃, 内存溢出 |
| AI/Agent 功能异常 | 3 | 请求超时, 补全质量下降, Agent 死循环 |
| 网络/代理 | 2 | 代理冲突, GFW 阻断 |
| 配置/环境 | 3 | 配置损坏, Python 未找到, Node.js 异常 |
| 文件/同步 | 2 | 同步冲突, File Watcher 异常 |
