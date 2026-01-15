"""
05_baseline_trend.py - Phase 2b: Baseline Trend Analysis

This script calculates long-term trends (2010-2018) as reference for COVID impact assessment:
1. CAGR (Compound Annual Growth Rate) per aggregate and country
2. Trend extrapolation to 2020
3. Deviation of actual 2020 values from trend

Output: CSV tables and visualization to outputs/

Usage:
    python scripts/05_baseline_trend.py
"""

import pandas as pd
import numpy as np
import pyarrow.parquet as pq
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuration
DATA_PATH = Path('data/parquet/')
OUTPUT_PATH = Path('outputs/')
TABLES_PATH = OUTPUT_PATH / 'tables'
FIGURES_PATH = OUTPUT_PATH / 'figures'
TABLES_PATH.mkdir(exist_ok=True)
FIGURES_PATH.mkdir(exist_ok=True)

# Sample countries for analysis
SAMPLE_COUNTRIES = ['DE', 'FR', 'IT', 'ES', 'NL', 'PL', 'AT', 'GR']

# Key aggregates to analyze
KEY_AGGREGATES = {
    'P3_S14': 'HH Consumption',
    'P3_S13': 'Gov Consumption',
    'P51G': 'Investment',
    'P6': 'Exports'
}

# Style settings
plt.style.use('seaborn-v0_8-whitegrid')
NOMINAL_DISCLAIMER = "Source: FIGARO-NAM (Eurostat). All values nominal, not inflation-adjusted."


def load_country_year(country: str, year: int) -> pd.DataFrame:
    """Load data for a specific country and year."""
    file_path = DATA_PATH / f'base={year}' / f'ctr={country}' / 'part-0.parquet'
    if file_path.exists():
        return pq.read_table(file_path).to_pandas()
    return pd.DataFrame()


def calculate_aggregate(df: pd.DataFrame, aggregate: str) -> float:
    """Calculate total value for a specific aggregate."""
    if df.empty:
        return np.nan
    # Filter for the aggregate in Set_j (usage side)
    mask = df['Set_j'] == aggregate
    return df.loc[mask, 'value'].sum()


def calculate_cagr(start_value: float, end_value: float, years: int) -> float:
    """Calculate Compound Annual Growth Rate."""
    if start_value <= 0 or end_value <= 0 or years <= 0:
        return np.nan
    return (end_value / start_value) ** (1 / years) - 1


def analyze_trends():
    """Analyze long-term trends 2010-2018 and compare with 2020."""
    print("Calculating baseline trends (2010-2018)...")

    # Collect time series data
    results = []

    for country in SAMPLE_COUNTRIES:
        print(f"  Processing {country}...")
        country_data = {}

        # Load years 2010-2018 for baseline, plus 2019-2020 for comparison
        for year in range(2010, 2021):
            df = load_country_year(country, year)
            for agg_code, agg_name in KEY_AGGREGATES.items():
                value = calculate_aggregate(df, agg_code)
                key = (country, agg_name, year)
                country_data[key] = value

        # Calculate CAGR 2010-2018
        for agg_code, agg_name in KEY_AGGREGATES.items():
            val_2010 = country_data.get((country, agg_name, 2010), np.nan)
            val_2018 = country_data.get((country, agg_name, 2018), np.nan)
            val_2019 = country_data.get((country, agg_name, 2019), np.nan)
            val_2020 = country_data.get((country, agg_name, 2020), np.nan)

            cagr = calculate_cagr(val_2010, val_2018, 8)

            # Extrapolate trend to 2020 (2 years from 2018)
            if not np.isnan(cagr) and not np.isnan(val_2018):
                trend_2020 = val_2018 * (1 + cagr) ** 2
            else:
                trend_2020 = np.nan

            # Calculate deviation
            if not np.isnan(trend_2020) and trend_2020 > 0:
                deviation_pct = (val_2020 - trend_2020) / trend_2020 * 100
            else:
                deviation_pct = np.nan

            # YoY change 2019-2020 for reference
            if not np.isnan(val_2019) and val_2019 > 0:
                yoy_change = (val_2020 - val_2019) / val_2019 * 100
            else:
                yoy_change = np.nan

            results.append({
                'Country': country,
                'Aggregate': agg_name,
                'Value_2010': val_2010,
                'Value_2018': val_2018,
                'Value_2020': val_2020,
                'CAGR_2010_2018': cagr * 100 if not np.isnan(cagr) else np.nan,
                'Trend_2020': trend_2020,
                'Deviation_from_Trend_%': deviation_pct,
                'YoY_2019_2020_%': yoy_change
            })

    return pd.DataFrame(results)


