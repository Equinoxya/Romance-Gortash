# Step 2 - Evening in the office

Dialogue script to build in the Toolkit dialog editor. Text only, no voice.
Notation and gender variants are explained in the README.

## How it starts

- Requires: `GR_Letter1_Delivered` (step 1).
- Starts when the player closes the invitation letter after reading it (`GR_Letters.txt`). The player first chooses to go tonight (`L1`) or not (`L2`). Saying no sets nothing: reading the letter again offers the choice again.
- Not in Gortash's office dialogue: in the base game, an allied Gortash leaves his office for the Morphic Pool as soon as the party leaves Wyrm's Rock, usually before the letter arrives. Line `P0` is kept but unused.
- BG3 has no day/night cycle, so the evening is set by a fade to black and the narrator line `N1`.

## Dark Urge backstory

Before the base game, the Dark Urge and Gortash were lovers: passionate, and with a rare understanding of each other. He believed them dead and grieved. In this scene he holds back and says "vous", because they no longer remember him. He names what they were only if asked (`B4`).

## Flags

| Flag | Set by | Meaning |
|---|---|---|
| `GR_Office_Visited` | `N1`, start of the scene | The scene cannot be replayed |
| `GR_Romance_Interested` | `C1`, `C2` | Romance is open, unlocks step 3 |
| `GR_Romance_Declined` | `C3` | Romance is closed, alliance unaffected |

---

## The letter

**L0 - Narrator**
- EN: Wyrm's Rock is not far, and the evening is still young. Somewhere up there, two glasses are being poured.
- FR: La Forteresse du roc du dracosir n'est pas loin, et la soirée ne fait que commencer. Quelque part là-haut, on remplit deux verres.

| Id | EN | FR | Goes to |
|---|---|---|---|
| L1 | Go to Wyrm's Rock tonight. | Se rendre à la Forteresse du roc du dracosir ce soir. | N1 |
| L2 | Not tonight. | Pas ce soir. | L3 |

**L3 - Narrator**
- EN: You fold the letter and put it away. It will keep.
- FR: Vous repliez la lettre et la rangez. Elle attendra.

End of dialogue. Nothing is set, so the letter offers the choice again.

## Opening

**P0 - Player** (unused, see "How it starts")
- EN: I received your invitation.
- FR: J'ai reçu votre invitation.

**A0 - Narrator**
- EN: You push open the doors. At the far end of the room, by his desk, Gortash is waiting.
- FR: Vous poussez les portes. Au fond de la pièce, près de son bureau, Gortash vous attend.

**AG - Gortash**
- EN: At last. I was beginning to take it personally.
- FR: Enfin. Je commençais à le prendre personnellement.

**N1 - Narrator**
- EN: The office has been emptied of clerks and guards. Two glasses wait on the desk, already poured.
- FR: Le bureau a été vidé de ses clercs et de ses gardes. Deux verres attendent sur la table, déjà servis.

**N2 - Gortash** `[Tav]`
- EN: You came. And alone, as asked. You have no idea how rare it is to meet someone who follows a simple instruction without being ordered to.
- FR: [Vous êtes venu. / Vous êtes venue. / Vous voilà.] Et sans escorte, comme demandé. Vous n'imaginez pas comme il est rare de croiser quelqu'un qui suit une consigne simple sans qu'on la lui ordonne.

**N2D - Gortash** `[Durge]`
- EN: You always did prefer to arrive after dark. Some habits survive anything, it seems - even what was done to you.
- FR: Vous avez toujours préféré arriver à la nuit tombée. Certaines habitudes survivent à tout, on dirait - même à ce qu'on vous a fait.

## Choice A

| Id | Condition | EN | FR | Goes to |
|---|---|---|---|---|
| A1 | | You promised better wine. I'm here to hold you to it. | Vous m'avez promis un meilleur vin. Je viens vérifier. | N3a |
| A2 | | What do you want, Gortash? | Que voulez-vous, Gortash ? | N3b |
| A3 | | An Archduke with no guards in the room. Either you trust me, or you're a fool. | Un Archiduc sans un seul garde dans la pièce. Soit vous me faites confiance, soit vous êtes un imbécile. | N3c |
| A4 | `[Durge]` | You talk as though you know me. | Vous parlez comme si vous me connaissiez. | N3d |

