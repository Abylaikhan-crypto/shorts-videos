"""Part 1 — voice every line with Kokoro, estimate word timings, build per-scene audio + timeline.json"""
import numpy as np, soundfile as sf, json, re, os
from kokoro_onnx import Kokoro

SR = 24000
FPS = 30
OUT = os.path.dirname(os.path.abspath(__file__))
k = Kokoro("/home/claude/tts/kokoro-v1.0.onnx", "/home/claude/tts/voices-v1.0.bin")

# speaker -> (voice, speed, pitch factor)
VOICES = {
    "N": ("af_heart", 1.02, 1.0),     # Maya, narrator (voice-over)
    "D": ("am_michael", 0.98, 0.93),  # Dale, stepdad (pitched down)
    "A": ("af_sarah", 0.97, 1.0),     # Ms. Alvarez, counselor
}

import sys
_ep = sys.argv[1]
OUT = os.path.dirname(os.path.abspath(_ep))
_ns = {}
exec(open(_ep).read(), _ns)
SCENES = _ns["SCENES"]
VOICES.update(_ns.get("VOICES", {}))
SENT_PAUSE = _ns.get("SENT_PAUSE", 0)      # extra silence after . ? ! inside a line
COMMA_PAUSE = _ns.get("COMMA_PAUSE", 0)    # extra silence after , inside a line
os.makedirs(f"{OUT}/audio", exist_ok=True)


import hashlib


def _gem(spk, text):
    import gtts
    voice, style = VOICES[spk][0].split(":", 1)[1], VOICES[spk][3] if len(VOICES[spk]) > 3 else ""
    os.makedirs("/home/claude/short/tts_cache", exist_ok=True)
    h = hashlib.md5(f"{voice}|{style}|{text}".encode()).hexdigest()
    p = f"/home/claude/short/tts_cache/{h}.npy"
    if os.path.exists(p): return np.load(p)
    a = gtts.speak(text, voice, style); np.save(p, a); return a


def radio(a):
    """bandpass-ish PA/radio colour"""
    from numpy.fft import rfft, irfft, rfftfreq
    f = rfftfreq(len(a), 1 / SR); A = rfft(a)
    A *= ((f > 300) & (f < 3400)).astype(np.float32) * 1.6
    b = irfft(A, len(a)).astype(np.float32)
    b = np.tanh(b * 2.2) / 2.2
    return b


RADIO = set(_ns.get("RADIO", []))


def synth(spk, text, sp=None):
    if str(VOICES[spk][0]).startswith("gemini:"):
        a = _gem(spk, text).astype(np.float32)
        if spk in RADIO: a = radio(a)
        return a / (np.abs(a).max() + 1e-9) * 0.85
    voice, speed, pitch = VOICES[spk][:3]
    if sp: speed = sp
    a, sr = k.create(text, voice=voice, speed=speed, lang="en-us")
    a = np.asarray(a, dtype=np.float32)
    if pitch != 1.0:  # resample: lowers pitch and slows slightly (menacing)
        n = int(len(a) / pitch)
        a = np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a).astype(np.float32)
    a = a / (np.abs(a).max() + 1e-9) * 0.85
    return a


def speech_mask(a, thr=0.02, win=240):
    env = np.convolve(np.abs(a), np.ones(win) / win, mode="same")
    return env > thr, env


def trim(a):
    m, _ = speech_mask(a)
    idx = np.where(m)[0]
    s, e = max(idx[0] - 600, 0), min(idx[-1] + 1200, len(a))
    return a[s:e]


