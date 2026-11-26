# exec'd inside dna.py globals for "We Will Not Land"
exec(open(f"{HERE}/hor_common.py").read())
COLS_EXTRA = {"N": (1, 1, 1), "CAP": (1, 0.86, 0.15), "CP": (1, 0.86, 0.15), "FA": (0.6, 0.85, 1.0), "MAN": (1, 0.3, 0.3)}
PLATE_DIR = f"{HERE}/b3d/plates"
PS = 1.15   # plates are scaled up a little so the camera can move


def plate(name):
    def f(ctx):
        im = _Image.open(f"{PLATE_DIR}/{name}.png").convert("RGBA").resize((int(1080 * PS), int(1920 * PS)), _Image.LANCZOS)
        s = to_surface(im)
        ctx.set_source_surface(s, 540 - 540 * PS, 960 - 960 * PS); ctx.paint()
    return f


for _n in ("aisle_red", "aisle_night", "row_red", "front_red", "door_red", "cockpit", "cockpit_grn", "bay", "runway_dawn"):
    SETS[_n] = plate(_n)

# ---------- cast ----------
YOU = dict(skin=(0.90, 0.72, 0.58), hair=(0.22, 0.15, 0.10), hairstyle="crew", outfit="hoodie", top=(0.32, 0.34, 0.42), seed=91, pants=(0.2, 0.2, 0.25))
NINA = dict(skin=(0.95, 0.80, 0.68), hair=(0.80, 0.62, 0.35), hairstyle="bun", outfit="cardigan", top=(0.12, 0.16, 0.34), no_lanyard=True, seed=140, blush=True)
CAPT = dict(skin=(0.90, 0.72, 0.60), hair=(0.75, 0.75, 0.78), hairstyle="crew", outfit="suit", top=(0.10, 0.12, 0.25), no_badge=True, seed=141, mustache=True)
COPI = dict(skin=(0.80, 0.60, 0.46), hair=(0.20, 0.14, 0.10), hairstyle="crew", outfit="suit", top=(0.10, 0.12, 0.25), no_badge=True, seed=142)
MAN = dict(skin=(0.93, 0.80, 0.70), hair=(0.06, 0.05, 0.05), hairstyle="crew", outfit="suit", top=(0.14, 0.14, 0.16), no_badge=True, seed=143)
PAX = [dict(skin=s, hair=h, hairstyle=hs, outfit="hoodie" if i % 2 else "sweater", top=c, seed=150 + i, blush=i % 3 == 0)
       for i, (s, h, hs, c) in enumerate([((0.95, 0.80, 0.68), (0.55, 0.35, 0.20), "long", (0.6, 0.3, 0.4)), ((0.70, 0.50, 0.38), (0.08, 0.06, 0.05), "crew", (0.3, 0.5, 0.4)),
                                             ((0.98, 0.86, 0.77), (0.85, 0.75, 0.45), "bob", (0.5, 0.5, 0.7)), ((0.55, 0.38, 0.28), (0.05, 0.04, 0.04), "curly", (0.8, 0.6, 0.2)),
                                             ((0.90, 0.72, 0.60), (0.40, 0.40, 0.42), "crew", (0.35, 0.35, 0.4)), ((0.80, 0.62, 0.48), (0.25, 0.15, 0.08), "bun", (0.7, 0.4, 0.3))])]

# ---------- light: characters take the colour of the scene ----------
_draw_char_raw = draw_char
TINT = {"red": (1.0, 0.66, 0.62), "night": (0.84, 0.88, 1.0), "dark": (0.74, 0.74, 0.86), "dawn": (1.0, 0.88, 0.76), "none": (1, 1, 1)}
SCENE_TINT = {}


def draw_char(ctx, ch, P, t):
    tint = TINT.get(P.get("tint") or SCENE_TINT.get(CUR["sc"], "none"), (1, 1, 1))
    if tint == (1, 1, 1): return _draw_char_raw(ctx, ch, P, t)
    ctx.push_group(); _draw_char_raw(ctx, ch, P, t); pat = ctx.pop_group()
    ctx.set_source(pat); ctx.paint()
    ctx.save(); ctx.set_operator(cairo.OPERATOR_MULTIPLY); ctx.set_source_rgb(*tint); ctx.mask(pat); ctx.restore()


# ---------- perspective helper for the aisle plates ----------
FPX = 1173.0


def proj_aisle(x, y, z):
    d = y + 0.6
    sx = 540 + FPX * x / d; sy = 960 - FPX * ((z - 1.65) / d + 0.017)
    return 540 + (sx - 540) * PS, 960 + (sy - 960) * PS, FPX * PS / d


