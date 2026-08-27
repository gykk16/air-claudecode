---
name: write
description: Delegate writing a new technical document (README, get-started, tutorial, how-to, API reference, troubleshooting, concept doc) to the technical-writer agent. Use when the user asks to write or create documentation.
context: fork
agent: technical-writer
background: false
argument-hint: "[document topic, audience, and purpose]"
---

# Write

Delegates writing a new document to the `technical-writer` agent,
which classifies the document type, structures it, drafts, and polishes
following the plugin's writing guide.

## Usage

```
/technical-writer:write <document topic, audience, and purpose>
```

Include enough context — the agent cannot see the conversation:
what the document covers, who reads it, and where it will live
(target file path or docs directory).

## Task

Write the following document: $ARGUMENTS

You are working from the task description alone. If the audience or purpose
is unclear, ask via AskUserQuestion before writing — the document type
decision depends on it. If no target location is given, use your default
output location rules.

## Report

When done, report back:

- Document type chosen and why
- Files created, with a brief outline of each
- Anything marked `[확인 필요]` that needs the author's verification
