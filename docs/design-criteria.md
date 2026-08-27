# Plugin Design Criteria

The standards behind every plugin in this marketplace. Follow them so new
plugins stay consistent with the existing ones; bend them only with a reason.

## Naming

- **Plugin names are roles**: `software-engineer`, `technical-writer`, `sql-engineer` —
  not tools (`sql-generator`) or features.
- **Skill names are actions**: `develop`, `write-tests`, `review`, `generate`, `polish`.
- Never repeat the plugin name in a skill name — the invocation is
  `/<plugin>:<skill>`, so `software-engineer:software-engineer` is a smell.
- Agents may share the plugin's role name (`software-engineer` plugin →
  `software-engineer` agent).

## Choosing the component shape

Decide by how the work is done, not by topic:

| The task... | Shape | Example |
| --- | --- | --- |
| Needs the conversation context, is interactive or quick | **Inline skill** (no fork) | `sql-engineer:generate`, `technical-writer:polish` |
| Is self-contained, touches many files, benefits from a clean context | **Fork skill → agent** (`context: fork`, `agent:`, `background: false`) | `develop`, `write-tests`, `review` |
| Chains multiple agents with loops or gates | **Inline orchestration skill** — a forked agent cannot spawn other agents | `super-engineer` |

Guideline-only content (no action) does not need its own skill if an agent is
the only consumer — put it in the agent prompt and `references/`.

## Single source of truth

- **The agent owns how the work is done**: persona, workflow, rules.
- **The skill is a delegation interface**: what to do (`$ARGUMENTS`), what to
  report back. Never restate the agent's workflow or rules in the skill —
  duplicated text drifts.
- A rule lives in exactly one file. Cross-reference instead of copying.

## Agents

Standard document structure, in this order:

1. Frontmatter: `name`, `description`, `tools`, `model`
2. Persona (2–3 lines)
3. `## Workflow` — numbered steps with **bold labels** (`1. **Understand** — ...`);
   state explicitly that steps run in order when order matters
4. `## Critical rules` — the hard constraints, right after Workflow
5. Domain rule sections
6. `## References — read what matches the task` — table mapping task → file,
   using `${CLAUDE_PLUGIN_ROOT}` paths

Grant the least tools needed: a reviewer gets no `Edit`/`Write`; a writer
gets no `Bash` unless it must run something.

## Skills

Fork skills follow: overview → `## Usage` → `## Task` → `## Report`.

- Usage must warn that **the agent cannot see the conversation** and say what
  context to include in the task description.
- Task passes `$ARGUMENTS` and tells the agent to ask (AskUserQuestion) rather
  than guess when the task is ambiguous.
- Report defines what comes back: what changed, files touched, how verified.

Write `description` frontmatter as trigger conditions, not a summary: name the
file types, keywords (Korean ones too), and actions that should activate it,
plus "Not for ..." exclusions when adjacent tasks could misfire.

## SKILL.md / agent body vs references

Split by **when it is read**, not by topic:

- Needed on every invocation → agent prompt or SKILL.md body (keep it lean).
- Needed only for some tasks → `references/<topic>.md`, routed by a table.
- Rule-style references stay prose/bullets/tables; keep code blocks only where
  the code IS the content (templates, syntax cheatsheets).

Consolidate skills whose content always loads together; split only when the
trigger conditions genuinely differ.

## Language

- All repository content is written in English (`.claude/rules/language.md`).
- Korean is allowed when it is the content itself: Korean writing rules,
  output-format specs that require Korean, copy-ready templates.

## Licensing

- Default `MIT`.
