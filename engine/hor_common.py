# exec'd inside dna.py globals for the horror series
YOU = dict(skin=(0.90, 0.72, 0.58), hair=(0.22, 0.15, 0.10), hairstyle="crew", outfit="hoodie", top=(0.32, 0.34, 0.42), seed=91, pants=(0.2, 0.2, 0.25))
LANDLORD = dict(skin=(0.88, 0.70, 0.58), hair=(0.80, 0.80, 0.82), hairstyle="crew", outfit="cardigan", top=(0.45, 0.40, 0.32), no_lanyard=True, seed=92, beard=True)
RED = (0.92, 0.12, 0.12)
COLS_EXTRA = ({"N": (1, 1, 1), "MOM": (1, 0.65, 0.8), "WH": (1, 0.2, 0.2), "LL": (1, 0.86, 0.15), "NB": (0.8, 0.7, 1.0)})

DOOR = (390, 560, 300, 740)   # x, y, w, h of the front door in the entry set


def entry(ctx, day=False):
    wall = (0.80, 0.76, 0.68) if day else (0.17, 0.17, 0.23)
    room(ctx, back=(220, 420, 640, 880), wall=wall, floor=shade(wall, 0.35), ceil=shade(wall, 0.1), side=shade(wall, 0.12), plank=True)
    x, y, w, h = DOOR
    ctx.rectangle(x - 22, y - 22, w + 44, h + 22); fs(ctx, shade(wall, -0.15) if day else (0.26, 0.24, 0.28), 6)   # frame
    for k, yy in enumerate((700, 760, 820)):
        ell(ctx, 280, yy - 60 * k + 120, 14, 14); fs(ctx, (0.6, 0.55, 0.45), 3)
    rrect(ctx, 240, 760, 70, 220, 20); fs(ctx, (0.35, 0.40, 0.55) if day else (0.15, 0.17, 0.25), 5)   # coat
    ctx.rectangle(730, 1140, 120, 160); fs(ctx, (0.40, 0.30, 0.22) if day else (0.16, 0.13, 0.12), 5)   # small cabinet
    rrect(ctx, 750, 780, 34, 54, 6); fs(ctx, (0.9, 0.9, 0.88) if day else (0.35, 0.35, 0.38), 3)   # switch
    if not day: vignette(ctx, 0.45)


def entry_day(ctx): entry(ctx, True)


def draw_door(ctx, open_=0.0, sh=(0, 0), chain=0.0, chain_fall=False, knob=0.0, under=0.6, feet=0.0, scratches=0.0, day=False, red=0.0):
    x, y, w, h = DOOR
    ctx.save(); ctx.translate(*sh)
    gap = w * open_
    ctx.rectangle(x, y, w, h); ctx.set_source_rgb(0.02, 0.02, 0.03); ctx.fill()
    if under > 0 and open_ < 0.02:
        ctx.rectangle(x + 6, y + h - 8, w - 12, 8); ctx.set_source_rgba(1, 0.92, 0.7, under); ctx.fill()
        glow(ctx, x + w / 2, y + h + 10, 260, (1, 0.85, 0.55), 0.25 * under)
        if feet > 0:
            for fx_ in (x + w * 0.36, x + w * 0.62):
                ctx.rectangle(fx_ - 30, y + h - 8, 60, 8); ctx.set_source_rgba(0, 0, 0, feet); ctx.fill()
                poly(ctx, [(fx_ - 30, y + h), (fx_ + 30, y + h), (fx_ + 120, y + h + 200), (fx_ + 20, y + h + 200)]); ctx.set_source_rgba(0, 0, 0, 0.5 * feet); ctx.fill()
    if open_ > 0.01:
        ctx.rectangle(x, y, gap, h); ctx.set_source_rgb(0.08, 0.07, 0.05); ctx.fill()
        glow(ctx, x + gap / 2, y + h / 2, 200, (1, 0.8, 0.5), 0.3 * flick(CUR["t"]))
    dx0 = x + gap
    col = (0.55, 0.42, 0.32) if day else (0.30, 0.22, 0.18)
    ctx.rectangle(dx0, y, w - gap * 0.85, h); fs(ctx, col, 6)
    pw = w - gap * 0.85
    for (py, ph) in ((y + 50, 260), (y + 360, 320)):
        ctx.rectangle(dx0 + pw * 0.14, py, pw * 0.72, ph); st(ctx, shade(col, 0.2), 5)
    ell(ctx, dx0 + pw / 2, y + 150, 11, 11); fs(ctx, (0.05, 0.05, 0.05), 3)   # peephole
    kx, ky = dx0 + pw * 0.82, y + 400
    ell(ctx, kx, ky, 26, 26); fs(ctx, (0.75, 0.65, 0.35), 4)
    ctx.save(); ctx.translate(kx, ky); ctx.rotate(knob); rrect(ctx, -36, -9, 50, 18, 8); fs(ctx, (0.75, 0.65, 0.35), 4); ctx.restore()
    # chain from frame (right) to door
    if not chain_fall:
        ax, ay = x + w + 14, y + 300; bx_, by_ = dx0 + pw * 0.86 - 120 * chain, y + 300
        rrect(ctx, ax - 14, ay - 30, 22, 60, 6); fs(ctx, (0.7, 0.7, 0.72), 3)
        n = 9
        for k in range(n):
            u = k / (n - 1); cx_ = lerp(ax, bx_, u); cy_ = ay + 45 * sin(u * pi) * (1 - chain * 0.6)
            ell(ctx, cx_, cy_, 9, 6); st(ctx, (0.75, 0.75, 0.78), 4)
    else:
        for k in range(7): ell(ctx, x + w + 10, y + 320 + k * 16, 6, 9); st(ctx, (0.75, 0.75, 0.78), 4)
    if scratches > 0:
        rs = random.Random(3)
        for k in range(5):
            sx = dx0 + 60 + k * 45 + rs.uniform(-10, 10); L_ = h * 0.8 * clamp(scratches * 1.4 - k * 0.12)
            if L_ <= 0: continue
            ctx.move_to(sx, y + 120); ctx.curve_to(sx + 10, y + 120 + L_ * 0.3, sx - 10, y + 120 + L_ * 0.6, sx + 5, y + 120 + L_)
            st(ctx, (0.85, 0.75, 0.62), 5)
    if red: ctx.rectangle(x, y, w, h); ctx.set_source_rgba(0.8, 0.05, 0.05, red); ctx.fill()
    ctx.restore()


