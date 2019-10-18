#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: test_instance.py
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
test_instance
----------------------------------
Tests for `instance` module.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from towerlib.entities import (EntityManager,
                               Instance)
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


class TestInstanceMutabilityAndEntities(IntegrationTest):

    def setUp(self):
        super(TestInstanceMutabilityAndEntities, self).setUp()
        self.instance = list(self.tower.instances)[0]
        self.instance_group = list(self.tower.instance_groups)[0]

    def test_instance_uuid(self):
        with self.recorder:
            self.assertEquals(self.instance.uuid, '00000000-0000-0000-0000-000000000000')

    def test_instance_hostname(self):
        with self.recorder:
            self.assertEquals(self.instance.hostname, 'awx')

    def test_instance_version(self):
        with self.recorder:
            self.assertEquals(self.instance.version, '6.1.0.0')

    def test_instance_capacity(self):
        with self.recorder:
            self.assertEquals(self.instance.capacity, 8)

    def test_instance_jobs(self):
        with self.recorder:
            self.assertIsInstance(self.instance.jobs, EntityManager)

    def test_instance_group_name(self):
        with self.recorder:
            self.assertEquals(self.instance_group.name, 'tower')

    def test_instance_group_capacity(self):
        with self.recorder:
            self.assertEquals(self.instance_group.capacity, 8)

    def test_instance_group_instances_count(self):
        with self.recorder:
            self.assertEquals(self.instance_group.instances_count, 1)

    def test_instance_group_instances(self):
        with self.recorder:
            self.assertIsInstance(self.instance_group.instances, Instance)

    def test_instance_group_controller(self):
        with self.recorder:
            self.assertIsNone(self.instance_group.controller)
