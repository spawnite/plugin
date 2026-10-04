# Character

Ask: who is the player, and where do they start? Offer the bodies from `engine/entities/player`: a primitive in any colour, a model from the asset library the player wears by name, or a VRM body. Recommend the one nearest to what the prompt names, or to what the games under **Inspiration** play as, or the default capsule when neither names one, and a start that faces what the round is about.

The meadow has an edge, and the character can walk off it and fall. Keep everything the round needs near the middle of the map, and end the round as a loss when the character falls: `player().transform[1]` drops below the ground.

Prove it: a screenshot of the start of a round, and one of the loss when the character walks off the edge, if the round can reach it.
