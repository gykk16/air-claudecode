# Performance Best Practices

## EXISTS vs IN

Use `exists` instead of `in` for subqueries:

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

-- Avoid: IN with subquery
select u.name
  from users u
 where u.id in (
    select o.user_id
      from orders o
     where o.status = 'completed'
)
```

## Avoid Functions on Indexed Columns

Never apply functions to indexed columns in WHERE clauses:

```sql
-- Bad: Function on indexed column
select id
     , name
  from users
 where year(created_at) = 2024

-- Good: Range condition
select id
     , name
  from users
 where created_at >= '2024-01-01'
   and created_at < '2025-01-01'
```

## Index Suggestions

When writing DDL, suggest indexes as comments -- do not create by default:

```sql
create table orders (
    id           bigint
  , user_id      bigint not null
  , order_date   date
  , status       varchar(20)
  , constraint pk_orders primary key (id)
);

-- Suggested indexes:
-- create index idx_orders_01 on orders(user_id);
-- create index idx_orders_02 on orders(order_date);
-- create index idx_orders_03 on orders(status);
```

## Anti-Pattern: SELECT *

```sql
-- Bad
select *
  from users
 where status = 'active'

-- Good
select id
     , name
     , email
  from users
 where status = 'active'
```

## General Tips

- Use `limit` for large result sets
- Prefer CTE over deeply nested subqueries
- Use table aliases to keep queries concise
- Avoid implicit type conversions in WHERE clauses
