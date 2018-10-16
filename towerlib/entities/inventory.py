#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: intentory.py
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
Main code for intentory

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import json
import logging

from dateutil.parser import parse

from towerlib.towerlibexceptions import InvalidVariables, InvalidHost, InvalidGroup
from .host import Host
from .group import Group
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
LOGGER_BASENAME = '''intentory'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class Inventory(Entity):  # pylint: disable=too-many-public-methods
    """Models the inventory entity of ansible tower"""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def created_by(self):
        """The user that created the inventory

        Returns:
            User: The user that created the inventory

        """
        url = self._data.get('related', {}).get('created_by')
        return self._tower._get_object_by_url('User', url)  # pylint: disable=protected-access

    @property
    def object_roles(self):
        """The object roles

        Returns:
            EntityManager: EntityManager of the object roles supported

        """
        url = self._data.get('related', {}).get('object_roles')
        return EntityManager(self._tower, entity_object='ObjectRole', primary_match_field='name', url=url)

    @property
    def object_role_names(self):
        """The names of the object roles

        Returns:
            list: A list of strings for the object_roles

        """
        return [object_role.name for object_role in self.object_roles]

    @property
    def name(self):
        """The name of the inventory

        Returns:
            string: The name of the inventory

        """
        return self._data.get('name')

    @property
    def description(self):
        """The description of the inventory

        Returns:
            string: The description of the inventory

        """
        return self._data.get('description')

    @property
    def organization(self):
        """The organization the inventory is part of

        Returns:
            Organization: The organization the inventory is part of

        """
        return self._tower.get_organization_by_id(self._data.get('organization'))

    @property
    def kind(self):
        """The kind of inventory

        Returns:
            string: The kind of inventory

        """
        return self._data.get('kind')

    @property
    def host_filter(self):
        """Not sure what this does

        Returns:
            None

        """
        return self._data.get('host_filter')

    @property
    def variables(self):
        """The variables set on the inventory

        Returns:
            string: A string of the variables set on the inventory usually in yaml format.

        """
        return self._data.get('variables')

    @property
    def has_active_failures(self):
        """A flag on whether the inventory has active failures

        Returns:
            bool: True if there are active failures, False if not

        """
        return self._data.get('has_active_failures')

    @property
    def total_hosts_count(self):
        """The total number of hosts in the inventory

        Returns:
            integer: The number of inventory hosts

        """
        return self._data.get('total_hosts')

    @property
    def hosts_with_active_failures_count(self):
        """The number of hosts with active failures

        Returns:
            integer: The number of hosts with active failures

        """
        return self._data.get('hosts_with_active_failures')

    @property
    def total_groups_count(self):
        """The number of groups

        Returns:
            integer: The number of groups

        """
        return self._data.get('total_groups')

    @property
    def groups_with_active_failures_count(self):
        """The number of groups with active failures

        Returns:
            integer: The number of groups with active failures

        """
        return self._data.get('groups_with_active_failures')

    @property
    def has_inventory_sources(self):
        """A flag of whether there are

        Returns:
            bool: True if set, False otherwise

        """
        return parse(self._data.get('has_inventory_sources'))

    @property
    def total_inventory_sources_count(self):
        """The number of sources

        Returns:
            integer: The number of sources

        """
        return self._data.get('total_inventory_sources')

    @property
    def inventory_sources_with_failures_count(self):
        """The number of sources with failures

        Returns:
            integer: The number of sources with failures

        """
        return self._data.get('inventory_sources_with_failures')

    @property
    def insights_credential(self):
        """Not sure what this is

        Returns:
            None

        """
        return self._data.get('insights_credential')

    @property
    def pending_deletion(self):
        """Whether the invertory is pending deletion

        Returns:
            bool: True if it is, False otherwise

        """
        return self._data.get('pending_deletion')

    @property
    def hosts(self):
        """The hosts of the inventory

        Returns:
            list of Host: The hosts of the inventory

        """
        return self._tower.hosts.filter({'inventory': self.id})

    @property
    def groups(self):
        """The groups of the inventory

        Returns:
            list of Group: The groups of the inventory

        """
        return self._tower.groups.filter({'inventory': self.id})

    def create_group(self, name, description, variables='{}'):
        """Creates a group

        Args:
            name: The name of the group to create
            description: The description of the group
            variables: A json with the variables that will be set on the created group

        Returns:
            Group: The created group is successful, None otherwise

        Raises:
            InvalidVariables: The variables provided as argument is not valid json.

        """
        try:
            _ = json.loads(variables)
            del _
        except ValueError:
            raise InvalidVariables(variables)
        url = '{api}/groups/'.format(api=self._tower.api)
        payload = {'name': name,
                   'description': description,
                   'inventory': self.id,
                   'variables': variables}
        response = self._tower.session.post(url, data=json.dumps(payload))
        return Group(self._tower, response.json()) if response.ok else None

    def delete_group(self, name):
        """Deletes the group

        Args:
            name: The name of the group to delete

        Returns:
            bool: True on success, False otherwise

        Raises:
            InvalidGroup: The group provided as argument does not exist.

        """
        group = self._tower.get_group_by_name(name)
        if not group:
            raise InvalidGroup(name)
        return group.delete()

    def create_host(self, name, description, variables='{}'):
        """Creates a host

        Args:
            name: The name of the host to create
            description: The description of the host
            variables: A json with the variables that will be set on the created host

        Returns:
            Host: The created host is successful, None otherwise

        Raises:
            InvalidVariables: The variables provided as argument is not valid json.

        """
        try:
            _ = json.loads(variables)
            del _
        except ValueError:
            raise InvalidVariables(variables)
        url = '{api}/hosts/'.format(api=self._tower.api)
        payload = {'name': name,
                   'description': description,
                   'inventory': self.id,
                   'enabled': True,
                   'instance_id': '',
                   'variables': variables}
        response = self._tower.session.post(url, data=json.dumps(payload))
        return Host(self._tower, response.json()) if response.ok else None

    def delete_host(self, name):
        """Deletes the host

        Args:
            name: The name of the host to delete

        Returns:
            bool: True on success, False otherwise

        Raises:
            InvalidHost: The host provided as argument does not exist.

        """
        host = self._tower.get_host_by_name(name)
        if not host:
            raise InvalidHost(name)
        return host.delete()
