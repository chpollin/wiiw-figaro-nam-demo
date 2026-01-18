# Exploration Report: Energy Crisis and COVID Recovery in Southern Europe

## Research Question

Did the 2022 energy crisis slow COVID recovery in Southern Europe?

## 1. Data Availability

### 1.1 Available Countries in Existing Analyses

| Country | Code | Group | In CSV/JSON | Complete 2019-2023 |
|---------|------|-------|-------------|-------------------|
| Spain | ES | Southern Europe | Yes | Yes |
| Italy | IT | Southern Europe | Yes | Yes |
| Greece | GR | Southern Europe | Yes | Yes |
| Portugal | PT | Southern Europe | **No** | Parquet available |
| Germany | DE | Comparison | Yes | Yes |
| Austria | AT | Comparison | Yes | Yes |
| Netherlands | NL | Comparison | Yes | Yes |

**Finding:** Portugal (PT) is missing from existing CSV/JSON files but is available in the Parquet dataset for all years 2010-2023.

### 1.2 Available Metrics

| Metric | Code | Description | Status |
|--------|------|-------------|--------|
| Household consumption | P3_S14 (via hh_consumption) | Primary indicator | Complete |
| Government consumption | P3_S13 (via gov_consumption) | Secondary | Complete |
| Investment | P51G (via investment) | Secondary | Complete |
| Imports | P7 (via imports) | Context indicator | Complete |

## 2. Time Series Extraction (Household Consumption, billion EUR)

### 2.1 Southern Europe Group (ES, IT, GR)

| Year | ES | IT | GR |
|------|---:|---:|---:|
| 2019 | 764,822 | 1,112,246 | 143,898 |
| 2020 | 634,717 | 975,340 | 120,799 |
| 2021 | 704,796 | 1,049,814 | 134,201 |
| 2022 | 817,165 | 1,201,167 | 160,040 |
| 2023 | 886,305 | 1,270,637 | 172,313 |

### 2.2 Comparison Group (DE, AT, NL)

| Year | DE | AT | NL |
|------|---:|---:|---:|
| 2019 | 1,840,602 | 213,411 | 377,190 |
| 2020 | 1,710,174 | 191,774 | 353,193 |
| 2021 | 1,801,857 | 200,994 | 384,134 |
| 2022 | 2,045,224 | 234,795 | 445,724 |
| 2023 | 2,177,320 | 255,017 | 482,497 |

## 3. Pattern Identification

### 3.1 COVID Drop 2020 (YoY Change vs. 2019)

| Country | Group | COVID Drop (%) | Ranking |
|---------|-------|---------------:|---------|
| ES | Southern Europe | -17.0% | 1 (deepest) |
| GR | Southern Europe | -16.1% | 2 |
| IT | Southern Europe | -12.3% | 3 |
| AT | Comparison | -10.1% | 4 |
| FR | (not target group) | -7.6% | 5 |
| DE | Comparison | -7.1% | 6 |
| NL | Comparison | -6.4% | 7 (mildest) |
| PL | (not target group) | -4.7% | 8 |

**Finding:** Southern Europe suffered significantly stronger COVID drops (-12% to -17%) than the comparison group (-6% to -10%).

### 3.2 Recovery Dynamics 2020-2021 (Calculated from Time Series)

| Country | Group | 2020 | 2021 | Recovery (%) | Level vs. 2019 (%) |
|---------|-------|-----:|-----:|-------------:|-------------------:|
| ES | Southern Europe | 634,717 | 704,796 | +11.0% | -7.9% |
| IT | Southern Europe | 975,340 | 1,049,814 | +7.6% | -5.6% |
| GR | Southern Europe | 120,799 | 134,201 | +11.1% | -6.7% |
| DE | Comparison | 1,710,174 | 1,801,857 | +5.4% | -2.1% |
| AT | Comparison | 191,774 | 200,994 | +4.8% | -5.8% |
| NL | Comparison | 353,193 | 384,134 | +8.8% | +1.8% |

