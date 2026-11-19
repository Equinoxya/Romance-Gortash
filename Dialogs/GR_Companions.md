# Extension - Companion reactions

How the companions react once the romance is open. Notation is explained in the README.

## How it works

- Requires: `GR_Romance_Interested`, and the companion in the party.
- Each reaction is a short camp dialogue, added as a new option or an opening line in that companion's camp dialogue. It plays once.
- Karlach has a full scene: Gortash sold her to Zariel. The others have one exchange each.
- In French, the companions say "tu" to the player. Check it against how each one speaks in the base game.

## Flags

| Flag | Set by | Meaning |
|---|---|---|
| `GR_React_Karlach` and one per companion | start of each reaction | The reaction cannot be replayed |
| `GR_Karlach_Furious` | `KB4` | Karlach refuses to talk about it again |
| `GR_Romance_Ended` | `KB3` | The player ends the romance for her |

---

## Karlach

**K1 - Karlach**
- EN: Tell me that letter isn't what I think it is. Black wax. His crest. In OUR camp.
- FR: Dis-moi que cette lettre n'est pas ce que je crois. De la cire noire. Ses armoiries. Dans NOTRE camp.

### Choice KA

| Id | EN | FR | Goes to |
|---|---|---|---|
| KA1 | It's an alliance, Karlach. Nothing else. | C'est une alliance, Karlach. Rien d'autre. | K2a |
| KA2 | It's what you think it is. | C'est bien ce que tu crois. | K2b |
| KA3 | I should have told you. I'm sorry. | J'aurais dû te le dire. Pardon. | K2c |

**K2a - Karlach**
- EN: Don't. I can smell a lie the way I smell smoke. He writes to you like that and you call it an alliance?
- FR: Arrête. Je sens un mensonge comme je sens la fumée. Il t'écrit comme ça, et tu appelles ça une alliance ?

**K2b - Karlach**
- EN: Fuck. Okay. At least you said it to my face.
- FR: Merde. D'accord. Au moins, tu me l'as dit en face.

**K2c - Karlach**
- EN: Yeah. You should have.
- FR: Ouais. Tu aurais dû.

All three go to K3.

**K3 - Karlach**
- EN: He sold me. I was his bodyguard, I'd have died for him, and he sold me to Zariel like a crate of scrap. Ten years in Avernus with an engine where my heart was. And you look at that man and see something worth keeping?
- FR: Il m'a vendue. J'étais sa garde du corps, je serais morte pour lui, et il m'a vendue à Zariel comme une caisse de ferraille. Dix ans en Averne, avec un moteur à la place du cœur. Et toi, tu regardes cet homme et tu y vois quelque chose qui vaut la peine d'être gardé ?

### Choice KB

| Id | Condition | EN | FR | Sets flag | Goes to |
|---|---|---|---|---|---|
| KB1 | | I see what he did to you. I won't ask you to forgive it. | Je vois ce qu'il t'a fait. Je ne te demanderai pas de le pardonner. | | K4a |
| KB2 | | He's changing. I've seen it. | Il change. Je l'ai vu. | | K4b |
| KB3 | | You're right. I'll end it. | Tu as raison. Je vais y mettre fin. | `GR_Romance_Ended` | K4c |
| KB4 | | This is my life, Karlach. Not yours. | C'est ma vie, Karlach. Pas la tienne. | `GR_Karlach_Furious` | K4d |
| KB5 | `[Durge]` | I loved him before I lost myself. I'm trying to find out what's left. | Je l'aimais avant de me perdre. J'essaie de savoir ce qu'il en reste. | | K4e |

**K4a - Karlach**
- EN: Good. Because I won't. But I'm not walking out on you either. Not yet. Just don't ever ask me to stand in a room with him and smile.
- FR: Tant mieux. Parce que je ne le ferai pas. Mais je ne te laisse pas tomber non plus. Pas encore. Ne me demande juste jamais de rester dans la même pièce que lui en souriant.

**K4b - Karlach**
- EN: Men like him don't change, soldier. They just find better reasons. I hope I'm wrong. Gods, I hope I'm wrong, for your sake.
- FR: Les hommes comme lui ne changent pas, soldat. Ils se trouvent juste de meilleures raisons. J'espère me tromper. Bons dieux, j'espère me tromper, pour toi.

**K4c - Karlach**
- EN: Thank you. I know what that costs. I do.
- FR: Merci. Je sais ce que ça coûte. Vraiment.

**K4d - Karlach**
- EN: Right. Your life. Then here's mine: I need some air, and I need you not to follow me.
- FR: C'est ça. Ta vie. Alors voilà la mienne : j'ai besoin d'air, et j'ai besoin que tu ne me suives pas.

**K4e - Karlach**
- EN: That's... hells. That's a lot to carry. I still hate him. But I get needing to know.
- FR: C'est... par les enfers. C'est lourd à porter. Je le déteste toujours. Mais je comprends qu'on ait besoin de savoir.

---

## Astarion

**AS1 - Astarion**
- EN: The Archduke. Really. You do realise most people settle for flowers, not a tyrant with a private army? I'm not judging. I'm taking notes.
- FR: L'Archiduc. Vraiment. Tu sais que la plupart des gens se contentent de fleurs, pas d'un tyran avec une armée privée ? Je ne juge pas. Je prends des notes.

