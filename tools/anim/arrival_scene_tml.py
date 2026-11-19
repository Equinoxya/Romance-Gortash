"""Build the arrival cinematic (GR_Office_Arrival.tml) in the editor's format, in one go.

    python tools/anim/arrival_scene_tml.py

Start from the timeline the editor generated (BACKUP), with the timeline closed in the Toolkit; then
reopen it, check it in the preview (Preview Options > Location > S_WYR_Gortash_OfficePos) and
Ctrl+S in the Timeline Panel so the Toolkit compiles it.

Two shots, as the office entrance is about 34 m in front of Gortash (level data:
S_WYR_Gortash_OfficePos and the entrance point S_Debug_Teleport_WYR_GortashsOffice):
1. At the doors: the player comes in and takes a few steps; a camera placed in the room, parented
   to Gortash like the player, looks back at them.
2. Cut, near Gortash: the last steps, filmed behind his shoulder (cam_player_OTS_subject1).
Positions are in Gortash's frame (metres): -Z is in front of him, rotations in radians.
Key times (the editor's "ΔTime") are absolute times in the sequence.
"""
import os, re, sys, uuid
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from build_toolkit import DATA, MOD

TML = os.path.join(DATA, 'Editor', 'Mods', MOD, 'Timeline', 'Generated', 'GR_Office_Arrival.tml')
BACKUP = os.path.join(os.path.dirname(__file__), 'GR_Office_Arrival.generated.tml')
PLAYER_TRACK = 'b3c5d367-d721-41d6-b268-6b0ce5d436a0'
GORTASH_TRACK = 'e0ad3136-0d4d-4bfc-a80b-0a41ca448c20'
SEQ = 13.64
CUT = 3.95                                  # end of the door shot
DOOR = (-2.6, -23.0)                        # just inside the office doors, in Gortash's frame (x, z): player position read in game (-3.17, 73.01, 210.08), 18/11

# player path: (time, x, z)
PATH = [(0.0, DOOR[0], DOOR[1]), (1.6, DOOR[0], DOOR[1] + 0.5), (CUT, DOOR[0], DOOR[1] + 3.1),
        (CUT + 0.02, 0.0, -3.3), (6.6, 0.0, -1.5), (7.8, 0.0, -1.1)]
ANIMS = [('ba49ec42-65c2-4012-861d-745be5fdfbd9', 0.0, 1.6, False),   # CINE_StandL_ToWalk_01
         ('7bd8e368-5ad3-487b-ab93-f868d968590f', 1.6, 5.0, True),    # CINE_Walk_01, loops through the cut
         ('5bac9aab-21d2-4bdf-8cd6-fedb605d720d', 6.6, 1.2, False)]   # CINE_Walk_ToStandL_01
# door camera: in the room, ahead of the player, at head height, looking back at the doors
DOOR_CAM_POS = (0.3, 1.6, -14.0)   # mid-aisle, looking back at the doors; near the doors it framed a wall (game, 18/11)
DOOR_CAM_ROT = '0; 3.14159; 0'              # unrotated, it looked at Gortash (preview)
DOOR_CAM_SCENE = 'a7578f69-00a4-49fe-b8fa-b2cceb145f53'   # cam_player_MCU of the camera scene
OTS_SCENE = 'ff9136ca-e96e-4709-8d3c-f4a6d0de5690'        # cam_player_OTS_subject1


def nid(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f'GR_arrival_scene/{name}'))


def transform_tracks(prefix):
    t = lambda n: nid(f'{prefix}/{n}')
    return (f'          <Track Name="Transform" TrackId="{t("transform")}" IsExpanded="true" Type="ComponentTrackTransform">\n'
            f'            <Track Name="Translate" TrackId="{t("translate")}" Type="KeyTrackWrapper">\n'
            f'              <Track Name="X" TrackId="{t("x")}" Type="KeyTrackFloat" />\n'
            f'              <Track Name="Y" TrackId="{t("y")}" Type="KeyTrackFloat" />\n'
            f'              <Track Name="Z" TrackId="{t("z")}" Type="KeyTrackFloat" />\n'
            f'            </Track>\n'
            f'            <Track Name="Rotation" TrackId="{t("rot")}" Type="KeyTrackRotation" />\n'
            f'            <Track Name="Scale" TrackId="{t("scale")}" FallbackValue="1" Type="KeyTrackFloat" />\n'
            f'            <Track Name="Parent Point" TrackId="{t("parent")}" AttachmentType="DummyAttachmentBone" Type="KeyTrackFrameOfReference" />\n'
            f'          </Track>\n')


def transform_component(prefix, xs, ys, zs, rot):
    def chan(name, keys):
        out = [f'            <Channel Name="{name}">']
        for i, (tm, v) in enumerate(keys):
            out.append(f'              <Key ΔTime="{round(tm, 3)}" Id="{nid(f"{prefix}/{name}/{i}")}" Value="{v}" />')
        out.append('            </Channel>')
        return out
    return '\n'.join([f'        <Components TrackId="{nid(prefix + "/transform")}">',
                      f'          <Component ComponentId="{nid(prefix + "/component")}" TimeDuration="{SEQ}">',
                      *chan('Transform.Translate.X', xs), *chan('Transform.Translate.Y', ys),
                      *chan('Transform.Translate.Z', zs), *chan('Transform.Rotation', [(0, rot)]),
                      '            <Channel Name="Transform.Parent Point">',
                      f'              <Key ΔTime="0" Id="{nid(prefix + "/parent0")}">',
                      f'                <Value TargetId="{GORTASH_TRACK}" TargetBone="Dummy_Root" KeepScale="true" />',
                      '              </Key>', '            </Channel>', '          </Component>', '        </Components>']) + '\n'


