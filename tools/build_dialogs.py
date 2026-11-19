"""Generate Toolkit dialog sources (.lsj) from the dialogue scripts.

    python tools/build_dialogs.py

Run with the Toolkit closed. Then open each dialog in the Dialog Editor (MoonGlasses) and
File > Save once: the editor writes the compiled DialogsBinary/*.lsf itself.

Format learned from a dialog made in the editor (Toolkit/templates/dialog_template.lsj) and from
the game's own dialogs:
- TagGreeting / TagAnswer = line said by an NPC (or the narrator, speaker -666)
- TagQuestion = player choice
- leaf nodes carry endnode = true
- a line's versions are TaggedTexts; each has tag rules on the player (speaker 1).
  The first version whose rules pass is shown, so the version with no rule goes last.

Texts are not written here: every line points to its handle in Localization/handles.md,
whose text is already in GortashRomance.loca.xml.
"""
import copy, json, os, sys, uuid as uuid_mod
sys.path.insert(0, os.path.dirname(__file__))
import lsf
from lsf import Node
from build_toolkit import DATA, MOD, REPO, ENGINE, handles, flag_uuid, stable_uuid

TEMPLATE = os.path.join(REPO, 'Toolkit', 'templates', 'dialog_template.lsj')
DIALOGS_DIR = os.path.join(DATA, 'Mods', MOD, 'Story', 'Dialogs')
BANK_DIR = os.path.join(DATA, 'Public', MOD, 'Content', 'Assets', '[PAK]_Dialogs')

GORTASH = 'b878a854-f790-4999-95c4-3f20f00f65ac'        # S_GLO_Gortash
PLAYERS = 'e0d1ff71-04a8-4340-ae64-9684d846eb83'        # GROUP_Players
NPC, PLAYER, NARRATOR = 0, 1, -666

TAG = {
    'DURGE': 'cd611d7d-b67d-42b4-a75c-a0c6091ef8a2',     # REALLY_DARK_URGE (what game dialogs check)
    'FEMALE': '3806477c-65a7-4100-9f92-be4c12c4fa4f',
    'NEUTRAL': '987da248-4855-40b8-9182-4ff04eb7c13d',   # IDENTITY_NEUTRAL
}
HAS_ALL, HAS_NONE = 0, 2   # TagCombineOp values seen in game dialogs

# ---------------------------------------------------------------------------
# Scenes. Each node: id -> dict(kind, who, only, next, set, check)
#   kind: 'line' (NPC/narrator) or 'choice' (player)
#   who: 'gortash' or 'narrator' (lines only)
#   only: None, 'tav' or 'durge'
#   next: list of node ids, in priority order (first valid NPC line wins)
# ---------------------------------------------------------------------------
def line(who, nxt=(), only=None, **kw):
    return dict(kind='line', who=who, next=list(nxt), only=only, **kw)


def choice(nxt=(), only=None, **kw):
    return dict(kind='choice', next=list(nxt), only=only, **kw)


def nested(dialog):
    """Hand over to another of our dialogs inside the same dialog session (game's "Nested Dialog"
    node, as in SHA_NightsongPrison_CINE_EnterWater): no return to the game in between.
    The game then sends InstanceDialogChanged instead of DialogEnded for this dialog."""
    return dict(kind='nested', target=dialog, next=[], only=None)


A_CHOICES = ['A1', 'A2', 'A3', 'A4']
B_CHOICES = ['B1', 'B2', 'B3', 'B4', 'B5']
C_CHOICES = ['C1', 'C2', 'C3']
X2 = ['X2D', 'X2']

