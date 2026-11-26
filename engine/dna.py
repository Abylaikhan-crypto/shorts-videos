"""DNA series, style 2. python dna.py dna1 preview a:1.0 ... | python dna.py dna1 render [scenes]"""
import json, os, sys, subprocess, random
from math import sin, cos, pi
import cairo
_argv = sys.argv; sys.argv = ["s2.py", "x"]
import s2 as S
sys.argv = _argv
from rig import *
from s2 import (layer, paint_layer, cam, depth, shake, punch, grain, label, pop_word, speed_lines, room, side_door, frame_pic,
                hallway_night, bedroom_night, dog_head, blanket, head_y, steam, dizzy_stars, snow, breath, to_surface)
import part1 as P1
from part1 import ik
import part1v2 as V
from ep_common import end_card, car_interior
from twins_common import text_bubble_phone

HERE = os.path.dirname(os.path.abspath(__file__))
PART = sys.argv[1]
EP = f"{HERE}/{PART}"
TL = {s["id"]: s for s in json.load(open(f"{EP}/timeline.json"))}
ADD = cairo.OPERATOR_ADD
CUR = {"sc": "a", "t": 0.0}


def DUR(sc): return TL[sc]["dur"]
def LE(sc, i): l = TL[sc]["lines"][i]; return l["start"] + l["dur"]


def WT(sc, word, li=None, nth=0):
    k = 0
    for i, l in enumerate(TL[sc]["lines"]):
        if li is not None and i != li: continue
        for w in l["words"]:
            if w[0].strip(".,!?'\"").lower() == word.lower():
                if k == nth: return w[1]
                k += 1
    raise KeyError(f"{sc}:{word}:{li}:{nth}")


def talkT(spk):
    sc, t = CUR["sc"], CUR["t"]
    for l in TL[sc]["lines"]:
        if l["spk"] == spk and l["start"] <= t < l["start"] + l["dur"]:
            i = min(int((t - l["start"]) * FPS), len(l["env"]) - 1); e = l["env"]
            return (e[i] + e[max(0, i - 1)]) / 2
    return 0.0


def M(base, **kw):
    d = dict(MOODS[base]) if isinstance(base, str) else dict(base); d.update(kw); return d


# ---------------- cast ----------------
RUBY = dict(skin=(0.80, 0.60, 0.46), hair=(0.07, 0.05, 0.05), hairstyle="long", outfit="hoodie", top=(0.22, 0.58, 0.62), seed=81, blush=True, pants=(0.25, 0.28, 0.40))
MOM = dict(skin=(0.98, 0.86, 0.77), hair=(0.80, 0.32, 0.13), hairstyle="curly", outfit="cardigan", top=(0.55, 0.30, 0.45), no_lanyard=True, seed=82, freckles=True, blush=True)
DAD = dict(skin=(0.96, 0.80, 0.68), hair=(0.86, 0.70, 0.38), hairstyle="crew", outfit="sweater", top=(0.30, 0.42, 0.62), seed=83, pants=(0.3, 0.3, 0.35))
SAM = dict(skin=(0.98, 0.86, 0.77), hair=(0.82, 0.35, 0.14), hairstyle="crew", outfit="hoodie", top=(0.40, 0.70, 0.35), seed=84, freckles=True, blush=True)
HANNAH = dict(skin=(0.98, 0.86, 0.77), hair=(0.80, 0.32, 0.13), hairstyle="curly", outfit="hoodie", top=(0.55, 0.55, 0.60), seed=85, freckles=True, blush=True)
KAREN = dict(skin=(0.80, 0.60, 0.46), hair=(0.07, 0.05, 0.05), hairstyle="bun", outfit="cardigan", top=(0.85, 0.65, 0.25), no_lanyard=True, seed=86, blush=True)
NURSE = dict(skin=(0.90, 0.72, 0.60), hair=(0.35, 0.25, 0.18), hairstyle="bun", outfit="longsleeve", top=(0.55, 0.78, 0.75), seed=87)
GRANDPA = dict(skin=(0.80, 0.60, 0.46), hair=(0.85, 0.85, 0.87), hairstyle="crew", outfit="sweater", top=(0.5, 0.35, 0.25), seed=88)
KID = 0.78   # Sam is smaller


# ---------------- sets ----------------
def xmas_tree(ctx, x, y, s, lit=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -25, -20, 50, 70, 6); fs(ctx, (0.45, 0.28, 0.16))
    for k, (w, yy) in enumerate([(230, -40), (190, -180), (145, -310), (95, -420)]):
        poly(ctx, [(-w, yy), (w, yy), (0, yy - 200)]); fs(ctx, (0.15, 0.48 - 0.03 * k, 0.28))
    rs = random.Random(5)
    for i in range(22):
        yy = rs.uniform(-480, -60); w = 200 * (1 - (-yy - 40) / 560)
        xx = rs.uniform(-w * 0.8, w * 0.8); c = rs.choice([(1, 0.3, 0.3), (1, 0.85, 0.3), (0.4, 0.7, 1), (1, 1, 0.8)])
        ell(ctx, xx, yy, 10, 10); ctx.set_source_rgb(*c); ctx.fill(); glow(ctx, xx, yy, 40, c, 0.35 * lit)
    star(ctx, 0, -630, 45); fs(ctx, (1, 0.85, 0.2), 4)
    ctx.restore()


def string_lights(ctx, x0, y0, x1, y1, n=14, sag=40):
    for i in range(n):
        u = i / (n - 1); x = lerp(x0, x1, u); y = lerp(y0, y1, u) + sag * sin(u * pi)
        c = [(1, 0.3, 0.3), (1, 0.85, 0.3), (0.4, 0.8, 1), (0.5, 1, 0.5)][i % 4]
        ell(ctx, x, y, 8, 11); ctx.set_source_rgb(*c); ctx.fill(); glow(ctx, x, y, 36, c, 0.4)


def couch_back(ctx, y=1180, col=(0.32, 0.45, 0.55)):
    rrect(ctx, 60, y - 260, 960, 300, 60); fs(ctx, col, 6)


def couch_front_fg(ctx, y=1380, col=(0.32, 0.45, 0.55)):
    rrect(ctx, 20, y, 1040, 260, 40); fs(ctx, shade(col, 0.05), 7)
    for x in (-40, 960): rrect(ctx, x, y - 120, 160, 420, 60); fs(ctx, shade(col, 0.12), 7)
    for x in (300, 560, 820): ctx.move_to(x, y + 20); ctx.line_to(x, y + 220); st(ctx, shade(col, 0.25), 5)


def living(ctx):
    room(ctx, back=(170, 520, 740, 640), wall=(0.80, 0.62, 0.46), floor=(0.50, 0.32, 0.22), ceil=(0.86, 0.76, 0.62), side=(0.72, 0.55, 0.40), rug=(0.65, 0.25, 0.25))
    ctx.rectangle(560, 600, 230, 300); fs(ctx, (0.16, 0.20, 0.40), 7)
    for k in range(18):
        rs = random.Random(k); ell(ctx, 560 + rs.uniform(10, 220), 600 + rs.uniform(10, 290), 4, 4); ctx.set_source_rgb(1, 1, 1); ctx.fill()
    ctx.move_to(675, 600); ctx.line_to(675, 900); st(ctx, (1, 1, 1), 7)
    xmas_tree(ctx, 310, 1160, 0.95)
    string_lights(ctx, 170, 540, 910, 540, 16, 30)
    frame_pic(ctx, 830, 620, 70, 90, 0, (0.9, 0.8, 0.6))
    glow(ctx, 310, 900, 450, (1, 0.7, 0.35), 0.25)


