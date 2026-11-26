"""The New Girl Knew All My Secrets — Part 3 (final)."""
import json, os, sys, cairo
from math import sin, cos, pi
from rig import *
import part1 as P1
import part1v2 as V
from part1 import ik
from twins_common import notebook_cu, pencil, hallway_school
from ng_common import *
import ng_part1 as N1

HERE = os.path.dirname(os.path.abspath(__file__))
EP = f"{HERE}/ng3"
TL = {s["id"]: s for s in json.load(open(f"{EP}/timeline.json"))}
V.TL = TL; V.EP = EP
P1.HEADER[:] = ["THE NEW GIRL KNEW MY SECRETS", "FINAL PART"]
MT = mood_at
talk = V.talk
DET_M = dict(bi=7, bo=-3, eo=0.85, ew=0, smile=-0.1)


def LS(sc, i): return TL[sc]["lines"][i]["start"]
def LE(sc, i): l = TL[sc]["lines"][i]; return l["start"] + l["dur"]
def Wd(sc, i, j): return TL[sc]["lines"][i]["words"][j][1]
def DUR(sc): return TL[sc]["dur"]
def zoomed(ctx, z, cx=540, cy=960): ctx.translate(540, 960); ctx.scale(z, z); ctx.translate(-cx, -cy)
hall = lambda c_, tt_: hallway_school(c_, tt_, sign="MAPLE RIDGE HIGH")
night_room = lambda c_, tt_: desk_room(c_, tt_, bear_on=False)


# ---------- A: recap ----------
def a(ctx, t):
    hall(ctx, t); overlay(ctx, (0, 0, 0), 0.5)
    video_call(ctx, t, CHLOE, dict(MOODS["smirk"], eo=0.75, smile=0.5), s=2.3, y=1000)
    vignette(ctx, 0.45)


# ---------- B: Chloe's accusation ----------
def b(ctx, t):
    t1, t2, t3, t4 = LS("b", 1), LS("b", 2), LS("b", 3), LS("b", 4)
    if t < t1 - 0.03 or (t2 - 0.03 <= t < t3 - 0.03):
        hall(ctx, t); overlay(ctx, (0, 0, 0), 0.5)
        video_call(ctx, t, CHLOE, dict(MOODS["angry"], flush=0.6, tear=0.3), mouth=talk("b", "C", t), s=2.3, y=1000)
    elif t < t2 - 0.03:
        char_ecu(ctx, t, MIA, (t - t1) / (t2 - t1), dict(MOODS["crying"], mo=0.0), hall, mouth=talk("b", "M", t), look=0.0)
    elif t < t4 - 0.03:
        hall(ctx, t); overlay(ctx, (0, 0, 0), 0.5)
        ctx.save(); ctx.translate(540, 1000); ctx.scale(2.3, 2.3)
        rrect(ctx, -170, -330, 340, 660, 40); fs(ctx, (0.12, 0.12, 0.14), 5)
        rrect(ctx, -155, -310, 310, 620, 28); ctx.set_source_rgb(0.15, 0.15, 0.18); ctx.fill()
        text(ctx, "Call ended", 0, 0, 30, col=(0.85, 0.3, 0.3)); text(ctx, "00:42", 0, 40, 24, col=(0.7, 0.7, 0.75), weight=False)
        ctx.restore()
    else:
        char_ecu(ctx, t, MIA, (t - t4) / (DUR("b") - t4), dict(MOODS["sad"], tear=0.6), hall, look=-0.2, lookY=0.4)
    vignette(ctx, 0.4)


# ---------- C: who really told? ----------
def c(ctx, t):
    t1, t2 = LS("c", 1), LS("c", 2)
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * t, 540, 1050)
        hall(ctx, t)
        draw_char(ctx, MIA, dict(x=380, y=1580, s=1.4, legs=True, mood=DET_M, look=0.7), t)
        draw_char(ctx, DEV, dict(x=740, y=1580, s=1.4, legs=True, mood="neutral", look=-0.7, glasses=True), t)
        ctx.restore()
    elif t < t2 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * (t - t1), 540, 1050)
        classroom(ctx, t)
        draw_char(ctx, GRANT, dict(x=540, y=1500, s=1.45, glasses=True, mood="neutral", look=0.0, lookY=0.6,
                                   armL=("ik", -40, -100, 1), armR=("ik", 40, -100, -1)), t)
        rrect(ctx, 260, 1360, 560, 60, 8); fs(ctx, (0.55, 0.40, 0.25)); ctx.rectangle(260, 1415, 560, 600); fs(ctx, (0.45, 0.32, 0.20))
        ctx.restore()
        V.name_tag(ctx, t, t1 + 0.3, t2 - 0.2, "MR. GRANT", "science teacher")
    else:
        char_ecu(ctx, t, DEV, (t - t2) / (DUR("c") - t2), DET_M, hall, mouth=talk("c", "D", t), look=-0.4, glasses=True)
    vignette(ctx, 0.35)


