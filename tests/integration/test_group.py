#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: test_group.py
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
test_group
----------------------------------
Tests for `group` module.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from towerlib.entities import (EntityManager,
                               Inventory,
                               User)
from towerlib.towerlibexceptions import (InvalidValue,
                                         InvalidGroup, InvalidHost)


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


class TestGroupMutabilityAndEntities(IntegrationTest):

    def setUp(self):
        super(TestGroupMutabilityAndEntities, self).setUp()
        self.group = self.tower.get_group_by_id(1)
        self.transient_group = self.tower.create_inventory_group('workflow',
                                                                 'Test Inventory',
                                                                 'Transient Group',
                                                                 'Description')
        self.transient_host = self.tower.create_host_in_inventory('workflow',
                                                                  'Test Inventory',
                                                                  'Transient Host',
                                                                  'Description',
                                                                  '{}')

    def tearDown(self):
        self.transient_group.delete()
        self.transient_host.delete()
        super(TestGroupMutabilityAndEntities, self).tearDown()

    def test_mutating_name(self):
        with self.recorder:
            with self.assertRaises(InvalidValue):
                self.group.name = 'a' * 513
            original_name = self.group.name
            new_name = 'valid_name'
            self.group.name = new_name
            self.assertEqual(self.group.name, new_name)
            self.group.name = original_name
            self.assertEqual(self.group.name, original_name)

    def test_mutating_description(self):
        with self.recorder:
            original_description = self.group.description
            new_description = 'valid_description'
            self.group.description = new_description
            self.assertEqual(self.group.description, new_description)
            self.group.description = original_description
            self.assertEqual(self.group.description, original_description)

    def test_inventory(self):
        with self.recorder:
            self.assertIsInstance(self.group.inventory, Inventory)

    def test_mutating_variables(self):
        with self.recorder:
            with self.assertRaises(InvalidValue):
                self.group.variables = 'garbage'
            original_variables = self.group.variables
            new_variables = '{"valid_variable":"value"}'
            self.group.variables = new_variables
            self.assertEqual(self.group.variables, new_variables)
            self.group.variables = original_variables
            self.assertEqual(self.group.variables, original_variables)

    def test_total_hosts_count(self):
        with self.recorder:
            self.assertEquals(self.group.total_hosts_count, 0)

    def test_total_groups_count(self):
        with self.recorder:
            self.assertEquals(self.group.total_groups_count, 0)

    def test_has_inventory_sources(self):
        with self.recorder:
            self.assertFalse(self.group.has_inventory_sources)

    def test_created_by(self):
        with self.recorder:
            self.assertIsInstance(self.group.created_by, User)

    def test_hosts(self):
        with self.recorder:
            self.assertIsInstance(self.group.hosts, EntityManager)

    def test_host_lifecycle(self):
        with self.recorder:
            self.assertEquals(len(list(self.group.hosts)), 0)
            self.assertTrue(self.group.add_host_by_name('Transient Host'))
            self.assertEquals(len(list(self.group.hosts)), 1)
            self.assertTrue(self.group.remove_host_by_name('Transient Host'))
            self.assertEquals(len(list(self.group.hosts)), 0)
            with self.assertRaises(InvalidHost):
                self.group.add_host_by_name('Transient HostBroken')
            with self.assertRaises(InvalidHost):
                self.group.remove_host_by_name('Test GroupBroken')

    def test_groups(self):
        with self.recorder:
            self.assertIsInstance(self.group.groups, EntityManager)

    def test_group_lifecycle(self):
        with self.recorder:
            self.assertEquals(len(list(self.group.groups)), 0)
            self.assertTrue(self.group.associate_group_by_name('Transient Group'))
            self.assertEquals(len(list(self.group.groups)), 1)
            self.assertTrue(self.group.disassociate_group_by_name('Transient Group'))
            self.assertEquals(len(list(self.group.groups)), 0)
            with self.assertRaises(InvalidGroup):
                self.group.associate_group_by_name('Transient GroupBroken')
            with self.assertRaises(InvalidGroup):
                self.group.disassociate_group_by_name('Transient GroupBroken')
