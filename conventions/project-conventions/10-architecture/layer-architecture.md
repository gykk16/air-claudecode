# Layer Architecture

## 4-Layer Structure

```
Bootstrap (Controller → Facade)
  → Domain Application (QueryApplication / CommandApplication)
    → Domain Service (Business Logic)
      → Domain Repository (JpaRepository / QueryRepository)
        → Domain Entity
```

Upper layers depend on lower layers only. Reverse dependencies prohibited.

---

## Layer 1: Bootstrap (HTTP Entry Point)

### Controller

| Item | Rule |
|------|------|
| Location | `{appname}/api/{Feature}Controller.kt` |
| Dependency Injection | **Facade only** (no Service/Application/Repository) |
| Return Type | `ResponseEntity<ApiResource<T>>` |
| Responsibility | Converts API Request DTO to Domain Request DTO |

```kotlin
@RestController
@RequestMapping("/api/holidays")
class HolidayController(private val holidayFacade: HolidayFacade) {
    @GetMapping("/{year}")
    fun getByYear(@PathVariable year: Int, pageable: Pageable): ResponseEntity<ApiResource<List<HolidayDto>>> =
        ApiResource.ofPage(holidayFacade.findPageByYear(year, pageable))

    @PostMapping
    fun create(@Valid @RequestBody request: CreateHolidayApiRequest): ResponseEntity<ApiResource<HolidayDto>> {
        val holiday = holidayFacade.create(CreateHolidayRequest(request.holidayDate, request.name))
        return ApiResource.success(holiday)
    }
}
```

### Facade (`@Component`)

| Item | Rule |
|------|------|
| Location | `{appname}/facade/{Feature}Facade.kt` |
| Dependency Injection | `QueryApplication`, `CommandApplication` |
| Annotation | `@Component` |
| KST Conversion | `.toKst()` happens here |

```kotlin
@Component
class HolidayFacade(
    private val holidayQueryApplication: HolidayQueryApplication,
    private val holidayCommandApplication: HolidayCommandApplication,
) {
    fun findPageByYear(year: Int, pageable: Pageable): Page<HolidayDto> =
        holidayQueryApplication.findPageByYear(year, pageable).map { HolidayDto.from(it) }

    fun create(request: CreateHolidayRequest): HolidayDto =
        HolidayDto.from(holidayCommandApplication.create(request))
}
```

**DTO Locations:**

| DTO Type | Location | Example |
|----------|----------|---------|
| API Request DTO | `{appname}/api/dto/` | `CreateHolidayApiRequest` |
| API Response DTO | `{appname}/api/dto/` | `HolidayDto` |
| Domain Request DTO | `domain/{feature}/dto/` | `CreateHolidayRequest` |
| Domain Info DTO | `domain/{feature}/dto/` | `HolidayInfo` |

---

## Layer 2: Domain Application (Orchestration)

**Package**: `{projectGroup}.domain.{feature}.application`

Thin delegation layer for transaction boundaries (CQRS-lite). Can inject Services from **multiple domains**; must **NOT** inject another Application.

### QueryApplication and CommandApplication

| Item | QueryApplication | CommandApplication |
|------|------------------|--------------------|
| Annotation | `@Service`, `@Transactional(readOnly = true)` | `@Service`, `@Transactional` |
| DataSource | Slave (Reader) | Master (Writer) |
| Return Type | `{Feature}Info` or `Page<{Feature}Info>` | `{Feature}Info` |
| Injection | Service only | Service only |

```kotlin
@Service
@Transactional(readOnly = true)
class HolidayQueryApplication(private val holidayService: HolidayService) {
    fun findPageByYear(year: Int, pageable: Pageable): Page<HolidayInfo> =
        holidayService.findPageByYear(year, pageable)
}

@Service
@Transactional
class HolidayCommandApplication(private val holidayService: HolidayService) {
    fun create(request: CreateHolidayRequest): HolidayInfo = holidayService.create(request)
    fun update(id: Long, request: UpdateHolidayRequest): HolidayInfo = holidayService.update(id, request)
    fun delete(id: Long) = holidayService.delete(id)
}
```

---

## Layer 3: Domain Service (Business Logic)

**Package**: `{projectGroup}.domain.{feature}.service`

