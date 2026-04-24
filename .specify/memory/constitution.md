<!--
SYNC IMPACT REPORT
==================
Version change: 1.0.0 → 1.0.1
Rationale: PATCH bump — non-semantic reformatting only. Hard line wraps at ~80
characters removed; paragraphs are now single lines separated by blank lines.
No principle, section, or governance rule changed in meaning.

Modified principles:
- None (wording unchanged)

Added sections:
- None

Removed sections:
- None

Templates requiring updates:
- ✅ .specify/memory/constitution.md (this file)
- ⚠ .specify/templates/plan-template.md — still needs per-feature Constitution
  Check populated with the five principle gates when planning.
- ⚠ .specify/templates/spec-template.md — no changes required.
- ⚠ .specify/templates/tasks-template.md — no structural change required.
- ⚠ AGENTS.md — still only contains the SpecKit marker; add a pointer to this
  constitution the next time agent guidance is expanded.

Follow-up TODOs:
- None.
-->

# Rubicon-ObjC Constitution

## Core Principles

### I. Bridge Fidelity (Objective-C Semantics)

Rubicon-ObjC exists to expose the Objective-C runtime to Python without hiding or reinventing it. Public APIs MUST mirror Objective-C naming, calling, and memory-management semantics (selectors, ARC/retain semantics, message dispatch, nil-handling) so that users who know Cocoa/Foundation can transfer that knowledge directly. Python-side convenience wrappers (e.g. `NSString` helpers) are permitted but MUST NOT silently change observable runtime behaviour, raise surprising exceptions in place of Objective-C errors, or leak/retain objects in ways that diverge from the documented Objective-C contract. Any deviation MUST be called out explicitly in the public documentation together with its rationale.

Rationale: The project's value is being a faithful bridge; users ship code to macOS and iOS where misaligned semantics become hard-to-diagnose, device-only bugs.

### II. Test-Driven, Fully Covered

Every change MUST be accompanied by automated tests runnable via `pytest` through `tox`. New behaviour and bug fixes MUST have tests that fail without the change and pass with it. The test suite MUST treat warnings as errors (per `pyproject.toml`: `filterwarnings = ["error"]`); new warnings MUST be either fixed or explicitly allow-listed with justification in the PR. Coverage MUST NOT regress; code paths gated by Python-version markers MUST use the existing `coverage_conditional_plugin` rules rather than blanket `# pragma: no cover`. Tests that require a running Objective-C runtime MUST be skipped (not silently passed) on unsupported platforms.

Rationale: The bridge is exercised across multiple Python versions and Apple platforms; without disciplined tests, regressions are invisible until a user hits them in production.

### III. Documentation as a Deliverable

Every user-visible addition or change (new API, new argument, new behaviour, deprecation, removal) MUST ship with:

- Updated reference, how-to, or tutorial content under `docs/` following the BeeWare documentation style guide, and
- A release note fragment under `changes/` using the `towncrier` categories configured in `pyproject.toml` (`feature`, `bugfix`, `removal`, `doc`, `misc`), referencing the GitHub issue or PR.

Docstrings for public symbols MUST describe the Objective-C types involved and any lifetime/ownership implications. Documentation-only PRs are valid and expected.

Rationale: Users pick up Rubicon through the docs; release notes are the contract we ship to downstream BeeWare packages (e.g. Toga, Briefcase).

### IV. Backward Compatibility & Clear Versioning

Releases follow Semantic Versioning on the `rubicon-objc` distribution:

- **MAJOR**: removals or incompatible changes to public Python APIs, to the set of supported Python versions, or to observable Objective-C bridging behaviour.
- **MINOR**: additive, backward-compatible features (new classes, wrappers, helpers, expanded platform support).
- **PATCH**: bug fixes and internal refactors with no API-visible effect.

Breaking changes MUST go through a deprecation cycle: the old behaviour remains, emits a `DeprecationWarning` with a concrete replacement, is documented in `changes/*.removal.md`, and is only removed in a subsequent MAJOR release. Anything not documented in `docs/` or exported through the package's public `__all__`/public module paths is internal and MAY change without notice — but such internals MUST be named or located so their non-public status is obvious to callers.

