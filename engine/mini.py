"""Seven one-part mini stories. python mini.py m1 preview a:1.0 ... | python mini.py m1 render"""
import json, os, sys, cairo, random
from math import sin, cos, pi
from rig import *
import part1 as P1
import part1v2 as V
from part1 import ik, DALE
from ep_common import end_card, house_day, PATT
from twins_common import char_ecu, hand_world, text_bubble_phone, notebook_cu, pencil, hallway_school, dining, table_front, DAD, MOM2
from ng_common import workbench, bench_front, classroom, cafeteria, desk_room, desk_front

HERE = os.path.dirname(os.path.abspath(__file__))
STORY = sys.argv[1]
EP = f"{HERE}/mini/{STORY}"
TL = {s["id"]: s for s in json.load(open(f"{EP}/timeline.json"))}
V.TL = TL; V.EP = EP
MT = mood_at
talk = V.talk
P1.HL.update({"DA": (0.6, 0.9, 0.6), "F": (1, 0.6, 0.3), "LL": (1, 0.7, 0.8), "MO": (1, 0.6, 0.8), "W": (0.8, 0.7, 1.0),
              "DOC": (0.5, 0.9, 1.0), "GP": (0.7, 0.85, 1.0), "R": (0.85, 0.7, 1.0), "SON": (0.7, 0.9, 0.7), "LI": (1, 0.7, 0.6)})


def LS(sc, i): return TL[sc]["lines"][i]["start"]
def LE(sc, i): l = TL[sc]["lines"][i]; return l["start"] + l["dur"]
def DUR(sc): return TL[sc]["dur"]
def zoomed(ctx, z, cx=540, cy=960): ctx.translate(540, 960); ctx.scale(z, z); ctx.translate(-cx, -cy)


def push(ctx, t, dur, cx=540, cy=1050, z0=1.0, z1=1.12):
    zoomed(ctx, lerp(z0, z1, sm(t / max(dur, 0.1))), cx, cy)


# ---------------- props ----------------
def dog(ctx, x, y, s=1.0, t=0.0, bark=0.0, flip=False, sit=False):
    ctx.save(); ctx.translate(x, y); ctx.scale(-s if flip else s, s)
    fur, dk = (0.88, 0.66, 0.36), (0.70, 0.48, 0.24)
    wag = 0.5 * sin(t * 14)
    ctx.save(); ctx.translate(130, -150); ctx.rotate(-0.9 + wag)
    rrect(ctx, -12, -110, 24, 110, 12); fs(ctx, fur); ctx.restore()
    if not sit:
        step = 10 * sin(t * 10)
        for lx, ph in ((-80, 1), (-40, -1), (60, -1), (100, 1)):
            rrect(ctx, lx - 18 + ph * step * 0.3, -95, 36, 95, 16); fs(ctx, dk if lx in (-40, 100) else fur)
            ell(ctx, lx + ph * step * 0.3, -2, 24, 12); fs(ctx, dk, 3)
        ell(ctx, 10, -135, 135, 78); fs(ctx, fur)
        ell(ctx, 10, -105, 90, 40); ctx.set_source_rgb(0.95, 0.85, 0.7); ctx.fill()
    hx, hy = (-140, -235) if not sit else (-90, -300)
    ell(ctx, hx, hy, 95, 85); fs(ctx, fur)
    ell(ctx, hx - 80, hy + 25, 60, 40); fs(ctx, (0.95, 0.85, 0.7))
    ell(ctx, hx - 128, hy + 8, 16, 12); ctx.set_source_rgb(0.1, 0.07, 0.05); ctx.fill()
    if bark > 0.05:
        poly(ctx, [(hx - 115, hy + 30), (hx - 40, hy + 35), (hx - 60, hy + 40 + 40 * bark)]); fs(ctx, (0.45, 0.12, 0.15), 4)
    ell(ctx, hx - 30, hy - 22, 12, 14); ctx.set_source_rgb(0.08, 0.06, 0.05); ctx.fill()
    ell(ctx, hx - 26, hy - 27, 4, 4); ctx.set_source_rgb(1, 1, 1); ctx.fill()
    ctx.save(); ctx.translate(hx + 45, hy - 40); ctx.rotate(0.35 + 0.1 * sin(t * 3))
    ell(ctx, 0, 60, 34, 75); fs(ctx, dk); ctx.restore()
    rrect(ctx, hx - 10, hy + 50, 90, 22, 10); fs(ctx, (0.85, 0.15, 0.2), 3)
    ctx.restore()


def woof(ctx, t, x, y, t0):
    if t < t0: return
    for k in range(3):
        tk = t0 + k * 0.45
        if tk <= t < tk + 0.4:
            p = back_out((t - tk) / 0.2)
            ctx.save(); ctx.translate(x + k * 40, y - k * 60); ctx.scale(p, p); ctx.rotate(-0.15)
            text(ctx, "WOOF!", 0, 0, 70, col=(1, 0.86, 0.15), stroke=10); ctx.restore()


def helmet(ctx, P):
    hx, hy = head_world(P); s = P.get("s", 1)
    ctx.save(); ctx.translate(hx, hy); ctx.scale(s, s)
    ctx.move_to(-110, -40); ctx.curve_to(-110, -170, 110, -170, 110, -40); ctx.close_path(); fs(ctx, (0.85, 0.12, 0.12))
    ell(ctx, 0, -40, 135, 22); fs(ctx, (0.75, 0.10, 0.10))
    shield(ctx, 0, -105, 22); fs(ctx, (0.95, 0.8, 0.3), 3)
    ctx.restore()


def library(ctx, t):
    ctx.set_source_rgb(0.55, 0.40, 0.28); ctx.paint()
    rs = random.Random(3)
    for y in range(260, 1500, 240):
        ctx.rectangle(0, y + 200, 1080, 30); fs(ctx, (0.40, 0.27, 0.17), 3)
        x = 10
        while x < 1070:
            w = rs.randint(28, 60); h_ = rs.randint(150, 195)
            ctx.rectangle(x, y + 200 - h_, w, h_); fs(ctx, rs.choice([(0.7, 0.2, 0.2), (0.2, 0.4, 0.7), (0.85, 0.7, 0.3), (0.3, 0.55, 0.35), (0.5, 0.3, 0.55), (0.9, 0.9, 0.85)]), 3)
            x += w + 2
    ctx.rectangle(0, 1500, 1080, 500); ctx.set_source_rgb(0.45, 0.32, 0.22); ctx.fill()
    glow(ctx, 540, 400, 700, (1, 0.9, 0.6), 0.2)


