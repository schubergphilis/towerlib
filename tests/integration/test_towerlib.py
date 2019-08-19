#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: test_towerlib.py
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
test_towerlib
----------------------------------
Tests for `towerlib` module.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from . import IntegrationTest
import time

__author__ = '''Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''2018-05-25'''
__copyright__ = '''Copyright 2018, Costas Tyfoxylos'''
__credits__ = ["Costas Tyfoxylos"]
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<ctyfoxylos@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

MAX_RETRY = 10
TIME_SLEEP = 1

class TestTowerlib(IntegrationTest):

    def test_basic_workflow(self):
        with self.recorder:
            org_name = "workflow"
            team_name = "workflow_team"
            user_admin_name = "workflow_admin"
            user_normal_name = "workflow_normal"

            # Create organization
            org = self.tower.create_organization(org_name)
            self.assertIsNotNone(org)

            # Create a Team
            team = self.tower.create_team_in_organization(org_name, team_name)
            self.assertIsNotNone(team)

            # Create user, assign user to organization and team
            user_admin = self.tower.create_user(user_admin_name, "password")
            self.assertIsNotNone(user_admin)
            self.assertTrue(user_admin.associate_organization_role(org, 'Member'))
            self.assertTrue(user_admin.associate_organization_role(org, 'Admin'))
            # self.assertTrue(team.add_user_as_member(user_admin.username))

            # Create user, assign user to organization and team
            user_normal = self.tower.create_user(user_normal_name, "password")
            self.assertIsNotNone(user_normal)
            self.assertTrue(user_normal.associate_organization_role(org, 'Member'))
            self.assertTrue(user_normal.associate_organization_role(org, 'Execute'))
            # self.assertTrue(team.add_user_as_member(user_normal.username))

            # Create a credential
            credential = self.tower.create_credential_in_organization(
                org.name,
                'Test Credential',
                'Description',
                user_admin_name,
                team.name,
                'Source Control',
            )
            self.assertIsNotNone(credential)

            # Create a project to the organization
            project = self.tower.create_project_in_organization(
                org_name,
                "Test project",
                "Description",
                credential.name,
                "https://github.com/ansible/ansible-tower-samples",
                scm_update_on_launch=False,
                scm_clean=False
            )
            self.assertIsNotNone(project)

            inventory = self.tower.create_inventory_in_organization(
                org_name,
                'Test Inventory',
                'Test Description'
            )
            self.assertIsNotNone(inventory)

            host = inventory.create_host("example.com", "Test hostname")
            self.assertIsNotNone(host)

            group = inventory.create_group("Test Group", "Test Groups")
            self.assertIsNotNone(group)

            host_r = self.tower.get_inventory_host_by_name(org_name, inventory.name, "example.com")
            self.assertIsNotNone(host_r)

            # We need to fully checkout the project before we can create the template
            # @TODO: Fix the create_job_template to allow creation without validating if it exists or not
            time.sleep(90)

            jt = self.tower.create_job_template(
                "Test Template",
                "Test Description",
                org_name,
                inventory.name,
                project.name,
                "hello_world.yml",
                credential.name,
                'Source Control'
            )
            self.assertIsNotNone(jt)

            self.assertTrue(jt.delete())
            self.assertTrue(group.delete())
            self.assertTrue(host.delete())
            self.assertTrue(self.tower.delete_organization_inventory(org_name, inventory.name))
            self.assertTrue(credential.delete())
            self.assertTrue(user_admin.delete())
            self.assertTrue(user_normal.delete())

            # Project requires a full checkout before it can be deleted. So we will need to wait a bit before
            # deleting it
            self.assertTrue(project.delete())

            self.assertTrue(self.tower.delete_team_in_organization(org_name, team_name))
            self.assertTrue(org.delete())
