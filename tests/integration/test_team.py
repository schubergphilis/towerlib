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

    def test_mutating_team_name(self):
        with self.recorder:
            original_team_name = 'workflow_team'
            organization = 'workflow'
            team = self.tower.get_organization_team_by_name(organization, original_team_name)
            with self.assertRaises(InvalidValue):
                team.name = 'a' * 513
            team.name = 'valid_name'
            self.assertEqual(team.name, 'valid_name')
            team.name = original_team_name
            self.assertEqual(team.name, original_team_name)

    def test_mutating_team_description(self):
        with self.recorder:
            original_team_name = 'workflow_team'
            organization = 'workflow'
            team = self.tower.get_organization_team_by_name(organization, original_team_name)
            original_description = team.description
            team.description = 'valid_description'
            self.assertEqual(team.description, 'valid_description')
            team.description = original_description
            self.assertEqual(team.description, original_description)

    def test_mutating_team_organization(self):
        with self.recorder:
            original_team_name = 'workflow_team'
            organization = 'workflow'
            team = self.tower.get_organization_team_by_name(organization, original_team_name)
            original_organization = team.organization
            with self.assertRaises(InvalidOrganization):
                team.organization = 'NoOrgBroken'
            team.organization = 'Default'
            self.assertEqual(team.organization.name, 'Default')
            team.organization = original_organization.name
            self.assertEqual(team.organization.name, original_organization.name)

    def test_team_roles(self):
        with self.recorder:
            original_team_name = 'workflow_team'
            organization = 'workflow'
            team = self.tower.get_organization_team_by_name(organization, original_team_name)
            self.assertIsInstance(team.roles, EntityManager)

    def test_team_object_roles(self):
        with self.recorder:
            original_team_name = 'workflow_team'
            organization = 'workflow'
            team = self.tower.get_organization_team_by_name(organization, original_team_name)
            self.assertIsInstance(team.object_roles, EntityManager)
            self.assertEqual(set(team.object_role_names), {'Admin', 'Member', 'Read'})

    def test_team_users(self):
        with self.recorder:
            original_team_name = 'workflow_team'
            organization = 'workflow'
            team = self.tower.get_organization_team_by_name(organization, original_team_name)
            self.assertIsInstance(team.users, EntityManager)

    def test_team_credentials(self):
        with self.recorder:
            original_team_name = 'workflow_team'
            organization = 'workflow'
            team = self.tower.get_organization_team_by_name(organization, original_team_name)
            self.assertIsInstance(team.credentials, EntityManager)

    def test_team_projects(self):
        with self.recorder:
            original_team_name = 'workflow_team'
            organization = 'workflow'
            team = self.tower.get_organization_team_by_name(organization, original_team_name)
            self.assertIsInstance(team.projects, EntityManager)

    def test_mutating_team_users(self):
        with self.recorder:
            original_team_name = 'workflow_team'
            organization = 'workflow'
            username = 'workflow_normal'
            username_broken = 'workflow_normalBroken'
            team = self.tower.get_organization_team_by_name(organization, original_team_name)
            self.assertFalse(bool(list(team.users)))
            with self.assertRaises(InvalidUser):
                team.add_user_as_member(username_broken)
            self.assertTrue(team.add_user_as_member(username))
            user = team.get_user_by_username(username)
            self.assertTrue(user.username == username)
            self.assertTrue(team.remove_user_as_member(username))
            self.assertTrue(team.add_user_as_admin(username))
            self.assertTrue(team.remove_user_as_admin(username))

    def test_mutating_team_projects(self):
        with self.recorder:
            original_team_name = 'workflow_team'
            organization = 'workflow'
            project = 'Test project'
            project_broken = 'Test projectBroken'
            team = self.tower.get_organization_team_by_name(organization, original_team_name)
            with self.assertRaises(InvalidProject):
                team.add_project_permission_admin(project_broken)
            self.assertTrue(team.add_project_permission_admin(project))
            with self.assertRaises(InvalidProject):
                team.remove_project_permission_admin(project_broken)
            self.assertTrue(team.remove_project_permission_admin(project))
            with self.assertRaises(InvalidProject):
                team.add_project_permission_update(project_broken)
            self.assertTrue(team.add_project_permission_update(project))
            with self.assertRaises(InvalidProject):
                team.remove_project_permission_update(project_broken)
            self.assertTrue(team.remove_project_permission_update(project))
            with self.assertRaises(InvalidProject):
                team.add_project_permission_use(project_broken)
            self.assertTrue(team.add_project_permission_use(project))
            with self.assertRaises(InvalidProject):
                team.remove_project_permission_use(project_broken)
            self.assertTrue(team.remove_project_permission_use(project))

    def test_mutating_team_job_templates(self):
        with self.recorder:
            original_team_name = 'workflow_team'
            organization = 'workflow'
            job_template = 'Demo Job Template'
            job_template_broken = 'Demo Job TemplateBroken'
            team = self.tower.get_organization_team_by_name(organization, original_team_name)
            with self.assertRaises(InvalidJobTemplate):
                team.add_job_template_permission_admin(job_template_broken)
            self.assertTrue(team.add_job_template_permission_admin(job_template))
            with self.assertRaises(InvalidJobTemplate):
                team.remove_job_template_permission_admin(job_template_broken)
            self.assertTrue(team.remove_job_template_permission_admin(job_template))
            with self.assertRaises(InvalidJobTemplate):
                team.add_job_template_permission_execute(job_template_broken)
            self.assertTrue(team.add_job_template_permission_execute(job_template))
            with self.assertRaises(InvalidJobTemplate):
                team.remove_job_template_permission_execute(job_template_broken)
            self.assertTrue(team.remove_job_template_permission_execute(job_template))

    def test_mutating_team_inventory(self):
        with self.recorder:
            original_team_name = 'workflow_team'
            organization = 'workflow'
            inventory = 'Test Inventory'
            inventory_broken = 'Test InventoryBroken'
            team = self.tower.get_organization_team_by_name(organization, original_team_name)
            with self.assertRaises(InvalidInventory):
                team.add_inventory_permission_admin(inventory_broken)
            self.assertTrue(team.add_inventory_permission_admin(inventory))
            with self.assertRaises(InvalidInventory):
                team.remove_inventory_permission_admin(inventory_broken)
            self.assertTrue(team.remove_inventory_permission_admin(inventory))
            with self.assertRaises(InvalidInventory):
                team.add_inventory_permission_use(inventory_broken)
            self.assertTrue(team.add_inventory_permission_use(inventory))
            with self.assertRaises(InvalidInventory):
                team.remove_inventory_permission_use(inventory_broken)
            self.assertTrue(team.remove_inventory_permission_use(inventory))
            with self.assertRaises(InvalidInventory):
                team.add_inventory_permission_update(inventory_broken)
            self.assertTrue(team.add_inventory_permission_update(inventory))
            with self.assertRaises(InvalidInventory):
                team.remove_inventory_permission_update(inventory_broken)
            self.assertTrue(team.remove_inventory_permission_update(inventory))
            with self.assertRaises(InvalidInventory):
                team.add_inventory_permission_ad_hoc(inventory_broken)
            self.assertTrue(team.add_inventory_permission_ad_hoc(inventory))
            with self.assertRaises(InvalidInventory):
                team.remove_inventory_permission_ad_hoc(inventory_broken)
            self.assertTrue(team.remove_inventory_permission_ad_hoc(inventory))

    def test_mutating_team_credential_permission(self):
        with self.recorder:
            original_team_name = 'workflow_team'
            organization = 'workflow'
            credential = 'Test Credential'
            credential_type = 'Source Control'
            credential_broken = 'Test CredentialBroken'
            team = self.tower.get_organization_team_by_name(organization, original_team_name)
            with self.assertRaises(InvalidCredential):
                team.add_credential_permission_admin(credential_broken, credential_type)
            self.assertTrue(team.add_credential_permission_admin(credential, credential_type))
            with self.assertRaises(InvalidCredential):
                team.remove_credential_permission_admin(credential_broken, credential_type)
            self.assertTrue(team.remove_credential_permission_admin(credential, credential_type))
            with self.assertRaises(InvalidCredential):
                team.add_credential_permission_use(credential_broken, credential_type)
            self.assertTrue(team.add_credential_permission_use(credential, credential_type))
            with self.assertRaises(InvalidCredential):
                team.remove_credential_permission_use(credential_broken, credential_type)
            self.assertTrue(team.remove_credential_permission_use(credential, credential_type))
