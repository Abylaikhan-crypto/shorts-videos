exec(open(f"{HERE}/plane_common.py").read())
HEADER = ["WE WILL NOT LAND", "PART 1"]
END_T = LE("l", 0) + 0.3
HOOK = [("\"WE WILL NOT", (1, 1, 1)), ("BE LANDING\"", (1, 0.25, 0.25))]
SCENE_TINT.update({k: "red" for k in "bcdefghijkl"}); SCENE_TINT["a"] = "red"
FUEL_SCENES = set("fghijkl")
HUD = fuel_hud(118, 112)


def LIGHT(sc, t):
    if sc == "a" and t < WT("a", "seat") - 0.06: return dict(amb=(0.9, 0.9, 1.0), bloom=0.8, thr=0.6, vig=0.55)
    return dict(amb=(1.0, 0.95, 0.95), bloom=0.9, thr=0.55, vig=0.6, haze=0.05, lights=[(540, 300, 600, 400, (1, 0.3, 0.2), 0.25)])


SHOTS = {
    "a": SC("a", ["seat", "it's", "you"], [INS(exterior), placard(), PHONE(lock_screen, bg="aisle_red"),
                                           you_ecu(lambda lt: M("sad", lid=0.98) if lt < 0.4 else M("worried", eo=1.2), "row_red", blur=14, dark=0.0)]),
    "b": SC("b", ["nobody", "then"], [aisle(z=(1.0, 1.12)), MED([(PAX[0], 260, 930, 1.3, M("worried"), None, dict(look=0.3)), (PAX[1], 800, 950, 1.3, M("worried"), None, dict(look=-0.2))], "row_red", blur=3),
                                      INS(pa_speaker)]),
    "c": SC("c", ["please", ("we", 0, 0), ("we", 1)], [INS(pa_speaker), aisle(z=(1.05, 1.2)), you_ecu(M("shock", eo=1.4), "row_red", blur=14),
                                                     INS(lambda c, lt, d: BG(c, "door_red", 0), z=(1.0, 1.35), cy=900)]),
    "d": SC("d", ["then"], [aisle(z=(1.1, 1.14)), panic_row]),
    "e": SC("e", [("the", 0, 2), "it's", "over"], [INS(seat_map("route")), INS(seat_map("off")), INS(seat_map("circle")), INS(seat_map("ocean"))]),
    "f": SC("f", ["fuel"], [INS(seat_map("fuel")), INS(fuel_big)]),
    "g": SC("g", [("her", 0, 0), ("her", 0, 1), ("please", 1), ("and", 1)], [aisle(walker=nina_walk, z=(1.0, 1.05)), INS(name_tag_ins),
                                                                           ECU(NINA, M("scared"), "aisle_red", tremble=0.8),
                                                                           ECU(NINA, M("scared", tear=0.3), "door_red", "FA", tremble=0.5), INS(keypad)]),
    "h": SC("h", [], [options_card([("A", "Break into the cockpit"), ("B", "Find a pilot on board"), ("C", "Trust the captain")],
                                   [T("h", "help"), T("h", "find"), T("h", "or")])]),
    "i": SC("i", ["everyone", "he's", "calm", "like"], [you_ecu(M("worried"), "row_red", blur=14, look=-0.6), panic_row, man_seat(), INS(newspaper),
                                                      ECU(MAN, M("cold"), "front_red", lookY=0.6)]),
    "j": SC("j", ["and"], [ECU(MAN, M("cold"), "front_red", z=(1.0, 1.2), look=0.0), ECU(MAN, M("smirk", smile=0.6, eo=0.8), "front_red", z=(1.2, 1.35), look=0.0)]),
    "k": SC("k", [("passenger", 1), ("fourteen", 1), ("alone", 2)], [INS(pa_speaker), you_ecu(M("worried"), "row_red", blur=14), placard(red=True),
                                                                  INS(lambda c, lt, d: BG(c, "door_red", 0), z=(1.2, 1.6), cy=900, amp=2)]),
    "l": SC("l", ["would"], [you_ecu(M("shock", eo=1.6), "row_red", blur=14, vertigo=True, z=(1.0, 1.0)),
                             END("PART 2", [("Would YOU go?", 54, (1, 0.86, 0.15)), ("Follow Paper & Plot", 46, (1, 1, 1)), ("This story is fiction.", 34, (0.8, 0.8, 0.8))], END_T,
                                 base=INS(lambda c, lt, d: BG(c, "door_red", 6), z=(1.3, 1.3), cy=900))]),
}
