"""Reusable cartoon rig + drawing helpers (Cairo). Characters are drawn in local units:
origin at hip centre, head centre at (0,-340), shoulders at (+-82,-212)."""
import cairo, math
from math import sin, cos, pi

W, H, FPS = 1080, 1920, 30
OUTL = (0.09, 0.07, 0.11)
LW = 5.5
DARK = [0.0]
DARKC = (0.03, 0.04, 0.09)


def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def sm(x): x = clamp(x); return x * x * (3 - 2 * x)
def lerp(a, b, u): return a + (b - a) * u
def mix(c1, c2, u): return tuple(lerp(a, b, u) for a, b in zip(c1, c2))
def ramp(t, t0, t1): return sm((t - t0) / (t1 - t0)) if t1 > t0 else float(t >= t0)
def back_out(x):
    x = clamp(x); c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def C(c): return mix(c, DARKC, DARK[0])
def shade(c, k): return mix(c, (0, 0, 0), k)
def tint(c, k): return mix(c, (1, 1, 1), k)


def fs(ctx, col, lw=LW, a=1.0, stroke=True):
    ctx.set_source_rgba(*C(col), a)
    if stroke:
        ctx.fill_preserve(); ctx.set_source_rgba(*C(OUTL), a); ctx.set_line_width(lw); ctx.stroke()
    else:
        ctx.fill()


def st(ctx, col, lw):
    ctx.set_source_rgb(*C(col)); ctx.set_line_width(lw); ctx.stroke()


def ell(ctx, x, y, rx, ry, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(max(rx, 0.01), max(ry, 0.01))
    ctx.new_sub_path(); ctx.arc(0, 0, 1, 0, 2 * pi); ctx.restore()


def rrect(ctx, x, y, w, h, r):
    r = max(0.1, min(r, w / 2, h / 2)); ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, pi / 2)
    ctx.arc(x + r, y + h - r, r, pi / 2, pi); ctx.arc(x + r, y + r, r, pi, 1.5 * pi); ctx.close_path()


def poly(ctx, pts):
    ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    ctx.close_path()


def blob(ctx, circles, col):
    for (x, y, r) in circles: ell(ctx, x, y, r + LW * 0.9, r + LW * 0.9)
    ctx.set_source_rgb(*C(OUTL)); ctx.fill()
    for (x, y, r) in circles: ell(ctx, x, y, r, r)
    ctx.set_source_rgb(*C(col)); ctx.fill()


def star(ctx, x, y, r, n=5, inner=0.45, rot=-pi / 2):
    for i in range(2 * n):
        rr = r if i % 2 == 0 else r * inner
        a = rot + i * pi / n
        (ctx.move_to if i == 0 else ctx.line_to)(x + rr * cos(a), y + rr * sin(a))
    ctx.close_path()


def glow(ctx, x, y, r, col, a, op=cairo.OPERATOR_ADD):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col, a); g.add_color_stop_rgba(1, *col, 0)
    ctx.save(); ctx.set_operator(op); ctx.set_source(g); ctx.arc(x, y, r, 0, 2 * pi); ctx.fill(); ctx.restore()


def text(ctx, s, x, y, size, col=(1, 1, 1), stroke=0, scol=(0, 0, 0), align="c", weight=True, font="Poppins"):
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if weight else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    e = ctx.text_extents(s)
    xx = x - e.x_advance / 2 if align == "c" else x if align == "l" else x - e.x_advance
    ctx.new_path(); ctx.move_to(xx, y); ctx.text_path(s)
    if stroke:
        ctx.set_source_rgb(*scol); ctx.set_line_width(stroke); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
    ctx.set_source_rgb(*col); ctx.fill()
    return e.x_advance


# ---------------- characters ----------------
SH_X, SH_Y = 82, -212
L1, L2, AW = 105, 100, 40


def arm_pts(sx, sy, spec):
    if spec[0] == "ang":
        a1, a2 = spec[1], spec[2]
        ex, ey = sx + L1 * sin(a1), sy + L1 * cos(a1)
        hx, hy = ex + L2 * sin(a2), ey + L2 * cos(a2)
    else:
        tx, ty, bend = spec[1], spec[2], spec[3]
        dx, dy = tx - sx, ty - sy; d = max(1e-3, math.hypot(dx, dy)); d2 = min(d, L1 + L2 - 1)
        a = math.acos(clamp((L1 * L1 + d2 * d2 - L2 * L2) / (2 * L1 * d2), -1, 1))
        ang = math.atan2(dy, dx) + bend * a
        ex, ey = sx + L1 * cos(ang), sy + L1 * sin(ang)
        hx, hy = sx + dx / d * d2, sy + dy / d * d2
    return (ex, ey), (hx, hy)


