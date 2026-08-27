# Test Rules

Templates and structure rules — code blocks here are copy-ready formats.
Write tests in the same language as the production code.

## Test Format

Kotlin:

```kotlin
@Test
fun `should return user when valid id is provided`(): Unit {
    // given
    val userId = 1L
    val expectedUser = User(id = userId, name = "John")

    // when
    val result = userService.findById(userId)

    // then
    assertThat(result).isNotNull
    assertThat(result.name).isEqualTo("John")
}
```

Java:

```java
@Test
@DisplayName("should return user when valid id is provided")
void findById_validId_returnsUser() {
    // given
    Long userId = 1L;
    User expectedUser = new User(userId, "John");

    // when
    User result = userService.findById(userId);

    // then
    assertThat(result).isNotNull();
    assertThat(result.name()).isEqualTo("John");
}
```

| Element | Kotlin | Java |
| --- | --- | --- |
| Method name | Backticks, descriptive sentence | camelCase `method_condition_expectedResult` |
| Display name | (method name is the sentence) | `@DisplayName` sentence |
| Return type | Explicit `: Unit` | `void` |
| Structure | given-when-then with comments, blank lines between sections | same |

## Naming

- Pattern: `should [expected behavior] when [condition]`
- Alternative: `[method] - [scenario] - [expected result]`

## Parameterized Tests

Same annotations in both languages (`@ParameterizedTest`, `@CsvSource`, `@MethodSource`).

```kotlin
@ParameterizedTest
@CsvSource(
    "user@example.com, true",
    "invalid, false",
    "'', false",
)
fun `should validate email format`(email: String, expected: Boolean): Unit {
    // given
    val validator = EmailValidator()

    // when
    val result = validator.isValid(email)

    // then
    assertThat(result).isEqualTo(expected)
}
```

Kotest data-driven (Kotlin only):

```kotlin
context("email validation") {
    withData(
        "user@example.com" to true,
        "invalid" to false,
    ) { (email, expected) ->
        EmailValidator().isValid(email) shouldBe expected
    }
}
```

## Test Organization

`@Nested` + `@DisplayName` in both languages (Kotlin: `inner class`, Java: non-static inner `class`).

```kotlin
@Nested
@DisplayName("UserService.create")
inner class CreateTests {

    @Test
    fun `should create user with valid input`(): Unit { }

    @Test
    fun `should throw exception when email is duplicate`(): Unit { }

    @Nested
    @DisplayName("when user is admin")
    inner class WhenAdmin {
        @Test
        fun `should assign admin role`(): Unit { }
    }
}
```

## Quality Checklist

| DO | DO NOT |
| --- | --- |
| Test business logic and behavior | Test trivial getters/setters |
| Test edge cases and boundaries | Write tests solely for coverage |
| Test error handling paths | Test framework behavior |
| Verify complex state transitions | Over-mock dependencies |
| Group related scenarios | Copy-paste test boilerplate |