def word_times(a, text):
    """Estimate word boundaries: split speech at silent gaps that match punctuation, then by letter count."""
    words = text.split()
    m, env = speech_mask(a)
    idx = np.where(m)[0]
    s0, s1 = idx[0] / SR, idx[-1] / SR
    # silent gaps > 110 ms inside speech
    gaps = []
    run = None
    for i in range(idx[0], idx[-1]):
        if not m[i]:
            if run is None: run = i
        else:
            if run is not None and (i - run) > 0.06 * SR:
                gaps.append((run / SR, i / SR))
            run = None
    breaks = [i for i, w in enumerate(words[:-1]) if re.search(r"[.,?!…]|\.\.\.$", w)]

    def weight(w):
        return len(re.sub(r"[^A-Za-z0-9']", "", w)) + 1.6

    def distribute(ws, t0, t1):
        tot = sum(weight(w) for w in ws)
        out, t = [], t0
        for w in ws:
            d = (t1 - t0) * weight(w) / tot
            out.append([t, t + d]); t += d
        return out

    # 1) proportional estimate, punctuation adds virtual pause weight
    tot = 0; items = []
    for w in words:
        p = 6 if w.endswith("...") else 4.5 if w[-1] in ".?!" else 2.5 if w[-1] == "," else 0
        items.append((weight(w), p)); tot += weight(w) + p
    tot -= items[-1][1]
    est, t = [], s0
    for (wt, p) in items:
        d = (s1 - s0) * wt / tot
        est.append([t, t + d]); t += d + (s1 - s0) * p / tot
    if not breaks:
        times = est
    else:
        # 2) snap each expected punctuation pause to the nearest real silent gap (within 0.7 s)
        # order-preserving DP match of punctuation breaks to silent gaps
        B, G = len(breaks), len(gaps)
        exp_t = [(est[b][1] + est[b + 1][0]) / 2 for b in breaks]
        SKIP = 0.8
        INF = 1e9
        dp = [[INF] * (G + 1) for _ in range(B + 1)]; bk = [[None] * (G + 1) for _ in range(B + 1)]
        for j in range(G + 1): dp[0][j] = 0
        for i in range(1, B + 1):
            for j in range(G + 1):
                if dp[i - 1][j] + SKIP < dp[i][j]: dp[i][j] = dp[i - 1][j] + SKIP; bk[i][j] = ("skip", j)
                if j > 0:
                    if dp[i][j - 1] < dp[i][j]: dp[i][j] = dp[i][j - 1]; bk[i][j] = ("gapskip", j - 1)
                    c = dp[i - 1][j - 1] + abs((gaps[j - 1][0] + gaps[j - 1][1]) / 2 - exp_t[i - 1]) \
                        - 0.6 * (gaps[j - 1][1] - gaps[j - 1][0])  # longer pauses are likelier sentence ends
                    if c < dp[i][j]: dp[i][j] = c; bk[i][j] = ("match", j - 1)
        i, j, match = B, G, {}
        while i > 0:
            kind, jj = bk[i][j]
            if kind == "match": match[i - 1] = jj; i -= 1; j = jj
            elif kind == "skip": i -= 1; j = jj
            else: j = jj
        cuts = []
        for bi, b in enumerate(breaks):
            if bi in match: g0, g1 = gaps[match[bi]]
            else: g0, g1 = est[b][1], est[b + 1][0]
            cuts.append((b, g0, g1))
        times, start, prev = [], s0, 0
        for b, g0, g1 in cuts:
            if g0 <= start: g0 = start + 0.05; g1 = max(g1, g0)
            times += distribute(words[prev:b + 1], start, g0); prev, start = b + 1, g1
        times += distribute(words[prev:], start, s1)
        # sanity: per-word durations must be plausible vs the proportional estimate
        bad = any((t1 - t0) < 0.075 for t0, t1 in times) or any(
            (t[1] - t[0]) > 3.0 * (e[1] - e[0]) + 0.25 for t, e in zip(times, est))
        if bad:
            times = est
    return [(w, round(t0, 3), round(t1, 3)) for w, (t0, t1) in zip(words, times)]


