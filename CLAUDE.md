# CLAUDE.md

Instructions for AI assistants working with this repository.

## Project Overview

This is a demonstration project for agentic macroeconomic data analysis using FIGARO-NAM (Eurostat National Accounts Matrix). It accompanies a workshop on LLM-assisted data analysis at wiiw (Vienna Institute for International Economic Studies).

## Repository Structure

```
wiiw-figaro-nam-demo/
├── CLAUDE.md                    # This file - AI assistant instructions
├── README.md                    # Project overview and quick start
├── .gitignore                   # Excludes data/ folder
├── .claude/agents/              # Subagent definitions
│   ├── analysis-agent.md        # Datenexploration, Hypothesen
│   ├── implementation-agent.md  # Code, Pipelines, Visualisierungen
│   └── synthesis-agent.md       # Paper-Erstellung
├── agents/                      # Arbeitsordner der Subagents
│   ├── analysis/                # Outputs: data-dictionary, hypotheses
│   ├── implementation/          # Outputs: validation reports
│   └── synthesis/               # Arbeitsnotizen
├── data/                        # Parquet data (not in git, 191 MB)
│   └── parquet/
│       └── base=YYYY/
│           └── ctr=XX/
│               └── part-0.parquet
├── knowledge/                   # Context Engineering files
│   ├── data.md                  # Data schema, code lists, access examples
│   ├── research.md              # Workflow phases, research questions
│   ├── requirements.md          # Technical dependencies
│   └── journal.md               # Session log for continuity
├── runs/                        # Versionierte Forschungsdurchlaeufe
│   └── run-YYYY-MM-DD-HHmm/
│       ├── meta.md              # Run-Metadaten und Status
│       ├── log.md               # Chronologisches Prozessprotokoll
│       └── paper/
│           ├── paper.md         # Finales Paper
│           └── figures/         # Abbildungen
├── scripts/                     # Python-Analyseskripte
└── outputs/                     # Ergebnisse (tables/, figures/)
```

## Key Context Files

Before starting work, read these files in order:

1. `knowledge/data.md` - Understand the data structure (schema, 181 codes, 50 countries)
2. `knowledge/research.md` - Current workflow phase and tasks
3. `knowledge/journal.md` - Recent session history

## Data Access

The data is NOT in the repository (too large). When working with data:

```python
import pyarrow.parquet as pq

# Read specific country and year
df = pq.read_table(
    'data/parquet/',
    filters=[('base', '=', '2020'), ('ctr', '=', 'AT')]
).to_pandas()
```

## Schema Reference

| Column | Type | Description |
|--------|------|-------------|
| `Set_i` | string | Row: Products (CPA_*), Industries (NACE), Accounts (D*, B*, P*, F*, S*, N*) |
| `m` | string | Partner country (50 values) |
| `Set_j` | string | Column: Industries or Accounts |
| `value` | float64 | Flow value (billion EUR) |
| `base` | category | Year (2010-2023) |
| `ctr` | category | Country code |

## Code Conventions

- Use Python with pyarrow/pandas for data analysis
- Filter by partition (base, ctr) before loading to reduce memory
- Document assumptions in journal.md
- Keep outputs reproducible (notebooks preferred)

## Current Workflow Phase

Check `knowledge/research.md` for the current phase status:

| Phase | Status |
|-------|--------|
| 1. Inspect/Understand | Complete |
| 2. Explore | Pending |
| 3. Human-in-the-Loop | Pending |
| 4. Plan | Pending |
| 5. Execute | Pending |
| 6. Summary | Pending |

## Style Guidelines

- No emojis in any output or documentation
- Use tables for structured information
- Keep markdown simple and scannable
- Reference specific files and line numbers when discussing code

## Session Continuity

After completing work:

1. Update `knowledge/journal.md` with session summary
2. Update phase status in `knowledge/research.md` if applicable
3. Document any new findings in appropriate knowledge files

---

## Agentenbasierter Forschungsworkflow

### Rollenverteilung

| Rolle | Aufgabe |
|-------|---------|
| **Expert in the Loop** | Gibt Forschungsfrage, validiert Zwischenergebnisse, entscheidet bei Unsicherheit |
| **Hauptagent (Claude Code)** | Orchestriert Workflow, fuehrt Log, stellt Rueckfragen, delegiert an Subagents |
| **Subagents** | Spezialisierte Helfer fuer Analyse, Implementierung, Synthese |

