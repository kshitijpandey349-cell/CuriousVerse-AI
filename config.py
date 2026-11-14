"""Environment-backed application settings."""
import os
from dataclasses import dataclass, field
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def _env(name: str, default: str) -> str:
    return os.getenv(name, default)


@dataclass(frozen=True)
class Settings:
    # default_factory reads the environment when Settings() is created,
    # not once at import time, so tests and reloads see current values.
    app_name: str = field(default_factory=lambda: _env("APP_NAME", "CURIOUSVERSE AI STUDIO"))
    app_env: str = field(default_factory=lambda: _env("APP_ENV", "development"))
    timezone: str = field(default_factory=lambda: _env("APP_TIMEZONE", "Asia/Dubai"))
    database_path: Path = field(default_factory=lambda: Path(_env("DATABASE_PATH", "data/curiousverse.sqlite3")))
    output_dir: Path = field(default_factory=lambda: Path(_env("OUTPUT_DIR", "output")))
    log_level: str = field(default_factory=lambda: _env("LOG_LEVEL", "INFO").upper())
    ffmpeg_path: str = field(default_factory=lambda: _env("FFMPEG_PATH", "ffmpeg"))
    piper_executable: str = field(default_factory=lambda: _env("PIPER_EXECUTABLE", ""))
    piper_model_path: str = field(default_factory=lambda: _env("PIPER_MODEL_PATH", ""))
    whisper_cpp_path: str = field(default_factory=lambda: _env("WHISPER_CPP_PATH", ""))
    youtube_client_secrets_file: str = field(default_factory=lambda: _env("YOUTUBE_CLIENT_SECRETS_FILE", ""))
    youtube_token_file: str = field(default_factory=lambda: _env("YOUTUBE_TOKEN_FILE", "secrets/youtube-token.json"))
    youtube_default_privacy: str = field(default_factory=lambda: _env("YOUTUBE_DEFAULT_PRIVACY", "private").lower())
    youtube_public_publishing_enabled: bool = field(
        default_factory=lambda: _env("YOUTUBE_PUBLIC_PUBLISHING_ENABLED", "false").lower() == "true"
    )
    llm_provider: str = field(default_factory=lambda: _env("LLM_PROVIDER", "manual"))

    def validate(self) -> None:
        if self.youtube_default_privacy not in {"private", "unlisted"}:
            raise ValueError("Default YouTube privacy must be private or unlisted.")
        if self.youtube_public_publishing_enabled:
            raise ValueError("Public publishing is disabled until an explicit human approval workflow exists.")

    def optional_integrations(self) -> dict:
        """Report which optional integrations are configured (never reveals secret values)."""
        import shutil
        return {
            "FFmpeg": bool(shutil.which(self.ffmpeg_path)),
            "Piper TTS": bool(self.piper_executable and self.piper_model_path),
            "whisper.cpp": bool(self.whisper_cpp_path),
            "YouTube OAuth client": bool(self.youtube_client_secrets_file),
        }


settings = Settings()
