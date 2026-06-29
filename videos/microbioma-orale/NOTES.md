# microbioma-orale — reel 9:16 (montaggio ffmpeg di clip AI)

Reel verticale 1080×1920 sul microbioma del solco gengivale: i patogeni parodontali
(PORPHY / PREVI / TREPI) vs il batterio buono *Streptococcus dentisani*.

**Non è un progetto HyperFrames/TTS standard.** Le clip sono avatar AI generati
esternamente (image-to-video) con voce baked-in, quindi il montaggio è un
post-process **ffmpeg** (no render HyperFrames, no TTS). Vedi `build/build_v1.py`.

## Asset sorgente (`assets/clips/`, NON versionati — `videos/**` è gitignored)

| File | Formato | Audio | Ruolo |
|---|---|---|---|
| `open-porphy-bloodcurrent.mp4` | 9:16 720×1280, 5.0s | — (muto) | Cold open cinematografico |
| `villain-porphy-seg2-closeup.mp4` | 9:16 720×1280, 15s | voce | PORPHY primo piano |
| `villain-porphy-seg1-takeA.mp4` | 9:16 720×1280, 15s | voce | PORPHY seg1 (non usata in v1) |
| `villain-porphy-seg1-takeB.mp4` | 9:16 720×1280, 15s | voce | PORPHY seg1 alt (== takeC, non usata) |
| `villain-previ-angry.mp4` | landscape 1088×704, 14s | voce | PREVI villain |
| `villain-previ-calm-4k.mp4` | landscape 4096×2650, 9.7s | voce | PREVI "calma" (non usata in v1) |
| `hero-strep-dentisani.mp4` | landscape 1088×704, 14.3s | voce | Eroe Strep dentisani |

Mancante: un clip di **TREPI** (*Treponema denticola*) — è nel cast ma non fornito.

## Scelte di montaggio (v1)

- Struttura **villain → eroe**, taglio serrato **~28s**.
- Landscape reincorniciati in 9:16 con **cover-crop fill** (riempie il frame, taglia
  solo i lati; personaggio centrato resta intero). I clip nativi 9:16 solo scalati.
- **Lower-third** coi nomi (accento: PORPHY rosso, PREVI viola, STREP oro).
- Voci normalizzate `loudnorm I=-16` per volumi coerenti; fade 0.15s su tagli.
- Tagli scelti sui **silenzi** (`silencedetect`) dove disponibili; PORPHY closeup è
  parlato continuo → troncato (serve il testo per tagliare sulle frasi).
- **End card** = placeholder (CTA + "BUONI vs CATTIVI").

## TODO v2 (in attesa input utente)

- [ ] **Sottotitoli IT** sincronizzati — serve il testo parlato di ogni clip (qui non c'è STT).
- [ ] **Musica** di sottofondo — serve un file royalty-free (riempie anche il cold open muto).
- [ ] **End card** con CTA + brand reali (+ eventuale cast image come sfondo).
- [ ] Conferma ordine / take; eventuale inserimento clip non usate o di TREPI.

## Changelog

- **v1** (`build_v1.py`) — cut base: cold open, cover-crop reframing, lower-third
  statici, voci loudnorm, end card placeholder.
- **v1.5** (`build_v15.py`) — polish montaggio (nessun input nuovo): lower-third
  **animati** (slide-in da sinistra), apertura in dissolvenza dal nero, titolo in
  fade-in, vignettatura per coesione, end card in fade-in. Stesso cut e durata.

## Rebuild

```bash
python3 videos/microbioma-orale/build/build_v1.py    # cut base   -> out/microbioma-orale-v1.mp4
python3 videos/microbioma-orale/build/build_v15.py   # rifinito   -> out/microbioma-orale-v1_5.mp4
```
