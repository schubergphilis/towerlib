#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: inventory source.py
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
from .core import (Entity,
                   validate_max_length)

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

class Settings:
    """Models the settings entity of ansible tower."""

    def __init__(self, tower_instance):
        self._tower = tower_instance

    def _get_settings_data(self, setting_type):
        url = '{api}/settings/{type}/'.format(api=self._tower.api, type=setting_type)
        response = self._tower.session.get(url)
        if not response.ok:
            LOGGER.error('Error getting setting type "%s", response was: "%s"', setting_type, response.text)
        # think about whether we should raise an exception here or instantiate with empty default values
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

    def configure_saml(self, payload):
        return self.saml.configure(payload)

class Saml(Entity):
    """Models the saml entity of ansible tower."""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def organization_information(self):
        return self._data.get('SOCIAL_AUTH_SAML_ORG_INFO')

    def configure(self, payload):
        pass