def flick(t, seed=0):
    v = sin(t * 37 + seed) * sin(t * 13.3 + seed * 2) + 0.3 * sin(t * 71)
    return 1.0 if v > -0.35 else 0.15


def kitchen_h(ctx):
    room(ctx, back=(150, 520, 780, 640), wall=(0.20, 0.21, 0.26), floor=(0.16, 0.13, 0.12), ceil=(0.10, 0.10, 0.14), side=(0.17, 0.18, 0.22))
    for x in range(170, 900, 130): rrect(ctx, x, 560, 115, 170, 8); fs(ctx, (0.22, 0.27, 0.30), 5)
    ctx.rectangle(150, 900, 780, 260); fs(ctx, (0.22, 0.27, 0.30), 5); ctx.rectangle(140, 880, 800, 30); fs(ctx, (0.35, 0.35, 0.36), 4)
    for x in range(200, 900, 170): rrect(ctx, x, 960, 140, 24, 8); fs(ctx, (0.30, 0.34, 0.38), 3)
    ctx.rectangle(470, 700, 160, 150); fs(ctx, (0.10, 0.12, 0.28), 6); ell(ctx, 590, 740, 18, 18); ctx.set_source_rgb(0.9, 0.9, 0.85); ctx.fill()
    poly(ctx, [(930, 560), (1180, 420), (1180, 1480), (930, 1160)]); fs(ctx, (0.40, 0.42, 0.45), 6)
    glow(ctx, 550, 780, 300, (0.4, 0.5, 1), 0.25); vignette(ctx, 0.5)


def corridor(ctx, lit=True, day=False, sign9b=False):
    wall = (0.62, 0.62, 0.50) if lit else (0.10, 0.11, 0.10)
    room(ctx, back=(400, 600, 280, 560), wall=wall, floor=shade(wall, 0.35), ceil=shade(wall, 0.15), side=shade(wall, 0.12), plank=False)
    # elevator at the end
    ctx.rectangle(450, 760, 180, 400); fs(ctx, (0.55, 0.57, 0.60) if lit else (0.12, 0.12, 0.13), 5)
    ctx.move_to(540, 760); ctx.line_to(540, 1160); st(ctx, OUTL, 4)
    rrect(ctx, 500, 700, 80, 40, 6); fs(ctx, (0.1, 0.1, 0.1), 3); text(ctx, "9", 540, 730, 28, col=(1, 0.5, 0.2))
    side_door(ctx, 120, 300, 470, 640, 1500, 1260, col=(0.40, 0.30, 0.25) if lit else (0.08, 0.07, 0.07))
    side_door(ctx, 780, 960, 640, 470, 1260, 1500, col=(0.40, 0.30, 0.25) if lit else (0.08, 0.07, 0.07))
    for x, n in ((210, "9A"), (870, "9B")):
        rrect(ctx, x - 45, 380, 90, 50, 8); fs(ctx, (0.9, 0.85, 0.6) if lit else (0.2, 0.2, 0.18), 3); text(ctx, n, x, 418, 32, col=(0.2, 0.2, 0.2))
    if sign9b:
        ctx.save(); ctx.translate(870, 900); ctx.rotate(0.08); ctx.rectangle(-70, -45, 140, 90); fs(ctx, (1, 1, 1), 4)
        text(ctx, "EMPTY", 0, 10, 30, col=(0.85, 0.1, 0.1)); ctx.restore()
        ctx.move_to(800, 700); ctx.line_to(940, 1100); ctx.move_to(940, 700); ctx.line_to(800, 1100); st(ctx, (0.9, 0.8, 0.2), 10)
    for k, y in enumerate((240, 420, 530)):
        w_ = 260 - 70 * k
        ctx.rectangle(540 - w_ / 2, y, w_, 22 - 5 * k); ctx.set_source_rgb(*((1, 1, 0.9) if lit else (0.2, 0.2, 0.2))); ctx.fill()
        if lit: glow(ctx, 540, y + 40, 300 - 60 * k, (0.9, 1, 0.8), 0.25)
    if not day: vignette(ctx, 0.5 if lit else 0.7)


def corridor_dark(ctx): corridor(ctx, False)
def corridor_9b(ctx): corridor(ctx, True, True, True)


def bedroom_h(ctx):
    bedroom_night(ctx); overlay(ctx, (0, 0, 0.05), 0.35)


def living_h(ctx):
    room(ctx, back=(180, 520, 720, 640), wall=(0.14, 0.15, 0.22), floor=(0.12, 0.10, 0.10), ceil=(0.08, 0.08, 0.12), side=(0.12, 0.13, 0.19))
    rrect(ctx, 100, 1150, 880, 260, 50); fs(ctx, (0.18, 0.20, 0.28), 6)   # couch back (camera behind couch)
    ctx.rectangle(330, 1100, 420, 40); fs(ctx, (0.10, 0.10, 0.12), 4)
    vignette(ctx, 0.5)


