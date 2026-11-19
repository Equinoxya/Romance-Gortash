# Step 3 - The ball

Dialogue script to build in the Toolkit dialog editor. Text only, no voice.
Notation and gender variants are explained in the README.

## How it starts

- Requires: `GR_Romance_Interested`, Gortash alive, alliance intact.
- At the next long rest, an invitation card is added to the player's inventory (same mechanism as the first letter).
- Starts when the player closes the invitation card after reading it, like the office scene: the player first chooses to go tonight (`L1`) or not (`L2`). Saying no sets nothing. Line `P0` is kept but unused.
- First version: the dance is told by the narrator. No custom animation. The herald and patriar lines (`N2`, `N3`, `N4`) are shown as narrator text (see "Open points").

## Flags

| Flag | Set by | Meaning |
|---|---|---|
| `GR_Ball_Invited` | invitation delivered | Unlocks `P0` |
| `GR_Ball_Attended` | `N1`, start of the scene | The scene cannot be replayed |
| `GR_Ball_Danced` | `N14` | The player danced with him |
| `GR_Romance_Ended` | `C4` | Romance is over for good |

Step 4 unlocks with `GR_Ball_Attended`, as long as `GR_Romance_Ended` is not set.

---

## Invitation card

**CARD_NAME - Item name**
- EN: Invitation Embossed in Black and Gold
- FR: Carton d'invitation noir et or

**CARD_DESC - Item description**
- EN: Stiff card, gilt edges. Someone has added a few lines by hand at the bottom.
- FR: Carton rigide à tranche dorée. Quelqu'un a ajouté quelques lignes à la main, tout en bas.

**CARD_TEXT - Item content**
- EN: The Archduke of Baldur's Gate requests the pleasure of your company at a ball held in honour of the city's deliverance, in the great hall of Wyrm's Rock Fortress.<br><br>Dress as you see fit. You will be the best-armed guest regardless.<br><br>*Consider this the proper invitation. There will be an orchestra. I am owed one dance, and I always collect. - E.G.*
- FR: L'Archiduc de la Porte de Baldur sollicite le plaisir de votre compagnie au bal donné en l'honneur de la délivrance de la cité, dans la grande salle de la Forteresse du roc du dracosir.<br><br>Venez dans la tenue qui vous plaira. Vous serez de toute façon la personne la mieux armée de la soirée.<br><br>*Voici l'invitation dans les règles. Il y aura un orchestre. On me doit une danse, et je recouvre toujours mes créances. - E.G.*

---

## The card

**L0 - Narrator**
- EN: The ball is tonight. Somewhere in Wyrm's Rock, an orchestra is tuning, and a place is being kept that nobody else would dare to take.
- FR: Le bal a lieu ce soir. Quelque part dans la Forteresse du roc du dracosir, un orchestre s'accorde, et l'on garde une place que personne d'autre n'oserait prendre.

| Id | EN | FR | Goes to |
|---|---|---|---|
| L1 | Go to the ball. | Se rendre au bal. | N1 |
| L2 | Not tonight. | Pas ce soir. | L3 |

**L3 - Narrator**
- EN: You set the card aside. The orchestra, you suspect, will wait.
- FR: Vous mettez le carton de côté. L'orchestre, vous vous en doutez, attendra.

End of dialogue. Nothing is set, so the card offers the choice again.

## Arrival

**P0 - Player** (unused, see "How it starts")
- EN: I'm here for the ball.
- FR: Je viens pour le bal.

**N1 - Narrator**
- EN: The audience hall has been remade for the night: banners of black and gold, a hundred candles, and the Steel Watch lined along the walls like ceremonial armour that might ask you to leave.
- FR: La salle d'audience a été refaite pour la nuit : bannières noir et or, une centaine de bougies, et la Garde d'Acier alignée le long des murs comme des armures d'apparat capables de vous prier de sortir.

