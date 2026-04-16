import time
import logging
from typing import Optional
import requests
from bs4 import BeautifulSoup

from src.crawler.models import Portfolio, Holding

logger = logging.getLogger(__name__)


class DataromaCrawler:
    def __init__(self, timeout: int = 10, delay: float = 1.0):
        self.timeout = timeout
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def fetch_page(self, url: str) -> Optional[str]:
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None

    def crawl_investor(self, name: str, url: str) -> Optional[Portfolio]:
        html = self.fetch_page(url)
        if not html:
            return None

        parser = HoldingsParser()
        holdings = parser.parse_holdings(html)
        total_value = parser.parse_total_value(html)
        date = parser.parse_date(html)

        portfolio = Portfolio(
            name=name,
            url=url,
            total_value=total_value,
            last_updated=date
        )

        for holding in holdings:
            portfolio.add_holding(holding)

        time.sleep(self.delay)
        return portfolio


class HoldingsParser:
    def parse_holdings(self, html: str) -> list[Holding]:
        holdings = []
        soup = BeautifulSoup(html, 'lxml')

        # Find the holdings table
        table = soup.find('table', {'id': 'grid'})
        if not table:
            logger.warning("Could not find holdings table")
            return holdings

        # Parse each row in tbody (skip header)
        tbody = table.find('tbody')
        if not tbody:
            logger.warning("Could not find tbody in holdings table")
            return holdings

        rows = tbody.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 12:
                continue

            try:
                # Column 1: Stock symbol and name (in td.stock > a)
                stock_cell = cells[1]
                stock_link = stock_cell.find('a')
                if not stock_link:
                    continue

                # Symbol is the direct text, name is in the span
                symbol = stock_link.contents[0].strip() if stock_link.contents else ""
                stock_name_span = stock_link.find('span')
                stock_name = stock_name_span.get_text(strip=True)[2:] if stock_name_span else ""  # Remove " - " prefix

                # Skip empty rows
                if not symbol:
                    continue

                # Column 2: Percentage of portfolio
                percentage = self._parse_percentage(cells[2].get_text(strip=True))

                # Column 3: Recent Activity
                activity = cells[3].get_text(strip=True)

                # Column 4: Shares
                shares = self._parse_number(cells[4].get_text(strip=True))

                # Column 5: Reported Price
                reported_price = self._parse_currency(cells[5].get_text(strip=True))

                # Column 6: Value
                value = self._parse_currency(cells[6].get_text(strip=True))

                # Column 8: Current Price
                current_price = self._parse_currency(cells[8].get_text(strip=True))

                # Column 9: Price change percent
                price_change_percent = self._parse_percentage(cells[9].get_text(strip=True))

                # Column 10: 52 Week Low
                week_low = self._parse_currency(cells[10].get_text(strip=True))

                # Column 11: 52 Week High
                week_high = self._parse_currency(cells[11].get_text(strip=True))

                holdings.append(Holding(
                    symbol=symbol,
                    stock_name=stock_name,
                    shares=int(shares) if shares else 0,
                    percentage=percentage,
                    reported_price=reported_price,
                    value=value,
                    current_price=current_price,
                    price_change_percent=price_change_percent,
                    week_low=week_low,
                    week_high=week_high,
                    activity=activity
                ))
            except (IndexError, ValueError) as e:
                logger.debug(f"Error parsing row: {e}")
                continue

        return holdings

    def parse_total_value(self, html: str) -> float:
        soup = BeautifulSoup(html, 'lxml')
        # Portfolio info is in p#p2 with spans for each field
        p2 = soup.find('p', {'id': 'p2'})
        if p2:
            spans = p2.find_all('span')
            if len(spans) >= 4:
                # 4th span contains portfolio value
                return self._parse_currency(spans[3].get_text(strip=True))
        return 0.0

    def parse_date(self, html: str) -> str:
        soup = BeautifulSoup(html, 'lxml')
        # Portfolio info is in p#p2 with spans for each field
        p2 = soup.find('p', {'id': 'p2'})
        if p2:
            spans = p2.find_all('span')
            if len(spans) >= 2:
                # 2nd span contains portfolio date
                return spans[1].get_text(strip=True)
        return ""

    @staticmethod
    def _parse_currency(text: str) -> float:
        text = text.replace('$', '').replace(',', '').strip()
        try:
            return float(text)
        except ValueError:
            return 0.0

    @staticmethod
    def _parse_number(text: str) -> float:
        text = text.replace(',', '').strip()
        try:
            return float(text)
        except ValueError:
            return 0.0

    @staticmethod
    def _parse_percentage(text: str) -> float:
        text = text.replace('%', '').strip()
        try:
            return float(text)
        except ValueError:
            return 0.0