def building_ext(ctx):
    g = cairo.LinearGradient(0, 0, 0, 1400); g.add_color_stop_rgb(0, 0.02, 0.02, 0.08); g.add_color_stop_rgb(1, 0.10, 0.10, 0.22); ctx.set_source(g); ctx.paint()
    ell(ctx, 860, 300, 60, 60); ctx.set_source_rgb(0.95, 0.95, 0.85); ctx.fill(); glow(ctx, 860, 300, 260, (0.8, 0.8, 1), 0.25)
    ctx.rectangle(260, 260, 560, 1700); fs(ctx, (0.16, 0.16, 0.20), 5)
    for r in range(10):
        for c in range(4):
            lit = (r == 1 and c == 2)
            ctx.rectangle(300 + c * 130, 320 + r * 150, 80, 90); ctx.set_source_rgb(*((1, 0.85, 0.5) if lit else (0.07, 0.07, 0.10))); ctx.fill()
            if lit: glow(ctx, 340 + c * 130, 365 + r * 150, 160, (1, 0.8, 0.4), 0.5)


SETS.update({"entry": entry, "entry_day": entry_day, "kitchen_h": kitchen_h, "corridor": corridor, "corridor_dark": corridor_dark,
             "corridor_9b": corridor_9b, "bedroom_h": bedroom_h, "living_h": living_h, "building_ext": building_ext})


def corridor_into(ctx, x, y, w, h, lit=True, name=None, figure=0.0, fig_s=1.0, zoom=1.0):
    ctx.save(); ctx.rectangle(x, y, w, h); ctx.clip()
    ctx.translate(x + w / 2, y + h / 2); s = w / 1080 * zoom; ctx.scale(s, s); ctx.translate(-540, -1000)
    BG(ctx, name or ("corridor" if lit else "corridor_dark"), 0)
    if figure > 0: shadow_figure(ctx, 560, 1260, 1.1 * fig_s, figure)
    ctx.restore()


def shadow_figure(ctx, x, y, s, a=1.0, eyes=True):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.push_group()
    ell(ctx, 0, -760, 46, 70); ctx.set_source_rgb(0, 0, 0); ctx.fill()
    ctx.move_to(-14, -700); ctx.line_to(14, -700); ctx.line_to(40, -600); ctx.line_to(-40, -600); ctx.close_path(); ctx.fill()
    ctx.move_to(-70, -610); ctx.curve_to(-80, -400, -55, -200, -40, 0); ctx.line_to(40, 0); ctx.curve_to(55, -200, 80, -400, 70, -610); ctx.close_path(); ctx.fill()
    for sx in (-1, 1):
        ctx.move_to(sx * 66, -600); ctx.curve_to(sx * 110, -420, sx * 120, -250, sx * 110, -120); st(ctx, (0, 0, 0), 18)
        for f_ in range(3): ctx.move_to(sx * 110, -120); ctx.line_to(sx * (100 + f_ * 12), -60); st(ctx, (0, 0, 0), 6)
    if eyes:
        for sx in (-1, 1): ell(ctx, sx * 16, -770, 7, 4); ctx.set_source_rgb(0.95, 0.95, 0.9); ctx.fill()
    ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    ctx.restore()


def cam_feed(ctx, x, y, w, h, lt, lit=True, figure=0.0, fig_s=1.0, label_="CAM 1  HALLWAY", ts="03:07", zoom=1.0, person=None):
    ctx.save(); ctx.rectangle(x, y, w, h); ctx.clip()
    corridor_into(ctx, x, y, w, h, lit, figure=figure, fig_s=fig_s, zoom=zoom)
    if person:
        ctx.save(); ctx.translate(x + w / 2, y + h / 2); s = w / 1080 * zoom; ctx.scale(s, s); ctx.translate(-540, -1000)
        person(ctx); ctx.restore()
    ctx.set_operator(cairo.OPERATOR_HSL_COLOR); ctx.set_source_rgb(0.35, 0.8, 0.45); ctx.paint(); ctx.set_operator(cairo.OPERATOR_OVER)
    for k in range(0, int(h), 6): ctx.rectangle(x, y + k, w, 2); ctx.set_source_rgba(0, 0, 0, 0.18); ctx.fill()
    ctx.restore()
    sz = max(16, w / 26)
    text(ctx, label_, x + 20, y + 20 + sz, sz, col=(1, 1, 1), align="l")
    text(ctx, f"{ts}:{int(lt * 7) % 60:02d}", x + w - 20, y + 20 + sz, sz, col=(1, 1, 1), align="r")
    if int(lt * 2) % 2 == 0: ell(ctx, x + 30, y + h - 30, sz * 0.4, sz * 0.4); ctx.set_source_rgb(1, 0.1, 0.1); ctx.fill()
    text(ctx, "REC", x + 50, y + h - 30 + sz * 0.35, sz, col=(1, 1, 1), align="l")


def peephole(lit=True, figure=0.0, name=None, zoom=1.0, lab=None):
    def f(ctx, lt, d):
        ctx.set_source_rgb(0, 0, 0); ctx.paint()
        r = 430 * (1 + 0.04 * sm(lt / d))
        ctx.save(); ell(ctx, 540, 900, r, r); ctx.clip()
        ctx.translate(540, 900); z = 1.3 * zoom * (1 + 0.05 * sm(lt / d)); ctx.scale(z, z); ctx.translate(-540, -1000)
        BG(ctx, name or ("corridor" if lit else "corridor_dark"), 0)
        if figure: shadow_figure(ctx, 540, 1250, 1.1, figure)
        ctx.restore()
        g = cairo.RadialGradient(540, 900, r * 0.55, 540, 900, r); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.95)
        ctx.set_source(g); ell(ctx, 540, 900, r, r); ctx.fill()
        ell(ctx, 540, 900, r, r); st(ctx, (0.15, 0.12, 0.1), 30)
        if lab: label(ctx, lt, 0.3, lab, 540, 1560, 80, -0.05, RED)
    return f


