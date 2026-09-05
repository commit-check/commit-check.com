# MCP server

[commit-check-mcp](https://github.com/commit-check/commit-check-mcp) exposes
the same rules to an AI coding agent as
[Model Context Protocol](https://modelcontextprotocol.io/) tools. An agent that
writes commits can check the message, the branch name and the author before
the commit exists, against the repository's own `cchk.toml`, and fix what
fails instead of finding out from the hook or the pull request.

## Add it to the agent

The server runs over stdio and is started by the client. With
[uv](https://docs.astral.sh/uv/) installed nothing else needs installing:

=== "Claude Code"

    ```json title=".claude/settings.local.json or ~/.claude/settings.json"
    {
      "mcpServers": {
        "commit-check": {
          "command": "uvx",
          "args": ["commit-check-mcp"]
        }
      }
    }
    ```

=== "Cursor"

    ```json title=".cursor/mcp.json"
    {
      "mcpServers": {
        "commit-check": {
          "command": "uvx",
          "args": ["commit-check-mcp"]
        }
      }
    }
    ```

=== "Claude Desktop, Windsurf, Cline, Roo Code"

    The same block, in each client's MCP settings file. The
    [README](https://github.com/commit-check/commit-check-mcp#use-with-an-mcp-client)
    lists the file for each.

=== "Zed"

    ```json title="~/.config/zed/settings.json"
    {
      "mcp_servers": {
        "commit-check": {
          "command": "uvx",
          "args": ["commit-check-mcp"]
        }
      }
    }
    ```

=== "Without uv"

    ```console
    $ pip install commit-check-mcp
    $ which commit-check-mcp
    ```

    Then use that absolute path as the `command`, with no `args`.

## Make the agent use it

Tools an agent *can* call are not tools it *will* call. One line in the
project's agent instructions — `CLAUDE.md`, `AGENTS.md`, a Cursor rule — makes
the check part of every commit:

```markdown title="CLAUDE.md"
Before every commit, validate the message with the commit-check MCP tool
(`validate_commit_message`) and rewrite it until it passes.
```

The result the agent gets back is the same structured verdict the CLI prints
with `--format json`: a status, and for each check its value, the error, a
suggestion and — when the correction is unambiguous — the corrected value in
`fix`. A type written `Fix` comes back as `"fix": "fix: add x"`, ready to
apply; a subject with no type at all leaves `fix` empty, and the agent works
from the suggestion instead. See [Reading the JSON](../example.md#reading-the-json).

## The tools

| Tool | Checks |
|---|---|
| `validate_commit_message(message, …)` | A message against the [commit message rules](../rules.md#commit-message-rules) |
| `validate_branch_name(branch?, …)` | A branch name, or the repository's current branch, against the [branch rules](../rules.md#branch-rules) |
| `validate_author_info(author_name?, author_email?, …)` | A name and email, or the repository's git author config, against the [author rules](../rules.md#author-rules) |
| `validate_push_safety(push_refs?, …)` | That a push is not a force push ([CC301](../rules.md#cc301)) |
| `validate_commit_context(message?, branch?, author_name?, author_email?, …)` | Any combination of the above in one call |
| `validate_repository_state(repo_path?, …)` | The latest commit, current branch and author config of a repository, with push safety on request |
| `describe_validation_rules(…)` | The effective configuration after defaults, the repository's file and any overrides |
| `server_health()` | Server, rule engine and SDK versions |

Every validation tool takes the same optional arguments:

- `repo_path` — the repository to validate against; the config file is looked
  up there, in the [usual places](../configuration.md#where-the-config-file-lives).
- `config_path` — a specific TOML file instead; a relative path resolves from
  `repo_path`.
- `config` — inline overrides, merged on top of the defaults and the file, for
  a one-off stricter or looser check.

All tools are read-only. Nothing is committed, pushed or written.

## The same rules, one step earlier

The MCP server reads the same `cchk.toml` as the [pre-commit hook](pre-commit.md),
the [Action](github-actions.md) and the [App](github-app.md), through the same
rule engine, so an agent that passes here passes there. It changes *when* the
verdict arrives: before the commit exists, inside the tool that is writing it,
instead of after, from a hook the agent may not be running or from a check on
the pull request. For a repository that forbids AI attribution trailers
([CC013](../rules.md#cc013)) or requires a sign-off ([CC012](../rules.md#cc012)),
this is where the agent learns it.
