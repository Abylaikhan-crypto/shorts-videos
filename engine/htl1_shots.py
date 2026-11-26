exec(open(f"{HERE}/hotel_common.py").read())
HEADER = ["CHECKOUT", "PART 1"]
END_T = LE("l", 1) + 0.3
HOOK = [("YOU WAKE UP", (1, 1, 1)), ("IN A HOTEL", (1, 1, 1)), ("YOU NEVER BOOKED", (1, 0.86, 0.15))]
SCENE_TINT.update({"j": "dark"})
HUD = checkout_hud(60, 50, set("cdefghijkl"))
LIGHT = LIGHT_STD
CROWD = lambda moods={}, skip=(): [(c[0], c[1], c[2], c[3], moods.get(c[0]["seed"], M("worried")), None, dict(look=c[4])) for c in
                                  ((WALT, 200, 880, 1.25, 0.4), (EX1, 380, 820, 0.9, 0.2), (EX2, 700, 820, 0.9, -0.2), (LEO, 540, 940, 1.15, 0), (MAYA, 880, 870, 1.3, -0.4), (GRANT, 330, 860, 1.2, 0.3)) if c[0]["seed"] not in skip]


def phone_dead(ctx, lt):
    ctx.set_source_rgb(0.02, 0.02, 0.03); ctx.paint()
    rrect(ctx, -60, -40, 110, 60, 8); st(ctx, (0.8, 0.15, 0.15), 6); ctx.rectangle(50, -20, 10, 20); ctx.set_source_rgb(0.8, 0.15, 0.15); ctx.fill()
    ctx.rectangle(-52, -32, 14, 44); ctx.set_source_rgb(0.8, 0.15, 0.15); ctx.fill()
    text(ctx, "0%", 0, 90, 40, col=(0.8, 0.15, 0.15))


