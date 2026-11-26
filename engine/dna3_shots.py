HEADER = ["MY DNA TEST WAS WRONG", "FINAL PART"]
END_T = LE("j", 1) + 0.3


def swap_walk(ctx, lt, d):
    g = cairo.LinearGradient(0, 0, 0, 1300); g.add_color_stop_rgb(0, 0.55, 0.75, 0.95); g.add_color_stop_rgb(1, 0.85, 0.92, 1.0); ctx.set_source(g); ctx.paint()
    for i in range(7): ctx.rectangle(-50 + i * 170, 700 - (i % 3) * 120, 150, 700); fs(ctx, [(0.85, 0.75, 0.65), (0.7, 0.75, 0.85), (0.9, 0.85, 0.7)][i % 3], 5)
    ctx.rectangle(-100, 1400, 1300, 600); ctx.set_source_rgb(0.65, 0.65, 0.68); ctx.fill()
    u = sm(clamp(lt / d))
    for ch, x0, x1, col in ((RUBY, 150, 930, (0.3, 0.5, 0.85)), (HANNAH, 930, 150, (0.9, 0.5, 0.6))):
        x = lerp(x0, x1, u)
        P = dict(x=x, y=1600, s=1.1, legs=True, mood=M("worried"), look=1 if x1 > x0 else -1)
        P["armR" if x1 > x0 else "armL"] = ik(P, x + (110 if x1 > x0 else -110), 1430, -1 if x1 > x0 else 1)
        draw_char(ctx, ch, P, CUR["t"]); suitcase(ctx, x + (130 if x1 > x0 else -130), 1490, 0.45, col)
    label(ctx, lt, 0.3, "swap", 540, 520, 90, -0.06, (1, 0.86, 0.15))


def room_with(bg, ch, col, mood):
    def f(ctx, lt, d):
        ctx.save(); cam(ctx, 1.0 + 0.06 * sm(lt / d), 540, 1080); BG(ctx, bg, 4)
        draw_char(ctx, ch, dict(x=470, y=head_y(1.5, 900), s=1.5, legs=True, mood=mood, look=0.3), CUR["t"])
        suitcase(ctx, 780, 1500, 0.8, col)
        ctx.restore()
    return f


def zoom_on(bg, cx, cy, z, word, wx, wy, amp=0):
    def f(ctx, lt, d):
        dx, dy = shake(lt, amp)
        ctx.save(); cam(ctx, z * (1 + 0.05 * sm(lt / d)), cx, cy, dx=dx, dy=dy); BG(ctx, bg, 0); ctx.restore()
        pop_word(ctx, lt, 0.1, word, wx, wy, 110, col=(1, 1, 1), life=1.0)
    return f


def breakfast(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.06 * sm(lt / d), 540, 1060); BG(ctx, "karen_apt", 4)
    P = dict(x=330, y=head_y(1.45, 880), s=1.45, mood=M("happy"), look=0.6)
    P["armR"] = ik(P, 520, 1180, -1)
    draw_char(ctx, KAREN, P, CUR["t"])
    draw_char(ctx, RUBY, dict(x=800, y=head_y(1.35, 940), s=1.35, mood=M("hopeful", smile=0.5), look=-0.6), CUR["t"])
    table_fg(ctx, 1320, (0.60, 0.48, 0.35))
    ell(ctx, 560, 1290, 110, 30); fs(ctx, (0.3, 0.3, 0.32), 5); ctx.move_to(660, 1290); ctx.line_to(760, 1270); st(ctx, (0.2, 0.2, 0.22), 14)
    ctx.restore()


def doodles(ctx, lt, d):
    ctx.set_source_rgb(0.60, 0.48, 0.35); ctx.paint()
    for i, (x, r) in enumerate(((330, -0.1), (750, 0.08))):
        ctx.save(); ctx.translate(x, 980); ctx.rotate(r)
        ctx.rectangle(-210, -210, 420, 420); fs(ctx, (1, 1, 1), 5)
        p = clamp((lt - i * 0.3) / 1.0)
        ctx.new_path(); ctx.arc(0, -20, 90, 0, 2 * pi * p); st(ctx, (0.2, 0.3, 0.7), 6)
        if p > 0.5:
            for sx in (-1, 1): ell(ctx, sx * 30, -40, 10, 14); ctx.set_source_rgb(0.2, 0.3, 0.7); ctx.fill()
            ctx.new_path(); ctx.arc(0, -10, 45, 0.3, pi - 0.3); st(ctx, (0.2, 0.3, 0.7), 6)
        if p > 0.9:
            star(ctx, 120, -140, 30); st(ctx, (0.2, 0.3, 0.7), 5)
        ctx.restore()
    label(ctx, lt, 1.0, "same doodle!", 540, 520, 76, -0.05, (1, 0.86, 0.15))


