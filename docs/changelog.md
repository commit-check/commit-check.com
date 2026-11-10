# Changelog

Notable changes to the commit-check CLI, one line each, newest first. Every
change, including maintenance, is in the
[GitHub releases](https://github.com/commit-check/commit-check/releases).

## Highlights

The releases worth knowing about. Each links to its entry below and to the
page that documents it.

| Version | What changed | Documented in |
|---|---|---|
| [2.20.3](#v2203) | Failures print a one-line header and an indented block per check, in place of the ASCII banner; an agent skill for coding agents | [Getting started](getting-started.md#2-watch-it-reject-something) · [With AI coding agents](guides/ai-agents.md#tell-the-agent) |
| [2.20.1](#v2201) | `--ai-attribution-only` checks a pull request description against your AI policy; JSON lists the AI tools found; more AI marks recognised | [Checking a pull request description](guides/policies.md#checking-a-pull-request-description) · [CC013](rules.md#cc013) |
| [2.20.0](#v2200) | Commits authored by an AI tool rejected; subject length `0` turns the rule off; Python 3.11+ required | [CC017](rules.md#cc017) · [CC013](rules.md#cc013) · [CC004](rules.md#cc004) |
| [2.19.5](#v2195) | GitHub merge queue branches accepted by default; aider's default co-author trailer recognised; exit 2 when git cannot read the repository | [CC201](rules.md#cc201) · [CC013](rules.md#cc013) · [Exit codes](troubleshoot.md#exit-codes) |
| [2.19.4](#v2194) | `agents/` branches accepted by default; Cursor's `Made-with: Cursor` trailer recognised | [CC201](rules.md#cc201) · [CC013](rules.md#cc013) |
| [2.19.3](#v2193) | A quoted `"false"` for a true/false setting refused instead of read as true | [Every option](configuration.md#every-option) |
| [2.19.2](#v2192) | Copilot coding agent recognised; config values of the wrong type refused; commit text printed safely | [CC013](rules.md#cc013) · [Every option](configuration.md#every-option) · [Color and links](example.md#color-and-links) |
| [2.19.1](#v2191) | `develop` accepted by default; stricter merge-subject, fixup, WIP and sign-off checks | [CC201](rules.md#cc201) · [CC001](rules.md#cc001) · [CC009](rules.md#cc009) |
| [2.19.0](#v2190) | Branch descriptions held to the Conventional Branch grammar; Amp, OpenHands, Factory Droid and Jules recognised | [CC201](rules.md#cc201) · [CC013](rules.md#cc013) |
| [2.18.3](#v2183) | `--fix` corrects a message in place; `--branch` reads GitLab, Bitbucket, Azure and Jenkins variables | [Fixing a message in place](example.md#fixing-a-message-in-place) · [Other CI](guides/other-ci.md) |
| [2.18.0](#v2180) | AI disclosure policy: three rules, and the correction written for you | [Policy guides](guides/policies.md#asking-for-disclosure-instead) · [CC014](rules.md#cc014) |
| [2.17.0](#v2170) | Concrete corrections for mechanical slips; a `warn` level per rule | [Reading the JSON](example.md#reading-the-json) · [Report without enforcing](configuration.md#report-a-rule-without-enforcing-it) |
| [2.16.0](#v2160) | Tag name validation, and file size, path and pattern policies | [CC401](rules.md#cc401) · [CC302–CC304](rules.md#push-rules) |
| [2.15.1](#v2151) | Color and rule-ID links appear only where they render; `NO_COLOR` honoured | [Color and links](example.md#color-and-links) |
| [2.15.0](#v2150) | `--rev` names the commit under test; skipped checks are named on stderr | [Command-line recipes](example.md#checking-a-range-of-commits) |
| [2.14.0](#v2140) | CC003 judges imperative mood by a word's form, not by a list of verbs | [CC003](rules.md#cc003) |
| [2.13.1](#v2131) | JSON output reports the checked value for passing checks | [Output for scripts and CI](example.md#output-for-scripts-and-ci) |
| [2.13.0](#v2130) | Stable rule IDs in terminal output and JSON | [Rules reference](rules.md) |
| [2.12.0](#v2120) | Author name and email patterns became configurable | [CC101](rules.md#cc101) · [CC102](rules.md#cc102) |
| [2.11.0](#v2110) | AI attribution policy | [Policy guides](guides/policies.md#ai-attribution) |
| [2.10.0](#v2100) | `dependabot/` and `renovate/` branches accepted by default | [CC201](rules.md#cc201) |
| [2.9.0](#v290) | AI agent branch prefixes accepted by default | [CC201](rules.md#cc201) |
| [2.8.0](#v280) | Custom `message_pattern`; Python 3.9 dropped | [CC001](rules.md#cc001) |
| [2.7.0](#v270) | Force push blocking | [CC301](rules.md#cc301) |
| [2.6.0](#v260) | `--format json` and the Python API; `--compact`, `--no-banner` | [Command-line recipes](example.md#output-for-scripts-and-ci) |
| [2.5.0](#v250) | Organization-wide config with `inherit_from` | [Across an organization](guides/organization.md) |
| [2.0.0](#v200) | Configuration moved from YAML to TOML — breaking | [Migrating from v1](migration.md) |

## v2.20.4 (2026-11-10) { #v2204 }

### Fixed

* `require_body` no longer takes trailers alone, such as the `Signed-off-by:` line from `git commit -s`, for a body. ([CC011](rules.md#cc011), [#689](https://github.com/commit-check/commit-check/pull/689))
* `ignore_authors` written as one string is split on commas, instead of skipping any author whose name is part of it. ([Every option](configuration.md#every-option), [#689](https://github.com/commit-check/commit-check/pull/689))
* `--author-name` and `--author-email` honour `git commit --author` and the `author.name` and `author.email` settings. ([Checking the committer](example.md#checking-the-committer), [#689](https://github.com/commit-check/commit-check/pull/689))

## v2.20.3 (2026-11-10) { #v2203 }

### Added

* An agent skill teaches coding agents to check a message before they commit. ([With AI coding agents](guides/ai-agents.md#tell-the-agent), [#679](https://github.com/commit-check/commit-check/pull/679), [#686](https://github.com/commit-check/commit-check/pull/686))

### Changed

* A failure prints a one-line header and an indented block per check, in place of the ASCII banner. ([Getting started](getting-started.md#2-watch-it-reject-something), [#682](https://github.com/commit-check/commit-check/pull/682))

### Fixed

* CC017 on a message that is not committed yet suggests setting your own `user.name` and `user.email`, not amending. ([CC017](rules.md#cc017), [#685](https://github.com/commit-check/commit-check/pull/685))
* `--ai-attribution-only` with no text piped in passes, instead of judging `HEAD`. ([Guide](guides/policies.md#checking-a-pull-request-description), [#684](https://github.com/commit-check/commit-check/pull/684))

## v2.20.2 (2026-11-08) { #v2202 }

### Changed

* `--ai-only` is renamed `--ai-attribution-only`; the old name still works. ([Guide](guides/policies.md#checking-a-pull-request-description), [#677](https://github.com/commit-check/commit-check/pull/677))

## v2.20.1 (2026-11-08) { #v2201 }

### Added

* `--ai-only` checks a pull request description against your AI policy, without the commit message rules. ([Guide](guides/policies.md#checking-a-pull-request-description), [#673](https://github.com/commit-check/commit-check/pull/673))
* `--format json` lists the AI tools it found in `ai_tools`, even under `ignore`. ([Reading the JSON](example.md#reading-the-json), [#673](https://github.com/commit-check/commit-check/pull/673))
* More AI marks are recognised: Warp, Crush, the Claude Code notice without the emoji, `Reviewed-by:` and similar trailers naming a tool, and Codex, Devin, Jules and Cursor run links. ([CC013](rules.md#cc013), [#672](https://github.com/commit-check/commit-check/pull/672), [#673](https://github.com/commit-check/commit-check/pull/673))

## v2.20.0 (2026-11-08) { #v2200 }

### Breaking

* Python 3.11 or newer is required. On `ubuntu-22.04`, add `actions/setup-python` before the Action. ([GitHub Action](guides/github-actions.md), [#662](https://github.com/commit-check/commit-check/pull/662))

### Added

* A commit authored by an AI tool, such as `claude[bot]`, fails under `forbid` and `disclose`. ([CC017](rules.md#cc017), [#661](https://github.com/commit-check/commit-check/pull/661))
* Continue, Mistral Vibe and Qwen Code are recognised. ([CC013](rules.md#cc013), [#657](https://github.com/commit-check/commit-check/pull/657), [#659](https://github.com/commit-check/commit-check/pull/659))

### Changed

* `subject_max_length = 0` or `subject_min_length = 0` turns that check off. ([CC004](rules.md#cc004), [#660](https://github.com/commit-check/commit-check/pull/660))

### Fixed

* `[commit] require_verified`, read by the GitHub App, no longer warns as an unknown setting. ([#656](https://github.com/commit-check/commit-check/pull/656))

## v2.19.5 (2026-11-04) { #v2195 }

### Fixed

* GitHub merge queue branches (`gh-readonly-queue/…`) pass the branch check by default. ([CC201](rules.md#cc201), [#653](https://github.com/commit-check/commit-check/pull/653))
* aider's default co-author trailer is recognised. ([CC013](rules.md#cc013), [#652](https://github.com/commit-check/commit-check/pull/652))
* When git cannot read the repository, for example "dubious ownership", the run exits 2 instead of passing without checking. ([Exit codes](troubleshoot.md#exit-codes), [#654](https://github.com/commit-check/commit-check/pull/654))

## v2.19.4 (2026-10-29) { #v2194 }

### Changed

* `agents/` branches, made by VS Code's Agents window, pass by default. ([CC201](rules.md#cc201), [#645](https://github.com/commit-check/commit-check/pull/645))

### Fixed

* Cursor's `Made-with: Cursor` trailer is recognised. ([CC013](rules.md#cc013), [#643](https://github.com/commit-check/commit-check/pull/643))

## v2.19.3 (2026-10-21) { #v2193 }

### Fixed

* A quoted true/false value such as `"false"` is a config error (exit 2) instead of being read as true. ([Every option](configuration.md#every-option), [#636](https://github.com/commit-check/commit-check/pull/636))

## v2.19.2 (2026-10-18) { #v2192 }

### Changed

* A setting of the wrong type, such as `subject_max_length = "50"`, is a config error (exit 2) instead of being misread. Check your config when you upgrade. ([Every option](configuration.md#every-option), [#624](https://github.com/commit-check/commit-check/pull/624))
* The rebase check reports a skip, not a pass, when its target branch does not exist. ([CC202](rules.md#cc202), [#617](https://github.com/commit-check/commit-check/pull/617))
* The tag check in a pre-push hook checks the tag name the remote receives. ([CC401](rules.md#cc401), [#615](https://github.com/commit-check/commit-check/pull/615))

### Fixed

* The Copilot coding agent is recognised. ([CC013](rules.md#cc013), [#632](https://github.com/commit-check/commit-check/pull/632))
* Commit text is printed safely: control characters are escaped, and a line starting with `::` can no longer act as a GitHub Actions command. ([Color and links](example.md#color-and-links), [#620](https://github.com/commit-check/commit-check/pull/620))
* Three slow patterns now run in linear time. ([#626](https://github.com/commit-check/commit-check/pull/626))

## v2.19.1 (2026-10-16) { #v2191 }

### Changed

* `develop` passes the branch check by default. ([CC201](rules.md#cc201), [#612](https://github.com/commit-check/commit-check/pull/612))
* Only merge subjects written by git or a forge skip the message rules; `Merge the parser rewrite` is now checked. ([CC001](rules.md#cc001), [#619](https://github.com/commit-check/commit-check/pull/619))
* The `commit-msg` hook drops git's comment lines and the `git commit -v` diff before checking. ([#618](https://github.com/commit-check/commit-check/pull/618))

### Fixed

* `squash!` and `amend!` commits are rejected like `fixup!` when fixup commits are not allowed. ([CC009](rules.md#cc009), [#613](https://github.com/commit-check/commit-check/pull/613))
* Every WIP form is caught, such as `WIP` followed by a tab or a dash. ([CC010](rules.md#cc010), [#616](https://github.com/commit-check/commit-check/pull/616))
* The sign-off check needs a real `Signed-off-by:` trailer with a name and an address. ([CC012](rules.md#cc012), [#621](https://github.com/commit-check/commit-check/pull/621))
* A `word:` prefix skips the case and mood checks only when it is an allowed commit type. ([CC002](rules.md#cc002), [#622](https://github.com/commit-check/commit-check/pull/622))
* Two more AI co-author forms are recognised, including Cursor Agent's. ([CC013](rules.md#cc013), [#623](https://github.com/commit-check/commit-check/pull/623))
* The config file is found when you run from a subdirectory. ([Where the config file lives](configuration.md#where-the-config-file-lives), [#625](https://github.com/commit-check/commit-check/pull/625))
* A parent config from `inherit_from` larger than 1 MiB is skipped. ([Across an organization](guides/organization.md), [#614](https://github.com/commit-check/commit-check/pull/614))

## v2.19.0 (2026-10-14) { #v2190 }

### Added

* `require_description_grammar` also checks the part after `<type>/`, so `feature/Add_Login` fails. ([CC201](rules.md#cc201), [#581](https://github.com/commit-check/commit-check/pull/581))
* Amp, OpenHands, Factory Droid and Jules are recognised. ([CC013](rules.md#cc013), [#606](https://github.com/commit-check/commit-check/pull/606))
* `--format json` says why a check was skipped. ([When a check is skipped](example.md#when-a-check-is-skipped), [#605](https://github.com/commit-check/commit-check/pull/605))

### Fixed

* The `check-tag` hook checks the tags the push sends, not the tags on `HEAD`. ([#603](https://github.com/commit-check/commit-check/pull/603))
* A tag build on GitHub Actions no longer fails the branch check on the tag name. ([#603](https://github.com/commit-check/commit-check/pull/603))

## v2.18.3 (2026-10-07) { #v2183 }

### Added

* `--fix` corrects mechanical slips in the message file, such as `Fix:` to `fix:`. ([Fixing a message in place](example.md#fixing-a-message-in-place), [#594](https://github.com/commit-check/commit-check/pull/594))
* `--branch` reads the branch name on GitLab, Bitbucket, Azure and Jenkins. ([Other CI](guides/other-ci.md), [#600](https://github.com/commit-check/commit-check/pull/600))
* A misspelt setting is reported with the closest real name. ([Settings nothing reads](configuration.md#settings-nothing-reads), [#593](https://github.com/commit-check/commit-check/pull/593))

## v2.18.2 (2026-09-28) { #v2182 }

### Fixed

* With `--message --branch`, piped input is read only as the message. ([#579](https://github.com/commit-check/commit-check/pull/579))
* The force-push check reports a skip, not a pass, when it has nothing to compare. ([CC301](rules.md#cc301), [#591](https://github.com/commit-check/commit-check/pull/591))

## v2.18.1 (2026-09-24) { #v2181 }

### Changed

* Python 3.15 is supported. Thanks [@itzzdev09](https://github.com/itzzdev09). ([#583](https://github.com/commit-check/commit-check/pull/583))

## v2.18.0 (2026-09-13) { #v2180 }

### Added

* `ai_attribution = "disclose"` accepts AI help disclosed with `Assisted-by:` and writes the fix for you. ([Asking for disclosure instead](guides/policies.md#asking-for-disclosure-instead), [#575](https://github.com/commit-check/commit-check/pull/575))
* A failed check names the rejected value, such as "Subject is 96 characters; it must be at most 80". ([#571](https://github.com/commit-check/commit-check/pull/571))
* Spec names in errors are links in terminals that support them. ([#568](https://github.com/commit-check/commit-check/pull/568))

### Changed

* `forbid` also rejects `Assisted-by:` and `Generated-by:` trailers. ([CC013](rules.md#cc013), [#575](https://github.com/commit-check/commit-check/pull/575))

### Fixed

* `main`, `master` and `develop` must match exactly, so `main-backup` fails. ([CC201](rules.md#cc201), [#569](https://github.com/commit-check/commit-check/pull/569))
* Only subjects git writes itself, such as `Merge ` and `fixup! `, skip the message format check. ([CC001](rules.md#cc001), [#569](https://github.com/commit-check/commit-check/pull/569))
* A regex setting that does not compile names the setting and exits 2. ([Exit codes](troubleshoot.md#exit-codes), [#574](https://github.com/commit-check/commit-check/pull/574))
* A config error exits 2 and names the file; `--dry-run` now runs the checks. ([#570](https://github.com/commit-check/commit-check/pull/570))
* An `inherit_from` that cannot be loaded is reported on stderr. ([#569](https://github.com/commit-check/commit-check/pull/569))

## v2.17.0 (2026-09-06) { #v2170 }

### Added

* A failed check gives the exact fix when there is only one, such as `Use "fix: add x"`, also as `fix` in JSON. ([Reading the JSON](example.md#reading-the-json), [#564](https://github.com/commit-check/commit-check/pull/564))
* `warn = [...]` reports a rule without failing the run. ([Report a rule without enforcing it](configuration.md#report-a-rule-without-enforcing-it), [#565](https://github.com/commit-check/commit-check/pull/565))

### Fixed

* The case check no longer reads the first word of a plain subject as a type. ([CC002](rules.md#cc002), [#564](https://github.com/commit-check/commit-check/pull/564))

## v2.16.0 (2026-08-31) { #v2160 }

### Added

* `--tag` checks tag names, SemVer by default. ([CC401](rules.md#cc401), [#559](https://github.com/commit-check/commit-check/pull/559))
* `--files` checks committed file size, forbidden paths and path length. ([CC302–CC304](rules.md#push-rules), [#560](https://github.com/commit-check/commit-check/pull/560))

## v2.15.1 (2026-08-16) { #v2151 }

### Fixed

* Color is printed only to a terminal, and `NO_COLOR` and `FORCE_COLOR` are honoured. Thanks [@larsch](https://github.com/larsch). ([Color and links](example.md#color-and-links), [#551](https://github.com/commit-check/commit-check/pull/551), [#552](https://github.com/commit-check/commit-check/pull/552))

## v2.15.0 (2026-08-13) { #v2150 }

### Added

* `--rev` checks a given commit, with its recorded author. ([Checking a range of commits](example.md#checking-a-range-of-commits), [#544](https://github.com/commit-check/commit-check/pull/544))

### Changed

* Skipped checks are named on stderr instead of passing in silence. ([When a check is skipped](example.md#when-a-check-is-skipped), [#544](https://github.com/commit-check/commit-check/pull/544))
* Only git's own `Merge ` and `fixup! ` prefixes skip the subject rules.

### Fixed

* The CLI no longer hangs in CI when stdin is open but empty. ([#544](https://github.com/commit-check/commit-check/pull/544))

## v2.14.0 (2026-08-12) { #v2140 }

### Changed

* The imperative check rejects only `fixed`, `adding` or `fixes` forms, so any imperative verb passes. ([CC003](rules.md#cc003), [#540](https://github.com/commit-check/commit-check/pull/540))

## v2.13.1 (2026-08-05) { #v2131 }

### Added

* `--format json` shows the checked value for passing checks too. ([#522](https://github.com/commit-check/commit-check/pull/522))

## v2.13.0 (2026-08-04) { #v2130 }

### Added

* Every rule has a stable ID such as `CC003`, shown in the output and the JSON with a docs link. ([Rules reference](rules.md), [#512](https://github.com/commit-check/commit-check/pull/512))
* `docs/`, `ci/`, `test/`, `refactor/`, `build/`, `perf/` and `style/` branches pass by default. ([#505](https://github.com/commit-check/commit-check/pull/505))

### Changed

* Rule IDs are clickable where the terminal supports links. ([#520](https://github.com/commit-check/commit-check/pull/520))
* The docs moved to commit-check.com; `docs.commit-check.com` links redirect. ([#514](https://github.com/commit-check/commit-check/pull/514))

## v2.12.2 (2026-08-01) { #v2122 }

### Fixed

* AI model names with spaces in co-author trailers are recognised. ([#506](https://github.com/commit-check/commit-check/pull/506))
* More imperative verbs are recognised. ([#496](https://github.com/commit-check/commit-check/pull/496))

## v2.12.1 (2026-07-31) { #v2121 }

### Fixed

* No crash when the package version cannot be read. ([#483](https://github.com/commit-check/commit-check/pull/483))

## v2.12.0 (2026-07-24) { #v2120 }

### Added

* `author_name_pattern` and `author_email_pattern` take your own regex. ([CC101](rules.md#cc101), [#459](https://github.com/commit-check/commit-check/pull/459))

### Fixed

* No crash on Chinese Windows. ([#475](https://github.com/commit-check/commit-check/pull/475))
* The author checks read `git config` first, the identity your next commit will use. ([#461](https://github.com/commit-check/commit-check/pull/461))

## v2.11.1 (2026-07-09) { #v2111 }

### Fixed

* `require_signed_off_by` accepts any name and skips authors in `ignore_authors`. ([#462](https://github.com/commit-check/commit-check/pull/462), [#464](https://github.com/commit-check/commit-check/pull/464))

## v2.11.0 (2026-07-06) { #v2110 }

### Added

* `ai_attribution = "forbid"` rejects commits with known AI tool signatures. ([Policy guides](guides/policies.md#ai-attribution), [#456](https://github.com/commit-check/commit-check/pull/456))

### Fixed

* The rebase check no longer takes `main-staging` for `main`. ([#451](https://github.com/commit-check/commit-check/pull/451))

## v2.10.1 (2026-06-30) { #v2101 }

### Fixed

* WIP is detected in any case. ([#448](https://github.com/commit-check/commit-check/pull/448))
* Brackets and other special characters are allowed in a commit description. ([#447](https://github.com/commit-check/commit-check/pull/447))

## v2.10.0 (2026-06-26) { #v2100 }

### Added

* `dependabot/` and `renovate/` branches pass by default. ([#442](https://github.com/commit-check/commit-check/pull/442))

## v2.9.0 (2026-06-22) { #v290 }

### Added

* AI agent branches `ai/`, `claude/`, `codex/`, `copilot/` and `cursor/` pass by default. ([#438](https://github.com/commit-check/commit-check/pull/438))

## v2.8.1 (2026-06-22) { #v281 }

### Added

* Editors autocomplete `cchk.toml` through SchemaStore. ([#433](https://github.com/commit-check/commit-check/pull/433))

## v2.8.0 (2026-06-13) { #v280 }

### Breaking

* Python 3.10 or newer is required. ([#424](https://github.com/commit-check/commit-check/pull/424))

### Added

* `message_pattern` replaces the Conventional Commits check with your own regex. ([CC001](rules.md#cc001), [#427](https://github.com/commit-check/commit-check/pull/427))

## v2.7.1 (2026-06-08) { #v271 }

### Fixed

* `auto` is accepted as an imperative verb. ([#417](https://github.com/commit-check/commit-check/pull/417))

## v2.7.0 (2026-05-16) { #v270 }

### Added

* `--no-force-push` and the `check-no-force-push` hook block force pushes. ([CC301](rules.md#cc301), [#412](https://github.com/commit-check/commit-check/pull/412))
* `validate_push()` runs the same check from Python. ([#412](https://github.com/commit-check/commit-check/pull/412))
* 156 more imperative verbs are recognised. ([#414](https://github.com/commit-check/commit-check/pull/414))

## v2.6.0 (2026-04-20) { #v260 }

### Added

* `--format json` and the Python API, for scripts and AI agents. ([Output for scripts and CI](example.md#output-for-scripts-and-ci), [#396](https://github.com/commit-check/commit-check/pull/396))
* `--compact` prints one line per failure, and `--no-banner` hides the banner. ([#402](https://github.com/commit-check/commit-check/pull/402))

## v2.5.0 (2026-04-03) { #v250 }

### Added

* `inherit_from` loads a shared config from GitHub, a file or an HTTPS URL. ([Across an organization](guides/organization.md))
* `ignore_authors` also skips a commit whose co-author is listed.
* The author checks read `git config` before the last commit.

## v2.0.0 (2025-10-01) { #v200 }

!!! warning

    Breaking release. Read [Migrating from v1](migration.md) before you upgrade.

### Breaking

* The config moved from `.commit-check.yml` to `cchk.toml` or `commit-check.toml`. ([Migrating from v1](migration.md))
* The hooks `check-commit-signoff`, `check-merge-base` and `check-imperative` and the flags `--signoff`, `--merge-base` and `--imperative` are removed. Use the matching `cchk.toml` settings.
* The modules `author.py`, `branch.py`, `commit.py` and `error.py` are removed. ([#280](https://github.com/commit-check/commit-check/pull/280))

## v0.10.2 (2025-08-26) { #v0102 }

Last release before the big v2.0 changes.

## v0.1.0 (2022-11-02) { #v010 }

Initial release of commit-check.