# ---------- D: the truth ----------
def d(ctx, t):
    t1, t2, t3 = LS("d", 1), LS("d", 2), LS("d", 3)
    if t < t2 - 0.03:
        char_ecu(ctx, t, GRANT, t / t2, MT([(0, "neutral"), (t1, dict(MOODS["worried"], smile=0.1))], t), classroom, mouth=talk("d", "T", t), look=0.3, glasses=True)
    elif t < t3 - 0.03:
        laptop_email(ctx, t, (t - t2) / (t3 - t2))
    else:
        char_ecu(ctx, t, MIA, (t - t3) / (DUR("d") - t3), dict(MOODS["sad"], tear=0.5), classroom, look=0.0)
    vignette(ctx, 0.35)


# ---------- E: talking to the bear ----------
def e(ctx, t):
    t1, t2, t3 = LS("e", 1), LS("e", 2), LS("e", 3)
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.05 * t, 640, 1100)
        desk_room(ctx, t, night=True, bear_red=0.6 + 0.4 * sin(t * 4))
        draw_char(ctx, MIA, dict(x=480, y=1470, s=1.35, mood=DET_M, look=1.0), t)
        desk_front(ctx, t, open_=False)
        ctx.restore()
    elif t < t2 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * (t - t1), 540, 1050)
        hall(ctx, t)
        ctx.rectangle(0, 300, 380, 1300); fs(ctx, (0.55, 0.40, 0.30))
        ell(ctx, 330, 1050, 12, 12); fs(ctx, (0.85, 0.75, 0.4), 3)
        draw_char(ctx, DEV, dict(x=720, y=1580, s=1.4, legs=True, mood="worried", look=-0.9, glasses=True, armL=("ik", 30, -100, 1), armR=("ik", -30, -105, -1)), t)
        ctx.restore()
    else:
        bearcam(ctx, t, lambda c_, tt_: (desk_room(c_, tt_, night=True, bear_on=False),
                                         draw_char(c_, MIA, dict(x=540, y=1700, s=2.0, mood=MT([(t2, DET_M), (t3, dict(MOODS["hopeful"], tear=0.7))], tt_),
                                                                 mouth=talk("e", "M", tt_), look=0.0, saccade=False), tt_),
                                         N1.desk_front(c_, tt_, open_=False) if False else None), stamp="10:58 PM")
        if Wd("e", 2, 16) <= t < t3:
            ctx.save(); ctx.translate(540, 1330); ctx.rotate(-0.05)
            ctx.rectangle(-200, -130, 400, 260); fs(ctx, (1, 1, 1), 4)
            text(ctx, "From: Mr. Grant", -170, -60, 28, col=(0.2, 0.2, 0.3), align="l"); text(ctx, "camera_0612.mp4", -170, 0, 28, col=(0.2, 0.35, 0.7), align="l")
            ctx.restore()
    vignette(ctx, 0.35)


