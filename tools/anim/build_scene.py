import bpy, math
bpy.ops.wm.read_factory_settings(use_empty=True)
D=r"C:\Users\obell\Desktop\GortashAnim\blender"
sc=bpy.context.scene; sc.render.fps=24
def imp(f):
    before=set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=D+"\\"+f); return set(bpy.data.objects)-before
body=imp("Proxy_HUM_M_FullBody.glb")
for o in body:
    if o.name.startswith('Icosphere'): bpy.data.objects.remove(o)
barm=bpy.data.objects['Armature']; barm.name='Corps_Squelette'
idle=imp("HUM_M_Rig_CINE_Still_Breathing_Idle_StandL_01.glb")
master=[o for o in idle if o.type=='ARMATURE'][0]
for o in list(idle):
    if o.type!='ARMATURE': bpy.data.objects.remove(o)
master.name='GR_HandOffer_Squelette'
act=master.animation_data.action; act.name='GR_HandOffer_LOOP'
f0,f1=map(int,act.frame_range); sc.frame_start=f0; sc.frame_end=f1
print("IDLE frames",f0,f1)
# the visible body follows the animated skeleton
for pb in barm.pose.bones:
    if pb.name in master.pose.bones:
        c=pb.constraints.new('COPY_TRANSFORMS'); c.target=master; c.subtarget=pb.name
barm.hide_select=True
# target for the right hand: in front, towards the other character, a little to his right, waist height
bpy.ops.object.empty_add(type='SPHERE', radius=0.06, location=(-0.22,0.45,1.12)); tgt=bpy.context.object; tgt.name='Cible_Main'
bpy.ops.object.empty_add(type='PLAIN_AXES', radius=0.1, location=(-0.35,0.0,0.9)); pole=bpy.context.object; pole.name='Coude_Direction'
ik=master.pose.bones['Elbow_R'].constraints.new('IK'); ik.target=tgt; ik.pole_target=pole; ik.chain_count=2; ik.pole_angle=math.radians(-90)
# the other character, 1.1 m in front
bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=1.7, location=(0,1.1,0.85)); p=bpy.context.object; p.name='Ton_personnage'; p.display_type='WIRE'
bpy.ops.object.camera_add(location=(2.6,0.55,1.35), rotation=(math.radians(85),0,math.radians(90))); sc.camera=bpy.context.object
bpy.ops.wm.save_as_mainfile(filepath=r"C:\Users\obell\Desktop\GortashAnim\GR_HandOffer.blend")
# quick preview render of the middle frame
sc.frame_set((f0+f1)//2)
sc.render.engine='BLENDER_WORKBENCH'; sc.render.resolution_x=640; sc.render.resolution_y=720
sc.render.filepath=r"C:\Users\obell\Desktop\GortashAnim\apercu.png"
bpy.ops.render.render(write_still=True)
print("SAVED")
