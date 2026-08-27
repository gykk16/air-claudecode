# DDL Policies

Ordered as a table design flows: key → required columns → types → comments,
then constraint policies (FK, index, check), then the complete template.

## Primary key

Always `bigint` type `id` as the primary key, named `pk_{table}`.
Consistent across tables, framework-friendly, and simple to join on.

## Audit columns

Every table includes these four columns:

| Column | Type |
| --- | --- |
| `created_by` | `varchar(50) not null` |
| `created_at` | `timestamp not null default current_timestamp` |
| `modified_by` | `varchar(50) not null` |
| `modified_at` | `timestamp not null default current_timestamp` |

Do not use `on update current_timestamp` — it updates `modified_at` implicitly
while `modified_by` stays stale, and the behavior is vendor-specific.
Set `modified_at` and `modified_by` together, explicitly, in every UPDATE.

## Column types

Use real date/time types — never `varchar`, `int`, or epoch `bigint` for dates:

| Purpose | Type | Column suffix |
| --- | --- | --- |
| Date only | `date` | `_date` (`order_date`) |
| Time only | `time` | — |
| Date and time | `timestamp` / `datetime` | `_at` (`scheduled_at`) |
| With timezone | `timestamptz` (PostgreSQL) | `_at` |

**Booleans: `bit not null` with default `0` or `1`.**
Never `char(1)` Y/N, `boolean`, `tinyint(1)`, or `number(1)`.
No check constraint needed — `bit` only accepts 0 and 1.

**Never `enum`** — use `varchar` instead. Enum values require `ALTER TABLE` to
change, syntax differs across vendors, rollback is painful, and ORMs handle
them poorly. Validate at the application layer. When status values need
metadata or DB-level management, use a reference table:

```sql
create table user_statuses (
    id           bigint comment '상태 ID'
  , code         varchar(20) not null comment '상태 코드'
  , name         varchar(50) not null comment '상태명'
  , constraint pk_user_statuses primary key (id)
) comment '사용자 상태';
-- create unique index udx_user_statuses_01 on user_statuses (code);
```

## Comment policy

**Always comment every table and every column.** Comments are clear and concise —
a short noun phrase stating what the value is, not how it is used.

- Table comment: what one row represents (`comment '주문'`).
- Column comment: what the value means; include the unit or rule when it matters
  (`comment '총 주문 금액'`).
- Reference columns append the FK notation: `comment '주문자 [→ users.id]'`.

```sql
-- MySQL / MariaDB: inline
  , order_date   date not null comment '주문 일자'

-- Oracle / PostgreSQL: comment statements after creation
comment on table orders is '주문';
comment on column orders.order_date is '주문 일자';
```

## Foreign key policy

**Never create FK constraints at the DB level.**
Document the reference in the column comment instead, using the `[→ table.id]`
notation from the comment policy above:

```sql
  , user_id      bigint not null comment '주문자 [→ users.id]'
```

## Index policy

**No indexes by default.** Suggest them as comments after the DDL; create only
when the user explicitly asks. Unique business keys use unique indexes (`udx_`),
also suggested as comments unless requested.

Do not suggest redundant indexes: a composite index covers queries on its
leftmost prefix, so `(user_id, order_date)` already serves `user_id`-only
lookups — a separate index on `user_id` adds no value.

## Check constraint policy

**Avoid check constraints — do not use or suggest them unless truly necessary.**
Validate values at the application layer. A check constraint is justified only
when a DB-level invariant must hold regardless of which application writes the
data (e.g. multiple writers on a shared schema). When used, name it
`chk_{table}_{nn}`.

## Complete template

```sql
create table orders (
    id              bigint comment '주문 ID'
  , user_id         bigint not null comment '주문자 [→ users.id]'
  , order_date      date not null comment '주문 일자'
  , total_amount    decimal(10, 2) comment '총 주문 금액'
  , status          varchar(20) not null default 'pending' comment '주문 상태'
  , canceled        bit not null default 0 comment '취소 여부'
  , created_by      varchar(50) not null comment '생성자'
  , created_at      timestamp not null default current_timestamp comment '생성 일시'
  , modified_by     varchar(50) not null comment '수정자'
  , modified_at     timestamp not null default current_timestamp comment '수정 일시'
  , constraint pk_orders primary key (id)
) comment '주문';

-- Suggested indexes:
-- create unique index udx_orders_01 on orders (user_id, order_date);
-- create index idx_orders_01 on orders (order_date);
--   (no separate index on user_id -- covered by udx_orders_01's leftmost prefix)
```
