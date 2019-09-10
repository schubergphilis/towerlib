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

    def test_mutating_project_name(self):
        with self.recorder:
            original_project_name = 'Test Project'
            organization = 'workflow'
            project = self.tower.get_organization_project_by_name(organization, original_project_name)
            with self.assertRaises(InvalidValue):
                project.name = 'a' * 513
            project.name = 'valid_name'
            self.assertEqual(project.name, 'valid_name')
            project.name = original_project_name
            self.assertEqual(project.name, original_project_name)

    def test_project_playbooks(self):
        with self.recorder:
            original_project_name = 'Test Project'
            organization = 'workflow'
            project = self.tower.get_organization_project_by_name(organization, original_project_name)
            self.assertTrue('hello_world.yml' in project.playbooks)

    def test_project_created_by_attribute(self):
        with self.recorder:
            original_project_name = 'Test Project'
            organization = 'workflow'
            project = self.tower.get_organization_project_by_name(organization, original_project_name)
            self.assertIsInstance(project.created_by, User)

    def test_project_object_role_names(self):
        with self.recorder:
            original_project_name = 'Test Project'
            organization = 'workflow'
            project = self.tower.get_organization_project_by_name(organization, original_project_name)
            self.assertEquals(set(project.object_role_names), {'Admin', 'Use', 'Update', 'Read'})

    def test_mutating_project_description(self):
        with self.recorder:
            original_project_name = 'Test Project'
            organization = 'workflow'
            project = self.tower.get_organization_project_by_name(organization, original_project_name)
            original_project_description = project.description
            project.description = 'valid_description'
            self.assertEqual(project.description, 'valid_description')
            project.description = original_project_description
            self.assertEqual(project.description, original_project_description)

    def test_mutating_project_local_path(self):
        with self.recorder:
            original_project_name = 'Test Project'
            organization = 'workflow'
            project = self.tower.get_organization_project_by_name(organization, original_project_name)
            self.assertEquals(project.local_path, '_8__test_project')

    def test_project_scm_type(self):
        with self.recorder:
            original_project_name = 'Test Project'
            organization = 'workflow'
            project = self.tower.get_organization_project_by_name(organization, original_project_name)
            self.assertEquals(project.scm_type, 'git')

    def test_mutating_project_scm_url(self):
        with self.recorder:
            original_project_name = 'Test Project'
            organization = 'workflow'
            project = self.tower.get_organization_project_by_name(organization, original_project_name)
            original_project_scm_url = project.scm_url
            with self.assertRaises(InvalidValue):
                project.scm_url = 'a' * 1025
            new_scm_url = 'https://test.com/whatever'
            project.scm_url = new_scm_url
            self.assertEqual(project.scm_url, new_scm_url)
            project.scm_url = original_project_scm_url
            self.assertEqual(project.scm_url, original_project_scm_url)

    def test_mutating_project_scm_branch(self):
        with self.recorder:
            original_project_name = 'Test Project'
            organization = 'workflow'
            project = self.tower.get_organization_project_by_name(organization, original_project_name)
            original_project_scm_branch = project.scm_branch
            with self.assertRaises(InvalidValue):
                project.scm_branch = 'a' * 257
            project.scm_branch = 'valid_scm_branch'
            self.assertEqual(project.scm_branch, 'valid_scm_branch')
            project.scm_branch = original_project_scm_branch
            self.assertEqual(project.scm_branch, original_project_scm_branch)

    def test_mutating_project_scm_clean(self):
        with self.recorder:
            original_project_name = 'Test Project'
            organization = 'workflow'
            project = self.tower.get_organization_project_by_name(organization, original_project_name)
            original_project_scm_clean = project.scm_clean
            project.scm_clean = not original_project_scm_clean
            self.assertEqual(project.scm_clean, not original_project_scm_clean)
            project.scm_clean = original_project_scm_clean
            self.assertEqual(project.scm_clean, original_project_scm_clean)

    def test_mutating_project_scm_delete_on_update(self):
        with self.recorder:
            original_project_name = 'Test Project'
            organization = 'workflow'
            project = self.tower.get_organization_project_by_name(organization, original_project_name)
            original_project_scm_delete_on_update = project.scm_delete_on_update
            project.scm_delete_on_update = not original_project_scm_delete_on_update
            self.assertEqual(project.scm_delete_on_update, not original_project_scm_delete_on_update)
            project.scm_delete_on_update = original_project_scm_delete_on_update
            self.assertEqual(project.scm_delete_on_update, original_project_scm_delete_on_update)

    def test_mutating_project_credential(self):
        with self.recorder:
            original_project_name = 'Test Project'
            organization = 'workflow'
            project = self.tower.get_organization_project_by_name(organization, original_project_name)
            self.assertIsInstance(project.credential, GenericCredential)
            with self.assertRaises(InvalidCredential):
                project.credential = 'BrokenCredname'
            project.credential = 'Test Credential'
            self.assertIsInstance(project.credential, GenericCredential)

    def test_mutating_project_timeout(self):
        with self.recorder:
            original_project_name = 'Test Project'
            organization = 'workflow'
            project = self.tower.get_organization_project_by_name(organization, original_project_name)
            original_project_timeout = project.timeout
            with self.assertRaises(InvalidValue):
                project.timeout = -2147483649
            with self.assertRaises(InvalidValue):
                project.timeout = 2147483648
            new_timeout = 10
            project.timeout = new_timeout
            self.assertEquals(project.timeout, new_timeout)
            project.timeout = original_project_timeout
            self.assertEquals(project.timeout, original_project_timeout)

    def test_project_last_job_run(self):
        with self.recorder:
            original_project_name = 'Test Project'
            organization = 'workflow'
            project = self.tower.get_organization_project_by_name(organization, original_project_name)
            self.assertIsInstance(project.last_job_run, datetime)

    def test_mutating_project_organization(self):
        with self.recorder:
            original_project_name = 'Test Project'
            organization = 'workflow'
            project = self.tower.get_organization_project_by_name(organization, original_project_name)
            original_project_organization = project.organization
            with self.assertRaises(InvalidOrganization):
                project.organization = 'BrokenOrg'
            project.organization = 'Default'
            self.assertEquals(project.organization.name, 'Default')
            project.organization = original_project_organization.name
            self.assertEquals(project.organization.name, original_project_organization.name)

    def test_mutating_project_scm_delete_on_next_update(self):
        with self.recorder:
            original_project_name = 'Test Project'
            organization = 'workflow'
            project = self.tower.get_organization_project_by_name(organization, original_project_name)
            self.assertIsNone(project.scm_delete_on_next_update)

    def test_mutating_project_scm_update_on_launch(self):
        with self.recorder:
            original_project_name = 'Test Project'
            organization = 'workflow'
            project = self.tower.get_organization_project_by_name(organization, original_project_name)
            original_project_scm_update_on_launch = project.scm_update_on_launch
            project.scm_update_on_launch = not original_project_scm_update_on_launch
            self.assertEqual(project.scm_update_on_launch, not original_project_scm_update_on_launch)
            project.scm_update_on_launch = original_project_scm_update_on_launch
            self.assertEqual(project.scm_update_on_launch, original_project_scm_update_on_launch)

    def test_mutating_project_scm_update_cache_timeout(self):
        with self.recorder:
            original_project_name = 'Test Project'
            organization = 'workflow'
            project = self.tower.get_organization_project_by_name(organization, original_project_name)
            original_project_scm_update_cache_timeout = project.scm_update_cache_timeout
            with self.assertRaises(InvalidValue):
                project.scm_update_cache_timeout = -1
            with self.assertRaises(InvalidValue):
                project.scm_update_cache_timeout = 2147483648
            new_scm_update_cache_timeout = 10
            project.scm_update_cache_timeout = new_scm_update_cache_timeout
            self.assertEquals(project.scm_update_cache_timeout, new_scm_update_cache_timeout)
            project.scm_update_cache_timeout = original_project_scm_update_cache_timeout
            self.assertEquals(project.scm_update_cache_timeout, original_project_scm_update_cache_timeout)

    def test_project_last_updated(self):
        with self.recorder:
            original_project_name = 'Test Project'
            organization = 'workflow'
            project = self.tower.get_organization_project_by_name(organization, original_project_name)
            self.assertIsInstance(project.last_updated, datetime)

    def test_mutating_project_custom_virtualenv(self):
        with self.recorder:
            original_project_name = 'Test Project'
            organization = 'workflow'
            project = self.tower.get_organization_project_by_name(organization, original_project_name)
            with self.assertRaises(InvalidValue):
                project.custom_virtualenv = 'a' * 101
