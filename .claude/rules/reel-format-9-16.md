# Reel format — 9:16 vertical is the default and the fallback

**Every reel in this repo is 9:16 vertical (1080×1920) unless the user explicitly asks for another aspect.** 9:16 is BOTH the default (new reels start here) AND the fallback (when the requested format is unspecified, ambiguous, or a source clip arrives in another aspect, resolve to 9:16 — never letterbox, never stretch, never silently emit 16:9).

"Reel" here means any short-form vertical deliverable produced in this repo:
- HyperFrames Shorts spawned from `templates/shorts/<style>/` (canvas set via `data-width`/`data-height`).
- ffmpeg montage reels assembled from source clips (e.g. `videos/<slug>/build/*.py`).

## The canonical spec

| Property | Default / fallback value |
|---|---|
| Aspect ratio | **9:16** |
| Resolution | **1080 × 1920** |
| Frame rate | **30 fps** |
| Pixel format | `yuv420p` |
| SAR | `1:1` (`setsar=1`) |
| Audio | AAC, 192k, 48000 Hz, stereo |
| Video codec | H.264 (`libx264`), `-crf 18-19`, `-movflags +faststart` |

These are the values already used across `templates/shorts/*` (1080×1920 canvas) and `videos/microbioma-orale/build/build_v1.py` (`VENC`/`AENC`). This rule makes them the explicit, enforced default instead of an implicit per-file convention.

## HyperFrames Shorts

The composition root carries the canvas:

```html
<div id="root" data-composition-id="main"
     data-start="0" data-duration="..."
     data-width="1080" data-height="1920">
```

- Every `templates/shorts/<style>/index.html` MUST declare `data-width="1080" data-height="1920"`.
- `npx hyperframes render videos/<slug>` derives output dimensions from these attributes — so a correct canvas IS the 9:16 default; there is no separate render flag to set.
- **Fallback:** if a composition is ever authored without `data-width`/`data-height`, treat 1080×1920 as the missing value. Do not let it fall through to a square or 16:9 default.

## ffmpeg montage reels — reframe is the fallback, not letterbox

When assembling a montage from source clips, **the output is always 1080×1920**. Each source is reframed to fill that frame:

- **Source already 9:16** (native vertical): scale exactly to the canvas.
  ```
  scale=1080:1920,setsar=1,fps=30
  ```
- **Source is any other aspect** (16:9 landscape, 4:3, square, off-ratio vertical): **cover-crop fill** — scale up to cover, then center-crop to the canvas. This keeps the subject full-height and immersive; it never adds blurred letterbox bands and never distorts.
  ```
  scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30
  ```

`force_original_aspect_ratio=increase` + `crop` is the **fallback reframe** — apply it to ANY source whose aspect you can't guarantee is 9:16. This is the pattern already proven on the PREVI / STREP landscape scenes in `build_v1.py`. The naked `scale=1080:1920` (which stretches a non-9:16 source) is acceptable ONLY when the source is verified native-vertical.

### Self-check for any montage scene

1. Is the source's native aspect exactly 9:16? → `scale=1080:1920` is safe.
2. Not sure, or it's landscape/square/off-ratio? → use the cover-crop fallback (`force_original_aspect_ratio=increase,crop=1080:1920`).
3. Never emit a scene whose `scale=` distorts the source or whose output is not 1080×1920. Every scene in a reel must end `…,setsar=1` at 1080×1920 so `concat` doesn't mismatch.

## When to override

Only when the user **explicitly** asks for a different aspect for a specific deliverable — "make a 16:9 version", "a square 1:1 cut for the feed". That is a per-request override for that one output; it does NOT change the repo default. The base/master reel stays 9:16. Note any such override in the video's `NOTES.md` so the deviation is visible.

## Why

Shorts/Reels/TikTok are vertical-first surfaces. A reel that ships 16:9 (or letterboxed) loses the full mobile viewport, reads as repurposed long-form, and tanks retention. Making 9:16 the default AND the fallback means an unspecified or mixed-aspect input can never silently produce a non-vertical master — the worst-case is a correctly cover-cropped 9:16, which is always a valid reel.
