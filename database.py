"""SQLite persistence foundation."""
import sqlite3
from contextlib import closing
from pathlib import Path
from app.config import settings

SCHEMA = """
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'general',
    status TEXT NOT NULL DEFAULT 'idea',
    notes TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS production_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER REFERENCES topics(id),
    format TEXT NOT NULL CHECK(format IN ('short', 'long')),
    status TEXT NOT NULL DEFAULT 'queued',
    output_path TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER REFERENCES production_jobs(id),
    youtube_video_id TEXT UNIQUE,
    privacy_status TEXT NOT NULL DEFAULT 'private',
    approval_status TEXT NOT NULL DEFAULT 'pending',
    uploaded_at TEXT
);
"""


def connect(db_path=None):
    path = Path(db_path or settings.database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(db_path=None):
    connection = connect(db_path)
    try:
        with connection:
            connection.executescript(SCHEMA)
    finally:
        connection.close()


def add_topic(title, category="general", notes="", db_path=None):
    title = (title or "").strip()
    if not title:
        raise ValueError("Topic title cannot be empty.")
    with closing(connect(db_path)) as connection, connection:
        cursor = connection.execute(
            "INSERT INTO topics (title, category, notes) VALUES (?, ?, ?)",
            (title, (category or "").strip() or "general", (notes or "").strip()),
        )
        return cursor.lastrowid


def list_topics(limit=100, db_path=None):
    with closing(connect(db_path)) as connection:
        return list(connection.execute(
            "SELECT * FROM topics ORDER BY created_at DESC, id DESC LIMIT ?",
            (max(1, min(int(limit), 500)),),
        ))