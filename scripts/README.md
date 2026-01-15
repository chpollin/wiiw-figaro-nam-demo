# Exploration Scripts

Phase 2 exploration scripts for FIGARO-NAM data analysis.

## Scripts

### Phase 2a: Base Exploration

| Script | Purpose | Output |
|--------|---------|--------|
| `01_data_quality.py` | Coverage, missing values, distributions | `outputs/tables/*.csv` |
| `02_top_flows.py` | Top flows, dominant sectors, trade partners | `outputs/tables/*.csv` |
| `03_temporal_analysis.py` | Time series, structural breaks | `outputs/tables/*.csv` |
| `04_visualizations.py` | Heatmaps, bar charts, time series | `outputs/figures/*.png` |

### Phase 2b: Extended Exploration

| Script | Purpose | Output |
|--------|---------|--------|
| `05_baseline_trend.py` | CAGR 2010-2018, trend deviation 2020 | `outputs/tables/*.csv`, `outputs/figures/*.png` |
| `06_export_analysis.py` | Export structure, trade balance by partner | `outputs/tables/*.csv`, `outputs/figures/*.png` |
| `07_negative_values.py` | Categorize 204k negative values | `outputs/tables/*.csv` |
| `08_io_linkages.py` | Intersectoral linkages, backward/forward | `outputs/tables/*.csv`, `outputs/figures/*.png` |

## Usage

```bash
# From project root
cd wiiw-figaro-nam-demo

# Run Phase 2a scripts
python scripts/01_data_quality.py
python scripts/02_top_flows.py
python scripts/03_temporal_analysis.py
python scripts/04_visualizations.py

# Run Phase 2b scripts
python scripts/05_baseline_trend.py
python scripts/06_export_analysis.py
python scripts/07_negative_values.py
python scripts/08_io_linkages.py
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

### 05_baseline_trend.py

Calculates long-term trends as COVID reference:
- CAGR (Compound Annual Growth Rate) 2010-2018 per country/aggregate
- Trend extrapolation to 2020
- Deviation of actual 2020 values from trend
- Key insight: quantifies COVID impact beyond simple YoY changes

### 06_export_analysis.py

Analyzes export structure (complement to import analysis):
- Top export destinations per country
- Exported products by category
- Export/Import balance by partner
- Trade balance visualization

### 07_negative_values.py

Categorizes and explains ~204k negative values:
- Distribution by Set_i/Set_j categories
- Temporal development
- Country differences
- Interpretation: taxes minus subsidies, adjustments, inventory changes

### 08_io_linkages.py

Analyzes intersectoral economic linkages:
- Product-to-industry intermediate consumption matrix
- Backward linkages (how much each industry buys)
- Forward linkages (how much each product supplies)
- Top intersectoral flows
- Heatmap visualization

## Notes

- All values in billion EUR (nominal, not inflation-adjusted)
- Domestic flows = where m == ctr
- Foreign flows (imports) = where m != ctr
- Negative values represent adjustments/balancing items
