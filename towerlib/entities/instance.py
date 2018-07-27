#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: instances.py
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
Main code for instances

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""


import logging

from .core import Entity, EntityManager

__author__ = '''Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''2018-01-03'''
__copyright__ = '''Copyright 2018, Costas Tyfoxylos'''
__credits__ = ["Costas Tyfoxylos"]
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<ctyfoxylos@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

# This is the main prefix used for logging
LOGGER_BASENAME = '''instances'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class Instance(Entity):
    """Models the instance entity of ansible tower"""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def uuid(self):
        """The uuid of the instance

        Returns:
            string: The uuid of the instance

        """
        return self._data.get('uuid')

    @property
    def hostname(self):
        """The hostname of the instance

        Returns:
            string: The hostname of the instance

        """
        return self._data.get('hostname')

    @property
    def version(self):
        """The version of the instance

        Returns:
            string: The version of the instance

        """
        return self._data.get('version')

    @property
    def capacity(self):
        """Not really sure what this is

        Returns:
            integer:

        """
        return self._data.get('capacity')

    @property
    def consumed_capacity(self):
        """Not really sure what this is

        Returns:
            integer:

        """
        return self._data.get('consumed_capacity')

    @property
    def percent_capacity_remaining(self):
        """Not really sure what this is

        Returns:
            integer:

        """
        return self._data.get('percent_capacity_remaining')

    @property
    def jobs_running_count(self):
        """The number of running jobs

        Returns:
            integer: The number of running jobs

        """
        return self._data.get('jobs_running')

    @property
    def jobs(self):
        """The jobs of the instance

        Returns:
            EntityManager: EntityManager of the jobs of the instance

        """
        url = self._data.get('related', {}).get('jobs')
        return EntityManager(self._tower, entity_object='Job', primary_match_field='name', url=url)


class InstanceGroup(Entity):
    """Models the instance_group entity of ansible tower"""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def name(self):
        """The name of the instance group

        Returns:
            string: The name of the instance group

        """
        return self._data.get('name')

    @property
    def capacity(self):
        """Not really sure what this is

        Returns:
            integer:

        """
        return self._data.get('capacity')

    @property
    def consumed_capacity(self):
        """Not really sure what this is

        Returns:
            integer:

        """
        return self._data.get('consumed_capacity')

    @property
    def percent_capacity_remaining(self):
        """Not really sure what this is

        Returns:
            integer:

        """
        return self._data.get('percent_capacity_remaining')

    @property
    def jobs_running_count(self):
        """The number of running jobs

        Returns:
            integer: The number of running jobs

        """
        return self._data.get('jobs_running')

    @property
    def instances_count(self):
        """The number of instances

        Returns:
            integer: The number of instances

        """
        return self._data.get('instances')

    @property
    def instances(self):
        """The instances of the instance group

        Returns:
            list of Instances: The instances of the instance group

        """
        url = self._data.get('related', {}).get('instances')
        return self._tower._get_object_by_url('Instance', url)  # pylint: disable=protected-access

    @property
    def controller(self):
        """Not really sure what this is

        Returns:
            None

        """
        return self._data.get('controller')
