"""Write Toolkit files (books, item root templates, flags) directly into the mod project.

Run with the Toolkit closed, then reopen it:
    python tools/build_toolkit.py              # writes everything
    python tools/build_toolkit.py --osiris     # also fills the matching placeholders in GR_Letters.txt

What it writes:
- Mods/<mod>/Localization/GortashRomance_Books.lsf: every book (BookId -> text handle
  taken from Localization/handles.md).
- Public/<mod>/RootTemplates/<uuid>.lsf: every item in ITEMS. The invitation letter you made
  in the Toolkit only gets its BookId changed (original kept in Toolkit/backup/).
- Public/<mod>/Flags/<uuid>.lsf: the main romance flags (FLAGS).

Re-running is safe: UUIDs are fixed (derived from the name), files are overwritten.
"""
import os, re, shutil, sys
import uuid as uuid_mod
sys.path.insert(0, os.path.dirname(__file__))
import lsf
from lsf import Node

MOD = 'GortashRomance_396ac9d9-d308-d392-0352-cf028922347d'
DATA = r'C:\Program Files (x86)\Steam\steamapps\common\Baldurs Gate 3\Data'
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(DATA, 'Public', MOD, 'RootTemplates')
LOCA_DIR = os.path.join(DATA, 'Mods', MOD, 'Localization')
FLAGS_DIR = os.path.join(DATA, 'Public', MOD, 'Flags')
OSIRIS = os.path.join(REPO, 'Story', 'RawFiles', 'Goals', 'GR_Letters.txt')
NAMESPACE = uuid_mod.UUID('396ac9d9-d308-d392-0352-cf028922347d')


def stable_uuid(name):
    return str(uuid_mod.uuid5(NAMESPACE, name))


# Object created by hand in the Toolkit (name, description and visuals live there).
LETTER1_BASE = '04f0d615-092d-418a-95a4-358a2e3ea0c1'

# Game templates used as parents (from Shared.pak, Public/Shared/RootTemplates/_merged.lsf)
PAPER_LETTER = '4d69834f-af2a-4197-9454-789049667b23'   # BOOK_GEN_Paper_Letter_C
PAPER_CARD = 'e027e262-3707-43c9-b023-d80778956f71'     # BOOK_Letter_A
WINE = '870caf9b-f767-4264-9d0a-2c3a88dc0565'           # CONS_Drink_Wine_B (drinkable)
KEY = '7f414907-9faf-4330-9741-9444e1df158d'            # BASE_KEY
DAGGER = '569b0f3d-abcd-4b01-aaf0-979091288163'         # WPN_HUM_Dagger_A_0 (plain dagger)

# Items. Fields:
#   name, uuid (None = derived from name), parent, name id, description id,
#   book text (line id, variant) or None, Osiris placeholder or None
ITEMS = [
    # Step 1 - invitation letter, one per player identity (base object made in the Toolkit)
    ('GR_Letter_Invitation',    LETTER1_BASE, None, None, None, ('LETTER1_TEXT', 'M'), None),
    ('GR_Letter_Invitation_F',  '6c1d0f3e-5b7a-4e21-9a44-1f0b7d2c8e51', LETTER1_BASE, None, None, ('LETTER1_TEXT', 'F'), None),
    ('GR_Letter_Invitation_NB', 'b2e4a9d7-3c58-4f06-8d1a-7e9c25f4a063', LETTER1_BASE, None, None, ('LETTER1_TEXT', 'NB'), None),
    # Step 3 - ball invitation
    ('GR_Card_Ball',            None, PAPER_LETTER, 'CARD_NAME', 'CARD_DESC', ('CARD_TEXT', 'all'), 'CARD_TEMPLATE'),
    # Step 4 - second letter (no crest, no wax: plain paper)
    ('GR_Letter_Night',         None, PAPER_LETTER, 'LETTER2_NAME', 'LETTER2_DESC', ('LETTER2_TEXT', 'all'), 'LETTER2_TEMPLATE'),
    # Step 5 - epilogue letters (black wax: same look as the invitation)
    ('GR_Letter_Epilogue',      None, LETTER1_BASE, 'EPILOGUE_NAME', 'EPILOGUE_DESC', ('EPILOGUE_TEXT', 'all'), 'EPILOGUE_TEMPLATE'),
    ('GR_Letter_Epilogue_Away', None, LETTER1_BASE, 'EPILOGUE_NAME', 'EPILOGUE_DESC', ('EPILOGUE_AWAY_TEXT', 'all'), 'EPILOGUE_AWAY_TEMPLATE'),
    # Breakup letters (black wax, unstamped)
    ('GR_Letter_Breakup1',      None, LETTER1_BASE, 'BREAKUP_NAME', 'BREAKUP_DESC', ('BREAKUP1_TEXT', 'all'), 'BREAKUP1_TEMPLATE'),
    ('GR_Letter_Breakup2',      None, LETTER1_BASE, 'BREAKUP_NAME', 'BREAKUP_DESC', ('BREAKUP2_TEXT', 'all'), 'BREAKUP2_TEMPLATE'),
    # Gifts: the note is in the description
    ('GR_Gift_Wine',            None, WINE, 'GIFT1_NAME', 'GIFT1_DESC', None, 'GIFT1_TEMPLATE'),
    # Paper items open a book; without one they would show "unreadable", so it shows the note
    ('GR_Gift_DanceCard',       None, PAPER_CARD, 'GIFT2_NAME', 'GIFT2_DESC', ('GIFT2_DESC', 'all'), 'GIFT2_TEMPLATE'),
    ('GR_Gift_Key',             None, KEY, 'GIFT3_NAME', 'GIFT3_DESC', None, 'GIFT3_TEMPLATE'),
    ('GR_Gift_Knife',           None, DAGGER, 'GIFT4_NAME', 'GIFT4_DESC', None, 'GIFT4_TEMPLATE'),
]

