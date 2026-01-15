# CLAUDE.md

Instructions for AI assistants working with this repository.

## Project Overview

This is a demonstration project for agentic macroeconomic data analysis using FIGARO-NAM (Eurostat National Accounts Matrix). It accompanies a workshop on LLM-assisted data analysis at wiiw (Vienna Institute for International Economic Studies).

## Repository Structure

```
wiiw-figaro-nam-demo/
├── CLAUDE.md           # This file - AI assistant instructions
├── README.md           # Project overview and quick start
├── .gitignore          # Excludes data/ folder
├── data/               # Parquet data (not in git, 191 MB)
│   └── parquet/
│       └── base=YYYY/
│           └── ctr=XX/
│               └── part-0.parquet
└── knowledge/          # Context Engineering files
    ├── data.md         # Data schema, code lists, access examples
    ├── research.md     # Workflow phases, research questions
    ├── requirements.md # Technical dependencies
    └── journal.md      # Session log for continuity
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
