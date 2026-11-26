"""Shared props, sets and characters for Parts 2 and 3."""
import cairo, random
from math import sin, cos, pi
from rig import *
import part1 as P1
from part1 import MAYA, DALE, MOM, ALV

ADD = cairo.OPERATOR_ADD
DET = dict(skin=(0.55, 0.38, 0.28), hair=(0.08, 0.06, 0.05), hairstyle="bun", outfit="suit", top=(0.24, 0.26, 0.32), seed=6, eye=(0.08, 0.05, 0.04))
PATT = dict(skin=(0.97, 0.84, 0.76), hair=(0.82, 0.82, 0.84), hairstyle="bun", outfit="cardigan", top=(0.72, 0.60, 0.85), seed=7, no_lanyard=True, blush=True)
TROOPER = dict(skin=(0.88, 0.68, 0.52), hair=(0.25, 0.18, 0.12), hairstyle="crew", outfit="uniform", top=(0.38, 0.40, 0.44), seed=8, pants=(0.3, 0.32, 0.36))
DALE_S = dict(DALE, outfit="suit", top=(0.30, 0.30, 0.34))
DALE_O = dict(DALE, outfit="orange", top=(0.95, 0.50, 0.15), sleeve=(0.95, 0.50, 0.15))
MOM_DAY = dict(MOM, top=(0.55, 0.70, 0.85))
DETERMINED = dict(bi=7, bo=-3, eo=0.85, ew=0, smile=-0.15)
BRAVE_MOM = dict(bi=-3, bo=-6, eo=0.95, smile=-0.1, tear=0.3)


