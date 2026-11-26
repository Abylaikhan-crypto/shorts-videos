"""My Stepdad Is a Cop — Part 2. python part2.py preview a:1.0 ... | render [scenes]"""
import json, os, sys, cairo
from math import sin, cos, pi
from rig import *
import part1 as P1
import part1v2 as V
from part1 import MAYA, DALE, MOM, ALV, ik
from ep_common import *

HERE = os.path.dirname(os.path.abspath(__file__))
EP = f"{HERE}/p2"
TL = {s["id"]: s for s in json.load(open(f"{EP}/timeline.json"))}
V.TL = TL; V.EP = EP
P1.HEADER[:] = ["MY STEPDAD IS A COP", "PART 2"]
P1.HL.update({"MO": (1, 0.6, 0.8), "M": (0.45, 0.85, 1.0)})
MT = mood_at
talk = V.talk


def LS(sc, i): return TL[sc]["lines"][i]["start"]
def LE(sc, i): l = TL[sc]["lines"][i]; return l["start"] + l["dur"]
def Wd(sc, i, j): return TL[sc]["lines"][i]["words"][j][1]
def DUR(sc): return TL[sc]["dur"]


def zoomed(ctx, z, cx=540, cy=960):
    ctx.translate(540, 960); ctx.scale(z, z); ctx.translate(-cx, -cy)


# ---------- A: recap ----------
def a(ctx, t):
    t1, tWas = LS("a", 1), Wd("a", 1, 8)
    if t < t1 - 0.03:
        V.maya_ecu(ctx, t, t / t1, "hopeful", bg=lambda c_, tt_: P1.office_bg(c_, tt_), dark=0.0, look=-0.4)
    elif t < tWas - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.2 * sm((t - t1) / (tWas - t1)), 540, 1000)
        P1.doorway(ctx, t, ramp(t, t1, t1 + 1.2)); ctx.restore()
    else:
        ctx.save(); zoomed(ctx, 1.0 + 0.06 * (t - tWas))
        gr = cairo.RadialGradient(540, 900, 50, 540, 900, 900); gr.add_color_stop_rgb(0, 1, 1, 0.95); gr.add_color_stop_rgb(1, 0.75, 0.70, 0.62)
        ctx.set_source(gr); ctx.paint()
        draw_char(ctx, DALE, dict(x=540, y=1960, s=2.6, hat=True, mood="smirk", glint=True, shadow=0.15, saccade=False), t)
        ctx.restore()
        V.flash(ctx, t, tWas, (1, 0.25, 0.2), 0.4, 0.7)
    vignette(ctx, 0.45)


