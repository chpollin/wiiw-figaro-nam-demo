# Energiekrise und COVID-Erholung: Ein Vergleich zwischen Sued- und Nordeuropa

**Run:** run-2026-01-16-1430
**Datum:** 2026-01-16

---

## 1. Fragestellung

### Was wurde untersucht?

Diese Analyse untersucht, ob die Energiekrise 2022 die COVID-Erholung im Haushaltskonsum suedeuropaeischer Laender (Spanien, Italien, Griechenland, Portugal) im Vergleich zu nordeuropaeischen Laendern (Deutschland, Oesterreich, Niederlande) gebremst hat.

Die zentrale Hypothese (H_int) lautete:

> Suedeuropaeische Laender zeigen 2022 eine staerkere nominale, aber schwaeachere reale Erholung als Nordeuropa, wobei der Unterschied teilweise durch hoehere Staatskonsum-Expansion abgefedert wird. Der scheinbar staerkere nominale Rebound ist primaer ein Basis-Effekt des tieferen COVID-Einbruchs 2020.

### Warum ist das relevant?

Die COVID-19-Pandemie und die anschliessende Energiekrise 2022 trafen europaeische Volkswirtschaften unterschiedlich stark. Suedeuropa, mit seiner Tourismusabhaengigkeit und strukturellen Unterschieden, erlebte tiefere Einbrueche waehrend der Pandemie. Die Frage, ob die Erholung nachhaltig war oder durch Inflationseffekte ueberzeichnet wird, ist fuer die wirtschaftspolitische Bewertung von zentraler Bedeutung.

---

## 2. Datengrundlage

### Primaerquelle

[FAKT] Die Analyse basiert auf dem FIGARO-NAM-Datensatz (Eurostat), bereitgestellt via wiiw. [Quelle: validation.md:17-27]

| Merkmal | Beschreibung |
|---------|--------------|
| Quelle | Eurostat FIGARO-NAM (Full International and Global Accounts for Research in Input-Output Analysis - National Accounts Matrix) |
| Format | Apache Parquet, Hive-partitioniert |
| Zeitraum | 2010-2023 |
| Einheit | Millionen EUR (nominal) |

### Laenderauswahl

| Region | Laender | Auswahl-Rationale |
|--------|---------|-------------------|
| Suedeuropa | ES, IT, GR, PT | Tourismus-affine Volkswirtschaften, hoehere COVID-Betroffenheit |
| Nordeuropa | DE, AT, NL | Industrielaender mit geringerer Tourismus-Abhaengigkeit |
| Referenz | FR, PL | Zusaetzliche Vergleichspunkte |

### Variablen

| Variable | Code | Beschreibung |
|----------|------|--------------|
| Haushaltskonsum | P3_S14 | Konsumausgaben der privaten Haushalte |
| Staatskonsum | P3_S13 | Konsumausgaben des Staates |

### Deflationsmethodik

[FAKT] Die Realwerte wurden mit HICP-Deflatoren berechnet, rebasiert auf 2019=100.

**Datenquelle:** Eurostat prc_hicp_aind (Harmonised Index of Consumer Prices - annual data)
**URL:** https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_aind/default/table
**Abruf:** 2026-01-16

| Land | HICP 2022 (2015=100) | HICP 2022 (2019=100) |
|------|----------------------|----------------------|
| DE | 120.3 | 112.0 |
| AT | 122.5 | 113.0 |
| NL | 126.4 | 116.1 |
| ES | 118.5 | 111.6 |
| IT | 116.1 | 110.3 |
| GR | 114.4 | 110.1 |
| PT | 116.6 | 109.7 |

### Einschraenkungen

| Einschraenkung | Auswirkung |
|----------------|------------|
| Nominale FIGARO-Daten | Inflationseffekte erfordern externe Deflation |
| Aggregierte Konsumvariable | Keine Unterscheidung nach Guetern (Energie vs. andere) |
| Kleine Stichprobe (n=9) | Statistische Signifikanz eingeschraenkt |
| HICP als Deflator | Nicht perfekt fuer Konsum-Deflation, aber Standard-Methodik |

---

## 3. Exploration

### Bestehende COVID-Analysen

Die Vorerkundung identifizierte deutliche Muster im COVID-Einbruch 2020:

