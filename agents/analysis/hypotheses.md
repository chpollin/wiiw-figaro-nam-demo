# Hypotheses: Energy Crisis and COVID Recovery in Southern Europe

## Research Question

Did the 2022 energy crisis slow COVID recovery in Southern Europe?

---

## Hypothesis 1: Differential Recovery Speed

**Priority: HIGH**

### Formulation

Southern European countries (ES, IT, GR, PT) showed slower real consumption recovery in 2021-2022 than the comparison group (DE, AT, NL), although their nominal growth rates were higher.

### Operationalization

| Step | Calculation | Data Source |
|------|-------------|-------------|
| 1 | Extract HH consumption nominal 2019, 2021, 2022 | all_countries_time_series.csv |
| 2 | Obtain HICP deflators (2019=100) from Eurostat | External (HICP prc_hicp_aind) |
| 3 | Real consumption = Nominal / (HICP/100) | Calculation |
| 4 | Real recovery index = Real_2022 / Real_2019 * 100 | Calculation |
| 5 | Group comparison Southern Europe vs. Comparison | t-test or mean comparison |

### Testable Prediction

- H0: Real recovery index Southern Europe >= Real recovery index Comparison
- H1: Real recovery index Southern Europe < Real recovery index Comparison

### Expected Result

The nominal increases in 2022 (+14-19% in Southern Europe) mask real purchasing power losses. After inflation adjustment, the comparison group should be more recovered.

### Effort

- Low (existing data + external deflators)
- Estimated time: 2-3 hours

---

## Hypothesis 2: Tourism Dependency as Driver

**Priority: MEDIUM**

### Formulation

Countries with high tourism dependency (GR, ES, PT) showed stronger recovery in 2021 but slowed recovery in 2022 compared to less tourism-dependent countries.

### Operationalization

| Step | Calculation | Data Source |
|------|-------------|-------------|
| 1 | Extract tourism sector consumption (CPA_I, CPA_H49-H53) | Parquet (Set_i filter) |
| 2 | Calculate tourism share of HH consumption | Aggregation |
| 3 | Compare tourism growth 2020-2021 vs. 2021-2022 | YoY calculation |
| 4 | Correlation tourism share 2019 vs. recovery dynamics | Regression |

### Testable Prediction

- H0: No relationship between tourism share and recovery pattern
- H1: Higher tourism dependency correlates with stronger recovery 2021 but slowdown 2022

### Expected Result

Tourism rebound 2021 (after lifting travel restrictions) explains parts of Southern Europe recovery. 2022 normalization.

### Effort

- Medium (Parquet query required)
- Estimated time: 4-5 hours

---

## Hypothesis 3: Energy Intensity of Consumption

**Priority: HIGH**

### Formulation

Households in Southern Europe had a higher share of energy-intensive expenditure in total consumption in 2022, leading to stronger price increase effects.

### Operationalization

| Step | Calculation | Data Source |
|------|-------------|-------------|
| 1 | Extract CPA_D35 (electricity/gas) HH consumption | Parquet (Set_i=CPA_D35, Set_j=S14) |
| 2 | Energy share = CPA_D35 / P3_S14 * 100 | Calculation |
| 3 | Change in energy share 2019-2022 by country | Time series |
| 4 | Relationship energy share increase vs. nominal consumption increase | Correlation |

### Testable Prediction

- H0: Energy share increase 2019-2022 is equal in Southern Europe and comparison group
- H1: Energy share increase 2019-2022 is higher in Southern Europe

### Expected Result

Due to higher energy price increases in more energy-dependent households, the nominal energy share rises more strongly, indicating lower purchasing power for other goods.

### Effort

- Low to medium (Parquet query)
- Estimated time: 3-4 hours

---

## Hypothesis 4: Fiscal Cushioning

**Priority: LOW**

### Formulation

Countries with stronger government consumption (P3_S13) expansion in 2022 showed better cushioning of the energy crisis for households.

### Operationalization

| Step | Calculation | Data Source |
|------|-------------|-------------|
| 1 | Gov consumption growth 2021-2022 by country | all_countries_time_series.csv |
| 2 | HH real consumption development (see H1) | Calculation |
| 3 | Correlation gov consumption growth vs. HH real consumption development | Regression |

### Testable Prediction

- H0: No relationship between fiscal expansion and HH consumption stability
- H1: Higher fiscal expansion stabilizes HH consumption

### Expected Result

Government energy price subsidies and transfers in some countries (DE, NL) have partially supported household purchasing power.

### Effort

- Low (existing data)
- Estimated time: 2 hours

---

## Hypothesis 5: Base Effect of COVID Depth

**Priority: MEDIUM**

### Formulation