def draw_arm(ctx, ch, sx, sy, spec, sleeve_frac=0.86, hand=True):
    (ex, ey), (hx, hy) = arm_pts(sx, sy, spec)
    cx_, cy_ = lerp(ex, hx, sleeve_frac), lerp(ey, hy, sleeve_frac)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.move_to(ex, ey); ctx.line_to(hx, hy); st(ctx, OUTL, AW * 0.7 + 2 * LW)
    ctx.move_to(ex, ey); ctx.line_to(hx, hy); st(ctx, ch["skin"], AW * 0.7)
    ctx.move_to(sx, sy); ctx.line_to(ex, ey); ctx.line_to(cx_, cy_); st(ctx, OUTL, AW + 2 * LW)
    ctx.move_to(sx, sy); ctx.line_to(ex, ey); ctx.line_to(cx_, cy_); st(ctx, ch.get("sleeve", ch["top"]), AW)
    if hand:
        ell(ctx, hx, hy, 22, 22); fs(ctx, ch["skin"])
    return (hx, hy)


def torso_path(ctx, b, wide=1.0):
    ctx.new_path()
    ctx.move_to(-78 * wide, 0); ctx.line_to(-86 * wide, -170 * b)
    ctx.curve_to(-90 * wide, -215 * b, -70 * wide, -236 * b, -34, -238 * b)
    ctx.line_to(34, -238 * b)
    ctx.curve_to(70 * wide, -236 * b, 90 * wide, -215 * b, 86 * wide, -170 * b)
    ctx.line_to(78 * wide, 0); ctx.close_path()


def back_hair(ctx, ch, hx, hy):
    st_ = ch.get("hairstyle")
    col = ch["hair"]
    if st_ == "curly":
        circ = [(hx + 100 * cos(math.radians(a)), hy + 100 * sin(math.radians(a)), 48) for a in range(150, 400, 20)]
        for k in range(4):
            for sx in (-1, 1):
                circ.append((hx + sx * (104 - k * 2), hy + 40 + k * 44, 46 - k * 3))
        blob(ctx, circ, col)
    elif st_ == "bob":
        rrect(ctx, hx - 118, hy - 118, 236, 214, 100); fs(ctx, col)
    elif st_ == "bun":
        ell(ctx, hx + 5, hy - 120, 46, 44); fs(ctx, col)
        rrect(ctx, hx - 104, hy - 100, 208, 150, 90); fs(ctx, col)
    elif st_ == "long":
        rrect(ctx, hx - 120, hy - 118, 240, 360, 110); fs(ctx, col)


def front_hair(ctx, ch, hx, hy):
    st_ = ch.get("hairstyle"); col = ch["hair"]
    if st_ == "crew":
        ctx.move_to(hx - 97, hy - 6)
        ctx.curve_to(hx - 104, hy - 92, hx - 52, hy - 120, hx, hy - 118)
        ctx.curve_to(hx + 56, hy - 120, hx + 104, hy - 92, hx + 97, hy - 6)
        ctx.line_to(hx + 88, hy - 22)
        ctx.curve_to(hx + 74, hy - 64, hx + 32, hy - 72, hx - 8, hy - 68)
        ctx.curve_to(hx - 52, hy - 66, hx - 82, hy - 50, hx - 88, hy - 22)
        ctx.close_path(); fs(ctx, col)
    elif st_ == "curly":
        circ = [(hx + 84 * cos(math.radians(a)), hy + 88 * sin(math.radians(a)) - 10, 31) for a in range(200, 345, 20)]
        circ += [(hx, hy - 96, 38), (hx - 44, hy - 90, 32), (hx + 44, hy - 90, 32)]
        blob(ctx, circ, col)
    elif st_ == "bob":
        ctx.move_to(hx - 102, hy + 26)
        ctx.curve_to(hx - 112, hy - 82, hx - 60, hy - 126, hx, hy - 122)
        ctx.curve_to(hx + 70, hy - 126, hx + 114, hy - 82, hx + 104, hy + 44)
        ctx.curve_to(hx + 92, hy - 20, hx + 60, hy - 72, hx - 10, hy - 60)
        ctx.curve_to(hx - 60, hy - 56, hx - 86, hy - 20, hx - 102, hy + 26)
        ctx.close_path(); fs(ctx, col)
    elif st_ == "long":
        ctx.move_to(hx - 106, hy + 60)
        ctx.curve_to(hx - 112, hy - 92, hx - 52, hy - 124, hx, hy - 120)
        ctx.curve_to(hx + 52, hy - 124, hx + 112, hy - 92, hx + 106, hy + 60)
        ctx.curve_to(hx + 96, hy - 10, hx + 70, hy - 72, hx + 14, hy - 84)
        ctx.curve_to(hx - 30, hy - 70, hx - 80, hy - 40, hx - 94, hy + 10)
        ctx.close_path(); fs(ctx, col)
    elif st_ == "bun":
        ctx.move_to(hx - 100, hy + 10)
        ctx.curve_to(hx - 106, hy - 90, hx - 50, hy - 120, hx, hy - 118)
        ctx.curve_to(hx + 50, hy - 120, hx + 106, hy - 90, hx + 100, hy + 10)
        ctx.curve_to(hx + 90, hy - 45, hx + 50, hy - 78, hx + 2, hy - 80)
        ctx.curve_to(hx - 50, hy - 78, hx - 90, hy - 45, hx - 100, hy + 10)
        ctx.close_path(); fs(ctx, col)


