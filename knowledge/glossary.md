# Glossar: Input-Output-Analyse und Oekonometrie

Dieses Glossar definiert zentrale Begriffe fuer die Arbeit mit FIGARO-NAM Daten und Input-Output-Analyse.

---

## Grundbegriffe der Input-Output-Analyse

### Transaktionsmatrix (Z-Matrix)
Matrix der intersektoralen Lieferungen. Element z_ij gibt den Wert der Lieferungen von Sektor i an Sektor j an. Basis fuer die Berechnung technischer Koeffizienten.

### Technische Koeffizienten (A-Matrix)
Direkte Inputkoeffizienten. Element a_ij = z_ij / x_j gibt den direkten Input aus Sektor i pro Einheit Output in Sektor j an. Zeigt unmittelbare Vorleistungsverflechtungen.

### Leontief-Inverse (L-Matrix)
Die Matrix (I - A)^(-1), wobei I die Einheitsmatrix und A die Matrix der technischen Koeffizienten ist. Erfasst sowohl direkte als auch indirekte Effekte von Nachfrageaenderungen auf die Produktion aller Sektoren.

### Output-Multiplikator
Summe einer Spalte der Leontief-Inversen. Gibt an, um wie viel die gesamtwirtschaftliche Produktion steigt, wenn die Endnachfrage in einem Sektor um eine Einheit zunimmt.

### Endnachfrage (Final Demand)
Letzte Verwendung von Guetern: Konsum (privat und staatlich), Investitionen, Exporte. Im Gegensatz zu Vorleistungen, die wieder in die Produktion eingehen.

### Vorleistungen (Intermediate Consumption)
Gueter und Dienstleistungen, die im Produktionsprozess verbraucht oder umgewandelt werden. Bilden die Zeilen/Spalten der Z-Matrix.

### Bruttowertschoepfung (Gross Value Added)
Output minus Vorleistungen. Entspricht der im Produktionsprozess neu geschaffenen Wertschoepfung. Summe aus Arbeitnehmerentgelt, Betriebsueberschuss und Produktionsabgaben netto.

### Rueckwaertsverflechtung (Backward Linkage)
Spaltensumme der Leontief-Inversen. Misst, wie stark ein Sektor Vorleistungen aus anderen Sektoren bezieht. Hohe Werte bei verarbeitender Industrie.

### Vorwaertsverflechtung (Forward Linkage)
Zeilensumme der Ghosh-Inversen oder Output-Koeffizienten. Misst, wie stark ein Sektor andere Sektoren beliefert. Hohe Werte bei Grundstoffindustrien und Energie.

---

## Oekonometrische Grundbegriffe

### Strukturbruch (Structural Break)
Signifikante Aenderung in den Parametern eines statistischen Modells zu einem bestimmten Zeitpunkt. Im FIGARO-Kontext: COVID-19 (2020), Energiekrise (2022).

### CAGR (Compound Annual Growth Rate)
Durchschnittliche jaehrliche Wachstumsrate ueber einen Zeitraum: CAGR = (Endwert/Anfangswert)^(1/n) - 1

### Herfindahl-Hirschman-Index (HHI)
Konzentrationsmass. Summe der quadrierten Marktanteile. Werte von 0 (perfekte Streuung) bis 1 (Monopol). EU-Schwelle fuer strategische Abhaengigkeit: 0.4

### Import Penetration Ratio (IPR)
Anteil der Importe an der inlaendischen Nachfrage: IPR = M / (BIP - X + M). Werte ueber 50% signalisieren hohe Importabhaengigkeit.

### Vertical Specialization (VS)
Anteil importierter Vorleistungen in Exporten. Quantifiziert Integration in globale Wertschoepfungsketten.

---

## Nationale Volkswirtschaftliche Gesamtrechnungen

### BIP (Bruttoinlandsprodukt)
Summe aller im Inland produzierten Waren und Dienstleistungen abzueglich Vorleistungen. Drei Berechnungsarten: Entstehung, Verteilung, Verwendung.

### Volkswirtschaftliche Gesamtrechnung (VGR)
System zur konsistenten Erfassung aller wirtschaftlichen Transaktionen einer Volkswirtschaft. In der EU nach ESA 2010 standardisiert.

### ESA 2010
European System of Accounts 2010. EU-weiter Standard fuer nationale Gesamtrechnungen. Definiert Transaktionscodes (D), Salden (B), Verwendung (P), Sektoren (S).

---

## FIGARO-spezifische Begriffe

### FIGARO
Full International and Global Accounts for Research in Input-Output Analysis. Offizielle EU-Statistik fuer Multi-Regional Input-Output Tables seit 2021.

### Set_i / Set_j
Dimensionen der FIGARO-NAM Matrix. Set_i: Herkunft (Produkte nach CPA, Transaktionen nach ESA). Set_j: Verwendung (Industrien nach NACE, Sektoren nach ESA).