def heads_aisle(ctx, t, rows=range(1, 14), skip=(), panic=0.0, hide_1a=False):
    rs = random.Random(7)
    items = []
    for i in rows:
        y = 1.0 + i * 0.9
        for side in (-1, 1):
            for k in range(3):
                if rs.random() < 0.25 or (i, side, k) in skip: continue
                x = side * (0.8 + k * 0.5); hair = rs.choice([(0.08, 0.06, 0.05), (0.35, 0.22, 0.12), (0.7, 0.55, 0.3), (0.5, 0.5, 0.52), (0.2, 0.12, 0.08)])
                items.append((y, x, hair, rs.random()))
    for y, x, hair, ph in sorted(items, key=lambda a: -a[0]):
        jx = panic * 0.06 * sin(t * 9 + ph * 20); jz = panic * 0.03 * sin(t * 7 + ph * 9)
        sx, sy, sc_ = proj_aisle(x + jx, y + 0.05, 1.22 + jz)
        ell(ctx, sx, sy, 0.12 * sc_, 0.14 * sc_); ctx.set_source_rgb(*shade(hair, 0.3)); ctx.fill()
        ell(ctx, sx, sy - 0.02 * sc_, 0.11 * sc_, 0.12 * sc_); ctx.set_source_rgb(*hair); ctx.fill()


def aisle(mood="red", z=(1.0, 1.08), cy=960, panic=0.0, walker=None, amp=0, post=None, rows=range(1, 14)):
    def f(ctx, lt, d):
        dx, dy = shake(lt, amp)
        ctx.save(); cam(ctx, punch(lt, 0.03) * lerp(z[0], z[1], sm(lt / d)), 540, cy, dx=dx, dy=dy)
        BG(ctx, f"aisle_{mood}", 0)
        heads_aisle(ctx, CUR["t"], rows, panic=panic)
        if walker: walker(ctx, lt, d)
        ctx.restore()
        if post: post(ctx, lt, d)
    return f


# ---------- props / inserts ----------
def exterior(ctx, lt, d):
    g = cairo.LinearGradient(0, 0, 0, 1920); g.add_color_stop_rgb(0, 0.01, 0.01, 0.05); g.add_color_stop_rgb(1, 0.08, 0.09, 0.20); ctx.set_source(g); ctx.paint()
    ell(ctx, 820, 380, 70, 70); ctx.set_source_rgb(0.95, 0.95, 0.88); ctx.fill(); glow(ctx, 820, 380, 320, (0.8, 0.8, 1), 0.3)
    rs = random.Random(3)
    for i in range(70): ell(ctx, rs.uniform(0, 1080), rs.uniform(0, 900), 2, 2); ctx.set_source_rgba(1, 1, 1, rs.uniform(0.3, 0.9)); ctx.fill()
    off = lt * 60
    for k in range(7):
        x = (k * 260 - off) % 1500 - 200; y = 1350 + 90 * sin(k * 2.1)
        blob(ctx, [(x, y, 160), (x + 120, y - 40, 140), (x + 240, y + 10, 150)], (0.18, 0.20, 0.32))
    ctx.save(); ctx.translate(540, 900 + 12 * sin(lt * 1.2)); ctx.rotate(-0.06)
    ell(ctx, 0, 0, 430, 62); ctx.set_source_rgb(0.62, 0.64, 0.70); ctx.fill()
    poly(ctx, [(-40, 10), (120, 10), (-160, 260), (-260, 260)]); ctx.set_source_rgb(0.52, 0.54, 0.60); ctx.fill()
    poly(ctx, [(300, -20), (420, -20), (460, -200), (390, -200)]); ctx.set_source_rgb(0.52, 0.54, 0.60); ctx.fill()
    for k in range(18): ell(ctx, -330 + k * 36, -12, 7, 9); ctx.set_source_rgb(1, 0.9, 0.6); ctx.fill()
    on = (lt % 1.2) < 0.15
    ell(ctx, -230, 260, 10, 10); ctx.set_source_rgb(*((1, 0.1, 0.1) if on else (0.4, 0.1, 0.1))); ctx.fill()
    if on: glow(ctx, -230, 260, 120, (1, 0.1, 0.1), 0.8)
    ctx.restore()
    label(ctx, lt, 0.4, "FLIGHT 1407", 540, 520, 80, -0.04, (1, 1, 1))
    label(ctx, lt, 0.9, "to Denver", 540, 610, 60, -0.04, (1, 0.86, 0.15))


def placard(red=False):
    def f(ctx, lt, d):
        BG(ctx, "aisle_red", 20); overlay(ctx, (0, 0, 0), 0.35)
        ctx.save(); cam(ctx, 1.0 + 0.15 * sm(lt / d), 540, 900)
        rrect(ctx, 140, 700, 800, 380, 30); fs(ctx, (0.85, 0.86, 0.88), 8)
        for i, x in enumerate((300, 540, 780)):
            ell(ctx, x, 800, 50, 50); fs(ctx, (1, 0.95, 0.7) if i == 1 else (0.6, 0.6, 0.62), 5)
        text(ctx, "14", 300, 1010, 110, col=(0.2, 0.2, 0.25)); text(ctx, "A  B", 560, 1010, 80, col=(0.4, 0.4, 0.45))
        c = RED if red and (lt * 3) % 1 < 0.6 else (0.2, 0.2, 0.25)
        text(ctx, "C", 800, 1010, 110, col=c)
        if red: glow(ctx, 800, 960, 260, (1, 0.1, 0.1), 0.4)
        ctx.restore()
    return f


