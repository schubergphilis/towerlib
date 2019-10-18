#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: test_user.py
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
test_user
----------------------------------
Tests for `user` module.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from towerlib.entities import EntityManager
from towerlib.towerlibexceptions import (InvalidOrganization,
                                         InvalidValue,
                                         InvalidRole)


from . import IntegrationTest

__author__ = '''Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''2018-05-25'''
__copyright__ = '''Copyright 2018, Costas Tyfoxylos'''
__credits__ = ["Costas Tyfoxylos"]
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<ctyfoxylos@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


class TestUserMutabilityAndEntities(IntegrationTest):

    def setUp(self):
        super(TestUserMutabilityAndEntities, self).setUp()
        self.user = self.tower.get_user_by_username('workflow_normal')

    def test_mutating_username(self):
        with self.recorder:
            with self.assertRaises(InvalidValue):
                self.user.username = 'a' * 151
            with self.assertRaises(InvalidValue):
                self.user.username = 'something**!'
            self.user.username = 'valid_username'
            self.assertEqual(self.user.username, 'valid_username')
            self.user.username = 'workflow_normal'
            self.assertEqual(self.user.username, 'workflow_normal')

    def test_mutating_first_name(self):
        with self.recorder:
            with self.assertRaises(InvalidValue):
                self.user.first_name = 'a' * 31
            original_first_name = self.user.first_name
            self.user.first_name = 'new_first_name'
            self.assertEqual(self.user.first_name, 'new_first_name')
            self.user.first_name = original_first_name
            self.assertEqual(self.user.first_name, original_first_name)

    def test_mutating_last_name(self):
        with self.recorder:
            with self.assertRaises(InvalidValue):
                self.user.last_name = 'a' * 31
            original_last_name = self.user.last_name
            self.user.last_name = 'new_first_name'
            self.assertEqual(self.user.last_name, 'new_first_name')
            self.user.last_name = original_last_name
            self.assertEqual(self.user.last_name, original_last_name)

    def test_mutating_email(self):
        with self.recorder:
            with self.assertRaises(InvalidValue):
                self.user.email = 'a' * 255
            original_email = self.user.email
            self.user.email = 'new@email.com'
            self.assertEqual(self.user.email, 'new@email.com')
            self.user.email = original_email
            self.assertEqual(self.user.email, original_email)

    def test_mutating_superuser_status(self):
        with self.recorder:
            is_superuser = self.user.is_superuser
            self.user.is_superuser = not is_superuser
            self.assertEqual(self.user.is_superuser, not is_superuser)
            self.user.is_superuser = is_superuser
            self.assertEqual(self.user.is_superuser, is_superuser)

    def test_mutating_auditor_status(self):
        with self.recorder:
            is_system_auditor = self.user.is_system_auditor
            self.user.is_system_auditor = not is_system_auditor
            self.assertEqual(self.user.is_system_auditor, not is_system_auditor)
            self.user.is_system_auditor = is_system_auditor
            self.assertEqual(self.user.is_system_auditor, is_system_auditor)

    def test_organizations(self):
        with self.recorder:
            self.assertIsInstance(self.user.organizations, EntityManager)

    def test_mutating_roles(self):
        with self.recorder:
            self.assertIsInstance(self.user.roles, EntityManager)
            with self.assertRaises(InvalidOrganization):
                self.user.associate_with_organization_role('DefaultBroken', 'Read')
            with self.assertRaises(InvalidRole):
                self.user.associate_with_organization_role('Default', 'ReadBroken')
            self.user.associate_with_organization_role('Default', 'Read')
            self.assertTrue('Read' in [role.name for role in self.user.roles])
            with self.assertRaises(InvalidOrganization):
                self.user.disassociate_from_organization_role('DefaultBroken', 'Read')
            with self.assertRaises(InvalidRole):
                self.user.disassociate_from_organization_role('Default', 'ReadBroken')
            self.user.disassociate_from_organization_role('Default', 'Read')
            self.assertTrue('Read' not in [role.name for role in self.user.roles])

    def test_teams(self):
        with self.recorder:
            self.assertIsInstance(self.user.teams, EntityManager)

    def test_projects(self):
        with self.recorder:
            self.assertIsInstance(self.user.projects, EntityManager)

    def test_credentials(self):
        with self.recorder:
            self.assertIsInstance(self.user.credentials, EntityManager)
