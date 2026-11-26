"""Procedural sound-effects library (48 kHz mono float). Every function returns a numpy array.
Recorded-style human sounds (scream, gasp, murmur) live in sfxlib/*.wav and are loaded by name."""
import numpy as np, soundfile as sf, os
from scipy import signal

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(7)


def T(d): return np.arange(int(round(d * SR))) / SR
def noise(d): return rng.standard_normal(int(round(d * SR)))
def env_exp(n, k): return np.exp(-np.arange(int(n)) / SR * k)
def adsr(n, a=0.01, r=0.1):
    e = np.ones(n); na, nr = min(n, int(a * SR)), min(n, int(r * SR))
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return e
def bp(x, lo, hi, o=2): return signal.sosfilt(signal.butter(o, [lo, hi], "band", fs=SR, output="sos"), x)
def lp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, "low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, "high", fs=SR, output="sos"), x)
def norm(x, pk=0.9): m = np.max(np.abs(x)) + 1e-9; return x / m * pk


def sweep_bp(x, f0, f1, q=3.0, steps=64):
    """band-pass whose centre glides f0->f1 (block-wise)."""
    out = np.zeros_like(x); n = len(x); b = n // steps + 1
    for i in range(steps):
        s = x[i * b:(i + 1) * b]
        if not len(s): break
        f = f0 * (f1 / f0) ** (i / (steps - 1)); w = f / q
        out[i * b:i * b + len(s)] = bp(s, max(30, f - w), min(SR / 2 - 100, f + w))
    return out


def reverb(x, size=0.8, wet=0.35, damp=4000):
    ir = noise(size) * env_exp(int(size * SR), 6.5 / size); ir = lp(ir, damp); ir /= np.sqrt((ir ** 2).sum())
    w = signal.fftconvolve(x, ir)[:len(x) + int(size * SR)]
    d = np.pad(x, (0, len(w) - len(x)))
    return d * (1 - wet) + w * wet * 0.6


# ---------------- transitions / cinematic ----------------
def whoosh(d=0.45, f0=250, f1=3500):
    x = sweep_bp(noise(d), f0, f1, q=2.2); n = len(x); t = np.linspace(0, 1, n)
    return norm(x * np.sin(np.pi * t) ** 1.6, 0.8)


def swish(d=0.22): return whoosh(d, 1200, 6000) * 0.8


def hit(d=1.6):
    t = T(d); n = len(t)
    sub = np.sin(2 * np.pi * (55 * np.exp(-t * 2.0) + 28) * t) * env_exp(n, 2.5)
    body = lp(noise(d), 600) * env_exp(n, 9)
    crack = hp(noise(d), 2500) * env_exp(n, 40) * 0.5
    return norm(reverb(sub * 1.0 + body * 0.8 + crack, 1.2, 0.3)[:n + SR // 2], 0.95)


def riser(d=2.0):
    t = T(d); n = len(t); u = t / d
    tone = sum(np.sin(2 * np.pi * f * (1 + 1.5 * u ** 2) * t) / (k + 1) for k, f in enumerate((110, 164.8, 220, 233)))
    air = sweep_bp(noise(d), 400, 7000, q=3)
    return norm((tone * 0.4 + air) * u ** 2.2, 0.85)


def sting():  # dissonant orchestral-ish stab for reveals
    d = 2.2; t = T(d); n = len(t); x = np.zeros(n)
    for f in (146.8, 155.6, 220, 311.1, 466.2):
        ph = 2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 5.5 * t)
        x += (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph)) * (1 + 0.003 * rng.standard_normal())
    x = lp(x, 3000) * env_exp(n, 1.8) * adsr(n, 0.015, 0.3)
    return norm(reverb(x + hit(d)[:n] * 0.6, 1.5, 0.4), 0.9)


def swell(d=4.0):  # warm heavenly chord for the light
    t = T(d); n = len(t); x = np.zeros(n)
    for k, f in enumerate((261.6, 329.6, 392.0, 523.3, 659.3, 784.0)):
        x += np.sin(2 * np.pi * f * t * (1 + 0.0015 * np.sin(2 * np.pi * (0.2 + k * 0.07) * t))) / (1 + 0.3 * k)
    e = np.minimum(1, t / (d * 0.6)) ** 2 * adsr(n, 0.01, 0.8)
    return norm(reverb(x * e, 2.0, 0.5), 0.7)


def heartbeat(d=3.0, bpm=80):
    out = np.zeros(int(d * SR)); per = 60 / bpm
    for b in np.arange(0, d - 0.3, per):
        for off, a in ((0, 1.0), (0.16, 0.7)):
            t = T(0.18); th = np.sin(2 * np.pi * 48 * t) * env_exp(len(t), 22) * a
            i = int((b + off) * SR); out[i:i + len(th)] += th[:len(out) - i]
    return norm(lp(out, 200), 0.9)


# ---------------- doors / objects ----------------
def click(d=0.03, f=3500):
    x = bp(noise(d), f * 0.6, min(f * 1.6, 20000)) * env_exp(int(d * SR), 180); return norm(x, 0.8)


