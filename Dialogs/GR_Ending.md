# Step 5 - Ending where he survives

Dialogue script to build in the Toolkit dialog editor. Text only, no voice.
Notation and gender variants are explained in the README.

## Requirements

- Alliance with Gortash intact, Gortash alive.
- `GR_Romance_Committed` set, `GR_Romance_Ended` not set.

In French, Gortash and the player say "tu" (since step 4). The narrator keeps "vous".

## Flags

| Flag | Set by | Meaning |
|---|---|---|
| `GR_Gortash_Saved` | part A, `A1` to `A3` | He survives the brain |
| `GR_Romance_Ended` | part B, choice `D4` | They part ways after the battle |
| `GR_Left_City` | part B, choice `D3` | The player leaves Baldur's Gate, picks the second epilogue letter |

## Feasibility

- **Part A** changes a scripted scene of the base game (his death in front of the brain). It is the hardest piece of the whole mod and may need the base dialogue to be overridden.
- **Part B** is a new scene after the final battle, also inside the scripted ending sequence.
- **Part C** is one letter at the reunion party: by far the easiest. It can ship first, on its own.

---

## Part A - In front of the brain

Replaces his death when the three Netherstones are used.

**N1 - Narrator**
- EN: The three Netherstones blaze. The brain's voice fills the cavern, and Gortash, at your side, raises his stone with the certainty of a man who has never once been outbid.
- FR: Les trois pierres infernales flamboient. La voix du cerveau emplit la caverne, et Gortash, à vos côtés, lève sa pierre avec l'assurance d'un homme sur qui personne n'a jamais surenchéri.

**N2 - Narrator**
- EN: Then the certainty leaves his face. The brain is not yielding. It is reaching for him.
- FR: Puis l'assurance quitte son visage. Le cerveau ne cède pas. Il se tend vers lui.

### Choice A

| Id | EN | FR | Goes to |
|---|---|---|---|
| A1 | *Throw yourself between him and the brain's will.* | *Vous jeter entre lui et la volonté du cerveau.* | N3a |
| A2 | *Tear the Netherstone from his hand.* | *Lui arracher la pierre infernale des mains.* | N3b |
| A3 | Enver! Let go! | Enver ! Lâche-la ! | N3c |
| A4 | *Do nothing.* | *Ne rien faire.* | base game scene, he dies |

**N3a - Narrator**
- EN: Its will hits you like a wall of black water. The tadpole behind your eye screams. But you have withstood this voice before, and for one heartbeat it has to choose between the two of you. One heartbeat is enough.
- FR: Sa volonté vous frappe comme un mur d'eau noire. La larve derrière votre œil hurle. Mais vous avez déjà résisté à cette voix, et le temps d'un battement de cœur, elle doit choisir entre vous deux. Ce battement suffit.

**N3b - Narrator**
- EN: You wrench the stone from his fingers. The link snaps. He staggers back like a man cut down from a rope, blood running from his nose, alive.
- FR: Vous arrachez la pierre de ses doigts. Le lien se rompt. Il recule en titubant comme un homme qu'on décroche d'une corde, le nez en sang, vivant.

**N3c - Narrator**
- EN: For a man who has never obeyed anyone, he obeys at once. The stone falls. The brain's grip closes on empty air.
- FR: Pour un homme qui n'a jamais obéi à personne, il obéit sur-le-champ. La pierre tombe. L'étreinte du cerveau se referme sur le vide.

All three set `GR_Gortash_Saved` and go to N4.

**N4 - Gortash**
- EN: It was never going to kneel. All my arithmetic, and not once did I account for... You. You were in none of my sums.
- FR: Il n'allait jamais s'agenouiller. Tous mes calculs, et pas une fois je n'ai pris en compte... Toi. Tu n'étais dans aucun de mes calculs.

**N5 - Narrator**
- EN: He is in no state to fight. The stone is yours now. So is what comes next.
- FR: Il n'est plus en état de se battre. La pierre est à vous, désormais. La suite aussi.

### Choice B

| Id | Condition | EN | FR | Goes to |
|---|---|---|---|---|
| B1 | | Get out of here. Live. That is an order, Archduke. | Sors d'ici. Vis. C'est un ordre, Archiduc. | N6a |
| B2 | | You have done enough. Let me finish this. | Tu en as assez fait. Laisse-moi finir. | N6b |
| B3 | `[Durge]` | I lost you once without even remembering it. Not again. | Je t'ai perdu une fois sans même m'en souvenir. Pas deux. | N6d |

**N6a - Gortash**
- EN: I do not take orders. I shall make one exception. Come back to me, or I will be extremely put out.
- FR: Je ne reçois pas d'ordres. Je ferai une exception. Reviens-moi, ou je serai extrêmement contrarié.

