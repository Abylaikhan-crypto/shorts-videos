"""My Twin Stole My Life — Part 1."""
import json, os, sys, cairo
from math import sin, cos, pi
from rig import *
import part1 as P1
import part1v2 as V
from twins_common import *
from part1 import ik

HERE = os.path.dirname(os.path.abspath(__file__))
EP = f"{HERE}/tw1"
TL = {s["id"]: s for s in json.load(open(f"{EP}/timeline.json"))}
V.TL = TL; V.EP = EP
P1.HEADER[:] = ["MY TWIN STOLE MY LIFE", "PART 1"]
P1.HL.update({"L": (0.45, 0.85, 1.0), "LA": (0.85, 0.55, 1.0), "MO": (1, 0.6, 0.8), "DA": (0.6, 0.9, 0.6), "Z": (1, 0.7, 0.4), "J": (0.5, 1.0, 0.7), "G": (0.8, 0.8, 0.9), "I": (0.8, 0.7, 1.0)})
MT = mood_at
talk = V.talk
LILY_WET = dict(LILY, hair=shade(HAIR, 0.35), top=shade(LILY["top"], 0.15))


def LS(sc, i): return TL[sc]["lines"][i]["start"]
def LE(sc, i): l = TL[sc]["lines"][i]; return l["start"] + l["dur"]
def Wd(sc, i, j): return TL[sc]["lines"][i]["words"][j][1]
def DUR(sc): return TL[sc]["dur"]
def zoomed(ctx, z, cx=540, cy=960): ctx.translate(540, 960); ctx.scale(z, z); ctx.translate(-cx, -cy)


def family_dinner(ctx, t, imp_mood="happy", mom_mood="joy", dad_mood="happy", talk_sc=None, imp_look=0.4):
    dining(ctx, t)
    P1.lamp(ctx, t, 1.0)
    mom = dict(x=200, y=1445, s=1.22, mood=mom_mood, look=0.9, blink=blinking(t, 23))
    dad = dict(x=880, y=1450, s=1.3, mood=dad_mood, look=-0.9, glasses=True, blink=blinking(t, 24))
    imp = dict(x=540, y=1450, s=1.3, mood=imp_mood, look=imp_look, blink=blinking(t, 21))
    if talk_sc:
        mom["mouth"] = talk(talk_sc, "MO", t); imp["mouth"] = talk(talk_sc, "LA", t)
    mom["armL"] = ik(mom, 150, 1352, 1); mom["armR"] = ik(mom, 250, 1352, -1)
    dad["armL"] = ik(dad, 820, 1352, 1); dad["armR"] = ik(dad, 940, 1352, -1)
    bob = 18 * max(0, sin(t * 2.6))
    imp["armL"] = ik(imp, 500, 1330 - bob, 1)      # character's RIGHT hand holds the fork
    imp["armR"] = ik(imp, 610, 1350, -1)
    draw_char(ctx, MOM2, mom, t); draw_char(ctx, DAD, dad, t); draw_char(ctx, LILY, imp, t)
    hx, hy = hand_world(imp, "L")
    fork(ctx, hx + 6, hy - 10, 0.9, rot=0.35)
    table_front(ctx, t, lasagna=True)
    ell(ctx, 540, 1372, 80, 18); fs(ctx, (0.98, 0.98, 0.98), 4)


# ---------- A: hook ----------
def a(ctx, t):
    z = 1.0 + 0.35 * sm(t / DUR("a"))
    ctx.save(); zoomed(ctx, z, 540, 1080)
    family_dinner(ctx, t)
    ctx.restore()
    ctx.rectangle(0, 0, 70, 1920); ctx.set_source_rgba(0.1, 0.07, 0.05, 0.9 - 0.4 * sm(t / 4)); ctx.fill()
    ctx.rectangle(1010, 0, 70, 1920); ctx.fill()
    vignette(ctx, 0.5)


