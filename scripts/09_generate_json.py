"""
09_generate_json.py - JSON-Aggregation fuer GitHub Pages Dashboard

Liest CSV-Dateien aus outputs/tables/ und erzeugt optimierte JSON-Dateien
fuer die statische Web-Visualisierung.

Output: docs/data/*.json

Usage:
    python scripts/09_generate_json.py
"""

import pandas as pd
import json
from pathlib import Path

# Pfade
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_TABLES = PROJECT_ROOT / 'outputs' / 'tables'
DOCS_DATA = PROJECT_ROOT / 'docs' / 'data'
DOCS_DATA.mkdir(parents=True, exist_ok=True)

# Deutsche Bezeichnungen fuer Laender
LAENDER_NAMEN = {
    'DE': 'Deutschland',
    'FR': 'Frankreich',
    'IT': 'Italien',
    'ES': 'Spanien',
    'AT': 'Oesterreich',
    'PL': 'Polen',
    'GR': 'Griechenland',
    'NL': 'Niederlande',
    'BE': 'Belgien',
    'PT': 'Portugal',
    'CZ': 'Tschechien',
    'HU': 'Ungarn',
    'SE': 'Schweden',
    'DK': 'Daenemark',
    'FI': 'Finnland',
    'IE': 'Irland',
    'SK': 'Slowakei',
    'BG': 'Bulgarien',
    'HR': 'Kroatien',
    'SI': 'Slowenien',
    'LT': 'Litauen',
    'LV': 'Lettland',
    'EE': 'Estland',
    'LU': 'Luxemburg',
    'CY': 'Zypern',
    'MT': 'Malta',
    'RO': 'Rumaenien',
    'GB': 'Grossbritannien',
    'CH': 'Schweiz',
    'NO': 'Norwegen',
    'US': 'USA',
    'CN': 'China',
    'JP': 'Japan',
    'KR': 'Suedkorea',
    'IN': 'Indien',
    'BR': 'Brasilien',
    'RU': 'Russland',
    'TR': 'Tuerkei',
    'AU': 'Australien',
    'CA': 'Kanada',
    'MX': 'Mexiko',
    'WRL_REST': 'Rest der Welt'
}

# Deutsche Bezeichnungen fuer NACE/CPA Codes
BRANCHEN_NAMEN = {
    'A01': 'Landwirtschaft',
    'A02': 'Forstwirtschaft',
    'A03': 'Fischerei',
    'B': 'Bergbau',
    'C10-C12': 'Nahrungsmittel',
    'C13-C15': 'Textilien',
    'C16': 'Holzwaren',
    'C17': 'Papier',
    'C18': 'Druckerzeugnisse',
    'C19': 'Kokerei, Mineraloelverarbeitung',
    'C20': 'Chemische Erzeugnisse',
    'C21': 'Pharmazeutika',
    'C22': 'Gummi- und Kunststoffwaren',
    'C23': 'Glas, Keramik, Baustoffe',
    'C24': 'Metallerzeugung',
    'C25': 'Metallerzeugnisse',
    'C26': 'EDV, Elektronik, Optik',
    'C27': 'Elektrische Ausruestungen',
    'C28': 'Maschinenbau',
    'C29': 'Kraftfahrzeuge',
    'C30': 'Sonstiger Fahrzeugbau',
    'C31_C32': 'Moebel, sonstige Waren',
    'C33': 'Reparatur von Maschinen',
    'D35': 'Energieversorgung',
    'E36': 'Wasserversorgung',
    'E37-E39': 'Abwasser, Abfall, Recycling',
    'F': 'Baugewerbe',
    'G45': 'Kfz-Handel und -Reparatur',
    'G46': 'Grosshandel',
    'G47': 'Einzelhandel',
    'H49': 'Landverkehr',
    'H50': 'Schifffahrt',
    'H51': 'Luftfahrt',
    'H52': 'Lagerei, Verkehrsdienste',
    'H53': 'Post- und Kurierdienste',
    'I': 'Gastgewerbe',
    'J58': 'Verlagswesen',
    'J59_J60': 'Film, TV, Rundfunk',
    'J61': 'Telekommunikation',
    'J62_J63': 'IT-Dienstleistungen',
    'K64': 'Finanzdienstleistungen',
    'K65': 'Versicherungen',
    'K66': 'Finanz- und Versicherungshilfen',
    'L': 'Grundstuecks- und Wohnungswesen',
    'M69_M70': 'Rechts-/Steuerberatung, Unternehmensberatung',
    'M71': 'Architektur- und Ingenieurbueros',
    'M72': 'Forschung und Entwicklung',
    'M73': 'Werbung und Marktforschung',
    'M74_M75': 'Sonstige freiberufliche Taetigkeiten',
    'N77': 'Vermietung beweglicher Sachen',
    'N78': 'Vermittlung von Arbeitskraeften',
    'N79': 'Reisebueros und Reiseveranstalter',
    'N80-N82': 'Sicherheitsdienste, Gebaeudebetreuung',
    'O84': 'Oeffentliche Verwaltung',
    'P85': 'Erziehung und Unterricht',
    'Q86': 'Gesundheitswesen',
    'Q87_Q88': 'Heime und Sozialwesen',
    'R90-R92': 'Kunst, Unterhaltung',
    'R93': 'Sport und Erholung',
    'S94': 'Interessenvertretungen',
    'S95': 'Reparatur von Gebrauchsguetern',
    'S96': 'Sonstige persoenliche Dienstleistungen',
    'T': 'Private Haushalte'
}