**N6b - Gortash**
- EN: Finish it, then. And be quick. I have discovered I am very bad at waiting for you.
- FR: Finis-en, alors. Et vite. Je découvre que je supporte très mal de t'attendre.

**N6d - Gortash** `[Durge]`
- EN: Then remember this instead.
- FR: Alors souviens-toi plutôt de ceci.

**N6d2 - Narrator** `[Durge]`
- EN: He kisses you, quick and fierce, tasting of blood, and lets you go.
- FR: Il vous embrasse, vite et fort, un goût de sang aux lèvres, puis vous laisse partir.

The base game ending continues from here, without him in the fight.

---

## Part B - After the battle

Requires `GR_Gortash_Saved`. Two versions, depending on what the player did with the brain.

### Docks - The brain is destroyed

**DN1 - Narrator**
- EN: The brain sinks into the Chionthar. On the ruined docks, a man in a torn black coat is waiting, with no guards, no gauntlet, and no speech prepared.
- FR: Le cerveau s'abîme dans le Chionthar. Sur les quais en ruine, un homme en manteau noir déchiré attend, sans gardes, sans gantelet, et sans discours préparé.

**DN1b - Flaming Fist** (overheard)
- EN: That's the one who saved the city. And [he / she / they] went straight to him. Gods help us all.
- FR: C'est [lui / elle / ellui] qui a sauvé la ville. Et [il / elle / iel] va droit vers lui. Que les dieux nous gardent.

**DN2 - Gortash**
- EN: You destroyed it. The most valuable asset this world has ever produced, and you dropped it in a river. And I find I would have paid more than that to see you walk out alive. Do not tell my creditors.
- FR: Tu l'as détruit. L'actif le plus précieux que ce monde ait jamais produit, et tu l'as jeté dans un fleuve. Et je découvre que j'aurais payé plus cher encore pour te voir en sortir en vie. N'en dis rien à mes créanciers.

| Id | EN | FR | Sets flag | Goes to |
|---|---|---|---|---|
| D1 | You still have a city. Try ruling it without a god in your pocket. | Il te reste une ville. Essaie de la gouverner sans un dieu dans la poche. | | DN3a |
| D2 | No more tyrants, Enver. Not even you. | Plus de tyrans, Enver. Pas même toi. | | DN3b |
| D3 | I'm leaving Baldur's Gate. | Je quitte la Porte de Baldur. | `GR_Left_City` | DN3c |
| D4 | This ends here. I saved your life. Do something with it that I won't have to come back and correct. | Tout s'arrête ici. Je t'ai sauvé la vie. Fais-en quelque chose que je n'aurai pas à revenir corriger. | `GR_Romance_Ended` | DN3x |

**DN3a - Gortash**
- EN: No god, no brain, no Chosen's title. Just a cobbler's son with a crown. It will be the hardest thing I have ever built. Stay, and watch me get it wrong?
- FR: Ni dieu, ni cerveau, ni titre d'Élu. Rien qu'un fils de cordonnier avec une couronne. Ce sera la chose la plus difficile que j'aie jamais bâtie. Reste, et regarde-moi me tromper ?

**DN3b - Gortash**
- EN: I can offer "fewer". One, to be exact, and under supervision. Yours.
- FR: Je peux proposer « moins ». Un seul, pour être précis, et sous surveillance. La tienne.

**DN3c - Gortash**
- EN: Then its gates will stay open for you. And I have a talent for letters, as you may have noticed.
- FR: Alors ses portes te resteront ouvertes. Et j'ai un certain talent pour les lettres, tu l'auras remarqué.

All three go to DN4.

**DN3x - Gortash**
- EN: A harder bargain than any devil ever offered me. Accepted.
- FR: Un marché plus dur que tout ce qu'un diable m'a jamais proposé. Accepté.

End of dialogue.

**DN4 - Narrator**
- EN: He takes your hand, bare fingers through yours, in front of the whole broken, breathing city.
- FR: Il prend votre main, ses doigts nus entre les vôtres, devant toute la ville, brisée mais vivante.

### Throne - The player takes control of the brain

**RN1 - Narrator**
- EN: The brain bends to your will. Every mind beneath the Absolute turns towards you like wheat in the wind. One does not turn. He walks.
- FR: Le cerveau plie sous votre volonté. Tous les esprits soumis à l'Absolue se tournent vers vous comme les blés sous le vent. Un seul ne se tourne pas. Il marche.