OFFICE = {
    'name': 'GR_Office_Evening',
    'source': 'GR_Office_Evening',     # section in handles.md
    'synopsis': 'Step 2. Evening in Gortash\'s office after the invitation letter. Flirt; the player opens or declines the romance.',
    'trigger': 'Started by GR_Letters.txt when the player closes the invitation letter. Requires GR_Letter1_Delivered; '
               'the scene plays once (GR_Office_Visited, set by N1). Choosing "Not tonight" sets nothing.',
    'root': 'L0',
    'nodes': {
        'L0':  line('narrator', ['L1', 'L2'], root=True,
                    check={'GR_Letter1_Delivered': True, 'GR_Office_Visited': False}),
        'L1':  choice(['N1']),
        'L2':  choice(['L3']),
        'L3':  line('narrator'),
        'N1':  line('narrator', ['N2D', 'N2'], set={'GR_Office_Visited': True}),
        'N2D': line('gortash', A_CHOICES, only='durge'),
        'N2':  line('gortash', A_CHOICES, only='tav'),
        'A1':  choice(['N3a']), 'A2': choice(['N3b']), 'A3': choice(['N3c']), 'A4': choice(['N3d'], only='durge'),
        'N3a': line('gortash', ['N4']), 'N3b': line('gortash', ['N4']),
        'N3c': line('gortash', ['N4']), 'N3d': line('gortash', ['N4']),
        'N4':  line('narrator', ['N5D', 'N5']),
        'N5D': line('gortash', B_CHOICES, only='durge'),
        'N5':  line('gortash', B_CHOICES, only='tav'),
        'B1':  choice(['N6a']), 'B2': choice(['N6b']), 'B3': choice(['N6c']),
        'B4':  choice(['N6d'], only='durge'), 'B5': choice(['X1']),
        'N6a': line('gortash', ['N7']), 'N6b': line('gortash', ['N7']),
        'N6c': line('gortash', ['N7']), 'N6d': line('gortash', ['N7']),
        'N7':  line('narrator', ['N8D', 'N8']),
        'N8D': line('gortash', C_CHOICES, only='durge'),
        'N8':  line('gortash', C_CHOICES, only='tav'),
        'C1':  choice(['N9a'], set={'GR_Romance_Interested': True}),
        'C2':  choice(['N9b'], set={'GR_Romance_Interested': True}),
        'C3':  choice(['N9c'], set={'GR_Romance_Declined': True}),
        'N9a': line('narrator', ['N9a2']), 'N9a2': line('gortash', X2),
        'N9b': line('gortash', X2), 'N9c': line('gortash'),
        'X1':  line('gortash'),
        'X2D': line('gortash', only='durge'), 'X2': line('gortash', only='tav'),
    },
}

