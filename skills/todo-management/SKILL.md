---
name: todo-management
description: Manage weekly markdown TODO files -- create, migrate, review tasks with priority levels, backlog, and topic-based views
model: haiku
argument-hint: "[today] [this week] [migrate] [backlog] [new week] [add task] [topics] [topic <name>]"
---

# TODO Management

Manage weekly markdown TODO files with daily sections, priority levels, task migration, and backlog tracking.

## Use When
- User says "todo", "task", "할 일", "투두", "이번주 할 일", "오늘 할 일"
- User wants to add, check, migrate, or review tasks
- User asks about backlog or weekly planning
- User wants to view or manage tasks by topic/project
- Sunday weekly review or new week setup

## Do Not Use When
- Jira ticket management -- use jira-master instead
- GitHub issue tracking -- use git-issue-master instead
- Calendar/schedule management -- use gog-calendar instead

---

## First-Time Setup

On first invocation, check if the todo workspace location is configured:

1. **Read user's CLAUDE.md** (`~/.claude/CLAUDE.md`) and look for a `todo-workspace` entry
2. **If not found**:
   a. Ask user via `AskUserQuestion` where to store TODO files (suggest default: `~/todo-workspace/`)
   b. **MUST save immediately**: Use the `Edit` tool to append the following block to `~/.claude/CLAUDE.md`:
      ```
      ## Todo Workspace
      todo-workspace: /absolute/path/to/todo
      ```
   c. **Do NOT proceed** to directory initialization until the Edit tool confirms the write succeeded
3. **If found**: use the configured path

Then initialize the directory structure if it doesn't exist:
```
<workspace>/
  ├── templates/
  │   └── weekly.md
  ├── backlog.md
  └── topics.md
```

- Copy `<skill_base_dir>/templates/weekly.md` as the weekly template
- Copy `<skill_base_dir>/templates/backlog.md` as `backlog.md`
- Copy `<skill_base_dir>/templates/topics.md` as `topics.md`

---

## File Structure

- **Weekly file**: `YYYY-WXX.md` (ISO week number, week starts Sunday)
- **Backlog**: `backlog.md` for unscheduled/deferred tasks
- **Topics**: `topics.md` for topic/project registry
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
- [ ] Task description @assignee #tag %topic ~estimate due-date [REF-ID]
```

Metadata fields (all optional, same line):
| Field | Format | Example |
|---|---|---|
| Assignee | `@name` | `@young` |
| Tag | `#tag` | `#bug`, `#feat`, `#refactor`, `#docs` |
| Topic | `%topic` | `%air-backend`, `%search-engine` |
| Estimate | `~Nh` or `~Nd` | `~2h`, `~1d` |
| Due date | `YYYY-MM-DD` | `2026-03-05` |
| External ref | `[ID]` | `[JIRA-101]` |
| Migration source | `<- Day` | `<- Mon` |
| Subtasks | indented 2 spaces | `  - [ ] Subtask` |

- `#tag` = task type (bug, feat, docs), `%topic` = project/area the task belongs to
- One task can have one `%topic` (keeps grouping simple)
- Topic names use kebab-case

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

### List Topics
1. Read `topics.md`
2. Show active topics with task counts (scan current week file + backlog for `%topic` matches)
3. Display format:
```
## Active Topics
- air-backend (3 open | 5 done)
- search-engine (1 open | 2 done)
- infra (0 open | 1 done)

## Archived
- auth-migration (completed 2026-02)
```

### Show Topic
1. Accept topic name (e.g., "show topic air-backend")
2. Scan current week file + backlog for tasks with matching `%topic`
3. Group by source: "This Week" (with day/priority info) and "Backlog"
4. Show estimate rollup and blocked count
5. Display format:
```
## Topic: air-backend (3 open | 2 done)

### This Week (W09)
- [ ] Implement auth API @young #feat ~4h 2026-02-28 [JIRA-101]  (Thu P0)
- [x] Fix DB connection pool #bug ~1h                              (Wed P1)
- [ ] Write onboarding guide #docs ~1d                             (Fri P1)

### Backlog
- [ ] Add rate limiting #feat ~3h
- [ ] Refactor error handling #refactor ~4h

---
Estimate remaining: ~9h | Blocked: 0
```

### Add Topic
1. Accept topic name and optional description
2. Validate kebab-case naming
3. Append to `## Active` section in `topics.md`
4. Confirm addition

### Archive Topic
1. Accept topic name
2. Scan current week file + backlog for open tasks with `%topic`
3. If open tasks exist: warn user and list them, ask to confirm
4. Move topic from `## Active` to `## Archived` with completion date
5. Confirm archival

### Topic Summary (part of Weekly Review)
1. During Saturday weekly review, also show per-topic breakdown:
```
### Topic Summary
| Topic | Created | Done | Dropped | Migrated | Rate |
|---|---|---|---|---|---|
| air-backend | 5 | 3 | 0 | 2 | 60% |
| search-engine | 2 | 2 | 0 | 0 | 100% |
```

---

## Topics File Format

```markdown
# Topics

> Active projects and areas of work. Tasks use %topic-name to link here.

## Active
- **topic-name**: Description of the topic/project

## Archived
- **topic-name**: (completed YYYY-MM) Description
```

- Topics use kebab-case names matching the `%topic` field in tasks
- `Active` topics appear in default views and summaries
- `Archived` topics are hidden from default views but tasks remain searchable

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
| Topic not in registry | Offer to add it to `topics.md` |
| No tasks for topic | "No tasks found for %topic-name." |
| Topics file not found | Create from template |

---

## Key Principles

- **One file per week**, daily sections within
- **Unfinished tasks must be explicitly migrated** -- no silent carry-over
- **3-day migration rule** forces priority re-evaluation
- **Keep P0 short** (1~3 items) to maintain focus
- **Sunday start**: weeks run Sun through Sat
- **Topics are views, not containers** -- tasks live in weekly/backlog files, `%topic` is a cross-cutting filter
- **Topics are optional** -- tasks without `%topic` work exactly as before
