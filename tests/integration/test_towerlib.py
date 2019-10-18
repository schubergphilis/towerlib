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

import copy
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
                               CredentialType,
                               GenericCredential,
                               JobTemplate)
from towerlib.towerlibexceptions import (AuthFailed,
                                         InvalidOrganization,
                                         InvalidUser,
                                         InvalidCredential,
                                         InvalidProject,
                                         InvalidTeam,
                                         InvalidInventory,
                                         InvalidGroup,
                                         InvalidVariables,
                                         InvalidHost,
                                         InvalidCredentialType,
                                         InvalidPlaybook,
                                         InvalidInstanceGroup,
                                         InvalidJobType,
                                         InvalidJobTemplate,
                                         InvalidVerbosity)
from . import IntegrationTest, placeholders
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
            url = 'https://github.com/ansible/ansible-tower-samples'
            duplicate_project = self.tower.create_project_in_organization('Default',
                                                                          'Project_name',
                                                                          'description',
                                                                          'Test Credential',
                                                                          url)
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
            with Timeout(TIMEOUT_IN_SECONDS) as timeout:
                while project.status != 'successful':
                    if timeout.reached:
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

    def test_tower_credential_types(self):
        with self.recorder:
            self.assertEqual(len(list(self.tower.tower_credential_types)), 19)

    def test_custom_credential_types(self):
        with self.recorder:
            self.assertEqual(len(list(self.tower.custom_credential_types)), 1)

    def test_credential_type_lifecycle(self):
        with self.recorder:
            credential = self.tower.create_credential_type('Test Credential Type',
                                                           'This is the description',
                                                           'net',
                                                           '{}',
                                                           '{}')
            self.assertIsInstance(credential, CredentialType)
            duplicate_credential = self.tower.create_credential_type('Test Credential Type',
                                                                     'This is the description',
                                                                     'net',
                                                                     '{}',
                                                                     '{}')
            self.assertIsNone(duplicate_credential)
            self.assertTrue(self.tower.delete_credential_type('Test Credential Type'))
            with self.assertRaises(InvalidCredentialType):
                self.tower.create_credential_type('Test Credential Type',
                                                  'This is the description',
                                                  'garbage',
                                                  '{}',
                                                  '{}')
            with self.assertRaises(InvalidVariables):
                self.tower.create_credential_type('Test Credential Type',
                                                  'This is the description',
                                                  'net',
                                                  'agadgffdsagsdffg',
                                                  '{}')
            with self.assertRaises(InvalidVariables):
                self.tower.create_credential_type('Test Credential Type',
                                                  'This is the description',
                                                  'net',
                                                  '{}',
                                                  'agadgffdsagsdffg')
            with self.assertRaises(InvalidCredentialType):
                self.tower.delete_credential_type('Non Existent Credential Type')

    def test_credentials(self):
        with self.recorder:
            self.assertIsInstance(self.tower.credentials, EntityManager)
            credentials_list = list(self.tower.get_credentials_by_name('Test Credential'))
            self.assertEqual(len(credentials_list), 2)
            credential = credentials_list[0]
            self.assertIsInstance(credential, GenericCredential)
            with self.assertRaises(InvalidCredentialType):
                _ = self.tower.get_organization_credential_by_name('Default',
                                                                   'Test Credential',
                                                                   'Garbage Credential Type')
            with self.assertRaises(InvalidOrganization):
                _ = self.tower.get_organization_credential_by_name('DefaultGarbage',
                                                                   'Test Credential',
                                                                   'Source Control')
            self.assertIsNone(self.tower.get_credential_type_by_name('Amazon Web ServicesBroken'))
            credential = self.tower.get_organization_credential_by_name('Default',
                                                                        'Test Credential',
                                                                        'Source Control')
            self.assertIsInstance(credential, GenericCredential)
            with self.assertRaises(InvalidOrganization):
                _ = self.tower.get_organization_credential_by_name_with_type_id('DefaultGarbage',
                                                                                'Test Credential',
                                                                                '2')
            credential = self.tower.get_organization_credential_by_name_with_type_id('Default',
                                                                                     'Test Credential',
                                                                                     '2')
            self.assertIsInstance(credential, GenericCredential)
            credential = self.tower.get_credential_by_id('2')
            self.assertIsInstance(credential, GenericCredential)
            self.assertIsNone(self.tower.get_credential_by_id('99999'))

    def test_credentials_lifecycle(self):
        with self.recorder:
            self.assertIsNone(self.tower.create_credential_with_credential_type_id('Testing',
                                                                                   '9999',
                                                                                   'description'))
            self.assertIsNone(self.tower.create_credential_with_credential_type_id('Testing',
                                                                                   '2',
                                                                                   'description',
                                                                                   '999'))
            self.assertIsNone(self.tower.create_credential_with_credential_type_id('Testing',
                                                                                   '2',
                                                                                   'description',
                                                                                   '1',
                                                                                   '999'))
            self.assertIsNone(self.tower.create_credential_with_credential_type_id('Testing',
                                                                                   '2',
                                                                                   'description',
                                                                                   '1',
                                                                                   '5',
                                                                                   '999'))
            credential = self.tower.create_credential_with_credential_type_id('Testing',
                                                                              '2',
                                                                              'description',
                                                                              '1',
                                                                              '5',
                                                                              '1')
            self.assertIsInstance(credential, GenericCredential)
            self.assertTrue(credential.delete())
            with self.assertRaises(InvalidOrganization):
                self.tower.create_credential_in_organization('BrokenOrg',
                                                             'CredName',
                                                             'CredDescription',
                                                             'workflow_admin',
                                                             'workflow_team',
                                                             'Source Control',
                                                             '{}')
            with self.assertRaises(InvalidUser):
                self.tower.create_credential_in_organization('workflow',
                                                             'CredName',
                                                             'CredDescription',
                                                             'workflow_adminBroken',
                                                             'workflow_team',
                                                             'Source Control',
                                                             '{}')
            with self.assertRaises(InvalidTeam):
                self.tower.create_credential_in_organization('workflow',
                                                             'CredName',
                                                             'CredDescription',
                                                             'workflow_admin',
                                                             'workflow_teamBroken',
                                                             'Source Control',
                                                             '{}')
            with self.assertRaises(InvalidCredentialType):
                self.tower.create_credential_in_organization('workflow',
                                                             'CredName',
                                                             'CredDescription',
                                                             'workflow_admin',
                                                             'workflow_team',
                                                             'Source Control Broken',
                                                             '{}')
            with self.assertRaises(InvalidVariables):
                self.tower.create_credential_in_organization('workflow',
                                                             'CredName',
                                                             'CredDescription',
                                                             'workflow_admin',
                                                             'workflow_team',
                                                             'Source Control',
                                                             'garbage')
            credential = self.tower.create_credential_in_organization('workflow',
                                                                      'CredName',
                                                                      'CredDescription',
                                                                      'workflow_admin',
                                                                      'workflow_team',
                                                                      'Source Control',
                                                                      '{}')
            self.assertIsInstance(credential, GenericCredential)
            with self.assertRaises(InvalidOrganization):
                self.tower.create_credential_in_organization_with_type_id('BrokenOrg',
                                                                          'CredName2',
                                                                          'CredDescription',
                                                                          'workflow_admin',
                                                                          'workflow_team',
                                                                          'Source Control',
                                                                          '{}')
            with self.assertRaises(InvalidUser):
                self.tower.create_credential_in_organization_with_type_id('workflow',
                                                                          'CredName2',
                                                                          'CredDescription',
                                                                          'workflow_adminBroken',
                                                                          'workflow_team',
                                                                          'Source Control',
                                                                          '{}')
            with self.assertRaises(InvalidTeam):
                self.tower.create_credential_in_organization_with_type_id('workflow',
                                                                          'CredName2',
                                                                          'CredDescription',
                                                                          'workflow_admin',
                                                                          'workflow_teamBroken',
                                                                          'Source Control',
                                                                          '{}')
            with self.assertRaises(InvalidVariables):
                self.tower.create_credential_in_organization_with_type_id('workflow',
                                                                          'CredName2',
                                                                          'CredDescription',
                                                                          'workflow_admin',
                                                                          'workflow_team',
                                                                          'Source Control',
                                                                          'garbage')
            credential_with_type_id = self.tower.create_credential_in_organization_with_type_id('workflow',
                                                                                                'CredName2',
                                                                                                'CredDescription',
                                                                                                'workflow_admin',
                                                                                                'workflow_team',
                                                                                                '2',
                                                                                                '{}')
            self.assertIsInstance(credential_with_type_id, GenericCredential)
            self.assertIsNone(self.tower.create_credential_in_organization_with_type_id('workflow',
                                                                                        'CredName2',
                                                                                        'CredDescription',
                                                                                        'workflow_admin',
                                                                                        'workflow_team',
                                                                                        '2',
                                                                                        '{}'))
            with self.assertRaises(InvalidOrganization):
                self.tower.delete_organization_credential_by_name('workflowBroken',
                                                                  'CredName',
                                                                  'Source Control')
            with self.assertRaises(InvalidCredentialType):
                self.tower.delete_organization_credential_by_name('workflow',
                                                                  'CredName',
                                                                  'Source ControlBroken')
            with self.assertRaises(InvalidCredential):
                self.tower.delete_organization_credential_by_name('workflow',
                                                                  'CredNameBroken',
                                                                  'Source Control')
            self.assertTrue(self.tower.delete_organization_credential_by_name('workflow',
                                                                              'CredName',
                                                                              'Source Control'))
            with self.assertRaises(InvalidOrganization):
                self.tower.delete_organization_credential_by_name_with_type_id('workflowBroken',
                                                                               'CredName2',
                                                                               '2')
            with self.assertRaises(InvalidCredential):
                self.tower.delete_organization_credential_by_name_with_type_id('workflow',
                                                                               'CredNameBroken',
                                                                               '2')
            self.assertTrue(self.tower.delete_organization_credential_by_name_with_type_id('workflow',
                                                                                           'CredName2',
                                                                                           '2'))

    def test_job_templates(self):
        with self.recorder:
            self.assertIsInstance(self.tower.job_templates, EntityManager)

    def test_job_templates_lifecycle(self):
        arguments = dict(name='Demo Job Template 2',
                         description='Description of job template',
                         organization='workflow',
                         inventory='Test Inventory',
                         project='Test Project',
                         playbook='hello_world.yml',
                         credential='Test Credential',
                         instance_groups=None,
                         host_config_key=None,
                         job_type='run',
                         vault_credential=None,
                         forks=0,
                         limit=0,
                         verbosity=0,
                         extra_vars='',
                         job_tags='',
                         force_handlers=False,
                         skip_tags='',
                         start_at_task='',
                         timeout=0,
                         use_fact_cache=False,
                         ask_diff_mode_on_launch=False,
                         ask_variables_on_launch=False,
                         ask_limit_on_launch=False,
                         ask_tags_on_launch=False,
                         ask_skip_tags_on_launch=False,
                         ask_job_type_on_launch=False,
                         ask_verbosity_on_launch=False,
                         ask_inventory_on_launch=False,
                         ask_credential_on_launch=False,
                         survey_enabled=False,
                         become_enabled=False,
                         diff_mode=False,
                         allow_simultaneous=False)
        with self.recorder:
            with self.assertRaises(InvalidInventory):
                args = copy.deepcopy(arguments)
                args['inventory'] = 'Broken'
                _ = self.tower.create_job_template(**args)
            with self.assertRaises(InvalidProject):
                args = copy.deepcopy(arguments)
                args['project'] = 'Broken'
                _ = self.tower.create_job_template(**args)
            with self.assertRaises(InvalidPlaybook):
                args = copy.deepcopy(arguments)
                args['playbook'] = 'Broken'
                _ = self.tower.create_job_template(**args)
            with self.assertRaises(InvalidCredential):
                args = copy.deepcopy(arguments)
                args['credential'] = 'Broken'
                _ = self.tower.create_job_template(**args)
            with self.assertRaises(InvalidInstanceGroup):
                args = copy.deepcopy(arguments)
                args['instance_groups'] = 'Broken'
                _ = self.tower.create_job_template(**args)
            with self.assertRaises(InvalidJobType):
                args = copy.deepcopy(arguments)
                args['job_type'] = 'Broken'
                _ = self.tower.create_job_template(**args)
            with self.assertRaises(InvalidVerbosity):
                args = copy.deepcopy(arguments)
                args['verbosity'] = 11
                _ = self.tower.create_job_template(**args)
            arguments['instance_groups'] = 'tower'
            job_template = self.tower.create_job_template(**arguments)
            self.assertIsInstance(job_template, JobTemplate)
            self.assertIsNone(self.tower.create_job_template(**arguments))
            job_template_by_name = self.tower.get_job_template_by_name(job_template.name)
            self.assertEqual(job_template.id, job_template_by_name.id)
            job_template_by_id = self.tower.get_job_template_by_id(job_template.id)
            self.assertEqual(job_template.id, job_template_by_id.id)
            with self.assertRaises(InvalidJobTemplate):
                self.tower.delete_job_template('NoneExistentJobTemplate')
            self.assertTrue(self.tower.delete_job_template(job_template.name))

    def test_roles(self):
        with self.recorder:
            self.assertIsInstance(self.tower.roles, EntityManager)

    def test_notification_templates(self):
        with self.recorder:
            self.assertIsInstance(self.tower.notification_templates, EntityManager)

    def test_object_by_url(self):
        url = '/api/v2/users/23/'
        user = self.tower._get_object_by_url('User', url)
        self.assertIsInstance(user, User)
