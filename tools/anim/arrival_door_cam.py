"""Door camera of the arrival cinematic, defined in the scene file like GR_cam_TWOSHOT_side.

    python tools/anim/arrival_door_cam.py

Moving a scene camera with a Transform track did not put it where expected: in game it framed a
wall up close whatever the values (18/11). Cameras defined in <timeline>_Scene.lsx work (the
evening's side two-shot). This one is attached to Gortash's Socket_DIAG_Camera, in his frame
(he faces -z, the doors are about 23 m away at -z), turned 180 degrees to look at the doors.
Then the compiled timeline's door camera uses it, without the transform.
Saving the timeline in the Toolkit can rewrite the _Scene.lsx: rerun this script afterwards.
"""
import os, re, sys, uuid
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import lsf
from build_toolkit import DATA, MOD

GEN = os.path.join(DATA, 'Public', MOD, 'Timeline', 'Generated')
SCENE = os.path.join(GEN, 'GR_Office_Arrival_Scene.lsx')
TL = os.path.join(GEN, 'GR_Office_Arrival.lsf')
CAM_ID = str(uuid.uuid5(uuid.NAMESPACE_URL, 'GR_arrival_scene/door_cam_scene'))
GORTASH_INDEX = 0                       # speaker 0 of GR_Office_Arrival (speaker 1 is the player)
POS = (0.0, 1.7, -0.3)                  # Gortash's point of view: at his eyes, just in front of his face, looking at the doors (user's idea, 18/11); far from him it ended in walls or outside
ROT = (0, 0, 0, 1)                      # 180 degrees: looking at the doors
FOV = 30
OLD_SCENE_CAM = 'a7578f69-00a4-49fe-b8fa-b2cceb145f53'   # cam_player_MCU used with the transform before


def obj(key, vtype, val):
    return (f'<node id="{key}"><children><node id="Object">'
            f'<attribute id="MapKey" type="guid" value="00000000-0000-0000-0000-000000000000"/>'
            f'<attribute id="MapValue" type="{vtype}" value="{val}"/></node></children></node>')


def scene_block():
    x, y, z = POS; qx, qy, qz, qw = ROT
    return ('<node id="TLCameras"><children><node id="Object">'
            f'<attribute id="MapKey" type="guid" value="{CAM_ID}"/><children><node id="TLCameras">'
            f'<attribute id="AttachTo" type="int32" value="{GORTASH_INDEX}"/>'
            '<attribute id="CameraType" type="uint8" value="1"/>'
            f'<attribute id="Identifier" type="guid" value="{CAM_ID}"/>'
            '<attribute id="LookAt" type="int32" value="-2"/>'
            '<attribute id="Name" type="LSString" value="GR_cam_door"/><children>'
            + obj('AttachBone', 'FixedString', 'Socket_DIAG_Camera') + obj('DOF', 'bool', 'false')
            + obj('DOFAperature', 'float', '22') + obj('DOFFarSharpDistance', 'float', '0.2')
            + obj('DOFNearSharpDistance', 'float', '0.5') + obj('DampingStrength', 'float', '5')
            + obj('FoV', 'float', FOV) +
            '<node id="Transform"><children><node id="Object">'
            '<attribute id="MapKey" type="guid" value="00000000-0000-0000-0000-000000000000"/><children><node id="MapValue">'
            f'<attribute id="Position" type="fvec3"><float3 x="{x}" y="{y}" z="{z}"/></attribute>'
            f'<attribute id="RotationQuat" type="fvec4"><float4 x="{qx}" y="{qy}" z="{qz}" w="{qw}"/></attribute>'
            '<attribute id="Scale" type="float" value="1"/>'
            '</node></children></node></children></node>'
            '</children></node></children></node></children></node>\n                ')


def patch_scene():
    s = open(SCENE, encoding='utf-8-sig').read()
    s = re.sub(r'<node id="TLCameras"><children><node id="Object"><attribute id="MapKey" type="guid" value="' + CAM_ID
               + r'"/>.*?(?=<node id="TLInheritedScenes">)', '', s, flags=re.S)   # our block, written on one line
    if '<node id="TLCameras">' in s:
        raise SystemExit('the scene already has other TLCameras: merge by hand')
    i = s.index('<node id="TLInheritedScenes">')
    s = s[:i] + scene_block() + s[i:]
    import xml.etree.ElementTree as ET
    ET.fromstring(s.split('?>', 1)[1])
    open(SCENE, 'w', encoding='utf-8').write(s)


def patch_timeline():
    d = lsf.read(TL)
    comps, cams = [None], []
    def walk(n):
        if n.name == 'EffectComponents': comps[0] = n
        if n.name == 'Object' and n.children and any(a == 'Camera' for a, _, _ in n.children[0].attrs):
            cams.append(n)
        for c in n.children: walk(c)
    for r in d['regions']: walk(r)
    # the door camera is the scene camera that had a transform
    tr = [c for c in comps[0].children if c.attr('Type') == 'TLTransform'
          and [ch for ch in c.children if ch.name == 'Actor'][0].attr('UUID') in {o.attr('MapKey') for o in cams}]
    if tr:
        actor = [ch for ch in tr[0].children if ch.name == 'Actor'][0].attr('UUID')
        comps[0].children.remove(tr[0])
    else:   # already patched: find it by its camera id
        actor = [o.attr('MapKey') for o in cams if o.children[0].attr('Camera') == CAM_ID][0]
    cam = [o for o in cams if o.attr('MapKey') == actor][0]
    v = cam.children[0]
    v.attrs = [(a, t, CAM_ID if a == 'Camera' else val) for a, t, val in v.attrs]
    lsf.write(d, TL)
    return actor


if __name__ == '__main__':
    patch_scene()
    print('scene camera GR_cam_door', CAM_ID, 'at', POS)
    print('timeline door camera', patch_timeline(), 'now uses it, no transform')
