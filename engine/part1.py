"""My Stepdad Is a Cop — Part 1. Usage: python part1.py preview s3 2.0 [more t...] | python part1.py render [scene...]"""
import cairo, json, os, sys, subprocess, random
from math import sin, cos, pi
from rig import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = {s["id"]: s for s in json.load(open(f"{HERE}/timeline.json"))}
ADD = cairo.OPERATOR_ADD

MAYA = dict(skin=(0.80, 0.58, 0.43), hair=(0.17, 0.10, 0.07), hairstyle="curly", outfit="hoodie",
            top=(0.18, 0.60, 0.62), eye=(0.12, 0.07, 0.05), blush=True, seed=1, pants=(0.25, 0.27, 0.36),
            shoes=(0.95, 0.95, 0.95))
DALE = dict(skin=(0.95, 0.76, 0.63), hair=(0.32, 0.22, 0.14), hairstyle="crew", outfit="uniform",
            top=(0.13, 0.19, 0.33), mustache=True, seed=2, wide=1.08, pants=(0.10, 0.13, 0.24))
MOM = dict(skin=(0.97, 0.82, 0.70), hair=(0.88, 0.70, 0.40), hairstyle="bob", outfit="sweater",
           top=(0.62, 0.42, 0.52), seed=3, blush=True, eye=(0.2, 0.3, 0.45))
ALV = dict(skin=(0.82, 0.60, 0.45), hair=(0.12, 0.08, 0.06), hairstyle="bun", outfit="cardigan",
           top=(0.86, 0.62, 0.22), seed=4)
MAYA_W = dict(MAYA, outfit="dress", top=(0.74, 0.62, 0.90), sleeve=MAYA["skin"], sleeve_frac=0.0, sash=(0.55, 0.42, 0.78))
MOM_W = dict(MOM, outfit="dress", top=(0.99, 0.98, 0.96), sleeve=MOM["skin"], sleeve_frac=0.0, sash=(0.95, 0.75, 0.8))
MAYA_S = dict(MAYA, outfit="longsleeve", top=(0.55, 0.57, 0.63))


def L(sc, i): return TL[sc]["lines"][i]
def Wd(sc, i, j): return TL[sc]["lines"][i]["words"][j][1]
def LEND(sc, i): l = TL[sc]["lines"][i]; return l["start"] + l["dur"]


def talk(sc, spk, t):
    for l in TL[sc]["lines"]:
        if l["spk"] == spk and l["start"] <= t < l["start"] + l["dur"]:
            i = int((t - l["start"]) * FPS); e = l["env"]
            return (e[min(i, len(e) - 1)] + e[max(0, min(i, len(e) - 1) - 1)]) / 2
    return 0.0


def ik(P, wx, wy, bend):
    lx, ly = local(P, wx, wy); return ("ik", lx, ly, bend)


# ======================= SCENE 1: hero outside the house =======================
STARS = [(random.Random(i).uniform(0, 1080), random.Random(i + 99).uniform(0, 820), random.Random(i + 7).uniform(1.5, 3.5)) for i in range(70)]


def house_night(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, 1350); g.add_color_stop_rgb(0, 0.04, 0.05, 0.14); g.add_color_stop_rgb(1, 0.13, 0.15, 0.32)
    ctx.set_source(g); ctx.paint()
    for i, (x, y, r) in enumerate(STARS):
        ell(ctx, x, y, r, r); ctx.set_source_rgba(1, 1, 0.9, 0.5 + 0.4 * sin(t * 3 + i)); ctx.fill()
    glow(ctx, 880, 300, 220, (0.6, 0.65, 0.9), 0.25)
    ell(ctx, 880, 300, 70, 70); ctx.set_source_rgb(0.95, 0.94, 0.85); ctx.fill()
    ell(ctx, 905, 285, 62, 62); ctx.set_source_rgb(0.09, 0.10, 0.24); ctx.fill()
    for x, r in [(-40, 160), (110, 130), (980, 170), (1100, 150)]:
        ell(ctx, x, 1180, r, r * 1.3); ctx.set_source_rgb(0.05, 0.08, 0.10); ctx.fill()
    poly(ctx, [(60, 790), (540, 500), (1020, 790)]); fs(ctx, (0.10, 0.09, 0.16))
    ctx.rectangle(120, 780, 840, 560); fs(ctx, (0.17, 0.16, 0.26))
    for y in range(820, 1340, 44):
        ctx.move_to(120, y); ctx.line_to(960, y); ctx.set_source_rgba(0, 0, 0, 0.18); ctx.set_line_width(3); ctx.stroke()
    for wx in (200, 720):
        glow(ctx, wx + 80, 950, 230, (1.0, 0.75, 0.35), 0.18)
        ctx.rectangle(wx, 880, 160, 140); fs(ctx, (1.0, 0.82, 0.46))
        ctx.move_to(wx + 80, 880); ctx.line_to(wx + 80, 1020); ctx.move_to(wx, 950); ctx.line_to(wx + 160, 950); st(ctx, OUTL, 6)
    ell(ctx, 540, 680, 48, 48); fs(ctx, (0.95, 0.72, 0.42))
    ctx.save(); ell(ctx, 540, 680, 45, 45); ctx.clip()  # small silhouette in the attic window (Maya)
    blob(ctx, [(530, 676, 18), (518, 668, 12), (544, 668, 12)], (0.12, 0.08, 0.10))
    ell(ctx, 530, 735, 34, 32); ctx.set_source_rgb(0.12, 0.08, 0.10); ctx.fill(); ctx.restore()
    rrect(ctx, 478, 1110, 124, 230, 8); fs(ctx, (0.30, 0.12, 0.12))
    ell(ctx, 585, 1230, 6, 6); fs(ctx, (0.9, 0.8, 0.4), 2)
    glow(ctx, 540, 1080, 120, (1, 0.8, 0.4), 0.45); ell(ctx, 540, 1082, 12, 16); fs(ctx, (1, 0.9, 0.6), 3)
    g = cairo.LinearGradient(0, 1330, 0, 1920); g.add_color_stop_rgb(0, 0.07, 0.13, 0.11); g.add_color_stop_rgb(1, 0.03, 0.06, 0.05)
    ctx.rectangle(0, 1330, 1080, 600); ctx.set_source(g); ctx.fill()
    poly(ctx, [(470, 1340), (610, 1340), (760, 1920), (330, 1920)]); ctx.set_source_rgb(0.20, 0.20, 0.25); ctx.fill()
    for x in (150, 300, 780, 930):
        blob(ctx, [(x, 1325, 60), (x + 50, 1305, 55), (x - 45, 1315, 50)], (0.08, 0.17, 0.13))


S1 = "s1"
t1b = L(S1, 1)["start"]
KEYS1 = [(0, 540, 960, 1.0), (t1b - 0.03, 600, 990, 1.2), (t1b, 655, 930, 2.05, "cut"), (TL[S1]["dur"], 655, 920, 2.35)]