def mouth_env(a):
    hop = SR // FPS
    n = len(a) // hop + 1
    rms = np.array([np.sqrt(np.mean(a[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(n)])
    v = np.clip(rms / (np.percentile(rms, 90) + 1e-9), 0, 1)
    return [round(float(x), 3) for x in v]


# ---------- SFX (synthesized) ----------
def t_(d): return np.arange(int(d * SR)) / SR

def sfx_boom():
    t = t_(1.6); f = 55 * np.exp(-t * 1.2) + 28
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 2.6)
    n = np.random.RandomState(1).randn(len(t)); n = np.convolve(n, np.ones(60) / 60, "same") * np.exp(-t * 9)
    return (s * 0.9 + n * 0.5) * 0.9

def sfx_clink():
    t = t_(0.9); out = np.zeros_like(t)
    for f, a in [(2650, 1), (3970, 0.6), (5300, 0.3)]:
        out += a * np.sin(2 * np.pi * f * t) * np.exp(-t * 9)
    t2 = t_(0.5); splash = np.random.RandomState(3).randn(len(t2)); splash = np.convolve(splash, np.ones(12) / 12, "same") * np.exp(-t2 * 7) * 0.5
    out[int(0.12 * SR):int(0.12 * SR) + len(t2)] += splash[:len(out) - int(0.12 * SR)]
    return out * 0.35

def sfx_heartbeat(dur):
    out = np.zeros(int(dur * SR))
    beat = lambda: np.sin(2 * np.pi * 48 * t_(0.22)) * np.exp(-t_(0.22) * 18)
    t = 0.0
    while t < dur - 0.4:
        for off, a in [(0, 1.0), (0.24, 0.7)]:
            i = int((t + off) * SR); b = beat() * a
            out[i:i + len(b)] += b[:len(out) - i]
        t += 0.95
    return out * 0.75

def sfx_tick():
    t = t_(0.08); return np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 60) * 0.25

def sfx_chime():
    t = t_(2.0); out = np.zeros_like(t)
    for i, f in enumerate([1046.5, 1318.5, 1568, 2093]):
        tt = np.clip(t - i * 0.09, 0, None)
        out += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 3) * (t >= i * 0.09)
    return out * 0.12

def sfx_siren():
    t = t_(1.1)
    f = 700 + 900 * np.sin(np.pi * np.clip(t / 0.55, 0, 2)) ** 2
    s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.3 + np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.7
    s = np.convolve(s, np.ones(8) / 8, "same")
    return s * np.minimum(1, t * 20) * np.exp(-t * 1.5) * 0.12

def sfx_rain(dur):
    n = np.random.RandomState(9).randn(int(dur * SR))
    n = np.convolve(n, np.ones(6) / 6, "same") - np.convolve(n, np.ones(80) / 80, "same")
    drops = np.zeros_like(n); rs = np.random.RandomState(4)
    for i in rs.randint(0, len(n) - 400, int(dur * 25)):
        drops[i:i + 300] += rs.uniform(0.2, 1) * np.sin(2 * np.pi * rs.uniform(1500, 4000) * np.arange(300) / SR) * np.exp(-np.arange(300) / 40)
    env = np.minimum(1, np.arange(len(n)) / (0.5 * SR)) * np.minimum(1, (len(n) - np.arange(len(n))) / (0.5 * SR))
    return (n * 0.25 + drops * 0.15) * env * 0.5

def sfx_steps():
    out = np.zeros(int(1.8 * SR))
    for k in range(4):
        i = int(k * 0.42 * SR); t = t_(0.15)
        s = np.sin(2 * np.pi * 70 * t) * np.exp(-t * 30) * (0.9 - k * 0.18)
        out[i:i + len(s)] += s
    return out * 0.6

def sfx_beep():
    out = np.zeros(int(0.7 * SR))
    for k in range(2):
        t = t_(0.12); b = np.sin(2 * np.pi * 1320 * t) * np.minimum(1, (0.12 - t) * 80) * np.minimum(1, t * 200)
        i = int(k * 0.22 * SR); out[i:i + len(b)] += b
    return out * 0.35

def sfx_crash():
    t = t_(1.2); rs = np.random.RandomState(11)
    n = rs.randn(len(t)) * np.exp(-t * 7)
    n = n - np.convolve(n, np.ones(10) / 10, "same")
    out = n * 0.8
    for k in range(14):
        f = rs.uniform(2500, 6500); st_ = rs.uniform(0, 0.5); tt = np.clip(t - st_, 0, None)
        out += 0.25 * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 18) * (t >= st_)
    return out * 0.7

