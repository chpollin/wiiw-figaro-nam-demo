# Glossary: Input-Output Analysis and Econometrics

This glossary defines central concepts for working with FIGARO-NAM data and input-output analysis.

---

## Fundamentals of Input-Output Analysis

### Transaction Matrix (Z-Matrix)
Matrix of intersectoral deliveries. Element z_ij indicates the value of deliveries from sector i to sector j. Basis for calculating technical coefficients.

### Technical Coefficients (A-Matrix)
Direct input coefficients. Element a_ij = z_ij / x_j indicates the direct input from sector i per unit of output in sector j. Shows immediate intermediate consumption linkages.

### Leontief Inverse (L-Matrix)
The matrix (I - A)^(-1), where I is the identity matrix and A is the matrix of technical coefficients. Captures both direct and indirect effects of demand changes on production across all sectors.

### Output Multiplier
Sum of a column of the Leontief inverse. Indicates how much total economic output increases when final demand in a sector increases by one unit.

### Final Demand
Final use of goods: consumption (private and government), investment, exports. In contrast to intermediate consumption, which feeds back into production.

### Intermediate Consumption
Goods and services consumed or transformed in the production process. Form the rows/columns of the Z-matrix.

### Gross Value Added (GVA)
Output minus intermediate consumption. Corresponds to the value newly created in the production process. Sum of compensation of employees, operating surplus, and production taxes net.

### Backward Linkage
Column sum of the Leontief inverse. Measures how strongly a sector sources intermediate inputs from other sectors. High values for manufacturing industries.

### Forward Linkage
Row sum of the Ghosh inverse or output coefficients. Measures how strongly a sector supplies other sectors. High values for basic industries and energy.

---

## Econometric Fundamentals

### Structural Break
Significant change in the parameters of a statistical model at a specific point in time. In the FIGARO context: COVID-19 (2020), Energy crisis (2022).

### CAGR (Compound Annual Growth Rate)
Average annual growth rate over a period: CAGR = (End Value/Start Value)^(1/n) - 1

### Herfindahl-Hirschman Index (HHI)
Concentration measure. Sum of squared market shares. Values from 0 (perfect dispersion) to 1 (monopoly). EU threshold for strategic dependency: 0.4

### Import Penetration Ratio (IPR)
Share of imports in domestic demand: IPR = M / (GDP - X + M). Values above 50% signal high import dependency.

### Vertical Specialization (VS)
Share of imported intermediate inputs in exports. Quantifies integration in global value chains.

---

## National Accounts

### GDP (Gross Domestic Product)
Sum of all goods and services produced domestically minus intermediate consumption. Three calculation approaches: production, income, expenditure.

### System of National Accounts (SNA)
System for consistent recording of all economic transactions in an economy. Standardized in the EU according to ESA 2010.

### ESA 2010
European System of Accounts 2010. EU-wide standard for national accounts. Defines transaction codes (D), balances (B), expenditure (P), sectors (S).

---

## FIGARO-Specific Terms

### FIGARO
Full International and Global Accounts for Research in Input-Output Analysis. Official EU statistics for Multi-Regional Input-Output Tables since 2021.

### Set_i / Set_j
Dimensions of the FIGARO-NAM Matrix. Set_i: Origin (Products by CPA, Transactions by ESA). Set_j: Use (Industries by NACE, Sectors by ESA).

### m (Partner)
Partner country in bilateral flows. Domestic production when m = ctr (reporting country).

### base
Base year of the data (2010-2023 available).

### ctr
Reporting country (50 countries/regions including WRL_REST).

### WRL_REST
Rest of the World - Aggregate for all countries not individually captured.

---

## Mapping: FIGARO Codes to Concepts

| Concept | FIGARO Code | Description |
|---------|-------------|-------------|
| Intermediate consumption | CPA products x NACE industries | Z-matrix block |
| Final demand | Set_j = P3_S14, P3_S13, P51G, P6 | Consumption, investment, exports |
| Value added | Set_i = D1, D29X39, B2, B3 | Components of GVA |
| Imports | m != ctr | Foreign deliveries |
| Exports | P6 in Set_j | Deliveries abroad |

---

## Abbreviations

