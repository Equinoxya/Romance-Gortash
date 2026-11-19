"""Minimal reader/writer for uncompressed BG3 LSF v7 files (LSOF), as saved by the Toolkit.

Usage:
  python tools/lsf.py dump FILE.lsf          -> prints the tree as LSX-like XML
  python tools/lsf.py tolsx FILE.lsf OUT.lsx
  python tools/lsf.py tolsf FILE.lsx OUT.lsf  (only the attribute types listed in TYPES)

Only handles files whose sections are stored uncompressed (CompressionFlags == 0),
which is what the BG3 Toolkit writes, and what the game's _merged files are once
extracted from their .pak. Writes the KeysAndAdjacency layout; reads both layouts.
"""
import struct, sys, uuid
import xml.etree.ElementTree as ET

TYPES = {1: 'uint8', 2: 'int16', 3: 'uint16', 4: 'int32', 5: 'uint32', 6: 'float', 7: 'double',
         11: 'fvec2', 12: 'fvec3', 13: 'fvec4', 19: 'bool', 20: 'string', 21: 'path', 22: 'FixedString',
         23: 'LSString', 24: 'uint64', 25: 'ScratchBuffer', 26: 'old_int64', 27: 'int8',
         28: 'TranslatedString', 29: 'WString', 30: 'LSWString', 31: 'guid', 32: 'int64',
         8: 'ivec2', 9: 'ivec3', 10: 'ivec4'}
TYPE_IDS = {v: k for k, v in TYPES.items()}
NUM = {1: '<B', 2: '<h', 3: '<H', 4: '<i', 5: '<I', 6: '<f', 7: '<d', 19: '<?', 24: '<Q', 26: '<q', 27: '<b', 32: '<q'}
VEC = {8: ('<i', 2), 9: ('<i', 3), 10: ('<i', 4), 11: ('<f', 2), 12: ('<f', 3), 13: ('<f', 4)}
STR = {20, 21, 22, 23, 29, 30}


class Node:
    def __init__(self, name):
        self.name = name
        self.attrs = []      # list of (name, type_id, value)
        self.children = []

    def attr(self, name):
        for n, t, v in self.attrs:
            if n == name:
                return v

    def child(self, name):
        for c in self.children:
            if c.name == name:
                return c


def _guid_from_lsf(b):
    # LSLib byte-swaps the last 8 bytes in pairs (ByteSwapGuids)
    b = bytearray(b)
    for i in range(8, 16, 2):
        b[i], b[i + 1] = b[i + 1], b[i]
    return str(uuid.UUID(bytes_le=bytes(b)))


def _guid_to_lsf(s):
    b = bytearray(uuid.UUID(s).bytes_le)
    for i in range(8, 16, 2):
        b[i], b[i + 1] = b[i + 1], b[i]
    return bytes(b)


def read(path):
    d = open(path, 'rb').read()
    assert d[:4] == b'LSOF', 'not an LSF file'
    version, engine = struct.unpack_from('<IQ', d, 4)
    meta = struct.unpack_from('<10IBBHI', d, 16)
    su, sd, ku, kd, nu, nd, au, ad, vu, vd, comp, _, _, fmt = meta
    assert version >= 6 and comp == 0 and sd == kd == nd == ad == vd == 0, 'compressed LSF not supported'
    pos = 64
    # section order on disk: names, nodes, attributes, values, then keys (empty in most files)
    sec = []
    for size in (su, nu, au, vu, ku):
        sec.append(d[pos:pos + size]); pos += size
    strings, nodes_b, attrs_b, values, keys = sec
    # names
    names = []
    p = 0
    (n_entries,) = struct.unpack_from('<I', strings, p); p += 4
    for _ in range(n_entries):
        (cnt,) = struct.unpack_from('<H', strings, p); p += 2
        chain = []
        for _ in range(cnt):
            (ln,) = struct.unpack_from('<H', strings, p); p += 2
            chain.append(strings[p:p + ln].decode('utf-8')); p += ln
        names.append(chain)
    name = lambda ref: names[ref >> 16][ref & 0xffff]
    if fmt != 1:
        return _read_v2(version, engine, name, nodes_b, attrs_b, values)
    # attributes
    raw_attrs = [struct.unpack_from('<IIiI', attrs_b, i) for i in range(0, len(attrs_b), 16)]
    def value(t, off, ln):
        return _value(values, t, off, ln)
    # nodes
    raw_nodes = [struct.unpack_from('<IiiI', nodes_b, i) for i in range(0, len(nodes_b), 16)]
    objs = [Node(name(n[0])) for n in raw_nodes]
    regions = []
    for i, (nref, parent, nxt, first) in enumerate(raw_nodes):
        o = objs[i]
        a = first if first != 0xffffffff else -1
        while a != -1:
            aref, tl, anext, off = raw_attrs[a]
            t, ln = tl & 0x3f, tl >> 6
            o.attrs.append((name(aref), t, value(t, off, ln)))
            a = anext
        if parent == -1:
            regions.append(o)
        else:
            objs[parent].children.append(o)
    return {'version': version, 'engine': engine, 'regions': regions}


