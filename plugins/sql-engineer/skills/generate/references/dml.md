# DML Patterns

## SELECT

- Never `select *` — always name the columns.
- Table aliases for multi-table queries.
- Explicit `join` syntax only — no comma joins.

```sql
-- Bad: implicit join
  from users u
     , orders o
 where u.id = o.user_id

-- Good: explicit join
  from users u
       inner join orders o
                  on u.id = o.user_id
```

## CTE over nested subqueries

```sql
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

## INSERT / UPDATE / DELETE

Always maintain the audit columns.

```sql
insert into users (
    name
  , email
  , status
  , created_by
  , created_at
  , modified_by
  , modified_at
) values (
    'John Doe'
  , 'john@example.com'
  , 'active'
  , 'system'
  , current_timestamp
  , 'system'
  , current_timestamp
);

update users
   set name = 'Jane Doe'
     , modified_by = 'admin'
     , modified_at = current_timestamp
 where id = 1;

delete from orders
 where status = 'canceled'
   and created_at < current_date - interval '1' year;
```

## Performance

- `exists` over `in` with subqueries:

```sql
 where exists (
    select 1
      from orders o
     where o.user_id = u.id
       and o.status = 'completed'
)
```

- Never apply functions to indexed columns in `where` — use range conditions:

```sql
-- Bad
 where year(created_at) = 2024

-- Good
 where created_at >= '2024-01-01'
   and created_at < '2025-01-01'
```

- Use `limit` for large result sets.
- Avoid implicit type conversions in `where` clauses.
- Comment complex logic — explain the business rule, not the syntax:

```sql
-- Users who ordered in the last 30 days but have not logged in
-- during the same period (potential churn risk)
```
