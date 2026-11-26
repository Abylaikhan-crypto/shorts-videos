exec(open(f"{HERE}/hor_common.py").read())
HEADER = ["DAD'S FRIDAY SECRET", "FULL STORY"]
END_T = LE("i", 0) + 0.3
HOOK = [("MY DAD LIED", (1, 1, 1)), ("EVERY", (1, 1, 1)), ("FRIDAY", (1, 0.86, 0.15))]
TEEN = dict(skin=(0.96, 0.82, 0.70), hair=(0.40, 0.24, 0.14), hairstyle="long", outfit="hoodie", top=(0.85, 0.40, 0.45), seed=95, blush=True, freckles=True)
BABY = dict(skin=(0.98, 0.86, 0.77), hair=(0.85, 0.55, 0.25), hairstyle="crew", outfit="hoodie", top=(1, 0.72, 0.82), seed=96, blush=True)
DADF = dict(DAD, outfit="cardigan", top=(0.35, 0.40, 0.48), no_lanyard=True)


def street_night(ctx):
    g = cairo.LinearGradient(0, 0, 0, 1300); g.add_color_stop_rgb(0, 0.03, 0.04, 0.12); g.add_color_stop_rgb(1, 0.14, 0.14, 0.28); ctx.set_source(g); ctx.paint()
    for i, (x, h_) in enumerate(((-40, 520), (300, 600), (660, 480), (960, 560))):
        ctx.rectangle(x, 1300 - h_, 330, h_ + 20); fs(ctx, (0.14, 0.13, 0.18), 5)
        poly(ctx, [(x - 20, 1300 - h_), (x + 165, 1300 - h_ - 160), (x + 350, 1300 - h_)]); fs(ctx, (0.10, 0.09, 0.12), 5)
        for k in range(2):
            ctx.rectangle(x + 50 + k * 150, 1300 - h_ + 80, 80, 90); ctx.set_source_rgb(*((1, 0.85, 0.5) if (i + k) % 2 else (0.08, 0.08, 0.12))); ctx.fill()
    ctx.rectangle(-100, 1300, 1300, 800); ctx.set_source_rgb(0.20, 0.20, 0.24); ctx.fill()
    ctx.rectangle(-100, 1300, 1300, 40); ctx.set_source_rgb(0.45, 0.45, 0.48); ctx.fill()
    for x in (200, 880):
        ctx.rectangle(x - 8, 700, 16, 620); ctx.set_source_rgb(0.15, 0.15, 0.18); ctx.fill()
        ell(ctx, x, 700, 36, 18); ctx.set_source_rgb(1, 0.9, 0.6); ctx.fill(); glow(ctx, x, 760, 320, (1, 0.8, 0.45), 0.4)


def center_ext(ctx):
    g = cairo.LinearGradient(0, 0, 0, 1300); g.add_color_stop_rgb(0, 0.04, 0.05, 0.14); g.add_color_stop_rgb(1, 0.16, 0.16, 0.30); ctx.set_source(g); ctx.paint()
    ctx.rectangle(120, 520, 840, 900); fs(ctx, (0.55, 0.30, 0.24), 6)
    for r in range(2):
        for c in range(4):
            ctx.rectangle(170 + c * 200, 700 + r * 260, 130, 160); ctx.set_source_rgb(1, 0.85, 0.5); ctx.fill()
    rrect(ctx, 240, 560, 600, 100, 14); fs(ctx, (0.95, 0.93, 0.85), 5); text(ctx, "COMMUNITY CENTER", 540, 625, 48, col=(0.3, 0.2, 0.2))
    ctx.rectangle(470, 1180, 140, 240); fs(ctx, (0.30, 0.20, 0.15), 5)
    ctx.rectangle(-100, 1420, 1300, 700); ctx.set_source_rgb(0.20, 0.20, 0.24); ctx.fill()
    glow(ctx, 540, 1180, 400, (1, 0.8, 0.45), 0.3)


def classroom_l(ctx):
    room(ctx, back=(140, 520, 800, 640), wall=(0.92, 0.88, 0.78), floor=(0.62, 0.55, 0.45), ceil=(0.95, 0.94, 0.90), side=(0.85, 0.80, 0.70), plank=False)
    rrect(ctx, 260, 580, 560, 260, 10); fs(ctx, (1, 1, 1), 6)
    text(ctx, "SIGN LANGUAGE", 540, 680, 52, col=(0.2, 0.3, 0.6)); text(ctx, "BEGINNERS", 540, 760, 44, col=(0.85, 0.2, 0.2))
    glow(ctx, 540, 400, 600, (1, 1, 0.9), 0.3)


