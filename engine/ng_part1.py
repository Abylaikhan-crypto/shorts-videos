"""The New Girl Knew All My Secrets — Part 1."""
import json, os, sys, cairo
from math import sin, cos, pi
from rig import *
import part1 as P1
import part1v2 as V
from part1 import ik
from twins_common import notebook_cu, pencil, hallway_school
from ng_common import *

HERE = os.path.dirname(os.path.abspath(__file__))
EP = f"{HERE}/ng1"
TL = {s["id"]: s for s in json.load(open(f"{EP}/timeline.json"))}
V.TL = TL; V.EP = EP
P1.HEADER[:] = ["THE NEW GIRL KNEW MY SECRETS", "PART 1"]
P1.HL.update({"M": (0.45, 0.85, 1.0), "H": (1.0, 0.55, 0.75), "D": (0.55, 0.9, 0.6), "C": (0.85, 0.55, 1.0), "T": (0.8, 0.8, 0.9), "E": (1, 0.6, 0.4)})
MT = mood_at
talk = V.talk


def LS(sc, i): return TL[sc]["lines"][i]["start"]
def LE(sc, i): l = TL[sc]["lines"][i]; return l["start"] + l["dur"]
def Wd(sc, i, j): return TL[sc]["lines"][i]["words"][j][1]
def DUR(sc): return TL[sc]["dur"]
def zoomed(ctx, z, cx=540, cy=960): ctx.translate(540, 960); ctx.scale(z, z); ctx.translate(-cx, -cy)


def mia_writing(ctx, t, mood="neutral", bear_red=0.0, night=True, dawn=0.0, write=True):
    desk_room(ctx, t, night=night, bear_red=bear_red)
    p = dict(x=520, y=1470, s=1.35, mood=mood, lookY=0.9 if write else 0.0, look=-0.1, blink=blinking(t, 31))
    wob = 10 * sin(t * 9) if write else 0
    p["armL"] = ik(p, 470 + wob, 1300, 1); p["armR"] = ik(p, 600, 1305, -1)
    draw_char(ctx, MIA, p, t)
    if write:
        hx, hy = hand_world(p, "L"); pencil(ctx, hx + 8, hy - 30, 0.6, rot=0.4)
    desk_front(ctx, t)
    if dawn > 0: overlay(ctx, (1, 0.6, 0.35), 0.15 * dawn, ADD)


def class_pair(ctx, t, mia_mood="neutral", har_mood="happy", har_talk=None, har_lean=0.0, har_x=760):
    classroom(ctx, t)
    draw_char(ctx, MIA, dict(x=330, y=1480, s=1.35, mood=mia_mood, look=0.7, blink=blinking(t, 31), armL=("ik", -30, -100, 1), armR=("ik", 30, -100, -1)), t)
    h = dict(x=har_x, y=1480, s=1.35, mood=har_mood, look=-0.8, tilt=-0.1 * har_lean, blink=blinking(t, 32),
             mouth=talk(har_talk, "H", t) if har_talk else 0)
    draw_char(ctx, HARPER, h, t)
    school_desk(ctx)


# ---------- A: hook ----------
def a(ctx, t):
    tWrote = Wd("a", 0, 10)
    if t < tWrote - 0.05:
        ctx.save(); zoomed(ctx, 1.1 + 0.15 * sm(t / tWrote), 540, 1050)
        class_pair(ctx, t, mia_mood="neutral", har_mood=dict(MOODS["happy"], smile=0.7), har_lean=ramp(t, 1.5, 2.2))
        ctx.restore()
    else:
        char_ecu(ctx, t, MIA, (t - tWrote) / 2, "shock", classroom, look=0.6, tremble=0.4)
        V.flash(ctx, t, tWrote, (1, 1, 1), 0.15, 0.4)
    vignette(ctx, 0.4)


# ---------- B: Mia and her diary ----------
def b(ctx, t):
    t1, tKnows, t2 = LS("b", 1), Wd("b", 1, 11), LS("b", 2)
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.05 * t, 540, 1100); mia_writing(ctx, t, mood="neutral"); ctx.restore()
        V.name_tag(ctx, t, 0.6, 3.0, "MIA", "that's me")
    elif t < tKnows + 0.3:
        lines = [("Dear diary,", (0.15, 0.15, 0.45), t1), ("Ethan laughed at my joke", (0.15, 0.15, 0.45), Wd("b", 1, 2)),
                 ("today. His laugh sounds", (0.15, 0.15, 0.45), Wd("b", 1, 3)), ("like music.", (0.15, 0.15, 0.45), Wd("b", 1, 4))]
        notebook_cu(ctx, t, (t - t1) / 6, lines=lines, photos=False)
    elif t < tKnows + 1.4:
        bearcam(ctx, t, lambda c_, tt_: mia_writing(c_, tt_, mood="neutral"))
    else:
        ctx.save(); zoomed(ctx, 1.0 + 0.05 * (t - t2), 640, 1150)
        desk_room(ctx, t, night=True, bear_on=False)
        p = dict(x=560, y=1470, s=1.35, mood="happy", look=0.5, blink=blinking(t, 31))
        p["armR"] = ik(p, 800, 1200, -1)
        draw_char(ctx, MIA, p, t)
        bear(ctx, 840, 1180, 1.0, t)
        desk_front(ctx, t, open_=False)
        ctx.restore()
        V.name_tag(ctx, t, Wd("b", 2, 17), DUR("b") - 0.2, "MR. BUTTONS", "my teddy bear")
    vignette(ctx, 0.45)