def s1(ctx, t):
    cx, cy, z = cam(KEYS1, t)
    second = t >= t1b
    ctx.save(); apply_cam(ctx, cx, cy, z)
    house_night(ctx, t)
    red = draw_car(ctx, -10, 1470, 0.95, t)
    dale = dict(x=655, y=1444, s=1.6, legs=True, hat=True, look=0.25, mood="happy", blink=blinking(t, 2))
    if not second:
        dale["armR"] = ("ang", 2.35, 2.95 + 0.38 * sin(t * 10))
    else:
        dale.update(mood="cold", look=0.0, shadow=0.55, glint=True)
    draw_char(ctx, DALE, dale, t)
    lx, ly = 230 * 0.95 - 10, 1470 - 190 * 0.95
    glow(ctx, lx, ly, 750, (1, 0.1, 0.1) if red else (0.15, 0.3, 1), 0.42 if second else 0.32)
    ctx.restore()
    if second:
        overlay(ctx, (0.02, 0.02, 0.06), 0.28)
        overlay(ctx, (0.5, 0.0, 0.05) if red else (0.0, 0.05, 0.4), 0.10, ADD)
    vignette(ctx, 0.65 if second else 0.45)


# ======================= SCENE 2: wedding (memory) =======================
PETALS = [(random.Random(i * 3).uniform(-50, 1130), random.Random(i * 5).uniform(0, 1900), random.Random(i * 11).uniform(0.6, 1.4)) for i in range(45)]
S2 = "s2"
t2d = L(S2, 1)["start"]
KEYS2 = [(0, 540, 960, 1.0), (t2d - 0.03, 560, 1000, 1.14), (t2d, 590, 1030, 1.48, "cut"), (TL[S2]["dur"], 595, 1030, 1.62)]


def wedding_bg(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, 1150)
    g.add_color_stop_rgb(0, 0.96, 0.58, 0.48); g.add_color_stop_rgb(0.7, 1.0, 0.80, 0.60); g.add_color_stop_rgb(1, 1.0, 0.90, 0.68)
    ctx.set_source(g); ctx.paint()
    glow(ctx, 540, 1080, 420, (1, 0.9, 0.6), 0.6)
    for i, x in enumerate(range(-60, 1200, 110)):
        ell(ctx, x, 1110 + (i % 3) * 18, 90, 110); ctx.set_source_rgba(0.62, 0.45, 0.42, 0.55); ctx.fill()
    g = cairo.LinearGradient(0, 1120, 0, 1920); g.add_color_stop_rgb(0, 0.52, 0.68, 0.38); g.add_color_stop_rgb(1, 0.30, 0.48, 0.27)
    ctx.rectangle(0, 1120, 1080, 800); ctx.set_source(g); ctx.fill()
    for k, (y0, y1, sag) in enumerate([(230, 300, 120), (380, 340, 110)]):
        pts = [(x, lerp(y0, y1, x / 1080) + sag * sin(pi * x / 1080) + 4 * sin(t * 1.3 + k)) for x in range(-20, 1110, 10)]
        ctx.move_to(*pts[0])
        for p in pts[1:]: ctx.line_to(*p)
        st(ctx, (0.25, 0.18, 0.15), 3)
        for j, (x, y) in enumerate(pts[::7]):
            a = 0.75 + 0.25 * sin(t * 4 + j * 1.7 + k)
            glow(ctx, x, y + 14, 34, (1, 0.85, 0.5), 0.5 * a)
            ell(ctx, x, y + 14, 8, 11); ctx.set_source_rgba(1, 0.93, 0.7, a); ctx.fill()
    # arch
    for px in (300, 780):
        rrect(ctx, px - 18, 760, 36, 760, 10); fs(ctx, (0.98, 0.97, 0.94))
    ctx.new_path(); ctx.arc(540, 760, 240, pi, 2 * pi); st(ctx, OUTL, 36 + 2 * LW)
    ctx.new_path(); ctx.arc(540, 760, 240, pi, 2 * pi); st(ctx, (0.98, 0.97, 0.94), 36)
    fl = []
    for i in range(26):
        a = pi + i * pi / 25
        fl.append((540 + 240 * cos(a), 760 + 240 * sin(a)))
    for i in range(10):
        fl += [(300, 800 + i * 70), (780, 800 + i * 70)]
    for i, (x, y) in enumerate(fl):
        c = [(0.98, 0.70, 0.78), (1, 1, 1), (0.99, 0.82, 0.68), (0.85, 0.55, 0.70)][i % 4]
        ell(ctx, x + 14 * sin(i * 2.1), y + 10 * cos(i * 1.3), 22, 20); fs(ctx, c, 3.5)
        ell(ctx, x + 14 * sin(i * 2.1), y + 10 * cos(i * 1.3), 6, 6); ctx.set_source_rgb(0.95, 0.8, 0.3); ctx.fill()
        if i % 3 == 0:
            ell(ctx, x - 20, y + 18, 16, 8, 0.6); fs(ctx, (0.35, 0.6, 0.35), 3)


def s2(ctx, t):
    cx, cy, z = cam(KEYS2, t)
    ctx.save(); apply_cam(ctx, cx, cy, z)
    wedding_bg(ctx, t)
    dtalk = talk(S2, "D", t)
    mom = dict(x=540, y=1215, s=1.25, mood="happy", look=0.3, blink=blinking(t, 3))
    mom["armL"] = ik(mom, 520, 1100, 1); mom["armR"] = ik(mom, 560, 1100, -1)
    ell(ctx, 540, 830, 150, 240); ctx.set_source_rgba(1, 1, 1, 0.45); ctx.fill()
    draw_char(ctx, MOM_W, mom, t)
    for i, (dx, dy, c) in enumerate([(-22, -10, (1, 1, 1)), (18, -14, (0.98, 0.7, 0.78)), (0, 8, (0.99, 0.82, 0.68)), (-30, 14, (0.98, 0.7, 0.78)), (28, 12, (1, 1, 1)), (0, -30, (0.85, 0.55, 0.7))]):
        ell(ctx, 540 + dx, 1100 + dy, 20, 19); fs(ctx, c, 3.5)
    maya = dict(x=805, y=1445, s=1.2, mood="happy", look=-1, lookY=-0.2, blink=blinking(t, 1))
    dale = dict(x=380, y=1470, s=1.45, mood="happy", look=1, mouth=dtalk, blink=blinking(t, 2))
    shx, shy = 805 - 82 * 1.2, 1445 - 212 * 1.2 + 8
    u = ramp(t, t2d - 0.6, t2d + 0.1)
    dale["armR"] = ik(dale, lerp(380 + 150, shx, u), lerp(1470 - 60, shy, u), 1)
    draw_char(ctx, MAYA_W, maya, t)
    draw_char(ctx, DALE, dale, t)
    for i, (x, y0, sp) in enumerate(PETALS):
        y = (y0 + t * 120 * sp) % 1950 - 30
        xx = x + 30 * sin(t * 1.5 * sp + i)
        ell(ctx, xx, y, 9, 5, t * 2 * sp + i); ctx.set_source_rgba(0.98, 0.72, 0.8, 0.9); ctx.fill()
    for x in range(-40, 1150, 120):
        yb = 1500 + 30 * sin(x * 0.05)
        blob(ctx, [(x, yb, 95), (x + 60, yb + 40, 90), (x, yb + 180, 140)], (0.24, 0.42, 0.24))
        for k in range(3):
            fx, fy = x + 40 * sin(x + k * 2.0), yb - 30 + k * 40
            ell(ctx, fx, fy, 14, 13); fs(ctx, [(1, 1, 1), (0.98, 0.7, 0.78), (1, 0.85, 0.5)][k], 3)
    ctx.restore()
    overlay(ctx, (1.0, 0.82, 0.55), 0.10)
    vignette(ctx, 0.42, 420, 1200)


