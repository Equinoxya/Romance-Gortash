"""The dance of the ball (GR_Ball): Wyll's act 3 waltz, played by Gortash and the player.

    python tools/anim/ball_waltz.py

Run after the Toolkit (re)saves the GR_Ball timeline, then gortash_emotions.py, then build_pack.py.

Source: the waltz of Wyll's romance ending (timeline Wyll_InPartyEND, phases 7 to 11), one half per
actor. Wyll has Gortash's skeleton (human male), so his half plays on Gortash as it is. The resources
below point at the game's own .GR2 files (Models.pak, Public/SharedDev/...): nothing is copied.
Placement, read in that timeline: Wyll at z -0.84 turned 180 degrees, the player at z +0.38, i.e. the
player 1.22 m in front of him (his front is -Z in his Dummy_Root frame, as in the office).

The waltz (28.67 s) seen on our two skeletons (GortashAnim, 2026-11-20):
  0-3.5 s they walk up and he takes her hand; 3.5-13 s slow dance, cheek to cheek;
  13.5-21 s kiss; 21-23.5 s still in each other's arms; 23.5-28.67 s they part.
Use in the ball:
  taking his hand (N9a, N9b, N9d): from 0 s, then the slow dance;
  on the floor (N10, N11, N11D, N12a, N12b, N12d): the slow dance (3.5-13 s), in pieces with a fade;
  "Pull him closer. Stop talking" (N12c): the kiss;
  "The music ends" (N13, grouped with N14): they part.
Only the "Tall" player half exists here (human, elf, half-elf, tiefling, drow, githyanki female):
the game also has Short and Strong halves (dwarf, halfling, gnome; half-orc, strong bodies) and the
male player halves, not wired yet.
"""
import os, sys, uuid
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import lsf
from build_toolkit import DATA, MOD, stable_uuid

SCENE = 'GR_Ball'
TL = os.path.join(DATA, 'Public', MOD, 'Timeline', 'Generated', SCENE + '.lsf')
RES_DIR = os.path.join(DATA, 'Public', MOD, 'Content', 'Assets', '[PAK]_GR_Animations')
# The game did not play an animation started from an offset (AnimationPlayStartOffset, game 20/11):
# only the first 13 s of the waltz showed, then both stood still. So the waltz is cut into four
# animations of our own, each starting at its first frame (GortashAnim/waltz_export.py, Blender):
PARTS = {'In': 11.8333, 'Loop': 4.0833, 'Kiss': 9.1667, 'Part': 7.6667}   # durations, s (waltz_export.py)
# In ends on Loop's first pose and Loop on its own first pose: In -> Loop -> Loop... with no fade,
# and Loop is Continuous (the game repeats it to the end of the component, like GR_HandOffer_LOOP).
# The first cut (Dance restarted every 9.5 s with fades) was jerky (game 20/11).
SKELETON = {'Gortash': '044ab023-7076-77e6-73c2-d0f26fca0776', 'Joueuse': 'edda91cd-d2be-3296-087c-45477f36daaa'}
ANIMS = {f'GR_Waltz{p}_{h}': (stable_uuid(f'GR/anim/GR_Waltz{p}_{h}'),
                              f'Public/{MOD}/Assets/Animations/GR_Waltz{p}_{h}.GR2', SKELETON[h], d)
         for p, d in PARTS.items() for h in SKELETON}
OLD = [stable_uuid('GR/anim/GR_Waltz_Gortash'), stable_uuid('GR/anim/GR_Waltz_Joueuse'),
       stable_uuid('GR/anim/GR_WaltzDance_Gortash'), stable_uuid('GR/anim/GR_WaltzDance_Joueuse')]   # earlier cuts
