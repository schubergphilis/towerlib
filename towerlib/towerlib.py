#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: towerlib.py
#
# Copyright 2018 Costas Tyfoxylos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the 'Software'), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#
# pylint: disable=too-many-lines
"""
Main code for towerlib.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import concurrent.futures
import json
import logging
import math
import sys

from cachetools import TTLCache, cached
from requests import Session

from towerlib.entities.core import validate_json
from .entities import (Config,
                       LicenseInfo,
                       LicenseFeatures,
                       Organization,
                       User,
                       CredentialType,
                       Credential,
                       JobTemplate,
                       VALID_CREDENTIAL_TYPES,
                       JOB_TYPES,
                       VERBOSITY_LEVELS,
                       Cluster,
                       ClusterInstance,
                       EntityManager,
                       Settings)
from .towerlibexceptions import (AuthFailed,
                                 InvalidOrganization,
                                 InvalidInventory,
                                 InvalidVariables,
                                 InvalidUser,
                                 InvalidTeam,
                                 InvalidCredential,
                                 InvalidHost,
                                 InvalidProject,
                                 InvalidGroup,
                                 InvalidCredentialType,
                                 InvalidPlaybook,
                                 InvalidInstanceGroup,
                                 InvalidJobType,
                                 InvalidVerbosity,
                                 InvalidJobTemplate,
                                 InvalidInventoryScript,
                                 FailedToDeleteTemplate)

__author__ = '''Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''2018-01-02'''
__copyright__ = '''Copyright 2018, Costas Tyfoxylos'''
__credits__ = ['Costas Tyfoxylos']
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<ctyfoxylos@schubergphilis.com>'''
__status__ = '''Development'''  # 'Prototype', 'Development', 'Production'.

# This is the main prefix used for logging
LOGGER_BASENAME = 'towerlib'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

PAGINATION_LIMIT = 25
CLUSTER_STATE_CACHING_SECONDS = 10
CONFIGURATION_STATE_CACHING_SECONDS = 60
CLUSTER_STATE_CACHE = TTLCache(maxsize=1, ttl=CLUSTER_STATE_CACHING_SECONDS)
CONFIGURATION_STATE_CACHE = TTLCache(maxsize=1, ttl=CONFIGURATION_STATE_CACHING_SECONDS)
GENERIC_SEARCH_ITEMS = ['credentials', 'groups', 'hosts', 'instances', 'inventories', 'inventory_scripts',
                         'inventory_sources', 'jobs', 'job_templates', 'notifications', 'organizations', 'projects',
                         'project_updates', 'roles', 'schedules', 'teams', 'users']


class Tower:  # pylint: disable=too-many-public-methods
    """Models the api of ansible tower."""

    # pylint: disable=too-many-arguments
    def __init__(self, host, username, password, secure=False, ssl_verify=True, token=None):
        self._logger = logging.getLogger(f'{LOGGER_BASENAME}.{self.__class__.__name__}')
        self.host = self._generate_host_name(host, secure)
        self.api = f'{self.host}/api/v2'
        self.username = username
        self.password = password
        self.token = token
        self.session = self._get_authenticated_session(secure, ssl_verify)

    @staticmethod
    def _generate_host_name(host, secure):
        return f'{"https" if secure else "http"}://{host}'

    def _get_authenticated_session(self, secure, ssl_verify):
        session = Session()
        if secure:
            session.verify = ssl_verify
        return self._authenticate(session, self.host, self.username, self.password, self.api, self.token)

    @staticmethod
    def _authenticate(session, host, username, password, api_url, token):
        session.get(host)
        session.headers.update({'content-type': 'application/json'})
        url = f'{api_url}/me/'
        if token:
            session.headers.update({"Authorization": "Bearer " + str(token)})
        else:
            session.auth = (username, password)
        response = session.get(url)
        if response.status_code == 401:
            raise AuthFailed(response.content)
        return session

    @property
    @cached(CONFIGURATION_STATE_CACHE)
    def configuration(self):
        """The configuration of the tower instance.

        Returns:
            Config: The configuration of the tower instance.

        """
        url = f'{self.api}/config/'
        results = self.session.get(url)
        config = results.json()
        features = [config.get('license_info',
                               {}).get('features',
                                       {}).get(key) for key in LicenseFeatures._fields]  # noqa
        info = [config.get('license_info',
                           {}).get(key) for key in LicenseInfo._fields]  # noqa
        # we overwrite the entry of "features" with the namedtuple of it.
        info[2] = LicenseFeatures(*features)
        configuration = [config.get(key) for key in Config._fields]  # noqa
        # we overwrite the entry of "license_info" with the namedtuple of it.
        configuration[1] = LicenseInfo(*info)
        return Config(*configuration)

    @property
    @cached(CLUSTER_STATE_CACHE)
    def cluster(self):
        """The cluster status of tower.

        Returns:
            Cluster: The information about the state of the cluster.

        """
        def get_instance(name, instance_list):
            """Getting an instance nametuple from an instance list."""
            node = next((instance for instance in instance_list
                         if instance.get('node') == name), None)
            data = [node.get(key_) for key_ in ('node', 'heartbeat')]
            return ClusterInstance(self, *data)

        url = f'{self.api}/ping/'
        results = self.session.get(url)
        ping = results.json()
        instance_groups = ping.get('instance_groups', [])[0]
        instance_list = ping.get('instances')
        capacity = instance_groups.get('capacity', 0)
        name = instance_groups.get('name', 'Unset')
        ha_enabled = ping.get('ha', False)
        version = ping.get('version', 'Unknown')
        instances = [get_instance(name_, instance_list)
                     for name_ in instance_groups.get('instances', [])]
        active_node = get_instance(ping.get('active_node'), instance_list)

        return Cluster(instances, capacity, name, ha_enabled, version, active_node)

    @property
    def organizations(self):
        """The organizations configured in tower.

        Returns:
            EntityManager: The manager object for organizations.

        """
        return EntityManager(self,
                             entity_name='organizations',
                             entity_object='Organization',
                             primary_match_field='name')

    def get_organization_by_name(self, name):
        """Retrieves an organization by name.

        Args:
            name: The name of the organization to retrieve.

        Returns:
            Organization: The organization if a match is found else None.

        """
        return next(self.organizations.filter({'name__iexact': name}), None)

    def get_organization_by_id(self, id_):
        """Retrieves an organization by id.

        Args:
            id_: The id of the organization to retrieve.

        Returns:
            Organization: The organization if a match is found else None.

        """
        return next(self.organizations.filter({'id': id_}), None)

    def create_organization(self, name, description=""):
        """Creates an organization in tower.

        Args:
            name: The name of the organization to create.
            description: The description of the organization to create.

        Returns:
            Organization: The organization on success, None otherwise.

        """
        url = f'{self.api}/organizations/'
        payload = {'name': name,
                   'description': description}
        response = self.session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Error creating organization, response was: "%s"', response.text)
            return None
        else:
            self._logger.info("New organization '{}' was created successfully.".format(payload['name']))
            return Organization(self, response.json())

    def delete_organization(self, name):
        """Deletes an organization from tower.

        Args:
            name: The name of the organization to delete.

        Returns:
            bool: True on success, False otherwise.

        Raises:
            InvalidOrganization: The organization provided as argument does not exist.

        """
        organization = self.get_organization_by_name(name)
        if not organization:
            raise InvalidOrganization(name)
        return organization.delete()

    @staticmethod
    def add_slash(url):
        """Adds a final slash to a url if there is not any."""
        return url + '/' if not url.endswith('/') else url

    def _get_first_page(self, url, params=None):
        parameters = {'page_size': PAGINATION_LIMIT}
        if params:
            parameters.update(params)
        try:
            response = self.session.get(url, params=parameters)
            response_data = response.json()
            response.close()
        except (ValueError, AttributeError, TypeError):
            self._logger.exception('Could not retrieve first page, response was %s', response.text)
            response_data = {}
        return response_data

    def _get_paginated_response(self, url, params=None):
        url = self.add_slash(url)
        response_data = self._get_first_page(url, params)
        count = response_data.get('count', 0)
        page_count = int(math.ceil(float(count) / PAGINATION_LIMIT))
        self._logger.debug('Calculated that there are %s pages to get', page_count)
        for result in response_data.get('results', []):
            yield result
        if page_count:
            with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
                futures = []
                if not params:
                    params = {}
                for index in range(page_count, 1, -1):
                    params.update({'page': index})
                    futures.append(executor.submit(self.session.get, url, params=params.copy()))
                for future in concurrent.futures.as_completed(futures):
                    try:
                        response = future.result()
                        response_data = response.json()
                        response.close()
                        for result in response_data.get('results'):
                            yield result
                    except Exception:  # pylint: disable=broad-except
                        self._logger.exception('Future failed...')

    @property
    def external_users(self):
        """Retrieves only users created by an external system.

        Returns:
            users (Generator): Users created by external system in tower.

        """
        return self.users.filter({'social_auth__isnull': False})

    @property
    def local_users(self):
        """Retrieves only users created locally in tower.

        Returns:
            users (Generator): Users created locally in tower.

        """
        return self.users.filter({'social_auth__isnull': True})

    @property
    def users(self):
        """A manager object for the users in tower.

        Returns:
            EntityManager: The manager object for users.

        """
        return EntityManager(self,
                             entity_name='users',
                             entity_object='User',
                             primary_match_field='username')

    def get_user_by_username(self, name):
        """Retrieves user by name.

        Args:
            name: The name of the user to retrieve.

        Returns:
            user (User): The user if a match is found else None.

        """
        return next(self.users.filter({'username__iexact': name}), None)

    def get_user_by_id(self, id_):
        """Retrieves a user by id.

        Args:
            id_: The id of the user to retrieve.

        Returns:
            User: The user if a match is found else None.

        """
        return next(self.users.filter({'id': id_}), None)

    def create_user(self,  # pylint: disable=too-many-arguments
                    username,
                    password,
                    first_name="",
                    last_name="",
                    email="",
                    is_superuser=False,
                    is_system_auditor=False,
                    ):
        """Creates a user in AWX/Tower.

        Args:
            username: The username to create for the user.
            password: The password to set for the user.
            first_name: The first name of the user.
            last_name: The last name of the user.
            email: The email of the user.
            is_superuser: Is the user a super user
            is_system_auditor: Is the user an auditor

        Returns:
            User: The created User object on success, None otherwise.

        """
        url = f'{self.api}/users/'
        payload = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'is_superuser': is_superuser,
            'is_system_auditor': is_system_auditor}
        response = self.session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Error creating user, response was: "%s"', response.text)
            return None
        else:
            self._logger.info("User '{}' was created successfully.".format(payload['name']))
            return User(self, response.json())

    def delete_user(self, username):
        """Deletes a user by username.

        Args:
            username: The username of the user to delete.

        Returns:
            bool: True on success, False otherwise.

        Raises:
            InvalidUser: The username provided as argument does not exist.

        """
        user = self.get_user_by_username(username)
        if not user:
            raise InvalidUser(username)
        return user.delete()

    def create_user_in_organization(self,  # pylint: disable=too-many-arguments
                                    organization,
                                    username,
                                    password,
                                    first_name,
                                    last_name,
                                    email):
        """Creates a user in an organization.

        Args:
            organization: The name of the organization to create the user under.
            username: The user's username.
            password: The user's password.
            first_name: The user's first name.
            last_name: The user's last name.
            email: The user's email.


        Returns:
            User: The user on success, None otherwise.

        Raises:
            InvalidOrganization: The organization provided as argument does not exist.

        """
        organization_ = self.get_organization_by_name(organization)
        if not organization_:
            raise InvalidOrganization(organization)
        user = self.create_user(username,
                                password,
                                first_name=first_name,
                                last_name=last_name,
                                email=email)
        if not user:
            return False
        user.associate_with_organization_role(organization, Organization.DEFAULT_MEMBER_ROLE)
        return user

    @property
    def projects(self):
        """The projects configured in tower.

        Returns:
            EntityManager: The manager object for projects.

        """
        return EntityManager(self,
                             entity_name='projects',
                             entity_object='Project',
                             primary_match_field='name')

    def get_projects_by_name(self, name):
        """Retrieves projects by name.

        Args:
            name: The name of the projects to retrieve.

        Returns:
            projects (Generator): A generator with the matching projects

        """
        return self.projects.filter({'name__iexact': name})

    def get_organization_project_by_name(self, organization, name):
        """Retrieves a project by name.

        Args:
            organization: The name of the organization the project belongs to.
            name: The name of the project to retrieve.

        Returns:
            Project: The project if a match is found else None.

        """
        organization_ = self.get_organization_by_name(organization)
        if not organization_:
            raise InvalidOrganization(organization)
        return organization_.get_project_by_name(name)

    def get_project_by_id(self, id_):
        """Retrieves a project by id.

        Args:
            id_: The id of the project to retrieve.

        Returns:
            Project: The project if a match is found else None.

        """
        return next(self.projects.filter({'id': id_}), None)

    def create_project_in_organization(self,  # pylint: disable=too-many-arguments
                                       organization,
                                       name,
                                       description,
                                       credential,
                                       scm_url,
                                       local_path='',
                                       custom_virtualenv='',
                                       scm_branch='master',
                                       scm_type='git',
                                       scm_clean=True,
                                       scm_delete_on_update=False,
                                       scm_update_on_launch=True,
                                       scm_update_cache_timeout=0):
        """Creates a project in an organization.

        Args:
            organization (str): The name of the organization to create the project under.
            name (str): The name of the project.
            description (str): The description of the project.
            credential (str): The name of the credential to use for the project.
            scm_url (str): The url of the scm.
            local_path (str): Local path (relative to PROJECTS_ROOT) containing playbooks and files for this project.
            custom_virtualenv (str): Local absolute file path containing a custom Python virtualenv to use.
            scm_branch (str): The default branch of the scm.
            scm_type (str): The type of the scm.
            scm_clean (bool): Clean scm or not.
            scm_delete_on_update (bool): Delete scm on update.
            scm_update_on_launch (bool): Update scm on launch.
            scm_update_cache_timeout (int): Scm cache update.

        Returns:
            Project: The created project on success, None otherwise.

        Raises:
            InvalidOrganization: The organization provided as argument does not exist.

        """
        organization_ = self.get_organization_by_name(organization)
        if not organization_:
            raise InvalidOrganization(organization)
        return organization_.create_project(name,
                                            description,
                                            credential,
                                            scm_url,
                                            local_path,
                                            custom_virtualenv,
                                            scm_branch,
                                            scm_type,
                                            scm_clean,
                                            scm_delete_on_update,
                                            scm_update_on_launch,
                                            scm_update_cache_timeout)

    def delete_organization_project(self, organization, name):
        """Deletes a project from tower.

        Args:
            organization: The organization the project belongs to.
            name: The name of the project to delete.

        Returns:
            bool: True on success, False otherwise.

        Raises:
            InvalidProject: The project provided as argument does not exist.

        """
        organization_ = self.get_organization_by_name(organization)
        if not organization_:
            raise InvalidOrganization(organization_)
        project = organization_.get_project_by_name(name)
        if not project:
            raise InvalidProject(name)
        return project.delete()

    @property
    def teams(self):
        """The teams configured in tower.

        Returns:
            EntityManager: The manager object for teams.

        """
        return EntityManager(self,
                             entity_name='teams',
                             entity_object='Team',
                             primary_match_field='name')

    def get_teams_by_name(self, name):
        """Retrieves teams by name.

        Args:
            name: The name of the teams to retrieve.

        Returns:
            teams (Generator): A generator with the matching teams

        """
        return self.teams.filter({'name__iexact': name})

    def get_organization_team_by_name(self, organization, name):
        """Retrieves a team by name.

        Args:
            organization: The name of the organization the team belongs to.
            name: The name of the team to retrieve.

        Returns:
            Team: The team if a match is found else None.

        Raises:
            InvalidOrganization: The organization provided as argument does not exist.

        """
        organization_ = self.get_organization_by_name(organization)
        if not organization_:
            raise InvalidOrganization(organization)
        return organization_.get_team_by_name(name)

    def get_team_by_id(self, id_):
        """Retrieves a team by id.

        Args:
            id_: The id of the team to retrieve.

        Returns:
            Team: The team if a match is found else None.

        """
        return next(self.teams.filter({'id': id_}), None)

    def create_team_in_organization(self, organization, team_name, description=""):
        """Creates a team under an organization.

        Args:
            organization: The name of the organization to create the team under.
            team_name: The name of the team to create.
            description: The description of the team to create.

        Returns:
            Team: The created team on success, None otherwise.

        Raises:
            InvalidOrganization: The organization provided as argument does not exist.

        """
        organization_ = self.get_organization_by_name(organization)
        if not organization_:
            raise InvalidOrganization(organization)
        return organization_.create_team(team_name, description)

    def delete_team_in_organization(self, organization, name):
        """Deletes a team from tower.

        Args:
            organization: The name of the organization the team belongs to.
            name: The name of the team to delete.

        Returns:
            bool: True on success, False otherwise.

        Raises:
            InvalidTeam: The team provided as argument does not exist.

        """
        team = self.get_organization_team_by_name(organization, name)
        if not team:
            raise InvalidTeam(team)
        return team.delete()

    @property
    def groups(self):
        """The groups configured in tower.

        Returns:
            EntityManager: The manager object for groups.

        """
        return EntityManager(self,
                             entity_name='groups',
                             entity_object='Group',
                             primary_match_field='name')

    def get_inventory_group_by_name(self, organization, inventory, name):
        """Retrieves a group by name.

        Args:
            organization: The name of the organization the inventory belongs to.
            inventory: The inventory to retrieve the group from.
            name: The name of the group to retrieve.

        Returns:
            Group: The group if a match is found else None.

        Raises:
            InvalidOrganization: The organisation provided as an argument does not exist.
            InvalidInventory: The inventory name provided as an argument does not exist.

        """
        organization_ = self.get_organization_by_name(organization)
        if not organization_:
            raise InvalidOrganization(organization_)
        inventory_ = organization_.get_inventory_by_name(inventory)
        if not inventory_:
            raise InvalidInventory(inventory_)
        return inventory_.get_group_by_name(name)

    def get_group_by_id(self, id_):
        """Retrieves a group by id.

        Args:
            id_: The id of the group to retrieve.

        Returns:
            Group: The group if a match is found else None.

        """
        return next(self.groups.filter({'id': id_}), None)

    # pylint: disable=too-many-arguments
    def create_inventory_group(self, organization, inventory, name, description, variables='{}'):
        """Creates a group in an inventory in tower.

        Args:
            organization: The organization the inventory belongs to.
            inventory: The name of the inventory to create the group in.
            name: The name of the group to create.
            description (str): The description of the group to create.
            variables (str): The Variables of the group in a json string format.

        Returns:
            bool: True on success, False otherwise.

        Raises:
            InvalidGroup: The group provided as argument does not exist.

        """
        inventory_ = self.get_organization_inventory_by_name(organization, inventory)
        if not inventory_:
            raise InvalidInventory(inventory)
        return inventory_.create_group(name, description, variables)

    def delete_inventory_group(self, organization, inventory, name):
        """Deletes a group from tower.

        Args:
            organization: The organization the inventory belongs to.
            inventory: The name of the inventory to retrieve the group from.
            name: The name of the group to delete.

        Returns:
            bool: True on success, False otherwise.

        Raises:
            InvalidGroup: The group provided as argument does not exist.

        """
        group = self.get_inventory_group_by_name(organization, inventory, name)
        if not group:
            raise InvalidGroup(name)
        return group.delete()

    @property
    def inventories(self):
        """The inventories configured in tower.

        Returns:
            list of Inventory: The inventories configured in tower.`

        """
        return EntityManager(self,
                             entity_name='inventories',
                             entity_object='Inventory',
                             primary_match_field='name')

    def get_inventories_by_name(self, name):
        """Retrieves inventories by name.

        Args:
            name: The name of the inventories to retrieve.

        Returns:
            inventories (Generator): A generator with the matching inventories

        """
        return self.inventories.filter({'name__iexact': name})

    def get_organization_inventory_by_name(self, organization, name):
        """Retrieves an inventory by name from an organization.

        Args:
            organization: The name of the organization to retrieve the inventory from.
            name: The name of the inventory to retrieve.

        Returns:
            Inventory: The inventory if a match is found else None.

        Raises:
            InvalidOrganization: The organization provided as argument does not exist.

        """
        organization_ = self.get_organization_by_name(organization)
        if not organization_:
            raise InvalidOrganization(organization)
        return organization_.get_inventory_by_name(name)

    def get_inventory_by_id(self, id_):
        """Retrieves an inventory by id.

        Args:
            id_: The id of the inventory to retrieve.

        Returns:
            Inventory: The inventory if a match is found else None.

        """
        return next(self.inventories.filter({'id': id_}), None)

    def create_organization_inventory(self,
                                      organization,
                                      name,
                                      description,
                                      variables='{}'):
        """Creates an inventory under an organization.

        Args:
            organization: The name of the organization to create the inventory under
            name: The name of the inventory
            description: The description of the inventory
            variables: A json of the variables to be set on the inventory

        Returns:
            Inventory: The created inventory on success, None otherwise

        Raises:
            InvalidOrganization: The organization provided as argument does not exist.

        """
        organization_ = self.get_organization_by_name(organization)
        if not organization_:
            raise InvalidOrganization(organization)
        return organization_.create_inventory(name, description, variables)

    @property
    def inventory_scripts(self):
        """The inventories configured in tower.

        Returns:
            list of Inventory: The inventories configured in tower.`

        """
        return EntityManager(self,
                             entity_name='inventory_scripts',
                             entity_object='InventoryScript',
                             primary_match_field='name')

    def create_organization_inventory_script(self,
                                             organization,
                                             name,
                                             description,
                                             script):
        """Creates a custom inventory script.

        Args:
            organization: The organization the inventory script is part of.
            name: Name of the inventory script.
            description: The description of the inventory script.
            script: The script of the inventory script.

        Returns:
            Inventory_script: The created inventory script is successful, None otherwise.

        """
        organization_ = self.get_organization_by_name(organization)
        if not organization_:
            raise InvalidOrganization(organization)
        return organization_.create_inventory_script(name, description, script)

    def get_organization_inventory_script_by_name(self, organization, name):
        """Retrieves an custom inventory script by name from an organization.

        Args:
            organization: The name of the organization to retrieve the custom inventory script from.
            name: The name of the custom inventory script to retrieve.

        Returns:
            Inventory: The custom inventory script if a match is found else None.

        Raises:
            InvalidOrganization: The organization provided as argument does not exist.

        """
        organization_ = self.get_organization_by_name(organization)
        if not organization_:
            raise InvalidOrganization(organization)
        return organization_.get_inventory_script_by_name(name)

    def delete_organization_inventory_script(self, organization, name):
        """Deletes an custom inventory script from tower.

        Args:
            organization: The organization the custom inventory script is a member of.
            name: The name of the custom inventory script to delete.

        Returns:
            bool: True on success, False otherwise.

        Raises:
            InvalidInventory: The custom inventory script provided as argument does not exist.

        """
        inventory_script = self.get_organization_inventory_script_by_name(organization, name)
        if not inventory_script:
            raise InvalidInventoryScript(name)
        return inventory_script.delete()

    def delete_organization_inventory(self, organization, name):
        """Deletes an inventory from tower.

        Args:
            organization: The organization the inventory is a member of.
            name: The name of the inventory to delete.

        Returns:
            bool: True on success, False otherwise.

        Raises:
            InvalidInventory: The inventory provided as argument does not exist.

        """
        inventory = self.get_organization_inventory_by_name(organization, name)
        if not inventory:
            raise InvalidInventory(name)
        return inventory.delete()

    @property
    def hosts(self):
        """The hosts configured in tower.

        Returns:
            EntityManager: The manager object for hosts

        """
        return EntityManager(self,
                             entity_name='hosts',
                             entity_object='Host',
                             primary_match_field='name')

    def get_hosts_by_name(self, name):
        """Retrieves hosts by name.

        Args:
            name: The name of the hosts to retrieve.

        Returns:
            hosts (Generator): A generator with the matching hosts

        """
        return self.hosts.filter({'name__iexact': name})

    def get_inventory_host_by_name(self, organization, inventory, name):
        """Retrieves a host by name from an inventory.

        Args:
            organization: The name of the organization the inventory belongs to.
            inventory: The name of the inventory to search for a host.
            name: The name of the host to retrieve.

        Returns:
            Host: The host if a match is found else None.

        """
        inventory_ = self.get_organization_inventory_by_name(organization, inventory)
        if not inventory_:
            raise InvalidInventory(inventory)
        return inventory_.get_host_by_name(name)

    def get_host_by_id(self, id_):
        """Retrieves a host by id.

        Args:
            id_: The id of the host to retrieve.

        Returns:
            Host: The host if a match is found else None.

        """
        return next(self.hosts.filter({'id': id_}), None)

    def create_host_in_inventory(self,  # pylint: disable=too-many-arguments
                                 organization,
                                 inventory,
                                 name,
                                 description,
                                 variables='{}'):
        """Creates a host under an inventory.

        Args:
            organization: The name of the organization the inventory belongs to.
            inventory: The name of the inventory to create the host under.
            name: The name of the host.
            description: The description of the host.
            variables: A json of the variables to be set on the host.

        Returns:
            Host: The created host on success, None otherwise.

        Raises:
            InvalidInventory: The inventory provided as argument does not exist.

        """
        inventory_ = self.get_organization_inventory_by_name(organization, inventory)
        if not inventory_:
            raise InvalidInventory(inventory)
        return inventory_.create_host(name, description, variables)

    def associate_groups_with_inventory_host(self, organization, inventory, hostname, groups):
        """Adds groups to a host.

        Args:
            organization: The name of the organization the inventory belongs to.
            inventory: The inventory to retrieve the host from.
            hostname: The name of the host to add the groups to.
            groups: A string of a single group or a list or tuple of group names to add to host.

        Returns:
            bool: True on complete success, False otherwise.

        Raises:
            InvalidHost: The host provided as argument does not exist.

        """
        host = self.get_inventory_host_by_name(organization, inventory, hostname)
        if not host:
            raise InvalidHost(hostname)
        return host.associate_with_groups(groups)

    def disassociate_groups_from_inventory_host(self, organization, inventory, hostname, groups):
        """Removes groups from a host.

        Args:
            organization: The name of the organization the inventory belongs to.
            inventory: The inventory which contains the host to affect.
            hostname: The name of the host to remove the groups from.
            groups: A string of a single group or a list or tuple of group names to remove from a host.

        Returns:
            bool: True on complete success, False otherwise.

        Raises:
            InvalidHost: The host provided as argument does not exist.

        """
        host = self.get_inventory_host_by_name(organization, inventory, hostname)
        if not host:
            raise InvalidHost(hostname)
        return host.disassociate_with_groups(groups)

    def delete_inventory_host(self, organization, inventory, name):
        """Deletes an host from tower.

        Args:
            organization: The name of the organization the inventory belongs to.
            inventory: The name of the inventory to delete the host from.
            name: The name of the host to delete.

        Returns:
            bool: True on success, False otherwise.

        Raises:
            InvalidHost: The host provided as argument does not exist.

        """
        host = self.get_inventory_host_by_name(organization, inventory, name)
        if not host:
            raise InvalidHost(name)
        return host.delete()

    @property
    def instances(self):
        """The instances configured in tower.

        Returns:
            EntityManager: The manager object for instances.

        """
        return EntityManager(self,
                             entity_name='instances',
                             entity_object='Instance',
                             primary_match_field='name')

    @property
    def instance_groups(self):
        """The instance_groups configured in tower.

        Returns:
            EntityManager: The manager object for instance groups.

        """
        return EntityManager(self,
                             entity_name='instance_groups',
                             entity_object='InstanceGroup',
                             primary_match_field='name')

    @property
    def credential_types(self):
        """The credential_types configured in tower.

        Returns:
            EntityManager: The manager object for credentials type.

        """
        return EntityManager(self,
                             entity_name='credential_types',
                             entity_object='CredentialType',
                             primary_match_field='name')

    @property
    def tower_credential_types(self):
        """The default credential_types configured in tower.

        Returns:
            EntityManager: The manager object for internal credential types.

        """
        return EntityManager(self,
                             entity_name='credential_types',
                             entity_object='CredentialType',
                             primary_match_field='name').filter({'managed_by_tower': 'true'})

    @property
    def custom_credential_types(self):
        """The custom credential_types configured in tower.

        Returns:
            EntityManager: The manager object for external credential types.

        """
        return EntityManager(self,
                             entity_name='credential_types',
                             entity_object='CredentialType',
                             primary_match_field='name').filter({'managed_by_tower': 'false'})

    def get_credential_type_by_name(self, name):
        """Retrieves a credential_type by name.

        Args:
            name: The name of the credential_type to retrieve.

        Returns:
            Host: The credential_type if a match is found else None.

        """
        return next(self.credential_types.filter({'name__iexact': name}), None)

    def get_credential_type_by_id(self, id_):
        """Retrieves a credential_type by id.

        Args:
            id_: The id of the credential_type to retrieve.

        Returns:
            Host: The credential_type if a match is found else None.

        """
        return next(self.credential_types.filter({'id': id_}), None)

    def create_credential_type(self,  # pylint: disable=too-many-arguments
                               name,
                               description,
                               type_,
                               inputs_='{}',
                               injectors='{}'):
        """Creates a credential type in tower.

        Args:
            name: The name of the credential type.
            description: The description of the credential type.
            type_: The kind of credential type.Valid values (u'scm', u'ssh', u'vault', u'net', u'cloud', u'insights').
            inputs_ (str): A json of the inputs to set to the credential type.
            injectors (str): A json of the injectors to set to the credential type.

        Returns:
            CredentialType on success, None otherwise.

        Raises:
            InvalidCredentialTypeKind: The credential type kind provided as argument does not exist.
            InvalidVariables: The inputs or injectors provided as argument is not valid json.

        """
        if type_.lower() not in VALID_CREDENTIAL_TYPES:
            raise InvalidCredentialType(type_)
        payload = {'name': name,
                   'description': description,
                   'kind': type_.lower()}
        if not validate_json(inputs_):
            raise InvalidVariables(inputs_)
        if not validate_json(injectors):
            raise InvalidVariables(injectors)
        payload['inputs'] = json.loads(inputs_)
        payload['injectors'] = json.loads(injectors)
        url = f'{self.api}/credential_types/'
        response = self.session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Error creating credential type "%s", response was: "%s"', type_, response.text)
            return None
        else:
            self._logger.info("New credential_type '{}' was created successfully".format(payload['name']))
            return CredentialType(self, response.json())

    def delete_credential_type(self, name):
        """Deletes a credential_type from tower.

        Args:
            name: The name of the credential_type to delete.

        Returns:
            bool: True on success, False otherwise.

        Raises:
            InvalidCredential: The credential provided as argument does not exist.

        """
        credential_type = self.get_credential_type_by_name(name)
        if not credential_type:
            raise InvalidCredentialType(name)
        return credential_type.delete()

    @property
    def credentials(self):
        """The credentials configured in tower.

        Returns:
            EntityManager: The manager object for credentials.

        """
        return EntityManager(self,
                             entity_name='credentials',
                             entity_object='Credential',
                             primary_match_field='name')

    def get_credentials_by_name(self, name):
        """Retrieves all credentials matching a certain name.

        Args:
            name: The name of the credential(s) to retrieve.

        Returns:
            Credentials (Generator): A credentials generator.

        """
        return self.credentials.filter({'name__iexact': name})

    @property
    def settings(self):
        """The settings part of tower.

        Returns:
            EntityManager: The manager object for settings.

        """
        return Settings(self)

    def get_organization_credential_by_name(self, organization, name, credential_type):
        """Retrieves all credentials matching a certain name.

        Args:
            organization: The organization that owns the credential.
            name: The name of the credential(s) to retrieve.
            credential_type: The type of the credential.

        Returns:
            Credential: A credential if found else None.

        Raises:
            InvalidCredentialType: The CredentialType given was not found.
            InvalidOrganization: The Organization given was not found.

        """
        # return self.credentials.filter({'name__iexact': name})
        credential_type_ = self.get_credential_type_by_name(credential_type)
        if not credential_type_:
            raise InvalidCredentialType(credential_type)
        organization_ = self.get_organization_by_name(organization)
        if not organization_:
            raise InvalidOrganization(organization)
        return next(self.credentials.filter({'organization': organization_.id,
                                             'name__iexact': name,
                                             'credential_type': credential_type_.id}), None)

    def get_organization_credential_by_name_with_type_id(self, organization, name, credential_type_id):
        """Retrieves all credentials matching a certain name.

        Args:
            organization (str): The organization that owns the credential.
            name (str): The name of the credential(s) to retrieve.
            credential_type_id (int): The integer of the type of the credential.

        Returns:
            Credential: A credential if found else None.

        Raises:
            InvalidOrganization: The Organization given was not found.

        """
        # return self.credentials.filter({'name__iexact': name})
        organization_ = self.get_organization_by_name(organization)
        if not organization_:
            raise InvalidOrganization(organization)
        return next(self.credentials.filter({'organization': organization_.id,
                                             'name__iexact': name,
                                             'credential_type': credential_type_id}), None)

    def get_credential_by_id(self, id_):
        """Retrieves a credential by id.

        Args:
            id_: The id of the credential to retrieve.

        Returns:
            Host: The credential if a match is found else None.

        """
        return next(self.credentials.filter({'id': id_}), None)

    def create_credential_with_credential_type_id(self,  # pylint: disable=too-many-arguments
                                                  name: str,
                                                  credential_type_id: int,
                                                  description='',
                                                  organization_id=None,
                                                  user_id=None,
                                                  team_id=None,
                                                  inputs='{}'):
        """Creates a credential using the id  of the provided credential type.

        Args:
            name (str): The name of the credential
            credential_type_id (int): The number of the credential type
            description (str): The description of the credential
            organization_id (int): The id of the organization
            user_id (int): The id of the user
            team_id (int): The id of the team
            inputs (str): The input to provide to the credential as json in a string format

        Returns:
            credential (Credential|None): A credential object on success, false otherwise.

        """
        payload = {
            'name': name,
            'description': description,
            'credential_type': credential_type_id,
            'organization': organization_id,
            'user': user_id,
            'team': team_id,
            'inputs': json.loads(inputs)
        }

        url = f'{self.api}/credentials/'
        response = self.session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Error creating credential "%s", response was: "%s"', name, response.text)
            return None
        else:
            self._logger.info("New credential '{}' was created successfully".format(payload['name']))
            return Credential(self, response.json())

    def create_credential_in_organization(self,  # pylint: disable=too-many-arguments
                                          organization,
                                          name,
                                          description,
                                          credential_type,
                                          user=None,
                                          team=None,
                                          inputs_='{}'):
        """Creates a credential under an organization.

        Args:
            organization: The name of the organization to create a credential under.
            name: The name of the credential to create.
            description: The description of the credential to create.
            user: The username of the user to assign to the credential.
            team: The name of the team to assign to the credential.
            credential_type: The name of the type of the credential.
            inputs_: A json with the values to set to the credential according to what is required by its type.

        Returns:
            Credential: The created credential upon success, None otherwise.

        Raises:
            InvalidOrganization: The organization provided as argument does not exist.
            InvalidCredentialType: The credential type provided as argument does not exist.
            InvalidVariables: The inputs provided as argument is not valid json.
            InvalidUser: The user provided as argument does not exist.
            InvalidTeam: The team provided as argument does not exist.

        """
        team_id = None
        user_id = None
        organization_ = self.get_organization_by_name(organization)
        if not organization_:
            raise InvalidOrganization(organization)
        if user:
            user_ = self.get_user_by_username(user)
            if not user_:
                raise InvalidUser(user)
            user_id = user_.id
        if team:
            team_ = organization_.get_team_by_name(team)
            if not team_:
                raise InvalidTeam(team)
            team_id = team_.id
        credential_type_ = self.get_credential_type_by_name(credential_type)
        if not credential_type_:
            raise InvalidCredentialType(credential_type)
        if not validate_json(inputs_):
            raise InvalidVariables(inputs_)
        return self.create_credential_with_credential_type_id(name,
                                                              credential_type_.id,
                                                              description=description,
                                                              user_id=user_id,
                                                              team_id=team_id,
                                                              organization_id=organization_.id,
                                                              inputs=inputs_
                                                              )

    def create_credential_in_organization_with_type_id(self,  # pylint: disable=too-many-arguments
                                                       organization,
                                                       name,
                                                       description,
                                                       user,
                                                       team,
                                                       credential_type_id,
                                                       inputs_='{}'):
        """Creates a credential under an organization.

        Args:
            organization (str): The name of the organization to create a credential under.
            name (str): The name of the credential to create.
            description (str): The description of the credential to create.
            user (str): The username of the user to assign to the credential.
            team (str): The name of the team to assign to the credential.
            credential_type_id (int): The number of the type of the credential.
            inputs_ (str): A json with the values to set to the credential according to what is required by its type.

        Returns:
            Credential: The created credential upon success, None otherwise.

        Raises:
            InvalidOrganization: The organization provided as argument does not exist.
            InvalidUser: The user provided as argument does not exist.
            InvalidTeam: The team provided as argument does not exist.
            InvalidVariables: The inputs provided as argument is not valid json.

        """
        organization_ = self.get_organization_by_name(organization)
        if not organization_:
            raise InvalidOrganization(organization)
        user_ = self.get_user_by_username(user)
        if not user_:
            raise InvalidUser(user)
        team_ = organization_.get_team_by_name(team)
        if not team_:
            raise InvalidTeam(team)
        payload = {'name': name,
                   'description': description,
                   'organization': organization_.id,
                   'user': user_.id,
                   'team': team_.id,
                   'credential_type': credential_type_id}
        if not validate_json(inputs_):
            raise InvalidVariables(inputs_)
        payload['inputs'] = json.loads(inputs_)
        url = f'{self.api}/credentials/'
        response = self.session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Error creating credential "%s", response was: "%s"', name, response.text)
            return None
        else:
            self._logger.info("New credential '{}' was created successfully".format(payload['name']))
            return Credential(self, response.json())

    def delete_organization_credential_by_name(self, organization, name, credential_type):
        """Deletes a credential from an organization.

        Args:
            organization: The organization that owns the credential.
            name: The name of the credential(s) to delete.
            credential_type: The type of the credential.

        Returns:
            bool: True on success, False otherwise.

        Raises:
            InvalidCredentialType: The CredentialType given was not found.
            InvalidOrganization: The Organization given was not found.
            InvalidCredential: The credential was not found.

        """
        credential_type_ = self.get_credential_type_by_name(credential_type)
        if not credential_type_:
            raise InvalidCredentialType(credential_type)
        organization_ = self.get_organization_by_name(organization)
        if not organization_:
            raise InvalidOrganization(organization)
        credential = next(self.credentials.filter({'organization': organization_.id,
                                                   'name__iexact': name,
                                                   'credential_type': credential_type_.id}), None)
        if not credential:
            raise InvalidCredential(name)
        return credential.delete()

    def delete_organization_credential_by_name_with_type_id(self, organization, name, credential_type_id):
        """Deletes a credential from an organization.

        Args:
            organization (str): The organization that owns the credential.
            name (str): The name of the credential(s) to delete.
            credential_type_id (int): The type of the credential.

        Returns:
            bool: True on success, False otherwise.

        Raises:
            InvalidOrganization: The Organization given was not found.
            InvalidCredential: The credential was not found.

        """
        organization_ = self.get_organization_by_name(organization)
        if not organization_:
            raise InvalidOrganization(organization)
        credential = next(self.credentials.filter({'organization': organization_.id,
                                                   'name__iexact': name,
                                                   'credential_type': credential_type_id}), None)
        if not credential:
            raise InvalidCredential(name)
        return credential.delete()

    @property
    def jobs(self):
        """The jobs executed in tower.

        Returns:
            EntityManager: The manager object for jobs.

        """
        return EntityManager(self,
                             entity_name='jobs',
                             entity_object='Job',
                             primary_match_field='name')

    @property
    def unified_jobs(self):
        """The unified jobs executed in tower.

        Returns:
            EntityManager: The manager object for unified jobs.

        """
        return EntityManager(self,
                             entity_name='unified_jobs',
                             entity_object='Job',
                             primary_match_field='name')

    def get_unified_job_by_id(self, id_):
        """Retrieves a job  by id.

        Args:
            id_: The id of the job  to retrieve.

        Returns:
            Host: The job if a match is found else None.

        """
        return next(self.unified_jobs.filter({'id': id_}), None)

    def get_unified_jobs_by_name(self, name):
        """Retrieves all unified jobs matching a certain name.

        Args:
            name: The name of the unified job(s) to retrieve.

        Returns:
            UnifiedJob (Generator): A unified job generator.

        """
        return next(self.unified_jobs.filter({'name__iexact': name}), None)

    @property
    def unified_job_templates(self):
        """The unified job templates configured in tower.

        Returns:
            EntityManager: The manager object for unified job templates.

        """
        return EntityManager(self,
                             entity_name='unified_job_templates',
                             entity_object='JobTemplate',
                             primary_match_field='name')

    @property
    def workflow_jobs(self):
        """The workflow jobs executed in tower.

        Returns:
            EntityManager: The manager object for workflow jobs.

        """
        return EntityManager(self,
                             entity_name='workflow_jobs',
                             entity_object='Job',
                             primary_match_field='name')

    def get_workflow_job_by_id(self, id_):
        """Retrieves a job  by id.

        Args:
            id_: The id of the job  to retrieve.

        Returns:
            Host: The job if a match is found else None.

        """
        return next(self.workflow_jobs.filter({'id': id_}), None)

    def get_workflow_jobs_by_name(self, name):
        """Retrieves all workflow jobs matching a certain name.

        Args:
            name: The name of the workflow job(s) to retrieve.

        Returns:
            UnifiedJob (Generator): A workflow job generator.

        """
        return next(self.workflow_jobs.filter({'name__iexact': name}), None)

    @property
    def workflow_job_templates(self):
        """The workflow job templates configured in tower.

        Returns:
            EntityManager: The manager object for workflow job templates.

        """
        return EntityManager(self,
                             entity_name='workflow_job_templates',
                             entity_object='JobTemplate',
                             primary_match_field='name')

    def get_workflow_job_template_by_id(self, id_):
        """Retrieves a workflow template job by id.

        Args:
            id_: The id of the workflow template job to retrieve.

        Returns:
            Host: The job if a match is found else None.

        """
        return next(self.workflow_job_templates.filter({'id': id_}), None)

    def get_workflow_job_templates_by_name(self, name):
        """Retrieves all workflow template jobs matching a certain name.

        Args:
            name: The name of the workflow template job(s) to retrieve.

        Returns:
            UnifiedJob (Generator): A workflow template job generator.

        """
        return next(self.workflow_job_templates.filter({'name__iexact': name}), None)

    @property
    def system_jobs(self):
        """The system jobs executed in tower.

        Returns:
            EntityManager: The manager object for system jobs.

        """
        return EntityManager(self,
                             entity_name='system_jobs',
                             entity_object='Job',
                             primary_match_field='name')

    def get_system_job_by_id(self, id_):
        """Retrieves a job  by id.

        Args:
            id_: The id of the job  to retrieve.

        Returns:
            Host: The job if a match is found else None.

        """
        return next(self.system_jobs.filter({'id': id_}), None)

    def get_system_jobs_by_name(self, name):
        """Retrieves all system jobs matching a certain name.

        Args:
            name: The name of the system job(s) to retrieve.

        Returns:
            UnifiedJob (Generator): A system job generator.

        """
        return next(self.system_jobs.filter({'name__iexact': name}), None)

    @property
    def job_templates(self):
        """The job templates configured in tower.

        Returns:
            EntityManager: The manager object for job templates.

        """
        return EntityManager(self,
                             entity_name='job_templates',
                             entity_object='JobTemplate',
                             primary_match_field='name')

    def get_job_template_by_name(self, name):
        """Retrieves job_template by name.

        Args:
            name: The name of the job_template to retrieve.

        Returns:
            job_templates (JobTemplate): A template with the matching name

        """
        return next(self.job_templates.filter({'name__iexact': name}), None)

    def get_job_template_by_id(self, id_):
        """Retrieves a job template by id.

        Args:
            id_: The id of the job template to retrieve.

        Returns:
            Host: The job template if a match is found else None.

        """
        return next(self.job_templates.filter({'id': id_}), None)

    def create_job_template(self,
                            # pylint: disable=too-many-arguments, too-many-locals, too-many-branches  # noqa: C901
                            name,
                            description,
                            organization,
                            inventory,
                            project,
                            playbook,
                            credential=None,
                            credential_type=None,
                            instance_groups=None,
                            host_config_key=None,
                            job_type='run',
                            vault_credential=None,
                            forks=0,
                            limit=0,
                            verbosity=0,
                            extra_vars='',
                            job_tags='',
                            force_handlers=False,
                            skip_tags='',
                            start_at_task='',
                            timeout=0,
                            use_fact_cache=False,
                            ask_diff_mode_on_launch=False,
                            ask_variables_on_launch=False,
                            ask_limit_on_launch=False,
                            ask_tags_on_launch=False,
                            ask_skip_tags_on_launch=False,
                            ask_job_type_on_launch=False,
                            ask_verbosity_on_launch=False,
                            ask_inventory_on_launch=False,
                            ask_credential_on_launch=False,
                            survey_enabled=False,
                            become_enabled=False,
                            diff_mode=False,
                            allow_simultaneous=False):
        """Creates a job template.

        Args:
            name: The name of the job template to create.
            description: The description of the job template to create.
            organization: The organization the inventory belongs to.
            inventory: The inventory to use for the template.
            project: The project to use for the template.
            playbook: The playbook to run for the template.
            credential: The credential to use for the template.
            credential_type: The type of the credential to use for the template.
            instance_groups: The instance groups to associate to the template.
            host_config_key: A host config key.
            job_type: The job type. Valid values are 'run' and 'check'.
            vault_credential: A vault credential.
            forks: The number of parallel or simultaneous processes to use while executing the playbook.
            limit: A host pattern to constrain the list of hosts that will be managed or affected by the playbook.
            verbosity: The level of output ansible will produce as the playbook executes. Values [0-4].
            extra_vars: Pass extra command line variables to the playbook.
            job_tags: Tags to identify the template.
            force_handlers:
            skip_tags: Skip specific parts of a play or task with tags.
            start_at_task:
            timeout:
            use_fact_cache:
            ask_diff_mode_on_launch:
            ask_variables_on_launch:
            ask_limit_on_launch:
            ask_tags_on_launch:
            ask_skip_tags_on_launch:
            ask_job_type_on_launch:
            ask_verbosity_on_launch:
            ask_inventory_on_launch:
            ask_credential_on_launch:
            survey_enabled:
            become_enabled:
            diff_mode:
            allow_simultaneous:

        Returns:
            JobTemplate: The created job template if successful, None otherwise.

        Raises:
            InvalidInventory: The inventory provided as argument does not exist.
            InvalidProject: The project provided as argument does not exist.
            InvalidPlaybook: The playbook provided as argument does not exist in project.
            InvalidInstanceGroup: The instance group provided as argument does not exist.
            InvalidJobType: The job type provided as argument does not exist.
            InvalidVerbosity: The verbosity provided is not in valid range of 0-4.
            InvalidCredentialType: The credential type is invalid.

        """
        credential_id = None
        inventory_ = self.get_organization_inventory_by_name(organization, inventory)
        if not inventory_:
            raise InvalidInventory(inventory)
        project_ = self.get_organization_project_by_name(organization, project)
        if not project_:
            raise InvalidProject(project)
        if playbook not in project_.playbooks:
            raise InvalidPlaybook(playbook)
        if all([credential, credential_type]):
            credential_ = inventory_.organization.get_credential_by_name(credential, credential_type)
            if not credential_:
                raise InvalidCredential(credential)
            credential_id = credential_.id
        elif any([credential, credential_type]):
            self._logger.error('Both credential and credential type should be provided.')
        instance_group_ids = []
        if instance_groups:
            if not isinstance(instance_groups, (list, tuple)):
                instance_groups = [instance_groups]
            tower_instance_groups_names = [group.name for group in self.instance_groups]
            invalid = set(instance_groups) - set(tower_instance_groups_names)
            if invalid:
                raise InvalidInstanceGroup(invalid)
            for instance_group in set(instance_groups):
                group = next((group for group in self.instance_groups
                              if group.name == instance_group), None)
                instance_group_ids.append(group.id)
        if job_type not in JOB_TYPES:
            raise InvalidJobType(job_type)
        if verbosity not in VERBOSITY_LEVELS:
            raise InvalidVerbosity(verbosity)
        payload = {'name': name,
                   'description': description,
                   'inventory': inventory_.id,
                   'project': project_.id,
                   'playbook': playbook,
                   'instance_groups': instance_group_ids,
                   'job_type': job_type,
                   'vault_credential': vault_credential,
                   'forks': forks,
                   'limit': limit,
                   'verbosity': verbosity,
                   'extra_vars': extra_vars,
                   'job_tags': job_tags,
                   'force_handlers': force_handlers,
                   'skip_tags': skip_tags,
                   'start_at_task': start_at_task,
                   'timeout': timeout,
                   'use_fact_cache': use_fact_cache,
                   'host_config_key': host_config_key,
                   'ask_diff_mode_on_launch': ask_diff_mode_on_launch,
                   'ask_variables_on_launch': ask_variables_on_launch,
                   'ask_limit_on_launch': ask_limit_on_launch,
                   'ask_tags_on_launch': ask_tags_on_launch,
                   'ask_skip_tags_on_launch': ask_skip_tags_on_launch,
                   'ask_job_type_on_launch': ask_job_type_on_launch,
                   'ask_verbosity_on_launch': ask_verbosity_on_launch,
                   'ask_inventory_on_launch': ask_inventory_on_launch,
                   'ask_credential_on_launch': ask_credential_on_launch,
                   'survey_enabled': survey_enabled,
                   'become_enabled': become_enabled,
                   'diff_mode': diff_mode,
                   'allow_simultaneous': allow_simultaneous}
        url = f'{self.api}/job_templates/'
        response = self.session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Error creating job template, response was: "%s"', response.text)
            return None
        job_template = JobTemplate(self, response.json())
        if credential_id:
            if not job_template.add_credential_by_id(credential_id):
                self._logger.error('Error adding credentials, reverting the creation of the job template')
                if not job_template.delete():
                    raise FailedToDeleteTemplate(name)
                return None
        return job_template

    def delete_job_template(self, name):
        """Deletes a job template from tower.

        Args:
            name: The name of the job template to delete.

        Returns:
            bool: True on success, False otherwise.

        Raises:
            InvalidJobTemplate: The job template provided as argument does not exist.

        """
        job_template = self.get_job_template_by_name(name)
        if not job_template:
            raise InvalidJobTemplate(name)
        return job_template.delete()

    @property
    def roles(self):
        """The roles configured in tower.

        Returns:
            EntityManager: The manager object for roles.

        """
        return EntityManager(self,
                             entity_name='roles',
                             entity_object='Role',
                             primary_match_field='name')

    def _get_object_by_url(self, object_type, url):
        url = f'{self.host}{url}'
        response = self.session.get(url)
        entities = sys.modules['towerlib.entities']
        obj = getattr(entities, object_type)
        return obj(self, response.json()) if response.ok else None

    @property
    def notification_templates(self):
        """The notification templates configured in tower.

        Returns:
            EntityManager: The manager object for groups.

        """
        return EntityManager(self,
                             entity_name='notification_templates',
                             entity_object='NotificationTemplate',
                             primary_match_field='name')

    @property
    def inventory_sources(self):
        """A manager object for the inventory_sources in tower.

        Returns:
            EntityManager: The manager object for inventory_sources.

        """
        return EntityManager(self,
                             entity_name='inventory_sources',
                             entity_object='InventorySource',
                             primary_match_field='name')

    @property
    def project_updates(self):
        """A manager object for the project_updates in tower.

        Returns:
            EntityManager: The manager object for project_updates.

        """
        return EntityManager(self,
                             entity_name='project_updates',
                             entity_object='ProjectUpdateJob',
                             primary_match_field='name')

    @property
    def schedules(self):
        """The schedules configured in tower.
        Returns:
            EntityManager: The manager object for schedules.
        """
        return EntityManager(self,
                             entity_name='schedules',
                             entity_object='Schedule',
                             primary_match_field='name')

    def get_schedule_by_id(self, id_):
        """Retrieves a schedule by id.
        Args:
            id_: The id of the schedule to retrieve.
        Returns:
            Schedule: The schedule if a match is found else None.
        """
        return next(self.schedules.filter({'id': id_}), None)

    def get_schedule_by_name(self, name):
        """Retrieves an schedule by name.
        Args:
            name: The name of the schedule to retrieve.
        Returns:
            Schedule: The schedule if a match is found else None.
        """
        return next(self.schedules.filter({'name__iexact': name}), None)

    def update_all_organization_projects(self, organization_name):
        """Update all the projects in ansible tower for a given organization.
        """
        organization = self.get_organization_by_name(organization_name)
        for project in organization.projects:
            project.update

    def update_project_by_id(self, project_id):
        """Update the ansible tower project with given project id.

        Args:
            project_id: The id of the project, which is to be updated.

        Returns:
            list: List of response of api request as json on success, None otherwise.

        """
        project = self.get_project_by_id(project_id)
        return project.update

    def update_organization_project_by_name(self, organization, project_name):
        """Update the ansible tower project with given project name.

        Args:
            organization: The name of the organization.
            project_name: The name of the project, which is to be updated.

        Returns:
            dict: dict of response of api request as json on success, None otherwise.

        """

        project = self.get_organization_project_by_name(organization, project_name)
        return project.update

    def update_project_by_scm_url(self, scm_url):
        """Send update request to update project for a given git repository (scm_url).

        Args:
            scm_url: the http url of the required repository.

        """

        matching_projects = [project for project in self.projects if project.scm_url == scm_url]
        for project in matching_projects:
            self._logger.debug("A request is being sent to update the project with the name '{}' and with scm url '{}'"
                               .format(project.name, scm_url))
            project.update

    def update_project_by_branch_name(self, scm_url, branch_name):
        """Update an ansible tower project or list of projects based on their branch name.

        A scm_branch can only be identified correctly with a corresponding scm_url.

        Args:
            scm_url: the URL of the relevant repository configured in the project.
            branch_name: the name of the branch, which is selected as scm_branch parameter of the project.

        """

        matching_projects = [project for project in self.projects if
                             project.scm_url == scm_url and project.scm_branch == branch_name]
        for project in matching_projects:
            self._logger.debug("A request is being sent to update the project with the name '{}' and with scm url '{}' "
                               "and branch name '{}'".format(project.name, scm_url, branch_name))
            project.update

    def change_job_template_data(self, job_template_data):
        """Send API PATCH request to update the job template information with the given data.
        https://docs.ansible.com/ansible-tower/3.6.1/html/towerapi/api_ref.html#/Authentication/Authentication_applications_partial_update_0

        Args:
            job_template_data: updated data of the job template as dictionary

        Returns:
            list: List of response of api request as json on success, False otherwise.

        """
        job_template_id = job_template_data['id']
        job_url = '{api}/job_templates/{id}/'.format(api=self.api, id=job_template_id)
        response = self.session.patch(job_url, data=json.dumps(job_template_data))
        if not response.ok:
            self._logger.error("Error updating the job template with the given data '{}'".format(job_template_data))
            return None
        else:
            self._logger.info("Job template with the name '{}' is updated successfully.".format(job_template_data['name']))
            return response.json()

    def change_project_of_job_template(self, job_template, project_id):
        """A job template in the ansible tower has to have a project from the list of projects.

        This function helps to change the project name of a job template in ansible tower for a given job template.

        Args:
            job_template: given job template object
            project_id: given project's id

        Returns:
            Object: The updated job_template object

        """

        project_obj = self.get_project_by_id(project_id)
        project_playbooks = self.get_playbooks_by_branch_name(project_obj.scm_url, project_obj.scm_branch)
        new_playbook = job_template.playbook
        if new_playbook not in project_playbooks:
            self._logger.warning("Job template's playbook '{}' is not found in the given project's playbook"
                                 "list. Now changing the playbook to '{}'. Please select a playbook manually."
                                 .format(new_playbook, project_playbooks[0]))
            new_playbook = project_playbooks[0]

        new_data = {
            "id": job_template.id,
            "project": project_obj.id,
            "playbook": new_playbook,
            "name": job_template.name,
            "description": job_template.description
        }
        response = self.change_job_template_data(new_data)
        if response is not None:
            self._logger.info("The project for the job template '{}' is changed from '{}' to '{}'".
                              format(job_template.name, job_template.project.name, project_obj.name))
        else:
            self._logger.error("Error updating the job template's project.")
        return response

    def change_job_type(self, given_labels, new_job_type):
        """Change the job template type in the given Ansible Tower, which means whether a job should run in 'Run' or
        'Check' mode.

        Args:
            given_labels: ist of labels which need to match
            new_job_type: the updated job type.

        Returns:

        """
        count = 0
        for job_template in self.job_templates:
            if job_template.labels['count'] > 0:
                label_results = job_template.labels['results']
                job_labels = [item['name'] for item in label_results]
                if set(given_labels) == set(job_labels):
                    count += 1
                    self._logger.info("Equal labels found for the job template '{}'".format(job_template.name))
                    existing_job_type = job_template.job_type
                    if existing_job_type.lower() == new_job_type.lower():
                        self._logger.info(
                            "Existing job-type is already: '{}'. Change is not required for this job template.".
                                format(existing_job_type))
                    else:
                        self._logger.debug("Changing job type from '{}' to '{}'"
                                           .format(existing_job_type, new_job_type))
                        job_template_data = {
                            "id": job_template.id,
                            "job_type": new_job_type,
                            "name": job_template.name,
                            "playbook": job_template.playbook
                        }
                        self.change_job_template_data(job_template_data)
        if count < 1:
            self._logger.debug("No job template, which matched all the labels in the config file.")

    def get_credential_id_from_existing_project_by_scm_url(self, scm_url):
        """This function gets credential id from an existing project, which has the same credential id.

        This function is for additional convenience. If there is already a project with the same scm url configured,
        then we will find it with this function. This function also makes sure that the user does not have to specify a
        credential id in the config file .
        This function will only be called if no credential id is given in the config file. Anyway, if no credential is
        given by config file and no credential id is found with this function, the script will continue and create
        projects, because projects can be created in Ansible Tower without credentials (but in that case, the scm
        update job will fail.)

        Args:
            scm_url: the scm_url of the corresponding project.

        Returns:
            id of a credential if corresponding project exists, else None.

        """
        scm_credential_type_ids = []
        credential_types = list(self.credential_types)
        for credential_type in credential_types:
            if credential_type.kind == 'scm':
                scm_credential_type_ids.append(credential_type.id)
        credential_id = None
        projects = list(self.projects)
        for scm_credential_type_id in scm_credential_type_ids:
            for project in projects:
                if project.scm_url == scm_url:
                    self._logger.debug("Project found with the scm credential.")
                    if project.credential.credential_type.id == scm_credential_type_id:
                        credential_id = project.credential.id
                        if credential_id:
                            self._logger.debug("Credential ID found from the existing project '{}' and the id is '{}'"
                                               .format(project.name, credential_id))
                            return credential_id
        return credential_id

    def get_ansible_facts_by_host_id(self, host_id):
        """Get the ansible_facts of the given host.

        Args:
            host_id: id of the host for which the method will return the ansible_facts.

        Returns:
            dict: ansible_facts as dictionary.

        """
        host = self.get_host_by_id(host_id)
        if not host:
            raise InvalidHost(host_id)
        return host.ansible_facts()

    def get_hosts_by_inventory_id(self, inventory_id):
        """Get filtered list of hosts for a given inventory id.

        Args:
             inventory_id: the given inventory id.

        Returns:
            list: the list of filtered host as EntityManger object.

        """
        hosts = [item for item in self.hosts if item.inventory.id == inventory_id]
        return hosts

    def get_jobs_by_name(self, name):
        """Get filtered list of jobs for a given name.

        Args:
            name: the given job name.

        Returns:
             list: the filtered list of jobs.

        """

        return self.jobs.filter({'name__iexact': name})

    def get_job_by_id(self, id_):
        """Retrieves a job by id.

        Args:
            id_: The id of the job to retrieve.

        Returns:
            Host: The host if a match is found else None.

        """
        return next(self.jobs.filter({'id': id_}), None)

    def get_project_updates_by_project_name(self, given_project_name):
        """Get project update with the given project name.

        Args:
            given_project_name: the name of the project.

        Returns:
            dict: the project with all the information.

        """

        return [item for item in self.project_updates if item.project.name == given_project_name]

    def get_project_updates_by_project_id(self, given_project_id):
        """Get project update with the given project id.

        Args:
            given_project_id: the id of the project.

        Returns:
            dict: the project with all the information.

        """

        return [item for item in self.project_updates if item.project.id == given_project_id]

    def get_project_update_by_id(self, id_):
        """Retrieves a project_update by id.

        Args:
            id_: The id of the project_update to retrieve.

        Returns:
            Host: The project_update if a match is found else None.

        """
        return next(self.project_updates.filter({'id': id_}), None)

    def get_project_updates_by_name(self, name):
        """Retrieves project_updates matching a certain name.

        Args:
            name: the given job_update name.

        Returns:
             list: the filtered list of project update jobs.

        """
        return self.project_updates.filter({'name__iexact': name})

    @property
    def job_events(self):
        """The job templates configured in tower.

        Returns:
            EntityManager: The manager object for job templates.

        """
        return EntityManager(self,
                             entity_name='job_events',
                             entity_object='JobEvent',
                             primary_match_field='name')

    def get_job_creation_dates_by_host(self, host):
        """Get job creation dates from ansible tower for a given host

        Args:
            host: the host object of tower instance.

        Returns:
            list: a list containing the formatted datetime objects.

        """
        job_events = host.job_events
        if job_events is None:
            self._logger.error("No job events found.")
            return None
        job_dates = []
        for job_event in job_events:
            job_event_time = job_event.created_at
            job_dates.append(job_event_time)
        return job_dates

    def get_groups_by_host(self, host):
        """Get groups for a particular host, which are directly connected.

        Args:
            host: the host object.

        Returns:
            list: list of custom groups.

        """
        url = "{api}/hosts/{id}/groups/".format(api=self.api, id=host.id)
        response = self.session.get(url)
        if not response.ok:
            self._logger.error("Error getting the project updates. response was: {})".format(response.text))
            return None
        else:
            results = response.json().get('results', [])
            groups = []
            for group in results:
                groups.append(group)
            return groups

    def get_all_groups_by_host(self, host):
        """Get groups for a particular host, which are directly and indirectly connected.

        Args:
            host: the host object.

        Returns:
            list: list of custom groups.

        """
        url = "{api}/hosts/{id}/all_groups/".format(api=self.api, id=host.id)
        response = self.session.get(url)
        if not response.ok:
            self._logger.error("Error getting the project updates. response was: {})".format(response.text))
            return None
        else:
            results = response.json().get('results', [])
            groups = []
            for group in results:
                groups.append(group)
            return groups


    def search_generic_item_by_keyword(self, generic_item_name_plural, keyword=''):
        """
        Search query string parameter to perform a case-insensitive search within all designated text fields of a model
        or item. Model/item means projects, jobs, inventories etc.
        https://docs.ansible.com/ansible-tower/latest/html/towerapi/searching.html

        Args:
            generic_item_name_plural: the plural name of the model/item e.g. projects, jobs, job_templates, users etc.
            keyword: case insensitive search string.

        Returns:
            list: list of matching item objects.

        """
        if not generic_item_name_plural.lower() in GENERIC_SEARCH_ITEMS:
            self._logger.error("The generic search item '{}' not found.".format(generic_item_name_plural))
            return None
        url = "{api}/{item}/?search={keyword}".format(api=self.api, item=generic_item_name_plural, keyword=keyword)
        response = self.session.get(url)
        if not response.ok:
            self._logger.error("Error getting the search result. Response was: {})".format(response.text))
            return None
        page_id = 2
        results = response.json().get('results', [])
        while response.json().get('next'):
            url = "{api}/{item}/?page={page_id}&search={keyword}".format(api=self.api,
                                                                         item=generic_item_name_plural,
                                                                         page_id=page_id,
                                                                         keyword=keyword)
            response = self.session.get(url)
            results.extend(response.json().get('results', []))
            if not response.ok:
                self._logger.error("Error getting search result for the api page '{page}'. Response was: "
                                   "{response})".format(page=page_id, response=response.text))
            page_id += 1
        return results