def police_hat(ctx, hx, hy):
    navy = (0.10, 0.14, 0.26)
    ctx.move_to(hx - 94, hy - 60); ctx.line_to(hx - 122, hy - 140)
    ctx.curve_to(hx - 60, hy - 178, hx + 60, hy - 178, hx + 122, hy - 140)
    ctx.line_to(hx + 94, hy - 60); ctx.close_path(); fs(ctx, navy)
    rrect(ctx, hx - 96, hy - 88, 192, 30, 6); fs(ctx, (0.05, 0.05, 0.07))
    ctx.move_to(hx - 100, hy - 62); ctx.curve_to(hx - 50, hy - 30, hx + 50, hy - 30, hx + 100, hy - 62)
    ctx.curve_to(hx + 60, hy - 52, hx - 60, hy - 52, hx - 100, hy - 62); ctx.close_path(); fs(ctx, (0.04, 0.04, 0.06))
    shield(ctx, hx, hy - 118, 20); fs(ctx, (0.95, 0.76, 0.25), 3.5)


def shield(ctx, x, y, s):
    ctx.move_to(x, y - s); ctx.line_to(x + s * 0.85, y - s * 0.6); ctx.line_to(x + s * 0.75, y + s * 0.3)
    ctx.curve_to(x + s * 0.5, y + s * 0.8, x + s * 0.1, y + s, x, y + s * 1.05)
    ctx.curve_to(x - s * 0.1, y + s, x - s * 0.5, y + s * 0.8, x - s * 0.75, y + s * 0.3)
    ctx.line_to(x - s * 0.85, y - s * 0.6); ctx.close_path()


def outfit(ctx, ch, b, P):
    o = ch["outfit"]; top = ch["top"]
    if o == "uniform":
        poly(ctx, [(-28, -238 * b), (0, -192 * b), (28, -238 * b)]); fs(ctx, (0.06, 0.08, 0.15), 4)
        for sx in (-1, 1):
            poly(ctx, [(sx * 36, -242 * b), (sx * 4, -196 * b), (sx * 52, -214 * b)]); fs(ctx, tint(top, 0.08), 4)
        ctx.move_to(0, -192 * b); ctx.line_to(0, -22); st(ctx, shade(top, 0.4), 4)
        for yy in (-160, -118, -76): ell(ctx, 6, yy * b, 5, 5); fs(ctx, (0.75, 0.75, 0.8), 2.5)
        for sx in (-1, 1):
            rrect(ctx, sx * 44 - 20, -168 * b, 40, 44, 6); fs(ctx, tint(top, 0.05), 3.5)
        star(ctx, 46, -180 * b, 21); fs(ctx, (0.98, 0.78, 0.22), 3.5)
        rrect(ctx, -66, -190 * b, 40, 10, 3); fs(ctx, (0.92, 0.8, 0.4), 2.5)
        rrect(ctx, -80, -26, 160, 26, 5); fs(ctx, (0.05, 0.05, 0.07), 4)
        rrect(ctx, -14, -22, 28, 18, 3); fs(ctx, (0.8, 0.8, 0.85), 3)
    elif o == "hoodie":
        ell(ctx, 0, -236 * b, 60, 20); fs(ctx, shade(top, 0.18), 4.5)
        for sx in (-1, 1):
            ctx.move_to(sx * 15, -222 * b); ctx.line_to(sx * 17, -158 * b); st(ctx, (0.95, 0.95, 0.95), 4.5)
        poly(ctx, [(-52, -74), (52, -74), (64, -12), (-64, -12)]); fs(ctx, shade(top, 0.08), 4)
    elif o == "dress":
        ctx.move_to(-40, -238 * b); ctx.curve_to(-30, -200 * b, 30, -200 * b, 40, -238 * b); ctx.close_path()
        fs(ctx, ch["skin"], 4)
        rrect(ctx, -82, -70, 164, 22, 8); fs(ctx, ch.get("sash", shade(top, 0.15)), 3.5)
    elif o == "sweater":
        ctx.move_to(-34, -238 * b); ctx.curve_to(-24, -212 * b, 24, -212 * b, 34, -238 * b); st(ctx, shade(top, 0.25), 5)
        for xx in range(-70, 75, 14):
            ctx.move_to(xx, -24); ctx.line_to(xx, -4); st(ctx, shade(top, 0.2), 3)
    elif o == "longsleeve":
        ctx.move_to(-32, -238 * b); ctx.curve_to(-22, -214 * b, 22, -214 * b, 32, -238 * b); st(ctx, shade(top, 0.25), 5)
    elif o == "cardigan":
        poly(ctx, [(-30, -238 * b), (30, -238 * b), (26, 0), (-26, 0)]); fs(ctx, (0.97, 0.96, 0.93), 4)
        for sx in (-1, 1):
            ctx.move_to(sx * 30, -238 * b); ctx.line_to(sx * 26, 0); st(ctx, shade(top, 0.25), 5)
        for yy in (-180, -130, -80, -30): ell(ctx, -36, yy * b, 5, 5); fs(ctx, shade(top, 0.4), 2.5)
        if not ch.get("no_lanyard"):
            ctx.move_to(-26, -236 * b); ctx.line_to(-6, -120 * b); ctx.move_to(26, -236 * b); ctx.line_to(6, -120 * b)
            st(ctx, (0.25, 0.45, 0.8), 4)
            rrect(ctx, -20, -124 * b, 40, 52, 5); fs(ctx, (1, 1, 1), 3)
            rrect(ctx, -12, -114 * b, 24, 18, 3); fs(ctx, (0.6, 0.75, 0.9), 2)
    elif o == "orange":
        ctx.move_to(-30, -238 * b); ctx.curve_to(-20, -205 * b, 20, -205 * b, 30, -238 * b); st(ctx, shade(top, 0.25), 5)
    elif o == "suit":
        poly(ctx, [(-34, -238 * b), (34, -238 * b), (22, -60), (-22, -60)]); fs(ctx, (0.97, 0.97, 0.97), 4)
        poly(ctx, [(-6, -228 * b), (6, -228 * b), (10, -110), (0, -95), (-10, -110)]); fs(ctx, (0.5, 0.1, 0.15), 3)
        for sx in (-1, 1):
            poly(ctx, [(sx * 36, -240 * b), (sx * 22, -60), (sx * 50, -150 * b)]); fs(ctx, shade(top, 0.15), 4)
        if not ch.get("no_badge"):
            shield(ctx, -52, -40, 16); fs(ctx, (0.95, 0.76, 0.25), 3)


