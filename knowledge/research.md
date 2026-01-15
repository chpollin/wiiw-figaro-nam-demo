# Research Documentation: FIGARO-NAM Analysis

## Research Context

Macroeconomic analysis of National Accounts data to understand economic structures, sectoral linkages, and temporal dynamics across European and global economies.

**Data scope:** 50 countries, 14 years (2010–2023), ~84 million data points

---

## Workflow Phases

```mermaid
graph TB
    P1[Phase 1: Inspect] -->|data.md| P2[Phase 2: Explore]
    P2 -->|candidates| P3[Phase 3: Human-in-Loop]
    P3 -->|selected| P4[Phase 4: Plan]
    P4 -->|notebook| P5[Phase 5: Execute]
    P5 -->|outputs| P6[Phase 6: Summary]
```

| Phase | Status | Output |
|-------|--------|--------|
| 1. Inspect/Understand | Complete | `data.md` with schema, codes |
| 2a. Explore (Base) | Complete | `scripts/01-04*.py`, base outputs |
| 2b. Explore (Extended) | Complete | `scripts/05-08*.py`, extended outputs |
| 3. Human-in-the-Loop | Pending | Selected questions |
| 4. Plan | Pending | Notebook outline |
| 5. Execute | Pending | Analysis outputs |
| 6. Summary | Pending | Final report |

---

### Phase 1: Inspect/Understand [Complete]

**Objective:** Establish comprehensive understanding of data structure and content.

**Completed tasks:**
- [x] Load partitioned Parquet data
- [x] Infer schema and variable types
- [x] Generate data dictionary with descriptions
- [x] Document code lists (181 codes for Set_i/Set_j)
- [x] Identify 50 countries, 14 years coverage

**Outputs:**
- [data.md](data.md) – Complete variable documentation
- Schema: `Set_i`, `m`, `Set_j`, `value`, `base`, `ctr`

---

### Phase 2a: Explore - Base [Complete]

**Objective:** Assess data quality and identify analysis opportunities.

**Scripts created:**

| Script | Purpose | Status |
|--------|---------|--------|
| `scripts/01_data_quality.py` | Coverage, missing values, distributions | Executed |
| `scripts/02_top_flows.py` | Top flows, sectors, trade partners | Executed |
| `scripts/03_temporal_analysis.py` | Time series, structural breaks | Executed |
| `scripts/04_visualizations.py` | Heatmaps, bar charts, time series | Executed |

**Data Quality Results:**
- 69.8 million rows total across 700 country-year files
- Complete coverage: all 50 countries x 14 years present
- 204,488 negative values (adjustments/balancing items)
- No missing values

**Key Empirical Findings:**

COVID-19 Impact (2019-2020):
| Country | HH Consumption | Gov Consumption |
|---------|----------------|-----------------|
| ES | -17.0% | +4.9% |
| GR | -16.1% | +3.0% |
| IT | -12.3% | +2.7% |
| DE | -7.1% | +7.2% |
| PL | -4.7% | +4.4% |

Sektorale Asymmetrie (Germany):
- Verlierer: N79 Travel -56%, H51 Airlines -46%, I Hotels -32%
- Gewinner: Q86 Healthcare +22%, K66 Financial +14%, H53 Postal +11%

Energy Crisis (2021-2022):
- Nominale HH-Konsumanstiege 10-19% (Inflationseffekt)
- Interpretation erfordert externe Deflator-Daten

**Outputs Phase 2a:**
- `outputs/tables/` - 15 CSV data files
- `outputs/figures/` - 4 PNG visualizations

---

### Phase 2b: Explore - Extended [Complete]

**Objective:** Deeper analysis with baseline trends, export structure, and IO linkages.

**Scripts created:**

| Script | Purpose | Status |
|--------|---------|--------|
| `scripts/05_baseline_trend.py` | CAGR 2010-2018, trend deviation analysis | Executed |
| `scripts/06_export_analysis.py` | Export structure, trade balance by partner | Executed |
| `scripts/07_negative_values.py` | Categorize negative values in dataset | Executed |
| `scripts/08_io_linkages.py` | Intersectoral linkages, backward/forward | Executed |

**Key Findings Phase 2b:**

Trend Deviation Analysis (COVID vs. CAGR 2010-2018):
| Country | HH Cons Deviation from Trend |
|---------|------------------------------|
| ES | -18.1% |
| IT | -13.8% |
| AT | -12.3% |
| GR | -11.2% |
| DE | -9.7% |

