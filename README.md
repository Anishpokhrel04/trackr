# TrackR

TrackR is a simple personal finance CLI tool written in Python. You can give it a CSV file of bank transactions, and it will find recurring payments (like subscriptions or rent), estimate your future account balance based on spending trends, print basic recommendations, and output an HTML report with a plot.

This project was built for the Introduction to Python course final project.

## Features

- Parses transaction CSV files with dates in `YYYY-MM-DD`, `DD.MM.YYYY`, or `MM/DD/YYYY` format.
- Groups transactions by description to detect repeating monthly or weekly payments.
- Simple linear prediction of future balance over a given number of days.
- Calculates savings rates and outputs financial advice.
- Saves a plot of balance history to a `.png` file using Matplotlib.
- Generates a standalone `report.html` file with summary statistics and charts.

## Project Structure

```text
trackr/
├── data/
│   └── sample_transactions.csv   # Example transaction file
├── output/                       # Output directory for generated reports & plots
├── pyproject.toml                # Build and dependency setup
├── README.md
└── src/
    └── trackr/
        ├── __init__.py           # Package version and exports
        ├── __main__.py           # Main entry point for python -m trackr
        ├── cli.py                # Command-line interface logic (argparse)
        ├── models.py             # Transaction and RecurringPayment classes
        ├── io.py                 # Reading and parsing CSV data
        ├── analysis.py           # Recurring payment detection & balance math
        ├── recommend.py          # Advice and rule generation
        ├── visualize.py          # Matplotlib chart generator
        └── htmlreport.py         # HTML page generator