N5 = ['N5D', 'N5']
BALL = {
    'name': 'GR_Ball',
    'source': 'GR_Ball',
    'synopsis': 'Step 3. The ball at Wyrm\'s Rock: the court watches, Gortash claims his dance. '
                'Herald and patriar lines are narrator text for now.',
    'trigger': 'Started by GR_Letters.txt when the player closes the invitation card. Requires GR_Ball_Invited; '
               'the scene plays once (GR_Ball_Attended, set by N1). Choosing "Not tonight" sets nothing.',
    'root': 'L0',
    'nodes': {
        'L0':   line('narrator', ['L1', 'L2'], root=True,
                     check={'GR_Ball_Invited': True, 'GR_Ball_Attended': False}),
        'L1':   choice(['N1']),
        'L2':   choice(['L3']),
        'L3':   line('narrator'),
        'N1':   line('narrator', ['N2'], set={'GR_Ball_Attended': True}),
        'N2':   line('narrator', ['N3']),            # herald
        'N3':   line('narrator', ['N4']),            # patriar
        'N4':   line('narrator', ['A1', 'A2', 'A3']),  # second patriar
        'A1':   choice(N5), 'A2': choice(['N4b']), 'A3': choice(['N4c'], only='durge'),
        'N4b':  line('narrator', N5), 'N4c': line('narrator', N5),
        'N5D':  line('gortash', ['B1', 'B2', 'B3', 'B4'], only='durge'),
        'N5':   line('gortash', ['B1', 'B2', 'B3', 'B4'], only='tav'),
        'B1':   choice(['N6a']), 'B2': choice(['N6b']), 'B3': choice(['N6c']), 'B4': choice(['N6d'], only='durge'),
        'N6a':  line('gortash', ['N7']), 'N6b': line('gortash', ['N7']),
        'N6c':  line('gortash', ['N7']), 'N6d': line('gortash', ['N7']),
        'N7':   line('narrator', ['N8']),
        'N8':   line('gortash', ['N8n']),
        'N8n':  line('narrator', ['C1', 'C2', 'C3', 'C4']),
        'C1':   choice(['N9a']), 'C2': choice(['N9b']), 'C3': choice(['N9c']),
        'C4':   choice(['N9x'], set={'GR_Romance_Ended': True}),
        'N9a':  line('narrator', ['N9a2']), 'N9a2': line('gortash', ['N10']),
        'N9b':  line('narrator', ['N9b2']), 'N9b2': line('gortash', ['N10']),
        'N9c':  line('gortash', ['N9c2']), 'N9c2': line('narrator', ['C3a', 'C3b']),
        'C3a':  choice(['N9d']), 'C3b': choice(['N9e']),
        'N9d':  line('narrator', ['N10']),
        'N9e':  line('gortash', ['N14b']),
        'N9x':  line('gortash'),
        'N10':  line('narrator', ['N11D', 'N11']),
        'N11D': line('gortash', ['D1', 'D2', 'D3', 'D4'], only='durge'),
        'N11':  line('gortash', ['D1', 'D2', 'D3', 'D4'], only='tav'),
        'D1':   choice(['N12a']), 'D2': choice(['N12b']), 'D3': choice(['N12c']), 'D4': choice(['N12d'], only='durge'),
        'N12a': line('gortash', ['N13']), 'N12b': line('gortash', ['N13']),
        'N12c': line('narrator', ['N13']), 'N12d': line('gortash', ['N13']),
        'N13':  line('narrator', ['N14']),
        'N14':  line('gortash', set={'GR_Ball_Danced': True}),
        'N14b': line('gortash'),
    },
}


D_CHOICES = ['D1', 'D2', 'D3', 'D3R']
NIGHT = {
    'name': 'GR_Private_Night',
    'source': 'GR_Private_Night',
    'synopsis': "Step 4. Private night in Gortash's rooms: first names, his confession, consent, a night told "
                'by the narrator with a fade to black, then dawn.',
    'trigger': 'Started by GR_Letters.txt when the player closes the second letter. Requires GR_Night_Invited and '
               'neither GR_Romance_Committed nor GR_Romance_Ended. Leaving at B3 or "Not tonight" sets nothing.',
    'root': 'L0',
    'nodes': {
        'L0':  line('narrator', ['L1', 'L2'], root=True,
                    check={'GR_Night_Invited': True, 'GR_Romance_Committed': False, 'GR_Romance_Ended': False}),
        'L1':  choice(['N1']), 'L2': choice(['L3']), 'L3': line('narrator'),
        'N1':  line('narrator', ['N2']),
        'N2':  line('gortash', ['A1', 'A2', 'A3', 'A4']),
        'A1':  choice(['N3a']), 'A2': choice(['N3b']), 'A3': choice(['N3c']), 'A4': choice(['N3d'], only='durge'),
        'N3a': line('gortash', ['N4D', 'N4']), 'N3b': line('gortash', ['N4D', 'N4']),
        'N3c': line('gortash', ['N4D', 'N4']), 'N3d': line('gortash', ['N4D', 'N4']),
        'N4D': line('gortash', ['B1', 'B2', 'B3'], only='durge'),
        'N4':  line('gortash', ['B1', 'B2', 'B3'], only='tav'),
        'B1':  choice(['N5a'], set={'GR_First_Names': True}),
        'B2':  choice(['N5b'], set={'GR_First_Names': True}),
        'B3':  choice(['N5x']),
        'N5a': line('narrator', ['N6D', 'N6']), 'N5b': line('gortash', ['N6D', 'N6']),
        'N5x': line('gortash'),
        'N6D': line('gortash', ['C1', 'C2', 'C3', 'C5', 'C4'], only='durge'),
        'N6':  line('gortash', ['C1', 'C2', 'C3', 'C5', 'C4'], only='tav'),
        'C1':  choice(['N7'], only='tav'), 'C2': choice(['N7']), 'C3': choice(['N7']),
        'C5':  choice(['N7'], only='durge'),
        'C4':  choice(['N7x'], set={'GR_Romance_Ended': True}),
        'N7x': line('gortash'),
        'N7':  line('narrator', ['N7b']),
        'N7b': line('gortash', ['E1', 'E2', 'E3', 'E4']),
        'E1':  choice(['N8a']), 'E2': choice(['N8b']), 'E3': choice(['N8c']), 'E4': choice(['N8d'], only='durge'),
        'N8a': line('narrator', ['N8']), 'N8b': line('narrator', ['N8']),
        'N8c': line('narrator', ['N8']), 'N8d': line('narrator', ['N8']),
        'N8':  line('narrator', ['N9']),
        'N9':  line('narrator', ['N10R', 'N10D', 'N10']),
        'N10R': line('gortash', D_CHOICES, only='durge', check={'BhaalResisted': True}),
        'N10D': line('gortash', D_CHOICES, only='durge', check={'BhaalResisted': False}),
        'N10': line('gortash', D_CHOICES, only='tav'),
        'D1':  choice(['N11']), 'D2': choice(['N11b']),
        'D3':  choice(['N11d'], only='durge', check={'BhaalResisted': False}),
        'D3R': choice(['N11r'], only='durge', check={'BhaalResisted': True}),
        'N11b': line('gortash', ['N11']), 'N11d': line('gortash', ['N11']), 'N11r': line('gortash', ['N11']),
        'N11': line('narrator', set={'GR_Romance_Committed': True}),
    },
}


