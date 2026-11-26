exec(open(f"{HERE}/hor_common.py").read())
HEADER = ["THE 3:07 KNOCK", "FINAL PART"]
END_T = LE("k", 0) + 0.3
BPM = {"a": (140, 145), "b": (145, 140), "c": (140, 150), "d": (150, 156), "e": (150, 156), "f": (156, 162), "g": (150, 140), "h": (130, 95),
       "i": (72, 74), "j": (74, 130), "k": (130, 130)}
def CLK(sc, t):
    if sc == "g": return "3:32 AM" if t >= T("g", "thirty-two") else "3:31 AM"
    return {"a": "3:21 AM", "b": "3:22 AM", "c": "3:24 AM", "d": "3:25 AM", "e": "3:27 AM", "f": "3:29 AM", "h": "3:33 AM", "i": "8:14 AM", "j": "8:16 AM", "k": ""}.get(sc, "")
HUD = hud_bpm_clock(BPM, CLK)
OPTS = [("A", "Hold the door"), ("B", "Hide in the bathroom"), ("C", "Find the last rule")]
cg = T("g", "the") - 0.06
SHOTS = {
    "a": SC("a", [("you", 0, 1), "inside"], [
        options_card(OPTS, [-1, -1, -1], pick=2, pick_t=0.15),
        MED([(YOU, 540, 860, 1.45, M("scared"), None, dict(legs=True, tilt=0.15, dark=0.3, armL=("ang", -1.2, -1.8), armR=("ang", 1.1, 1.7)))], "kitchen_h", blur=0, amp=6),
        INS(salt_ins("jar")),
    ]),
    "b": SC("b", ["pour", "hold"], [
        rule_card(4, "SALT ON|THE DOORWAY"),
        INS(salt_ins("diagram")),
        INS(elevator_ins(clock="3:33")),
    ]),
    "c": SC("c", [("the", 0, 0), ("the", 0, 1)], [
        INS(salt_ins("jar"), z=(1.2, 1.3)),
        INS(chain_ins(fall=True), amp=5),
        knock_door(words=(), open_=lambda lt, d: 0.14 * sm(clamp(lt / d)), figure_gap=1, z=(1.05, 1.2)),
    ]),
    "d": SC("d", ["and"], [
        door_you(M("angry", teeth=True), x=650, push=True, open_=lambda lt, d: 0.12 * (1 - sm(clamp(lt / d))), amp=6),
        INS(salt_ins("pour")),
    ]),
    "e": SC("e", ["long", "all"], [
        knock_door(words=(), scratches=lambda lt, d: 0.3 * lt / d, under=0.4),
        knock_door(words=(), scratches=lambda lt, d: 0.3 + 0.4 * lt / d, under=0.4, z=(2.0, 2.2)),
        knock_door(words=(), scratches=lambda lt, d: 0.7 + 0.3 * lt / d, under=0.4, z=(1.0, 1.08)),
    ]),
    "f": SC("f", [("let", 0, 1), ("let", 0, 2)], [
        you_ecu(M("crying", smile=-0.6), "entry", amp=5),
        knock_door(words=(), red=0.35, z=(1.3, 1.5), scratches=1.0, under=0.4),
        INS(figure_ecu),
    ]),
    "g": SC("g", ["the"], [
        clock_ins([(0, "3:31"), (T("g", "thirty-two") - 0.05, "3:32")]),
        corridor_out([T("g", "one") - cg, T("g", "by") - cg, WT("g", "one", None, 1) - cg]),
    ]),
    "h": SC("h", [("ding", 1)], [
        clock_ins([(0, "3:33")]),
        INS(elevator_ins(ding_t=0.05, clock=None), post=lambda c, lt, d: overlay(c, (0, 0, 0), clamp((lt - 1.2) / 0.5))),
    ]),
    "i": SC("i", [("you", 0, 1), "he"], [
        door_you(M("sad", lid=0.5), x=700, day=True),
        phone_ins(scr_landlord, bg="entry_day"),
        ECU(LANDLORD, M("cold"), "entry_day", "LL", glasses=True, z=(1.0, 1.2)),
    ]),
    "j": SC("j", [("three", 0, 0), ("the", 1, 0), ("you", 1, 0)], [
        phone_ins(scr_cam(ts="03:07"), bg="entry_day"),
        phone_ins(scr_cam(person=you_double, ts="03:07"), bg="entry_day", z=(1.0, 1.25)),
        INS(lambda c, lt, d: cam_feed(c, 0, 0, 1080, 1920, lt, True, person=you_double, zoom=1.6)),
        INS(lambda c, lt, d: cam_feed(c, 0, 0, 1080, 1920, lt, True, person=you_double, zoom=3.2), z=(1.0, 1.1), cy=760, amp=5,
            post=lambda c, lt, d: overlay(c, (1, 0, 0), 0.25 * (int(lt * 8) % 2))),
    ]),
    "k": SC("k", [END_T - 0.4], [
        knock_door(words=(), under=0.8, scratches=1.0, z=(1.0, 1.1)),
        END("THE END", [("Would YOU have opened the door?", 46, (1, 0.86, 0.15)), ("Follow Paper & Plot", 46, (1, 1, 1)), ("This story is fiction.", 34, (0.8, 0.8, 0.8))], END_T,
            base=knock_door(words=(), under=0.8, scratches=1.0, z=(1.1, 1.1))),
    ]),
}

HOOK = [("DON'T LET IT IN", (1, 1, 1)), ('UNTIL', (1, 1, 1)), ('3:33', (1, 0.2, 0.2))]
