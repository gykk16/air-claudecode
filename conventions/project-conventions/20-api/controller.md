# Controller Design

## URL Design

### Base Path Rules

All API paths must start with `/api/v1/`.

### kebab-case

Use kebab-case for all URL segments. Never use camelCase or snake_case.

### Plural Resource Names

Resource names must be plural nouns.

### RESTful URL Patterns

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/v1/orders/{id}` | Get single resource |
| GET | `/api/v1/orders` | Get paginated list |
| POST | `/api/v1/orders` | Create resource |
| PUT | `/api/v1/orders/{id}` | Replace resource (full update) |
| PATCH | `/api/v1/orders/{id}` | Partial update |
| DELETE | `/api/v1/orders/{id}` | Delete resource |
| POST | `/api/v1/orders/bulk` | Bulk create |
| GET | `/api/v1/orders/{id}/items` | Sub-resource list |

**URL Design Guidelines**

| Rule | Good | Bad |
|------|------|-----|
| Nouns not verbs | `/api/v1/orders` | `/api/v1/getOrders` |
| Hierarchy | `/api/v1/orders/{id}/items` | `/api/v1/order-items?orderId=` |
| Max 3 levels | `/api/v1/orders/{id}/items` | `/api/v1/users/{id}/orders/{id}/items/{id}/details` |
| No trailing slashes | `/api/v1/orders` | `/api/v1/orders/` |
| Actions as sub-paths | `POST /api/v1/orders/{id}/cancel` | `POST /api/v1/cancelOrder` |

---

## Response Format

### ApiResource Methods

| Method | Usage |
|--------|-------|
| `ApiResource.success()` | DELETE or void response |
| `ApiResource.success(data)` | Single object response |
| `ApiResource.of(data)` | Alias for `success(data)` |
| `ApiResource.ofPage(page)` | Paginated response (Page<T>) |
| `ApiResource.ofCollection(list)` | Non-paginated list response |

### Pageable Default

Always use `@PageableDefault(size = 100)`. Never rely on Spring's default (20).

### Standard CRUD Controller Example

```kotlin
@RestController
@RequestMapping("/api/v1/orders")
class OrderController(
    private val orderFacade: OrderFacade,
) {

    @GetMapping("/{id}")
    fun getOrder(
        @PathVariable id: Long,
    ): ResponseEntity<ApiResource<OrderApiResponse>> {
        return ResponseEntity.ok(ApiResource.success(orderFacade.getOrder(id)))
    }

    @GetMapping
    fun getOrders(
        @PageableDefault(size = 100) pageable: Pageable,
    ): ResponseEntity<ApiResource<Page<OrderApiResponse>>> {
        return ResponseEntity.ok(ApiResource.ofPage(orderFacade.getOrders(pageable)))
    }

    @PostMapping
    fun createOrder(
        @Valid @RequestBody request: CreateOrderApiRequest,
    ): ResponseEntity<ApiResource<OrderApiResponse>> {
        return ResponseEntity.ok(ApiResource.success(orderFacade.createOrder(request.toDomainRequest())))
    }

    @PutMapping("/{id}")
    fun updateOrder(
        @PathVariable id: Long,
        @Valid @RequestBody request: UpdateOrderApiRequest,
    ): ResponseEntity<ApiResource<OrderApiResponse>> {
        return ResponseEntity.ok(ApiResource.success(orderFacade.updateOrder(id, request.toDomainRequest())))
    }

    @DeleteMapping("/{id}")
    fun deleteOrder(
        @PathVariable id: Long,
    ): ResponseEntity<ApiResource<Unit>> {
        orderFacade.deleteOrder(id)
        return ResponseEntity.ok(ApiResource.success())
    }
}
```

---

## Search Endpoints

For 1-2 filter parameters, use `@RequestParam` directly. For 3 or more, encapsulate in a `{Feature}SearchApiRequest` with a `toSearchCondition()` method and bind with `@ModelAttribute`.

```kotlin
// Simple: 1-2 params
@GetMapping
fun getOrders(
    @RequestParam(required = false) status: String?,
    @RequestParam(required = false) userId: Long?,
    @PageableDefault(size = 100) pageable: Pageable,
): ResponseEntity<ApiResource<Page<OrderApiResponse>>> {
    return ResponseEntity.ok(ApiResource.ofPage(orderFacade.getOrders(status, userId, pageable)))
}

// Complex: 3+ params — use SearchApiRequest + @ModelAttribute
data class OrderSearchApiRequest(
    val status: String?,
    val userId: Long?,
    val productName: String?,
    val searchDates: SearchDates?,
) {
    fun toSearchCondition(): OrderSearchCondition =
        OrderSearchCondition(
            status = status,
            userId = userId,
            productName = productName,
            dateFrom = searchDates?.from,
            dateTo = searchDates?.to,
        )
}

