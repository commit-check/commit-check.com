---
hide:
  - navigation
  - toc
template: home.html
title: Commit Check
description: Enforce commit message, branch naming, author and signoff standards across your CLI, pre-commit hooks, CI, and AI agents.
---

<!-- markdownlint-disable MD041 MD033 MD036 MD025 -->

# Commit Check

## One config, enforced everywhere

Write the policy once. The same rules run on a developer's laptop, in CI, and in
whatever your AI agent is committing on your behalf.

=== "Command line"

    ```console
    $ commit-check --message --branch
    CC003 subject_imperative check failed ==> docs: revamped the profile
    Commit message should use imperative mood (e.g., 'fix bug' not 'fixed bug')
    Suggest: Change the first verb to imperative form
    Docs: https://commit-check.com/rules/#cc003
    ```

=== "pre-commit"

    ```yaml title=".pre-commit-config.yaml"
    repos:
      - repo: https://github.com/commit-check/commit-check
        rev: v2.11.0
        hooks:
          - id: check-message
          - id: check-branch
          - id: check-author-email
    ```

=== "GitHub Actions"

    ```yaml title=".github/workflows/commit-check.yml"
    - uses: commit-check/commit-check-action@v2
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        message: true
        branch: true
        pr-comments: ${{ github.event_name == 'pull_request' }}
    ```

=== "AI agents"

    ```json title="MCP server"
    {
      "mcpServers": {
        "commit-check": {
          "command": "uvx",
          "args": ["commit-check-mcp"]
        }
      }
    }
    ```

## What it checks

<div class="grid cards" markdown>

