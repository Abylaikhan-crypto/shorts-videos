exec(open(f"{HERE}/hor_common.py").read())
HEADER = ["THE LAST TRAIN", "FULL STORY"]
END_T = LE("j", 0) + 0.3
HOOK = [("YOU WAKE UP", (1, 1, 1)), ("ON AN EMPTY", (1, 1, 1)), ("TRAIN", (1, 0.86, 0.15))]
WORKER = dict(skin=(0.70, 0.50, 0.38), hair=(0.10, 0.08, 0.07), hairstyle="crew", outfit="hoodie", top=(1.0, 0.55, 0.10), seed=130, beard=True)
COLS_EXTRA = {"N": (1, 1, 1), "W": (1, 0.7, 0.3)}


def car(ctx):
    room(ctx, back=(400, 640, 280, 560), wall=(0.70, 0.72, 0.74), floor=(0.35, 0.36, 0.38), ceil=(0.82, 0.84, 0.86), side=(0.60, 0.62, 0.64), plank=False)
    ctx.rectangle(450, 700, 180, 440); fs(ctx, (0.45, 0.47, 0.50), 5); ctx.rectangle(490, 740, 100, 160); ctx.set_source_rgb(0.05, 0.05, 0.07); ctx.fill()
    for side in (-1, 1):   # windows (black tunnel) and benches along both walls
        for k in range(3):
            f0, f1 = k / 3, (k + 0.8) / 3
            def P(f, yy):
                x = lerp(-400 if side < 0 else 1480, 400 if side < 0 else 680, f ** 0.6)
                yb = lerp(yy, 640 + (yy - 0) * 0.29, f ** 0.6)
                return x, yb
            poly(ctx, [P(f0, 420), P(f1, 420), P(f1, 980), P(f0, 980)]); fs(ctx, (0.04, 0.04, 0.06), 6)
        poly(ctx, [(-400 if side < 0 else 1480, 1500), (400 if side < 0 else 680, 1140), (400 if side < 0 else 680, 1100), (-400 if side < 0 else 1480, 1300)])
        fs(ctx, (0.15, 0.35, 0.65), 6)
    for x in (180, 900):
        ctx.move_to(x, -100); ctx.line_to(x, 2100); st(ctx, (0.85, 0.80, 0.55), 22)
    for k in range(5):
        y = 200 + k * 90; w_ = 420 - k * 70
        ctx.rectangle(540 - w_ / 2, y, w_, 18 - 3 * k); ctx.set_source_rgb(1, 1, 0.95); ctx.fill()


def seats_side(ctx):
    ctx.set_source_rgb(0.68, 0.70, 0.72); ctx.paint()
    for k in range(3):
        ctx.rectangle(60 + k * 340, 420, 300, 420); fs(ctx, (0.04, 0.04, 0.06), 8)
    ctx.rectangle(-50, 1150, 1180, 120); fs(ctx, (0.15, 0.35, 0.65), 6)
    ctx.rectangle(-50, 1000, 1180, 160); fs(ctx, (0.18, 0.40, 0.70), 6)
    for k in range(4): ctx.move_to(130 + k * 280, 1000); ctx.line_to(130 + k * 280, 1270); st(ctx, (0.10, 0.25, 0.50), 5)
    ctx.rectangle(-50, 1270, 1180, 700); ctx.set_source_rgb(0.35, 0.36, 0.38); ctx.fill()
    ctx.move_to(540, -100); ctx.line_to(540, 2100); st(ctx, (0.85, 0.80, 0.55), 22)


