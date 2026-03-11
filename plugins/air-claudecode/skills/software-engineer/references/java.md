# Java Reference

Based on [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html) + modern Java (17+).

**Exceptions**: 4-space indent, 120-char line break, Kotlin-style parameter wrapping.

## Class Layout

1. Static fields → 2. Instance fields → 3. Constructors → 4. Public methods → 5. Private methods → 6. Inner classes

- Group related methods, keep interface member order, overloads next to each other

```java
@Service
public class OrderService {
    private static final int MAX_CACHE = 100;
    private final OrderRepository orderRepository;

    public OrderService(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    public Order createOrder(CreateOrderRequest request) { }
    private void validate(CreateOrderRequest request) { }

    public Optional<Order> findOrder(Long id) { }
}
```

## Records & Sealed Classes

```java
// Record for DTOs (Java 16+)
public record User(Long id, String email, String name, Role role) { }

// Sealed interface (Java 17+)
public sealed interface Result<T> permits Success, Error {
    record Success<T>(T data) implements Result<T> { }
    record Error<T>(String message) implements Result<T> { }
}
```

## Type Rules

- Prefer primitive types (`int`, `long`, `boolean`) by default
- Use wrapper types (`Integer`, `Long`) only when nullable or required by generics (`List<Long>`, `Optional<Integer>`)

## Immutability & Null Handling

```java
private final UserRepository userRepository;           // final fields
List<User> users = List.of(user1, user2);              // unmodifiable collections

Optional<User> findById(Long id);                      // Optional for return types
String name = findById(id).map(User::name).orElse("Unknown");
// Never return null from collections -- return List.of()
```

## Modern Idioms

```java
var users = userRepository.findAll();                   // var (10+)
if (obj instanceof String s) { s.length(); }           // pattern matching (16+)
String label = switch (status) {                        // switch expression (14+)
    case ACTIVE -> "Active";
    case PENDING -> "Pending";
};
List<String> names = users.stream()                     // Stream API
    .filter(User::isActive).map(User::name).sorted().toList();
```

## Formatting

```java
// >120 chars: Kotlin-style wrapping
public OrderService(
    OrderRepository orderRepository, PaymentService paymentService, NotificationService notificationService
) {
    this.orderRepository = orderRepository;
}

// Ternary: operator-first wrapping
String message = isVipUser(user)
    ? buildVipWelcomeMessage(user, promotions)
    : buildStandardWelcomeMessage(user);
```

- One class per file, no wildcard imports, annotations on separate lines

## Early Returns

```java
if (user == null) return;
if (!user.isActive()) return;
if (!user.hasPermission("admin")) return;
// main logic -- no deep nesting
```

## Error Handling

```java
Optional<User> findUser(Long id);                      // expected absence
throw new UserNotFoundException(id);                    // domain exception (unchecked)
// Specific catch only -- NEVER catch (Exception e)
```

## Anti-Patterns

- **Optional as field/parameter**: only for return types
- **Mutable DTOs with setters**: use records or immutable classes