def serving_counter(ctx, t, scoop=0.0):
    ctx.rectangle(-10, 1330, 1100, 50); fs(ctx, (0.80, 0.82, 0.86))
    ctx.rectangle(-10, 1375, 1100, 600); fs(ctx, (0.65, 0.68, 0.72))
    for x, c in [(150, (0.95, 0.85, 0.4)), (330, (0.55, 0.75, 0.35)), (510, (0.85, 0.5, 0.3))]:
        rrect(ctx, x - 75, 1300, 150, 40, 6); fs(ctx, (0.88, 0.88, 0.9), 3); ell(ctx, x, 1305, 60, 12); ctx.set_source_rgb(*c); ctx.fill()


def tray(ctx, x, y, s=1.0, heap=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -140, -20, 280, 50, 10); fs(ctx, (0.92, 0.5, 0.35))
    blob(ctx, [(-50, -30 - 10 * heap, 40 + 15 * heap), (20, -40 - 20 * heap, 45 + 20 * heap), (80, -25, 30 + 10 * heap)], (0.95, 0.82, 0.45))
    ell(ctx, -90, -15, 26, 14); fs(ctx, (0.5, 0.75, 0.35), 3)
    ctx.restore()


def radiator(ctx, x, y):
    for k in range(7):
        rrect(ctx, x + k * 42, y, 34, 260, 14); fs(ctx, (0.85, 0.85, 0.88), 4)
    ctx.rectangle(x - 8, y + 240, 7 * 42 + 4, 24); fs(ctx, (0.75, 0.75, 0.78), 3)


def toolbox(ctx, x, y, s, open_=0.0, t=0.0, letters=True):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -260, -150, 520, 200, 16); fs(ctx, (0.18, 0.40, 0.80))
    if letters and open_ > 0.3:
        for k in range(10):
            ctx.save(); ctx.translate(-200 + k * 44, -150 - 50 * open_); ctx.rotate(-0.05 + 0.02 * k)
            ctx.rectangle(-30, -60, 60, 120); fs(ctx, (0.99, 0.97, 0.90), 3)
            text(ctx, str(14 + k) if k < 5 else "", 0, 0, 22, col=(0.8, 0.2, 0.2))
            ctx.restore()
    ctx.save(); ctx.translate(-260, -150); ctx.rotate(-1.9 * open_)
    rrect(ctx, 0, -40, 520, 46, 12); fs(ctx, (0.15, 0.35, 0.72)); ctx.restore()
    rrect(ctx, -60, -190 if open_ < 0.2 else -150, 120, 30, 10); st(ctx, (0.1, 0.1, 0.12), 8)
    ctx.restore()


def cake(ctx, x, y, s, t):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -120, -110, 240, 110, 16); fs(ctx, (0.98, 0.80, 0.85))
    ctx.move_to(-120, -80); ctx.curve_to(-60, -50, 0, -100, 60, -60); ctx.curve_to(90, -45, 110, -70, 120, -80); st(ctx, (1, 1, 1), 10)
    rrect(ctx, -7, -180, 14, 70, 4); fs(ctx, (0.5, 0.75, 1.0), 3)
    ell(ctx, 0, -195 + 3 * sin(t * 12), 10, 18); ctx.set_source_rgb(1, 0.8, 0.2); ctx.fill(); glow(ctx, 0, -195, 80, (1, 0.8, 0.3), 0.6)
    ctx.restore()


def mini_end(ctx, t, tEnd, q):
    end_card(ctx, t, tEnd, "THE END", [(q, 46, (1, 0.86, 0.15)), ("Follow Paper & Plot", 46, (1, 1, 1)), ("A new story every day", 40, (1, 1, 1))])


# ================= M1: the dog =================
BEN = dict(skin=(0.92, 0.74, 0.60), hair=(0.40, 0.25, 0.14), hairstyle="crew", outfit="hoodie", top=(0.92, 0.55, 0.20), seed=51, pants=(0.3, 0.3, 0.4))
FF = dict(skin=(0.70, 0.50, 0.38), hair=(0.12, 0.10, 0.08), hairstyle="crew", outfit="uniform", top=(0.75, 0.58, 0.25), seed=52, wide=1.12)
MOM_P = dict(MOM2, outfit="longsleeve", top=(0.75, 0.65, 0.85))
DAD_P = dict(DAD, outfit="longsleeve", top=(0.45, 0.55, 0.70))


