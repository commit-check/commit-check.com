import nox

nox.options.reuse_existing_virtualenvs = True


@nox.session
def docs(session: nox.Session) -> None:
    """Build the site."""
    session.install("-r", "docs/requirements.txt")
    session.run("mkdocs", "build", "--strict")


@nox.session(name="docs-live")
def docs_live(session: nox.Session) -> None:
    """Serve the site with live reload."""
    session.install("-r", "docs/requirements.txt")
    session.run("mkdocs", "serve", "--livereload")
