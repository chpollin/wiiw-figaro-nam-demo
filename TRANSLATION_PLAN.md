# Translation Plan: German to English

This document lists all files containing German text that need translation to English.

## Summary Statistics

| Category | Files | Estimated Lines |
|----------|-------|-----------------|
| Core Documentation | 4 | ~500 |
| Knowledge Base | 5 | ~840 |
| Agent Definitions | 3 | ~210 |
| Research Run Outputs | 5 | ~400 |
| Python Scripts | 2 | ~220 |
| Web Interface | 5 | ~110 |
| **TOTAL** | **24** | **~2,280** |

---

## Priority 1: Core Infrastructure (Critical for Functionality)

### 1.1 CLAUDE.md (AI Instructions)

**Path:** `CLAUDE.md`

**Lines:** 115-238 (Section "Agentenbasierter Forschungsworkflow")

**Content to translate:**
- Line 17: `# Datenexploration, Hypothesen`
- Line 20: `# Arbeitsordner der Subagents`
- Line 34: `# Versionierte Forschungsdurchlaeufe`
- Line 41: `# Python-Analyseskripte`
- Line 42: `# Ergebnisse (tables/, figures/)`
- Lines 117-123: Role table (Expert in the Loop, Hauptagent, Subagents)
- Lines 125-133: Available Subagents table
- Lines 135-146: Workflow phases
- Lines 148-156: Run management
- Lines 158-184: meta.md template
- Lines 186-196: log.md template
- Lines 198-212: Rueckfragen structure
- Lines 214-220: Agent working folders table
- Lines 224-238: Paper structure with epistemische markers

**Scope:** ~125 lines

---

### 1.2 Agent Definitions

#### .claude/agents/analysis-agent.md

**Path:** `.claude/agents/analysis-agent.md`

**Content to translate:**
- Line 3: description field
- Lines 8-15: Context and role description
- Lines 17-37: Tasks and outputs sections
- Lines 42-63: Output table and handover format

**Scope:** ~60 lines

#### .claude/agents/implementation-agent.md

**Path:** `.claude/agents/implementation-agent.md`

**Content to translate:**
- Line 3: description field
- Lines 8-37: Context, tasks, code standards
- Lines 55-82: Outputs and handover format

**Scope:** ~70 lines

#### .claude/agents/synthesis-agent.md

**Path:** `.claude/agents/synthesis-agent.md`

**Content to translate:**
- Line 3: description field
- Line 8: Role description
- Line 14-15: Language specification (change "Deutsch" to "English")
- Lines 17-31: Tasks with epistemische markers
- Lines 33-67: Paper structure template
- Lines 69-77: Reference formats table

**Scope:** ~80 lines

---

### 1.3 Web Dashboard (User-Facing)

#### docs/index.html

**Path:** `docs/index.html`

**Content to translate:**
- Line 6: meta description
- Line 7: author meta tag
- Line 8: page title
- Line 16: subtitle
- Line 18: data disclaimer
- Lines 23-40: Tab button labels (Zeitreihen, Erholung, Kreislauf, Handel, Sektoren, IO-Verflechtung)
- Lines 48-54: Dropdown labels and options
- Lines 57-66: Research question B3
- Lines 73-87: Control labels
- Line 93: Research question text
- Lines 101-120+: Additional tab content

**Scope:** ~60 lines

#### docs/js/app.js

**Path:** `docs/js/app.js`

**Lines to translate:**
- Line 2: File header comment
- Line 3: Description comment
- Line 55: console.log message
- Line 58: console.error message

**Scope:** ~5 lines

#### docs/js/timeseries.js

**Path:** `docs/js/timeseries.js`

**Lines to translate:**
- Line 2: File header comment
- Line 49: Hint comment

**Scope:** ~5 lines

---

### 1.4 Data Generation Script

#### scripts/09_generate_json.py

**Path:** `scripts/09_generate_json.py`