def staged_office():
    """Office evening split in two dialogs, for staging in Gortash's real office
    (Story/drafts/GR_Office_Staging.txt): the "tonight?" choice, then the evening itself."""
    n = OFFICE['nodes']
    invitation = {
        'name': 'GR_Office_Invitation', 'source': 'GR_Office_Evening',
        'synopsis': 'Step 2, part 1. After reading the invitation letter: go to Wyrm\'s Rock tonight, or not.',
        'trigger': 'Started by GR_Letters.txt when the player closes the invitation letter. '
                   '"Tonight" sets GR_Office_Visited; the script then moves the party into the office.',
        'root': 'L0',
        'nodes': {'L0': n['L0'], 'L1': choice([], set={'GR_Office_Visited': True}), 'L2': n['L2'], 'L3': n['L3']},
    }
    evening_nodes = {k: v for k, v in n.items() if not k.startswith('L')}
    evening_nodes['N1'] = line('narrator', ['N2D', 'N2'], root=True, check={'GR_Letter1_Delivered': True})
    evening = dict(OFFICE, root='N1', nodes=evening_nodes,
                   synopsis='Step 2, part 2. Evening in Gortash\'s office. Flirt; the player opens or declines the romance.',
                   trigger='Started by GR_Letters.txt once the party and Gortash have been moved into his office.')
    arrival = {
        'name': 'GR_Office_Arrival', 'source': 'GR_Office_Evening',
        'synopsis': 'Step 2, cinematic. The player pushes open the office doors and walks up to Gortash.',
        'trigger': 'Started by GR_Letters.txt once the player stands at the office doors; the evening follows.',
        'root': 'A0',
        # AG (Gortash) also gives the timeline generator a speaker to film: with only the narrator
        # it found no speaker and made no cameras
        # NE: the evening follows in the same dialog session (no return to the game between the two)
        # A0 and AG form one group (one timeline phase, played once, no "Continue" in between), as in
        # the game's cinematics: once split in two phases, the unvoiced narrator line waited for a click
        'nodes': {'A0': line('narrator', ['AG'], root=True, check={'GR_Letter1_Delivered': True}, group=('A0', 0)),
                  'AG': line('gortash', ['NE'], group=('A0', 1)),
                  'NE': nested('GR_Office_Evening')},
    }
    return [invitation, arrival, evening]


