# exec'd inside dna.py globals for "Checkout" (hotel series)
exec(open(f"{HERE}/hor_common.py").read())
COLS_EXTRA = {"N": (1, 1, 1), "TV": (0.6, 0.85, 1.0), "WAL": (1, 0.86, 0.15), "MAY": (0.5, 1, 0.8), "LEO": (1, 0.7, 0.4), "GR": (1, 0.35, 0.35)}
AI_DIR = f"{HERE}/ai_bg2"
PS = 1.12


def aiplate(name):
    def f(ctx):
        im = _Image.open(f"{AI_DIR}/{name}.png").convert("RGBA")
        k = max(1080 * PS / im.width, 1920 * PS / im.height)
        im = im.resize((int(im.width * k), int(im.height * k)), _Image.LANCZOS)
        ctx.set_source_surface(to_surface(im), 540 - im.width / 2, 960 - im.height / 2); ctx.paint()
    return f


for _n in ("room714", "room_tv", "window_fog", "corridor", "corridor_dark", "elevator", "stair_door", "lobby", "bus_rain", "hospital", "light_door"):
    SETS[_n] = aiplate(_n)

YOU = dict(skin=(0.90, 0.72, 0.58), hair=(0.22, 0.15, 0.10), hairstyle="crew", outfit="hoodie", top=(0.28, 0.36, 0.30), seed=91, pants=(0.2, 0.2, 0.25))
MAYA = dict(skin=(0.72, 0.52, 0.40), hair=(0.08, 0.06, 0.05), hairstyle="bun", outfit="longsleeve", top=(0.35, 0.68, 0.68), seed=170, blush=True)
WALT = dict(skin=(0.92, 0.76, 0.64), hair=(0.85, 0.85, 0.87), hairstyle="crew", outfit="cardigan", top=(0.55, 0.40, 0.28), no_lanyard=True, seed=171, beard=True)
LEO = dict(skin=(0.96, 0.82, 0.70), hair=(0.55, 0.32, 0.15), hairstyle="crew", outfit="hoodie", top=(0.85, 0.45, 0.20), seed=172, freckles=True, blush=True)
GRANT = dict(skin=(0.95, 0.80, 0.68), hair=(0.30, 0.22, 0.14), hairstyle="crew", outfit="suit", top=(0.15, 0.17, 0.22), no_badge=True, seed=173)
EX1 = dict(skin=(0.60, 0.42, 0.32), hair=(0.06, 0.05, 0.05), hairstyle="curly", outfit="hoodie", top=(0.60, 0.25, 0.35), seed=174, blush=True)
EX2 = dict(skin=(0.88, 0.70, 0.58), hair=(0.45, 0.30, 0.15), hairstyle="crew", outfit="sweater", top=(0.30, 0.40, 0.55), seed=175)

_draw_char_raw = draw_char
TINTS = {"warm": (1.0, 0.86, 0.72), "dark": (0.55, 0.62, 0.80), "blue": (0.75, 0.82, 1.0), "sun": (1.0, 0.92, 0.82), "none": (1, 1, 1)}
SCENE_TINT = {}


def draw_char(ctx, ch, P, t):
    tint = TINTS.get(P.get("tint") or SCENE_TINT.get(CUR["sc"], "warm"))
    if tint == (1, 1, 1): return _draw_char_raw(ctx, ch, P, t)
    ctx.push_group(); _draw_char_raw(ctx, ch, P, t); pat = ctx.pop_group()
    ctx.set_source(pat); ctx.paint()
    ctx.save(); ctx.set_operator(cairo.OPERATOR_MULTIPLY); ctx.set_source_rgb(*tint); ctx.mask(pat); ctx.restore()


def BGI(name, z=(1.0, 1.1), cy=960, cx=540, amp=0, post=None, dark=0.0):
    def f(ctx, lt, d):
        dx, dy = shake(lt, amp)
        ctx.save(); cam(ctx, punch(lt, 0.03) * lerp(z[0], z[1], sm(lt / d)), cx, cy, dx=dx, dy=dy); BG(ctx, name, 0); ctx.restore()
        if dark: overlay(ctx, (0, 0, 0), dark)
        if post: post(ctx, lt, d)
    return f


def cast_shot(bg, cast, z=(1.0, 1.08), cy=1050, blur=3, amp=0, post=None, darkness=None):
    """cast: list of (ch, x, hy, s, mood, spk, extra)"""
    def f(ctx, lt, d):
        dx, dy = shake(lt, amp)
        ctx.save(); cam(ctx, punch(lt, 0.03) * lerp(z[0], z[1], sm(lt / d)), 540, cy, dx=dx, dy=dy); BG(ctx, bg, blur)
        for c in cast:
            ch, x, hy, s, mood, spk = c[:6]; ex = c[6] if len(c) > 6 else {}
            mo = mood(lt) if callable(mood) else mood
            P = dict(x=x, y=head_y(s, hy), s=s, mood=mo, mouth=talkT(spk) if spk else 0.0); P.update(ex(lt) if callable(ex) else ex)
            draw_char(ctx, ch, P, CUR["t"])
        ctx.restore()
        if darkness: overlay(ctx, (0, 0, 0), darkness(lt, d))
        if post: post(ctx, lt, d)
    return f


