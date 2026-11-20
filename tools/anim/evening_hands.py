"""Hand gestures of the evening (GR_Office_Evening), in the compiled timeline.

    python tools/anim/evening_hands.py

Run after the Toolkit (re)saves the evening timeline, with the Toolkit closed, then build_pack.py.
- Hand offer ("come back"): Gortash starts GR_HandOffer_IN OFFER_AT seconds into the line, then
  holds GR_HandOffer_LOOP until the line ends (it was 2.5 s before the end: too late, game 18/11).
- Hand kiss (narrator line "He turns your hand over..."): GR_HandAccept_Gortash and _Joueuse,
  filmed with the camera of the hand offer (the player's close-up hid the hands, game 18/11).
The hand-accept animations were added straight into the compiled file: a Toolkit save of the
timeline drops them, so this script puts them back when they are missing.
"""
import os, sys, uuid
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import lsf
from build_toolkit import DATA, MOD

TL = os.path.join(DATA, 'Public', MOD, 'Timeline', 'Generated', 'GR_Office_Evening.lsf')
GORTASH = 'c8e31ca3-90e7-53f2-b035-a57c7d4c730a'   # actors of this timeline
PLAYER = '07190402-febe-5fb5-91b3-1f3525334698'
OFFER_IN, OFFER_LOOP = '504eb042-442b-5912-8a83-8a07ac590865', '3edd2852-cebd-5be0-be3e-d53229eafd01'
ACCEPT = [('561ba179-110d-5412-9793-064dbb42143a', GORTASH), ('b1f70ade-ea5d-5511-98a0-111c46556bd5', PLAYER)]
ACCEPT_LEN = 3.0
OFFER_AT = 3.5          # s into the line: after his opening gesture (2.2 s), on "So here is one"
HAND_CAM = '5acd0ea2-9c47-4776-af77-d35f89019ecb'   # camera of the hand-offer shots
KISS_NODE = '7fe2eb4a-6159-5e93-90f8-7ec7852baa14'  # "He turns your hand over and presses his lips..."
MARK = 'GR_evening_hands'
# Gortash's step forward on "He sets his glass down and steps closer" (removed, game 18/11)
STEP_ANIM, STEP_NODE = 'afd91676-b953-474c-975b-b268780c1e5d', '8ef52b08-ab6b-5d06-9820-0499dd9610b5'
# The hands only meet at the spacing of GR_HandAccept.blend: the player 0.68 m in front of Gortash.
# In game she stands about 1.1 m away (GR_Letters.txt, PlayerCloser), so from the step closer to
# the hand kiss the player is drawn there, in Gortash's frame (Dummy_Root). Its X axis is his SIDE:
# X = -0.68 put her at his shoulder, Z = +0.68 behind him (game 19/11): his front is -Z; she is turned 180 degrees to face him.
CLOSE_X = 0.0            # sideways; Blender has her 0.12 m to his right, add it here if the hands miss
CLOSE_Z = -0.68
CLOSE_ROT = [0.0, 1.0, 0.0, 0.0]
# Gortash's replies just before (N6a, N6c, N6d) are close-ups of him: placing her there hides the jump
# that whipped her hair at the start of N7 (game 19/11). N6b has another camera (9b704794), left out.
HIDDEN_PLACE_NODES = ['844d1ae3-cd2e-5a3f-b1ad-1fd66d9b9bf4', 'e030fa92-152f-5587-a781-6e70342ba99a',
                      'dedc417d-ff83-591d-b93a-f0549a349df5']
CLOSE_NODES = [STEP_NODE, KISS_NODE] + HIDDEN_PLACE_NODES   # + the hand-offer lines, found by their animation
# Vanilla gesture of Gortash after the kiss: read as a bow (game 19/11), removed
BOW_ANIM = '85cc45da-8f37-49e4-af64-1737fcf56c5b'
# Hand-kiss animations (added in the compiled file): the hands let go over 1 s, not 0.3 s (game 19/11)
KISS_ANIMS, KISS_FADE_OUT = ['8357d7d4-ef4d-5769-a2c3-d5aa4d2d9349', '80c04527-b35b-50fa-9ced-cba8acc40c88'], 1.0
# The player stands in front of Gortash for the whole evening, not from N6 on (game 20/11: she moved
# in the middle of the talk). The 0.3 s fade between the arrival cinematic and the evening hides the move.
CLOSE_EVERYWHERE = True
# No line filmed the player any more (game 20/11). On the long lines where he talks about her, the
# end of the line cuts to her face (camera actor of cam_player_MCU, attached to the player).
PLAYER_CAM = 'c2b18d1e-cdc9-43e9-abb1-dd86a03824e5'
REACTION_AT = 0.65   # share of the line on Gortash before the cut to her
REACTION_NODES = {   # node -> line
    'N2': None, 'N2D': None, 'N3b': None, 'N3d': None, 'N5': None, 'N5D': None, 'N6d': None, 'N9c': None}


