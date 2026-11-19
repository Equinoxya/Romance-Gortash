# Step 4 - Second letter and private night

Dialogue script to build in the Toolkit dialog editor. Text only, no voice.
Notation and gender variants are explained in the README.

## How it starts

- Requires: `GR_Ball_Attended`, `GR_Romance_Ended` not set, Gortash alive, alliance intact.
- At the next long rest, the second letter is added to the player's inventory.
- Starts when the player closes the second letter after reading it, like the office and the ball: the player first chooses to go tonight (`L1`) or not (`L2`). Saying no sets nothing. Line `P0` is kept but unused.
- The intimate part is narrated and ends on a fade to black. No custom animation.
- In French, Gortash and the player switch from "vous" to "tu" at `N4` and keep it for the rest of the mod. The narrator keeps "vous".

## Flags

| Flag | Set by | Meaning |
|---|---|---|
| `GR_Night_Invited` | letter delivered | Unlocks `P0` |
| `GR_First_Names` | `B1`, `B2` | They now say "tu" in French, picks the right breakup letter. Set when the player says his name rather than at `N4`, so that leaving at `B3` changes nothing |
| `GR_Romance_Committed` | `N11`, `N11b`, `N11d` | Romance is established, needed for step 5 |
| `GR_Romance_Ended` | `C4` | Romance is over for good |

If the player leaves at `B3`, no flag changes and the scene stays available.

---

## Second letter

**LETTER2_NAME - Item name**
- EN: Unsealed Letter in a Familiar Hand
- FR: Lettre sans sceau, d'une écriture familière

**LETTER2_DESC - Item description**
- EN: No crest, no wax. Whoever wrote this did not want it to look official.
- FR: Ni armoiries, ni cire. Son auteur ne voulait pas qu'elle ait l'air officielle.

**LETTER2_TEXT - Item content**
- EN: No crest this time, and no title.<br><br>I have spent the day signing decrees and thinking of none of them. This is inefficient, and I hold you responsible.<br><br>My private rooms are above the office. The guards on that stair have been dismissed for the night. The door will be unlocked for you, and for no one else.<br><br>Come if you wish to. If you do not, burn this and we shall never speak of it. I would rather be refused than obeyed.<br><br>Enver
- FR: Pas d'armoiries cette fois, ni de titre.<br><br>J'ai passé la journée à signer des décrets sans penser à aucun d'eux. C'est inefficace, et je vous en tiens pour responsable.<br><br>Mes appartements se trouvent au-dessus du bureau. Les gardes de cet escalier ont congé pour la nuit. La porte sera ouverte pour vous, et pour personne d'autre.<br><br>Venez si vous le souhaitez. Sinon, brûlez ceci et nous n'en parlerons jamais. Je préfère un refus à de l'obéissance.<br><br>Enver

---

## The letter

**L0 - Narrator**
- EN: The stair above his office will be unguarded tonight. The letter does not say what waits at the top. It does not need to.
- FR: L'escalier au-dessus de son bureau ne sera pas gardé ce soir. La lettre ne dit pas ce qui attend en haut. Elle n'en a pas besoin.

| Id | EN | FR | Goes to |
|---|---|---|---|
| L1 | Go to him tonight. | Le rejoindre ce soir. | N1 |
| L2 | Not tonight. | Pas ce soir. | L3 |

**L3 - Narrator**
- EN: You fold the letter. He would rather be refused than obeyed; tonight, he will simply have to wait.
- FR: Vous repliez la lettre. Il préfère un refus à de l'obéissance ; ce soir, il devra simplement attendre.

End of dialogue. Nothing is set, so the letter offers the choice again.

## Arrival

**P0 - Player** (unused, see "How it starts")
- EN: I got your letter. The other one.
- FR: J'ai reçu votre lettre. L'autre.

**N1 - Narrator**
- EN: His rooms are smaller than you expected. No throne, no banners: a desk buried in blueprints, a fire, a bed. The gauntlet lies on the table, unbuckled. Without it, his hand looks like anyone's.
- FR: Ses appartements sont plus petits que vous ne l'imaginiez. Ni trône, ni bannières : un bureau enseveli sous les plans, un feu, un lit. Le gantelet repose sur la table, débouclé. Sans lui, sa main ressemble à celle de n'importe qui.