# Main romance flags (README, "Flags").
FLAGS = [
    ('GR_Letter1_Delivered',  'First letter delivered'),
    ('GR_Office_Visited',     'Office scene played'),
    ('GR_Romance_Interested', 'Romance open after the office'),
    ('GR_Romance_Declined',   'Player refused in the office'),
    ('GR_Ball_Invited',       'Ball invitation delivered'),
    ('GR_Ball_Attended',      'Player attended the ball'),
    ('GR_Ball_Danced',        'Player danced with Gortash at the ball'),
    ('GR_Night_Invited',      'Second letter delivered'),
    ('GR_Romance_Committed',  'Romance established after the private night'),
    ('GR_Romance_Ended',      'Romance over for good'),
    ('GR_Gortash_Saved',      'Gortash survived the brain'),
    ('GR_First_Names',        'They say "tu" in French (set during the private night)'),
    ('GR_Left_City',          'The player left Baldur\'s Gate at the end'),
    # Extension: Dark Urge memories (Dialogs/GR_Memories.md)
    ('GR_Memory1_Seen',       'Dark Urge memory 1 (first meeting) played'),
    ('GR_Memory2_Seen',       'Dark Urge memory 2 (the rooftop) played'),
    ('GR_Memory3_Seen',       'Dark Urge memory 3 (the last morning) played'),
    # Extension: after Orin (Dialogs/GR_Orin.md)
    ('GR_Orin_Done',          "Scene after Orin's death played"),
]
# Same value as the game's own romance state flags set on the player
# (e.g. ORI_Astarion_State_HadAct2RomanceNight): usable on a character and in dialogues.
FLAG_USAGE = 5

ENGINE = (4 << 55) | (8 << 47) | (0 << 31) | 500   # 4.8.0.500, same as the Toolkit's own files
FS, LSS, I32, BOOL, TS, GUID, U8 = 22, 23, 4, 19, 28, 31, 1


def flag_uuid(name):
    return stable_uuid(name)


def item_uuid(item):
    return item[1] or stable_uuid(item[0])


def book_id(item):
    name, _, _, _, _, text, _ = item
    if name == 'GR_Letter_Invitation':
        return 'GR_Letter_Invitation_M'
    return name


def handles():
    """{(id, variant): handle} from Localization/handles.md"""
    out = {}
    for line in open(os.path.join(REPO, 'Localization', 'handles.md'), encoding='utf-8'):
        m = re.match(r'\| (\S+) \| [^|]+ \| (\w+) \| `(h[0-9a-g]+)` \|', line)
        if m:
            out[(m.group(1), m.group(2))] = m.group(3)
    return out


def book_action(bid):
    attrs = Node('Attributes')
    attrs.attrs = [('Animation', FS, ''), ('Conditions', LSS, ''), ('BookId', FS, bid)]
    action = Node('Action')
    action.attrs = [('ActionType', I32, 11)]   # 11 = Book
    action.children = [attrs]
    peace = Node('OnUsePeaceActions')
    peace.children = [action]
    return peace