def party(ctx):
    dining_big(ctx)
    for x, c in ((200, (0.95, 0.4, 0.5)), (330, (0.4, 0.7, 1)), (760, (1, 0.85, 0.3)), (880, (0.5, 0.9, 0.5))):
        ctx.move_to(x, 900); ctx.line_to(x + 10, 1100); st(ctx, (0.9, 0.9, 0.9), 3)
        ell(ctx, x, 840, 55, 68); fs(ctx, c, 4)
    rrect(ctx, 330, 600, 420, 90, 12); fs(ctx, (1, 0.85, 0.9), 4); text(ctx, "HAPPY 1ST", 540, 662, 50, col=(0.85, 0.3, 0.45))


SETS.update({"street_night": street_night, "center_ext": center_ext, "classroom_l": classroom_l, "party": party})


def dad_leaving(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.06 * sm(lt / d), 540, 980); BG(ctx, "entry", 0)
    draw_door(ctx, open_=0.25, under=0)
    P = dict(x=700, y=head_y(1.5, 840), s=1.5, legs=True, mood=M("smirk", smile=0.3), look=0.6, dark=0.15)
    P["armR"] = ("ang", 2.6, 3.1 + 0.3 * sin(lt * 8))
    draw_char(ctx, DADF, P, CUR["t"]); rrect(ctx, 520, 1330, 120, 90, 10); fs(ctx, (0.25, 0.2, 0.18), 5)
    ctx.restore()
    label(ctx, lt, 2.25, "\"working late\"", 540, 560, 76, -0.05, (1, 0.86, 0.15))


def hours_sign(ctx, lt, d):
    ctx.set_source_rgb(0.25, 0.28, 0.35); ctx.paint()
    ctx.save(); ctx.translate(540, 900); ctx.rotate(-0.03)
    rrect(ctx, -360, -300, 720, 600, 20); fs(ctx, (0.96, 0.96, 0.94), 7)
    text(ctx, "OFFICE HOURS", 0, -190, 64, col=(0.2, 0.2, 0.3))
    text(ctx, "MON - FRI", 0, -60, 56, col=(0.4, 0.4, 0.45)); text(ctx, "9:00 - 5:00", 0, 60, 90, col=(0.2, 0.2, 0.3))
    ctx.restore()
    if lt > 0.5:
        p = back_out(clamp((lt - 0.5) / 0.2)); ctx.save(); ctx.translate(560, 960); ctx.scale(p, p); ctx.new_path(); ctx.arc(0, 0, 250, 0, 2 * pi); st(ctx, RED, 14); ctx.restore()


def follow(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.08 * sm(lt / d), 540, 1150); BG(ctx, "street_night", 0)
    x = lerp(620, 820, lt / d)
    draw_char(ctx, DADF, dict(x=x, y=1420, s=0.75, legs=True, mood="neutral", look=1, dark=0.5), CUR["t"])
    ctx.restore()
    draw_char(ctx, TEEN, dict(x=200, y=head_y(1.9, 1000), s=1.9, mood=M("worried"), look=1, dark=0.45), CUR["t"])
    rrect(ctx, -60, 900, 200, 1100, 30); fs(ctx, (0.10, 0.08, 0.07), 0)   # tree trunk in foreground
    blob(ctx, [(40, 760, 260), (220, 700, 200)], (0.05, 0.10, 0.06))


def dad_enters(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.1 * sm(lt / d), 540, 1150); BG(ctx, "center_ext", 0)
    u = sm(clamp(lt / d)); draw_char(ctx, DADF, dict(x=lerp(800, 560, u), y=1440, s=0.75, legs=True, mood="neutral", look=-1, dark=0.4), CUR["t"])
    ctx.restore()


def door12(ctx, lt, d):
    ctx.set_source_rgb(0.80, 0.76, 0.66); ctx.paint()
    rrect(ctx, 240, 300, 600, 1400, 10); fs(ctx, (0.45, 0.32, 0.22), 7)
    ctx.rectangle(390, 420, 300, 300); fs(ctx, (1, 0.95, 0.8), 6)
    text(ctx, "12", 540, 400, 90, col=(1, 1, 1), stroke=10)
    ctx.save(); ctx.translate(540, 900); ctx.rotate(0.04); ctx.rectangle(-210, -120, 420, 240); fs(ctx, (1, 1, 1), 4)
    text(ctx, "Tuesday & Friday", 0, -40, 34, col=(0.3, 0.3, 0.35), weight=False); text(ctx, "6:00 PM", 0, 30, 60, col=(0.2, 0.2, 0.3)); ctx.restore()
    ell(ctx, 790, 1050, 22, 22); fs(ctx, (0.85, 0.7, 0.3), 4)