# ======================= SCENE 3: dinner =======================
S3 = "s3"
tk = Wd(S3, 0, 4)
tD3 = L(S3, 1)["start"]
t33 = L(S3, 2)["start"]
tMom = Wd(S3, 2, 8)
KEYS3 = [(0, 540, 960, 1.0), (tk - 0.12, 540, 990, 1.07), (tk - 0.1, 770, 1180, 1.75, "cut"), (tD3 - 0.1, 770, 1180, 1.9),
         (tD3 - 0.08, 540, 960, 2.45, "cut"), (t33 - 0.02, 540, 955, 2.75), (t33, 860, 1050, 2.15, "cut"),
         (tMom - 0.12, 860, 1045, 2.3), (tMom - 0.1, 220, 1030, 2.15, "cut"), (TL[S3]["dur"], 220, 1030, 2.3)]
GLASS = (741, 1347)


def dining_bg(ctx, t, dim):
    ctx.set_source_rgb(*mix((0.56, 0.60, 0.50), (0.2, 0.22, 0.25), dim)); ctx.paint()
    for x in range(0, 1080, 64):
        ctx.rectangle(x, 0, 30, 1150); ctx.set_source_rgba(0, 0, 0, 0.05); ctx.fill()
    ctx.rectangle(0, 1150, 1080, 300); ctx.set_source_rgb(*mix((0.42, 0.30, 0.22), (0.15, 0.12, 0.12), dim)); ctx.fill()
    ctx.rectangle(60, 400, 280, 400); fs(ctx, (0.10, 0.14, 0.28))
    ell(ctx, 250, 500, 30, 30); ctx.set_source_rgb(0.85, 0.85, 0.75); ctx.fill()
    ctx.move_to(200, 400); ctx.line_to(200, 800); ctx.move_to(60, 600); ctx.line_to(340, 600); st(ctx, (0.9, 0.9, 0.85), 10)
    for sx, x0 in ((1, 30), (-1, 370)):
        ctx.move_to(x0, 380); ctx.curve_to(x0 + sx * 90, 500, x0 + sx * 40, 700, x0 + sx * 70, 840); ctx.line_to(x0, 840); ctx.close_path()
        fs(ctx, (0.55, 0.16, 0.18))
    rrect(ctx, 690, 470, 230, 180, 6); fs(ctx, (0.55, 0.40, 0.22))
    ctx.rectangle(708, 488, 194, 144); ctx.set_source_rgb(1.0, 0.85, 0.65); ctx.fill()
    ctx.new_path(); ctx.arc(805, 600, 60, pi, 2 * pi); st(ctx, (1, 1, 1), 8)
    for x, c in [(780, (0.13, 0.19, 0.33)), (830, (0.98, 0.98, 0.98)), (812, (0.74, 0.62, 0.9))]:
        ell(ctx, x, 590 if x != 812 else 605, 9, 9); ctx.set_source_rgb(*C(c)); ctx.fill()
        rrect(ctx, x - 9, 600 if x != 812 else 612, 18, 30 if x != 812 else 18, 5); ctx.fill()


def lamp(ctx, t, inten):
    sw = 10 * sin(t * 1.1)
    ctx.move_to(540, 0); ctx.line_to(540 + sw, 250); st(ctx, OUTL, 5)
    ctx.save(); ctx.set_operator(ADD)
    g = cairo.LinearGradient(0, 330, 0, 1400); g.add_color_stop_rgba(0, 1, 0.85, 0.5, 0.25 * inten); g.add_color_stop_rgba(1, 1, 0.85, 0.5, 0)
    poly(ctx, [(450 + sw, 330), (630 + sw, 330), (1000, 1400), (80, 1400)]); ctx.set_source(g); ctx.fill(); ctx.restore()
    poly(ctx, [(500 + sw, 250), (580 + sw, 250), (640 + sw, 335), (440 + sw, 335)]); fs(ctx, mix((0.95, 0.75, 0.35), (0.3, 0.25, 0.2), 1 - inten))
    glow(ctx, 540 + sw, 345, 120, (1, 0.85, 0.5), 0.6 * inten)