def legs(ctx, ch, b):
    pc = ch.get("pants", (0.15, 0.15, 0.2))
    for sx in (-1, 1):
        rrect(ctx, sx * 38 - 31, -10, 62, 250, 24); fs(ctx, pc)
        ell(ctx, sx * 40 + sx * 10, 246, 46, 22); fs(ctx, ch.get("shoes", (0.06, 0.06, 0.08)))


def blinking(t, seed):
    return ((t + seed * 1.37) % 3.9) < 0.11


MOODS = {
    "neutral": dict(bi=0, bo=0, eo=1.0, ew=0, smile=0.15, mo=0, lid=0, tear=0, flush=0, tremble=0, smirk=0, tilt=0),
    "happy":   dict(bi=-4, bo=-3, eo=0.92, smile=1.0),
    "joy":     dict(bi=-6, bo=-5, eo=0.0, smile=1.0, mo=0.35),           # eyes closed in a laugh
    "smirk":   dict(bi=3, bo=-9, eo=0.75, smile=0.3, smirk=1, tilt=0.06),
    "cold":    dict(bi=7, bo=-4, eo=0.6, smile=-0.35),
    "angry":   dict(bi=14, bo=-8, eo=0.55, smile=-0.7, flush=0.45),
    "sad":     dict(bi=-11, bo=4, eo=0.85, lid=0.55, smile=-0.65, tilt=-0.04),
    "worried": dict(bi=-10, bo=3, eo=1.0, lid=0.25, smile=-0.35),
    "scared":  dict(bi=-13, bo=2, eo=1.22, ew=1, smile=-0.45, mo=0.3, tremble=0.6),
    "shock":   dict(bi=-15, bo=-15, eo=1.35, ew=1, mo=0.95),
    "crying":  dict(bi=-12, bo=5, eo=0.7, lid=0.5, smile=-0.85, mo=0.25, tear=1, tremble=0.5, tilt=-0.05),
    "hopeful": dict(bi=-8, bo=-2, eo=1.05, ew=0, smile=0.35, tear=0.4),
}


def mood_at(track, t, blend=0.25):
    """track: [(t0, mood_or_dict), ...] sorted. Returns blended face dict."""
    def get(mv):
        d = dict(MOODS["neutral"]); d.update(MOODS[mv] if isinstance(mv, str) else mv); return d
    cur, prev, tc = get(track[0][1]), None, track[0][0]
    for i, (tt, mv) in enumerate(track):
        if t >= tt:
            prev = get(track[i - 1][1]) if i > 0 else None; cur = get(mv); tc = tt
    if prev is None: return cur
    u = sm((t - tc) / blend)
    return {k: lerp(prev.get(k, 0), cur.get(k, 0), u) for k in cur}


