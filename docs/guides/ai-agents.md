# With AI coding agents

A coding agent commits more often than a person, and when a hook rejects a
commit it can reach for `git commit --no-verify` to get past it. Agents that
work in the cloud often run no hook at all. Four layers keep the policy in
place, cheapest first. Only the last one cannot be skipped.

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

For more than one line of guidance, install the
[agent skill](https://github.com/commit-check/commit-check/blob/main/skills/commit-check/SKILL.md).
It teaches the agent to read `cchk.toml`, check a message before it commits,
follow the [AI attribution policy](policies.md) and never skip the hook. It
uses the [Agent Skills](https://agentskills.io) format, which Claude Code,
GitHub Copilot, Codex, Cursor and others load:

```console
$ npx skills add https://github.com/commit-check/commit-check --skill commit-check
```

With the [MCP server](mcp.md) the agent can also check the message as a tool
call; [Make the agent use it](mcp.md#make-the-agent-use-it) has the line to add
for that.

An instruction is read, not enforced: the agent can still decide to skip the
hook.

## Block `--no-verify`

Claude Code runs a [PreToolUse hook](https://code.claude.com/docs/en/hooks)
before each shell command, and a hook that exits with code 2 stops the command
and tells the agent why. This one stops `--no-verify`, and `-n` on
`git commit`:

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
            "command": "\"${CLAUDE_PROJECT_DIR:-.}\"/.claude/hooks/no-verify.sh"
          }
        ]
      }
    ]
  }
}
```

Make the script executable, install [jq](https://jqlang.org/) (without it the
hook stops every command), and commit both files, so everyone who works in the
repository gets the hook. It reads the command as written and does not catch
every way around a hook, such as a command wrapped in `bash -c` or
pre-commit's `SKIP` variable.

The same files work in other agents. [Cursor](https://cursor.com/docs/reference/third-party-hooks)
loads hooks from `.claude/settings.json` (on by default) and treats exit code 2
the same way. [GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/hooks-reference)
reads `.claude/settings.json` in the repository too. The
`${CLAUDE_PROJECT_DIR:-.}` form falls back to the repository root in an agent
that does not set that variable.

## Check before the agent hands over

A blocked `--no-verify` only matters where a commit hook runs. A cloud agent
such as the Copilot coding agent commits in a fresh sandbox, where your
pre-commit hooks were never installed. A stop hook closes that gap: when the
agent is about to finish, it runs Commit Check on every commit of the branch
and, if one fails, sends the agent back to fix it.

```bash title=".claude/hooks/commit-check-stop.sh"
#!/usr/bin/env bash
# Before the agent finishes, check every commit it made on this branch.
# Asks the agent to fix them once per HEAD, so it cannot loop forever.
command -v commit-check >/dev/null || exit 0
base=$(git merge-base HEAD origin/HEAD 2>/dev/null ||
       git merge-base HEAD origin/main 2>/dev/null) || exit 0
marker="$(git rev-parse --git-dir)/commit-check-stop"
[ "$(cat "$marker" 2>/dev/null)" = "$(git rev-parse HEAD)" ] && exit 0

report=""
for sha in $(git rev-list --no-merges "$base"..HEAD); do
  out=$(commit-check --message --rev "$sha" --compact 2>&1)
  [ $? -eq 1 ] && report+="$(git log -1 --format='%h %s' "$sha")"$'\n'"$out"$'\n'
done
[ -z "$report" ] && exit 0

git rev-parse HEAD >"$marker"
jq -cn --arg r "Commit Check failed on these commits:
$report
Reword them so they pass, then finish." '{decision: "block", reason: $r}'
```

Only a failed check (exit code 1) sends the agent back. A config error, a
missing `commit-check` or a branch with no `origin` lets it finish, and the
pull request check below still applies. If the agent stops again without
changing its commits, the hook lets it go.

For Claude Code and Cursor, add a `Stop` entry next to `PreToolUse` in
`.claude/settings.json`:

```json title=".claude/settings.json"
{
  "hooks": {
    "PreToolUse": [ … ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PROJECT_DIR:-.}\"/.claude/hooks/commit-check-stop.sh"
          }
        ]
      }
    ]
  }
}
```

The Copilot coding agent reads only `.github/hooks/*.json` from the
repository, and `agentStop` is its name for the same event:

```json title=".github/hooks/commit-check.json"
{
  "version": 1,
  "hooks": {
    "agentStop": [
      {
        "type": "command",
        "bash": "./.claude/hooks/commit-check-stop.sh"
      }
    ]
  }
}
```

The agent needs `commit-check` in its environment. For the Copilot coding
agent, install it in the setup steps it runs before it starts:

```yaml title=".github/workflows/copilot-setup-steps.yml"
name: Copilot Setup Steps
on: workflow_dispatch
jobs:
  copilot-setup-steps:  # Copilot looks for this exact job name
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/setup-python@v7
        with:
          python-version: '3.x'
      - run: pip install commit-check
```

## Check the pull request

Hooks in the agent are feedback; the agent or a person can still get a bad
commit to the pull request. The check that holds for every agent is the one
on the pull request. The [GitHub App](github-app.md) needs no workflow file
and also checks the agents that commit as an app
([which ones](github-app.md#bots-re-runs-and-commits-checked-twice)); the
[Action](github-actions.md) does the same job in CI. Make the check required
and a commit that skipped the hook still cannot merge, since both look at every
commit of the pull request. The App's check is named **Commit Check**
([enforcing it](github-app.md#enforcing-it)); the Action's takes its job's
name, `commit-check` in [the example](github-actions.md#making-it-a-required-check).