def cab(ctx):
    ctx.set_source_rgb(0.12, 0.13, 0.16); ctx.paint()
    poly(ctx, [(60, 380), (1020, 380), (960, 1060), (120, 1060)]); ctx.set_source_rgb(0.01, 0.01, 0.02); ctx.fill()
    poly(ctx, [(500, 700), (580, 700), (900, 1060), (180, 1060)]); ctx.set_source_rgb(0.08, 0.08, 0.09); ctx.fill()
    for sx in (-1, 1):
        ctx.move_to(540 + sx * 12, 700); ctx.line_to(540 + sx * 260, 1060); st(ctx, (0.6, 0.6, 0.65), 6)
    poly(ctx, [(60, 380), (1020, 380), (960, 1060), (120, 1060)]); st(ctx, (0.25, 0.26, 0.30), 26)
    poly(ctx, [(-50, 1060), (1130, 1060), (1130, 1500), (-50, 1500)]); fs(ctx, (0.20, 0.21, 0.25), 6)
    for i, (x, c) in enumerate(((220, (1, 0.2, 0.2)), (330, (0.2, 1, 0.4)), (440, (1, 0.8, 0.2)))):
        ell(ctx, x, 1150, 22, 22); ctx.set_source_rgb(*c); ctx.fill()
    rrect(ctx, 600, 1110, 300, 160, 14); ctx.set_source_rgb(0.05, 0.12, 0.10); ctx.fill(); text(ctx, "AUTO", 750, 1210, 60, col=(0.3, 1, 0.5))
    rrect(ctx, 380, 1500, 320, 420, 40); fs(ctx, (0.25, 0.18, 0.15), 6)   # empty seat
    rrect(ctx, 400, 1300, 280, 240, 40); fs(ctx, (0.30, 0.22, 0.18), 6)


def depot(ctx):
    g = cairo.LinearGradient(0, 0, 0, 1200); g.add_color_stop_rgb(0, 0.03, 0.03, 0.06); g.add_color_stop_rgb(1, 0.18, 0.12, 0.10); ctx.set_source(g); ctx.paint()
    for row, (y, s) in enumerate(((900, 0.5), (1080, 0.75), (1320, 1.0))):
        for k in range(-1, 4):
            x = k * 560 * s + row * 140
            rrect(ctx, x, y - 260 * s, 520 * s, 240 * s, 30 * s); fs(ctx, (0.62, 0.64, 0.68), 4)
            for j in range(4): rrect(ctx, x + 30 * s + j * 120 * s, y - 220 * s, 90 * s, 90 * s, 8 * s); ctx.set_source_rgb(0.06, 0.06, 0.08); ctx.fill()
            ctx.rectangle(x, y - 70 * s, 520 * s, 22 * s); ctx.set_source_rgb(0.15, 0.35, 0.65); ctx.fill()
    ctx.rectangle(-100, 1340, 1300, 700); ctx.set_source_rgb(0.12, 0.10, 0.09); ctx.fill()
    for x in (180, 880):
        ctx.rectangle(x - 10, 380, 20, 960); ctx.set_source_rgb(0.08, 0.08, 0.09); ctx.fill()
        rrect(ctx, x - 60, 370, 120, 30, 8); ctx.set_source_rgb(1, 0.75, 0.4); ctx.fill()
    rrect(ctx, 360, 300, 360, 90, 10); fs(ctx, (0.9, 0.9, 0.85), 4); text(ctx, "DEPOT 4", 540, 362, 48, col=(0.2, 0.2, 0.2))


SETS.update({"car": car, "seats_side": seats_side, "cab": cab, "depot": depot})


def car_wide(sleep=False, you=True, z=(1.0, 1.08), walk=None):
    def f(ctx, lt, d):
        ctx.save(); cam(ctx, punch(lt, 0.03) * lerp(z[0], z[1], sm(lt / d)), 540, 1000); BG(ctx, "car", 0)
        if walk:
            u = sm(clamp(lt / d)); s = lerp(0.55, 1.6, u)
            draw_char(ctx, YOU, dict(x=540, y=head_y(s, lerp(820, 700, u)), s=s, legs=True, mood=M("worried"), look=0.0, tilt=0.04 * sin(lt * 8)), CUR["t"])
        elif you:
            P = dict(x=230, y=head_y(1.25, 900), s=1.25, mood=M("sad", lid=1.0) if sleep else M("shock"), blink=sleep, tilt=0.35 if sleep else 0, look=0.5)
            draw_char(ctx, YOU, P, CUR["t"])
        ctx.restore()
    return f


