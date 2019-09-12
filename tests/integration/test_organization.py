#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: test_organization.py
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
test_organization
----------------------------------
Tests for `organization` module.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import time

from towerlib.entities import (EntityManager,
                               User,
                               Project,
                               Team,
                               Inventory,
                               GenericCredential)
from towerlib.towerlibexceptions import (InvalidValue,
                                         InvalidCredential,
                                         InvalidProject,
                                         InvalidTeam,
                                         InvalidVariables,
                                         InvalidInventory, InvalidCredentialType)
from . import IntegrationTest
from .common import Timeout, TIMEOUT_IN_SECONDS

__author__ = '''Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''2018-05-25'''
__copyright__ = '''Copyright 2018, Costas Tyfoxylos'''
__credits__ = ["Costas Tyfoxylos"]
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<ctyfoxylos@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


class TestOrganizationMutabilityAndEntities(IntegrationTest):

    def setUp(self):
        super(TestOrganizationMutabilityAndEntities, self).setUp()
        organization = 'workflow'
        self.organization = self.tower.get_organization_by_name(organization)

    def test_mutating_name(self):
        with self.recorder:
            with self.assertRaises(InvalidValue):
                self.organization.name = 'a' * 513
            original_name = self.organization.name
            new_name = 'valid_name'
            self.organization.name = new_name
            self.assertEqual(self.organization.name, new_name)
            self.organization.name = original_name
            self.assertEqual(self.organization.name, original_name)

    def test_mutating_description(self):
        with self.recorder:
            original_description = self.organization.description
            new_description = 'valid_description'
            self.organization.description = new_description
            self.assertEqual(self.organization.description, new_description)
            self.organization.description = original_description
            self.assertEqual(self.organization.description, original_description)

    def test_mutating_custom_virtualenv(self):
        with self.recorder:
            with self.assertRaises(InvalidValue):
                self.organization.custom_virtualenv = 'a' * 101
            self.assertIsNone(self.organization.custom_virtualenv)

    def test_created_by_attribute(self):
        with self.recorder:
            self.assertIsInstance(self.organization.created_by, User)

    def test_modified_by_attribute(self):
        with self.recorder:
            self.assertIsInstance(self.organization.modified_by, User)

    def test_object_role_names(self):
        with self.recorder:
            self.assertEquals(set(self.organization.object_role_names), {'Admin',
                                                                         'Execute',
                                                                         'Project Admin',
                                                                         'Inventory Admin',
                                                                         'Credential Admin',
                                                                         'Workflow Admin',
                                                                         'Notification Admin',
                                                                         'Job Template Admin',
                                                                         'Auditor',
                                                                         'Member',
                                                                         'Read'})

    def test_object_roles(self):
        with self.recorder:
            self.assertIsInstance(self.organization.object_roles, EntityManager)

    def test_job_templates_count(self):
        with self.recorder:
            self.assertEquals(self.organization.job_templates_count, 0)

    def test_admins_count(self):
        with self.recorder:
            self.assertEquals(self.organization.admins_count, 1)

    def test_projects_count(self):
        with self.recorder:
            self.assertEquals(self.organization.projects_count, 1)

    def test_projects(self):
        with self.recorder:
            self.assertIsInstance(self.organization.projects, EntityManager)

    def test_projects_lifecycle(self):
        with self.recorder:
            url = 'https://github.com/ansible/ansible-tower-samples'
            project = self.organization.create_project('Project_name',
                                                       'description',
                                                       'Test Credential',
                                                       url)
            self.assertIsInstance(project, Project)
            duplicate_project = self.organization.create_project('Project_name',
                                                                 'description',
                                                                 'Test Credential',
                                                                 url)
            self.assertFalse(duplicate_project)
            with self.assertRaises(InvalidCredential):
                self.organization.create_project('name',
                                                 'description',
                                                 'No Credential',
                                                 'https://github.com/ansible/ansible-tower-samples')
            with Timeout(TIMEOUT_IN_SECONDS) as timeout:
                while project.status != 'successful':
                    if timeout.reached:
                        raise TimeoutError
                    time.sleep(1)
            self.assertTrue(self.organization.delete_project('Project_name'))
            with self.assertRaises(InvalidProject):
                self.organization.delete_project('Project_name')

    def test_users(self):
        with self.recorder:
            self.assertIsInstance(self.organization.users, EntityManager)

    def test_users_count(self):
        with self.recorder:
            self.assertEquals(self.organization.users_count, 2)

    def test_teams(self):
        with self.recorder:
            self.assertIsInstance(self.organization.teams, EntityManager)
            self.assertIsInstance(self.organization.get_team_by_name('workflow_team'), Team)
            self.assertIsNone(self.organization.get_team_by_name('non_existent_team'))

    def test_teams_count(self):
        with self.recorder:
            self.assertEquals(self.organization.teams_count, 1)

    def test_team_lifecycle(self):
        with self.recorder:
            team = self.organization.create_team('team_name',
                                                 'description')
            self.assertIsInstance(team, Team)
            duplicate_team = self.organization.create_team('team_name',
                                                           'description2')
            self.assertFalse(duplicate_team)
            self.assertTrue(self.organization.delete_team('team_name'))
            with self.assertRaises(InvalidTeam):
                self.organization.delete_team('team_name')

    def test_inventories(self):
        with self.recorder:
            self.assertIsInstance(self.organization.inventories, EntityManager)
            self.assertIsInstance(self.organization.get_inventory_by_name('Test Inventory'), Inventory)
            self.assertIsNone(self.organization.get_inventory_by_name('non_Test Inventory'))

    def test_inventories_count(self):
        with self.recorder:
            self.assertEquals(self.organization.inventories_count, 1)

    def test_inventory_lifecycle(self):
        with self.recorder:
            with self.assertRaises(InvalidVariables):
                self.organization.create_inventory('inventory_name',
                                                   'description',
                                                   'garbage')
            inventory = self.organization.create_inventory('inventory_name',
                                                           'description',
                                                           '{}')
            self.assertIsInstance(inventory, Inventory)
            duplicate_inventory = self.organization.create_inventory('inventory_name',
                                                                     'description2')
            self.assertFalse(duplicate_inventory)
            self.assertTrue(self.organization.delete_inventory('inventory_name'))
            with self.assertRaises(InvalidInventory):
                self.organization.delete_inventory('inventory_nameBroken')

    def test_credentials(self):
        with self.recorder:
            self.assertIsInstance(self.organization.credentials, EntityManager)
            self.assertIsInstance(self.organization.get_credential_by_name('Test Credential', 'Source Control'),
                                  GenericCredential)
            with self.assertRaises(InvalidCredentialType):
                self.organization.get_credential_by_name('Test Credential', 'Source ControlBroken')
            self.assertIsInstance(self.organization.get_credential_by_name_with_type_id('Test Credential', 2),
                                  GenericCredential)
            self.assertIsInstance(self.organization.get_credential_by_id(2), GenericCredential)
            self.assertIsNone(self.organization.get_credential_by_name('non_Test Credential', 'Source Control'))
            self.assertIsNone(self.organization.get_credential_by_name_with_type_id('non_Test Credential', 2))
            self.assertIsNone(self.organization.get_credential_by_id(999))
