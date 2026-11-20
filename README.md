# Gortash Romance (BG3 mod)

A Baldur's Gate 3 mod that adds a romance path with Lord Enver Gortash, for Tav and the Dark Urge. Written in English, with a full French translation.

## Status

- **Written**: every letter, scene and extension, in English and French, with Tav / Dark Urge variants and masculine / feminine / non-binary variants. 330 localized strings per language.
- **Built and playing in game** (v1.0.0.15, 2026-11-19): the invitation letter, and the office evening staged in Gortash's real office at night: an arrival cinematic, camera cuts, gestures, a wine glass in his hand, a moving mouth, and our own animations for the hand he offers, the player taking it and the hand kiss.
- **Changed on 2026-11-19, not seen in game yet**: the hands and the hand kiss redone so the hands rest on each other, the bow after the kiss removed, the hand offer no longer drops, a shorter invitation letter signed "E.", lighter wording for Gortash and pet names after the private night.
- **Generated and wired, not played yet**: the ball, the private night, the Dark Urge memories, the scene after Orin.
- **Next**: the to-do list, in French, in `docs/A_faire.md`.

## Before you start

- The official BG3 Toolkit cannot add dialogues. The scenes need a community-unlocked Toolkit (Toolkit Unlocked or MoonGlasses), which Larian does not support. The letters and gifts alone can be made with the official Toolkit.
- Plan to publish on Nexus Mods. Whether mod.io accepts a dialogue mod made with an unlocked Toolkit is not confirmed.
- New lines have no voice. The dance and the private night are told by the narrator, with a fade to black.

## The story

After his coronation, Gortash sends a letter to camp inviting the player to his office one evening. He flirts; if the player responds, an invitation to a ball follows, with a dance. A second, private letter leads to a night in his rooms. If the player stays allied with him and the romance holds, he survives the confrontation with the brain.

For Tav, this is a new romance. For the Dark Urge, it is a reunion: the two were lovers before the base game, and Gortash grieved when he believed them dead.

## Roadmap

| Step | Content | Status |
|---|---|---|
| 1 | Invitation letter delivered at camp after the coronation | **Done** (2026-11-20): short letter signed "E." |
| 2 | Evening in his office: flirt dialogue | **Done** (2026-11-20, v1.0.0.21): from camp to the office and back, staged with a timeline and custom animations |
| 3 | Invitation card and ball with a dance | Draft in `Dialogs/GR_Ball.md`, awaiting review |
| 4 | Second letter and private night (text, fade to black) | Draft in `Dialogs/GR_Private_Night.md`, awaiting review |
| 5 | Ending where he survives (alliance + romance) | Draft in `Dialogs/GR_Ending.md`, awaiting review |

Steps are in story order. Every scene has Tav and Dark Urge variants. "Draft" means the text is written and localized, but not yet built in the Toolkit.

## Extensions

Optional content on top of the five steps. All of it is a draft awaiting review.

| Extension | Script | Content |
|---|---|---|
| Gifts | `Dialogs/GR_Gifts.md` | Bottle, dance card, key, and a knife for the Dark Urge, each with a note |
| Ambient greetings | `Dialogs/GR_Ambient.md` | What Gortash says between scenes, by stage of the romance |
| Breakup letter | `Dialogs/GR_Breakup.md` | A last letter if the player ends it |
| Companion reactions | `Dialogs/GR_Companions.md` | A full scene with Karlach, one exchange each for seven others |
| Jealousy | `Dialogs/GR_Jealousy.md` | Gortash asks where he stands if the player has another romance |
| Dark Urge memories | `Dialogs/GR_Memories.md` | Three narrated memories of their past. Generated and wired (`GR_Memory_*` dialogs, one per long rest), not played yet |
| The foundry | `Dialogs/GR_Foundry.md` | The romance is tested if the player destroys the Steel Watch |
| After Orin | `Dialogs/GR_Orin.md` | His reaction to Orin's death, with lines for a Dark Urge who rejected Bhaal. Generated and wired (`GR_Orin`, first long rest after her death), not played yet |

