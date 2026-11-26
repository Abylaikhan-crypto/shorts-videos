"""Procedural airliner sets for 'We Will Not Land'. python plane.py <plate> [<plate>...]  -> b3d/plates/<plate>.png"""
import bpy, math, sys, time, os
from mathutils import Vector

OUT = "/home/claude/short/b3d/plates"
os.makedirs(OUT, exist_ok=True)
MATS = {}


def reset(mood):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = int(os.environ.get('SAMPLES', 40)); sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 6
    sc.render.resolution_x, sc.render.resolution_y = 1080, 1920; sc.render.resolution_percentage = int(os.environ.get('PCT', 100))
    sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
    sc.view_settings.exposure = {"red": -1.3, "night": -0.6, "dawn": -3.0, "dark": -0.2}.get(mood, 0)
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = {"dawn": (1.0, 0.55, 0.3, 1)}.get(mood, (0.02, 0.025, 0.05, 1))
    bg.inputs['Strength'].default_value = {"dawn": 0.8}.get(mood, 0.05)
    MATS.clear()
    return sc


def mat(name, col, rough=0.6, emit=0.0, metal=0.0):
    key = (name, col, emit)
    if key in MATS: return MATS[key]
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    if emit:
        b.inputs['Emission Color'].default_value = (*col, 1); b.inputs['Emission Strength'].default_value = emit
    MATS[key] = m
    return m


def box(loc, size, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot); o = bpy.context.object
    o.scale = [s / 2 for s in size]; o.data.materials.append(m); return o


def cyl(loc, r, depth, m, rot=(0, 0, 0), verts=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot); o = bpy.context.object
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o


def light(loc, energy, col, size=0.3, kind='POINT'):
    bpy.ops.object.light_add(type=kind, location=loc); L = bpy.context.object
    L.data.energy = energy; L.data.color = col
    if kind in ('POINT', 'SPOT'): L.data.shadow_soft_size = size
    return L


def camera(loc, look, lens=24):
    bpy.ops.object.camera_add(location=loc); c = bpy.context.object
    d = Vector(look) - Vector(loc); c.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); c.data.lens = lens
    bpy.context.scene.camera = c; return c


def cabin(mood="red", rows=14, front_door=True):
    """fuselage along +Y; floor z=0; aisle at x=0"""
    wall = mat("wall", (0.78, 0.78, 0.76), 0.5)
    seat = mat("seat", (0.10, 0.18, 0.40), 0.8)
    head = mat("head", (0.85, 0.86, 0.88), 0.7)
    carpet = mat("carpet", (0.18, 0.16, 0.22), 0.9)
    winm = mat("win", (0.05, 0.07, 0.15), 0.2, emit=0.6)
    scr = mat("scr", (0.2, 0.5, 1.0), 0.3, emit=3.0)
    bin_ = mat("bin", (0.86, 0.86, 0.84), 0.4)
    # shell (inside of a big cylinder) + floor
    shell = cyl((0, rows * 0.45, 1.05), 2.05, rows * 0.9 + 8, wall, rot=(math.radians(90), 0, 0), verts=48)
    box((0, rows * 0.45, -0.02), (3.9, rows * 0.9 + 8, 0.04), carpet)
    box((0, rows * 0.45, 0.005), (0.55, rows * 0.9 + 8, 0.01), mat("aisle", (0.35, 0.10, 0.12), 0.9))
    for i in range(rows):
        y = 1.0 + i * 0.9
        for side in (-1, 1):
            for k in range(3):
                x = side * (0.55 + 0.25 + k * 0.5)
                box((x, y, 0.42), (0.46, 0.48, 0.12), seat)
                box((x, y - 0.24, 0.85), (0.46, 0.1, 0.85), seat, rot=(math.radians(8), 0, 0))
                box((x, y - 0.2, 1.2), (0.36, 0.11, 0.18), head)
                box((x, y - 0.31, 0.95), (0.18, 0.012, 0.13), scr)       # seatback screen faces the row behind (+y view from rear)
            # window on the wall
            box((side * 1.92, y, 1.25), (0.05, 0.26, 0.36), winm, rot=(0, math.radians(side * -18), 0))
        # overhead bins
    for side in (-1, 1):
        box((side * 1.3, rows * 0.45, 2.05), (1.0, rows * 0.9 + 2, 0.5), bin_, rot=(0, math.radians(side * 15), 0))
    ceil_col = {"red": (0.9, 0.12, 0.07), "night": (0.55, 0.65, 1.0), "dawn": (1, 0.85, 0.7), "dark": (0.3, 0.35, 0.6)}[mood]
    strip = mat("strip", ceil_col, 0.3, emit=3.0)
    for side in (-1, 1):
        box((side * 0.72, rows * 0.45, 2.42), (0.06, rows * 0.9 + 2, 0.04), strip)
        box((side * 0.33, rows * 0.45, 0.02), (0.03, rows * 0.9 + 2, 0.02), mat("floorled", (1, 0.5, 0.15), 0.3, emit=5))
    for i in range(0, rows, 3):
        light((0, 1.0 + i * 0.9, 2.3), 60 if mood != "dark" else 25, ceil_col, 0.6)
    if front_door:   # bulkhead + cockpit door at the far end (+y)
        yb = rows * 0.9 + 1.4
        bh = mat("bulk", (0.80, 0.80, 0.78), 0.5)
        box((-1.25, yb, 1.2), (1.6, 0.1, 2.6), bh); box((1.25, yb, 1.2), (1.6, 0.1, 2.6), bh); box((0, yb, 2.35), (0.9, 0.1, 0.5), bh)
        box((0, yb + 0.02, 1.05), (0.9, 0.08, 2.1), mat("door", (0.62, 0.63, 0.66), 0.35, metal=0.3))
        box((0.32, yb - 0.04, 1.2), (0.12, 0.02, 0.18), mat("keypad", (1.0, 0.1, 0.1), 0.3, emit=4))
        box((0, yb - 0.05, 1.75), (0.22, 0.02, 0.22), mat("peep", (0.02, 0.02, 0.03), 0.1))
        box((0, yb - 0.06, 2.25), (0.5, 0.02, 0.14), mat("exit", (0.2, 1.0, 0.3), 0.3, emit=5))
    return rows


