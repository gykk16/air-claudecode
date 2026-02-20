# Clean Code Reference

> Code is read far more than written. Optimize for the reader.

## Principles

| Principle | Rule |
|-----------|------|
| Readability | Names reveal intent; self-documenting code |
| Abstraction | Each function at a single level; don't over-extract simple logic |
| KISS | Simplest solution that works |
| DRY | Extract repeated logic |
| YAGNI | Only what's currently required |

## Abstraction Levels

```
// Bad -- mixed levels
fun processOrder(order) {
    validateOrder(order)          // high
    conn = getConnection()        // low
    stmt = prepareStatement(...)  // low
    sendConfirmationEmail(order)  // high
}

// Good
fun processOrder(order) {
    validateOrder(order)
    saveOrder(order)
    sendConfirmationEmail(order)
}
```

Extract when a block has a distinct purpose. Keep simple logic inline -- 5 lines don't need 4 methods.

## Naming

| Type | Convention | Example |
|------|------------|---------|
| Classes | PascalCase | `UserService` |
| Functions | camelCase (verbs) | `findUserById()` |
| Constants | SCREAMING_SNAKE | `MAX_RETRY_COUNT` |
| Booleans | question form | `isValid`, `hasPermission` |

## Do NOT

- Interfaces for single implementations
- Abstractions for hypothetical future needs
- Comments that explain WHAT -- only explain WHY
- Unused code -- delete it
