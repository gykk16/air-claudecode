# Concurrency & Coroutines

> Always use the project's `CoroutineUtils` for coroutine operations. Never use raw `runBlocking`, `async`, or `launch`.

## MDC Context Propagation (required)

Use MDC-preserving functions from `{projectGroup}.common.utils.coroutine`:

| Function | Purpose | Returns |
|----------|---------|---------|
| `runBlockingWithMDC` | Bridge blocking code to coroutines with MDC | `T` (blocking) |
| `asyncWithMDC` | Launch concurrent coroutine with MDC | `Deferred<T>` |
| `launchWithMDC` | Fire-and-forget coroutine with MDC | `Job` |

```kotlin
import {projectGroup}.common.utils.coroutine.runBlockingWithMDC
import {projectGroup}.common.utils.coroutine.asyncWithMDC
import {projectGroup}.common.utils.coroutine.launchWithMDC

// Parallel execution with MDC preserved
fun fetchUserDashboard(userId: Long): DashboardInfo = runBlockingWithMDC {
    val user = asyncWithMDC { userClient.fetchUser(userId) }
    val orders = asyncWithMDC { orderClient.fetchOrders(userId) }
    DashboardInfo(user.await(), orders.await())
}

// Fire-and-forget with MDC preserved
fun processOrder(order: Order): Unit = runBlockingWithMDC {
    launchWithMDC { notificationService.sendConfirmation(order) }
    launchWithMDC { auditService.logOrderCreated(order) }
}
```

Raw `runBlocking`/`async`/`launch` drop MDC context (traceId, requestId) -- always use the MDC-preserving wrappers.

---

## Dispatcher Selection

Choose the right dispatcher based on the workload type.

| Dispatcher | Functions | Use Case |
|------------|-----------|----------|
| **Default** (CPU) | `runBlockingWithMDC`, `asyncWithMDC`, `launchWithMDC` | CPU-bound computation |
| **Virtual Thread** (preferred for I/O) | `runBlockingOnVirtualThread`, `asyncOnVirtualThread`, `launchOnVirtualThread` | Blocking I/O (preferred) |
| **IO** (fallback) | `runBlockingOnIoThread`, `asyncOnIoThread`, `launchOnIoThread` | Blocking I/O (fallback) |

### Selection guide

| Workload | Dispatcher | Example |
|----------|------------|---------|
| CPU computation | Default | Data transformation, calculation |
| HTTP/API calls | Virtual Thread | REST client calls, gRPC |
| File I/O | IO or Virtual Thread | File read/write, stream processing |
| Database queries | Virtual Thread | JDBC calls outside JPA transaction |
| Mixed workload | Virtual Thread | Combined I/O operations |

Prefer Virtual Thread functions over IO Dispatcher for blocking I/O -- virtual threads handle blocking calls more efficiently, with lower overhead.

```kotlin
import {projectGroup}.common.utils.coroutine.runBlockingOnVirtualThread

fun fetchExternalData(): AggregatedData = runBlockingOnVirtualThread {
    val flights = asyncWithMDC { flightClient.search(criteria) }
    val hotels = asyncWithMDC { hotelClient.search(criteria) }
    AggregatedData(flights.await(), hotels.await())
}
```

Pass a custom dispatcher to `runBlockingWithMDC(myCustomDispatcher) { ... }` when needed.

---

## Retry Pattern

Use the project's `retry` and `retryBlocking` functions. Do not implement custom retry logic.

```kotlin
import {projectGroup}.common.utils.coroutine.retry
import {projectGroup}.common.utils.coroutine.retryBlocking

// Default: 3 attempts, 500ms delay, no backoff
val result = retry { externalApi.call() }

// Custom: exponential backoff, selective exception matching
val result = retry(
    maxAttempts = 5,
    delay = 100.milliseconds,
    backoffMultiplier = 2.0,
    retryOn = { it is IOException || it is TimeoutException },
) { externalApi.call() }

// Blocking version
val result = retryBlocking(maxAttempts = 3) { externalApi.call() }
```

### Retry parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `maxAttempts` | `3` | Total number of attempts (must be >= 1) |
| `delay` | `500ms` | Initial delay between retries |
| `backoffMultiplier` | `1.0` | Multiplier for exponential backoff (1.0 = fixed delay) |
| `retryOn` | All exceptions | Predicate to filter retryable exceptions |

---

## Debug Logging

```kotlin
import {projectGroup}.common.utils.coroutine.withLogging

suspend fun fetchUserData(userId: Long): UserData = withLogging("fetchUserData") {
    val user = asyncWithMDC { userClient.fetch(userId) }
    val orders = asyncWithMDC { orderClient.fetchByUser(userId) }
    UserData(user.await(), orders.await())
}
// Logs: # >>> fetchUserData, start thread: 42
// Logs: # <<< fetchUserData, end thread: 43
```

> Use `withLogging` only for debugging. Remove or guard with log-level checks in production-critical paths.

---

## Structured Concurrency

Never launch coroutines in `GlobalScope` or unstructured scopes. Always bind child coroutines to a parent scope.

```kotlin
// Bad: GlobalScope -- coroutine leaks if parent fails
fun process(): Unit { GlobalScope.launch { sendNotification() } }

// Good: Structured -- child cancels with parent
fun process(): Unit = runBlockingWithMDC { launchWithMDC { sendNotification() } }
```

Respect cancellation in long-running loops with `ensureActive()`. Use `supervisorScope` to prevent one failure from cancelling sibling coroutines. Rethrow `CancellationException` -- never swallow it.

---

## Integration with Spring

Use coroutines in the Service layer for parallel I/O. Keep the Application layer as the transaction boundary.

```kotlin
@Service
class ProductService(
    private val inventoryClient: InventoryClient,
    private val pricingClient: PricingClient,
) {
    fun enrichProducts(products: List<Product>): List<EnrichedProduct> =
        runBlockingOnVirtualThread {
            products.map { product ->
                asyncWithMDC {
                    val inventory = inventoryClient.getStock(product.id)
                    val pricing = pricingClient.getPrice(product.id)
                    EnrichedProduct(product, inventory, pricing)
                }
            }.awaitAll()
        }
}
```

Do not start coroutines that perform database operations outside the transaction boundary. JPA operations must remain within the `@Transactional` scope that the Application layer manages -- parallel coroutines lose transaction context.
