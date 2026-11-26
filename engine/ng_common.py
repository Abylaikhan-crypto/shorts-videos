"""Characters, sets and props for 'The New Girl Knew All My Secrets'."""
import cairo, random
from math import sin, cos, pi
from rig import *
import part1 as P1
import part1v2 as V
from ep_common import end_card, house_day
from twins_common import char_ecu, hand_world, text_bubble_phone

ADD = cairo.OPERATOR_ADD
MIA = dict(skin=(0.98, 0.86, 0.76), hair=(0.80, 0.38, 0.15), hairstyle="bob", outfit="sweater", top=(0.45, 0.60, 0.40),
           eye=(0.2, 0.35, 0.55), blush=True, seed=31, pants=(0.30, 0.32, 0.45), shoes=(0.85, 0.85, 0.88))
HARPER = dict(skin=(0.98, 0.85, 0.74), hair=(0.96, 0.82, 0.48), hairstyle="long", outfit="cardigan", top=(0.98, 0.58, 0.72),
              no_lanyard=True, eye=(0.2, 0.35, 0.6), blush=True, seed=32, pants=(0.95, 0.95, 0.97), shoes=(0.98, 0.6, 0.72))
DEV = dict(skin=(0.60, 0.42, 0.30), hair=(0.10, 0.07, 0.05), hairstyle="crew", outfit="hoodie", top=(0.35, 0.42, 0.56), seed=33,
           pants=(0.2, 0.22, 0.28))
CHLOE = dict(skin=(0.88, 0.66, 0.52), hair=(0.35, 0.15, 0.10), hairstyle="bun", outfit="hoodie", top=(0.16, 0.16, 0.20), seed=34)
ETHAN = dict(skin=(0.93, 0.76, 0.62), hair=(0.08, 0.06, 0.05), hairstyle="crew", outfit="hoodie", top=(0.80, 0.22, 0.22), seed=35)
GRANT = dict(skin=(0.88, 0.68, 0.54), hair=(0.62, 0.62, 0.64), hairstyle="crew", outfit="suit", top=(0.45, 0.33, 0.24), beard=True, seed=36, no_badge=True)


