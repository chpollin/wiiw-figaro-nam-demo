# Run Metadaten

Run-ID: run-2026-01-16-1430
Status: abgeschlossen
Start: 2026-01-16 14:30
Ende: 2026-01-16 15:10
Commit: 345968b

## Forschungsfrage

Hat die Energiekrise 2022 die COVID-Erholung in Suedeuropa gebremst?

Konkretisierung:
- Laender: ES, IT, GR, PT (Suedeuropa) vs. DE, AT, NL (Vergleichsgruppe)
- Zeitraum: 2019 (Pre-COVID), 2020 (COVID), 2021 (Erholung), 2022-2023 (Energiekrise)
- Metrik: Haushaltskonsum (P3_S14) als Indikator fuer wirtschaftliche Erholung
- Fragestellung: Zeigen suedeuropaeische Laender 2022 eine Verlangsamung oder Umkehr der Erholung?

## Hypothesen

H_int (Integriert aus H1 + H4 + H5):
> Suedeuropaeische Laender zeigen 2022 eine staerkere nominale, aber schwaeachere reale Erholung als Nordeuropa, wobei der Unterschied teilweise durch hoehere Staatskonsum-Expansion abgefedert wird. Der scheinbar staerkere nominale Rebound ist primaer ein Basis-Effekt des tieferen COVID-Einbruchs 2020.

## Zusammenfassung

**Ergebnis: Hypothese teilweise bestaetigt (1/3 Komponenten)**

1. **Basis-Effekt (bestaetigt):** Korrelation r = -0.52 zwischen COVID-Einbruch und Erholungsrate. Suedeuropas tieferer Einbruch (-14.4%) erklaert die hoeheren nominalen Erholungsraten.

2. **Nominale Ueberlegenheit Suedeuropas (widerlegt):** Entgegen der Erwartung zeigt Nordeuropa einen hoeheren nominalen Index (113.1 vs. 110.0). Real konvergieren beide Regionen auf ~99.5% des Vorkrisenniveaus.

3. **Fiskalische Abfederung (Gegenteil):** Nordeuropa, insbesondere Deutschland (+21.2%), zeigte staerkere Staatskonsum-Expansion als Suedeuropa (+14.3%).

**Kernbefund:** Die Energiekrise 2022 hat die Erholung in beiden Regionen nominal verzerrt, aber real konvergieren alle Laender auf aehnliches Niveau. Der Unterschied liegt nicht in der Erholungsdynamik, sondern in den unterschiedlichen fiskalischen Reaktionen.

## Outputs

| Typ | Dateien |
|-----|---------|
| Skripte | scripts/11_extract_portugal.py, scripts/12_hypothesis_h_int.py |
| Tabellen | outputs/tables/PT_time_series.csv, recovery_comparison.csv, basis_effect_analysis.csv, fiscal_response.csv |
| Grafiken | outputs/figures/basis_effect_scatter.png, recovery_nominal_vs_real.png, fiscal_cushion.png |
| Paper | runs/run-2026-01-16-1430/paper/paper.md |
| Validierung | agents/implementation/validation.md |