def tv_msg(lines, spk="TV"):
    def f(ctx, lt, d):
        ctx.save(); cam(ctx, 1.0 + 0.06 * sm(lt / d), 540, 960); BG(ctx, "room_tv", 18); ctx.restore(); overlay(ctx, (0, 0, 0), 0.35)
        ctx.save(); ctx.translate(540, 900); ctx.rotate(-0.02)
        rrect(ctx, -430, -330, 860, 640, 40); fs(ctx, (0.30, 0.22, 0.16), 10)
        rrect(ctx, -380, -280, 760, 520, 60); ctx.set_source_rgb(0.08, 0.14, 0.26); ctx.fill()
        glow(ctx, 0, -20, 520, (0.5, 0.7, 1), 0.35)
        shown = 0
        for i, (t0, s_) in enumerate(lines):
            if lt >= t0:
                text(ctx, s_, 0, -150 + i * 110, 64 if len(s_) < 16 else 52, col=(0.85, 0.93, 1.0)); shown += 1
        for k in range(-280, 240, 8): ctx.rectangle(-380, k, 760, 3); ctx.set_source_rgba(0, 0, 0, 0.18); ctx.fill()
        a = talkT(spk)
        for i in range(24):
            h_ = 6 + 70 * a * abs(sin(i * 1.3 + CUR["t"] * 15)); ctx.rectangle(-300 + i * 26, 200 - h_ / 2, 14, h_); ctx.set_source_rgb(0.6, 0.85, 1); ctx.fill()
        ctx.restore()
    return f


def door_sign(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.12 * sm(lt / d), 540, 960); BG(ctx, "corridor", 22); ctx.restore(); overlay(ctx, (0, 0, 0), 0.35)
    ctx.save(); ctx.translate(540, 960)
    rrect(ctx, -420, -900, 840, 1800, 10); fs(ctx, (0.42, 0.26, 0.16), 8)
    ell(ctx, 260, -80, 60, 60); fs(ctx, (0.85, 0.7, 0.35), 6)
    rrect(ctx, 180, -100, 200, 40, 20); fs(ctx, (0.85, 0.7, 0.35), 5)
    sw = 0.12 * sin(lt * 2.5) * (1 - clamp(lt / 3))
    ctx.translate(250, -60); ctx.rotate(sw)
    ctx.move_to(-30, 0); ctx.line_to(0, 120); ctx.line_to(30, 0); st(ctx, (0.9, 0.85, 0.7), 6)
    rrect(ctx, -170, 110, 340, 420, 20); fs(ctx, (0.95, 0.92, 0.85), 6)
    text(ctx, "CHECKED", 0, 260, 62, col=(0.75, 0.1, 0.1)); text(ctx, "OUT", 0, 350, 90, col=(0.75, 0.1, 0.1))
    ctx.restore()


def ticket(ctx, lt, d):
    ctx.set_source_rgb(0.18, 0.14, 0.12); ctx.paint(); glow(ctx, 540, 900, 600, (1, 0.85, 0.6), 0.25)
    for i, (dx_, r) in enumerate(((-120, -0.12), (0, 0.0), (120, 0.1))):
        if lt < i * 0.3: continue
        ctx.save(); ctx.translate(540 + dx_, 960 + i * 40); ctx.rotate(r)
        rrect(ctx, -280, -150, 560, 300, 16); fs(ctx, (0.95, 0.90, 0.75), 5)
        ctx.rectangle(-280, -150, 560, 70); ctx.set_source_rgb(0.15, 0.35, 0.65); ctx.fill()
        text(ctx, "CITY BUS", 0, -100, 40, col=(1, 1, 1))
        text(ctx, "ROUTE 9", 0, 0, 80, col=(0.15, 0.15, 0.2)); text(ctx, "NOV 25  -  11:48 PM", 0, 90, 34, col=(0.4, 0.3, 0.3))
        ctx.restore()


def keycard(ctx, lt, d):
    ctx.set_source_rgb(0.06, 0.06, 0.08); ctx.paint(); glow(ctx, 540, 900, 600, (1, 0.9, 0.6), 0.25 * sm(clamp(lt / 0.8)))
    p = sm(clamp(lt / 0.7)); ctx.save(); ctx.translate(540, lerp(1300, 950, p)); ctx.rotate(lerp(0.4, -0.06, p))
    rrect(ctx, -330, -210, 660, 420, 30); fs(ctx, (0.75, 0.62, 0.30), 6)
    ctx.rectangle(-330, -110, 660, 60); ctx.set_source_rgb(0.15, 0.12, 0.08); ctx.fill()
    text(ctx, "ROOM", -120, 70, 50, col=(0.3, 0.22, 0.1)); text(ctx, "714", 120, 100, 130, col=(0.25, 0.15, 0.05))
    ctx.restore()


