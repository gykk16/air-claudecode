---
name: write-tests
description: Delegate a test generation task to the test-engineer agent. Use when the user asks to write, generate, or add tests for Kotlin or Java code.
context: fork
agent: test-engineer
background: false
argument-hint: "[target class or method to test]"
---

# Write Tests

Delegates a test generation task to the `test-engineer` agent,
which works in its own context following the plugin's test rules.

## Usage

```
/software-engineer:write-tests <target class or method>
```

Include enough context in the task description — the agent cannot see the
conversation: target class/method, scenarios that matter, and any scope limits.

## Task

Write tests for: $ARGUMENTS

You are working from the task description alone. If the test scope is ambiguous
(which class/method, which scenarios), ask via AskUserQuestion before writing —
do not guess.

## Report

When done, report back:

- What was tested and why (scenarios covered)
- Test files created or modified
- Test run result (`./gradlew test`)