def lock_screen(ctx, lt):
    ctx.set_source_rgb(0.08, 0.10, 0.20); ctx.paint()
    text(ctx, "2:14", 0, -120, 120, col=(1, 1, 1)); text(ctx, "Thursday", 0, -50, 26, col=(0.8, 0.8, 0.9), weight=False)
    rrect(ctx, -130, 40, 260, 70, 16); ctx.set_source_rgba(1, 1, 1, 0.15); ctx.fill(); text(ctx, "Airplane mode", 0, 85, 22, col=(1, 1, 1), weight=False)


def pa_speaker(ctx, lt, d):
    ctx.set_source_rgb(0.75, 0.74, 0.72); ctx.paint()
    BG(ctx, "aisle_red", 25); overlay(ctx, (0, 0, 0), 0.4)
    ctx.save(); cam(ctx, 1.0 + 0.12 * sm(lt / d), 540, 860)
    ell(ctx, 540, 860, 260, 260); fs(ctx, (0.55, 0.55, 0.56), 8)
    for k in range(-8, 9):
        for j in range(-8, 9):
            if k * k + j * j < 70: ell(ctx, 540 + k * 26, 860 + j * 26, 7, 7); ctx.set_source_rgb(0.15, 0.15, 0.16); ctx.fill()
    a = talkT("CAP")
    for k in range(3):
        r = 280 + 60 * k + 40 * ((lt * 2 + k / 3) % 1)
        ctx.new_path(); ctx.arc(540, 860, r, 0, 2 * pi); ctx.set_source_rgba(1, 1, 1, 0.25 * (0.3 + a) * (1 - k / 3)); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()
    for i in range(30):
        h_ = 8 + 160 * talkT("CAP") * abs(sin(i * 1.7 + CUR["t"] * 18))
        ctx.rectangle(160 + i * 25, 1270 - h_ / 2, 14, h_); ctx.set_source_rgb(1, 0.86, 0.15); ctx.fill()


def seat_map(stage="route"):
    """stage: route | off | circle | ocean | fuel"""
    def f(ctx, lt, d):
        ctx.set_source_rgb(0.02, 0.02, 0.03); ctx.paint()
        z = {"route": 1.0, "off": 1.25, "circle": 1.6, "ocean": 0.9, "fuel": 1.0}[stage]
        ctx.save(); cam(ctx, z * (1 + 0.05 * sm(lt / d)), 540 if stage != "fuel" else 760, 900 if stage != "fuel" else 1150)
        rrect(ctx, 80, 560, 920, 700, 24); fs(ctx, (0.05, 0.05, 0.06), 10)
        ctx.save(); rrect(ctx, 110, 590, 860, 640, 14); ctx.clip()
        ctx.set_source_rgb(0.05, 0.14, 0.32); ctx.paint()
        blob(ctx, [(150, 700, 220), (250, 900, 200), (180, 1100, 210)], (0.16, 0.36, 0.22))
        blob(ctx, [(900, 640, 140), (960, 760, 120)], (0.16, 0.36, 0.22))
        ctx.save(); ctx.set_dash([12, 10]); ctx.move_to(330, 1000); ctx.curve_to(500, 820, 700, 760, 900, 700); st(ctx, (1, 1, 1), 4); ctx.restore()
        ell(ctx, 900, 700, 10, 10); ctx.set_source_rgb(1, 0.86, 0.15); ctx.fill(); text(ctx, "DENVER", 900, 670, 30, col=(1, 1, 1))
        if stage == "route": px, py, ang = 600, 790, -0.35
        else:
            a_ = CUR["t"] * 0.9; px, py = 560 + 90 * cos(a_), 1010 + 70 * sin(a_); ang = a_ + pi / 2
        if stage in ("circle", "ocean", "off", "fuel"):
            ctx.save(); ctx.set_dash([6, 8]); ctx.new_path(); ctx.arc(560, 1010, 90, 0, 2 * pi); st(ctx, (1, 0.4, 0.3), 3); ctx.restore()
        ctx.save(); ctx.translate(px, py); ctx.rotate(ang); poly(ctx, [(22, 0), (-14, -12), (-8, 0), (-14, 12)]); fs(ctx, (1, 1, 1), 2); ctx.restore()
        if stage == "ocean": text(ctx, "ATLANTIC OCEAN", 560, 1140, 34, col=(0.6, 0.8, 1.0))
        rrect(ctx, 720, 1120, 230, 90, 12); ctx.set_source_rgba(0, 0, 0, 0.6); ctx.fill()
        text(ctx, "FUEL", 835, 1150, 22, col=(0.8, 0.8, 0.85)); text(ctx, "1:58", 835, 1195, 44, col=RED if stage == "fuel" else (1, 1, 1))
        ctx.restore(); ctx.restore()
    return f


