HEADER = ["MY DNA TEST WAS WRONG", "PART 2"]
END_T = LE("k", 1) + 0.3


def SEPIA(lab=None, t0=0.2):
    def f(ctx, lt, d):
        overlay(ctx, (1, 0.8, 0.5), 0.22); grain(ctx, lt, 0.12); vignette(ctx, 0.6, 380, 1100)
        if lab: label(ctx, lt, t0, lab, 540, 520, 72)
    return f


def nursery_wide(ctx, lt, d):
    BG(ctx, "nursery", 3)
    for i, x in enumerate((180, 420, 660, 900)):
        bassinet(ctx, x, 1250, 0.9, (1, 0.72, 0.8) if i in (1, 2) else (0.7, 0.82, 1.0))
    label(ctx, lt, 0.3, "3:12 AM", 800, 520, 70, 0.06)


def two_babies(ctx, lt, d):
    BG(ctx, "nursery", 14)
    bassinet(ctx, 300, 1050, 1.5, tag="WELLS"); bassinet(ctx, 790, 1060, 1.5, tag="PRICE")


def split_life(ctx, lt, d):
    for i, (bg, ch, lab) in enumerate((("ruby_room", RUBY, "RUBY"), ("tiny_room", HANNAH, "HANNAH"))):
        ctx.save(); ctx.rectangle(i * 540, 0, 540, 1920); ctx.clip()
        ctx.save(); ctx.translate(i * 540 - 270, 0); BG(ctx, bg, 6); ctx.restore()
        draw_char(ctx, ch, dict(x=i * 540 + 270, y=head_y(1.35, 860), s=1.35, mood="neutral" if i else "happy", dark=0.0), CUR["t"])
        ctx.restore()
        text(ctx, lab, i * 540 + 270, 1200, 56, col=(1, 1, 1), stroke=10)
    ctx.rectangle(534, 0, 12, 1920); ctx.set_source_rgb(1, 1, 1); ctx.fill()
    label(ctx, lt, 0.4, "16 years", 540, 520, 80, -0.05, (1, 0.86, 0.15))


def cafe_wide(z0=1.0, z1=1.08, moods=None, empty=(), run=None):
    moods = moods or {}
    def f(ctx, lt, d):
        ctx.save(); cam(ctx, punch(lt, 0.04) * lerp(z0, z1, sm(lt / d)), 540, 1060)
        BG(ctx, "cafe", 5)
        cast = ((RUBY, 110, 0.92, 1010), (MOM, 280, 0.95, 1000), (DAD, 445, 0.97, 995), (SAM, 590, 0.75, 1070), (KAREN, 790, 0.95, 1000), (HANNAH, 965, 0.92, 1010))
        for ch, x, s, hy in cast:
            if ch["seed"] in empty: continue
            m = moods.get(ch["seed"], "worried")
            draw_char(ctx, ch, dict(x=x, y=head_y(s, hy), s=s, mood=m(lt) if callable(m) else m, look=0.4 if x < 540 else -0.4), CUR["t"])
        if run:
            ch, x0 = run; u = sm(clamp(lt / 0.9)); x = lerp(x0, 1300, u)
            draw_char(ctx, ch, dict(x=x, y=head_y(1.15, 960), s=1.15, legs=True, mood=M("crying") if ch is HANNAH else M("worried"), tilt=0.2, look=1), CUR["t"])
        table_fg(ctx, 1320, (0.40, 0.25, 0.16))
        for x in (250, 450, 800): ell(ctx, x, 1360, 50, 22); fs(ctx, (1, 1, 1), 4)
        ctx.restore()
    return f


