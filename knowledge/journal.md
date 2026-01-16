# Working Journal: FIGARO-NAM Analysis

This journal documents the collaboration between Christopher Pollin and Claude Code (Opus 4.5) during the development of an agentic workflow for macroeconomic data analysis.

**Project:** wiiw-figaro-nam-demo
**Workshop:** AI for Data Analysis & Visualisation (wiiw, 10 February 2026)
**Data Provider:** David Zenz (wiiw)

---

## Session Log

### 2026-01-16 (Session 7) - Agentic Research Run: Energiekrise vs COVID-Erholung

**Objective:** Vollstaendiger agentenbasierter Forschungsdurchlauf mit Custom Subagents

**Workflow-Setup:**
- Erstellung von drei Custom Subagents (`.claude/agents/`):
  - `analysis-agent.md` - Datenexploration, Hypothesenbildung
  - `implementation-agent.md` - Code-Entwicklung, Visualisierung
  - `synthesis-agent.md` - Paper-Erstellung
- Erweiterung von `CLAUDE.md` mit vollstaendiger Workflow-Dokumentation
- Anlage der Arbeitsordner-Struktur (`agents/`, `runs/`)

**Forschungsfrage:**
> Hat die Energiekrise 2022 die COVID-Erholung in Suedeuropa gebremst?

**Phase 1 - Exploration:**
- 5 Hypothesen formuliert (H1-H5)
- Integrierte Hypothese H_int aus H1+H4+H5 entwickelt
- Expert-in-the-Loop Entscheidung: Portugal ergaenzen, nominal+real analysieren

**Phase 2 - Implementierung:**
- Portugal-Daten aus Parquet extrahiert (`scripts/11_extract_portugal.py`)
- Hauptanalyse-Skript erstellt (`scripts/12_hypothesis_h_int.py`)
- HICP-Deflatoren (Eurostat) integriert fuer Real-Berechnung
- 3 Tabellen + 3 Grafiken generiert

**Phase 3 - Synthese:**
- Paper erstellt: `runs/run-2026-01-16-1430/paper/paper.md`
- Visuelle Qualitaetspruefung durch User identifizierte Grafikfehler
- Korrekturen: Dynamischer Titel, korrekter Zeitraum, vollstaendige Datenpunkte

**Zentrale Befunde:**

| Teilhypothese | Status | Kernbefund |
|---------------|--------|------------|
| H5: Basis-Effekt | BESTAETIGT | r = -0.52, tieferer Einbruch erklaert hoehere Erholungsraten |
| H1a: Sued nominal staerker | WIDERLEGT | Nord 113.1 vs. Sued 110.0 |
| H1b: Sued real schwaecher | NICHT BESTAETIGT | Praktisch gleich (99.6 vs. 99.5) |
| H4: Sued hoehere Fiskalexpansion | WIDERLEGT | Nord +19.7% vs. Sued +14.3% |

**Ueberraschende Erkenntnisse:**
1. Nordeuropa zeigt staerkere nominale Erholung (Energiepreis-Inflation)
2. Deutschland fuehrt bei Staatskonsum-Expansion (+21.2%)
3. Reale Konvergenz beider Regionen auf ~99.5% des Vorkrisenniveaus

**Dateien erstellt:**

| Datei | Beschreibung |
|-------|--------------|
| `.claude/agents/analysis-agent.md` | Subagent: Exploration |
| `.claude/agents/implementation-agent.md` | Subagent: Code |
| `.claude/agents/synthesis-agent.md` | Subagent: Paper |
| `scripts/11_extract_portugal.py` | PT-Daten Extraktion |
| `scripts/12_hypothesis_h_int.py` | Hauptanalyse H_int |
| `outputs/tables/PT_time_series.csv` | Portugal Zeitreihe |
| `outputs/tables/recovery_comparison.csv` | Erholungsvergleich |
| `outputs/tables/basis_effect_analysis.csv` | Basis-Effekt |
| `outputs/tables/fiscal_response.csv` | Fiskalische Reaktion |
| `outputs/figures/basis_effect_scatter.png` | Streudiagramm |
| `outputs/figures/recovery_nominal_vs_real.png` | Erholungsbalken |
| `outputs/figures/fiscal_cushion.png` | Fiskal-Grafik |
| `runs/run-2026-01-16-1430/` | Vollstaendiger Run |
| `agents/analysis/hypotheses.md` | Hypothesendokumentation |

**Methodische Learnings:**
- Custom Subagents erfordern Session-Neustart zum Laden
- Visuelle Qualitaetspruefung durch User essentiell
- Dynamische Titel verhindern Diskrepanzen zwischen Daten und Beschriftung

