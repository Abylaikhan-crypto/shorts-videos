"""My Stepdad Is a Cop — Part 3 (final). python part3.py preview a:1.0 ... | render [scenes]"""
import json, os, sys, cairo, random
from math import sin, cos, pi
from rig import *
import part1 as P1
import part1v2 as V
from part1 import MAYA, DALE, MOM, ALV, ik
from ep_common import *

HERE = os.path.dirname(os.path.abspath(__file__))
EP = f"{HERE}/p3"
TL = {s["id"]: s for s in json.load(open(f"{EP}/timeline.json"))}
V.TL = TL; V.EP = EP
P1.HEADER[:] = ["MY STEPDAD IS A COP", "FINAL PART"]
P1.HL.update({"MO": (1, 0.6, 0.8), "M": (0.45, 0.85, 1.0), "P": (0.8, 0.7, 1.0), "X": (0.5, 0.9, 1.0)})
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
    ctx.save(); zoomed(ctx, 1.2 + 0.25 * sm(t / DUR("a")), 560, 860)
    shelf_cu(ctx, t, hand_u=0.55 + 0.2 * sm(t / DUR("a")), rec_t0=-170, low=True)
    ctx.restore()
    vignette(ctx, 0.65)


# ---------- B: the plate ----------
def b(ctx, t):
    tC = LS("b", 0) + 2.85
    t2, t3, t4, tMe, tFirst, tProt = LS("b", 2), LS("b", 3), LS("b", 4), Wd("b", 4, 5), Wd("b", 4, 10), Wd("b", 4, 17)
    if t < tC - 0.02:
        ctx.save(); zoomed(ctx, 1.45 + 0.1 * sm(t / tC), 560, 860)
        shelf_cu(ctx, t, hand_u=0.75 + 0.07 * sm(t / tC), rec_t0=-175, low=True)
        ctx.restore()
    elif t < t2 - 0.03:
        tt = t - tC
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * tt, 540, 1050)
        kitchen_set(ctx, t)
        mom = dict(x=290, y=1450, s=1.3, legs=True, mood=MT([(tC, "shock"), (tC + 0.8, BRAVE_MOM)], t), look=0.9,
                   armL=("ang", -0.5, -0.9), armR=("ang", 0.5, 0.9))
        draw_char(ctx, MOM, mom, t)
        turn = ramp(tt, 0.1, 0.4)
        draw_char(ctx, DALE, dict(x=820, y=1470, s=1.55, legs=True, mood=MT([(tC, "shock"), (tC + 0.4, "angry")], t), look=lerp(1, -1, turn),
                                  flinch=1 - ramp(tt, 0, 0.3), armR=ik(dict(x=820, y=1470, s=1.55), lerp(980, 900, turn), lerp(900, 1250, turn), -1)), t)
        rs = random.Random(3)
        for k in range(16):
            ang = rs.uniform(-pi, 0); sp = rs.uniform(300, 900)
            px = 330 + cos(ang) * sp * min(tt, 0.5); py = 1760 + sin(ang) * sp * min(tt, 0.5) + 900 * min(tt, 0.5) ** 2
            ctx.save(); ctx.translate(px, min(py, 1790)); ctx.rotate(tt * 8 + k)
            poly(ctx, [(-18, -8), (14, -12), (6, 12)]); fs(ctx, (0.97, 0.97, 0.97), 3); ctx.restore()
        ctx.restore()
        V.flash(ctx, t, tC, (1, 1, 1), 0.15, 0.6)
    elif t < t3 - 0.03:
        V.dale_ecu(ctx, t, "b", (t - t2) / (t3 - t2), dict(MOODS["angry"], flush=0.8))
    elif t < tFirst - 0.05:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * (t - t3))
        kitchen_set(ctx, t)
        mom = dict(x=540, y=1920, s=2.4, mouth=talk("b", "MO", t), saccade=False, mood=BRAVE_MOM,
                   look=-0.8 if t < Wd("b", 3, 3) else 0.9, lookY=0.1)
        if t >= tMe - 0.1: mom.update(look=0.0, lookY=0.0, mood=dict(BRAVE_MOM, smile=0.15), tilt=0.06 * sin((t - tMe) * 6) * (1 - ramp(t, tMe + 0.5, tMe + 1.0)))
        draw_char(ctx, MOM, mom, t)
        ctx.restore()
    elif t < tProt - 0.05:
        V.maya_ecu(ctx, t, (t - tFirst) / (tProt - tFirst), MT([(tFirst, "shock"), (tFirst + 0.6, dict(DETERMINED, tear=0.5))], t),
                   bg=lambda c_, tt_: P1.hallway(c_, tt_), dark=0.2, look=-0.3)
    else:
        ctx.save(); zoomed(ctx, 1.45, 560, 860)
        shelf_cu(ctx, t, rec_t0=-180, low=True)
        hx = lerp(1300, 600, ramp(t, tProt, tProt + 0.35))
        ctx.restore()
        ctx.save(); zoomed(ctx, 1.45, 560, 860); ctx.translate(0, -260)
        ctx.move_to(1500, 1500); ctx.line_to(hx + 60, 1200); st(ctx, OUTL, 160); ctx.move_to(1500, 1500); ctx.line_to(hx + 60, 1200); st(ctx, MAYA["top"], 148)
        ell(ctx, hx, 1180, 70, 60); fs(ctx, MAYA["skin"], 6)
        ctx.restore()
    vignette(ctx, 0.55)


