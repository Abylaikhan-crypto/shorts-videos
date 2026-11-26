# exec'd inside dna.py globals for "3:07 AM" (smart-house series)
exec(open(f"{HERE}/hor_common.py").read())
from s2 import dog_body, dog_head, FUR, FURD, CREAM
exec(open(f"{HERE}/hotel_common.py").read())     # aiplate(), BGI, cast_shot, tints (hotel sets stay unused)
COLS_EXTRA = {"N": (1, 1, 1), "NOVA": (0.45, 0.95, 1.0), "HSP": (1, 0.35, 0.35), "HALE": (1, 0.35, 0.35), "MOM": (1, 0.6, 0.8),
              "DISP": (0.6, 0.85, 1.0), "DIAZ": (1, 0.86, 0.15)}
AI_DIR = f"{HERE}/ai_bg_hs"
for _n in ("h_hall", "h_bedroom", "h_bedroom_dark", "h_kitchen", "h_closet", "h_attic", "h_attic_hatch", "h_exterior", "h_living", "h_stairs"):
    SETS[_n] = aiplate(_n)

YOU = dict(skin=(0.93, 0.76, 0.64), hair=(0.30, 0.20, 0.12), hairstyle="crew", outfit="longsleeve", top=(0.22, 0.30, 0.52), seed=191, pants=(0.25, 0.28, 0.4))
HALE = dict(skin=(0.86, 0.80, 0.74), hair=(0.40, 0.30, 0.20), hairstyle="long", outfit="hoodie", top=(0.55, 0.56, 0.58), seed=192, beard=True,
            pants=(0.2, 0.2, 0.22))
DIAZ = dict(skin=(0.78, 0.56, 0.42), hair=(0.10, 0.07, 0.05), hairstyle="bun", outfit="uniform", top=(0.12, 0.16, 0.32), seed=193)
COP2 = dict(skin=(0.95, 0.80, 0.68), hair=(0.40, 0.28, 0.16), hairstyle="crew", outfit="uniform", top=(0.12, 0.16, 0.32), seed=194)
MOM = dict(skin=(0.98, 0.86, 0.77), hair=(0.80, 0.32, 0.13), hairstyle="curly", outfit="cardigan", top=(0.55, 0.30, 0.45), no_lanyard=True, seed=195, blush=True)
DAD = dict(skin=(0.96, 0.80, 0.68), hair=(0.30, 0.22, 0.14), hairstyle="crew", outfit="sweater", top=(0.30, 0.42, 0.62), seed=196, pants=(0.3, 0.3, 0.35))

TINTS.update({"night": (0.84, 0.88, 1.0), "police": (0.92, 0.88, 0.97), "morning": (1.0, 0.93, 0.84)})
SCENE_TINT = {}
_dct = draw_char


def draw_char(ctx, ch, P, t):
    P = dict(P); P.setdefault("tint", SCENE_TINT.get(CUR["sc"], "night")); return _dct(ctx, ch, P, t)


CYAN = (0.35, 0.95, 1.0)


def speaker(ctx, x, y, s, spk=("NOVA",), red=False, on=1.0):
    """smart speaker puck with a light ring that pulses with the voice"""
    a = max(talkT(k) for k in spk) if spk else 0.0
    col = (1, 0.2, 0.2) if red else CYAN
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ell(ctx, 0, 90, 230, 40); ctx.set_source_rgba(0, 0, 0, 0.35); ctx.fill()
    ctx.move_to(-200, -40); ctx.line_to(-200, 70); ctx.curve_to(-200, 120, 200, 120, 200, 70); ctx.line_to(200, -40); ctx.close_path(); fs(ctx, (0.16, 0.17, 0.2), 7)
    for k in range(-180, 190, 18):
        ell(ctx, k, 40, 4, 4); ctx.set_source_rgba(0.35, 0.36, 0.4, 1); ctx.fill()
    ell(ctx, 0, -40, 200, 46); fs(ctx, (0.22, 0.23, 0.27), 7)
    g = on * (0.55 + 0.45 * min(1, a * 4))
    ell(ctx, 0, -40, 170, 34); ctx.set_source_rgba(*col, g); ctx.set_line_width(16); ctx.stroke()
    ctx.restore()
    glow(ctx, x, y - 40 * s, 420 * s, col, 0.35 * g)


