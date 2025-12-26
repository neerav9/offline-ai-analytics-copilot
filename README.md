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

Sample Outputs 
---
```
$ python -m src.main
==================================================
V3 DATASET SCHEMA SIGNALS
==================================================
student_name: {'type': 'categorical', 'missing_count': 0, 'signals': {'unique_count': 4, 'sample_values': ['Rahul', 'Anita', 'Kiran', 'Meena']}}
maths: {'type': 'numeric', 'missing_count': 0, 'signals': {'min': 65.0, 'max': 92.0, 'mean': 80.75, 'is_integer_like': True, 'unique_count': 4}}
physics: {'type': 'numeric', 'missing_count': 0, 'signals': {'min': 70.0, 'max': 91.0, 'mean': 83.0, 'is_integer_like': True, 'unique_count': 4}}
chemistry: {'type': 'numeric', 'missing_count': 0, 'signals': {'min': 68.0, 'max': 94.0, 'mean': 80.5, 'is_integer_like': True, 'unique_count': 4}}
biology: {'type': 'numeric', 'missing_count': 0, 'signals': {'min': 72.0, 'max': 90.0, 'mean': 83.0, 'is_integer_like': True, 'unique_count': 3}}
total_marks: {'type': 'numeric', 'missing_count': 0, 'signals': {'min': 275.0, 'max': 365.0, 'mean': 327.25, 'is_integer_like': True, 'unique_count': 4}}
exam_date: {'type': 'date', 'missing_count': 0}

==================================================
V3 SEMANTIC MAPPING PROPOSALS
==================================================
revenue -> {'column': 'total_marks', 'confidence': 1.0, 'evidence': ['column_name_match', 'numeric_behavior', 'type_match']}
order_date -> {'column': 'exam_date', 'confidence': 0.8, 'evidence': ['column_name_match', 'type_match']}
category -> {'column': 'student_name', 'confidence': 0.2, 'evidence': ['type_match']}
units_sold -> {'column': 'maths', 'confidence': 0.5, 'evidence': ['numeric_behavior', 'type_match']}
unit_price -> {'column': 'maths', 'confidence': 0.5, 'evidence': ['numeric_behavior', 'type_match']}
entity_name -> {'column': 'student_name', 'confidence': 0.2, 'evidence': ['type_match']}

=== HUMAN CONFIRMATION REQUIRED ===

----------------------------------
Canonical field : revenue
Proposed column : total_marks
Confidence      : 1.0
Evidence        : column_name_match, numeric_behavior, type_match
Accept mapping? (y = accept / n = reject / custom = enter column name): y

----------------------------------
Canonical field : order_date
Proposed column : exam_date
Confidence      : 0.8
Evidence        : column_name_match, type_match
Accept mapping? (y = accept / n = reject / custom = enter column name): y

----------------------------------
Canonical field : category
Proposed column : student_name
Confidence      : 0.2
Evidence        : type_match
Accept mapping? (y = accept / n = reject / custom = enter column name): n
Skipping mapping for 'category'.

----------------------------------
Canonical field : units_sold
Proposed column : maths
Confidence      : 0.5
Evidence        : numeric_behavior, type_match
Accept mapping? (y = accept / n = reject / custom = enter column name): n
Skipping mapping for 'units_sold'.

----------------------------------
Canonical field : unit_price
Proposed column : maths
Confidence      : 0.5
Evidence        : numeric_behavior, type_match
Accept mapping? (y = accept / n = reject / custom = enter column name): n
Skipping mapping for 'unit_price'.

----------------------------------
Canonical field : entity_name
Proposed column : student_name
Confidence      : 0.2
Evidence        : type_match
Accept mapping? (y = accept / n = reject / custom = enter column name): y

==================================================
V3 CONFIRMED MAPPINGS
==================================================
revenue -> total_marks
order_date -> exam_date
entity_name -> student_name

==================================================
V3 CANONICAL DATAFRAME
==================================================
  entity_name  revenue  order_date
0       Rahul      315  2024-03-10
1       Anita      354  2024-03-10
2       Kiran      275  2024-03-10
3       Meena      365  2024-03-10

==================================================
SYSTEM REASONING (V3.9)
==================================================
Dataset shape: Entity–Metric–Time

Enabled analyses:
✓ Summary
✓ Ranking
✓ Trend

Disabled analyses:
✗ Comparison — Category not mapped

Assumptions:
• Metric values are comparable across records

Risks:
⚠ Low metric variance may reduce ranking reliability
⚠ Single time value limits trend analysis depth

==================================================
DATA INSPECTION REPORT
==================================================
{'shape': {'rows': 4, 'columns': 7}, 'missing_values': {'student_name': {'missing_count': 0, 'missing_percent': 0.0}, 'maths': {'missing_count': 0, 'missing_percen
t': 0.0}, 'physics': {'missing_count': 0, 'missing_percent': 0.0}, 'chemistry': {'missing_count': 0, 'missing_percent': 0.0}, 'biology': {'missing_count': 0, 'missing_percent': 0.0}, 'total_marks': {'missing_count': 0, 'missing_percent': 0.0}, 'exam_date': {'missing_count': 0, 'missing_percent': 0.0}}, 'duplicates': {'total_duplicate_rows': 0, 'duplicate_by_key': None}, 'numeric_checks': {'revenue_consistency': 'NOT_APPLICABLE'}}                                                        
==================================================
AI-ASSISTED SUGGESTIONS
==================================================
- No missing values detected. No null handling is required.
- No duplicate records detected.

==================================================
GUIDED ANALYTICS OPTIONS
==================================================
1. View summary
0. Exit

Select an option number to proceed: 1

==================================================
RESULT
==================================================
{'total_revenue': 1309}

==================================================
EXPLANATION
==================================================
Overall, total value is 1309.00.

==================================================
GUIDED ANALYTICS OPTIONS
==================================================
1. View summary
0. Exit

Select an option number to proceed: 0

Exiting guided analytics. Goodbye!
```

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
