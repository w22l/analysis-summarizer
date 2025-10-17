# Article Analysis and Summarization Agent

An AI-powered toolkit that ingests long-form articles, surfaces executive summaries, interrogates underlying assumptions, and flags potential errors or biases. The project is designed with GitHub Spec Kit artifacts to ensure clear constitution, specification, planning, and task breakdown prior to execution.

## Highlights
- **Spec-Driven Design:** See `spec/` for the constitution, implementation plan, and task definitions produced with GitHub Spec Kit principles.
- **CrewAI Orchestration:** Specialized agents collaborate sequentially to cover summarization, assumption analysis, and error detection.
- **Modern CLI Experience:** Typer + Rich interface with commands for running analyses, inspecting configuration, viewing history, and auditing the article cache.
- **Flexible LLM Backends:** Choose between `xai/grok-4-fast` via OpenRouter or local `gpt-oss:20b` via Ollama.
- **Persistent Storage:** SQLite ledger caches article content and tracks generated reports.
- **Markdown Deliverables:** Reports are saved to disk (default `output/`) and rendered in-terminal for quick review.

## Tech Stack
- **Python 3.8+**
- **CrewAI**
- **LangChain (OpenAI + Ollama integrations)**
- **Typer / Rich**
- **SQLite (standard library `sqlite3`)**
- **Requests + BeautifulSoup4 for article acquisition**
- **GitHub Spec Kit documentation (`spec/` directory)**

## Setup

1. **Clone and install dependencies**
   ```bash
   git clone https://github.com/w22l/analysis-summarizer.git
   cd analysis-summarizer
   pip install -r requirements.txt
   ```

2. **Configure the environment**
   Create a `.env` file (sample values shown below):
   ```
   OPENROUTER_API_KEY="your_openrouter_api_key"  # required when MODEL_PROVIDER=openrouter
   MODEL_PROVIDER="openrouter"                   # options: openrouter, ollama
   OPENROUTER_MODEL="xai/grok-4-fast"
   OLLAMA_MODEL="gpt-oss:20b"
   OUTPUT_DIR="output"
   DATABASE_PATH="data/analysis.db"
   ```

   - Install [Ollama](https://ollama.ai/) and pull `gpt-oss:20b` if using the local model.
   - Obtain an [OpenRouter](https://openrouter.ai/) API key for hosted model access.

3. **Verify the spec**
   Review `spec/constitution.md`, `spec/spec.md`, `spec/plan.md`, and `spec/tasks.md` to understand the design intent that guides the implementation.

## CLI Usage

All commands are executed through the Typer CLI housed in `main.py`.

### Analyze an article
```bash
python main.py analyze "https://example.com/article" --output ./output --model openrouter
```
- Downloads (or reuses cached) article content.
- Runs the CrewAI workflow.
- Writes a markdown report to the chosen output directory.

### Inspect configuration
```bash
python main.py show-config
```

### Review analysis history
```bash
python main.py history --limit 5
```

### List cached articles
```bash
python main.py cache --limit 5
```

Use `--help` on any command for additional options.

## Generated Reports

- Saved as markdown files in the configured `OUTPUT_DIR`.
- File names include a timestamp and slugified article title or URL.
- Each report contains metadata, executive summary bullets, authorial assumptions, and a table of potential errors/biases.
- The associated metadata is recorded in SQLite for later retrieval.

## Project Layout
```
.
├── agents.py
├── article_service.py
├── config.py
├── main.py
├── requirements.txt
├── spec/
│   ├── constitution.md
│   ├── plan.md
│   ├── spec.md
│   └── tasks.md
├── storage.py
├── tasks.py
├── output/
└── data/            # created at runtime for the SQLite database
```

## Contributing

Pull requests and feedback are welcome. Please align changes with the existing spec kit documentation or update the spec accordingly.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
