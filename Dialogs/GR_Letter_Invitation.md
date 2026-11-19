# Step 1 - Invitation letter

Text of the first letter. Notation is explained in the README.

## How it starts

- The coronation scene is over.
- At the next long rest, the letter is added to the player's inventory (`Story/RawFiles/Goals/GR_Letters.txt`).

## Flags

| Flag | Set by | Meaning |
|---|---|---|
| `GR_Letter1_Delivered` | letter delivered | Unlocks the office scene (step 2) |

---

## Letter

**LETTER1_NAME - Item name**
- EN: Letter Sealed in Black Wax
- FR: Lettre au sceau de cire noire

**LETTER1_DESC - Item description**
- EN: Heavy paper, black wax pressed with the Archduke's crest, and a faint trace of machine oil. No one at camp saw who left it.
- FR: Papier épais, cire noire frappée aux armes de l'Archiduc, et une légère odeur d'huile de machine. Personne au camp n'a vu qui l'a déposée.

**LETTER1_TEXT - Item content**
- EN: At the coronation, I spent more time watching you than the crowd. I notice most things. I rarely write to them.<br><br>My office, at Wyrm's Rock. After dark. Come alone - the Watch will let you pass.<br><br>No ceremony, no audience. Only the two of us, and a wine far better than your camp deserves.<br><br>E.<br><br>P.S. Burn this, or keep it. I am curious which.
- FR: Au couronnement, j'ai passé plus de temps à vous regarder qu'à regarder la foule. Je remarque presque tout. J'écris rarement à ce que je remarque.<br><br>Mon bureau, à la Forteresse du roc du dracosir. Après la tombée de la nuit. Venez [seul / seule / sans escorte] : la Garde vous laissera passer.<br><br>Ni cérémonie, ni public. Rien que nous deux, et un vin bien meilleur que ce que mérite votre campement.<br><br>E.<br><br>P.S. Brûlez cette lettre, ou gardez-la. Je suis curieux de savoir ce que vous choisirez.

## Open points

- Decided: three letter items, one per identity. `tools/build_toolkit.py` writes the books `GR_Letter_Invitation_M/F/NB` and the items `GR_Letter_Invitation` (M, made in the Toolkit), `GR_Letter_Invitation_F` and `GR_Letter_Invitation_NB` (inherit from it). `GR_Letters.txt` gives the one that matches the player's identity.
