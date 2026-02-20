# DateTime Handling

> Store and process in UTC. Convert to KST only at the final display boundary.

## Core Rules

| Rule | Description |
|------|-------------|
| **Internal timezone** | UTC everywhere (JVM, DB, domain logic) |
| **Controller input** | Must be UTC. If KST arrives, convert to UTC immediately |
| **Controller output** | UTC by default. Convert to KST only when display requires it |
| **KST conversion** | Use `.toKst()` extension only at the response boundary (Facade / Response DTO) |
| **Utilities** | Use `{projectGroup}.common.utils.datetime` for all datetime operations |

---

## JVM Timezone Configuration

Set UTC as the JVM default timezone in every bootstrap `-app` module.

```kotlin
fun main(args: Array<String>) {
    TimeZone.setDefault(TimeZone.getTimeZone("UTC"))
    runApplication<MyApplication>(*args)
}
```

> **IMPORTANT**: Without this configuration, `LocalDateTime.now()` returns system-local time (KST on Korean servers), causing inconsistencies.

---

## Controller Input: Always UTC

All datetime inputs in controllers must be UTC. If a client sends KST, convert to UTC immediately in the Controller or Facade layer before passing it to domain.

```kotlin
// UTC input -- pass directly
@PostMapping("/events")
fun createEvent(@Valid @RequestBody request: CreateEventApiRequest): ResponseEntity<ApiResource<EventDto>> {
    return ApiResource.success(eventFacade.create(CreateEventRequest(name = request.name, startAt = request.startAt)))
}

// KST input -- convert to UTC immediately at the entry point
@PostMapping("/events")
fun createEvent(@Valid @RequestBody request: CreateEventApiRequest): ResponseEntity<ApiResource<EventDto>> {
    val utcStartAt = request.startAt.toUtc()  // convert KST → UTC here
    return ApiResource.success(eventFacade.create(CreateEventRequest(name = request.name, startAt = utcStartAt)))
}
```

When timezone-aware input is needed, use `ZonedDateTime` and normalize to UTC:

```kotlin
data class CreateEventApiRequest(
    val name: String,
    @param:JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ssXXX'['VV']'")
    val startAt: ZonedDateTime,
)

val utcStartAt = request.startAt.withZoneSameInstant(ZoneOffset.UTC).toLocalDateTime()
```

---

## Controller Output: KST Conversion at Response Boundary

Convert to KST only when building the API response DTO. Domain and Service layers must never perform KST conversion.

```kotlin
// In Facade -- UTC → KST at response boundary
@Component
class EventFacade(private val eventQueryApplication: EventQueryApplication) {
    fun findById(id: Long): EventDto {
        val event = eventQueryApplication.findById(id)
        return EventDto(
            id = event.id,
            name = event.name,
            startAt = event.startAt.toKst(),
            createdAt = event.createdAt.toKst(),
        )
    }
}
```

Alternatively, convert inside the Response DTO factory (`from()`) using `.toKst()`.

---

## DateTime Lifecycle

```
[Client Request]
  UTC datetime input (or KST → convert to UTC immediately)
    ↓
[Controller / Facade]
  Ensure UTC before passing to domain
    ↓
[Domain (Application → Service → Repository)]
  All operations in UTC. No KST awareness.
    ↓
[Database]
  Stored as UTC
    ↓
[Domain → Facade / Response DTO]
  Convert to KST with .toKst() only if display requires it
    ↓
[Client Response]
  KST for display, or UTC for machine-to-machine
```

---

## Utility Classes

> **IMPORTANT**: Use `{projectGroup}.common.utils.datetime` for all datetime operations. Do not use raw `java.time` formatting or manual calculations.

### DateFormatter (parsing & formatting)

| Method | Result |
|--------|--------|
| `"2025-01-24".toDate()` | `LocalDate` |
| `"20250124".numericToDate()` | `LocalDate` |
| `"2025-01-24T14:30:00".toDateTime()` | `LocalDateTime` |
| `date.toStr()` | `"2025-01-24"` |
| `date.toNumericStr()` | `"20250124"` |
| `date.toKorean()` | `"2025년 1월 24일"` |
| `dateTime.toStr()` | `"2025-01-24T14:30:00"` |
| `dateTime.toKorean()` | `"2025년 1월 24일 14시 30분"` |

### Timezone Conversion

| Method | Direction | Use Case |
|--------|-----------|----------|
| `LocalDateTime.toKst()` | UTC → KST | Display in Facade / Response DTO |
| `ZonedDateTime.toKst()` | UTC → KST | Display in Facade / Response DTO |
| `LocalDateTime.toUtc()` | KST → UTC | Normalize KST input at controller boundary |
| `ZonedDateTime.toUtc()` | KST → UTC | Normalize KST input at controller boundary |

### SearchDates (date range for queries)

```kotlin
val dates = SearchDates.lastMonth()
val dates = SearchDates.of(startDate, endDate)
val dates = SearchDates.lastDays(7)
val dates = SearchDates.thisWeek()

data class OrderSearchCondition(
    val status: OrderStatus? = null,
    val searchDates: SearchDates = SearchDates.lastMonth(),
)
```

### Range Classes

```kotlin
val range = LocalDateRange(startDate, endDate)
date in range                // containment check
range.overlaps(otherRange)   // overlap check
range.daysBetween()          // day count

val dtRange = LocalDateTimeRange(startDt, endDt)
dtRange.hoursBetween()
```

### Date Extensions

```kotlin
date.isToday()
date.isPast()
birthDate.getAge()           // International age
birthDate.getKoreanAge()     // Korean age
```

---

## ISO-8601 Formats

| Type | Format | Example |
|------|--------|---------|
| Date | `yyyy-MM-dd` | `2025-01-02` |
| Time | `HH:mm:ss` | `14:30:00` |
| DateTime | `yyyy-MM-dd'T'HH:mm:ss` | `2025-01-02T14:30:00` |
| DateTime UTC | `yyyy-MM-dd'T'HH:mm:ss'Z'` | `2025-01-02T05:30:00Z` |
| ZonedDateTime | `yyyy-MM-dd'T'HH:mm:ssXXX'['VV']'` | `2025-01-02T14:30:00+09:00[Asia/Seoul]` |
