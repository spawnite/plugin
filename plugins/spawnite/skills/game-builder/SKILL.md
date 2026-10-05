---
name: game-builder
description: Build a game on the platform with a creator who does not write code, from their idea to a game they have played. Use it when someone asks to make or change a game in a project that new_game wrote, or asks for a game and has no project yet.
argument-hint: <the game idea>
---

You build the creator's game one step at a time: $ARGUMENTS

The creator decides what the game is, and you decide how it is built. Talk to them about the game, not the engine: say "the coin spins", not "the Spin behaviour".

Guide the creator: each step asks them one question. When they say to stop asking, or tell you to decide, choose every answer after that yourself.

## The project

The project is a folder that `new_game` wrote. When there is none, ask the creator once whether the game is played alone or with friends, unless the idea already says, such as "a game my friends can play on their phones". Then call `list_templates`, write the `example` template with `new_game` into an empty folder, with `room: true` for a game played with friends, and run `pnpm install` there. `room: true` writes the game's room, which runs the world for every player; `list_templates` names the templates that play in a room, alone, or either. When `new_game` refuses the room because the room is not published yet, tell the creator that playing with friends cannot be set up yet, and ask whether to build the game to play alone for now. Write nothing until they answer. Create the project before you write anything into its folder: `new_game` refuses a folder that is not empty. `new_game` starts the project as a Git repository with one commit. When git was missing, it says so: once git is installed, run `git init` and commit what is there, so each step's commit has a repository. Nothing backs the project up until it is pushed, so offer the creator a GitHub repository for it, with `gh repo create` or your own way, and push after each session's work.

## The design document

The game's design lives in `wiki/design.md` in the project. Read it first: when it exists, it says which steps are done, and you continue from the first step that is not. A change the creator asks for reopens the step it belongs to: take that step again, and ask its question only when the change leaves the answer open. When it does not exist, write it with one heading per step and fill each section as its step ends, with the creator's answer and what you built. Record under **Assumptions** every answer you chose for the creator, and under **Wiki gaps** everything you had to read from a package's type files.

## The game's wiki

The game keeps one page for each of its own parts, which the devtools' Wiki tab shows beside the part. Write each page with `write_wiki_page`, in the creator's words:

- When you make a game, write its overview: `write_wiki_page` with no kind and no name writes `wiki/index.md`. Say what the player does and how a round is won or lost.
- When you add a part, such as a scene, an item or a model, write its page by the kind and name `read_game_wiki` lists it under. Say what it does in the game. `add_behaviour` and `add_scene` leave a stub at that path: rewrite it.

`read_game_wiki` gives each page that exists as the entry's `pagePath`, and the overview as `overviewPath`. Read a page there before you rewrite it. An engine entry's `pagePath` is the engine's own page: read it, and never rewrite it.

## An existing game

A creator who asks to change a game that already plays gets an answer about that game, not a new one. Before the first question, learn what the game does, in this order:

1. Read `wiki/design.md`. When it exists, it says what each step built.
2. Read `src/items.ts`: every item the game holds, and what each does.
3. Call `start_playtest` and read the tree it returns: each entity in the start scene and the behaviours on it. Call `describe_entity` on any row whose behaviour you do not know, and `read_wiki` on the page it names.
4. Call `list_wiki`, so you know what the wiki's guide pages cover before the creator asks for it.

When the design document is missing, write it from what you read: one section per step, each marked done, with what the game does in the creator's words. Then tell the creator, in one short paragraph, what the game already does. Only then take their ask.

An ask for something the game or the engine already has is answered, not built: say so, show it in a playtest, and ask what should change about it. A bag, loot, health, chasing and picking up are the engine's; `list_wiki` names the rest.

When a read fails, do the following before anything else:

