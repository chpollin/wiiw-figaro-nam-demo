"""
02_top_flows.py - Phase 2: Top Flows Analysis

This script identifies:
- Largest flows by absolute value
- Dominant sectors (by value added, output)
- Top trading partners per country
- Key bilateral relationships

Output: Console summary + CSV exports to outputs/

Usage:
    python scripts/02_top_flows.py
"""

import pyarrow.parquet as pq
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuration
DATA_PATH = Path('data/parquet/')
OUTPUT_PATH = Path('outputs/')
OUTPUT_PATH.mkdir(exist_ok=True)

# Sample countries for detailed analysis
SAMPLE_COUNTRIES = ['DE', 'FR', 'IT', 'AT', 'PL', 'GR']
SAMPLE_YEAR = 2020


def load_country_year(ctr, year):
    """Load data for specific country and year."""
    return pq.read_table(
        DATA_PATH,
        filters=[('base', '=', int(year)), ('ctr', '=', ctr)]
    ).to_pandas()


def analyze_top_flows(df, ctr, n=20):
    """Find largest flows by absolute value."""
    print(f"\n{'='*60}")
    print(f"TOP {n} FLOWS - {ctr}")
    print("="*60)

    # Sort by absolute value
    df_sorted = df.reindex(df['value'].abs().sort_values(ascending=False).index)
    top = df_sorted.head(n)[['Set_i', 'm', 'Set_j', 'value']]

    print(top.to_string(index=False))
    return top


def analyze_value_added(df, ctr):
    """Analyze value added by industry (D11 = wages, B2 = operating surplus)."""
    print(f"\n{'='*60}")
    print(f"VALUE ADDED BY INDUSTRY - {ctr}")
    print("="*60)

    # Wages (D11) by industry - domestic only
    wages = df[(df['Set_i'] == 'D11') & (df['m'] == ctr)].copy()
    wages = wages.groupby('Set_j')['value'].sum().sort_values(ascending=False)

    print("\nTop 10 industries by wages (D11):")
    for industry, val in wages.head(10).items():
        print(f"  {industry}: {val:,.0f}")

    # Operating surplus (B2) by industry
    surplus = df[(df['Set_i'] == 'B2') & (df['m'] == ctr)].copy()
    surplus = surplus.groupby('Set_j')['value'].sum().sort_values(ascending=False)

    print("\nTop 10 industries by operating surplus (B2):")
    for industry, val in surplus.head(10).items():
        print(f"  {industry}: {val:,.0f}")

    return wages, surplus


def analyze_intermediate_consumption(df, ctr):
    """Analyze intermediate consumption (products used by industries)."""
    print(f"\n{'='*60}")
    print(f"INTERMEDIATE CONSUMPTION - {ctr}")
    print("="*60)

    # Filter: CPA products -> NACE industries, domestic
    mask = (
        df['Set_i'].str.startswith('CPA_') &
        df['Set_j'].str.match(r'^[A-T]') &
        (df['m'] == ctr)
    )
    intermediates = df[mask].copy()

    # By consuming industry
    by_industry = intermediates.groupby('Set_j')['value'].sum().sort_values(ascending=False)
    print("\nTop 10 industries by intermediate consumption:")
    for industry, val in by_industry.head(10).items():
        print(f"  {industry}: {val:,.0f}")

    # By product consumed
    by_product = intermediates.groupby('Set_i')['value'].sum().sort_values(ascending=False)
    print("\nTop 10 products consumed as intermediates:")
    for product, val in by_product.head(10).items():
        print(f"  {product}: {val:,.0f}")

    return by_industry, by_product


def analyze_final_demand(df, ctr):
    """Analyze final demand (consumption, investment)."""
    print(f"\n{'='*60}")
    print(f"FINAL DEMAND - {ctr}")
    print("="*60)

    # Household consumption (P3_S14)
    hh_cons = df[(df['Set_j'] == 'P3_S14') & (df['m'] == ctr)]
    hh_by_product = hh_cons.groupby('Set_i')['value'].sum().sort_values(ascending=False)

    print("\nTop 10 products in household consumption (P3_S14):")
    for product, val in hh_by_product.head(10).items():
        print(f"  {product}: {val:,.0f}")

    # Government consumption (P3_S13)
    gov_cons = df[(df['Set_j'] == 'P3_S13') & (df['m'] == ctr)]
    gov_by_product = gov_cons.groupby('Set_i')['value'].sum().sort_values(ascending=False)

    print("\nTop 10 products in government consumption (P3_S13):")
    for product, val in gov_by_product.head(10).items():
        print(f"  {product}: {val:,.0f}")

    # Investment (P51G)
    investment = df[(df['Set_j'] == 'P51G') & (df['m'] == ctr)]
    inv_by_product = investment.groupby('Set_i')['value'].sum().sort_values(ascending=False)

    print("\nTop 10 products in investment (P51G):")
    for product, val in inv_by_product.head(10).items():
        print(f"  {product}: {val:,.0f}")

    return hh_by_product, gov_by_product, inv_by_product


