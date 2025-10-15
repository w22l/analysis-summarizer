from crewai import Task
import requests
from bs4 import BeautifulSoup

class ArticleAnalysisTasks:
    def _fetch_article_content(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            soup = BeautifulSoup(response.text, 'html.parser')
            # This is a simple example; a more robust solution would involve
            # more sophisticated content extraction logic.
            paragraphs = soup.find_all('p')
            article_text = '\n'.join([p.get_text() for p in paragraphs])
            return article_text
        except requests.exceptions.RequestException as e:
            return f"Error fetching article: {e}"

    def summarize_article(self, agent, url):
        article_content = self._fetch_article_content(url)
        return Task(
            description=f'Summarize the following article:\n\n{article_content}',
            agent=agent,
            expected_output="A concise summary of the article's key points in markdown format."
        )

    def identify_assumptions(self, agent, url):
        article_content = self._fetch_article_content(url)
        return Task(
            description=f'Identify the underlying assumptions in the following article:\n\n{article_content}',
            agent=agent,
            expected_output="A list of the author's underlying assumptions in markdown format."
        )

    def identify_errors(self, agent, url):
        article_content = self._fetch_article_content(url)
        return Task(
            description=f'Identify potential factual errors, logical fallacies, and biases in the following article:\n\n{article_content}',
            agent=agent,
            expected_output="A list of potential errors and biases in the article, with explanations, in markdown format."
        )

