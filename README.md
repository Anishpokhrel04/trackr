# TrackR

TrackR is a lightweight Python command-line application built for personal finance analysis. It ingests CSV transaction data to automatically identify recurring payments (subscriptions, rent, salaries), compute daily cash flow, project future account balance trends, and generate visual HTML summary reports.

This repository serves as the final submission for the Introduction to Python course.

---

## Key Features

- **CSV Ingestion (`io.py`):** Loads bank transaction files with flexible date formats (`YYYY-MM-DD`, `DD.MM.YYYY`, `MM/DD/YYYY`).
- **Recurring Payment Engine (`analysis.py`):** Groups descriptions and measures transaction intervals to identify repeating fixed expenses and income.
- **Balance Trend Forecasting (`analysis.py`):** Calculates historical daily balances and projects linear trends forward over a configurable date range.
- **Rule-Based Recommendations (`recommend.py`):** Evaluates savings rates and fixed expense ratios to generate actionable advice.
- **Visual Analytics (`visualize.py`):** Plots account balance history and linear projections to high-resolution PNG charts using Matplotlib.
- **Interactive Dashboard (`htmlreport.py`):** Compiles key financial metrics, recurring ledgers, recommendations, and embedded charts into a single standalone `report.html`.

---

## Project Architecture

```text
trackr/
├── data/
│   └── sample_transactions.csv   # Sample transaction dataset for testing
├── output/                       # Default folder for generated HTML & PNG reports
├── src/
│   └── trackr/
│       ├── __init__.py           # Package initialization & version metadata
        ├── __main__.py           # Executable entry point (`python -m trackr`)
        ├── analysis.py           # Core math: recurring detection & projections
        ├── cli.py                # Command-line interface logic (`argparse`)
        ├── htmlreport.py         # Self-contained HTML report builder
        ├── io.py                 # CSV loading and transaction normalization
        ├── models.py             # Dataclass definitions (`Transaction`, `RecurringPayment`)
        ├── recommend.py          # Financial rule and advice engine
        └── visualize.py          # Matplotlib chart rendering module
├── tests/
│   ├── __init__.py
│   └── test_analysis.py          # Pytest unit tests for core logic
├── pyproject.toml                # Project packaging configuration (PEP 621)
└── README.md                     # Comprehensive project documentation