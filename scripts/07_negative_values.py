"""
07_negative_values.py - Phase 2b: Negative Values Analysis

This script categorizes and analyzes the ~204k negative values in the dataset:
1. Distribution by Set_i/Set_j categories
2. Temporal development
3. Country differences

Output: CSV tables to outputs/tables/

Usage:
    python scripts/07_negative_values.py
"""

import pandas as pd
import numpy as np
import pyarrow.parquet as pq
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuration
DATA_PATH = Path('data/parquet/')
OUTPUT_PATH = Path('outputs/')
TABLES_PATH = OUTPUT_PATH / 'tables'
TABLES_PATH.mkdir(exist_ok=True)

# Sample countries
SAMPLE_COUNTRIES = ['DE', 'FR', 'IT', 'ES', 'NL', 'PL', 'AT', 'GR']

# Category mappings for Set_i codes
SET_I_CATEGORIES = {
    'CPA_Products': lambda x: x.startswith('CPA_'),
    'D_Transactions': lambda x: x.startswith('D'),
    'B_Balances': lambda x: x.startswith('B'),
    'P_Uses': lambda x: x.startswith('P'),
    'Other': lambda x: True  # Catch-all
}

# Category mappings for Set_j codes
SET_J_CATEGORIES = {
    'Industries': lambda x: len(x) <= 4 and not x.startswith(('P', 'D', 'B', 'S', 'F', 'N')),
    'Final_Demand': lambda x: x.startswith('P'),
    'Sectors': lambda x: x.startswith('S'),
    'Other': lambda x: True
}


def categorize_code(code: str, category_map: dict) -> str:
    """Categorize a code based on mapping rules."""
    for category, rule in category_map.items():
        if rule(str(code)):
            return category
    return 'Other'


def load_all_data():
    """Load all parquet files and filter for negative values."""
    print("Loading all data and filtering negative values...")

    all_negatives = []

    years = range(2010, 2024)
    total_files = len(SAMPLE_COUNTRIES) * len(list(years))
    processed = 0

    for year in range(2010, 2024):
        for country in SAMPLE_COUNTRIES:
            file_path = DATA_PATH / f'base={year}' / f'ctr={country}' / 'part-0.parquet'
            if file_path.exists():
                df = pq.read_table(file_path).to_pandas()
                negatives = df[df['value'] < 0].copy()
                negatives['year'] = year
                negatives['country'] = country
                all_negatives.append(negatives)

            processed += 1
            if processed % 20 == 0:
                print(f"  Processed {processed}/{total_files} files...")

    if all_negatives:
        return pd.concat(all_negatives, ignore_index=True)
    return pd.DataFrame()


def analyze_by_category(df: pd.DataFrame):
    """Analyze negative values by Set_i and Set_j categories."""
    print("\nAnalyzing by category...")

    # Categorize codes
    df['Set_i_category'] = df['Set_i'].apply(lambda x: categorize_code(x, SET_I_CATEGORIES))
    df['Set_j_category'] = df['Set_j'].apply(lambda x: categorize_code(x, SET_J_CATEGORIES))

    # Summary by Set_i category
    set_i_summary = df.groupby('Set_i_category').agg(
        count=('value', 'count'),
        total_value=('value', 'sum'),
        mean_value=('value', 'mean'),
        min_value=('value', 'min'),
        max_value=('value', 'max')
    ).round(2)

    # Summary by Set_j category
    set_j_summary = df.groupby('Set_j_category').agg(
        count=('value', 'count'),
        total_value=('value', 'sum'),
        mean_value=('value', 'mean'),
        min_value=('value', 'min'),
        max_value=('value', 'max')
    ).round(2)

    # Cross-tabulation
    cross_tab = pd.crosstab(
        df['Set_i_category'],
        df['Set_j_category'],
        values=df['value'],
        aggfunc='count',
        margins=True
    )

    return set_i_summary, set_j_summary, cross_tab


def analyze_by_year(df: pd.DataFrame):
    """Analyze negative values by year."""
    print("Analyzing by year...")

    year_summary = df.groupby('year').agg(
        count=('value', 'count'),
        total_value=('value', 'sum'),
        mean_value=('value', 'mean'),
        countries_affected=('country', 'nunique')
    ).round(2)

    return year_summary


