"""
06_export_analysis.py - Phase 2b: Export Structure Analysis

This script analyzes export structure as complement to import analysis (Script 02):
1. Top export destinations per country
2. Exported products by category
3. Export/Import balance by partner

Note: In FIGARO, exports from country X to Y appear in Y's data as imports (m=X).
To get exports, we load partner country data and filter for m=FOCUS_COUNTRY.

Output: CSV tables to outputs/tables/

Usage:
    python scripts/06_export_analysis.py
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

# Focus country for detailed analysis
FOCUS_COUNTRY = 'DE'
ANALYSIS_YEAR = 2019  # Pre-COVID baseline

# Partner countries to check for exports
PARTNER_COUNTRIES = [
    'AT', 'BE', 'BG', 'CY', 'CZ', 'DK', 'EE', 'ES', 'FI', 'FR',
    'GR', 'HR', 'HU', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT', 'NL',
    'PL', 'PT', 'RO', 'SE', 'SI', 'SK', 'US', 'CN', 'JP', 'GB', 'CH'
]

# Product category mapping
PRODUCT_CATEGORIES = {
    'Agriculture': ['CPA_A01', 'CPA_A02', 'CPA_A03'],
    'Mining': ['CPA_B'],
    'Food & Beverages': ['CPA_C10-C12'],
    'Textiles': ['CPA_C13-C15'],
    'Chemicals': ['CPA_C20', 'CPA_C21'],
    'Machinery': ['CPA_C28'],
    'Vehicles': ['CPA_C29', 'CPA_C30'],
    'Electronics': ['CPA_C26', 'CPA_C27'],
    'Services': ['CPA_G', 'CPA_H', 'CPA_I', 'CPA_J', 'CPA_K', 'CPA_L', 'CPA_M', 'CPA_N'],
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


def load_exports_from_partners(country: str, year: int) -> pd.DataFrame:
    """Load exports by looking at partner countries' imports from this country.

    In FIGARO, exports from country X to Y appear in country Y's data as imports (m=X).
    """
    print(f"  Loading exports from partner countries...")
    all_exports = []

    for partner in PARTNER_COUNTRIES:
        if partner == country:
            continue

        file_path = DATA_PATH / f'base={year}' / f'ctr={partner}' / 'part-0.parquet'
        if file_path.exists():
            df = pq.read_table(file_path).to_pandas()
            # Filter for imports from our focus country (= our exports to them)
            exports_to_partner = df[df['m'] == country].copy()
            if not exports_to_partner.empty:
                exports_to_partner['destination'] = partner
                all_exports.append(exports_to_partner)

    if all_exports:
        result = pd.concat(all_exports, ignore_index=True)
        print(f"  Found {len(result):,} export flows to {len(all_exports)} partners")
        return result
    return pd.DataFrame()


def analyze_exports_by_partner(exports_df: pd.DataFrame) -> pd.DataFrame:
    """Analyze exports by destination country."""
    if exports_df.empty:
        return pd.DataFrame(columns=['Partner', 'Export_Value', 'Share_%'])

    by_partner = exports_df.groupby('destination')['value'].sum().sort_values(ascending=False)

    total = by_partner.sum()
    result = pd.DataFrame({
        'Partner': by_partner.index,
        'Export_Value': by_partner.values,
        'Share_%': (by_partner.values / total * 100).round(2) if total > 0 else 0
    })

    return result


def analyze_exports_by_product(exports_df: pd.DataFrame) -> pd.DataFrame:
    """Analyze exports by product category."""
    if exports_df.empty:
        return pd.DataFrame(columns=['Product', 'Export_Value', 'Share_%'])

    by_product = exports_df.groupby('Set_i')['value'].sum().sort_values(ascending=False)

    total = by_product.sum()
    result = pd.DataFrame({
        'Product': by_product.index,
        'Export_Value': by_product.values,
        'Share_%': (by_product.values / total * 100).round(2) if total > 0 else 0
    })

    return result


def categorize_product(product_code: str) -> str:
    """Categorize a product code."""
    for category, codes in PRODUCT_CATEGORIES.items():
        for code in codes:
            if str(product_code).startswith(code):
                return category
    if str(product_code).startswith('CPA_C'):
        return 'Manufacturing (Other)'
    elif str(product_code).startswith('CPA_'):
        return 'Other Products'
    return 'Non-Product'


def analyze_exports_by_category(exports_df: pd.DataFrame) -> pd.DataFrame:
    """Analyze exports by product category."""
    if exports_df.empty:
        return pd.DataFrame(columns=['Category', 'Export_Value', 'Share_%'])

    exports_df = exports_df.copy()
    exports_df['Category'] = exports_df['Set_i'].apply(categorize_product)

    by_category = exports_df.groupby('Category')['value'].sum().sort_values(ascending=False)

    total = by_category.sum()
    result = pd.DataFrame({
        'Category': by_category.index,
        'Export_Value': by_category.values,
        'Share_%': (by_category.values / total * 100).round(2) if total > 0 else 0
    })

    return result


def analyze_trade_balance(imports_df: pd.DataFrame, exports_df: pd.DataFrame, country: str) -> pd.DataFrame:
    """Calculate trade balance by partner."""
    # Exports by destination
    if not exports_df.empty:
        exports = exports_df.groupby('destination')['value'].sum()
    else:
        exports = pd.Series(dtype=float)

    # Imports: flows where m != country (partner delivers to us)
    imports = imports_df[imports_df['m'] != country].groupby('m')['value'].sum()

    # Combine - align on common partners
    all_partners = set(exports.index) | set(imports.index)
    balance_data = []
    for partner in all_partners:
        exp_val = exports.get(partner, 0)
        imp_val = imports.get(partner, 0)
        balance_data.append({
            'Partner': partner,
            'Exports': exp_val,
            'Imports': imp_val,
            'Balance': exp_val - imp_val,
            'Total_Trade': exp_val + imp_val
        })

    balance = pd.DataFrame(balance_data)
    balance = balance.set_index('Partner')
    balance = balance.sort_values('Total_Trade', ascending=False)

    return balance


def plot_trade_balance(balance_df: pd.DataFrame, country: str, year: int):
    """Create trade balance visualization."""
    print("\nCreating trade balance chart...")

    if balance_df.empty:
        print("  No data for visualization")
        return

    # Top 15 partners by total trade
    top_partners = balance_df.head(15).copy()

    fig, ax = plt.subplots(figsize=(12, 8))

    x = np.arange(len(top_partners))
    width = 0.35

    bars1 = ax.bar(x - width/2, top_partners['Exports'] / 1e6, width,
                   label='Exports', color='#2ca02c')
    bars2 = ax.bar(x + width/2, top_partners['Imports'] / 1e6, width,
                   label='Imports', color='#d62728')

    # Add balance line
    ax.plot(x, top_partners['Balance'] / 1e6, 'ko-', linewidth=2,
            markersize=6, label='Balance')

    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.set_ylabel('Billion EUR')
    ax.set_title(f'{country}: Trade with Top Partners ({year})\nExports, Imports, and Balance',
                 fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(top_partners.index, rotation=45, ha='right')
    ax.legend()

    # Add disclaimer
    fig.text(0.5, 0.02, NOMINAL_DISCLAIMER, ha='center', fontsize=8, style='italic', color='gray')

    plt.tight_layout(rect=[0, 0.05, 1, 1])
    fig.savefig(FIGURES_PATH / f'{country}_trade_balance.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {FIGURES_PATH / f'{country}_trade_balance.png'}")


def main():
    """Run export analysis."""
    print("FIGARO-NAM Export Analysis")
    print("=" * 60)
    print(f"Focus: {FOCUS_COUNTRY}, Year: {ANALYSIS_YEAR}")

    # Load focus country data (for imports)
    print(f"\nLoading {FOCUS_COUNTRY} data for {ANALYSIS_YEAR}...")
    imports_df = load_country_year(FOCUS_COUNTRY, ANALYSIS_YEAR)

    if imports_df.empty:
        print("No data loaded!")
        return

    print(f"Loaded {len(imports_df):,} rows (imports perspective)")

    # Load exports from partner countries
    print("\nLoading exports (from partner perspectives)...")
    exports_df = load_exports_from_partners(FOCUS_COUNTRY, ANALYSIS_YEAR)

    # Analyze exports by partner
    print("\nAnalyzing exports by partner...")
    exports_by_partner = analyze_exports_by_partner(exports_df)

    # Analyze exports by product
    print("Analyzing exports by product...")
    exports_by_product = analyze_exports_by_product(exports_df)

    # Analyze exports by category
    print("Analyzing exports by category...")
    exports_by_category = analyze_exports_by_category(exports_df)

    # Analyze trade balance
    print("Calculating trade balance...")
    trade_balance = analyze_trade_balance(imports_df, exports_df, FOCUS_COUNTRY)

    # Save tables
    print("\nSaving tables...")

    exports_by_partner.to_csv(TABLES_PATH / f'{FOCUS_COUNTRY}_exports_by_partner.csv', index=False)
    print(f"  Saved: {TABLES_PATH / f'{FOCUS_COUNTRY}_exports_by_partner.csv'}")

    exports_by_product.head(50).to_csv(TABLES_PATH / f'{FOCUS_COUNTRY}_exports_by_product.csv', index=False)
    print(f"  Saved: {TABLES_PATH / f'{FOCUS_COUNTRY}_exports_by_product.csv'}")

    exports_by_category.to_csv(TABLES_PATH / f'{FOCUS_COUNTRY}_exports_by_category.csv', index=False)
    print(f"  Saved: {TABLES_PATH / f'{FOCUS_COUNTRY}_exports_by_category.csv'}")

    trade_balance.to_csv(TABLES_PATH / f'{FOCUS_COUNTRY}_trade_balance.csv')
    print(f"  Saved: {TABLES_PATH / f'{FOCUS_COUNTRY}_trade_balance.csv'}")

    # Create visualization
    plot_trade_balance(trade_balance, FOCUS_COUNTRY, ANALYSIS_YEAR)

    # Print summary
    print("\n" + "=" * 60)
    print(f"SUMMARY: {FOCUS_COUNTRY} Export Structure ({ANALYSIS_YEAR})")
    print("=" * 60)

    print("\nTop 10 Export Destinations:")
    if not exports_by_partner.empty:
        print(exports_by_partner.head(10).to_string(index=False))
    else:
        print("  No export data found")

    print("\n\nExports by Product Category:")
    if not exports_by_category.empty:
        print(exports_by_category.to_string(index=False))
    else:
        print("  No export data found")

    print("\n\nTrade Balance (Top 10 Partners):")
    if not trade_balance.empty:
        balance_summary = trade_balance.head(10)[['Exports', 'Imports', 'Balance']].copy()
        balance_summary = balance_summary / 1e6  # Convert to billions
        balance_summary.columns = ['Exports (Bn)', 'Imports (Bn)', 'Balance (Bn)']
        print(balance_summary.round(1).to_string())

    # Key insights
    print("\n" + "=" * 60)
    print("Key Findings:")
    print("=" * 60)

    if not exports_by_partner.empty:
        total_exports = exports_by_partner['Export_Value'].sum()
        print(f"\nTotal exports (to tracked partners): {total_exports/1e6:.1f} billion EUR")

        # Top surplus partners
        surplus_partners = trade_balance[trade_balance['Balance'] > 0].head(5)
        if not surplus_partners.empty:
            print(f"\nTop trade surplus partners:")
            for partner in surplus_partners.index:
                surplus = surplus_partners.loc[partner, 'Balance'] / 1e6
                print(f"  {partner}: +{surplus:.1f} Bn EUR")

        # Top deficit partners
        deficit_partners = trade_balance[trade_balance['Balance'] < 0].sort_values('Balance').head(5)
        if not deficit_partners.empty:
            print(f"\nTop trade deficit partners:")
            for partner in deficit_partners.index:
                deficit = deficit_partners.loc[partner, 'Balance'] / 1e6
                print(f"  {partner}: {deficit:.1f} Bn EUR")
    else:
        print("\nNo bilateral export data found in partner countries.")


if __name__ == '__main__':
    main()
