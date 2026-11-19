# Extension - Ambient greetings

One-line greetings Gortash uses when the player talks to him between scenes. Notation is explained in the README.

## How it works

- Add these as alternative opening lines in Gortash's existing dialogue at Wyrm's Rock.
- Only one plays, chosen by the flags below. If none applies, his base game greeting plays.
- French follows the rule of the mod: "vous" until the private night, "tu" after it.

| Line | Shown when |
|---|---|
| `G1`, `G1D` | `GR_Romance_Interested`, before the ball |
| `G2` | `GR_Ball_Danced`, before the private night |
| `G2b` | `GR_Ball_Attended` without `GR_Ball_Danced`, before the private night |
| `G3`, `G3D` | `GR_Romance_Committed` |
| `G4` | `GR_Romance_Declined` |
| `G5` | `GR_Romance_Ended` |

---

**G1 - Gortash** `[Tav]`
- EN: Back so soon? Careful. People will say the Archduke has a favourite, and I shall have to stop denying it.
- FR: Déjà de retour ? Prenez garde. On dira que l'Archiduc a une préférence, et je devrai cesser de le nier.

**G1D - Gortash** `[Durge]`
- EN: Every time you walk through that door, I count it as something stolen back. Do keep walking through it.
- FR: Chaque fois que vous franchissez cette porte, je compte cela comme un vol réparé. Continuez de la franchir.

**G2 - Gortash**
- EN: My tailors are still recovering. So, I confess, am I.
- FR: Mes tailleurs ne s'en sont pas encore remis. Moi non plus, je l'avoue.

**G2b - Gortash**
- EN: You still owe me a dance. I am keeping the debt on my books, with interest.
- FR: Vous me devez toujours une danse. Je garde la créance dans mes livres, avec les intérêts.

**G3 - Gortash** `[Tav]`
- EN: There you are. I was halfway through a death warrant, and it has lost all interest.
- FR: Te voilà. J'étais au milieu d'un arrêt de mort, et il a perdu tout intérêt.

**G3D - Gortash** `[Durge]`
- EN: Come in. Close the door. Let the city wait. It has had me for years, and you were gone for most of them.
- FR: Entre. Ferme la porte. Que la ville attende. Elle m'a eu pendant des années, et tu n'étais pas là pour la plupart.

**G4 - Gortash**
- EN: Ally. Strictly business, as agreed. You will notice I am being impeccably well behaved.
- FR: [Cher allié. / Chère alliée. / Vous voilà.] Les affaires, rien que les affaires, comme convenu. Vous remarquerez que ma conduite est irréprochable.

**G5 - Gortash**
- EN: You have business with the Archduke, I assume. He is the only one of us still receiving you.
- FR: Vous venez voir l'Archiduc, je suppose. Il est le seul de nous deux à vous recevoir encore.
