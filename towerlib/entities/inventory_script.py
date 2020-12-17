#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: inventory_script.py
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
Main code for inventory_script.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import logging
import re
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
LOGGER_BASENAME = '''inventory_script'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class InventoryScript(Entity):
    """Models the inventory script entity of ansible tower."""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def name(self):
        """The name of the inventory script.

        Returns:
            string: The name of the inventory script.

        """
        return self._data.get('name')

    @name.setter
    def name(self, value):
        """Update the name of the inventory script.

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
        """The description of the inventory script.

        Returns:
            string: The description of the inventory script.

        """
        return self._data.get('description')

    @description.setter
    def description(self, value):
        """Update the first name of the inventory script.

        Returns:
            None:

        """
        self._update_values('description', value)

    @property
    def script(self):
        """The script of the inventory script.

        Returns:
            string: The script of the inventory script.

        """
        return self._data.get('script')

    @script.setter
    def script(self, value):
        """Update the script of the inventory script.

        Returns:
            None:

        """
        pattern = '(#!/(usr|bin)/(sh|bash|bin)(/)?(make|env)?)'
        conditions = re.match(pattern, value)
        if conditions:
            self._update_values('script', value)
        else:
            raise InvalidValue('Script content is invalid, it should start with a shebang.')
