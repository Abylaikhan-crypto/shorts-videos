HEADER = ["MY DNA TEST WAS WRONG", "PART 1"]
END_T = LE("l", 0) + 0.3


def kit_boxes(ctx, lt, d):
    ctx.set_source_rgb(0.55, 0.36, 0.24); ctx.paint(); glow(ctx, 540, 900, 700, (1, 0.8, 0.5), 0.3)
    for i, (x, y, r) in enumerate(((330, 820, -0.1), (750, 800, 0.08), (340, 1180, 0.06), (760, 1190, -0.07))):
        p = back_out(clamp((lt - i * 0.12) / 0.25))
        if p <= 0: continue
        ctx.save(); ctx.translate(x, y); ctx.rotate(r); ctx.scale(p, p)
        rrect(ctx, -160, -150, 320, 300, 18); fs(ctx, (0.12, 0.55, 0.55), 6)
        ctx.rectangle(-20, -150, 40, 300); ctx.rectangle(-160, -20, 320, 40); ctx.set_source_rgb(0.9, 0.15, 0.2); ctx.fill()
        text(ctx, "HELIX", 0, -60, 40, col=(1, 1, 1)); text(ctx, "DNA KIT", 0, 90, 30, col=(1, 1, 1))
        ctx.restore()


def tubes(ctx, lt, d):
    ctx.set_source_rgb(0.92, 0.88, 0.80); ctx.paint(); glow(ctx, 540, 800, 600, (1, 0.9, 0.7), 0.3)
    for i, (n, ch) in enumerate((("DAD", DAD), ("MOM", MOM), ("SAM", SAM), ("RUBY", RUBY))):
        x = 200 + i * 225; p = back_out(clamp((lt - i * 0.1) / 0.25))
        ctx.save(); ctx.translate(x, 1050); ctx.scale(p, p)
        rrect(ctx, -45, -300, 90, 420, 40); fs(ctx, (0.92, 0.96, 1.0), 6)
        rrect(ctx, -45, -10, 90, 130, 40); ctx.set_source_rgba(0.85, 0.9, 0.95, 1); ctx.fill()
        rrect(ctx, -55, -370, 110, 90, 18); fs(ctx, (0.12, 0.55, 0.55), 5)
        rrect(ctx, -70, 160, 140, 60, 10); fs(ctx, (1, 1, 1), 3); text(ctx, n, 0, 202, 30, col=(0.2, 0.2, 0.3))
        ctx.restore()


def popcorn(ctx, lt, d):
    ctx.set_source_rgb(0.25, 0.2, 0.3); ctx.paint(); glow(ctx, 540, 900, 600, (1, 0.8, 0.5), 0.3)
    poly(ctx, [(260, 900), (820, 900), (740, 1500), (340, 1500)]); fs(ctx, (1, 1, 1), 7)
    for k in range(5): poly(ctx, [(300 + k * 110, 900), (350 + k * 110, 900), (330 + k * 90, 1500), (300 + k * 90, 1500)]); ctx.set_source_rgb(0.9, 0.15, 0.2); ctx.fill()
    rs = random.Random(2)
    for k in range(40):
        x = rs.uniform(270, 810); y = rs.uniform(760, 920); ell(ctx, x, y, 34, 30); fs(ctx, (1, 0.97, 0.85), 4)
    for k in range(5):
        u = ((lt * 1.6 + k / 5) % 1); x = 540 + 260 * sin(k * 2.3); y = 820 - 600 * u + 900 * u * u
        ell(ctx, x, y, 30, 26); fs(ctx, (1, 0.97, 0.85), 4)


def couch_cast_fn(faces=None, mood_all="happy", spk_map=None, z=(1.0, 1.08), amp=0):
    faces = faces or {}; spk_map = spk_map or {}
    def f(ctx, lt, d):
        dx, dy = shake(lt, amp)
        ctx.save(); cam(ctx, punch(lt, 0.04) * lerp(z[0], z[1], sm(lt / d)), 540, 1100, dx=dx, dy=dy)
        BG(ctx, "living_dark", 6)
        couch_back(ctx, 1260)
        for ch, x, s, hy in ((DAD, 220, 1.25, 960), (SAM, 430, 1.0, 1060), (MOM, 640, 1.22, 965), (RUBY, 860, 1.2, 975)):
            m = faces.get(ch["seed"], mood_all); m = m(lt) if callable(m) else m
            spk = spk_map.get(ch["seed"])
            draw_char(ctx, ch, dict(x=x, y=head_y(s, hy), s=s, mood=m, mouth=talkT(spk) if spk else 0, dark=0.15, lookY=0.5, look=0.3 if x < 540 else -0.3), CUR["t"])
        couch_front_fg(ctx, 1430)
        rrect(ctx, 420, 1300, 240, 150, 10); fs(ctx, (0.75, 0.76, 0.8), 5)
        glow(ctx, 540, 1200, 520, (0.6, 0.8, 1), 0.35)
        ctx.restore()
    return f


