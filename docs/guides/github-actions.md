# GitHub Action

A local hook can be skipped with `git commit --no-verify`. The Action runs in
CI whatever happened locally, and once it is a
[required status check](#making-it-a-required-check) a pull request that
fails it cannot merge.

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

## Making it a required check { #making-it-a-required-check }

Until it is required, a failing Commit Check does not stop anyone from
merging. Require it in the branch's ruleset or branch protection, where the
repository's plan allows one. GitHub names an Action's check after its job, so
with the workflow above the check to require is `commit-check`.

## Commenting on the pull request

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

## Reporting without failing

While a team is adopting the policy, it is often better to report problems
without blocking merges. `dry-run` always exits `0`:

```yaml
      - uses: commit-check/commit-check-action@v2
        with:
          message: true
          dry-run: true
```

Turn it off once the history is clean.

## Pull requests from forks

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
