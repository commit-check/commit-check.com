---
date:
  created: 2026-06-21
readtime: 7
categories:
  - UPDATES
tags:
  - commit-check
  - configuration
authors:
  - shenxianpeng
---

# From zero-config to org-wide policy

Commit Check works the moment you install it, but its real strength shows up
when you start shaping the policy to fit your team. This post covers everything from the default behavior to organization-wide
shared configuration.

<!-- more -->

## Three places to configure

Commit Check resolves configuration in order of priority:

1. **Command-line arguments** — override settings for a single run
2. **Environment variables** — `CCHK_*` variables, ideal for CI
3. **Configuration files** — `cchk.toml` or `commit-check.toml`

If none of these exist, the lenient defaults apply: Conventional Commits for
messages, Conventional Branch for branch names.

## A real `cchk.toml`

Drop a `cchk.toml` (or `.github/cchk.toml`) in your repository root to take
control:

```toml
[commit]
# https://www.conventionalcommits.org
conventional_commits = true
subject_imperative = true
subject_max_length = 80
subject_min_length = 5
allow_commit_types = ["feat", "fix", "docs", "style", "refactor", "test", "chore", "ci"]
allow_merge_commits = true
allow_wip_commits = false
require_signed_off_by = false
# Bypass checks for bot/automation authors and co-authors:
ignore_authors = ["dependabot[bot]", "renovate[bot]", "copilot[bot]"]

[branch]
# https://conventional-branch.github.io/
conventional_branch = true
allow_branch_types = ["feature", "bugfix", "hotfix", "release", "chore", "feat", "fix"]
```

Every field maps to a rule that runs at commit, push, or CI time. Because the
file lives in your repo, the policy is reviewed and versioned like code.

!!! tip "IDE autocompletion comes for free"
    Commit Check's TOML schema is published on
    [SchemaStore](https://www.schemastore.org/), so editors like VS Code (via
    *Even Better TOML*), PyCharm, and IntelliJ give you autocompletion,
    validation, and inline docs for `cchk.toml` — no manual schema path needed.

## CLI and environment overrides

For one-off checks or pipeline tweaks, skip the file entirely:

```bash
# Override per run
commit-check --message --subject-imperative=true --subject-max-length=72

# Or via environment variables
export CCHK_SUBJECT_IMPERATIVE=true
export CCHK_SUBJECT_MAX_LENGTH=72
commit-check --message
```

The same overrides work inside pre-commit hook `args`, so a single repo can
loosen a shared rule without forking the whole policy.

## Share one policy across many repos

`inherit_from` is the feature that makes Commit Check work across an
organization. Point each repository at a base config and override only what
differs:

```toml
# .github/cchk.toml — inherit the org base, then adjust locally
inherit_from = "github:my-org/.github:cchk.toml"

[commit]
subject_max_length = 72  # local override wins
```

`inherit_from` accepts several sources:

- **GitHub shorthand:** `github:owner/repo:path/to/cchk.toml`
- **Pinned to a ref:** `github:owner/repo@main:path/to/cchk.toml`
- **Local path:** `../shared/cchk.toml`
- **HTTPS URL:** `https://example.com/cchk.toml`

The `github:` shorthand fetches from `raw.githubusercontent.com`, and plain
HTTP URLs are rejected for security. Local settings always override the
inherited base — so the org sets the floor, and each repo customizes from
there.

## Don't forget push safety

Policy isn't only about message wording. Use `--no-force-push` in a `pre-push`
hook to catch history-rewriting pushes:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/commit-check/commit-check
    rev: v2.6.0
    hooks:
      - id: check-no-force-push
        stages: [pre-push]
```

A note: piping `git push` into `commit-check` is **not** a prevention
mechanism — by then the push has already started. Use the `pre-push` hook
instead.

## Summary

Start with zero config, add a `cchk.toml` when you want stricter rules, and
reach for `inherit_from` when you want one standard across every repository.
Same engine, same file format, scaling with your team.

Full reference: <https://commit-check.com/configuration/>
