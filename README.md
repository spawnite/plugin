# Spawnite plugin

This repository is the plugin marketplace for [Spawnite](https://wiki.spawnite.com), a game platform built for coding agents. It holds the `spawnite` plugin for Claude Code: the Spawnite MCP server, the `game-builder`, `wiki` and `model-builder` skills, the `/spawnite:new-game` command, and the hooks that hand your agent what you send from a game's devtools. Each release of the `@spawnite` packages writes the plugin again, so its skills match the tools that npm serves.

## Install

Run the following commands once:

```sh
claude plugin marketplace add spawnite/plugin
claude plugin install spawnite@spawnite
```

Then start a new Claude Code session. Inside a session, `/plugin install spawnite --marketplace spawnite/plugin` does both in one command.

Claude Code doesn't update a plugin from this marketplace on its own. To receive each release, open `/plugin`, select **Marketplaces**, select `spawnite`, then select **Enable auto-update**. To update once instead, run `claude plugin update spawnite@spawnite`.

For Codex and other agents, and to check that the connection works, see [Connect your agent](https://wiki.spawnite.com/learn/connect-your-agent/).

## Licence

MIT No Attribution, in [LICENSE](LICENSE). The plugin runs `@spawnite/mcp` from npm, which carries its own licence.