# ---------- F: Chloe calls back ----------
def f(ctx, t):
    t1, t2, t3, tHarp = LS("f", 1), LS("f", 2), LS("f", 3), Wd("f", 3, 3)
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * t, 540, 1100)
        desk_room(ctx, t, night=True)
        p = dict(x=520, y=1470, s=1.35, mood=MT([(0, "shock"), (1.5, "hopeful")], t), look=0.0, armL=("ik", -70, -330, 1))
        draw_char(ctx, MIA, p, t)
        hx, hy = hand_world(p, "L"); rrect(ctx, hx - 20, hy - 70, 40, 90, 8); fs(ctx, (0.1, 0.1, 0.12), 3)
        desk_front(ctx, t, open_=False)
        ctx.restore()
    elif t < t2 - 0.03:
        night_room(ctx, t); overlay(ctx, (0, 0, 0), 0.45)
        video_call(ctx, t, CHLOE, dict(MOODS["crying"], tremble=0.5), mouth=talk("f", "C", t), s=2.3, y=1000)
    elif t < t3 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * (t - t2), 540, 1100)
        desk_room(ctx, t, night=True, dawn=0.0) if False else desk_room(ctx, t, night=True)
        p = dict(x=520, y=1470, s=1.35, mood="joy", look=0.0, armL=("ik", -70, -330, 1), tilt=0.06)
        draw_char(ctx, MIA, p, t)
        hx, hy = hand_world(p, "L"); rrect(ctx, hx - 20, hy - 70, 40, 90, 8); fs(ctx, (0.1, 0.1, 0.12), 3)
        desk_front(ctx, t, open_=False)
        ctx.restore()
        ctx.save(); rrect(ctx, 760, 280, 260, 80, 14); ctx.set_source_rgba(0, 0, 0, 0.6); ctx.fill()
        text(ctx, "3:04 AM", 890, 335, 40, col=(0.5, 1, 0.6)); ctx.restore()
    else:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * (t - t3), 540, 1050)
        classroom(ctx, t)
        draw_char(ctx, HARPER, dict(x=540, y=1500, s=1.4, mood=dict(MOODS["sad"], tear=0.3), lookY=0.5,
                                    armL=("ik", -20, -100, 1), armR=("ik", 20, -100, -1)), t)
        draw_char(ctx, GRANT, dict(x=900, y=1480, s=1.3, glasses=True, mood="cold", look=-0.9), t)
        ctx.restore()
        if t < tHarp:
            ctx.set_source_rgb(0.85, 0.87, 0.92); ctx.paint()
            text_bubble_phone(ctx, t, [("[photo] diary page 1", False, -1), ("Message deleted", False, t3 + 0.6), ("Message deleted", False, t3 + 1.0)],
                              title="Class 10B (31)", s=2.2, y=1000)
    vignette(ctx, 0.35)


# ---------- G: ending ----------
def g(ctx, t):
    t1, t2, t3 = LS("g", 1), LS("g", 2), LS("g", 3)
    tEnd = LE("g", 3) + 0.35
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * t, 540, 1100)
        desk_room(ctx, t, night=True, bear_on=False)
        p = dict(x=520, y=1470, s=1.35, mood=dict(MOODS["happy"], smile=0.4), lookY=0.9)
        p["armL"] = ik(p, 470 + 10 * sin(t * 9), 1300, 1); p["armR"] = ik(p, 600, 1305, -1)
        draw_char(ctx, MIA, p, t); hx, hy = hand_world(p, "L"); pencil(ctx, hx + 8, hy - 30, 0.6, rot=0.4)
        desk_front(ctx, t)
        rrect(ctx, 760, 1180, 220, 120, 10); fs(ctx, (0.30, 0.30, 0.35)); ell(ctx, 870, 1240, 16, 16); fs(ctx, (0.8, 0.8, 0.3), 3)
        ctx.restore()
    elif t < t2 - 0.03:
        ctx.save(); zoomed(ctx, 1.8, 860, 1080)
        desk_room(ctx, t, night=True, lamp=False, bear_on=False)
        ctx.rectangle(0, 0, 1080, 1920); ctx.set_source_rgba(0, 0, 0.05, 0.5); ctx.fill()
        glow(ctx, 840, 1080, 420, (1, 0.8, 0.45), 0.7)
        bear(ctx, 840, 1180, 1.0, t)
        glow(ctx, 840, 1120, 200, (1, 0.85, 0.5), 0.35)
        desk_front(ctx, t, diary=False)
        ctx.restore()
    elif t < t3 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * (t - t2), 540, 1100)
        house_day(ctx, t)
        draw_char(ctx, MIA, dict(x=330, y=1560, s=1.35, legs=True, mood="joy", look=0.8), t)
        draw_char(ctx, CHLOE, dict(x=560, y=1580, s=1.35, legs=True, mood=dict(MOODS["hopeful"], tear=0.4, smile=0.6), look=-0.6), t)
        dv = dict(x=820, y=1570, s=1.35, legs=True, mood="happy", look=-0.7, glasses=True); dv["armR"] = ("ang", 2.6, 3.0 + 0.3 * sin(t * 8))
        draw_char(ctx, DEV, dv, t)
        ctx.restore()
    else:
        char_ecu(ctx, t, MIA, (t - t3) / 2, dict(MOODS["happy"], smile=0.4, bi=-6, bo=-2), lambda c_, tt_: desk_room(c_, tt_, night=False, bear_on=False), look=0.0, saccade=False)
    vignette(ctx, 0.3)
    end_card(ctx, t, tEnd, "THE END", [("Would YOU forgive Chloe?", 52, (1, 0.86, 0.15)), ("Comment YES or NO", 44, (1, 1, 1)),
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