def living_dark(ctx):
    living(ctx); overlay(ctx, (0.03, 0.04, 0.14), 0.55)
    xmas_tree(ctx, 310, 1160, 0.95, lit=1.6); string_lights(ctx, 170, 540, 910, 540, 16, 30)


def kitchen(ctx, night=False):
    room(ctx, back=(150, 520, 780, 640), wall=(0.92, 0.88, 0.80), floor=(0.62, 0.42, 0.28), ceil=(0.95, 0.93, 0.88), side=(0.85, 0.80, 0.70))
    for x in range(170, 900, 130): rrect(ctx, x, 560, 115, 170, 8); fs(ctx, (0.55, 0.70, 0.75), 5); ell(ctx, x + 95, 700, 6, 6); fs(ctx, (0.9, 0.85, 0.6), 2)
    ctx.rectangle(150, 900, 780, 260); fs(ctx, (0.55, 0.70, 0.75), 5)
    ctx.rectangle(140, 880, 800, 30); fs(ctx, (0.85, 0.85, 0.82), 4)
    ctx.rectangle(470, 760, 160, 110); fs(ctx, (0.15, 0.20, 0.40) if night else (0.7, 0.88, 1.0), 6)
    poly(ctx, [(930, 560), (1180, 420), (1180, 1480), (930, 1160)]); fs(ctx, (0.88, 0.90, 0.92), 6)   # fridge on right wall
    string_lights(ctx, 150, 540, 930, 540, 14, 25)
    ell(ctx, 540, 300, 110, 34); fs(ctx, (0.95, 0.85, 0.55), 4)
    glow(ctx, 540, 360, 500, (1, 0.8, 0.5), 0.35 if night else 0.2)
    if night: overlay(ctx, (0.03, 0.04, 0.14), 0.55); glow(ctx, 540, 420, 520, (1, 0.75, 0.4), 0.35)


def kitchen_night(ctx): kitchen(ctx, True)


def table_fg(ctx, y=1350, col=(0.55, 0.36, 0.24)):
    poly(ctx, [(-80, y), (1160, y), (1260, 2000), (-180, 2000)]); fs(ctx, col, 7)
    for k in range(1, 5): ctx.move_to(-80, y + k * 60); ctx.line_to(1160, y + k * 60); st(ctx, shade(col, 0.2), 3)


def nursery(ctx):
    room(ctx, back=(150, 520, 780, 600), wall=(0.80, 0.90, 0.84), floor=(0.75, 0.78, 0.80), ceil=(0.92, 0.95, 0.93), side=(0.72, 0.82, 0.76), plank=False)
    ctx.rectangle(240, 600, 600, 260); fs(ctx, (0.55, 0.70, 0.85), 6)
    ell(ctx, 860, 640, 50, 50); fs(ctx, (1, 1, 1), 5); ctx.move_to(860, 640); ctx.line_to(860, 605); ctx.move_to(860, 640); ctx.line_to(885, 650); st(ctx, OUTL, 5)
    for y in (230, 300): ctx.rectangle(-200, y, 1480, 30); ctx.set_source_rgba(1, 1, 0.9, 0.5); ctx.fill()


def bassinet(ctx, x, y, s, blanket_col=(1, 0.72, 0.8), tag=""):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-170, -60); ctx.line_to(-150, 60); ctx.line_to(150, 60); ctx.line_to(170, -60); ctx.close_path(); fs(ctx, (0.85, 0.92, 0.98), 5)
    blob(ctx, [(40, -50, 85), (110, -45, 60)], blanket_col)
    ell(ctx, -95, -75, 55, 50); fs(ctx, (0.98, 0.84, 0.74), 4)
    ctx.move_to(-120, -77); ctx.curve_to(-110, -71, -100, -71, -90, -77); st(ctx, OUTL, 3.5)
    ctx.move_to(-80, -77); ctx.curve_to(-70, -71, -60, -71, -50, -77); st(ctx, OUTL, 3.5)
    ctx.move_to(-150, 70); ctx.line_to(-130, 200); ctx.move_to(150, 70); ctx.line_to(130, 200); st(ctx, (0.6, 0.6, 0.65), 8)
    if tag: rrect(ctx, -80, 0, 160, 40, 8); fs(ctx, (1, 1, 1), 3); text(ctx, tag, 0, 30, 24, col=(0.4, 0.3, 0.4))
    ctx.restore()


def hospital_ext(ctx):
    g = cairo.LinearGradient(0, 0, 0, 1300); g.add_color_stop_rgb(0, 0.04, 0.05, 0.14); g.add_color_stop_rgb(1, 0.15, 0.18, 0.35); ctx.set_source(g); ctx.paint()
    ctx.rectangle(140, 520, 800, 1100); fs(ctx, (0.75, 0.75, 0.80), 6)
    for r in range(6):
        for c in range(6):
            lit = random.Random(r * 7 + c).random() > 0.35
            ctx.rectangle(190 + c * 125, 600 + r * 150, 80, 90); ctx.set_source_rgb(*((1, 0.88, 0.55) if lit else (0.2, 0.22, 0.35))); ctx.fill()
    rrect(ctx, 330, 420, 420, 110, 16); fs(ctx, (0.95, 0.95, 1.0), 5); text(ctx, "ST. MARY'S", 540, 495, 56, col=(0.2, 0.3, 0.6))
    ctx.rectangle(500, 160, 80, 200); ctx.rectangle(440, 220, 200, 80); ctx.set_source_rgb(0.9, 0.15, 0.15); ctx.fill(); glow(ctx, 540, 260, 260, (1, 0.2, 0.2), 0.4)
    ctx.rectangle(-100, 1600, 1300, 500); ctx.set_source_rgb(0.12, 0.12, 0.16); ctx.fill()


def hosp_hall(ctx):
    room(ctx, back=(400, 600, 280, 560), wall=(0.82, 0.88, 0.86), floor=(0.70, 0.74, 0.76), ceil=(0.90, 0.93, 0.92), side=(0.75, 0.83, 0.80), plank=False)
    side_door(ctx, 120, 300, 470, 640, 1500, 1260, col=(0.55, 0.70, 0.80)); side_door(ctx, 780, 960, 640, 470, 1260, 1500, col=(0.55, 0.70, 0.80))
    for x, n in ((210, "204"), (870, "206")): rrect(ctx, x - 55, 380, 110, 50, 8); fs(ctx, (1, 1, 1), 3); text(ctx, n, x, 418, 32, col=(0.2, 0.3, 0.5))
    for y in (250, 420): ctx.rectangle(450, y, 180, 24); ctx.set_source_rgba(1, 1, 0.95, 0.9); ctx.fill()
    overlay(ctx, (0.02, 0.05, 0.15), 0.35)


def cafe(ctx):
    room(ctx, back=(160, 520, 760, 640), wall=(0.55, 0.36, 0.26), floor=(0.40, 0.26, 0.18), ceil=(0.30, 0.20, 0.15), side=(0.48, 0.31, 0.22))
    ctx.rectangle(200, 580, 420, 380); fs(ctx, (0.70, 0.82, 0.92), 7)
    for k in range(5): ctx.rectangle(200, 860 - k * 40, 420, 6); ctx.set_source_rgba(1, 1, 1, 0.2); ctx.fill()
    text(ctx, "CAFE", 410, 660, 60, col=(0.95, 0.95, 0.9))
    rrect(ctx, 680, 590, 200, 260, 10); fs(ctx, (0.15, 0.18, 0.16), 6)
    for k in range(5): ctx.rectangle(705, 630 + k * 42, 150 - 20 * (k % 2), 8); ctx.set_source_rgba(1, 1, 1, 0.7); ctx.fill()
    for x in (300, 540, 780):
        ctx.move_to(x, 200); ctx.line_to(x, 380); st(ctx, OUTL, 4)
        poly(ctx, [(x - 50, 380), (x + 50, 380), (x + 70, 430), (x - 70, 430)]); fs(ctx, (0.15, 0.35, 0.30), 4)
        glow(ctx, x, 460, 260, (1, 0.8, 0.45), 0.4)