def bear(ctx, x, y, s=1.0, t=0.0, red=0.0, opened=False):
    """Mr. Buttons. red = LED glow in his left button eye (0..1)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    br = (0.62, 0.42, 0.26)
    blob(ctx, [(0, 40, 85), (-70, 100, 38), (70, 100, 38), (-80, 0, 30), (80, 0, 30)], br)
    blob(ctx, [(0, -90, 80), (-62, -150, 30), (62, -150, 30)], br)
    for sx in (-1, 1): ell(ctx, sx * 62, -150, 15, 15); ctx.set_source_rgb(0.85, 0.65, 0.5); ctx.fill()
    ell(ctx, 0, -62, 36, 28); fs(ctx, (0.85, 0.68, 0.50), 4)
    ell(ctx, 0, -76, 11, 8); ctx.set_source_rgb(0.15, 0.08, 0.05); ctx.fill()
    ctx.move_to(0, -68); ctx.line_to(0, -52); ctx.move_to(-12, -48); ctx.curve_to(-4, -42, 4, -42, 12, -48); st(ctx, (0.15, 0.08, 0.05), 3.5)
    for sx in (-1, 1):
        ell(ctx, sx * 30, -108, 13, 13); fs(ctx, (0.08, 0.08, 0.1), 3)
        for (dx, dy) in ((-4, -4), (4, -4), (-4, 4), (4, 4)):
            ell(ctx, sx * 30 + dx, -108 + dy, 1.8, 1.8); ctx.set_source_rgb(0.4, 0.4, 0.45); ctx.fill()
    if red > 0:
        glow(ctx, 30, -108, 60, (1, 0.1, 0.1), 0.9 * red)
        ell(ctx, 30, -108, 6, 6); ctx.set_source_rgba(1, 0.2, 0.2, red); ctx.fill()
    ell(ctx, 0, 50, 45, 50); ctx.set_source_rgb(0.80, 0.60, 0.42); ctx.fill()
    ctx.restore()


def desk_room(ctx, t, night=True, lamp=True, bear_red=0.0, diary=True, bear_on=True):
    wall = (0.22, 0.30, 0.38) if night else (0.65, 0.80, 0.82)
    ctx.set_source_rgb(*wall); ctx.paint()
    for x in range(0, 1080, 90):
        ctx.rectangle(x, 0, 45, 1300); ctx.set_source_rgba(1, 1, 1, 0.04); ctx.fill()
    ctx.rectangle(560, 330, 400, 480); fs(ctx, (0.05, 0.07, 0.18) if night else (0.78, 0.92, 1.0))
    if night:
        ell(ctx, 860, 430, 34, 34); ctx.set_source_rgb(0.95, 0.94, 0.85); ctx.fill()
    ctx.move_to(760, 330); ctx.line_to(760, 810); ctx.move_to(560, 570); ctx.line_to(960, 570); st(ctx, (0.9, 0.9, 0.85), 10)
    rrect(ctx, 90, 380, 300, 220, 8); fs(ctx, (0.85, 0.80, 0.70))
    for k in range(4): ctx.rectangle(110 + k * 70, 400, 50, 70); ctx.set_source_rgb(*[(0.9, 0.5, 0.5), (0.5, 0.7, 0.9), (0.95, 0.8, 0.4), (0.6, 0.8, 0.6)][k]); ctx.fill()
    ctx.rectangle(0, 1300, 1080, 700); ctx.set_source_rgb(0.30, 0.22, 0.18); ctx.fill()
    if lamp:
        ctx.move_to(170, 1300); ctx.line_to(220, 1050); ctx.line_to(320, 980); st(ctx, (0.25, 0.25, 0.3), 10)
        poly(ctx, [(270, 950), (390, 960), (370, 1040), (290, 1030)]); fs(ctx, (0.95, 0.85, 0.5))
        glow(ctx, 330, 1150, 420, (1, 0.85, 0.5), 0.45 if night else 0.15)
    if bear_on:
        bear(ctx, 840, 1180, 1.0, t, red=bear_red)


def desk_front(ctx, t, diary=True, open_=True):
    ctx.rectangle(-10, 1290, 1100, 40); fs(ctx, (0.62, 0.45, 0.30))
    ctx.rectangle(-10, 1325, 1100, 700); fs(ctx, (0.52, 0.37, 0.24))
    if diary:
        if open_:
            poly(ctx, [(330, 1300), (520, 1290), (520, 1320), (330, 1328)]); fs(ctx, (0.98, 0.96, 0.9), 3)
            poly(ctx, [(520, 1290), (700, 1300), (700, 1328), (520, 1320)]); fs(ctx, (0.98, 0.96, 0.9), 3)
        else:
            rrect(ctx, 400, 1295, 240, 30, 6); fs(ctx, (0.55, 0.20, 0.35), 3)


def bearcam(ctx, t, draw_scene, stamp="02:13 AM"):
    """POV of the hidden camera: green tint, fisheye vignette, REC overlay."""
    ctx.save(); ctx.translate(540, 960); ctx.scale(1.15, 1.15); ctx.translate(-540, -960)
    draw_scene(ctx, t)
    ctx.restore()
    overlay(ctx, (0.1, 0.35, 0.15), 0.35, cairo.OPERATOR_MULTIPLY)
    overlay(ctx, (0.05, 0.25, 0.08), 0.18, ADD)
    rs = random.Random(int(t * 30))
    for _ in range(140):
        ctx.rectangle(rs.uniform(0, 1080), rs.uniform(0, 1920), 3, 3); ctx.set_source_rgba(1, 1, 1, 0.08); ctx.fill()
    g = cairo.RadialGradient(540, 960, 350, 540, 960, 1100); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.95)
    ctx.set_source(g); ctx.paint()
    if (t * 1.6) % 1 < 0.6:
        ell(ctx, 120, 300, 14, 14); ctx.set_source_rgb(0.95, 0.15, 0.15); ctx.fill()
    text(ctx, "REC", 150, 312, 34, col=(0.95, 0.95, 0.95), align="l")
    text(ctx, stamp, 960, 312, 34, col=(0.95, 0.95, 0.95), align="r")
    for (x0, y0, dx, dy) in [(80, 380, 1, 1), (1000, 380, -1, 1), (80, 1560, 1, -1), (1000, 1560, -1, -1)]:
        ctx.move_to(x0, y0 + dy * 70); ctx.line_to(x0, y0); ctx.line_to(x0 + dx * 70, y0); st(ctx, (0.95, 0.95, 0.95), 6)


def classroom(ctx, t):
    ctx.set_source_rgb(0.80, 0.84, 0.74); ctx.paint()
    rrect(ctx, 140, 300, 800, 420, 10); fs(ctx, (0.55, 0.40, 0.25))
    ctx.rectangle(165, 325, 750, 370); ctx.set_source_rgb(0.18, 0.32, 0.25); ctx.fill()
    text(ctx, "Chapter 7: The Water Cycle", 540, 430, 40, col=(0.9, 0.9, 0.85), weight=False)
    ctx.new_path(); ctx.arc(540, 590, 70, pi, 2 * pi); st(ctx, (0.9, 0.9, 0.85), 5)
    ctx.rectangle(0, 1450, 1080, 500); ctx.set_source_rgb(0.62, 0.55, 0.45); ctx.fill()
    for x in (60, 860):
        rrect(ctx, x, 1180, 160, 30, 6); fs(ctx, (0.75, 0.6, 0.4))


def school_desk(ctx):
    ctx.rectangle(-10, 1360, 1100, 40); fs(ctx, (0.80, 0.65, 0.42))
    ctx.rectangle(-10, 1395, 1100, 600); fs(ctx, (0.68, 0.54, 0.34))
    ctx.rectangle(530, 1395, 20, 600); ctx.set_source_rgba(0, 0, 0, 0.15); ctx.fill()


def cafeteria(ctx, t):
    ctx.set_source_rgb(0.96, 0.90, 0.72); ctx.paint()
    for x in range(80, 1080, 330):
        ctx.rectangle(x, 340, 230, 380); fs(ctx, (0.80, 0.92, 1.0))
        ctx.move_to(x + 115, 340); ctx.line_to(x + 115, 720); st(ctx, (1, 1, 1), 8)
    ctx.rectangle(0, 1450, 1080, 500); ctx.set_source_rgb(0.75, 0.72, 0.68); ctx.fill()
    rrect(ctx, 380, 820, 320, 90, 10); fs(ctx, (0.9, 0.3, 0.25)); text(ctx, "CAFETERIA", 540, 880, 44, col=(1, 1, 1))


def lunch_table(ctx):
    ctx.rectangle(-10, 1370, 1100, 36); fs(ctx, (0.85, 0.85, 0.88))
    ctx.rectangle(-10, 1400, 1100, 600); fs(ctx, (0.55, 0.62, 0.72))
    for x in (220, 860):
        rrect(ctx, x - 90, 1345, 180, 40, 6); fs(ctx, (0.92, 0.5, 0.35), 3)
        ell(ctx, x - 30, 1350, 30, 10); ctx.set_source_rgb(0.95, 0.85, 0.4); ctx.fill()


def oak_scene(ctx, t):
    gr = cairo.LinearGradient(0, 0, 0, 1200); gr.add_color_stop_rgb(0, 0.65, 0.82, 0.98); gr.add_color_stop_rgb(1, 0.92, 0.95, 1.0)
    ctx.set_source(gr); ctx.paint()
    ctx.rectangle(-10, 760, 520, 560); fs(ctx, (0.80, 0.55, 0.45))
    for k in range(3):
        for j in range(2): ctx.rectangle(40 + k * 150, 820 + j * 180, 90, 110); fs(ctx, (0.75, 0.88, 0.98), 3)
    ctx.rectangle(0, 1300, 1080, 700); ctx.set_source_rgb(0.42, 0.65, 0.35); ctx.fill()
    poly(ctx, [(620, 1420), (700, 700), (860, 700), (940, 1420)]); fs(ctx, (0.45, 0.30, 0.18))
    for (dx, dy, r) in [(-150, -60, 230), (130, -90, 250), (0, -230, 260), (-280, 80, 170), (300, 60, 180)]:
        ell(ctx, 780 + dx, 600 + dy, r, r * 0.85); ctx.set_source_rgb(0.30, 0.55, 0.28); ctx.fill()
    ell(ctx, 780, 1050, 50, 80); ctx.set_source_rgb(0.15, 0.08, 0.04); ctx.fill()


def workbench(ctx, t):
    ctx.set_source_rgb(0.18, 0.20, 0.26); ctx.paint()
    for (x, y) in [(120, 380), (560, 380)]:
        rrect(ctx, x, y, 400, 260, 12); fs(ctx, (0.08, 0.08, 0.1), 5)
        ctx.rectangle(x + 16, y + 16, 368, 228); ctx.set_source_rgb(0.05, 0.12, 0.10); ctx.fill()
        for k in range(8):
            ctx.rectangle(x + 30, y + 34 + k * 26, 80 + (k * 53) % 220, 10); ctx.set_source_rgb(0.3, 0.9, 0.5); ctx.fill()
    ctx.rectangle(0, 1300, 1080, 700); ctx.set_source_rgb(0.40, 0.30, 0.22); ctx.fill()
    for (x, w, c) in [(80, 30, (0.8, 0.2, 0.2)), (130, 20, (0.9, 0.8, 0.2)), (930, 40, (0.6, 0.6, 0.65))]:
        rrect(ctx, x, 1180, w, 120, 6); fs(ctx, c, 3)


def bench_front(ctx):
    ctx.rectangle(-10, 1290, 1100, 40); fs(ctx, (0.55, 0.42, 0.30))
    ctx.rectangle(-10, 1325, 1100, 700); fs(ctx, (0.45, 0.34, 0.24))


def chip_cu(ctx, t, tt):
    ctx.set_source_rgb(0.62, 0.42, 0.26); ctx.paint()
    for k in range(60):
        rs = random.Random(k)
        ctx.move_to(rs.uniform(0, 1080), rs.uniform(0, 1920)); ctx.rel_line_to(rs.uniform(-30, 30), rs.uniform(10, 50)); st(ctx, (0.55, 0.36, 0.22), 4)
    z = 1.0 + 0.12 * sm(tt)
    ctx.save(); ctx.translate(540, 900); ctx.scale(z, z); ctx.translate(-540, -900)
    ell(ctx, 540, 900, 380, 380); ctx.set_source_rgb(0.95, 0.92, 0.85); ctx.fill()
    rrect(ctx, 360, 720, 360, 360, 20); fs(ctx, (0.10, 0.35, 0.18), 6)
    for k in range(6):
        ctx.move_to(390, 760 + k * 50); ctx.line_to(690, 760 + k * 50); st(ctx, (0.85, 0.7, 0.3), 3)
    ell(ctx, 540, 900, 90, 90); fs(ctx, (0.08, 0.08, 0.1), 6); ell(ctx, 540, 900, 50, 50); ctx.set_source_rgb(0.15, 0.25, 0.5); ctx.fill()
    ell(ctx, 520, 880, 14, 14); ctx.set_source_rgb(1, 1, 1); ctx.fill()
    if (t * 1.6) % 1 < 0.6:
        ell(ctx, 660, 760, 16, 16); ctx.set_source_rgb(1, 0.15, 0.15); ctx.fill(); glow(ctx, 660, 760, 70, (1, 0.1, 0.1), 0.8)
    ctx.move_to(720, 1000); ctx.curve_to(820, 1060, 860, 1200, 940, 1260); st(ctx, (0.2, 0.2, 0.25), 10)
    text(ctx, "WiFi", 640, 1050, 34, col=(0.9, 0.9, 0.9))
    ctx.restore()


def video_call(ctx, t, who, mood, mouth=0.0, s=2.1, y=980, title="Chloe"):
    ctx.save(); ctx.translate(540, y); ctx.scale(s, s)
    rrect(ctx, -170, -330, 340, 660, 40); fs(ctx, (0.12, 0.12, 0.14), 5)
    ctx.save(); rrect(ctx, -155, -310, 310, 620, 28); ctx.clip()
    ctx.set_source_rgb(0.25, 0.22, 0.30); ctx.paint()
    glow(ctx, 0, -60, 260, (0.6, 0.5, 0.9), 0.3)
    draw_char(ctx, who, dict(x=0, y=430, s=1.25, mood=mood, mouth=mouth, saccade=False), t)
    ctx.rectangle(-155, -310, 310, 54); ctx.set_source_rgba(0, 0, 0, 0.35); ctx.fill()
    text(ctx, title, 0, -275, 22, col=(1, 1, 1))
    ell(ctx, 0, 270, 26, 26); ctx.set_source_rgb(0.9, 0.2, 0.2); ctx.fill()
    ctx.restore(); ctx.restore()


def laptop_email(ctx, t, tt):
    ctx.set_source_rgb(0.30, 0.25, 0.22); ctx.paint()
    z = 1.0 + 0.06 * sm(tt)
    ctx.save(); ctx.translate(540, 900); ctx.scale(z, z); ctx.translate(-540, -900)
    rrect(ctx, 70, 480, 940, 640, 24); fs(ctx, (0.15, 0.15, 0.18), 5)
    ctx.rectangle(100, 510, 880, 580); ctx.set_source_rgb(0.98, 0.98, 1.0); ctx.fill()
    ctx.rectangle(100, 510, 880, 70); ctx.set_source_rgb(0.9, 0.92, 0.96); ctx.fill()
    for i, (lab, val) in enumerate([("From:", "Mr. D. Grant"), ("To:", "Mr. & Mrs. Hayes"), ("Subject:", "Final exam incident - hallway camera")]):
        text(ctx, lab, 130, 640 + i * 60, 30, col=(0.45, 0.45, 0.5), align="l")
        text(ctx, val, 300, 640 + i * 60, 30, col=(0.1, 0.1, 0.15), align="l", weight=(i == 2))
    for k in range(5):
        ctx.rectangle(130, 840 + k * 40, 700 - (k * 90) % 300, 14); ctx.set_source_rgb(0.75, 0.75, 0.8); ctx.fill()
    rrect(ctx, 130, 1010, 320, 60, 10); fs(ctx, (0.85, 0.9, 1.0), 2); text(ctx, "camera_0612.mp4", 290, 1050, 24, col=(0.2, 0.35, 0.7))
    ctx.rectangle(30, 1120, 1020, 40); fs(ctx, (0.2, 0.2, 0.24))
    ctx.restore()