### Verfuegbare Subagents

| Agent | Beschreibung | Phase | Tools |
|-------|--------------|-------|-------|
| `analysis-agent` | Datenexploration, Qualitaetspruefung, Hypothesenbildung | 1 | Read, Grep, Glob, Bash |
| `implementation-agent` | Code-Entwicklung, Pipelines, Visualisierungen | 2 | Read, Write, Edit, Bash, Glob, Grep |
| `synthesis-agent` | Paper-Erstellung, Ergebnisdokumentation | 3 | Read, Write, Edit, Glob, Grep |

Alle Agents verwenden `model: opus` fuer maximale Analysequalitaet.

### Workflow-Phasen

```
Phase 1: Exploration     --> analysis-agent
Phase 2: Implementierung --> implementation-agent
Phase 3: Dokumentation   --> synthesis-agent
```

Nach jeder Phase prueft der Hauptagent:
- Ist die Forschungsfrage beantwortbar?
- **Ja**: Weiter zur naechsten Phase
- **Nein**: Rueckfrage an Experten oder erneuter Durchlauf

### Run-Management

Bei neuer Forschungsfrage:

1. **Run-Ordner anlegen**: `runs/run-YYYY-MM-DD-HHmm/`
2. **meta.md initialisieren** mit Forschungsfrage und Status
3. **log.md initialisieren** fuer Prozessprotokoll
4. **Agents sequentiell aufrufen**
5. **Nach Abschluss**: Git-Commit, meta.md finalisieren

### meta.md Vorlage

```markdown
# Run Metadaten

Run-ID: run-YYYY-MM-DD-HHmm
Status: laufend | abgeschlossen | abgebrochen
Start: YYYY-MM-DD HH:mm
Ende:
Commit:

## Forschungsfrage

[Frage hier]

## Hypothesen

[Liste der bearbeiteten Hypothesen]

## Zusammenfassung

[Kurzes Fazit nach Abschluss]

## Abbruchgrund (falls relevant)

[Begruendung und gewonnene Erkenntnisse]
```

### log.md Vorlage

```markdown
# Prozessprotokoll

| Zeit | Akteur | Aktion | Ergebnis |
|------|--------|--------|----------|
| HH:mm | Hauptagent | Run initialisiert | meta.md angelegt |
| HH:mm | analysis-agent | Daten geladen | 14 Jahre, 27 Laender |
| HH:mm | Experte | Hypothese gewaehlt | H2 priorisiert |
```

### Rueckfragen an Experten

Bei Unsicherheit stellt der Hauptagent strukturierte Rueckfragen:

| Element | Beschreibung |
|---------|--------------|
| **Kontext** | Was ist die aktuelle Situation? |
| **Optionen** | Welche Wege gibt es? (mit Vor-/Nachteilen) |
| **Frage** | Konkrete Entscheidungsfrage |

Trigger fuer Rueckfragen:
- Ambiguitaet in der Forschungsfrage
- Auswahl zwischen mehreren Hypothesen
- Unerwartete Befunde
- Abbruchentscheidung

### Arbeitsordner der Agents

| Ordner | Inhalt |
|--------|--------|
| `agents/analysis/` | data-dictionary.md, exploration-report.md, hypotheses.md |
| `agents/implementation/` | validation.md, Arbeitsnotizen |
| `agents/synthesis/` | Entwuerfe, Arbeitsnotizen |

Die finalen Outputs (Code, Tabellen, Grafiken) landen in `scripts/`, `outputs/tables/`, `outputs/figures/`.

### Paper-Struktur

| Abschnitt | Inhalt |
|-----------|--------|
| Fragestellung | Was wurde untersucht und warum? |
| Datengrundlage | Quellen, Zeitraum, Einschraenkungen |
| Exploration | Was wurde bei der Datenexploration gefunden? |
| Befunde | Was zeigen die Daten? (mit Referenzen) |
| Interpretation | Was folgt daraus? (klar als Interpretation markiert) |
| Offene Fragen | Was bleibt unklar? |

Epistemische Marker:
- **[FAKT]**: Direkte Datenbeobachtung
- **[INFERENZ]**: Interpretation mit Annahmen
- **[HYPOTHESE]**: Frage fuer weitere Forschung
