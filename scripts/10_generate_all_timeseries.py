"""
10_generate_all_timeseries.py - Generate time series for all 8 focus countries

Reads Parquet data directly and generates time series CSVs for:
DE, FR, IT, ES, AT, PL, GR, NL

Output: outputs/tables/{CTR}_time_series.csv

Usage:
    python scripts/10_generate_all_timeseries.py
"""

import pyarrow.parquet as pq
import pandas as pd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuration
DATA_PATH = Path('data/parquet/')
OUTPUT_PATH = Path('outputs/tables/')
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

YEARS = list(range(2010, 2024))
FOCUS_COUNTRIES = ['DE', 'FR', 'IT', 'ES', 'AT', 'PL', 'GR', 'NL']


def load_country_year(ctr, year):
    """Load data for specific country and year."""
    return pq.read_table(
        DATA_PATH,
        filters=[('base', '=', int(year)), ('ctr', '=', ctr)]
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
    print(f"  Processing {ctr}...", end=" ", flush=True)

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

    result = pd.DataFrame(data)
    print(f"done ({len(result)} years)")
    return result


def main():
    print("=" * 60)
    print("GENERATING TIME SERIES FOR ALL FOCUS COUNTRIES")
    print("=" * 60)
    print(f"\nCountries: {', '.join(FOCUS_COUNTRIES)}")
    print(f"Years: {YEARS[0]}-{YEARS[-1]} ({len(YEARS)} years)")
    print(f"Output: {OUTPUT_PATH}/\n")

    all_data = []

    for ctr in FOCUS_COUNTRIES:
        ts = build_time_series(ctr)

        # Save individual country file
        output_file = OUTPUT_PATH / f'{ctr}_time_series.csv'
        ts.to_csv(output_file, index=False)
        print(f"    Saved: {output_file}")

        all_data.append(ts)

    # Also create a combined file
    combined = pd.concat(all_data, ignore_index=True)
    combined_file = OUTPUT_PATH / 'all_countries_time_series.csv'
    combined.to_csv(combined_file, index=False)
    print(f"\n  Combined file: {combined_file}")

    # Summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    # Show 2019 vs 2020 comparison (COVID)
    print("\nHH Consumption Change 2019-2020 (COVID):")
    for ctr in FOCUS_COUNTRIES:
        ctr_data = combined[combined['country'] == ctr]
        val_2019 = ctr_data[ctr_data['year'] == 2019]['hh_consumption'].values[0]
        val_2020 = ctr_data[ctr_data['year'] == 2020]['hh_consumption'].values[0]
        change = (val_2020 - val_2019) / val_2019 * 100
        print(f"  {ctr}: {change:+.1f}%")

    # Show 2021 vs 2022 comparison (Energy)
    print("\nHH Consumption Change 2021-2022 (Energy Crisis):")
    for ctr in FOCUS_COUNTRIES:
        ctr_data = combined[combined['country'] == ctr]
        val_2021 = ctr_data[ctr_data['year'] == 2021]['hh_consumption'].values[0]
        val_2022 = ctr_data[ctr_data['year'] == 2022]['hh_consumption'].values[0]
        change = (val_2022 - val_2021) / val_2021 * 100
        print(f"  {ctr}: {change:+.1f}%")

    print("\n" + "=" * 60)
    print("TIME SERIES GENERATION COMPLETE")
    print(f"Files created: {len(FOCUS_COUNTRIES) + 1}")
    print("=" * 60)


if __name__ == '__main__':
    main()
