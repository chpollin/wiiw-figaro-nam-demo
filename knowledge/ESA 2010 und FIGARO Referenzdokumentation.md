# ESA 2010 und FIGARO Referenzdokumentation

Dieses Dokument synthetisiert das Grundlagenwissen für die Arbeit mit dem FIGARO-NAM Datensatz. Es dient als Nachschlagewerk für Transaktionscodes, Sektordefinitionen, methodische Besonderheiten und Analyseindikatoren.

---

## Transaktionscodes (D-Systematik)

Die D-Codes klassifizieren Verteilungstransaktionen im European System of Accounts 2010.

### Arbeitnehmerentgelt (D.1)

**D.11 – Bruttolöhne und -gehälter**
Umfasst alle Bar- und Sachleistungen an Arbeitnehmer. Barleistungen beinhalten Grundgehälter, Überstundenzuschläge, Prämien, Boni und 13./14. Monatsgehälter. Sachleistungen umfassen Firmenwagen, verbilligte Produkte, Dienstwohnungen und Mitarbeiteraktien.

**D.12 – Sozialbeiträge der Arbeitgeber**
Gliedert sich in tatsächliche Beiträge an Sozialversicherungsträger (D.121) und unterstellte Sozialbeiträge für direkte Arbeitgeberleistungen ohne Versicherungsvermittlung (D.122), etwa betriebliche Direktzusagen für Pensionen.

### Nettogrößen (Steuern minus Subventionen)

**D.21X31 – Gütersteuern minus Gütersubventionen**
Zentrale Übergangsgröße von der Bruttowertschöpfung zum BIP zu Marktpreisen. Enthält Mehrwertsteuer, Importzölle, Verbrauchsteuern abzüglich Gütersubventionen wie Agrarpreisstützungen oder Wohnungsbauförderung.

**D.29X39 – Sonstige Produktionsabgaben minus sonstige Subventionen**
Erscheint im Einkommensentstehungskonto auf Branchen- und Sektorebene. Umfasst Grundsteuern auf Betriebsgebäude, Gewerbeerlaubnisgebühren, Kfz-Steuern für Betriebsfahrzeuge abzüglich Lohnkostenzuschüssen, Verlustausgleichen und Zinsvergünstigungen. Negative Werte im Datensatz signalisieren, dass Subventionen die Abgaben übersteigen.

### Vermögenseinkommen (D.4)

Entgelte für die Bereitstellung finanzieller und nichtfinanzieller Vermögenswerte.

| Code | Bezeichnung | Inhalt |
|------|-------------|--------|
| D.41 | Zinsen | Entgelt für Einlagen, Kredite, Anleihen |
| D.42 | Ausschüttungen und Entnahmen | Dividenden, Gewinnentnahmen aus Quasi-Kapitalgesellschaften |
| D.43 | Reinvestierte Gewinne | Aus ausländischen Direktinvestitionen |
| D.44 | Vermögenseinkommen aus Versicherungsverträgen | Kapitalerträge der Versicherungsnehmer |
| D.45 | Pachten | Entgelt für natürliche Ressourcen (Land, Bodenschätze) |

### Weitere Verteilungstransaktionen

| Code | Bezeichnung | Inhalt |
|------|-------------|--------|
| D.5 | Einkommen- und Vermögensteuern | Lohnsteuer, Körperschaftsteuer, Kapitalertragsteuer |
| D.61 | Nettosozialbeiträge | Arbeitgeber- und Arbeitnehmerbeiträge zur Sozialversicherung |
| D.62 | Monetäre Sozialleistungen | Renten, Arbeitslosengeld, Krankengeld, Kindergeld |
| D.7 | Sonstige laufende Transfers | Versicherungsprämien und -leistungen, EU-Eigenmittel, Entwicklungshilfe |
| D.8 | Zunahme betrieblicher Versorgungsansprüche | Anpassung für Pensionsrückstellungen |
| D.9 | Vermögenstransfers | Erbschaftsteuer, Investitionszuschüsse, Schuldenerlasse |

