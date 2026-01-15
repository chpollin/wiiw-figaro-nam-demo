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

## Referenzen

- ESA 2010 Manual: Regulation EU No 549/2013
- Miller & Blair: Input-Output Analysis, 3rd Edition 2022
- OECD TiVA Database Documentation
- Eurostat FIGARO Methodology Notes