| Abbreviation | Meaning |
|--------------|---------|
| CAGR | Compound Annual Growth Rate |
| CPA | Classification of Products by Activity |
| ESA | European System of Accounts |
| FIGARO | Full International and Global Accounts for Research in IO |
| GVA | Gross Value Added |
| HHI | Herfindahl-Hirschman Index |
| IO | Input-Output |
| IPR | Import Penetration Ratio |
| MRIO | Multi-Regional Input-Output |
| NACE | Statistical Classification of Economic Activities |
| NAM | National Accounts Matrix |
| NPISH | Non-Profit Institutions Serving Households |
| PPP | Purchasing Power Parity |
| SNA | System of National Accounts |
| SUT | Supply and Use Tables |
| TiVA | Trade in Value Added |
| VS | Vertical Specialization |
| YoY | Year-over-Year |

---

## ESA 2010 Transaction Codes (D-Codes)

### Compensation of Employees (D.1)

**D.11 - Wages and Salaries**
All cash and in-kind payments to employees. Cash payments: base salaries, overtime, bonuses, 13th/14th month salaries. In-kind payments: company cars, subsidized housing, employee shares.

**D.12 - Employers' Social Contributions**
Actual contributions to social insurance (D.121) and imputed social contributions for direct employer benefits (D.122), e.g., direct pension commitments.

### Net Items

**D.21X31 - Taxes minus Subsidies on Products**
Central transition item from gross value added to GDP at market prices. Includes VAT, import duties, excise taxes minus product subsidies like agricultural price support or housing subsidies.

**D.29X39 - Other Taxes minus Subsidies on Production**
Property taxes, business license fees minus wage subsidies, interest subsidies. Negative values: subsidies exceed taxes.

### Property Income (D.4)

| Code | Name |
|------|------|
| D.41 | Interest |
| D.42 | Dividends and withdrawals from income of quasi-corporations |
| D.43 | Reinvested earnings on foreign direct investment |
| D.44 | Investment income attributable to insurance policy holders |
| D.45 | Rent (land, mineral resources) |

### Other D-Codes

| Code | Name |
|------|------|
| D.5 | Current taxes on income and wealth |
| D.61 | Net social contributions |
| D.62 | Social benefits other than transfers in kind (pensions, unemployment benefits, child benefits) |
| D.7 | Other current transfers |
| D.8 | Adjustment for change in pension entitlements |
| D.9 | Capital transfers |

---

## ESA 2010 Balance Items (B-Codes)

**B.1g - Gross Value Added**
Output minus intermediate consumption. Central measure for productivity measurement.

**B.2 - Operating Surplus**
Accrues to corporations. Calculation: B.1g - D.1 - (D.29-D.39). Corresponds to profit before property income.

**B.3 - Mixed Income**
Only for household sector (S.14). Inseparable mix of labor compensation and capital return for sole proprietorships, freelancers, farmers.

**B.8 - Saving by Sector**

| Sector | Interpretation |
|--------|----------------|
| S.11 (Corporations) | Retained earnings after dividends |
| S.13 (Government) | Primary surplus/deficit |
| S.14 (Households) | Classic saving for wealth accumulation |

**B.9 - Net Lending/Borrowing**
Positive: Sector provides funds. Negative: Sector needs funds.
Formula: B.9 = B.8 + Capital transfers - Gross investment

**B9FX9** - Statistical discrepancy between real economy B.9 and B.9F from financial account.

---

## ESA 2010 Expenditure Codes (P-Codes)

**P.3 - Final Consumption Expenditure**

| Sector | Content |
|--------|---------|
| P3_S13 | Government consumption (collective + individually attributable) |
| P3_S14 | Private household consumption |
| P3_S15 | NPISH consumption (churches, associations, parties) |

**P.51G - Gross Fixed Capital Formation (GFCF)**
Acquisitions less disposals of fixed assets: buildings, machinery, software, R&D, intellectual property.

**P.6 - Exports**
Deliveries of goods and services to non-residents.

**P.7 - Imports**
Acquisitions of goods and services from non-residents.

---

## ESA 2010 Institutional Sectors (S-Codes)

**S.11 - Non-financial Corporations**
Market producers of goods and non-financial services.

**S.12 - Financial Corporations**
Financial intermediation: banks (S.122), insurance (S.128), pension funds (S.129).

**S.13 - General Government**
Central government (S.1311), state government (S.1312), local government (S.1313), social security funds (S.1314).

**S.14 - Households**
Consumers and small producers. Only sector with B.3 (Mixed Income).

