# ESA 2010 and FIGARO Reference Documentation

This document synthesizes the foundational knowledge for working with the FIGARO-NAM dataset. It serves as a reference for transaction codes, sector definitions, methodological specifics, and analysis indicators.

---

## Transaction Codes (D-Classification)

The D-codes classify distributive transactions in the European System of Accounts 2010.

### Compensation of Employees (D.1)

**D.11 - Wages and Salaries**
Encompasses all cash and in-kind payments to employees. Cash payments include base salaries, overtime supplements, bonuses, and 13th/14th month salaries. In-kind payments include company cars, subsidized products, staff housing, and employee shares.

**D.12 - Employers' Social Contributions**
Divided into actual contributions to social insurance carriers (D.121) and imputed social contributions for direct employer benefits without insurance intermediation (D.122), such as direct company pension commitments.

### Net Items (Taxes minus Subsidies)

**D.21X31 - Taxes minus Subsidies on Products**
Central transition item from gross value added to GDP at market prices. Includes value added tax, import duties, excise taxes minus product subsidies such as agricultural price support or housing subsidies.

**D.29X39 - Other Taxes minus Subsidies on Production**
Appears in the generation of income account at industry and sector level. Includes property taxes on business premises, business license fees, vehicle taxes for company vehicles minus wage subsidies, loss compensation, and interest subsidies. Negative values in the dataset indicate that subsidies exceed taxes.

### Property Income (D.4)

Compensation for providing financial and non-financial assets.

| Code | Name | Content |
|------|------|---------|
| D.41 | Interest | Compensation for deposits, loans, bonds |
| D.42 | Dividends and withdrawals | Dividends, profit withdrawals from quasi-corporations |
| D.43 | Reinvested earnings | From foreign direct investment |
| D.44 | Investment income from insurance | Capital returns of insurance policyholders |
| D.45 | Rent | Compensation for natural resources (land, mineral deposits) |

### Other Distributive Transactions

| Code | Name | Content |
|------|------|---------|
| D.5 | Current taxes on income and wealth | Income tax, corporate tax, capital gains tax |
| D.61 | Net social contributions | Employer and employee contributions to social insurance |
| D.62 | Social benefits other than transfers in kind | Pensions, unemployment benefits, sickness benefits, child benefits |
| D.7 | Other current transfers | Insurance premiums and benefits, EU own resources, development aid |
| D.8 | Adjustment for change in pension entitlements | Adjustment for pension provisions |
| D.9 | Capital transfers | Inheritance tax, investment grants, debt cancellation |

---

## Balance Items (B-Classification)

The B-codes represent account balances with sector-specific interpretation.

### Operating Surplus and Mixed Income

**B.2 - Operating Surplus**
Accrues to corporations where owner compensation is separately recorded as D.1. Corresponds to profit before property income.

Calculation: B.2 = Gross Value Added (B.1g) - Compensation of Employees (D.1) - Other Taxes on Production net (D.29-D.39)

**B.3 - Mixed Income**
Reserved for sole proprietorships in the household sector (S.14), where labor compensation and capital return are inseparably mixed. Typical for craftsmen, freelancers, agricultural enterprises.

### Saving by Sector (B.8)

Saving has a specific economic meaning for each institutional sector.

| Sector | Code | Interpretation |
|--------|------|----------------|
| Non-financial Corporations | S.11 | Retained earnings after dividends and taxes. Internal financing source for investment. |
| Financial Corporations | S.12 | Retained earnings from financial intermediation. Often low due to high payout ratios. |
| Government | S.13 | Primary surplus or deficit after transfers. Negative value signals deficit in current expenditure. |
| Households | S.14 | Classic saving. Non-consumed income for wealth accumulation and retirement provision. |
| NPISH | S.15 | Surplus or deficit after fulfilling transfer function. Usually marginal. |

### Net Lending/Borrowing (B.9)

Shows whether a sector provides funds net (Net Lending, positive) or requires them (Net Borrowing, negative).

Calculation: B.9 = Saving (B.8) + Capital transfers received - Capital transfers paid - Gross investment

**B9FX9** captures the statistical discrepancy between the real economy B.9 and the B.9F derived from the financial account. Theoretically identical, practically divergent due to measurement errors.

---

## Expenditure Codes (P-Classification)

### Gross Fixed Capital Formation (P.51G)

Acquisitions less disposals of fixed assets. Includes buildings and structures, equipment and machinery, intellectual property (R&D, software, databases), cultivated biological resources, and costs of ownership transfer (notary fees, broker commissions).

Net fixed capital formation (P.51N) is obtained after deducting consumption of fixed capital (P.51C).

### Final Consumption Expenditure (P.3)

Expenditure for need satisfaction, distributed by sector.

| Sector | Content |
|--------|---------|
| Government (S.13) | Collective services (defense, administration) and individually attributable services (education, health) |
| Households (S.14) | Private consumption for goods and services |
| NPISH (S.15) | Services from churches, parties, associations, unions |

---

## Institutional Sectors (S-Classification)

### Domestic Sectors

**S.11 - Non-financial Corporations**
Market producers of goods and non-financial services. Subsectors by control: publicly controlled (S.11001), nationally privately controlled (S.11002), foreign controlled (S.11003).

**S.12 - Financial Corporations**
Financial intermediation and ancillary services. Nine subsectors from central bank (S.121) through credit institutions (S.122) to pension funds (S.129).

