"""My Stepdad Is a Cop — Part 1 (2-minute cut). python part1v2.py preview <scene> t... | render [scenes]"""
import cairo, json, os, sys, subprocess, random
from math import sin, cos, pi
from rig import *
import part1 as P1
from part1 import MAYA, DALE, MOM, ALV, MAYA_W, MOM_W, ik

HERE = os.path.dirname(os.path.abspath(__file__))
EP = f"{HERE}/p1v2"
TL = {s["id"]: s for s in json.load(open(f"{EP}/timeline.json"))}
ADD = cairo.OPERATOR_ADD
MT = mood_at


def L(sc, i): return TL[sc]["lines"][i]
def LS(sc, i): return TL[sc]["lines"][i]["start"]
def LE(sc, i): l = TL[sc]["lines"][i]; return l["start"] + l["dur"]
def Wd(sc, i, j): return TL[sc]["lines"][i]["words"][j][1]
def DUR(sc): return TL[sc]["dur"]


def talk(sc, spk, t, li=None):
    for k, l in enumerate(TL[sc]["lines"]):
        if l["spk"] == spk and (li is None or k == li) and l["start"] <= t < l["start"] + l["dur"]:
            i = int((t - l["start"]) * FPS); e = l["env"]; i = min(i, len(e) - 1)
            return (e[i] + e[max(0, i - 1)]) / 2
    return 0.0


def flash(ctx, t, t0, col=(1, 1, 1), dur=0.18, a=0.8):
    if t0 <= t < t0 + dur: overlay(ctx, col, a * (1 - (t - t0) / dur), ADD)


def name_tag(ctx, t, t0, t1, name, role, y=1345):
    if t < t0 or t > t1 + 0.35: return
    u = back_out((t - t0) / 0.35); o = 1 - ramp(t, t1, t1 + 0.35)
    ctx.save(); ctx.push_group()
    ctx.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(50); w1 = ctx.text_extents(name).x_advance
    ctx.set_font_size(30); w2 = ctx.text_extents(role).x_advance
    w = max(w1, w2) + 70; x = lerp(-w - 20, 60, u)
    rrect(ctx, x, y, w, 118, 18); ctx.set_source_rgba(0.06, 0.06, 0.10, 0.88); ctx.fill()
    rrect(ctx, x, y, 14, 118, 7); ctx.set_source_rgb(0.9, 0.12, 0.15); ctx.fill()
    text(ctx, name, x + 34, y + 56, 50, align="l")
    text(ctx, role, x + 34, y + 100, 30, col=(1, 0.86, 0.15), align="l")
    ctx.pop_group_to_source(); ctx.paint_with_alpha(o); ctx.restore()


RAIN = [(random.Random(i).uniform(0, 1200), random.Random(i + 500).uniform(0, 1920), random.Random(i + 900).uniform(0.7, 1.3)) for i in range(140)]


def rain(ctx, t, a=0.35):
    ctx.set_line_width(3)
    for x0, y0, sp in RAIN:
        y = (y0 + t * 1900 * sp) % 2000 - 40; x = (x0 - t * 260 * sp) % 1200 - 60
        ctx.move_to(x, y); ctx.line_to(x - 9, y + 46 * sp); ctx.set_source_rgba(0.8, 0.85, 1, a); ctx.stroke()


# ============ A: hook ============
def a(ctx, t):
    t2 = LS("a", 1)
    keys = [(0, 540, 960, 1.0), (t2 - 0.03, 600, 990, 1.2), (t2, 655, 930, 2.05, "cut"), (DUR("a"), 655, 920, 2.35)]
    cx, cy, z = cam(keys, t); second = t >= t2
    ctx.save(); apply_cam(ctx, cx, cy, z)
    P1.house_night(ctx, t)
    red = draw_car(ctx, -10, 1470, 0.95, t)
    dale = dict(x=655, y=1444, s=1.6, legs=True, hat=True, look=0.25, blink=blinking(t, 2),
                mood=MT([(0, "happy"), (t2, "cold")], t))
    if not second: dale["armR"] = ("ang", 2.35, 2.95 + 0.38 * sin(t * 10))
    else: dale.update(look=0.0, shadow=0.55 * ramp(t, t2, t2 + 0.6), glint=True, saccade=False)
    draw_char(ctx, DALE, dale, t)
    glow(ctx, 210, 1290, 750, (1, 0.1, 0.1) if red else (0.15, 0.3, 1), 0.42 if second else 0.32)
    ctx.restore()
    if second:
        overlay(ctx, (0.02, 0.02, 0.06), 0.28); overlay(ctx, (0.5, 0.0, 0.05) if red else (0.0, 0.05, 0.4), 0.10, ADD)
    vignette(ctx, 0.65 if second else 0.45)
    name_tag(ctx, t, 0.55, t2 - 0.25, "DALE", "my stepdad · police officer")


# ============ B: Maya intro (bedroom, day) ============
def bedroom(ctx, t, night=0.0, dawn=0.0):
    ctx.set_source_rgb(*mix(mix((0.80, 0.74, 0.92), (0.16, 0.15, 0.30), night), (0.55, 0.42, 0.45), dawn * night)); ctx.paint()
    ctx.rectangle(0, 1500, 1080, 500); ctx.set_source_rgb(*mix((0.62, 0.48, 0.38), (0.12, 0.10, 0.14), night)); ctx.fill()
    sky = mix(mix((0.70, 0.88, 1.0), (0.06, 0.08, 0.22), night), (1.0, 0.62, 0.40), dawn)
    ctx.rectangle(80, 360, 320, 460); fs(ctx, sky)
    if night > 0.5 and dawn < 0.5:
        ell(ctx, 300, 450, 34, 34); ctx.set_source_rgba(0.95, 0.94, 0.85, 1 - dawn * 2); ctx.fill()
    if dawn > 0:
        glow(ctx, 240, 820, 300, (1, 0.7, 0.4), 0.7 * dawn)
    ctx.move_to(240, 360); ctx.line_to(240, 820); ctx.move_to(80, 590); ctx.line_to(400, 590); st(ctx, (0.95, 0.95, 0.95), 10)
    for x0, sx in ((60, 1), (420, -1)):
        ctx.move_to(x0, 330); ctx.curve_to(x0 + sx * 60, 500, x0 + sx * 20, 700, x0 + sx * 50, 860); ctx.line_to(x0, 860); ctx.close_path()
        fs(ctx, mix((0.95, 0.6, 0.72), (0.3, 0.2, 0.3), night))
    rrect(ctx, 600, 380, 200, 260, 6); fs(ctx, mix((0.15, 0.2, 0.45), (0.08, 0.08, 0.18), night))
    star(ctx, 700, 500, 60); ctx.set_source_rgb(*mix((1, 0.85, 0.2), (0.4, 0.35, 0.2), night)); ctx.fill()
    rrect(ctx, 840, 420, 170, 200, 6); fs(ctx, mix((0.98, 0.5, 0.45), (0.3, 0.15, 0.2), night))
    ell(ctx, 905, 560, 26, 20); ctx.set_source_rgb(0.1, 0.1, 0.15); ctx.fill()
    ctx.move_to(928, 556); ctx.line_to(928, 470); ctx.line_to(965, 485); st(ctx, (0.1, 0.1, 0.15), 8)
    pts = [(x, 260 + 50 * sin(pi * x / 1080)) for x in range(0, 1081, 60)]
    ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    st(ctx, (0.3, 0.25, 0.3), 3)
    for i, (x, y) in enumerate(pts):
        aa = 0.6 + 0.4 * sin(t * 3 + i)
        glow(ctx, x, y + 12, 40, (1, 0.8, 0.45), (0.25 + 0.5 * night) * aa)
        ell(ctx, x, y + 12, 7, 9); ctx.set_source_rgba(1, 0.9, 0.6, 0.6 + 0.4 * aa); ctx.fill()
    ctx.rectangle(640, 760, 330, 16); fs(ctx, (0.55, 0.38, 0.24), 3)
    blob(ctx, [(700, 715, 34), (676, 685, 14), (724, 685, 14)], mix((0.72, 0.5, 0.32), (0.25, 0.2, 0.18), night))
    for k, c in enumerate([(0.8, 0.3, 0.3), (0.3, 0.5, 0.8), (0.9, 0.7, 0.3)]):
        ctx.rectangle(800 + k * 34, 690, 28, 70); fs(ctx, mix(c, (0.15, 0.15, 0.2), night), 3)