# ---------- B: Dale charms the counselor; the card ----------
def b(ctx, t):
    t1, t2, tAcc, t3, t4, tSl, t5 = LS("b", 1), LS("b", 2), Wd("b", 2, 2), LS("b", 3), LS("b", 4), Wd("b", 4, 9), LS("b", 5)
    if tSl - 0.05 <= t < t5 - 0.03:
        card_insert(ctx, t, (t - tSl) / (t5 - tSl)); vignette(ctx, 0.45); return
    keys = [(0, 600, 1000, 1.12), (t1 - 0.05, 650, 990, 1.22), (t1 - 0.03, 280, 1000, 1.95, "cut"), (t2 - 0.05, 280, 1000, 2.05),
            (t2 - 0.03, 880, 950, 2.0, "cut"), (t3 - 0.05, 880, 950, 2.2), (t3 - 0.03, 280, 1000, 2.0, "cut"), (t4 - 0.05, 280, 1000, 2.1),
            (t4 - 0.03, 600, 1000, 1.12, "cut"), (tSl, 620, 1000, 1.18), (t5 - 0.03, 300, 1000, 2.0, "cut"), (DUR("b"), 300, 1000, 2.12)]
    cx, cy, z = cam(keys, t)
    ctx.save(); apply_cam(ctx, cx, cy, z)
    P1.office_bg(ctx, t)
    alv = dict(x=280, y=1460, s=1.32, glasses=True, look=0.9, blink=blinking(t, 4), mouth=talk("b", "A", t),
               mood=MT([(0, "worried"), (t1, dict(MOODS["worried"], bi=2, bo=-2)), (t3, "scared"), (t5, dict(MOODS["worried"], smile=0.2))], t))
    if t >= t3: alv.update(lookY=0.8, look=0.6)
    if t >= t5: alv.update(look=1, lookY=0.2)
    alv["armL"] = ik(alv, 235, 1392, 1); alv["armR"] = ik(alv, 330, 1392, -1)
    maya = dict(x=620, y=1480, s=1.12, look=-0.2, lookY=1, blink=blinking(t, 1),
                mood=MT([(0, "sad"), (t2, "scared"), (t5, "hopeful")], t), armL=("ik", 15, -92, 1), armR=("ik", -8, -102, -1))
    signing = t4 <= t
    dale = dict(x=890, y=1500, s=1.5, hat=True, blink=blinking(t, 2), mouth=talk("b", "D", t), look=-0.8,
                mood=MT([(0, "happy"), (t2, "smirk"), (tAcc - 0.1, "cold"), (t4, "neutral")], t))
    if signing:
        dale.update(look=0.6, lookY=1.0)
        dale["armR"] = ik(dale, 990, 1320, -1); dale["armL"] = ik(dale, 960, 1300, 1)
    else:
        dale["armL"] = ("ang", -0.4 - 0.3 * sin(t * 2.5) * min(1, talk("b", "D", t) * 4), -1.8)
    draw_char(ctx, ALV, alv, t); draw_char(ctx, MAYA, maya, t); draw_char(ctx, DALE, dale, t)
    if signing:
        ctx.save(); ctx.translate(985, 1300); ctx.rotate(0.2)
        rrect(ctx, -60, -80, 120, 160, 8); fs(ctx, (0.6, 0.45, 0.3)); ctx.rectangle(-48, -62, 96, 128); fs(ctx, (1, 1, 1), 3)
        ctx.restore()
    P1.desk(ctx)
    ctx.restore()
    vignette(ctx, 0.35)


# ---------- C: the car ride ----------
def c(ctx, t):
    t1, t2, t3 = LS("c", 1), LS("c", 2), LS("c", 3)
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.05 * t)
        car_interior(ctx, t)
        draw_char(ctx, MAYA, dict(x=790, y=1470, s=1.05, mood="sad", look=-0.3, lookY=0.8, blink=blinking(t, 1), armL=("ik", 15, -92, 1), armR=("ik", -8, -102, -1)), t)
        rrect(ctx, 640, 1250, 400, 300, 40); fs(ctx, (0.18, 0.18, 0.24))
        draw_char(ctx, DALE, dict(x=320, y=1560, s=1.5, mood="cold", look=-0.2, lookY=-0.6, blink=blinking(t, 2),
                                  armL=("ik", -40, -110, 1), armR=("ik", 60, -110, -1)), t)
        car_front(ctx)
        ctx.restore()
    elif t < t2 - 0.03:
        ctx.set_source_rgb(0.04, 0.05, 0.09); ctx.paint()
        tt = (t - t1) / (t2 - t1); z = 1.0 + 0.08 * tt
        ctx.save(); zoomed(ctx, z)
        rrect(ctx, 40, 640, 1000, 420, 60); fs(ctx, (0.14, 0.15, 0.2), 14)
        ctx.save(); rrect(ctx, 70, 670, 940, 360, 40); ctx.clip()
        ctx.set_source_rgb(0.12, 0.15, 0.25); ctx.paint()
        draw_char(ctx, DALE, dict(x=540, y=2050, s=4.0, mood="cold", look=0.3, lookY=-0.2, saccade=False, blink=blinking(t, 2), shadow=0.35), t)
        glow(ctx, lerp(1200, -100, (t * 0.45) % 1), 800, 400, (1, 0.75, 0.4), 0.2)
        ctx.restore()
        ctx.restore()
    elif t < t3 - 0.03:
        ctx.save(); zoomed(ctx, 1.05)
        car_interior(ctx, t)
        draw_char(ctx, DALE, dict(x=420, y=1800, s=2.3, mood="angry", look=0.8, lookY=0.2, mouth=talk("c", "D", t), saccade=False,
                                  armR=("ang", 1.3, 1.0)), t)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ell(ctx, 760, 1320, 120, 90, -0.3); fs(ctx, DALE["skin"], 6)
        for k in range(4):
            x0 = 700 + k * 45; ctx.move_to(x0, 1260); ctx.line_to(x0 + 30, 1150 - 10 * (k % 2)); st(ctx, OUTL, 52)
            ctx.move_to(x0, 1260); ctx.line_to(x0 + 30, 1150 - 10 * (k % 2)); st(ctx, DALE["skin"], 40)
        ctx.restore()
    else:
        V.maya_ecu(ctx, t, (t - t3) / (DUR("c") - t3), "crying", bg=lambda c_, tt_: car_interior(c_, tt_), dark=0.3, look=-0.4)
        old_phone(ctx, 300, 1500, 1.4, t, rot=0.3)
    V.rain(ctx, t, 0.18)
    overlay(ctx, (0.0, 0.03, 0.15), 0.18)
    vignette(ctx, 0.55)


