"""Tests for the redirect stubs ``scripts/mkdocs_hooks.py`` writes after a build.

Run them with the rest of the suite::

    pytest tests/
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

HOOKS_PATH = Path(__file__).parent.parent / "scripts" / "mkdocs_hooks.py"

# ``scripts/`` is not a package: MkDocs loads the hook by path, and so does this.
_spec = importlib.util.spec_from_file_location("mkdocs_hooks", HOOKS_PATH)
assert _spec is not None and _spec.loader is not None
hooks = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hooks)


def _build(tmp_path: Path, site_url: str | None) -> Path:
    site = tmp_path / "site"
    site.mkdir()
    hooks.on_post_build({"site_dir": str(site), "site_url": site_url})
    return site


def _target(stub: Path) -> str:
    """The URL a stub sends the browser to."""
    text = stub.read_text(encoding="utf-8")
    start = text.index('var target = "') + len('var target = "')
    return text[start : text.index('"', start)]


@pytest.fixture
def not_netlify(monkeypatch):
    monkeypatch.delenv("NETLIFY", raising=False)


def test_every_retired_and_legacy_url_gets_a_stub(tmp_path, not_netlify):
    site = _build(tmp_path, "https://commit-check.com/")

    for old, target in hooks.MOVED_URLS.items():
        assert (
            _target(site / old / "index.html") == f"https://commit-check.com/{target}"
        )
    for legacy, target in hooks.LEGACY_URLS.items():
        assert _target(site / f"{legacy}.html") == f"https://commit-check.com/{target}"


def test_a_stub_redirects_three_ways_and_keeps_the_fragment(tmp_path, not_netlify):
    site = _build(tmp_path, "https://commit-check.com/")
    text = (site / "rules.html").read_text(encoding="utf-8")

    url = "https://commit-check.com/rules/"
    assert f'<link rel="canonical" href="{url}">' in text
    assert f'<meta http-equiv="refresh" content="0; url={url}">' in text
    # The script, not the meta refresh, is what carries ``#cc003`` across.
    assert "location.replace(target + location.hash)" in text
    assert f'<a href="{url}">{url}</a>' in text


def test_a_site_url_without_a_trailing_slash_still_joins(tmp_path, not_netlify):
    # Deploy previews pass their own URL in, sometimes without the slash.
    site = _build(tmp_path, "https://deploy-preview-7--commit-check.netlify.app")

    assert _target(site / "rules.html") == (
        "https://deploy-preview-7--commit-check.netlify.app/rules/"
    )


def test_without_a_site_url_the_targets_are_root_relative(tmp_path, not_netlify):
    site = _build(tmp_path, None)

    assert _target(site / "rules.html") == "/rules/"
    assert _target(site / "projects" / "index.html") == "/"


def test_on_netlify_only_the_retired_pages_get_stubs(tmp_path, monkeypatch):
    # netlify.toml redirects the .html URLs; a stub there would shadow
    # rules/index.html and loop.
    monkeypatch.setenv("NETLIFY", "true")
    site = _build(tmp_path, "https://commit-check.com/")

    for old in hooks.MOVED_URLS:
        assert (site / old / "index.html").is_file()
    assert not any(site.glob("*.html"))


def test_a_stub_never_overwrites_a_page_the_build_wrote(tmp_path, not_netlify):
    # The stubs run after the build, so a retired URL that became a real page
    # again would be replaced by a redirect away from itself.
    site = tmp_path / "site"
    site.mkdir()
    page = site / "guides" / "pre-commit" / "index.html"
    page.parent.mkdir(parents=True)
    page.write_text("real page", encoding="utf-8")

    hooks.on_post_build(
        {"site_dir": str(site), "site_url": "https://commit-check.com/"}
    )

    assert page.read_text(encoding="utf-8") == "real page"


def test_no_stub_redirects_to_another_stub():
    # A chain would cost a second hop, and a cycle would never end.
    retired = {f"{old}/" for old in hooks.MOVED_URLS}
    for target in [*hooks.MOVED_URLS.values(), *hooks.LEGACY_URLS.values()]:
        assert target not in retired, target


def test_the_pages_the_cli_links_to_never_move():
    # Every released commit-check prints commit-check.com/rules/#ccNNN, and
    # links to configuration/; those two pages must stay where they are.
    assert "rules" not in hooks.MOVED_URLS
    assert "configuration" not in hooks.MOVED_URLS
