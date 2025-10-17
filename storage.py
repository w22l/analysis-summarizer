import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional


@dataclass
class ArticleRecord:
    id: int
    url: str
    title: Optional[str]
    content: str
    content_hash: str
    fetched_at: datetime


@dataclass
class AnalysisRecord:
    id: int
    article_url: str
    article_title: Optional[str]
    output_path: str
    model_provider: str
    model_name: str
    created_at: datetime


class ArticleRepository:
    def __init__(self, database_path: Path):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE NOT NULL,
                    title TEXT,
                    content TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    fetched_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    article_id INTEGER NOT NULL,
                    model_provider TEXT NOT NULL,
                    model_name TEXT NOT NULL,
                    output_path TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(article_id) REFERENCES articles(id)
                )
                """
            )

    def get_article(self, url: str) -> Optional[ArticleRecord]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM articles WHERE url = ?", (url,)
            ).fetchone()
            if not row:
                return None
            return self._row_to_article(row)

    def save_article(
        self,
        *,
        url: str,
        title: Optional[str],
        content: str,
        content_hash: str,
        fetched_at: datetime,
    ) -> ArticleRecord:
        fetched_iso = fetched_at.isoformat()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO articles (url, title, content, content_hash, fetched_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(url) DO UPDATE SET
                    title = excluded.title,
                    content = excluded.content,
                    content_hash = excluded.content_hash,
                    fetched_at = excluded.fetched_at
                """,
                (url, title, content, content_hash, fetched_iso),
            )
            row = conn.execute(
                "SELECT * FROM articles WHERE url = ?", (url,)
            ).fetchone()
            return self._row_to_article(row)

    def record_analysis(
        self,
        *,
        article_id: int,
        model_provider: str,
        model_name: str,
        output_path: Path,
        created_at: datetime,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO analyses (article_id, model_provider, model_name, output_path, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    article_id,
                    model_provider,
                    model_name,
                    str(output_path),
                    created_at.isoformat(),
                ),
            )

    def list_recent_analyses(self, limit: int = 10) -> List[AnalysisRecord]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT
                    analyses.id,
                    articles.url as article_url,
                    articles.title as article_title,
                    analyses.output_path,
                    analyses.model_provider,
                    analyses.model_name,
                    analyses.created_at
                FROM analyses
                INNER JOIN articles ON analyses.article_id = articles.id
                ORDER BY analyses.created_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
            records = []
            for row in rows:
                records.append(
                    AnalysisRecord(
                        id=row["id"],
                        article_url=row["article_url"],
                        article_title=row["article_title"],
                        output_path=row["output_path"],
                        model_provider=row["model_provider"],
                        model_name=row["model_name"],
                        created_at=datetime.fromisoformat(row["created_at"]),
                    )
                )
            return records

    def list_cached_articles(self, limit: int = 10) -> List[ArticleRecord]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM articles ORDER BY fetched_at DESC LIMIT ?", (limit,)
            ).fetchall()
            return [self._row_to_article(row) for row in rows]

    @staticmethod
    def _row_to_article(row: sqlite3.Row) -> ArticleRecord:
        return ArticleRecord(
            id=row["id"],
            url=row["url"],
            title=row["title"],
            content=row["content"],
            content_hash=row["content_hash"],
            fetched_at=datetime.fromisoformat(row["fetched_at"]),
        )
