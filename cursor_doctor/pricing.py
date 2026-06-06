"""Cursor 定价选型矩阵 — 帮你快速决策选哪个套餐"""

from dataclasses import dataclass
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich.text import Text
from rich.columns import Columns
from rich import box

console = Console()

@dataclass
class Plan:
    """单个 Cursor 套餐"""
    name: str
    price: str            # 显示价格
    price_monthly: float  # 月费
    price_annual: float   # 年费(月均)
    features: list[str]
    pros: list[str]
    cons: list[str]
    best_for: str
    tier: str             # free / pro / business / ultra

PLANS: list[Plan] = [
    Plan(
        name="Free (入門)",
        tier="free",
        price="免費",
        price_monthly=0,
        price_annual=0,
        features=[
            "2000 次补全/月",
            "50 次慢速请求/月",
            "基础AI模型",
            "社区支持",
        ],
        pros=["完全免费", "适合尝鲜体验", "无需信用卡"],
        cons=["请求次数极低", "模型受限", "无上下文感知"],
        best_for="刚接触AI编程、偶尔使用",
    ),
    Plan(
        name="Pro (主流)",
        tier="pro",
        price="USD $20/月",
        price_monthly=20,
        price_annual=16,
        features=[
            "不限次 AI 补全 ⭐ NEW",
            "不限次 Agent 工具调用 ⭐ NEW",
            "高级AI模型 (GPT-5/Claude 4)",
            "长上下文 (200K)",
            "优先支持",
        ],
        pros=[
            "最热门选择",
            "取消500次限制后性价比暴涨",
            "完整AI功能",
            "个人开发者够用",
        ],
        cons=["单人使用", "无团队协作功能", "不能报销发票"],
        best_for="独立开发者、自由职业、个人项目",
    ),
    Plan(
        name="Business (团队)",
        tier="business",
        price="USD $60/月",
        price_monthly=60,
        price_annual=48,
        features=[
            "Pro 所有功能",
            "团队管理后台",
            "管理员控制",
            "用量分析面板",
            "SSO 单点登录",
            "优先邮件支持",
        ],
        pros=[
            "团队协作 & 管理",
            "企业发票报销",
            "集中精力管控",
            "限时促销 70% off ⚡",
        ],
        cons=["价格较高", "个人用性价比低于Pro", "团队规模有限制"],
        best_for="小团队、初创公司、需要管理功能的企业",
    ),
    Plan(
        name="Ultra (旗舰)",
        tier="ultra",
        price="USD $200/月",
        price_monthly=200,
        price_annual=160,
        features=[
            "Pro 所有功能",
            "自定义模型接入",
            "私有部署选项",
            "无限上下文",
            "专属客户经理",
            "SLA 保障 (99.9%)",
            "高级安全审计",
            "自定义数据保留",
        ],
        pros=[
            "最强功能",
            "10x 速度 (优先队列)",
            "私有化部署",
            "企业级安全",
        ],
        cons=["价格昂贵", "对个人/小团队过度配置", "需要合同",
              "2026年5月新推出，生态不成熟"],
        best_for="大型企业、合规需求、私有部署需求",
    ),
]


def render_decision_tree() -> None:
    """展示定价决策树 - 帮助用户快速选型"""
    tree = Panel(
        "[bold cyan]🎯 Cursor 定价决策树[/]\n\n"
        "[dim]问自己:[/]\n\n"
        "  [yellow]Q1:[/] 每月AI编程 [bold]超过 10 小时[/bold]？\n"
        "    ├─ 否 → [green]Free 或 Pro[/]\n"
        "    └─ 是 → [yellow]Q2[/]\n\n"
        "  [yellow]Q2:[/] 需要 [bold]团队协作/管理[/bold] + 能 [bold]报销[/bold]？\n"
        "    ├─ 否 → [green]Pro ($20/月) ✅[/] ⬅️ [bold yellow]90% 开发者的最佳选择[/]\n"
        "    └─ 是 → [yellow]Q3[/]\n\n"
        "  [yellow]Q3:[/] 团队 [bold]> 10人[/]？或需 [bold]私有部署/SLA/审计[/bold]？\n"
        "    ├─ 否 → [green]Business ($60/月)[/]\n"
        "    └─ 是 → [green]Ultra ($200/月)[/]\n\n"
        "[dim]💡 提示: 新 Pro 取消了 500 次限制 + 工具调用限制，[/]"
        "[dim]现在 Pro 是个人开发者的绝对性价比之选。[/]",
        border_style="cyan",
        title="决策树",
        padding=(1, 2),
    )
    console.print(tree)


