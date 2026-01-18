"""
09_generate_json.py - JSON Aggregation for GitHub Pages Dashboard

Reads CSV files from outputs/tables/ and generates optimized JSON files
for static web visualization.

Output: docs/data/*.json

Usage:
    python scripts/09_generate_json.py
"""

import pandas as pd
import json
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_TABLES = PROJECT_ROOT / 'outputs' / 'tables'
DOCS_DATA = PROJECT_ROOT / 'docs' / 'data'
DOCS_DATA.mkdir(parents=True, exist_ok=True)

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


def generate_trade_partners():
    """Generate trade_partners.json from export/import CSVs."""
    print("Generating trade_partners.json...")

    result = {
        'country': 'DE',
        'year': 2019,
        'exports': [],
        'imports': [],
        'balance': []
    }

    # Load exports
    exports_file = OUTPUT_TABLES / 'DE_exports_by_partner.csv'
    if exports_file.exists():
        exports_df = pd.read_csv(exports_file)
        for _, row in exports_df.head(20).iterrows():
            partner = row.get('Partner', row.get('partner', ''))
            result['exports'].append({
                'partner': partner,
                'partner_name': COUNTRY_NAMES.get(partner, partner),
                'value': float(row.get('Export_Value', row.get('value', 0))),
                'share': float(row.get('Share_%', 0))
            })

    # Load imports
    imports_file = OUTPUT_TABLES / 'DE_imports_by_partner.csv'
    if imports_file.exists():
        imports_df = pd.read_csv(imports_file)
        for _, row in imports_df.head(20).iterrows():
            partner = row.get('Partner', row.get('partner', ''))
            result['imports'].append({
                'partner': partner,
                'partner_name': COUNTRY_NAMES.get(partner, partner),
                'value': float(row.get('Import_Value', row.get('value', 0))),
                'share': float(row.get('Share_%', 0))
            })

    # Load trade balance
    balance_file = OUTPUT_TABLES / 'DE_trade_balance.csv'
    if balance_file.exists():
        balance_df = pd.read_csv(balance_file)
        # Sort by total trade
        if 'Total_Trade' in balance_df.columns:
            balance_df = balance_df.sort_values('Total_Trade', ascending=False)
        for _, row in balance_df.head(20).iterrows():
            partner = row.get('Partner', row.get('partner', ''))
            if partner:
                result['balance'].append({
                    'partner': partner,
                    'partner_name': COUNTRY_NAMES.get(partner, partner),
                    'exports': float(row.get('Exports', 0)),
                    'imports': float(row.get('Imports', 0)),
                    'net': float(row.get('Balance', 0))
                })

    # Load imports by product/sector (for IPR view)
    result['imports_by_sector'] = []
    imports_product_file = OUTPUT_TABLES / 'DE_imports_by_product.csv'
    if imports_product_file.exists():
        imports_df = pd.read_csv(imports_product_file)
        total_imports = imports_df['value'].sum()
        for _, row in imports_df.head(20).iterrows():
            code = str(row.get('Set_i', ''))
            result['imports_by_sector'].append({
                'code': code,
                'label': get_sector_name(code),
                'value': float(row.get('value', 0)),
                'share': float(row.get('value', 0)) / total_imports * 100 if total_imports > 0 else 0
            })

    return result


def generate_sectors():
    """Generate sectors.json from sector data."""
    print("Generating sectors.json...")

    result = {
        'country': 'DE',
        'dynamics': [],
        'wages_by_sector': [],
        'consumption_by_product': []
    }

    # Load sector dynamics
    dynamics_file = OUTPUT_TABLES / 'DE_sector_dynamics.csv'
    if dynamics_file.exists():
        dyn_df = pd.read_csv(dynamics_file)
        for _, row in dyn_df.iterrows():
            # Column is Set_j in CSV
            code = str(row.get('Set_j', row.get('sector', row.get('Sector', ''))))
            # Use YoY changes (change_2019_2020 etc.)
            change_2020 = row.get('change_2019_2020', 0)
            change_2021 = row.get('change_2020_2021', 0)
            change_2022 = row.get('change_2021_2022', 0)
            result['dynamics'].append({
                'code': code,
                'label': get_sector_name(code),
                'change_2020': float(change_2020) if pd.notna(change_2020) else 0,
                'change_2021': float(change_2021) if pd.notna(change_2021) else 0,
                'change_2022': float(change_2022) if pd.notna(change_2022) else 0
            })

    # Load wages by sector (columns: Set_j, value)
    wages_file = OUTPUT_TABLES / 'DE_wages_by_industry.csv'
    if wages_file.exists():
        wages_df = pd.read_csv(wages_file)
        for _, row in wages_df.head(30).iterrows():
            code = str(row.get('Set_j', row.get('Industry', '')))
            result['wages_by_sector'].append({
                'code': code,
                'label': get_sector_name(code),
                'value': float(row.get('value', 0))
            })

    # Load household consumption by product (columns: Set_i, value)
    consumption_file = OUTPUT_TABLES / 'DE_hh_consumption_by_product.csv'
    if consumption_file.exists():
        cons_df = pd.read_csv(consumption_file)
        for _, row in cons_df.head(30).iterrows():
            code = str(row.get('Set_i', row.get('Product', '')))
            result['consumption_by_product'].append({
                'code': code,
                'label': get_sector_name(code),
                'value': float(row.get('value', 0))
            })

    return result


