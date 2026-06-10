---
status: active        # active | deprecated
domain: <domain>      # matches the specs/<domain>/ folder
---

# <Capability Name>

## Purpose

What this capability is responsible for.

## Why

Optional. Keep to ≤4 lines. Skip entirely when the purpose is self-evident.

- Problem: what was missing or broken without this.
- Goal: the outcome it delivers.
- Flow: the key user journey, one line.

## Behavior

- The system must...
- The system must...
- The system must not...

## Rules

- Important business or technical rules.
- Authorization requirements.
- Data constraints.
- Ordering, timing, or lifecycle rules.

## Inputs and outputs

Inputs:

- ...

Outputs:

- ...

## Edge cases

- ...
- ...

## Observability

How we know this is working in production.

- logs
- events
- metrics
- audit records
- alerts

## Scenarios

For user-visible workflow capabilities, mirror the key rules as executable BDD
scenarios in a sibling `<capability>.feature` (Gherkin). Skip for pure
data/internal contracts. Keep scenarios few and behavioral, not exhaustive.

- `./<capability>.feature`

## Related

- `docs/system.md`
- `docs/specs/...`
- `docs/decisions/...`