def analyze_by_country(df: pd.DataFrame):
    """Analyze negative values by country."""
    print("Analyzing by country...")

    country_summary = df.groupby('country').agg(
        count=('value', 'count'),
        total_value=('value', 'sum'),
        mean_value=('value', 'mean'),
        years_affected=('year', 'nunique')
    ).round(2)

    return country_summary


def analyze_specific_codes(df: pd.DataFrame):
    """Identify most frequent negative value codes."""
    print("Analyzing specific codes...")

    # Top Set_i codes with negative values
    top_set_i = df.groupby('Set_i').agg(
        count=('value', 'count'),
        total_value=('value', 'sum')
    ).sort_values('count', ascending=False).head(20)

    # Top Set_j codes with negative values
    top_set_j = df.groupby('Set_j').agg(
        count=('value', 'count'),
        total_value=('value', 'sum')
    ).sort_values('count', ascending=False).head(20)

    # Top combinations
    top_combinations = df.groupby(['Set_i', 'Set_j']).agg(
        count=('value', 'count'),
        total_value=('value', 'sum')
    ).sort_values('count', ascending=False).head(30)

    return top_set_i, top_set_j, top_combinations


def main():
    """Run negative values analysis."""
    print("FIGARO-NAM Negative Values Analysis")
    print("=" * 60)

    # Load data
    df = load_all_data()

    if df.empty:
        print("No data loaded!")
        return

    print(f"\nTotal negative values found: {len(df):,}")
    print(f"Total negative sum: {df['value'].sum():,.0f}")

    # Analyze by category
    set_i_summary, set_j_summary, cross_tab = analyze_by_category(df)

    # Analyze by year
    year_summary = analyze_by_year(df)

    # Analyze by country
    country_summary = analyze_by_country(df)

    # Analyze specific codes
    top_set_i, top_set_j, top_combinations = analyze_specific_codes(df)

    # Save all tables
    print("\nSaving tables...")

    set_i_summary.to_csv(TABLES_PATH / 'negative_values_by_set_i.csv')
    print(f"  Saved: {TABLES_PATH / 'negative_values_by_set_i.csv'}")

    set_j_summary.to_csv(TABLES_PATH / 'negative_values_by_set_j.csv')
    print(f"  Saved: {TABLES_PATH / 'negative_values_by_set_j.csv'}")

    cross_tab.to_csv(TABLES_PATH / 'negative_values_crosstab.csv')
    print(f"  Saved: {TABLES_PATH / 'negative_values_crosstab.csv'}")

    year_summary.to_csv(TABLES_PATH / 'negative_values_by_year.csv')
    print(f"  Saved: {TABLES_PATH / 'negative_values_by_year.csv'}")

    country_summary.to_csv(TABLES_PATH / 'negative_values_by_country.csv')
    print(f"  Saved: {TABLES_PATH / 'negative_values_by_country.csv'}")

    top_set_i.to_csv(TABLES_PATH / 'negative_values_top_set_i.csv')
    print(f"  Saved: {TABLES_PATH / 'negative_values_top_set_i.csv'}")

    top_set_j.to_csv(TABLES_PATH / 'negative_values_top_set_j.csv')
    print(f"  Saved: {TABLES_PATH / 'negative_values_top_set_j.csv'}")

    top_combinations.to_csv(TABLES_PATH / 'negative_values_top_combinations.csv')
    print(f"  Saved: {TABLES_PATH / 'negative_values_top_combinations.csv'}")

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY: Negative Values Distribution")
    print("=" * 60)

    print("\nBy Set_i Category:")
    print(set_i_summary.to_string())

    print("\n\nBy Set_j Category:")
    print(set_j_summary.to_string())

    print("\n\nBy Year (sample):")
    print(year_summary.to_string())

    print("\n\nBy Country:")
    print(country_summary.to_string())

    print("\n" + "=" * 60)
    print("Interpretation:")
    print("=" * 60)
    print("""
Negative values in FIGARO-NAM typically represent:
1. D29X39: Taxes minus subsidies (negative when subsidies > taxes)
2. Statistical adjustments and balancing items
3. Inventory changes (can be negative)
4. NPISH consumption adjustments

These are NOT errors but legitimate accounting entries in the
National Accounts framework (ESA 2010).
""")


if __name__ == '__main__':
    main()
