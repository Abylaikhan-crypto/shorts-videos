"""Style-2 test: fast cuts, moving camera, depth rooms, inserts, one-word captions.
python s2.py preview a:1.0 ... | python s2.py render [scenes]"""
import json, os, sys, subprocess, random
import cairo, numpy as np
from PIL import Image, ImageFilter
from math import sin, cos, pi
from rig import *
import part1 as P1
from part1 import ik
from twins_common import DAD, MOM2

HERE = os.path.dirname(os.path.abspath(__file__))
EP = f"{HERE}/mini/s2"
TL = {s["id"]: s for s in json.load(open(f"{EP}/timeline.json"))}
ADD = cairo.OPERATOR_ADD


def DUR(sc): return TL[sc]["dur"]


def WT(sc, word, li=None, nth=0):
    k = 0
    for i, l in enumerate(TL[sc]["lines"]):
        if li is not None and i != li: continue
        for w in l["words"]:
            if w[0].strip(".,!?'").lower() == word.lower():
                if k == nth: return w[1]
                k += 1
    raise KeyError(word)


def talk(sc, spk, t):
    for l in TL[sc]["lines"]:
        if l["spk"] == spk and l["start"] <= t < l["start"] + l["dur"]:
            i = min(int((t - l["start"]) * FPS), len(l["env"]) - 1); e = l["env"]
            return (e[i] + e[max(0, i - 1)]) / 2
    return 0.0


# ---------------- characters ----------------
BEN = dict(skin=(0.92, 0.74, 0.60), hair=(0.40, 0.25, 0.14), hairstyle="crew", outfit="hoodie", top=(0.92, 0.55, 0.20), seed=51, pants=(0.3, 0.3, 0.4))
MOM_P = dict(MOM2, outfit="longsleeve", top=(0.75, 0.65, 0.85))
DAD_P = dict(DAD, outfit="longsleeve", top=(0.45, 0.55, 0.70))
FUR, FURD, CREAM = (0.88, 0.66, 0.36), (0.70, 0.48, 0.24), (0.96, 0.87, 0.72)

# ---------------- utilities ----------------
_CACHE = {}
PAD_X, PAD_Y = 260, 460   # cached layers are bigger than the frame so the camera can move


def to_surface(img):
    a = np.asarray(img.convert("RGBA")).astype(np.uint16)
    a[..., :3] = (a[..., :3] * a[..., 3:4] // 255)
    bgra = a[..., [2, 1, 0, 3]].astype(np.uint8).copy()
    h, w = bgra.shape[:2]
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    np.frombuffer(s.get_data(), np.uint8).reshape(h, s.get_stride())[:, :w * 4] = bgra.reshape(h, w * 4); s.mark_dirty()
    return s


def to_image(s):
    s.flush(); w, h = s.get_width(), s.get_height()
    a = np.frombuffer(s.get_data(), np.uint8).reshape(h, s.get_stride())[:, :w * 4].reshape(h, w, 4)
    return Image.fromarray(a[..., [2, 1, 0, 3]].copy(), "RGBA")


def layer(key, fn, blur=0, opaque=True):
    """Render fn(ctx) once onto an oversized canvas (frame coords), optionally blurred, and cache it."""
    if key not in _CACHE:
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W + 2 * PAD_X, H + 2 * PAD_Y)
        c = cairo.Context(s); c.translate(PAD_X, PAD_Y)
        c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
        fn(c)
        if blur:
            im = to_image(s)
            if opaque:
                im = im.convert("RGB").filter(ImageFilter.GaussianBlur(blur)).convert("RGBA")
            else:   # blur premultiplied channels so edges stay clean
                a = np.asarray(im).astype(np.float32); al = a[..., 3:4] / 255
                pm = np.concatenate([a[..., :3] * al, a[..., 3:4]], -1)
                pm = np.stack([np.asarray(Image.fromarray(pm[..., i].astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))) for i in range(4)], -1).astype(np.float32)
                al2 = np.maximum(pm[..., 3:4], 1) / 255
                rgb = np.clip(pm[..., :3] / al2, 0, 255)
                im = Image.fromarray(np.concatenate([rgb, pm[..., 3:4]], -1).astype(np.uint8), "RGBA")
            s = to_surface(im)
        _CACHE[key] = s
    return _CACHE[key]


def paint_layer(ctx, surf, a=1.0):
    ctx.set_source_surface(surf, -PAD_X, -PAD_Y); ctx.paint_with_alpha(a)


def cam(ctx, z=1.0, cx=540, cy=960, rot=0.0, dx=0, dy=0):
    ctx.translate(540 + dx, 960 + dy); ctx.rotate(rot); ctx.scale(z, z); ctx.translate(-cx, -cy)


def depth(ctx, d, px, py, z=1.0):
    """parallax: a layer at depth d moves d times as much as the camera pan (px, py) and zoom."""
    zz = 1 + (z - 1) * d
    ctx.translate(540 - px * d, 960 - py * d); ctx.scale(zz, zz); ctx.translate(-540, -960)


def shake(t, amp, f=38):
    return amp * sin(t * f), amp * 0.7 * sin(t * f * 1.3 + 1.7)


def punch(lt, amt=0.07, d=0.18):
    return 1 + amt * (1 - sm(clamp(lt / d)))


