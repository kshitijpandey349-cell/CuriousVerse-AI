from app.config import Settings
from app.database import initialize_database
import sqlite3
import pytest


def test_private_default():
    assert Settings().youtube_default_privacy in {"private", "unlisted"}


def test_public_upload_is_blocked():
    with pytest.raises(ValueError):
        Settings(youtube_public_publishing_enabled=True).validate()


def test_database_schema_initializes(tmp_path):
    path = tmp_path / "test.sqlite3"
    initialize_database(path)
    connection = sqlite3.connect(path)
    tables = {row[0] for row in connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )}
    connection.close()
    assert {"topics", "production_jobs", "uploads"} <= tables