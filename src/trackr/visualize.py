"""Visualization module for saving balance trend plots to PNG files."""

from datetime import datetime
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt


def plot_balance_trend(
    dates: List[datetime], balances: List[float], output_path: str | Path
) -> Path:
    """Generate a balance plot and save it to a PNG file."""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dates, balances, color="#2b5c8f", linewidth=2, label="Account Balance ($)")

    ax.set_title("Historical and Projected Account Balance", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date", fontsize=10)
    ax.set_ylabel("Balance ($)", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(loc="upper left")

    fig.autofmt_xdate()
    plt.tight_layout()

    plt.savefig(output_file, dpi=300)
    plt.close(fig)

    return output_file