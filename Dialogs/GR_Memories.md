# Extension - Memories of the Dark Urge

Three short memories that come back to the Dark Urge in their sleep. Notation is explained in the README.

## How it works

- Dark Urge only. Each memory is a short narrated scene played during a long rest, after one step of the romance.
- In the memories, Gortash says "tu": this is how they spoke before the base game. The narrator says "vous".

| Memory | Plays at the first long rest after | Flag set |
|---|---|---|
| First meeting | `GR_Office_Visited` with `GR_Romance_Interested` | `GR_Memory1_Seen` |
| The rooftop | `GR_Ball_Attended` | `GR_Memory2_Seen` |
| The last morning | `GR_Romance_Committed` | `GR_Memory3_Seen` |

---

## First meeting

**M1a - Narrator**
- EN: Sleep brings something that is not quite a dream. A counting-house cellar, a single lamp. A young man in a patched coat is explaining, with total confidence, how he intends to rob a devil.
- FR: Le sommeil vous apporte quelque chose qui n'est pas tout à fait un rêve. La cave d'un comptoir, une seule lampe. Un jeune homme au manteau rapiécé explique, avec une assurance totale, comment il compte voler un diable.

**M1b - Gortash**
- EN: You are the only person I have ever met who heard that plan and asked "when", instead of "why".
- FR: Tu es la seule personne que j'aie jamais rencontrée qui, en entendant ce plan, ait demandé « quand » au lieu de « pourquoi ».

**M1c - Narrator**
- EN: You remember laughing. You remember the look on his face, as if the sound were worth more than the crown he was planning to steal.
- FR: Vous vous souvenez d'avoir ri. Vous vous souvenez de son regard, comme si ce rire valait plus que la couronne qu'il projetait de voler.

## The rooftop

**M2a - Narrator**
- EN: Another night comes back to you. A rooftop above the Lower City, blood drying on your hands, and him beside you, entirely unafraid.
- FR: Une autre nuit vous revient. Un toit au-dessus de la Ville Basse, le sang qui sèche sur vos mains, et lui à vos côtés, sans la moindre peur.

**M2b - Gortash**
- EN: Everyone else flinches when you come back like this. I find I only want to know whether you are in pain.
- FR: Tous les autres reculent quand tu reviens dans cet état. Moi, je veux seulement savoir si tu as mal.

**M2c - Narrator**
- EN: No one had ever asked you that. You did not know what to answer, so you kissed him.
- FR: Personne ne vous l'avait jamais demandé. Faute de savoir quoi répondre, vous l'avez embrassé.

## The last morning

**M3a - Narrator**
- EN: The last memory is the clearest. A grey morning. He is fastening the gauntlet, already late, already half an Archduke in his own head.
- FR: Le dernier souvenir est le plus net. Un matin gris. Il boucle son gantelet, déjà en retard, déjà à moitié Archiduc dans sa tête.

**M3b - Gortash**
- EN: Tonight, when this is done, I have something to say to you. It will keep until then.
- FR: Ce soir, quand tout sera réglé, j'aurai quelque chose à te dire. Cela peut attendre jusque-là.

**M3c - Narrator**
- EN: It did not keep. That afternoon, Orin reached you first. You wake with the taste of blood in your mouth, and the certainty that you know, now, what he meant to say.
- FR: Cela n'a pas attendu. L'après-midi même, Orin est arrivée avant lui. Vous vous éveillez avec un goût de sang dans la bouche, et la certitude de savoir, à présent, ce qu'il voulait vous dire.

## Open points

- Wired in `GR_Letters.txt` (region "Dark Urge memories"): each memory starts with `QRY_StartDialog` when the long rest ends, one per rest, oldest first. If it cannot start, it waits for the next rest. Generated as `GR_Memory_FirstMeeting`, `GR_Memory_Rooftop` and `GR_Memory_LastMorning` by `tools/build_dialogs.py`. Not played yet.
- The first memory refers to the theft of the Crown of Karsus. Check the details against what the base game says about it.