def clock_ins(times):
    """times: list of (t0, 'H:MM') shown in sequence"""
    def f(ctx, lt, d):
        ctx.set_source_rgb(0.02, 0.02, 0.04); ctx.paint()
        cur = times[0][1]
        for t0, s_ in times:
            if lt >= t0: cur = s_
        ctx.save(); cam(ctx, 1.0 + 0.15 * sm(lt / d), 540, 960)
        poly(ctx, [(170, 760), (910, 760), (960, 1200), (120, 1200)]); fs(ctx, (0.08, 0.08, 0.10), 8)
        rrect(ctx, 210, 820, 660, 320, 24); ctx.set_source_rgb(0.01, 0.0, 0.0); ctx.fill()
        glow(ctx, 540, 980, 520, (1, 0.1, 0.05), 0.4)
        h_, m_ = cur.split(":")
        text(ctx, h_, 340, 1065, 200, col=(1, 0.12, 0.08)); text(ctx, m_, 640, 1065, 200, col=(1, 0.12, 0.08))
        for yy in (940, 1020): ell(ctx, 455, yy, 14, 14); ctx.set_source_rgba(1, 0.12, 0.08, 1.0 if (lt % 1) < 0.5 else 0.3); ctx.fill()
        text(ctx, "AM", 820, 1110, 40, col=(1, 0.3, 0.25))
        ctx.restore()
    return f


def knock_door(feet=0.0, words=(0.1, 0.45, 0.8), z=(1.0, 1.1), under=0.7, red=0.0, scratches=0.0, chain=0.0, open_=0.0, post=None, figure_gap=0.0):
    def f(ctx, lt, d):
        sh = (0, 0)
        for w0 in words:
            if w0 <= lt < w0 + 0.15: sh = shake(lt, 10)
        ctx.save(); cam(ctx, punch(lt, 0.03) * lerp(z[0], z[1], sm(lt / d)), 540, 930, dx=sh[0] * 0.5, dy=0)
        BG(ctx, "entry", 0)
        sc_ = scratches(lt, d) if callable(scratches) else scratches
        ch_ = chain(lt, d) if callable(chain) else chain
        op_ = open_(lt, d) if callable(open_) else open_
        draw_door(ctx, open_=op_, sh=sh, under=under * flick(CUR["t"], 3), feet=feet, scratches=sc_, chain=ch_, red=red)
        if figure_gap and op_ > 0.02:
            x, y, w, h = DOOR
            ctx.save(); ctx.rectangle(x, y, w * op_, h); ctx.clip()
            for sx in (-1, 1): ell(ctx, x + w * op_ / 2 + sx * 10, y + 220, 6, 4); ctx.set_source_rgb(1, 1, 0.9); ctx.fill()
            ctx.restore()
        ctx.restore()
        for w0 in words:
            pop_word(ctx, lt, w0, "KNOCK", 540 + 220 * sin(w0 * 7), 520 + 120 * cos(w0 * 5), 100, col=(1, 1, 1), rot=-0.12 + 0.24 * ((w0 * 10) % 2 > 1), life=0.4)
        if post: post(ctx, lt, d)
    return f


def note(ctx, lines, hl=None, torn=True, rot=-0.03, scrap=False):
    ctx.save(); ctx.rotate(rot)
    w, h = (700, 360) if scrap else (760, 1000)
    pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2)]
    if torn:
        for k in range(12): pts.append((w / 2 - (k + 1) * w / 12, h / 2 + (18 if k % 2 else -14)))
    else: pts.append((-w / 2, h / 2))
    poly(ctx, pts); fs(ctx, (0.96, 0.86, 0.45), 5)
    for k in range(int(h / 70)): ctx.move_to(-w / 2 + 30, -h / 2 + 90 + k * 70); ctx.line_to(w / 2 - 30, -h / 2 + 90 + k * 70); st(ctx, (0.75, 0.65, 0.35), 2)
    ctx.select_font_face("Poppins", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_BOLD)
    y = -h / 2 + 80
    for i, ln in enumerate(lines):
        ctx.set_font_size(40); ctx.move_to(-w / 2 + 40, y)
        ctx.set_source_rgb(*((0.80, 0.08, 0.08) if hl == i else (0.15, 0.12, 0.25))); ctx.show_text(ln); y += 70
    ctx.restore()


NOTE1 = ["If it knocks at 3:07 -", "1. NEVER open the door.", "   It can't come in unless", "   you let it.", "2. It knows the voices you", "   love. DO NOT answer.", "3. It will try to make yo"]


def note_ins(lines=NOTE1, hl=None, z=(1.0, 1.12), cy=960, scrap=False, lab=None, rot=-0.03, lab_y=560):
    def f(ctx, lt, d):
        ctx.save(); cam(ctx, punch(lt, 0.04) * lerp(z[0], z[1], sm(lt / d)), 540, cy)
        BG(ctx, "kitchen_h", 18); overlay(ctx, (0, 0, 0), 0.3)
        glow(ctx, 540, 960, 600, (1, 0.9, 0.6), 0.2)
        ctx.translate(540, 960); note(ctx, lines, hl(lt) if callable(hl) else hl, scrap=scrap, rot=rot)
        ctx.restore()
        if lab: label(ctx, lt, 0.2, lab, 540, lab_y, 80, -0.05, RED)
    return f


def rule_card(num, txt, sub=None):
    def f(ctx, lt, d):
        ctx.set_source_rgb(0.02, 0.02, 0.03); ctx.paint()
        glow(ctx, 540, 900, 700, (0.8, 0.05, 0.05), 0.25 + 0.1 * sin(lt * 6))
        p = back_out(clamp(lt / 0.25))
        ctx.save(); ctx.translate(540, 880); ctx.scale(p, p); ctx.rotate(-0.03)
        rrect(ctx, -230, -230, 460, 120, 20); ctx.set_source_rgb(*RED); ctx.fill()
        text(ctx, f"RULE {num}", 0, -150, 70, col=(1, 1, 1))
        rrect(ctx, -430, -80, 860, 300, 24); fs(ctx, (0.08, 0.08, 0.10), 0); rrect(ctx, -430, -80, 860, 300, 24); st(ctx, RED, 8)
        lines = txt.split("|")
        for i, ln in enumerate(lines): text(ctx, ln, 0, -5 + i * 80 + (40 if len(lines) == 1 else 0) + (40 if len(lines) == 2 else 0), 62, col=(1, 1, 1))
        ctx.restore()
        if sub: label(ctx, lt, 0.5, sub, 540, 1220, 56, -0.03, (0.85, 0.85, 0.9))
    return f