def thud(d=0.5, f=70):
    t = T(d); n = len(t)
    return norm(np.sin(2 * np.pi * f * t) * env_exp(n, 14) + lp(noise(d), 400) * env_exp(n, 30) * 0.6, 0.9)


def creak(d=0.9):
    n = int(d * SR); x = np.zeros(n); t = 0.0
    while t < d - 0.01:
        u = t / d; rate = 45 + 90 * np.sin(np.pi * u) + 15 * rng.standard_normal()
        i = int(t * SR); x[i] += 1.0; t += 1 / max(25, rate)
    x = signal.lfilter([1], [1, -0.97], x)  # stick-slip pulses
    y = bp(x, 500, 1400, 3) + 0.5 * bp(x, 1800, 2600, 2)
    return norm(y * adsr(n, 0.05, 0.2), 0.7)


def door_open(): return norm(np.concatenate([click(0.04, 2500), np.zeros(int(0.05 * SR)), click(0.03, 4000) * 0.6,
                                             creak(0.9) * 0.8]), 0.8)


def door_close():
    x = thud(0.6, 65); c = click(0.04, 3000) * 0.5; x[int(0.03 * SR):int(0.03 * SR) + len(c)] += c
    return norm(reverb(x, 0.6, 0.25), 0.9)


def door_slam(): return norm(reverb(thud(0.8, 55) * 1.2 + hp(noise(0.8), 1500) * env_exp(int(0.8 * SR), 25) * 0.4, 1.0, 0.35), 1.0)


def beep(f=1800, d=0.09, a=0.6):
    t = T(d); return np.sin(2 * np.pi * f * t) * adsr(len(t), 0.003, 0.02) * a


def reader_ok():
    x = np.concatenate([beep(1760, 0.08), np.zeros(int(0.03 * SR)), beep(2350, 0.12), np.zeros(int(0.08 * SR))])
    return norm(np.concatenate([x, door_unlock()]), 0.8)


def reader_denied():
    t = T(0.25); b = signal.square(2 * np.pi * 330 * t) * 0.25 * adsr(len(t), 0.005, 0.03)
    return lp(np.concatenate([b, np.zeros(int(0.08 * SR)), b]), 3000)


def door_unlock():
    x = np.concatenate([click(0.03, 2000), np.zeros(int(0.06 * SR)), thud(0.25, 140) * 0.5 + 0])
    return norm(x, 0.8)


def card_slide():
    d = 0.35; x = sweep_bp(noise(d), 2500, 5500, q=4) * np.sin(np.pi * np.linspace(0, 1, int(d * SR))) ** 2
    return norm(np.concatenate([x, click(0.02, 5000) * 0.4]), 0.6)


def paper(d=0.6):
    n = int(d * SR); x = np.zeros(n)
    for _ in range(int(d * 40)):
        i = rng.integers(0, n - 2000); L = rng.integers(200, 1600)
        x[i:i + L] += hp(noise(L / SR), 1800) * env_exp(L, rng.uniform(60, 200)) * rng.uniform(0.3, 1)
    return norm(bp(x, 1500, 9000) * adsr(n, 0.05, 0.15), 0.6)


def steps(n=4, gap=0.5, soft=True):
    out = np.zeros(int((n * gap + 0.4) * SR))
    for k in range(n):
        t = T(0.15); s = lp(noise(0.15), 300 if soft else 900) * env_exp(len(t), 35) + np.sin(2 * np.pi * 80 * t) * env_exp(len(t), 40) * 0.6
        i = int((k * gap + 0.03 * rng.standard_normal() + 0.05) * SR); out[i:i + len(s)] += s * rng.uniform(0.7, 1)
    return norm(out, 0.7)


def elevator_dead():  # button clicked three times, nothing happens
    out = np.zeros(int(1.2 * SR))
    for k, t0 in enumerate((0.0, 0.35, 0.6)):
        c = thud(0.08, 220) * 0.3; c[:1200] += click(0.025, 2200); i = int(t0 * SR); out[i:i + len(c)] += c
    return norm(out, 0.6)


def clock_tick(n=6, gap=1.0):
    out = np.zeros(int(n * gap * SR))
    for k in range(n):
        c = click(0.02, 4500 if k % 2 else 3200); i = int(k * gap * SR); out[i:i + len(c)] += c
    return reverb(out, 0.5, 0.25)


def monitor_beep(n=4, gap=0.85):
    out = np.zeros(int(n * gap * SR))
    for k in range(n): b = beep(1000, 0.12, 0.5); i = int(k * gap * SR); out[i:i + len(b)] += b
    return reverb(out, 0.4, 0.2)


def phone_dead():  # short low "battery empty" buzz
    t = T(0.4); return norm(signal.square(2 * np.pi * 150 * t) * env_exp(len(t), 6) * adsr(len(t), 0.005, 0.05) * 0.3, 0.4)


