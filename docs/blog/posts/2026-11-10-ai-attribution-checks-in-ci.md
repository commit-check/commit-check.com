---
date:
  created: 2026-11-10
readtime: 6
slug: ai-attribution-checks-in-ci
description: >-
  I read the CI checks that eleven projects run on AI-assisted commits. The
  same trailer is required by one project and blocks the merge in another.
  Here is what each one checks, and what none of them can.
categories:
  - UPDATES
tags:
  - commit-check
  - ai
  - governance
authors:
  - shenxianpeng
---

# How eleven projects check AI attribution in CI

GitHub's [Octoverse report][octoverse] has this line:

> By September 2026, more than 40% of pull requests on GitHub started with an
> agent's first draft, up from 17% in March.

Many of those agents sign their work. Claude Code, for one, adds a
`Co-Authored-By:` line to its commits unless you turn that off.

Projects have answered with AI policies. A policy file doesn't stop a line
that a tool adds by default, so some projects now check the rule in CI. I read
eleven of those checks. Every project name below links to the file at the
commit I read.

<!-- more -->

## The same two lines, opposite results

Take two lines an agent might leave on a commit, and ask what each project's
check does with them:

| Project | `Co-Authored-By: Claude …` | `Assisted-by: Claude Code` |
|---|---|---|
| [Incus][incus] | fails | fails |
| [Apache XTable][xtable] | fails | not checked |
| [JUnit][junit] | fails | fails |
| [Neovim][neovim] | fails | fails: only a bare `AI-assisted` is allowed |
| [FreeBSD atf][atf] | fails | passes: it is the trailer they ask for |
| [Nextcloud][nextcloud] | labels the pull request | labels the pull request |
| [Vim][vim] | not checked | labels the pull request |
| [Ant Design Vue][antdv] | passes: it is required | fails: no AI co-author |

Three things stand out.

**The same line is required in one project and blocks the merge in another.**
Ant Design Vue fails a commit that has no AI co-author: "Every commit must
include an AI co-author trailer." Incus and JUnit fail a commit that has one,
and XTable fails a commit that credits Claude.

**Projects that want disclosure don't agree on its form.** FreeBSD atf and
Nextcloud ask for an `Assisted-by:` trailer, and Nextcloud's example names
both the tool and the model. Neovim wants the tool left out. Its check prints
`Only a generic "AI-assisted" token is allowed`, and a trailer that names the
tool fails.

**Not every check blocks.** Vim and Nextcloud add an "AI assisted" label and
leave the decision to reviewers. Nextcloud fails only when an agent signs
off, because the DCO "must only be attested by a human contributor".

So there is no habit a contributor, or an agent, can learn once and use
everywhere. The rule has to come from the repository they are contributing to.

## Two projects check the pull request instead