**Phase Status:**
- Phase 3 (Human-in-the-Loop): Erster vollstaendiger Run abgeschlossen
- Agentic Workflow demonstriert und dokumentiert

---

### 2026-01-15 (Session 6) - Dashboard Erweiterung & UI-Refactoring

**Objective:** Fehlende Visualisierungen hinzufuegen und CSS/HTML verbessern

**Neue Visualisierungen:**

1. **Erholung-Tab** (`docs/js/recovery.js`)
   - Recovery-Indikator: Vergleich mit Pre-COVID Niveau (2019 = 0%)
   - Balkendiagramm mit 8 Laendern, sortiert nach Erholung
   - Dropdown fuer Vergleichszeitraum (2021/2022/2023 vs 2019)
   - Forschungsfrage B3: Hat die Energiekrise 2022 die COVID-Erholung gebremst?

2. **Kreislauf-Tab** (`docs/js/sankey.js`)
   - Sankey-Diagramm fuer Wirtschaftskreislauf
   - Flow: Einkommen (D11, B2) -> Volkseinkommen -> Verwendung (P3, P51G)
   - Jahr-Auswahl: 2019/2020/2022
   - Forschungsfrage A1: Wie fliesst Wertschoepfung?

3. **Handel: IPR-Ansicht** (Erweiterung `docs/js/trade.js`)
   - Neue Option: "Importe nach Sektor (IPR)"
   - Zeigt Import-Intensitaet nach Produktgruppe
   - Dynamisches Label: "Anzahl Partner" vs "Anzahl Sektoren"

**CSS-Refactoring** (`docs/css/style.css`):
- CSS Custom Properties (Design Tokens) fuer Farben, Spacing, Typografie
- Responsive Breakpoints bei 768px und 480px
- Verbesserte Accessibility mit Focus-States
- Laenderfarben als CSS-Variablen

**HTML-Refactoring** (`docs/index.html`):
- Semantische Elemente: `<article>`, `<figure>`, `<aside>`
- ARIA-Labels fuer bessere Accessibility
- Meta-Tags fuer SEO

