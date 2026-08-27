---
name: generate
description: Generate SQL (DDL/DML) following team formatting, naming, and policy rules, vendor-aware. Use when the user asks for SQL — create table, schema design, or select/insert/update/delete queries ("sql", "ddl", "dml", "테이블", "쿼리"). Not for executing SQL, SQL theory questions, or ORM entity code.
argument-hint: "[query-type] [table/context]"
---

# SQL Generate

Generate SQL with the team's formatting and policy rules, applied inline so it
can use the schema context already in the conversation.

## Steps

1. **Confirm the database vendor** — required before generating.
   Skip only when the vendor is already clear from the conversation or project.
   Otherwise ask via AskUserQuestion with options: Oracle, MySQL, PostgreSQL, MariaDB.
2. **Generate** — apply the formatting and naming rules below, plus the matching reference:
   - DDL (create/alter table, schema design): read `references/ddl.md`
   - DML (select/insert/update/delete): read `references/dml.md`
3. **Present** the SQL with a short note on design decisions and any vendor-specific syntax used.

## Formatting rules

- Lowercase keywords and identifiers.
- **Leading commas** — commas at the beginning of the line.
- **Right-aligned main clauses** (`select`, `from`, `where`, `group by`, `order by`, `limit`);
  `having` at column 0; `join` indented under `from`; `on` indented under `join`.
- One condition per line in `where`; `and`/`or` aligned under `where`.

```sql
select u.id
     , u.name
     , o.order_date
  from users u
       inner join orders o
                  on u.id = o.user_id
 where u.status = 'active'
   and o.order_date >= '2024-01-01'
 group by u.id
        , u.name
        , o.order_date
having count(*) > 1
 order by o.order_date desc
 limit 10
```

## Naming rules

- Tables: **snake_case, plural** nouns (`users`, `order_items`) — no `tbl_` prefixes.
- Columns: snake_case; no abbreviations unless universally understood (`total_amount`, not `tot_amt`).
- **Datetime columns end with `_at`** (`created_at`, `scheduled_at`);
  **date-only columns end with `_date`** (`order_date`, `event_date`).
- Booleans: `bit` type; `is_`/`has_`/`can_` prefix is optional — use it only when it
  improves clarity (`is_active`, `has_permission`), omit when the name alone is clear
  (`canceled`, `deleted`).

Constraint and index names use `{prefix}{table}_{nn}` numbering:

| Kind | Prefix | Example |
| --- | --- | --- |
| Primary key | `pk_{table}` (no numbering) | `pk_orders` |
| Foreign key | `fk_` | `fk_orders_01` — not used by default, see FK policy in `references/ddl.md` |
| Index | `idx_` | `idx_orders_01` |
| Unique index | `udx_` | `udx_orders_01` |
| Full-text index | `fdx_` | `fdx_boards_01` |
| Check | `chk_` | `chk_orders_01` |

## Checklist

- [ ] Vendor confirmed (or evident from context)
- [ ] Lowercase, leading commas, right-aligned clauses
- [ ] Explicit `join`, no `select *`
- [ ] DDL: `bigint id` PK + four audit columns
- [ ] DDL: every table and column has a clear, concise comment
- [ ] `varchar` for status values (no `enum`), `bit` for booleans
- [ ] `_at` for datetime columns, `_date` for date columns
- [ ] No FK constraints — references noted in column comments as `[→ table.id]`
- [ ] No indexes by default — suggested as comments
- [ ] No check constraints unless truly necessary
- [ ] No `on update current_timestamp` — set `modified_at`/`modified_by` explicitly
- [ ] Vendor-specific syntax applied
