import logging
from pathlib import Path
from datetime import datetime
from typing import List

from src.crawler import DataromaCrawler, InvestorReader
from src.crawler.models import Portfolio
from src.report import ReportGenerator
from src.email import EmailService

logger = logging.getLogger(__name__)


class PortfolioService:
    def __init__(self, csv_path: str = "resources/investors.csv"):
        self.csv_path = csv_path
        self.crawler = DataromaCrawler(timeout=10, delay=1.0)
        self.reader = InvestorReader(csv_path)
        self.report_generator = ReportGenerator()
        self.email_service = EmailService()

    def crawl_portfolios(self) -> List[Portfolio]:
        investors = self.reader.read_investors()

        if not investors:
            logger.error("No investors to crawl")
            return []

        portfolios = []

        for name, url in investors:
            logger.info(f"Crawling {name}...")
            portfolio = self.crawler.crawl_investor(name, url)
            if portfolio:
                portfolios.append(portfolio)
                logger.info(f"  Found {len(portfolio.holdings)} holdings")
            else:
                logger.warning(f"  Failed to crawl {name}")

        logger.info(f"\nSuccessfully crawled {len(portfolios)} investor(s)")
        for portfolio in portfolios:
            logger.info(f"\n{portfolio.name}")
            logger.info(f"  URL: {portfolio.url}")
            logger.info(f"  Total Value: ${portfolio.total_value:,.2f}")
            logger.info(f"  Last Updated: {portfolio.last_updated}")
            logger.info(f"  Holdings: {len(portfolio.holdings)}")

        return portfolios

    def generate_report(self, portfolios: List[Portfolio]) -> str:
        valid_portfolios = [p for p in portfolios if p.holdings]

        if not valid_portfolios:
            logger.warning("No portfolios with holdings found. Skipping report generation.")
            return None

        logger.info("\nGenerating HTML report...")

        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = reports_dir / f"portfolio_report_{timestamp}.html"

        try:
            saved_path = self.report_generator.save_report(valid_portfolios, str(report_path))
            logger.info(f"✓ Report saved to {saved_path}")
            return saved_path
        except Exception as e:
            logger.error(f"✗ Failed to generate report: {e}")
            return None

    def send_report_email(self, report_path: str) -> bool:
        if not report_path:
            logger.warning("No report path provided")
            return False

        return self.email_service.send_report(report_path)

    def run(self) -> str:
        portfolios = self.crawl_portfolios()
        report_path = self.generate_report(portfolios)
        return report_path