**N3a - Gortash**
- EN: Someone with priorities. Good. That glass is yours. A Tethyrian red, older than my ambitions, though not by much.
- FR: Quelqu'un qui a le sens des priorités. Bien. Ce verre-là est pour vous. Un rouge du Téthyr, plus vieux que mes ambitions, mais de peu.

**N3b - Gortash**
- EN: Straight to the ledger. I respect that. What I want, tonight, is one hour in which nobody asks me to sign anything. And your company. I have been curious about it for longer than I care to admit.
- FR: Droit au but. J'apprécie. Ce que je veux, ce soir, c'est une heure où personne ne me demande de signer quoi que ce soit. Et votre compagnie. Elle m'intrigue depuis plus longtemps que je ne voudrais l'admettre.

**N3c - Gortash**
- EN: Neither. I have simply calculated that you are more interesting alive and unthreatened. Do stop looking for the exits, you're making the furniture nervous.
- FR: Ni l'un ni l'autre. J'ai simplement calculé que vous [étiez plus intéressant / étiez plus intéressante / aviez plus d'intérêt] en vie et sans menace. Cessez donc de chercher les sorties, vous rendez les meubles nerveux.

**N3d - Gortash** `[Durge]`
- EN: I knew you better than anyone alive. We built all of this together, you and I, across a table much like this one. You were the only one in the room I never had to explain myself to. I have missed that more than I expected.
- FR: Je vous connaissais mieux que personne. Nous avons tout bâti ensemble, vous et moi, autour d'une table comme celle-ci. Vous étiez la seule personne à qui je n'avais jamais rien à expliquer. Cela m'a manqué plus que je ne le pensais.

All four go to N4.

## Middle

**N4 - Narrator**
- EN: He hands you a glass. His fingers are in no hurry to leave yours.
- FR: Il vous tend un verre. Ses doigts ne se pressent pas de quitter les vôtres.

**N5 - Gortash** `[Tav]`
- EN: Everyone in this city wants something from me. You are the first in a long time who might simply take it without asking. That ought to worry me. Instead, I keep thinking about it.
- FR: Tout le monde dans cette ville veut quelque chose de moi. Vous êtes [le premier / la première / la première personne] depuis longtemps qui pourrait simplement le prendre sans demander. Cela devrait m'inquiéter. Au lieu de quoi, j'y repense sans cesse.

**N5D - Gortash** `[Durge]`
- EN: They took your memory and left the rest. The poise, the appetite, the way you look at a room as if deciding what to keep. I would know you in the dark.
- FR: Ils vous ont pris votre mémoire et laissé tout le reste. L'aplomb, l'appétit, cette façon de regarder une pièce comme pour décider ce que vous allez en garder. Je vous reconnaîtrais dans le noir.

## Choice B

| Id | Condition | EN | FR | Goes to |
|---|---|---|---|---|
| B1 | | Careful, my lord. That almost sounded like a compliment. | Prudence, monseigneur. On aurait presque dit un compliment. | N6a |
| B2 | | And what is it you think I would take? | Et que croyez-vous que je prendrais ? | N6b |
| B3 | | Flattery is cheap. You want an ally who won't turn on you. | La flatterie ne coûte rien. Vous voulez [un allié / une alliée / quelqu'un] qui ne vous trahira pas. | N6c |
| B4 | `[Durge]` | Then tell me what we were to each other. | Alors dites-moi ce que nous étions l'un pour l'autre. | N6d |
| B5 | | I've heard enough. Goodnight, Archduke. | J'en ai assez entendu. Bonne nuit, Archiduc. | X1 |

**N6a - Gortash**
- EN: It was one. I ration them, so do try to enjoy it.
- FR: C'en était un. Je les rationne, alors tâchez d'en profiter.

**N6b - Gortash**
- EN: Whatever you pleased. That is precisely the trouble with you.
- FR: Tout ce qui vous plairait. C'est bien là le problème, avec vous.

**N6c - Gortash**
- EN: I want both. I am a tyrant, I'm told. We are greedy by profession.
- FR: Je veux les deux. Je suis un tyran, paraît-il. Nous sommes avides par métier.

**N6d - Gortash** `[Durge]`
- EN: Everything. Partners in the plan, and lovers long before it was finished. You knew the worst of me and it did not drive you away. I knew the worst of you and wanted more. Then you were gone, and I learned what the word "loss" is actually for.
- FR: Tout. Associés dans le plan, et amants bien avant qu'il soit achevé. Vous connaissiez le pire de moi, et cela ne vous a pas fait fuir. Je connaissais le pire de vous, et j'en voulais davantage. Puis vous avez disparu, et j'ai appris à quoi sert vraiment le mot « perte ».

