"""CSV parsing module with support for multiple bank date formats."""

import csv
from datetime import datetime
from pathlib import Path
from typing import List

from trackr.models import Transaction

DATE_FORMATS = ["%Y-%m-%d", "%d.%m.%Y", "%m/%d/%Y"]


def parse_date(date_str: str) -> datetime:
    """Parse string date using common bank formats."""
    cleaned = date_str.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(cleaned, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unsupported date format: {date_str}")


def load_transactions(file_path: str | Path) -> List[Transaction]:
    """Read CSV file and convert rows into a list of Transaction objects."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"CSV file not found: {path}")

    transactions: List[Transaction] = []
    with open(path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions.append(
                Transaction(
                    date=parse_date(row["date"]),
                    description=row["description"].strip(),
                    amount=float(row["amount"]),
                )
            )

    return sorted(transactions, key=lambda t: t.date)