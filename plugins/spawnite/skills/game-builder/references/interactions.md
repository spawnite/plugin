# First interactions

Ask: what does the player do most, and what happens when they do it? Recommend what the prompt names the player doing, or what the games under **Inspiration** have them do, or picking things up when neither fits. For example: touch a coin and it is picked up, get touched by the monster and the round ends, stand on an answer and it is marked right or wrong.

Read `list_wiki` first: the engine already has behaviours for picking up (`engine/behaviours/pickup`), touching an area (`engine/behaviours/trigger`), chasing the player (`engine/behaviours/chase`) and pressing to use (`engine/behaviours/interact`). Use one before you write your own.

Build the round's end with it: a timer, a count, or a modal with the result and a button that starts again.

Keep areas the player must choose between far enough apart that walking to one never crosses another.

Prove it: one screenshot of each ending the round can have, each reached with `until`, and one of a second round, which must start clean.
