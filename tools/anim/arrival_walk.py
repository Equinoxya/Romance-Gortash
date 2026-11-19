"""Add the player's walk to the arrival cinematic (GR_Office_Arrival), in the compiled timeline.

    python tools/anim/arrival_walk.py

Run after the Toolkit (re)saves the timeline, with the Toolkit closed or the timeline not open.
The player is attached to Gortash (frame of reference, like the wine glass in his hand), turned to
face him, and slides from START_Z metres in front of him to END_Z while playing the game's
cinematic walk: start walking, walk (looped), stop. The camera of the first shot is attached to the
player, so it follows the walk. Only the picture moves: the real character already stands there.
"""
import copy, os, sys, uuid
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import lsf
from build_toolkit import DATA, MOD

TL = os.path.join(DATA, 'Public', MOD, 'Timeline', 'Generated', 'GR_Office_Arrival.lsf')
PLAYER = 'd68d01c3-e5f9-56d6-8df7-ab3cfe130ffd'    # speaker 1 of GR_Office_Arrival
GORTASH = '0d26d4d7-32d8-5f68-b75c-a57208a204e3'   # speaker 0
# Gortash-local distance (m) along his facing axis, over time (s): set off, walk, stop
# The walk lasts the whole narrator line (0-8.64 s): 7.2 m, about 1 m/s while looping.
# (4.4 s / 3.8 m left the player standing for the rest of the line, game 18/11.)
# (Along -Z, 8 m and 4.5 m began in a wall in the preview; this path is along X.)
PATH_X = [(0.0, -9.0), (1.6, -8.2), (7.4, -2.4), (8.6, -1.8)]
END = 13.64
ANIMS = [  # (AnimationSourceId, start, end, loop) - HUM_M names; each body type maps the same id
    ('ba49ec42-65c2-4012-861d-745be5fdfbd9', 0.0, 1.6, False),   # CINE_StandL_ToWalk_01
    ('7bd8e368-5ad3-487b-ab93-f868d968590f', 1.6, 7.4, True),    # CINE_Walk_01
    ('5bac9aab-21d2-4bdf-8cd6-fedb605d720d', 7.4, 8.6, False),   # CINE_Walk_ToStandL_01
]
DIALOG_BIN = os.path.join(DATA, 'Mods', MOD, 'Story', 'DialogsBinary', 'GR_Office_Arrival.lsf')
GROUP = ['8dd83f35-a498-5f3a-b4e3-a9aa3df22210', '2e34ebb1-bee7-5791-acd9-b0b238dd815d']  # A0 then AG
MARK = 'GR_arrival_walk'   # our components carry IDs derived from this, so the script can be rerun


def nid(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f'{MARK}/{name}'))


def N(name, attrs=(), children=()):
    # attribute types are given by name and stored as lsf type ids
    n = lsf.Node(name); n.attrs = [(a, lsf.TYPE_IDS[t], v) for a, t, v in attrs]; n.children = list(children)
    return n


def key(t, val_type, val):
    return N('Key', [('Time', 'float', t), ('InterpolationType', 'uint8', 2), ('Value', val_type, val)])