def SPEAKER(bg="h_bedroom_dark", spk=("NOVA",), red=False, z=(1.0, 1.15), post=None):
    def f(ctx, lt, d):
        ctx.save(); cam(ctx, punch(lt, 0.03) * lerp(z[0], z[1], sm(lt / d)), 540, 1000); BG(ctx, bg, 22)
        ctx.restore(); overlay(ctx, (0, 0, 0), 0.25)
        poly(ctx, [(-100, 1220), (1180, 1180), (1180, 2000), (-100, 2000)]); fs(ctx, (0.20, 0.15, 0.13), 8)   # nightstand
        speaker(ctx, 540, 1130, 1.6, spk, red)
        if post: post(ctx, lt, d)
    return f


def slats(ctx, lt, light=0.6):
    """inside the closet: dark louvres with thin stripes of light"""
    for y in range(0, 1920, 72):
        ctx.rectangle(0, y, 1080, 40); ctx.set_source_rgba(0.02, 0.02, 0.04, 0.88); ctx.fill()
        ctx.rectangle(0, y + 34, 1080, 6); ctx.set_source_rgba(0.14, 0.14, 0.18, 0.9); ctx.fill()
    for x in (0, 1040): ctx.rectangle(x, 0, 40, 1920); ctx.set_source_rgb(0.03, 0.03, 0.05); ctx.fill()


def CLOSET(cast=(), bg="h_bedroom_dark", z=(1.0, 1.06), post=None, eyes=None, phone_glow=None):
    """view out through the slats. cast like cast_shot. eyes(lt,d)->0..1 shows HALE's eyes close-up"""
    def f(ctx, lt, d):
        ctx.save(); cam(ctx, lerp(z[0], z[1], sm(lt / d)), 540, 1000); BG(ctx, bg, 2)
        for c in cast:
            ch, x, hy, s, mood, spk = c[:6]; ex = c[6] if len(c) > 6 else {}
            mo = mood(lt) if callable(mood) else mood
            P = dict(x=x, y=head_y(s, hy), s=s, mood=mo, mouth=talkT(spk) if spk else 0.0); P.update(ex(lt) if callable(ex) else ex)
            draw_char(ctx, ch, P, CUR["t"])
        ctx.restore()
        if eyes:
            e = eyes(lt, d)
            if e > 0:
                overlay(ctx, (0, 0, 0), 0.5 * e)
                draw_char(ctx, HALE, dict(x=540, y=head_y(4.2, 1000), s=4.2, mood=M("neutral", eo=1.2), look=0.0, tint="dark"), CUR["t"])
        if phone_glow is not None:
            g = phone_glow(lt, d)
            if g > 0: glow(ctx, 540, 1700, 900, (0.6, 0.8, 1), 0.7 * g)
        slats(ctx, lt)
        if phone_glow is not None and phone_glow(lt, d) > 0:
            glow(ctx, 540, 1750, 500, (0.7, 0.85, 1), 0.5 * phone_glow(lt, d))
        if post: post(ctx, lt, d)
    return f


def police_lights(ctx, lt, a=0.5):
    ph = int(lt * 4) % 2
    glow(ctx, 200 if ph else 880, 700, 1100, (1, 0.1, 0.15) if ph else (0.15, 0.3, 1), a)