**N2 - Herald**
- EN: The Archduke's guest of honour!
- FR: [L'invité d'honneur de l'Archiduc ! / L'invitée d'honneur de l'Archiduc ! / Sur invitation personnelle de l'Archiduc !]

**N3 - Patriar** (overheard)
- EN: Is that the one? I heard [he / she / they] walked out of the Shadow-Cursed Lands without a scratch.
- FR: C'est bien [lui / elle / ellui] ? On raconte qu'[il / elle / iel] a traversé les Terres maudites sans une égratignure.

**N4 - Second patriar** (overheard)
- EN: I heard [he / she / they] put a knife to the Archduke's throat, and he sent [him / her / them] flowers.
- FR: Moi, on m'a dit qu'[il / elle / iel] avait mis une lame sous la gorge de l'Archiduc, et qu'il lui avait envoyé des fleurs.

## Choice A

| Id | Condition | EN | FR | Goes to |
|---|---|---|---|---|
| A1 | | *Walk on.* Let them talk. | *Passer votre chemin.* Qu'ils parlent. | N5 |
| A2 | | It was two knives, actually. | Deux lames, en réalité. | N4b |
| A3 | `[Durge]` | *Smile at them until they stop smiling.* | *Leur sourire jusqu'à ce qu'ils cessent de sourire.* | N4c |

**N4b - Narrator**
- EN: The patriars discover a sudden and passionate interest in the buffet.
- FR: Les patriars se découvrent une passion soudaine pour le buffet.

**N4c - Narrator** `[Durge]`
- EN: You say nothing. You simply look at them the way one looks at a meal. The conversation dies, as if it sensed what else might.
- FR: Vous ne dites rien. Vous les regardez simplement comme on regarde un repas. La conversation meurt, comme si elle sentait ce qui pourrait suivre.

Both go to N5.

## Gortash

**N5 - Gortash** `[Tav]`
- EN: There you are. I had a second speech prepared, in case you did not come. It was considerably less charming.
- FR: Vous voilà. J'avais préparé un second discours, au cas où vous ne viendriez pas. Il était nettement moins charmant.

**N5D - Gortash** `[Durge]`
- EN: The last ball we attended together, you slipped away early with our host's signet ring - and the finger it was on. Tonight, do try to stay for the dancing.
- FR: Au dernier bal où nous sommes allés ensemble, vous avez filé avant la fin avec la chevalière de notre hôte - et le doigt qui la portait. Ce soir, tâchez de rester pour la danse.

## Choice B

| Id | Condition | EN | FR | Goes to |
|---|---|---|---|---|
| B1 | | You look almost respectable, Archduke. | Vous avez presque l'air respectable, Archiduc. | N6a |
| B2 | | All this, for one dance? | Tout cela pour une danse ? | N6b |
| B3 | | Half this room wants you dead. | La moitié de cette salle veut votre mort. | N6c |
| B4 | `[Durge]` | I don't remember that ball. | Je ne me souviens pas de ce bal. | N6d |

**N6a - Gortash**
- EN: Slander. I look entirely respectable. It took three tailors and a threat.
- FR: Calomnie. J'ai l'air parfaitement respectable. Il a fallu trois tailleurs et une menace.

**N6b - Gortash**
- EN: All this is for the city. The dance is for me. I allow myself one indulgence per coup.
- FR: Tout cela est pour la ville. La danse est pour moi. Je m'accorde un caprice par coup d'État.

**N6c - Gortash**
- EN: More than half. That is what makes a good party. But tonight they will have to watch me enjoy myself first.
- FR: Plus de la moitié. C'est ce qui fait les bonnes soirées. Mais ce soir, ils devront d'abord me regarder m'amuser.

**N6d - Gortash** `[Durge]`
- EN: No. But I do. You wore red, and I could not look at anyone else. I intend to give you a better one to keep.
- FR: Non. Mais moi, si. Vous portiez du rouge, et je ne pouvais regarder personne d'autre. Je compte vous en offrir un meilleur à garder.

All four go to N7.

## The dance

**N7 - Narrator**
- EN: The orchestra begins something slow. Around you the floor clears - not out of courtesy, but because he has raised one gloved hand, and the room has learned what that means.
- FR: L'orchestre entame un air lent. Autour de vous, la piste se vide - non par courtoisie, mais parce qu'il a levé une main gantée, et que la salle a appris ce que cela signifie.

**N8 - Gortash**
- EN: My dance, I believe.
- FR: Ma danse, je crois.

**N8n - Narrator**
- EN: He offers you his hand. The bare one, not the gauntlet.
- FR: Il vous tend la main. La main nue, pas le gantelet.

## Choice C

| Id | EN | FR | Sets flag | Goes to |
|---|---|---|---|---|
| C1 | *Take his hand and lead.* | *Prendre sa main et mener.* | | N9a |
| C2 | *Take his hand and let him lead.* | *Prendre sa main et le laisser mener.* | | N9b |
| C3 | I don't dance. | Je ne danse pas. | | N9c |
| C4 | Not tonight, Gortash. Not ever. | Pas ce soir, Gortash. Ni jamais. | `GR_Romance_Ended` | N9x |

**N9a - Narrator**
- EN: You take the lead. He allows it for exactly three bars, then tests you with a turn. You hold, and something like delight crosses his face.
- FR: Vous menez. Il le tolère pendant trois mesures exactement, puis vous met à l'épreuve d'un tour. Vous tenez bon, et quelque chose comme du ravissement passe sur son visage.

**N9a2 - Gortash**
- EN: Nobody leads me. I find I do not mind it. Tell no one.
- FR: Personne ne me mène. Je découvre que cela ne me déplaît pas. N'en dites rien à personne.

Goes to N10.

**N9b - Narrator**
- EN: He leads the way he governs: precisely, one step ahead, with a firm hand at your back. To your considerable annoyance, he is good.
- FR: Il mène comme il gouverne : avec précision, un pas d'avance, et une main ferme dans votre dos. À votre grand agacement, il danse bien.

**N9b2 - Gortash**
- EN: A childhood among cobblers. One learns to mind one's feet.
- FR: Une enfance chez des cordonniers. On apprend à surveiller ses pieds.

Goes to N10.

**N9c - Gortash**
- EN: Neither do I, as a rule. So we shall be bad at it together, in front of everyone who matters. Think of the scandal.
- FR: Moi non plus, en règle générale. Nous serons donc mauvais ensemble, devant tous ceux qui comptent. Songez au scandale.

**N9c2 - Narrator**
- EN: He does not withdraw his hand.
- FR: Il ne retire pas sa main.

| Id | EN | FR | Goes to |
|---|---|---|---|
| C3a | *Take it.* | *La prendre.* | N9d |
| C3b | No. | Non. | N9e |

**N9d - Narrator**
- EN: You are, in fact, bad at it. He is not, and he covers for you so smoothly that half the room will swear you were magnificent.
- FR: Vous dansez mal, en effet. Lui non, et il vous couvre avec tant d'aisance que la moitié de la salle jurera que vous étiez magnifique.

Goes to N10.

**N9e - Gortash**
- EN: Then stand with me and let us watch them dance instead. It is nearly as satisfying, and they are far more afraid.
- FR: Alors restez près de moi et regardons-les danser. C'est presque aussi satisfaisant, et ils ont bien plus peur.

Goes to N14b. No dance, the romance continues.

**N9x - Gortash**
- EN: Understood. Enjoy the wine. It is the last thing of mine you will be offered.
- FR: Compris. Profitez du vin. C'est la dernière chose venant de moi qu'on vous offrira.

End of dialogue.

## During the dance

**N10 - Narrator**
- EN: The room turns around you, a blur of candles, silk and watching eyes. He speaks low, for you alone.
- FR: La salle tourne autour de vous, un tourbillon de bougies, de soie et de regards. Il parle bas, pour vous seulement.

**N11 - Gortash** `[Tav]`
- EN: They are all trying to work out what you are to me. An asset, a hostage, a weakness. I have been running the same sum myself, and it keeps giving me an answer I did not budget for.
- FR: Ils cherchent tous à comprendre ce que vous êtes pour moi. Un atout, un otage, une faiblesse. Je refais moi-même le calcul, et il me donne toujours un résultat que je n'avais pas prévu au budget.

**N11D - Gortash** `[Durge]`
- EN: Bhaal made you to end the world. I only ever wanted to own it. Yet here we are, dancing in it, and for once neither of us is in a hurry.
- FR: Bhaal vous a donné vie pour détruire le monde. Moi, je n'ai jamais voulu que le posséder. Et nous voilà, à danser dedans, sans qu'aucun de nous deux soit pressé, pour une fois.

## Choice D

| Id | Condition | EN | FR | Goes to |
|---|---|---|---|---|
| D1 | | And what answer is that? | Et quel est ce résultat ? | N12a |
| D2 | | Careful. A weakness can be used against you. | Prudence. Une faiblesse, cela s'exploite. | N12b |
| D3 | | *Pull him closer.* Stop talking, Archduke. | *L'attirer plus près.* Taisez-vous, Archiduc. | N12c |
| D4 | `[Durge]` | And if the Urge takes me here, in your arms? | Et si la Pulsion me prend ici, dans vos bras ? | N12d |

**N12a - Gortash**
- EN: Ask me again somewhere with fewer witnesses.
- FR: Reposez-moi la question dans un endroit avec moins de témoins.

**N12b - Gortash**
- EN: So can a strength. That has never stopped me from acquiring one.
- FR: Une force aussi. Cela ne m'a jamais retenu d'en acquérir une.

**N12c - Narrator**
- EN: He stops talking. It is, by all accounts, a first.
- FR: Il se tait. C'est, de l'avis général, une première.

**N12d - Gortash** `[Durge]`
- EN: Then I shall be the best-dressed corpse in Baldur's Gate, and you will be terribly sorry in the morning. I will take those odds. With you, I always have.
- FR: Alors je serai le cadavre le mieux habillé de la Porte de Baldur, et vous le regretterez amèrement au matin. J'accepte le risque. Avec vous, je l'ai toujours accepté.

All four go to N13.

## End of the evening

**N13 - Narrator**
- EN: The music ends. He holds on one beat longer than the dance requires, then bows over your hand, for the whole court to see.
- FR: La musique s'achève. Il vous retient un temps de plus que la danse ne l'exige, puis s'incline sur votre main, devant toute la cour.

**N14 - Gortash** (sets `GR_Ball_Danced`)
- EN: Thank you for the dance. You will hear from me again - privately, this time.
- FR: Merci pour cette danse. Vous aurez de mes nouvelles - en privé, cette fois.

**N14b - Gortash** (no dance)
- EN: Thank you for the evening. You will hear from me again - privately, this time.
- FR: Merci pour cette soirée. Vous aurez de mes nouvelles - en privé, cette fois.

## Open points

- The ball needs extra characters in the hall (herald, patriars, dancers). For a first version, the herald and patriar lines can be narrator text instead.
- `N3` assumes the player went through the Shadow-Cursed Lands, which is always true by Act 3.