Intersectoral Linkages (Germany 2019):
- Highest backward linkage: Motor vehicles, Construction, Machinery
- Highest forward linkage: Legal/Accounting (M69_70), Real estate (L), Wholesale (G46)
- Total intermediate consumption: 2.5 billion EUR (domestic flows)

Export Structure (Germany 2019):
- Top destinations: US (9.8%), CN (9.6%), FR (8.1%), NL (7.6%)
- Top categories: Services (33%), Manufacturing other (23%), Vehicles (11%)

Negative Values Analysis:
- ~36k negative values in 8-country sample (14 years)
- Mainly B-Balances (adjustments) and D-Transactions (subsidies > taxes)
- Legitimate ESA 2010 accounting entries, not errors

**Outputs Phase 2b:**
- `outputs/tables/` - 17 additional CSV files (32 total)
- `outputs/figures/` - 3 additional PNG visualizations (7 total)

**Knowledge Documentation:**
- `knowledge/glossary.md` - IO analysis and econometrics terminology
- `knowledge/exploration_plan.md` - Planning document for Phase 2b

---

### Phase 3: Human-in-the-Loop

**Objective:** Collaborative selection of research questions.

**Selection matrix:**

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Feasibility | High | Can be answered with available data |
| Interpretability | High | Results are meaningful to stakeholders |
| Relevance | Medium | Policy or academic significance |
| Novelty | Low | Adds to existing knowledge |

**Process:**
1. Review Phase 2 candidates
2. Score against criteria
3. Select 2–3 questions for implementation

---

### Phase 4: Plan

**Objective:** Transform research questions into reproducible workflows.

**Notebook structure:**

```
1. Setup & Data Loading
2. Data Preparation
3. Analysis
4. Visualization
5. Interpretation
6. Limitations
```

**For each question, define:**
- Data filters (countries, years, sectors)
- Aggregation method
- Metrics to compute
- Visualization types
- Validation checks

---

### Phase 5: Execute

**Objective:** Implement analysis pipeline and generate outputs.

**Potential output types:**

| Type | Description | Tools |
|------|-------------|-------|
| **Sankey/Flow** | Income generation → distribution → use | plotly, networkD3 |
| **Structural Breaks** | COVID (2020), Energy crisis (2022) | scipy, statsmodels |
| **Clustering** | Country typologies by structure | scikit-learn |
| **Import Dependency** | Sectoral external exposure | pandas aggregation |

---

### Phase 6: Summary

**Objective:** Synthesize findings with appropriate epistemic framing.

**Structure:**

| Section | Content |
|---------|---------|
| Key findings | Direct observations from data |
| Interpretations | What this might mean |
| Limitations | Data constraints, caveats |
| Next steps | Hypotheses for future work |

**Epistemic markers:**
- **[FACT]** Direct data observation
- **[INFERENCE]** Interpretation requiring assumptions
- **[HYPOTHESIS]** Question for future investigation

---

## Candidate Research Questions

*To be refined during Phase 2/3*

| # | Question | Feasibility | Data Requirements |
|---|----------|-------------|-------------------|
| 1 | How has sectoral GDP composition changed across EU since 2010? | High | Set_i industries, value by year |
| 2 | Which sectors show highest import dependency? | High | m (partner), Set_i products |
| 3 | What structural breaks occurred 2020–2022? | Medium | Time series, change detection |
| 4 | Can countries be clustered by economic structure? | Medium | Cross-country comparison |
| 5 | How do core vs. peripheral EU economies differ? | Medium | Pre-defined country groups |

---

## Methodological Notes

### Promptotyping Approach

| Principle | Application |
|-----------|-------------|
| Context Engineering | `knowledge/` folder with structured docs |
| Iterative Development | Track progress in `journal.md` |
| Human-in-the-Loop | Phase 3 decision point |
| Reproducibility | Notebook-based workflows |

### Quality Assurance

- [ ] Cross-validate against Eurostat published aggregates
- [ ] Plausibility checks (GDP totals, known economic events)
- [ ] Document all assumptions and transformations
- [ ] Peer review of interpretation claims

### Key References

- [Eurostat FIGARO](https://ec.europa.eu/eurostat/web/esa-supply-use-input-tables/figaro)
- [NACE Rev. 2 Classification](https://ec.europa.eu/eurostat/web/nace-rev2)
- [CPA 2.1 Classification](https://ec.europa.eu/eurostat/web/cpa)
- [ESA 2010 und FIGARO Referenzdokumentation](ESA%202010%20und%20FIGARO%20Referenzdokumentation.md) - Local domain knowledge