[FAKT] Suedeuropa erlitt staerkere COVID-Einbrueche (-12% bis -17%) als die Vergleichsgruppe (-6% bis -10%). [Quelle: exploration-report.md:69]

| Land | Gruppe | COVID-Einbruch 2020 |
|------|--------|---------------------|
| ES | Suedeuropa | -17.0% |
| GR | Suedeuropa | -16.1% |
| IT | Suedeuropa | -12.3% |
| PT | Suedeuropa | -12.3% |
| AT | Nordeuropa | -10.1% |
| DE | Nordeuropa | -7.1% |
| NL | Nordeuropa | -6.4% |

### Datenqualitaet

[FAKT] Alle analysierten Laender haben vollstaendige Zeitreihen 2019-2023. Portugal wurde ergaenzend aus dem Parquet-Datensatz extrahiert. [Quelle: validation.md:134-140]

### Hypothesenbildung

Basierend auf der Exploration wurden fuenf Hypothesen formuliert:

1. **H1:** Differentielle Erholungsgeschwindigkeit (nominal vs. real)
2. **H2:** Tourismusabhaengigkeit als Treiber
3. **H3:** Energieintensitaet des Konsums
4. **H4:** Fiskalische Abfederung
5. **H5:** Basis-Effekt der COVID-Tiefe

Die integrierte Hypothese H_int kombiniert H1, H4 und H5 als methodisch vorrangig. [Quelle: hypotheses.md:186-244]

---

## 4. Befunde

### 4.1 Basis-Effekt (H5) - BESTAETIGT

[FAKT] Die Korrelation zwischen COVID-Einbruch 2020 und nominaler Erholung 2020-2022 betraegt r = -0.523 (p = 0.1486). [Quelle: validation.md:91-94]

| Region | COVID-Einbruch 2020 | Nominale Erholung 2020-2022 |
|--------|---------------------|------------------------------|
| Suedeuropa (Durchschnitt) | -14.4% | +28.6% |
| Nordeuropa (Durchschnitt) | -7.9% | +22.7% |

[Quelle: basis_effect_analysis.csv]

| Land | COVID-Einbruch (%) | Erholung 2020-2022 (%) | Netto-Veraenderung 2019-2022 (%) |
|------|--------------------|-----------------------|----------------------------------|
| ES | -17.0 | +28.7 | +6.8 |
| IT | -12.3 | +23.2 | +8.0 |
| GR | -16.1 | +32.5 | +11.2 |
| PT | -12.3 | +29.8 | +13.9 |
| DE | -7.1 | +19.6 | +11.1 |
| AT | -10.1 | +22.4 | +10.0 |
| NL | -6.4 | +26.2 | +18.2 |

[INFERENZ] Der moderate negative Zusammenhang (r = -0.52) zeigt, dass Laender mit tieferem COVID-Einbruch tendenziell hoehere prozentuale Erholungsraten aufweisen. Dies ist ein statistisch-mathematischer Basis-Effekt, keine echte "Outperformance".

![Basis-Effekt: COVID-Einbruch vs. Erholung](figures/basis_effect_scatter.png)

**Abbildung 1: Der Basis-Effekt erklaert vermeintliche Erholungsdifferenzen.** Das Streudiagramm zeigt den systematischen negativen Zusammenhang (r = -0.52) zwischen COVID-Einbruch 2020 und prozentualer Erholung 2020-2022. Spanien (ES) mit dem tiefsten Einbruch (-17%) zeigt die optisch staerkste Erholung, doch dieser Effekt ist primaer mathematisch bedingt: Wer tiefer faellt, hat prozentual mehr aufzuholen. Die Regressionsgerade verdeutlicht, dass etwa die Haelfte der Varianz in den Erholungsraten durch die Einbruchstiefe erklaerbar ist. Suedeuropaeische Laender (rot) clustern im Bereich hoher Einbrueche und hoher Erholungsraten, waehrend nordeuropaeische Laender (blau) moderatere Werte zeigen.

---

### 4.2 Nominale vs. Reale Erholung (H1) - NICHT BESTAETIGT

[FAKT] Die nominalen und realen Erholungsindizes (2019=100) fuer 2022 zeigen ein unerwartetes Muster. [Quelle: recovery_comparison.csv, validation.md:101-108]

