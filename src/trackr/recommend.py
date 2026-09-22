"""Rule-based recommendation engine for financial analysis."""

from typing import List

from trackr.models import RecurringPayment, Transaction


def generate_recommendations(
    transactions: List[Transaction], recurring: List[RecurringPayment]
) -> List[str]:
    """Generate textual recommendations based on transactions and recurring expenses."""
    recommendations: List[str] = []

    total_income = sum(t.amount for t in transactions if t.is_income)
    total_expenses = abs(sum(t.amount for t in transactions if t.is_expense))

    if total_income == 0:
        recommendations.append("Warning: No income transactions detected in the dataset.")
        return recommendations

    # Check recurring expenses against income
    recurring_expenses = abs(
        sum(r.average_amount for r in recurring if r.is_subscription_or_expense)
    )

    recurring_ratio = (recurring_expenses / total_income) * 100
    if recurring_ratio > 30:
        recommendations.append(
            f"High Fixed Expenses: Recurring expenses eat up {recurring_ratio:.1f}% of total income. Consider canceling unused subscriptions."
        )

    # Check overall savings rate
    net_savings = total_income - total_expenses
    savings_rate = (net_savings / total_income) * 100

    if savings_rate < 0:
        recommendations.append(
            "Negative Cash Flow: Overall expenses exceed total income over this period."
        )
    elif savings_rate < 15:
        recommendations.append(
            f"Low Savings Rate: You are saving {savings_rate:.1f}% of income. Target at least 20% for emergency reserves."
        )
    else:
        recommendations.append(
            f"Good Savings Rate: You saved {savings_rate:.1f}% of income during this period."
        )

    return recommendations