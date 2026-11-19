"""Arrival cinematic, version "Gortash at his desk" (compiled timeline + scene cameras).

    python tools/anim/arrival_desk.py

Gortash waits at his desk, reading, his back to the doors (GR_Letters.txt puts him at
(-17.25, 73.01, 209.75), a spot read in game on 18/11, turned 101.3 degrees). The doors are
then about 14 m behind him. In his frame (he faces -z): door = (-3.1, +13.7).
1. Over the desk, in front of him, looking at him: he reads, the player comes in far behind him.
2. Cut, behind the player: the last steps up to his back.
3. His line: the generated close-up.
Run with the timeline closed in the Toolkit; a Toolkit save of this timeline undoes it.
The turn on his line comes in a next step.
"""
import os, re, sys, uuid
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import lsf
from build_toolkit import DATA, MOD

GEN = os.path.join(DATA, 'Public', MOD, 'Timeline', 'Generated')
SCENE = os.path.join(GEN, 'GR_Office_Arrival_Scene.lsx')
TL = os.path.join(GEN, 'GR_Office_Arrival.lsf')
PLAYER, GORTASH = 'd68d01c3-e5f9-56d6-8df7-ab3cfe130ffd', '0d26d4d7-32d8-5f68-b75c-a57208a204e3'
GORTASH_INDEX = 0
DESK_ACTOR, FOLLOW_ACTOR = '42d481b4-120d-5a38-bca0-73de3beb6d4b', '773fbee6-349c-5aed-8741-8b09008880c2'

def nid(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f'GR_arrival_scene/{name}'))

# scene cameras, in Gortash's frame from his Socket_DIAG_Camera (head height); unrotated looks +z
CAMS = [  # (id, name, position, rotation quaternion, fov)
    (nid('door_cam_scene'), 'GR_cam_desk', (0.5, -0.3, -2.2), (0, 0, 0, 1), 45),    # beyond the desk, facing him; 1.4 m in front at head height framed him from the belt up, desk unseen (game, 18/11)
    (nid('follow_cam_scene'), 'GR_cam_follow', (-1.0, -0.1, 5.6), (0, 1, 0, 0), 40), # behind the player (1.5 m at the cut), facing his back
]
CUT, END_A0, SEQ = 5.5, 8.64, 13.64
# player path in Gortash's frame (time, x, z): from the doors to just behind him
# The player comes in at (-8.47, 73.01, 210.10), a point read in game on 18/11 (the first door
# point, 14 m away, was replaced). He is turned like MessHallBodyguard_008_BackupPosition (101.3
# degrees), so that point is (-2.07, 8.54) in his frame: about 7.4 m, one continuous walk at
# about 1 m/s, across the cut.
PATH = [(0.0, -2.07, 8.54), (1.6, -1.95, 8.04), (CUT, -0.957, 4.05), (7.4, -0.474, 2.1), (8.6, -0.3, 1.4)]
PLAYER_ROT = [0.0, -0.1212, 0.0, 0.9926]   # -0.243 rad: walking along that line, towards him
ANIM_TIMES = {'ba49ec42-65c2-4012-861d-745be5fdfbd9': (0.0, 1.6),     # CINE_StandL_ToWalk_01
              '7bd8e368-5ad3-487b-ab93-f868d968590f': (1.6, 7.4),     # CINE_Walk_01 (loops)
              '5bac9aab-21d2-4bdf-8cd6-fedb605d720d': (7.4, 8.6)}     # CINE_Walk_ToStandL_01
READ_MAP = '5470292e-5bb1-4470-a317-950b96e27d32'                       # CINE_Read_Map_01


def obj(key, vtype, val):
    return (f'<node id="{key}"><children><node id="Object">'
            f'<attribute id="MapKey" type="guid" value="00000000-0000-0000-0000-000000000000"/>'
            f'<attribute id="MapValue" type="{vtype}" value="{val}"/></node></children></node>')


def cam_block(cid, name, pos, rot, fov):
    x, y, z = pos; qx, qy, qz, qw = rot
    return ('<node id="Object">'
            f'<attribute id="MapKey" type="guid" value="{cid}"/><children><node id="TLCameras">'
            f'<attribute id="AttachTo" type="int32" value="{GORTASH_INDEX}"/>'
            '<attribute id="CameraType" type="uint8" value="1"/>'
            f'<attribute id="Identifier" type="guid" value="{cid}"/>'
            '<attribute id="LookAt" type="int32" value="-2"/>'
            f'<attribute id="Name" type="LSString" value="{name}"/><children>'
            + obj('AttachBone', 'FixedString', 'Socket_DIAG_Camera') + obj('DOF', 'bool', 'false')
            + obj('DOFAperature', 'float', '22') + obj('DOFFarSharpDistance', 'float', '0.2')
            + obj('DOFNearSharpDistance', 'float', '0.5') + obj('DampingStrength', 'float', '5')
            + obj('FoV', 'float', fov) +
            '<node id="Transform"><children><node id="Object">'
            '<attribute id="MapKey" type="guid" value="00000000-0000-0000-0000-000000000000"/><children><node id="MapValue">'
            f'<attribute id="Position" type="fvec3"><float3 x="{x}" y="{y}" z="{z}"/></attribute>'
            f'<attribute id="RotationQuat" type="fvec4"><float4 x="{qx}" y="{qy}" z="{qz}" w="{qw}"/></attribute>'
            '<attribute id="Scale" type="float" value="1"/>'
            '</node></children></node></children></node>'
            '</children></node></children></node>')