def window_class(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.1 * sm(lt / d), 540, 1000); BG(ctx, "classroom_l", 0)
    for i, (ch, x) in enumerate(((dict(MOM, hair=(0.25, 0.18, 0.12), freckles=False, seed=120), 180), (dict(GRANDPA, seed=121), 380), (DADF, 600), (dict(KAREN, seed=122), 840))):
        ph = sin(CUR["t"] * 5 + i)
        P = dict(x=x, y=head_y(1.0, 1000), s=1.0, mood=M("worried") if ch is DADF else "happy", look=0.2)
        P["armR"] = ik(P, x + 70, 1010 + 30 * ph, -1); P["armL"] = ik(P, x - 60, 1030 - 30 * ph, 1)
        if ch is DADF: P["sweat"] = True
        draw_char(ctx, ch, P, CUR["t"])
    ctx.restore()
    ctx.set_source_rgb(0.10, 0.09, 0.12)   # window frame (we look from outside)
    ctx.rectangle(0, 0, 1080, 380); ctx.rectangle(0, 1480, 1080, 440); ctx.rectangle(0, 0, 80, 1920); ctx.rectangle(1000, 0, 80, 1920); ctx.fill()
    ctx.move_to(540, 380); ctx.line_to(540, 1480); st(ctx, (0.10, 0.09, 0.12), 22)


def ily_hand(ctx, lt, d):
    ctx.set_source_rgb(0.95, 0.85, 0.70); ctx.paint(); glow(ctx, 540, 900, 700, (1, 0.9, 0.7), 0.4)
    p = back_out(clamp(lt / 0.35))
    ctx.save(); ctx.translate(540, 1100); ctx.scale(p, p)
    sk = DADF["skin"]
    rrect(ctx, -110, 260, 220, 700, 70); fs(ctx, DADF["top"], 8)
    rrect(ctx, -150, -60, 300, 360, 110); fs(ctx, sk, 8)
    rrect(ctx, -150, -470, 80, 440, 40); fs(ctx, sk, 8)    # pinky
    rrect(ctx, 60, -560, 86, 530, 43); fs(ctx, sk, 8)       # index
    ctx.save(); ctx.translate(140, 60); ctx.rotate(1.05); rrect(ctx, -42, -330, 84, 340, 42); fs(ctx, sk, 8); ctx.restore()   # thumb
    for k, x in enumerate((-55, -5)): rrect(ctx, x, -120, 70, 150, 35); fs(ctx, shade(sk, 0.08), 6)   # folded fingers
    ctx.restore()
    label(ctx, lt, 0.4, "I LOVE YOU", 540, 500, 110, -0.04, (1, 0.35, 0.5))


def baby_ecu(mood, lab=None, tilt=0.0, laugh=False):
    def f(ctx, lt, d):
        ctx.save(); cam(ctx, punch(lt) * (1 + 0.1 * sm(lt / d)), 540, 960); BG(ctx, "party", 16)
        tl = tilt * sm(clamp(lt / 0.8)) if laugh else 0
        draw_char(ctx, BABY, dict(x=540, y=head_y(2.6, 900), s=2.6, mood=mood, tilt=tl + 0.05 * sin(CUR["t"] * 9) * laugh), CUR["t"])
        rrect(ctx, 120, 1420, 840, 600, 40); fs(ctx, (0.98, 0.82, 0.88), 7)   # high chair tray
        ctx.restore()
        if lab: lab(ctx, lt, d)
    return f


def deaf_icon(ctx, lt, d):
    if lt < 0.3: return
    p = back_out(clamp((lt - 0.3) / 0.25)); ctx.save(); ctx.translate(840, 520); ctx.scale(p, p)
    ell(ctx, 0, 0, 90, 90); fs(ctx, (1, 1, 1), 6)
    ctx.new_path(); ctx.arc(5, -10, 40, pi, 2.4 * pi); st(ctx, OUTL, 12)
    ctx.move_to(-60, -60); ctx.line_to(60, 60); st(ctx, RED, 14); ctx.restore()
    label(ctx, lt, 0.5, "born deaf", 540, 1560, 80, -0.04, (1, 1, 1))


def dad_baby(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.06 * sm(lt / d), 540, 1000); BG(ctx, "living", 6)
    P = dict(x=330, y=head_y(1.6, 860), s=1.6, mood=M("worried", smile=0.1), look=0.8, sweat=True)
    P["armR"] = ik(P, 520, 1060 + 30 * sin(lt * 6), -1)
    draw_char(ctx, DADF, P, CUR["t"])
    draw_char(ctx, BABY, dict(x=780, y=head_y(1.1, 1150), s=1.1, mood=M("worried"), look=-0.6), CUR["t"])
    ctx.restore()
    label(ctx, lt, 0.3, "...?", 780, 760, 90, 0.1)


