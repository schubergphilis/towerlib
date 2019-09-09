#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: test_core.py
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
test_core
----------------------------------
Tests for `core` module.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from towerlib.entities import (Cluster,
                               EntityManager,
                               Organization,
                               User,
                               Project,
                               Team,
                               Group,
                               Inventory,
                               Host,
                               CredentialType,
                               GenericCredential,
                               JobTemplate)
from towerlib.towerlibexceptions import (AuthFailed,
                                         InvalidOrganization,
                                         InvalidUser,
                                         InvalidCredential,
                                         InvalidProject,
                                         InvalidTeam,
                                         InvalidInventory,
                                         InvalidGroup,
                                         InvalidVariables,
                                         InvalidHost,
                                         InvalidCredentialType,
                                         InvalidPlaybook,
                                         InvalidInstanceGroup,
                                         InvalidJobType,
                                         InvalidVerbosity)


from . import IntegrationTest

__author__ = '''Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''2018-05-25'''
__copyright__ = '''Copyright 2018, Costas Tyfoxylos'''
__credits__ = ["Costas Tyfoxylos"]
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<ctyfoxylos@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


class TestCore(IntegrationTest):

    pass
    # def test_authentication(self):
    #     with self.recorder:
    #         with self.assertRaises(AuthFailed):
    #             self.tower._authenticate(self.recorder.session,
    #                                      self.tower._generate_host_name(placeholders.get('hostname'), secure=False),
    #                                      username='garbage',
    #                                      password='wrongP4ssw0rd',
    #                                      api_url=self.tower.api)
    #
    # def test_configuration(self):
    #     with self.recorder:
    #         self.assertIsNone(self.tower.configuration.license_info.subscription_name)
    #         self.assertTrue(self.tower.configuration.license_info.license_key == 'OPEN')
    #         self.assertTrue(self.tower.configuration.license_info.valid_key)
