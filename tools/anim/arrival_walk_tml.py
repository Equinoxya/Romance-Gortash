"""Write the player's walk into the arrival timeline's editor file (GR_Office_Arrival.tml).

    python tools/anim/arrival_walk_tml.py

Run with the timeline closed in the Toolkit; then reopen it (Ctrl+T in the Dialog Editor) to preview,
and File > Save in the Timeline Panel so the Toolkit compiles it. Same content as arrival_walk.py
(which patched the compiled file directly), but in the editor's own format, so it survives saves.
Rotation keys are in radians ("0; 180; 0" turned the player 180 rad). Key times: the editor names them "ΔTime"; whether they are absolute or relative to the previous key
is checked in the preview (DELTA below).
"""
import os, re, sys, uuid
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from build_toolkit import DATA, MOD

TML = os.path.join(DATA, 'Editor', 'Mods', MOD, 'Timeline', 'Generated', 'GR_Office_Arrival.tml')
PLAYER_TRACK = 'b3c5d367-d721-41d6-b268-6b0ce5d436a0'     # GROUP_Players track
GORTASH_TRACK = 'e0ad3136-0d4d-4bfc-a80b-0a41ca448c20'    # Lord Enver Gortash track
SEQ_DURATION = 13.64
# (time s, local Z in Gortash's frame). In front of him is -Z (preview, 2026-11-18: +Z put the player behind him)
PATH = [(0.0, -3.3), (1.6, -2.8), (3.2, -1.5), (4.4, -1.1)]   # 8 m and 4.5 m started inside a wall (preview)
ANIMS = [('ba49ec42-65c2-4012-861d-745be5fdfbd9', 0.0, 1.6, False),   # CINE_StandL_ToWalk_01
         ('7bd8e368-5ad3-487b-ab93-f868d968590f', 1.6, 1.6, True),    # CINE_Walk_01 (loop)
         ('5bac9aab-21d2-4bdf-8cd6-fedb605d720d', 3.2, 1.2, False)]   # CINE_Walk_ToStandL_01
DELTA = False    # ΔTime is the time in the sequence (preview, 2026-11-18: read as deltas, the player went back and forth)


def nid(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f'GR_arrival_walk_tml/{name}'))


ANIM_TRACK, TR_TRACK = nid('anim_track'), nid('transform_track')


def tracks():
    t = lambda n: nid('track/' + n)
    return (f'          <Track Name="Animation" TrackId="{ANIM_TRACK}" SlotId="e3ff500b-8db3-4fbd-a180-6aad8c3ba4f4" Type="ComponentTrackAnimation">\n'
            f'            <Track Name="Hide VFX" TrackId="{t("hidevfx")}" Type="KeyTrackBoolean" />\n'
            f'          </Track>\n'
            f'          <Track Name="Transform" TrackId="{TR_TRACK}" IsExpanded="true" Type="ComponentTrackTransform">\n'
            f'            <Track Name="Translate" TrackId="{t("translate")}" Type="KeyTrackWrapper">\n'
            f'              <Track Name="X" TrackId="{t("x")}" Type="KeyTrackFloat" />\n'
            f'              <Track Name="Y" TrackId="{t("y")}" Type="KeyTrackFloat" />\n'
            f'              <Track Name="Z" TrackId="{t("z")}" Type="KeyTrackFloat" />\n'
            f'            </Track>\n'
            f'            <Track Name="Rotation" TrackId="{t("rot")}" Type="KeyTrackRotation" />\n'
            f'            <Track Name="Scale" TrackId="{t("scale")}" FallbackValue="1" Type="KeyTrackFloat" />\n'
            f'            <Track Name="Parent Point" TrackId="{t("parent")}" AttachmentType="DummyAttachmentBone" Type="KeyTrackFrameOfReference" />\n'
            f'          </Track>\n')


def components():
    out = [f'        <Components TrackId="{ANIM_TRACK}">']
    for i, (src, start, dur, loop) in enumerate(ANIMS):
        ts = f' TimeStart="{start}"' if start else ''
        cont = ' IsContinuous="true"' if loop else ''
        out.append(f'          <Component ComponentId="{nid(f"anim{i}")}"{ts} ΔTimeDuration="{dur}" AnimationSourceId="{src}" PlayRate="1"{cont} AnimationType="Base" />')
    out.append('        </Components>')
    keys, prev = [], 0.0
    for i, (tm, z) in enumerate(PATH):
        dt = tm - prev if DELTA else tm
        prev = tm
        keys.append(f'              <Key ΔTime="{round(dt, 3)}" Id="{nid(f"zkey{i}")}" Value="{z}" />')
    out += [f'        <Components TrackId="{TR_TRACK}">',
            f'          <Component ComponentId="{nid("transform")}" TimeDuration="{SEQ_DURATION}">',
            '            <Channel Name="Transform.Translate.X">',
            f'              <Key ΔTime="0" Id="{nid("x0")}" Value="0" />',
            '            </Channel>',
            '            <Channel Name="Transform.Translate.Y">',
            f'              <Key ΔTime="0" Id="{nid("y0")}" Value="0" />',
            '            </Channel>',
            '            <Channel Name="Transform.Translate.Z">', *keys, '            </Channel>',
            '            <Channel Name="Transform.Rotation">',
            f'              <Key ΔTime="0" Id="{nid("r0")}" Value="0; 3.14159; 0" />',
            '            </Channel>',
            '            <Channel Name="Transform.Parent Point">',
            f'              <Key ΔTime="0" Id="{nid("p0")}">',
            f'                <Value TargetId="{GORTASH_TRACK}" TargetBone="Dummy_Root" KeepScale="true" />',
            '              </Key>',
            '            </Channel>',
            '          </Component>',
            '        </Components>']
    return '\n'.join(out) + '\n'


def main():
    s = open(TML, 'rb').read().decode('utf-8-sig').replace('\r\n', '\n')
    if ANIM_TRACK in s:
        print('already there: restore the file from the backup before rerunning'); return
    # tracks: inside the player's track, after its Foot IK track
    a = s.index(f'TrackId="{PLAYER_TRACK}"')
    b = s.index('Type="ComponentTrackPhysics" />\n', a) + len('Type="ComponentTrackPhysics" />\n')
    s = s[:b] + tracks() + s[b:]
    # components: at the end of the first (only) sequence
    e = s.index('      </Sequence>')
    s = s[:e] + components() + s[e:]
    open(TML, 'wb').write(b'\xef\xbb\xbf' + s.replace('\n', '\r\n').encode('utf-8'))
    import xml.etree.ElementTree as ET
    ET.fromstring(s.split('?>', 1)[1])
    print('walk written into', os.path.basename(TML))


if __name__ == '__main__':
    main()
