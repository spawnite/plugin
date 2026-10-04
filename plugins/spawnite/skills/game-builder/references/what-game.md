# What game

Ask: what does the player do, and how does a round end? Offer a win, a loss and a length that fit the idea, taken from the games under **Inspiration** where they fit, such as "collect every coin before 30 seconds run out, or the time runs out", and recommend the one closest to the prompt. When neither the prompt nor those games give a goal, recommend collecting every pickup before 30 seconds run out. A game can have no loss.

Write under **What game** in the design document:

- One sentence the creator would say about the game.
- How a round is won, how it is lost, and how long it lasts.
- Anything the creator named: a number, a theme, questions, a name.

Build: name the game in `index.html` and the lobby's text, and state the rules on the lobby's screen. Remove what the template shows that this game does not use, such as the goal ring. The template's coin readout, `Readout` in `src/app/app.tsx`, sits outside every scene and shows the wallet that pickups fill. A game that keeps score relabels it and shows its score there, rather than drawing a second counter. A game with no score removes it.

Prove it: a screenshot of the lobby with the game's name and rules.