Not done, because they need work inside the Toolkit or outside this repository: a real animated dance, a real location for his rooms, and recorded voices (lines are silent; only the mouth moves, see below). `docs/voice_lines.md` lists every spoken line per character for anyone who wants to record them.

## Files

- `Dialogs/*.md`: the source of all text, English and French side by side. Edit the text here.
- `tools/build_loca.py`: rebuilds the three files below from the dialogue scripts
- `tools/build_toolkit.py`: writes books, item root templates and flags straight into the Toolkit project (run with the Toolkit closed; `--osiris` also fills `GR_Letters.txt`). Items and the game templates they inherit from:
  - `GR_Letter_Invitation` (made in the Toolkit, masculine greeting), `_F`, `_NB`: inherit from it
  - `GR_Letter_Epilogue`, `GR_Letter_Epilogue_Away`, `GR_Letter_Breakup1`, `GR_Letter_Breakup2`: inherit from `GR_Letter_Invitation` (black wax, same look)
  - `GR_Card_Ball`, `GR_Letter_Night`: plain paper letter (`BOOK_GEN_Paper_Letter_C`)
  - `GR_Gift_Wine`: `CONS_Drink_Wine_B`, so it can be drunk. `GR_Gift_Key`: `BASE_KEY`. `GR_Gift_Knife`: a plain dagger (`WPN_HUM_Dagger_A_0`)
  - `GR_Gift_DanceCard`: paper card (`BOOK_Letter_A`); reading it shows its note, since paper items always open a book
- `tools/build_voice.py`: gives Gortash's lines a moving mouth with silent voice files (see Timelines)
- `tools/anim/`: animation and timeline scripts. `evening_hands.py` sets the hand offer, the hand kiss, the player's position and the removed gestures in the office timeline: run it after every Toolkit save of `GR_Office_Evening`, then `build_pack.py`. The `arrival_*` scripts build the arrival cinematic. `fix_glb.py` makes a Blender export readable by LSLib.
- The animation sources (Blender files, exports, `.GR2`) are not in this repository: they live in a separate work folder (`GortashAnim`). `GortashAnim/hands_contact.py` rebuilds the hand-taking and hand-kiss animations so the hands rest on each other.
- `tools/lsf.py`: reads and writes the Toolkit's uncompressed `.lsf` files (`python tools/lsf.py dump FILE.lsf` to inspect one)
- `Toolkit/backup/`: the Toolkit files as they were before `build_toolkit.py` first changed them
- `Localization/English/GortashRomance.loca.xml`: English text, generated
- `Localization/French/GortashRomance.loca.xml`: French text, generated, same handles
- `Localization/handles.md`: handle of every line, to copy into the Toolkit, generated
- `Story/RawFiles/Goals/GR_Letters.txt`: Osiris script that delivers the letters and gifts
- `docs/voice_lines.md`: every spoken line per character, generated
- `docs/Guide-Gortash-Romance.pdf`: step-by-step guide (in French) for the Toolkit work
- `docs/guide.html`: source of the guide

After editing a dialogue script, run `python3 tools/build_loca.py`. Handles do not change when the text changes, only when a line id is renamed.

## Notation in the dialogue scripts

- `[Tav]`: shown when the player is not the Dark Urge. `[Durge]`: shown when the player is the Dark Urge. No tag: shown to both.
- `[Durge, rejected Bhaal]` and `[Durge, accepted Bhaal]`: extra conditions on what the Dark Urge did in Bhaal's temple.
- `[a / b / c]` inside a line: three versions of that line, picked by the player's identity, always in the order masculine / feminine / non-binary.
- English only needs this when someone talks about the player (`[he / she / they]`).
- French also needs it for agreements (`[venu / venue / ...]`). The non-binary version uses `iel` / `ellui` and wording with no agreement, never the masculine by default.
- In French, Gortash says "vous" until the private night (step 4), then "tu". The narrator always says "vous". Two exceptions: he goes back to "vous" in the foundry scene, and says "tu" in the Dark Urge's memories.
- After the private night he has a pet name for the player: "my favourite problem" ("mon problème préféré") for Tav, "my blade" ("ma lame") for the Dark Urge.

