# Command-line recipes

Ways to invoke the checks directly. For wiring them into a workflow, see
[Integrations](guides/integrations.md) instead — that covers the setup this page
assumes you already have.

Every option, and the environment variable and TOML key that set it, is listed
in [Configuration](configuration.md).

## Checking a commit message

The message can come from the repository, a file, standard input, or a named
revision.

=== "From the repository"

    Validates `HEAD`'s message. This is what the `commit-msg` hook runs.

    ```console
    $ commit-check -m
    ```

=== "From a file"

    ```console
    $ commit-check -m commit_message.txt
    ```

=== "From stdin"

    Useful in scripts and for trying a message before committing it.

    ```console
    $ echo "feat(auth): add OAuth2 login" | commit-check -m
    ```

=== "From a revision"

    `--rev` names the commit under test — anything `git rev-parse`
    understands. A revision that does not resolve is a one-line error before
    any check runs.

    ```console
    $ commit-check -m --rev HEAD~1
    $ commit-check -m --rev 1a2b3c4
    ```

    A revision and a message file would name two different subjects for the
    same checks, so passing both is rejected; stdin is likewise not consulted
    while `--rev` is set.

### Trying a message before you write it

```console
$ echo "updated the parser" | commit-check -m
CC001 message check failed ==> updated the parser
The commit message should follow Conventional Commits.
Suggest: Use <type>(<scope>): <description>, where <type> is one of: feat, fix, ...
Docs: https://commit-check.com/rules/#cc001
```

Fix it and it goes quiet:

```console
$ echo "fix(parser): handle empty input" | commit-check -m
```

### Multi-line messages

A body and trailers survive a heredoc, so you can test the whole thing:

```console
$ cat > /tmp/msg.txt << 'EOF'
fix(auth): resolve login timeout

Users were timing out during login. Raises the session timeout and
reports the failure instead of hanging.

Fixes #123
EOF
$ commit-check -m /tmp/msg.txt
```

## Checking the branch

```console
$ commit-check --branch
```

Runs [CC201](rules.md#cc201), and [CC202](rules.md#cc202) if
`require_rebase_target` is set. `master`, `main`, `HEAD` and `PR-*` are always
accepted; everything else needs a `<type>/<description>` shape:

```text
fix/empty-config-crash
feature/role-caching
release/v1.2.0
```

## Checking the committer

```console
$ commit-check --author-name --author-email
```

Either flag works alone. [CC101](rules.md#cc101) and
[CC102](rules.md#cc102) describe what the built-in patterns accept and how to
tighten them.

Without `--rev`, these validate the *local git config* — whoever is about to
commit — falling back to `HEAD`'s author only when no identity is configured.
That is the right subject for a hook and the wrong one for CI: an existing
commit's identity is a fact about the commit, not about the operator running
the check. Add `--rev` and both checks read that commit's recorded author, and
the config is never consulted:

```console
$ commit-check --author-name --author-email --rev HEAD
```

## Blocking force pushes

```console
$ commit-check --no-force-push
```

Compares the current branch against its upstream and fails if pushing would
require a force. Better as a `pre-push` hook, which sees the actual refs being
pushed:

```yaml title=".pre-commit-config.yaml"
repos:
  - repo: https://github.com/commit-check/commit-check
    rev: v2.15.1
    hooks:
      - id: check-no-force-push
        stages: [pre-push]
```

!!! warning "Piping `git push` into it does not prevent anything"

    `git push | commit-check --no-force-push` reads too late — the push has
    already started — and `git push` output does not carry the ref lines Git
    hands to a `pre-push` hook. Install the hook instead.

## Pointing at a different config

```console
$ commit-check -m --config /path/to/cchk.toml
```

Useful for testing a policy change before committing it, or for a monorepo
where one directory follows different rules. See
[Configuration](configuration.md) for where the file is looked up by default
and how CLI, environment and file settings override each other.

## Output for scripts and CI

=== "JSON"

    Machine-readable, one object per check, including `rule_id` and `docs_url`.

    ```console
    $ commit-check -m --format json
    ```

=== "Compact"

    One line per failure. Implies `--no-banner`.

    ```console
    $ commit-check -m --compact
    [FAIL] CC003 subject_imperative: docs: revamped the profile
    ```

=== "No banner"

    Plain text without the ASCII art, which is noise in a CI log.

    ```console
    $ commit-check -m --no-banner
    ```

=== "Dry run"

    Reports problems but always exits `0`. For adopting the policy on a
    repository whose history is not clean yet.

    ```console
    $ commit-check -m --dry-run
    ```

### Color and links

Output adapts to where it is going. A terminal gets ANSI color, and on
terminals that render OSC 8 hyperlinks the rule ID is itself a link to its
documentation. Piped or redirected output — a CI log, a file — gets plain
text with a `Docs:` line instead, so nothing is lost and no escape codes
leak into places that read them as noise.

To override the detection:

| Variable | Effect |
| --- | --- |
| `NO_COLOR=1` | no color, wherever it runs ([no-color.org](https://no-color.org)) |
| `FORCE_COLOR=1` / `FORCE_COLOR=0` | color on or off, outranking everything else |
| `FORCE_HYPERLINK=1` / `FORCE_HYPERLINK=0` | linked rule IDs on or off |

### Checking a range of commits

`--rev` makes each commit addressable without checking it out or piping its
message, and it is the only way the author checks apply to the commit rather
than to the local config:

```bash title="check-recent.sh"
#!/usr/bin/env bash
# Check the last N commits; exits non-zero if any fail.

# Resolved before the loop rather than inside it: an unreadable range or a
# directory that is not a repository would otherwise expand to nothing, and
# a loop that never runs would report success.
shas=$(git rev-list -n "${1:-10}" HEAD) || exit 1

status=0
for sha in $shas; do
  if ! commit-check -m --author-name --author-email --rev "$sha" --compact; then
    echo "  ↑ $sha"
    status=1
  fi
done
exit $status
```

On a `pull_request` checkout the same loop covers exactly the commits the PR
adds — `HEAD` is GitHub's synthetic merge commit, whose first parent is the
base branch and second the PR branch:

```console
$ git rev-list HEAD^1..HEAD^2
```

### When a check is skipped

A check that had nothing to judge reports a **skip**, not a pass. The common
case is a merge subject: `Merge branch 'x'` is git's writing, so
[CC002](rules.md#cc002), [CC003](rules.md#cc003), [CC004](rules.md#cc004) and
[CC005](rules.md#cc005) decline it rather than grade prose the author never
wrote. Only git's literal `Merge ` prefix qualifies (plus `fixup! ` for
CC003); a subject that merely starts with the lowercase word is judged like
any other.

Text mode names every skipped check in one line on stderr, leaving stdout and
the exit code untouched — a skip is still not a failure:

```console
$ echo "Merge branch 'main' into topic" | commit-check -m --no-banner
⊘ skipped (not validated): subject-max-length, subject-min-length
```

In JSON each skipped check carries `"status": "skip"`, distinct from `"pass"`.

!!! warning "A green run can still have validated nothing"

    On a `pull_request` checkout, `HEAD` is the synthetic merge commit — so a
    bare `commit-check -m` exits `0` with every subject rule skipped. The
    notice makes that visible; the fix is to check what you actually mean:
    the PR title piped on stdin, or each branch commit via `--rev` as above.

### Reading the JSON

```console
$ commit-check -m --format json | jq -r '.checks[] | select(.status == "fail") | .rule_id'
CC001
```

Each failed check carries the rule ID, the offending value, the suggestion and
a link to its documentation — the same information the text output prints, in a
form other tools can consume.