LOOP_IDS = [ANIMS[f'GR_WaltzLoop_{h}'][0] for h in SKELETON]
FADE = 0.6
LINES = {   # line -> what of the waltz it shows
    'N9a': 'start', 'N9b': 'start', 'N9d': 'start',
    'N10': 'dance', 'N11': 'dance', 'N11D': 'dance', 'N12a': 'dance', 'N12b': 'dance', 'N12d': 'dance',
    'N12c': 'kiss', 'N13': 'part',
}
DANCE_DIST = -1.22     # the player in front of Gortash, in his Dummy_Root frame
MARK = 'GR_ball_waltz'
# Music: the epilogue party's (EPI_Epilogue_EnterParty), the way that timeline plays it: sound events
# in the timeline's EnterPhaseSoundEvents / ExitSoundEvents regions (the dialog's music), not TLSoundEvent.
MUSIC_ENTER = '9ca172cf-da90-46d6-8ce2-98206eb00c2a'   # EPI_Epilogue_EnterParty_Music_Enter
MUSIC_EXIT = '03e5f847-fc44-431e-83a9-f91d9dc986a9'    # EPI_Epilogue_EnterParty_Music_Exit
# Camera: the generated timeline only has close-ups, which filmed the inside of her hair during the
# dance (game 20/11). The dance lines use the office's side two-shot (GR_cam_TWOSHOT_side, played in
# game on 17/11), copied into GR_Ball_Scene.lsx with a camera actor of its own.
TWOSHOT = '7c1e2a90-3b5d-4f62-9a18-6d0e4b2f8c11'
SCENES_DIR = os.path.join(DATA, 'Public', MOD, 'Timeline', 'Generated')
CAMERA_LINES = list(LINES) + ['N7']
MUSIC_FROM = 'N7'                                      # "The orchestra begins something slow"
MUSIC_UNTIL = ['N13', 'N9e', 'N9x']                    # the music ends / no dance / refused


def nid(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f'{MARK}/{name}'))


def node(name, attrs=(), children=()):
    n = lsf.Node(name); n.attrs = [(a, lsf.TYPE_IDS[t], v) for a, t, v in attrs]; n.children = list(children)
    return n


def write_resources():
    """One animation resource per part and half, laid out like ours (GR_HandKiss_Gortash)."""
    template = lsf.read(os.path.join(RES_DIR, '8357d7d4-ef4d-5769-a2c3-d5aa4d2d9349.lsf'))
    for old in OLD:
        if os.path.exists(os.path.join(RES_DIR, old + '.lsf')): os.remove(os.path.join(RES_DIR, old + '.lsf'))
    for name, (rid, gr2, skeleton, duration) in ANIMS.items():
        d = template
        stack, res = list(d['regions']), None
        while stack and res is None:
            n = stack.pop()
            if n.name == 'Resource': res = n
            stack += n.children
        vals = {'ID': rid, 'Name': name, 'SourceFile': gr2, 'Template': gr2[:-4] + '.Anim.0',
                'Duration': duration, 'SkeletonResource': skeleton}
        res.attrs = [(a, t, vals.get(a, v)) for a, t, v in res.attrs]
        lsf.write(d, os.path.join(RES_DIR, rid + '.lsf'))
        print(f'resource   {name} -> {rid}')


def pieces(kind, s, e):
    """[(start, end, part, fade in, continuous)] covering the phase s..e."""
    if kind == 'part':
        return [(s, e, 'Part', FADE, False)]
    first = {'start': 'In', 'dance': None, 'kiss': 'Kiss'}[kind]
    out, t = [], s
    if first:
        end = min(e, s + PARTS[first])
        out.append((s, end, first, 0.3 if kind == 'start' else FADE, False)); t = end
    if t < e - 0.05:   # then the loop, repeated by the game to the end of the line
        out.append((t, e, 'Loop', 0.0 if first else FADE, True))
    return out


