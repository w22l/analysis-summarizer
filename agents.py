from crewai import Agent
import os

class ArticleAnalysisAgents:
    def __init__(self):
        # In a real-world scenario, you would load the LLM configuration from a
        # configuration file or environment variables.
        # For this example, we'll use placeholders.
        self.llm = None  # Replace with your LLM configuration

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