**S.13 - General Government**
Four levels: federal (S.1311), state (S.1312), local (S.1313), social security (S.1314). Produces mainly non-market goods and performs redistribution.

**S.14 - Households**
Persons or groups of persons as consumers and as producers (sole proprietorships, self-employed). Only sector with mixed income (B.3).

**S.15 - Non-Profit Institutions Serving Households (NPISH)**
Churches, political parties, unions, associations, foundations. Produce non-market goods for households.

### Rest of World

**S.2 - Rest of the World**
Aggregates all non-resident units for cross-border transactions. Disaggregated by country in FIGARO.

---

## FIGARO-Specific Methodology

### Positioning in Comparison

FIGARO (Full International and Global Accounts for Research in Input-Output Analysis) has been the only official EU statistic for Multi-Regional Input-Output Tables since 2021.

| Feature | FIGARO | WIOD | EXIOBASE 3 |
|---------|--------|------|------------|
| Publisher | Eurostat/JRC (official) | University of Groningen | Academic consortium |
| Time series | 2010-2022, annually updated | 2000-2014, discontinued | 1995-current, irregular |
| Sectors | 64 NACE Rev. 2 | 56 ISIC Rev. 4 | 163 industries x 200 products |
| NA consistency | Complete (99.8% EU GDP) | Benchmarked with deviations | Estimated |
| Environmental extensions | CO2 separate | Socio-economic satellites | Extensive |
| Trade balancing | QDR methodology | Mirror flows | Estimated reconciliation |

### QDR Methodology

FIGARO's methodological unique feature for bilateral trade balancing. Resolves trade asymmetries at HS-6-digit level through weighted averaging considering country-specific export and import asymmetries.

### Construction Process

The construction goes through four phases.

1. Harmonization of national Supply-Use Tables to NACE/CPA classification
2. Bilateral trade balancing using QDR
3. Benchmarking to national accounts aggregates for 45 countries plus Rest of World
4. Transformation into Input-Output tables using Model B (Industry Technology Assumption) or Model D (Fixed Product Sales Structure)

### Known Limitations

**Sectoral aggregation:** 64 industries limit precise environmental footprint analyses. A single agricultural sector for heterogeneous products complicates differentiated assessments.

**Rest of World modeling:** Only export/import vectors instead of complete SUT matrices for non-EU countries.

**Time lag:** T-2 years. Current projections are based on previous SUT structures.

**Validation deviations:** WAPE between FIGARO and OECD-ICIO is 34%, between FIGARO and EXIOBASE 83%. Differences result from different data sources and balancing methods.

**Country-specific limitations:** Estimated SUTs for non-EU countries, difficult-to-capture service trade, manual adjustments for Brazil, Russia, UK.

### Extensions

**FIGARO-E3:** Disaggregation to 176 industries x 213 products with labor and energy extensions.

**FIGARO-REG:** Regional resolution to 240 EU NUTS2 regions.

---

## Indicators for Import Dependency

### Import Penetration Ratio

Share of domestic demand satisfied by imports.

Formula: IPR = M / (GDP - X + M) x 100

Applicable at sector or product level. Values above 50% signal high import dependency.

### Vertical Specialization Index

Share of imported intermediate inputs in exports. Quantifies backward linkages in global value chains.

According to Hummels, Ishii & Yi (2001): VS = imported intermediate inputs in exports / gross exports

### Foreign Value Added Share (EXGR_FVASH)

OECD TiVA indicator for foreign value added content in gross exports.

Empirical reference values: industrialized countries 20-30%, small open economies over 40%.

### EU Commission Thresholds

Definition of strategic dependencies via three criteria.

1. Herfindahl-Hirschman Index above 0.4 for import concentration
2. Import share above 50% of total demand
3. Qualitatively low substitutability

This methodology identified 137 dependent products in 2021, and 204 products in sensitive ecosystems in 2023 with improved FIGARO-based methodology.

---

## Normalization Methods for Country Comparisons

The method choice depends on the analysis objective.

### Per Capita Normalization

Suitable for living standard and welfare comparisons. Denominator is mean annual population. Distortions possible with different age structures or labor force participation rates.

### GDP Share Calculation

Formula: Indicator / GDP x 100

Standardizes for economic size. Standard for trade openness and relative dependency measures. Small countries reach values above 100% through re-exports, large countries like the USA typically only 25%.

### Purchasing Power Parity (PPP)

Appropriate for comparisons of real purchasing power and living standards. Not suitable for trade flows as these occur at market prices.

Data sources: Eurostat-OECD PPP Programme (annually for 36+ European countries), World Bank ICP (every three years globally).

### Recommendations by Comparison Purpose

| Purpose | Method |
|---------|--------|
| Living standard | PPP per capita |
| Economic structure | Share of GDP |
| Trade linkages | EU=100 Index |
| Productivity | Per employed person |
| Time series analysis | Constant prices + PPP |

---

## Further Sources

**ESA 2010 Manual:** Regulation EU No 549/2013, available at ec.europa.eu/eurostat/esa2010

**FIGARO Documentation:** ec.europa.eu/eurostat/web/esa-supply-use-input-tables/figaro

**OECD TiVA Guide:** stats.oecd.org (Guide to OECD Trade in Value Added, 2023)

**Methodological Foundations:** Miller & Blair, Input-Output Analysis: Foundations and Extensions, 3rd Edition 2022
