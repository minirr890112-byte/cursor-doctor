"""
Cursor 错误签名数据库 — 基于中文社区 77 条 Cursor 报错/崩溃信号提取
"""
from dataclasses import dataclass, field
from typing import Callable, Optional
import re

@dataclass
class ErrorSignature:
    """单个 Cursor 错误/异常的特征描述"""
    id: str
    name: str
    category: str
    severity: str           # critical / high / medium / low
    symptoms: list[str]     # 用户感知的症状关键词
    log_patterns: list[str] # 日志/错误信息中的正则模式
    diagnosis: str          # 中文诊断描述
    fix_hint: str           # 修复方案关键词
    frequency: int          # 社区出现频率 (来自77条信号统计)
    platform: str = "all"   # mac / win / linux / all
    workaround: str = ""    # 临时解决方案

# ============================================
# 核心错误分类
# ============================================

SIGNATURES: list[ErrorSignature] = [
    # --- MCP/Agent 连接类 (频率最高, 25+) ---
    ErrorSignature(
        id="MCP-001",
        name="MCP Client Closed",
        category="mcp_connection",
        severity="critical",
        symptoms=["MCP Server连接失败", "Client Closed", "Agent无法启动", "MCP自动断开"],
        log_patterns=[
            r"MCP\s*(Client|Server).*closed",
            r"MCP.*connection.*refused",
            r"MCP.*timeout",
            r"Failed to connect to MCP",
        ],
        diagnosis="MCP (Model Context Protocol) 客户端与服务端连接断开。常见原因：端口被占用、防火墙拦截、代理冲突。",
        fix_hint="重启Cursor / 检查端口 8090-8099 / 关闭VPN / 重置MCP配置",
        frequency=15,
    ),
    ErrorSignature(
        id="MCP-002",
        name="Shell Parse Failure",
        category="mcp_connection",
        severity="critical",
        symptoms=["Shell解析失败", "命令执行错误", "Agent卡住", "无法运行Shell命令"],
        log_patterns=[
            r"Shell.*parse.*fail",
            r"shell.*error",
            r"Failed to (parse|execute).*shell",
            r"Invalid shell command",
        ],
        diagnosis="Cursor Agent 在执行 Shell 命令时解析失败。通常由 PATH 环境变量配置错误、特殊字符转义问题引起。",
        fix_hint="检查 ~/.zshrc / 确保 PATH 正确 / 简化命令中的特殊字符",
        frequency=12,
    ),
    ErrorSignature(
        id="MCP-003",
        name="Unauthorized / Token Expired",
        category="mcp_connection",
        severity="high",
        symptoms=["未授权", "Token过期", "登录失效", "Auth失败", "需要重新登录"],
        log_patterns=[
            r"(unauthorized|Unauthorized)",
            r"token.*(expired|invalid)",
            r"auth.*fail",
            r"401.*unauthorized",
        ],
        diagnosis="Cursor 授权 token 过期或被服务器拒绝。可能原因：账号在多设备登录、token 自然过期、网络代理干扰认证请求。",
        fix_hint="重新登录 Cursor / 清除 Cursor 缓存 / 检查代理设置",
        frequency=10,
    ),

    # --- Crashes (10+) ---
    ErrorSignature(
        id="CRASH-001",
        name="Cursor 启动崩溃 / 白屏",
        category="crash",
        severity="critical",
        symptoms=["白屏", "启动闪退", "无法打开", "启动后自动关闭"],
        log_patterns=[
            r"Segmentation fault",
            r"crash.*on startup",
            r"Application.*exit.*unexpected",
            r"Electron.*(crash|fatal)",
        ],
        diagnosis="Cursor 启动时直接崩溃或白屏。常见于更新后缓存冲突、GPU 渲染兼容性问题、系统缺少必要依赖。",
        fix_hint="清除 Cursor 缓存 / 禁用 GPU 加速 / 重新安装",
        frequency=8,
    ),
    ErrorSignature(
        id="CRASH-002",
        name="Plugin/Extension 崩溃",
        category="crash",
        severity="high",
        symptoms=["插件崩溃", "扩展报错", "插件无法加载", "Extension Host 崩溃"],
        log_patterns=[
            r"Extension.*(crash|failed|error)",
            r"plugin.*unexpected",
            r"Extension Host.*terminated",
        ],
        diagnosis="Cursor 的 VS Code 扩展插件崩溃。问题插件会拖垮整个 Cursor 扩展宿主进程。",
        fix_hint="禁用最近安装的扩展 / 安全模式启动 / 删除 extensions 目录缓存",
        frequency=6,
    ),
    ErrorSignature(
        id="CRASH-003",
        name="内存溢出 (OOM)",
        category="crash",
        severity="high",
        symptoms=["内存占用高", "卡顿", "系统提示内存不足", "Cursor卡死后无响应"],
        log_patterns=[
            r"Out of memory",
            r"Memory.*allocation.*fail",
            r"heap.*out of memory",
            r"JavaScript heap",
        ],
        diagnosis="Cursor 进程内存耗尽导致崩溃。常见于大型项目、AI 对话历史过长、大量打开文件。",
        fix_hint="关闭不用的文件 / 限制 AI 对话上下文 / 增加系统交换空间",
        frequency=5,
    ),

    # --- AI/Agent 功能类 (15+) ---
    ErrorSignature(
        id="AI-001",
        name="AI 请求失败 / 超时",
        category="ai_agent",
        severity="high",
        symptoms=["AI不响应", "请求超时", "生成被中断", "AI报错Network Error"],
        log_patterns=[
            r"(AI|Agent).*(timeout|fail|error)",
            r"Network.*error.*(AI|completion)",
            r"Request.*aborted",
            r"API.*(timeout|rate limit)",
        ],
        diagnosis="AI 补全/对话请求失败或超时。通常是网络问题、API 限流、或代理配置导致 AI 服务不可达。",
        fix_hint="检查代理/VPN / 更换网络 / 等待限流冷却 / 使用镜像 API",
        frequency=12,
    ),
    ErrorSignature(
        id="AI-002",
        name="AI 补全不准确 / 答非所问",
        category="ai_agent",
        severity="medium",
        symptoms=["代码补全错误", "回答偏离上下文", "建议质量下降", "AI降智"],
        log_patterns=[
            r"completion.*unexpected",
            r"response.*(gibberish|nonsense)",
            r"model.*(degrad|downgrade)",
        ],
        diagnosis="AI 补全质量异常下降。可能反映了模型端降智、上下文窗口过载、或系统提示被错误覆盖。",
        fix_hint="关闭并重新打开 Cursor / 减少对话上下文 / 切换模型",
        frequency=8,
    ),
    ErrorSignature(
        id="AI-003",
        name="Agent 循环 / 不终止",
        category="ai_agent",
        severity="medium",
        symptoms=["Agent一直运行", "不停尝试", "死循环", "无法停止Agent"],
        log_patterns=[
            r"agent.*(loop|infinite|stuck)",
            r"iteration.*limit.*reached",
            r"too many (retries|attempts)",
        ],
        diagnosis="Cursor Agent 陷入执行循环无法自行终止。通常由于错误反馈循环、权限不足反复重试导致。",
        fix_hint="手动终止 Agent / 检查命令权限 / 重新表述问题 / 重启 Cursor",
        frequency=5,
    ),

    # --- 网络/代理类 (8+) ---
    ErrorSignature(
        id="NET-001",
        name="代理冲突导致连接失败",
        category="network_proxy",
        severity="high",
        symptoms=["无法连接服务器", "代理设置异常", "SSL证书错误", "连接不稳定"],
        log_patterns=[
            r"proxy.*(error|fail|conflict)",
            r"SSL.*(certificate|handshake).*fail",
            r"tunnel.*error",
            r"ECONNRESET|ECONNREFUSED",
        ],
        diagnosis="本地代理/VPN 与 Cursor 内置代理设置冲突，导致 API 请求被拦截或路由异常。",
        fix_hint="关闭系统代理 / 在 Cursor 设置中配置代理 / 使用系统代理模式",
        frequency=8,
    ),
    ErrorSignature(
        id="NET-002",
        name="GFW / 网络不可达",
        category="network_proxy",
        severity="critical",
        symptoms=["无法访问Cursor服务", "总是Network Error", "中国地区连接失败"],
        log_patterns=[
            r"ENOTFOUND.*cursor",
            r"network.*(unreachable|blocked)",
            r"(DNS|resolve).*failure",
            r"connection.*(refused|reset|timed out)",
        ],
        diagnosis="Cursor 云服务在中国大陆网络不可达（GFW 阻断）。常见于国内用户直接使用官方源。",
        fix_hint="配置国内镜像 / 使用科学上网 / Cursor 设置中配置 HTTP 代理",
        frequency=5,
    ),

    # --- 配置/环境类 (10+) ---
    ErrorSignature(
        id="CFG-001",
        name="Cursor 配置损坏",
        category="config_env",
        severity="high",
        symptoms=["设置失效", "配置丢失", "自定义快捷键失效", "主题失效"],
        log_patterns=[
            r"config.*(corrupt|invalid|fail)",
            r"settings\.json.*(error|parse)",
            r"failed to (load|read).*config",
        ],
        diagnosis="Cursor 配置文件（settings.json / keybindings.json）损坏或格式错误。",
        fix_hint="删除 ~/.cursor/settings.json 备份并恢复 / 重置为默认配置",
        frequency=7,
    ),
    ErrorSignature(
        id="CFG-002",
        name="Python 环境/解释器未找到",
        category="config_env",
        severity="medium",
        symptoms=["Python解释器未找到", "Jupyter无法启动", "Python插件报错"],
        log_patterns=[
            r"Python.*(interpreter|path).*(not found|missing|invalid)",
            r"no.*python.*(found|selected)",
            r"jupyter.*(kernel|startup).*error",
        ],
        diagnosis="Cursor 未配置正确的 Python 解释器路径，导致 Python 插件和 Jupyter 支持失效。",
        fix_hint="在 Cursor 中配置 Python 解释器 / 安装 Python 扩展 / 检查 pyenv 配置",
        frequency=6,
    ),
    ErrorSignature(
        id="CFG-003",
        name="Node.js / npm 环境异常",
        category="config_env",
        severity="medium",
        symptoms=["npm命令失败", "Node.js报错", "前端开发环境异常"],
        log_patterns=[
            r"node.*(not found|version|error)",
            r"npm.*(ERR|error|fail)",
            r"nvm.*(not found|version)",
        ],
        diagnosis="Node.js/npm 环境问题导致 Cursor 依赖的前端工具链运行异常。",
        fix_hint="检查 nvm/node 版本 / npm install 重新安装依赖 / 确认 .nvmrc",
        frequency=5,
    ),

    # --- 文件/同步类 (5+) ---
    ErrorSignature(
        id="SYNC-001",
        name="Cursor 同步冲突/失败",
        category="sync_setting",
        severity="medium",
        symptoms=["设置同步失败", "多设备同步冲突", "同步后配置丢失"],
        log_patterns=[
            r"sync.*(fail|conflict|error)",
            r"settings.*sync.*(failed|error)",
            r"conflict.*(detected|resolution)",
        ],
        diagnosis="Cursor 多设备设置同步出现冲突或失败。常见于同时编辑配置、网络中断时同步。",
        fix_hint="手动选择同步版本 / 关闭自动同步 / 清除云端同步数据",
        frequency=4,
    ),
    ErrorSignature(
        id="SYNC-002",
        name="文件监视异常 (File Watcher)",
        category="sync_setting",
        severity="low",
        symptoms=["文件变化不刷新", "文件监视失败", "自动保存异常"],
        log_patterns=[
            r"file.*watcher.*(error|fail|limit)",
            r"(inotify|fsevents).*(limit|error)",
            r"too many open files",
        ],
        diagnosis="系统文件监视器达到上限，导致 Cursor 无法跟踪文件变化。macOS 上常见于大型 monorepo 项目。",
        fix_hint="增大文件监视上限 / 排除 node_modules / 关闭不必要的大目录",
        frequency=3,
    ),

    # --- 订阅/套餐类 (10+, 2026年6月新增) ---
    ErrorSignature(
        id="PRC-001",
        name="Curosr 套餐选择困惑",
        category="pricing_plan",
        severity="medium",
        symptoms=["不知道该选哪个套餐", "20刀vs60刀", "Pro还是Business", "Ultra值不值", "套餐对比"],
        log_patterns=[
            r"plan.*(confuse|confusion|unclear)",
            r"subscription.*(question|issue|problem)",
            r"which.*plan",
            r"pricing.*(confuse|change|update)",
            r"(pro|business|ultra).*(which|vs|compare)",
        ],
        diagnosis="Cursor 2026年5月定价调整后，用户困惑于 Pro($20)、Business($60)、Ultra($200) 哪个最适合自己。取消500次限制后加剧了选择困难。",
        fix_hint="运行 cursor-doctor pricing 查看决策树 / 90%个人开发者选 Pro $20",
        frequency=10,
        workaround="先试用 Pro，不满意再升级 — Cursor 支持随时升降级",
    ),
    ErrorSignature(
        id="PRC-002",
        name="500次限制迁移困惑",
        category="pricing_plan",
        severity="medium",
        symptoms=["500次怎么办", "之前500次限流", "取消限制后不知道", "Pro 限制是不是没了", "额度恢复"],
        log_patterns=[
            r"(500|配额|quota).*(limit|限制|次数)",
            r"request.*limit.*(removed|gone|change)",
            r"取消.*(500|限制|quota)",
            r"unlimited.*(now|update|change)",
        ],
        diagnosis="历史用户对 Pro 从'每月500次'变'不限次'的迁移感到困惑：已取消的要不要续费？被限流过的要怎么恢复？",
        fix_hint="运行 cursor-doctor pricing 查看迁移指南 / 重启 Cursor 自动解除限制",
        frequency=8,
        workaround="所有 Pro 用户已自动升级到无限次，无需操作",
    ),
    ErrorSignature(
        id="PRC-003",
        name="代充/团购/合租风险",
        category="pricing_plan",
        severity="high",
        symptoms=["代充被骗", "团购被封", "合租账号被封", "咸鱼买Cursor被封", "便宜订阅有风险"],
        log_patterns=[
            r"(代充|团购|合租|共享).*(风险|封|骗|问题)",
            r"account.*(banned|suspended).*(third.?party|shared)",
            r"subscription.*(fraud|unauthorized|shared)",
            r"(third.?party|shared|group).*subscription",
        ],
        diagnosis="通过非官方渠道（咸鱼、淘宝代充、团购、合租）购买 Cursor 订阅存在封号风险。Cursor 会检测异常支付和多设备共享。",
        fix_hint="官方渠道订阅 cursor.com / 个人使用不超过2设备 / 避免代充和合租",
        frequency=6,
        platform="all",
    ),

    # --- 性能卡顿类 (8+, 2026年6月新增) ---
    ErrorSignature(
        id="PERF-001",
        name="Cursor 卡顿/响应缓慢",
        category="performance",
        severity="high",
        symptoms=["Cursor很卡", "打字延迟", "界面不流畅", "慢得像PPT", "滚动卡顿"],
        log_patterns=[
            r"(lag|slow|freeze|stutter|延迟|卡顿)",
            r"performance.*(degrad|issue|problem)",
            r"render.*(delay|slow|timeout)",
            r"UI.*(unresponsive|blocked|hang)",
            r"event.*loop.*(block|delay)",
        ],
        diagnosis="Cursor 使用一段时间后变得卡顿。常见原因：AI对话历史过长（内存膨胀）、项目文件数过多、扩展插件堆积、GPU渲染问题。",
        fix_hint="关闭不需要的对话 tab / 关闭未使用的扩展 / 重启 Cursor / 清除 Cursor 缓存",
        frequency=8,
    ),
    ErrorSignature(
        id="PERF-002",
        name="AI 对话响应慢 / 排队",
        category="performance",
        severity="high",
        symptoms=["AI半天不回", "排队中", "等待中", "生成很慢", "响应超时只给一半"],
        log_patterns=[
            r"(queue|排队|等待).*(long|time|timeout)",
            r"response.*(slow|delay|timeout)",
            r"generation.*(cancel|stop|interrupt)",
            r"taking.*too.*long",
            r"(throttle|rate.?limit)",
        ],
        diagnosis="AI 对话/补全响应极慢，常见于高峰期排队、API 限流、或网络延迟。Ultra 用户有优先队列可缓解。",
        fix_hint="避开高峰期使用 / 更换节点 / 升级 Ultra 享受优先队列 / 检查代理延迟",
        frequency=7,
    ),
    ErrorSignature(
        id="PERF-003",
        name="项目索引卡住/一直转圈",
        category="performance",
        severity="medium",
        symptoms=["索引一直转圈", "索引到99%不动", "代码提示不准确", "项目索引失败"],
        log_patterns=[
            r"index.*(stuck|hang|fail|never.*finish)",
            r"indexing.*(stalled|timeout|error)",
            r"semantic.*index.*(fail|error)",
            r"embedding.*(fail|timeout|error)",
        ],
        diagnosis="Cursor 的项目代码索引进程卡住。原因：大型node_modules被索引、磁盘空间不足、索引进程被系统中断。",
        fix_hint="在 Cursor 设置排除 node_modules / 重启索引 / 清除索引缓存 / 检查磁盘空间",
        frequency=5,
    ),

    # --- 更新/升级类 (7+, 2026年6月新增) ---
    ErrorSignature(
        id="UPD-001",
        name="自动更新失败 / 更新卡住",
        category="update_issue",
        severity="medium",
        symptoms=["更新失败", "下载卡住", "更新后打不开", "update loop 循环更新"],
        log_patterns=[
            r"update.*(fail|error|stuck|corrupt)",
            r"download.*(fail|interrupt|corrupt)",
            r"auto.?update.*(error|problem)",
            r"install.*update.*(fail|error)",
        ],
        diagnosis="Cursor 自动更新失败或进入更新循环。常见原因：网络问题下载不完整、权限不足、杀毒软件拦截更新进程。",
        fix_hint="手动下载最新版安装 / 关闭杀毒软件后重试 / 用终端运行 cursor --update",
        frequency=6,
    ),
    ErrorSignature(
        id="UPD-002",
        name="更新后崩溃/不兼容",
        category="update_issue",
        severity="critical",
        symptoms=["更新后白屏", "更新后闪退", "版本不兼容", "更新后配置丢失", "新版无法打开"],
        log_patterns=[
            r"after.*update.*(crash|white|blank)",
            r"update.*(broke|break|incompatible)",
            r"version.*(mismatch|incompatible|rollback)",
            r"downgrade.*(needed|required)",
        ],
        diagnosis="Cursor 更新到新版本后出现崩溃、白屏、闪退等严重问题。一般是新版本bug、系统兼容性问题、或旧配置不兼容新版本。",
        fix_hint="回滚旧版本 / 清除配置文件 / 安全模式启动 / 等待hotfix更新",
        frequency=5,
    ),
    ErrorSignature(
        id="UPD-003",
        name="macOS 兼容性问题",
        category="update_issue",
        severity="high",
        symptoms=["macOS更新后打不开", "macOS版本太老", "26.x不兼容", "Apple Silicon兼容问题"],
        log_patterns=[
            r"macOS.*(version|compatible|update)",
            r"(apple|mac|macOS).*(silicon|m1|m2|m3|m4|arm64)",
            r"not.*(compatible|supported).*(mac|macOS)",
            r"rosetta.*(issue|problem|error)",
        ],
        diagnosis="Cursor 在 macOS 特定版本（如26.x Beta）上出现兼容性问题，或 Apple Silicon 原生支持不完善。",
        fix_hint="确认 macOS >= 13.0 / 用 Rosetta 模式运行 / 不要用 Beta 版 macOS / 等待官方适配",
        frequency=4,
        platform="mac",
    ),

    # --- 账号/登录类 (6+, 2026年6月新增) ---
    ErrorSignature(
        id="ACC-001",
        name="登录循环 / 反复要求重新登录",
        category="account_auth",
        severity="high",
        symptoms=["反复登录", "登录后又被踢", "会话过期超快", "登录循环Authentication loop"],
        log_patterns=[
            r"(login|auth|sign.?in).*(loop|repeat|again|expire)",
            r"session.*(expired|invalid|revoke)",
            r"token.*(expired|invalid|refresh.*fail)",
            r"re.?auth.*(required|needed|prompt)",
        ],
        diagnosis="Cursor 反复要求重新登录，登录后短时间内又被踢出。原因：多设备登录冲突导致 token 被撤销、代理/VPN 触发安全验证、系统时间不同步。",
        fix_hint="单设备使用 / 退出所有设备再登录 / 关闭代理登录 / 检查系统时间",
        frequency=6,
    ),
    ErrorSignature(
        id="ACC-002",
        name="订阅状态异常 / 付款后未生效",
        category="account_auth",
        severity="medium",
        symptoms=["付款了还是免费版", "订阅显示不对", "升级后没生效", "续费后还是过期"],
        log_patterns=[
            r"subscription.*(status|issue|not.*active)",
            r"payment.*(success|done|completed).*(not.*active|still.*free)",
            r"billing.*(error|issue|problem)",
            r"renew.*(fail|not.*reflect|delay)",
        ],
        diagnosis="用户在 Cursor 官网/App内付款后，订阅状态未同步到本地客户端，Pro 功能未解锁。",
        fix_hint="退出重新登录 / 清除 Cursor 缓存后重试 / 等待 1-2 小时同步 / 联系 support@cursor.com",
        frequency=5,
    ),

    # --- MCP/Agent 补充 (新增) ---
    ErrorSignature(
        id="MCP-004",
        name="MCP Server 多实例冲突",
        category="mcp_connection",
        severity="medium",
        symptoms=["MCP端口占用", "MCP启动失败", "地址已被使用", "EADDRINUSE", "多个Cursor实例冲突"],
        log_patterns=[
            r"(EADDRINUSE|address.*already.*in.*use)",
            r"port.*(already|occupied|in.*use)",
            r"MCP.*(already.*running|start.*fail.*port)",
            r"another.*instance.*running",
        ],
        diagnosis="多个 Cursor 实例或 MCP Server 实例同时运行导致端口冲突（默认端口 8090-8099 范围）。",
        fix_hint="关闭所有 Cursor 窗口 / 用 lsof -i:8090 找占用进程 / 修改 MCP 端口配置",
        frequency=4,
    ),
]