# ---------- C: running through the rain ----------
def night_street(ctx, t, speed=900):
    ctx.set_source_rgb(0.05, 0.06, 0.12); ctx.paint()
    off = (t * speed * 0.3) % 600
    for i in range(-1, 4):
        x = i * 600 - off
        poly(ctx, [(x + 40, 900), (x + 280, 720), (x + 520, 900)]); ctx.set_source_rgb(0.08, 0.08, 0.15); ctx.fill()
        ctx.rectangle(x + 80, 900, 400, 420); ctx.set_source_rgb(0.10, 0.10, 0.18); ctx.fill()
        ctx.rectangle(x + 140, 980, 90, 80); ctx.set_source_rgb(1, 0.8, 0.45); ctx.fill()
        glow(ctx, x + 185, 1020, 160, (1, 0.8, 0.45), 0.25)
    ctx.rectangle(0, 1320, 1080, 700); ctx.set_source_rgb(0.08, 0.12, 0.10); ctx.fill()


def fence(ctx, t, speed=900):
    off = (t * speed) % 120
    for i in range(-1, 11):
        x = i * 120 - off
        poly(ctx, [(x, 1460), (x + 30, 1420), (x + 60, 1460), (x + 60, 1920), (x, 1920)]); fs(ctx, (0.22, 0.20, 0.25), 4)
    ctx.rectangle(-10, 1520, 1100, 26); fs(ctx, (0.22, 0.20, 0.25), 4)