def create_trend_tables(df: pd.DataFrame):
    """Create and save trend analysis tables."""
    print("\nSaving trend tables...")

    # Table 1: CAGR by country and aggregate
    cagr_pivot = df.pivot_table(
        index='Country',
        columns='Aggregate',
        values='CAGR_2010_2018',
        aggfunc='first'
    ).round(2)
    cagr_pivot.to_csv(TABLES_PATH / 'baseline_trends_cagr.csv')
    print(f"  Saved: {TABLES_PATH / 'baseline_trends_cagr.csv'}")

    # Table 2: Trend deviation 2020
    deviation_pivot = df.pivot_table(
        index='Country',
        columns='Aggregate',
        values='Deviation_from_Trend_%',
        aggfunc='first'
    ).round(2)
    deviation_pivot.to_csv(TABLES_PATH / 'trend_deviation_2020.csv')
    print(f"  Saved: {TABLES_PATH / 'trend_deviation_2020.csv'}")

    # Table 3: Full results
    df.to_csv(TABLES_PATH / 'baseline_trend_analysis.csv', index=False)
    print(f"  Saved: {TABLES_PATH / 'baseline_trend_analysis.csv'}")

    return cagr_pivot, deviation_pivot


def plot_trend_deviation(df: pd.DataFrame):
    """Create visualization of trend deviation."""
    print("\nCreating trend deviation chart...")

    # Filter for HH Consumption (most impacted by COVID)
    hh_data = df[df['Aggregate'] == 'HH Consumption'].copy()
    hh_data = hh_data.sort_values('Deviation_from_Trend_%')

    # Create figure with two panels
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Panel 1: Deviation from trend
    ax1 = axes[0]
    colors = ['#d62728' if x < 0 else '#2ca02c' for x in hh_data['Deviation_from_Trend_%']]
    bars = ax1.barh(hh_data['Country'], hh_data['Deviation_from_Trend_%'], color=colors)
    ax1.axvline(x=0, color='black', linewidth=0.8)
    ax1.set_xlabel('Deviation from 2010-2018 Trend (%)')
    ax1.set_title('HH Consumption 2020: Actual vs. Trend\n(Based on CAGR 2010-2018)',
                  fontsize=11, fontweight='bold')

    # Add value labels
    for bar, val in zip(bars, hh_data['Deviation_from_Trend_%']):
        x_pos = val + 0.5 if val >= 0 else val - 0.5
        ha = 'left' if val >= 0 else 'right'
        ax1.text(x_pos, bar.get_y() + bar.get_height()/2, f'{val:.1f}%',
                 va='center', ha=ha, fontsize=9)

    # Panel 2: CAGR comparison
    ax2 = axes[1]

    # Prepare data for grouped bar chart
    agg_order = ['HH Consumption', 'Gov Consumption', 'Investment', 'Exports']
    cagr_data = df.pivot_table(
        index='Country',
        columns='Aggregate',
        values='CAGR_2010_2018',
        aggfunc='first'
    ).reindex(columns=agg_order)

    x = np.arange(len(cagr_data.index))
    width = 0.2

    for i, agg in enumerate(agg_order):
        ax2.bar(x + i * width, cagr_data[agg], width, label=agg)

    ax2.set_ylabel('CAGR 2010-2018 (%)')
    ax2.set_title('Baseline Growth Rates by Country\n(Pre-COVID Period)',
                  fontsize=11, fontweight='bold')
    ax2.set_xticks(x + width * 1.5)
    ax2.set_xticklabels(cagr_data.index)
    ax2.legend(loc='upper right', fontsize=8)
    ax2.axhline(y=0, color='black', linewidth=0.5)

    # Add disclaimer
    fig.text(0.5, 0.02, NOMINAL_DISCLAIMER, ha='center', fontsize=8, style='italic', color='gray')

    plt.tight_layout(rect=[0, 0.05, 1, 1])
    fig.savefig(FIGURES_PATH / 'trend_deviation_chart.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {FIGURES_PATH / 'trend_deviation_chart.png'}")


def main():
    """Run baseline trend analysis."""
    print("FIGARO-NAM Baseline Trend Analysis")
    print("=" * 60)

    # Analyze trends
    results_df = analyze_trends()

    # Create tables
    cagr_table, deviation_table = create_trend_tables(results_df)

    # Create visualization
    plot_trend_deviation(results_df)

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY: Trend Deviation Analysis")
    print("=" * 60)

    print("\nCAGR 2010-2018 (%):")
    print(cagr_table.to_string())

    print("\n\nDeviation from Trend 2020 (%):")
    print(deviation_table.to_string())

    print("\n" + "=" * 60)
    print("Key Finding: COVID impact vs. long-term trend")
    print("=" * 60)

    # Find most impacted
    hh_deviation = results_df[results_df['Aggregate'] == 'HH Consumption']
    worst = hh_deviation.loc[hh_deviation['Deviation_from_Trend_%'].idxmin()]
    print(f"\nMost impacted: {worst['Country']} HH Consumption")
    print(f"  - CAGR 2010-2018: {worst['CAGR_2010_2018']:.1f}%")
    print(f"  - Trend 2020 would have been: {worst['Trend_2020']/1e6:.2f} trillion EUR")
    print(f"  - Actual 2020: {worst['Value_2020']/1e6:.2f} trillion EUR")
    print(f"  - Deviation from trend: {worst['Deviation_from_Trend_%']:.1f}%")


if __name__ == '__main__':
    main()