All four go to N7.

## The offer

**N7 - Narrator**
- EN: He sets his glass down. You stand near enough now for the gold of his gauntlet to catch the candlelight between you. He does not touch you. He waits.
- FR: Il repose son verre. Vous êtes à présent assez près pour que l'or de son gantelet accroche la lueur des bougies entre vous. Il ne vous touche pas. Il attend.

**N8 - Gortash** `[Tav]`
- EN: I never make an offer I haven't costed. So here is one: come back. Not for the alliance, that is already signed. For this. Whatever this is turning into.
- FR: Je ne fais jamais d'offre sans en avoir calculé le prix. En voici une : revenez. Pas pour l'alliance, elle est déjà signée. Pour ceci. Quoi que ce soit en train de devenir.

**N8D - Gortash** `[Durge]`
- EN: I never make an offer I haven't costed. So here is one: come back. Not for the plan, that runs without us now. For this. I have already mourned you once. I do not intend to waste the second chance.
- FR: Je ne fais jamais d'offre sans en avoir calculé le prix. En voici une : revenez. Pas pour le plan, il tourne sans nous désormais. Pour ceci. J'ai déjà porté votre deuil une fois. Je ne compte pas gâcher la seconde chance.

## Choice C

| Id | EN | FR | Sets flag | Goes to |
|---|---|---|---|---|
| C1 | *Take his hand.* Then stop calculating and find out. | *Prendre sa main.* Alors cessez de calculer, et voyez par vous-même. | `GR_Romance_Interested` | N9a |
| C2 | Invite me properly next time. I might say yes. | Invitez-moi dans les règles, la prochaine fois. Je pourrais dire oui. | `GR_Romance_Interested` | N9b |
| C3 | We are allies, Gortash. Nothing more. | Nous sommes alliés, Gortash. Rien de plus. | `GR_Romance_Declined` | N9c |

**N9a - Narrator**
- EN: He lifts your hand and bows over it, unhurried, until his lips rest on the back of it. When he straightens, for one unguarded moment, the Archduke looks like a man who has miscounted.
- FR: Il lève votre main et s'incline dessus, sans hâte, jusqu'à poser ses lèvres sur le dos de vos doigts. Quand il se redresse, l'Archiduc a l'air, l'espace d'un instant, d'un homme qui s'est trompé dans ses comptes.

**N9a2 - Gortash**
- EN: Well. That was not in the design. I shall have to redraw it.
- FR: Tiens. Ce n'était pas prévu dans les plans. Il va falloir que je les redessine.

Goes to X2.

**N9b - Gortash**
- EN: Properly. With an orchestra, if need be. You will hear from me.
- FR: Dans les règles. Avec un orchestre, s'il le faut. Vous aurez de mes nouvelles.

Goes to X2. This line announces the ball of step 3.

**N9c - Gortash**
- EN: As you like. I am a patient man, and the offer does not expire. Finish your wine, at least. Wasting it would be a crime, and I only commit the profitable ones.
- FR: Comme il vous plaira. Je suis un homme patient, et l'offre n'expire pas. Finissez au moins votre vin. Le gâcher serait un crime, et je ne commets que ceux qui rapportent.

End of dialogue.

## Exits

**X1 - Gortash** (player left early, no romance flag)
- EN: A pity. The door is behind you. The invitation stays open.
- FR: Dommage. La porte est derrière vous. L'invitation reste valable.

**X2 - Gortash** `[Tav]` (romance open)
- EN: Go, before your companions come looking and I am forced to be civil to them. And thank you for coming. I don't say that often either.
- FR: Partez, avant que vos compagnons ne viennent vous chercher et que je sois obligé d'être aimable avec eux. Et [merci d'être venu / merci d'être venue / merci de votre visite]. Cela non plus, je ne le dis pas souvent.

**X2D - Gortash** `[Durge]` (romance open)
- EN: Go. And this time, come back to me in one piece.
- FR: Allez. Et cette fois, revenez-moi en un seul morceau.

## Open points

- After `X1`, the scene is closed. To let the player try again later, do not set `GR_Office_Visited` on that exit.
