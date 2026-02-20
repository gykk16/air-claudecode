# QueryDSL

## Core Principles

| Guideline | Description |
|-----------|-------------|
| **Extend QuerydslRepositorySupport** | All QueryDSL repositories must extend the project's support class |
| **`QueryRepository` suffix** | All QueryDSL repository classes must use `QueryRepository` suffix (e.g., `OrderQueryRepository`) |
| **`fetch` prefix** | All QueryDSL select methods must be prefixed with `fetch` |
| **`@QueryProjection`** | Use `@QueryProjection` on DTO constructors for type-safe projections -- avoid `Projections.constructor` |
| **No associations** | Use QueryDSL JOINs instead of entity associations |
| **`Pageable` for pagination** | Always accept `Pageable` as a parameter for paginated queries |
| **`SearchCondition` for complex filters** | Encapsulate multiple search parameters in a dedicated `{Feature}SearchCondition` object |

## Repository Structure

### Standard QueryDSL repository

```kotlin
@Repository
class OrderQueryRepository(
) : QuerydslRepositorySupport(Order::class.java) {

    private val order = QOrder.order
    private val user = QUser.user

    fun fetchById(id: Long): OrderDto? {
        return select(
            QOrderDto(
                order.id,
                order.totalAmount,
                order.status,
            )
        )
            .from(order)
            .where(order.id.eq(id))
            .fetchOne()
    }

    fun fetchAllByUserId(userId: Long): List<OrderDto> {
        return select(
            QOrderDto(
                order.id,
                order.totalAmount,
                order.status,
            )
        )
            .from(order)
            .where(order.userId.eq(userId))
            .orderBy(order.createdAt.desc())
            .fetch()
    }
}
```

### Naming convention

| Operation | Prefix | Example |
|-----------|--------|---------|
| Single result | `fetchXxx` | `fetchById(id)`, `fetchByEmail(email)` |
| List result | `fetchAllXxx` | `fetchAllByUserId(userId)` |
| Paged result | `fetchPageXxx` | `fetchPageByStatus(status, pageable)` |
| Count | `fetchCountXxx` | `fetchCountByStatus(status)` |
| Exists check | `existsXxx` | `existsByEmail(email)` |

```kotlin
// Bad: Missing fetch prefix
fun findById(id: Long): OrderDto?
fun getOrdersByUser(userId: Long): List<OrderDto>

// Good: fetch prefix
fun fetchById(id: Long): OrderDto?
fun fetchAllByUser(userId: Long): List<OrderDto>
```

## DTO Projection with @QueryProjection

```kotlin
data class OrderDto @QueryProjection constructor(
    val id: Long,
    val totalAmount: BigDecimal,
    val status: OrderStatus,
)

data class OrderWithUserDto @QueryProjection constructor(
    val orderId: Long,
    val totalAmount: BigDecimal,
    val userName: String,
    val userEmail: String,
)
```

```kotlin
fun fetchWithUser(orderId: Long): OrderWithUserDto? {
    return select(
        QOrderWithUserDto(
            order.id,
            order.totalAmount,
            user.name,
            user.email,
        )
    )
        .from(order)
        .join(user).on(order.userId.eq(user.id))
        .where(order.id.eq(orderId))
        .fetchOne()
}
```

> **Avoid `Projections.constructor`**: not type-safe, breaks silently if the constructor changes. Always use `@QueryProjection` instead.

## Pagination

> **IMPORTANT**: Always use `Pageable` for paginated queries. Do not pass raw `page`/`size` parameters directly.

### Using applyPagination

```kotlin
fun fetchPageByCondition(
    condition: OrderSearchCondition,
    pageable: Pageable,
): Page<OrderDto> {
    return applyPagination(
        pageable,
        contentQuery = { queryFactory ->
            queryFactory
                .select(
                    QOrderDto(
                        order.id,
                        order.totalAmount,
                        order.status,
                    )
                )
                .from(order)
                .where(
                    QuerydslExpressions.eq(order.status, condition.status),
                    QuerydslExpressions.dateTimeBetween(
                        order.createdAt, condition.startDate, condition.endDate,
                    ),
                )
                .orderBy(order.createdAt.desc())
        },
        countQuery = { queryFactory ->
            queryFactory
                .select(order.count())
                .from(order)
                .where(
                    QuerydslExpressions.eq(order.status, condition.status),
                    QuerydslExpressions.dateTimeBetween(
                        order.createdAt, condition.startDate, condition.endDate,
                    ),
                )
        },
    )
}
```

