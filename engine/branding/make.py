import sys; sys.path.insert(0, '/home/claude/short')
import cairo
from math import pi
from rig import *
import part1 as P1

def bg(ctx, w, h):
    g = cairo.LinearGradient(0, 0, w, h); g.add_color_stop_rgb(0, 0.10, 0.07, 0.20); g.add_color_stop_rgb(1, 0.30, 0.06, 0.12)
    ctx.set_source(g); ctx.paint()

# avatar 800x800
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 800); ctx = cairo.Context(s); bg(ctx, 800, 800)
glow(ctx, 400, 400, 380, (1, 0.5, 0.3), 0.35)
ctx.save(); ctx.translate(400, 400); ctx.rotate(-0.08)
poly(ctx, [(-210, -270), (120, -270), (210, -180), (210, 270), (-210, 270)])
ctx.set_source_rgb(0.99, 0.97, 0.92); ctx.fill_preserve(); ctx.set_source_rgb(*OUTL); ctx.set_line_width(14); ctx.stroke()
poly(ctx, [(120, -270), (120, -180), (210, -180)]); ctx.set_source_rgb(0.85, 0.82, 0.76); ctx.fill_preserve(); ctx.set_source_rgb(*OUTL); ctx.stroke()
for y in (-150, -95, 175, 225):
    ctx.move_to(-150, y); ctx.line_to(150 if y > 0 else 60, y); ctx.set_source_rgba(0.6, 0.6, 0.65, 0.8); ctx.set_line_width(10); ctx.stroke()
text(ctx, "&", 0, 120, 330, col=(0.9, 0.12, 0.15))
ctx.restore()
s.write_to_png('/home/claude/short/branding/avatar.png')

# banner 2560x1440 (safe area 1546x423 centred)
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 2560, 1440); ctx = cairo.Context(s); bg(ctx, 2560, 1440)
for i in range(60):
    import random; r = random.Random(i)
    ell(ctx, r.uniform(0, 2560), r.uniform(0, 1440), 3, 3); ctx.set_source_rgba(1, 1, 1, r.uniform(0.2, 0.6)); ctx.fill()
glow(ctx, 1280, 720, 900, (1, 0.45, 0.3), 0.25)
draw_char(ctx, P1.DALE, dict(x=330, y=1180, s=1.4, mood="smirk", hat=True, saccade=False, shadow=0.35), 0.3)
draw_char(ctx, P1.MAYA, dict(x=2230, y=1180, s=1.3, mood="scared", look=-1, saccade=False, armL=("ik", 15, -92, 1), armR=("ik", -8, -102, -1)), 0.3)
text(ctx, "PAPER & PLOT", 1280, 700, 160, col=(1, 1, 1), stroke=18)
text(ctx, "Animated drama stories  •  New part every other day", 1280, 800, 52, col=(1, 0.86, 0.15), stroke=10)
s.write_to_png('/home/claude/short/branding/banner.png')
