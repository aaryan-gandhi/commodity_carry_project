# Commodity Futures Carry Strategy

FINMA Markets Capstone · Aaryan Gandhi, Serena Chui, Cathy Zou · Mentor: Richard Howes

**One line:** each month, rank 12 commodity futures by annualised roll yield, go long the 3 most backwardated and short the 3 most in contango, size positions by inverse volatility, and target ~10% portfolio volatility.

This is a **harvesting strategy, not a predictive one**. We are not forecasting commodity prices. We are testing whether a known risk premium exists in our sample, and whether the futures curve tells us where it is largest.

---

## 1. Thesis

### The mechanism
A futures price is partly a **forecast** of the future spot price and partly a **risk premium**: a discount that hedgers accept in order to offload price risk.

- **Hedging pressure (Keynes, "normal backwardation").** Producers such as miners, farmers and oil companies sell futures to lock in prices. Speculators who take the other side demand a discount, so futures trade below the expected future spot. The speculator is effectively selling insurance and earns the gap.
- **Theory of storage (Kaldor, Working, Brennan).** Backwardation appears when inventories are tight. Thin inventories mean supply shocks move prices sharply, so the long position carries more risk and should earn more. Contango signals plentiful inventory and little premium.

### Why the curve is our signal
We cannot observe the premium directly, but we can observe the curve slope:

> curve slope = expected spot change + risk premium

Steep backwardation is a noisy but informative proxy for a large premium. Ranking commodities by carry therefore ranks them by *where we are paid most for providing insurance*.

### What carry is not
Roll yield is **not** free money. If futures were unbiased forecasts, backwardation would only mean spot is expected to fall, and that fall would cancel the roll gain. The strategy earns only the premium component. Testing that is the point of H2.

### Why long-short
Going long high carry and short low carry nets out the common "commodities went up or down" move. The book isolates the *difference* in premia across commodities rather than taking a directional bet on the asset class.

### Expected failure mode
A risk premium is compensation for bearing risk, so it **should** lose money in some periods. We expect losses to cluster in high-volatility stress episodes, when shocks flip curves (for example 2008 and early 2020). A backtest with no bad stretches would be a warning sign, not a success.

---

## 2. Hypotheses

These were set **before** running the backtest. Each result in the report is presented as confirming or rejecting one of them.

| # | Hypothesis | Prediction from the thesis | Test | Rejected if |
|---|---|---|---|---|
| H1 | The carry portfolio earns a positive return after costs | Longs collect a premium; shorts avoid paying one | Annualised return, Sharpe and t-stat of monthly returns, net of costs | Mean net return is not significantly above zero |
| H2 | Returns come mainly from roll, not spot | The premium is earned through the curve, not by predicting price | Decompose each commodity's and the portfolio's monthly return into roll yield and spot change | Roll gains are cancelled by offsetting spot moves on average |
| H3 | Steeper carry spreads predict higher returns | Steeper backwardation means scarcer inventory and a larger premium | Bucket months by the top-3 minus bottom-3 carry gap; compare next-month returns | No monotonic relationship between spread and subsequent return |
| H4 | Losses cluster in high-volatility regimes | The premium compensates for crash risk | Split months by a pre-defined volatility regime; compare return, Sharpe and drawdown | Performance is no worse, or better, in high-vol regimes |

**Volatility regime definition (H4), fixed in advance:** a month is "high-vol" if the cross-sectional average of the 12 commodities' 60-day realised volatility is above its full-sample median. This classification is used for ex-post analysis only and never feeds the trading signal.

---

## 3. Strategy specification (frozen)

Frozen on: **YYYY-MM-DD** (fill in on commit). Any change after this date is recorded in the decisions log with a reason.

| Component | Setting | Reason |
|---|---|---|
| Universe | 12 commodities, 4 sectors (see §4) | Liquid, diversified across sectors, histories back to 2005 |
| Sample | 2005 to latest available | Covers 2008, 2014–16 oil collapse, April 2020 negative WTI, 2022 energy spike |
| Signal | Annualised roll yield: `(F1/F2 − 1) × 365/Δdays` | Direct measure of curve slope; annualising makes contracts with different spacing comparable |
| Δdays | Actual days between expiries from `LAST_TRADEABLE_DT` (flat 30/60 days as fallback only) | Grains and softs list 4–5 contracts a year, not 12; a flat assumption mis-annualises them |
| Selection | Long top 3, short bottom 3 of 12 | Top and bottom quartiles; enough names to diversify, few enough to keep the signal sharp |
| Signal timing | Ranked on month-end close | Curves change slowly; monthly matches the roll cycle and limits costs |
| Within-leg weights | Inverse 60-day realised volatility, renormalised per leg | Stops natural gas from dominating risk |
| Book balance | Gross long notional = gross short notional | Isolates carry from overall commodity direction |
| Portfolio vol target | 10% annualised, scaled monthly using trailing realised vol | Standard, citable level; makes drawdowns interpretable |
| Leverage cap | 2× gross notional | Prevents the vol scalar blowing up exposure in calm periods |
| Contract held | gen2 | Avoids delivery-window illiquidity, such as the negative WTI front month in April 2020 |
| Look-ahead guard | Weights from month *t* close are applied to month *t+1* returns only | Prevents using information not available at decision time |
| Transaction costs | 3–5 bps for liquid names (WTI, Brent, gold); 8–10 bps for agriculturals; charged on turnover | Practitioner-style assumption; per-commodity values in `config/universe.csv` |

