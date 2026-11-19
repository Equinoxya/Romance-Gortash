# Extension - Jealousy

Gortash asks where he stands if the player already has another romance. Notation is explained in the README.

## How it starts

- Requires: `GR_Ball_Attended`, `GR_Romance_Ended` not set, the private night not played yet, and the player in a romance with a companion (base game flag, to look up).
- Plays the next time the player talks to Gortash, before his usual dialogue.
- French uses "vous": the scene happens before the private night.

## Flags

| Flag | Set by | Meaning |
|---|---|---|
| `GR_Jealousy_Done` | start of the scene | The scene cannot be replayed |
| `GR_Exclusive_Promised` | `JA1` | The player promised to end the other romance |

---

**J1 - Gortash**
- EN: A question, before this goes any further. My informants tell me your bedroll is not always empty. I do not ask who. I ask whether I am an appointment or an exception.
- FR: Une question, avant que ceci n'aille plus loin. Mes informateurs m'assurent que votre couche n'est pas toujours vide. Je ne demande pas qui. Je demande si je suis un rendez-vous ou une exception.

## Choice JA

| Id | EN | FR | Sets flag | Goes to |
|---|---|---|---|---|
| JA1 | You're the exception. I'll end the other. | Vous êtes l'exception. Je mettrai fin à l'autre. | `GR_Exclusive_Promised` | J2a |
| JA2 | I don't belong to anyone, Gortash. Not even you. | Je n'appartiens à personne, Gortash. Pas même à vous. | | J2b |
| JA3 | You have spies in my camp? | Vous avez des espions dans mon camp ? | | J2c |
| JA4 | Does it matter to you that much? | Cela compte à ce point, pour vous ? | | J2d |

**J2a - Gortash**
- EN: I shall hold you to that. I am told I am unbearable when I hold people to things.
- FR: Je vous prendrai au mot. Il paraît que je suis insupportable quand je prends les gens au mot.

End of dialogue.

**J2b - Gortash**
- EN: No. I can see that. It is infuriating, and it is most of the reason I asked. Very well. I will not share gracefully, but I will share. Do not expect me to like them.
- FR: Non. Je le vois bien. C'est exaspérant, et c'est en grande partie pourquoi je posais la question. Soit. Je ne partagerai pas de bonne grâce, mais je partagerai. N'attendez pas de moi que je les apprécie.

End of dialogue.

**J2c - Gortash**
- EN: I have spies in every camp. Yours simply sends the most interesting reports.
- FR: J'ai des espions dans tous les camps. Le vôtre envoie simplement les rapports les plus intéressants.

Goes back to Choice JA, without `JA3`.

**J2d - Gortash**
- EN: I have owned a great many things and wanted very few. Yes. It matters.
- FR: J'ai possédé beaucoup de choses et j'en ai désiré très peu. Oui. Cela compte.

**J3 - Narrator**
- EN: He looks away first. You suspect that does not happen often.
- FR: Il détourne le regard le premier. Vous devinez que cela n'arrive pas souvent.

End of dialogue.

## Open points

- `JA1` does not end the other romance by itself. Doing it for real means touching the base game romance flags of each companion.
