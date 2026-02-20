# Spring Reference

## Dependency Injection

- Constructor injection only -- no `@Autowired` field injection
- `final` on all injected fields
- Single constructor = `@Autowired` not needed

```kotlin
// Kotlin
@Service
class UserService(
    private val userRepository: UserRepository,
    private val emailService: EmailService,
)
```

```java
// Java
@Service
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;

    public UserService(UserRepository userRepository, EmailService emailService) {
        this.userRepository = userRepository;
        this.emailService = emailService;
    }
}
```

## Layer Separation

| Layer | Responsibility | Annotation |
|-------|----------------|------------|
| Controller | HTTP handling, request/response mapping | `@RestController` |
| Service | Business logic, transaction management | `@Service` |
| Repository | Data access only | `@Repository` |

- Do NOT put business logic in controllers
- Do NOT access repositories directly from controllers
- Do NOT leak JPA entities to controllers -- use DTOs

## Exception Handling

```kotlin
// Custom exception
class UserNotFoundException(id: Long) :
    RuntimeException("User not found: $id")

// Global handler
@RestControllerAdvice
class GlobalExceptionHandler {
    @ExceptionHandler(UserNotFoundException::class)
    fun handleNotFound(ex: UserNotFoundException): ResponseEntity<ErrorResponse> =
        ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(ErrorResponse(ex.message))
}
```

## Transaction

- `@Transactional` on service methods, not on repositories or controllers
- Read-only queries: `@Transactional(readOnly = true)`
- Keep transactions short -- only DB operations inside
- **No I/O inside transactions**: no HTTP calls, no file I/O, no message queue publishing
- Do I/O before or after the transaction, not during

```kotlin
@Service
class OrderService(private val orderRepository: OrderRepository) {

    @Transactional
    fun createOrder(request: CreateOrderRequest): Order { }

    @Transactional(readOnly = true)
    fun findOrder(id: Long): Order? { }
}
```

## REST API Conventions

```kotlin
@RestController
@RequestMapping("/api/v1/users")
class UserController(private val userService: UserService) {

    @GetMapping("/{id}")
    fun getUser(@PathVariable id: Long): UserResponse { }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    fun createUser(@Valid @RequestBody request: CreateUserRequest): UserResponse { }

    @PutMapping("/{id}")
    fun updateUser(@PathVariable id: Long, @Valid @RequestBody request: UpdateUserRequest): UserResponse { }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    fun deleteUser(@PathVariable id: Long) { }
}
```

- Use plural nouns for resource paths (`/users`, `/orders`)
- Return appropriate HTTP status codes
- `@Valid` on request bodies for validation
- Controller methods only: parse request → call service → return response

## Configuration

- Use `@ConfigurationProperties` over `@Value` for grouped config
- Externalize all environment-specific values

```kotlin
@ConfigurationProperties(prefix = "app.payment")
data class PaymentProperties(
    val apiUrl: String,
    val timeout: Duration = Duration.ofSeconds(30),
    val maxRetries: Int = 3,
)
```

## Anti-Patterns

- `@Autowired` field injection -- use constructor injection
- Business logic in controllers -- move to service layer
- JPA entities in API responses -- use DTOs
- `@Transactional` on private methods -- won't work (proxy-based AOP)
- Catching generic `Exception` in `@ExceptionHandler` -- use specific types
