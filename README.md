# wiiw-figaro-nam-demo

Agentic workflow demonstration for macroeconomic data analysis using FIGARO-NAM (Eurostat National Accounts Matrix).

## Context

This repository accompanies a workshop on LLM-assisted data analysis at the Vienna Institute for International Economic Studies (wiiw). It demonstrates advanced Promptotyping methodology applied to complex, partitioned time-series data.

| | |
|---|---|
| **Workshop** | AI for Data Analysis & Visualisation |
| **Date** | 10 February 2026 |
| **Contact** | David Zenz (wiiw) |

## Purpose

This use case demonstrates what agentic research workflows can achieve with Promptotyping. It serves as a showcase of the method's potential for macroeconomic research, not as hands-on material for workshop participants.

## Data

FIGARO-NAM provides National Accounts Matrices from Eurostat in Hive-partitioned Parquet format.

| Metric | Value |
|--------|-------|
| Files | 700 parquet files |
| Size | 191 MB total |
| Years | 2010–2023 (14 years) |
| Countries | 50 (EU + global economies) |
| Rows/file | ~120,000 |

**Structure:**
```
data/parquet/base=YYYY/ctr=XX/part-0.parquet
```

> **Note:** Data files are excluded from git (see `.gitignore`). Contact David Zenz for data access.

See [knowledge/data.md](knowledge/data.md) for complete documentation including schema, code lists, and access examples.

## Workflow

```mermaid
graph LR
    A[1. Inspect] --> B[2. Explore]
    B --> C[3. Human-in-Loop]
    C --> D[4. Plan]
    D --> E[5. Execute]
    E --> F[6. Summary]
```

| Phase | Description |
|-------|-------------|
| **Inspect/Understand** | Load data, infer structure, generate data dictionary |
| **Explore** | Assess coverage, identify outliers, suggest analysis perspectives |
| **Human-in-the-Loop** | Select research questions based on feasibility and relevance |
| **Plan** | Transform questions into reproducible notebook workflows |
| **Execute** | Implement analysis pipeline and generate outputs |
| **Summary** | Synthesize findings, distinguish facts from interpretation |

## Knowledge Base

The `knowledge/` directory provides structured context for LLM-assisted work:

| File | Purpose |
|------|---------|
| [data.md](knowledge/data.md) | Data structure, schema, code lists, access examples |
| [research.md](knowledge/research.md) | Research questions and workflow phases |
| [requirements.md](knowledge/requirements.md) | Technical dependencies and setup |
| [journal.md](knowledge/journal.md) | Working journal for iterative development |

## Quick Start

```bash
# Clone repository
git clone https://github.com/DigitalHumanitiesCraft/wiiw-figaro-nam-demo.git
cd wiiw-figaro-nam-demo

# Setup Python environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install pyarrow pandas matplotlib seaborn

# Place data in data/parquet/ directory
# Then load data
python -c "import pyarrow.parquet as pq; print(pq.read_table('data/parquet/').schema)"
```

## Related

- [wiiw-patent-analysis-demo](https://github.com/DigitalHumanitiesCraft/wiiw-patent-analysis-demo) – Use Case 1 from the same workshop
- [Promptotyping methodology](https://chpollin.github.io/promptotyping/)

## License

MIT