def m1(sc, ctx, t):
    if sc == "a":
        ctx.save(); push(ctx, t, DUR("a"), 540, 1150, 1.0, 1.2)
        P1.hallway(ctx, t); dog(ctx, 600, 1700, 1.3, t, bark=abs(sin(t * 9)))
        ctx.restore(); woof(ctx, t, 260, 900, 0.2)
        overlay(ctx, (0, 0.03, 0.15), 0.25); vignette(ctx, 0.55)
        P1.HEADER[:] = ["MY DOG SAVED MY FAMILY", "FULL STORY"]
    elif sc == "b":
        t1 = LS("b", 1)
        if t < t1 - 0.03:
            ctx.save(); push(ctx, t, t1)
            house_day(ctx, t)
            draw_char(ctx, BEN, dict(x=380, y=1560, s=1.4, legs=True, mood="joy", look=0.8, armR=ik(dict(x=380, y=1560, s=1.4), 560, 1450, -1)), t)
            dog(ctx, 760, 1720, 1.0, t, sit=True)
            ctx.restore(); overlay(ctx, (0.9, 0.75, 0.5), 0.12)
            V.name_tag(ctx, t, 0.8, t1 - 0.3, "MAX", "our new dog")
        else:
            char_ecu(ctx, t, DAD_P, (t - t1) / (DUR("b") - t1), dict(MOODS["angry"], flush=0.5), P1.hallway, mouth=talk("b", "DA", t), dark=0.2, glasses=True)
        vignette(ctx, 0.45)
    elif sc == "c":
        t1 = LS("c", 1)
        ctx.save(); push(ctx, t, DUR("c"), 540, 1150)
        P1.hallway(ctx, t)
        if t < t1 - 0.03:
            b = dict(x=700, y=1570, s=1.35, legs=True, mood="shock", look=-1, dark=0.2)
            tug = 20 * sin(t * 10)
            b["armL"] = ik(b, 470 + tug, 1460, -1)
            draw_char(ctx, BEN, b, t); dog(ctx, 460 + tug * 0.5, 1720, 1.05, t, bark=0.3)
        else:
            ctx.rectangle(380, 760, 300, 600); fs(ctx, (0.22, 0.18, 0.25))
            dog(ctx, 600, 1720, 1.1, t, bark=abs(sin(t * 9)), flip=True)
            woof(ctx, t, 300, 1000, t1)
        ctx.restore(); overlay(ctx, (0, 0.03, 0.15), 0.25); vignette(ctx, 0.55)
    elif sc == "d":
        ctx.save(); push(ctx, t, DUR("d"), 540, 1150)
        P1.house_night(ctx, t)
        for (ch, x, mood) in [(DAD_P, 230, "worried"), (MOM_P, 470, dict(MOODS["sad"], tremble=0.3)), (BEN, 720, dict(MOODS["scared"], tremble=0.4))]:
            P = dict(x=x, y=1650, s=1.25, legs=True, mood=mood, look=0.3, tilt=0.08 * sin(t * 2 + x), dark=0.25,
                     armL=("ik", 25, -105, 1), armR=("ik", -25, -110, -1))
            if ch is DAD_P: P["glasses"] = True
            draw_char(ctx, ch, P, t)
        dog(ctx, 950, 1850, 0.9, t, sit=True, flip=True)
        ctx.restore(); overlay(ctx, (0, 0.03, 0.15), 0.25); vignette(ctx, 0.5)
    elif sc == "e":
        ph = (t * 2.4) % 1 < 0.5
        def bg(c_, tt_): P1.house_night(c_, tt_); glow(c_, 200, 1300, 700, (1, 0.15, 0.1) if ph else (1, 0.6, 0.1), 0.4)
        ctx.save(); z = 1.0 + 0.08 * sm(t / DUR("e")); zoomed(ctx, z)
        bg(ctx, t)
        P = dict(x=540, y=1880, s=2.3, mood=dict(MOODS["worried"], bi=4, bo=-2), mouth=talk("e", "F", t), look=0.2)
        draw_char(ctx, FF, P, t); helmet(ctx, P)
        ctx.restore(); vignette(ctx, 0.45)
    elif sc == "f":
        t1 = LS("f", 1); tEnd = LE("f", 1) + 0.35
        ctx.save(); push(ctx, t, DUR("f"), 540, 1150)
        house_day(ctx, t)
        b = dict(x=420, y=1600, s=1.4, legs=True, mood=dict(MOODS["hopeful"], tear=0.5, smile=0.6), look=0.7, tilt=0.06)
        b["armR"] = ik(b, 680, 1400, -1)
        dog(ctx, 850, 1760, 1.15, t, sit=True); draw_char(ctx, BEN, b, t)
        ctx.restore(); vignette(ctx, 0.3)
        mini_end(ctx, t, tEnd, "Does your pet have a superpower?")


# ================= M2: the lunch lady =================
JADE = dict(skin=(0.45, 0.30, 0.22), hair=(0.06, 0.05, 0.05), hairstyle="long", outfit="hoodie", top=(0.70, 0.60, 0.90), seed=53, blush=True)
LUNCH = dict(skin=(0.88, 0.68, 0.54), hair=(0.70, 0.70, 0.72), hairstyle="bun", outfit="cardigan", top=(0.97, 0.97, 0.97), no_lanyard=True, seed=54, blush=True)
JDAD = dict(DAD, skin=JADE["skin"], hair=(0.08, 0.06, 0.05), beard=False)
JMOM = dict(MOM2, skin=JADE["skin"], hair=(0.08, 0.06, 0.05))
NURSE = dict(JADE, outfit="longsleeve", top=(0.30, 0.65, 0.65), hairstyle="bun")


def lunch_scene(ctx, t, mood_l="happy", mood_j="happy", scoop=True, talk_l=0.0):
    cafeteria(ctx, t)
    l = dict(x=330, y=1420, s=1.35, mood=mood_l, look=0.7, mouth=talk_l, blink=blinking(t, 54))
    if scoop: l["armR"] = ("ang", 1.2 + 0.4 * sin(t * 4), 1.6 + 0.5 * sin(t * 4))
    draw_char(ctx, LUNCH, l, t)
    hx, hy = head_world(l); ctx.save(); ell(ctx, hx, hy - 60 * 1.35, 105 * 1.35, 60 * 1.35); ctx.set_source_rgba(1, 1, 1, 0.35); ctx.fill(); ctx.restore()
    draw_char(ctx, JADE, dict(x=780, y=1520, s=1.3, mood=mood_j, look=-0.8, blink=blinking(t, 53)), t)
    serving_counter(ctx, t)
    tray(ctx, 760, 1330, 1.0, heap=lerp(0.2, 1.4, sm((t % 4) / 2)) if scoop else 1.4)


