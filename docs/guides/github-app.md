# GitHub App

The hosted [Commit Check App](https://github.com/marketplace/commit-check)
runs the same rule engine as the CLI, against the same config file, with no
workflow file and no CI minutes. Install it once, push, and every commit gets
a **Commit Check** result that says what failed, the value that failed, and
how to fix it. Not every rule applies where the App runs; the
[list](#which-rules) is below.

[Install from the GitHub Marketplace](https://github.com/marketplace/commit-check){ .md-button .md-button--primary }

Choosing between the App and the [GitHub Action](github-actions.md): see
[Where to run it](integrations.md#app-or-action). Both read the same config and
report the same rule IDs, so running both is fine.

## Install

On the Marketplace page, pick the account to install on. For an organization,
choose **All repositories** and every repository, including ones created later,
is covered; with **Only select repositories**, only those are checked and new
ones have to be added by hand. A personal account works the same way.

There is nothing to add to a repository. A repository that already has a
`cchk.toml` or `commit-check.toml` is checked against it from the next push; one
without a config file is checked with the defaults, advisory only (see
[Without a config file](#without-a-config-file)).

## What you get

On every push to a branch and on every pull request, each commit gets a check
run named **Commit Check** on the Checks tab, in the commit's status and in the
merge box. (Tag pushes and branch deletions carry nothing to check; commits by
bots are skipped, and squash mode checks a pull request as one message — both
[below](#bots-re-runs-and-commits-checked-twice).) The result reads the same
way everywhere:

- a one-line verdict — `All 4 checks passed`, or `2 of 4 checks failed`;
- for a failure, a table of what failed, the value that failed and the rule
  ID, linked to the [rule reference](../rules.md);
- **How to fix**: the rule's own explanation and suggestion;
- the full listing of everything that was checked, folded away;
- the version of the rule engine that produced it.

**Details** on the check opens that report; nothing lives on any other site.

### Which rules

The App runs the commit message, author and branch rules — [CC001–CC013](../rules.md#commit-message-rules),
[CC101–CC102](../rules.md#author-rules) and [CC201–CC202](../rules.md#branch-rules) —
with the commit's own branch as the branch under test. One thing it does not
do: the push, file and tag rules ([CC301–CC304](../rules.md#push-rules),
[CC401](../rules.md#tag-rules)) run where a push or a tag happens, in the
[pre-commit hooks](pre-commit.md) and the CLI.

[CC202](../rules.md#cc202) (`require_rebase_target`) is decided from GitHub's
own comparison of the head with the target branch rather than from the clone,
which holds only the commits under test. A failure says how many commits
behind the target the branch is.

### Pull requests

Every commit of a pull request is checked on its own, fork pull requests
included, and pushing more commits checks the new ones. A team that
squash-merges keeps none of those commits, so it can check the result instead:

```toml title="cchk.toml"
[pull_request]
check = "squash"
```

The pull request then gets one result on its head commit, against the message
a squash merge would land — built the way GitHub builds it from the
repository's merge settings, pull request number included. Editing the title or
description re-runs it. The [configuration page](../configuration.md#pull-requests-every-commit-or-the-squash-message)
has the table of what is checked under each merge setting.

### Bots, re-runs, and commits checked twice

- Commits by bots (any author whose name ends in `[bot]`: dependabot,
  renovate, and the like) are skipped. For finer control use
  [`ignore_authors`](../configuration.md#every-option), which the rule engine
  applies itself.
- **Re-run** on the Checks tab checks a commit again — after a config change,
  say. In squash mode it re-checks the pull request.
- A commit pushed to a branch that has an open pull request raises both a push
  and a pull request event; the App checks it once.

## Configuration

The App reads the same file the CLI reads, as it stands at the head of the
push or pull request, in the same four places: `cchk.toml`, `commit-check.toml`, `.github/cchk.toml`,
`.github/commit-check.toml`. Every option on the
[configuration page](../configuration.md) that belongs to a rule the App runs
applies, precedence included; the `[push]`, `[files]` and `[tag]` sections are
read but have nothing to act on here. Nothing is App-specific to set, apart
from the two sections below.

[`inherit_from`](organization.md) works, with one limit: the shared file is
fetched without credentials, so it has to be readable anonymously. A config in
a private `.github` repository is not, and inheritance
[fails open](organization.md#other-sources) — the repository is checked against
its own file alone.

### Without a config file

A repository with no config file has not chosen its rules, so its result is
**advisory**: failures are reported in full, but the check is neutral — titled,
say, `2 of 4 checks would fail (not enforced)` — and never blocks a merge. Below the
fixes the report says why, and gives the smallest file that turns enforcement
on:

```toml title="cchk.toml"
[commit]
conventional_commits = true

[branch]
conventional_branch = true  # false if branch names are free-form
```

Add it, push, and failures are failures. A pass is a pass either way.

!!! warning "Required means nothing until there is a config"

    GitHub treats a neutral check as passing. Making **Commit Check** a required
    check on a repository with no config file blocks nothing. Add the file
    first.

### Jira ticket references

The App can additionally require a ticket reference in every message. This
check is App-side, so the CLI and the Action ignore the section:

```toml title="cchk.toml"
[jira]
required = true
pattern = "PROJ-\\d+"        # default: any KEY-123
suggestion = "Add the ticket, e.g. PROJ-123"
```

It reports as `JIRA jira-ticket` in the same table as the other rules. It
checks the reference's shape, not whether the ticket exists.

## Enforcing it

The App marks a commit; it cannot refuse a push. What keeps a violating change
off the protected branch is a **required status check** named `Commit Check`
in the branch's ruleset or branch protection, where the repository's plan
allows one. With that in place a failing result blocks the merge button and a
passing one clears it.

The order matters: config file first, then the required check, for the reason
in the box above.

## Across an organization

Installing on the organization with **All repositories** covers every
repository; keeping their rules in step is
[`inherit_from`](organization.md): one shared `cchk.toml` in the
organization's `.github` repository, one line in each repository that inherits
it. The [Across an organization](organization.md) guide walks through it,
including how to roll a policy out without a wall of red.

## Plans

Public repositories and everything on personal accounts are free, and stay
free. Today that is every repository: private repositories in organizations
are checked at no charge while the App is new, and a paid **Team** plan for
them is planned. When it arrives, a repository it applies to gets a neutral
check saying so — nothing is blocked — and this page will say so first.

## Privacy

The App fetches the commits under test and the configuration file, nothing
else, and stores nothing: no database, no copy of any message, author or
config. The [privacy page](../privacy.md) lists the permissions it asks for and
what each one is used for.

## When something is off

**No check appears.** The App is not installed on that repository (check the
installation's repository list), the push was a tag or a branch deletion, or
every commit was by a bot.

**A rule you never turned on is failing.** The repository has no config file
and the defaults apply — which is why the result is advisory. The
[Troubleshooting](../troubleshoot.md) page covers the defaults; the starter
config above turns them into a policy.

**The check says "Commit Check could not run".** That is an error, not a
verdict: the App hit a problem checking the commit and says so rather than
staying silent. **Re-run** it; if it keeps failing,
[open an issue](https://github.com/commit-check/commit-check/issues) with the
text of the report.

**A shared config is not being applied.** `inherit_from` fails open, and the
App fetches the shared file anonymously. Make the file readable, or check the
[organization guide](organization.md#other-sources) for the sources it accepts.
