# Java Guidelines

Based on the [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html) + modern Java (17+).
**Exceptions to Google style**: 4-space indent, 120-char line limit, Kotlin-style parameter wrapping.

## Class Layout

- Order: static fields → instance fields → constructors → public methods → private methods → inner classes.
- Group related methods; keep interface member order; overloads next to each other.

## Types & Data

- `record` for DTOs; `sealed` interfaces for restricted hierarchies.
- Primitives (`int`, `long`, `boolean`) by default; wrappers only when nullable or required by generics (`List<Long>`, `Optional<Integer>`).

## Immutability & Null Handling

- `final` fields; unmodifiable collections (`List.of()`).
- `Optional<T>` for return types only — never as a field or parameter.
- Never return `null` from collection-returning methods — return `List.of()`.

## Modern Idioms

- `var` when the type is obvious from the right-hand side.
- Pattern matching for `instanceof`; switch expressions over switch statements.
- Stream API with `.toList()` over manual loops; method references where they read naturally.
- Guard clauses / early returns over deep nesting.

## Formatting

- Lines over 120 chars: Kotlin-style wrapping — parameters on the next line, closing parenthesis on its own line.
- Ternary wrapping: operator-first (`?` and `:` start the line).
- One class per file; no wildcard imports; annotations on separate lines.

## Error Handling

- `Optional` for expected absence; unchecked domain exceptions (`UserNotFoundException`) for unexpected errors.
- Catch specific exception types only — never `catch (Exception e)`.

## Concurrency

- Never create raw `Thread` instances — use `ExecutorService` or virtual threads.
- Virtual threads (21+) for I/O-bound tasks; fixed platform pools sized to cores for CPU-bound work.
- Prefer immutable objects over shared mutable state; when unavoidable, use `java.util.concurrent` types (`ConcurrentHashMap`, `AtomicLong`, `computeIfAbsent`) over manual `synchronized`.
- Always set timeouts on blocking calls — never wait indefinitely.

## Anti-Patterns

- `Optional` as field or parameter — return types only
- Mutable DTOs with setters — use records or immutable classes
- `null` returns from collections — return empty collections
- `catch (Exception e)` — catch specific types