**Content to translate:**
- Lines 2-10: Module docstring
- Lines 23-67: `LAENDER_NAMEN` dictionary (46 country names)
  - 'DE': 'Deutschland' -> 'Germany'
  - 'FR': 'Frankreich' -> 'France'
  - etc.
- Lines 70-134: `BRANCHEN_NAMEN` dictionary (~65 sector names)
  - 'A01': 'Landwirtschaft' -> 'Agriculture'
  - 'C29': 'Kraftfahrzeuge' -> 'Motor vehicles'
  - etc.
- Lines 137-150: `CODE_BEZEICHNUNGEN` dictionary (12 ESA codes)
  - 'D11': 'Loehne und Gehaelter' -> 'Wages and salaries'
  - 'B2': 'Betriebsueberschuss' -> 'Operating surplus'
  - etc.
- Line 153-154: Function docstring
- Lines 167, 186, 202, 204: Print statements and crisis labels

**Scope:** ~180 lines

**Note:** After translating this file, regenerate JSON files by running the script.

---

## Priority 2: Knowledge Base Documentation

### 2.1 knowledge/glossary.md

**Path:** `knowledge/glossary.md`

**Content to translate:**
- Line 1: Title
- Line 3: Introduction
- Lines 7-36: Input-Output Analysis basics (12 definitions)
- Lines 38-56: Econometric basics (5 definitions)
- Lines 57-67: National Accounts
- Lines 70-89: FIGARO-specific terms
- Lines 92-101: FIGARO code mapping table
- Lines 104-126: Abbreviations list
- Lines 129-167: ESA 2010 D-Codes
- Lines 170-193: ESA 2010 B-Codes
- Lines 197-215: ESA 2010 P-Codes
- Lines 218-237: ESA 2010 S-Codes
- Lines 240-260: FIGARO Methodology
- Lines 262-278: Empirical reference values
- Lines 282-335: Web Dashboard architecture

**Scope:** ~300 lines

---

### 2.2 knowledge/journal.md

**Path:** `knowledge/journal.md`

**Content to translate:**
- Line 13: Session 7 title
- Lines 15-23: Workflow setup
- Line 26: Research question blockquote
- Lines 28-42: Phase descriptions
- Lines 44-56: Central findings table
- Lines 53-56: Surprising findings
- Lines 58-74: Files created table
- Lines 77-80: Methodological learnings
- Lines 82-84: Phase status
- Lines 88-150: Earlier session entries

**Scope:** ~200 lines

---

### 2.3 knowledge/research.md

**Path:** `knowledge/research.md`

**Content to translate:**
- Lines 81-92: Sectoral Asymmetry table
- Lines 108-131: Extended exploration findings
- Lines 177-184: Tab descriptions
- Lines 199-203: David's 4 Analysis Types

**Scope:** ~100 lines

---

### 2.4 knowledge/exploration_plan.md

**Path:** `knowledge/exploration_plan.md`

**Full document translation required**

**Scope:** ~120 lines

---

### 2.5 knowledge/ESA 2010 und FIGARO Referenzdokumentation.md

**Path:** `knowledge/ESA 2010 und FIGARO Referenzdokumentation.md`

**Note:** Full document, needs assessment

**Scope:** TBD (large file)

---

## Priority 3: Research Run Documentation

### 3.1 agents/analysis/hypotheses.md

**Path:** `agents/analysis/hypotheses.md`

**Content to translate:**
- Line 1: Title
- Lines 4-5: Research question
- Lines 9-170: Five hypotheses (H1-H5) with operationalization
- Lines 174-182: Priority ranking table
- Lines 186-244: Selected hypothesis H_int
- Lines 247-263: Data requirements
- Lines 267-276: Next steps recommendation

**Scope:** ~280 lines

---

### 3.2 agents/analysis/exploration-report.md

**Path:** `agents/analysis/exploration-report.md`

**Full document translation required**

**Scope:** TBD

---

### 3.3 agents/implementation/validation.md

**Path:** `agents/implementation/validation.md`

