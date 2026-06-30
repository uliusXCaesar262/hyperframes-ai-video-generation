# TTS Pronunciation Map — Bonebenders Shorts Template

Per-template overrides the Phase 2a script writer MUST apply before writing `videos/<slug>/script.txt`. Bonebenders content is **Italian-primary** (the brand publishes IT first, EN as a mirror), and it is **clinical** — dense with anatomical, protocol, and brand terms that a TTS engine reads from spelling alone. These decisions reflect how the terms are actually said in Italian clinical speech.

Authority order, narrowest wins:
1. This file (Bonebenders-specific)
2. `.claude/rules/tts-pronunciation.md` → "Acronym vs Word — disambiguation"
3. `.claude/rules/tts-pronunciation.md` → "Tech & brand pronunciation pitfalls"

> **Language note.** If the narration is Italian, generate with an Italian edge-tts voice (e.g. `it-IT-DiegoNeural`, `it-IT-GiuseppeNeural`) — NOT the English `en-US-AndrewNeural` default. An English voice butchers Italian clinical vocabulary. Set the voice in the TTS step explicitly for Bonebenders videos. If the narration is English (the `/en/` mirror), the English default applies and the brand-name rows below still hold.

## Decisions for Bonebenders' surface tokens

| Token | Spoken as | TTS spelling in `script.txt` | Reason |
| ----- | --------- | ----------------------------- | ------ |
| `Bonebenders` | "bon-bénders" (EN brand name, kept as-is in IT) | `Bonebenders` | Proper brand noun. In an Italian script an IT voice may over-italianize it; if it mangles, spell `Bon benders`. Probe-test once. |
| `Studio Denti Più` | "stúdio dénti più" | `Studio Denti Più` | Italian — reads correctly on an IT voice. On an EN voice spell `Studio Denti Pyoo`. |
| `GBR` | "G B R" (initials) | `G B R` | Guided Bone Regeneration — true initialism, spell out. |
| `ERE` | "E R E" (initials) | `E R E` | Edentulous Ridge Expansion — initialism. |
| `ISQ` | "I S Q" | `I S Q` | Implant Stability Quotient — initialism. |
| `PRF` / `PRGF` | "P R F" / "P R G F" | `P R F` / `P R G F` | Platelet-rich fibrin protocols — initialisms. |
| `2017` (classificazione) | "duemiladiciassette" (IT) | `2017` | An IT voice says the year natively; an EN voice says "twenty-seventeen" — fine. No transform. |
| `osteointegrazione` | "ò-ste-o-integratsióne" | `osteointegrazione` | Long IT compound; IT voice handles it. On EN voice, rephrase to "osseointegration". |
| `parodontologia` | "pa-ro-don-to-lo-gía" | `parodontologia` | IT voice native. EN voice: use "periodontology". |
| `mm` (millimetri) | "millimetri" (IT) | `millimetri` | Never leave the unit abbreviation `mm` — an IT voice may say "emme emme". Write the full word. |
| `Dr.` / `Dott.` | "dottór" (IT) | `Dottor` | Spell out the title; `Dr.`/`Dott.` may be read as letters. |
| `WhatsApp` | "wòtsapp" | `WhatsApp` | Reads correctly on both IT and EN voices. |
| `AI` | "ay-eye" (EN) / "a-i" (IT) | `AI` | Rare in this brand's content; if present, keep native. |

## Heteronyms to watch (Italian)

Italian has far fewer TTS heteronyms than English, but a few clinical words flip stress:

| Word | Senses | Fix |
| ---- | ------ | --- |
| `àncora` / `ancóra` | "anchor" (noun) vs "again/still" | Italian voices usually get this from context; if the implant-anchoring sense reads wrong, rephrase to "il sistema di ancoraggio". |
| `àmbito` | "field/area" | Reads fine; listed for awareness. |
| `pèrfora` / `perfòra` | verb stress | Prefer "esegue la perforazione" if the bare verb reads wrong. |

For **English-mirror** scripts, the full English heteronym table in `.claude/rules/tts-pronunciation.md` applies (`live`, `lead`, `read`, etc.) — audit against it.

## Required leading comment in every Bonebenders-template script

Phase 2a MUST prepend this HTML comment to `videos/<slug>/script.txt`. It's stripped before TTS reaches the engine — it exists so any human editing the script sees the decisions and the voice choice:

```html
<!-- TTS pronunciation overrides — see templates/shorts/bonebenders/PRONUNCIATION.md
     - VOICE: Italian narration → use an it-IT edge-tts voice (e.g. it-IT-DiegoNeural),
       NOT the en-US default. English mirror → en-US default is fine.
     - Bonebenders: brand noun, keep as-is (probe once on the chosen voice)
     - GBR / ERE / ISQ / PRF: spell out as initialisms (G B R, E R E, …)
     - mm: write "millimetri" — never the abbreviation
     - Dott./Dr.: write "Dottor"
-->
```

## Adding a new Bonebenders token to this map

When a regen cycle reveals a new mispronunciation specific to the brand's clinical surface:

1. Add the row with the spoken form + script-spelling + reason.
2. Note the voice it failed on (IT vs EN) — some fixes are voice-specific.
3. Update the leading-comment block so Phase 2a writes the new entry into future scripts.
4. Commit this file in the same PR as the regenerated `videos/<slug>/script.txt`.
