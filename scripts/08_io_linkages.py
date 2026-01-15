"""
08_io_linkages.py - Phase 2b: Input-Output Linkages Analysis

This script analyzes intersectoral linkages in the economy:
1. Main supplier and buyer sectors
2. Backward and forward linkages
3. Top intersectoral flows

Output: CSV tables and heatmap to outputs/

Usage:
    python scripts/08_io_linkages.py
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

# Focus country and year
FOCUS_COUNTRY = 'DE'
ANALYSIS_YEAR = 2019

# NACE industry codes (simplified for display)
INDUSTRY_LABELS = {
    'A01': 'Agriculture',
    'A02': 'Forestry',
    'A03': 'Fishing',
    'B': 'Mining',
    'C10-C12': 'Food products',
    'C13-C15': 'Textiles',
    'C16': 'Wood products',
    'C17': 'Paper',
    'C18': 'Printing',
    'C19': 'Coke & petroleum',
    'C20': 'Chemicals',
    'C21': 'Pharmaceuticals',
    'C22': 'Rubber & plastic',
    'C23': 'Non-metallic minerals',
    'C24': 'Basic metals',
    'C25': 'Metal products',
    'C26': 'Electronics',
    'C27': 'Electrical equip.',
    'C28': 'Machinery',
    'C29': 'Motor vehicles',
    'C30': 'Other transport',
    'C31_C32': 'Furniture',
    'C33': 'Repair & installation',
    'D35': 'Electricity & gas',
    'E36': 'Water supply',
    'E37-E39': 'Waste management',
    'F': 'Construction',
    'G45': 'Motor vehicle trade',
    'G46': 'Wholesale trade',
    'G47': 'Retail trade',
    'H49': 'Land transport',
    'H50': 'Water transport',
    'H51': 'Air transport',
    'H52': 'Warehousing',
    'H53': 'Postal services',
    'I': 'Accommodation & food',
    'J58': 'Publishing',
    'J59_J60': 'Film & broadcasting',
    'J61': 'Telecommunications',
    'J62_J63': 'IT services',
    'K64': 'Financial services',
    'K65': 'Insurance',
    'K66': 'Financial auxiliaries',
    'L68': 'Real estate',
    'M69_M70': 'Legal & accounting',
    'M71': 'Architecture & engineering',
    'M72': 'R&D',
    'M73': 'Advertising',
    'M74_M75': 'Other professional',
    'N77': 'Rental & leasing',
    'N78': 'Employment activities',
    'N79': 'Travel agencies',
    'N80-N82': 'Security & admin',
    'O84': 'Public administration',
    'P85': 'Education',
    'Q86': 'Healthcare',
    'Q87_Q88': 'Social work',
    'R90-R92': 'Arts & entertainment',
    'R93': 'Sports & recreation',
    'S94': 'Membership orgs',
    'S95': 'Repair of goods',
    'S96': 'Other personal services',
    'T': 'Household services',
    'U': 'Extraterritorial'
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


def is_industry_code(code: str) -> bool:
    """Check if a code is an industry code (not a transaction code)."""
    if pd.isna(code):
        return False
    code = str(code)
    # Industry codes are typically short alphanumeric
    # Exclude transaction codes (D, B, P, S, F, N prefixes for non-industries)
    if code.startswith(('D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9',
                        'B1', 'B2', 'B3', 'B8', 'B9',
                        'P1', 'P2', 'P3', 'P5', 'P6',
                        'S1', 'S2', 'CPA_')):
        return False
    # Check for valid industry patterns
    return len(code) <= 10 and any(c.isalpha() for c in code)


def is_product_code(code: str) -> bool:
    """Check if a code is a CPA product code."""
    return str(code).startswith('CPA_')


def extract_io_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Extract intermediate consumption matrix (products x industries)."""
    # Filter for CPA products (rows) going to industries (columns)
    # This represents intermediate consumption

    # Products are in Set_i (starting with CPA_)
    # Industries are in Set_j

    # Filter for domestic flows only (m = country)
    domestic = df[df['m'] == FOCUS_COUNTRY].copy()

    # Filter for product-to-industry flows
    io_flows = domestic[
        domestic['Set_i'].apply(is_product_code) &
        domestic['Set_j'].apply(is_industry_code)
    ].copy()

    return io_flows


