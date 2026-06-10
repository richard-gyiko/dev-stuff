#!/usr/bin/env python3
"""Scaffold a docs/ tree for the spec-driven-docs model.

Idempotent: safe to re-run. Never overwrites an existing system.md or spec.

Creates:
  docs/system.md            (stub with the standard sections)
  docs/specs/.gitkeep
  docs/decisions/.gitkeep
  .scratchpad/ entry in .gitignore

Std-lib only. Domain folders are NOT pre-created — add docs/specs/<domain>/
when the first capability in that domain appears.

Usage:
    python bootstrap-docs.py [repo_root]   # defaults to .
"""

import sys
from pathlib import Path

SYSTEM_MD = """\
# System

## Overview

One paragraph: what this system is and does.

## Modules

- module — responsibility (link to specs)

## Data flows

- source → transform → sink

## Integrations

- external system — purpose

## Deployment

- where and how this runs

## Related specs/decisions

- `docs/specs/...`
- `docs/decisions/...`
"""


def ensure_gitignore(root):
    gi = root / ".gitignore"
    entry = ".scratchpad/"
    existing = gi.read_text(encoding="utf-8") if gi.exists() else ""
    if entry in existing.split():
        return f"  .gitignore already ignores {entry}"
    sep = "" if existing.endswith("\n") or not existing else "\n"
    gi.write_text(f"{existing}{sep}{entry}\n", encoding="utf-8")
    return f"  added {entry} to .gitignore"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    docs = root / "docs"
    done = []

    (docs / "specs").mkdir(parents=True, exist_ok=True)
    (docs / "decisions").mkdir(parents=True, exist_ok=True)

    for d in ("specs", "decisions"):
        keep = docs / d / ".gitkeep"
        if not keep.exists():
            keep.write_text("", encoding="utf-8")
            done.append(f"  created docs/{d}/.gitkeep")

    system = docs / "system.md"
    if system.exists():
        done.append("  docs/system.md exists - left untouched")
    else:
        system.write_text(SYSTEM_MD, encoding="utf-8")
        done.append("  created docs/system.md")

    done.append(ensure_gitignore(root))

    print("bootstrap complete:")
    for line in done:
        print(line)


if __name__ == "__main__":
    main()
