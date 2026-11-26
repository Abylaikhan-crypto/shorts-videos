"""My Twin Stole My Life — Part 3 (final)."""
import json, os, sys, cairo
from math import sin, cos, pi
from rig import *
import part1 as P1
import part1v2 as V
from part1 import ik
from twins_common import *
import tw_part1 as T1

HERE = os.path.dirname(os.path.abspath(__file__))
EP = f"{HERE}/tw3"
TL = {s["id"]: s for s in json.load(open(f"{EP}/timeline.json"))}
V.TL = TL; V.EP = EP
P1.HEADER[:] = ["MY TWIN STOLE MY LIFE", "FINAL PART"]
MT = mood_at
talk = V.talk
REAL = dict(LANA, hairstyle="long", seed=29)


def LS(sc, i): return TL[sc]["lines"][i]["start"]
def LE(sc, i): l = TL[sc]["lines"][i]; return l["start"] + l["dur"]
def Wd(sc, i, j): return TL[sc]["lines"][i]["words"][j][1]
def DUR(sc): return TL[sc]["dur"]
def zoomed(ctx, z, cx=540, cy=960): ctx.translate(540, 960); ctx.scale(z, z); ctx.translate(-cx, -cy)


def letter_prop(ctx, x, y, s=1.0, rot=0.0, kind="swiss"):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    ctx.rectangle(-150, -100, 300, 200); fs(ctx, (1, 1, 1), 4)
    if kind == "swiss":
        ctx.rectangle(-150, -100, 300, 46); ctx.set_source_rgb(0.85, 0.12, 0.15); ctx.fill()
        text(ctx, "ALPINE ACADEMY", 0, -66, 24, col=(1, 1, 1)); text(ctx, "Switzerland", 0, -14, 20, col=(0.3, 0.3, 0.35), weight=False)
        text(ctx, "ACCEPTED", 0, 40, 36, col=(0.15, 0.55, 0.25))
    else:
        text(ctx, "WESTBROOK", 0, -50, 30, col=(0.55, 0.15, 0.2)); text(ctx, "ART ACADEMY", 0, -15, 24, col=(0.55, 0.15, 0.2))
        ctx.move_to(-110, 60); ctx.line_to(110, 60); st(ctx, (0.3, 0.3, 0.35), 3)
        text(ctx, "Signature", -60, 85, 16, col=(0.4, 0.4, 0.45), weight=False)
    ctx.restore()


def pen_cu(ctx, t, tt, circle=0.0):
    ctx.set_source_rgb(0.75, 0.30, 0.28); ctx.paint()
    z = 1.0 + 0.1 * sm(tt)
    ctx.save(); ctx.translate(540, 900); ctx.scale(z, z); ctx.translate(-540, -900)
    letter_prop(ctx, 560, 1100, 2.2, rot=0.04, kind="westbrook")
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    hx, hy = lerp(260, 420, sm(tt * 2)), lerp(650, 900, sm(tt * 2))
    ctx.move_to(-200, 300); ctx.line_to(hx - 50, hy - 60); st(ctx, OUTL, 170); ctx.move_to(-200, 300); ctx.line_to(hx - 50, hy - 60); st(ctx, LILY["top"], 158)
    pencil(ctx, hx + 40, hy + 40, 2.2, rot=-0.7)
    ell(ctx, hx, hy, 80, 66, 0.7); fs(ctx, SKIN, 6)
    if circle > 0:
        ctx.new_path(); ctx.arc(hx, hy, 210, -pi / 2, -pi / 2 + 2 * pi * circle); st(ctx, (0.95, 0.15, 0.15), 14)
        if circle > 0.95: text(ctx, "RIGHT HAND", hx + 40, hy - 250, 56, col=(0.95, 0.15, 0.15), stroke=10, scol=(1, 1, 1))
    ctx.restore()


def kitchen_family(ctx, t, dad_talk=False, mom_talk=False):
    V.kitchen_day(ctx, t)
    draw_char(ctx, LILY, dict(x=430, y=1440, s=1.15, mood=dict(MOODS["smirk"], eo=0.85), look=0.6, blink=blinking(t, 21)), t)
    draw_char(ctx, REAL, dict(x=880, y=1460, s=1.2, mood="worried", look=-0.8, blink=blinking(t, 29)), t)
    mom = dict(x=230, y=1500, s=1.35, mood="neutral", look=0.9, mouth=talk("b", "MO", t) if mom_talk else 0)
    dad = dict(x=640, y=1510, s=1.4, mood=dict(MOODS["worried"], smile=0.15), look=0.8, glasses=True, mouth=talk("b", "DA", t) if dad_talk else 0)
    dad["armL"] = ik(dad, 600, 1240, 1); dad["armR"] = ik(dad, 700, 1250, -1)
    draw_char(ctx, MOM2, mom, t); draw_char(ctx, DAD, dad, t)
    letter_prop(ctx, 650, 1230, 0.75, rot=-0.06)
    ctx.rectangle(-10, 1400, 1100, 600); fs(ctx, (0.85, 0.62, 0.42))


