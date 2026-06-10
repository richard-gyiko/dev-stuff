---
name: spec-driven-docs
description: Minimal spec-driven documentation model for a repo's `docs/` tree — capability specs (with optional product-intent `Why` blocks and executable BDD `.feature` sidecars), ADRs, a `system.md` map, YAML frontmatter for filtering/preload, and an enforcement loop (git hooks → CI → linters) that makes rules self-defending. Use whenever creating, organizing, or maintaining project docs; deciding whether a change needs a doc/spec/ADR update; writing or reviewing capability specs, ADRs, PRDs, or BDD/Gherkin/Cucumber scenarios; adding frontmatter to docs; setting up checks that enforce architecture or documentation rules; reviewing PRs for documentation hygiene; or migrating an existing `docs/` tree into the spec/decision/system layout. Reach for this even when the user says "write up why we built this", "add a feature file", or "enforce our module boundaries" without naming docs explicitly.
---

# Spec-Driven Documentation

Persist only documentation with durable value: what the system must do, what contracts must hold, why major decisions were made, how the system fits together.

Everything else (task lists, plans, scratchpads, PR history, change archives) belongs in issues, PRs, commits, or ignored local folders.

**Durable behavior** = a contract a future change must respect: authorization rules, data contracts, API behavior, external integrations, money/billing rules, user-visible workflow rules, production operational behavior.

## Three persistent doc types

```
docs/
  system.md                              # system map: modules, flows, links
  specs/<domain>/<capability>.md         # durable behavior per capability
  specs/<domain>/<capability>.feature    # optional BDD scenarios (user-visible flows)
  decisions/<slug>.md                    # ADRs for major choices
```

- **`system.md`** — map, not territory. List modules, data flows, integrations, deployment shape. Link to specs/decisions; do not duplicate them.
- **specs** — name by capability, not ticket. State purpose, behavior, rules, I/O, edge cases, observability.
  - Optional **`Why`** block at the top (Problem / Goal / Flow, ≤4 lines) captures product intent. Skip when obvious.
  - Optional **BDD sidecar** `<capability>.feature` for user-visible workflows: executable Gherkin (e.g. Cucumber) that mirrors the spec's key rules. Reviewable, maps flow → test. Skip for pure data/internal contracts; keep scenarios few and behavioral.
- **decisions** — ADRs. Capture context, decision, alternatives, consequences. Numbered.

The `.feature` file is part of its spec, not a fourth doc type.

### Frontmatter

Every spec and ADR carries minimal YAML frontmatter so tools and agents can
filter, index, and preload without parsing the body.

Spec:

```yaml
---
status: active        # active | deprecated
domain: agents        # matches the specs/<domain>/ folder
---
```

ADR:

```yaml
---
status: accepted               # proposed | accepted | superseded | deprecated
date: 2026-06-10               # decision date (immutable)
superseded-by: <slug>          # optional, the ADR that replaces this one
---
```

Keep it minimal. Do not add `updated` (git owns freshness) or a `related:` list
(the prose `## Related` is the single source — tools derive the graph from it).
`.feature` files take no frontmatter — use Gherkin `@tags` to filter scenarios.

## Forbidden in persistent docs

```
tasks.md  plan.md  todo.md  scratch.md  notes.md
active/   done/    archive/  changes/
```

Use `.scratchpad/` (gitignored) for ephemeral agent scratch. Do not use `.agent/` — it visually collides with the `.agents/skills/` convention.

## When to create or update

- **Update an existing spec** when durable behavior changes. Default action.
- **Create a new spec** only when a new durable capability appears.
- **Create an ADR** only for major architectural decisions worth not re-litigating.
- **No doc change** for typo fixes, UI polish, one-off scripts, no-behavior refactors, experiments, task-level implementation.

See [references/triggers.md](references/triggers.md) for the full durable-vs-not trigger list.

## Naming

Lowercase kebab-case. Capability-shaped, not ticket-shaped.

- Good: `tool-execution.md`, `slack-release-notifications.md`, `invoice-transaction-matching.md`
- Bad: `add-auth.md`, `fix-agent-permissions.md`, `auth.md`, `misc.md`

ADR files: slug-only, same kebab-case rule, no number prefix. Example: `keep-agent-plans-ephemeral.md`. Order and lifecycle come from the `date:` and `status:` frontmatter, not the filename — this avoids number-collision conflicts when ADRs land on parallel branches.

See [references/examples.md](references/examples.md) for fuller good/bad lists and spec-body anti-patterns.

## Workflow for a change

1. Understand the request.
2. Check whether an existing spec applies.
3. If durable behavior changes, update that spec (and, for user-visible workflows, its `.feature` scenarios).
4. Keep the implementation plan ephemeral (chat/PR description).
5. Implement and test.
6. Update `system.md` only if the system map changed.
7. Add an ADR only if a major decision was made.

For trivial changes: implement, test, do not touch docs.

## Bootstrapping a new repo

When `docs/` does not yet exist, run the scaffolder (idempotent, never overwrites):

```
python scripts/bootstrap-docs.py [repo_root]
```

It creates `docs/system.md` (stubbed sections), `docs/specs/` and `docs/decisions/` (with `.gitkeep`), and adds `.scratchpad/` to `.gitignore`. Then optionally drop `assets/pr-checklist.md` into the PR template.

Do not pre-create domain folders. Add `docs/specs/<domain>/` when the first capability in that domain appears.

## Templates

Ready-to-copy templates in `assets/`. Read and copy when creating a new file.

- `assets/spec-template.md` — standard capability spec (includes optional `Why` block)
- `assets/data-spec-template.md` — data-heavy variant (sources, quality checks)
- `assets/feature-template.feature` — minimal Gherkin BDD sidecar for a spec
- `assets/adr-template.md` — architecture decision record
- `assets/pr-checklist.md` — drop into PR template or copy into PR description

## Linking

Keep `## Related` links bidirectional. When spec A references spec B, add A to B's `## Related` section too. Same for spec ↔ ADR.

## Enforcement

Docs do not enforce themselves. A spec or ADR is a claim; without a check, it
rots and agents (and humans) drift from it. Wire the same loop for both:

```
git hook (pre-commit/pre-push)  →  skill/agent check  →  CI  →  linter/test  →  feedback
```

- Encode each load-bearing rule as a mechanical check where possible: lint rule, type, schema test, custom ESLint/ruff rule, or a `.feature` run in CI.
- Agents pass the same gates humans do — no skipping. CI is the backstop when a local hook is bypassed.
- BDD `.feature` files are the executable arm: CI runs them; a failing scenario blocks merge.
- When a rule cannot be automated, link the spec/ADR from the PR checklist so review catches it.

The doc model enforces *itself* via `scripts/check-docs.py` — it lints frontmatter, blocks forbidden ephemeral files/folders, and validates `.feature` sidecars. Wire it into a pre-commit hook and CI:

```
python scripts/check-docs.py [docs_dir]   # exits non-zero on violations
```

See [references/enforcement.md](references/enforcement.md) for the layer-by-layer harness and worked examples.

## Migrating an existing `docs/` tree

See [references/migration.md](references/migration.md) for keep / move / delete / merge rules and worked examples.

## Agent rules

1. Read `docs/system.md` before broad architectural changes.
2. Check `docs/specs/` before changing durable behavior.
3. Update an existing spec rather than creating a new one when possible.
4. Never add persistent plans, task lists, scratchpads, or active/done/archive folders.
5. Prefer fewer, better docs over many stale docs.
6. Keep `.feature` scenarios in sync with the spec, and never disable a check to make a change pass — fix the code or update the rule.
