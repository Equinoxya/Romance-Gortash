"""Prepare a folder ready to pack into a .pak (with the BG3 Modders Multitool).

    python tools/build_pack.py

Copies the Toolkit project (Data/Mods/<mod> and Data/Public/<mod>) into build/GortashRomance/,
and turns every language's .xml text files into one binary GortashRomance.loca, which is what
the game reads, placed in Localization/<Language>/ at the root of the pack. Story goals are shipped as raw .txt; the game compiles them at load.
"""
import os, shutil, struct, sys
import xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(__file__))
from build_toolkit import DATA, MOD, REPO, stable_uuid

OUT = os.path.join(REPO, 'build', 'GortashRomance')
KEEP_LOOPING = {stable_uuid('GR/anim/GR_HandOffer_LOOP'),
                '7bd8e368-5ad3-487b-ab93-f868d968590f',   # HUM_M_Rig_DFLT_CINE_Walk_01
                '5470292e-5bb1-4470-a317-950b96e27d32',   # CINE_Read_Map_01 (Gortash at his desk, arrival)
                stable_uuid('GR/anim/GR_WaltzLoop_Gortash'), stable_uuid('GR/anim/GR_WaltzLoop_Joueuse')}   # ball dance


def write_loca(entries, path):
    """entries: list of (handle, version, text). Binary LOCA format read by the game."""
    head = struct.pack('<4sII', b'LOCA', len(entries), 12 + 70 * len(entries))
    table, texts = bytearray(), bytearray()
    for handle, version, text in entries:
        t = text.encode('utf-8') + b'\0'
        table += handle.encode('ascii').ljust(64, b'\0') + struct.pack('<HI', version, len(t))
        texts += t
    open(path, 'wb').write(head + table + texts)


