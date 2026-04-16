import logging

from src.service import PortfolioService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    service = PortfolioService("resources/investors.csv")
    service.run()


if __name__ == '__main__':
    main()