def patch_scene():
    s = open(SCENE, encoding='utf-8-sig').read()
    s = re.sub(r'<node id="TLCameras"><children><node id="Object"><attribute id="MapKey" type="guid" value="'
               + CAMS[0][0] + r'"/>.*?(?=<node id="TLInheritedScenes">)', '', s, flags=re.S)
    if '<node id="TLCameras">' in s:
        raise SystemExit('the scene already has other TLCameras: merge by hand')
    block = '<node id="TLCameras"><children>' + ''.join(cam_block(*c) for c in CAMS) + '</children></node>\n                '
    i = s.index('<node id="TLInheritedScenes">')
    s = s[:i] + block + s[i:]
    import xml.etree.ElementTree as ET
    ET.fromstring(s.split('?>', 1)[1])
    open(SCENE, 'w', encoding='utf-8').write(s)


def N(name, attrs=(), children=()):
    n = lsf.Node(name); n.attrs = [(a, lsf.TYPE_IDS[t], v) for a, t, v in attrs]; n.children = list(children)
    return n


def setattr_(n, name, tname, val):
    for i, (a, t, v) in enumerate(n.attrs):
        if a == name:
            n.attrs[i] = (a, t, val); return
    n.attrs.append((name, lsf.TYPE_IDS[tname], val))


def keys(ch):
    return [c for c in ch.children if c.name == 'Keys'][0]


def patch_timeline():
    d = lsf.read(TL)
    comps, cams = [None], {}
    def walk(n):
        if n.name == 'EffectComponents': comps[0] = n
        if n.name == 'Object' and n.children and n.children[0].attr('Camera'): cams[n.attr('MapKey')] = n.children[0]
        for c in n.children: walk(c)
    for r in d['regions']: walk(r)
    C = comps[0].children
    actor = lambda c: [x for x in c.children if x.name == 'Actor'][0].attr('UUID')
    # cameras: both look at Gortash
    setattr_(cams[DESK_ACTOR], 'Camera', 'guid', CAMS[0][0]); setattr_(cams[DESK_ACTOR], 'LookAt', 'guid', GORTASH)
    setattr_(cams[FOLLOW_ACTOR], 'Camera', 'guid', CAMS[1][0]); setattr_(cams[FOLLOW_ACTOR], 'LookAt', 'guid', GORTASH)   # looking at the player, Gortash was out of frame (game, 18/11)
    shots = sorted([c for c in C if c.attr('Type') == 'TLShot'], key=lambda c: c.attr('StartTime') or 0)
    setattr_(shots[0], 'EndTime', 'float', CUT)
    setattr_(shots[1], 'StartTime', 'float', CUT)
    # player walk
    for c in C:
        if c.attr('Type') == 'TLAnimation' and c.attr('AnimationSourceId') in ANIM_TIMES:
            s, e = ANIM_TIMES[c.attr('AnimationSourceId')]
            if s: setattr_(c, 'StartTime', 'float', s)
            setattr_(c, 'EndTime', 'float', e)
    tr = [c for c in C if c.attr('Type') == 'TLTransform' and actor(c) == PLAYER][0]
    ch = [x for x in tr.children if x.name == 'TransformChannels'][0].children
    mk = lambda t, vt, v: N('Key', [('Time', 'float', t), ('InterpolationType', 'uint8', 2), ('Value', vt, v)])
    keys(ch[0]).children = [mk(t, 'float', x) for t, x, z in PATH]
    keys(ch[2]).children = [mk(t, 'float', z) for t, x, z in PATH]
    keys(ch[3]).children = [mk(0.0, 'fvec4', PLAYER_ROT)]
    # Gortash reads at his desk through the whole scene (for now)
    rid = nid('gortash/readmap')
    comps[0].children = [c for c in C if c.attr('ID') != rid]
    comps[0].children.append(N('EffectComponent', [
        ('Type', 'LSString', 'TLAnimation'), ('ID', 'guid', rid), ('EndTime', 'float', SEQ),
        ('AnimationSourceId', 'guid', READ_MAP), ('FadeIn', 'double', 0.5), ('FadeOut', 'double', 0.5),
        ('AnimationGroup', 'guid', nid('gortash/group')), ('Continuous', 'bool', True)],
        [N('Actor', [('UUID', 'guid', GORTASH)])]))
    lsf.write(d, TL)


if __name__ == '__main__':
    patch_scene()
    patch_timeline()
    print('arrival at the desk: 2 scene cameras, walk from the doors behind him, Gortash reading')
