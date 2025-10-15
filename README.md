# Article Analysis and Summarization Agent

This project contains an AI agent designed to analyze articles and generate summaries of key points, identify underlying assumptions, and list potential errors or biases. The agent is built using the CrewAI framework and can be configured to use either a local `gpt-oss:20b` model via Ollama or the `xai-grok-4-fast` model via OpenRouter.

## Features

- **Summarization:** Extracts and condenses the key points from an article.
- **Assumption Identification:** Uncovers the underlying assumptions made by the author.
- **Error and Bias Detection:** Identifies potential factual errors, logical fallacies, and biases in the text.
- **Markdown Output:** Generates a well-structured markdown report of the analysis.
- **Flexible Model Selection:** Supports both local and remote large language models.

## Tech Stack

- **CrewAI:** A framework for orchestrating autonomous AI agents.
- **Large Language Models (LLMs):**
  - `gpt-oss:20b` via Ollama (local)
  - `xai-grok-4-fast` via OpenRouter (remote)
- **Python:** The core programming language.

## Getting Started

### Prerequisites

- Python 3.8+
- Pip for package management
- Ollama (if using the local `gpt-oss:20b` model)
- An OpenRouter account and API key (if using the `xai-grok-4-fast` model)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/w22l/analysis-summarizer.git
   cd analysis-summarizer
   ```

2. **Install the required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment variables:**
   - Create a `.env` file in the root of the project.
   - If using OpenRouter, add the following line:
     ```
     OPENROUTER_API_KEY="your_openrouter_api_key"
     ```

### Running the Agent

To run the agent, you will need to provide the URL of the article you want to analyze.

```bash
python main.py --url "https://example.com/article"
```

The agent will process the article and generate a markdown file in the `output` directory containing the analysis.

## Project Structure

```
.
├── README.md
├── main.py
├── requirements.txt
├── agents.py
├── tasks.py
└── output/
```

- `main.py`: The main entry point for the application.
- `requirements.txt`: A list of the Python packages required for the project.
- `agents.py`: Defines the different AI agents used in the analysis process.
- `tasks.py`: Defines the tasks that the agents will perform.
- `output/`: The directory where the generated markdown files are saved.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or find any bugs.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.