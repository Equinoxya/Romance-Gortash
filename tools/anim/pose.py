import bpy, math, sys
from mathutils import Vector, Quaternion, Matrix
TARGET=Vector((-0.20,0.45,1.10))
bpy.ops.wm.open_mainfile(filepath=r"C:\Users\obell\Desktop\GortashAnim\GR_HandOffer.blend")
sc=bpy.context.scene; m=bpy.data.objects['GR_HandOffer_Squelette']; P=m.pose.bones
for pb in P:
    for c in list(pb.constraints): pb.constraints.remove(c)
bpy.data.objects['Cible_Main'].location=TARGET
act=m.animation_data.action
F=0; sc.frame_set(F); vl=bpy.context.view_layer
def W(n): return P[n].head.copy()          # armature space (armature at origin)
def rot_about(pb, R):
    h=pb.head.copy()
    pb.matrix = Matrix.Translation(h) @ R.to_matrix().to_4x4() @ Matrix.Translation(-h) @ pb.matrix
    vl.update()
# mute the arm's own curves so we can pose freely
def curves(a):
    if hasattr(a,'fcurves') and a.fcurves: return list(a.fcurves)
    out=[]
    for l in a.layers:
        for s in l.strips:
            for cb in s.channelbags: out+=list(cb.fcurves)
    return out
ARM=['Shoulder_R','Elbow_R','Wrist_R']
for fc in curves(act):
    if any(f'"{b}"' in fc.data_path for b in ARM): fc.mute=True
sc.frame_set(F)
for it in range(40):
    for j in ('Elbow_R','Shoulder_R'):
        e=W('Wrist_R'); h=W(j)
        a=(e-h).normalized(); b=(TARGET-h).normalized()
        q=a.rotation_difference(b)
        q=Quaternion(q.axis, q.angle*0.5)
        rot_about(P[j], q)
err=(W('Wrist_R')-TARGET).length
print("ERR",round(err,3),"elbow",[round(x,2) for x in W('Elbow_R')],"wrist",[round(x,2) for x in W('Wrist_R')])
# hand: fingers toward the other character and slightly down, palm up
fwd=Vector((0.15,1,-0.25)).normalized()
for it in range(10):
    d=(W('MiddleFinger1_R')-W('Wrist_R')).normalized()
    rot_about(P['Wrist_R'], d.rotation_difference(fwd))
    n=(W('IndexFinger1_R')-W('PinkyFinger0_R')).cross(W('MiddleFinger1_R')-W('Wrist_R')).normalized()
    want=Vector((0,0,-1))
    # rotate around finger axis to bring palm normal up
    d=(W('MiddleFinger1_R')-W('Wrist_R')).normalized()
    nproj=(n-d*n.dot(d)).normalized(); wproj=(want-d*want.dot(d)).normalized()
    ang=math.atan2(nproj.cross(wproj).dot(d), nproj.dot(wproj))
    rot_about(P['Wrist_R'], Quaternion(d, ang))
n=(W('IndexFinger1_R')-W('PinkyFinger0_R')).cross(W('MiddleFinger1_R')-W('Wrist_R')).normalized()
print("PALM normal",[round(x,2) for x in n])
# store the pose as constant keys over the loop
f0,f1=map(int,act.frame_range)
for b in ARM:
    pb=P[b]; pb.rotation_mode='QUATERNION'; q=pb.matrix_basis.to_quaternion(); loc=pb.matrix_basis.to_translation()
    for fc in curves(act):
        if f'"{b}"' in fc.data_path: fc.mute=False
    for fc in [fc for fc in curves(act) if f'"{b}"' in fc.data_path and 'rotation' in fc.data_path]:
        fc.keyframe_points.clear()
    for f in (f0,f1):
        pb.rotation_quaternion=q; pb.keyframe_insert('rotation_quaternion',frame=f)
print("POSE",{b:[round(x,3) for x in P[b].rotation_quaternion] for b in ARM})
bpy.ops.wm.save_as_mainfile(filepath=r"C:\Users\obell\Desktop\GortashAnim\GR_HandOffer.blend")
sc.render.engine='BLENDER_WORKBENCH'; sc.render.resolution_x=640; sc.render.resolution_y=720
cam=sc.camera
bpy.data.objects['Ton_personnage'].hide_render=True
for name,loc,rot in (('cote',(2.6,0.55,1.35),(85,0,90)),('face',(-1.2,2.4,1.4),(82,0,207)),('dessus',(-0.6,1.2,2.6),(30,0,200))):
    cam.location=loc; cam.rotation_euler=[math.radians(x) for x in rot]
    sc.frame_set(100); sc.render.filepath=rf"C:\Users\obell\Desktop\GortashAnim\apercu_{name}.png"; bpy.ops.render.render(write_still=True)
print("DONE")
