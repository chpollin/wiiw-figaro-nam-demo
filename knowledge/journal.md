# Working Journal: FIGARO-NAM Analysis

This journal documents the collaboration between Christopher Pollin and Claude Code (Opus 4.5) during the development of an agentic workflow for macroeconomic data analysis.

**Project:** wiiw-figaro-nam-demo
**Workshop:** AI for Data Analysis & Visualisation (wiiw, 10 February 2026)
**Data Provider:** David Zenz (wiiw)

---

## Session Log

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