def render_comparison_table() -> Table:
    """渲染定价对比表"""
    table = Table(
        title="📊 Cursor 套餐对比 (2026年6月最新)",
        box=box.HEAVY_EDGE,
        show_header=True,
        header_style="bold white",
        title_style="bold cyan",
    )
    table.add_column("特性", style="cyan", no_wrap=True, width=22)
    table.add_column("Free", justify="center", style="dim")
    table.add_column("Pro $20", justify="center", style="green bold")
    table.add_column("Business $60", justify="center", style="yellow")
    table.add_column("Ultra $200", justify="center", style="red")

    rows = [
        ("AI 补全次数", "2000/月", "无限 ⭐", "无限", "无限"),
        ("Agent 工具调用", "❌", "无限 ⭐", "无限", "无限"),
        ("上下文长度", "8K", "200K", "200K", "无限制"),
        ("高级模型", "基础", "✅", "✅", "✅ + 自定义"),
        ("团队管理", "❌", "❌", "✅", "✅"),
        ("SSO/发票", "❌", "❌", "✅", "✅"),
        ("SLA 保障", "❌", "❌", "❌", "✅ 99.9%"),
        ("私有部署", "❌", "❌", "❌", "✅"),
        ("适合谁", "尝鲜", "👤 个人", "👥 小团队", "🏢 企业"),
    ]

    for row in rows:
        table.add_row(*row)

    return table


def render_migration_guide() -> None:
    """500次限制 → 无限迁移指南"""
    guide = Panel(
        "[bold yellow]📋 500次限制 → 无限使用：你需要知道的一切[/]\n\n"
        "[bold]变化了什么？[/]\n"
        "  ✅ Cursor Pro 已取消 [red]每月500次[/] 请求限制\n"
        "  ✅ Agent 工具调用也 [red]不再计次[/]\n"
        "  ✅ 高级模型不再限流\n\n"
        "[bold]你是哪种情况？[/]\n\n"
        "  [cyan]1.[/] 已是 Pro 用户，之前被500次卡住\n"
        "     → [green]无需操作[/]！限制已自动解除。重启 Cursor 体验无限次\n\n"
        "  [cyan]2.[/] 之前因500次限流而没续费 / 降级了\n"
        "     → [green]重新订阅 Pro ($20/月)[/]。比之前实际价值 [bold]翻倍[/]\n\n"
        "  [cyan]3.[/] 用的是 Free 版，担心付费\n"
        "     → Pro 现在 [bold]性价比极高[/]，一小时的外卖钱换无限AI编程\n\n"
        "  [cyan]4.[/] 之前在 60刀 Business，现在纠结要不要降到 Pro\n"
        "     → 问自己：还用团队管理、SSO、发票报销吗？\n"
        "       ✅ 需要 → 留 Business（可找促销 70% off 降到 $18/月）\n"
        "       ❌ 不需要 → 降级到 Pro，每小时省 $1.3\n\n"
        "[bold yellow]⚠️ 注意事项:[/]\n"
        "  • Cursor 保留 Fair Use 政策，禁止明显滥用（如多账号共享）\n"
        "  • Ultra $200 暂不推荐个人开发者，过度配置\n"
        "  • Business 60刀 团购/代充可能有风险，建议官网直购\n\n"
        "[dim]数据来源: 2026年6月 V2EX 101条讨论 + CSDN 55篇文章 + Cursor 官方公告[/]",
        border_style="yellow",
        title="迁移指南",
        padding=(1, 2),
    )
    console.print(guide)


def render_pricing_matrix() -> None:
    """完整定价页面：决策树 + 对比表 + 迁移指南"""
    render_decision_tree()
    console.print()
    console.print(render_comparison_table())
    console.print()
    render_migration_guide()


def get_recommendation(budget: str, team_size: str, hours_per_day: str) -> str:
    """根据用户回答返回推荐套餐"""
    budget_lower = budget.strip().lower()
    team = team_size.strip().lower()
    hours = hours_per_day.strip().lower()

    # 按优先级判断
    if "企业" in team or "10" in team or "大" in team or "私有" in budget:
        return "Ultra ($200/月)"
    if "团队" in team or "多人" in team or "管理" in budget or "报销" in budget:
        return "Business ($60/月)"
    if "免费" in budget or "0" in budget or "不想付费" in budget:
        return "Free (免费)"
    # 默认推荐 Pro（性价比之王）
    return "Pro ($20/月) ⭐ 推荐"
