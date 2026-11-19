"""Build Gortash's hand offer (GR_HandOffer_IN / _LOOP) from scratch, export .glb, render previews.

    blender -b --python tools/anim/make_handoffer.py

Body breathes with the game's standing idle; the right arm is posed by script (wrist placed on a
target, palm turned up and half towards the other person), with a slight sway while held.
Then: python tools/anim/fix_glb.py <LSLib glb> <exports>, and Divine convert-model to .GR2.
"""
import bpy, math
from mathutils import Vector, Quaternion, Matrix

G = r"C:\Users\obell\Desktop\GortashAnim"
TARGET = Vector((-0.24, 0.25, 1.15))     # wrist: elbow near the body, forearm forward (arm ~0.29 + 0.26 m)
FINGERS_TO = Vector((0.25, 1, -0.10))    # fingers point towards the other person, slightly inwards
PALM_UP = Vector((0.45, 0, -0.89))       # (sign as computed below) palm up, tilted towards the other person
IN_FRAMES = 30                           # reach: 1.25 s at 24 fps, then settles
SWAY_DEG = 1.6                           # held arm: small sway on the shoulder
ARM = ['Shoulder_R', 'Elbow_R', 'Wrist_R']
FING = ['IndexFinger1_R', 'IndexFinger2_R', 'MiddleFinger1_R', 'MiddleFinger2_R', 'RingFinger1_R',
        'RingFinger2_R', 'PinkyFinger1_R', 'PinkyFinger2_R']

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.fps = 24; vl = bpy.context.view_layer

def imp(f):
    before = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=G + "\\blender\\" + f)
    return set(bpy.data.objects) - before

body = imp("Proxy_HUM_M_FullBody.glb")
barm = [o for o in body if o.type == 'ARMATURE'][0]
for o in body:
    if o.name.startswith('Icosphere'): o.hide_render = True
idle = imp("HUM_M_Rig_CINE_Still_Breathing_Idle_StandL_01.glb")
m = [o for o in idle if o.type == 'ARMATURE'][0]
for o in idle:
    if o.type != 'ARMATURE': o.hide_render = True
m.name = 'GR_HandOffer_Squelette'; P = m.pose.bones
for pb in barm.pose.bones:
    if pb.name in P:
        c = pb.constraints.new('COPY_TRANSFORMS'); c.target = m; c.subtarget = pb.name
src = m.animation_data.action
F0, F1 = map(int, src.frame_range)

def curves(a):
    out = []
    for l in a.layers:
        for s in l.strips:
            for cb in s.channelbags: out += list(cb.fcurves)
    return out

def W(n): return P[n].head.copy()

def rot_about(pb, q):
    h = pb.head.copy()
    pb.matrix = Matrix.Translation(h) @ q.to_matrix().to_4x4() @ Matrix.Translation(-h) @ pb.matrix
    vl.update()

# idle rotations of the arm at frame 0 (start of the reach)
sc.frame_set(0)
rest = {b: P[b].matrix_basis.to_quaternion() for b in ARM + FING}

# pose the arm at frame 0 with the idle curves muted
for fc in curves(src):
    if any(f'"{b}"' in fc.data_path for b in ARM): fc.mute = True
sc.frame_set(0)
for _ in range(200):
    for j in ('Elbow_R', 'Shoulder_R'):
        a = (W('Wrist_R') - W(j)).normalized(); b = (TARGET - W(j)).normalized()
        q = a.rotation_difference(b); rot_about(P[j], Quaternion(q.axis, q.angle * 0.8))
# elbow down: swing the whole arm around the shoulder-wrist line (the wrist stays put) to the lowest elbow
axis = (W('Wrist_R') - W('Shoulder_R')).normalized(); best = (W('Elbow_R').z, 0)
for deg in range(-90, 91, 3):
    rot_about(P['Shoulder_R'], Quaternion(axis, math.radians(deg))); best = min(best, (W('Elbow_R').z, deg))
    rot_about(P['Shoulder_R'], Quaternion(axis, -math.radians(deg)))
rot_about(P['Shoulder_R'], Quaternion(axis, math.radians(best[1]))); print("ELBOW_SWING", best[1])
fwd = FINGERS_TO.normalized()
for _ in range(12):
    d = (W('MiddleFinger1_R') - W('Wrist_R')).normalized()
    rot_about(P['Wrist_R'], d.rotation_difference(fwd))
    n = (W('IndexFinger1_R') - W('PinkyFinger0_R')).cross(W('MiddleFinger1_R') - W('Wrist_R')).normalized()
    d = (W('MiddleFinger1_R') - W('Wrist_R')).normalized(); want = PALM_UP.normalized()
    npj = (n - d * n.dot(d)).normalized(); wpj = (want - d * want.dot(d)).normalized()
    rot_about(P['Wrist_R'], Quaternion(d, math.atan2(npj.cross(wpj).dot(d), npj.dot(wpj))))