# ESA 2010 Codes
CODE_BEZEICHNUNGEN = {
    'D11': 'Loehne und Gehaelter',
    'D12': 'Sozialbeitraege der Arbeitgeber',
    'D21X31': 'Guetersteuern minus Subventionen',
    'D29X39': 'Produktionsabgaben minus Subventionen',
    'B2': 'Betriebsueberschuss',
    'B3': 'Selbstaendigeneinkommen',
    'P3_S13': 'Staatskonsum',
    'P3_S14': 'Privater Konsum',
    'P3_S15': 'NPISH-Konsum',
    'P51G': 'Bruttoanlageinvestitionen',
    'P6': 'Exporte',
    'P7': 'Importe'
}


def get_branche_name(code):
    """Hole deutsche Bezeichnung fuer Branchencode."""
    # Versuche direkten Match
    if code in BRANCHEN_NAMEN:
        return BRANCHEN_NAMEN[code]
    # Versuche ohne CPA_ Prefix
    clean_code = code.replace('CPA_', '').replace('_', '-')
    if clean_code in BRANCHEN_NAMEN:
        return BRANCHEN_NAMEN[clean_code]
    # Fallback: Code selbst
    return code


def generate_time_series():
    """Generiere time_series.json aus Zeitreihen fuer alle 8 Fokus-Laender."""
    print("Generiere time_series.json...")

    # Fokus-Laender (alle 8)
    FOCUS_COUNTRIES = ['DE', 'FR', 'IT', 'ES', 'AT', 'PL', 'GR', 'NL']
    jahre = list(range(2010, 2024))

    # Strukturiere Daten
    result = {
        'jahre': jahre,
        'laender': FOCUS_COUNTRIES,
        'laender_namen': {code: LAENDER_NAMEN.get(code, code) for code in FOCUS_COUNTRIES},
        'aggregate': {
            'hh_konsum': {},
            'staat_konsum': {},
            'investitionen': {},
            'importe': {}
        },
        'krisen_marker': [
            {'jahr': 2020, 'bezeichnung': 'COVID-19'},
            {'jahr': 2022, 'bezeichnung': 'Energiekrise'}
        ]
    }

    # Lade Zeitreihen fuer alle Laender
    for ctr in FOCUS_COUNTRIES:
        ts_file = OUTPUT_TABLES / f'{ctr}_time_series.csv'
        if ts_file.exists():
            ts_df = pd.read_csv(ts_file)
            if 'year' in ts_df.columns:
                ts_df = ts_df.set_index('year')
                result['aggregate']['hh_konsum'][ctr] = ts_df['hh_consumption'].tolist() if 'hh_consumption' in ts_df else []
                result['aggregate']['staat_konsum'][ctr] = ts_df['gov_consumption'].tolist() if 'gov_consumption' in ts_df else []
                result['aggregate']['investitionen'][ctr] = ts_df['investment'].tolist() if 'investment' in ts_df else []
                result['aggregate']['importe'][ctr] = ts_df['imports'].tolist() if 'imports' in ts_df else []
                print(f"  - {ctr}: {len(ts_df)} Jahre geladen")
        else:
            print(f"  - {ctr}: WARNUNG - keine Datei gefunden ({ts_file})")

    # Lade YoY-Aenderungen (nur DE verfuegbar)
    yoy_file = OUTPUT_TABLES / 'DE_yoy_changes.csv'
    if yoy_file.exists():
        yoy_df = pd.read_csv(yoy_file)
        if 'year' in yoy_df.columns:
            yoy_df = yoy_df.set_index('year')
            result['veraenderungen'] = {
                'DE': {
                    'hh_konsum': yoy_df['hh_consumption'].tolist() if 'hh_consumption' in yoy_df else [],
                    'staat_konsum': yoy_df['gov_consumption'].tolist() if 'gov_consumption' in yoy_df else [],
                    'investitionen': yoy_df['investment'].tolist() if 'investment' in yoy_df else [],
                    'importe': yoy_df['imports'].tolist() if 'imports' in yoy_df else []
                }
            }

    # Lade Strukturbrueche
    breaks_file = OUTPUT_TABLES / 'structural_breaks_comparison.csv'
    if breaks_file.exists():
        breaks_df = pd.read_csv(breaks_file)
        result['strukturbrueche'] = breaks_df.to_dict('records')

    return result