**Full document translation required**

**Scope:** TBD

---

### 3.4 runs/run-2026-01-16-1430/meta.md

**Path:** `runs/run-2026-01-16-1430/meta.md`

**Content to translate:**
- Line 11: Research question
- Lines 13-17: Concretization
- Lines 19-22: H_int hypothesis
- Lines 26-34: Summary and core finding
- Lines 36-44: Outputs table

**Scope:** ~30 lines

---

### 3.5 runs/run-2026-01-16-1430/log.md

**Path:** `runs/run-2026-01-16-1430/log.md`

**Content to translate:**
- Table headers: Zeit, Akteur, Aktion, Ergebnis
- All log entries

**Scope:** ~25 lines

---

### 3.6 runs/run-2026-01-16-1430/paper/paper.md

**Path:** `runs/run-2026-01-16-1430/paper/paper.md`

**Full scientific paper translation required**

**Scope:** TBD (likely 100+ lines)

---

## Priority 4: Python Script Comments

### 4.1 scripts/12_hypothesis_h_int.py

**Path:** `scripts/12_hypothesis_h_int.py`

**Content to translate:**
- Lines 4-9: Hypothesis description in docstring
- Line 72: print statement
- Line 80: print statement

**Scope:** ~40 lines

---

## Execution Order

### Phase 1: Core Infrastructure
1. [ ] `scripts/09_generate_json.py` - Translate dictionaries
2. [ ] Run script to regenerate `docs/data/*.json`
3. [ ] `docs/index.html` - Translate UI
4. [ ] `docs/js/app.js` - Translate comments
5. [ ] `docs/js/timeseries.js` - Translate comments
6. [ ] `CLAUDE.md` - Translate workflow section

### Phase 2: Agent Definitions
7. [ ] `.claude/agents/analysis-agent.md`
8. [ ] `.claude/agents/implementation-agent.md`
9. [ ] `.claude/agents/synthesis-agent.md`

### Phase 3: Knowledge Base
10. [ ] `knowledge/glossary.md`
11. [ ] `knowledge/journal.md`
12. [ ] `knowledge/research.md`
13. [ ] `knowledge/exploration_plan.md`
14. [ ] `knowledge/ESA 2010 und FIGARO Referenzdokumentation.md`

### Phase 4: Research Outputs
15. [ ] `agents/analysis/hypotheses.md`
16. [ ] `agents/analysis/exploration-report.md`
17. [ ] `agents/implementation/validation.md`
18. [ ] `runs/run-2026-01-16-1430/meta.md`
19. [ ] `runs/run-2026-01-16-1430/log.md`
20. [ ] `runs/run-2026-01-16-1430/paper/paper.md`

### Phase 5: Script Comments
21. [ ] `scripts/12_hypothesis_h_int.py`

---

## Translation Guidelines

1. **Preserve markdown formatting** - Keep headers, tables, code blocks intact
2. **Technical terms** - Use standard English economics terminology
3. **ESA 2010 codes** - Use official Eurostat English translations
4. **Consistency** - Use same translations for recurring terms
5. **File references** - Do not translate file paths or code identifiers

## Key Term Glossary (for consistency)

| German | English |
|--------|---------|
| Bruttowertschoepfung | Gross Value Added (GVA) |
| Vorleistungen | Intermediate consumption |
| Endnachfrage | Final demand |
| Rueckwaertsverflechtung | Backward linkages |
| Vorwaertsverflechtung | Forward linkages |
| Volkswirtschaftliche Gesamtrechnungen | National Accounts |
| Staatskonsum | Government consumption |
| Privater Konsum | Household consumption |
| Investitionen | Investment (GFCF) |
| Loehne und Gehaelter | Wages and salaries |
| Betriebsueberschuss | Operating surplus |
| Strukturbruch | Structural break |
| Forschungsfrage | Research question |
| Hypothese | Hypothesis |
| Befund | Finding |
| Inferenz | Inference |

---

*Generated: 2026-01-18*
