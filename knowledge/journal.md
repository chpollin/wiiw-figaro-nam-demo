# Working Journal: FIGARO-NAM Analysis

This journal documents the collaboration between Christopher Pollin and Claude Code (Opus 4.5) during the development of an agentic workflow for macroeconomic data analysis.

**Project:** wiiw-figaro-nam-demo
**Workshop:** AI for Data Analysis & Visualisation (wiiw, 10 February 2026)
**Data Provider:** David Zenz (wiiw)

---

## Session Log

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

## Pending Deep Research Topics

The following questions require external research (ESA 2010 Manual, Eurostat documentation):

1. **ESA 2010 Transaction Codes**
   - D11 vs D12 (wages vs employer contributions)
   - D21X31 (taxes minus subsidies on products)
   - B2 vs B3 (operating surplus vs mixed income)
   - B8_S* (saving by institutional sector)
   - B9FX9 (net lending/borrowing)

2. **Methodological Standards**
   - How is import dependency typically measured?
   - What defines a "structural break" in national accounts?
   - Standard approaches for country clustering by economic structure

3. **Context Knowledge**
   - FIGARO vs WIOD vs EXIOBASE - differences?
   - Core vs periphery EU countries - standard definition?

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
