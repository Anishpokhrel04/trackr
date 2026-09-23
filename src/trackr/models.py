"""Data models for financial transactions and recurring payments."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    """Represents a single financial transaction."""

    date: datetime
    description: str
    amount: float

    @property
    def is_expense(self) -> bool:
        """Return True if the transaction is an expense (negative amount)."""
        return self.amount < 0

    @property
    def is_income(self) -> bool:
        """Return True if the transaction is income (positive amount)."""
        return self.amount > 0


@dataclass
class RecurringPayment:
    """Represents a detected recurring payment (e.g., subscriptions, rent, salary)."""

    description: str
    average_amount: float
    occurrence_count: int
    interval_days: float

    @property
    def is_subscription_or_expense(self) -> bool:
        """Return True if the recurring item is an outgoing payment."""
        return self.average_amount < 0