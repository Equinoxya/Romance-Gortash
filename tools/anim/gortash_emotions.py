"""Gortash's facial emotions, line by line, in the compiled timelines.

    python tools/anim/gortash_emotions.py

Run after the Toolkit (re)saves a timeline (and after evening_hands.py for the evening), then
build_pack.py. The Toolkit's "Generate ML Emotions" needs a Larian service the public Toolkit cannot
reach, so the emotions are set here instead.

Palette and rhythm taken from Larian's own Gortash timelines (WYR_KillDirectorGortash_GortashInOffice,
WYR_GortashConfrontation_OM_KarlachAndGortashEncounter, Ceremony, SoulConsumption; read 2026-11-20):
- in conversation he is mostly Thinking, with Happy variation 3 (the smirk) on his wit, Confusion
  (raised eyebrow) for doubt, Anger variation 3 (contained), a little Surprise and Disgust (contempt);
  Sad, Fear and Pain are kept for his death scene, so here Sad only for the rare unguarded moments;
- 2 to 4 changes per line, every 2 to 4 s, often back to Neutral at the end of a long line.
Emotion codes (TLEmotionEvent Key 'Emotion', names from the Toolkit's LSFrameworkPlugin):
1 Neutral, 2 Happy, 4 Thinking, 8 Angry, 16 Fear, 32 Sad, 64 Surprise, 128 Disgust, 1024 Confusion.
"""
import os, sys, uuid
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import lsf
from build_toolkit import DATA, MOD, stable_uuid

NEU, HAP, THI, ANG, SUR, DIS, SAD, CON = 1, 2, 4, 8, 64, 128, 32, 1024
SMIRK = (HAP, 3)

# line -> [(share of the line, emotion, variation)], variation 0 = none
EMOTIONS = {
    'GR_Office_Evening': {
        'N2':   [(0, THI, 1), (.45, *SMIRK), (.9, NEU, 0)],
        'N2D':  [(0, THI, 3), (.6, SAD, 1), (.92, NEU, 0)],
        'N3a':  [(0, *SMIRK), (.3, THI, 1), (.65, *SMIRK)],
        'N3b':  [(0, THI, 0), (.15, *SMIRK), (.5, THI, 1), (.8, HAP, 1)],
        'N3c':  [(0, CON, 1), (.35, THI, 1), (.7, *SMIRK)],
        'N3d':  [(0, THI, 1), (.35, HAP, 1), (.75, SAD, 1), (.95, NEU, 0)],
        'N5':   [(0, THI, 1), (.4, CON, 0), (.7, THI, 3), (.95, NEU, 0)],
        'N5D':  [(0, THI, 0), (.4, HAP, 1), (.75, THI, 3)],
        'N6a':  [(0, *SMIRK), (.5, THI, 1)],
        'N6b':  [(0, CON, 1), (.45, *SMIRK)],
        'N6c':  [(0, *SMIRK), (.5, THI, 2), (.8, *SMIRK)],
        'N6d':  [(0, THI, 1), (.25, HAP, 1), (.7, SAD, 1), (.95, NEU, 0)],
        'N8':   [(0, THI, 3), (.3, *SMIRK), (.6, THI, 1), (.9, NEU, 0)],
        'N8D':  [(0, THI, 3), (.25, *SMIRK), (.65, SAD, 1), (.9, NEU, 0)],
        'N9a2': [(0, SUR, 1), (.45, *SMIRK)],
        'N9b':  [(0, *SMIRK), (.6, THI, 1)],
        'N9c':  [(0, CON, 1), (.3, THI, 1), (.7, *SMIRK)],
        'X1':   [(0, ANG, 3), (.5, THI, 2)],
        'X2':   [(0, THI, 1), (.3, *SMIRK), (.7, THI, 3)],
        'X2D':  [(0, THI, 3), (.5, SAD, 1)],
    },
    'GR_Ball': {
        'N5':   [(0, *SMIRK), (.4, THI, 1), (.75, *SMIRK)],
        'N5D':  [(0, THI, 0), (.4, *SMIRK), (.75, CON, 1)],
        'N6a':  [(0, DIS, 1), (.4, *SMIRK)],
        'N6b':  [(0, THI, 1), (.5, *SMIRK)],
        'N6c':  [(0, *SMIRK), (.45, ANG, 3), (.75, *SMIRK)],
        'N6d':  [(0, THI, 1), (.4, HAP, 1), (.8, THI, 3)],
        'N8':   [(0, *SMIRK)],
        'N9a2': [(0, SUR, 1), (.4, HAP, 1)],
        'N9b2': [(0, *SMIRK), (.6, THI, 1)],
        'N9c':  [(0, CON, 1), (.35, *SMIRK), (.75, HAP, 1)],
        'N9e':  [(0, THI, 1), (.4, *SMIRK), (.75, DIS, 1)],
        'N9x':  [(0, ANG, 3), (.5, THI, 2), (.9, NEU, 0)],
        'N11':  [(0, THI, 1), (.4, CON, 0), (.75, THI, 3)],
        'N11D': [(0, THI, 3), (.5, HAP, 1), (.9, NEU, 0)],
        'N12a': [(0, *SMIRK)],
        'N12b': [(0, THI, 1), (.5, *SMIRK)],
        'N12d': [(0, *SMIRK), (.5, THI, 1), (.8, HAP, 1)],
        'N14':  [(0, HAP, 1), (.6, THI, 1)],
        'N14b': [(0, HAP, 1), (.6, THI, 1)],
    },
}
MARK = 'GR_gortash_emotions'


