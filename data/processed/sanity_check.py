"""
Sanity-check raw commodity price series before they go anywhere near a backtest.

For each contract series (e.g. CO1, CO2, CO3) this script:
  1. Plots the raw price over time.
  2. Flags flat stretches (>= FLAT_MIN_DAYS identical consecutive closes),
     which usually mean Bloomberg forward-filled a gap rather than the
     market actually going nowhere.
  3. Flags one-day jumps whose |return| exceeds JUMP_THRESHOLD, which can be
     a genuine move, a bad tick, or a unit/rebase error.
  4. Flags calendar gaps bigger than MAX_GAP_DAYS between consecutive rows,
     which is more than a normal weekend/holiday and suggests missing data.

Currently configured for Brent (CO). To do another commodity, copy the
config block below and swap CSV_PATH / TICKER / CONTRACT_COLS.
"""

import pandas as pd
import matplotlib.pyplot as plt

# ---- config: change these three lines to check a different commodity ----
CSV_PATH = 'data/raw/Brent(CO).csv'
TICKER = 'CO'
CONTRACT_COLS = ['CO1', 'CO2', 'CO3']

# ---- anomaly thresholds ----
FLAT_MIN_DAYS = 3      # 3+ identical consecutive closes gets flagged
JUMP_THRESHOLD = 0.10  # 10% one-day move gets flagged
MAX_GAP_DAYS = 5        # more than 5 calendar days between rows gets flagged

OUT_DIR = 'data/processed/sanity_plots'


def load_prices(csv_path, contract_cols):
    df = pd.read_csv(csv_path)
    df = df[['Date'] + contract_cols].dropna(how='all')
    df = df.dropna(subset=['Date'])
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    df = df.sort_values('Date').reset_index(drop=True)
    return df


def find_flat_stretches(dates, prices, min_days):
    flagged = []
    run_start = 0
    for i in range(1, len(prices) + 1):
        same_as_prev = i < len(prices) and prices.iloc[i] == prices.iloc[run_start]
        if not same_as_prev:
            run_len = i - run_start
            if run_len >= min_days:
                flagged.append((dates.iloc[run_start], dates.iloc[i - 1], run_len, prices.iloc[run_start]))
            run_start = i
    return flagged


def find_jumps(dates, prices, threshold):
    returns = prices.pct_change()
    mask = returns.abs() > threshold
    return list(zip(dates[mask], prices[mask], returns[mask]))


def find_gaps(dates, max_gap_days):
    diffs = dates.diff().dt.days
    flagged = []
    for i in diffs[diffs > max_gap_days].index:
        flagged.append((dates.iloc[i - 1], dates.iloc[i], diffs.iloc[i]))
    return flagged


def check_series(df, col):
    dates, prices = df['Date'], df[col]

    flats = find_flat_stretches(dates, prices, FLAT_MIN_DAYS)
    jumps = find_jumps(dates, prices, JUMP_THRESHOLD)
    gaps = find_gaps(dates, MAX_GAP_DAYS)

    print(f'\n=== {col} ===')
    print(f'{len(flats)} flat stretch(es) >= {FLAT_MIN_DAYS} days:')
    for start, end, length, price in flats:
        print(f'  {start.date()} to {end.date()} ({length} days) @ {price}')

    print(f'{len(jumps)} one-day jump(s) > {JUMP_THRESHOLD:.0%}:')
    for date, price, ret in jumps:
        print(f'  {date.date()}: {ret:+.1%} to {price}')

    print(f'{len(gaps)} calendar gap(s) > {MAX_GAP_DAYS} days:')
    for prev_date, date, gap in gaps:
        print(f'  {prev_date.date()} -> {date.date()} ({int(gap)} days)')

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(dates, prices, linewidth=0.8, label=col)
    for start, end, _, price in flats:
        ax.axvspan(start, end, color='orange', alpha=0.3)
    for date, price, _ in jumps:
        ax.scatter([date], [price], color='red', zorder=5)
    ax.set_title(f'{col} price ({flags_summary(flats, jumps, gaps)})')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    fig.tight_layout()

    import os
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = f'{OUT_DIR}/{col}_sanity.png'
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f'Saved plot to {out_path}')


def flags_summary(flats, jumps, gaps):
    return f'{len(flats)} flat, {len(jumps)} jumps, {len(gaps)} gaps'


if __name__ == '__main__':
    df = load_prices(CSV_PATH, CONTRACT_COLS)
    for col in CONTRACT_COLS:
        check_series(df, col)