**RN2 - Gortash**
- EN: So. It kneels to you. I spent years on that design, and you take it in an afternoon. Tell me there is a seat beside that throne. I did draw up the plans.
- FR: Ainsi, il s'agenouille devant toi. J'ai passé des années sur ce projet, et tu t'en empares en un après-midi. Dis-moi qu'il y a un siège à côté de ce trône. C'est tout de même moi qui ai dessiné les plans.

| Id | EN | FR | Goes to |
|---|---|---|---|
| R1 | There always was. | Il y en a toujours eu un. | RN3a |
| R2 | Kneel, Enver. | À genoux, Enver. | RN3b |

**RN3a - Gortash**
- EN: Then let us show the world what a proper tyranny looks like. Together. I shall handle the paperwork.
- FR: Alors montrons au monde à quoi ressemble une tyrannie digne de ce nom. Ensemble. Je m'occupe des formalités.

**RN3b - Narrator**
- EN: He looks at you for a long moment. Then, slowly, the Archduke of Baldur's Gate goes down on one knee.
- FR: Il vous regarde un long moment. Puis, lentement, l'Archiduc de la Porte de Baldur met un genou à terre.

**RN3b2 - Gortash**
- EN: For you. Once. And never in public.
- FR: Pour toi. Une fois. Et jamais en public.

Both go to RN4.

**RN4 - Narrator**
- EN: The empire of the Absolute will be remembered for its cruelty, its order, and its two thrones. No chronicle will record that its tyrants were happy. They were.
- FR: De l'empire de l'Absolue, on retiendra la cruauté, l'ordre, et ses deux trônes. Aucune chronique ne dira que ses tyrans étaient heureux. Ils l'étaient.

This line stands in for an epilogue letter: the reunion party does not happen in this ending.

---

## Part C - Letter at the reunion party

Requires `GR_Gortash_Saved`, the brain destroyed, `GR_Romance_Ended` not set. Delivered with the other letters at the party, six months later.

**EPILOGUE_NAME - Item name**
- EN: Letter from Enver
- FR: Lettre d'Enver

**EPILOGUE_DESC - Item description**
- EN: Black wax again, but the seal has been pressed with a thumb, not a crest.
- FR: De la cire noire, encore, mais le sceau a été marqué du pouce, pas d'un blason.

**EPILOGUE_TEXT - Item content**
- EN: I am told a gathering of heroes is being held tonight, and that an Archduke would "spoil the mood". I am choosing not to be offended.<br><br>Six months. The city still stands, the patriars still loathe me, and this season I have signed three laws that benefit someone other than myself. I blame you entirely.<br><br>Come home when the wine runs out. I have kept the good bottle, and the door, as ever, is unlocked.<br><br>Enver<br><br>P.S. This one is a summons.
- FR: On me dit qu'une assemblée de héros se tient ce soir, et qu'un Archiduc y « gâcherait l'ambiance ». Je choisis de ne pas m'en offusquer.<br><br>Six mois. La ville tient debout, les patriars me détestent toujours, et j'ai signé cette saison trois lois qui profitent à quelqu'un d'autre que moi. Je t'en tiens pour entièrement responsable.<br><br>Rentre quand il n'y aura plus de vin. J'ai gardé la bonne bouteille, et la porte, comme toujours, n'est pas fermée à clé.<br><br>Enver<br><br>P.S. Cette fois, c'est une convocation.

**EPILOGUE_AWAY_TEXT - Item content** (used when `GR_Left_City` is set, same name and description)
- EN: I am told a gathering of heroes is being held tonight, somewhere I am not. I am choosing not to be offended.<br><br>Six months. You said you were leaving Baldur's Gate, and I said its gates would stay open. They have. I have had the hinges oiled twice.<br><br>I will not ask where you are. I have people for that, and I have forbidden them to tell me. It is the most restraint I have ever shown, and I resent every day of it.<br><br>Come back when the road runs out. The good bottle is still unopened.<br><br>Enver
- FR: On me dit qu'une assemblée de héros se tient ce soir, quelque part où je ne suis pas. Je choisis de ne pas m'en offusquer.<br><br>Six mois. Tu as dit que tu quittais la Porte de Baldur, et j'ai dit que ses portes resteraient ouvertes. Elles le sont. J'en ai fait huiler les gonds deux fois.<br><br>Je ne demanderai pas où tu es. J'ai des gens pour cela, et je leur ai interdit de me le dire. C'est la plus grande retenue dont j'aie jamais fait preuve, et j'en maudis chaque jour.<br><br>Reviens quand la route s'arrêtera. La bonne bouteille n'est toujours pas ouverte.<br><br>Enver

## Open points

- Part A describes his death in the base game from memory. Check the exact scene before writing the override.
