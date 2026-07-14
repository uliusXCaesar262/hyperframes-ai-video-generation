# Arco Sovramascellare — BoneBenders Short

Vertical 9:16 reel (15.0s) built from
[Ode al pilastro nascosto del mascellare superiore](https://bonebenders.com/blog/ode-al-pilastro-nascosto-del-mascellare-superiore/).

## Contents

| File | Role |
|---|---|
| `script.txt` | Italian narration (4 phases) |
| `audio/narration.wav` | edge-tts `it-IT-DiegoNeural` @ +40% |
| `transcript.json` | Word timings (char-proportion fallback) |
| `index.html` | HyperFrames composition |

## Preview / render

```bash
npx hyperframes preview videos/arco-sovramascellare
npx hyperframes render videos/arco-sovramascellare -o videos/arco-sovramascellare/out/arco-sovramascellare.mp4
```

## Source facts used

- PNR ≈ 14 mm from crest at premolar (Chan et al., cited in article)
- Palatal bone at canine ≈ 5 mm at 9 mm from crest (Todorovic et al.)
- Three arc segments: PNR, canine pillar base (BCB), anterior nasal spine (ANS)