def options_card(opts, times, pick=None, pick_t=99, countdown=None):
    def f(ctx, lt, d):
        ctx.set_source_rgb(0.03, 0.03, 0.05); ctx.paint()
        glow(ctx, 540, 900, 700, (0.3, 0.3, 0.6), 0.2)
        text(ctx, "YOUR OPTIONS", 540, 520, 64, col=(1, 1, 1), stroke=10)
        for i, (k, s_) in enumerate(opts):
            if lt < times[i]: continue
            p = back_out(clamp((lt - times[i]) / 0.2)); y = 680 + i * 190
            sel = pick == i and lt >= pick_t
            ctx.save(); ctx.translate(540, y); ctx.scale(p, p)
            rrect(ctx, -420, -70, 840, 140, 24); fs(ctx, (0.15, 0.55, 0.25) if sel else (0.12, 0.12, 0.16), 0)
            rrect(ctx, -420, -70, 840, 140, 24); st(ctx, (0.3, 0.9, 0.4) if sel else (0.5, 0.5, 0.6), 6)
            ell(ctx, -330, 0, 48, 48); ctx.set_source_rgb(*RED); ctx.fill(); text(ctx, k, -330, 22, 56, col=(1, 1, 1))
            text(ctx, s_, -250, 20, 50, col=(1, 1, 1), align="l")
            ctx.restore()
        if countdown:
            for t0, n in countdown:
                pop_word(ctx, lt, t0, n, 540, 1420, 160, col=RED, rot=0, life=0.9)
    return f


def phone_ins(screen, bg="bedroom_h", amp=0, z=(1.0, 1.1), post=None):
    return PHONE(screen, bg=bg, blur=20, amp=amp, z=z, post=post)


def scr_call(ctx, lt, fail_t=99):
    ctx.set_source_rgb(0.12, 0.13, 0.17); ctx.paint()
    for k in range(4):
        ctx.rectangle(-140 + k * 16, -290 - k * 6, 10, 10 + k * 6); ctx.set_source_rgb(*((0.4, 0.4, 0.45) if lt > fail_t else (1, 1, 1))); ctx.fill()
    if lt > fail_t: ctx.move_to(-145, -310); ctx.line_to(-80, -270); st(ctx, RED, 4)
    text(ctx, "911", 0, -120, 80, col=(1, 1, 1))
    text(ctx, "Calling..." if lt < fail_t else "NO SERVICE", 0, -50, 30, col=(0.8, 0.8, 0.85) if lt < fail_t else RED)
    ell(ctx, 0, 200, 50, 50); ctx.set_source_rgb(*RED); ctx.fill()
    ctx.save(); ctx.translate(0, 200); ctx.rotate(2.3); rrect(ctx, -30, -10, 60, 20, 10); ctx.set_source_rgb(1, 1, 1); ctx.fill(); ctx.restore()


def scr_cam(lit=True, figure=0.0, person=None, ts="03:07"):
    def f(ctx, lt):
        ctx.set_source_rgb(0.05, 0.05, 0.07); ctx.paint()
        text(ctx, "DOORBELL", 0, -250, 26, col=(1, 1, 1))
        cam_feed(ctx, -150, -200, 300, 400, lt, lit, figure, person=person, ts=ts)
        text(ctx, "No motion detected" if not person else "Motion detected", 0, 250, 20, col=(0.8, 0.8, 0.85) if not person else RED, weight=False)
    return f


def scr_mom(ctx, lt):
    ctx.rectangle(-160, -310, 320, 70); ctx.set_source_rgb(0.92, 0.92, 0.95); ctx.fill(); text(ctx, "Mom", 0, -265, 24, col=(0.15, 0.15, 0.2))
    text(ctx, "2:57 AM", 0, -205, 16, col=(0.5, 0.5, 0.55), weight=False)
    rrect(ctx, -140, -180, 240, 90, 18); ctx.set_source_rgb(0.88, 0.88, 0.9); ctx.fill()
    text(ctx, "Goodnight sweetie.", -125, -140, 20, col=(0.1, 0.1, 0.12), align="l", weight=False)
    text(ctx, "Love you!", -125, -110, 20, col=(0.1, 0.1, 0.12), align="l", weight=False)
    rrect(ctx, -150, 120, 300, 110, 16); ctx.set_source_rgb(0.95, 0.95, 0.97); ctx.fill()
    text(ctx, "Mom's location", 0, 160, 18, col=(0.4, 0.4, 0.45), weight=False); text(ctx, "800 miles away", 0, 200, 26, col=RED)


def scr_landlord(ctx, lt):
    ctx.set_source_rgb(0.12, 0.13, 0.17); ctx.paint()
    avatar(ctx, LANDLORD, 0, -140, 80)
    text(ctx, "Landlord", 0, 0, 34, col=(1, 1, 1)); text(ctx, f"00:{int(lt) + 12:02d}", 0, 45, 22, col=(0.7, 0.7, 0.75), weight=False)