---

## 4. Universe

Exact tickers, `cost_bps` and `contract_months` live in `config/universe.csv`.

| Sector | Commodity | Bloomberg root | Note |
|---|---|---|---|
| Energy | WTI Crude | `CL` | Monthly cycle |
| Energy | Brent Crude | `CO` | Cross-check against WTI |
| Energy | Natural Gas | `NG` | Highest volatility; strongly seasonal |
| Energy | Heating Oil | `HO` | Seasonal (winter demand) |
| Precious metals | Gold | `GC` | Structurally low or negative carry; useful contrast |
| Precious metals | Silver | `SI` | |
| Base metals | Copper | `HG` | |
| Agriculture | Corn | `C ` | Root includes a space: `C 1 Comdty` |
| Agriculture | Wheat | `W ` | Same quirk |
| Agriculture | Soybeans | `S ` | Same quirk |
| Agriculture | Sugar #11 | `SB` | |
| Agriculture | Coffee "C" | `KC` | |

---

## 5. Validation plan

All variants are reported, not just the best one.

1. **Return decomposition (H2):** roll vs spot, per commodity and for the portfolio.
2. **Carry-spread buckets (H3):** next-month returns by terciles of the top-minus-bottom carry gap.
3. **Volatility regimes (H4):** return, Sharpe and max drawdown in high-vol vs low-vol months.
4. **Pre/post-2014 split:** the shale boom changed the shape of the energy curve; report both halves.
5. **Sub-period stability:** performance in each multi-year block across the sample.
6. **Sensitivity table:** top 2/bottom 2 and top 4/bottom 4; 20- and 90-day vol lookbacks; weekly rebalancing; equal weighting; no vol target.
7. **Named stress windows:** Oct–Dec 2008 and Mar–Apr 2020, including whether holding gen2 shielded the book from negative WTI.
8. **Benchmarks:** equal-weight long-only basket of the 12, and the Bloomberg Commodity Index.

Reported statistics: annualised return and volatility, Sharpe, Sortino, Calmar, max drawdown, hit rate, skew and kurtosis.

---

## 6. What would prove us wrong

- No positive net return after costs (H1 fails).
- Returns explained by spot moves rather than roll (H2 fails), meaning the curve was just forecasting.
- Edge confined to one decade or one commodity.
- Results that only hold for one specific parameter choice.

---

## 7. Known risks

- **Carry crashes and curve rehearsals:**

Commodity carry strategies are exposed to sudden losses when the futures curve changes sharply from backwardation to contango, or when an existing curve premium rapidly compresses. A steeply backwardated curve can reflect scarce inventories and strong immediate demand, but an unexpected supply recovery, demand shock or inventory rebuild can weaken near-dated prices relative to deferred contracts. Positions established on the assumption that the curve will remain favourable can then suffer mark-to-market losses, particularly when the strategy is concentrated in one commodity sector. Commodity futures risk premia vary with inventory conditions, meaning the economic drivers supporting carry can change over time. 

*Mitigation*

Stress-test the strategy against abrupt changes in curve slope and inventory conditions; cap individual commodity and sector exposures; and evaluate drawdowns during historical supply-demand shocks. Do not rely solely on the current curve shape as a predictor of future returns.

- **Seasonality:**

Natural gas, heating oil and agricultural futures exhibit pronounced seasonal supply-demand patterns. Natural gas demand often rises during winter heating periods, heating oil demand can increase during colder months, and grain prices respond to planting, harvest and weather cycles. These predictable patterns can influence the futures curve independently of the scarcity premium that a carry strategy intends to capture. Research on commodity forward curves highlights the importance of explicitly accounting for seasonal effects when modelling contracts such as heating oil and natural gas.

If the strategy interprets a seasonal curve pattern as a persistent carry signal, it may enter positions that perform poorly when the seasonal cycle reverses. For example, a curve shape associated with winter demand may weaken as heating demand declines and inventories recover.

*Mitigation*
Adjust signals for contract-specific seasonality, compare each contract's curve slope with its historical pattern for the same time of year, and test whether carry returns persist after seasonal adjustment. This is particularly important if the strategy compares raw curve slopes across different commodities.

- **Crowding and premium compression:**

Commodity carry is a well-established investment approach, so the strategy may face competition from systematic funds, commodity trading advisers and institutional investors exploiting similar futures-curve signals. If more participants trade the same positions, entry prices may become less attractive, reducing the premium available to later investors. Crowded positions can also unwind simultaneously following a common macroeconomic shock, amplifying price moves and transaction costs.

Research demonstrates that futures-curve information can help identify attractive roll yields and improve commodity investment strategies, but those results do not guarantee that the same premium will persist in a different sample or trading environment.

