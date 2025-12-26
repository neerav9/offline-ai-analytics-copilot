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
│   │   ├── canonical_schema.py   # Canonical field definitions
│   │   ├── semantic_mapper.py    # Semantic mapping proposals
│   │   ├── schema_adapter.py     # Canonical dataframe builder
│   │   └── system_reasoner.py    # Capability gating & risk reasoning
│   │
│   └── main.py                   # CLI entry point
│
├── requirements.txt
└── README.md
```

---

## System Evolution

### Version 1 — Deterministic Analytics Core

* Fixed, intent-based analytics (summary, trend, rank, compare)
* Each intent mapped to explicit metric logic
* Unsupported questions rejected by design

---

### Version 2 — Data Inspection & Guided Analytics

* Dataset inspection (shape, nulls, duplicates, numeric consistency)
* AI-assisted data quality suggestions
* Guided analytics limited to valid operations

---

### Version 3 — Schema Reasoning & Semantic Mapping

* Schema signal extraction from unknown datasets
* Semantic mapping to a canonical schema
* Human-in-the-loop confirmation
* Canonical dataframe construction
* Analytics enabled or disabled based on schema validity

---

### Version 3.9 — System Reasoning Layer

* Explicit reasoning about dataset shape and capabilities
* Enabled and disabled analyses clearly explained
* Assumptions and analytical risks surfaced

---

## Canonical Schema (Conceptual)

| Canonical Field | Meaning                          |
| --------------- | -------------------------------- |
| metric          | Value being analyzed             |
| entity          | Who / what the metric belongs to |
| time            | Temporal reference               |
| category        | Grouping dimension               |

---

## Supported Analytical Intents

| Intent  | Description                      | Required Signals      |
| ------- | -------------------------------- | --------------------- |
| SUMMARY | Aggregate overview               | metric                |
| TREND   | Metric over time                 | metric + time         |
| RANK    | Rank entities by metric          | metric + entity       |
| COMPARE | Compare metric across categories | metric + category     |
| WHY     | Explain change drivers           | metric + time + group |

---

## How to Run

```bash
pip install -r requirements.txt
python -m src.main
```

---

## Key Design Principles

* Correctness over coverage
* Explicit refusal over silent failure
* Deterministic logic over black-box ML
* Human confirmation for semantic ambiguity
* Explainability at every stage

---

## Disclaimer

This system intentionally prioritizes analytical safety and correctness.
It may refuse to answer questions when required assumptions cannot be verified.

## Sample Outputs

<img width="1717" height="523" alt="image" src="https://github.com/user-attachments/assets/20c4b332-8559-43d7-8efd-bea874b051b4" />
<img width="835" height="398" alt="image" src="https://github.com/user-attachments/assets/f254f76b-2c61-448b-a562-b22e71c770fb" />
<img width="843" height="543" alt="image" src="https://github.com/user-attachments/assets/5336a2e9-d734-48ba-8d8e-c9652934291b" />
<img width="843" height="344" alt="image" src="https://github.com/user-attachments/assets/3c5ddac6-5734-4cbd-8ad1-6401d8146501" />
<img width="589" height="484" alt="image" src="https://github.com/user-attachments/assets/aaab6736-318d-479d-b6ec-be6a17215f3b" />
<img width="1794" height="467" alt="image" src="https://github.com/user-attachments/assets/b9bd0f4e-a9e7-45a2-9b4e-b09ef2bd5606" />
<img width="659" height="542" alt="image" src="https://github.com/user-attachments/assets/8c71ddb1-2eed-4426-bb47-0eeba29a4b11" />
<img width="568" height="379" alt="image" src="https://github.com/user-attachments/assets/4da30579-feed-46c7-ae3b-8b35ea64da2f" />








