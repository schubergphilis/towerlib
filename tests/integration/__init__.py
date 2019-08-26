#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: __init__.py
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
.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from betamax import recorder
from betamax.fixtures import unittest
from requests import Session

import logging

from towerlib import Tower
from .. import placeholders

__author__ = '''Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''2018-05-25'''
__copyright__ = '''Copyright 2018, Costas Tyfoxylos'''
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<ctyfoxylos@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


class TowerMock(Tower):

    def __init__(self, host, username, password, secure=False, ssl_verify=True):
        self._logger = logging.getLogger("TowerMock")
        protocol = 'https' if secure else 'http'
        self.host = '{protocol}://{host}'.format(protocol=protocol, host=host.lower())
        self.api = '{host}/api/v2'.format(host=self.host)
        self.username = username
        self.password = password
        self.session = self._get_authenticated_session(secure, ssl_verify)
        self.mock = True

    def _get_authenticated_session(self, secure, ssl_verify):
        session = Session()
        if secure:
            session.verify = ssl_verify
        session.auth = (self.username, self.password)
        session.headers.update({'content-type': 'application/json'})
        return session


class IntegrationTest(unittest.BetamaxTestCase):

    def setUp(self):
        super(IntegrationTest, self).setUp()
        self.tower = self.setup_tower()
        self.recorder = recorder.Betamax(session=self.tower.session)
        self.recorder.use_cassette(self.generate_cassette_name())
        self.recorder.start()

    @staticmethod
    def setup_tower():
        host = placeholders.get('hostname')
        username = placeholders.get('username')
        password = placeholders.get('password')
        try:
            tower = Tower(host, username, password)
        except Exception:
            tower = TowerMock(host, username, password)
        return tower
