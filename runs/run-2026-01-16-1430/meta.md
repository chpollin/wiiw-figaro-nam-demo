# Run Metadata

Run-ID: run-2026-01-16-1430
Status: completed
Start: 2026-01-16 14:30
End: 2026-01-16 15:10
Commit: 345968b

## Research Question

Did the 2022 energy crisis slow COVID recovery in Southern Europe?

Specification:
- Countries: ES, IT, GR, PT (Southern Europe) vs. DE, AT, NL (Comparison group)
- Period: 2019 (Pre-COVID), 2020 (COVID), 2021 (Recovery), 2022-2023 (Energy crisis)
- Metric: Household consumption (P3_S14) as indicator for economic recovery
- Question: Do Southern European countries show a slowdown or reversal of recovery in 2022?

## Hypotheses

H_int (Integrated from H1 + H4 + H5):
> Southern European countries show stronger nominal but weaker real recovery in 2022 than Northern Europe, with the difference partially cushioned by higher government consumption expansion. The apparently stronger nominal rebound is primarily a base effect of the deeper COVID drop in 2020.

## Summary

**Result: Hypothesis partially confirmed (1/3 components)**

1. **Base effect (confirmed):** Correlation r = -0.52 between COVID drop and recovery rate. Southern Europe's deeper drop (-14.4%) explains the higher nominal recovery rates.

2. **Nominal superiority of Southern Europe (refuted):** Contrary to expectations, Northern Europe shows a higher nominal index (113.1 vs. 110.0). In real terms, both regions converge to ~99.5% of pre-crisis level.

3. **Fiscal cushioning (opposite):** Northern Europe, especially Germany (+21.2%), showed stronger government consumption expansion than Southern Europe (+14.3%).

**Key finding:** The 2022 energy crisis distorted recovery nominally in both regions, but in real terms all countries converge to similar levels. The difference lies not in recovery dynamics but in the different fiscal responses.

## Outputs

| Type | Files |
|------|-------|
| Scripts | scripts/11_extract_portugal.py, scripts/12_hypothesis_h_int.py |
| Tables | outputs/tables/PT_time_series.csv, recovery_comparison.csv, basis_effect_analysis.csv, fiscal_response.csv |
| Figures | outputs/figures/basis_effect_scatter.png, recovery_nominal_vs_real.png, fiscal_cushion.png |
| Paper | runs/run-2026-01-16-1430/paper/paper.md |
| Validation | agents/implementation/validation.md |