def kitchen_spit(ctx, lt, d):
    ctx.save(); cam(ctx, punch(lt, 0.04) * (1 + 0.06 * sm(lt / d)), 540, 1060)
    BG(ctx, "kitchen", 5)
    for ch, x, s, hy, m in ((DAD, 220, 1.3, 940, M("joy", mo=0.6)), (SAM, 430, 1.0, 1040, M("joy", mo=0.7)), (MOM, 650, 1.25, 950, M("joy", mo=0.5)), (RUBY, 860, 1.25, 960, M("joy", mo=0.6))):
        P = dict(x=x, y=head_y(s, hy), s=s, mood=m, tilt=0.06 * sin(lt * 8 + x))
        P["armR"] = ik(P, x + 40 * s, hy + 60 * s, -1)
        draw_char(ctx, ch, P, CUR["t"])
        hx, hy2 = head_world(P); rrect(ctx, hx + 18 * s, hy2 + 70 * s, 28 * s, 110 * s, 12 * s); fs(ctx, (0.92, 0.96, 1.0), 4)
    table_fg(ctx, 1380)
    ctx.restore()
    for k in range(3): pop_word(ctx, lt, 0.2 + k * 0.5, "HA!", 220 + k * 320, 620 + (k % 2) * 90, 90, col=(1, 1, 1), life=0.45)


def viking_fx(ctx, lt, d, PP):
    hx, hy = head_world(PP); s = PP["s"]
    for sx in (-1, 1):
        ctx.move_to(hx + sx * 90 * s, hy - 90 * s); ctx.curve_to(hx + sx * 170 * s, hy - 120 * s, hx + sx * 190 * s, hy - 220 * s, hx + sx * 150 * s, hy - 270 * s)
        ctx.curve_to(hx + sx * 150 * s, hy - 200 * s, hx + sx * 120 * s, hy - 150 * s, hx + sx * 70 * s, hy - 120 * s); ctx.close_path(); fs(ctx, (0.97, 0.94, 0.85), 5)
    ctx.move_to(hx - 115 * s, hy - 70 * s); ctx.curve_to(hx - 110 * s, hy - 200 * s, hx + 110 * s, hy - 200 * s, hx + 115 * s, hy - 70 * s); ctx.close_path(); fs(ctx, (0.65, 0.66, 0.70), 5)


def tear_fx(ctx, lt, d, PP): pass


def hosp_flash(ctx, lt, d):
    ctx.save(); cam(ctx, 1.05 - 0.05 * sm(lt / d), 540, 1000)
    BG(ctx, "nursery", 10)
    P = dict(x=540, y=head_y(1.7, 820), s=1.7, mood=M("happy", tear=0.5), dark=0.0, lookY=0.8)
    P["armL"] = ik(P, 450, 1180, 1); P["armR"] = ik(P, 650, 1190, -1)
    draw_char(ctx, dict(MOM, top=(0.85, 0.85, 0.95)), P, CUR["t"])
    blob(ctx, [(540, 1180, 120), (620, 1170, 90)], (1, 0.72, 0.8)); ell(ctx, 470, 1150, 55, 50); fs(ctx, (0.80, 0.62, 0.50), 4)
    ctx.move_to(445, 1150); ctx.curve_to(455, 1158, 465, 1158, 475, 1150); st(ctx, OUTL, 3.5)
    ctx.restore()
    overlay(ctx, (1, 0.8, 0.5), 0.22); grain(ctx, lt, 0.12); vignette(ctx, 0.6, 380, 1100)
    label(ctx, lt, 0.2, "16 years ago", 540, 520, 72)


