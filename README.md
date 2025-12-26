# Offline AI Analytics Copilot

A correctness-first, offline analytics system that safely analyzes **unknown datasets** by reasoning about schema, semantics, and analytical validity *before* executing any analysis.

This project is intentionally designed to **refuse unsafe or misleading analytics**, rather than silently producing incorrect results.

---

## Problem Statement

Most analytics tools assume the dataset schema in advance.
When those assumptions are wrong or incomplete, systems often:

- produce misleading metrics,
- enable invalid comparisons,
- or silently hallucinate insights.

These failures are dangerous because they **look correct**.

This project addresses a core question:

> **How can an analytics system reason about an unfamiliar dataset and decide what analyses are safe — and which must be blocked?**

---

## Core Idea

The system follows a **schema-driven, capability-gated analytics workflow**:

1. Inspect the dataset and extract schema signals  
   (data types, uniqueness, distributions, missing values)
2. Propose semantic mappings to a **canonical analytical schema**
3. Require **human confirmation** for ambiguous mappings
4. Construct a canonical dataframe based on confirmed mappings
5. Enable or disable analytics based on available schema capabilities
6. Execute only safe, deterministic analytics
7. Explain assumptions, risks, and disabled analyses explicitly

All logic runs **offline** using deterministic computation.  
No external APIs or cloud services are required.

---

## Repository Structure

```text
offline-ai-analytics-copilot/
│
├── data/
│   └── curated/
│       └── *.csv                  # Example datasets
│
├── src/
│   ├── core/
│   │   ├── metrics.py             # Deterministic metric functions
│   │   └── analytics_engine.py    # Intent → metric routing
│   │
│   ├── explanation/
│   │   ├── explainer.py           # Natural-language explanations
│   │   ├── guided_analytics.py    # Capability-based analytics menu
│   │   └── suggestions.py         # Data quality suggestions
│   │
│   ├── utils/
│   │   └── data_inspector.py      # Missing values, duplicates, checks
│   │
│   ├── v3/
│   │   ├── schema_extractor.py    # Schema signal extraction
│   │   ├── canonical_schema.py    # Canonical field definitions
│   │   ├── semantic_mapper.py     # Semantic mapping proposals
│   │   ├── schema_adapter.py      # Canonical dataframe builder
│   │   └── system_reasoner.py     # Capability gating & risk reasoning
│   │
│   └── main.py                    # CLI entry point
│
├── requirements.txt
└── README.md
```
System Evolution

The project was built iteratively, with each version addressing a specific failure mode.

Version 1 — Deterministic Analytics Core
---
Fixed, intent-based analytics (summary, trend, rank, compare)

Each intent mapped to explicit metric logic

Unsupported questions rejected by design

Focus: Reliable computation

Version 2 — Data Inspection & Guided Analytics
---
Dataset inspection (shape, nulls, duplicates, numeric consistency)

AI-assisted data quality suggestions

Guided analytics limited to valid operations

Focus: Preventing analysis on dirty data

Version 3 — Schema Reasoning & Semantic Mapping
---
Schema signal extraction from unknown datasets

Semantic mapping to a canonical schema

Human-in-the-loop confirmation

Canonical dataframe construction

Analytics enabled or disabled based on schema validity

Focus: Preventing semantically invalid analytics

Version 3.9 — System Reasoning Layer
---
Explicit reasoning about dataset shape and capabilities

Enabled / disabled analyses explained

Assumptions and analytical risks surfaced

Focus: Analytical transparency and trust

Canonical Schema (Conceptual)
---
The system reasons using abstract analytical concepts rather than hardcoded column names:

| Canonical Field | Meaning                          |
| --------------- | -------------------------------- |
| metric          | Value being analyzed             |
| entity          | Who / what the metric belongs to |
| time            | Temporal reference               |
| category        | Grouping dimension               |


Datasets are mapped into this schema only when safe to do so.

Supported Analytical Intents
---
Each intent is enabled only if required schema signals are confirmed.

| Intent  | Description                      | Required Signals      |
| ------- | -------------------------------- | --------------------- |
| SUMMARY | Aggregate overview               | metric                |
| TREND   | Metric over time                 | metric + time         |
| RANK    | Rank entities by metric          | metric + entity       |
| COMPARE | Compare metric across categories | metric + category     |
| WHY     | Explain change drivers           | metric + time + group |

If requirements are not met, the system refuses execution and explains why.

Example Behavior
---
Sales Dataset

Enables: summary, ranking, comparison, trend

Explains: assumptions about metric consistency

Student Marks Dataset

Enables: summary, ranking

Disables: comparison (no category confirmed)

Explains: why certain analytics are blocked

How to run:
---
```
pip install -r requirements.txt
python -m src.main
```

Follow the CLI prompts to:

confirm semantic mappings

explore guided analytics

observe enabled and disabled capabilities

Key Design Principles

Correctness over coverage

Explicit refusal over silent failure

Deterministic logic over black-box ML

Human confirmation for semantic ambiguity

Explainability at every stage

Use Cases
---
Safely analyzing unfamiliar CSV datasets

Auditing analytics assumptions

Preventing misleading dashboards

Teaching schema-aware analytics reasoning

Offline analytics in restricted environments

Disclaimer
---
This system intentionally prioritizes analytical safety and correctness.
It may refuse to answer questions when required assumptions cannot be verified.