def b(ctx, t):
    cx, cy, z = cam([(0, 540, 960, 1.0), (DUR("b"), 560, 1000, 1.14)], t)
    ctx.save(); apply_cam(ctx, cx, cy, z)
    bedroom(ctx, t)
    maya = dict(x=560, y=1480, s=1.55, legs=True, blink=blinking(t, 1), armL=("ik", 15, -92, 1), armR=("ik", -8, -102, -1),
                mood=MT([(0, "neutral"), (Wd("b", 0, 6) - 0.1, "sad")], t), lookY=0.15 * ramp(t, 2.5, 3.0))
    draw_char(ctx, MAYA, maya, t)
    ctx.restore()
    vignette(ctx, 0.35)
    name_tag(ctx, t, 0.6, 2.5, "MAYA", "14 years old · that's me")


# ============ C: bills (kitchen, night) ============
def kitchen_night(ctx, t):
    ctx.set_source_rgb(0.20, 0.23, 0.35); ctx.paint()
    ctx.rectangle(0, 280, 1080, 250); fs(ctx, (0.26, 0.30, 0.42))
    for x in range(0, 1080, 216):
        ctx.rectangle(x + 10, 290, 196, 230); st(ctx, OUTL, 4)
        rrect(ctx, x + 98, 490, 20, 8, 3); ctx.set_source_rgb(0.75, 0.75, 0.8); ctx.fill()
    ctx.rectangle(400, 600, 300, 280); fs(ctx, (0.06, 0.08, 0.20))
    ell(ctx, 620, 680, 26, 26); ctx.set_source_rgb(0.92, 0.92, 0.82); ctx.fill()
    ctx.move_to(550, 600); ctx.line_to(550, 880); ctx.move_to(400, 740); ctx.line_to(700, 740); st(ctx, (0.75, 0.75, 0.8), 9)
    rrect(ctx, 20, 560, 230, 900, 16); fs(ctx, (0.62, 0.65, 0.70))
    ctx.move_to(30, 900); ctx.line_to(240, 900); st(ctx, OUTL, 4)
    rrect(ctx, 210, 640, 14, 120, 6); fs(ctx, (0.45, 0.45, 0.5), 3)
    # torn family photo on the fridge
    poly(ctx, [(55, 640), (190, 640), (176, 700), (196, 760), (178, 805), (55, 805)]); fs(ctx, (1, 1, 1), 4)
    ctx.rectangle(68, 652, 100, 140); ctx.set_source_rgb(0.75, 0.85, 0.95); ctx.fill()
    for x, c, yy in [(95, MOM["hair"], 700), (135, MAYA["hair"], 720)]:
        ell(ctx, x, yy, 14, 14); ctx.set_source_rgb(*c); ctx.fill()
        rrect(ctx, x - 14, yy + 14, 28, 50, 8); ctx.fill()
    ell(ctx, 120, 650, 10, 10); ctx.set_source_rgb(0.9, 0.2, 0.2); ctx.fill()


def c(ctx, t):
    t2 = LS("c", 1)
    keys = [(0, 125, 740, 2.4), (1.4, 125, 735, 2.5), (2.9, 540, 960, 1.0), (t2 - 0.04, 540, 990, 1.08),
            (t2 - 0.02, 430, 1010, 1.95, "cut"), (DUR("c"), 430, 1010, 2.1)]
    cx, cy, z = cam(keys, t)
    ctx.save(); apply_cam(ctx, cx, cy, z)
    kitchen_night(ctx, t)
    P1.lamp(ctx, t * 0.5, 0.7)
    maya = dict(x=985, y=1480, s=1.2, mood="worried", look=-1, lookY=0.2, blink=blinking(t, 1))
    draw_char(ctx, MAYA, maya, t)
    ctx.rectangle(1035, 400, 60, 1200); fs(ctx, (0.17, 0.20, 0.31))
    ctx.rectangle(1020, 400, 20, 1200); fs(ctx, (0.45, 0.32, 0.22))
    mom = dict(x=430, y=1470, s=1.35, blink=blinking(t, 3), tilt=-0.12, look=0.1, lookY=0.9,
               mood=MT([(0, "sad"), (t2 + 1.2, "crying")], t),
               armL=("ang", -0.25, 2.55), armR=("ik", 70, -62, -1))
    draw_char(ctx, MOM, mom, t)
    ctx.rectangle(-10, 1390, 1100, 60); fs(ctx, (0.45, 0.32, 0.24))
    ctx.rectangle(-10, 1445, 1100, 500); fs(ctx, (0.36, 0.25, 0.19))
    for i, (x, y, r) in enumerate([(470, 1380, -0.15), (560, 1392, 0.12), (640, 1375, 0.3)]):
        ctx.save(); ctx.translate(x, y); ctx.rotate(r)
        ctx.rectangle(-55, -24, 110, 40); fs(ctx, (0.97, 0.97, 0.94), 3)
        if i != 1: text(ctx, "PAST DUE", 0, 4, 18, col=(0.85, 0.1, 0.1))
        else:
            for k in range(3):
                ctx.move_to(-40, -12 + k * 10); ctx.line_to(40, -12 + k * 10); st(ctx, (0.6, 0.6, 0.65), 3)
        ctx.restore()
    rrect(ctx, 250, 1360, 70, 40, 6); fs(ctx, (0.3, 0.3, 0.35), 3)
    ctx.restore()
    overlay(ctx, (0.0, 0.03, 0.12), 0.15)
    vignette(ctx, 0.55)


# ============ D: highway in the rain ============
def small_car(ctx, x, y, s, t):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    body = (0.78, 0.18, 0.18)
    poly(ctx, [(60, -110), (110, -185), (300, -185), (350, -110)]); fs(ctx, body)
    poly(ctx, [(85, -115), (122, -172), (200, -172), (200, -115)]); fs(ctx, (0.15, 0.2, 0.3), 4)
    poly(ctx, [(212, -115), (212, -172), (292, -172), (330, -115)]); fs(ctx, (0.15, 0.2, 0.3), 4)
    ctx.save(); ctx.rectangle(212, -172, 120, 57); ctx.clip()  # Maya in the back seat
    ell(ctx, 260, -128, 22, 22); ctx.set_source_rgb(*MAYA["skin"]); ctx.fill()
    blob(ctx, [(250, -150, 18), (272, -150, 18), (240, -128, 14), (282, -128, 14)], MAYA["hair"])
    ctx.restore()
    rrect(ctx, -10, -125, 440, 90, 28); fs(ctx, body)
    ctx.save(); ctx.translate(415, -122); ctx.rotate(-0.9)   # open hood
    rrect(ctx, 0, -8, 110, 16, 6); fs(ctx, shade(body, 0.1)); ctx.restore()
    blink_on = (t % 0.8) < 0.4
    for hx_ in (-4, 424):
        ell(ctx, hx_, -95, 12, 14); fs(ctx, (1, 0.6, 0.1) if blink_on else (0.5, 0.3, 0.1), 3)
        if blink_on: glow(ctx, hx_, -95, 120, (1, 0.55, 0.1), 0.6)
    for wx in (85, 345):
        ell(ctx, wx, -30, 40, 40); fs(ctx, (0.04, 0.04, 0.05)); ell(ctx, wx, -30, 17, 17); fs(ctx, (0.6, 0.6, 0.65), 3)
    for k in range(5):  # steam
        p = ((t * 0.5 + k * 0.2) % 1.0)
        ell(ctx, 440 + 30 * sin(k * 2 + t), -150 - p * 220, 30 + p * 40, 26 + p * 30); ctx.set_source_rgba(0.85, 0.88, 0.95, 0.35 * (1 - p)); ctx.fill()
    ctx.restore()


def highway(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, 980); g.add_color_stop_rgb(0, 0.04, 0.05, 0.10); g.add_color_stop_rgb(1, 0.15, 0.16, 0.25)
    ctx.set_source(g); ctx.paint()
    for i in range(40):
        x = (i * 97) % 1080; ell(ctx, x, 960 - (i * 13) % 40, 3, 3); ctx.set_source_rgba(1, 0.85, 0.5, 0.6); ctx.fill()
    poly(ctx, [(-200, 1920), (1280, 1920), (600, 980), (480, 980)]); ctx.set_source_rgb(0.11, 0.11, 0.14); ctx.fill()
    ctx.rectangle(-10, 980, 1100, 20); ctx.set_source_rgb(0.08, 0.1, 0.1); ctx.fill()
    poly(ctx, [(0, 1000), (480, 980), (-200, 1920), (-10, 1920)]); ctx.set_source_rgb(0.07, 0.10, 0.08); ctx.fill()
    for k in range(6):
        u = k / 6; y0 = lerp(1000, 1920, u * u); y1 = lerp(1000, 1920, (u + 0.08) ** 2)
        poly(ctx, [(540 - 4 - 30 * u * u, y0), (540 + 4 + 30 * u * u, y0), (540 + 6 + 36 * (u + 0.08) ** 2, y1), (540 - 6 - 36 * (u + 0.08) ** 2, y1)])
        ctx.set_source_rgba(0.9, 0.85, 0.5, 0.7); ctx.fill()
    ctx.move_to(610, 990); ctx.line_to(1100, 1500); st(ctx, (0.55, 0.55, 0.6), 8)
    for k in range(7):
        u = k / 7; x = lerp(620, 1080, u); y = lerp(1000, 1480, u)
        ctx.move_to(x, y); ctx.line_to(x, y + 30 + 60 * u); st(ctx, (0.45, 0.45, 0.5), 5 + 6 * u)


