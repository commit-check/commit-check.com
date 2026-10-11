---
date:
  created: 2026-10-11
readtime: 4
slug: ai-commit-attribution-policy
description: >-
  AI coding agents stamp their own trailers on your commits. Open source has
  answered that three ways; here is how to enforce whichever one your project
  chose, on every commit.
categories:
  - UPDATES
tags:
  - commit-check
  - ai
  - governance
authors:
  - shenxianpeng
---

# Your AI agent signs your commits. Does your project have a policy for that?

Ask Claude Code or Cursor to commit for you and, by default, the commit comes
out stamped:

```text
fix: resolve race condition in the cache

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

Whether that line belongs in your history is a policy question, and open
source has already given three different answers.

<!-- more -->

| Position | Who takes it |
|---|---|
| No AI trailers in the history; disclose in the pull request instead | [Kubernetes](https://www.kubernetes.dev/docs/guide/pull-requests/) |
| AI is welcome, but say so with a trailer, and never credit the tool as a person | [Linux kernel](https://docs.kernel.org/process/coding-assistants.html) and [Fedora](https://docs.fedoraproject.org/en-US/council/policy/ai-policy/) (`Assisted-by:`), the [ASF](https://www.apache.org/legal/generative-tooling.html) (`Generated-by:`) |
| The tool is a co-author like anyone else | [pytest](https://docs.pytest.org/en/stable/contributing.html) |

The kernel adds one hard rule on top: an AI agent must never add a
`Signed-off-by:` line, because only a person can certify the
[DCO](https://developercertificate.org/).

The trouble is that all of these are policies written in a CONTRIBUTING file
and enforced by a reviewer's eyes. Nobody reads trailers carefully on the
twentieth pull request of the day.

## Making the policy a check

[Commit Check](https://github.com/commit-check/commit-check) is open-source
commit policy as code for teams and AI agents: the rules for commit messages,
branch names, authors and sign-offs live in one config file and are enforced in
hooks, CI and pull requests. Since [v2.18](../../changelog.md#v2180) it turns
each of those positions into one setting in `cchk.toml`:

```toml
[commit]
ai_attribution = "forbid"    # or "disclose", or "ignore" (the default)
```

With `forbid`, the stamped commit above fails:

```text
CC013 ai-attribution check failed ==> Claude Code
AI attribution is forbidden in this project — detected: Claude Code
Suggest: This project does not accept AI attribution in commit messages. Remove the AI trailer lines and re-commit.
Docs: https://commit-check.com/rules/#cc013
```

With `disclose`, the same commit fails for a different reason, and the failure
tells you exactly what to write instead:

```text
CC014 ai-disclosure check failed ==> Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
AI assistance is not disclosed with Assisted-by or Generated-by — detected: Claude Code
Suggest: Disclose the tool with "Assisted-by: Claude Opus 5"
Docs: https://commit-check.com/rules/#cc014

CC015 ai-co-author check failed ==> Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
An AI tool is credited as a co-author: Claude Code
Suggest: Use "Assisted-by: Claude Opus 5" in place of the co-author line
Docs: https://commit-check.com/rules/#cc015
```

A third rule, [CC016](../../rules.md#cc016), rejects a sign-off by the tool.
Only a person can certify the DCO, so no list of accepted trailers makes that
sign-off acceptable. Each of the three rules can be
[demoted to a warning](../../configuration.md#report-a-rule-without-enforcing-it)
on its own, so you can roll the policy out gently.

The detection covers co-author and sign-off lines that name Claude Code, GitHub
Copilot, Codex, Gemini, Cursor, Devin, Aider, Windsurf, Tabby or a model, and
vendor marks such as "Generated with Claude Code". It matches the tools'
noreply addresses, so a human co-author who happens to be called Claude is left
alone. [CC013](../../rules.md#cc013) keeps the current list.

## The fix comes with the failure

With `--format json`, the failing checks carry the corrected message, so a
script or an agent can apply it without interpreting anything:

```json
"fix": "fix: resolve race condition in the cache\n\nAssisted-by: Claude Opus 5"
```

Since [v2.18.3](../../changelog.md#v2183), `--fix` applies it for you. Give it
the message file, or give the pre-commit hook
[`args: [--fix]`](../../guides/pre-commit.md#fixing-the-message-instead-of-rejecting-it),
and the co-author line is rewritten as the disclosure before the commit is
recorded:

```console
$ commit-check -m --fix msg.txt
✎ fixed the commit message: CC014 ai-disclosure
$ cat msg.txt
fix: resolve race condition in the cache

Assisted-by: Claude Opus 5
```

That is also the point of the [MCP server](../../guides/mcp.md): the agent asks
for your rules before it commits, and writes the disclosure your project wants
in the first place.

## Run it where it cannot be skipped

The same `cchk.toml` drives a pre-commit hook, a GitHub Action, a GitHub App
and a plain CLI for any other CI, so the policy a developer sees locally is the
one enforced on the pull request
([where to run it](../../guides/integrations.md)):

```bash
pip install commit-check
printf 'fix: resolve race condition\n\nAssisted-by: Claude Opus 5\n' | CCHK_AI_ATTRIBUTION=disclose commit-check -m
```

## What it cannot do

This checks disclosure, not authorship. It catches a commit that says it was
AI-assisted; it cannot catch one that was AI-assisted and says nothing. Against
a policy of "no AI contributions at all", it is an honesty check for
contributors who already follow the rules, not a detector. For the far more
common policy, "tell us when you used it, and in this format", it turns a
paragraph in CONTRIBUTING into a check that runs on every commit.

The rules, with examples, are in the [rules reference](../../rules.md#cc013),
and the [policy guide](../../guides/policies.md#ai-attribution) walks through
each setting.

Which of the three positions does your project take, and is it written down
anywhere yet? Tell us in
[Discussions](https://github.com/commit-check/commit-check/discussions).
