# À faire (préparé le 16/11/2026 au soir)

Ce qui a été fait sans toi, et ce qu'il reste à faire dans le Toolkit et le jeu.

## Déjà prêt dans le projet Toolkit

- **Le bal** (`GR_Ball`, 55 nœuds) et **la nuit privée** (`GR_Private_Night`, 53 nœuds) sont générés, comme la scène du bureau.
- Chacun se lance en refermant son objet : le carton du bal, la deuxième lettre. Le joueur choisit d'abord « ce soir » ou « pas ce soir ».
- 8 nouvelles répliques pour ces choix, en anglais et en français, dans `Dialogs/GR_Ball.md` et `Dialogs/GR_Private_Night.md` (sections « The card » et « The letter »). Relis-les et réécris-les si tu veux, puis lance `python tools/build_loca.py`.
- `GR_Letters.txt` contient les deux nouveaux déclencheurs.
- La version du mod est passée à **1.0.0.2** dans le `meta.lsx` du projet.
- **Les souvenirs du Dark Urge** (extension, ajoutés le 17/11) : trois petites scènes racontées (`GR_Memory_FirstMeeting`, `GR_Memory_Rooftop`, `GR_Memory_LastMorning`), 3 nœuds chacune, et leurs flags `GR_Memory1_Seen` à `GR_Memory3_Seen`. Chacune se lance à la fin du premier long repos après une étape (bureau avec romance ouverte, bal, nuit privée), pour un Dark Urge seulement, un souvenir par repos.
- **Après Orin** (extension, 17/11) : la scène `GR_Orin` (15 nœuds, flag `GR_Orin_Done`). Elle se lance au premier long repos après la mort d'Orin, si Orin meurt après la nuit privée et que la romance tient. Tav et Durge ont chacun leur début ; pour Durge, les réponses dépendent de Bhaal (accepté ou rejeté).