def fuel_big(ctx, lt, d):
    ctx.set_source_rgb(0.02, 0.02, 0.03); ctx.paint()
    glow(ctx, 540, 900, 600, (1, 0.1, 0.05), 0.25)
    text(ctx, "FUEL", 540, 700, 90, col=(0.85, 0.85, 0.9))
    text(ctx, "1:58:00" if lt < 0.6 else f"1:57:{59 - int((lt - 0.6) * 4) % 60:02d}", 540, 960, 200, col=RED, stroke=14)
    ctx.rectangle(190, 1080, 700, 40); fs(ctx, (0.15, 0.15, 0.17), 3); ctx.rectangle(190, 1080, 700 * 0.3, 40); ctx.set_source_rgb(*RED); ctx.fill()


def keypad(ctx, lt, d):
    BG(ctx, "door_red", 14); overlay(ctx, (0, 0, 0), 0.4)
    ctx.save(); cam(ctx, 1.0 + 0.1 * sm(lt / d), 540, 900)
    rrect(ctx, 290, 520, 500, 760, 30); fs(ctx, (0.25, 0.26, 0.28), 8)
    rrect(ctx, 340, 570, 400, 130, 14); ctx.set_source_rgb(0.05, 0.0, 0.0); ctx.fill()
    flash = (lt * 3) % 1 < 0.6
    text(ctx, "DENIED" if lt > 0.4 else "* * * *", 540, 660, 64, col=RED if flash or lt < 0.4 else (0.4, 0.05, 0.05))
    for r in range(4):
        for c in range(3):
            rrect(ctx, 350 + c * 135, 740 + r * 130, 110, 105, 16); fs(ctx, (0.75, 0.76, 0.78), 4)
            text(ctx, "123456789*0#"[r * 3 + c], 405 + c * 135, 810 + r * 130, 50, col=(0.2, 0.2, 0.25))
    ctx.restore()


def name_tag_ins(ctx, lt, d):
    ctx.set_source_rgb(*NINA["top"]); ctx.paint()
    ctx.save(); cam(ctx, 1.0 + 0.1 * sm(lt / d), 540, 960)
    rrect(ctx, 260, 820, 560, 220, 20); fs(ctx, (0.85, 0.75, 0.35), 8)
    text(ctx, "NINA", 540, 960, 120, col=(0.15, 0.15, 0.2)); text(ctx, "CABIN CREW", 540, 1010, 30, col=(0.3, 0.25, 0.1))
    ctx.restore()


def newspaper(ctx, lt, d):
    BG(ctx, "front_red", 18); overlay(ctx, (0, 0, 0), 0.3)
    ctx.save(); cam(ctx, 1.0 + 0.12 * sm(lt / d), 540, 900); ctx.translate(540, 950); ctx.rotate(-0.05)
    ctx.rectangle(-420, -520, 840, 1040); fs(ctx, (0.92, 0.90, 0.84), 6)
    text(ctx, "THE DAILY POST", 0, -430, 60, col=(0.1, 0.1, 0.1))
    ctx.rectangle(-380, -400, 760, 6); ctx.set_source_rgb(0.1, 0.1, 0.1); ctx.fill()
    text(ctx, "GOLD HEIST:", 0, -300, 90, col=(0.1, 0.1, 0.1)); text(ctx, "$4M STILL", 0, -200, 90, col=(0.1, 0.1, 0.1)); text(ctx, "MISSING", 0, -100, 90, col=RED)
    ctx.rectangle(-380, -40, 360, 300); ctx.set_source_rgb(0.6, 0.6, 0.58); ctx.fill()
    for k in range(12): ctx.rectangle(20, -30 + k * 26, 360, 10); ctx.set_source_rgb(0.6, 0.6, 0.58); ctx.fill()
    ctx.restore()


def man_seat(smile=0.0):
    def f(ctx, lt, d):
        ctx.save(); cam(ctx, 1.0 + 0.08 * sm(lt / d), 540, 1000); BG(ctx, "front_red", 6)
        for i, x in enumerate((180, 900)):
            draw_char(ctx, PAX[i], dict(x=x, y=head_y(1.2, 1000), s=1.2, mood=M("scared"), look=0.3 if x < 540 else -0.3, tremble=0.5), CUR["t"])
        P = dict(x=560, y=head_y(1.4, 900), s=1.4, mood=M("cold", smile=smile), look=-0.1, lookY=0.8)
        P["armL"] = ik(P, 470, 1180, 1); P["armR"] = ik(P, 650, 1180, -1)
        draw_char(ctx, MAN, P, CUR["t"])
        ctx.save(); ctx.translate(560, 1180); ctx.rotate(0.05); ctx.rectangle(-170, -110, 340, 220); fs(ctx, (0.9, 0.88, 0.82), 4)
        text(ctx, "GOLD HEIST", 0, -50, 34, col=(0.1, 0.1, 0.1)); ctx.restore()
        ctx.restore()
        label(ctx, lt, 0.4, "seat 1A", 820, 560, 70, 0.06, (1, 0.86, 0.15))
    return f


