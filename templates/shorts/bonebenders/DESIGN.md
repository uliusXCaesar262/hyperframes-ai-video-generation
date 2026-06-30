# DESIGN — Bonebenders Shorts (Dark Clinical Stage)

Visual system for **YouTube Shorts** (1080x1920, 30fps, 60-180s) for **Bonebenders** — the evidence-based dental / regenerative-surgery brand of **Dr. Ernesto Bruschi**, parodontologist and implantologist in Frosinone, Italy. Cool slate-near-black canvas with one bright sky-blue accent, serif (Playfair Display) headlines over Inter body. Designed to read like a calm, peer-referenced clinical voice — *not* a hype reel. The single warm/loud element is the distressed Bonebenders logo; everything that frames it is cold and orderly.

The brand's own stylesheet calls the mood **"Minimal Freddo"** — cool grays, one accent, medical whites. This template honors that: restraint is the identity.

## Provenance

Colors and typography are derived from the **Bonebenders Design System handoff** (`claude.ai/design` export) — not eyeballed:

- **Tokens:** `colors_and_type.css` from the handoff — the canonical `:root` CSS variables (sky-scale accent, slate neutrals, Inter + Playfair font stacks). The dark-mode block (`.dark { … }`) supplies this template's canvas, surfaces, and accent.
- **Accent note (important):** the brand pivoted its accent **emerald → sky**. The CSS keeps `--emerald-*` token *names* for back-compat, but the hex values map to Tailwind **`sky`**. Hex is authoritative; the prose "emerald" in older brand docs is stale. **Use sky blue.**
- **Logo:** `logo-bonebenders-transparent.png` — white "crossed bones + clenched fist + Bonebenders" lockup on transparent, the variant intended for dark backgrounds. (The `-dark.png` variant is dark navy ink for *light* backgrounds — do NOT use it here.)
- **Voice / copy register:** the handoff README's "Content fundamentals" — first-person singular, calm, clinical, sentence case, never salesy, **zero emoji**, no exclamation marks in marketing headings. The placeholder copy in `index.html` follows it.

## Style Prompt

A cool, near-black clinical stage tuned for vertical video about dental and regenerative surgery. Slate-950 canvas (`#020617`) holds medical-white type and a single bright sky-blue accent. Headlines are **serif** — Playfair Display, the brand's signature — set against Inter for body, overlines, and data. Layout is phase-based: one phase visible per frame, a 240px top safe-zone reserved for the white Bonebenders lockup, generous vertical breathing room. Motion is calm and grounded — soft y-rises, gentle scale-ins, no percussive shake. Reads like a surgeon explaining a protocol: precise, unhurried, trustworthy. One loud element (the accent, or the logo); everything else quiet.

## Canvas

- Resolution: **1080 x 1920** (vertical Shorts)
- Frame rate: **30fps**
- Duration target: **60-180s** (YT Shorts hard max 180s)
- Background: solid `#020617` (slate-950). No full-screen linear gradients (banding under H.264) — use radial highlights or solid + localized glow only. The brand also forbids decorative gradients generally (see What NOT to Do).

## Colors

Hex values are the Bonebenders dark-mode tokens (Tailwind sky + slate). The token role is in the comment for traceability — if you re-tune, edit `colors_and_type.css`-equivalents first.

| Role | Hex | Token origin | Usage |
|---|---|---|---|
| Background | `#020617` | `slate-950` (`--bg` dark) | Page canvas |
| Surface | `#0f172a` | `slate-900` (`--bg-elevated` dark) | Cards, panels |
| Surface elevated | `#1e293b` | `slate-800` (`--bg-subtle` dark) | Inset / hover surfaces |
| Primary text | `#f8fafc` | `slate-50` (`--fg` dark) | Headlines — medical white |
| Body text | `#cbd5e1` | `slate-300` | Body copy on dark |
| Dim / meta text | `#94a3b8` | `slate-400` (`--fg-muted` dark) | Captions, sub-labels |
| Accent — sky (bright) | `#38bdf8` | `sky-400` (`--accent` dark) | Hero, overlines, accent — the one loud hue |
| Accent — sky mid | `#0ea5e9` | `sky-500` | Secondary accent, gradient bridge in fills |
| Accent — sky deep | `#0284c7` | `sky-600` (`--accent-bg`) | Solid fills only (keep on ≥24px) |
| Functional — WhatsApp | `#22c55e` | `green-500` (booking) | **Booking CTA only** — the clinic books via WhatsApp |
| Pill background | `rgba(248,250,252,0.05)` | derived | Default chip / pill fill |
| Pill border | `rgba(248,250,252,0.14)` | derived | Default chip / pill stroke |
| Hairline | `rgba(248,250,252,0.10)` | derived | Card frame on dark |

