---
hide:
  - navigation
  - toc
template: landing.html
title: Commit Check
description: Catch bad commits before they merge. Messages, branches, authors and AI attribution, checked from your commit hook to every pull request.
---

<!-- markdownlint-disable MD041 MD033 MD036 MD025 -->

<!--
  This page is mostly raw HTML: the sections are laid out by
  stylesheets/landing.css and the two animated demos are driven by
  javascripts/landing.js. Without JavaScript, or with reduced motion
  requested, every demo shows its final frame and every Action panel is
  listed in turn, so nothing here depends on the script to be read.

  Timeline attributes the script reads, all in milliseconds from the start
  of a demo:
    data-on="t"      fades in at t
    data-from="t"    is not displayed before t
    data-until="t"   is not displayed from t on (no-JS: never displayed)
    data-type="t"    types its own text out from t, data-speed ms a key
    data-hl="t"      is highlighted from t
-->

<section class="cc-band cc-band--ink cc-hero" aria-labelledby="cc-title">
<svg class="cc-hero__graph" viewBox="0 0 480 760" aria-hidden="true" focusable="false"><g fill="none" stroke="#2C9CCD" stroke-opacity=".08" stroke-width="2"><path d="M40 0V760M120 0V760M200 0V760M280 0V760M360 0V760M440 0V760"/><path d="M120 180C120 230 200 230 200 280M280 420C280 470 200 470 200 520M40 560C40 610 120 610 120 660M360 120C360 170 440 170 440 220"/></g><g fill="#0B1620" stroke="#2C9CCD" stroke-opacity=".16" stroke-width="2"><circle cx="40" cy="120" r="6"/><circle cx="120" cy="180" r="6"/><circle cx="200" cy="280" r="6"/><circle cx="280" cy="90" r="6"/><circle cx="280" cy="420" r="6"/><circle cx="360" cy="330" r="6"/><circle cx="200" cy="520" r="6"/><circle cx="40" cy="560" r="6"/><circle cx="120" cy="660" r="6"/><circle cx="440" cy="220" r="6"/><circle cx="360" cy="120" r="6"/></g></svg>
<div class="cc-wrap cc-hero__grid">
<div class="cc-hero__copy">
<p class="cc-pill"><span class="cc-pill__dot"></span>Open source · MIT licensed</p>
<h1 id="cc-title" class="cc-display">Catch bad commits <span class="cc-accent">before they merge.</span></h1>
<p class="cc-lede">Commit Check validates commit messages, branch names, authors and sign-offs against one <code>cchk.toml</code> — in your commit hook, in CI, on every pull request and inside your AI agent. When the fix is obvious, it hands you the line.</p>
<div class="cc-actions">
<a class="cc-btn cc-btn--primary" href="guides/github-actions/">Add to GitHub Actions <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h9M8.5 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
<div class="cc-install"><span class="cc-install__sigil" aria-hidden="true">$</span><code>pip install commit-check</code><button class="cc-copy" type="button" data-copy="pip install commit-check" aria-label="Copy the install command"><svg viewBox="0 0 16 16" aria-hidden="true"><rect x="5" y="5" width="8.5" height="8.5" rx="2" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M10.5 3.2A1.5 1.5 0 0 0 9 2H4a2 2 0 0 0-2 2v5a1.5 1.5 0 0 0 1.2 1.5" fill="none" stroke="currentColor" stroke-width="1.4"/></svg></button></div>
</div>
</div>
<!--
  A transcript of a real run: commit-check 2.18.0 as a pre-commit
  commit-msg hook. The hook also prints an ASCII-art banner between
  "exit code: 1" and the CC001 line; it is left out, nothing else is.
-->
<figure class="cc-term" aria-label="A commit-msg hook rejects a commit message, suggests the fix, then accepts the corrected message">
<div class="cc-term__bar" aria-hidden="true"><span class="cc-dots"><i></i><i></i><i></i></span><span>~/app · feature/streaming · commit-msg hook</span></div>
<div class="cc-term__body cc-tl" data-loop="15500">
<div class="cc-line"><span class="cc-sigil">❯ </span><span data-type="400" data-speed="42">git commit -m "Fix: add streaming support"</span><i class="cc-caret" data-until="2500"></i></div>
<div class="cc-line cc-row" data-on="2500"><span>check commit message</span><span class="cc-leader" aria-hidden="true"></span><span class="cc-t-fail">Failed</span></div>
<div class="cc-line cc-t-dim" data-on="2650">- hook id: check-message</div>
<div class="cc-line cc-t-dim" data-on="2750">- exit code: 1</div>
<div class="cc-line cc-gap" data-on="2900">Commit rejected by Commit-Check.</div>
<div class="cc-line" data-on="3100"><span class="cc-t-fail cc-b">CC001</span> message check failed ==&gt; Fix: add streaming support</div>
<div class="cc-line cc-t-dim" data-on="3250">The commit message should follow Conventional Commits. See https://www.conventionalcommits.org</div>
<div class="cc-line" data-on="3400"><span class="cc-t-blue">Suggest:</span> Use "<span class="cc-t-pass cc-b">fix: add streaming support</span>"</div>
<div class="cc-line cc-t-dim" data-on="3500">Docs: https://commit-check.com/rules/#cc001</div>
<div class="cc-line cc-gap" data-on="5200"><span class="cc-sigil">❯ </span><span data-type="5600" data-speed="42">git commit -m "fix: add streaming support"</span><i class="cc-caret" data-from="5200" data-until="7700"></i></div>
<div class="cc-line cc-row" data-on="7700"><span>check commit message</span><span class="cc-leader" aria-hidden="true"></span><span class="cc-t-pass">Passed</span></div>
<div class="cc-line cc-t-dim" data-on="7900">[feature/streaming 77663ff] fix: add streaming support</div>
</div>
</figure>
</div>
<ul class="cc-wrap cc-facts">
<li>MIT licensed, no account needed</li>
<li>Python 3.10 – 3.14 on Linux, macOS and Windows</li>
<li>Signed build provenance on every release</li>
<li>CLI and hook work with any Git host</li>
</ul>
</section>

