"""
09_generate_json.py - JSON Aggregation for GitHub Pages Dashboard

Reads CSV files from outputs/tables/ and generates optimized JSON files
for static web visualization.

Output: docs/data/*.json

Usage:
    python scripts/09_generate_json.py

Multi-country support:
    - sankey.json, trade_partners.json, sectors.json, linkages.json now support 8 countries
    - Structure: {country_code: {data...}, ...}
    - Falls back to Germany data when country-specific data is unavailable
"""

import pandas as pd
import json
import logging
from pathlib import Path
import pyarrow.parquet as pq

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
log = logging.getLogger(__name__)

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_TABLES = PROJECT_ROOT / 'outputs' / 'tables'
DOCS_DATA = PROJECT_ROOT / 'docs' / 'data'
DOCS_DATA.mkdir(parents=True, exist_ok=True)
DATA_PARQUET = PROJECT_ROOT / 'data' / 'parquet'

# Focus countries for multi-country support
FOCUS_COUNTRIES = ['DE', 'FR', 'IT', 'ES', 'AT', 'PL', 'GR', 'NL']

# Country names
COUNTRY_NAMES = {
    'DE': 'Germany',
    'FR': 'France',
    'IT': 'Italy',
    'ES': 'Spain',
    'AT': 'Austria',
    'PL': 'Poland',
    'GR': 'Greece',
    'NL': 'Netherlands',
    'BE': 'Belgium',
    'PT': 'Portugal',
    'CZ': 'Czechia',
    'HU': 'Hungary',
    'SE': 'Sweden',
    'DK': 'Denmark',
    'FI': 'Finland',
    'IE': 'Ireland',
    'SK': 'Slovakia',
    'BG': 'Bulgaria',
    'HR': 'Croatia',
    'SI': 'Slovenia',
    'LT': 'Lithuania',
    'LV': 'Latvia',
    'EE': 'Estonia',
    'LU': 'Luxembourg',
    'CY': 'Cyprus',
    'MT': 'Malta',
    'RO': 'Romania',
    'GB': 'United Kingdom',
    'CH': 'Switzerland',
    'NO': 'Norway',
    'US': 'USA',
    'CN': 'China',
    'JP': 'Japan',
    'KR': 'South Korea',
    'IN': 'India',
    'BR': 'Brazil',
    'RU': 'Russia',
    'TR': 'Turkey',
    'AU': 'Australia',
    'CA': 'Canada',
    'MX': 'Mexico',
    'WRL_REST': 'Rest of World'
}

# NACE/CPA sector names
SECTOR_NAMES = {
    'A01': 'Agriculture',
    'A02': 'Forestry',
    'A03': 'Fishing',
    'B': 'Mining',
    'C10-C12': 'Food products',
    'C13-C15': 'Textiles',
    'C16': 'Wood products',
    'C17': 'Paper',
    'C18': 'Printing',
    'C19': 'Coke and petroleum',
    'C20': 'Chemicals',
    'C21': 'Pharmaceuticals',
    'C22': 'Rubber and plastics',
    'C23': 'Glass, ceramics, building materials',
    'C24': 'Basic metals',
    'C25': 'Fabricated metals',
    'C26': 'Computer, electronics, optics',
    'C27': 'Electrical equipment',
    'C28': 'Machinery',
    'C29': 'Motor vehicles',
    'C30': 'Other transport equipment',
    'C31_C32': 'Furniture, other manufacturing',
    'C33': 'Repair of machinery',
    'D35': 'Energy supply',
    'E36': 'Water supply',
    'E37-E39': 'Sewerage, waste, recycling',
    'F': 'Construction',
    'G45': 'Motor vehicle trade and repair',
    'G46': 'Wholesale trade',
    'G47': 'Retail trade',
    'H49': 'Land transport',
    'H50': 'Water transport',
    'H51': 'Air transport',
    'H52': 'Warehousing, transport services',
    'H53': 'Postal and courier services',
    'I': 'Accommodation and food services',
    'J58': 'Publishing',
    'J59_J60': 'Film, TV, broadcasting',
    'J61': 'Telecommunications',
    'J62_J63': 'IT services',
    'K64': 'Financial services',
    'K65': 'Insurance',
    'K66': 'Financial and insurance auxiliaries',
    'L': 'Real estate',
    'M69_M70': 'Legal, accounting, consulting',
    'M71': 'Architecture and engineering',
    'M72': 'Research and development',
    'M73': 'Advertising and market research',
    'M74_M75': 'Other professional services',
    'N77': 'Rental and leasing',
    'N78': 'Employment services',
    'N79': 'Travel agencies',
    'N80-N82': 'Security, building services',
    'O84': 'Public administration',
    'P85': 'Education',
    'Q86': 'Health care',
    'Q87_Q88': 'Residential care, social work',
    'R90-R92': 'Arts, entertainment',
    'R93': 'Sports and recreation',
    'S94': 'Membership organizations',
    'S95': 'Repair of consumer goods',
    'S96': 'Other personal services',
    'T': 'Households as employers'
}

