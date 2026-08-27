# Spring Guidelines

> For annotation ordering rules (Spring/JPA/Lombok), see `annotation-order.md`.

## Dependency Injection

- Constructor injection only — no `@Autowired` field injection.
- `final` (`val`) on all injected fields.
- Single constructor needs no `@Autowired`.

## Layer Separation

| Layer | Responsibility |
| --- | --- |
| Controller | HTTP routing only — parse request, call Facade, return response |
| Facade | Orchestration across services; I/O around transactions |
| Service | Business logic, transaction management |
| Repository | Data access only |

- No business logic in controllers; never access repositories from controllers.
- Never leak JPA entities to controllers or API responses — use DTOs.

## Controller Design

### URL design

- All paths start with `/api/v1/`.
- **kebab-case** for all URL segments; **plural nouns** for resources (`/users`, `/orders`).
- Nouns, not verbs; max 3 levels of nesting.
- Non-CRUD actions as sub-paths: `POST /api/v1/orders/{id}/cancel`.

### Response format

- All controllers return `ResponseEntity<ApiResource<T>>`.
- `ApiResource.success(data)` for single objects; `ApiResource.ofPage(page)` for paginated results; `ApiResource.success()` for DELETE/void.
- Default pageable: `Pageable.ofSize(100)`.

### Structure

- **7 lines or fewer** per method — controllers handle HTTP routing only.
- Inject **Facade only** (or Application for trivially simple pass-through cases).
- `@Valid @RequestBody` for request DTOs; `@Validated` on the class when using constraint annotations on parameters.
- Conversion logic lives in the request DTO's `toDomainRequest()`.

### Search endpoints

- 1–2 filters: `@RequestParam` directly.
- 3+ filters: encapsulate in a `{Feature}SearchCondition` object.
- Use `LocalDateRange` for date range fields.

## Transactions

- `@Transactional` on service methods only — not on repositories, controllers, or private methods.
- Self-invocation bypasses the proxy — call `@Transactional` methods from another bean (e.g., Facade), never from within the same class.
- Read-only queries: `@Transactional(readOnly = true)`.
- Keep transactions short — only DB operations inside.
- **No I/O inside transactions**: no HTTP calls, file I/O, or message publishing. Do I/O in the Facade, before or after the transaction.

## Exception Handling

- Domain exceptions are unchecked (`RuntimeException` subclasses) with contextual messages: `UserNotFoundException(id)`.
- Handle globally in `@RestControllerAdvice`; map each exception to an appropriate HTTP status.
- Handle specific exception types only — never generic `Exception`.

## Configuration

- `@ConfigurationProperties` over `@Value` for grouped config.
- Externalize all environment-specific values.

## Anti-Patterns

- `@Autowired` field injection — use constructor injection
- Business logic in controllers — move to Facade/Service
- JPA entities in API responses — use DTOs
- `@Transactional` on private methods or self-invoked methods — won't work (proxy-based AOP)
- Catching generic `Exception` in `@ExceptionHandler` — use specific types
