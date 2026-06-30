# Bonebenders Shorts Template

Vertical YouTube Short (1080x1920, 30fps, 60-180s) for **Bonebenders** — the evidence-based dental / regenerative-surgery brand of **Dr. Ernesto Bruschi** (Frosinone, Italy). Dark "Minimal Freddo" clinical stage: slate-near-black canvas, one bright sky-blue accent, **serif (Playfair Display) headlines** over Inter body. Calm and peer-referenced, not a hype reel.

The full design system (colors with provenance, type scale, motion, surface detail, SFX, anti-patterns) lives in [DESIGN.md](./DESIGN.md). Read it before editing. TTS pronunciation decisions (Italian-first, clinical terms) live in [PRONUNCIATION.md](./PRONUNCIATION.md).

## What this template ships

A self-contained 24-second demo composition (`index.html`) showcasing four reusable phase archetypes — same structure as `templates/shorts/anthropic/` and `templates/shorts/archon/`, rebranded for Bonebenders:

| Phase | Pattern | Use for |
|---|---|---|
| 1 — Hero slam | overline + pre-line + 180px serif slam word + caption pill | scroll-stop hook (solid sky, Playfair serif) |
| 2 — Stat pill row | overline + headline + 2 stat pills (outlined-sky / solid-sky) | "30+ anni / 4 aree" trust receipts |
| 3 — Service cards | overline + 3 indexed cards (mono-sky) | service areas, protocols, method steps |
| 4 — CTA / booking | overline + serif topic slam + outcome line + WhatsApp pill | thumbnail-grade close — clinic booking |

Each phase is mutex-visible (only one at a time), separated by a blur + crossfade transition. Entrance animations only — the transition handles the exit (per HyperFrames rule). Phase 4 is built thumbnail-grade per [`.claude/rules/shorts-thumbnail-final-frame.md`](../../../.claude/rules/shorts-thumbnail-final-frame.md).

## Provenance — brand assets come from the design-system handoff

Everything is traceable to the **Bonebenders Design System** export, not eyeballed:

- **Tokens:** `colors_and_type.css` (handoff) — the dark-mode `:root` variables (sky accent, slate neutrals, Inter + Playfair stacks).
- **Accent:** the brand pivoted **emerald → sky**; CSS token *names* stayed `--emerald-*` but the hex map to Tailwind **sky**. This template uses sky (`#38bdf8` bright / `#0284c7` deep).
- **Logo:** `logo-bonebenders-transparent.png` — the white lockup for dark backgrounds (copied into `assets/`). The `-dark.png` ink variant is for light backgrounds — not used here.
- **Fonts:** the four brand woff2 files (Inter + Playfair Display, latin + latin-ext) ship in `assets/fonts/` and are `@font-face`d in `index.html` — self-hosted, offline, brand-exact.
- **Voice / copy:** the handoff's "Content fundamentals" — first-person singular, calm, clinical, sentence case, zero emoji, no exclamation marks. The placeholder copy follows it.

If you re-tune the palette, edit [DESIGN.md](./DESIGN.md) first (it holds the token origin), then propagate hex into `index.html`'s `--sky`, `--sky-600`, etc.

## How this differs from the Anthropic / Archon templates

Same four-phase skeleton, but the brand identity inverts several of their rules — read these before reusing patterns:

