# Extension - The foundry

What happens to the romance if the player destroys the Steel Watch Foundry. Notation is explained in the README.

## How it starts

- Requires: `GR_Romance_Interested`, `GR_Romance_Ended` not set, and the foundry destroyed (base game flag, to look up).
- Plays the next time the player talks to Gortash, before his usual dialogue.
- In French, Gortash goes back to "vous" for this whole scene, even after the private night. It is deliberate: he is putting distance between them.

## Flags

| Flag | Set by | Meaning |
|---|---|---|
| `GR_Foundry_Done` | start of the scene | The scene cannot be replayed |
| `GR_Foundry_Reconciled` | `FB1`, `FB2`, `FB3` | The romance survives |
| `GR_Romance_Ended` | `FB4` | The romance is over for good |

---

**F1 - Narrator**
- EN: The office smells of smoke that does not come from the fire. He does not rise when you enter. He does not look up.
- FR: Le bureau sent une fumée qui ne vient pas de la cheminée. Il ne se lève pas à votre entrée. Il ne lève pas les yeux.

**F2 - Gortash**
- EN: Years of work. The foundry, the Watch, every safeguard I built so that this city would never again depend on the mercy of people like the ones who sold me. Gone in an afternoon. And I am told you were there.
- FR: Des années de travail. La fonderie, la Garde, chaque rempart que j'ai bâti pour que cette ville ne dépende plus jamais de la pitié de gens comme ceux qui m'ont vendu. Disparus en un après-midi. Et l'on me dit que vous y étiez.

## Choice FA

| Id | EN | FR | Goes to |
|---|---|---|---|
| FA1 | There were people chained to those machines. | Il y avait des gens enchaînés à ces machines. | F3a |
| FA2 | I did it. I won't apologise. | C'est moi. Je ne m'excuserai pas. | F3b |
| FA3 | I did it for you. That thing was going to get you killed. | Je l'ai fait pour vous. Cette chose allait causer votre perte. | F3c |
| FA4 | It was a mistake. I'm sorry. | C'était une erreur. Pardon. | F3d |

**F3a - Gortash**
- EN: Gondians. Yes. I know precisely how many, I signed for each of them. I told myself it was a clause in a contract. You have just read it aloud to me, and I do not thank you for it.
- FR: Des Gondiens. Oui. Je sais précisément combien, j'ai signé pour chacun d'eux. Je me disais que ce n'était qu'une clause dans un contrat. Vous venez de me la lire à voix haute, et je ne vous en remercie pas.

**F3b - Gortash**
- EN: No. Of course you won't. That is one of the things I... It is one of the things about you.
- FR: Non. Bien sûr que non. C'est l'une des choses que je... C'est l'une des choses, chez vous.

**F3c - Gortash**
- EN: Do not dress it up as a kindness. You took my army because you could not stomach it. Have the decency to say so.
- FR: Ne maquillez pas cela en bonté. Vous m'avez pris mon armée parce qu'elle vous soulevait le cœur. Ayez la décence de le dire.

**F3d - Gortash**
- EN: A mistake is a misplaced decimal. This was a choice. Do not insult us both.
- FR: Une erreur, c'est une virgule mal placée. Ceci était un choix. Ne nous insultez pas tous les deux.

All four go to F4.

**F4 - Gortash**
- EN: So here is where we stand. The Archduke has every reason to have you thrown from the top of this fortress. And I have been sitting here for an hour, unable to give the order.
- FR: Voici donc où nous en sommes. L'Archiduc a toutes les raisons de vous faire jeter du haut de cette forteresse. Et moi, je suis assis ici depuis une heure, incapable d'en donner l'ordre.

## Choice FB

| Id | EN | FR | Sets flag | Goes to |
|---|---|---|---|---|
| FB1 | Then don't give it. Rule without the Watch. I'll stand beside you. | Alors ne le donnez pas. Gouvernez sans la Garde. Je resterai à vos côtés. | `GR_Foundry_Reconciled` | F5a |
| FB2 | You would have become the thing that sold you. I stopped it. | Vous seriez devenu ce qui vous a vendu. Je l'ai empêché. | `GR_Foundry_Reconciled` | F5b |
| FB3 | *Say nothing. Wait.* | *Ne rien dire. Attendre.* | `GR_Foundry_Reconciled` | F5c |
| FB4 | Give the order, then. Or let me go. | Donnez l'ordre, alors. Ou laissez-moi partir. | `GR_Romance_Ended` | F5x |

**F5a - Gortash**
- EN: Beside me. With no army, half the patriars sharpening their knives, and a brain under the city. You do choose your moments. Stay, then. I am too angry to be gracious about it. Stay anyway.
- FR: À mes côtés. Sans armée, avec la moitié des patriars qui aiguisent leurs couteaux et un cerveau sous la ville. Vous choisissez vos moments. Restez, alors. Je suis trop en colère pour le dire avec grâce. Restez quand même.

**F5b - Gortash**
- EN: That is a vile thing to say to me. It is also the only thing anyone has said today that I shall still be thinking about tonight.
- FR: C'est une chose ignoble à me dire. C'est aussi la seule, de toute cette journée, à laquelle je penserai encore ce soir.

**F5c - Narrator**
- EN: The silence stretches. At last he pushes the second glass across the desk, without looking at you. It is not forgiveness. It is a chair left pulled out.
- FR: Le silence s'étire. Enfin, il pousse le second verre vers vous sur le bureau, sans vous regarder. Ce n'est pas un pardon. C'est une chaise laissée tirée.

**F5x - Gortash**
- EN: Go. The alliance holds until the brain is dead, because I am not a fool. Everything else, you burned with the foundry.
- FR: Partez. L'alliance tient jusqu'à la mort du cerveau, car je ne suis pas un imbécile. Tout le reste, vous l'avez brûlé avec la fonderie.

## Open points

- In the base game, destroying the foundry may break the alliance or make Gortash hostile. Check what happens before building this scene: it may need the base reaction to be overridden.
- If the scene plays after the private night, the player's French lines `FA3`, `FB1`, `FB2` and `FB4` still say "vous". Add "tu" versions if that bothers you.
