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

import os
import socket
from base64 import b64encode
from sys import platform
from urllib.parse import quote_plus

import betamax
from betamax_serializers import pretty_json

__author__ = '''Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''2018-05-25'''
__copyright__ = '''Copyright 2018, Costas Tyfoxylos'''
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<ctyfoxylos@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


def b64_string(input_string):
    """Return a base64 encoded string (not bytes) from input_string."""
    return b64encode(input_string.encode('utf-8')).decode('utf-8')


def get_environment_variable(key):
    """Return environment variable or placeholder string."""
    return os.environ.get('TOWERLIB_{}'.format(key.upper()), 'placeholder_{}'.format(key))


placeholders = {value: get_environment_variable(value)
                for value in ['username', 'password', 'hostname', 'install_uuid', 'secure', 'ssl_verify']}

placeholders['basic_auth'] = b64_string('{}:{}'.format(placeholders['username'], placeholders['password']))

betamax.Betamax.register_serializer(pretty_json.PrettyJSONSerializer)
with betamax.Betamax.configure() as config:
    config.cassette_library_dir = 'tests/integration/cassettes'
    config.default_cassette_options['serialize_with'] = 'prettyjson'
    config.default_cassette_options['record_mode'] = 'new_episodes'
    config.default_cassette_options['match_requests_on'] = ['method', 'uri', 'body']
    for key, value in placeholders.items():
        if key == 'username':
            continue
        if key == 'password':
            value = quote_plus(value)


if platform == 'darwin':  # Work around issue with betamax on OS X
    socket.gethostbyname = lambda x: '127.0.0.1'