def cockpit(mood="night"):
    dark = mat("ck", (0.10, 0.11, 0.13), 0.6)
    box((0, 0, -0.05), (3, 4, 0.1), dark)
    cyl((0, 0, 1.0), 1.8, 4, dark, rot=(math.radians(90), 0, 0))
    box((0, 1.5, 0.75), (2.6, 0.8, 0.5), mat("panel", (0.16, 0.17, 0.20), 0.5))
    for i, x in enumerate((-0.9, -0.45, 0.45, 0.9)):
        box((x, 1.12, 0.95), (0.36, 0.02, 0.3), mat(f"disp{i}", (0.2, 0.7, 1.0) if i % 2 else (0.3, 1.0, 0.5), 0.3, emit=3))
    box((0, 1.12, 0.95), (0.2, 0.02, 0.2), mat("gear", (1.0, 0.1, 0.08) if mood != "green" else (0.1, 1.0, 0.2), 0.3, emit=8))
    winm = mat("ws", (0.02, 0.03, 0.08), 0.05, emit=0.3)
    for x in (-0.6, 0.6): box((x, 1.95, 1.5), (1.0, 0.05, 0.6), winm, rot=(math.radians(-25), 0, math.radians(-12 if x > 0 else 12)))
    for x in (-0.6, 0.6):
        box((x, 0.6, 0.45), (0.55, 0.55, 0.15), mat("cs", (0.25, 0.2, 0.18), 0.8))
        box((x, 0.32, 0.85), (0.55, 0.12, 0.8), mat("cs", (0.25, 0.2, 0.18), 0.8))
    light((0, 0.2, 2.0), 60, (0.45, 0.6, 1.0), 0.8)
    light((0, -0.6, 1.4), 25, (0.9, 0.8, 0.7), 0.8)
    for k in range(40):
        import random; r = random.Random(k)
        box((r.uniform(-1.6, 1.6), 2.6, r.uniform(1.4, 2.4)), (0.02, 0.01, 0.02), mat("star", (1, 1, 1), 0.3, emit=20))
    light((0, 1.2, 0.9), 8, (1.0, 0.15, 0.1) if mood != "green" else (0.2, 1, 0.3), 0.2)


