#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: settings.py
#
# Copyright 2019 Yorick Hoorneman
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
Main code for settings.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import logging

from towerlib.towerlibexceptions import InvalidValue
from .core import Entity

__author__ = '''Yorick Hoorneman <yhoorneman@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''2019-11-22'''
__copyright__ = '''Copyright 2019, Yorick Hoorneman'''
__credits__ = ["Yorick Hoorneman"]
__license__ = '''MIT'''
__maintainer__ = '''Yorick Hoorneman'''
__email__ = '''<yhoorneman@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

# This is the main prefix used for logging
LOGGER_BASENAME = '''settings'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


# pylint: disable=too-few-public-methods
class Settings:
    """Models the settings entity of ansible tower."""

    def __init__(self, tower_instance):
        self._tower = tower_instance

    def _get_settings_data(self, setting_type):
        setting_types = ['all',
                         'authentication',
                         'azuread-oauth2',
                         'changed', 'github',
                         'github-org',
                         'github-team',
                         'google-oauth2',
                         'jobs',
                         'ldap',
                         'logging',
                         'named-url',
                         'radius',
                         'saml',
                         'system',
                         'tacacsplus',
                         'ui']
        if not setting_type.lower() in setting_types:
            raise InvalidValue(f'{setting_type} is invalid. The following setting types are allowed:'
                               f'{setting_types}')
        url = f'{self._tower.api}/settings/{setting_type}/'
        response = self._tower.session.get(url)
        if not response.ok:
            LOGGER.error('Error getting setting type "%s", response was: "%s"', setting_type, response.text)
        return response.json() if response.ok else {}

    @property
    def saml(self):
        """The saml settings in tower.

        Returns:
            Saml: The saml settings in tower.

        """
        setting_type = 'saml'
        data = self._get_settings_data(setting_type)
        return Saml(self._tower, data)

    # def configure_saml(self, payload):
    #     """Function to set the whole saml configuration in one go.
    #
    #     Returns:
    #         None:
    #
    #     """
    #     return self.saml.configure(payload)


