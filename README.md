<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/commit-check/.github/main/branding/banner-dark.png">
  <img src="https://raw.githubusercontent.com/commit-check/.github/main/branding/banner-light.png" alt="Commit Check">
</picture>

**The website, docs and blog for Commit Check.**

[![Website](https://img.shields.io/badge/Website-commit--check.com-2c9ccd?labelColor=0b1620)](https://commit-check.com)
[![Deploy](https://img.shields.io/github/actions/workflow/status/commit-check/commit-check.com/deploy.yml?branch=main&labelColor=0b1620&label=deploy)](https://github.com/commit-check/commit-check.com/actions/workflows/deploy.yml)

[Docs](https://commit-check.com/getting-started/) ·
[Rules](https://commit-check.com/rules/) ·
[CLI](https://github.com/commit-check/commit-check) ·
[GitHub Action](https://github.com/commit-check/commit-check-action) ·
[GitHub App](https://github.com/apps/commit-check) ·
[MCP server](https://github.com/commit-check/commit-check-mcp)

</div>

Source for [commit-check.com](https://commit-check.com): the landing page, the
blog, and the documentation for every Commit Check project.

## Building locally

```console
$ pip install -r docs/requirements.txt
$ mkdocs serve
```

Or through nox, which manages the environment for you:

```console
$ nox -s docs-live
```

Building the share cards needs cairo on the system (`libcairo2` on Debian and
Ubuntu, `cairo` from Homebrew on macOS). To skip them while writing:

```console
$ SOCIAL_CARDS=false mkdocs serve
```

## Layout

| Path | Contents |
| --- | --- |
| `docs/index.md` | Landing page. Renders through `docs/overrides/home.html`. |
| `docs/getting-started/`, `docs/guides/` | Tutorials and how-to guides. |
| `docs/rules.md`, `docs/configuration.md` | Reference. |
| `docs/blog/` | Blog, published with Material's blog plugin. |
| `docs/overrides/`, `docs/stylesheets/`, `docs/assets/` | Theme, styles, brand assets. |
| `scripts/mkdocs_hooks.py` | Redirect stubs for the URLs the old Sphinx site served. |

## Keeping the reference in sync with the code

`docs/rules.md` and the options table in `docs/configuration.md` describe
behaviour that lives in the
[commit-check](https://github.com/commit-check/commit-check) repository. They
are checked against the installed package in CI rather than maintained by hand
alone, so a rule or option cannot change there without this site failing here.

## Deployment

Pushes to `main` build and publish to GitHub Pages. Pull requests get a Netlify
deploy preview, configured in `netlify.toml`. The custom domain is pinned by
`docs/CNAME`, which MkDocs copies to the site root on every build.

## Community

Questions and ideas go to [Discussions](https://github.com/commit-check/commit-check/discussions),
bugs and typos on the site to [Issues](https://github.com/commit-check/commit-check.com/issues).
Released under the [MIT License](https://github.com/commit-check/commit-check.com/blob/main/LICENSE).
