import sqlite3

import pytest

from app.config import Settings
from app.database import add_topic, initialize_database, list_topics


def test_private_default():
    assert Settings().youtube_default_privacy in {"private", "unlisted"}


def test_public_upload_is_blocked():
    with pytest.raises(ValueError):
        Settings(youtube_public_publishing_enabled=True).validate()


def test_invalid_privacy_rejected():
    with pytest.raises(ValueError):
        Settings(youtube_default_privacy="public").validate()


def test_settings_read_environment_at_creation(monkeypatch):
    monkeypatch.setenv("APP_TIMEZONE", "UTC")
    monkeypatch.setenv("YOUTUBE_DEFAULT_PRIVACY", "UNLISTED")
    s = Settings()
    assert s.timezone == "UTC"
    assert s.youtube_default_privacy == "unlisted"
    s.validate()


def test_public_flag_from_environment_is_blocked(monkeypatch):
    monkeypatch.setenv("YOUTUBE_PUBLIC_PUBLISHING_ENABLED", "true")
    with pytest.raises(ValueError):
        Settings().validate()


def test_optional_integrations_report_unconfigured(monkeypatch):
    for name in ("PIPER_EXECUTABLE", "PIPER_MODEL_PATH", "WHISPER_CPP_PATH", "YOUTUBE_CLIENT_SECRETS_FILE"):
        monkeypatch.delenv(name, raising=False)
    status = Settings().optional_integrations()
    assert status["Piper TTS"] is False
    assert status["whisper.cpp"] is False
    assert status["YouTube OAuth client"] is False


def test_database_schema_initializes(tmp_path):
    path = tmp_path / "test.sqlite3"
    initialize_database(path)
    connection = sqlite3.connect(path)
    tables = {row[0] for row in connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )}
    connection.close()
    assert {"topics", "production_jobs", "uploads"} <= tables


def test_initialize_database_is_idempotent(tmp_path):
    path = tmp_path / "test.sqlite3"
    initialize_database(path)
    initialize_database(path)


def test_add_and_list_topics(tmp_path):
    path = tmp_path / "test.sqlite3"
    initialize_database(path)
    first = add_topic("  Why is the sky blue?  ", "science", " Rayleigh scattering ", db_path=path)
    second = add_topic("How do black holes form?", "space", db_path=path)
    rows = list_topics(db_path=path)
    assert [r["id"] for r in rows] == [second, first]  # newest first
    saved = {r["id"]: r for r in rows}[first]
    assert saved["title"] == "Why is the sky blue?"
    assert saved["notes"] == "Rayleigh scattering"
    assert saved["status"] == "idea"


def test_blank_category_defaults_to_general(tmp_path):
    path = tmp_path / "test.sqlite3"
    initialize_database(path)
    add_topic("Topic", "   ", db_path=path)
    assert list_topics(db_path=path)[0]["category"] == "general"


@pytest.mark.parametrize("title", ["", "   ", None])
def test_empty_topic_title_rejected(tmp_path, title):
    path = tmp_path / "test.sqlite3"
    initialize_database(path)
    with pytest.raises(ValueError):
        add_topic(title, db_path=path)
    assert list_topics(db_path=path) == []


def test_list_topics_limit_is_bounded(tmp_path):
    path = tmp_path / "test.sqlite3"
    initialize_database(path)
    for i in range(5):
        add_topic(f"Topic {i}", db_path=path)
    assert len(list_topics(limit=2, db_path=path)) == 2
    assert len(list_topics(limit=0, db_path=path)) == 1  # clamped to minimum 1


def test_production_job_format_constraint(tmp_path):
    path = tmp_path / "test.sqlite3"
    initialize_database(path)
    connection = sqlite3.connect(path)
    with pytest.raises(sqlite3.IntegrityError):
        connection.execute("INSERT INTO production_jobs (format) VALUES ('medium')")
    connection.close()


def test_dashboard_renders_without_errors(tmp_path, monkeypatch):
    from pathlib import Path
    from streamlit.testing.v1 import AppTest
    dashboard = Path(__file__).resolve().parents[1] / "app" / "dashboard.py"
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "dash.sqlite3"))
    import app.config as config
    import app.database as database
    monkeypatch.setattr(config, "settings", config.Settings())
    monkeypatch.setattr(database, "settings", config.settings)
    at = AppTest.from_file(str(dashboard), default_timeout=20).run()
    assert not at.exception
    assert any("Optional integrations" in s.value for s in at.sidebar.subheader)
