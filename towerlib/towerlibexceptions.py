#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: towerlibexceptions.py
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
Custom exception code for towerlib

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

__author__ = '''Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''2018-01-02'''
__copyright__ = '''Copyright 2018, Costas Tyfoxylos'''
__credits__ = ["Costas Tyfoxylos"]
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<ctyfoxylos@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


class AuthFailed(Exception):
    """The token retirieval failed"""


class InvalidUserLevel(Exception):
    """The value provided is not allowed.

    Valid values ('standard', 'system_auditor', 'system_administrator')
    """


class InvalidOrganization(Exception):
    """The organization provided is not a valid organization"""


class InvalidVariables(Exception):
    """The variables are not valid json"""


class InvalidInventory(Exception):
    """The inventory provided is invalid"""


class InvalidCredentialType(Exception):
    """The credential type provided is invalid."""


class InvalidCredentialTypeKind(Exception):
    """The credential type kind provided is invalid.

    Valid values (u'scm', u'ssh', u'vault', u'net', u'cloud', u'insights')
    """


class InvalidUser(Exception):
    """The user provided is invalid"""


class InvalidTeam(Exception):
    """The team provided is invalid"""


class InvalidCredential(Exception):
    """The credential provided is invalid."""


class InvalidGroup(Exception):
    """The group provided is invalid."""


class InvalidHost(Exception):
    """The host provided is invalid."""


class InvalidProject(Exception):
    """The project provided is not valid"""


class InvalidJobType(Exception):
    """The job type provided is not valid. Valid values (u'run', u'check')"""


class InvalidPlaybook(Exception):
    """The playbook specified does not exist in the project"""


class InvalidInstanceGroup(Exception):
    """The instance group provided does not exist"""


class InvalidVerbosity(Exception):
    """The verbosity level provided is not valid. Valid values (0, 1, 2, 3, 4)"""


class InvalidJobTemplate(Exception):
    """The job template provided is not valid."""


class PermissionNotFound(Exception):
    """The premission was not found in the entity"""
