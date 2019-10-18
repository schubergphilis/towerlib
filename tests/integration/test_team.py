#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: test_team.py
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
test_team
----------------------------------
Tests for `team` module.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from towerlib.entities import EntityManager
from towerlib.towerlibexceptions import (InvalidOrganization,
                                         InvalidUser,
                                         InvalidCredential,
                                         InvalidProject,
                                         InvalidInventory,
                                         InvalidValue, InvalidJobTemplate)


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


class TestTeamMutabilityAndEntities(IntegrationTest):

    def setUp(self):
        super(TestTeamMutabilityAndEntities, self).setUp()
        original_name = 'workflow_team'
        organization = 'workflow'
        self.team = self.tower.get_organization_team_by_name(organization, original_name)

    def test_mutating_name(self):
        with self.recorder:

            with self.assertRaises(InvalidValue):
                self.team.name = 'a' * 513
            original_name = self.team.name
            self.team.name = 'valid_name'
            self.assertEqual(self.team.name, 'valid_name')
            self.team.name = original_name
            self.assertEqual(self.team.name, original_name)

    def test_mutating_description(self):
        with self.recorder:
            original_description = self.team.description
            self.team.description = 'valid_description'
            self.assertEqual(self.team.description, 'valid_description')
            self.team.description = original_description
            self.assertEqual(self.team.description, original_description)

    def test_mutating_organization(self):
        with self.recorder:
            original_organization = self.team.organization
            with self.assertRaises(InvalidOrganization):
                self.team.organization = 'NoOrgBroken'
            self.team.organization = 'Default'
            self.assertEqual(self.team.organization.name, 'Default')
            self.team.organization = original_organization.name
            self.assertEqual(self.team.organization.name, original_organization.name)

    def test_roles(self):
        with self.recorder:
            self.assertIsInstance(self.team.roles, EntityManager)

    def test_object_roles(self):
        with self.recorder:
            self.assertIsInstance(self.team.object_roles, EntityManager)
            self.assertEqual(set(self.team.object_role_names), {'Admin', 'Member', 'Read'})

    def test_users(self):
        with self.recorder:
            self.assertIsInstance(self.team.users, EntityManager)

    def test_credentials(self):
        with self.recorder:
            self.assertIsInstance(self.team.credentials, EntityManager)

    def test_projects(self):
        with self.recorder:
            self.assertIsInstance(self.team.projects, EntityManager)

    def test_mutating_users(self):
        with self.recorder:
            username = 'workflow_normal'
            username_broken = 'workflow_normalBroken'
            self.assertFalse(bool(list(self.team.users)))
            with self.assertRaises(InvalidUser):
                self.team.add_user_as_member(username_broken)
            self.assertTrue(self.team.add_user_as_member(username))
            user = self.team.get_user_by_username(username)
            self.assertTrue(user.username == username)
            self.assertTrue(self.team.remove_user_as_member(username))
            self.assertTrue(self.team.add_user_as_admin(username))
            self.assertTrue(self.team.remove_user_as_admin(username))

    def test_mutating_projects(self):
        with self.recorder:
            project = 'Test project'
            project_broken = 'Test projectBroken'
            with self.assertRaises(InvalidProject):
                self.team.add_project_permission_admin(project_broken)
            self.assertTrue(self.team.add_project_permission_admin(project))
            with self.assertRaises(InvalidProject):
                self.team.remove_project_permission_admin(project_broken)
            self.assertTrue(self.team.remove_project_permission_admin(project))
            with self.assertRaises(InvalidProject):
                self.team.add_project_permission_update(project_broken)
            self.assertTrue(self.team.add_project_permission_update(project))
            with self.assertRaises(InvalidProject):
                self.team.remove_project_permission_update(project_broken)
            self.assertTrue(self.team.remove_project_permission_update(project))
            with self.assertRaises(InvalidProject):
                self.team.add_project_permission_use(project_broken)
            self.assertTrue(self.team.add_project_permission_use(project))
            with self.assertRaises(InvalidProject):
                self.team.remove_project_permission_use(project_broken)
            self.assertTrue(self.team.remove_project_permission_use(project))

    def test_mutating_job_templates(self):
        with self.recorder:
            job_template = 'Demo Job Template'
            job_template_broken = 'Demo Job TemplateBroken'
            with self.assertRaises(InvalidJobTemplate):
                self.team.add_job_template_permission_admin(job_template_broken)
            self.assertTrue(self.team.add_job_template_permission_admin(job_template))
            with self.assertRaises(InvalidJobTemplate):
                self.team.remove_job_template_permission_admin(job_template_broken)
            self.assertTrue(self.team.remove_job_template_permission_admin(job_template))
            with self.assertRaises(InvalidJobTemplate):
                self.team.add_job_template_permission_execute(job_template_broken)
            self.assertTrue(self.team.add_job_template_permission_execute(job_template))
            with self.assertRaises(InvalidJobTemplate):
                self.team.remove_job_template_permission_execute(job_template_broken)
            self.assertTrue(self.team.remove_job_template_permission_execute(job_template))

    def test_mutating_inventory(self):
        with self.recorder:
            inventory = 'Test Inventory'
            inventory_broken = 'Test InventoryBroken'
            with self.assertRaises(InvalidInventory):
                self.team.add_inventory_permission_admin(inventory_broken)
            self.assertTrue(self.team.add_inventory_permission_admin(inventory))
            with self.assertRaises(InvalidInventory):
                self.team.remove_inventory_permission_admin(inventory_broken)
            self.assertTrue(self.team.remove_inventory_permission_admin(inventory))
            with self.assertRaises(InvalidInventory):
                self.team.add_inventory_permission_use(inventory_broken)
            self.assertTrue(self.team.add_inventory_permission_use(inventory))
            with self.assertRaises(InvalidInventory):
                self.team.remove_inventory_permission_use(inventory_broken)
            self.assertTrue(self.team.remove_inventory_permission_use(inventory))
            with self.assertRaises(InvalidInventory):
                self.team.add_inventory_permission_update(inventory_broken)
            self.assertTrue(self.team.add_inventory_permission_update(inventory))
            with self.assertRaises(InvalidInventory):
                self.team.remove_inventory_permission_update(inventory_broken)
            self.assertTrue(self.team.remove_inventory_permission_update(inventory))
            with self.assertRaises(InvalidInventory):
                self.team.add_inventory_permission_ad_hoc(inventory_broken)
            self.assertTrue(self.team.add_inventory_permission_ad_hoc(inventory))
            with self.assertRaises(InvalidInventory):
                self.team.remove_inventory_permission_ad_hoc(inventory_broken)
            self.assertTrue(self.team.remove_inventory_permission_ad_hoc(inventory))

    def test_mutating_credential_permission(self):
        with self.recorder:
            credential = 'Test Credential'
            credential_type = 'Source Control'
            credential_broken = 'Test CredentialBroken'
            with self.assertRaises(InvalidCredential):
                self.team.add_credential_permission_admin(credential_broken, credential_type)
            self.assertTrue(self.team.add_credential_permission_admin(credential, credential_type))
            with self.assertRaises(InvalidCredential):
                self.team.remove_credential_permission_admin(credential_broken, credential_type)
            self.assertTrue(self.team.remove_credential_permission_admin(credential, credential_type))
            with self.assertRaises(InvalidCredential):
                self.team.add_credential_permission_use(credential_broken, credential_type)
            self.assertTrue(self.team.add_credential_permission_use(credential, credential_type))
            with self.assertRaises(InvalidCredential):
                self.team.remove_credential_permission_use(credential_broken, credential_type)
            self.assertTrue(self.team.remove_credential_permission_use(credential, credential_type))