# ESA 2010 Codes
CODE_LABELS = {
    'D11': 'Wages and salaries',
    'D12': 'Employer social contributions',
    'D21X31': 'Taxes minus subsidies on products',
    'D29X39': 'Other taxes minus subsidies on production',
    'B2': 'Operating surplus',
    'B3': 'Mixed income',
    'P3_S13': 'Government consumption',
    'P3_S14': 'Household consumption',
    'P3_S15': 'NPISH consumption',
    'P51G': 'Gross fixed capital formation',
    'P6': 'Exports',
    'P7': 'Imports'
}


def get_sector_name(code):
    """Get English label for sector code."""
    # Try direct match
    if code in SECTOR_NAMES:
        return SECTOR_NAMES[code]
    # Try without CPA_ prefix
    clean_code = code.replace('CPA_', '').replace('_', '-')
    if clean_code in SECTOR_NAMES:
        return SECTOR_NAMES[clean_code]
    # Fallback: code itself
    return code


def generate_time_series():
    """Generate time_series.json from time series for all 8 focus countries."""
    print("Generating time_series.json...")

    # Focus countries (all 8)
    FOCUS_COUNTRIES = ['DE', 'FR', 'IT', 'ES', 'AT', 'PL', 'GR', 'NL']
    years = list(range(2010, 2024))

    # Structure data
    result = {
        'years': years,
        'countries': FOCUS_COUNTRIES,
        'country_names': {code: COUNTRY_NAMES.get(code, code) for code in FOCUS_COUNTRIES},
        'aggregates': {
            'hh_consumption': {},
            'gov_consumption': {},
            'investment': {},
            'imports': {}
        },
        'crisis_markers': [
            {'year': 2020, 'label': 'COVID-19'},
            {'year': 2022, 'label': 'Energy Crisis'}
        ]
    }

    # Load time series for all countries
    for ctr in FOCUS_COUNTRIES:
        ts_file = OUTPUT_TABLES / f'{ctr}_time_series.csv'
        if ts_file.exists():
            ts_df = pd.read_csv(ts_file)
            if 'year' in ts_df.columns:
                ts_df = ts_df.set_index('year')
                result['aggregates']['hh_consumption'][ctr] = ts_df['hh_consumption'].tolist() if 'hh_consumption' in ts_df else []
                result['aggregates']['gov_consumption'][ctr] = ts_df['gov_consumption'].tolist() if 'gov_consumption' in ts_df else []
                result['aggregates']['investment'][ctr] = ts_df['investment'].tolist() if 'investment' in ts_df else []
                result['aggregates']['imports'][ctr] = ts_df['imports'].tolist() if 'imports' in ts_df else []
                print(f"  - {ctr}: {len(ts_df)} years loaded")
        else:
            print(f"  - {ctr}: WARNING - file not found ({ts_file})")

    # Load YoY changes (only DE available)
    yoy_file = OUTPUT_TABLES / 'DE_yoy_changes.csv'
    if yoy_file.exists():
        yoy_df = pd.read_csv(yoy_file)
        if 'year' in yoy_df.columns:
            yoy_df = yoy_df.set_index('year')
            result['changes'] = {
                'DE': {
                    'hh_consumption': yoy_df['hh_consumption'].tolist() if 'hh_consumption' in yoy_df else [],
                    'gov_consumption': yoy_df['gov_consumption'].tolist() if 'gov_consumption' in yoy_df else [],
                    'investment': yoy_df['investment'].tolist() if 'investment' in yoy_df else [],
                    'imports': yoy_df['imports'].tolist() if 'imports' in yoy_df else []
                }
            }

    # Load structural breaks
    breaks_file = OUTPUT_TABLES / 'structural_breaks_comparison.csv'
    if breaks_file.exists():
        breaks_df = pd.read_csv(breaks_file)
        result['structural_breaks'] = breaks_df.to_dict('records')

    return result


