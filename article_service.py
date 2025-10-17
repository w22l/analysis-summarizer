import hashlib
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple

import requests
from bs4 import BeautifulSoup

from storage import ArticleRecord, ArticleRepository


class ArticleDownloadError(Exception):
    """Raised when an article cannot be downloaded or parsed."""


@dataclass
class ArticlePayload:
    record: ArticleRecord
    content: str
    title: Optional[str]


class ArticleService:
    def __init__(self, repository: ArticleRepository):
        self.repository = repository

    def get_article(self, url: str) -> ArticlePayload:
        cached = self.repository.get_article(url)
        if cached:
            return ArticlePayload(record=cached, content=cached.content, title=cached.title)

        content, title = self._download_article(url)
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        record = self.repository.save_article(
            url=url,
            title=title,
            content=content,
            content_hash=content_hash,
            fetched_at=datetime.utcnow(),
        )
        return ArticlePayload(record=record, content=content, title=title)

    def _download_article(self, url: str) -> Tuple[str, Optional[str]]:
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise ArticleDownloadError(f"Failed to fetch article: {exc}") from exc

        soup = BeautifulSoup(response.text, "html.parser")
        title = self._extract_title(soup)
        content = self._extract_body(soup)

        if not content.strip():
            raise ArticleDownloadError("Unable to extract article content.")

        return content, title

    @staticmethod
    def _extract_title(soup: BeautifulSoup) -> Optional[str]:
        if soup.title and soup.title.string:
            return soup.title.string.strip()
        heading = soup.find("h1")
        if heading and heading.get_text():
            return heading.get_text().strip()
        return None

    @staticmethod
    def _extract_body(soup: BeautifulSoup) -> str:
        article_tag = soup.find("article")
        paragraphs = (
            article_tag.find_all("p") if article_tag else soup.find_all("p")
        )
        text_segments = []
        for paragraph in paragraphs:
            text = paragraph.get_text(strip=True)
            if text:
                text_segments.append(text)
        return "\n\n".join(text_segments)