def main():
    write_resources()
    d = lsf.read(TL); content = d['regions'][0]
    find = lambda n, name: [c for c in n.children if c.name == name]
    phases = find(find(content, 'Effect')[0], 'Phases')[0].children
    starts, t = [], 0.0
    for p in phases:
        starts.append((t, t + p.attr('Duration'))); t += p.attr('Duration')
    comps = []
    def walk(n):
        if n.name == 'EffectComponents': comps.append(n)
        for c in n.children: walk(c)
    walk(content); comps = comps[0]
    actors = {}
    for n in content.children:
        if n.name != 'TimelineActorData': continue
        for o in (o for c in n.children for o in ([c] if c.name == 'Object' else c.children)):
            for v in o.children:
                if v.name == 'Value' and v.attr('ActorTypeId') == 'character':
                    actors['player' if v.attr('IsPlayer') else v.attr('Speaker')] = o.attr('MapKey')
    gortash, player = actors[0], actors['player']
    ours = set()
    for i in range(len(phases)):
        for k in range(8):
            for who in ('G', 'P', 'T'):
                ours.add(nid(f'{who}{i}.{k}'))
    comps.children = [c for c in comps.children if c.attr('ID') not in ours]
    phase_of = {p.attr('DialogNodeId'): i for i, p in enumerate(phases)}
    group = {'G': nid('group/G'), 'P': nid('group/P')}
    done = []
    for line, kind in LINES.items():
        i = phase_of.get(stable_uuid(f'{SCENE}/node/{line}'))
        if i is None:
            continue
        s, e = starts[i]
        parts = pieces(kind, s, e)
        for k, (a, b, part, fade_in, continuous) in enumerate(parts):
            for who, actor, name in (('G', gortash, f'GR_Waltz{part}_Gortash'), ('P', player, f'GR_Waltz{part}_Joueuse')):
                attrs = [('Type', 'LSString', 'TLAnimation'), ('ID', 'guid', nid(f'{who}{i}.{k}')),
                         ('StartTime', 'float', round(a, 3)), ('EndTime', 'float', round(b, 3)),
                         ('PhaseIndex', 'int32', i), ('AnimationSourceId', 'guid', ANIMS[name][0])]
                fade_out = FADE if k == len(parts) - 1 else 0.0
                attrs += [('FadeIn', 'double', fade_in), ('FadeOut', 'double', fade_out),
                          ('AnimationGroup', 'guid', group[who])]
                if continuous: attrs.append(('Continuous', 'bool', True))
                comps.children.append(node('EffectComponent', attrs, [node('Actor', [('UUID', 'guid', actor)])]))
        # the player at the waltz's distance, facing him, in his frame
        key = lambda v, t: node('Key', [('Time', 'float', s), ('InterpolationType', 'uint8', 2), ('Value', t, v)])
        chan = lambda k: node('TransformChannel', [], [node('Keys', [], [k])])
        frame = node('Key', [('Time', 'float', s), ('InterpolationType', 'uint8', 2)], [node('Value', [], [node('frameOfReference', [
            ('targetId', 'guid', gortash), ('targetBone', 'FixedString', 'Dummy_Root'),
            ('OneFrameOnly', 'bool', False), ('KeepScale', 'bool', True)])])])
        comps.children.append(node('EffectComponent', [
            ('Type', 'LSString', 'TLTransform'), ('ID', 'guid', nid(f'T{i}.0')),
            ('StartTime', 'float', s), ('EndTime', 'float', e), ('PhaseIndex', 'int32', i),
            ('IsSnappedToEnd', 'bool', True)], [
            node('Actor', [('UUID', 'guid', player)]),
            node('TransformChannels', [], [chan(key(0.0, 'float')), chan(key(0.0, 'float')),
              chan(key(DANCE_DIST, 'float')), chan(key([0.0, 1.0, 0.0, 0.0], 'fvec4')), node('TransformChannel'),
              node('TransformChannel', [], [node('Keys', [], [frame])])])]))
        done.append(f'{line}:{kind}')
    set_music(d, phase_of)
    set_camera(content, comps, phase_of, gortash)
    lsf.write(d, TL)
    print('waltz on', ', '.join(done))