<section class="cc-band cc-paths" id="where-it-runs" aria-labelledby="cc-paths-title">
<div class="cc-wrap">
<header class="cc-head cc-head--center">
<p class="cc-eyebrow">Where it runs</p>
<h2 id="cc-paths-title" class="cc-h2">One config file. Five places to enforce it.</h2>
<p class="cc-sub">Pick the entry point that matches how your team works. Every one reads the same <code>cchk.toml</code> and reports the same rule IDs — start with one, add the rest later.</p>
</header>
<div class="cc-config">
<p class="cc-config__bar"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 1.5h5.5L13 5v9.5H4z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/><path d="M9.5 1.5V5H13" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>cchk.toml</p>
<div class="cc-config__body"><span class="cc-t-blue">[commit]</span>
conventional_commits = <span class="cc-t-pass">true</span>
subject_max_length   = <span class="cc-t-num">80</span>
<span class="cc-t-blue">[branch]</span>
conventional_branch  = <span class="cc-t-pass">true</span></div>
</div>
<svg class="cc-fan" viewBox="0 0 1000 64" preserveAspectRatio="none" aria-hidden="true" focusable="false"><g fill="none" stroke-width="1.6" vector-effect="non-scaling-stroke"><path d="M500 0C500 36 100 28 100 64"/><path d="M500 0C500 36 300 28 300 64"/><path class="cc-fan__main" d="M500 0V64"/><path d="M500 0C500 36 700 28 700 64"/><path d="M500 0C500 36 900 28 900 64"/></g></svg>
<ul class="cc-surfaces">
<li><a class="cc-surface" href="getting-started/">
<span class="cc-surface__icon"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 7l4.5 4.5L5 16M12 17h7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
<span class="cc-surface__kicker">Any forge, any CI</span>
<span class="cc-surface__name">Command line</span>
<span class="cc-surface__desc">The engine itself, with JSON output and a Python API for scripts.</span>
<code class="cc-surface__code">pip install commit-check</code>
<span class="cc-surface__go">Getting started →</span>
</a></li>
<li><a class="cc-surface" href="guides/pre-commit/">
<span class="cc-surface__icon"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><path d="M2.5 12H8M16 12h5.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></span>
<span class="cc-surface__kicker">Fastest feedback</span>
<span class="cc-surface__name">pre-commit hook</span>
<span class="cc-surface__desc">Rejects a bad message on the laptop, before Git records it.</span>
<code class="cc-surface__code">- id: check-message</code>
<span class="cc-surface__go">Hook guide →</span>
</a></li>
<li><a class="cc-surface cc-surface--main" href="guides/github-actions/">
<span class="cc-surface__icon"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M10 8.5v7l5.5-3.5z" fill="currentColor"/></svg></span>
<span class="cc-surface__flag">Most teams start here</span>
<span class="cc-surface__kicker">Enforced in CI</span>
<span class="cc-surface__name">GitHub Action</span>
<span class="cc-surface__desc">A required check no one can skip, with a PR comment and a job summary.</span>
<code class="cc-surface__code">commit-check-action@v2</code>
<span class="cc-surface__go">Action guide →</span>
</a></li>
<li><a class="cc-surface" href="guides/github-app/">
<span class="cc-surface__icon"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l8 4.5v9L12 21l-8-4.5v-9zM12 12l8-4.5M12 12v9M12 12L4 7.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg></span>
<span class="cc-surface__kicker">Zero YAML</span>
<span class="cc-surface__name">GitHub App</span>
<span class="cc-surface__desc">Install once. Every push and pull request gets a check run, no CI minutes.</span>
<code class="cc-surface__code">apps/commit-check</code>
<span class="cc-surface__go">App guide →</span>
</a></li>
<li><a class="cc-surface" href="guides/mcp/">
<span class="cc-surface__icon"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4.5" y="8" width="15" height="11" rx="3" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 4v4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><circle cx="9.5" cy="13.5" r="1.3" fill="currentColor"/><circle cx="14.5" cy="13.5" r="1.3" fill="currentColor"/></svg></span>
<span class="cc-surface__kicker">For AI agents</span>
<span class="cc-surface__name">MCP server</span>
<span class="cc-surface__desc">Your coding agent checks its own commit before it writes it.</span>
<code class="cc-surface__code">uvx commit-check-mcp</code>
<span class="cc-surface__go">MCP guide →</span>
</a></li>
</ul>
<p class="cc-more-link"><a href="guides/integrations/">Not sure which? Compare them side by side →</a></p>
</div>
</section>

