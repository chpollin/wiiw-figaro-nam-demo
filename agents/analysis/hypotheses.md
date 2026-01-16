# Hypothesen: Energiekrise und COVID-Erholung in Suedeuropa

## Forschungsfrage

Hat die Energiekrise 2022 die COVID-Erholung in Suedeuropa gebremst?

---

## Hypothese 1: Differentielle Erholungsgeschwindigkeit

**Prioritaet: HOCH**

### Formulierung

Suedeuropaeische Laender (ES, IT, GR, PT) zeigten 2021-2022 eine langsamere reale Konsum-Erholung als die Vergleichsgruppe (DE, AT, NL), obwohl ihre nominalen Wachstumsraten hoeher waren.

### Operationalisierung

| Schritt | Berechnung | Datenquelle |
|---------|------------|-------------|
| 1 | HH-Konsum nominal 2019, 2021, 2022 extrahieren | all_countries_time_series.csv |
| 2 | HICP-Deflatoren (2019=100) von Eurostat beziehen | Extern (HICP prc_hicp_aind) |
| 3 | Realer Konsum = Nominal / (HICP/100) | Berechnung |
| 4 | Realer Erholungsindex = Real_2022 / Real_2019 * 100 | Berechnung |
| 5 | Gruppenvergleich Suedeuropa vs. Vergleich | t-Test oder Mittelwertvergleich |

### Testbare Vorhersage

- H0: Realer Erholungsindex Suedeuropa >= Realer Erholungsindex Vergleich
- H1: Realer Erholungsindex Suedeuropa < Realer Erholungsindex Vergleich

### Erwartetes Ergebnis

Die nominalen Anstiege 2022 (+14-19% in Suedeuropa) maskieren reale Kaufkraftverluste. Nach Inflationsbereinigung sollte die Vergleichsgruppe staerker erholt sein.

### Aufwand

- Niedrig (bestehende Daten + externe Deflatoren)
- Geschaetzte Zeit: 2-3 Stunden

---

## Hypothese 2: Tourismusabhaengigkeit als Treiber

**Prioritaet: MITTEL**

### Formulierung

Laender mit hoher Tourismusabhaengigkeit (GR, ES, PT) zeigten 2021 eine staerkere aber 2022 eine gebremste Erholung gegenueber weniger tourismusabhaengigen Laendern.

### Operationalisierung

| Schritt | Berechnung | Datenquelle |
|---------|------------|-------------|
| 1 | Tourismussektor-Konsum (CPA_I, CPA_H49-H53) extrahieren | Parquet (Set_i Filter) |
| 2 | Anteil Tourismus am HH-Konsum berechnen | Aggregation |
| 3 | Tourismuswachstum 2020-2021 vs. 2021-2022 vergleichen | YoY-Berechnung |
| 4 | Korrelation Tourismusanteil 2019 vs. Erholungsdynamik | Regression |

### Testbare Vorhersage

- H0: Kein Zusammenhang zwischen Tourismusanteil und Erholungsmuster
- H1: Hoehere Tourismusabhaengigkeit korreliert mit staerkerer Erholung 2021 aber Verlangsamung 2022

### Erwartetes Ergebnis

Tourismusrebound 2021 (nach Aufhebung Reisebeschraenkungen) erklaert Teile der Suedeuropa-Erholung. 2022 Normalisierung.

### Aufwand

- Mittel (Parquet-Abfrage erforderlich)
- Geschaetzte Zeit: 4-5 Stunden

---

## Hypothese 3: Energieintensitaet des Konsums

**Prioritaet: HOCH**

### Formulierung

Haushalte in Suedeuropa hatten 2022 einen hoeheren Anteil energieintensiver Ausgaben am Gesamtkonsum, was zu staerkeren Preissteigerungseffekten fuehrte.

### Operationalisierung

| Schritt | Berechnung | Datenquelle |
|---------|------------|-------------|
| 1 | CPA_D35 (Strom/Gas) Konsum der HH extrahieren | Parquet (Set_i=CPA_D35, Set_j=S14) |
| 2 | Energieanteil = CPA_D35 / P3_S14 * 100 | Berechnung |
| 3 | Veraenderung Energieanteil 2019-2022 nach Land | Zeitreihe |
| 4 | Zusammenhang Energieanteilsanstieg vs. nominaler Konsumanstieg | Korrelation |

