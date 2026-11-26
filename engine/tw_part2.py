"""My Twin Stole My Life — Part 2."""
import json, os, sys, cairo
from math import sin, cos, pi
from rig import *
import part1 as P1
import part1v2 as V
from part1 import ik
from twins_common import *
import tw_part1 as T1

HERE = os.path.dirname(os.path.abspath(__file__))
EP = f"{HERE}/tw2"
TL = {s["id"]: s for s in json.load(open(f"{EP}/timeline.json"))}
V.TL = TL; V.EP = EP
P1.HEADER[:] = ["MY TWIN STOLE MY LIFE", "PART 2"]
MT = mood_at
talk = V.talk
REAL = dict(LANA, hairstyle="long", seed=29)          # the real Lily, now forced to live as "Lana"
LILY_WET = T1.LILY_WET


def LS(sc, i): return TL[sc]["lines"][i]["start"]
def LE(sc, i): l = TL[sc]["lines"][i]; return l["start"] + l["dur"]
def Wd(sc, i, j): return TL[sc]["lines"][i]["words"][j][1]
def DUR(sc): return TL[sc]["dur"]
def zoomed(ctx, z, cx=540, cy=960): ctx.translate(540, 960); ctx.scale(z, z); ctx.translate(-cx, -cy)


def living_night(c_, t):
    V.living_room(c_, t); c_.rectangle(0, 0, 1080, 1920); c_.set_source_rgba(0.05, 0.05, 0.2, 0.25); c_.fill()


# ---------- A: recap ----------
def a(ctx, t):
    tMom = Wd("a", 0, 13)
    if t < tMom - 0.05:
        ctx.save(); zoomed(ctx, 2.0 + 0.15 * sm(t / tMom), 540, 1040)
        T1.family_dinner(ctx, t, imp_mood=dict(MOODS["smirk"], eo=0.8), imp_look=0.0)
        ctx.restore()
    else:
        ctx.save(); zoomed(ctx, 2.0 + 0.1 * sm((t - tMom) / 1.5), 230, 1040)
        T1.family_dinner(ctx, t, mom_mood=dict(MOODS["cold"], eo=0.9))
        ctx.restore()
    vignette(ctx, 0.45)


# ---------- B: nobody believes ----------
def b(ctx, t):
    t1, t2, t3, t4 = LS("b", 1), LS("b", 2), LS("b", 3), LS("b", 4)
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * t, 540, 1000)
        living_night(ctx, t)
        draw_char(ctx, LILY, dict(x=250, y=1500, s=1.35, legs=True, mood="worried", look=0.6), t)
        draw_char(ctx, MOM2, dict(x=540, y=1490, s=1.4, legs=True, mood="cold", look=0.8, armL=("ik", 30, -110, 1), armR=("ik", -30, -115, -1)), t)
        draw_char(ctx, LILY_WET, dict(x=840, y=1500, s=1.35, legs=True, mood="crying", look=-0.8), t)
        ctx.restore()
    elif t < t2 - 0.03:
        char_ecu(ctx, t, LILY_WET, (t - t1) / (t2 - t1), dict(MOODS["crying"], mo=0.1), living_night, mouth=talk("b", "L", t), look=-0.5)
    elif t < t3 - 0.03:
        mood = MT([(t2, dict(MOODS["worried"], tear=0.3)), (LE("b", 2) - 0.6, dict(MOODS["smirk"], eo=0.8))], t)
        char_ecu(ctx, t, LILY, (t - t2) / (t3 - t2), mood, living_night, mouth=talk("b", "LA", t), look=0.6)
    elif t < t4 - 0.03:
        char_ecu(ctx, t, MOM2, (t - t3) / (t4 - t3), dict(MOODS["angry"], flush=0.3), living_night, mouth=talk("b", "MO", t), look=0.2)
    else:
        ctx.save(); zoomed(ctx, 1.0 + 0.05 * (t - t4), 540, 1050)
        lana_room(ctx, t)
        rrect(ctx, 520, 1250, 560, 280, 30); fs(ctx, (0.25, 0.20, 0.32))
        draw_char(ctx, LILY_WET, dict(x=760, y=1420, s=1.3, mood="crying", lookY=0.8, armL=("ik", 15, -92, 1), armR=("ik", -8, -102, -1)), t)
        ctx.move_to(520, 1400); ctx.curve_to(700, 1330, 900, 1330, 1100, 1390); ctx.line_to(1100, 1920); ctx.line_to(520, 1920); ctx.close_path(); fs(ctx, (0.2, 0.15, 0.28))
        ctx.restore()
    vignette(ctx, 0.45)


