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
## Installation & Setup

### Requirements

Before running TrackR, make sure the following are installed:

* **Python 3.10 or newer**
* **Git**
* **uv** or **pip**

### 1. Clone the Repository

```bash
git clone https://github.com/Anishpokhrel04/trackr.git
cd trackr
```

### 2. Install the Project

Using `uv`:

```bash
uv pip install -e ".[dev]"
```

Or using `pip`:

```bash
python -m venv .venv
```

Activate the virtual environment:

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

Then install TrackR:

```bash
pip install -e ".[dev]"
```

### 3. Verify the Installation

Run:

```bash
python -m trackr --help
```

or:

```bash
uv run -m trackr --help
```

If the installation was successful, TrackR will display the available command-line options.

---

## Input Data Format

TrackR accepts transaction data in **CSV format**.

The CSV file must contain the following three columns:

```csv
date,description,amount
```

### Example

```csv
date,description,amount
2026-03-01,Salary ACME Corp,3200.00
2026-03-01,Landlord Rent Payment,-950.00
2026-03-05,Supermarket Groceries,-45.50
2026-03-10,Netflix,-15.99
2026-04-01,Salary ACME Corp,3200.00
2026-04-01,Landlord Rent Payment,-950.00
2026-04-10,Netflix,-15.99
```

### Column Description

| Column        | Description                            |
| ------------- | -------------------------------------- |
| `date`        | Date of the transaction                |
| `description` | Name or description of the transaction |
| `amount`      | Transaction amount                     |

### Amount Convention

TrackR uses the following convention:

* **Positive values** represent income.
* **Negative values** represent expenses.

For example:

```text
3200.00   → Salary / Income
-950.00   → Rent / Expense
-45.50    → Groceries / Expense
```

### Supported Date Formats

TrackR supports multiple common date formats:

```text
YYYY-MM-DD
DD.MM.YYYY
MM/DD/YYYY
```

Examples:

```text
2026-03-01
01.03.2026
03/01/2026
```

The transaction dates are normalized internally so that transactions can be processed consistently regardless of the input date format.

---

## Running TrackR

Once the project is installed and the CSV data is prepared, run the analysis using:

```bash
uv run -m trackr analyze data/sample_transactions.csv --starting-balance 0.0 --predict-days 30
```

Or with Python:

```bash
python -m trackr analyze data/sample_transactions.csv --starting-balance 0.0 --predict-days 30
```

After execution, the generated files are stored in the `output/` directory:

```text
output/
├── report.html
└── balance_plot.png
```

Open `report.html` in a web browser to view the financial analysis, recurring transactions, recommendations, balance information, and visualization.

---