def DOG(bg="h_bedroom_dark", z=(1.0, 1.12), bark=lambda lt: 0.0, look_up=True, post=None, sit=False, amp=0, dark=0.0):
    def f(ctx, lt, d):
        dx, dy = shake(lt, amp)
        ctx.save(); cam(ctx, punch(lt, 0.03) * lerp(z[0], z[1], sm(lt / d)), 540, 1000, dx=dx, dy=dy); BG(ctx, bg, 14); ctx.restore()
        if dark: overlay(ctx, (0, 0, 0), dark)
        b = bark(lt)
        ctx.save(); ctx.translate(540, 1150); ctx.scale(2.6, 2.6)
        dog_head(ctx, 0, 0, 1.0, CUR["t"], bark=b, tilt=-0.35 if look_up else 0.0, look=-0.6 if look_up else 0, sad=0.0)
        ctx.restore()
        if post: post(ctx, lt, d)
    return f


def dog_in(ctx, x, y, s, run=False, bark=0.0, flip=False, sit=False, tilt=0.0):
    dog_body(ctx, x, y, s, CUR["t"], bark=bark, flip=flip, sit=sit, run=run, tilt=tilt)


# ---------- phone screens (phone coords: 320 x 620 centred) ----------
def scr_kcam(ctx, lt):
    ctx.set_source_rgb(0.05, 0.05, 0.07); ctx.paint()
    text(ctx, "HOME CAM", 0, -255, 24, col=(1, 1, 1))
    ctx.save(); ctx.rectangle(-150, -220, 300, 420); ctx.clip(); ctx.translate(0, -10); ctx.scale(300 / 1080, 420 / 1920 * 1.0)
    ctx.translate(-540, -960); BG(ctx, "h_kitchen", 0); ctx.restore()
    ctx.save(); ctx.rectangle(-150, -220, 300, 420); ctx.clip()
    ctx.set_operator(cairo.OPERATOR_HSL_SATURATION); ctx.set_source_rgb(0.5, 0.5, 0.5); ctx.paint(); ctx.set_operator(cairo.OPERATOR_OVER)
    for k in range(-220, 200, 5): ctx.rectangle(-150, k, 300, 2); ctx.set_source_rgba(0, 0, 0, 0.2); ctx.fill()
    ctx.restore()
    text(ctx, "KITCHEN", -140, -195, 16, col=(1, 1, 1), align="l"); text(ctx, f"03:07:{int(lt * 1) % 60 + 12:02d}", 140, -195, 16, col=(1, 1, 1), align="r")
    if int(lt * 2) % 2 == 0: ell(ctx, -132, 180, 6, 6); ctx.set_source_rgb(1, 0.1, 0.1); ctx.fill()
    text(ctx, "REC", -118, 186, 16, col=(1, 1, 1), align="l")
    rrect(ctx, -150, 220, 300, 60, 14); ctx.set_source_rgb(0.85, 0.2, 0.2); ctx.fill(); text(ctx, "Motion detected", 0, 258, 20, col=(1, 1, 1))


def scr_voicemsg(ctx, lt):
    ctx.rectangle(-160, -310, 320, 70); ctx.set_source_rgb(0.92, 0.92, 0.95); ctx.fill(); text(ctx, "Mom", 0, -265, 24, col=(0.15, 0.15, 0.2))
    text(ctx, "3:09 AM", 0, -205, 16, col=(0.5, 0.5, 0.55), weight=False)
    rrect(ctx, -140, -170, 260, 90, 30); ctx.set_source_rgb(0.88, 0.88, 0.9); ctx.fill()
    ell(ctx, -105, -125, 24, 24); ctx.set_source_rgb(0.25, 0.55, 1.0); ctx.fill()
    poly(ctx, [(-112, -137), (-112, -113), (-94, -125)]); ctx.set_source_rgb(1, 1, 1); ctx.fill()
    a = talkT("MOM")
    for i in range(18):
        h_ = 8 + 50 * a * abs(sin(i * 1.7 + CUR["t"] * 12)); ctx.rectangle(-70 + i * 10, -125 - h_ / 2, 6, h_); ctx.set_source_rgb(0.4, 0.4, 0.45); ctx.fill()


