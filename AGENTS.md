# AGENTS.md — AI Agent Guidelines

This file provides working guidelines for AI coding agents contributing to this repository.

This repository is the documentation site for [commit-check](https://github.com/commit-check/commit-check). Everything here describes behaviour that lives in **another** repository,
so the pages go stale on their own: a release happens elsewhere and nothing in this repository changes. The rules below exist to catch that.

## Keep the site in step with the released version

**Do this on every change, whatever you came here to do.** It is not a release-time task — the point is that no change leaves the site describing a version that no longer exists.

1. **Find the latest released version.**

   ```console
   $ curl -s https://pypi.org/pypi/commit-check/json | python -c "import json,sys; print(json.load(sys.stdin)['info']['version'])"
   ```

   The [releases page](https://github.com/commit-check/commit-check/releases) answers the same question, provided you read only **published** releases.
   A draft is not one, and you cannot tell by looking for a tag: a draft can be saved against a tag that already exists, and publishing to PyPI is a
   separate step from publishing the GitHub release. Read the published release, or ask PyPI as above — PyPI is what the pin check compares against, since that is what a reader installs.

2. **Check the install pins.** The pre-commit snippets pin a revision with `rev:`, and a stale pin is invisible: the snippet keeps working, it just installs an older release than the page around it describes.
   These are the only version-pinned snippets — the GitHub Action is referenced by its moving major tag (`commit-check-action@v2`) and `uvx commit-check-mcp` carries no version, so neither goes stale.

   ```console
   $ grep -rn "rev: v" docs | grep -v docs/blog
   ```

   Every one of those must name the released version. **Blog posts are excluded on purpose** — they are dated records of what was current when they were written, and moving their pins forward would falsify them. Never touch them.

3. **Check the changelog.** `docs/changelog.md` must have an entry for the latest release, and that entry must carry its **release date**, not `(unreleased)`:

   ```markdown
   ## v2.15.0 (2026-08-13) { #v2150 }
   ```

   The date is the release's own publication date, not today's. A release that is out but still marked `(unreleased)` here is the most common form of this drift.

   A notable release also needs a row in the **Highlights** table at the top, newest first, linking to its entry and to the page that documents the feature properly.
   A patch release that only fixes bugs does not need a row; a release that adds or changes user-visible behaviour does.

4. **Anything out of step, fix it in the same change.** Do not open a follow-up issue and do not mention it in passing — bring it into step and say so in the pull request description.

### Verify with the test suite

The check above is automated, and the `docs-sync` job runs it on every pull request. Run it locally before you push:

```console
$ python -m pip install --upgrade pytest commit-check
$ python -m pytest tests/ -q
```

`tests/docs_sync_test.py` reads the *installed* package and asserts the pins match it, along with every documented rule, option and default. Two details matter, and both are ways to check the wrong thing without noticing:

- **`--upgrade` is not optional.** Without it, `pip` leaves an already-installed `commit-check` alone, so the run measures whatever was in the environment — quite possibly the release before the one you are checking against.
- **Run it as `python -m pytest`, not `pytest`.** A bare `pytest` can resolve to a different environment than the `python` you just installed into, and the version it then imports is not the one you think.

Install the **released** package, not a checkout of `main` — a development version reports something like `2.14.0.post1.dev6`, which matches no pin and tells you nothing.

### The one case where pins may name an unreleased version

When the site is being prepared for a release that has not been published yet, the pins and the changelog date are written **ahead** of the tag. `test_pinned_revisions_match_the_released_version` fails for as long as that is true, because PyPI does not have the version yet. That is expected, and it is the only acceptable reason for that test to be red:

- Say so plainly in the pull request description.
- Do not weaken the test, and do not pin the `docs-sync` job to a version to make it pass.
- The pull request merges **after** the release is published, and CI is re-run to confirm it goes green.

## Writing

- The site documents what the tool **does**, in the version a reader can install today. If a page describes behaviour that only exists on `main`, it is wrong until that release ships.
- Pasted terminal output is a **transcript**: run the command and copy what it printed. Do not hand-write or adjust sample output — `tests/docs_sync_test.py` compares the rule names in those samples against the package and will catch an invented one.
- Prefer fixing a page over adding one. Every new page is another thing that can go stale.

## Workflow

- All changes must be submitted to the `main` branch **via a pull request**. Never push commits directly to `main`.
- Build the site before you push if you touched navigation, links or anything structural: `pipx run nox -s docs` (runs `mkdocs build --strict`, which fails on a broken internal link).

## Git Rules

- **Follow the Conventional Branch spec** for branch names: `<type>/<description>` with lowercase kebab-case descriptions. Allowed types: `feature/`, `bugfix/`, `hotfix/`, `release/`, `chore/`. Example: `chore/refresh-install-pins`.
- **Follow the Conventional Commits spec** for commit messages: `<type>: <description>` (e.g., `feat: ...`, `fix: ...`, `chore: ...`, `docs: ...`). Most changes here are `docs:`.
- **No force push.** Never use `git push --force` or `git push --force-with-lease`.
- **Additive commits only.** When addressing review feedback, add new commits on top. Never rebase or squash history after the pull request is open.

## Staging Files

- Stage **only the files you changed**: `git add <file>...`.
- Never use `git add .` / `git add -A` / `git add --all`, and never stage unrelated or generated files. The built site lands in `site/` — it is never committed.
