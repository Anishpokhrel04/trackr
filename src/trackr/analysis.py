"""Financial analysis module: recurring transaction detection and balance trend projection."""

import re
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

from trackr.models import RecurringPayment, Transaction


def normalize_description(desc: str) -> str:
    """Normalize transaction description by removing numbers and extra spaces."""
    return re.sub(r"\s+", " ", re.sub(r"\d+", "", desc.lower())).strip()


def detect_recurring(
    transactions: List[Transaction], min_occurrences: int = 3
) -> List[RecurringPayment]:
    """Identify repeating expenses and income based on frequency and amounts."""
    groups: Dict[str, List[Transaction]] = defaultdict(list)
    for t in transactions:
        groups[normalize_description(t.description)].append(t)

    recurring: List[RecurringPayment] = []
    for norm_key, item_list in groups.items():
        if len(item_list) < min_occurrences:
            continue

        sorted_items = sorted(item_list, key=lambda x: x.date)
        intervals = [
            (sorted_items[i + 1].date - sorted_items[i].date).days
            for i in range(len(sorted_items) - 1)
        ]

        avg_interval = sum(intervals) / len(intervals) if intervals else 0.0
        avg_amount = sum(t.amount for t in sorted_items) / len(sorted_items)

        recurring.append(
            RecurringPayment(
                description=sorted_items[0].description,
                average_amount=round(avg_amount, 2),
                occurrence_count=len(sorted_items),
                interval_days=round(avg_interval, 1),
            )
        )

    return recurring


def predict_balance(
    transactions: List[Transaction], starting_balance: float = 0.0, days: int = 30
) -> Tuple[List[datetime], List[float]]:
    """Compute cumulative daily account balance and project linear trend forward."""
    if not transactions:
        return [], []

    sorted_txs = sorted(transactions, key=lambda t: t.date)
    start_date, end_date = sorted_txs[0].date, sorted_txs[-1].date

    daily_changes: Dict[datetime, float] = defaultdict(float)
    for t in sorted_txs:
        daily_changes[datetime(t.date.year, t.date.month, t.date.day)] += t.amount

    dates: List[datetime] = []
    balances: List[float] = []
    current_balance, current_day = starting_balance, start_date

    while current_day <= end_date:
        current_balance += daily_changes.get(current_day, 0.0)
        dates.append(current_day)
        balances.append(round(current_balance, 2))
        current_day += timedelta(days=1)

    # Calculate average daily rate & project forward
    total_days = max((end_date - start_date).days, 1)
    daily_rate = (balances[-1] - starting_balance) / total_days
    last_balance = balances[-1]

    for d in range(1, days + 1):
        dates.append(end_date + timedelta(days=d))
        balances.append(round(last_balance + (daily_rate * d), 2))

    return dates, balances