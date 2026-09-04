# Policy guides

Two rules are off by default because they encode a decision only your project
can make: whether contributors must certify the origin of their work, and
whether AI assistance is welcome, disclosed, or refused.

Commit Check does not take a side on either. It gives you a way to enforce the
position you have already taken, so it stops being relitigated in every review.

## Require signoff (DCO)

Projects that use the [Developer Certificate of Origin](https://developercertificate.org/)
require every commit to carry a `Signed-off-by` trailer. The Linux kernel and
much of the CNCF work this way.

A DCO bot rejecting a pull request after the fact is a poor experience: the
contributor has to rewrite history for every commit in the branch. Checking
locally fixes it before it becomes a problem.

### Turn it on

```toml title="cchk.toml"
[commit]
require_signed_off_by = true
```

This enables [CC012](../rules.md#cc012), which is off by default.

### Signing off

```console
$ git commit --signoff -m "fix: handle an empty config file"
```

The trailer is appended automatically from your `user.name` and `user.email`:

```text
fix: handle an empty config file

Signed-off-by: Your Name <you@example.com>
```

Forgot it? Fix the last commit in place:

```console
$ git commit --amend --signoff --no-edit
```

Fix a whole branch:

```console
$ git rebase --signoff main
```

!!! tip "Make it automatic"

    Signing off is easy to forget. Combine this rule with the
    [pre-commit hook](pre-commit.md) so a missing trailer
    is caught at commit time, not at review time.

### Identity matters

The DCO is a statement about who wrote the code, so it only means something if
the identity is real. [CC101](../rules.md#cc101) and
[CC102](../rules.md#cc102) check the committer name and email, and are enabled
by default when their check runs:

```console
$ commit-check --author-name --author-email
```

To require a company address:

```toml title="cchk.toml"
[commit]
author_email_pattern = "^.+@example\\.com$"
```

### Bots

Automation cannot meaningfully sign the DCO, and forcing it to produces
meaningless trailers. Exempt bots instead:

```toml title="cchk.toml"
[commit]
require_signed_off_by = true
ignore_authors = ["dependabot[bot]", "renovate[bot]"]
```

`ignore_authors` matches the commit author and any `Co-authored-by:` trailers.

## AI attribution

AI coding tools add trailers to commit messages identifying themselves. Whether
that is welcome, required, or unacceptable is a decision each project makes for
itself — and the industry has landed in different places:

- The **Linux kernel** added an `Assisted-by:` trailer, treating AI assistance
  as something to disclose.
- **Some projects disallow AI-assisted contributions outright**, usually over
  provenance and licensing.
- **Most projects have no stated position**, which means the question resurfaces
  in every code review.

### The default: no opinion

```toml
[commit]
ai_attribution = "ignore"   # the default
```

[CC013](../rules.md#cc013) is off. Commits carrying AI trailers pass, and so do
commits without them.

### Forbidding AI-attributed commits

```toml title="cchk.toml"
[commit]
ai_attribution = "forbid"
```

Commits carrying a recognised AI signature now fail:

```text
CC013 ai-attribution check failed ==> feat: add caching layer
AI attribution policy violation
Suggest: This project forbids AI-assisted commits. Remove AI trailers and re-commit.
Docs: https://commit-check.com/rules/#cc013
```

Recognised signatures are trailers and co-author lines naming Claude Code,
GitHub Copilot, Codex, Gemini, Cursor, Devin, Aider, Windsurf and Tabby, plus
generic AI model patterns.

!!! warning "This checks disclosure, not authorship"

    CC013 reads commit metadata. It detects a commit that *says* it was
    AI-assisted; it cannot detect one that was AI-assisted and did not say so.

    Set against a policy of "no AI contributions", it is an honesty check on
    contributors who are already following the rules — not an enforcement
    mechanism against those who aren't. Be clear with yourself about which of
    those you are buying.

### Exempting automation

Bots that legitimately carry AI trailers can be excluded:

```toml title="cchk.toml"
[commit]
ai_attribution = "forbid"
ignore_authors = ["dependabot[bot]", "renovate[bot]"]
```

### Documenting the decision

Whichever way you go, the config file is not where contributors look. State the
policy where they will see it — `CONTRIBUTING.md`, the pull request template —
and let Commit Check be the mechanism rather than the announcement.

Enforcing an undocumented policy produces a confusing failure for somebody
acting in good faith.
