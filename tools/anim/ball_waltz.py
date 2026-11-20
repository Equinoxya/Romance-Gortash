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
WYLL = 'Public/SharedDev/Assets/Characters/_Anims/_Cinematic/Act03/CAMP/Wyll_InPartyEND/'
DURATION = 28.6668
ANIMS = {   # name -> (resource id, game .GR2, skeleton)
    'GR_Waltz_Gortash': (stable_uuid('GR/anim/GR_Waltz_Gortash'),
                         WYLL + 'HUM_M_Rig_SCENE_Wyll_InPartyEND_WyllWaltzKissTall_Wyll.GR2',
                         '044ab023-7076-77e6-73c2-d0f26fca0776'),
    'GR_Waltz_Joueuse': (stable_uuid('GR/anim/GR_Waltz_Joueuse'),
                         WYLL + 'HUM_F_Rig/HUM_F_Rig_SCENE_Wyll_InPartyEND_WyllWaltzKissTall_PLYR.GR2',
                         'edda91cd-d2be-3296-087c-45477f36daaa'),
}
APPROACH, DANCE, KISS, PART = (0.0, 3.5), (3.5, 13.0), (13.5, 21.0), (23.5, DURATION)
FADE = 0.6
LINES = {   # line -> what of the waltz it shows
    'N9a': 'start', 'N9b': 'start', 'N9d': 'start',
    'N10': 'dance', 'N11': 'dance', 'N11D': 'dance', 'N12a': 'dance', 'N12b': 'dance', 'N12d': 'dance',
    'N12c': 'kiss', 'N13': 'part',
}
DANCE_DIST = -1.22     # the player in front of Gortash, in his Dummy_Root frame
MARK = 'GR_ball_waltz'


def nid(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f'{MARK}/{name}'))


def node(name, attrs=(), children=()):
    n = lsf.Node(name); n.attrs = [(a, lsf.TYPE_IDS[t], v) for a, t, v in attrs]; n.children = list(children)
    return n


def write_resources():
    """One animation resource per half, laid out like ours (GR_HandKiss_Gortash), pointing at the game's file."""
    template = lsf.read(os.path.join(RES_DIR, '8357d7d4-ef4d-5769-a2c3-d5aa4d2d9349.lsf'))
    for name, (rid, gr2, skeleton) in ANIMS.items():
        d = template
        stack, res = list(d['regions']), None
        while stack and res is None:
            n = stack.pop()
            if n.name == 'Resource': res = n
            stack += n.children
        vals = {'ID': rid, 'Name': name, 'SourceFile': gr2, 'Template': gr2[:-4] + '.Anim.0',
                'Duration': DURATION, 'SkeletonResource': skeleton}
        res.attrs = [(a, t, vals.get(a, v)) for a, t, v in res.attrs]
        lsf.write(d, os.path.join(RES_DIR, rid + '.lsf'))
        print(f'resource   {name} -> {rid}')


def pieces(kind, s, e):
    """[(start, end, offset)] covering the phase s..e."""
    out, t = [], s
    if kind == 'start':
        first = min(e, s + (DANCE[1] - APPROACH[0]))
        out.append((s, first, 0.0)); t = first
        kind = 'dance'
    if kind == 'kiss':
        return [(s, min(e, s + KISS[1] - KISS[0]), KISS[0])] + ([(s + KISS[1] - KISS[0], e, KISS[1])] if e > s + KISS[1] - KISS[0] else [])
    if kind == 'part':
        return [(s, e, PART[0])]
    span = DANCE[1] - DANCE[0]
    while t < e - 0.05:
        end = min(e, t + span)
        out.append((t, end, DANCE[0]))
        t = end
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
        for k, (a, b, off) in enumerate(pieces(kind, s, e)):
            for who, actor, name in (('G', gortash, 'GR_Waltz_Gortash'), ('P', player, 'GR_Waltz_Joueuse')):
                attrs = [('Type', 'LSString', 'TLAnimation'), ('ID', 'guid', nid(f'{who}{i}.{k}')),
                         ('StartTime', 'float', round(a, 3)), ('EndTime', 'float', round(b, 3)),
                         ('PhaseIndex', 'int32', i), ('AnimationSourceId', 'guid', ANIMS[name][0])]
                if off: attrs.append(('AnimationPlayStartOffset', 'double', off))
                attrs += [('FadeIn', 'double', FADE if (k or kind != 'start') else 0.3),
                          ('FadeOut', 'double', FADE), ('AnimationGroup', 'guid', group[who])]
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
    lsf.write(d, TL)
    print('waltz on', ', '.join(done))


if __name__ == '__main__':
    main()