def _value(values, t, off, ln):
    b = values[off:off + ln]
    if t in NUM: return struct.unpack(NUM[t], b)[0]
    if t in VEC:
        f, n = VEC[t]; return list(struct.unpack('<' + f[1] * n, b))
    if t in STR: return b.rstrip(b'\0').decode('utf-8', 'replace')
    if t == 31: return _guid_from_lsf(b)
    if t == 28:
        ver, hl = struct.unpack_from('<Hi', b, 0)
        return {'version': ver, 'handle': b[6:6 + hl].rstrip(b'\0').decode()}
    return b.hex()


def _read_v2(version, engine, name, nodes_b, attrs_b, values):
    """Older layout (game _merged files): 12-byte nodes and attributes, values in order."""
    raw_nodes = [struct.unpack_from('<Iii', nodes_b, i) for i in range(0, len(nodes_b), 12)]
    objs = [Node(name(n[0])) for n in raw_nodes]
    off = 0
    for i in range(0, len(attrs_b), 12):
        aref, tl, node = struct.unpack_from('<IIi', attrs_b, i)
        t, ln = tl & 0x3f, tl >> 6
        objs[node].attrs.append((name(aref), t, _value(values, t, off, ln)))
        off += ln
    regions = []
    for i, (nref, first, parent) in enumerate(raw_nodes):
        (regions if parent == -1 else objs[parent].children).append(objs[i])
    return {'version': version, 'engine': engine, 'regions': regions}


def write(doc, path):
    buckets = [[] for _ in range(0x200)]
    index = {}
    def ref(s):
        if s not in index:
            h = 0
            for c in s.encode('utf-8'):
                h = (h * 31 + c) & 0xffffffff
            bk = (h & 0x1ff) ^ ((h >> 9) & 0x1ff) ^ ((h >> 18) & 0x1ff) ^ ((h >> 27) & 0x1ff)
            index[s] = (bk << 16) | len(buckets[bk])
            buckets[bk].append(s)
        return index[s]
    nodes, attrs, values = [], [], bytearray()
    def enc(t, v):
        if t in NUM: return struct.pack(NUM[t], v)
        if t in VEC:
            f, n = VEC[t]; return struct.pack('<' + f[1] * n, *v)
        if t in STR: return v.encode('utf-8') + b'\0'
        if t == 31: return _guid_to_lsf(v)
        if t == 28:
            h = v['handle'].encode() + b'\0'
            return struct.pack('<Hi', v['version'], len(h)) + h
        return bytes.fromhex(v)
    def walk(o, parent):
        idx = len(nodes)
        nodes.append([ref(o.name), parent, -1, -1])
        prev = None
        for n, t, v in o.attrs:
            b = enc(t, v)
            ai = len(attrs)
            attrs.append([ref(n), t | (len(b) << 6), -1, len(values)])
            values.extend(b)
            if prev is None: nodes[idx][3] = ai
            else: attrs[prev][2] = ai
            prev = ai
        last = None
        for c in o.children:
            ci = walk(c, idx)
            if last is not None: nodes[last][2] = ci
            last = ci
        return idx
    last = None
    for r in doc['regions']:
        ri = walk(r, -1)
        if last is not None: nodes[last][2] = ri
        last = ri
    sb = bytearray(struct.pack('<I', len(buckets)))
    for chain in buckets:
        sb += struct.pack('<H', len(chain))
        for s in chain:
            e = s.encode('utf-8'); sb += struct.pack('<H', len(e)) + e
    nb = b''.join(struct.pack('<IiiI', a, b, c, d & 0xffffffff) for a, b, c, d in nodes)
    ab = b''.join(struct.pack('<IIiI', *a) for a in attrs)
    out = bytearray(b'LSOF') + struct.pack('<IQ', doc['version'], doc['engine'])
    out += struct.pack('<10IBBHI', len(sb), 0, 0, 0, len(nb), 0, len(ab), 0, len(values), 0, 0, 0, 0, 1)
    out += sb + nb + ab + values
    open(path, 'wb').write(out)


