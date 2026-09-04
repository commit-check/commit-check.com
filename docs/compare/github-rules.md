# Compared with GitHub's built-in rules

GitHub can enforce some of the same policies natively — but the useful ones sit
behind its paid tiers, and the commit-metadata rules specifically behind the
most expensive one:

| Policy | Native GitHub | Commit Check |
|---|---|---|
| Commit message patterns | [Enterprise plan only](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-organization-settings/creating-rulesets-for-repositories-in-your-organization) (from [$21/user/month](https://github.com/pricing)) | Every plan, free |
| Author / committer email patterns | Enterprise plan only | Every plan, free |
| Branch naming patterns | Enterprise plan only | Every plan, free |
| Branch/tag rulesets on a private repository | [Pro or Team plan and up](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets); push rulesets Team and up | Every plan, free |
| Organization-wide rules | Team plan and up, enforced centrally | [Shared config via `inherit_from`](../guides/organization.md) — each repo opts in, local settings override |

For a 20-person team on the GitHub Team plan, turning on native commit message
rules means upgrading every seat from $4 to $21 at current list pricing —
about **$340 a month** for a regex. The failure experience differs too: native
rulesets speak [RE2](https://github.com/google/re2/wiki/Syntax) (no lookaheads)
and report a bare mismatch, while Commit Check failures carry a rule ID, a
concrete suggestion, and a link to [the rule's documentation](../rules.md).

One honest difference in the other direction: GitHub's rules run server-side
and refuse the ref update itself, so nothing lands on the protected branch no
matter how it is pushed. Commit Check's pre-commit hook is fast local feedback
a developer can bypass (`git commit --no-verify`); its enforcement boundary is
CI and a required check, which keeps a violating change from merging. For a
pull-request workflow the outcome is the same — the protected branch never
receives it.
