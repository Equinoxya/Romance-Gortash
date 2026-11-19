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
- EN: Letter Sealed with the Archduke's Crest
- FR: Lettre scellée aux armes de l'Archiduc

**LETTER1_DESC - Item description**
- EN: Heavy paper, black wax, and a faint trace of machine oil. Someone left it at camp while no one was looking.
- FR: Papier épais, cire noire et légère odeur d'huile de machine. Quelqu'un l'a déposée au camp sans se faire remarquer.

**LETTER1_TEXT - Item content**
- EN: To the hero of the hour,<br><br>Baldur's Gate has a new Archduke, and you had the good taste to attend the occasion. I noticed. I notice most things.<br><br>Ceremony, however, is a poor setting for honest conversation: too many ears, too much applause. I would rather speak with you the way I prefer to do business - privately, and without an audience.<br><br>Come to my office at Wyrm's Rock after dusk. The Steel Watch will be told to expect you. They will not trouble you, provided you do not trouble them.<br><br>Bring your wits. Leave your companions. I promise the wine will be better than whatever you have been drinking in that camp of yours.<br><br>Lord Enver Gortash<br>Archduke of Baldur's Gate<br><br>P.S. Do not mistake this for a summons. I write those in a different hand. This is an invitation, and I extend very few.
- FR: [Au héros du moment, / À l'héroïne du moment, / À la célébrité du moment,]<br><br>La Porte de Baldur a un nouvel Archiduc, et vous avez eu le bon goût d'assister à l'événement. Je l'ai remarqué. Je remarque presque tout.<br><br>Une cérémonie se prête toutefois mal aux conversations sincères : trop d'oreilles, trop d'applaudissements. Je préfère vous parler comme je traite mes affaires - en privé, et sans public.<br><br>Venez à mon bureau de la Forteresse du roc du dracosir après le crépuscule. La Garde d'Acier sera prévenue de votre visite. Elle ne vous importunera pas, tant que vous ne l'importunez pas.<br><br>Apportez votre esprit. Laissez vos compagnons. Je vous promets un vin meilleur que tout ce que vous buvez dans votre campement.<br><br>Seigneur Enver Gortash<br>Archiduc de la Porte de Baldur<br><br>P.S. Ne prenez pas ceci pour une convocation. Je les rédige d'une autre main. Ceci est une invitation, et j'en accorde très peu.

## Open points

- Decided: three letter items, one per identity. `tools/build_toolkit.py` writes the books `GR_Letter_Invitation_M/F/NB` and the items `GR_Letter_Invitation` (M, made in the Toolkit), `GR_Letter_Invitation_F` and `GR_Letter_Invitation_NB` (inherit from it). `GR_Letters.txt` gives the one that matches the player's identity.
