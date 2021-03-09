#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: test_job.py
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
test_job
----------------------------------
Tests for `job` module.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from datetime import datetime

from towerlib.entities import (EntityManager,
                               User,
                               Inventory,
                               Project,
                               JobRun)
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


class TestJobEntities(IntegrationTest):

    # def setUp(self):
    #     super(TestJobEntities, self).setUp()
    #     self.job = self.tower.get_job_by_id(2)
    #
    # def test_mutating_name(self):
    #     with self.recorder:
    #         with self.assertRaises(InvalidValue):
    #             self.job.name = 'a' * 513
    #         original_name = self.job.name
    #         new_name = 'valid_jobname'
    #         self.job.name = new_name
    #         self.assertEqual(self.job.name, new_name)
    #         self.job.name = original_name
    #         self.assertEqual(self.job.name, original_name)
    #
    # def test_mutating_description(self):
    #     with self.recorder:
    #         original_description = self.job.description
    #         new_description = 'valid_description'
    #         self.job.description = new_description
    #         self.assertEqual(self.job.description, new_description)
    #         self.job.description = original_description
    #         self.assertEqual(self.job.description, original_description)
    #
    # def test_inventory(self):
    #     with self.recorder:
    #         self.assertIsInstance(self.job.inventory, Inventory)
    #
    # def test_mutating_enabled(self):
    #     with self.recorder:
    #         original_enabled = self.job.enabled
    #         new_enabled = not original_enabled
    #         self.job.enabled = new_enabled
    #         self.assertEqual(self.job.enabled, new_enabled)
    #         self.job.enabled = original_enabled
    #         self.assertEqual(self.job.enabled, original_enabled)
    #
    # def test_mutating_instance_id(self):
    #     with self.recorder:
    #         with self.assertRaises(InvalidValue):
    #             self.job.instance_id = 'a' * 1025
    #         original_instance_id = self.job.instance_id
    #         new_instance_id = 'valid_instance_id'
    #         self.job.instance_id = new_instance_id
    #         self.assertEqual(self.job.instance_id, new_instance_id)
    #         self.job.instance_id = original_instance_id
    #         self.assertEqual(self.job.instance_id, original_instance_id)
    #
    # def test_mutating_variables(self):
    #     with self.recorder:
    #         with self.assertRaises(InvalidValue):
    #             self.job.variables = 'garbage'
    #         original_variables = self.job.variables
    #         new_variables = '{"valid_variable":"value"}'
    #         self.job.variables = new_variables
    #         self.assertEqual(self.job.variables, new_variables)
    #         self.job.variables = original_variables
    #         self.assertEqual(self.job.variables, original_variables)
    #
    # def test_has_inventory_sources(self):
    #     with self.recorder:
    #         self.assertFalse(self.job.has_inventory_sources)
    #
    # def test_insights_system_id(self):
    #     with self.recorder:
    #         self.assertIsNone(self.job.insights_system_id)
    #
    # def test_created_by(self):
    #     with self.recorder:
    #         self.assertIsInstance(self.job.created_by, User)
    #
    # def test_modified_by(self):
    #     with self.recorder:
    #         self.assertIsInstance(self.job.modified_by, User)
    #
    # def test_groups(self):
    #     with self.recorder:
    #         self.assertIsInstance(self.job.groups, EntityManager)
    #
    def test_job_template_attributes(self):
        with self.recorder:
            template_name = 'Demo Job Template'
            job_template = self.tower.get_job_template_by_name(template_name)
            self.assertIsInstance(job_template.created_by, User)
            self.assertIsInstance(job_template.modified_by, User)
            self.assertIsInstance(job_template.modified_at, datetime)
            self.assertEquals(job_template.name, template_name)
            self.assertEquals(job_template.description, '')
            self.assertEquals(job_template.job_type, 'run')
            self.assertIsInstance(job_template.inventory, Inventory)
            self.assertIsInstance(job_template.project, Project)
            self.assertEquals(job_template.playbook, 'hello_world.yml')
            self.assertIsInstance(job_template.credentials, EntityManager)
            self.assertIsInstance(job_template.extra_credentials, EntityManager)
            self.assertIsInstance(job_template.object_roles, EntityManager)
            self.assertIsNone(job_template.vault_credential)
            self.assertEquals(job_template.limit, '')
            self.assertEquals(job_template.verbosity, 0)
            self.assertEquals(job_template.job_tags, '')
            self.assertFalse(job_template.force_handlers)
            self.assertEquals(job_template.skip_tags, '')
            self.assertEquals(job_template.extra_vars, '')
            self.assertEquals(job_template.start_at_task, '')
            self.assertEquals(job_template.timeout, 0)
            self.assertEquals(job_template.forks_count, 0)
            self.assertFalse(job_template.use_fact_cache)
            self.assertFalse(job_template.ask_diff_mode_on_launch)
            self.assertFalse(job_template.ask_variables_on_launch)
            self.assertFalse(job_template.ask_limit_on_launch)
            self.assertFalse(job_template.ask_tags_on_launch)
            self.assertFalse(job_template.ask_skip_tags_on_launch)
            self.assertFalse(job_template.ask_job_type_on_launch)
            self.assertFalse(job_template.ask_verbosity_on_launch)
            self.assertFalse(job_template.ask_inventory_on_launch)
            self.assertFalse(job_template.ask_credential_on_launch)
            self.assertFalse(job_template.survey_enabled)
            self.assertFalse(job_template.become_enabled)
            self.assertFalse(job_template.allow_simultaneous)
            self.assertFalse(job_template.diff_mode)
            self.assertIsInstance(job_template.launch(), JobRun)
            self.assertIsNone(job_template.launch(inventory='Bogus'))
            self.assertEquals(job_template.survey_spec, {})

    def test_jobs(self):
        with self.recorder:
            self.assertIsInstance(self.tower.jobs, EntityManager)

    def test_job_templates(self):
        with self.recorder:
            self.assertIsInstance(self.tower.job_templates, EntityManager)

    def test_unified_jobs(self):
        with self.recorder:
            self.assertIsInstance(self.tower.unified_jobs, EntityManager)

    def test_unified_job_templates(self):
        with self.recorder:
            self.assertIsInstance(self.tower.unified_job_templates, EntityManager)

    def test_system_jobs(self):
        with self.recorder:
            self.assertIsInstance(self.tower.system_jobs, EntityManager)

    def test_workflow_jobs(self):
        with self.recorder:
            self.assertIsInstance(self.tower.workflow_jobs, EntityManager)

    def test_workflow_job_templates(self):
        with self.recorder:
            self.assertIsInstance(self.tower.workflow_job_templates, EntityManager)