def dinner4(ctx, t, imp_mood="happy", imp_talk=False, real_talk=False, mom_mood="neutral", mom_talk=False, pen_up=0.0):
    dining(ctx, t); P1.lamp(ctx, t, 1.0)
    mom = dict(x=150, y=1450, s=1.12, mood=mom_mood, look=0.9, mouth=talk("d", "MO", t) if mom_talk else 0, blink=blinking(t, 23))
    imp = dict(x=410, y=1455, s=1.2, mood=imp_mood, look=0.6, mouth=talk("d", "LA", t) if imp_talk else 0, blink=blinking(t, 21))
    real = dict(x=680, y=1455, s=1.2, mood=DETERMINED_L, look=-0.7, mouth=talk("d", "L", t) if real_talk else 0, blink=blinking(t, 29))
    dad = dict(x=940, y=1460, s=1.22, mood="neutral", look=-0.9, glasses=True)
    imp["armL"] = ik(imp, lerp(380, 470, pen_up), lerp(1350, 1300, pen_up), 1)
    for p_ in (mom, dad, real): p_["armL"] = ik(p_, p_["x"] - 50, 1352, 1); p_["armR"] = ik(p_, p_["x"] + 50, 1352, -1)
    draw_char(ctx, MOM2, mom, t); draw_char(ctx, LILY, imp, t); draw_char(ctx, REAL, real, t); draw_char(ctx, DAD, dad, t)
    if pen_up > 0:
        hx, hy = hand_world(imp, "L"); pencil(ctx, hx + 10, hy - 10, 0.8, rot=-0.6)
    table_front(ctx, t, lasagna=False)
    letter_prop(ctx, 540, 1372, 0.5, rot=0.03, kind="westbrook")


DETERMINED_L = dict(bi=7, bo=-3, eo=0.85, ew=0, smile=-0.1)


# ---------- A: recap ----------
def a(ctx, t):
    lines = [("Day 61:", (0.15, 0.15, 0.45), 0.0), ("Make sure the real Lily", (0.85, 0.1, 0.1), Wd("a", 0, 13)), ("DISAPPEARS.", (0.85, 0.1, 0.1), Wd("a", 0, 18))]
    notebook_cu(ctx, t, t / DUR("a"), lines=lines, photos=False)
    vignette(ctx, 0.5)


# ---------- B: the boarding school letter ----------
def b(ctx, t):
    t1, t2, t3, t4 = LS("b", 1), LS("b", 2), LS("b", 3), LS("b", 4)
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * t, 540, 1100)
        V.kitchen_day(ctx, t)
        ctx.rectangle(-10, 1300, 1100, 700); fs(ctx, (0.85, 0.62, 0.42))
        letter_prop(ctx, 540, 1180, 1.6, rot=-0.05)
        ctx.restore()
    elif t < t2 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * (t - t1), 540, 1100)
        kitchen_family(ctx, t, dad_talk=True); ctx.restore()
    elif t < t3 - 0.03:
        char_ecu(ctx, t, MOM2, (t - t2) / (t3 - t2), dict(MOODS["cold"], eo=0.9), V.kitchen_day, mouth=talk("b", "MO", t), look=0.6)
    elif t < t4 - 0.03:
        char_ecu(ctx, t, REAL, (t - t3) / (t4 - t3), MT([(t3, "shock"), (t3 + 2.4, "crying")], t), V.kitchen_day, look=-0.3)
    else:
        wave = 0.3 * sin(t * 9)
        char_ecu(ctx, t, LILY, (t - t4) / (DUR("b") - t4), dict(MOODS["smirk"], eo=0.8), V.kitchen_day, look=0.2, armR=("ang", 2.6, 3.0 + wave))
    vignette(ctx, 0.35)


