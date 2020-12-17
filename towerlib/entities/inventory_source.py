#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: inventory source.py
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
Main code for inventory_source.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import logging

from towerlib.towerlibexceptions import InvalidValue
from .core import (Entity,
                   validate_max_length)

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
LOGGER_BASENAME = '''inventory_source'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class InventorySource(Entity):
    """Models the inventory source entity of ansible tower."""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def name(self):
        """The name of the inventory source.

        Returns:
            string: The name of the inventory source.

        """
        return self._data.get('name')

    @name.setter
    def name(self, value):
        """Update the name of the inventory source.

        Returns:
            None:

        """
        max_characters = 512
        conditions = [validate_max_length(value, max_characters)]
        if all(conditions):
            self._update_values('name', value)
        else:
            raise InvalidValue(f'{value} is invalid. Condition max_characters must be less or equal to '
                               f'{max_characters}')

    @property
    def description(self):
        """The description of the inventory source.

        Returns:
            string: The description of the inventory source.

        """
        return self._data.get('description')

    @description.setter
    def description(self, value):
        """Update the first name of the inventory source.

        Returns:
            None

        """
        self._update_values('description', value)

    @property
    def source(self):
        """The source of the inventory source.

        Returns:
            string: The source of the inventory source.

        """
        return self._data.get('source')

    @property
    def source_path(self):
        """The source_path of the inventory source.

        Returns:
            string: The source path of the inventory source.

        """
        return self._data.get('source_path')

    @property
    def source_script(self):
        """The source_script of the inventory source.

        Returns:
            string: The source path of the inventory source.

        """
        return self._data.get('source_script')

    @property
    def source_vars(self):
        """The source_vars of the inventory source.

        Returns:
            string: The source path of the inventory source.

        """
        return self._data.get('source_vars')

    @property
    def source_regions(self):
        """The source_regions of the inventory source.

        Returns:
            string: The source path of the inventory source.

        """
        return self._data.get('source_regions')

    @property
    def instance_filters(self):
        """The instance_filters of the inventory source.

        Returns:
            string: The source path of the inventory source.

        """
        return self._data.get('instance_filters')

    @property
    def overwrite(self):
        """The overwrite of the inventory source.

        Returns:
            string: The source path of the inventory source.

        """
        return self._data.get('overwrite')

    @property
    def overwrite_vars(self):
        """The overwrite_vars of the inventory source.

        Returns:
            string: The source path of the inventory source.

        """
        return self._data.get('overwrite_vars')

    @property
    def timeout(self):
        """The timeout of the inventory source.

        Returns:
            string: The source path of the inventory source.

        """
        return self._data.get('timeout')

    @property
    def verbosity(self):
        """The verbosity of the inventory source.

        Returns:
            string: The source path of the inventory source.

        """
        return self._data.get('verbosity')

    @property
    def update_on_launch(self):
        """The update_on_launch of the inventory source.

        Returns:
            string: The source path of the inventory source.

        """
        return self._data.get('update_on_launch')

    @property
    def update_cache_timeout(self):
        """The update_cache_timeout of the inventory source.

        Returns:
            string: The source path of the inventory source.

        """
        return self._data.get('update_cache_timeout')

    @property
    def source_project(self):
        """The source_project of the inventory source.

        Returns:
            string: The source path of the inventory source.

        """
        return self._data.get('source_project')

    @property
    def update_on_project_update(self):
        """The update_on_project_update of the inventory source.

        Returns:
            string: The source path of the inventory source.

        """
        return self._data.get('update_on_project_update')

    @property
    def inventory(self):
        """The inventory of the inventory source.

        Returns:
            string: The source path of the inventory source.

        """
        return self._data.get('inventory')
