# Mission

## Problem

Studying and working across different tools leaves scattered notes, and loses track of both where
attention went and what was learned.

## Product

A Personal Knowledge Curator (automated personal RAG) that:

1. tracks and aggregates real work and study sessions from ActivityWatch, locally;
2. compares each new note or raw text with the knowledge already stored, then creates a note,
   updates an existing one, or discards the input as noise;
3. stops and asks for human confirmation when the case is ambiguous or contradicts stored knowledge.

## Users

- The author, in daily use.
- Reviewers of this public repository, as a portfolio for AI Engineering internships (AI
  Solutions, AI Operations, AI Automation, AI Transformation).

## Principles

- **Privacy first.** The boundaries below are requirements.
- **Deterministic and AI layers are separate.** Collection, cleaning, deduplication and storage are
  plain Python that runs and is tested without a language model. Model-driven decisions live in
  `agent/`. Embedding calls sit behind an interface that tests can replace.
- **Measured behavior.** Deterministic code has automated tests; curator decisions have evaluations
  with recorded results, including failed cases.
- **Human authority.** The curator never resolves an ambiguous or contradictory case on its own.

## Data boundaries

| Data | Leaves the machine | Committed to Git |
|---|---|---|
| ActivityWatch events and anything derived from them | Never | Never |
| Text of inbox files, Notion pages and curated notes | To Azure AI Foundry, for embeddings and curation | Never |
| Embeddings and the Qdrant index | Embeddings are computed on Azure; the index stays local | Never |
| Evaluation cases | To Azure AI Foundry Evaluations | Yes, synthetic only |
| Credentials | Only to the service that issued them | Never |

Note content is therefore private from the repository but not local-only: all text that is curated
or indexed is sent to Azure. Content that must not reach a cloud service must not enter `inbox/` or the Notion sources.
Logs, test fixtures and published evaluation reports contain no personal data.

## Source of truth

Curated notes are local Markdown files in `notes/`, ignored by Git. The Qdrant index is derived
only from them and can be rebuilt at any time. Notion is a read-only source.
