"""Brighten the arrival cinematic (GR_Office_Arrival): raise the Key and Fill lights of its scene file.

    python tools/anim/arrival_light.py

The scene's "Default" lighting setup (Key 10, Fill 2.5, Rim 15 as the generator writes it) lit the
characters too dimly in the dark office (game, 18/11). Sets absolute values, so it can be rerun.
Saving the timeline in the Toolkit can rewrite the _Scene.lsx: rerun it afterwards, with
arrival_walk.py, then build_pack.py. Edit LIGHTS to taste (the Rim light is left as it is).
"""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from build_toolkit import DATA, MOD

SCENE = os.path.join(DATA, 'Public', MOD, 'Timeline', 'Generated', 'GR_Office_Arrival_Scene.lsx')
LIGHTS = {'Key': 20, 'Fill': 6}


def main():
    s = open(SCENE, encoding='utf-8-sig').read()
    for name, value in LIGHTS.items():
        pat = (r'(<attribute id="Intensity" type="float" value=")[\d.]+("/>\s*<attribute id="LightChannelFlags"[^>]*/>\s*'
               r'<attribute id="LightCookieTexture"[^>]*/>\s*<attribute id="Name" type="LSString" value="%s")' % name)
        s, n = re.subn(pat, r'\g<1>%s\g<2>' % value, s)
        if n != 1:
            raise SystemExit(f'light {name}: expected 1 match, found {n}')
    open(SCENE, 'w', encoding='utf-8').write(s)
    print('arrival lights:', LIGHTS)


if __name__ == '__main__':
    main()