def photo_wall(circle_t=None, arrows=False):
    def f(ctx, lt, d):
        ctx.set_source_rgb(0.80, 0.62, 0.46); ctx.paint(); glow(ctx, 540, 900, 700, (1, 0.85, 0.6), 0.3)
        c = 0.0 if circle_t is None else clamp((lt - circle_t) / 0.5)
        ctx.save(); ctx.translate(540, 900); ctx.rotate(-0.02); family_photo(ctx, c); ctx.restore()
        if arrows and lt > circle_t + 0.5:
            label(ctx, lt, circle_t + 0.5, "red hair", 300, 470, 56, -0.1, (1, 0.6, 0.4))
            label(ctx, lt, circle_t + 0.9, "red hair", 820, 470, 56, 0.1, (1, 0.6, 0.4))
            label(ctx, lt, circle_t + 1.3, "...and me?", 640, 1250, 64, -0.05, (0.5, 0.95, 1))
    return f


def split_photo(ctx, lt, d):
    ctx.set_source_rgb(0.1, 0.1, 0.15); ctx.paint()
    for i, ch in enumerate((HANNAH, MOM)):
        x0 = i * 540
        ctx.save(); ctx.rectangle(x0 + 10, 350, 520, 960); ctx.clip()
        ctx.set_source_rgb(*((0.6, 0.8, 0.9) if i == 0 else (0.85, 0.75, 0.65))); ctx.paint()
        u = sm(clamp(lt / 0.4)); xx = x0 + 270 + (1 - u) * (-300 if i == 0 else 300)
        draw_char(ctx, ch, dict(x=xx, y=head_y(2.0, 820), s=2.0, mood="neutral" if i == 0 else "happy", saccade=False), CUR["t"])
        ctx.restore()
        text(ctx, "HANNAH" if i == 0 else "MY MOM", x0 + 270, 1290, 50, col=(1, 1, 1), stroke=10)
    if lt > 0.8:
        p = back_out(clamp((lt - 0.8) / 0.2)); ctx.save(); ctx.translate(540, 830); ctx.scale(p, p); text(ctx, "=", 0, 40, 200, col=(1, 0.86, 0.15), stroke=20); ctx.restore()


def zero_slam(ctx, lt, d):
    phone(ctx, 540, 960, 2.4, 0.0, scr_zero, lt, 0.3)


def hand_phone(ctx, lt, d):
    ctx.set_source_rgb(0.05, 0.05, 0.12); ctx.paint()
    tr = 6 * sin(lt * 40)
    phone(ctx, 540 + tr, 950, 2.1, -0.06, scr_chat([("Hi. I think you might be my mom?", True, 0.7)], "Karen Price"), lt, 0.4)
    for sx in (-1, 1):
        ctx.save(); ctx.translate(540 + sx * 330 + tr, 1400); ctx.rotate(-sx * 0.3)
        rrect(ctx, -90, -120, 180, 600, 70); fs(ctx, RUBY["top"], 7); ell(ctx, 0, -150, 95, 110); fs(ctx, RUBY["skin"], 7); ctx.restore()


