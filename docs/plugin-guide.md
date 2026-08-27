# Creating a New Plugin

This guide walks through adding a new plugin to this marketplace, from
directory scaffold to validation. For decisions on how to structure the
plugin (agent vs skill, fork vs inline), see [design-criteria.md](design-criteria.md).

## 1. Scaffold the plugin

Create the plugin directory under `plugins/`:

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json        # manifest only — nothing else goes in this directory
├── agents/                # subagent definitions (if the plugin delegates work)
│   └── <agent-name>.md
├── references/            # on-demand knowledge read by agents
│   └── <topic>.md
└── skills/
    └── <skill-name>/
        ├── SKILL.md
        └── references/    # on-demand knowledge for inline (non-fork) skills
```

Component directories (`agents/`, `skills/`, `references/`) live at the plugin
root. Only `plugin.json` goes inside `.claude-plugin/`.

## 2. Write the manifest

`.claude-plugin/plugin.json`:

```json
{
  "name": "<plugin-name>",
  "version": "0.1.0",
  "description": "<what it does, one sentence>",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "license": "MIT",
  "keywords": ["..."]
}
```

- `name` must be kebab-case and unique in the marketplace.
- Use `MIT` unless the content is derived from licensed material —
  then keep the origin license and add an attribution README
  (see `plugins/technical-writer/` for an example).

## 3. Register in the marketplace

Add an entry to `.claude-plugin/marketplace.json`, keeping `name`, `version`,
and `description` identical to the plugin's `plugin.json`:

```json
{
  "name": "<plugin-name>",
  "description": "<same as plugin.json>",
  "version": "0.1.0",
  "author": { "name": "Your Name", "email": "you@example.com" },
  "source": "./plugins/<plugin-name>",
  "category": "<development|testing|productivity|documentation|database|...>"
}
```

## 4. Validate

```bash
claude plugin validate .                     # marketplace manifest
claude plugin validate ./plugins/<plugin-name>  # plugin manifest
```

Both must pass before committing.

## 5. Test locally

```bash
claude --plugin-dir ./plugins/<plugin-name>
```

Invoke the skill as `/<plugin-name>:<skill-name>` inside the session.
After editing a skill mid-session, reload with `/reload-plugins`.

## 6. Update the README

Add a row to the Plugins table in the root `README.md` — plugin name,
its commands, and the same description as the manifest.

## Checklist

- [ ] `plugin.json` and marketplace entry are identical (name/version/description)
- [ ] Component directories at the plugin root, only `plugin.json` in `.claude-plugin/`
- [ ] Follows the design criteria (naming, agent/skill split, doc structure)
- [ ] `claude plugin validate` passes for both marketplace and plugin
- [ ] Tested with `--plugin-dir`
- [ ] Root README Plugins table updated