def draw_face(ctx, ch, P, F, t, hx, hy, look, lookY, m):
    fx, fy = hx + look * 14, hy + lookY * 7
    if ch.get("blush") or F["flush"] > 0.05:
        a = 0.28 + 0.4 * F["flush"]
        col = mix((0.95, 0.45, 0.45), (0.9, 0.15, 0.12), F["flush"])
        for sx in (-1, 1):
            ell(ctx, fx + sx * 54, fy + 36, 18 + 6 * F["flush"], 9 + 3 * F["flush"]); ctx.set_source_rgba(*C(col), a); ctx.fill()
    if ch.get("freckles"):
        for sx in (-1, 1):
            for (ox, oy) in ((44, 22), (58, 30), (50, 38), (66, 20), (38, 34)):
                ell(ctx, fx + sx * ox, fy + oy, 3.2, 3.2); ctx.set_source_rgba(0.62, 0.36, 0.22, 0.75); ctx.fill()
    eyc = ch.get("eye", (0.1, 0.07, 0.06))
    eo, ew = F["eo"], F["ew"]
    blink = P.get("blink", False)
    for sx in (-1, 1):
        ex_, ey_ = fx + sx * 34, fy + 2
        es = F.get("eyes")
        if es == "x" and not blink:
            ctx.move_to(ex_ - sx * 14, ey_ - 12); ctx.line_to(ex_ + sx * 10, ey_); ctx.line_to(ex_ - sx * 14, ey_ + 12); st(ctx, OUTL, 7)
            continue
        if es == "spiral" and not blink:
            ctx.save(); ctx.translate(ex_, ey_); ctx.rotate(t * 9 * sx)
            ell(ctx, 0, 0, 20, 20); fs(ctx, (1, 1, 1), 4)
            ctx.new_path()
            for k in range(60):
                a_ = k * 0.32; r_ = 1 + k * 0.28
                (ctx.line_to if k else ctx.move_to)(r_ * cos(a_), r_ * sin(a_))
            st(ctx, OUTL, 3.5); ctx.restore()
            continue
        if blink or eo < 0.08:
            k = 1 if not blink and F["smile"] > 0.5 else -1   # happy closed eyes curve up
            ctx.move_to(ex_ - 14, ey_ + 2); ctx.curve_to(ex_ - 5, ey_ + 2 + k * -8, ex_ + 5, ey_ + 2 + k * -8, ex_ + 14, ey_ + 2)
            st(ctx, OUTL, 5.5)
            continue
        if ew > 0.5:
            rx, ry = 17 * min(eo, 1.15), 20 * eo
            ell(ctx, ex_, ey_, rx, ry); fs(ctx, (1, 1, 1), 4)
            px, py = ex_ + look * 6, ey_ + lookY * 6
            ell(ctx, px, py, 8.5, 10.5); ctx.set_source_rgb(*C(eyc)); ctx.fill()
            ell(ctx, px + 3, py - 4, 3.2, 3.2); ctx.set_source_rgb(1, 1, 1); ctx.fill()
        else:
            rx, ry = 11.5, max(3.5, 14 * eo)
            ell(ctx, ex_ + look * 3, ey_ + lookY * 4, rx, ry); ctx.set_source_rgb(*C(eyc)); ctx.fill()
            if ry > 8 or P.get("glint"):
                ell(ctx, ex_ + look * 3 + 4, ey_ + lookY * 4 - min(4, ry * 0.4), 3.6, 3.6); ctx.set_source_rgb(1, 1, 1); ctx.fill()
            if F["tear"] > 0.2:   # watery shine
                ell(ctx, ex_ + look * 3 - 3, ey_ + lookY * 4 + ry * 0.45, 4, 2.2); ctx.set_source_rgba(0.75, 0.9, 1, 0.9); ctx.fill()
        lid = F["lid"]
        if lid > 0.05:
            ctx.save(); ell(ctx, ex_, ey_, 21, 23); ctx.clip()
            ytop = ey_ - 24 + lid * 26
            ctx.move_to(ex_ - 24, ey_ - 30); ctx.line_to(ex_ + 24, ey_ - 30); ctx.line_to(ex_ + 24, ytop - sx * 3 * lid)
            ctx.line_to(ex_ - 24, ytop + sx * 3 * lid); ctx.close_path(); ctx.set_source_rgb(*C(ch["skin"])); ctx.fill()
            ctx.restore()
            ctx.move_to(ex_ - 17, ytop + sx * 3 * lid); ctx.line_to(ex_ + 17, ytop - sx * 3 * lid); st(ctx, OUTL, 4)
        if F["tear"] > 0.05 and not blink:
            L = 55 * F["tear"]
            ctx.move_to(ex_ - 2, ey_ + 14); ctx.curve_to(ex_ - 8, ey_ + 14 + L * 0.5, ex_ - 2, ey_ + 14 + L * 0.8, ex_ - 6, ey_ + 14 + L)
            ctx.set_source_rgba(0.6, 0.85, 1.0, 0.75); ctx.set_line_width(7); ctx.stroke()
            dy = ((t * 0.9 + sx * 0.37) % 1.0) * 70
            if F["tear"] > 0.6:
                d_ = ey_ + 20 + dy
                ctx.move_to(ex_ - 6, d_ - 10); ctx.curve_to(ex_ - 14, d_ + 2, ex_ - 10, d_ + 9, ex_ - 6, d_ + 9)
                ctx.curve_to(ex_ - 2, d_ + 9, ex_ + 2, d_ + 2, ex_ - 6, d_ - 10)
                ctx.set_source_rgba(0.6, 0.85, 1.0, 0.9 * (1 - dy / 70)); ctx.fill()
    if P.get("glasses"):
        for sx in (-1, 1):
            rrect(ctx, fx + sx * 34 - 26, fy - 18, 52, 40, 12); st(ctx, (0.25, 0.15, 0.1), 5)
        ctx.move_to(fx - 8, fy - 4); ctx.line_to(fx + 8, fy - 4); st(ctx, (0.25, 0.15, 0.1), 5)
    ctx.move_to(fx - 7, fy + 26); ctx.curve_to(fx - 2, fy + 36, fx + 6, fy + 36, fx + 9, fy + 27)
    st(ctx, shade(ch["skin"], 0.3), 5)
    mx, my = fx + look * 3, fy + 62
    if ch.get("mustache"):
        for sx in (-1, 1):
            ctx.move_to(fx, fy + 42); ctx.curve_to(fx + sx * 20, fy + 36, fx + sx * 42, fy + 44, fx + sx * 44, fy + 58)
            ctx.curve_to(fx + sx * 26, fy + 54, fx + sx * 10, fy + 54, fx, fy + 50); ctx.close_path()
            fs(ctx, ch["hair"], 3.5)
        my += 6
    if ch.get("beard"):
        ctx.move_to(fx - 88, fy + 10); ctx.curve_to(fx - 80, fy + 110, fx + 80, fy + 110, fx + 88, fy + 10)
        ctx.curve_to(fx + 60, fy + 60, fx + 30, fy + 50, fx, fy + 52); ctx.curve_to(fx - 30, fy + 50, fx - 60, fy + 60, fx - 88, fy + 10)
        ctx.close_path(); fs(ctx, ch["hair"], 4)
    sm_ = F["smile"]; trem = F["tremble"]
    op = F["mo"] + m
    mouthc = (0.42, 0.11, 0.14)
    if F.get("teeth"):
        w = 30 + 6 * m; h = 18 + 22 * min(1, op)
        rrect(ctx, mx - w, my - h / 2, 2 * w, h, 7); fs(ctx, (1, 1, 1), 4.5)
        ctx.move_to(mx - w + 3, my); ctx.line_to(mx + w - 3, my)
        for k in range(1, 5): ctx.move_to(mx - w + k * 2 * w / 5, my - h / 2 + 2); ctx.line_to(mx - w + k * 2 * w / 5, my + h / 2 - 2)
        st(ctx, OUTL, 3)
    elif op > 0.08:
        w = 17 + 8 * max(0, sm_) + m * 5
        h = 4 + op * 16
        ctx.move_to(mx - w, my + 2 - 4 * sm_)
        ctx.curve_to(mx - w * 0.6, my + 2 - h * 0.5 * (1 - max(0, sm_)), mx + w * 0.6, my + 2 - h * 0.5 * (1 - max(0, sm_)), mx + w, my + 2 - 4 * sm_)
        ctx.curve_to(mx + w * 0.7, my + 4 + h * 1.4, mx - w * 0.7, my + 4 + h * 1.4, mx - w, my + 2 - 4 * sm_)
        ctx.close_path(); fs(ctx, mouthc, 4)
        if sm_ > 0.5:
            ctx.save(); ctx.move_to(mx - w, my + 2 - 4 * sm_); ctx.curve_to(mx - w * 0.7, my + 4 + h * 1.4, mx + w * 0.7, my + 4 + h * 1.4, mx + w, my + 2 - 4 * sm_)
            ctx.close_path(); ctx.clip(); ctx.rectangle(mx - w, my - 10, 2 * w, 9); ctx.set_source_rgb(1, 1, 1); ctx.fill(); ctx.restore()
        if op > 0.35:
            ell(ctx, mx, my + 2 + h * 0.75, w * 0.45, h * 0.25); ctx.set_source_rgba(0.85, 0.4, 0.45, 0.9); ctx.fill()
    elif F["smirk"] > 0.5:
        ctx.move_to(mx - 20, my + 4); ctx.curve_to(mx - 6, my + 9, mx + 10, my + 5, mx + 24, my - 8); st(ctx, OUTL, 5.5)
    elif sm_ > 0.6:
        ctx.move_to(mx - 28, my - 6); ctx.curve_to(mx - 14, my + 22, mx + 14, my + 22, mx + 28, my - 6); ctx.close_path()
        fs(ctx, mouthc, 4.5)
        ctx.save(); ctx.move_to(mx - 28, my - 6); ctx.curve_to(mx - 14, my + 22, mx + 14, my + 22, mx + 28, my - 6)
        ctx.close_path(); ctx.clip(); ctx.rectangle(mx - 30, my - 8, 60, 9); ctx.set_source_rgb(1, 1, 1); ctx.fill(); ctx.restore()
    else:
        w = 17 + 5 * abs(sm_)
        q = trem * 2.5 * sin(t * 33)
        ctx.move_to(mx - w, my + 4 - sm_ * 7)
        ctx.curve_to(mx - w * 0.35, my + 4 + sm_ * 9 + q, mx + w * 0.35, my + 4 + sm_ * 9 - q, mx + w, my + 4 - sm_ * 7)
        st(ctx, OUTL, 5.5)
        if sm_ < -0.6:  # quivering chin line
            ctx.move_to(mx - 8, my + 22); ctx.curve_to(mx - 3, my + 26 + q, mx + 3, my + 26 - q, mx + 8, my + 22); st(ctx, shade(ch["skin"], 0.25), 3)
    return fx, fy