## SearchCondition

> **IMPORTANT**: Encapsulate complex search parameters in a dedicated `{Feature}SearchCondition` data class. Do not pass multiple filter parameters individually.

```kotlin
// Bad: Multiple individual parameters
fun fetchAllByCondition(name: String?, status: UserStatus?, startDate: LocalDate?, endDate: LocalDate?): List<UserDto>

// Good: SearchCondition object
data class UserSearchCondition(
    val name: String? = null,
    val status: UserStatus? = null,
    val startDate: LocalDate? = null,
    val endDate: LocalDate? = null,
)

fun fetchAllByCondition(condition: UserSearchCondition): List<UserDto>
```

### Use SearchDates for date range fields

> **Tip**: Use `SearchDates` from the common module instead of raw `startDate`/`endDate` fields. `SearchDates` provides built-in safeguards against invalid or excessively wide date ranges.

```kotlin
// Bad: Raw date fields with no validation
data class OrderSearchCondition(
    val status: OrderStatus? = null,
    val startDate: LocalDate? = null,
    val endDate: LocalDate? = null,
)

// Good: Use SearchDates for date range with built-in safeguards
data class OrderSearchCondition(
    val status: OrderStatus? = null,
    val searchDates: SearchDates = SearchDates.lastMonth(),
)
```

### SearchDates factory methods

| Method | Range | Description |
|--------|-------|-------------|
| `SearchDates.of(start, end)` | Custom | Custom date range with auto-adjustment |
| `SearchDates.today()` | Today | Single day (today) |
| `SearchDates.yesterday()` | Yesterday | Single day (yesterday) |
| `SearchDates.lastDays(n)` | Last N days | From N days ago to today |
| `SearchDates.lastWeeks(n)` | Last N weeks | From N weeks ago to today |
| `SearchDates.lastMonths(n)` | Last N months | From N months ago to today |
| `SearchDates.thisWeek()` | Current week | Week start to today |
| `SearchDates.lastWeek()` | Previous week | Previous full week |
| `SearchDates.thisMonth()` | Current month | 1st of month to today |
| `SearchDates.lastMonth()` | Previous month | Previous full month |

## Dynamic Conditions

Pass `SearchCondition` fields to `QuerydslExpressions` methods for null-safe dynamic filtering.

```kotlin
fun fetchAllByCondition(condition: UserSearchCondition): List<UserDto> {
    return select(
        QUserDto(
            user.id,
            user.name,
            user.email,
        )
    )
        .from(user)
        .where(
            QuerydslExpressions.containsIgnoreCase(user.name, condition.name),
            QuerydslExpressions.eq(user.status, condition.status),
            QuerydslExpressions.dateBetween(user.createdAt, condition.startDate, condition.endDate),
        )
        .fetch()
}
```

### Available expressions

| Method | Description |
|--------|-------------|
| `eq(path, value)` | Equals (String, Boolean, Enum, Number) |
| `gt(path, value)` | Greater than (Number) |
| `gte(path, value)` | Greater than or equal (Number) |
| `lt(path, value)` | Less than (Number) |
| `lte(path, value)` | Less than or equal (Number) |
| `contains(path, value)` | String contains |
| `containsIgnoreCase(path, value)` | Case-insensitive contains |
| `containsIgnoreCaseAndSpace(path, value)` | Ignore case and whitespace |
| `startsWith(path, value)` | String starts with |
| `in(path, collection)` | In collection (String, Enum) |
| `inIgnoreCase(path, collection)` | Case-insensitive in (String) |
| `dateBetween(path, start, end)` | Date range (supports partial -- either bound may be null) |
| `dateTimeBetween(path, start, end)` | DateTime range (supports partial) |
| `isTrue(path)` | Boolean true check |
| `isFalse(path)` | Boolean false check |

> All methods return `null` when the value is null or empty. QueryDSL silently ignores `null` predicates in `where()` clauses, so no explicit null checks are needed at the call site.