def generate_linkages():
    """Generate linkages.json from IO linkage data."""
    print("Generating linkages.json...")

    result = {
        'country': 'DE',
        'year': 2019,
        'backward': [],
        'forward': [],
        'top_flows': []
    }

    # Load backward linkages (columns: Industry, Intermediate_Inputs, Label)
    backward_file = OUTPUT_TABLES / 'backward_linkages.csv'
    if backward_file.exists():
        back_df = pd.read_csv(backward_file)
        for _, row in back_df.head(20).iterrows():
            code = str(row.get('Industry', ''))
            label = str(row.get('Label', ''))
            result['backward'].append({
                'code': code,
                'label': get_sector_name(code) if get_sector_name(code) != code else label,
                'value': float(row.get('Intermediate_Inputs', 0))
            })

    # Load forward linkages (columns: Product, Total_Supply)
    forward_file = OUTPUT_TABLES / 'forward_linkages.csv'
    if forward_file.exists():
        fwd_df = pd.read_csv(forward_file)
        for _, row in fwd_df.head(20).iterrows():
            code = str(row.get('Product', ''))
            result['forward'].append({
                'code': code,
                'label': get_sector_name(code),
                'value': float(row.get('Total_Supply', 0))
            })

    # Load top flows
    flows_file = OUTPUT_TABLES / 'top_intersectoral_flows.csv'
    if flows_file.exists():
        flows_df = pd.read_csv(flows_file)
        for _, row in flows_df.head(15).iterrows():
            from_code = str(row.get('From_Product', row.get('from', '')))
            to_code = str(row.get('To_Industry', row.get('to', '')))
            result['top_flows'].append({
                'from_code': from_code,
                'from_label': get_sector_name(from_code),
                'to_code': to_code,
                'to_label': get_sector_name(to_code),
                'value': float(row.get('Value', row.get('value', 0)))
            })

    return result


def generate_sankey():
    """Generate sankey.json for circular flow visualization."""
    print("Generating sankey.json...")

    # Try loading from combined time series file first
    all_ts_file = OUTPUT_TABLES / 'all_countries_time_series.csv'
    de_ts_file = OUTPUT_TABLES / 'DE_time_series.csv'

    result = {}
    years = [2019, 2020, 2022]

    if de_ts_file.exists():
        df = pd.read_csv(de_ts_file)

        for year in years:
            year_data = df[df['year'] == year]
            if len(year_data) > 0:
                row = year_data.iloc[0]
                result[str(year)] = {
                    'D11': float(row.get('wages_D11', 0)),
                    'B2': float(row.get('surplus_B2', 0)),
                    'B3': 0,  # Not separately in time_series
                    'P3_S14': float(row.get('hh_consumption', 0)),
                    'P3_S13': float(row.get('gov_consumption', 0)),
                    'P51G': float(row.get('investment', 0)),
                    'net_exports': 0  # External balance not in time_series
                }

    # If no data, create placeholders
    if not result:
        for year in years:
            result[str(year)] = {
                'D11': 1500000,
                'B2': 800000,
                'B3': 200000,
                'P3_S14': 1600000,
                'P3_S13': 500000,
                'P51G': 450000,
                'net_exports': 50000
            }
            print(f"  - {year}: placeholder data used")

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
    print("=" * 60)
    print("FIGARO-NAM JSON Generator for GitHub Pages")
    print("=" * 60)

    # Generate and save JSON files
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
            print(f"  Saved: {output_path}")
        except Exception as e:
            print(f"  ERROR in {filename}: {e}")

    print("\n" + "=" * 60)
    print("JSON generation complete!")
    print(f"Files in: {DOCS_DATA}")
    print("=" * 60)


if __name__ == '__main__':
    main()