# ---------- B: intro ----------
def b(ctx, t):
    t1, t2, tLaugh, tCopy, tOr = LS("b", 1), LS("b", 2), Wd("b", 1, 4), Wd("b", 1, 12), Wd("b", 2, 7)
    ctx.save(); zoomed(ctx, 1.0 + 0.1 * sm(t / DUR("b")), 540, 1000)
    V.bedroom(ctx, t)
    joy = tLaugh <= t < tLaugh + 1.0
    lily = dict(x=330, y=1520, s=1.45, legs=True, look=0.3, blink=blinking(t, 21), mood="joy" if joy else "happy")
    lana = dict(x=760, y=1520, s=1.45, legs=True, look=-0.3, blink=blinking(t, 22),
                mood="joy" if joy else MT([(0, "neutral"), (tOr, "smirk")], t))
    if t >= tOr: lana.update(look=-1, lookY=0.1)
    draw_char(ctx, LILY, lily, t); draw_char(ctx, LANA, lana, t)
    ctx.restore()
    if tCopy - 0.1 <= t < tCopy + 1.4:
        p = back_out((t - tCopy + 0.1) / 0.3)
        ctx.save(); ctx.translate(540, 700); ctx.scale(p, p)
        rrect(ctx, -300, -60, 600, 110, 20); ctx.set_source_rgba(0.1, 0.1, 0.15, 0.85); ctx.fill()
        text(ctx, "CTRL+C  •  CTRL+V", 0, 22, 54, col=(1, 0.86, 0.15)); ctx.restore()
    V.name_tag(ctx, t, 0.8, 2.9, "LILY", "that's me")
    V.name_tag(ctx, t, 2.9, 5.0, "LANA", "my twin sister")
    vignette(ctx, 0.3)


# ---------- C: always compared ----------
def c(ctx, t):
    t1, t2, tAc, t3, tNever, t4, t5, t6 = LS("c", 1), LS("c", 2), Wd("c", 2, 20), LS("c", 3), Wd("c", 3, 7), LS("c", 4), LS("c", 5), LS("c", 6)
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * t)
        V.kitchen_day(ctx, t)
        draw_char(ctx, LANA, dict(x=540, y=1480, s=1.45, mood="sad", lookY=0.9, armL=("ik", -40, -90, 1), armR=("ik", 40, -90, -1)), t)
        ctx.rectangle(-10, 1380, 1100, 600); fs(ctx, (0.85, 0.62, 0.42))
        ctx.save(); ctx.translate(560, 1360); ctx.rotate(-0.08); ctx.rectangle(-110, -70, 220, 140); fs(ctx, (1, 1, 1), 3)
        text(ctx, "REPORT CARD", 0, -30, 20, col=(0.2, 0.2, 0.3)); text(ctx, "C-", 0, 40, 64, col=(0.85, 0.15, 0.15)); ctx.restore()
        ctx.restore()
    elif t < t2 - 0.03:
        char_ecu(ctx, t, MOM2, (t - t1) / (t2 - t1), dict(MOODS["cold"], eo=0.9), V.kitchen_day, mouth=talk("c", "MO", t), look=0.6)
    elif t < t3 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * (t - t2), 540, 1000)
        V.bedroom(ctx, t)
        lily = dict(x=540, y=1520, s=1.5, legs=True, mood=MT([(t2, "happy"), (tAc - 0.2, "joy")], t), look=0.2,
                    armL=("ik", -50, -200, 1), armR=("ik", 50, -200, -1))
        draw_char(ctx, LILY, lily, t)
        ctx.save(); ctx.translate(540, 1520 - 215 * 1.5); ctx.rotate(-0.04)
        ctx.rectangle(-150, -100, 300, 200); fs(ctx, (1, 1, 1), 4)
        text(ctx, "WESTBROOK", 0, -50, 30, col=(0.55, 0.15, 0.2)); text(ctx, "ART ACADEMY", 0, -15, 24, col=(0.55, 0.15, 0.2))
        text(ctx, "Interview invitation", 0, 30, 18, col=(0.3, 0.3, 0.35), weight=False)
        if t >= tAc + 0.8: text(ctx, "FULL SCHOLARSHIP", 0, 70, 22, col=(0.85, 0.6, 0.1))
        ctx.restore()
        if t >= tAc + 0.8:
            for k in range(6): V.sparkle(ctx, 330 + k * 85, 900 + 60 * sin(k * 2), t, k)
        ctx.restore()
    elif t < tNever - 0.05:
        drawing_cu(ctx, t, (t - t3) / (tNever - t3), prog=ramp(t, t3, tNever))
    elif t < t4 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.03 * (t - tNever), 540, 1000)
        V.bedroom(ctx, t)
        ctx.rectangle(60, 600, 330, 950); fs(ctx, (0.35, 0.25, 0.25))
        draw_char(ctx, LANA, dict(x=230, y=1520, s=1.35, legs=True, mood="cold", look=0.8, armL=("ik", 50, -110, 1), armR=("ik", -50, -105, -1)), t)
        draw_char(ctx, LILY, dict(x=760, y=1520, s=1.35, legs=True, mood="hopeful", look=-0.8), t)
        ctx.restore()
    elif t < t5 - 0.03:
        char_ecu(ctx, t, LANA, (t - t4) / (t5 - t4), dict(MOODS["smirk"], eo=0.7), lambda c_, tt_: V.bedroom(c_, tt_), mouth=talk("c", "LA", t), look=0.4)
    elif t < t6 - 0.03:
        char_ecu(ctx, t, LILY, (t - t5) / (t6 - t5), dict(MOODS["sad"], tear=0.4), lambda c_, tt_: V.bedroom(c_, tt_), mouth=talk("c", "L", t), look=-0.4)
    else:
        char_ecu(ctx, t, LANA, (t - t6) / (DUR("c") - t6), dict(MOODS["cold"], eo=0.7), lambda c_, tt_: V.bedroom(c_, tt_), mouth=talk("c", "LA", t),
                 look=lerp(0.4, 1.0, ramp(t, LE("c", 6), LE("c", 6) + 0.4)))
    vignette(ctx, 0.35)