def nid(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f'{MARK}/{name}'))


def setattr_(n, k, v, t=None):
    names = [a for a, _, _ in n.attrs]
    if k in names:
        i = names.index(k); n.attrs[i] = (k, n.attrs[i][1], v)
    else:
        n.attrs.append((k, lsf.TYPE_IDS[t], v))


def main():
    d = lsf.read(TL)
    content = d['regions'][0]
    find = lambda n, name: [c for c in n.children if c.name == name]
    phases = find(find(content, 'Effect')[0], 'Phases')[0].children
    starts, t = [], 0.0
    for p in phases:
        starts.append((t, t + p.attr('Duration'))); t += p.attr('Duration')
    comps = []
    def walk(n):
        if n.name == 'EffectComponents': comps.append(n)
        for c in n.children: walk(c)
    walk(content)
    comps = comps[0]
    anims = [c for c in comps.children if c.attr('Type') == 'TLAnimation']

    # Hand offer: every phase that has it
    for ph in sorted({c.attr('PhaseIndex') for c in anims if c.attr('AnimationSourceId') == OFFER_IN}):
        s, e = starts[ph]
        for c in anims:
            if c.attr('PhaseIndex') != ph: continue
            # IN ends on the first pose of LOOP (within 2 degrees): no fade between them. With IN fading
            # out 0.3 s and LOOP fading in 0.3 s, the idle pose came back and the arm dropped (game 19/11).
            if c.attr('AnimationSourceId') == OFFER_IN:
                setattr_(c, 'StartTime', s + OFFER_AT); setattr_(c, 'EndTime', s + OFFER_AT + 1.5)
                setattr_(c, 'FadeOut', 0.0, 'double')
            elif c.attr('AnimationSourceId') == OFFER_LOOP:
                setattr_(c, 'StartTime', s + OFFER_AT + 1.5); setattr_(c, 'EndTime', e)
                setattr_(c, 'FadeIn', 0.0, 'double')
        print(f'hand offer: phase {ph}, from {OFFER_AT} s into the line, held until its end ({e - s:.1f} s)')

    # Hand kiss
    kiss = [i for i, p in enumerate(phases) if p.attr('DialogNodeId') == KISS_NODE]
    if not kiss:
        raise SystemExit('evening_hands: hand-kiss line not found in the timeline')
    ph = kiss[0]; s, e = starts[ph]
    group = next((c.attr('AnimationGroup') for c in anims if c.attr('AnimationGroup')), nid('group'))
    for i, (src, actor) in enumerate(ACCEPT):
        c = next((c for c in anims if c.attr('AnimationSourceId') == src), None)
        if c is None:
            c = lsf.Node('EffectComponent')
            c.attrs = [('Type', lsf.TYPE_IDS['LSString'], 'TLAnimation'), ('ID', lsf.TYPE_IDS['guid'], nid(f'accept{i}'))]
            a = lsf.Node('Actor'); a.attrs = [('UUID', lsf.TYPE_IDS['guid'], actor)]
            c.children = [a]
            comps.children.append(c)
            print('hand kiss: added', src)
        setattr_(c, 'StartTime', s, 'float'); setattr_(c, 'EndTime', s + ACCEPT_LEN, 'float')
        setattr_(c, 'PhaseIndex', ph, 'int32'); setattr_(c, 'AnimationSourceId', src, 'guid')
        # FadeOut 0: the kiss starts on its last pose (within 3 degrees); a fade let the idle pose
        # back in between the two and the arms dipped (game 20/11)
        setattr_(c, 'FadeIn', 0.3, 'double'); setattr_(c, 'FadeOut', 0.0, 'double')
        setattr_(c, 'AnimationGroup', group, 'guid')
    for c in comps.children:
        if c.attr('Type') == 'TLShot' and c.attr('PhaseIndex') == ph:
            for cc in c.children:
                if cc.name == 'CameraContainer':
                    cc.attrs = [(a, t, HAND_CAM if a == 'Object' else v) for a, t, v in cc.attrs]
    print(f'hand kiss: phase {ph}, both animations at its start, filmed with the hand-offer camera')
    before = len(comps.children)
    comps.children = [c for c in comps.children if not (c.attr('Type') == 'TLAnimation'
                      and c.attr('AnimationSourceId') == BOW_ANIM and c.attr('PhaseIndex') == ph)]
    print('hand kiss: bow after the kiss removed' if len(comps.children) < before else 'hand kiss: no bow to remove')
    kisses = [c for c in comps.children if c.attr('Type') == 'TLAnimation' and c.attr('AnimationSourceId') in KISS_ANIMS]
    for c in kisses:
        setattr_(c, 'FadeIn', 0.0, 'double'); setattr_(c, 'FadeOut', KISS_FADE_OUT, 'double')
    print(f'hand kiss: {len(kisses)} kiss animations, fade out {KISS_FADE_OUT} s'
          + ('' if len(kisses) == 2 else '  !! expected 2: re-add them in the Toolkit'))

    # No step forward for Gortash
    step = [i for i, p in enumerate(phases) if p.attr('DialogNodeId') == STEP_NODE]
    before = len(comps.children)
    comps.children = [c for c in comps.children if not (c.attr('Type') == 'TLAnimation'
                      and c.attr('AnimationSourceId') == STEP_ANIM and c.attr('PhaseIndex') in step)]
    print('step closer: Gortash walk removed' if len(comps.children) < before else 'step closer: no walk to remove')

    # The player close to Gortash, one transform per phase
    close = sorted({i for i, p in enumerate(phases) if p.attr('DialogNodeId') in CLOSE_NODES}
                   | {c.attr('PhaseIndex') for c in anims if c.attr('AnimationSourceId') == OFFER_IN})
    if CLOSE_EVERYWHERE:
        close = list(range(len(phases)))
    ours = {nid(f'close{i}') for i in range(len(phases))}   # previous run
    comps.children = [c for c in comps.children if c.attr('ID') not in ours]
    N = lambda name, attrs=(), children=(): _node(name, attrs, children)
    for i in close:
        s, e = starts[i]
        key = lambda v, t: N('Key', [('Time', 'float', s), ('InterpolationType', 'uint8', 2), ('Value', t, v)])
        chan = lambda k: N('TransformChannel', [], [N('Keys', [], [k])])
        frame = N('Key', [('Time', 'float', s), ('InterpolationType', 'uint8', 2)], [N('Value', [], [N('frameOfReference', [
            ('targetId', 'guid', GORTASH), ('targetBone', 'FixedString', 'Dummy_Root'),
            ('OneFrameOnly', 'bool', False), ('KeepScale', 'bool', True)])])])
        comps.children.append(N('EffectComponent', [
            ('Type', 'LSString', 'TLTransform'), ('ID', 'guid', nid(f'close{i}')),
            ('StartTime', 'float', s), ('EndTime', 'float', e), ('PhaseIndex', 'int32', i),
            ('IsSnappedToEnd', 'bool', True)], [
            N('Actor', [('UUID', 'guid', PLAYER)]),
            N('TransformChannels', [], [chan(key(CLOSE_X, 'float')), chan(key(0.0, 'float')),
              chan(key(CLOSE_Z, 'float')), chan(key(CLOSE_ROT, 'fvec4')), N('TransformChannel'),
              N('TransformChannel', [], [N('Keys', [], [frame])])])]))
    print(f'player {CLOSE_Z} m in front of Gortash in phases {close}')
    # Reaction shots on the player at the end of the long lines about her
    from build_toolkit import stable_uuid
    react = {stable_uuid(f'GR_Office_Evening/node/{n}') for n in REACTION_NODES}
    mine = {nid(f'react{i}') for i in range(len(phases))}
    comps.children = [c for c in comps.children if c.attr('ID') not in mine]   # previous run
    added = []
    for i, p in enumerate(phases):
        if p.attr('DialogNodeId') not in react: continue
        s, e = starts[i]
        shots = [c for c in comps.children if c.attr('Type') == 'TLShot' and c.attr('PhaseIndex') == i]
        if len(shots) != 1: continue
        cut = round(s + REACTION_AT * (e - s), 2)
        setattr_(shots[0], 'EndTime', cut); setattr_(shots[0], 'IsSnappedToEnd', False, 'bool')
        comps.children.append(N('EffectComponent', [
            ('Type', 'LSString', 'TLShot'), ('ID', 'guid', nid(f'react{i}')),
            ('StartTime', 'float', cut), ('EndTime', 'float', e), ('PhaseIndex', 'int32', i),
            ('IsSnappedToEnd', 'bool', True)], [N('CameraContainer', [('Object', 'guid', PLAYER_CAM)])]))
        added.append(i)
    print(f'reaction shots on the player in phases {added}')
    lsf.write(d, TL)


def _node(name, attrs=(), children=()):
    n = lsf.Node(name); n.attrs = [(a, lsf.TYPE_IDS[t], v) for a, t, v in attrs]; n.children = list(children)
    return n


if __name__ == '__main__':
    main()
