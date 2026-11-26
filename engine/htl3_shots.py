exec(open(f"{HERE}/hotel_common.py").read())
HEADER = ["CHECKOUT", "FINAL PART"]
END_T = LE("l", 1) + 0.3
HOOK = [("WHO GETS", (1, 1, 1)), ("THE KEY?", (1, 0.86, 0.15))]
SCENE_TINT.update({"j": "sun", "k": "sun", "l": "sun", "h": "warm", "i": "warm"})
HUD = checkout_hud(10, 0.5, set("abcdefghi"))
LIGHT = LIGHT_STD
CROWD = lambda moods={}, look=0.0: [(c[0], c[1], c[2], c[3], moods.get(c[0]["seed"], M("worried")), None, dict(look=look)) for c in
                                    ((WALT, 200, 880, 1.25), (EX1, 380, 820, 0.9), (EX2, 700, 820, 0.9), (LEO, 540, 940, 1.15), (MAYA, 880, 870, 1.3))]


def walt_walk(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.04 * sm(lt / d), 540, 1000); BG(ctx, "corridor", 2)
    u = sm(clamp(lt / d)); s = lerp(0.9, 1.7, u)
    draw_char(ctx, WALT, dict(x=540, y=head_y(s, lerp(820, 760, u)), s=s, legs=True, mood=M("hopeful", smile=0.3), tilt=0.03 * sin(lt * 6)), CUR["t"])
    ctx.restore()


def into_light(ctx, lt, d):
    ctx.save(); cam(ctx, 1.0 + 0.05 * sm(lt / d), 540, 1000); BG(ctx, "light_door", 0)
    u = sm(clamp(lt / d)); s = lerp(1.3, 0.55, u)
    ctx.push_group()
    draw_char(ctx, LEO, dict(x=lerp(560, 470, u), y=head_y(s, lerp(900, 760, u)), s=s, legs=True, mood=M("hopeful"), look=-0.5), CUR["t"])
    pat = ctx.pop_group(); ctx.set_source(pat); ctx.paint_with_alpha(1 - 0.85 * u)
    ctx.restore()
    glow(ctx, 470, 760, 600, (1, 0.95, 0.85), 0.5 * u)


def monitor(ctx, lt, d):
    ctx.set_source_rgb(0.02, 0.03, 0.03); ctx.paint()
    ctx.new_path()
    for x in range(0, 1080, 6):
        ph = ((x / 1080) * 2.5 - lt * 1.1) % 1
        y = 960 - (240 if 0.45 < ph < 0.5 else -100 if 0.5 <= ph < 0.55 else 0)
        (ctx.line_to if x else ctx.move_to)(x, y)
    st(ctx, (0.2, 1, 0.5), 7); glow(ctx, 540, 960, 500, (0.2, 1, 0.5), 0.15)
    overlay(ctx, (1, 1, 1), 1 - clamp(lt / 0.6))


def tag_maya(ctx, lt, d):
    ctx.set_source_rgb(*MAYA["top"]); ctx.paint()
    ctx.save(); cam(ctx, 1.0 + 0.1 * sm(lt / d), 540, 960)
    rrect(ctx, 220, 800, 640, 260, 24); fs(ctx, (1, 1, 1), 8)
    text(ctx, "MAYA", 540, 950, 130, col=(0.15, 0.3, 0.5)); text(ctx, "RN - ST. LUKE'S", 540, 1020, 34, col=(0.4, 0.4, 0.45))
    ctx.restore()


SHOTS = {
    "a": SC("a", ["everyone"], [INS(keycard, z=(1.0, 1.1)), cast_shot("corridor", CROWD(), blur=0, z=(1.0, 1.12))]),
    "b": SC("b", ["he", ("i've", 1), ("don't", 1)], [walt_walk, ECU(WALT, M("hopeful", smile=0.3), "corridor", armR=("ik", 90, -250, -1)), ECU(WALT, M("hopeful", smile=0.4), "corridor", "WAL"),
                                                   ECU(WALT, M("happy", tear=0.5), "corridor", "WAL", z=(1.1, 1.25))]),
    "c": SC("c", ["but"], [ECU(MAYA, M("sad"), "corridor", look=0.6), cast_shot("corridor", [(MAYA, 760, 860, 1.4, M("sad"), None, dict(look=-0.8)), (LEO, 380, 920, 1.25, M("scared"), None, dict(look=0.2))], blur=6)]),
    "d": SC("d", [], [ECU(LEO, M("crying", smile=0.2), "corridor", "LEO", tremble=0.7)]),
    "e": SC("e", [("he's", 0, 1), "and"], [ECU(LEO, M("sad", tear=0.6), "corridor"), ECU(LEO, M("crying"), "corridor", tremble=1.0, z=(1.15, 1.3)), ECU(YOU, M("sad", tear=0.5), "corridor")]),
    "f": SC("f", [], [options_card([("A", "Use it yourself"), ("B", "Give it to Walter"), ("C", "Give it to Leo")], [T("f", "use"), T("f", "give"), T("f", "or")], pick=2, pick_t=T("f", "boy") + 0.3)]),
    "g": SC("g", [("you", 0, 1), "and"], [cast_shot("corridor", [(YOU, 640, 960, 1.4, M("sad", smile=0.3), None, dict(look=-0.6)), (LEO, 400, 900, 1.25, M("crying"), None, dict(look=0.6))], blur=6),
                                         INS(hand_key), ECU(LEO, M("shock", tear=0.6), "corridor", lookY=0.6)]),
    "h": SC("h", ["it", "and"], [BGI("stair_door", amp=4, post=lambda c, lt, d: pop_word(c, lt, 0.05, "CLICK", 540, 560, 120, col=(1, 1, 1), life=1.0)), BGI("light_door", z=(1.0, 1.15)),
                                 BGI("light_door", z=(1.15, 1.35), cy=1000, post=lambda c, lt, d: glow(c, 470, 900, 800, (1, 0.95, 0.85), 0.5 * sm(lt / d)))]),
    "i": SC("i", ["then", "and", ("checkout", 1)], [ECU(LEO, M("hopeful", tear=0.4, smile=0.4), "light_door", look=0.6), into_light, tv_msg([(0, "...")]),
                                                   tv_msg([(0, "CHECKOUT"), (0.4, "COMPLETE")])]),
    "j": SC("j", [("beeping", 1), ("a", 1, 0), "morning"], [INS(lambda c, lt, d: c.paint() if c.set_source_rgb(1, 1, 1) is None else None), INS(monitor),
                                                           cast_shot("hospital", [(YOU, 560, 960, 1.4, lambda lt: M("sad", lid=0.98) if lt < 0.6 else M("worried"), None, dict(tint="sun"))], blur=3),
                                                           BGI("hospital", z=(1.2, 1.4), cx=620, cy=800)]),
    "k": SC("k", ["two", ("you", 0, 1), "he"], [ECU(MAYA, M("hopeful", smile=0.4), "hospital", "MAY"), ECU(MAYA, M("hopeful", smile=0.3), "hospital", "MAY", z=(1.1, 1.2)),
                                               ECU(YOU, M("shock", tear=0.5), "hospital"), ECU(LEO, M("joy"), "hospital", armR=("ang", 2.6, 3.1))]),
    "l": SC("l", [("would", 1)], [INS(tag_maya),
                                  END("THE END", [("Would YOU give away the key?", 46, (1, 0.86, 0.15)), ("Follow Paper & Plot", 46, (1, 1, 1)), ("This story is fiction.", 34, (0.8, 0.8, 0.8))], END_T,
                                      base=BGI("hospital", z=(1.1, 1.1)))]),
}
