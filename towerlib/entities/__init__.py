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

Import all parts from entities here

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""


from towerlib.entities.credential import Credential, CredentialType
from towerlib.entities.group import Group
from towerlib.entities.host import Host
from towerlib.entities.instance import Instance, InstanceGroup
from towerlib.entities.inventory import Inventory
from towerlib.entities.job import (JobRun,
                                   JobSummary,
                                   JobEvent,
                                   JobTemplate,
                                   SystemJob,
                                   ProjectUpdateJob,
                                   AdHocCommandJob,
                                   Job)
from towerlib.entities.role import Role, ObjectRole
from towerlib.entities.core import (Entity,
                                    Config,
                                    LicenseInfo,
                                    LicenseFeatures,
                                    CERTIFICATE_TYPE_KINDS,
                                    JOB_TYPES,
                                    VERBOSITY_LEVELS,
                                    Cluster,
                                    ClusterInstance,
                                    EntityManager)
from towerlib.entities.organization import Organization
from towerlib.entities.project import Project
from towerlib.entities.team import Team
from towerlib.entities.user import User

__author__ = '''Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''2018-01-02'''
__copyright__ = '''Copyright 2018, Costas Tyfoxylos'''
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<ctyfoxylos@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

# This is to 'use' the module(s), so lint doesn't complain

assert Entity
assert Config
assert LicenseInfo
assert LicenseFeatures
assert CERTIFICATE_TYPE_KINDS
assert JOB_TYPES
assert VERBOSITY_LEVELS
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
assert JobTemplate
assert Role
assert ObjectRole
assert JobRun
assert JobSummary
assert JobEvent
assert ProjectUpdateJob
assert SystemJob
assert AdHocCommandJob
assert Job
assert Cluster
assert ClusterInstance
assert EntityManager
