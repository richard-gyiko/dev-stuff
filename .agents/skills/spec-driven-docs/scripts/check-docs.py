#!/usr/bin/env python3
"""Lint a docs/ tree against the spec-driven-docs model.

The skill preaches an enforcement loop; this is its executable arm. Wire it into
a pre-commit hook and CI so the doc rules defend themselves.

Checks:
  - specs and ADRs carry valid YAML frontmatter (status, plus domain / date)
  - no forbidden ephemeral files or folders leak into docs/
  - .feature sidecars are real Gherkin (declare a Feature)

Std-lib only, no external deps. Exits non-zero on any violation.

Usage:
    python check-docs.py [docs_dir]      # defaults to ./docs
"""

import sys
from pathlib import Path

SPEC_STATUS = {"active", "deprecated"}
ADR_STATUS = {"proposed", "accepted", "superseded", "deprecated"}

FORBIDDEN_FILES = {"tasks.md", "plan.md", "todo.md", "scratch.md", "notes.md"}
FORBIDDEN_DIRS = {"active", "done", "archive", "changes"}


def parse_frontmatter(text):
    """Return dict of top-level scalar keys from a leading --- block, or None."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    fm = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fm
        if ":" in line and not line.startswith((" ", "\t", "#")):
            key, _, val = line.partition(":")
            fm[key.strip()] = val.split("#", 1)[0].strip()
    return None  # no closing fence


def check(docs_dir):
    docs = Path(docs_dir)
    errors = []
    if not docs.is_dir():
        return [f"{docs}: not a directory"]

    # forbidden files / dirs anywhere under docs/
    for p in docs.rglob("*"):
        if p.is_dir() and p.name in FORBIDDEN_DIRS:
            errors.append(f"{p}: forbidden folder (keep ephemeral work out of docs/)")
        if p.is_file() and p.name in FORBIDDEN_FILES:
            errors.append(f"{p}: forbidden ephemeral file (belongs in an issue/PR)")

    # specs: frontmatter status + domain
    for p in (docs / "specs").rglob("*.md"):
        fm = parse_frontmatter(p.read_text(encoding="utf-8"))
        if fm is None:
            errors.append(f"{p}: missing YAML frontmatter")
            continue
        if fm.get("status") not in SPEC_STATUS:
            errors.append(f"{p}: status must be one of {sorted(SPEC_STATUS)}")
        if not fm.get("domain"):
            errors.append(f"{p}: missing 'domain' in frontmatter")

    # ADRs: frontmatter status + date
    for p in (docs / "decisions").glob("*.md"):
        fm = parse_frontmatter(p.read_text(encoding="utf-8"))
        if fm is None:
            errors.append(f"{p}: missing YAML frontmatter")
            continue
        if fm.get("status") not in ADR_STATUS:
            errors.append(f"{p}: status must be one of {sorted(ADR_STATUS)}")
        if not fm.get("date"):
            errors.append(f"{p}: missing 'date' in frontmatter")

    # .feature sidecars: must declare a Feature
    for p in (docs / "specs").rglob("*.feature"):
        if "Feature:" not in p.read_text(encoding="utf-8"):
            errors.append(f"{p}: no 'Feature:' declaration - not valid Gherkin")

    return errors


def main():
    docs_dir = sys.argv[1] if len(sys.argv) > 1 else "docs"
    errors = check(docs_dir)
    if errors:
        print(f"docs check failed ({len(errors)} issue(s)):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)
    print(f"docs check passed ({docs_dir})")


if __name__ == "__main__":
    main()