def bay():
    metal = mat("m", (0.25, 0.26, 0.28), 0.45, metal=0.7)
    box((0, 0, -0.05), (3, 5, 0.1), metal); box((0, 0, 1.8), (3, 5, 0.1), metal)
    box((-1.5, 0, 0.9), (0.1, 5, 1.9), metal); box((1.5, 0, 0.9), (0.1, 5, 1.9), metal); box((0, 2.5, 0.9), (3, 0.1, 1.9), metal)
    for i in range(6):
        box((-1.2, -1.8 + i * 0.7, 0.9), (0.4, 0.5, 1.6), mat("rack", (0.15, 0.16, 0.18), 0.5, metal=0.4))
        box((-0.99, -1.8 + i * 0.7, 1.2), (0.02, 0.1, 0.05), mat("led", (0.1, 1, 0.3), 0.3, emit=6))
    for i in range(8):
        cyl((0.6 + 0.08 * i, 0, 1.6 - 0.04 * i), 0.025, 5, mat("cable", (0.6, 0.4, 0.1) if i % 2 else (0.15, 0.15, 0.6), 0.5), rot=(math.radians(90), 0, 0), verts=8)
    box((0.7, 1.6, 0.6), (0.5, 0.5, 0.9), mat("gearbox", (0.45, 0.45, 0.48), 0.35, metal=0.8))
    box((0.7, 1.32, 0.75), (0.08, 0.06, 0.5), mat("lever", (0.9, 0.6, 0.1), 0.4))
    box((0.0, -2.2, 1.0), (0.4, 0.05, 2.0), mat("ladder", (0.5, 0.5, 0.52), 0.4, metal=0.8))
    light((0, -2.0, 1.75), 90, (1.0, 0.15, 0.08), 0.3)
    light((0.3, 0.5, 1.6), 40, (0.4, 0.6, 1.0), 0.6)
    light((0.7, 1.0, 1.2), 25, (1.0, 0.7, 0.3), 0.3)


def runway():
    box((0, 60, -0.05), (30, 140, 0.1), mat("tarmac", (0.08, 0.08, 0.09), 0.8))
    for i in range(40):
        y = i * 3
        for x in (-12, 12):
            box((x, y, 0.1), (0.3, 0.3, 0.2), mat("rl", (1.0, 0.85, 0.5), 0.3, emit=12))
        box((0, y, 0.01), (0.5, 1.6, 0.02), mat("cl", (0.9, 0.9, 0.9), 0.5))
    w = bpy.context.scene.world; nt = w.node_tree; sky = nt.nodes.new("ShaderNodeTexSky")
    try:
        sky.sky_type = 'NISHITA'; sky.sun_elevation = math.radians(3); sky.sun_rotation = math.radians(170)
    except Exception: pass
    nt.links.new(sky.outputs[0], nt.nodes['Background'].inputs['Color']); nt.nodes["Background"].inputs["Strength"].default_value = 0.25
    bpy.ops.mesh.primitive_uv_sphere_add(radius=8, location=(10, 220, 4)); s = bpy.context.object; s.data.materials.append(mat("sun", (1.0, 0.6, 0.25), 0.3, emit=12))


PLATES = {
    # name: (mood, builder, camera loc, look, lens)
    "aisle_red":   ("red",   lambda: cabin("red"),   (0, -0.6, 1.65), (0, 20, 1.3), 22),
    "aisle_night": ("night", lambda: cabin("night"), (0, -0.6, 1.65), (0, 20, 1.3), 22),
    "row_red":     ("red",   lambda: cabin("red"),   (0.2, 7.7, 1.3), (-1.3, 6.2, 0.9), 20),
    "front_red":   ("red",   lambda: cabin("red"),   (0.3, 9.5, 1.55), (0, 20, 1.3), 24),
    "door_red":    ("red",   lambda: cabin("red"),   (0.2, 11.6, 1.45), (0, 14, 1.35), 22),
    "cockpit":     ("night", lambda: cockpit("red"), (0, -0.9, 1.35), (0, 1.8, 1.05), 20),
    "cockpit_grn": ("night", lambda: cockpit("green"), (0, -0.9, 1.35), (0, 1.8, 1.05), 20),
    "bay":         ("dark",  bay,                    (-0.2, -2.0, 1.2), (0.6, 2.0, 0.7), 18),
    "runway_dawn": ("dawn",  runway,                 (0, -6, 3.5), (0, 60, 2.0), 30),
}

if __name__ == "__main__":
    for name in sys.argv[1:]:
        mood, build, loc, look, lens = PLATES[name]
        sc = reset(mood); build(); camera(loc, look, lens)
        sc.render.filepath = f"{OUT}/{name}.png"
        t = time.time(); bpy.ops.render.render(write_still=True); print("plate", name, round(time.time() - t, 1), flush=True)