SHOTS = {
    "a": SC("a", ["room", "the", "bus"], [ECU(YOU, lambda lt: M("sad", lid=0.98) if lt < 0.5 else M("shock"), "room714", blur=16),
                                          BGI("corridor", z=(1.3, 1.45), cy=900, post=L("ROOM 714", 0.2, 540, 560, 100, -0.04, (1, 0.86, 0.15))),
                                          cast_shot("room714", [(YOU, 540, 950, 1.35, M("worried"), None, dict(look=0.3))], blur=2),
                                          BGI("bus_rain", z=(1.0, 1.15), post=lambda c, lt, d: (overlay(c, (1, 0.8, 0.5), 0.2), grain(c, lt, 0.12), label(c, lt, 0.2, "last night", 540, 560, 80)))]),
    "b": SC("b", ["the", "and"], [PHONE(phone_dead, bg="room714"), BGI("window_fog"), BGI("window_fog", z=(1.2, 1.5), cy=800)]),
    "c": SC("c", [("good", 1), ("checkout", 1), ("please", 1)], [BGI("room_tv", z=(1.0, 1.2), post=lambda c, lt, d: overlay(c, (0.5, 0.7, 1), 0.5 * (1 - clamp(lt / 0.2)), ADD)),
                                                               tv_msg([(0, "GOOD EVENING,"), (0.5, "GUESTS")]), tv_msg([(0, "CHECKOUT IN"), (0.6, "60:00")]),
                                                               tv_msg([(0, "ONLY ONE GUEST"), (0.8, "MAY LEAVE")])]),
    "d": SC("d", ["the", "and"], [ECU(YOU, M("worried"), "corridor", blur=16, look=0.6), BGI("corridor", z=(1.0, 1.15)), cast_shot("corridor", CROWD(skip=(91,)), blur=0, z=(1.0, 1.06))]),
    "e": SC("e", [("a", 0, 0), "an", ("a", 0, 2), ("a", 0, 4)], [cast_shot("corridor", CROWD(), blur=0, z=(1.05, 1.1)),
                                                                ECU(MAYA, M("worried"), "corridor", post=lambda c, lt, d: V.name_tag(c, lt, 0.1, d, "MAYA", "nurse", y=1180)),
                                                                ECU(WALT, M("neutral"), "corridor", post=lambda c, lt, d: V.name_tag(c, lt, 0.1, d, "WALTER", "old man", y=1180)),
                                                                ECU(GRANT, M("angry"), "corridor", armL=("ik", -60, -330, 1), post=lambda c, lt, d: V.name_tag(c, lt, 0.1, d, "GRANT", "businessman", y=1180)),
                                                                ECU(LEO, M("scared"), "corridor", post=lambda c, lt, d: V.name_tag(c, lt, 0.1, d, "LEO", "14 years old", y=1180))]),
    "f": SC("f", ["somebody", "i"], [ECU(GRANT, M("angry", flush=0.6), "corridor", "GR"), cast_shot("corridor", [(GRANT, 540, 860, 1.6, M("angry", flush=0.8), "GR", dict(armR=("ang", 0.4, 0.1)))], blur=4),
                                     ECU(GRANT, M("angry", flush=1.0, bi=15), "corridor", "GR", amp=6)]),
    "g": SC("g", [("the", 0, 1), "it"], [BGI("elevator", post=lambda c, lt, d: (c.save(), c.translate(540, 560), c.rotate(-0.05), rrect(c, -300, -60, 600, 120, 14), fs(c, (0.95, 0.9, 0.8), 5),
                                                                                    text(c, "OUT OF SERVICE", 0, 22, 56, col=(0.75, 0.1, 0.1)), c.restore())),
                                         BGI("stair_door", post=L("LOCKED", 0.2, 540, 560, 100, -0.04, (1, 0.35, 0.35))), BGI("stair_door", z=(1.8, 2.1), cx=790, cy=900, post=L("KEY CARD", 0.1, 540, 560, 90, -0.04, (1, 0.86, 0.15)))]),
    "h": SC("h", ["we", "nobody"], [ECU(MAYA, M("worried"), "corridor", "MAY"), cast_shot("corridor", CROWD(skip=()), blur=0, z=(1.05, 1.1)), ECU(MAYA, M("cold", eo=0.9), "corridor", "MAY")]),
    "i": SC("i", [], [options_card([("A", "Search the rooms"), ("B", "Break the door"), ("C", "Go back and wait")], [T("i", "search"), T("i", "break"), T("i", "or")])]),
    "j": SC("j", ["the", "total", "somebody"], [cast_shot("corridor", CROWD(), blur=0), cast_shot("corridor", CROWD(), blur=0, darkness=lambda lt, d: 0.95 * (1 - flick(CUR["t"], 9) * (1 - clamp(lt / d)))),
                                               BGI("corridor_dark", dark=0.6), BGI("corridor_dark", dark=0.85, post=lambda c, lt, d: pop_word(c, lt, 0.05, "AAAH!", 540, 800, 150, col=(1, 1, 1), life=1.5))]),
    "k": SC("k", [("the", 0, 1), "his", "and"], [cast_shot("corridor", CROWD(skip=(173,)), blur=0, post=lambda c, lt, d: overlay(c, (1, 1, 1), 0.7 * (1 - clamp(lt / 0.25)), ADD)),
                                                cast_shot("corridor", CROWD({170: M("shock"), 171: M("shock"), 172: M("scared")}, skip=(173,)), blur=0, z=(1.05, 1.15)),
                                                BGI("corridor", z=(1.4, 1.7), cx=330, cy=900), INS(door_sign)]),
    "l": SC("l", [("who", 1)], [INS(door_sign, z=(1.1, 1.3)),
                                END("PART 2", [("Who would YOU trust?", 52, (1, 0.86, 0.15)), ("Follow Paper & Plot", 46, (1, 1, 1)), ("This story is fiction.", 34, (0.8, 0.8, 0.8))], END_T,
                                    base=BGI("corridor_dark", z=(1.1, 1.1)))]),
}
