#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: misc.py
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
Main code for miscellaneous

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import logging
from collections import namedtuple

from dateutil.parser import parse
from cachetools import TTLCache, cached

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
LOGGER_BASENAME = '''misc'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

USER_LEVELS = (u'standard', u'system_auditor', u'system_administrator')
CERTIFICATE_TYPE_KINDS = (u'scm', u'ssh', u'vault', u'net', u'cloud', u'insights')
JOB_TYPES = (u'run', u'check')
VERBOSITY_LEVELS = (0, 1, 2, 3, 4)

Config = namedtuple('Config', ['eula',
                               'license_info',
                               'analytics_status',
                               'version',
                               'project_base_dir',
                               'time_zone',
                               'ansible_version',
                               'project_local_paths'])

LicenseInfo = namedtuple('LicenseInfo', ['subscription_name',
                                         'valid_key',
                                         'features',
                                         'date_expired',
                                         'available_instances',
                                         'hostname',
                                         'free_instances',
                                         'instance_count',
                                         'time_remaining',
                                         'compliant',
                                         'grace_period_remaining',
                                         'trial',
                                         'company_name',
                                         'date_warning',
                                         'license_type',
                                         'license_key',
                                         'license_date',
                                         'deployment_id',
                                         'current_instances'])

LicenseFeatures = namedtuple('LicenseFeatures', ['surveys',
                                                 'multiple_organizations',
                                                 'workflows',
                                                 'system_tracking',
                                                 'enterprise_auth',
                                                 'rebranding',
                                                 'activity_streams',
                                                 'ldap',
                                                 'ha'])

Cluster = namedtuple('InstanceGroups', ['instances',
                                        'capacity',
                                        'name',
                                        'ha_enabled',
                                        'version',
                                        'active_node'])
INSTANCE_STATE_CACHING_SECONDS = 60
INSTANCE_STATE_CACHE = TTLCache(maxsize=1, ttl=INSTANCE_STATE_CACHING_SECONDS)


class ClusterInstance(object):
    """Models the instance of a node as part of the cluster"""

    def __init__(self, tower_instance, name, hearbeat):
        self._tower = tower_instance
        self.name = name
        self._heartbeat = hearbeat
        self._instance_data = self._get_instance_data()

    @cached(INSTANCE_STATE_CACHE)
    def _get_instance_data(self):
        url = '{api}/instances/'.format(api=self._tower.api)
        results = self._tower.session.get(url)
        result_json = results.json()
        return next((instance for instance in result_json.get('results', [])
                     if instance.get('hostname') == self.name), {})

    @property
    def heartbeat(self):
        """Datetime object of when the last heartbeat was recorded"""
        try:
            date_ = parse(self._heartbeat)
        except (ValueError, TypeError):
            date_ = None
        return date_

    @property
    def id(self):  # pylint: disable=invalid-name
        """The id of the node"""
        return self._instance_data.get('id')

    @property
    def uuid(self):
        """The uuid of the node"""
        return self._instance_data.get('uuid')

    @property
    def hostname(self):
        """The hostname of the node"""
        return self._instance_data.get('hostname')

    @property
    def version(self):
        """The version of tower on the node"""
        return self._instance_data.get('version')

    @property
    def capacity(self):
        """The capacity of the node"""
        return self._instance_data.get('capacity')

    @property
    def consumed_capacity(self):
        """The consumed capacity"""
        return self._instance_data.get('consumed_capacity')

    @property
    def percent_capacity_remaining(self):
        """The percentage of remaining capacity"""
        return self._instance_data.get('percent_capacity_remaining')

    @property
    def jobs_running(self):
        """The number of running jobs"""
        return self._instance_data.get('jobs_running')

    @property
    def created_at(self):
        """The date and time the entity was created in tower

        Returns:
            datetime: The datetime object of the date and time of the creation of the object
            None: If there is no entry for the creation

        """
        try:
            date_ = parse(self._instance_data.get('created'))
        except (ValueError, TypeError):
            date_ = None
        return date_

    @property
    def modified_at(self):
        """The date and time the entity was modified in tower

        Returns:
            datetime: The datetime object of the date and time of the modification of the object
            None: If there is no entry for the modification

        """
        try:
            date_ = parse(self._instance_data.get('modified'))
        except (ValueError, TypeError):
            date_ = None
        return date_


class Entity(object):
    """The basic object that holds common responses across all entities"""

    def __init__(self, tower_instance, data):
        logger_name = u'{base}.{suffix}'.format(base=LOGGER_BASENAME,
                                                suffix=self.__class__.__name__)
        self._logger = logging.getLogger(logger_name)
        self._tower = tower_instance
        self._data = data

    @property
    def id(self):  # pylint: disable=invalid-name
        """The id of the object

        Returns:
            int: The number of the internal id of the object in tower

        """
        return self._data.get('id')

    @property
    def type(self):
        """The type of the object

        Returns:
            string: The name of the type of the object in tower

        """
        return self._data.get('type')

    @property
    def url(self):
        """The url of the object

        Returns:
            string: The full url of the representation of the object in tower

        """
        return self._tower.host + self._data.get('url')

    @property
    def created_at(self):
        """The date and time the entity was created in tower

        Returns:
            datetime: The datetime object of the date and time of the creation of the object
            None: If there is no entry for the creation

        """
        try:
            date_ = parse(self._data.get('created'))
        except (ValueError, TypeError):
            date_ = None
        return date_

    @property
    def modified_at(self):
        """The date and time the entity was modified in tower

        Returns:
            datetime: The datetime object of the date and time of the modification of the object
            None: If there is no entry for the modification

        """
        try:
            date_ = parse(self._data.get('modified'))
        except (ValueError, TypeError):
            date_ = None
        return date_

    def delete(self):
        """Deletes the entity from tower

        Returns:
            bool: True on success, False otherwise

        """
        response = self._tower.session.delete(self.url)
        return response.ok


class EntityManager(object):
    """Manages entities by making them act like iterables but also implements contains and other useful stuff."""

    def __init__(self, tower_instance, entity_object, primary_match_field, entity_name=None, url=None):  # pylint: disable=too-many-arguments
        if not any([entity_name, url]):
            raise ValueError('Either entity_name or url needs to be provided, received none.')
        self._tower = tower_instance
        self._object_type = entity_object
        self._primary_match_field = primary_match_field
        self._name = entity_name
        self._next_state = None
        if entity_name:
            self._url = '{api}/{entity_name}'.format(api=self._tower.api, entity_name=entity_name)
        else:
            self._url = '{host}{url}'.format(host=self._tower.host, url=url)

    @property
    def _objects(self):
        return self._get_entity_objects()

    def _get_entity_objects(self, params=None):
        module = __import__('towerlib.entities')
        entity_object = getattr(module, self._object_type)
        for data in self._tower._get_paginated_response(self._url, params=params):  # pylint: disable=protected-access
            yield entity_object(self._tower, data)

    def __iter__(self):
        return self._objects

    def __contains__(self, value):
        return next(self.filter({self._primary_match_field: value}), False)

    def filter(self, params):
        """Implements filtering based on the filtering capabilities of tower

        Args:
            params: Dictionary of filters to be passed to the api

        Returns:
              Generator of the objects retrieved based on the filtering
        https://docs.ansible.com/ansible-tower/latest/html/towerapi/filtering.html

        """
        return self._get_entity_objects(params)