def s3(ctx, t):
    dim = ramp(t, tD3 - 0.1, tD3 + 0.2) * 0.75
    cx, cy, z = cam(KEYS3, t)
    ctx.save(); apply_cam(ctx, cx, cy, z)
    dining_bg(ctx, t, dim * 0.6)
    knocked = t >= tk
    mom = dict(x=200, y=1445, s=1.22, mood="neutral", look=0.4, blink=blinking(t, 3))
    dale = dict(x=540, y=1455, s=1.45, mood="neutral", look=0.2, lookY=0.5, blink=blinking(t, 2), mouth=talk(S3, "D", t))
    maya = dict(x=870, y=1445, s=1.18, mood="neutral", look=-0.3, lookY=0.4, blink=blinking(t, 1))
    if knocked:
        maya.update(mood="shock", look=-0.6, lookY=0.6)
        mom.update(mood="worried", look=1, lookY=0.2)
        if t > tk + 0.35: dale.update(mood="cold", look=1, lookY=0.1)
    if t >= tD3 - 0.1:
        dale.update(mood="angry", look=0, lookY=0, shadow=0.45, glint=True)
        maya.update(mood="scared", look=-1, lookY=0)
        mom.update(mood="worried", look=0.2, lookY=1)
    if t >= t33:
        maya.update(mood="scared", look=-0.8, lookY=0.4, tear=t > t33 + 0.9)
        dale.update(mood="cold", lookY=0.4, look=0.6)
        mom.update(mood="sad", look=0.15, lookY=1, blink=False)
    mom["armL"] = ik(mom, 150, 1352, 1); mom["armR"] = ik(mom, 270, 1352, -1)
    dale["armL"] = ik(dale, 440, 1352, 1); dale["armR"] = ik(dale, 640, 1352, -1)
    jerk = ramp(t, tk - 0.15, tk + 0.02)
    maya["armL"] = ik(maya, lerp(800, 768, jerk), lerp(1350, 1330, jerk), 1)
    maya["armR"] = ik(maya, 950, 1352, -1)
    draw_char(ctx, MOM, mom, t); draw_char(ctx, DALE, dale, t); draw_char(ctx, MAYA, maya, t)
    # table
    ctx.rectangle(-10, 1335, 1100, 70); fs(ctx, mix((0.95, 0.92, 0.85), (0.4, 0.38, 0.38), dim * 0.5))
    ctx.rectangle(-10, 1400, 1100, 530); fs(ctx, mix((0.88, 0.84, 0.76), (0.35, 0.33, 0.33), dim * 0.5))
    for x in range(60, 1080, 150):
        ctx.move_to(x, 1410); ctx.curve_to(x + 20, 1600, x - 20, 1750, x + 10, 1920); ctx.set_source_rgba(0, 0, 0, 0.08); ctx.set_line_width(6); ctx.stroke()
    for x in (200, 540, 870):
        ell(ctx, x, 1366, 92, 22); fs(ctx, (0.98, 0.98, 0.98), 4)
        ell(ctx, x - 20, 1362, 34, 10); ctx.set_source_rgb(0.55, 0.32, 0.2); ctx.fill()
        for k in range(5):
            ell(ctx, x + 25 + 7 * k, 1366 + 3 * sin(k * 2), 6, 5); ctx.set_source_rgb(0.4, 0.7, 0.3); ctx.fill()
    # juice: puddle, drip, glass
    pu = ramp(t, tk + 0.12, tk + 0.9)
    if knocked:
        ell(ctx, 690, 1368, 125 * pu, 20 * pu); ctx.set_source_rgba(0.98, 0.62, 0.15, 0.9); ctx.fill()
        dr = ramp(t, tk + 0.5, tk + 2.2)
        if dr > 0:
            ctx.move_to(620, 1398); ctx.line_to(700, 1398); ctx.curve_to(700, 1398 + 120 * dr, 680, 1398 + 160 * dr, 662, 1398 + 170 * dr)
            ctx.curve_to(645, 1398 + 160 * dr, 650, 1398 + 60 * dr, 620, 1398); ctx.set_source_rgba(0.95, 0.6, 0.18, 0.75); ctx.fill()
    ang = -pi / 2 * ramp(t, tk + 0.02, tk + 0.22)
    ctx.save(); ctx.translate(*GLASS); ctx.rotate(ang)
    full = 1 - ramp(t, tk + 0.1, tk + 0.6)
    ctx.rectangle(0, -64, 38, 64)
    ctx.set_source_rgba(0.85, 0.95, 1.0, 0.55); ctx.fill_preserve(); ctx.set_source_rgb(*OUTL); ctx.set_line_width(4); ctx.stroke()
    if full > 0.02:
        ctx.rectangle(3, -60 * full + (0 if ang > -0.3 else 0), 32, 58 * full); ctx.set_source_rgba(0.98, 0.62, 0.15, 0.95); ctx.fill()
    ctx.restore()
    lamp(ctx, t, 1 - dim * 0.8)
    ctx.restore()
    if dim > 0: overlay(ctx, (0.02, 0.03, 0.10), 0.25 * dim)
    vignette(ctx, 0.4 + 0.35 * dim)


# ======================= SCENE 4: hallway / grip / threat =======================
S4 = "s4"
tHis = Wd(S4, 0, 8)
tD4 = L(S4, 1)["start"]
tNumb = Wd(S4, 0, 16)
tCop = Wd(S4, 1, 14)


def hallway(ctx, t):
    ctx.set_source_rgb(0.07, 0.08, 0.15); ctx.paint()
    poly(ctx, [(0, 0), (1080, 0), (700, 560), (380, 560)]); ctx.set_source_rgb(0.05, 0.06, 0.12); ctx.fill()
    poly(ctx, [(0, 0), (380, 560), (380, 1150), (0, 1920)]); ctx.set_source_rgb(0.10, 0.11, 0.21); ctx.fill()
    poly(ctx, [(1080, 0), (700, 560), (700, 1150), (1080, 1920)]); ctx.set_source_rgb(0.09, 0.10, 0.19); ctx.fill()
    ctx.rectangle(380, 560, 320, 590); ctx.set_source_rgb(0.12, 0.13, 0.24); ctx.fill()
    poly(ctx, [(0, 1920), (1080, 1920), (700, 1150), (380, 1150)]); ctx.set_source_rgb(0.08, 0.07, 0.10); ctx.fill()
    poly(ctx, [(360, 1920), (720, 1920), (600, 1150), (480, 1150)]); ctx.set_source_rgb(0.20, 0.07, 0.09); ctx.fill()
    ctx.rectangle(475, 780, 130, 370); fs(ctx, (0.16, 0.14, 0.22))
    ctx.rectangle(475, 1142, 130, 8); ctx.set_source_rgb(1, 0.8, 0.45); ctx.fill()
    for (x0, y0, w, h) in [(90, 640, 150, 170), (230, 760, 90, 110)]:
        k = w / 150
        poly(ctx, [(x0, y0), (x0 + w, y0 + 60 * k), (x0 + w, y0 + 60 * k + h), (x0, y0 + h)]); fs(ctx, (0.25, 0.2, 0.15))
    poly(ctx, [(860, 690), (1000, 560), (1000, 1720), (860, 1430)]); ctx.set_source_rgb(1.0, 0.82, 0.5); ctx.fill()
    poly(ctx, [(860, 690), (930, 650), (930, 1560), (860, 1430)]); fs(ctx, (0.22, 0.18, 0.25))
    ctx.save(); ctx.set_operator(ADD)
    g = cairo.LinearGradient(1000, 1500, 300, 1900); g.add_color_stop_rgba(0, 1, 0.8, 0.45, 0.35); g.add_color_stop_rgba(1, 1, 0.8, 0.45, 0)
    poly(ctx, [(930, 1560), (1000, 1720), (600, 1920), (250, 1920)]); ctx.set_source(g); ctx.fill(); ctx.restore()


KEYS4 = [(0, 540, 960, 1.0), (tHis - 0.06, 520, 1060, 1.12)]


