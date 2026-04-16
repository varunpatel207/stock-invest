import logging
from typing import List, Tuple
import pandas as pd

logger = logging.getLogger(__name__)


class InvestorReader:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def read_investors(self) -> List[Tuple[str, str]]:
        try:
            df = pd.read_csv(self.csv_path)
            # Validate required columns
            if 'Investor' not in df.columns or 'URL' not in df.columns:
                logger.error("CSV must contain 'Investor' and 'URL' columns")
                return []

            # Filter out empty rows
            df = df.dropna(subset=['Investor', 'URL'])
            df = df[df['Investor'].str.strip() != '']
            df = df[df['URL'].str.strip() != '']

            investors = list(zip(df['Investor'], df['URL']))
            logger.info(f"Loaded {len(investors)} investors from {self.csv_path}")
            return investors

        except FileNotFoundError:
            logger.error(f"CSV file not found: {self.csv_path}")
            return []
        except Exception as e:
            logger.error(f"Error reading CSV: {e}")
            return []
