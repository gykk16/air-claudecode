# gogcli Calendar Commands Reference

Summary of `gog calendar` subcommands. All commands support `--account`, `--json`, `--plain` global flags.

---

## List Events

```bash
gog calendar events [<calendarId>] [flags]
```

| Flag | Description |
|---|---|
| `--from` | Start time (RFC3339, date, or relative: today, tomorrow, monday) |
| `--to` | End time |
| `--today` | Today only (timezone-aware) |
| `--tomorrow` | Tomorrow only (timezone-aware) |
| `--week` | This week (use with `--week-start`) |
| `--week-start` | Week start day (sun, mon, ...). Default: mon |
| `--days=N` | Next N days |
| `--max=10` | Max results |
| `--all` | Fetch from all calendars |
| `--query` | Free text search |
| `--weekday` | Include day-of-week columns |

### Examples

```bash
# Today's events
gog calendar events --account work --today --json

# This week (Sunday start)
gog calendar events --account work --week --week-start=sun --json

# Date range
gog calendar events --account personal --from 2026-02-18 --to 2026-02-22 --json

# All calendars
gog calendar events --account work --today --all --json
```

---

## Search Events

```bash
gog calendar search <query> [flags]
```

| Flag | Description |
|---|---|
| `--from` | Start time |
| `--to` | End time |
| `--today` | Today only |
| `--tomorrow` | Tomorrow only |
| `--week` | This week |
| `--calendar` | Calendar ID (default: primary) |
| `--max=25` | Max results |

### Examples

```bash
gog calendar search "sprint" --account work --week --json
```

---

## Create Event

```bash
gog calendar create <calendarId> [flags]
```

| Flag | Description |
|---|---|
| `--summary` | Event title (required) |
| `--from` | Start time RFC3339 (required) |
| `--to` | End time RFC3339 (required) |
| `--description` | Description |
| `--location` | Location |
| `--attendees` | Attendee emails (comma-separated) |
| `--all-day` | All-day event (use date-only in `--from`/`--to`) |
| `--visibility` | default, public, private, confidential |
| `--transparency` | busy (opaque), free (transparent) |
| `--with-meet` | Create Google Meet link |
| `--send-updates` | Notifications: all, externalOnly, none (default: all) |
| `--reminder` | Reminder (e.g., popup:30m, email:1d). Max 5 |
| `--rrule` | Recurrence rule (e.g., RRULE:FREQ=WEEKLY;BYDAY=MO) |

### Examples

```bash
# Basic event
gog calendar create primary \
  --account work \
  --summary "Team Meeting" \
  --from "2026-02-20T14:00:00+09:00" \
  --to "2026-02-20T15:00:00+09:00" \
  --location "Room A" \
  --attendees "kim@company.com,park@company.com" \
  --json

# All-day event
gog calendar create primary \
  --account personal \
  --summary "Vacation" \
  --from "2026-02-20" \
  --to "2026-02-21" \
  --all-day \
  --json

# With Google Meet
gog calendar create primary \
  --account work \
  --summary "Remote Meeting" \
  --from "2026-02-20T10:00:00+09:00" \
  --to "2026-02-20T11:00:00+09:00" \
  --with-meet \
  --json
```

---

## Update Event

```bash
gog calendar update <calendarId> <eventId> [flags]
```

| Flag | Description |
|---|---|
| `--summary` | New title (empty string to clear) |
| `--from` | New start time |
| `--to` | New end time |
| `--description` | New description |
| `--location` | New location |
| `--attendees` | Replace all attendees |
| `--add-attendee` | Add attendees (preserve existing) |
| `--scope` | Recurring events: single, future, all (default: all) |

### Examples

```bash
# Change time
gog calendar update primary <eventId> \
  --account work \
  --from "2026-02-20T15:00:00+09:00" \
  --to "2026-02-20T16:00:00+09:00" \
  --json

# Add attendee
gog calendar update primary <eventId> \
  --account work \
  --add-attendee "lee@company.com" \
  --json
```

---

## Delete Event

```bash
gog calendar delete <calendarId> <eventId> [flags]
```

| Flag | Description |
|---|---|
| `--scope` | Recurring events: single, future, all (default: all) |

### Examples

```bash
gog calendar delete primary <eventId> --account personal
```

---

## Respond to Invitation

```bash
gog calendar respond <calendarId> <eventId> [flags]
```

| Flag | Description |
|---|---|
| `--status` | accepted, declined, tentative, needsAction |
| `--comment` | Response comment |

### Examples

```bash
gog calendar respond primary <eventId> --account work --status accepted
```

---

## Check Conflicts

```bash
gog calendar conflicts [flags]
```

| Flag | Description |
|---|---|
| `--from` | Start time |
| `--to` | End time |
| `--today` | Today only |
| `--week` | This week |
| `--calendars` | Calendar IDs (comma-separated, default: primary) |

### Examples

```bash
gog calendar conflicts --account work --today --json
```

---

## List Calendars

```bash
gog calendar calendars [flags]
```

### Examples

```bash
gog calendar calendars --account work --json
```

---

## Account Management

```bash
# List registered accounts
gog auth list --json

# Set aliases
gog auth alias set personal me@gmail.com
gog auth alias set work work@company.com

# List aliases
gog auth alias list

# Authenticate / re-authenticate
gog auth add <email>
gog auth add <email> --services calendar --force-consent
```