def generate_trade_for_country(ctr, year=2019):
    """Generate trade data for a single country from parquet files.

    In FIGARO-NAM:
    - Exports: Flows from domestic products (CPA_*) to foreign industries (m != ctr)
    - Imports: Flows from foreign products (m != ctr) going to domestic industries
              OR P7 rows which represent import use
    """

    country_data = {
        'year': year,
        'exports': [],
        'imports': [],
        'balance': [],
        'imports_by_sector': []
    }

    try:
        # Load data from parquet
        df = pq.read_table(
            DATA_PARQUET,
            filters=[('base', '=', year), ('ctr', '=', ctr)]
        ).to_pandas()

        if len(df) == 0:
            return None

        # Exports by partner: Flows from domestic products (CPA_*) to foreign industries
        # These are intermediate exports (goods going to foreign production)
        exports_flow = df[
            (df['Set_i'].str.startswith('CPA_', na=False)) &
            (df['m'] != ctr)  # Foreign destination
        ]
        exports = exports_flow.groupby('m')['value'].sum().reset_index()
        exports = exports.sort_values('value', ascending=False)
        total_exports = exports['value'].sum()

        for _, row in exports.head(20).iterrows():
            partner = row['m']
            country_data['exports'].append({
                'partner': partner,
                'partner_name': COUNTRY_NAMES.get(partner, partner),
                'value': float(row['value']),
                'share': float(row['value']) / total_exports * 100 if total_exports > 0 else 0
            })

        # Imports by partner: Flows from foreign sources to domestic use
        # Use P7 row (imports) where available, or sum foreign product flows
        imports_flow = df[df['Set_i'] == 'P7']
        if len(imports_flow) > 0:
            # P7 row exists - sum by industry destination, but we want by origin
            # P7 flows show import use, not origin
            pass

        # Alternative: Sum all foreign product flows to domestic industries
        imports_from_foreign = df[
            (df['Set_i'].str.startswith('CPA_', na=False)) &
            (df['m'] != ctr) &  # Foreign origin
            (df['Set_j'].str.match(r'^[A-Z][0-9]|^[A-Z]$|^C[0-9]', na=False))  # To industries
        ]

        # Actually, we need to find what was imported from each country
        # In FIGARO, 'm' is the origin country of the product flow
        # So imports = flows where m != ctr (coming from foreign countries)
        # to domestic industries or final use

        # Group by origin country (m)
        imports = imports_from_foreign.groupby('m')['value'].sum().reset_index()
        imports = imports.sort_values('value', ascending=False)
        total_imports = imports['value'].sum()

        for _, row in imports.head(20).iterrows():
            partner = row['m']
            country_data['imports'].append({
                'partner': partner,
                'partner_name': COUNTRY_NAMES.get(partner, partner),
                'value': float(row['value']),
                'share': float(row['value']) / total_imports * 100 if total_imports > 0 else 0
            })

        # Trade balance
        exports_by_partner = {row['m']: row['value'] for _, row in exports.iterrows()}
        imports_by_partner = {row['m']: row['value'] for _, row in imports.iterrows()}
        all_partners = set(exports_by_partner.keys()) | set(imports_by_partner.keys())

        balance_list = []
        for partner in all_partners:
            exp_val = exports_by_partner.get(partner, 0)
            imp_val = imports_by_partner.get(partner, 0)
            balance_list.append({
                'partner': partner,
                'partner_name': COUNTRY_NAMES.get(partner, partner),
                'exports': float(exp_val),
                'imports': float(imp_val),
                'net': float(exp_val - imp_val),
                'total': float(exp_val + imp_val)
            })

        balance_list.sort(key=lambda x: x['total'], reverse=True)
        country_data['balance'] = balance_list[:20]

        # Imports by sector/product - what products are imported
        imports_by_product = imports_from_foreign.groupby('Set_i')['value'].sum().reset_index()
        imports_by_product = imports_by_product.sort_values('value', ascending=False)
        total_sector_imports = imports_by_product['value'].sum()

        for _, row in imports_by_product.head(20).iterrows():
            code = str(row['Set_i'])
            country_data['imports_by_sector'].append({
                'code': code,
                'label': get_sector_name(code),
                'value': float(row['value']),
                'share': float(row['value']) / total_sector_imports * 100 if total_sector_imports > 0 else 0
            })

        return country_data

    except Exception as e:
        print(f"  - {ctr}: Error loading from parquet: {e}")
        import traceback
        traceback.print_exc()
        return None