def d(ctx, t):
    tP = Wd("d", 0, 13); tD = LS("d", 1)
    lights = t > tP + 0.4; ph = (t * 2.4) % 1 < 0.5
    if t < tD - 0.1:
        cx, cy, z = cam([(0, 540, 960, 1.0), (tD - 0.1, 560, 1010, 1.12)], t)
        ctx.save(); apply_cam(ctx, cx, cy, z)
        highway(ctx, t)
        small_car(ctx, 470, 1520, 1.15, t)
        if t > tP - 0.1:
            xx = lerp(-700, -120, 1 - (1 - clamp((t - tP + 0.1) / 1.2)) ** 3)
            draw_car(ctx, xx, 1560, 1.0, t)
        mom = dict(x=330, y=1470, s=1.25, legs=True, blink=blinking(t, 3), look=-0.5 if t > tP else 0.4,
                   mood=MT([(0, "worried"), (tP + 0.5, "hopeful")], t), armL=("ik", -70, -440, 1), armR=("ik", 70, -440, -1))
        draw_char(ctx, MOM, mom, t)
        rrect(ctx, 330 - 150, 1470 - 340 * 1.25 - 200, 300, 70, 30); fs(ctx, (0.45, 0.30, 0.18))
        ctx.restore()
    else:
        tt = t - tD
        z = 1.0 + 0.08 * sm(tt / 3)
        ctx.save(); ctx.translate(540, 960); ctx.scale(z, z); ctx.translate(-540, -960)
        highway(ctx, t + 3)
        glow(ctx, 120, 1100, 600, (1, 0.1, 0.1) if ph else (0.15, 0.3, 1), 0.5)
        dale = dict(x=410, y=1500, s=1.65, hat=True, mouth=talk("d", "D", t), blink=blinking(t, 2), look=0.6,
                    mood=MT([(0, "happy")], t), armR=("ik", 150, -150, -1), armL=("ang", -0.14, -0.05))
        draw_char(ctx, DALE, dale, t)
        hx_, hy_ = 410 + 150 * 1.65, 1500 - 150 * 1.65
        rrect(ctx, hx_ - 10, hy_ - 22, 70, 30, 8); fs(ctx, (0.15, 0.15, 0.18), 3)
        ctx.save(); ctx.set_operator(ADD)
        g = cairo.LinearGradient(hx_, hy_, 1080, hy_ + 300); g.add_color_stop_rgba(0, 1, 1, 0.85, 0.45); g.add_color_stop_rgba(1, 1, 1, 0.85, 0)
        poly(ctx, [(hx_ + 60, hy_ - 20), (1200, hy_ - 220), (1200, hy_ + 520), (hx_ + 60, hy_ + 8)]); ctx.set_source(g); ctx.fill(); ctx.restore()
        mom = dict(x=880, y=1520, s=1.3, blink=blinking(t, 3), look=-1, mood=MT([(0, "worried"), (tt + tD - tt + 0.8, "hopeful")], t),
                   armL=("ik", -70, -440, 1), armR=("ik", 70, -440, -1))
        draw_char(ctx, MOM, mom, t)
        rrect(ctx, 880 - 156, 1520 - 340 * 1.3 - 210, 312, 72, 30); fs(ctx, (0.45, 0.30, 0.18))
        ctx.restore()
        name_tag(ctx, t, tD + 0.25, DUR("d") - 0.2, "OFFICER DALE BROOKS", "the man who stopped to help")
    if lights:
        overlay(ctx, (0.5, 0.0, 0.05) if ph else (0.0, 0.05, 0.45), 0.10, ADD)
    rain(ctx, t)
    overlay(ctx, (0.0, 0.03, 0.12), 0.18)
    vignette(ctx, 0.55)


# ============ E: montage of good times ============
def kitchen_day(ctx, t):
    ctx.set_source_rgb(0.99, 0.92, 0.74); ctx.paint()
    for x in range(0, 1080, 90):
        ctx.rectangle(x, 1050, 45, 400); ctx.set_source_rgba(1, 1, 1, 0.25); ctx.fill()
    ctx.rectangle(0, 280, 1080, 250); fs(ctx, (0.62, 0.82, 0.88))
    for x in range(0, 1080, 216):
        ctx.rectangle(x + 10, 290, 196, 230); st(ctx, OUTL, 4)
        rrect(ctx, x + 98, 490, 20, 8, 3); ctx.set_source_rgb(0.95, 0.95, 0.95); ctx.fill()
    ctx.rectangle(380, 600, 320, 300); fs(ctx, (0.75, 0.92, 1.0))
    glow(ctx, 540, 720, 300, (1, 1, 0.85), 0.6)
    ctx.move_to(540, 600); ctx.line_to(540, 900); ctx.move_to(380, 750); ctx.line_to(700, 750); st(ctx, (1, 1, 1), 10)
    for k, x in enumerate((430, 470, 650)):
        ell(ctx, x, 905, 22, 18); fs(ctx, (0.85, 0.5, 0.35), 3)
        ell(ctx, x, 880, 14 + 4 * k % 2, 22); fs(ctx, (0.35, 0.65, 0.35), 3)


def sparkle(ctx, x, y, t, ph=0, r=28):
    k = (sin(t * 6 + ph) + 1) / 2
    star(ctx, x, y, r * (0.4 + 0.6 * k), n=4, inner=0.25); ctx.set_source_rgba(1, 1, 0.8, 0.5 + 0.5 * k); ctx.fill()