# ---------- D: Zoe's message ----------
def d(ctx, t):
    t1, t2, t3 = LS("d", 1), LS("d", 2), LS("d", 3)
    if t < t2 - 0.03:
        keys = [(0, 540, 960, 1.0), (t1 - 0.03, 540, 1000, 1.08), (t1, 380, 1000, 1.7, "cut"), (t2, 380, 1000, 1.8)]
        cx, cy, z = cam(keys, t)
        ctx.save(); apply_cam(ctx, cx, cy, z)
        hallway_school(ctx, t)
        zoe = dict(x=360, y=1560, s=1.4, legs=True, mood="joy" if t > t1 + 0.3 else "happy", look=0.8, mouth=talk("d", "Z", t),
                   armL=("ik", -60, -140, 1), armR=("ik", 40, -150, -1))
        draw_char(ctx, ZOE, zoe, t)
        rrect(ctx, 360 + 40 * 1.4 - 30, 1560 - 160 * 1.4 - 55, 60, 100, 10); fs(ctx, (0.12, 0.12, 0.14), 3)
        draw_char(ctx, LILY, dict(x=760, y=1560, s=1.4, legs=True, mood=MT([(0, "happy"), (t1 + 2.5, "worried")], t), look=-0.8), t)
        ctx.restore()
    elif t < t3 - 0.03:
        char_ecu(ctx, t, LILY, (t - t2) / (t3 - t2), "worried", hallway_school, mouth=talk("d", "L", t), look=-0.5)
    else:
        ctx.set_source_rgb(0.85, 0.87, 0.92); ctx.paint()
        text_bubble_phone(ctx, t, [("You're the only real friend I have. I can't trust Lana.", False, t3 - 0.2),
                                   ("Sent 2:14 AM", False, t3 + 2.4)], title="Lily", s=2.2, y=880)
    vignette(ctx, 0.3)


