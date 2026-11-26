"""Sound mix v2: voices + Lyria music (per-scene mood) + ambience beds + timed SFX cues + soft whooshes on cuts.
python mix2.py <PART> <out.mp4>      reads <PART>/timeline.json, <PART>/cuts.json, <PART>/cues.py
cues.py defines:
  MOOD = {"a": "tense", ...}          music mood per scene (music/<mood>_<i>.wav), "none" = silence
  AMB  = {"a": ("room", 1.0), ...}    ambience bed per scene (sfx2.AMB) and gain
  CUES = [(scene, when, kind, gain, pan, offset), ...]
        when: seconds in scene | "word" | "word#n" | "word@line#n" ; kind: sfx2.LIB name or callable
  MUSIC_GAIN (optional, default 1.0), CUT_WHOOSH (optional, default 0.12)
"""
import numpy as np, soundfile as sf, json, subprocess, os, sys, glob
from scipy import signal
import sfx2

SR = 48000
PART = os.path.abspath(sys.argv[1]); OUT = sys.argv[2]; HERE = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(f"{PART}/timeline.json")); CUTS = json.load(open(f"{PART}/cuts.json")) if os.path.exists(f"{PART}/cuts.json") else {}
G = {}; exec(open(f"{PART}/cues.py").read(), G)
MOOD, AMB, CUES = G["MOOD"], G.get("AMB", {}), G.get("CUES", [])
MUSIC_GAIN, CUT_WHOOSH = G.get("MUSIC_GAIN", 1.25), G.get("CUT_WHOOSH", 0.12)

starts, pos = {}, 0
for s in TL: starts[s["id"]] = pos / SR; pos += int(round(s["frames"] / 30 * SR))
N = pos; TAIL = int(1.0 * SR)
L = np.zeros(N + TAIL); R = np.zeros(N + TAIL)


def add(x, t, gain=1.0, pan=0.0, stereo=None):
    i = int(round(t * SR))
    if i >= len(L): return
    if stereo is not None:
        a, b = stereo[:, 0], stereo[:, 1]
    else:
        th = (pan + 1) * np.pi / 4; a, b = x * np.cos(th) * 1.414, x * np.sin(th) * 1.414
    n = min(len(a), len(L) - i); L[i:i + n] += a[:n] * gain; R[i:i + n] += b[:n] * gain


# ---------- voices ----------
V = np.zeros(N + TAIL)
for s in TL:
    v, sr = sf.read(f"{PART}/audio/{s['id']}_voice.wav")
    v = signal.resample_poly(v, SR, sr) if sr != SR else v
    i = int(round(starts[s["id"]] * SR)); n = min(len(v), int(round(s["frames"] / 30 * SR)))
    V[i:i + n] += v[:n]
L += V; R += V

# ---------- word timing ----------
SCN = {s["id"]: s for s in TL}


def when(sc, w):
    if isinstance(w, (int, float)): return starts[sc] + w
    word, li, nth = w, None, 0
    if "#" in word: word, nth = word.split("#"); nth = int(nth)
    if "@" in word: word, li = word.split("@"); li = int(li)
    k = 0
    for i, l in enumerate(SCN[sc]["lines"]):
        if li is not None and i != li: continue
        for ww in l["words"]:
            if ww[0].strip(".,!?'\"").lower() == word.lower():
                if k == nth: return starts[sc] + ww[1]
                k += 1
    raise KeyError(f"cue word {sc}:{w}")


# ---------- music ----------
def track(mood, i):
    fs = sorted(glob.glob(f"{HERE}/music/{mood}_*.wav"))
    x, sr = sf.read(fs[i % len(fs)]);
    if x.ndim == 1: x = np.stack([x, x], 1)
    if sr != SR: x = signal.resample_poly(x, SR, sr, axis=0)
    return x / (np.sqrt((x ** 2).mean()) + 1e-9) * 0.1


runs = []  # (mood, t0, t1)
for s in TL:
    m = MOOD.get(s["id"], "none"); t0 = starts[s["id"]]; t1 = t0 + s["frames"] / 30
    if runs and runs[-1][0] == m: runs[-1][2] = t1
    else: runs.append([m, t0, t1])
