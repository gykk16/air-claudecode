# Git Workflow

## Branch Structure ([Git Flow](https://git-flow.sh/workflows/gitflow/))

| Branch | Base | Merges Into | Purpose | Example |
|--------|------|-------------|---------|---------|
| `main` | - | - | Production-ready code | - |
| `develop` | `main` | - | Integration branch | - |
| `feature/*` | `develop` | `develop` | New features | `feature/PROJ-123-add-login` |
| `release/*` | `develop` | `main` + `develop` | Release preparation | `release/1.2.0` |
| `hotfix/*` | `main` | `main` + `develop` | Critical production fixes | `hotfix/PROJ-456-fix-null-pointer` |
| `support/*` | `main` | - | Long-term support | `support/1.0.x` |

**Naming:** `{type}/{description}` — lowercase, hyphens between words, include Jira ticket ID when applicable.

## Conventional Commits

Format: `{type}({scope}): {description}`

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code refactoring |
| `test` | Add or fix tests |
| `docs` | Documentation |
| `chore` | Build, CI, tooling |
| `style` | Formatting, whitespace |
| `perf` | Performance improvement |
| `build` | Build system or dependencies |
| `ci` | CI configuration changes |

**Rules:** Imperative mood (`add`, `fix`, `update`). No capital letter after type/scope. No trailing period. Subject under 72 chars. Body explains what and why, not how.

**Example:**
```
feat(auth): add OAuth2 login with Google

Allow users to sign in using their Google account.
Reduces friction in onboarding.

Refs: PROJ-123
```

## Merge Strategy

| Action | Strategy |
|--------|----------|
| Feature → develop | **Squash and merge** (clean history, one commit per feature) |
| Release → main | **Merge commit** (preserve release history) |
| Hotfix → main + develop | **Merge commit** (preserve fix history) |
| Update feature from develop | **Rebase** (keep linear) |

## Workflow Summary

| Scenario | Branch From | PR Strategy | Tag After Merge |
|----------|-------------|-------------|-----------------|
| Feature | `develop` | Squash and merge to `develop` | No |
| Release | `develop` | Merge commit to `main` + `develop` | `v{major}.{minor}.{patch}` |
| Hotfix | `main` | Merge commit to `main` + `develop` | `v{major}.{minor}.{patch}` |

**General Steps:** Create branch → make commits → open PR → merge → delete branch → tag (for releases/hotfixes).

## Tag Convention

Format: `v{major}.{minor}.{patch}`

| Segment | When to increment |
|---------|------------------|
| Major | Breaking changes or incompatible API changes |
| Minor | New backward-compatible features |
| Patch | Backward-compatible bug fixes |

Examples: `v1.0.0`, `v1.2.3`, `v2.0.0`

## Protected Branches

- `main` / `develop`: PR only, no force push, no delete
- `feature/*` / `hotfix/*`: direct push allowed, delete after merge
