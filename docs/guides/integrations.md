# Where to run it

Commit Check is one rule engine with several places to run it, and every one
of them reads the same `cchk.toml`. That is the point: the rules cannot drift
between what a developer sees locally and what is enforced on the pull request.

| Where | Catches problems | Can be bypassed | Set up |
|---|---|---|---|
| [Pre-commit hook](pre-commit.md) | As the message is written | Yes — `--no-verify` | `.pre-commit-config.yaml` in each repository |
| [GitHub Action](github-actions.md) | On every push and pull request, in CI | No | A workflow file in each repository |
| [GitHub App](github-app.md) | On every push and pull request, hosted | No | Install once for the organization |
| [Command line](../example.md) | Wherever you call it: a range of commits, a CI you write yourself | — | `pip install commit-check` |
| [MCP server](mcp.md) | Before the commit exists, inside an AI coding agent | — | One entry in the agent's MCP config |
| [Organization config](organization.md) | Everywhere at once | — | One shared `cchk.toml`, whichever of the above runs it |

## Which one

- **Every project wants a hook.** It is the cheapest place to enforce commit
  policy: the developer finds out while they are still writing the message,
  not after a CI round trip.
- **A policy needs a check that cannot be skipped.** Anyone can pass
  `--no-verify` to a hook. The Action and the App run where that is not
  possible, and a required check keeps a violating change from merging.
- **More than a handful of repositories wants one config.** `inherit_from`
  lets every repository share a base policy and override only what it
  genuinely needs, whichever of the above runs the checks.

### App or Action? { #app-or-action }

| | GitHub App | GitHub Action |
|---|---|---|
| Setup | Install once for the organization | A workflow file in each repository |
| Runs on | GitHub.com | GitHub.com and GitHub Enterprise Server, any runner |
| Cost | No CI minutes | A runner per run; metered minutes on private repositories |
| Output | A check run per commit | Job summary, PR comment, `result` output |
| Fits | Organization-wide coverage with no per-repository work | Custom workflows, self-hosted runners, GHES |

Both read the same config and report the same rule IDs, so a team can run
both: the App for coverage, the Action where a workflow needs the result.

## How they combine

A hook gives fast feedback to people who want to follow the policy. The Action
or the App is what makes it a policy. Most projects want both: the hook on
every laptop, and one of the two on the pull request.

## Pre-commit hook { #as-a-pre-commit-hook }

Runs at `commit-msg` and `pre-commit` time on the developer's machine, fetched
by pre-commit itself, so there is nothing to install. Hooks can be skipped, by
design. [Set it up →](pre-commit.md)

## GitHub Action { #in-github-actions }

A workflow file in the repository, on any runner, GitHub Enterprise Server
included. Posts a job summary, can comment on the pull request, and exposes a
`result` output for the rest of the workflow. [Set it up →](github-actions.md)

## GitHub App { #as-a-github-app }

Hosted. Install it once on an organization and every repository, including
ones created later, gets a **Commit Check** result on each commit of every
push and pull request, with no workflow file and no CI minutes.
[Set it up →](github-app.md)

## MCP server

The same rules as tools for an AI coding agent, so the message is right before
the commit exists. One entry in the agent's MCP settings. [Set it up →](mcp.md)

## Across an organization { #across-an-organization }

One `cchk.toml` in the organization's `.github` repository; each repository
inherits it with one line and overrides only what it must.
[Set it up →](organization.md)