---

## Saldengrößen (B-Systematik)

Die B-Codes repräsentieren Kontensalden mit sektorspezifischer Interpretation.

### Betriebsüberschuss und Selbständigeneinkommen

**B.2 – Betriebsüberschuss (Operating Surplus)**
Fällt bei Kapitalgesellschaften an, wo Eigentümerentgelt separat als D.1 erfasst wird. Entspricht dem Gewinn vor Vermögenseinkommen.

Berechnung: B.2 = Bruttowertschöpfung (B.1g) − Arbeitnehmerentgelt (D.1) − sonstige Produktionsabgaben netto (D.29−D.39)

**B.3 – Selbständigeneinkommen (Mixed Income)**
Reserviert für Einzelunternehmen im Haushaltssektor (S.14), bei denen Arbeitsentgelt und Kapitalrendite untrennbar vermischt sind. Typisch für Handwerker, Freiberufler, landwirtschaftliche Betriebe.

### Sparen nach Sektoren (B.8)

Das Sparen hat für jeden institutionellen Sektor eine eigene ökonomische Bedeutung.

| Sektor | Code | Interpretation |
|--------|------|----------------|
| Nichtfinanzielle Kapitalgesellschaften | S.11 | Einbehaltene Gewinne nach Dividenden und Steuern. Interne Finanzierungsquelle für Investitionen. |
| Finanzielle Kapitalgesellschaften | S.12 | Einbehaltene Gewinne aus Finanzvermittlung. Oft gering wegen hoher Ausschüttungsquoten. |
| Staat | S.13 | Primärüberschuss bzw. -defizit nach Transfers. Negativer Wert signalisiert Defizit bei laufenden Ausgaben. |
| Private Haushalte | S.14 | Klassisches Sparen. Nicht-konsumiertes Einkommen für Vermögensbildung und Altersvorsorge. |
| NPISH | S.15 | Überschuss oder Fehlbetrag nach Erfüllung der Transferfunktion. Meist marginal. |

### Finanzierungssaldo (B.9)

Zeigt, ob ein Sektor netto Mittel bereitstellt (Net Lending, positiv) oder benötigt (Net Borrowing, negativ).

Berechnung: B.9 = Sparen (B.8) + empfangene Vermögenstransfers − geleistete Vermögenstransfers − Bruttoinvestitionen

**B9FX9** erfasst die statistische Diskrepanz zwischen dem realwirtschaftlich ermittelten B.9 und dem aus dem Finanzierungskonto abgeleiteten B.9F. Theoretisch identisch, praktisch divergent durch Messfehler.

---

## Verwendungscodes (P-Systematik)

### Bruttoanlageinvestitionen (P.51G)

Zugänge abzüglich Abgänge von Anlagegütern. Umfasst Bauten und Bauwerke, Ausrüstungen und Maschinen, geistiges Eigentum (F&E, Software, Datenbanken), kultivierte biologische Ressourcen sowie Kosten des Eigentumswechsels (Notargebühren, Maklerprovisionen).

Nettoanlageinvestitionen (P.51N) ergeben sich nach Abzug der Abschreibungen (P.51C).

### Konsumausgaben (P.3)

Ausgaben zur Bedürfnisbefriedigung, sektoral verteilt.

| Sektor | Inhalt |
|--------|--------|
| Staat (S.13) | Kollektive Dienste (Verteidigung, Verwaltung) und individuell zurechenbare Dienste (Bildung, Gesundheit) |
| Private Haushalte (S.14) | Privater Konsum für Güter und Dienstleistungen |
| NPISH (S.15) | Dienste von Kirchen, Parteien, Vereinen, Gewerkschaften |

---

## Institutionelle Sektoren (S-Systematik)

### Inländische Sektoren

