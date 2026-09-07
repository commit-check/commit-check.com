# Terms of Service

These terms cover the **Commit Check GitHub App** — the hosted service we run,
which you install onto your GitHub account. The command-line tool, the
pre-commit hooks, the GitHub Action and the MCP server are not covered here:
they run inside your own environment and are governed by the [MIT
licence](https://github.com/commit-check/commit-check/blob/main/LICENSE) of the
repository you got them from.

Installing the App means you accept these terms.

## What the service does

The App reads the commits of a push or pull request and the repository's
configuration file, evaluates them against the rules that file turns on, and
posts the result as a GitHub check run. That is all it does. It never writes to
your repository, never rejects a push, and never blocks a merge on its own — a
failing check only blocks a merge if you make it a
[required status check](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-status-checks-before-merging)
yourself.

What it reads and what it stores is set out on the [privacy page](privacy.md).

## Your side

You are responsible for the repositories you install the App on, for the rules
you turn on, and for having the right to install it on an organization's
repositories. Do not attempt to disrupt the service — for instance by sending
traffic designed to exhaust it, or by probing it for vulnerabilities without
telling us first. If you find a security problem, please
[report it](https://github.com/commit-check/commit-check/security/policy) rather
than exploiting it.

## Plans, billing and trials

**Nothing is charged today.** The Marketplace listing is not published yet, so
there is no plan to buy and every repository is checked at no charge. This
section describes what will apply once it is; the
[pricing section](index.md#pricing) and the
[App guide](guides/github-app.md#plans) say the same, and will say so before
anything changes.

Public repositories are free on any account, and so is everything on a personal
account. An organization's private repositories will be covered by the Team
plan, at the price shown in the pricing section.

Billing, trials, renewals, cancellations and refunds will be handled by GitHub
under the [GitHub Marketplace Terms of
Service](https://docs.github.com/en/site-policy/github-terms/github-marketplace-terms-of-service),
not by us — we never see your payment details. The Team plan comes with a
14-day free trial; cancelling is done from your GitHub account's billing
settings and takes effect at the end of the current period.

If the price changes, the change applies to your account from the next
renewal, and GitHub notifies you.

## Availability

The App is offered as is. We aim to keep it running and to fix what breaks, but
we do not promise a level of uptime, and there is no support commitment beyond
the [issue tracker](https://github.com/commit-check/commit-check/issues).
We may change how the service works, or stop running it, with notice on this
site and on the Marketplace listing.

If the hosted App stops being available to you, the
[GitHub Action](guides/github-actions.md) reads the same configuration file and
reports the same rule IDs. Nothing you write in `cchk.toml` is locked to the
hosted service.

## Liability

To the extent the law allows, the App is provided without warranty of any kind,
and we are not liable for indirect or consequential loss arising from using it
— including anything that follows from a check run that passed when you think
it should have failed, or failed when you think it should have passed. Commit
Check validates commit metadata; it is not a review, a test suite or a security
control, and it is not a substitute for any of them.

Where liability cannot be excluded, it is limited to what you paid for the
service in the twelve months before the claim.

## Ending it

You can end these terms at any time by uninstalling the App from your account.
We may suspend or end an installation that breaches these terms, or that is
being used to disrupt the service.

## Changes to these terms

Changes are published on this page, and the date below changes with them.
Continuing to use the App after a change means you accept it. If a change
matters materially to paying accounts, we will also note it on the Marketplace
listing.

## Contact

[Open an issue](https://github.com/commit-check/commit-check/issues) for
anything about these terms or the service.

_Last updated: 2026-09-07._