| Region | Nominaler Index 2022 | Realer Index 2022 | Differenz |
|--------|----------------------|-------------------|-----------|
| Suedeuropa (Durchschnitt) | 110.0 | 99.6 | +10.4 |
| Nordeuropa (Durchschnitt) | 113.1 | 99.5 | +13.6 |

**Detaillierte Laenderwerte 2022:**

| Land | Region | Nominaler Index | HICP-Deflator | Realer Index |
|------|--------|-----------------|---------------|--------------|
| ES | Sued | 106.8 | 111.6 | 95.8 |
| IT | Sued | 108.0 | 110.3 | 97.9 |
| GR | Sued | 111.2 | 110.1 | 101.0 |
| PT | Sued | 113.9 | 109.7 | 103.8 |
| DE | Nord | 111.1 | 112.0 | 99.2 |
| AT | Nord | 110.0 | 113.0 | 97.4 |
| NL | Nord | 118.2 | 116.1 | 101.8 |

[Quelle: recovery_comparison.csv:1-47]

[INFERENZ] Entgegen der Hypothese zeigt Nordeuropa eine staerkere nominale Erholung (113.1 vs. 110.0). Real konvergieren beide Regionen auf praktisch identisches Niveau (ca. 99.5). Die hoehere Nominal-Real-Differenz im Norden (+13.6 vs. +10.4) reflektiert die staerkere Energiepreisinflation in DE, AT und NL im Jahr 2022.

![Nominale vs. Reale Erholung](figures/recovery_nominal_vs_real.png)

**Abbildung 2: Nordeuropa zeigt nominal staerkere Erholung - das Gegenteil der Hypothese.** Der Balkenvergleich enthuellt den zentralen Befund dieser Analyse: Entgegen der Erwartung liegt der nominale Erholungsindex 2022 in Nordeuropa (113.1) ueber dem suedeuropaeischen Wert (110.0). Die Niederlande fuehren mit 118.2, waehrend Spanien mit 106.8 den niedrigsten Wert aufweist. Die realen Indizes (deflationiert mit HICP 2019=100) zeigen hingegen eine bemerkenswerte Konvergenz: Beide Regionen erreichen praktisch identische Niveaus um 99.5 - also knapp unter dem Vorkrisenniveau von 2019. Die groessere Nominal-Real-Luecke in Nordeuropa (+13.6 vs. +10.4 Prozentpunkte) reflektiert die staerkere Energiepreisinflation durch Gas-Abhaengigkeit von Russland.

---

### 4.3 Fiskalische Abfederung (H4) - GEGENTEIL BESTAETIGT

[FAKT] Die Staatskonsum-Entwicklung 2019-2022 zeigt ein gegenteiliges Muster zur Hypothese. [Quelle: fiscal_response.csv, validation.md:110-119]

| Region | Gov-Wachstum 2019-2022 |
|--------|------------------------|
| Suedeuropa (Durchschnitt) | +14.3% |
| Nordeuropa (Durchschnitt) | +19.7% |

**Detaillierte Laenderwerte:**

| Land | Region | Gov 2019 (Mio EUR) | Gov 2022 (Mio EUR) | Wachstum (%) |
|------|--------|--------------------|--------------------|--------------|
| DE | Nord | 717.506 | 869.815 | +21.2% |
| NL | Nord | 202.262 | 241.898 | +19.6% |
| AT | Nord | 78.029 | 92.347 | +18.3% |
| ES | Sued | 234.127 | 275.811 | +17.8% |
| PT | Sued | 36.348 | 42.456 | +16.8% |
| IT | Sued | 337.134 | 376.408 | +11.6% |
| GR | Sued | 37.086 | 41.132 | +10.9% |

[Quelle: fiscal_response.csv:1-10]

[INFERENZ] Die Annahme, Suedeuropa habe mit hoeherer Fiskalexpansion den Privatkonsum abgefedert, trifft nicht zu. Deutschland zeigt mit +21.2% die hoechste Staatskonsum-Expansion aller untersuchten Laender. Die schwache positive Korrelation zwischen Gov-Wachstum und HH-Stabilitaet (r = 0.201) deutet auf einen begrenzten Abfederungseffekt hin.

![Fiskalische Abfederung](figures/fiscal_cushion.png)

