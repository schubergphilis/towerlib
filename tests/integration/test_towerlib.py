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

import time

from towerlib.entities import (Cluster,
                               EntityManager,
                               Organization,
                               User,
                               Project,
                               Team,
                               Group,
                               Inventory,
                               Host,
                               CredentialType)
from towerlib.towerlibexceptions import (AuthFailed,
                                         InvalidOrganization,
                                         InvalidUser,
                                         InvalidCredential,
                                         InvalidProject,
                                         InvalidTeam,
                                         InvalidInventory,
                                         InvalidGroup,
                                         InvalidVariables,
                                         InvalidHost)
from . import IntegrationTest, placeholders

__author__ = '''Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''2018-05-25'''
__copyright__ = '''Copyright 2018, Costas Tyfoxylos'''
__credits__ = ["Costas Tyfoxylos"]
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<ctyfoxylos@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


class Timeout:
    def __init__(self, seconds):
        self.seconds = seconds

    def __enter__(self):
        self.die_after = time.time() + self.seconds
        return self

    def __exit__(self, type, value, traceback):
        pass

    @property
    def timed_out(self):
        return time.time() > self.die_after


class TestTowerlib(IntegrationTest):

    def test_authentication(self):
        with self.recorder:
            with self.assertRaises(AuthFailed):
                self.tower._authenticate(self.recorder.session,
                                         self.tower._generate_host_name(placeholders.get('hostname'), secure=False),
                                         username='garbage',
                                         password='wrongP4ssw0rd',
                                         api_url=self.tower.api)

    def test_configuration(self):
        with self.recorder:
            self.assertIsNone(self.tower.configuration.license_info.subscription_name)
            self.assertTrue(self.tower.configuration.license_info.license_key == 'OPEN')
            self.assertTrue(self.tower.configuration.license_info.valid_key)

    def test_cluster(self):
        with self.recorder:
            self.assertIsInstance(self.tower.cluster, Cluster)
            self.assertTrue(len(self.tower.cluster.instances) >= 1)

    def test_organizations(self):
        with self.recorder:
            self.assertIsInstance(self.tower.organizations, EntityManager)
            default_org = self.tower.get_organization_by_name('Default')
            self.assertIsInstance(default_org, Organization)
            self.assertTrue(default_org.name == self.tower.get_organization_by_id(default_org.id).name)

    def test_organization_lifecycle(self):
        with self.recorder:
            org = self.tower.create_organization('Test_Org', 'Test Org description')
            self.assertIsInstance(org, Organization)
            self.assertIsNone(self.tower.create_organization('Test_Org', 'Test Org description'))
            self.assertTrue(self.tower.delete_organization('Test_Org'))
            with self.assertRaises(InvalidOrganization):
                self.assertFalse(self.tower.delete_organization('Test_Org'))

    def test_external_users(self):
        with self.recorder:
            self.assertTrue(len(list(self.tower.external_users)) == 0)

    def test_local_users(self):
        with self.recorder:
            self.assertTrue(len(list(self.tower.local_users)) >= 1)

    def test_user_retrieval(self):
        with self.recorder:
            admin_user = self.tower.get_user_by_username('admin')
            self.assertIsInstance(admin_user, User)
            self.assertIsNone(self.tower.get_user_by_username('NoSuchUser'))
            self.assertTrue(admin_user.username == self.tower.get_user_by_id(admin_user.id).username)

    def test_user_lifecycle(self):
        with self.recorder:
            user = self.tower.create_user('new_user',
                                          'password',
                                          'first_name',
                                          'last_name',
                                          'new@user.com')
            self.assertIsInstance(user, User)
            duplicate_user = self.tower.create_user('new_user',
                                                    'password2',
                                                    'first_name2',
                                                    'last_name2',
                                                    'new2s@user.com')
            self.assertIsNone(duplicate_user)
            self.assertTrue(self.tower.delete_user('new_user'))
            with self.assertRaises(InvalidUser):
                self.tower.delete_user('new_user')

    def test_organization_user_lifecycle(self):
        with self.recorder:
            user = self.tower.create_user_in_organization('Default',
                                                          'new_org_user',
                                                          'password',
                                                          'first_name',
                                                          'last_name',
                                                          'new@user.com')
            self.assertIsInstance(user, User)
            duplicate_user = self.tower.create_user_in_organization('Default',
                                                                    'new_org_user',
                                                                    'password',
                                                                    'first_name',
                                                                    'last_name',
                                                                    'new@user.com')
            self.assertFalse(duplicate_user)
            self.assertTrue(self.tower.delete_user('new_org_user'))
            with self.assertRaises(InvalidUser):
                self.tower.delete_user('new_org_user')
            with self.assertRaises(InvalidOrganization):
                self.tower.create_user_in_organization('Non_existant_Organization',
                                                       'new_org_user',
                                                       'password',
                                                       'first_name',
                                                       'last_name',
                                                       'new@user.com')

    def test_projects(self):
        with self.recorder:
            self.assertIsInstance(self.tower.projects, EntityManager)
            projects_generator = self.tower.get_projects_by_name('Demo Project')
            demo_project = list(projects_generator)[0]
            self.assertIsInstance(demo_project, Project)
            project = self.tower.get_organization_project_by_name('Default', 'Demo Project')
            self.assertIsInstance(project, Project)
            self.assertTrue(project.name == self.tower.get_project_by_id(project.id).name)
            with self.assertRaises(InvalidOrganization):
                self.tower.get_organization_project_by_name('Non_existent_org_name', 'Non existent project name')

    def test_project_lifecycle(self):
        with self.recorder:
            project = self.tower.create_project_in_organization('Default',
                                                                'Project_name',
                                                                'description',
                                                                'Test Credential',
                                                                'https://github.com/ansible/ansible-tower-samples')
            self.assertIsInstance(project, Project)
            duplicate_project = self.tower.create_project_in_organization('Default',
                                                                          'Project_name',
                                                                          'description',
                                                                          'Test Credential',
                                                                          'https://github.com/ansible/ansible-tower-samples')
            self.assertFalse(duplicate_project)
            with self.assertRaises(InvalidOrganization):
                self.tower.create_project_in_organization('NoOrg',
                                                          'name',
                                                          'description',
                                                          'Test Credential',
                                                          'https://github.com/ansible/ansible-tower-samples')
            with self.assertRaises(InvalidCredential):
                self.tower.create_project_in_organization('Default',
                                                          'name',
                                                          'description',
                                                          'No Credential',
                                                          'https://github.com/ansible/ansible-tower-samples')
            with Timeout(60) as timeout:
                while project.status != 'successful':
                    if timeout.timed_out:
                        raise TimeoutError
                    time.sleep(1)
            self.assertTrue(self.tower.delete_organization_project('Default', 'Project_name'))
            with self.assertRaises(InvalidOrganization):
                self.tower.delete_organization_project('DefaultBroken', 'Project_name')
            with self.assertRaises(InvalidProject):
                self.tower.delete_organization_project('Default', 'Project_name')

    def test_teams(self):
        with self.recorder:
            self.assertIsInstance(self.tower.teams, EntityManager)
            team_generator = self.tower.get_teams_by_name('workflow_team')
            team = list(team_generator)[0]
            self.assertIsInstance(team, Team)
            self.assertTrue(team.name == self.tower.get_team_by_id(team.id).name)
            _ = self.tower.get_organization_team_by_name('workflow', 'workflow_team')
            with self.assertRaises(InvalidOrganization):
                self.tower.get_organization_team_by_name('workflowBroken', 'workflow_team')

    def test_team_lifecycle(self):
        with self.recorder:
            team = self.tower.create_team_in_organization('Default',
                                                          'team_name',
                                                          'description')
            self.assertIsInstance(team, Team)
            duplicate_team = self.tower.create_team_in_organization('Default',
                                                                    'team_name',
                                                                    'description2')
            self.assertFalse(duplicate_team)
            with self.assertRaises(InvalidOrganization):
                self.tower.create_team_in_organization('DefaultBroken',
                                                       'team_name',
                                                       'description2')
            self.assertTrue(self.tower.delete_team_in_organization('Default', 'team_name'))
            with self.assertRaises(InvalidOrganization):
                self.tower.delete_team_in_organization('DefaultBroken', 'team_name')
            with self.assertRaises(InvalidTeam):
                self.tower.delete_team_in_organization('Default', 'team_name')

    def test_groups(self):
        with self.recorder:
            self.assertIsInstance(self.tower.groups, EntityManager)
            group = self.tower.get_inventory_group_by_name('workflow', 'Test Inventory', 'Test Group')
            self.assertIsInstance(group, Group)
            self.assertTrue(group.name == self.tower.get_group_by_id(group.id).name)

    def test_group_lifecycle(self):
        with self.recorder:
            group = self.tower.create_inventory_group('Default',
                                                      'Demo Inventory',
                                                      'group_name',
                                                      'description')
            self.assertIsInstance(group, Group)
            duplicate_group = self.tower.create_inventory_group('Default',
                                                                'Demo Inventory',
                                                                'group_name',
                                                                'description2')
            self.assertFalse(duplicate_group)
            with self.assertRaises(InvalidOrganization):
                self.tower.create_inventory_group('DefaultBroken',
                                                  'Demo Inventory',
                                                  'group_name',
                                                  'description')
            with self.assertRaises(InvalidInventory):
                self.tower.create_inventory_group('Default',
                                                  'Demo Inventory Broken',
                                                  'group_name',
                                                  'description')
            self.assertTrue(self.tower.delete_inventory_group('Default', 'Demo Inventory', 'group_name'))
            with self.assertRaises(InvalidOrganization):
                self.tower.delete_inventory_group('DefaultBroken', 'Demo Inventory', 'group_name')
            with self.assertRaises(InvalidInventory):
                self.tower.delete_inventory_group('Default', 'Demo Inventory Broken', 'group_name')
            with self.assertRaises(InvalidGroup):
                self.tower.delete_inventory_group('Default', 'Demo Inventory', 'group_name_broken')

    def test_inventories(self):
        with self.recorder:
            self.assertIsInstance(self.tower.inventories, EntityManager)
            inventory_generator = self.tower.get_inventories_by_name('Demo Inventory')
            inventory = list(inventory_generator)[0]
            self.assertIsInstance(inventory, Inventory)
            self.assertTrue(inventory.name == self.tower.get_inventory_by_id(inventory.id).name)

    def test_inventory_lifecycle(self):
        with self.recorder:
            inventory = self.tower.create_organization_inventory('Default',
                                                                 'Inventory_name',
                                                                 'description',
                                                                 '{}')
            self.assertIsInstance(inventory, Inventory)
            duplicate_inventory = self.tower.create_organization_inventory('Default',
                                                                           'Inventory_name',
                                                                           'description2',
                                                                           '{}')
            self.assertFalse(duplicate_inventory)
            with self.assertRaises(InvalidOrganization):
                self.tower.create_organization_inventory('DefaultBroken',
                                                         'Inventory_name',
                                                         'description2',
                                                         '{}')
            with self.assertRaises(InvalidVariables):
                self.tower.create_organization_inventory('Default',
                                                         'Inventory_name',
                                                         'description2',
                                                         'broken')
            self.assertTrue(self.tower.delete_organization_inventory('Default', 'Inventory_name'))
            with self.assertRaises(InvalidOrganization):
                self.tower.delete_organization_inventory('DefaultBroken', 'Inventory_name')
            with self.assertRaises(InvalidInventory):
                self.tower.delete_organization_inventory('Default', 'Inventory_nameBroken')

    def test_hosts(self):
        with self.recorder:
            self.assertIsInstance(self.tower.hosts, EntityManager)
            host_generator = self.tower.get_hosts_by_name('example.com')
            host = list(host_generator)[0]
            self.assertIsInstance(host, Host)
            self.assertTrue(host.name == self.tower.get_host_by_id(host.id).name)
            other_host = self.tower.get_inventory_host_by_name('workflow', 'Test Inventory', 'example.com')
            self.assertTrue(host.name == other_host.name)
            with self.assertRaises(InvalidInventory):
                self.tower.get_inventory_host_by_name('workflow', 'Test Inventory Broken', 'example.com')

    def test_host_lifecycle(self):
        with self.recorder:
            host = self.tower.create_host_in_inventory('workflow',
                                                       'Test Inventory',
                                                       'host_name',
                                                       'description',
                                                       '{}')
            self.assertIsInstance(host, Host)
            duplicate_host = self.tower.create_host_in_inventory('workflow',
                                                                 'Test Inventory',
                                                                 'host_name',
                                                                 'description2',
                                                                 '{}')
            self.assertFalse(duplicate_host)
            with self.assertRaises(InvalidHost):
                self.tower.associate_groups_with_inventory_host('workflow',
                                                                'Test Inventory',
                                                                'host_nameBroken',
                                                                'Test Group')
            self.assertTrue(self.tower.associate_groups_with_inventory_host('workflow',
                                                                            'Test Inventory',
                                                                            'host_name',
                                                                            'Test Group'))
            self.assertTrue(self.tower.disassociate_groups_from_inventory_host('workflow',
                                                                               'Test Inventory',
                                                                               'host_name',
                                                                               'Test Group'))
            with self.assertRaises(InvalidHost):
                self.tower.disassociate_groups_from_inventory_host('workflow',
                                                                   'Test Inventory',
                                                                   'host_nameBroken',
                                                                   'Test Group')
            with self.assertRaises(InvalidOrganization):
                self.tower.create_host_in_inventory('workflowBroken',
                                                    'Test Inventory',
                                                    'host_name',
                                                    'description2',
                                                    '{}')
            with self.assertRaises(InvalidInventory):
                self.tower.create_host_in_inventory('workflow',
                                                    'Test Inventory broken',
                                                    'host_name',
                                                    'description2',
                                                    '{}')
            self.assertTrue(self.tower.delete_inventory_host('workflow', 'Test Inventory', 'host_name'))
            with self.assertRaises(InvalidOrganization):
                self.tower.delete_inventory_host('workflowBroken', 'Test Inventory', 'host_name')
            with self.assertRaises(InvalidInventory):
                self.tower.delete_inventory_host('workflow', 'Test Inventory Broken', 'host_name')
            with self.assertRaises(InvalidHost):
                self.tower.delete_inventory_host('workflow', 'Test Inventory', 'host_name')

    def test_instances(self):
        with self.recorder:
            self.assertIsInstance(self.tower.instances, EntityManager)

    def test_instance_groups(self):
        with self.recorder:
            self.assertIsInstance(self.tower.instance_groups, EntityManager)

    def test_credential_types(self):
        with self.recorder:
            self.assertIsInstance(self.tower.credential_types, EntityManager)
            credential_type = self.tower.get_credential_type_by_name('Amazon Web Services')
            self.assertIsInstance(credential_type, CredentialType)
            self.assertIsNone(self.tower.get_credential_type_by_name('Amazon Web ServicesBroken'))
            self.assertTrue(credential_type.name == self.tower.get_credential_type_by_id(credential_type.id).name)


    # def test_basic_workflow(self):
    #     with self.recorder:
    #         org_name = "workflow"
    #         team_name = "workflow_team"
    #         user_admin_name = "workflow_admin"
    #         user_normal_name = "workflow_normal"
    #
    #         # Create organization
    #         org = self.tower.create_organization(org_name)
    #         self.assertIsNotNone(org)
    #
    #         # Create a Team
    #         team = self.tower.create_team_in_organization(org_name, team_name)
    #         self.assertIsNotNone(team)
    #
    #         # Create user, assign user to organization and team
    #         user_admin = self.tower.create_user(user_admin_name, "password")
    #         self.assertIsNotNone(user_admin)
    #         self.assertTrue(user_admin.associate_organization_role(org, 'Member'))
    #         self.assertTrue(user_admin.associate_organization_role(org, 'Admin'))
    #         # self.assertTrue(team.add_user_as_member(user_admin.username))
    #
    #         # Create user, assign user to organization and team
    #         user_normal = self.tower.create_user(user_normal_name, "password")
    #         self.assertIsNotNone(user_normal)
    #         self.assertTrue(user_normal.associate_organization_role(org, 'Member'))
    #         self.assertTrue(user_normal.associate_organization_role(org, 'Execute'))
    #         # self.assertTrue(team.add_user_as_member(user_normal.username))
    #
    #         # Create a credential
    #         credential = self.tower.create_credential_in_organization(
    #             org.name,
    #             'Test Credential',
    #             'Description',
    #             user_admin_name,
    #             team.name,
    #             'Source Control',
    #         )
    #         self.assertIsNotNone(credential)
    #
    #         # Create a project to the organization
    #         project = self.tower.create_project_in_organization(
    #             org_name,
    #             "Test project",
    #             "Description",
    #             credential.name,
    #             "https://github.com/ansible/ansible-tower-samples",
    #             scm_update_on_launch=False,
    #             scm_clean=False
    #         )
    #         self.assertIsNotNone(project)
    #
    #         inventory = self.tower.create_inventory_in_organization(
    #             org_name,
    #             'Test Inventory',
    #             'Test Description'
    #         )
    #         self.assertIsNotNone(inventory)
    #
    #         host = inventory.create_host("example.com", "Test hostname")
    #         self.assertIsNotNone(host)
    #
    #         group = inventory.create_group("Test Group", "Test Groups")
    #         self.assertIsNotNone(group)
    #
    #         host_r = self.tower.get_inventory_host_by_name(org_name, inventory.name, "example.com")
    #         self.assertIsNotNone(host_r)
    #
    #         # We need to fully checkout the project before we can create the template
    #         # @TODO: Fix the create_job_template to allow creation without validating if it exists or not
    #         if not self.tower.mock:
    #             time.sleep(90)
    #
    #         jt = self.tower.create_job_template(
    #             "Test Template",
    #             "Test Description",
    #             org_name,
    #             inventory.name,
    #             project.name,
    #             "hello_world.yml",
    #             credential.name,
    #             'Source Control'
    #         )
    #         self.assertIsNotNone(jt)
    #
    #         self.assertTrue(self.tower.delete_job_template(jt.name))
    #         self.assertTrue(self.tower.delete_inventory_group(org_name, inventory.name, group.name))
    #         self.assertTrue(self.tower.delete_inventory_host(org_name, inventory.name, host.name))
    #         self.assertTrue(self.tower.delete_organization_inventory(org_name, inventory.name))
    #         self.assertTrue(self.tower.delete_organization_credential_by_name(org_name, credential.name,
    #                                                                           'Source Control'))
    #         self.assertTrue(self.tower.delete_user(user_admin.username))
    #         self.assertTrue(self.tower.delete_user(user_normal.username))
    #
    #         # Project requires a full checkout before it can be deleted. So we will need to wait a bit before
    #         # deleting it
    #         self.assertTrue(project.delete())
    #
    #         self.assertTrue(self.tower.delete_team_in_organization(org_name, team_name))
    #         self.assertTrue(self.tower.delete_organization(org.name))