def _scenes():
    # The office evening is played as two dialogs (staged in Gortash's office, see GR_Letters.txt)
    return staged_office() + [BALL, NIGHT] + MEMORIES + [ORIN]


def memory(n, name, title, after):
    """Extension: one narrated Dark Urge memory (Dialogs/GR_Memories.md). Gortash only speaks
    inside the memory, so the dialog may start whatever state he is in (AllowDeadSpeakers)."""
    seen = f'GR_Memory{n}_Seen'
    return {
        'name': name, 'source': 'GR_Memories', 'dead_ok': True,
        'synopsis': f'Extension. Dark Urge memory {n}: {title}. Narrated, Gortash speaks inside the memory ("tu" in French).',
        'trigger': f'Started by GR_Letters.txt at the first long rest after {after}, for a Dark Urge only, '
                   f'one memory per rest. Plays once ({seen}).',
        'root': f'M{n}a',
        'nodes': {
            f'M{n}a': line('narrator', [f'M{n}b'], root=True, check={seen: False}, set={seen: True}),
            f'M{n}b': line('gortash', [f'M{n}c']),
            f'M{n}c': line('narrator'),
        },
    }


MEMORIES = [memory(1, 'GR_Memory_FirstMeeting', 'first meeting', 'GR_Romance_Interested'),
            memory(2, 'GR_Memory_Rooftop', 'the rooftop', 'GR_Ball_Attended'),
            memory(3, 'GR_Memory_LastMorning', 'the last morning', 'GR_Romance_Committed')]

ORIN_START = {'GR_Orin_Done': False}
ORIN = {
    'name': 'GR_Orin',
    'source': 'GR_Orin',
    'synopsis': "Extension. Gortash's reaction to Orin's death, after the private night. "
                "Durge lines depend on what happened in Bhaal's temple.",
    'trigger': 'Started by GR_Letters.txt at the first long rest after Orin dies, if she dies after the private night '
               '(GR_Romance_Committed) and the romance has not ended. Plays once (GR_Orin_Done, set at the start).',
    'root': ['O1D', 'O1'],     # first valid root plays: Durge, then Tav
    'nodes': {
        'O1D': line('narrator', ['O2D'], only='durge', root=True, check=ORIN_START, set={'GR_Orin_Done': True}),
        'O1':  line('gortash', ['OA1', 'OA2'], only='tav', root=True, check=ORIN_START, set={'GR_Orin_Done': True}),
        'OA1': choice(['O2a']), 'OA2': choice(['O2b']),
        'O2a': line('gortash'), 'O2b': line('gortash'),
        'O2D': line('gortash', ['OD1', 'OD2', 'OD3']),
        'OD1': choice(['O3r'], check={'BhaalResisted': True}),
        'OD2': choice(['O3a'], check={'BhaalAccepted': True}),
        'OD3': choice(['O3k']),
        'O3r': line('gortash', ['O4r']), 'O4r': line('narrator'),
        'O3a': line('gortash', ['O4a']), 'O4a': line('narrator'),
        'O3k': line('gortash'),
    },
}



# ---------------------------------------------------------------------------
def fs(v): return {'type': 'FixedString', 'value': v}
def b(v): return {'type': 'bool', 'value': v}


def rule(tag, op):
    return {'HasChildRules': b(False), 'TagCombineOp': {'type': 'uint8', 'value': op},
            'Tags': [{'Tag': [{'Object': {'type': 'guid', 'value': TAG[tag]}}]}],
            'speaker': {'type': 'int32', 'value': PLAYER}}


