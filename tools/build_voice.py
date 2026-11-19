"""Give Gortash's lines a moving mouth, without a voice.

    python tools/build_voice.py

The game only plays a line's lip animation alongside its voice file. So each Gortash line in the
built dialogs gets, in Data/Mods/<mod>/Localization/English/:
- Soundbanks/vb878a854..._<handle>.wem: a silent sound (16-bit PCM in a Wwise RIFF; the game's own
  voices are Vorbis, but this is played: tested in game 2026-11-17 on GR_Office_Evening N3a)
- Soundbanks/b878a854....lsf: the voice meta (sound file, length) for all those lines
- Animation/FX_vb878a854..._<handle>.ffxanim: the lip animation of a real Gortash line of about
  the same length, borrowed from English_Animations.pak (so the lips do not match our words)
- Animation/FaceFXActors/<Gortash uuid>.ffxactor/.ffxbones: needed for the game to find the lips
Run with the Toolkit closed, then tools/build_pack.py.
"""
import copy, os, re, struct, sys, zlib
import xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(__file__))
import lsf
from build_toolkit import DATA, MOD, REPO

LOC = os.path.join(DATA, 'Localization')
GORTASH = 'b878a854-f790-4999-95c4-3f20f00f65ac'
SPK = 'v' + GORTASH.replace('-', '')
DIALOGS = ['GR_Office_Evening', 'GR_Ball', 'GR_Private_Night', 'GR_Memories', 'GR_Orin']
OUT = os.path.join(DATA, 'Mods', MOD, 'Localization', 'English')
GUSTAV = 'Mods/Gustav/Localization/English/'
RATE = 44100


def lz4(src, size):
    dst = bytearray(); i = 0
    while i < len(src):
        t = src[i]; i += 1; l = t >> 4
        if l == 15:
            while True:
                b = src[i]; i += 1; l += b
                if b != 255: break
        dst += src[i:i + l]; i += l
        if i >= len(src): break
        off = src[i] | (src[i + 1] << 8); i += 2; m = t & 15
        if m == 15:
            while True:
                b = src[i]; i += 1; m += b
                if b != 255: break
        m += 4; s = len(dst) - off
        for k in range(m): dst.append(dst[s + k])
    return bytes(dst)


class Pak:
    def __init__(self, path):
        self.f = open(path, 'rb')
        _, _, off, _ = struct.unpack_from('<4sIQI', self.f.read(40))
        self.f.seek(off); n, cs = struct.unpack('<II', self.f.read(8))
        data = lz4(self.f.read(cs), n * 272)
        self.idx = {}
        for k in range(n):
            e = data[k * 272:(k + 1) * 272]
            self.idx[e[:256].split(b'\0')[0].decode()] = e

    def read(self, name):
        e = self.idx[name]
        o1, o2, _, flags, sd, us = struct.unpack_from('<IHBBII', e, 256)
        self.f.seek(o1 | (o2 << 32)); raw = self.f.read(sd); m = flags & 0xf
        return raw if m == 0 else zlib.decompress(raw) if m == 1 else lz4(raw, us)


def silent_wem(seconds):
    data = b'\0' * (2 * int(seconds * RATE))
    # Wwise PCM header: WAVE_FORMAT_EXTENSIBLE, mono, channel config 0x4101 (as in the game's voices)
    fmt = struct.pack('<HHIIHHHHI', 0xFFFE, 1, RATE, RATE * 2, 2, 16, 6, 16, 0x4101)
    body = b'WAVE' + b'fmt ' + struct.pack('<I', len(fmt)) + fmt + b'data' + struct.pack('<I', len(data)) + data
    return b'RIFF' + struct.pack('<I', len(body)) + body


def our_lines():
    """(handle, English text) of every Gortash line in the built dialogs."""
    text = {c.get('contentuid'): c.text or '' for c in
            ET.parse(os.path.join(REPO, 'Localization', 'English', 'GortashRomance.loca.xml')).getroot().iter('content')}
    out, section = [], None
    for l in open(os.path.join(REPO, 'Localization', 'handles.md'), encoding='utf-8'):
        if l.startswith('## '):
            section = l[3:].strip()
        m = re.match(r'\| [^|]+ \| Gortash \| [^|]+ \| `(h\w+)` \|', l)
        if m and section in DIALOGS:
            out.append((m.group(1), text[m.group(1)]))
    return out


def main():
    meta_pak = Pak(os.path.join(LOC, 'VoiceMeta.pak'))
    anim_pak = Pak(os.path.join(LOC, 'English_Animations.pak'))
    tmp = os.path.join(REPO, 'build', '_gortash_meta.lsf')   # lsf.read takes a path
    os.makedirs(os.path.dirname(tmp), exist_ok=True)
    open(tmp, 'wb').write(meta_pak.read(GUSTAV + f'Soundbanks/{GORTASH.replace("-", "")}.lsf'))
    meta = lsf.read(tmp); os.remove(tmp)

    def find(n):
        if n.name == 'MapValue' and any(c.name == 'VoiceTextMetaData' for c in n.children): return n
        for c in n.children:
            r = find(c)
            if r: return r
    mv = find(meta['regions'][0])
    # donors: Gortash story lines that have a lip animation, by length
    donors = []
    for n in mv.children:
        v = n.children[0]
        h = n.attr('MapKey')
        if v.attr('Priority') == 'P1_StoryDialog' and GUSTAV + f'Animation/FX_{SPK}_{h}.ffxanim' in anim_pak.idx:
            donors.append((v.attr('Length'), h, n))
    donors.sort(key=lambda d: d[0])

    for d in ('Soundbanks', 'Animation'):
        p = os.path.join(OUT, d)
        for f in (os.listdir(p) if os.path.isdir(p) else []):
            if f.startswith(('FX_' + SPK, SPK)):
                os.remove(os.path.join(p, f))
    os.makedirs(os.path.join(OUT, 'Soundbanks'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'Animation', 'FaceFXActors'), exist_ok=True)
    for ext in ('ffxactor', 'ffxbones'):
        open(os.path.join(OUT, 'Animation', 'FaceFXActors', f'{GORTASH}.{ext}'), 'wb').write(
            anim_pak.read(GUSTAV + f'Animation/FaceFXActors/{GORTASH}.{ext}'))

    used, entries = {}, []
    for handle, text in our_lines():
        want = len(text.split()) / 2.6 + 0.6     # roughly how long he would take to say it
        fresh = [d for d in donors if d[1] not in used.values()] or donors
        length, dh, dn = min(fresh, key=lambda d: abs(d[0] - want))
        used[handle] = dh
        e = copy.deepcopy(dn)
        e.attrs = [(a, t, handle if a == 'MapKey' else v) for a, t, v in e.attrs]
        v = e.children[0]
        v.attrs = [(a, t, f'{SPK}_{handle}.wem' if a == 'Source' else x) for a, t, x in v.attrs]
        entries.append(e)
        open(os.path.join(OUT, 'Soundbanks', f'{SPK}_{handle}.wem'), 'wb').write(silent_wem(length))
        open(os.path.join(OUT, 'Animation', f'FX_{SPK}_{handle}.ffxanim'), 'wb').write(
            anim_pak.read(GUSTAV + f'Animation/FX_{SPK}_{dh}.ffxanim'))
        print(f'{handle}  {want:5.1f}s -> {length:5.1f}s  {text[:50]}')
    mv.children = entries
    lsf.write(meta, os.path.join(OUT, 'Soundbanks', f'{GORTASH.replace("-", "")}.lsf'))
    print(len(entries), 'lines')


if __name__ == '__main__':
    main()
