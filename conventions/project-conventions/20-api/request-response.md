# Request & Response Conventions

## Never Return Entities

Never return JPA entities as API responses -- always convert to a response DTO. Conversion flow: `Entity → {Feature}Info (domain) → {Feature}Dto (API response)`.

```kotlin
// Bad: exposes JPA entity directly
fun getOrder(@PathVariable id: Long): Order = orderFacade.getOrderEntity(id)

// Good: entity -> domain DTO -> API response DTO
fun getOrder(@PathVariable id: Long): ResponseEntity<ApiResource<OrderDto>> =
    ResponseEntity.ok(ApiResource.success(orderFacade.getOrder(id)))
```

---

## DTO Package Structure

```
{appname}/
├── api/
│   └── OrderController.kt
├── facade/
│   └── OrderFacade.kt
├── dto/
│   ├── request/
│   │   ├── CreateOrderApiRequest.kt
│   │   └── UpdateOrderApiRequest.kt
│   └── response/
│       └── OrderDto.kt
└── config/
    └── ...
```

- Separate into `dto/request/` and `dto/response/` packages
- Do NOT mix request/response DTOs in the same file
- Do NOT place DTOs inside the `api/` package

---

## Naming Convention

| Type | Naming | Package |
|------|--------|---------|
| API Request | `{Action}{Feature}ApiRequest` | `dto/request/` |
| API Response | `{Feature}Dto` | `dto/response/` |
| Domain DTO | `{Feature}Info` | domain `dto/` |
| Domain Request | `Create{Feature}Request` | domain `dto/` |

---

## DTO Examples

```kotlin
// Request DTO
data class CreateOrderApiRequest(
    @NotBlank val itemName: String,
    @Min(1) val quantity: Int,
    @param:JsonFormat(pattern = "yyyy-MM-dd") val desiredDate: LocalDate,
) {
    fun toDomainRequest(): CreateOrderRequest = CreateOrderRequest(itemName, quantity, desiredDate)
}

// Response DTO
data class OrderDto(
    val id: Long,
    val itemName: String,
    val status: String,
    @get:JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss") val createdAt: LocalDateTime,
) {
    companion object {
        fun from(info: OrderInfo): OrderDto = OrderDto(info.id, info.itemName, info.status.code, info.createdAt)
    }
}
```

---

## JsonFormat Use-Site Targets

| Target | Direction | Use case |
|--------|-----------|----------|
| `@param:JsonFormat` | Request (deserialization) | Constructor parameters |
| `@get:JsonFormat` | Response (serialization) | Getter formatting |
| `@field:JsonFormat` | Both directions | Field-level for both |

Using `@param` on response or `@get` on request **will not work**.

```kotlin
// Request -- @param:
@param:JsonFormat(pattern = "yyyy-MM-dd") val desiredDate: LocalDate

// Response -- @get:
@get:JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss") val createdAt: LocalDateTime

// Both directions -- @field:
@field:JsonFormat(pattern = "yyyy-MM-dd") val startDate: LocalDate

// Bad: missing use-site target -- ambiguous in Kotlin, may not work
@JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss") val createdAt: LocalDateTime
```
