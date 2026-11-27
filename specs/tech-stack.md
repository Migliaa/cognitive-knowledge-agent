# Tech Stack

A dependency not listed here needs an update to this file in the PR that adds it.

## Core

- Python 3.12+
- `httpx` for HTTP, `pydantic` v2 for data models and validation
- `pytest`, `ruff`, `mypy` (strict)

## Sources

- ActivityWatch local REST API, `http://localhost:5600/api/0/`
- Local files in `inbox/` at the repository root, ignored by Git
- Notion API, read-only

Each source sits behind a common boundary so that new ones can be added without changing
processing or the agent.

## Storage

- Curated notes: local Markdown files in `notes/` (source of truth)
- Vector database: Qdrant in local on-disk mode, stored in `qdrant_data/`, with a later path to
  Docker or Qdrant Cloud. Moving to Qdrant Cloud would change the data boundaries in `mission.md`.
- `inbox/`, `notes/` and `qdrant_data/` sit at the repository root and are ignored by Git;
  `tests/test_private_data_ignored.py` enforces it.

## AI

- Curator agent: Azure AI Foundry SDK, with tool calling over the RAG
- Embeddings: a model hosted on Azure AI Foundry
- Evaluations: Azure AI Foundry Evaluations

Exact packages and models are chosen in the feature spec that first needs them.

## Human in the loop

Interactive approval in the CLI. Telegram is a Phase 2 candidate.

## Excluded from the MVP

| Technology | Reason |
|---|---|
| Redis | No measured bottleneck. Semantic caching is reconsidered in Phase 2 if one appears. |
| Docker | Local Qdrant and a virtual environment are enough to run the MVP. Packaging is Phase 2. |
| Kubernetes | A single-user local application has nothing to orchestrate. |
| Databricks | The data volume of one person's notes does not need a data platform. |
| n8n | Approval happens in the CLI, so no external workflow engine is needed. |
