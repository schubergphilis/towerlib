#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: credentials.py
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
Main code for credentials

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import json
import logging

from towerlib.towerlibexceptions import InvalidOrganization
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
LOGGER_BASENAME = '''credentials'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class CredentialType(Entity):
    """Models the credential_type entity of ansible tower"""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def name(self):
        """The name of the credential type

        Returns:
            string: The name of the credential type

        """
        return self._data.get('name')

    @property
    def description(self):
        """The description of the credential type

        Returns:
            string: The description of the credential type

        """
        return self._data.get('description')

    @property
    def kind(self):
        """The kind of the credential type

        Accepted values are : (u'scm', u'ssh', u'vault', u'net', u'cloud', u'insights')

        Returns:
            string: The kind of the credential type

        """
        return self._data.get('kind')

    @property
    def managed_by_tower(self):
        """Flag indicating whether the credential is internal to tower

        Returns:
            bool: True if credential is internal to tower, False if it is user created

        """
        return self._data.get('managed_by_tower')

    @property
    def inputs(self):
        """The inputs of the credential type

        Returns:
            dictionary: A structure of the credential type supported inputs

        """
        return self._data.get('inputs')

    @property
    def injectors(self):
        """The injectors of the credential typs

        Returns:
            dictionary: A structure of the credential type supported injectors

        """
        return self._data.get('injectors')


class Credential(object):  # pylint: disable=too-few-public-methods
    """Credential factory to handle the different credential types returned"""

    def __new__(cls, tower_instance, data):
        entity_type = data.get('credential_type')
        if entity_type == 1:  # pylint: disable=no-else-return
            return MachineCredential(tower_instance, data)
        elif entity_type == 14:
            return VaultCredential(tower_instance, data)
        else:
            return GenericCredential(tower_instance, data)


class GenericCredential(Entity):
    """Models the credential entity of ansible tower"""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)
        self._object_roles = None
        self._payload = ['name',
                         'description',
                         'organization',
                         'user',
                         'team',
                         'credential_type',
                         'inputs']

    @property
    def host(self):
        """The host of the credential

        Returns:
            dictionary: The host structure of the credential

        """
        return self._data.get('summary_fields', {}).get('host')

    @property
    def project(self):
        """The project of the credential

        Returns:
            dictionary: The project structure of the credential

        """
        return self._data.get('summary_fields', {}).get('project')

    @property
    def created_by(self):
        """The user that created the credential

        Returns:
            User: The user that created the credential

        """
        url = self._data.get('related', {}).get('created_by')
        return self._tower._get_object_by_url('User', url)  # pylint: disable=protected-access

    @property
    def modified_by(self):
        """The person that modified the credential last

        Returns:
            User: The user that modified the credential in tower last

        """
        url = self._data.get('related', {}).get('modified_by')
        return self._tower._get_object_by_url('User', url)  # pylint: disable=protected-access

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
    def owner_users(self):
        """The owners of the credential

        Returns:
            EntityManager: EntityManager of the users that are owners

        """
        url = self._data.get('related', {}).get('owner_users')
        return EntityManager(self._tower, entity_object='User', primary_match_field='username', url=url)

    @property
    def owner_teams(self):
        """The owner teams of the credential

        Returns:
            EntityManager: EntityManager of the teams that are owners

        """
        url = self._data.get('related', {}).get('owner_teams')
        return EntityManager(self._tower, entity_object='Team', primary_match_field='name', url=url)

    @property
    def name(self):
        """The name of the credential

        Returns:
            string: The name of the credential

        """
        return self._data.get('name')

    @name.setter
    def name(self, value):
        """Set the name of the credential

        Returns:
            bool: True if successful, False otherwise

        """
        payload = {attribute: self._data.get(attribute)
                   for attribute in self._payload}
        payload['name'] = value
        return self._update_values(payload)

    @property
    def description(self):
        """The description of the credential

        Returns:
            string: The description of the credential

        """
        return self._data.get('description')

    @description.setter
    def description(self, value):
        """Set the description of the credential

        Returns:
            bool: True if successful, False otherwise

        """
        payload = {attribute: self._data.get(attribute)
                   for attribute in self._payload}
        payload['description'] = value
        return self._update_values(payload)

    @property
    def organization(self):
        """The organization the credential is part of

        Returns:
            Organization: The organization the credential is part of

        """
        return self._tower.get_organization_by_id(self._data.get('organization'))

    @organization.setter
    def organization(self, value):
        """Set the organization of the credential

        Returns:
            bool: True if successful, False otherwise

        """
        payload = {attribute: self._data.get(attribute)
                   for attribute in self._payload}
        organization = self._tower.get_organization_by_name(value)
        if not organization:
            raise InvalidOrganization(value)
        payload['organization'] = organization.id
        return self._update_values(payload)

    @property
    def credential_type(self):
        """The type of the credential

        Returns:
            CredentialType: The type of the credential

        """
        return self._tower.get_credential_type_by_id(self._data.get('credential_type'))

    @property
    def inputs(self):
        """The inputs of the credential

        Returns:
            dictionary: A structure of the credential supported inputs

        """
        return self._data.get('inputs')

    def _update_values(self, payload):
        url = '{api}/credentials/{id}/'.format(api=self._tower.api,
                                               id=self.id)
        response = self._tower.session.put(url, data=json.dumps(payload))
        if response.ok:
            self._data = response.json()


class MachineCredential(GenericCredential):
    """Models the machine credential"""

    def __init__(self, tower_instance, data):
        GenericCredential.__init__(self, tower_instance, data)

    @property
    def username(self):
        """The username that is set in the credential

        Returns:
            basestring: The username that is set in the credential

        """
        return self._data.get('inputs', {}).get('username')

    @username.setter
    def username(self, value):
        """Set the username of the credential

        Returns:
            bool: True if successful, False otherwise

        """
        payload = {attribute: self._data.get(attribute)
                   for attribute in self._payload}
        payload['inputs']['username'] = value
        return self._update_values(payload)

    @property
    def password(self):
        """The password that is set in the credential

        Returns:
            basestring: The password that is set in the credential

        """
        return self._data.get('inputs', {}).get('password')

    @password.setter
    def password(self, value):
        """Set the password of the credential

        Returns:
            bool: True if successful, False otherwise

        """
        payload = {attribute: self._data.get(attribute)
                   for attribute in self._payload}
        payload['inputs']['password'] = value
        return self._update_values(payload)


class VaultCredential(GenericCredential):
    """Models the machine credential"""

    def __init__(self, tower_instance, data):
        GenericCredential.__init__(self, tower_instance, data)

    @property
    def token(self):
        """The token that is set in the credential

        Returns:
            basestring: The token that is set in the credential

        """
        return self._data.get('inputs', {}).get('hashi_vault_token')

    @token.setter
    def token(self, value):
        """Set the token of the credential

        Returns:
            bool: True if successful, False otherwise

        """
        payload = {attribute: self._data.get(attribute)
                   for attribute in self._payload}
        payload['inputs']['hashi_vault_token'] = value
        return self._update_values(payload)

    @property
    def vault_address(self):
        """The vault address that is set in the credential

        Returns:
            basestring: The vault address that is set in the credential

        """
        return self._data.get('inputs', {}).get('hashi_vault_addr')

    @vault_address.setter
    def vault_address(self, value):
        """Set the password of the credential

        Returns:
            bool: True if successful, False otherwise

        """
        payload = {attribute: self._data.get(attribute)
                   for attribute in self._payload}
        payload['inputs']['hashi_vault_addr'] = value
        return self._update_values(payload)

    @property
    def ca_host_verify(self):
        """The ca host verify setting that is set in the credential

        Returns:
            basestring: The vault address that is set in the credential

        """
        return self._data.get('inputs', {}).get('hashi_vault_pre_python_279_cahostverify')

    @ca_host_verify.setter
    def ca_host_verify(self, value):
        """Set the ca host verify of the credential

        Returns:
            bool: True if successful, False otherwise

        """
        if value.lower() not in ['no', 'yes']:
            raise ValueError('Value should be either no/yes')
        payload = {attribute: self._data.get(attribute)
                   for attribute in self._payload}
        payload['inputs']['hashi_vault_pre_python_279_cahostverify'] = value.lower()
        return self._update_values(payload)
