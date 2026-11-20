"""Cut Wyll's act 3 waltz into four animations for the ball (run headless on a copy of GR_HandAccept.blend).

    blender -b GR_HandAccept_copy.blend --python waltz_export.py -- <folder with the two waltz .glb>

The timeline did not play a game animation started from an offset (AnimationPlayStartOffset, game
20/11): only the piece starting at 0 s played. So each part of the waltz becomes its own animation:
In (0-13 s: walk up, hand, slow dance), Dance (3.5-13 s), Kiss (13.5-21 s), Part (23.5-end).
Exports go to export/, one per half, with the same settings as the hand-kiss exports.
"""
import bpy, os, sys
SRC = sys.argv[sys.argv.index('--') + 1]
OUT = r'C:\Users\obell\Desktop\GortashAnim\export'
FPS = 24
PARTS = {'In': (0.0, 13.0), 'Dance': (3.5, 13.0), 'Kiss': (13.5, 21.0), 'Part': (23.5, 28.6668)}
HALVES = {'Gortash': ('GR_HandOffer_Squelette', 'HUM_M_Rig_SCENE_Wyll_InPartyEND_WyllWaltzKissTall_Wyll.glb'),
          'Joueuse': ('Joueuse_Squelette', 'HUM_F_Rig_SCENE_Wyll_InPartyEND_WyllWaltzKissTall_PLYR.glb')}
sc = bpy.context.scene
sc.render.fps = FPS
for half, (obj_name, glb) in HALVES.items():
    before_o, before_a = set(bpy.data.objects), set(bpy.data.actions)
    bpy.ops.import_scene.gltf(filepath=os.path.join(SRC, glb))
    act = [a for a in bpy.data.actions if a not in before_a][0]
    for o in [o for o in bpy.data.objects if o not in before_o]:
        bpy.data.objects.remove(o)
    act.name = f'GR_Waltz_{half}_full'; act.use_fake_user = True
    obj = bpy.data.objects[obj_name]
    obj.animation_data.action = act
    if act.slots: obj.animation_data.action_slot = act.slots[0]
    for part, (a, b) in PARTS.items():
        for o in bpy.context.scene.objects: o.select_set(False)
        obj.select_set(True); bpy.context.view_layer.objects.active = obj
        sc.frame_start, sc.frame_end = round(a * FPS), round(b * FPS)
        path = os.path.join(OUT, f'GR_Waltz{part}_{half}.glb')
        bpy.ops.export_scene.gltf(filepath=path, use_selection=True, export_format='GLB', export_animations=True,
                                  export_animation_mode='ACTIVE_ACTIONS', export_force_sampling=True,
                                  export_optimize_animation_size=False, export_frame_range=True)
        print('EXPORTED', path)
