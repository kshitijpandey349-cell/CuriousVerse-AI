"""Command-line health check."""
import shutil
from app.config import settings
from app.database import initialize_database


def main():
    settings.validate()
    initialize_database()
    print(f"{settings.app_name} — foundation check")
    print(f"Timezone: {settings.timezone}")
    print(f"Database: {settings.database_path.resolve()}")
    print(f"FFmpeg: {shutil.which(settings.ffmpeg_path) or 'not installed (optional for now)'}")
    print("Database initialized successfully.")


if __name__ == "__main__":
    main()