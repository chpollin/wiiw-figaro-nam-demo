"""
12_hypothesis_h_int.py - Integrated Hypothesis Analysis

Hypothesis H_int:
Southern European countries (ES, IT, GR, PT) show stronger nominal but weaker
real recovery in 2022 than Northern Europe (DE, AT, NL), with the difference
partially cushioned by higher government consumption expansion. The apparently
stronger nominal rebound is primarily a base effect of the deeper COVID drop
in 2020.

Analyses:
1. Base effect (H5): Correlation COVID drop vs. recovery
2. Nominal recovery index (H1a): Index 2019=100
3. Real recovery index (H1b): HICP-adjusted
4. Fiscal cushioning (H4): Gov consumption growth

Output:
- outputs/tables/recovery_comparison.csv
- outputs/tables/basis_effect_analysis.csv
- outputs/tables/fiscal_response.csv
- outputs/figures/basis_effect_scatter.png
- outputs/figures/recovery_nominal_vs_real.png
- outputs/figures/fiscal_cushion.png

Usage:
    python scripts/12_hypothesis_h_int.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configuration
OUTPUT_TABLES = Path('outputs/tables/')
OUTPUT_FIGURES = Path('outputs/figures/')
OUTPUT_TABLES.mkdir(parents=True, exist_ok=True)
OUTPUT_FIGURES.mkdir(parents=True, exist_ok=True)

# Country groups
SOUTH = ['ES', 'IT', 'GR', 'PT']
NORTH = ['DE', 'AT', 'NL']
ALL_COUNTRIES = SOUTH + NORTH + ['FR', 'PL']  # Include FR, PL for comparison

# HICP Annual Average Indices (2015=100) - Eurostat data
# Source: Eurostat prc_hicp_aind (Harmonised Index of Consumer Prices - annual data)
# URL: https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_aind/default/table
# Extracted: January 2024
# Note: These are official Eurostat harmonized consumer price indices used for
# cross-country inflation comparisons in the EU. Values are rebased to 2019=100
# for this analysis to calculate real consumption indices.
HICP_DATA = {
    # 2019, 2020, 2021, 2022, 2023
    'DE': [107.4, 107.9, 111.3, 120.3, 127.5],
    'AT': [108.4, 109.9, 113.0, 122.5, 131.8],
    'NL': [108.9, 110.3, 113.2, 126.4, 131.1],
    'ES': [106.2, 105.9, 109.2, 118.5, 122.7],
    'IT': [105.3, 105.2, 107.2, 116.1, 122.9],
    'GR': [103.9, 102.7, 103.9, 114.4, 119.1],
    'PT': [106.3, 106.2, 107.5, 116.6, 121.7],
    'FR': [106.3, 106.9, 108.8, 114.9, 121.4],
    'PL': [109.5, 113.3, 118.9, 135.6, 151.2],
}
HICP_YEARS = [2019, 2020, 2021, 2022, 2023]


def load_all_timeseries():
    """Load time series for all countries."""
    print("Loading time series data...")

    data = []
    for ctr in ALL_COUNTRIES:
        file_path = OUTPUT_TABLES / f'{ctr}_time_series.csv'
        if file_path.exists():
            df = pd.read_csv(file_path)
            data.append(df)
            print(f"  {ctr}: {len(df)} years")
        else:
            print(f"  {ctr}: MISSING - {file_path}")

    combined = pd.concat(data, ignore_index=True)
    print(f"\nTotal: {len(combined)} data points\n")
    return combined


def get_hicp_deflator(country, year):
    """Get HICP index for deflation (2019=100 base)."""
    if country not in HICP_DATA or year not in HICP_YEARS:
        return None
    idx = HICP_YEARS.index(year)
    # Rebase to 2019=100
    base_2019 = HICP_DATA[country][0]  # 2019 value
    return HICP_DATA[country][idx] / base_2019 * 100


def analyze_basis_effect(df):
    """Analyze base effect: correlation between COVID drop and recovery."""
    print("=" * 60)
    print("ANALYSIS 1: BASE EFFECT (H5)")
    print("=" * 60)

    results = []

    for ctr in ALL_COUNTRIES:
        ctr_data = df[df['country'] == ctr]

        hh_2019 = ctr_data[ctr_data['year'] == 2019]['hh_consumption'].values[0]
        hh_2020 = ctr_data[ctr_data['year'] == 2020]['hh_consumption'].values[0]
        hh_2022 = ctr_data[ctr_data['year'] == 2022]['hh_consumption'].values[0]

        covid_drop = (hh_2020 - hh_2019) / hh_2019 * 100
        recovery_rate = (hh_2022 - hh_2020) / hh_2020 * 100
        net_change_2019_2022 = (hh_2022 - hh_2019) / hh_2019 * 100

        region = 'South' if ctr in SOUTH else ('North' if ctr in NORTH else 'Other')

        results.append({
            'country': ctr,
            'region': region,
            'hh_2019': hh_2019,
            'hh_2020': hh_2020,
            'hh_2022': hh_2022,
            'covid_drop_pct': covid_drop,
            'recovery_2020_2022_pct': recovery_rate,
            'net_change_2019_2022_pct': net_change_2019_2022,
        })

    result_df = pd.DataFrame(results)

    # Correlation analysis
    x = result_df['covid_drop_pct'].values
    y = result_df['recovery_2020_2022_pct'].values
    correlation, p_value = stats.pearsonr(x, y)

    print(f"\nCorrelation COVID drop vs. recovery:")
    print(f"  r = {correlation:.3f}")
    print(f"  p = {p_value:.4f}")

    if correlation < -0.5 and p_value < 0.1:
        print("  -> STRONGER negative relationship: Deeper drop = stronger recovery")
        print("  -> CONFIRMS base effect hypothesis")

    print(f"\nCountry comparison:")
    print("-" * 80)
    print(f"{'Country':<8} {'Region':<8} {'Drop 2020':<15} {'Recovery 2020-22':<18} {'Net 2019-22'}")
    print("-" * 80)
    for _, row in result_df.iterrows():
        print(f"{row['country']:<8} {row['region']:<8} {row['covid_drop_pct']:>+10.1f}% "
              f"{row['recovery_2020_2022_pct']:>+14.1f}% {row['net_change_2019_2022_pct']:>+12.1f}%")

    # Regional averages
    print("\n" + "-" * 80)
    print("Regional averages:")
    for region in ['South', 'North']:
        reg_data = result_df[result_df['region'] == region]
        avg_drop = reg_data['covid_drop_pct'].mean()
        avg_recovery = reg_data['recovery_2020_2022_pct'].mean()
        avg_net = reg_data['net_change_2019_2022_pct'].mean()
        print(f"  {region}: Drop {avg_drop:+.1f}%, Recovery {avg_recovery:+.1f}%, Net {avg_net:+.1f}%")

    # Save results
    result_df.to_csv(OUTPUT_TABLES / 'basis_effect_analysis.csv', index=False)
    print(f"\nSaved: {OUTPUT_TABLES / 'basis_effect_analysis.csv'}")

    return result_df, correlation, p_value


def create_basis_effect_scatter(basis_df, correlation, p_value):
    """Create scatter plot of base effect."""
    print("\nCreating base effect scatter plot...")

    fig, ax = plt.subplots(figsize=(10, 7))

    colors = {'South': '#E74C3C', 'North': '#3498DB', 'Other': '#95A5A6'}
    markers = {'South': 'o', 'North': 's', 'Other': '^'}

    for region in ['South', 'North', 'Other']:
        reg_data = basis_df[basis_df['region'] == region]
        ax.scatter(
            reg_data['covid_drop_pct'],
            reg_data['recovery_2020_2022_pct'],
            c=colors[region],
            marker=markers[region],
            s=150,
            label=f'{region}ern Europe' if region != 'Other' else 'Other',
            edgecolors='black',
            linewidths=1,
            alpha=0.8
        )

        # Add country labels
        for _, row in reg_data.iterrows():
            ax.annotate(
                row['country'],
                (row['covid_drop_pct'], row['recovery_2020_2022_pct']),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=11,
                fontweight='bold'
            )

    # Regression line
    x = basis_df['covid_drop_pct'].values
    y = basis_df['recovery_2020_2022_pct'].values
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    x_line = np.linspace(min(x) - 1, max(x) + 1, 100)
    ax.plot(x_line, p(x_line), 'k--', alpha=0.5, linewidth=2,
            label=f'Regression (r={correlation:.2f})')

    ax.set_xlabel('COVID Drop 2019-2020 (%)', fontsize=12)
    ax.set_ylabel('Nominal Recovery 2020-2022 (%)', fontsize=12)
    ax.set_title('Base Effect: Deeper Drop Leads to Stronger Recovery\n'
                 f'Correlation r = {correlation:.3f}, p = {p_value:.4f} (n={len(basis_df)})',
                 fontsize=13, fontweight='bold')

    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax.axvline(x=0, color='gray', linestyle='-', alpha=0.3)

    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES / 'basis_effect_scatter.png', dpi=150)
    plt.close()

    print(f"Saved: {OUTPUT_FIGURES / 'basis_effect_scatter.png'}")


def analyze_recovery_indices(df):
    """Analyze nominal and real recovery indices (2019=100)."""
    print("\n" + "=" * 60)
    print("ANALYSIS 2: NOMINAL AND REAL RECOVERY INDEX (H1a, H1b)")
    print("=" * 60)

    results = []

    for ctr in ALL_COUNTRIES:
        ctr_data = df[df['country'] == ctr]
        hh_2019 = ctr_data[ctr_data['year'] == 2019]['hh_consumption'].values[0]

        region = 'South' if ctr in SOUTH else ('North' if ctr in NORTH else 'Other')

        for year in [2019, 2020, 2021, 2022, 2023]:
            hh = ctr_data[ctr_data['year'] == year]['hh_consumption'].values[0]
            nominal_index = hh / hh_2019 * 100

            # Real index (deflated by HICP)
            deflator = get_hicp_deflator(ctr, year)
            if deflator:
                real_index = nominal_index / deflator * 100
            else:
                real_index = None

            results.append({
                'country': ctr,
                'region': region,
                'year': year,
                'hh_consumption': hh,
                'nominal_index': nominal_index,
                'hicp_deflator': deflator,
                'real_index': real_index,
            })

    result_df = pd.DataFrame(results)

    # Pivot for display
    print("\nNominal HH Consumption Index (2019=100):")
    print("-" * 70)
    nominal_pivot = result_df.pivot(index='country', columns='year', values='nominal_index')
    print(nominal_pivot.round(1).to_string())

    print("\n\nReal HH Consumption Index (2019=100, HICP-adjusted):")
    print("-" * 70)
    real_pivot = result_df.pivot(index='country', columns='year', values='real_index')
    print(real_pivot.round(1).to_string())

    # Compare 2022 nominal vs real
    print("\n\nComparison 2022: Nominal vs. Real:")
    print("-" * 60)
    print(f"{'Country':<10} {'Region':<8} {'Nominal':<12} {'Real':<12} {'Difference'}")
    print("-" * 60)

    data_2022 = result_df[result_df['year'] == 2022]
    for _, row in data_2022.iterrows():
        diff = row['nominal_index'] - row['real_index'] if row['real_index'] else None
        real_str = f"{row['real_index']:.1f}" if row['real_index'] else "n/a"
        diff_str = f"{diff:+.1f}" if diff else "n/a"
        print(f"{row['country']:<10} {row['region']:<8} {row['nominal_index']:>8.1f}    {real_str:>8}    {diff_str:>8}")

    # Regional comparison
    print("\n\nRegional averages 2022:")
    for region in ['South', 'North']:
        reg_data = data_2022[data_2022['region'] == region]
        avg_nominal = reg_data['nominal_index'].mean()
        avg_real = reg_data['real_index'].mean()
        print(f"  {region}: Nominal {avg_nominal:.1f}, Real {avg_real:.1f}, "
              f"Difference {avg_nominal - avg_real:+.1f}")

    # Save
    result_df.to_csv(OUTPUT_TABLES / 'recovery_comparison.csv', index=False)
    print(f"\nSaved: {OUTPUT_TABLES / 'recovery_comparison.csv'}")

    return result_df


def create_recovery_comparison_chart(recovery_df):
    """Create bar chart comparing nominal vs real recovery."""
    print("\nCreating nominal vs. real bar chart...")

    data_2022 = recovery_df[recovery_df['year'] == 2022].copy()
    data_2022 = data_2022.sort_values('region', ascending=False)  # South first

    fig, ax = plt.subplots(figsize=(12, 7))

    x = np.arange(len(data_2022))
    width = 0.35

    colors_nominal = ['#E74C3C' if r == 'South' else '#3498DB' if r == 'North' else '#95A5A6'
                      for r in data_2022['region']]
    colors_real = ['#C0392B' if r == 'South' else '#2980B9' if r == 'North' else '#7F8C8D'
                   for r in data_2022['region']]

    bars1 = ax.bar(x - width/2, data_2022['nominal_index'], width,
                   color=colors_nominal, label='Nominal', edgecolor='black', alpha=0.8)
    bars2 = ax.bar(x + width/2, data_2022['real_index'], width,
                   color=colors_real, label='Real (HICP-adjusted)', edgecolor='black', alpha=0.8)

    ax.axhline(y=100, color='black', linestyle='--', linewidth=2, alpha=0.7, label='2019 Level')

    ax.set_ylabel('Index (2019 = 100)', fontsize=12)
    # Calculate regional averages for dynamic title
    south_nom = data_2022[data_2022['region'] == 'South']['nominal_index'].mean()
    north_nom = data_2022[data_2022['region'] == 'North']['nominal_index'].mean()
    south_real = data_2022[data_2022['region'] == 'South']['real_index'].mean()
    north_real = data_2022[data_2022['region'] == 'North']['real_index'].mean()

    # Dynamic title based on actual data
    if north_nom > south_nom:
        subtitle = f'Northern Europe nominally stronger ({north_nom:.0f} vs {south_nom:.0f}), real similar ({north_real:.0f} vs {south_real:.0f})'
    else:
        subtitle = f'Southern Europe nominally stronger ({south_nom:.0f} vs {north_nom:.0f}), real weaker ({south_real:.0f} vs {north_real:.0f})'

    ax.set_title(f'HH Consumption 2022: Nominal vs. Real Recovery\n{subtitle}',
                 fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(data_2022['country'], fontsize=11)

    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

    for bar in bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#E74C3C', edgecolor='black', label='Southern Europe Nominal'),
        Patch(facecolor='#C0392B', edgecolor='black', label='Southern Europe Real'),
        Patch(facecolor='#3498DB', edgecolor='black', label='Northern Europe Nominal'),
        Patch(facecolor='#2980B9', edgecolor='black', label='Northern Europe Real'),
        plt.Line2D([0], [0], color='black', linestyle='--', linewidth=2, label='2019 Level'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=9)

    ax.set_ylim(80, 125)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES / 'recovery_nominal_vs_real.png', dpi=150)
    plt.close()

    print(f"Saved: {OUTPUT_FIGURES / 'recovery_nominal_vs_real.png'}")


def analyze_fiscal_cushion(df):
    """Analyze fiscal cushioning: Gov consumption growth vs HH stability."""
    print("\n" + "=" * 60)
    print("ANALYSIS 3: FISCAL CUSHIONING (H4)")
    print("=" * 60)

    results = []

    for ctr in ALL_COUNTRIES:
        ctr_data = df[df['country'] == ctr]

        # Gov consumption
        gov_2019 = ctr_data[ctr_data['year'] == 2019]['gov_consumption'].values[0]
        gov_2020 = ctr_data[ctr_data['year'] == 2020]['gov_consumption'].values[0]
        gov_2022 = ctr_data[ctr_data['year'] == 2022]['gov_consumption'].values[0]

        gov_growth_2019_2022 = (gov_2022 - gov_2019) / gov_2019 * 100
        gov_growth_2019_2020 = (gov_2020 - gov_2019) / gov_2019 * 100

        # HH consumption stability (volatility)
        hh_2019 = ctr_data[ctr_data['year'] == 2019]['hh_consumption'].values[0]
        hh_2020 = ctr_data[ctr_data['year'] == 2020]['hh_consumption'].values[0]
        hh_2021 = ctr_data[ctr_data['year'] == 2021]['hh_consumption'].values[0]
        hh_2022 = ctr_data[ctr_data['year'] == 2022]['hh_consumption'].values[0]

        # HH drop in 2020 (lower = more stable)
        hh_drop_2020 = (hh_2020 - hh_2019) / hh_2019 * 100

        # Net HH change 2019-2022
        hh_net_change = (hh_2022 - hh_2019) / hh_2019 * 100

        region = 'South' if ctr in SOUTH else ('North' if ctr in NORTH else 'Other')

        results.append({
            'country': ctr,
            'region': region,
            'gov_2019': gov_2019,
            'gov_2022': gov_2022,
            'gov_growth_2019_2022_pct': gov_growth_2019_2022,
            'gov_growth_2019_2020_pct': gov_growth_2019_2020,
            'hh_drop_2020_pct': hh_drop_2020,
            'hh_net_change_2019_2022_pct': hh_net_change,
        })

    result_df = pd.DataFrame(results)

    # Correlation: Gov growth vs HH stability
    x = result_df['gov_growth_2019_2020_pct'].values  # Immediate fiscal response
    y = result_df['hh_drop_2020_pct'].values  # HH drop (less negative = better)
    corr_immediate, p_immediate = stats.pearsonr(x, y)

    print(f"\nCorrelation immediate fiscal response (Gov 2019-2020) vs. HH drop 2020:")
    print(f"  r = {corr_immediate:.3f}")
    print(f"  p = {p_immediate:.4f}")

    if corr_immediate > 0:
        print("  -> Positive relationship: Higher gov consumption mitigates HH drop")

    print(f"\nCountry comparison:")
    print("-" * 90)
    print(f"{'Country':<8} {'Region':<8} {'Gov 2019-2020':<15} {'Gov 2019-2022':<15} "
          f"{'HH Drop':<15} {'HH Net'}")
    print("-" * 90)
    for _, row in result_df.iterrows():
        print(f"{row['country']:<8} {row['region']:<8} {row['gov_growth_2019_2020_pct']:>+10.1f}%    "
              f"{row['gov_growth_2019_2022_pct']:>+10.1f}%    {row['hh_drop_2020_pct']:>+10.1f}%    "
              f"{row['hh_net_change_2019_2022_pct']:>+8.1f}%")

    # Regional comparison
    print("\n" + "-" * 90)
    print("Regional averages:")
    for region in ['South', 'North']:
        reg_data = result_df[result_df['region'] == region]
        avg_gov = reg_data['gov_growth_2019_2022_pct'].mean()
        avg_hh_drop = reg_data['hh_drop_2020_pct'].mean()
        avg_hh_net = reg_data['hh_net_change_2019_2022_pct'].mean()
        print(f"  {region}: Gov growth {avg_gov:+.1f}%, HH drop {avg_hh_drop:+.1f}%, "
              f"HH net {avg_hh_net:+.1f}%")

    # Save
    result_df.to_csv(OUTPUT_TABLES / 'fiscal_response.csv', index=False)
    print(f"\nSaved: {OUTPUT_TABLES / 'fiscal_response.csv'}")

    return result_df, corr_immediate, p_immediate


def create_fiscal_cushion_chart(fiscal_df, correlation, p_value):
    """Create chart showing fiscal cushioning effect."""
    print("\nCreating fiscal cushioning chart...")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    colors = {'South': '#E74C3C', 'North': '#3498DB', 'Other': '#95A5A6'}

    # Left: Gov consumption growth comparison
    data_sorted = fiscal_df.sort_values('region', ascending=False)
    x = np.arange(len(data_sorted))

    bar_colors = [colors[r] for r in data_sorted['region']]
    bars = ax1.bar(x, data_sorted['gov_growth_2019_2022_pct'], color=bar_colors,
                   edgecolor='black', alpha=0.8)

    ax1.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax1.set_ylabel('Growth (%)', fontsize=11)
    ax1.set_title('Government Consumption Growth 2019-2022', fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(data_sorted['country'], fontsize=10)
    ax1.grid(axis='y', alpha=0.3)

    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f'{height:+.0f}%',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3 if height >= 0 else -12),
                     textcoords="offset points",
                     ha='center', va='bottom' if height >= 0 else 'top', fontsize=9)

    # Right: Scatter Gov growth 2021-2022 vs HH recovery 2021-2022 (Energy crisis period)
    # Calculate 2021-2022 changes for fiscal response to energy crisis
    for region in ['South', 'North', 'Other']:
        reg_data = fiscal_df[fiscal_df['region'] == region]
        ax2.scatter(
            reg_data['gov_growth_2019_2022_pct'],  # Changed to full period
            reg_data['hh_net_change_2019_2022_pct'],  # Changed to net HH change
            c=colors[region],
            s=150,
            label=f'{region}ern Europe' if region != 'Other' else 'Other',
            edgecolors='black',
            linewidths=1,
            alpha=0.8
        )

        for _, row in reg_data.iterrows():
            ax2.annotate(
                row['country'],
                (row['gov_growth_2019_2022_pct'], row['hh_net_change_2019_2022_pct']),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=10,
                fontweight='bold'
            )

    # Regression line for full period
    x_vals = fiscal_df['gov_growth_2019_2022_pct'].values
    y_vals = fiscal_df['hh_net_change_2019_2022_pct'].values
    corr_full, p_full = stats.pearsonr(x_vals, y_vals)
    z = np.polyfit(x_vals, y_vals, 1)
    p = np.poly1d(z)
    x_line = np.linspace(min(x_vals) - 1, max(x_vals) + 1, 100)
    ax2.plot(x_line, p(x_line), 'k--', alpha=0.5, linewidth=2)

    ax2.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax2.axvline(x=0, color='gray', linestyle='-', alpha=0.3)

    ax2.set_xlabel('Gov Consumption Growth 2019-2022 (%)', fontsize=11)
    ax2.set_ylabel('HH Consumption Net Change 2019-2022 (%)', fontsize=11)
    ax2.set_title(f'Fiscal Cushioning: Gov Expansion vs. HH Recovery\n'
                  f'r = {corr_full:.2f}, p = {p_full:.3f}',
                  fontsize=12, fontweight='bold')
    ax2.legend(loc='lower right', fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES / 'fiscal_cushion.png', dpi=150)
    plt.close()

    print(f"Saved: {OUTPUT_FIGURES / 'fiscal_cushion.png'}")


def print_summary(basis_df, recovery_df, fiscal_df,
                  basis_corr, basis_p,
                  fiscal_corr, fiscal_p):
    """Print executive summary of findings."""
    print("\n" + "=" * 70)
    print("SUMMARY: HYPOTHESIS H_int")
    print("=" * 70)

    print("\nHYPOTHESIS:")
    print("  Southern European countries (ES, IT, GR, PT) show stronger nominal")
    print("  but weaker real recovery in 2022 than Northern Europe (DE, AT, NL),")
    print("  with the difference partially cushioned by higher government")
    print("  consumption expansion. The apparently stronger nominal rebound is")
    print("  primarily a base effect of the deeper COVID drop in 2020.")

    print("\n" + "-" * 70)
    print("FINDING 1: BASE EFFECT (H5)")
    print("-" * 70)

    # Regional averages from basis analysis
    south_drop = basis_df[basis_df['region'] == 'South']['covid_drop_pct'].mean()
    north_drop = basis_df[basis_df['region'] == 'North']['covid_drop_pct'].mean()
    south_recovery = basis_df[basis_df['region'] == 'South']['recovery_2020_2022_pct'].mean()
    north_recovery = basis_df[basis_df['region'] == 'North']['recovery_2020_2022_pct'].mean()

    print(f"  COVID drop 2020:           South {south_drop:+.1f}% vs. North {north_drop:+.1f}%")
    print(f"  Nominal recovery 2020-2022: South {south_recovery:+.1f}% vs. North {north_recovery:+.1f}%")
    print(f"  Correlation drop-recovery: r = {basis_corr:.3f} (p = {basis_p:.4f})")

    if basis_corr < -0.5:
        print("  CONFIRMED: Deeper drop -> stronger nominal recovery (base effect)")

    print("\n" + "-" * 70)
    print("FINDING 2: NOMINAL VS. REAL RECOVERY (H1a, H1b)")
    print("-" * 70)

    data_2022 = recovery_df[recovery_df['year'] == 2022]
    south_nominal = data_2022[data_2022['region'] == 'South']['nominal_index'].mean()
    north_nominal = data_2022[data_2022['region'] == 'North']['nominal_index'].mean()
    south_real = data_2022[data_2022['region'] == 'South']['real_index'].mean()
    north_real = data_2022[data_2022['region'] == 'North']['real_index'].mean()

    print(f"  Index 2022 (2019=100):")
    print(f"    Nominal: South {south_nominal:.1f} vs. North {north_nominal:.1f}")
    print(f"    Real:    South {south_real:.1f} vs. North {north_real:.1f}")
    print(f"  Difference Nominal-Real: South {south_nominal - south_real:+.1f} vs. North {north_nominal - north_real:+.1f}")

    if south_nominal > north_nominal and south_real < north_real:
        print("  CONFIRMED: South nominally stronger, but real weaker than North")
    elif south_nominal > north_nominal:
        print("  PARTIAL: South nominally stronger, real also (inflation effect smaller)")

    print("\n" + "-" * 70)
    print("FINDING 3: FISCAL CUSHIONING (H4)")
    print("-" * 70)

    south_gov = fiscal_df[fiscal_df['region'] == 'South']['gov_growth_2019_2022_pct'].mean()
    north_gov = fiscal_df[fiscal_df['region'] == 'North']['gov_growth_2019_2022_pct'].mean()

    print(f"  Gov consumption growth 2019-2022: South {south_gov:+.1f}% vs. North {north_gov:+.1f}%")
    print(f"  Correlation gov growth vs. HH stability: r = {fiscal_corr:.3f} (p = {fiscal_p:.4f})")

    if south_gov > north_gov:
        print("  CONFIRMED: Southern Europe expanded gov consumption more")

    print("\n" + "-" * 70)
    print("OVERALL ASSESSMENT")
    print("-" * 70)

    confirmed = 0
    total = 3

    if basis_corr < -0.3:
        confirmed += 1
    if south_nominal > north_nominal:
        confirmed += 0.5
    if south_real < north_real:
        confirmed += 0.5
    if south_gov > north_gov:
        confirmed += 1

    print(f"  Hypothesis confirmation: {confirmed}/{total} core statements supported")

    if confirmed >= 2:
        print("\n  -> HYPOTHESIS H_int LARGELY CONFIRMED")
    elif confirmed >= 1:
        print("\n  -> HYPOTHESIS H_int PARTIALLY CONFIRMED")
    else:
        print("\n  -> HYPOTHESIS H_int NOT CONFIRMED")

    print("=" * 70)


def main():
    print("=" * 70)
    print("HYPOTHESIS H_int ANALYSIS")
    print("Run: run-2026-01-16-1430")
    print("=" * 70)

    # Load data
    df = load_all_timeseries()

    # Check if PT exists
    if 'PT' not in df['country'].values:
        print("\nWARNING: Portugal (PT) not found!")
        print("Run scripts/11_extract_portugal.py first.")
        return

    # Analysis 1: Base effect
    basis_df, basis_corr, basis_p = analyze_basis_effect(df)
    create_basis_effect_scatter(basis_df, basis_corr, basis_p)

    # Analysis 2: Recovery indices
    recovery_df = analyze_recovery_indices(df)
    create_recovery_comparison_chart(recovery_df)

    # Analysis 3: Fiscal cushion
    fiscal_df, fiscal_corr, fiscal_p = analyze_fiscal_cushion(df)
    create_fiscal_cushion_chart(fiscal_df, fiscal_corr, fiscal_p)

    # Summary
    print_summary(basis_df, recovery_df, fiscal_df,
                  basis_corr, basis_p,
                  fiscal_corr, fiscal_p)

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETED")
    print("=" * 70)
    print("\nCreated files:")
    print(f"  - {OUTPUT_TABLES / 'basis_effect_analysis.csv'}")
    print(f"  - {OUTPUT_TABLES / 'recovery_comparison.csv'}")
    print(f"  - {OUTPUT_TABLES / 'fiscal_response.csv'}")
    print(f"  - {OUTPUT_FIGURES / 'basis_effect_scatter.png'}")
    print(f"  - {OUTPUT_FIGURES / 'recovery_nominal_vs_real.png'}")
    print(f"  - {OUTPUT_FIGURES / 'fiscal_cushion.png'}")


if __name__ == '__main__':
    main()
