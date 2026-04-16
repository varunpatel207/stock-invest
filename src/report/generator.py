import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

from src.crawler.models import Portfolio, Holding

logger = logging.getLogger(__name__)


class ReportGenerator:
    def __init__(self, template_dir: str = "resources/report"):
        self.template_dir = Path(template_dir)
        self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))

    @staticmethod
    def get_high_conviction_holdings(portfolio: Portfolio) -> List[Holding]:
        if not portfolio.holdings:
            return []

        num_stocks = len(portfolio.holdings)
        threshold = 100.0 / num_stocks

        high_conviction = [
            h for h in portfolio.holdings
            if h.percentage >= threshold
        ]

        # Sort by percentage descending
        return sorted(high_conviction, key=lambda h: h.percentage, reverse=True)

    @staticmethod
    def build_portfolio_context(portfolio: Portfolio) -> Dict[str, Any]:
        high_conviction = ReportGenerator.get_high_conviction_holdings(portfolio)
        num_holdings = len(portfolio.holdings)
        threshold = 100.0 / num_holdings if num_holdings > 0 else 0

        return {
            'name': portfolio.name,
            'url': portfolio.url,
            'total_value': portfolio.total_value,
            'last_updated': portfolio.last_updated,
            'num_holdings': num_holdings,
            'high_conviction_count': len(high_conviction),
            'threshold': threshold,
            'high_conviction_holdings': [
                {
                    'symbol': h.symbol,
                    'stock_name': h.stock_name,
                    'percentage': h.percentage,
                    'value': h.value,
                    'shares': h.shares,
                    'reported_price': h.reported_price,
                    'current_price': h.current_price,
                    'price_change_percent': h.price_change_percent,
                    'week_low': h.week_low,
                    'week_high': h.week_high,
                    'activity': h.activity,
                    'activity_type': 'add' if ('Add' in h.activity or 'Buy' in h.activity)
                                    else ('reduce' if ('Reduce' in h.activity or 'Sell' in h.activity)
                                    else 'neutral'),
                    'price_direction': 'positive' if h.price_change_percent >= 0 else 'negative',
                }
                for h in high_conviction
            ]
        }

    def build_report_context(self, portfolios: List[Portfolio]) -> Dict[str, Any]:
        portfolio_contexts = [
            self.build_portfolio_context(p) for p in portfolios
        ]

        return {
            'report_date': datetime.now().strftime("%B %d, %Y at %I:%M %p"),
            'portfolios': portfolio_contexts,
            'total_portfolios': len(portfolio_contexts),
            'total_investors': len(portfolio_contexts),
        }

    def generate_html_report(self, portfolios: List[Portfolio]) -> str:
        # Build context
        context = self.build_report_context(portfolios)

        # Render template
        template = self.env.get_template("portfolio_report.html")
        html = template.render(**context)

        return html

    def save_report(self, portfolios: List[Portfolio], output_path: str) -> str:
        html = self.generate_html_report(portfolios)

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            f.write(html)

        logger.info(f"Report saved to {output_file}")
        return str(output_file)