<section class="cc-band cc-band--ink cc-action" id="github-action" aria-labelledby="cc-action-title">
<div class="cc-wrap">
<header class="cc-head cc-head--center">
<p class="cc-eyebrow">commit-check-action</p>
<h2 id="cc-action-title" class="cc-h2">Every pull request, checked and explained.</h2>
<p class="cc-sub">The Action reports where your reviewers already look — a PR comment, the job summary, inline annotations — and exposes a JSON result the next step can gate on.</p>
</header>
<!--
  The reports below follow the formats commit-check-action writes (see the
  comment block above _report_footer in its main.py). The footer shows only
  "Rules reference": the real one also names the installed version, which
  would go stale here.
-->
<div class="cc-demo" data-cycle="8200">
<div class="cc-tabs" role="tablist" aria-label="What the Action reports">
<button class="cc-tab" type="button" role="tab" id="cc-tab-comments" aria-controls="cc-panel-comments" aria-selected="true">pr-comments<i class="cc-tab__bar"></i></button>
<button class="cc-tab" type="button" role="tab" id="cc-tab-summary" aria-controls="cc-panel-summary" aria-selected="false" tabindex="-1">job-summary<i class="cc-tab__bar"></i></button>
<button class="cc-tab" type="button" role="tab" id="cc-tab-title" aria-controls="cc-panel-title" aria-selected="false" tabindex="-1">pr-title<i class="cc-tab__bar"></i></button>
<button class="cc-tab" type="button" role="tab" id="cc-tab-message" aria-controls="cc-panel-message" aria-selected="false" tabindex="-1">message<i class="cc-tab__bar"></i></button>
<button class="cc-tab" type="button" role="tab" id="cc-tab-branch" aria-controls="cc-panel-branch" aria-selected="false" tabindex="-1">branch<i class="cc-tab__bar"></i></button>
</div>

<div class="cc-panel cc-tl" role="tabpanel" id="cc-panel-comments" aria-labelledby="cc-tab-comments" tabindex="0">
<p class="cc-caption"><strong>One report on the pull request, edited in place on every push.</strong><span>Turn it on with <code>pr-comments: true</code></span></p>
<div class="cc-window">
<div class="cc-window__bar" aria-hidden="true"><span class="cc-dots"><i></i><i></i><i></i></span><span class="cc-url">github.com/acme/widgets/pull/128</span></div>
<div class="cc-pr">
<p class="cc-pr__title">feat: add login page <span class="cc-pr__num">#128</span><span class="cc-open">Open</span></p>
<p class="cc-pr__meta"><b>alex</b> wants to merge 3 commits into <code class="cc-ref">main</code> from <code class="cc-ref">feature/add-login</code></p>
<p class="cc-pr__tabs" aria-hidden="true"><span class="is-active">Conversation <i>4</i></span><span>Commits <i>3</i></span><span>Checks <i>2</i></span><span class="cc-wide">Files changed <i>6</i></span></p>
</div>
<div class="cc-window__body cc-conv">
<div class="cc-comment" data-on="200">
<span class="cc-avatar" aria-hidden="true"><svg viewBox="0 0 64 64"><path d="M21 10V54" stroke="#2C9CCD" stroke-opacity=".4" stroke-width="5" stroke-linecap="round"/><path d="M21 34L30 43L47 22" fill="none" stroke="#2C9CCD" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><circle cx="21" cy="34" r="6.5" fill="#0B1620" stroke="#2C9CCD" stroke-width="4.5"/></svg></span>
<div class="cc-comment__box">
<p class="cc-comment__head"><b>github-actions</b><span class="cc-chip">bot</span> commented<span class="cc-chip cc-chip--end" data-on="3600">edited</span></p>
<div class="cc-comment__body">
<p class="cc-report__title">Commit Check</p>
<div data-until="3600">
<p class="cc-verdict"><i class="cc-st cc-st--fail" aria-hidden="true"></i>2 of 5 checks failed</p>
<table class="cc-table">
<thead><tr><th>Scope</th><th>Checked value</th><th>Failed checks</th></tr></thead>
<tbody>
<tr data-on="800"><td class="cc-lnk">Commit 2/3 (5584f46)</td><td><code>bad msg</code></td><td class="cc-lnk">CC001 message</td></tr>
<tr data-on="1150"><td class="cc-lnk">Commit 3/3 (37d6def)</td><td><code>Fix: handle empty password</code></td><td class="cc-lnk">CC001 message</td></tr>
</tbody>
</table>
<p class="cc-fold">▸ Show all 5 checks</p>
</div>
<div class="cc-flash" data-from="3600">
<p class="cc-verdict"><i class="cc-st cc-st--pass" aria-hidden="true"></i>All 5 checks passed</p>
<p class="cc-fold">▸ Show all 5 checks</p>
</div>
<p class="cc-report__foot">Rules reference</p>
</div>
</div>
</div>
<p class="cc-event" data-on="2500"><svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="3" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M8 1v4M8 11v4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg><span><b>alex</b> force-pushed <code>feature/add-login</code>, rewording 2 commits</span></p>
<p class="cc-note" data-on="4300">The same comment was updated. No new comment, no noise in the thread.</p>
</div>
</div>
</div>