def nina_walk(ctx, lt, d):
    u = sm(clamp(lt / d)); s = lerp(0.55, 1.7, u)
    draw_char(ctx, NINA, dict(x=540, y=head_y(s, lerp(760, 680, u)), s=s, legs=True, mood=M("scared"), tilt=0.04 * sin(lt * 9), tremble=0.6), CUR["t"])


def you_walk(ctx, lt, d):
    u = sm(clamp(lt / d)); s = lerp(1.6, 0.5, u)
    draw_char(ctx, YOU, dict(x=540, y=head_y(s, lerp(640, 790, u)), s=s, legs=True, mood=M("worried"), tilt=0.04 * sin(lt * 9)), CUR["t"])


def panic_row(ctx, lt, d):
    ctx.save(); cam(ctx, punch(lt) * (1 + 0.05 * sm(lt / d)), 540, 1000, dx=shake(lt, 4)[0]); BG(ctx, "row_red", 4)
    for i, (x, hy, s) in enumerate(((220, 900, 1.25), (560, 960, 1.15), (880, 920, 1.25))):
        draw_char(ctx, PAX[i + 2], dict(x=x, y=head_y(s, hy), s=s, mood=M("shock", mo=0.6 + 0.3 * sin(CUR["t"] * 9 + i)), look=0.6 - 0.6 * i, tremble=0.6), CUR["t"])
    ctx.restore()
    for k, (w, x, y) in enumerate((("WHAT?!", 240, 600), ("NO!", 820, 650), ("WHY?!", 520, 520))):
        pop_word(ctx, lt, 0.15 + k * 0.35, w, x, y, 90, col=(1, 1, 1), life=1.0)


def fuel_hud(start_min, end_min):
    """returns a HUD function with fuel counting down over the part"""
    def hud(ctx, sc, t):
        if sc not in FUEL_SCENES: return
        keys = list(TL); i = keys.index(sc); n = len(keys)
        m = lerp(start_min, end_min, (i + t / DUR(sc)) / n)
        rrect(ctx, 700, 200, 320, 76, 38); ctx.set_source_rgba(0, 0, 0, 0.6); ctx.fill()
        text(ctx, f"FUEL {int(m // 60)}:{int(m % 60):02d}", 860, 254, 38, col=RED if m < 45 else (1, 1, 1))
    return hud


def fuel_num(txt, sub="FUEL", col=None):
    def f(ctx, lt, d):
        ctx.set_source_rgb(0.02, 0.02, 0.03); ctx.paint(); glow(ctx, 540, 900, 600, (1, 0.1, 0.05), 0.25)
        text(ctx, sub, 540, 700, 90, col=(0.85, 0.85, 0.9))
        p = back_out(clamp(lt / 0.25)); ctx.save(); ctx.translate(540, 900); ctx.scale(p, p)
        text(ctx, txt, 0, 60, 220, col=col or RED, stroke=14); ctx.restore()
    return f


def door_crack(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.15 * sm(lt / d), 540, 900); BG(ctx, "door_red", 0)
    w_ = 6 + 30 * sm(clamp(lt / 0.8))
    ctx.rectangle(600 - w_ / 2, 560, w_, 760); ctx.set_source_rgb(0.75, 0.85, 1.0); ctx.fill()
    glow(ctx, 600, 940, 220 + 4 * w_, (0.6, 0.75, 1.0), 0.6)
    ctx.restore()


def cockpit_shot(captain=True, copilot=True, z=(1.0, 1.1), cx=540, cy=1000, green=False):
    def f(ctx, lt, d):
        ctx.save(); cam(ctx, lerp(z[0], z[1], sm(lt / d)), cx, cy); BG(ctx, "cockpit_grn" if green else "cockpit", 0)
        if copilot: draw_char(ctx, COPI, dict(x=820, y=head_y(1.3, 900), s=1.3, mood=M("sad", lid=1.0), blink=True, tilt=0.45, dark=0.2), CUR["t"])
        if captain: draw_char(ctx, CAPT, dict(x=280, y=head_y(1.3, 880), s=1.3, mood=M("worried"), look=0.6, glasses=False, dark=0.1), CUR["t"])
        ctx.restore()
    return f


def gear_panel(state="red"):
    def f(ctx, lt, d):
        ctx.set_source_rgb(0.08, 0.09, 0.11); ctx.paint()
        ctx.save(); cam(ctx, 1.0 + 0.1 * sm(lt / d), 540, 900)
        rrect(ctx, 200, 520, 680, 760, 30); fs(ctx, (0.16, 0.17, 0.20), 8)
        text(ctx, "LANDING GEAR", 540, 620, 54, col=(0.85, 0.85, 0.9))
        on = state == "green" or (lt * 2.5) % 1 < 0.6
        col = (0.2, 1, 0.35) if state == "green" else RED
        for k, x in enumerate((360, 540, 720)):
            ell(ctx, x, 820, 70, 70); ctx.set_source_rgb(*(col if on else shade(col, 0.7))); ctx.fill()
            if on: glow(ctx, x, 820, 200, col, 0.5)
        text(ctx, "DOWN" if state == "green" else "UNSAFE", 540, 1040, 110, col=col if on else shade(col, 0.6))
        rrect(ctx, 480, 1110, 120, 140, 20); fs(ctx, (0.75, 0.76, 0.78), 5)
        ctx.restore()
    return f