def old_photo(ctx, lt, d):
    ctx.set_source_rgb(0.30, 0.22, 0.18); ctx.paint()
    ctx.save(); ctx.translate(540, 900); ctx.rotate(0.05)
    ctx.rectangle(-330, -400, 660, 800); fs(ctx, (0.96, 0.93, 0.85), 6)
    ctx.save(); ctx.rectangle(-290, -360, 580, 620); ctx.clip(); ctx.set_source_rgb(0.75, 0.65, 0.5); ctx.paint()
    draw_char(ctx, GRANDPA, dict(x=0, y=head_y(1.4, -80), s=1.4, mood=M("joy", mo=0.5), saccade=False), 0.3)
    ctx.restore(); text(ctx, "Dad, 1989", 0, 330, 40, col=(0.4, 0.3, 0.2), weight=False)
    ctx.restore()
    overlay(ctx, (1, 0.8, 0.5), 0.2); grain(ctx, lt, 0.1)


def house_ins(which):
    def f(ctx, lt, d):
        BG(ctx, which, 0)
    return f


def cup_tip(ctx, lt, d):
    ctx.set_source_rgb(0.45, 0.30, 0.20); ctx.paint()
    u = sm(clamp(lt / 0.35)); ctx.save(); ctx.translate(540, 1000); ctx.rotate(1.4 * u)
    rrect(ctx, -110, -160, 220, 260, 30); fs(ctx, (1, 1, 1), 7); ctx.restore()
    if lt > 0.25:
        p = clamp((lt - 0.25) / 0.4)
        blob(ctx, [(640 + 120 * p, 1120, 60 + 120 * p), (760 + 200 * p, 1160, 40 + 90 * p), (560 + 60 * p, 1150, 30 + 60 * p)], (0.40, 0.24, 0.14))
        for k in range(6):
            a_ = -pi / 2 + (k - 2.5) * 0.4; r = 180 * p
            ell(ctx, 680 + r * cos(a_), 1050 + r * sin(a_) + 300 * p * p, 16, 16); ctx.set_source_rgb(0.40, 0.24, 0.14); ctx.fill()


def car_scene(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.05 * sm(lt / d), 540, 1000)
    ctx.set_source_rgb(0.04, 0.05, 0.10); ctx.paint()
    off = (lt * 400) % 1200
    for k in range(4):
        x = (k * 400 - off) % 1600 - 300; glow(ctx, x, 700, 160, (1, 0.8, 0.4), 0.35)
    rrect(ctx, 60, 380, 960, 700, 60); ctx.set_source_rgba(0.15, 0.20, 0.35, 0.7); ctx.fill()
    V.rain(ctx, lt, 0.3)
    for ch, x, s, hy in ((RUBY, 360, 1.5, 900), (SAM, 720, 1.2, 1000)):
        draw_char(ctx, ch, dict(x=x, y=head_y(s, hy), s=s, mood=M("sad", tear=0.3) if ch is RUBY else M("worried"), dark=0.45, look=0.3 if ch is RUBY else -0.5), CUR["t"])
    rrect(ctx, -40, 1350, 1160, 700, 40); fs(ctx, (0.10, 0.10, 0.13), 6)
    ctx.restore()
    for k in range(14):
        rs = random.Random(k); x = rs.uniform(0, 1080); y = (rs.uniform(0, 1920) + lt * 60) % 1920
        ell(ctx, x, y, 10, 14); ctx.set_source_rgba(0.8, 0.9, 1, 0.3); ctx.fill()


def hands_hold(ctx, lt, d):
    ctx.set_source_rgb(0.08, 0.09, 0.15); ctx.paint(); glow(ctx, 540, 1000, 600, (0.5, 0.6, 1), 0.2)
    ctx.move_to(60, 1950); ctx.line_to(470, 1080); st(ctx, OUTL, 236); ctx.move_to(60, 1950); ctx.line_to(470, 1080); st(ctx, RUBY["top"], 220)
    ell(ctx, 520, 1000, 130, 110, -0.5); fs(ctx, RUBY["skin"], 7)
    ctx.move_to(1020, 1950); ctx.line_to(660, 1120); st(ctx, OUTL, 176); ctx.move_to(1020, 1950); ctx.line_to(660, 1120); st(ctx, SAM["top"], 160)
    ell(ctx, 610, 1030, 92, 80, 0.4); fs(ctx, SAM["skin"], 6)
    for k in range(4): ell(ctx, 470 + k * 34, 935 + k * 8, 26, 50, 0.3); fs(ctx, SAM["skin"], 5)
    overlay(ctx, (0.03, 0.04, 0.14), 0.25)


