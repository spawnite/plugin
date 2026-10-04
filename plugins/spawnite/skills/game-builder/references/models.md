# Models

Ask: where do the game's models come from? Name what the game still draws as a placeholder, such as the player's body or the things the round is about, and offer the following sources in this order, in the creator's words:

- **Ready-made, from the platform's library.** They are free and there at once. Find them with `list_assets`, and copy one into the game with `pnpm exec spawnite add asset <id>` in the project.
- **Made for the game in Blender.** They are free, and the creator installs Blender once. Make each model with the `model-builder` skill. When no Blender is found, `make_model` replies with the install command for the creator's computer: give them that command, and the [Blender page](https://wiki.spawnite.com/learn/blender/).
- **Files the creator brings,** from any tool, such as Meshy, Tripo or Sketchfab. Put each file in `public/assets/`, check it with `check_model` and against the Models page (`read_wiki`, page `learn/models`), and ask the creator to check that its licence lets them publish it in their game.

Recommend the library when it holds a model that fits the game, and Blender otherwise. When the creator has said "you decide", take the same default. The creator may mix sources, such as the library for the trees and Blender for the character.

A model that breaks a rule on the Models page still draws, and the bake names the rule. Fix what the bake names before the step ends.

Prove it: a screenshot of each new model in the game, standing where the round uses it.
