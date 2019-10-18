#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: test_credential.py
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
test_credential
----------------------------------
Tests for `credential` module.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""


from towerlib.entities import (EntityManager, User)

from towerlib.towerlibexceptions import (InvalidValue, InvalidCredentialType, InvalidOrganization)


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


class TestCredentialTypeMutabilityAndEntities(IntegrationTest):

    def setUp(self):
        super(TestCredentialTypeMutabilityAndEntities, self).setUp()
        self.credential_type = self.tower.get_credential_type_by_name('Machine')
        self.custom_credential_type = self.tower.create_credential_type('CustomCredentialType',
                                                                        'Custom description',
                                                                        'Cloud',
                                                                        inputs_=('{"fields": [{"id": "username",'
                                                                                 '"label": "Username",'
                                                                                 '"type": "string"}]}'),
                                                                        injectors='{"file": {"template": "test"}}'
                                                                        )

    def tearDown(self):
        self.custom_credential_type.delete()
        super(TestCredentialTypeMutabilityAndEntities, self).tearDown()

    def test_mutating_name(self):
        with self.recorder:
            with self.assertRaises(InvalidValue):
                self.custom_credential_type.name = 'a' * 513
            original_name = self.custom_credential_type.name
            new_name = 'valid_name'
            self.custom_credential_type.name = new_name
            self.assertEqual(self.custom_credential_type.name, new_name)
            self.custom_credential_type.name = original_name
            self.assertEqual(self.custom_credential_type.name, original_name)

    def test_mutating_description(self):
        with self.recorder:
            original_description = self.custom_credential_type.description
            new_description = 'valid_description'
            self.custom_credential_type.description = new_description
            self.assertEqual(self.custom_credential_type.description, new_description)
            self.custom_credential_type.description = original_description
            self.assertEqual(self.custom_credential_type.description, original_description)

    def test_kind(self):
        with self.recorder:
            self.assertEquals(self.credential_type.kind, 'ssh')

    def test_managed_by_tower(self):
        with self.recorder:
            self.assertTrue(self.credential_type.managed_by_tower)

    def test_mutating_inputs(self):
        with self.recorder:
            with self.assertRaises(InvalidValue):
                self.custom_credential_type.inputs = 'garbage'
            original_inputs = self.custom_credential_type.inputs
            new_inputs = {'fields': [{'id': 'new_value', 'type': 'string', 'label': 'New Label'}]}
            self.custom_credential_type.inputs = new_inputs
            self.assertEqual(self.custom_credential_type.inputs, new_inputs)
            self.custom_credential_type.inputs = original_inputs
            self.assertEqual(self.custom_credential_type.inputs, original_inputs)

    def test_mutating_injectors(self):
        with self.recorder:
            with self.assertRaises(InvalidValue):
                self.custom_credential_type.injectors = 'garbage'
            original_injectors = self.custom_credential_type.injectors
            new_injectors = {'file': {'template': 'new_value'}}
            self.custom_credential_type.injectors = new_injectors
            self.assertEqual(self.custom_credential_type.injectors, new_injectors)
            self.custom_credential_type.injectors = original_injectors
            self.assertEqual(self.custom_credential_type.injectors, original_injectors)


class TestCredentialMutabilityAndEntities(IntegrationTest):

    def setUp(self):
        super(TestCredentialMutabilityAndEntities, self).setUp()
        self.credential = self.tower.get_credential_by_id(1)

    def test_host(self):
        with self.recorder:
            self.assertIsNone(self.credential.host)

    def test_project(self):
        with self.recorder:
            self.assertIsNone(self.credential.project)

    def test_created_by(self):
        with self.recorder:
            self.assertIsInstance(self.credential.created_by, User)

    def test_modified_by(self):
        with self.recorder:
            self.assertIsInstance(self.credential.modified_by, User)

    def test_object_roles(self):
        with self.recorder:
            self.assertIsInstance(self.credential.object_roles, EntityManager)

    def test_owner_users(self):
        with self.recorder:
            self.assertIsInstance(self.credential.owner_users, EntityManager)

    def test_owner_teams(self):
        with self.recorder:
            self.assertIsInstance(self.credential.owner_teams, EntityManager)

    def test_mutating_name(self):
        with self.recorder:
            with self.assertRaises(InvalidValue):
                self.credential.name = 'a' * 513
            original_name = self.credential.name
            new_name = 'valid_name'
            self.credential.name = new_name
            self.assertEqual(self.credential.name, new_name)
            self.credential.name = original_name
            self.assertEqual(self.credential.name, original_name)

    def test_mutating_description(self):
        with self.recorder:
            original_description = self.credential.description
            new_description = 'valid_description'
            self.credential.description = new_description
            self.assertEqual(self.credential.description, new_description)
            self.credential.description = original_description
            self.assertEqual(self.credential.description, original_description)

    def test_mutating_organization(self):
        with self.recorder:
            original_organization = self.credential.organization
            with self.assertRaises(InvalidOrganization):
                self.credential.organization = 'brokenOrg'
            new_organization = 'workflow'
            self.credential.organization = new_organization
            self.assertEqual(self.credential.organization.name, new_organization)
            self.credential.organization = original_organization.name
            self.assertEqual(self.credential.organization.name, original_organization.name)

    def test_mutating_credential_type(self):
        with self.recorder:
            _ = self.credential.credential_type
            new_credential_type = 'BrokenCredType'
            with self.assertRaises(InvalidCredentialType):
                self.credential.credential_type = new_credential_type

    def test_mutating_inputs(self):
        with self.recorder:
            with self.assertRaises(InvalidValue):
                self.credential.inputs = 'garbage'
            original_inputs = self.credential.inputs
            new_inputs = {'username': 'new'}
            self.credential.inputs = new_inputs
            self.assertEqual(self.credential.inputs, new_inputs)
            self.credential.inputs = original_inputs
            self.assertEqual(self.credential.inputs, original_inputs)

    def test_mutating_username(self):
        with self.recorder:
            original_username = self.credential.username
            new_username = 'valid_username'
            self.credential.username = new_username
            self.assertEqual(self.credential.username, new_username)
            self.credential.username = original_username
            self.assertEqual(self.credential.username, original_username)