**S.15 - NPISH**
Non-Profit Institutions Serving Households. Churches, parties, unions, associations.

**S.2 - Rest of World**
All non-resident units. Disaggregated by country in FIGARO.

---

## FIGARO Methodology

### Comparison with Other MRIO Databases

| Feature | FIGARO | WIOD | EXIOBASE |
|---------|--------|------|----------|
| Publisher | Eurostat/JRC (official) | University of Groningen | Academic |
| Time series | 2010-2022, annual | 2000-2014, discontinued | 1995-current |
| Sectors | 64 NACE Rev. 2 | 56 ISIC Rev. 4 | 163 industries |
| NA consistency | Complete (99.8% EU GDP) | Benchmarked | Estimated |

### QDR Methodology
FIGARO's distinctive feature: Bilateral trade balancing at HS-6-digit level through weighted averaging of country-specific asymmetries.

### Known Limitations
- Sectoral aggregation: 64 industries limits precise analyses
- Rest of World: Only export/import vectors, no complete SUTs
- Time lag: T-2 years
- Validation deviations: WAPE to OECD-ICIO ~34%, to EXIOBASE ~83%

---

## Empirical Reference Values from FIGARO-NAM

### COVID-19 Structural Break (2019-2020)
| Country | HH Consumption YoY | Trend Deviation |
|---------|-------------------|-----------------|
| ES | -17.0% | -18.1% |
| GR | -16.1% | -11.2% |
| IT | -12.3% | -13.8% |
| DE | -7.1% | -9.7% |

### Sectoral Winners/Losers (DE 2020)
- Losers: N79 Travel (-56%), H51 Airlines (-46%), I Hotels (-32%)
- Winners: Q86 Healthcare (+22%), K66 Financial (+14%)

### Intersectoral Linkages (DE 2019)
- Highest backward linkage: Motor vehicles, Construction, Machinery
- Highest forward linkage: Legal/Accounting, Real Estate, Wholesale

---

## Web Dashboard Architecture

### Technology Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Visualization | D3.js v7 | Maximum flexibility, professional charts |
| Styling | Vanilla CSS | No dependencies, simple |
| Data format | JSON | Browser-native, compact |
| Hosting | GitHub Pages | Static, free |

### Dashboard Structure

```
docs/
├── index.html          # Main HTML with tab navigation
├── css/style.css       # Responsive styling
├── js/
│   ├── app.js          # Data loading, helper functions
│   ├── timeseries.js   # Multi-line chart
│   ├── trade.js        # Bar chart
│   ├── sectors.js      # Diverging bar chart
│   └── linkages.js     # IO linkages
└── data/
    ├── time_series.json
    ├── trade_partners.json
    ├── sectors.json
    ├── linkages.json
    └── metadata.json
```

### JSON Data Aggregation

**Source:** CSV files from `outputs/tables/` (Phase 2 Exploration)
**Generator:** `scripts/09_generate_json.py`
**Target:** `docs/data/*.json` (~47 KB total)

### D3.js Visualization Types

| Chart | D3 Method | Data |
|-------|-----------|------|
| Time series | `d3.line()` + `d3.curveMonotoneX` | time_series.json |
| Trade | `d3.scaleBand()` + `rect` | trade_partners.json |
| Sectors | Diverging bars (pos/neg around 0) | sectors.json |
| Linkages | `d3.scaleSequential()` + `d3.interpolateBlues` | linkages.json |

### Interactive Elements

- **Tooltips:** `d3.select('body').append('div').attr('class', 'tooltip')`
- **Checkboxes:** Country selection for multi-line comparison
- **Dropdowns:** Aggregate selection, mode selection
- **Slider:** Top-N selection for rankings
- **Buttons:** Year selection for structural breaks

### Crisis Markers

| Year | Name | Visualization |
|------|------|---------------|
| 2020 | COVID-19 | Vertical dashed line |
| 2022 | Energy crisis | Vertical dashed line |

---

## References

- ESA 2010 Manual: Regulation EU No 549/2013
- Miller & Blair: Input-Output Analysis, 3rd Edition 2022
- OECD TiVA Database Documentation
- Eurostat FIGARO Methodology Notes
- D3.js Documentation: https://d3js.org/
- Local Reference: [ESA 2010 and FIGARO Reference Documentation](ESA%202010%20and%20FIGARO%20Reference%20Documentation.md)