def set_camera(content, comps, phase_of, gortash):
    import re
    office = open(os.path.join(SCENES_DIR, 'GR_Office_Evening_Scene.lsx'), encoding='utf-8').read()
    ball_path = os.path.join(SCENES_DIR, SCENE + '_Scene.lsx')
    ball = open(ball_path, encoding='utf-8').read()
    if 'GR_cam_TWOSHOT_side' not in ball:
        lines = office.split(chr(10))
        a = next(i for i, l in enumerate(lines) if l.strip() == '<node id="TLCameras">' and l.startswith(' ' * 16 + '<'))
        b = next(i for i, l in enumerate(lines) if i > a and l.startswith(' ' * 16 + '</node>'))
        block = chr(10).join(lines[a:b + 1])
        mark = ' ' * 16 + '<node id="TLInheritedScenes">'
        assert mark in ball, 'GR_Ball_Scene.lsx layout changed'
        ball = ball.replace(mark, block + chr(10) + mark, 1)
        open(ball_path, 'w', encoding='utf-8', newline='').write(ball)
        print('camera     GR_cam_TWOSHOT_side added to GR_Ball_Scene.lsx')
    # camera actor, copied from a generated one
    actor_id = nid('cam/twoshot')
    holder = None
    for n in content.children:
        if n.name != 'TimelineActorData': continue
        for c in n.children:
            objs = [c] if c.name == 'Object' else c.children
            for o in objs:
                if o.name == 'Object' and any(v.name == 'Value' and v.attr('ActorTypeId') == 'scenecam' for v in o.children):
                    holder = (c if c.name != 'Object' else n, o); break
            if holder: break
    parent, model = holder
    parent.children = [o for o in parent.children if o.attr('MapKey') != actor_id]
    import copy
    cam = copy.deepcopy(model)
    cam.attrs = [(a, t, actor_id if a == 'MapKey' else v) for a, t, v in cam.attrs]
    for v in cam.children:
        if v.name == 'Value':
            v.attrs = [(a, t, {'Camera': TWOSHOT, 'AttachTo': gortash, 'LookAt': gortash}.get(a, v_)) for a, t, v_ in v.attrs]
    parent.children.append(cam)
    shots = 0
    for line in CAMERA_LINES:
        i = phase_of.get(stable_uuid(f'{SCENE}/node/{line}'))
        if i is None: continue
        for c in comps.children:
            if c.attr('Type') == 'TLShot' and c.attr('PhaseIndex') == i:
                for cc in c.children:
                    if cc.name == 'CameraContainer':
                        cc.attrs = [(a, t, actor_id if a == 'Object' else v) for a, t, v in cc.attrs]; shots += 1
    print(f'camera     side two-shot on {shots} shots of the dance')


def set_music(d, phase_of):
    region = {r.name: r for r in d['regions']}
    def event(eid, typ='SoundEvent'):
        return node(typ, [('EventID', 'guid', eid), ('SoundType', 'uint8', 1)])
    def phase_map(name, entries):
        m = [c for c in region[name].children if c.name == 'SoundEventMap'][0]
        mine = {i for i, _ in entries}
        m.children = [o for o in m.children if o.attr('MapKey') not in mine]
        for i, eid in entries:
            m.children.append(node('Object', [('MapKey', 'uint64', i)], [node('SoundEventMap', [], [event(eid)])]))
    start = phase_of.get(stable_uuid(f'{SCENE}/node/{MUSIC_FROM}'))
    stops = [phase_of[stable_uuid(f'{SCENE}/node/{n}')] for n in MUSIC_UNTIL if stable_uuid(f'{SCENE}/node/{n}') in phase_of]
    if start is None:
        print('music: no phase for', MUSIC_FROM); return
    phase_map('EnterPhaseSoundEvents', [(start, MUSIC_ENTER)] + [(i, MUSIC_EXIT) for i in stops])
    ex = region['ExitSoundEvents']   # and when the dialog ends, whatever the path
    ex.children = [c for c in ex.children if c.attr('EventID') != MUSIC_EXIT] + [event(MUSIC_EXIT, 'GlobalSoundEvent')]
    print(f'music: epilogue party music from phase {start} ({MUSIC_FROM}), stopped in phases {stops} and at the end')


if __name__ == '__main__':
    main()
