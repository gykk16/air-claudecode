# air-claudecode

Shared team skills and agent prompts for Claude Code.

## Skills

Use `/air-claudecode:<skill-name>` to invoke:

- `setup` -- Verify installation and check prerequisites (gh CLI, Atlassian MCP)
- `git-commit` -- Conventional commit with Jira/GitHub issue linking
- `git-branch` -- Create branch from Jira ticket or manual description
- `git-pr-master` -- GitHub PR CRUD with reviewer/label/milestone suggestions
- `git-issue-master` -- GitHub issue CRUD with label/milestone/assignee suggestions
- `jira-master` -- Jira ticket CRUD with interactive project/type/priority selection
- `code-review` -- Comprehensive code review with severity-rated feedback in Korean

## Agents

- **jira-master** (sonnet): Jira ticket management via Atlassian MCP
- **git-issue-master** (sonnet): GitHub issue management with Jira linking
- **git-pr-master** (sonnet): GitHub PR management with Jira linking
- **code-reviewer** (opus): Comprehensive code review with severity-rated Korean output
