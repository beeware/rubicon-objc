# Rubicon-ObjC - Agent Development Guide

<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
<!-- SPECKIT END -->

Rubicon-ObjC is a Python to Objective-C runtime bridge, maintained as part of the [BeeWare](https://beeware.org) suite. It lets Python code instantiate Objective-C objects, send messages, subclass Objective-C classes, and interoperate with Cocoa / Foundation types. It is used on macOS and iOS and is a dependency of other BeeWare projects (e.g. Toga, Briefcase), so stability and backward compatibility matter.

## Repository layout

- `src/rubicon/objc/` — the package. Public API is what is re-exported from `rubicon.objc.__init__`. Key modules: `api.py`, `runtime.py`, `types.py`, `collections.py`, `ctypes_patch.py`, `eventloop.py`.
- `tests/` — `pytest` suite. Tests that exercise real Objective-C classes live under `tests/objc/` and are built with `make -C tests/objc` before the Python tests run (handled automatically by `tox`).
- `docs/en/` — MkDocs documentation (tutorials, how-to, reference, background). Built via `beeware-docs-tools`.
- `changes/` — `towncrier` news fragments. Every user-visible change ships a fragment here.
- `stubs/` — type stubs used by the docs toolchain.
- `pyproject.toml`, `tox.ini`, `.pre-commit-config.yaml` — canonical source for dependencies, supported Python versions (3.10–3.15), lint rules, test matrix, and coverage configuration.
- `.specify/` — SpecKit workspace (constitution, templates, extensions). Do not edit `.specify/memory/constitution.md` outside the `/speckit.constitution` workflow.


## Toolchain

- **Python**: 3.10–3.14 (see `core/pyproject.toml` classifiers).
- **Supported platforms**: macOS and iOS. Most runtime tests require a working Objective-C runtime and therefore only pass on macOS.
- **Task runner**: `tox` (with `tox-uv`). Install the dev tooling via `uv pip install --group dev` at the repo root, or let `tox` bootstrap.
- **Lint/format**: `ruff` (check + format), `codespell`, `rumdl` (Markdown), configured in root `pyproject.toml`.
- **Pre-commit**: `pre-commit run --all-files` — MUST pass before PR.
- **Packaging / testbed driver**: `briefcase`.
- **Release notes**: `towncrier` (config in root `pyproject.toml`).
- **Docs**: MkDocs; built with the `docs` dependency group.

Do not replace or bypass these tools. Add new dependencies only with a clear need and a compatible license (BSD-3-Clause friendly).

## Commands you should use

Run these via the Bash tool. Do not invent ad-hoc scripts when an equivalent `tox` env exists.

- Full matrix test run (matches CI): `tox`
- Fast single-version tests: `tox -e py312-fast` (swap for 310/311/313/314/315). `-fast` enables `pytest-xdist` and develop installs.
- Coverage run for one version: `tox -e py312-cov` then `tox -e coverage312`.
- Objective-C test fixtures only: `make -C tests/objc` (tox does this for you, but useful when iterating).
- Lint / format (all pre-commit hooks, same as CI): `tox -e pre-commit` or `pre-commit run --all-files`.
- Docs build: `tox -e docs` (full), `tox -e docs-lint` (link/spell check), `tox -e docs-live` (local preview).
- Towncrier check (required before merge for user-visible changes): `tox -e towncrier-check`.
- Assemble release notes (maintainers only): `tox -e towncrier -- build`.

Warnings are errors: `pyproject.toml` sets `filterwarnings = ["error"]`. A test that emits an unhandled warning will fail. Fix the cause; do not silence it globally.

## Coding rules (derived from the constitution)

1. **Bridge fidelity.** Public APIs MUST mirror Objective-C semantics — selectors, message dispatch, ARC/retain behaviour, `nil` handling. Convenience wrappers are fine, but they MUST NOT silently change observable runtime behaviour or object lifetimes. If you deviate, document it.
2. **Test-driven.** Every behaviour change or bug fix MUST include a test that fails without the change and passes with it. Place tests in the appropriate `tests/test_*.py` file (create a new module only when no existing one fits). If the test needs Objective-C fixtures, add/extend the `.h`/`.m` files under `tests/objc/` and update its `Makefile` target.
3. **Coverage must not regress.** Use the existing `coverage_conditional_plugin` markers (`no-cover-if-*`) in `pyproject.toml` for version- or platform-specific branches instead of blanket `# pragma: no cover`.
4. **Documentation is part of the change.** For any user-visible addition, update the relevant `docs/en/...` page (reference/how-to/tutorial/background) and add a `changes/<issue>.<category>.md` fragment. Categories: `feature`, `bugfix`, `removal`, `doc`, `misc` (see `pyproject.toml [tool.towncrier]`). Reference the issue number in the filename.
5. **Docstrings.** Public symbols MUST document the Objective-C types they accept/return and any lifetime/ownership implications.
6. **Backward compatibility.** Do not remove or rename public API without a deprecation cycle: keep the old name, emit a `DeprecationWarning` pointing to the replacement, add a `changes/<issue>.removal.md`. Removal happens in a later MAJOR release, not the same PR.
7. **Internals.** Anything not exported from `rubicon.objc.__init__` or otherwise documented in `docs/` is internal and may change; keep the internal/public split obvious (naming, module location).
8. **Memory-sensitive code.** Changes touching `ctypes`, `objc_msgSend`, block trampolines, or manual retain/release MUST add tests that cover reference counts and MUST document ownership rules in the docstring.
9. **Style.** Enforced by `ruff` (rules in `pyproject.toml [tool.ruff.lint]`), `codespell`, and `rumdl`. Run pre-commit before declaring work done. Do not disable a rule inline without justification in the PR.

## Pull request checklist (what CI will verify)

- [ ] `tox` matrix passes on supported Python versions.
- [ ] Coverage report shows no new uncovered lines outside documented conditional rules.
- [ ] `tox -e pre-commit` clean.
- [ ] `tox -e docs` and `tox -e docs-lint` pass when docs change.
- [ ] `tox -e towncrier-check` passes: a `changes/*.md` fragment exists for any user-visible change (or a `misc` fragment for internal-only work).
- [ ] Public API changes have matching docs and docstring updates.
- [ ] Deprecations follow the cycle described above.