### Testbare Vorhersage

- H0: Energieanteilsanstieg 2019-2022 ist in Suedeuropa gleich wie in Vergleichsgruppe
- H1: Energieanteilsanstieg 2019-2022 ist in Suedeuropa hoeher

### Erwartetes Ergebnis

Durch hoehere Energie-Preisanstiege in energieabhaengigeren Haushalten steigt der nominale Energieanteil staerker, was auf geringere Kaufkraft fuer andere Gueter hindeutet.

### Aufwand

- Niedrig bis Mittel (Parquet-Abfrage)
- Geschaetzte Zeit: 3-4 Stunden

---

## Hypothese 4: Fiskalische Abfederung

**Prioritaet: NIEDRIG**

### Formulierung

Laender mit staerkerer Ausweitung des Staatskonsums (P3_S13) 2022 zeigten eine bessere Abfederung der Energiekrise fuer Haushalte.

### Operationalisierung

| Schritt | Berechnung | Datenquelle |
|---------|------------|-------------|
| 1 | Gov-Konsum Wachstum 2021-2022 nach Land | all_countries_time_series.csv |
| 2 | HH-Realkonsum-Entwicklung (siehe H1) | Berechnung |
| 3 | Korrelation Gov-Konsum-Wachstum vs. HH-Realkonsum-Entwicklung | Regression |

### Testbare Vorhersage

- H0: Kein Zusammenhang zwischen fiskalischer Expansion und HH-Konsumstabilitaet
- H1: Hoehere fiskalische Expansion stabilisiert HH-Konsum

### Erwartetes Ergebnis

Staatliche Energiepreis-Subventionen und Transfers in einigen Laendern (DE, NL) haben die Haushaltskaufkraft teilweise gestuetzt.

### Aufwand

- Niedrig (bestehende Daten)
- Geschaetzte Zeit: 2 Stunden

---

## Hypothese 5: Basis-Effekt der COVID-Tiefe

**Prioritaet: MITTEL**

### Formulierung

Laender mit tieferem COVID-Einbruch 2020 zeigen mechanisch hoehere prozentuale Erholungsraten 2021-2022, was keine echte Ueberlegenheit der Erholung bedeutet.

### Operationalisierung

| Schritt | Berechnung | Datenquelle |
|---------|------------|-------------|
| 1 | COVID-Einbruch (%) = (2020-2019)/2019 | all_countries_time_series.csv |
| 2 | Erholungsrate (%) = (2022-2020)/2020 | Berechnung |
| 3 | Korrelation Einbruchstiefe vs. Erholungsrate | Streudiagramm |
| 4 | Niveau-Vergleich (Index 2019=100 fuer 2022) | Berechnung |

### Testbare Vorhersage

- H0: Erholungsrate ist unabhaengig von Einbruchstiefe
- H1: Staerkerer Einbruch korreliert mit hoeherer prozentualer Erholung (Basis-Effekt)

### Erwartetes Ergebnis

ES und GR (tiefster Einbruch) zeigen nominell staerkste Erholung, liegen aber im Niveau-Vergleich zurueck.

### Aufwand

- Sehr niedrig (bestehende Daten)
- Geschaetzte Zeit: 1 Stunde

---

## Priorisierte Reihenfolge (Original)

| Prioritaet | Hypothese | Aufwand | Empfehlung |
|------------|-----------|---------|------------|
| 1 | H1: Differentielle Erholungsgeschwindigkeit | Niedrig | **ZUERST TESTEN** |
| 2 | H5: Basis-Effekt | Sehr niedrig | Parallel zu H1 |
| 3 | H3: Energieintensitaet | Mittel | Nach H1/H5 |
| 4 | H2: Tourismusabhaengigkeit | Mittel | Optional |
| 5 | H4: Fiskalische Abfederung | Niedrig | Ergaenzend |

---

## AUSGEWAEHLTE HYPOTHESE: H_int (Integriert)