# ---------- C: Zoe's test ----------
def c(ctx, t):
    t1, t2, tTxt, t3 = LS("c", 1), LS("c", 2), Wd("c", 2, 6), LS("c", 3)
    zbg = lambda c_, tt_: V.bedroom(c_, tt_, night=0.6)
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.05 * t, 640, 1050)
        lana_room(ctx, t)
        rrect(ctx, 400, 1250, 680, 280, 30); fs(ctx, (0.25, 0.20, 0.32))
        p = dict(x=700, y=1420, s=1.35, mood=dict(MOODS["hopeful"], tear=0.2), look=0.4, armL=("ik", -70, -330, 1))
        draw_char(ctx, REAL, p, t)
        hx, hy = hand_world(p, "L"); rrect(ctx, hx - 20, hy - 70, 40, 90, 8); fs(ctx, (0.1, 0.1, 0.12), 3)
        ctx.restore()
    elif t < t2 - 0.03:
        char_ecu(ctx, t, ZOE, (t - t1) / (t2 - t1), dict(MOODS["neutral"], bi=4, bo=-4, smile=0.0), zbg, mouth=talk("c", "Z", t), look=0.3,
                 armR=("ik", 95, -330, -1))
    elif t < t3 - 0.03:
        ctx.set_source_rgb(0.85, 0.87, 0.92); ctx.paint()
        text_bubble_phone(ctx, t, [("Okay. What did we bury in my backyard in 4th grade?", True, t2 - 1.0),
                                   ("A time capsule with the gold key!", False, tTxt),
                                   ("Wait... then who's calling me right now??", True, tTxt + 1.6)], title="Lily", s=2.2, y=1000)
    else:
        char_ecu(ctx, t, ZOE, (t - t3) / (DUR("c") - t3), dict(MOODS["cold"], eo=0.85), zbg, mouth=talk("c", "Z", t), look=0.3, armR=("ik", 95, -330, -1))
    vignette(ctx, 0.35)


