"""The New Girl Knew All My Secrets — Part 2."""
import json, os, sys, cairo
from math import sin, cos, pi
from rig import *
import part1 as P1
import part1v2 as V
from part1 import ik
from twins_common import notebook_cu, pencil, hallway_school
from ng_common import *
import ng_part1 as N1

HERE = os.path.dirname(os.path.abspath(__file__))
EP = f"{HERE}/ng2"
TL = {s["id"]: s for s in json.load(open(f"{EP}/timeline.json"))}
V.TL = TL; V.EP = EP
P1.HEADER[:] = ["THE NEW GIRL KNEW MY SECRETS", "PART 2"]
MT = mood_at
talk = V.talk


def LS(sc, i): return TL[sc]["lines"][i]["start"]
def LE(sc, i): l = TL[sc]["lines"][i]; return l["start"] + l["dur"]
def Wd(sc, i, j): return TL[sc]["lines"][i]["words"][j][1]
def DUR(sc): return TL[sc]["dur"]
def zoomed(ctx, z, cx=540, cy=960): ctx.translate(540, 960); ctx.scale(z, z); ctx.translate(-cx, -cy)
hall = lambda c_, tt_: hallway_school(c_, tt_, sign="MAPLE RIDGE HIGH")


def garage(ctx, t, bear_cut=0.0, dev_talk=False, dev_mood="neutral", mia_mood="worried"):
    workbench(ctx, t)
    draw_char(ctx, MIA, dict(x=260, y=1470, s=1.3, mood=mia_mood, look=0.7, blink=blinking(t, 31)), t)
    d = dict(x=780, y=1470, s=1.35, mood=dev_mood, look=-0.5, lookY=0.6, glasses=True, mouth=talk("b", "D", t) if dev_talk else 0, blink=blinking(t, 33))
    d["armL"] = ik(d, 560, 1280, 1); d["armR"] = ik(d, 680, 1290, -1)
    draw_char(ctx, DEV, d, t)
    bear(ctx, 560, 1230, 0.9, t)
    bench_front(ctx)


# ---------- A: recap ----------
def a(ctx, t):
    tRed = Wd("a", 0, 17)
    ctx.save(); zoomed(ctx, 2.2 + 0.4 * sm(t / DUR("a")), 860, 1080)
    desk_room(ctx, t, night=True, bear_red=ramp(t, tRed - 0.1, tRed + 0.1))
    desk_front(ctx, t, open_=False)
    ctx.restore()
    overlay(ctx, (0.0, 0.0, 0.08), 0.25)
    vignette(ctx, 0.55)


# ---------- B: Dev finds the camera ----------
def b(ctx, t):
    t1, t2, t3, t4, t5 = LS("b", 1), LS("b", 2), LS("b", 3), LS("b", 4), LS("b", 5)
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * t, 540, 1080); garage(ctx, t, mia_mood="worried", dev_mood="happy"); ctx.restore()
        V.name_tag(ctx, t, 1.5, t1 - 0.2, "DEV", "my only friend")
    elif t < t3 - 0.03:
        ctx.save(); zoomed(ctx, 1.4 + 0.05 * (t - t1), 620, 1150)
        garage(ctx, t, dev_talk=True, dev_mood=MT([(t1, dict(MOODS["neutral"], bi=-6, bo=4)), (t2, "neutral")], t), mia_mood=MT([(t1, "worried"), (Wd("b", 2, 9), dict(MOODS["sad"], tear=0.6))], t))
        ctx.restore()
    elif t < t4 - 0.03:
        chip_cu(ctx, t, (t - t3) / (t4 - t3))
        V.flash(ctx, t, Wd("b", 3, 3), (1, 1, 1), 0.15, 0.3)
    elif t < t5 - 0.03:
        bearcam(ctx, t, lambda c_, tt_: N1.mia_writing(c_, tt_, mood="neutral"), stamp="11:47 PM")
    else:
        char_ecu(ctx, t, DEV, (t - t5) / (DUR("b") - t5), dict(MOODS["worried"], ew=1, eo=1.1), workbench, mouth=talk("b", "D", t), look=-0.4, glasses=True)
    vignette(ctx, 0.4)


