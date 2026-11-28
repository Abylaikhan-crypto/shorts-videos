"""Assemble the Veo clips into 1080x1920 video with captions, hook and end card. python assemble.py -> jan/scenes/video.mp4"""
import json, subprocess, numpy as np, cairo, math, os, sys
D = "/home/claude/short/jan"; W, H, FPS = 1080, 1920, 30
TL = json.load(open(f"{D}/timeline.json")); PLAN = json.load(open(f"{D}/plan.json"))
st = {}; p = 0
for s in TL: st[s["id"]] = p; p += s["frames"] / FPS
TOTAL = sum(s["frames"] for s in TL)
WORDS = []   # (t0, t1, word)
for s in TL:
    for ln in s["lines"]:
        ws = ln["words"]
        for i, w in enumerate(ws):
            end = ws[i + 1][1] if i + 1 < len(ws) else w[2] + 0.2
            WORDS.append((st[s["id"]] + w[1], st[s["id"]] + end, w[0]))
HOOK = [("THE KIDS CALLED", (1, 1, 1)), ("HIM THE GHOST", (1, 0.86, 0.15))]
HOOK_T = 2.2
m = next(s for s in TL if s["id"] == "m"); wl = m["lines"][1]["words"]
END_T = st["m"] + wl[0][1] - 0.1
clamp = lambda x: max(0.0, min(1.0, x))
def back_out(x, s=1.7): x -= 1; return x * x * ((s + 1) * x + s) + 1


def big_text(ctx, s_, y, size, col, stroke=22):
    ctx.save(); ctx.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    e = ctx.text_extents(s_); k = min(1.0, 980 / max(1, e.x_advance)); ctx.translate(540, y); ctx.scale(k, k)
    ctx.new_path(); ctx.move_to(-e.x_advance / 2, size * 0.35); ctx.text_path(s_)
    ctx.set_source_rgb(0, 0, 0); ctx.set_line_width(stroke); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
    ctx.set_source_rgb(*col); ctx.fill(); ctx.restore()


def overlay(ctx, t):
    if t < END_T:
        cur = next((w for w in WORDS if w[0] - 0.04 <= t < w[1]), None)
        if cur and t >= HOOK_T - 0.2:
            word = cur[2].upper().strip(",.?!"); pp = back_out(clamp((t - cur[0] + 0.04) / 0.1))
            ctx.save(); ctx.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(104)
            e = ctx.text_extents(word); k = min(1.0, 940 / max(1, e.x_advance)) * (0.75 + 0.25 * pp)
            ctx.translate(540, 1390); ctx.scale(k, k)
            ctx.new_path(); ctx.move_to(-e.x_advance / 2, 8); ctx.text_path(word); ctx.set_source_rgba(0, 0, 0, 0.5); ctx.fill()
            ctx.new_path(); ctx.move_to(-e.x_advance / 2, 0); ctx.text_path(word)
            ctx.set_source_rgb(0, 0, 0); ctx.set_line_width(18); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
            ctx.set_source_rgb(1, 1, 1); ctx.fill(); ctx.restore()
    if t < HOOK_T:
        a = 1 - clamp((t - HOOK_T + 0.25) / 0.25)
        ctx.save(); ctx.push_group(); ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0, 0, 0, 0.4); ctx.fill()
        for i, (s_, col) in enumerate(HOOK):
            pp = back_out(clamp((t - 0.08 * i) / 0.22))
            ctx.save(); ctx.translate(540, 760 + i * 150); ctx.scale(pp, pp); ctx.rotate(-0.03); ctx.translate(-540, -(760 + i * 150))
            big_text(ctx, s_, 760 + i * 150, 118, col, 26); ctx.restore()
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a); ctx.restore()
    if t >= END_T:
        u = clamp((t - END_T) / 0.4)
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0, 0, 0, 0.55 * u); ctx.fill()
        for i, (s_, size, col) in enumerate([("Would YOU have", 92, (1, 1, 1)), ("sat with him?", 92, (1, 0.86, 0.15)),
                                              ("Follow Paper & Plot", 52, (1, 1, 1)), ("This story is fiction.", 36, (0.8, 0.8, 0.8))]):
            pp = back_out(clamp((t - END_T - 0.12 * i) / 0.3))
            if pp <= 0: continue
            y = [800, 910, 1080, 1160][i]
            ctx.save(); ctx.translate(540, y); ctx.scale(pp, pp); ctx.translate(-540, -y); big_text(ctx, s_, y, size, col, 18); ctx.restore()


def frames_of(clip, n):
    pr = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", clip, "-vf", f"scale={W}:{H}:flags=lanczos,fps={FPS}", "-f", "rawvideo",
                           "-pix_fmt", "bgra", "-"], stdout=subprocess.PIPE)
    last = None
    for i in range(n):
        b = pr.stdout.read(W * H * 4)
        if len(b) == W * H * 4: last = b
        yield last
    pr.stdout.close(); pr.wait()


os.makedirs(f"{D}/scenes", exist_ok=True)
enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", f"{D}/scenes/video.tmp.mp4"], stdin=subprocess.PIPE)
fi = 0
for k, sh in enumerate(PLAN):
    f0 = round(sh["t0"] * FPS); f1 = round(PLAN[k + 1]["t0"] * FPS) if k + 1 < len(PLAN) else TOTAL
    for b in frames_of(f"{D}/clips/{sh['id']}.mp4", f1 - f0):
        arr = np.frombuffer(b, np.uint8).copy()
        surf = cairo.ImageSurface.create_for_data(memoryview(arr), cairo.FORMAT_ARGB32, W, H)
        overlay(cairo.Context(surf), fi / FPS); surf.flush()
        enc.stdin.write(arr.tobytes()); fi += 1
enc.stdin.close(); assert enc.wait() == 0
os.replace(f"{D}/scenes/video.tmp.mp4", f"{D}/scenes/video.mp4"); print("frames", fi, "of", TOTAL)
