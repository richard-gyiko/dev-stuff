# docs/specs/<domain>/<capability>.feature
# Executable spec. Mirrors the Rules / Flow in <capability>.md.
# Keep scenarios few and behavioral — the happy path plus the rules that matter.
# Not a test dump: if a rule is internal/data-only, leave it in the .md.

# Use @tags (not YAML frontmatter) to filter/select scenarios — frontmatter
# would break the Gherkin parser. Tag by domain, suite, or risk: @billing @smoke
@<domain>
Feature: <Capability Name>
  Why: <one line — the problem this solves, mirrors the spec's Why>

  Scenario: <happy path, named by its outcome>
    Given <starting state>
    When <the user action>
    Then <the observable result>

  Scenario: <a load-bearing rule or edge case>
    Given <state>
    When <action>
    Then <result>