# 快速查找函数
def find_matching_signatures(error_text: str) -> list[tuple[ErrorSignature, str]]:
    """在错误文本中匹配已知签名"""
    matches = []
    for sig in SIGNATURES:
        for pattern in sig.log_patterns:
            if re.search(pattern, error_text, re.IGNORECASE):
                matches.append((sig, pattern))
                break
    return matches


def find_by_id(sig_id: str) -> Optional[ErrorSignature]:
    """按 ID 查找签名"""
    for sig in SIGNATURES:
        if sig.id == sig_id:
            return sig
    return None


def count_by_category() -> dict[str, int]:
    """统计各类别签名数量"""
    counts: dict[str, int] = {}
    for sig in SIGNATURES:
        counts[sig.category] = counts.get(sig.category, 0) + 1
    return counts


CATEGORY_NAMES: dict[str, str] = {
    "mcp_connection": "MCP/Agent 连接",
    "crash": "崩溃/闪退",
    "ai_agent": "AI/Agent 功能异常",
    "network_proxy": "网络/代理",
    "config_env": "配置/环境",
    "sync_setting": "文件/同步",
    "pricing_plan": "订阅/套餐",
    "performance": "性能卡顿",
    "update_issue": "更新/升级",
    "account_auth": "账号/登录",
}