def m2(sc, ctx, t):
    P1.HEADER[:] = ["THE LUNCH LADY KNEW", "FULL STORY"]
    if sc == "a":
        ctx.save(); push(ctx, t, DUR("a"), 540, 1150); lunch_scene(ctx, t, mood_j=MT([(0, "shock"), (2.5, "happy")], t)); ctx.restore(); vignette(ctx, 0.3)
    elif sc == "b":
        ctx.save(); push(ctx, t, DUR("b"), 540, 1100)
        V.kitchen_night(ctx, t); P1.lamp(ctx, t * 0.5, 0.6)
        draw_char(ctx, JDAD, dict(x=420, y=1470, s=1.4, mood="sad", lookY=0.9, tilt=-0.08, armL=("ang", -0.25, 2.55), armR=("ik", 60, -60, -1)), t)
        draw_char(ctx, JADE, dict(x=880, y=1500, s=1.2, mood="worried", look=-1), t)
        ctx.rectangle(-10, 1390, 1100, 600); fs(ctx, (0.40, 0.29, 0.22))
        ctx.save(); ctx.translate(520, 1380); ctx.rotate(-0.1); ctx.rectangle(-80, -40, 160, 70); fs(ctx, (1, 1, 1), 3)
        text(ctx, "LAID OFF", 0, 8, 26, col=(0.85, 0.1, 0.1)); ctx.restore()
        ctx.restore(); vignette(ctx, 0.5)
    elif sc == "c":
        ctx.save(); push(ctx, t, DUR("c"), 540, 1100)
        V.kitchen_night(ctx, t); P1.lamp(ctx, t * 0.5, 0.6)
        draw_char(ctx, JMOM, dict(x=330, y=1460, s=1.3, mood=dict(MOODS["hopeful"], smile=0.3), look=0.8), t)
        draw_char(ctx, JADE, dict(x=760, y=1470, s=1.2, mood=MT([(0, "neutral"), (3.5, "worried")], t), look=-0.5, lookY=0.5), t)
        ctx.rectangle(-10, 1390, 1100, 600); fs(ctx, (0.40, 0.29, 0.22))
        for x in (330, 760):
            ell(ctx, x, 1400, 90, 20); fs(ctx, (1, 1, 1), 3); rrect(ctx, x - 40, 1375, 80, 30, 6); fs(ctx, (0.85, 0.65, 0.35), 3)
        ctx.restore(); vignette(ctx, 0.5)
    elif sc == "d":
        t1 = LS("d", 1)
        if t < t1 - 0.03:
            ctx.save(); push(ctx, t, t1, 540, 1150); lunch_scene(ctx, t, mood_j="worried", scoop=False, mood_l="neutral"); ctx.restore()
        else:
            def bg(c_, tt_): cafeteria(c_, tt_)
            char_ecu(ctx, t, LUNCH, (t - t1) / (DUR("d") - t1), dict(MOODS["hopeful"], tear=0.6, smile=0.4), bg, mouth=talk("d", "LL", t), look=0.3)
        vignette(ctx, 0.35)
    elif sc == "e":
        t1 = LS("e", 1); tEnd = LE("e", 1) + 0.35
        if t < t1 - 0.03:
            ctx.set_source_rgb(0.75, 0.62, 0.48); ctx.paint()
            ctx.save(); ctx.translate(540, 960); ctx.rotate(-0.04); s_ = 1.0 + 0.05 * t; ctx.scale(s_, s_)
            ctx.rectangle(-360, -260, 720, 520); fs(ctx, (0.98, 0.95, 0.88), 6)
            rrect(ctx, -300, -200, 300, 190, 18); fs(ctx, (0.25, 0.55, 0.35), 4); text(ctx, "GIFT CARD", -150, -95, 36, col=(1, 1, 1)); text(ctx, "GROCERY", -150, -45, 28, col=(0.9, 1, 0.9))
            text(ctx, "Pass it on", 180, -60, 40, col=(0.2, 0.25, 0.5), weight=False); text(ctx, "someday.", 180, -10, 40, col=(0.2, 0.25, 0.5), weight=False)
            ctx.move_to(60, 140); ctx.curve_to(100, 100, 150, 150, 200, 120); st(ctx, (0.85, 0.3, 0.4), 5)
            ctx.restore()
        else:
            ctx.save(); push(ctx, t - t1, DUR("e") - t1, 540, 1100)
            P1.office_bg(ctx, t)
            n = dict(x=380, y=1560, s=1.4, legs=True, mood="happy", look=0.8); n["armR"] = ik(n, 640, 1330, -1)
            draw_char(ctx, NURSE, n, t)
            draw_char(ctx, dict(BEN, top=(0.4, 0.7, 0.9), seed=60), dict(x=800, y=1600, s=1.0, legs=True, mood="joy", look=-0.8), t)
            rrect(ctx, 610, 1300, 70, 50, 8); fs(ctx, (0.95, 0.6, 0.2), 3)
            ctx.restore()
            V.name_tag(ctx, t, t1 + 0.5, tEnd - 0.4, "JADE", "15 years later")
        vignette(ctx, 0.3)
        mini_end(ctx, t, tEnd, "Who was YOUR quiet hero?")


# ================= M3: the library note =================
AVA = dict(skin=(0.96, 0.82, 0.70), hair=(0.55, 0.35, 0.20), hairstyle="long", outfit="cardigan", top=(0.35, 0.55, 0.75), no_lanyard=True, seed=55, blush=True)
LAURA = dict(MOM2, hair=(0.62, 0.30, 0.18), top=(0.80, 0.45, 0.40), seed=56)


def m3(sc, ctx, t):
    P1.HEADER[:] = ["A NOTE FROM MY MOM", "FULL STORY"]
    if sc == "a":
        ctx.save(); push(ctx, t, DUR("a"), 540, 1150, 1.0, 1.25)
        library(ctx, t)
        a = dict(x=540, y=1560, s=1.45, legs=True, mood=MT([(0, "neutral"), (2.6, "shock")], t), lookY=0.6)
        a["armL"] = ik(a, 470, 1300, 1); a["armR"] = ik(a, 610, 1300, -1)
        draw_char(ctx, AVA, a, t)
        poly(ctx, [(440, 1300), (540, 1290), (540, 1330), (440, 1335)]); fs(ctx, (0.98, 0.96, 0.9), 3)
        poly(ctx, [(540, 1290), (640, 1300), (640, 1335), (540, 1330)]); fs(ctx, (0.98, 0.96, 0.9), 3)
        if t > 2.0:
            fy = lerp(1320, 1640, sm((t - 2.0) / 1.2))
            ctx.save(); ctx.translate(560 + 40 * sin(t * 3), fy); ctx.rotate(0.3 * sin(t * 4)); ctx.rectangle(-45, -30, 90, 60); fs(ctx, (1, 0.95, 0.7), 3); ctx.restore()
        ctx.restore(); vignette(ctx, 0.35)
    elif sc == "b":
        lines = [("If you find this,", (0.15, 0.15, 0.45), LS("b", 1)), ("I hope you're braver", (0.15, 0.15, 0.45), LS("b", 1) + 1.0),
                 ("than me.", (0.15, 0.15, 0.45), LS("b", 1) + 1.6), ("Write your story.", (0.15, 0.15, 0.45), LS("b", 1) + 2.4), ("Love, L.", (0.85, 0.2, 0.3), LS("b", 1) + 3.4)]
        notebook_cu(ctx, t, t / DUR("b"), lines=lines, photos=False)
        vignette(ctx, 0.45)
    elif sc == "c":
        char_ecu(ctx, t, AVA, t / DUR("c"), MT([(0, "neutral"), (1.0, "shock"), (3.2, dict(MOODS["hopeful"], tear=0.3))], t), library, look=0.0)
        vignette(ctx, 0.35)
    elif sc == "d":
        t1 = LS("d", 1)
        if t < t1 - 0.03:
            ctx.save(); push(ctx, t, t1, 540, 1080)
            dining(ctx, t); P1.lamp(ctx, t, 1.0)
            draw_char(ctx, LAURA, dict(x=330, y=1450, s=1.35, mood=MT([(0, "happy"), (2.6, "shock")], t), look=0.6, lookY=0.4), t)
            draw_char(ctx, AVA, dict(x=760, y=1460, s=1.3, mood="worried", look=-0.7), t)
            table_front(ctx, t, lasagna=False)
            ctx.save(); ctx.translate(540, 1370); ctx.rotate(0.1); ctx.rectangle(-60, -30, 120, 60); fs(ctx, (1, 0.95, 0.7), 3); ctx.restore()
            ctx.restore()
        else:
            char_ecu(ctx, t, LAURA, (t - t1) / (DUR("d") - t1), dict(MOODS["sad"], tear=0.7, smile=0.1), dining, mouth=talk("d", "MO", t), look=0.3)
        vignette(ctx, 0.35)
    elif sc == "e":
        t1 = LS("e", 1); tEnd = LE("e", 1) + 0.35
        if t < t1 - 0.03:
            ctx.save(); push(ctx, t, t1, 540, 1100)
            desk_room(ctx, t, night=True, bear_on=False)
            a = dict(x=520, y=1470, s=1.35, mood=dict(MOODS["hopeful"], tear=0.0, smile=0.4), lookY=0.9)
            a["armL"] = ik(a, 470 + 10 * sin(t * 9), 1300, 1); a["armR"] = ik(a, 600, 1305, -1)
            draw_char(ctx, AVA, a, t); hx, hy = hand_world(a, "L"); pencil(ctx, hx + 8, hy - 30, 0.6, rot=0.4)
            desk_front(ctx, t)
            ctx.restore()
        else:
            ctx.save(); push(ctx, t - t1, DUR("e") - t1, 540, 1100)
            V.kitchen_day(ctx, t)
            l = dict(x=540, y=1480, s=1.45, mood=dict(MOODS["happy"], smile=0.6), lookY=0.9)
            l["armL"] = ik(l, 490 + 10 * sin(t * 9), 1330, 1); l["armR"] = ik(l, 620, 1335, -1)
            draw_char(ctx, LAURA, l, t); hx, hy = hand_world(l, "L"); pencil(ctx, hx + 8, hy - 30, 0.6, rot=0.4)
            ctx.rectangle(-10, 1380, 1100, 600); fs(ctx, (0.85, 0.62, 0.42))
            rrect(ctx, 420, 1340, 260, 40, 6); fs(ctx, (0.98, 0.96, 0.9), 3); text(ctx, "Chapter 4", 550, 1372, 22, col=(0.3, 0.3, 0.5))
            ctx.restore()
        vignette(ctx, 0.3)
        mini_end(ctx, t, tEnd, "What dream did YOUR parents give up?")