def c(ctx, t):
    t1, tHear, t2, t3 = LS("c", 1), Wd("c", 1, 6), LS("c", 2), LS("c", 3)
    lightning = 1 - ramp(t, t1, t1 + 0.6) if t >= t1 else 0
    if t < tHear - 0.05:
        ctx.save(); zoomed(ctx, 1.05)
        night_street(ctx, t)
        bob = 12 * abs(sin(t * 9))
        maya = dict(x=560, y=1520 - bob, s=1.35, mood=dict(MOODS["scared"], mo=0.5, bi=2, bo=-2, tremble=0), look=0.9, tilt=0.12,
                    armL=("ang", 0.8 + 0.6 * sin(t * 9), 2.2), armR=("ik", 20, -150, -1))
        MAYA_WET = dict(MAYA, hair=shade(MAYA["hair"], 0.35))
        draw_char(ctx, MAYA_WET, maya, t)
        old_phone(ctx, 560 + 20 * 1.35, 1520 - bob - 150 * 1.35, 0.55, t, rot=0.4)
        fence(ctx, t)
        ctx.restore()
    elif t < t3 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.1 * sm((t - tHear) / (t3 - tHear)), 540, 1000)
        P1.doorway(ctx, t, 1.0, dark=0.92)
        ctx.restore()
        overlay(ctx, (0.0, 0.02, 0.1), 0.45)
        if t >= t2:
            draw_char(ctx, DALE, dict(x=540, y=1960, s=2.4, mood=dict(MOODS["angry"], flush=0.6), mouth=talk("c", "D", t) + 0.2, dark=0.45, shadow=0.4), t)
    else:
        ctx.save(); zoomed(ctx, 1.0 + 0.05 * (t - t3), 540, 1000)
        porch(ctx, t, inside=(0.55, 0.20, 0.22))
        porch_front(ctx, 0.0)
        knock = abs(sin((t - t3 - 2.6) * 11)) if t > t3 + 2.6 and t < t3 + 3.4 else 0
        draw_char(ctx, dict(MAYA, hair=shade(MAYA["hair"], 0.35)), dict(x=820, y=1500, s=1.35, legs=True, mood=dict(MOODS["crying"], mo=0.3), look=-0.8,
                                   armL=("ik", -150 - 20 * knock, -260, 1), armR=("ik", 0, -140, -1)), t)
        ctx.restore()
    if lightning > 0: overlay(ctx, (0.85, 0.9, 1), 0.7 * lightning, ADD)
    V.rain(ctx, t, 0.45)
    overlay(ctx, (0.0, 0.03, 0.15), 0.18)
    vignette(ctx, 0.55)


# ---------- D: Mrs. Patterson ----------
def d(ctx, t):
    t1, tDial, t2 = LS("d", 1), Wd("d", 1, 17), LS("d", 2)
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * t, 540, 1000)
        porch(ctx, t, inside=(1, 0.88, 0.62))
        draw_char(ctx, PATT, dict(x=545, y=1265, s=1.45, legs=True, glasses=True, mood="shock", mouth=talk("d", "P", t), look=0.6,
                                  armL=("ik", -40, -200, 1), armR=("ik", 120, -60, -1)), t)
        draw_char(ctx, dict(MAYA, hair=shade(MAYA["hair"], 0.35)), dict(x=840, y=1560, s=1.35, legs=True, mood="crying", look=-0.9), t)
        ctx.restore()
        V.rain(ctx, t, 0.25)
    elif t < t2 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.03 * (t - t1))
        V.living_room(ctx, t)
        draw_char(ctx, MAYA, dict(x=330, y=1470, s=1.25, mood=dict(MOODS["sad"], tear=0.6), look=0.8, lookY=0.6), t)
        ctx.move_to(170, 1150); ctx.curve_to(240, 1050, 430, 1050, 490, 1150); ctx.line_to(520, 1500); ctx.line_to(140, 1500); ctx.close_path()
        fs(ctx, (0.55, 0.62, 0.8))
        patt = dict(x=760, y=1470, s=1.3, glasses=True, look=-0.6, lookY=0.7, mood=MT([(t1, "worried"), (t1 + 1.6, "shock"), (tDial - 0.6, DETERMINED)], t),
                    tremble=0.4 if t > tDial - 1.5 else 0)
        lift = ramp(t, tDial - 0.4, tDial + 0.2)
        patt["armR"] = ik(patt, lerp(880, 870, lift), lerp(1420, 1050, lift), -1)
        draw_char(ctx, PATT, patt, t)
        V.couch_front(ctx)
        rrect(ctx, 300, 1560, 520, 200, 20); fs(ctx, (0.55, 0.38, 0.25))
        old_phone(ctx, 470, 1600, 0.75, t, rec_t0=t1 - 330, rot=1.5)
        for k in range(5):
            r = ((t * 1.2 + k * 0.2) % 1) * 160
            ctx.new_path(); ctx.arc(470, 1560, 60 + r, -2.4, -0.7); ctx.set_source_rgba(1, 0.9, 0.6, 0.6 * (1 - r / 160)); ctx.set_line_width(6); ctx.stroke()
        ctx.save(); ctx.translate(640, 1640); ctx.rotate(-0.1); rrect(ctx, -70, -40, 140, 80, 6); fs(ctx, (1, 1, 1), 3)
        text(ctx, "MS. R. ALVAREZ", 0, -5, 15, col=(0.15, 0.2, 0.35)); text(ctx, "(555) 014-2209", 0, 20, 15, col=(0.85, 0.15, 0.15)); ctx.restore()
        ctx.restore()
    else:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * (t - t2))
        V.living_room(ctx, t)
        patt = dict(x=520, y=1880, s=2.3, glasses=True, look=0.2, mood=DETERMINED, mouth=talk("d", "P", t), saccade=False)
        patt["armR"] = ("ik", 118, -300, -1)
        draw_char(ctx, PATT, patt, t)
        hx, hy = 520 + 2.3 * 118, 1880 - 2.3 * 300
        ctx.save(); ctx.translate(hx + 10, hy - 40); ctx.rotate(-1.35); rrect(ctx, -120, -24, 240, 48, 22); fs(ctx, (0.85, 0.8, 0.7)); ctx.restore()
        ctx.restore()
    vignette(ctx, 0.45)