print("WRIST", [round(x, 2) for x in W('Wrist_R')], "ELBOW", [round(x, 2) for x in W('Elbow_R')])
offer = {b: P[b].matrix_basis.to_quaternion() for b in ARM}
for fc in curves(src): fc.mute = False

def key_arm(action, frames):
    m.animation_data.action = action
    for fc in list(curves(action)):
        if any(f'"{b}"' in fc.data_path for b in ARM + FING) and 'rotation' in fc.data_path:
            fc.keyframe_points.clear()
    for f, pose in frames:
        for b, q in pose.items():
            P[b].rotation_mode = 'QUATERNION'; P[b].rotation_quaternion = q
            P[b].keyframe_insert('rotation_quaternion', frame=f)

def sway(f, amp=SWAY_DEG):
    # 3 slow cycles over the loop, so it loops cleanly
    s = math.sin(2 * math.pi * 3 * (f - F0) / (F1 - F0))
    return Quaternion(Vector((1, 0, 0)), math.radians(amp) * s)

def fingers(t):
    # fingers relax a touch while held (idle pose blended with a slightly more open hand)
    return {b: rest[b].slerp(Quaternion(), 0.25 * t) for b in FING}

# LOOP: whole idle, arm held with a slight sway, fingers relaxed
loop = src.copy(); loop.name = 'GR_HandOffer_LOOP'
frames = []
for f in range(F0, F1 + 1, 3):
    q = sway(f)
    pose = {'Shoulder_R': offer['Shoulder_R'] @ q, 'Elbow_R': offer['Elbow_R'] @ sway(f + 7, SWAY_DEG * 0.6),
            'Wrist_R': offer['Wrist_R']}
    pose.update(fingers(1))
    frames.append((f, pose))
key_arm(loop, frames)

# IN: idle start, arm eases into the offer (first value of the loop), fingers open as it arrives
inn = src.copy(); inn.name = 'GR_HandOffer_IN'
start = {'Shoulder_R': offer['Shoulder_R'] @ sway(F0), 'Elbow_R': offer['Elbow_R'] @ sway(F0 + 7, SWAY_DEG * 0.6),
         'Wrist_R': offer['Wrist_R']}
frames = []
for f in range(0, IN_FRAMES + 7, 2):
    t = min(f / IN_FRAMES, 1.0); e = 1 - (1 - t) ** 3          # ease-out: quick start, soft arrival
    # the elbow leads, the wrist follows a little later
    lag = {'Shoulder_R': e, 'Elbow_R': min(1, e * 1.08), 'Wrist_R': max(0, min(1, (t - 0.15) / 0.85)) ** 0.7}
    pose = {b: rest[b].slerp(start[b], lag[b]) for b in ARM}
    pose.update({b: rest[b].slerp(Quaternion(), 0.25 * e) for b in FING})
    frames.append((f, pose))
key_arm(inn, frames)
end_in = IN_FRAMES + 6
for fc in curves(inn):
    for k in [k for k in fc.keyframe_points if k.co[0] > end_in][::-1]: fc.keyframe_points.remove(k)
inn.use_frame_range = True; inn.frame_start = 0; inn.frame_end = end_in
print("IN_FRAMES", end_in, "LOOP", F0, F1)

bpy.ops.wm.save_as_mainfile(filepath=G + r"\GR_HandOffer.blend")

# previews: reach (4 frames) and held (2 frames), 3/4 front view
sc.render.engine = 'BLENDER_WORKBENCH'; sc.render.resolution_x = 360; sc.render.resolution_y = 420
bpy.ops.object.camera_add(location=(-1.3, 2.3, 1.45), rotation=(math.radians(82), 0, math.radians(210)))
sc.camera = bpy.context.object
for cam_name, loc, rot in (('face', (-1.3, 2.3, 1.45), (82, 0, 210)), ('cote', (2.6, 0.5, 1.35), (85, 0, 90))):
  sc.camera.location = loc; sc.camera.rotation_euler = [math.radians(x) for x in rot]
  for name, act, fr in (('in', inn, (0, 10, 20, end_in)), ('loop', loop, (40, 120))):
    m.animation_data.action = act
    for f in fr:
        sc.frame_set(f); sc.render.filepath = rf"{G}\v2_{cam_name}_{name}_{f:03d}.png"; bpy.ops.render.render(write_still=True)

# export each action alone, armature only
for o in bpy.data.objects: o.select_set(False)
m.select_set(True); vl.objects.active = m
for act, (s, e) in ((inn, (0, end_in)), (loop, (F0, F1))):
    m.animation_data.action = act; sc.frame_start, sc.frame_end = s, e
    bpy.ops.export_scene.gltf(filepath=G + rf"\export\{act.name}.glb", use_selection=True, export_animations=True,
                              export_animation_mode='ACTIVE_ACTIONS', export_skins=True, export_def_bones=False,
                              export_frame_range=True, export_force_sampling=True)
print("DONE", end_in / 24)
