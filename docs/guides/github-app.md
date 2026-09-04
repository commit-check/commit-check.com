# GitHub App

The hosted [Commit Check App](https://github.com/marketplace/commit-check)
runs the same rules with no workflow file. Install it on an organization with
**All repositories** selected and every repository, including ones created
later, gets a **Commit Check** result on each commit of every push and pull
request. With **Only select repositories**, only those are checked and new
ones have to be added by hand.

[Install from the GitHub Marketplace](https://github.com/marketplace/commit-check){ .md-button .md-button--primary }

- Reads the repository's `cchk.toml` or `commit-check.toml`, so an existing
  config needs nothing App-specific. A repository without one is checked with
  the defaults and the result is advisory: failures are reported in full, but
  the check is neutral and never blocks a merge until a config file is added.
- Checks every commit in a pull request individually, fork pull requests
  included; **Re-run** on the Checks tab re-checks a commit. A team that
  squash-merges sets [`check = "squash"`](../configuration.md#pull-requests-every-commit-or-the-squash-message)
  and gets one result per pull request instead: the message the squash merge
  would land.
- Skips bot commits (dependabot, renovate).
- Uses no CI minutes: results appear in seconds.

Free for public repositories and for everything on personal accounts. Private
repositories in an organization are covered by the Team plan, which comes with
a 14-day trial.

Choosing between the App and the Action: see
[Where to run it](integrations.md#app-or-action).


The App fetches commit metadata and the configuration file, nothing else, and
stores nothing. See the [privacy page](../privacy.md).