**Contrast verified (WCAG, on `#020617`):**
- Primary text (`#f8fafc`): ~18:1 (AAA)
- Body text (`#cbd5e1`): ~12:1 (AAA)
- Dim text (`#94a3b8`): ~6:1 (AA normal)
- Sky-400 (`#38bdf8`): ~9:1 (AAA) — safe down to body sizes
- Sky-600 (`#0284c7`): ~4.6:1 (AA normal at 24px+) — keep on fills / large only
- WhatsApp green (`#22c55e`) as a solid pill with near-black text (`#02140a`): pill passes as large UI; never use green as small text on the dark canvas

**Mono-accent rule (brand-specific — differs from Anthropic/Archon).** Bonebenders is a **single-accent** brand: sky carries every phase. Do **NOT** rotate hues per phase (no purple/magenta/orange). Variety comes from *treatment* — outlined-sky vs solid-sky, bright vs deep, glow vs flat — not from a second color. The **only** non-sky accent permitted is WhatsApp green, reserved exclusively for the booking CTA in the final phase.

## Typography

The brand pairing — and the single biggest differentiator from the Anthropic/Archon shorts templates: **Playfair Display** (serif display) carries **all headlines, hero slams, and stat numbers**. **Inter** carries overlines, body, captions, labels, and the CTA. Serif headlines ARE the Bonebenders identity — never substitute a sans headline.

| Role | Family | Weight | Treatment |
|---|---|---|---|
| Hero slam | `'Playfair Display', serif` | 700 | `letter-spacing: -0.02em`, solid sky, soft glow `text-shadow` |
| Headline | `'Playfair Display', serif` | 700 | `letter-spacing: -0.01em`, line-height 1.05-1.08, white |
| Stat number | `'Playfair Display', serif` | 700 | `tabular-nums`, sky or inverted slate-950 on solid-sky pill |
| Pre-line | `'Playfair Display', serif` | 700 | white, sits above the hero slam |
| Body large | `'Inter', sans-serif` | 600 | line-height 1.25, body or dim |
| Body | `'Inter', sans-serif` | 500 | line-height 1.25 |
| Section overline | `'Inter', sans-serif` | 700 | UPPERCASE, `letter-spacing: 5px`, sky or dim |
| Caption / label | `'Inter', sans-serif` | 600 | sentence case |
| CTA pill | `'Inter', sans-serif` | 700 | on WhatsApp green, near-black text |

**Type scale (Shorts-tuned, per `.claude/rules/shorts-typography.md`):**

| Role | Size |
|---|---|
| Hero slam (e.g. "RIGENERA") | 160-180px (drop to 140px for 9-11 char words) |
| CTA topic slam (final frame) | 140-150px |
| Pre-line | 70px |
| Headline | 60-64px |
| Stat number | 150-160px |
| Body large / outcome line | 44-48px |
| Section overline (Inter) | 36px |
| Service card title | 44-48px |
| Service card sub | 30px |
| Caption pill | 34px |

**Tabular numerals on stats:** add `font-variant-numeric: tabular-nums lining-nums` so digits don't jitter.

**Self-hosted fonts.** The four brand woff2 files ship in `assets/fonts/` and are `@font-face`d in `index.html` with the brand's unicode-ranges. This keeps the render brand-exact and offline. Do not swap to a Google-fetched Inter/Playfair — use the bundled woff2.

## Layout

**Safe zones — non-negotiable.** The white Bonebenders lockup sits at `top: 72px`, ~560px wide. Every phase reserves top space for it.

```
PHASE_PAD_TOP    = 240px   (clears the top banner)
PHASE_PAD_X      = 72px    (default side padding — brand is narrow/readable)
PHASE_PAD_BOTTOM = 220px   (clears the progress bar + reading room)
```

`.phase-content` MUST use `width: 100%; height: 100%; padding: 240px 72px 220px; display: flex; flex-direction: column; box-sizing: border-box`. Padding positions content inward — NEVER `position: absolute; top: Npx`.

**Phase mutex:** Only one phase visible per frame. Opacity + visibility crossfades on whole phases. Each phase runs 4-8s.

## Motion Language

The brand is **publication-grade calm** — restraint over flash. Differs from Archon's percussive language.

- **Easing:**
  - `power3.out` for hero slams, headlines, primary rises (the workhorse)
  - `power2.out` for body / caption / overline entrances
  - `back.out(1.4)` for stat pills and the CTA pill — a *gentle* spring, NOT Archon's 1.7
  - `sine.inOut` for ambient breathing only
  - **Avoid** `elastic`, `bounce`, and inline screen-shake — they read toy-like for a clinical brand.
- **Duration:**
  - Hero / topic slam: 0.7-0.85s
  - Headline: 0.5-0.7s
  - Body / caption / card: 0.5-0.55s
  - Phase crossfade: 0.4s opacity + 0.5s blur