*Mitigation*
Assess net returns after realistic transaction costs, test the strategy across different historical periods and monitor whether profitability weakens out of sample. Evaluate turnover and position concentration, and avoid assuming that historical carry premiums will remain constant.

- **Structural contango Risk:**

A persistent change in commodity-market structure can undermine carry signals across an entire sector. In energy, for example, changes in shale production, storage capacity, transportation infrastructure or inventory management may alter the relationship between nearby and deferred futures prices. If these changes lead to a sustained increase in storage availability or reduce the frequency of physical shortages, the historical relationship between curve shape and subsequent returns may weaken.

This risk differs from a carry crash: a crash is an abrupt adverse move, whereas a structural change can gradually erode the strategy's expected return over many months or years. Evidence of structural breaks in commodity futures bases and cost-of-carry relationships supports the need to account for changing market regimes

*Mitigation*
Test performance across distinct market regimes, monitor rolling carry returns and curve characteristics, and compare historical relationships with current inventory and storage conditions. If the strategy's expected return deteriorates persistently, consider reducing exposure or revising the signal rather than assuming mean reversion will restore profitability.

- **Liquidity and Operational Risk:** thin liquidity in agricultural contracts; delivery and negative-price risk near expiry.

Commodity futures markets differ substantially in liquidity. Major energy and agricultural contracts may have deep markets in their most actively traded maturities, while less-traded delivery months can have wider bid–ask spreads, lower market depth and greater market impact. Consequently, a strategy that appears profitable using settlement prices may earn materially lower returns after execution costs, especially when positions must be rolled or exited during volatile markets.

Expiry also creates operational risks. Futures contracts may require physical delivery under their exchange rules, and traders who unintentionally hold deliverable contracts beyond the permitted close-out date can face significant operational and financial consequences. Furthermore, extreme dislocations can produce unusual or even negative futures prices, as illustrated by the April 2020 WTI crude oil episode. Such events can invalidate simplistic return, sizing and risk-management assumptions.

*Mitigation*
Restrict trading to sufficiently liquid contracts, incorporate bid–ask spreads and market impact into backtests, and implement explicit roll calendars and pre-expiry close-out rules. Confirm contract specifications, position limits, margin requirements and exchange price-limit rules. Test the strategy under extreme price moves and verify that the backtest handles negative futures prices correctly.

---

## 8. Open decisions

To confirm with the team and Richard. Record the outcome in the decisions log.

- [ ] **Seasonality handling.** Option A: keep raw front-spread carry and flag seasonality as a limitation. Option B: for seasonal names, use deseasonalised carry, i.e. current carry minus its trailing average for the same calendar month (feasible with gen1–gen3 data). Option C: use a 12-month spread (needs deeper contracts pulled). The chosen option is the primary spec; the others are reported as robustness checks.
- [ ] **Out-of-sample hold-out.** Whether to reserve 2020 onwards as an untouched test period. Parameters are already fixed a priori, so this is an extra safeguard rather than essential.

---

## 9. Repo structure

```
├── README.md
├── requirements.txt
├── .gitignore
├── config/
│   ├── universe.csv      # 12 commodities: tickers, held generic, cost_bps, contract_months
│   └── fixes.csv         # data-quality decisions (audit trail)
├── data/
│   ├── raw/              # Bloomberg exports — NOT tracked
│   └── processed/        # cleaned panels — tracked
├── src/
│   ├── make_synthetic.py # synthetic 12-commodity panel with injected faults
│   ├── audit.py          # data-quality checks → output/tables/audit_issues.csv
│   ├── load.py
│   ├── signal.py
│   ├── portfolio.py
│   └── backtest.py
├── notebooks/            # 01_data_audit.ipynb, ...
└── output/
    ├── figures/
    └── tables/
```

## 10. Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Until the Bloomberg pull is complete, run `python src/make_synthetic.py` to generate a panel with the same schema as the real data. Swapping to real data is a single filename change.

## 11. Conventions

- Every notebook starts with `os.chdir("..")` so paths resolve from the repo root.
- `data/raw/` is never committed; `data/processed/` is.
- Work on short-lived feature branches off `main`. No two people edit the same notebook at once.
- Data anomalies are logged by `src/audit.py`, never silently fixed. Each fix is recorded in `config/fixes.csv`.
- Every judgment call (Δdays method, cut-offs, cost assumptions, contract choice, seasonality) goes in the decisions log with date and reason.

## 12. References

- Keynes, J. M. (1930). *A Treatise on Money*: normal backwardation.
- Fama, E. & French, K. (1987). Commodity futures prices: some evidence on forecast power, premiums, and the theory of storage. *Journal of Business*.
- Erb, C. & Harvey, C. (2006). The strategic and tactical value of commodity futures. *Financial Analysts Journal*.
- Gorton, G. & Rouwenhorst, K. G. (2006). Facts and fantasies about commodity futures. *Financial Analysts Journal*.
- Gorton, G., Hayashi, F. & Rouwenhorst, K. G. (2013). The fundamentals of commodity futures returns. *Review of Finance*.
- Koijen, R., Moskowitz, T., Pedersen, L. & Vrugt, E. (2018). Carry. *Journal of Financial Economics*.
