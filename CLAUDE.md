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
│   ├── analysis-agent.md        # Data exploration, hypotheses
│   ├── implementation-agent.md  # Code, pipelines, visualizations
│   └── synthesis-agent.md       # Paper writing
├── agents/                      # Subagent working directories
│   ├── analysis/                # Outputs: data-dictionary, hypotheses
│   ├── implementation/          # Outputs: validation reports
│   └── synthesis/               # Working notes
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
├── runs/                        # Versioned research runs
│   └── run-YYYY-MM-DD-HHmm/
│       ├── meta.md              # Run metadata and status
│       ├── log.md               # Chronological process log
│       └── paper/
│           ├── paper.md         # Final paper
│           └── figures/         # Figures
├── scripts/                     # Python analysis scripts
└── outputs/                     # Results (tables/, figures/)
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
| 2. Explore | Complete |
| 3. Human-in-the-Loop | In Progress |
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

## Agent-Based Research Workflow

### Role Distribution

| Role | Task |
|------|------|
| **Expert in the Loop** | Provides research question, validates intermediate results, decides under uncertainty |
| **Main Agent (Claude Code)** | Orchestrates workflow, maintains log, asks clarifying questions, delegates to subagents |
| **Subagents** | Specialized helpers for analysis, implementation, synthesis |

### Available Subagents

| Agent | Description | Phase | Tools |
|-------|-------------|-------|-------|
| `analysis-agent` | Data exploration, quality checks, hypothesis formation | 1 | Read, Grep, Glob, Bash |
| `implementation-agent` | Code development, pipelines, visualizations | 2 | Read, Write, Edit, Bash, Glob, Grep |
| `synthesis-agent` | Paper writing, results documentation | 3 | Read, Write, Edit, Glob, Grep |

All agents use `model: opus` for maximum analysis quality.

### Workflow Phases

```
Phase 1: Exploration     --> analysis-agent
Phase 2: Implementation  --> implementation-agent
Phase 3: Documentation   --> synthesis-agent
```

After each phase, the main agent checks:
- Can the research question be answered?
- **Yes**: Proceed to next phase
- **No**: Clarifying question to expert or re-run

### Run Management

For new research questions:

1. **Create run folder**: `runs/run-YYYY-MM-DD-HHmm/`
2. **Initialize meta.md** with research question and status
3. **Initialize log.md** for process log
4. **Call agents sequentially**
5. **After completion**: Git commit, finalize meta.md

### meta.md Template

```markdown
# Run Metadata

Run-ID: run-YYYY-MM-DD-HHmm
Status: running | completed | aborted
Start: YYYY-MM-DD HH:mm
End:
Commit:

## Research Question

[Question here]

## Hypotheses

[List of processed hypotheses]

## Summary

[Brief conclusion after completion]

## Abort Reason (if applicable)

[Justification and lessons learned]
```

### log.md Template

```markdown
# Process Log

| Time | Actor | Action | Result |
|------|-------|--------|--------|
| HH:mm | Main agent | Run initialized | meta.md created |
| HH:mm | analysis-agent | Data loaded | 14 years, 27 countries |
| HH:mm | Expert | Hypothesis selected | H2 prioritized |
```

### Clarifying Questions to Experts

When uncertain, the main agent asks structured clarifying questions:

| Element | Description |
|---------|-------------|
| **Context** | What is the current situation? |
| **Options** | What paths are available? (with pros/cons) |
| **Question** | Specific decision question |

Triggers for clarifying questions:
- Ambiguity in the research question
- Selection between multiple hypotheses
- Unexpected findings
- Abort decision

### Agent Working Directories

| Directory | Contents |
|-----------|----------|
| `agents/analysis/` | data-dictionary.md, exploration-report.md, hypotheses.md |
| `agents/implementation/` | validation.md, working notes |
| `agents/synthesis/` | drafts, working notes |

Final outputs (code, tables, figures) go to `scripts/`, `outputs/tables/`, `outputs/figures/`.

### Paper Structure

| Section | Content |
|---------|---------|
| Research Question | What was investigated and why? |
| Data Foundation | Sources, time period, limitations |
| Exploration | What was found during data exploration? |
| Findings | What do the data show? (with references) |
| Interpretation | What follows from this? (clearly marked as interpretation) |
| Open Questions | What remains unclear? |

Epistemic Markers:
- **[FACT]**: Direct data observation
- **[INFERENCE]**: Interpretation with assumptions
- **[HYPOTHESIS]**: Question for further research