def car_night(ctx):
    car_interior(ctx, 0.0)


def bridge(ctx):
    g = cairo.LinearGradient(0, 0, 0, 1200); g.add_color_stop_rgb(0, 0.03, 0.03, 0.12); g.add_color_stop_rgb(1, 0.18, 0.14, 0.35); ctx.set_source(g); ctx.paint()
    rs = random.Random(9)
    for i in range(60):
        ell(ctx, rs.uniform(0, 1080), rs.uniform(0, 700), 2.5, 2.5); ctx.set_source_rgba(1, 1, 0.9, rs.uniform(0.3, 0.9)); ctx.fill()
    ell(ctx, 820, 330, 70, 70); ctx.set_source_rgb(0.97, 0.95, 0.85); ctx.fill(); glow(ctx, 820, 330, 300, (0.8, 0.8, 1), 0.3)
    for i in range(16):   # skyline
        x = i * 75 - 30; h_ = rs.uniform(120, 380)
        ctx.rectangle(x, 1100 - h_, 70, h_ + 10); ctx.set_source_rgb(0.08, 0.08, 0.16); ctx.fill()
        for k in range(int(h_ / 50)):
            if rs.random() > 0.5: ctx.rectangle(x + 15 + 25 * (k % 2), 1100 - h_ + 20 + k * 45, 12, 16); ctx.set_source_rgb(1, 0.85, 0.5); ctx.fill()
    ctx.rectangle(-100, 1100, 1300, 900); ctx.set_source_rgb(0.06, 0.08, 0.18); ctx.fill()
    for i in range(30):
        x = rs.uniform(0, 1080); y = rs.uniform(1120, 1500)
        ctx.rectangle(x, y, rs.uniform(20, 70), 5); ctx.set_source_rgba(1, 0.85, 0.5, 0.4); ctx.fill()
    poly(ctx, [(-100, 1560), (1180, 1560), (1180, 2000), (-100, 2000)]); fs(ctx, (0.30, 0.28, 0.32), 6)
    ctx.rectangle(-100, 1380, 1300, 22); fs(ctx, (0.55, 0.50, 0.55), 5)
    for x in range(-60, 1140, 90): ctx.rectangle(x, 1400, 14, 160); ctx.set_source_rgb(0.45, 0.42, 0.48); ctx.fill()
    for x in (120, 960):
        ctx.rectangle(x - 8, 900, 16, 660); ctx.set_source_rgb(0.2, 0.2, 0.25); ctx.fill()
        ell(ctx, x, 900, 34, 20); ctx.set_source_rgb(1, 0.9, 0.6); ctx.fill(); glow(ctx, x, 920, 300, (1, 0.8, 0.45), 0.45)


def ruby_room_day(ctx):
    room(ctx, back=(180, 520, 720, 640), wall=(0.78, 0.82, 0.95), floor=(0.70, 0.52, 0.36), ceil=(0.92, 0.93, 0.98), side=(0.70, 0.74, 0.88))
    ctx.rectangle(560, 600, 240, 280); fs(ctx, (0.75, 0.9, 1.0), 7)
    for x, c in ((260, (0.95, 0.5, 0.5)), (390, (0.5, 0.7, 0.95))): rrect(ctx, x, 620, 100, 140, 6); fs(ctx, c, 4)
    string_lights(ctx, 180, 540, 900, 540, 14, 40)


def ruby_room_night(ctx):
    ruby_room_day(ctx); overlay(ctx, (0.03, 0.04, 0.16), 0.6); string_lights(ctx, 180, 540, 900, 540, 14, 40)