### m (Partner)
Partnerland in bilateralen Stroemen. Inlandsproduktion wenn m = ctr (Berichtsland).

### base
Basisjahr der Daten (2010-2023 verfuegbar).

### ctr
Berichtsland (50 Laender/Regionen inklusive WRL_REST).

### WRL_REST
Rest der Welt - Aggregat fuer alle nicht einzeln erfassten Laender.

---

## Mapping: FIGARO-Codes zu Konzepten

| Konzept | FIGARO-Code | Beschreibung |
|---------|-------------|--------------|
| Vorleistungen | CPA-Produkte x NACE-Industrien | Z-Matrix Block |
| Endnachfrage | Set_j = P3_S14, P3_S13, P51G, P6 | Konsum, Investitionen, Exporte |
| Wertschoepfung | Set_i = D1, D29X39, B2, B3 | Komponenten der GVA |
| Importe | m != ctr | Auslaendische Lieferungen |
| Exporte | P6 in Set_j | Lieferungen ans Ausland |

---

## Abkuerzungsverzeichnis

| Abkuerzung | Bedeutung |
|------------|-----------|
| CAGR | Compound Annual Growth Rate |
| CPA | Classification of Products by Activity |
| ESA | European System of Accounts |
| FIGARO | Full International and Global Accounts for Research in IO |
| GVA | Gross Value Added |
| HHI | Herfindahl-Hirschman-Index |
| IO | Input-Output |
| IPR | Import Penetration Ratio |
| MRIO | Multi-Regional Input-Output |
| NACE | Nomenclature statistique des Activites economiques |
| NAM | National Accounts Matrix |
| NPISH | Non-Profit Institutions Serving Households |
| PPP | Purchasing Power Parity |
| SUT | Supply and Use Tables |
| TiVA | Trade in Value Added |
| VGR | Volkswirtschaftliche Gesamtrechnung |
| VS | Vertical Specialization |
| YoY | Year-over-Year |

---

## ESA 2010 Transaktionscodes (D-Codes)

### Arbeitnehmerentgelt (D.1)

**D.11 - Bruttoloehne und -gehaelter**
Alle Bar- und Sachleistungen an Arbeitnehmer. Barleistungen: Grundgehaelter, Ueberstunden, Praemien, 13./14. Monatsgehalt. Sachleistungen: Firmenwagen, Dienstwohnungen, Mitarbeiteraktien.

**D.12 - Sozialbeitraege der Arbeitgeber**
Tatsaechliche Beitraege an Sozialversicherung (D.121) und unterstellte Sozialbeitraege fuer direkte Arbeitgeberleistungen (D.122), z.B. betriebliche Pensionszusagen.

### Netto-Groessen

**D.21X31 - Guetersteuern minus Guetersubventionen**
Zentrale Uebergangsgroesse von Bruttowertschoepfung zum BIP. Enthaelt MwSt, Importzoelle, Verbrauchsteuern abzueglich Agrarsubventionen und Wohnungsbaufoerderung.

**D.29X39 - Sonstige Produktionsabgaben minus sonstige Subventionen**
Grundsteuern, Gewerberlaubnisgebuehren abzueglich Lohnkostenzuschüsse, Zinsvergünstigungen. Negative Werte: Subventionen > Abgaben.

### Vermögenseinkommen (D.4)

| Code | Bezeichnung |
|------|-------------|
| D.41 | Zinsen |
| D.42 | Dividenden und Gewinnentnahmen |
| D.43 | Reinvestierte Gewinne aus Direktinvestitionen |
| D.44 | Kapitalertraege aus Versicherungsvertraegen |
| D.45 | Pachten (Land, Bodenschaetze) |

### Weitere D-Codes

| Code | Bezeichnung |
|------|-------------|
| D.5 | Einkommen- und Vermoegensteuern |
| D.61 | Nettosozialbeitraege |
| D.62 | Monetaere Sozialleistungen (Renten, ALG, Kindergeld) |
| D.7 | Sonstige laufende Transfers |
| D.8 | Zunahme betrieblicher Versorgungsansprueche |
| D.9 | Vermoegenstransfers |

---

## ESA 2010 Saldengroessen (B-Codes)

**B.1g - Bruttowertschoepfung**
Output minus Vorleistungen. Zentrale Groesse fuer Produktivitaetsmessung.

**B.2 - Betriebsueberschuss (Operating Surplus)**
Faellt bei Kapitalgesellschaften an. Berechnung: B.1g - D.1 - (D.29-D.39). Entspricht Gewinn vor Vermoegenseinkommen.

**B.3 - Selbstaendigeneinkommen (Mixed Income)**
Nur fuer Haushaltssektor (S.14). Untrennbare Mischung aus Arbeitsentgelt und Kapitalrendite bei Einzelunternehmen, Freiberuflern, Landwirten.

**B.8 - Sparen nach Sektoren**

