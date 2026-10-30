"""Photoreal renders of the house with Blender Cycles.

Run from the folder that holds house.glb:
  blender -b -P render_house.py -- [--shots front,back,...] [--res 3840] [--samples 1024] [--cpu] [--hour 16.5] [--save]

Writes renders/<shot>.png next to this script, and house.blend with --save.
Units: the model comes out of the web viewer in feet; it is scaled to real meters here.
"""
import bpy, sys, os, math
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def arg(name, default=None, flag=False):
    if flag: return name in argv
    return argv[argv.index(name) + 1] if name in argv else default

FT = 0.3048
# shots in the web viewer's coordinates (x, up, z in feet) and its vertical field of view
SHOTS = {
    'front':     ((-2, 9.5, 146), (55, 11, 46), 42),
    'corner':    ((175, 26, 160), (62, 10, 30), 42),
    'back':      ((44, 44, -118), (46, 0, 2), 42),
    'firepit':   ((10, 5, -50), (45, 6, 20), 42),
    'falls':     ((37.5, 4, -28), (37.5, 0, -42), 60),
    'porch':     ((36, 9, 14), (46, -4, -14), 60),
    'aerial':    ((-80, 115, 150), (52, 0, 8), 42),
}
def bl(p):  # web viewer (x, y up, z) in feet -> Blender (x, y, z up) in meters (glTF import maps z -> -y)
    x, y, z = p; return Vector((x * FT, -z * FT, y * FT))

shots = arg('--shots', 'front,back,falls').split(',')
res = int(arg('--res', '1920')); samples = int(arg('--samples', '512')); hour = float(arg('--hour', '16.5'))

# ---------------------------------------------------------------- scene
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.join(HERE, 'house.glb'))
objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
for o in bpy.context.scene.objects:
    if o.parent is None: o.scale = (FT, FT, FT)
bpy.context.view_layer.update()
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

def nodes(mat):
    mat.use_nodes = True; return mat.node_tree.nodes, mat.node_tree.links
def bsdf(mat): return next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)

# ---------------------------------------------------------------- materials: upgrade the web viewer's stand-ins by name
water_mat = bpy.data.materials.new('Pond water'); N, L = nodes(water_mat); N.clear()
out = N.new('ShaderNodeOutputMaterial'); pb = N.new('ShaderNodeBsdfPrincipled')
pb.inputs['Base Color'].default_value = (1, 1, 1, 1); pb.inputs['Roughness'].default_value = .015; pb.inputs['IOR'].default_value = 1.333
pb.inputs['Transmission Weight'].default_value = 1.0
vol = N.new('ShaderNodeVolumeAbsorption'); vol.inputs['Color'].default_value = (.32, .62, .55, 1); vol.inputs['Density'].default_value = .9
# gentle wind ripples as bump
tc = N.new('ShaderNodeTexCoord'); nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 3.0; nz.inputs['Detail'].default_value = 6
bump = N.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = .06; bump.inputs['Distance'].default_value = .02
L.new(tc.outputs['Object'], nz.inputs['Vector']); L.new(nz.outputs['Fac'], bump.inputs['Height']); L.new(bump.outputs['Normal'], pb.inputs['Normal'])
L.new(pb.outputs['BSDF'], out.inputs['Surface']); L.new(vol.outputs['Volume'], out.inputs['Volume'])

for o in objs:
    for slot in o.material_slots:
        m = slot.material
        if not m: continue
        n = m.name.lower(); b = bsdf(m) if m.use_nodes else None
        if n.startswith('pond_water'):
            # close the surface into a solid so light is absorbed with depth, like real water
            sol = o.modifiers.new('depth', 'SOLIDIFY'); sol.thickness = 9 * FT; sol.offset = -1; slot.material = water_mat
        elif n.startswith('pool'):
            slot.material = water_mat; sol = o.modifiers.new('depth', 'SOLIDIFY'); sol.thickness = .3; sol.offset = -1
        elif n.startswith('glass') and b:
            b.inputs['Transmission Weight'].default_value = 1; b.inputs['Roughness'].default_value = 0; b.inputs['Base Color'].default_value = (.9, .95, .95, 1); b.inputs['Alpha'].default_value = 1
        elif ('boulder' in n or n.startswith('rock')) and b:
            # the scanned stones are red desert granite: pull them toward grey-tan fieldstone
            link = b.inputs['Base Color'].links
            if link:
                T = m.node_tree; src = link[0].from_socket
                bw = T.nodes.new('ShaderNodeRGBToBW'); mx = T.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs['Factor'].default_value = .6
                T.links.new(src, bw.inputs['Color']); T.links.new(src, mx.inputs['A']); T.links.new(bw.outputs['Val'], mx.inputs['B'])
                T.links.new(mx.outputs['Result'], b.inputs['Base Color'])
        if b and m.blend_method == 'BLEND' and not n.startswith(('glass', 'pond')):
            m.blend_method = 'HASHED'

