import bpy, math
bpy.ops.wm.read_factory_settings(use_empty=True)
G=r"C:\Users\obell\Desktop\GortashAnim"
sc=bpy.context.scene; sc.render.fps=24
def imp(f):
    before=set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=f); return set(bpy.data.objects)-before
body=imp(G+r"\blender\Proxy_HUM_M_FullBody.glb")
barm=[o for o in body if o.type=='ARMATURE'][0]
for o in body:
    if o.name.startswith('Icosphere'): o.hide_render=True
for name,frame in (('GR_HandOffer_IN',0),('GR_HandOffer_IN',36),('GR_HandOffer_LOOP',150)):
    new=imp(G+rf"\check\{name}.glb")
    a=[o for o in new if o.type=='ARMATURE'][0]
    for o in new:
        if o.type!='ARMATURE': o.hide_render=True
    for pb in barm.pose.bones:
        for c in list(pb.constraints): pb.constraints.remove(c)
        if pb.name in a.pose.bones:
            c=pb.constraints.new('COPY_TRANSFORMS'); c.target=a; c.subtarget=pb.name
    bpy.ops.object.camera_add(location=(-1.2,2.4,1.4), rotation=(math.radians(82),0,math.radians(207))); sc.camera=bpy.context.object
    sc.frame_set(frame)
    sc.render.engine='BLENDER_WORKBENCH'; sc.render.resolution_x=400; sc.render.resolution_y=450
    sc.render.filepath=rf"{G}\verif_{name}_{frame}.png"; bpy.ops.render.render(write_still=True)
    a.hide_render=True
print("OK")