def tagged_text(handle, rules, seed):
    return {'HasTagRule': b(True),
            'RuleGroup': [{'Rules': [{'Rule': rules}] if rules else [{}],
                           'TagCombineOp': {'type': 'uint8', 'value': 0}}],
            'TagTexts': [{'TagText': [{
                'LineId': {'type': 'guid', 'value': stable_uuid(seed)},
                'TagText': {'handle': handle, 'type': 'TranslatedString', 'version': 1},
                'stub': b(True)}]}]}


def texts(h, scene, nid):
    """Versions of a line: identity variants first, the no-rule version last.
    Tav / Dark Urge is not tested here but on the node (see flags()): text blocks that combine
    two rules make the editor report them as unreachable ("invalid structure")."""
    base = []
    seed = f"{scene['name']}/{nid}"
    if (nid, 'all') in h:
        return [tagged_text(h[(nid, 'all')], base, seed)]
    return [tagged_text(h[(nid, 'NB')], base + [rule('NEUTRAL', HAS_ALL)], seed + '/NB'),
            tagged_text(h[(nid, 'F')], base + [rule('FEMALE', HAS_ALL)], seed + '/F'),
            tagged_text(h[(nid, 'M')], base, seed + '/M')]


# Base game global flags usable in check/set, by short name
BASE_FLAGS = {
    'BhaalResisted': '74944ac3-1ea0-4eae-9653-1f1319f8646b',   # ORI_DarkUrge_State_BhaalResisted
    'BhaalAccepted': '904c45e0-bb06-40ed-b5d7-4f1c851b9d86',   # ORI_DarkUrge_State_BhaalAccepted
}


def flags(d, only=None):
    """Flag checks or sets. only='tav'/'durge' adds a REALLY_DARK_URGE tag check on the player,
    the way most game dialogs test it (a 'Tag' group whose paramval is the player's speaker index)."""
    groups = []
    if d:
        groups.append({'flag': [{'UUID': fs(BASE_FLAGS.get(name) or flag_uuid(name)), 'value': b(val)}
                                for name, val in d.items()],
                       'type': fs('Global')})
    if only:
        groups.append({'flag': [{'UUID': fs(TAG['DURGE']), 'paramval': {'type': 'int32', 'value': PLAYER},
                                 'value': b(only == 'durge')}],
                       'type': fs('Tag')})
    return [{'flaggroup': groups}] if groups else [{}]


def section_handles(scene):
    """handles.md lines restricted to this scene's section."""
    out, inside = {}, False
    import re
    for l in open(os.path.join(REPO, 'Localization', 'handles.md'), encoding='utf-8'):
        if l.startswith('## '):
            inside = l.strip() == '## ' + scene['source']
        elif inside:
            m = re.match(r'\| (\S+) \| [^|]+ \| (\w+) \| `(h[0-9a-g]+)` \|', l)
            if m: out[(m.group(1), m.group(2))] = m.group(3)
    return out


def keep_editor_data(path, d):
    """When the dialog was already saved in the editor, keep what the editor added to it:
    the link to its generated timeline, the timeline grouping of each node, and the flag
    combinations the user chose to ignore. Regenerating would otherwise unlink the timeline."""
    if not os.path.exists(path):
        return
    old = json.load(open(path, encoding='utf-8-sig'))['save']['regions']
    dl, ed = d['save']['regions']['dialog'], d['save']['regions']['editorData']
    if 'TimelineId' in old['dialog']:
        dl['TimelineId'] = old['dialog']['TimelineId']
    if 'ignoreInvalidFlagCombinations' in old.get('editorData', {}):
        ed['ignoreInvalidFlagCombinations'] = old['editorData']['ignoreInvalidFlagCombinations']
    old_nodes = {n['UUID']['value']: n for n in old['dialog']['nodes'][0]['node']}
    for n in dl['nodes'][0]['node']:
        o = old_nodes.get(n['UUID']['value'], {})
        # Node groups (GroupID/GroupIndex) are not kept: the timeline generator puts a grouped
        # narrator line and the next line in one phase, and the game then moves on by itself
        # without a "Continue" (seen on GR_Office_Evening N9a -> N9a2)
        for k in ('ValidatedFlags',):
            if k in o:
                n[k] = o[k]
    if 'TimelineId' in dl:
        print('kept       timeline link', dl['TimelineId']['value'])