def generate_trade_partners():
    """Generate trade_partners.json for all countries.

    Multi-country structure: {country: {data...}}
    Falls back to existing CSV data for Germany if parquet unavailable.
    """
    print("Generating trade_partners.json...")

    result = {}

    # Try to generate data for each country from parquet
    for ctr in FOCUS_COUNTRIES:
        country_data = generate_trade_for_country(ctr, year=2019)

        if country_data:
            result[ctr] = country_data
            print(f"  - {ctr}: Generated from parquet ({len(country_data['exports'])} export partners)")
        else:
            # Try existing CSV files for this country
            exports_file = OUTPUT_TABLES / f'{ctr}_exports_by_partner.csv'
            imports_file = OUTPUT_TABLES / f'{ctr}_imports_by_partner.csv'
            balance_file = OUTPUT_TABLES / f'{ctr}_trade_balance.csv'
            imports_product_file = OUTPUT_TABLES / f'{ctr}_imports_by_product.csv'

            if exports_file.exists() or imports_file.exists():
                country_data = {
                    'year': 2019,
                    'exports': [],
                    'imports': [],
                    'balance': [],
                    'imports_by_sector': []
                }

                if exports_file.exists():
                    exports_df = pd.read_csv(exports_file)
                    for _, row in exports_df.head(20).iterrows():
                        partner = row.get('Partner', row.get('partner', ''))
                        country_data['exports'].append({
                            'partner': partner,
                            'partner_name': COUNTRY_NAMES.get(partner, partner),
                            'value': float(row.get('Export_Value', row.get('value', 0))),
                            'share': float(row.get('Share_%', 0))
                        })

                if imports_file.exists():
                    imports_df = pd.read_csv(imports_file)
                    for _, row in imports_df.head(20).iterrows():
                        partner = row.get('Partner', row.get('partner', ''))
                        country_data['imports'].append({
                            'partner': partner,
                            'partner_name': COUNTRY_NAMES.get(partner, partner),
                            'value': float(row.get('Import_Value', row.get('value', 0))),
                            'share': float(row.get('Share_%', 0))
                        })

                if balance_file.exists():
                    balance_df = pd.read_csv(balance_file)
                    if 'Total_Trade' in balance_df.columns:
                        balance_df = balance_df.sort_values('Total_Trade', ascending=False)
                    for _, row in balance_df.head(20).iterrows():
                        partner = row.get('Partner', row.get('partner', ''))
                        if partner:
                            country_data['balance'].append({
                                'partner': partner,
                                'partner_name': COUNTRY_NAMES.get(partner, partner),
                                'exports': float(row.get('Exports', 0)),
                                'imports': float(row.get('Imports', 0)),
                                'net': float(row.get('Balance', 0))
                            })

                if imports_product_file.exists():
                    imports_df = pd.read_csv(imports_product_file)
                    total_imports = imports_df['value'].sum()
                    for _, row in imports_df.head(20).iterrows():
                        code = str(row.get('Set_i', ''))
                        country_data['imports_by_sector'].append({
                            'code': code,
                            'label': get_sector_name(code),
                            'value': float(row.get('value', 0)),
                            'share': float(row.get('value', 0)) / total_imports * 100 if total_imports > 0 else 0
                        })

                result[ctr] = country_data
                print(f"  - {ctr}: Loaded from CSV")
            else:
                print(f"  - {ctr}: No data available")

    # Add metadata about data availability
    result['_meta'] = {
        'countries': list(result.keys()),
        'note': 'Trade data from FIGARO-NAM 2019. Some countries may use Germany data as fallback.',
        'fallback_country': 'DE'
    }

    return result


