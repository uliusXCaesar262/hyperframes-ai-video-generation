#!/usr/bin/env python3
"""Build v1 of the 9:16 oral-microbiome reel (villain -> hero), ffmpeg montage.
Modular: render each scene to build/sN.mp4 (1080x1920, 30fps, stereo 48k), then concat.
v1 = visual proof: reframe + lower-thirds + placeholder end card. No subtitles/music yet."""
import subprocess, os, sys

ROOT = "/home/user/hyperframes-ai-video-generation/videos/microbioma-orale"
CLIPS = f"{ROOT}/assets/clips"
BUILD = f"{ROOT}/build"
OUT   = f"{ROOT}/out"
os.makedirs(BUILD, exist_ok=True); os.makedirs(OUT, exist_ok=True)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"   # bold
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"        # regular

# accents
RED  = "0xE23B4E"   # PORPHY
PURP = "0xB166F0"   # PREVI
GOLD = "0xFFC53D"   # STREP / hero
WHITE= "white"
DIM  = "0xCFCFCF"

VENC = ["-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-r","30"]
AENC = ["-c:a","aac","-b:a","192k","-ar","48000","-ac","2"]

def run(cmd):
    print(">>", " ".join(cmd[:6]), "...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG ERROR:\n", r.stderr[-2500:]); sys.exit(1)

def lower_third(name, species, accent, x=48, y=1486, w=900):
    """drawbox banner + accent bar + name + species. Returns filter string (no leading comma)."""
    h = 150
    return (
        f"drawbox=x={x}:y={y}:w={w}:h={h}:color=black@0.5:t=fill,"
        f"drawbox=x={x}:y={y}:w=12:h={h}:color={accent}:t=fill,"
        f"drawtext=fontfile={FB}:text='{name}':fontcolor=white:fontsize=62:x={x+44}:y={y+22}:shadowcolor=black@0.6:shadowx=2:shadowy=2,"
        f"drawtext=fontfile={FR}:text='{species}':fontcolor={DIM}:fontsize=34:x={x+46}:y={y+96}"
    )

def afades(dur):
    return f"loudnorm=I=-16:TP=-1.5:LRA=11,aformat=sample_fmts=fltp:channel_layouts=stereo,afade=t=in:st=0:d=0.15,afade=t=out:st={dur-0.18:.2f}:d=0.18"

# ---------------- Scene 0: cold open (native vertical, no audio) ----------------
D0 = 2.8
vf0 = (
    "scale=1080:1920,setsar=1,fps=30,eq=brightness=-0.03,"
    f"drawtext=fontfile={FB}:text='IL SOLCO GENGIVALE':fontcolor=white:fontsize=66:x=(w-text_w)/2:y=150:box=1:boxcolor=black@0.45:boxborderw=22,"
    f"drawtext=fontfile={FR}:text='campo di battaglia invisibile':fontcolor={GOLD}:fontsize=40:x=(w-text_w)/2:y=252"
)
run(["ffmpeg","-y","-ss","0.2","-t",str(D0),"-i",f"{CLIPS}/open-porphy-bloodcurrent.mp4",
     "-f","lavfi","-t",str(D0),"-i","anullsrc=channel_layout=stereo:sample_rate=48000",
     "-filter_complex",f"[0:v]{vf0}[v]","-map","[v]","-map","1:a",*VENC,*AENC,"-shortest",f"{BUILD}/s0.mp4"])

# ---------------- Scene 1: PORPHY closeup (native vertical) ----------------
D1 = 8.0
vf1 = "scale=1080:1920,setsar=1,fps=30," + lower_third("PORPHY","Porphyromonas gingivalis",RED)
run(["ffmpeg","-y","-ss","2.9","-t",str(D1),"-i",f"{CLIPS}/villain-porphy-seg2-closeup.mp4",
     "-filter_complex",f"[0:v]{vf1}[v];[0:a]{afades(D1)}[a]","-map","[v]","-map","[a]",*VENC,*AENC,f"{BUILD}/s1.mp4"])