def fridge_zoom(focus, z, cx=540, cy=960):
    def f(ctx, lt, d):
        ctx.save(); cam(ctx, z * (1 + 0.06 * sm(lt / d)), cx, cy); fridge_cu(ctx, lt, focus); ctx.restore()
    return f


def bed_phone(ch, bg):
    def f(ctx, lt, d):
        ctx.save(); cam(ctx, 1.0 + 0.08 * sm(lt / d), 540, 1050); BG(ctx, bg, 6)
        P = dict(x=540, y=head_y(1.6, 930), s=1.6, mood=M("hopeful", smile=0.3), lookY=0.7, dark=0.35)
        P["armL"] = ik(P, 500, 1230, 1); P["armR"] = ik(P, 590, 1235, -1)
        draw_char(ctx, ch, P, CUR["t"])
        rrect(ctx, 490, 1150, 110, 170, 14); fs(ctx, (0.12, 0.12, 0.14), 4); glow(ctx, 545, 1100, 420, (0.6, 0.8, 1), 0.35)
        blanket(ctx, 1330, (0.35, 0.40, 0.65))
        ctx.restore()
    return f


def bridge_walk(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.05 * sm(lt / d), 540, 1150); BG(ctx, "bridge", 0)
    u = sm(clamp(lt / d))
    for ch, x0, x1 in ((RUBY, -80, 400), (HANNAH, 1160, 690)):
        x = lerp(x0, x1, u)
        draw_char(ctx, ch, dict(x=x, y=1640, s=0.95, legs=True, mood=M("worried"), look=1 if x1 > x0 else -1, dark=0.3), CUR["t"])
    ctx.restore()


def girls_two(mR, mH, spkR=None, spkH=None, sparkle=False):
    def f(ctx, lt, d):
        ctx.save(); cam(ctx, punch(lt, 0.04) * (1.0 + 0.08 * sm(lt / d)), 540, 1000); BG(ctx, "bridge", 8)
        draw_char(ctx, RUBY, dict(x=330, y=head_y(1.7, 860), s=1.7, mood=mR, look=0.8, mouth=talkT(spkR) if spkR else 0, dark=0.15), CUR["t"])
        draw_char(ctx, HANNAH, dict(x=760, y=head_y(1.7, 860), s=1.7, mood=mH, look=-0.8, mouth=talkT(spkH) if spkH else 0, dark=0.15), CUR["t"])
        ctx.restore()
        if sparkle:
            for k in range(5): V.sparkle(ctx, 200 + k * 170, 560 + 80 * sin(k * 2), CUR["t"], k * 0.3)
    return f


def big_dinner(ctx, lt, d):
    ctx.save(); cam(ctx, punch(lt, 0.04) * (1.0 + 0.06 * sm(lt / d)), 540, 1060); BG(ctx, "dining_big", 4)
    for ch, x, s, hy, m in ((KAREN, 110, 0.95, 1000, "joy"), (MOM, 270, 0.97, 990, "happy"), (DAD, 430, 1.0, 985, "joy"), (SAM, 580, 0.78, 1060, "joy"),
                            (RUBY, 740, 0.95, 1000, "happy"), (HANNAH, 930, 0.95, 1000, "joy")):
        draw_char(ctx, ch, dict(x=x, y=head_y(s, hy), s=s, mood=m, tilt=0.04 * sin(CUR["t"] * 3 + x)), CUR["t"])
    table_fg(ctx, 1300, (0.55, 0.36, 0.24))
    for x, c in ((220, (0.85, 0.5, 0.3)), (540, (0.9, 0.75, 0.3)), (860, (0.4, 0.7, 0.35))):
        ell(ctx, x, 1340, 110, 36); fs(ctx, (1, 1, 1), 4); blob(ctx, [(x - 30, 1320, 40), (x + 25, 1315, 45)], c)
    ctx.restore()
    label(ctx, lt, 0.2, "Sunday", 540, 520, 90, -0.05, (1, 0.86, 0.15))


def pancake_squeeze(ctx, lt, d):
    ctx.save(); cam(ctx, punch(lt, 0.04) * (1.0 + 0.06 * sm(lt / d)), 540, 1060); BG(ctx, "karen_apt", 4)
    for ch, x, s, hy, m in ((DAD, 150, 1.0, 960, "joy"), (MOM, 320, 0.98, 975, "happy"), (KAREN, 500, 1.0, 965, "joy"), (SAM, 650, 0.8, 1060, "joy"),
                            (RUBY, 800, 0.96, 985, "joy"), (HANNAH, 960, 0.96, 985, "happy")):
        draw_char(ctx, ch, dict(x=x, y=head_y(s, hy), s=s, mood=m, tilt=0.05 * sin(CUR["t"] * 3 + x)), CUR["t"])
    table_fg(ctx, 1320, (0.60, 0.48, 0.35))
    for x in (260, 540, 820):
        ctx.save(); ctx.translate(x, 1345); ctx.scale(0.6, 0.4)
        ctx.move_to(0, 70); ctx.curve_to(-140, -10, -70, -110, 0, -40); ctx.curve_to(70, -110, 140, -10, 0, 70); fs(ctx, (0.92, 0.70, 0.35), 6); ctx.restore()
    ctx.restore()
    label(ctx, lt, 0.2, "Wednesday", 540, 520, 90, -0.05, (1, 0.86, 0.15))


