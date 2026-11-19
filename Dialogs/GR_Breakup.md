# Extension - Breakup letter

A last letter if the player ends the romance. Notation is explained in the README.

## How it works

- Trigger: `GR_Romance_Ended`. The letter arrives at the next long rest (`GR_Letters.txt`).
- Two versions, because of the French "vous" / "tu" rule:
  - `BREAKUP1`: `GR_First_Names` is not set (the romance ended at the ball, at the foundry, with Karlach).
  - `BREAKUP2`: `GR_First_Names` is set (the romance ended during or after the private night).
- Both use the same item name and description.
- Not sent if the romance ends in the final scene on the docks: there is no long rest after it.

---

**BREAKUP_NAME - Item name**
- EN: Letter with No Signature
- FR: Lettre sans signature

**BREAKUP_DESC - Item description**
- EN: Black wax, unstamped. The handwriting is steadier than it would like to be.
- FR: Cire noire, sans sceau. L'écriture est plus ferme qu'elle ne voudrait l'être.

**BREAKUP1_TEXT - Item content**
- EN: I do not write twice to people who refuse me. Consider this the exception that proves the habit.<br><br>Your answer was clear, and I was owed nothing else. The alliance stands. I keep my contracts, even when they have stopped being pleasant.<br><br>I will only ask you to return the invitation. Not for security. I find I do not like the thought of it lying about your camp, amusing your friends.<br><br>That is all. It was, I am told, a very good ball.
- FR: Je n'écris pas deux fois à ceux qui me refusent. Voyez ceci comme l'exception qui confirme l'habitude.<br><br>Votre réponse était claire, et je n'avais droit à rien d'autre. L'alliance tient. J'honore mes contrats, même quand ils ont cessé d'être agréables.<br><br>Je vous demanderai seulement de me rendre l'invitation. Pas par sécurité. Je découvre que je n'aime pas l'idée qu'elle traîne dans votre camp et amuse vos amis.<br><br>C'est tout. Ce fut, paraît-il, un très beau bal.

**BREAKUP2_TEXT - Item content**
- EN: The door is locked again. I thought you should hear it from me, and not from the handle.<br><br>I will not pretend this is a matter of business. I made you an offer with nothing held back, which I have done exactly once, and you declined it. That is your right. It is also the last time.<br><br>The alliance stands. Once the brain is dealt with, we need never be in the same room again.<br><br>Keep the wine.
- FR: La porte est de nouveau fermée à clé. J'ai pensé que tu devais l'apprendre de moi, et non de la poignée.<br><br>Je ne prétendrai pas qu'il s'agit d'affaires. Je t'ai fait une offre sans rien garder pour moi, ce qui m'est arrivé exactement une fois, et tu l'as déclinée. C'est ton droit. C'est aussi la dernière fois.<br><br>L'alliance tient. Une fois le cerveau vaincu, nous n'aurons plus jamais à nous trouver dans la même pièce.<br><br>Garde le vin.