def old_phone(ctx, x, y, s, t, rec_t0=None, low=False, popup=0.0, rot=0.0, rec_off=0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rrect(ctx, -62, -118, 124, 236, 20); fs(ctx, (0.14, 0.14, 0.17), 4)
    rrect(ctx, -52, -100, 104, 192, 8); ctx.set_source_rgb(0.05, 0.07, 0.13); ctx.fill()
    glow(ctx, 0, -5, 120, (0.4, 0.6, 1.0), 0.18)
    ctx.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    rrect(ctx, 26, -94, 20, 10, 2); st(ctx, (0.8, 0.8, 0.85), 1.5)
    ctx.rectangle(28, -92, 6 if low else 15, 6); ctx.set_source_rgb(*((0.95, 0.2, 0.2) if low else (0.3, 0.9, 0.4))); ctx.fill()
    if rec_t0 is not None and t >= rec_t0:
        sec = int(t - rec_t0) + rec_off
        if (t * 1.6) % 1 < 0.6:
            ell(ctx, -26, -52, 9, 9); ctx.set_source_rgb(0.95, 0.15, 0.15); ctx.fill()
        text(ctx, "REC", 10, -44, 22, col=(0.95, 0.15, 0.15))
        text(ctx, f"{sec // 60:02d}:{sec % 60:02d}", 0, -8, 30, col=(1, 1, 1))
        for i in range(13):
            h_ = 6 + 28 * abs(sin(t * 9 + i * 1.7)) * (0.5 + 0.5 * sin(i * 0.9 + t * 3))
            ctx.rectangle(-46 + i * 7.3, 40 - h_ / 2, 4, h_); ctx.set_source_rgb(0.95, 0.3, 0.3); ctx.fill()
    else:
        text(ctx, "Voice Recorder", 0, -60, 13, col=(0.85, 0.85, 0.9))
        for i in range(13):
            ctx.rectangle(-46 + i * 7.3, 0, 4, 2); ctx.set_source_rgb(0.5, 0.5, 0.6); ctx.fill()
        ell(ctx, 0, 52, 22, 22); ctx.set_source_rgb(0.95, 0.15, 0.15); ctx.fill_preserve(); ctx.set_source_rgb(1, 1, 1); ctx.set_line_width(4); ctx.stroke()
    for (a0, l0) in [(0.3, 70), (1.4, 55), (2.6, 80), (3.7, 50), (4.9, 65)]:   # crack
        ctx.move_to(18, -40); ctx.line_to(18 + l0 * cos(a0), -40 + l0 * sin(a0)); ctx.line_to(18 + l0 * 1.3 * cos(a0 + 0.2), -40 + l0 * 1.3 * sin(a0 + 0.2))
    ctx.set_source_rgba(0.9, 0.95, 1, 0.55); ctx.set_line_width(1.6); ctx.stroke()
    if popup > 0:
        ctx.save(); ctx.translate(0, 10); ctx.scale(popup, popup)
        rrect(ctx, -48, -26, 96, 52, 10); fs(ctx, (0.97, 0.97, 0.97), 2)
        text(ctx, "Battery", 0, -4, 14, col=(0.2, 0.2, 0.25)); text(ctx, "1%", 0, 18, 20, col=(0.9, 0.15, 0.15))
        ctx.restore()
    ctx.restore()


def shelf_cu(ctx, t, hand_u=0.0, rec_t0=None, low=True, popup=0.0, shake=0.0):
    """Close-up of the kitchen shelf where the phone hides behind the cereal box."""
    ctx.set_source_rgb(0.20, 0.23, 0.35); ctx.paint()
    for x in range(-100, 1200, 140):
        ctx.rectangle(x, 0, 6, 1920); ctx.set_source_rgba(0, 0, 0, 0.12); ctx.fill()
    sx = shake * 8 * sin(t * 70)
    ctx.save(); ctx.translate(sx, -260)
    ctx.rectangle(-20, 1300, 1120, 60); fs(ctx, (0.45, 0.32, 0.22))
    for (x, w, hgt, c) in [(80, 150, 230, (0.65, 0.75, 0.55)), (250, 120, 180, (0.85, 0.85, 0.75))]:
        rrect(ctx, x, 1300 - hgt, w, hgt, 20); fs(ctx, c)
        rrect(ctx, x + 10, 1300 - hgt - 30, w - 20, 34, 8); fs(ctx, (0.55, 0.4, 0.3))
    old_phone(ctx, 560, 1180, 0.95, t, rec_t0=rec_t0, low=low, popup=popup, rot=-0.06, rec_off=150)
    rrect(ctx, 610, 860, 330, 440, 10); fs(ctx, (0.92, 0.35, 0.18))
    rrect(ctx, 640, 900, 270, 140, 10); fs(ctx, (1, 0.85, 0.25), 4)
    text(ctx, "CRUNCH", 775, 990, 56, col=(0.85, 0.2, 0.15))
    for k in range(5):
        ell(ctx, 700 + k * 45, 1150 + 20 * sin(k * 2), 22, 18); fs(ctx, (0.95, 0.75, 0.35), 3)
    glow(ctx, 560, 1180, 260, (0.4, 0.6, 1.0), 0.15)
    if hand_u > 0:
        hx, hy = lerp(-350, 360, hand_u), lerp(800, 1060, hand_u)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.move_to(hx - 600, hy - 380); ctx.line_to(hx - 60, hy - 30); st(ctx, OUTL, 236); ctx.move_to(hx - 600, hy - 380); ctx.line_to(hx - 60, hy - 30); st(ctx, DALE["top"], 224)
        ell(ctx, hx, hy, 120, 95, 0.55); fs(ctx, DALE["skin"], 6)
        for k in range(4):
            a = 0.25 + k * 0.32
            x0, y0 = hx + 80 * cos(a - 0.6), hy + 60 * sin(a - 0.6)
            ctx.move_to(x0, y0); ctx.line_to(x0 + 110 * cos(a - 0.2), y0 + 110 * sin(a - 0.2)); st(ctx, OUTL, 58)
            ctx.move_to(x0, y0); ctx.line_to(x0 + 110 * cos(a - 0.2), y0 + 110 * sin(a - 0.2)); st(ctx, DALE["skin"], 46)
    ctx.restore()


def kitchen_set(ctx, t):
    """Night kitchen (from Part 1) with a floor and the shelf on the right wall."""
    import part1v2 as V
    V.kitchen_night(ctx, t)
    ctx.rectangle(0, 1560, 1080, 400); ctx.set_source_rgb(0.30, 0.26, 0.24); ctx.fill()
    for x in range(0, 1080, 120):
        ctx.move_to(x, 1560); ctx.line_to(x - 60, 1920); st(ctx, (0.24, 0.2, 0.19), 3)
    ctx.rectangle(780, 900, 300, 22); fs(ctx, (0.45, 0.32, 0.22))
    rrect(ctx, 960, 770, 80, 130, 6); fs(ctx, (0.92, 0.35, 0.18), 3)
    rrect(ctx, 820, 820, 60, 80, 14); fs(ctx, (0.65, 0.75, 0.55), 3)


def card_insert(ctx, t, tt):
    ctx.set_source_rgb(0.30, 0.20, 0.13); ctx.paint()
    for y in range(0, 1920, 90):
        ctx.move_to(0, y); ctx.curve_to(400, y + 20, 700, y - 20, 1080, y + 10); st(ctx, (0.26, 0.17, 0.11), 6)
    u = sm(tt * 1.3)
    ax = lerp(250, 560, u)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(-300, 1250); ctx.line_to(ax - 90, 1000); st(ctx, OUTL, 190); ctx.move_to(-300, 1250); ctx.line_to(ax - 90, 1000); st(ctx, ALV["top"], 178)
    ell(ctx, ax, 960, 95, 80, -0.3); fs(ctx, ALV["skin"], 6)
    ctx.save(); ctx.translate(ax + 70, 900); ctx.rotate(-0.12)
    rrect(ctx, -10, -60, 300, 170, 10); fs(ctx, (0.99, 0.98, 0.95), 5)
    text(ctx, "MS. R. ALVAREZ", 140, -10, 30, col=(0.15, 0.2, 0.35))
    text(ctx, "School Counselor", 140, 25, 22, col=(0.4, 0.4, 0.45), weight=False)
    text(ctx, "(555) 014-2209", 140, 70, 30, col=(0.85, 0.15, 0.15))
    ctx.restore()
    for k in range(4):
        ctx.move_to(ax + 40, 900 + k * 28); ctx.line_to(ax + 110, 890 + k * 30); st(ctx, OUTL, 40); ctx.move_to(ax + 40, 900 + k * 28); ctx.line_to(ax + 110, 890 + k * 30); st(ctx, ALV["skin"], 30)
    mx = lerp(1250, 900, sm((tt - 0.4) * 2))
    ctx.move_to(1400, 1350); ctx.line_to(mx + 80, 1080); st(ctx, OUTL, 170); ctx.move_to(1400, 1350); ctx.line_to(mx + 80, 1080); st(ctx, MAYA["top"], 158)
    ell(ctx, mx, 1050, 80, 70, 0.4); fs(ctx, MAYA["skin"], 6)


def car_interior(ctx, t):
    ctx.set_source_rgb(0.05, 0.06, 0.11); ctx.paint()
    poly(ctx, [(60, 260), (1020, 260), (1080, 900), (0, 900)]); ctx.set_source_rgb(0.08, 0.10, 0.18); ctx.fill()
    for k in range(3):   # streetlights sweeping past
        p = ((t * 0.45 + k / 3) % 1)
        glow(ctx, lerp(1300, -300, p), 420, 260, (1, 0.75, 0.4), 0.35)
    rrect(ctx, 400, 300, 280, 80, 14); fs(ctx, (0.15, 0.17, 0.22), 6)
    ctx.rectangle(420, 314, 240, 52); ctx.set_source_rgb(0.25, 0.3, 0.42); ctx.fill()
    ell(ctx, 470, 340, 36, 12); ctx.set_source_rgb(*DALE["skin"]); ctx.fill()
    for xx in (452, 488):
        ell(ctx, xx, 340, 5, 4); ctx.set_source_rgb(0.05, 0.05, 0.05); ctx.fill()


def car_front(ctx):
    ctx.rectangle(-20, 1400, 1120, 600); fs(ctx, (0.10, 0.10, 0.13))
    ell(ctx, 300, 1420, 170, 170); st(ctx, (0.04, 0.04, 0.06), 30)
    rrect(ctx, 640, 1430, 300, 60, 10); ctx.set_source_rgb(0.2, 0.5, 0.9); ctx.fill()
    glow(ctx, 790, 1460, 200, (0.2, 0.5, 0.9), 0.25)


def porch(ctx, t, inside=(1, 0.88, 0.62), open_u=1.0):
    ctx.set_source_rgb(0.10, 0.11, 0.20); ctx.paint()
    for y in range(0, 1920, 46):
        ctx.move_to(0, y); ctx.line_to(1080, y); st(ctx, (0.07, 0.08, 0.15), 3)
    ctx.rectangle(0, 1640, 1080, 400); ctx.set_source_rgb(0.20, 0.16, 0.14); ctx.fill()
    ctx.rectangle(300, 520, 480, 1130); fs(ctx, (0.85, 0.85, 0.82), 8)
    ctx.rectangle(330, 550, 420, 1090); ctx.set_source_rgb(*inside); ctx.fill()
    glow(ctx, 540, 1100, 650, (1, 0.85, 0.55), 0.4)
    glow(ctx, 860, 520, 160, (1, 0.85, 0.5), 0.6); ell(ctx, 860, 520, 16, 22); fs(ctx, (1, 0.92, 0.65), 3)


def porch_front(ctx, open_u):
    w = 420 * cos(open_u * 1.35)
    poly(ctx, [(330, 550), (330 + w, 550 + 40 * open_u), (330 + w, 1640 - 40 * open_u), (330, 1640)]); fs(ctx, (0.55, 0.18, 0.18), 6)


def house_day(ctx, t):
    gr = cairo.LinearGradient(0, 0, 0, 1300); gr.add_color_stop_rgb(0, 0.50, 0.75, 0.96); gr.add_color_stop_rgb(1, 0.85, 0.93, 1.0)
    ctx.set_source(gr); ctx.paint()
    glow(ctx, 880, 300, 200, (1, 0.95, 0.6), 0.6); ell(ctx, 880, 300, 70, 70); ctx.set_source_rgb(1, 0.93, 0.55); ctx.fill()
    for x, r in [(-40, 160), (110, 130), (980, 170), (1100, 150)]:
        ell(ctx, x, 1180, r, r * 1.3); ctx.set_source_rgb(0.35, 0.60, 0.33); ctx.fill()
    poly(ctx, [(60, 790), (540, 500), (1020, 790)]); fs(ctx, (0.55, 0.30, 0.25))
    ctx.rectangle(120, 780, 840, 560); fs(ctx, (0.95, 0.88, 0.72))
    for y in range(820, 1340, 44):
        ctx.move_to(120, y); ctx.line_to(960, y); ctx.set_source_rgba(0, 0, 0, 0.08); ctx.set_line_width(3); ctx.stroke()
    for wx in (200, 720):
        ctx.rectangle(wx, 880, 160, 140); fs(ctx, (0.70, 0.85, 0.95))
        ctx.move_to(wx + 80, 880); ctx.line_to(wx + 80, 1020); ctx.move_to(wx, 950); ctx.line_to(wx + 160, 950); st(ctx, (1, 1, 1), 6)
    rrect(ctx, 478, 1110, 124, 230, 8); fs(ctx, (0.55, 0.18, 0.18))
    ctx.rectangle(0, 1330, 1080, 600); ctx.set_source_rgb(0.45, 0.70, 0.38); ctx.fill()
    ctx.rectangle(0, 1640, 1080, 300); ctx.set_source_rgb(0.40, 0.40, 0.44); ctx.fill()
    poly(ctx, [(470, 1340), (610, 1340), (640, 1640), (440, 1640)]); ctx.set_source_rgb(0.78, 0.76, 0.72); ctx.fill()


def apartment(ctx, t):
    ctx.set_source_rgb(0.99, 0.95, 0.84); ctx.paint()
    ctx.rectangle(0, 1460, 1080, 500); ctx.set_source_rgb(0.80, 0.66, 0.50); ctx.fill()
    ctx.rectangle(330, 330, 420, 520); fs(ctx, (0.78, 0.92, 1.0))
    glow(ctx, 540, 560, 420, (1, 0.97, 0.8), 0.7)
    ctx.move_to(540, 330); ctx.line_to(540, 850); ctx.move_to(330, 590); ctx.line_to(750, 590); st(ctx, (1, 1, 1), 12)
    ctx.save(); ctx.set_operator(ADD)
    poly(ctx, [(330, 330), (750, 330), (1080, 1600), (100, 1700)]); ctx.set_source_rgba(1, 0.95, 0.75, 0.10); ctx.fill(); ctx.restore()
    rrect(ctx, 880, 1180, 120, 140, 12); fs(ctx, (0.85, 0.5, 0.35))
    for k in range(6):
        a = -pi / 2 + (k - 2.5) * 0.4
        ell(ctx, 940 + 80 * cos(a), 1160 + 100 * sin(a), 22, 55, a + pi / 2); fs(ctx, (0.35, 0.65, 0.38), 4)


def boxes(ctx):
    for (x, y, w, h_, lab) in [(40, 1420, 260, 200, "KITCHEN"), (80, 1260, 200, 160, "BOOKS"), (790, 1440, 260, 200, "MAYA")]:
        ctx.rectangle(x, y, w, h_); fs(ctx, (0.82, 0.65, 0.42))
        ctx.move_to(x, y + 30); ctx.line_to(x + w, y + 30); st(ctx, (0.65, 0.5, 0.3), 4)
        text(ctx, lab, x + w / 2, y + h_ / 2 + 25, 34, col=(0.25, 0.2, 0.15))


def courtroom(ctx, t, dim=0.0):
    ctx.set_source_rgb(*mix((0.55, 0.38, 0.24), (0.2, 0.15, 0.12), dim)); ctx.paint()
    for x in range(0, 1080, 135):
        ctx.rectangle(x + 8, 250, 119, 900); ctx.set_source_rgba(0, 0, 0, 0.08); ctx.fill()
    ctx.rectangle(0, 1150, 1080, 800); ctx.set_source_rgb(*mix((0.40, 0.26, 0.16), (0.15, 0.1, 0.08), dim)); ctx.fill()
    ell(ctx, 540, 380, 90, 90); fs(ctx, (0.85, 0.7, 0.35)); star(ctx, 540, 380, 50); ctx.set_source_rgb(0.6, 0.45, 0.2); ctx.fill()


def newspaper(ctx, t, tt):
    ctx.set_source_rgb(0.10, 0.08, 0.10); ctx.paint()
    u = back_out(tt * 2.2)
    ctx.save(); ctx.translate(540, 900); ctx.rotate((1 - min(1, tt * 2.2)) * 6.28 * 1.5 - 0.05); ctx.scale(u, u)
    ctx.rectangle(-420, -600, 840, 1150); fs(ctx, (0.95, 0.93, 0.86), 6)
    text(ctx, "THE DAILY HERALD", 0, -520, 54, col=(0.1, 0.1, 0.1))
    ctx.move_to(-390, -490); ctx.line_to(390, -490); st(ctx, (0.1, 0.1, 0.1), 4)
    text(ctx, "DECORATED OFFICER", 0, -400, 66, col=(0.1, 0.1, 0.1))
    text(ctx, "CHARGED", 0, -320, 86, col=(0.75, 0.08, 0.08))
    text(ctx, "Two more families come forward", 0, -250, 34, col=(0.25, 0.25, 0.25), weight=False)
    ctx.rectangle(-380, -210, 400, 420); ctx.set_source_rgb(0.75, 0.75, 0.72); ctx.fill()
    ctx.save(); ctx.rectangle(-380, -210, 400, 420); ctx.clip()
    draw_char(ctx, DALE, dict(x=-180, y=260, s=1.05, hat=True, mood="cold", saccade=False, dark=0.0), 0.3)
    overlay(ctx, (0.5, 0.5, 0.5), 0.35, cairo.OPERATOR_SATURATE)
    ctx.restore()
    for k in range(12):
        ctx.move_to(50, -190 + k * 34); ctx.line_to(380, -190 + k * 34); st(ctx, (0.6, 0.6, 0.6), 8)
    for k in range(8):
        ctx.move_to(-380, 260 + k * 34); ctx.line_to(380, 260 + k * 34); st(ctx, (0.6, 0.6, 0.6), 8)
    ctx.restore()


def end_card(ctx, t, t0, title, lines):
    if t < t0: return
    overlay(ctx, (0.02, 0.02, 0.05), 0.82 * ramp(t, t0, t0 + 0.3))
    p = back_out((t - t0 - 0.1) / 0.35)
    if t > t0 + 0.1:
        ctx.save(); ctx.translate(540, 820); ctx.scale(p, p)
        ctx.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(120)
        w = ctx.text_extents(title).x_advance + 90
        rrect(ctx, -w / 2, -120, w, 170, 30); ctx.set_source_rgb(0.9, 0.12, 0.15); ctx.fill()
        text(ctx, title, 0, 6, 120); ctx.restore()
    for i, (s_, size, col) in enumerate(lines):
        q = ramp(t, t0 + 0.45 + i * 0.3, t0 + 0.75 + i * 0.3)
        if q > 0:
            ctx.save(); ctx.translate(540, 1030 + i * 95); ctx.scale(0.9 + 0.1 * q, 0.9 + 0.1 * q)
            ctx.push_group(); text(ctx, s_, 0, 0, size, col=col, stroke=10); ctx.pop_group_to_source(); ctx.paint_with_alpha(q)
            ctx.restore()
