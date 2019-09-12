#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: test_inventory.py
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
test_inventory
----------------------------------
Tests for `inventory` module.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import time

from towerlib.entities import (EntityManager,
                               User,
                               Project,
                               Team,
                               Inventory,
                               GenericCredential,
                               Group,
                               Host)
from towerlib.towerlibexceptions import (InvalidValue,
                                         InvalidCredential,
                                         InvalidProject,
                                         InvalidTeam,
                                         InvalidVariables,
                                         InvalidInventory, InvalidCredentialType, InvalidOrganization, InvalidGroup,
                                         InvalidHost)
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


class TestInventoryMutabilityAndEntities(IntegrationTest):

    def setUp(self):
        super(TestInventoryMutabilityAndEntities, self).setUp()
        organization = 'workflow'
        inventory = 'Test Inventory'
        self.inventory = self.tower.get_organization_inventory_by_name(organization, inventory)

    def test_created_by_attribute(self):
        with self.recorder:
            self.assertIsInstance(self.inventory.created_by, User)

    def test_object_roles(self):
        with self.recorder:
            self.assertIsInstance(self.inventory.object_roles, EntityManager)

    def test_object_role_names(self):
        with self.recorder:
            self.assertEquals(set(self.inventory.object_role_names), {'Admin', 'Update', 'Ad Hoc', 'Use', 'Read'})

    def test_mutating_name(self):
        with self.recorder:
            with self.assertRaises(InvalidValue):
                self.inventory.name = 'a' * 513
            original_name = self.inventory.name
            new_name = 'valid_name'
            self.inventory.name = new_name
            self.assertEqual(self.inventory.name, new_name)
            self.inventory.name = original_name
            self.assertEqual(self.inventory.name, original_name)

    def test_mutating_description(self):
        with self.recorder:
            original_description = self.inventory.description
            new_description = 'valid_description'
            self.inventory.description = new_description
            self.assertEqual(self.inventory.description, new_description)
            self.inventory.description = original_description
            self.assertEqual(self.inventory.description, original_description)

    def test_mutating_organization(self):
        with self.recorder:
            original_organization = self.inventory.organization
            new_organization = 'Default'
            self.inventory.organization = new_organization
            self.assertEqual(self.inventory.organization.name, new_organization)
            self.inventory.organization = original_organization.name
            self.assertEqual(self.inventory.organization.name, original_organization.name)
            with self.assertRaises(InvalidOrganization):
                self.inventory.organization = 'GarbageOrg'

    def test_kind(self):
        with self.recorder:
            self.assertEquals(self.inventory.kind, '')

    def test_host_filter(self):
        with self.recorder:
            self.assertIsNone(self.inventory.host_filter)

    def test_has_inventory_sources(self):
        with self.recorder:
            self.assertFalse(self.inventory.has_inventory_sources)

    def test_mutating_variables(self):
        with self.recorder:
            original_variables = self.inventory.variables
            new_variables = '{"key":"value"}'
            self.inventory.variables = new_variables
            self.assertEqual(self.inventory.variables, new_variables)
            self.inventory.variables = original_variables
            self.assertEqual(self.inventory.variables, original_variables)
            with self.assertRaises(InvalidValue):
                self.inventory.variables = 'GarbageVariables'

    def test_total_host_count(self):
        with self.recorder:
            self.assertEquals(self.inventory.total_hosts_count, 1)

    def test_total_groups_count(self):
        with self.recorder:
            self.assertEquals(self.inventory.total_groups_count, 1)

    def test_total_inventory_sources_count(self):
        with self.recorder:
            self.assertEquals(self.inventory.total_inventory_sources_count, 0)

    def test_insights_credential(self):
        with self.recorder:
            self.assertIsNone(self.inventory.insights_credential)

    def test_pending_deletion(self):
        with self.recorder:
            self.assertFalse(self.inventory.pending_deletion)

    def test_hosts(self):
        with self.recorder:
            self.assertEquals(len(list(self.inventory.hosts)), 1)
            self.assertIsInstance(self.inventory.get_host_by_name('example.com'), Host)
            self.assertIsNone(self.inventory.get_host_by_name('example.comBroken'))

    def test_hosts_lifecycle(self):
        with self.recorder:
            host = self.inventory.create_host('Host_name',
                                              'description',
                                              '{}')
            self.assertIsInstance(host, Host)
            duplicate_host = self.inventory.create_host('Host_name',
                                                        'description',
                                                        '{}')
            self.assertFalse(duplicate_host)
            with self.assertRaises(InvalidVariables):
                self.inventory.create_host('Host_name',
                                            'description',
                                            'garbage')
            self.assertTrue(self.inventory.delete_host('Host_name'))
            with self.assertRaises(InvalidHost):
                self.inventory.delete_host('Host_name')

    def test_groups(self):
        with self.recorder:
            self.assertEquals(len(list(self.inventory.groups)), 1)
            self.assertIsInstance(self.inventory.get_group_by_name('Test Group'), Group)
            self.assertIsNone(self.inventory.get_group_by_name('Test GroupBroken'))

    def test_groups_lifecycle(self):
        with self.recorder:
            group = self.inventory.create_group('Group_name',
                                                'description',
                                                '{}')
            self.assertIsInstance(group, Group)
            duplicate_group = self.inventory.create_group('Group_name',
                                                          'description',
                                                          '{}')
            self.assertFalse(duplicate_group)
            with self.assertRaises(InvalidVariables):
                self.inventory.create_group('Group_name',
                                            'description',
                                            'garbage')
            self.assertTrue(self.inventory.delete_group('Group_name'))
            with self.assertRaises(InvalidGroup):
                self.inventory.delete_group('Group_name')