def nested_node(uuid, nid, target_resource, position):
    """A "Nested Dialog" node, copied from the game's (SHA_NightsongPrison_CINE_EnterWater N26).
    NestedDialogNodeUUID is the target's DialogBank resource id; speakers keep their index."""
    s = lambda v: {'type': 'LSString', 'value': v}
    data = [('ID', nid), ('TemplateNodeUUID', '00000000-0000-0000-0000-000000000000'), ('TemplateVersion', '0'),
            ('collapsed', 'False'), ('logicalname', nid), ('position', position), ('sourcetemplate', '')]
    link = lambda i: {'Key': {'type': 'int32', 'value': i}, 'Value': {'type': 'int32', 'value': i}}
    return {'NestedDialogNodeUUID': {'type': 'guid', 'value': target_resource},
            'SpeakerLinking': [{'SpeakerLinkingEntry': [link(NPC), link(PLAYER)]}],
            'Tags': [{}], 'UUID': fs(uuid), 'checkflags': [{}], 'children': [{}],
            'constructor': fs('Nested Dialog'),
            'editorData': [{'data': [{'key': fs(k), 'val': s(v)} for k, v in data]}],
            'endnode': b(True), 'setflags': [{}]}


def build(scene):
    tpl = json.load(open(TEMPLATE, encoding='utf-8'))
    tpl_node = tpl['save']['regions']['dialog']['nodes'][0]['node'][1]
    h = section_handles(scene)
    ids = {nid: stable_uuid(f"{scene['name']}/node/{nid}") for nid in scene['nodes']}

    # simple layout: column = depth from the root, row = order of appearance
    roots = scene['root'] if isinstance(scene['root'], list) else [scene['root']]
    depth, order = {r: 0 for r in roots}, list(roots)
    for nid in order:
        for c in scene['nodes'][nid]['next']:
            if c not in depth:
                depth[c] = depth[nid] + 1; order.append(c)
    rows = {}
    nodes = []
    for i, nid in enumerate(order, 1):
        spec = scene['nodes'][nid]
        row = rows.get(depth[nid], 0); rows[depth[nid]] = row + 1
        if spec['kind'] == 'nested':
            nodes.append(nested_node(ids[nid], nid, stable_uuid(f"{spec['target']}/resource"),
                                     f"{-600 + 380 * depth[nid]};{-420 + 260 * row}"))
            continue
        n = copy.deepcopy(tpl_node)
        is_choice = spec['kind'] == 'choice'
        n['constructor'] = fs('TagQuestion' if is_choice else ('TagGreeting' if spec.get('root') else 'TagAnswer'))
        n['UUID'] = fs(ids[nid])
        if spec.get('group'):   # (first node of the group, index): GroupID is the first node's UUID
            n['GroupID'] = fs(ids[spec['group'][0]])
            n['GroupIndex'] = {'type': 'int32', 'value': spec['group'][1]}
        n['speaker'] = {'type': 'int32', 'value': PLAYER if is_choice else (NARRATOR if spec['who'] == 'narrator' else NPC)}
        n['TaggedTexts'] = [{'TaggedText': texts(h, scene, nid)}]
        n['checkflags'] = flags(spec.get('check'), spec['only'])
        n['setflags'] = flags(spec.get('set'))
        n['children'] = [{'child': [{'UUID': fs(ids[c])} for c in spec['next']]}] if spec['next'] else [{}]
        if spec.get('root'):
            n['Root'] = b(True)
        if not spec['next']:
            n['endnode'] = b(True)
        for e in n['editorData'][0]['data']:
            k = e['key']['value']
            if k == 'ID': e['val']['value'] = nid           # the script's line id, shown in the editor
            if k == 'logicalname': e['val']['value'] = nid
            if k == 'position': e['val']['value'] = f"{-600 + 380 * depth[nid]};{-420 + 260 * row}"
        nodes.append(n)

    d = copy.deepcopy(tpl)
    dl = d['save']['regions']['dialog']
    ed = d['save']['regions']['editorData']
    dl['UUID'] = fs(stable_uuid(f"{scene['name']}/dialog"))
    dl['nodes'] = [{'RootNodes': [{'RootNodes': fs(ids[r])} for r in roots], 'node': nodes}]
    dl['speakerlist'] = [{'speaker': [
        {'SpeakerMappingId': {'type': 'guid', 'value': stable_uuid(f"{scene['name']}/speaker/0")},
         'index': fs('0'), 'list': {'type': 'LSString', 'value': GORTASH}},
        {'SpeakerMappingId': {'type': 'guid', 'value': stable_uuid(f"{scene['name']}/speaker/1")},
         'index': fs('1'), 'list': {'type': 'LSString', 'value': PLAYERS}}]}]
    ed['synopsis'] = {'type': 'LSString', 'value': scene['synopsis']}
    ed['HowToTrigger'] = {'type': 'LSString', 'value': scene['trigger']}
    ed['nextNodeId'] = {'type': 'uint32', 'value': len(nodes)}
    ed['bronzeNodesCount'] = {'type': 'int32', 'value': len(nodes)}
    ed['defaultPath'] = [{'defaultPathNode': [{'UUID': {'type': 'LSString', 'value': ids[roots[0]]}}]}]

    os.makedirs(DIALOGS_DIR, exist_ok=True)
    path = os.path.join(DIALOGS_DIR, scene['name'] + '.lsj')
    keep_editor_data(path, d)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=3, ensure_ascii=False)
    print('dialog    ', path, f'({len(nodes)} nodes)')

    # Register the dialog as a resource, as the editor does on save
    res = stable_uuid(f"{scene['name']}/resource")
    r = Node('Resource')
    r.attrs = [('ID', 22, res),
               ('SourceFile', 23, f"Mods/{MOD}/Story/Dialogs/{scene['name']}.lsj"),
               ('Name', 23, scene['name']),
               ('automated', 19, False), ('isWorld', 19, False), ('isBehaviour', 19, False),
               ('EnableTimeline', 19, True), ('BlockFTB', 19, True), ('AllowDeadSpeakers', 19, bool(scene.get('dead_ok'))),
               ('IsAllowingJoinCombat', 19, False), ('isSubbedDialog', 19, False), ('isPrivateDialog', 19, False)]
    bank = Node('DialogBank'); bank.children = [r]
    os.makedirs(BANK_DIR, exist_ok=True)
    lsf.write({'version': 7, 'engine': ENGINE, 'regions': [bank]}, os.path.join(BANK_DIR, res + '.lsf'))
    print('resource  ', f"{scene['name']} -> {res}")
    missing = [nid for nid in scene['nodes'] if nid not in depth]
    if missing:
        print('WARNING unreachable nodes:', missing)


if __name__ == '__main__':
    # --out DIR: write into DIR (Mods/... and Public/... below it) instead of the Toolkit project
    # --only A,B: only these dialogs (by name), so dialogs already saved in the editor are left alone
    scenes = _scenes()
    if '--only' in sys.argv:
        names = sys.argv[sys.argv.index('--only') + 1].split(',')
        scenes = [s for s in scenes if s['name'] in names]
        assert len(scenes) == len(names), 'unknown dialog name'
    if '--out' in sys.argv:
        out = sys.argv[sys.argv.index('--out') + 1]
        DIALOGS_DIR = os.path.join(out, 'Mods', MOD, 'Story', 'Dialogs')
        BANK_DIR = os.path.join(out, 'Public', MOD, 'Content', 'Assets', '[PAK]_Dialogs')
    for s in scenes:
        build(s)