def sfx_knock():
    out = np.zeros(int(1.2 * SR))
    for k in range(3):
        t = t_(0.12); b = np.sin(2 * np.pi * 110 * t) * np.exp(-t * 45) + 0.3 * np.random.RandomState(k).randn(len(t)) * np.exp(-t * 80)
        i = int(k * 0.28 * SR); out[i:i + len(b)] += b
    return out * 0.6

def sfx_riser():
    t = t_(1.0); n = np.random.RandomState(5).randn(len(t))
    n = n - np.convolve(n, np.ones(30) / 30, "same")
    return n * (t / 1.0) ** 2 * 0.08


timeline = []
for sc in SCENES:
    pieces, lines_info = [], []
    cur = sc["lead"]
    pieces.append(np.zeros(int(sc["lead"] * SR), np.float32))
    for ln in sc["lines"]:
        spk, text, gap = ln[:3]
        sp_ = ln[3] if len(ln) > 3 else None
        chunks = re.split(r"(?<=[.,?!])\s+", text) if (SENT_PAUSE or COMMA_PAUSE) and not str(VOICES[spk][0]).startswith("gemini:") else [text]
        if len(chunks) > 1:
            parts_, wt, off_ = [], [], 0.0
            for ci, ch in enumerate(chunks):
                ac = trim(synth(spk, ch, sp_))
                wt += [(w, off_ + t0, off_ + t1) for w, t0, t1 in word_times(ac, ch)]
                parts_.append(ac); off_ += len(ac) / SR
                if ci < len(chunks) - 1:
                    p_ = SENT_PAUSE if ch[-1] in ".?!" else COMMA_PAUSE
                    parts_.append(np.zeros(int(p_ * SR), np.float32)); off_ += p_
            a = np.concatenate(parts_)
        else:
            a = trim(synth(spk, text, sp_))
            wt = word_times(a, text)
        lines_info.append(dict(spk=spk, text=text, start=round(cur, 3), dur=round(len(a) / SR, 3),
                               words=[(w, round(cur + t0, 3), round(cur + t1, 3)) for w, t0, t1 in wt],
                               env=mouth_env(a)))
        pieces.append(a); cur += len(a) / SR
        pieces.append(np.zeros(int(gap * SR), np.float32)); cur += gap
    pieces.append(np.zeros(int(sc["tail"] * SR), np.float32))
    voice = np.concatenate(pieces)
    dur = len(voice) / SR
    # snap scene length to whole frames
    nfr = int(round(dur * FPS)); dur = nfr / FPS
    voice = np.pad(voice, (0, max(0, int(dur * SR) - len(voice))))[:int(dur * SR)]
    fx = np.zeros_like(voice)
    sfx_events = []
    for kind, li, wi, off in sc["sfx"]:
        if li is None: t0 = off
        elif wi is None: t0 = lines_info[li]["start"] + off
        else: t0 = lines_info[li]["words"][wi][1] + off
        s = {"boom": sfx_boom, "clink": sfx_clink, "tick": sfx_tick, "chime": sfx_chime,
             "siren": sfx_siren, "riser": sfx_riser, "beep": sfx_beep, "crash": sfx_crash, "knock": sfx_knock}.get(kind)
        s = sfx_heartbeat(dur) if kind == "heartbeat" else sfx_rain(dur) if kind == "rain" else sfx_steps() if kind == "steps" else s()
        i = max(0, int(t0 * SR)); fx[i:i + len(s)] += s[:len(fx) - i]
        sfx_events.append((kind, round(t0, 3)))
    sf.write(f"{OUT}/audio/{sc['id']}_voice.wav", voice, SR)
    sf.write(f"{OUT}/audio/{sc['id']}_fx.wav", fx, SR)
    timeline.append(dict(id=sc["id"], dur=dur, frames=nfr, lines=lines_info, sfx=sfx_events))
    print(sc["id"], f"{dur:.2f}s", [(l['spk'], l['start'], l['dur']) for l in lines_info])

json.dump(timeline, open(f"{OUT}/timeline.json", "w"))
print("TOTAL", sum(s["dur"] for s in timeline))
