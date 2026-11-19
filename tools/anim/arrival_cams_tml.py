"""Camera shots of the arrival cinematic (GR_Office_Arrival.tml), in the editor's format.

    python tools/anim/arrival_cams_tml.py

Run with the timeline closed in the Toolkit, after arrival_walk_tml.py.
- Walk (narrator line A0): cam_player_OTS_subject1, behind Gortash's shoulder, looking at the
  player as they come in. The generated cam_player_MCU was attached to the player's starting point
  and did not follow the walk (preview, 2026-11-18).
- Gortash's line (AG) keeps the generated close-up: it framed his hair while the player stood in the
  wrong place, and is fine now (preview, 2026-11-18).
Camera ids come from the camera scene bnz_standing_Px1_Shipping.lsx.
"""
import os, re, sys, uuid
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from build_toolkit import DATA, MOD

TML = os.path.join(DATA, 'Editor', 'Mods', MOD, 'Timeline', 'Generated', 'GR_Office_Arrival.tml')
GORTASH, PLAYER = 'e0ad3136-0d4d-4bfc-a80b-0a41ca448c20', 'b3c5d367-d721-41d6-b268-6b0ce5d436a0'
CAMS = [  # (name, scene camera id, attach to, look at)
    ('cam_player_OTS_subject1', 'ff9136ca-e96e-4709-8d3c-f4a6d0de5690', GORTASH, PLAYER),
]


def nid(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f'GR_arrival_cams/{name}'))


def main():
    s = open(TML, 'rb').read().decode('utf-8-sig').replace('\r\n', '\n')
    track_ids = []
    for name, cam, attach, look in CAMS:
        tid = nid(name + '/track'); track_ids.append(tid)
        if tid in s:
            continue
        block = (f'        <Track Name="{name}" TrackId="{tid}" ActorType="scenecam" ActorId="{nid(name + "/actor")}" '
                 f'AssignedActorId="00000000-0000-0000-0000-000000000000" SceneCameraId="{cam}" '
                 f'SceneCameraAttachTo="{attach}" SceneCameraLookAt="{look}" Type="ActorTrackSceneCamera">\n'
                 '          <CustomActorData Type="CustomActorSoundData" />\n          <ActorEndState />\n'
                 '          <ActorIdleOverrideData />\n          <BehaviourActorStartCondition />\n        </Track>\n')
        a = s.index('<Track Name="Cameras"')
        b = s.index('\n      </Track>', a) + 1          # end of the Cameras folder
        s = s[:b] + block + s[b:]
    # the two shots of the sequence, in order
    seq = s.index('<Sequence ')
    shots = s.index('<Components TrackId="', seq)
    end = s.index('</Components>', shots)
    part = s[shots:end]
    ids = iter(track_ids)
    part = re.sub(r'<Camera CameraId="[^"]+"', lambda m: f'<Camera CameraId="{next(ids)}"', part, count=len(track_ids))
    s = s[:shots] + part + s[end:]
    # No background extras ("peanuts") in this scene: the camera template adds three, and in the
    # preview they stood between the camera and the walking player. Without a template, none spawns.
    s = re.sub(r'(ActorType="peanut" ActorId="[^"]+" AssignedActorId=")[^"]+"',
               r'\g<1>00000000-0000-0000-0000-000000000000"', s)
    open(TML, 'wb').write(b'\xef\xbb\xbf' + s.replace('\n', '\r\n').encode('utf-8'))
    import xml.etree.ElementTree as ET
    ET.fromstring(s.split('?>', 1)[1])
    print('shots:', [c[0] for c in CAMS])


if __name__ == '__main__':
    main()
