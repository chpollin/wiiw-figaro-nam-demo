# Data Documentation: FIGARO-NAM

## Overview

FIGARO-NAM (Full International and Global Accounts for Research in Input-Output Analysis – National Accounts Matrix) provides detailed national accounts data from Eurostat. The data captures economic flows between sectors, including production, income generation, distribution, and use.

## Format

**Type:** Apache Parquet (partitioned)

**Directory structure:**
```
data/
└── parquet/
    └── base=YYYY/
        └── ctr=XX/
            └── part-0.parquet
```

**Partitioning scheme (Hive-style):**
- `base` – Reference year (2010–2023)
- `ctr` – ISO 3166-1 alpha-2 country code

**Dataset statistics:**
- Total files: 700 parquet files
- Total size: 191 MB
- Average file size: ~273 KB
- Rows per file: ~120,000

## Coverage

**Temporal:** 2010–2023 (14 years)

**Geographical (50 countries/regions):**

| Category | Countries |
|----------|-----------|
| EU member states | AT, BE, BG, CY, CZ, DE, DK, EE, ES, FI, FR, GR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK |
| Other European | AL, CH, GB, ME, MK, NO, RS, RU, TR |
| Americas | AR, BR, CA, MX, US |
| Asia-Pacific | AU, CN, ID, IN, JP, KR |
| Other | SA, ZA |
| Aggregate | WRL_REST (Rest of World) |

## Variables

**Schema (6 columns):**

| Column | Type | Description |
|--------|------|-------------|
| `Set_i` | string | Row category: Products (CPA_*) or Industries (NACE) or Accounts (D*, B*, F*, P*, S*, N*) |
| `m` | string | Partner country code (50 values) |
| `Set_j` | string | Column category: Industries or Accounts |
| `value` | float64 | Flow value (monetary, billion EUR) |
| `base` | category | Reference year (partition key) |
| `ctr` | category | Country code (partition key) |

**Value statistics (sample: AT 2010):**
- Range: -9,750 to 151,292
- Mean: 29.3
- Median: 0.028
- Negative values: 283 (adjustments/balancing items)
- Missing values: 0

## Code Lists

### Set_i / Set_j Categories (181 unique codes)

**Products (CPA 2.1 classification, 64 codes):**
- `CPA_A01` – Products of agriculture
- `CPA_A02` – Products of forestry
- `CPA_A03` – Fish and aquaculture products
- `CPA_B` – Mining and quarrying products
- `CPA_C10-12` to `CPA_C33` – Manufacturing products
- `CPA_D35` – Electricity, gas, steam
- `CPA_E36` to `CPA_E37-39` – Water, sewerage, waste
- `CPA_F` – Constructions and construction works
- `CPA_G45` to `CPA_G47` – Trade services
- `CPA_H49` to `CPA_H53` – Transportation services
- `CPA_I` – Accommodation and food services
- `CPA_J58` to `CPA_J62_63` – Information and communication
- `CPA_K64` to `CPA_K66` – Financial services
- `CPA_L` – Real estate services
- `CPA_M69_70` to `CPA_M74_75` – Professional services
- `CPA_N77` to `CPA_N80-82` – Administrative services
- `CPA_O84` – Public administration services
- `CPA_P85` – Education services
- `CPA_Q86` to `CPA_Q87_88` – Health and social work
- `CPA_R90-92` to `CPA_R93` – Arts and recreation
- `CPA_S94` to `CPA_S96` – Other services
- `CPA_T` – Household services

**Industries (NACE Rev. 2, 64 codes):**
- `A01`, `A02`, `A03` – Agriculture, forestry, fishing
- `B` – Mining and quarrying
- `C10-C12` to `C33` – Manufacturing
- `D35` – Electricity, gas
- `E36`, `E37-E39` – Water supply, waste
- `F` – Construction
- `G45`, `G46`, `G47` – Trade
- `H49` to `H53` – Transportation
- `I` – Accommodation and food
- `J58` to `J62_J63` – Information and communication
- `K64`, `K65`, `K66` – Financial and insurance
- `L` – Real estate
- `M69_M70` to `M74_M75` – Professional services
- `N77` to `N80-N82` – Administrative services
- `O84` – Public administration
- `P85` – Education
- `Q86`, `Q87_Q88` – Health
- `R90-R92`, `R93` – Arts and recreation
- `S94`, `S95`, `S96` – Other services
- `T` – Households as employers

**National Accounts codes:**

| Prefix | Category | Examples |
|--------|----------|----------|
| `D*` | Distributive transactions | D11 (wages), D12 (employer contributions), D21X31 (taxes-subsidies), D4 (property income), D5 (taxes on income), D61/D62 (social contributions/benefits), D7 (transfers), D8 (capital transfers), D9 (other) |
| `B*` | Balancing items | B2 (operating surplus), B3 (mixed income), B8_S* (saving by sector), B9FX9 (net lending) |
| `P*` | Products/expenditure | P3_S13/S14/S15 (final consumption by sector), P33 (valuables), P51G (GFCF), P7 (imports) |
| `F*` | Financial instruments | F1 (monetary gold), F21/F22 (currency/deposits), F29 (other deposits), F31/F32 (debt securities), F41/F42 (loans), F51/F52 (equity), F6 (insurance), F7 (derivatives), F8 (other) |
| `S*` | Institutional sectors | S11 (non-financial corps), S12 (financial corps), S13 (government), S14 (households), S15 (NPISH), S2 (rest of world) |
| `N*` | Non-financial assets | N111G (dwellings), N112G (other buildings), N1131G/N1132G (transport equipment), N115G (ICT), N1171G/N1179G (IP products), N11OG (other) |
| `NP` | Non-produced assets | Natural resources, contracts, etc. |

### Country Codes (m column)

All 50 values in `m` match the `ctr` partition values – representing bilateral trade/flow partners.

## Data Quality Notes

**Completeness:**
- Full coverage: 14 years x 50 countries = 700 files
- No missing values in any file
- Complete matrix: ~120,000 rows per country-year

**Data characteristics:**
- Sparse matrix with many small values (median 0.028)
- Negative values present (283 in sample) – represent adjustments, discrepancies, or capital flows
- Large outliers (max 151,292) – major economic aggregates

## Access

Data provided by David Zenz (wiiw). Original source: Eurostat FIGARO database.

**Note:** The `data/` folder is excluded from version control via `.gitignore` due to file size (191 MB). Data must be obtained separately and placed in the `data/parquet/` directory.

## Technical Notes

Reading partitioned Parquet in Python:
```python
import pyarrow.parquet as pq

dataset = pq.ParquetDataset('data/parquet/')
table = dataset.read()
df = table.to_pandas()
```

Reading with filters:
```python
import pyarrow.parquet as pq

# Read specific country and year
df = pq.read_table(
    'data/parquet/',
    filters=[('base', '=', '2020'), ('ctr', '=', 'DE')]
).to_pandas()
```

Reading partitioned Parquet in R:
```r
library(arrow)

df <- open_dataset("data/parquet/") |>
  filter(base == 2020, ctr == "DE") |>
  collect()
```
