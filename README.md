# air-claudecode

Lightweight skill-sharing plugin for Claude Code teams. Zero dependencies, zero config.

Add this repository as a marketplace to install its plugins.

## Plugins

None yet.

## Installation

```bash
/plugin marketplace add <org>/air-claudecode
/plugin install <plugin-name>@air-claudecode
```

## Development

Each plugin lives under `plugins/<plugin-name>/`:

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json        # manifest only — nothing else goes here
└── skills/                # components live at the plugin root
    └── <skill-name>/
        └── SKILL.md
```

To add a new plugin:

1. Create `plugins/<plugin-name>/.claude-plugin/plugin.json` (`name` must be kebab-case)
2. Add components (`skills/`, `agents/`, `hooks/`, ...) at the plugin root
3. Register the plugin in `.claude-plugin/marketplace.json`
4. Validate with `claude plugin validate .`

To test locally:

```bash
claude --plugin-dir ./plugins/<plugin-name>
```

After editing a skill mid-session, reload with `/reload-plugins`.

## References

- [Plugins overview](https://code.claude.com/docs/en/plugins.md)
- [Plugins reference](https://code.claude.com/docs/en/plugins-reference.md)
- [Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)
- [Official examples](https://github.com/anthropics/claude-code/tree/main/plugins)
