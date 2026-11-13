"""Environment-backed application settings."""
import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "CURIOUSVERSE AI STUDIO")
    timezone: str = os.getenv("APP_TIMEZONE", "Asia/Dubai")
    database_path: Path = Path(os.getenv("DATABASE_PATH", "data/curiousverse.sqlite3"))
    output_dir: Path = Path(os.getenv("OUTPUT_DIR", "output"))
    ffmpeg_path: str = os.getenv("FFMPEG_PATH", "ffmpeg")
    youtube_default_privacy: str = os.getenv("YOUTUBE_DEFAULT_PRIVACY", "private").lower()
    youtube_public_publishing_enabled: bool = os.getenv(
        "YOUTUBE_PUBLIC_PUBLISHING_ENABLED", "false"
    ).lower() == "true"

    def validate(self) -> None:
        if self.youtube_default_privacy not in {"private", "unlisted"}:
            raise ValueError("Default YouTube privacy must be private or unlisted.")
        if self.youtube_public_publishing_enabled:
            raise ValueError("Public publishing is disabled until an explicit human approval workflow exists.")


settings = Settings()