**S.11 – Nichtfinanzielle Kapitalgesellschaften**
Marktproduzenten von Waren und nichtfinanziellen Dienstleistungen. Untersektoren nach Kontrolle: öffentlich kontrolliert (S.11001), national privat kontrolliert (S.11002), auslandskontrolliert (S.11003).

**S.12 – Finanzielle Kapitalgesellschaften**
Finanzvermittlung und Hilfsdienstleistungen. Neun Untersektoren von Zentralbank (S.121) über Kreditinstitute (S.122) bis Pensionsfonds (S.129).

**S.13 – Staat**
Vier Ebenen: Bund (S.1311), Länder (S.1312), Gemeinden (S.1313), Sozialversicherung (S.1314). Produziert hauptsächlich nichtmarktbestimmte Güter und nimmt Umverteilung vor.

**S.14 – Private Haushalte**
Personen oder Personengruppen als Konsumenten und als Produzenten (Einzelunternehmen, Selbständige). Einziger Sektor mit Selbständigeneinkommen (B.3).

**S.15 – Private Organisationen ohne Erwerbszweck (NPISH)**
Kirchen, politische Parteien, Gewerkschaften, Vereine, Stiftungen. Produzieren nichtmarktbestimmte Güter für private Haushalte.

### Übrige Welt

**S.2 – Rest of the World**
Aggregiert alle gebietsfremden Einheiten für grenzüberschreitende Transaktionen. In FIGARO nach Ländern disaggregiert.

---

## FIGARO-spezifische Methodik

### Positionierung im Vergleich

FIGARO (Full International and Global Accounts for Research in Input-Output Analysis) ist seit 2021 die einzige offizielle EU-Statistik für Multi-Regional Input-Output Tables.

| Merkmal | FIGARO | WIOD | EXIOBASE 3 |
|---------|--------|------|------------|
| Herausgeber | Eurostat/JRC (offiziell) | Universität Groningen | Akademisches Konsortium |
| Zeitreihe | 2010–2022, jährlich aktualisiert | 2000–2014, eingestellt | 1995–aktuell, unregelmäßig |
| Sektoren | 64 NACE Rev. 2 | 56 ISIC Rev. 4 | 163 Industrien × 200 Produkte |
| VGR-Konsistenz | Vollständig (99,8% EU-BIP) | Benchmarked mit Abweichungen | Geschätzt |
| Umwelt-Extensions | CO₂ separat | Socio-economic Satellites | Umfangreich |
| Handels-Balancing | QDR-Methodik | Mirror-Flows | Geschätzte Reconciliation |

### QDR-Methodik

FIGAROs methodisches Alleinstellungsmerkmal für bilaterale Handelsbalancierung. Löst Handelsasymmetrien auf HS-6-Digit-Ebene durch gewichtete Mittelwertbildung unter Berücksichtigung länderspezifischer Export- und Import-Asymmetrien.

### Konstruktionsprozess

Der Aufbau durchläuft vier Phasen.

1. Harmonisierung nationaler Supply-Use-Tables auf NACE/CPA-Klassifikation
2. Bilaterale Handelsbalancierung mittels QDR
3. Benchmarking auf VGR-Aggregate für 45 Länder plus Rest der Welt
4. Transformation in Input-Output-Tabellen nach Modell B (Industry Technology Assumption) oder Modell D (Fixed Product Sales Structure)

### Bekannte Limitationen

**Sektorale Aggregation:** 64 Industrien limitieren präzise Umwelt-Footprint-Analysen. Ein einzelner Agrarsektor für heterogene Produkte erschwert differenzierte Bewertungen.

**Rest-der-Welt-Modellierung:** Nur Export/Import-Vektoren statt vollständiger SUT-Matrizen für Nicht-EU-Länder.

**Zeitliche Verzögerung:** T-2 Jahre. Aktuelle Projektionen basieren auf vorherigen SUT-Strukturen.

**Validierungsabweichungen:** WAPE zwischen FIGARO und OECD-ICIO beträgt 34%, zwischen FIGARO und EXIOBASE 83%. Differenzen resultieren aus unterschiedlichen Datenquellen und Balancing-Methoden.