# ---------- D: Mom at the door; laughter at night; decision ----------
def d(ctx, t):
    t1, t2, t3 = LS("d", 1), LS("d", 2), LS("d", 3)
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.05 * t, 540, 1000)
        porch(ctx, t)
        draw_char(ctx, MOM, dict(x=545, y=1265, s=1.5, legs=True, mood="worried", look=0.6, blink=blinking(t, 3),
                                 armL=("ik", -10, -120, 1), armR=("ik", 10, -120, -1)), t)
        mx = lerp(1300, 760, sm(t / 2.6))
        draw_char(ctx, MAYA, dict(x=mx, y=1480 + 10 * abs(sin(t * 12)) * (1 - sm(t / 2.6)), s=1.3, legs=True, mood="crying", look=-1), t)
        ctx.restore()
        overlay(ctx, (0.0, 0.03, 0.15), 0.15)
    elif t < t2 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.05 * (t - t1))
        porch(ctx, t)
        mom = dict(x=470, y=1900, s=2.4, mood=dict(MOODS["worried"], tear=0.7), look=0.9, mouth=talk("d", "MO", t), blink=False)
        mom["look"] = 0.9 if (t - t1) % 2.2 < 1.4 else -0.9
        draw_char(ctx, MOM, mom, t)
        draw_char(ctx, MAYA, dict(x=780, y=2050, s=2.2, mood="crying", look=-0.8, lookY=-0.3), t)
        ctx.restore()
    else:
        tAway = t3
        if t < t3 - 0.03:
            ctx.save(); zoomed(ctx, 1.0 + 0.03 * (t - t2), 540, 1000)
            V.bedroom(ctx, t, night=1.0)
            ctx.rectangle(80, 640, 360, 870); fs(ctx, (0.20, 0.16, 0.24)); ctx.rectangle(80, 640, 360, 870); st(ctx, (0.30, 0.22, 0.20), 14)
            ctx.rectangle(84, 1500, 352, 14); ctx.set_source_rgb(1, 0.82, 0.48); ctx.fill()
            glow(ctx, 260, 1514, 260, (1, 0.8, 0.45), 0.35)
            xx = 200 + 120 * sin(t * 0.8)
            ctx.rectangle(xx - 30, 1500, 60, 14); ctx.set_source_rgba(0.08, 0.06, 0.08, 0.95); ctx.fill()
            ctx.rectangle(-10, 1514, 1100, 420); ctx.set_source_rgb(0.12, 0.10, 0.14); ctx.fill()
            rrect(ctx, 600, 1020, 470, 500, 30); fs(ctx, (0.30, 0.22, 0.20))
            draw_char(ctx, MAYA, dict(x=830, y=1430, s=1.2, mood=dict(MOODS["sad"], tear=0.6), look=-1, lookY=0.1, dark=0.25,
                                      armL=("ik", 15, -92, 1), armR=("ik", -8, -102, -1)), t)
            ctx.move_to(560, 1400); ctx.curve_to(700, 1300, 950, 1300, 1100, 1380); ctx.line_to(1100, 1920); ctx.line_to(560, 1920); ctx.close_path()
            fs(ctx, (0.30, 0.25, 0.45))
            ctx.restore()
            overlay(ctx, (0.0, 0.03, 0.16), 0.2)
        else:
            def moon_bg(c_, tt_):
                c_.set_source_rgb(0.08, 0.09, 0.2); c_.paint(); glow(c_, 850, 500, 600, (0.6, 0.7, 1.0), 0.3)
            V.maya_ecu(ctx, t, (t - t3) / (DUR("d") - t3), MT([(t3, dict(MOODS["sad"], tear=0.5)), (Wd("d", 3, 4), DETERMINED)], t, 0.6),
                       bg=moon_bg, dark=0.2)
            overlay(ctx, (0.3, 0.4, 0.8), 0.06, ADD)
    vignette(ctx, 0.55)