# ---------- E: Jake ----------
def e(ctx, t):
    t1, t2, t3, tSaw = LS("e", 1), LS("e", 2), LS("e", 3), Wd("e", 3, 2)
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * t)
        hallway_school(ctx, t)
        draw_char(ctx, JAKE, dict(x=330, y=1560, s=1.45, legs=True, mood="cold", look=-1, lookY=0.3, armL=("ik", 40, -105, 1), armR=("ik", -40, -110, -1)), t)
        draw_char(ctx, LILY, dict(x=780, y=1560, s=1.4, legs=True, mood="worried", look=-1), t)
        ctx.restore()
    elif t < t2 - 0.03:
        char_ecu(ctx, t, JAKE, (t - t1) / (t2 - t1), dict(MOODS["angry"], flush=0.2, eo=0.8), hallway_school, mouth=talk("e", "J", t), look=0.5)
    elif t < t3 - 0.03:
        char_ecu(ctx, t, LILY, (t - t2) / (t3 - t2), dict(MOODS["worried"], tear=0.3), hallway_school, mouth=talk("e", "L", t), look=-0.5)
    else:
        char_ecu(ctx, t, JAKE, (t - t3) / (DUR("e") - t3), "sad", hallway_school, mouth=talk("e", "J", t), look=0.4)
        V.flash(ctx, t, tSaw, (1, 1, 1), 0.15, 0.35)
    vignette(ctx, 0.35)


# ---------- F: sketchbook gone ----------
def f(ctx, t):
    tLana = Wd("f", 1, 9)
    if t < tLana - 0.05:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * t, 540, 1000)
        V.bedroom(ctx, t)
        ctx.rectangle(560, 1180, 480, 30); fs(ctx, (0.55, 0.38, 0.24))
        rrect(ctx, 700, 1120, 220, 60, 6); st(ctx, (0.5, 0.5, 0.55), 3)
        ctx.set_dash([12, 10]); rrect(ctx, 700, 1120, 220, 60, 6); st(ctx, (0.9, 0.2, 0.2), 4); ctx.set_dash([])
        sx = 420 + 160 * sin(t * 1.6)
        draw_char(ctx, LILY, dict(x=sx, y=1520, s=1.45, legs=True, mood=dict(MOODS["scared"], tremble=0.2), look=0.8 * sin(t * 2.3),
                                  lookY=0.4, armL=("ang", -0.8 - 0.5 * sin(t * 4), -1.6), armR=("ang", 0.8 + 0.5 * sin(t * 4 + 1), 1.6)), t)
        ctx.restore()
        for k in range(3):
            p = ((t * 0.8 + k * 0.33) % 1)
            ctx.save(); ctx.translate(200 + k * 330, 300 + p * 1400); ctx.rotate(p * 6 + k)
            ctx.rectangle(-50, -60, 100, 120); ctx.set_source_rgba(1, 1, 1, 0.5 * (1 - p)); ctx.fill(); ctx.restore()
    else:
        def door_bg(c_, tt_):
            lana_room(c_, tt_, night=True)
            c_.rectangle(0, 0, 1080, 1920); c_.set_source_rgba(0.0, 0.0, 0.05, 0.4); c_.fill()
        char_ecu(ctx, t, LANA, (t - tLana) / (DUR("f") - tLana), MT([(tLana, "neutral"), (Wd("f", 1, 16), dict(MOODS["smirk"], eo=0.7))], t),
                 door_bg, dark=0.25, look=0.3, saccade=False)
    vignette(ctx, 0.4)