def grip_insert(ctx, t, tt):
    g = cairo.LinearGradient(0, 0, 1080, 1920); g.add_color_stop_rgb(0, 0.05, 0.05, 0.12); g.add_color_stop_rgb(1, 0.12, 0.08, 0.14)
    ctx.set_source(g); ctx.paint()
    glow(ctx, 900, 1500, 900, (1, 0.75, 0.4), 0.18)
    z = 1.12 + 0.1 * tt
    ctx.save(); ctx.translate(540, 900); ctx.scale(z, z); ctx.translate(-440, -930)
    squeeze = 0.5 + 0.5 * sm(tt * 3)
    numb = ramp(t, tNumb - 0.2, tNumb + 0.4)
    skin = mix(MAYA["skin"], (0.72, 0.68, 0.75), numb * 0.55)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    # Maya forearm from lower right to hand at left
    ctx.move_to(1250, 1500); ctx.line_to(640, 1060); st(ctx, OUTL, 210 + 12)
    ctx.move_to(1250, 1500); ctx.line_to(640, 1060); st(ctx, MAYA["top"], 210)
    ctx.move_to(660, 1075); ctx.line_to(330, 860); st(ctx, OUTL, 128 - 10 * squeeze)
    ctx.move_to(660, 1075); ctx.line_to(330, 860); st(ctx, skin, 116 - 10 * squeeze)
    ctx.new_path()
    tr = 6 * numb * sin(t * 40)
    for i, (a, ln) in enumerate([(-2.55, 150), (-2.85, 165), (-3.12, 155), (-3.4, 130)]):
        a2 = a + 0.25 * sm(tt * 2) * (1 - numb * 0.4) + 0.05 * sin(t * 7 + i) + tr * 0.004
        x0, y0 = 300 + 30 * cos(a), 845 + 30 * sin(a)
        x1, y1 = x0 + ln * cos(a2), y0 + ln * sin(a2)
        ctx.move_to(x0, y0); ctx.line_to(x1, y1); st(ctx, OUTL, 50); ctx.move_to(x0, y0); ctx.line_to(x1, y1); st(ctx, skin, 40)
    ell(ctx, 300, 860, 95, 82, 0.6); fs(ctx, skin, 6)
    ctx.move_to(330, 930); ctx.line_to(250, 1010); st(ctx, OUTL, 50); ctx.move_to(330, 930); ctx.line_to(250, 1010); st(ctx, skin, 40)
    # Dale's hand around the wrist, coming from top
    ctx.move_to(780, -150); ctx.line_to(590, 760); st(ctx, OUTL, 250 + 12)
    ctx.move_to(780, -150); ctx.line_to(590, 760); st(ctx, DALE["top"], 250)
    rrect(ctx, 470, 700, 250, 70, 14); fs(ctx, shade(DALE["top"], 0.2))
    ell(ctx, 560, 880, 140, 120, 0.25); fs(ctx, DALE["skin"], 6)
    for i in range(4):
        fx0 = 460 + i * 62
        curl = 60 + 25 * squeeze
        ctx.move_to(fx0, 930); ctx.curve_to(fx0 - 15, 990, fx0 - 30, 1040 + curl * 0.3, fx0 - 60, 1060 + curl * 0.2)
        st(ctx, OUTL, 64); ctx.move_to(fx0, 930); ctx.curve_to(fx0 - 15, 990, fx0 - 30, 1040 + curl * 0.3, fx0 - 60, 1060 + curl * 0.2)
        st(ctx, DALE["skin"], 52)
        ctx.move_to(fx0 - 38, 1010); ctx.line_to(fx0 - 22, 1018); st(ctx, shade(DALE["skin"], 0.3), 4)
    ctx.move_to(420, 860); ctx.curve_to(380, 920, 400, 990, 440, 1000); st(ctx, OUTL, 70)
    ctx.move_to(420, 860); ctx.curve_to(380, 920, 400, 990, 440, 1000); st(ctx, DALE["skin"], 58)
    ctx.restore()
    overlay(ctx, (0.05, 0.0, 0.1), 0.15)


def s4(ctx, t):
    if t < tHis - 0.05:
        cx, cy, z = cam(KEYS4, t)
        ctx.save(); apply_cam(ctx, cx, cy, z)
        hallway(ctx, t)
        maya = dict(x=780, y=1560, s=1.25, legs=True, mood="scared", look=-1, lookY=-0.3, blink=blinking(t, 1))
        dx = lerp(-260, 290, sm(t / 1.15))
        dale = dict(x=dx, y=1600, s=1.85, legs=True, mood="cold", look=1, lookY=0.3, dark=0.62, shadow=0.5, glint=True)
        g_ = ramp(t, 1.15, 1.6)
        rest = (780 - 128, 1550)
        maya["armL"] = ik(maya, lerp(rest[0], 612, g_), lerp(rest[1], 1440, g_), -1)
        dale["armR"] = ik(dale, lerp(dx + 160, 612, g_), lerp(1560, 1432, g_), 1)
        draw_char(ctx, MAYA, maya, t)
        draw_char(ctx, DALE, dale, t)
        ctx.restore()
        overlay(ctx, (0.0, 0.03, 0.15), 0.25)
    elif t < tD4 - 0.03:
        grip_insert(ctx, t, (t - tHis) / (tD4 - tHis))
    else:
        tt = (t - tD4) / (TL[S4]["dur"] - tD4)
        ctx.save(); z = 1.0 + 0.16 * sm(tt)
        ctx.translate(540, 960); ctx.scale(z, z); ctx.translate(-540, -980)
        g = cairo.LinearGradient(0, 0, 0, 1920); g.add_color_stop_rgb(0, 0.04, 0.05, 0.12); g.add_color_stop_rgb(1, 0.10, 0.08, 0.14)
        ctx.set_source(g); ctx.paint()
        ctx.rectangle(860, 300, 120, 1200); ctx.set_source_rgba(1, 0.8, 0.45, 0.25); ctx.fill()
        dale = dict(x=540, y=1990, s=3.0, mood="angry", look=0, lookY=0.15, dark=0.22, shadow=0.62, glint=True,
                    mouth=talk(S4, "D", t), blink=blinking(t, 2) and t < tCop - 0.5)
        draw_char(ctx, DALE, dale, t)
        ctx.save(); ctx.set_operator(ADD)
        g = cairo.LinearGradient(1080, 0, 600, 0); g.add_color_stop_rgba(0, 1, 0.75, 0.4, 0.25); g.add_color_stop_rgba(1, 1, 0.75, 0.4, 0)
        ctx.rectangle(0, 0, 1080, 1920); ctx.set_source(g); ctx.fill(); ctx.restore()
        gl = ramp(t, tCop - 0.05, tCop + 0.12) * (1 - ramp(t, tCop + 0.25, tCop + 0.8))
        if gl > 0:
            bx, by = 540 + 46 * 3.0, 1990 - 180 * 3.0
            glow(ctx, bx, by, 160, (1, 0.9, 0.6), 0.8 * gl)
            star(ctx, bx, by, 90 * gl, n=4, inner=0.12); ctx.set_source_rgba(1, 1, 0.9, gl); ctx.fill()
        ctx.restore()
        overlay(ctx, (0.0, 0.03, 0.15), 0.18)
    beat = (t % 0.95)
    pulse = max(sm(1 - beat / 0.18), 0.6 * sm(1 - abs(beat - 0.3) / 0.15)) if beat < 0.45 else 0
    vignette(ctx, 0.62 + 0.18 * pulse, 380, 1150)


# ======================= SCENE 5: long sleeves in July =======================
S5 = "s5"
tIn = Wd(S5, 0, 7)
KEYS5 = [(0, 540, 1130, 1.55), (tIn - 0.06, 540, 1110, 1.68), (tIn - 0.04, 875, 690, 2.5, "cut"), (TL[S5]["dur"], 875, 690, 2.7)]


