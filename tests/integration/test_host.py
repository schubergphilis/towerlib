#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: test_host.py
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
test_host
----------------------------------
Tests for `host` module.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from towerlib.entities import (EntityManager,
                               Inventory,
                               User)
from towerlib.towerlibexceptions import (InvalidValue,
                                         InvalidGroup)


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


class TestHostMutabilityAndEntities(IntegrationTest):

    def setUp(self):
        super(TestHostMutabilityAndEntities, self).setUp()
        self.host = self.tower.get_host_by_id(2)

    def test_mutating_name(self):
        with self.recorder:
            with self.assertRaises(InvalidValue):
                self.host.name = 'a' * 513
            original_name = self.host.name
            new_name = 'valid_hostname'
            self.host.name = new_name
            self.assertEqual(self.host.name, new_name)
            self.host.name = original_name
            self.assertEqual(self.host.name, original_name)

    def test_mutating_description(self):
        with self.recorder:
            original_description = self.host.description
            new_description = 'valid_description'
            self.host.description = new_description
            self.assertEqual(self.host.description, new_description)
            self.host.description = original_description
            self.assertEqual(self.host.description, original_description)

    def test_inventory(self):
        with self.recorder:
            self.assertIsInstance(self.host.inventory, Inventory)

    def test_mutating_enabled(self):
        with self.recorder:
            original_enabled = self.host.enabled
            new_enabled = not original_enabled
            self.host.enabled = new_enabled
            self.assertEqual(self.host.enabled, new_enabled)
            self.host.enabled = original_enabled
            self.assertEqual(self.host.enabled, original_enabled)

    def test_mutating_instance_id(self):
        with self.recorder:
            with self.assertRaises(InvalidValue):
                self.host.instance_id = 'a' * 1025
            original_instance_id = self.host.instance_id
            new_instance_id = 'valid_instance_id'
            self.host.instance_id = new_instance_id
            self.assertEqual(self.host.instance_id, new_instance_id)
            self.host.instance_id = original_instance_id
            self.assertEqual(self.host.instance_id, original_instance_id)

    def test_mutating_variables(self):
        with self.recorder:
            with self.assertRaises(InvalidValue):
                self.host.variables = 'garbage'
            original_variables = self.host.variables
            new_variables = '{"valid_variable":"value"}'
            self.host.variables = new_variables
            self.assertEqual(self.host.variables, new_variables)
            self.host.variables = original_variables
            self.assertEqual(self.host.variables, original_variables)

    def test_has_inventory_sources(self):
        with self.recorder:
            self.assertFalse(self.host.has_inventory_sources)

    def test_insights_system_id(self):
        with self.recorder:
            self.assertIsNone(self.host.insights_system_id)

    def test_created_by(self):
        with self.recorder:
            self.assertIsInstance(self.host.created_by, User)

    def test_modified_by(self):
        with self.recorder:
            self.assertIsInstance(self.host.modified_by, User)

    def test_groups(self):
        with self.recorder:
            self.assertIsInstance(self.host.groups, EntityManager)

    def test_groups_lifecycle(self):
        with self.recorder:
            self.assertEquals(len(list(self.host.groups)), 0)
            self.assertTrue(self.host.associate_with_groups('Test Group'))
            self.assertEquals(len(list(self.host.groups)), 1)
            self.assertTrue(self.host.disassociate_with_groups('Test Group'))
            self.assertEquals(len(list(self.host.groups)), 0)
            with self.assertRaises(InvalidGroup):
                self.host.associate_with_groups('Test GroupBroken')
            with self.assertRaises(InvalidGroup):
                self.host.disassociate_with_groups('Test GroupBroken')
