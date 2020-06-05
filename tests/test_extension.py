# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under the Apache license (see LICENSE)
from pathlib import Path
from textwrap import dedent

import pytest
from markdown import Markdown

import mkdocs_click

EXPECTED = (Path(__file__).parent / "app" / "expected.md").read_text()


def test_extension():
    """
    Markdown output for a relatively complex Click application is correct.
    """
    md = Markdown(extensions=[mkdocs_click.makeExtension()])

    source = dedent(
        """
        ::: mkdocs-click
            :module: tests.app.cli
            :command: cli
        """
    )

    assert md.convert(source) == md.convert(EXPECTED)


def test_depth():
    """
    The :depth: attribute increases the level of headers.
    """
    md = Markdown(extensions=[mkdocs_click.makeExtension()])

    source = dedent(
        """
        # CLI Reference

        ::: mkdocs-click
            :module: tests.app.cli
            :command: cli
            :depth: 1
        """
    )

    expected = f"# CLI Reference\n\n{EXPECTED.replace('# ', '## ')}"

    assert md.convert(source) == md.convert(expected)


@pytest.mark.parametrize("option", ["module", "command"])
def test_required_options(option):
    """
    The module and command options are required.
    """
    md = Markdown(extensions=[mkdocs_click.makeExtension()])

    source = dedent(
        """
        ::: mkdocs-click
            :module: tests.app.cli
            :command: cli
        """
    )

    source = source.replace(f":{option}:", ":somethingelse:")

    with pytest.raises(mkdocs_click.MkDocsClickException):
        md.convert(source)