def nid(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f'{MARK}/{name}'))


def node(name, attrs=(), children=()):
    n = lsf.Node(name); n.attrs = [(a, lsf.TYPE_IDS[t], v) for a, t, v in attrs]; n.children = list(children)
    return n


def gortash_actor(content):
    """The speaker-0 character of the timeline (Gortash in all our scenes)."""
    for n in content.children:
        if n.name != 'TimelineActorData': continue
        for o in (o for c in n.children for o in ([c] if c.name == 'Object' else c.children)):
            for v in o.children:
                if v.name == 'Value' and v.attr('ActorTypeId') == 'character' and v.attr('Speaker') == 0:
                    return o.attr('MapKey')


def apply(scene):
    path = os.path.join(DATA, 'Public', MOD, 'Timeline', 'Generated', scene + '.lsf')
    d = lsf.read(path); content = d['regions'][0]
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
    actor = gortash_actor(content)
    if not actor:
        raise SystemExit(f'{scene}: no speaker-0 character in the timeline')
    phase_of = {p.attr('DialogNodeId'): i for i, p in enumerate(phases)}
    mine = {nid(f'{scene}/{line}') for line in EMOTIONS[scene]}
    def his_emotion(c):
        return c.attr('Type') == 'TLEmotionEvent' and any(
            a.name == 'Actor' and a.attr('UUID') == actor for a in c.children)
    done, missing = [], []
    for line, keys in EMOTIONS[scene].items():
        i = phase_of.get(stable_uuid(f'{scene}/node/{line}'))
        if i is None:
            missing.append(line); continue
        s, e = starts[i]
        # ours from a previous run, and any emotion the generator gave him on this line
        comps.children = [c for c in comps.children
                          if c.attr('ID') != nid(f'{scene}/{line}') and not (his_emotion(c) and c.attr('PhaseIndex') == i)]
        key_nodes = []
        for share, emo, var in keys:
            attrs = [('Time', 'float', round(s + share * (e - s), 3)), ('InterpolationType', 'uint8', 3),
                     ('Emotion', 'int32', emo)]
            if var: attrs.append(('Variation', 'int32', var))
            key_nodes.append(node('Key', attrs))
        comps.children.append(node('EffectComponent', [
            ('Type', 'LSString', 'TLEmotionEvent'), ('ID', 'guid', nid(f'{scene}/{line}')),
            ('StartTime', 'float', s), ('EndTime', 'float', e), ('PhaseIndex', 'int32', i),
            ('IsSnappedToEnd', 'bool', True)],
            [node('Actor', [('UUID', 'guid', actor)]), node('Keys', [], key_nodes)]))
        done.append(line)
    lsf.write(d, path)
    print(f'{scene}: emotions on {len(done)} lines of Gortash' + (f' (not in this timeline: {", ".join(missing)})' if missing else ''))


if __name__ == '__main__':
    for scene in EMOTIONS:
        apply(scene)