def read_xml(path):
    out = []
    for c in ET.parse(path).getroot().iter('content'):
        out.append((c.get('contentuid'), int(c.get('version') or 1), c.text or ''))
    return out


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    for part in ('Mods', 'Public'):
        shutil.copytree(os.path.join(DATA, part, MOD), os.path.join(OUT, part, MOD),
                        ignore=shutil.ignore_patterns('*.xml'))
    # The Toolkit also writes editor-only data here; the game does not need it
    shutil.rmtree(os.path.join(OUT, 'Mods', MOD, 'Scripts'), ignore_errors=True)
    # Editor autosaves and the throwaway test dialog (GR_Test) are not part of the mod
    for d in ('Dialogs', 'DialogsBinary'):
        p = os.path.join(OUT, 'Mods', MOD, 'Story', d)
        shutil.rmtree(os.path.join(p, 'Autosave'), ignore_errors=True)
        for f in (os.listdir(p) if os.path.isdir(p) else []):
            if f.startswith('GR_Test'):
                os.remove(os.path.join(p, f))
    bank = os.path.join(OUT, 'Public', MOD, 'Content', 'Assets', '[PAK]_Dialogs')
    if os.path.isdir(bank):
        import lsf
        for f in os.listdir(bank):
            res = lsf.read(os.path.join(bank, f))['regions'][0].children[0]
            name = res.attr('Name')
            # keep only the resource id that build_dialogs.py writes (and GR_Letters.txt uses);
            # the editor adds its own entry when it saves a dialog it did not know yet
            if name.startswith('GR_Test') or res.attr('ID') != stable_uuid(f'{name}/resource'):
                os.remove(os.path.join(bank, f))
                print('skipped    dialog resource', name, res.attr('ID'))
    # A timeline generated in the editor points at the editor's own resource for its dialog,
    # which was just removed: point it at the resource kept above instead
    tl_bank = os.path.join(OUT, 'Public', MOD, 'Content', 'Generated', '[PAK]_GeneratedDialogTimelines')
    if os.path.isdir(tl_bank):
        import lsf
        for f in os.listdir(tl_bank):
            p = os.path.join(tl_bank, f)
            doc = lsf.read(p)
            res = doc['regions'][0].children[0]
            want = stable_uuid(f"{res.attr('Name')}/resource")
            res.attrs = [(n, t, want if n == 'DialogResourceId' else v) for n, t, v in res.attrs]
            lsf.write(doc, p)
            print('timeline  ', res.attr('Name'), '->', want)
    # Animations added in the Timeline Editor default to "Continuous", which makes a gesture loop
    # until the line ends. None of Larian's office gestures use it: drop it from the packed timelines.
    import lsf
    tl_dir = os.path.join(OUT, 'Public', MOD, 'Timeline', 'Generated')
    for f in (os.listdir(tl_dir) if os.path.isdir(tl_dir) else []):
        if f.endswith('.lsf') and not f.endswith('_Scene.lsf'):
            p = os.path.join(tl_dir, f)
            doc, n = lsf.read(p), [0]
            def walk(node):
                # except the animations meant to repeat: our hand-offer loop (held until the player
                # chooses) and the walk cycle of the arrival cinematic (tools/anim/arrival_walk.py)
                if node.name == 'EffectComponent' and node.attr('Type') == 'TLAnimation'                         and node.attr('AnimationSourceId') not in KEEP_LOOPING:
                    kept = [a for a in node.attrs if a[0] != 'Continuous']
                    n[0] += len(node.attrs) - len(kept); node.attrs = kept
                for c in node.children: walk(c)
            for r in doc['regions']: walk(r)
            if n[0]:
                lsf.write(doc, p)
                print('no loop   ', f, n[0], 'animations')
    # The game ships every timeline scene as both _Scene.lsx and _Scene.lsf; the Toolkit only
    # wrote the .lsx, and a timeline without its .lsf crashed the game. Write the .lsf from it.
    import lsf
    for root, _, files in os.walk(OUT):
        for f in files:
            if f.endswith('_Scene.lsx'):
                p = os.path.join(root, f)
                lsf.write(lsf.from_xml(p), p[:-4] + '.lsf')
                print('scene     ', f[:-4] + '.lsf')
    # The Toolkit writes vectors in .lsx as a child element (<float3 x= y= z=/>); the Multitool
    # (LSLib) only reads them as value="x y z" and rejects the file otherwise
    import re
    vec = re.compile(r'(<attribute id="[^"]+" type="[a-z]*vec\d")>\s*<\w+((?:\s+[xyzw]="[^"]*")+)\s*/>\s*</attribute>')
    for root, _, files in os.walk(OUT):
        for f in files:
            if f.endswith('.lsx'):
                p = os.path.join(root, f)
                s = open(p, encoding='utf-8').read()
                t, n = vec.subn(lambda m: m.group(1) + ' value="' + ' '.join(re.findall(r'="([^"]*)"', m.group(2))) + '"/>', s)
                if n:
                    open(p, 'w', encoding='utf-8').write(t)
                    print('vectors   ', f, n)
    story = os.path.join(OUT, 'Mods', MOD, 'Story')
    for f in os.listdir(story):   # compiled story and build logs: the game rebuilds from RawFiles
        if os.path.isfile(os.path.join(story, f)):
            os.remove(os.path.join(story, f))
    src_loca = os.path.join(DATA, 'Mods', MOD, 'Localization')
    # The text source is the repository (Localization/<Language>/GortashRomance.loca.xml, written
    # by build_loca.py). Copy it into the Toolkit project first: packing the Toolkit's own copy
    # shipped stale text (game 20/11: the old letter name and text after the rewrite).
    repo_loca = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Localization')
    for lang in sorted(os.listdir(repo_loca)):
        src = os.path.join(repo_loca, lang, 'GortashRomance.loca.xml')
        if os.path.isfile(src):
            os.makedirs(os.path.join(src_loca, lang), exist_ok=True)
            shutil.copyfile(src, os.path.join(src_loca, lang, 'GortashRomance.loca.xml'))
            print(f'loca       {lang}: text copied from the repository')
    for lang in sorted(os.listdir(src_loca)):
        d = os.path.join(src_loca, lang)
        if not os.path.isdir(d):
            continue
        entries, seen = [], set()
        for f in sorted(os.listdir(d)):
            if f.endswith('.xml'):
                for e in read_xml(os.path.join(d, f)):
                    if e[0] not in seen:
                        seen.add(e[0]); entries.append(e)
        # The game reads mod text from Localization/<Language>/ at the root of the .pak
        # (not under Mods/<mod>/, where the Toolkit keeps its .xml sources)
        dst = os.path.join(OUT, 'Localization', lang)
        os.makedirs(dst, exist_ok=True)
        write_loca(entries, os.path.join(dst, 'GortashRomance.loca'))
        print(f'loca       {lang}: {len(entries)} lines')
    for root, _, files in os.walk(OUT):
        for f in files:
            print('file      ', os.path.relpath(os.path.join(root, f), OUT))
    check_animation_durations()


