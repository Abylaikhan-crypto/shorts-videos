exec(open(f"{HERE}/house_common.py").read())
HEADER = ["3:07 AM", "FINAL PART"]
END_T = LE("l", 1) + 0.3
HOOK = [("HE KNOWS", (1, 1, 1)), ("YOU'RE IN", (1, 1, 1)), ("THE CLOSET", (1, 0.86, 0.15))]
LIGHT = LIGHT_NIGHT
SCENE_TINT.update({"b": "police", "c": "police", "d": "police", "i": "morning", "j": "morning"})
_hud = clock_hud(3, 15, 40)
def HUD(ctx, sc, t):
    if sc in "abcdefgh": _hud(ctx, sc, t)
PL = lambda a=0.45: (lambda c, lt, d: police_lights(c, lt, a))
HALE_ST = lambda x=560, s=0.95, mood=M("neutral"), hy=820: (HALE, x, hy, s, mood, None, dict(legs=True))


def hale_run(ctx, lt, d):
    walk_shot(HALE, "h_hall", 560, 520, 760, 1.5, 0.7, M("scared"), run=True, post=PL(0.35))(ctx, lt, d)


def dog_run(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0, 540, 1000); BG(ctx, "h_hall", 6)
    u = clamp(lt / d); dog_in(ctx, lerp(-200, 1300, u), 1500, 1.4, run=True, bark=0.6)
    ctx.restore(); police_lights(ctx, lt, 0.3); speed_lines(ctx, lt, 0.5) if False else None


def tug(ctx, lt, d):
    dx, dy = shake(lt, 6)
    ctx.save(); cam(ctx, 1.05, 540, 1000, dx=dx, dy=dy); BG(ctx, "h_hall", 5)
    draw_char(ctx, HALE, dict(x=640, y=head_y(1.35, 820), s=1.35, legs=True, mood=M("angry"), tilt=0.12 + 0.05 * sin(lt * 14)), CUR["t"])
    dog_in(ctx, 330, 1600, 1.3, bark=0.4 + 0.2 * sin(lt * 16), flip=False, tilt=-0.2 + 0.1 * sin(lt * 16))
    ctx.restore(); police_lights(ctx, lt, 0.3)
    label(ctx, lt, 0.4, "GOOD BOY!", 540, 560, 100, -0.06, (1, 0.86, 0.15))


SHOTS = {
    "a": SC("a", ["one", "then", "you"], [CLOSET([HALE_ST(560, 0.95)]), CLOSET([HALE_ST(560, 1.4, hy=760)], z=(1.0, 1.1)),
                                          ECU(YOU, M("scared", tear=0.5), "h_closet", dark=0.35, tremble=0.8), CLOSET([HALE_ST(560, 1.4, hy=760)], eyes=lambda lt, d: 1.0)]),
    "b": SC("b", ["sirens", "doors", ("police", 1)], [BGI("h_bedroom_dark", z=(1.0, 1.1), post=PL(0.6)), BGI("h_exterior", z=(1.0, 1.1)), BGI("h_exterior", z=(1.3, 1.5), cy=1300),
                                                    cast_shot("h_stairs", [(DIAZ, 400, 900, 1.35, M("angry"), "DIAZ", {}), (COP2, 760, 880, 1.25, M("neutral"), None, {})], blur=5, post=PL(0.4))]),
    "c": SC("c", ["he", "but", ("he", 0, 1)], [ECU(HALE, M("scared"), "h_bedroom_dark", post=PL(0.4)), hale_run, dog_run, tug]),
    "d": SC("d", ["it's", ("we", 1), ("you're", 1)], [BGI("h_stairs", amp=6, post=PL(0.5)),
                                                     cast_shot("h_hall", [(COP2, 380, 860, 1.3, M("neutral"), None, {}), (HALE, 720, 900, 1.2, M("sad"), None, dict(lookY=0.8))], blur=4, post=PL(0.35)),
                                                     ECU(DIAZ, M("hopeful"), "h_hall", "DIAZ", post=PL(0.25)), ECU(YOU, M("crying", smile=0.3), "h_bedroom_dark")]),
    "e": SC("e", ["and", "makes"], [BGI("h_attic_hatch", z=(1.0, 1.2)), BGI("h_attic", z=(1.0, 1.15)), ECU(DIAZ, M("shock"), "h_attic")]),
    "f": SC("f", ["empty", "your", "and", "day"], [BGI("h_attic", z=(1.3, 1.5), cy=1350), BGI("h_attic", z=(1.4, 1.6), cx=300, cy=1150),
                                                   BGI("h_attic", z=(1.6, 1.8), cx=760, cy=1450), BGI("h_attic", z=(1.8, 2.0), cx=700, cy=1420), INS(notebook)]),
    "g": SC("g", ["he", "he's"], [cast_shot("h_hall", [(DIAZ, 380, 860, 1.35, M("sad"), "DIAZ", {}), (YOU, 760, 900, 1.3, M("shock"), None, dict(look=-0.6))], blur=5),
                                  INS(old_photo), ECU(DIAZ, M("sad"), "h_hall", "DIAZ")]),
    "h": SC("h", ["every", "listening"], [BGI("h_attic", dark=0.35, post=lambda c, lt, d: pop_word(c, lt, 0.05, "41 DAYS", 540, 900, 170, col=(1, 0.35, 0.35), life=3)),
                                          BGI("h_bedroom_dark", cy=350, z=(1.15, 1.35), dark=0.1), ECU(YOU, M("shock", tear=0.4), "h_bedroom_dark", vertigo=True)]),
    "i": SC("i", ["mom", ("i'm", 1)], [BGI("h_living", post=L("6:40 AM", 0.2, 540, 560, 110, -0.04, (1, 0.86, 0.15))),
                                       cast_shot("h_living", [(DAD, 260, 860, 1.2, M("happy", tear=0.3), None, {}), (YOU, 540, 900, 1.3, M("crying", smile=0.4), None, dict(armL=("ik", -150, -60, 1))),
                                                              (MOM, 780, 860, 1.3, M("crying", smile=0.3), None, dict(armR=("ik", -170, -60, -1)))], blur=3),
                                       ECU(MOM, M("crying", smile=0.3), "h_living", "MOM")]),
    "j": SC("j", ["he"], [DOG("h_living", look_up=False), steak]),
    "k": SC("k", ["three", "the", ("motion", 1)], [BGI("h_hall", post=L("1 WEEK LATER", 0.1, 540, 560, 100, -0.04, (1, 0.86, 0.15))),
                                                   BGI("h_bedroom_dark", post=L("3:07 AM", 0.1, 540, 560, 130, -0.04, (1, 0.35, 0.35))),
                                                   ECU(YOU, lambda lt: M("sad", lid=0.98) if lt < 0.7 else M("shock"), "h_bedroom_dark"), SPEAKER()]),
    "l": SC("l", ["four", "there", "would"], [SPEAKER(z=(1.15, 1.3)), SPEAKER(red=True, post=lambda c, lt, d: pop_word(c, lt, 0.02, "4", 540, 650, 320, col=(1, 0.35, 0.35), life=4)),
                                              BGI("h_attic_hatch", z=(1.0, 1.3), dark=0.3),
                                              END("THE END?", [("Would YOU go check?", 52, (1, 0.86, 0.15)), ("Follow Paper & Plot", 46, (1, 1, 1)),
                                                               ("This story is fiction.", 34, (0.8, 0.8, 0.8))], END_T, base=BGI("h_attic_hatch", z=(1.1, 1.1), dark=0.4))]),
}