def sam_hug(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.08 * sm(lt / d), 540, 1000); BG(ctx, "dining_big", 10)
    R = dict(x=280, y=head_y(1.5, 830), s=1.5, mood="joy", tilt=0.1); H = dict(x=800, y=head_y(1.5, 830), s=1.5, mood="joy", tilt=-0.1)
    R["armR"] = ik(R, 520, 1150, -1); H["armL"] = ik(H, 560, 1150, 1)
    draw_char(ctx, RUBY, R, CUR["t"]); draw_char(ctx, HANNAH, H, CUR["t"])
    S_ = dict(x=540, y=head_y(1.4, 960), s=1.4, mood=M("joy", mo=0.4))
    S_["armL"] = ik(S_, 330, 1150, 1); S_["armR"] = ik(S_, 750, 1150, -1)
    draw_char(ctx, SAM, S_, CUR["t"])
    ctx.restore()
    for k in range(4):
        u = ((lt * 0.6 + k / 4) % 1)
        ctx.save(); ctx.translate(300 + k * 160, 760 - 300 * u); ctx.scale(1.3, 1.3)
        ctx.move_to(0, 18); ctx.curve_to(-40, -10, -18, -38, 0, -16); ctx.curve_to(18, -38, 40, -10, 0, 18); ctx.set_source_rgba(1, 0.35, 0.45, 1 - u); ctx.fill(); ctx.restore()


def kit_single(ctx, lt, d):
    ctx.set_source_rgb(0.18, 0.15, 0.22); ctx.paint(); glow(ctx, 540, 960, 600, (0.6, 0.9, 0.9), 0.25)
    ctx.save(); ctx.translate(540, 960); ctx.rotate(-0.06)
    rrect(ctx, -260, -300, 520, 600, 24); fs(ctx, (0.12, 0.55, 0.55), 7)
    text(ctx, "HELIX", 0, -120, 80, col=(1, 1, 1)); text(ctx, "DNA KIT", 0, -40, 50, col=(1, 1, 1))
    text(ctx, "Find out who", 0, 120, 40, col=(0.85, 1, 1), weight=False); text(ctx, "you really are", 0, 175, 40, col=(0.85, 1, 1), weight=False)
    ctx.restore()


def new_photo(ctx, lt, d):
    ctx.set_source_rgb(0.80, 0.62, 0.46); ctx.paint(); glow(ctx, 540, 900, 700, (1, 0.85, 0.6), 0.35)
    ctx.save(); ctx.translate(540, 900); ctx.rotate(0.02)
    family_photo(ctx, people=[(KAREN, -300, 0.62, -60), (DAD, -180, 0.66, -80), (MOM, -55, 0.64, -70), (RUBY, 70, 0.62, -50), (HANNAH, 190, 0.62, -50), (SAM, 310, 0.52, 0)])
    ctx.restore()
    for k in range(3): V.sparkle(ctx, 200 + k * 340, 520, CUR["t"], k * 0.4)


