# Changelog

All **notable changes** to this project will be documented in this file.

Full changelog available at [GitHub releases](https://github.com/commit-check/commit-check/releases).

## v2.13.0 (2026-08-04)

### New Features

* **Stable rule IDs** — every diagnostic now carries an ID such as `CC003` that
  never changes once released. The ID appears in terminal output and in
  `--format json` as `rule_id`, alongside a `docs_url` pointing at the rule's
  section of the [rules reference](rules.md), so a failure can be cited in
  review, looked up, or matched by tooling.
  See PR [#512](https://github.com/commit-check/commit-check/pull/512).
* **More branch types accepted by default** — `docs/`, `ci/`, `test/`,
  `refactor/`, `build/`, `perf/` and `style/` join the default
  `allow_branch_types`, which stays a superset of the Conventional Branch
  specification.
  See PR [#505](https://github.com/commit-check/commit-check/pull/505).

### Bug Fixes

* **Rule IDs link to their documentation** — where the terminal renders OSC 8
  hyperlinks, the ID itself is the link and the separate `Docs:` line is
  dropped. Piped output and CI logs keep the printed URL. Failure output also
  names rules the way the reference titles them (`subject-min-length` rather
  than `subject_min_length`), and the advice for the length rules now names the
  configured limit instead of referring to it.
  See PR [#520](https://github.com/commit-check/commit-check/pull/520).

### Documentation

* The documentation, the landing page and the blog moved to
  [commit-check.com](https://commit-check.com) and are published from one
  domain. `docs.commit-check.com` URLs redirect.
  See PRs [#515](https://github.com/commit-check/commit-check/pull/515),
  [#518](https://github.com/commit-check/commit-check/pull/518) and
  [#519](https://github.com/commit-check/commit-check/pull/519).

## v2.12.2 (2026-08-01)

### Bug Fixes

* **Space-separated AI model names** — Co-author trailers naming a model with
  spaces rather than hyphens are now recognised by the AI attribution check.
  See PR [#506](https://github.com/commit-check/commit-check/pull/506).

### Chores

* Recognised more common imperative verbs, so ordinary subjects stop being
  rejected by `subject_imperative`.
  See PR [#496](https://github.com/commit-check/commit-check/pull/496).

## v2.12.1 (2026-07-31)

### Bug Fixes

* **Running without the package installed** — `PackageNotFoundError` is handled
  instead of crashing when the version cannot be resolved.
  See PR [#483](https://github.com/commit-check/commit-check/pull/483).
* Hardened the `pip install` step flagged by SonarCloud code scanning.
  See PR [#479](https://github.com/commit-check/commit-check/pull/479).

## v2.12.0 (2026-07-24)

### New Features

* **Configurable author patterns** — `author_name` and `author_email` accept a
  custom regex, so organisations can require their own naming or email domain
  instead of the built-in patterns.
  See PR [#459](https://github.com/commit-check/commit-check/pull/459).

### Bug Fixes

* **Crash on Chinese Windows** — commit messages are no longer decoded with the
  system GBK codec, which raised `UnicodeDecodeError`.
  See PR [#475](https://github.com/commit-check/commit-check/pull/475).
* **Author validation reads git config first** — `git config user.name` is the
  identity the *next* commit will carry, so it is checked before falling back
  to the last commit's author. A misconfigured identity used to pass whenever
  the previous commit happened to be valid.
  See PR [#461](https://github.com/commit-check/commit-check/pull/461).
* `require_signed_off_by` accepts any name, and is skipped for authors listed
  in `ignore_authors`.
  See PRs [#462](https://github.com/commit-check/commit-check/pull/462) and
  [#464](https://github.com/commit-check/commit-check/pull/464).

## v2.11.0 (2026-07-06)

### New Features

* **AI attribution governance** — Added support for forbidding known AI tool
  signatures (e.g., `Co-authored-by: Copilot`) in commit messages. New
  `[commit]` config option `ai_attribution` (default `"ignore"`) rejects
  commits carrying known AI tool signatures when set to `"forbid"`. See PR [#456](https://github.com/commit-check/commit-check/pull/456).

### Bug Fixes

* Fixed `MergeBaseValidator` branch detection — replaced `git branch -a`
  regex matching with `git rev-parse --verify` to avoid false positives
  (e.g., pattern `main` matching `main-staging`). See PR [#451](https://github.com/commit-check/commit-check/pull/451).

### Chores

* Added OpenSSF Scorecard workflow, badge, and pinned dependency SHAs for CI
* Migrated PyPI publishing to `pypa/gh-action-pypi-publish`
* Removed OpenSSF Scorecard badge after evaluation (moved to Scorecard dashboard)

## v2.10.1 (2026-06-30)

### Bug Fixes

* **WIP detection case-insensitivity** — `WIP` (`[WIP]`, `WIP:`, `wip:`,
  etc.) is now recognized regardless of case across all common patterns.
  See PR [#448](https://github.com/commit-check/commit-check/pull/448).
* **Conventional commit special characters** — Allowed special characters
  (parentheses, brackets, etc.) in the description part of conventional commit
  messages. See PR [#447](https://github.com/commit-check/commit-check/pull/447).

### Refactors

* Extracted `_get_commit_message` to `BaseValidator` to remove code
  duplication across validators. See PR [#445](https://github.com/commit-check/commit-check/pull/445).
* Removed legacy YAML config parsing code from `util.py`.
  See PR [#444](https://github.com/commit-check/commit-check/pull/444).

## v2.10.0 (2026-06-26)

### New Features

* **Dependabot / Renovate as default branch type** — `dependabot/` and
  `renovate/` branch prefixes are now included in `DEFAULT_BRANCH_TYPES`,
  so dependency update branches are automatically recognized.
  See PR [#442](https://github.com/commit-check/commit-check/pull/442).

## v2.9.0 (2026-06-22)

### New Features

* **AI agent branch prefixes (Conventional Branch v1.1.0)** — Added
  `ai/`, `claude/`, `codex/`, `copilot/`, and `cursor/` to
  `DEFAULT_BRANCH_TYPES` so branches created by AI coding agents are
  recognized as valid. See PR [#438](https://github.com/commit-check/commit-check/pull/438).

## v2.8.1 (2026-06-22)

### Chores

* Fixed 27 SonarQube code-quality issues across source and test files,
  including path traversal vulnerability fix, cognitive complexity
  reduction, and duplicate branch consolidation. See PR [#436](https://github.com/commit-check/commit-check/pull/436).
* Added SchemaStore IDE autocompletion support for `cchk.toml`.
  See PR [#433](https://github.com/commit-check/commit-check/pull/433).

## v2.8.0 (2026-06-13)

### New Features

* **Custom commit message pattern** — New `message_pattern` option in the
  `[commit]` config section allows replacing the built-in Conventional Commits
  regex with a user-defined regex pattern. Also supported via the
  `CCHK_MESSAGE_PATTERN` environment variable. See PR [#427](https://github.com/commit-check/commit-check/pull/427).

### Breaking Changes

* **Dropped Python 3.9 support** — Minimum required Python version is now
  3.10. Type annotations have been modernized (PEP 604/585) and the
  `py.typed` marker added for downstream type checkers.
  See PR [#424](https://github.com/commit-check/commit-check/pull/424).

## v2.7.1 (2026-06-08)

### Chores

* Added `auto` to the list of imperative verbs. See PR [#417](https://github.com/commit-check/commit-check/pull/417).
* Added commit-check vs GitHub Rulesets comparison table to the README.
  See PR [#419](https://github.com/commit-check/commit-check/pull/419).

## v2.7.0 (2026-05-16)

### New Features

* **Force push detection and blocking** — Added `--no-force-push` CLI flag and
  `check-no-force-push` pre-push hook that inspect pushed ref ancestry via
  `git merge-base --is-ancestor` to detect and block `git push --force` and
  `git push -f`. A new `[push]` TOML config section with
  `allow_force_push` (default `true`) controls the behavior. Environment
  variable `CCHK_ALLOW_FORCE_PUSH` is also supported.

* **`validate_push()` API** — New `commit_check.api.validate_push()`
  function for programmatic push safety checks, matching the `--no-force-push`
  CLI behavior without spawning a subprocess.

* **Standalone mode** — When `--no-force-push` is run outside a pre-push hook
  (no stdin), it checks whether pushing `HEAD` to its configured upstream
  would require force, using `git ls-remote` and optional `git fetch` to
  resolve the remote commit.

* **Expanded imperative verbs** — Added 156 new imperative verbs across 10
  categories (auth/security, data ops, lifecycle, I/O, debugging, UI/UX,
  engineering, general), growing the total from 234 to 390.
  See PR [#414](https://github.com/commit-check/commit-check/pull/414).

## v2.6.0 (2026-04-20)

### New Features

* **Lower-noise CLI failure output** — Added `--no-banner` to suppress the ASCII art header while preserving detailed errors and suggestions.
* **Compact failure mode** — Added `--compact` to print one `[FAIL]` line per failing check for CI logs and automation-friendly terminal output. This mode also suppresses the banner.

### Bug Fixes

* Fixed `print_error_header` state handling so repeated validations stay consistent when `--compact` is used.

## v2.5.0 (2026-04-03)

### New Features

* **Co-author bypass in `ignore_authors`** — `_should_skip_commit_validation()` now parses `Co-authored-by:` trailers in the commit message body. If any co-author name matches `ignore_authors`, all commit checks are skipped. Useful for AI bots that co-author commits (e.g., `coderabbitai[bot]`).
* **Organization-level config inheritance via `inherit_from`** — New top-level TOML key that loads a parent config from a GitHub shorthand (`github:owner/repo:path`), a local file path, or an HTTPS URL, then deep-merges it with local settings. HTTP (non-TLS) URLs are rejected to prevent MITM attacks.
* **Git config author validation** — `AuthorValidator` now checks `git config user.name` / `user.email` first (the identity used for the *next* commit), falling back to `git log` if unset. Previously, a misconfigured identity would pass if the last commit had a valid author.

### Bug Fixes

* Fixed incorrect mock target in `test_main_with_message_empty_string_no_stdin_with_git`: was patching `commit_check.util.get_commit_info` (ineffective) instead of `commit_check.engine.get_commit_info`.

## v2.0.0 (2025-10-01)

!!! warning

    This major release introduces significant architectural changes and breaking updates to commit-check. Please review carefully before upgrading.

### What's New

* **TOML Configuration** — Replaces the old `.commit-check.yml` with `cchk.toml` or `commit-check.toml` for clearer syntax.
* **Simplified CLI & Hooks** — Legacy pre-commit hooks and command-line options have been removed for a cleaner, more consistent interface.
* **New Validation Engine** — The validation system has been completely redesigned around a new ValidationEngine to improve maintainability and flexibility.

#### Breaking Changes

Configuration Format:

* `.commit-check.yml` has been replaced with `cchk.toml` or `commit-check.toml`.
* All YAML configurations must be migrated to TOML from this version onward.
* See the [Migration Guide](migration.md) for step-by-step instructions.

Removed Pre-commit Hooks and CLI Options:

* Several legacy hooks and command-line flags have been removed in favor of a simplified interface.
* Removed hooks: `check-commit-signoff`, `check-merge-base`, `check-imperative`.
* Removed CLI options: `--signoff`, `--merge-base`, `--imperative`.

Module Removal:

* The following legacy modules have been removed: `author.py`, `branch.py`, `commit.py`, `error.py`.

Architecture Redesign:

* The validation system has been completely restructured around the new `ValidationEngine`, breaking compatibility with any code or integrations relying on the old module structure.

See PR [#280](https://github.com/commit-check/commit-check/pull/280)

## v0.10.2 (2025-08-26)

Last release before the big v2.0 changes.

## v0.1.0 (2022-11-02)

Initial release of commit-check.