def peek(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.1 * sm(lt / d), 540, 1000)
    BG(ctx, "hall", 0)
    poly(ctx, [(780, 1260), (960, 1500), (700, 2000), (380, 2000)]); ctx.set_source_rgba(1, 0.75, 0.4, 0.18); ctx.fill()
    draw_char(ctx, RUBY, dict(x=820, y=head_y(1.4, 900), s=1.4, legs=False, mood=M("worried"), look=1, dark=0.45, tilt=-0.1), CUR["t"])
    ctx.restore()


def kitchen_two(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.06 * sm(lt / d), 540, 1050)
    BG(ctx, "kitchen_night", 4)
    draw_char(ctx, MOM, dict(x=360, y=head_y(1.4, 900), s=1.4, mood=M("sad"), look=0.5, lookY=0.6, dark=0.35), CUR["t"])
    draw_char(ctx, DAD, dict(x=740, y=head_y(1.45, 890), s=1.45, mood=M("sad"), look=-0.5, lookY=0.6, dark=0.35), CUR["t"])
    table_fg(ctx, 1320)
    ell(ctx, 540, 1300, 70, 24); fs(ctx, (1, 1, 1), 4)
    ctx.restore()
    label(ctx, lt, 0.4, "tick... tock...", 760, 520, 60, 0.06, (0.85, 0.85, 0.9))


def photo_fade(ctx, lt, d):
    ctx.set_source_rgb(0.18, 0.15, 0.22); ctx.paint()
    ctx.save(); ctx.translate(540, 900); ctx.rotate(-0.02); family_photo(ctx)
    a = sm(clamp((lt - 0.3) / 1.2))
    ctx.rectangle(5, -290, 165, 580); ctx.set_source_rgba(0.75, 0.88, 0.80, a); ctx.fill()
    ctx.restore()
    overlay(ctx, (0.03, 0.04, 0.14), 0.3)


