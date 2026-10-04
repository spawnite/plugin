//  This duplicates `spawnite chat pending` (packages/cli/src/chat.ts) with
//  Node alone, so a hook starts without fetching the cli through npx on every
//  prompt and tool call. Change the CLI first; mirror here.

import {
    existsSync,
    mkdirSync,
    readdirSync,
    readFileSync,
    renameSync,
} from "node:fs";
import { basename, dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const event = process.argv[2];

//  A subagent's call carries agent_id: skipped, so a worker never takes
//  a message meant for the session. Input the hook cannot read counts as
//  the session's.
try {
    if (JSON.parse(readFileSync(0, "utf8")).agent_id) process.exit(0);
} catch {
    //  No payload, or not JSON.
}

/** Every game depends on the engine; a monorepo's root does not. */
function isGame(folder) {
    try {
        const manifest = JSON.parse(
            readFileSync(join(folder, "package.json"), "utf8"),
        );
        return "@spawnite/engine" in (manifest.dependencies ?? {});
    } catch {
        return false;
    }
}

/** Each .json under a folder, or none where it is missing. */
const listJson = (folder) =>
    existsSync(folder)
        ? readdirSync(folder)
              .filter((name) => name.endsWith(".json"))
              .map((name) => join(folder, name))
        : [];

/** The session's folder, then each folder under its games folder, as the
 *  monorepo keeps them. */
const folder = process.cwd();
const gamesFolder = join(folder, "games");
const candidates = [
    folder,
    ...(existsSync(gamesFolder)
        ? readdirSync(gamesFolder).map((name) => join(gamesFolder, name))
        : []),
];

//  Oldest first across the games, by the stamp that names each file.
const stamp = (file) => basename(file, ".json");
const files = candidates
    .filter(isGame)
    .flatMap((game) => listJson(join(game, ".spawnite", "chat")))
    .sort((first, second) => (stamp(first) < stamp(second) ? -1 : 1));

const rendered = files.flatMap((file) => {
    const { content } = JSON.parse(readFileSync(file, "utf8"));
    const read = join(dirname(file), "read");
    mkdirSync(read, { recursive: true });
    //  The MCP reads the same folder: a message it moved first is its own.
    try {
        renameSync(file, join(read, basename(file)));
    } catch {
        return [];
    }
    return [
        content
            .flatMap((block) =>
                block.type === "text"
                    ? [block.text]
                    : block.type === "resource_link"
                      ? [`Screenshot: ${fileURLToPath(block.uri)}`]
                      : [],
            )
            .join("\n\n"),
    ];
});

//  On Stop the message keeps the agent working, with the text as what to
//  do next; the next Stop finds it read and lets the agent stop. On
//  UserPromptSubmit it rides with what the person typed, and on PostToolUse
//  with the tool's result.
if (rendered.length > 0) {
    const text = `The creator sent these from the game's devtools chat:\n\n${rendered.join("\n\n---\n\n")}`;
    console.log(
        JSON.stringify(
            event === "Stop"
                ? { decision: "block", reason: text }
                : {
                      hookSpecificOutput: {
                          hookEventName: event,
                          additionalContext: text,
                      },
                  },
        ),
    );
}
