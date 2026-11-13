# Architecture

## Data flow
1. Topic queue stores candidate subjects.
2. Research service records sources and verification status.
3. Script service creates separate Short and long scripts plus storyboards.
4. Audio service generates narration using a configured local or approved provider.
5. Visual service creates original diagrams or imports licensed assets with attribution.
6. Editing service renders through FFmpeg.
7. Quality service validates media, sources, rights and duplicate fingerprints.
8. Upload service uses official YouTube OAuth/API and defaults to private or unlisted.
9. Scheduler persists jobs and recovers queued work after restart.
10. Dashboard exposes status, previews, editing and approvals.

## Resource strategy
- Run one heavy production job at a time.
- Avoid loading multiple models simultaneously.
- Use preview resolution where appropriate.
- Use bounded subprocess timeouts and retain useful logs.
- Never delete source assets before output validation.
- Keep generated media outside Git.

## Security
- Environment and OAuth token files are excluded from Git.
- Dashboard binds to localhost by default.
- Never collect Google passwords.
- Uploads are private/unlisted by default.
- Public publishing requires explicit human approval and policy compliance.

## Milestones
M0: foundation, configuration, SQLite and dashboard.
M1: topic queue, research sources and fact-check review.
M2: script editor and storyboard.
M3: local TTS and audio validation.
M4: original visuals and licensed asset registry.
M5: FFmpeg renderer, subtitles and thumbnails.
M6: media, factual and rights quality gates.
M7: YouTube OAuth and resumable uploads.
M8: persistent scheduler, retry and restart recovery.
M9: packaging, end-to-end tests and deployment.

Each milestone must include tests and updated documentation. Do not describe future work as implemented.