# ================= M4: fake sick =================
ZOEY = dict(skin=(0.97, 0.82, 0.70), hair=(0.12, 0.08, 0.06), hairstyle="curly", outfit="hoodie", top=(0.85, 0.25, 0.30), seed=57, blush=True)
ZMOM = dict(MOM2, hair=(0.15, 0.10, 0.08), top=(0.55, 0.70, 0.55), seed=58)
DOCTOR = dict(skin=(0.75, 0.55, 0.42), hair=(0.25, 0.18, 0.12), hairstyle="crew", outfit="cardigan", top=(0.97, 0.97, 0.98), no_lanyard=True, seed=59, mustache=True)


def m4(sc, ctx, t):
    P1.HEADER[:] = ["I FAKED BEING SICK", "FULL STORY"]
    if sc == "a":
        ctx.save(); push(ctx, t, DUR("a"), 540, 1100)
        V.bedroom(ctx, t)
        rrect(ctx, 150, 1300, 800, 300, 30); fs(ctx, (0.85, 0.85, 0.95))
        draw_char(ctx, ZOEY, dict(x=540, y=1500, s=1.4, mood=MT([(0, dict(MOODS["smirk"], eo=0.8)), (2.4, "shock")], t), look=0.3), t)
        ctx.move_to(150, 1420); ctx.curve_to(400, 1340, 700, 1340, 950, 1420); ctx.line_to(950, 1920); ctx.line_to(150, 1920); ctx.close_path(); fs(ctx, (0.55, 0.70, 0.95))
        rrect(ctx, 720, 520, 220, 190, 6); fs(ctx, (1, 1, 1)); text(ctx, "MATH TEST", 830, 590, 30, col=(0.85, 0.15, 0.15)); text(ctx, "TODAY", 830, 650, 40, col=(0.2, 0.2, 0.3))
        ctx.restore(); vignette(ctx, 0.3)
    elif sc == "b":
        t1 = LS("b", 1)
        if t < t1 - 0.03:
            ctx.save(); push(ctx, t, t1, 540, 1100)
            V.bedroom(ctx, t); radiator(ctx, 330, 1250)
            draw_char(ctx, ZOEY, dict(x=480, y=1560, s=1.35, legs=True, mood=MT([(0, "scared"), (2.6, dict(MOODS["happy"], smile=0.7, flush=0.9))], t), look=0.6, tilt=0.35 if t > 2.6 else 0), t)
            for k in range(4):
                p = ((t * 0.8 + k * 0.25) % 1); ell(ctx, 480 + 60 * sin(k * 2), 1000 - p * 200, 20 + p * 20, 26 + p * 20); ctx.set_source_rgba(1, 1, 1, 0.4 * (1 - p)); ctx.fill()
            ctx.restore()
        else:
            char_ecu(ctx, t, ZMOM, (t - t1) / (DUR("b") - t1), dict(MOODS["shock"], mo=0.3), V.bedroom, mouth=talk("b", "MO", t), look=0.3)
        vignette(ctx, 0.3)
    elif sc == "c":
        t1 = LS("c", 1)
        if t < t1 - 0.03:
            ctx.save(); push(ctx, t, t1, 540, 1080)
            P1.office_bg(ctx, t)
            d = dict(x=330, y=1480, s=1.4, mood=MT([(0, "neutral"), (2.8, "smirk")], t), look=0.6)
            draw_char(ctx, DOCTOR, d, t)
            hx, hy = head_world(d); ctx.move_to(hx - 50, hy + 200); ctx.curve_to(hx - 60, hy + 330, hx + 60, hy + 330, hx + 50, hy + 200); st(ctx, (0.2, 0.2, 0.25), 6)
            draw_char(ctx, ZMOM, dict(x=760, y=1480, s=1.35, mood="worried", look=-0.6), t)
            draw_char(ctx, ZOEY, dict(x=560, y=1560, s=1.1, mood=dict(MOODS["sad"], tremble=0.2), look=-0.4), t)
            P1.desk(ctx)
            ctx.restore()
        else:
            char_ecu(ctx, t, DOCTOR, (t - t1) / (DUR("c") - t1), dict(MOODS["cold"], eo=0.9, smile=0.0), P1.office_bg, mouth=talk("c", "DOC", t), look=0.4)
        vignette(ctx, 0.3)
    elif sc == "d":
        ctx.save(); push(ctx, t, DUR("d"), 540, 1100)
        V.bedroom(ctx, t)
        draw_char(ctx, ZOEY, dict(x=540, y=1470, s=1.4, mood=dict(MOODS["crying"], mo=0.5), look=0.0, armL=("ik", -40, -110, 1), armR=("ik", 40, -110, -1)), t)
        ctx.rectangle(-10, 1380, 1100, 600); fs(ctx, (0.85, 0.62, 0.42))
        ell(ctx, 540, 1390, 140, 40); fs(ctx, (1, 1, 1), 4); ell(ctx, 540, 1385, 110, 26); ctx.set_source_rgb(0.95, 0.85, 0.6); ctx.fill()
        rrect(ctx, 820, 1180, 120, 200, 30); fs(ctx, (0.8, 0.9, 1.0), 4); rrect(ctx, 845, 1230, 70, 120, 10); fs(ctx, (0.1, 0.1, 0.12), 3)
        ctx.restore(); vignette(ctx, 0.3)
    elif sc == "e":
        t1 = LS("e", 1); tEnd = LE("e", 1) + 0.35
        if t < t1 - 0.03:
            ctx.save(); push(ctx, t, t1, 540, 1080)
            classroom(ctx, t)
            draw_char(ctx, ZOEY, dict(x=540, y=1480, s=1.4, mood=MT([(0, "happy"), (2.5, "shock")], t), look=0.0), t)
            from ng_common import school_desk; school_desk(ctx)
            ctx.save(); ctx.translate(540, 1380); ctx.rotate(-0.05); ctx.rectangle(-150, -40, 300, 80); fs(ctx, (1, 1, 1), 3); text(ctx, "MATH TEST", 0, 12, 34, col=(0.2, 0.2, 0.3)); ctx.restore()
            ctx.restore()
        else:
            ctx.set_source_rgb(0.80, 0.84, 0.74); ctx.paint()
            ctx.save(); ctx.translate(540, 900); ctx.rotate(-0.04); s_ = 1.0 + 0.05 * (t - t1); ctx.scale(s_, s_)
            ctx.rectangle(-330, -430, 660, 860); fs(ctx, (1, 1, 1), 5)
            text(ctx, "MATH TEST", -60, -330, 50, col=(0.2, 0.2, 0.3))
            for k in range(8): ctx.rectangle(-270, -230 + k * 70, 400, 14); ctx.set_source_rgb(0.8, 0.8, 0.85); ctx.fill()
            ctx.new_path(); ctx.arc(200, -320, 90, 0, 2 * pi); st(ctx, (0.9, 0.15, 0.15), 10)
            text(ctx, "C", 200, -290, 110, col=(0.9, 0.15, 0.15))
            ctx.restore()
        vignette(ctx, 0.3)
        mini_end(ctx, t, tEnd, "Have YOU ever faked being sick?")