| Id | EN | FR | Goes to |
|---|---|---|---|
| ASA | Jealous? | Tu es jaloux ? | AS2a |
| ASB | It's complicated. | C'est compliqué. | AS2b |

**AS2a - Astarion**
- EN: Of him? Darling, please. Of the wine cellar, perhaps.
- FR: De lui ? Allons donc, trésor. De sa cave à vin, peut-être.

**AS2b - Astarion**
- EN: It always is, with the ones who own dungeons. Do be careful. I say that with entirely selfish concern.
- FR: Ça l'est toujours, avec ceux qui possèdent des cachots. Fais attention à toi, tout de même. Je le dis par pur égoïsme.

## Shadowheart

**SH1 - Shadowheart**
- EN: A man who trades in secrets and control. I was raised by people like that. They are very good at making a cage feel like a gift.
- FR: Un homme qui fait commerce de secrets et de contrôle. J'ai été élevée par des gens comme lui. Ils savent très bien donner à une cage des airs de cadeau.

| Id | EN | FR | Goes to |
|---|---|---|---|
| SHA | I know what he is. | Je sais ce qu'il est. | SH2a |
| SHB | He's different with me. | Il est différent avec moi. | SH2b |

**SH2a - Shadowheart**
- EN: Then you are ahead of where I was. Stay there.
- FR: Alors tu as de l'avance sur celle que j'étais. Garde-la.

**SH2b - Shadowheart**
- EN: They always are. That is how it works. I hope you are the exception.
- FR: Ils le sont toujours. C'est comme ça que ça marche. J'espère que tu seras l'exception.

## Wyll

**WY1 - Wyll**
- EN: My father sits in that man's fortress with a tadpole behind his eyes. And you dine there. I'm trying to understand, truly. Help me.
- FR: Mon père est dans la forteresse de cet homme, une larve derrière les yeux. Et toi, tu y dînes. J'essaie de comprendre, sincèrement. Aide-moi.

| Id | EN | FR | Goes to |
|---|---|---|---|
| WYA | I'm closer to him than any blade could get. I can help your father. | Je suis plus près de lui qu'aucune lame ne pourrait l'être. Je peux aider ton père. | WY2a |
| WYB | I can't explain it, Wyll. | Je ne peux pas l'expliquer, Wyll. | WY2b |

**WY2a - Wyll**
- EN: Then use it. If any part of this is for him, I can bear the rest.
- FR: Alors sers-t'en. Si une part de tout cela est pour lui, je supporterai le reste.

**WY2b - Wyll**
- EN: No. I don't suppose you can. I'll keep my blade out of it, for you. I can't promise more.
- FR: Non. J'imagine que non. Je garderai ma lame au fourreau, pour toi. Je ne peux pas promettre davantage.

## Gale

**GA1 - Gale**
- EN: I once loved a goddess, so I am poorly placed to lecture anyone on unwise attachments to the powerful. I will only say this: it ended with a bomb in my chest.
- FR: J'ai aimé une déesse, je suis donc mal placé pour sermonner quiconque sur les attachements imprudents envers les puissants. Je dirai seulement ceci : cela s'est terminé avec une bombe dans ma poitrine.

| Id | EN | FR | Goes to |
|---|---|---|---|
| GAA | Noted. | C'est noté. | GA2a |
| GAB | He's not Mystra. | Il n'est pas Mystra. | GA2b |

**GA2a - Gale**
- EN: That is all I ask. That, and an invitation, should there be a wedding. I am told his cellar is superb.
- FR: C'est tout ce que je demande. Cela, et une invitation, s'il devait y avoir un mariage. On dit sa cave remarquable.

**GA2b - Gale**
- EN: No. Mystra never pretended to be anything other than a god. Do mind the difference.
- FR: Non. Mystra n'a jamais prétendu être autre chose qu'une déesse. Garde cette différence en tête.

## Lae'zel

**LA1 - Lae'zel**
- EN: The tyrant is strong, and he bends for you. Among my people, this would be called a conquest. See that the conquest is yours.
- FR: Le tyran est fort, et il plie devant toi. Chez les miens, on appellerait cela une conquête. Veille à ce que cette conquête soit la tienne.

## Minthara

**MI1 - Minthara**
- EN: Finally, a choice I respect. Power should bed power. Do not let him forget which of you is the greater danger.
- FR: Enfin un choix que je respecte. Le pouvoir doit s'unir au pouvoir. Ne le laisse pas oublier qui de vous deux représente le plus grand danger.

## Jaheira

**JA1 - Jaheira**
- EN: I have buried better people than Enver Gortash for less than he has done. I will not bury you beside him. Remember that when the time comes to choose.
- FR: J'ai enterré des gens meilleurs qu'Enver Gortash pour moins que ce qu'il a fait. Je ne t'enterrerai pas à ses côtés. Souviens-t'en quand viendra l'heure de choisir.

## Open points

- Karlach leaving the party after `KB4` is not scripted. For now she only stops talking about it.
- `WY1` assumes Wyll's father is held at Wyrm's Rock. Hide the line if he has already been freed.
