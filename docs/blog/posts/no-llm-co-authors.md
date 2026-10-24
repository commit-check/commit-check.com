---
date:
  created: 2026-10-24
readtime: 4
slug: no-llm-co-authors
description: >-
  Some projects close any pull request that credits an LLM as a co-author.
  Here is how to check that rule on every pull request, including the
  co-author lines a squash merge copies into main.
categories:
  - UPDATES
tags:
  - commit-check
  - ai
  - github-app
authors:
  - shenxianpeng
---

# "No LLM bots in Co-authored-by": checking the rule before the squash merge

Some projects have written down a short, strict rule about AI tools. The AI
policy that [pip](https://github.com/pypa/pip/blob/main/AI_POLICY.md) and
[attrs](https://github.com/python-attrs/attrs/blob/main/.github/AI_POLICY.md)
use puts it in one line:

> No LLM bots in `Co-authored-by:`s.

A pull request that lists an LLM product as a co-author "can't be merged and
will be closed without further discussion". Using AI tools is still allowed,
but contributors "must remove any LLM co-author tags and take full ownership
of every line."

A machine can check that rule. Unless one does, a reviewer has to open every
commit of every pull request and read its trailers.

<!-- more -->

## Why squash merges make it worse

The co-author line is rarely on the commit a reviewer looks at. An agent adds
it to the commit it wrote, the contributor pushes a fix on top, and the review
happens on the final diff.

When the project squashes on merge, GitHub's default squash message collects
the `Co-authored-by:` and `Signed-off-by:` lines from all of the pull
request's commits and appends them, whichever body the repository uses. It also credits each commit author other than the person
who opened the pull request, so commits written by the Copilot coding agent
reach main with a `Co-authored-by: Copilot` line. One line missed in any commit
becomes a permanent co-author credit on main.

## One file

[Commit Check](https://github.com/commit-check/commit-check) reads its rules
from a `cchk.toml`. This one checks the co-author rule, turns off the message
format and branch name rules, and allows any subject up to 1000 characters.
The default author name and email checks ([CC101](../../rules.md#cc101),
[CC102](../../rules.md#cc102)) stay on:

```toml
warn = ["CC014"]  # the policy does not ask for disclosure: report it, never fail

[commit]
ai_attribution = "disclose"   # fail if an AI tool is credited as co-author or sign-off
conventional_commits = false  # no message format
subject_max_length = 1000     # allow long subjects
subject_min_length = 0        # and short ones

[branch]
conventional_branch = false   # no branch name rules

[pull_request]
check = "squash"  # check the one commit a squash merge lands
```

The `disclose` policy fails a commit that credits an AI tool as a co-author
([CC015](../../rules.md#cc015)) or has it sign off
([CC016](../../rules.md#cc016)). It also asks for an `Assisted-by:` disclosure
([CC014](../../rules.md#cc014)). This policy doesn't ask for one, so the
`warn` line reports it without failing the check.

## Check the commit that lands

With the [Commit Check App](https://github.com/apps/commit-check) installed,
every pull request gets a **Commit Check** result. The `[pull_request]` section
makes it check the commit a squash merge would land: the title and body your
merge settings produce, plus the co-author and sign-off lines GitHub adds from
the commits. A pull request whose second commit was co-authored by Claude Code
gets this:

```text
❌ Squash message failed (1 of 3 checks)

Squash message  `Add retries to the HTTP client (#214)`  CC015 ai-co-author
  value: Co-Authored-By: Claude <noreply@anthropic.com>
  An AI tool is credited as a co-author: Claude Code
```

Make **Commit Check** a required check in the branch's ruleset, and the pull
request can't be merged until the contributor removes the line from their
commits. The App can read the repository and its pull requests and can write
only check runs ([what it reads](../../privacy.md)). It never comments, and it is
free for public repositories. The
[App guide](../../guides/github-app.md#pull-requests) shows what is checked
under each merge setting.

If you would rather keep it in a workflow,
[commit-check-action](https://github.com/commit-check/commit-check-action)
reads the same file and checks every commit of the pull request.

## What it catches

It catches the co-author and sign-off lines that Claude Code, GitHub Copilot
(including the coding agent), Cursor, Codex, Devin, Jules, Amp, Factory Droid
and OpenHands write, and model names such as `gemini-2.5-pro`. It matches those
known signatures, so a tool it doesn't recognize yet passes. Human co-authors
pass, including people who happen to be called Claude or Jules, and so do
Dependabot and pre-commit.ci. `Assisted-by:` and `Generated-by:` trailers pass
too, since this policy doesn't forbid them.

## What it can't do

It checks what a commit says, not who wrote it. A commit with no AI trailer
passes, whoever wrote it. The other half of the policy, "take full ownership of
every line", is still the reviewer's job. What the check removes is the part a
reviewer is worst at: reading trailers on the twentieth pull request of the
day.

If your project's AI policy says something different, such as "disclose it
with `Assisted-by:`" or "no AI trailers at all",
[this earlier post](ai-commit-attribution-policy.md) shows the setting for
each.