def main():
    d = lsf.read(TL)
    comps = None
    def find(n):
        nonlocal comps
        if n.name == 'EffectComponents': comps = n
        for c in n.children: find(c)
    for r in d['regions']: find(r)
    ours = {nid(f'anim{i}') for i in range(len(ANIMS))} | {nid('transform')}
    # Drop our previous run AND any other walk/transform on the player: the Toolkit compiles the walk
    # written in the .tml (looping until 7.4 s), which doubled ours: walking on the spot (game, 18/11)
    is_player = lambda c: any(a.name == 'Actor' and a.attr('UUID') == PLAYER for a in c.children)
    comps.children = [c for c in comps.children if c.attr('ID') not in ours
                      and not (c.attr('Type') in ('TLAnimation', 'TLTransform') and is_player(c))]
    group = nid('group')
    for i, (src, s, e, loop) in enumerate(ANIMS):
        attrs = [('Type', 'LSString', 'TLAnimation'), ('ID', 'guid', nid(f'anim{i}'))]
        if s: attrs.append(('StartTime', 'float', s))
        attrs += [('EndTime', 'float', e), ('AnimationSourceId', 'guid', src),
                  ('FadeIn', 'double', 0.25), ('FadeOut', 'double', 0.25), ('AnimationGroup', 'guid', group)]
        if loop: attrs.append(('Continuous', 'bool', True))
        comps.children.append(N('EffectComponent', attrs, [N('Actor', [('UUID', 'guid', PLAYER)])]))
    chan = lambda keys: N('TransformChannel', [], [N('Keys', [], keys)])
    x = [key(t, 'float', v) for t, v in PATH_X]
    zero = lambda: [key(0.0, 'float', 0.0)]
    rot = [key(0.0, 'fvec4', [0.0, -0.7071, 0.0, 0.7071])]          # turned 180 degrees: facing Gortash
    frame = N('Key', [('Time', 'float', 0.0), ('InterpolationType', 'uint8', 2)], [N('Value', [], [N('frameOfReference', [
        ('targetId', 'guid', GORTASH), ('targetBone', 'FixedString', 'Dummy_Root'),
        ('OneFrameOnly', 'bool', False), ('KeepScale', 'bool', True)])])])
    tr = N('EffectComponent', [('Type', 'LSString', 'TLTransform'), ('ID', 'guid', nid('transform')),
            ('EndTime', 'float', END)],
            [N('Actor', [('UUID', 'guid', PLAYER)]),
            N('TransformChannels', [], [chan(x), chan(zero()), chan(zero()), chan(rot),
            N('TransformChannel'),
            N('TransformChannel', [], [N('Keys', [], [frame])])])])
    comps.children.append(tr)
    # First shot: behind Gortash's shoulder, looking at the player (cam_player_OTS_subject1 of the
    # camera scene); the generated camera was attached to the player's start and did not follow
    import copy as _copy
    cam_actor = nid('cam_ots')
    holder = [None]
    def find_actor(n, parent):
        if n.name == 'Object' and n.attr('MapKey') == '0ff48363-808a-492c-89d3-3ca86831c342':
            holder[0] = (n, parent)
        for c in n.children: find_actor(c, n)
    for r in d['regions']: find_actor(r, None)
    src, parent = holder[0]
    parent.children = [c for c in parent.children if c.attr('MapKey') != cam_actor]
    cam = _copy.deepcopy(src)
    cam.attrs = [(a, t, cam_actor if a == 'MapKey' else v) for a, t, v in cam.attrs]
    val = cam.children[0]
    vals = {'Camera': 'ff9136ca-e96e-4709-8d3c-f4a6d0de5690', 'AttachTo': GORTASH, 'LookAt': PLAYER}
    val.attrs = [(a, t, vals.get(a, v)) for a, t, v in val.attrs]
    parent.children.append(cam)
    # The shots, in time order: first = the walk, last = Gortash's line, the ones in between are the
    # narrator's text after the walk (they showed a wall at floor level: the scene camera
    # GR_cam_follow, 5.6 m behind Gortash). All but the last use the same shoulder camera.
    shots = sorted([c for c in comps.children if c.attr('Type') == 'TLShot'], key=lambda c: c.attr('StartTime') or 0)
    for shot in shots[:-1]:
        for cc in shot.children:
            if cc.name == 'CameraContainer':
                cc.attrs = [(a, t, cam_actor if a == 'Object' else v) for a, t, v in cc.attrs]
    single_phase(d)
    lsf.write(d, TL)
    print('arrival walk:', len(ANIMS), 'animations + transform on the player;', len(shots) - 1, 'shots on the shoulder camera')
    group_dialog()


def single_phase(d):
    """One phase for both nodes (narrator A0, Gortash AG), as the generator makes it. Undoes the
    two-phase split of 18/11 (the unvoiced narrator line then waited for a click). Playing it once
    relies on A0 and AG being one group in the dialog (group_dialog)."""
    find = lambda n, name: [c for c in n.children if c.name == name]
    content = d['regions'][0]
    phases = find(find(content, 'Effect')[0], 'Phases')[0]
    mapping = find(find(content, 'TimelinePhases')[0], 'Object')[0].children
    setattr_ = lambda n, k, v: n.attrs.__setitem__([a for a, _, _ in n.attrs].index(k), (k, [t for a, t, _ in n.attrs if a == k][0], v))
    if len(phases.children) > 1:
        total = sum(p.attr('Duration') for p in phases.children)
        phases.children = phases.children[:1]
        setattr_(phases.children[0], 'Duration', total)
    for m in mapping:
        setattr_(m, 'MapValue', 0)
    print('phases: one phase,', len(mapping), 'nodes on it')


def group_dialog():
    """Put A0 and AG in one group in the compiled dialog, the way the game compiles its cinematics
    (SHA_NightsongPrison_CINE_EnterWater): GroupID = first node's UUID, GroupIndex 0, 1, right after
    UUID. Without it, AG leading on to the nested evening replayed the whole phase (game log, 18/11:
    27.9 s from DialogStarted to InstanceDialogChanged). build_dialogs.py writes the same groups in
    the .lsj, so a Toolkit save of the dialog gives the same result."""
    d = lsf.read(DIALOG_BIN)
    nodes = [c for c in d['regions'][0].children if c.name == 'nodes'][0]
    done = 0
    for n in nodes.children:
        if n.name == 'node' and n.attr('UUID') in GROUP:
            n.attrs = [a for a in n.attrs if a[0] not in ('GroupID', 'GroupIndex')]
            i = [a for a, _, _ in n.attrs].index('UUID') + 1
            n.attrs[i:i] = [('GroupID', lsf.TYPE_IDS['FixedString'], GROUP[0]),
                            ('GroupIndex', lsf.TYPE_IDS['int32'], GROUP.index(n.attr('UUID')))]
            done += 1
    if done != 2:
        raise SystemExit(f'group_dialog: found {done} of the 2 nodes')
    lsf.write(d, DIALOG_BIN)
    print('dialog: A0 + AG grouped in the compiled dialog')


if __name__ == '__main__':
    main()
