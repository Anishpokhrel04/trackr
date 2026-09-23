"""Financial analysis logic: recurring payment detection and balance projection."""

import re
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

from trackr.models import RecurringPayment, Transaction


def normalize_description(desc: str) -> str:
    """Normalize transaction description by lowercase, removing digits and extra spaces."""
    cleaned = re.sub(r"\d+", "", desc.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


def detect_recurring(
    transactions: List[Transaction], min_occurrences: int = 3
) -> List[RecurringPayment]:
    """Identify recurring transactions based on description similarity and regular frequency."""
    groups: Dict[str, List[Transaction]] = defaultdict(list)
    for t in transactions:
        norm_key = normalize_description(t.description)
        groups[norm_key].append(t)

    recurring: List[RecurringPayment] = []

    for norm_key, item_list in groups.items():
        if len(item_list) < min_occurrences:
            continue

        # Sort chronologically
        sorted_items = sorted(item_list, key=lambda x: x.date)

        # Calculate interval differences between consecutive payments
        intervals = [
            (sorted_items[i + 1].date - sorted_items[i].date).days
            for i in range(len(sorted_items) - 1)
        ]
        
        avg_interval = sum(intervals) / len(intervals) if intervals else 0
        avg_amount = sum(t.amount for t in sorted_items) / len(sorted_items)

        # Display raw description of the first occurrence for readability
        display_name = sorted_items[0].description

        recurring.append(
            RecurringPayment(
                description=display_name,
                average_amount=round(avg_amount, 2),
                occurrence_count=len(sorted_items),
                interval_days=round(avg_interval, 1),
            )
        )

    return recurring


def predict_balance(
    transactions: List[Transaction], starting_balance: float = 0.0, days: int = 30
) -> Tuple[List[datetime], List[float]]:
    """Calculate historical cumulative balance and project linear trend into the future."""
    if not transactions:
        return [], []

    sorted_txs = sorted(transactions, key=lambda t: t.date)
    start_date = sorted_txs[0].date
    end_date = sorted_txs[-1].date

    # Build daily net change map
    daily_changes: Dict[datetime, float] = defaultdict(float)
    for t in sorted_txs:
        # Normalize date to midnight
        day = datetime(t.date.year, t.date.month, t.date.day)
        daily_changes[day] += t.amount

    dates: List[datetime] = []
    balances: List[float] = []

    current_balance = starting_balance
    current_day = start_date

    while current_day <= end_date:
        current_balance += daily_changes.get(current_day, 0.0)
        dates.append(current_day)
        balances.append(round(current_balance, 2))
        current_day += timedelta(days=1)

    # Historical average daily change
    total_days = (end_date - start_date).days or 1
    total_net = balances[-1] - starting_balance
    daily_rate = total_net / total_days

    # Project future days
    last_balance = balances[-1]
    for d in range(1, days + 1):
        future_date = end_date + timedelta(days=d)
        projected = last_balance + (daily_rate * d)
        dates.append(future_date)
        balances.append(round(projected, 2))

    return dates, balances