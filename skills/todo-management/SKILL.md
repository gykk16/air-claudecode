---
name: todo-management
description: Manage weekly markdown TODO files -- create, migrate, review tasks with priority levels, subtasks, backlog, and topic-based views
model: haiku
argument-hint: "[today] [this week] [migrate] [backlog] [new week] [add task] [add subtask] [topics] [topic <name>]"
---

# TODO Management

Manage weekly markdown TODO files with daily sections, priority levels, subtasks, task migration, backlog, and topic-based views.

## Use When
- User says "todo", "task", "할 일", "투두", "이번주 할 일", "오늘 할 일"
- User wants to add, check, migrate, or review tasks
- User wants to add or manage subtasks ("add subtask", "서브태스크")
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

| File | Purpose |
|---|---|
| `YYYY-WXX.md` | Weekly file (ISO week, Sunday start) |
| `backlog.md` | Unscheduled/deferred tasks (P1, P2, Ideas) |
| `topics.md` | Topic/project registry (Active, Archived) |
| `templates/weekly.md` | Template for new week creation |

### Week Number Calculation

Use ISO week numbering with **Sunday as week start**:
```bash
date +%G-W%V  # reference, but adjust for Sunday start
```

---

## Task Syntax

Each task is a single line with optional metadata fields:

```
- [ ] Task description @assignee #tag %topic ~estimate due-date [REF-ID]
```

| Field | Format | Example |
|---|---|---|
| Assignee | `@name` | `@alice` |
| Tag | `#tag` | `#bug`, `#feat`, `#refactor`, `#docs` |
| Topic | `%topic` | `%air-backend`, `%search-engine` |
| Estimate | `~Nh` or `~Nd` | `~2h`, `~1d` |
| Due date | `YYYY-MM-DD` | `2026-03-05` |
| External ref | `[ID]` | `[JIRA-101]` |
| Link | `[text](url)` | `[slack](https://...)` |
| Migration source | `<- Day` | `<- Mon` |

All metadata fields are optional and placed on the same line.

- `#tag` = task type (bug, feat, docs), `%topic` = project/area the task belongs to
- One task can have one `%topic` (keeps grouping simple)
- Topic names use kebab-case

---

## Subtasks

Subtasks are indented **2 spaces** under a parent task:

```markdown
- [ ] git repo 세팅 %항공-내재화 #feat ~2d
  - [ ] 기본 아키텍처 설계 ~2h
  - [ ] 패키지 구조 세팅 ~2h
  - [x] 라이브러리 선정 및 추가 ~1h
  - [ ] 배포 스크립트 세팅 ~3h
```

### Rules

| Rule | Detail |
|---|---|
| Max depth | **2 levels only** (parent → child). No nested subtasks |
| Metadata | Subtasks support all fields except `%topic` (inherited from parent) |
| Progress | Auto-display `(done/total)` counter next to parent when subtasks exist |
| Completion | Parent `[x]` only when **all** children are `[x]` or `[-]` |
| Blocked | If any child is `[!]`, parent is considered blocked |
| Migration | Parent migrates with **all** children together as a unit |
| Estimates | Parent `~estimate` = total budget. Child estimates = breakdown |
| Adding | New subtask appended at end of children list |
| Dropping | Dropping parent (`[-]`) drops all children. Dropping a child does not affect parent |

### Progress Display

The `(done/total)` counter is shown in **display output only** -- it is NOT written into the markdown file. Progress is calculated on read.

```markdown
- [ ] git repo 세팅 (1/4) %항공-내재화 #feat ~2d
  - [x] 기본 아키텍처 설계 ~2h
  - [ ] 패키지 구조 세팅 ~2h
  - [ ] 라이브러리 선정 및 추가 ~1h
  - [ ] 배포 스크립트 세팅 ~3h
```

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

See `templates/weekly.md` for the full template. Structure:

```markdown
# YYYY-WXX (Sun DD ~ Sat DD)

## Sun MM-DD

### P0

### P1

### P2

---

## Mon MM-DD
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
4. For tasks with subtasks, show `(done/total)` progress counter

### Add Task
1. Parse task description and metadata from user input
2. Determine target day (default: today) and priority (default: P1)
3. Append to the correct section in the weekly file
4. **If user specifies subtasks** (e.g., "add task X with subtasks A, B, C"):
   - Create parent task line
   - Add each subtask indented 2 spaces below parent
5. Confirm addition

### Add Subtask
1. Find the parent task by description or line number
2. Validate parent is not itself a subtask (max 2 levels)
3. Append new subtask indented 2 spaces at end of existing children
4. Confirm addition

### Complete Task
1. Find the task by description or line number
2. **If task has subtasks**: check all children are `[x]` or `[-]` before allowing parent completion
   - If incomplete children exist: warn user and list them
   - User can force-complete (marks all open children `[-]`) or complete children first
3. **If task is a subtask**: change `[ ]` to `[x]`, then check if all siblings are done to prompt parent completion
4. Change `[ ]` to `[x]`
5. Confirm completion

### Migrate Tasks (End of Day)
1. Find all `[ ]` (open) parent-level tasks in today's section
2. For each open task:
   - Change to `[>]` in today's section
   - Copy to next day as `[ ]` with `<- Day` marker
   - **If task has subtasks**: migrate parent and all children together
     - Children keep their current status (`[x]` stays `[x]`, `[ ]` stays `[ ]`)
     - Only the parent gets `[>]` / `<- Day` markers, not individual children
3. **3+ day migration rule**: if a task has been migrated 3+ times, prompt user:
   - Move to backlog (with all subtasks)
   - Drop with `[-]` (drops parent and all children)
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
   - Move to next week's Sunday (with subtasks)
   - Move to backlog (with subtasks)
   - Drop with `[-]` (drops parent and all children)
3. Show weekly summary:
   - Total tasks: created, completed, dropped, migrated (parent-level only)
   - Completion rate
   - Per-topic breakdown (see Topic Summary below)

---

## Backlog Operations

- Show backlog grouped by P1, P2, Ideas
- Add task to backlog with priority (supports subtasks)
- Move backlog task to a specific day
- Review backlog (suggested every Sunday)

---

## Topic Operations

Topics are **cross-cutting views**, not containers. Tasks live in weekly/backlog files; `%topic` is a filter.

### List Topics
1. Read `topics.md`
2. Show active topics with task counts (scan current week file + backlog for `%topic` matches)
3. Display format:
```
## Active Topics
- air-backend (3 open | 5 done)
- search-engine (1 open | 2 done)

