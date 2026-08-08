# Configuration

Commit Check reads its settings from four places. When the same option is set
in more than one, the first one listed wins:

1. **Command-line arguments** — `--subject-imperative=true`
2. **Environment variables** — `CCHK_SUBJECT_IMPERATIVE=true`
3. **A configuration file** — `cchk.toml` or `commit-check.toml`
4. **Built-in defaults**

That ordering is what makes the layering useful: the file carries the policy
the project agreed on, the environment overrides it for a single CI job, and a
flag overrides both for a single run.

!!! tip "Defaults are not "nothing""

    Two different things decide whether a rule fires: whether you asked for
    that check at all, and what the option defaults to. A check only runs when
    its flag is passed — `--message` never evaluates branch rules — but once a
    check is running, these apply with no configuration file present:

    | Check | Enforced by default |
    |---|---|
    | `--message` | Conventional Commits ([CC001](rules.md#cc001)), subject lengths of 5–80 characters ([CC004](rules.md#cc004), [CC005](rules.md#cc005)), and an allow-list of ten commit types |
    | `--branch` | Conventional Branch ([CC201](rules.md#cc201)) and an allow-list of twenty-one branch types |
    | `--author-name` / `--author-email` | The built-in name and email patterns ([CC101](rules.md#cc101), [CC102](rules.md#cc102)) |

    Off until you turn them on: subject capitalization, imperative mood,
    required body and signoff, and rebase requirements.

    The `allow_*` options are a mix, so read them individually rather than
    assuming: `allow_commit_types` and `allow_branch_types` are allow-lists
    that restrict from the start, while `allow_merge_commits`,
    `allow_revert_commits`, `allow_empty_commits`, `allow_fixup_commits`,
    `allow_wip_commits` and `allow_force_push` all default to permitting
    everything. The *Default* column in the
    [rules reference](rules.md#rule-index) is the full picture.

## Where the config file lives

The file is TOML, and may be called `cchk.toml` or `commit-check.toml`. Commit
Check searches four locations and uses the first that exists:

1. `cchk.toml`
2. `commit-check.toml`
3. `.github/cchk.toml`
4. `.github/commit-check.toml`

Pass `--config` to point at one directly and skip the search:

```console
$ commit-check --config path/to/cchk.toml --message
```

!!! tip "Why `.github/`"

    Putting the file in `.github/` keeps the repository root uncluttered and
    matches where Dependabot and Renovate already keep theirs. Commit Check
    treats both locations identically.

!!! tip "Editor autocompletion"

    The TOML schema is published on [SchemaStore](https://www.schemastore.org/),
    so VS Code (via
    [Even Better TOML](https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml)),
    PyCharm and IntelliJ offer completion, validation and inline documentation
    for `cchk.toml` with nothing to configure.

## Inheriting a shared config

An organization can keep one base policy and have every repository build on it.
Point `inherit_from` at the shared file; the parent loads first, and anything
set locally overrides it. The key itself is never passed to the validation
engine.

```toml title=".github/cchk.toml"
inherit_from = "github:my-org/.github:cchk.toml"

[commit]
subject_max_length = 72  # overrides whatever the parent set
```

The value can be a GitHub shorthand, a local path or an HTTPS URL:

| Form | Example |
|---|---|
| GitHub, default branch | `github:owner/repo:path/to/cchk.toml` |
| GitHub, pinned branch | `github:owner/repo@main:path/to/cchk.toml` |
| Local file | `../../shared/org-cchk.toml` |
| HTTPS URL | `https://example.com/shared/cchk.toml` |

!!! note "Inheritance fails quietly"

    If the target is unreachable or the format is not recognized, Commit Check
    ignores the inheritance and uses the local configuration alone. Plain HTTP
    URLs are rejected outright. A repository that silently stops inheriting
    still passes its own checks, so pin the branch when the policy matters.

## A worked example

Every line below that differs from the built-in default is marked, so it is
clear what this file is actually changing:

```toml title="cchk.toml"
[commit]
# https://www.conventionalcommits.org
conventional_commits = true
# message_pattern = ""             # optional: a custom regex, replacing the above
subject_capitalized = false
subject_imperative = true          # changed: off by default
subject_max_length = 80
subject_min_length = 5
# changed: a subset of the default list, which also has perf, build and ci
allow_commit_types = ["feat", "fix", "docs", "style", "refactor", "test", "chore"]
allow_merge_commits = true
allow_revert_commits = true
allow_empty_commits = false        # changed: allowed by default
allow_fixup_commits = true
allow_wip_commits = false          # changed: allowed by default
require_body = false
require_signed_off_by = false
ai_attribution = "forbid"          # changed: "ignore" by default
# ignore_authors = []              # optional: bypass all commit checks for these authors

[push]
allow_force_push = true            # set false to block force pushes

[branch]
# https://conventionalbranch.org
conventional_branch = true
# changed: spec types only. The default is a superset — these plus the
# Conventional Commit types, AI agent prefixes and bot prefixes — so setting
# this at all narrows it. Omit the line to accept all of them.
allow_branch_types = ["feature", "bugfix", "hotfix", "release", "chore"]
# allow_branch_names = []          # optional: extra standalone names, e.g. ["develop"]
# require_rebase_target = "main"   # optional: no rebase requirement by default
# ignore_authors = []              # optional: as above, for branch checks
```

!!! warning "`allow_*` options describe what is permitted"

    They read backwards from most linters. `allow_wip_commits = false` is the
    setting that *rejects* WIP commits; leaving it at its default of `true`
    lets them through.

## Command-line arguments

Every option can be set as a flag, which is what makes a TOML file optional
entirely — useful when the policy lives in `.pre-commit-config.yaml` instead.

| Type | Form |
|---|---|
| Boolean | `--option-name=true` / `--option-name=false` |
| Integer | `--option-name=80` |
| List | `--option-name=value1,value2,value3` |
| String | `--option-name=value` |

```console
$ commit-check --message --subject-imperative=false
$ commit-check --message --subject-max-length=72
$ commit-check --message --allow-commit-types=feat,fix,docs
$ commit-check --branch --allow-branch-types=feature,bugfix,hotfix
```

Used from a hook definition, with no config file anywhere in the repository:

```yaml title=".pre-commit-config.yaml"
repos:
  - repo: https://github.com/commit-check/commit-check
    rev: v2.13.4
    hooks:
      - id: check-message
        args:
          - --subject-imperative=false
          - --subject-max-length=100
          - --allow-merge-commits=false
```

## Environment variables

Any option can also be set through the environment, which is the practical way
to vary policy per CI job without editing the file. Uppercase the option name,
replace hyphens with underscores, and prefix `CCHK_`:

```console
$ export CCHK_SUBJECT_MAX_LENGTH=72
$ export CCHK_ALLOW_COMMIT_TYPES=feat,fix,docs,chore
$ CCHK_SUBJECT_MAX_LENGTH=100 commit-check --message
```

The full mapping between the three forms:

| TOML Config | Environment Variable | CLI Argument |
|---|---|---|
| `conventional_commits = true` | `CCHK_CONVENTIONAL_COMMITS=true` | `--conventional-commits=true` |
| `message_pattern = "^PROJ-\\d+: .+"` | `CCHK_MESSAGE_PATTERN=^PROJ-\\d+: .+` | N/A (config file only) |
| `subject_capitalized = false` | `CCHK_SUBJECT_CAPITALIZED=false` | `--subject-capitalized=false` |
| `subject_imperative = true` | `CCHK_SUBJECT_IMPERATIVE=true` | `--subject-imperative=true` |
| `subject_max_length = 80` | `CCHK_SUBJECT_MAX_LENGTH=80` | `--subject-max-length=80` |
| `subject_min_length = 5` | `CCHK_SUBJECT_MIN_LENGTH=5` | `--subject-min-length=5` |
| `allow_commit_types = ["feat", "fix"]` | `CCHK_ALLOW_COMMIT_TYPES=feat,fix` | `--allow-commit-types=feat,fix` |
| `allow_merge_commits = true` | `CCHK_ALLOW_MERGE_COMMITS=true` | `--allow-merge-commits=true` |
| `allow_revert_commits = true` | `CCHK_ALLOW_REVERT_COMMITS=true` | `--allow-revert-commits=true` |
| `allow_empty_commits = false` | `CCHK_ALLOW_EMPTY_COMMITS=false` | `--allow-empty-commits=false` |
| `allow_fixup_commits = true` | `CCHK_ALLOW_FIXUP_COMMITS=true` | `--allow-fixup-commits=true` |
| `allow_wip_commits = false` | `CCHK_ALLOW_WIP_COMMITS=false` | `--allow-wip-commits=false` |
| `require_body = false` | `CCHK_REQUIRE_BODY=false` | `--require-body=false` |
| `require_signed_off_by = false` | `CCHK_REQUIRE_SIGNED_OFF_BY=false` | `--require-signed-off-by=false` |
| `ignore_authors = ["bot"]` | `CCHK_IGNORE_AUTHORS=bot,user` | `--ignore-authors=bot,user` |
| `author_email_pattern=^.+@example\.com$` | `CCHK_AUTHOR_EMAIL_PATTERN=^.+@example\.com$` | `--author-email-pattern=^.+@example\.com$` |
| `author_name_pattern=^.+ .+$` | `CCHK_AUTHOR_NAME_PATTERN=^.+ .+$` | `--author-name-pattern=^.+ .+$` |
| `conventional_branch = true` | `CCHK_CONVENTIONAL_BRANCH=true` | `--conventional-branch=true` |
| `allow_branch_types = ["feature"]` | `CCHK_ALLOW_BRANCH_TYPES=feature,bugfix` | `--allow-branch-types=feature,bugfix` |
| `allow_branch_names = ["develop"]` | `CCHK_ALLOW_BRANCH_NAMES=develop,staging` | `--allow-branch-names=develop,staging` |
| `require_rebase_target = "main"` | `CCHK_REQUIRE_REBASE_TARGET=main` | `--require-rebase-target=main` |
| `allow_force_push = true` | `CCHK_ALLOW_FORCE_PUSH=true` | `--no-force-push` (sets `allow_force_push` to `false`) |
| `ai_attribution = "forbid"` | `CCHK_AI_ATTRIBUTION=forbid` | `--ai-attribution=forbid` |
| `ignore_authors = ["bot"]` (in branch section) | `CCHK_BRANCH_IGNORE_AUTHORS=bot,user` | `--branch-ignore-authors=bot,user` |

## Which value wins

The four sources layer, so the same option can be set in several at once. Only
the highest-priority one takes effect:

```console
$ grep subject_max_length cchk.toml
subject_max_length = 100

$ export CCHK_SUBJECT_MAX_LENGTH=80

$ commit-check --message --subject-max-length=50
```

The limit applied is 50 — the flag beats the environment, which beats the file.
Nothing warns about the values that lost, which is worth remembering when a
setting in the file appears to have no effect.

## Every option

Types are as TOML understands them. A default shown as `""` means the option is
unset, which is never the same as the check being off — but it does not mean
the same thing twice, so read the description rather than the cell:

- `message_pattern` unset leaves `conventional_commits` to generate the
  pattern. [CC001](rules.md#cc001) still runs.
- `author_name_pattern` unset falls back to the built-in name pattern.
  [CC101](rules.md#cc101) still runs.
- `require_rebase_target` unset is the one case where the check really does not
  run — there is no branch to compare against.

| Section | Option | Type | Default | Description |
|---|---|---|---|---|
| commit | conventional_commits | bool | true | Enforce Conventional Commits specification. |
| commit | message_pattern | str | "" (no custom pattern) | Custom regex pattern for commit message validation.  When set, this pattern replaces the auto-generated Conventional Commits regex entirely, making it possible to enforce custom formats such as JIRA smart commits (e.g., `"^PROJ-\\d+: .+"`).  When `message_pattern` is set (non-empty) it takes precedence over `conventional_commits`. |
| commit | subject_capitalized | bool | false | Subject must start with a capital letter. |
| commit | subject_imperative | bool | false | Subject must be in imperative mood. Forms of verbs can be found at [imperatives.py](https://github.com/commit-check/commit-check/blob/main/commit_check/imperatives.py) |
| commit | subject_max_length | int | 80 | Maximum length of the subject line. |
| commit | subject_min_length | int | 5 | Minimum length of the subject line. |
| commit | allow_commit_types | list[str] | ["feat", "fix", "docs", "style", "refactor", "test", "chore", "perf", "build", "ci"] | Allowed commit types when conventional_commits is true. |
| commit | allow_merge_commits | bool | true | Allow merge commits. |
| commit | allow_revert_commits | bool | true | Allow revert commits. |
| commit | allow_empty_commits | bool | true | Allow empty commits. |
| commit | allow_fixup_commits | bool | true | Allow fixup commits (e.g., "fixup! <commit message>"). |
| commit | allow_wip_commits | bool | true | Allow work-in-progress commits (e.g., "WIP: <commit message>"). |
| commit | require_body | bool | false | Require a body in the commit message. |
| commit | ignore_authors | list[str] | [] (none ignored) | List of commit authors **or co-authors** (`Co-authored-by:` lines) to bypass all commit checks. Useful for bots (e.g., `"dependabot[bot]"`, `"coderabbitai[bot]"`). |
| commit | author_email_pattern | str | `^.+@.+$` | Custom regex for the author email check. When empty, the built-in default pattern is used. This option only takes effect when the author_email check is enabled (`-e` / `--author-email`). |
| commit | author_name_pattern | str | "" (built-in default) | Custom regex for the author name check. When empty, the built-in default pattern is used (it is not disabled). This option only takes effect when the author_name check is enabled (`-n` / `--author-name`). |
| commit | require_signed_off_by | bool | false | Require "Signed-off-by" line in the commit message footer. |
| commit | ai_attribution | str | "ignore" | AI attribution policy. `"forbid"` rejects any commit containing known AI tool signatures (Claude Code, Copilot, Codex, Gemini, Cursor, Devin, Aider, Windsurf, Tabby, and generic AI model patterns). `"ignore"` disables the check. This feature is a response to the industry-wide discussion on AI disclosure in open source (Linux kernel `Assisted-by:` trailer, CPython, VS Code, Apache, Fedora policies). |
| branch | conventional_branch | bool | true | Enforce Conventional Branch specification. |
| branch | allow_branch_types | list[str] | ["feature", "bugfix", "hotfix", "release", "chore", "feat", "fix", "build", "ci", "docs", "perf", "refactor", "style", "test", "ai", "claude", "codex", "copilot", "cursor", "dependabot", "renovate"] | Allowed branch types when `conventional_branch` is true. The default is a superset of the [Conventional Branch spec](https://conventionalbranch.org/): the spec types (`feature`, `bugfix`, `hotfix`, `release`, `chore`) plus the Conventional Commit types (`build`, `ci`, `docs`, `perf`, `refactor`, `style`, `test`), AI agent prefixes (`ai`, `claude`, `codex`, `copilot`, `cursor`) and bot prefixes (`dependabot`, `renovate`). For strict spec-only validation, set this option explicitly (e.g. `["feature", "bugfix", "hotfix", "release", "chore"]`). |
| branch | allow_branch_names | list[str] | [] (empty list) | Additional standalone branch names allowed when conventional_branch is true (e.g., ["develop", "staging"]). By default, master, main, HEAD, and PR-* are always allowed. |
| branch | require_rebase_target | str | "" (no requirement) | Target branch for rebase requirement. If not set, no rebase validation is performed. |
| push | allow_force_push | bool | true | Allow force pushes. Set to `false` to block force pushes when used as a pre-push hook or with `--no-force-push`. |
| branch | ignore_authors | list[str] | [] (none ignored) | List of authors to ignore (i.e., always allow). |