# ---------------- electrical / TV ----------------
def static(d=1.0):
    x = bp(noise(d), 800, 9000); cr = (rng.random(int(d * SR)) > 0.9995) * rng.standard_normal(int(d * SR)) * 6
    return norm((x + cr) * adsr(int(d * SR), 0.01, 0.1), 0.6)


def tv_on():
    t = T(0.12); pop = np.sin(2 * np.pi * 90 * t) * env_exp(len(t), 30)
    return norm(np.concatenate([pop, static(0.7) * np.linspace(1, 0.2, int(0.7 * SR))]), 0.7)


def hum_tone(d, f=60, flick=0.0):
    t = T(d); x = sum(np.sin(2 * np.pi * f * k * t) / k for k in (1, 2, 3, 4, 6)) + 0.05 * hp(noise(d), 3000)
    if flick: x *= 1 - flick * (rng.random(len(t)) > 0.996).astype(float).cumsum() % 2
    return x


def power_down():
    d = 1.4; t = T(d); u = t / d; f = 60 * (1 - 0.8 * u)
    x = sum(np.sin(2 * np.pi * np.cumsum(f * k) / SR) / k for k in (1, 2, 3)) * (1 - u) ** 1.5
    c = thud(0.4, 60); x[:len(c)] += c * 0.8
    return norm(x, 0.8)


def power_up():
    c = np.concatenate([thud(0.25, 90), np.zeros(int(0.1 * SR))]); h = hum_tone(1.2, 60) * adsr(int(1.2 * SR), 0.02, 0.6) * 0.5
    b = np.concatenate([c, h]); fl = np.ones(len(b)); k = int(0.35 * SR)
    for s in (0.40, 0.48, 0.62): fl[int(s * SR):int(s * SR) + k // 6] = 0.2
    return norm(b * fl, 0.7)


# ---------------- ambience beds (loop-friendly) ----------------
def amb_room(d): return lp(np.cumsum(noise(d)) * 0.002, 300) + 0.002 * hum_tone(d, 50)
def amb_hall(d): return amb_room(d) + 0.010 * hum_tone(d, 60)
def amb_fog(d): return bp(noise(d), 150, 900) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.07 * T(d))) * 0.25


def amb_rain(d):
    x = bp(noise(d), 1500, 9000) * 0.25 + lp(noise(d), 500) * 0.25; n = len(x)
    drops = (rng.random(n) > 0.9985) * rng.uniform(0.2, 1, n); x += hp(signal.lfilter([1], [1, -0.9], drops), 2000) * 0.5
    return x


def amb_hospital(d):
    x = amb_room(d) * 0.6 + 0.3 * bp(noise(d), 300, 2000) * 0.03
    m = monitor_beep(int(d / 1.0) + 1, 1.0)[:len(x)] * 0.25
    return x + np.pad(m, (0, len(x) - len(m)))


def thunder(d=3.5):
    t = T(d); n = len(t); x = lp(noise(d), 180) * env_exp(n, 1.2) * (1 + 2 * env_exp(n, 6))
    return norm(reverb(x, 2.0, 0.4), 0.9)


def crash():
    d = 2.2; t = T(d); n = len(t)
    body = lp(noise(d), 1500) * env_exp(n, 3.5); boom = np.sin(2 * np.pi * 45 * t) * env_exp(n, 3)
    glass = np.zeros(n)
    for _ in range(40):
        i = rng.integers(int(0.05 * SR), int(1.4 * SR)); f = rng.uniform(3000, 8000); L = int(0.15 * SR)
        glass[i:i + L] += np.sin(2 * np.pi * f * T(0.15)) * env_exp(L, 30) * rng.uniform(0.1, 0.4)
    return norm(reverb(body + boom * 1.2 + glass, 1.2, 0.3), 1.0)


def brakes(d=1.4):
    t = T(d); f = 2600 + 120 * np.sin(2 * np.pi * 7 * t); x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    return norm((x * 0.5 + bp(noise(d), 2000, 4000) * 0.5) * adsr(len(t), 0.05, 0.2), 0.6)


def white_flash():  # bright airy "whoomp" into white
    return norm(whoosh(1.0, 200, 8000) * 0.6 + swell(1.6)[:int(1.0 * SR)] * 0.5, 0.8)


def load(name):
    x, sr = sf.read(f"{HERE}/sfxlib/{name}.wav")
    if x.ndim > 1: x = x.mean(1)
    if sr != SR: x = signal.resample_poly(x, SR, sr)
    return x


def scream(): return norm(reverb(load("scream_f2"), 1.4, 0.45), 0.9)
def gasp(): return norm(reverb(load("gasp"), 0.5, 0.2), 0.7)
def murmur(): return norm(reverb(load("murmur"), 0.8, 0.3), 0.6)


LIB = {k: v for k, v in globals().items() if callable(v) and not k.startswith("_") and k not in
       ("T", "noise", "env_exp", "adsr", "bp", "lp", "hp", "norm", "sweep_bp", "reverb", "load", "beep", "hum_tone")}
AMB = {"room": amb_room, "hall": amb_hall, "fog": amb_fog, "rain": amb_rain, "hospital": amb_hospital}