def analyze_trade_partners(df, ctr):
    """Analyze trading partners (imports by origin)."""
    print(f"\n{'='*60}")
    print(f"TRADING PARTNERS - {ctr}")
    print("="*60)

    # Imports = flows from other countries (m != ctr)
    imports = df[(df['Set_i'].str.startswith('CPA_')) & (df['m'] != ctr)]
    by_partner = imports.groupby('m')['value'].sum().sort_values(ascending=False)

    print("\nTop 15 import origins:")
    for partner, val in by_partner.head(15).items():
        print(f"  {partner}: {val:,.0f}")

    # Imports by product category
    by_product = imports.groupby('Set_i')['value'].sum().sort_values(ascending=False)
    print("\nTop 10 imported product categories:")
    for product, val in by_product.head(10).items():
        print(f"  {product}: {val:,.0f}")

    return by_partner, by_product


def create_summary_table(year):
    """Create summary table across all sample countries."""
    print(f"\n{'='*60}")
    print(f"CROSS-COUNTRY SUMMARY - {year}")
    print("="*60)

    results = []
    for ctr in SAMPLE_COUNTRIES:
        df = load_country_year(ctr, year)
        domestic = df[df['m'] == ctr]

        # Key aggregates
        wages = df[(df['Set_i'] == 'D11') & (df['m'] == ctr)]['value'].sum()
        surplus = df[(df['Set_i'] == 'B2') & (df['m'] == ctr)]['value'].sum()
        hh_cons = df[(df['Set_j'] == 'P3_S14') & (df['m'] == ctr)]['value'].sum()
        gov_cons = df[(df['Set_j'] == 'P3_S13') & (df['m'] == ctr)]['value'].sum()
        investment = df[(df['Set_j'] == 'P51G') & (df['m'] == ctr)]['value'].sum()
        imports = df[(df['Set_i'].str.startswith('CPA_')) & (df['m'] != ctr)]['value'].sum()

        results.append({
            'Country': ctr,
            'Wages (D11)': wages,
            'Op. Surplus (B2)': surplus,
            'HH Consumption': hh_cons,
            'Gov Consumption': gov_cons,
            'Investment': investment,
            'Imports': imports
        })

    summary = pd.DataFrame(results)
    print(summary.to_string(index=False))

    # Save
    summary.to_csv(OUTPUT_PATH / 'country_summary.csv', index=False)
    print(f"\nSaved: {OUTPUT_PATH / 'country_summary.csv'}")

    return summary


def main():
    """Run top flows analysis."""
    print("FIGARO-NAM Top Flows Analysis")
    print("="*60)

    # Detailed analysis for Germany
    df_de = load_country_year('DE', SAMPLE_YEAR)
    print(f"\nLoaded Germany {SAMPLE_YEAR}: {len(df_de):,} rows")

    analyze_top_flows(df_de, 'DE')
    wages, surplus = analyze_value_added(df_de, 'DE')
    by_industry, by_product = analyze_intermediate_consumption(df_de, 'DE')
    hh, gov, inv = analyze_final_demand(df_de, 'DE')
    partners, imports = analyze_trade_partners(df_de, 'DE')

    # Cross-country summary
    summary = create_summary_table(SAMPLE_YEAR)

    # Save detailed results
    results = {
        'wages_by_industry': wages,
        'surplus_by_industry': surplus,
        'intermediates_by_industry': by_industry,
        'intermediates_by_product': by_product,
        'hh_consumption_by_product': hh,
        'imports_by_partner': partners,
        'imports_by_product': imports
    }

    for name, data in results.items():
        data.to_csv(OUTPUT_PATH / f'DE_{name}.csv')

    print(f"\n{'='*60}")
    print("Analysis complete. Results saved to outputs/")
    print("="*60)


if __name__ == '__main__':
    main()
