exec(open(f"{HERE}/house_common.py").read())
HEADER = ["3:07 AM", "PART 1"]
END_T = LE("l", 1) + 0.3
HOOK = [("YOUR SMART SPEAKER", (1, 1, 1)), ("SAYS SOMEONE IS", (1, 1, 1)), ("IN THE HOUSE", (1, 0.86, 0.15))]
HUD = clock_hud(3, 7, 12)
LIGHT = LIGHT_NIGHT
WAKE = lambda lt: M("sad", lid=0.98) if lt < 0.9 else M("shock")
SHOTS = {
    "a": SC("a", ["speaker", "three", "motion", "kitchen"], [ECU(YOU, WAKE, "h_bedroom_dark", dark=0.1), SPEAKER(),
                                                            BGI("h_bedroom_dark", z=(1.0, 1.15), post=L("3:07 AM", 0.1, 540, 560, 130, -0.04, (1, 0.86, 0.15))),
                                                            SPEAKER(z=(1.15, 1.3)), ECU(YOU, M("shock"), "h_bedroom_dark", look=0.5)]),
    "b": SC("b", ["your", "it's", "biscuit"], [BGI("h_hall", z=(1.0, 1.12), post=L("HOME ALONE", 0.2, 540, 560, 110, -0.04, (1, 0.86, 0.15))),
                                               PHONE(scr_chat([("Have fun at the wedding!", True, 0.0), ("Love you. Back Sunday night!", False, 0.6)], title="Mom"), bg="h_bedroom"),
                                               you_dog("h_bedroom", M("happy"), dog_bark=lambda lt: 0.0),
                                               DOG("h_bedroom", look_up=False, post=lambda c, lt, d: V.name_tag(c, lt, 0.1, d, "BISCUIT", "good boy", y=1180))]),
    "c": SC("c", ["he's", "staring", "growling"], [DOG("h_bedroom_dark", look_up=False), dog_at_door, BGI("h_hall", cy=420, z=(1.25, 1.5), dark=0.15),
                                                   DOG("h_bedroom_dark", bark=lambda lt: 0.25 + 0.12 * abs(sin(lt * 22)), amp=2)]),
    "d": SC("d", ["the", "nobody"], [PHONE(scr_kcam, bg="h_bedroom_dark"), BGI("h_kitchen", z=(1.0, 1.15)), BGI("h_kitchen", z=(1.25, 1.45), cx=430,
                                                                                                         post=L("NOBODY?", 0.3, 540, 560, 110, -0.04, (1, 0.35, 0.35)))]),
    "e": SC("e", ["a", "someone"], [BGI("h_kitchen", z=(1.5, 1.75), cx=820, cy=1150), INS(plate_ins),
                                    ECU(YOU, M("scared"), "h_bedroom_dark", tremble=0.5)]),
    "f": SC("f", [("honey", 1), "attic"], [PHONE(scr_voicemsg, bg="h_bedroom_dark", amp=5), PHONE(scr_voicemsg, bg="h_bedroom_dark", z=(1.1, 1.22)),
                                          BGI("h_attic_hatch", z=(1.0, 1.15), post=lambda c, lt, d: (glow(c, 540, 300, 600, (1, 0.8, 0.4), 0.35),
                                                                                                    label(c, lt, 0.2, "attic light: ON", 540, 1250, 80, -0.05, (1, 0.86, 0.15))))]),
    "g": SC("g", ["you", ("all", 1), ("occupants", 1), ("two", 1)], [BGI("h_attic_hatch", z=(1.1, 1.3), dark=0.25), ECU(YOU, M("worried"), "h_bedroom_dark"),
                                                                    PHONE(scr_app(2, 99), bg="h_bedroom_dark"), PHONE(scr_app(2, 0.0), bg="h_bedroom_dark", z=(1.1, 1.25)),
                                                                    SPEAKER(z=(1.2, 1.4), post=lambda c, lt, d: pop_word(c, lt, 0.05, "TWO", 540, 600, 170, col=(1, 0.35, 0.35), life=3))]),
    "h": SC("h", ["you", "someone", ("someone", 0, 1)], [BGI("h_hall", dark=0.35, post=lambda c, lt, d: pop_word(c, lt, 0.05, "2", 540, 900, 400, col=(1, 0.35, 0.35), life=3)),
                                                         ECU(YOU, M("scared"), "h_bedroom_dark", tremble=0.4),
                                                         BGI("h_hall", z=(1.0, 1.15), dark=0.3, post=lambda c, lt, d: shadow_figure(c, 545, 1080, 0.55, 0.55 * sm(clamp(lt / d)), eyes=True)),
                                                         BGI("h_attic_hatch", z=(1.2, 1.5), dark=0.3)]),
    "i": SC("i", ["slow", "moving", "right"], [ECU(YOU, M("scared"), "h_bedroom_dark", lookY=-0.8), BGI("h_bedroom_dark", cy=350, z=(1.2, 1.35), amp=2,
                                                                                                    post=lambda c, lt, d: label(c, lt, 0.2, "creak...", 540, 600, 90)),
                                               BGI("h_hall", cy=420, z=(1.3, 1.6), dark=0.2), BGI("h_hall", z=(1.0, 1.1), dark=0.25)]),
    "j": SC("j", [], [options_card([("A", "Hide in the closet"), ("B", "Run for the front door"), ("C", "Call 911, stay quiet")], [T("j", "hide"), T("j", "run"), T("j", "call")])]),
    "k": SC("k", ["the", "and", "speaker"], [DOG("h_bedroom_dark", bark=lambda lt: abs(sin(lt * 9)), amp=3), BGI("h_hall", cy=420, z=(1.4, 1.45), dark=0.3),
                                             ECU(YOU, M("scared", eo=1.3), "h_bedroom_dark"), SPEAKER(z=(1.0, 1.2))]),
    "l": SC("l", [("what", 1)], [SPEAKER(spk=("HSP",), red=True, z=(1.2, 1.55)),
                                 END("PART 2", [("What would YOU do?", 52, (1, 0.86, 0.15)), ("Follow Paper & Plot", 46, (1, 1, 1)), ("This story is fiction.", 34, (0.8, 0.8, 0.8))], END_T,
                                     base=BGI("h_bedroom_dark", z=(1.1, 1.1), dark=0.2))]),
}