def build_linkage_matrix(io_flows: pd.DataFrame) -> pd.DataFrame:
    """Build sector linkage matrix from IO flows."""
    # Aggregate by Set_i (product/supplying sector) and Set_j (receiving industry)
    matrix = io_flows.pivot_table(
        index='Set_i',
        columns='Set_j',
        values='value',
        aggfunc='sum',
        fill_value=0
    )

    return matrix


def calculate_top_flows(io_flows: pd.DataFrame, n: int = 30) -> pd.DataFrame:
    """Identify top intersectoral flows."""
    # Group by product-industry pair
    top = io_flows.groupby(['Set_i', 'Set_j'])['value'].sum()
    top = top.sort_values(ascending=False).head(n)

    result = pd.DataFrame({
        'From_Product': [idx[0] for idx in top.index],
        'To_Industry': [idx[1] for idx in top.index],
        'Value': top.values
    })

    # Add labels
    result['From_Label'] = result['From_Product'].str.replace('CPA_', '')
    result['To_Label'] = result['To_Industry'].apply(
        lambda x: INDUSTRY_LABELS.get(x, x)
    )

    return result


def calculate_backward_linkages(matrix: pd.DataFrame) -> pd.Series:
    """Calculate backward linkages (column sums = how much each industry buys)."""
    return matrix.sum(axis=0).sort_values(ascending=False)


def calculate_forward_linkages(matrix: pd.DataFrame) -> pd.Series:
    """Calculate forward linkages (row sums = how much each product supplies)."""
    return matrix.sum(axis=1).sort_values(ascending=False)


