# Compared with other tools

What else checks commit messages, branch names and pull request titles on
GitHub, what each one does, and when it is the better choice. Prices and
features are as the projects list them in September 2026; follow the links
for the current state. GitHub's own rulesets are on
[their own page](github-rules.md).

## The field

| Tool | What it is | What it checks | Where it runs | Price |
|---|---|---|---|---|
| [commitlint](https://commitlint.js.org/) with [commitlint-github-action](https://github.com/wagoid/commitlint-github-action) | The reference Conventional Commits linter in the JavaScript world: shared configs, plugins, a [commitizen](https://commitizen.github.io/cz-cli/) prompt | Commit messages | Node hook (husky), CI Action | Free, open source |
| [action-semantic-pull-request](https://github.com/amannn/action-semantic-pull-request) | The most-used pull request title check; Electron, Vite and Vercel run it | The pull request title (optionally the single commit, for squash merges) | GitHub Action | Free, open source |
| [Semantic PRs](https://github.com/Ezard/semantic-prs) | A GitHub App with the same idea: type and scope on the title or the commits | Pull request title or commits | GitHub App | Free, open source |
| [commitcheck](https://github.com/marketplace/commitcheck) | A hosted App that applies one regular expression, set in its web admin | Commit message, pull request title or description, by regex | GitHub App | Free for public repositories; $25 a month for private ones |
| [DCO app](https://github.com/apps/dco) and [DCO-2](https://github.com/cncf/dco2) | The sign-off check the Linux kernel and the CNCF use, with a remediation flow for missing sign-offs | `Signed-off-by` trailers | GitHub App | Free, open source |
| [PRLint](https://github.com/ewolfe/prlint), [PR Title Checker](https://github.com/marketplace/actions/pr-title-checker) | Regular expressions over pull request fields | Title, body, labels, branch | App / Action | Free, open source |
| **Commit Check** | One rule engine with [24 documented rules](../rules.md), run as a hook, a CLI, an Action, a hosted App or an MCP tool | Commit message, branch name, author name and email, sign-off, AI attribution, force pushes, file size and paths, tag names; the squash message of a pull request | All of the above | Free, open source; the App's private organization repositories move to a paid plan later |

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

## Which to choose

- You want the pull request title checked and nothing else: `action-semantic-pull-request`.
- You are in a JavaScript repository with husky and want plugins: commitlint.
- You need sign-off with a remediation flow: the DCO app, or DCO-2.
- You want one policy for messages, branches and authors, the same everywhere
  a commit is made and checked, with a hosted option that needs no workflow
  file: Commit Check.
