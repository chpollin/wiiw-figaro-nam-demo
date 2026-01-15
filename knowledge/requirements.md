# Technical Requirements: FIGARO-NAM Analysis

## Quick Reference

| Component | Recommended |
|-----------|-------------|
| Language | Python 3.11+ or R 4.3+ |
| Notebook | Quarto (.qmd) or Jupyter (.ipynb) |
| Memory | 8+ GB RAM |
| Storage | ~200 MB for data |

## Python Setup

### Option 1: pip (recommended)

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install pyarrow pandas numpy scipy scikit-learn matplotlib seaborn plotly jupyter
```

### Option 2: conda

```bash
conda create -n figaro python=3.11
conda activate figaro
pip install pyarrow pandas numpy scipy scikit-learn matplotlib seaborn plotly jupyter
```

### Python Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pyarrow | ≥14.0 | Parquet I/O, partitioned datasets |
| pandas | ≥2.0 | Data manipulation |
| polars | ≥0.20 | Large dataset handling (optional) |
| numpy | ≥1.24 | Numerical operations |
| scipy | ≥1.11 | Statistical functions |
| scikit-learn | ≥1.3 | Clustering, dimensionality reduction |
| matplotlib | ≥3.8 | Base plotting |
| seaborn | ≥0.13 | Statistical visualization |
| plotly | ≥5.18 | Interactive plots |
| jupyter | ≥1.0 | Notebooks |

## R Setup

```r
install.packages(c("arrow", "dplyr", "tidyr", "ggplot2", "plotly", "networkD3"))
```

| Package | Purpose |
|---------|---------|
| arrow | Parquet I/O |
| dplyr | Data manipulation |
| tidyr | Data reshaping |
| ggplot2 | Visualization |
| plotly | Interactive plots |
| networkD3 | Sankey diagrams |

## Quarto Installation

```bash
# macOS
brew install quarto

# Linux (Ubuntu/Debian)
wget https://quarto.org/download/latest/quarto-linux-amd64.deb
sudo dpkg -i quarto-linux-amd64.deb

# Windows
winget install Posit.Quarto
# Or download from https://quarto.org/docs/get-started/
```

## Hardware Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| RAM | 4 GB | 8+ GB |
| Storage | 500 MB | 2 GB |
| CPU | Any | Multi-core for parallel processing |

**Performance tips:**
- Use `polars` instead of `pandas` for faster processing
- Filter by partition (`base`, `ctr`) before loading
- Use chunked reading for memory-constrained environments

## LLM Integration

### Recommended Models

| Model | Use Case |
|-------|----------|
| Claude Opus/Sonnet | Complex analysis, code generation |
| GPT-4 | General coding assistance |
| Local (Ollama) | Sensitive data workflows |

### Context Engineering

For optimal LLM assistance:

1. Upload `knowledge/*.md` files at session start
2. Reference `journal.md` for session continuity
3. Provide specific file paths and error messages
4. Use `data.md` code lists for accurate variable names

### Example Prompt Structure

```
Context: Working with FIGARO-NAM data (see data.md)
Task: [Specific analysis goal]
Constraints: [Memory limits, output format]
Output: [Code, visualization, interpretation]
```

## Verification

Test your setup:

```python
# Python
import pyarrow.parquet as pq
df = pq.read_table('data/parquet/', filters=[('base', '=', '2020'), ('ctr', '=', 'AT')]).to_pandas()
print(f"Loaded {len(df):,} rows")
```

```r
# R
library(arrow)
df <- open_dataset("data/parquet/") |> filter(base == 2020, ctr == "AT") |> collect()
print(paste("Loaded", nrow(df), "rows"))
```