- **Serif headlines.** Playfair Display carries every headline, hero, and stat number. (Anthropic/Archon forbid serif — Bonebenders requires it.)
- **Single accent.** Sky carries every phase; NO per-phase hue rotation. (Archon rotates cyan/magenta/purple/blue — Bonebenders does not.) WhatsApp green is the lone exception, booking CTA only.
- **No gradient hero fill, no inline shake.** Calm, publication-grade motion. (Archon's cyan→magenta text-fill drift and slam shake are banned here.)
- **Italian-first narration.** Use an `it-IT` edge-tts voice, not the `en-US` default — see [PRONUNCIATION.md](./PRONUNCIATION.md).

## Spawn a new Bonebenders-themed video from this template

From the repo root:

```bash
# 1. Pick a slug (kebab-case, descriptive)
SLUG="osteointegrazione-30s"

# 2. Copy the template
cp -r templates/shorts/bonebenders videos/$SLUG

# 3. Update meta.json
#    {
#      "id": "osteointegrazione-30s",
#      "name": "Osteointegrazione in 30s"
#    }

# 4. Edit videos/$SLUG/index.html
#    - Replace each phase's text (overlines, pre-line, hero word, stats, cards, CTA)
#    - Adjust #root data-duration + the T1/T2/T3 transition timestamps if your script length differs from 24s
#    - Drop narration at videos/$SLUG/audio/narration.wav and uncomment the <audio> block
#    - The top banner already points at assets/logo-bonebenders-transparent.png — keep it

# 5. Validate
npx hyperframes lint    videos/$SLUG
npx hyperframes validate videos/$SLUG    # adds WCAG contrast audit
npx hyperframes inspect videos/$SLUG     # checks for layout overflow

# 6. Preview
npx hyperframes preview videos/$SLUG

# 7. Render
npx hyperframes render videos/$SLUG -o videos/$SLUG/out/$SLUG.mp4
```

PowerShell equivalent for step 2: `Copy-Item -Recurse templates/shorts/bonebenders videos/$SLUG`.

> This repo uses **PNPM**; the `npx hyperframes ...` form also works — use whichever you prefer.

## Customizing per video

Most styling is driven by CSS variables on `#root`:

```css
#root {
  --bg:      #020617;   /* slate-950 canvas */
  --fg:      #f8fafc;   /* medical white headings */
  --sky:     #38bdf8;   /* the one accent — sky-400 */
  --sky-600: #0284c7;   /* solid fills */
  --wa:      #22c55e;   /* WhatsApp booking pill only */
  --pad-top: 240px;     /* increase if your banner is taller */
  /* ... */
}
```

To vary the two stat pills, keep them both sky and switch treatment: `.stat-pill.outline` (sky digit on faint tint) vs `.stat-pill.solid` (slate-950 digit on a filled sky block). Do **not** introduce a second hue.

## Logo / banner

The banner is a single `<img>` of `assets/logo-bonebenders-transparent.png` — the white "crossed bones + fist + Bonebenders" lockup, ~560px wide, centered in the top safe zone. No CSS wordmark needed (unlike Archon). If you want the round avatar variant instead, the handoff also shipped `logo-bonebenders-round.jpeg` (not copied here — pull it from the design-system export).

## Adding narration

1. Generate Italian TTS — use an `it-IT` edge-tts voice (see PRONUNCIATION.md), e.g.:
   `python scripts/edge-tts-fallback.py videos/$SLUG --voice it-IT-DiegoNeural`
2. Uncomment the `<audio id="narration">` block at the bottom of `index.html`.
3. Tune `data-start` / `data-duration`, then sync phase timestamps to spoken-word landmarks.

## Adding SFX

Default for this template is **`cinematic-whoosh` on transitions only** (calm clinical posture, like the Anthropic family). Sync the cue, then uncomment the whoosh block:

```bash
bash scripts/sync-video-sfx.sh videos/$SLUG cinematic-whoosh
```

Fire each whoosh at the visual phase-swap moment (`T1`/`T2`/`T3`), `data-duration="1.5"`, `data-volume="0.11"`. Per-element slams are opt-in for a single deliberate beat — never the default. Full caps in [`.claude/rules/audio-design.md`](../../../.claude/rules/audio-design.md).

## Adding more phases

1. Duplicate a `<div class="phase">` block; give it a new id (`#phase5`), `z-index: 5; opacity: 0;`.
2. Add per-phase CSS — keep `padding: var(--pad-top) var(--pad-x) var(--pad-bottom)`.
3. Bump `#root` `data-duration` to cover the new total.
4. Add entrance tweens + a transition block following the `P*`/`T*` convention.
5. Re-run `npx hyperframes lint` after every change.

## Don'ts

See `DESIGN.md` "What NOT to Do" for the full list. The big ones:

- No light canvas — dark clinical stage only.
- No second accent hue — sky carries everything; WhatsApp green is booking-CTA only.
- No sans headlines — Playfair Display (serif) on every headline/hero/stat.
- No decorative gradients, no inline shake — publication-grade calm.
- No emoji, no exclamation marks in headings — calm clinical voice.
- No `<br>` in content text — use `max-width`.
- No background music on Shorts.
- Don't use the `-dark.png` logo — use the white transparent lockup.