def to_xml(doc):
    def esc(s): return str(s).replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')
    out = []
    def walk(o, ind):
        out.append('\t' * ind + f'<node id="{o.name}">')
        for n, t, v in o.attrs:
            tn = TYPES.get(t, str(t))
            if t == 28:
                out.append('\t' * (ind + 1) + f'<attribute id="{n}" type="{tn}" handle="{v["handle"]}" version="{v["version"]}" />')
            else:
                if isinstance(v, list): v = ' '.join(str(x) for x in v)
                if isinstance(v, bool): v = 'True' if v else 'False'
                out.append('\t' * (ind + 1) + f'<attribute id="{n}" type="{tn}" value="{esc(v)}" />')
        if o.children:
            out.append('\t' * (ind + 1) + '<children>')
            for c in o.children: walk(c, ind + 2)
            out.append('\t' * (ind + 1) + '</children>')
        out.append('\t' * ind + '</node>')
    e = doc['engine']
    out.append('<?xml version="1.0" encoding="utf-8"?>\n<save>')
    out.append(f'\t<version major="{e >> 55}" minor="{(e >> 47) & 0xff}" revision="{(e >> 31) & 0xffff}" build="{e & 0x7fffffff}" lslib_meta="v1,bswap_guids,lsf_keys_adjacency" />')
    for r in doc['regions']:
        out.append(f'\t<region id="{r.name}">')
        walk(r, 2)
        out.append('\t</region>')
    out.append('</save>')
    return '\n'.join(out)


def from_xml(path, version=7):
    root = ET.parse(path).getroot()
    v = root.find('version')
    engine = (int(v.get('major')) << 55) | (int(v.get('minor')) << 47) | (int(v.get('revision')) << 31) | int(v.get('build'))
    def conv(el):
        o = Node(el.get('id'))
        for a in el.findall('attribute'):
            t = TYPE_IDS[a.get('type')]
            if t == 28: val = {'handle': a.get('handle'), 'version': int(a.get('version'))}
            else:
                s = a.get('value')
                if t in NUM and t != 19: val = float(s) if t in (6, 7) else int(s)
                elif t == 19: val = s.lower() == 'true'
                elif t in VEC:
                    if s is None:   # newer .lsx: <attribute type="fvec3"><float3 x= y= z=/></attribute>
                        c = list(a)[0]
                        s = ' '.join(c.get(k) for k in 'xyzw' if c.get(k) is not None)
                    val = [(float if t >= 11 else int)(x) for x in s.split()]
                else: val = s
            o.attrs.append((a.get('id'), t, val))
        ch = el.find('children')
        if ch is not None:
            o.children = [conv(c) for c in ch.findall('node')]
        return o
    regions = []
    for r in root.findall('region'):
        o = conv(r.find('node'))
        o.name = r.get('id')   # in .lsf the top node carries the region's name (.lsx may say "root")
        regions.append(o)
    return {'version': version, 'engine': engine, 'regions': regions}


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'dump': print(to_xml(read(sys.argv[2])))
    elif cmd == 'tolsx': open(sys.argv[3], 'w', encoding='utf-8').write(to_xml(read(sys.argv[2])))
    elif cmd == 'tolsf': write(from_xml(sys.argv[2]), sys.argv[3])
