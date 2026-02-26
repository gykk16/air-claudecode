---
name: todo-management
description: Manage weekly markdown TODO files -- create, migrate, review tasks with priority levels and backlog
model: haiku
argument-hint: "[today] [this week] [migrate] [backlog] [new week] [add task]"
---

# TODO Management

Manage weekly markdown TODO files with daily sections, priority levels, task migration, and backlog tracking.

## Use When
- User says "todo", "task", "할 일", "투두", "이번주 할 일", "오늘 할 일"
- User wants to add, check, migrate, or review tasks
- User asks about backlog or weekly planning
- Sunday weekly review or new week setup

## Do Not Use When
- Jira ticket management -- use jira-master instead
- GitHub issue tracking -- use git-issue-master instead
- Calendar/schedule management -- use gog-calendar instead

---

## First-Time Setup

On first invocation, check if the todo workspace location is configured:

1. **Read user's CLAUDE.md** (`~/.claude/CLAUDE.md`) and look for a `todo-workspace` entry
2. **If not found**: ask user via `AskUserQuestion` where to store TODO files
   - Suggest default: `~/todo-workspace/`
   - Save the chosen path to `~/.claude/CLAUDE.md` as:
     ```
     ## Todo Workspace
     todo-workspace: /absolute/path/to/todo
     ```
3. **If found**: use the configured path

Then initialize the directory structure if it doesn't exist:
```
<workspace>/
  ├── templates/
  │   └── weekly.md
  └── backlog.md
```

- Copy `<skill_base_dir>/templates/weekly.md` as the weekly template
- Copy `<skill_base_dir>/templates/backlog.md` as `backlog.md`

---

## File Structure

- **Weekly file**: `YYYY-WXX.md` (ISO week number, week starts Sunday)
- **Backlog**: `backlog.md` for unscheduled/deferred tasks
- **Template**: `templates/weekly.md` for new week creation

### Week Number Calculation

Use ISO week numbering but with **Sunday as week start**:
```bash
date +%G-W%V  # reference, but adjust for Sunday start
```

---

## Task Syntax

Each task is a single line with optional metadata fields:

```
- [ ] Task description @assignee #tag ~estimate due-date [REF-ID]
```

Metadata fields (all optional, same line):
| Field | Format | Example |
|---|---|---|
| Assignee | `@name` | `@young` |
| Tag | `#tag` | `#bug`, `#feat`, `#refactor`, `#docs` |
| Estimate | `~Nh` or `~Nd` | `~2h`, `~1d` |
| Due date | `YYYY-MM-DD` | `2026-03-05` |
| External ref | `[ID]` | `[JIRA-101]` |
| Migration source | `<- Day` | `<- Mon` |
| Subtasks | indented 2 spaces | `  - [ ] Subtask` |

---

## Status Symbols

| Symbol | Meaning |
|---|---|
| `- [ ]` | Open -- not started |
| `- [x]` | Done -- completed |
| `- [-]` | Dropped -- won't do / cancelled |
| `- [>]` | Migrated -- moved to next day |
| `- [!]` | Blocked -- waiting on something |

---

## Priority Levels

Each daily section has three priority subsections:

| Level | Meaning | Max Tasks |
|---|---|---|
| **P0** | Must do today | 1~3 |
| **P1** | Should do today (important but flexible) | no limit |
| **P2** | Nice to have (do if time allows) | no limit |

---

## Weekly File Format

```markdown
# YYYY-WXX (Mon DD ~ Mon DD)

## Sun MM-DD

### P0
- [ ] Critical task

### P1
- [ ] Important task

### P2
- [ ] Nice to have

---

## Mon MM-DD

### P0
...
```

- Days run **Sun through Sat**
- Days separated by horizontal rule (`---`)
- Each day has `### P0`, `### P1`, `### P2` subsections

---

## Operations

### Show Today
1. Determine current date and find the matching weekly file
2. Read the day's section
3. Display tasks grouped by priority with status counts

### Add Task
1. Parse task description and metadata from user input
2. Determine target day (default: today) and priority (default: P1)
3. Append to the correct section in the weekly file
4. Confirm addition

### Complete Task
1. Find the task by description or line number
2. Change `[ ]` to `[x]`
3. Confirm completion

### Migrate Tasks (End of Day)
1. Find all `[ ]` (open) tasks in today's section
2. For each open task:
   - Change to `[>]` in today's section
   - Copy to next day as `[ ]` with `<- Day` marker
3. **3+ day migration rule**: if a task has been migrated 3+ times, prompt user:
   - Move to backlog
   - Drop with `[-]`
   - Keep migrating (must justify)

### Cross-Week Migration
- If migrating past Saturday: move to next week file's Sunday section or backlog
- Create next week file from template if it doesn't exist

### New Week Setup (Sunday)
1. Create new weekly file from template: `YYYY-WXX.md`
2. Calculate date range (Sun ~ Sat) and fill in headings
3. Pull tasks from backlog that have due dates in this week
4. Show pulled tasks for review

### Weekly Review (Saturday)
1. Read all `[>]` tasks from the week
2. For each, ask user to decide:
   - Move to next week's Sunday
   - Move to backlog
   - Drop with `[-]`
3. Show weekly summary:
   - Total tasks: created, completed, dropped, migrated
   - Completion rate

### Backlog Management
- Show backlog grouped by P1, P2, Ideas
- Add task to backlog with priority
- Move backlog task to a specific day
- Review backlog (suggested every Sunday)

---

## Backlog File Format

```markdown
# Backlog

## P1
- [ ] Important unscheduled task @young #feat ~4h [JIRA-201]

## P2
- [ ] Lower priority task #refactor

## Ideas
- [ ] Someday/maybe idea
```

---

## Display Format

When showing tasks, use this format:

```
## Today: Wed 02-26 (2026-W09)

### P0 (1/1 done)
- [x] Deploy hotfix #ops ~1h [JIRA-301]

### P1 (0/2 done)
- [ ] Review PR for auth module @young #review ~2h
- [!] Update API docs #docs -- blocked: waiting on spec

### P2 (0/1 done)
- [ ] Clean up test fixtures #refactor ~1h

---
Summary: 1/4 done | 1 blocked | 0 migrated
```

---

## Error Handling

| Scenario | Action |
|---|---|
| Weekly file not found | Offer to create from template |
| Workspace not configured | Run first-time setup |
| No tasks for today | Show "No tasks for today. Add one?" |
| Backlog empty | "Backlog is empty." |

---

## Key Principles

- **One file per week**, daily sections within
- **Unfinished tasks must be explicitly migrated** -- no silent carry-over
- **3-day migration rule** forces priority re-evaluation
- **Keep P0 short** (1~3 items) to maintain focus
- **Sunday start**: weeks run Sun through Sat
