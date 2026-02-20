# Common Codes & Enums

## Core Rule

All categorized domain codes must implement `CommonCode` from `{projectGroup}.common.codes`. Always persist enums as `EnumType.STRING` -- never `ORDINAL`.

## CommonCode Interface

```kotlin
interface CommonCode {
    val code: String        // Machine-readable code value
    val description: String // Human-readable description
    val name: String        // Enum constant name (from Kotlin enum)
}
```

## Enum Definition

### Standard Pattern

```kotlin
enum class OrderStatus(
    override val code: String,
    override val description: String,
) : CommonCode {
    PENDING("PENDING", "Order placed, awaiting payment"),
    PAID("PAID", "Payment confirmed"),
    CANCELLED("CANCELLED", "Order cancelled"),
    ;

    companion object {
        fun fromCode(code: String): OrderStatus =
            entries.find { it.code == code }
                ?: throw IllegalArgumentException("Unknown OrderStatus code: $code")
    }
}
```

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Enum class | PascalCase, descriptive noun | `OrderStatus`, `PaymentMethod` |
| Enum constants | SCREAMING_SNAKE_CASE | `PENDING`, `IN_PROGRESS` |
| `code` value | Matches constant name or domain-specific code | `"PENDING"`, `"CC"` |
| `description` | Clear English description | `"Order placed, awaiting payment"` |

Add a trailing semicolon (`;`) after the last enum constant when the enum has a companion object or methods.

## JPA Entity Usage

Always use `@Enumerated(EnumType.STRING)`. Never use `EnumType.ORDINAL` -- it breaks silently when you reorder or remove constants.

```kotlin
@Enumerated(EnumType.STRING)
@Column(nullable = false, length = 20)   // length = longest constant name, with headroom
var status: OrderStatus = OrderStatus.PENDING
```

## Lookup Methods

```kotlin
// Throws when code is unknown
fun fromCode(code: String): PaymentMethod =
    entries.find { it.code == code }
        ?: throw IllegalArgumentException("Unknown PaymentMethod code: $code")

// Returns null when code is unknown
fun fromCodeOrNull(code: String): PaymentMethod? =
    entries.find { it.code == code }
```

## When to Use CommonCode

| Scenario | Use CommonCode |
|----------|---------------|
| Business status codes (`OrderStatus`, `BookingStatus`) | Yes |
| Category/type classifications (`PaymentMethod`, `BookingType`) | Yes |
| Role/permission types (`UserRole`, `MembershipTier`) | Yes |
| Configuration flags (simple `Boolean`) | No |
| Internal-only markers | No -- plain enum or sealed class |
| Response codes | No -- use `ResponseCode` interface instead |

```kotlin
// Response codes use ResponseCode, not CommonCode
enum class ErrorCode(
    override val status: Int,
    override val message: String,
) : ResponseCode {
    DATA_NOT_FOUND(406, "Data not found"),
}

// Internal enum without CommonCode is fine
enum class SortDirection { ASC, DESC }
```

## Package Location

| Module | Location |
|--------|----------|
| Domain-specific codes | `domain/{feature}/entity/` (alongside Entity) |
| Shared across features | `domain/common/codes/` |
| Common module codes | `common/codes/` |

## REST Docs Integration

`CommonCodeDocsTest` automatically documents enums implementing `CommonCode`. The test generates REST Docs snippets listing all `code` and `description` pairs, keeping API documentation in sync with the codebase.
