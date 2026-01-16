# Exploration Report: Energiekrise und COVID-Erholung in Suedeuropa

## Forschungsfrage

Hat die Energiekrise 2022 die COVID-Erholung in Suedeuropa gebremst?

## 1. Datenverfuegbarkeit

### 1.1 Vorhandene Laender in bestehenden Analysen

| Land | Code | Gruppe | In CSV/JSON | Vollstaendig 2019-2023 |
|------|------|--------|-------------|------------------------|
| Spanien | ES | Suedeuropa | Ja | Ja |
| Italien | IT | Suedeuropa | Ja | Ja |
| Griechenland | GR | Suedeuropa | Ja | Ja |
| Portugal | PT | Suedeuropa | **Nein** | Parquet verfuegbar |
| Deutschland | DE | Vergleich | Ja | Ja |
| Oesterreich | AT | Vergleich | Ja | Ja |
| Niederlande | NL | Vergleich | Ja | Ja |

**Befund:** Portugal (PT) fehlt in den existierenden CSV/JSON-Dateien, ist aber im Parquet-Datensatz fuer alle Jahre 2010-2023 vorhanden.

### 1.2 Metriken verfuegbar

| Metrik | Code | Beschreibung | Status |
|--------|------|--------------|--------|
| Haushaltskonsum | P3_S14 (via hh_consumption) | Primaerindikator | Vollstaendig |
| Staatskonsum | P3_S13 (via gov_consumption) | Sekundaer | Vollstaendig |
| Investitionen | P51G (via investment) | Sekundaer | Vollstaendig |
| Importe | P7 (via imports) | Kontextindikator | Vollstaendig |

## 2. Extraktion der Zeitreihen (Haushaltskonsum, Mrd. EUR)

### 2.1 Suedeuropa-Gruppe (ES, IT, GR)

| Jahr | ES | IT | GR |
|------|----:|----:|----:|
| 2019 | 764,822 | 1.112,246 | 143,898 |
| 2020 | 634,717 | 975,340 | 120,799 |
| 2021 | 704,796 | 1.049,814 | 134,201 |
| 2022 | 817,165 | 1.201,167 | 160,040 |
| 2023 | 886,305 | 1.270,637 | 172,313 |

### 2.2 Vergleichsgruppe (DE, AT, NL)

| Jahr | DE | AT | NL |
|------|----:|----:|----:|
| 2019 | 1.840,602 | 213,411 | 377,190 |
| 2020 | 1.710,174 | 191,774 | 353,193 |
| 2021 | 1.801,857 | 200,994 | 384,134 |
| 2022 | 2.045,224 | 234,795 | 445,724 |
| 2023 | 2.177,320 | 255,017 | 482,497 |

## 3. Musteridentifikation

### 3.1 COVID-Einbruch 2020 (YoY-Veraenderung gegenueber 2019)

| Land | Gruppe | COVID-Einbruch (%) | Ranking |
|------|--------|-------------------:|---------|
| ES | Suedeuropa | -17.0% | 1 (tiefster) |
| GR | Suedeuropa | -16.1% | 2 |
| IT | Suedeuropa | -12.3% | 3 |
| AT | Vergleich | -10.1% | 4 |
| FR | (nicht Zielgruppe) | -7.6% | 5 |
| DE | Vergleich | -7.1% | 6 |
| NL | Vergleich | -6.4% | 7 (mildester) |
| PL | (nicht Zielgruppe) | -4.7% | 8 |

**Befund:** Suedeuropa erlitt deutlich staerkere COVID-Einbrueche (-12% bis -17%) als die Vergleichsgruppe (-6% bis -10%).

### 3.2 Erholungsdynamik 2020-2021 (Berechnung aus Zeitreihen)

| Land | Gruppe | 2020 | 2021 | Erholung (%) | Niveau vs. 2019 (%) |
|------|--------|-----:|-----:|-------------:|--------------------:|
| ES | Suedeuropa | 634,717 | 704,796 | +11.0% | -7.9% |
| IT | Suedeuropa | 975,340 | 1.049,814 | +7.6% | -5.6% |
| GR | Suedeuropa | 120,799 | 134,201 | +11.1% | -6.7% |
| DE | Vergleich | 1.710,174 | 1.801,857 | +5.4% | -2.1% |
| AT | Vergleich | 191,774 | 200,994 | +4.8% | -5.8% |
| NL | Vergleich | 353,193 | 384,134 | +8.8% | +1.8% |

**Befund:** Suedeuropa hatte 2021 eine staerkere Erholungsdynamik (+7.6% bis +11.1%), erreichte aber das 2019er-Niveau noch nicht.

### 3.3 Energiekrise-Effekt 2022 (nominale YoY-Veraenderung 2021-2022)

