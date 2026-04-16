# Stock Investment Portfolio Crawler

A Python-based crawler that fetches superinvestor portfolios from Dataroma and generates beautiful, multi-investor HTML reports highlighting high-conviction holdings. Perfect for tracking key investor moves and identifying conviction in specific stocks.

## ✨ Features

- **Multi-investor crawling**: Fetch portfolios for 20+ investors simultaneously
- **Detailed holding extraction**: Symbol, price, activity, performance metrics, 52-week range
- **High-conviction identification**: Automatic threshold calculation based on portfolio concentration
- **Jinja2 HTML reports**: Professional, responsive reports ready for email distribution
- **Batch report generation**: All investors in one clean HTML file with sections per investor
- **Timestamp tracking**: Auto-saved reports with date/time stamps

## 🚀 Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Add investors to crawl** (`resources/investors.csv`):
```csv
Investor,URL
Hillman Value Fund,https://www.dataroma.com/m/holdings.php?m=AKO
Dodge & Cox,https://www.dataroma.com/m/holdings.php?m=DDC
Baupost Group,https://www.dataroma.com/m/holdings.php?m=BIF
```

3. **Run the crawler:**
```bash
python main.py
```

Reports are generated in `reports/portfolio_report_YYYYMMDD_HHMMSS.html`

## 📊 What You Get

Each report includes per investor:
- **Portfolio Summary**: Total value, last updated date, holdings count
- **High-Conviction Holdings Table**:
  - Ticker & company name
  - Portfolio concentration %
  - Position value in $
  - Share count
  - Reported vs current price
  - Price change since report date
  - 52-week low/high range
  - Recent activity (Add/Reduce/Buy/Sell)

## 🎯 High-Conviction Formula

Conviction threshold = `100 / (number of holdings)`

Examples:
- Portfolio with 10 holdings → Only show positions ≥10%
- Portfolio with 20 holdings → Only show positions ≥5%
- Portfolio with 22 holdings → Only show positions ≥4.55%

**Why?** Larger allocations indicate stronger confidence in the thesis.

## 📁 Project Structure

```
src/
├── crawler/           # Web scraping & data extraction
│   ├── models.py      # Portfolio & Holding classes
│   ├── crawler.py     # Dataroma scraper + HTML parser
│   └── reader.py      # CSV reader
├── report/            # Report generation
│   └── generator.py   # Jinja2 report generator
└── __init__.py

resources/
├── investors.csv      # Add investors to crawl here
└── report/
    └── portfolio_report.html  # Jinja2 template

reports/               # Generated HTML reports
└── portfolio_report_*.html
```

## 🔍 Example Report Features

- **Color-coded metrics**: Green for gains, red for losses
- **Activity badges**: Visual tags for Add/Reduce/Buy/Sell
- **Responsive design**: Works on desktop, tablet, mobile
- **Print-friendly**: Optimized for printing or PDF export
- **Multi-investor view**: All portfolios in one report for easy comparison

## 🚧 Next Steps

- [ ] Daily email automation
- [ ] Historical tracking & comparison charts
- [ ] Alert system for major position changes
- [ ] Performance metrics dashboard

## 📝 Data Extraction

The crawler parses Dataroma's HTML holdings table and extracts:
- Current & reported prices
- Share counts & portfolio %
- 52-week ranges
- Recent buy/sell activity
- All formatting cleaned for analysis