# ---------- G: bus broke down ----------
def g(ctx, t):
    t1 = LS("g", 1)
    ctx.save(); zoomed(ctx, 1.0 + 0.04 * t, 540, 1050)
    night_street(ctx, t, 0)
    bus_broken(ctx, -200, 1500, 0.9, t)
    wx = lerp(980, 600, sm(t / DUR("g")))
    lily = dict(x=wx, y=1560 + 6 * abs(sin(t * 6)), s=1.35, legs=True, mood=MT([(0, "sad"), (t1, dict(MOODS["worried"], tear=0.3))], t),
                look=-0.4, lookY=0.6 if t > t1 else 0, armL=("ik", 10, -150, 1), armR=("ang", 0.14, 0.05))
    draw_char(ctx, LILY_WET, lily, t)
    hx, hy = hand_world(lily, "L")
    rrect(ctx, hx - 24, hy - 60, 48, 84, 8); fs(ctx, (0.08, 0.08, 0.1), 3)
    ctx.restore()
    V.rain(ctx, t, 0.4)
    overlay(ctx, (0.0, 0.03, 0.15), 0.2)
    vignette(ctx, 0.55)


# ---------- H: the reveal ----------
def h(ctx, t):
    tMe, t1, t2, t3, t4 = Wd("h", 0, 17), LS("h", 1), LS("h", 2), LS("h", 3), LS("h", 4)
    tEnd = LE("h", 4) + 0.35
    if t < tMe - 0.05:
        ctx.save(); zoomed(ctx, 1.0 + 0.25 * sm(t / tMe), 540, 1080)
        family_dinner(ctx, t)
        ctx.restore()
        op = ramp(t, 0.2, 1.4)
        w = 540 * op
        ctx.rectangle(0, 0, 540 - w, 1920); ctx.set_source_rgb(0.20, 0.14, 0.10); ctx.fill()
        ctx.rectangle(540 + w, 0, 540 - w, 1920); ctx.fill()
    elif t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.9 + 0.1 * sm((t - tMe) / 0.8), 540, 1060)
        family_dinner(ctx, t)
        ctx.restore()
        V.flash(ctx, t, tMe, (1, 1, 1), 0.15, 0.5)
    elif t < t2 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * (t - t1), 540, 1060)
        family_dinner(ctx, t, mom_mood="joy", dad_mood="joy")
        ctx.restore()
    elif t < t3 - 0.03:
        ctx.save(); zoomed(ctx, 2.0 + 0.1 * sm((t - t2) / (t3 - t2)), 540, 1040)
        family_dinner(ctx, t, imp_mood=dict(MOODS["smirk"], eo=0.8), talk_sc="h", imp_look=0.0)
        ctx.restore()
    elif t < t4 - 0.03:
        ctx.save(); zoomed(ctx, 2.0 + 0.1 * sm((t - t3) / (t4 - t3)), 230, 1040)
        family_dinner(ctx, t, mom_mood=dict(MOODS["cold"], eo=0.9), talk_sc="h")
        ctx.restore()
    else:
        def door(c_, tt_):
            c_.set_source_rgb(0.08, 0.06, 0.06); c_.paint(); glow(c_, 540, 900, 700, (1, 0.8, 0.5), 0.35)
        char_ecu(ctx, t, LILY_WET, (t - t4) / 2.5, dict(MOODS["crying"], tremble=0.8), door, dark=0.1, look=0.0)
    vignette(ctx, 0.45)
    end_card(ctx, t, tEnd, "PART 2", [("FOLLOW so you don't miss it", 56, (1, 1, 1)), ("Who is the REAL Lily?", 50, (1, 0.86, 0.15))])


SCENES = {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f, "g": g, "h": h}
V.SCENES = SCENES

if __name__ == "__main__":
    os.makedirs(f"{EP}/preview", exist_ok=True)
    if sys.argv[1] == "preview":
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        for arg in sys.argv[2:]:
            sc, ts = arg.split(":"); V.frame(surf, sc, float(ts)); surf.write_to_png(f"{EP}/preview/{sc}_{ts}.png")
    else:
        for sc in (sys.argv[2:] or SCENES.keys()): V.render(sc)
