#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: role.py
#
# Copyright 2018 Costas Tyfoxylos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Main code for role

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import logging

from .core import Entity, EntityManager

__author__ = '''Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''2018-01-03'''
__copyright__ = '''Copyright 2018, Costas Tyfoxylos'''
__credits__ = ["Costas Tyfoxylos"]
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<ctyfoxylos@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

# This is the main prefix used for logging
LOGGER_BASENAME = '''role'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class Role(Entity):
    """Models the role entity of ansible tower"""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def name(self):
        """The name of the role

        Returns:
            string: The name of the role

        """
        return self._data.get('name')

    @property
    def description(self):
        """The description of the role

        Returns:
            string: The description of the role

        """
        return self._data.get('description')

    @property
    def summary_fields(self):
        """The summary fields of the role

        Returns:
            Organization: The summary fields of the role

        """
        return self._data.get('summary_fields')

    @property
    def users(self):
        """The users of the team

        Returns:
            EntityManager: EntityManager of the users

        """
        url = self._data.get('related', {}).get('users')
        return EntityManager(self._tower, entity_object='User', primary_match_field='username', url=url)

    @property
    def teams(self):
        """The teams that have the role assigned

        Returns:
            EntityManager: EntityManager of the teams

        """
        url = self._data.get('related', {}).get('teams')
        return EntityManager(self._tower, entity_object='Team', primary_match_field='name', url=url)

    @property
    def projects(self):
        """The projects of the team

        Returns:
            EntityManager: EntityManager of the projects

        """
        url = self._data.get('related', {}).get('projects')
        return EntityManager(self._tower, entity_object='Project', primary_match_field='name', url=url)


class ObjectRole(Role):
    """Models the object role entity of ansible tower"""

    def __init__(self, tower_instance, data):
        Role.__init__(self, tower_instance, data)

    @property
    def team(self):
        """The team that has the object role assigned

        Returns:
            Team: The team that has the object role assigned

        """
        url = self._data.get('related', {}).get('team')
        return self._tower._get_object_by_url('Team', url)  # pylint: disable=protected-access
