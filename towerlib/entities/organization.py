#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: organization.py
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
Main code for organization.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import logging

from towerlib.towerlibexceptions import (InvalidTeam,
                                         InvalidVariables,
                                         InvalidInventory,
                                         InvalidCredential,
                                         InvalidProject,
                                         InvalidCredentialType,
                                         InvalidValue,
                                         InvalidInventoryScript)
from .core import (Entity,
                   EntityManager,
                   validate_max_length,
                   validate_json)
from .inventory import Inventory
from .inventory_script import InventoryScript
from .project import Project
from .team import Team

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
LOGGER_BASENAME = '''organization'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class Organization(Entity):  # pylint: disable=too-many-public-methods
    """Models the organization entity of ansible tower."""

    DEFAULT_MEMBER_ROLE = 'Member'

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def name(self):
        """The name of the Organization.

        Returns:
            string: The name of the organization.

        """
        return self._data.get('name')

    @name.setter
    def name(self, value):
        """Update the name of the organization.

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
        """The description of the Organization.

        Returns:
            string: The description of the Organization.

        """
        return self._data.get('description')

    @description.setter
    def description(self, value):
        """Update the description of the organization.

        Returns:
            None:

        """
        self._update_values('description', value)

    @property
    def custom_virtualenv(self):
        """The path of the custom virtual environment.

        Returns:
            string: The path of the custom virtual environment.

        """
        return self._data.get('custom_virtualenv')

    @custom_virtualenv.setter
    def custom_virtualenv(self, value):
        """Update the custom_virtualenv of the group.

        Returns:
            None:

        """
        max_characters = 100
        conditions = [validate_max_length(value, max_characters)]
        if all(conditions):
            self._update_values('custom_virtualenv', value)
        else:
            raise InvalidValue(f'{value} is invalid. Condition max_characters must be less than or equal to '
                               f'{max_characters}')

    @property
    def created_by(self):
        """The User that created the organization.

        Returns:
            User: The user that created the organization in tower.

        """
        url = self._data.get('related', {}).get('created_by')
        return self._tower._get_object_by_url('User', url)  # pylint: disable=protected-access

    @property
    def modified_by(self):
        """The User that modified the organization last.

        Returns:
            User: The user that modified the organization in tower last.

        """
        url = self._data.get('related', {}).get('modified_by')
        return self._tower._get_object_by_url('User', url)  # pylint: disable=protected-access

    def _get_object_role_id(self, name):
        """
        Returns the object role ID for a given member.

        Args:
            name: The role we want to get the id for

        Returns:
            int: The ID of the role
            None: If the role is not found

        """
        return next((obj.id for obj in self.object_roles
                     if obj.name.lower() == name.lower()), None)

    @property
    def object_roles(self):
        """The object roles.

        Returns:
            EntityManager: EntityManager of the roles supported.

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
    def _related_field_counts(self):
        """
        Get the related fields counts.

        Returns:
            dict: A dictionary of all the related field counts

        """
        return self._data.get('summary_fields', {}).get('related_field_counts', {})

    @property
    def job_templates_count(self):
        """The number of job templates of the organization.

        Returns:
            integer: The count of the job templates on the organization.

        """
        return self._related_field_counts.get('job_templates', 0)

    @property
    def admins_count(self):
        """The number of administrators of the organization.

        Returns:
            integer: The count of the administrators on the organization.

        """
        return self._related_field_counts.get('admins', 0)

    @property
    def projects(self):
        """The projects of the organization.

        Returns:
            EntityManager: EntityManager of the projects.

        """
        url = self._data.get('related', {}).get('projects')
        return EntityManager(self._tower,
                             entity_object='Project',
                             primary_match_field='name',
                             url=url)

    @property
    def projects_count(self):
        """The number of projects of the organization.

        Returns:
            integer: The count of the projects on the organization.

        """
        return self._related_field_counts.get('projects', 0)

    def get_project_by_name(self, name):
        """Retrieves a project.

        Args:
            name: The name of the project to retrieve.

        Returns:
            project (Project): project on success else None.

        """
        return next(self._tower.projects.filter({'organization': self.id, 'name__iexact': name}), None)

    def create_project(self,  # pylint: disable=too-many-arguments, too-many-locals
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
        """Creates a project in the organization.

        Args:
            name (str): The name of the project.
            description (str): The description of the project.
            credential (str): The name of the credential to use for the project or '' if None.
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
            InvalidCredential: The credential provided as argument does not exist.

        """
        # Credential Type 2 = SCM
        url = '{api}/projects/'.format(api=self._tower.api)
        payload = {'name': name,
                   'description': description,
                   'scm_type': scm_type,
                   'custom_virtualenv': custom_virtualenv,
                   'local_path': local_path,
                   'scm_url': scm_url,
                   'scm_branch': scm_branch,
                   'scm_clean': scm_clean,
                   'scm_delete_on_update': scm_delete_on_update,
                   'timeout': 0,
                   'organization': self.id,
                   'scm_update_on_launch': scm_update_on_launch,
                   'scm_update_cache_timeout': scm_update_cache_timeout}
        if credential:
            credential_ = self.get_credential_by_name_with_type_id(credential, credential_type_id=2)
            if not credential_:
                raise InvalidCredential(credential)
            payload['credential'] = credential_.id
        response = self._tower.session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Error creating project, response was: "%s"', response.text)
        return Project(self._tower, response.json()) if response.ok else None

    def delete_project(self, name):
        """Deletes a project by username.

        Args:
            name: The name of the project to delete.

        Returns:
            bool: True on success, False otherwise.

        Raises:
            InvalidProject: The project provided as argument does not exist.

        """
        project = self.get_project_by_name(name)
        if not project:
            raise InvalidProject(name)
        return project.delete()

    @property
    def users(self):
        """The users of the organization.

        Returns:
            EntityManager: EntityManager of the users of the organization.

        """
        url = f'{self.api_url}users/'
        return EntityManager(self._tower,
                             entity_object='User',
                             primary_match_field='username',
                             url=url)

    @property
    def users_count(self):
        """The number of user of the organization.

        Returns:
            integer: The count of the users on the organization.

        """
        return self._related_field_counts.get('users', 0)

    @property
    def teams(self):
        """The teams of the organization.

        Returns:
            EntityManager: EntityManager of the teams of the organization.

        """
        url = f'{self.api_url}teams/'
        return EntityManager(self._tower,
                             entity_object='Team',
                             primary_match_field='name',
                             url=url)

    @property
    def teams_count(self):
        """The number of teams of the organization.

        Returns:
            integer: The count of the teams on the organization.

        """
        return self._related_field_counts.get('teams', 0)

    def get_team_by_name(self, name):
        """Retrieves a team.

        Args:
            name: The name of the team to retrieve.

        Returns:
            team (Team): team on success else None.

        """
        return next(self._tower.teams.filter({'organization': self.id, 'name__iexact': name}), None)

    def create_team(self, name, description):
        """Creates a team.

        Args:
            name: The name of the team to create.
            description: The description of the team.

        Returns:
            Team: The created Team object on success, None otherwise.

        """
        payload = {'name': name,
                   'description': description,
                   'organization': self.id}
        url = f'{self._tower.api}/teams/'
        response = self._tower.session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Error creating team "%s", response was : "%s"', name, response.text)
        return Team(self._tower, response.json()) if response.ok else None

    def delete_team(self, name):
        """Deletes a team by name.

        Args:
            name: The name of the team to delete.

        Returns:
            bool: True on success, False otherwise.

        Raises:
            InvalidTeam: The team provided as argument does not exist.

        """
        team = self.get_team_by_name(name)
        if not team:
            raise InvalidTeam(name)
        return team.delete()

    @property
    def inventories(self):
        """The inventories of the organization.

        Returns:
            EntityManager: EntityManager of the inventories of the organization.

        """
        url = f'{self.api_url}inventories/'
        return EntityManager(self._tower,
                             entity_object='Inventory',
                             primary_match_field='name',
                             url=url)

    @property
    def inventories_count(self):
        """The number of inventories of the organization.

        Returns:
            integer: The count of the inventories on the organization.

        """
        return self._related_field_counts.get('inventories', 0)

    def get_inventory_by_name(self, name):
        """Retrieves an inventory.

        Args:
            name: The name of the inventory to retrieve.

        Returns:
            inventory(Inventory): inventory on success else None.

        """
        return next(self._tower.inventories.filter({'organization': self.id, 'name__iexact': name}), None)

    def create_inventory(self, name, description, variables='{}'):
        """Creates an inventory.

        Args:
            name: The name of the inventory to create.
            description: The description of the inventory.
            variables: A json with the initial variables set on the inventory.

        Returns:
            Inventory: The created Inventory object on success, None otherwise.

        Raises:
            InvalidVariables: The variables provided as argument is not valid json.

        """
        if not validate_json(variables):
            raise InvalidVariables(variables)
        payload = {'name': name,
                   'description': description,
                   'organization': self.id,
                   'variables': variables}
        url = f'{self._tower.api}/inventories/'
        response = self._tower.session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Error creating inventory "%s", response was "%s"', name, response.text)
        return Inventory(self._tower, response.json()) if response.ok else None

    @property
    def inventory_scripts(self):
        """The inventory scripts of the organization.

        Returns:
            EntityManager: EntityManager of the inventory scripts of the organization.

        """
        return self._tower.inventory_scripts.filter({'organization': self.id})

    def get_inventory_script_by_name(self, name):
        """Retrieves an custom inventory script.

        Args:
            name: The name of the custom inventory script to retrieve.

        Returns:
            inventory(Inventory): custom inventory script on success else None.

        """
        return next(self._tower.inventory_scripts.filter({'organization': self.id, 'name__iexact': name}), None)

    def create_inventory_script(self, name, description, script):
        """Creates a custom inventory script.

        Args:
            name: Name of the inventory script.
            description: The description of the inventory script.
            script: The script of the inventory script.

        Returns:
            Inventory_script: The created inventory script is successful, None otherwise.

        """
        url = f'{self._tower.api}/inventory_scripts/'
        payload = {'name': name,
                   'description': description,
                   'script': script,
                   'organization': self.id
                   }
        response = self._tower.session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Error creating host "%s", response was "%s"', name, response.text)
        return InventoryScript(self._tower, response.json()) if response.ok else None

    def delete_inventory_script(self, name):
        """Deletes a custom inventory script.

        Args:
            name: The name of the custom inventory script to delete.

        Returns:
            bool: True on success, False otherwise.

        Raises:
            InvalidInventoryScript: The inventory_script provided as argument does not exist.

        """
        inventory_script = self.get_inventory_script_by_name(name)
        if not inventory_script:
            raise InvalidInventoryScript(name)
        return inventory_script.delete()

    def delete_inventory(self, name):
        """Deletes an inventory by name.

        Args:
            name: The name of the inventory to delete.

        Returns:
            bool: True on success, False otherwise.

        Raises:
            InvalidInventory: The inventory provided as argument does not exist.

        """
        inventory = self.get_inventory_by_name(name)
        if not inventory:
            raise InvalidInventory(name)
        return inventory.delete()

    @property
    def credentials(self):
        """The credentials of the organization.

        Returns:
            EntityManager: EntityManager of the credentials of the organization.

        """
        url = f'{self.api_url}credentials/'
        return EntityManager(self._tower,
                             entity_object='Credential',
                             primary_match_field='name',
                             url=url)

    def get_credential_by_name(self, name, credential_type):
        """Retrieves credential matching a certain name.

        Args:
            name: The name of the credential to retrieve.
            credential_type: The type of credential.

        Returns:
            Credential: A credential if found else none.

        Raises:
            InvalidCredentialType: The credential type given as a parameter was not found.

        """
        credential_type_ = self._tower.get_credential_type_by_name(credential_type)
        if not credential_type_:
            raise InvalidCredentialType(name)
        return next(self.credentials.filter({'organization': self.id,
                                             'name__iexact': name,
                                             'credential_type': credential_type_.id}), None)

    def get_credential_by_name_with_type_id(self, name, credential_type_id):
        """Retrieves credential matching a certain name and the provided type by id.

        Args:
            name (str): The name of the credential to retrieve.
            credential_type_id (int): The type of credential.

        Returns:
            Credential: A credential if found else none.

        """
        return next(self.credentials.filter({'organization': self.id,
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
