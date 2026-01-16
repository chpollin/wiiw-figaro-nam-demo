"""
11_extract_portugal.py - Extract Portugal time series data

Reads Parquet data for Portugal (PT) and generates time series CSV
matching the format of other country files.

Output: outputs/tables/PT_time_series.csv

Usage:
    python scripts/11_extract_portugal.py
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
COUNTRY = 'PT'


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
    print(f"Processing {ctr}...", flush=True)

    data = []
    for year in YEARS:
        print(f"  Year {year}...", end=" ", flush=True)
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
        print("done", flush=True)

    return pd.DataFrame(data)


def main():
    print("=" * 60)
    print("EXTRACTING PORTUGAL TIME SERIES")
    print("=" * 60)
    print(f"\nCountry: {COUNTRY}")
    print(f"Years: {YEARS[0]}-{YEARS[-1]} ({len(YEARS)} years)")
    print(f"Output: {OUTPUT_PATH}/\n")

    # Build time series
    ts = build_time_series(COUNTRY)

    # Save to CSV
    output_file = OUTPUT_PATH / f'{COUNTRY}_time_series.csv'
    ts.to_csv(output_file, index=False)
    print(f"\nSaved: {output_file}")

    # Show summary
    print("\n" + "=" * 60)
    print("SUMMARY: Portugal Key Indicators")
    print("=" * 60)

    print("\nHH Consumption (Mrd EUR):")
    for _, row in ts.iterrows():
        print(f"  {int(row['year'])}: {row['hh_consumption']/1000:.1f}")

    print("\nGov Consumption (Mrd EUR):")
    for _, row in ts.iterrows():
        print(f"  {int(row['year'])}: {row['gov_consumption']/1000:.1f}")

    # COVID impact
    val_2019 = ts[ts['year'] == 2019]['hh_consumption'].values[0]
    val_2020 = ts[ts['year'] == 2020]['hh_consumption'].values[0]
    val_2022 = ts[ts['year'] == 2022]['hh_consumption'].values[0]

    covid_drop = (val_2020 - val_2019) / val_2019 * 100
    recovery = (val_2022 - val_2020) / val_2020 * 100

    print(f"\nCOVID-Einbruch 2019-2020: {covid_drop:+.1f}%")
    print(f"Erholung 2020-2022: {recovery:+.1f}%")

    print("\n" + "=" * 60)
    print("PORTUGAL EXTRACTION COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()