# ================= M5: grandpa's voicemail =================
CHAMP = dict(skin=(0.75, 0.55, 0.40), hair=(0.08, 0.06, 0.05), hairstyle="crew", outfit="hoodie", top=(0.18, 0.25, 0.45), seed=61)
GRANDPA = dict(skin=(0.80, 0.60, 0.46), hair=(0.85, 0.85, 0.87), hairstyle="crew", outfit="sweater", top=(0.55, 0.35, 0.25), beard=True, seed=62)
CDAD = dict(DAD, skin=CHAMP["skin"], hair=(0.1, 0.08, 0.06), seed=63)


def voicemail_phone(ctx, t, t0):
    ctx.save(); ctx.translate(540, 980); ctx.scale(2.2, 2.2)
    rrect(ctx, -170, -330, 340, 660, 40); fs(ctx, (0.12, 0.12, 0.14), 5)
    rrect(ctx, -155, -310, 310, 620, 28); ctx.set_source_rgb(0.97, 0.97, 0.98); ctx.fill()
    ctx.save(); ell(ctx, 0, -170, 80, 80); ctx.clip(); ctx.set_source_rgb(0.75, 0.85, 0.95); ctx.paint()
    draw_char(ctx, GRANDPA, dict(x=0, y=40, s=0.6, mood="happy", glasses=True, saccade=False), 0.3); ctx.restore()
    ell(ctx, 0, -170, 80, 80); st(ctx, (0.3, 0.3, 0.35), 3)
    text(ctx, "Grandpa", 0, -55, 28, col=(0.1, 0.1, 0.15)); text(ctx, "Voicemail · 0:07", 0, -22, 18, col=(0.5, 0.5, 0.55), weight=False)
    for i in range(24):
        h_ = 8 + 50 * abs(sin(t * 8 + i * 0.9)) * (0.4 + 0.6 * abs(sin(i * 0.5))) if t > t0 else 8
        ctx.rectangle(-120 + i * 10, 60 - h_ / 2, 6, h_); ctx.set_source_rgb(0.25, 0.55, 1.0); ctx.fill()
    ell(ctx, 0, 200, 40, 40); ctx.set_source_rgb(0.25, 0.55, 1.0); ctx.fill()
    poly(ctx, [(-10, 185), (-10, 215), (16, 200)]) if t < t0 else (ctx.rectangle(-12, 186, 8, 28), ctx.rectangle(4, 186, 8, 28))
    ctx.set_source_rgb(1, 1, 1); ctx.fill()
    ctx.restore()


