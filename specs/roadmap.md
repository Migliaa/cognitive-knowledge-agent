# Roadmap

Each MVP milestone is one pull request with its own feature spec in `specs/features/<name>/`.
Milestone names are independent of GitHub issue and pull request numbers.

## MVP

| Milestone | Scope | Location |
|---|---|---|
| M1 | Deterministic client for the local ActivityWatch API, with session aggregation (issue #1) | `src/cognitive_agent/ingestion/` |
| M2 | Content ingestion from `inbox/` and Notion, cleaning and hash deduplication; Qdrant index of the curated Markdown notes, with index rebuild | `ingestion/`, `processing/` |
| M3 | Curator agent on Azure AI Foundry SDK with RAG tool calling (create, update, discard) and CLI approval | `src/cognitive_agent/agent/` |
| M4 | Evaluation suite of 20 to 25 synthetic edge cases | `evals/` |

M1 is fully local and deterministic, and produces no report.

Only curated notes are indexed in Qdrant. Raw texts ingested in M2 are not indexed: they are
cleaned and deduplicated for the curator. Embeddings are computed on Azure behind an interface
that tests can replace.

Pass thresholds for M4 are written in its spec before the first evaluation run.

## Phase 2 (out of MVP scope)

- Docker packaging
- Redis caching, only if a measured bottleneck justifies it
- Chrome extension for web highlights
- YouTube transcripts
- Approval through Telegram
- ActivityWatch as a passive context trigger: work in selected apps or pages (for example PDF,
  Notion, Gemini, IDE; selectable later) activates the curator to capture relevant information
  without manual highlighting, after a validity and correctness check

### Open questions for Phase 2

- Content capture: ActivityWatch records activity such as apps, window titles and, with its browser
  extension, URLs, but not page text. Which component reads the content?
- Privacy boundary: does text captured because of the trigger count as data derived from
  ActivityWatch? `mission.md` forbids that data from leaving the machine, while curating the text
  requires sending it to Azure.
