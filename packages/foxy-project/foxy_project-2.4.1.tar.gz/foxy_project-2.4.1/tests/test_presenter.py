# SPDX-FileCopyrightText: 2016-2024 Michael Bryan <michaelfbryan@gmail.com> - Ken Mijime <kenaco666@gmail.com>
# SPDX-FileCopyrightText: 2024-present Fabien Hermitte
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from datetime import date

import pytest

from foxy_project.changelog import default_issue_pattern
from foxy_project.changelog.domain_model import Changelog
from foxy_project.changelog.presenter import MarkdownPresenter


@pytest.fixture(params=["", "Title"])
def title(request):
    return request.param


@pytest.fixture(params=["", "Description"])
def description(request):
    return request.param


# pylint: disable=redefined-outer-name
@pytest.fixture
def empty_changelog(title, description):
    return Changelog(title, description)


@pytest.fixture
def changelog(title, description):
    return Changelog(title, description)


@pytest.fixture
def markdown_presenter():
    return MarkdownPresenter("compact")


def test_markdown_presenter_empty_changelog(empty_changelog, markdown_presenter):
    markdown = markdown_presenter.present(empty_changelog)
    assert empty_changelog.title in markdown
    assert empty_changelog.description in markdown


def test_markdown_presenter_changelog_with_features(changelog, markdown_presenter):
    changelog.add_release("Unreleased", "HEAD", date(2020, 1, 1), None)
    changelog.add_note("", "feat", "description")
    changelog.add_note("", "feat", "description", scope="scope")
    description = f"{changelog.description}\n\n" if changelog.description else ""
    assert_markdown = (
        f"# {changelog.title}\n\n{description}## Unreleased (2020-01-01)\n\n#### New Features\n\n* "
        f"description\n* (scope): description\n"
    )
    markdown = markdown_presenter.present(changelog)
    assert assert_markdown == markdown


def test_markdown_presenter_custom_template_changelog_with_features(changelog, markdown_presenter):
    # scope in bold
    markdown_presenter = MarkdownPresenter("tests/custom_template/custom_template.jinja2")
    changelog.add_release("Unreleased", "HEAD", date(2020, 1, 1), None)
    changelog.add_note("", "feat", "description")
    changelog.add_note("", "feat", "description", scope="scope")
    description = f"{changelog.description}\n\n" if changelog.description else ""
    assert_markdown = (
        f"# {changelog.title}\n\n{description}## Unreleased (2020-01-01)\n\n#### New Features\n\n"
        f"* description\n* **scope**: description\n"
    )
    markdown = markdown_presenter.present(changelog)
    assert assert_markdown == markdown


def test_markdown_presenter_changelog_with_fixes(changelog, markdown_presenter):
    changelog.add_release("Unreleased", "HEAD", date(2020, 1, 1), None)
    changelog.add_note("", "fix", "description")
    changelog.add_note("", "fix", "description", scope="scope")
    description = f"{changelog.description}\n\n" if changelog.description else ""
    assert_markdown = (
        f"# {changelog.title}\n\n{description}## Unreleased (2020-01-01)\n\n#### Fixes\n\n* "
        f"description\n* (scope): description\n"
    )
    markdown = markdown_presenter.present(changelog)
    assert assert_markdown == markdown


def test_markdown_presenter_changelog_custom_template_with_fixes(changelog):
    # scope in bold
    markdown_presenter = MarkdownPresenter("tests/custom_template/custom_template.jinja2")
    changelog.add_release("Unreleased", "HEAD", date(2020, 1, 1), None)
    changelog.add_note("", "fix", "description")
    changelog.add_note("", "fix", "description", scope="scope")
    description = f"{changelog.description}\n\n" if changelog.description else ""
    assert_markdown = (
        f"# {changelog.title}\n\n{description}## Unreleased (2020-01-01)\n"
        f"\n#### Fixes\n\n* description\n* **scope**: description\n"
    )
    markdown = markdown_presenter.present(changelog)
    assert assert_markdown == markdown


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Some text about #42", "Some text about [#42](http://gitlab.com/issues/42)"),
        (
            "Some text with #12 and #42",
            "Some text with [#12](http://gitlab.com/issues/12) and [#42](http://gitlab.com/issues/42)",
        ),
        ("Some text will be unchanged", "Some text will be unchanged"),
        (
            "This is also valid ticket id #ACH-123",
            "This is also valid ticket id [#ACH-123](http://gitlab.com/issues/ACH-123)",
        ),
    ],
)
def test_link_default_match(text, expected, markdown_presenter):
    issue_url = "http://gitlab.com/issues/{id}"
    linked_text = markdown_presenter._link(issue_url, default_issue_pattern, text)  # pylint: disable=protected-access
    assert linked_text == expected


def test_link_default_url(markdown_presenter):
    linked_text = markdown_presenter._link(  # pylint: disable=protected-access
        "", default_issue_pattern, "Some text about #42"
    )
    assert linked_text == "Some text about #42"
