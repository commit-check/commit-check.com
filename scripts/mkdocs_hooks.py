"""MkDocs build hooks.

Emits redirect stubs for the ``.html`` URLs the original Sphinx site served, so
links already published elsewhere keep working on hosts that have no other
redirect mechanism (GitHub Pages). Netlify skips the stubs: it declares the same
URLs as ``[[redirects]]`` in ``netlify.toml``, which resolve before file lookup
and cannot collide with the pages they target.
"""

from __future__ import annotations

import os
from pathlib import Path

#: Sphinx page name -> path under this site.
LEGACY_URLS = {
    "configuration": "configuration/",
    "rules": "rules/",
    "example": "example/",
    "migration": "migration/",
    "troubleshoot": "troubleshoot/",
    "changelog": "changelog/",
    # The CLI reference is no longer a generated page; the flags it listed are
    # documented alongside the settings that control them.
    "cli_args": "configuration/",
    "cli": "configuration/",
    "README": "getting-started/",
    "what-is-new": "changelog/",
    "genindex": "",
}

#: Retired page URL -> the page that absorbed it.
#
# Unlike LEGACY_URLS these are directory URLs, so the stub is written to
# ``<old>/index.html``. Nothing is served at the old path any more, so the stub
# cannot shadow a real page the way a flat ``rules.html`` would, and it is
# written on every host rather than skipped on Netlify.
#
# Two URLs are deliberately absent: ``rules/`` and ``configuration/``. The rule
# IDs printed by every released version of the package link to
# ``commit-check.com/rules/#ccNNN`` — the URL is hardcoded in
# ``commit_check/rules_catalog.py`` — so those two pages do not move.
MOVED_URLS = {
    "getting-started/installation": "getting-started/",
    "getting-started/quickstart": "getting-started/",
    "getting-started/why": "",
    # guides/pre-commit, guides/github-actions and guides/organization were
    # folded into guides/integrations for a while and are real pages again;
    # a stub here would overwrite them.
    "guides/signoff": "guides/policies/",
    "guides/ai-attribution": "guides/policies/",
    "what-is-new": "changelog/",
    "projects": "",
    # An orphan: nothing linked to it, it was not in the nav, and it matched no
    # key in .authors.yml, so the blog never treated it as an author page.
    "blog/author/team": "blog/",
}

# Redirect stubs for the URLs the Sphinx site served.
# The script carries the fragment across, because the links most worth keeping
# alive are the per-rule ones (``rules.html#cc003``) and a plain redirect drops
# the ``#cc003``. It also refuses to redirect a page to itself: a host that
# normalises ``/rules`` and ``/rules/`` to the same resource would otherwise
# serve this stub in place of the real page and loop forever.
REDIRECT = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Redirecting…</title>
<link rel="canonical" href="{url}">
<script>
(function () {{
  var target = "{url}";
  var here = location.protocol + "//" + location.host + location.pathname;
  if (here !== target && here + "/" !== target) {{
    location.replace(target + location.hash);
  }}
}})();
</script>
<meta http-equiv="refresh" content="0; url={url}">
</head>
<body>Redirecting to <a href="{url}">{url}</a>…</body>
</html>
"""


def on_post_build(config, **kwargs) -> None:
    """Write a redirect stub for each URL this site no longer serves."""
    site = Path(config["site_dir"])
    # Deploy previews pass their own URL in, and it may arrive without the
    # trailing slash the targets below are joined onto.
    base = (config["site_url"] or "/").rstrip("/") + "/"

    # Retired pages first: these run on every host, Netlify included. The old
    # path has no page of its own any more, so the stub is the only thing that
    # can answer for it.
    for old, target in MOVED_URLS.items():
        stub = site / old / "index.html"
        stub.parent.mkdir(parents=True, exist_ok=True)
        stub.write_text(REDIRECT.format(url=base + target), encoding="utf-8")

    # On Netlify the .html stubs would be served in place of the real pages:
    # Netlify resolves ``/rules/`` to the file ``rules.html``, so the stub that
    # redirects to ``/rules/`` would shadow ``rules/index.html`` and loop. The
    # ``[[redirects]]`` table in netlify.toml covers the same URLs with real
    # 301s, so these are only written for hosts without redirects.
    if os.environ.get("NETLIFY") == "true":
        return
    for legacy, target in LEGACY_URLS.items():
        (site / f"{legacy}.html").write_text(
            REDIRECT.format(url=base + target), encoding="utf-8"
        )