# ---------- D: the academy ----------
def d(ctx, t):
    t1, t2, tID, t3, t4, t5, t6, t7 = LS("d", 1), LS("d", 2), Wd("d", 2, 4), LS("d", 3), LS("d", 4), LS("d", 5), LS("d", 6), LS("d", 7)
    if t < t1 - 0.03 or (t2 - 0.03 <= t < tID + 0.3):
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * (t % 6), 540, 1100)
        academy_ext(ctx, t)
        rx = lerp(1150, 720, sm(t / 3.0)) if t < t1 else 720
        draw_char(ctx, GUARD, dict(x=460, y=1560, s=1.5, legs=True, mood="cold", look=1, armL=("ik", 40, -105, 1), armR=("ik", -40, -110, -1)), t)
        pr = dict(x=rx, y=1570 + (6 * abs(sin(t * 10)) if t < 3 else 0), s=1.4, legs=True, mood="worried", look=-1)
        if t >= t2: pr["armL"] = ik(pr, 600, 1290, 1)
        draw_char(ctx, REAL, pr, t)
        if t >= t2:
            hx, hy = hand_world(pr, "L"); rrect(ctx, hx - 50, hy - 40, 100, 64, 6); fs(ctx, (1, 1, 1), 3)
        ctx.restore()
    elif t < t2 - 0.03:
        char_ecu(ctx, t, GUARD, (t - t1) / (t2 - t1), "cold", academy_ext, mouth=talk("d", "G", t), look=0.4)
    elif t < t3 - 0.03:
        ctx.set_source_rgb(0.3, 0.32, 0.4); ctx.paint()
        ctx.save(); ctx.translate(540, 900); ctx.rotate(-0.05); s_ = 1.0 + 0.04 * (t - tID)
        ctx.scale(s_, s_)
        rrect(ctx, -380, -240, 760, 480, 30); fs(ctx, (0.97, 0.97, 0.99), 6)
        ctx.rectangle(-380, -240, 760, 90); ctx.set_source_rgb(0.15, 0.3, 0.6); ctx.fill()
        text(ctx, "WESTBROOK HIGH · STUDENT ID", 0, -180, 32, col=(1, 1, 1))
        ctx.rectangle(-340, -120, 240, 300); ctx.set_source_rgb(0.8, 0.88, 0.95); ctx.fill()
        ctx.save(); ctx.rectangle(-340, -120, 240, 300); ctx.clip()
        draw_char(ctx, LILY, dict(x=-220, y=320, s=0.8, mood="happy", saccade=False), 0.3); ctx.restore()
        text(ctx, "LILY CARTER", 120, -40, 48, col=(0.1, 0.1, 0.15)); text(ctx, "Grade 11", 120, 20, 32, col=(0.4, 0.4, 0.45), weight=False)
        ctx.restore()
    elif t < t4 - 0.03:
        char_ecu(ctx, t, GUARD, (t - t3) / (t4 - t3), dict(MOODS["joy"], mo=0.2), academy_ext, mouth=talk("d", "G", t), look=0.4)
    elif t < t6 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.05 * (t - t4), 540, 1000)
        interview_room(ctx, t)
        draw_char(ctx, INTERV, dict(x=300, y=1500, s=1.4, glasses=True, mood=MT([(0, "neutral"), (t5 - 0.4, "happy")], t), look=0.8, mouth=talk("d", "I", t)), t)
        imp = dict(x=760, y=1500, s=1.4, mood="happy", look=-0.8, armL=ik(dict(x=760, y=1500, s=1.4), 560, 1240, 1))
        draw_char(ctx, LILY, imp, t)
        ctx.save(); ctx.translate(560, 1200); ctx.rotate(0.1); ctx.rectangle(-110, -150, 220, 180); fs(ctx, (1, 1, 1), 4)
        ctx.move_to(-80, -40); ctx.curve_to(-30, -130, 30, -130, 80, -40); st(ctx, (0.2, 0.2, 0.25), 4); ctx.restore()
        ctx.rectangle(-10, 1400, 1100, 600); fs(ctx, (0.45, 0.32, 0.22))
        ctx.restore()
        if t < t5:   # seen through the window
            ctx.set_source_rgb(0.95, 0.93, 0.88); ctx.rectangle(0, 0, 1080, 260); ctx.fill(); ctx.rectangle(0, 1560, 1080, 360); ctx.fill()
            ctx.rectangle(0, 0, 90, 1920); ctx.fill(); ctx.rectangle(990, 0, 90, 1920); ctx.fill()
            ctx.move_to(540, 260); ctx.line_to(540, 1560); ctx.move_to(90, 910); ctx.line_to(990, 910); st(ctx, (0.95, 0.93, 0.88), 18)
            ctx.rectangle(90, 260, 900, 1300); ctx.set_source_rgba(0.7, 0.85, 1.0, 0.12); ctx.fill()
    elif t < t7 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.05 * (t - t6), 540, 1100)
        academy_ext(ctx, t)
        ix = lerp(540, 330, sm((t - t6) / 2.0))
        draw_char(ctx, REAL, dict(x=760, y=1570, s=1.4, legs=True, mood=dict(MOODS["crying"], tremble=0.3), look=-1), t)
        draw_char(ctx, LILY, dict(x=ix, y=1570, s=1.4, legs=True, mood=dict(MOODS["smirk"], eo=0.8), look=1, tilt=0.06), t)
        ctx.restore()
    else:
        char_ecu(ctx, t, LILY, (t - t7) / (DUR("d") - t7), dict(MOODS["smirk"], eo=0.7), academy_ext, mouth=talk("d", "LA", t), look=0.9, tilt=0.08)
    vignette(ctx, 0.35)