| Land | Gruppe | HH-Konsum 2022 (%) | Bemerkung |
|------|--------|-------------------:|-----------|
| GR | Suedeuropa | +19.3% | Hoechster nominaler Anstieg |
| PL | (nicht Zielgruppe) | +17.2% | |
| AT | Vergleich | +16.8% | |
| NL | Vergleich | +16.0% | |
| ES | Suedeuropa | +15.9% | |
| IT | Suedeuropa | +14.4% | |
| DE | Vergleich | +13.5% | |
| FR | (nicht Zielgruppe) | +9.6% | Niedrigster Anstieg |

**WICHTIGE EINSCHRAENKUNG:** Diese Zahlen sind nominal. Die hohen Anstiege 2022 spiegeln grossteils die Inflation (Energie- und Lebensmittelpreise) wider, nicht reales Konsumwachstum.

### 3.4 Erholungsgrad relativ zum Vorkrisenniveau (Index 2019=100)

| Land | Gruppe | 2020 | 2021 | 2022 | 2023 |
|------|--------|-----:|-----:|-----:|-----:|
| ES | Suedeuropa | 83.0 | 92.1 | 106.8 | 115.9 |
| IT | Suedeuropa | 87.7 | 94.4 | 108.0 | 114.2 |
| GR | Suedeuropa | 83.9 | 93.3 | 111.2 | 119.7 |
| DE | Vergleich | 92.9 | 97.9 | 111.1 | 118.3 |
| AT | Vergleich | 89.9 | 94.2 | 110.0 | 119.5 |
| NL | Vergleich | 93.6 | 101.8 | 118.2 | 127.9 |

**Befund:** Nominell haben alle Laender 2022 das Vorkrisenniveau ueberschritten. Das taeuscht jedoch ueber reale Kaufkraftverluste hinweg.

## 4. Trend-Abweichungsanalyse (Deviation from Pre-Crisis CAGR 2010-2018)

| Land | CAGR 2010-2018 (%) | Trendabweichung 2020 (%) |
|------|-------------------:|-------------------------:|
| ES | 2.08 | -18.1 |
| IT | 1.45 | -13.8 |
| GR | -1.02 | -11.2 |
| AT | 3.16 | -12.3 |
| DE | 2.86 | -9.7 |
| NL | 3.35 | -9.3 |

**Befund:** Spanien zeigt die groesste Abweichung vom langfristigen Trend (-18.1%), gefolgt von Italien (-13.8%). Griechenland hatte bereits einen negativen Vorkrisentrend.

## 5. Zentrale Befunde

### 5.1 Klare Muster (FACT)

1. **COVID-Asymmetrie:** Suedeuropa erlitt 2020 staerkere Konsumeinbrueche (-12% bis -17%) als die Vergleichsgruppe (-6% bis -10%)

2. **Erholungsdynamik 2021:** Suedeuropa erholte sich 2021 schneller (+7-11%) als die Vergleichsgruppe (+5-9%), blieb aber unter dem 2019er-Niveau

3. **Nominale Ueberhoehung 2022:** Alle Laender zeigen starke nominale Konsumanstiege 2022 (+10-19%), interpretierbar als Inflationseffekt

### 5.2 Interpretationsbedarf (INFERENCE)

1. **Reale vs. nominale Entwicklung:** Ohne externe Deflator-Daten (HICP) kann nicht bestimmt werden, ob der reale Konsum 2022 gewachsen oder geschrumpft ist

2. **Energieintensitaet:** Suedeuropa koennte staerker von Energiepreisanstiegen betroffen sein (hoehere Kuehlkosten im Sommer, geringere Energieeffizienz)

3. **Tourismuseffekt:** GR, ES, IT haben hohe Tourismuszugehoerigkeit - 2021/2022 Erholung koennte durch Tourismusrebound verstaerkt sein

## 6. Datenluecken

| Luecke | Auswirkung | Loesung |
|--------|------------|---------|
| Portugal (PT) fehlt | Unvollstaendige Suedeuropa-Gruppe | Parquet-Abfrage erforderlich |
| Nur nominale Werte | Inflationseffekt nicht bereinigt | Externe HICP-Daten noetig |
| Sektorale Aufschluesselung fehlt | Keine Identifikation von Energiepreiseffekten | Weitere Parquet-Analyse |

## 7. Empfehlung

Die bestehenden Daten reichen fuer eine erste Hypothesenformulierung. Fuer eine vollstaendige Analyse wird empfohlen:

1. **PT-Daten extrahieren** aus Parquet (niedriger Aufwand)
2. **HICP-Deflatoren einbeziehen** fuer reale Interpretation (externer Datenbedarf)
3. **Sektorale Analyse** fuer CPA_D35 (Energie) Konsumanteil

---

Erstellt: 2026-01-16
Datenbasis: outputs/tables/all_countries_time_series.csv, docs/data/time_series.json