# ---------- E: the arrest ----------
def e(ctx, t):
    t1, t2, tArr, t3, t4, tFirst = LS("e", 1), LS("e", 2), Wd("e", 2, 7), LS("e", 3), LS("e", 4), Wd("e", 4, 9)
    SP = dict(label="STATE POLICE", body=(0.30, 0.33, 0.38), panel=(0.92, 0.88, 0.70), lsize=26)
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.03 * t, 540, 1000)
        house_day(ctx, t)
        u1 = 1 - (1 - clamp((t - 0.9) / 1.3)) ** 3; u2 = 1 - (1 - clamp((t - 1.6) / 1.3)) ** 3
        if t > 0.9: draw_car(ctx, lerp(-600, 20, u1), 1820, 0.95, t, **SP)
        if t > 1.6: draw_car(ctx, lerp(1300, 570, u2), 1820, 0.95, t + 0.2, flip=True, **SP)
        ctx.restore()
    elif t < t2 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * (t - t1))
        house_day(ctx, t)
        dale = dict(x=540, y=1900, s=2.2, mood=dict(MOODS["happy"], smile=0.6, bi=-6, bo=2, tremble=0.2), mouth=talk("e", "D", t), look=0.3, sweat=True,
                    armL=("ang", -1.2, -2.2), armR=("ang", 1.2, 2.2))
        draw_char(ctx, DALE, dale, t)
        ctx.restore()
    elif t < t3 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.05 * (t - t2))
        house_day(ctx, t)
        draw_char(ctx, DET, dict(x=540, y=1880, s=2.3, mood=dict(MOODS["cold"], eo=0.8, smile=-0.1), mouth=talk("e", "X", t), look=-0.4, saccade=False), t)
        ctx.restore()
        if t >= tArr: V.flash(ctx, t, tArr, (1, 1, 1), 0.15, 0.4)
    elif t < tFirst - 0.05:
        tt = t - t3
        ctx.save(); zoomed(ctx, 1.0 + 0.03 * tt, 540, 1050)
        house_day(ctx, t)
        draw_car(ctx, 570, 1820, 0.95, t, flip=True, **SP)
        walking = t >= t4
        dx = 540 + (lerp(0, 160, sm((t - t4) / 2.0)) if walking else 0)
        dale = dict(x=dx, y=1500, s=1.5, legs=True, mood=dict(MOODS["angry"], flush=0.7), mouth=talk("e", "D", t), look=-0.5 if not walking else -1,
                    armL=("ik", 10, -95, 1), armR=("ik", -10, -95, -1))
        if walking and t > Wd("e", 4, 5): dale.update(mood="cold", mouth=0, look=-1, lookY=0.1)
        draw_char(ctx, TROOPER, dict(x=dx + 230, y=1510, s=1.45, legs=True, mood="cold", look=-1, armL=ik(dict(x=dx + 230, y=1510, s=1.45), dx + 90, 1400, 1)), t)
        draw_char(ctx, DALE, dale, t)
        for sx in (-1, 1):
            ell(ctx, dx + sx * 14, 1500 - 95 * 1.5, 26, 14); st(ctx, (0.8, 0.82, 0.86), 6)
        draw_char(ctx, DET, dict(x=dx - 260, y=1510, s=1.4, legs=True, mood="cold", look=1), t)
        ctx.restore()
    else:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * (t - tFirst))
        house_day(ctx, t)
        draw_char(ctx, MOM_DAY, dict(x=830, y=1900, s=2.0, mood=dict(MOODS["hopeful"], tear=0.5), look=-0.7, armL=ik(dict(x=830, y=1900, s=2.0), 600, 1500, 1)), t)
        draw_char(ctx, MAYA, dict(x=460, y=1940, s=2.3, mood=MT([(tFirst, DETERMINED), (tFirst + 1.2, dict(MOODS["hopeful"], tear=0.0, smile=0.15))], t),
                                  look=0.0, saccade=False), t)
        ctx.restore()
    vignette(ctx, 0.35)


