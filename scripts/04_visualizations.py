"""
04_visualizations.py - Phase 2: Exploration Visualizations

This script generates key visualizations for the structural breaks analysis:
1. Heatmap: COVID impact across countries and aggregates
2. Diverging bar chart: Sectoral winners and losers
3. Time series: Household consumption trends with crisis markers

Output: PNG images to outputs/figures/

Usage:
    python scripts/04_visualizations.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuration
OUTPUT_PATH = Path('outputs/')
FIGURES_PATH = OUTPUT_PATH / 'figures'
TABLES_PATH = OUTPUT_PATH / 'tables'
FIGURES_PATH.mkdir(exist_ok=True)

# Style settings
plt.style.use('seaborn-v0_8-whitegrid')
COLORS = {
    'negative': '#d62728',
    'positive': '#2ca02c',
    'neutral': '#7f7f7f',
    'primary': '#1f77b4'
}

# Data disclaimer
NOMINAL_DISCLAIMER = "Source: FIGARO-NAM (Eurostat). All values nominal, not inflation-adjusted."


def plot_covid_heatmap():
    """Create heatmap of COVID structural breaks across countries."""
    print("Creating COVID impact heatmap...")

    # Load structural breaks data
    breaks = pd.read_csv(TABLES_PATH / 'structural_breaks_comparison.csv')

    # Prepare data for heatmap
    heatmap_data = breaks.set_index('Country')[
        ['COVID HH Cons (2020)', 'COVID Gov Cons (2020)', 'Energy HH Cons (2022)']
    ]
    heatmap_data.columns = ['HH Consumption\n(COVID 2020)', 'Gov Consumption\n(COVID 2020)', 'HH Consumption\n(Energy 2022)']

    # Sort by COVID HH impact
    heatmap_data = heatmap_data.sort_values('HH Consumption\n(COVID 2020)')

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Custom colormap: red for negative, white for zero, green for positive
    cmap = sns.diverging_palette(10, 133, as_cmap=True)

    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt='.1f',
        cmap=cmap,
        center=0,
        linewidths=0.5,
        cbar_kws={'label': 'Year-over-Year Change (%)'},
        ax=ax
    )

    ax.set_title('Structural Breaks: COVID-19 (2020) and Energy Crisis (2022)\nYear-over-Year Changes in Key Aggregates',
                 fontsize=12, fontweight='bold', pad=20)
    ax.set_xlabel('')
    ax.set_ylabel('Country')

    # Add disclaimer
    fig.text(0.5, 0.02, NOMINAL_DISCLAIMER, ha='center', fontsize=8, style='italic', color='gray')

    plt.tight_layout(rect=[0, 0.05, 1, 1])
    fig.savefig(FIGURES_PATH / 'heatmap_structural_breaks.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {FIGURES_PATH / 'heatmap_structural_breaks.png'}")


def plot_sector_diverging():
    """Create diverging bar chart for sectoral winners/losers."""
    print("Creating sectoral impact chart...")

    # Load sector dynamics
    sectors = pd.read_csv(TABLES_PATH / 'DE_sector_dynamics.csv', index_col=0)

    # Get top losers and winners
    change_col = 'change_2019_2020'
    sorted_sectors = sectors[change_col].sort_values()

    # Select top 8 losers and top 5 winners
    losers = sorted_sectors.head(8)
    winners = sorted_sectors.tail(5)
    selected = pd.concat([losers, winners])

    # Sector labels with NACE codes for reproducibility
    sector_labels = {
        'N79': 'N79 - Travel agencies',
        'H51': 'H51 - Air transport',
        'A03': 'A03 - Fishing',
        'I': 'I - Accommodation & food',
        'N78': 'N78 - Employment activities',
        'R93': 'R93 - Sports & recreation',
        'S96': 'S96 - Other personal services',
        'R90-R92': 'R90-92 - Arts & entertainment',
        'Q86': 'Q86 - Healthcare',
        'K66': 'K66 - Financial aux. services',
        'O84': 'O84 - Public administration',
        'H53': 'H53 - Postal services',
        'H50': 'H50 - Water transport',
        'C24': 'C24 - Basic metals',
        'C29': 'C29 - Motor vehicles'
    }

    # Create labels with NACE codes
    labels = [sector_labels.get(s, s) for s in selected.index]
    values = selected.values
    colors = [COLORS['negative'] if v < 0 else COLORS['positive'] for v in values]

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))

    y_pos = np.arange(len(labels))
    bars = ax.barh(y_pos, values, color=colors, edgecolor='white', linewidth=0.5)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel('Year-over-Year Change (%)')
    ax.set_title('Germany: Sectoral Impact of COVID-19 (2019-2020)\nIntermediate Consumption by Industry',
                 fontsize=12, fontweight='bold', pad=20)

    # Add vertical line at zero
    ax.axvline(x=0, color='black', linewidth=0.8)

    # Add value labels
    for bar, val in zip(bars, values):
        x_pos = val + 1 if val >= 0 else val - 1
        ha = 'left' if val >= 0 else 'right'
        ax.text(x_pos, bar.get_y() + bar.get_height()/2, f'{val:+.1f}%',
                va='center', ha=ha, fontsize=9)

    ax.set_xlim(-70, 35)

    # Add disclaimer
    fig.text(0.5, 0.02, NOMINAL_DISCLAIMER, ha='center', fontsize=8, style='italic', color='gray')

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(FIGURES_PATH / 'diverging_sectors_covid.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {FIGURES_PATH / 'diverging_sectors_covid.png'}")


def plot_time_series():
    """Create time series with structural break markers."""
    print("Creating time series chart...")

    # Load time series
    ts = pd.read_csv(TABLES_PATH / 'DE_time_series.csv')

    # Create figure with two panels
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # Panel 1: Absolute values
    ax1 = axes[0]
    ax1.plot(ts['year'], ts['hh_consumption'] / 1e6, 'o-', color=COLORS['primary'],
             linewidth=2, markersize=6, label='Household consumption')
    ax1.plot(ts['year'], ts['gov_consumption'] / 1e6, 's-', color=COLORS['positive'],
             linewidth=2, markersize=5, label='Government consumption')
    ax1.plot(ts['year'], ts['investment'] / 1e6, '^-', color=COLORS['neutral'],
             linewidth=2, markersize=5, label='Investment')

    # Add crisis markers
    ax1.axvspan(2019.5, 2020.5, alpha=0.2, color='red', label='COVID-19')
    ax1.axvspan(2021.5, 2022.5, alpha=0.2, color='orange', label='Energy crisis')

    ax1.set_ylabel('Trillion EUR')
    ax1.set_title('Germany: Key Aggregates (2010-2023)\nNominal Values',
                  fontsize=12, fontweight='bold', pad=10)
    ax1.legend(loc='upper left', framealpha=0.9)
    ax1.set_ylim(0, 2.5)

    # Panel 2: Year-over-year changes
    ax2 = axes[1]

    # Calculate YoY changes
    ts['hh_yoy'] = ts['hh_consumption'].pct_change() * 100
    ts['gov_yoy'] = ts['gov_consumption'].pct_change() * 100
    ts['inv_yoy'] = ts['investment'].pct_change() * 100

    ax2.bar(ts['year'] - 0.2, ts['hh_yoy'], width=0.2, color=COLORS['primary'], label='HH consumption')
    ax2.bar(ts['year'], ts['gov_yoy'], width=0.2, color=COLORS['positive'], label='Gov consumption')
    ax2.bar(ts['year'] + 0.2, ts['inv_yoy'], width=0.2, color=COLORS['neutral'], label='Investment')

    ax2.axhline(y=0, color='black', linewidth=0.8)
    ax2.axvspan(2019.5, 2020.5, alpha=0.2, color='red')
    ax2.axvspan(2021.5, 2022.5, alpha=0.2, color='orange')

    ax2.set_xlabel('Year')
    ax2.set_ylabel('YoY Change (%)')
    ax2.set_title('Year-over-Year Changes', fontsize=11, fontweight='bold', pad=10)
    ax2.legend(loc='upper left', framealpha=0.9)
    ax2.set_ylim(-15, 20)

    plt.xticks(ts['year'], rotation=45)

    # Add disclaimer
    fig.text(0.5, 0.01, NOMINAL_DISCLAIMER, ha='center', fontsize=8, style='italic', color='gray')

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig(FIGURES_PATH / 'timeseries_germany.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {FIGURES_PATH / 'timeseries_germany.png'}")


def plot_country_comparison():
    """Create country comparison bar chart for COVID impact."""
    print("Creating country comparison chart...")

    # Load data
    breaks = pd.read_csv(TABLES_PATH / 'structural_breaks_comparison.csv')
    breaks = breaks.sort_values('COVID HH Cons (2020)')

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(breaks))
    width = 0.35

    bars1 = ax.bar(x - width/2, breaks['COVID HH Cons (2020)'], width,
                   label='Household Consumption', color=COLORS['primary'])
    bars2 = ax.bar(x + width/2, breaks['COVID Gov Cons (2020)'], width,
                   label='Government Consumption', color=COLORS['positive'])

    ax.axhline(y=0, color='black', linewidth=0.8)
    ax.set_ylabel('Year-over-Year Change (%)')
    ax.set_title('COVID-19 Impact Across Countries (2019-2020)\nHousehold vs Government Consumption Response',
                 fontsize=12, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(breaks['Country'])
    ax.legend()

    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, -12 if height < 0 else 3),
                    textcoords="offset points",
                    ha='center', va='bottom' if height >= 0 else 'top',
                    fontsize=8)

    # Add disclaimer
    fig.text(0.5, 0.02, NOMINAL_DISCLAIMER, ha='center', fontsize=8, style='italic', color='gray')

    plt.tight_layout(rect=[0, 0.05, 1, 1])
    fig.savefig(FIGURES_PATH / 'comparison_covid_countries.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {FIGURES_PATH / 'comparison_covid_countries.png'}")


def main():
    """Generate all visualizations."""
    print("FIGARO-NAM Visualization Pipeline")
    print("=" * 60)

    plot_covid_heatmap()
    plot_sector_diverging()
    plot_time_series()
    plot_country_comparison()

    print("\n" + "=" * 60)
    print("Visualization complete. Figures saved to outputs/figures/")
    print("=" * 60)

    # List generated files
    print("\nGenerated files:")
    for f in sorted(FIGURES_PATH.glob('*.png')):
        print(f"  - {f.name}")


if __name__ == '__main__':
    main()
