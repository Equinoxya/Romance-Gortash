# Extension - After Orin

Gortash's reaction once Orin is dead. Notation is explained in the README.

## How it starts

- Requires: Orin dies after `GR_Romance_Committed` is set, and `GR_Romance_Ended` is not set. Orin's death is the global flag `GLO_Orin_State_PermaDefeated`.
- Plays at the first long rest after her death, started by `GR_Letters.txt` like the other scenes. Starting it the next time the player talks to Gortash would mean intercepting his own dialogue: not done.
- French uses "tu": the scene requires the private night.
- For the Dark Urge, the scene depends on what happened in Bhaal's temple. This is also where a Dark Urge who rejected Bhaal gets their own lines.

## Extra conditions

- `[Durge, rejected Bhaal]`: global flag `ORI_DarkUrge_State_BhaalResisted`.
- `[Durge, accepted Bhaal]`: global flag `ORI_DarkUrge_State_BhaalAccepted`.
- `OD3` has no condition, so a Dark Urge always has an answer.

## Flags

| Flag | Set by | Meaning |
|---|---|---|
| `GR_Orin_Done` | start of the scene | The scene cannot be replayed |

---

## Tav

**O1 - Gortash** `[Tav]`
- EN: Orin is dead. I had the news before you reached the street. Sit down, you are bleeding on a carpet I am fond of. And let me look at you.
- FR: Orin est morte. Je l'ai su avant que tu n'atteignes la rue. Assieds-toi, tu saignes sur un tapis auquel je tiens. Et laisse-moi te regarder.

| Id | EN | FR | Goes to |
|---|---|---|---|
| OA1 | Worried about me, Enver? | Tu t'inquiétais pour moi, Enver ? | O2a |
| OA2 | It's done. Her stone is ours. | C'est fait. Sa pierre est à nous. | O2b |

**O2a - Gortash**
- EN: Appalled by the possibility. Do not make me say it again.
- FR: Consterné par cette éventualité. Ne m'oblige pas à le redire.

**O2b - Gortash**
- EN: Ours. I notice the word did not make me flinch. Extraordinary.
- FR: À nous. Je remarque que le mot ne m'a pas fait tressaillir. Extraordinaire.

## Dark Urge

**O1D - Narrator** `[Durge]`
- EN: He is on his feet before the door has closed. For once, he has no remark prepared.
- FR: Il est debout avant que la porte ne se referme. Pour une fois, il n'a aucune remarque de prête.

**O2D - Gortash** `[Durge]`
- EN: She took you from me with a knife in the dark. Tell me she saw it coming this time. Tell me she knew it was you.
- FR: Elle m'a privé de toi, d'un coup de lame dans le noir. Dis-moi que cette fois, elle l'a vu venir. Dis-moi qu'elle savait que c'était toi.

| Id | Condition | EN | FR | Goes to |
|---|---|---|---|---|
| OD1 | `[Durge, rejected Bhaal]` | Orin is dead. So is Bhaal's claim on me. I refused him. | Orin est morte. Et Bhaal n'a plus aucun droit sur moi. Je lui ai dit non. | O3r |
| OD2 | `[Durge, accepted Bhaal]` | Orin is dead. I am my father's Chosen now. | Orin est morte. C'est moi que mon père a choisi, désormais. | O3a |
| OD3 | `[Durge]` | She knew. | Elle le savait. | O3k |

**O3r - Gortash** `[Durge, rejected Bhaal]`
- EN: You refused a god. Your own father. And you walked out of his temple on your own feet. For years I shared you with a voice in your blood and never resented it, because it came with you. Until this moment, I did not know how much I wanted you without it.
- FR: Tu as dit non à un dieu. À ton propre père. Et tu as quitté son temple sur tes deux jambes. Pendant des années, j'ai dû te partager avec une voix dans ton sang, sans jamais lui en vouloir, puisqu'elle venait avec toi. J'ignorais, jusqu'à cet instant, à quel point je te voulais sans elle.

**O4r - Narrator** `[Durge, rejected Bhaal]`
- EN: He takes your face in both hands, as if checking that all of you came back.
- FR: Il prend votre visage entre ses mains, comme pour vérifier que rien de vous ne manque.

**O3a - Gortash** `[Durge, accepted Bhaal]`
- EN: Then Bhaal has his Chosen and Bane has his, and they are standing in the same room, entirely on the same side. The gods must be furious. Come here.
- FR: Alors Bhaal a [son Élu / son Élue / choisi quelqu'un] et Bane a le sien, et les deux se tiennent dans la même pièce, résolument du même côté. Les dieux doivent être furieux. Viens là.

**O4a - Narrator** `[Durge, accepted Bhaal]`
- EN: He kisses you without flinching from what you are now. He never has.
- FR: Il vous embrasse sans reculer devant ce que vous êtes à présent. Il n'a jamais reculé.

**O3k - Gortash** `[Durge]`
- EN: Good. Good. Then I can stop imagining it differently every night.
- FR: Bien. Bien. Alors je peux cesser de l'imaginer autrement chaque nuit.

## Open points

- Generated as `GR_Orin` by `tools/build_dialogs.py` (15 nodes, two start nodes: `O1D` for the Dark Urge, `O1` for Tav). Not played yet.
- `O1` mentions blood on the carpet, written for a scene right after the fight. At a long rest it may read oddly.

- If Orin dies before the private night, this scene never plays. A "vous" version would be needed to cover that order.
- `O3a` treats Gortash as Bane's Chosen, as in the base game.