# ---------- C: who gave the bear ----------
def c(ctx, t):
    t1, t2, t3 = LS("c", 1), LS("c", 2), LS("c", 3)
    if t < t1 - 0.03:
        char_ecu(ctx, t, DEV, t / t1, "neutral", workbench, mouth=talk("c", "D", t), look=-0.4, glasses=True)
    elif t < t2 - 0.03:
        def party(c_, tt_):
            c_.set_source_rgb(0.98, 0.88, 0.75); c_.paint()
            for k in range(10):
                x = 60 + k * 105; c_.move_to(x, 300); c_.line_to(x + 50, 380); c_.line_to(x + 100, 300); c_.close_path(); c_.set_source_rgb(*[(1, 0.5, 0.5), (0.5, 0.7, 1), (1, 0.85, 0.3)][k % 3]); c_.fill()
        ctx.save(); zoomed(ctx, 1.0 + 0.05 * (t - t1), 540, 1050)
        party(ctx, t)
        draw_char(ctx, MIA, dict(x=330, y=1500, s=1.35, mood="joy", look=0.7), t)
        ch = dict(x=760, y=1500, s=1.35, mood=dict(MOODS["happy"], smile=0.8), look=-0.7); ch["armL"] = ik(ch, 560, 1250, 1)
        draw_char(ctx, CHLOE, ch, t)
        bear(ctx, 560, 1230, 0.6, t)
        ctx.restore()
        overlay(ctx, (0.9, 0.75, 0.5), 0.15)
        rrect(ctx, 60, 280, 380, 70, 14); ctx.set_source_rgba(0, 0, 0, 0.6); ctx.fill()
        text(ctx, "ONE YEAR AGO", 250, 328, 32, col=(1, 1, 1))
        V.name_tag(ctx, t, Wd("c", 1, 7), t2 - 0.2, "CHLOE", "my best friend")
    elif t < t3 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * (t - t2), 540, 1050)
        V.bedroom(ctx, t, night=1.0)
        draw_char(ctx, MIA, dict(x=330, y=1500, s=1.35, mood="joy", look=0.6), t)
        draw_char(ctx, CHLOE, dict(x=760, y=1500, s=1.35, mood="joy", look=-0.6), t)
        ctx.restore()
        overlay(ctx, (0.9, 0.75, 0.5), 0.15)
    else:
        ctx.set_source_rgb(0.85, 0.87, 0.92); ctx.paint()
        text_bubble_phone(ctx, t, [("Chloe? Where are you??", True, t3 + 1.0), ("Are you okay?", True, t3 + 2.0), ("Please answer me", True, t3 + 3.2),
                                   ("Delivered", False, t3 + 4.3)], title="Chloe", s=2.2, y=1000)
    vignette(ctx, 0.35)


# ---------- D: group chat ----------
def d(ctx, t):
    t1, t2, t3, t4 = LS("d", 1), LS("d", 2), LS("d", 3), LS("d", 4)
    if t < t2 - 0.03:
        ctx.set_source_rgb(0.85, 0.87, 0.92); ctx.paint()
        sh = 6 * sin(t * 60) * (1 - ramp(t, 0.2, 2.6)) if t < 2.6 else 0
        ctx.save(); ctx.translate(sh, 0)
        text_bubble_phone(ctx, t, [("[photo] diary page 1", False, 0.4), ("[photo] diary page 2", False, 0.8),
                                   ("'his laugh sounds like music' LOL", False, t1 + 1.0), ("hahahaha", False, t1 + 2.0),
                                   ("Mia wrote POEMS??", False, t1 + 3.0), ("so cringe", False, t1 + 4.2)], title="Class 10B (31)", s=2.2, y=1000)
        ctx.restore()
    elif t < t3 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * (t - t2), 540, 1050)
        hall(ctx, t)
        for (x, ch_) in [(160, ETHAN), (920, HARPER)]:
            pass
        for k, x in enumerate((120, 330, 750, 960)):
            kid = dict(DEV, top=[(0.8, 0.5, 0.3), (0.4, 0.6, 0.8), (0.6, 0.4, 0.7), (0.3, 0.6, 0.4)][k], glasses=False, seed=40 + k,
                       hair=[(0.2, 0.15, 0.1), (0.85, 0.7, 0.4), (0.1, 0.1, 0.1), (0.5, 0.3, 0.2)][k], skin=[(0.95, 0.8, 0.7), (0.7, 0.5, 0.35), (0.98, 0.85, 0.75), (0.5, 0.35, 0.25)][k])
            draw_char(ctx, kid, dict(x=x, y=1580, s=1.0, legs=True, mood="joy", look=-0.5 if x > 540 else 0.5, tilt=0.06 * sin(t * 8 + k)), t)
        draw_char(ctx, MIA, dict(x=540, y=1600, s=1.3, legs=True, mood="crying", lookY=0.5), t)
        ctx.restore()
    elif t < t4 - 0.03:
        char_ecu(ctx, t, ETHAN, (t - t3) / (t4 - t3), dict(MOODS["worried"], bi=-4, bo=4), hall, mouth=talk("d", "E", t), look=0.4)
        V.name_tag(ctx, t, t3 + 0.1, t4 - 0.2, "ETHAN", "my crush")
    else:
        char_ecu(ctx, t, MIA, (t - t4) / (DUR("d") - t4), dict(MOODS["crying"], tremble=0.6), hall, look=-0.2)
    vignette(ctx, 0.35)