def karen_apt(ctx, night=False):
    room(ctx, back=(60, 480, 960, 760), wall=(0.80, 0.74, 0.58), floor=(0.55, 0.50, 0.42), ceil=(0.75, 0.72, 0.62), side=(0.70, 0.64, 0.50), plank=False)
    for k in range(6): ctx.move_to(60 + k * 160, 480); ctx.line_to(60 + k * 160, 1240); st(ctx, (0.72, 0.66, 0.50), 3)
    ctx.move_to(700, 500); ctx.line_to(740, 600); ctx.line_to(720, 680); st(ctx, (0.5, 0.45, 0.35), 3)   # crack
    ctx.rectangle(120, 600, 200, 220); fs(ctx, (0.15, 0.2, 0.4) if night else (0.7, 0.85, 0.95), 6)
    rrect(ctx, 720, 760, 220, 460, 18); fs(ctx, (0.93, 0.93, 0.90), 6)   # small fridge
    rs = random.Random(4)
    for k in range(9):
        x, y = 740 + (k % 3) * 66, 790 + (k // 3) * 110
        ctx.save(); ctx.translate(x + 28, y + 40); ctx.rotate(rs.uniform(-0.2, 0.2)); ctx.rectangle(-28, -40, 56, 76)
        fs(ctx, rs.choice([(1, 0.9, 0.6), (0.8, 0.9, 1), (1, 0.8, 0.85)]), 2); ctx.restore()
    for k in range(7): rrect(ctx, 340 + k * 40, 1040, 32, 170, 14); fs(ctx, (0.85, 0.85, 0.88), 3)   # radiator
    rrect(ctx, 360, 880, 280, 20, 6); fs(ctx, (0.55, 0.40, 0.28), 3)
    if night: overlay(ctx, (0.03, 0.04, 0.14), 0.5); glow(ctx, 540, 500, 500, (1, 0.8, 0.45), 0.3)


def karen_apt_night(ctx): karen_apt(ctx, True)


def tiny_room(ctx):
    room(ctx, back=(40, 500, 1000, 760), wall=(0.62, 0.64, 0.70), floor=(0.45, 0.40, 0.36), ceil=(0.55, 0.56, 0.62), side=(0.55, 0.56, 0.62), plank=False)
    ctx.rectangle(640, 600, 200, 220); fs(ctx, (0.12, 0.16, 0.34), 6)
    for k, c in enumerate([(0.9, 0.5, 0.5), (0.5, 0.8, 0.6), (0.6, 0.6, 0.95)]):
        rrect(ctx, 120 + k * 130, 640, 100, 130, 4); fs(ctx, c, 3)
    overlay(ctx, (0.03, 0.04, 0.14), 0.45)


def dining_big(ctx):
    room(ctx, back=(140, 520, 800, 640), wall=(0.88, 0.75, 0.58), floor=(0.55, 0.36, 0.24), ceil=(0.92, 0.85, 0.72), side=(0.80, 0.66, 0.50))
    ctx.rectangle(560, 600, 260, 300); fs(ctx, (0.75, 0.88, 1.0), 7)
    string_lights(ctx, 140, 540, 940, 540, 16, 30)
    ell(ctx, 540, 320, 160, 40); fs(ctx, (0.95, 0.85, 0.55), 4); glow(ctx, 540, 400, 600, (1, 0.8, 0.5), 0.35)


def big_house(ctx):
    g = cairo.LinearGradient(0, 0, 0, 1400); g.add_color_stop_rgb(0, 0.45, 0.70, 0.95); g.add_color_stop_rgb(1, 0.80, 0.90, 1.0); ctx.set_source(g); ctx.paint()
    ctx.rectangle(-100, 1350, 1300, 700); ctx.set_source_rgb(0.40, 0.70, 0.35); ctx.fill()
    poly(ctx, [(60, 760), (540, 420), (1020, 760)]); fs(ctx, (0.45, 0.30, 0.30), 6)
    ctx.rectangle(110, 750, 860, 620); fs(ctx, (0.97, 0.95, 0.90), 6)
    for x in (220, 400, 680, 860):
        for y in (820, 1060): ctx.rectangle(x - 55, y, 110, 140); fs(ctx, (0.6, 0.8, 0.95), 5)
    for x in (300, 780): ctx.rectangle(x - 18, 760, 36, 610); fs(ctx, (1, 1, 1), 4)
    rrect(ctx, 480, 1130, 120, 240, 10); fs(ctx, (0.35, 0.22, 0.16), 5)
    ctx.rectangle(150, 1450, 400, 160); fs(ctx, (0.15, 0.15, 0.18), 5)   # car
    text(ctx, "$$$", 860, 560, 90, col=(0.2, 0.7, 0.3), stroke=12)


def tiny_apt_ext(ctx):
    ctx.set_source_rgb(0.62, 0.66, 0.72); ctx.paint()
    ctx.rectangle(140, 300, 800, 1600); fs(ctx, (0.55, 0.50, 0.48), 6)
    for r in range(9):
        for c in range(5):
            ctx.rectangle(190 + c * 150, 360 + r * 160, 90, 100); fs(ctx, (0.35, 0.40, 0.50), 4)
    ctx.rectangle(190 + 2 * 150, 360 + 6 * 160, 90, 100); ctx.set_source_rgb(1, 0.85, 0.5); ctx.fill()


SETS = {"living": living, "living_dark": living_dark, "kitchen": kitchen, "kitchen_night": kitchen_night, "nursery": nursery,
        "hospital_ext": hospital_ext, "hosp_hall": hosp_hall, "cafe": cafe, "car_night": car_night, "bridge": bridge, "hall": hallway_night,
        "bedroom_night": bedroom_night, "ruby_room": ruby_room_day, "ruby_room_night": ruby_room_night, "karen_apt": karen_apt,
        "karen_apt_night": karen_apt_night, "tiny_room": tiny_room, "dining_big": dining_big, "big_house": big_house, "tiny_apt_ext": tiny_apt_ext}


def BG(ctx, name, blur=0):
    paint_layer(ctx, layer(f"{name}_{blur}", SETS[name], blur))


# ---------------- phones, screens and props ----------------
def phone(ctx, x, y, s, rot, screen, lt=0.0, glow_a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    if glow_a: glow(ctx, 0, 0, 420, (0.6, 0.8, 1), glow_a)
    rrect(ctx, -170, -330, 340, 660, 40); fs(ctx, (0.12, 0.12, 0.14), 5)
    rrect(ctx, -155, -310, 310, 620, 28); ctx.set_source_rgb(0.97, 0.97, 0.98); ctx.fill()
    ctx.save(); rrect(ctx, -155, -310, 310, 620, 28); ctx.clip(); screen(ctx, lt); ctx.restore()
    ctx.restore()


def app_header(ctx, title="HELIX DNA"):
    ctx.rectangle(-160, -310, 320, 80); ctx.set_source_rgb(0.12, 0.55, 0.55); ctx.fill()
    text(ctx, title, 0, -260, 24, col=(1, 1, 1))


def scr_results_ready(ctx, lt):
    app_header(ctx)
    ell(ctx, 0, -100, 70, 70); ctx.set_source_rgb(0.12, 0.55, 0.55); ctx.fill()
    ctx.move_to(-30, -100); ctx.line_to(-8, -75); ctx.line_to(35, -128); st(ctx, (1, 1, 1), 12)
    text(ctx, "Your results", 0, 20, 28, col=(0.15, 0.15, 0.2)); text(ctx, "are ready!", 0, 58, 28, col=(0.15, 0.15, 0.2))
    rrect(ctx, -110, 120, 220, 60, 30); ctx.set_source_rgb(0.95, 0.45, 0.3); ctx.fill(); text(ctx, "VIEW", 0, 160, 24, col=(1, 1, 1))


def scr_pie(ctx, lt):
    app_header(ctx); text(ctx, "DAD", 0, -180, 30, col=(0.15, 0.15, 0.2))
    p = clamp(lt / 0.6)
    parts = [(0.40, (0.2, 0.7, 0.35)), (0.25, (0.3, 0.5, 0.9)), (0.20, (0.95, 0.65, 0.2)), (0.15, (0.8, 0.35, 0.5))]
    a0 = -pi / 2
    for f, c in parts:
        a1 = a0 + 2 * pi * f * p
        ctx.move_to(0, -10); ctx.arc(0, -10, 110, a0, a1); ctx.close_path(); ctx.set_source_rgb(*c); ctx.fill(); a0 = a1
    ell(ctx, 0, -10, 50, 50); ctx.set_source_rgb(0.97, 0.97, 0.98); ctx.fill()
    text(ctx, "40%", 0, 4, 30, col=(0.2, 0.6, 0.3))
    text(ctx, "Irish", 0, 160, 34, col=(0.2, 0.6, 0.3))


def avatar(ctx, ch, x, y, r=44):
    ctx.save(); ell(ctx, x, y, r, r); ctx.clip(); ctx.set_source_rgb(0.85, 0.9, 0.95); ctx.paint()
    s_ = r / 140; draw_char(ctx, ch, dict(x=x, y=y + 340 * s_ + r * 0.35, s=s_, mood="happy", saccade=False), 0.3); ctx.restore()
    ell(ctx, x, y, r, r); st(ctx, (0.3, 0.3, 0.35), 3)


def scr_tree(ctx, lt, show_ruby=False, ruby_red=False):
    app_header(ctx, "FAMILY MATCHES")
    pos = {"DAD": (-80, -150), "MOM": (80, -150), "SAM": (-80, 30), "RUBY": (80, 30)}
    chs = {"DAD": DAD, "MOM": MOM, "SAM": SAM, "RUBY": RUBY}
    for a_ in ("DAD", "MOM"):
        ctx.move_to(*pos[a_]); ctx.line_to(*pos["SAM"]); st(ctx, (0.2, 0.75, 0.35), 6)
    if show_ruby:
        for a_ in ("DAD", "MOM"):
            ctx.save(); ctx.set_dash([10, 10]); ctx.move_to(*pos[a_]); ctx.line_to(*pos["RUBY"]); st(ctx, (0.9, 0.2, 0.2), 5); ctx.restore()
    for n, (x, y) in pos.items():
        avatar(ctx, chs[n], x, y, 48); text(ctx, n, x, y + 78, 20, col=(0.2, 0.2, 0.25))
    text(ctx, "Sam  MATCH: Mom + Dad", 0, 170, 18, col=(0.2, 0.6, 0.3))
    if ruby_red:
        rrect(ctx, -130, 200, 260, 70, 12); ctx.set_source_rgb(0.95, 0.2, 0.2); ctx.fill(); text(ctx, "RUBY: 0%", 0, 248, 30, col=(1, 1, 1))


def scr_click_ruby(ctx, lt):
    scr_tree(ctx, lt)
    u = sm(clamp(lt / 0.6)); cx, cy = lerp(60, 85, u), lerp(240, 40, u)
    if lt > 0.65: ell(ctx, 80, 30, 60 + 30 * clamp((lt - 0.65) / 0.2), 60 + 30 * clamp((lt - 0.65) / 0.2)); ctx.set_source_rgba(0.2, 0.5, 1, 0.3 * (1 - clamp((lt - 0.65) / 0.3))); ctx.fill()
    poly(ctx, [(cx, cy), (cx, cy + 50), (cx + 13, cy + 38), (cx + 24, cy + 60), (cx + 33, cy + 55), (cx + 22, cy + 34), (cx + 38, cy + 33)]); fs(ctx, (1, 1, 1), 4)


def scr_zero(ctx, lt):
    app_header(ctx, "RUBY")
    p = back_out(clamp(lt / 0.25))
    ctx.save(); ctx.translate(0, -60); ctx.scale(p, p); text(ctx, "0%", 0, 40, 130, col=(0.92, 0.15, 0.15)); ctx.restore()
    text(ctx, "No close relatives", 0, 90, 22, col=(0.25, 0.25, 0.3)); text(ctx, "in your family", 0, 120, 22, col=(0.25, 0.25, 0.3))


def scr_matches(ctx, lt, highlight=0.0):
    app_header(ctx, "RUBY - MATCHES")
    scroll = 260 * sm(clamp(lt / 1.0))
    ctx.save(); ctx.translate(0, -scroll)
    rows = [("Distant cousin", "0.4%"), ("Distant cousin", "0.3%"), ("4th cousin", "0.9%"), ("Distant cousin", "0.2%"), ("5th cousin", "0.5%"),
            ("Karen Price", "50%"), ("Distant cousin", "0.3%")]
    for i, (n, p_) in enumerate(rows):
        y = -200 + i * 90
        k = n == "Karen Price"
        rrect(ctx, -140, y, 280, 76, 12); ctx.set_source_rgb(*((1, 0.93, 0.75) if k and highlight else (0.93, 0.94, 0.96))); ctx.fill()
        text(ctx, n, -120, y + 34, 20, col=(0.15, 0.15, 0.2), align="l"); text(ctx, p_, 120, y + 34, 22, col=(0.9, 0.3, 0.2) if k else (0.5, 0.5, 0.55), align="r")
        text(ctx, "Parent / Child" if k else "", -120, y + 62, 16, col=(0.85, 0.35, 0.2), align="l", weight=False)
    ctx.restore()


def scr_karen_card(ctx, lt):
    app_header(ctx, "MATCH FOUND")
    avatar(ctx, dict(KAREN, hair=(0.25, 0.25, 0.28)), 0, -130, 70)
    ctx.save(); ell(ctx, 0, -130, 70, 70); ctx.clip(); ctx.set_source_rgba(0.5, 0.5, 0.55, 0.85); ctx.paint(); ctx.restore()
    text(ctx, "?", 0, -105, 70, col=(1, 1, 1))
    text(ctx, "Karen Price", 0, -10, 34, col=(0.15, 0.15, 0.2))
    text(ctx, "Parent / Child", 0, 30, 24, col=(0.85, 0.35, 0.2))
    p = clamp(lt / 0.8)
    rrect(ctx, -120, 80, 240, 26, 13); ctx.set_source_rgb(0.9, 0.9, 0.92); ctx.fill()
    rrect(ctx, -120, 80, 240 * 0.5 * p / 0.5 if p < 1 else 120, 26, 13); ctx.set_source_rgb(0.95, 0.4, 0.25); ctx.fill()
    text(ctx, f"{int(50 * p)}% shared DNA", 0, 150, 24, col=(0.25, 0.25, 0.3))


def scr_chat(msgs, title="Karen Price", typing_t=None):
    def f(ctx, lt):
        ctx.rectangle(-160, -310, 320, 70); ctx.set_source_rgb(0.92, 0.92, 0.95); ctx.fill(); text(ctx, title, 0, -265, 22, col=(0.15, 0.15, 0.2))
        yy = -200
        for (m, mine, t0) in msgs:
            if lt < t0: continue
            a = back_out(clamp((lt - t0) / 0.3))
            ctx.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL); ctx.set_font_size(19)
            words = m.split(); lines_, cur = [], ""
            for w in words:
                if ctx.text_extents(cur + " " + w).x_advance > 200 and cur: lines_.append(cur); cur = w
                else: cur = (cur + " " + w).strip()
            lines_.append(cur)
            hgt = 20 + 26 * len(lines_); bx = -90 if mine else -140
            ctx.save(); ctx.translate(bx + 115, yy + hgt / 2); ctx.scale(a, a); ctx.translate(-(bx + 115), -(yy + hgt / 2))
            rrect(ctx, bx, yy, 230, hgt, 16); ctx.set_source_rgb(*((0.25, 0.55, 1.0) if mine else (0.88, 0.88, 0.9))); ctx.fill()
            for i, ln in enumerate(lines_): text(ctx, ln, bx + 14, yy + 30 + i * 26, 19, col=(1, 1, 1) if mine else (0.1, 0.1, 0.12), align="l", weight=False)
            ctx.restore(); yy += hgt + 16
        if typing_t is not None and typing_t[0] <= lt < typing_t[1]:
            rrect(ctx, -140, yy, 100, 50, 20); ctx.set_source_rgb(0.88, 0.88, 0.9); ctx.fill()
            for k in range(3):
                ell(ctx, -115 + k * 25, yy + 25 - 6 * max(0, sin(lt * 9 - k)), 7, 7); ctx.set_source_rgb(0.5, 0.5, 0.55); ctx.fill()
    return f


def scr_photo(ctx, lt, ch=None, sharp=1.0):
    ch = ch or HANNAH
    ctx.set_source_rgb(0.6, 0.8, 0.9); ctx.paint()
    draw_char(ctx, ch, dict(x=0, y=360, s=1.05, mood="happy", saccade=False), 0.3)
    if sharp < 1: ctx.set_source_rgba(0.85, 0.85, 0.88, 1 - sharp); ctx.paint()


def family_photo(ctx, ruby_circle=0.0, people=None):
    rrect(ctx, -420, -330, 840, 660, 10); fs(ctx, (0.45, 0.30, 0.18), 8)
    ctx.rectangle(-380, -290, 760, 580); ctx.set_source_rgb(0.75, 0.88, 0.80); ctx.fill()
    ctx.save(); ctx.rectangle(-380, -290, 760, 580); ctx.clip()
    people = people or [(DAD, -250, 0.82, -90), (MOM, -85, 0.80, -70), (RUBY, 85, 0.78, -60), (SAM, 250, 0.66, 0)]
    for ch, x, s_, hy in people:
        draw_char(ctx, ch, dict(x=x, y=hy + 340 * s_, s=s_, mood="happy", saccade=False), 0.3)
    ctx.restore()
    if ruby_circle > 0:
        ctx.new_path(); ctx.arc(90, -60, 115, -pi / 2, -pi / 2 + 2 * pi * ruby_circle); st(ctx, (0.95, 0.15, 0.15), 10)


def bracelets(ctx, lt, t_swap=0.6):
    u = sm(clamp((lt - t_swap) / 0.6))
    for i, (name, y) in enumerate((("BABY GIRL WELLS", -140), ("BABY GIRL PRICE", 140))):
        yy = lerp(y, -y, u); xx = 60 * sin(u * pi) * (1 if i == 0 else -1)
        rrect(ctx, -330 + xx, yy - 55, 660, 110, 55); fs(ctx, (1, 0.75, 0.82), 6)
        rrect(ctx, -230 + xx, yy - 32, 460, 64, 12); fs(ctx, (1, 1, 1), 3); text(ctx, name, xx, yy + 14, 38, col=(0.45, 0.25, 0.35))
    for k in (-1, 1):   # swap arrows
        if 0.2 < u < 0.95:
            ctx.new_path(); ctx.arc(k * 380, 0, 120, -pi / 2 * k, pi / 2 * k); st(ctx, (1, 1, 1), 10)


def cups(ctx, lt):
    ctx.set_source_rgb(0.45, 0.30, 0.20); ctx.paint()
    for k in range(6): ctx.rectangle(0, k * 330, 1080, 8); ctx.set_source_rgba(0, 0, 0, 0.15); ctx.fill()
    for i, (x, y) in enumerate(((280, 700), (780, 720), (300, 1220), (790, 1200))):
        ell(ctx, x, y + 30, 170, 150); fs(ctx, (0.95, 0.95, 0.95), 6)
        ell(ctx, x, y, 115, 105); fs(ctx, (1, 1, 1), 6); ell(ctx, x, y + 6, 92, 82); ctx.set_source_rgb(0.40, 0.24, 0.14); ctx.fill()
        ctx.move_to(x - 30, y + 10); ctx.curve_to(x - 10, y - 20, x + 10, y + 30, x + 30, y); st(ctx, (0.85, 0.70, 0.55), 6)
        for k in range(2):
            u = (lt * 0.5 + k * 0.5 + i * 0.13) % 1
            ell(ctx, x + 30 * sin(u * 6 + i), y - 60 - 200 * u, 25 + 25 * u, 20 + 15 * u); ctx.set_source_rgba(1, 1, 1, 0.35 * (1 - u)); ctx.fill()


def keys_bag(ctx, lt, which="keys"):
    ctx.set_source_rgb(0.45, 0.30, 0.20); ctx.paint()
    glow(ctx, 540, 900, 600, (1, 0.85, 0.6), 0.25)
    if which == "keys":
        rrect(ctx, 380, 820, 220, 320, 50); fs(ctx, (0.12, 0.12, 0.14), 7)
        ell(ctx, 490, 930, 55, 55); st(ctx, (0.75, 0.75, 0.8), 8); text(ctx, "LX", 490, 950, 50, col=(0.8, 0.8, 0.85))
        ell(ctx, 650, 780, 70, 70); st(ctx, (0.8, 0.8, 0.82), 12)
        poly(ctx, [(690, 740), (900, 560), (930, 590), (880, 640), (900, 660), (720, 790)]); fs(ctx, (0.8, 0.8, 0.85), 5)
    else:
        rrect(ctx, 250, 760, 580, 460, 60); fs(ctx, (0.75, 0.15, 0.25), 8)
        ctx.new_path(); ctx.arc(540, 760, 170, pi, 2 * pi); st(ctx, (0.55, 0.10, 0.18), 22)
        rrect(ctx, 480, 830, 120, 70, 12); fs(ctx, (1, 0.85, 0.3), 5)
        for k in range(5): ell(ctx, 300 + k * 120, 1150, 10, 10); ctx.set_source_rgb(1, 0.85, 0.3); ctx.fill()
    for k in range(3):
        a_ = lt * 3 + k * 2.1; sx, sy = 540 + 330 * cos(a_), 960 + 330 * sin(a_)
        star(ctx, sx, sy, 22); ctx.set_source_rgb(1, 1, 0.8); ctx.fill()


def hands_match(ctx, lt):
    ctx.set_source_rgb(0.55, 0.40, 0.28); ctx.paint()
    glow(ctx, 540, 960, 700, (1, 0.85, 0.6), 0.25)
    u = sm(clamp(lt / 0.6))
    for i, (x, sleeve) in enumerate(((lerp(300, 380, u), KAREN["top"]), (lerp(780, 700, u), RUBY["top"]))):
        ctx.save(); ctx.translate(x, 1000)
        rrect(ctx, -110, 250, 220, 500, 40); fs(ctx, sleeve, 7)
        rrect(ctx, -105, -60, 210, 330, 90); fs(ctx, RUBY["skin"], 7)
        for k in range(4): rrect(ctx, -95 + k * 52, -260 - 20 * (k in (1, 2)), 44, 230, 22); fs(ctx, RUBY["skin"], 6)
        rrect(ctx, -160 if i == 0 else 110, -80, 52, 170, 26); fs(ctx, RUBY["skin"], 6)
        ctx.restore()


def pancakes(ctx, lt):
    ctx.set_source_rgb(0.80, 0.74, 0.58); ctx.paint()
    ell(ctx, 540, 1000, 430, 330); fs(ctx, (1, 1, 1), 8); ell(ctx, 540, 1000, 360, 270); st(ctx, (0.85, 0.85, 0.88), 4)
    for k, (x, y, s_) in enumerate(((440, 980, 1.0), (640, 1030, 0.9), (540, 900, 0.85))):
        ctx.save(); ctx.translate(x, y); ctx.scale(s_ * 1.6, s_ * 1.4)
        ctx.move_to(0, 70); ctx.curve_to(-140, -10, -70, -110, 0, -40); ctx.curve_to(70, -110, 140, -10, 0, 70); fs(ctx, (0.92, 0.70, 0.35), 5)
        ctx.restore()
    for k in range(4):
        u = (lt * 0.5 + k / 4) % 1; ell(ctx, 420 + k * 80, 820 - 260 * u, 30 + 30 * u, 24 + 20 * u); ctx.set_source_rgba(1, 1, 1, 0.4 * (1 - u)); ctx.fill()
    rrect(ctx, 470, 760, 140, 90, 20); fs(ctx, (0.95, 0.8, 0.3), 4)


def fridge_cu(ctx, lt, focus=None):
    ctx.set_source_rgb(0.93, 0.93, 0.90); ctx.paint()
    rs = random.Random(11)
    for k in range(12):
        x, y = 140 + (k % 3) * 290, 260 + (k // 3) * 380
        ctx.save(); ctx.translate(x + 120, y + 150); ctx.rotate(rs.uniform(-0.15, 0.15))
        ctx.rectangle(-120, -150, 240, 300); fs(ctx, rs.choice([(1, 0.95, 0.75), (0.85, 0.92, 1), (1, 0.85, 0.9)]), 4)
        if k % 4 == 0:   # drawing of a house
            poly(ctx, [(-60, 0), (0, -60), (60, 0)]); fs(ctx, (0.9, 0.3, 0.3), 3); ctx.rectangle(-50, 0, 100, 80); fs(ctx, (0.95, 0.85, 0.4), 3)
        elif k % 4 == 1:  # stick family
            for j in range(3):
                ell(ctx, -60 + j * 60, -40, 18, 18); st(ctx, OUTL, 4); ctx.move_to(-60 + j * 60, -22); ctx.line_to(-60 + j * 60, 50); st(ctx, OUTL, 4)
        elif k % 4 == 2:
            text(ctx, "A+", 0, 30, 90, col=(0.85, 0.2, 0.2))
        else:
            star(ctx, 0, 0, 70); fs(ctx, (1, 0.8, 0.2), 4)
        ell(ctx, 0, -140, 16, 16); ctx.set_source_rgb(0.9, 0.2, 0.3); ctx.fill()
        ctx.restore()
    if focus == "medals":
        for k in range(3):
            x = 300 + k * 240; ctx.move_to(x - 40, 500); ctx.line_to(x, 760); ctx.line_to(x + 40, 500); st(ctx, (0.2, 0.4, 0.8), 20)
            ell(ctx, x, 830, 90, 90); fs(ctx, (1, 0.8, 0.25), 6); text(ctx, str(k + 1), x, 860, 80, col=(0.75, 0.5, 0.1))
    if focus == "teeth":
        rrect(ctx, 290, 760, 500, 380, 40); fs(ctx, (0.95, 0.75, 0.8), 7)
        text(ctx, "Hannah's first tooth", 540, 830, 38, col=(0.5, 0.25, 0.35))
        for k in range(3): rrect(ctx, 400 + k * 110, 900, 70, 90, 25); fs(ctx, (1, 1, 1), 4)


def suitcase(ctx, x, y, s, col):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -120, -170, 240, 340, 30); fs(ctx, col, 6)
    rrect(ctx, -50, -230, 100, 70, 20); st(ctx, OUTL, 12)
    for k in (-60, 60): ctx.move_to(k, -160); ctx.line_to(k, 160); st(ctx, shade(col, 0.25), 6)
    ctx.restore()


def calendar_card(ctx, lt, top, big, flip_t=None):
    ctx.save()
    rrect(ctx, -260, -300, 520, 600, 30); fs(ctx, (1, 1, 1), 8)
    rrect(ctx, -260, -300, 520, 150, 30); ctx.set_source_rgb(0.9, 0.15, 0.2); ctx.fill(); ctx.rectangle(-260, -200, 520, 50); ctx.fill()
    text(ctx, top, 0, -205, 60, col=(1, 1, 1)); text(ctx, big, 0, 120 if len(big) <= 3 else 90, 190 if len(big) <= 3 else 120, col=(0.12, 0.12, 0.16))
    for x in (-150, 150): ell(ctx, x, -300, 22, 22); fs(ctx, (0.75, 0.75, 0.8), 5)
    ctx.restore()


# ---------------- generic shots ----------------
def ECU(ch, mood, bg="living", spk=None, s=2.7, hy=860, x=540, blur=18, z=(1.0, 1.12), amp=0, dark=0.0, vertigo=False, fx=None, post=None, **P):
    def f(ctx, lt, d):
        dx, dy = shake(lt, amp)
        ctx.save(); cam(ctx, punch(lt) * lerp(z[0], z[1], sm(lt / d)), 540, hy + 60, dx=dx, dy=dy)
        if vertigo:
            ctx.save(); vz = 1 + 0.45 * sm(lt / d); ctx.translate(540, hy); ctx.scale(vz, vz); ctx.translate(-540, -hy); BG(ctx, bg, blur); ctx.restore()
        else: BG(ctx, bg, blur)
        mo = mood(lt) if callable(mood) else mood
        PP = dict(x=x, y=head_y(s, hy), s=s, mood=mo, mouth=talkT(spk) if spk else 0.0, dark=dark); PP.update(P)
        draw_char(ctx, ch, PP, CUR["t"])
        if fx: fx(ctx, lt, d, PP)
        ctx.restore()
        if post: post(ctx, lt, d)
    return f


def MED(cast, bg, blur=5, z=(1.0, 1.08), cx=540, cy=1050, fg=None, fx=None, post=None, amp=0, pan=0):
    """cast: list of (ch, x, hy, s, mood, spk, extraP)"""
    def f(ctx, lt, d):
        dx, dy = shake(lt, amp)
        ctx.save(); cam(ctx, punch(lt, 0.04) * lerp(z[0], z[1], sm(lt / d)), cx + pan * sm(lt / d), cy, dx=dx, dy=dy)
        BG(ctx, bg, blur)
        for c in cast:
            ch, x, hy, s, mood, spk = c[:6]; ex = c[6] if len(c) > 6 else {}
            mo = mood(lt) if callable(mood) else mood
            PP = dict(x=x, y=head_y(s, hy), s=s, mood=mo, mouth=talkT(spk) if spk else 0.0)
            PP.update(ex(lt) if callable(ex) else ex)
            draw_char(ctx, ch, PP, CUR["t"])
        if fg: fg(ctx, lt, d)
        if fx: fx(ctx, lt, d)
        ctx.restore()
        if post: post(ctx, lt, d)
    return f


def INS(draw, bg=None, blur=16, z=(1.0, 1.14), rot=0.0, cy=960, amp=0, dim=0.0, post=None):
    def f(ctx, lt, d):
        dx, dy = shake(lt, amp)
        ctx.save(); cam(ctx, punch(lt, 0.06) * lerp(z[0], z[1], sm(lt / d)), 540, cy, rot=rot, dx=dx, dy=dy)
        if bg: BG(ctx, bg, blur)
        if dim: overlay(ctx, (0, 0, 0), dim)
        draw(ctx, lt, d)
        ctx.restore()
        if post: post(ctx, lt, d)
    return f


def PHONE(screen, bg="bedroom_night", blur=20, s=2.1, rot=-0.04, y=980, glow_a=0.3, amp=0, z=(1.0, 1.1), post=None):
    return INS(lambda c, lt, d: phone(c, 540, y, s, rot, screen, lt, glow_a), bg=bg, blur=blur, z=z, amp=amp, post=post)


def LAPTOP(screen, bg="living_dark", blur=16, z=(1.0, 1.1), post=None):
    def draw(ctx, lt, d):
        poly(ctx, [(60, 1500), (1020, 1500), (1180, 1760), (-100, 1760)]); fs(ctx, (0.75, 0.76, 0.8), 7)
        rrect(ctx, 90, 420, 900, 1080, 30); fs(ctx, (0.15, 0.15, 0.18), 7)
        glow(ctx, 540, 960, 700, (0.6, 0.8, 1), 0.25)
        ctx.save(); ctx.translate(540, 960); ctx.scale(2.6, 1.65); ctx.rectangle(-160, -310, 320, 620); ctx.clip()
        ctx.set_source_rgb(0.97, 0.97, 0.98); ctx.paint(); screen(ctx, lt); ctx.restore()
    return INS(draw, bg=bg, blur=blur, z=z, post=post)


def END(title, lines, t_end, base=None):
    def f(ctx, lt, d):
        if base: base(ctx, lt, d)
        end_card(ctx, CUR["t"], t_end, title, lines)
    return f


def L(s, t0, x=540, y=520, size=72, rot=-0.08, col=(1, 1, 1)):
    return lambda ctx, lt, d: label(ctx, lt, t0, s, x, y, size, rot, col)


def chain(*fs_):
    def f(ctx, lt, d, *a):
        for g in fs_: g(ctx, lt, d, *a)
    return f


# ---------------- scene assembly ----------------
def cuts(sc, *specs):
    out = [0.0]
    for sp in specs:
        if isinstance(sp, (int, float)): out.append(float(sp))
        elif isinstance(sp, str): out.append(WT(sc, sp) - 0.06)
        else: out.append(WT(sc, *sp) - 0.06)
    out.append(DUR(sc) + 0.5)
    return out


def SC(sc, specs, fns, whips=()):
    ts = cuts(sc, *specs)
    assert len(fns) == len(ts) - 1, (sc, len(fns), len(ts))
    lst = [(ts[i], ts[i + 1], fns[i]) for i in range(len(fns))]
    return lst, {ts[i]: "whip" for i in whips}


HUD = None
exec(open(f"{HERE}/{PART}_shots.py").read())   # defines SHOTS and HEADER


def draw_shot_at(ctx, sc, t):
    lst, _ = SHOTS[sc]
    for t0, t1, fn in lst:
        if t0 <= t < t1:
            ctx.save(); fn(ctx, t - t0, min(t1, DUR(sc)) - t0); ctx.restore(); return


WHIP = 0.13


def draw_scene(ctx, sc, t):
    lst, trans = SHOTS[sc]
    for tb in trans:
        if abs(t - tb) < WHIP:
            u = (t - tb) / WHIP
            off = u * 1100 if u < 0 else (u - 1) * 1100
            ctx.push_group(); draw_shot_at(ctx, sc, t); pat = ctx.pop_group()
            ctx.set_source_rgb(0, 0, 0); ctx.paint()
            n = 9; ctx.save(); ctx.set_operator(ADD)
            for k in range(n):
                ctx.save(); ctx.translate(-off - k * 38, 0); ctx.set_source(pat); ctx.paint_with_alpha(1 / n); ctx.restore()
            ctx.restore(); return
    draw_shot_at(ctx, sc, t)


COLS = {"N": (1, 1, 1), "RU": (0.45, 0.9, 0.95), "MO": (1, 0.65, 0.8), "DA": (1, 0.86, 0.15), "SAM": (0.6, 1, 0.5), "HA": (1, 0.6, 0.4), "KA": (1, 0.85, 0.5)}
COLS.update(globals().get("COLS_EXTRA", {}))


def captions(ctx, sc, t):
    cur = None
    for ln in TL[sc]["lines"]:
        ws = ln["words"]
        for i, w in enumerate(ws):
            end = ws[i + 1][1] if i + 1 < len(ws) else w[2] + 0.2
            if w[1] - 0.04 <= t < end: cur = (w, ln["spk"])
    if not cur: return
    w, spk = cur
    word = w[0].upper().strip(",.")
    p = back_out(clamp((t - w[1] + 0.04) / 0.1))
    ctx.save(); ctx.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(104)
    e = ctx.text_extents(word); k = min(1.0, 940 / max(1, e.x_advance)) * (0.75 + 0.25 * p)
    ctx.translate(540, 1390); ctx.scale(k, k)
    ctx.new_path(); ctx.move_to(-e.x_advance / 2, 8); ctx.text_path(word); ctx.set_source_rgba(0, 0, 0, 0.5); ctx.fill()
    ctx.new_path(); ctx.move_to(-e.x_advance / 2, 0); ctx.text_path(word)
    ctx.set_source_rgb(0, 0, 0); ctx.set_line_width(18); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
    ctx.set_source_rgb(*COLS.get(spk, (1, 1, 1))); ctx.fill()
    ctx.restore()


def frame(surf, sc, t):
    CUR["sc"], CUR["t"] = sc, t
    ctx = cairo.Context(surf)
    ctx.set_source_rgb(0, 0, 0); ctx.paint()
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    draw_scene(ctx, sc, t)
    if globals().get("LIGHT"): apply_light(surf, LIGHT(sc, t), t)
    ctx.set_operator(cairo.OPERATOR_OVER)
    grain(ctx, t, 0.045)
    if HUD and not (sc == LAST and t > END_T): HUD(ctx, sc, t)
    if not (sc == LAST and t > END_T): captions(ctx, sc, t)
    if globals().get("HOOK") and sc == FIRST and t < HOOK_T: hook_card(ctx, t)
    P1.header(ctx)


HOOK_T = 2.2
import numpy as _np
from PIL import Image as _Image, ImageFilter as _IF
_YY, _XX = _np.mgrid[0:480, 0:270].astype(_np.float32)


def apply_light(surf, L, t):
    """Cinematic pass: ambient + coloured soft lights multiply the frame, then bloom, haze and vignette.
    L: dict(amb=(r,g,b), lights=[(x, y, rx, ry, (r,g,b), k), ...], bloom=0.8, thr=0.6, haze=0.0, vig=0.55, gamma=1.1)"""
    if not L: return
    surf.flush(); w, h = surf.get_width(), surf.get_height()
    buf = _np.frombuffer(surf.get_data(), _np.uint8).reshape(h, surf.get_stride())[:, :w * 4].reshape(h, w, 4)
    img = buf[..., [2, 1, 0]].astype(_np.float32) / 255
    lm = _np.ones((480, 270, 3), _np.float32) * _np.array(L.get("amb", (0.4, 0.4, 0.5)), _np.float32)
    haze = _np.zeros_like(lm)
    for (x, y, rx, ry, col, k) in L.get("lights", []):
        g = _np.exp(-(((_XX - x / 4) / (rx / 4)) ** 2 + ((_YY - y / 4) / (ry / 4)) ** 2))[..., None]
        lm += g * _np.array(col, _np.float32) * k
        haze += g * _np.array(col, _np.float32) * k
    vig = L.get("vig", 0.55)
    v = 1 - vig * _np.clip(((_XX - 135) / 190) ** 2 + ((_YY - 240) / 340) ** 2, 0, 1)
    lm *= v[..., None]
    lm_full = _np.asarray(_Image.fromarray(_np.clip(lm / 2 * 255, 0, 255).astype(_np.uint8)).resize((w, h), _Image.BILINEAR), _np.float32) / 255 * 2
    out = _np.clip(img * lm_full, 0, 1) ** L.get("gamma", 1.1)
    hz = L.get("haze", 0.0)
    if hz:
        hf = _np.asarray(_Image.fromarray(_np.clip(haze / 2 * 255, 0, 255).astype(_np.uint8)).resize((w, h), _Image.BILINEAR), _np.float32) / 255 * 2
        out = out + hf * hz
    bl = L.get("bloom", 0.8)
    if bl:
        small = _Image.fromarray((_np.clip(out - L.get("thr", 0.6), 0, 1) * 255).astype(_np.uint8)).resize((w // 6, h // 6), _Image.BILINEAR).filter(_IF.GaussianBlur(9))
        out = out + _np.asarray(small.resize((w, h), _Image.BILINEAR), _np.float32) / 255 * bl
    out = (_np.clip(out, 0, 1) * 255).astype(_np.uint8)
    buf[..., 2] = out[..., 0]; buf[..., 1] = out[..., 1]; buf[..., 0] = out[..., 2]
    surf.mark_dirty()


def hook_card(ctx, t):
    a = 1 - clamp((t - HOOK_T + 0.25) / 0.25)
    ctx.save(); ctx.push_group()
    ctx.rectangle(0, 0, 1080, 1920); ctx.set_source_rgba(0, 0, 0, 0.45); ctx.fill()
    lines = HOOK
    for i, (s_, col) in enumerate(lines):
        p = back_out(clamp((t - 0.08 * i) / 0.22))
        ctx.save(); ctx.translate(540, 700 + i * 150); ctx.scale(p, p); ctx.rotate(-0.03)
        ctx.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        size = 118; ctx.set_font_size(size); e = ctx.text_extents(s_)
        k = min(1.0, 980 / max(1, e.x_advance)); ctx.scale(k, k)
        ctx.new_path(); ctx.move_to(-e.x_advance / 2, size * 0.35); ctx.text_path(s_)
        ctx.set_source_rgb(0, 0, 0); ctx.set_line_width(26); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
        ctx.set_source_rgb(*col); ctx.fill(); ctx.restore()
    ctx.pop_group_to_source(); ctx.paint_with_alpha(a); ctx.restore()


def render(sc):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    n = TL[sc]["frames"]; os.makedirs(f"{EP}/scenes", exist_ok=True)
    tmp = f"{EP}/scenes/{sc}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(n):
        frame(surf, sc, i / FPS); surf.flush(); p.stdin.write(bytes(surf.get_data()))
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, f"{EP}/scenes/{sc}.mp4"); print("done", sc, n)
    else: print("FAILED", sc)


P1.HEADER[:] = HEADER
LAST = list(TL)[-1]
FIRST = list(TL)[0]

if __name__ == "__main__":
    os.makedirs(f"{EP}/preview", exist_ok=True)
    if sys.argv[2] == "preview":
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        for arg in sys.argv[3:]:
            sc, ts = arg.split(":"); frame(surf, sc, float(ts)); surf.write_to_png(f"{EP}/preview/{sc}_{ts}.png")
    elif sys.argv[2] == "mids":
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        for sc, (lst, _) in SHOTS.items():
            for t0, t1, _f in lst:
                tm = (t0 + min(t1, DUR(sc))) / 2; frame(surf, sc, tm); surf.write_to_png(f"{EP}/preview/{sc}_{tm:05.2f}.png")
    else:
        for sc in (sys.argv[3:] or TL.keys()): render(sc)
