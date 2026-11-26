exec(open(f"{HERE}/plane_common.py").read())
HEADER = ["WE WILL NOT LAND", "FINAL PART"]
END_T = LE("l", 0) + 0.3
HOOK = [("LOCKED UNDER", (1, 1, 1)), ("THE PLANE", (1, 1, 1)), ("38 MIN OF FUEL", (1, 0.25, 0.25))]
SCENE_TINT.update({"a": "dark", "b": "dark", "c": "dark", "d": "red", "e": "red", "f": "red", "g": "red", "h": "red", "i": "night", "j": "dawn", "k": "dawn", "l": "dawn"})
FUEL_SCENES = set("abcdefghi")
HUD = fuel_hud(38, 7)


def LIGHT(sc, t):
    if sc in "abc": return dict(amb=(0.9, 0.9, 1.0), bloom=1.0, thr=0.5, vig=0.7, haze=0.06, lights=[(540, 400, 500, 500, (1, 0.25, 0.15), 0.35)])
    if sc in "defgh": return dict(amb=(1.0, 0.95, 0.95), bloom=0.9, thr=0.55, vig=0.6, lights=[(540, 300, 600, 400, (1, 0.3, 0.2), 0.25)])
    if sc == "i": return dict(amb=(1.0, 1.0, 1.05), bloom=0.7, thr=0.6, vig=0.5)
    if sc in "jl": return dict(amb=(0.78, 0.74, 0.72), bloom=0.45, thr=0.75, vig=0.55)
    return dict(amb=(1.05, 0.98, 0.92), bloom=0.9, thr=0.55, vig=0.5, lights=[(800, 500, 600, 600, (1, 0.6, 0.3), 0.4)])


SHOTS = {
    "a": SC("a", ["nobody"], [bay_shot(z=(1.0, 1.1)), you_ecu(M("angry", teeth=True), "bay", blur=14, amp=8, post=lambda c, lt, d: [pop_word(c, lt, k * 0.5, "BANG", 300 + 480 * (k % 2), 600, 110, col=(1, 1, 1), life=0.4) for k in range(6)])]),
    "b": SC("b", ["you"], [INS(fuel_num("0:38")), options_card([("A", "Wait for help"), ("B", "Break the hatch"), ("C", "Fix the wheels")],
                                                               [T("b", "wait") - T("b", "you") + 0.06, T("b", "try") - T("b", "you") + 0.06, T("b", "or") - T("b", "you") + 0.06],
                                                               pick=2, pick_t=T("b", "now") - T("b", "you") + 0.3)]),
    "c": SC("c", [("the", 0, 1), "but", ("you", 0, 1), "hard"], [you_ecu(M("cold", eo=0.9), "bay", blur=14), INS(case_ins("front"), amp=4), INS(case_ins("front"), z=(1.4, 1.6), cy=700),
                                                                INS(lever_ins(jam=True, handle=True)), you_ecu(M("angry", teeth=True, flush=1), "bay", blur=14, amp=8)]),
    "d": SC("d", ["the", "and"], [INS(lever_ins(jam=False, handle=True, snap_t=0.1)), aisle(panic=1.0, amp=14), INS(gear_drop)]),
    "e": SC("e", ["she", "it's"], [ECU(NINA, M("shock"), "aisle_red", look=-0.5), INS(hatch_ins()), INS(hatch_ins("jammed"))]),
    "f": SC("f", ["the", ("sit", 1), ("and", 1)], [ECU(NINA, M("worried"), "front_red", look=1), ECU(MAN, M("cold"), "front_red", z=(1.0, 1.15), lookY=-0.2),
                                                  ECU(MAN, M("angry", eo=0.8), "front_red", "MAN", z=(1.1, 1.25)), ECU(NINA, M("scared", tear=0.3), "front_red", tremble=0.8)]),
    "g": SC("g", ["and"], [MED([(PAX[i], x, 880, 1.25, M("angry"), None, dict(legs=True)) for i, x in enumerate((150, 400, 680, 930))], "front_red", blur=4), tackle]),
    "h": SC("h", ["nina", "and"], [INS(hatch_ins("open")), nina_pull, INS(gear_panel("green"))]),
    "i": SC("i", ["please", "we"], [INS(pa_speaker), aisle("night", z=(1.0, 1.06)), you_ecu(M("hopeful", tear=0.4, smile=0.4), "aisle_night", blur=14)]),
    "j": SC("j", [("the", 0, 0), ("the", 0, 3)], [INS(fuel_num("0:06")), INS(lambda c, lt, d: BG(c, "runway_dawn", 0), z=(1.0, 1.25), cy=1000, amp=4),
                                                aisle("night", panic=1.0, post=lambda c, lt, d: [pop_word(c, lt, 0.2 + k * 0.4, w, 280 + 520 * (k % 2), 600 + 80 * k, 100, col=(1, 1, 1), life=0.8) for k, w in enumerate(("YES!", "WE MADE IT!", "WOO!"))])]),
    "k": SC("k", [("for", 0, 0), "it", ("fourteen", 1)], [police, ECU(MAN, M("sad"), "aisle_night", lookY=0.7), INS(case_ins("gold")), ECU(CAPT, M("happy"), "aisle_night", "CP")]),
    "l": SC("l", [END_T - 0.4], [INS(lambda c, lt, d: BG(c, "runway_dawn", 0), z=(1.1, 1.18), cy=1000),
        END("THE END", [("Would YOU have gone down there?", 46, (1, 0.86, 0.15)), ("Follow Paper & Plot", 46, (1, 1, 1)), ("This story is fiction.", 34, (0.8, 0.8, 0.8))], END_T,
            base=INS(lambda c, lt, d: BG(c, "runway_dawn", 4), z=(1.18, 1.18), cy=1000))]),
}
