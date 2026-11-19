"""Make a Blender glTF export readable by LSLib (Divine convert-model glb -> GR2).

    python tools/anim/fix_glb.py REFERENCE_FROM_LSLIB.glb EXPORT1.glb [EXPORT2.glb ...]

Blender drops the scene extension EXT_lslib_profile (bone order, skeleton id) that LSLib needs, and
adds the armature object as an extra root node. Copy the extension from a .glb that LSLib wrote
(any animation on the same skeleton), make Dummy_Root the scene root, drop empty child lists.
"""
import json, struct, sys

def rd(p):
    b = open(p, 'rb').read(); n = struct.unpack_from('<I', b, 12)[0]
    return json.loads(b[20:20 + n]), b[20 + n:]

def wr(p, j, rest):
    s = json.dumps(j, separators=(',', ':')).encode(); s += b' ' * ((4 - len(s) % 4) % 4)
    body = struct.pack('<I', len(s)) + b'JSON' + s + rest
    open(p, 'wb').write(b'glTF' + struct.pack('<II', 2, 12 + len(body)) + body)

ref, _ = rd(sys.argv[1])
ext = ref['scenes'][0]['extensions']
for p in sys.argv[2:]:
    j, rest = rd(p)
    j['scenes'][0]['extensions'] = ext
    j['extensionsUsed'] = sorted(set(j.get('extensionsUsed', [])) | {'EXT_lslib_profile'})
    names = [x['name'] for x in j['nodes']]
    root = names.index('Dummy_Root')
    j['scenes'][0]['nodes'] = [root]
    for x in j['nodes']:
        if x.get('children') == [] or (x['name'] not in ext['EXT_lslib_profile']['BoneOrder'] and 'children' in x):
            x.pop('children', None)
    wr(p, j, rest)
    print('fixed', p)
