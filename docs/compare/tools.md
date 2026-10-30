# Compared with other tools

What else checks commit messages, branch names and pull request titles on
GitHub, what each one does, and when it is the better choice. Prices and
features are as the projects list them in September and October 2026; follow the links
for the current state. GitHub's own rulesets are on
[their own page](github-rules.md).

## The field

| Tool | What it is | What it checks | Where it runs | Price |
|---|---|---|---|---|
| [commitlint](https://commitlint.js.org/) with [commitlint-github-action](https://github.com/wagoid/commitlint-github-action) | The reference Conventional Commits linter in the JavaScript world: shared configs, plugins, a [commitizen](https://commitizen.github.io/cz-cli/) prompt | Commit messages | Node hook (husky), CI Action | Free, open source |
| [gitlint](https://github.com/jorisroovers/gitlint) | A Python commit message linter with a `commit-msg` hook, configured in a `.gitlint` file; one of the two commit linters the [pre-commit hooks page](https://pre-commit.com/hooks.html) features. Its latest release, 0.19.1, is from March 2023, and its [PyPI page](https://pypi.org/project/gitlint/) says the maintainer is looking for co-maintainers | Commit messages: title and body length, whitespace, required words, regexes; Conventional Commits and sign-off as opt-in rules | Git hook, pre-commit, CLI | Free, open source |
| [action-semantic-pull-request](https://github.com/amannn/action-semantic-pull-request) | The most-used pull request title check; Electron, Vite and Vercel run it | The pull request title (optionally the single commit, for squash merges) | GitHub Action | Free, open source |
| [Semantic PRs](https://github.com/Ezard/semantic-prs) | A GitHub App with the same idea: type and scope on the title or the commits | Pull request title or commits | GitHub App | Free, open source |
| [commitcheck](https://github.com/marketplace/commitcheck) | A hosted App that applies one regular expression, set in its web admin | Commit message, pull request title or description, by regex | GitHub App | Free for public repositories; $25 a month for private ones |
| [DCO app](https://github.com/apps/dco) and [DCO-2](https://github.com/cncf/dco2) | The sign-off check the Linux kernel and the CNCF use, with a remediation flow for missing sign-offs | `Signed-off-by` trailers | GitHub App | Free, open source |
| [PRLint](https://github.com/ewolfe/prlint), [PR Title Checker](https://github.com/marketplace/actions/pr-title-checker) | Regular expressions over pull request fields | Title, body, labels, branch | App / Action | Free, open source |
| **Commit Check** | One rule engine, [documented rule by rule](../rules.md), run as a hook, a CLI, an Action, a hosted App or an MCP tool | Commit message, branch name, author name and email, sign-off, AI attribution, force pushes, file size and paths, tag names; the pull request title (Action) and the squash message of a pull request (App) | All of the above | Free, open source; the App's private organization repositories move to a paid plan later |

## What is different about Commit Check

- **One config, every place it runs.** The same `cchk.toml` drives the
  [pre-commit hook](../guides/pre-commit.md), the [Action](../guides/github-actions.md),
  the [App](../guides/github-app.md) and the [MCP server](../guides/mcp.md).
  The others cover one place each: commitlint is a Node hook and an Action;
  the title checkers are Actions or Apps; commitcheck is an App.
- **More than the message.** Branch names, author identity, sign-off, AI
  attribution trailers, force pushes and file rules are rules, not separate
  tools to find and wire up.
- **A failure explains itself.** Every rule has a stable ID, a one-line error,
  a suggestion and a documentation page, and the Action and App show all of
  it where the failure is. A regex tool reports a mismatch.
- **Squash-aware.** The App can check the message a squash merge would land,
  built from the repository's merge settings, rather than every commit on the
  branch or only the title.
- **No JavaScript toolchain.** It is a Python package with no runtime
  dependencies; a Go, Rust or Java repository does not need Node to lint its
  commits.

## Where the others are stronger

- **commitlint's ecosystem.** Years of shared configs (`@commitlint/config-*`),
  plugins and editor integrations, plus an interactive prompt for writing the
  message. Commit Check has no prompt, and its rules are the ones it ships.
- **A Node monorepo already on husky.** If commitlint is installed and the
  policy is "message only", there is little to gain from switching.
- **Sign-off remediation.** The DCO app can accept a later commit that
  certifies earlier ones, and lets a maintainer override. Commit Check checks
  the trailer and stops there.
- **Rejecting the push itself.** Only GitHub's rulesets (and a server-side
  hook on GitHub Enterprise Server) refuse a ref update; see the
  [rulesets page](github-rules.md). Every tool above, Commit Check included,
  marks the commit or blocks the merge.

## Coming from gitlint

Both are Python, both run as a `commit-msg` hook through pre-commit, so the
switch is a change to `.pre-commit-config.yaml` and a translation of
`.gitlint` into `cchk.toml`.

Replace the hook:

```yaml title=".pre-commit-config.yaml"
repos:
  - repo: https://github.com/commit-check/commit-check
    rev: v2.19.4
    hooks:
      - id: check-message
```

Install it the same way: `pre-commit install --hook-type commit-msg`.

Two defaults differ. Commit Check requires
[Conventional Commits](../rules.md#cc001) unless you turn it off, where
gitlint makes it an opt-in rule (`contrib=CT1`). And gitlint requires a body
out of the box (B6), where Commit Check does not. This keeps gitlint's
defaults:

```toml title="cchk.toml"
[commit]
conventional_commits = false  # drop if you used contrib=CT1
subject_max_length = 72       # T1
subject_min_length = 5        # T8
allow_wip_commits = false     # T5's default word, WIP
require_body = true           # B6
```

Rule by rule:

| gitlint | Commit Check |
|---|---|
| T1 `title-max-length` | `subject_max_length` ([CC004](../rules.md#cc004)) |
| T5 `title-must-not-contain-word` (default `WIP`) | `allow_wip_commits = false` ([CC010](../rules.md#cc010)), which rejects a subject that starts with `WIP`; gitlint rejects the word anywhere in the title |
| T7 `title-match-regex`, B8 `body-match-regex` | `message_pattern`, one regex over the whole message ([CC001](../rules.md#cc001)) |
| T8 `title-min-length` | `subject_min_length` ([CC005](../rules.md#cc005)) |
| B5 `body-min-length`, B6 `body-is-missing` | `require_body` ([CC011](../rules.md#cc011)); there is no minimum length |
| M1 `author-valid-email` | the `check-author-email` hook ([CC102](../rules.md#cc102)), with `author_email_pattern` |
| CT1 `contrib-title-conventional-commits` | `conventional_commits`, on by default ([CC001](../rules.md#cc001)) |
| CC1 `contrib-body-requires-signed-off-by` | `require_signed_off_by` ([CC012](../rules.md#cc012)) |
| CC2 `contrib-disallow-cleanup-commits` | `allow_fixup_commits = false` ([CC009](../rules.md#cc009)) |
| I4 `ignore-by-author-name` | `ignore_authors` |
| merge, revert, fixup commits ignored | the format rules already skip the subjects git writes; [CC006](../rules.md#cc006), [CC007](../rules.md#cc007) and [CC009](../rules.md#cc009) decide whether they are allowed |
| T2–T4, T6 whitespace and tab rules, T3 trailing punctuation, B1–B4 body line rules, B7 changed-file mention, user-defined Python rules | no equivalent |

The last row is the honest gap: if your policy depends on body line length or
a custom rule written in Python, gitlint still does that and Commit Check does
not. What you gain is the rest of this page: branch names, authors, the
Action, the App, and a release that is current.

## Which to choose

- You want the pull request title checked and nothing else: `action-semantic-pull-request`.
- You are in a JavaScript repository with husky and want plugins: commitlint.
- You need sign-off with a remediation flow: the DCO app, or DCO-2.
- You rely on gitlint's body line rules or your own Python rules: gitlint.
- You want one policy for messages, branches and authors, the same everywhere
  a commit is made and checked, with a hosted option that needs no workflow
  file: Commit Check.