- **Direction:** Vertical y-rises dominate (`y: +30/40 → 0`). Hero uses a soft `scale: 0.92 → 1.0`. Horizontal slides only for card rows (`x: -36 → 0`). No rotation. No scale-pop above 1.04.
- **Stagger:** ~0.9s between stat pills; ~0.9s between service cards (each card gets its own narration beat per `step-by-step-reveal.md`); 0.3-0.5s between a phase's overline → headline.
- **No inline shake.** The clinical brand never shakes a word. If a beat truly needs punctuation, a single subtle `scale: 1 → 1.03 → 1` pulse is the ceiling.
- **No gradient text-fill drift.** The brand forbids decorative gradients — the hero is solid sky, not a swept gradient (this is the Archon flourish, banned here).

## Surface Detail

- **Stat pills:** 28px radius. Two treatments within the mono palette — **outlined-sky** (`linear-gradient(160deg, rgba(56,189,248,0.12), rgba(56,189,248,0.03))`, `border: 2px solid rgba(56,189,248,0.40)`, sky digit + glow) and **solid-sky** (`linear-gradient(160deg, var(--sky), var(--sky-600))`, slate-950 digit — the one loud block). Pair them for variety without a second hue.
- **Service cards:** 22px radius, `background: linear-gradient(160deg, rgba(15,23,42,0.92), rgba(2,6,23,0.92))`, `border: 1.5px solid rgba(248,250,252,0.10)`. A sky index chip (84px, `rgba(56,189,248,0.14)` fill, sky border) anchors the left edge.
- **Caption / chip pill:** Inter 600, `background: rgba(248,250,252,0.05)`, `border: 1.5px solid rgba(248,250,252,0.14)`, fully rounded.
- **WhatsApp CTA pill (final frame only):** solid `#22c55e`, near-black text `#02140a`, fully rounded, soft green shadow. The ONLY green element in the template.
- **Ambient:** a single sky radial drift (`rgba(56,189,248,0.10)` top-left + a fainter `rgba(14,165,233,0.06)` bottom-right), ~9% alpha, sine yoyo over ~12s. Mono-hue — echoes the accent, never a rainbow.
- **Film grain:** SVG `feTurbulence` at 3% opacity, `mix-blend-mode: overlay` — breaks H.264 banding on the near-black canvas.

## Audio / SFX Cues

Canonical rules: [`.claude/rules/audio-design.md`](../../../.claude/rules/audio-design.md). Cue files live in [`shared/audio/sfx/`](../../../shared/audio/) (sync via [`scripts/sync-video-sfx.sh`](../../../scripts/sync-video-sfx.sh)).

**Default cue set: `cinematic-whoosh` on phase transitions ONLY** — same posture as the Anthropic family. The clinical brand reads calm; per-element impact-slams / scale-slams / pops cheapen it and compete with narration. They are opt-in for a single deliberate beat (e.g. one stat reveal), never the default.

- Whoosh fires at the exact visual phase-swap moment (`T1`/`T2`/`T3`), `data-duration="1.5"` (full decay tail), `data-volume="0.11"`.
- **No background music on Shorts** (repo audio rule). Narration + whoosh only.
- Optional `sonic-logo` at composition start (`data-volume="0.45"`) if the video wants a brand stinger in the cold open.

Hard cap: **never** exceed `0.25` on a per-cue SFX. See the audio-design rule for the full table.

## What NOT to Do

1. **No light canvas.** This is the dark clinical stage. The brand has a light mode, but Shorts use the dark token set for scroll-stopping contrast. (If a specific video must be light, that's a deliberate override — flag it in the video's notes.)
2. **No second accent hue.** Sky carries every phase. No purple, magenta, orange, red. The brand explicitly forbids them. WhatsApp green is the sole exception, booking CTA only.
3. **No sans headlines.** Playfair Display (serif) carries every headline, hero, and stat number — this is the brand signature. Inter is body/UI only.
4. **No decorative gradients.** The hero is solid sky, not a swept gradient text-fill. Gradients are permitted only as the subtle pill/card surface tints already in the CSS.
5. **No percussive shake / strobe.** Publication-grade calm. No inline screen-shake on slams, no glitch flashes. A single subtle scale pulse is the loudest a beat may get.
6. **No emoji. No exclamation marks in headings.** Brand voice rule — zero emoji anywhere, calm declaratives. ("Scrivimi." not "Scrivimi!")
7. **No salesy copy.** First-person singular, calm, clinical. No "rivoluzionario", "il migliore", "scopri", star-rating badges. Trust signals are stated (30+ anni, peer-reviewed), not shouted.
8. **No `<br>` in content text.** Use `max-width` for natural wrapping.
9. **No background music on Shorts.** Narration + whoosh only.
10. **No `position: absolute; top: Npx` on `.phase-content`.** Use padding to position; absolute overflows on dynamic text.
11. **Don't use the `-dark.png` logo.** That's dark ink for light backgrounds. On the dark stage use `logo-bonebenders-transparent.png` (white).
12. **Final frame must stay thumbnail-grade.** Per [`.claude/rules/shorts-thumbnail-final-frame.md`](../../../.claude/rules/shorts-thumbnail-final-frame.md) — topic slam + outcome + booking CTA + brand chrome, held ≥1.5s static. Never end on a fade-to-black.