def build_books(h):
    root = Node('TranslatedStringKeys')
    for item in ITEMS:
        if item[5] is None:
            continue
        k = Node('TranslatedStringKey')
        k.attrs = [('Content', TS, {'handle': h[item[5]], 'version': 1}),
                   ('UUID', FS, book_id(item)), ('Speaker', FS, ''), ('ExtraData', LSS, ''), ('Stub', BOOL, True)]
        root.children.append(k)
    path = os.path.join(LOCA_DIR, 'GortashRomance_Books.lsf')
    lsf.write({'version': 7, 'engine': ENGINE, 'regions': [root]}, path)
    print('books     ', len(root.children), path)


def set_book(doc, bid):
    go = doc['regions'][0].child('GameObjects')
    peace = go.child('OnUsePeaceActions')
    if peace is None:
        go.children.append(book_action(bid))
        return
    for action in peace.children:
        if action.attr('ActionType') == 11:
            a = action.child('Attributes')
            a.attrs = [x for x in a.attrs if x[0] != 'BookId'] + [('BookId', FS, bid)]
            return
    peace.children.append(book_action(bid).children[0])


def build_templates(h):
    base_path = os.path.join(TEMPLATES, LETTER1_BASE + '.lsf')
    backup = os.path.join(REPO, 'Toolkit', 'backup', LETTER1_BASE + '.lsf')
    if not os.path.exists(backup):
        os.makedirs(os.path.dirname(backup), exist_ok=True)
        shutil.copy2(base_path, backup)
    for item in ITEMS:
        name, _, parent, name_id, desc_id, text, _ = item
        u = item_uuid(item)
        path = os.path.join(TEMPLATES, u + '.lsf')
        if u == LETTER1_BASE:
            doc = lsf.read(base_path)
            set_book(doc, book_id(item))
        else:
            go = Node('GameObjects')
            go.attrs = [('MapKey', FS, u), ('Name', LSS, name), ('LevelName', FS, ''),
                        ('Type', FS, 'item'), ('ParentTemplateId', FS, parent)]
            if name_id:
                go.attrs.append(('DisplayName', TS, {'handle': h[(name_id, 'all')], 'version': 1}))
            if desc_id:
                go.attrs.append(('Description', TS, {'handle': h[(desc_id, 'all')], 'version': 1}))
            if text:
                go.children = [book_action(book_id(item))]
            root = Node('Templates'); root.children = [go]
            doc = {'version': 7, 'engine': ENGINE, 'regions': [root]}
        lsf.write(doc, path)
        print('template  ', f'{name}_{u}')


def build_flags():
    os.makedirs(FLAGS_DIR, exist_ok=True)
    for name, desc in FLAGS:
        u = flag_uuid(name)
        root = Node('Flags')
        root.attrs = [('UUID', GUID, u), ('Name', FS, name), ('Description', LSS, desc), ('Usage', U8, FLAG_USAGE)]
        lsf.write({'version': 7, 'engine': ENGINE, 'regions': [root]}, os.path.join(FLAGS_DIR, u + '.lsf'))
        print('flag      ', f'{name}_{u}')


def fill_osiris():
    s = open(OSIRIS, encoding='utf-8').read()
    n = 0
    for name, _ in FLAGS:
        s, k = re.subn(re.escape(f'<{name}>'), f'{name}_{flag_uuid(name)}', s); n += k
    for item in ITEMS:
        if item[6]:
            s, k = re.subn(re.escape(f'(ITEMROOT)<{item[6]}>'), f'(ITEMROOT){item[0]}_{item_uuid(item)}', s); n += k
    open(OSIRIS, 'w', encoding='utf-8').write(s)
    print('osiris     placeholders filled:', n)


if __name__ == '__main__':
    h = handles()
    build_books(h)
    build_templates(h)
    build_flags()
    if '--osiris' in sys.argv:
        fill_osiris()
    # Story scripts: the repo is the source, the Toolkit reads them from the mod folder
    goals = os.path.join(DATA, 'Mods', MOD, 'Story', 'RawFiles', 'Goals')
    os.makedirs(goals, exist_ok=True)
    src = os.path.dirname(OSIRIS)
    for f in sorted(os.listdir(src)):
        if f.endswith('.txt'):
            shutil.copy2(os.path.join(src, f), goals)
            print('story     ', os.path.join(goals, f))
