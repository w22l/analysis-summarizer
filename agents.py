from crewai import Agent
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI

from config import Settings


class ArticleAnalysisAgents:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.llm = self._load_llm()

    def _load_llm(self):
        provider = self.settings.model_provider
        if provider == "openrouter":
            if not self.settings.openrouter_api_key:
                raise ValueError(
                    "OpenRouter selected but OPENROUTER_API_KEY is not configured."
                )
            return ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.settings.openrouter_api_key,
                model=self.settings.openrouter_model,
                temperature=0.3,
            )

        if provider == "ollama":
            return Ollama(model=self.settings.ollama_model)

        raise ValueError(f"Unsupported model provider '{provider}'.")

    def summarizer_agent(self):
        return Agent(
            role="Article Summarizer",
            goal="Summarize the key points of an article.",
            backstory="You are an expert in summarizing articles, able to extract the most important information and present it in a concise and easy-to-understand format.",
            verbose=True,
            memory=True,
            llm=self.llm
        )

    def assumptions_agent(self):
        return Agent(
            role="Assumption Identifier",
            goal="Identify the underlying assumptions in an article.",
            backstory="You have a keen eye for identifying hidden assumptions and biases in written content. You can uncover the author's underlying beliefs and perspectives.",
            verbose=True,
            memory=True,
            llm=self.llm
        )

    def errors_agent(self):
        return Agent(
            role="Error and Bias Detector",
            goal="Identify potential factual errors, logical fallacies, and biases in an article.",
            backstory="You are a meticulous fact-checker and critical thinker, able to spot inconsistencies, logical flaws, and biased language in any text.",
            verbose=True,
            memory=True,
            llm=self.llm
        )
