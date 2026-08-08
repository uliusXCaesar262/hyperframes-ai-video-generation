"""Generate an original, royalty-free ambient underscore for the reel.

Calm A-minor progression (Am - F - C - G, looped) at 80 BPM: warm detuned
pads + soft arpeggio + sub bass + gentle kick + whisper hats. ~25s, fades.
Output: audio/music.wav (44.1 kHz, stereo, 16-bit PCM).

Run:  .venv/bin/python videos/espansori-alveolo-reel/make_music.py
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import soundfile as sf

SR = 44_100
BPM = 80.0
BEAT = 60.0 / BPM              # 0.75 s
BAR = 4 * BEAT                 # 3.0 s
DURATION = 25.0                # a hair over the 24s timeline
N = int(SR * DURATION)
t = np.arange(N) / SR

# ── Note frequencies ────────────────────────────────────────────────────────
def hz(name: str) -> float:
    names = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5,
             "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
    pitch, octave = name[:-1], int(name[-1])
    midi = 12 * (octave + 1) + names[pitch]
    return 440.0 * 2 ** ((midi - 69) / 12)

# Am - F - C - G, one chord per bar, looped across 8 bars (24s)
PROG = [
    ["A3", "C4", "E4"],   # Am
    ["F3", "A3", "C4"],   # F
    ["C4", "E4", "G4"],   # C
    ["G3", "B3", "D4"],   # G
] * 2
ROOTS = ["A2", "F2", "C3", "G2"] * 2

master = np.zeros(N, dtype=np.float64)


def env_adsr(length, a, d, s_level, r):
    """Simple ADSR amplitude envelope of `length` samples."""
    e = np.zeros(length)
    a_n, d_n, r_n = int(a * SR), int(d * SR), int(r * SR)
    a_n = min(a_n, length)
    e[:a_n] = np.linspace(0, 1, a_n, endpoint=False) if a_n else e[:a_n]
    d_n = min(d_n, length - a_n)
    if d_n:
        e[a_n:a_n + d_n] = np.linspace(1, s_level, d_n, endpoint=False)
    sus_end = length - r_n
    e[a_n + d_n:sus_end] = s_level
    if r_n:
        e[sus_end:] = np.linspace(s_level, 0, length - sus_end)
    return e


# ── Warm detuned pads (raised-cosine bar windows, overlapping) ───────────────
for bar_idx, chord in enumerate(PROG):
    start = int(bar_idx * BAR * SR)
    win_len = int((BAR + 0.6) * SR)          # overlap 0.3s into neighbours
    seg_start = max(0, start - int(0.3 * SR))
    seg_end = min(N, seg_start + win_len)
    L = seg_end - seg_start
    if L <= 0:
        continue
    window = np.hanning(L)
    local_t = np.arange(L) / SR
    for note in chord:
        f = hz(note)
        for detune in (-0.15, 0.15):
            osc = (0.6 * np.sin(2 * np.pi * (f + detune) * local_t)
                   + 0.25 * np.sin(2 * np.pi * 2 * (f + detune) * local_t)
                   + 0.10 * np.sin(2 * np.pi * 3 * (f + detune) * local_t))
            master[seg_start:seg_end] += 0.055 * window * osc

# ── Sub bass — root per bar ──────────────────────────────────────────────────
for bar_idx, root in enumerate(ROOTS):
    start = int(bar_idx * BAR * SR)
    L = min(int(BAR * SR), N - start)
    if L <= 0:
        continue
    f = hz(root)
    local_t = np.arange(L) / SR
    e = env_adsr(L, 0.08, 0.2, 0.8, 0.25)
    master[start:start + L] += 0.22 * e * np.sin(2 * np.pi * f * local_t)

# ── Soft arpeggio — eighth notes, one octave up, plucky ──────────────────────
eighth = BEAT / 2
n_eighths = int(DURATION / eighth)
for i in range(n_eighths):
    start = int(i * eighth * SR)
    bar_idx = int((i * eighth) // BAR)
    if bar_idx >= len(PROG):
        break
    chord = PROG[bar_idx]
    note = chord[i % len(chord)]
    f = hz(note) * 2
    L = min(int(0.42 * SR), N - start)
    if L <= 0:
        continue
    local_t = np.arange(L) / SR
    e = env_adsr(L, 0.005, 0.3, 0.0, 0.1)
    tone = np.sin(2 * np.pi * f * local_t) + 0.3 * np.sin(2 * np.pi * 2 * f * local_t)
    master[start:start + L] += 0.10 * e * tone

# ── Gentle kick on beats 1 & 3 ───────────────────────────────────────────────
n_beats = int(DURATION / BEAT)
for i in range(n_beats):
    if i % 2 != 0:
        continue
    start = int(i * BEAT * SR)
    L = min(int(0.16 * SR), N - start)
    if L <= 0:
        continue
    local_t = np.arange(L) / SR
    pitch = 90 * np.exp(-local_t * 30) + 42
    e = np.exp(-local_t * 22)
    master[start:start + L] += 0.55 * e * np.sin(2 * np.pi * pitch * local_t)

# ── Whisper hats on offbeats ─────────────────────────────────────────────────
rng = np.random.default_rng(7)
for i in range(n_eighths):
    if i % 2 == 0:
        continue
    start = int(i * eighth * SR)
    L = min(int(0.05 * SR), N - start)
    if L <= 0:
        continue
    e = np.exp(-np.arange(L) / SR * 120)
    master[start:start + L] += 0.03 * e * rng.uniform(-1, 1, L)

# ── Master: fades + normalize ────────────────────────────────────────────────
fade_in = int(1.0 * SR)
fade_out = int(2.5 * SR)
master[:fade_in] *= np.linspace(0, 1, fade_in)
master[-fade_out:] *= np.linspace(1, 0, fade_out)

peak = np.max(np.abs(master)) or 1.0
master = master / peak * 0.82
master = np.tanh(master * 1.1)               # gentle glue/soft-clip

stereo = np.stack([master, np.roll(master, int(0.008 * SR))], axis=1)  # tiny width
stereo = stereo / (np.max(np.abs(stereo)) or 1.0) * 0.9

out = Path(__file__).resolve().parent / "audio" / "music.wav"
out.parent.mkdir(parents=True, exist_ok=True)
sf.write(str(out), stereo.astype(np.float32), SR, subtype="PCM_16")
print(f"wrote {out}  ({DURATION:.1f}s, {SR} Hz, stereo)")
