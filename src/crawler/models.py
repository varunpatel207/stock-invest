from dataclasses import dataclass, field
from typing import List


@dataclass
class Holding:
    symbol: str
    stock_name: str = ""
    shares: int = 0
    percentage: float = 0.0
    reported_price: float = 0.0
    value: float = 0.0
    current_price: float = 0.0
    price_change_percent: float = 0.0
    week_low: float = 0.0
    week_high: float = 0.0
    activity: str = ""


@dataclass
class Portfolio:
    name: str
    url: str
    holdings: List[Holding] = field(default_factory=list)
    total_value: float = 0.0
    last_updated: str = ""

    def add_holding(self, holding: Holding) -> None:
        self.holdings.append(holding)
