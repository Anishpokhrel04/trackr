"""CSV loading and validation for transaction history."""

import csv
from datetime import datetime
from pathlib import Path
from typing import List

from trackr.models import Transaction


def load_transactions(file_path: str | Path) -> List[Transaction]:
    """Load and parse transactions from a CSV file.

    Expected CSV columns: date, description, amount
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Transaction file not found: {file_path}")

    transactions: List[Transaction] = []
    
    # Supported date formats
    date_formats = ["%Y-%m-%d", "%d.%m.%Y", "%m/%d/%Y"]

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_date = row["date"].strip()
            description = row["description"].strip()
            amount = float(row["amount"].strip())

            parsed_date = None
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(raw_date, fmt)
                    break
                except ValueError:
                    continue

            if parsed_date is None:
                raise ValueError(f"Unsupported date format: '{raw_date}' in file {file_path}")

            transactions.append(Transaction(date=parsed_date, description=description, amount=amount))

    # Return transactions sorted chronologically
    return sorted(transactions, key=lambda t: t.date)