# ---------- E: the old phone ----------
def e(ctx, t):
    t1, t2 = LS("e", 1), LS("e", 2)
    if t < t1 - 0.03:
        ctx.set_source_rgb(0.18, 0.15, 0.22); ctx.paint()
        ctx.rectangle(0, 1100, 1080, 900); ctx.set_source_rgb(0.30, 0.24, 0.24); ctx.fill()
        ctx.save(); zoomed(ctx, 1.0 + 0.08 * t / t1); ctx.translate(0, -300)
        rrect(ctx, 200, 1000, 680, 380, 10); fs(ctx, (0.85, 0.75, 0.6))
        ctx.rectangle(230, 1030, 620, 320); ctx.set_source_rgb(0.95, 0.9, 0.82); ctx.fill()
        old_phone(ctx, 540, 1190, 1.0, t, rot=1.45)
        lid = ramp(t, 0.3, 1.2)
        ctx.save(); ctx.translate(200, 1000); ctx.rotate(-1.3 * lid)
        rrect(ctx, 0, -60 * (1 - lid), 680, 70 + 60 * (1 - lid) if lid < 0.99 else 70, 10); fs(ctx, (0.80, 0.68, 0.52)); ctx.restore()
        ctx.restore()
        glow(ctx, 540, 890, 300, (1, 0.95, 0.8), 0.2 * lid)
    elif t < t2 - 0.03:
        ctx.set_source_rgb(0.08, 0.08, 0.14); ctx.paint()
        old_phone(ctx, 540, 900, 4.0 + 0.3 * (t - t1) / (t2 - t1), t)
    else:
        def tent(c_, tt_):
            c_.set_source_rgb(0.03, 0.03, 0.06); c_.paint()
            c_.move_to(-100, 1920); c_.curve_to(-100, 200, 1180, 200, 1180, 1920); c_.close_path(); c_.set_source_rgb(0.20, 0.15, 0.32); c_.fill()
        V.maya_ecu(ctx, t, (t - t2) / (DUR("e") - t2), DETERMINED, bg=tent, dark=0.35, lookY=0.8)
        rec = (t - t2) % 2.4 > 1.2
        old_phone(ctx, 540, 1640, 1.8, t, rec_t0=(t2 if rec else None))
        glow(ctx, 540, 1500, 700, (0.4, 0.6, 1.0), 0.35)
    vignette(ctx, 0.55)