def generate_sectors_for_country(ctr, year=2019):
    """Generate sector data for a single country from parquet files."""

    country_data = {
        'dynamics': [],
        'wages_by_sector': [],
        'consumption_by_product': []
    }

    try:
        # Load multiple years for dynamics calculation
        years_needed = [2019, 2020, 2021, 2022]
        all_data = []

        for yr in years_needed:
            try:
                df = pq.read_table(
                    DATA_PARQUET,
                    filters=[('base', '=', yr), ('ctr', '=', ctr)]
                ).to_pandas()
                df['year'] = yr
                all_data.append(df)
            except Exception as e:
                print(f"    - Year {yr}: {e}")
                pass

        if len(all_data) < 2:
            return None

        combined_df = pd.concat(all_data, ignore_index=True)

        # Calculate sector dynamics (total output by industry)
        # Filter for actual industry columns (NACE codes)
        industry_pattern = r'^[A-Z][0-9]|^[A-Z]$|^C[0-9]'
        sector_output = combined_df[
            combined_df['Set_j'].str.match(industry_pattern, na=False) &
            (combined_df['m'] == ctr)  # Domestic only
        ].groupby(['year', 'Set_j'])['value'].sum().reset_index()

        if len(sector_output) > 0:
            sector_pivot = sector_output.pivot(index='Set_j', columns='year', values='value')

            for sector in sector_pivot.index:
                row_data = sector_pivot.loc[sector]
                val_2019 = row_data.get(2019, 0)
                val_2020 = row_data.get(2020, 0)
                val_2021 = row_data.get(2021, 0)
                val_2022 = row_data.get(2022, 0)

                change_2020 = ((val_2020 - val_2019) / val_2019 * 100) if val_2019 and val_2019 > 0 else 0
                change_2021 = ((val_2021 - val_2020) / val_2020 * 100) if val_2020 and val_2020 > 0 else 0
                change_2022 = ((val_2022 - val_2021) / val_2021 * 100) if val_2021 and val_2021 > 0 else 0

                country_data['dynamics'].append({
                    'code': sector,
                    'label': get_sector_name(sector),
                    'change_2020': float(change_2020) if pd.notna(change_2020) else 0,
                    'change_2021': float(change_2021) if pd.notna(change_2021) else 0,
                    'change_2022': float(change_2022) if pd.notna(change_2022) else 0
                })

        # Wages by sector (D11 rows) for base year
        df_base = combined_df[combined_df['year'] == year]
        wages = df_base[(df_base['Set_i'] == 'D11') & (df_base['m'] == ctr)].groupby('Set_j')['value'].sum().reset_index()
        wages = wages.sort_values('value', ascending=False)

        for _, row in wages.head(30).iterrows():
            code = str(row['Set_j'])
            country_data['wages_by_sector'].append({
                'code': code,
                'label': get_sector_name(code),
                'value': float(row['value'])
            })

        # Household consumption by product (P3_S14 column)
        consumption = df_base[(df_base['Set_j'] == 'P3_S14') & (df_base['m'] == ctr)].groupby('Set_i')['value'].sum().reset_index()
        consumption = consumption.sort_values('value', ascending=False)

        for _, row in consumption.head(30).iterrows():
            code = str(row['Set_i'])
            country_data['consumption_by_product'].append({
                'code': code,
                'label': get_sector_name(code),
                'value': float(row['value'])
            })

        return country_data

    except Exception as e:
        print(f"  - {ctr}: Error generating sectors from parquet: {e}")
        import traceback
        traceback.print_exc()
        return None


