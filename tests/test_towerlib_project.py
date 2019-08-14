#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: test_towerlib.py
#
# Copyright 2018 Ilija Matoski
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
test_towerlib_configuration
----------------------------------
Tests for `towerlib` module.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from betamax.decorator import use_cassette
from unittest import TestCase
from .helpers import get_tower

__author__ = '''Ilija Matoski <imatoski@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''2018-05-25'''
__copyright__ = '''Copyright 2018, Ilija Matoski'''
__credits__ = ["Ilija Matoski"]
__license__ = '''MIT'''
__maintainer__ = '''Ilija Matoski'''
__email__ = '''<imatoski@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

TOWER_VERSION = '6.1.0.0'
TOWER_NAME = 'tower'


class TestTowerlibProject(TestCase):

    @use_cassette('get_projects', record='once')
    def test_get_projects(self, session):
        tower = get_tower(session=session)
        projects = list(tower.projects)
        self.assertEquals(len(projects), 1)
        project = next(projects)
        self.assertEquals(project.Name, "Demo Project")
        project_demo = tower.get_projects_by_name(project.Name)
        self.assertEquals()

    # @use_cassette('user_organization_create_assign_remove_delete')
    # def test_organization_user(self, session):
    #     tower = get_tower(session=session)
    #     self.assertIsNotNone(tower)
    #     username = "test_user_default_organization"
    #     organization = "Default"
    #     self.assertIsNone(tower.get_organization_user_by_username(organization, username))
    #     user = tower.create_user_in_organization(organization,
    #                                              "first_name", "last_name", "example@example.com",
    #                                              username, "password")
    #     self.assertIsNotNone(user)
    #     self.assertIsNotNone(tower.get_organization_user_by_username(organization, username))
    #     self.assertTrue(tower.delete_organization_user(organization, username))
    #     self.assertIsNone(tower.get_organization_user_by_username(organization, username))
    #     self.assertTrue(user.delete())
    #