def bike(ctx, x, y, t, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for wx in (-150, 150):
        ell(ctx, wx, 0, 92, 92); st(ctx, OUTL, 12)
        for k in range(6):
            a = t * 9 + k * pi / 3
            ctx.move_to(wx, 0); ctx.line_to(wx + 85 * cos(a), 85 * sin(a)); st(ctx, (0.6, 0.6, 0.65), 3)
    ctx.move_to(-150, 0); ctx.line_to(-30, -130); ctx.line_to(110, -130); ctx.line_to(150, 0)
    ctx.move_to(-30, -130); ctx.line_to(10, 0); ctx.line_to(-150, 0); ctx.move_to(10, 0); ctx.line_to(110, -130)
    st(ctx, OUTL, 18); ctx.move_to(-150, 0); ctx.line_to(-30, -130); ctx.line_to(110, -130); ctx.line_to(150, 0)
    ctx.move_to(-30, -130); ctx.line_to(10, 0); ctx.line_to(-150, 0); ctx.move_to(10, 0); ctx.line_to(110, -130)
    st(ctx, (0.95, 0.35, 0.55), 11)
    ctx.move_to(110, -130); ctx.line_to(100, -200); st(ctx, OUTL, 10)
    ctx.move_to(70, -210); ctx.line_to(140, -200); st(ctx, OUTL, 12)
    rrect(ctx, -75, -160, 80, 22, 10); fs(ctx, (0.2, 0.2, 0.22))
    ctx.restore()


def stage_bg(ctx, t):
    ctx.set_source_rgb(0.08, 0.06, 0.10); ctx.paint()
    ctx.rectangle(0, 300, 1080, 760); ctx.set_source_rgb(0.20, 0.10, 0.16); ctx.fill()
    for sx, x0 in ((1, 0), (-1, 1080)):
        ctx.move_to(x0, 260); ctx.curve_to(x0 + sx * 260, 300, x0 + sx * 150, 800, x0 + sx * 230, 1060); ctx.line_to(x0, 1060); ctx.close_path()
        fs(ctx, (0.72, 0.10, 0.14))
        for k in range(4):
            ctx.move_to(x0 + sx * (40 + k * 40), 300); ctx.curve_to(x0 + sx * (60 + k * 40), 600, x0 + sx * (30 + k * 45), 800, x0 + sx * (50 + k * 45), 1050)
            st(ctx, (0.5, 0.05, 0.08), 4)
    ctx.rectangle(0, 240, 1080, 90); fs(ctx, (0.72, 0.10, 0.14))
    ctx.rectangle(0, 1040, 1080, 70); fs(ctx, (0.45, 0.30, 0.18))
    ctx.save(); ctx.set_operator(ADD)
    g = cairo.LinearGradient(0, 240, 0, 1060); g.add_color_stop_rgba(0, 1, 0.95, 0.75, 0.05); g.add_color_stop_rgba(1, 1, 0.95, 0.75, 0.35)
    poly(ctx, [(500, 240), (580, 240), (760, 1060), (320, 1060)]); ctx.set_source(g); ctx.fill(); ctx.restore()
    ell(ctx, 540, 1050, 230, 30); ctx.set_source_rgba(1, 0.95, 0.75, 0.35); ctx.fill()


def living_room(ctx, t):
    ctx.set_source_rgb(0.96, 0.80, 0.62); ctx.paint()
    ctx.rectangle(0, 1450, 1080, 500); ctx.set_source_rgb(0.70, 0.52, 0.38); ctx.fill()
    rrect(ctx, 120, 420, 260, 190, 6); fs(ctx, (0.55, 0.40, 0.22))
    ctx.rectangle(138, 438, 224, 154); ctx.set_source_rgb(1.0, 0.85, 0.65); ctx.fill()
    ctx.new_path(); ctx.arc(250, 560, 60, pi, 2 * pi); st(ctx, (1, 1, 1), 8)
    ctx.rectangle(860, 600, 14, 500); fs(ctx, (0.3, 0.25, 0.2))
    poly(ctx, [(800, 520), (934, 520), (970, 620), (764, 620)]); fs(ctx, (1, 0.9, 0.7))
    glow(ctx, 867, 620, 300, (1, 0.85, 0.5), 0.5)
    rrect(ctx, 40, 1080, 1000, 420, 60); fs(ctx, (0.55, 0.28, 0.25))


def couch_front(ctx):
    rrect(ctx, -10, 1380, 1100, 600, 50); fs(ctx, (0.62, 0.32, 0.28))
    for x in (40, 380, 720):
        rrect(ctx, x, 1400, 330, 120, 40); fs(ctx, (0.68, 0.37, 0.32), 4)


def e(ctx, t):
    t1, tPan, t2, t3 = LS("e", 1), Wd("e", 1, 7), LS("e", 2), LS("e", 3)
    if t < t1 - 0.05:   # fixing everything
        cx, cy, z = cam([(0, 540, 960, 1.0), (t1, 520, 1000, 1.1)], t)
        ctx.save(); apply_cam(ctx, cx, cy, z)
        kitchen_day(ctx, t)
        dale = dict(x=400, y=1500, s=1.5, mood="happy", blink=blinking(t, 2), look=0.4, armR=("ang", 2.6, 2.95 + 0.25 * sin(t * 5)))
        draw_char(ctx, DALE, dale, t)
        wx, wy = 400 + 1.5 * (82 + 105 * sin(2.6) + 100 * sin(2.95 + 0.25 * sin(t * 5))), 1500 + 1.5 * (-212 + 105 * cos(2.6) + 100 * cos(2.95 + 0.25 * sin(t * 5)))
        ctx.save(); ctx.translate(wx, wy); ctx.rotate(-0.6 + 0.25 * sin(t * 5))
        rrect(ctx, -10, -100, 20, 100, 8); fs(ctx, (0.7, 0.72, 0.78)); ctx.arc(0, -110, 26, 0, 2 * pi); fs(ctx, (0.7, 0.72, 0.78)); ctx.restore()
        mom = dict(x=840, y=1510, s=1.3, mood="happy", blink=blinking(t, 3), look=-1, armL=("ik", 30, -110, 1), armR=("ik", -30, -110, -1))
        draw_char(ctx, MOM, mom, t)
        ctx.rectangle(-10, 1330, 1100, 40); fs(ctx, (0.92, 0.92, 0.95)); ctx.rectangle(-10, 1365, 1100, 600); fs(ctx, (0.55, 0.75, 0.82))
        ell(ctx, 610, 1335, 120, 16); fs(ctx, (0.75, 0.78, 0.82))
        ctx.move_to(610, 1325); ctx.line_to(610, 1250); ctx.line_to(660, 1250); st(ctx, (0.65, 0.67, 0.72), 14)
        for k, (x, y) in enumerate([(560, 1230), (690, 1200), (630, 1160), (720, 1290)]): sparkle(ctx, x, y, t, k * 1.7)
        ctx.restore()
    elif t < tPan - 0.05:   # bike
        ctx.save()
        g = cairo.LinearGradient(0, 0, 0, 1250); g.add_color_stop_rgb(0, 0.55, 0.80, 0.98); g.add_color_stop_rgb(1, 0.85, 0.94, 1.0)
        ctx.set_source(g); ctx.paint()
        ell(ctx, 850, 350, 70, 70); ctx.set_source_rgb(1, 0.92, 0.5); ctx.fill(); glow(ctx, 850, 350, 200, (1, 0.95, 0.6), 0.5)
        off = (t * 320) % 400
        for i in range(-1, 5):
            x = i * 400 - off
            ctx.rectangle(x + 180, 950, 30, 300); fs(ctx, (0.5, 0.35, 0.22))
            blob(ctx, [(x + 195, 900, 110), (x + 120, 960, 80), (x + 270, 960, 80)], (0.35, 0.62, 0.32))
        ctx.rectangle(0, 1250, 1080, 700); ctx.set_source_rgb(0.48, 0.72, 0.38); ctx.fill()
        ctx.rectangle(0, 1560, 1080, 120); ctx.set_source_rgb(0.80, 0.78, 0.75); ctx.fill()
        for i in range(-1, 8):
            x = i * 180 - (t * 640) % 180
            ctx.move_to(x, 1560); ctx.line_to(x, 1680); st(ctx, (0.65, 0.63, 0.6), 4)
        bob = 4 * sin(t * 18)
        bike(ctx, 620, 1640, t, 1.0)
        maya = dict(x=600, y=1475 + bob, s=1.05, mood="joy", blink=False, look=0.5, armL=ik(dict(x=600, y=1475 + bob, s=1.05), 700, 1435, 1),
                    armR=ik(dict(x=600, y=1475 + bob, s=1.05), 760, 1440, -1))
        draw_char(ctx, MAYA, maya, t)
        dale = dict(x=300, y=1560 + 6 * abs(sin(t * 9)), s=1.35, legs=True, mood="happy", blink=blinking(t, 2), look=1)
        dale["armR"] = ik(dale, 560, 1490, -1)
        draw_char(ctx, DALE, dale, t)
        ctx.restore()
    elif t < t2 - 0.05:   # star pancakes
        ctx.save(); z = 1.0 + 0.06 * (t - tPan)
        ctx.translate(540, 960); ctx.scale(z, z); ctx.translate(-540, -960)
        kitchen_day(ctx, t)
        dale = dict(x=330, y=1480, s=1.45, mood="happy", blink=t % 2.5 < 0.25, look=0.8, armR=("ang", 1.9, 1.3))
        draw_char(ctx, DALE, dale, t)
        maya = dict(x=780, y=1480, s=1.25, mood="joy", look=-0.6)
        draw_char(ctx, MAYA, maya, t)
        ctx.rectangle(-10, 1380, 1100, 600); fs(ctx, (0.85, 0.62, 0.42))
        ell(ctx, 560, 1400, 150, 34); fs(ctx, (1, 1, 1), 4)
        for k in range(4):
            star(ctx, 560, 1380 - k * 26, 95 - k * 6, n=5, inner=0.62, rot=-pi / 2 + 0.1 * k)
            fs(ctx, (0.92, 0.66, 0.30) if k % 2 == 0 else (0.86, 0.58, 0.25), 4)
        rrect(ctx, 535, 1280, 50, 24, 6); fs(ctx, (1, 0.95, 0.6), 3)
        for k in range(3):
            p = (t * 0.6 + k * 0.33) % 1
            ell(ctx, 520 + k * 40, 1260 - p * 160, 10 + p * 18, 14 + p * 20); ctx.set_source_rgba(1, 1, 1, 0.45 * (1 - p)); ctx.fill()
        ctx.restore()
    elif t < t3 - 0.05:   # school play
        ctx.save()
        stage_bg(ctx, t)
        maya = dict(x=540, y=1035, s=0.95, legs=False, mood="happy", look=-0.5, lookY=0.6, blink=blinking(t, 1),
                    armL=("ang", -2.4, -2.9), armR=("ang", 2.4, 2.9))
        draw_char(ctx, MAYA, maya, t)
        star(ctx, 540, 1035 - 340 * 0.95 - 110, 46); fs(ctx, (1, 0.85, 0.2), 4)
        rrect(ctx, -10, 1060, 1100, 900, 0); ctx.set_source_rgb(0.06, 0.05, 0.08); ctx.fill()
        for row, (y, sc) in enumerate([(1620, 1.0), (1800, 1.2)]):
            for i in range(-1, 9):
                x = i * 140 + (70 if row else 0)
                if row == 0 and 250 < x < 420: continue
                ell(ctx, x, y, 55 * sc, 62 * sc); ctx.set_source_rgb(0.12, 0.10, 0.15); ctx.fill()
                rrect(ctx, x - 80 * sc, y + 50 * sc, 160 * sc, 200, 40); ctx.fill()
        clap = abs(sin(t * 13))
        dale = dict(x=330, y=1950, s=1.35, mood="joy", look=0.4, lookY=-0.6,
                    armL=("ik", -12 - 40 * clap, -205, 1), armR=("ik", 12 + 40 * clap, -205, -1))
        glow(ctx, 330, 1500, 330, (1, 0.9, 0.6), 0.25)
        draw_char(ctx, DALE, dale, t)
        ctx.restore()
    else:   # Mom laughing on the couch
        ctx.save(); z = 1.0 + 0.05 * (t - t3)
        ctx.translate(540, 960); ctx.scale(z, z); ctx.translate(-540, -960)
        living_room(ctx, t)
        bounce = 5 * abs(sin(t * 14))
        draw_char(ctx, DALE, dict(x=260, y=1470, s=1.4, mood="happy", look=0.8, blink=blinking(t, 2)), t)
        draw_char(ctx, MOM, dict(x=560, y=1470 - bounce, s=1.35, mood="joy", tilt=0.08 * sin(t * 7)), t)
        draw_char(ctx, MAYA, dict(x=850, y=1480, s=1.2, mood="happy", look=-0.9, blink=blinking(t, 1)), t)
        couch_front(ctx)
        ctx.restore()
    for tc in (t1, tPan, t2, t3):
        flash(ctx, t, tc - 0.05)
    overlay(ctx, (1, 0.85, 0.6), 0.09)
    vignette(ctx, 0.4, 420, 1150)


# ============ F: wedding ============
def f(ctx, t):
    tD, t3 = LS("f", 1), LS("f", 2)
    keys = [(0, 540, 960, 1.0), (tD - 0.03, 560, 1000, 1.14), (tD, 590, 1030, 1.48, "cut"), (t3 - 0.03, 595, 1030, 1.62),
            (t3, 805, 1030, 2.1, "cut"), (DUR("f"), 805, 1030, 2.25)]
    cx, cy, z = cam(keys, t)
    ctx.save(); apply_cam(ctx, cx, cy, z)
    P1.wedding_bg(ctx, t)
    mom = dict(x=540, y=1215, s=1.25, mood="happy", look=0.3, blink=blinking(t, 3))
    mom["armL"] = ik(mom, 520, 1100, 1); mom["armR"] = ik(mom, 560, 1100, -1)
    ell(ctx, 540, 830, 150, 240); ctx.set_source_rgba(1, 1, 1, 0.45); ctx.fill()
    draw_char(ctx, MOM_W, mom, t)
    for (dx, dy, cc) in [(-22, -10, (1, 1, 1)), (18, -14, (0.98, 0.7, 0.78)), (0, 8, (0.99, 0.82, 0.68)), (-30, 14, (0.98, 0.7, 0.78)), (28, 12, (1, 1, 1)), (0, -30, (0.85, 0.55, 0.7))]:
        ell(ctx, 540 + dx, 1100 + dy, 20, 19); fs(ctx, cc, 3.5)
    maya = dict(x=805, y=1445, s=1.2, look=-1, lookY=-0.2, blink=blinking(t, 1),
                mood=MT([(0, "happy"), (tD + 0.3, "hopeful"), (t3, dict(MOODS["hopeful"], smile=0.6, tear=0.5))], t))
    if t >= t3: maya.update(look=-0.2, lookY=0)
    dale = dict(x=380, y=1470, s=1.45, mood="happy", look=1, mouth=talk("f", "D", t), blink=blinking(t, 2))
    shx, shy = 805 - 82 * 1.2, 1445 - 212 * 1.2 + 8
    u = ramp(t, tD - 0.6, tD + 0.1)
    dale["armR"] = ik(dale, lerp(530, shx, u), lerp(1410, shy, u), 1)
    draw_char(ctx, MAYA_W, maya, t)
    draw_char(ctx, DALE, dale, t)
    for i, (x, y0, sp) in enumerate(P1.PETALS):
        y = (y0 + t * 120 * sp) % 1950 - 30; xx = x + 30 * sin(t * 1.5 * sp + i)
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


# ============ G: dinner ============
def mom_wrist_insert(ctx, t, tt):
    ctx.set_source_rgb(0.90, 0.86, 0.78); ctx.paint()
    for x in range(-200, 1300, 120):
        ctx.move_to(x, 0); ctx.line_to(x + 300, 1920); ctx.set_source_rgba(0, 0, 0, 0.04); ctx.set_line_width(40); ctx.stroke()
    z = 1.05 + 0.12 * sm(tt)
    ctx.save(); ctx.translate(540, 900); ctx.scale(z, z); ctx.translate(-540, -900)
    skin = MOM["skin"]
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(-200, 1250); ctx.line_to(420, 960); st(ctx, OUTL, 230 + 12); ctx.move_to(-200, 1250); ctx.line_to(420, 960); st(ctx, MOM["top"], 230)
    ctx.move_to(400, 970); ctx.line_to(760, 800); st(ctx, OUTL, 140 + 12); ctx.move_to(400, 970); ctx.line_to(760, 800); st(ctx, skin, 140)
    for k, (dx, dy) in enumerate([(-55, -38), (-12, -50), (32, -54), (74, -48)]):
        ell(ctx, 520 + dx, 905 + dy * 0.2 + 20, 18, 34, -0.45); ctx.set_source_rgba(0.45, 0.30, 0.55, 0.55); ctx.fill()
    ell(ctx, 470, 960, 20, 30, -0.4); ctx.set_source_rgba(0.45, 0.30, 0.55, 0.45); ctx.fill()
    ell(ctx, 790, 780, 120, 100, -0.4); fs(ctx, skin, 6)
    rrect(ctx, 760, 700, 230, 170, 20); fs(ctx, (1, 1, 1), 5)
    for k in range(3):   # bunched sleeve folds
        ctx.move_to(330 + k * 25, 900 + k * 4); ctx.curve_to(350 + k * 25, 960, 360 + k * 25, 1010, 380 + k * 25, 1060); st(ctx, shade(MOM["top"], 0.25), 4)
    ctx.restore()


def g(ctx, t):
    tk, tS, tC, t3, tSaw, t5, tDid = Wd("g", 0, 6), LS("g", 1) - 0.32, LS("g", 2), LS("g", 3), Wd("g", 3, 11), LS("g", 5), Wd("g", 5, 6)
    if tSaw + 0.15 <= t < t5 - 0.03:
        mom_wrist_insert(ctx, t, (t - tSaw) / (t5 - tSaw))
        vignette(ctx, 0.5); return
    keys = [(0, 540, 960, 1.0), (tk - 0.12, 540, 990, 1.07), (tk - 0.1, 770, 1180, 1.75, "cut"), (tS - 0.42, 770, 1180, 1.9),
            (tS - 0.4, 560, 1130, 1.5, "cut"), (tC - 0.07, 560, 1120, 1.6),
            (tC - 0.05, 540, 960, 2.45, "cut"), (t3 - 0.05, 540, 955, 2.7),
            (t3 - 0.03, 380, 1150, 1.55, "cut"), (tSaw + 0.13, 380, 1140, 1.65),
            (t5 - 0.03, 230, 1010, 2.15, "cut"), (tDid - 0.08, 230, 1010, 2.3), (tDid - 0.06, 860, 1050, 2.2, "cut"), (DUR("g"), 860, 1050, 2.32)]
    dim = ramp(t, tS - 0.3, tS) * 0.75
    cx, cy, z = cam(keys, t)
    shk = 14 * max(0, 1 - (t - tS) / 0.35) * sin(t * 80) if t >= tS else 0
    ctx.save(); apply_cam(ctx, cx + shk, cy, z)
    P1.dining_bg(ctx, t, dim * 0.6)
    jump = 14 * max(0, sin(min(1, (t - tS) / 0.22) * pi)) if t >= tS else 0
    mom = dict(x=200, y=1445, s=1.22, look=0.4, blink=blinking(t, 3) and t < tS,
               mood=MT([(0, "happy"), (tk + 0.1, "worried"), (tS, "scared"), (t3, "worried"), (t5, "sad")], t, 0.15))
    dale = dict(x=540, y=1455, s=1.45, look=0.2, lookY=0.5, blink=blinking(t, 2), mouth=talk("g", "D", t),
                mood=MT([(0, "happy"), (tk + 0.3, "cold"), (tS - 0.45, "angry"), (LE("g", 2) + 0.3, "cold")], t, 0.15))
    maya = dict(x=870, y=1445, s=1.18, look=-0.3, lookY=0.4, blink=blinking(t, 1),
                mood=MT([(0, "neutral"), (tk, "shock"), (tS, "scared"), (t3, "worried"), (tSaw, "shock"), (tDid - 0.06, "crying")], t, 0.15))
    if t >= tk: maya.update(look=-0.6, lookY=0.6, flinch=1 - ramp(t, tk, tk + 0.4)); mom.update(look=1, lookY=0.2)
    if t > tk + 0.35: dale.update(look=1, lookY=0.1)
    if t >= tS - 0.45:
        dale.update(look=0.8, lookY=0, glint=True, saccade=False)
        maya.update(look=-1, lookY=0, flinch=1 - ramp(t, tS, tS + 0.4)); mom.update(look=0.8, lookY=0.3, flinch=1 - ramp(t, tS, tS + 0.4))
    if t >= tC - 0.05: dale.update(look=0, shadow=0.45)
    if t >= t3: dale.update(lookY=0.4, look=0.6, shadow=0.3); maya.update(look=-1, lookY=0.2)
    if t >= t5: mom.update(look=0.2, lookY=1, saccade=False)
    mom["armR"] = ik(mom, 270, 1352, -1)
    up = ramp(t, t3, t3 + 0.35) * (1 - ramp(t, t5, t5 + 0.5))
    mom["y"] -= 50 * up
    mom["armR"] = ik(mom, lerp(270, 470, up), lerp(1352, 1345, up), -1)
    mom["armL"] = ik(mom, lerp(150, 230, ramp(t, t5, t5 + 0.6)), lerp(1352, 1300, ramp(t, t5, t5 + 0.6)), 1)
    dale["armL"] = ik(dale, 440, 1352 - jump, 1)
    raise_ = ramp(t, tS - 0.42, tS - 0.12) * (1 - ramp(t, tS - 0.1, tS))
    dale["armR"] = ("ang", lerp(0.3, 2.7, raise_), lerp(0.1, 3.0, raise_)) if raise_ > 0.01 and t < tS else ik(dale, 630, 1340 - jump, -1)
    jerk = ramp(t, tk - 0.15, tk + 0.02)
    maya["armL"] = ik(maya, lerp(800, 768, jerk), lerp(1350, 1330, jerk), 1); maya["armR"] = ik(maya, 950, 1352, -1)
    draw_char(ctx, MOM, mom, t); draw_char(ctx, DALE, dale, t); draw_char(ctx, MAYA, maya, t)
    if up > 0.2:
        hx_, hy_ = lerp(270, 470, up), 1345
        rrect(ctx, hx_ - 30, hy_ - 40, 70, 50, 8); fs(ctx, (1, 1, 1), 3)
    if t >= tS and t < tS + 0.25:
        star(ctx, 640, 1330, 90 * (1 - (t - tS) / 0.25) + 30, n=8, inner=0.45); ctx.set_source_rgba(1, 0.95, 0.6, 0.7); ctx.fill()
    ctx.rectangle(-10, 1335, 1100, 70); fs(ctx, mix((0.95, 0.92, 0.85), (0.4, 0.38, 0.38), dim * 0.5))
    ctx.rectangle(-10, 1400, 1100, 530); fs(ctx, mix((0.88, 0.84, 0.76), (0.35, 0.33, 0.33), dim * 0.5))
    for x in (200, 540, 870):
        jy = jump * (1.0 if x == 540 else 0.6)
        ell(ctx, x, 1366 - jy, 92, 22); fs(ctx, (0.98, 0.98, 0.98), 4)
        ell(ctx, x - 20, 1362 - jy, 34, 10); ctx.set_source_rgb(0.55, 0.32, 0.2); ctx.fill()
        for kk in range(5):
            ell(ctx, x + 25 + 7 * kk, 1366 - jy + 3 * sin(kk * 2), 6, 5); ctx.set_source_rgb(0.4, 0.7, 0.3); ctx.fill()
    if t >= tk:
        pu = ramp(t, tk + 0.12, tk + 0.9)
        ell(ctx, 690, 1368, 125 * pu, 20 * pu); ctx.set_source_rgba(0.98, 0.62, 0.15, 0.9); ctx.fill()
        dr = ramp(t, tk + 0.5, tk + 2.2)
        if dr > 0:
            ctx.move_to(620, 1398); ctx.line_to(700, 1398); ctx.curve_to(700, 1398 + 120 * dr, 680, 1398 + 160 * dr, 662, 1398 + 170 * dr)
            ctx.curve_to(645, 1398 + 160 * dr, 650, 1398 + 60 * dr, 620, 1398); ctx.set_source_rgba(0.95, 0.6, 0.18, 0.75); ctx.fill()
    ang = -pi / 2 * ramp(t, tk + 0.02, tk + 0.22)
    ctx.save(); ctx.translate(741, 1347 - jump * 0.6); ctx.rotate(ang)
    full = 1 - ramp(t, tk + 0.1, tk + 0.6)
    ctx.rectangle(0, -64, 38, 64); ctx.set_source_rgba(0.85, 0.95, 1.0, 0.55); ctx.fill_preserve(); ctx.set_source_rgb(*OUTL); ctx.set_line_width(4); ctx.stroke()
    if full > 0.02: ctx.rectangle(3, -60 * full, 32, 58 * full); ctx.set_source_rgba(0.98, 0.62, 0.15, 0.95); ctx.fill()
    ctx.restore()
    P1.lamp(ctx, t, 1 - dim * 0.8)
    ctx.restore()
    if dim > 0: overlay(ctx, (0.02, 0.03, 0.10), 0.25 * dim)
    flash(ctx, t, tS, (1, 0.3, 0.25), 0.25, 0.45)
    vignette(ctx, 0.4 + 0.35 * dim)


# ============ H: hallway, grip, threats (intercut) ============
def dark_bg(ctx, beam=True):
    gg = cairo.LinearGradient(0, 0, 0, 1920); gg.add_color_stop_rgb(0, 0.04, 0.05, 0.12); gg.add_color_stop_rgb(1, 0.10, 0.08, 0.14)
    ctx.set_source(gg); ctx.paint()
    if beam: ctx.rectangle(860, 300, 120, 1200); ctx.set_source_rgba(1, 0.8, 0.45, 0.22); ctx.fill()


def dale_ecu(ctx, t, sc, tt, mood, glint_t=None):
    ctx.save(); z = 1.0 + 0.1 * sm(tt)
    ctx.translate(540, 960); ctx.scale(z, z); ctx.translate(-540, -980)
    dark_bg(ctx)
    draw_char(ctx, DALE, dict(x=540, y=1990, s=3.0, mood=mood, look=0, lookY=0.15, dark=0.22, shadow=0.62, glint=True,
                             mouth=talk(sc, "D", t), saccade=False, blink=blinking(t, 2)), t)
    ctx.save(); ctx.set_operator(ADD)
    gr = cairo.LinearGradient(1080, 0, 600, 0); gr.add_color_stop_rgba(0, 1, 0.75, 0.4, 0.25); gr.add_color_stop_rgba(1, 1, 0.75, 0.4, 0)
    ctx.rectangle(0, 0, 1080, 1920); ctx.set_source(gr); ctx.fill(); ctx.restore()
    if glint_t is not None:
        gl = ramp(t, glint_t - 0.05, glint_t + 0.12) * (1 - ramp(t, glint_t + 0.25, glint_t + 0.8))
        if gl > 0:
            bx, by = 540 + 46 * 3.0, 1990 - 180 * 3.0
            glow(ctx, bx, by, 160, (1, 0.9, 0.6), 0.8 * gl)
            star(ctx, bx, by, 90 * gl, n=4, inner=0.12); ctx.set_source_rgba(1, 1, 0.9, gl); ctx.fill()
    ctx.restore()


def maya_ecu(ctx, t, tt, mood, bg="dark", s=2.5, y=1820, look=0.0, lookY=0.0, dark=0.15):
    ctx.save(); z = 1.0 + 0.08 * sm(tt)
    ctx.translate(540, 960); ctx.scale(z, z); ctx.translate(-540, -960)
    if bg == "dark": dark_bg(ctx, beam=False)
    else: bg(ctx, t)
    draw_char(ctx, MAYA, dict(x=540, y=y, s=s, mood=mood, look=look, lookY=lookY, dark=dark, blink=blinking(t, 1) and mood not in ("crying",)), t)
    ctx.restore()


def h(ctx, t):
    t1, t2, tSo, tD1, tThen, tD2, tCop = LS("h", 1), LS("h", 2), Wd("h", 2, 4), LS("h", 3), Wd("h", 3, 8), LS("h", 4), Wd("h", 4, 11)
    P1.tNumb = Wd("h", 2, 9)
    if t < t1 - 0.03 or (t2 - 0.03 <= t < tSo - 0.05):
        cx, cy, z = cam([(0, 540, 960, 1.0), (t1, 520, 1040, 1.1), (t2 - 0.03, 560, 1100, 1.15, "cut"), (tSo, 540, 1120, 1.22)], t)
        ctx.save(); apply_cam(ctx, cx, cy, z)
        P1.hallway(ctx, t)
        grab = ramp(t, t2, t2 + 0.3)
        maya = dict(x=780, y=1560, s=1.25, legs=True, look=-1, lookY=-0.3, blink=blinking(t, 1),
                    mood=MT([(0, dict(MOODS["scared"], bi=-4, bo=4, mo=0, tremble=0.3)), (t2, "shock")], t), flinch=grab * (1 - ramp(t, t2 + 0.3, t2 + 0.8)))
        dx = lerp(-260, 290, sm(t / 1.4))
        dale = dict(x=dx, y=1600, s=1.85, legs=True, mood="cold", look=1, lookY=0.3, dark=0.62, shadow=0.5, glint=True)
        maya["armL"] = ik(maya, lerp(652, 612, grab), lerp(1550, 1440, grab), -1)
        dale["armR"] = ik(dale, lerp(dx + 160, 612, grab), lerp(1560, 1432, grab), 1)
        draw_char(ctx, MAYA, maya, t); draw_char(ctx, DALE, dale, t)
        ctx.restore()
        overlay(ctx, (0.0, 0.03, 0.15), 0.25)
    elif t < t2 - 0.03:
        cx, cy, z = cam([(t1, 760, 1120, 1.85), (t2, 760, 1110, 1.95)], t)
        ctx.save(); apply_cam(ctx, cx, cy, z)
        P1.hallway(ctx, t)
        draw_char(ctx, DALE, dict(x=290, y=1600, s=1.85, legs=True, mood="cold", look=1, lookY=0.3, dark=0.62, shadow=0.5), t)
        draw_char(ctx, MAYA, dict(x=780, y=1560, s=1.25, legs=True, look=-1, lookY=-0.4, mouth=talk("h", "M", t), blink=False,
                                  mood=dict(MOODS["scared"], bi=-2, bo=5, mo=0, tremble=0.5, tear=0.3)), t)
        ctx.restore()
        overlay(ctx, (0.0, 0.03, 0.15), 0.22)
    elif t < tD1 - 0.03:
        P1.grip_insert(ctx, t, (t - tSo) / (tD1 - tSo))
    elif t < tThen - 0.05:
        dale_ecu(ctx, t, "h", (t - tD1) / (tThen - tD1), "angry")
        overlay(ctx, (0.0, 0.03, 0.15), 0.18)
    elif t < tD2 - 0.05:
        maya_ecu(ctx, t, (t - tThen) / (tD2 - tThen), dict(MOODS["crying"], tremble=0.9), look=-0.3)
        overlay(ctx, (0.0, 0.03, 0.15), 0.12)
    else:
        dale_ecu(ctx, t, "h", (t - tD2) / (DUR("h") - tD2), MT([(tD2, "smirk"), (Wd("h", 4, 1) - 0.1, "cold")], t), glint_t=tCop)
        overlay(ctx, (0.0, 0.03, 0.15), 0.18)
    beat = t % 0.95
    pulse = max(sm(1 - beat / 0.18), 0.6 * sm(1 - abs(beat - 0.3) / 0.15)) if beat < 0.45 else 0
    vignette(ctx, 0.62 + 0.18 * pulse, 380, 1150)


# ============ I: Mom stops outside the door ============
def i_(ctx, t):
    tStop, tW, tAway, tCry = Wd("i", 0, 4), LS("i", 1), LS("i", 2), LS("i", 3)
    if t < tCry - 0.05:
        cx, cy, z = cam([(0, 540, 960, 1.0), (tStop - 0.2, 520, 1000, 1.05), (tW + 0.6, 300, 1380, 1.9), (tCry, 290, 1400, 2.0)], t)
        ctx.save(); apply_cam(ctx, cx, cy, z)
        bedroom(ctx, t, night=1.0)
        ctx.rectangle(80, 640, 360, 870); fs(ctx, (0.20, 0.16, 0.24))
        ctx.rectangle(80, 640, 360, 870); st(ctx, (0.30, 0.22, 0.20), 14)
        ell(ctx, 400, 1080, 13, 13); fs(ctx, (0.6, 0.55, 0.3), 3)
        ctx.rectangle(84, 1500, 352, 14); ctx.set_source_rgb(1, 0.82, 0.48); ctx.fill()
        glow(ctx, 260, 1514, 260, (1, 0.8, 0.45), 0.35)
        ctx.rectangle(-10, 1514, 1100, 420); ctx.set_source_rgb(0.12, 0.10, 0.14); ctx.fill()
        u_in, u_out = ramp(t, tStop - 0.1, tStop + 0.5), ramp(t, tAway + 0.2, tAway + 1.4)
        if u_in > 0 and u_out < 1:
            for k, ox in enumerate((-50, 50)):
                xx = lerp(-80, 260 + ox, u_in) + u_out * 500
                ctx.save(); ctx.rectangle(84, 1500, 352, 14); ctx.clip()
                ctx.rectangle(xx - 32, 1500, 64, 14); ctx.set_source_rgba(0.08, 0.06, 0.08, 0.95); ctx.fill(); ctx.restore()
        rrect(ctx, 600, 1020, 470, 500, 30); fs(ctx, (0.30, 0.22, 0.20))
        maya = dict(x=830, y=1430, s=1.2, look=-1, lookY=0.3, blink=blinking(t, 1), dark=0.25,
                    mood=MT([(0, "sad"), (tStop, "hopeful"), (tAway + 0.3, "crying")], t), armL=("ik", 15, -92, 1), armR=("ik", -8, -102, -1))
        draw_char(ctx, MAYA, maya, t)
        ctx.move_to(560, 1400); ctx.curve_to(700, 1300, 950, 1300, 1100, 1380); ctx.line_to(1100, 1920); ctx.line_to(560, 1920); ctx.close_path()
        fs(ctx, (0.30, 0.25, 0.45))
        ctx.restore()
        overlay(ctx, (0.0, 0.03, 0.16), 0.2)
        vignette(ctx, 0.6)
    else:
        tt = (t - tCry) / (DUR("i") - tCry)
        dawn = ramp(t, tCry, DUR("i"))
        ctx.save(); z = 1.0 + 0.06 * tt
        ctx.translate(540, 960); ctx.scale(z, z); ctx.translate(-540, -960)
        ctx.save(); ctx.translate(-200, -700); ctx.scale(1.6, 1.6); bedroom(ctx, t, night=1.0, dawn=dawn); ctx.restore()
        draw_char(ctx, MAYA, dict(x=600, y=1840, s=2.4, mood="crying", look=0.3, lookY=0.4, dark=0.2 - 0.15 * dawn, tilt=-0.08), t)
        ctx.restore()
        overlay(ctx, (1, 0.6, 0.35), 0.10 * dawn, ADD)
        vignette(ctx, 0.5)


# ============ J: long sleeves in July ============
def j(ctx, t):
    P1.s5(ctx, t)


# ============ K: counselor ============
def desk_phone(ctx, x, y, lifted, hand=None):
    rrect(ctx, x - 60, y - 40, 120, 50, 12); fs(ctx, (0.25, 0.25, 0.3))
    if not lifted:
        rrect(ctx, x - 70, y - 62, 140, 30, 14); fs(ctx, (0.2, 0.2, 0.25))
    elif hand:
        ctx.move_to(x, y - 30); ctx.curve_to(x - 40, y - 140, hand[0] + 60, hand[1] + 80, hand[0], hand[1]); st(ctx, (0.15, 0.15, 0.18), 4)


def k(ctx, t):
    tA1, t2, tCr, tA2 = LS("k", 1), LS("k", 2), Wd("k", 2, 7), LS("k", 3)
    tCall = Wd("k", 3, 7)
    keys = [(0, 540, 960, 1.0), (tA1 - 0.05, 540, 1000, 1.1), (tA1 - 0.03, 330, 1010, 1.9, "cut"), (t2 - 0.05, 330, 1005, 2.02),
            (t2 - 0.03, 800, 1060, 1.95, "cut"), (tA2 - 0.05, 800, 1060, 2.15), (tA2 - 0.03, 330, 1000, 1.85, "cut"), (DUR("k"), 320, 990, 1.98)]
    cx, cy, z = cam(keys, t)
    ctx.save(); apply_cam(ctx, cx, cy, z)
    P1.office_bg(ctx, t)
    lifting = ramp(t, tCall - 0.3, tCall + 0.3)
    alv = dict(x=300, y=1460, s=1.32, look=1, lookY=0.5, glasses=True, blink=blinking(t, 4), mouth=talk("k", "A", t),
               mood=MT([(0, "worried"), (tA2, dict(MOODS["worried"], smile=0.25, bi=-6, bo=-2))], t))
    if t >= tA1 - 0.03: alv.update(lookY=0.0)
    alv["armR"] = ik(alv, 345, 1392, -1)
    hand_w = (lerp(170, 300 - 95 * 1.32, lifting), lerp(1350, 1460 - 320 * 1.32, lifting))
    alv["armL"] = ik(alv, hand_w[0], hand_w[1], 1) if t >= tA2 else ik(alv, 255, 1392, 1)
    maya = dict(x=800, y=1470, s=1.18, look=-0.2, lookY=1, blink=blinking(t, 1),
                mood=MT([(0, "sad"), (tA1, "scared"), (t2, dict(MOODS["worried"], smile=0.2, tremble=0.4)), (tCr, "crying")], t))
    if t >= tA1 - 0.03: maya.update(look=-1, lookY=0.2)
    if t >= t2: maya.update(look=-0.8, lookY=0.1)
    maya["armL"] = ("ik", 15, -92, 1); maya["armR"] = ("ik", -8, -102, -1)
    draw_char(ctx, ALV, alv, t); draw_char(ctx, MAYA, maya, t)
    P1.desk(ctx)
    desk_phone(ctx, 170, 1385, t >= tA2 and lifting > 0, hand_w)
    if t >= tA2 and lifting > 0:
        ctx.save(); ctx.translate(*hand_w); ctx.rotate(-0.9 * lifting)
        rrect(ctx, -70, -16, 140, 32, 14); fs(ctx, (0.2, 0.2, 0.25)); ctx.restore()
    ctx.restore()
    vignette(ctx, 0.35)


# ============ L: the cliffhanger ============
def l(ctx, t):
    tPol, t2, tDale, tD, tStor = Wd("l", 0, 4), LS("l", 1), Wd("l", 1, 9), LS("l", 2), Wd("l", 2, 6)
    tEnd = LE("l", 2) + 0.3
    lights_on = t > tPol + 0.6; ph = (t * 2.4) % 1.0 < 0.5
    if t < t2 - 0.03:
        cx, cy, z = cam([(0, 540, 960, 1.0), (t2 - 0.05, 470, 900, 1.12)], t)
        ctx.save(); apply_cam(ctx, cx, cy, z)
        P1.s7_window(ctx, t)
        maya = dict(x=830, y=1440, s=1.22, legs=True, look=-1, lookY=-0.2, blink=blinking(t, 1),
                    mood=MT([(0, "worried"), (tPol + 0.4, "hopeful")], t), armL=("ik", 15, -92, 1), armR=("ik", -8, -102, -1))
        draw_char(ctx, MAYA, maya, t)
        ctx.restore()
    elif t < tDale - 0.02:
        tt = t - t2; z = 1.0 + 0.25 * sm(tt / (tDale - t2))
        ctx.save(); ctx.translate(540, 960); ctx.scale(z, z); ctx.translate(-540, -1000)
        P1.doorway(ctx, t, ramp(tt, 0.25, 1.6)); ctx.restore()
    elif t < tStor + 0.15 or t >= tEnd:
        tt = t - tDale; z = 1.0 + 0.08 * sm(tt / 3)
        ctx.save(); ctx.translate(540, 960); ctx.scale(z, z); ctx.translate(-540, -960)
        gr = cairo.RadialGradient(540, 900, 50, 540, 900, 900); gr.add_color_stop_rgb(0, 1, 1, 0.95); gr.add_color_stop_rgb(1, 0.75, 0.70, 0.62)
        ctx.set_source(gr); ctx.paint()
        ctx.rectangle(-20, 0, 190, 1920); fs(ctx, (0.50, 0.34, 0.20), 8); ctx.rectangle(910, 0, 190, 1920); fs(ctx, (0.50, 0.34, 0.20), 8)
        draw_char(ctx, DALE, dict(x=540, y=1960, s=2.6, hat=True, mood="smirk", look=0, glint=True, shadow=0.15,
                                  mouth=talk("l", "D", t), saccade=False, blink=blinking(t, 2)), t)
        ctx.restore()
        overlay(ctx, (1, 0.25, 0.2), 0.75 * (1 - ramp(tt, 0.0, 0.45)), ADD)
    else:
        maya_ecu(ctx, t, (t - tStor) / 1.0, dict(MOODS["shock"], tremble=1.0), bg=lambda c_, tt_: P1.office_bg(c_, tt_), dark=0.0)
        flash(ctx, t, tStor + 0.15, (1, 1, 1), 0.12, 0.5)
    if lights_on:
        overlay(ctx, (0.6, 0.0, 0.05) if ph else (0.0, 0.08, 0.55), 0.12, ADD)
    vignette(ctx, 0.5)
    if t >= tEnd:
        u = ramp(t, tEnd, tEnd + 0.3)
        overlay(ctx, (0.02, 0.02, 0.05), 0.8 * u)
        p = back_out((t - tEnd - 0.1) / 0.35)
        if t > tEnd + 0.1:
            ctx.save(); ctx.translate(540, 880); ctx.scale(p, p)
            rrect(ctx, -270, -130, 540, 190, 30); ctx.set_source_rgb(0.9, 0.12, 0.15); ctx.fill()
            text(ctx, "PART 2", 0, 18, 150); ctx.restore()
        q = ramp(t, tEnd + 0.45, tEnd + 0.75)
        if q > 0:
            ctx.save(); ctx.translate(540, 1110); s_ = 0.9 + 0.1 * q + 0.03 * sin(t * 6); ctx.scale(s_, s_)
            text(ctx, "FOLLOW so you don't miss it", 0, 0, 56, stroke=10); ctx.restore()
        if t > tEnd + 0.9:
            text(ctx, "Would YOU have told someone?", 540, 1250, 50, col=(1, 0.86, 0.15), stroke=10)


P1.HL["M"] = (0.45, 0.85, 1.0)
SCENES = {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f, "g": g, "h": h, "i": i_, "j": j, "k": k, "l": l}


def captions(ctx, sc, t):
    for ln in TL[sc]["lines"]:
        ws = ln["words"]
        if t < ws[0][1] - 0.06 or t > ln["start"] + ln["dur"] + 0.15: continue
        ch = P1.chunks(ws); cur = ch[0]
        for c_ in ch:
            if t >= c_[0][1] - 0.06: cur = c_
        ctx.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(88)
        words = [w[0].upper() for w in cur]
        sp = ctx.text_extents(" ").x_advance
        widths = [ctx.text_extents(w).x_advance for w in words]
        tot = sum(widths) + sp * (len(words) - 1)
        kk = min(1.0, 960 / tot)
        p = back_out((t - cur[0][1] + 0.06) / 0.14)
        ctx.save(); ctx.translate(540, 1255); ctx.scale(kk * (0.8 + 0.2 * p), kk * (0.8 + 0.2 * p))
        x = -tot / 2; active = None
        for i, w in enumerate(cur):
            if t >= w[1] - 0.03: active = i
        for i, w in enumerate(words):
            ctx.new_path(); ctx.move_to(x, 6); ctx.text_path(w); ctx.set_source_rgba(0, 0, 0, 0.45); ctx.fill()
            ctx.new_path(); ctx.move_to(x, 0); ctx.text_path(w)
            ctx.set_source_rgb(0, 0, 0); ctx.set_line_width(15); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
            ctx.set_source_rgb(*(P1.HL[ln["spk"]] if i == active else (1, 1, 1))); ctx.fill()
            x += widths[i] + sp
        ctx.restore()


def frame(surf, sc, t):
    ctx = cairo.Context(surf)
    ctx.set_source_rgb(0, 0, 0); ctx.paint()
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    SCENES[sc](ctx, t)
    ctx.set_operator(cairo.OPERATOR_OVER)
    captions(ctx, sc, t)
    P1.header(ctx)
    if sc != "a":
        aa = 1 - clamp(t / 0.12)
        if aa > 0: overlay(ctx, (0, 0, 0), aa)


def render(sc):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    n = TL[sc]["frames"]; os.makedirs(f"{EP}/scenes", exist_ok=True)
    tmp = f"{EP}/scenes/{sc}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                          "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(n):
        frame(surf, sc, i / FPS); surf.flush(); p.stdin.write(bytes(surf.get_data()))
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, f"{EP}/scenes/{sc}.mp4"); print("done", sc, n)
    else: print("FAILED", sc)


if __name__ == "__main__":
    os.makedirs(f"{EP}/preview", exist_ok=True)
    if sys.argv[1] == "preview":
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        for arg in sys.argv[2:]:
            sc, ts = arg.split(":")
            frame(surf, sc, float(ts)); surf.write_to_png(f"{EP}/preview/{sc}_{ts}.png")
    else:
        for sc in (sys.argv[2:] or SCENES.keys()): render(sc)