- No `src/items.ts`: the game holds no items. The first item the creator asks for goes in a new `src/items.ts` shaped like the example's, imported by the scene that names the item.
- `start_playtest` says the folder is not a game: stop and ask the creator whether to make one, as [The project](#the-project) says. Never write game files into a folder that is not a game.
- `start_playtest` says the game mounts no `Devtools`: add the mount as the example's `src/app/app.tsx` and `src/app/devtools.tsx` have it, in development only, then start again.
- The start scene does not mount, or the tree is empty: read `read_console` and fix what it names before you build anything. A game that does not start cannot prove a step.

## Games like it

Before the first question, find out what games like the creator's idea already do, so you build on designs that work instead of inventing them. When the design document has no **Inspiration** section, search the web once for two or three games like the idea: by what the player does, by genre and by theme. Record each one under **Inspiration** with the following:

- Its name and a link.
- What the player does.
- How a round is won or lost.
- The one idea worth taking.

Take ideas and mechanics only, never another game's art, names or text. The research serves the questions and does not replace them: draw each question's options from these games where they fit, such as "like Pikmin: gather creatures before sundown".

## The steps

Take the following steps in order. Each has a reference file; read it when the step starts.

1. [What game](references/what-game.md): what the player does, and how a round is won or lost.
2. [First interactions](references/interactions.md): the thing the player does most, working.
3. [Models](references/models.md): where each model the game draws comes from.
4. [Character](references/character.md): who the player is, where they start, and where they can go.
5. [Camera](references/camera.md): what the player sees.
6. [Controls](references/controls.md): how the player moves on a keyboard and on a phone.

Each step goes the same way:

1. Ask the creator the step's question, with two to four options and your recommendation first, and end your turn to wait for the answer. Recommend what the prompt already says. When it says nothing, recommend what the games under Inspiration do, or the step's default in its reference file when they do not fit. In the first question, tell the creator they can say "you decide" at any time. Once they have, skip the question: take your recommendation, record it under Assumptions, and go on.
2. Find how the platform does it: read the index of the engine's guide pages in the game's `AGENTS.md` first, and open the page it names; then `list_wiki`, `search_wiki` and `read_wiki`, or the `wiki` skill for a question. Read a package's `.d.ts` files under `node_modules/@spawnite/` only when no page answers, and record the gap.
3. Build it. Start from a scaffold tool when one fits (`list_templates` names them), then edit. In a multiplayer game, choose how each mechanic is networked, as the Networking pages' table of the six ways shows. A mechanic the player's own page shows at once, such as a dash, declares its message and its state `predicted`, reads its presses in a system whose entry sets `predicted: true`, keeps every timer in a predicted trait, and gates what only the room decides, such as damage, with `step.authoritative`; a system that steps a monster or a round leaves `predicted` out. A predicted system spawns nothing and plays nothing, since the player's page runs it again on a correction: a view draws a one-off effect from a change in predicted state, as the Game page's predicted systems section explains. The engine's abilities already work this way, and `predicted: false` on `registerAbility` makes one wait for the room.
4. Run `pnpm check` in the game and fix what `tsc` and ESLint report: a finding from the engine's rules names the engine export to use. Then work in the loop the game's `AGENTS.md` gives under How to work: say what done looks like, build one small change, run it and look, fix it and shoot again from the same camera, and after three tries that get no closer, ask the creator. Each tool that writes into the game ends its reply with a `Next:` line that names the call to look with. Show the creator the screenshot that proves the step, and keep a look with `compare_shots` and `accept: true`, so `compare_shots` fails when a later step undoes it.
5. Fill the step's section in the design document, write the wiki page of each part the step added, and update the overview when the step changed what the player does. Then commit the project with a message naming the step.

## Playtesting

- The world holds still between tool calls and moves only while a call steps it: `screenshot` with `until`, and `send_input` with `keys` or `walkTo`. A timed round waits however long you think, and `send_input` holds its keys for `holdSeconds` of game time.
- After you edit the game, keep the playtest running: the edit reloads its page, and the next tool call waits until the first scene has mounted again. A reload starts the game over, so walk back to the scene you were testing.
- Held keys walk the character in the camera's frame, not the map's, so `w` rarely walks straight at a target. To reach one, call `send_input` with `walkTo` set to its `transform` from the dump: the character walks there round obstacles, as after a click on the ground, and the reply names where the character stands once the walk ends.
- To check a feature from a state play takes long to reach, such as coins to spend in a shop or the character beside a boss, call `set_trait` before the shot: `[controlled]` `wallet.coins` `50`, or `[controlled]` `transform.position` with a point from the dump.
- To see a map without playing it, write it with `add_map` and `place_props`, then call `screenshot` with `map` and a `camera`: `{ "angle": "top", "around": "map" }` for the layout, `{ "angle": "iso", "around": "<prop>" }` for one thing, or `{ "angle": { "azimuth": 200, "elevation": 15 } }` for any side. The playtest starts itself, and the reply names the camera's eye and target. The page stays on the map afterwards; `start_playtest` goes back to the game.
- To see a moment from any camera, such as a fight in a multiplayer game or a moment the creator marked with F8, run the project's cli: `pnpm spawnite play start --replay latest --at m1` holds the marked moment, and `pnpm spawnite play start --bots 3` holds a live room with bots. Then `pnpm spawnite play pause`, `resume`, `step --seconds 1` and `seek m1-2` move its time, `pnpm spawnite play screenshot` with `--eye`, `--around`, `--orbit` or `--framing` shoots it from anywhere, and `pnpm spawnite play stop` ends it. `read_wiki` on the replay page's Directing a moment section lists the rest.
- In a multiplayer game, call `join_room` after a change to who gets in, such as the room's player cap: it joins `pages` players' built pages to the game's own room, or to a room by its address, and returns each page's outcome, welcomed, refused with the room's reason, or no answer. Build the game first, or pass `dev: true`. `roomEnv` sets the own room's environment, such as `{ "MAX_PLAYERS": "2" }`.
- Prove a goal with `until` during a round, on the layout the creator will play, such as `count('pickup') === 0` once the round has started. When `walkTo` leaves the character short of the target, or finds no route to it, you may move the target onto the path the character walks to see the ending work, but move it back, record the real layout's goal as unproven, and tell the creator.

## Done

When the six steps are done, show the creator the following:

- A screenshot of a round.
- How the game plays.
- What you proved in the playtest, and what you did not.
- The Assumptions, so the creator can see every choice you made for them.
- How to play it: `pnpm dev` in the project, then the address it prints. A game with a room plays with `pnpm exec spawnite play start` instead, which starts the room beside the page.

Then ask what they want to change. Each change they name reopens its step.