class Saml(Entity):
    """Models the saml entity of ansible tower."""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def url(self):
        return f'{self._tower.host}/api/v2/settings/saml/'

    @property
    def callback_url(self):
        """The saml callback url.

        Returns:
            string: The saml callback url.

        """
        return self._data.get('SOCIAL_AUTH_SAML_CALLBACK_URL')

    @property
    def enabled_idps(self):
        """The configured IDPS as a dictionary.

        Returns:
            string: The configured IDPS as a dictionary.

        """
        return self._data.get('SOCIAL_AUTH_SAML_ENABLED_IDPS')

    @enabled_idps.setter
    def enabled_idps(self, value):
        """Update the Entity ID, SSO URL and certificate for each identity provider (IdP) in use.

        Returns:
            None:

        """
        self._update_values('SOCIAL_AUTH_SAML_ENABLED_IDPS', value)

    @property
    def extra_data(self):
        """The IDP attributes that are mapped to extra_attributes.

        Returns:
            string: The IDP attributes that are mapped to extra_attributes.

        """
        return self._data.get('SOCIAL_AUTH_SAML_EXTRA_DATA')

    @extra_data.setter
    def extra_data(self, value):
        """Update the IDP attributes that are mapped to extra_attributes.

        Returns:
            None:

        """
        self._update_values('SOCIAL_AUTH_SAML_EXTRA_DATA', value)

    @property
    def metadata_url(self):
        """The saml metadata url.

        Returns:
            string: The saml metadata url.

        """
        return self._data.get('SOCIAL_AUTH_SAML_METADATA_URL')

    @property
    def organization_attributes(self):
        """The saml callback url.

        Returns:
            string: The saml callback url.

        """
        return self._data.get('SOCIAL_AUTH_SAML_ORGANIZATION_ATTR')

    @organization_attributes.setter
    def organization_attributes(self, value):
        """Update the translation of user organization membership into Tower.

        Returns:
            None:

        """
        self._update_values('SOCIAL_AUTH_SAML_ORGANIZATION_ATTR', value)

    @property
    def organization_map(self):
        """The mapping to organization admins/users from social auth accounts.

        Returns:
            string: The mapping to organization admins/users from social auth accounts.

        """
        return self._data.get('SOCIAL_AUTH_SAML_ORGANIZATION_MAP')

    @organization_map.setter
    def organization_map(self, value):
        """Update the mapping to organization admins/users from social auth accounts.

        Control which users are placed into which Tower organizations based on their username and email address.

        Returns:
            None:

        """
        self._update_values('SOCIAL_AUTH_SAML_ORGANIZATION_MAP', value)

    @property
    def organization_information(self):
        """The organization information url.

        Returns:
            string: The organization information url.

        """
        return self._data.get('SOCIAL_AUTH_SAML_ORG_INFO')

    @organization_information.setter
    def organization_information(self, value):
        """Update the organization information url.

        Returns:
            None:

        """
        self._update_values('SOCIAL_AUTH_SAML_ORG_INFO', value)

    @property
    def security_config(self):
        """The saml security config.

        Returns:
            string: The saml security config.

        """
        return self._data.get('SOCIAL_AUTH_SAML_SECURITY_CONFIG')

    @security_config.setter
    def security_config(self, value):
        """Update the saml security config.

        Returns:
            None:

        """
        self._update_values('SOCIAL_AUTH_SAML_SECURITY_CONFIG', value)

    @property
    def sp_entity_id(self):
        """The application-defined unique identifier for SAML service provider (SP) configuration.

        Returns:
            string: The application-defined unique identifier for SAML service provider (SP) configuration.

        """
        return self._data.get('SOCIAL_AUTH_SAML_SP_ENTITY_ID')

    @sp_entity_id.setter
    def sp_entity_id(self, value):
        """Update the application-defined unique identifier for SAML service provider (SP) configuration.

        Returns:
            None:

        """
        self._update_values('SOCIAL_AUTH_SAML_SP_ENTITY_ID', value)

    @property
    def sp_extra(self):
        """The Service Provider configuration setting.

        Returns:
            string: The Service Provider configuration setting.

        """
        return self._data.get('SOCIAL_AUTH_SAML_SP_EXTRA')

    @sp_extra.setter
    def sp_extra(self, value):
        """Update the Service Provider configuration setting.

        Returns:
            None:

        """
        self._update_values('SOCIAL_AUTH_SAML_SP_EXTRA', value)

    @property
    def sp_private_key(self):
        """The private key.

        Returns:
            string: The private key.

        """
        return self._data.get('SOCIAL_AUTH_SAML_SP_PRIVATE_KEY')

    @sp_private_key.setter
    def sp_private_key(self, value):
        """Update the private key.

        Returns:
            None:

        """
        self._update_values('SOCIAL_AUTH_SAML_SP_PRIVATE_KEY', value)

    @property
    def sp_public_cert(self):
        """The public certificate.

        Returns:
            string: The public certificate.

        """
        return self._data.get('SOCIAL_AUTH_SAML_SP_PUBLIC_CERT')

    @sp_public_cert.setter
    def sp_public_cert(self, value):
        """Update the public certificate.

        Returns:
            None:

        """
        self._update_values('SOCIAL_AUTH_SAML_SP_PUBLIC_CERT', value)

    @property
    def support_contact(self):
        """The support contact information.

        Returns:
            string: The support contact information.

        """
        return self._data.get('SOCIAL_AUTH_SAML_SUPPORT_CONTACT')

    @support_contact.setter
    def support_contact(self, value):
        """Update the support contact information.

        Returns:
            None:

        """
        self._update_values('SOCIAL_AUTH_SAML_SUPPORT_CONTACT', value)

    @property
    def team_attributes(self):
        """The translation of user team membership into Tower.

        Returns:
            string: The translation of user team membership into Tower.

        """
        return self._data.get('SOCIAL_AUTH_SAML_TEAM_ATTR')

    @team_attributes.setter
    def team_attributes(self, value):
        """Update the translation of user team membership into Tower.

        Returns:
            None:

        """
        self._update_values('SOCIAL_AUTH_SAML_TEAM_ATTR', value)

    @property
    def team_map(self):
        """The mapping of team members (users) from social auth accounts.

        Returns:
            string: The mapping of team members (users) from social auth accounts.

        """
        return self._data.get('SOCIAL_AUTH_SAML_TEAM_MAP')

    @team_map.setter
    def team_map(self, value):
        """Update the mapping of team members (users) from social auth accounts.

        Returns:
            None:

        """
        self._update_values('SOCIAL_AUTH_SAML_TEAM_MAP', value)

    @property
    def technical_contact(self):
        """The technical contact information.

        Returns:
            string: The technical contact information.

        """
        return self._data.get('SOCIAL_AUTH_SAML_TECHNICAL_CONTACT')

    @technical_contact.setter
    def technical_contact(self, value):
        """Update the technical contact information.

        Returns:
            None:

        """
        self._update_values('SOCIAL_AUTH_SAML_TECHNICAL_CONTACT', value)

    # def configure(self, payload):
    #     """Function to set the whole saml configuration in one go.
    #
    #     Returns:
    #         None:
    #
    #     """