| Sektor | Interpretation |
|--------|----------------|
| S.11 (Kapitalgesellschaften) | Einbehaltene Gewinne nach Dividenden |
| S.13 (Staat) | Primaerueberschuss/-defizit |
| S.14 (Haushalte) | Klassisches Sparen fuer Vermoegensbildung |

**B.9 - Finanzierungssaldo (Net Lending/Borrowing)**
Positiv: Sektor stellt Mittel bereit. Negativ: Sektor benoetigt Mittel.
Formel: B.9 = B.8 + Vermoegenstransfers - Bruttoinvestitionen

**B9FX9** - Statistische Diskrepanz zwischen realwirtschaftlichem B.9 und B.9F aus Finanzierungskonto.

---

## ESA 2010 Verwendungscodes (P-Codes)

**P.3 - Konsumausgaben**

| Sektor | Inhalt |
|--------|--------|
| P3_S13 | Staatskonsum (kollektiv + individuell zurechenbar) |
| P3_S14 | Privater Haushaltskonsum |
| P3_S15 | NPISH-Konsum (Kirchen, Vereine, Parteien) |

**P.51G - Bruttoanlageinvestitionen (GFCF)**
Zugaenge abzueglich Abgaenge von Anlageguetern: Bauten, Maschinen, Software, F&E, geistiges Eigentum.

**P.6 - Exporte**
Lieferungen von Waren und Dienstleistungen an Gebietsfremde.

**P.7 - Importe**
Bezuege von Waren und Dienstleistungen von Gebietsfremden.

---

## ESA 2010 Institutionelle Sektoren (S-Codes)

**S.11 - Nichtfinanzielle Kapitalgesellschaften**
Marktproduzenten von Waren und nichtfinanziellen Dienstleistungen.

**S.12 - Finanzielle Kapitalgesellschaften**
Finanzvermittlung: Banken (S.122), Versicherungen (S.128), Pensionsfonds (S.129).

**S.13 - Staat**
Bund (S.1311), Laender (S.1312), Gemeinden (S.1313), Sozialversicherung (S.1314).

**S.14 - Private Haushalte**
Konsumenten und Kleinproduzenten. Einziger Sektor mit B.3 (Mixed Income).

**S.15 - NPISH**
Non-Profit Institutions Serving Households. Kirchen, Parteien, Gewerkschaften, Vereine.

**S.2 - Uebrige Welt (Rest of World)**
Alle gebietsfremden Einheiten. In FIGARO nach Laendern disaggregiert.

---

## FIGARO Methodik

### Vergleich mit anderen MRIO-Datenbanken

| Merkmal | FIGARO | WIOD | EXIOBASE |
|---------|--------|------|----------|
| Herausgeber | Eurostat/JRC (offiziell) | Uni Groningen | Akademisch |
| Zeitreihe | 2010-2022, jaehrlich | 2000-2014, eingestellt | 1995-aktuell |
| Sektoren | 64 NACE Rev. 2 | 56 ISIC Rev. 4 | 163 Industrien |
| VGR-Konsistenz | Vollstaendig (99.8% EU-BIP) | Benchmarked | Geschaetzt |

### QDR-Methodik
FIGAROs Alleinstellungsmerkmal: Bilaterale Handelsbalancierung auf HS-6-Digit-Ebene durch gewichtete Mittelwertbildung laenderspezifischer Asymmetrien.

### Bekannte Limitationen
- Sektorale Aggregation: 64 Industrien limitiert praezise Analysen
- Rest-der-Welt: Nur Export/Import-Vektoren, keine vollstaendigen SUTs
- Zeitliche Verzoegerung: T-2 Jahre
- Validierungsabweichungen: WAPE zu OECD-ICIO ~34%, zu EXIOBASE ~83%

---

## Empirische Referenzwerte aus FIGARO-NAM

### COVID-19 Strukturbruch (2019-2020)
| Land | HH-Konsum YoY | Trend-Abweichung |
|------|---------------|------------------|
| ES | -17.0% | -18.1% |
| GR | -16.1% | -11.2% |
| IT | -12.3% | -13.8% |
| DE | -7.1% | -9.7% |

### Sektorale Gewinner/Verlierer (DE 2020)
- Verlierer: N79 Travel (-56%), H51 Airlines (-46%), I Hotels (-32%)
- Gewinner: Q86 Healthcare (+22%), K66 Financial (+14%)

### Intersektorale Verflechtung (DE 2019)
- Hoechste Rueckwaertsverflechtung: Motor vehicles, Construction, Machinery
- Hoechste Vorwaertsverflechtung: Legal/Accounting, Real Estate, Wholesale

---

## Referenzen

- ESA 2010 Manual: Regulation EU No 549/2013
- Miller & Blair: Input-Output Analysis, 3rd Edition 2022
- OECD TiVA Database Documentation
- Eurostat FIGARO Methodology Notes
- Lokale Referenz: [ESA 2010 und FIGARO Referenzdokumentation](ESA%202010%20und%20FIGARO%20Referenzdokumentation.md)