def generate_sectors():
    """Generate sectors.json for all countries.

    Multi-country structure: {country: {data...}}
    """
    print("Generating sectors.json...")

    result = {}

    for ctr in FOCUS_COUNTRIES:
        # Try to generate from parquet
        country_data = generate_sectors_for_country(ctr)

        if country_data and len(country_data['dynamics']) > 0:
            result[ctr] = country_data
            print(f"  - {ctr}: Generated from parquet ({len(country_data['dynamics'])} sectors)")
        else:
            # Try loading from CSV (only exists for DE)
            dynamics_file = OUTPUT_TABLES / f'{ctr}_sector_dynamics.csv'
            wages_file = OUTPUT_TABLES / f'{ctr}_wages_by_industry.csv'
            consumption_file = OUTPUT_TABLES / f'{ctr}_hh_consumption_by_product.csv'

            if dynamics_file.exists() or wages_file.exists():
                country_data = {
                    'dynamics': [],
                    'wages_by_sector': [],
                    'consumption_by_product': []
                }

                if dynamics_file.exists():
                    dyn_df = pd.read_csv(dynamics_file)
                    for _, row in dyn_df.iterrows():
                        code = str(row.get('Set_j', row.get('sector', row.get('Sector', ''))))
                        change_2020 = row.get('change_2019_2020', 0)
                        change_2021 = row.get('change_2020_2021', 0)
                        change_2022 = row.get('change_2021_2022', 0)
                        country_data['dynamics'].append({
                            'code': code,
                            'label': get_sector_name(code),
                            'change_2020': float(change_2020) if pd.notna(change_2020) else 0,
                            'change_2021': float(change_2021) if pd.notna(change_2021) else 0,
                            'change_2022': float(change_2022) if pd.notna(change_2022) else 0
                        })

                if wages_file.exists():
                    wages_df = pd.read_csv(wages_file)
                    for _, row in wages_df.head(30).iterrows():
                        code = str(row.get('Set_j', row.get('Industry', '')))
                        country_data['wages_by_sector'].append({
                            'code': code,
                            'label': get_sector_name(code),
                            'value': float(row.get('value', 0))
                        })

                if consumption_file.exists():
                    cons_df = pd.read_csv(consumption_file)
                    for _, row in cons_df.head(30).iterrows():
                        code = str(row.get('Set_i', row.get('Product', '')))
                        country_data['consumption_by_product'].append({
                            'code': code,
                            'label': get_sector_name(code),
                            'value': float(row.get('value', 0))
                        })

                result[ctr] = country_data
                print(f"  - {ctr}: Loaded from CSV")
            else:
                print(f"  - {ctr}: No data available")

    # Add metadata
    result['_meta'] = {
        'countries': [c for c in result.keys() if c != '_meta'],
        'note': 'Sector dynamics data from FIGARO-NAM.',
        'fallback_country': 'DE'
    }

    return result