- **Timeline du bureau** (17/11) : **marche en jeu**, la caméra passe du joueur à Gortash. Pour la refaire ou en faire une autre : éditeur de dialogues, Timeline > Generate > Full, module GortashRomance, puis sur Parameters choisir **Custom** > `Default/bnz_standing_Px1_Shipping.lsf` (modèle à un interlocuteur ; le choix par défaut, `Px0_demoWOTC`, n'a que des caméras sur le joueur), décocher « Generate ML Emotions ». « Camera scene » doit dire **valid**. Gortash doit être près du joueur : la timeline filme chacun là où il est.
- Ce qu'il a fallu corriger pour la timeline (fait par `build_pack.py`) : générer le `_Scene.lsf` que le Toolkit n'écrit pas (sans lui, le jeu plantait), réécrire les vecteurs du `_Scene.lsx` pour le Multitool, rattacher la timeline à notre ressource de dialogue.
- **Correctif « invalid structure »** (17/11) : le test Tav / Dark Urge est maintenant une condition sur le nœud (comme dans les dialogues du jeu), plus une règle dans chaque variante de texte. Les 7 dialogues sont régénérés. `build_dialogs.py` garde ce que l'éditeur ajoute (lien vers la timeline, groupes, combinaisons de flags ignorées), et `build_pack.py` rattache la timeline à la ressource de dialogue que lance `GR_Letters.txt`.

## Étapes, dans l'ordre

1. **Relancer le Toolkit** (il ne lit les nouveaux dialogues qu'au démarrage).
2. **Éditeur de dialogues** : ouvrir `GR_Office_Evening`, bouger un nœud, File > Save, et vérifier que l'erreur sur N2, N5 et X2 a disparu. Puis pareil pour `GR_Ball`, `GR_Private_Night`, les trois souvenirs (`GR_Memory_FirstMeeting`, `GR_Memory_Rooftop`, `GR_Memory_LastMorning`) et `GR_Orin`. Le message sur les combinaisons de flags est normal. Le message « Module not loaded » sur un dossier Autosave aussi : cliquer OK.
3. **StoryEditor** : ouvrir `GR_Letters`, Generate Definitions, puis Build. Il doit passer sans erreur.
4. Fermer le Toolkit, puis `python tools/build_pack.py`.
5. **Multitool** : mettre Build à **2**, puis Rebuild.
6. **BG3ModManager** : Refresh (vérifier 1.0.0.2), Save Load Order, Export Order to Game.
7. **Tester en jeu** avec la console du Script Extender (ci-dessous).

## Tester sans jouer jusque-là

Dans la console du Script Extender, sur une sauvegarde de test :

Le bal :

```lua
Osi.SetFlag("GR_Ball_Invited_bb642d72-c815-514d-93f4-6e0fc7deb142", Osi.GetHostCharacter())
```

```lua
Osi.TemplateAddTo("GR_Card_Ball_adb0c465-2e66-57cd-b97e-494e2c0b0186", Osi.GetHostCharacter(), 1, 1)
```

Puis lire le carton et le refermer.

La nuit privée :

```lua
Osi.SetFlag("GR_Night_Invited_2390e96e-2fe0-5d5f-a764-11fa5eeb83bf", Osi.GetHostCharacter())
```

```lua
Osi.TemplateAddTo("GR_Letter_Night_6f0efd58-c77e-58b9-8ca6-82fb8324d922", Osi.GetHostCharacter(), 1, 1)
```

Puis lire la lettre et la refermer.

Les souvenirs (avec un Dark Urge), directement :

```lua
Osi.QRY_StartDialog("GR_Memory_FirstMeeting_07875786-2825-58af-ba35-1d031c7a3fd9", "S_GLO_Gortash_b878a854-f790-4999-95c4-3f20f00f65ac", Osi.GetHostCharacter())
```

Ou comme en vrai : poser le flag de l'étape, puis faire un long repos.

```lua
Osi.SetFlag("GR_Romance_Interested_37b333a2-d7be-59f9-809a-dd7759564264", Osi.GetHostCharacter())
```

Ce flag envoie aussi le carton du bal au même repos, c'est normal.

Après Orin, directement :

```lua
Osi.QRY_StartDialog("GR_Orin_4d2355e0-e20d-548b-8fbb-002f4ab8e60b", "S_GLO_Gortash_b878a854-f790-4999-95c4-3f20f00f65ac", Osi.GetHostCharacter())
```

À vérifier : les textes, les répliques Tav ou Durge, et pour un Dark Urge les répliques qui changent selon Bhaal (N10, D3).

Pour la timeline du bureau : la caméra suit-elle Gortash et le joueur, et le texte féminin / non-binaire s'affiche-t-il avec un Tav qui n'est pas un homme (N2, N5, X2) ?

## La vraie mise en scène du bureau (marche en jeu, 1.0.0.4, 17/11)

Testé depuis la Forteresse : le joueur arrive seul à 1,7 m de Gortash, à sa place dans son bureau, et la soirée se joue avec sa timeline. Pas encore testé : lire la lettre depuis le camp (autre niveau).

Gestes et verre (17/11) :
- 7 gestes sur la piste Animation – Body de Gortash (N3a désigne un siège, N4 boit, N6c haussement d'épaules, N7 pas en avant, N8/N8D hochement, N9c hochement). Testés en jeu sauf N9c ; ils bouclaient : l'option « Continuous » est retirée par `build_pack.py`.
- Un verre (`CINE_DrinkWineGlassA_NotForDecoration`, ajouté comme acteur « template ») est accroché à `Dummy_R_Hand` de Gortash (Transform > Parent Point, `TargetId` = piste de Gortash) et n'est visible que de N4 à N6 (piste Show Actor). Pas encore vu en jeu.
- 17/11 après-midi : N4 et N7 filmés sur Gortash (on voit le verre). Trois caméras du modèle `Px1_Shipping` ajoutées dans le `.tml` (`cam_subject1_OTSMID_player` pour N3a, N5, N6a, N6c, N7 ; `cam_subject1_OTS_player` pour N9b, X1 ; `Q_cam_subject1_WIDEOTS_player` pour N1). Gestes ajoutés : révérence N9b (`Bows_Flourish_01`), porte X1 (`PointAreaBehind_RHand`), mains ouvertes N5 (`ShowHands_StandL_01_IN`), épaule N6a (`ShrugRight`), révérence légère N9a (`Bows_Shallow_01`). Pas encore vus en jeu.
- 17/11 : les plans de dos (OTS) rendaient mal en jeu. Les 8 répliques concernées (N1, N3a, N5, N6a, N6c, N7, N9b, X1) passent sur `cam_subject1_MCU`, le plan de face de Gortash. Le modèle `Px1_Shipping` n'a pas de plan de face plus large que celui-là.
- **Essai de bouche (17/11), sur N3a seulement** (« Someone with priorities… », handle `h923dd3e2…`). Le jeu range la bouche de chaque réplique doublée dans `Localization/English/Animation/FX_v<personnage>_<handle>.ffxanim`, et la relie au son par `Localization/English/Soundbanks/<personnage>.lsf` (fichier son, durée). Pour l'essai, on a copié dans le projet (`Mods/<mod>/Localization/English/`) la bouche d'une vraie réplique de Gortash de 6,5 s (`h003d96ac…`) sous notre handle, avec une entrée de son qui pointe vers un `.wem` qui n'existe pas. On cherche à savoir si la bouche bouge sans fichier son. Sinon, il faudra un `.wem` muet (fait avec Wwise). Résultat : **la bouche ne bouge pas sans son**.
- Essai 2 (d'après le guide du wiki BG3, « Adding New Voice Lines ») : la bouche démarre avec le son, et le mod doit aussi contenir les fichiers de visage du personnage (`Animation/FaceFXActors/<uuid>.ffxactor` et `.ffxbones`, copiés de ceux de Gortash). Ajout d'un `.wem` muet fait à la main (PCM 16 bits, 44,1 kHz, 6,5 s, à côté de la fiche dans `Soundbanks/`). Les voix du jeu sont en Vorbis, mais le PCM est lu : **la bouche bouge** (testé en jeu le 17/11).
- Étendu à toutes les répliques de Gortash (80, dans le bureau, le bal, la nuit, les souvenirs et après Orin) par `python tools/build_voice.py`, à relancer avant `build_pack.py` si les textes changent. Chaque réplique emprunte la bouche d'une vraie réplique de Gortash de durée proche. La plus longue du jeu fait 14 s : sur les répliques plus longues, la bouche s'arrête avant la fin.
- 17/11 : pas de « Continuer » sous N9a (« Il retourne votre main… ») : l'éditeur avait groupé N9a et N9a2 (GroupID), la timeline les jouait dans une seule phase et le jeu passait seul à N9a2. Groupe retiré du dialogue (`.lsj` et `.lsf`), `build_dialogs.py` ne garde plus les groupes, et la séquence est coupée en deux dans le `.tml` (« Sequence 3b - N9a2 »). À recompiler dans le Toolkit.
- 17/11 : quand il s'approche (N7, N8, N8D), plan `cam_subject1_OTSCLOSE_player` ajouté au `.tml` : Testé en jeu : on voit surtout le dos du joueur, refusé. N7, N8 et N8D repassent sur `cam_subject1_MCU` (de face). Tous les plans « par-dessus l'épaule » du modèle `Px1_Shipping` montrent trop le dos ; pour un vrai plan à deux, il faudrait notre propre caméra (copie du modèle avec une caméra déplacée).
- Essai de caméra sur mesure (17/11) : `GR_cam_TWOSHOT_side`, ajoutée dans `GR_Office_Evening_Scene.lsx` (bloc TLCameras, copié de `cam_subject1_OTSCLOSE_player`). Elle est accrochée au joueur, à 2,2 m sur le côté (2,6 au premier essai), à mi-chemin entre les deux, tournée de 90°, FoV 35, sans flou. Utilisée sur N7, N8 et N8D. Repère de la scène : chaque personnage regarde vers -z, l'autre est devant lui. Attention : un enregistrement de la timeline dans le Toolkit peut réécrire le `_Scene.lsx` et effacer cette caméra (sauvegarde : `before_twoshot_*` dans le scratchpad).
- Baisemain : l'animation de Wyll (`HoldHandKiss`) n'offre pour Gortash que la moitié « joueur » ; la moitié qui embrasse n'est pas proposée. Remplacé par une révérence légère.
- Pour les clés posées à la main, la tête de lecture de l'éditeur reste en fin de réplique : plus simple de les écrire dans le `.tml` (Toolkit avec la timeline fermée), puis rouvrir la timeline et l'enregistrer pour qu'il recompile.

- Le bureau est maintenant deux dialogues : `GR_Office_Invitation` (« ce soir / pas ce soir », en refermant la lettre) et `GR_Office_Evening` (la soirée, à partir de N1, avec sa timeline).
- `GR_Letters.txt` (région « Step 2 ») : après « ce soir », fondu au noir, Gortash est placé à son bureau et le groupe téléporté dans le bureau (point de téléportation de Larian), puis la soirée se joue. Ensuite, Gortash retourne au Bassin morphique s'il y était ; le groupe reste dans le bureau. Si la soirée ne peut pas démarrer, l'écran revient quand même.
- Corrigé par rapport au brouillon : `ScreenFadeDone` donne un numéro de joueur, pas un personnage.
- Testé en jeu le 17/11 (1.0.0.3) : fondu, téléportation et soirée avec timeline marchent. Mais le groupe entier arrivait à 34 m de Gortash (le point de test de Larian est à l'entrée de la zone du bureau). Depuis la 1.0.0.4 : le joueur arrive **seul, à côté de Gortash** ; depuis le camp, le groupe va d'abord à la Forteresse (écran de chargement), puis le joueur seul. Sécurité : si une téléportation ne finit pas, l'image revient au bout de 20 s.
- La pièce est bien son bureau selon Larian : les bustes sont les `S_WYR_GortashOfficeBustPlaque_*`. La salle du couronnement est une autre pièce (`CeremonyRoom`).
- Version du mod : **1.0.0.4**.
- À faire dans le Toolkit : enregistrer `GR_Office_Invitation` et `GR_Office_Evening`, **regénérer la timeline** de `GR_Office_Evening` (ses nœuds L0 à L3 sont partis), puis Build dans le StoryEditor.

Tester sur une sauvegarde de test (console), en remettant l'étape à zéro :

```lua
Osi.ClearFlag("GR_Office_Visited_94e19093-83bf-57a7-ba98-d02610e40e3e", Osi.GetHostCharacter())
```

```lua
Osi.DB_GR_OfficeVisited:Delete(1)
```

```lua
Osi.TemplateAddTo("GR_Letter_Invitation_04f0d615-092d-418a-95a4-358a2e3ea0c1", Osi.GetHostCharacter(), 1, 1)
```

Puis lire la lettre, la refermer, choisir « ce soir ».

## Points à trancher

- **Après Orin** : le script disait « la prochaine fois que le joueur parle à Gortash ». Ça demanderait d'intercepter son dialogue d'origine, donc la scène se lance au long repos. Du coup, la réplique sur le sang sur le tapis tombe un peu à côté : à réécrire si tu veux.
- Si Orin meurt avant la nuit privée, la scène ne se joue pas (elle est en « tu »).

- Les souvenirs se lancent juste après le long repos. Si le jeu joue déjà une scène à ce moment-là, le souvenir attend le repos suivant : à vérifier en jeu que ça ne tombe pas mal.

- Après la soirée au bureau mise en scène, le joueur reste dans le bureau. Le renvoyer au camp passe par la logique de la nuit au camp du jeu, ce qui risquerait de déclencher un repos.
- La scène du bal fait parler le héraut et les patriars par le narrateur. De vrais personnages demanderaient de les placer dans un niveau.

## 1.0.0.5 (17/11) : plus proches

- Le plan de côté marche en jeu (capture du 17/11). Mais ils étaient à 1,7 m : `TeleportTo` pose le joueur à côté de Gortash, pas tout près.
- `GR_Letters.txt` : après cette téléportation, le joueur est déplacé (`TeleportToPosition`) sur la ligne qui le relie à Gortash, à 65 % de la distance, soit environ 1,1 m. Les scènes de Larian placent les deux personnages à 1,2 m. Ensuite seulement, la soirée démarre (événement `GR_Office_PlayerCloser`). Si ça ne marche pas, le délai de 20 s rend quand même l'image.
- Caméra de côté rapprochée : 2,2 m au lieu de 2,6.
- Version **1.0.0.5** dans le `meta.lsx` : Build **5** dans le Multitool. Le script n'est pas recompilé dans le StoryEditor (Toolkit fermé), le jeu le compile au chargement.

## La nuit au bureau (recherche du 17/11, rien de changé)

- Le jeu change l'éclairage par script avec `TriggerSetLighting(zone, éclairage)` et `TriggerSetAtmosphere(zone, atmosphère)`, sur une zone d'éclairage (trigger `LTN_…` / `ATM_…`). C'est ce que font les camps de l'acte 3 la nuit.
- Éclairage et atmosphère de nuit du jeu, utilisés par le camp de la ferme (niveau BGO_Main_A) : `LTN_Default_Night_VUE_A` = `b3ca5158-0e0d-e7d0-a108-8cb4b985e331`, `ATM_Default_Night_VUE_A` = `1b400b27-513d-ebc0-a7d7-2e1872b56b91`.
- Problème : le niveau BGO_Main_A (dont la forteresse) n'a pas de zone d'éclairage. Il utilise l'éclairage du niveau (`meta.lsf` : LevelLighting `1986e8d8-…`, LevelAtmosphere `be77c334-…`). Il n'y a donc pas de zone à passer en nuit par script.
- Pistes : (1) ajouter notre propre zone d'éclairage autour du bureau dans le niveau (Toolkit, niveau de la ville), puis la passer en nuit par script pendant la soirée ; (2) plus simple, assombrir l'image dans la timeline (éclairage des personnages de nuit, exposition plus basse), mais les fenêtres resteraient claires.

## 1.0.0.6 (17/11) : la nuit et la main tendue

- **Nuit** : le mod ajoute deux zones au niveau de la ville (`Mods/<mod>/Levels/BGO_Main_A/Triggers/_merged.lsf`, copiées du format des zones `…_BGO_Visions` du jeu) : `GR_LTN_GortashOffice` (éclairage) et `GR_ATM_GortashOffice` (atmosphère). Ce sont des boîtes centrées sur la pièce principale du bureau (d'après `S_WYR_KillDirectorGortash_OfficeMainRoom`) : centre (-22,3 ; 75,1 ; 209,7), taille 28,7 × 8 × 26,5. Leur réglage normal est celui du niveau. `GR_Letters.txt` les passe en nuit au début du fondu (`PROC_GR_Office_Night`) et les remet en jour au nettoyage (`PROC_GR_Office_Day`, dans `PROC_GR_Office_Cleanup`). Pas testé : on ne sait pas encore si le jeu accepte une zone ajoutée par un mod, ni si la taille de boîte est la bonne (taille entière ou demi-taille).
- **Main tendue** : à la fin de N8 / N8D, juste avant « Prendre sa main », Gortash jouait `HUM_M_Rig_SCENE_UND_Automn_HoldHands_PLYR_IN` (7,4 s) : refusé en jeu (deux mains tendues vers la poitrine, puis figé à la fin car FadeOut 0). Remplacé par `HUM_M_Rig_CINE_StandL_handOutRight` (3 s, clé `1d625f7d-…`, une main), qui finit 0,4 s avant la fin de la réplique avec un fondu de 0,5 s. Trouvées dans `Shared.pak`, `Characters/Humans/[PAK]_Male_Cine`). Ajoutée dans le `.tml` et dans la timeline compilée. Pas encore vue en jeu.
- Version **1.0.0.6** : Build **6** dans le Multitool.

## Main tendue faite maison (17/11)

Notre propre animation, `GR_HandOffer` : Gortash tend la main droite vers le joueur, paume vers le haut, et la garde tendue en respirant pendant le choix « Prendre sa main ».

- Dossier de travail : `C:\Users\obell\Desktop\GortashAnim` (`GR_HandOffer.blend`, sources extraites du jeu, exports, aperçus).
- Outils : Blender 5.3 et LSLib (`C:\Users\obell\Desktop\Packed`). `Divine.exe` est dans `Packed\Tools` et a besoin de `granny2.dll`, qui est à la racine de `Packed` : une copie est mise dans `Tools`.
- Lire un `.GR2` du jeu : `Divine.exe -g bg3 -a convert-model -s X.GR2 -d X.glb`. Pour une animation, ajouter `-e conform --conform-path HUM_M_Base.GR2` (le squelette).
- Fabriquer l'animation (scripts dans `tools/anim/`, à lancer avec `blender -b --python`) :
  - `build_scene.py` : corps + squelette animé par la respiration au repos (`HUM_M_Rig_CINE_Still_Breathing_Idle_StandL_01`) ;
  - `pose.py` : place le poignet droit sur une cible devant lui (épaule et coude calculés), paume vers le haut ;
  - `export.py` : deux actions, `GR_HandOffer_IN` (1,5 s, la main monte) et `GR_HandOffer_LOOP` (11,5 s, respiration, bras tenu), exportées en `.glb` ;
  - `verify.py` : aperçus après aller-retour.
- Repasser en `.GR2` : l'export de Blender perd une fiche dont LSLib a besoin. `python tools/anim/fix_glb.py <un .glb fait par LSLib> <exports>`, puis `Divine.exe -g bg3 -a convert-model -s X.glb -d X.GR2`.
- Dans le mod :
  - les `.GR2` sont dans `Public/<mod>/Assets/Animations/` ;
  - une fiche d'animation par fichier dans `Public/<mod>/Content/Assets/[PAK]_GR_Animations/<id>.lsf`, copiée de `HUM_M_Rig_CINE_StandL_handOutRight` ;
  - id `GR_HandOffer_IN` = `504eb042-…`, `GR_HandOffer_LOOP` = `3edd2852-…`.
- Timeline : à la fin de N8 et de N8D, `IN` joue de -2,5 s à -1 s, puis `LOOP` de -1 s à la fin, en boucle (`Continuous` gardé : `build_pack.py` ne le retire plus pour cette animation). La timeline désigne directement l'id de la fiche : à vérifier en jeu que ça suffit (les gestes du jeu passent par une table de correspondance par squelette).
- Testé en jeu le 17/11 : la timeline accepte bien l'id de la fiche, l'animation joue. Mais première version pas naturelle : bras presque tendu à fond (cible trop loin pour un bras de 0,29 + 0,26 m), main raide.
- Version 2 (`tools/anim/make_handoffer.py`, remplace `build_scene.py`, `pose.py`, `export.py`) : coude près du corps et avant-bras vers l'avant (poignet à 25 cm devant, 1,15 m de haut), coude descendu au plus bas, paume vers le haut et un peu tournée vers le joueur, montée en 1,25 s qui ralentit à l'arrivée (le coude part avant le poignet), puis bras qui oscille très légèrement et doigts un peu plus ouverts. Aperçus `v2_*.png` dans le dossier GortashAnim. Pas encore vue en jeu.

## 1.0.0.7 (17/11) : l'arrivée par les portes

- Après « ce soir » et le fondu, le joueur est posé dans le couloir devant les portes du bureau : (16,96 ; 73,01 ; 210,02), position relevée en jeu avec `Osi.GetPosition`. L'image revient. Il marche (`PROC_CharacterMoveTo`, « Walk ») jusqu'à Gortash, puis fait quelques pas de plus (`CharacterMoveToPosition`) s'il est à plus de 1,4 m, jusqu'à 65 % de la distance. La soirée démarre à l'arrivée.
- La porte n'a pas été trouvée dans les fichiers (sous-niveau) ni par la console. On compte sur le jeu, qui ouvre les portes non verrouillées sur le chemin. Pas d'animation « pousser les portes » : à ajouter à la liste des animations.
- Sécurités : le délai de 20 s ne coupe plus la marche (`DB_GR_Office_Walking`). Si la marche ne finit pas en 90 s (le joueur clique ailleurs, chemin bloqué), la soirée démarre là où il est.
- La zone de nuit est élargie jusqu'aux portes : x de -36,6 à 19, centre -8,8, taille 55,6 × 8 × 26,5.
- Version **1.0.0.7** : Build **7**. Pas encore testé.

## Cinématique d'arrivée (en cours, 17/11)

- Nouveau dialogue `GR_Office_Arrival` (ressource `0620d73a-…`), une seule ligne du narrateur `A0` : « Vous poussez les portes. Au fond de la pièce, près de son bureau, Gortash vous attend. » Défini dans `staged_office()` de `build_dialogs.py`, texte dans `Dialogs/GR_Office_Evening.md`.
- Testé le 17/11 (1.0.0.7, marche à pied depuis le couloir) : devant les portes, la Garde d'acier lance un combat. Abandonné : le joueur est de nouveau placé à côté de Gortash (à environ 1,1 m), là où il n'y a pas de combat, et seule la cinématique montre l'entrée par les portes (la timeline déplace son image, pas le vrai personnage).
- `GR_Letters.txt` : une fois les deux en place, `PROC_GR_Office_TryStartArrival` lance `GR_Office_Arrival` et l'image revient ; à sa fin, la soirée. Si la cinématique ne démarre pas, la soirée démarre directement.
- 17/11 soir : la timeline est générée (une seule séquence de 13,6 s : A0 puis AG, la réplique de Gortash « Vous voilà. Je commençais à me poser des questions. », ajoutée parce que le générateur ne trouvait aucun personnage avec le narrateur seul). `python tools/anim/arrival_walk.py` ajoute dans la timeline compilée : la marche (`CINE_StandL_ToWalk_01`, `CINE_Walk_01` en boucle, `CINE_Walk_ToStandL_01`) et un déplacement du joueur attaché à Gortash (comme le verre), tourné vers lui, de 8 m à 1,1 m devant lui en 7,6 s. Le premier plan (`cam_player_MCU`) est attaché au joueur et le suit. À relancer après chaque enregistrement de cette timeline dans le Toolkit. Version 1.0.0.8, pas encore testé.
- Inconnues du premier essai : le sens de l'axe « devant Gortash » (s'il arrive de derrière lui, inverser le signe), la vitesse (pieds qui glissent ?), un mur ou un meuble sur le trajet.
- Reste à faire (ancien plan) :
  - dans le Toolkit, enregistrer `GR_Office_Arrival` puis générer sa timeline (Full, Custom `bnz_standing_Px1_Shipping.lsf`) ;
  - y mettre les animations de marche du jeu (`HUM_M_Rig_DFLT_CINE_StandL_ToWalk_01`, `..._Walk_01` en boucle, `..._Walk_ToStandL_01`), le déplacement (TLTransform : Larian déplace les personnages dans l'espace de la scène, origine à découvrir par un essai) et les plans ;
  - la porte : la timeline peut la cacher par un plan qui commence juste après qu'elle s'ouvre, ou il faudra la trouver pour l'ouvrir par script (`Open`).

### Réglage de la cinématique dans le Toolkit (18/11)

- Charger le niveau `BGO_Main_A` (« Wyrm's Crossing ») dans le Toolkit, ouvrir la timeline, puis dans la fenêtre « Timeline Preview » : Preview Options > Location > filtre « Gortash_OfficePos » > double-clic sur `S_WYR_Gortash_OfficePos`. L'aperçu se joue alors dans le vrai bureau.
- La liste des lieux montre `GR_LTN_GortashOffice` et `GR_ATM_GortashOffice` : le Toolkit (et donc le jeu) charge bien les zones de nuit ajoutées par le mod.
- Dans la scène, Gortash est en (0 ; 0 ; -0,832), tourné de 180°. Devant lui, c'est **-Z** dans son repère : le premier essai (+Z) mettait le joueur derrière lui.
- Les rotations des clés du `.tml` sont en **radians** : « 0; 180; 0 » tournait le joueur de 180 radians. Utiliser 3,14159.
- `tools/anim/arrival_walk_tml.py` écrit la marche dans le `.tml` (timeline fermée dans le Toolkit), corrigé avec ces deux points. Pas encore revu en aperçu.
- Le Toolkit avec la ville chargée monte à 96 % de mémoire et a planté en rouvrant la timeline. Fermer les autres programmes avant.
- Le Toolkit cherche aussi un `MC_…GR2` (mouvement du corps) pour les répliques doublées : message « Could not read granny file … MC_vb878a854… » pour la réplique AG. Sans conséquence connue pour l'instant.

### Cinématique d'arrivée réglée en aperçu (18/11, version 1.0.0.9)

- Réglée dans le Toolkit avec la ville chargée. Ton personnage part à 3,3 m devant Gortash : à 8 m puis 4,5 m, il sortait d'un mur. Il se met en marche, marche, s'arrête à 1,1 m de lui en 4,4 s. Le premier plan est `cam_player_OTS_subject1` (derrière l'épaule de Gortash, tourné vers le joueur). Les trois figurants du modèle de scène sont retirés (template vidé). Le gros plan de Gortash sur sa réplique est gardé.
- Les temps des clés `ΔTime` du `.tml` sont des temps **absolus** dans la séquence. Lus comme des écarts, ils faisaient faire des allers-retours au personnage.
- Méthode : `tools/anim/arrival_walk_tml.py`, puis `tools/anim/arrival_cams_tml.py`, sur une copie de la timeline générée, avec la timeline fermée dans le Toolkit. On la rouvre, puis Timeline Panel > Ctrl+S. Le Toolkit recompile le `.lsf`, parfois avec une minute de retard. `tools/anim/arrival_walk.py` (qui écrit dans le `.lsf` compilé) n'est plus nécessaire : ne pas le relancer sur un `.lsf` déjà compilé par le Toolkit, sinon la marche est en double.
- Fondu au noir de 0,3 s entre la cinématique et la soirée (`GR_Office_ArrivalCut`), pour cacher l'interface qui réapparaissait.
- À tester en jeu.

### Arrivée en deux plans (18/11)

- L'entrée : d'abord placée à 34 m (point de test de Larian), mais en jeu ce point est dehors. La pièce (`S_WYR_KillDirectorGortash_OfficeMainRoom`) s'arrête à environ 18 m devant Gortash : entrée replacée à (-1,9 ; -17,8) dans son repère, le 18/11. La zone de nuit marche : le ciel vu dehors était de nuit. Données du niveau : `S_WYR_Gortash_OfficePos`, qui est aussi le `S_WYR_GortashsPositionInOffice` du script, et le point d'entrée `S_Debug_Teleport_WYR_GortashsOffice`.
- `tools/anim/arrival_scene_tml.py` construit toute la cinématique à partir de `tools/anim/GR_Office_Arrival.generated.tml`, la timeline telle que le générateur l'a faite :
  - plan 1 (0 à 3,95 s), caméra `GR_cam_door` : une caméra du modèle de scène, déplacée par un Transform attaché à Gortash (ça marche), placée dans la pièce et tournée vers la porte. Le joueur entre et fait trois pas ;
  - coupe ;
  - plan 2 : `cam_player_OTS_subject1`, les derniers pas de 3,3 m à 1,1 m ;
  - puis le gros plan de Gortash.
- **L'aperçu du Toolkit tourne Gortash autrement que le jeu** (à vérifier) : dans l'aperçu, « devant lui » donne sur le fond de la pièce et ses murs, et l'entrée tombe dehors. Dans le jeu, `LookFromTrigger` le tourne face à l'entrée. À tester en jeu avant de régler autre chose.
- Pour rouvrir une timeline quand la fenêtre du dialogue est réduite : ouvrir le dialogue en lecture seule (« Oui ») puis Ctrl+T. Ctrl+S dans le Timeline Panel compile quand même.


## Prise de main (18/11)

Quand le joueur choisit C1 « Prendre sa main », la joueuse pose sa main dans celle de Gortash et ils la tiennent.

- Fichier Blender : `GortashAnim\GR_HandAccept.blend`. Il contient aussi IN et LOOP corrigés : le poignet de Gortash n'est plus tordu, la torsion est répartie sur `Elbow_Twist_R`.
- Animations dans `Public/<mod>/Assets/Animations/` :
  - `GR_HandOffer_IN` (1,5 s) et `GR_HandOffer_LOOP` (4 s), remplacées ;
  - nouvelles, 3 s chacune : `GR_HandAccept_Gortash` (HUM_M) et `GR_HandAccept_Joueuse` (HUM_F).
- Fiches d'animation dans `[PAK]_GR_Animations` :
  - `GR_HandAccept_Gortash` = `561ba179-…` ;
  - `GR_HandAccept_Joueuse` = `b1f70ade-…`, squelette HUM_F `edda91cd-d2be-3296-087c-45477f36daaa`.
- Timeline `GR_Office_Evening`, phase N9a (début à 13,92 s) :
  - les deux animations jouent de 13,92 à 16,92 s ;
  - le geste qui était déjà là sur Gortash (`85cc45da-…`) est décalé à 16,92–22,92 s ;
  - sauvegarde de la timeline d'avant dans `GortashAnim\backup_mod\`.
- À vérifier en jeu :
  - Position : dans Blender, la joueuse est à 0,68 m devant Gortash, décalée de 0,12 m vers sa main droite. En jeu, elle est à environ 1,1 m, donc les mains ne se toucheront sans doute pas tant qu'on ne la rapproche pas dans la scène.
  - Type de corps : l'animation de la joueuse est faite pour HUM_F. Sur un autre type de corps, le jeu ne la jouera probablement pas correctement.
  - Fin des 3 s : on ne sait pas encore ce que font les personnages à la fin de l'animation.
- Version **non incrémentée** : `build_pack.py` a été relancé, le dossier `build/` est prêt à packer.


## Baisemain (18/11)

Juste après la prise de main (choix C1, phase N9a), Gortash lève la main de la joueuse, s'incline et embrasse le dos de sa main, puis se redresse.

- Fichier Blender : `GortashAnim\GR_HandAccept.blend`. Les actions de travail `HK_base_G` et `HK_base_F` servent de base, elles ne sont pas exportées.
- Animations (4 s, 96 frames à 24 images/s), qui commencent exactement sur la dernière pose de la prise de main :
  - `GR_HandKiss_Gortash` : la main monte (frames 6 à 28), il s'incline de 62° depuis le dos (10 à 34), les lèvres touchent la main (36 à 56), il se redresse (58 à 80), puis il revient à la pose de départ.
  - `GR_HandKiss_Joueuse` : son bras suit, la main reste dans celle de Gortash.
- Fiches d'animation :
  - `GR_HandKiss_Gortash` = `8357d7d4-…` ;
  - `GR_HandKiss_Joueuse` = `80c04527-…` (squelette HUM_F).
- Timeline `GR_Office_Evening`, phase N9a :
  - le baisemain joue de 16,92 à 20,92 s, juste après la prise de main (13,92 à 16,92 s) ;
  - le geste vanilla de Gortash (`85cc45da-…`) est décalé à 20,92–26,92 s ;
  - sauvegarde de la timeline d'avant dans `GortashAnim\backup_mod\`.
- Vérifications dans Blender :
  - aucune traversée (moins de 0,4 cm sur les corps simplifiés) ;
  - lèvres au contact de la main entre les frames 36 et 56 ;
  - tête à environ 13 cm du buste de la joueuse ;
  - pieds fixes (moins de 1 cm) ;
  - mouvement fluide, sans à-coup ;
  - torsion des avant-bras répartie.
- Texte de N9a adapté le 20/11 à l'animation : « Il lève votre main et s'incline dessus, sans hâte, jusqu'à poser ses lèvres sur le dos de vos doigts… » (avant : « au creux de votre poignet »).

### 19/11 soir : corrections après le test en jeu (vidéo 21h52)

- Mains : `GortashAnim\hands_contact.py` (à lancer dans `GR_HandAccept.blend`) refait les 4 animations de prise de main et de baisemain à partir des actions `*_AVANT_MAINS`. Doigts détendus, main de la joueuse posée sur la paume de Gortash sans traversée des maillages.
- Baisemain : Gortash ne garde que 75 % de sa courbure (`BOW_KEEP`). Sa bouche remonte d'environ 12 cm et la main de la joueuse monte avec (environ 1,43 m). Son corps n'avance pas (`BOW_FORWARD` = 0) : avec 6 cm d'avancée, le bras de la joueuse se repliait (coude à 64°, poignet à 77°). Sans avancée, le bras est presque tendu (coude à 37°, poignet à 61°). Pas encore vu en jeu.
- Avant-bras de la joueuse : l'os `Elbow_Twist_L` prend toute la rotation de la main, comme dans les animations du jeu. Avant, il en prenait 27° sur 68° pendant la prise de main, ce qui pinçait l'avant-bras.
- Détour du bras au début de la prise de main réduit (`APPROACH_BACK` 0,15 → 0,05 m).
- Timeline (`tools/anim/evening_hands.py`) :
  - geste vanilla `85cc45da-…` après le baisemain (la « révérence ») retiré ;
  - fondu de fin du baisemain : 1 s au lieu de 0,3 s ;
  - la joueuse est placée devant Gortash dès N6a, N6c et N6d (gros plans de Gortash), pour éviter le saut au début de N7. N6b n'est pas traité (autre caméra, `9b704794`).
- Main tendue : le bras retombait un instant environ 1 s après le début du geste. `GR_HandOffer_IN` s'effaçait en 0,3 s et `GR_HandOffer_LOOP` mettait 0,3 s à apparaître, donc la pose de repos revenait entre les deux. Les deux fondus sont à 0 (les poses se raccordent à moins de 2° près), réglés dans `evening_hands.py`.
- N7 réécrite (il ne s'avance plus) : « Il repose son verre. Vous êtes à présent assez près pour que… ». Le texte anglais du projet Toolkit est l'ancien : à recoller depuis `Toolkit/texts_to_paste.md` si la ligne est réimportée.
