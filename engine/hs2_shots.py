exec(open(f"{HERE}/house_common.py").read())
HEADER = ["3:07 AM", "PART 2"]
END_T = LE("l", 1) + 0.3
HOOK = [("SOMEONE IS", (1, 1, 1)), ("LIVING IN", (1, 1, 1)), ("YOUR ATTIC", (1, 0.86, 0.15))]
LIGHT = LIGHT_NIGHT
_K = list(TL); _T0 = WT("c", "eight", 1); _T4 = WT("h", "four", 1)
def _el(sc, t):   # story seconds since "eight minutes"
    s = 0.0
    for k in _K:
        if k == sc: return s + t
        s += DUR(k)
_E0, _E4 = _el("c", _T0), _el("h", _T4)
def HUD(ctx, sc, t):
    e = _el(sc, t)
    if e < _E0: return
    m = max(0.5, 8 - 4 * (e - _E0) / (_E4 - _E0))
    rrect(ctx, 600, 200, 420, 76, 38); ctx.set_source_rgba(0.55, 0, 0, 0.75); ctx.fill()
    text(ctx, f"POLICE IN {int(m)}:{int((m % 1) * 60):02d}", 810, 254, 34, col=(1, 1, 1))
HALE_SIT = lambda mood=M("neutral"), look=0.0, spk=None, x=560, s=1.0: (HALE, x, 1000, s, mood, spk, dict(look=look))
YOU_GRAY = dict(YOU, top=HALE["top"])
SHOTS = {
    "a": SC("a", ["slip", "through"], [you_dog("h_bedroom_dark", M("scared"), hug=True), BGI("h_closet", z=(1.0, 1.15)), CLOSET()]),
    "b": SC("b", ["your", ("nine", 1)], [PHONE(scr_911, bg="h_closet"), ECU(YOU, M("scared"), "h_closet", dark=0.3, tremble=1.0),
                                         PHONE(scr_911, bg="h_closet", z=(1.1, 1.25))]),
    "c": SC("c", [("officers", 1), ("eight", 1), ("stay", 1)], [ECU(YOU, M("scared"), "h_closet", dark=0.35, tremble=0.6), PHONE(scr_911, bg="h_closet"),
                                                                 BGI("h_closet", dark=0.3, post=L("8 MINUTES", 0.1, 540, 700, 120, -0.04, (1, 0.35, 0.35))), CLOSET()]),
    "d": SC("d", ["ladder", "one", "two", "three"], [BGI("h_attic_hatch", z=(1.0, 1.1), dark=0.25), BGI("h_attic_hatch", z=(1.2, 1.3), amp=2, dark=0.25),
                                                     CLOSET(post=lambda c, lt, d: label(c, lt, 0.05, "creak", 300, 600, 80)), ECU(YOU, M("scared", eo=1.3), "h_closet", dark=0.35),
                                                     CLOSET(post=lambda c, lt, d: label(c, lt, 0.05, "creak", 780, 700, 80))]),
    "e": SC("e", [("a", 0, 1), "long", "and", "the"], [walk_shot(HALE, "h_bedroom_dark", 1200, 700, 820, 0.8, 0.8, dark=0.55, post=lambda c, lt, d: slats(c, lt)),
                                                        CLOSET([(HALE, 560, 820, 0.9, M("neutral"), None, dict(legs=True))], z=(1.1, 1.2)),
                                                        ECU(HALE, M("neutral", lid=0.4), "h_bedroom_dark", dark=0.15),
                                                        cast_shot("h_bedroom_dark", [(HALE, 540, 900, 1.5, M("neutral"), None, {})], blur=6,
                                                                  post=lambda c, lt, d: label(c, lt, 0.2, "YOUR hoodie", 540, 520, 100, -0.05, (1, 0.86, 0.15))),
                                                        cast_shot("h_bedroom", [(YOU_GRAY, 540, 900, 1.45, M("happy"), None, {})], blur=4, post=sepia("last month"))]),
    "f": SC("f", ["the", "your", ("the", 0, 1)], [ECU(YOU, M("shock"), "h_closet", dark=0.3), BGI("h_kitchen", post=sepia("missing food")),
                                                  cast_shot("h_bedroom", [(YOU, 540, 900, 1.45, M("worried"), None, dict(look=0.5))], blur=4, post=sepia("where's my hoodie?")),
                                                  BGI("h_bedroom_dark", cy=350, z=(1.2, 1.35), post=sepia("just the old house..."))]),
    "g": SC("g", ["he", "like", ("i", 1)], [CLOSET([(HALE, 540, 820, 0.85, M("neutral"), None, dict(legs=True))]),
                                            BGI("h_bedroom_dark", z=(1.3, 1.4), dark=0.3, post=lambda c, lt, d: (pop_word(c, lt, 0.1, "knock", 380, 800, 110, col=(1, 1, 1), life=0.6),
                                                                                                              pop_word(c, lt, 0.9, "knock", 700, 1000, 110, col=(1, 1, 1), life=0.6))),
                                            ECU(YOU, M("scared", eo=1.3), "h_closet", dark=0.35, tremble=0.6), ECU(HALE, M("neutral"), "h_bedroom_dark", "HALE", dark=0.2)]),
    "h": SC("h", ["you", "the", ("four", 1)], [DOG("h_closet", bark=lambda lt: 0.2 + 0.1 * abs(sin(lt * 20)), dark=0.35), muzzle, PHONE(scr_911, bg="h_closet"),
                                               PHONE(scr_911, bg="h_closet", z=(1.15, 1.3), post=L("4 MINUTES", 0.05, 540, 520, 110, -0.04, (1, 0.35, 0.35)))]),
    "i": SC("i", [("the", 0, 1), "then", ("this", 1)], [BGI("h_bedroom_dark", z=(1.3, 1.5), dark=0.25), CLOSET([HALE_SIT()]), CLOSET([HALE_SIT(M("sad"), 0.5)], z=(1.1, 1.2)),
                                                       ECU(HALE, M("sad"), "h_bedroom_dark", "HALE", dark=0.15)]),
    "j": SC("j", [], [options_card([("A", "Stay in the closet"), ("B", "Run past him"), ("C", "Let Biscuit out")], [T("j", "stay"), T("j", "run"), T("j", "let")])]),
    "k": SC("k", ["a", "and"], [PHONE(scr_mom_text, bg="h_closet", amp=4), PHONE(scr_mom_text, bg="h_closet", z=(1.1, 1.2)),
                                CLOSET([HALE_SIT()], phone_glow=lambda lt, d: 1.0)]),
    "l": SC("l", ["slowly", "and", ("what", 1)], [CLOSET([HALE_SIT(look=-0.6)], phone_glow=lambda lt, d: 1.0, z=(1.0, 1.1)),
                                                  CLOSET([HALE_SIT()], eyes=lambda lt, d: sm(clamp(lt / d * 1.5)), phone_glow=lambda lt, d: 1.0),
                                                  ECU(HALE, M("happy", smile=0.5, lid=0.3), "h_bedroom_dark", dark=0.25, z=(1.1, 1.35)),
                                                  END("FINAL PART", [("Stay, run, or let the dog out?", 46, (1, 0.86, 0.15)), ("Follow Paper & Plot", 46, (1, 1, 1)),
                                                                     ("This story is fiction.", 34, (0.8, 0.8, 0.8))], END_T, base=BGI("h_closet", z=(1.1, 1.1), dark=0.3))]),
}