def hud_bpm_clock(BPM, CLK):
    def hud(ctx, sc, t):
        b0, b1 = BPM.get(sc, (80, 80)); u = t / DUR(sc); bpm = lerp(b0, b1, sm(u))
        clk = CLK(sc, t) if callable(CLK) else CLK.get(sc, "")
        beat = (t * bpm / 60) % 1; pulse = 1 + 0.25 * max(0, 1 - beat * 5)
        if bpm > 105:
            a = 0.35 * max(0, 1 - beat * 3) * (bpm - 105) / 30
            g = cairo.RadialGradient(540, 960, 500, 540, 960, 1150); g.add_color_stop_rgba(0, 0.8, 0, 0, 0); g.add_color_stop_rgba(1, 0.8, 0, 0, a)
            ctx.set_source(g); ctx.paint()
        rrect(ctx, 60, 200, 300, 76, 38); ctx.set_source_rgba(0, 0, 0, 0.55); ctx.fill()
        ctx.save(); ctx.translate(112, 238); ctx.scale(pulse, pulse)
        ctx.move_to(0, 18); ctx.curve_to(-34, -6, -18, -32, 0, -14); ctx.curve_to(18, -32, 34, -6, 0, 18); ctx.set_source_rgb(*RED); ctx.fill(); ctx.restore()
        text(ctx, f"{int(bpm)} BPM", 160, 254, 36, col=(1, 1, 1) if bpm < 105 else (1, 0.4, 0.4), align="l")
        if clk:
            rrect(ctx, 760, 200, 260, 76, 38); ctx.set_source_rgba(0, 0, 0, 0.55); ctx.fill()
            text(ctx, clk, 890, 254, 38, col=(1, 1, 1))
    return hud


def you_ecu(mood, bg="entry", dark=0.25, **kw):
    return ECU(YOU, mood, bg, dark=dark, **kw)


def you_bed(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.06 * sm(lt / d), 540, 1050); BG(ctx, "bedroom_h", 5)
    ell(ctx, 540, 1210, 420, 130); fs(ctx, (0.75, 0.75, 0.82), 6)
    draw_char(ctx, YOU, dict(x=540, y=head_y(1.7, 960), s=1.7, mood=M("worried"), look=0.6, dark=0.35), CUR["t"])
    blanket(ctx, 1290, (0.22, 0.25, 0.42))
    ctx.restore()


def ext_building(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.35 * sm(lt / d), 600, 520); BG(ctx, "building_ext", 0); ctx.restore()
    label(ctx, lt, 0.25, "9th floor", 760, 700, 74, 0.05, (1, 0.86, 0.15))


def tv_scene(on_t=0.3, lit=lambda t: True, figure=lambda lt: 0.0, zoom=1.0, close=False):
    def f(ctx, lt, d):
        ctx.save(); cam(ctx, (1.45 if close else 1.0) * (1 + 0.06 * sm(lt / d)), 540, 860)
        BG(ctx, "living_h", 0)
        x, y, w, h = 250, 640, 580, 400
        rrect(ctx, x - 20, y - 20, w + 40, h + 40, 12); fs(ctx, (0.04, 0.04, 0.05), 5)
        if lt < on_t: ctx.rectangle(x, y, w, h); ctx.set_source_rgb(0.02, 0.02, 0.03); ctx.fill()
        elif lt < on_t + 0.35:
            rs = random.Random(int(lt * 30))
            for k in range(160): ctx.rectangle(x + rs.uniform(0, w - 8), y + rs.uniform(0, h - 6), 8, 6); g_ = rs.uniform(0.2, 1); ctx.set_source_rgb(g_, g_, g_); ctx.fill()
        else:
            cam_feed(ctx, x, y, w, h, lt, lit(CUR["t"]), figure(lt), zoom=zoom)
            glow(ctx, 540, 840, 600, (0.4, 0.9, 0.5), 0.25)
        ctx.restore()
    return f


def chain_ins(slide=lambda lt, d: 0.0, fall=False):
    def f(ctx, lt, d):
        ctx.set_source_rgb(0.20, 0.15, 0.12); ctx.paint()
        ctx.rectangle(640, 0, 440, 1920); fs(ctx, (0.26, 0.24, 0.28), 0)
        ctx.rectangle(0, 0, 640, 1920); fs(ctx, (0.30, 0.22, 0.18), 0)
        u = slide(lt, d)
        rrect(ctx, 180, 860, 420, 70, 14); fs(ctx, (0.65, 0.65, 0.68), 6)   # track on door
        ctx.rectangle(200, 885, 380, 20); ctx.set_source_rgb(0.25, 0.25, 0.28); ctx.fill()
        rrect(ctx, 760, 820, 90, 220, 16); fs(ctx, (0.65, 0.65, 0.68), 6)   # anchor on frame
        if not fall:
            kx = lerp(240, 560, u)
            ell(ctx, kx, 895, 26, 26); fs(ctx, (0.8, 0.8, 0.82), 5)
            n = 10
            for k in range(n):
                v = k / (n - 1); cx_ = lerp(kx, 805, v); cy_ = 895 + 60 * sin(v * pi) * (1 - u * 0.7)
                ell(ctx, cx_, cy_, 20, 13, 0.3 * (k % 2)); st(ctx, (0.8, 0.8, 0.82), 8)
        else:
            p = clamp(lt / 0.4)
            for k in range(10): ell(ctx, 805 + 10 * sin(k), 940 + k * 34 * p + 10, 13, 20); st(ctx, (0.8, 0.8, 0.82), 8)
        overlay(ctx, (0, 0, 0.05), 0.35); vignette(ctx, 0.5)
    return f