def seats_pan(ctx, lt, d):
    ctx.save(); ctx.translate(-200 * sm(lt / d), 0); cam(ctx, 1.15, 540, 1000); BG(ctx, "seats_side", 0); ctx.restore()
    label(ctx, lt, 0.4, "empty", 540, 560, 80, -0.05, (1, 1, 1))


def led_screen(blank_t=99):
    def f(ctx, lt, d):
        ctx.set_source_rgb(0.05, 0.05, 0.07); ctx.paint()
        ctx.save(); cam(ctx, 1.0 + 0.1 * sm(lt / d), 540, 900)
        rrect(ctx, 60, 650, 960, 420, 20); fs(ctx, (0.15, 0.15, 0.17), 8)
        rrect(ctx, 100, 690, 880, 340, 10); ctx.set_source_rgb(0.02, 0.01, 0.0); ctx.fill()
        for yy in range(700, 1030, 14):
            for xx in range(110, 980, 14): ell(ctx, xx, yy, 2.5, 2.5); ctx.set_source_rgba(1, 0.5, 0.1, 0.10); ctx.fill()
        text(ctx, "NEXT STOP:", 540, 830, 96, col=(1, 0.55, 0.12))
        if lt < blank_t:
            n = int(clamp((lt - 0.4) / 0.08, 0, 7)); text(ctx, "MAPLE ST"[:n], 540, 960, 96, col=(1, 0.55, 0.12))
        elif (lt * 2) % 1 < 0.6:
            ctx.rectangle(330, 950, 420, 14); ctx.set_source_rgb(1, 0.55, 0.12); ctx.fill()
        ctx.restore()
    return f


def phone_nosig(ctx, lt):
    ctx.set_source_rgb(0.10, 0.11, 0.14); ctx.paint()
    for k in range(4): ctx.rectangle(-60 + k * 30, -40 - k * 14, 20, 20 + k * 14); ctx.set_source_rgb(0.35, 0.35, 0.4); ctx.fill()
    ctx.move_to(-80, -110); ctx.line_to(60, 0); st(ctx, RED, 8)
    text(ctx, "No Service", 0, 90, 34, col=(1, 1, 1))
    text(ctx, "SOS only", 0, 140, 24, col=(0.7, 0.7, 0.75), weight=False)


def speed_window(ctx, lt, d):
    dx, dy = shake(lt, 6)
    ctx.save(); ctx.translate(dx, dy)
    BG(ctx, "seats_side", 0)
    for k in range(3):
        ctx.save(); ctx.rectangle(60 + k * 340, 420, 300, 420); ctx.clip()
        off = (lt * 2600) % 900
        for j in range(4):
            x = 60 + k * 340 + 400 - off + j * 300 - 300
            ctx.rectangle(x, 560 + 60 * (j % 2), 260, 14); ctx.set_source_rgba(1, 0.85, 0.5, 0.9); ctx.fill()
        ctx.restore()
    ctx.restore()
    speed_lines(ctx, lt, horiz=True, a=0.25, n=26)
    label(ctx, lt, 0.3, "too fast", 540, 1560, 90, -0.05, RED)


def cab_door(open_t=99):
    def f(ctx, lt, d):
        ctx.set_source_rgb(0.55, 0.57, 0.60); ctx.paint()
        ctx.save(); cam(ctx, 1.0 + 0.06 * sm(lt / d), 540, 960)
        ctx.rectangle(260, 320, 560, 1300); ctx.set_source_rgb(0.02, 0.02, 0.03); ctx.fill()
        op = sm(clamp((lt - open_t) / 0.6)) if lt > open_t else 0
        w_ = 560 * (1 - 0.85 * op)
        poly(ctx, [(260, 320), (260 + w_, 320 - 40 * op), (260 + w_, 1620 + 40 * op), (260, 1620)]); fs(ctx, (0.45, 0.47, 0.50), 6)
        if op < 0.5:
            rrect(ctx, 380, 420, 320, 200, 10); ctx.set_source_rgb(0.05, 0.05, 0.07); ctx.fill()
            rrect(ctx, 380, 700, 320, 80, 8); ctx.set_source_rgb(0.9, 0.15, 0.15); ctx.fill(); text(ctx, "DRIVER ONLY", 540, 755, 40, col=(1, 1, 1))
        ctx.restore()
    return f


