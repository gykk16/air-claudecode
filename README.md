# air-claudecode

Lightweight plugin marketplace for Claude Code teams — engineering workflow,
technical writing, and SQL. Zero dependencies, zero config.

Add this repository as a marketplace to install its plugins.

## Plugins

| Plugin | Commands | Description |
| --- | --- | --- |
| `software-engineer` | `develop`, `write-tests`, `review`, `super-engineer` | Engineering workflow for Kotlin, Java, and Spring — implementation, test generation, and code review agents |
| `technical-writer` | `write`, `review`, `polish` | Technical documentation writing, review, and sentence polishing based on the Toss technical writing guide |
| `sql-engineer` | `generate` | Vendor-aware SQL generation (DDL/DML) with strict formatting, naming, and policy rules |

Commands are invoked as `/<plugin>:<command>`, e.g. `/sql-engineer:generate`.

The `software-engineer` plugin runs each phase individually, or the whole
quality-gated pipeline (develop → test → review → fix until approved) at once:

```
# individual phases
/software-engineer:develop <task>
/software-engineer:write-tests <target>
/software-engineer:review

# full pipeline
/software-engineer:super-engineer <task>
```

## Installation

Add the marketplace once, then install the plugins you need:

```bash
# 1. Add the marketplace
/plugin marketplace add gykk16/air-claudecode

# or from a local clone
/plugin marketplace add /path/to/air-claudecode

# 2. Install plugins
/plugin install software-engineer@air-claudecode
/plugin install technical-writer@air-claudecode
/plugin install sql-engineer@air-claudecode
```

Check what's installed with `/plugin list`, and toggle plugins with
`/plugin enable|disable <plugin-name>@air-claudecode`.

## Update

```bash
# Refresh the marketplace catalog to the latest commit
/plugin marketplace update air-claudecode
```

Installed plugins follow the refreshed catalog. Auto-update is disabled by
default for custom marketplaces — to turn it on, open `/plugin`, go to the
Marketplaces tab, select `air-claudecode`, and enable auto-update.

## Uninstall

```bash
/plugin uninstall <plugin-name>@air-claudecode
/plugin marketplace remove air-claudecode
```

## Contributing

To add a new plugin, follow [docs/plugin-guide.md](docs/plugin-guide.md) and
the standards in [docs/design-criteria.md](docs/design-criteria.md).

## References

- [Plugins overview](https://code.claude.com/docs/en/plugins.md)
- [Plugins reference](https://code.claude.com/docs/en/plugins-reference.md)
- [Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)
- [Official examples](https://github.com/anthropics/claude-code/tree/main/plugins)