def salt_ins(stage="jar"):
    def f(ctx, lt, d):
        if stage == "jar":
            BG(ctx, "kitchen_h", 14); overlay(ctx, (0, 0, 0), 0.25)
            rrect(ctx, 360, 700, 360, 520, 50); fs(ctx, (0.85, 0.88, 0.92), 7)
            rrect(ctx, 340, 640, 400, 100, 20); fs(ctx, (0.25, 0.45, 0.75), 6)
            text(ctx, "SALT", 540, 980, 90, col=(0.25, 0.45, 0.75))
            if lt > 0.4:
                u = sm(clamp((lt - 0.4) / 0.6))
                ctx.save(); ctx.translate(560, lerp(820, 560, u)); ctx.rotate(0.15); note(ctx, ["4. SALT. 3:33."], scrap=True, rot=0); ctx.restore()
        elif stage == "pour":
            ctx.set_source_rgb(0.12, 0.10, 0.10); ctx.paint()
            poly(ctx, [(-100, 820), (1180, 820), (1180, 2000), (-100, 2000)]); fs(ctx, (0.18, 0.14, 0.12), 0)
            ctx.rectangle(-100, 600, 1300, 220); fs(ctx, (0.30, 0.22, 0.18), 0)   # door bottom
            ctx.rectangle(-100, 800, 1300, 24); ctx.set_source_rgba(1, 0.9, 0.7, 0.8 * flick(CUR["t"], 2)); ctx.fill()
            u = clamp(lt / (d * 0.9)); xe = lerp(-60, 1140, u)
            ctx.rectangle(-60, 900, xe + 60, 40); ctx.set_source_rgb(0.95, 0.95, 0.97); ctx.fill()
            rs = random.Random(1)
            for k in range(80):
                xx = rs.uniform(-60, 1140)
                if xx < xe: ell(ctx, xx, 900 + rs.uniform(-20, 60), 4, 4); ctx.set_source_rgb(1, 1, 1); ctx.fill()
            ctx.save(); ctx.translate(xe, 600); ctx.rotate(2.4)
            rrect(ctx, -80, -120, 160, 240, 30); fs(ctx, (0.85, 0.88, 0.92), 6); ctx.restore()
            ctx.move_to(xe - 40, 680); ctx.line_to(xe - 10, 900); st(ctx, (1, 1, 1), 8)
        elif stage == "diagram":
            ctx.set_source_rgb(0.04, 0.04, 0.06); ctx.paint()
            ctx.save(); ctx.translate(0, 80); BG(ctx, "entry", 0); draw_door(ctx, under=0.8); ctx.restore(); overlay(ctx, (0, 0, 0), 0.35)
            x, y, w, h = DOOR; y += 80
            ctx.rectangle(x - 40, y + h + 70, w + 80, 26); ctx.set_source_rgb(1, 1, 1); ctx.fill()
            label(ctx, lt, 0.2, "salt line", 540, y + h + 200, 70, -0.04, (1, 1, 1))
    return f


def elevator_ins(ding_t=99, clock="3:33"):
    def f(ctx, lt, d):
        ctx.set_source_rgb(0.05, 0.05, 0.06); ctx.paint()
        rrect(ctx, 290, 500, 500, 900, 30); fs(ctx, (0.45, 0.46, 0.50), 8)
        rrect(ctx, 380, 600, 320, 160, 16); ctx.set_source_rgb(0.02, 0.02, 0.02); ctx.fill()
        text(ctx, "9", 540, 720, 120, col=(1, 0.5, 0.15))
        on = lt >= ding_t
        ell(ctx, 540, 1000, 90, 90); fs(ctx, (1, 0.9, 0.5) if on else (0.3, 0.3, 0.32), 7)
        if on:
            glow(ctx, 540, 1000, 500, (1, 0.85, 0.4), 0.6 * (1 - clamp((lt - ding_t) / 1.5)))
            pop_word(ctx, lt, ding_t, "DING", 540, 1620, 150, col=(1, 0.9, 0.5), rot=0, life=1.2)
        poly(ctx, [(540, 950), (500, 1010), (580, 1010)]); ctx.set_source_rgb(0.1, 0.1, 0.1); ctx.fill()
        if clock: label(ctx, lt, 0.1, clock, 540, 440, 90, 0, RED)
    return f


def bpm_ins(vals):
    def f(ctx, lt, d):
        ctx.set_source_rgb(0.02, 0.03, 0.04); ctx.paint()
        cur = vals[0][1]
        for t0, v in vals:
            if lt >= t0: cur = v
        for k in range(0, 1080, 60): ctx.move_to(k, 600); ctx.line_to(k, 1300); st(ctx, (0.05, 0.2, 0.1), 2)
        ctx.new_path()
        sp = cur / 60
        for x in range(0, 1080, 6):
            ph = ((x / 1080) * 3 - lt * sp) % 1
            y = 950 - (260 if 0.45 < ph < 0.5 else -120 if 0.5 <= ph < 0.55 else 0)
            (ctx.line_to if x else ctx.move_to)(x, y)
        st(ctx, (0.2, 1, 0.4), 7)
        text(ctx, str(cur), 540, 600, 200, col=RED if cur > 100 else (0.2, 1, 0.4), stroke=14)
        text(ctx, "BPM", 540, 700, 60, col=(1, 1, 1))
    return f


def breathe_ecu(phases):
    """phases: list of (t0, label, dur) in shot-local time"""
    def f(ctx, lt, d):
        ctx.save(); cam(ctx, 1.0 + 0.04 * sm(lt / d), 540, 920); BG(ctx, "entry", 18)
        lab, prog = None, 0
        for t0, l_, du in phases:
            if lt >= t0: lab, prog = l_, clamp((lt - t0) / du)
        draw_char(ctx, YOU, dict(x=540, y=head_y(2.6, 860), s=2.6, mood=M("sad", lid=0.95) if lab else M("scared"), blink=bool(lab), dark=0.25), CUR["t"])
        ctx.restore()
        if lab:
            r = 380 + (40 * prog if lab == "IN" else 40 if lab == "HOLD" else 40 * (1 - prog))
            ctx.new_path(); ctx.arc(540, 850, r, -pi / 2, -pi / 2 + 2 * pi * prog); st(ctx, (0.4, 0.8, 1), 14)
            rrect(ctx, 400, 1150, 280, 80, 40); ctx.set_source_rgba(0, 0, 0, 0.6); ctx.fill()
            text(ctx, f"{lab} {min(4, int(prog * 4) + 1)}/4", 540, 1208, 46, col=(0.5, 0.85, 1))
    return f