## Archived
- auth-migration (completed 2026-02)
```

### Show Topic
1. Accept topic name (e.g., "show topic air-backend")
2. Scan current week file + backlog for tasks with matching `%topic`
3. Group by source: "This Week" (with day/priority info) and "Backlog"
4. Show subtasks under their parent tasks
5. Show estimate rollup and blocked count
6. Display format:
```
## Topic: air-backend (3 open | 2 done)

### This Week (W09)

⬜ 1. Implement auth API (1/3)                              (Thu P0)
   └ @alice | #feat | ~4h | 2026-02-28 | [JIRA-101]
   └ [x] Define API spec ~1h
   └ [ ] Implement endpoints ~2h
   └ [ ] Write tests ~1h

✅ 2. Fix DB connection pool                                (Wed P1)
   └ #bug | ~1h

### Backlog

⬜ 3. Add rate limiting
   └ #feat | ~3h

⬜ 4. Refactor error handling
   └ #refactor | ~4h

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
During Saturday weekly review, show per-topic breakdown:
```
### Topic Summary
| Topic | Created | Done | Dropped | Migrated | Rate |
|---|---|---|---|---|---|
| air-backend | 5 | 3 | 0 | 2 | 60% |
| search-engine | 2 | 2 | 0 | 0 | 100% |
```

---

## Display Format

When showing tasks, use this **clean list** format. Each task is numbered, with status icon prefix. Metadata is on a separate `└` line below the task name. Subtasks use `└ [ ]` format. Counts are **parent-level tasks only**.

**Status icons:**
| Icon | Meaning |
|---|---|
| ✅ | Done |
| ⬜ | Open (no subtasks) |
| ⬜ N/M | Open with subtask progress |
| 🟡 | Blocked |
| ➡️ | Migrated |
| ⛔ | Dropped |

**Example:**

```
## Today: Wed 02-26 (W09)

### P0 (1/1)

✅ 1. Deploy hotfix
   └ #ops | ~1h | [JIRA-301]

### P1 (0/3)

⬜ 2. Review PR for auth module
   └ @alice | #review | ~2h

🟡 3. Update API docs
   └ #docs
   └ blocked: waiting on spec

⬜ 4. git repo 세팅 (1/4)
   └ @bob | %항공-내재화 | #feat | ~2d
   └ [x] 기본 아키텍처 설계 ~2h
   └ [ ] 패키지 구조 세팅 ~2h
   └ [ ] 라이브러리 선정 및 추가 ~1h
   └ [ ] 배포 스크립트 세팅 ~3h

### P2 (0/1)

⬜ 5. Clean up test fixtures
   └ #refactor | ~1h

---
1/5 done | 1 blocked | 0 migrated
```

**Rules:**
- Task name is the first line, **without** metadata -- keep it clean and scannable
- Metadata (`@assignee`, `#tag`, `%topic`, `~estimate`, `[REF]`) goes on the next `└` line, pipe-separated
- Blocked reason gets its own `└ blocked:` line
- External refs (`[JIRA-101]`, `[slack](url)`) go in the metadata line
- Subtasks use `└ [ ]` / `└ [x]` format
- Done tasks show ✅ with task name only (metadata can be omitted)
- Empty priority sections show just the header (e.g., `### P0 -- empty`)
- Numbers are sequential across all priorities (not per-section)

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
| Complete parent with open subtasks | Warn and list incomplete children |
| Add subtask to a subtask | Reject: "Max 2 levels. Subtasks cannot have children." |
| Subtask without parent | Treat as regular task (remove indent) |

---

## Key Principles

- **One file per week**, daily sections within
- **Unfinished tasks must be explicitly migrated** -- no silent carry-over
- **3-day migration rule** forces priority re-evaluation
- **Keep P0 short** (1~3 items) to maintain focus
- **Sunday start**: weeks run Sun through Sat
- **Topics are views, not containers** -- `%topic` is a cross-cutting filter
- **Topics are optional** -- tasks without `%topic` work exactly as before
- **Subtasks max 2 levels** -- parent → child only, no deeper nesting
- **Subtasks are atomic with parent** -- migrate, drop, and move as a unit
- **Counts use parent-level tasks** -- subtasks are progress within a task, not separate tasks