rnd = np.random.default_rng(7)
GRAIN = [to_surface(Image.fromarray(np.dstack([g, g, g, np.full_like(g, 255)]), "RGBA").resize((W, H)))
         for g in [rnd.integers(80, 176, (H // 2, W // 2), dtype=np.uint8) for _ in range(4)]]


def grain(ctx, t, a=0.06):
    ctx.save(); ctx.set_source_surface(GRAIN[int(t * 24) % 4], 0, 0); ctx.paint_with_alpha(a); ctx.restore()


def light_pass(ctx, warm=(1, 0.75, 0.45), cool=(0.25, 0.35, 0.7), a=0.22):
    g = cairo.LinearGradient(0, 0, 1080, 1920); g.add_color_stop_rgba(0, *cool, a); g.add_color_stop_rgba(1, *warm, a * 0.6)
    ctx.save(); ctx.set_source(g); ctx.set_operator(cairo.OPERATOR_SOFT_LIGHT); ctx.paint(); ctx.restore()


def label(ctx, t, t0, s, x, y, size=64, rot=-0.08, col=(1, 1, 1), t1=99):
    if t < t0 or t > t1: return
    p = back_out(clamp((t - t0) / 0.22))
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(p, p)
    ctx.select_font_face("Poppins", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    e = ctx.text_extents(s)
    ctx.new_path(); ctx.move_to(-e.x_advance / 2, size * 0.35); ctx.text_path(s)
    ctx.set_source_rgb(0, 0, 0); ctx.set_line_width(size * 0.16); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
    ctx.set_source_rgb(*col); ctx.fill(); ctx.restore()


def pop_word(ctx, t, t0, s, x, y, size=110, col=(1, 0.86, 0.15), rot=-0.12, life=0.5):
    if not (t0 <= t < t0 + life): return
    p = back_out(clamp((t - t0) / 0.12)); o = 1 - ramp(t, t0 + life - 0.12, t0 + life)
    ctx.save(); ctx.push_group(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(p, p)
    text(ctx, s, 0, size * 0.35, size, col=col, stroke=size * 0.17)
    ctx.pop_group_to_source(); ctx.paint_with_alpha(o); ctx.restore()


def speed_lines(ctx, t, cx=540, cy=960, a=0.35, n=36, horiz=False):
    rs = random.Random(int(t * 15))
    ctx.save(); ctx.set_line_width(5)
    for i in range(n):
        if horiz:
            y = rs.uniform(0, 1920); x = rs.uniform(-200, 1080); L = rs.uniform(200, 600)
            ctx.move_to(x, y); ctx.line_to(x + L, y)
        else:
            ang = rs.uniform(0, 2 * pi); r0 = rs.uniform(520, 700)
            ctx.move_to(cx + r0 * cos(ang), cy + r0 * sin(ang)); ctx.line_to(cx + 1500 * cos(ang), cy + 1500 * sin(ang))
        ctx.set_source_rgba(1, 1, 1, a * rs.uniform(0.4, 1)); ctx.stroke()
    ctx.restore()


# ---------------- rooms with depth ----------------
def room(ctx, back=(330, 560, 420, 600), wall=(0.16, 0.18, 0.30), floor=(0.22, 0.15, 0.12), ceil=(0.10, 0.11, 0.20),
         side=None, plank=True, rug=None, base=(0.9, 0.9, 0.95)):
    bx, by, bw, bh = back
    L_, R_, T_, B_ = bx, bx + bw, by, by + bh
    sideL = side or shade(wall, 0.15); sideR = shade(wall, 0.28)
    poly(ctx, [(-400, -400), (1480, -400), (R_, T_), (L_, T_)]); ctx.set_source_rgb(*ceil); ctx.fill()
    poly(ctx, [(-400, -400), (L_, T_), (L_, B_), (-400, 2400)]); ctx.set_source_rgb(*sideL); ctx.fill()
    poly(ctx, [(1480, -400), (R_, T_), (R_, B_), (1480, 2400)]); ctx.set_source_rgb(*sideR); ctx.fill()
    ctx.rectangle(L_, T_, bw, bh); ctx.set_source_rgb(*wall); ctx.fill()
    poly(ctx, [(-400, 2400), (1480, 2400), (R_, B_), (L_, B_)]); ctx.set_source_rgb(*floor); ctx.fill()
    vx, vy = bx + bw / 2, by + bh * 0.45
    if plank:
        for k in range(-9, 10):
            xb = vx + k * 190
            x2 = L_ + (k + 9) / 18 * bw
            ctx.move_to(x2, B_); ctx.line_to(vx + (x2 - vx) * 6.5, B_ + (B_ - vy) * 5.5)
            ctx.set_source_rgba(0, 0, 0, 0.22); ctx.set_line_width(4); ctx.stroke()
        for j in range(1, 9):
            f = (j / 9) ** 1.8
            y = B_ + f * 1400
            ctx.move_to(-400, y); ctx.line_to(1480, y); ctx.set_source_rgba(0, 0, 0, 0.08); ctx.set_line_width(3); ctx.stroke()
    if rug:
        poly(ctx, [(vx - bw * 0.22, B_ + 6), (vx + bw * 0.22, B_ + 6), (vx + 520, 2400), (vx - 520, 2400)]); fs(ctx, rug, 0)
    # baseboards and corner lines for crisp depth
    ctx.move_to(-400, 2400 - 0); ctx.line_to(L_, B_); ctx.line_to(R_, B_); ctx.line_to(1480, 2400)
    ctx.set_source_rgba(*base, 0.35); ctx.set_line_width(10); ctx.stroke()
    for (a_, b_) in [((L_, T_), (-400, -400)), ((R_, T_), (1480, -400)), ((L_, T_), (L_, B_)), ((R_, T_), (R_, B_))]:
        ctx.move_to(*a_); ctx.line_to(*b_); ctx.set_source_rgba(0, 0, 0, 0.35); ctx.set_line_width(4); ctx.stroke()
    return L_, R_, T_, B_


def side_door(ctx, x0, x1, top0, top1, bot0, bot1, col=(0.30, 0.22, 0.18), lit=False):
    poly(ctx, [(x0, top0), (x1, top1), (x1, bot1), (x0, bot0)]); fs(ctx, col, 5)
    if lit:
        poly(ctx, [(x1 - (x1 - x0) * 0.12, top1 + 6), (x1, top1), (x1, bot1), (x1 - (x1 - x0) * 0.12, bot1 - 6)])
        ctx.set_source_rgb(1, 0.82, 0.5); ctx.fill()
    kx = x0 + (x1 - x0) * 0.8; ky = (top0 + bot0) / 2 * 0.5 + (top1 + bot1) / 2 * 0.5 + 20
    ell(ctx, kx, ky, 9, 11); fs(ctx, (0.9, 0.75, 0.3), 3)


def frame_pic(ctx, x, y, w, h, skew=0.0, col=(0.85, 0.8, 0.6)):
    poly(ctx, [(x, y), (x + w, y + skew), (x + w, y + h - skew), (x, y + h)]); fs(ctx, (0.35, 0.25, 0.15), 5)
    m = 10
    poly(ctx, [(x + m, y + m), (x + w - m, y + skew + m), (x + w - m, y + h - skew - m), (x + m, y + h - m)]); ctx.set_source_rgb(*col); ctx.fill()


def hallway_night(ctx):
    L_, R_, T_, B_ = room(ctx, back=(400, 600, 280, 560), wall=(0.15, 0.17, 0.30), floor=(0.20, 0.14, 0.12), ceil=(0.08, 0.09, 0.17), rug=(0.42, 0.10, 0.13))
    # window at far end with moonlight
    ctx.rectangle(470, 680, 140, 190); fs(ctx, (0.55, 0.65, 0.95), 6)
    ctx.move_to(540, 680); ctx.line_to(540, 870); ctx.move_to(470, 775); ctx.line_to(610, 775); st(ctx, (0.2, 0.2, 0.3), 6)
    glow(ctx, 540, 775, 380, (0.45, 0.55, 1.0), 0.35)
    g = cairo.LinearGradient(540, 870, 540, 1900); g.add_color_stop_rgba(0, 0.6, 0.7, 1, 0.22); g.add_color_stop_rgba(1, 0.6, 0.7, 1, 0)
    poly(ctx, [(470, 1160), (610, 1160), (820, 1920), (260, 1920)]); ctx.set_source(g); ctx.fill()
    # side doors in perspective
    side_door(ctx, 120, 300, 470, 640, 1500, 1260)
    side_door(ctx, 780, 960, 640, 470, 1260, 1500, lit=True)
    frame_pic(ctx, -60, 520, 120, 170, 25); frame_pic(ctx, 330, 690, 50, 80, 8, (0.6, 0.75, 0.9))
    frame_pic(ctx, 1010, 520, 120, 170, -25, (0.75, 0.6, 0.8))
    # ceiling lamp (off) and warm spill from the lit door
    ell(ctx, 540, 300, 90, 30); fs(ctx, (0.85, 0.85, 0.8), 4)
    g = cairo.LinearGradient(960, 1400, 500, 1920); g.add_color_stop_rgba(0, 1, 0.75, 0.4, 0.38); g.add_color_stop_rgba(1, 1, 0.75, 0.4, 0)
    poly(ctx, [(960, 1260), (960, 1500), (700, 2000), (380, 2000)]); ctx.set_source(g); ctx.fill()
    vignette(ctx, 0.35)


def bedroom_night(ctx):
    room(ctx, back=(200, 520, 680, 640), wall=(0.20, 0.22, 0.38), floor=(0.24, 0.17, 0.14), ceil=(0.10, 0.11, 0.22), plank=True)
    ctx.rectangle(560, 620, 220, 260); fs(ctx, (0.35, 0.45, 0.85), 7)
    ctx.move_to(670, 620); ctx.line_to(670, 880); ctx.move_to(560, 750); ctx.line_to(780, 750); st(ctx, (0.15, 0.15, 0.25), 7)
    ell(ctx, 720, 680, 26, 26); ctx.set_source_rgb(0.95, 0.95, 0.85); ctx.fill()
    glow(ctx, 670, 750, 420, (0.45, 0.55, 1), 0.3)
    poly(ctx, [(300, 640), (440, 640), (440, 840), (300, 840)]); fs(ctx, (0.85, 0.4, 0.3), 4)   # poster
    star(ctx, 370, 740, 50); ctx.set_source_rgb(1, 0.85, 0.3); ctx.fill()
    vignette(ctx, 0.4)


def bedroom_parents(ctx):
    room(ctx, back=(160, 520, 760, 660), wall=(0.22, 0.20, 0.32), floor=(0.24, 0.17, 0.14), ceil=(0.10, 0.10, 0.20))
    for x in (260, 820):
        rrect(ctx, x - 60, 980, 120, 90, 10); fs(ctx, (0.35, 0.25, 0.18), 4)
        poly(ctx, [(x - 40, 900), (x + 40, 900), (x + 55, 975), (x - 55, 975)]); fs(ctx, (0.95, 0.85, 0.6), 4)
    glow(ctx, 260, 930, 300, (1, 0.75, 0.4), 0.25)
    frame_pic(ctx, 420, 600, 240, 170, 0, (0.55, 0.7, 0.55))
    vignette(ctx, 0.4)


def living_day(ctx):
    room(ctx, back=(220, 560, 640, 620), wall=(0.95, 0.85, 0.65), floor=(0.75, 0.52, 0.32), ceil=(0.98, 0.93, 0.82), side=(0.90, 0.78, 0.58),
         rug=(0.55, 0.65, 0.75))
    ctx.rectangle(560, 640, 240, 300); fs(ctx, (0.75, 0.9, 1.0), 7)
    ctx.move_to(680, 640); ctx.line_to(680, 940); st(ctx, (1, 1, 1), 8)
    glow(ctx, 680, 790, 600, (1, 0.9, 0.6), 0.45)
    rrect(ctx, 260, 880, 260, 150, 30); fs(ctx, (0.45, 0.55, 0.45), 5)   # couch
    rrect(ctx, 240, 840, 300, 80, 30); fs(ctx, (0.50, 0.62, 0.50), 5)
    for x, c in [(-20, (0.9, 0.4, 0.3)), (40, (0.3, 0.5, 0.85)), (100, (0.95, 0.8, 0.3))]:
        frame_pic(ctx, x, 560, 50, 70, 10, c)


def house_ext(ctx):
    P1.house_night(ctx, 0.0)


# ---------------- props ----------------
def dog_body(ctx, x, y, s=1.0, t=0.0, bark=0.0, flip=False, sit=False, run=False, tilt=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(-s if flip else s, s)
    wag = 0.5 * sin(t * 16)
    ctx.save(); ctx.translate(130, -150); ctx.rotate(-0.9 + wag); rrect(ctx, -12, -110, 24, 110, 12); fs(ctx, FUR); ctx.restore()
    if not sit:
        stp = (22 if run else 10) * sin(t * (22 if run else 10))
        for lx, ph in ((-80, 1), (-40, -1), (60, -1), (100, 1)):
            ctx.save(); ctx.translate(lx, -95); ctx.rotate(ph * stp * 0.02)
            rrect(ctx, -18, 0, 36, 95, 16); fs(ctx, FURD if lx in (-40, 100) else FUR); ctx.restore()
        ell(ctx, 10, -135 + (6 * sin(t * 22) if run else 0), 135, 78); fs(ctx, FUR)
        ell(ctx, 10, -105, 90, 40); ctx.set_source_rgb(*CREAM); ctx.fill()
        hx, hy = -140, -235
    else:
        for lx in (-70, -30):
            rrect(ctx, lx - 16, -140, 32, 140, 14); fs(ctx, FUR)
        ell(ctx, 40, -110, 125, 115, -0.4); fs(ctx, FUR)
        ell(ctx, 10, -80, 60, 70); ctx.set_source_rgb(*CREAM); ctx.fill()
        hx, hy = -90, -300
    ctx.save(); ctx.translate(hx, hy); ctx.rotate(tilt); dog_head(ctx, 0, 0, 1.0, t, bark); ctx.restore()
    ctx.restore()


def dog_head(ctx, x, y, s, t, bark=0.0, tilt=0.0, look=0.0, sad=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(tilt); ctx.scale(s, s)
    ctx.save(); ctx.translate(60, -55); ctx.rotate(0.35 + 0.12 * sin(t * 3) + 0.4 * bark)
    ell(ctx, 0, 65, 36, 80); fs(ctx, FURD); ctx.restore()
    ell(ctx, 0, 0, 100, 92); fs(ctx, FUR)
    ell(ctx, -30, -30, 40, 30); ctx.set_source_rgba(1, 1, 1, 0.15); ctx.fill()
    ell(ctx, -80, 30, 66, 46); fs(ctx, CREAM)
    if bark > 0.05:
        poly(ctx, [(-140, 40), (-40, 46), (-70, 52 + 55 * bark)]); fs(ctx, (0.42, 0.10, 0.14), 4)
        for k in range(3):
            poly(ctx, [(-125 + k * 22, 42), (-114 + k * 22, 42), (-119 + k * 22, 54)]); ctx.set_source_rgb(1, 1, 1); ctx.fill()
        ell(ctx, -78, 52 + 40 * bark, 16, 9); ctx.set_source_rgb(0.95, 0.45, 0.5); ctx.fill()
    ell(ctx, -138, 14, 18, 14); ctx.set_source_rgb(0.1, 0.07, 0.05); ctx.fill()
    ell(ctx, -143, 9, 6, 4); ctx.set_source_rgba(1, 1, 1, 0.7); ctx.fill()
    for ex in (-36, 18):
        ell(ctx, ex + look * 5, -22, 15, 18); ctx.set_source_rgb(0.08, 0.06, 0.05); ctx.fill()
        ell(ctx, ex + look * 5 + 5, -29, 5.5, 5.5); ctx.set_source_rgb(1, 1, 1); ctx.fill()
        ell(ctx, ex + look * 5 - 4, -14, 2.5, 2.5); ctx.set_source_rgb(1, 1, 1); ctx.fill()
        ctx.move_to(ex - 16, -50 - 8 * bark + 6 * sad); ctx.line_to(ex + 14, -52 + 8 * bark - 6 * sad); st(ctx, shade(FURD, 0.3), 6)
    rrect(ctx, -10, 70, 100, 24, 10); fs(ctx, (0.85, 0.15, 0.2), 3)
    ell(ctx, 30, 102, 13, 13); fs(ctx, (1, 0.85, 0.3), 3)
    ctx.restore()


def blanket(ctx, y, col=(0.35, 0.45, 0.80)):
    ctx.move_to(-300, y + 40); ctx.curve_to(200, y - 30, 800, y - 30, 1380, y + 40); ctx.line_to(1380, 2400); ctx.line_to(-300, 2400); ctx.close_path()
    fs(ctx, col, 7)
    for k in range(5):
        ctx.move_to(-300, y + 140 + k * 90); ctx.curve_to(300, y + 100 + k * 90, 800, y + 160 + k * 90, 1380, y + 120 + k * 90)
        ctx.set_source_rgba(1, 1, 1, 0.12); ctx.set_line_width(14); ctx.stroke()


def snow(ctx, t, n=90, seed=1, sz=6, sp=180, a=0.85):
    rs = random.Random(seed)
    for i in range(n):
        x0, y0, k = rs.uniform(-100, 1180), rs.uniform(-200, 2100), rs.uniform(0.6, 1.4)
        y = (y0 + t * sp * k) % 2200 - 140; x = x0 + 30 * sin(t * 1.3 * k + i)
        ell(ctx, x, y, sz * k, sz * k); ctx.set_source_rgba(1, 1, 1, a); ctx.fill()


def breath(ctx, t, x, y, period=1.4, ph=0.0, s=1.0):
    u = ((t + ph) % period) / period
    if u > 0.75: return
    for k in range(3):
        r = (20 + 60 * u + k * 12) * s
        ell(ctx, x - (40 + 120 * u + k * 20) * s, y - 20 * u * s - k * 10 * s, r, r * 0.7); ctx.set_source_rgba(1, 1, 1, 0.32 * (1 - u / 0.75)); ctx.fill()


def dizzy_stars(ctx, t, x, y, r=130):
    for k in range(4):
        a_ = t * 5 + k * pi / 2
        star(ctx, x + r * cos(a_), y + 0.35 * r * sin(a_), 22 + 6 * sin(a_)); fs(ctx, (1, 0.86, 0.2), 4)


def steam(ctx, t, x, y, s=1.0):
    for sx in (-1, 1):
        for k in range(3):
            u = ((t * 2.2 + k / 3) % 1)
            ell(ctx, x + sx * (150 + 60 * u) * s, y - 220 * u * s, (24 + 30 * u) * s, (20 + 26 * u) * s)
            ctx.set_source_rgba(1, 1, 1, 0.7 * (1 - u)); ctx.fill()


def head_y(s, hy):  # body y that puts the head at screen y hy
    return hy + 340 * s


# ================= shots =================
def sh_clock(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.18 * sm(lt / d), 540, 1000)
    paint_layer(ctx, layer("bed_blur", bedroom_night, 22))
    overlay(ctx, (0, 0, 0.05), 0.35)
    # night stand top in perspective
    poly(ctx, [(-100, 1230), (1180, 1230), (1500, 2100), (-420, 2100)]); fs(ctx, (0.30, 0.20, 0.15), 0)
    poly(ctx, [(-100, 1230), (1180, 1230), (1190, 1260), (-110, 1260)]); ctx.set_source_rgb(0.4, 0.28, 0.2); ctx.fill()
    # clock body
    poly(ctx, [(250, 820), (830, 820), (870, 1300), (210, 1300)]); fs(ctx, (0.12, 0.12, 0.15), 8)
    rrect(ctx, 290, 900, 500, 300, 20); ctx.set_source_rgb(0.03, 0.02, 0.02); ctx.fill()
    on = (lt % 1.0) < 0.5
    glow(ctx, 540, 1050, 500, (1, 0.1, 0.05), 0.35)
    text(ctx, "3", 385, 1130, 210, col=(1, 0.15, 0.1)); text(ctx, "00", 625, 1130, 210, col=(1, 0.15, 0.1))
    for yy in (1010, 1080): ell(ctx, 478, yy, 14, 14); ctx.set_source_rgba(1, 0.15, 0.1, 1.0 if on else 0.35); ctx.fill()
    text(ctx, "AM", 740, 1180, 44, col=(1, 0.3, 0.25))
    ctx.restore()
    label(ctx, lt, 0.35, "3:00 AM", 760, 600, 70)


def sh_wake(ctx, lt, d, t_open=0.3):
    z = punch(lt) * (1 + 0.06 * sm(lt / d)); dx, dy = shake(lt, 10 if lt > t_open else 0)
    ctx.save(); cam(ctx, z, 540, 960, dx=dx, dy=dy)
    paint_layer(ctx, layer("bed_blur", bedroom_night, 22))
    ell(ctx, 540, 1320, 520, 200); fs(ctx, (0.95, 0.95, 1.0), 7)   # pillow
    s = 2.6; hy = 880
    mood = "neutral" if lt < t_open else dict(MOODS["shock"], eo=1.6)
    draw_char(ctx, BEN, dict(x=540, y=head_y(s, hy), s=s, mood=mood, blink=lt < t_open, dark=0.25, look=-0.3), lt)
    blanket(ctx, 1380)
    ctx.restore()
    if lt > t_open:
        for k in range(6):   # shock lines around the head
            a_ = -pi / 2 + (k - 2.5) * 0.35; p = clamp((lt - t_open) / 0.15)
            ctx.move_to(540 + 330 * cos(a_), 780 + 330 * sin(a_)); ctx.line_to(540 + (330 + 90 * p) * cos(a_), 780 + (330 + 90 * p) * sin(a_))
            st(ctx, (1, 1, 1), 10)
    overlay(ctx, (0.05, 0.08, 0.25), 0.25)


def sh_hall_bark(ctx, lt, d, words=()):
    z = 1.05 + 0.25 * sm(lt / d); dx, dy = shake(lt, 6)
    ctx.save(); cam(ctx, z, 540, 1300, dx=dx, dy=dy)
    paint_layer(ctx, layer("hall", hallway_night))
    bark = abs(sin(lt * 11))
    dog_body(ctx, 600, 1560, 1.25, lt, bark=bark)
    ctx.restore()
    for k, w0 in enumerate(words):
        pop_word(ctx, lt, w0, "WOOF!", 300 + (k % 2) * 420, 760 + (k % 3) * 140, rot=-0.15 + 0.3 * (k % 2))


def certificate(ctx, lt):
    ctx.rectangle(-420, -560, 840, 1120); fs(ctx, (0.99, 0.97, 0.90), 7)
    ctx.rectangle(-380, -520, 760, 1040); st(ctx, (0.75, 0.6, 0.3), 6)
    text(ctx, "ADOPTION", 0, -390, 80, col=(0.25, 0.25, 0.4)); text(ctx, "CERTIFICATE", 0, -310, 46, col=(0.55, 0.45, 0.3))
    ctx.rectangle(-170, -250, 340, 300); fs(ctx, (0.85, 0.92, 1.0), 5)
    ctx.save(); ctx.rectangle(-170, -250, 340, 300); ctx.clip(); dog_head(ctx, 20, -70, 1.25, 0.3); ctx.restore()
    text(ctx, "Name:  MAX", 0, 150, 52, col=(0.2, 0.2, 0.3))
    text(ctx, "Happy Tails Shelter", 0, 230, 40, col=(0.45, 0.45, 0.5), weight=False)
    for k in range(3): ctx.rectangle(-300, 300 + k * 60, 600, 10); ctx.set_source_rgb(0.85, 0.85, 0.88); ctx.fill()


def sh_adopt(ctx, lt, d, t_stamp=0.45):
    ctx.set_source_rgb(0.55, 0.38, 0.26); ctx.paint()
    for k in range(9): ctx.rectangle(0, k * 230, 1080, 6); ctx.set_source_rgba(0, 0, 0, 0.12); ctx.fill()
    glow(ctx, 540, 700, 900, (1, 0.85, 0.6), 0.25)
    dx, dy = shake(lt - t_stamp, 18 * (1 - clamp((lt - t_stamp) / 0.3))) if lt > t_stamp else (0, 0)
    ctx.save(); cam(ctx, 0.78 + 0.07 * sm(lt / d), 540, 1080, rot=-0.06, dx=dx, dy=dy)
    ctx.translate(540, 960); certificate(ctx, lt)
    if lt > t_stamp - 0.12:
        p = clamp((lt - t_stamp + 0.12) / 0.12); sc_ = lerp(2.6, 1.0, sm(p))
        ctx.save(); ctx.translate(130, 330); ctx.rotate(-0.25); ctx.scale(sc_, sc_)
        ctx.push_group()
        rrect(ctx, -250, -80, 500, 160, 20); st(ctx, (0.85, 0.1, 0.15), 16)
        text(ctx, "ADOPTED", 0, 38, 110, col=(0.85, 0.1, 0.15))
        ctx.pop_group_to_source(); ctx.paint_with_alpha(0.25 + 0.65 * p); ctx.restore()
    ctx.restore()
    if t_stamp <= lt < t_stamp + 0.1: overlay(ctx, (1, 1, 1), 0.5 * (1 - (lt - t_stamp) / 0.1), ADD)


def sh_flashback(ctx, lt, d, t_label=0.5):
    ctx.save(); cam(ctx, 1.08 - 0.08 * sm(lt / d), 540 + 30 * sm(lt / d), 1100)
    paint_layer(ctx, layer("living_blur", living_day, 8))
    dog_body(ctx, 700, 1640, 1.45, lt, sit=True, flip=True, tilt=-0.15)
    b = dict(x=420, y=1700, s=1.6, legs=False, mood="joy", tilt=0.12)
    b["armR"] = ik(b, 720, 1330, -1); b["armL"] = ik(b, 560, 1420, 1)
    draw_char(ctx, BEN, b, lt)
    for k in range(4):
        u = ((lt * 0.6 + k / 4) % 1)
        ctx.save(); ctx.translate(560 + 140 * sin(k * 2.1 + u * 3), 1000 - 380 * u); ctx.scale(1.2, 1.2)
        ctx.move_to(0, 18); ctx.curve_to(-40, -10, -18, -38, 0, -16); ctx.curve_to(18, -38, 40, -10, 0, 18)
        ctx.set_source_rgba(1, 0.35, 0.45, 1 - u); ctx.fill(); ctx.restore()
    ctx.restore()
    overlay(ctx, (1, 0.8, 0.5), 0.16); grain(ctx, lt, 0.1); vignette(ctx, 0.55, 380, 1100)
    label(ctx, lt, t_label, "1 week ago", 540, 470, 76)


def sh_dad_ecu(ctx, lt, d):
    dx, dy = shake(lt, 4)
    ctx.save(); cam(ctx, punch(lt) * (1 + 0.14 * sm(lt / d)), 540, 920, dx=dx, dy=dy)
    paint_layer(ctx, layer("hall_blur", hallway_night, 20))
    glow(ctx, 900, 800, 600, (1, 0.75, 0.4), 0.25)
    s = 2.8
    draw_char(ctx, DAD_P, dict(x=540, y=head_y(s, 900), s=s, mood=dict(MOODS["angry"], flush=0.9, teeth=True), glasses=True, dark=0.15), lt)
    steam(ctx, lt, 540, 640, 1.8)
    ctx.restore()


def sh_dad_yell(ctx, lt, d, sc, t0):
    pan = 60 * sm(lt / d)
    ctx.save()
    ctx.save(); depth(ctx, 0.5, pan, 0, 1.0); paint_layer(ctx, layer("hall_blur6", hallway_night, 6)); ctx.restore()
    ctx.save(); depth(ctx, 1.0, pan, 0)
    s = 2.0; P = dict(x=600, y=head_y(2.0, 800), s=s, mood=dict(MOODS["angry"], flush=0.8, bi=18), glasses=True, mouth=1.0 + 0.4 * talk(sc, "DA", t0 + lt), look=-0.8, dark=0.1)
    P["armL"] = ik(P, 170, 760, 1); P["armR"] = ("ang", 0.5, 0.2)
    draw_char(ctx, DAD_P, P, lt)
    ctx.restore()
    ctx.save(); depth(ctx, 1.8, pan, 0)
    paint_layer(ctx, layer("dog_fg", lambda c: dog_head(c, 120, 1750, 3.2, 0.2, look=0.6), 14, opaque=False))
    ctx.restore()
    ctx.restore()
    for k in range(5):   # yell burst lines
        a_ = -0.9 + k * 0.25; r0 = 330
        ctx.move_to(560 + r0 * cos(pi + a_), 820 + r0 * sin(pi + a_)); ctx.line_to(560 + (r0 + 110) * cos(pi + a_), 820 + (r0 + 110) * sin(pi + a_))
        st(ctx, (1, 1, 1), 9)


def sh_dog_tilt(ctx, lt, d, t_bark):
    ctx.save(); cam(ctx, 1 + 0.05 * sm(lt / d), 540, 960)
    paint_layer(ctx, layer("hall_blur", hallway_night, 20))
    tilt = -0.35 * sm(clamp(lt / 0.25)) * (1 - sm(clamp((lt - t_bark + 0.1) / 0.1)))
    bark = abs(sin((lt - t_bark) * 11)) if lt > t_bark else 0
    dx, dy = shake(lt, 8 if lt > t_bark else 0)
    dog_head(ctx, 560 + dx, 1000 + dy, 3.4, lt, bark=bark, tilt=tilt, look=-0.4)
    ctx.restore()
    if lt < t_bark: label(ctx, lt, 0.3, "?", 820, 520, 130, rot=0.15)
    else: pop_word(ctx, lt, t_bark, "WOOF!", 540, 520, 150, life=1)


def sh_dog_bark_cam(ctx, lt, d, words=()):
    dx, dy = shake(lt, 14)
    ctx.save(); cam(ctx, punch(lt, 0.12) * (1.0 + 0.12 * sm(lt / d)), 540, 1000, dx=dx, dy=dy)
    paint_layer(ctx, layer("hall_blur", hallway_night, 20))
    dog_head(ctx, 560, 1040, 3.8, lt, bark=abs(sin(lt * 11)))
    ctx.restore()
    speed_lines(ctx, lt, 540, 1000, 0.25)
    for k, w0 in enumerate(words): pop_word(ctx, lt, w0, "WOOF!", 280 + 520 * (k % 2), 560 + 120 * k)


def sh_sleeve(ctx, lt, d, t_grab=0.15):
    ctx.save(); cam(ctx, 1.05 + 0.08 * sm(lt / d), 540, 960)
    paint_layer(ctx, layer("hall_blur", hallway_night, 20))
    tug = 34 * sin(lt * 14) * (lt > t_grab)
    ctx.translate(tug, 0)
    ctx.move_to(-400, 640); ctx.line_to(560, 920); st(ctx, OUTL, 330); ctx.move_to(-400, 640); ctx.line_to(560, 920); st(ctx, BEN["top"], 312)
    ctx.move_to(520, 910); ctx.line_to(640, 945); st(ctx, OUTL, 300); ctx.move_to(520, 910); ctx.line_to(640, 945); st(ctx, shade(BEN["top"], 0.15), 282)
    for k in range(6): ctx.move_to(540 + k * 20, 790 + k * 6); ctx.line_to(520 + k * 20, 1060 + k * 6); st(ctx, shade(BEN["top"], 0.3), 4)
    ell(ctx, 790, 990, 120, 100, 0.3); fs(ctx, BEN["skin"], 7)
    for k in range(4): ell(ctx, 900 + k * 6, 930 + k * 48, 58, 26, -0.2); fs(ctx, BEN["skin"], 6)
    dog_head(ctx, 620 + 2.7 * 95, 900 - 2.7 * 30 + 130, 2.7, lt, bark=0.3, tilt=0.12 * sin(lt * 14), look=-0.5)
    ctx.move_to(250, 880); ctx.line_to(520, 945); st(ctx, OUTL, 62); ctx.move_to(250, 880); ctx.line_to(520, 945); st(ctx, BEN["top"], 48)
    ctx.restore()
    pop_word(ctx, lt, t_grab + 0.05, "GRRR!", 760, 560, 110, col=(1, 1, 1), life=0.9)


def wall_strip(ctx, off):
    ctx.rectangle(-200, 0, 1480, 1500); ctx.set_source_rgb(0.17, 0.19, 0.33); ctx.fill()
    ctx.rectangle(-200, 1500, 1480, 500); ctx.set_source_rgb(0.20, 0.14, 0.12); ctx.fill()
    ctx.rectangle(-200, 1480, 1480, 30); ctx.set_source_rgb(0.85, 0.85, 0.9); ctx.fill()
    for k in range(-2, 8):
        x = (k * 700 - off) % 3500 - 700
        if k % 2 == 0:
            ctx.rectangle(x, 520, 360, 980); fs(ctx, (0.30, 0.22, 0.18), 6); ell(ctx, x + 300, 1050, 12, 12); fs(ctx, (0.9, 0.75, 0.3), 3)
        else:
            frame_pic(ctx, x + 60, 650, 220, 280, 0, [(0.6, 0.75, 0.9), (0.85, 0.7, 0.5), (0.7, 0.85, 0.6)][k % 3])


def sh_track(ctx, lt, d):
    speed = 900
    off = lt * speed
    wall_strip(ctx, off)
    g = cairo.LinearGradient(0, 0, 0, 1920); g.add_color_stop_rgba(0, 0, 0, 0.1, 0.35); g.add_color_stop_rgba(1, 0, 0, 0.1, 0.1); ctx.set_source(g); ctx.paint()
    b = dict(x=430, y=1680, s=1.5, legs=True, mood=dict(MOODS["shock"], eyes=None), tilt=0.28, look=0.8)
    b["armR"] = ik(b, 615, 1545, -1); b["armL"] = ("ang", -0.35 + 0.15 * sin(lt * 12), -0.2)
    draw_char(ctx, BEN, b, lt)
    dog_body(ctx, 880, 1760, 1.0, lt, run=True, bark=0.25)
    # foreground banister posts zip past (blurred feel via alpha copies)
    for k in range(-1, 4):
        x = (k * 520 - off * 1.9) % 2600 - 400
        for j in range(5):
            ctx.rectangle(x + j * 14, 1200, 70, 800); ctx.set_source_rgba(0.35, 0.24, 0.16, 0.22); ctx.fill()
    speed_lines(ctx, lt, horiz=True, a=0.18, n=20)


def sh_dash(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.1 * sm(lt / d), 540, 1050)
    paint_layer(ctx, layer("hall2", hall_to_parents))
    u = sm(clamp(lt / (d * 0.9)))
    x = lerp(620, 560, u); y = lerp(1900, 1210, u); s = lerp(1.6, 0.42, u)
    dog_body(ctx, x, y, s, lt, run=True, flip=True)
    ctx.restore()
    speed_lines(ctx, lt, 540, 1000, 0.3)


def hall_to_parents(ctx):
    hallway_night(ctx)
    ctx.rectangle(455, 830, 170, 330); fs(ctx, (0.32, 0.24, 0.20), 5)
    ctx.rectangle(470, 1150, 140, 10); ctx.set_source_rgb(1, 0.8, 0.45); ctx.fill()
    rrect(ctx, 490, 880, 100, 40, 6); fs(ctx, (0.95, 0.9, 0.75), 3); text(ctx, "M & D", 540, 910, 22, col=(0.4, 0.3, 0.2))


def sh_parents(ctx, lt, d, t_x2):
    ctx.save(); cam(ctx, punch(lt) * (1.0 + 0.08 * sm(lt / d)), 540, 1100)
    paint_layer(ctx, layer("par_blur", bedroom_parents, 10))
    rrect(ctx, 80, 620, 920, 420, 40); fs(ctx, (0.45, 0.30, 0.22), 7)   # headboard
    for x in (330, 750): ell(ctx, x, 1040, 170, 70); fs(ctx, (0.95, 0.95, 1.0), 6)
    m = dict(x=330, y=head_y(1.35, 960), s=1.35, mood=dict(MOODS["worried"]), look=0.6, dark=0.2, tilt=-0.05)
    draw_char(ctx, MOM_P, m, lt)
    tug = 30 * sin(lt * 13)
    P = dict(x=760, y=head_y(1.4, 960), s=1.4, mood=dict(MOODS["angry"], eo=0.4, teeth=lt > t_x2 - 0.2), glasses=False, look=0.5, dark=0.2, tilt=0.12 + 0.03 * sin(lt * 13))
    P["armR"] = ik(P, 990 + tug, 1210, -1)
    draw_char(ctx, DAD_P, P, lt)
    blanket(ctx, 1300, (0.55, 0.40, 0.65))
    dog_body(ctx, 1150 + tug, 1460, 0.9, lt, bark=0.25)
    ctx.restore()
    overlay(ctx, (0.05, 0.08, 0.25), 0.2)
    label(ctx, lt, t_x2, "x2", 860, 560, 130, rot=0.1, col=(1, 0.86, 0.15))


def sh_door_out(ctx, lt, d):
    ctx.save(); cam(ctx, 1.25 - 0.15 * sm(lt / d), 540, 1150)
    paint_layer(ctx, layer("house_blur", house_ext, 3))
    op = sm(clamp(lt / 0.5))
    ctx.rectangle(400, 1000, 280, 470); ctx.set_source_rgb(1, 0.85, 0.55); ctx.fill()
    glow(ctx, 540, 1250, 500, (1, 0.8, 0.45), 0.5 * op)
    w_ = 280 * (1 - op * 0.85)
    poly(ctx, [(400, 1000), (400 + w_, 1000 - 30 * op), (400 + w_, 1470 + 30 * op), (400, 1470)]); fs(ctx, (0.45, 0.15, 0.15), 6)
    if lt > 0.45:
        k = clamp((lt - 0.45) / 1.0)
        for i, (ch, xo) in enumerate([(DAD_P, -90), (MOM_P, 20), (BEN, 120)]):
            draw_char(ctx, ch, dict(x=540 + xo, y=1520 + 40 * k, s=0.55 + 0.15 * k, legs=True, mood="worried", dark=0.55, tremble=0.6), lt)
    ctx.restore()
    snow(ctx, lt, 60, 2, 9, 220)


def sh_cold(ctx, lt, d, t_lab):
    pan = 50 * sm(lt / d)
    ctx.save(); depth(ctx, 0.4, pan, 0, 1.0); paint_layer(ctx, layer("house_blur8", house_ext, 7)); ctx.restore()
    snow(ctx, lt, 50, 3, 4, 120, 0.6)
    ctx.save(); depth(ctx, 1.0, pan, 0)
    ctx.rectangle(-300, 1420, 1700, 700); ctx.set_source_rgb(0.85, 0.88, 0.95); ctx.fill()
    for i, (ch, x, extra) in enumerate([(DAD_P, 230, dict(glasses=True)), (MOM_P, 520, {}), (BEN, 800, {})]):
        P = dict(x=x, y=1540, s=1.25, legs=True, mood=dict(MOODS["scared"], teeth=True), tremble=1.2, dark=0.15,
                 armL=("ik", 30, -105, 1), armR=("ik", -30, -110, -1)); P.update(extra)
        draw_char(ctx, ch, P, lt)
        hx, hy = head_world(P); breath(ctx, lt, hx - 20, hy + 70, ph=i * 0.4, s=1.2)
    ctx.restore()
    ctx.save(); depth(ctx, 1.7, pan, 0); snow(ctx, lt, 25, 4, 16, 300); ctx.restore()
    label(ctx, lt, t_lab, "-5°C", 830, 520, 110, rot=0.08, col=(0.7, 0.9, 1.0))


def sh_dizzy_boy(ctx, lt, d):
    rot = 0.12 * sin(lt * 4.5)
    ctx.save(); cam(ctx, 1.05 + 0.05 * sin(lt * 3), 540, 960, rot=rot)
    ctx.set_source_rgb(0.12, 0.15, 0.3); ctx.paint()
    ctx.save(); ctx.translate(540, 900); ctx.rotate(lt * 2.5)
    for k in range(16):
        ctx.move_to(0, 0); ctx.arc(0, 0, 1600, k * pi / 8, k * pi / 8 + pi / 16); ctx.close_path()
        ctx.set_source_rgba(0.3, 0.45, 0.8, 0.35); ctx.fill()
    ctx.restore()
    s = 2.7
    draw_char(ctx, BEN, dict(x=540, y=head_y(s, 880), s=s, mood=dict(MOODS["worried"], eyes="spiral", mo=0.3), tilt=0.15 * sin(lt * 3)), lt)
    dizzy_stars(ctx, lt, 540, 560, 260)
    ctx.restore()
    overlay(ctx, (0.4, 0.9, 0.5), 0.08)


def sh_mom_dizzy(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.08 * sm(lt / d), 540, 1000, rot=0.05 * sin(lt * 3))
    paint_layer(ctx, layer("house_blur8", house_ext, 7))
    ctx.rectangle(-300, 1650, 1700, 400); ctx.set_source_rgb(0.85, 0.88, 0.95); ctx.fill()
    s = 2.0; P = dict(x=540, y=head_y(s, 860), s=s, mood=dict(MOODS["sad"], eyes="spiral"), tilt=0.18 * sin(lt * 2.6), dark=0.1)
    P["armR"] = ik(P, 640, 690, -1)
    draw_char(ctx, MOM_P, P, lt)
    hx, hy = head_world(P)
    dizzy_stars(ctx, lt, hx, hy - 230, 200)
    ctx.restore()
    snow(ctx, lt, 40, 5, 10, 200)


# ================= scene → shot lists =================
def shots(sc):
    D = DUR(sc)
    if sc == "a":
        t1, t2 = WT("a", "our") - 0.05, WT("a", "would") - 0.12
        return [(0, t1, lambda c, l, d: sh_clock(c, l, d)),
                (t1, t2, lambda c, l, d: sh_wake(c, l, d, 0.25)),
                (t2, D, lambda c, l, d: sh_hall_bark(c, l, d, words=(0.15, 0.6, 1.05)))], {t1: "whip"}
    if sc == "b":
        t1, t2, t3, t4 = WT("b", "just") - 0.3, WT("b", "dad") - 0.05, WT("b", "max") - 0.05, WT("b", "everyone's") + 0.25
        return [(0, t1, lambda c, l, d: sh_adopt(c, l, d, WT("b", "adopted") + 0.05)),
                (t1, t2, lambda c, l, d: sh_flashback(c, l, d, WT("b", "one") - t1)),
                (t2, t3, lambda c, l, d: sh_dad_ecu(c, l, d)),
                (t3, t4, lambda c, l, d: sh_dad_yell(c, l, d, "b", t3)),
                (t4, D, lambda c, l, d: sh_dog_tilt(c, l, d, WT("b", "sleep") + 0.45 - t4))], {t1: "whip"}
    if sc == "c":
        t1, t2, t3, t4 = WT("c", "he") - 0.05, WT("c", "and") - 0.05, WT("c", "then") - 0.05, WT("c", "and", li=1, nth=0) - 0.1
        return [(0, t1, lambda c, l, d: sh_dog_bark_cam(c, l, d, words=(0.1, 0.7, 1.3))),
                (t1, t2, lambda c, l, d: sh_sleeve(c, l, d)),
                (t2, t3, lambda c, l, d: sh_track(c, l, d)),
                (t3, t4, lambda c, l, d: sh_dash(c, l, d)),
                (t4, D, lambda c, l, d: sh_parents(c, l, d, WT("c", "same") - t4))], {t3: "whip"}
    if sc == "d":
        t1, t2, t3 = WT("d", "in") - 0.05, WT("d", "my") - 0.05, WT("d", "mom") - 0.05
        return [(0, t1, lambda c, l, d: sh_door_out(c, l, d)),
                (t1, t2, lambda c, l, d: sh_cold(c, l, d, WT("d", "cold") - 0.1 - t1)),
                (t2, t3, lambda c, l, d: sh_dizzy_boy(c, l, d)),
                (t3, D, lambda c, l, d: sh_mom_dizzy(c, l, d))], {t2: "whip"}


SHOTS = {sc: shots(sc) for sc in TL}


def draw_shot_at(ctx, sc, t):
    lst, _ = SHOTS[sc]
    for t0, t1, fn in lst:
        if t0 <= t < t1 or (fn is lst[-1][2] and t >= t0):
            ctx.save(); fn(ctx, t - t0, t1 - t0); ctx.restore(); return


WHIP = 0.13


def draw_scene(ctx, sc, t):
    lst, trans = SHOTS[sc]
    for tb, kind in trans.items():
        if abs(t - tb) < WHIP:
            u = (t - tb) / WHIP            # -1..1
            off = (-1 if u < 0 else 1) * (1 - abs(u)) * 0 + (u * 1100 if u < 0 else (u - 1) * 1100)
            tt = tb - 0.001 if u < 0 else tb + 0.001
            ctx.push_group(); draw_shot_at(ctx, sc, tt if abs(u) > 0.99 else t); pat = ctx.pop_group()
            ctx.set_source_rgb(0, 0, 0); ctx.paint()
            n = 9; ctx.save(); ctx.set_operator(ADD)
            for k in range(n):
                ctx.save(); ctx.translate(-off - k * 38, 0); ctx.set_source(pat); ctx.paint_with_alpha(1 / n); ctx.restore()
            ctx.restore(); return
    draw_shot_at(ctx, sc, t)


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
    ctx.set_source_rgb(*((1, 0.86, 0.15) if spk == "DA" else (1, 1, 1))); ctx.fill()
    ctx.restore()


def frame(surf, sc, t):
    ctx = cairo.Context(surf)
    ctx.set_source_rgb(0, 0, 0); ctx.paint()
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    draw_scene(ctx, sc, t)
    ctx.set_operator(cairo.OPERATOR_OVER)
    grain(ctx, t, 0.045)
    captions(ctx, sc, t)
    P1.header(ctx)


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


P1.HEADER[:] = ["MY DOG SAVED MY FAMILY", "FULL STORY"]

if __name__ == "__main__":
    os.makedirs(f"{EP}/preview", exist_ok=True)
    if sys.argv[1] == "preview":
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        for arg in sys.argv[2:]:
            sc, ts = arg.split(":"); frame(surf, sc, float(ts)); surf.write_to_png(f"{EP}/preview/{sc}_{ts}.png")
    else:
        for sc in (sys.argv[2:] or TL.keys()): render(sc)
