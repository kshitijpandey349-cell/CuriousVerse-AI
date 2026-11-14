# CURIOUSVERSE AI STUDIO

A local-first workspace for researching, scripting, producing and safely preparing original educational YouTube videos.

**Current status:** foundation scaffold. The initial dashboard and local database are intended to run without API credentials. Research automation, narration, rendering, quality gates, YouTube uploads and scheduling are later milestones and must not be described as complete until implemented and tested.

## Channel
Science, space, technology, history and everyday mysteries for a general English-speaking audience.

## Publishing targets
- One Short daily: 30–60 seconds, 9:16.
- One long video daily: 5–8 minutes, 16:9.
- Timezone: Asia/Dubai.

Targets are not reasons to publish rushed or duplicate content. Public publishing must require human review.

## Requirements
Windows 11, Python 3.11+, Git. Optional: FFmpeg, Piper TTS, whisper.cpp. YouTube integration requires a Google Cloud project and OAuth desktop credentials.

## Quick start (PowerShell)
    py -3.12 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    Copy-Item .env.example .env
    streamlit run app/dashboard.py

If activation is blocked:
    Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

Alternative without activation:
    .\.venv\Scripts\python.exe -m streamlit run app/dashboard.py

## Tests
    python -m pytest
    # or: pytest   (pytest.ini puts the repo root on the import path)

## Local-only dashboard
`.streamlit/config.toml` binds Streamlit to `localhost` and disables usage statistics. The sidebar and `python -m app.main` list which optional integrations (FFmpeg, Piper, whisper.cpp, YouTube OAuth) are configured.

## Security
Never commit .env, Google OAuth client secrets, refresh tokens or access tokens. Never share Google passwords or tokens in chat. Use official Google OAuth and YouTube Data API. Start with private/unlisted uploads.

## Limitations
- Claude Code is a coding agent, not an unlimited video-generation or TTS API.
- Local tools have hardware and model limits.
- A powered-off laptop cannot run scheduled jobs. Jobs can resume after startup, or run on an always-on server.
- This repository is a foundation, not yet a completed end-to-end automation system.

Read CLAUDE.md and docs/ARCHITECTURE.md before development.