def scr_app(occ=2, t_occ=0.0):
    def f(ctx, lt):
        ctx.set_source_rgb(0.08, 0.10, 0.14); ctx.paint()
        text(ctx, "SMART HOME", 0, -255, 24, col=(1, 1, 1))
        for i, (nm, tt) in enumerate((("Front door", 0.2), ("Back door", 0.5), ("Garage", 0.8))):
            y = -200 + i * 70; on = lt >= tt
            rrect(ctx, -150, y, 300, 60, 14); ctx.set_source_rgb(0.15, 0.18, 0.24); ctx.fill()
            text(ctx, nm, -130, y + 38, 20, col=(1, 1, 1), align="l", weight=False)
            text(ctx, "LOCKED" if on else "...", 135, y + 38, 18, col=(0.4, 1, 0.6) if on else (0.7, 0.7, 0.75), align="r")
        if lt >= t_occ:
            a = back_out(clamp((lt - t_occ) / 0.4))
            ctx.save(); ctx.translate(0, 75); ctx.scale(a, a)
            rrect(ctx, -150, -70, 300, 140, 18); ctx.set_source_rgb(0.75, 0.12, 0.12); ctx.fill()
            text(ctx, "OCCUPANTS", 0, -20, 24, col=(1, 1, 1)); text(ctx, str(occ), 0, 50, 64, col=(1, 1, 1))
            ctx.restore()
    return f


def scr_911(ctx, lt):
    ctx.set_source_rgb(0.12, 0.13, 0.17); ctx.paint()
    text(ctx, "911", 0, -150, 90, col=(1, 1, 1))
    text(ctx, f"00:{int(lt) + 3:02d}", 0, -80, 26, col=(0.7, 0.9, 0.7), weight=False)
    a = max(talkT("DISP"), 0)
    for i in range(16):
        h_ = 6 + 60 * a * abs(sin(i * 1.3 + CUR["t"] * 14)); ctx.rectangle(-120 + i * 15, 40 - h_ / 2, 8, h_); ctx.set_source_rgb(0.6, 0.85, 1); ctx.fill()
    ell(ctx, 0, 220, 50, 50); ctx.set_source_rgb(*RED); ctx.fill()


def scr_mom_text(ctx, lt):
    ctx.rectangle(-160, -310, 320, 70); ctx.set_source_rgb(0.92, 0.92, 0.95); ctx.fill(); text(ctx, "Mom", 0, -265, 24, col=(0.15, 0.15, 0.2))
    rrect(ctx, -140, -190, 250, 90, 18); ctx.set_source_rgb(0.88, 0.88, 0.9); ctx.fill()
    text(ctx, "Are you ok??", -125, -150, 20, col=(0.1, 0.1, 0.12), align="l", weight=False)
    text(ctx, "ANSWER ME", -125, -118, 20, col=(0.1, 0.1, 0.12), align="l")


# ---------- props ----------
def plate_ins(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.1 * sm(lt / d), 540, 960); BG(ctx, "h_kitchen", 20); ctx.restore(); overlay(ctx, (0, 0, 0), 0.3)
    glow(ctx, 540, 1000, 700, (0.8, 0.9, 1), 0.25)
    ell(ctx, 540, 1080, 360, 150); fs(ctx, (0.95, 0.95, 0.97), 8); ell(ctx, 540, 1080, 260, 100); st(ctx, (0.8, 0.82, 0.86), 4)
    if lt > 0.0:
        poly(ctx, [(380, 1060), (640, 990), (640, 1100)]); fs(ctx, (0.92, 0.78, 0.50), 6)        # half sandwich
        poly(ctx, [(395, 1055), (630, 1000), (630, 1020), (400, 1068)]); ctx.set_source_rgb(0.35, 0.7, 0.3); ctx.fill()
    if lt > 0.6:
        ctx.save(); ctx.translate(760, 1060); ctx.rotate(0.5); rrect(ctx, -10, -180, 20, 300, 8); fs(ctx, (0.75, 0.76, 0.8), 5); ctx.restore()


