# dev-stuff

[![skills.sh](https://skills.sh/b/richard-gyiko/dev-stuff)](https://skills.sh/richard-gyiko/dev-stuff)

Personal collection of agent skills, installable via [skills.sh](https://www.skills.sh).

## Install

```sh
npx skills add richard-gyiko/dev-stuff
```

## Skills

- **[spec-driven-docs](.agents/skills/spec-driven-docs/SKILL.md)** — Minimal spec-driven documentation model for projects. Use when creating, organizing, or maintaining a repo's `docs/` directory; deciding whether a change needs a doc update; writing or updating capability specs, ADRs, or `system.md`; reviewing PRs for documentation hygiene; or migrating an existing `docs/` tree into the spec/decision/system layout.

## Layout

```
.agents/skills/<skill-name>/
  SKILL.md          # required, with name + description frontmatter
  assets/           # templates the skill copies from
  references/       # supplementary docs the skill links to
```

Compatible with Claude Code (`.agents/skills/` is auto-discovered) and any other agent runtime that follows the skills.sh discovery convention.
