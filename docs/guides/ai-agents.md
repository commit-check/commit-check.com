# With AI coding agents

A coding agent commits more often than a person, and when a hook rejects a
commit it can reach for `git commit --no-verify` to get past it. Three layers
keep the policy in place, cheapest first. Only the last one cannot be skipped.

## Tell the agent

Put the rule where agents read their instructions. `AGENTS.md` at the
repository root is read by Codex, Cursor, Jules, Devin, the Copilot coding
agent and [many others](https://agents.md/). Claude Code reads it too when the
repository has no `CLAUDE.md`; if it has one, add `@AGENTS.md` to it.

```markdown title="AGENTS.md"
## Commits

Commit messages and branch names follow `cchk.toml`. When the commit-check
hook fails, fix the message and commit again. Never pass `--no-verify` to
`git commit` or `git push`, or `-n` to `git commit`.
```

With the [MCP server](mcp.md) the agent can check the message before it
commits; [Make the agent use it](mcp.md#make-the-agent-use-it) has the line to
add for that.

An instruction is read, not enforced: the agent can still decide to skip the
hook.

## Block it in Claude Code

Claude Code runs a [PreToolUse hook](https://code.claude.com/docs/en/hooks)
before each shell command, and a hook that exits with code 2 stops the command
and tells Claude why. This one stops `--no-verify`, and `-n` on `git commit`:

```bash title=".claude/hooks/no-verify.sh"
#!/usr/bin/env bash
# Stop git from skipping the hooks: --no-verify, or -n on git commit.
# Quoted text becomes _ first, so a commit message that mentions -n passes.
command -v jq >/dev/null || { echo "This hook needs jq." >&2; exit 2; }
cmd=$(jq -r '.tool_input.command' | sed -E "s/\"[^\"]*\"/_/g; s/'[^']*'/_/g")
any='git [^;&|]*--no-verify'
commit='git( +-C +[^ ]+)* +commit[^;&|]* +-[a-zA-Z]*n'

if grep -Eq -e "$any" -e "$commit" <<<"$cmd"; then
  echo "Do not skip the hooks (--no-verify, -n)." \
       "Fix what Commit Check reported and commit again." >&2
  exit 2
fi
```

```json title=".claude/settings.json"
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/no-verify.sh",
            "args": []
          }
        ]
      }
    ]
  }
}
```

Make the script executable, install [jq](https://jqlang.org/) (without it the
hook stops every command), and commit both files, so everyone who works in the
repository with Claude Code gets the hook. It reads the command as written and
does not catch every way around a hook, such as a command wrapped in `bash -c`
or pre-commit's `SKIP` variable.

## Check the pull request

Agents that work in the cloud, such as the Copilot coding agent, Codex, Jules
and Devin, commit in their own sandbox, where no hook runs unless their setup
installs one. The check that holds for every agent is the one on the pull
request. The [GitHub App](github-app.md) needs no workflow file and also
checks the agents that commit as an app
([which ones](github-app.md#bots-re-runs-and-commits-checked-twice)); the
[Action](github-actions.md) does the same job in CI. Make **Commit Check** a
[required check](github-app.md#enforcing-it), and a commit that skipped the
hook still cannot merge.
