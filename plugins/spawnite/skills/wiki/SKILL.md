---
name: wiki
description: Answer a question about the game platform, its engine or its ui from the platform's wiki. Use it when you need to know how a component, a behaviour, the camera, the player or a template works before you build with it.
argument-hint: <question>
context: fork
model: sonnet
background: false
---

Answer this question from the platform's wiki: $ARGUMENTS

1. Call the Spawnite server's `list_wiki` tool first, and pick the page whose use cases match the question. To see what the scaffold tools write, call `list_templates`.
2. When no use case matches, search with `search_wiki`. Use an export's name or a phrase from a page, in one or two words, and try two or three queries before you give up. Set `scope` to `reference` for an export's signature.
3. Read each page that looks relevant with `read_wiki`. A section address, such as `engine/entities/player#the-jump`, reads just that section.
4. Answer from what the pages say, not from what you expect. Quote a code sample exactly when the question is how to use something.

Reply with the answer, then the address of each page you read, such as `engine/behaviours/spin`. When no page answers the question, say so, and name the pages you read.
