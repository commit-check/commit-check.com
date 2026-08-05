# Troubleshooting

## A check fails and you need the commit through anyway

Every check can be bypassed. Doing so is sometimes the right call — you are
mid-rebase, or the rule is wrong and fixing it properly can wait — but the
bypass is the second thing to reach for. The first is reading what failed:
every diagnostic names the rule, quotes the value that failed it, and links to
the page explaining it.

Take an author name check that rejects a one-character name:

```shell
check committer name.....................................................Failed
- hook id: check-author-name
- exit code: 1

Commit rejected by Commit-Check.

CC101 author-name check failed ==> 12
The committer name seems invalid
Suggest: git config user.name 'Your Name'
Docs: https://commit-check.com/rules/#cc101
```

`12` is the value Git actually recorded as the author — usually a sign that
`user.name` was never set on this machine, or was set by a script. The fix is
the one the `Suggest:` line gives:

```shell
git config user.name "Your Name"
git commit --amend --reset-author --no-edit
```

### Skipping one hook

When the check is genuinely wrong for a single commit, skip that hook by ID and
leave the rest running. `SKIP` is a
[pre-commit](https://pre-commit.com/#temporarily-disabling-hooks) feature, so it
takes the hook's `id`, not the rule ID:

```shell
SKIP=check-author-name git commit --amend --no-edit
```

The IDs are `check-message`, `check-branch`, `check-author-name`,
`check-author-email` and `check-no-force-push`.

### Skipping every hook

`--no-verify` bypasses the whole pre-commit run — Commit Check and everything
else you have configured:

```shell
git commit --amend --no-edit --no-verify
```

!!! warning "A local bypass is not a CI bypass"

    `SKIP` and `--no-verify` only affect the hooks on your machine. If the same
    policy runs in CI — through the
    [GitHub Action](guides/integrations.md#in-github-actions), say — it will
    check the commit again when you push, and reject it there. To exempt a
    commit everywhere, change the policy rather than the invocation: turn the
    rule off in `cchk.toml`, or add the author to
    [`ignore_authors`](configuration.md#every-option) if the exemption is
    permanent.

## A rule fires that you never turned on

Commit Check is not silent by default. Whichever checks you asked for run with
their defaults already applied, even with no config file present: `--message`
enforces Conventional Commits, the 5–80 character subject limits and an
allow-list of ten commit types; `--branch` enforces Conventional Branch and an
allow-list of twenty-one branch types; `--author-name` and `--author-email`
apply the built-in patterns. The *Default* column in the
[rules reference](rules.md#rule-index) shows every rule's starting state, and
the [configuration page](configuration.md) spells the split out.

To see what a given repository is actually enforcing, check which config file
it picked up — the search order is in
[where the config file lives](configuration.md#where-the-config-file-lives), and
`--config` overrides it:

```shell
commit-check --config cchk.toml --message
```

## Nothing is checked at all

A check only runs when its own flag is passed. `commit-check --message` never
evaluates branch rules, and `commit-check --branch` never reads the commit
message — so a hook wired up with the wrong flag passes silently, forever.

```shell
commit-check --message --branch --author-name --author-email
```

Each rule in the [rules reference](rules.md) lists the flag that activates it.

## Something else

If the failure does not match anything above, the JSON output shows exactly
what was evaluated and why, which is usually enough to see where the config
disagrees with the expectation:

```shell
commit-check --message --format json
```

Failing that, [open an issue](https://github.com/commit-check/commit-check/issues)
with that output attached.