# ---------- C: the secret ----------
def c(ctx, t):
    t1, t2, t3 = LS("c", 1), LS("c", 2), LS("c", 3)
    if t < t1 - 0.03:
        char_ecu(ctx, t, REAL, t / t1, MT([(0, "sad"), (Wd("c", 0, 8), DETERMINED_L)], t), lambda c_, tt_: lana_room(c_, tt_), dark=0.15, look=0.2)
    elif t < t2 - 0.03:
        drawing_cu(ctx, t, (t - t1) / (t2 - t1), prog=ramp(t, t1, t2))
        if t >= Wd("c", 1, 1):
            text(ctx, "LEFT-HANDED", 540, 1520, 64, col=(0.15, 0.55, 0.95), stroke=12, scol=(1, 1, 1))
    elif t < t3 - 0.03:
        fork_cu(ctx, t, (t - t2) / (t3 - t2), circle=ramp(t, Wd("c", 2, 9), Wd("c", 2, 12) + 0.3))
        overlay(ctx, (0.9, 0.75, 0.5), 0.12)
        rrect(ctx, 60, 280, 330, 70, 14); ctx.set_source_rgba(0, 0, 0, 0.6); ctx.fill()
        text(ctx, "PART 1 · DINNER", 225, 328, 30, col=(1, 1, 1))
        if t >= Wd("c", 2, 12): text(ctx, "RIGHT HAND", 540, 1520, 64, col=(0.95, 0.15, 0.15), stroke=12, scol=(1, 1, 1))
    else:
        char_ecu(ctx, t, REAL, (t - t3) / (DUR("c") - t3), DETERMINED_L, lambda c_, tt_: lana_room(c_, tt_), dark=0.15, look=0.0, saccade=False)
    vignette(ctx, 0.4)


# ---------- D: the trap ----------
def d(ctx, t):
    t1, t2, t3, tHand, t4, tLeft = LS("d", 1), LS("d", 2), LS("d", 3), Wd("d", 3, 7), LS("d", 4), Wd("d", 4, 3)
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * t, 540, 1080); dinner4(ctx, t); ctx.restore()
    elif t < t2 - 0.03:
        ctx.save(); zoomed(ctx, 2.0 + 0.1 * sm((t - t1) / (t2 - t1)), 680, 1040); dinner4(ctx, t, real_talk=True); ctx.restore()
    elif t < t3 - 0.03:
        ctx.save(); zoomed(ctx, 2.0 + 0.1 * sm((t - t2) / (t3 - t2)), 410, 1040); dinner4(ctx, t, imp_mood="happy", imp_talk=True); ctx.restore()
    elif t < t4 - 0.03:
        pen_cu(ctx, t, (t - t3) / (t4 - t3), circle=ramp(t, tHand, tHand + 0.5))
    else:
        ctx.save(); zoomed(ctx, 2.0 + 0.15 * sm((t - t4) / 2), 150, 1040)
        dinner4(ctx, t, mom_mood=MT([(t4, "worried"), (tLeft - 0.1, "shock")], t), mom_talk=True, pen_up=1.0)
        ctx.restore()
        V.flash(ctx, t, tLeft, (1, 1, 1), 0.15, 0.5)
    vignette(ctx, 0.4)


# ---------- E: Lana breaks ----------
def e(ctx, t):
    t1, t2, t3, t4 = LS("e", 1), LS("e", 2), LS("e", 3), LS("e", 4)
    dbg = lambda c_, tt_: dining(c_, tt_)
    if t < t1 - 0.03:
        char_ecu(ctx, t, LILY, t / t1, dict(MOODS["angry"], flush=0.7), dbg, mouth=talk("e", "LA", t), shake=0.4 if t < 0.6 else 0)
    elif t < t2 - 0.03:
        char_ecu(ctx, t, LILY, (t - t1) / (t2 - t1), dict(MOODS["angry"], bi=-6, bo=4, tear=0.6, flush=0.5), dbg, mouth=talk("e", "LA", t))
    elif t < t3 - 0.03:
        char_ecu(ctx, t, LILY, (t - t2) / (t3 - t2), dict(MOODS["crying"], tremble=0.8), dbg, mouth=talk("e", "LA", t), lookY=0.4)
    elif t < t4 - 0.03:
        char_ecu(ctx, t, MOM2, (t - t3) / (t4 - t3), MT([(t3, "shock"), (t3 + 0.8, "crying")], t), dbg, look=-0.3)
    else:
        char_ecu(ctx, t, MOM2, (t - t4) / (DUR("e") - t4), "crying", dbg, mouth=talk("e", "MO", t), look=-0.3)
    vignette(ctx, 0.45)


