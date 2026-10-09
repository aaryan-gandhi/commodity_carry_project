from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

FILES = {
    "CO": "Brent(CO).csv",
    "KC": "Coffee(KC).csv",
    "HG": "Copper.csv",
    "C": "Corn(C).csv",
    "CL": "Crudeoil.csv",
    "GC": "Gold.csv",
    "HO": "Heatingoil(HO).csv",
    "NG": "Naturalgas.csv",
    "SI": "Silver(SI).csv",
    "S": "Soybeans(S).csv",
    "SB": "Sugar(SB).csv",
    "W": "Wheat(W).csv",
}

COLUMN_NAMES = {
    "CO": ["CO1", "CO2", "CO3"],
    "KC": ["KC1", "KC2", "KC3"],
    "HG": ["HG1", "HG2", "HG3"],
    "C": ["C1", "C2", "C3"],
    "CL": ["CL1", "Cl2", "CL3"],
    "GC": ["GC1", "GC2", "GC3"],
    "HO": ["HO1", "HO2", "HO3"],
    "NG": ["NG1", "NG2", "NG3"],
    "SI": ["SI1", "SI2", "SI3"],
    "S": ["S1", "S2", "S3"],
    "SB": ["SB1", "SB2", "SB3"],
    "W": ["W1", "W2", "W3"],
}


def load_commodity_contract(ticker, contract_number):
    """
    Load one contract depth for one commodity.

    Example:
    load_commodity_contract("CL", 1)
    returns a DataFrame with Date and CL1.
    """
    file_path = RAW_DIR / FILES[ticker]
    contract_column = COLUMN_NAMES[ticker][contract_number - 1]

    df = pd.read_csv(file_path)

    df = df[["Date", contract_column]].copy()

    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

    df[contract_column] = pd.to_numeric(
        df[contract_column],
        errors="coerce"
    )

    df = df.dropna(subset=["Date"])

    df = (
        df.sort_values("Date")
        .drop_duplicates(subset="Date", keep="last")
        .set_index("Date")
    )

    if ticker == "CL" and contract_number == 2:
        df = df.rename(columns={"Cl2": "CL2"})

    return df


def build_contract_panel(contract_number):
    """
    Outer-join every commodity at one contract depth.

    Example:
    contract_number=1 creates columns:
    CO1, KC1, HG1, C1, CL1, GC1, HO1, NG1, SI1, S1, SB1, W1
    """
    series_list = []

    for ticker in FILES:
        contract_df = load_commodity_contract(ticker, contract_number)
        series_list.append(contract_df)

    panel = pd.concat(series_list, axis=1, join="outer")

    panel = panel.sort_index()

    return panel


def print_panel_check(panel, panel_name):
    print(f"\n--- {panel_name} ---")
    print(f"Date range: {panel.index.min().date()} to {panel.index.max().date()}")
    print(f"Rows: {len(panel):,}")
    print(f"Columns: {len(panel.columns)}")
    print("\nMissing values by column:")
    print(panel.isna().sum().sort_values())


if __name__ == "__main__":
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    panel_1 = build_contract_panel(contract_number=1)
    panel_2 = build_contract_panel(contract_number=2)
    panel_3 = build_contract_panel(contract_number=3)

    panel_1.to_csv(PROCESSED_DIR / "contract_panel_1.csv")
    panel_2.to_csv(PROCESSED_DIR / "contract_panel_2.csv")
    panel_3.to_csv(PROCESSED_DIR / "contract_panel_3.csv")

    print_panel_check(panel_1, "Contract 1 panel")
    print_panel_check(panel_2, "Contract 2 panel")
    print_panel_check(panel_3, "Contract 3 panel")

    print("\nSaved files:")
    print("data/processed/contract_panel_1.csv")
    print("data/processed/contract_panel_2.csv")
    print("data/processed/contract_panel_3.csv")