def notebook(ctx, lt, d):
    ctx.set_source_rgb(0.10, 0.09, 0.08); ctx.paint(); glow(ctx, 540, 950, 650, (1, 0.95, 0.8), 0.45)
    ctx.save(); ctx.translate(540, 960); ctx.rotate(-0.05)
    rrect(ctx, -400, -560, 800, 1120, 16); fs(ctx, (0.93, 0.90, 0.80), 7)
    for k in range(-480, 520, 70): ctx.move_to(-360, k); ctx.line_to(360, k); st(ctx, (0.7, 0.8, 0.9), 2)
    days = ["DAY 1", "DAY 2", "DAY 3", "DAY 17", "DAY 29", "DAY 40", "DAY 41"]
    n = 1 + int(lt / max(0.25, (d * 0.8) / len(days)))
    for i, dd in enumerate(days[:n]):
        red = dd == "DAY 41"
        text(ctx, dd, -330, -440 + i * 140, 70 if red else 58, col=(0.75, 0.1, 0.1) if red else (0.15, 0.15, 0.25), align="l")
        if not red:
            for k in range(4): ctx.move_to(-20 + k * 70, -460 + i * 140); ctx.line_to(30 + k * 70, -455 + i * 140); st(ctx, (0.3, 0.3, 0.4), 4)
    ctx.restore()


def notebook_lab(ctx, lt, d): notebook(ctx, lt, d)


def clock_hud(h0, m0, m1):
    def hud(ctx, sc, t):
        keys = list(TL); i = keys.index(sc); m = lerp(m0, m1, (i + t / DUR(sc)) / len(keys))
        rrect(ctx, 760, 200, 260, 76, 38); ctx.set_source_rgba(0, 0, 0, 0.6); ctx.fill()
        text(ctx, f"{h0}:{int(m):02d} AM", 890, 254, 36, col=(1, 1, 1))
    return hud


def police_hud(m0, m1, scenes):
    base = clock_hud(3, 14, 22)
    def hud(ctx, sc, t):
        if sc not in scenes: return
        keys = [k for k in TL if k in scenes]; i = keys.index(sc); m = lerp(m0, m1, (i + t / DUR(sc)) / len(keys))
        rrect(ctx, 600, 200, 420, 76, 38); ctx.set_source_rgba(0.5, 0, 0, 0.7); ctx.fill()
        text(ctx, f"POLICE IN {int(m):d}:{int((m % 1) * 60):02d}", 810, 254, 34, col=(1, 1, 1))
    return hud


def LIGHT_NIGHT(sc, t):
    return dict(amb=(0.92, 0.95, 1.0), bloom=0.7, thr=0.6, vig=0.62)


def you_dog(bg="h_bedroom", mood=M("neutral"), z=(1.0, 1.08), dog_bark=lambda lt: 0.0, hug=False, post=None, blur=4, dark=0.0):
    def f(ctx, lt, d):
        ctx.save(); cam(ctx, punch(lt, 0.03) * lerp(z[0], z[1], sm(lt / d)), 540, 1050); BG(ctx, bg, blur)
        ex = dict(armR=("ik", -160, -60, -1)) if hug else {}
        draw_char(ctx, YOU, dict(x=620, y=head_y(1.45, 880), s=1.45, mood=mood(lt) if callable(mood) else mood, **ex), CUR["t"])
        dog_in(ctx, 470 if hug else 330, 1560, 1.15, bark=dog_bark(lt), flip=hug, sit=True)
        ctx.restore()
        if dark: overlay(ctx, (0, 0, 0), dark)
        if post: post(ctx, lt, d)
    return f


def dog_at_door(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.08 * sm(lt / d), 540, 1100); BG(ctx, "h_bedroom_dark", 3)
    dog_in(ctx, 640, 1520, 1.25, bark=0.15 + 0.1 * abs(sin(lt * 18)), flip=True, tilt=0.35)
    ctx.restore()


def sepia(lab=None, y=520):
    return lambda c, lt, d: (overlay(c, (1, 0.8, 0.5), 0.28), grain(c, lt, 0.14), label(c, lt, 0.2, lab, 540, y, 84) if lab else None)


