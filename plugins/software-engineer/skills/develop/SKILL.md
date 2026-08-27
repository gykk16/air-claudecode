---
name: develop
description: Delegate a code implementation task (feature, bug fix, refactoring) to the software-engineer agent. Use when the user asks to implement, fix, or refactor Kotlin/Java/Spring code.
context: fork
agent: software-engineer
background: false
argument-hint: "[task description]"
---

# Develop

Delegates a code implementation task to the `software-engineer` agent,
which works in its own context following the plugin's coding guidelines.

## Usage

```
/software-engineer:develop <task description>
```

Include enough context in the task description — the agent cannot see the
conversation: target module/files, expected behavior, and any constraints.

## Task

Implement the following task: $ARGUMENTS

You are working from the task description alone. If it is ambiguous or missing
context (target module, expected behavior, edge cases), ask via AskUserQuestion
before implementing — do not guess.

## Report

When done, report back:

- What changed and why
- Which files were touched
- How it was verified (build, tests, review)