# Our own animations: each .GR2 has a resource (Content/Assets/[PAK]_GR_Animations/<id>.lsf) whose
# Duration the game trusts, e.g. to loop it. Those resources are written by hand, so a re-export of
# a different length goes unnoticed (GR_HandOffer_LOOP went from 11.46 s to 4 s, 18/11).
DIVINE = r'C:\Users\obell\Desktop\Packed\Tools\Divine.exe'
CONFORM = r'C:\Users\obell\Desktop\GortashAnim\source\HUM_M_Base.GR2'   # skeleton, needed to read an animation


def gr2_duration(gr2, tmp):
    """Length in seconds of an animation .GR2: convert it to .glb with LSLib's Divine and take the
    largest key time of its animation tracks (glTF stores each track's time range as min/max)."""
    import json, subprocess
    glb = os.path.join(tmp, os.path.basename(gr2) + '.glb')
    subprocess.run([DIVINE, '-g', 'bg3', '-a', 'convert-model', '-s', gr2, '-d', glb,
                    '-e', 'conform', '--conform-path', CONFORM], capture_output=True, timeout=120)
    if not os.path.exists(glb):
        return None
    data = open(glb, 'rb').read()
    n = struct.unpack('<I', data[12:16])[0]          # first chunk of a .glb: the JSON
    doc = json.loads(data[20:20 + n])
    times = [doc['accessors'][s['input']]['max'][0] for a in doc.get('animations', []) for s in a['samplers']]
    return max(times) if times else None


def check_animation_durations():
    import glob, tempfile, lsf
    resources = glob.glob(os.path.join(OUT, 'Public', MOD, 'Content', 'Assets', '*', '*.lsf'))
    anims = []
    for p in resources:
        for region in lsf.read(p)['regions']:
            stack = [region]
            while stack:
                node = stack.pop(); stack += node.children
                src = node.attr('SourceFile') if node.name == 'Resource' else None
                if src and src.lower().endswith('.gr2') and node.attr('Duration') is not None:
                    if not src.startswith(f'Public/{MOD}/'):   # the game's own file (ball_waltz.py)
                        print(f'anim       {node.attr("Name")}: game file {src.rsplit("/", 1)[-1]}, not checked')
                        continue
                    anims.append((node.attr('Name'), node.attr('Duration'), os.path.join(OUT, *src.split('/'))))
    if not anims:
        return
    if not (os.path.exists(DIVINE) and os.path.exists(CONFORM)):
        print('WARNING    animation durations not checked: Divine.exe or HUM_M_Base.GR2 not found')
        return
    bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        for name, declared, gr2 in sorted(anims):
            real = gr2_duration(gr2, tmp) if os.path.exists(gr2) else None
            if real is None:
                print(f'WARNING    animation {name}: could not read {os.path.basename(gr2)}'); bad += 1
            elif abs(real - declared) > 1 / 24:      # more than one frame apart
                print(f'WARNING    animation {name}: the .GR2 lasts {real:.3f} s, its resource says {declared:.3f} s'
                      f' -> fix Duration in Content/Assets/[PAK]_GR_Animations'); bad += 1
            else:
                print(f'anim       {name}: {real:.3f} s, resource OK')
    if bad:
        print(f'WARNING    {bad} animation resource(s) to fix before packing (see above)')


if __name__ == '__main__':
    main()