# ---------- F: court, newspaper, behind bars ----------
def f(ctx, t):
    tPlay, tSil, t1, t2 = Wd("f", 0, 12), Wd("f", 0, 19), LS("f", 1), LS("f", 2)
    if t < t1 - 0.03:
        dim = ramp(t, tSil - 0.1, tSil + 0.3) * 0.6
        ctx.save(); zoomed(ctx, 1.0 + 0.03 * t, 540, 1000)
        courtroom(ctx, t, dim)
        draw_char(ctx, dict(ALV, hair=(0.85, 0.85, 0.87), outfit="suit", top=(0.08, 0.08, 0.1), no_lanyard=True, seed=9),
                  dict(x=540, y=1000, s=1.0, glasses=True, mood="cold", look=0.2 if t < tSil else 0.8), t)
        ctx.rectangle(-10, 900, 1100, 120); fs(ctx, (0.45, 0.30, 0.18))
        lawyer = dict(DALE_S, hair=(0.6, 0.6, 0.62), mustache=False, skin=(0.9, 0.72, 0.6), seed=12)
        draw_char(ctx, DALE_S, dict(x=300, y=1620, s=1.35, mood=MT([(0, "smirk"), (tPlay + 0.4, "shock"), (tSil, "cold")], t), look=0.4), t)
        draw_char(ctx, lawyer, dict(x=90, y=1640, s=1.3, mood=MT([(0, "smirk"), (tPlay + 0.6, "worried")], t), look=0.6, mouth=0.4 * abs(sin(t * 8)) if t < tPlay else 0), t)
        ctx.rectangle(-10, 1500, 1100, 60); fs(ctx, (0.45, 0.30, 0.18))
        rrect(ctx, 700, 1400, 220, 130, 8); fs(ctx, (0.2, 0.2, 0.25)); rrect(ctx, 690, 1520, 240, 20, 4); fs(ctx, (0.3, 0.3, 0.35))
        if t >= tPlay:
            for k in range(4):
                r = ((t * 1.1 + k * 0.25) % 1) * 220
                ctx.new_path(); ctx.arc(810, 1450, 40 + r, -2.3, -0.8); ctx.set_source_rgba(1, 0.9, 0.6, 0.7 * (1 - r / 220)); ctx.set_line_width(7); ctx.stroke()
        ctx.rectangle(-10, 1540, 1100, 400); fs(ctx, (0.38, 0.25, 0.15))
        ctx.restore()
        if dim > 0: overlay(ctx, (0.02, 0.02, 0.06), 0.4 * dim)
    elif t < t2 - 0.03:
        newspaper(ctx, t, (t - t1) / (t2 - t1))
    else:
        ctx.save(); zoomed(ctx, 1.0 + 0.05 * (t - t2))
        ctx.set_source_rgb(0.35, 0.36, 0.38); ctx.paint()
        draw_char(ctx, DALE_O, dict(x=540, y=1900, s=2.3, mood=dict(MOODS["cold"], smile=-0.5), lookY=0.6, look=0.2, saccade=False), t)
        for x in range(60, 1080, 150):
            ctx.rectangle(x, -10, 34, 1940); fs(ctx, (0.55, 0.57, 0.6), 5)
        ctx.restore()
    vignette(ctx, 0.5)