def plot_linkages_heatmap(matrix: pd.DataFrame, country: str, year: int):
    """Create heatmap of sector linkages."""
    print("\nCreating linkages heatmap...")

    # Select top industries by total intermediate consumption
    col_totals = matrix.sum(axis=0).sort_values(ascending=False)
    top_industries = col_totals.head(15).index

    # Select top products by total supply
    row_totals = matrix.sum(axis=1).sort_values(ascending=False)
    top_products = row_totals.head(15).index

    # Subset matrix
    subset = matrix.loc[top_products, top_industries]

    # Create labels
    row_labels = [str(p).replace('CPA_', '') for p in subset.index]
    col_labels = [INDUSTRY_LABELS.get(c, c)[:15] for c in subset.columns]

    # Convert to billions for readability
    subset_bn = subset / 1e6

    fig, ax = plt.subplots(figsize=(14, 10))

    sns.heatmap(
        subset_bn,
        annot=True,
        fmt='.0f',
        cmap='YlOrRd',
        linewidths=0.5,
        cbar_kws={'label': 'Billion EUR'},
        ax=ax,
        xticklabels=col_labels,
        yticklabels=row_labels
    )

    ax.set_title(f'{country}: Intersectoral Linkages ({year})\nTop Products (rows) x Top Industries (columns)',
                 fontsize=12, fontweight='bold', pad=20)
    ax.set_xlabel('Purchasing Industry')
    ax.set_ylabel('Supplying Product')

    # Rotate labels
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    # Add disclaimer
    fig.text(0.5, 0.01, NOMINAL_DISCLAIMER, ha='center', fontsize=8, style='italic', color='gray')

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig(FIGURES_PATH / 'sector_linkages_heatmap.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {FIGURES_PATH / 'sector_linkages_heatmap.png'}")


def main():
    """Run IO linkages analysis."""
    print("FIGARO-NAM Input-Output Linkages Analysis")
    print("=" * 60)
    print(f"Focus: {FOCUS_COUNTRY}, Year: {ANALYSIS_YEAR}")

    # Load data
    print(f"\nLoading {FOCUS_COUNTRY} data for {ANALYSIS_YEAR}...")
    df = load_country_year(FOCUS_COUNTRY, ANALYSIS_YEAR)

    if df.empty:
        print("No data loaded!")
        return

    print(f"Loaded {len(df):,} rows")

    # Extract IO matrix
    print("\nExtracting IO flows...")
    io_flows = extract_io_matrix(df)
    print(f"Found {len(io_flows):,} product-to-industry flows")

    # Build linkage matrix
    print("Building linkage matrix...")
    matrix = build_linkage_matrix(io_flows)
    print(f"Matrix dimensions: {matrix.shape[0]} products x {matrix.shape[1]} industries")

    # Calculate top flows
    print("Identifying top intersectoral flows...")
    top_flows = calculate_top_flows(io_flows, n=50)

    # Calculate linkages
    print("Calculating backward linkages...")
    backward = calculate_backward_linkages(matrix)

    print("Calculating forward linkages...")
    forward = calculate_forward_linkages(matrix)

    # Save tables
    print("\nSaving tables...")

    matrix.to_csv(TABLES_PATH / 'sector_linkages_matrix.csv')
    print(f"  Saved: {TABLES_PATH / 'sector_linkages_matrix.csv'}")

    top_flows.to_csv(TABLES_PATH / 'top_intersectoral_flows.csv', index=False)
    print(f"  Saved: {TABLES_PATH / 'top_intersectoral_flows.csv'}")

    # Backward linkages table
    backward_df = pd.DataFrame({
        'Industry': backward.index,
        'Intermediate_Inputs': backward.values,
        'Label': [INDUSTRY_LABELS.get(i, i) for i in backward.index]
    })
    backward_df.to_csv(TABLES_PATH / 'backward_linkages.csv', index=False)
    print(f"  Saved: {TABLES_PATH / 'backward_linkages.csv'}")

    # Forward linkages table
    forward_df = pd.DataFrame({
        'Product': forward.index,
        'Total_Supply': forward.values
    })
    forward_df.to_csv(TABLES_PATH / 'forward_linkages.csv', index=False)
    print(f"  Saved: {TABLES_PATH / 'forward_linkages.csv'}")

    # Create visualization
    plot_linkages_heatmap(matrix, FOCUS_COUNTRY, ANALYSIS_YEAR)

    # Print summary
    print("\n" + "=" * 60)
    print(f"SUMMARY: {FOCUS_COUNTRY} Intersectoral Linkages ({ANALYSIS_YEAR})")
    print("=" * 60)

    print("\nTop 10 Intersectoral Flows:")
    print(top_flows[['From_Label', 'To_Label', 'Value']].head(10).to_string(index=False))

    print("\n\nTop 10 Industries by Backward Linkage (Total Intermediate Inputs):")
    for i, (ind, val) in enumerate(backward.head(10).items()):
        label = INDUSTRY_LABELS.get(ind, ind)
        print(f"  {i+1}. {label}: {val/1e6:.1f} Bn EUR")

    print("\n\nTop 10 Products by Forward Linkage (Total Supply to Industries):")
    for i, (prod, val) in enumerate(forward.head(10).items()):
        label = str(prod).replace('CPA_', '')
        print(f"  {i+1}. {label}: {val/1e6:.1f} Bn EUR")

    # Key insights
    print("\n" + "=" * 60)
    print("Key Findings:")
    print("=" * 60)

    total_io = matrix.values.sum()
    print(f"\nTotal intermediate consumption: {total_io/1e6:.1f} billion EUR")

    # Most connected industries
    print("\nMost connected industries (high backward linkage):")
    for ind in backward.head(3).index:
        label = INDUSTRY_LABELS.get(ind, ind)
        val = backward[ind] / 1e6
        print(f"  - {label}: buys {val:.1f} Bn EUR in intermediate inputs")

    print("\nMost supplied products (high forward linkage):")
    for prod in forward.head(3).index:
        label = str(prod).replace('CPA_', '')
        val = forward[prod] / 1e6
        print(f"  - {label}: supplies {val:.1f} Bn EUR to industries")


if __name__ == '__main__':
    main()