**N2 - Gortash**
- EN: You came. I gave you every way out I could think of, and you came anyway.
- FR: [Vous êtes venu. Je vous ai laissé toutes les issues auxquelles j'ai pu penser, et vous êtes venu quand même. / Vous êtes venue. Je vous ai laissé toutes les issues auxquelles j'ai pu penser, et vous êtes venue quand même. / Vous voilà. Je vous ai laissé toutes les issues auxquelles j'ai pu penser, et vous voilà quand même.]

## Choice A

| Id | Condition | EN | FR | Goes to |
|---|---|---|---|---|
| A1 | | You said you would rather be refused than obeyed. This is neither. | Vous préfériez un refus à de l'obéissance. Ceci n'est ni l'un ni l'autre. | N3a |
| A2 | | You took off the gauntlet. | Vous avez retiré le gantelet. | N3b |
| A3 | | I almost burned it. | J'ai failli la brûler. | N3c |
| A4 | `[Durge]` | Have I ever set foot in this room before? | Ai-je déjà mis les pieds dans cette pièce ? | N3d |

**N3a - Gortash**
- EN: No. This is the third thing. I have very little practice with it.
- FR: Non. C'est la troisième possibilité. J'en ai très peu l'habitude.

**N3b - Gortash**
- EN: It is a weapon. I did not want one between us tonight. Do not make me regret the sentiment.
- FR: C'est une arme. Je n'en voulais pas entre nous ce soir. Ne me faites pas regretter ce sentiment.

**N3c - Gortash**
- EN: And yet. I shall choose to be flattered by the "almost".
- FR: Et pourtant. Je choisis d'être flatté par le « failli ».

**N3d - Gortash** `[Durge]`
- EN: Not this one. There were other rooms, and more nights than I could count. You used to say they were the only hours when neither of us was pretending. I have slept badly ever since.
- FR: Pas celle-ci. Il y en a eu d'autres, et plus de nuits que je ne saurais en compter. Vous disiez que c'étaient les seules heures où aucun de nous deux ne jouait un rôle. Je dors mal depuis.

All four go to N4.

## The name

**N4 - Gortash** `[Tav]`
- EN: I think we are past titles. Not "Archduke". Not "my lord". Enver. I should like to hear how it sounds from you.
- FR: Je crois que nous avons passé l'âge des titres, et du vouvoiement. Ni « Archiduc », ni « monseigneur ». Enver. J'aimerais entendre comment il sonne dans ta bouche.

**N4D - Gortash** `[Durge]`
- EN: You used to call me Enver. No one has since. I should like to hear it again.
- FR: Autrefois, tu m'appelais Enver, et nous ne nous disions pas « vous ». Personne ne m'a appelé ainsi depuis. J'aimerais l'entendre à nouveau.

## Choice B

| Id | EN | FR | Goes to |
|---|---|---|---|
| B1 | Enver. | Enver. | N5a |
| B2 | Enver. It suits you better than the crown. | Enver. Cela te va mieux que la couronne. | N5b |
| B3 | This is too soon for me. I should go. | C'est trop tôt pour moi. Je devrais partir. | N5x |

**N5a - Narrator**
- EN: Something in his shoulders comes undone at the sound of it.
- FR: Quelque chose se dénoue dans ses épaules en l'entendant.

**N5b - Gortash**
- EN: Do not let the crown hear you.
- FR: Que la couronne ne t'entende pas.

Both go to N6.

**N5x - Gortash**
- EN: Then go, and no harm done. The door stays unlocked. Tonight, and after.
- FR: Alors pars, et sans rancune. La porte reste ouverte. Ce soir, et après.

End of dialogue. The scene stays available.

## Confession

**N6 - Gortash** `[Tav]`
- EN: I was sold as a child, for a handful of coin, to a devil. Everything since has been a transaction. I made certain of it, so that nothing could be taken from me again without a price. You are the first thing I have wanted that I do not know how to buy.
- FR: Enfant, on m'a vendu à un diable pour une poignée de pièces. Depuis, tout n'a été que transaction. J'y ai veillé, pour que plus rien ne puisse m'être pris sans en payer le prix. Tu es la première chose que je désire sans savoir comment l'acheter.

**N6D - Gortash** `[Durge]`
- EN: When Orin put her knife in you and they told me you were dead, I did what I always do. I recalculated. I told myself it was a loss of capital. Then I went home to a bed that still smelled of you, and I have never lied to myself so badly, before or since. I loved you. I never said it while you could still remember hearing it.
- FR: Quand Orin a planté sa lame en toi et qu'on m'a annoncé ta mort, j'ai fait ce que je fais toujours. J'ai recalculé. Je me suis dit que c'était une perte de capital. Puis je suis rentré dans un lit qui portait encore ton odeur, et je ne me suis jamais aussi mal menti, ni avant, ni depuis. Je t'aimais. Je ne l'ai jamais dit tant que tu pouvais encore t'en souvenir.

## Choice C

| Id | Condition | EN | FR | Sets flag | Goes to |
|---|---|---|---|---|---|
| C1 | `[Tav]` | You don't have to buy me. I'm here. | Tu n'as pas à m'acheter. Je suis là. | | N7 |
| C2 | | *Kiss him.* | *L'embrasser.* | | N7 |
| C3 | | Then don't calculate. Just this once. | Alors ne calcule pas. Juste cette fois. | | N7 |
| C5 | `[Durge]` | I don't remember loving you. But something in me does. | Je ne me souviens pas de t'avoir aimé. Mais quelque chose en moi s'en souvient. | | N7 |
| C4 | | This was a mistake. Goodbye, Enver. | C'était une erreur. Adieu, Enver. | `GR_Romance_Ended` | N7x |

**N7x - Gortash**
- EN: I see. Close the door on your way out. I would rather not watch you go.
- FR: Je vois. Ferme la porte en sortant. Je préfère ne pas te regarder partir.

End of dialogue.

## The night

Tone: sensual, with Gortash taking charge. He asks for consent in `N7b`. Nothing explicit is shown: the scene fades to black after `N8`.

**N7 - Narrator**
- EN: He kisses you the way he does nothing else: without a plan. Then the plan comes back. His bare hand closes around your jaw and tilts your face up to his, and his voice drops to the tone he keeps for giving orders to a city.
- FR: Il vous embrasse comme il ne fait rien d'autre : sans plan. Puis le plan revient. Sa main nue se referme sur votre mâchoire et lève votre visage vers le sien, et sa voix descend jusqu'au ton qu'il réserve aux ordres donnés à une ville.

**N7b - Gortash**
- EN: I have spent my life taking what I wanted. Tonight, I intend to take my time. Tell me to stop, and I stop. Otherwise, you will do as you are told.
- FR: J'ai passé ma vie à prendre ce que je voulais. Ce soir, je compte prendre mon temps. Dis-moi d'arrêter, et j'arrête. Sinon, tu feras ce qu'on te dit.

### Choice E

| Id | Condition | EN | FR | Goes to |
|---|---|---|---|---|
| E1 | | Yes, my lord. | Oui, monseigneur. | N8a |
| E2 | | *Hold his gaze.* Make me. | *Soutenir son regard.* Oblige-moi. | N8b |
| E3 | | *Push him back onto the bed.* Tonight, the Archduke takes orders. | *Le pousser sur le lit.* Ce soir, c'est l'Archiduc qui obéit. | N8c |
| E4 | `[Durge]` | You always liked giving orders. I always liked choosing which ones to follow. | Tu as toujours aimé donner des ordres. J'ai toujours aimé choisir lesquels suivre. | N8d |

**N8a - Narrator**
- EN: A slow smile. He undresses you without hurry, like something he paid dearly for and means to enjoy. When your hands move to help, he catches both your wrists in one of his and holds them above your head. "No. Mine." You let him.
- FR: Un sourire lent. Il vous déshabille sans hâte, comme une chose payée très cher dont il compte profiter. Quand vos mains veulent l'aider, il saisit vos deux poignets d'une seule main et les maintient au-dessus de votre tête. « Non. À moi. » Vous le laissez faire.

**N8b - Narrator**
- EN: His eyes darken with delight. He backs you against the desk, blueprints scattering, his mouth at your throat and his hand firm at the small of your back. He proves, at length, that he can.
- FR: Son regard s'assombrit de plaisir. Il vous fait reculer contre le bureau, les plans s'éparpillent, sa bouche sur votre gorge et sa main ferme au creux de vos reins. Il vous prouve, longuement, qu'il en est capable.

**N8c - Narrator**
- EN: For one breath he is too surprised to move. Then he laughs, low, and lets himself fall. "Once," he says, as you settle over him and take his wrists. "Only for you." He makes a far worse subject than ruler, and you enjoy correcting him.
- FR: Le temps d'un souffle, la surprise le fige. Puis il rit, tout bas, et se laisse tomber. « Une fois », dit-il, tandis que vous vous installez sur lui et prenez ses poignets. « Pour toi seulement. » Il fait un bien plus mauvais sujet que souverain, et vous prenez plaisir à le corriger.

**N8d - Narrator** `[Durge]`
- EN: "And you followed every one that mattered." He knows exactly where to put his hands, and your body remembers before you do. He holds you down with nothing but his voice, and every order is one you once taught him to give.
- FR: « Et tu as suivi tous ceux qui comptaient. » Il sait exactement où poser ses mains, et votre corps s'en souvient avant vous. Il vous tient immobile par sa seule voix, et chacun de ses ordres est un ordre que vous lui avez appris à donner.

All four go to N8.

**N8 - Narrator**
- EN: The fire burns low. The blueprints lie where they fell. For a few hours, the Archduke of Baldur's Gate rules nothing beyond this room, and does not miss the rest.
- FR: Le feu baisse. Les plans restent là où ils sont tombés. Pendant quelques heures, l'Archiduc de la Porte de Baldur ne règne sur rien d'autre que cette pièce, et le reste ne lui manque pas.

Fade to black.

## Before dawn

**N9 - Narrator**
- EN: You wake before dawn. He is already awake, watching the ceiling, one arm around you as though he expects someone to come and collect you.
- FR: Vous vous éveillez avant l'aube. Il ne dort déjà plus et fixe le plafond, un bras autour de vous, comme s'il s'attendait à ce qu'on vienne vous réclamer.

**N10 - Gortash** `[Tav]`
- EN: Stay until the bells, my favourite problem. After that I must be a tyrant again, and you must save the world from people like me. But until the bells.
- FR: Reste jusqu'aux cloches, mon problème préféré. Ensuite, je devrai redevenir un tyran, et toi sauver le monde des gens de mon espèce. Mais jusqu'aux cloches.

**N10D - Gortash** `[Durge]` (Bhaal still has a hold on them)
- EN: You slept, my blade. No knives, no whispers, no blood on the sheets. Either your father's grip is slipping, or I am more soothing than my reputation suggests.
- FR: Tu as dormi, ma lame. Ni couteaux, ni murmures, ni sang sur les draps. Soit l'emprise de ton père faiblit, soit je suis plus apaisant que ma réputation ne le laisse croire.

**N10R - Gortash** `[Durge, rejected Bhaal]`
- EN: You slept, my blade. No knives, no whispers. I keep waiting for your father's voice to take you back from me, and it keeps not coming. I could grow used to that.
- FR: Tu as dormi, ma lame. Ni couteaux, ni murmures. J'attends sans cesse que la voix de ton père te reprenne à moi, et elle ne vient pas. Je pourrais m'y habituer.

## Choice D

| Id | Condition | EN | FR | Goes to |
|---|---|---|---|---|
| D1 | | Until the bells. | Jusqu'aux cloches. | N11 |
| D2 | | And once the brain is dealt with? What are we then? | Et une fois le cerveau vaincu ? Que serons-nous ? | N11b |
| D3 | `[Durge]` | If He takes me, you will be the first one I kill. | S'Il me prend, tu seras le premier que je tuerai. | N11d |
| D3R | `[Durge, rejected Bhaal]` | He has no hold on me now. What is left is mine. And yours. | Il n'a plus de prise sur moi. Ce qui reste est à moi. Et à toi. | N11r |

**N11b - Gortash**
- EN: Alive, if I have any say in it. Beyond that, I am open to negotiation. For the first time in my life, I should like to lose one.
- FR: En vie, si j'ai mon mot à dire. Pour le reste, je suis ouvert à la négociation. Pour la première fois de ma vie, j'aimerais en perdre une.

**N11d - Gortash** `[Durge]`
- EN: I know. I have known since the day we met. Stay anyway.
- FR: Je le sais. Je le sais depuis le jour de notre rencontre. Reste quand même.

**N11r - Gortash** `[Durge, rejected Bhaal]`
- EN: Then I am the richest man in Faerûn, and for once I did not steal it.
- FR: Alors je suis l'homme le plus riche de Faerûn, et pour une fois, je n'ai rien volé.

All three go to N11.

**N11 - Narrator** (sets `GR_Romance_Committed`)
- EN: He pulls you closer. Outside, the city he stole sleeps on, unaware that its tyrant is, at this moment, entirely conquered.
- FR: Il vous attire contre lui. Dehors, la ville qu'il a volée dort toujours, sans savoir que son tyran est, à cet instant, entièrement conquis.

## Open points

- `N10D` and `D3` are for a Dark Urge still under Bhaal's influence: hide them once Bhaal is rejected. `N10R`, `D3R` and `N11r` replace them in that case. `[Durge, rejected Bhaal]` is the base game global flag `ORI_DarkUrge_State_BhaalResisted` (set in `Act3b_LOW_BhaalTemple`).
- `N6D` assumes Gortash believed the Dark Urge dead after Orin's attack. Check it against what he says in the base game.
- For the Dark Urge, this night is a reunion: the two were lovers before the base game (see the backstory note in `GR_Office_Evening.md`).
- His private rooms do not exist as a location. The scene can play in the office behind the fade to black.