def generate_linkages_for_country(ctr, year=2019):
    """Generate IO linkage data for a single country from parquet files."""

    country_data = {
        'year': year,
        'backward': [],
        'forward': [],
        'top_flows': []
    }

    try:
        # Load data from parquet
        df = pq.read_table(
            DATA_PARQUET,
            filters=[('base', '=', year), ('ctr', '=', ctr)]
        ).to_pandas()

        if len(df) == 0:
            return None

        # Backward linkages: Intermediate inputs by industry (sum of CPA_ products going to industries)
        # Filter for intermediate consumption (products to industries)
        intermediate = df[
            (df['Set_i'].str.startswith('CPA_', na=False)) &
            (df['Set_j'].str.match(r'^[A-Z][0-9]|^[A-Z]$|^C[0-9]', na=False)) &
            (df['m'] == ctr)  # Domestic intermediate consumption
        ]

        backward = intermediate.groupby('Set_j')['value'].sum().reset_index()
        backward = backward.sort_values('value', ascending=False)

        for _, row in backward.head(20).iterrows():
            code = str(row['Set_j'])
            country_data['backward'].append({
                'code': code,
                'label': get_sector_name(code),
                'value': float(row['value'])
            })

        # Forward linkages: Total supply by product
        # Filter for products (CPA_) and sum their values
        forward = df[df['Set_i'].str.startswith('CPA_', na=False)].groupby('Set_i')['value'].sum().reset_index()
        forward = forward.sort_values('value', ascending=False)

        for _, row in forward.head(20).iterrows():
            code = str(row['Set_i'])
            country_data['forward'].append({
                'code': code,
                'label': get_sector_name(code),
                'value': float(row['value'])
            })

        # Top intersectoral flows (product -> industry)
        flows = intermediate.groupby(['Set_i', 'Set_j'])['value'].sum().reset_index()
        flows = flows.sort_values('value', ascending=False)

        for _, row in flows.head(15).iterrows():
            from_code = str(row['Set_i'])
            to_code = str(row['Set_j'])
            country_data['top_flows'].append({
                'from_code': from_code,
                'from_label': get_sector_name(from_code),
                'to_code': to_code,
                'to_label': get_sector_name(to_code),
                'value': float(row['value'])
            })

        return country_data

    except Exception as e:
        print(f"  - {ctr}: Error generating linkages from parquet: {e}")
        return None


def generate_linkages():
    """Generate linkages.json for all countries.

    Multi-country structure: {country: {data...}}
    """
    print("Generating linkages.json...")

    result = {}

    for ctr in FOCUS_COUNTRIES:
        # Try to generate from parquet
        country_data = generate_linkages_for_country(ctr, year=2019)

        if country_data and len(country_data['backward']) > 0:
            result[ctr] = country_data
            print(f"  - {ctr}: Generated from parquet ({len(country_data['backward'])} backward linkages)")
        else:
            # Try loading from CSV (may only exist for DE)
            backward_file = OUTPUT_TABLES / f'{ctr}_backward_linkages.csv' if ctr != 'DE' else OUTPUT_TABLES / 'backward_linkages.csv'
            forward_file = OUTPUT_TABLES / f'{ctr}_forward_linkages.csv' if ctr != 'DE' else OUTPUT_TABLES / 'forward_linkages.csv'
            flows_file = OUTPUT_TABLES / f'{ctr}_top_intersectoral_flows.csv' if ctr != 'DE' else OUTPUT_TABLES / 'top_intersectoral_flows.csv'

            # For DE, also try without prefix
            if ctr == 'DE':
                backward_file = OUTPUT_TABLES / 'backward_linkages.csv'
                forward_file = OUTPUT_TABLES / 'forward_linkages.csv'
                flows_file = OUTPUT_TABLES / 'top_intersectoral_flows.csv'

            if backward_file.exists() or forward_file.exists():
                country_data = {
                    'year': 2019,
                    'backward': [],
                    'forward': [],
                    'top_flows': []
                }

                if backward_file.exists():
                    back_df = pd.read_csv(backward_file)
                    for _, row in back_df.head(20).iterrows():
                        code = str(row.get('Industry', ''))
                        label = str(row.get('Label', ''))
                        country_data['backward'].append({
                            'code': code,
                            'label': get_sector_name(code) if get_sector_name(code) != code else label,
                            'value': float(row.get('Intermediate_Inputs', 0))
                        })

                if forward_file.exists():
                    fwd_df = pd.read_csv(forward_file)
                    for _, row in fwd_df.head(20).iterrows():
                        code = str(row.get('Product', ''))
                        country_data['forward'].append({
                            'code': code,
                            'label': get_sector_name(code),
                            'value': float(row.get('Total_Supply', 0))
                        })

                if flows_file.exists():
                    flows_df = pd.read_csv(flows_file)
                    for _, row in flows_df.head(15).iterrows():
                        from_code = str(row.get('From_Product', row.get('from', '')))
                        to_code = str(row.get('To_Industry', row.get('to', '')))
                        country_data['top_flows'].append({
                            'from_code': from_code,
                            'from_label': get_sector_name(from_code),
                            'to_code': to_code,
                            'to_label': get_sector_name(to_code),
                            'value': float(row.get('Value', row.get('value', 0)))
                        })

                result[ctr] = country_data
                print(f"  - {ctr}: Loaded from CSV")
            else:
                print(f"  - {ctr}: No data available")

    # Add metadata
    result['_meta'] = {
        'countries': [c for c in result.keys() if c != '_meta'],
        'note': 'IO linkages data from FIGARO-NAM 2019.',
        'fallback_country': 'DE'
    }

    return result