Countries with deeper COVID drop in 2020 mechanically show higher percentage recovery rates in 2021-2022, which does not mean genuine recovery superiority.

### Operationalization

| Step | Calculation | Data Source |
|------|-------------|-------------|
| 1 | COVID drop (%) = (2020-2019)/2019 | all_countries_time_series.csv |
| 2 | Recovery rate (%) = (2022-2020)/2020 | Calculation |
| 3 | Correlation drop depth vs. recovery rate | Scatter plot |
| 4 | Level comparison (Index 2019=100 for 2022) | Calculation |

### Testable Prediction

- H0: Recovery rate is independent of drop depth
- H1: Stronger drop correlates with higher percentage recovery (base effect)

### Expected Result

ES and GR (deepest drop) show nominally strongest recovery, but lag in level comparison.

### Effort

- Very low (existing data)
- Estimated time: 1 hour

---

## Prioritized Order (Original)

| Priority | Hypothesis | Effort | Recommendation |
|----------|------------|--------|----------------|
| 1 | H1: Differential recovery speed | Low | **TEST FIRST** |
| 2 | H5: Base effect | Very low | Parallel to H1 |
| 3 | H3: Energy intensity | Medium | After H1/H5 |
| 4 | H2: Tourism dependency | Medium | Optional |
| 5 | H4: Fiscal cushioning | Low | Supplementary |

---

## SELECTED HYPOTHESIS: H_int (Integrated)

**Status: APPROVED by Expert in the Loop (2026-01-16)**

### Formulation

> Southern European countries (ES, IT, GR, PT) show stronger nominal but weaker real recovery in 2022 than Northern Europe (DE, AT, NL), with the difference partially cushioned by higher government consumption expansion in Southern Europe. The apparently stronger nominal rebound is primarily a base effect of the deeper COVID drop in 2020.

### Components

| Component | Origin | Function |
|-----------|--------|----------|
| Base effect | H5 | Methodological control |
| Nominal vs. real recovery | H1 | Core hypothesis |
| Fiscal cushioning | H4 | Explanatory mechanism |

### Causal Chain

```
H5 (Base effect)     --> Methodological control: High recovery rates = artifact?
        |
        v
H1 (Differential    --> Core hypothesis: Nominal strong, real weak?
    recovery)
        |
        v
H4 (Fiscal          --> Explanatory mechanism: Government consumption as buffer?
    cushioning)
```

### Operationalization

| Step | Metric | Data Source | Status |
|------|--------|-------------|--------|
| 1 | Extract PT data | Parquet | Pending |
| 2 | Base effect: Correlation drop 2020 vs. recovery 2021-22 | Existing CSV | Pending |
| 3 | Nominal index 2019=100, level 2022 | Existing CSV | Pending |
| 4 | Obtain HICP deflators | Eurostat external | Pending |
| 5 | Real index 2019=100, level 2022 | Calculation | Pending |
| 6 | Government consumption growth vs. HH consumption stabilization | Existing CSV | Pending |
| 7 | Create visualizations | matplotlib | Pending |

### Expected Outputs

| Output | Description |
|--------|-------------|
| `outputs/tables/recovery_comparison.csv` | Nominal and real recovery indices |
| `outputs/tables/basis_effect_analysis.csv` | Correlation drop vs. recovery |
| `outputs/tables/fiscal_response.csv` | Government consumption development |
| `outputs/figures/recovery_nominal_vs_real.png` | Bar chart comparison |
| `outputs/figures/basis_effect_scatter.png` | Scatter plot |
| `outputs/figures/fiscal_cushion.png` | Gov consumption vs. HH consumption |

### Testable Predictions

1. **Base effect:** Negative correlation between COVID drop 2020 and level index 2022
2. **Nominal illusion:** Southern Europe nominal >100%, real <100% (2019=100)
3. **Fiscal cushioning:** Countries with higher gov consumption growth show more stable HH consumption

---

## Data Requirements for Complete Analysis

### Internally Available

- HH consumption nominal 2019-2023 (6 of 7 countries)
- Government consumption 2019-2023
- Investment 2019-2023

### Parquet Extraction Required

- Portugal (PT) data
- Sectoral breakdown (CPA_D35, CPA_I)

### External Required

- HICP deflators (Eurostat prc_hicp_aind)
- Optional: Energy price indices

---

## Recommendation for Next Step

**Implement immediately:**

1. Calculate hypothesis H5 (base effect) with existing data
2. Prepare hypothesis H1: Obtain HICP data from Eurostat

**Short-term:**

3. Extract PT data from Parquet for complete Southern Europe group

---

Created: 2026-01-16
Basis: exploration-report.md, outputs/tables/*.csv