# ---------- C: Harper arrives ----------
def c(ctx, t):
    t1, t2, t3 = LS("c", 1), LS("c", 2), LS("c", 3)
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * t, 540, 1050)
        class_pair(ctx, t, mia_mood="neutral", har_mood=dict(MOODS["happy"], smile=0.8), har_x=lerp(1300, 760, sm((t - 2.0) / 1.5)))
        ctx.restore()
        V.name_tag(ctx, t, 2.2, t1 - 0.2, "HARPER", "the new girl")
    elif t < t3 - 0.03:
        mood = dict(MOODS["happy"], smile=0.8) if t < Wd("c", 1, 8) else dict(MOODS["happy"], smile=0.5, bi=-2, bo=-4)
        char_ecu(ctx, t, HARPER, (t - t1) / (t3 - t1), mood, classroom, mouth=talk("c", "H", t), look=-0.5, tilt=0.05)
    else:
        char_ecu(ctx, t, MIA, (t - t3) / (DUR("c") - t3), dict(MOODS["shock"], mo=0.4, tremble=0.4), classroom, look=0.5)
    vignette(ctx, 0.35)


# ---------- D: lunch ----------
def d(ctx, t):
    t1, t2, t3 = LS("d", 1), LS("d", 2), LS("d", 3)
    if t < t1 - 0.03 or t >= t3 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.03 * (t % 8), 540, 1080)
        cafeteria(ctx, t)
        for x in (90, 1000):
            ell(ctx, x, 1150, 60, 66); ctx.set_source_rgba(0.3, 0.3, 0.35, 0.5); ctx.fill(); rrect(ctx, x - 80, 1210, 160, 200, 40); ctx.fill()
        sweep = 0.9 * sin(t * 1.6) if t >= t3 else 0.6
        draw_char(ctx, MIA, dict(x=380, y=1490, s=1.4, mood="worried" if t >= t3 else "neutral", look=sweep), t)
        draw_char(ctx, HARPER, dict(x=lerp(720, 640, ramp(t, 0.8, 1.6)) if t < t3 else 760, y=1490, s=1.4, mood=dict(MOODS["happy"], smile=0.6),
                                    look=-0.9, tilt=-0.12 * ramp(t, 0.8, 1.6) if t < t3 else 0), t)
        lunch_table(ctx)
        ctx.restore()
    elif t < t2 - 0.03:
        char_ecu(ctx, t, HARPER, (t - t1) / (t2 - t1), dict(MOODS["smirk"], eo=0.8), cafeteria, mouth=talk("d", "H", t) * 0.6, look=-0.6, tilt=-0.08)
    else:
        char_ecu(ctx, t, MIA, (t - t2) / (t3 - t2), dict(MOODS["scared"], tremble=0.5), cafeteria, look=0.4)
    vignette(ctx, 0.35)


# ---------- E: the trap ----------
def e(ctx, t):
    t1, t2, t3, t4 = LS("e", 1), LS("e", 2), LS("e", 3), LS("e", 4)
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.05 * t, 540, 1100); mia_writing(ctx, t, mood=DETERMINED_M); ctx.restore()
    elif t < t2 - 0.03:
        lines = [("Secret:", (0.85, 0.1, 0.1), t1), ("I hid $500 inside the", (0.15, 0.15, 0.45), Wd("e", 1, 2)),
                 ("old oak tree behind", (0.15, 0.15, 0.45), Wd("e", 1, 7)), ("the school.", (0.15, 0.15, 0.45), Wd("e", 1, 10))]
        notebook_cu(ctx, t, (t - t1) / 4, lines=lines, photos=False)
    elif t < t3 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.05 * (t - t2), 640, 1100)
        oak_scene(ctx, t)
        dig = sin(t * 7) * 15
        h = dict(x=620, y=1560, s=1.4, legs=True, mood=dict(MOODS["happy"], smile=0.3), look=1, lookY=0.2)
        h["armR"] = ik(h, 770 + dig, 1060, -1)
        draw_char(ctx, HARPER, h, t)
        ctx.rectangle(-10, 760, 300, 1200); fs(ctx, (0.78, 0.52, 0.42))
        draw_char(ctx, MIA, dict(x=200, y=1580, s=1.2, legs=True, mood="shock", look=1), t)
        ctx.rectangle(-10, 760, 120, 1200); fs(ctx, (0.78, 0.52, 0.42))
        ctx.restore()
    elif t < t4 - 0.03:
        char_ecu(ctx, t, HARPER, (t - t3) / (t4 - t3), dict(MOODS["happy"], smile=0.4, bi=-10, bo=4, ew=1, eo=1.15), oak_scene, mouth=talk("e", "H", t), look=-0.8, sweat=True)
    else:
        char_ecu(ctx, t, MIA, (t - t4) / (DUR("e") - t4), DETERMINED_M, oak_scene, look=0.3)
    vignette(ctx, 0.35)