<div class="cc-panel cc-tl" role="tabpanel" id="cc-panel-summary" aria-labelledby="cc-tab-summary" tabindex="0">
<p class="cc-caption"><strong>The full breakdown lands in the workflow run: each check, the value, the fix.</strong><span>Turn it on with <code>job-summary: true</code></span></p>
<div class="cc-window">
<div class="cc-window__bar" aria-hidden="true"><span class="cc-dots"><i></i><i></i><i></i></span><span class="cc-url">github.com/acme/widgets/actions/runs/1180</span></div>
<div class="cc-window__body cc-run">
<div class="cc-run__side" aria-hidden="true"><span class="is-active">Summary</span><span class="cc-run__label">Jobs</span><span><i class="cc-st cc-st--fail"></i>commit-check</span><span class="cc-run__label">Run details</span><span class="cc-dim">Usage</span><span class="cc-dim">Workflow file</span></div>
<div class="cc-run__main">
<div class="cc-run__meta"><p>Triggered via pull_request<b>alex pushed 5584f46</b></p><p>Status<b>Failure</b></p><p>Total duration<b>14s</b></p></div>
<div class="cc-card">
<p class="cc-card__head">commit-check summary</p>
<div class="cc-card__body">
<p class="cc-report__title">Commit Check</p>
<p class="cc-verdict"><i class="cc-st cc-st--fail" aria-hidden="true"></i>2 of 5 checks failed</p>
<p class="cc-fold">▾ Show all 5 checks</p>
<div class="cc-tree">
<div class="cc-b" data-on="500">Commit message</div>
<div data-on="670">  <span class="cc-t-okd">✔</span> PR title (feat: add login page)</div>
<div data-on="840">  <span class="cc-t-okd">✔</span> Commit 1/3 (d87faca) (feat: add login page)</div>
<div data-on="1010">  <span class="cc-t-bad">✖</span> Commit 2/3 (5584f46) (1 failure)</div>
<div class="cc-b" data-on="1180">      CC001 message</div>
<div class="cc-dim" data-on="1350">        value: bad msg</div>
<div class="cc-dim cc-hang" data-on="1520">        Suggest: Use &lt;type&gt;(&lt;scope&gt;): &lt;description&gt;, where &lt;type&gt; is one of: feat, fix, docs, style, refactor, test, chore, perf, build, ci</div>
<div data-on="1690">  <span class="cc-t-bad">✖</span> Commit 3/3 (37d6def) (1 failure)</div>
<div class="cc-b" data-on="1860">      CC001 message</div>
<div class="cc-dim" data-on="2030">        value: Fix: handle empty password</div>
<div class="cc-t-okd cc-b" data-on="2200">        Fix: fix: handle empty password</div>
<div class="cc-b" data-on="2370">Branch</div>
<div data-on="2540">  <span class="cc-t-okd">✔</span> Branch (feature/add-login)</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>