[LangChain's docs repository][langchain] reads the pull request description,
because a squash merge makes it the commit message on main. It fails on the
"Generated with Claude Code" badge and on a Claude co-author line, and asks
for "one plain sentence instead, for example: Prepared with Claude Code."

[Solana web3.js][solana] makes the author tick exactly one of two boxes in
the description: "No AI tooling was used" or "AI tooling was used". For
outside contributors it also looks for a tool's signature left in the title,
the description, the commits or the branch name, and says what it takes that
to mean: "the change was opened without its author reading it."

## Eight shell scripts and three config files

Eight of the eleven checks are shell scripts written for one repository. Each
carries its own list of tools: XTable's has one name, Incus's nine,
Nextcloud's fourteen. A list like that is out of date when the next agent
ships. And a pattern loose enough to find `claude` on an author line also
stops a contributor whose name is Claude.

The other three use [Commit Check](https://github.com/commit-check/commit-check),
which I maintain. There the policy is one setting, and the list of tools comes
with the tool.

[JUnit][junit] forbids AI marks. Its contributing guide says "Git commits must
be authored by you and not attribute an AI tool as co-author", and the
workflow that checks it has four settings:

```yaml
- uses: commit-check/commit-check-action@08357050a644b85d321164f23054f176c13bb018 # v2.20.2
  env:
    CCHK_AI_ATTRIBUTION: forbid
    CCHK_CONVENTIONAL_COMMITS: false
    # Disable default length rules
    CCHK_SUBJECT_MIN_LENGTH: 0
    CCHK_SUBJECT_MAX_LENGTH: 10000
  with:
    message: true
    branch: false
```

[FreeBSD atf][atf] asks for disclosure. The same file also requires a
sign-off and refuses GitHub's noreply author addresses. This is its AI part:

```toml
[commit]
ai_attribution = "disclose"
ai_disclosure_trailers = ["Assisted-by"]
```

[Evolution Gaming][evolution] is a company, and its policy opens with "AI
tools may assist with development, but a human author takes responsibility
for every commit." It publishes one workflow for its repositories to copy
and mark as required. The workflow sets `CCHK_AI_ATTRIBUTION: "forbid"` and
keeps a grep of its own next to it, for trailers the version it pins doesn't
catch.

One commit message gets opposite answers from two of them. In a directory
with FreeBSD atf's `commit-check.toml`:

```console
$ cat message.txt
Fix flaky retry test

Wait for the worker to drain before asserting.

Assisted-by: Claude Code
Signed-off-by: Jane Doe <jane@example.org>
$ commit-check --message message.txt
$ echo $?
0
```

With JUnit's settings:

```console
$ export CCHK_AI_ATTRIBUTION=forbid CCHK_CONVENTIONAL_COMMITS=false
$ export CCHK_SUBJECT_MIN_LENGTH=0 CCHK_SUBJECT_MAX_LENGTH=10000
$ commit-check --message message.txt
✖ Commit rejected by Commit Check · 1 check failed

✖ CC013 ai-attribution failed: Claude Code
  AI attribution is forbidden in this project — detected: Claude Code
  Suggest: This project does not accept AI attribution in commit messages. Remove the AI trailer lines and re-commit.
  Docs:    https://commit-check.com/rules/#cc013
```

## What none of them can check

All eleven read what a commit or a pull request says. None can tell who, or
what, wrote the diff. Delete the trailer and the commit looks like any other.

GitHub's 40% has the same limit. Octoverse defines an agent-started pull
request as one "whose first draft came from a coding agent that we can
detect", and says of its agent signals: "It is a floor, since not all agent
use may be detected."

So these checks don't catch someone who hides AI use. They catch the default:
the line a tool added and the contributor never looked at. They also tell the
contributor what this project wants while the pull request is still open,
which a policy file can't do if nobody opened it.

## If you are writing this rule

- **Decide what a commit should say, not which tools are allowed.** Ten of the
  eleven take one of three positions: no AI marks (JUnit, Incus), disclose it
  in the form the project names (FreeBSD atf, Neovim), or label it and let
  reviewers decide (Vim). Ant Design Vue takes a fourth: always credit the
  tool.
- **Put the fix in the failure message.** Nextcloud's prints the trailer to
  use in place of the one it rejected.
- **If you squash on merge, check the description too**, as LangChain does.

With Commit Check the first two positions are `ai_attribution = "forbid"` and
`ai_attribution = "disclose"`. The
[policies guide](../../guides/policies.md#recipes-from-real-projects) has the
settings for more policies, Nextcloud's among them, and
[the same check for a pull request description](../../guides/policies.md#checking-a-pull-request-description).
The [GitHub App](https://github.com/apps/commit-check) runs the same rules
without a workflow.

If your project checks this in a way I didn't cover, I would like to read it.

[octoverse]: https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/
[incus]: https://github.com/lxc/incus/blob/63377d9bacba35715edf1bcfb4fd155485a6a6fb/.github/workflows/commits.yml
[xtable]: https://github.com/apache/incubator-xtable/blob/0e97d0ae94ac81f9b3e2cc3f86cc2d479e67173c/.github/workflows/commit_coauthor_validation.yml
[junit]: https://github.com/junit-team/junit-framework/blob/13e10545e89a8e217c9d9d2807c449f296205033/.github/workflows/_forbid-ai-attribution.yml
[neovim]: https://github.com/neovim/neovim/blob/7e394dbb896eaf86cb1046666dd423d512cda55f/.github/workflows/labeler_pr.yml
[atf]: https://github.com/freebsd/atf/blob/1f183309cb6f7f6352bed578c0d1554812afdcfa/commit-check.toml
[nextcloud]: https://github.com/nextcloud/android/blob/23951692e38cad0518a000b8542871cfd739e060/.github/workflows/ai-policy.yml
[vim]: https://github.com/vim/vim/blob/437b1deed5d7aece25ae4a5c1c11c550aa1fe206/.github/workflows/label.yml
[antdv]: https://github.com/vueComponent/ant-design-vue/blob/7483836f0adac76516e527df893c3d84a7cd4005/.github/workflows/ai-co-author.yml
[langchain]: https://github.com/langchain-ai/docs/blob/c219b081f6d95d741b99fb6dd69d5a60325e5706/.github/workflows/check-pr-ai-attribution.yml
[solana]: https://github.com/solana-foundation/solana-web3.js/blob/a325305c5680184a1dce27ddb592188810175883/.github/workflows/pr-hygiene.yml
[evolution]: https://github.com/evolution-gaming/.github/blob/9486d3e8e67c3fdcf5cb4301ca3a6cfe93072afb/.github/workflows/human-commit-ownership.yml