def draw_brows(ctx, ch, P, F, fx, fy):
    ew = F["ew"]
    bc = shade(ch["hair"], 0.25) if ch.get("hairstyle") != "bob" else shade(ch["hair"], 0.45)
    for sx in (-1, 1):
        bx, by = fx + sx * 34, fy - 36 - (8 if ew > 0.5 else 0)
        bi, bo = F["bi"], F["bo"]
        if F["smirk"] > 0.5 and sx == 1: bi, bo = -6, -12
        ctx.move_to(bx - sx * 15, by + bi); ctx.line_to(bx + sx * 15, by + bo)
        st(ctx, bc, 7.5 + 2 * clamp(bi / 14))
        if bi > 9:   # anger crease
            ctx.move_to(fx - 6, fy - 30); ctx.line_to(fx - 3, fy - 20); ctx.move_to(fx + 6, fy - 30); ctx.line_to(fx + 3, fy - 20)
            st(ctx, shade(ch["skin"], 0.3), 3.5)


def draw_sweat(ctx, P, t, hx, hy):
    if P.get("sweat"):
        sx_, sy_ = hx + 70, hy - 50 + ((t * 0.6) % 1) * 30
        ctx.move_to(sx_, sy_ - 14); ctx.curve_to(sx_ - 10, sy_, sx_ - 7, sy_ + 10, sx_, sy_ + 10)
        ctx.curve_to(sx_ + 7, sy_ + 10, sx_ + 10, sy_, sx_, sy_ - 14); fs(ctx, (0.7, 0.9, 1.0), 3)


