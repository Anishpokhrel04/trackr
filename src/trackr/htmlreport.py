"""Self-contained HTML dashboard generator for TrackR analysis reports."""

from pathlib import Path
from typing import List

from trackr.models import RecurringPayment, Transaction


def generate_html_report(
    transactions: List[Transaction],
    recurring: List[RecurringPayment],
    recommendations: List[str],
    plot_rel_path: str,
    output_path: str | Path,
) -> Path:
    """Generate a self-contained HTML dashboard report."""
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    total_income = sum(t.amount for t in transactions if t.is_income)
    total_expenses = abs(sum(t.amount for t in transactions if t.is_expense))
    net_savings = total_income - total_expenses

    recurring_rows = "".join(
        f"<tr><td>{r.description}</td><td>${abs(r.average_amount):.2f}</td><td>{r.occurrence_count}</td><td>{r.interval_days} days</td></tr>"
        for r in recurring
    )

    recommendation_items = "".join(f"<li>{rec}</li>" for rec in recommendations)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>TrackR Financial Dashboard</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f4f6f9; color: #333; margin: 0; padding: 20px; }}
        .container {{ max-width: 900px; margin: 0 auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        h1 {{ color: #2b5c8f; margin-top: 0; }}
        .grid {{ display: flex; gap: 15px; margin-bottom: 25px; }}
        .card {{ flex: 1; background: #f8fafc; padding: 15px; border-radius: 6px; border: 1px solid #e2e8f0; text-align: center; }}
        .card h3 {{ margin: 0 0 8px 0; font-size: 14px; color: #64748b; }}
        .card p {{ margin: 0; font-size: 22px; font-weight: bold; color: #1e293b; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ padding: 10px; border-bottom: 1px solid #e2e8f0; text-align: left; }}
        th {{ background: #f1f5f9; }}
        img {{ max-width: 100%; border-radius: 6px; margin: 20px 0; }}
        ul {{ background: #eff6ff; padding: 15px 30px; border-radius: 6px; border-left: 4px solid #3b82f6; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>TrackR Financial Analysis Dashboard</h1>
        
        <div class="grid">
            <div class="card"><h3>Total Income</h3><p>${total_income:,.2f}</p></div>
            <div class="card"><h3>Total Expenses</h3><p>${total_expenses:,.2f}</p></div>
            <div class="card"><h3>Net Savings</h3><p>${net_savings:,.2f}</p></div>
        </div>

        <h2>Balance History & Projection</h2>
        <img src="{plot_rel_path}" alt="Balance Plot">

        <h2>Detected Recurring Payments</h2>
        <table>
            <thead>
                <tr><th>Description</th><th>Avg Amount</th><th>Occurrences</th><th>Avg Interval</th></tr>
            </thead>
            <tbody>
                {recurring_rows or "<tr><td colspan='4'>No recurring payments detected.</td></tr>"}
            </tbody>
        </table>

        <h2>Actionable Recommendations</h2>
        <ul>
            {recommendation_items or "<li>No specific recommendations. Good financial status!</li>"}
        </ul>
    </div>
</body>
</html>
"""

    out_file.write_text(html_content, encoding="utf-8")
    return out_file