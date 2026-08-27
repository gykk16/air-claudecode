---
name: review
description: Delegate a technical document review to the technical-writer agent — document type fit, information architecture, and sentence quality, reported by severity with fixes. Use when the user asks to review or improve documentation.
context: fork
agent: technical-writer
background: false
argument-hint: "[document file or directory]"
---

# Review

Delegates a document review to the `technical-writer` agent, which diagnoses
the document against the writing guide and reports issues by severity.

## Usage

```
/technical-writer:review <document file or directory>
```

The agent cannot see the conversation — name the target file(s) explicitly.

## Task

Review the following document(s): $ARGUMENTS

Read the entire document first, then diagnose in checklist order
(type fit → information architecture → sentences) using
`${CLAUDE_PLUGIN_ROOT}/references/review-checklist.md`.

Report issues only — do NOT modify the document unless the task explicitly
asks you to apply the fixes.

## Report

Return findings ordered by severity (🔴 → 🟡 → 🟢), each with location,
one-sentence problem statement, and a paste-ready fix.
Group repeated problems of the same kind.