DETERMINED_M = dict(bi=7, bo=-3, eo=0.85, ew=0, smile=-0.1)


# ---------- F: sleepless night ----------
def f(ctx, t):
    t1, t2 = LS("f", 1), LS("f", 2)
    if t < t2 - 0.03:
        dawn = ramp(t, 3.0, t2)
        ctx.save(); zoomed(ctx, 1.0 + 0.06 * sm(t / t2), 540, 1150)
        desk_room(ctx, t, night=True)
        p = dict(x=520, y=1470, s=1.35, mood=MT([(0, "worried"), (t1, dict(MOODS["worried"], lid=0.5))], t), look=0.6 * sin(t * 1.3), blink=blinking(t, 31))
        p["armL"] = ik(p, 440, 1260, 1); p["armR"] = ik(p, 600, 1260, -1)
        draw_char(ctx, MIA, p, t)
        ctx.move_to(250, 1300); ctx.curve_to(400, 1120, 650, 1120, 790, 1300); ctx.close_path(); fs(ctx, (0.55, 0.45, 0.65))
        desk_front(ctx, t, diary=False)
        if dawn > 0: overlay(ctx, (1, 0.6, 0.35), 0.18 * dawn, ADD)
        ctx.restore()
        if t >= t1:
            for (x, y, lab, t0) in [(260, 520, "WINDOW: LOCKED", Wd("f", 1, 3)), (260, 620, "CLOSET: EMPTY", Wd("f", 1, 6))]:
                if t >= t0:
                    p_ = back_out((t - t0) / 0.3); ctx.save(); ctx.translate(x + 200, y); ctx.scale(p_, p_)
                    rrect(ctx, -230, -42, 460, 70, 14); ctx.set_source_rgba(0, 0, 0, 0.6); ctx.fill()
                    text(ctx, lab, 0, 10, 38, col=(0.5, 1, 0.6)); ctx.restore()
    else:
        char_ecu(ctx, t, HARPER, (t - t2) / (DUR("f") - t2), dict(MOODS["smirk"], eo=0.8, smile=0.5), classroom, mouth=talk("f", "H", t), look=-0.5, tilt=0.06)
    vignette(ctx, 0.45)


# ---------- G: the bear ----------
def g(ctx, t):
    t1, tBl, tRed, t2 = LS("g", 1), Wd("g", 1, 11), Wd("g", 1, 12), LS("g", 2)
    tEnd = LE("g", 2) + 0.35
    red = ramp(t, tBl - 0.05, tBl + 0.1) * (1 - ramp(t, tBl + 0.3, tBl + 0.5)) + ramp(t, tRed - 0.05, tRed + 0.1)
    if t < t1 - 0.03:
        char_ecu(ctx, t, MIA, t / t1, dict(MOODS["worried"], lid=0.3), lambda c_, tt_: desk_room(c_, tt_, bear_on=False), dark=0.15, look=0.2)
    else:
        z = 1.0 + 1.6 * sm((t - t1) / (tRed - t1)) + 0.2 * sm((t - tRed) / 3)
        ctx.save(); zoomed(ctx, z, 860, 1080)
        desk_room(ctx, t, night=True, bear_red=red)
        desk_front(ctx, t, open_=False)
        ctx.restore()
        overlay(ctx, (0.0, 0.0, 0.08), 0.25)
        if t >= tRed: V.flash(ctx, t, tRed, (1, 0.2, 0.2), 0.3, 0.5)
    vignette(ctx, 0.55)
    end_card(ctx, t, tEnd, "PART 2", [("FOLLOW so you don't miss it", 56, (1, 1, 1)), ("Who is watching Mia?", 50, (1, 0.86, 0.15))])


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
