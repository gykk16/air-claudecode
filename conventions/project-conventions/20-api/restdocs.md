# REST Docs

## Core Rules

- Extend **`RestDocsSupport`** base class
- Mock the **Facade** (not Service)
- Use **`DocsFieldType`**: `STRING`, `NUMBER`, `BOOLEAN`, `DATE`, `DATETIME`, `ENUM(Class::class)`
- Use **Field DSL**: `"fieldName" type TYPE means "description"`
- Optional fields: `isOptional true`; examples: `example "value"`

---

## RestDocsSupport Base Class

```kotlin
// test-support module
abstract class RestDocsSupport {
    protected lateinit var mockMvc: MockMvc

    @BeforeEach
    fun setUp() { /* standaloneSetup + documentationConfiguration */ }

    abstract fun initController(): Any
}

// Usage
class OrderDocsTest : RestDocsSupport() {
    private val orderFacade: OrderFacade = mockk()
    override fun initController(): Any = OrderController(orderFacade)

    @Test
    fun `get order by id`() {
        every { orderFacade.getOrder(any()) } returns OrderDto(id = 1L, ...)
        mockMvc.perform(get("/api/v1/orders/{id}", 1L))
            .andExpect(status().isOk)
            .andDo(document("get-order-by-id",
                pathParameters("id" means "주문 ID"),
                responseCommonFieldsSubsection(),
                dataResponseFields(
                    "id" type NUMBER means "주문 ID" example "1",
                    "status" type ENUM(OrderStatus::class) means "주문 상태",
                    "createdAt" type DATETIME means "생성일시",
                ),
            ))
    }
}
```

---

## Mock Facade (not Service)

Always mock the Facade -- the layer the Controller directly depends on. Mocking a Service that the Controller does not inject results in a null Facade and NPE at runtime.

```kotlin
// Good
private val orderFacade: OrderFacade = mockk()
override fun initController(): Any = OrderController(orderFacade)

// Bad -- orderFacade is null, NPE at runtime
private val orderService: OrderService = mockk()
override fun initController(): Any = OrderController(orderFacade)
```

---

## DocsFieldType Reference

| Type | Usage | Example value |
|------|-------|---------------|
| `STRING` | Text fields | `"항공권"` |
| `NUMBER` | Integer or decimal numbers | `1`, `9900` |
| `BOOLEAN` | True/false flags | `true` |
| `ARRAY` | JSON arrays | `[...]` |
| `OBJECT` | Nested JSON objects | `{...}` |
| `DATE` | Date only (`yyyy-MM-dd`) | `"2024-01-15"` |
| `DATETIME` | Date and time (`yyyy-MM-dd'T'HH:mm:ss`) | `"2024-01-15T10:00:00"` |
| `ENUM(Class::class)` | Enum with documented values | `OrderStatus::class` |

---

## Field DSL Syntax

```kotlin
"fieldName" type STRING means "필드 설명"
"fieldName" type STRING means "필드 설명" isOptional true
"fieldName" type NUMBER means "주문 ID" example "1"
"fieldName" type NUMBER means "페이지 번호" withDefaultValue "0"
"status" type ENUM(OrderStatus::class) means "주문 상태"
"desiredDate" type DATE means "희망 날짜" isOptional true example "2024-01-15"
```

---

## Response Strategy

| Response type | Method combination |
|--------------|-------------------|
| Single object | `responseCommonFieldsSubsection()` + `dataResponseFields(...)` |
| Array | `responseArrayCommonFieldsSubsection()` + `dataResponseFields(...)` |
| String (DELETE) | `responseStringCommonFields()` |
| Pagination | `responseCommonFieldsSubsection()` + `dataResponseFields(...)` + `pageRequestFormat()` + `pageCommonFormat()` |

For pagination, add `queryParameters(pageRequestFormat())` for request params and `pageCommonFormat()` after `dataResponseFields(...)` for page metadata.

---

## Test Method Naming

Test method names become the snippet directory name. Use descriptive English phrases -- no "should" prefix, no "test" prefix, no camelCase.

```kotlin
fun `get order by id`() { }            // -> get-order-by-id/
fun `list orders with pagination`() { } // -> list-orders-with-pagination/
```

---

## Korean Field Description Rule

All field descriptions (`means "..."`) **must be written in Korean**.

```kotlin
// Good
"id" type NUMBER means "주문 ID" example "1"
"status" type ENUM(OrderStatus::class) means "주문 상태"

// Bad
"id" type NUMBER means "Order ID"   // English not allowed
```

---

## Quick Reference

```kotlin
class {Feature}DocsTest : RestDocsSupport() {
    private val {feature}Facade: {Feature}Facade = mockk()
    override fun initController(): Any = {Feature}Controller({feature}Facade)

    @Test
    fun `{action} {feature}`() {
        every { {feature}Facade.{method}(any()) } returns {stub}
        mockMvc.perform(get("/api/v1/{features}/{id}", 1L))
            .andExpect(status().isOk)
            .andDo(document("{action}-{feature}",
                responseCommonFieldsSubsection(),
                dataResponseFields("id" type NUMBER means "ID" example "1"),
            ))
    }
}
```

---

## Build Commands

```bash
./gradlew clean :modules:docs:docs
./gradlew test --tests "{projectGroup}.docs.{Feature}DocsTest"
```
