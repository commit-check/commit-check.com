---
date:
  created: 2026-06-21
readtime: 6
categories:
  - ANNOUNCEMENTS
tags:
  - commit-check
authors:
  - shenxianpeng
---

# One policy file for your Git history

Most teams have a wiki page titled something like "How we write commit
messages." It covers commit conventions, branch naming, sign-offs, and
author email consistency — and then nobody reads it.

**Commit Check** exists to turn that wiki page into something Git actually
enforces.

<!-- more -->

## A policy engine, not a linter

Commit Check is a lightweight policy engine for Git *metadata* — the parts of a
commit that live around your code rather than inside it:

- **Commit messages** — Conventional Commits, subject length, imperative mood
- **Branch names** — Conventional Branch types like `feature/`, `bugfix/`, `release/`
- **Author identity** — name and email consistency
- **Sign-off trailers** — `Signed-off-by` for DCO workflows
- **Push safety** — catch accidental force-pushes before they rewrite history

That word — *policy* — matters. Instead of scattering rules across a CI
script, a pre-commit hook, and a stale convention doc, you write them
**once** in a versioned `cchk.toml`.

## Write it once, enforce it everywhere

That single policy file is read by every enforcement point:

```bash
pip install commit-check
commit-check --message --branch
```

The same `cchk.toml` then drives:

- the **CLI** for local one-off checks,
- **pre-commit** hooks so problems are caught before a commit lands,
- **CI / GitHub Actions** so pull requests are validated for the whole team.

Because the policy is committed alongside your code, it is reviewed, diffed, and
versioned like everything else. When the rules change, the change shows up in a
pull request.

## Zero configuration to start

You do not need a config file to begin. With no `cchk.toml`, Commit Check
applies lenient, sensible defaults: commit messages should follow
[Conventional Commits](https://www.conventionalcommits.org/) and branch names
should follow the [Conventional Branch](https://conventional-branch.github.io/)
convention. That is enough to get value on day one.

```bash
echo "feat: add streaming support" | commit-check -m
```

When you need stricter rules — a maximum subject length, required sign-off,
or an allow-list of commit types — add a `cchk.toml`. The next post walks
through the details.

## Add the badge

Once Commit Check is guarding your repository, let people know:

```text
[![commit-check](https://img.shields.io/badge/commit--check-enabled-brightgreen?logo=Git&logoColor=white&color=%232c9ccd)](https://github.com/commit-check/commit-check)
```

## Where to go next

- **Getting Started:** <https://commit-check.com/>
- **GitHub Action:** <https://github.com/commit-check/commit-check-action>
- **Source & issues:** <https://github.com/commit-check/commit-check>

Clean commits. Clear standards. One policy file.
