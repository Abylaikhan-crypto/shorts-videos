exec(open(f"{HERE}/hor_common.py").read())
HEADER = ["THE 3:07 KNOCK", "PART 2"]
END_T = LE("k", 1) + 0.3
BPM = {"a": (120, 125), "b": (125, 110), "c": (105, 80), "d": (80, 88), "e": (92, 115), "f": (112, 105), "g": (105, 116), "h": (116, 126),
       "i": (126, 132), "j": (132, 142), "k": (142, 148)}
CLK = {"a": "3:12 AM", "b": "3:13 AM", "c": "3:14 AM", "d": "3:15 AM", "e": "3:15 AM", "f": "3:16 AM", "g": "3:17 AM", "h": "3:17 AM",
       "i": "3:18 AM", "j": "3:19 AM", "k": "3:20 AM"}
HUD = hud_bpm_clock(BPM, CLK)
cb = T("b", "breathe"); ch_ = T("b", "hold"); co = T("b", "out")
c_c = T("c", "the") - 0.06
c_g = 0.0
SHOTS = {
    "a": SC("a", ["one", "and"], [
        you_ecu(M("scared", eo=1.5), "entry", amp=6),
        INS(bpm_ins([(0, 120)])),
        knock_door(words=(), feet=1.0, under=0.9, z=(1.05, 1.2)),
    ]),
    "b": SC("b", [], [breathe_ecu([(cb, "IN", ch_ - cb), (ch_, "HOLD", co - ch_), (co, "OUT", 1.6)])]),
    "c": SC("c", ["the"], [
        INS(bpm_ins([(0, 100), (T("c", "ninety") - 0.05, 90), (T("c", "eighty") - 0.05, 80)])),
        knock_door(words=(T("c", "gets") - c_c,), z=(1.0, 0.95), under=0.6),
    ]),
    "d": SC("d", ["it's"], [
        tv_scene(on_t=T("d", "turns") - 0.06),
        tv_scene(on_t=-1, close=True),
    ]),
    "e": SC("e", ["something", ("too", 0, 0)], [
        tv_scene(on_t=-1, close=True, lit=lambda t: flick(t, 5) > 0.5, figure=lambda lt: 1.0 if flick(CUR["t"], 5) < 0.5 else 0.0),
        tv_scene(on_t=-1, close=True, zoom=1.6, lit=lambda t: flick(t, 5) > 0.5, figure=lambda lt: 1.0 if flick(CUR["t"], 5) < 0.5 else 0.0),
        tv_scene(on_t=-1, close=True, zoom=2.3, lit=lambda t: False, figure=lambda lt: 1.0),
    ]),
    "f": SC("f", ["stuck", ("rule", 1), ("come", 1), ("not", 1)], [
        MED([(YOU, 640, 880, 1.5, M("worried"), None, dict(look=1, dark=0.3, legs=True))], "kitchen_h", blur=0),
        note_ins(lines=["3. It will try to make", "   you say COME IN.", "   Don't say ANYTHING."], scrap=True, z=(0.95, 1.1)),
        rule_card(3, "DON'T SAY|ANYTHING"),
        note_ins(lines=["3. It will try to make", "   you say COME IN.", "   Don't say ANYTHING."], scrap=True, hl=1, z=(1.3, 1.5), lab="NOT ONE WORD"),
        you_ecu(M("scared", eo=1.4), "kitchen_h", armL=("ik", 30, -300, 1), armR=("ik", -30, -295, -1)),
    ]),
    "g": SC("g", ["then", ("honey", 1), ("i", 1)], [
        knock_door(words=(T("g", "knock") - 0.0, WT("g", "knock", None, 1) - 0.0)),
        you_ecu(M("worried"), "entry", look=-0.8),
        knock_door(words=(), feet=1.0, under=0.95, z=(1.05, 1.2)),
        peephole(lab="NOBODY"),
    ]),
    "h": SC("h", ["then", "nine"], [
        you_ecu(M("worried", mo=0.5), "entry", look=-0.8),
        you_ecu(M("shock", eo=1.4), "entry", amp=3),
        INS(lambda c, lt, d: BG(c, "corridor_9b", 0), z=(1.0, 1.25), cy=1000, post=L("6 years", 0.3, 540, 560, 90, -0.05, RED)),
    ]),
    "i": SC("i", [("you", 1)], [
        knock_door(words=(), red=0.3, z=(1.2, 1.4), feet=1.0),
        INS(figure_ecu),
    ]),
    "j": SC("j", [("the", 0, 0)], [
        you_ecu(M("scared"), "entry", look=-1),
        INS(chain_ins(slide=lambda lt, d: sm(clamp(lt / d)))),
    ]),
    "k": SC("k", ["comment"], [
        options_card([("A", "Hold the door"), ("B", "Hide in the bathroom"), ("C", "Find the last rule")], [T("k", "a"), T("k", "b"), T("k", "c")]),
        END("PART 3", [("Comment A, B or C", 54, (1, 0.86, 0.15)), ("Follow Paper & Plot", 46, (1, 1, 1)), ("This story is fiction.", 34, (0.8, 0.8, 0.8))], END_T,
            base=options_card([("A", "Hold the door"), ("B", "Hide in the bathroom"), ("C", "Find the last rule")], [-1, -1, -1])),
    ]),
}

HOOK = [('IT CAN HEAR', (1, 1, 1)), ('YOUR', (1, 1, 1)), ('HEARTBEAT', (1, 0.2, 0.2))]
