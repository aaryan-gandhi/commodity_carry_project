from pathlib import Path
import pandas as pd

INPUT_DIR = Path("data/processed")
OUTPUT_DIR = Path("data/processed")

PANEL_FILES = [
    "contract_panel_1.csv",
    "contract_panel_2.csv",
    "contract_panel_3.csv",
]


def long_gap_mask(series, max_fillable_gap=1):
    """
    Return True for missing observations that belong to a gap longer
    than max_fillable_gap. Those observations must remain missing.
    """
    missing = series.isna()

    group_id = missing.ne(missing.shift()).cumsum()

    gap_length = missing.groupby(group_id).transform("sum")

    return missing & (gap_length > max_fillable_gap)


def clean_panel(file_name):
    input_path = INPUT_DIR / file_name

    panel = pd.read_csv(input_path, parse_dates=["Date"])

    panel = panel.sort_values("Date").set_index("Date")

    missing_before = panel.isna().sum()

    cleaned = panel.copy()

    for column in cleaned.columns:
        keep_missing = long_gap_mask(
            cleaned[column],
            max_fillable_gap=1
        )

        fillable_gap = cleaned[column].isna() & ~keep_missing

        forward_filled = cleaned[column].ffill()
        cleaned.loc[fillable_gap, column] = forward_filled[fillable_gap]

    missing_after = cleaned.isna().sum()

    output_name = file_name.replace(".csv", "_clean.csv")
    output_path = OUTPUT_DIR / output_name

    cleaned.reset_index().to_csv(output_path, index=False)

    qc = pd.DataFrame({
        "missing_before": missing_before,
        "missing_after": missing_after,
        "values_filled": missing_before - missing_after,
    })

    qc_name = file_name.replace(".csv", "_missing_data_qc.csv")
    qc_path = OUTPUT_DIR / qc_name
    qc.to_csv(qc_path)

    print(f"\n--- {file_name} ---")
    print(qc)
    print(f"Saved cleaned panel: {output_path}")
    print(f"Saved QC table:      {qc_path}")


if __name__ == "__main__":
    for panel_file in PANEL_FILES:
        clean_panel(panel_file)
