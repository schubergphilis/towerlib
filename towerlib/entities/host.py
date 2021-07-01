#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: host.py
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
Main code for host.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import logging

from towerlib.towerlibexceptions import InvalidGroup, InvalidValue
from .core import Entity, EntityManager, validate_max_length, validate_json

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
LOGGER_BASENAME = '''host'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class Host(Entity):
    """Models the host entity of ansible tower."""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def name(self):
        """The name of the host.

        Returns:
            string: The name of the host.

        """
        return self._data.get('name')

    @name.setter
    def name(self, value):
        """Update the name of the hosts.

        Returns:
            None:

        """
        max_characters = 512
        conditions = [validate_max_length(value, max_characters)]
        if all(conditions):
            self._update_values('name', value)
        else:
            raise InvalidValue(f'{value} is invalid. Condition max_characters must be less than or equal to '
                               f'{max_characters}')

    @property
    def description(self):
        """The description of the host.

        Returns:
            string: The description of the host.

        """
        return self._data.get('description')

    @description.setter
    def description(self, value):
        """Update the description on the host.

        Returns:
            None:

        """
        self._update_values('description', value)

    @property
    def inventory(self):
        """The inventory that the host is part of.

        Returns:
            Inventory: The inventory that the host is part of.

        """
        return self._tower.get_inventory_by_id(self._data.get('inventory'))

    @property
    def enabled(self):
        """Flag about whether the host is enabled in tower.

        Returns:
            bool: True if the host is enabled, False otherwise.

        """
        return self._data.get('enabled')

    @enabled.setter
    def enabled(self, value):
        """Update the enabled status of the host.

        Returns:
            None:

        """
        self._update_values('enabled', value)

    @property
    def instance_id(self):
        """Not sure what this is.

        Returns:
            string:

        """
        return self._data.get('instance_id')

    @instance_id.setter
    def instance_id(self, value):
        """Update the instance_id of the host.

        Returns:
            None:

        """
        max_characters = 1024
        conditions = [validate_max_length(value, max_characters)]
        if all(conditions):
            self._update_values('instance_id', value)
        else:
            raise InvalidValue(f'{value} is invalid. Condition max_characters must be less than or equal to '
                               f'{max_characters}')

    @property
    def variables(self):
        """The variables set on the host.

        Returns:
            string: A string of the variables set on the host usually in yaml format.

        """
        return self._data.get('variables')

    @variables.setter
    def variables(self, value):
        """Update the variables on the host.

        Returns:
            None:

        """
        conditions = [validate_json(value)]
        if all(conditions):
            self._update_values('variables', value)
        else:
            raise InvalidValue(f'{value} is not valid json.')

    @property
    def has_active_failures(self):
        """Flag about whether the host has active failures.

        Returns:
            bool: True if the host has active failures, False otherwise.

        """
        return self._data.get('has_active_failures')

    @property
    def has_inventory_sources(self):
        """Flag about whether the host has inventory sources.

        Returns:
            bool: True if the host has inventory sources, False otherwise.

        """
        return self._data.get('has_inventory_sources')

    @property
    def last_job(self):
        """The id of the last job.

        Returns:
            integer: The id of the last job.

        """
        return self._data.get('last_job')

    @property
    def last_job_host_summary(self):
        """The id of the last job summary.

        Returns:
            integer: The id of the last job summary..

        """
        return self._data.get('last_job_host_summary')

    @property
    def insights_system_id(self):
        """Not sure what this is.

        Returns:
            None.

        """
        return self._data.get('insights_system_id')

    @property
    def created_by(self):
        """The user that created the host.

        Returns:
            User: The user that created the host.

        """
        url = self._data.get('related', {}).get('created_by')
        return self._tower._get_object_by_url('User', url)  # pylint: disable=protected-access

    @property
    def modified_by(self):
        """The person that modified the host last.

        Returns:
            User: The user that modified the host in tower last.

        """
        url = self._data.get('related', {}).get('modified_by')
        return self._tower._get_object_by_url('User', url)  # pylint: disable=protected-access

    @property
    def groups(self):
        """The groups that the host is part of.

        Returns:
            EntityManager: EntityManager of the groups of the host.

        """
        url = self._data.get('related', {}).get('groups')
        return EntityManager(self._tower,
                             entity_object='Group',
                             primary_match_field='name',
                             url=url)

    @property
    def all_groups(self):
        """The groups that the host is directly and indirectly part of.

        Returns:
            EntityManager: EntityManager of the groups of the host.

        """
        url = self._data.get('related', {}).get('all_groups')
        return EntityManager(self._tower,
                             entity_object='Group',
                             primary_match_field='name',
                             url=url)

    @property
    def recent_jobs(self):
        """The most recent jobs run on the host.

        Returns:
            list if dict: The most recent jobs run on the host.

        """
        return self._data.get('summary_fields', {}).get('recent_jobs')

    @property
    def ansible_facts(self):
        """Returns ansible facts gathered about the host in json.

        Args: None

        Returns:
            json: Json representation of ansible facts

        Raises: None

        """
        url = f'{self._tower.api}/hosts/{self.id}/ansible_facts'
        response = self._tower.session.get(url)
        if not response.ok:
            self._logger.error('Error finding ansible facts for %s.', self._data.get('name'))
        return response.json() if response.ok else '{}'

    def associate_with_groups(self, groups):
        """Associate the host with the provided groups.

        Args:
            groups: The groups to associate the host with.
            Accepts a single group string or a list or tuple of groups.

        Returns:
            bool: True on complete success, False otherwise.

        Raises:
            InvalidGroup: The group provided as argument does not exist.

        """
        if not isinstance(groups, (list, tuple)):
            groups = [groups]
        lower_inventory_group_names = [
            group.name.lower() for group in self.inventory.groups]
        missing_groups = [group_name for group_name in groups
                          if group_name.lower() not in lower_inventory_group_names]
        if missing_groups:
            raise InvalidGroup(missing_groups)
        lower_group_names = [name.lower() for name in groups]
        final_groups = [group for group in self.inventory.groups
                        if group.name.lower() in lower_group_names]
        return all([group._add_host_by_id(self.id)  # pylint: disable=protected-access
                    for group in final_groups])

    def disassociate_with_groups(self, groups):
        """Disassociate the host from the provided groups.

        Args:
            groups: The group name(s) to disassociate the host from.
            Accepts a single group string or a list or tuple of groups.

        Returns:
            bool: True on complete success, False otherwise.

        Raises:
            InvalidGroup: The group provided as argument does not exist.

        """
        if not isinstance(groups, (list, tuple)):
            groups = [groups]
        missing_groups = [group_name for group_name in groups
                          if group_name not in self.groups]
        if missing_groups:
            raise InvalidGroup(missing_groups)
        lower_group_names = [name.lower() for name in groups]
        inventory_groups = [group for group in self.inventory.groups
                            if group.name.lower() in lower_group_names]
        return all([group._remove_host_by_id(self.id)  # pylint: disable=protected-access
                    for group in inventory_groups])

    @property
    def job_events(self):
        """The job_events for the host.

        Returns:
            job_events (list): All job events of the host

        """
        return self._tower.job_events.filter({'host': self.id})