def pax_list(ctx, lt, d):
    def scr(c, lt_):
        c.set_source_rgb(0.95, 0.96, 0.98); c.paint()
        c.rectangle(-160, -310, 320, 60); c.set_source_rgb(0.12, 0.2, 0.45); c.fill(); text(c, "PASSENGER LIST", 0, -272, 20, col=(1, 1, 1))
        rows = [("13A", "Miller, J."), ("13C", "Okafor, D."), ("14A", "Chen, L."), ("14C", "YOU"), ("15B", "Rossi, M.")]
        for i, (s_, n_) in enumerate(rows):
            y = -200 + i * 70; hl = s_ == "14C"
            if hl: c.rectangle(-150, y - 30, 300, 60); c.set_source_rgb(1, 0.92, 0.5); c.fill()
            text(c, s_, -130, y + 8, 22, col=(0.2, 0.2, 0.3), align="l"); text(c, n_, -40, y + 8, 22, col=(0.2, 0.2, 0.3), align="l")
        if lt_ > 0.5: text(c, "Occupation:", -130, 190, 18, col=(0.4, 0.4, 0.45), align="l", weight=False); text(c, "Aircraft mechanic", -130, 225, 24, col=RED, align="l")
    phone(ctx, 540, 960, 2.1, 0.03, scr, lt, 0.2)


def belly(ctx, lt, d):
    ctx.set_source_rgb(0.05, 0.06, 0.10); ctx.paint()
    ctx.rectangle(-50, 1250, 1180, 700); ctx.set_source_rgb(0.12, 0.12, 0.14); ctx.fill()
    x = lerp(-200, 560, sm(clamp(lt / 1.2)))
    ctx.save(); ctx.translate(x, 1180); ctx.rotate(0.04)
    ell(ctx, 0, 0, 420, 70); ctx.set_source_rgb(0.62, 0.64, 0.70); ctx.fill()
    poly(ctx, [(-40, 10), (120, 10), (-160, 200), (-260, 200)]); ctx.set_source_rgb(0.52, 0.54, 0.60); ctx.fill()
    ctx.restore()
    rs = random.Random(int(lt * 20))
    for k in range(30):
        sx = x - 300 + rs.uniform(-80, 80); sy = 1250 + rs.uniform(-30, 10)
        ctx.move_to(sx, sy); ctx.line_to(sx - rs.uniform(60, 200), sy - rs.uniform(0, 80)); st(ctx, (1, 0.7, 0.2), 4)
    glow(ctx, x - 300, 1240, 300, (1, 0.6, 0.2), 0.5)
    ctx.move_to(200, 600); ctx.line_to(880, 1000); ctx.move_to(880, 600); ctx.line_to(200, 1000)
    label(ctx, lt, 0.6, "no wheels = no chance", 540, 560, 64, -0.04, RED)


def hatch_ins(state="closed"):
    def f(ctx, lt, d):
        ctx.set_source_rgb(0.12, 0.12, 0.14); ctx.paint()
        ctx.save(); cam(ctx, 1.0 + 0.1 * sm(lt / d), 540, 960)
        rrect(ctx, 240, 640, 600, 600, 20); fs(ctx, (0.38, 0.39, 0.42), 8)
        if state == "open":
            u = sm(clamp(lt / 0.6)); ctx.rectangle(270, 670, 540, 540 * u); ctx.set_source_rgb(0.02, 0.02, 0.03); ctx.fill()
        if state == "jammed":
            rrect(ctx, 600, 900, 260, 60, 10); fs(ctx, (0.25, 0.18, 0.12), 5)
            rrect(ctx, 760, 885, 70, 90, 8); fs(ctx, (0.8, 0.75, 0.6), 5)
            label(ctx, lt, 0.3, "belt in the latch", 540, 560, 60, -0.04, RED)
        rrect(ctx, 470, 1120, 140, 50, 20); fs(ctx, (0.75, 0.6, 0.15), 5)
        text(ctx, "EQUIPMENT BAY", 540, 760, 44, col=(0.9, 0.9, 0.85))
        ctx.restore()
    return f


