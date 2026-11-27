# Roadmap

Each PR has its own feature spec in `specs/features/<name>/`.

## MVP

| PR | Scope | Location |
|---|---|---|
| #1 | Deterministic client for the local ActivityWatch API, with session aggregation (issue #1) | `src/cognitive_agent/ingestion/` |
| #2 | Content ingestion from `inbox/` and Notion, cleaning, hash deduplication, Qdrant storage and index rebuild from Markdown notes | `ingestion/`, `processing/` |
| #3 | Curator agent on Azure AI Foundry SDK with RAG tool calling (create, update, discard) and CLI approval | `src/cognitive_agent/agent/` |
| #4 | Evaluation suite of 20 to 25 synthetic edge cases | `evals/` |

PR #1 is fully local and deterministic, and produces no report.

Pass thresholds for PR #4 are written in its spec before the first evaluation run.

## Phase 2 (out of MVP scope)

- Docker packaging
- Redis caching, only if a measured bottleneck justifies it
- Chrome extension for web highlights
- YouTube transcripts
- Approval through Telegram
- ActivityWatch as a passive context trigger: work in selected apps or pages (for example PDF,
  Notion, Gemini, IDE; selectable later) activates the curator to capture relevant information
  without manual highlighting, after a validity and correctness check
