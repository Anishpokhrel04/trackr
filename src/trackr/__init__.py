"""TrackR: Personal Finance & Transaction Analysis Tool."""

from trackr.analysis import detect_recurring, predict_balance
from trackr.io import load_transactions
from trackr.models import RecurringPayment, Transaction
from trackr.recommend import generate_recommendations

__version__ = "0.1.0"

__all__ = [
    "Transaction",
    "RecurringPayment",
    "load_transactions",
    "detect_recurring",
    "predict_balance",
    "generate_recommendations",
]