-   :material-message-text-outline:{ .lg .middle } __Commit messages__

    ---

    Conventional Commits by default, or your own pattern. Subject length, mood,
    capitalisation, required body, forbidden merge/fixup/WIP commits.

    [:octicons-arrow-right-24: CC001–CC013](rules.md#commit-message-rules)

-   :material-source-branch:{ .lg .middle } __Branch names__

    ---

    Conventional Branch naming, plus rebase checks that catch a branch drifting
    behind its target before CI wastes a run on stale code.

    [:octicons-arrow-right-24: CC201–CC202](rules.md#branch-rules)

-   :material-account-check-outline:{ .lg .middle } __Committer identity__

    ---

    Catch commits authored by `ec2-user` on a build box, or require everyone to
    contribute from a company address.

    [:octicons-arrow-right-24: CC101–CC102](rules.md#author-rules)

-   :material-file-sign:{ .lg .middle } __Signoff and DCO__

    ---

    Require the `Signed-off-by` trailer locally, so contributors find out before
    CI rejects the pull request.

    [:octicons-arrow-right-24: Signoff guide](guides/signoff.md)

-   :material-robot-outline:{ .lg .middle } __AI attribution__

    ---

    Whatever your project has decided about AI-assisted commits, enforce it
    mechanically instead of relitigating it in review.

    [:octicons-arrow-right-24: AI attribution guide](guides/ai-attribution.md)

-   :material-office-building-outline:{ .lg .middle } __Org-wide policy__

    ---

    Inherit a base config from a shared repository, then let each project
    override only what it needs.

    [:octicons-arrow-right-24: Organization guide](guides/organization.md)

</div>

## Built to be trusted

<div class="grid cards" markdown>

-   :material-shield-check:{ .lg .middle } __SLSA Level 3__

    ---

    Build provenance with artifact attestation you can verify before
    installing.

-   :material-tag-outline:{ .lg .middle } __Stable rule IDs__

    ---

    Every diagnostic carries an ID like `CC003` that never changes, so you can
    cite it in review, suppress it, or feed it to tooling.

-   :material-source-commit:{ .lg .middle } __Used in production__

    ---

    Running at Apache, Texas Instruments, Mila, and
    [many more](https://github.com/commit-check/commit-check-action/network/dependents).

</div>

## Trusted by developers worldwide

<div class="trusted-by" markdown>

**Used by developers and organizations worldwide in their production workflows.**

<div class="logo-grid">
  <div class="logo-item">
    <img src="https://github.com/apache.png" alt="Apache" title="Apache">
    <span>Apache</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/discovery-unicamp.png" alt="Discovery Unicamp" title="Discovery Unicamp">
    <span>Discovery Unicamp</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/TexasInstruments.png" alt="Texas Instruments" title="Texas Instruments">
    <span>Texas Instruments</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/opencadc.png" alt="OpenCADC" title="OpenCADC">
    <span>OpenCADC</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/extrawest.png" alt="Extrawest" title="Extrawest">
    <span>Extrawest</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/Chainlift.png" alt="Chainlift" title="Chainlift">
    <span>Chainlift</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/mila-iqia.png" alt="Mila" title="Mila">
    <span>Mila</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/RLinf.png" alt="RLinf" title="RLinf">
    <span>RLinf</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/istio-ecosystem.png" alt="Istio Ecosystem" title="Istio Ecosystem">
    <span>Istio Ecosystem</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/Juniper.png" alt="Juniper Networks" title="Juniper Networks">
    <span>Juniper Networks</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/PnX-SI.png" alt="French National Parks" title="French National Parks">
    <span>French National Parks</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/OpenDriveLab.png" alt="OpenDriveLab" title="OpenDriveLab">
    <span>OpenDriveLab</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/UT-Austin-RobIn.png" alt="UT Austin RobIn" title="UT Austin RobIn">
    <span>UT Austin RobIn</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/WorldArena2.png" alt="WorldArena2" title="WorldArena2">
    <span>WorldArena2</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/moniqohq.png" alt="moniqo" title="moniqo">
    <span>moniqo</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/elumobility.png" alt="elu mobility" title="elu mobility">
    <span>elu mobility</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/OpenEnergyPlatform.png" alt="Open Energy Platform" title="Open Energy Platform">
    <span>Open Energy Platform</span>
  </div>
  <div class="logo-item">
    <img src="https://github.com/collective.png" alt="Collective" title="Collective">
    <span>Collective</span>
  </div>
</div>

</div>

## Ecosystem

Commit Check is a family of projects — one engine, multiple surfaces.
Write your policy **once** in a `cchk.toml`, enforce it **everywhere**.

<div class="grid cards" markdown>

-   :fontawesome-brands-python: __commit-check__ `v2.11.0`

    ---

    **Core engine** — Python CLI, library & pre-commit hooks.

    :material-star: AI attribution governance, message patterns, JSON output

    [:octicons-arrow-right-24: Docs](getting-started/installation.md)
    [:octicons-arrow-right-24: Repo](https://github.com/commit-check/commit-check)

-   :material-github: __commit-check-action__ `v2.10.0`

    ---

    **GitHub Action** — seamless CI integration with PR comments.

    :material-star: Windows runner, PR title validation

    [:octicons-arrow-right-24: Docs](guides/github-actions.md)
    [:octicons-arrow-right-24: Repo](https://github.com/commit-check/commit-check-action)

-   :material-robot: __commit-check-mcp__ `v0.1.7`

    ---

    **MCP Server** — structured tools for AI coding agents.

    :material-star: AI attribution governance, message patterns

    [:octicons-arrow-right-24: Repo](https://github.com/commit-check/commit-check-mcp)

</div>

[See all projects →](projects.md){ .md-button }

## Ready in two minutes

```console
$ pip install commit-check
$ commit-check --message --branch
```

No configuration file needed to start — sensible defaults apply immediately, and
you tighten them when you are ready.

[Install :octicons-arrow-right-24:](getting-started/installation.md){ .md-button .md-button--primary }
[Why Commit Check?](getting-started/why.md){ .md-button }

---

<div class="community-section" markdown>

## Join our community

**Be part of a growing ecosystem of developers who care about Commit Check.**

[GitHub Issue :fontawesome-brands-github:](https://github.com/commit-check/commit-check/issues){ .md-button }
[GitHub Pull Request :fontawesome-brands-github:](https://github.com/commit-check/commit-check/pulls){ .md-button }

</div>