Rationale: Rubicon is depended on by other BeeWare projects and third-party apps; predictable versioning keeps the ecosystem upgradable.

### V. Platform & Toolchain Discipline

The project MUST support every Python version listed in `pyproject.toml` classifiers (currently 3.10 through 3.15) and MUST NOT introduce syntax or stdlib features unavailable on the lowest supported version. Dependencies MUST be pinned in `pyproject.toml` dependency groups; loosening a pin or adding a runtime dependency requires explicit justification in the PR. Code style is enforced by pre-commit (Ruff, codespell, rumdl) with the rules defined in `pyproject.toml`; CI MUST run the full `tox` matrix and pre-commit before a release. Releases are cut from `main` with a clean `towncrier` run producing `docs/en/about/releases.md`.

Rationale: The bridge lives at the intersection of Python versions and Apple platforms; disciplined toolchain management is what makes the matrix tractable.

## Additional Constraints & Quality Standards

- **Supported runtimes**: CPython 3.10+ on macOS and iOS; other Apple platforms (tvOS, watchOS, visionOS) are best-effort and MUST NOT regress when changes are made primarily for macOS/iOS.
- **Licensing**: All contributions are licensed under BSD-3-Clause (per `LICENSE`). New third-party code or assets MUST be license-compatible and attributed.
- **Security & memory safety**: Code touching `ctypes`, `objc_msgSend`, block trampolines, or manual retain/release MUST include tests covering reference-count behaviour and MUST document ownership in the docstring.
- **Community standards**: All participation is governed by the BeeWare Code of Conduct (`CODE_OF_CONDUCT.md`). Contributor obligations for AI tooling are defined by the BeeWare AI Policy referenced in `CONTRIBUTING.md`; contributors remain responsible for their submissions regardless of tooling used.

## Development Workflow & Review Gates

- **Branching**: Work happens on feature branches; PRs target `main`.
- **Pre-commit**: Contributors MUST install and run the configured pre-commit hooks; CI re-runs them and will reject non-conforming diffs.
- **CI gates (MUST all pass before merge)**:
  1. `tox` test matrix (pytest with warnings-as-errors) across supported Python versions.
  2. Coverage report with no uncovered new lines outside documented `coverage_conditional_plugin` rules.
  3. Pre-commit (Ruff lint/format, codespell, rumdl).
  4. Docs build (Sphinx via `beeware-docs-tools`).
  5. Presence of a `changes/*.md` fragment for any user-visible change, or an explicit `misc` fragment for internal work.
- **Review**: At least one maintainer approval is required. Reviewers MUST verify that each of the five Core Principles is satisfied or that the PR explicitly justifies any exception in a "Complexity Tracking" / deviation note.
- **Release**: Version is derived from the Git tag via `setuptools_scm`. Release PRs run `towncrier build` to assemble the release notes and bump the SemVer tag consistent with Principle IV.

## Governance

- **Authority**: This constitution supersedes ad-hoc conventions. Where it conflicts with older README/docs guidance, the constitution wins and the older text MUST be updated.
- **Amendment procedure**: Proposed amendments are opened as PRs editing this file. They MUST include (a) the motivation, (b) the updated Sync Impact Report at the top of this file, and (c) any downstream template or docs edits required to stay consistent. Amendments require maintainer approval on the same terms as code changes.
- **Versioning policy (of this document)**:
  - MAJOR: removing, renaming, or materially redefining a principle or the governance process.
  - MINOR: adding a principle or section, or expanding a principle's binding rules.
  - PATCH: wording clarifications, typo fixes, non-semantic refinements.
- **Compliance review**: At the start of planning any feature (see `.specify/templates/plan-template.md` "Constitution Check"), the plan MUST state how the five Core Principles are satisfied; unjustified violations block the plan. Release PRs MUST include a short statement confirming the checks in "Development Workflow & Review Gates" all passed.
- **Runtime guidance**: Contributor-facing day-to-day guidance lives in `CONTRIBUTING.md` and the online docs under `docs/`; agent/tooling guidance lives in `AGENTS.md`. Those files are subordinate to this constitution and MUST be updated whenever it changes in a way that affects workflow.

**Version**: 1.0.0 | **Ratified**: 2026-04-24 | **Last Amended**: 2026-04-24
