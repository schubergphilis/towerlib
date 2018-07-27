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
towerlib package

Import all parts from towerlib here

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
from ._version import __version__

from .towerlibexceptions import (AuthFailed,
                                 InvalidUserLevel,
                                 InvalidOrganization,
                                 InvalidVariables,
                                 InvalidInventory,
                                 InvalidCredentialTypeKind,
                                 InvalidUser,
                                 InvalidTeam,
                                 InvalidCredential,
                                 InvalidGroup,
                                 InvalidHost,
                                 InvalidProject,
                                 InvalidCredentialType,
                                 InvalidPlaybook,
                                 InvalidInstanceGroup,
                                 InvalidJobType,
                                 InvalidVerbosity,
                                 InvalidJobTemplate,
                                 PermissionNotFound)

from .towerlib import Tower
from .entities import (Organization,  # NOQA
                       User,
                       Team,
                       Project,
                       Group,
                       Inventory,
                       Host,
                       Instance,
                       InstanceGroup,
                       CredentialType,
                       Credential,
                       JobTemplate,
                       Job,
                       JobSummary,
                       JobRun,
                       JobEvent,
                       SystemJob,
                       AdHocCommandJob,
                       ProjectUpdateJob,
                       ObjectRole)

__author__ = '''Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''2018-01-02'''
__copyright__ = '''Copyright 2018, Costas Tyfoxylos'''
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<ctyfoxylos@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

# This is to 'use' the module(s), so lint doesn't complain
assert __version__

# assert exceptions
assert AuthFailed
assert InvalidUserLevel
assert InvalidOrganization
assert InvalidVariables
assert InvalidInventory
assert InvalidCredentialTypeKind
assert InvalidUser
assert InvalidTeam
assert InvalidCredential
assert InvalidGroup
assert InvalidHost
assert InvalidProject
assert InvalidCredentialType
assert InvalidPlaybook
assert InvalidInstanceGroup
assert InvalidJobType
assert InvalidVerbosity
assert InvalidJobTemplate
assert PermissionNotFound

# assert objects
assert Tower
assert Organization
assert User
assert Team
assert Project
assert Group
assert Inventory
assert Host
assert Instance
assert InstanceGroup
assert CredentialType
assert Credential