# ---------- F: healing ----------
def f(ctx, t):
    t1, t2 = LS("f", 1), LS("f", 2)
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.03 * t, 540, 1050)
        P1.office_bg(ctx, t)
        for (ch, x, s, mood, lk) in [(MOM2, 170, 1.15, dict(MOODS["hopeful"], tear=0.3), 0.6), (LANA, 420, 1.1, "sad", 0.4),
                                     (LILY, 660, 1.1, "hopeful", -0.4), (DAD, 910, 1.2, dict(MOODS["hopeful"], tear=0.0), -0.6)]:
            P = dict(x=x, y=1470, s=s, mood=mood, look=lk, blink=blinking(t, ch["seed"]))
            if ch is DAD: P["glasses"] = True
            draw_char(ctx, ch, P, t)
        V.couch_front(ctx)
        ctx.restore()
    elif t < t2 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * (t - t1), 540, 1050)
        lana_room(ctx, t, night=False)
        strum = sin(t * 12)
        lana = dict(x=540, y=1520, s=1.5, mood=MT([(t1, "neutral"), (t1 + 1.5, "joy")], t), look=0.0, tilt=0.06 * sin(t * 3),
                    armL=("ik", -10, -150, 1), armR=("ik", 40 + 18 * strum, -40, -1))
        draw_char(ctx, LANA, lana, t)
        guitar(ctx, 540 + 10 * 1.5, 1520 - 70 * 1.5, 1.2, rot=-0.9)
        for k in range(3):
            p = ((t * 0.7 + k * 0.33) % 1)
            nx, ny = 760 + 60 * sin(k * 2 + t), 1100 - p * 400
            ell(ctx, nx, ny, 18, 14, -0.4); fs(ctx, (1, 0.86, 0.15), 3); ctx.move_to(nx + 15, ny - 4); ctx.line_to(nx + 15, ny - 70); ctx.line_to(nx + 40, ny - 55); st(ctx, OUTL, 5)
        ctx.restore()
    else:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * (t - t2), 540, 1100)
        academy_ext(ctx, t)
        draw_char(ctx, LILY, dict(x=380, y=1570, s=1.4, legs=True, mood="joy", look=0.6), t)
        draw_char(ctx, LANA, dict(x=760, y=1570 - 20 * abs(sin(t * 7)), s=1.4, legs=True, mood="joy", look=-0.6,
                                  armL=("ang", -2.6, -3.0 + 0.3 * sin(t * 9)), armR=("ang", 2.6, 3.0 - 0.3 * sin(t * 9))), t)
        for k in range(14):
            p = ((t * 0.5 + k * 0.07) % 1)
            ell(ctx, (k * 97) % 1080, 300 + p * 1500, 8, 5, t + k); ctx.set_source_rgb(*[(1, 0.86, 0.15), (0.85, 0.55, 1.0), (0.45, 0.85, 1.0)][k % 3]); ctx.fill()
        ctx.restore()
    vignette(ctx, 0.3)


# ---------- G: ending + the clue ----------
def g(ctx, t):
    t1, t2 = LS("g", 1), LS("g", 2)
    tEnd = LE("g", 2) + 0.35
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * t, 540, 1050)
        V.bedroom(ctx, t)
        draw_char(ctx, LILY, dict(x=420, y=1520, s=1.45, legs=True, mood="joy", look=0.6, tilt=0.08, armR=ik(dict(x=420, y=1520, s=1.45), 600, 1220, -1)), t)
        draw_char(ctx, LANA, dict(x=680, y=1520, s=1.45, legs=True, mood="happy", look=-0.6, tilt=-0.08, armL=ik(dict(x=680, y=1520, s=1.45), 500, 1220, 1)), t)
        ctx.restore()
    elif t < t2 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * (t - t1), 540, 1050)
        V.bedroom(ctx, t)
        ctx.rectangle(40, 600, 300, 950); fs(ctx, (0.55, 0.40, 0.30))
        draw_char(ctx, MOM2, dict(x=190, y=1520, s=1.3, legs=True, mood=dict(MOODS["happy"], smile=0.4, bi=3, bo=-3), look=0.9), t)
        draw_char(ctx, dict(LILY, hairstyle="bun"), dict(x=560, y=1520, s=1.4, legs=True, mood="joy", look=-0.6), t)
        draw_char(ctx, dict(LANA, hairstyle="long"), dict(x=850, y=1520, s=1.4, legs=True, mood="joy", look=-0.7), t)
        ctx.restore()
    else:
        fork_cu(ctx, t, (t - t2) / 3, circle=ramp(t, t2 + 1.0, t2 + 1.6))
        overlay(ctx, (0.9, 0.75, 0.5), 0.12)
        rrect(ctx, 60, 280, 330, 70, 14); ctx.set_source_rgba(0, 0, 0, 0.6); ctx.fill()
        text(ctx, "PART 1 · DINNER", 225, 328, 30, col=(1, 1, 1))
    vignette(ctx, 0.35)
    end_card(ctx, t, tEnd, "THE END", [("Did you spot the clue? Comment below!", 44, (1, 0.86, 0.15)),
                                       ("Follow Paper & Plot for the next story", 40, (1, 1, 1))])


SCENES = {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f, "g": g}
V.SCENES = SCENES

if __name__ == "__main__":
    os.makedirs(f"{EP}/preview", exist_ok=True)
    if sys.argv[1] == "preview":
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        for arg in sys.argv[2:]:
            sc, ts = arg.split(":"); V.frame(surf, sc, float(ts)); surf.write_to_png(f"{EP}/preview/{sc}_{ts}.png")
    else:
        for sc in (sys.argv[2:] or SCENES.keys()): V.render(sc)