<div class="cc-panel cc-tl" role="tabpanel" id="cc-panel-title" aria-labelledby="cc-tab-title" tabindex="0">
<p class="cc-caption"><strong>Squash merges turn the PR title into the commit, so the title is checked too.</strong><span>Turn it on with <code>pr-title: true</code></span></p>
<div class="cc-window">
<div class="cc-window__bar" aria-hidden="true"><span class="cc-dots"><i></i><i></i><i></i></span><span class="cc-url">github.com/acme/widgets/pull/128</span></div>
<div class="cc-pr">
<p class="cc-pr__title" data-until="1500">add login page <span class="cc-pr__num">#128</span><span class="cc-open">Open</span></p>
<p class="cc-pr__title" data-from="1500" data-until="3300"><span class="cc-editbox"><span data-type="1900" data-speed="150">feat: </span>add login page<i class="cc-caret cc-caret--ink"></i></span><span class="cc-save">Save</span></p>
<p class="cc-pr__title" data-from="3300">feat: add login page <span class="cc-pr__num">#128</span><span class="cc-open">Open</span></p>
<p class="cc-pr__meta"><b>alex</b> wants to merge 3 commits into <code class="cc-ref">main</code> from <code class="cc-ref">feature/add-login</code></p>
<p class="cc-pr__tabs" aria-hidden="true"><span class="is-active">Conversation <i>4</i></span><span>Commits <i>3</i></span><span>Checks <i>2</i></span><span class="cc-wide">Files changed <i>6</i></span></p>
</div>
<div class="cc-window__body cc-stack">
<div class="cc-card">
<p class="cc-card__head">Checks</p>
<div class="cc-check">
<i class="cc-st cc-st--fail" data-until="3300" aria-hidden="true"></i><i class="cc-st cc-st--wait" data-from="3300" data-until="4200" aria-hidden="true"></i><i class="cc-st cc-st--pass" data-from="4200" aria-hidden="true"></i>
<p><b>Commit Check / commit-check (pull_request)</b><span class="cc-mono cc-t-bad" data-until="3300">CC001 message · PR title (add login page)</span><span class="cc-mono cc-t-wait" data-from="3300" data-until="4200">Re-running on the edited title…</span><span class="cc-mono cc-t-okd" data-from="4200">✔ PR title (feat: add login page)</span></p>
</div>
</div>
<div class="cc-card cc-card--pad">
<p class="cc-squash__label">Squash and merge creates this commit on <code>main</code>:</p>
<p class="cc-squash"><span data-type="1900" data-speed="150">feat: </span>add login page (#128)</p>
<div class="cc-merge"><span class="cc-mergebtn" data-until="4200">Squash and merge</span><span class="cc-mergebtn cc-mergebtn--ready" data-from="4200">Squash and merge</span><span class="cc-dim" data-until="4200">A required check has not passed</span><span class="cc-dim" data-from="4200">All checks have passed</span></div>
</div>
</div>
</div>
</div>

<div class="cc-panel cc-tl" role="tabpanel" id="cc-panel-message" aria-labelledby="cc-tab-message" tabindex="0">
<p class="cc-caption"><strong>Every commit in the pull request, checked against Conventional Commits.</strong><span>On by default: <code>message: true</code></span></p>
<div class="cc-window">
<div class="cc-window__bar" aria-hidden="true"><span class="cc-dots"><i></i><i></i><i></i></span><span class="cc-url">github.com/acme/widgets/pull/128/checks</span></div>
<div class="cc-pr">
<p class="cc-pr__title">feat: add login page <span class="cc-pr__num">#128</span><span class="cc-open">Open</span></p>
<p class="cc-pr__meta"><b>alex</b> wants to merge 3 commits into <code class="cc-ref">main</code> from <code class="cc-ref">feature/add-login</code></p>
<p class="cc-pr__tabs" aria-hidden="true"><span>Conversation <i>4</i></span><span>Commits <i>3</i></span><span class="is-active">Checks <i>2</i></span><span class="cc-wide">Files changed <i>6</i></span></p>
</div>
<div class="cc-window__body cc-stack">
<div class="cc-card">
<p class="cc-card__head">Commit message</p>
<div class="cc-commit"><i class="cc-st cc-st--wait" data-until="500" aria-hidden="true"></i><i class="cc-st cc-st--pass" data-from="500" aria-hidden="true"></i><span>feat: add login page</span><code>d87faca</code></div>
<div class="cc-commit"><i class="cc-st cc-st--wait" data-until="900" aria-hidden="true"></i><i class="cc-st cc-st--fail" data-from="900" aria-hidden="true"></i><span>bad msg</span><code>5584f46</code></div>
<div class="cc-commit"><i class="cc-st cc-st--wait" data-until="1300" aria-hidden="true"></i><i class="cc-st cc-st--fail" data-from="1300" aria-hidden="true"></i><span>Fix: handle empty password</span><code>37d6def</code></div>
</div>
<div class="cc-card">
<p class="cc-card__head">Annotations <span class="cc-dim">2 errors</span></p>
<div class="cc-annot" data-on="2000"><p class="cc-annot__title"><i class="cc-st cc-st--fail" aria-hidden="true"></i>CC001 message</p><p class="cc-mono">Commit 2/3 (5584f46): The commit message should follow Conventional Commits.<br>value: bad msg<br>Suggest: Use &lt;type&gt;(&lt;scope&gt;): &lt;description&gt;, where &lt;type&gt; is one of: feat, fix, docs, …</p></div>
<div class="cc-annot" data-on="2700"><p class="cc-annot__title"><i class="cc-st cc-st--fail" aria-hidden="true"></i>CC001 message</p><p class="cc-mono">Commit 3/3 (37d6def): The commit message should follow Conventional Commits.<br>value: Fix: handle empty password<br><b class="cc-t-okd">Fix: fix: handle empty password</b></p></div>
</div>
</div>
</div>
</div>

<div class="cc-panel cc-tl" role="tabpanel" id="cc-panel-branch" aria-labelledby="cc-tab-branch" tabindex="0">
<p class="cc-caption"><strong>Branch names checked against Conventional Branch, with the rename to run.</strong><span>On by default: <code>branch: true</code></span></p>
<div class="cc-window">
<div class="cc-window__bar" aria-hidden="true"><span class="cc-dots"><i></i><i></i><i></i></span><span class="cc-url">github.com/acme/widgets/pull/131/checks</span></div>
<div class="cc-pr">
<p class="cc-pr__title">feat: add login page <span class="cc-pr__num">#131</span><span class="cc-open">Open</span></p>
<p class="cc-pr__meta"><b>alex</b> wants to merge 1 commit into <code class="cc-ref">main</code> from <code class="cc-ref cc-ref--bad">Feature/Add-Login</code></p>
<p class="cc-pr__tabs" aria-hidden="true"><span>Conversation <i>1</i></span><span>Commits <i>1</i></span><span class="is-active">Checks <i>1</i></span><span class="cc-wide">Files changed <i>6</i></span></p>
</div>
<div class="cc-window__body cc-split">
<div class="cc-stack">
<div class="cc-card cc-card--pad">
<p class="cc-branchrow"><i class="cc-st cc-st--wait" data-until="800" aria-hidden="true"></i><i class="cc-st cc-st--fail" data-from="800" aria-hidden="true"></i><b>Branch</b><code class="cc-ref cc-ref--bad">Feature/Add-Login</code></p>
<div class="cc-finding" data-on="900"><p><span class="cc-rule">CC201</span> The branch should follow Conventional Branch.</p><p class="cc-mono">value: Feature/Add-Login<br><b class="cc-t-okd">Fix: feature/Add-Login</b></p></div>
</div>
<div class="cc-term cc-term--inline" data-on="1600">
<div class="cc-line"><span class="cc-sigil">❯ </span><span data-type="1900" data-speed="45">git branch -m feature/Add-Login</span></div>
<div class="cc-line" data-on="3600"><span class="cc-sigil">❯ </span><span data-type="3800" data-speed="45">commit-check --branch &amp;&amp; echo passed</span></div>
<div class="cc-line cc-t-pass cc-b" data-on="5700">passed</div>
</div>
</div>
<div class="cc-card cc-card--pad cc-types">
<p class="cc-types__head">Conventional Branch types</p>
<ul><li data-hl="5700">feature/</li><li>bugfix/</li><li>hotfix/</li><li>release/</li><li>chore/</li></ul>
<p class="cc-dim"><code>main</code> and <code>master</code> always pass. Add your own types in <code>cchk.toml</code>.</p>
</div>
</div>
</div>
</div>
</div>

<div class="cc-action__more">
<div class="cc-yaml">
<p class="cc-yaml__bar">.github/workflows/commit-check.yml<button class="cc-copy cc-copy--text" type="button" data-copy-from="cc-yaml-src">Copy</button></p>
<div class="cc-yaml__body" id="cc-yaml-src"><span class="cc-t-blue">on</span>:
  pull_request:
    types: [opened, synchronize, reopened, edited]
<span class="cc-t-blue">permissions</span>:
  contents: read
  pull-requests: write
<span class="cc-t-blue">jobs</span>:
  commit-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
        with:
          fetch-depth: 0
      - uses: <b>commit-check/commit-check-action@v2</b>
        with:
          pr-title: <span class="cc-t-pass">true</span>
          pr-comments: <span class="cc-t-pass">true</span></div>
</div>
<div class="cc-points">
<div class="cc-point"><p class="cc-point__title">Make it a required check</p><p>Branch protection does the rest: a violating commit cannot merge, however it was made.</p></div>
<div class="cc-point"><p class="cc-point__title">Verified before it installs</p><p>The Action checks the wheel's signed build provenance and fails the step if it does not match.</p></div>
<div class="cc-point"><p class="cc-point__title">Try it without blocking anyone</p><p><code>dry-run: true</code> reports every finding as a warning and always exits 0.</p></div>
<p class="cc-point__links"><a href="guides/github-actions/">Read the Action guide →</a><a href="https://github.com/marketplace/actions/commit-check-action">View on Marketplace →</a></p>
</div>
</div>
</div>
</section>

<section class="cc-band cc-rules" id="what-it-checks" aria-labelledby="cc-rules-title">
<div class="cc-wrap">
<header class="cc-head cc-head--split">
<div>
<p class="cc-eyebrow">What it checks</p>
<h2 id="cc-rules-title" class="cc-h2">Rules grouped by what they protect.</h2>
<p class="cc-sub">A few are on by default. Turn on what your project needs, rule by rule, or set any rule to warn instead of fail.</p>
</div>
<a class="cc-btn cc-btn--quiet" href="rules/#rule-index">Browse all rules →</a>
</header>
<ul class="cc-groups">
<li class="cc-group">
<p class="cc-group__head"><span>Commit messages</span><code>CC001–CC012</code></p>
<p class="cc-group__desc">Conventional Commits, subject length, imperative mood, sign-off, and merge, revert, fixup or WIP commits.</p>
<p class="cc-ex cc-ex--bad"><span aria-hidden="true">✖</span><span class="cc-sr">Rejected: </span>Fix: add streaming support</p>
<p class="cc-ex cc-ex--ok"><span aria-hidden="true">✔</span><span class="cc-sr">Accepted: </span>fix: add streaming support</p>
</li>
<li class="cc-group">
<p class="cc-group__head"><span>Branch names</span><code>CC201–CC202</code></p>
<p class="cc-group__desc">Conventional Branch naming, and whether the branch is rebased onto its target.</p>
<p class="cc-ex cc-ex--bad"><span aria-hidden="true">✖</span><span class="cc-sr">Rejected: </span>my-new-thing</p>
<p class="cc-ex cc-ex--ok"><span aria-hidden="true">✔</span><span class="cc-sr">Accepted: </span>feature/streaming-support</p>
</li>
<li class="cc-group">
<p class="cc-group__head"><span>AI attribution</span><code>CC013–CC016</code></p>
<p class="cc-group__desc">Spots the trailers Claude Code, Cursor and others add. Forbid them, or require a disclosure instead.</p>
<p class="cc-ex cc-ex--bad"><span aria-hidden="true">✖</span><span class="cc-sr">Rejected: </span>Co-authored-by: Claude</p>
<p class="cc-ex cc-ex--ok"><span aria-hidden="true">✔</span><span class="cc-sr">Accepted: </span>Assisted-by: Claude</p>
</li>
<li class="cc-group">
<p class="cc-group__head"><span>Author identity</span><code>CC101–CC102</code></p>
<p class="cc-group__desc">Names and emails that match the patterns you set — here <code>author_email_pattern = "@acme\.dev$"</code> — so a build box cannot write itself into the history.</p>
<p class="cc-ex cc-ex--bad"><span aria-hidden="true">✖</span><span class="cc-sr">Rejected: </span>ec2-user &lt;root@ip-10-0-0-12&gt;</p>
<p class="cc-ex cc-ex--ok"><span aria-hidden="true">✔</span><span class="cc-sr">Accepted: </span>Jane Doe &lt;jane@acme.dev&gt;</p>
</li>
<li class="cc-group">
<p class="cc-group__head"><span>Pushes and files</span><code>CC301–CC304</code></p>
<p class="cc-group__desc">No force-pushes, no oversized files, no forbidden paths — caught at pre-push, before they leave the laptop.</p>
<p class="cc-ex cc-ex--bad"><span aria-hidden="true">✖</span><span class="cc-sr">Rejected: </span>git push --force origin main</p>
<p class="cc-ex cc-ex--bad"><span aria-hidden="true">✖</span><span class="cc-sr">Rejected: </span>assets/model.bin, 240 MB</p>
</li>
<li class="cc-group cc-group--ink">
<p class="cc-group__head"><span>Across an organization</span></p>
<p class="cc-group__desc">One shared policy for every repository. Each repo inherits it and overrides only what differs.</p>
<p class="cc-group__code"><span class="cc-t-blue">inherit_from</span> = "github:acme/.github:cchk.toml"</p>
<a class="cc-group__link" href="guides/organization/">Organization guide →</a>
</li>
</ul>
</div>
</section>

<section class="cc-band cc-band--white cc-anatomy" aria-labelledby="cc-anatomy-title">
<div class="cc-wrap cc-anatomy__grid">
<div>
<p class="cc-eyebrow">Every finding</p>
<h2 id="cc-anatomy-title" class="cc-h2">Not just “failed”. What failed, and the fix.</h2>
<ol class="cc-steps">
<li><span><b>A stable rule ID</b> that links to its documentation.</span></li>
<li><span><b>The exact value</b> that was checked.</span></li>
<li><span><b>Why it failed</b>, in one sentence.</span></li>
<li><span><b>A fix you can paste</b>, whenever the correction is unambiguous.</span></li>
</ol>
</div>
<!-- Real output of commit-check 2.18.0; the ASCII-art banner it prints first is left out. -->
<div class="cc-diag">
<p class="cc-t-dim">$ echo "Fix: add streaming support" | commit-check -m</p>
<p><span class="cc-mark">1</span><span><span class="cc-t-fail cc-b">CC001</span> message check failed ==&gt;</span></p>
<p><span class="cc-mark">2</span><span class="cc-t-white">Fix: add streaming support</span></p>
<p><span class="cc-mark">3</span><span class="cc-t-dim">The commit message should follow Conventional Commits.</span></p>
<p><span class="cc-mark">4</span><span><span class="cc-t-blue">Suggest:</span> Use "<span class="cc-t-pass cc-b">fix: add streaming support</span>"</span></p>
<p class="cc-diag__docs cc-t-dim">Docs: https://commit-check.com/rules/#cc001</p>
</div>
</div>
</section>

<section class="cc-band cc-proof" aria-label="Who uses Commit Check">
<div class="cc-wrap">
<ul class="cc-stats">
<li><b>1.6M+</b><span>downloads on PyPI</span></li>
<li><b>160+</b><span>repositories run the Action</span></li>
<li><b>Apache</b><span>allowlists the Action for its projects' CI</span></li>
</ul>
<p class="cc-users"><span>In the CI of</span><a href="https://github.com/apache">Apache</a><a href="https://github.com/TexasInstruments">Texas Instruments</a><a href="https://github.com/mila-iqia">Mila</a><a href="https://github.com/istio-ecosystem">Istio Ecosystem</a><a href="https://github.com/OpenDriveLab">OpenDriveLab</a><a href="https://github.com/commit-check/commit-check-action/network/dependents">and more →</a></p>
</div>
</section>

<section class="cc-band cc-band--white cc-pricing" id="pricing" aria-labelledby="cc-pricing-title">
<div class="cc-wrap">
<header class="cc-head">
<p class="cc-eyebrow">Pricing</p>
<h2 id="cc-pricing-title" class="cc-h2">Free for open source. Team plan, soon.</h2>
<p class="cc-sub">The CLI, the hook, the Action and the MCP server are MIT licensed — nothing to buy. Plans only cover the hosted GitHub App, the one surface we run for you.</p>
</header>
<ul class="cc-plans">
<li class="cc-plan"><p class="cc-plan__name">Open Source</p><p class="cc-plan__price">Free</p><p class="cc-plan__desc">Public repositories, on any account.</p><a href="https://github.com/apps/commit-check">Install the App →</a></li>
<li class="cc-plan"><p class="cc-plan__name">Personal</p><p class="cc-plan__price">Free</p><p class="cc-plan__desc">Private repositories on a personal account.</p><a href="https://github.com/apps/commit-check">Install the App →</a></li>
<li class="cc-plan cc-plan--soon"><p class="cc-plan__name">Team</p><p class="cc-plan__price">Coming soon</p><p class="cc-plan__desc">Private repositories in an organization. Until then, the Action covers private repositories for free.</p><a href="https://github.com/commit-check/commit-check-app">Watch for the launch →</a></li>
</ul>
<p class="cc-plans__note">Nothing is blocked while you try it: without a config file the App reports its findings but leaves the check run neutral. GitHub's own commit-metadata rules sit behind its Enterprise plan — <a href="compare/github-rules/">the arithmetic, and the caveats →</a></p>
</div>
</section>

<div class="cc-band cc-faq" markdown>
<div class="cc-wrap" markdown>

<h2 class="cc-h2" id="questions">Questions</h2>

??? question "Does it read my source code?"

    No. The CLI validates commit metadata and never opens your files. The
    hosted App uses a blob-filtered fetch and a sparse checkout that
    materializes only the config files, so no other repository content is ever
    downloaded. Content scanning is deliberately out of scope.

??? question "Can a developer bypass it?"

    The pre-commit hook, yes: `git commit --no-verify` is one flag, and a local
    hook is there for fast feedback. The enforcement boundary is CI. Make the Action or the App a required status check and a
    violating change cannot merge, however it was committed.

??? question "Will turning it on block everyone tomorrow?"

    No. Without a config file the App reports in full but leaves the check
    neutral, and it never rejects a push. Most rules are off until you turn
    them on — the [rules reference](rules.md#rule-index) marks which start on.

??? question "What about the history I already have?"

    Only new commits are checked. Nothing asks you to rewrite what is already
    merged.

??? question "Does it only work on GitHub?"

    The CLI and the pre-commit hook run anywhere Git does — GitLab, Gitea,
    Bitbucket, a local machine. The Action and the App are GitHub-specific
    because they integrate with GitHub's check runs.

??? question "Do I need Node.js?"

    No. On a modern Python there are no runtime dependencies at all.

??? question "Which Python versions are supported?"

    3.10 through 3.14. CI runs the suite on all five, across Linux, macOS and
    Windows — fifteen combinations on every change.

??? question "How do I know the package I installed is the one you built?"

    Every release carries a signed
    [build provenance attestation](https://docs.github.com/en/actions/concepts/security/artifact-attestations)
    naming the workflow in this repository that built it. Check a wheel
    yourself with `gh attestation verify <file> --repo commit-check/commit-check`;
    the GitHub Action runs the same check before it installs anything, and
    fails the step if verification does not pass.

??? question "Who is behind this?"

    Commit Check is written and maintained by
    [Xianpeng Shen](https://github.com/shenxianpeng), who also runs the hosted
    App. The engine, the Action, the App and the MCP server are open source
    under the [commit-check](https://github.com/commit-check) organization —
    if the hosted App ever stops, the [GitHub Action](guides/github-actions.md)
    reads the same config and reports the same rule IDs.


</div>
</div>

<section class="cc-band cc-band--ink cc-cta" aria-labelledby="cc-cta-title">
<div class="cc-wrap cc-cta__grid">
<div>
<h2 id="cc-cta-title" class="cc-h2 cc-h2--xl">Start with two commands.</h2>
<p class="cc-sub">No config file needed. The defaults check Conventional Commits, Conventional Branch and subject length; tighten them when you are ready.</p>
<div class="cc-actions">
<a class="cc-btn cc-btn--primary" href="getting-started/">Read the quickstart</a>
<a class="cc-btn cc-btn--ghost" href="https://github.com/commit-check/commit-check">Star on GitHub</a>
</div>
</div>
<div class="cc-cta__code"><p><span class="cc-sigil">$ </span>pip install commit-check</p><p><span class="cc-sigil">$ </span>commit-check --message --branch</p></div>
</div>
</section>

<nav class="cc-band cc-sitemap" aria-label="Site map">
<div class="cc-wrap cc-sitemap__grid">
<div><p>Product</p><a href="getting-started/">Command line</a><a href="guides/pre-commit/">pre-commit hook</a><a href="guides/github-actions/">GitHub Action</a><a href="guides/github-app/">GitHub App</a><a href="guides/mcp/">MCP server</a></div>
<div><p>Docs</p><a href="getting-started/">Getting started</a><a href="rules/">Rules</a><a href="configuration/">Configuration</a><a href="troubleshoot/">Troubleshooting</a><a href="changelog/">Changelog</a></div>
<div><p>Compare</p><a href="compare/github-rules/">GitHub's built-in rules</a><a href="compare/tools/">Other tools</a><a href="https://conventionalbranch.org">Conventional Branch</a></div>
<div><p>Community</p><a href="https://github.com/commit-check/commit-check/discussions">Discussions</a><a href="https://github.com/commit-check/commit-check/issues">Issues</a><a href="blog/">Blog</a><a href="https://github.com/commit-check">Contribute</a></div>
</div>
</nav>
