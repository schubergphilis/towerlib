#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: team.py
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
Main code for team

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import json
import logging

from towerlib.towerlibexceptions import (InvalidUser,
                                         PermissionNotFound,
                                         InvalidProject,
                                         InvalidJobTemplate,
                                         InvalidInventory,
                                         InvalidCredential)
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
LOGGER_BASENAME = '''team'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class Team(Entity):  # pylint: disable=too-many-public-methods
    """Models the team entity of ansible tower"""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)
        self._object_roles = None

    @property
    def name(self):
        """The name of the team

        Returns:
            string: The name of the team

        """
        return self._data.get('name')

    @property
    def description(self):
        """The description of the team

        Returns:
            string: The description of the team

        """
        return self._data.get('description')

    @property
    def organization(self):
        """The Organization of the team

        Returns:
            Organization: The organization of the team

        """
        return self._tower.get_organization_by_id(self._data.get('organization'))

    @property
    def roles(self):
        """The roles

        Returns:
            EntityManager: EntityManager of the roles

        """
        url = self._data.get('related', {}).get('roles')
        return EntityManager(self._tower, entity_object='Role', primary_match_field='name', url=url)

    @property
    def object_roles(self):
        """The object roles

        Returns:
            EntityManager: EntityManager of the object roles supported

        """
        if not self._object_roles:
            url = self._data.get('related', {}).get('object_roles')
            self._object_roles = EntityManager(self._tower,
                                               entity_object='ObjectRole',
                                               primary_match_field='name',
                                               url=url)
        return self._object_roles

    @property
    def object_role_names(self):
        """The names of the object roles

        Returns:
            list: A list of strings for the object_roles

        """
        return (object_role.name for object_role in self.object_roles)

    @property
    def users(self):
        """The users of the team

        Returns:
            EntityManager: EntityManager of the users

        """
        url = self._data.get('related', {}).get('users')
        return EntityManager(self._tower, entity_object='User', primary_match_field='username', url=url)

    @property
    def credentials(self):
        """The credentials of the team

        Returns:
            EntityManager: EntityManager of the credentials

        """
        url = self._data.get('related', {}).get('credentials')
        return EntityManager(self._tower, entity_object='Credential', primary_match_field='name', url=url)

    @property
    def projects(self):
        """The projects of the team

        Returns:
            EntityManager: EntityManager of the projects

        """
        url = self._data.get('related', {}).get('projects')
        return EntityManager(self._tower, entity_object='Project', primary_match_field='name', url=url)

    def add_user_as_member(self, username):
        """Adds a user as a member of the team

        Args:
            username: The username of the user to add

        Returns:
            True on success, False otherwise

        """
        return self._post_user_with_permission(username, 'member')

    def remove_user_as_member(self, username):
        """Removes a user as a member of the team

        Args:
            username: The username of the user to remove

        Returns:
            True on success, False otherwise

        """
        return self._post_user_with_permission(username, 'member', remove=True)

    def add_user_as_admin(self, username):
        """Adds a user as an admin of the team

        Args:
            username: The username of the user to add

        Returns:
            True on success, False otherwise

        """
        return self._post_user_with_permission(username, 'admin')

    def remove_user_as_admin(self, username):
        """Removes a user as an admin of the team

        Args:
            username: The username of the user to remove

        Returns:
            True on success, False otherwise

        """
        return self._post_user_with_permission(username, 'admin', remove=True)

    @staticmethod
    def _get_permission(role_name, object_roles):
        permission = next((role for role in object_roles
                           if role.name.lower() == role_name))
        if not permission:
            raise PermissionNotFound(role_name)
        return permission

    def _post_user_with_permission(self, username, role_name, remove=False):
        permission = self._get_permission(role_name, self.object_roles)
        user = self._tower.get_user_by_username(username)
        if not user:
            raise InvalidUser(username)
        url = '{api}/users/{id}/roles/'.format(api=self._tower.api,
                                               id=user.id)
        payload = {'id': permission.id}
        if remove:
            roles_ids = [role.id for role in user.roles]
            if permission.id not in roles_ids:
                self._logger.warning('{} is not part of the team'.format(username))
                return False
            payload['disassociate'] = True
        response = self._tower.session.post(url, data=json.dumps(payload))
        return response.ok

    def add_project_permission_admin(self, project_name):
        """Adds a project with admin permissions

        Args:
            project_name: The name of the project to add

        Returns:
            True on success, False otherwise

        """
        return self._post_project_permission(project_name, 'admin')

    def add_project_permission_update(self, project_name):
        """Adds a project with update permissions

        Args:
            project_name: The name of the project to add

        Returns:
            True on success, False otherwise

        """
        return self._post_project_permission(project_name, 'update')

    def add_project_permission_use(self, project_name):
        """Adds a project with use permissions

        Args:
            project_name: The name of the project to add

        Returns:
            True on success, False otherwise

        """
        return self._post_project_permission(project_name, 'use')

    def remove_project_permission_admin(self, project_name):
        """Removes a project with admin permissions

        Args:
            project_name: The name of the project to remove

        Returns:
            True on success, False otherwise

        """
        return self._post_project_permission(project_name, 'admin', remove=True)

    def remove_project_permission_update(self, project_name):
        """Removes a project with update permissions

        Args:
            project_name: The name of the project to remove

        Returns:
            True on success, False otherwise

        """
        return self._post_project_permission(project_name, 'update', remove=True)

    def remove_project_permission_use(self, project_name):
        """Removes a project with use permissions

        Args:
            project_name: The name of the project to remove

        Returns:
            True on success, False otherwise

        """
        return self._post_project_permission(project_name, 'use', remove=True)

    def add_job_template_permission_admin(self, job_template_name):
        """Adds a job template with admin permissions

        Args:
            job_template_name: The name of the job template to add

        Returns:
            True on success, False otherwise

        """
        return self._post_job_template_permission(job_template_name, 'admin')

    def add_job_template_permission_execute(self, job_template_name):
        """Adds a job template with execute permissions

        Args:
            job_template_name: The name of the job template to add

        Returns:
            True on success, False otherwise

        """
        return self._post_job_template_permission(job_template_name, 'execute')

    def remove_job_template_permission_admin(self, job_template_name):
        """Removes a job template with admin permissions

        Args:
            job_template_name: The name of the job template to remove

        Returns:
            True on success, False otherwise

        """
        return self._post_job_template_permission(job_template_name, 'admin', remove=True)

    def remove_job_template_permission_execute(self, job_template_name):
        """Removes a job template with execute permissions

        Args:
            job_template_name: The name of the job template to remove

        Returns:
            True on success, False otherwise

        """
        return self._post_job_template_permission(job_template_name, 'execute', remove=True)

    def add_inventory_permission_admin(self, inventory_name):
        """Adds an inventory with admin permissions

        Args:
            inventory_name: The name of the inventory to add

        Returns:
            True on success, False otherwise

        """
        return self._post_inventory_permission(inventory_name, 'admin')

    def add_inventory_permission_use(self, inventory_name):
        """Adds an inventory with use permissions

        Args:
            inventory_name: The name of the inventory to add

        Returns:
            True on success, False otherwise

        """
        return self._post_inventory_permission(inventory_name, 'use')

    def add_inventory_permission_update(self, inventory_name):
        """Adds an inventory with update permissions

        Args:
            inventory_name: The name of the inventory to add

        Returns:
            True on success, False otherwise

        """
        return self._post_inventory_permission(inventory_name, 'update')

    def add_inventory_permission_ad_hoc(self, inventory_name):
        """Adds an inventory with ad hoc permissions

        Args:
            inventory_name: The name of the inventory to add

        Returns:
            True on success, False otherwise

        """
        return self._post_inventory_permission(inventory_name, 'ad hoc')

    def remove_inventory_permission_admin(self, inventory_name):
        """Removes an inventory with admin permissions

        Args:
            inventory_name: The name of the inventory to remove

        Returns:
            True on success, False otherwise

        """
        return self._post_inventory_permission(inventory_name, 'admin', remove=True)

    def remove_inventory_permission_use(self, inventory_name):
        """Removes an inventory with use permissions

        Args:
            inventory_name: The name of the inventory to remove

        Returns:
            True on success, False otherwise

        """
        return self._post_inventory_permission(inventory_name, 'use', remove=True)

    def remove_inventory_permission_update(self, inventory_name):
        """Removes an inventory with update permissions

        Args:
            inventory_name: The name of the inventory to remove

        Returns:
            True on success, False otherwise

        """
        return self._post_inventory_permission(inventory_name, 'update', remove=True)

    def remove_inventory_permission_ad_hoc(self, inventory_name):
        """Removes an inventory with ad hoc permissions

        Args:
            inventory_name: The name of the inventory to remove

        Returns:
            True on success, False otherwise

        """
        return self._post_inventory_permission(inventory_name, 'ad hoc', remove=True)

    def add_credential_permission_admin(self, credential_name):
        """Adds a credential with admin permissions

        Args:
            credential_name: The name of the credential to add

        Returns:
            True on success, False otherwise

        """
        return self._post_credential_permission(credential_name, 'admin')

    def add_credential_permission_use(self, credential_name):
        """Adds a credential with admin permissions

        Args:
            credential_name: The name of the credential to add

        Returns:
            True on success, False otherwise

        """
        return self._post_credential_permission(credential_name, 'use')

    def remove_credential_permission_admin(self, credential_name):
        """Removes a credential with admin permissions

        Args:
            credential_name: The name of the credential to remove

        Returns:
            True on success, False otherwise

        """
        return self._post_credential_permission(credential_name, 'admin', remove=True)

    def remove_credential_permission_use(self, credential_name):
        """Removes a credential with use permissions

        Args:
            credential_name: The name of the credential to remove

        Returns:
            True on success, False otherwise

        """
        return self._post_credential_permission(credential_name, 'use', remove=True)

    def _post_project_permission(self, project_name, permission_name, remove=False):
        project = self._tower.get_project_by_name(project_name)
        if not project:
            raise InvalidProject(project_name)
        return self._post_permission(project.object_roles, permission_name, remove)

    def _post_job_template_permission(self, job_template_name, permission_name, remove=False):
        job_template = self._tower.get_job_template_by_name(job_template_name)
        if not job_template:
            raise InvalidJobTemplate(job_template_name)
        return self._post_permission(job_template.object_roles, permission_name, remove)

    def _post_inventory_permission(self, inventory_name, permission_name, remove=False):
        inventory = self._tower.get_inventory_by_name(inventory_name)
        if not inventory:
            raise InvalidInventory(inventory_name)
        return self._post_permission(inventory.object_roles, permission_name, remove)

    def _post_credential_permission(self, credential_name, permission_name, remove=False):
        credential = self._tower.get_credential_by_name(credential_name)
        if not credential:
            raise InvalidCredential(credential_name)
        return self._post_permission(credential.object_roles, permission_name, remove)

    def _post_permission(self, roles, permission_name, remove=False):
        permission = self._get_permission(permission_name, roles)
        if remove:
            url = '{api}/roles/{id}/teams/'.format(api=self._tower.api,
                                                   id=permission.id)
            payload = {'id': self.id,
                       'disassociate': True}
        else:
            url = '{api}/teams/{id}/roles/'.format(api=self._tower.api,
                                                   id=self.id)
            payload = {'id': permission.id}
        response = self._tower.session.post(url, data=json.dumps(payload))
        return response.ok