X = 1.5  # crossfade between runs
Mus = np.zeros((N + TAIL, 2)); used = {}
for m, t0, t1 in runs:
    if m == "none": continue
    need = int((t1 - t0 + 2 * X) * SR); buf = np.zeros((0, 2)); k = used.get(m, 0)
    while len(buf) < need:
        tr = track(m, k); k += 1; xf = int(3.0 * SR)
        if len(buf):
            r = np.linspace(0, 1, xf)[:, None]; buf[-xf:] = buf[-xf:] * (1 - r) + tr[:xf] * r; buf = np.concatenate([buf, tr[xf:]])
        else: buf = tr
    used[m] = k; buf = buf[:need]; e = np.ones(need); f = int(X * SR)
    if t0 > 0: e[:f] = np.linspace(0, 1, f)
    e[-f:] = np.linspace(1, 0, f)
    i = max(0, int((t0 - (X if t0 > 0 else 0)) * SR)); n = min(need, len(Mus) - i); Mus[i:i + n] += (buf * e[:, None])[:n]
spk = np.convolve(np.abs(V), np.ones(4800) / 4800, "same") > 0.01
duck = np.convolve(spk.astype(float), np.ones(14400) / 14400, "same")
mg = MUSIC_GAIN * (0.55 - 0.30 * duck)
L += Mus[:, 0] * mg; R += Mus[:, 1] * mg
STEM_V, STEM_M = V.copy(), Mus.mean(1) * mg

# ---------- ambience ----------
for s in TL:
    a = AMB.get(s["id"])
    if not a: continue
    name, g = a; d = s["frames"] / 30 + 0.6
    x = sfx2.AMB[name](d); x = x / (np.sqrt((x ** 2).mean()) + 1e-9) * 0.012 * g
    e = np.ones(len(x)); f = int(0.3 * SR); e[:f] = np.linspace(0, 1, f); e[-f:] = np.linspace(1, 0, f)
    add(x * e, max(0, starts[s["id"]] - 0.3), 1.0, 0.0)

# ---------- whooshes on cuts ----------
for sc, c in CUTS.items():
    if sc not in starts: continue
    for t in c["cuts"]:
        g = 0.35 if t in c["whips"] else CUT_WHOOSH
        add(sfx2.whoosh(0.4), starts[sc] + t - 0.22, g, float(np.random.default_rng(int(t * 100)).uniform(-0.4, 0.4)))
    if c.get("whips"):
        for t in c["whips"]:
            if t not in c["cuts"]: add(sfx2.whoosh(0.4), starts[sc] + t - 0.22, 0.35)

# ---------- cues ----------
for cue in CUES:
    sc, w, kind = cue[:3]; g = cue[3] if len(cue) > 3 else 1.0; pan = cue[4] if len(cue) > 4 else 0.0; off = cue[5] if len(cue) > 5 else 0.0
    x = kind() if callable(kind) else sfx2.LIB[kind]()
    add(x * 0.35, when(sc, w) + off, g, pan)

mix = np.stack([L, R], 1)[:N]
mix = np.tanh(mix * 1.2) / np.tanh(1.2) * 0.95
sf.write(f"{PART}/audio/mix2.wav", mix.astype(np.float32), SR)
if os.environ.get("STEMS"):
    fx = (L + R) / 2 - STEM_V - STEM_M
    w = SR // 2; rm = lambda a: np.array([np.sqrt((a[i:i + w] ** 2).mean()) for i in range(0, N - w, w)])
    v, m, f = rm(STEM_V[:N]), rm(STEM_M[:N]), rm(fx[:N]); sp = v > 0.02
    db = lambda a: round(20 * np.log10(np.mean(a) + 1e-9), 1)
    print("voice(speech)", db(v[sp]), "music(speech)", db(m[sp]), "music(gaps)", db(m[~sp]), "fx mean", db(f), "fx max", db(np.max(f)), "fx max at", np.argmax(f) / 2)
if os.environ.get("AUDIO_ONLY"): print("audio ok", N / SR); sys.exit()
open(f"{PART}/scenes/list.txt", "w").write("".join(f"file '{s['id']}.mp4'\n" for s in TL))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{PART}/scenes/list.txt", "-c", "copy",
                f"{PART}/scenes/video.mp4"], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{PART}/scenes/video.mp4", "-i", f"{PART}/audio/mix2.wav",
                "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-shortest", "-movflags", "+faststart", f"{PART}/{OUT}"], check=True)
print("ok", N / SR)
