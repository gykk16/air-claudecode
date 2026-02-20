# Annotation Order Reference

> Spring/JPA first, Lombok last. Core before config.

## Class-level

| Layer | Order |
|-------|-------|
| Entity | `@Entity` → `@Table` → `@Builder` → `@AllArgsConstructor` → `@NoArgsConstructor(access = PROTECTED)` → `@Getter` |
| Controller | `@RestController` → `@RequestMapping` → `@RequiredArgsConstructor` |
| Service | `@Service` → `@Transactional(readOnly = true)` → `@RequiredArgsConstructor` |
| Configuration | `@Configuration` → `@Enable*` → `@RequiredArgsConstructor` |
| DTO | `@Builder` → `@AllArgsConstructor` → `@Getter` → `@ToString` |

> Avoid `@ToString`, `@EqualsAndHashCode` on entities -- LazyInitializationException risk.

## Field-level

| Type | Order |
|------|-------|
| ID | `@Id` → `@GeneratedValue(strategy = IDENTITY)` |
| Column | `@Column(nullable = false)` → `@NotBlank` |
| Enum | `@Enumerated(EnumType.STRING)` → `@Column(length = 20)` |
| Relationship | `@ManyToOne(fetch = LAZY)` → `@JoinColumn(name = "user_id")` |
| Audit | `@CreatedDate` → `@Column(updatable = false)` |

## Method-level

| Layer | Order |
|-------|-------|
| Controller | `@GetMapping` → `@PreAuthorize` → `@Cacheable` |
| Service | `@Transactional` → `@CacheEvict` |
| Repository | `@Query` → `@Lock` → `@EntityGraph` |
| Event | `@Async` → `@TransactionalEventListener(phase = AFTER_COMMIT)` |

## Parameter-level

| Type | Order |
|------|-------|
| Request body | `@Valid` → `@RequestBody` |
| Validation | `@field:NotBlank` → `@field:Size(max = 100)` |

## Lombok Order

| Order | Annotation |
|-------|------------|
| 1st | `@Builder` |
| 2nd | `@NoArgsConstructor`, `@AllArgsConstructor`, `@RequiredArgsConstructor` |
| 3rd | `@Getter`, `@Setter` |
| 4th | `@ToString` |
| 5th | `@EqualsAndHashCode` |
