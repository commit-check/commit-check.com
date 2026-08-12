# Integrations

Commit Check runs in three places, and all three read the same `cchk.toml`.
That is the point: the rules cannot drift between what a developer sees locally
and what CI enforces.

| Where | Catches problems | Can be bypassed |
|---|---|---|
| [Pre-commit hook](#as-a-pre-commit-hook) | As the message is written | Yes — `--no-verify` |
| [GitHub Actions](#in-github-actions) | On every pull request | No |
| [Organization config](#across-an-organization) | Everywhere at once | — |

A hook gives fast feedback to people who want to follow the policy. The Action
is what makes it a policy. Most projects want both.

## As a pre-commit hook

A pre-commit hook is the cheapest place to enforce commit policy: the developer
finds out while they are still writing the message, not after a CI round trip.

Add Commit Check to `.pre-commit-config.yaml`:

```yaml title=".pre-commit-config.yaml"
repos:
  - repo: https://github.com/commit-check/commit-check
    rev: v2.14.0
    hooks:
      - id: check-message
      - id: check-branch
      - id: check-author-name
      - id: check-author-email
```

Then install the hooks. `check-message` runs at the `commit-msg` stage, so it
needs its own install step:

```console
$ pre-commit install --hook-type commit-msg
$ pre-commit install
```

That is it. The next malformed commit message is rejected before it exists.

!!! warning "If `check-message` never runs"

    It is almost always because `pre-commit install --hook-type commit-msg` was
    not run — a plain `pre-commit install` only wires up the `pre-commit` stage.
    More in [Troubleshooting](../troubleshoot.md).

### Available hooks

| Hook ID | Stage | Rules |
|---|---|---|
| `check-message` | `commit-msg` | [CC001–CC013](../rules.md#commit-message-rules) |
| `check-branch` | `pre-commit` | [CC201–CC202](../rules.md#branch-rules) |
| `check-author-name` | `pre-commit` | [CC101](../rules.md#cc101) |
| `check-author-email` | `pre-commit` | [CC102](../rules.md#cc102) |
| `check-no-force-push` | `pre-push` | [CC301](../rules.md#cc301) |

`check-no-force-push` also needs its own install:

```console
$ pre-commit install --hook-type pre-push
```

### Configuring without a TOML file

Options can be passed as hook arguments, which keeps everything in one file:

```yaml title=".pre-commit-config.yaml"
repos:
  - repo: https://github.com/commit-check/commit-check
    rev: v2.14.0
    hooks:
      - id: check-message
        args:
          - --subject-imperative=true
          - --subject-max-length=72
          - --allow-merge-commits=false
```

A `cchk.toml` is usually the better choice once you have more than a couple of
options, because CI and the CLI read it too. See
[Configuration](../configuration.md) for the precedence rules.

### Skipping a hook

Occasionally you need to get a commit through — a mid-rebase fixup, an
automated migration. `pre-commit` supports this natively:

```console
$ SKIP=check-message git commit -m "wip"
```

!!! warning "Local hooks are not a policy boundary"

    Anyone can pass `--no-verify`. Hooks exist to give fast feedback to people
    who want to follow the policy, not to stop people who don't. Pair them with
    the [GitHub Action](#in-github-actions), which runs where it cannot be
    skipped.

## In GitHub Actions

Local hooks can be skipped. A CI check cannot, which makes GitHub Actions the
place where your policy is actually a policy.

```yaml title=".github/workflows/commit-check.yml"
name: Commit Check

on:
  push:
  pull_request:
    branches: [main]

jobs:
  commit-check:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v7
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          fetch-depth: 0        # (1)!
      - uses: commit-check/commit-check-action@v2
        with:
          message: true
          branch: true
          author-name: true
          author-email: true
```

1. Commit Check needs the full history to inspect every commit in the pull
   request. Without this it only sees the most recent one.

The Action reads the same `cchk.toml` as the CLI, so a repository that already
has one needs no Action-specific configuration.

### Commenting on the pull request

Instead of making contributors open the job log, have the Action post what
needs fixing directly on the PR:

```yaml
      - uses: commit-check/commit-check-action@v2
        with:
          message: true
          branch: true
          pr-comments: ${{ github.event_name == 'pull_request' }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

This needs extra permissions on the job:

```yaml
    permissions:
      contents: read
      pull-requests: write
```

### Reporting without failing

While a team is adopting the policy, it is often better to report problems
without blocking merges. `dry-run` always exits `0`:

```yaml
      - uses: commit-check/commit-check-action@v2
        with:
          message: true
          dry-run: true
```

Turn it off once the history is clean.

### Pull requests from forks

A `pull_request` workflow triggered by a fork receives a **read-only**
`GITHUB_TOKEN`, and `permissions: pull-requests: write` does not override that.
`pr-comments` will therefore fail to post on fork pull requests unless the
repository has *Send write tokens to workflows from pull requests* enabled under
**Settings → Actions → General**.

!!! warning "Do not reach for `pull_request_target` casually"

    `pull_request_target` does get a write token, but it runs in the context of
    the base repository with access to its secrets. Checking out and executing
    the fork's code under that trigger is the "pwn request" pattern and hands
    repository access to anyone who can open a pull request.

    If you use it, check out the base branch only and never run code from the
    pull request.

The checks themselves still run on fork pull requests and still fail the build;
only the commenting is affected.

## Across an organization

Copying `cchk.toml` into forty repositories works until the day you want to
change it. `inherit_from` lets each repository pull a shared base config and
override only what it genuinely needs.

### The shared config

Put the policy in a repository every project can read — GitHub's `.github`
repository is the conventional home:

```toml title="my-org/.github → cchk.toml"
[commit]
conventional_commits = true
subject_imperative = true
subject_max_length = 72
allow_merge_commits = false

[branch]
conventional_branch = true
allow_branch_types = ["feature", "bugfix", "hotfix", "release", "chore"]
```

### Inheriting it

Each repository then needs one line:

```toml title="any-repo → .github/cchk.toml"
inherit_from = "github:my-org/.github:cchk.toml"
```

Local settings win, so a project with a different constraint overrides just that
one option:

```toml title="a-repo-with-longer-subjects → .github/cchk.toml"
inherit_from = "github:my-org/.github:cchk.toml"

[commit]
subject_max_length = 100      # everything else comes from the org config
```

### Pinning the version

By default the shorthand resolves to the parent repository's default branch,
which means a change to the org config takes effect everywhere on the next run.
That is usually what you want. When it isn't, pin to a ref:

```toml
inherit_from = "github:my-org/.github@v1:cchk.toml"
```

### Other sources

=== "GitHub shorthand"

    ```toml
    inherit_from = "github:my-org/.github:cchk.toml"
    ```

=== "Local path"

    ```toml
    inherit_from = "../../shared/org-cchk.toml"
    ```

    Useful in a monorepo, where the shared config is already checked out.

=== "HTTPS URL"

    ```toml
    inherit_from = "https://example.com/shared/cchk.toml"
    ```

    Plain HTTP is rejected.

!!! warning "Inheritance fails open"

    If the parent config is unreachable — a network blip, a renamed file, a
    private repository — Commit Check silently falls back to the local config
    rather than failing the build. This keeps CI green during an outage, but it
    also means a typo in `inherit_from` is easy to miss. Verify the merged
    result when you first set it up:

    ```console
    $ commit-check --message --format json
    ```

### Rolling it out

Turning on a strict policy across an organization at once produces a wall of
red. A gentler sequence:

1. Ship the org config with [`dry-run`](#reporting-without-failing) enabled in
   CI, so violations are reported but nothing blocks.
2. Look at what actually fails. Some rules will turn out to be wrong for some
   teams — that is information, not an obstacle.
3. Turn off `dry-run` for repositories whose history is already clean.
4. Tighten the shared config over time.
