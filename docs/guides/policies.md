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
contributor has to rewrite history for every commit in the branch. A local check
catches a missing sign-off at commit time, before there is anything to rewrite.

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
[CC102](../rules.md#cc102) check the author name and email, and are enabled
by default when their check runs:

```console
$ commit-check --author-name --author-email
```

To require a company address:

```toml title="cchk.toml"
[commit]
author_email_pattern = "^.+@example\\.com$"
```

To refuse GitHub's no-reply addresses, which cannot receive mail and can lose
their link to the author's account after a username change:

```toml title="cchk.toml"
[commit]
author_email_pattern = '(?i)^(?!.*@users\.noreply\.github\.com$).+@.+$'
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

AI coding tools stamp their own trailers on the commits they help with.
Whether that is welcome, required or unacceptable is a decision each project
makes for itself, and the industry has landed in three places — which are the
three values `ai_attribution` takes:

| `ai_attribution` | The project's position | Rules |
|---|---|---|
| `"ignore"` (default) | no stated position | — |
| `"forbid"` | no AI attribution in the history | [CC013](../rules.md#cc013) |
| `"disclose"` | AI is welcome, said out loud, and not credited as a person | [CC014](../rules.md#cc014)–[CC016](../rules.md#cc016) |

Whichever you pick, the check reads what the message says. It cannot see
assistance that left no trace — see the note below.

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
CC013 ai-attribution check failed ==> Claude Code
AI attribution is forbidden in this project — detected: Claude Code
Suggest: This project does not accept AI attribution in commit messages. Remove the AI trailer lines and re-commit.
Docs: https://commit-check.com/rules/#cc013
```

Recognised signatures are co-author and sign-off lines naming Claude Code,
GitHub Copilot, Codex, Gemini, Cursor, Devin, Aider, Windsurf, Tabby, Amp,
OpenHands, Factory Droid, Jules, Continue, Mistral Vibe and Qwen Code, the
disclosure trailers `Assisted-by:` and
`Generated-by:`, vendor marks such as `🤖 Generated with Claude Code`, Amp's
`Amp-Thread-ID:`, the Copilot coding agent's `Agent-Logs-Url:` and Cursor's
`Made-with: Cursor`, and generic AI model names. This is the
position [Kubernetes](https://www.kubernetes.dev/docs/guide/pull-requests/)
takes — no AI trailers in the history, disclosure in the pull request
instead.

These rules read only the message. Jules and OpenHands can commit under their
own bot identity instead of adding a co-author line, and such a commit passes
when its message contains no recognized AI signature. The Copilot coding agent
also commits as its own account, but every commit it makes carries an
`Agent-Logs-Url:` trailer, so its commits are caught.

!!! warning "This checks disclosure, not authorship"

    These rules read commit metadata. They detect a commit that *says* it
    was AI-assisted; they cannot detect one that was AI-assisted and did
    not say so.

    Set against a policy of "no AI contributions", it is an honesty check on
    contributors who are already following the rules — not an enforcement
    mechanism against those who aren't. Be clear with yourself about which of
    those you are buying.

### Checking AI attribution and nothing else

`ai_attribution` sits alongside the message rules that are on by default, so
`--message` still applies Conventional Commits and the subject length limits
(80 characters at most, 5 at least). A project that has its own commit style
and only wants the AI check turns those off:

```toml title="cchk.toml"
[commit]
ai_attribution = "forbid"
conventional_commits = false
subject_max_length = 0   # 0 turns the length rule off
subject_min_length = 0
```

Or, in the GitHub Action, without a config file:

```yaml
- uses: commit-check/commit-check-action@v2
  env:
    CCHK_AI_ATTRIBUTION: forbid
    CCHK_CONVENTIONAL_COMMITS: false
    CCHK_SUBJECT_MAX_LENGTH: 0
    CCHK_SUBJECT_MIN_LENGTH: 0
  with:
    message: true
    branch: false
```

Leave the length limits on and a long subject fails the job too. Dependency
bots write long ones: Renovate's `Update dependency
com.googlecode.owasp-java-html-sanitizer:owasp-java-html-sanitizer to
v20261103` is 95 characters.

### Asking for disclosure instead

Most projects that allow AI assistance ask to be told about it.
[Fedora](https://docs.fedoraproject.org/en-US/council/policy/ai-policy/) and
FluxCD want an `Assisted-by:` trailer, as the
[Linux kernel](https://docs.kernel.org/process/coding-assistants.html) did
until its maintainers decided in October 2026 to drop the tag; the
[Apache Software Foundation](https://www.apache.org/legal/generative-tooling.html)
recommends `Generated-by:`. The kernel still says an AI agent must
never add a `Signed-off-by:` line, because only a person can certify the
[DCO](https://developercertificate.org/).

```toml title="cchk.toml"
[commit]
ai_attribution = "disclose"
```

That turns on three rules, each about one of those conditions:

| Rule | Asks that |
|---|---|
| [CC014](../rules.md#cc014) | the assistance is disclosed with an accepted trailer |
| [CC015](../rules.md#cc015) | the tool is not credited as a co-author |
| [CC016](../rules.md#cc016) | the tool did not sign off the commit |

A commit that a vendor stamped and nobody disclosed fails the first two, and
the failure carries the disclosure already written:

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

Both carry the same correction in `--format json`: the co-author line rewritten
as the project's disclosure trailer, keeping the name the tool gave itself.

```json
"fix": "feat: add caching layer\n\nAssisted-by: Claude Opus 5"
```

Once the tool is disclosed, CC015 asks only for the co-author line to go, and
a commit in the kernel's `Assisted-by:` format passes all three:

```bash
printf 'feat: add caching layer\n\nAssisted-by: LLM coccinelle sparse\nSigned-off-by: Jane Dev <jane@example.com>' | commit-check -m
```

### Choosing the format

`ai_disclosure_trailers` is the list of trailers that count as a disclosure,
and the first one is what a correction is written with:

```toml title="cchk.toml"
[commit]
ai_attribution = "disclose"
ai_disclosure_trailers = ["Assisted-by"]   # Assisted-by, and nothing else
```

Listing `Co-authored-by` says the project accepts the tool as a co-author —
[pytest](https://github.com/pytest-dev/pytest/blob/main/CONTRIBUTING.rst) and
IREE do — and CC015 then passes. `Signed-off-by` is refused whatever else you
list, so CC016 cannot be configured away.

`ai_disclosure_pattern` asks for a particular shape, such as FluxCD's
`agent/model`:

```toml title="cchk.toml"
[commit]
ai_attribution = "disclose"
ai_disclosure_pattern = '^\S+/\S+$'
```

```text
CC014 ai-disclosure check failed ==> Assisted-by: Claude Code
The Assisted-by value does not match the required pattern: ^\S+/\S+$
Suggest: Write the Assisted-by value so that it matches ^\S+/\S+$ (set by ai_disclosure_pattern in the [commit] config)
```

That failure carries no correction, because the tool should not guess which
model or format you meant.

### Refusing the tool as a co-author, without asking for disclosure

[pip](https://github.com/pypa/pip/blob/main/AI_POLICY.md) and
[attrs](https://github.com/python-attrs/attrs/blob/main/.github/AI_POLICY.md)
close any pull request that lists an LLM as a co-author, but they don't ask
contributors to disclose AI use. Put CC014 in the top-level `warn` list and
the other two keep enforcing:

```toml title="cchk.toml"
warn = ["ai_disclosure"]

[commit]
ai_attribution = "disclose"
```

```text
CC014 ai-disclosure check warning ==> 🤖 Generated with [Claude
AI assistance is not disclosed with Assisted-by or Generated-by — detected: Claude Code
Suggest: Disclose the tool with "Assisted-by: Claude Code"
Docs: https://commit-check.com/rules/#cc014
This rule is set to warn in the config; it does not fail the run.
```

The run still passes. The warning still suggests a disclosure that pip and
attrs don't ask for: commit-check has no switch that turns off a single rule,
so reporting CC014 is as quiet as it gets. See
[Report a rule without enforcing it](../configuration.md#report-a-rule-without-enforcing-it).

[CPython](https://devguide.python.org/getting-started/ai-tools/) sets no rule
for commits at all: disclosing AI use is appreciated but not required, and
triagers judge each contribution by whether its author can explain it in their
own words. A policy like that leaves nothing for commit-check to enforce, so
keep `ai_attribution` at its default, `"ignore"`.

### Recipes from real projects

Many projects enforce their AI policy with a hand-written grep step in CI.
Each policy below fits in a few lines of `cchk.toml`. Add
`conventional_commits = false` if your project does not use Conventional
Commits (see [Checking AI attribution and nothing else](#checking-ai-attribution-and-nothing-else)).

| Project | Its rule for commits | `cchk.toml` |
|---|---|---|
| [Kubernetes](https://www.kubernetes.dev/docs/guide/pull-requests/) | No AI co-author, no AI sign-off, no `Assisted-by` | `ai_attribution = "forbid"` |
| [Linux kernel](https://docs.kernel.org/process/coding-assistants.html) | Every commit signed off by a person; an AI never signs off | `ai_attribution = "disclose"`, `require_signed_off_by = true`, top-level `warn = ["ai_disclosure"]` |
| Nextcloud | `Assisted-by: AGENT_NAME:MODEL_VERSION` on AI-assisted commits; an AI never signs off | `ai_attribution = "disclose"`, `ai_disclosure_pattern = '^[^:\s]+:\S+'` |
| [pip](https://github.com/pypa/pip/blob/main/AI_POLICY.md), [attrs](https://github.com/python-attrs/attrs/blob/main/.github/AI_POLICY.md) | No AI co-author; disclosure not required | `ai_attribution = "disclose"`, top-level `warn = ["ai_disclosure"]` |
| Fedora, FluxCD | Disclose with `Assisted-by:` | `ai_attribution = "disclose"`, `ai_disclosure_trailers = ["Assisted-by"]` |

The Nextcloud recipe, in full:

```toml title="cchk.toml"
[commit]
ai_attribution = "disclose"
ai_disclosure_pattern = '^[^:\s]+:\S+'   # AGENT_NAME:MODEL_VERSION
```

`Assisted-by: ClaudeCode:claude-sonnet-4-6` passes. `Assisted-by: Claude Code`
fails CC014 because it names no model, and `Signed-off-by: Claude
<noreply@anthropic.com>` fails CC016.

Some projects ask every commit to say whether AI was used, with
`Assisted-by: none` when it was not. `disclose` only asks when a commit shows
signs of AI, so pair it with a `message_pattern` that requires the trailer:

```toml title="cchk.toml"
[commit]
ai_attribution = "disclose"
message_pattern = '(?ms).*^Assisted-by:[ \t]*\S'
```

`message_pattern` replaces the Conventional Commits check, so this recipe
cannot be combined with `conventional_commits = true`. A commit with no
`Assisted-by:` line fails CC001; `Assisted-by: none` passes.

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