In the Toolkit, each `[a / b / c]` line becomes three text variants on the same node, each with its identity tag. `[Tav]` and `[Durge]` are a `REALLY_DARK_URGE` tag check on the node itself, as most game dialogs do it: a variant that tests both the tag and the identity makes the editor report the dialog as invalid.

Timelines: generated in the dialog editor (Timeline > Generate > Full, Custom camera scene `Public/Shared/Timeline/Scenes/Default/bnz_standing_Px1_Shipping.lsf`, uncheck "Generate ML Emotions"). The default `Px0` scenes have no camera for the NPC. The camera scene lives in `Shared.pak`; a copy was extracted to `Data/Public/Shared/Timeline/Scenes/Default/` so the file picker can select it. `build_dialogs.py` keeps what the editor adds to a saved dialog (timeline link, ignored flag combinations), but not node groups: a grouped narrator line and the next line were played as one timeline phase, and the game skipped the "Continue" between them. `build_pack.py` points each timeline at the dialog resource that `GR_Letters.txt` starts, writes the `_Scene.lsf` the Toolkit leaves out (the game crashed without it; every base game timeline ships one), and rewrites `_Scene.lsx` vectors so the Multitool accepts them. `GR_Office_Evening` has one and it plays in game (2026-11-17), cutting between the player and Gortash when they stand together; with Gortash elsewhere, only the player is filmed.

The office timeline was then edited by hand (`.tml` with the Toolkit closed, then reopened and saved so the Toolkit recompiles it), and tested in game on 2026-11-17:
- 12 gestures on Gortash (pointing, drinking, shrugs, nods, bows). Animations added in the editor default to "Continuous" and loop; `build_pack.py` removes it.
- A wine glass (`CINE_DrinkWineGlassA_NotForDecoration`, a template actor) parented to his `Dummy_R_Hand`, shown only while he drinks.
- Front shots of Gortash instead of the template's over-the-shoulder shots, which showed mostly the player's back.
- One custom camera, `GR_cam_TWOSHOT_side`, added to `GR_Office_Evening_Scene.lsx` for the moment he steps closer (N7, N8, N8D): side view of both. Not seen in game yet. Saving the timeline in the Toolkit may rewrite the scene file and drop it.

Moving mouth without a voice (works in game, 2026-11-17): `python tools/build_voice.py` gives each of Gortash's 80 lines a silent `.wem` (hand-made PCM; the game's voices are Vorbis, but PCM plays), a voice meta entry, the lip animation (`.ffxanim`) of a real Gortash line of similar length, and his FaceFX actor files, all under `Mods/<mod>/Localization/English/`. The lips do not match our words. The longest Gortash line in the game is 14 s, so on longer lines the mouth stops early. Without the `.wem` the mouth does not move. Method from the BG3 Community Wiki guide "Adding New Voice Lines And Dialog".

## Flags

| Flag | Meaning |
|---|---|
| `GR_Letter1_Delivered` | First letter delivered |
| `GR_Office_Visited` | Office scene played |
| `GR_Romance_Interested` | Romance open after the office |
| `GR_Romance_Declined` | Player refused in the office |
| `GR_Ball_Invited`, `GR_Ball_Attended`, `GR_Ball_Danced` | Ball progress |
| `GR_Night_Invited` | Second letter delivered |
| `GR_Romance_Committed` | Romance established after the private night |
| `GR_Romance_Ended` | Romance over for good |
| `GR_Gortash_Saved` | He survived the brain |
| `GR_First_Names` | They say "tu" in French (set during the private night) |
| `GR_Left_City` | The player left Baldur's Gate at the end |