| Item | Rule |
|------|------|
| Annotation | `@Service` |
| Transaction | **No** `@Transactional` (propagated from Application) |
| Dependency Injection | Repository only (JpaRepository, QueryRepository) |
| Return Type | `{Feature}Info` |
| Conversion | `{Feature}Info.from(entity)` |
| Same-layer injection | Other Service injection allowed |

```kotlin
@Service
class HolidayService(
    private val holidayJpaRepository: HolidayJpaRepository,
    private val holidayQueryRepository: HolidayQueryRepository,
) {
    fun findPageByYear(year: Int, pageable: Pageable): Page<HolidayInfo> =
        holidayQueryRepository.fetchPageByYear(year, pageable)

    fun findById(id: Long): HolidayInfo =
        holidayJpaRepository.findById(id)
            .map { HolidayInfo.from(it) }
            .orElseThrow { HolidayNotFoundException(id) }

    fun create(request: CreateHolidayRequest): HolidayInfo =
        HolidayInfo.from(holidayJpaRepository.save(Holiday.create(request.holidayDate, request.name)))

    fun update(id: Long, request: UpdateHolidayRequest): HolidayInfo {
        val entity = holidayJpaRepository.findById(id).orElseThrow { HolidayNotFoundException(id) }
        entity.update(request.holidayDate, request.name)
        return HolidayInfo.from(entity)  // JPA dirty checking
    }
}
```

---

## Layer 4: Domain Repository (Persistence)

**Package**: `{projectGroup}.domain.{feature}.repository`

### JpaRepository — simple CRUD, derived queries, `@Query`

```kotlin
@Repository
interface HolidayJpaRepository : JpaRepository<Holiday, Long> {
    @Query("select h from Holiday h where year(h.holidayDate) = :year order by h.holidayDate")
    fun findByYear(year: Int): List<Holiday>
}
```

### QueryRepository — dynamic conditions, pagination, complex joins. **Methods must use `fetch` prefix**.

```kotlin
@Repository
class HolidayQueryRepository : QuerydslRepositorySupport(Holiday::class.java) {
    fun fetchPageByYear(year: Int, pageable: Pageable): Page<HolidayInfo> =
        applyPagination(
            pageable,
            contentQuery = { it.selectFrom(holiday).where(holiday.holidayDate.year().eq(year)).orderBy(holiday.holidayDate.asc()) },
            countQuery = { it.select(holiday.count()).from(holiday).where(holiday.holidayDate.year().eq(year)) },
        ).map { HolidayInfo.from(it) }
}
```

---

## Domain Entity & DTO

### Entity

Rules: extends `BaseTimeEntity`, mutable fields use `private set`, mutations via `update()`, factory via `companion object { fun create(...) }`, **Entity must NOT import DTO**.

```kotlin
@Entity
@Table(name = "holidays")
class Holiday(holidayDate: LocalDate, name: String, id: Long? = null) : BaseTimeEntity() {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long? = id
    @Column(nullable = false) var holidayDate: LocalDate = holidayDate; private set
    @Column(nullable = false, length = 100) var name: String = name; private set

    fun update(holidayDate: LocalDate, name: String) { this.holidayDate = holidayDate; this.name = name }
    companion object { fun create(holidayDate: LocalDate, name: String) = Holiday(holidayDate, name) }
}
```

### Domain DTOs

> Entity must not import DTO classes. Use `{Feature}Info.from(entity)` pattern — never `entity.toInfo()`.

```kotlin
data class HolidayInfo(val id: Long, val holidayDate: LocalDate, val name: String) {
    companion object {
        fun from(entity: Holiday) = HolidayInfo(entity.id!!, entity.holidayDate, entity.name)
    }
}

data class CreateHolidayRequest(val holidayDate: LocalDate, val name: String)
data class UpdateHolidayRequest(val holidayDate: LocalDate, val name: String)

class HolidayNotFoundException(id: Long) : KnownException("Holiday not found: $id")
```

---

## DTO Flow

```
[HTTP Request JSON] → CreateHolidayApiRequest (Bootstrap) → CreateHolidayRequest (Domain)
  → Holiday Entity → HolidayInfo.from(entity) → HolidayDto (Bootstrap) → [HTTP Response JSON]
```