**Status: GENEHMIGT durch Expert in the Loop (2026-01-16)**

### Formulierung

> Suedeuropaeische Laender (ES, IT, GR, PT) zeigen 2022 eine staerkere nominale, aber schwaeachere reale Erholung als Nordeuropa (DE, AT, NL), wobei der Unterschied teilweise durch hoehere Staatskonsum-Expansion in Suedeuropa abgefedert wird. Der scheinbar staerkere nominale Rebound ist primaer ein Basis-Effekt des tieferen COVID-Einbruchs 2020.

### Komponenten

| Komponente | Ursprung | Funktion |
|------------|----------|----------|
| Basis-Effekt | H5 | Methodische Kontrolle |
| Nominale vs. reale Erholung | H1 | Kernhypothese |
| Fiskalische Abfederung | H4 | Erklaerungsmechanismus |

### Kausale Kette

```
H5 (Basis-Effekt)     --> Methodische Kontrolle: Hohe Erholungsraten = Artefakt?
        |
        v
H1 (Differentielle    --> Kernhypothese: Nominal stark, real schwach?
    Erholung)
        |
        v
H4 (Fiskalische       --> Erklaerungsmechanismus: Staatskonsum als Puffer?
    Abfederung)
```

### Operationalisierung

| Schritt | Metrik | Datenquelle | Status |
|---------|--------|-------------|--------|
| 1 | PT-Daten extrahieren | Parquet | Ausstehend |
| 2 | Basis-Effekt: Korrelation Einbruch 2020 vs. Erholung 2021-22 | Bestehende CSV | Ausstehend |
| 3 | Nominaler Index 2019=100, Niveau 2022 | Bestehende CSV | Ausstehend |
| 4 | HICP-Deflatoren holen | Eurostat extern | Ausstehend |
| 5 | Realer Index 2019=100, Niveau 2022 | Berechnung | Ausstehend |
| 6 | Staatskonsum-Wachstum vs. HH-Konsum-Stabilisierung | Bestehende CSV | Ausstehend |
| 7 | Visualisierungen erstellen | matplotlib | Ausstehend |

### Erwartete Outputs

| Output | Beschreibung |
|--------|--------------|
| `outputs/tables/recovery_comparison.csv` | Nominale und reale Erholungsindizes |
| `outputs/tables/basis_effect_analysis.csv` | Korrelation Einbruch vs. Erholung |
| `outputs/tables/fiscal_response.csv` | Staatskonsum-Entwicklung |
| `outputs/figures/recovery_nominal_vs_real.png` | Balkendiagramm Vergleich |
| `outputs/figures/basis_effect_scatter.png` | Streudiagramm |
| `outputs/figures/fiscal_cushion.png` | Gov-Konsum vs. HH-Konsum |

### Testbare Vorhersagen

1. **Basis-Effekt:** Negative Korrelation zwischen COVID-Einbruch 2020 und Niveau-Index 2022
2. **Nominale Illusion:** Suedeuropa nominal >100%, real <100% (2019=100)
3. **Fiskalische Abfederung:** Laender mit hoeherem Gov-Konsum-Wachstum zeigen stabileren HH-Konsum

---

## Datenbedarf fuer vollstaendige Analyse

### Intern verfuegbar

- HH-Konsum nominal 2019-2023 (6 von 7 Laendern)
- Staatskonsum 2019-2023
- Investitionen 2019-2023

### Parquet-Extraktion erforderlich

- Portugal (PT) Daten
- Sektorale Aufschluesselung (CPA_D35, CPA_I)

### Extern erforderlich

- HICP-Deflatoren (Eurostat prc_hicp_aind)
- Optional: Energiepreisindizes

---

## Empfehlung fuer naechsten Schritt

**Sofort umsetzen:**

1. Hypothese H5 (Basis-Effekt) mit bestehenden Daten berechnen
2. Hypothese H1 vorbereiten: HICP-Daten von Eurostat beschaffen

**Kurzfristig:**

3. PT-Daten aus Parquet extrahieren fuer vollstaendige Suedeuropa-Gruppe

---

Erstellt: 2026-01-16
Basis: exploration-report.md, outputs/tables/*.csv
