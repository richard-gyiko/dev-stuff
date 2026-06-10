# Enforcement harness

A spec, ADR, or rule with no check is a comment that rots. The point of the
harness is that the rule and its check live together, and every author — human
or agent — passes the same gates. Keep it minimal: automate the rules that are
load-bearing, link the rest from review.

## The loop

```
git hook (pre-commit / pre-push)
   → skill / agent self-check
      → CI (the backstop)
         → linter / type / test / .feature run
            → feedback (fail fast, point at the spec/ADR)
```

Each layer is cheaper-and-earlier than the next. A local hook gives instant
feedback; CI is the non-bypassable backstop for when a hook is skipped
(`--no-verify`, a fresh clone, an agent shortcut).

## Mapping a rule to a check

Pick the cheapest mechanical check that proves the rule:

| Rule kind | Enforce with |
|---|---|
| Module boundaries / import rules | lint rule (ESLint `no-restricted-imports`, ruff, dependency-cruiser) |
| Data contract / schema / field semantics | schema test, type check, contract test |
| API behavior (status, shape, idempotency) | integration test, `.feature` scenario |
| N+1 / query patterns | query-count assertion, custom lint rule |
| ORM / library restrictions | custom lint rule, banned-import check |
| User-visible workflow | BDD `.feature` run in CI |
| Formatting / style | formatter + lint in pre-commit |
| Architectural choice (ADR) | the check the ADR's "consequences" implies — wire it when the ADR lands |

If a rule genuinely cannot be automated, it is not enforced — say so in the
spec and add it to the PR checklist so a human catches it in review.

## BDD as the executable arm

`.feature` files are not documentation theatre — they run. Wire them so a
failing scenario blocks merge:

- Local: a pre-push hook runs the affected `.feature` suite.
- CI: full `.feature` run on every PR; red blocks merge.
- The scenario text mirrors the spec's rules, so a failure points straight at
  the durable behavior that broke.

Review `.feature` diffs the way you review the spec: they are the contract made
executable, and they are easier to read than AI-generated unit tests.

## Agents pass the same gates

- No `--no-verify`, no skipping CI, no "the test is flaky so I disabled it".
- If an agent proposes skipping a step, CI is the catch — the gate is the same
  one humans hit.
- Hooks and CI commands belong in the repo (committed config), not in an
  individual's local setup, so agents inherit them automatically.

## Worked example

ADR: *"All DB access goes through the repository layer — no ORM calls in
controllers."*

1. ADR records context / decision / consequences.
2. Spec for the affected capability states the rule.
3. Enforcement: a lint rule bans ORM imports outside `repositories/`.
4. Hook: pre-commit runs the linter → instant local failure.
5. CI: same linter runs on PR → backstop.
6. Feedback: lint error message links the ADR (`see docs/decisions/db-access-through-repository-layer.md`).

The decision is now self-defending: the next agent that adds an ORM call in a
controller is stopped before merge, with a pointer to *why*.

## Keep it minimal

- Do not gold-plate. Enforce the rules that actually break things; leave
  cosmetic preferences to the formatter.
- One check per rule, owned by the spec/ADR that states the rule.
- Prefer a fast local hook + a CI backstop over many slow, redundant gates.