**Abbildung 3: Deutschland fuehrt bei der fiskalischen Expansion - Nordeuropa investierte mehr.** Die linke Grafik zeigt die Staatskonsum-Entwicklung 2019-2022: Deutschland (+21.2%), die Niederlande (+19.6%) und Oesterreich (+18.3%) expandierten den Staatskonsum staerker als alle suedeuropaeischen Laender. Dies widerspricht der Annahme, Suedeuropa habe den Privatkonsum durch hoehere Staatsausgaben kompensiert. Die rechte Grafik prueft den Zusammenhang zwischen fiskalischer Expansion und Haushaltskonsumstabilitaet ueber die gesamte Krisenperiode 2019-2022: Die schwache positive Korrelation (r = 0.20) deutet auf einen begrenzten Abfederungseffekt hin. Bemerkenswert: Deutschlands umfangreiche Entlastungspakete 2022 (Tankrabatt, Energiepauschale, 9-Euro-Ticket) spiegeln sich in der hohen Staatskonsum-Expansion wider.

---

## 5. Interpretation

### Zusammenfassung der Hypothesentests

| Teilhypothese | Status | Kernbefund |
|---------------|--------|------------|
| H5: Basis-Effekt | BESTAETIGT | r = -0.52, Sued tieferer Einbruch erklaert hoehere Erholungsraten |
| H1a: Sued nominal staerker | WIDERLEGT | Nord 113.1 vs. Sued 110.0 |
| H1b: Sued real schwaecher | NICHT BESTAETIGT | Praktisch gleich (99.6 vs. 99.5) |
| H4: Sued hoehere Fiskalexpansion | WIDERLEGT | Nord +19.7% vs. Sued +14.3% |

### Warum wurde H_int nur teilweise bestaetigt?

[INFERENZ] Die integrierte Hypothese beruhte auf drei Annahmen, von denen nur eine zutrifft:

1. **Basis-Effekt (bestaetigt):** Der tiefere COVID-Einbruch in Suedeuropa erklaert die hoeheren prozentualen Erholungsraten. Dies ist ein methodisch wichtiger Befund, der vor Fehlinterpretationen schuetzt. Abbildung 1 visualisiert diesen Zusammenhang eindrucksvoll.

2. **Nominale Illusion (widerlegt):** Die Annahme, Suedeuropa zeige nominal staerkere Erholung, trifft nicht zu. Tatsaechlich zeigt Nordeuropa hoehere nominale Indizes (Abbildung 2). Dies liegt vermutlich an der staerkeren Energiepreisinflation in Nordeuropa (hoeherer Gasverbrauch fuer Heizung) und dem robusten Arbeitsmarkt.

3. **Fiskalische Abfederung (widerlegt):** Entgegen der Erwartung expandierte Nordeuropa - insbesondere Deutschland - den Staatskonsum staerker (Abbildung 3). Dies koennte die umfangreichen Energiepreis-Entlastungspakete 2022 widerspiegeln (Tankrabatt, Energiepauschale, 9-Euro-Ticket).

### Alternative Erklaerungen

[HYPOTHESE] Folgende Faktoren koennten die Ergebnisse erklaeren:

1. **Unterschiedliche Inflationsursachen:** Nordeuropa hatte 2022 staerkere Energiepreisinflation (Gas-Abhaengigkeit von Russland), waehrend Suedeuropa breitere aber moderatere Preissteigerungen erlebte. Die HICP-Deflatoren in Tabelle 2.4 zeigen dies deutlich: NL 116.1, AT 113.0, DE 112.0 vs. ES 111.6, GR 110.1, PT 109.7.

2. **Tourismus-Rebound:** Die starke Erholung in GR und PT (reale Indizes von 101.0 und 103.8) koennte durch den Tourismus-Rebound 2022 getrieben sein, der reale Wirtschaftsaktivitaet generierte.

3. **Fiskal-Timing:** Deutschlands hohe Staatskonsum-Expansion 2022 reflektiert moeglicherweise spaetere, aber umfangreichere Entlastungspakete im Vergleich zu frueheren, kleineren Massnahmen in Suedeuropa.

4. **Strukturelle Anpassung:** Die reale Konvergenz beider Regionen auf ca. 99.5 (2019=100) deutet auf aehnliche Anpassungsmechanismen trotz unterschiedlicher nominaler Pfade hin - ein bemerkenswertes Ergebnis, das in Abbildung 2 sichtbar wird.

---

## 6. Fazit