@GetMapping
fun searchOrders(
    @ModelAttribute request: OrderSearchApiRequest,
    @PageableDefault(size = 100) pageable: Pageable,
): ResponseEntity<ApiResource<Page<OrderApiResponse>>> {
    return ResponseEntity.ok(ApiResource.ofPage(orderFacade.searchOrders(request.toSearchCondition(), pageable)))
}
```

### SearchDates

Use the `SearchDates` type for date range fields.

```kotlin
import {projectGroup}.common.search.SearchDates

SearchDates.of(from = LocalDate.of(2024, 1, 1), to = LocalDate.of(2024, 12, 31))
SearchDates.fromToday()
SearchDates.ofMonth(year = 2024, month = 1)
```

---

## Controller Structure

### Method Size Rule

Each controller method must be **7 lines or fewer**. Controllers handle HTTP routing only -- no business logic.

### Annotation Order

```kotlin
// Class level
@RestController
@RequestMapping("/api/v1/orders")
@Validated
class OrderController

// Method level
@GetMapping("/{id}")
@PreAuthorize("hasRole('USER')")
fun getOrder(...)

// Parameter level
@PathVariable id: Long
@Valid @RequestBody request: CreateOrderApiRequest
@PageableDefault(size = 100) pageable: Pageable
@RequestParam(required = false) status: String?
@ModelAttribute request: OrderSearchApiRequest
```

### Dependencies

**Standard: Inject Facade.** Controllers depend on Facade as the primary entry point.

```kotlin
class OrderController(private val orderFacade: OrderFacade)
```

**Exception: Application for simple pass-through.** When no orchestration is needed, injecting the Application service directly is acceptable.

```kotlin
class OrderStatusController(private val orderStatusApplication: OrderStatusApplication)
```

---

## DateTime Input/Output

### Input: UTC

All datetime inputs received from clients must be UTC. Never accept KST directly from the API layer.

```kotlin
// LocalDateTime (implicit UTC)
data class CreateOrderApiRequest(
    val scheduledAt: LocalDateTime,  // must be UTC
)

// ZonedDateTime — convert to UTC in toDomainRequest()
data class CreateOrderApiRequest(
    val scheduledAt: ZonedDateTime,
) {
    fun toDomainRequest(): CreateOrderRequest =
        CreateOrderRequest(
            scheduledAt = scheduledAt.withZoneSameInstant(ZoneOffset.UTC).toLocalDateTime(),
        )
}
```

### Output: KST at Response Boundary

Convert to KST only inside the response DTO or Facade, never inside the controller.

```kotlin
data class OrderApiResponse(
    val scheduledAtKst: LocalDateTime,
) {
    companion object {
        fun from(order: Order): OrderApiResponse =
            OrderApiResponse(scheduledAtKst = order.scheduledAt.toKst())
    }
}
```

### Incorrect Example

```kotlin
// Bad: KST conversion inside controller
@GetMapping("/{id}")
fun getOrder(@PathVariable id: Long): ResponseEntity<ApiResource<OrderApiResponse>> {
    val order = orderFacade.getOrder(id)
    return ResponseEntity.ok(ApiResource.success(
        OrderApiResponse(scheduledAtKst = order.scheduledAt.toKst())  // wrong place
    ))
}
```

---

## Common Pitfalls

| Pitfall | Wrong | Right |
|---------|-------|-------|
| Verb in URL | `POST /api/v1/createOrder` | `POST /api/v1/orders` |
| Singular resource name | `/api/v1/order/{id}` | `/api/v1/orders/{id}` |
| camelCase URL | `/api/v1/orderItems` | `/api/v1/order-items` |
| Trailing slash | `/api/v1/orders/` | `/api/v1/orders` |
| Business logic in controller | Inline calculation, DB access | Delegate to Facade |
| No `@Valid` on request body | `@RequestBody request: ...` | `@Valid @RequestBody request: ...` |
| Default pageable size | `pageable: Pageable` (size=20) | `@PageableDefault(size = 100) pageable: Pageable` |
| KST conversion in controller | `order.scheduledAt.toKst()` in controller | Convert in response DTO or Facade |
| Accepting KST input | `scheduledAt: LocalDateTime` (KST) | Always accept UTC, convert in DTO |
| Injecting Repository directly | `private val orderRepository: OrderRepository` | Inject Facade or Application |
| Deep nesting (4+ levels) | `/api/v1/users/{id}/orders/{id}/items/{id}/details` | Flatten to `/api/v1/order-items/{id}` |
| Using `in` for search params (3+) | `@RequestParam` x5 | `@ModelAttribute OrderSearchApiRequest` |