def m5(sc, ctx, t):
    P1.HEADER[:] = ["GRANDPA'S LAST VOICEMAIL", "FULL STORY"]
    if sc == "a":
        char_ecu(ctx, t, CHAMP, t / DUR("a"), dict(MOODS["sad"], tear=0.5), lambda c_, tt_: desk_room(c_, tt_, night=True, bear_on=False), look=0.0, armL=("ik", -70, -330, 1))
        vignette(ctx, 0.45)
    elif sc == "b":
        ctx.set_source_rgb(0.15, 0.16, 0.22); ctx.paint(); voicemail_phone(ctx, t, 0.2); vignette(ctx, 0.4)
    elif sc == "c":
        ctx.save(); push(ctx, t, DUR("c"), 540, 1100)
        workbench(ctx, t)
        for k, (x, y) in enumerate([(150, 1150), (300, 1180), (880, 1160)]):
            rrect(ctx, x - 70, y - 60, 140, 120, 6); fs(ctx, (0.75, 0.6, 0.4))
        draw_char(ctx, CHAMP, dict(x=380, y=1560, s=1.35, legs=True, mood="worried", look=0.8 * sin(t * 1.5)), t)
        draw_char(ctx, CDAD, dict(x=760, y=1560, s=1.4, legs=True, mood="sad", look=-0.6 * sin(t * 1.2), glasses=True), t)
        ctx.restore(); vignette(ctx, 0.4)
    elif sc == "d":
        t1 = LS("d", 1)
        if t < t1 - 0.03:
            ctx.save(); push(ctx, t, t1, 600, 1300)
            house_day(ctx, t)
            from rig import draw_car
            draw_car(ctx, 80, 1820, 1.6, t, label="", body=(0.55, 0.20, 0.18), panel=(0.55, 0.20, 0.18))
            toolbox(ctx, 520, 1540, 0.55)
            draw_char(ctx, CHAMP, dict(x=850, y=1600, s=1.25, legs=True, mood=MT([(0, "sad"), (2.2, "shock")], t), look=-1), t)
            ctx.restore()
        else:
            ctx.set_source_rgb(0.35, 0.30, 0.28); ctx.paint()
            ctx.save(); ctx.translate(540, 1150); ctx.scale(1.6, 1.6); toolbox(ctx, 0, 0, 1.0, open_=ramp(t, t1, t1 + 1.0), t=t); ctx.restore()
            glow(ctx, 540, 950, 400, (1, 0.95, 0.75), 0.3 * ramp(t, t1, t1 + 1.0))
        vignette(ctx, 0.35)
    elif sc == "e":
        t1 = LS("e", 1); tEnd = LE("e", 1) + 0.35
        if t < t1 - 0.03:
            lines = [("Happy 14th, champ.", (0.15, 0.15, 0.45), 0.3), ("I'm still cheering", (0.15, 0.15, 0.45), 1.6), ("for you.", (0.15, 0.15, 0.45), 2.4),
                     ("- Grandpa", (0.85, 0.2, 0.3), 3.0)]
            notebook_cu(ctx, t, t / t1, lines=lines, photos=False)
        else:
            char_ecu(ctx, t, CHAMP, (t - t1) / (DUR("e") - t1), dict(MOODS["hopeful"], tear=0.7, smile=0.5), lambda c_, tt_: desk_room(c_, tt_, night=False, bear_on=False), look=0.0)
        vignette(ctx, 0.35)
        mini_end(ctx, t, tEnd, "Tell us about YOUR grandparent")


# ================= M6: the neighbor =================
EMMA = dict(skin=(0.97, 0.84, 0.74), hair=(0.95, 0.80, 0.45), hairstyle="bob", outfit="hoodie", top=(0.98, 0.80, 0.25), seed=64, blush=True)
ROSE = dict(PATT, top=(0.55, 0.65, 0.85), seed=65)
SON = dict(DAD, hair=(0.35, 0.3, 0.28), top=(0.35, 0.35, 0.40), beard=False, seed=66)


def rose_house(ctx, t, rose=True, rose_mood="neutral"):
    house_day(ctx, t)
    if rose:
        ctx.save(); ctx.rectangle(720, 880, 160, 140); ctx.clip()
        ctx.set_source_rgb(0.75, 0.85, 0.92); ctx.paint()
        draw_char(ctx, ROSE, dict(x=800, y=1180, s=0.55, mood=rose_mood, glasses=True, look=-0.5, saccade=False), t)
        ctx.restore()
        ctx.move_to(800, 880); ctx.line_to(800, 1020); ctx.move_to(720, 950); ctx.line_to(880, 950); st(ctx, (1, 1, 1), 6)


def m6(sc, ctx, t):
    P1.HEADER[:] = ["MY NEIGHBOR WATCHED ME", "FULL STORY"]
    if sc == "a":
        ctx.save(); zoomed(ctx, lerp(1.0, 2.6, sm((t - 1.0) / 4.0)), lerp(540, 800, sm((t - 1.0) / 4.0)), lerp(1100, 950, sm((t - 1.0) / 4.0)))
        rose_house(ctx, t)
        draw_char(ctx, EMMA, dict(x=lerp(200, 420, t / 6), y=1800, s=1.2, legs=True, mood="neutral", look=0.6), t)
        ctx.restore(); vignette(ctx, 0.35)
    elif sc == "b":
        ctx.save(); push(ctx, t, DUR("b"), 540, 1200)
        rose_house(ctx, t)
        draw_char(ctx, EMMA, dict(x=lerp(500, 120, t / DUR("b")), y=1800, s=1.2, legs=True, mood="worried", look=0.9 if t % 2 < 1 else -0.6), t)
        ctx.restore(); vignette(ctx, 0.35)
    elif sc == "c":
        ctx.save(); push(ctx, t, DUR("c"), 640, 1200)
        rose_house(ctx, t, rose=False)
        draw_car(ctx, 120, 1850, 1.1, t, label="AMBULANCE", body=(0.97, 0.97, 0.97), panel=(0.9, 0.2, 0.2), lsize=24)
        draw_char(ctx, EMMA, dict(x=950, y=1800, s=1.1, legs=True, mood="shock", look=-1), t)
        ctx.restore(); vignette(ctx, 0.35)
    elif sc == "d":
        t1 = LS("d", 1)
        if t < 3.6:
            ctx.save(); push(ctx, t, 3.6, 540, 1100)
            from ep_common import porch
            porch(ctx, t, inside=(0.9, 0.85, 0.75))
            s_ = dict(x=430, y=1560, s=1.45, legs=True, mood="sad", look=0.6); s_["armR"] = ik(s_, 620, 1330, -1)
            draw_char(ctx, SON, s_, t); rrect(ctx, 590, 1290, 90, 110, 6); fs(ctx, (0.35, 0.5, 0.7), 3)
            draw_char(ctx, EMMA, dict(x=800, y=1580, s=1.25, legs=True, mood="worried", look=-0.7), t)
            ctx.restore()
        else:
            lines = [("Oct 3 - Emma got to school", (0.15, 0.15, 0.45), 3.6), ("safe. Yellow hoodie.", (0.15, 0.15, 0.45), 4.2),
                     ("Oct 4 - Emma got to school", (0.15, 0.15, 0.45), t1), ("safe today. She was smiling.", (0.85, 0.2, 0.3), t1 + 1.2)]
            notebook_cu(ctx, t, (t - 3.6) / 6, lines=lines, photos=False)
        vignette(ctx, 0.35)
    elif sc == "e":
        t1 = LS("e", 1); tEnd = LE("e", 1) + 0.35
        if t < t1 - 0.03:
            from ep_common import porch
            char_ecu(ctx, t, SON, t / t1, dict(MOODS["sad"], tear=0.4), lambda c_, tt_: porch(c_, tt_, inside=(0.9, 0.85, 0.75)), mouth=talk("e", "SON", t), look=0.3)
        else:
            ctx.save(); push(ctx, t - t1, DUR("e") - t1, 700, 1100)
            rose_house(ctx, t, rose=False)
            e = dict(x=460, y=1800, s=1.3, legs=True, mood=dict(MOODS["hopeful"], tear=0.5, smile=0.4), look=1, lookY=-0.4)
            e["armR"] = ("ang", 2.6, 3.0 + 0.3 * sin(t * 8))
            draw_char(ctx, EMMA, e, t)
            ctx.restore()
        vignette(ctx, 0.3)
        mini_end(ctx, t, tEnd, "Who watches over YOU?")


