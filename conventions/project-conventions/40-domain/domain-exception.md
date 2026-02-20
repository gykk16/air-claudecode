# Domain Exception Handling

> Each domain feature has its own `{Feature}Error` enum, `{Feature}Exception` base class, and specific exception subclasses.

## Exception Hierarchy

```
BizRuntimeException (common) -- unrecoverable business errors, with stack trace
BizException (common) -- recoverable business errors, with stack trace
KnownException (common) -- expected errors (validation, not found), no stack trace
  └── {Feature}Exception (domain) -- feature-specific base, open class
        ├── {Feature}NotFoundException
        ├── {Feature}AlreadyExistsException
        └── {Feature}InvalidStateException
```

| Class | Module | Purpose | HTTP Status | Stack Trace |
|---|---|---|---|---|
| `BizRuntimeException` | common | Unrecoverable errors (data integrity failures) | 500 | Yes |
| `BizException` | common | Recoverable business errors | 500 | Yes |
| `KnownException` | common | Expected errors -- logged at INFO | 406 | No |
| `{Feature}Exception` | domain | Feature-specific base; extends `KnownException` | 406 | No |
| `{Feature}NotFoundException` | domain | Entity not found within the feature | 406 | No |

---

## Package Structure

```
domain/{feature}/
└── exception/
    ├── {Feature}Error.kt        # Error code enum implementing ResponseCode
    └── {Feature}Exception.kt    # Base exception + all subclasses
```

---

## Error Code Enum

```kotlin
enum class HolidayError(
    override val code: String,
    override val message: String,
    override val status: HttpStatus = HttpStatus.NOT_ACCEPTABLE,
) : ResponseCode {
    NOT_FOUND("HOLIDAY_001", "공휴일 정보를 찾을 수 없습니다."),
    ALREADY_EXISTS("HOLIDAY_002", "이미 등록된 공휴일입니다."),
    INVALID_DATE_RANGE("HOLIDAY_003", "공휴일 날짜 범위가 올바르지 않습니다."),
    CANNOT_DELETE_PAST("HOLIDAY_004", "이미 지난 공휴일은 삭제할 수 없습니다."),
}
```

### Naming Conventions

| Element | Convention | Example |
|---|---|---|
| Enum class name | `{Feature}Error` | `HolidayError` |
| Constant name | `SCREAMING_SNAKE_CASE` | `NOT_FOUND`, `ALREADY_EXISTS` |
| Code value | `{FEATURE}_{3-digit sequence}` | `HOLIDAY_001` |
| Message language | Korean | `"공휴일 정보를 찾을 수 없습니다."` |
| Default HTTP status | `406 NOT_ACCEPTABLE` | `HttpStatus.NOT_ACCEPTABLE` |

Use `{Feature}Error` for feature-specific errors. Use common `ErrorCode` for generic validation or input format errors at the API layer.

---

## Exception Classes

```kotlin
// Base exception -- must be open class
open class HolidayException(
    error: HolidayError,
    message: String = error.message,
) : KnownException(error, message)

// Specific subclass
class HolidayNotFoundException(holidayId: Long) : HolidayException(
    error = HolidayError.NOT_FOUND,
    message = "공휴일 정보를 찾을 수 없습니다. holidayId=$holidayId",
)

// Without subclass -- for rare or one-off errors
throw HolidayException(HolidayError.CANNOT_DELETE_PAST)
throw HolidayException(
    error = HolidayError.INVALID_DATE_RANGE,
    message = "공휴일 날짜 범위가 올바르지 않습니다. startDate=$startDate, endDate=$endDate",
)
```

### Subclass Patterns

| Subclass | Constructor parameter | Message pattern |
|---|---|---|
| `{Feature}NotFoundException` | Entity identifier (`id: Long`) | `"... 찾을 수 없습니다. {feature}Id=$id"` |
| `{Feature}AlreadyExistsException` | Unique key (`date: LocalDate`) | `"이미 등록되어 있습니다. date=$date"` |
| `{Feature}InvalidStateException` | Current state value | `"올바르지 않은 상태입니다. status=$status"` |

---

## Usage in Service

Throw exceptions in the **Service layer only**. Always include relevant context in the message.

```kotlin
@Service
@Transactional(readOnly = true)
class HolidayService(private val holidayRepository: HolidayRepository) {

    fun findById(holidayId: Long): Holiday =
        holidayRepository.findById(holidayId) ?: throw HolidayNotFoundException(holidayId)

    @Transactional
    fun create(date: LocalDate, name: String): Holiday {
        if (holidayRepository.existsByDate(date)) {
            throw HolidayException(HolidayError.ALREADY_EXISTS, "이미 등록된 공휴일입니다. date=$date")
        }
        return holidayRepository.save(Holiday(date = date, name = name))
    }
}
```