def camera_track(name, scene_cam, attach, look, with_transform):
    tid = nid(name + '/track')
    body = transform_tracks(name) if with_transform else ''
    return tid, (f'        <Track Name="{name}" TrackId="{tid}" ActorType="scenecam" ActorId="{nid(name + "/actor")}" '
                 f'AssignedActorId="00000000-0000-0000-0000-000000000000" SceneCameraId="{scene_cam}" '
                 f'SceneCameraAttachTo="{attach}" SceneCameraLookAt="{look}" Type="ActorTrackSceneCamera">\n'
                 + body.replace('          <', '          <', 1) +
                 '          <CustomActorData Type="CustomActorSoundData" />\n          <ActorEndState />\n'
                 '          <ActorIdleOverrideData />\n          <BehaviourActorStartCondition />\n        </Track>\n')


def main():
    if not os.path.exists(BACKUP):
        raise SystemExit(f'missing {BACKUP}: copy of the timeline as the editor generated it')
    s = open(BACKUP, 'rb').read().decode('utf-8-sig').replace('\r\n', '\n')
    # player: animation track + transform track, after the player's Foot IK track
    a = s.index(f'TrackId="{PLAYER_TRACK}"')
    b = s.index('Type="ComponentTrackPhysics" />\n', a) + len('Type="ComponentTrackPhysics" />\n')
    anim_track = nid('player/anim')
    s = s[:b] + (f'          <Track Name="Animation" TrackId="{anim_track}" SlotId="e3ff500b-8db3-4fbd-a180-6aad8c3ba4f4" Type="ComponentTrackAnimation">\n'
                 f'            <Track Name="Hide VFX" TrackId="{nid("player/hidevfx")}" Type="KeyTrackBoolean" />\n'
                 '          </Track>\n') + transform_tracks('player') + s[b:]
    # cameras: the door camera (moved by a transform) and the over-the-shoulder one
    door_tid, door_block = camera_track('GR_cam_door', DOOR_CAM_SCENE, GORTASH_TRACK, PLAYER_TRACK, True)
    ots_tid, ots_block = camera_track('cam_player_OTS_subject1', OTS_SCENE, GORTASH_TRACK, PLAYER_TRACK, False)
    a = s.index('<Track Name="Cameras"'); b = s.index('\n      </Track>', a) + 1
    s = s[:b] + door_block + ots_block + s[b:]
    # no background extras ("peanuts")
    s = re.sub(r'(ActorType="peanut" ActorId="[^"]+" AssignedActorId=")[^"]+"',
               r'\g<1>00000000-0000-0000-0000-000000000000"', s)
    # shots: door, then over the shoulder until the narrator's line ends, then the generated close-up
    seq = s.index('<Sequence '); c0 = s.index('<Components TrackId="', seq); c1 = s.index('</Components>', c0)
    shots = s[c0:c1]
    first = re.search(r'\s*<Component ComponentId="[^"]+" TimeDuration="([0-9.]+)"(.*?)</Component>', shots, re.S)
    end_first = float(first.group(1))
    new_first = (f'\n          <Component ComponentId="{nid("shot/door")}" TimeDuration="{CUT}"{first.group(2).split(">",1)[0]}>\n'
                 f'            <CameraContainer>\n              <Camera CameraId="{door_tid}" />\n            </CameraContainer>\n          </Component>'
                 f'\n          <Component ComponentId="{nid("shot/ots")}" TimeStart="{CUT}" TimeDuration="{round(end_first - CUT, 3)}"{first.group(2).split(">",1)[0]}>\n'
                 f'            <CameraContainer>\n              <Camera CameraId="{ots_tid}" />\n            </CameraContainer>\n          </Component>')
    shots = shots[:first.start()] + new_first + shots[first.end():]
    s = s[:c0] + shots + s[c1:]
    # sequence components: player animations and transform, door camera transform
    out = [f'        <Components TrackId="{anim_track}">']
    for i, (src, start, dur, loop) in enumerate(ANIMS):
        ts = f' TimeStart="{start}"' if start else ''
        cont = ' IsContinuous="true"' if loop else ''
        out.append(f'          <Component ComponentId="{nid(f"player/anim{i}")}"{ts} ΔTimeDuration="{dur}" AnimationSourceId="{src}" PlayRate="1"{cont} AnimationType="Base" />')
    out.append('        </Components>')
    comps = '\n'.join(out) + '\n'
    comps += transform_component('player', [(t, x) for t, x, z in PATH], [(0, 0)], [(t, z) for t, x, z in PATH], '0; 3.14159; 0')
    cx, cy, cz = DOOR_CAM_POS
    comps += transform_component('GR_cam_door', [(0, cx)], [(0, cy)], [(0, cz)], DOOR_CAM_ROT)
    e = s.index('      </Sequence>')
    s = s[:e] + comps + s[e:]
    import xml.etree.ElementTree as ET
    ET.fromstring(s.split('?>', 1)[1])
    open(TML, 'wb').write(b'\xef\xbb\xbf' + s.replace('\n', '\r\n').encode('utf-8'))
    print('arrival scene written: door shot', CUT, 's, then over the shoulder')


if __name__ == '__main__':
    main()
