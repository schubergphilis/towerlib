#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: test_project.py
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
test_project
----------------------------------
Tests for `project` module.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
from datetime import datetime

from towerlib.entities import (User,
                               GenericCredential)
from towerlib.towerlibexceptions import (InvalidOrganization,
                                         InvalidCredential,
                                         InvalidValue)
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


class TestProjectMutabilityAndEntities(IntegrationTest):

    def setUp(self):
        super(TestProjectMutabilityAndEntities, self).setUp()
        original_name = 'Test Project'
        organization = 'workflow'
        self.project = self.tower.get_organization_project_by_name(organization, original_name)

    def test_mutating_name(self):
        with self.recorder:
            with self.assertRaises(InvalidValue):
                self.project.name = 'a' * 513
            original_name = self.project.name
            self.project.name = 'valid_name'
            self.assertEqual(self.project.name, 'valid_name')
            self.project.name = original_name
            self.assertEqual(self.project.name, original_name)

    def test_playbooks(self):
        with self.recorder:
            self.assertTrue('hello_world.yml' in self.project.playbooks)

    def test_created_by_attribute(self):
        with self.recorder:
            self.assertIsInstance(self.project.created_by, User)

    def test_object_role_names(self):
        with self.recorder:
            self.assertEquals(set(self.project.object_role_names), {'Admin', 'Use', 'Update', 'Read'})

    def test_mutating_description(self):
        with self.recorder:
            original_description = self.project.description
            self.project.description = 'valid_description'
            self.assertEqual(self.project.description, 'valid_description')
            self.project.description = original_description
            self.assertEqual(self.project.description, original_description)

    def test_mutating_local_path(self):
        with self.recorder:
            self.assertEquals(self.project.local_path, '_8__test_project')

    def test_scm_type(self):
        with self.recorder:
            self.assertEquals(self.project.scm_type, 'git')

    def test_mutating_scm_url(self):
        with self.recorder:
            original_scm_url = self.project.scm_url
            with self.assertRaises(InvalidValue):
                self.project.scm_url = 'a' * 1025
            new_scm_url = 'https://test.com/whatever'
            self.project.scm_url = new_scm_url
            self.assertEqual(self.project.scm_url, new_scm_url)
            self.project.scm_url = original_scm_url
            self.assertEqual(self.project.scm_url, original_scm_url)

    def test_mutating_scm_branch(self):
        with self.recorder:
            original_scm_branch = self.project.scm_branch
            with self.assertRaises(InvalidValue):
                self.project.scm_branch = 'a' * 257
            self.project.scm_branch = 'valid_scm_branch'
            self.assertEqual(self.project.scm_branch, 'valid_scm_branch')
            self.project.scm_branch = original_scm_branch
            self.assertEqual(self.project.scm_branch, original_scm_branch)

    def test_mutating_scm_clean(self):
        with self.recorder:
            original_scm_clean = self.project.scm_clean
            self.project.scm_clean = not original_scm_clean
            self.assertEqual(self.project.scm_clean, not original_scm_clean)
            self.project.scm_clean = original_scm_clean
            self.assertEqual(self.project.scm_clean, original_scm_clean)

    def test_mutating_scm_delete_on_update(self):
        with self.recorder:
            original_scm_delete_on_update = self.project.scm_delete_on_update
            self.project.scm_delete_on_update = not original_scm_delete_on_update
            self.assertEqual(self.project.scm_delete_on_update, not original_scm_delete_on_update)
            self.project.scm_delete_on_update = original_scm_delete_on_update
            self.assertEqual(self.project.scm_delete_on_update, original_scm_delete_on_update)

    def test_mutating_credential(self):
        with self.recorder:
            self.assertIsInstance(self.project.credential, GenericCredential)
            with self.assertRaises(InvalidCredential):
                self.project.credential = 'BrokenCredname'
            self.project.credential = 'Test Credential'
            self.assertIsInstance(self.project.credential, GenericCredential)

    def test_mutating_timeout(self):
        with self.recorder:
            original_timeout = self.project.timeout
            with self.assertRaises(InvalidValue):
                self.project.timeout = -2147483649
            with self.assertRaises(InvalidValue):
                self.project.timeout = 2147483648
            new_timeout = 10
            self.project.timeout = new_timeout
            self.assertEquals(self.project.timeout, new_timeout)
            self.project.timeout = original_timeout
            self.assertEquals(self.project.timeout, original_timeout)

    def test_last_job_run(self):
        with self.recorder:
            self.assertIsInstance(self.project.last_job_run, datetime)

    def test_mutating_organization(self):
        with self.recorder:
            original_organization = self.project.organization
            with self.assertRaises(InvalidOrganization):
                self.project.organization = 'BrokenOrg'
            self.project.organization = 'Default'
            self.assertEquals(self.project.organization.name, 'Default')
            self.project.organization = original_organization.name
            self.assertEquals(self.project.organization.name, original_organization.name)

    def test_mutating_scm_delete_on_next_update(self):
        with self.recorder:
            self.assertIsNone(self.project.scm_delete_on_next_update)

    def test_mutating_scm_update_on_launch(self):
        with self.recorder:
            original_scm_update_on_launch = self.project.scm_update_on_launch
            self.project.scm_update_on_launch = not original_scm_update_on_launch
            self.assertEqual(self.project.scm_update_on_launch, not original_scm_update_on_launch)
            self.project.scm_update_on_launch = original_scm_update_on_launch
            self.assertEqual(self.project.scm_update_on_launch, original_scm_update_on_launch)

    def test_mutating_scm_update_cache_timeout(self):
        with self.recorder:
            original_scm_update_cache_timeout = self.project.scm_update_cache_timeout
            with self.assertRaises(InvalidValue):
                self.project.scm_update_cache_timeout = -1
            with self.assertRaises(InvalidValue):
                self.project.scm_update_cache_timeout = 2147483648
            new_scm_update_cache_timeout = 10
            self.project.scm_update_cache_timeout = new_scm_update_cache_timeout
            self.assertEquals(self.project.scm_update_cache_timeout, new_scm_update_cache_timeout)
            self.project.scm_update_cache_timeout = original_scm_update_cache_timeout
            self.assertEquals(self.project.scm_update_cache_timeout, original_scm_update_cache_timeout)

    def test_last_updated(self):
        with self.recorder:
            self.assertIsInstance(self.project.last_updated, datetime)

    def test_mutating_custom_virtualenv(self):
        with self.recorder:
            with self.assertRaises(InvalidValue):
                self.project.custom_virtualenv = 'a' * 101