def fire_news(ctx, lt, d):
    ctx.set_source_rgb(0.20, 0.16, 0.12); ctx.paint()
    ctx.save(); ctx.translate(540, 930); ctx.rotate(0.04)
    ctx.rectangle(-430, -560, 860, 1120); fs(ctx, (0.88, 0.82, 0.68), 6)
    text(ctx, "THE EVENING STAR", 0, -470, 56, col=(0.15, 0.12, 0.1)); text(ctx, "1986", 330, -470, 30, col=(0.4, 0.3, 0.2))
    text(ctx, "GRAND HOTEL", 0, -340, 96, col=(0.15, 0.12, 0.1)); text(ctx, "DESTROYED", 0, -240, 96, col=(0.6, 0.1, 0.08)); text(ctx, "BY FIRE", 0, -140, 96, col=(0.15, 0.12, 0.1))
    ctx.rectangle(-380, -70, 760, 420); ctx.set_source_rgb(0.25, 0.2, 0.17); ctx.fill()
    blob(ctx, [(-100, 150, 140), (60, 100, 170), (200, 160, 130)], (0.55, 0.30, 0.15))
    ctx.rectangle(-250, 120, 500, 230); ctx.set_source_rgb(0.12, 0.1, 0.09); ctx.fill()
    ctx.restore()
    overlay(ctx, (1, 0.8, 0.5), 0.18); grain(ctx, lt, 0.12)


def stuck_clock(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.1 * sm(lt / d), 540, 960); BG(ctx, "room714", 20); ctx.restore(); overlay(ctx, (0, 0, 0), 0.4)
    ell(ctx, 540, 900, 300, 300); fs(ctx, (0.95, 0.92, 0.85), 14); ell(ctx, 540, 900, 300, 300); st(ctx, (0.45, 0.32, 0.18), 30)
    for k in range(12):
        a_ = k * pi / 6; ctx.move_to(540 + 250 * cos(a_), 900 + 250 * sin(a_)); ctx.line_to(540 + 275 * cos(a_), 900 + 275 * sin(a_)); st(ctx, OUTL, 8)
    for ang, L, w in ((-pi / 2 + 2.14 / 12 * 2 * pi, 150, 16), (-pi / 2 + 14 / 60 * 2 * pi, 230, 10)):
        ctx.move_to(540, 900); ctx.line_to(540 + L * cos(ang), 900 + L * sin(ang)); st(ctx, OUTL, w)
    sa = -pi / 2 + (int(lt * 2) % 2) * 0.1
    ctx.move_to(540, 900); ctx.line_to(540 + 260 * cos(sa), 900 + 260 * sin(sa)); st(ctx, (0.8, 0.1, 0.1), 4)
    label(ctx, lt, 0.4, "stuck", 540, 1330, 80, -0.05, (1, 0.35, 0.35))


def hand_key(ctx, lt, d):
    ctx.set_source_rgb(0.10, 0.09, 0.10); ctx.paint(); glow(ctx, 540, 1000, 700, (1, 0.9, 0.7), 0.3)
    u = sm(clamp(lt / d))
    rrect(ctx, 120, 1100, 340, 900, 120); fs(ctx, LEO["top"], 8)          # Leo's sleeve
    ell(ctx, 330, 1060, 170, 150); fs(ctx, LEO["skin"], 8)
    ctx.save(); ctx.translate(lerp(820, 420, u), lerp(800, 980, u)); ctx.rotate(-0.4)
    rrect(ctx, -160, -100, 320, 200, 20); fs(ctx, (0.75, 0.62, 0.30), 6); text(ctx, "714", 0, 40, 90, col=(0.25, 0.15, 0.05)); ctx.restore()
    rrect(ctx, 700, 500, 380, 900, 140); fs(ctx, YOU["top"], 8)
    ell(ctx, lerp(820, 470, u), lerp(760, 960, u), 160, 130); fs(ctx, YOU["skin"], 8)


def checkout_hud(start_min, end_min, scenes):
    def hud(ctx, sc, t):
        if sc not in scenes: return
        keys = list(TL); i = keys.index(sc)
        m = lerp(start_min, end_min, (i + t / DUR(sc)) / len(keys))
        rrect(ctx, 640, 200, 380, 76, 38); ctx.set_source_rgba(0, 0, 0, 0.6); ctx.fill()
        text(ctx, f"CHECKOUT {int(m):02d}:{int((m % 1) * 60):02d}", 830, 254, 36, col=(1, 0.35, 0.35) if m < 15 else (1, 1, 1))
    return hud


def LIGHT_STD(sc, t):
    return dict(amb=(1.0, 0.98, 0.96), bloom=0.7, thr=0.62, vig=0.55)
