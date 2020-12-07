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
Main code for inventory.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import logging

from towerlib.towerlibexceptions import (InvalidVariables,
                                         InvalidHost,
                                         InvalidGroup,
                                         InvalidValue,
                                         InvalidOrganization,
                                         InvalidCredential,
                                         InvalidProject)
from .core import (Entity,
                   EntityManager,
                   validate_max_length,
                   validate_json)
from .group import Group
from .host import Host
from .inventory_source import InventorySource

__author__ = '''Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''2018-01-03'''
__copyright__ = '''Copyright 2018, Costas Tyfoxylos'''
__credits__ = ["Costas Tyfoxylos"]
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<ctyfoxylos@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

# This is the main prefix used for logging.
LOGGER_BASENAME = '''intentory'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class Inventory(Entity):  # pylint: disable=too-many-public-methods
    """Models the inventory entity of ansible tower."""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def created_by(self):
        """The user that created the inventory.

        Returns:
            User: The user that created the inventory.

        """
        url = self._data.get('related', {}).get('created_by')
        return self._tower._get_object_by_url('User', url)  # pylint: disable=protected-access

    @property
    def object_roles(self):
        """The object roles.

        Returns:
            EntityManager: EntityManager of the object roles supported.

        """
        url = self._data.get('related', {}).get('object_roles')
        return EntityManager(self._tower,
                             entity_object='ObjectRole',
                             primary_match_field='name',
                             url=url)

    @property
    def object_role_names(self):
        """The names of the object roles.

        Returns:
            list: A list of strings for the object_roles.

        """
        return [object_role.name for object_role in self.object_roles]

    @property
    def name(self):
        """The name of the inventory.

        Returns:
            string: The name of the inventory.

        """
        return self._data.get('name')

    @name.setter
    def name(self, value):
        """Update the name of the user.

        Returns:
            None:

        """
        max_characters = 512
        conditions = [validate_max_length(value, max_characters)]
        if all(conditions):
            self._update_values('name', value)
        else:
            raise InvalidValue(f'{value} is invalid. Condition max_characters must be less or equal to '
                               f'{max_characters}.')

    @property
    def description(self):
        """The description of the inventory.

        Returns:
            string: The description of the inventory.

        """
        return self._data.get('description')

    @description.setter
    def description(self, value):
        """Update the description of the user.

        Returns:
            None:

        """
        self._update_values('description', value)

    @property
    def organization(self):
        """The organization the inventory is part of.

        Returns:
            Organization: The organization the inventory is part of.

        """
        return self._tower.get_organization_by_id(self._data.get('organization'))

    @organization.setter
    def organization(self, value):
        """Update the organization of the inventory.

        Returns:
            None:

        """
        organization = self._tower.get_organization_by_name(value)
        if not organization:
            raise InvalidOrganization(value)
        self._update_values('organization', organization.id)

    @property
    def kind(self):
        """The kind of inventory.

        Returns:
            string: The kind of inventory.

        """
        return self._data.get('kind')

    @property
    def host_filter(self):
        """Not sure what this does.

        Returns:
            string :The host filter.

        """
        return self._data.get('host_filter')

    @property
    def variables(self):
        """The variables set on the inventory.

        Returns:
            string: A string of the variables set on the inventory usually in yaml format.

        """
        return self._data.get('variables')

    @variables.setter
    def variables(self, value):
        """Update the variables of the team.

        Returns:
            None:

        """
        if validate_json(value):
            self._update_values('variables', value)
        else:
            raise InvalidValue(f'Value is not valid json received: {value}')

    @property
    def has_active_failures(self):
        """A flag on whether the inventory has active failures.

        Returns:
            bool: True if there are active failures, False if not.

        """
        return self._data.get('has_active_failures')

    @property
    def has_inventory_sources(self):
        """A flag of whether there are.

        Returns:
            bool: True if set, False otherwise.

        """
        return self._data.get('has_inventory_sources')

    @property
    def total_inventory_sources_count(self):
        """The number of sources.

        Returns:
            integer: The number of sources.

        """
        return self._data.get('total_inventory_sources')

    @property
    def inventory_sources_with_failures_count(self):
        """The number of sources with failures.

        Returns:
            integer: The number of sources with failures.

        """
        return self._data.get('inventory_sources_with_failures')

    @property
    def insights_credential(self):
        """Not sure what this is.

        Returns:
            None.

        """
        return self._data.get('insights_credential')

    @property
    def pending_deletion(self):
        """Whether the invertory is pending deletion.

        Returns:
            bool: True if it is, False otherwise.

        """
        return self._data.get('pending_deletion')

    @property
    def hosts(self):
        """The hosts of the inventory.

        Returns:
            list of Host: The hosts of the inventory.

        """
        return self._tower.hosts.filter({'inventory': self.id})

    @property
    def total_hosts_count(self):
        """The total number of hosts in the inventory.

        Returns:
            integer: The number of inventory hosts.

        """
        return self._data.get('total_hosts')

    @property
    def hosts_with_active_failures_count(self):
        """The number of hosts with active failures.

        Returns:
            integer: The number of hosts with active failures.

        """
        return self._data.get('hosts_with_active_failures')

    def get_host_by_name(self, name):
        """Retrieves a host.

        Args:
            name: The name of the host to retrieve.

        Returns:
            host (Host): returns a host if found else None.

        Raises:
            InvalidHost: The host provided as argument does not exist.

        """
        return next(self._tower.hosts.filter({'inventory': self.id, 'name__iexact': name}), None)

    def create_host(self, name, description, variables='{}'):
        """Creates a host.

        Args:
            name: The name of the host to create.
            description: The description of the host.
            variables: A json with the variables that will be set on the created host.

        Returns:
            Host: The created host is successful, None otherwise.

        Raises:
            InvalidVariables: The variables provided as argument is not valid json.

        """
        if not validate_json(variables):
            raise InvalidVariables(variables)
        url = f'{self._tower.api}/hosts/'
        payload = {'name': name,
                   'description': description,
                   'inventory': self.id,
                   'enabled': True,
                   'instance_id': '',
                   'variables': variables}
        response = self._tower.session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Error creating host "%s", response was "%s"', name, response.text)
        return Host(self._tower, response.json()) if response.ok else None

    def delete_host(self, name):
        """Deletes the host.

        Args:
            name: The name of the host to delete.

        Returns:
            bool: True on success, False otherwise.

        Raises:
            InvalidHost: The host provided as argument does not exist.

        """
        host = next(self._tower.hosts.filter({'inventory': self.id, 'name__iexact': name}), None)
        if not host:
            raise InvalidHost(name)
        return host.delete()

    @property
    def groups(self):
        """The groups of the inventory.

        Returns:
            list of Group: The groups of the inventory.

        """
        return self._tower.groups.filter({'inventory': self.id})

    @property
    def total_groups_count(self):
        """The number of groups.

        Returns:
            integer: The number of groups.

        """
        return self._data.get('total_groups')

    @property
    def groups_with_active_failures_count(self):
        """The number of groups with active failures.

        Returns:
            integer: The number of groups with active failures.

        """
        return self._data.get('groups_with_active_failures')

    def get_group_by_name(self, name):
        """Retrieves the group.

        Args:
            name: The name of the group to retrieve.

        Returns:
            group (Group): returns a group if found else None.

        Raises:
            InvalidGroup: The group provided as argument does not exist.

        """
        return next(self._tower.groups.filter({'inventory': self.id, 'name__iexact': name}), None)

    def create_group(self, name, description, variables='{}'):
        """Creates a group.

        Args:
            name: The name of the group to create.
            description: The description of the group.
            variables: A json with the variables that will be set on the created group.

        Returns:
            Group: The created group is successful, None otherwise.

        Raises:
            InvalidVariables: The variables provided as argument is not valid json.

        """
        if not validate_json(variables):
            raise InvalidVariables(variables)
        url = f'{self._tower.api}/groups/'
        payload = {'name': name,
                   'description': description,
                   'inventory': self.id,
                   'variables': variables}
        response = self._tower.session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Error creating group "%s", response was "%s"', name, response.text)
        return Group(self._tower, response.json()) if response.ok else None

    def delete_group(self, name):
        """Deletes the group.

        Args:
            name: The name of the group to delete.

        Returns:
            bool: True on success, False otherwise.

        Raises:
            InvalidGroup: The group provided as argument does not exist.

        """
        group = next(self._tower.groups.filter({'inventory': self.id, 'name__iexact': name}), None)
        if not group:
            raise InvalidGroup(name)
        return group.delete()

    @property
    def sources(self):
        """The inventory_sources of the inventory.

        Returns:
            list of Host: The inventory_sources of the inventory.

        """
        return self._tower.inventory_sources.filter({'inventory': self.id})

    def create_source(self,  # pylint: disable=too-many-locals, too-many-arguments
                      name,
                      description,
                      source='scm',
                      source_path='',
                      source_script=None,
                      source_vars='',
                      credential='',
                      credential_type='',
                      source_regions='',
                      instance_filters='',
                      group_by='',
                      overwrite=True,
                      overwrite_vars=True,
                      timeout=0,
                      verbosity=1,
                      update_on_launch=True,
                      update_cache_timeout=0,
                      source_project='',
                      update_on_project_update=False):
        """Creates a source.

        Args:
            name ():
            description ():
            source ():
            source_path ():
            source_script ():
            source_vars ():
            credential ():
            credential_type ():
            source_regions ():
            instance_filters ():
            group_by ():
            overwrite ():
            overwrite_vars ():
            timeout ():
            verbosity ():
            update_on_launch ():
            update_cache_timeout ():
            source_project ():
            update_on_project_update ():

        Returns:
            bool

        """
        credential_ = self.organization.get_credential_by_name(credential, credential_type)
        if not credential_:
            raise InvalidCredential(credential)
        project = self.organization.get_project_by_name(source_project)
        if not project:
            raise InvalidProject(source_project)
        url = f'{self._tower.api}/inventory_sources/'
        payload = {'name': name,
                   'description': description,
                   'source': source,
                   'source_path': source_path,
                   'source_script': source_script,
                   'source_vars': source_vars,
                   'credential': credential_.id,
                   'source_regions': source_regions,
                   'instance_filters': instance_filters,
                   'group_by': group_by,
                   'overwrite': overwrite,
                   'overwrite_vars': overwrite_vars,
                   'timeout': timeout,
                   'verbosity': verbosity,
                   'inventory': self.id,
                   'update_on_launch': update_on_launch,
                   'update_cache_timeout': update_cache_timeout,
                   'source_project': project.id,
                   'update_on_project_update': update_on_project_update}
        response = self._tower.session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Error creating source "%s", response was "%s"', name, response.text)
        return InventorySource(self._tower, response.json()) if response.ok else None

    def create_source_with_credential_id(self,  # pylint: disable=too-many-locals, too-many-arguments
                                         name,
                                         description,
                                         credential_id,
                                         source='scm',
                                         source_path='',
                                         source_script=None,
                                         source_vars='',
                                         source_regions='',
                                         instance_filters='',
                                         group_by='',
                                         overwrite=True,
                                         overwrite_vars=True,
                                         timeout=0,
                                         verbosity=1,
                                         update_on_launch=True,
                                         update_cache_timeout=0,
                                         source_project='',
                                         update_on_project_update=False):
        """Creates Source with credential id.

        Args:
            name ():
            description ():
            credential_id ():
            source ():
            source_path ():
            source_script ():
            source_vars ():
            source_regions ():
            instance_filters ():
            group_by ():
            overwrite ():
            overwrite_vars ():
            timeout ():
            verbosity ():
            update_on_launch ():
            update_cache_timeout ():
            source_project ():
            update_on_project_update ():

        Returns:
            bool

        """
        project = self.organization.get_project_by_name(source_project)
        if not project:
            raise InvalidProject(source_project)
        url = f'{self._tower.api}/inventory_sources/'
        payload = {'name': name,
                   'description': description,
                   'source': source,
                   'source_path': source_path,
                   'source_script': source_script,
                   'source_vars': source_vars,
                   'credential': credential_id,
                   'source_regions': source_regions,
                   'instance_filters': instance_filters,
                   'group_by': group_by,
                   'overwrite': overwrite,
                   'overwrite_vars': overwrite_vars,
                   'timeout': timeout,
                   'verbosity': verbosity,
                   'inventory': self.id,
                   'update_on_launch': update_on_launch,
                   'update_cache_timeout': update_cache_timeout,
                   'source_project': project.id,
                   'update_on_project_update': update_on_project_update}
        response = self._tower.session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Error creating source "%s", response was "%s"', name, response.text)
        return InventorySource(self._tower, response.json()) if response.ok else None