# ---------- E: confronting Harper ----------
def e(ctx, t):
    t1, t2, t3 = LS("e", 1), LS("e", 2), LS("e", 3)
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.04 * t, 540, 1050)
        hall(ctx, t)
        draw_char(ctx, HARPER, dict(x=330, y=1580, s=1.4, legs=True, mood=dict(MOODS["smirk"], eo=0.85), look=0.7), t)
        draw_char(ctx, MIA, dict(x=lerp(1250, 780, sm(t / 2.0)), y=1580, s=1.4, legs=True, mood=dict(DETERMINED_M2, tremble=0.4), look=-0.8), t)
        ctx.restore()
    elif t < t2 - 0.03:
        char_ecu(ctx, t, MIA, (t - t1) / (t2 - t1), dict(MOODS["angry"], bi=6, tear=0.5, flush=0.3), hall, mouth=talk("e", "M", t), look=-0.4)
    elif t < t3 - 0.03:
        char_ecu(ctx, t, HARPER, (t - t2) / (t3 - t2), MT([(t2, dict(MOODS["happy"], smile=0.3)), (Wd("e", 2, 3), dict(MOODS["cold"], eo=0.8))], t),
                 hall, mouth=talk("e", "H", t), look=0.4)
    else:
        char_ecu(ctx, t, HARPER, (t - t3) / (DUR("e") - t3), dict(MOODS["angry"], flush=0.2, eo=0.7), hall, mouth=talk("e", "H", t), look=0.2, tilt=-0.05)
    vignette(ctx, 0.4)


DETERMINED_M2 = dict(bi=7, bo=-3, eo=0.85, ew=0, smile=-0.1)


# ---------- F: Chloe on video ----------
def f(ctx, t):
    t1, t2, t3 = LS("f", 1), LS("f", 2), LS("f", 3)
    tEnd = LE("f", 3) + 0.35
    if t < t1 - 0.03:
        ctx.save(); zoomed(ctx, 1.0 + 0.15 * sm(t / t1), 540, 1050)
        hall(ctx, t)
        h = dict(x=330, y=1580, s=1.4, legs=True, mood=dict(MOODS["smirk"], eo=0.8), look=0.7); h["armR"] = ik(h, 560, 1200, -1)
        draw_char(ctx, HARPER, h, t)
        rrect(ctx, 520, 1100, 90, 160, 14); fs(ctx, (0.12, 0.12, 0.14), 4); glow(ctx, 565, 1180, 160, (0.6, 0.5, 1), 0.4)
        draw_char(ctx, MIA, dict(x=800, y=1580, s=1.4, legs=True, mood="worried", look=-0.8), t)
        ctx.restore()
    elif t < t3 - 0.03:
        hall(ctx, t)
        overlay(ctx, (0, 0, 0), 0.5)
        mood = dict(MOODS["smirk"], eo=0.8) if t < t2 else dict(MOODS["smirk"], eo=0.75, smile=0.5)
        video_call(ctx, t, CHLOE, mood, mouth=talk("f", "C", t), s=2.3, y=1000)
        V.flash(ctx, t, t1, (1, 1, 1), 0.2, 0.5)
    else:
        char_ecu(ctx, t, MIA, (t - t3) / 3, dict(MOODS["shock"], tremble=0.8), hall, look=0.0)
    vignette(ctx, 0.45)
    end_card(ctx, t, tEnd, "PART 3 · FINAL", [("FOLLOW so you don't miss it", 56, (1, 1, 1)), ("Why does Chloe hate Mia?", 50, (1, 0.86, 0.15))])


SCENES = {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f}
V.SCENES = SCENES

if __name__ == "__main__":
    os.makedirs(f"{EP}/preview", exist_ok=True)
    if sys.argv[1] == "preview":
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        for arg in sys.argv[2:]:
            sc, ts = arg.split(":"); V.frame(surf, sc, float(ts)); surf.write_to_png(f"{EP}/preview/{sc}_{ts}.png")
    else:
        for sc in (sys.argv[2:] or SCENES.keys()): V.render(sc)