def landlord_flash(talk_=False, lean=False, lab=None):
    def f(ctx, lt, d):
        if not talk_ and not lean:
            ctx.save(); cam(ctx, 1.0 + 0.05 * sm(lt / d), 540, 1050); BG(ctx, "entry_day", 4)
            draw_char(ctx, LANDLORD, dict(x=360, y=head_y(1.45, 900), s=1.45, mood="neutral", look=0.7, glasses=True), CUR["t"])
            P = dict(x=760, y=head_y(1.4, 920), s=1.4, mood="happy", look=-0.6); P["armL"] = ik(P, 700, 1250, 1); P["armR"] = ik(P, 830, 1250, -1)
            draw_char(ctx, YOU, P, CUR["t"]); rrect(ctx, 650, 1180, 240, 190, 10); fs(ctx, (0.75, 0.6, 0.4), 6)
            ctx.restore()
        else:
            ctx.save(); cam(ctx, punch(lt) * (1.0 + (0.25 if lean else 0.08) * sm(lt / d)), 540, 900); BG(ctx, "entry_day", 18)
            draw_char(ctx, LANDLORD, dict(x=540, y=head_y(2.7, 860), s=2.7, mood=M("cold", eo=1.2) if lean else M("worried"), glasses=True,
                                          mouth=talkT("LL")), CUR["t"])
            ctx.restore()
        overlay(ctx, (1, 0.8, 0.5), 0.2); grain(ctx, lt, 0.12); vignette(ctx, 0.6, 380, 1100)
        if lab: label(ctx, lt, 0.2, lab, 540, 520, 72)
    return f


def drawer_ins(ctx, lt, d):
    ctx.set_source_rgb(0.10, 0.09, 0.09); ctx.paint()
    ctx.save(); cam(ctx, 1.0 + 0.1 * sm(lt / d), 540, 960)
    rrect(ctx, 120, 600, 840, 760, 20); fs(ctx, (0.30, 0.22, 0.16), 8); rrect(ctx, 160, 640, 760, 680, 10); ctx.set_source_rgb(0.18, 0.13, 0.10); ctx.fill()
    rs = random.Random(6)
    for k in range(9):
        ctx.save(); ctx.translate(rs.uniform(240, 840), rs.uniform(720, 1240)); ctx.rotate(rs.uniform(0, pi))
        rrect(ctx, -70, -22, 140, 44, 10); fs(ctx, (0.15, 0.15, 0.16), 4); ctx.rectangle(30, -22, 40, 44); ctx.set_source_rgb(0.85, 0.6, 0.2); ctx.fill(); ctx.restore()
    u = sm(clamp((lt - 0.4) / 0.8))
    ctx.save(); ctx.translate(560, lerp(1000, 900, u)); ctx.rotate(0.2); ctx.scale(0.45, 0.45); note(ctx, NOTE1[:2]); ctx.restore()
    ctx.restore()
    glow(ctx, 540, 960, 600, (1, 0.9, 0.6), 0.15)


def figure_ecu(ctx, lt, d):
    ctx.set_source_rgb(0.0, 0.0, 0.0); ctx.paint()
    a = clamp(lt / 0.6)
    ctx.save(); cam(ctx, 1.0 + 0.15 * sm(lt / d), 540, 700)
    cam_feed(ctx, 0, 0, 1080, 1920, lt, lit=False, figure=0, zoom=1)
    shadow_figure(ctx, 540, 1700, 2.3, a)
    ctx.restore()


def you_double(ctx):
    P = dict(x=560, y=1330, s=0.85, legs=True, mood=M("neutral", eyes=None), look=-1)
    P["armR"] = ik(P, 660, 980, -1)
    draw_char(ctx, YOU, P, 0.3)
    hx, hy = head_world(P)
    for sx in (-1, 1): ell(ctx, hx + sx * 30 * 0.85, hy, 9, 9); ctx.set_source_rgb(1, 1, 1); ctx.fill()


def T(sc, w):
    return WT(sc, *w) if isinstance(w, tuple) else WT(sc, w)


def door_you(mood, x=640, day=False, push=False, open_=0.0, z=(1.0, 1.08), amp=0, look=-1):
    def f(ctx, lt, d):
        dx, dy = shake(lt, amp)
        ctx.save(); cam(ctx, lerp(z[0], z[1], sm(lt / d)), 540, 980, dx=dx, dy=dy)
        BG(ctx, "entry_day" if day else "entry", 0)
        op = open_(lt, d) if callable(open_) else open_
        draw_door(ctx, open_=op, under=0 if day else 0.7 * flick(CUR["t"], 3), day=day)
        P = dict(x=x, y=head_y(1.5, 840), s=1.5, legs=True, mood=mood(lt) if callable(mood) else mood, look=look, dark=0 if day else 0.3, tilt=-0.2 if push else 0)
        if push: P["armL"] = ik(P, DOOR[0] + DOOR[2] - 10, 1000, 1); P["armR"] = ik(P, DOOR[0] + DOOR[2] - 20, 900, -1)
        draw_char(ctx, YOU, P, CUR["t"])
        ctx.restore()
    return f


def corridor_out(steps):
    def f(ctx, lt, d):
        ctx.save(); cam(ctx, 1.0 + 0.08 * sm(lt / d), 540, 1000); BG(ctx, "corridor", 0)
        n = sum(1 for s_ in steps if lt >= s_)
        if n: overlay(ctx, (0, 0, 0), min(0.95, 0.32 * n))
        if n >= 2: shadow_figure(ctx, 540, 1250, 1.1, 0.5 * (n - 1))
        ctx.restore()
    return f
