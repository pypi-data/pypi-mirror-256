# SPDX-FileCopyrightText: 2016-2024 Michael Bryan <michaelfbryan@gmail.com> - Ken Mijime <kenaco666@gmail.com>
# SPDX-FileCopyrightText: 2024-present Fabien Hermitte
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import os
import re

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape

from foxy_project.changelog.domain_model import Changelog
from foxy_project.changelog.domain_model import PresenterInterface


default_template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates")

default_template = {"compact": "compact.jinja2", "lastrelease": "lastrelease.jinja2"}


class MarkdownPresenter(PresenterInterface):  # pylint: disable=too-few-public-methods
    def __init__(self, template=None, issue_url=None):  # noqa: ARG002
        # It is an embedded template
        if template in default_template:
            template_dir = default_template_dir
            template_name = default_template[template]
        # It is a custom template
        else:
            template_dir, template_name = os.path.split(template)

        env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(
                disabled_extensions=("html", "htm", "xml"),
                default_for_string=True,
                default=False,
            ),
        )

        self.template = env.get_template(template_name)

    def present(self, changelog: Changelog) -> str:
        text = self.template.render(changelog=changelog)
        return self._link(changelog.issue_url, changelog.issue_pattern, text)

    @staticmethod
    def _link(url, pattern, text: str) -> str:
        """Replaces all occurrences of pattern in text with markdown links based on url template"""
        if not url or not pattern:
            return text

        def replace(match):
            groups = match.groups()
            if len(groups) == 2:
                matching_text = groups[0]
                ticket_id = groups[1]
            elif len(groups) == 1:
                matching_text = ticket_id = groups[0]
            else:
                raise ValueError("Invalid pattern")
            ticket_url = url.format(id=ticket_id)
            return f"[{matching_text}]({ticket_url})"

        return re.sub(pattern, replace, text)
