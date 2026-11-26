import bpy, time, math
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 48; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920; sc.render.resolution_percentage = 50
sc.render.filepath = '/home/claude/short/b3d/test.png'
def box(name, loc, size, col, emit=0):
    bpy.ops.mesh.primitive_cube_add(location=loc); o = bpy.context.object; o.scale = [s / 2 for s in size]; o.name = name
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = 0.6
    if emit: b.inputs['Emission Color'].default_value = (*col, 1); b.inputs['Emission Strength'].default_value = emit
    o.data.materials.append(m); return o
# bunker corridor
box('floor', (0, 10, -0.05), (4, 24, 0.1), (0.15, 0.14, 0.13))
box('ceil', (0, 10, 3.05), (4, 24, 0.1), (0.1, 0.1, 0.1))
box('wl', (-2.05, 10, 1.5), (0.1, 24, 3), (0.35, 0.33, 0.30))
box('wr', (2.05, 10, 1.5), (0.1, 24, 3), (0.35, 0.33, 0.30))
box('door', (0, 21.9, 1.2), (2.2, 0.2, 2.4), (0.25, 0.22, 0.2))
box('sign', (0, 21.7, 2.7), (2.4, 0.1, 0.4), (1, 0.75, 0.2), emit=4)
for i in range(5):
    box(f'lamp{i}', (0, 3 + i * 4, 2.95), (0.6, 0.6, 0.08), (1, 0.15, 0.1), emit=12)
    bpy.ops.object.light_add(type='POINT', location=(0, 3 + i * 4, 2.6)); L = bpy.context.object; L.data.energy = 300; L.data.color = (1, 0.2, 0.12)
for i in range(6):
    box(f'pipe{i}', (-1.9, 1 + i * 4, 2.6), (0.15, 3.6, 0.15), (0.4, 0.4, 0.42))
bpy.ops.object.camera_add(location=(0.3, -1.5, 1.4), rotation=(math.radians(88), 0, 0)); cam = bpy.context.object; sc.camera = cam; cam.data.lens = 22
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.02
sc.view_settings.view_transform = 'AgX'
t = time.time(); bpy.ops.render.render(write_still=True); print('render s', round(time.time() - t, 1))