The extensions add their own flags, listed at the top of each script. `GR_Memory1_Seen` to `GR_Memory3_Seen` (Dark Urge memories) and `GR_Orin_Done` (after Orin) are generated with the 13 above.

These 13 flags are generated by `tools/build_toolkit.py` into `Public/<mod>/Flags/`, with a fixed UUID derived from the name, and are already filled in `GR_Letters.txt` as `Name_UUID`. In dialogues, pick them by name in the Toolkit. Their `Usage` is 5, the value the game uses for its own romance state flags set on the player.

## French terms to check against the game

Written from memory, to confirm in the French version of BG3:

- Shadow-Cursed Lands: `Terres maudites`
- Netherstones: `pierres infernales`
- the Urge: `la Pulsion`
- the Absolute: `l'Absolue`
- patriars: `patriars`
- Chosen: `Élu`
- Tethyr: `Téthyr`
- Flaming Fist: `Poing Enflammé`
- Lower City: `Ville Basse`
- Avernus: `Averne`
- Gondians: `Gondiens`

## Not verified yet

The 13 items load in the Toolkit, with inheritance and their Book action. In game (2026-11-16): the invitation letter is delivered by `GR_Letters.txt` and shows its name, description and text. The other items and steps have not been played yet.

To test: `python tools/build_voice.py` (when Gortash's lines change), `python tools/build_pack.py`, then drop `build/GortashRomance` on the BG3 Modders Multitool (it packs and installs the .pak). Mod text must sit in `Localization/<Language>/` at the root of the pack, which `build_pack.py` does.

`GR_Letters.txt` has no placeholder left. Base game flags, tags and the Act 3 goal were taken from the game's own story scripts, and every Osiris call matches how those scripts use it (sources at the top of the file). Still to check:

- that the goal, parented to `Act3`, is still active during the epilogue party

Step 2 is staged and works in game (2026-11-17, v1.0.0.4, from inside Wyrm's Rock; from camp not tested yet): closing the letter starts `GR_Office_Invitation` ("tonight?"); "tonight" fades to black, moves Gortash to his place in his real office and the player, alone, next to him, and plays `GR_Office_Evening` there with its timeline (`GR_Letters.txt`, region "Step 2").

Next steps, in French: `docs/A_faire.md`. The ball (`GR_Ball`) and the private night (`GR_Private_Night`) are generated and wired like the office scene (closing the card / the second letter), not yet saved in the editor nor played.

Dialogues: `tools/build_dialogs.py` writes (`--only NAME,NAME` to leave the other dialogs alone) the dialog source (.lsj) and its DialogBank resource. Then restart the Toolkit (it only reads new resources at start), open the dialog in the MoonGlasses Dialog Editor and File > Save, which writes `DialogsBinary/*.lsf`. `GR_Office_Evening` (step 2) opens and saves this way; its texts, Tav/Durge rules and identity variants show correctly. The only warning is the intended one: no start node when `GR_Letter1_Delivered` is missing or `GR_Office_Visited` is set. It starts when the player closes the invitation letter (`GR_Letters.txt`, `GameBookInterfaceClosed`) and first asks whether to go tonight; "Not tonight" can be chosen again later. No timeline. In game (2026-11-16), started from the Script Extender console with `QRY_StartDialog`, it plays even though Gortash is far away. A save keeps the version of `GR_Letters.txt` it already ran until the mod version changes: after editing the story, raise the version in `Data/Mods/<mod>/meta.lsx` (the game and BG3ModManager read that file, not the one in the .pak), repack, and export the load order again.

It builds in the Toolkit's Story Editor (2026-11-16), so the mod flags, items, base game flags and tags it uses are all known. First build of a new story: click Generate Definitions, then Build.