def draw_char(ctx, ch, P, t):
    """P keys: x,y,s, mood, mouth, look, lookY, armL/armR specs, legs, hat, shadow, dark, tear, sleeve_pull"""
    s = P.get("s", 1.0)
    DARK[0] = P.get("dark", 0.0)
    F = dict(MOODS["neutral"]); F.update(MOODS.get(P.get("mood", "neutral"), {}) if isinstance(P.get("mood", "neutral"), str) else P["mood"])
    F.update(P.get("face", {}))
    m = P.get("mouth", 0.0)
    trem = F.get("tremble", 0) + P.get("tremble", 0)
    jx = trem * 2.2 * sin(t * 47 + ch.get("seed", 0)) + P.get("shake", 0) * 9 * sin(t * 60)
    ctx.save(); ctx.translate(P["x"] + jx * s, P["y"] + P.get("flinch", 0) * 14 * s); ctx.scale(s, s * (1 - 0.03 * P.get("flinch", 0)))
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    b = 1 + 0.012 * sin(t * 2.2 + ch.get("seed", 0))
    look, lookY = P.get("look", 0.0), P.get("lookY", 0.0)
    if P.get("saccade", True) and not P.get("blink"):
        k = math.floor(t / 1.25 + ch.get("seed", 0) * 0.37)
        look += 0.13 * math.sin(k * 12.9898 + ch.get("seed", 0)); lookY += 0.08 * math.sin(k * 78.233)
    talking = min(1.0, m * 3)
    tilt = P.get("tilt", 0.0) + F.get("tilt", 0) + talking * 0.035 * sin(t * 6.3 + ch.get("seed", 0)) + 0.012 * sin(t * 1.1 + ch.get("seed", 0))
    hx, hy = look * 6, -340 * b + talking * 3 * sin(t * 9)
    ctx.save(); ctx.translate(0, -258 * b); ctx.rotate(tilt); ctx.translate(0, 258 * b)
    back_hair(ctx, ch, hx, hy)
    ctx.restore()
    if P.get("legs"): legs(ctx, ch, b)
    rrect(ctx, -21, -268 * b, 42, 46, 10); fs(ctx, shade(ch["skin"], 0.12))
    torso_path(ctx, b, ch.get("wide", 1.0)); fs(ctx, ch["top"])
    outfit(ctx, ch, b, P)
    sy = SH_Y * b
    if "sleeve_pull" in P:  # right arm across body, left hand pulling sleeve down over wrist
        u = P["sleeve_pull"]
        sx_, ex, ey, hx2, hy2 = -SH_X, -118, -64 * b, 58, -128 * b
        ctx.move_to(ex, ey); ctx.line_to(hx2, hy2); st(ctx, OUTL, AW * 0.7 + 2 * LW)
        ctx.move_to(ex, ey); ctx.line_to(hx2, hy2); st(ctx, ch["skin"], AW * 0.7)
        bx, by = lerp(ex, hx2, 0.74), lerp(ey, hy2, 0.74)
        ell(ctx, bx, by, 15, 10, -0.35); ctx.set_source_rgba(*C((0.42, 0.28, 0.55)), 0.7); ctx.fill()
        ell(ctx, bx + 3, by, 8, 6, -0.35); ctx.set_source_rgba(*C((0.35, 0.2, 0.45)), 0.6); ctx.fill()
        ell(ctx, hx2, hy2, 22, 22); fs(ctx, ch["skin"])
        f = lerp(0.42, 0.93, u)
        cx_, cy_ = lerp(ex, hx2, f), lerp(ey, hy2, f)
        ctx.move_to(sx_, sy); ctx.line_to(ex, ey); ctx.line_to(cx_, cy_); st(ctx, OUTL, AW + 2 * LW)
        ctx.move_to(sx_, sy); ctx.line_to(ex, ey); ctx.line_to(cx_, cy_); st(ctx, ch.get("sleeve", ch["top"]), AW)
        draw_arm(ctx, ch, SH_X, sy, ("ik", cx_ + 6, cy_ + 6, -1))
    else:
        draw_arm(ctx, ch, -SH_X, sy, P.get("armL", ("ang", -0.14, -0.05)), ch.get("sleeve_frac", 0.86))
        draw_arm(ctx, ch, SH_X, sy, P.get("armR", ("ang", 0.14, 0.05)), ch.get("sleeve_frac", 0.86))
    # head (tilted around the neck)
    ctx.save(); ctx.translate(0, -258 * b); ctx.rotate(tilt); ctx.translate(0, 258 * b)
    for sx in (-1, 1):
        ell(ctx, hx + sx * 92, hy + 8, 15, 22); fs(ctx, ch["skin"])
    ell(ctx, hx, hy, 95, 102); fs(ctx, ch["skin"])
    sh = P.get("shadow", 0.0)
    if sh > 0:
        ctx.save(); ell(ctx, hx, hy, 93, 100); ctx.clip()
        g = cairo.LinearGradient(0, hy - 110, 0, hy + 70)
        g.add_color_stop_rgba(0, 0.02, 0.02, 0.08, sh); g.add_color_stop_rgba(1, 0.02, 0.02, 0.08, sh * 0.25)
        ctx.set_source(g); ctx.paint(); ctx.restore()
    fx, fy = draw_face(ctx, ch, P, F, t, hx, hy, look, lookY, m)
    front_hair(ctx, ch, hx, hy)
    draw_brows(ctx, ch, P, F, fx, fy)
    draw_sweat(ctx, P, t, hx, hy)
    if P.get("hat"): police_hat(ctx, hx, hy)
    ctx.restore()  # tilt
    ctx.restore()
    DARK[0] = 0.0


