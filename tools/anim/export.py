import bpy, math
from mathutils import Quaternion
G=r"C:\Users\obell\Desktop\GortashAnim"
bpy.ops.wm.open_mainfile(filepath=G+r"\GR_HandOffer.blend")
sc=bpy.context.scene; m=bpy.data.objects['GR_HandOffer_Squelette']; P=m.pose.bones
loop=m.animation_data.action
ARM=['Shoulder_R','Elbow_R','Wrist_R']
offer={b:P[b].rotation_quaternion.copy() for b in ARM}
# original idle arm rotation at frame 0, from a fresh import
before=set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=G+r"\blender\HUM_M_Rig_CINE_Still_Breathing_Idle_StandL_01.glb")
new=set(bpy.data.objects)-before
ref=[o for o in new if o.type=='ARMATURE'][0]
sc.frame_set(0)
rest={b:ref.pose.bones[b].matrix_basis.to_quaternion() for b in ARM}
idle_src=ref.animation_data.action
# IN: idle body, arm goes from its idle pose to the offer in 1 s, then holds (1.5 s total)
inn=idle_src.copy(); inn.name='GR_HandOffer_IN'
for o in new: bpy.data.objects.remove(o)
m.animation_data.action=inn
def curves(a):
    out=[]
    for l in a.layers:
        for s in l.strips:
            for cb in s.channelbags: out+=list(cb.fcurves)
    return out
for fc in list(curves(inn)):
    if any(f'"{b}"' in fc.data_path for b in ARM) and 'rotation' in fc.data_path: fc.keyframe_points.clear()
for f in range(0,37,2):
    t=min(f/24,1.0); t=t*t*(3-2*t)   # ease in/out
    for b in ARM:
        P[b].rotation_mode='QUATERNION'; P[b].rotation_quaternion=rest[b].slerp(offer[b],t); P[b].keyframe_insert('rotation_quaternion',frame=f)
# cut IN at 36 frames: remove keys after 36
for fc in curves(inn):
    for k in [k for k in fc.keyframe_points if k.co[0]>36][::-1]: fc.keyframe_points.remove(k)
inn.frame_range=(0,36) if hasattr(inn,'frame_range') else None
inn.use_frame_range=True; inn.frame_start=0; inn.frame_end=36
bpy.ops.wm.save_as_mainfile(filepath=G+r"\GR_HandOffer.blend")
# export each action alone, armature only
for o in bpy.data.objects: o.select_set(False)
m.select_set(True); bpy.context.view_layer.objects.active=m
for a,(s,e) in ((inn,(0,36)),(loop,tuple(map(int,loop.frame_range)))):
    m.animation_data.action=a; sc.frame_start,sc.frame_end=s,e
    bpy.ops.export_scene.gltf(filepath=G+rf"\export\{a.name}.glb", use_selection=True, export_animations=True,
                              export_animation_mode='ACTIVE_ACTIONS', export_skins=True, export_def_bones=False,
                              export_frame_range=True, export_force_sampling=True)
    print("EXPORTED",a.name,s,e)
