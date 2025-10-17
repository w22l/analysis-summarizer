# Article Analysis Agent Specification

## Overview
An orchestration layer built with CrewAI coordinating specialized agents to ingest an article, generate key-point summaries, uncover assumptions, and enumerate probable errors or biases. Output must be a cohesive markdown report saved to disk and optionally printed to stdout.

## Architecture
- **CLI Frontend:** Typer-based command-line app with Rich-powered UX.
- **Agent Orchestration:** CrewAI sequential crew of summarizer, assumptions analyst, and error checker.
- **LLM Backends:** 
  - Primary: `xai/grok-4-fast` via OpenRouter.
  - Secondary: `gpt-oss:20b` via Ollama fallback.
- **Data Layer:** SQLite database (`analysis.db`) storing raw articles, fetch metadata, and analysis history.
- **Config:** `.env` loaded with dotenv; CLI flags override defaults for output path, model choice, and database location.

## Data Flow
1. CLI validates inputs, resolves config, and ensures output/database paths.
2. ArticleRepository checks SQLite cache; fetches via Requests + BeautifulSoup when absent and stores content.
3. CrewAI tasks operate on shared article payload, leveraging a single LLM instance.
4. Final markdown report assembled and saved to target directory.

## Non-Functional Requirements
- **Reliability:** Graceful error handling for network failures and model invocation issues.
- **Observability:** Verbose toggle, structured logging for agent actions.
- **Portability:** Pure Python dependencies; works on macOS/Linux.
- **Extensibility:** Modular task definitions and repository abstraction for future data sources.
