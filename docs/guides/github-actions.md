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

1. Recommended, not required: the Action then reads the pull request's
   commits from the clone. With a shallow clone it lists them through the
   GitHub API instead (up to 250), and if it cannot, it warns and checks the
   head commit alone.

The Action reads the same `cchk.toml` as the CLI, so a repository that already
has one needs no Action-specific configuration.

## Inputs

| Input | Default | What it does |
|---|---|---|
| `message` | `true` | Check every commit message of the pull request |
| `branch` | `true` | Check the branch name |
| `author-name` | `false` | Check each commit's author name |
| `author-email` | `false` | Check each commit's author email |
| `pr-title` | `false` | Check the pull request title against Conventional Commits, the one that matters for squash merges. Pull request events only |
| `pr-comments` | `false` | Post the report as a pull request comment, edited in place on later runs |
| `job-summary` | `true` | Write the report to the job summary |
| `dry-run` | `false` | Report failures as warnings and always exit `0` |

`pull_request` does not fire when a title is edited. With `pr-title: true`,
add `types: [opened, synchronize, reopened, edited]` to re-check a renamed pull
request.

The Action also sets a `result` output: the check results as JSON, read with
`fromJSON(steps.<id>.outputs.result)`. Its `status` is `pass`, `warn`, `skip`
or `fail`, and each scope carries the same per-check fields as
`commit-check --format json`.

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
```

The Action posts with the workflow's own token, so no `GITHUB_TOKEN` needs to
be passed in. It does need extra permissions on the job:

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
On such a run the Action skips the comment with a warning and says so in the
job summary; the check, the annotations and the summary still work. For
feedback on fork pull requests themselves, use the [GitHub App](github-app.md),
which is not bound by the workflow's token.

!!! warning "Do not reach for `pull_request_target` casually"

    `pull_request_target` does get a write token, but it runs in the context of
    the base repository with access to its secrets. Checking out and executing
    the fork's code under that trigger is the "pwn request" pattern and hands
    repository access to anyone who can open a pull request.

    If you use it, check out the base branch only and never run code from the
    pull request.

The checks themselves still run on fork pull requests and still fail the build;
only the commenting is affected.