# ---------- G: new home ----------
def g(ctx, t):
    t1, t2 = LS("g", 1), LS("g", 2)
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.03 * t, 540, 1000)
        apartment(ctx, t)
        draw_char(ctx, MOM_DAY, dict(x=330, y=1480, s=1.3, legs=True, mood=dict(MOODS["hopeful"], tear=0, smile=0.4), look=0.8,
                                     armL=("ik", -60, -110, 1), armR=("ik", 60, -110, -1)), t)
        rrect(ctx, 330 - 110, 1480 - 210, 220, 150, 8); fs(ctx, (0.82, 0.65, 0.42))
        draw_char(ctx, MAYA, dict(x=760, y=1490, s=1.2, legs=True, mood=dict(MOODS["hopeful"], tear=0, smile=0.5), look=-0.8), t)
        boxes(ctx)
        ctx.restore()
    elif t < t2 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * (t - t1))
        apartment(ctx, t)
        draw_char(ctx, MOM_DAY, dict(x=540, y=1900, s=2.4, mood=dict(MOODS["crying"], smile=-0.3, tremble=0.3), mouth=talk("g", "MO", t), look=0.3), t)
        ctx.restore()
    else:
        tt = t - t2
        hug = ramp(tt, 1.4, 2.0)
        ctx.save(); zoomed(ctx, 1.0 + 0.05 * tt, 540, 1000)
        apartment(ctx, t)
        mom = dict(x=lerp(330, 430, hug), y=1600, s=1.8, mood=dict(MOODS["joy"], tear=0.8, smile=0.8), look=1, tilt=0.12 * hug)
        maya = dict(x=lerp(760, 650, hug), y=1660, s=1.6, mood=dict(MOODS["hopeful"], tear=0.6, smile=0.7), look=-1, mouth=talk("g", "M", t), tilt=-0.1 * hug)
        mom["armR"] = ik(mom, lerp(mom["x"] + 120, maya["x"] - 40, hug), lerp(1450, 1260, hug), -1)
        maya["armL"] = ik(maya, lerp(maya["x"] - 120, mom["x"] + 60, hug), lerp(1500, 1300, hug), 1)
        draw_char(ctx, MOM_DAY, mom, t); draw_char(ctx, MAYA, maya, t)
        ctx.restore()
        overlay(ctx, (1, 0.9, 0.7), 0.06 * hug, ADD)
    vignette(ctx, 0.3)


# ---------- H: ending ----------
def h(ctx, t):
    t1, t2 = LS("h", 1), LS("h", 2)
    tEnd = LE("h", 2) + 0.35
    ctx.save(); zoomed(ctx, 1.0 + 0.12 * sm(t / tEnd), 540, 980)
    V.bedroom(ctx, t)
    maya = dict(x=540, y=1500, s=1.6, blink=blinking(t, 1), armL=("ik", 15, -92, 1), armR=("ik", -8, -102, -1),
                mood=MT([(0, dict(MOODS["sad"], smile=0.1, lid=0.3)), (t1, dict(MOODS["hopeful"], tear=0)), (t2, dict(MOODS["hopeful"], tear=0, smile=0.55))], t),
                look=0.0, lookY=0.0, saccade=t < t1)
    draw_char(ctx, MAYA, maya, t)
    ctx.restore()
    vignette(ctx, 0.3)
    end_card(ctx, t, tEnd, "THE END", [("Going through something like this?", 44, (1, 1, 1)),
                                        ("Tell a trusted adult.", 60, (1, 0.86, 0.15)),
                                        ("Follow Paper & Plot for the next story", 40, (1, 1, 1))])
    if t >= tEnd + 0.8:
        text(ctx, "This story is fiction.", 540, 1480, 30, col=(0.8, 0.8, 0.85))


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