def cab_empty(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.12 * sm(lt / d), 540, 1000); BG(ctx, "cab", 0)
    ctx.save(); poly(ctx, [(60, 380), (1020, 380), (960, 1060), (120, 1060)]); ctx.clip()
    for k in range(6):
        u = ((lt * 1.6 + k / 6) % 1) ** 2
        for sx in (-1, 1):
            x = 540 + sx * lerp(20, 600, u); y = lerp(700, 1100, u)
            ell(ctx, x, y, lerp(3, 40, u), lerp(2, 16, u)); ctx.set_source_rgb(1, 0.85, 0.5); ctx.fill()
    ctx.restore(); ctx.restore()
    label(ctx, lt, 0.2, "NOBODY", 540, 560, 110, -0.04, RED)


def cab_slow(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.06 * sm(lt / d), 540, 1000); BG(ctx, "cab", 0)
    ctx.save(); poly(ctx, [(60, 380), (1020, 380), (960, 1060), (120, 1060)]); ctx.clip()
    for k in range(6):
        u = ((lt * 0.5 + k / 6) % 1) ** 2
        for sx in (-1, 1):
            x = 540 + sx * lerp(20, 600, u); y = lerp(700, 1100, u)
            ell(ctx, x, y, lerp(3, 40, u), lerp(2, 16, u)); ctx.set_source_rgb(1, 0.6, 0.25); ctx.fill()
    glow(ctx, 540, 700, 300 + 200 * sm(lt / d), (1, 0.6, 0.25), 0.5)
    ctx.restore(); ctx.restore()


def depot_pan(z=(1.0, 1.1), pan=0, lab=None):
    def f(ctx, lt, d):
        ctx.save(); ctx.translate(-pan * sm(lt / d), 0); cam(ctx, lerp(z[0], z[1], sm(lt / d)), 540, 1000); BG(ctx, "depot", 0); ctx.restore()
        if lab: label(ctx, lt, 0.2, lab, 540, 560, 90, -0.04, (1, 0.7, 0.3))
    return f


def worker_window(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.08 * sm(lt / d), 540, 960)
    BG(ctx, "depot", 10)
    sh = shake(lt, 8) if (lt % 0.6) < 0.1 and lt < 1.5 else (0, 0)
    P = dict(x=560 + sh[0], y=head_y(1.6, 780), s=1.6, mood=M("smirk", smile=0.5), look=-0.2)
    P["armL"] = ik(P, 380, 700, 1)
    draw_char(ctx, WORKER, P, CUR["t"])
    rrect(ctx, 720, 980, 120, 60, 14); fs(ctx, (0.15, 0.15, 0.17), 4); glow(ctx, 790, 1000, 260, (1, 1, 0.9), 0.7)
    ctx.restore()
    ctx.set_source_rgb(0.62, 0.64, 0.68)   # window frame, we are inside the train
    ctx.rectangle(0, 0, 1080, 300); ctx.rectangle(0, 1500, 1080, 420); ctx.rectangle(0, 0, 90, 1920); ctx.rectangle(990, 0, 90, 1920); ctx.fill()


LIGHT_CAR = lambda t: dict(amb=(0.55, 0.60, 0.75), bloom=0.7, thr=0.62, vig=0.6, haze=0.08,
                           lights=[(540, 250, 650, 380, (0.55, 0.65, 0.85), 0.6),
                                   ((t * 1100) % 2400 - 600, 900, 260, 1100, (1.0, 0.8, 0.5), 0.9 * flick(t, 7))])


