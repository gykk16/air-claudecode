# Common Module Reference

## Value Objects (required)

Use typed Value Objects instead of primitive types.

| Type | Instead of | Create | Key methods |
|------|-----------|--------|-------------|
| `Email` | `String` | `Email.of()`, `.asEmail` | `.masked()`, `.isValid` |
| `PhoneNumber` | `String` | `PhoneNumber.of()`, `.asPhoneNumber` | `.toE164()`, `.toNational()`, `.isValid`, `.isValidMobile` |
| `Money` | `BigDecimal`/`Long` | `Money.krw()`, `Money.usd()`, extension | arithmetic operators, `.format()` |
| `Rate` | `Double`/`BigDecimal` | `Rate.ofPercent()`, `.percent`, `.of()` | `.applyTo()`, `.remainderOf()` |

---

### Email

```kotlin
val email = Email.of("user@example.com")   // factory
val email = "user@example.com".asEmail     // extension
val isValid = Email.isValid("user@example.com")  // true
val masked = email.masked()                // "us**@example.com"
```

---

### Money

```kotlin
val price = Money.krw(10_000L)             // factory
val price = 10_000L.krw                    // extension

val total    = price + fee.toKrw()         // addition
val doubled  = price * 2                   // scalar multiplication
val discount = price * BigDecimal("0.9")
val formatted = price.format()             // "10,000"

val discountRate = Rate.ofPercent(10)
val discounted   = price.applyRate(discountRate)  // price * 0.90
```

`PhoneNumber` and `Rate` follow the same factory/extension/method pattern as above. See the table for their specific methods.

---

## Exceptions

| Class | Usage | Logging |
|-------|-------|---------|
| `KnownException` | Expected errors (validation, not found) | INFO, no stack trace |
| `BizRuntimeException` | Unrecoverable business errors | ERROR, with stack trace |
| `BizException` | Recoverable business errors | ERROR |

```kotlin
// Feature exception hierarchy (domain/{feature}/exception/)
open class OrderException(error: OrderError, message: String? = null) :
    KnownException(error, message ?: error.message)

class OrderNotFoundException(id: Long) : OrderException(
    OrderError.NOT_FOUND, "Order not found: id=$id",
)
class OrderAlreadyCancelledException(id: Long) : OrderException(
    OrderError.ALREADY_CANCELLED, "Order already cancelled: id=$id",
)
```

### Precondition Validation

```kotlin
knownRequired(order.status == OrderStatus.PENDING, OrderError.INVALID_STATE) {
    "Order must be PENDING to confirm. current=${order.status}"
}
val user = knownRequiredNotNull(userRepository.findById(userId), UserError.NOT_FOUND) {
    "User not found: id=$userId"
}
knownNotBlank(request.reason, OrderError.REASON_REQUIRED) { "Reason must not be blank" }
```

---

## DateTime Utilities

| Utility | Methods |
|---------|---------|
| `DateFormatter` | `.toDate()`, `.toDateTime()`, `.toStr()`, `.toKorean()` |
| `SearchDates` | `.lastMonth()`, `.lastDays(n)`, `.thisWeek()`, `.of(start, end)` |
| `LocalDateRange` | `.from(start, end)`, `in`, `.overlaps()`, `.daysBetween()` |

---

## Extensions

### String

`.maskName()`, `.maskDigits()`, `.maskEmail()`, `.ifNullOrBlank()`, `.removeAllSpaces()`

### DateTime

`.isToday()`, `.isPast()`, `.getAge()`, `.getKoreanAge()`, `.toKst()`, `.toUtc()`

---

## Other Utilities

| Utility | Purpose |
|---------|---------|
| `stopWatch` | Measure execution time |
| `runBlockingWithMDC` / `asyncWithMDC` | Coroutine MDC propagation |
| `AesCipher` | AES encryption/decryption |

```kotlin
val elapsed = stopWatch { processOrder(order) }
log.info("processOrder took ${elapsed}ms")

val cipher = AesCipher(secretKey = "your-32-char-secret-key-here!!!!")
val encrypted = cipher.encrypt("sensitive-data")
val decrypted = cipher.decrypt(encrypted)
```
