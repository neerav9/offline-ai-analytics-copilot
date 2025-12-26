# Offline AI Analytics Copilot

A correctness-first, offline analytics system that safely analyzes unknown datasets by reasoning about schema, semantic meaning, and analytical validity before execution.

---

## Problem Statement

Most analytics tools assume the dataset schema in advance.
When the schema is unfamiliar, incomplete, or misleading, these systems often:

- produce incorrect metrics,
- silently enable invalid analysis,
- or hallucinate insights without warning.

This project addresses a core question:

**How can an analytics system reason about an unknown dataset and refuse unsafe analysis instead of producing misleading results?**

---

## Core Idea

The system follows a **schema-driven, capability-gated analytics approach**:

1. Inspect the dataset and extract schema signals (types, distributions, uniqueness)
2. Propose semantic mappings to a canonical analytical schema
3. Require human confirmation for ambiguous mappings
4. Build a canonical representation of the data
5. Enable or disable analytics based on confirmed schema capabilities
6. Execute only safe, explainable analytics
7. Explicitly explain assumptions, risks, and disabled analyses

All computation runs **offline** using deterministic logic.
No external APIs or cloud services are required.

---

## System Evolution

The project was built iteratively, with each version addressing a specific analytical failure mode.

### Version 1 — Deterministic Analytics Core
- Implemented fixed, intent-based analytics (summary, trend, rank, compare)
- Mapped each intent to deterministic metric functions
- Rejected unsupported questions by design

**Focus:** Reliable computation over flexibility

---

### Version 2 — Data Inspection & Guided Analytics
- Added dataset inspection (shape, missing values, duplicates, numeric consistency)
- Introduced AI-assisted data quality suggestions
- Implemented guided analytics to restrict users to valid analysis paths

**Focus:** Preventing bad analysis caused by dirty or incomplete data

---

### Version 3 — Schema Reasoning & Semantic Mapping
- Extracted schema signals from unknown datasets
- Proposed semantic mappings to a canonical schema
- Required human confirmation for ambiguous fields
- Enabled or disabled analytics based on confirmed schema
- Added system-level reasoning to explain assumptions, risks, and limitations

**Focus:** Preventing analytics on semantically invalid data

---

## Supported Analytical Intents

The system supports a fixed set of analytical intents.
Each intent maps to a deterministic pipeline and is enabled only when required schema conditions are met.

| Intent   | Description                          | Required Schema Signals        |
|-------- |--------------------------------------|--------------------------------|
| SUMMARY | Aggregate metric overview             | metric                         |
| TREND   | Metric over time                      | metric + date                  |
| RANK    | Rank entities by metric               | metric + entity                |
| COMPARE | Compare metric across categories      | metric + category              |
| WHY     | Explain change drivers                | metric + time + grouping       |

If required schema signals are missing or unconfirmed, the intent is **disabled**, not approximated.

---

## Example Behavior

- A sales dataset enables summary, ranking, comparison, and trend analysis.
- A student marks dataset enables summary and ranking, but disables comparison if no category is confirmed.
- If a required field is rejected during semantic mapping, dependent analytics are automatically blocked.

The system explains **why** each analysis is enabled or disabled.

---

## Key Design Principles

- Correctness over coverage
- Explicit refusal over silent failure
- Deterministic logic over black-box ML
- Human-in-the-loop for semantic ambiguity
- Explainability at every stage

---

## Use Cases

- Safely analyzing unfamiliar CSV datasets
- Auditing analytics assumptions
- Preventing misleading dashboards
- Teaching schema-aware analytics reasoning
- Offline analytics in restricted environments

---

## Current Status

✅ **Version 3 complete** — Schema reasoning, semantic mapping, and capability-gated analytics implemented.

---

## Roadmap

- V4: Domain-agnostic metric generalization
- V5: Pluggable domain packs (education, finance, operations)
- V6: Optional local LLM-based explanation layer (offline)

---

## Disclaimer

This project intentionally prioritizes analytical safety and correctness over coverage.
It may refuse to answer questions when required assumptions cannot be verified.
