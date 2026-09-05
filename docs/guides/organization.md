# Across an organization

Copying `cchk.toml` into forty repositories works until the day you want to
change it. One shared config fixes that, two ways: the [GitHub App](github-app.md)
applies the organization's file to every repository that has none of its own,
with nothing added to any repository; and `inherit_from` lets a repository that
does have a config start from the shared one and override only what it
genuinely needs.

## The shared config

Put the policy in a repository every project can read — GitHub's `.github`
repository is the conventional home:

```toml title="my-org/.github → cchk.toml"
[commit]
conventional_commits = true
subject_imperative = true
subject_max_length = 72
allow_merge_commits = false

[branch]
conventional_branch = true
allow_branch_types = ["feature", "bugfix", "hotfix", "release", "chore"]
```

## With the App: nothing to add

Where the [GitHub App](github-app.md) is installed on the organization, that
file is already in force: a repository with no `cchk.toml` of its own is
checked against the organization's, including repositories created tomorrow,
and the check run's last line says so. The App reads the file with its own
credentials, so the `.github` repository can be private. A personal account's
`.github` repository does the same for that account's repositories. A repository that
commits its own config uses that instead — to build on the shared one rather
than replace it, inherit it, below.

The hook, the CLI and the Action do not know about the organization's file
unless a repository points at it, which is what the next section is for.

## Inheriting it

Each repository then needs one line:

```toml title="any-repo → .github/cchk.toml"
inherit_from = "github:my-org/.github:cchk.toml"
```

Local settings win, so a project with a different constraint overrides just that
one option:

```toml title="a-repo-with-longer-subjects → .github/cchk.toml"
inherit_from = "github:my-org/.github:cchk.toml"

[commit]
subject_max_length = 100      # everything else comes from the org config
```

## Pinning the version

By default the shorthand resolves to the parent repository's default branch,
which means a change to the org config takes effect everywhere on the next run.
That is usually what you want. When it isn't, pin to a ref:

```toml
inherit_from = "github:my-org/.github@v1:cchk.toml"
```

## Other sources

=== "GitHub shorthand"

    ```toml
    inherit_from = "github:my-org/.github:cchk.toml"
    ```

=== "Local path"

    ```toml
    inherit_from = "../../shared/org-cchk.toml"
    ```

    Useful in a monorepo, where the shared config is already checked out.

=== "HTTPS URL"

    ```toml
    inherit_from = "https://example.com/shared/cchk.toml"
    ```

    Plain HTTP is rejected.

!!! warning "Inheritance fails open"

    If the parent config is unreachable — a network blip, a renamed file, a
    private repository — Commit Check silently falls back to the local config
    rather than failing the build. This keeps CI green during an outage, but it
    also means a typo in `inherit_from` is easy to miss. Verify the merged
    result when you first set it up:

    ```console
    $ commit-check --message --format json
    ```

## Rolling it out

Turning on a strict policy across an organization at once produces a wall of
red. A gentler sequence:

1. Ship the org config with [`dry-run`](github-actions.md#reporting-without-failing) enabled in
   CI, so violations are reported but nothing blocks.
2. Look at what actually fails. Some rules will turn out to be wrong for some
   teams — that is information, not an obstacle.
3. Turn off `dry-run` for repositories whose history is already clean.
4. Tighten the shared config over time.
