# Privacy

This page describes what the **Commit Check GitHub App** reads, what it
keeps, and what it never sees. The command-line tool, the pre-commit hooks
and the GitHub Action run entirely inside your own environment and send
nothing anywhere; this page is about the hosted App only.

## What the App reads

When you install the App, GitHub grants it these permissions and nothing
else:

| Permission | Level | Used for |
|---|---|---|
| Metadata | read | Knowing which repositories it is installed on |
| Contents | read | Fetching the commits under test and the repository's `cchk.toml` / `commit-check.toml` |
| Checks | write | Posting the **Commit Check** result on each commit |
| Pull requests | read | Listing the commits of a pull request |

On every push and pull request event the App performs a shallow, sparse
fetch of the commits under test into a temporary directory: the commit
objects themselves and the configuration file, if any. **No other file in
the repository is ever fetched.** The rules are evaluated, the result is
posted as a check run, and the temporary directory is deleted before the
event is considered handled.

## What the App keeps

Nothing. The App has no database and stores no repository content, commit
messages, author details or configuration. Each event is processed from the
webhook payload and discarded.

The hosting platform retains **operational logs** for a short period. A log
line carries the webhook delivery id, the commit SHA being checked, the id
of the check run created and, when a check could not run, the error text
the tool produced — never an author name or email, and never file content.

## What the App never sees

- Your source code beyond the configuration file named above
- Repositories the App is not installed on
- Anything at all if the webhook signature does not verify — unsigned or
  mis-signed deliveries are rejected before they are read

## Where it runs

The App runs on [Fly.io](https://fly.io) in the `ams` (Amsterdam) region.
Traffic between GitHub and the App is encrypted in transit; GitHub signs
every delivery and the App verifies the signature before doing anything
else.

## Contact

Questions about this page or the App's data handling:
[open an issue](https://github.com/commit-check/commit-check/issues).

_Last updated: 2026-09-03._