def bathroom(ctx, t):
    ctx.set_source_rgb(0.78, 0.88, 0.92); ctx.paint()
    for x in range(0, 1081, 90):
        ctx.move_to(x, 0); ctx.line_to(x, 1920)
    for y in range(0, 1921, 90):
        ctx.move_to(0, y); ctx.line_to(1080, y)
    ctx.set_source_rgb(0.70, 0.80, 0.85); ctx.set_line_width(4); ctx.stroke()
    ctx.rectangle(50, 320, 290, 450); fs(ctx, (0.80, 0.93, 1.0))
    glow(ctx, 260, 420, 160, (1, 1, 0.8), 0.9)
    ctx.move_to(195, 320); ctx.line_to(195, 770); ctx.move_to(50, 545); ctx.line_to(340, 545); st(ctx, (1, 1, 1), 12)
    ctx.save(); ctx.set_operator(ADD)
    poly(ctx, [(50, 320), (340, 320), (900, 1500), (350, 1700)]); ctx.set_source_rgba(1, 0.95, 0.7, 0.10); ctx.fill(); ctx.restore()
    # calendar
    ell(ctx, 875, 375, 6, 6); fs(ctx, (0.5, 0.5, 0.5), 3)
    ctx.move_to(875, 375); ctx.line_to(800, 410); ctx.move_to(875, 375); ctx.line_to(950, 410); st(ctx, OUTL, 3)
    rrect(ctx, 770, 400, 210, 335, 8); fs(ctx, (1, 1, 1))
    rrect(ctx, 770, 400, 210, 70, 8); fs(ctx, (0.88, 0.2, 0.2))
    text(ctx, "JULY", 875, 452, 44, col=(1, 1, 1))
    for r in range(4):
        for c in range(5):
            x, y = 785 + c * 38, 485 + r * 46
            ctx.rectangle(x, y, 32, 38); ctx.set_source_rgb(0.90, 0.91, 0.94); ctx.fill()
            text(ctx, str(r * 5 + c + 8), x + 16, y + 27, 17, col=(0.35, 0.35, 0.4))
    x, y = 785 + 2 * 38 + 16, 485 + 1 * 46 + 19
    ell(ctx, x, y, 22, 22); ctx.set_source_rgba(0.9, 0.2, 0.2, 0.0); ctx.fill()
    ctx.rectangle(785 + 2 * 38 - 2, 485 + 46 - 2, 36, 42); st(ctx, (0.88, 0.2, 0.2), 5)
    star(ctx, 815, 700, 16, n=8, inner=0.6); ctx.set_source_rgb(1, 0.75, 0.1); ctx.fill()
    text(ctx, "98°F", 895, 713, 34, col=(0.88, 0.2, 0.2))


def s5(ctx, t):
    cx, cy, z = cam(KEYS5, t)
    ctx.save(); apply_cam(ctx, cx, cy, z)
    bathroom(ctx, t)
    maya = dict(x=540, y=1520, s=1.5, mood="sad", look=-0.25, lookY=0.9, sleeve_pull=ramp(t, 0.7, 1.9), blink=blinking(t, 1))
    draw_char(ctx, MAYA_S, maya, t)
    rrect(ctx, -20, 1470, 1120, 500, 20); fs(ctx, (0.97, 0.97, 0.98))
    ell(ctx, 540, 1540, 260, 46); fs(ctx, (0.88, 0.92, 0.95))
    rrect(ctx, 520, 1420, 40, 70, 10); fs(ctx, (0.75, 0.78, 0.82))
    ctx.restore()
    if t >= tIn - 0.04:
        u = ramp(t, tIn, tIn + 0.25)
        overlay(ctx, (1, 0.9, 0.5), 0.08 * u, ADD)
    vignette(ctx, 0.3)


# ======================= SCENE 6: counselor =======================
S6 = "s6"
tA = L(S6, 1)["start"]
t63 = L(S6, 2)["start"]
KEYS6 = [(0, 540, 960, 1.0), (tA - 0.05, 540, 1000, 1.1), (tA - 0.03, 330, 1010, 1.9, "cut"), (t63 - 0.05, 330, 1005, 2.02),
         (t63 - 0.03, 800, 1060, 1.9, "cut"), (TL[S6]["dur"], 800, 1060, 2.05)]


def office_bg(ctx, t):
    ctx.set_source_rgb(0.96, 0.91, 0.80); ctx.paint()
    ctx.rectangle(0, 1250, 1080, 700); ctx.set_source_rgb(0.86, 0.78, 0.64); ctx.fill()
    ctx.rectangle(390, 330, 300, 390); fs(ctx, (0.75, 0.88, 0.98))
    ell(ctx, 470, 560, 70, 80); ctx.set_source_rgb(0.45, 0.68, 0.40); ctx.fill()
    ctx.rectangle(462, 600, 16, 120); ctx.set_source_rgb(0.45, 0.32, 0.2); ctx.fill()
    ctx.move_to(540, 330); ctx.line_to(540, 720); ctx.move_to(390, 525); ctx.line_to(690, 525); st(ctx, (1, 1, 1), 12)
    ctx.rectangle(30, 300, 270, 900); fs(ctx, (0.55, 0.38, 0.24))
    cols = [(0.8, 0.3, 0.3), (0.3, 0.5, 0.8), (0.9, 0.7, 0.3), (0.4, 0.65, 0.45), (0.6, 0.4, 0.7)]
    for r, y in enumerate((320, 520, 720, 920)):
        x = 45
        for i in range(8):
            w = 22 + (i * 7 + r * 3) % 12
            ctx.rectangle(x, y + 30 + (i % 3) * 8, w, 160 - (i % 3) * 8); fs(ctx, cols[(i + r) % 5], 3)
            x += w + 4
        ctx.rectangle(30, y + 190, 270, 14); fs(ctx, (0.45, 0.30, 0.18), 3)
    rrect(ctx, 760, 330, 250, 380, 10); fs(ctx, (0.40, 0.62, 0.85))
    ell(ctx, 885, 430, 1, 1)
    ctx.move_to(885, 470); ctx.curve_to(820, 420, 830, 360, 885, 395); ctx.curve_to(940, 360, 950, 420, 885, 470); ctx.close_path()
    fs(ctx, (1, 0.45, 0.5), 4)
    text(ctx, "YOU ARE", 885, 560, 46, col=(1, 1, 1))
    text(ctx, "NOT ALONE", 885, 620, 46, col=(1, 1, 1))
    rrect(ctx, 920, 1080, 120, 150, 14); fs(ctx, (0.85, 0.45, 0.3))
    for k in range(7):
        a = -pi / 2 + (k - 3) * 0.35
        ell(ctx, 980 + 90 * cos(a), 1060 + 110 * sin(a), 26, 60, a + pi / 2); fs(ctx, (0.3, 0.6, 0.35), 4)


def desk(ctx):
    ctx.rectangle(-10, 1385, 1100, 50); fs(ctx, (0.62, 0.42, 0.26))
    ctx.rectangle(-10, 1430, 1100, 500); fs(ctx, (0.50, 0.33, 0.20))
    rrect(ctx, 500, 1310, 110, 80, 8); fs(ctx, (0.45, 0.75, 0.85))
    ctx.move_to(540, 1312); ctx.curve_to(520, 1270, 570, 1260, 555, 1240); ctx.line_to(575, 1240)
    ctx.curve_to(590, 1270, 560, 1280, 570, 1312); ctx.close_path(); fs(ctx, (1, 1, 1), 3)
    rrect(ctx, 100, 1320, 70, 70, 10); fs(ctx, (0.95, 0.95, 0.9))
    ctx.new_path(); ctx.arc(175, 1355, 20, -pi / 2, pi / 2); st(ctx, OUTL, 6)