def LIGHT(sc, t):
    if sc in "abdf": return LIGHT_CAR(t)
    if sc == "c": return dict(amb=(0.35, 0.30, 0.30), bloom=1.0, thr=0.45, vig=0.6, haze=0.2, lights=[(540, 900, 600, 300, (1, 0.55, 0.2), 1.1)])
    if sc == "e": return dict(amb=(0.6, 0.6, 0.7), bloom=0.5, thr=0.6, vig=0.6, lights=[(540, 900, 600, 700, (0.6, 0.7, 1), 0.5)])
    if sc == "g": return dict(amb=(0.35, 0.40, 0.55), bloom=1.0, thr=0.5, vig=0.6, haze=0.15, lights=[(540, 760, 420, 300, (0.9, 0.95, 1), 1.2), (220, 1150, 200, 150, (1, 0.2, 0.2), 0.7)])
    if sc == "h": return dict(amb=(0.40, 0.32, 0.32), bloom=1.0, thr=0.5, vig=0.6, haze=0.18, lights=[(180, 420, 360, 500, (1, 0.6, 0.25), 1.3), (880, 420, 360, 500, (1, 0.6, 0.25), 1.3), (540, 760, 500, 300, (1, 0.6, 0.25), 0.6)])
    if sc == "i": return dict(amb=(0.38, 0.33, 0.38), bloom=1.0, thr=0.55, vig=0.55, haze=0.15, lights=[(790, 1000, 320, 320, (1, 1, 0.9), 1.4), (150, 500, 400, 600, (1, 0.6, 0.25), 1.0)])
    if sc == "j": return dict(amb=(0.45, 0.38, 0.38), bloom=0.8, thr=0.55, vig=0.55, lights=[(180, 420, 360, 500, (1, 0.6, 0.25), 1.1), (880, 420, 360, 500, (1, 0.6, 0.25), 1.1)])
    return None


SHOTS = {
    "a": SC("a", [], [car_wide(sleep=True)]),
    "b": SC("b", ["the", "every"], [you_ecu(lambda lt: M("sad", lid=0.98) if lt < 0.25 else M("shock", eo=1.5), "car"), car_wide(you=False, z=(1.0, 1.2)), seats_pan]),
    "c": SC("c", ["and", "just"], [led_screen(), led_screen(blank_t=0.0), you_ecu(M("worried"), "car", lookY=-0.6)]),
    "d": SC("d", ["and"], [phone_ins(phone_nosig, bg="car"), speed_window]),
    "e": SC("e", [], [options_card([("A", "Pull the brake"), ("B", "Walk to the driver"), ("C", "Wait")], [T("e", "pull"), T("e", "walk"), T("e", "or")], pick=1, pick_t=T("e", "wait") + 0.3)]),
    "f": SC("f", [("you", 0, 1), "it"], [car_wide(walk=True), cab_door(), cab_door(open_t=0.05)]),
    "g": SC("g", [], [cab_empty]),
    "h": SC("h", ["orange", "rows", ("a", 0, 0)], [cab_slow, depot_pan(z=(1.3, 1.15)), depot_pan(pan=160, z=(1.2, 1.2)), depot_pan(z=(1.0, 1.08), lab="DEPOT")]),
    "i": SC("i", [("fell", 1), ("at", 1)], [worker_window,
                                            ECU(WORKER, M("smirk", smile=0.6), "depot", "W"),
                                            ECU(YOU, M("worried", flush=0.8, smile=0.2), "car", post=L("...oh.", 0.3, 540, 560, 90))]),
    "j": SC("j", [END_T - 0.4], [depot_pan(z=(1.0, 1.05)),
                                 END("THE END", [("Would YOU pull the brake?", 50, (1, 0.86, 0.15)), ("Follow Paper & Plot", 46, (1, 1, 1)), ("This story is fiction.", 34, (0.8, 0.8, 0.8))], END_T,
                                     base=depot_pan(z=(1.05, 1.05)))]),
}
