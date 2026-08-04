"""Anti-drift guard between this site and the commit-check package.

The reference pages describe behaviour that lives in another repository, so
nothing stops the two from diverging except a check that reads both. These
tests import the installed ``commit-check`` and assert that every rule and
option it defines is documented here, with the defaults it actually uses.

Run them against the version the site documents::

    pip install commit-check
    pytest tests/
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from commit_check.rules_catalog import ALL_RULES
from commit_check.config_merger import get_default_config

DOCS = Path(__file__).parent.parent / "docs"


def _read_doc(name: str) -> str:
    """Read a file from the ``docs`` directory."""
    return (DOCS / name).read_text(encoding="utf-8")


def _rule_section(content: str, rule_id: str) -> str:
    """Return just the part of the rules page belonging to one rule."""
    _, _, after = content.partition(f"{{ #{rule_id.lower()} }}")
    return re.split(r"\{ #cc\d{3} \}", after)[0]


class TestRulesDocumentation:
    """Every rule the package defines stays documented here."""

    def test_every_rule_is_documented(self):
        """Each rule ID must have an anchor in the rules reference page."""
        content = _read_doc("rules.md")
        for entry in ALL_RULES:
            anchor = f"{{ #{entry.rule_id.lower()} }}"
            assert anchor in content, (
                f"{entry.rule_id} ({entry.check}) is missing from docs/rules.md"
            )

    def test_every_rule_has_a_section_heading(self):
        """Each rule needs a ``name (CCxxx)`` heading, not just an anchor."""
        content = _read_doc("rules.md")
        for entry in ALL_RULES:
            heading = (
                f"### {entry.name} ({entry.rule_id}) {{ #{entry.rule_id.lower()} }}"
            )
            assert heading in content, (
                f"docs/rules.md has no section titled '{heading}'"
            )

    def test_every_rule_explains_itself(self):
        """Each rule section must answer what it does and why it matters."""
        content = _read_doc("rules.md")
        for entry in ALL_RULES:
            section = _rule_section(content, entry.rule_id)
            for required in ("**What it does**", "**Why is this bad?**", "**Options**"):
                assert required in section, (
                    f"{entry.rule_id} ({entry.check}) section is missing {required}"
                )


_OPTIONS_ROW = re.compile(
    r"^\|\s*(commit|branch|push)\s*"  # section
    r"\|\s*(\w+)\s*"  # option name
    r"\|\s*(bool|int|str|list\[str\])\s*"  # type
    r"\|\s*(.+?)\s*\|",  # documented default
    re.M,
)

# Markdown code spans use single backticks.
_QUOTED = re.compile(r'^(?:`+(.*?)`+|"(.*?)")')


def _parse_options_table(content: str) -> dict[tuple[str, str], tuple[str, str]]:
    """Map ``(section, option) -> (type, raw default cell)``."""
    return {
        (section, option): (type_, cell)
        for section, option, type_, cell in _OPTIONS_ROW.findall(content)
    }


def _documented_default(type_: str, cell: str) -> Any:
    """Turn a documented default cell into a comparable Python value.

    Cells carry a human annotation after the value itself (``"" (disabled)``),
    so the value is read from the front of the cell and the rest ignored.
    """
    cell = cell.strip()
    if type_ == "bool":
        return cell.startswith("true")
    if type_ == "int":
        match = re.match(r"-?\d+", cell)
        return int(match.group()) if match else None
    if type_ == "list[str]":
        return re.findall(r'"(.*?)"', cell)
    quoted = _QUOTED.match(cell)
    if quoted is None:
        return cell
    backticked, double_quoted = quoted.groups()
    return backticked if backticked is not None else double_quoted


class TestDocumentedDefaults:
    """The documented defaults match the ones the package actually uses."""

    def test_every_runtime_option_is_documented(self):
        """Every option the runtime defines has a row in the options table."""
        documented = _parse_options_table(_read_doc("configuration.md"))
        for section, options in get_default_config().items():
            for option in options:
                assert (section, option) in documented, (
                    f"[{section}] {option} exists in get_default_config() but "
                    f"has no row in the options table of docs/configuration.md"
                )

    def test_no_invented_options_are_documented(self):
        """The options table does not document options that do not exist."""
        runtime = get_default_config()
        for section, option in _parse_options_table(_read_doc("configuration.md")):
            assert option in runtime.get(section, {}), (
                f"docs/configuration.md documents [{section}] {option}, which "
                f"does not exist in get_default_config()"
            )

    def test_documented_defaults_match_the_runtime(self):
        """Every documented default equals the value the runtime actually uses."""
        documented = _parse_options_table(_read_doc("configuration.md"))
        runtime = get_default_config()

        for (section, option), (type_, cell) in sorted(documented.items()):
            if option not in runtime.get(section, {}):
                continue  # reported by test_no_invented_options_are_documented
            expected = runtime[section][option]
            actual = _documented_default(type_, cell)
            if isinstance(expected, list):
                # Allow-lists: order carries no meaning, membership does.
                assert set(actual or []) == set(expected), (
                    f"docs/configuration.md documents [{section}] {option} "
                    f"with {sorted(set(actual or []) - set(expected))} that are "
                    f"not defaults, and is missing "
                    f"{sorted(set(expected) - set(actual or []))}"
                )
            else:
                assert actual == expected, (
                    f"docs/configuration.md documents [{section}] {option} as "
                    f"{cell.strip()!r}, but the runtime default is {expected!r}"
                )
