# Migrating from v1

Version 2.0 replaced the YAML configuration with TOML. The change is mechanical
— nothing about what Commit Check validates went away — but the two formats
express policy very differently, and there is no automatic conversion.

In v1 a config file was a list of checks, each carrying its own regex, error
message and suggestion. You wrote the pattern; Commit Check ran it. In v2 the
patterns are built in and the file selects and tunes them by name. A v1 file
was mostly regex; a v2 file is mostly booleans.

The practical consequence: you do not translate a v1 file line by line. You
decide which rules you want and write those down, which is usually far shorter.

## Converting the file

Take a representative v1 config:

```yaml title=".commit-check.yml (v1)"
checks:
- check: message
    regex: '^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test){1}(\([\w\-\.]+\))?(!)?: ([\w ])+([\s\S]*)|(Merge).*|(fixup!.*)'
    error: "The commit message should be structured as follows:\n\n
    <type>[optional scope]: <description>\n
    [optional body]\n
    [optional footer(s)]\n\n
    More details please refer to https://www.conventionalcommits.org"
    suggest: please check your commit message whether matches above regex

- check: branch
    regex: ^(bugfix|feature|release|hotfix|task|chore)\/.+|(master)|(main)|(HEAD)|(PR-.+)
    error: "Branches must begin with these types: bugfix/ feature/ release/ hotfix/ task/ chore/"
    suggest: run command `git checkout -b type/branch_name`

- check: author_name
    regex: ^[A-Za-zÀ-ÖØ-öø-ÿĀ-ſƀ-ɏ ,.\'-]+$|.*(\[bot])
    error: The committer name seems invalid
    suggest: run command `git config user.name "Your Name"`

- check: author_email
    regex: ^.+@.+$
    error: The committer email seems invalid
    suggest: run command `git config user.email yourname@example.com`

- check: commit_signoff
    regex: Signed-off-by:.*[A-Za-z0-9]\s+<.+@.+>
    error: Signed-off-by not found in latest commit
    suggest: run command `git commit -m "conventional commit message" --signoff`

- check: merge_base
    regex: main # it can be master, develop, devel etc based on your project.
    error: Current branch is not rebased onto target branch
    suggest: Please ensure your branch is rebased with the target branch
```

Every one of those checks still exists. Named rather than spelled out, the
whole file becomes:

```toml title="cchk.toml (v2)"
[commit]
conventional_commits = true
require_signed_off_by = true

[branch]
conventional_branch = true
require_rebase_target = "main"
```

The regexes are gone because they were restating the built-in behaviour. So are
`error` and `suggest`: Commit Check now supplies both, along with a stable rule
ID and a link to the rule's documentation.

!!! warning "Check your type lists before deleting the old file"

    "Restating the built-in behaviour" is nearly true, not exactly true, and
    the gap is silent — the shorter file above accepts slightly less than the
    v1 one it replaces. Two types in that v1 example are missing from the v2
    defaults:

    - `revert` as a commit type. `revert: drop the cache` passed under v1 and
      is rejected by the default `allow_commit_types`. (Unrelated to
      `allow_revert_commits`, which governs Git's own `Revert "..."` commits
      and is on by default.)
    - `task` as a branch type. `task/CC-42` passed under v1 and is rejected by
      the default `allow_branch_types`.

    Keep them by naming the list you want, remembering that setting either
    option replaces the default rather than adding to it:

    ```toml
    [commit]
    allow_commit_types = ["build", "chore", "ci", "docs", "feat", "fix",
                          "perf", "refactor", "revert", "style", "test"]

    [branch]
    allow_branch_types = ["bugfix", "chore", "feature", "hotfix", "release", "task"]
    ```

    Compare your own v1 regex against
    [every option](configuration.md#every-option) before deleting it — this is
    the one part of the migration that fails quietly, months later, on a commit
    that used to be fine.

### What each v1 check became

| v1 `check:` | v2 option | Rule |
|---|---|---|
| `message` | `[commit] conventional_commits` | [CC001](rules.md#cc001) |
| `branch` | `[branch] conventional_branch` | [CC201](rules.md#cc201) |
| `author_name` | `[commit] author_name_pattern` | [CC101](rules.md#cc101) |
| `author_email` | `[commit] author_email_pattern` | [CC102](rules.md#cc102) |
| `commit_signoff` | `[commit] require_signed_off_by` | [CC012](rules.md#cc012) |
| `merge_base` | `[branch] require_rebase_target` | [CC202](rules.md#cc202) |
| `imperative` | `[commit] subject_imperative` | [CC003](rules.md#cc003) |

The two `*_pattern` options are the exception to "no more regexes": they exist
so an author policy stricter than the default stays expressible.

### Keeping a custom message format

If the v1 `regex` enforced something that is not Conventional Commits — JIRA
smart commits, say — that is what `message_pattern` is for. Set it and it
replaces the generated Conventional Commits pattern entirely:

```toml title="cchk.toml"
[commit]
message_pattern = "^PROJ-\\d+: .+"
```

## Converting the command line

Only the config flag changed, and only because the file did:

```console
$ commit-check --config .commit-check.yml    # v1
$ commit-check --config cchk.toml            # v2
```

A config file is now optional. With none, the defaults apply immediately:

```console
$ commit-check --message --branch
```

## Doing the migration

1. Keep the old file until you are done:

    ```console
    $ cp .commit-check.yml .commit-check.yml.backup
    ```

2. Write `cchk.toml` — in the repository root or in `.github/`. Use the table
   above rather than translating regexes.

3. Check it against real commits without failing anything, which is what
   `--dry-run` is for:

    ```console
    $ commit-check --message --branch --author-name --author-email --dry-run
    ```

4. Try a message that should fail, so you know the policy is doing something:

    ```console
    $ echo "nonsense" | commit-check --message
    ```

    A passing run on a message that ought to fail usually means the config file
    was not found — see
    [where the config file lives](configuration.md#where-the-config-file-lives).

5. Delete `.commit-check.yml` and the backup.

## If something does not work

**The config file is not found.** It has to be named `cchk.toml` or
`commit-check.toml`, in the repository root or `.github/`. Any other name needs
`--config`.

**TOML fails to parse.** Usually unquoted strings, `True` instead of `true`, or
a trailing comma in an array. Editors validate the file against the published
schema — see
[where the config file lives](configuration.md#where-the-config-file-lives).

**A rule does not behave as expected.** Check the option name and its default in
[every option](configuration.md#every-option); the `allow_*` options in
particular describe what is *permitted*, so `false` is the strict setting.

**Something else.** [Open an issue](https://github.com/commit-check/commit-check/issues)
— include the output of `commit-check --message --format json`.
