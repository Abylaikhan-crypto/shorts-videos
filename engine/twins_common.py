"""Characters, sets and props for 'My Twin Stole My Life'."""
import cairo, random, math
from math import sin, cos, pi
from rig import *
import part1 as P1
import part1v2 as V
from ep_common import old_phone, end_card, house_day

ADD = cairo.OPERATOR_ADD
HAIR = (0.30, 0.18, 0.10)
SKIN = (0.93, 0.76, 0.64)
LILY = dict(skin=SKIN, hair=HAIR, hairstyle="long", outfit="hoodie", top=(0.98, 0.76, 0.22), eye=(0.25, 0.32, 0.18),
            blush=True, seed=21, pants=(0.30, 0.38, 0.58), shoes=(0.95, 0.95, 0.95))
LANA = dict(LILY, hairstyle="bun", outfit="longsleeve", top=(0.30, 0.22, 0.40), seed=22, pants=(0.12, 0.12, 0.15), shoes=(0.1, 0.1, 0.12))
MOM2 = dict(skin=(0.95, 0.80, 0.68), hair=(0.16, 0.10, 0.08), hairstyle="bob", outfit="sweater", top=(0.28, 0.55, 0.60), seed=23,
            eye=(0.2, 0.25, 0.2), blush=True)
DAD = dict(skin=(0.92, 0.74, 0.60), hair=(0.36, 0.25, 0.17), hairstyle="crew", outfit="sweater", top=(0.38, 0.42, 0.52), seed=24, beard=True)
ZOE = dict(skin=(0.45, 0.30, 0.22), hair=(0.08, 0.06, 0.05), hairstyle="curly", outfit="cardigan", top=(0.95, 0.55, 0.66), no_lanyard=True, seed=25)
JAKE = dict(skin=(0.96, 0.80, 0.68), hair=(0.85, 0.68, 0.38), hairstyle="crew", outfit="hoodie", top=(0.30, 0.55, 0.36), seed=26)
GUARD = dict(skin=(0.70, 0.50, 0.38), hair=(0.12, 0.10, 0.08), hairstyle="crew", outfit="uniform", top=(0.20, 0.22, 0.27), seed=27, wide=1.12, pants=(0.15, 0.15, 0.2))
INTERV = dict(skin=(0.96, 0.84, 0.76), hair=(0.80, 0.80, 0.82), hairstyle="bob", outfit="suit", top=(0.32, 0.22, 0.30), seed=28)


def hand_world(P, side):
    """World position of a hand. side 'L' = viewer-left arm (character's RIGHT hand), 'R' = character's LEFT hand."""
    s = P.get("s", 1.0); b = 1.0
    sx = -SH_X if side == "L" else SH_X
    spec = P.get("armL" if side == "L" else "armR", ("ang", -0.14, -0.05) if side == "L" else ("ang", 0.14, 0.05))
    _, (hx, hy) = arm_pts(sx, SH_Y * b, spec)
    return P["x"] + hx * s, P["y"] + hy * s


