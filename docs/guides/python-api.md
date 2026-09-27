# Python API

`commit_check.api` runs the same checks as the command line from Python code —
a bot, a server-side hook, an agent you are building — without starting a
subprocess. Each function takes the value to check and returns a plain `dict`
in the shape `commit-check --format json` prints, ready to branch on, log or
hand to a model. It ships with the package: `pip install commit-check` is all
it needs.

```python
from commit_check.api import validate_message

result = validate_message("Fix: add streaming support")
for check in result["checks"]:
    if check["status"] == "fail":
        print(check["rule_id"], check["suggest"])
        print("fix:", check["fix"])
```

```text
CC001 Use "fix: add streaming support"
fix: fix: add streaming support
```

## Functions

| Function | Checks | When the value is left out |
|---|---|---|
| `validate_message(message, *, config=None)` | The commit message: Conventional Commits, subject length, case and mood, body, sign-off, AI attribution — whichever rules the config enables | Required |
| `validate_branch(branch=None, *, config=None)` | The branch name, and its rebase target when one is configured | The current branch, from `git branch --show-current` |
| `validate_author(name=None, email=None, *, config=None)` | The author's name and email | Both come from `git config` |
| `validate_tag(tag=None, *, config=None)` | Tag names, one per line | The tags pointing at `HEAD`; with none, the result is `skip` |
| `validate_push(push_refs=None, *, config=None)` | That a push is not a force push; the check is always on here | Pass the pre-push lines, `<local ref> <local sha> <remote ref> <remote sha>`, one per line — without them there is nothing to compare |
| `validate_all(message=None, branch=None, author_name=None, author_email=None, *, config=None)` | Message, branch and author together, in one result | Whatever is left out is not checked, and nothing is read from git |

The git lookups run in the current working directory, as the CLI's do.

```python
from commit_check.api import validate_all

result = validate_all(message="feat: implement new feature", branch="user-login")
print(result["status"])
for check in result["checks"]:
    print(check["rule_id"], check["check"], check["status"])
```

```text
fail
CC001 message pass
CC004 subject_max_length pass
CC005 subject_min_length pass
CC201 branch fail
```

## The result

Every function returns the same shape:

```python
{
    "status": "pass" | "fail" | "skip",
    "warnings": 0,               # how many checks have status "warn"
    "checks": [
        {
            "rule_id": "CC001",
            "check": "message",
            "status": "pass" | "fail" | "warn" | "skip",
            "value": "...",      # what was checked
            "error": "...",      # why it failed
            "suggest": "...",    # advice for a person
            "fix": "...",        # the corrected value, or "" when it takes judgment
            "docs_url": "https://commit-check.com/rules/#cc001",
        },
    ],
}
```

- **Only `fail` is a rejection.** Code that branches on `status == "fail"`
  keeps working whatever else the result holds.
- **`skip` is not `pass`.** A check skips when it never ran — the author is in
  `ignore_authors`, or there was nothing to check — and the top-level `status`
  is `skip` only when every check skipped. A skipped run validated nothing, so
  do not read it as approval.
- **`warn`** is a rule listed under the config's `warn`: reported in full,
  never a failure. The top-level `status` stays `pass`, and `warnings` counts
  them.
- **`fix`** is non-empty only when the correction is mechanical, so it can be
  applied as it stands; otherwise follow `suggest`.
  [Reading the JSON](../example.md#reading-the-json) lists the cases.

## Configuration

The API does not read `cchk.toml`. It starts from the built-in defaults and
merges the `config` you pass, a `dict` shaped like the TOML file:

```python
from commit_check.api import validate_message

result = validate_message(
    "docs: update readme",
    config={"commit": {"allow_commit_types": ["feat", "fix"]}},
)
print(result["status"])
print(result["checks"][0]["suggest"])
```

```text
fail
Use <type>(<scope>): <description>, where <type> is one of: feat, fix
```

A top-level `warn` works as it does in the file:

```python
from commit_check.api import validate_message

result = validate_message("add streaming support", config={"warn": ["message"]})
print(result["status"], result["warnings"])
```

```text
pass 1
```

To apply a repository's own policy, load its file and pass it along:

```python
import tomllib  # on Python 3.10: import tomli as tomllib

from commit_check.api import validate_message

with open("cchk.toml", "rb") as f:
    config = tomllib.load(f)

result = validate_message("feat: add streaming support", config=config)
```

On Python 3.10, `tomli` is already installed: commit-check depends on it
there. `inherit_from` is not followed this way; only the file's own keys
apply. Every key is in the [configuration reference](../configuration.md).

## Fixing until it passes

An agent can apply `fix` and check again — the loop the
[MCP server](mcp.md) teaches its clients:

```python
from commit_check.api import validate_message

message = "Fix: add streaming support"
for _ in range(3):
    result = validate_message(message)
    fixes = [c["fix"] for c in result["checks"] if c["status"] == "fail" and c["fix"]]
    if result["status"] != "fail" or not fixes:
        break
    message = fixes[0]

print(result["status"], message)
```

```text
pass fix: add streaming support
```

When `fix` is empty the correction takes judgment — choosing a type for a bare
subject, shortening a long one — and `suggest` says what is needed.
