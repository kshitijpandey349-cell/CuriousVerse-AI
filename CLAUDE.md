# CURIOUSVERSE AI STUDIO

You are the lead engineer for this repository. Read this file before every task and inspect the existing code before editing. Build real, tested software; never present a placeholder as a completed feature.

## Product
A local-first Windows 11 application for planning, researching, scripting, producing and preparing original educational YouTube videos for CURIOUSVERSE.

Editorial areas: science, space, technology, history and everyday mysteries. Audience: general English-speaking viewers.

## Targets
- One Short daily: 30–60 seconds, vertical 9:16.
- One long video daily: 5–8 minutes, horizontal 16:9.
- Timezone: Asia/Dubai.
- Targets never justify rushed, duplicate or low-quality content.
- Default uploads to private or unlisted. Public publishing requires a deliberate human approval workflow.
- Respect Google/YouTube eligibility, OAuth, API, copyright and platform rules. Never bypass safeguards.

## Stack
Python 3.11+, Streamlit, SQLite, FFmpeg, Pillow, pytest. Optional integrations: Piper TTS, whisper.cpp, Google API Python Client and YouTube Data API v3.

Do not require paid APIs for core functionality. Do not assume Claude Code subscription access includes API access. Provide manual workflows and clearly label optional paid services.

## Modules
Research and source tracking; topic scoring; separate Short and long scripts; storyboard; narration; original/appropriately licensed visuals; FFmpeg editing; subtitles; thumbnails; media and rights quality checks; YouTube OAuth/upload; persistent scheduler; dashboard and logs.

## Engineering rules
1. Inspect repository and git status before edits.
2. Preserve working features and user data. Never delete unrelated files.
3. Support Windows 11 and 8 GB RAM: sequential jobs, conservative rendering, bounded queues.
4. Never commit credentials, OAuth tokens, .env files or personal data.
5. Do not reuse other creators' scripts, videos, thumbnails, music or footage without permission.
6. Record source URLs and asset license/attribution details. Never invent sources or claim verification that did not happen.
7. Important factual claims need trustworthy sources; flag uncertainty and conflicts.
8. No automated likes, comments, subscriptions, views or engagement manipulation.
9. A feature is complete only after implementation and tests.
10. Never report unrun tests as passing.

## Security and publishing
Do not collect Google passwords. Store OAuth tokens locally in ignored files. Bind the dashboard to localhost by default. Upload privately/unlisted by default. Never publish publicly without explicit human approval and compliance with account requirements.

## Roadmap
M0 foundation/config/database/dashboard.
M1 research and source verification.
M2 script editor and storyboard.
M3 narration and audio validation.
M4 original visuals and licensed asset registry.
M5 FFmpeg renderer, subtitles and thumbnails.
M6 quality gates and duplicate detection.
M7 YouTube OAuth and resumable upload.
M8 persistent scheduler and restart recovery.
M9 tests, packaging and deployment docs.

At every milestone: summarize changed files, run tests, fix failures and update README. Ask only for genuinely required configuration. Never ask the user to paste secrets into chat.

## Current milestone
Create a reliable local foundation that runs without API keys, YouTube credentials, Piper, Whisper or FFmpeg. Clearly identify optional integrations that are not configured.