---
description: Create a new game project from a template, then say what to build first.
argument-hint: <example|mmorpg> <folder>
---

Create a new game with the `new_game` tool. The template is the first word of `$ARGUMENTS`, one of the registry's items: `example`, a lobby and a run through three coins to a goal ring, or `mmorpg`, the full game. The folder is the second word, resolved against the current directory to an absolute path.

After the tool returns, run `pnpm install` in the new folder, and tell me:

1. What the template already does, from its `package.json` description.
2. Which scaffold tools add to it: `add_behaviour`, `add_entity`, `add_npc`, `add_scene`, `add_panel` and `add_shader`, each taking the project's absolute path.
3. Where its items go: `src/items.ts` registers each item the game holds by name, with what it does as data. The example's holds one potion.
4. One question: what should the game do first?
