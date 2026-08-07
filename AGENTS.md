# AGENTS.md

General repo guidance lives in `README.md` and `CLAUDE.md` (architecture, workflow DAG,
per-video output layout, gotchas). Standard commands are documented there and in
`.claude/skills/hyperframes-cli/SKILL.md` — don't duplicate them here.

## Cursor Cloud specific instructions

This repo has no long-running server and no root `package.json`/lockfile. The "product" is a
pipeline that turns a topic into a vertical (1080×1920) HyperFrames short. There are two ways to
drive it; only the second one works in this cloud VM:

- **Archon automated path (`archon workflow run create-<template>-short …`) — NOT available here.**
  It requires the Archon CLI + Claude Code authenticated against a **Claude Pro/Max OAuth
  subscription** (`CLAUDE_USE_GLOBAL_AUTH=true`, no `ANTHROPIC_API_KEY`). Those are user
  credentials we can't provision autonomously, so don't rely on this path for testing.
- **Cursor-only fallback path — this is what works here.** Do the playbook steps yourself:
  copy a template (`cp -r templates/shorts/classic videos/<slug>`), write `videos/<slug>/script.txt`
  (blank-line-separated phase blocks — 4 blocks for the shipped templates), generate narration with
  the repo's own Python TTS script, wire the narration `<audio>` element into `index.html`, then use
  the HyperFrames CLI to `lint` / `preview` / `render`. See `.claude/skills/diy-yt-creator/` playbooks.

### Environment specifics (already provisioned in the snapshot; update script keeps it fresh)

- **Python TTS deps live in a repo-local venv at `.venv`** (created by the update script). Always
  invoke the TTS/timing scripts with `.venv/bin/python`, e.g.
  `.venv/bin/python scripts/kokoro-tts.py videos/<slug> --shorts`. Bare `python`/`pip` is the
  system interpreter and does NOT have `kokoro` (Ubuntu 24.04 also blocks bare `pip install` via
  PEP 668). Kokoro is the free/local default and needs no API key.
- **`espeak-ng` is installed system-wide** (apt). Kokoro requires it for phoneme conversion; without
  it `scripts/kokoro-tts.py` errors.
- **Kokoro's first generation downloads models** (~325MB Kokoro-82M + the `en_core_web_sm` spaCy
  model) into `~/.cache/`. This is captured in the snapshot, so later runs are offline. If you ever
  hit a "model not found" error, the download was network-blocked — just retry.
- **The HyperFrames CLI has no local install** — run it on demand with `npx hyperframes …` (or
  `pnpm exec hyperframes …`). Node 22, FFmpeg, and system Chrome are present (`npx hyperframes doctor`).
- **`render` is slow here (screenshot fallback).** System Chrome lacks `chrome-headless-shell`, so
  rendering falls back to per-frame screenshots (~3–4 min for a 24s draft). This is expected, not a
  hang. Optional speedup: `npx @puppeteer/browsers install chrome-headless-shell` (or point
  `HYPERFRAMES_BROWSER_PATH` at one). Prefer `--quality draft` while iterating.
- **`bun` is installed at `~/.bun/bin`** (used only by the Archon `parse-input` node). It is NOT on
  the default PATH — add `export PATH="$HOME/.bun/bin:$PATH"` if you need it. Not required for the
  Cursor-only path.
- **Env file:** `.archon/.env` is created from `.env.example` (git-ignored). TTS scripts read it.
- **Git-ignored outputs:** `.venv/`, `videos/**`, and rendered MP4s (`out/`) are not committed, so a
  scratch video under `videos/<slug>/` won't show up in a diff.

### Dev / test / build / run quick reference

- Lint a composition: `npx hyperframes lint videos/<slug>` (also `templates/shorts/<name>`).
- Run in dev mode (hot-reload studio): `npx hyperframes preview videos/<slug> --port 3002`.
- Render an MP4: `npx hyperframes render videos/<slug> --quality draft -o videos/<slug>/out/<slug>.mp4`.
- Generate narration: `.venv/bin/python scripts/kokoro-tts.py videos/<slug> --shorts`.
