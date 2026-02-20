# SQL Style Guide

> **Key Principle**: Use ANSI SQL, lowercase keywords, leading commas, and right-aligned clauses. Optimize for clarity over brevity.

## General Principles

- Use **ANSI SQL** as default -- avoid vendor-specific syntax unless necessary
- Use **lowercase** for all SQL keywords and identifiers
- Write readable, maintainable queries
- Optimize for clarity over brevity

## Formatting Rules

### Keyword Alignment

- Main clauses (`select`, `from`, `where`, `group by`, `order by`, `limit`) right-aligned
- `having` left-aligned at column 0
- `join` indented under `from`; `on` indented under `join`
- Place commas at the **beginning** of lines (leading commas)

```sql
select u.id
     , u.name
     , u.email
     , o.order_date
     , o.total_amount
  from users u
       inner join orders o
                  on u.id = o.user_id
 where u.status = 'active'
   and o.order_date >= '2024-01-01'
 group by u.id
        , u.name
        , u.email
        , o.order_date
        , o.total_amount
having count(*) > 1
 order by o.order_date desc
 limit 10
```

Benefits of leading commas: easy to comment out columns, clear visual alignment, simpler version control diffs.

## Naming Conventions

- **Tables**: `snake_case`, plural nouns (e.g., `users`, `order_items`, `product_categories`)
- **Columns**: `snake_case`, avoid abbreviations unless widely understood (e.g., `user_id`, `created_at`, `is_active`)
- **Primary key**: `id` or `{table_name}_id`; **Foreign key**: `{referenced_table}_id`
- **Do NOT use database `ENUM` type** for code/status columns -- always use `varchar`
- **Do NOT add foreign key constraints by default** -- only when explicitly requested

### Code/Status Columns

> **IMPORTANT**: Do not use the database `ENUM` type for code or status columns in DDL. Always use `varchar` instead. Database `ENUM` types require schema migrations (ALTER TABLE) to add or remove values, whereas `varchar` columns allow application-level changes without DDL modifications.

```sql
-- Good: varchar for code/status columns
create table orders (
    id           bigint
  , status       varchar(20) not null   -- managed by application enum
  , payment_type varchar(20) not null   -- managed by application enum
  , constraint pk_orders primary key (id)
);

-- Bad: database ENUM type -- requires ALTER TABLE to add new values
create table orders (
    id           bigint
  , status       enum('PENDING', 'PAID', 'SHIPPED') not null
  , constraint pk_orders primary key (id)
);
```

### Constraint Naming Conventions

| Type        | Pattern                           | Example        |
|-------------|-----------------------------------|----------------|
| Primary Key | `pk_{table_name}`                 | `pk_orders`    |
| Unique Key  | `uk_{table_name}_01`, `_02`, ...  | `uk_users_01`  |
| Foreign Key | `fk_{table_name}_01`, `_02`, ...  | `fk_orders_01` |
| Index       | `idx_{table_name}_01`, `_02`, ... | `idx_orders_01`|
| Sequence    | `seq_{table_name}_01`, `_02`, ... | `seq_orders_01`|
| Check       | `ck_{table_name}_01`, `_02`, ...  | `ck_orders_01` |

```sql
-- Default: No FK constraint, no index
create table orders (
    id           bigint
  , user_id      bigint not null
  , total_amount decimal(10, 2)
  , created_at   timestamp default current_timestamp
  , constraint pk_orders primary key (id)
  , constraint uk_orders_01 unique (user_id, created_at)
);

-- Suggested indexes:
-- create index idx_orders_01 on orders(user_id);
-- create index idx_orders_02 on orders(created_at);

-- Only when explicitly requested: With FK constraint
create table orders (
    id           bigint
  , user_id      bigint not null
  , total_amount decimal(10, 2)
  , created_at   timestamp default current_timestamp
  , constraint pk_orders primary key (id)
  , constraint fk_orders_01
      foreign key (user_id) references users(id)
);
```

## Query Best Practices

- Avoid `select *` -- always specify column names explicitly
- Use table aliases for multi-table queries
- Always use explicit `JOIN` syntax (not implicit comma joins)
- Prefer `exists` over `in` for subqueries
- Prefer CTEs over nested subqueries for complex queries

```sql
-- CTE (preferred for complex queries)
with active_users as (
    select id
         , name
      from users
     where status = 'active'
)
, recent_orders as (
    select user_id
         , count(*) as order_count
      from orders
     where order_date >= current_date - interval '30' day
     group by user_id
)
select au.name
     , ro.order_count
  from active_users au
       join recent_orders ro
            on au.id = ro.user_id
```

### INSERT / UPDATE / DELETE

```sql
-- INSERT
insert into users (
    name
  , email
  , status
  , created_at
) values (
    'John Doe'
  , 'john@example.com'
  , 'active'
  , current_timestamp
);

-- UPDATE
update users
   set name = 'Jane Doe'
     , email = 'jane@example.com'
     , updated_at = current_timestamp
 where id = 1;

-- DELETE
delete from orders
 where status = 'cancelled'
   and created_at < current_date - interval '1' year;
```

## Performance Best Practices

### Indexing

- **Do NOT create indexes by default** -- only suggest if needed
- When writing DDL, suggest indexes as comments:

```sql
create table orders (
    id           bigint
  , user_id      bigint not null
  , order_date   date
  , constraint pk_orders primary key (id)
);

-- Suggested indexes:
-- create index idx_orders_01 on orders(user_id);
-- create index idx_orders_02 on orders(order_date);
```

### EXISTS vs IN

```sql
-- Good: EXISTS
select u.name
  from users u
 where exists (
    select 1
      from orders o
     where o.user_id = u.id
       and o.status = 'completed'
)

-- Bad: IN with subquery
select u.name
  from users u
 where u.id in (
    select o.user_id
      from orders o
     where o.status = 'completed'
)
```

### Avoid Functions on Indexed Columns

Avoid applying functions to indexed columns in `WHERE` clauses -- this prevents index use:

```sql
-- Bad: function on indexed column prevents index usage
select id, name
  from users
 where year(created_at) = 2024

-- Good: range condition allows index usage
select id, name
  from users
 where created_at >= '2024-01-01'
   and created_at < '2025-01-01'
```
