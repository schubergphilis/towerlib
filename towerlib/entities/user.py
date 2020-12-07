#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: user.py
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
Main code for user.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import logging

from towerlib.towerlibexceptions import InvalidValue, InvalidRole, InvalidOrganization
from .core import (Entity,
                   EntityManager,
                   validate_max_length,
                   validate_characters)

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
LOGGER_BASENAME = '''user'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class User(Entity):
    """Models the user entity of ansible tower."""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def username(self):
        """The username of the user.

        Returns:
            string: The username of the user.

        """
        return self._data.get('username')

    @username.setter
    def username(self, value):
        """Update the username of the user.

        Returns:
            None:

        """
        max_characters = 150
        valid_metacharacters = '@.+-_'
        conditions = [validate_max_length(value, max_characters),
                      validate_characters(value, extra_chars=valid_metacharacters)]
        if all(conditions):
            self._update_values('username', value)
        else:
            raise InvalidValue(f'{value} is invalid. Condition max_characters must be less or equal to '
                               f'{max_characters} and valid character are only alphanums and {valid_metacharacters}')

    @property
    def password(self):
        """The password of the user.

        Returns:
            string: The masked password value of the user.

        """
        return '*********'

    @password.setter
    def password(self, value):
        """Update the password of the user.

        Returns:
            None:

        """
        self._update_values('password', value)

    @property
    def first_name(self):
        """The first name of the user.

        Returns:
            string: The first name of the user.

        """
        return self._data.get('first_name')

    @first_name.setter
    def first_name(self, value):
        """Update the first name of the user.

        Returns:
            None:

        """
        max_characters = 30
        conditions = [validate_max_length(value, max_characters)]
        if all(conditions):
            self._update_values('first_name', value)
        else:
            raise InvalidValue(f'{value} is invalid. Condition max_characters must be less or equal to '
                               f'{max_characters}')

    @property
    def last_name(self):
        """The last name of the user.

        Returns:
            string: The last name of the user.

        """
        return self._data.get('last_name')

    @last_name.setter
    def last_name(self, value):
        """Update the last name of the user.

        Returns:
            None:

        """
        max_characters = 30
        conditions = [validate_max_length(value, max_characters)]
        if all(conditions):
            self._update_values('last_name', value)
        else:
            raise InvalidValue(value)

    @property
    def email(self):
        """The email of the user.

        Returns:
            string: The email of the user.

        """
        return self._data.get('email')

    @email.setter
    def email(self, value):
        """Update the email address of the user.

        Returns:
            None:

        """
        max_characters = 254
        conditions = [validate_max_length(value, max_characters)]
        if all(conditions):
            self._update_values('email', value)
        else:
            raise InvalidValue(f'{value} is invalid. Condition max_characters must be less or equal to '
                               f'{max_characters}')

    @property
    def is_superuser(self):
        """The superuser status of the user.

        Returns:
            bool: True if the user is a superuser, False otherwise.

        """
        return self._data.get('is_superuser')

    @is_superuser.setter
    def is_superuser(self, value):
        """Update the is_superuser field of the user.

        Returns:
            None:

        """
        self._update_values('is_superuser', value)

    @property
    def is_system_auditor(self):
        """The system auditor status of the user.

        Returns:
            bool: True if the user is a system auditor, False otherwise.

        """
        return self._data.get('is_system_auditor')

    @is_system_auditor.setter
    def is_system_auditor(self, value):
        """Update the is_system_auditor field of the user.

        Returns:
            None:

        """
        self._update_values('is_system_auditor', value)

    @property
    def ldap_dn(self):
        """The ldap dn setting for the user.

        Returns:
            string: The ldap dn entry for the user.

        """
        return self._data.get('ldap_dn')

    @property
    def external_account(self):
        """The external account entry for the user.

        Returns:
            string: The external account entry for the user if it exists.
            None: If no entry exists.

        """
        return self._data.get('external_account')

    @property
    def auth(self):
        """The authentication setting for the user.

        Returns:
            list: Used authentication methods set for the user.

        """
        return self._data.get('auth')

    @property
    def organizations(self):
        """The organizations that the user is part of.

        Returns:
            EntityManager: EntityManager of the organizations.

        """
        url = self._data.get('related', {}).get('organizations')
        return EntityManager(self._tower,
                             entity_object='Organization',
                             primary_match_field='name',
                             url=url)

    @property
    def roles(self):
        """The roles that the user has.

        Returns:
            EntityManager: EntityManager of the roles.

        """
        url = self._data.get('related', {}).get('roles')
        return EntityManager(self._tower,
                             entity_object='Role',
                             primary_match_field='name',
                             url=url)

    @property
    def teams(self):
        """The teams that the user is part of.

        Returns:
            EntityManager: EntityManager of the teams.

        """
        url = self._data.get('related', {}).get('teams')
        return EntityManager(self._tower,
                             entity_object='Team',
                             primary_match_field='name',
                             url=url)

    @property
    def projects(self):
        """The projects that the user is part of.

        Returns:
            EntityManager: EntityManager of the projects.

        """
        url = self._data.get('related', {}).get('projects')
        return EntityManager(self._tower,
                             entity_object='Project',
                             primary_match_field='name',
                             url=url)

    @property
    def credentials(self):
        """The credentials that the user has.

        Returns:
            EntityManager: EntityManager of the credentials.

        """
        url = self._data.get('related', {}).get('credentials')
        return EntityManager(self._tower,
                             entity_object='Credential',
                             primary_match_field='name',
                             url=url)

    @property
    def last_login(self):
        """The last time the user logged in to the system.

        Returns:
            datetime: The datetime object of the date and time of the last login for the user.
            None: If there is no entry for the last login date.

        """
        return self._to_datetime(self._data.get('last_login'))

    def _assign_permission_role(self, role_id, disassociate=False):
        payload = {'id': role_id}
        if disassociate:
            payload['disassociate'] = True
        url = f"{self._tower.host}{self._data.get('related', {}).get('roles')}"
        response = self._tower.session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Error editing the role permissions for user "%s", response was :"%s"', self.username,
                               response.text)
        return response.ok

    def associate_with_organization_role(self, organization, role):
        """Associate a user to an organizational role.

        Args:
            organization: The organization that we want to assign to
            role: The role we want to assign to the object

        Returns:
            bool: If it managed to associate the user to the organization

        """
        organization_ = self._tower.get_organization_by_name(organization)
        if not organization_:
            raise InvalidOrganization(organization)
        role_id = organization_._get_object_role_id(role)  # pylint: disable=protected-access
        if role_id is None:
            raise InvalidRole(role)
        return self._assign_permission_role(role_id)

    def disassociate_from_organization_role(self, organization, role):
        """Disassociate a user to an organizational role.

        Args:
            organization: The organization object that we want to assign to
            role: The role we want to assign to the object

        Returns:
            bool: If it managed to disassociate the user to the organization

        """
        organization_ = self._tower.get_organization_by_name(organization)
        if not organization_:
            raise InvalidOrganization(organization)
        role_id = organization_._get_object_role_id(role)  # pylint: disable=protected-access
        if role_id is None:
            raise InvalidRole(role)
        return self._assign_permission_role(role_id, disassociate=True)
