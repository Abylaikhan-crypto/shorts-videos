"""Mix voices + SFX + a synthesized mood pad into one track, then mux with the concatenated video."""
import numpy as np, soundfile as sf, json, subprocess, os
SR = 24000
import sys
HERE = os.path.abspath(sys.argv[1])
OUTNAME = sys.argv[2]
TL = json.load(open(f"{HERE}/timeline.json"))
MOOD = json.loads(sys.argv[3])
CHORDS = {"dark": [55, 110, 130.81, 164.81], "warm": [65.41, 130.81, 164.81, 196.0, 261.63],
          "tense": [55, 58.27, 82.41, 116.54], "sad": [43.65, 87.31, 110, 130.81, 164.81]}


def pad(freqs, n, t0, mood):
    t = (np.arange(n) + t0) / SR
    out = np.zeros(n)
    for i, f in enumerate(freqs):
        a = 1.0 / (1 + i * 0.35)
        for det in (-0.6, 0.6):
            out += a * np.sin(2 * np.pi * (f + det) * t + i) + 0.15 * a * np.sin(2 * np.pi * 2 * (f + det) * t)
    lfo = 0.75 + 0.25 * np.sin(2 * np.pi * (0.9 if mood == "tense" else 0.15) * t)
    return out * lfo / (len(freqs) * 2)


voice, fx, music = [], [], []
pos = 0
for i, s in enumerate(TL):
    v, _ = sf.read(f"{HERE}/audio/{s['id']}_voice.wav"); f, _ = sf.read(f"{HERE}/audio/{s['id']}_fx.wav")
    n = int(round(s["frames"] / 30 * SR)); v = np.pad(v, (0, max(0, n - len(v))))[:n]; f = np.pad(f, (0, max(0, n - len(f))))[:n]
    p = pad(CHORDS[MOOD[s["id"]]], n + int(0.4 * SR), pos, MOOD[s["id"]])
    voice.append(v); fx.append(f); music.append((pos, p))
    pos += n
V = np.concatenate(voice); F = np.concatenate(fx)
M = np.zeros(pos + int(0.5 * SR))
for p0, p in music:  # crossfade pads over 0.4 s
    env = np.ones(len(p)); k = int(0.4 * SR)
    env[:k] = np.linspace(0, 1, k); env[-k:] = np.linspace(1, 0, k)
    st = max(0, p0 - k // 2); M[st:st + len(p)] += (p * env)[:len(M) - st]
M = M[:pos]
# duck music under speech
spk = np.convolve(np.abs(V), np.ones(2400) / 2400, "same") > 0.02
duck = np.convolve(spk.astype(float), np.ones(4800) / 4800, "same")
mix = V * 1.0 + F * 0.9 + M * (0.16 - 0.07 * duck)
mix = np.tanh(mix * 1.1) / np.tanh(1.1) * 0.95
sf.write(f"{HERE}/audio/mix.wav", mix.astype(np.float32), SR)
open(f"{HERE}/scenes/list.txt", "w").write("".join(f"file '{s['id']}.mp4'\n" for s in TL))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{HERE}/scenes/list.txt", "-c", "copy",
                f"{HERE}/scenes/video.mp4"], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{HERE}/scenes/video.mp4", "-i", f"{HERE}/audio/mix.wav",
                "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-shortest", "-movflags", "+faststart",
                f"{HERE}/{OUTNAME}"], check=True)
print("ok", pos / SR)