def walk_shot(ch, bg, x0, x1, hy, s0, s1, mood=M("neutral"), run=False, z=(1.0, 1.0), dark=0.0, post=None, flip_dog=None, blur=2):
    def f(ctx, lt, d):
        u = sm(clamp(lt / d)); ctx.save(); cam(ctx, lerp(z[0], z[1], u), 540, 1000); BG(ctx, bg, blur)
        s = lerp(s0, s1, u)
        draw_char(ctx, ch, dict(x=lerp(x0, x1, u), y=head_y(s, hy + 12 * abs(sin(lt * (14 if run else 7)))), s=s, legs=True, mood=mood,
                                tilt=(0.06 if run else 0.02) * sin(lt * (14 if run else 7))), CUR["t"])
        if flip_dog: flip_dog(ctx, lt, d, u)
        ctx.restore()
        if dark: overlay(ctx, (0, 0, 0), dark)
        if post: post(ctx, lt, d)
    return f


def muzzle(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.06 * sm(lt / d), 540, 1000); BG(ctx, "h_closet", 18); ctx.restore(); overlay(ctx, (0, 0, 0), 0.4)
    ctx.save(); ctx.translate(540, 1150); ctx.scale(2.6, 2.6)
    dog_head(ctx, 0, 0, 1.0, CUR["t"], bark=0.0, tilt=0.0, look=0.3, sad=0.6); ctx.restore()
    for k, (x, y) in enumerate(((240, 1250), (300, 1150))):
        rrect(ctx, x - 230, y - 40, 300, 95, 45); fs(ctx, YOU["skin"], 7)
    rrect(ctx, -60, 1150, 260, 260, 60); fs(ctx, YOU["top"], 8)
    slats(ctx, lt) if False else None


def steak(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.08 * sm(lt / d), 540, 1000); BG(ctx, "h_living", 14); ctx.restore()
    ctx.save(); ctx.translate(560, 1100); ctx.scale(2.4, 2.4); dog_head(ctx, 0, 0, 1.0, CUR["t"], bark=0.5 + 0.2 * sin(lt * 10), tilt=0.1); ctx.restore()
    ctx.save(); ctx.translate(300, 1500); ctx.rotate(-0.2)
    blob(ctx, [(-120, 0, 120), (40, -20, 110), (140, 10, 90)], (0.55, 0.22, 0.15)); ctx.restore()
    ell(ctx, 300, 1600, 330, 70); fs(ctx, (0.92, 0.92, 0.95), 6)
    label(ctx, lt, 0.3, "GOOD BOY", 540, 560, 110, -0.06, (1, 0.86, 0.15))


def old_photo(ctx, lt, d):
    ctx.set_source_rgb(0.12, 0.10, 0.09); ctx.paint()
    ctx.save(); ctx.translate(540, 960); ctx.rotate(0.05)
    rrect(ctx, -380, -470, 760, 900, 8); fs(ctx, (0.95, 0.93, 0.88), 6)
    ctx.rectangle(-330, -420, 660, 660); ctx.clip()
    ctx.save(); ctx.translate(0, -90); ctx.scale(660 / 1080, 660 / 1080); ctx.translate(-540, -960); BG(ctx, "h_living", 2)
    kid = dict(skin=(0.90, 0.82, 0.76), hair=(0.25, 0.18, 0.12), hairstyle="crew", outfit="sweater", top=(0.7, 0.3, 0.25), seed=197, freckles=True)
    _dct(ctx, kid, dict(x=540, y=head_y(1.6, 900), s=1.6, mood=M("happy"), tint="none"), CUR["t"])
    ctx.restore(); ctx.restore()
    ctx.save(); ctx.translate(540, 960); ctx.rotate(0.05); text(ctx, "Danny, 1998", 0, 360, 56, col=(0.25, 0.2, 0.2)); ctx.restore()
    overlay(ctx, (1, 0.8, 0.5), 0.22); grain(ctx, lt, 0.12)
