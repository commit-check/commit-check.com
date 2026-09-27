# commit-check.com

[![Website](https://img.shields.io/badge/Website-commit--check.com-2c9ccd?labelColor=0b1620&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI%2bPHBhdGggZD0iTTIxIDM0TDMwIDQzTDQ3IDIyIiBmaWxsPSJub25lIiBzdHJva2U9IiMyQzlDQ0QiIHN0cm9rZS13aWR0aD0iOCIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8%2bPGNpcmNsZSBjeD0iMjEiIGN5PSIzNCIgcj0iNyIgZmlsbD0iIzBCMTYyMCIgc3Ryb2tlPSIjMkM5Q0NEIiBzdHJva2Utd2lkdGg9IjUiLz48L3N2Zz4K)](https://commit-check.com)

Source for [commit-check.com](https://commit-check.com) — the landing page,
the blog, and the documentation for the commit-check family of projects.

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
