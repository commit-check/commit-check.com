# With release tools

release-please, semantic-release, git-cliff and `cz bump` read your commit
messages to decide the next version and write the changelog. A commit they
cannot parse is not an error to them: it is left out of the changelog, or it
does not count toward a release. Commit Check is the gate in front of them,
so what they read always parses.

## Check the message the tool will read

Which message that is depends on how pull requests are merged.

- **Merge commits or rebase.** Every commit on the branch lands on `main`, and
  the release tool reads each one. Check each one: the
  [pre-commit hook](pre-commit.md) while it is written, and the
  [Action](github-actions.md) with its default `message: true` on the pull
  request.
- **Squash merge.** The branch's commits are thrown away, and the pull
  request title becomes the commit on `main`. release-please, for one,
  "highly recommend[s]" squash merges. Check the title: `pr-title: true` on
  the Action, or `check = "squash"` on the [App](github-app.md#pull-requests),
  which checks the full message a squash merge would land. With GitHub's
  default squash message, a pull request of a single commit lands that
  commit's message rather than the title. The App follows that setting; with
  the Action, set the squash commit message to "Pull request title" in the
  repository settings so the title you check is the one that lands.

```yaml title=".github/workflows/commit-check.yml"
name: Commit Check

on:
  pull_request:
    types: [opened, edited, synchronize, reopened]

jobs:
  commit-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: commit-check/commit-check-action@v2
        with:
          message: false  # the branch's commits do not reach main
          pr-title: true
```

The default [commit types](../configuration.md) are the Conventional Commits
ones the tools release on (`feat`, `fix`, `perf`) plus the ones they record
without releasing. A breaking change written as `feat!:` or `feat(api)!:`
passes, and so does a `BREAKING CHANGE:` footer.

## Let the tool's own pull request through

release-please and changesets open their release pull request from a branch
whose name you cannot choose:

| Tool | Branch | Default title |
|---|---|---|
| release-please | `release-please--branches--main`, plus `--components--<name>` in a monorepo | `chore(main): release 1.2.3` |
| [changesets/action](https://github.com/changesets/action) | `changeset-release/main` | `Version Packages` |

Commit Check 2.19.4 rejects both branch names under
[CC201](../rules.md#cc201). Allow them:

```toml title="cchk.toml"
[branch]
allow_branch_names = ["release-please--branches--.+", "changeset-release/.+"]
```

Each entry is a regular expression that has to match the whole branch name,
so these allow the tools' branches and nothing that merely contains them.
[commit-check#648](https://github.com/commit-check/commit-check/pull/648)
accepts both names by default; once it is released, this section is no longer
needed.

release-please's title passes [CC001](../rules.md#cc001) as it is.
changesets' `Version Packages` does not, so with `pr-title: true` give it a
Conventional Commits title and commit message:

```yaml
- uses: changesets/action@v1
  with:
    commit-message: "chore: version packages"
    pr-title: "chore: version packages"
```

## Per tool

| Tool | What it reads | Notes |
|---|---|---|
| [release-please](https://github.com/googleapis/release-please) | Conventional Commits on the release branch since the last release | Branch name above. Its README recommends squash merges, so check the title. |
| [semantic-release](https://github.com/semantic-release/semantic-release) | Commits since the last release, with the Angular preset by default | The Angular types are Commit Check's defaults. |
| [git-cliff](https://github.com/orhun/git-cliff) | Commits, parsed as Conventional Commits when `conventional_commits = true` in `cliff.toml` | With `filter_unconventional = true`, a commit that does not parse is dropped from the changelog without a word. |
| [Commitizen](https://commitizen-tools.github.io/commitizen/) `cz bump` | Conventional Commits since the last tag | Commitizen has its own `cz check`. Commit Check adds branch names, authors, sign-off and the App, from one config. |
| [changesets](https://github.com/changesets/changesets) | Changeset files, not commit messages | Only its branch name and PR title matter here, both above. |
