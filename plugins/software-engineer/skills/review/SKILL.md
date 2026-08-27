---
name: review
description: Delegate a comprehensive code review to the code-reviewer agent — quality, security, performance, testing, with severity-rated Korean output. Use when the user asks to review code, a diff, or a PR.
context: fork
agent: code-reviewer
background: false
argument-hint: "[target file, directory, or PR number]"
---

# Review

Delegates a comprehensive code review to the `code-reviewer` agent,
which reviews in its own context and returns a severity-rated report in Korean.

## Usage

```
/software-engineer:review <target file, directory, or PR number>
```

With no target, the agent reviews the current `git diff`.
The agent cannot see the conversation — name the target explicitly
when it is not the current working tree changes.

## Task

Review the following target: $ARGUMENTS

If no target is given, review the current uncommitted changes (`git diff`).
If the target is a PR number, use `gh pr diff` to get the changes.
If the target is ambiguous, ask via AskUserQuestion before reviewing.

## Report

Return the full structured review (PR Review Summary format, in Korean),
including severity tables, statistics, and the checklist summary.
