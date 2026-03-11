# Formatting Rules

## Keyword Alignment

Right-align main clauses to create readable structure:

- Main clauses (`select`, `from`, `where`, `group by`, `order by`, `limit`) right-aligned
- `having` left-aligned at column 0
- `join` indented under `from`
- `on` indented under `join`

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

## Comma Placement

Place commas at the **beginning** of lines (leading commas):

```sql
-- Good: Leading commas
select id
     , name
     , email
     , created_at
  from users

-- Bad: Trailing commas
select id,
       name,
       email,
       created_at
  from users
```

Benefits:
- Easy to comment out columns
- Clear visual alignment
- Simpler version control diffs

## Indentation

- Use consistent indentation
- Align related elements vertically
- `join` indented 7 spaces from `from`
- `on` indented to align after `join` clause

```sql
select p.product_id
     , p.product_name
     , c.category_name
     , sum(oi.quantity) as total_sold
  from products p
       join categories c
            on p.category_id = c.category_id
       join order_items oi
            on p.product_id = oi.product_id
 where p.is_active = true
   and c.category_name in ('Electronics', 'Clothing')
 group by p.product_id
        , p.product_name
        , c.category_name
```

## WHERE Clause

- Place each condition on a new line
- Align `and` / `or` operators under `where`

```sql
select id
     , name
  from users
 where status = 'active'
   and created_at >= '2024-01-01'
   and (role = 'admin'
        or role = 'manager')
```
