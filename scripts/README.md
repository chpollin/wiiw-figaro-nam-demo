# Exploration Scripts

Phase 2 exploration scripts for FIGARO-NAM data analysis.

## Scripts

| Script | Purpose | Output |
|--------|---------|--------|
| `01_data_quality.py` | Coverage, missing values, distributions | `outputs/coverage_matrix.csv`, `outputs/country_statistics.csv`, `outputs/block_structure.csv` |
| `02_top_flows.py` | Top flows, dominant sectors, trade partners | `outputs/country_summary.csv`, `outputs/DE_*.csv` |
| `03_temporal_analysis.py` | Time series, structural breaks | `outputs/DE_time_series.csv`, `outputs/structural_breaks_comparison.csv` |

## Usage

```bash
# From project root
cd wiiw-figaro-nam-demo

# Run all scripts
python scripts/01_data_quality.py
python scripts/02_top_flows.py
python scripts/03_temporal_analysis.py
```

## Requirements

```bash
pip install pyarrow pandas numpy
```

## Output Directory

All outputs are saved to `outputs/` (created automatically).

## Script Details

### 01_data_quality.py

Checks data completeness and quality:
- Verifies 700 country-year combinations
- Checks for missing values (none expected)
- Analyzes value distributions
- Identifies outliers using IQR method
- Categorizes Set_i/Set_j codes by type

### 02_top_flows.py

Identifies dominant patterns:
- Largest flows by absolute value
- Value added by industry (D11 wages, B2 surplus)
- Intermediate consumption patterns
- Final demand composition (household, government, investment)
- Trading partners and import structure

### 03_temporal_analysis.py

Analyzes changes over time:
- 14-year time series (2010-2023)
- Year-over-year percentage changes
- COVID structural break (2019-2020)
- Energy crisis impact (2021-2022)
- Sectoral dynamics comparison
- Cross-country comparison

## Notes

- All values in billion EUR (nominal, not inflation-adjusted)
- Domestic flows = where m == ctr
- Foreign flows (imports) = where m != ctr
- Negative values represent adjustments/balancing items
