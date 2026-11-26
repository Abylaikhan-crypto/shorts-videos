exec(open(f"{HERE}/hotel_common.py").read())
HEADER = ["CHECKOUT", "PART 2"]
END_T = LE("l", 0) + 0.3
HOOK = [("ONLY ONE", (1, 1, 1)), ("CAN LEAVE.", (1, 1, 1)), ("WHO?", (1, 0.86, 0.15))]
SCENE_TINT.update({"g": "blue"})
HUD = checkout_hud(50, 30, set("abcdefghijkl"))
LIGHT = LIGHT_STD
CROWD = lambda moods={}, look=None: [(c[0], c[1], c[2], c[3], moods.get(c[0]["seed"], M("worried")), None, dict(look=c[4] if look is None else look)) for c in
                                     ((WALT, 200, 880, 1.25, 0.4), (EX1, 380, 820, 0.9, 0.2), (EX2, 700, 820, 0.9, -0.2), (LEO, 540, 940, 1.15, 0), (MAYA, 880, 870, 1.3, -0.4))]
SEPIA = lambda lab=None: (lambda c, lt, d: (overlay(c, (1, 0.8, 0.5), 0.25), grain(c, lt, 0.12), label(c, lt, 0.2, lab, 540, 560, 90) if lab else None))
SHOTS = {
    "a": SC("a", ["the", "nobody", "who's"], [BGI("corridor", post=L("50:00", 0.2, 540, 560, 110, -0.04, (1, 0.35, 0.35))), INS(door_sign), cast_shot("corridor", CROWD(), blur=0),
                                              ECU(LEO, M("scared"), "corridor", tremble=0.6)]),
    "b": SC("b", ["he's", "at", "like"], [ECU(WALT, M("neutral", lid=0.3), "corridor", lookY=0.7), BGI("corridor", z=(2.0, 2.2), cy=1700), BGI("corridor", z=(2.8, 3.0), cy=1750),
                                          ECU(WALT, M("shock"), "corridor")]),
    "c": SC("c", ["forty", ("i", 0, 1), "this"], [ECU(WALT, M("sad"), "corridor", "WAL"), BGI("lobby", post=SEPIA("1986")), ECU(WALT, M("sad", tear=0.4), "corridor", "WAL"), INS(fire_news)]),
    "d": SC("d", [("the", 0, 1), ("then", 1)], [ECU(LEO, M("crying"), "corridor"),
                                               cast_shot("corridor", [(LEO, 380, 900, 1.4, M("crying"), None, dict(armR=("ik", 120, -130, -1))), (MAYA, 720, 860, 1.45, M("sad"), None, dict(armL=("ik", -130, -130, 1)))], blur=6),
                                               ECU(MAYA, M("worried"), "corridor", "MAY")]),
    "e": SC("e", ["every", ("same", 0, 1), ("same", 0, 3)], [ECU(YOU, M("worried"), "room714", blur=16, look=-0.6), BGI("room714"), BGI("room714", z=(1.3, 1.5), cy=1100), INS(stuck_clock)], whips=(2,)),
    "f": SC("f", ["every", ("a", 0, 0)], [ECU(YOU, M("shock"), "corridor"), cast_shot("corridor", CROWD(), blur=0, z=(1.05, 1.12)), INS(ticket)]),
    "g": SC("g", [("i", 1)], [cast_shot("corridor", CROWD({172: M("scared"), 171: M("shock")}), blur=0),
                              BGI("bus_rain", z=(1.0, 1.25), amp=3, post=lambda c, lt, d: (overlay(c, (1, 1, 1), 0.85 * sm(clamp((lt - d + 1.2) / 1.2)), ADD), grain(c, lt, 0.1)))]),
    "h": SC("h", [("thirty", 1)], [BGI("corridor", z=(1.0, 1.1)), tv_msg([(0, "30:00"), (0.6, "ONLY ONE GUEST"), (1.2, "MAY LEAVE")])]),
    "i": SC("i", ["nothing", "walter", ("nothing", 0, 1)], [cast_shot("room714", [(MAYA, 540, 900, 1.4, M("worried"), None, dict(look=0.6, legs=True))], blur=2),
                                                           ECU(MAYA, M("sad"), "room714"), cast_shot("lobby", [(WALT, 540, 880, 1.3, M("worried"), None, dict(lookY=0.6))], blur=2), ECU(WALT, M("sad"), "lobby")]),
    "j": SC("j", ["and"], [ECU(YOU, M("worried"), "corridor", lookY=0.9), ECU(YOU, M("shock", eo=1.4), "corridor", lookY=0.9, z=(1.1, 1.3))]),
    "k": SC("k", [("room", 0, 0), "your", "it", ("everyone", 1)], [INS(keycard), INS(keycard, z=(1.3, 1.5), cy=1000), ECU(YOU, M("shock"), "corridor"), ECU(YOU, M("worried", tear=0.2), "corridor", z=(1.2, 1.4)),
                                                                  cast_shot("corridor", CROWD({172: M("shock"), 171: M("shock"), 170: M("shock")}, look=0.0), blur=0, z=(1.0, 1.18))]),
    "l": SC("l", ["the"], [INS(keycard, z=(1.0, 1.15)),
                           END("PART 3", [("Use it, or give it away?", 50, (1, 0.86, 0.15)), ("Follow Paper & Plot", 46, (1, 1, 1)), ("This story is fiction.", 34, (0.8, 0.8, 0.8))], END_T,
                               base=cast_shot("corridor", CROWD(look=0.0), blur=4, z=(1.15, 1.15)))]),
}
