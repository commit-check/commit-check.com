# Compared with other tools

What else checks commit messages, branch names and pull or merge request
titles on GitHub, GitLab and Bitbucket, what each one does, and when it is the
better choice. Prices and features are as the projects list them between
September and November 2026; follow the links for the current state. GitHub's
own rulesets are on [their own page](github-rules.md); GitLab's and
Bitbucket's own settings are in their sections below.

## On GitHub { #the-field }

| Tool | What it is | What it checks | Where it runs | Price |
|---|---|---|---|---|
| [commitlint](https://commitlint.js.org/) with [commitlint-github-action](https://github.com/wagoid/commitlint-github-action) | The reference Conventional Commits linter in the JavaScript world: shared configs, plugins, a [commitizen](https://commitizen.github.io/cz-cli/) prompt | Commit messages | Node hook (husky), CI Action | Free, open source |
| [gitlint](https://github.com/jorisroovers/gitlint) | A Python commit message linter with a `commit-msg` hook, configured in a `.gitlint` file; one of the two commit linters the [pre-commit hooks page](https://pre-commit.com/hooks.html) features. Its latest release, 0.19.1, is from March 2023, and its [PyPI page](https://pypi.org/project/gitlint/) says the maintainer is looking for co-maintainers | Commit messages: title and body length, whitespace, required words, regexes; Conventional Commits and sign-off as opt-in rules | Git hook, pre-commit, CLI | Free, open source |
| [action-semantic-pull-request](https://github.com/amannn/action-semantic-pull-request) | The most-used pull request title check; Electron, Vite and Vercel run it | The pull request title (optionally the single commit, for squash merges) | GitHub Action | Free, open source |
| [Semantic PRs](https://github.com/Ezard/semantic-prs) | A GitHub App with the same idea: type and scope on the title or the commits | Pull request title or commits | GitHub App | Free, open source |
| [commitcheck](https://github.com/marketplace/commitcheck) | A hosted App that applies one regular expression, set in its web admin | Commit message, pull request title or description, by regex | GitHub App | Free for public repositories; $25 a month for private ones |
| [DCO app](https://github.com/apps/dco) and [DCO-2](https://github.com/cncf/dco2) | The sign-off check the Linux kernel and the CNCF use, with a remediation flow for missing sign-offs | `Signed-off-by` trailers | GitHub App | Free, open source |
| [PRLint](https://github.com/ewolfe/prlint), [PR Title Checker](https://github.com/marketplace/actions/pr-title-checker) | Regular expressions over pull request fields | Title, body, labels, branch | App / Action | Free, open source |
| **Commit Check** | One rule engine, [documented rule by rule](../rules.md), run as a hook, a CLI, an Action, a hosted App, a GitLab CI/CD component, a Bitbucket pipe or an MCP tool | Commit message, branch name, author name and email, sign-off, AI attribution, force pushes, file size and paths, tag names; the pull or merge request title (Action, GitLab CI, Bitbucket Pipelines) and the squash message of a pull request (App) | All of the above, plus GitLab CI and Bitbucket Pipelines | Free, open source; the App's private organization repositories move to a paid plan later |

## On GitLab

GitLab has commit policies of its own, in its paid tiers. On GitLab Free, a
check is a job in the merge request pipeline.

| Tool | What it is | What it checks | Where it runs | Price |
|---|---|---|---|---|
| [Push rules](https://docs.gitlab.com/user/project/repository/push_rules/) | GitLab's own `pre-receive` hooks, set for a project or a group | Commit messages that must or must not match a regex, branch names, author and committer email, DCO sign-off, signed commits | On the GitLab server, when the push arrives | Premium and Ultimate |
| [Merge request title validation](https://docs.gitlab.com/user/project/merge_requests/title_validation) | A merge request setting, generally available since GitLab 18.10 | The merge request title, against a pattern; a title that does not match blocks the merge | GitLab | Premium and Ultimate |
| [commitlint](https://commitlint.js.org/guides/ci-setup) in a CI job | commitlint's documented GitLab CI setup, linting every commit of the merge request | Commit messages | A Node job in the pipeline | Free, open source |
| [Danger JS](https://danger.systems/js/) | Rules you write yourself, in a `dangerfile.js` or `dangerfile.ts` | Whatever the Dangerfile checks | A Node job in the pipeline | Free, open source |
| **Commit Check** | On GitLab.com, the [CI/CD Catalog component](https://gitlab.com/explore/catalog/commit-check/commit-check), two lines in `.gitlab-ci.yml`; on a self-managed GitLab, a job you [write out](../guides/other-ci.md#writing-the-job-yourself) ([setup](../guides/other-ci.md#gitlab-ci)) | The source branch and every commit the merge request adds; the title, AI attribution in the description, authors and files as inputs | A job in merge request pipelines | Free, open source |

- **On GitLab Free** there are no push rules and no title validation, so a CI
  job is the way to check anything. The component is that job, with every
  failure explained under its rule ID.
- **On Premium and Ultimate** push rules refuse the push itself, which no CI
  job can do. They are one regular expression per field. Commit Check checks
  with named rules, each failure carrying a suggestion and a link to its
  documentation, and the same `cchk.toml` runs in the developer's commit hook.
  The two combine: push rules for what must never reach the server, the
  component for the rest.
- A CI job blocks the merge only with **Pipelines must succeed** turned on;
  see [Making a failed check block the merge](../guides/other-ci.md#making-a-failed-check-block-the-merge).
  It also checks the title as it was when the pipeline ran: editing the title
  or description does not start a new pipeline, where GitLab's own title
  validation judges the current title.

## On Bitbucket

Bitbucket Cloud cannot check commit messages by itself:
[Atlassian's knowledge base](https://support.atlassian.com/bitbucket-cloud/kb/commit-message-validation-with-regex-patterns-using-local-hooks/)
says there is no native feature for it and lists server-side hooks as a
feature request. The choice is a Pipelines step or a Marketplace app, and on
Data Center a pre-receive hook app.

| Tool | What it is | What it checks | Where it runs | Price |
|---|---|---|---|---|
| [commitlint](https://commitlint.js.org/guides/ci-setup) in a Pipelines step | commitlint's documented Bitbucket setup, in a `pull-requests` pipeline | Commit messages | A Node step | Free, open source |
| [Danger JS](https://danger.systems/js/) | Rules you write yourself in a Dangerfile; supports Bitbucket Cloud and Server | Whatever the Dangerfile checks | A Node step | Free, open source |
| [Better Commit Policy Connector](https://marketplace.atlassian.com/apps/1214430/better-commit-policy-connector-for-bitbucket) | Midori's Marketplace app, enforced through merge checks | Commit messages, committer, branch names, pull request titles and descriptions | Bitbucket Cloud, Server and Data Center | Free; needs Midori's [Better Commit Policy for Jira](https://marketplace.atlassian.com/apps/1213415/better-commit-policy-for-jira-git-bitbucket-and-more), a paid app (free up to 10 Jira Cloud users) |
| [Yet Another Commit Checker](https://marketplace.atlassian.com/apps/1211854/yet-another-commit-checker) | Appfire's pre-receive hook app; not offered for Bitbucket Cloud | Commit messages by regex, branch names, Jira issue keys, committer name and email | Bitbucket Data Center and Server | Paid, through Atlassian |
| **Commit Check** | The [Commit Check pipe](https://bitbucket.org/commit-check/commit-check), one line in a `pull-requests` step ([setup](../guides/other-ci.md#bitbucket-pipelines)) | The source branch and every commit the pull request adds; the title, AI attribution in the description, authors and files as variables | A Pipelines step | Free, open source |

- **The pipe needs no Node and no Jira.** It runs in an image of its own, with
  the same `cchk.toml` as the hook and the GitHub Action. As on GitLab,
  editing a pull request does not start a pipeline, so run the step again
  after changing the title or description.
- **Blocking the merge is a Premium setting.** On Bitbucket Cloud,
  [merge checks](https://support.atlassian.com/bitbucket-cloud/docs/suggest-or-require-checks-before-a-merge/)
  that stop the merge need the Premium plan; on other plans they only warn,
  and the pull request can still be merged. That holds for every tool in the
  table that runs in Cloud.
- **Jira-centred policies** are where the Marketplace apps are stronger: they
  check an issue key against Jira itself. Commit Check can require a key's
  shape with `message_pattern`, not that the issue exists.

## AI attribution checkers

Newer tools check AI attribution in commits. They differ in which way the
policy points.

| Tool | What it does | Where it runs | Price |
|---|---|---|---|
| [no-ai-marks](https://github.com/marketplace/actions/no-ai-marks) | Fails when commits, pull requests, branch names or files carry AI attribution or hidden watermarks. An `Assisted-by:` trailer is an error too | GitHub Action, reusable workflow, pre-commit, CLI | Free, open source |
| [CommitGuard](https://pypi.org/project/commitguardian/) | Blocks AI, bot and agent attribution in commits: co-author lines, AI identities and AI trailers. Marked pre-alpha | Git hooks, CLI, GitHub Actions, an optional GitHub App | Free, open source |
| [commitlint-config-agent-coauthor](https://www.npmjs.com/package/commitlint-config-agent-coauthor) | The other way round: requires a `Co-authored-by` trailer when an AI agent made the commit, detected from environment variables | commitlint | Free, open source |
| **Commit Check** | Either way: `ai_attribution = "forbid"` rejects known AI tool signatures ([CC013](../rules.md#cc013)); `"disclose"` requires a trailer such as `Assisted-by:` on a commit that shows signs of AI assistance (a vendor's co-author line, an AI sign-off, a tool's mark) and rejects an AI co-author or sign-off ([CC014](../rules.md#cc014) to [CC016](../rules.md#cc016)). To have every pull request declare, [CC501](../rules.md#cc501) requires one AI declaration box ticked in the template | Everywhere on this page | Free, open source |

A project that accepts AI-assisted work and wants it declared needs a check
that requires the disclosure, not one that rejects every trace of AI. See
[Asking for disclosure instead](../guides/policies.md#asking-for-disclosure-instead).

## What is different about Commit Check

- **One config, every place it runs.** The same `cchk.toml` drives the
  [pre-commit hook](../guides/pre-commit.md), the [Action](../guides/github-actions.md),
  the [App](../guides/github-app.md), the
  [GitLab component and the Bitbucket pipe](../guides/other-ci.md) and the
  [MCP server](../guides/mcp.md). The others cover one place each: commitlint
  is a Node hook and a CI job; the title checkers are Actions or Apps;
  commitcheck is an App; push rules and Marketplace apps belong to one forge.
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
- **Rejecting the push itself.** Only rules that run on the server refuse a
  ref update: GitHub's rulesets (see the [rulesets page](github-rules.md)) and
  a server-side hook on GitHub Enterprise Server, GitLab's push rules, and a
  pre-receive hook app such as Yet Another Commit Checker on Bitbucket Data
  Center. Every other tool above, Commit Check included, marks the commit or
  blocks the merge.

## Coming from gitlint

Both are Python, both run as a `commit-msg` hook through pre-commit, so the
switch is a change to `.pre-commit-config.yaml` and a translation of
`.gitlint` into `cchk.toml`.

Replace the hook:

```yaml title=".pre-commit-config.yaml"
repos:
  - repo: https://github.com/commit-check/commit-check
    rev: v2.24.2
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
body_max_line_length = 80     # B1
```

Rule by rule:

| gitlint | Commit Check |
|---|---|
| T1 `title-max-length` | `subject_max_length` ([CC004](../rules.md#cc004)) |
| T5 `title-must-not-contain-word` (default `WIP`) | `allow_wip_commits = false` ([CC010](../rules.md#cc010)), which rejects a subject that starts with `WIP`; gitlint rejects the word anywhere in the title |
| T7 `title-match-regex`, B8 `body-match-regex` | `message_pattern`, one regex over the whole message ([CC001](../rules.md#cc001)) |
| T8 `title-min-length` | `subject_min_length` ([CC005](../rules.md#cc005)) |
| B1 `body-max-line-length` | `body_max_line_length` ([CC018](../rules.md#cc018)), off by default; lines with a URL, a single word with no space (a path, a hash) and trailers are not counted |
| B5 `body-min-length`, B6 `body-is-missing` | `require_body` ([CC011](../rules.md#cc011)); there is no minimum length |
| M1 `author-valid-email` | the `check-author-email` hook ([CC102](../rules.md#cc102)), with `author_email_pattern` |
| CT1 `contrib-title-conventional-commits` | `conventional_commits`, on by default ([CC001](../rules.md#cc001)) |
| CC1 `contrib-body-requires-signed-off-by` | `require_signed_off_by` ([CC012](../rules.md#cc012)) |
| CC2 `contrib-disallow-cleanup-commits` | `allow_fixup_commits = false` ([CC009](../rules.md#cc009)) |
| I4 `ignore-by-author-name` | `ignore_authors` |
| merge, revert, fixup commits ignored | the format rules already skip the subjects git writes; [CC006](../rules.md#cc006), [CC007](../rules.md#cc007) and [CC009](../rules.md#cc009) decide whether they are allowed |
| T2–T4, T6 whitespace and tab rules, T3 trailing punctuation, B2–B4 body whitespace, tab and blank-line rules, B7 changed-file mention, user-defined Python rules | no equivalent |

The last row is the honest gap: if your policy depends on whitespace rules or
a custom rule written in Python, gitlint still does that and Commit Check does
not. What you gain is the rest of this page: branch names, authors, the
Action, the App, and a release that is current.

## Which to choose

- You want the pull request title checked and nothing else: `action-semantic-pull-request`.
- You are in a JavaScript repository with husky and want plugins: commitlint.
- You need sign-off with a remediation flow: the DCO app, or DCO-2.
- You rely on gitlint's whitespace rules or your own Python rules: gitlint.
- You are on GitLab Premium, a regex per field is enough, and the push itself
  must be refused: push rules.
- Your policy is Jira issue keys on Bitbucket: a Marketplace app that reads
  Jira.
- You want one policy for messages, branches and authors, the same everywhere
  a commit is made and checked, on GitHub, GitLab and Bitbucket, with a hosted
  option on GitHub that needs no workflow file: Commit Check.
