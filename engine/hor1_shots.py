exec(open(f"{HERE}/hor_common.py").read())
HEADER = ["THE 3:07 KNOCK", "PART 1"]
END_T = LE("m", 1) + 0.3
BPM = {"a": (70, 95), "b": (95, 100), "c": (100, 105), "d": (105, 110), "e": (110, 110), "f": (110, 116), "g": (105, 100), "h": (108, 115),
       "i": (115, 118), "j": (118, 118), "k": (118, 128), "l": (128, 132), "m": (132, 140)}
CLK = {"a": "3:07 AM", "b": "3:07 AM", "c": "3:07 AM", "d": "3:08 AM", "e": "3:08 AM", "f": "3:08 AM", "g": "3:08 AM", "h": "3:09 AM",
       "i": "3:09 AM", "j": "3:09 AM", "k": "3:10 AM", "l": "3:10 AM", "m": "3:11 AM"}
HUD = hud_bpm_clock(BPM, CLK)
c_to = T("a", "to") - 0.06
c_but = T("d", "but") - 0.06
SHOTS = {
    "a": SC("a", ["you", "to"], [
        clock_ins([(0, "3:07")]),
        you_ecu(lambda lt: M("sad", lid=0.98) if lt < 0.3 else M("shock", eo=1.6), "bedroom_h", amp=0),
        knock_door(words=(0.06, 0.34, 0.62)),
    ]),
    "b": SC("b", ["on", "nobody"], [
        INS(you_bed, post=lambda c, lt, d: V.name_tag(c, lt, 0.05, d - 0.05, "YOU", "lives alone", y=1180)),
        ext_building,
        you_ecu(M("worried"), "bedroom_h"),
    ]),
    "c": SC("c", ["the", "totally"], [
        door_you(M("worried"), x=720),
        peephole(),
        peephole(zoom=1.5, lab="EMPTY"),
    ]),
    "d": SC("d", ["but"], [
        phone_ins(scr_cam(), bg="entry"),
        knock_door(words=(T("d", "doesn't") + 0.2 - c_but, T("d", "doesn't") + 0.48 - c_but, T("d", "doesn't") + 0.76 - c_but)),
    ]),
    "e": SC("e", [], [
        options_card([("A", "Open the door"), ("B", "Call the police"), ("C", "Hide")], [T("e", "open"), T("e", "call"), T("e", "or")], pick=1, pick_t=T("e", "hide") + 0.3),
    ]),
    "f": SC("f", ["no", "your"], [
        phone_ins(lambda c, lt: scr_call(c, lt, 99), bg="entry"),
        phone_ins(lambda c, lt: scr_call(c, lt, 0.0), bg="entry", amp=6),
        you_ecu(M("scared"), "entry", post=lambda c, lt, d: glow(c, 540, 1150, 500, (0.6, 0.8, 1), 0.25)),
    ]),
    "g": SC("g", ["landlord", ("if", 1), "kitchen", ("and", 1)], [
        you_ecu(M("worried", lid=0.4), "entry", look=0.6),
        landlord_flash(lab="move-in day"),
        landlord_flash(talk_=True),
        INS(drawer_ins, post=lambda c, lt, d: (overlay(c, (1, 0.8, 0.5), 0.2), grain(c, lt, 0.12))),
        landlord_flash(lean=True),
    ], whips=(1,)),
    "h": SC("h", ["under", "yellow"], [
        MED([(YOU, 540, 860, 1.4, M("scared"), None, dict(legs=True, tilt=0.25, dark=0.3, armL=("ang", -0.8 + 0.5 * sin(1), -1.1)))], "kitchen_h", blur=0, amp=4, z=(1.0, 1.1)),
        INS(drawer_ins),
        note_ins(z=(0.75, 0.85)),
    ], whips=(0,)),
    "i": SC("i", ["it", ("rule", 1), "do"], [
        rule_card(1, "NEVER OPEN|THE DOOR"),
        note_ins(hl=1, z=(1.0, 1.1), cy=760),
        rule_card(2, "IT KNOWS THE|VOICES YOU LOVE"),
        you_ecu(M("scared"), "kitchen_h", post=L("DO NOT ANSWER", 0.05, 540, 520, 80, -0.04, RED)),
    ]),
    "j": SC("j", [], [note_ins(z=(1.15, 1.3), cy=1250, lab="TORN OFF", lab_y=1660)]),
    "k": SC("k", [("sweetie", 1), ("open", 1), "cold"], [
        you_ecu(M("scared"), "entry", look=-0.9),
        knock_door(words=(), feet=1.0, under=0.95, z=(1.05, 1.25)),
        you_ecu(M("crying", smile=-0.5), "entry", look=-0.9, amp=3),
        peephole(lab="NOBODY"),
    ]),
    "l": SC("l", ["and", "ten"], [
        INS(lambda c, lt, d: phone(c, 540, 980, 2.1, -0.04, scr_mom, lt, 0.3), bg="entry", blur=20, z=(1.3, 1.45), cy=1380),
        INS(lambda c, lt, d: phone(c, 540, 980, 2.1, -0.04, scr_mom, lt, 0.3), bg="entry", blur=20, z=(1.4, 1.6), cy=700),
        you_ecu(M("shock", eo=1.6), "entry", amp=4),
    ]),
    "m": SC("m", [("i", 0, 1), "would"], [
        knock_door(words=(), feet=1.0, red=0.25, z=(1.2, 1.5), under=0.9),
        you_ecu(M("scared", eo=1.6), "entry", amp=6, z=(1.3, 1.6)),
        END("PART 2", [("Would YOU open the door?", 52, (1, 0.86, 0.15)), ("Follow Paper & Plot", 46, (1, 1, 1)), ("This story is fiction.", 34, (0.8, 0.8, 0.8))], END_T,
            base=knock_door(words=(), feet=1.0, red=0.2, z=(1.5, 1.5))),
    ]),
}
