import logging

from src.service import PortfolioService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    service = PortfolioService("resources/investors.csv")
    report_path = service.run()
    if report_path:
        service.send_report_email(report_path)


if __name__ == '__main__':
    main()
