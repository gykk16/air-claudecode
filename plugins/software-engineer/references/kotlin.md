# Kotlin Guidelines

Based on the official [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html).

## Class Layout

- Order: properties & init blocks → secondary constructors → methods → companion object → nested classes.
- Group related methods together (not alphabetically, not by visibility); keep interface member order; overloads next to each other.
- Data class property order: required → optional with defaults → timestamps.
- Sealed class member order: success first → errors → states → common operations.

## Immutability & Null Safety

- `val` over `var`; immutable collections (`List`, `Map`) over mutable ones.
- `data class` for DTOs; `copy()` over mutation; sealed classes/interfaces for restricted hierarchies.
- Never use `!!` — use `?.`, `?:`, or `requireNotNull()` with a message.
- Nullable types for expected absence; exceptions for unexpected errors.

## Idioms

- Expression body for single-expression functions; `when` for 3+ branches.
- Default parameters over overloads; named arguments for multi-arg calls.
- String templates over concatenation.
- Higher-order functions over manual loops; `asSequence()` for large collections.
- Guard clauses / early returns over deep nesting.
- Prefer coroutines over threads; keep suspending functions main-safe.
- Extension functions to extend types you don't own — no utility classes.

## Scope Functions

Use sparingly and idiomatically — never nest them.

| Function | Use case |
| --- | --- |
| `let` | null check + transform |
| `apply` | object configuration |
| `also` | side effects (logging) |

## Formatting

- 4-space indent; trailing commas; chained calls on the next line.
- Omit `: Unit`, semicolons, and redundant `public`.
- Packages: lowercase, no underscores.
- Acronyms: 2 letters uppercase (`IO`), longer capitalize first only (`Xml`).

## Anti-Patterns

- Over-engineering — interface + impl + factory for a one-line function
- God classes — split by responsibility
- Copy-paste — extract to an extension function or interface
- Over-functional chains — break complex chains into clear named steps
- Nested scope functions — restructure instead