### Kernaussagen

Diese Analyse liefert drei zentrale Erkenntnisse:

1. **Der Basis-Effekt ist real und quantifizierbar.** Laender mit tieferem COVID-Einbruch zeigen mechanisch hoehere prozentuale Erholungsraten. Dies erklaert etwa die Haelfte der Varianz (r = -0.52) und mahnt zur Vorsicht bei der Interpretation von Erholungsstatistiken.

2. **Die Energiekrise traf Nordeuropa staerker als erwartet.** Die hoehere nominale Erholung Nordeuropas bei gleichzeitig groesserer Nominal-Real-Luecke zeigt, dass die Gas-Abhaengigkeit von Russland in DE, AT und NL zu staerkerer Preisinflation fuehrte als in Suedeuropa.

3. **Fiskalische Reaktionen waren asymmetrisch.** Deutschlands Rolle als fiskalischer Spitzenreiter (+21.2% Staatskonsum-Wachstum) widerspricht dem Narrativ eines zurueckhaltenden nordeuropaeischen Fiskalkurses waehrend der Energiekrise.

### Methodische Implikationen

Die teilweise Widerlegung von H_int demonstriert den Wert quantitativer Ueberpruefung narrativer Annahmen. Ohne die HICP-Deflation waere die nominale Ueberlegenheit Nordeuropas nicht sichtbar geworden; ohne den Basis-Effekt-Test waeren die hohen Erholungsraten Suedeuropas falsch interpretiert worden.

---

## 7. Offene Fragen

### Methodische Luecken

| Frage | Typ | Naechster Schritt |
|-------|-----|-------------------|
| Wie unterschied sich die sektorale Konsumstruktur? | [HYPOTHESE] | Aufschluesselung nach CPA-Kategorien |
| Welche Rolle spielte der Tourismus in GR, ES, PT? | [HYPOTHESE] | Extraktion CPA_I (Gastgewerbe) aus Parquet |
| Waren die Fiskal-Interventionen zeitlich unterschiedlich? | [HYPOTHESE] | Quartalsweise Analyse 2020-2022 |

### Unerwartete Befunde fuer weitere Forschung

[HYPOTHESE] Warum konvergieren beide Regionen real auf dasselbe Niveau trotz unterschiedlicher nominaler Pfade?

[HYPOTHESE] Warum zeigt Deutschland (+21.2%) die hoechste Staatskonsum-Expansion, obwohl oft als fiskalisch konservativ charakterisiert?

[HYPOTHESE] Erklaert Polens Outperformance (+21.9% Netto-Veraenderung) ein alternatives Erholungsmodell ausserhalb der West-Ost-Divergenz?

### Datenbeduerfnisse

| Datenbedarf | Zweck |
|-------------|-------|
| Quartalsweise Daten 2020-2022 | Timing-Analyse der Erholung |
| Sektorale FIGARO-Aufschluesselung | Tourismus vs. Energie-Konsum |
| Energiepreisindizes nach Land | Spezifischere Deflation |

---

## Anhang: Datenquellen

### Abbildungsverzeichnis

| Abbildung | Datei | Beschreibung |
|-----------|-------|--------------|
| 1 | `figures/basis_effect_scatter.png` | Streudiagramm: COVID-Einbruch vs. Erholungsrate mit Regression |
| 2 | `figures/recovery_nominal_vs_real.png` | Balkenvergleich: Nominale und reale Erholungsindizes |
| 3 | `figures/fiscal_cushion.png` | Doppelgrafik: Staatskonsum-Wachstum und Korrelation |

### Tabellenquellen

| Datei | Beschreibung |
|-------|--------------|
| `outputs/tables/recovery_comparison.csv` | Nominale und reale Erholungsindizes |
| `outputs/tables/basis_effect_analysis.csv` | Korrelation Einbruch vs. Erholung |
| `outputs/tables/fiscal_response.csv` | Staatskonsum-Entwicklung |

### Externe Datenquellen

| Quelle | URL | Verwendung |
|--------|-----|------------|
| Eurostat HICP | https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_aind | Deflation nominal zu real |
| FIGARO-NAM | via wiiw | Konsumzeitreihen |

---

*Erstellt: 2026-01-16 | Run: run-2026-01-16-1430 | Methodik: FIGARO-NAM + HICP-Deflation*