**Kleine UI-Verbesserungen:**
- Erholung: X-Achsen-Labels 45 Grad rotiert (bottom margin 60->100)
- Sankey: Distincte Farben (income=#059669, distribution=#7c3aed, use=#dc2626)
- Handel: Label wechselt dynamisch je nach Modus

**Neue Dateien:**

| Datei | Beschreibung |
|-------|--------------|
| `docs/js/recovery.js` | Recovery-Indikator Chart |
| `docs/js/sankey.js` | Sankey-Diagramm |
| `docs/data/sankey.json` | Kreislauf-Daten (3 Jahre) |

**Aktualisierte JSON-Groessen:**

| Datei | Groesse |
|-------|---------|
| `time_series.json` | 15.0 KB |
| `trade_partners.json` | 8.0 KB |
| `sectors.json` | 21.9 KB |
| `linkages.json` | 7.6 KB |
| `sankey.json` | 0.5 KB |
| `metadata.json` | 4.3 KB |
| **Total** | **~57 KB** |

**Phase Status:**
- Phase 3 (Human-in-the-Loop): Dashboard erweitert auf 6 Tabs
- Forschungsfragen-Abdeckung verbessert

---

### 2026-01-15 (Session 5) - Web Dashboard & Multi-Country Data

**Objective:** Create interactive GitHub Pages dashboard for Phase 3 Human-in-the-Loop exploration

**Planning:**
- Entered plan mode and created comprehensive architecture plan
- User selected D3.js (not Chart.js/Plotly) for maximum flexibility
- User selected German-only UI (not bilingual)
- Plan documented in `docs/` folder structure

**Implementation:**

1. **JSON Data Aggregation Script** (`scripts/09_generate_json.py`)
   - Reads 34 CSV files from `outputs/tables/`
   - Generates 5 optimized JSON files (~47 KB total):
     - `time_series.json` - Macro aggregates by year/country
     - `trade_partners.json` - Export/Import by partner
     - `sectors.json` - Sectoral dynamics with YoY changes
     - `linkages.json` - IO backward/forward linkages
     - `metadata.json` - German labels for codes
   - Fixed column name mappings (Set_j vs Industry, Set_i vs Product)

2. **Static Web Dashboard** (`docs/`)
   - `index.html` - Tab-based navigation (4 views)
   - `css/style.css` - Clean scientific design
   - `js/app.js` - Data loading, tooltip helpers, formatting
   - `js/timeseries.js` - Multi-line chart with crisis markers
   - `js/trade.js` - Horizontal bar chart (Export/Import/Balance)
   - `js/sectors.js` - Diverging bar chart (YoY changes)
   - `js/linkages.js` - IO linkage visualization

3. **D3.js Visualizations (v7)**
   - Responsive SVG charts
   - Interactive tooltips
   - Crisis markers (COVID 2020, Energiekrise 2022)
   - Country color palette for multi-line comparison

**Bug Fixes:**
- Fixed negative rect width errors: Added dimension checks (`if (width <= 0 || height <= 0) return;`) to all 4 chart update functions
- Fixed country filter: Only show countries with actual data in checkboxes
- Fixed CSV column mappings: `Set_j` instead of `Industry`, `change_2019_2020` instead of `change_2020`

**Data Gap Identified:**
- Time series CSV only exists for Germany (`DE_time_series.csv`)
- Other 7 focus countries (FR, IT, ES, AT, PL, GR, NL) have:
  - Structural break data (in `structural_breaks_comparison.csv`)
  - CAGR/trend data (in `baseline_trend_analysis.csv`)
  - But NO complete time series CSV
- Solution: Need to generate time series for all 8 countries from Parquet data

**Files Created:**

| File | Description |
|------|-------------|
| `scripts/09_generate_json.py` | JSON aggregation from CSVs |
| `docs/index.html` | Dashboard HTML with 4 tabs |
| `docs/css/style.css` | Responsive styling |
| `docs/js/app.js` | Main logic, data loading |
| `docs/js/timeseries.js` | Time series D3 chart |
| `docs/js/trade.js` | Trade partner D3 chart |
| `docs/js/sectors.js` | Sector dynamics D3 chart |
| `docs/js/linkages.js` | IO linkages D3 chart |
| `docs/data/time_series.json` | 5.3 KB |
| `docs/data/trade_partners.json` | 8.0 KB |
| `docs/data/sectors.json` | 21.9 KB |
| `docs/data/linkages.json` | 7.6 KB |
| `docs/data/metadata.json` | 4.3 KB |

**User Testing:**
- All 4 tabs visually working (confirmed via screenshots)
- Console errors fixed after dimension check implementation

**Multi-Country Data Extension:**
- Created `scripts/10_generate_all_timeseries.py` to extract time series from Parquet
- Generated time series CSVs for all 8 focus countries (DE, FR, IT, ES, AT, PL, GR, NL)
- Updated `scripts/09_generate_json.py` to load all 8 countries
- Regenerated `time_series.json` (now 15 KB with all countries)

**Verification - COVID Impact (2019-2020 HH Consumption):**

| Country | Change |
|---------|--------|
| ES | -17.0% |
| GR | -16.1% |
| IT | -12.3% |
| AT | -10.1% |
| FR | -7.6% |
| DE | -7.1% |
| NL | -6.4% |
| PL | -4.7% |

**Updated File Sizes:**

| File | Size |
|------|------|
| `time_series.json` | 15.0 KB (was 5.3 KB) |
| `trade_partners.json` | 8.0 KB |
| `sectors.json` | 21.9 KB |
| `linkages.json` | 7.6 KB |
| `metadata.json` | 4.3 KB |
| **Total** | **56.8 KB** |

**Phase Status:**
- Phase 3 (Human-in-the-Loop): Dashboard complete with 8 countries
- Ready for GitHub Pages deployment

---

### 2026-01-15 (Session 4) - Extended Exploration & Documentation

**Objective:** Implement Phase 2b exploration scripts and complete knowledge documentation

**Actions:**
- Created comprehensive glossary (`knowledge/glossary.md`) with IO analysis terms
- Implemented 4 new exploration scripts (05-08)
- Executed all 4 scripts successfully
- Fixed export analysis: FIGARO records exports in partner country data (m=exporter)
- Extended glossary with ESA 2010 codes, FIGARO methodik, empirische Referenzwerte
- Updated research.md with Phase 2a/2b structure

**Script Execution Results:**

05_baseline_trend.py:
- CAGR 2010-2018 calculated for 8 countries x 4 aggregates
- Trend deviation quantified: ES worst at -18.1% below trend
- Key insight: YoY understates impact; trend deviation shows full gap

06_export_analysis.py:
- Fixed: Exports found by loading partner countries (m=DE in FR data = DE exports to FR)
- DE top export destinations: US (9.8%), CN (9.6%), FR (8.1%)
- Export categories: Services 33%, Manufacturing 23%, Vehicles 11%

07_negative_values.py:
- Found 36,199 negative values in 8-country sample
- Mainly B-Balances (adjustments) and CPA-Products
- Germany accounts for most (6.5M EUR total negative)
- Confirmed: legitimate ESA 2010 entries (subsidies > taxes, inventory changes)

08_io_linkages.py:
- Built 62x61 product-industry matrix for DE 2019
- Highest backward linkage: Motor vehicles, Construction
- Highest forward linkage: Legal/Accounting (M69_70), Real estate (L)
- Top flow: C29 (vehicles) to Motor vehicles industry (61.6 Bn)

**Knowledge Documentation Extended:**
- glossary.md: Added D-Codes, B-Codes, P-Codes, S-Codes from ESA 2010
- glossary.md: Added FIGARO vs WIOD vs EXIOBASE comparison
- glossary.md: Added empirical reference values from our analysis
- research.md: Split Phase 2 into 2a (Base) and 2b (Extended)

**Output Summary:**
- Tables: 32 CSV files in outputs/tables/
- Figures: 7 PNG files in outputs/figures/
- Commits: 2 (Phase 2a, Phase 2b)

**Phase Status:**
- Phase 2 (Explore): Complete (both 2a and 2b)
- Phase 3 (Human-in-the-Loop): Ready to begin

---

### 2026-01-15 (Session 3) - Exploration Execution & Visualization

**Objective:** Run exploration scripts, generate visualizations, integrate domain knowledge

**Actions:**
- Executed all 4 exploration scripts (01-04)
- Fixed PyArrow filter bug: `base` partition requires `int(year)` not string
- Fixed DataFrame column access bug in sector dynamics (integer keys)
- Created output directory structure: `outputs/tables/` + `outputs/figures/`
- Generated 14 CSV tables and 4 PNG visualizations
- Integrated ESA 2010 reference documentation from Deep Research
- Applied constructive feedback: added nominal disclaimers, NACE codes in labels

**Empirical Findings:**

COVID-19 Impact (2019-2020):
| Country | HH Consumption | Gov Consumption |
|---------|----------------|-----------------|
| ES | -17.0% | +4.9% |
| GR | -16.1% | +3.0% |
| IT | -12.3% | +2.7% |
| AT | -10.1% | +3.9% |
| FR | -7.6% | +2.7% |
| DE | -7.1% | +7.2% |
| NL | -6.4% | +3.7% |
| PL | -4.7% | +4.4% |

Sektorale Asymmetrie (Germany):
- Verlierer: N79 Travel -56%, H51 Airlines -46%, I Hotels -32%
- Gewinner: Q86 Healthcare +22%, K66 Financial +14%, H53 Postal +11%

Energy Crisis (2021-2022):
- Nominale HH-Konsumanstiege 10-19% (Inflationseffekt, nicht real)
- GR +19%, AT/PL +17%, NL +16%, ES +16%

**Technical Learnings:**
- PyArrow Hive-partitions: Filter-Werte muessen zum Spaltentyp passen
- 70 Mio Zeilen performant mit partition pruning
- Seaborn diverging palette fuer pos/neg Visualisierung

**Files Created/Modified:**
- `scripts/02_top_flows.py` - Fixed int filter
- `scripts/03_temporal_analysis.py` - Fixed int filter and column keys
- `scripts/04_visualizations.py` - New visualization pipeline
- `outputs/tables/*.csv` - 14 data tables
- `outputs/figures/*.png` - 4 visualizations
- `knowledge/ESA 2010 und FIGARO Referenzdokumentation.md` - Domain knowledge

**Knowledge Gap Status:**
| Topic | Status |
|-------|--------|
| ESA 2010 Codes (D, B, P) | Closed - see Referenzdoku |
| Import dependency metrics | Closed - IPR, VS, FVASH documented |
| FIGARO vs WIOD vs EXIOBASE | Closed - comparison table |
| Core vs Periphery EU | Open - political definition |
| Deflators for real values | Open - external data needed |

**Phase Status:**
- Phase 2 (Explore): Complete

---

### 2026-01-15 (Session 2) - Use Case Analysis & Exploration Setup

**Objective:** Analyze David's use case requirements and prepare Phase 2 exploration

**Context:**
David Zenz provided the FIGARO-NAM data with a detailed 6-phase workflow specification for demonstrating agentic AI research capabilities.

**Key Discussion: Two Approaches**

We discussed two options for the workshop demo:
1. **Claude Code as Agent** - Use Claude Code directly for interactive analysis
2. **Custom Agent System** - Build a programmatic agent via API

Decision: **Option 1** - Claude Code is already an agent system. Building a custom system would add complexity, cost (API fees), and time without clear benefit for a demo.

**Domain Knowledge Gap Analysis**

Identified that we (Christopher + Claude) lack deep macroeconomic expertise. Categorized knowledge needs:

| Category | Can Answer from Data | Needs External Research |
|----------|---------------------|------------------------|
| Code meanings (D11, B2, etc.) | Partial - see values | Full definitions needed |
| Structural breaks | Yes - visible in data | Interpretation context |
| Import dependency | Yes - calculable | Standard metrics |
| Country clustering | Yes - technically | Economic interpretation |

**Actions:**
- Analyzed David's email specifying 6-phase workflow
- Mapped FIGARO-NAM data to circular flow concept (Production -> Income -> Distribution -> Use)
- Identified matrix block structure (Products x Industries, Transactions x Sectors)
- Tested COVID structural break: DE household consumption -7% (2019-2020)
- Created `scripts/` folder for Phase 2 exploration
- Started `01_data_quality.py`

**Technical Findings (Germany 2020):**
- Domestic flows: 40.3 trillion EUR (97%)
- Foreign flows: 1.1 trillion EUR (3%)
- Top import partners: WRL_REST, USA, China, France
- COVID impact visible: Travel agencies -56%, Airlines -46%, Hotels -32%
- Growth sectors: Healthcare +22%, Logistics +11%

**Files Created:**
- `scripts/01_data_quality.py` - Coverage, missing values, distributions

**Next Steps:**
- Complete exploration scripts (02, 03)
- Run scripts and save outputs
- Formulate Deep Research prompt for ESA 2010 / FIGARO methodology
- Prepare candidate research questions for Phase 3

---

### 2026-01-15 (Session 1) - Initial Data Inspection & Setup

**Objective:** Understand data structure, set up repository, document in knowledge base

**Actions:**
- Analyzed all 700 parquet files in `data/parquet/`
- Extracted schema: 6 columns (Set_i, m, Set_j, value, base, ctr)
- Documented 181 unique codes for Set_i/Set_j
- Categorized codes: CPA products (64), NACE industries (64), National Accounts (D, B, P, F, S, N codes)
- Identified 50 countries/regions including WRL_REST aggregate
- Created `.gitignore` to exclude data folder (191 MB)
- Created `CLAUDE.md` for AI assistant instructions
- Optimized all markdown files (README, research, requirements, journal, data)
- Removed emojis per user preference

**Observations:**
- Data is complete: 14 years x 50 countries = 700 files
- ~120,000 rows per file representing bilateral economic flows
- Values range from -9,750 to 151,292 (billion EUR)
- Negative values (283 in sample) represent adjustments/balancing items
- Hive-style partitioning optimal for filtered queries

**Files Created/Modified:**
- `CLAUDE.md` - AI assistant instructions
- `knowledge/data.md` - Complete schema and code documentation
- `knowledge/research.md` - Workflow phases with status tracking
- `knowledge/requirements.md` - Technical setup guide
- `knowledge/journal.md` - This file
- `README.md` - Project overview with Quick Start
- `.gitignore` - Exclude data folder

**Phase Status:**
- Phase 1 (Inspect/Understand): Complete

---

## Knowledge Status

### Resolved Topics (documented in glossary.md)

| Topic | Status | Location |
|-------|--------|----------|
| ESA 2010 D-Codes (D.11, D.12, D.21X31, etc.) | Documented | glossary.md |
| ESA 2010 B-Codes (B.2, B.3, B.8, B.9) | Documented | glossary.md |
| ESA 2010 P-Codes (P.3, P.51G, P.6, P.7) | Documented | glossary.md |
| ESA 2010 S-Codes (Institutional Sectors) | Documented | glossary.md |
| Import dependency metrics (IPR, VS, FVASH) | Documented | glossary.md |
| FIGARO vs WIOD vs EXIOBASE | Documented | glossary.md |
| Structural break definition | Documented | glossary.md |

### Open Topics

| Topic | Status | Notes |
|-------|--------|-------|
| Core vs Periphery EU | Open | Political/economic definition needed |
| Deflators for real values | Open | External Eurostat data required |
| Country clustering methodology | Open | For Phase 4/5 if selected |

---

## Template for New Entries

### [YYYY-MM-DD] - Session Title

**Objective:**
*What we set out to accomplish*

**Actions:**
*What was done (bullet points)*

**Observations:**
*What we learned or discovered*

**Files Created/Modified:**
*List of files with brief description*

**Next Steps:**
*What remains to be done*

---