# ---------- F: the fight, recorded ----------
def f(ctx, t):
    tHid, tRec, t1, tHer, t2, t3 = Wd("f", 0, 9), Wd("f", 0, 19), LS("f", 1), Wd("f", 1, 18), LS("f", 2), LS("f", 3)
    if t < tHid - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * t, 540, 1000)
        kitchen_set(ctx, t)
        mom = dict(x=280, y=1450, s=1.3, legs=True, mood="scared", look=0.8, blink=blinking(t, 3), armL=("ik", -10, -120, 1), armR=("ik", 10, -120, -1))
        draw_char(ctx, MOM, mom, t)
        dale = dict(x=640, y=1470, s=1.55, legs=True, mood="angry", look=-1, mouth=0.4 + 0.3 * abs(sin(t * 7)), blink=False,
                    armR=("ang", 2.0 + 0.2 * sin(t * 6), 2.4))
        draw_char(ctx, DALE, dale, t)
        ctx.restore()
    elif t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.03 * (t - tHid))
        shelf_cu(ctx, t, rec_t0=tRec, low=False)
        hx = lerp(1300, 760, ramp(t, tHid, tHid + 0.8)) if t < tRec + 0.4 else lerp(760, 1300, ramp(t, tRec + 0.4, tRec + 1.0))
        ctx.move_to(1500, 1240); ctx.line_to(hx + 60, 960); st(ctx, OUTL, 160); ctx.move_to(1500, 1240); ctx.line_to(hx + 60, 960); st(ctx, MAYA["top"], 148)
        ell(ctx, hx, 940, 70, 60); fs(ctx, MAYA["skin"], 6)
        ctx.restore()
    elif t < t2 - 0.03:
        V.dale_ecu(ctx, t, "f", (t - t1) / (t2 - t1), dict(MOODS["angry"], flush=0.8))
        overlay(ctx, (0.0, 0.03, 0.15), 0.12)
    elif t < t3 - 0.03:
        def kbg(c_, tt_): kitchen_set(c_, tt_)
        ctx.save(); zoomed(ctx, 1.0 + 0.05 * (t - t2))
        kitchen_set(ctx, t)
        draw_char(ctx, MOM, dict(x=540, y=1920, s=2.4, mood="crying", look=0.5, mouth=talk("f", "MO", t)), t)
        ctx.restore()
    else:
        def hall(c_, tt_): P1.hallway(c_, tt_)
        V.maya_ecu(ctx, t, (t - t3) / (DUR("f") - t3), dict(MOODS["scared"], tremble=1.0, tear=0.4), bg=hall, dark=0.25, look=-0.7)
        overlay(ctx, (0.0, 0.03, 0.15), 0.15)
    vignette(ctx, 0.55)


# ---------- G: the beep ----------
def g(ctx, t):
    tBeep, t2, t3 = Wd("g", 1, 4), LS("g", 2), LS("g", 3)
    if t < t2 - 0.03:
        pop = back_out((t - tBeep) / 0.25) if t >= tBeep else 0
        ctx.save(); zoomed(ctx, 1.25 + 0.15 * sm(t / t2), 560, 900)
        shelf_cu(ctx, t, rec_t0=-160, low=True, popup=pop, shake=1 - ramp(t, tBeep, tBeep + 0.5) if t >= tBeep else 0)
        ctx.restore()
        if t >= tBeep: V.flash(ctx, t, tBeep, (0.6, 0.8, 1), 0.2, 0.4)
    elif t < t3 - 0.03:
        V.dale_ecu(ctx, t, "g", (t - t2) / (t3 - t2), "cold")
    else:
        ctx.save(); zoomed(ctx, 1.0 + 0.1 * sm((t - t3) / 2.5), 700, 1000)
        kitchen_set(ctx, t)
        draw_char(ctx, MOM, dict(x=280, y=1450, s=1.3, legs=True, mood="shock", look=0.9), t)
        dx = lerp(560, 760, sm((t - t3) / 2.4))
        draw_char(ctx, DALE, dict(x=dx, y=1470 + 6 * abs(sin(t * 6)), s=1.55, legs=True, mood="cold", look=1, lookY=-0.3, shadow=0.3), t)
        ctx.restore()
    beat = t % 0.8
    vignette(ctx, 0.6 + 0.15 * (sm(1 - beat / 0.15) if beat < 0.15 else 0))


# ---------- H: inches away ----------
def h(ctx, t):
    tEnd = LE("h", 0) + 0.35
    ctx.save(); zoomed(ctx, 1.2 + 0.25 * sm(t / tEnd), 560, 860)
    shelf_cu(ctx, t, hand_u=ramp(t, 0.0, tEnd) * 0.75, rec_t0=-170, low=True)
    ctx.restore()
    vignette(ctx, 0.65)
    end_card(ctx, t, tEnd, "PART 3 · FINAL", [("FOLLOW so you don't miss it", 56, (1, 1, 1)), ("Will he find the phone?", 50, (1, 0.86, 0.15))])


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