def s6(ctx, t):
    cx, cy, z = cam(KEYS6, t)
    ctx.save(); apply_cam(ctx, cx, cy, z)
    office_bg(ctx, t)
    alv = dict(x=300, y=1460, s=1.32, mood="worried", look=1, lookY=0.5, glasses=True, blink=blinking(t, 4), mouth=talk(S6, "A", t))
    maya = dict(x=800, y=1470, s=1.18, mood="sad", look=-0.2, lookY=1, blink=blinking(t, 1))
    if t >= tA - 0.03:
        alv.update(lookY=0.0); maya.update(mood="scared", look=-1, lookY=0.2)
    if t >= t63 - 0.03:
        maya.update(mood="sad", look=-1, lookY=0, tear=True, blink=False)
    alv["armL"] = ik(alv, 255, 1392, 1); alv["armR"] = ik(alv, 345, 1392, -1)
    maya["armL"] = ("ik", 15, -92, 1); maya["armR"] = ("ik", -8, -102, -1)
    draw_char(ctx, ALV, alv, t); draw_char(ctx, MAYA, maya, t)
    desk(ctx)
    ctx.restore()
    vignette(ctx, 0.35)


# ======================= SCENE 7: the cliffhanger =======================
S7 = "s7"
tPol = Wd(S7, 0, 4)
t72 = L(S7, 1)["start"]
tDale = Wd(S7, 1, 9)
tEnd = LEND(S7, 1) + 0.25
KEYS7 = [(0, 540, 960, 1.0), (t72 - 0.05, 470, 900, 1.12)]


def s7_window(ctx, t):
    ctx.set_source_rgb(0.95, 0.90, 0.80); ctx.paint()
    ctx.rectangle(0, 1500, 1080, 500); ctx.set_source_rgb(0.80, 0.72, 0.60); ctx.fill()
    ctx.rectangle(70, 330, 580, 660); fs(ctx, (0.97, 0.97, 0.97), 6)
    ctx.save(); ctx.rectangle(90, 350, 540, 620); ctx.clip()
    g = cairo.LinearGradient(0, 350, 0, 820); g.add_color_stop_rgb(0, 0.55, 0.78, 0.96); g.add_color_stop_rgb(1, 0.85, 0.93, 1.0)
    ctx.set_source(g); ctx.paint()
    ctx.rectangle(60, 610, 700, 160); ctx.set_source_rgb(0.72, 0.42, 0.35); ctx.fill()
    for x in range(80, 700, 70):
        ctx.rectangle(x, 640, 40, 50); ctx.set_source_rgb(0.85, 0.92, 0.98); ctx.fill()
    ctx.rectangle(60, 770, 700, 250); ctx.set_source_rgb(0.45, 0.46, 0.50); ctx.fill()
    for x in range(100, 700, 120):
        ctx.move_to(x, 800); ctx.line_to(x - 30, 1000); st(ctx, (0.95, 0.95, 0.9), 5)
    u = sm((t - tPol + 0.2) / 1.4)
    if t > tPol - 0.2:
        draw_car(ctx, lerp(-520, 120, 1 - (1 - clamp((t - tPol + 0.2) / 1.4)) ** 3), 960, 0.78, t)
    ctx.restore()
    ctx.move_to(360, 330); ctx.line_to(360, 990); ctx.move_to(70, 640); ctx.line_to(650, 640); st(ctx, (0.97, 0.97, 0.97), 16)
    rrect(ctx, 720, 380, 230, 300, 8); fs(ctx, (0.98, 0.95, 0.7))
    for k in range(4):
        ctx.move_to(745, 440 + k * 55); ctx.line_to(925, 440 + k * 55); st(ctx, (0.6, 0.6, 0.6), 4)


def doorway(ctx, t, open_u, show_dale=True, dark=0.92):
    ctx.set_source_rgb(0.86, 0.80, 0.68); ctx.paint()
    ctx.rectangle(0, 1640, 1080, 400); ctx.set_source_rgb(0.72, 0.64, 0.52); ctx.fill()
    ctx.rectangle(300, 520, 480, 1130); fs(ctx, (0.50, 0.34, 0.20), 8)
    ctx.rectangle(330, 550, 420, 1090); ctx.set_source_rgb(0.98, 0.97, 0.92); ctx.fill()
    if show_dale and open_u > 0.05:
        glow(ctx, 540, 1100, 600, (1, 1, 0.95), 0.5)
        draw_char(ctx, DALE, dict(x=545, y=1265, s=1.5, legs=True, hat=True, dark=dark, mood="smirk", look=0), t)
        ctx.save(); ctx.set_operator(ADD)
        poly(ctx, [(330, 1640), (750, 1640), (1000, 1940), (100, 1940)]); ctx.set_source_rgba(1, 1, 0.9, 0.25 * open_u); ctx.fill(); ctx.restore()
    w = 420 * cos(open_u * 1.35)
    poly(ctx, [(330, 550), (330 + w, 550 + 40 * open_u), (330 + w, 1640 - 40 * open_u), (330, 1640)]); fs(ctx, (0.62, 0.43, 0.27), 6)
    if w > 60:
        ell(ctx, 330 + w - 40 * (w / 420), 1100, 12 * w / 420 + 3, 12); fs(ctx, (0.85, 0.75, 0.4), 3)
        rrect(ctx, 330 + w * 0.2, 640, w * 0.6, 300, 6); ctx.set_source_rgba(0, 0, 0, 0.08); ctx.fill()