def head_world(P):
    s = P.get("s", 1.0)
    return P["x"] + P.get("look", 0) * 6 * s, P["y"] - 340 * s


def local(P, wx, wy):
    s = P.get("s", 1.0)
    return (wx - P["x"]) / s, (wy - P["y"]) / s


# ---------------- props ----------------
def draw_car(ctx, x, y, s, t, lights=True, flip=False, label="POLICE", body=(0.07, 0.07, 0.09), panel=(0.95, 0.95, 0.96), lsize=34):
    ctx.save(); ctx.translate(x, y); ctx.scale(-s if flip else s, s)
    poly(ctx, [(115, -112), (150, -182), (320, -182), (370, -112)]); fs(ctx, body)
    poly(ctx, [(135, -118), (162, -170), (230, -170), (230, -118)]); fs(ctx, (0.2, 0.27, 0.38), 4)
    poly(ctx, [(242, -118), (242, -170), (312, -170), (350, -118)]); fs(ctx, (0.2, 0.27, 0.38), 4)
    rrect(ctx, 0, -125, 470, 92, 30); fs(ctx, body)
    rrect(ctx, 120, -112, 240, 62, 8); fs(ctx, panel, 4)
    ctx.save()
    if flip: ctx.translate(480, 0); ctx.scale(-1, 1)
    text(ctx, label, 240, -70, lsize, col=(0.08, 0.1, 0.2))
    ctx.restore()
    ell(ctx, 462, -95, 10, 12); fs(ctx, (1, 0.95, 0.7), 3)
    ell(ctx, 8, -95, 8, 12); fs(ctx, (0.9, 0.1, 0.1), 3)
    for wx in (95, 375):
        ell(ctx, wx, -30, 40, 40); fs(ctx, (0.04, 0.04, 0.05)); ell(ctx, wx, -30, 18, 18); fs(ctx, (0.6, 0.6, 0.65), 3)
    ph = (t * 2.4) % 1.0
    red_on, blue_on = ph < 0.5, ph >= 0.5
    rrect(ctx, 186, -200, 46, 18, 5); fs(ctx, (1, 0.15, 0.15) if red_on else (0.45, 0.08, 0.08), 3.5)
    rrect(ctx, 234, -200, 46, 18, 5); fs(ctx, (0.25, 0.45, 1) if blue_on else (0.08, 0.12, 0.4), 3.5)
    ctx.restore()
    return red_on


def vignette(ctx, a, inner=480, outer=1250):
    g = cairo.RadialGradient(W / 2, H / 2, inner, W / 2, H / 2, outer)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, a)
    ctx.set_source(g); ctx.paint()


def overlay(ctx, col, a, op=cairo.OPERATOR_OVER):
    ctx.save(); ctx.set_operator(op); ctx.set_source_rgba(*col, a); ctx.paint(); ctx.restore()


def cam(keys, t):
    k0 = keys[0]
    for k in keys[1:]:
        if t < k[0]:
            if len(k) > 4 and k[4] == "cut": return k0[1:4]
            u = sm((t - k0[0]) / max(1e-6, k[0] - k0[0]))
            return tuple(lerp(a, b, u) for a, b in zip(k0[1:4], k[1:4]))
        k0 = k
    return k0[1:4]


def apply_cam(ctx, cx, cy, z, ww=W, wh=H):
    cx = clamp(cx, W / (2 * z), ww - W / (2 * z)); cy = clamp(cy, H / (2 * z), wh - H / (2 * z))
    ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-cx, -cy)
