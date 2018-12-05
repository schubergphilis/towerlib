#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: group.py
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
Main code for group

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import json
import logging

from towerlib.towerlibexceptions import InvalidHost, InvalidGroup
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
LOGGER_BASENAME = '''group'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class Group(Entity):
    """Models the group entity of ansible tower"""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def name(self):
        """The name of the group

        Returns:
            string: The name of the group

        """
        return self._data.get('name')

    @property
    def description(self):
        """The description of the group

        Returns:
            string: The description of the group

        """
        return self._data.get('description')

    @property
    def inventory(self):
        """The inventory that the group is part of

        Returns:
            Inventory: The inventory that the group is part of

        """
        return self._tower.get_inventory_by_id(self._data.get('inventory'))

    @property
    def variables(self):
        """The variables set on the group

        Returns:
            string: A string of the variables set on the group usually in yaml format.

        """
        return self._data.get('variables')

    @property
    def has_active_failures(self):
        """A flag on whether the group has active failures

        Returns:
            bool: True if there are active failures, False if not

        """
        return self._data.get('has_active_failures')

    @property
    def total_hosts_count(self):
        """The total number of hosts in the group

        Returns:
            integer: The number of group hosts

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
        return self._data.get('has_inventory_sources')

    @property
    def created_by(self):
        """The user that created the group

        Returns:
            User: The user that created the group

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

    def _add_host_by_id(self, id_):
        payload = {'id': id_}
        return self._post_host(payload)

    def _remove_host_by_id(self, id_):
        payload = {'id': id_,
                   'disassociate': 1}
        return self._post_host(payload)

    def _post_host(self, payload):
        url = '{api}/groups/{id}/hosts/'.format(api=self._tower.api, id=self.id)
        response = self._tower.session.post(url, data=json.dumps(payload))
        return response.ok

    def _associate_group_by_id(self, id_):
        payload = {'id': id_}
        return self._post_group(payload)

    def _disassociate_group_by_id(self, id_):
        payload = {'id': id_,
                   'disassociate': 1}
        return self._post_group(payload)

    def _post_group(self, payload):
        url = '{api}/groups/{id}/children/'.format(api=self._tower.api, id=self.id)
        response = self._tower.session.post(url, data=json.dumps(payload))
        return response.ok

    def add_host_by_name(self, name):
        """Add a host to the group by name

        Args:
            name: The name of the host to add to the group

        Returns:
            bool: True on success, False otherwise

        Raises:
            InvalidHost: The host provided as argument does not exist.

        """
        host = self._tower.get_host_by_name(name)
        if not host:
            raise InvalidHost(name)
        return self._add_host_by_id(host.id)

    def remove_host_by_name(self, name):
        """Removes a host from the group

        Args:
            name: The name of the host to remove

        Returns:
            bool: True on success, False otherwise

        Raises:
            InvalidHost: The host provided as argument does not exist.

        """
        host = self._tower.get_host_by_name(name)
        if not host:
            raise InvalidHost(name)
        return self._remove_host_by_id(host.id)

    def associate_group_by_name(self, name):
        """Associate a group to the group by name

        Args:
            name: The name of the group to associate with the group

        Returns:
            bool: True on success, False otherwise

        Raises:
            InvalidGroup: The group provided as argument does not exist.

        """
        group = self._tower.get_group_by_name(name)
        if not group:
            raise InvalidGroup(name)
        return self._associate_group_by_id(group.id)

    def disassociate_group_by_name(self, name):
        """Disassociate a group from the group

        Args:
            name: The name of the group to disassociate

        Returns:
            bool: True on success, False otherwise

        Raises:
            InvalidGroup: The group provided as argument does not exist.

        """
        group = self._tower.get_group_by_name(name)
        if not group:
            raise InvalidGroup(name)
        return self._disassociate_group_by_id(group.id)

    @property
    def hosts(self):
        """The hosts of the group

        Returns:
            EntityManager: EntityManager of the hosts of the group

        """
        url = self._data.get('related', {}).get('hosts')
        return EntityManager(self._tower, entity_object='Host', primary_match_field='name', url=url)

    @property
    def groups(self):
        """The associated groups of the group

        Returns:
            EntityManager: EntityManager of the groups of the group

        """
        url = self._data.get('related', {}).get('children')
        return EntityManager(self._tower, entity_object='Group', primary_match_field='name', url=url)
