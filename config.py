import os
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Container for runtime configuration."""

    model_provider: str
    openrouter_api_key: Optional[str]
    openrouter_model: str
    ollama_model: str
    output_dir: Path
    database_path: Path
    verbose: bool = False

    def with_overrides(
        self,
        *,
        model_provider: Optional[str] = None,
        output_dir: Optional[Path] = None,
        database_path: Optional[Path] = None,
        verbose: Optional[bool] = None,
    ) -> "Settings":
        """Return a copy of the settings with provided overrides applied."""
        return replace(
            self,
            model_provider=model_provider or self.model_provider,
            output_dir=(output_dir or self.output_dir),
            database_path=(database_path or self.database_path),
            verbose=self.verbose if verbose is None else verbose,
        )


def load_settings() -> Settings:
    """Load configuration from .env and environment variables."""
    load_dotenv()

    model_provider = os.getenv("MODEL_PROVIDER", "openrouter").strip().lower()
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY") or None
    openrouter_model = os.getenv("OPENROUTER_MODEL", "xai/grok-4-fast")
    ollama_model = os.getenv("OLLAMA_MODEL", "gpt-oss:20b")
    output_dir = Path(
        os.getenv("OUTPUT_DIR", "output")
    ).expanduser().resolve()
    database_path = Path(
        os.getenv("DATABASE_PATH", "data/analysis.db")
    ).expanduser().resolve()

    return Settings(
        model_provider=model_provider,
        openrouter_api_key=openrouter_api_key,
        openrouter_model=openrouter_model,
        ollama_model=ollama_model,
        output_dir=output_dir,
        database_path=database_path,
    )
