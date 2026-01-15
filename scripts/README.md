# Exploration Scripts

Phase 2 exploration scripts for FIGARO-NAM data analysis.

## Scripts

| Script | Purpose | Output |
|--------|---------|--------|
| `01_data_quality.py` | Coverage, missing values, distributions | `outputs/tables/*.csv` |
| `02_top_flows.py` | Top flows, dominant sectors, trade partners | `outputs/tables/*.csv` |
| `03_temporal_analysis.py` | Time series, structural breaks | `outputs/tables/*.csv` |
| `04_visualizations.py` | Heatmaps, bar charts, time series | `outputs/figures/*.png` |

## Usage

```bash
# From project root
cd wiiw-figaro-nam-demo

# Run all scripts
python scripts/01_data_quality.py
python scripts/02_top_flows.py
python scripts/03_temporal_analysis.py
python scripts/04_visualizations.py
```

## Requirements

```bash
pip install pyarrow pandas numpy matplotlib seaborn
```

## Output Directory

```
outputs/
  tables/     # CSV data files
  figures/    # PNG visualizations
```

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

### 04_visualizations.py

Generates publication-ready figures:
- Heatmap of structural breaks across countries
- Diverging bar chart of sectoral winners/losers
- Time series with crisis period markers
- Country comparison bar chart

## Notes

- All values in billion EUR (nominal, not inflation-adjusted)
- Domestic flows = where m == ctr
- Foreign flows (imports) = where m != ctr
- Negative values represent adjustments/balancing items