def s7(ctx, t):
    lights_on = t > tPol + 0.6
    ph = (t * 2.4) % 1.0 < 0.5
    if t < t72 - 0.03:
        cx, cy, z = cam(KEYS7, t)
        ctx.save(); apply_cam(ctx, cx, cy, z)
        s7_window(ctx, t)
        maya = dict(x=830, y=1440, s=1.22, legs=True, mood="neutral", look=-1, lookY=-0.2, blink=blinking(t, 1))
        if t > tPol + 0.3: maya.update(mood="scared")
        maya["armL"] = ("ik", 15, -92, 1); maya["armR"] = ("ik", -8, -102, -1)
        draw_char(ctx, MAYA, maya, t)
        ctx.restore()
    elif t < tDale - 0.02:
        tt = t - t72
        z = 1.0 + 0.25 * sm(tt / (tDale - t72))
        ctx.save(); ctx.translate(540, 960); ctx.scale(z, z); ctx.translate(-540, -1000)
        doorway(ctx, t, ramp(tt, 0.25, 1.6))
        ctx.restore()
    elif t < tEnd + 2.6:
        tt = t - tDale
        z = 1.0 + 0.08 * sm(tt / 2)
        ctx.save(); ctx.translate(540, 960); ctx.scale(z, z); ctx.translate(-540, 960)
        ctx.translate(0, -1920)
        g = cairo.RadialGradient(540, 900, 50, 540, 900, 900); g.add_color_stop_rgb(0, 1, 1, 0.95); g.add_color_stop_rgb(1, 0.75, 0.70, 0.62)
        ctx.set_source(g); ctx.paint()
        ctx.rectangle(-20, 0, 190, 1920); fs(ctx, (0.50, 0.34, 0.20), 8)
        ctx.rectangle(910, 0, 190, 1920); fs(ctx, (0.50, 0.34, 0.20), 8)
        draw_char(ctx, DALE, dict(x=540, y=1960, s=2.6, hat=True, mood="smirk", look=0, lookY=0, glint=True, shadow=0.15,
                                  blink=blinking(t, 2)), t)
        ctx.restore()
        fl = 1 - ramp(tt, 0.0, 0.45)
        overlay(ctx, (1, 0.25, 0.2), 0.75 * fl, ADD)
    if lights_on and t < tDale - 0.02:
        overlay(ctx, (0.6, 0.0, 0.05) if ph else (0.0, 0.08, 0.55), 0.13, ADD)
    elif t >= tDale - 0.02:
        overlay(ctx, (0.45, 0.0, 0.05) if ph else (0.0, 0.06, 0.4), 0.10, ADD)
    vignette(ctx, 0.5)
    if t >= tEnd:
        u = ramp(t, tEnd, tEnd + 0.3)
        overlay(ctx, (0.02, 0.02, 0.05), 0.8 * u)
        p = back_out((t - tEnd - 0.1) / 0.35)
        if t > tEnd + 0.1:
            ctx.save(); ctx.translate(540, 880); ctx.scale(p, p)
            rrect(ctx, -270, -130, 540, 190, 30); ctx.set_source_rgb(0.9, 0.12, 0.15); ctx.fill()
            text(ctx, "PART 2", 0, 18, 150, col=(1, 1, 1))
            ctx.restore()
        q = ramp(t, tEnd + 0.45, tEnd + 0.75)
        if q > 0:
            ctx.save(); ctx.translate(540, 1110); s_ = 0.9 + 0.1 * q + 0.03 * sin(t * 6); ctx.scale(s_, s_)
            text(ctx, "FOLLOW so you don't miss it", 0, 0, 56, col=(1, 1, 1), stroke=10)
            ctx.restore()
        r = ramp(t, tEnd + 0.9, tEnd + 1.2)
        if r > 0:
            text(ctx, "Would YOU have told someone?", 540, 1250, 50, col=(1, 0.86, 0.15), stroke=10)


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6, "s7": s7}
HL = {"N": (1, 0.86, 0.15), "D": (1, 0.33, 0.30), "A": (0.45, 0.95, 0.62)}


def chunks(words):
    out, cur = [], []
    for w in words:
        cur.append(w)
        txt = " ".join(x[0] for x in cur)
        if len(cur) >= 3 or len(txt) > 13 or w[0][-1] in ".,?!":
            out.append(cur); cur = []
    if cur: out.append(cur)
    return out


def captions(ctx, sc, t):
    for l in TL[sc]["lines"]:
        ws = l["words"]
        end = l["start"] + l["dur"] + 0.15
        if t < ws[0][1] - 0.06 or t > end: continue
        ch = chunks(ws)
        cur = ch[0]
        for c in ch:
            if t >= c[0][1] - 0.06: cur = c
        ctx.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        fsz = 88
        ctx.set_font_size(fsz)
        words = [w[0].upper() for w in cur]
        sp = ctx.text_extents(" ").x_advance
        widths = [ctx.text_extents(w).x_advance for w in words]
        tot = sum(widths) + sp * (len(words) - 1)
        k = min(1.0, 960 / tot)
        p = back_out((t - cur[0][1] + 0.06) / 0.14)
        sc_ = k * (0.8 + 0.2 * p)
        ctx.save(); ctx.translate(540, 1255); ctx.scale(sc_, sc_)
        x = -tot / 2
        active = None
        for i, w in enumerate(cur):
            if t >= w[1] - 0.03: active = i
        for i, w in enumerate(words):
            ctx.new_path(); ctx.move_to(x, 6); ctx.text_path(w); ctx.set_source_rgba(0, 0, 0, 0.45); ctx.fill()
            ctx.new_path(); ctx.move_to(x, 0); ctx.text_path(w)
            ctx.set_source_rgb(0, 0, 0); ctx.set_line_width(15); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
            ctx.set_source_rgb(*(HL[l["spk"]] if i == active else (1, 1, 1))); ctx.fill()
            x += widths[i] + sp
        ctx.restore()


HEADER = ["MY STEPDAD IS A COP", "PART 1"]


def header(ctx):
    ctx.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(38)
    a, b = HEADER
    wa, wb = ctx.text_extents(a).x_advance, ctx.text_extents(b).x_advance
    tot = wa + 44 + wb + 44 + 14
    x0 = 540 - tot / 2; y = 190
    rrect(ctx, x0, y - 40, wa + 44, 62, 31); ctx.set_source_rgba(0, 0, 0, 0.55); ctx.fill()
    rrect(ctx, x0 + wa + 58, y - 40, wb + 44, 62, 31); ctx.set_source_rgb(0.9, 0.12, 0.15); ctx.fill()
    ctx.new_path(); ctx.move_to(x0 + 22, y + 3); ctx.text_path(a); ctx.set_source_rgb(1, 1, 1); ctx.fill()
    ctx.new_path(); ctx.move_to(x0 + wa + 80, y + 3); ctx.text_path(b); ctx.set_source_rgb(1, 1, 1); ctx.fill()


def frame(surf, sc, t):
    ctx = cairo.Context(surf)
    ctx.set_source_rgb(0, 0, 0); ctx.paint()
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    SCENES[sc](ctx, t)
    ctx.set_operator(cairo.OPERATOR_OVER)
    captions(ctx, sc, t)
    header(ctx)
    if sc != "s1":
        a = 1 - clamp(t / 0.12)
        if a > 0: overlay(ctx, (0, 0, 0), a)


def render(sc):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    n = TL[sc]["frames"]
    tmp = f"{HERE}/scenes/{sc}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                          "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(n):
        frame(surf, sc, i / FPS); surf.flush()
        p.stdin.write(bytes(surf.get_data()))
    p.stdin.close()
    if p.wait() == 0:
        os.replace(tmp, f"{HERE}/scenes/{sc}.mp4")
        print("done", sc, n)
    else:
        print("FAILED", sc)


if __name__ == "__main__":
    os.makedirs(f"{HERE}/scenes", exist_ok=True); os.makedirs(f"{HERE}/preview", exist_ok=True)
    if sys.argv[1] == "preview":
        sc = sys.argv[2]
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        for ts in sys.argv[3:]:
            frame(surf, sc, float(ts)); surf.write_to_png(f"{HERE}/preview/{sc}_{ts}.png")
    else:
        for sc in (sys.argv[2:] or SCENES.keys()):
            render(sc)