# ---------- E: the notebook ----------
def e(ctx, t):
    t1, t2, t3, t4 = LS("e", 1), LS("e", 2), LS("e", 3), LS("e", 4)
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.05 * t, 540, 1150)
        lana_room(ctx, t)
        lift = ramp(t, 1.8, 2.6)
        ctx.save(); ctx.translate(200, 1420); ctx.rotate(-0.25 * lift)
        rrect(ctx, 0, -80, 840, 100, 20); fs(ctx, (0.35, 0.28, 0.45)); ctx.restore()
        rrect(ctx, 180, 1420, 880, 200, 10); fs(ctx, (0.3, 0.2, 0.15))
        if lift > 0.5:
            ctx.save(); ctx.translate(560, 1400); ctx.rotate(0.1); rrect(ctx, -90, -60, 180, 120, 8); fs(ctx, (0.15, 0.15, 0.2)); ctx.restore()
            glow(ctx, 560, 1400, 220, (1, 1, 0.8), 0.3 * lift)
        draw_char(ctx, REAL, dict(x=330, y=1560, s=1.35, legs=True, mood=MT([(0, "worried"), (2.4, "shock")], t), look=0.8, lookY=0.7,
                                  armR=ik(dict(x=330, y=1560, s=1.35), 450, 1400, -1)), t)
        ctx.restore()
        overlay(ctx, (0.0, 0.0, 0.1), 0.25)
    else:
        lines = [("Day 1: practice her handwriting.", (0.15, 0.15, 0.45), Wd("e", 1, 0)),
                 ("Day 20: learn her passwords.", (0.15, 0.15, 0.45), Wd("e", 1, 5)),
                 ("Day 47: she still doesn't suspect", (0.15, 0.15, 0.45), Wd("e", 1, 10)),
                 ("a thing.", (0.15, 0.15, 0.45), Wd("e", 1, 10) + 0.4)]
        if t >= t2 - 0.03:
            lines = [("how she laughs", (0.15, 0.15, 0.45), t2 + 1.4), ("how she ties her shoes", (0.15, 0.15, 0.45), t2 + 3.0),
                     ("how she holds her ...", (0.15, 0.15, 0.45), t2 + 4.4)]
        if t >= t4 - 0.03:
            lines = [("Day 60:", (0.15, 0.15, 0.45), t4), ("BECOME LILY.", (0.85, 0.1, 0.1), Wd("e", 4, 2)), ("FOREVER.", (0.85, 0.1, 0.1), Wd("e", 4, 4))]
        notebook_cu(ctx, t, (t - t1) / 15, lines=lines, torn=(t3 - 0.03 <= t < t4 - 0.03) or t >= t4, photos=(t2 - 0.03 <= t < t4 - 0.03))
        if t3 - 0.03 <= t < t4 - 0.03:
            V.flash(ctx, t, t3 + 0.6, (1, 0.3, 0.3), 0.25, 0.3)
    vignette(ctx, 0.45)


# ---------- F: last page ----------
def f(ctx, t):
    t1 = LS("f", 1)
    tEnd = LE("f", 1) + 0.35
    if t < t1 - 0.03:
        char_ecu(ctx, t, REAL, t / t1, "shock", lambda c_, tt_: lana_room(c_, tt_), dark=0.25, lookY=0.8)
    else:
        lines = [("Day 61:", (0.15, 0.15, 0.45), t1), ("Make sure the real Lily", (0.85, 0.1, 0.1), Wd("f", 1, 2)), ("DISAPPEARS.", (0.85, 0.1, 0.1), Wd("f", 1, 7))]
        notebook_cu(ctx, t, (t - t1) / 3, lines=lines, photos=False)
        sh = ramp(t, Wd("f", 1, 7) + 0.3, Wd("f", 1, 7) + 1.2)
        if sh > 0:
            ctx.save(); ctx.push_group()
            ell(ctx, 900, 700, 200, 240); rrect(ctx, 700, 880, 400, 1100, 120); ctx.set_source_rgb(0, 0, 0); ctx.fill()
            ctx.pop_group_to_source(); ctx.paint_with_alpha(0.55 * sh); ctx.restore()
    vignette(ctx, 0.55)
    end_card(ctx, t, tEnd, "PART 3 · FINAL", [("FOLLOW so you don't miss it", 56, (1, 1, 1)), ("What does 'disappear' mean?", 48, (1, 0.86, 0.15))])


SCENES = {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f}
V.SCENES = SCENES

if __name__ == "__main__":
    os.makedirs(f"{EP}/preview", exist_ok=True)
    if sys.argv[1] == "preview":
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        for arg in sys.argv[2:]:
            sc, ts = arg.split(":"); V.frame(surf, sc, float(ts)); surf.write_to_png(f"{EP}/preview/{sc}_{ts}.png")
    else:
        for sc in (sys.argv[2:] or SCENES.keys()): V.render(sc)