def generate_trade_partners():
    """Generiere trade_partners.json aus Export/Import CSVs."""
    print("Generiere trade_partners.json...")

    result = {
        'land': 'DE',
        'jahr': 2019,
        'exporte': [],
        'importe': [],
        'bilanz': []
    }

    # Lade Exporte
    exports_file = OUTPUT_TABLES / 'DE_exports_by_partner.csv'
    if exports_file.exists():
        exports_df = pd.read_csv(exports_file)
        for _, row in exports_df.head(20).iterrows():
            partner = row.get('Partner', row.get('partner', ''))
            result['exporte'].append({
                'partner': partner,
                'partner_name': LAENDER_NAMEN.get(partner, partner),
                'wert': float(row.get('Export_Value', row.get('value', 0))),
                'anteil': float(row.get('Share_%', 0))
            })

    # Lade Importe
    imports_file = OUTPUT_TABLES / 'DE_imports_by_partner.csv'
    if imports_file.exists():
        imports_df = pd.read_csv(imports_file)
        for _, row in imports_df.head(20).iterrows():
            partner = row.get('Partner', row.get('partner', ''))
            result['importe'].append({
                'partner': partner,
                'partner_name': LAENDER_NAMEN.get(partner, partner),
                'wert': float(row.get('Import_Value', row.get('value', 0))),
                'anteil': float(row.get('Share_%', 0))
            })

    # Lade Handelsbilanz
    balance_file = OUTPUT_TABLES / 'DE_trade_balance.csv'
    if balance_file.exists():
        balance_df = pd.read_csv(balance_file)
        # Sortiere nach Gesamthandel
        if 'Total_Trade' in balance_df.columns:
            balance_df = balance_df.sort_values('Total_Trade', ascending=False)
        for _, row in balance_df.head(20).iterrows():
            partner = row.get('Partner', row.get('partner', ''))
            if partner:
                result['bilanz'].append({
                    'partner': partner,
                    'partner_name': LAENDER_NAMEN.get(partner, partner),
                    'exporte': float(row.get('Exports', 0)),
                    'importe': float(row.get('Imports', 0)),
                    'saldo': float(row.get('Balance', 0))
                })

    return result


def generate_sectors():
    """Generiere sectors.json aus Sektordaten."""
    print("Generiere sectors.json...")

    result = {
        'land': 'DE',
        'dynamik': [],
        'loehne_nach_branche': [],
        'konsum_nach_produkt': []
    }

    # Lade Sektordynamik
    dynamics_file = OUTPUT_TABLES / 'DE_sector_dynamics.csv'
    if dynamics_file.exists():
        dyn_df = pd.read_csv(dynamics_file)
        for _, row in dyn_df.iterrows():
            # Spalte heisst Set_j in der CSV
            code = str(row.get('Set_j', row.get('sector', row.get('Sector', ''))))
            # Nutze YoY-Aenderungen (change_2019_2020 etc.)
            change_2020 = row.get('change_2019_2020', 0)
            change_2021 = row.get('change_2020_2021', 0)
            change_2022 = row.get('change_2021_2022', 0)
            result['dynamik'].append({
                'code': code,
                'bezeichnung': get_branche_name(code),
                'veraenderung_2020': float(change_2020) if pd.notna(change_2020) else 0,
                'veraenderung_2021': float(change_2021) if pd.notna(change_2021) else 0,
                'veraenderung_2022': float(change_2022) if pd.notna(change_2022) else 0
            })

    # Lade Loehne nach Branche (Spalten: Set_j, value)
    wages_file = OUTPUT_TABLES / 'DE_wages_by_industry.csv'
    if wages_file.exists():
        wages_df = pd.read_csv(wages_file)
        for _, row in wages_df.head(30).iterrows():
            code = str(row.get('Set_j', row.get('Industry', '')))
            result['loehne_nach_branche'].append({
                'code': code,
                'bezeichnung': get_branche_name(code),
                'wert': float(row.get('value', 0))
            })

    # Lade HH-Konsum nach Produkt (Spalten: Set_i, value)
    consumption_file = OUTPUT_TABLES / 'DE_hh_consumption_by_product.csv'
    if consumption_file.exists():
        cons_df = pd.read_csv(consumption_file)
        for _, row in cons_df.head(30).iterrows():
            code = str(row.get('Set_i', row.get('Product', '')))
            result['konsum_nach_produkt'].append({
                'code': code,
                'bezeichnung': get_branche_name(code),
                'wert': float(row.get('value', 0))
            })

    return result