def party_wide(ctx, lt, d):
    ctx.save(); cam(ctx, punch(lt, 0.04) * (1 + 0.06 * sm(lt / d)), 540, 1060); BG(ctx, "party", 4)
    for ch, x, s, hy, m in ((MOM, 220, 1.05, 960, "happy"), (TEEN, 420, 1.0, 975, "happy"), (DADF, 860, 1.1, 950, M("worried", smile=0.2))):
        draw_char(ctx, ch, dict(x=x, y=head_y(s, hy), s=s, mood=m, look=0.2), CUR["t"])
    draw_char(ctx, BABY, dict(x=630, y=head_y(0.85, 1080), s=0.85, mood="joy"), CUR["t"])
    table_fg(ctx, 1320)
    rrect(ctx, 560, 1240, 160, 90, 14); fs(ctx, (1, 0.8, 0.85), 5); ctx.rectangle(636, 1180, 8, 60); ctx.set_source_rgb(0.5, 0.7, 1); ctx.fill()
    ell(ctx, 640, 1170, 9, 15); ctx.set_source_rgb(1, 0.8, 0.2); ctx.fill(); glow(ctx, 640, 1170, 70, (1, 0.8, 0.3), 0.6)
    ctx.restore()


def dad_kneel(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.1 * sm(lt / d), 540, 1050); BG(ctx, "party", 8)
    u = sm(clamp(lt / 0.8))
    draw_char(ctx, DADF, dict(x=360, y=head_y(1.5, lerp(820, 1000, u)), s=1.5, mood=M("hopeful", smile=0.2), look=0.8), CUR["t"])
    draw_char(ctx, BABY, dict(x=780, y=head_y(1.1, 1060), s=1.1, mood="neutral", look=-0.7), CUR["t"])
    rrect(ctx, 640, 1230, 280, 70, 20); fs(ctx, (0.95, 0.95, 0.98), 6)
    ctx.restore()


def family_end(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.05 * sm(lt / d), 540, 1000); BG(ctx, "party", 6)
    for ch, x, s, hy, m in ((MOM, 200, 1.4, 880, M("joy", tear=0.5)), (DADF, 420, 1.45, 870, M("joy", tear=0.3)), (TEEN, 860, 1.35, 890, "joy")):
        draw_char(ctx, ch, dict(x=x, y=head_y(s, hy), s=s, mood=m), CUR["t"])
    draw_char(ctx, BABY, dict(x=640, y=head_y(1.0, 1080), s=1.0, mood="joy", tilt=0.1 * sin(CUR["t"] * 6)), CUR["t"])
    ctx.restore()
    for k in range(4): V.sparkle(ctx, 200 + k * 230, 520 + 60 * sin(k), CUR["t"], k * 0.3)


SHOTS = {
    "a": SC("a", ["but"], [dad_leaving, INS(hours_sign)]),
    "b": SC("b", ["i"], [ECU(MOM, M("crying"), "kitchen_h", dark=0.2),
                        MED([(TEEN, 760, 900, 1.5, M("worried"), None, dict(look=-1, dark=0.45))], "hall", blur=0)]),
    "c": SC("c", [], [follow]),
    "d": SC("d", ["went", "room"], [ECU(TEEN, M("cold", eo=0.8), "street_night", dark=0.3, look=0.6), dad_enters, INS(door12)], whips=(1,)),
    "e": SC("e", ["a", "sign", "beginners"], [ECU(TEEN, M("shock"), "center_ext", dark=0.2, post=lambda c, lt, d: glow(c, 540, 1000, 500, (1, 0.85, 0.5), 0.2)),
                                             window_class, INS(window_class, z=(1.5, 1.7), cy=700),
                                             INS(window_class, z=(1.6, 1.8), cy=1080, post=L("Dad?!", 0.1, 760, 560, 90, 0.08, (1, 0.86, 0.15)))]),
    "f": SC("f", ["dad", "mom"], [baby_ecu(M("neutral"), lab=deaf_icon), dad_baby, ECU(MOM, M("sad", tear=0.4), "living", dark=0.1)]),
    "g": SC("g", ["dad", "signed"], [party_wide, dad_kneel, ECU(DADF, M("hopeful", tear=0.3), "party", z=(1.0, 1.15))]),
    "h": SC("h", [("lily", 1), ("and", 1)], [INS(ily_hand), baby_ecu(M("joy", mo=0.8), tilt=0.5, laugh=True),
                                              ECU(MOM, M("joy", tear=0.9), "party")]),
    "i": SC("i", [END_T - 0.4], [family_end,
                                 END("THE END", [("Would YOU have followed him?", 48, (1, 0.86, 0.15)), ("Follow Paper & Plot", 46, (1, 1, 1)), ("This story is fiction.", 34, (0.8, 0.8, 0.8))], END_T, base=family_end)]),
}
