"""Cut Wyll's act 3 waltz into the animations of the ball (run headless on a copy of GR_HandAccept.blend).

    blender -b GR_HandAccept_copy.blend --python waltz_export.py -- <folder with the two waltz .glb>

The game does not play an animation started from an offset (AnimationPlayStartOffset, game 20/11), so
each part of the waltz is an animation of its own, starting at its first frame:
  In    0 s -> 11.83 s   walk up, hand, start of the slow dance; ends on the loop's first pose
  Loop  7.75 -> 11.83 s  the slow dance; 7.75 s and 11.83 s are the closest poses of the dance
                         (1.7 cm on average over both bodies), and the last 6 frames are blended
                         into the first, so it loops without a jump (played with Continuous)
  Kiss  11.83 -> 21 s    from the loop's pose into the kiss
  Part  21 s -> end      they let go and part
A first cut (20/11: Dance 3.5-13 s restarted every 9.5 s, fades between pieces) looked jerky and cut back
to the middle of the dance.
"""
import bpy, os, sys
SRC = sys.argv[sys.argv.index('--') + 1]
OUT = r'C:\Users\obell\Desktop\GortashAnim\export'
FPS = 24
PARTS = {'In': (0, 284, False), 'Loop': (186, 284, True), 'Kiss': (284, 504, False), 'Part': (504, 688, False)}
BLEND = 6
HALVES = {'Gortash': ('GR_HandOffer_Squelette', 'HUM_M_Rig_SCENE_Wyll_InPartyEND_WyllWaltzKissTall_Wyll.glb'),
          'Joueuse': ('Joueuse_Squelette', 'HUM_F_Rig_SCENE_Wyll_InPartyEND_WyllWaltzKissTall_PLYR.glb')}
sc = bpy.context.scene
sc.render.fps = FPS


def curves(act):
    return [f for l in act.layers for s in l.strips for cb in s.channelbags for f in cb.fcurves]


def cut(full, obj, a, b, loop):
    """A new action with frames a..b of `full`, shifted to start at 0."""
    new = bpy.data.actions.new(full.name.replace('_full', '') + '_part')
    obj.animation_data.action = new
    if new.slots: obj.animation_data.action_slot = new.slots[0]
    n = b - a
    for fc in curves(full):
        vals = [fc.evaluate(a + k) for k in range(n + 1)]
        if loop:
            for k in range(n - BLEND, n + 1):
                w = (k - (n - BLEND)) / BLEND
                vals[k] = vals[k] * (1 - w) + vals[0] * w
        nf = new.fcurve_ensure_for_datablock(obj, fc.data_path, index=fc.array_index) \
            if hasattr(new, 'fcurve_ensure_for_datablock') else None
        if nf is None:
            obj.keyframe_insert(fc.data_path, index=fc.array_index, frame=0)
            nf = [f for f in curves(new) if f.data_path == fc.data_path and f.array_index == fc.array_index][0]
        nf.keyframe_points.clear()
        nf.keyframe_points.add(n + 1)
        for k, v in enumerate(vals):
            nf.keyframe_points[k].co = (k, v); nf.keyframe_points[k].interpolation = 'LINEAR'
        nf.update()
    return new


for half, (obj_name, glb) in HALVES.items():
    before_o, before_a = set(bpy.data.objects), set(bpy.data.actions)
    bpy.ops.import_scene.gltf(filepath=os.path.join(SRC, glb))
    full = [a for a in bpy.data.actions if a not in before_a][0]
    for o in [o for o in bpy.data.objects if o not in before_o]:
        bpy.data.objects.remove(o)
    full.name = f'GR_Waltz_{half}_full'
    obj = bpy.data.objects[obj_name]
    for part, (a, b, loop) in PARTS.items():
        obj.animation_data.action = full
        act = cut(full, obj, a, b, loop)
        for o in bpy.context.scene.objects: o.select_set(False)
        obj.select_set(True); bpy.context.view_layer.objects.active = obj
        sc.frame_start, sc.frame_end = 0, b - a
        path = os.path.join(OUT, f'GR_Waltz{part}_{half}.glb')
        bpy.ops.export_scene.gltf(filepath=path, use_selection=True, export_format='GLB', export_animations=True,
                                  export_animation_mode='ACTIVE_ACTIONS', export_force_sampling=True,
                                  export_optimize_animation_size=False, export_frame_range=True)
        print('EXPORTED', path, (b - a) / FPS)