def hatch_from_below(slam_t=0.3):
    def f(ctx, lt, d):
        ctx.set_source_rgb(0.02, 0.02, 0.03); ctx.paint()
        open_ = 1 - sm(clamp((lt - slam_t) / 0.15))
        ctx.rectangle(290, 300, 500, 380 * open_); ctx.set_source_rgb(0.9, 0.85, 0.75); ctx.fill()
        if open_ > 0: glow(ctx, 540, 450, 500, (1, 0.9, 0.7), 0.6 * open_)
        for k in range(8): ctx.rectangle(470, 700 + k * 140, 140, 18); fs(ctx, (0.35, 0.35, 0.38), 3)
        ctx.move_to(470, 700); ctx.line_to(470, 1900); ctx.move_to(610, 700); ctx.line_to(610, 1900); st(ctx, (0.35, 0.35, 0.38), 14)
        if lt > slam_t: pop_word(ctx, lt, slam_t, "SLAM", 540, 560, 140, col=(1, 1, 1), rot=-0.08, life=1.0)
    return f


def lock_ins(ctx, lt, d):
    ctx.set_source_rgb(0.30, 0.31, 0.34); ctx.paint()
    ell(ctx, 540, 900, 220, 220); fs(ctx, (0.65, 0.62, 0.50), 10)
    ctx.save(); ctx.translate(540, 900); ctx.rotate(-pi / 2 * sm(clamp((lt - 0.3) / 0.4)))
    rrect(ctx, -40, -170, 80, 340, 30); fs(ctx, (0.85, 0.80, 0.60), 6); ctx.restore()
    if lt > 0.65: pop_word(ctx, lt, 0.65, "CLICK", 540, 1300, 110, col=(1, 1, 1), life=1.2)


def bay_shot(you=True, flash=False, z=(1.0, 1.08), mood=None, look=0.6, amp=0, ladder=False):
    def f(ctx, lt, d):
        dx, dy = shake(lt, amp)
        ctx.save(); cam(ctx, lerp(z[0], z[1], sm(lt / d)), 540, 1000, dx=dx, dy=dy); BG(ctx, "bay", 0)
        if you:
            P = dict(x=360 if not ladder else 420, y=head_y(1.5, lerp(500, 860, sm(clamp(lt / d))) if ladder else 860), s=1.5, legs=True, mood=mood or M("worried"), look=look, tremble=0.4)
            P["armR"] = ik(P, P["x"] + 220, 1000, -1)
            draw_char(ctx, YOU, P, CUR["t"])
            hx, hy = head_world(P); breath(ctx, CUR["t"], hx - 30, hy + 80, s=1.2)
        ctx.restore()
        if flash:
            g = cairo.RadialGradient(lerp(300, 760, sm(clamp(lt / 1.2))), 1100, 40, lerp(300, 760, sm(clamp(lt / 1.2))), 1100, 420)
            g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.88)
            ctx.set_source(g); ctx.paint()
    return f


def lever_ins(jam=False, snap_t=None, handle=False):
    def f(ctx, lt, d):
        ctx.set_source_rgb(0.10, 0.10, 0.12); ctx.paint()
        dx, dy = shake(lt, 10) if snap_t is not None and snap_t <= lt < snap_t + 0.4 else (0, 0)
        ctx.save(); ctx.translate(dx, dy); cam(ctx, 1.0 + 0.08 * sm(lt / d), 540, 960)
        rrect(ctx, 200, 700, 680, 700, 30); fs(ctx, (0.42, 0.43, 0.46), 8)
        text(ctx, "MANUAL GEAR RELEASE", 540, 790, 40, col=(1, 0.8, 0.2))
        ang = -0.9 if snap_t is not None and lt > snap_t else 0.0
        ctx.save(); ctx.translate(380, 1050); ctx.rotate(ang); rrect(ctx, 0, -30, 360, 60, 30); fs(ctx, (0.95, 0.65, 0.10), 6); ctx.restore()
        if jam:
            rrect(ctx, 560, 1100, 300, 200, 16); fs(ctx, (0.78, 0.80, 0.84), 6)
            for x in (600, 820): rrect(ctx, x - 20, 1180, 40, 40, 6); fs(ctx, (0.5, 0.5, 0.52), 3)
        if handle:
            ctx.save(); ctx.translate(560, 1080); ctx.rotate(-0.4); rrect(ctx, -20, -20, 300, 40, 18); fs(ctx, (0.75, 0.76, 0.80), 5); ctx.restore()
        ctx.restore()
        if snap_t is not None and lt > snap_t:
            if lt < snap_t + 0.12: overlay(ctx, (1, 1, 1), 0.6, ADD)
            pop_word(ctx, lt, snap_t, "SNAP!", 540, 560, 140, col=(1, 1, 1), life=1.2)
    return f