SHOTS = {
    "a": SC("a", ["bought", "just"], [
        MED([(DAD, 540, 900, 1.7, "happy", None, dict(armL=("ang", -1.2, -1.6), armR=("ang", 1.2, 1.6)))], "living", blur=8,
            post=L("Christmas", 0.3, 760, 520, 70)),
        INS(kit_boxes, post=L("x4", 0.5, 820, 480, 110, 0.1, (1, 0.86, 0.15))),
        MED([(DAD, 220, 940, 1.3, "joy", None), (SAM, 430, 1040, 1.0, "joy", None), (MOM, 650, 950, 1.25, "happy", None), (RUBY, 860, 960, 1.25, "joy", None)], "living", blur=4),
    ]),
    "b": SC("b", [("four", 0, 1), "who's"], [
        INS(tubes),
        kitchen_spit,
        ECU(DAD, M("smirk", smile=0.6), "kitchen", "DA", fx=viking_fx, post=L("Viking?", 0.6, 800, 520, 76, 0.08)),
    ]),
    "c": SC("c", ["the", "dad", "we"], [
        INS(lambda c, lt, d: (c.save(), c.translate(540, 900), c.rotate(-0.05), calendar_card(c, lt, "6 WEEKS", "LATER"), c.restore()), bg="living", blur=18, cy=960),
        PHONE(scr_results_ready, bg="living", blur=18),
        INS(popcorn),
        couch_cast_fn(mood_all="happy"),
    ]),
    "d": SC("d", ["my", "i'm"], [
        LAPTOP(scr_pie),
        LAPTOP(lambda c, lt: scr_tree(c, lt)),
        ECU(SAM, M("joy", mo=0.4), "living", "SAM", s=2.9, fx=viking_fx, amp=4, post=L("VIKING!", 0.2, 540, 520, 90, -0.06, (1, 0.86, 0.15))),
    ]),
    "e": SC("e", ["and", ("zero", 1), ("no", 1, 0), ("no", 1, 1), ("no", 1, 2)], [
        LAPTOP(scr_click_ruby),
        couch_cast_fn(faces={84: "neutral", 82: "worried", 83: "worried", 81: "neutral"}, z=(1.0, 1.2)),
        INS(zero_slam, amp=10, post=lambda c, lt, d: (overlay(c, (1, 0.1, 0.1), 0.35 * (1 - clamp(lt / 0.3)), ADD))),
        ECU(MOM, M("shock", eo=1.5), "living_dark", dark=0.1),
        ECU(DAD, M("shock", eo=1.5), "living_dark", dark=0.1),
        ECU(SAM, M("worried"), "living_dark", s=2.9, dark=0.1, post=L("?", 0.15, 820, 560, 130, 0.15)),
    ]),
    "f": SC("f", ["right", ("i", 1, 0), "held"], [
        ECU(DAD, M("worried", smile=0.3), "living_dark", "DA", sweat=True, dark=0.1),
        ECU(RUBY, M("worried", tear=0.3), "living_dark", dark=0.1, look=-0.6),
        ECU(MOM, M("crying"), "living_dark", "MO", dark=0.1),
        hosp_flash,
    ]),
    "g": SC("g", ["he", "linda", "she"], [
        ECU(DAD, M("cold"), "living_dark", dark=0.25, look=0.0, z=(1.0, 1.05)),
        MED([(MOM, 300, 900, 1.6, "worried", None, dict(look=0.8, dark=0.2)), (DAD, 820, 880, 1.7, "cold", None, dict(look=-0.9, dark=0.4))], "living_dark", blur=10, z=(1.05, 1.15)),
        ECU(DAD, M("cold", bi=10), "living_dark", "DA", dark=0.35, z=(1.0, 1.18)),
        ECU(MOM, M("angry", flush=0.9, tear=0.4), "living_dark", "MO", amp=8, dark=0.05),
    ], whips=(3,)),
    "h": SC("h", [("i", 0, 0)], [
        ECU(RUBY, M("shock", tear=0.4), "living_dark", vertigo=True, dark=0.1, z=(1.0, 1.0)),
        INS(photo_wall(0.2)),
    ]),
    "i": SC("i", [("i", 0, 1), ("and", 0, 0), "karen"], [
        MED([(RUBY, 540, 980, 1.6, M("sad"), None, dict(dark=0.35))], "bedroom_night", blur=6, fg=lambda c, lt, d: blanket(c, 1300, (0.35, 0.40, 0.65))),
        PHONE(lambda c, lt: scr_matches(c, lt)),
        ECU(RUBY, M("shock"), "bedroom_night", dark=0.2, post=lambda c, lt, d: glow(c, 540, 1100, 600, (0.6, 0.8, 1), 0.25)),
        PHONE(scr_karen_card, amp=3),
    ]),
    "j": SC("j", ["three", ("were", 1)], [
        hand_phone,
        PHONE(scr_chat([("Hi. I think you might be my mom?", True, -1)], "Karen Price", typing_t=(0.0, 99))),
        PHONE(scr_chat([("Hi. I think you might be my mom?", True, -1), ("Were you born on March 3rd... at St. Mary's Hospital?", False, 0.05)], "Karen Price")),
    ]),
    "k": SC("k", ["then", "red", ("she", 1)], [
        ECU(RUBY, M("shock", tear=0.3), "bedroom_night", dark=0.2, post=L("...I was.", 0.2, 540, 520, 76)),
        PHONE(lambda c, lt: scr_photo(c, lt, sharp=clamp(lt / 1.0))),
        PHONE(lambda c, lt: scr_photo(c, lt), z=(1.15, 1.6)),
        INS(split_photo),
    ]),
    "l": SC("l", ["photo", END_T - 0.4], [
        INS(photo_wall(None), z=(1.0, 1.05)),
        INS(photo_wall(0.0, arrows=True), z=(1.05, 1.15)),
        END("PART 2", [("Tomorrow. Did you spot the clue?", 52, (1, 0.86, 0.15)), ("Follow Paper & Plot", 46, (1, 1, 1)), ("This story is fiction.", 34, (0.8, 0.8, 0.8))], END_T,
            base=INS(photo_wall(0.0, arrows=False), z=(1.15, 1.2))),
    ]),
}

HOOK = [('MY DNA TEST:', (1, 1, 1)), ('0% MATCH', (1, 0.2, 0.2)), ('WITH MY FAMILY', (1, 1, 1))]