| Step | From | To | Where |
|------|------|----|-------|
| HTTP in | JSON body | `{Feature}ApiRequest` (Bootstrap) | Spring deserialization |
| Bootstrap → Domain | `{Feature}ApiRequest` | `{Feature}Request` (Domain) | Controller or Facade |
| Domain write | `{Feature}Request` | `{Feature}` Entity | Service (`Entity.create()`) |
| Domain read | `{Feature}` Entity | `{Feature}Info` (Domain) | Service (`Info.from(entity)`) |
| Domain → Bootstrap | `{Feature}Info` | `{Feature}Dto` (Bootstrap) | Facade (`Dto.from(info)`) |
| HTTP out | `{Feature}Dto` | JSON body | `ApiResource.success()` |

---

## Dependency Direction Rule

`Controller → Facade → Application → Service → Repository` — each layer injects **only the layer immediately below**.

| Layer | Injects | Prohibited |
|-------|---------|------------|
| Controller | Facade only | Service, Application, Repository |
| Facade | Application only | Service, Repository |
| Application | Service only | Repository, other Application |
| Service | Repository | (other Services OK within same domain) |

| Layer | Transaction | DataSource |
|-------|-------------|------------|
| Controller / Facade | None | - |
| QueryApplication | `@Transactional(readOnly = true)` | Slave (Reader) |
| CommandApplication | `@Transactional` | Master (Writer) |
| Service | None (propagated from Application) | - |

---

## Cross-Domain Orchestration

### Approach 1: Facade → Multiple Applications (Separate Transactions)

```kotlin
@Component
class BookingFacade(
    private val bookingCommandApplication: BookingCommandApplication,
    private val paymentQueryApplication: PaymentQueryApplication,
    private val userQueryApplication: UserQueryApplication,
) {
    fun createBooking(request: CreateBookingApiRequest): BookingDto {
        val user    = userQueryApplication.findById(request.userId)           // TX 1 (readOnly)
        val payment = paymentQueryApplication.findById(request.paymentId)     // TX 2 (readOnly)
        val booking = bookingCommandApplication.create(                        // TX 3 (write)
            CreateBookingRequest(user.id, payment.id, request.scheduleId))
        return BookingDto.from(booking)
    }
}
```

### Approach 2: Cross-Domain Application (Single Transaction)

```kotlin
@Service
@Transactional
class BookingCommandApplication(
    private val bookingService: BookingService,
    private val paymentService: PaymentService,
    private val inventoryService: InventoryService,
) {
    fun create(request: CreateBookingRequest): BookingInfo {
        val booking = bookingService.create(request)
        paymentService.reserve(booking.id, request.paymentId)
        inventoryService.decrease(booking.scheduleId)
        return booking
    }
}
```

| Approach | Transaction | Use Case | Risk |
|----------|-------------|----------|------|
| Facade → multiple Applications | Separate per call | Independent reads, fire-and-forget | No atomicity guarantee |
| Application → multiple Services | Single shared transaction | Write operations requiring atomicity | Longer lock hold time |

---

## Anti-Patterns

| # | Anti-Pattern | Problem | Correct Method |
|---|--------------|---------|----------------|
| 1 | Controller calls Service directly | Bypasses Facade and Application layers | Controller → Facade → Application → Service |
| 2 | Controller calls Application directly | Bypasses Facade; no DTO conversion | Controller → Facade → Application |
| 3 | Facade calls Repository directly | Skips Application and Service layers | Facade → Application → Service → Repository |
| 4 | Service returns API DTO (`{Feature}Dto`) | Creates upward dependency on Bootstrap | Service returns Domain DTO (`{Feature}Info`) only |
| 5 | Return Entity as API response | Exposes internal structure; no contract | Entity → Info → Dto conversion chain |
| 6 | Business logic in Application | Role confusion; Application is delegation only | Business logic belongs in Service |
| 7 | `@Transactional` on Service | Duplicate transaction management; conflicts | Manage transactions only at Application level |
| 8 | `entity.toInfo()` method in Entity | Reversed dependency; Entity imports DTO | Use `{Feature}Info.from(entity)` pattern |
| 9 | Application injecting another Application | Breaks layer rule; nested transaction risk | Inject Services from multiple domains instead |
| 10 | Facade injecting Service or Repository | Skips intermediate layers | Facade injects Application only |
