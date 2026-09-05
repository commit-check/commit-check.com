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

On every push and pull request event the App fetches the commits under
test into a temporary directory. The fetch is shallow and filtered
(`--filter=blob:none`), so what comes across the wire is the commit
metadata — message, author, timestamps, the list of paths each commit
touches — plus the contents of exactly one file: the configuration file,
if the repository has one. **The contents of no other file are ever
downloaded**, not even into the temporary directory's object store. The
rules are evaluated, the result is posted as a check run, and the temporary
directory is deleted before the event is considered handled.

For a repository owned by an organization that has no configuration file of
its own, the App reads the organization's configuration file from its
`.github` repository, at the same paths, with the same permission. When a
configuration file inherits from another repository with a `github:`
address, the App fetches that one file too. Configuration files are the only
file contents the App ever reads.

For a private repository owned by an organization, the App also asks GitHub
which Marketplace plan that organization is on, to decide whether the Team
plan applies. That request carries the organization's account id and nothing
about the repository.

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
- The contents of a delivery whose signature does not verify. GitHub signs
  the raw request body, so the App has to receive that body to check the
  signature; an unsigned or mis-signed delivery is rejected at that point,
  before anything in it is parsed or acted on

## Where it runs

The App runs on [Fly.io](https://fly.io) in the `ams` (Amsterdam) region.
Traffic between GitHub and the App is encrypted in transit; GitHub signs
every delivery and the App verifies the signature before doing anything
else.

## Contact

Questions about this page or the App's data handling:
[open an issue](https://github.com/commit-check/commit-check/issues).

_Last updated: 2026-09-03._