**Länderspezifische Einschränkungen:** Geschätzte SUTs für Nicht-EU-Länder, schwer erfassbarer Dienstleistungshandel, manuelle Anpassungen für Brasilien, Russland, UK.

### Erweiterungen

**FIGARO-E3:** Disaggregation auf 176 Industrien × 213 Produkte mit Labor- und Energy-Extensions.

**FIGARO-REG:** Regionale Auflösung auf 240 EU-NUTS2-Regionen.

---

## Indikatoren für Import-Abhängigkeit

### Import Penetration Ratio

Anteil der durch Importe befriedigten inländischen Nachfrage.

Formel: IPR = M / (BIP − X + M) × 100

Anwendbar auf Sektor- oder Produktebene. Werte über 50% signalisieren hohe Importabhängigkeit.

### Vertical Specialization Index

Anteil importierter Vorleistungen in Exporten. Quantifiziert Rückwärtsverflechtung in globalen Wertschöpfungsketten.

Nach Hummels, Ishii & Yi (2001): VS = importierte Vorleistungen in Exporten / Bruttoexporte

### Foreign Value Added Share (EXGR_FVASH)

OECD TiVA-Indikator für ausländischen Wertschöpfungsgehalt in Bruttoexporten.

Empirische Referenzwerte: Industrieländer 20–30%, kleine offene Volkswirtschaften über 40%.

### EU-Kommission Schwellenwerte

Definition strategischer Abhängigkeiten über drei Kriterien.

1. Herfindahl-Hirschman-Index über 0,4 für Importkonzentration
2. Import-Anteil über 50% der Gesamtnachfrage
3. Qualitativ niedrige Substituierbarkeit

Diese Methodik identifizierte 2021 insgesamt 137 abhängige Produkte, 2023 mit verbesserter FIGARO-basierter Methodik 204 Produkte in sensitiven Ökosystemen.

---

## Normalisierungsmethoden für Ländervergleiche

Die Methodenwahl hängt vom Analyseziel ab.

### Pro-Kopf-Normalisierung

Geeignet für Lebensstandard- und Wohlfahrtsvergleiche. Nenner ist die mittlere Jahresbevölkerung. Bei unterschiedlichen Altersstrukturen oder Erwerbsquoten sind Verzerrungen möglich.

### BIP-Anteilsrechnung

Formel: Indikator / BIP × 100

Standardisiert für Wirtschaftsgröße. Standard für Handelsoffenheit und relative Abhängigkeitsmaße. Kleine Länder erreichen durch Re-Exporte Werte über 100%, große Länder wie die USA typischerweise nur 25%.

### Kaufkraftparität (PPP/KKS)

Angemessen für Vergleiche realer Kaufkraft und Lebensstandards. Nicht geeignet für Handelsströme, da diese zu Marktpreisen erfolgen.

Datenquellen: Eurostat-OECD PPP Programme (jährlich für 36+ europäische Länder), World Bank ICP (alle drei Jahre global).

### Empfehlungen nach Vergleichszweck

| Zweck | Methode |
|-------|---------|
| Lebensstandard | PPP pro Kopf |
| Wirtschaftsstruktur | Anteil am BIP |
| Handelsverflechtung | EU=100 Index |
| Produktivität | Pro Erwerbstätigem |
| Zeitreihenanalyse | Konstante Preise + PPP |

---

## Weiterführende Quellen

**ESA 2010 Manual:** Regulation EU No 549/2013, verfügbar unter ec.europa.eu/eurostat/esa2010

**FIGARO Dokumentation:** ec.europa.eu/eurostat/web/esa-supply-use-input-tables/figaro

**OECD TiVA Guide:** stats.oecd.org (Guide to OECD Trade in Value Added, 2023)

**Methodische Grundlagen:** Miller & Blair, Input-Output Analysis: Foundations and Extensions, 3rd Edition 2022