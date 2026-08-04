# commit-check.com

[![Website](https://img.shields.io/static/v1?label=Website&message=commit-check.com&color=2c9ccd&logo=git&logoColor=white)](https://commit-check.com)

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