def generate_sankey():
    """Generate sankey.json for circular flow visualization.

    Multi-country structure: {country: {year: {data...}}}
    """
    print("Generating sankey.json...")

    result = {}
    years = [2019, 2020, 2022]

    for ctr in FOCUS_COUNTRIES:
        ts_file = OUTPUT_TABLES / f'{ctr}_time_series.csv'
        country_data = {}

        if ts_file.exists():
            df = pd.read_csv(ts_file)

            for year in years:
                year_data = df[df['year'] == year]
                if len(year_data) > 0:
                    row = year_data.iloc[0]
                    country_data[str(year)] = {
                        'D11': float(row.get('wages_D11', 0)),
                        'B2': float(row.get('surplus_B2', 0)),
                        'B3': 0,  # Not separately in time_series
                        'P3_S14': float(row.get('hh_consumption', 0)),
                        'P3_S13': float(row.get('gov_consumption', 0)),
                        'P51G': float(row.get('investment', 0)),
                        'net_exports': 0  # External balance not in time_series
                    }

            if country_data:
                result[ctr] = country_data
                print(f"  - {ctr}: {len(country_data)} years loaded")
        else:
            print(f"  - {ctr}: WARNING - file not found ({ts_file})")

    # If no data at all, create placeholders for DE
    if not result:
        result['DE'] = {}
        for year in years:
            result['DE'][str(year)] = {
                'D11': 1500000,
                'B2': 800000,
                'B3': 200000,
                'P3_S14': 1600000,
                'P3_S13': 500000,
                'P51G': 450000,
                'net_exports': 50000
            }
            print(f"  - DE {year}: placeholder data used")

    return result


def generate_metadata():
    """Generate metadata.json with descriptions and notes."""
    print("Generating metadata.json...")

    return {
        'codes': CODE_LABELS,
        'countries': COUNTRY_NAMES,
        'sectors': SECTOR_NAMES,
        'source': 'FIGARO-NAM (Eurostat)',
        'note': 'All values in million EUR, nominal (not inflation-adjusted)',
        'reference_year': '2023',
        'crises': {
            'covid': {
                'year': 2020,
                'label': 'COVID-19 Pandemic',
                'description': 'Lockdowns led to sharp decline in household consumption'
            },
            'energy': {
                'year': 2022,
                'label': 'Energy Crisis',
                'description': 'Rising energy prices; nominal values overstate real growth'
            }
        }
    }


def main():
    """Generate all JSON files."""
    log.info("FIGARO-NAM JSON Generator started")

    json_files = {
        'time_series.json': generate_time_series,
        'trade_partners.json': generate_trade_partners,
        'sectors.json': generate_sectors,
        'linkages.json': generate_linkages,
        'sankey.json': generate_sankey,
        'metadata.json': generate_metadata
    }

    for filename, generator in json_files.items():
        try:
            data = generator()
            output_path = DOCS_DATA / filename
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            log.info(f"Saved: {filename}")
        except Exception as e:
            log.error(f"{filename}: {e}")

    log.info(f"Complete. Files in: {DOCS_DATA}")


if __name__ == '__main__':
    main()