**Finding:** Southern Europe had stronger recovery dynamics in 2021 (+7.6% to +11.1%) but had not yet reached the 2019 level.

### 3.3 Energy Crisis Effect 2022 (Nominal YoY Change 2021-2022)

| Country | Group | HH Consumption 2022 (%) | Note |
|---------|-------|------------------------:|------|
| GR | Southern Europe | +19.3% | Highest nominal increase |
| PL | (not target group) | +17.2% | |
| AT | Comparison | +16.8% | |
| NL | Comparison | +16.0% | |
| ES | Southern Europe | +15.9% | |
| IT | Southern Europe | +14.4% | |
| DE | Comparison | +13.5% | |
| FR | (not target group) | +9.6% | Lowest increase |

**IMPORTANT LIMITATION:** These figures are nominal. The high increases in 2022 largely reflect inflation (energy and food prices), not real consumption growth.

### 3.4 Recovery Level Relative to Pre-Crisis (Index 2019=100)

| Country | Group | 2020 | 2021 | 2022 | 2023 |
|---------|-------|-----:|-----:|-----:|-----:|
| ES | Southern Europe | 83.0 | 92.1 | 106.8 | 115.9 |
| IT | Southern Europe | 87.7 | 94.4 | 108.0 | 114.2 |
| GR | Southern Europe | 83.9 | 93.3 | 111.2 | 119.7 |
| DE | Comparison | 92.9 | 97.9 | 111.1 | 118.3 |
| AT | Comparison | 89.9 | 94.2 | 110.0 | 119.5 |
| NL | Comparison | 93.6 | 101.8 | 118.2 | 127.9 |

**Finding:** Nominally, all countries exceeded the pre-crisis level by 2022. However, this masks real purchasing power losses.

## 4. Trend Deviation Analysis (Deviation from Pre-Crisis CAGR 2010-2018)

| Country | CAGR 2010-2018 (%) | Trend Deviation 2020 (%) |
|---------|-------------------:|-------------------------:|
| ES | 2.08 | -18.1 |
| IT | 1.45 | -13.8 |
| GR | -1.02 | -11.2 |
| AT | 3.16 | -12.3 |
| DE | 2.86 | -9.7 |
| NL | 3.35 | -9.3 |

**Finding:** Spain shows the largest deviation from long-term trend (-18.1%), followed by Italy (-13.8%). Greece already had a negative pre-crisis trend.

## 5. Key Findings

### 5.1 Clear Patterns (FACT)

1. **COVID Asymmetry:** Southern Europe suffered stronger consumption drops in 2020 (-12% to -17%) than the comparison group (-6% to -10%)

2. **Recovery Dynamics 2021:** Southern Europe recovered faster in 2021 (+7-11%) than the comparison group (+5-9%) but remained below the 2019 level

3. **Nominal Inflation 2022:** All countries show strong nominal consumption increases in 2022 (+10-19%), interpretable as inflation effect

### 5.2 Interpretation Required (INFERENCE)

1. **Real vs. Nominal Development:** Without external deflator data (HICP), it cannot be determined whether real consumption grew or shrank in 2022

2. **Energy Intensity:** Southern Europe could be more affected by energy price increases (higher cooling costs in summer, lower energy efficiency)

3. **Tourism Effect:** GR, ES, IT have high tourism dependency - 2021/2022 recovery could be amplified by tourism rebound

## 6. Data Gaps

| Gap | Impact | Solution |
|-----|--------|----------|
| Portugal (PT) missing | Incomplete Southern Europe group | Parquet query required |
| Only nominal values | Inflation effect not adjusted | External HICP data needed |
| Sectoral breakdown missing | No identification of energy price effects | Further Parquet analysis |

## 7. Recommendation

Existing data is sufficient for initial hypothesis formulation. For complete analysis, recommended:

1. **Extract PT data** from Parquet (low effort)
2. **Include HICP deflators** for real interpretation (external data requirement)
3. **Sectoral analysis** for CPA_D35 (energy) consumption share

---

Created: 2026-01-16
Data basis: outputs/tables/all_countries_time_series.csv, docs/data/time_series.json
