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
          fetch-depth: 0        # recommended, see below
      - uses: commit-check/commit-check-action@v2
        with:
          message: true
          branch: true
          author-name: true
          author-email: true
```

`fetch-depth: 0` is recommended, not required: the Action then reads the pull
request's commits from the clone. With a shallow clone it lists them through
the GitHub API instead (up to 250), and if it cannot, it warns and checks the
head commit alone.

The Action reads the same `cchk.toml` as the CLI, so a repository that already
has one needs no Action-specific configuration.

!!! note "Python 3.11 or newer"

    The Action runs on the runner's own Python, and since v2.19.0 it needs
    3.11 or newer. The `*-latest` GitHub-hosted runners have it.
    `ubuntu-22.04` ships 3.10, so add a setup step before the Action there:

    ```yaml
    - uses: actions/setup-python@v7
      with:
        python-version: "3.11"
    ```

## Inputs

| Input | Default | What it does |
|---|---|---|
| `message` | `true` | Check every commit message of the pull request |
| `branch` | `true` | Check the branch name |
| `author-name` | `false` | Check each commit's author name |
| `author-email` | `false` | Check each commit's author email |
| `files` | `false` | Check the files each commit changes against the [`[files]` rules](../rules.md#push-rules) of `cchk.toml` (size, prohibited paths, path length). Needs `fetch-depth: 0`: a commit the clone holds without its parent is skipped. Since v2.24.0 |
| `pr-title` | `false` | Check the pull request title, the one that matters for squash merges, against the message rules a one-line title can meet: every `message` rule except a body (CC011), a sign-off (CC012) and an AI author (CC017). Pull request events only |
| `message-ai-attribution` | `false` | Check every commit against the [AI rules](policies.md#checking-ai-attribution-and-nothing-else) of `cchk.toml` (`ai_attribution`) only, author included, without the format rules. Takes the place of `message` |
| `pr-body-ai-attribution` | `false` | Check the [pull request description](policies.md#checking-a-pull-request-description) against the AI rules of `cchk.toml`, and its [AI declaration boxes](../rules.md#cc501) when `[pull_request] ai_declaration_checkboxes` is set. Pull request events only |
| `ai-label` | `false` | Label the pull request when an AI tool wrote any of it (a commit, the description, or an agent's app that opened it): `true` for `ai-assisted`, or the label's name. Labels are only added, never removed. Needs `pull-requests: write`; skipped on fork pull requests under `pull_request` |
| `pr-comments` | `false` | Post the report as a pull request comment, edited in place on later runs. Needs `pull-requests: write`; skipped on fork pull requests |
| `job-summary` | `true` | Write the report to the job summary |
| `dry-run` | `false` | Report failures as warnings and always exit `0` |
| `config-source` | `head` | Where a pull request run reads `cchk.toml`: `head`, the checked-out files, or `base`, the base branch, so a pull request cannot loosen the rules it is checked against. See [below](#config-source). Since v2.25.0 |

`pull_request` does not fire when a title or description is edited. With
`pr-title` or `pr-body-ai-attribution`, add
`types: [opened, synchronize, reopened, edited]` to re-check an edited pull
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

## Checking against the base branch's config { #config-source }

By default the Action reads `cchk.toml` from the checkout, which on a pull
request is the pull request's own copy. A pull request that edits the config
is then checked against its edit: it can drop a rule and pass the very check
the rule was for.

With `config-source: base`, a pull request is checked against the config on
its base branch instead, as CODEOWNERS is. A config change takes effect once it
merges:

```yaml
      - uses: commit-check/commit-check-action@v2
        with:
          message: true
          branch: true
          config-source: base
```

- A pull request that changes or adds the config gets a notice saying the
  change applies after it merges.
- A parent named by a local path in `inherit_from` is read from the base
  branch too. A `github:` or HTTPS parent is fetched as usual.
- If the base branch cannot be read, the step fails rather than fall back to
  the pull request's config.
- On a push or any event other than a pull request, the setting has no
  effect, and the Action says so in a notice.

The config file is only half of it. Under `pull_request` the workflow file
also comes from the pull request, so its inputs and `CCHK_*` variables can be
changed the same way. Protect `.github/` with a CODEOWNERS review as well.

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
