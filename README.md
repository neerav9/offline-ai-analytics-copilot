# Offline AI Analytics Copilot

An offline AI analytics copilot that answers business questions using deterministic computation and local language models for explainable insights.

## Overview
This project aims to build a safe, offline-first AI system that assists with data analysis by combining deterministic analytics pipelines with AI-based explanation.

## Status
🚧 Version 1 (V1) — In Progress

More details will be added as the project evolves.

## Supported Question Types (V1)

The system supports a fixed set of analytical intents. Each intent maps to a deterministic analytics pipeline.

| Intent  | Core Metrics Used                       |
| ------- | --------------------------------------- |
| SUMMARY | total revenue, units, revenue by region |
| TREND   | revenue by time                         |
| COMPARE | grouped revenue                         |
| RANK    | sorted revenue                          |
| WHY     | delta + breakdown                       |

Questions outside this scope are intentionally rejected to ensure reliability and explainability.