SHOTS = {
    "a": SC("a", ["just", "hannah", ("i", 0, 0)], [
        swap_walk,
        INS(lambda c, lt, d: (c.save(), c.translate(540, 900), c.rotate(0.05), calendar_card(c, lt, "ONE", "WEEK"), c.restore()), bg="ruby_room", blur=18),
        room_with("ruby_room", HANNAH, (0.9, 0.5, 0.6), M("worried")),
        room_with("tiny_room", RUBY, (0.3, 0.5, 0.85), M("worried")),
    ]),
    "b": SC("b", [("the", 0, 0), ("the", 0, 1), "but", "pancakes"], [
        INS(lambda c, lt, d: BG(c, "karen_apt", 0), post=L("tiny", 0.2, 540, 520, 90, -0.05)),
        zoom_on("karen_apt", 460, 1130, 2.6, "RATTLE!", 540, 700, amp=6),
        zoom_on("karen_apt", 830, 990, 2.2, "HMMMMM", 540, 640),
        breakfast,
        INS(lambda c, lt, d: pancakes(c, lt)),
    ]),
    "c": SC("c", [("and", 0, 0), "snorted", "wait", "my"], [
        ECU(RUBY, M("smirk", smile=0.6), "karen_apt"),
        ECU(KAREN, M("joy", mo=0.5), "karen_apt", amp=3),
        ECU(KAREN, M("joy", mo=0.2, eyes="x"), "karen_apt", amp=8, post=lambda c, lt, d: pop_word(c, lt, 0.05, "SNORT!", 540, 560, 120, life=1.2)),
        ECU(KAREN, M("shock", smile=0.5), "karen_apt", "KA"),
        ECU(RUBY, M("joy", mo=0.4), "karen_apt", "RU", amp=3),
    ]),
    "d": SC("d", [("the", 0, 1), ("the", 0, 2), "for"], [
        INS(lambda c, lt, d: hands_match(c, lt), post=L("same hands", 0.4, 540, 520, 80, -0.05, (1, 0.86, 0.15))),
        MED([(KAREN, 320, 880, 1.6, M("joy", mo=0.4), None), (RUBY, 770, 890, 1.55, M("joy", mo=0.4), None)], "karen_apt", blur=8, amp=2),
        INS(doodles),
        ECU(RUBY, M("hopeful", tear=0.4, smile=0.5), "karen_apt"),
    ]),
    "e": SC("e", [("her", 0, 0), ("her", 0, 1), ("her", 0, 2), "that", "complicated"], [
        fridge_zoom(None, 0.9),
        fridge_zoom(None, 1.6, 540, 700),
        fridge_zoom("medals", 1.3, 540, 830),
        fridge_zoom("teeth", 1.3, 540, 950),
        ECU(RUBY, M("sad", smile=-0.1), "karen_apt_night", dark=0.1),
        MED([(KAREN, 540, 900, 1.6, M("sad", tear=0.5), None, dict(lookY=0.7, dark=0.2, armL=("ik", 40, -150, 1), armR=("ik", -40, -150, -1)))], "karen_apt_night", blur=8,
            fx=lambda c, lt, d: (c.save(), c.translate(540, 1240), c.rotate(-0.1), c.rectangle(-90, -70, 180, 140), fs(c, (1, 1, 1), 4),
                                 c.rectangle(-75, -55, 150, 110), c.set_source_rgb(0.6, 0.8, 0.9), c.fill(), c.restore())),
    ]),
    "f": SC("f", [("your", 1, 0), ("mom", 1, 1)], [
        bed_phone(RUBY, "tiny_room"),
        PHONE(scr_chat([("Your mom makes the best lasagna", False, 0.05), ("Your dad's jokes are terrible", False, WT("f", "your", 1, 1) - WT("f", "your", 1, 0)),
                        ("...I miss my mom.", False, WT("f", "i", 1, 0) - WT("f", "your", 1, 0))], "Hannah"), bg="tiny_room"),
        ECU(HANNAH, M("crying"), "ruby_room_night", dark=0.15, post=lambda c, lt, d: glow(c, 540, 1150, 500, (0.6, 0.8, 1), 0.25)),
    ]),
    "g": SC("g", [("on", 0, 1), ("i", 1, 0), ("i", 2, 0)], [
        bridge_walk,
        girls_two(M("worried"), M("cold")),
        ECU(HANNAH, M("sad", tear=0.5), "bridge", "HA", dark=0.15),
        ECU(RUBY, M("sad", tear=0.6), "bridge", "RU", dark=0.15),
    ]),
    "h": SC("h", ["nobody"], [
        ECU(HANNAH, M("hopeful", tear=0.4, smile=0.4), "bridge", "HA", dark=0.1),
        girls_two(M("joy", tear=0.3), M("joy", tear=0.3), spkH="HA", sparkle=True),
    ]),
    "i": SC("i", ["wednesday", ("and", 1, 0), "because"], [
        big_dinner,
        pancake_squeeze,
        ECU(SAM, M("joy", mo=0.3), "dining_big", s=2.9, post=L("2 sisters!", 0.3, 540, 520, 90, -0.06, (1, 0.86, 0.15))),
        sam_hug,
    ]),
    "j": SC("j", ["instead", END_T - 0.4], [
        INS(kit_single),
        INS(new_photo, z=(1.0, 1.1), post=L("Both places.", WT("j", "both", 1) - WT("j", "instead") + 0.05, 540, 1220, 80, -0.04, (1, 0.86, 0.15))),
        END("THE END", [("Would YOU want to know?", 52, (1, 0.86, 0.15)), ("Follow Paper & Plot", 46, (1, 1, 1)), ("This story is fiction.", 34, (0.8, 0.8, 0.8))], END_T,
            base=INS(new_photo, z=(1.1, 1.12))),
    ]),
}

HOOK = [('TWO GIRLS.', (1, 1, 1)), ('ONE LIFE.', (1, 0.86, 0.15)), ('WHO STAYS?', (1, 1, 1))]
