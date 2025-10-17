from typing import Optional

from crewai import Task


class ArticleAnalysisTasks:
    def __init__(self, *, article_body: str, url: str, title: Optional[str]):
        self.article_body = article_body
        self.url = url
        self.title = title

    def summarize_article(self, agent):
        return Task(
            description=(
                "You are provided with an article and must produce a crisp, executive summary "
                "highlighting primary claims, supporting evidence, and contextual framing.\n\n"
                f"Article URL: {self.url}\n"
                f"Article Title: {self.title or 'Unknown'}\n\n"
                f"Article Content:\n{self.article_body}"
            ),
            agent=agent,
            expected_output=(
                "A markdown bullet list (5-8 items) covering thesis, key evidence, and notable context."
            ),
        )

    def identify_assumptions(self, agent):
        return Task(
            description=(
                "Analyze the article to surface implicit and explicit assumptions made by the author. "
                "Explain why each assumption matters and note any evidence needed to validate it.\n\n"
                f"Article URL: {self.url}\n"
                f"Article Title: {self.title or 'Unknown'}\n\n"
                f"Article Content:\n{self.article_body}"
            ),
            agent=agent,
            expected_output=(
                "A markdown bullet list. Each bullet must include the assumption, rationale, and verification notes."
            ),
        )

    def identify_errors(self, agent):
        return Task(
            description=(
                "Review the article for potential factual inaccuracies, logical fallacies, or biased framing. "
                "Classify each finding by type and suggest verification steps.\n\n"
                f"Article URL: {self.url}\n"
                f"Article Title: {self.title or 'Unknown'}\n\n"
                f"Article Content:\n{self.article_body}"
            ),
            agent=agent,
            expected_output=(
                "A markdown table with columns Issue, Category, Confidence, and Recommended Verification."
            ),
        )
