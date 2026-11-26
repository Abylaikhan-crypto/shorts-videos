exec(open(f"{HERE}/plane_common.py").read())
HEADER = ["WE WILL NOT LAND", "PART 2"]
END_T = LE("l", 1) + 0.3
HOOK = [("WHY DID THE", (1, 1, 1)), ("CAPTAIN", (1, 1, 1)), ("CALL ME?", (1, 0.86, 0.15))]
SCENE_TINT.update({"a": "red", "b": "red", "c": "night", "d": "night", "e": "night", "f": "night", "g": "night", "h": "night", "i": "dark", "j": "dark", "k": "dark", "l": "dark"})
FUEL_SCENES = set("abcdefghijkl")
HUD = fuel_hud(62, 41)


def LIGHT(sc, t):
    if sc in "ab": return dict(amb=(1.0, 0.95, 0.95), bloom=0.9, thr=0.55, vig=0.6, lights=[(540, 300, 600, 400, (1, 0.3, 0.2), 0.25)])
    if sc in "cdefgh": return dict(amb=(0.95, 0.97, 1.05), bloom=1.0, thr=0.5, vig=0.6, lights=[(540, 1000, 500, 400, (0.4, 0.6, 1.0), 0.3)])
    return dict(amb=(0.9, 0.9, 1.0), bloom=1.0, thr=0.5, vig=0.7, haze=0.06, lights=[(540, 400, 500, 500, (1, 0.25, 0.15), 0.35)])


SHOTS = {
    "a": SC("a", ["fourteen", ("you", 0, 1), ("past", 0, 0), ("past", 0, 1), "this"], [
        MED([(PAX[0], 220, 930, 1.3, M("worried"), None, dict(look=0)), (PAX[3], 560, 980, 1.2, M("shock"), None, dict(look=0)), (PAX[1], 880, 930, 1.3, M("worried"), None, dict(look=0))], "row_red", blur=3),
        placard(red=True), aisle(walker=you_walk, z=(1.0, 1.06)), ECU(NINA, M("worried"), "aisle_red", look=0.6), ECU(MAN, M("cold"), "front_red", lookY=0.8), man_seat()]),
    "b": SC("b", ["just"], [INS(lambda c, lt, d: BG(c, "door_red", 0), z=(1.0, 1.25), cy=900), door_crack]),
    "c": SC("c", [("the", 0, 1), "breathing"], [ECU(CAPT, M("worried"), "cockpit", look=0.4), ECU(COPI, M("sad", lid=1.0), "cockpit", blink=True, tilt=0.4),
                                                cockpit_shot(z=(1.0, 1.08))]),
    "d": SC("d", [("i", 0, 0)], [ECU(CAPT, M("worried"), "cockpit", "CP"), ECU(CAPT, M("worried", sweat=1), "cockpit", "CP", z=(1.1, 1.25), sweat=True)]),
    "e": SC("e", ["landing"], [cockpit_shot(z=(1.2, 1.5), cy=1050), INS(gear_panel("red"))]),
    "f": SC("f", ["nobody", ("the", 0, 1), "is"], [ECU(CAPT, M("worried"), "cockpit", "CP"), INS(belly), INS(pax_list), you_ecu(M("shock"), "cockpit", blur=18)]),
    "g": SC("g", [("you", 0, 0), "but"], [you_ecu(M("worried"), "cockpit", blur=18),
                                         INS(lambda c, lt, d: (BG(c, "bay", 8), overlay(c, (1, 0.8, 0.5), 0.25), label(c, lt, 0.3, "6 years ago", 540, 560, 76))),
                                         you_ecu(M("cold", eo=0.9), "cockpit", blur=18, z=(1.0, 1.15))]),
    "h": SC("h", ["it", ("there's", 0, 1), "pull"], [ECU(CAPT, M("worried"), "cockpit", "CP"), INS(hatch_ins()), bay_shot(you=False, z=(1.0, 1.25)), INS(lever_ins())]),
    "i": SC("i", [("it's", 0, 1), "and"], [bay_shot(ladder=True), bay_shot(amp=8, mood=M("scared")), you_ecu(M("scared", tremble=0.8), "bay", blur=14, tremble=1.0)]),
    "j": SC("j", [("you", 0, 0), "something"], [bay_shot(flash=True, look=0.8), you_ecu(M("angry", teeth=True), "bay", blur=14, amp=5), INS(lever_ins(jam=True))]),
    "k": SC("k", ["you", "there's", "seat"], [INS(case_ins("front")), INS(case_ins("turn")), INS(case_ins("tag")), INS(case_ins("tag"), z=(1.5, 1.8), cy=820)]),
    "l": SC("l", [("you", 0, 1), ("fuel", 1), "what"], [INS(hatch_from_below(0.25)), INS(lock_ins), INS(fuel_num("0:41")),
        END("PART 3", [("What would YOU do?", 54, (1, 0.86, 0.15)), ("Follow Paper & Plot", 46, (1, 1, 1)), ("This story is fiction.", 34, (0.8, 0.8, 0.8))], END_T,
            base=bay_shot(you=False, z=(1.2, 1.2)))]),
}
