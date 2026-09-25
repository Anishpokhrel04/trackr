import argparse
from pathlib import Path

from trackr.analysis import detect_recurring, predict_balance
from trackr.htmlreport import generate_html_report
from trackr.io import load_transactions
from trackr.recommend import generate_recommendations
from trackr.visualize import plot_balance_trend


def main():
    parser = argparse.ArgumentParser(
        description="TrackR - Personal finance analysis tool"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a transaction CSV file")
    analyze_parser.add_argument("csv_file", type=str, help="Path to input CSV file")
    analyze_parser.add_argument(
        "--starting-balance", type=float, default=0.0, help="Initial account balance"
    )
    analyze_parser.add_argument(
        "--predict-days", type=int, default=30, help="Days to project into future"
    )
    analyze_parser.add_argument(
        "--output-dir", type=str, default="output", help="Directory to save output reports"
    )

    args = parser.parse_args()

    if args.command == "analyze":
        csv_path = Path(args.csv_file)
        # Ensure output directory exists before writing
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        print(f"[TrackR] Reading transactions from: {csv_path}")
        txs = load_transactions(csv_path)
        print(f"[TrackR] Successfully parsed {len(txs)} transaction records.")

        # Run recurring detection & predictions
        recurring = detect_recurring(txs)
        dates, balances = predict_balance(
            txs, starting_balance=args.starting_balance, days=args.predict_days
        )
        recs = generate_recommendations(txs, recurring)

        # Plot chart
        chart_path = out_dir / "balance_plot.png"
        plot_balance_trend(dates, balances, chart_path)
        print(f"Chart saved to {chart_path}")

        # Generate HTML report
        report_path = out_dir / "report.html"
        generate_html_report(txs, recurring, recs, "balance_plot.png", report_path)
        print(f"Report generated successfully: {report_path}")


if __name__ == "__main__":
    main()