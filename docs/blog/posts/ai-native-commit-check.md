---
date:
  created: 2026-06-21
readtime: 6
categories:
  - UPDATES
tags:
  - commit-check
  - automation
  - ai
authors:
  - shenxianpeng
---

# AI-native: JSON output and a Python API

More and more commits are written — or at least drafted — by AI agents and
automation. So Commit Check is also built for machines — not just humans reading
terminal output. This post covers the two
features that make that possible: machine-readable JSON output and an
import-friendly Python API.

<!-- more -->

## Structured output with `--format json`

Add `--format json` to any invocation and Commit Check returns structured data
instead of decorated text. The exit code is unchanged (`0` = pass, `1` = fail),
so existing CI scripts keep working:

```bash
echo "feat: add streaming support" | commit-check -m --format json
```

```json
{
  "status": "pass",
  "checks": [
    { "check": "message",           "status": "pass", "value": "", "error": "", "suggest": "" },
    { "check": "subject_imperative", "status": "pass", "value": "", "error": "", "suggest": "" }
  ]
}
```

When a check fails, each result carries the full `error`
and `suggest` fields an agent needs to **self-correct** — no scraping required:

```bash
echo "wip bad commit" | commit-check -m --format json
```

```json
{
  "status": "fail",
  "checks": [
    {
      "check":   "message",
      "status":  "fail",
      "value":   "wip bad commit",
      "error":   "The commit message should follow Conventional Commits. See https://www.conventionalcommits.org",
      "suggest": "Use <type>(<scope>): <description>, where <type> is one of: feat, fix, docs, ..."
    }
  ]
}
```

Pass the `suggest` string back to an LLM, and it has what it needs to
rewrite the message and retry.

## Quieter text, for humans

If you live in a terminal but find the ASCII banner noisy, two modes dial it
down:

- `--no-banner` keeps the failure details and suggestions but drops the
  ASCII-art banner.
- `--compact` prints a single `[FAIL]` line per failing check (and implies
  `--no-banner`).

```bash
echo "wip bad commit" | commit-check -m --compact
```

```text
[FAIL] message: wip bad commit
```

## The Python API — no subprocess needed

For tools and agents running in Python, spawning a subprocess to validate
a string adds unnecessary overhead. The `commit_check.api` module exposes
functions that return plain dicts — easy to serialize, forward to an LLM,
or chain into a larger workflow:

```python
from commit_check.api import validate_message, validate_branch, validate_all

result = validate_message("feat: add streaming support")
if result["status"] != "pass":
    # hand result straight back to your agent loop
    ...
```

Because the functions return the same structured shape as the JSON output,
you can move between CLI and in-process validation without changing how you
handle results.

## Why this matters

The same policy that protects a human's `git commit` now protects an agent's
automated one — and gives that agent the precise feedback it needs to fix its
own mistakes. One `cchk.toml`, enforced identically whether the author is a
person, a CI job, or a model.

Read more in the
[README](https://github.com/commit-check/commit-check#ai-native-usage).