def fork(ctx, x, y, s=1.0, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rrect(ctx, -5, -10, 10, 70, 5); fs(ctx, (0.82, 0.84, 0.88), 3)
    rrect(ctx, -14, -40, 28, 34, 6); fs(ctx, (0.82, 0.84, 0.88), 3)
    for k in (-9, -3, 3, 9):
        ctx.move_to(k, -40); ctx.line_to(k, -70); st(ctx, OUTL, 7); ctx.move_to(k, -40); ctx.line_to(k, -70); st(ctx, (0.82, 0.84, 0.88), 3)
    ctx.restore()


def pencil(ctx, x, y, s=1.0, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rrect(ctx, -7, -80, 14, 90, 3); fs(ctx, (0.98, 0.80, 0.20), 3)
    poly(ctx, [(-7, 10), (7, 10), (0, 30)]); fs(ctx, (0.95, 0.85, 0.7), 3)
    ell(ctx, 0, 27, 3, 4); ctx.set_source_rgb(0.2, 0.2, 0.2); ctx.fill()
    ctx.restore()


def char_ecu(ctx, t, ch, tt, mood, bg, s=2.5, y=1820, x=540, look=0.0, lookY=0.0, dark=0.0, mouth=0.0, **kw):
    ctx.save(); z = 1.0 + 0.08 * sm(tt)
    ctx.translate(540, 960); ctx.scale(z, z); ctx.translate(-540, -960)
    bg(ctx, t)
    P = dict(x=x, y=y, s=s, mood=mood, look=look, lookY=lookY, dark=dark, mouth=mouth, blink=blinking(t, ch.get("seed", 0)) and mouth < 0.05)
    P.update(kw)
    draw_char(ctx, ch, P, t)
    ctx.restore()


# ------------------- sets -------------------
def dining(ctx, t, dim=0.0, night=True):
    wall = mix((0.88, 0.72, 0.56), (0.30, 0.25, 0.25), dim)
    ctx.set_source_rgb(*wall); ctx.paint()
    for x in range(0, 1080, 72):
        ctx.rectangle(x, 0, 36, 1150); ctx.set_source_rgba(1, 1, 1, 0.06); ctx.fill()
    ctx.rectangle(0, 1150, 1080, 300); ctx.set_source_rgb(*mix((0.55, 0.36, 0.24), (0.2, 0.14, 0.12), dim)); ctx.fill()
    ctx.rectangle(70, 400, 270, 380); fs(ctx, (0.08, 0.10, 0.22) if night else (0.75, 0.9, 1.0))
    ctx.move_to(205, 400); ctx.line_to(205, 780); ctx.move_to(70, 590); ctx.line_to(340, 590); st(ctx, (0.95, 0.95, 0.9), 9)
    rrect(ctx, 700, 460, 230, 190, 6); fs(ctx, (0.45, 0.32, 0.20))
    ctx.rectangle(718, 478, 194, 154); ctx.set_source_rgb(0.80, 0.90, 1.0); ctx.fill()
    for xx in (775, 855):   # framed photo of the twins
        ell(ctx, xx, 545, 18, 18); ctx.set_source_rgb(*HAIR); ctx.fill()
        ell(ctx, xx, 550, 13, 13); ctx.set_source_rgb(*SKIN); ctx.fill()
        rrect(ctx, xx - 20, 568, 40, 50, 10); ctx.set_source_rgb(0.98, 0.76, 0.22); ctx.fill()


def table_front(ctx, t, items=True, dim=0.0, lasagna=True):
    ctx.rectangle(-10, 1335, 1100, 70); fs(ctx, mix((0.96, 0.93, 0.86), (0.4, 0.38, 0.38), dim * 0.5))
    ctx.rectangle(-10, 1400, 1100, 530); fs(ctx, mix((0.75, 0.30, 0.28), (0.3, 0.15, 0.15), dim * 0.5))
    for x in range(40, 1080, 110):
        ctx.move_to(x, 1405); ctx.line_to(x, 1920); ctx.set_source_rgba(1, 1, 1, 0.12); ctx.set_line_width(14); ctx.stroke()
    if items:
        for x in (190, 890):
            ell(ctx, x, 1366, 92, 22); fs(ctx, (0.98, 0.98, 0.98), 4)
            ell(ctx, x - 15, 1362, 40, 11); ctx.set_source_rgb(0.85, 0.45, 0.25); ctx.fill()
        if lasagna:
            rrect(ctx, 440, 1335, 200, 50, 10); fs(ctx, (0.85, 0.85, 0.88), 4)
            rrect(ctx, 452, 1340, 176, 26, 6); ctx.set_source_rgb(0.85, 0.42, 0.20); ctx.fill()
            for k in range(3):
                p = ((t * 0.5 + k * 0.33) % 1)
                ell(ctx, 500 + k * 40, 1320 - p * 120, 10 + p * 14, 12 + p * 16); ctx.set_source_rgba(1, 1, 1, 0.4 * (1 - p)); ctx.fill()


def hallway_school(ctx, t, sign="WESTBROOK HIGH"):
    ctx.set_source_rgb(0.90, 0.92, 0.95); ctx.paint()
    ctx.rectangle(0, 1450, 1080, 500); ctx.set_source_rgb(0.72, 0.70, 0.66); ctx.fill()
    for x in range(-20, 1100, 130):
        ctx.rectangle(x, 520, 122, 930); fs(ctx, (0.30, 0.45, 0.75), 4)
        for y in (560, 600, 640):
            ctx.move_to(x + 30, y); ctx.line_to(x + 92, y); st(ctx, (0.2, 0.32, 0.55), 4)
        rrect(ctx, x + 96, 900, 12, 50, 4); fs(ctx, (0.75, 0.75, 0.8), 2)
    ctx.rectangle(0, 470, 1080, 50); fs(ctx, (0.85, 0.85, 0.88), 3)
    rrect(ctx, 380, 300, 320, 140, 10); fs(ctx, (0.98, 0.95, 0.85))
    text(ctx, sign, 540, 385, 38, col=(0.75, 0.2, 0.2))


def lana_room(ctx, t, night=True):
    ctx.set_source_rgb(*((0.18, 0.13, 0.24) if night else (0.42, 0.32, 0.50))); ctx.paint()
    ctx.rectangle(0, 1500, 1080, 500); ctx.set_source_rgb(0.12, 0.10, 0.14); ctx.fill()
    for (x, y, w, h_, c) in [(90, 380, 220, 300, (0.85, 0.2, 0.3)), (360, 420, 180, 240, (0.15, 0.15, 0.2)), (820, 360, 200, 280, (0.95, 0.75, 0.2))]:
        ctx.save(); ctx.translate(x + w / 2, y + h_ / 2); ctx.rotate(0.05 * sin(x))
        rrect(ctx, -w / 2, -h_ / 2, w, h_, 4); fs(ctx, mix(c, (0.1, 0.1, 0.1), 0.4 if night else 0)); ctx.restore()
    star(ctx, 920, 500, 60, n=5); ctx.set_source_rgba(0.1, 0.1, 0.1, 0.6); ctx.fill()
    glow(ctx, 900, 900, 260, (0.6, 0.4, 1.0), 0.25)


def notebook_cu(ctx, t, tt, page="days", lines=(), torn=False, photos=True):
    ctx.set_source_rgb(0.10, 0.08, 0.12); ctx.paint()
    z = 1.0 + 0.1 * sm(tt)
    ctx.save(); ctx.translate(540, 900); ctx.scale(z, z); ctx.translate(-540, -900); ctx.rotate(-0.03)
    rrect(ctx, 90, 280, 900, 1060, 14); fs(ctx, (0.97, 0.95, 0.88), 5)
    for y in range(380, 1320, 56):
        ctx.move_to(130, y); ctx.line_to(950, y); st(ctx, (0.7, 0.8, 0.92), 2)
    ctx.move_to(200, 290); ctx.line_to(200, 1330); st(ctx, (0.9, 0.5, 0.5), 3)
    if photos:
        for i, (px, py, r) in enumerate([(740, 470, 0.12), (800, 760, -0.1)]):
            ctx.save(); ctx.translate(px, py); ctx.rotate(r)
            ctx.rectangle(-110, -120, 220, 240); fs(ctx, (1, 1, 1), 4)
            ctx.rectangle(-95, -105, 190, 170); ctx.set_source_rgb(0.75, 0.85, 0.95); ctx.fill()
            ctx.save(); ctx.rectangle(-95, -105, 190, 170); ctx.clip()
            draw_char(ctx, LILY, dict(x=0, y=260, s=0.62, mood="happy" if i == 0 else "neutral", saccade=False), 0.5)
            ctx.restore()
            ctx.rectangle(-30, -135, 60, 26); ctx.set_source_rgba(0.95, 0.9, 0.6, 0.85); ctx.fill()
            ctx.restore()
    y = 420
    for i, (s_, col, t0) in enumerate(lines):
        if t >= t0:
            a = ramp(t, t0, t0 + 0.3)
            ctx.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL); ctx.set_font_size(58)
            wdt = ctx.text_extents(s_).x_advance; fsz = 58 * min(1.0, 720 / max(1, wdt))
            ctx.push_group(); text(ctx, s_, 230, y, fsz, col=col, align="l", weight=(col[0] > 0.5)); ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
        y += 124
    if torn:
        ctx.move_to(990, 280)
        for k in range(16):
            ctx.line_to(990 - (30 if k % 2 else 0), 280 + k * 68)
        ctx.line_to(1100, 1340); ctx.line_to(1100, 280); ctx.close_path(); ctx.set_source_rgb(0.10, 0.08, 0.12); ctx.fill()
    ctx.restore()


def text_bubble_phone(ctx, t, msgs, title="Lily", x=540, y=900, s=1.9, rot=-0.04):
    """A modern phone showing chat bubbles: msgs=[(text, mine, t0)]."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rrect(ctx, -170, -330, 340, 660, 40); fs(ctx, (0.12, 0.12, 0.14), 5)
    rrect(ctx, -155, -310, 310, 620, 28); ctx.set_source_rgb(0.97, 0.97, 0.98); ctx.fill()
    ctx.rectangle(-155, -310, 310, 70); ctx.set_source_rgb(0.92, 0.92, 0.95); ctx.fill()
    text(ctx, title, 0, -265, 22, col=(0.15, 0.15, 0.2))
    yy = -200
    for (m, mine, t0) in msgs:
        if t < t0: continue
        a = back_out((t - t0) / 0.3)
        ctx.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL); ctx.set_font_size(17)
        words = m.split(); lines_, cur = [], ""
        for w in words:
            if ctx.text_extents(cur + " " + w).x_advance > 200 and cur: lines_.append(cur); cur = w
            else: cur = (cur + " " + w).strip()
        lines_.append(cur)
        hgt = 18 + 24 * len(lines_)
        bx = 140 - 230 if mine else -140
        ctx.save(); ctx.translate(bx + 115, yy + hgt / 2); ctx.scale(a, a); ctx.translate(-(bx + 115), -(yy + hgt / 2))
        rrect(ctx, bx, yy, 230, hgt, 16); ctx.set_source_rgb(*((0.25, 0.55, 1.0) if mine else (0.88, 0.88, 0.9))); ctx.fill()
        for i, ln in enumerate(lines_):
            text(ctx, ln, bx + 14, yy + 28 + i * 24, 17, col=(1, 1, 1) if mine else (0.1, 0.1, 0.12), align="l", weight=False)
        ctx.restore()
        yy += hgt + 16
    ctx.restore()


def night_street(ctx, t, offset=0.0):
    ctx.set_source_rgb(0.05, 0.06, 0.12); ctx.paint()
    off = (t * 120 + offset) % 600
    for i in range(-1, 4):
        x = i * 600 - off
        poly(ctx, [(x + 40, 900), (x + 280, 720), (x + 520, 900)]); ctx.set_source_rgb(0.08, 0.08, 0.15); ctx.fill()
        ctx.rectangle(x + 80, 900, 400, 420); ctx.set_source_rgb(0.10, 0.10, 0.18); ctx.fill()
        ctx.rectangle(x + 140, 980, 90, 80); ctx.set_source_rgb(1, 0.8, 0.45); ctx.fill()
        glow(ctx, x + 185, 1020, 160, (1, 0.8, 0.45), 0.25)
    ctx.rectangle(0, 1320, 1080, 700); ctx.set_source_rgb(0.12, 0.12, 0.15); ctx.fill()
    for i in range(-1, 4):
        x = i * 500 - (t * 120 + offset) % 500 + 250
        ctx.rectangle(x - 6, 700, 12, 640); fs(ctx, (0.25, 0.25, 0.3), 3)
        glow(ctx, x, 700, 300, (1, 0.85, 0.55), 0.35); ell(ctx, x, 700, 26, 14); fs(ctx, (1, 0.9, 0.6), 3)


def bus_broken(ctx, x, y, s, t):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, 0, -330, 900, 300, 30); fs(ctx, (0.95, 0.75, 0.15))
    for k in range(5):
        rrect(ctx, 40 + k * 165, -300, 140, 110, 10); fs(ctx, (0.25, 0.32, 0.45), 4)
    rrect(ctx, 0, -150, 900, 26, 6); fs(ctx, (0.15, 0.15, 0.15), 3)
    for wx in (160, 740):
        ell(ctx, wx, -30, 60, 60); fs(ctx, (0.05, 0.05, 0.06)); ell(ctx, wx, -30, 25, 25); fs(ctx, (0.6, 0.6, 0.65), 3)
    on = (t % 0.8) < 0.4
    for hx_ in (10, 890):
        ell(ctx, hx_, -80, 14, 16); fs(ctx, (1, 0.6, 0.1) if on else (0.5, 0.3, 0.1), 3)
        if on: glow(ctx, hx_, -80, 120, (1, 0.55, 0.1), 0.6)
    for k in range(5):
        p = ((t * 0.4 + k * 0.2) % 1.0)
        ell(ctx, 880 + 30 * sin(k * 2 + t), -330 - p * 260, 40 + p * 50, 34 + p * 40); ctx.set_source_rgba(0.8, 0.8, 0.85, 0.35 * (1 - p)); ctx.fill()
    ctx.restore()


def academy_ext(ctx, t):
    gr = cairo.LinearGradient(0, 0, 0, 1300); gr.add_color_stop_rgb(0, 0.55, 0.75, 0.95); gr.add_color_stop_rgb(1, 0.88, 0.94, 1.0)
    ctx.set_source(gr); ctx.paint()
    poly(ctx, [(40, 560), (540, 330), (1040, 560)]); fs(ctx, (0.90, 0.88, 0.82))
    ctx.rectangle(80, 560, 920, 900); fs(ctx, (0.95, 0.93, 0.88))
    for x in (130, 300, 700, 870):
        rrect(ctx, x, 600, 70, 860, 10); fs(ctx, (0.98, 0.97, 0.94), 4)
    text(ctx, "WESTBROOK ART ACADEMY", 540, 520, 40, col=(0.35, 0.3, 0.25))
    rrect(ctx, 430, 1050, 220, 410, 100); fs(ctx, (0.35, 0.22, 0.15))
    rrect(ctx, 440, 700, 200, 260, 12); fs(ctx, (1.0, 0.9, 0.65))
    ctx.rectangle(0, 1460, 1080, 500); ctx.set_source_rgb(0.75, 0.72, 0.68); ctx.fill()
    for k in range(6):
        ctx.rectangle(0, 1460 + k * 30, 1080, 6); ctx.set_source_rgba(0, 0, 0, 0.06); ctx.fill()


def interview_room(ctx, t):
    ctx.set_source_rgb(0.92, 0.88, 0.80); ctx.paint()
    ctx.rectangle(0, 1400, 1080, 600); ctx.set_source_rgb(0.55, 0.40, 0.28); ctx.fill()
    for (x, y, w, h_, c) in [(80, 380, 260, 200, (0.4, 0.6, 0.85)), (380, 340, 300, 240, (0.95, 0.6, 0.4)), (740, 400, 240, 190, (0.5, 0.75, 0.5))]:
        rrect(ctx, x, y, w, h_, 6); fs(ctx, (0.75, 0.6, 0.35)); ctx.rectangle(x + 14, y + 14, w - 28, h_ - 28); ctx.set_source_rgb(*c); ctx.fill()


def guitar(ctx, x, y, s=1.0, rot=-0.6):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rrect(ctx, -14, -330, 28, 260, 6); fs(ctx, (0.35, 0.22, 0.12))
    rrect(ctx, -22, -380, 44, 60, 10); fs(ctx, (0.25, 0.15, 0.08))
    blob(ctx, [(0, -40, 95), (0, 80, 125)], (0.80, 0.45, 0.18))
    ell(ctx, 0, 30, 32, 32); ctx.set_source_rgb(0.15, 0.08, 0.04); ctx.fill()
    for k in (-8, 0, 8):
        ctx.move_to(k, -370); ctx.line_to(k, 150); st(ctx, (0.9, 0.9, 0.85), 1.5)
    ctx.restore()


def drawing_cu(ctx, t, tt, prog=1.0):
    """Close-up: Lily drawing with her LEFT hand in a sketchbook."""
    ctx.set_source_rgb(0.85, 0.72, 0.55); ctx.paint()
    z = 1.0 + 0.08 * sm(tt)
    ctx.save(); ctx.translate(540, 900); ctx.scale(z, z); ctx.translate(-540, -900)
    rrect(ctx, 120, 420, 840, 900, 14); fs(ctx, (0.99, 0.98, 0.95), 5)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    pts = [(300 + 400 * u, 860 - 260 * sin(u * pi) + 40 * sin(u * 12)) for u in [k / 60 for k in range(61)]]
    n = int(len(pts) * clamp(prog))
    if n > 1:
        ctx.move_to(*pts[0])
        for p in pts[1:n]: ctx.line_to(*p)
        st(ctx, (0.2, 0.2, 0.25), 6)
    ell(ctx, 540, 1000, 150, 60); st(ctx, (0.35, 0.35, 0.4), 4)
    px, py = pts[max(0, n - 1)]
    ctx.move_to(-220, 1500); ctx.line_to(px - 160, py + 190); st(ctx, OUTL, 160); ctx.move_to(-220, 1500); ctx.line_to(px - 160, py + 190); st(ctx, LILY["top"], 148)
    ell(ctx, px - 95, py + 120, 72, 58, -0.6); fs(ctx, SKIN, 6)
    pencil(ctx, px - 16 * 1.8, py + 21.6 * 1.8, 1.8, rot=3.79)
    ctx.restore()


def fork_cu(ctx, t, tt, circle=0.0):
    """Close-up: 'Lily' at the table eating with her RIGHT hand (viewer left)."""
    ctx.set_source_rgb(0.75, 0.30, 0.28); ctx.paint()
    z = 1.0 + 0.1 * sm(tt)
    ctx.save(); ctx.translate(540, 900); ctx.scale(z, z); ctx.translate(-540, -900)
    ell(ctx, 560, 1050, 330, 120); fs(ctx, (0.98, 0.98, 0.98), 5)
    rrect(ctx, 420, 1000, 280, 80, 14); ctx.set_source_rgb(0.85, 0.42, 0.2); ctx.fill()
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(-200, 300); ctx.line_to(330, 760); st(ctx, OUTL, 170); ctx.move_to(-200, 300); ctx.line_to(330, 760); st(ctx, LILY["top"], 158)
    ell(ctx, 380, 820, 80, 66, 0.7); fs(ctx, SKIN, 6)
    fork(ctx, 420, 880, 2.0, rot=2.5)
    if circle > 0:
        ctx.new_path(); ctx.arc(390, 830, 200, -pi / 2, -pi / 2 + 2 * pi * circle); st(ctx, (0.95, 0.15, 0.15), 14)
    ctx.restore()