SHOTS = {
    "a": SC("a", ["we", "two"], [
        ECU(HANNAH, M("neutral"), "tiny_room", post=lambda c, lt, d: V.name_tag(c, lt, 0.15, d - 0.1, "HANNAH", "the other girl", y=1180)),
        INS(lambda c, lt, d: BG(c, "hospital_ext", 0), post=L("same night", 0.3, 540, 1180, 72, -0.05)),
        INS(lambda c, lt, d: BG(c, "hosp_hall", 0), post=L("2 rooms apart", 0.2, 540, 1180, 70, -0.05, (1, 0.86, 0.15))),
    ]),
    "b": SC("b", [("a", 0, 1), "two", "somebody", "for", ("and", 1)], [
        ECU(NURSE, M("sad", lid=0.75, mo=0.9), "nursery", post=SEPIA("16 years ago")),
        INS(nursery_wide, post=SEPIA()),
        INS(two_babies, post=SEPIA()),
        INS(lambda c, lt, d: (c.save(), c.translate(540, 960), c.scale(1.4, 1.4), bracelets(c, lt), c.restore()), bg="nursery", blur=20, dim=0.2, post=SEPIA()),
        INS(split_life, z=(1.0, 1.05)),
        ECU(HANNAH, M("sad"), "tiny_room", dark=0.1),
    ], whips=(4,)),
    "c": SC("c", ["both", "nobody"], [
        INS(lambda c, lt, d: BG(c, "cafe", 0), post=L("Saturday", 0.3, 760, 520, 70)),
        cafe_wide(),
        INS(lambda c, lt, d: cups(c, lt)),
    ]),
    "d": SC("d", [("she", 1, 0), ("she", 1, 1)], [
        ECU(MOM, M("shock", eo=1.5), "cafe", vertigo=True, z=(1.0, 1.0)),
        ECU(MOM, M("crying", smile=-0.3), "cafe", "MO"),
        ECU(HANNAH, M("worried", lid=0.3), "cafe", look=-0.5),
    ]),
    "e": SC("e", ["her", "you", "he"], [
        ECU(KAREN, M("hopeful", tear=0.6), "cafe", look=0.4),
        ECU(RUBY, M("hopeful", smile=0.4, flush=0.4), "cafe", look=-0.4),
        ECU(KAREN, M("happy", tear=0.7), "cafe", "KA"),
        INS(old_photo),
    ]),
    "f": SC("f", ["until", ("and", 0, 0), "so", "big", "tiny", "two"], [
        ECU(HANNAH, M("cold"), "cafe"),
        INS(lambda c, lt, d: keys_bag(c, lt, "keys")),
        INS(lambda c, lt, d: keys_bag(c, lt, "bag")),
        ECU(HANNAH, M("angry", flush=0.6), "cafe", "HA", amp=3),
        INS(house_ins("big_house"), z=(1.0, 1.1)),
        INS(house_ins("tiny_apt_ext"), z=(1.1, 1.0), post=L("tiny", 0.2, 760, 520, 80, 0.06)),
        ECU(KAREN, M("sad", tear=0.4), "cafe", lookY=0.6, post=L("2 jobs", 0.2, 800, 520, 76, 0.08, (1, 0.86, 0.15))),
    ]),
    "g": SC("g", ["no", "somebody"], [
        ECU(KAREN, M("worried", tear=0.6), "cafe", "KA"),
        ECU(HANNAH, M("angry", flush=1.0, bi=18, teeth=False), "cafe", "HA", amp=10, post=lambda c, lt, d: overlay(c, (1, 1, 1), 0.5 * (1 - clamp(lt / 0.12)), ADD)),
        INS(cup_tip, amp=6),
    ]),
    "h": SC("h", ["karen", "and", "on", "sam"], [
        cafe_wide(empty=(85,), run=(HANNAH, 960)),
        cafe_wide(empty=(85, 86), run=(KAREN, 790)),
        cafe_wide(empty=(85, 86), moods={81: M("sad", tear=0.4), 82: M("crying"), 83: M("sad"), 84: M("worried")}, z0=1.05, z1=1.2),
        car_scene,
        INS(hands_hold),
    ], whips=(3,)),
    "i": SC("i", ["she's", ("and", 2)], [
        peek,
        ECU(MOM, M("sad", tear=0.3), "kitchen_night", "MO", dark=0.2),
        ECU(DAD, M("worried"), "kitchen_night", "DA", dark=0.2),
    ]),
    "j": SC("j", ["maybe", "karen"], [
        kitchen_two,
        ECU(MOM, M("crying", smile=-0.2), "kitchen_night", "MO", dark=0.2),
        ECU(RUBY, M("shock", tear=0.5), "hall", vertigo=True, z=(1.0, 1.0), dark=0.25),
    ]),
    "k": SC("k", ["and", "guest", END_T - 0.4], [
        MED([(RUBY, 540, 1050, 0.9, M("sad"), None, dict(dark=0.4, legs=True))], "hall", blur=0, z=(1.0, 1.15)),
        INS(photo_fade),
        ECU(RUBY, M("crying", smile=-0.6), "hall", dark=0.25),
        END("PART 3", [("Tomorrow. What would YOU do?", 50, (1, 0.86, 0.15)), ("Follow Paper & Plot", 46, (1, 1, 1)), ("This story is fiction.", 34, (0.8, 0.8, 0.8))], END_T,
            base=ECU(RUBY, M("crying", smile=-0.6), "hall", dark=0.25)),
    ]),
}

HOOK = [('WE WERE', (1, 1, 1)), ('SWITCHED', (1, 0.86, 0.15)), ('AT BIRTH', (1, 1, 1))]