# ---------------------------------------------------------------- sky and sun, same path as the viewer's sun slider
t = (hour - 6) / 13.5
elev = max(-4, math.sin(math.pi * t) * 62) * math.pi / 180
az = (-80 + 200 * t) * math.pi / 180
d = Vector((math.sin(az) * math.cos(elev), math.sin(elev), math.cos(az) * math.cos(elev)))   # viewer coords
db = Vector((d.x, -d.z, d.y)).normalized()                                                        # Blender coords
world = bpy.data.worlds.new('Sky'); bpy.context.scene.world = world; N, L = nodes(world); N.clear()
sky = N.new('ShaderNodeTexSky'); sky.sky_type = 'NISHITA'; sky.sun_disc = True
sky.sun_elevation = math.asin(db.z); sky.sun_rotation = math.atan2(db.x, -db.y)  # Cycles: dir = (cos e sin r, -cos e cos r, sin e)
sky.air_density = 1.0; sky.dust_density = 1.5; sky.ozone_density = 1.0; sky.altitude = 10
bg = N.new('ShaderNodeBackground'); bg.inputs['Strength'].default_value = .25
wo = N.new('ShaderNodeOutputWorld'); L.new(sky.outputs['Color'], bg.inputs['Color']); L.new(bg.outputs['Background'], wo.inputs['Surface'])
sun = bpy.data.objects.new('Sun', bpy.data.lights.new('Sun', 'SUN')); bpy.context.scene.collection.objects.link(sun)
sun.data.energy = 4.0; sun.data.angle = math.radians(.55); sun.data.color = (1, .96, .9)
sun.rotation_euler = db.to_track_quat('Z', 'Y').to_euler()   # a sun lamp shines down its -Z

# ---------------------------------------------------------------- render settings
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; cy = sc.cycles
cy.samples = samples; cy.use_denoising = True; cy.max_bounces = 12; cy.transmission_bounces = 12; cy.volume_bounces = 2
cy.use_adaptive_sampling = True; cy.adaptive_threshold = .01
if not arg('--cpu', flag=True):
    prefs = bpy.context.preferences.addons['cycles'].preferences
    for kind in ('OPTIX', 'CUDA', 'HIP', 'METAL', 'ONEAPI'):
        try:
            prefs.compute_device_type = kind; prefs.get_devices()
            gpus = [dv for dv in prefs.devices if dv.type == kind]
            if gpus:
                for dv in prefs.devices: dv.use = dv.type == kind
                cy.device = 'GPU'; cy.denoiser = 'OPTIX' if kind == 'OPTIX' else 'OPENIMAGEDENOISE'; print('render device:', kind, [g.name for g in gpus]); break
        except Exception as e: pass
    else: print('no GPU found, rendering on the CPU')
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'; sc.view_settings.exposure = float(arg('--exposure', '-1.2'))
sc.render.resolution_x = res; sc.render.resolution_y = round(res * 9 / 16); sc.render.film_transparent = False
sc.render.image_settings.file_format = 'PNG'

cam = bpy.data.objects.new('Camera', bpy.data.cameras.new('Camera')); sc.collection.objects.link(cam); sc.camera = cam
cam.data.sensor_fit = 'VERTICAL'; cam.data.clip_start = .1; cam.data.clip_end = 3000

if arg('--save', flag=True): bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, 'house.blend'))
os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True)
for s in shots:
    p, tgt, fov = SHOTS[s]; cam.location = bl(p); cam.rotation_euler = (bl(tgt) - bl(p)).to_track_quat('-Z', 'Y').to_euler()
    cam.data.angle_y = math.radians(fov)
    sc.render.filepath = os.path.join(HERE, 'renders', s + '.png'); bpy.ops.render.render(write_still=True); print('wrote', sc.render.filepath)
