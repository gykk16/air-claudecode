---
name: super-engineer
description: End-to-end development workflow — implement with the software-engineer agent, generate tests with the test-engineer agent, review with the code-reviewer agent, and loop fixes until the review passes. Use when the user wants a task developed with quality gates in one go.
argument-hint: "[task description]"
---

# Super Engineer

Orchestrates this plugin's three agents into one quality-gated workflow.
Runs inline: this conversation drives the loop and delegates each phase
to the matching agent.

Task: $ARGUMENTS

## Workflow

1. **Develop** — delegate the task to the `software-engineer` agent.
2. **Test** — if the change contains testable logic (business rules, branches,
   error paths), delegate test generation for the changed code to the
   `test-engineer` agent. Skip for pure config/docs/rename changes and say so.
3. **Review** — delegate a review of all changes (including tests) to the
   `code-reviewer` agent.
4. **Gate** — decide from the review result:
   - **Approved** (no P0/P1 issues): done — go to Report.
   - **Not approved**: send the P0/P1 findings back to the `software-engineer`
     agent as a fix task, then return to step 3. Fix P2/NIT only when trivial.
5. **Iteration cap** — at most 3 develop→review cycles. If issues remain after
   the third review, stop and report the unresolved findings instead of looping.

## Rules

- Give each agent a self-contained task description — agents cannot see this
  conversation. Include target files, expected behavior, and (for fix rounds)
  the exact review findings to address.
- Never weaken or delete tests to make the review pass.
- If the task itself is ambiguous, ask the user before starting the loop.

## Report

When the loop ends, report:

- What was implemented, and the files changed
- Tests written (or why testing was skipped) and their result
- Final review status, iterations used, and any remaining P2/NIT items