def case_ins(stage="front"):
    def f(ctx, lt, d):
        ctx.set_source_rgb(0.06, 0.06, 0.08); ctx.paint()
        ctx.save(); cam(ctx, 1.0 + 0.1 * sm(lt / d), 540, 960)
        if stage == "turn": ctx.translate(540, 960); ctx.scale(cos(lt * 3) if lt < 0.5 else 1, 1); ctx.translate(-540, -960)
        rrect(ctx, 200, 720, 680, 480, 30); fs(ctx, (0.80, 0.82, 0.86), 8)
        ctx.rectangle(200, 940, 680, 12); ctx.set_source_rgb(0.6, 0.62, 0.66); ctx.fill()
        for x in (300, 780): rrect(ctx, x - 30, 920, 60, 60, 8); fs(ctx, (0.45, 0.45, 0.48), 4)
        rrect(ctx, 470, 640, 140, 90, 30); st(ctx, (0.45, 0.45, 0.48), 18)
        if stage in ("tag", "turn") and lt > 0.4:
            ctx.save(); ctx.translate(760, 760); ctx.rotate(0.25); rrect(ctx, -90, -50, 180, 220, 16); fs(ctx, (1, 0.95, 0.7), 5)
            text(ctx, "SEAT", 0, 30, 34, col=(0.3, 0.3, 0.35)); text(ctx, "1A", 0, 120, 90, col=RED); ctx.restore()
        if stage == "gold":
            rrect(ctx, 220, 740, 640, 200, 20); ctx.set_source_rgb(0.25, 0.2, 0.1); ctx.fill()
            for k in range(6): rrect(ctx, 250 + k * 100, 980, 80, 160, 10); fs(ctx, (1, 0.8, 0.2), 4)
            glow(ctx, 540, 1060, 400, (1, 0.8, 0.3), 0.6)
        ctx.restore()
    return f


def gear_drop(ctx, lt, d):
    ctx.set_source_rgb(0.03, 0.04, 0.10); ctx.paint()
    ctx.save(); ctx.translate(540, 760); ctx.rotate(0.03)
    ell(ctx, 0, 0, 520, 140); ctx.set_source_rgb(0.55, 0.57, 0.62); ctx.fill()
    u = sm(clamp(lt / 0.5))
    for x in (-220, 220):
        ctx.save(); ctx.translate(x, 100); ctx.rotate(-1.4 * (1 - u))
        rrect(ctx, -18, 0, 36, 320, 12); fs(ctx, (0.35, 0.36, 0.40), 4)
        ell(ctx, 0, 330, 70, 70); fs(ctx, (0.08, 0.08, 0.09), 6); ell(ctx, 0, 330, 30, 30); ctx.set_source_rgb(0.5, 0.5, 0.52); ctx.fill()
        ctx.restore()
    ctx.restore()
    if lt > 0.45: pop_word(ctx, lt, 0.45, "CLUNK", 540, 1450, 140, col=(1, 1, 1), life=1.2)


def tackle(ctx, lt, d):
    ctx.save(); cam(ctx, punch(lt) * (1 + 0.06 * sm(lt / d)), 540, 1000, dx=shake(lt, 6)[0]); BG(ctx, "front_red", 4)
    for i, x in enumerate((140, 340, 760, 960)):
        P = dict(x=x + (lerp(0, 120 if x < 540 else -120, sm(clamp(lt / 0.8)))), y=head_y(1.25, 900), s=1.25, legs=True, mood=M("angry"), look=1 if x < 540 else -1)
        draw_char(ctx, PAX[i], P, CUR["t"])
    draw_char(ctx, MAN, dict(x=550, y=head_y(1.35, 860 + 60 * sm(clamp((lt - 0.6) / 0.5))), s=1.35, legs=True, mood=M("shock"), tilt=0.3 * sm(clamp((lt - 0.6) / 0.5))), CUR["t"])
    ctx.restore()


def nina_pull(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.06 * sm(lt / d), 540, 1000); BG(ctx, "front_red", 6)
    N_ = dict(x=460, y=head_y(1.5, 820), s=1.5, mood=M("worried"), lookY=0.8)
    N_["armL"] = ik(N_, 520, 1300, 1); N_["armR"] = ik(N_, 600, 1300, -1)
    draw_char(ctx, NINA, N_, CUR["t"])
    u = sm(clamp(lt / d))
    draw_char(ctx, YOU, dict(x=600, y=head_y(1.5, lerp(1500, 1150, u)), s=1.5, mood=M("worried", flush=0.6), lookY=-0.7, armL=("ik", -40, -500, 1)), CUR["t"])
    rrect(ctx, 200, 1500, 680, 60, 10); fs(ctx, (0.38, 0.39, 0.42), 6)
    ctx.restore()


def police(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.06 * sm(lt / d), 540, 1000); BG(ctx, "aisle_night", 8)
    for x in (260, 820):
        draw_char(ctx, dict(skin=(0.8, 0.62, 0.5), hair=(0.1, 0.08, 0.06), hairstyle="crew", outfit="uniform", top=(0.12, 0.15, 0.30), seed=160 + x), dict(x=x, y=head_y(1.4, 860), s=1.4, legs=True, mood=M("cold"), look=0.2 if x < 540 else -0.2), CUR["t"])
    draw_char(ctx, MAN, dict(x=540, y=head_y(1.3, 920), s=1.3, legs=True, mood=M("sad"), lookY=0.6, armL=("ik", 30, -200, 1), armR=("ik", -30, -200, -1)), CUR["t"])
    ctx.restore()
    label(ctx, lt, 0.3, "POLICE", 540, 560, 90, -0.04, (0.4, 0.7, 1))
