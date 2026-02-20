# JPA & Hibernate

## 1. Core Principles

| Principle | Rule |
|-----------|------|
| **Base class** | Always extend `BaseEntity` (full auditing) or `BaseTimeEntity` (timestamps only) |
| **Enum mapping** | Always use `@Enumerated(EnumType.STRING)` -- never ORDINAL |
| **Fetch type** | Always use `FetchType.LAZY` for all associations |
| **Table name** | Always specify `@Table(name = "xxx")` explicitly |
| **No associations** | Default: store FK as plain ID value, do NOT map entity associations |

---

## 2. BaseEntity vs BaseTimeEntity

| Class | When to use | Fields |
|-------|-------------|--------|
| `BaseTimeEntity` | Auditing by time only (no user tracking needed) | `createdAt`, `modifiedAt` |
| `BaseEntity` | Full auditing (time + user) | `createdAt`, `modifiedAt`, `createdBy`, `modifiedBy` |

```kotlin
@MappedSuperclass
@EntityListeners(AuditingEntityListener::class)
abstract class BaseTimeEntity {

    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    lateinit var createdAt: LocalDateTime
        protected set

    @LastModifiedDate
    @Column(name = "modified_at", nullable = false)
    lateinit var modifiedAt: LocalDateTime
        protected set
}

@MappedSuperclass
@EntityListeners(AuditingEntityListener::class)
abstract class BaseEntity : BaseTimeEntity() {

    @CreatedBy
    @Column(name = "created_by", nullable = false, updatable = false, length = 50)
    lateinit var createdBy: String
        protected set

    @LastModifiedBy
    @Column(name = "modified_by", nullable = false, length = 50)
    lateinit var modifiedBy: String
        protected set
}
```

---

## 3. Association Policy

| Rule | Description |
|------|-------------|
| **Default** | Do NOT map entity associations -- store FK as plain ID value |
| **Exception** | Unidirectional only, when absolutely necessary |
| **Prohibited** | Bidirectional associations are strictly forbidden |
| **Querying** | Use QueryDSL for joining related data |

### Correct: No Association (store FK as ID)

```kotlin
@Entity
@Table(name = "orders")
class Order(
    val userId: Long,       // store FK as plain Long, NOT @ManyToOne User
    val totalAmount: Long,
) : BaseEntity() {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0
}
```

### Exception: Unidirectional Only (when absolutely necessary)

```kotlin
@Entity
@Table(name = "order_items")
class OrderItem(
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id", nullable = false)
    val order: Order,

    val productId: Long,
    val quantity: Int,
) : BaseEntity() {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0
}
```

---

## 4. Entity Structure

### Standard Entity Pattern

```kotlin
@Entity
@Table(name = "users")
class User(
    val email: String,

    var name: String,

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, length = 30)
    var status: UserStatus,
) : BaseEntity() {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0

    fun updateName(newName: String) {
        this.name = newName
    }

    companion object {
        fun create(email: String, name: String): User {
            return User(
                email = email,
                name = name,
                status = UserStatus.ACTIVE,
            )
        }
    }
}
```

### Entity Checklist

| Item | Requirement |
|------|-------------|
| `@Entity` | Required on every entity class |
| `@Table(name = "...")` | Always specify explicit table name |
| Extends base class | Must extend `BaseEntity` or `BaseTimeEntity` |
| `val` for id | Use `val` for immutable fields (`id`) |
| `var` for mutable | Use `var` for fields that change |
| Domain enums | Must implement `CommonCode` interface |
| Mutation method | Mutations via `update*()` method |
| Factory method | Creation via `create()` companion object function |
| No DTO import | Entity must NOT import DTO classes |

---

## 5. Enum Mapping

Always use `EnumType.STRING` -- never `ORDINAL` (breaks if enum values are reordered).

```kotlin
@Enumerated(EnumType.STRING)
@Column(name = "status", nullable = false, length = 30)
var status: OrderStatus = OrderStatus.PENDING
```

All domain enums must implement the `CommonCode` interface from the common module:

```kotlin
enum class OrderStatus(
    override val code: String,
    override val displayName: String,
) : CommonCode {
    PENDING("PENDING", "대기중"),
    CONFIRMED("CONFIRMED", "확정"),
    CANCELLED("CANCELLED", "취소"),
}
```

---

## 6. Fetch Strategies

Always use `FetchType.LAZY`. `@ManyToOne` and `@OneToOne` default to `EAGER` in JPA -- you MUST override them explicitly:

```kotlin
@ManyToOne(fetch = FetchType.LAZY)
@JoinColumn(name = "order_id")
val order: Order
```

Lazy loading issues (`LazyInitializationException`, N+1) are resolved by fetching as a DTO via QueryDSL within the transaction -- never by switching to `EAGER`.

---

## 7. Locking Strategies

| Strategy | Annotation | Use Case |
|----------|-----------|---------|
| **Optimistic** | `@Version` | Low contention, read-heavy; fails fast on conflict |
| **Pessimistic** | `@Lock(LockModeType.PESSIMISTIC_WRITE)` | High contention, critical sections; blocks concurrent access |

```kotlin
// Optimistic: add @Version field to the entity
@Version
val version: Long = 0

// Pessimistic: annotate the repository query method
@Lock(LockModeType.PESSIMISTIC_WRITE)
@Query("select p from Product p where p.id = :id")
fun findByIdWithLock(@Param("id") id: Long): Product?
```

---

## 8. Entity State & Dirty Checking

Managed entities within a `@Transactional` method are automatically tracked -- no explicit `save()` call is needed for updates, just mutate the entity.

```kotlin
@Transactional
fun updateUserName(userId: Long, newName: String) {
    val user = userRepository.findById(userId)
        ?: throw UserNotFoundException(userId)

    user.updateName(newName)
    // No userRepository.save(user) needed -- dirty checking handles it
}
```

---

## 9. Configuration

### Recommended YAML Settings

```yaml
spring:
  jpa:
    hibernate:
      ddl-auto: none              # never auto-generate DDL in production
    open-in-view: false           # disable OSIV (mandatory)
    properties:
      hibernate:
        default_batch_fetch_size: 500
        jdbc.batch_size: 500
        order_updates: true       # batch UPDATE statements together
        order_inserts: true       # batch INSERT statements together
```

### OSIV (Open Session in View)

> **Mandatory**: Set `open-in-view: false`. OSIV keeps the DB connection open for the entire HTTP request lifecycle, causing connection pool exhaustion under load. With it disabled, connections are released at the end of `@Transactional` scope and all data fetching must be explicit in the service layer.