# ---------------- Scene 2: PREVI angry (landscape -> cover-crop fill) ----------------
# Landscape is wider than 9:16, so cover-crop only trims the sides; full height kept,
# centered character preserved. Looks far more immersive than blurred letterbox bands.
D2 = 6.0
vf2 = (
    "[0:v]fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,"
    "eq=brightness=0.02:saturation=1.05,"
    f"{lower_third('PREVI','Prevotella',PURP)}[v]"
)
run(["ffmpeg","-y","-ss","1.03","-t",str(D2),"-i",f"{CLIPS}/villain-previ-angry.mp4",
     "-filter_complex",f"{vf2};[0:a]{afades(D2)}[a]","-map","[v]","-map","[a]",*VENC,*AENC,f"{BUILD}/s2.mp4"])

# ---------------- Scene 3: STREP dentisani hero (landscape -> cover-crop fill) ----------------
D3 = 8.0
vf3 = (
    "[0:v]fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,"
    "eq=brightness=0.03:saturation=1.06,"
    f"{lower_third('STREP. DENTISANI','il batterio buono',GOLD)}[v]"
)
run(["ffmpeg","-y","-ss","0.7","-t",str(D3),"-i",f"{CLIPS}/hero-strep-dentisani.mp4",
     "-filter_complex",f"{vf3};[0:a]{afades(D3)}[a]","-map","[v]","-map","[a]",*VENC,*AENC,f"{BUILD}/s3.mp4"])

# ---------------- Scene 4: end card (static) ----------------
# bg still from cold-open environment
run(["ffmpeg","-y","-ss","4.2","-i",f"{CLIPS}/open-porphy-bloodcurrent.mp4","-frames:v","1","-q:v","3",f"{BUILD}/endbg.jpg"])
D4 = 3.4
vf4 = (
    "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=30,eq=brightness=-0.28:saturation=0.9,setsar=1,fps=30,"
    f"drawtext=fontfile={FB}:text='BUONI vs CATTIVI':fontcolor=white:fontsize=92:x=(w-text_w)/2:y=560:shadowcolor=black@0.7:shadowx=3:shadowy=3,"
    f"drawtext=fontfile={FR}:text='Il microbioma del solco gengivale':fontcolor={DIM}:fontsize=42:x=(w-text_w)/2:y=700,"
    f"drawtext=fontfile={FB}:text='PORPHY   PREVI   TREPI':fontcolor={RED}:fontsize=50:x=(w-text_w)/2:y=920,"
    f"drawtext=fontfile={FR}:text='vs':fontcolor=0x999999:fontsize=40:x=(w-text_w)/2:y=1010,"
    f"drawtext=fontfile={FB}:text='STREPTOCOCCUS DENTISANI':fontcolor={GOLD}:fontsize=52:x=(w-text_w)/2:y=1090,"
    "drawbox=x=280:y=1340:w=520:h=104:color=0xFFC53D:t=fill,"
    f"drawtext=fontfile={FB}:text='LA TUA CTA QUI':fontcolor=0x111111:fontsize=42:x=(w-text_w)/2:y=1372"
)
run(["ffmpeg","-y","-loop","1","-t",str(D4),"-i",f"{BUILD}/endbg.jpg",
     "-f","lavfi","-t",str(D4),"-i","anullsrc=channel_layout=stereo:sample_rate=48000",
     "-filter_complex",f"[0:v]{vf4}[v]","-map","[v]","-map","1:a",*VENC,*AENC,"-shortest",f"{BUILD}/s4.mp4"])

# ---------------- Concat ----------------
scenes = [f"{BUILD}/s{i}.mp4" for i in range(5)]
inputs = []
for s in scenes: inputs += ["-i", s]
n = len(scenes)
pre  = "".join(f"[{i}:v]setsar=1[v{i}];" for i in range(n))   # normalize SAR to avoid concat mismatch
maps = "".join(f"[v{i}][{i}:a]" for i in range(n))
run(["ffmpeg","-y",*inputs,"-filter_complex",f"{pre}{maps}concat=n={n}:v=1:a=1[v][a]",
     "-map","[v]","-map","[a]",*VENC,*AENC,"-movflags","+faststart",f"{OUT}/microbioma-orale-v1.mp4"])

print("\nDONE ->", f"{OUT}/microbioma-orale-v1.mp4")
