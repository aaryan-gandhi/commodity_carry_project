from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/processed")

PANEL_1_PATH = DATA_DIR / "contract_panel_1_clean.csv"
PANEL_2_PATH = DATA_DIR / "contract_panel_2_clean.csv"

OUTPUT_PATH = DATA_DIR / "daily_roll_yield.csv"
QC_OUTPUT_PATH = DATA_DIR / "daily_roll_yield_summary.csv"

# Version 1 assumption:
# monthly-cycle energy and metals = 30 days between Contract 1 and Contract 2
# wider-cycle agriculture contracts = 60 days between Contract 1 and Contract 2
DAYS_BETWEEN_CONTRACTS = {
    "CO": 30,  # Brent crude
    "CL": 30,  # WTI crude
    "HO": 30,  # Heating oil
    "NG": 30,  # Natural gas
    "GC": 30,  # Gold
    "SI": 30,  # Silver
    "HG": 30,  # Copper
    "C": 60,   # Corn
    "W": 60,   # Wheat
    "S": 60,   # Soybeans
    "SB": 60,  # Sugar
    "KC": 60,  # Coffee
}

COMMODITIES = [
    "CO",
    "KC",
    "HG",
    "C",
    "CL",
    "GC",
    "HO",
    "NG",
    "SI",
    "S",
    "SB",
    "W",
]


def load_panel(file_path):
    """Load one cleaned panel and use Date as its index."""
    df = pd.read_csv(file_path, parse_dates=["Date"])
    df = df.sort_values("Date").set_index("Date")
    return df


def calculate_roll_yield(panel_1, panel_2):
    """
    Calculate annualized roll yield for each commodity.

    Formula:
    (F1 / F2 - 1) * (365 / days_between_contracts)
    """
    roll_yield = pd.DataFrame(index=panel_1.index)

    for ticker in COMMODITIES:
        front_column = f"{ticker}1"
        next_column = f"{ticker}2"

        days = DAYS_BETWEEN_CONTRACTS[ticker]

        roll_yield[ticker] = (
            (panel_1[front_column] / panel_2[next_column] - 1)
            * (365 / days)
        )

    return roll_yield


def create_summary(roll_yield):
    """Create basic quality-control statistics for every roll-yield series."""
    summary = pd.DataFrame({
        "observations": roll_yield.count(),
        "missing_values": roll_yield.isna().sum(),
        "mean_annualized_roll_yield": roll_yield.mean(),
        "median_annualized_roll_yield": roll_yield.median(),
        "min_annualized_roll_yield": roll_yield.min(),
        "max_annualized_roll_yield": roll_yield.max(),
    })

    return summary


if __name__ == "__main__":
    panel_1 = load_panel(PANEL_1_PATH)
    panel_2 = load_panel(PANEL_2_PATH)

    roll_yield = calculate_roll_yield(panel_1, panel_2)

    roll_yield.reset_index().to_csv(OUTPUT_PATH, index=False)

    summary = create_summary(roll_yield)
    summary.to_csv(QC_OUTPUT_PATH)

    print("\n--- Daily Roll Yield Summary ---")
    print(summary.round(4))

    print(f"\nSaved daily roll-yield panel: {OUTPUT_PATH}")
    print(f"Saved quality-control summary: {QC_OUTPUT_PATH}")