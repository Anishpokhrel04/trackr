from datetime import datetime
from trackr.models import Transaction
from trackr.analysis import detect_recurring, predict_balance


def test_transaction_model():
    t = Transaction(date=datetime(2026, 3, 1), description="Test Rent", amount=-950.0)
    assert t.is_expense is True
    assert t.is_income is False


def test_detect_recurring():
    txs = [
        Transaction(datetime(2026, 3, 1), "Netflix", -17.99),
        Transaction(datetime(2026, 4, 1), "Netflix", -17.99),
        Transaction(datetime(2026, 5, 1), "Netflix", -17.99),
    ]
    recurring = detect_recurring(txs, min_occurrences=3)
    assert len(recurring) == 1
    assert recurring[0].description == "Netflix"


def test_predict_balance():
    txs = [
        Transaction(datetime(2026, 3, 1), "Salary", 1000.0),
        Transaction(datetime(2026, 3, 2), "Expenses", -500.0),
    ]
    dates, balances = predict_balance(txs, starting_balance=0.0, days=10)
    assert len(dates) > 0
    assert len(balances) == len(dates)