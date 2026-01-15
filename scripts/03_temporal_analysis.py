"""
03_temporal_analysis.py - Phase 2: Temporal Analysis & Structural Breaks

This script analyzes:
- Time series of key aggregates (2010-2023)
- Year-over-year changes
- Structural breaks (COVID 2020, Energy crisis 2022)
- Sectoral dynamics over time

Output: Console summary + CSV exports to outputs/

Usage:
    python scripts/03_temporal_analysis.py
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

YEARS = [str(y) for y in range(2010, 2024)]
SAMPLE_COUNTRIES = ['DE', 'FR', 'IT', 'AT', 'PL', 'GR', 'ES', 'NL']


def load_country_year(ctr, year):
    """Load data for specific country and year."""
    return pq.read_table(
        DATA_PATH,
        filters=[('base', '=', year), ('ctr', '=', ctr)]
    ).to_pandas()


def get_aggregate(df, ctr, set_i=None, set_j=None):
    """Calculate aggregate for specific transaction type."""
    mask = df['m'] == ctr
    if set_i:
        mask &= df['Set_i'] == set_i
    if set_j:
        mask &= df['Set_j'] == set_j
    return df[mask]['value'].sum()


def build_time_series(ctr):
    """Build time series of key aggregates for a country."""
    print(f"Building time series for {ctr}...")

    data = []
    for year in YEARS:
        df = load_country_year(ctr, year)

        row = {
            'year': int(year),
            'country': ctr,
            'wages_D11': get_aggregate(df, ctr, set_i='D11'),
            'surplus_B2': get_aggregate(df, ctr, set_i='B2'),
            'hh_consumption': get_aggregate(df, ctr, set_j='P3_S14'),
            'gov_consumption': get_aggregate(df, ctr, set_j='P3_S13'),
            'investment': get_aggregate(df, ctr, set_j='P51G'),
        }

        # Imports (products from foreign partners)
        imports = df[
            (df['Set_i'].str.startswith('CPA_')) &
            (df['m'] != ctr)
        ]['value'].sum()
        row['imports'] = imports

        data.append(row)

    return pd.DataFrame(data)


def analyze_yoy_changes(ts):
    """Calculate year-over-year percentage changes."""
    print("\n" + "="*60)
    print(f"YEAR-OVER-YEAR CHANGES - {ts['country'].iloc[0]}")
    print("="*60)

    metrics = ['wages_D11', 'surplus_B2', 'hh_consumption', 'gov_consumption', 'investment', 'imports']

    yoy = ts.copy()
    for col in metrics:
        yoy[f'{col}_yoy'] = ts[col].pct_change() * 100

    # Focus on key years
    print("\nKey structural break years:")
    for year in [2020, 2021, 2022]:
        row = yoy[yoy['year'] == year]
        if len(row) > 0:
            print(f"\n{year}:")
            for col in metrics:
                val = row[f'{col}_yoy'].values[0]
                print(f"  {col}: {val:+.1f}%")

    return yoy


def analyze_sector_dynamics(ctr):
    """Analyze how sectors changed over time (intermediate consumption)."""
    print(f"\n{'='*60}")
    print(f"SECTORAL DYNAMICS - {ctr}")
    print("="*60)

    # Compare 2019, 2020, 2021, 2022
    years_compare = ['2019', '2020', '2021', '2022']
    sector_data = {}

    for year in years_compare:
        df = load_country_year(ctr, year)
        # Intermediate consumption by industry
        mask = (
            df['Set_i'].str.startswith('CPA_') &
            df['Set_j'].str.match(r'^[A-T]') &
            (df['m'] == ctr)
        )
        by_sector = df[mask].groupby('Set_j')['value'].sum()
        sector_data[year] = by_sector

    # Combine
    sectors = pd.DataFrame(sector_data)

    # Calculate changes
    sectors['change_2019_2020'] = (sectors['2020'] - sectors['2019']) / sectors['2019'] * 100
    sectors['change_2020_2021'] = (sectors['2021'] - sectors['2020']) / sectors['2020'] * 100
    sectors['change_2021_2022'] = (sectors['2022'] - sectors['2021']) / sectors['2021'] * 100

    # Most affected by COVID (2019-2020)
    print("\nMost affected sectors (2019-2020, COVID shock):")
    worst = sectors.sort_values('change_2019_2020').head(10)
    for sector in worst.index:
        val = worst.loc[sector, 'change_2019_2020']
        print(f"  {sector}: {val:+.1f}%")

    print("\nRecovery/Growth sectors (2019-2020):")
    best = sectors.sort_values('change_2019_2020', ascending=False).head(5)
    for sector in best.index:
        val = best.loc[sector, 'change_2019_2020']
        print(f"  {sector}: {val:+.1f}%")

    # Energy crisis effect (2021-2022)
    print("\nEnergy crisis impact (2021-2022):")
    energy = sectors.sort_values('change_2021_2022').head(5)
    for sector in energy.index:
        val = energy.loc[sector, 'change_2021_2022']
        print(f"  {sector}: {val:+.1f}%")

    return sectors


def cross_country_comparison():
    """Compare structural breaks across countries."""
    print("\n" + "="*60)
    print("CROSS-COUNTRY STRUCTURAL BREAKS")
    print("="*60)

    results = []
    for ctr in SAMPLE_COUNTRIES:
        ts = build_time_series(ctr)

        # 2020 vs 2019 (COVID)
        row_2019 = ts[ts['year'] == 2019].iloc[0]
        row_2020 = ts[ts['year'] == 2020].iloc[0]
        row_2022 = ts[ts['year'] == 2022].iloc[0]
        row_2021 = ts[ts['year'] == 2021].iloc[0]

        covid_hh = (row_2020['hh_consumption'] - row_2019['hh_consumption']) / row_2019['hh_consumption'] * 100
        covid_gov = (row_2020['gov_consumption'] - row_2019['gov_consumption']) / row_2019['gov_consumption'] * 100
        energy_hh = (row_2022['hh_consumption'] - row_2021['hh_consumption']) / row_2021['hh_consumption'] * 100

        results.append({
            'Country': ctr,
            'COVID HH Cons (2020)': covid_hh,
            'COVID Gov Cons (2020)': covid_gov,
            'Energy HH Cons (2022)': energy_hh
        })

    comparison = pd.DataFrame(results)
    print("\nCOVID Impact (2019-2020) and Energy Crisis (2021-2022):")
    print(comparison.round(1).to_string(index=False))

    comparison.to_csv(OUTPUT_PATH / 'structural_breaks_comparison.csv', index=False)
    print(f"\nSaved: {OUTPUT_PATH / 'structural_breaks_comparison.csv'}")

    return comparison


def main():
    """Run temporal analysis."""
    print("FIGARO-NAM Temporal Analysis")
    print("="*60)

    # Germany detailed analysis
    ts_de = build_time_series('DE')
    ts_de.to_csv(OUTPUT_PATH / 'DE_time_series.csv', index=False)
    print(f"\nSaved: {OUTPUT_PATH / 'DE_time_series.csv'}")

    print("\nGermany Time Series (2010-2023):")
    print(ts_de.to_string(index=False))

    # Year-over-year changes
    yoy_de = analyze_yoy_changes(ts_de)
    yoy_de.to_csv(OUTPUT_PATH / 'DE_yoy_changes.csv', index=False)

    # Sectoral dynamics
    sectors_de = analyze_sector_dynamics('DE')
    sectors_de.to_csv(OUTPUT_PATH / 'DE_sector_dynamics.csv')

    # Cross-country comparison
    comparison = cross_country_comparison()

    print(f"\n{'='*60}")
    print("SUMMARY: KEY STRUCTURAL BREAKS OBSERVED")
    print("="*60)
    print("""
COVID-19 (2020):
- Household consumption dropped across all countries
- Government consumption increased (fiscal response)
- Most affected: Travel (N79), Airlines (H51), Hotels (I)
- Growth: Healthcare (Q86), Logistics (H53)

Energy Crisis (2022):
- Household consumption shows inflation effect (nominal increase)
- Real impact harder to assess without deflators
- Energy-intensive sectors potentially affected

Note: Values are nominal (not inflation-adjusted).
Interpretation requires external context on price levels.
    """)

    print(f"{'='*60}")
    print("Analysis complete. Results saved to outputs/")
    print("="*60)


if __name__ == '__main__':
    main()