# ================= M7: the wrong number =================
NORA = dict(skin=(0.72, 0.52, 0.40), hair=(0.10, 0.07, 0.05), hairstyle="long", outfit="longsleeve", top=(0.45, 0.35, 0.60), seed=67, blush=True)
LINDA = dict(MOM2, hair=(0.75, 0.70, 0.62), top=(0.70, 0.50, 0.40), seed=68)


def m7(sc, ctx, t):
    P1.HEADER[:] = ["A TEXT FROM A STRANGER", "FULL STORY"]
    if sc == "a":
        ctx.set_source_rgb(0.85, 0.87, 0.92); ctx.paint()
        cake(ctx, 880, 1700, 0.9, t)
        text_bubble_phone(ctx, t, [("Happy birthday, sweetheart. Mom loves you.", False, 3.0)], title="Unknown number", s=2.2, y=980)
        vignette(ctx, 0.3)
    elif sc == "b":
        def bg(c_, tt_):
            V.bedroom(c_, tt_, night=0.7)
            rrect(c_, 760, 1050, 180, 220, 8); fs(c_, (0.55, 0.40, 0.25))
            c_.save(); c_.rectangle(775, 1065, 150, 190); c_.clip(); c_.set_source_rgb(0.85, 0.9, 1); c_.paint()
            draw_char(c_, LINDA, dict(x=850, y=1420, s=0.5, mood="happy", saccade=False, skin=NORA["skin"]), 0.3); c_.restore()
        char_ecu(ctx, t, NORA, t / DUR("b"), dict(MOODS["crying"], tremble=0.4), bg, look=0.0, x=420)
        vignette(ctx, 0.4)
    elif sc == "c":
        ctx.set_source_rgb(0.85, 0.87, 0.92); ctx.paint()
        text_bubble_phone(ctx, t, [("Happy birthday, sweetheart. Mom loves you.", False, -1),
                                   ("I think you have the wrong number. But thank you. Today, I really needed that.", True, 1.0)], title="Unknown number", s=2.2, y=980)
        vignette(ctx, 0.3)
    elif sc == "d":
        t1, t2 = LS("d", 1), LS("d", 2)
        if t < t1 - 0.03:
            ctx.set_source_rgb(0.15, 0.16, 0.22); ctx.paint()
            ctx.save(); ctx.translate(540, 980); ctx.scale(2.2, 2.2)
            rrect(ctx, -170, -330, 340, 660, 40); fs(ctx, (0.12, 0.12, 0.14), 5)
            rrect(ctx, -155, -310, 310, 620, 28); ctx.set_source_rgb(0.18, 0.2, 0.28); ctx.fill()
            text(ctx, "Unknown number", 0, -150, 26, col=(1, 1, 1)); text(ctx, "incoming call...", 0, -110, 18, col=(0.75, 0.75, 0.8), weight=False)
            ell(ctx, 0, 200, 40 + 4 * sin(t * 10), 40 + 4 * sin(t * 10)); ctx.set_source_rgb(0.2, 0.75, 0.35); ctx.fill()
            ctx.restore()
        elif t < t2 - 0.03:
            char_ecu(ctx, t, LINDA, (t - t1) / (t2 - t1), dict(MOODS["sad"], tear=0.6), V.kitchen_day, mouth=talk("d", "LI", t), look=0.2, armL=("ik", -70, -330, 1))
        else:
            char_ecu(ctx, t, NORA, (t - t2) / 2.5, dict(MOODS["shock"], tear=0.5), lambda c_, tt_: V.bedroom(c_, tt_, night=0.7), look=0.0, armL=("ik", -70, -330, 1))
        vignette(ctx, 0.35)
    elif sc == "e":
        tEnd = LE("e", 0) + 0.35
        ctx.set_source_rgb(0.85, 0.87, 0.92); ctx.paint()
        cake(ctx, 880, 1700, 0.9, t)
        text_bubble_phone(ctx, t, [("Happy birthday, sweetheart!", False, 0.5), ("Happy birthday to you too, Linda!", True, 1.5),
                                   ("Same time next year?", False, 2.6), ("Always.", True, 3.6)], title="Linda", s=2.2, y=980)
        vignette(ctx, 0.3)
        mini_end(ctx, t, tEnd, "Would YOU have texted back?")


STORIES = {"m1": m1, "m2": m2, "m3": m3, "m4": m4, "m5": m5, "m6": m6, "m7": m7}
HEADERS = {"m1": ["MY DOG SAVED MY FAMILY", "FULL STORY"], "m2": ["THE LUNCH LADY KNEW", "FULL STORY"], "m3": ["A NOTE FROM MY MOM", "FULL STORY"],
           "m4": ["I FAKED BEING SICK", "FULL STORY"], "m5": ["GRANDPA'S LAST VOICEMAIL", "FULL STORY"], "m6": ["MY NEIGHBOR WATCHED ME", "FULL STORY"],
           "m7": ["A TEXT FROM A STRANGER", "FULL STORY"]}
P1.HEADER[:] = HEADERS[STORY]
fn = STORIES[STORY]
V.SCENES = {sid: (lambda s_: (lambda ctx, t: fn(s_, ctx, t)))(sid) for sid in TL}

if __name__ == "__main__":
    os.makedirs(f"{EP}/preview", exist_ok=True)
    if sys.argv[2] == "preview":
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        for arg in sys.argv[3:]:
            sc, ts = arg.split(":"); V.frame(surf, sc, float(ts)); surf.write_to_png(f"{EP}/preview/{sc}_{ts}.png")
    else:
        for sc in (sys.argv[3:] or TL.keys()): V.render(sc)