def generate_linkages():
    """Generiere linkages.json aus IO-Verflechtungsdaten."""
    print("Generiere linkages.json...")

    result = {
        'land': 'DE',
        'jahr': 2019,
        'rueckwaerts': [],
        'vorwaerts': [],
        'top_fluesse': []
    }

    # Lade Rueckwaertsverflechtung (Spalten: Industry, Intermediate_Inputs, Label)
    backward_file = OUTPUT_TABLES / 'backward_linkages.csv'
    if backward_file.exists():
        back_df = pd.read_csv(backward_file)
        for _, row in back_df.head(20).iterrows():
            code = str(row.get('Industry', ''))
            label = str(row.get('Label', ''))
            result['rueckwaerts'].append({
                'code': code,
                'bezeichnung': get_branche_name(code) if get_branche_name(code) != code else label,
                'wert': float(row.get('Intermediate_Inputs', 0))
            })

    # Lade Vorwaertsverflechtung (Spalten: Product, Total_Supply)
    forward_file = OUTPUT_TABLES / 'forward_linkages.csv'
    if forward_file.exists():
        fwd_df = pd.read_csv(forward_file)
        for _, row in fwd_df.head(20).iterrows():
            code = str(row.get('Product', ''))
            result['vorwaerts'].append({
                'code': code,
                'bezeichnung': get_branche_name(code),
                'wert': float(row.get('Total_Supply', 0))
            })

    # Lade Top-Fluesse
    flows_file = OUTPUT_TABLES / 'top_intersectoral_flows.csv'
    if flows_file.exists():
        flows_df = pd.read_csv(flows_file)
        for _, row in flows_df.head(15).iterrows():
            from_code = str(row.get('From_Product', row.get('from', '')))
            to_code = str(row.get('To_Industry', row.get('to', '')))
            result['top_fluesse'].append({
                'von_code': from_code,
                'von_bezeichnung': get_branche_name(from_code),
                'nach_code': to_code,
                'nach_bezeichnung': get_branche_name(to_code),
                'wert': float(row.get('Value', row.get('value', 0)))
            })

    return result


def generate_metadata():
    """Generiere metadata.json mit Beschreibungen und Hinweisen."""
    print("Generiere metadata.json...")

    return {
        'codes': CODE_BEZEICHNUNGEN,
        'laender': LAENDER_NAMEN,
        'branchen': BRANCHEN_NAMEN,
        'quellen': 'FIGARO-NAM (Eurostat)',
        'hinweis': 'Alle Werte in Mio. EUR, nominal (nicht inflationsbereinigt)',
        'stand': '2023',
        'krisen': {
            'covid': {
                'jahr': 2020,
                'bezeichnung': 'COVID-19 Pandemie',
                'beschreibung': 'Lockdowns fuehrten zu starkem Rueckgang des privaten Konsums'
            },
            'energie': {
                'jahr': 2022,
                'bezeichnung': 'Energiekrise',
                'beschreibung': 'Steigende Energiepreise, nominale Werte ueberzeichnen reales Wachstum'
            }
        }
    }


def main():
    """Generiere alle JSON-Dateien."""
    print("=" * 60)
    print("FIGARO-NAM JSON-Generator fuer GitHub Pages")
    print("=" * 60)

    # Generiere und speichere JSON-Dateien
    json_files = {
        'time_series.json': generate_time_series,
        'trade_partners.json': generate_trade_partners,
        'sectors.json': generate_sectors,
        'linkages.json': generate_linkages,
        'metadata.json': generate_metadata
    }

    for filename, generator in json_files.items():
        try:
            data = generator()
            output_path = DOCS_DATA / filename
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  Gespeichert: {output_path}")
        except Exception as e:
            print(f"  FEHLER bei {filename}: {e}")

    print("\n" + "=" * 60)
    print("JSON-Generierung abgeschlossen!")
    print(f"Dateien in: {DOCS_DATA}")
    print("=" * 60)


if __name__ == '__main__':
    main()
